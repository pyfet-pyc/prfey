# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\etree\ElementTree.py
"""Lightweight XML support for Python.

 XML is an inherently hierarchical data format, and the most natural way to
 represent it is with a tree.  This module has two classes for this purpose:

    1. ElementTree represents the whole XML document as a tree and

    2. Element represents a single node in this tree.

 Interactions with the whole document (reading and writing to/from files) are
 usually done on the ElementTree level.  Interactions with a single XML element
 and its sub-elements are done on the Element level.

 Element is a flexible container object designed to store hierarchical data
 structures in memory. It can be described as a cross between a list and a
 dictionary.  Each Element has a number of properties associated with it:

    'tag' - a string containing the element's name.

    'attributes' - a Python dictionary storing the element's attributes.

    'text' - a string containing the element's text content.

    'tail' - an optional string containing text after the element's end tag.

    And a number of child elements stored in a Python sequence.

 To create an element instance, use the Element constructor,
 or the SubElement factory function.

 You can also use the ElementTree class to wrap an element structure
 and convert it to and from XML.

"""
__all__ = [
 'Comment',
 'dump',
 'Element', 'ElementTree',
 'fromstring', 'fromstringlist',
 'iselement', 'iterparse',
 'parse', 'ParseError',
 'PI', 'ProcessingInstruction',
 'QName',
 'SubElement',
 'tostring', 'tostringlist',
 'TreeBuilder',
 'VERSION',
 'XML', 'XMLID',
 'XMLParser', 'XMLPullParser',
 'register_namespace',
 'canonicalize', 'C14NWriterTarget']
VERSION = '1.3.0'
import sys, re, warnings, io, collections, collections.abc, contextlib
from . import ElementPath

class ParseError(SyntaxError):
    __doc__ = "An error when parsing an XML document.\n\n    In addition to its exception value, a ParseError contains\n    two extra attributes:\n        'code'     - the specific exception code\n        'position' - the line and column of the error\n\n    "


def iselement(element):
    """Return True if *element* appears to be an Element."""
    return hasattr(element, 'tag')


class Element:
    __doc__ = "An XML element.\n\n    This class is the reference implementation of the Element interface.\n\n    An element's length is its number of subelements.  That means if you\n    want to check if an element is truly empty, you should check BOTH\n    its length AND its text attribute.\n\n    The element tag, attribute names, and attribute values can be either\n    bytes or strings.\n\n    *tag* is the element name.  *attrib* is an optional dictionary containing\n    element attributes. *extra* are additional element attributes given as\n    keyword arguments.\n\n    Example form:\n        <tag attrib>text<child/>...</tag>tail\n\n    "
    tag = None
    attrib = None
    text = None
    tail = None

    def __init__(self, tag, attrib={}, **extra):
        if not isinstance(attrib, dict):
            raise TypeError('attrib must be dict, not %s' % (
             attrib.__class__.__name__,))
        self.tag = tag
        self.attrib = {**attrib, **extra}
        self._children = []

    def __repr__(self):
        return '<%s %r at %#x>' % (self.__class__.__name__, self.tag, id(self))

    def makeelement(self, tag, attrib):
        """Create a new element with the same type.

        *tag* is a string containing the element name.
        *attrib* is a dictionary containing the element attributes.

        Do not call this method, use the SubElement factory function instead.

        """
        return self.__class__(tag, attrib)

    def copy(self):
        """Return copy of current element.

        This creates a shallow copy. Subelements will be shared with the
        original tree.

        """
        elem = self.makeelement(self.tag, self.attrib)
        elem.text = self.text
        elem.tail = self.tail
        elem[:] = self
        return elem

    def __len__(self):
        return len(self._children)

    def __bool__(self):
        warnings.warn("The behavior of this method will change in future versions.  Use specific 'len(elem)' or 'elem is not None' test instead.",
          FutureWarning,
          stacklevel=2)
        return len(self._children) != 0

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, element):
        if isinstance(index, slice):
            for elt in element:
                self._assert_is_element(elt)

        else:
            self._assert_is_element(element)
        self._children[index] = element

    def __delitem__(self, index):
        del self._children[index]

    def append(self, subelement):
        """Add *subelement* to the end of this element.

        The new element will appear in document order after the last existing
        subelement (or directly after the text, if it's the first subelement),
        but before the end tag for this element.

        """
        self._assert_is_element(subelement)
        self._children.append(subelement)

    def extend(self, elements):
        """Append subelements from a sequence.

        *elements* is a sequence with zero or more elements.

        """
        for element in elements:
            self._assert_is_element(element)
            self._children.append(element)

    def insert(self, index, subelement):
        """Insert *subelement* at position *index*."""
        self._assert_is_element(subelement)
        self._children.insert(index, subelement)

    def _assert_is_element(self, e):
        if not isinstance(e, _Element_Py):
            raise TypeError('expected an Element, not %s' % type(e).__name__)

    def remove(self, subelement):
        """Remove matching subelement.

        Unlike the find methods, this method compares elements based on
        identity, NOT ON tag value or contents.  To remove subelements by
        other means, the easiest way is to use a list comprehension to
        select what elements to keep, and then use slice assignment to update
        the parent element.

        ValueError is raised if a matching element could not be found.

        """
        self._children.remove(subelement)

    def getchildren(self):
        """(Deprecated) Return all subelements.

        Elements are returned in document order.

        """
        warnings.warn("This method will be removed in future versions.  Use 'list(elem)' or iteration over elem instead.",
          DeprecationWarning,
          stacklevel=2)
        return self._children

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        return ElementPath.find(self, path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """Find text for first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *default* is the value to return if the element was not found,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return text content of first matching element, or default value if
        none was found.  Note that if an element is found having no text
        content, the empty string is returned.

        """
        return ElementPath.findtext(self, path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Returns list containing all matching elements in document order.

        """
        return ElementPath.findall(self, path, namespaces)

    def iterfind(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return an iterable yielding all matching elements in document order.

        """
        return ElementPath.iterfind(self, path, namespaces)

    def clear(self):
        """Reset element.

        This function removes all subelements, clears all attributes, and sets
        the text and tail attributes to None.

        """
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None

    def get(self, key, default=None):
        """Get element attribute.

        Equivalent to attrib.get, but some implementations may handle this a
        bit more efficiently.  *key* is what attribute to look for, and
        *default* is what to return if the attribute was not found.

        Returns a string containing the attribute value, or the default if
        attribute was not found.

        """
        return self.attrib.get(key, default)

    def set(self, key, value):
        """Set element attribute.

        Equivalent to attrib[key] = value, but some implementations may handle
        this a bit more efficiently.  *key* is what attribute to set, and
        *value* is the attribute value to set it to.

        """
        self.attrib[key] = value

    def keys(self):
        """Get list of attribute names.

        Names are returned in an arbitrary order, just like an ordinary
        Python dict.  Equivalent to attrib.keys()

        """
        return self.attrib.keys()

    def items(self):
        """Get element attributes as a sequence.

        The attributes are returned in arbitrary order.  Equivalent to
        attrib.items().

        Return a list of (name, value) tuples.

        """
        return self.attrib.items()

    def iter(self, tag=None):
        """Create tree iterator.

        The iterator loops over the element and all subelements in document
        order, returning all elements with a matching tag.

        If the tree structure is modified during iteration, new or removed
        elements may or may not be included.  To get a stable set, use the
        list() function on the iterator, and loop over the resulting list.

        *tag* is what tags to look for (default is to return all elements)

        Return an iterator containing all the matching elements.

        """
        if tag == '*':
            tag = None
        if tag is None or (self.tag == tag):
            yield self
        for e in self._children:
            yield from e.iter(tag)

    def getiterator(self, tag=None):
        warnings.warn("This method will be removed in future versions.  Use 'elem.iter()' or 'list(elem.iter())' instead.",
          DeprecationWarning,
          stacklevel=2)
        return list(self.iter(tag))

    def itertext(self):
        """Create text iterator.

        The iterator loops over the element and all subelements in document
        order, returning all inner text.

        """
        tag = self.tag
        if not isinstance(tag, str):
            if tag is not None:
                return
        t = self.text
        if t:
            yield t
        for e in self:
            yield from e.itertext()
            t = e.tail
            if t:
                yield t


def SubElement(parent, tag, attrib={}, **extra):
    """Subelement factory which creates an element instance, and appends it
    to an existing parent.

    The element tag, attribute names, and attribute values can be either
    bytes or Unicode strings.

    *parent* is the parent element, *tag* is the subelements name, *attrib* is
    an optional directory containing element attributes, *extra* are
    additional attributes given as keyword arguments.

    """
    attrib = {**attrib, **extra}
    element = parent.makeelement(tag, attrib)
    parent.append(element)
    return element


def Comment(text=None):
    """Comment element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *text* is a string containing the comment string.

    """
    element = Element(Comment)
    element.text = text
    return element


def ProcessingInstruction(target, text=None):
    """Processing Instruction element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *target* is a string containing the processing instruction, *text* is a
    string containing the processing instruction contents, if any.

    """
    element = Element(ProcessingInstruction)
    element.text = target
    if text:
        element.text = element.text + ' ' + text
    return element


PI = ProcessingInstruction

class QName:
    __doc__ = 'Qualified name wrapper.\n\n    This class can be used to wrap a QName attribute value in order to get\n    proper namespace handing on output.\n\n    *text_or_uri* is a string containing the QName value either in the form\n    {uri}local, or if the tag argument is given, the URI part of a QName.\n\n    *tag* is an optional argument which if given, will make the first\n    argument (text_or_uri) be interpreted as a URI, and this argument (tag)\n    be interpreted as a local name.\n\n    '

    def __init__(self, text_or_uri, tag=None):
        if tag:
            text_or_uri = '{%s}%s' % (text_or_uri, tag)
        self.text = text_or_uri

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.text)

    def __hash__(self):
        return hash(self.text)

    def __le__(self, other):
        if isinstance(other, QName):
            return self.text <= other.text
        return self.text <= other

    def __lt__(self, other):
        if isinstance(other, QName):
            return self.text < other.text
        return self.text < other

    def __ge__(self, other):
        if isinstance(other, QName):
            return self.text >= other.text
        return self.text >= other

    def __gt__(self, other):
        if isinstance(other, QName):
            return self.text > other.text
        return self.text > other

    def __eq__(self, other):
        if isinstance(other, QName):
            return self.text == other.text
        return self.text == other


class ElementTree:
    __doc__ = 'An XML element hierarchy.\n\n    This class also provides support for serialization to and from\n    standard XML.\n\n    *element* is an optional root element node,\n    *file* is an optional file handle or file name of an XML file whose\n    contents will be used to initialize the tree with.\n\n    '

    def __init__(self, element=None, file=None):
        self._root = element
        if file:
            self.parse(file)

    def getroot(self):
        """Return root element of this tree."""
        return self._root

    def _setroot(self, element):
        """Replace root element of this tree.

        This will discard the current contents of the tree and replace it
        with the given element.  Use with care!

        """
        self._root = element

    def parse--- This code section failed: ---

 L. 582         0  LOAD_CONST               False
                2  STORE_FAST               'close_source'

 L. 583         4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'source'
                8  LOAD_STR                 'read'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     28  'to 28'

 L. 584        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'source'
               18  LOAD_STR                 'rb'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'source'

 L. 585        24  LOAD_CONST               True
               26  STORE_FAST               'close_source'
             28_0  COME_FROM            12  '12'

 L. 586        28  SETUP_FINALLY       124  'to 124'

 L. 587        30  LOAD_FAST                'parser'
               32  LOAD_CONST               None
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    76  'to 76'

 L. 589        38  LOAD_GLOBAL              XMLParser
               40  CALL_FUNCTION_0       0  ''
               42  STORE_FAST               'parser'

 L. 590        44  LOAD_GLOBAL              hasattr
               46  LOAD_FAST                'parser'
               48  LOAD_STR                 '_parse_whole'
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_FALSE    76  'to 76'

 L. 595        54  LOAD_FAST                'parser'
               56  LOAD_METHOD              _parse_whole
               58  LOAD_FAST                'source'
               60  CALL_METHOD_1         1  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _root

 L. 596        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _root
               70  POP_BLOCK        
               72  CALL_FINALLY        124  'to 124'
               74  RETURN_VALUE     
             76_0  COME_FROM           102  '102'
             76_1  COME_FROM            52  '52'
             76_2  COME_FROM            36  '36'

 L. 598        76  LOAD_FAST                'source'
               78  LOAD_METHOD              read
               80  LOAD_CONST               65536
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'data'

 L. 599        86  LOAD_FAST                'data'
               88  POP_JUMP_IF_TRUE     92  'to 92'

 L. 600        90  JUMP_FORWARD        104  'to 104'
             92_0  COME_FROM            88  '88'

 L. 601        92  LOAD_FAST                'parser'
               94  LOAD_METHOD              feed
               96  LOAD_FAST                'data'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  JUMP_BACK            76  'to 76'
            104_0  COME_FROM            90  '90'

 L. 602       104  LOAD_FAST                'parser'
              106  LOAD_METHOD              close
              108  CALL_METHOD_0         0  ''
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _root

 L. 603       114  LOAD_FAST                'self'
              116  LOAD_ATTR                _root
              118  POP_BLOCK        
              120  CALL_FINALLY        124  'to 124'
              122  RETURN_VALUE     
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            72  '72'
            124_2  COME_FROM_FINALLY    28  '28'

 L. 605       124  LOAD_FAST                'close_source'
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 606       128  LOAD_FAST                'source'
              130  LOAD_METHOD              close
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          
            136_0  COME_FROM           126  '126'
              136  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 72

    def iter(self, tag=None):
        """Create and return tree iterator for the root element.

        The iterator loops over all elements in this tree, in document order.

        *tag* is a string with the tag name to iterate over
        (default is to return all elements).

        """
        return self._root.iter(tag)

    def getiterator(self, tag=None):
        warnings.warn("This method will be removed in future versions.  Use 'tree.iter()' or 'list(tree.iter())' instead.",
          DeprecationWarning,
          stacklevel=2)
        return list(self.iter(tag))

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().find(path), which is Element.find()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.find(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().findtext(path),  which is Element.findtext()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.findtext(path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().findall(path), which is Element.findall().

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return list containing all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.findall(path, namespaces)

    def iterfind(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().iterfind(path), which is element.iterfind()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return an iterable yielding all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.iterfind(path, namespaces)

    def write(self, file_or_filename, encoding=None, xml_declaration=None, default_namespace=None, method=None, *, short_empty_elements=True):
        """Write element tree to a file as XML.

        Arguments:
          *file_or_filename* -- file name or a file object opened for writing

          *encoding* -- the output encoding (default: US-ASCII)

          *xml_declaration* -- bool indicating if an XML declaration should be
                               added to the output. If None, an XML declaration
                               is added if encoding IS NOT either of:
                               US-ASCII, UTF-8, or Unicode

          *default_namespace* -- sets the default XML namespace (for "xmlns")

          *method* -- either "xml" (default), "html, "text", or "c14n"

          *short_empty_elements* -- controls the formatting of elements
                                    that contain no content. If True (default)
                                    they are emitted as a single self-closed
                                    tag, otherwise they are emitted as a pair
                                    of start/end tags

        """
        if not method:
            method = 'xml'
        elif method not in _serialize:
            raise ValueError('unknown method %r' % method)
        if not encoding:
            if method == 'c14n':
                encoding = 'utf-8'
            else:
                encoding = 'us-ascii'
        enc_lower = encoding.lower()
        with _get_writer(file_or_filename, enc_lower) as write:
            if method == 'xml':
                if xml_declaration or (xml_declaration is None and enc_lower not in ('utf-8',
                                                                                     'us-ascii',
                                                                                     'unicode')):
                    declared_encoding = encoding
                    if enc_lower == 'unicode':
                        import locale
                        declared_encoding = locale.getpreferredencoding()
                    write("<?xml version='1.0' encoding='%s'?>\n" % (
                     declared_encoding,))
            if method == 'text':
                _serialize_text(write, self._root)
            else:
                qnames, namespaces = _namespaces(self._root, default_namespace)
                serialize = _serialize[method]
                serialize(write, (self._root), qnames, namespaces, short_empty_elements=short_empty_elements)

    def write_c14n(self, file):
        return self.write(file, method='c14n')


@contextlib.contextmanager
def _get_writer(file_or_filename, encoding):
    try:
        write = file_or_filename.write
    except AttributeError:
        if encoding == 'unicode':
            file = open(file_or_filename, 'w')
        else:
            file = open(file_or_filename, 'w', encoding=encoding, errors='xmlcharrefreplace')
        with file:
            yield file.write
    else:
        if encoding == 'unicode':
            yield write
        else:
            with contextlib.ExitStack() as stack:
                if isinstance(file_or_filename, io.BufferedIOBase):
                    file = file_or_filename
                elif isinstance(file_or_filename, io.RawIOBase):
                    file = io.BufferedWriter(file_or_filename)
                    stack.callback(file.detach)
                else:
                    file = io.BufferedIOBase()
                    file.writable = lambda: True
                    file.write = write
                try:
                    file.seekable = file_or_filename.seekable
                    file.tell = file_or_filename.tell
                except AttributeError:
                    pass
                else:
                    file = io.TextIOWrapper(file, encoding=encoding,
                      errors='xmlcharrefreplace',
                      newline='\n')
                    stack.callback(file.detach)
                    yield file.write


def _namespaces(elem, default_namespace=None):
    qnames = {None: None}
    namespaces = {}
    if default_namespace:
        namespaces[default_namespace] = ''

    def add_qname(qname):
        try:
            if qname[:1] == '{':
                uri, tag = qname[1:].rsplit('}', 1)
                prefix = namespaces.get(uri)
                if prefix is None:
                    prefix = _namespace_map.get(uri)
                    if prefix is None:
                        prefix = 'ns%d' % len(namespaces)
                    if prefix != 'xml':
                        namespaces[uri] = prefix
                if prefix:
                    qnames[qname] = '%s:%s' % (prefix, tag)
                else:
                    qnames[qname] = tag
            else:
                if default_namespace:
                    raise ValueError('cannot use non-qualified names with default_namespace option')
                qnames[qname] = qname
        except TypeError:
            _raise_serialization_error(qname)

    for elem in elem.iter():
        tag = elem.tag
        if isinstance(tag, QName):
            if tag.text not in qnames:
                add_qname(tag.text)
        elif isinstance(tag, str):
            if tag not in qnames:
                add_qname(tag)
        elif tag is not None:
            if tag is not Comment:
                if tag is not PI:
                    _raise_serialization_error(tag)
        for key, value in elem.items():
            if isinstance(key, QName):
                key = key.text
            elif key not in qnames:
                add_qname(key)
            if isinstance(value, QName):
                if value.text not in qnames:
                    add_qname(value.text)
                text = elem.text
                if isinstance(text, QName):
                    if text.text not in qnames:
                        add_qname(text.text)
        else:
            return (
             qnames, namespaces)


def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is Comment:
        write('<!--%s-->' % text)
    elif tag is ProcessingInstruction:
        write('<?%s?>' % text)
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)

        else:
            write('<' + tag)
            items = list(elem.items())
            if items or (namespaces):
                if namespaces:
                    for v, k in sorted((namespaces.items()), key=(lambda x: x[1])):
                        if k:
                            k = ':' + k
                        else:
                            write(' xmlns%s="%s"' % (
                             k,
                             _escape_attrib(v)))

    for k, v in items:
        if isinstance(k, QName):
            k = k.text
        else:
            if isinstance(v, QName):
                v = qnames[v.text]
            else:
                v = _escape_attrib(v)
            write(' %s="%s"' % (qnames[k], v))
    else:
        if text or not len(elem) or short_empty_elements:
            write('>')
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)
            else:
                write('</' + tag + '>')

        else:
            write(' />')
        if elem.tail:
            write(_escape_cdata(elem.tail))


HTML_EMPTY = ('area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input',
              'isindex', 'link', 'meta', 'param')
try:
    HTML_EMPTY = set(HTML_EMPTY)
except NameError:
    pass
else:

    def _serialize_html(write, elem, qnames, namespaces, **kwargs):
        tag = elem.tag
        text = elem.text
        if tag is Comment:
            write('<!--%s-->' % _escape_cdata(text))
        else:
            pass
        if tag is ProcessingInstruction:
            write('<?%s?>' % _escape_cdata(text))
        else:
            tag = qnames[tag]
            if tag is None:
                if text:
                    write(_escape_cdata(text))
                for e in elem:
                    _serialize_html(write, e, qnames, None)

            else:
                write('<' + tag)
                items = list(elem.items())
                if items or (namespaces):
                    if namespaces:
                        for v, k in sorted((namespaces.items()), key=(lambda x: x[1])):
                            if k:
                                k = ':' + k
                            else:
                                write(' xmlns%s="%s"' % (
                                 k,
                                 _escape_attrib(v)))
                        else:
                            for k, v in items:
                                if isinstance(k, QName):
                                    k = k.text
                                else:
                                    if isinstance(v, QName):
                                        v = qnames[v.text]
                                    else:
                                        v = _escape_attrib_html(v)
                                    write(' %s="%s"' % (qnames[k], v))
                            else:
                                write('>')
                                ltag = tag.lower()
                                if not text or ltag == 'script' or ltag == 'style':
                                    write(text)
                                else:
                                    write(_escape_cdata(text))
                                for e in elem:
                                    _serialize_html(write, e, qnames, None)
                                else:
                                    if ltag not in HTML_EMPTY:
                                        write('</' + tag + '>')

        if elem.tail:
            write(_escape_cdata(elem.tail))


    def _serialize_text(write, elem):
        for part in elem.itertext():
            write(part)
        else:
            if elem.tail:
                write(elem.tail)


    _serialize = {'xml':_serialize_xml,  'html':_serialize_html, 
     'text':_serialize_text}

    def register_namespace(prefix, uri):
        """Register a namespace prefix.

    The registry is global, and any existing mapping for either the
    given prefix or the namespace URI will be removed.

    *prefix* is the namespace prefix, *uri* is a namespace uri. Tags and
    attributes in this namespace will be serialized with prefix if possible.

    ValueError is raised if prefix is reserved or is invalid.

    """
        if re.match('ns\\d+$', prefix):
            raise ValueError('Prefix format reserved for internal use')
        for k, v in list(_namespace_map.items()):
            if not k == uri:
                if v == prefix:
                    pass
            del _namespace_map[k]
        else:
            _namespace_map[uri] = prefix


    _namespace_map = {'http://www.w3.org/XML/1998/namespace':'xml', 
     'http://www.w3.org/1999/xhtml':'html', 
     'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf', 
     'http://schemas.xmlsoap.org/wsdl/':'wsdl', 
     'http://www.w3.org/2001/XMLSchema':'xs', 
     'http://www.w3.org/2001/XMLSchema-instance':'xsi', 
     'http://purl.org/dc/elements/1.1/':'dc'}
    register_namespace._namespace_map = _namespace_map

    def _raise_serialization_error(text):
        raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))


    def _escape_cdata(text):
        try:
            if '&' in text:
                text = text.replace('&', '&amp;')
            if '<' in text:
                text = text.replace('<', '&lt;')
            if '>' in text:
                text = text.replace('>', '&gt;')
            return text
        except (TypeError, AttributeError):
            _raise_serialization_error(text)


    def _escape_attrib(text):
        try:
            if '&' in text:
                text = text.replace('&', '&amp;')
            if '<' in text:
                text = text.replace('<', '&lt;')
            if '>' in text:
                text = text.replace('>', '&gt;')
            if '"' in text:
                text = text.replace('"', '&quot;')
            if '\r\n' in text:
                text = text.replace('\r\n', '\n')
            if '\r' in text:
                text = text.replace('\r', '\n')
            if '\n' in text:
                text = text.replace('\n', '&#10;')
            if '\t' in text:
                text = text.replace('\t', '&#09;')
            return text
        except (TypeError, AttributeError):
            _raise_serialization_error(text)


    def _escape_attrib_html(text):
        try:
            if '&' in text:
                text = text.replace('&', '&amp;')
            if '>' in text:
                text = text.replace('>', '&gt;')
            if '"' in text:
                text = text.replace('"', '&quot;')
            return text
        except (TypeError, AttributeError):
            _raise_serialization_error(text)


    def tostring(element, encoding=None, method=None, *, xml_declaration=None, default_namespace=None, short_empty_elements=True):
        """Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which can
    be one of "xml" (default), "html", "text" or "c14n", *default_namespace*
    sets the default XML namespace (for "xmlns").

    Returns an (optionally) encoded string containing the XML data.

    """
        stream = io.StringIO() if encoding == 'unicode' else io.BytesIO()
        ElementTree(element).write(stream, encoding, xml_declaration=xml_declaration,
          default_namespace=default_namespace,
          method=method,
          short_empty_elements=short_empty_elements)
        return stream.getvalue()


    class _ListDataStream(io.BufferedIOBase):
        __doc__ = 'An auxiliary stream accumulating into a list reference.'

        def __init__(self, lst):
            self.lst = lst

        def writable(self):
            return True

        def seekable(self):
            return True

        def write(self, b):
            self.lst.append(b)

        def tell(self):
            return len(self.lst)


    def tostringlist(element, encoding=None, method=None, *, xml_declaration=None, default_namespace=None, short_empty_elements=True):
        lst = []
        stream = _ListDataStream(lst)
        ElementTree(element).write(stream, encoding, xml_declaration=xml_declaration,
          default_namespace=default_namespace,
          method=method,
          short_empty_elements=short_empty_elements)
        return lst


    def dump(elem):
        """Write element tree or element structure to sys.stdout.

    This function should be used for debugging only.

    *elem* is either an ElementTree, or a single Element.  The exact output
    format is implementation dependent.  In this version, it's written as an
    ordinary XML file.

    """
        if not isinstance(elem, ElementTree):
            elem = ElementTree(elem)
        elem.write((sys.stdout), encoding='unicode')
        tail = elem.getroot().tail
        if not tail or tail[(-1)] != '\n':
            sys.stdout.write('\n')


    def parse(source, parser=None):
        """Parse XML document into element tree.

    *source* is a filename or file object containing XML data,
    *parser* is an optional parser instance defaulting to XMLParser.

    Return an ElementTree instance.

    """
        tree = ElementTree
        tree.parse(source, parser)
        return tree


    def iterparse(source, events=None, parser=None):
        """Incrementally parse XML document into ElementTree.

    This class also reports what's going on to the user based on the
    *events* it is initialized with.  The supported events are the strings
    "start", "end", "start-ns" and "end-ns" (the "ns" events are used to get
    detailed namespace information).  If *events* is omitted, only
    "end" events are reported.

    *source* is a filename or file object containing XML data, *events* is
    a list of events to report back, *parser* is an optional parser instance.

    Returns an iterator providing (event, elem) pairs.

    """
        pullparser = XMLPullParser(events=events, _parser=parser)

        def iterator():
            try:
                while True:
                    yield from pullparser.read_events()
                    data = source.read(16384)
                    if not data:
                        pass
                    else:
                        pullparser.feed(data)

                root = pullparser._close_and_return_root()
                yield from pullparser.read_events()
                it.root = root
            finally:
                if close_source:
                    source.close()

            if False:
                yield None

        class IterParseIterator(collections.abc.Iterator):
            __next__ = iterator.__next__

        it = IterParseIterator
        it.root = None
        del iterator
        del IterParseIterator
        close_source = False
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
            close_source = True
        return it


    class XMLPullParser:

        def __init__(self, events=None, *, _parser=None):
            self._events_queue = collections.deque()
            self._parser = _parser or XMLParser(target=(TreeBuilder))
            if events is None:
                events = ('end', )
            self._parser._setevents(self._events_queue, events)

        def feed(self, data):
            """Feed encoded data to parser."""
            if self._parser is None:
                raise ValueError('feed() called after end of stream')
            if data:
                try:
                    self._parser.feed(data)
                except SyntaxError as exc:
                    try:
                        self._events_queue.append(exc)
                    finally:
                        exc = None
                        del exc

        def _close_and_return_root(self):
            root = self._parser.close()
            self._parser = None
            return root

        def close(self):
            """Finish feeding data to parser.

        Unlike XMLParser, does not return the root element. Use
        read_events() to consume elements from XMLPullParser.
        """
            self._close_and_return_root()

        def read_events(self):
            """Return an iterator over currently available (event, elem) pairs.

        Events are consumed from the internal event queue as they are
        retrieved from the iterator.
        """
            events = self._events_queue
            while True:
                if events:
                    event = events.popleft()
                    if isinstance(event, Exception):
                        raise event
                    else:
                        yield event


    def XML(text, parser=None):
        """Parse XML document from string constant.

    This function can be used to embed "XML Literals" in Python code.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
        if not parser:
            parser = XMLParser(target=(TreeBuilder))
        parser.feed(text)
        return parser.close()


    def XMLID(text, parser=None):
        """Parse XML document from string constant for its IDs.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an (Element, dict) tuple, in which the
    dict maps element id:s to elements.

    """
        if not parser:
            parser = XMLParser(target=(TreeBuilder))
        parser.feed(text)
        tree = parser.close()
        ids = {}
        for elem in tree.iter():
            id = elem.get('id')
            if id:
                ids[id] = elem
        else:
            return (
             tree, ids)


    fromstring = XML

    def fromstringlist(sequence, parser=None):
        """Parse XML document from sequence of string fragments.

    *sequence* is a list of other sequence, *parser* is an optional parser
    instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
        if not parser:
            parser = XMLParser(target=(TreeBuilder))
        for text in sequence:
            parser.feed(text)
        else:
            return parser.close()


    class TreeBuilder:
        __doc__ = 'Generic element structure builder.\n\n    This builder converts a sequence of start, data, and end method\n    calls to a well-formed element structure.\n\n    You can use this class to build an element structure using a custom XML\n    parser, or a parser for some other XML-like format.\n\n    *element_factory* is an optional element factory which is called\n    to create new Element instances, as necessary.\n\n    *comment_factory* is a factory to create comments to be used instead of\n    the standard factory.  If *insert_comments* is false (the default),\n    comments will not be inserted into the tree.\n\n    *pi_factory* is a factory to create processing instructions to be used\n    instead of the standard factory.  If *insert_pis* is false (the default),\n    processing instructions will not be inserted into the tree.\n    '

        def __init__(self, element_factory=None, *, comment_factory=None, pi_factory=None, insert_comments=False, insert_pis=False):
            self._data = []
            self._elem = []
            self._last = None
            self._root = None
            self._tail = None
            if comment_factory is None:
                comment_factory = Comment
            self._comment_factory = comment_factory
            self.insert_comments = insert_comments
            if pi_factory is None:
                pi_factory = ProcessingInstruction
            self._pi_factory = pi_factory
            self.insert_pis = insert_pis
            if element_factory is None:
                element_factory = Element
            self._factory = element_factory

        def close(self):
            """Flush builder buffers and return toplevel document Element."""
            assert len(self._elem) == 0, 'missing end tags'
            assert self._root is not None, 'missing toplevel element'
            return self._root

        def _flush(self):
            if self._data:
                if self._last is not None:
                    text = ''.join(self._data)
                    if self._tail:
                        assert self._last.tail is None, 'internal error (tail)'
                        self._last.tail = text
                    else:
                        assert self._last.text is None, 'internal error (text)'
                        self._last.text = text
                self._data = []

        def data(self, data):
            """Add text to current element."""
            self._data.append(data)

        def start(self, tag, attrs):
            """Open new element and return it.

        *tag* is the element name, *attrs* is a dict containing element
        attributes.

        """
            self._flush()
            self._last = elem = self._factory(tag, attrs)
            if self._elem:
                self._elem[(-1)].append(elem)
            elif self._root is None:
                self._root = elem
            self._elem.append(elem)
            self._tail = 0
            return elem

        def end(self, tag):
            """Close and return current Element.

        *tag* is the element name.

        """
            self._flush()
            self._last = self._elem.pop()
            assert self._last.tag == tag, 'end tag mismatch (expected %s, got %s)' % (
             self._last.tag, tag)
            self._tail = 1
            return self._last

        def comment(self, text):
            """Create a comment using the comment_factory.

        *text* is the text of the comment.
        """
            return self._handle_single(self._comment_factory, self.insert_comments, text)

        def pi(self, target, text=None):
            """Create a processing instruction using the pi_factory.

        *target* is the target name of the processing instruction.
        *text* is the data of the processing instruction, or ''.
        """
            return self._handle_single(self._pi_factory, self.insert_pis, target, text)

        def _handle_single(self, factory, insert, *args):
            elem = factory(*args)
            if insert:
                self._flush()
                self._last = elem
                if self._elem:
                    self._elem[(-1)].append(elem)
                self._tail = 1
            return elem


    class XMLParser:
        __doc__ = 'Element structure builder for XML source data based on the expat parser.\n\n    *target* is an optional target object which defaults to an instance of the\n    standard TreeBuilder class, *encoding* is an optional encoding string\n    which if given, overrides the encoding specified in the XML file:\n    http://www.iana.org/assignments/character-sets\n\n    '

        def __init__(self, *, target=None, encoding=None):
            try:
                from xml.parsers import expat
            except ImportError:
                try:
                    import pyexpat as expat
                except ImportError:
                    raise ImportError('No module named expat; use SimpleXMLTreeBuilder instead')

            else:
                parser = expat.ParserCreate(encoding, '}')
                if target is None:
                    target = TreeBuilder
                self.parser = self._parser = parser
                self.target = self._target = target
                self._error = expat.error
                self._names = {}
                parser.DefaultHandlerExpand = self._default
                if hasattr(target, 'start'):
                    parser.StartElementHandler = self._start
                if hasattr(target, 'end'):
                    parser.EndElementHandler = self._end
                if hasattr(target, 'start_ns'):
                    parser.StartNamespaceDeclHandler = self._start_ns
                if hasattr(target, 'end_ns'):
                    parser.EndNamespaceDeclHandler = self._end_ns
                if hasattr(target, 'data'):
                    parser.CharacterDataHandler = target.data
                if hasattr(target, 'comment'):
                    parser.CommentHandler = target.comment
                if hasattr(target, 'pi'):
                    parser.ProcessingInstructionHandler = target.pi
                parser.buffer_text = 1
                parser.ordered_attributes = 1
                parser.specified_attributes = 1
                self._doctype = None
                self.entity = {}
            try:
                self.version = 'Expat %d.%d.%d' % expat.version_info
            except AttributeError:
                pass

        def _setevents(self, events_queue, events_to_report):
            parser = self._parser
            append = events_queue.append
            for event_name in events_to_report:
                if event_name == 'start':
                    parser.ordered_attributes = 1
                    parser.specified_attributes = 1

                    def handler(tag, attrib_in, event=event_name, append=append, start=self._start):
                        append((event, start(tag, attrib_in)))

                    parser.StartElementHandler = handler
                else:
                    if event_name == 'end':

                        def handler(tag, event=event_name, append=append, end=self._end):
                            append((event, end(tag)))

                        parser.EndElementHandler = handler
                    else:
                        if event_name == 'start-ns':
                            if hasattr(self.target, 'start_ns'):

                                def handler(prefix, uri, event=event_name, append=append, start_ns=self._start_ns):
                                    append((event, start_ns(prefix, uri)))

                            else:

                                def handler(prefix, uri, event=event_name, append=append):
                                    append((event, (prefix or '', uri or '')))

                            parser.StartNamespaceDeclHandler = handler
                        else:
                            if event_name == 'end-ns':
                                if hasattr(self.target, 'end_ns'):

                                    def handler(prefix, event=event_name, append=append, end_ns=self._end_ns):
                                        append((event, end_ns(prefix)))

                                else:

                                    def handler(prefix, event=event_name, append=append):
                                        append((event, None))

                                parser.EndNamespaceDeclHandler = handler
                            else:
                                if event_name == 'comment':

                                    def handler(text, event=event_name, append=append, self=self):
                                        append((event, self.target.comment(text)))

                                    parser.CommentHandler = handler
                                else:
                                    if event_name == 'pi':

                                        def handler(pi_target, data, event=event_name, append=append, self=self):
                                            append((event, self.target.pi(pi_target, data)))

                                        parser.ProcessingInstructionHandler = handler
                                    else:
                                        raise ValueError('unknown event %r' % event_name)

        def _raiseerror(self, value):
            err = ParseError(value)
            err.code = value.code
            err.position = (value.lineno, value.offset)
            raise err

        def _fixname(self, key):
            try:
                name = self._names[key]
            except KeyError:
                name = key
                if '}' in name:
                    name = '{' + name
                self._names[key] = name
            else:
                return name

        def _start_ns(self, prefix, uri):
            return self.target.start_ns(prefix or '', uri or '')

        def _end_ns(self, prefix):
            return self.target.end_ns(prefix or '')

        def _start(self, tag, attr_list):
            fixname = self._fixname
            tag = fixname(tag)
            attrib = {}
            if attr_list:
                for i in range(0, len(attr_list), 2):
                    attrib[fixname(attr_list[i])] = attr_list[(i + 1)]

                return self.target.start(tag, attrib)

        def _end(self, tag):
            return self.target.end(self._fixname(tag))

        def _default(self, text):
            prefix = text[:1]
            if prefix == '&':
                try:
                    data_handler = self.target.data
                except AttributeError:
                    return
                else:
                    try:
                        data_handler(self.entity[text[1:-1]])
                    except KeyError:
                        from xml.parsers import expat
                        err = expat.error('undefined entity %s: line %d, column %d' % (
                         text, self.parser.ErrorLineNumber,
                         self.parser.ErrorColumnNumber))
                        err.code = 11
                        err.lineno = self.parser.ErrorLineNumber
                        err.offset = self.parser.ErrorColumnNumber
                        raise err

            elif prefix == '<' and text[:9] == '<!DOCTYPE':
                self._doctype = []
            elif self._doctype is not None:
                if prefix == '>':
                    self._doctype = None
                    return
                text = text.strip()
                if not text:
                    return
                self._doctype.append(text)
                n = len(self._doctype)
                if n > 2:
                    type = self._doctype[1]
                    if type == 'PUBLIC' and n == 4:
                        name, type, pubid, system = self._doctype
                        if pubid:
                            pubid = pubid[1:-1]
                    elif type == 'SYSTEM' and n == 3:
                        name, type, system = self._doctype
                        pubid = None
                    else:
                        return
                    if hasattr(self.target, 'doctype'):
                        self.target.doctype(name, pubid, system[1:-1])
                    elif hasattr(self, 'doctype'):
                        warnings.warn('The doctype() method of XMLParser is ignored.  Define doctype() method on the TreeBuilder target.', RuntimeWarning)
                    self._doctype = None

        def feed(self, data):
            """Feed encoded data to parser."""
            try:
                self.parser.Parse(data, 0)
            except self._error as v:
                try:
                    self._raiseerror(v)
                finally:
                    v = None
                    del v

        def close--- This code section failed: ---

 L.1699         0  SETUP_FINALLY        20  'to 20'

 L.1700         2  LOAD_FAST                'self'
                4  LOAD_ATTR                parser
                6  LOAD_METHOD              Parse
                8  LOAD_STR                 ''
               10  LOAD_CONST               1
               12  CALL_METHOD_2         2  ''
               14  POP_TOP          
               16  POP_BLOCK        
               18  JUMP_FORWARD         66  'to 66'
             20_0  COME_FROM_FINALLY     0  '0'

 L.1701        20  DUP_TOP          
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _error
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    64  'to 64'
               30  POP_TOP          
               32  STORE_FAST               'v'
               34  POP_TOP          
               36  SETUP_FINALLY        52  'to 52'

 L.1702        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _raiseerror
               42  LOAD_FAST                'v'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  BEGIN_FINALLY    
             52_0  COME_FROM_FINALLY    36  '36'
               52  LOAD_CONST               None
               54  STORE_FAST               'v'
               56  DELETE_FAST              'v'
               58  END_FINALLY      
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            28  '28'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            18  '18'

 L.1703        66  SETUP_FINALLY       116  'to 116'
               68  SETUP_FINALLY        82  'to 82'

 L.1704        70  LOAD_FAST                'self'
               72  LOAD_ATTR                target
               74  LOAD_ATTR                close
               76  STORE_FAST               'close_handler'
               78  POP_BLOCK        
               80  JUMP_FORWARD        102  'to 102'
             82_0  COME_FROM_FINALLY    68  '68'

 L.1705        82  DUP_TOP          
               84  LOAD_GLOBAL              AttributeError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   100  'to 100'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L.1706        96  POP_EXCEPT       
               98  JUMP_FORWARD        112  'to 112'
            100_0  COME_FROM            88  '88'
              100  END_FINALLY      
            102_0  COME_FROM            80  '80'

 L.1708       102  LOAD_FAST                'close_handler'
              104  CALL_FUNCTION_0       0  ''
              106  POP_BLOCK        
              108  CALL_FINALLY        116  'to 116'
              110  RETURN_VALUE     
            112_0  COME_FROM            98  '98'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM           108  '108'
            116_1  COME_FROM_FINALLY    66  '66'

 L.1711       116  LOAD_FAST                'self'
              118  DELETE_ATTR              parser
              120  LOAD_FAST                'self'
              122  DELETE_ATTR              _parser

 L.1712       124  LOAD_FAST                'self'
              126  DELETE_ATTR              target
              128  LOAD_FAST                'self'
              130  DELETE_ATTR              _target
              132  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 108


    def canonicalize(xml_data=None, *, out=None, from_file=None, **options):
        """Convert XML to its C14N 2.0 serialised form.

    If *out* is provided, it must be a file or file-like object that receives
    the serialised canonical XML output (text, not bytes) through its ``.write()``
    method.  To write to a file, open it in text mode with encoding "utf-8".
    If *out* is not provided, this function returns the output as text string.

    Either *xml_data* (an XML string) or *from_file* (a file path or
    file-like object) must be provided as input.

    The configuration options are the same as for the ``C14NWriterTarget``.
    """
        if xml_data is None:
            if from_file is None:
                raise ValueError("Either 'xml_data' or 'from_file' must be provided as input")
        sio = None
        if out is None:
            sio = out = io.StringIO()
        parser = XMLParser(target=C14NWriterTarget((out.write), **options))
        if xml_data is not None:
            parser.feed(xml_data)
            parser.close()
        elif from_file is not None:
            parse(from_file, parser=parser)
        if sio is not None:
            return sio.getvalue()


    _looks_like_prefix_name = re.compile('^\\w+:\\w+$', re.UNICODE).match

    class C14NWriterTarget:
        __doc__ = '\n    Canonicalization writer target for the XMLParser.\n\n    Serialises parse events to XML C14N 2.0.\n\n    The *write* function is used for writing out the resulting data stream\n    as text (not bytes).  To write to a file, open it in text mode with encoding\n    "utf-8" and pass its ``.write`` method.\n\n    Configuration options:\n\n    - *with_comments*: set to true to include comments\n    - *strip_text*: set to true to strip whitespace before and after text content\n    - *rewrite_prefixes*: set to true to replace namespace prefixes by "n{number}"\n    - *qname_aware_tags*: a set of qname aware tag names in which prefixes\n                          should be replaced in text content\n    - *qname_aware_attrs*: a set of qname aware attribute names in which prefixes\n                           should be replaced in text content\n    - *exclude_attrs*: a set of attribute names that should not be serialised\n    - *exclude_tags*: a set of tag names that should not be serialised\n    '

        def __init__(self, write, *, with_comments=False, strip_text=False, rewrite_prefixes=False, qname_aware_tags=None, qname_aware_attrs=None, exclude_attrs=None, exclude_tags=None):
            self._write = write
            self._data = []
            self._with_comments = with_comments
            self._strip_text = strip_text
            self._exclude_attrs = set(exclude_attrs) if exclude_attrs else None
            self._exclude_tags = set(exclude_tags) if exclude_tags else None
            self._rewrite_prefixes = rewrite_prefixes
            if qname_aware_tags:
                self._qname_aware_tags = set(qname_aware_tags)
            else:
                self._qname_aware_tags = None
            if qname_aware_attrs:
                self._find_qname_aware_attrs = set(qname_aware_attrs).intersection
            else:
                self._find_qname_aware_attrs = None
            self._declared_ns_stack = [
             [
              ('http://www.w3.org/XML/1998/namespace', 'xml')]]
            self._ns_stack = []
            if not rewrite_prefixes:
                self._ns_stack.append(list(_namespace_map.items()))
            self._ns_stack.append([])
            self._prefix_map = {}
            self._preserve_space = [False]
            self._pending_start = None
            self._root_seen = False
            self._root_done = False
            self._ignored_depth = 0

        def _iter_namespaces(self, ns_stack, _reversed=reversed):
            for namespaces in _reversed(ns_stack):
                if namespaces:
                    yield from namespaces

            if False:
                yield None

        def _resolve_prefix_name(self, prefixed_name):
            prefix, name = prefixed_name.split(':', 1)
            for uri, p in self._iter_namespaces(self._ns_stack):
                if p == prefix:
                    return f"{{{uri}}}{name}"
            else:
                raise ValueError(f'Prefix {prefix} of QName "{prefixed_name}" is not declared in scope')

        def _qname(self, qname, uri=None):
            if uri is None:
                uri, tag = qname[1:].rsplit('}', 1) if qname[:1] == '{' else ('', qname)
            else:
                tag = qname
            prefixes_seen = set
            for u, prefix in self._iter_namespaces(self._declared_ns_stack):
                if u == uri:
                    if prefix not in prefixes_seen:
                        return (
                         f"{prefix}:{tag}" if prefix else tag, tag, uri)
                prefixes_seen.add(prefix)
            else:
                if self._rewrite_prefixes:
                    if uri in self._prefix_map:
                        prefix = self._prefix_map[uri]
                    else:
                        prefix = self._prefix_map[uri] = f"n{len(self._prefix_map)}"
                    self._declared_ns_stack[(-1)].append((uri, prefix))
                    return (
                     f"{prefix}:{tag}", tag, uri)
                if not uri:
                    if '' not in prefixes_seen:
                        return (
                         tag, tag, uri)
                for u, prefix in self._iter_namespaces(self._ns_stack):
                    if u == uri:
                        self._declared_ns_stack[(-1)].append((uri, prefix))
                        return (
                         f"{prefix}:{tag}" if prefix else tag, tag, uri)
                else:
                    if not uri:
                        return (
                         tag, tag, uri)
                    raise ValueError(f'Namespace "{uri}" is not declared in scope')

        def data(self, data):
            if not self._ignored_depth:
                self._data.append(data)

        def _flush(self, _join_text=''.join):
            data = _join_text(self._data)
            del self._data[:]
            if self._strip_text:
                if not self._preserve_space[(-1)]:
                    data = data.strip()
                if self._pending_start is not None:
                    args, self._pending_start = self._pending_start, None
                    if data:
                        qname_text = data if _looks_like_prefix_name(data) else None
                        (self._start)(*args, *(qname_text,))
                        if qname_text is not None:
                            return
                if data:
                    if self._root_seen:
                        self._write(_escape_cdata_c14n(data))

        def start_ns(self, prefix, uri):
            if self._ignored_depth:
                return
            if self._data:
                self._flush()
            self._ns_stack[(-1)].append((uri, prefix))

        def start(self, tag, attrs):
            if self._exclude_tags is not None:
                if self._ignored_depth or (tag in self._exclude_tags):
                    self._ignored_depth += 1
                    return
                if self._data:
                    self._flush()
                new_namespaces = []
                self._declared_ns_stack.append(new_namespaces)
                if self._qname_aware_tags is not None:
                    if tag in self._qname_aware_tags:
                        self._pending_start = (
                         tag, attrs, new_namespaces)
                        return
            self._start(tag, attrs, new_namespaces)

        def _start--- This code section failed: ---

 L.1903         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _exclude_attrs
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    36  'to 36'
               10  LOAD_FAST                'attrs'
               12  POP_JUMP_IF_FALSE    36  'to 36'

 L.1904        14  LOAD_CLOSURE             'self'
               16  BUILD_TUPLE_1         1 
               18  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               20  LOAD_STR                 'C14NWriterTarget._start.<locals>.<dictcomp>'
               22  MAKE_FUNCTION_8          'closure'
               24  LOAD_FAST                'attrs'
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'attrs'
             36_0  COME_FROM            12  '12'
             36_1  COME_FROM             8  '8'

 L.1906        36  LOAD_FAST                'tag'
               38  BUILD_SET_1           1 
               40  LOAD_FAST                'attrs'
               42  BUILD_SET_UNPACK_2     2 
               44  STORE_FAST               'qnames'

 L.1907        46  BUILD_MAP_0           0 
               48  STORE_FAST               'resolved_names'

 L.1910        50  LOAD_FAST                'qname_text'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    86  'to 86'

 L.1911        58  LOAD_DEREF               'self'
               60  LOAD_METHOD              _resolve_prefix_name
               62  LOAD_FAST                'qname_text'
               64  CALL_METHOD_1         1  ''
               66  DUP_TOP          
               68  STORE_FAST               'qname'
               70  LOAD_FAST                'resolved_names'
               72  LOAD_FAST                'qname_text'
               74  STORE_SUBSCR     

 L.1912        76  LOAD_FAST                'qnames'
               78  LOAD_METHOD              add
               80  LOAD_FAST                'qname'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM            56  '56'

 L.1913        86  LOAD_DEREF               'self'
               88  LOAD_ATTR                _find_qname_aware_attrs
               90  LOAD_CONST               None
               92  COMPARE_OP               is-not
               94  POP_JUMP_IF_FALSE   176  'to 176'
               96  LOAD_FAST                'attrs'
               98  POP_JUMP_IF_FALSE   176  'to 176'

 L.1914       100  LOAD_DEREF               'self'
              102  LOAD_METHOD              _find_qname_aware_attrs
              104  LOAD_FAST                'attrs'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'qattrs'

 L.1915       110  LOAD_FAST                'qattrs'
              112  POP_JUMP_IF_FALSE   170  'to 170'

 L.1916       114  LOAD_FAST                'qattrs'
              116  GET_ITER         
            118_0  COME_FROM           166  '166'
            118_1  COME_FROM           136  '136'
              118  FOR_ITER            168  'to 168'
              120  STORE_FAST               'attr_name'

 L.1917       122  LOAD_FAST                'attrs'
              124  LOAD_FAST                'attr_name'
              126  BINARY_SUBSCR    
              128  STORE_FAST               'value'

 L.1918       130  LOAD_GLOBAL              _looks_like_prefix_name
              132  LOAD_FAST                'value'
              134  CALL_FUNCTION_1       1  ''
              136  POP_JUMP_IF_FALSE_BACK   118  'to 118'

 L.1919       138  LOAD_DEREF               'self'
              140  LOAD_METHOD              _resolve_prefix_name
              142  LOAD_FAST                'value'
              144  CALL_METHOD_1         1  ''
              146  DUP_TOP          
              148  STORE_FAST               'qname'
              150  LOAD_FAST                'resolved_names'
              152  LOAD_FAST                'value'
              154  STORE_SUBSCR     

 L.1920       156  LOAD_FAST                'qnames'
              158  LOAD_METHOD              add
              160  LOAD_FAST                'qname'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
              166  JUMP_BACK           118  'to 118'
            168_0  COME_FROM           118  '118'
              168  JUMP_FORWARD        180  'to 180'
            170_0  COME_FROM           112  '112'

 L.1922       170  LOAD_CONST               None
              172  STORE_FAST               'qattrs'
              174  JUMP_FORWARD        180  'to 180'
            176_0  COME_FROM            98  '98'
            176_1  COME_FROM            94  '94'

 L.1924       176  LOAD_CONST               None
              178  STORE_FAST               'qattrs'
            180_0  COME_FROM           174  '174'
            180_1  COME_FROM           168  '168'

 L.1927       180  LOAD_DEREF               'self'
              182  LOAD_ATTR                _qname
              184  STORE_DEREF              'parse_qname'

 L.1928       186  LOAD_CLOSURE             'parse_qname'
              188  BUILD_TUPLE_1         1 
              190  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              192  LOAD_STR                 'C14NWriterTarget._start.<locals>.<dictcomp>'
              194  MAKE_FUNCTION_8          'closure'
              196  LOAD_GLOBAL              sorted

 L.1929       198  LOAD_FAST                'qnames'

 L.1929       200  LOAD_LAMBDA              '<code_object <lambda>>'
              202  LOAD_STR                 'C14NWriterTarget._start.<locals>.<lambda>'
              204  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1928       206  LOAD_CONST               ('key',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  GET_ITER         
              212  CALL_FUNCTION_1       1  ''
              214  STORE_FAST               'parsed_qnames'

 L.1932       216  LOAD_FAST                'new_namespaces'
              218  POP_JUMP_IF_FALSE   244  'to 244'

 L.1933       220  LOAD_LISTCOMP            '<code_object <listcomp>>'
              222  LOAD_STR                 'C14NWriterTarget._start.<locals>.<listcomp>'
              224  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1935       226  LOAD_FAST                'new_namespaces'

 L.1933       228  GET_ITER         
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'attr_list'

 L.1937       234  LOAD_FAST                'attr_list'
              236  LOAD_METHOD              sort
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          
              242  JUMP_FORWARD        248  'to 248'
            244_0  COME_FROM           218  '218'

 L.1940       244  BUILD_LIST_0          0 
              246  STORE_FAST               'attr_list'
            248_0  COME_FROM           242  '242'

 L.1943       248  LOAD_FAST                'attrs'
          250_252  POP_JUMP_IF_FALSE   362  'to 362'

 L.1944       254  LOAD_GLOBAL              sorted
              256  LOAD_FAST                'attrs'
              258  LOAD_METHOD              items
              260  CALL_METHOD_0         0  ''
              262  CALL_FUNCTION_1       1  ''
              264  GET_ITER         
            266_0  COME_FROM           358  '358'
              266  FOR_ITER            362  'to 362'
              268  UNPACK_SEQUENCE_2     2 
              270  STORE_FAST               'k'
              272  STORE_FAST               'v'

 L.1945       274  LOAD_FAST                'qattrs'
              276  LOAD_CONST               None
              278  COMPARE_OP               is-not
          280_282  POP_JUMP_IF_FALSE   320  'to 320'
              284  LOAD_FAST                'k'
              286  LOAD_FAST                'qattrs'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   320  'to 320'
              294  LOAD_FAST                'v'
              296  LOAD_FAST                'resolved_names'
              298  COMPARE_OP               in
          300_302  POP_JUMP_IF_FALSE   320  'to 320'

 L.1946       304  LOAD_FAST                'parsed_qnames'
              306  LOAD_FAST                'resolved_names'
              308  LOAD_FAST                'v'
              310  BINARY_SUBSCR    
              312  BINARY_SUBSCR    
              314  LOAD_CONST               0
              316  BINARY_SUBSCR    
              318  STORE_FAST               'v'
            320_0  COME_FROM           300  '300'
            320_1  COME_FROM           290  '290'
            320_2  COME_FROM           280  '280'

 L.1947       320  LOAD_FAST                'parsed_qnames'
              322  LOAD_FAST                'k'
              324  BINARY_SUBSCR    
              326  UNPACK_SEQUENCE_3     3 
              328  STORE_FAST               'attr_qname'
              330  STORE_FAST               'attr_name'
              332  STORE_FAST               'uri'

 L.1949       334  LOAD_FAST                'attr_list'
              336  LOAD_METHOD              append
              338  LOAD_FAST                'uri'
          340_342  POP_JUMP_IF_FALSE   348  'to 348'
              344  LOAD_FAST                'attr_qname'
              346  JUMP_FORWARD        350  'to 350'
            348_0  COME_FROM           340  '340'
              348  LOAD_FAST                'attr_name'
            350_0  COME_FROM           346  '346'
              350  LOAD_FAST                'v'
              352  BUILD_TUPLE_2         2 
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
          358_360  JUMP_BACK           266  'to 266'
            362_0  COME_FROM           266  '266'
            362_1  COME_FROM           250  '250'

 L.1952       362  LOAD_FAST                'attrs'
              364  LOAD_METHOD              get
              366  LOAD_STR                 '{http://www.w3.org/XML/1998/namespace}space'
              368  CALL_METHOD_1         1  ''
              370  STORE_FAST               'space_behaviour'

 L.1953       372  LOAD_DEREF               'self'
              374  LOAD_ATTR                _preserve_space
              376  LOAD_METHOD              append

 L.1954       378  LOAD_FAST                'space_behaviour'
          380_382  POP_JUMP_IF_FALSE   392  'to 392'
              384  LOAD_FAST                'space_behaviour'
              386  LOAD_STR                 'preserve'
              388  COMPARE_OP               ==
              390  JUMP_FORWARD        400  'to 400'
            392_0  COME_FROM           380  '380'

 L.1955       392  LOAD_DEREF               'self'
              394  LOAD_ATTR                _preserve_space
              396  LOAD_CONST               -1
              398  BINARY_SUBSCR    
            400_0  COME_FROM           390  '390'

 L.1953       400  CALL_METHOD_1         1  ''
              402  POP_TOP          

 L.1958       404  LOAD_DEREF               'self'
              406  LOAD_ATTR                _write
              408  STORE_FAST               'write'

 L.1959       410  LOAD_FAST                'write'
              412  LOAD_STR                 '<'
              414  LOAD_FAST                'parsed_qnames'
              416  LOAD_FAST                'tag'
              418  BINARY_SUBSCR    
              420  LOAD_CONST               0
              422  BINARY_SUBSCR    
              424  BINARY_ADD       
              426  CALL_FUNCTION_1       1  ''
              428  POP_TOP          

 L.1960       430  LOAD_FAST                'attr_list'
          432_434  POP_JUMP_IF_FALSE   460  'to 460'

 L.1961       436  LOAD_FAST                'write'
              438  LOAD_STR                 ''
              440  LOAD_METHOD              join
              442  LOAD_LISTCOMP            '<code_object <listcomp>>'
              444  LOAD_STR                 'C14NWriterTarget._start.<locals>.<listcomp>'
              446  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              448  LOAD_FAST                'attr_list'
              450  GET_ITER         
              452  CALL_FUNCTION_1       1  ''
              454  CALL_METHOD_1         1  ''
              456  CALL_FUNCTION_1       1  ''
              458  POP_TOP          
            460_0  COME_FROM           432  '432'

 L.1962       460  LOAD_FAST                'write'
              462  LOAD_STR                 '>'
              464  CALL_FUNCTION_1       1  ''
              466  POP_TOP          

 L.1965       468  LOAD_FAST                'qname_text'
              470  LOAD_CONST               None
              472  COMPARE_OP               is-not
          474_476  POP_JUMP_IF_FALSE   502  'to 502'

 L.1966       478  LOAD_FAST                'write'
              480  LOAD_GLOBAL              _escape_cdata_c14n
              482  LOAD_FAST                'parsed_qnames'
              484  LOAD_FAST                'resolved_names'
              486  LOAD_FAST                'qname_text'
              488  BINARY_SUBSCR    
              490  BINARY_SUBSCR    
              492  LOAD_CONST               0
              494  BINARY_SUBSCR    
              496  CALL_FUNCTION_1       1  ''
              498  CALL_FUNCTION_1       1  ''
              500  POP_TOP          
            502_0  COME_FROM           474  '474'

 L.1968       502  LOAD_CONST               True
              504  LOAD_DEREF               'self'
              506  STORE_ATTR               _root_seen

 L.1969       508  LOAD_DEREF               'self'
              510  LOAD_ATTR                _ns_stack
              512  LOAD_METHOD              append
              514  BUILD_LIST_0          0 
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

Parse error at or near `BUILD_SET_UNPACK_2' instruction at offset 42

        def end(self, tag):
            if self._ignored_depth:
                self._ignored_depth -= 1
                return
            if self._data:
                self._flush()
            self._write(f"</{self._qname(tag)[0]}>")
            self._preserve_space.pop()
            self._root_done = len(self._preserve_space) == 1
            self._declared_ns_stack.pop()
            self._ns_stack.pop()

        def comment(self, text):
            if not self._with_comments:
                return
            if self._ignored_depth:
                return
            if self._root_done:
                self._write('\n')
            elif self._root_seen:
                if self._data:
                    self._flush()
            self._write(f"<!--{_escape_cdata_c14n(text)}-->")
            if not self._root_seen:
                self._write('\n')

        def pi(self, target, data):
            if self._ignored_depth:
                return
            if self._root_done:
                self._write('\n')
            elif self._root_seen:
                if self._data:
                    self._flush()
            self._write(f"<?{target} {_escape_cdata_c14n(data)}?>" if data else f"<?{target}?>")
            if not self._root_seen:
                self._write('\n')


    def _escape_cdata_c14n(text):
        try:
            if '&' in text:
                text = text.replace('&', '&amp;')
            if '<' in text:
                text = text.replace('<', '&lt;')
            if '>' in text:
                text = text.replace('>', '&gt;')
            if '\r' in text:
                text = text.replace('\r', '&#xD;')
            return text
        except (TypeError, AttributeError):
            _raise_serialization_error(text)


    def _escape_attrib_c14n(text):
        try:
            if '&' in text:
                text = text.replace('&', '&amp;')
            if '<' in text:
                text = text.replace('<', '&lt;')
            if '"' in text:
                text = text.replace('"', '&quot;')
            if '\t' in text:
                text = text.replace('\t', '&#x9;')
            if '\n' in text:
                text = text.replace('\n', '&#xA;')
            if '\r' in text:
                text = text.replace('\r', '&#xD;')
            return text
        except (TypeError, AttributeError):
            _raise_serialization_error(text)


    try:
        _Element_Py = Element
        from _elementtree import *
        from _elementtree import _set_factories
    except ImportError:
        pass
    else:
        _set_factories(Comment, ProcessingInstruction)