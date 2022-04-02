# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\treebuilders\etree.py
from __future__ import absolute_import, division, unicode_literals
from six import text_type
import re
from . import base
from .. import _ihatexml
from .. import constants
from ..constants import namespaces
from .._utils import moduleFactoryFactory
tag_regexp = re.compile('{([^}]*)}(.*)')

def getETreeBuilder(ElementTreeImplementation, fullTree=False):
    ElementTree = ElementTreeImplementation
    ElementTreeCommentType = ElementTree.Comment('asd').tag

    class Element(base.Node):

        def __init__(self, name, namespace=None):
            self._name = name
            self._namespace = namespace
            self._element = ElementTree.Element(self._getETreeTag(name, namespace))
            if namespace is None:
                self.nameTuple = (
                 namespaces['html'], self._name)
            else:
                self.nameTuple = (
                 self._namespace, self._name)
            self.parent = None
            self._childNodes = []
            self._flags = []

        def _getETreeTag(self, name, namespace):
            if namespace is None:
                etree_tag = name
            else:
                etree_tag = '{%s}%s' % (namespace, name)
            return etree_tag

        def _setName(self, name):
            self._name = name
            self._element.tag = self._getETreeTag(self._name, self._namespace)

        def _getName(self):
            return self._name

        name = property(_getName, _setName)

        def _setNamespace(self, namespace):
            self._namespace = namespace
            self._element.tag = self._getETreeTag(self._name, self._namespace)

        def _getNamespace(self):
            return self._namespace

        namespace = property(_getNamespace, _setNamespace)

        def _getAttributes(self):
            return self._element.attrib

        def _setAttributes(self, attributes):
            for key in list(self._element.attrib.keys()):
                del self._element.attrib[key]
            else:
                for key, value in attributes.items():
                    if isinstance(key, tuple):
                        name = '{%s}%s' % (key[2], key[1])
                    else:
                        name = key
                    self._element.set(name, value)

        attributes = property(_getAttributes, _setAttributes)

        def _getChildNodes(self):
            return self._childNodes

        def _setChildNodes(self, value):
            del self._element[:]
            self._childNodes = []
            for element in value:
                self.insertChild(element)

        childNodes = property(_getChildNodes, _setChildNodes)

        def hasContent(self):
            """Return true if the node has children or text"""
            return bool(self._element.text or len(self._element))

        def appendChild(self, node):
            self._childNodes.append(node)
            self._element.append(node._element)
            node.parent = self

        def insertBefore(self, node, refNode):
            index = list(self._element).index(refNode._element)
            self._element.insert(index, node._element)
            node.parent = self

        def removeChild(self, node):
            self._childNodes.remove(node)
            self._element.remove(node._element)
            node.parent = None

        def insertText(self, data, insertBefore=None):
            if not len(self._element):
                if not self._element.text:
                    self._element.text = ''
                self._element.text += data
            else:
                if insertBefore is None:
                    if not self._element[(-1)].tail:
                        self._element[(-1)].tail = ''
                    self._element[(-1)].tail += data
                else:
                    children = list(self._element)
                    index = children.index(insertBefore._element)
                if index > 0:
                    if not self._element[(index - 1)].tail:
                        self._element[(index - 1)].tail = ''
                    self._element[(index - 1)].tail += data
                else:
                    if not self._element.text:
                        self._element.text = ''
                    self._element.text += data

        def cloneNode(self):
            element = type(self)(self.name, self.namespace)
            for name, value in self.attributes.items():
                element.attributes[name] = value
            else:
                return element

        def reparentChildren(self, newParent):
            if newParent.childNodes:
                newParent.childNodes[(-1)]._element.tail += self._element.text
            else:
                if not newParent._element.text:
                    newParent._element.text = ''
                if self._element.text is not None:
                    newParent._element.text += self._element.text
            self._element.text = ''
            base.Node.reparentChildren(self, newParent)

    class Comment(Element):

        def __init__(self, data):
            self._element = ElementTree.Comment(data)
            self.parent = None
            self._childNodes = []
            self._flags = []

        def _getData(self):
            return self._element.text

        def _setData(self, value):
            self._element.text = value

        data = property(_getData, _setData)

    class DocumentType(Element):

        def __init__(self, name, publicId, systemId):
            Element.__init__(self, '<!DOCTYPE>')
            self._element.text = name
            self.publicId = publicId
            self.systemId = systemId

        def _getPublicId(self):
            return self._element.get('publicId', '')

        def _setPublicId(self, value):
            if value is not None:
                self._element.set('publicId', value)

        publicId = property(_getPublicId, _setPublicId)

        def _getSystemId(self):
            return self._element.get('systemId', '')

        def _setSystemId(self, value):
            if value is not None:
                self._element.set('systemId', value)

        systemId = property(_getSystemId, _setSystemId)

    class Document(Element):

        def __init__(self):
            Element.__init__(self, 'DOCUMENT_ROOT')

    class DocumentFragment(Element):

        def __init__(self):
            Element.__init__(self, 'DOCUMENT_FRAGMENT')

    def testSerializer(element):
        rv = []

        def serializeElement--- This code section failed: ---

 L. 201         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'element'
                4  LOAD_STR                 'tag'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 202        10  LOAD_FAST                'element'
               12  LOAD_METHOD              getroot
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'element'
             18_0  COME_FROM             8  '8'

 L. 203        18  LOAD_FAST                'element'
               20  LOAD_ATTR                tag
               22  LOAD_STR                 '<!DOCTYPE>'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE   122  'to 122'

 L. 204        28  LOAD_FAST                'element'
               30  LOAD_METHOD              get
               32  LOAD_STR                 'publicId'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_TRUE     48  'to 48'
               38  LOAD_FAST                'element'
               40  LOAD_METHOD              get
               42  LOAD_STR                 'systemId'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_FALSE   100  'to 100'
             48_0  COME_FROM            36  '36'

 L. 205        48  LOAD_FAST                'element'
               50  LOAD_METHOD              get
               52  LOAD_STR                 'publicId'
               54  CALL_METHOD_1         1  ''
               56  JUMP_IF_TRUE_OR_POP    60  'to 60'
               58  LOAD_STR                 ''
             60_0  COME_FROM            56  '56'
               60  STORE_FAST               'publicId'

 L. 206        62  LOAD_FAST                'element'
               64  LOAD_METHOD              get
               66  LOAD_STR                 'systemId'
               68  CALL_METHOD_1         1  ''
               70  JUMP_IF_TRUE_OR_POP    74  'to 74'
               72  LOAD_STR                 ''
             74_0  COME_FROM            70  '70'
               74  STORE_FAST               'systemId'

 L. 207        76  LOAD_DEREF               'rv'
               78  LOAD_METHOD              append
               80  LOAD_STR                 '<!DOCTYPE %s "%s" "%s">'

 L. 208        82  LOAD_FAST                'element'
               84  LOAD_ATTR                text
               86  LOAD_FAST                'publicId'
               88  LOAD_FAST                'systemId'
               90  BUILD_TUPLE_3         3 

 L. 207        92  BINARY_MODULO    
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_FORWARD        590  'to 590'
            100_0  COME_FROM            46  '46'

 L. 210       100  LOAD_DEREF               'rv'
              102  LOAD_METHOD              append
              104  LOAD_STR                 '<!DOCTYPE %s>'
              106  LOAD_FAST                'element'
              108  LOAD_ATTR                text
              110  BUILD_TUPLE_1         1 
              112  BINARY_MODULO    
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
          118_120  JUMP_FORWARD        590  'to 590'
            122_0  COME_FROM            26  '26'

 L. 211       122  LOAD_FAST                'element'
              124  LOAD_ATTR                tag
              126  LOAD_STR                 'DOCUMENT_ROOT'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   230  'to 230'

 L. 212       132  LOAD_DEREF               'rv'
              134  LOAD_METHOD              append
              136  LOAD_STR                 '#document'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 213       142  LOAD_FAST                'element'
              144  LOAD_ATTR                text
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   180  'to 180'

 L. 214       152  LOAD_DEREF               'rv'
              154  LOAD_METHOD              append
              156  LOAD_STR                 '|%s"%s"'
              158  LOAD_STR                 ' '
              160  LOAD_FAST                'indent'
              162  LOAD_CONST               2
              164  BINARY_ADD       
              166  BINARY_MULTIPLY  
              168  LOAD_FAST                'element'
              170  LOAD_ATTR                text
              172  BUILD_TUPLE_2         2 
              174  BINARY_MODULO    
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
            180_0  COME_FROM           150  '150'

 L. 215       180  LOAD_FAST                'element'
              182  LOAD_ATTR                tail
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 216       190  LOAD_GLOBAL              TypeError
              192  LOAD_STR                 'Document node cannot have tail'
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           188  '188'

 L. 217       198  LOAD_GLOBAL              hasattr
              200  LOAD_FAST                'element'
              202  LOAD_STR                 'attrib'
              204  CALL_FUNCTION_2       2  ''
              206  POP_JUMP_IF_FALSE   226  'to 226'
              208  LOAD_GLOBAL              len
              210  LOAD_FAST                'element'
              212  LOAD_ATTR                attrib
              214  CALL_FUNCTION_1       1  ''
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 218       218  LOAD_GLOBAL              TypeError
              220  LOAD_STR                 'Document node cannot have attributes'
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
            226_0  COME_FROM           216  '216'
            226_1  COME_FROM           206  '206'
          226_228  JUMP_FORWARD        590  'to 590'
            230_0  COME_FROM           130  '130'

 L. 219       230  LOAD_FAST                'element'
              232  LOAD_ATTR                tag
              234  LOAD_DEREF               'ElementTreeCommentType'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   270  'to 270'

 L. 220       242  LOAD_DEREF               'rv'
              244  LOAD_METHOD              append
              246  LOAD_STR                 '|%s<!-- %s -->'
              248  LOAD_STR                 ' '
              250  LOAD_FAST                'indent'
              252  BINARY_MULTIPLY  
              254  LOAD_FAST                'element'
              256  LOAD_ATTR                text
              258  BUILD_TUPLE_2         2 
              260  BINARY_MODULO    
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
          266_268  JUMP_FORWARD        590  'to 590'
            270_0  COME_FROM           238  '238'

 L. 222       270  LOAD_GLOBAL              isinstance
              272  LOAD_FAST                'element'
              274  LOAD_ATTR                tag
              276  LOAD_GLOBAL              text_type
              278  CALL_FUNCTION_2       2  ''
          280_282  POP_JUMP_IF_TRUE    308  'to 308'
              284  LOAD_ASSERT              AssertionError

 L. 223       286  LOAD_STR                 'Expected unicode, got %s, %s'
              288  LOAD_GLOBAL              type
              290  LOAD_FAST                'element'
              292  LOAD_ATTR                tag
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_FAST                'element'
              298  LOAD_ATTR                tag
              300  BUILD_TUPLE_2         2 
              302  BINARY_MODULO    

 L. 222       304  CALL_FUNCTION_1       1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           280  '280'

 L. 224       308  LOAD_GLOBAL              tag_regexp
              310  LOAD_METHOD              match
              312  LOAD_FAST                'element'
              314  LOAD_ATTR                tag
              316  CALL_METHOD_1         1  ''
              318  STORE_FAST               'nsmatch'

 L. 226       320  LOAD_FAST                'nsmatch'
              322  LOAD_CONST               None
              324  COMPARE_OP               is
          326_328  POP_JUMP_IF_FALSE   338  'to 338'

 L. 227       330  LOAD_FAST                'element'
              332  LOAD_ATTR                tag
              334  STORE_FAST               'name'
              336  JUMP_FORWARD        372  'to 372'
            338_0  COME_FROM           326  '326'

 L. 229       338  LOAD_FAST                'nsmatch'
              340  LOAD_METHOD              groups
              342  CALL_METHOD_0         0  ''
              344  UNPACK_SEQUENCE_2     2 
              346  STORE_FAST               'ns'
              348  STORE_FAST               'name'

 L. 230       350  LOAD_GLOBAL              constants
              352  LOAD_ATTR                prefixes
              354  LOAD_FAST                'ns'
              356  BINARY_SUBSCR    
              358  STORE_FAST               'prefix'

 L. 231       360  LOAD_STR                 '%s %s'
              362  LOAD_FAST                'prefix'
              364  LOAD_FAST                'name'
              366  BUILD_TUPLE_2         2 
              368  BINARY_MODULO    
              370  STORE_FAST               'name'
            372_0  COME_FROM           336  '336'

 L. 232       372  LOAD_DEREF               'rv'
              374  LOAD_METHOD              append
              376  LOAD_STR                 '|%s<%s>'
              378  LOAD_STR                 ' '
              380  LOAD_FAST                'indent'
              382  BINARY_MULTIPLY  
              384  LOAD_FAST                'name'
              386  BUILD_TUPLE_2         2 
              388  BINARY_MODULO    
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

 L. 234       394  LOAD_GLOBAL              hasattr
              396  LOAD_FAST                'element'
              398  LOAD_STR                 'attrib'
              400  CALL_FUNCTION_2       2  ''
          402_404  POP_JUMP_IF_FALSE   554  'to 554'

 L. 235       406  BUILD_LIST_0          0 
              408  STORE_FAST               'attributes'

 L. 236       410  LOAD_FAST                'element'
              412  LOAD_ATTR                attrib
              414  LOAD_METHOD              items
              416  CALL_METHOD_0         0  ''
              418  GET_ITER         
              420  FOR_ITER            506  'to 506'
              422  UNPACK_SEQUENCE_2     2 
              424  STORE_FAST               'name'
              426  STORE_FAST               'value'

 L. 237       428  LOAD_GLOBAL              tag_regexp
              430  LOAD_METHOD              match
              432  LOAD_FAST                'name'
              434  CALL_METHOD_1         1  ''
              436  STORE_FAST               'nsmatch'

 L. 238       438  LOAD_FAST                'nsmatch'
              440  LOAD_CONST               None
              442  COMPARE_OP               is-not
          444_446  POP_JUMP_IF_FALSE   484  'to 484'

 L. 239       448  LOAD_FAST                'nsmatch'
              450  LOAD_METHOD              groups
              452  CALL_METHOD_0         0  ''
              454  UNPACK_SEQUENCE_2     2 
              456  STORE_FAST               'ns'
              458  STORE_FAST               'name'

 L. 240       460  LOAD_GLOBAL              constants
              462  LOAD_ATTR                prefixes
              464  LOAD_FAST                'ns'
              466  BINARY_SUBSCR    
              468  STORE_FAST               'prefix'

 L. 241       470  LOAD_STR                 '%s %s'
              472  LOAD_FAST                'prefix'
              474  LOAD_FAST                'name'
              476  BUILD_TUPLE_2         2 
              478  BINARY_MODULO    
              480  STORE_FAST               'attr_string'
              482  JUMP_FORWARD        488  'to 488'
            484_0  COME_FROM           444  '444'

 L. 243       484  LOAD_FAST                'name'
              486  STORE_FAST               'attr_string'
            488_0  COME_FROM           482  '482'

 L. 244       488  LOAD_FAST                'attributes'
              490  LOAD_METHOD              append
              492  LOAD_FAST                'attr_string'
              494  LOAD_FAST                'value'
              496  BUILD_TUPLE_2         2 
              498  CALL_METHOD_1         1  ''
              500  POP_TOP          
          502_504  JUMP_BACK           420  'to 420'

 L. 246       506  LOAD_GLOBAL              sorted
              508  LOAD_FAST                'attributes'
              510  CALL_FUNCTION_1       1  ''
              512  GET_ITER         
              514  FOR_ITER            554  'to 554'
              516  UNPACK_SEQUENCE_2     2 
              518  STORE_FAST               'name'
              520  STORE_FAST               'value'

 L. 247       522  LOAD_DEREF               'rv'
              524  LOAD_METHOD              append
              526  LOAD_STR                 '|%s%s="%s"'
              528  LOAD_STR                 ' '
              530  LOAD_FAST                'indent'
              532  LOAD_CONST               2
              534  BINARY_ADD       
              536  BINARY_MULTIPLY  
              538  LOAD_FAST                'name'
              540  LOAD_FAST                'value'
              542  BUILD_TUPLE_3         3 
              544  BINARY_MODULO    
              546  CALL_METHOD_1         1  ''
              548  POP_TOP          
          550_552  JUMP_BACK           514  'to 514'
            554_0  COME_FROM           402  '402'

 L. 248       554  LOAD_FAST                'element'
              556  LOAD_ATTR                text
          558_560  POP_JUMP_IF_FALSE   590  'to 590'

 L. 249       562  LOAD_DEREF               'rv'
              564  LOAD_METHOD              append
              566  LOAD_STR                 '|%s"%s"'
            568_0  COME_FROM            98  '98'
              568  LOAD_STR                 ' '
              570  LOAD_FAST                'indent'
              572  LOAD_CONST               2
              574  BINARY_ADD       
              576  BINARY_MULTIPLY  
              578  LOAD_FAST                'element'
              580  LOAD_ATTR                text
              582  BUILD_TUPLE_2         2 
              584  BINARY_MODULO    
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          
            590_0  COME_FROM           558  '558'
            590_1  COME_FROM           266  '266'
            590_2  COME_FROM           226  '226'
            590_3  COME_FROM           118  '118'

 L. 250       590  LOAD_FAST                'indent'
              592  LOAD_CONST               2
              594  INPLACE_ADD      
              596  STORE_FAST               'indent'

 L. 251       598  LOAD_FAST                'element'
              600  GET_ITER         
              602  FOR_ITER            620  'to 620'
              604  STORE_FAST               'child'

 L. 252       606  LOAD_DEREF               'serializeElement'
              608  LOAD_FAST                'child'
              610  LOAD_FAST                'indent'
              612  CALL_FUNCTION_2       2  ''
              614  POP_TOP          
          616_618  JUMP_BACK           602  'to 602'

 L. 253       620  LOAD_FAST                'element'
              622  LOAD_ATTR                tail
          624_626  POP_JUMP_IF_FALSE   656  'to 656'

 L. 254       628  LOAD_DEREF               'rv'
              630  LOAD_METHOD              append
              632  LOAD_STR                 '|%s"%s"'
              634  LOAD_STR                 ' '
              636  LOAD_FAST                'indent'
              638  LOAD_CONST               2
              640  BINARY_SUBTRACT  
              642  BINARY_MULTIPLY  
              644  LOAD_FAST                'element'
              646  LOAD_ATTR                tail
              648  BUILD_TUPLE_2         2 
              650  BINARY_MODULO    
              652  CALL_METHOD_1         1  ''
              654  POP_TOP          
            656_0  COME_FROM           624  '624'

Parse error at or near `COME_FROM' instruction at offset 568_0

        serializeElement(element, 0)
        return '\n'.join(rv)

    def tostring(element):
        rv = []
        filter = _ihatexml.InfosetFilter()

        def serializeElement(element):
            if isinstance(element, ElementTree.ElementTree):
                element = element.getroot()
            elif element.tag == '<!DOCTYPE>':
                if element.get('publicId') or element.get('systemId'):
                    publicId = element.get('publicId') or ''
                    systemId = element.get('systemId') or ''
                    rv.append('<!DOCTYPE %s PUBLIC "%s" "%s">' % (
                     element.text, publicId, systemId))
                else:
                    rv.append('<!DOCTYPE %s>' % (element.text,))
            else:
                if element.tag == 'DOCUMENT_ROOT':
                    if element.text is not None:
                        rv.append(element.text)
                    else:
                        if element.tail is not None:
                            raise TypeError('Document node cannot have tail')
                        if hasattr(element, 'attrib') and len(element.attrib):
                            raise TypeError('Document node cannot have attributes')
                    for child in element:
                        serializeElement(child)

                else:
                    if element.tag == ElementTreeCommentType:
                        rv.append('<!--%s-->' % (element.text,))
                    else:
                        if not element.attrib:
                            rv.append('<%s>' % (filter.fromXmlName(element.tag),))
                        else:
                            attr = ' '.join(['%s="%s"' % (
                             filter.fromXmlName(name), value) for name, value in element.attrib.items()])
                            rv.append('<%s %s>' % (element.tag, attr))
                        if element.text:
                            rv.append(element.text)
                        for child in element:
                            serializeElement(child)

                        rv.append('</%s>' % (element.tag,))
            if element.tail:
                rv.append(element.tail)

        serializeElement(element)
        return ''.join(rv)

    class TreeBuilder(base.TreeBuilder):
        documentClass = Document
        doctypeClass = DocumentType
        elementClass = Element
        commentClass = Comment
        fragmentClass = DocumentFragment
        implementation = ElementTreeImplementation

        def testSerializer(self, element):
            return testSerializer(element)

        def getDocument(self):
            if fullTree:
                return self.document._element
            if self.defaultNamespace is not None:
                return self.document._element.find('{%s}html' % self.defaultNamespace)
            return self.document._element.find('html')

        def getFragment(self):
            return base.TreeBuilder.getFragment(self)._element

    return locals()


getETreeModule = moduleFactoryFactory(getETreeBuilder)