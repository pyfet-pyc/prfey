# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\treebuilders\dom.py
from __future__ import absolute_import, division, unicode_literals
from collections import MutableMapping
from xml.dom import minidom, Node
import weakref
from . import base
from .. import constants
from ..constants import namespaces
from .._utils import moduleFactoryFactory

def getDomBuilder(DomImplementation):
    Dom = DomImplementation

    class AttrList(MutableMapping):

        def __init__(self, element):
            self.element = element

        def __iter__(self):
            return iter(self.element.attributes.keys())

        def __setitem__(self, name, value):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                attr = self.element.ownerDocument.createAttribute(name)
                attr.value = value
                self.element.attributes[name] = attr

        def __len__(self):
            return len(self.element.attributes)

        def items(self):
            return list(self.element.attributes.items())

        def values(self):
            return list(self.element.attributes.values())

        def __getitem__(self, name):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                return self.element.attributes[name].value

        def __delitem__(self, name):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                del self.element.attributes[name]

    class NodeBuilder(base.Node):

        def __init__(self, element):
            base.Node.__init__(self, element.nodeName)
            self.element = element

        namespace = property(lambda self: hasattr(self.element, 'namespaceURI') and self.element.namespaceURI or None)

        def appendChild(self, node):
            node.parent = self
            self.element.appendChild(node.element)

        def insertText(self, data, insertBefore=None):
            text = self.element.ownerDocument.createTextNode(data)
            if insertBefore:
                self.element.insertBefore(text, insertBefore.element)
            else:
                self.element.appendChild(text)

        def insertBefore(self, node, refNode):
            self.element.insertBefore(node.element, refNode.element)
            node.parent = self

        def removeChild(self, node):
            if node.element.parentNode == self.element:
                self.element.removeChild(node.element)
            node.parent = None

        def reparentChildren(self, newParent):
            while self.element.hasChildNodes():
                child = self.element.firstChild
                self.element.removeChild(child)
                newParent.element.appendChild(child)

            self.childNodes = []

        def getAttributes(self):
            return AttrList(self.element)

        def setAttributes(self, attributes):
            if attributes:
                for name, value in list(attributes.items()):
                    if isinstance(name, tuple):
                        if name[0] is not None:
                            qualifiedName = name[0] + ':' + name[1]
                        else:
                            qualifiedName = name[1]
                        self.element.setAttributeNS(name[2], qualifiedName, value)
                    else:
                        self.element.setAttribute(name, value)

        attributes = property(getAttributes, setAttributes)

        def cloneNode(self):
            return NodeBuilder(self.element.cloneNode(False))

        def hasContent(self):
            return self.element.hasChildNodes()

        def getNameTuple(self):
            if self.namespace is None:
                return (
                 namespaces['html'], self.name)
            return (self.namespace, self.name)

        nameTuple = property(getNameTuple)

    class TreeBuilder(base.TreeBuilder):

        def documentClass(self):
            self.dom = Dom.getDOMImplementation().createDocument(None, None, None)
            return weakref.proxy(self)

        def insertDoctype(self, token):
            name = token['name']
            publicId = token['publicId']
            systemId = token['systemId']
            domimpl = Dom.getDOMImplementation()
            doctype = domimpl.createDocumentType(name, publicId, systemId)
            self.document.appendChild(NodeBuilder(doctype))
            if Dom == minidom:
                doctype.ownerDocument = self.dom

        def elementClass(self, name, namespace=None):
            if namespace is None and self.defaultNamespace is None:
                node = self.dom.createElement(name)
            else:
                node = self.dom.createElementNS(namespace, name)
            return NodeBuilder(node)

        def commentClass(self, data):
            return NodeBuilder(self.dom.createComment(data))

        def fragmentClass(self):
            return NodeBuilder(self.dom.createDocumentFragment())

        def appendChild(self, node):
            self.dom.appendChild(node.element)

        def testSerializer(self, element):
            return testSerializer(element)

        def getDocument(self):
            return self.dom

        def getFragment(self):
            return base.TreeBuilder.getFragment(self).element

        def insertText(self, data, parent=None):
            data = data
            if parent != self:
                base.TreeBuilder.insertText(self, data, parent)
            else:
                if hasattr(self.dom, '_child_node_types'):
                    if Node.TEXT_NODE not in self.dom._child_node_types:
                        self.dom._child_node_types = list(self.dom._child_node_types)
                        self.dom._child_node_types.append(Node.TEXT_NODE)
                self.dom.appendChild(self.dom.createTextNode(data))

        implementation = DomImplementation
        name = None

    def testSerializer(element):
        element.normalize()
        rv = []

        def serializeElement--- This code section failed: ---

 L. 183         0  LOAD_FAST                'element'
                2  LOAD_ATTR                nodeType
                4  LOAD_GLOBAL              Node
                6  LOAD_ATTR                DOCUMENT_TYPE_NODE
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE   130  'to 130'

 L. 184        12  LOAD_FAST                'element'
               14  LOAD_ATTR                name
               16  POP_JUMP_IF_FALSE   106  'to 106'

 L. 185        18  LOAD_FAST                'element'
               20  LOAD_ATTR                publicId
               22  POP_JUMP_IF_TRUE     30  'to 30'
               24  LOAD_FAST                'element'
               26  LOAD_ATTR                systemId
               28  POP_JUMP_IF_FALSE    80  'to 80'
             30_0  COME_FROM            22  '22'

 L. 186        30  LOAD_FAST                'element'
               32  LOAD_ATTR                publicId
               34  JUMP_IF_TRUE_OR_POP    38  'to 38'
               36  LOAD_STR                 ''
             38_0  COME_FROM            34  '34'
               38  STORE_FAST               'publicId'

 L. 187        40  LOAD_FAST                'element'
               42  LOAD_ATTR                systemId
               44  JUMP_IF_TRUE_OR_POP    48  'to 48'
               46  LOAD_STR                 ''
             48_0  COME_FROM            44  '44'
               48  STORE_FAST               'systemId'

 L. 188        50  LOAD_DEREF               'rv'
               52  LOAD_METHOD              append
               54  LOAD_STR                 '|%s<!DOCTYPE %s "%s" "%s">'

 L. 189        56  LOAD_STR                 ' '
               58  LOAD_FAST                'indent'
               60  BINARY_MULTIPLY  
               62  LOAD_FAST                'element'
               64  LOAD_ATTR                name
               66  LOAD_FAST                'publicId'
               68  LOAD_FAST                'systemId'
               70  BUILD_TUPLE_4         4 

 L. 188        72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_ABSOLUTE       126  'to 126'
             80_0  COME_FROM            28  '28'

 L. 191        80  LOAD_DEREF               'rv'
               82  LOAD_METHOD              append
               84  LOAD_STR                 '|%s<!DOCTYPE %s>'
               86  LOAD_STR                 ' '
               88  LOAD_FAST                'indent'
               90  BINARY_MULTIPLY  
               92  LOAD_FAST                'element'
               94  LOAD_ATTR                name
               96  BUILD_TUPLE_2         2 
               98  BINARY_MODULO    
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_FORWARD        500  'to 500'
            106_0  COME_FROM            16  '16'

 L. 193       106  LOAD_DEREF               'rv'
              108  LOAD_METHOD              append
              110  LOAD_STR                 '|%s<!DOCTYPE >'
              112  LOAD_STR                 ' '
              114  LOAD_FAST                'indent'
              116  BINARY_MULTIPLY  
              118  BUILD_TUPLE_1         1 
              120  BINARY_MODULO    
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
          126_128  JUMP_FORWARD        500  'to 500'
            130_0  COME_FROM            10  '10'

 L. 194       130  LOAD_FAST                'element'
              132  LOAD_ATTR                nodeType
              134  LOAD_GLOBAL              Node
              136  LOAD_ATTR                DOCUMENT_NODE
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   156  'to 156'

 L. 195       142  LOAD_DEREF               'rv'
              144  LOAD_METHOD              append
              146  LOAD_STR                 '#document'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
          152_154  JUMP_FORWARD        500  'to 500'
            156_0  COME_FROM           140  '140'

 L. 196       156  LOAD_FAST                'element'
              158  LOAD_ATTR                nodeType
              160  LOAD_GLOBAL              Node
              162  LOAD_ATTR                DOCUMENT_FRAGMENT_NODE
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   182  'to 182'

 L. 197       168  LOAD_DEREF               'rv'
              170  LOAD_METHOD              append
              172  LOAD_STR                 '#document-fragment'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
          178_180  JUMP_FORWARD        500  'to 500'
            182_0  COME_FROM           166  '166'

 L. 198       182  LOAD_FAST                'element'
              184  LOAD_ATTR                nodeType
              186  LOAD_GLOBAL              Node
              188  LOAD_ATTR                COMMENT_NODE
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   222  'to 222'

 L. 199       194  LOAD_DEREF               'rv'
              196  LOAD_METHOD              append
              198  LOAD_STR                 '|%s<!-- %s -->'
              200  LOAD_STR                 ' '
              202  LOAD_FAST                'indent'
              204  BINARY_MULTIPLY  
              206  LOAD_FAST                'element'
              208  LOAD_ATTR                nodeValue
              210  BUILD_TUPLE_2         2 
              212  BINARY_MODULO    
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
          218_220  JUMP_FORWARD        500  'to 500'
            222_0  COME_FROM           192  '192'

 L. 200       222  LOAD_FAST                'element'
              224  LOAD_ATTR                nodeType
              226  LOAD_GLOBAL              Node
              228  LOAD_ATTR                TEXT_NODE
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   262  'to 262'

 L. 201       236  LOAD_DEREF               'rv'
              238  LOAD_METHOD              append
              240  LOAD_STR                 '|%s"%s"'
              242  LOAD_STR                 ' '
              244  LOAD_FAST                'indent'
              246  BINARY_MULTIPLY  
              248  LOAD_FAST                'element'
              250  LOAD_ATTR                nodeValue
              252  BUILD_TUPLE_2         2 
              254  BINARY_MODULO    
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
              260  JUMP_FORWARD        500  'to 500'
            262_0  COME_FROM           232  '232'

 L. 203       262  LOAD_GLOBAL              hasattr
              264  LOAD_FAST                'element'
              266  LOAD_STR                 'namespaceURI'
              268  CALL_FUNCTION_2       2  ''
          270_272  POP_JUMP_IF_FALSE   310  'to 310'

 L. 204       274  LOAD_FAST                'element'
              276  LOAD_ATTR                namespaceURI
              278  LOAD_CONST               None
              280  COMPARE_OP               is-not

 L. 203   282_284  POP_JUMP_IF_FALSE   310  'to 310'

 L. 205       286  LOAD_STR                 '%s %s'
              288  LOAD_GLOBAL              constants
              290  LOAD_ATTR                prefixes
              292  LOAD_FAST                'element'
              294  LOAD_ATTR                namespaceURI
              296  BINARY_SUBSCR    

 L. 206       298  LOAD_FAST                'element'
              300  LOAD_ATTR                nodeName

 L. 205       302  BUILD_TUPLE_2         2 
              304  BINARY_MODULO    
              306  STORE_FAST               'name'
              308  JUMP_FORWARD        316  'to 316'
            310_0  COME_FROM           282  '282'
            310_1  COME_FROM           270  '270'

 L. 208       310  LOAD_FAST                'element'
              312  LOAD_ATTR                nodeName
              314  STORE_FAST               'name'
            316_0  COME_FROM           308  '308'

 L. 209       316  LOAD_DEREF               'rv'
              318  LOAD_METHOD              append
              320  LOAD_STR                 '|%s<%s>'
              322  LOAD_STR                 ' '
              324  LOAD_FAST                'indent'
              326  BINARY_MULTIPLY  
              328  LOAD_FAST                'name'
              330  BUILD_TUPLE_2         2 
              332  BINARY_MODULO    
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          

 L. 210       338  LOAD_FAST                'element'
              340  LOAD_METHOD              hasAttributes
              342  CALL_METHOD_0         0  ''
          344_346  POP_JUMP_IF_FALSE   500  'to 500'

 L. 211       348  BUILD_LIST_0          0 
              350  STORE_FAST               'attributes'

 L. 212       352  LOAD_GLOBAL              range
              354  LOAD_GLOBAL              len
              356  LOAD_FAST                'element'
              358  LOAD_ATTR                attributes
              360  CALL_FUNCTION_1       1  ''
              362  CALL_FUNCTION_1       1  ''
              364  GET_ITER         
              366  FOR_ITER            452  'to 452'
              368  STORE_FAST               'i'

 L. 213       370  LOAD_FAST                'element'
              372  LOAD_ATTR                attributes
              374  LOAD_METHOD              item
              376  LOAD_FAST                'i'
              378  CALL_METHOD_1         1  ''
              380  STORE_FAST               'attr'

 L. 214       382  LOAD_FAST                'attr'
              384  LOAD_ATTR                nodeName
              386  STORE_FAST               'name'

 L. 215       388  LOAD_FAST                'attr'
              390  LOAD_ATTR                value
              392  STORE_FAST               'value'

 L. 216       394  LOAD_FAST                'attr'
              396  LOAD_ATTR                namespaceURI
              398  STORE_FAST               'ns'

 L. 217       400  LOAD_FAST                'ns'
          402_404  POP_JUMP_IF_FALSE   428  'to 428'

 L. 218       406  LOAD_STR                 '%s %s'
              408  LOAD_GLOBAL              constants
              410  LOAD_ATTR                prefixes
              412  LOAD_FAST                'ns'
              414  BINARY_SUBSCR    
              416  LOAD_FAST                'attr'
              418  LOAD_ATTR                localName
              420  BUILD_TUPLE_2         2 
              422  BINARY_MODULO    
              424  STORE_FAST               'name'
              426  JUMP_FORWARD        434  'to 434'
            428_0  COME_FROM           402  '402'

 L. 220       428  LOAD_FAST                'attr'
              430  LOAD_ATTR                nodeName
              432  STORE_FAST               'name'
            434_0  COME_FROM           426  '426'

 L. 221       434  LOAD_FAST                'attributes'
              436  LOAD_METHOD              append
              438  LOAD_FAST                'name'
              440  LOAD_FAST                'value'
              442  BUILD_TUPLE_2         2 
              444  CALL_METHOD_1         1  ''
              446  POP_TOP          
          448_450  JUMP_BACK           366  'to 366'

 L. 223       452  LOAD_GLOBAL              sorted
              454  LOAD_FAST                'attributes'
              456  CALL_FUNCTION_1       1  ''
              458  GET_ITER         
              460  FOR_ITER            500  'to 500'
              462  UNPACK_SEQUENCE_2     2 
              464  STORE_FAST               'name'
              466  STORE_FAST               'value'

 L. 224       468  LOAD_DEREF               'rv'
              470  LOAD_METHOD              append
              472  LOAD_STR                 '|%s%s="%s"'
              474  LOAD_STR                 ' '
            476_0  COME_FROM           104  '104'
              476  LOAD_FAST                'indent'
              478  LOAD_CONST               2
              480  BINARY_ADD       
              482  BINARY_MULTIPLY  
              484  LOAD_FAST                'name'
              486  LOAD_FAST                'value'
              488  BUILD_TUPLE_3         3 
              490  BINARY_MODULO    
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
          496_498  JUMP_BACK           460  'to 460'
            500_0  COME_FROM           344  '344'
            500_1  COME_FROM           260  '260'
            500_2  COME_FROM           218  '218'
            500_3  COME_FROM           178  '178'
            500_4  COME_FROM           152  '152'
            500_5  COME_FROM           126  '126'

 L. 225       500  LOAD_FAST                'indent'
              502  LOAD_CONST               2
              504  INPLACE_ADD      
              506  STORE_FAST               'indent'

 L. 226       508  LOAD_FAST                'element'
              510  LOAD_ATTR                childNodes
              512  GET_ITER         
              514  FOR_ITER            532  'to 532'
              516  STORE_FAST               'child'

 L. 227       518  LOAD_DEREF               'serializeElement'
              520  LOAD_FAST                'child'
              522  LOAD_FAST                'indent'
              524  CALL_FUNCTION_2       2  ''
              526  POP_TOP          
          528_530  JUMP_BACK           514  'to 514'

Parse error at or near `COME_FROM' instruction at offset 476_0

        serializeElement(element, 0)
        return '\n'.join(rv)

    return locals()


getDomModule = moduleFactoryFactory(getDomBuilder)