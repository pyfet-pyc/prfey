# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
             26_0  COME_FROM            68  '68'
               26  FOR_ITER             86  'to 86'
               28  STORE_FAST               'element'

 L. 127        30  LOAD_FAST                'element'
               32  LOAD_GLOBAL              Marker
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L. 128        38  POP_TOP          
               40  JUMP_ABSOLUTE        86  'to 86'
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
               68  POP_JUMP_IF_FALSE    26  'to 26'

 L. 132        70  LOAD_FAST                'self'
               72  LOAD_METHOD              remove
               74  LOAD_FAST                'element'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 133        80  POP_TOP          
               82  BREAK_LOOP           86  'to 86'
               84  JUMP_BACK            26  'to 26'
             86_0  COME_FROM            10  '10'

 L. 134        86  LOAD_GLOBAL              list
               88  LOAD_METHOD              append
               90  LOAD_FAST                'self'
               92  LOAD_FAST                'node'
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 42_0

    def nodesEqual(self, node1, node2):
        if not node1.nameTuple == node2.nameTuple:
            return False
        else:
            return node1.attributes == node2.attributes or False
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

    def reconstructActiveFormattingElements(self):
        if not self.activeFormattingElements:
            return
        i = len(self.activeFormattingElements) - 1
        entry = self.activeFormattingElements[i]
        if entry == Marker or entry in self.openElements:
            return
        while True:
            if entry != Marker and entry not in self.openElements:
                if i == 0:
                    i = -1
                    break
                i -= 1
                entry = self.activeFormattingElements[i]

        while True:
            i += 1
            entry = self.activeFormattingElements[i]
            clone = entry.cloneNode()
            element = self.insertElement({'type':'StartTag',  'name':clone.name, 
             'namespace':clone.namespace, 
             'data':clone.attributes})
            self.activeFormattingElements[i] = element
            if element == self.activeFormattingElements[(-1)]:
                break

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
        else:
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
        elif not self.insertFromTable or self.insertFromTable and self.openElements[(-1)].name not in tableInsertModeElements:
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
            if lastTable:
                if lastTable.parent:
                    fosterParent = lastTable.parent
                    insertBefore = lastTable
                else:
                    fosterParent = self.openElements[(self.openElements.index(lastTable) - 1)]
            else:
                fosterParent = self.openElements[0]
            return (
             fosterParent, insertBefore)

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