# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\treebuilders\base.py
from __future__ import absolute_import, division, unicode_literals
from six import text_type
from ..constants import scopingElements, tableInsertModeElements, namespaces
Marker = None
listElementsMap = {None:(
  frozenset(scopingElements), False), 
 'button':(
  frozenset(scopingElements | set([(namespaces['html'], 'button')])), False), 
 'list':(
  frozenset(scopingElements | set([(namespaces['html'], 'ol'),
   (
    namespaces['html'], 'ul')])), False), 
 'table':(
  frozenset([(namespaces['html'], 'html'),
   (
    namespaces['html'], 'table')]), False), 
 'select':(
  frozenset([(namespaces['html'], 'optgroup'),
   (
    namespaces['html'], 'option')]), True)}

class Node(object):
    __doc__ = 'Represents an item in the tree'

    def __init__(self, name):
        """Creates a Node

        :arg name: The tag name associated with the node

        """
        self.name = name
        self.parent = None
        self.value = None
        self.attributes = {}
        self.childNodes = []
        self._flags = []

    def __str__(self):
        attributesStr = ' '.join(['%s="%s"' % (name, value) for name, value in self.attributes.items()])
        if attributesStr:
            return '<%s %s>' % (self.name, attributesStr)
        return '<%s>' % self.name

    def __repr__(self):
        return '<%s>' % self.name

    def appendChild(self, node):
        """Insert node as a child of the current node

        :arg node: the node to insert

        """
        raise NotImplementedError

    def insertText(self, data, insertBefore=None):
        """Insert data as text in the current node, positioned before the
        start of node insertBefore or to the end of the node's text.

        :arg data: the data to insert

        :arg insertBefore: True if you want to insert the text before the node
            and False if you want to insert it after the node

        """
        raise NotImplementedError

    def insertBefore(self, node, refNode):
        """Insert node as a child of the current node, before refNode in the
        list of child nodes. Raises ValueError if refNode is not a child of
        the current node

        :arg node: the node to insert

        :arg refNode: the child node to insert the node before

        """
        raise NotImplementedError

    def removeChild(self, node):
        """Remove node from the children of the current node

        :arg node: the child node to remove

        """
        raise NotImplementedError

    def reparentChildren(self, newParent):
        """Move all the children of the current node to newParent.
        This is needed so that trees that don't store text as nodes move the
        text in the correct way

        :arg newParent: the node to move all this node's children to

        """
        for child in self.childNodes:
            newParent.appendChild(child)
        else:
            self.childNodes = []

    def cloneNode(self):
        """Return a shallow copy of the current node i.e. a node with the same
        name and attributes but with no parent or child nodes
        """
        raise NotImplementedError

    def hasContent(self):
        """Return true if the node has children or text, false otherwise
        """
        raise NotImplementedError


class ActiveFormattingElements(list):

    def append--- This code section failed: ---

 L. 124         0  LOAD_CONST               0
                2  STORE_FAST               'equalCount'

 L. 125         4  LOAD_FAST                'node'
                6  LOAD_GLOBAL              Marker
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    86  'to 86'

 L. 126        12  LOAD_FAST                'self'
               14  LOAD_CONST               None
               16  LOAD_CONST               None
               18  LOAD_CONST               -1
               20  BUILD_SLICE_3         3 
               22  BINARY_SUBSCR    
               24  GET_ITER         
             26_0  COME_FROM            84  '84'
             26_1  COME_FROM            68  '68'
               26  FOR_ITER             86  'to 86'
               28  STORE_FAST               'element'

 L. 127        30  LOAD_FAST                'element'
               32  LOAD_GLOBAL              Marker
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 128        38  POP_TOP          
               40  BREAK_LOOP           86  'to 86'
             42_0  COME_FROM            36  '36'

 L. 129        42  LOAD_FAST                'self'
               44  LOAD_METHOD              nodesEqual
               46  LOAD_FAST                'element'
               48  LOAD_FAST                'node'
               50  CALL_METHOD_2         2  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 130        54  LOAD_FAST                'equalCount'
               56  LOAD_CONST               1
               58  INPLACE_ADD      
               60  STORE_FAST               'equalCount'
             62_0  COME_FROM            52  '52'

 L. 131        62  LOAD_FAST                'equalCount'
               64  LOAD_CONST               3
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 132        70  LOAD_FAST                'self'
               72  LOAD_METHOD              remove
               74  LOAD_FAST                'element'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 133        80  POP_TOP          
               82  BREAK_LOOP           86  'to 86'
               84  JUMP_BACK            26  'to 26'
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            40  '40'
             86_2  COME_FROM            26  '26'
             86_3  COME_FROM            10  '10'

 L. 134        86  LOAD_GLOBAL              list
               88  LOAD_METHOD              append
               90  LOAD_FAST                'self'
               92  LOAD_FAST                'node'
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 94

    def nodesEqual(self, node1, node2):
        if not node1.nameTuple == node2.nameTuple:
            return False
        if not node1.attributes == node2.attributes:
            return False
        return True


class TreeBuilder(object):
    __doc__ = 'Base treebuilder implementation\n\n    * documentClass - the class to use for the bottommost node of a document\n    * elementClass - the class to use for HTML Elements\n    * commentClass - the class to use for comments\n    * doctypeClass - the class to use for doctypes\n\n    '
    documentClass = None
    elementClass = None
    commentClass = None
    doctypeClass = None
    fragmentClass = None

    def __init__(self, namespaceHTMLElements):
        """Create a TreeBuilder

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        """
        if namespaceHTMLElements:
            self.defaultNamespace = 'http://www.w3.org/1999/xhtml'
        else:
            self.defaultNamespace = None
        self.reset()

    def reset(self):
        self.openElements = []
        self.activeFormattingElements = ActiveFormattingElements()
        self.headPointer = None
        self.formPointer = None
        self.insertFromTable = False
        self.document = self.documentClass()

    def elementInScope(self, target, variant=None):
        exactNode = hasattr(target, 'nameTuple')
        if not exactNode:
            if isinstance(target, text_type):
                target = (
                 namespaces['html'], target)
            assert isinstance(target, tuple)
        listElements, invert = listElementsMap[variant]
        for node in reversed(self.openElements):
            if exactNode:
                if node == target:
                    return True
            if not exactNode:
                if node.nameTuple == target:
                    return True
            if invert ^ (node.nameTuple in listElements):
                return False
        else:
            assert False

    def reconstructActiveFormattingElements--- This code section failed: ---

 L. 224         0  LOAD_FAST                'self'
                2  LOAD_ATTR                activeFormattingElements
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 225         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 228        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                activeFormattingElements
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               1
               20  BINARY_SUBTRACT  
               22  STORE_FAST               'i'

 L. 229        24  LOAD_FAST                'self'
               26  LOAD_ATTR                activeFormattingElements
               28  LOAD_FAST                'i'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'entry'

 L. 230        34  LOAD_FAST                'entry'
               36  LOAD_GLOBAL              Marker
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_TRUE     52  'to 52'
               42  LOAD_FAST                'entry'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                openElements
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    56  'to 56'
             52_0  COME_FROM            40  '40'

 L. 231        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM           106  '106'
             56_1  COME_FROM            50  '50'

 L. 234        56  LOAD_FAST                'entry'
               58  LOAD_GLOBAL              Marker
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE   108  'to 108'
               64  LOAD_FAST                'entry'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                openElements
               70  COMPARE_OP               not-in
               72  POP_JUMP_IF_FALSE   108  'to 108'

 L. 235        74  LOAD_FAST                'i'
               76  LOAD_CONST               0
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    88  'to 88'

 L. 237        82  LOAD_CONST               -1
               84  STORE_FAST               'i'

 L. 238        86  JUMP_FORWARD        108  'to 108'
             88_0  COME_FROM            80  '80'

 L. 239        88  LOAD_FAST                'i'
               90  LOAD_CONST               1
               92  INPLACE_SUBTRACT 
               94  STORE_FAST               'i'

 L. 241        96  LOAD_FAST                'self'
               98  LOAD_ATTR                activeFormattingElements
              100  LOAD_FAST                'i'
              102  BINARY_SUBSCR    
              104  STORE_FAST               'entry'
              106  JUMP_BACK            56  'to 56'
            108_0  COME_FROM           186  '186'
            108_1  COME_FROM           182  '182'
            108_2  COME_FROM            86  '86'
            108_3  COME_FROM            72  '72'
            108_4  COME_FROM            62  '62'

 L. 245       108  LOAD_FAST                'i'
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  STORE_FAST               'i'

 L. 248       116  LOAD_FAST                'self'
              118  LOAD_ATTR                activeFormattingElements
              120  LOAD_FAST                'i'
              122  BINARY_SUBSCR    
              124  STORE_FAST               'entry'

 L. 249       126  LOAD_FAST                'entry'
              128  LOAD_METHOD              cloneNode
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'clone'

 L. 252       134  LOAD_FAST                'self'
              136  LOAD_METHOD              insertElement
              138  LOAD_STR                 'StartTag'

 L. 253       140  LOAD_FAST                'clone'
              142  LOAD_ATTR                name

 L. 254       144  LOAD_FAST                'clone'
              146  LOAD_ATTR                namespace

 L. 255       148  LOAD_FAST                'clone'
              150  LOAD_ATTR                attributes

 L. 252       152  LOAD_CONST               ('type', 'name', 'namespace', 'data')
              154  BUILD_CONST_KEY_MAP_4     4 
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'element'

 L. 258       160  LOAD_FAST                'element'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                activeFormattingElements
              166  LOAD_FAST                'i'
              168  STORE_SUBSCR     

 L. 261       170  LOAD_FAST                'element'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                activeFormattingElements
              176  LOAD_CONST               -1
              178  BINARY_SUBSCR    
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE_BACK   108  'to 108'

 L. 262       184  JUMP_FORWARD        188  'to 188'
              186  JUMP_BACK           108  'to 108'
            188_0  COME_FROM           184  '184'

Parse error at or near `JUMP_BACK' instruction at offset 186

    def clearActiveFormattingElements(self):
        entry = self.activeFormattingElements.pop()
        while self.activeFormattingElements:
            if entry != Marker:
                entry = self.activeFormattingElements.pop()

    def elementInActiveFormattingElements(self, name):
        """Check if an element exists between the end of the active
        formatting elements and the last marker. If it does, return it, else
        return false"""
        for item in self.activeFormattingElements[::-1]:
            if item == Marker:
                break
            else:
                if item.name == name:
                    return item
        else:
            return False

    def insertRoot(self, token):
        element = self.createElement(token)
        self.openElements.append(element)
        self.document.appendChild(element)

    def insertDoctype(self, token):
        name = token['name']
        publicId = token['publicId']
        systemId = token['systemId']
        doctype = self.doctypeClass(name, publicId, systemId)
        self.document.appendChild(doctype)

    def insertComment(self, token, parent=None):
        if parent is None:
            parent = self.openElements[(-1)]
        parent.appendChild(self.commentClass(token['data']))

    def createElement(self, token):
        """Create an element but don't insert it anywhere"""
        name = token['name']
        namespace = token.get'namespace'self.defaultNamespace
        element = self.elementClassnamenamespace
        element.attributes = token['data']
        return element

    def _getInsertFromTable(self):
        return self._insertFromTable

    def _setInsertFromTable(self, value):
        """Switch the function used to insert an element from the
        normal one to the misnested table one and back again"""
        self._insertFromTable = value
        if value:
            self.insertElement = self.insertElementTable
        else:
            self.insertElement = self.insertElementNormal

    insertFromTable = property(_getInsertFromTable, _setInsertFromTable)

    def insertElementNormal(self, token):
        name = token['name']
        assert isinstance(name, text_type), 'Element %s not unicode' % name
        namespace = token.get'namespace'self.defaultNamespace
        element = self.elementClassnamenamespace
        element.attributes = token['data']
        self.openElements[(-1)].appendChild(element)
        self.openElements.append(element)
        return element

    def insertElementTable(self, token):
        """Create an element and insert it into the tree"""
        element = self.createElement(token)
        if self.openElements[(-1)].name not in tableInsertModeElements:
            return self.insertElementNormal(token)
        parent, insertBefore = self.getTableMisnestedNodePosition()
        if insertBefore is None:
            parent.appendChild(element)
        else:
            parent.insertBeforeelementinsertBefore
        self.openElements.append(element)
        return element

    def insertText(self, data, parent=None):
        """Insert text data."""
        if parent is None:
            parent = self.openElements[(-1)]
        if not self.insertFromTable and self.insertFromTable or self.openElements[(-1)].name not in tableInsertModeElements:
            parent.insertText(data)
        else:
            parent, insertBefore = self.getTableMisnestedNodePosition()
            parent.insertTextdatainsertBefore

    def getTableMisnestedNodePosition(self):
        """Get the foster parent element, and sibling to insert before
        (or None) when inserting a misnested table node"""
        lastTable = None
        fosterParent = None
        insertBefore = None
        for elm in self.openElements[::-1]:
            if elm.name == 'table':
                lastTable = elm
                break
        else:
            if lastTable:
                if lastTable.parent:
                    fosterParent = lastTable.parent
                    insertBefore = lastTable
                else:
                    fosterParent = self.openElements[(self.openElements.index(lastTable) - 1)]
            else:
                fosterParent = self.openElements[0]
            return (fosterParent, insertBefore)

    def generateImpliedEndTags(self, exclude=None):
        name = self.openElements[(-1)].name
        if name in frozenset(('dd', 'dt', 'li', 'option', 'optgroup', 'p', 'rp', 'rt')):
            if name != exclude:
                self.openElements.pop()
                self.generateImpliedEndTags(exclude)

    def getDocument(self):
        """Return the final tree"""
        return self.document

    def getFragment(self):
        """Return the final fragment"""
        fragment = self.fragmentClass()
        self.openElements[0].reparentChildren(fragment)
        return fragment

    def testSerializer(self, node):
        """Serialize the subtree of node in the format required by unit tests

        :arg node: the node from which to start serializing

        """
        raise NotImplementedError