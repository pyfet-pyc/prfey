# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\dom\minidom.py
"""Simple implementation of the Level 1 DOM.

Namespaces and other minor Level 2 features are also supported.

parse("foo.xml")

parseString("<foo><bar/></foo>")

Todo:
=====
 * convenience methods for getting elements and text.
 * more testing
 * bring some of the writer and linearizer code into conformance with this
        interface
 * SAX 2 namespaces
"""
import io, xml.dom
from xml.dom import EMPTY_NAMESPACE, EMPTY_PREFIX, XMLNS_NAMESPACE, domreg
from xml.dom.minicompat import *
from xml.dom.xmlbuilder import DOMImplementationLS, DocumentLS
_nodeTypes_with_children = (
 xml.dom.Node.ELEMENT_NODE,
 xml.dom.Node.ENTITY_REFERENCE_NODE)

class Node(xml.dom.Node):
    namespaceURI = None
    parentNode = None
    ownerDocument = None
    nextSibling = None
    previousSibling = None
    prefix = EMPTY_PREFIX

    def __bool__(self):
        return True

    def toxml(self, encoding=None):
        return self.toprettyxml('', '', encoding)

    def toprettyxml(self, indent='\t', newl='\n', encoding=None):
        if encoding is None:
            writer = io.StringIO()
        else:
            writer = io.TextIOWrapper((io.BytesIO()), encoding=encoding,
              errors='xmlcharrefreplace',
              newline='\n')
        if self.nodeType == Node.DOCUMENT_NODE:
            self.writexml(writer, '', indent, newl, encoding)
        else:
            self.writexml(writer, '', indent, newl)
        if encoding is None:
            return writer.getvalue()
        return writer.detach().getvalue()

    def hasChildNodes(self):
        return bool(self.childNodes)

    def _get_childNodes(self):
        return self.childNodes

    def _get_firstChild(self):
        if self.childNodes:
            return self.childNodes[0]

    def _get_lastChild(self):
        if self.childNodes:
            return self.childNodes[(-1)]

    def insertBefore(self, newChild, refChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(newChild.childNodes):
                self.insertBefore(c, refChild)
            else:
                return newChild

        if newChild.nodeType not in self._child_node_types:
            raise xml.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(newChild), repr(self)))
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        if refChild is None:
            self.appendChild(newChild)
        else:
            try:
                index = self.childNodes.index(refChild)
            except ValueError:
                raise xml.dom.NotFoundErr()
            else:
                if newChild.nodeType in _nodeTypes_with_children:
                    _clear_id_cache(self)
                self.childNodes.insert(index, newChild)
                newChild.nextSibling = refChild
                refChild.previousSibling = newChild
                if index:
                    node = self.childNodes[(index - 1)]
                    node.nextSibling = newChild
                    newChild.previousSibling = node
                else:
                    newChild.previousSibling = None
                newChild.parentNode = self
        return newChild

    def appendChild(self, node):
        if node.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            for c in tuple(node.childNodes):
                self.appendChild(c)
            else:
                return node

        if node.nodeType not in self._child_node_types:
            raise xml.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        elif node.nodeType in _nodeTypes_with_children:
            _clear_id_cache(self)
        if node.parentNode is not None:
            node.parentNode.removeChild(node)
        _append_child(self, node)
        node.nextSibling = None
        return node

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType == self.DOCUMENT_FRAGMENT_NODE:
            refChild = oldChild.nextSibling
            self.removeChild(oldChild)
            return self.insertBefore(newChild, refChild)
        if newChild.nodeType not in self._child_node_types:
            raise xml.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(newChild), repr(self)))
        if newChild is oldChild:
            return
        if newChild.parentNode is not None:
            newChild.parentNode.removeChild(newChild)
        try:
            index = self.childNodes.index(oldChild)
        except ValueError:
            raise xml.dom.NotFoundErr()
        else:
            self.childNodes[index] = newChild
            newChild.parentNode = self
            oldChild.parentNode = None
            if newChild.nodeType in _nodeTypes_with_children or oldChild.nodeType in _nodeTypes_with_children:
                _clear_id_cache(self)
            else:
                newChild.nextSibling = oldChild.nextSibling
                newChild.previousSibling = oldChild.previousSibling
                oldChild.nextSibling = None
                oldChild.previousSibling = None
                if newChild.previousSibling:
                    newChild.previousSibling.nextSibling = newChild
                if newChild.nextSibling:
                    newChild.nextSibling.previousSibling = newChild
                return oldChild

    def removeChild(self, oldChild):
        try:
            self.childNodes.remove(oldChild)
        except ValueError:
            raise xml.dom.NotFoundErr()
        else:
            if oldChild.nextSibling is not None:
                oldChild.nextSibling.previousSibling = oldChild.previousSibling
            else:
                if oldChild.previousSibling is not None:
                    oldChild.previousSibling.nextSibling = oldChild.nextSibling
                oldChild.nextSibling = oldChild.previousSibling = None
                if oldChild.nodeType in _nodeTypes_with_children:
                    _clear_id_cache(self)
                oldChild.parentNode = None
                return oldChild

    def normalize(self):
        L = []
        for child in self.childNodes:
            if child.nodeType == Node.TEXT_NODE:
                if not child.data:
                    if L:
                        L[(-1)].nextSibling = child.nextSibling
                    if child.nextSibling:
                        child.nextSibling.previousSibling = child.previousSibling
                    child.unlink()
                elif L and L[(-1)].nodeType == child.nodeType:
                    node = L[(-1)]
                    node.data = node.data + child.data
                    node.nextSibling = child.nextSibling
                    if child.nextSibling:
                        child.nextSibling.previousSibling = node
                    child.unlink()
                else:
                    L.append(child)
            else:
                L.append(child)
                if child.nodeType == Node.ELEMENT_NODE:
                    child.normalize()

        self.childNodes[:] = L

    def cloneNode(self, deep):
        return _clone_node(self, deep, self.ownerDocument or self)

    def isSupported(self, feature, version):
        return self.ownerDocument.implementation.hasFeature(feature, version)

    def _get_localName(self):
        pass

    def isSameNode(self, other):
        return self is other

    def getInterface(self, feature):
        if self.isSupported(feature, None):
            return self
        return

    def getUserData--- This code section failed: ---

 L. 231         0  SETUP_FINALLY        18  'to 18'

 L. 232         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _user_data
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 233        18  DUP_TOP          
               20  LOAD_GLOBAL              AttributeError
               22  LOAD_GLOBAL              KeyError
               24  BUILD_TUPLE_2         2 
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    42  'to 42'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 234        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'
               42  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 38

    def setUserData(self, key, data, handler):
        old = None
        try:
            d = self._user_data
        except AttributeError:
            d = {}
            self._user_data = d
        else:
            if key in d:
                old = d[key][0]
            else:
                if data is None:
                    handler = None
                    if old is not None:
                        del d[key]
                else:
                    d[key] = (
                     data, handler)
                return old

    def _call_user_data_handler(self, operation, src, dst):
        if hasattr(self, '_user_data'):
            for key, (data, handler) in list(self._user_data.items()):
                if handler is not None:
                    handler.handle(operation, key, data, src, dst)

    def unlink(self):
        self.parentNode = self.ownerDocument = None
        if self.childNodes:
            for child in self.childNodes:
                child.unlink()
            else:
                self.childNodes = NodeList()

        self.previousSibling = None
        self.nextSibling = None

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        self.unlink()


defproperty(Node, 'firstChild', doc='First child node, or None.')
defproperty(Node, 'lastChild', doc='Last child node, or None.')
defproperty(Node, 'localName', doc='Namespace-local name of this node.')

def _append_child(self, node):
    childNodes = self.childNodes
    if childNodes:
        last = childNodes[(-1)]
        node.previousSibling = last
        last.nextSibling = node
    childNodes.append(node)
    node.parentNode = self


def _in_document(node):
    while True:
        if node is not None:
            if node.nodeType == Node.DOCUMENT_NODE:
                return True
            node = node.parentNode

    return False


def _write_data(writer, data):
    """Writes datachars to writer."""
    if data:
        data = data.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;').replace('>', '&gt;')
        writer.write(data)


def _get_elements_by_tagName_helper(parent, name, rc):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            if name == '*' or (node.tagName == name):
                rc.append(node)
            _get_elements_by_tagName_helper(node, name, rc)
    else:
        return rc


def _get_elements_by_tagName_ns_helper(parent, nsURI, localName, rc):
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            if not localName == '*':
                if node.localName == localName:
                    if nsURI == '*' or (node.namespaceURI == nsURI):
                        rc.append(node)
                    _get_elements_by_tagName_ns_helper(node, nsURI, localName, rc)
                else:
                    return rc


class DocumentFragment(Node):
    nodeType = Node.DOCUMENT_FRAGMENT_NODE
    nodeName = '#document-fragment'
    nodeValue = None
    attributes = None
    parentNode = None
    _child_node_types = (Node.ELEMENT_NODE,
     Node.TEXT_NODE,
     Node.CDATA_SECTION_NODE,
     Node.ENTITY_REFERENCE_NODE,
     Node.PROCESSING_INSTRUCTION_NODE,
     Node.COMMENT_NODE,
     Node.NOTATION_NODE)

    def __init__(self):
        self.childNodes = NodeList()


class Attr(Node):
    __slots__ = ('_name', '_value', 'namespaceURI', '_prefix', 'childNodes', '_localName',
                 'ownerDocument', 'ownerElement')
    nodeType = Node.ATTRIBUTE_NODE
    attributes = None
    specified = False
    _is_id = False
    _child_node_types = (
     Node.TEXT_NODE, Node.ENTITY_REFERENCE_NODE)

    def __init__(self, qName, namespaceURI=EMPTY_NAMESPACE, localName=None, prefix=None):
        self.ownerElement = None
        self._name = qName
        self.namespaceURI = namespaceURI
        self._prefix = prefix
        self.childNodes = NodeList()
        self.childNodes.append(Text())

    def _get_localName(self):
        try:
            return self._localName
        except AttributeError:
            return self.nodeName.split(':', 1)[(-1)]

    def _get_specified(self):
        return self.specified

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value
        if self.ownerElement is not None:
            _clear_id_cache(self.ownerElement)

    nodeName = name = property(_get_name, _set_name)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.childNodes[0].data = value
        if self.ownerElement is not None:
            _clear_id_cache(self.ownerElement)
        self.childNodes[0].data = value

    nodeValue = value = property(_get_value, _set_value)

    def _get_prefix(self):
        return self._prefix

    def _set_prefix(self, prefix):
        nsuri = self.namespaceURI
        if prefix == 'xmlns':
            if nsuri:
                if nsuri != XMLNS_NAMESPACE:
                    raise xml.dom.NamespaceErr("illegal use of 'xmlns' prefix for the wrong namespace")
        self._prefix = prefix
        if prefix is None:
            newName = self.localName
        else:
            newName = '%s:%s' % (prefix, self.localName)
        if self.ownerElement:
            _clear_id_cache(self.ownerElement)
        self.name = newName

    prefix = property(_get_prefix, _set_prefix)

    def unlink(self):
        elem = self.ownerElement
        if elem is not None:
            del elem._attrs[self.nodeName]
            del elem._attrsNS[(self.namespaceURI, self.localName)]
            if self._is_id:
                self._is_id = False
                elem._magic_id_nodes -= 1
                self.ownerDocument._magic_id_count -= 1
        for child in self.childNodes:
            child.unlink()
        else:
            del self.childNodes[:]

    def _get_isId(self):
        if self._is_id:
            return True
        doc = self.ownerDocument
        elem = self.ownerElement
        if doc is None or (elem is None):
            return False
        info = doc._get_elem_info(elem)
        if info is None:
            return False
        if self.namespaceURI:
            return info.isIdNS(self.namespaceURI, self.localName)
        return info.isId(self.nodeName)

    def _get_schemaType(self):
        doc = self.ownerDocument
        elem = self.ownerElement
        if doc is None or (elem is None):
            return _no_type
        info = doc._get_elem_info(elem)
        if info is None:
            return _no_type
        if self.namespaceURI:
            return info.getAttributeTypeNS(self.namespaceURI, self.localName)
        return info.getAttributeType(self.nodeName)


defproperty(Attr, 'isId', doc='True if this attribute is an ID.')
defproperty(Attr, 'localName', doc='Namespace-local name of this attribute.')
defproperty(Attr, 'schemaType', doc='Schema type for this attribute.')

class NamedNodeMap(object):
    __doc__ = "The attribute list is a transient interface to the underlying\n    dictionaries.  Mutations here will change the underlying element's\n    dictionary.\n\n    Ordering is imposed artificially and does not reflect the order of\n    attributes as found in an input document.\n    "
    __slots__ = ('_attrs', '_attrsNS', '_ownerElement')

    def __init__(self, attrs, attrsNS, ownerElement):
        self._attrs = attrs
        self._attrsNS = attrsNS
        self._ownerElement = ownerElement

    def _get_length(self):
        return len(self._attrs)

    def item--- This code section failed: ---

 L. 490         0  SETUP_FINALLY        26  'to 26'

 L. 491         2  LOAD_FAST                'self'
                4  LOAD_GLOBAL              list
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _attrs
               10  LOAD_METHOD              keys
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_FAST                'index'
               18  BINARY_SUBSCR    
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 492        26  DUP_TOP          
               28  LOAD_GLOBAL              IndexError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 493        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 42

    def items(self):
        L = []
        for node in self._attrs.values():
            L.append((node.nodeName, node.value))
        else:
            return L

    def itemsNS(self):
        L = []
        for node in self._attrs.values():
            L.append(((node.namespaceURI, node.localName), node.value))
        else:
            return L

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self._attrs
        return key in self._attrsNS

    def keys(self):
        return self._attrs.keys()

    def keysNS(self):
        return self._attrsNS.keys()

    def values(self):
        return self._attrs.values()

    def get(self, name, value=None):
        return self._attrs.get(name, value)

    __len__ = _get_length

    def _cmp(self, other):
        if self._attrs is getattr(other, '_attrs', None):
            return 0
        return (id(self) > id(other)) - (id(self) < id(other))

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __getitem__(self, attname_or_tuple):
        if isinstance(attname_or_tuple, tuple):
            return self._attrsNS[attname_or_tuple]
        return self._attrs[attname_or_tuple]

    def __setitem__(self, attname, value):
        if isinstance(value, str):
            try:
                node = self._attrs[attname]
            except KeyError:
                node = Attr(attname)
                node.ownerDocument = self._ownerElement.ownerDocument
                self.setNamedItem(node)
            else:
                node.value = value
        else:
            if not isinstance(value, Attr):
                raise TypeError('value must be a string or Attr object')
            node = value
            self.setNamedItem(node)

    def getNamedItem--- This code section failed: ---

 L. 571         0  SETUP_FINALLY        14  'to 14'

 L. 572         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _attrs
                6  LOAD_FAST                'name'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 573        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 574        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30

    def getNamedItemNS--- This code section failed: ---

 L. 577         0  SETUP_FINALLY        18  'to 18'

 L. 578         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _attrsNS
                6  LOAD_FAST                'namespaceURI'
                8  LOAD_FAST                'localName'
               10  BUILD_TUPLE_2         2 
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 579        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 580        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 34

    def removeNamedItem(self, name):
        n = self.getNamedItem(name)
        if n is not None:
            _clear_id_cache(self._ownerElement)
            del self._attrs[n.nodeName]
            del self._attrsNS[(n.namespaceURI, n.localName)]
            if hasattr(n, 'ownerElement'):
                n.ownerElement = None
            return n
        raise xml.dom.NotFoundErr()

    def removeNamedItemNS(self, namespaceURI, localName):
        n = self.getNamedItemNS(namespaceURI, localName)
        if n is not None:
            _clear_id_cache(self._ownerElement)
            del self._attrsNS[(n.namespaceURI, n.localName)]
            del self._attrs[n.nodeName]
            if hasattr(n, 'ownerElement'):
                n.ownerElement = None
            return n
        raise xml.dom.NotFoundErr()

    def setNamedItem(self, node):
        if not isinstance(node, Attr):
            raise xml.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        old = self._attrs.get(node.name)
        if old:
            old.unlink()
        self._attrs[node.name] = node
        self._attrsNS[(node.namespaceURI, node.localName)] = node
        node.ownerElement = self._ownerElement
        _clear_id_cache(node.ownerElement)
        return old

    def setNamedItemNS(self, node):
        return self.setNamedItem(node)

    def __delitem__(self, attname_or_tuple):
        node = self[attname_or_tuple]
        _clear_id_cache(node.ownerElement)
        node.unlink()

    def __getstate__(self):
        return (
         self._attrs, self._attrsNS, self._ownerElement)

    def __setstate__(self, state):
        self._attrs, self._attrsNS, self._ownerElement = state


defproperty(NamedNodeMap, 'length', doc='Number of nodes in the NamedNodeMap.')
AttributeList = NamedNodeMap

class TypeInfo(object):
    __slots__ = ('namespace', 'name')

    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    def __repr__(self):
        if self.namespace:
            return '<%s %r (from %r)>' % (self.__class__.__name__, self.name,
             self.namespace)
        return '<%s %r>' % (self.__class__.__name__, self.name)

    def _get_name(self):
        return self.name

    def _get_namespace(self):
        return self.namespace


_no_type = TypeInfo(None, None)

class Element(Node):
    __slots__ = ('ownerDocument', 'parentNode', 'tagName', 'nodeName', 'prefix', 'namespaceURI',
                 '_localName', 'childNodes', '_attrs', '_attrsNS', 'nextSibling',
                 'previousSibling')
    nodeType = Node.ELEMENT_NODE
    nodeValue = None
    schemaType = _no_type
    _magic_id_nodes = 0
    _child_node_types = (
     Node.ELEMENT_NODE,
     Node.PROCESSING_INSTRUCTION_NODE,
     Node.COMMENT_NODE,
     Node.TEXT_NODE,
     Node.CDATA_SECTION_NODE,
     Node.ENTITY_REFERENCE_NODE)

    def __init__(self, tagName, namespaceURI=EMPTY_NAMESPACE, prefix=None, localName=None):
        self.parentNode = None
        self.tagName = self.nodeName = tagName
        self.prefix = prefix
        self.namespaceURI = namespaceURI
        self.childNodes = NodeList()
        self.nextSibling = self.previousSibling = None
        self._attrs = None
        self._attrsNS = None

    def _ensure_attributes(self):
        if self._attrs is None:
            self._attrs = {}
            self._attrsNS = {}

    def _get_localName(self):
        try:
            return self._localName
        except AttributeError:
            return self.tagName.split(':', 1)[(-1)]

    def _get_tagName(self):
        return self.tagName

    def unlink(self):
        if self._attrs is not None:
            for attr in list(self._attrs.values()):
                attr.unlink()

        self._attrs = None
        self._attrsNS = None
        Node.unlink(self)

    def getAttribute--- This code section failed: ---

 L. 721         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _attrs
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 722        10  LOAD_STR                 ''
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 723        14  SETUP_FINALLY        30  'to 30'

 L. 724        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _attrs
               20  LOAD_FAST                'attname'
               22  BINARY_SUBSCR    
               24  LOAD_ATTR                value
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    14  '14'

 L. 725        30  DUP_TOP          
               32  LOAD_GLOBAL              KeyError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 726        44  POP_EXCEPT       
               46  LOAD_STR                 ''
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'
               50  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 46

    def getAttributeNS--- This code section failed: ---

 L. 729         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _attrsNS
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 730        10  LOAD_STR                 ''
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 731        14  SETUP_FINALLY        34  'to 34'

 L. 732        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _attrsNS
               20  LOAD_FAST                'namespaceURI'
               22  LOAD_FAST                'localName'
               24  BUILD_TUPLE_2         2 
               26  BINARY_SUBSCR    
               28  LOAD_ATTR                value
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    14  '14'

 L. 733        34  DUP_TOP          
               36  LOAD_GLOBAL              KeyError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 734        48  POP_EXCEPT       
               50  LOAD_STR                 ''
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 50

    def setAttribute(self, attname, value):
        attr = self.getAttributeNode(attname)
        if attr is None:
            attr = Attr(attname)
            attr.value = value
            attr.ownerDocument = self.ownerDocument
            self.setAttributeNode(attr)
        elif value != attr.value:
            attr.value = value
            if attr.isId:
                _clear_id_cache(self)

    def setAttributeNS(self, namespaceURI, qualifiedName, value):
        prefix, localname = _nssplit(qualifiedName)
        attr = self.getAttributeNodeNS(namespaceURI, localname)
        if attr is None:
            attr = Attr(qualifiedName, namespaceURI, localname, prefix)
            attr.value = value
            attr.ownerDocument = self.ownerDocument
            self.setAttributeNode(attr)
        else:
            if value != attr.value:
                attr.value = value
                if attr.isId:
                    _clear_id_cache(self)
            if attr.prefix != prefix:
                attr.prefix = prefix
                attr.nodeName = qualifiedName

    def getAttributeNode(self, attrname):
        if self._attrs is None:
            return
        return self._attrs.get(attrname)

    def getAttributeNodeNS(self, namespaceURI, localName):
        if self._attrsNS is None:
            return
        return self._attrsNS.get((namespaceURI, localName))

    def setAttributeNode(self, attr):
        if attr.ownerElement not in (None, self):
            raise xml.dom.InuseAttributeErr('attribute node already owned')
        self._ensure_attributes()
        old1 = self._attrs.get(attr.name, None)
        if old1 is not None:
            self.removeAttributeNode(old1)
        old2 = self._attrsNS.get((attr.namespaceURI, attr.localName), None)
        if old2 is not None:
            if old2 is not old1:
                self.removeAttributeNode(old2)
        _set_attribute_node(self, attr)
        if old1 is not attr:
            return old1
        if old2 is not attr:
            return old2

    setAttributeNodeNS = setAttributeNode

    def removeAttribute(self, name):
        if self._attrsNS is None:
            raise xml.dom.NotFoundErr()
        try:
            attr = self._attrs[name]
        except KeyError:
            raise xml.dom.NotFoundErr()
        else:
            self.removeAttributeNode(attr)

    def removeAttributeNS(self, namespaceURI, localName):
        if self._attrsNS is None:
            raise xml.dom.NotFoundErr()
        try:
            attr = self._attrsNS[(namespaceURI, localName)]
        except KeyError:
            raise xml.dom.NotFoundErr()
        else:
            self.removeAttributeNode(attr)

    def removeAttributeNode(self, node):
        if node is None:
            raise xml.dom.NotFoundErr()
        try:
            self._attrs[node.name]
        except KeyError:
            raise xml.dom.NotFoundErr()
        else:
            _clear_id_cache(self)
            node.unlink()
            node.ownerDocument = self.ownerDocument
            return node

    removeAttributeNodeNS = removeAttributeNode

    def hasAttribute(self, name):
        if self._attrs is None:
            return False
        return name in self._attrs

    def hasAttributeNS(self, namespaceURI, localName):
        if self._attrsNS is None:
            return False
        return (namespaceURI, localName) in self._attrsNS

    def getElementsByTagName(self, name):
        return _get_elements_by_tagName_helper(self, name, NodeList())

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _get_elements_by_tagName_ns_helper(self, namespaceURI, localName, NodeList())

    def __repr__(self):
        return '<DOM Element: %s at %#x>' % (self.tagName, id(self))

    def writexml(self, writer, indent='', addindent='', newl=''):
        writer.write(indent + '<' + self.tagName)
        attrs = self._get_attributes()
        for a_name in attrs.keys():
            writer.write(' %s="' % a_name)
            _write_data(writer, attrs[a_name].value)
            writer.write('"')
        else:
            if self.childNodes:
                writer.write('>')
                if len(self.childNodes) == 1 and self.childNodes[0].nodeType in (
                 Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                    self.childNodes[0].writexml(writer, '', '', '')
                else:
                    writer.write(newl)
                    for node in self.childNodes:
                        node.writexml(writer, indent + addindent, addindent, newl)
                    else:
                        writer.write(indent)

                writer.write('</%s>%s' % (self.tagName, newl))
            else:
                writer.write('/>%s' % newl)

    def _get_attributes(self):
        self._ensure_attributes()
        return NamedNodeMap(self._attrs, self._attrsNS, self)

    def hasAttributes(self):
        if self._attrs:
            return True
        return False

    def setIdAttribute(self, name):
        idAttr = self.getAttributeNode(name)
        self.setIdAttributeNode(idAttr)

    def setIdAttributeNS(self, namespaceURI, localName):
        idAttr = self.getAttributeNodeNS(namespaceURI, localName)
        self.setIdAttributeNode(idAttr)

    def setIdAttributeNode(self, idAttr):
        if not (idAttr is None or self.isSameNode(idAttr.ownerElement)):
            raise xml.dom.NotFoundErr()
        if _get_containing_entref(self) is not None:
            raise xml.dom.NoModificationAllowedErr()
        if not idAttr._is_id:
            idAttr._is_id = True
            self._magic_id_nodes += 1
            self.ownerDocument._magic_id_count += 1
            _clear_id_cache(self)


defproperty(Element, 'attributes', doc='NamedNodeMap of attributes on the element.')
defproperty(Element, 'localName', doc='Namespace-local name of this element.')

def _set_attribute_node(element, attr):
    _clear_id_cache(element)
    element._ensure_attributes()
    element._attrs[attr.name] = attr
    element._attrsNS[(attr.namespaceURI, attr.localName)] = attr
    attr.ownerElement = element


class Childless:
    __doc__ = 'Mixin that makes childless-ness easy to implement and avoids\n    the complexity of the Node methods that deal with children.\n    '
    __slots__ = ()
    attributes = None
    childNodes = EmptyNodeList()
    firstChild = None
    lastChild = None

    def _get_firstChild(self):
        pass

    def _get_lastChild(self):
        pass

    def appendChild(self, node):
        raise xml.dom.HierarchyRequestErr(self.nodeName + ' nodes cannot have children')

    def hasChildNodes(self):
        return False

    def insertBefore(self, newChild, refChild):
        raise xml.dom.HierarchyRequestErr(self.nodeName + ' nodes do not have children')

    def removeChild(self, oldChild):
        raise xml.dom.NotFoundErr(self.nodeName + ' nodes do not have children')

    def normalize(self):
        pass

    def replaceChild(self, newChild, oldChild):
        raise xml.dom.HierarchyRequestErr(self.nodeName + ' nodes do not have children')


class ProcessingInstruction(Childless, Node):
    nodeType = Node.PROCESSING_INSTRUCTION_NODE
    __slots__ = ('target', 'data')

    def __init__(self, target, data):
        self.target = target
        self.data = data

    def _get_nodeValue(self):
        return self.data

    def _set_nodeValue(self, value):
        self.data = value

    nodeValue = property(_get_nodeValue, _set_nodeValue)

    def _get_nodeName(self):
        return self.target

    def _set_nodeName(self, value):
        self.target = value

    nodeName = property(_get_nodeName, _set_nodeName)

    def writexml(self, writer, indent='', addindent='', newl=''):
        writer.write('%s<?%s %s?>%s' % (indent, self.target, self.data, newl))


class CharacterData(Childless, Node):
    __slots__ = ('_data', 'ownerDocument', 'parentNode', 'previousSibling', 'nextSibling')

    def __init__(self):
        self.ownerDocument = self.parentNode = None
        self.previousSibling = self.nextSibling = None
        self._data = ''
        Node.__init__(self)

    def _get_length(self):
        return len(self.data)

    __len__ = _get_length

    def _get_data(self):
        return self._data

    def _set_data(self, data):
        self._data = data

    data = nodeValue = property(_get_data, _set_data)

    def __repr__(self):
        data = self.data
        if len(data) > 10:
            dotdotdot = '...'
        else:
            dotdotdot = ''
        return '<DOM %s node "%r%s">' % (
         self.__class__.__name__, data[0:10], dotdotdot)

    def substringData(self, offset, count):
        if offset < 0:
            raise xml.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise xml.dom.IndexSizeErr('count cannot be negative')
        return self.data[offset:offset + count]

    def appendData(self, arg):
        self.data = self.data + arg

    def insertData(self, offset, arg):
        if offset < 0:
            raise xml.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr('offset cannot be beyond end of data')
        if arg:
            self.data = '%s%s%s' % (
             self.data[:offset], arg, self.data[offset:])

    def deleteData(self, offset, count):
        if offset < 0:
            raise xml.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise xml.dom.IndexSizeErr('count cannot be negative')
        if count:
            self.data = self.data[:offset] + self.data[offset + count:]

    def replaceData(self, offset, count, arg):
        if offset < 0:
            raise xml.dom.IndexSizeErr('offset cannot be negative')
        if offset >= len(self.data):
            raise xml.dom.IndexSizeErr('offset cannot be beyond end of data')
        if count < 0:
            raise xml.dom.IndexSizeErr('count cannot be negative')
        if count:
            self.data = '%s%s%s' % (
             self.data[:offset], arg, self.data[offset + count:])


defproperty(CharacterData, 'length', doc='Length of the string data.')

class Text(CharacterData):
    __slots__ = ()
    nodeType = Node.TEXT_NODE
    nodeName = '#text'
    attributes = None

    def splitText(self, offset):
        if offset < 0 or (offset > len(self.data)):
            raise xml.dom.IndexSizeErr('illegal offset value')
        newText = self.__class__()
        newText.data = self.data[offset:]
        newText.ownerDocument = self.ownerDocument
        next = self.nextSibling
        if self.parentNode:
            if self in self.parentNode.childNodes:
                if next is None:
                    self.parentNode.appendChild(newText)
                else:
                    self.parentNode.insertBefore(newText, next)
        self.data = self.data[:offset]
        return newText

    def writexml(self, writer, indent='', addindent='', newl=''):
        _write_data(writer, '%s%s%s' % (indent, self.data, newl))

    def _get_wholeText--- This code section failed: ---

 L.1094         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  BUILD_LIST_1          1 
                6  STORE_FAST               'L'

 L.1095         8  LOAD_FAST                'self'
               10  LOAD_ATTR                previousSibling
               12  STORE_FAST               'n'
             14_0  COME_FROM            64  '64'
             14_1  COME_FROM            60  '60'

 L.1096        14  LOAD_FAST                'n'
               16  LOAD_CONST               None
               18  COMPARE_OP               is-not
               20  POP_JUMP_IF_FALSE    66  'to 66'

 L.1097        22  LOAD_FAST                'n'
               24  LOAD_ATTR                nodeType
               26  LOAD_GLOBAL              Node
               28  LOAD_ATTR                TEXT_NODE
               30  LOAD_GLOBAL              Node
               32  LOAD_ATTR                CDATA_SECTION_NODE
               34  BUILD_TUPLE_2         2 
               36  COMPARE_OP               in
               38  POP_JUMP_IF_FALSE    66  'to 66'

 L.1098        40  LOAD_FAST                'L'
               42  LOAD_METHOD              insert
               44  LOAD_CONST               0
               46  LOAD_FAST                'n'
               48  LOAD_ATTR                data
               50  CALL_METHOD_2         2  ''
               52  POP_TOP          

 L.1099        54  LOAD_FAST                'n'
               56  LOAD_ATTR                previousSibling
               58  STORE_FAST               'n'
               60  JUMP_BACK            14  'to 14'

 L.1101        62  JUMP_FORWARD         66  'to 66'
               64  JUMP_BACK            14  'to 14'
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            38  '38'
             66_2  COME_FROM            20  '20'

 L.1102        66  LOAD_FAST                'self'
               68  LOAD_ATTR                nextSibling
               70  STORE_FAST               'n'
             72_0  COME_FROM           120  '120'
             72_1  COME_FROM           116  '116'

 L.1103        72  LOAD_FAST                'n'
               74  LOAD_CONST               None
               76  COMPARE_OP               is-not
               78  POP_JUMP_IF_FALSE   122  'to 122'

 L.1104        80  LOAD_FAST                'n'
               82  LOAD_ATTR                nodeType
               84  LOAD_GLOBAL              Node
               86  LOAD_ATTR                TEXT_NODE
               88  LOAD_GLOBAL              Node
               90  LOAD_ATTR                CDATA_SECTION_NODE
               92  BUILD_TUPLE_2         2 
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   122  'to 122'

 L.1105        98  LOAD_FAST                'L'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'n'
              104  LOAD_ATTR                data
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L.1106       110  LOAD_FAST                'n'
              112  LOAD_ATTR                nextSibling
              114  STORE_FAST               'n'
              116  JUMP_BACK            72  'to 72'

 L.1108       118  JUMP_FORWARD        122  'to 122'
              120  JUMP_BACK            72  'to 72'
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            96  '96'
            122_2  COME_FROM            78  '78'

 L.1109       122  LOAD_STR                 ''
              124  LOAD_METHOD              join
              126  LOAD_FAST                'L'
              128  CALL_METHOD_1         1  ''
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 62

    def replaceWholeText--- This code section failed: ---

 L.1114         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parentNode
                4  STORE_FAST               'parent'

 L.1115         6  LOAD_FAST                'self'
                8  LOAD_ATTR                previousSibling
               10  STORE_FAST               'n'
             12_0  COME_FROM            62  '62'
             12_1  COME_FROM            58  '58'

 L.1116        12  LOAD_FAST                'n'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    64  'to 64'

 L.1117        20  LOAD_FAST                'n'
               22  LOAD_ATTR                nodeType
               24  LOAD_GLOBAL              Node
               26  LOAD_ATTR                TEXT_NODE
               28  LOAD_GLOBAL              Node
               30  LOAD_ATTR                CDATA_SECTION_NODE
               32  BUILD_TUPLE_2         2 
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    64  'to 64'

 L.1118        38  LOAD_FAST                'n'
               40  LOAD_ATTR                previousSibling
               42  STORE_FAST               'next'

 L.1119        44  LOAD_FAST                'parent'
               46  LOAD_METHOD              removeChild
               48  LOAD_FAST                'n'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.1120        54  LOAD_FAST                'next'
               56  STORE_FAST               'n'
               58  JUMP_BACK            12  'to 12'

 L.1122        60  JUMP_FORWARD         64  'to 64'
               62  JUMP_BACK            12  'to 12'
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            36  '36'
             64_2  COME_FROM            18  '18'

 L.1123        64  LOAD_FAST                'self'
               66  LOAD_ATTR                nextSibling
               68  STORE_FAST               'n'

 L.1124        70  LOAD_FAST                'content'
               72  POP_JUMP_IF_TRUE     84  'to 84'

 L.1125        74  LOAD_FAST                'parent'
               76  LOAD_METHOD              removeChild
               78  LOAD_FAST                'self'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
             84_0  COME_FROM           134  '134'
             84_1  COME_FROM           130  '130'
             84_2  COME_FROM            72  '72'

 L.1126        84  LOAD_FAST                'n'
               86  LOAD_CONST               None
               88  COMPARE_OP               is-not
               90  POP_JUMP_IF_FALSE   136  'to 136'

 L.1127        92  LOAD_FAST                'n'
               94  LOAD_ATTR                nodeType
               96  LOAD_GLOBAL              Node
               98  LOAD_ATTR                TEXT_NODE
              100  LOAD_GLOBAL              Node
              102  LOAD_ATTR                CDATA_SECTION_NODE
              104  BUILD_TUPLE_2         2 
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   136  'to 136'

 L.1128       110  LOAD_FAST                'n'
              112  LOAD_ATTR                nextSibling
              114  STORE_FAST               'next'

 L.1129       116  LOAD_FAST                'parent'
              118  LOAD_METHOD              removeChild
              120  LOAD_FAST                'n'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.1130       126  LOAD_FAST                'next'
              128  STORE_FAST               'n'
              130  JUMP_BACK            84  'to 84'

 L.1132       132  JUMP_FORWARD        136  'to 136'
              134  JUMP_BACK            84  'to 84'
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           108  '108'
            136_2  COME_FROM            90  '90'

 L.1133       136  LOAD_FAST                'content'
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L.1134       140  LOAD_FAST                'content'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               data

 L.1135       146  LOAD_FAST                'self'
              148  RETURN_VALUE     
            150_0  COME_FROM           138  '138'

 L.1137       150  LOAD_CONST               None
              152  RETURN_VALUE     

Parse error at or near `JUMP_FORWARD' instruction at offset 60

    def _get_isWhitespaceInElementContent(self):
        if self.data.strip():
            return False
        elem = _get_containing_element(self)
        if elem is None:
            return False
        info = self.ownerDocument._get_elem_info(elem)
        if info is None:
            return False
        return info.isElementContent()


defproperty(Text, 'isWhitespaceInElementContent', doc='True iff this text node contains only whitespace and is in element content.')
defproperty(Text, 'wholeText', doc='The text of all logically-adjacent text nodes.')

def _get_containing_element(node):
    c = node.parentNode
    while True:
        if c is not None:
            if c.nodeType == Node.ELEMENT_NODE:
                return c
            c = c.parentNode


def _get_containing_entref(node):
    c = node.parentNode
    while True:
        if c is not None:
            if c.nodeType == Node.ENTITY_REFERENCE_NODE:
                return c
            c = c.parentNode


class Comment(CharacterData):
    nodeType = Node.COMMENT_NODE
    nodeName = '#comment'

    def __init__(self, data):
        CharacterData.__init__(self)
        self._data = data

    def writexml(self, writer, indent='', addindent='', newl=''):
        if '--' in self.data:
            raise ValueError("'--' is not allowed in a comment node")
        writer.write('%s<!--%s-->%s' % (indent, self.data, newl))


class CDATASection(Text):
    __slots__ = ()
    nodeType = Node.CDATA_SECTION_NODE
    nodeName = '#cdata-section'

    def writexml(self, writer, indent='', addindent='', newl=''):
        if self.data.find(']]>') >= 0:
            raise ValueError("']]>' not allowed in a CDATA section")
        writer.write('<![CDATA[%s]]>' % self.data)


class ReadOnlySequentialNamedNodeMap(object):
    __slots__ = ('_seq', )

    def __init__(self, seq=()):
        self._seq = seq

    def __len__(self):
        return len(self._seq)

    def _get_length(self):
        return len(self._seq)

    def getNamedItem(self, name):
        for n in self._seq:
            if n.nodeName == name:
                return n

    def getNamedItemNS(self, namespaceURI, localName):
        for n in self._seq:
            if n.namespaceURI == namespaceURI:
                if n.localName == localName:
                    return n

    def __getitem__(self, name_or_tuple):
        if isinstance(name_or_tuple, tuple):
            node = (self.getNamedItemNS)(*name_or_tuple)
        else:
            node = self.getNamedItem(name_or_tuple)
        if node is None:
            raise KeyError(name_or_tuple)
        return node

    def item--- This code section failed: ---

 L.1234         0  LOAD_FAST                'index'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.1235         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.1236        12  SETUP_FINALLY        26  'to 26'

 L.1237        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _seq
               18  LOAD_FAST                'index'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L.1238        26  DUP_TOP          
               28  LOAD_GLOBAL              IndexError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.1239        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 42

    def removeNamedItem(self, name):
        raise xml.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def removeNamedItemNS(self, namespaceURI, localName):
        raise xml.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def setNamedItem(self, node):
        raise xml.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def setNamedItemNS(self, node):
        raise xml.dom.NoModificationAllowedErr('NamedNodeMap instance is read-only')

    def __getstate__(self):
        return [
         self._seq]

    def __setstate__(self, state):
        self._seq = state[0]


defproperty(ReadOnlySequentialNamedNodeMap, 'length', doc='Number of entries in the NamedNodeMap.')

class Identified:
    __doc__ = 'Mix-in class that supports the publicId and systemId attributes.'
    __slots__ = ('publicId', 'systemId')

    def _identified_mixin_init(self, publicId, systemId):
        self.publicId = publicId
        self.systemId = systemId

    def _get_publicId(self):
        return self.publicId

    def _get_systemId(self):
        return self.systemId


class DocumentType(Identified, Childless, Node):
    nodeType = Node.DOCUMENT_TYPE_NODE
    nodeValue = None
    name = None
    publicId = None
    systemId = None
    internalSubset = None

    def __init__(self, qualifiedName):
        self.entities = ReadOnlySequentialNamedNodeMap()
        self.notations = ReadOnlySequentialNamedNodeMap()
        if qualifiedName:
            prefix, localname = _nssplit(qualifiedName)
            self.name = localname
        self.nodeName = self.name

    def _get_internalSubset(self):
        return self.internalSubset

    def cloneNode(self, deep):
        if self.ownerDocument is None:
            clone = DocumentType(None)
            clone.name = self.name
            clone.nodeName = self.name
            operation = xml.dom.UserDataHandler.NODE_CLONED
            if deep:
                clone.entities._seq = []
                clone.notations._seq = []
                for n in self.notations._seq:
                    notation = Notation(n.nodeName, n.publicId, n.systemId)
                    clone.notations._seq.append(notation)
                    n._call_user_data_handler(operation, n, notation)
                else:
                    for e in self.entities._seq:
                        entity = Entity(e.nodeName, e.publicId, e.systemId, e.notationName)
                        entity.actualEncoding = e.actualEncoding
                        entity.encoding = e.encoding
                        entity.version = e.version
                        clone.entities._seq.append(entity)
                        e._call_user_data_handler(operation, e, entity)
                    else:
                        self._call_user_data_handler(operation, self, clone)

                return clone
        return

    def writexml(self, writer, indent='', addindent='', newl=''):
        writer.write('<!DOCTYPE ')
        writer.write(self.name)
        if self.publicId:
            writer.write("%s  PUBLIC '%s'%s  '%s'" % (
             newl, self.publicId, newl, self.systemId))
        elif self.systemId:
            writer.write("%s  SYSTEM '%s'" % (newl, self.systemId))
        if self.internalSubset is not None:
            writer.write(' [')
            writer.write(self.internalSubset)
            writer.write(']')
        writer.write('>' + newl)


class Entity(Identified, Node):
    attributes = None
    nodeType = Node.ENTITY_NODE
    nodeValue = None
    actualEncoding = None
    encoding = None
    version = None

    def __init__(self, name, publicId, systemId, notation):
        self.nodeName = name
        self.notationName = notation
        self.childNodes = NodeList()
        self._identified_mixin_init(publicId, systemId)

    def _get_actualEncoding(self):
        return self.actualEncoding

    def _get_encoding(self):
        return self.encoding

    def _get_version(self):
        return self.version

    def appendChild(self, newChild):
        raise xml.dom.HierarchyRequestErr('cannot append children to an entity node')

    def insertBefore(self, newChild, refChild):
        raise xml.dom.HierarchyRequestErr('cannot insert children below an entity node')

    def removeChild(self, oldChild):
        raise xml.dom.HierarchyRequestErr('cannot remove children from an entity node')

    def replaceChild(self, newChild, oldChild):
        raise xml.dom.HierarchyRequestErr('cannot replace children of an entity node')


class Notation(Identified, Childless, Node):
    nodeType = Node.NOTATION_NODE
    nodeValue = None

    def __init__(self, name, publicId, systemId):
        self.nodeName = name
        self._identified_mixin_init(publicId, systemId)


class DOMImplementation(DOMImplementationLS):
    _features = [
     ('core', '1.0'),
     ('core', '2.0'),
     ('core', None),
     ('xml', '1.0'),
     ('xml', '2.0'),
     ('xml', None),
     ('ls-load', '3.0'),
     ('ls-load', None)]

    def hasFeature(self, feature, version):
        if version == '':
            version = None
        return (feature.lower(), version) in self._features

    def createDocument(self, namespaceURI, qualifiedName, doctype):
        if doctype:
            if doctype.parentNode is not None:
                raise xml.dom.WrongDocumentErr('doctype object owned by another DOM tree')
        doc = self._create_document()
        add_root_element = namespaceURI is None and not (qualifiedName is None and doctype is None)
        if not qualifiedName:
            if add_root_element:
                raise xml.dom.InvalidCharacterErr('Element with no name')
        if add_root_element:
            prefix, localname = _nssplit(qualifiedName)
            if prefix == 'xml':
                if namespaceURI != 'http://www.w3.org/XML/1998/namespace':
                    raise xml.dom.NamespaceErr("illegal use of 'xml' prefix")
            if prefix:
                if not namespaceURI:
                    raise xml.dom.NamespaceErr('illegal use of prefix without namespaces')
                element = doc.createElementNS(namespaceURI, qualifiedName)
                if doctype:
                    doc.appendChild(doctype)
            doc.appendChild(element)
        if doctype:
            doctype.parentNode = doctype.ownerDocument = doc
        doc.doctype = doctype
        doc.implementation = self
        return doc

    def createDocumentType(self, qualifiedName, publicId, systemId):
        doctype = DocumentType(qualifiedName)
        doctype.publicId = publicId
        doctype.systemId = systemId
        return doctype

    def getInterface(self, feature):
        if self.hasFeature(feature, None):
            return self
        return

    def _create_document(self):
        return Document()


class ElementInfo(object):
    __doc__ = 'Object that represents content-model information for an element.\n\n    This implementation is not expected to be used in practice; DOM\n    builders should provide implementations which do the right thing\n    using information available to it.\n\n    '
    __slots__ = ('tagName', )

    def __init__(self, name):
        self.tagName = name

    def getAttributeType(self, aname):
        return _no_type

    def getAttributeTypeNS(self, namespaceURI, localName):
        return _no_type

    def isElementContent(self):
        return False

    def isEmpty(self):
        """Returns true iff this element is declared to have an EMPTY
        content model."""
        return False

    def isId(self, aname):
        """Returns true iff the named attribute is a DTD-style ID."""
        return False

    def isIdNS(self, namespaceURI, localName):
        """Returns true iff the identified attribute is a DTD-style ID."""
        return False

    def __getstate__(self):
        return self.tagName

    def __setstate__(self, state):
        self.tagName = state


def _clear_id_cache(node):
    if node.nodeType == Node.DOCUMENT_NODE:
        node._id_cache.clear()
        node._id_search_stack = None
    elif _in_document(node):
        node.ownerDocument._id_cache.clear()
        node.ownerDocument._id_search_stack = None


class Document(Node, DocumentLS):
    __slots__ = ('_elem_info', 'doctype', '_id_search_stack', 'childNodes', '_id_cache')
    _child_node_types = (
     Node.ELEMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE,
     Node.COMMENT_NODE, Node.DOCUMENT_TYPE_NODE)
    implementation = DOMImplementation()
    nodeType = Node.DOCUMENT_NODE
    nodeName = '#document'
    nodeValue = None
    attributes = None
    parentNode = None
    previousSibling = nextSibling = None
    actualEncoding = None
    encoding = None
    standalone = None
    version = None
    strictErrorChecking = False
    errorHandler = None
    documentURI = None
    _magic_id_count = 0

    def __init__(self):
        self.doctype = None
        self.childNodes = NodeList()
        self._elem_info = {}
        self._id_cache = {}
        self._id_search_stack = None

    def _get_elem_info(self, element):
        if element.namespaceURI:
            key = (
             element.namespaceURI, element.localName)
        else:
            key = element.tagName
        return self._elem_info.get(key)

    def _get_actualEncoding(self):
        return self.actualEncoding

    def _get_doctype(self):
        return self.doctype

    def _get_documentURI(self):
        return self.documentURI

    def _get_encoding(self):
        return self.encoding

    def _get_errorHandler(self):
        return self.errorHandler

    def _get_standalone(self):
        return self.standalone

    def _get_strictErrorChecking(self):
        return self.strictErrorChecking

    def _get_version(self):
        return self.version

    def appendChild(self, node):
        if node.nodeType not in self._child_node_types:
            raise xml.dom.HierarchyRequestErr('%s cannot be child of %s' % (repr(node), repr(self)))
        if node.parentNode is not None:
            node.parentNode.removeChild(node)
        if node.nodeType == Node.ELEMENT_NODE:
            if self._get_documentElement():
                raise xml.dom.HierarchyRequestErr('two document elements disallowed')
        return Node.appendChild(self, node)

    def removeChild(self, oldChild):
        try:
            self.childNodes.remove(oldChild)
        except ValueError:
            raise xml.dom.NotFoundErr()
        else:
            oldChild.nextSibling = oldChild.previousSibling = None
            oldChild.parentNode = None
            if self.documentElement is oldChild:
                self.documentElement = None
            else:
                return oldChild

    def _get_documentElement(self):
        for node in self.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                return node

    def unlink(self):
        if self.doctype is not None:
            self.doctype.unlink()
            self.doctype = None
        Node.unlink(self)

    def cloneNode(self, deep):
        if not deep:
            return
        clone = self.implementation.createDocument(None, None, None)
        clone.encoding = self.encoding
        clone.standalone = self.standalone
        clone.version = self.version
        for n in self.childNodes:
            childclone = _clone_node(n, deep, clone)
            if not childclone.ownerDocument.isSameNode(clone):
                raise AssertionError
            else:
                clone.childNodes.append(childclone)
                if childclone.nodeType == Node.DOCUMENT_NODE:
                    assert clone.documentElement is None
                elif childclone.nodeType == Node.DOCUMENT_TYPE_NODE:
                    assert clone.doctype is None
                    clone.doctype = childclone
                childclone.parentNode = clone
        else:
            self._call_user_data_handler(xml.dom.UserDataHandler.NODE_CLONED, self, clone)
            return clone

    def createDocumentFragment(self):
        d = DocumentFragment()
        d.ownerDocument = self
        return d

    def createElement(self, tagName):
        e = Element(tagName)
        e.ownerDocument = self
        return e

    def createTextNode(self, data):
        if not isinstance(data, str):
            raise TypeError('node contents must be a string')
        t = Text()
        t.data = data
        t.ownerDocument = self
        return t

    def createCDATASection(self, data):
        if not isinstance(data, str):
            raise TypeError('node contents must be a string')
        c = CDATASection()
        c.data = data
        c.ownerDocument = self
        return c

    def createComment(self, data):
        c = Comment(data)
        c.ownerDocument = self
        return c

    def createProcessingInstruction(self, target, data):
        p = ProcessingInstruction(target, data)
        p.ownerDocument = self
        return p

    def createAttribute(self, qName):
        a = Attr(qName)
        a.ownerDocument = self
        a.value = ''
        return a

    def createElementNS(self, namespaceURI, qualifiedName):
        prefix, localName = _nssplit(qualifiedName)
        e = Element(qualifiedName, namespaceURI, prefix)
        e.ownerDocument = self
        return e

    def createAttributeNS(self, namespaceURI, qualifiedName):
        prefix, localName = _nssplit(qualifiedName)
        a = Attr(qualifiedName, namespaceURI, localName, prefix)
        a.ownerDocument = self
        a.value = ''
        return a

    def _create_entity(self, name, publicId, systemId, notationName):
        e = Entity(name, publicId, systemId, notationName)
        e.ownerDocument = self
        return e

    def _create_notation(self, name, publicId, systemId):
        n = Notation(name, publicId, systemId)
        n.ownerDocument = self
        return n

    def getElementById--- This code section failed: ---

 L.1716         0  LOAD_FAST                'id'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _id_cache
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.1717        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _id_cache
               14  LOAD_FAST                'id'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L.1718        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _elem_info
               24  POP_JUMP_IF_TRUE     36  'to 36'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _magic_id_count
               30  POP_JUMP_IF_TRUE     36  'to 36'

 L.1719        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'
             36_1  COME_FROM            24  '24'

 L.1721        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _id_search_stack
               40  STORE_FAST               'stack'

 L.1722        42  LOAD_FAST                'stack'
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L.1724        50  LOAD_FAST                'self'
               52  LOAD_ATTR                documentElement
               54  BUILD_LIST_1          1 
               56  STORE_FAST               'stack'

 L.1725        58  LOAD_FAST                'stack'
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _id_search_stack
               64  JUMP_FORWARD         74  'to 74'
             66_0  COME_FROM            48  '48'

 L.1726        66  LOAD_FAST                'stack'
               68  POP_JUMP_IF_TRUE     74  'to 74'

 L.1729        70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'
             74_1  COME_FROM            64  '64'

 L.1731        74  LOAD_CONST               None
               76  STORE_FAST               'result'
             78_0  COME_FROM           396  '396'
             78_1  COME_FROM           390  '390'

 L.1732        78  LOAD_FAST                'stack'
            80_82  POP_JUMP_IF_FALSE   398  'to 398'

 L.1733        84  LOAD_FAST                'stack'
               86  LOAD_METHOD              pop
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               'node'

 L.1735        92  LOAD_FAST                'stack'
               94  LOAD_METHOD              extend
               96  LOAD_LISTCOMP            '<code_object <listcomp>>'
               98  LOAD_STR                 'Document.getElementById.<locals>.<listcomp>'
              100  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              102  LOAD_FAST                'node'
              104  LOAD_ATTR                childNodes
              106  GET_ITER         
              108  CALL_FUNCTION_1       1  ''
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L.1738       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _get_elem_info
              118  LOAD_FAST                'node'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'info'

 L.1739       124  LOAD_FAST                'info'
          126_128  POP_JUMP_IF_FALSE   322  'to 322'

 L.1743       130  LOAD_FAST                'node'
              132  LOAD_ATTR                attributes
              134  LOAD_METHOD              values
              136  CALL_METHOD_0         0  ''
              138  GET_ITER         
            140_0  COME_FROM           318  '318'
            140_1  COME_FROM           310  '310'
            140_2  COME_FROM           300  '300'
            140_3  COME_FROM           270  '270'
            140_4  COME_FROM           264  '264'
            140_5  COME_FROM           206  '206'
              140  FOR_ITER            320  'to 320'
              142  STORE_FAST               'attr'

 L.1744       144  LOAD_FAST                'attr'
              146  LOAD_ATTR                namespaceURI
              148  POP_JUMP_IF_FALSE   208  'to 208'

 L.1745       150  LOAD_FAST                'info'
              152  LOAD_METHOD              isIdNS
              154  LOAD_FAST                'attr'
              156  LOAD_ATTR                namespaceURI
              158  LOAD_FAST                'attr'
              160  LOAD_ATTR                localName
              162  CALL_METHOD_2         2  ''
              164  POP_JUMP_IF_FALSE   206  'to 206'

 L.1746       166  LOAD_FAST                'node'
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _id_cache
              172  LOAD_FAST                'attr'
              174  LOAD_ATTR                value
              176  STORE_SUBSCR     

 L.1747       178  LOAD_FAST                'attr'
              180  LOAD_ATTR                value
              182  LOAD_FAST                'id'
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   194  'to 194'

 L.1748       188  LOAD_FAST                'node'
              190  STORE_FAST               'result'
              192  JUMP_FORWARD        206  'to 206'
            194_0  COME_FROM           186  '186'

 L.1749       194  LOAD_FAST                'node'
              196  LOAD_ATTR                _magic_id_nodes
              198  POP_JUMP_IF_TRUE    206  'to 206'

 L.1750       200  POP_TOP          
          202_204  BREAK_LOOP          384  'to 384'
            206_0  COME_FROM           198  '198'
            206_1  COME_FROM           192  '192'
            206_2  COME_FROM           164  '164'
              206  JUMP_BACK           140  'to 140'
            208_0  COME_FROM           148  '148'

 L.1751       208  LOAD_FAST                'info'
              210  LOAD_METHOD              isId
              212  LOAD_FAST                'attr'
              214  LOAD_ATTR                name
              216  CALL_METHOD_1         1  ''
          218_220  POP_JUMP_IF_FALSE   266  'to 266'

 L.1752       222  LOAD_FAST                'node'
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                _id_cache
              228  LOAD_FAST                'attr'
              230  LOAD_ATTR                value
              232  STORE_SUBSCR     

 L.1753       234  LOAD_FAST                'attr'
              236  LOAD_ATTR                value
              238  LOAD_FAST                'id'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   250  'to 250'

 L.1754       244  LOAD_FAST                'node'
              246  STORE_FAST               'result'
              248  JUMP_FORWARD        264  'to 264'
            250_0  COME_FROM           242  '242'

 L.1755       250  LOAD_FAST                'node'
              252  LOAD_ATTR                _magic_id_nodes
          254_256  POP_JUMP_IF_TRUE    318  'to 318'

 L.1756       258  POP_TOP          
          260_262  BREAK_LOOP          384  'to 384'
            264_0  COME_FROM           248  '248'
              264  JUMP_BACK           140  'to 140'
            266_0  COME_FROM           218  '218'

 L.1757       266  LOAD_FAST                'attr'
              268  LOAD_ATTR                _is_id
              270  POP_JUMP_IF_FALSE_BACK   140  'to 140'

 L.1758       272  LOAD_FAST                'node'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                _id_cache
              278  LOAD_FAST                'attr'
              280  LOAD_ATTR                value
              282  STORE_SUBSCR     

 L.1759       284  LOAD_FAST                'attr'
              286  LOAD_ATTR                value
              288  LOAD_FAST                'id'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   302  'to 302'

 L.1760       296  LOAD_FAST                'node'
              298  STORE_FAST               'result'
              300  JUMP_BACK           140  'to 140'
            302_0  COME_FROM           292  '292'

 L.1761       302  LOAD_FAST                'node'
              304  LOAD_ATTR                _magic_id_nodes
              306  LOAD_CONST               1
              308  COMPARE_OP               ==
              310  POP_JUMP_IF_FALSE_BACK   140  'to 140'

 L.1762       312  POP_TOP          
          314_316  BREAK_LOOP          384  'to 384'
            318_0  COME_FROM           254  '254'
              318  JUMP_BACK           140  'to 140'
            320_0  COME_FROM           140  '140'
              320  JUMP_FORWARD        384  'to 384'
            322_0  COME_FROM           126  '126'

 L.1763       322  LOAD_FAST                'node'
              324  LOAD_ATTR                _magic_id_nodes
          326_328  POP_JUMP_IF_FALSE   384  'to 384'

 L.1764       330  LOAD_FAST                'node'
              332  LOAD_ATTR                attributes
              334  LOAD_METHOD              values
              336  CALL_METHOD_0         0  ''
              338  GET_ITER         
            340_0  COME_FROM           380  '380'
            340_1  COME_FROM           372  '372'
            340_2  COME_FROM           348  '348'
              340  FOR_ITER            384  'to 384'
              342  STORE_FAST               'attr'

 L.1765       344  LOAD_FAST                'attr'
              346  LOAD_ATTR                _is_id
          348_350  POP_JUMP_IF_FALSE_BACK   340  'to 340'

 L.1766       352  LOAD_FAST                'node'
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                _id_cache
              358  LOAD_FAST                'attr'
              360  LOAD_ATTR                value
              362  STORE_SUBSCR     

 L.1767       364  LOAD_FAST                'attr'
              366  LOAD_ATTR                value
              368  LOAD_FAST                'id'
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE_BACK   340  'to 340'

 L.1768       376  LOAD_FAST                'node'
              378  STORE_FAST               'result'
          380_382  JUMP_BACK           340  'to 340'
            384_0  COME_FROM           340  '340'
            384_1  COME_FROM           326  '326'
            384_2  COME_FROM           320  '320'
            384_3  COME_FROM           314  '314'
            384_4  COME_FROM           260  '260'
            384_5  COME_FROM           202  '202'

 L.1769       384  LOAD_FAST                'result'
              386  LOAD_CONST               None
              388  COMPARE_OP               is-not
              390  POP_JUMP_IF_FALSE_BACK    78  'to 78'

 L.1770   392_394  JUMP_FORWARD        398  'to 398'
              396  JUMP_BACK            78  'to 78'
            398_0  COME_FROM           392  '392'
            398_1  COME_FROM            80  '80'

 L.1771       398  LOAD_FAST                'result'
              400  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 396

    def getElementsByTagName(self, name):
        return _get_elements_by_tagName_helper(self, name, NodeList())

    def getElementsByTagNameNS(self, namespaceURI, localName):
        return _get_elements_by_tagName_ns_helper(self, namespaceURI, localName, NodeList())

    def isSupported(self, feature, version):
        return self.implementation.hasFeature(feature, version)

    def importNode(self, node, deep):
        if node.nodeType == Node.DOCUMENT_NODE:
            raise xml.dom.NotSupportedErr('cannot import document nodes')
        elif node.nodeType == Node.DOCUMENT_TYPE_NODE:
            raise xml.dom.NotSupportedErr('cannot import document type nodes')
        return _clone_node(node, deep, self)

    def writexml(self, writer, indent='', addindent='', newl='', encoding=None):
        if encoding is None:
            writer.write('<?xml version="1.0" ?>' + newl)
        else:
            writer.write('<?xml version="1.0" encoding="%s"?>%s' % (
             encoding, newl))
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)

    def renameNode--- This code section failed: ---

 L.1802         0  LOAD_FAST                'n'
                2  LOAD_ATTR                ownerDocument
                4  LOAD_FAST                'self'
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L.1803        10  LOAD_GLOBAL              xml
               12  LOAD_ATTR                dom
               14  LOAD_METHOD              WrongDocumentErr

 L.1804        16  LOAD_STR                 'cannot rename nodes from other documents;\nexpected %s,\nfound %s'

 L.1805        18  LOAD_FAST                'self'
               20  LOAD_FAST                'n'
               22  LOAD_ATTR                ownerDocument
               24  BUILD_TUPLE_2         2 

 L.1804        26  BINARY_MODULO    

 L.1803        28  CALL_METHOD_1         1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM             8  '8'

 L.1806        32  LOAD_FAST                'n'
               34  LOAD_ATTR                nodeType
               36  LOAD_GLOBAL              Node
               38  LOAD_ATTR                ELEMENT_NODE
               40  LOAD_GLOBAL              Node
               42  LOAD_ATTR                ATTRIBUTE_NODE
               44  BUILD_TUPLE_2         2 
               46  COMPARE_OP               not-in
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L.1807        50  LOAD_GLOBAL              xml
               52  LOAD_ATTR                dom
               54  LOAD_METHOD              NotSupportedErr

 L.1808        56  LOAD_STR                 'renameNode() only applies to element and attribute nodes'

 L.1807        58  CALL_METHOD_1         1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            48  '48'

 L.1809        62  LOAD_FAST                'namespaceURI'
               64  LOAD_GLOBAL              EMPTY_NAMESPACE
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE   182  'to 182'

 L.1810        70  LOAD_STR                 ':'
               72  LOAD_FAST                'name'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE   128  'to 128'

 L.1811        78  LOAD_FAST                'name'
               80  LOAD_METHOD              split
               82  LOAD_STR                 ':'
               84  LOAD_CONST               1
               86  CALL_METHOD_2         2  ''
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'prefix'
               92  STORE_FAST               'localName'

 L.1812        94  LOAD_FAST                'prefix'
               96  LOAD_STR                 'xmlns'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   180  'to 180'

 L.1813       102  LOAD_FAST                'namespaceURI'
              104  LOAD_GLOBAL              xml
              106  LOAD_ATTR                dom
              108  LOAD_ATTR                XMLNS_NAMESPACE
              110  COMPARE_OP               !=

 L.1812       112  POP_JUMP_IF_FALSE   180  'to 180'

 L.1814       114  LOAD_GLOBAL              xml
              116  LOAD_ATTR                dom
              118  LOAD_METHOD              NamespaceErr

 L.1815       120  LOAD_STR                 "illegal use of 'xmlns' prefix"

 L.1814       122  CALL_METHOD_1         1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
              126  JUMP_FORWARD        190  'to 190'
            128_0  COME_FROM            76  '76'

 L.1817       128  LOAD_FAST                'name'
              130  LOAD_STR                 'xmlns'
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   172  'to 172'

 L.1818       136  LOAD_FAST                'namespaceURI'
              138  LOAD_GLOBAL              xml
              140  LOAD_ATTR                dom
              142  LOAD_ATTR                XMLNS_NAMESPACE
              144  COMPARE_OP               !=

 L.1817       146  POP_JUMP_IF_FALSE   172  'to 172'

 L.1819       148  LOAD_FAST                'n'
              150  LOAD_ATTR                nodeType
              152  LOAD_GLOBAL              Node
              154  LOAD_ATTR                ATTRIBUTE_NODE
              156  COMPARE_OP               ==

 L.1817       158  POP_JUMP_IF_FALSE   172  'to 172'

 L.1820       160  LOAD_GLOBAL              xml
              162  LOAD_ATTR                dom
              164  LOAD_METHOD              NamespaceErr

 L.1821       166  LOAD_STR                 "illegal use of the 'xmlns' attribute"

 L.1820       168  CALL_METHOD_1         1  ''
              170  RAISE_VARARGS_1       1  'exception instance'
            172_0  COME_FROM           158  '158'
            172_1  COME_FROM           146  '146'
            172_2  COME_FROM           134  '134'

 L.1822       172  LOAD_CONST               None
              174  STORE_FAST               'prefix'

 L.1823       176  LOAD_FAST                'name'
              178  STORE_FAST               'localName'
            180_0  COME_FROM           112  '112'
            180_1  COME_FROM           100  '100'
              180  JUMP_FORWARD        190  'to 190'
            182_0  COME_FROM            68  '68'

 L.1825       182  LOAD_CONST               None
              184  STORE_FAST               'prefix'

 L.1826       186  LOAD_CONST               None
              188  STORE_FAST               'localName'
            190_0  COME_FROM           180  '180'
            190_1  COME_FROM           126  '126'

 L.1827       190  LOAD_FAST                'n'
              192  LOAD_ATTR                nodeType
              194  LOAD_GLOBAL              Node
              196  LOAD_ATTR                ATTRIBUTE_NODE
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   234  'to 234'

 L.1828       202  LOAD_FAST                'n'
              204  LOAD_ATTR                ownerElement
              206  STORE_FAST               'element'

 L.1829       208  LOAD_FAST                'element'
              210  LOAD_CONST               None
              212  COMPARE_OP               is-not
              214  POP_JUMP_IF_FALSE   238  'to 238'

 L.1830       216  LOAD_FAST                'n'
              218  LOAD_ATTR                _is_id
              220  STORE_FAST               'is_id'

 L.1831       222  LOAD_FAST                'element'
              224  LOAD_METHOD              removeAttributeNode
              226  LOAD_FAST                'n'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  JUMP_FORWARD        238  'to 238'
            234_0  COME_FROM           200  '200'

 L.1833       234  LOAD_CONST               None
              236  STORE_FAST               'element'
            238_0  COME_FROM           232  '232'
            238_1  COME_FROM           214  '214'

 L.1834       238  LOAD_FAST                'prefix'
              240  LOAD_FAST                'n'
              242  STORE_ATTR               prefix

 L.1835       244  LOAD_FAST                'localName'
              246  LOAD_FAST                'n'
              248  STORE_ATTR               _localName

 L.1836       250  LOAD_FAST                'namespaceURI'
              252  LOAD_FAST                'n'
              254  STORE_ATTR               namespaceURI

 L.1837       256  LOAD_FAST                'name'
              258  LOAD_FAST                'n'
              260  STORE_ATTR               nodeName

 L.1838       262  LOAD_FAST                'n'
              264  LOAD_ATTR                nodeType
              266  LOAD_GLOBAL              Node
              268  LOAD_ATTR                ELEMENT_NODE
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   284  'to 284'

 L.1839       276  LOAD_FAST                'name'
              278  LOAD_FAST                'n'
              280  STORE_ATTR               tagName
              282  JUMP_FORWARD        326  'to 326'
            284_0  COME_FROM           272  '272'

 L.1842       284  LOAD_FAST                'name'
              286  LOAD_FAST                'n'
              288  STORE_ATTR               name

 L.1843       290  LOAD_FAST                'element'
              292  LOAD_CONST               None
              294  COMPARE_OP               is-not
          296_298  POP_JUMP_IF_FALSE   326  'to 326'

 L.1844       300  LOAD_FAST                'element'
              302  LOAD_METHOD              setAttributeNode
              304  LOAD_FAST                'n'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          

 L.1845       310  LOAD_FAST                'is_id'
          312_314  POP_JUMP_IF_FALSE   326  'to 326'

 L.1846       316  LOAD_FAST                'element'
              318  LOAD_METHOD              setIdAttributeNode
              320  LOAD_FAST                'n'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
            326_0  COME_FROM           312  '312'
            326_1  COME_FROM           296  '296'
            326_2  COME_FROM           282  '282'

 L.1852       326  LOAD_FAST                'n'
              328  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 328


defproperty(Document, 'documentElement', doc='Top-level element of this document.')

def _clone_node(node, deep, newOwnerDocument):
    """
    Clone a node and give it the new owner document.
    Called by Node.cloneNode and Document.importNode
    """
    if node.ownerDocument.isSameNode(newOwnerDocument):
        operation = xml.dom.UserDataHandler.NODE_CLONED
    else:
        operation = xml.dom.UserDataHandler.NODE_IMPORTED
    if node.nodeType == Node.ELEMENT_NODE:
        clone = newOwnerDocument.createElementNS(node.namespaceURI, node.nodeName)
        for attr in node.attributes.values():
            clone.setAttributeNS(attr.namespaceURI, attr.nodeName, attr.value)
            a = clone.getAttributeNodeNS(attr.namespaceURI, attr.localName)
            a.specified = attr.specified
        else:
            if deep:
                for child in node.childNodes:
                    c = _clone_node(child, deep, newOwnerDocument)
                    clone.appendChild(c)

    elif node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
        clone = newOwnerDocument.createDocumentFragment()
        if deep:
            for child in node.childNodes:
                c = _clone_node(child, deep, newOwnerDocument)
                clone.appendChild(c)

    elif node.nodeType == Node.TEXT_NODE:
        clone = newOwnerDocument.createTextNode(node.data)
    elif node.nodeType == Node.CDATA_SECTION_NODE:
        clone = newOwnerDocument.createCDATASection(node.data)
    elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
        clone = newOwnerDocument.createProcessingInstruction(node.target, node.data)
    elif node.nodeType == Node.COMMENT_NODE:
        clone = newOwnerDocument.createComment(node.data)
    elif node.nodeType == Node.ATTRIBUTE_NODE:
        clone = newOwnerDocument.createAttributeNS(node.namespaceURI, node.nodeName)
        clone.specified = True
        clone.value = node.value
    elif node.nodeType == Node.DOCUMENT_TYPE_NODE:
        assert node.ownerDocument is not newOwnerDocument
        operation = xml.dom.UserDataHandler.NODE_IMPORTED
        clone = newOwnerDocument.implementation.createDocumentType(node.name, node.publicId, node.systemId)
        clone.ownerDocument = newOwnerDocument
        if deep:
            clone.entities._seq = []
            clone.notations._seq = []
            for n in node.notations._seq:
                notation = Notation(n.nodeName, n.publicId, n.systemId)
                notation.ownerDocument = newOwnerDocument
                clone.notations._seq.append(notation)
                if hasattr(n, '_call_user_data_handler'):
                    n._call_user_data_handler(operation, n, notation)
            else:
                for e in node.entities._seq:
                    entity = Entity(e.nodeName, e.publicId, e.systemId, e.notationName)
                    entity.actualEncoding = e.actualEncoding
                    entity.encoding = e.encoding
                    entity.version = e.version
                    entity.ownerDocument = newOwnerDocument
                    clone.entities._seq.append(entity)
                    if hasattr(e, '_call_user_data_handler'):
                        e._call_user_data_handler(operation, e, entity)

    else:
        raise xml.dom.NotSupportedErr('Cannot clone node %s' % repr(node))
    if hasattr(node, '_call_user_data_handler'):
        node._call_user_data_handler(operation, node, clone)
    return clone


def _nssplit(qualifiedName):
    fields = qualifiedName.split(':', 1)
    if len(fields) == 2:
        return fields
    return (
     None, fields[0])


def _do_pulldom_parse(func, args, kwargs):
    events = func(*args, **kwargs)
    toktype, rootNode = events.getEvent()
    events.expandNode(rootNode)
    events.clear()
    return rootNode


def parse(file, parser=None, bufsize=None):
    """Parse a file into a DOM by filename or file object."""
    if parser is None:
        if not bufsize:
            from xml.dom import expatbuilder
            return expatbuilder.parse(file)
        from xml.dom import pulldom
        return _do_pulldom_parse(pulldom.parse, (file,), {'parser':parser, 
         'bufsize':bufsize})


def parseString(string, parser=None):
    """Parse a file into a DOM from a string."""
    if parser is None:
        from xml.dom import expatbuilder
        return expatbuilder.parseString(string)
    from xml.dom import pulldom
    return _do_pulldom_parse(pulldom.parseString, (string,), {'parser': parser})


def getDOMImplementation(features=None):
    if features:
        if isinstance(features, str):
            features = domreg._parse_feature_string(features)
        for f, v in features:
            if not Document.implementation.hasFeature(f, v):
                return None

        return Document.implementation