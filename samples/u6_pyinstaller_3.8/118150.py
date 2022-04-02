# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\treebuilders\etree_lxml.py
"""Module for supporting the lxml.etree library. The idea here is to use as much
of the native library as possible, without using fragile hacks like custom element
names that break between releases. The downside of this is that we cannot represent
all possible trees; specifically the following are known to cause problems:

Text or comments as siblings of the root element
Docypes with no name

When any of these things occur, we emit a DataLossWarning
"""
from __future__ import absolute_import, division, unicode_literals
import warnings, re, sys
from . import base
from ..constants import DataLossWarning
from .. import constants
from . import etree as etree_builders
from .. import _ihatexml
import lxml.etree as etree
fullTree = True
tag_regexp = re.compile('{([^}]*)}(.*)')
comment_type = etree.Comment('asd').tag

class DocumentType(object):

    def __init__(self, name, publicId, systemId):
        self.name = name
        self.publicId = publicId
        self.systemId = systemId


class Document(object):

    def __init__(self):
        self._elementTree = None
        self._childNodes = []

    def appendChild(self, element):
        self._elementTree.getroot().addnext(element._element)

    def _getChildNodes(self):
        return self._childNodes

    childNodes = property(_getChildNodes)


def testSerializer(element):
    rv = []
    infosetFilter = _ihatexml.InfosetFilter(preventDoubleDashComments=True)

    def serializeElement--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'element'
                4  LOAD_STR                 'tag'
                6  CALL_FUNCTION_2       2  ''
             8_10  POP_JUMP_IF_TRUE    300  'to 300'

 L.  61        12  LOAD_GLOBAL              hasattr
               14  LOAD_FAST                'element'
               16  LOAD_STR                 'getroot'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE   186  'to 186'

 L.  63        22  LOAD_DEREF               'rv'
               24  LOAD_METHOD              append
               26  LOAD_STR                 '#document'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.  64        32  LOAD_FAST                'element'
               34  LOAD_ATTR                docinfo
               36  LOAD_ATTR                internalDTD
               38  POP_JUMP_IF_FALSE   122  'to 122'

 L.  65        40  LOAD_FAST                'element'
               42  LOAD_ATTR                docinfo
               44  LOAD_ATTR                public_id
               46  POP_JUMP_IF_TRUE     70  'to 70'

 L.  66        48  LOAD_FAST                'element'
               50  LOAD_ATTR                docinfo
               52  LOAD_ATTR                system_url

 L.  65        54  POP_JUMP_IF_TRUE     70  'to 70'

 L.  67        56  LOAD_STR                 '<!DOCTYPE %s>'
               58  LOAD_FAST                'element'
               60  LOAD_ATTR                docinfo
               62  LOAD_ATTR                root_name
               64  BINARY_MODULO    
               66  STORE_FAST               'dtd_str'
               68  JUMP_FORWARD         96  'to 96'
             70_0  COME_FROM            54  '54'
             70_1  COME_FROM            46  '46'

 L.  69        70  LOAD_STR                 '<!DOCTYPE %s "%s" "%s">'

 L.  70        72  LOAD_FAST                'element'
               74  LOAD_ATTR                docinfo
               76  LOAD_ATTR                root_name

 L.  71        78  LOAD_FAST                'element'
               80  LOAD_ATTR                docinfo
               82  LOAD_ATTR                public_id

 L.  72        84  LOAD_FAST                'element'
               86  LOAD_ATTR                docinfo
               88  LOAD_ATTR                system_url

 L.  69        90  BUILD_TUPLE_3         3 
               92  BINARY_MODULO    
               94  STORE_FAST               'dtd_str'
             96_0  COME_FROM            68  '68'

 L.  73        96  LOAD_DEREF               'rv'
               98  LOAD_METHOD              append
              100  LOAD_STR                 '|%s%s'
              102  LOAD_STR                 ' '
              104  LOAD_FAST                'indent'
              106  LOAD_CONST               2
              108  BINARY_ADD       
              110  BINARY_MULTIPLY  
              112  LOAD_FAST                'dtd_str'
              114  BUILD_TUPLE_2         2 
              116  BINARY_MODULO    
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
            122_0  COME_FROM            38  '38'

 L.  74       122  LOAD_FAST                'element'
              124  LOAD_METHOD              getroot
              126  CALL_METHOD_0         0  ''
              128  STORE_FAST               'next_element'

 L.  75       130  LOAD_FAST                'next_element'
              132  LOAD_METHOD              getprevious
              134  CALL_METHOD_0         0  ''
              136  LOAD_CONST               None
              138  COMPARE_OP               is-not
              140  POP_JUMP_IF_FALSE   152  'to 152'

 L.  76       142  LOAD_FAST                'next_element'
              144  LOAD_METHOD              getprevious
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'next_element'
              150  JUMP_BACK           130  'to 130'
            152_0  COME_FROM           140  '140'

 L.  77       152  LOAD_FAST                'next_element'
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
              158  POP_JUMP_IF_FALSE   184  'to 184'

 L.  78       160  LOAD_DEREF               'serializeElement'
              162  LOAD_FAST                'next_element'
              164  LOAD_FAST                'indent'
              166  LOAD_CONST               2
              168  BINARY_ADD       
              170  CALL_FUNCTION_2       2  ''
              172  POP_TOP          

 L.  79       174  LOAD_FAST                'next_element'
              176  LOAD_METHOD              getnext
              178  CALL_METHOD_0         0  ''
              180  STORE_FAST               'next_element'
              182  JUMP_BACK           152  'to 152'
            184_0  COME_FROM           158  '158'
              184  JUMP_FORWARD        808  'to 808'
            186_0  COME_FROM            20  '20'

 L.  80       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'element'
              190  LOAD_GLOBAL              str
              192  CALL_FUNCTION_2       2  ''
              194  POP_JUMP_IF_TRUE    208  'to 208'
              196  LOAD_GLOBAL              isinstance
              198  LOAD_FAST                'element'
              200  LOAD_GLOBAL              bytes
              202  CALL_FUNCTION_2       2  ''
          204_206  POP_JUMP_IF_FALSE   260  'to 260'
            208_0  COME_FROM           194  '194'

 L.  82       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'element'
              212  LOAD_GLOBAL              str
              214  CALL_FUNCTION_2       2  ''
              216  POP_JUMP_IF_TRUE    236  'to 236'
              218  LOAD_GLOBAL              sys
              220  LOAD_ATTR                version_info
              222  LOAD_CONST               0
              224  BINARY_SUBSCR    
              226  LOAD_CONST               2
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_TRUE    236  'to 236'
              232  LOAD_ASSERT              AssertionError
              234  RAISE_VARARGS_1       1  'exception instance'
            236_0  COME_FROM           230  '230'
            236_1  COME_FROM           216  '216'

 L.  83       236  LOAD_DEREF               'rv'
              238  LOAD_METHOD              append
              240  LOAD_STR                 '|%s"%s"'
              242  LOAD_STR                 ' '
              244  LOAD_FAST                'indent'
              246  BINARY_MULTIPLY  
              248  LOAD_FAST                'element'
              250  BUILD_TUPLE_2         2 
              252  BINARY_MODULO    
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_FORWARD        808  'to 808'
            260_0  COME_FROM           204  '204'

 L.  86       260  LOAD_DEREF               'rv'
              262  LOAD_METHOD              append
              264  LOAD_STR                 '#document-fragment'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          

 L.  87       270  LOAD_FAST                'element'
              272  GET_ITER         
              274  FOR_ITER            296  'to 296'
              276  STORE_FAST               'next_element'

 L.  88       278  LOAD_DEREF               'serializeElement'
              280  LOAD_FAST                'next_element'
              282  LOAD_FAST                'indent'
              284  LOAD_CONST               2
              286  BINARY_ADD       
              288  CALL_FUNCTION_2       2  ''
              290  POP_TOP          
          292_294  JUMP_BACK           274  'to 274'
          296_298  JUMP_FORWARD        808  'to 808'
            300_0  COME_FROM             8  '8'

 L.  89       300  LOAD_FAST                'element'
              302  LOAD_ATTR                tag
              304  LOAD_GLOBAL              comment_type
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   384  'to 384'

 L.  90       312  LOAD_DEREF               'rv'
              314  LOAD_METHOD              append
              316  LOAD_STR                 '|%s<!-- %s -->'
              318  LOAD_STR                 ' '
              320  LOAD_FAST                'indent'
              322  BINARY_MULTIPLY  
              324  LOAD_FAST                'element'
              326  LOAD_ATTR                text
              328  BUILD_TUPLE_2         2 
              330  BINARY_MODULO    
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L.  91       336  LOAD_GLOBAL              hasattr
              338  LOAD_FAST                'element'
              340  LOAD_STR                 'tail'
              342  CALL_FUNCTION_2       2  ''
          344_346  POP_JUMP_IF_FALSE   808  'to 808'
              348  LOAD_FAST                'element'
              350  LOAD_ATTR                tail
          352_354  POP_JUMP_IF_FALSE   808  'to 808'

 L.  92       356  LOAD_DEREF               'rv'
              358  LOAD_METHOD              append
              360  LOAD_STR                 '|%s"%s"'
              362  LOAD_STR                 ' '
              364  LOAD_FAST                'indent'
              366  BINARY_MULTIPLY  
              368  LOAD_FAST                'element'
              370  LOAD_ATTR                tail
              372  BUILD_TUPLE_2         2 
              374  BINARY_MODULO    
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          
          380_382  JUMP_FORWARD        808  'to 808'
            384_0  COME_FROM           308  '308'

 L.  94       384  LOAD_GLOBAL              isinstance
              386  LOAD_FAST                'element'
              388  LOAD_GLOBAL              etree
              390  LOAD_ATTR                _Element
              392  CALL_FUNCTION_2       2  ''
          394_396  POP_JUMP_IF_TRUE    402  'to 402'
              398  LOAD_ASSERT              AssertionError
              400  RAISE_VARARGS_1       1  'exception instance'
            402_0  COME_FROM           394  '394'

 L.  95       402  LOAD_GLOBAL              etree_builders
              404  LOAD_ATTR                tag_regexp
              406  LOAD_METHOD              match
              408  LOAD_FAST                'element'
              410  LOAD_ATTR                tag
              412  CALL_METHOD_1         1  ''
              414  STORE_FAST               'nsmatch'

 L.  96       416  LOAD_FAST                'nsmatch'
              418  LOAD_CONST               None
              420  COMPARE_OP               is-not
          422_424  POP_JUMP_IF_FALSE   488  'to 488'

 L.  97       426  LOAD_FAST                'nsmatch'
              428  LOAD_METHOD              group
              430  LOAD_CONST               1
              432  CALL_METHOD_1         1  ''
              434  STORE_FAST               'ns'

 L.  98       436  LOAD_FAST                'nsmatch'
              438  LOAD_METHOD              group
              440  LOAD_CONST               2
              442  CALL_METHOD_1         1  ''
              444  STORE_FAST               'tag'

 L.  99       446  LOAD_GLOBAL              constants
              448  LOAD_ATTR                prefixes
              450  LOAD_FAST                'ns'
              452  BINARY_SUBSCR    
              454  STORE_FAST               'prefix'

 L. 100       456  LOAD_DEREF               'rv'
              458  LOAD_METHOD              append
              460  LOAD_STR                 '|%s<%s %s>'
              462  LOAD_STR                 ' '
              464  LOAD_FAST                'indent'
              466  BINARY_MULTIPLY  
              468  LOAD_FAST                'prefix'

 L. 101       470  LOAD_DEREF               'infosetFilter'
              472  LOAD_METHOD              fromXmlName
              474  LOAD_FAST                'tag'
              476  CALL_METHOD_1         1  ''

 L. 100       478  BUILD_TUPLE_3         3 
              480  BINARY_MODULO    
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
              486  JUMP_FORWARD        518  'to 518'
            488_0  COME_FROM           422  '422'

 L. 103       488  LOAD_DEREF               'rv'
              490  LOAD_METHOD              append
              492  LOAD_STR                 '|%s<%s>'
              494  LOAD_STR                 ' '
              496  LOAD_FAST                'indent'
              498  BINARY_MULTIPLY  

 L. 104       500  LOAD_DEREF               'infosetFilter'
              502  LOAD_METHOD              fromXmlName
              504  LOAD_FAST                'element'
              506  LOAD_ATTR                tag
              508  CALL_METHOD_1         1  ''

 L. 103       510  BUILD_TUPLE_2         2 
              512  BINARY_MODULO    
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          
            518_0  COME_FROM           486  '486'

 L. 106       518  LOAD_GLOBAL              hasattr
              520  LOAD_FAST                'element'
              522  LOAD_STR                 'attrib'
              524  CALL_FUNCTION_2       2  ''
          526_528  POP_JUMP_IF_FALSE   694  'to 694'

 L. 107       530  BUILD_LIST_0          0 
              532  STORE_FAST               'attributes'

 L. 108       534  LOAD_FAST                'element'
              536  LOAD_ATTR                attrib
              538  LOAD_METHOD              items
              540  CALL_METHOD_0         0  ''
              542  GET_ITER         
              544  FOR_ITER            646  'to 646'
              546  UNPACK_SEQUENCE_2     2 
              548  STORE_FAST               'name'
              550  STORE_FAST               'value'

 L. 109       552  LOAD_GLOBAL              tag_regexp
              554  LOAD_METHOD              match
              556  LOAD_FAST                'name'
              558  CALL_METHOD_1         1  ''
              560  STORE_FAST               'nsmatch'

 L. 110       562  LOAD_FAST                'nsmatch'
              564  LOAD_CONST               None
              566  COMPARE_OP               is-not
          568_570  POP_JUMP_IF_FALSE   618  'to 618'

 L. 111       572  LOAD_FAST                'nsmatch'
              574  LOAD_METHOD              groups
              576  CALL_METHOD_0         0  ''
              578  UNPACK_SEQUENCE_2     2 
              580  STORE_FAST               'ns'
              582  STORE_FAST               'name'

 L. 112       584  LOAD_DEREF               'infosetFilter'
              586  LOAD_METHOD              fromXmlName
              588  LOAD_FAST                'name'
              590  CALL_METHOD_1         1  ''
              592  STORE_FAST               'name'

 L. 113       594  LOAD_GLOBAL              constants
              596  LOAD_ATTR                prefixes
              598  LOAD_FAST                'ns'
              600  BINARY_SUBSCR    
              602  STORE_FAST               'prefix'

 L. 114       604  LOAD_STR                 '%s %s'
              606  LOAD_FAST                'prefix'
              608  LOAD_FAST                'name'
              610  BUILD_TUPLE_2         2 
              612  BINARY_MODULO    
              614  STORE_FAST               'attr_string'
              616  JUMP_FORWARD        628  'to 628'
            618_0  COME_FROM           568  '568'

 L. 116       618  LOAD_DEREF               'infosetFilter'
              620  LOAD_METHOD              fromXmlName
              622  LOAD_FAST                'name'
              624  CALL_METHOD_1         1  ''
              626  STORE_FAST               'attr_string'
            628_0  COME_FROM           616  '616'

 L. 117       628  LOAD_FAST                'attributes'
              630  LOAD_METHOD              append
              632  LOAD_FAST                'attr_string'
              634  LOAD_FAST                'value'
              636  BUILD_TUPLE_2         2 
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          
          642_644  JUMP_BACK           544  'to 544'

 L. 119       646  LOAD_GLOBAL              sorted
              648  LOAD_FAST                'attributes'
              650  CALL_FUNCTION_1       1  ''
              652  GET_ITER         
              654  FOR_ITER            694  'to 694'
              656  UNPACK_SEQUENCE_2     2 
              658  STORE_FAST               'name'
              660  STORE_FAST               'value'

 L. 120       662  LOAD_DEREF               'rv'
              664  LOAD_METHOD              append
              666  LOAD_STR                 '|%s%s="%s"'
              668  LOAD_STR                 ' '
              670  LOAD_FAST                'indent'
              672  LOAD_CONST               2
              674  BINARY_ADD       
              676  BINARY_MULTIPLY  
              678  LOAD_FAST                'name'
              680  LOAD_FAST                'value'
              682  BUILD_TUPLE_3         3 
              684  BINARY_MODULO    
              686  CALL_METHOD_1         1  ''
              688  POP_TOP          
          690_692  JUMP_BACK           654  'to 654'
            694_0  COME_FROM           526  '526'
            694_1  COME_FROM           184  '184'

 L. 122       694  LOAD_FAST                'element'
              696  LOAD_ATTR                text
          698_700  POP_JUMP_IF_FALSE   730  'to 730'

 L. 123       702  LOAD_DEREF               'rv'
              704  LOAD_METHOD              append
              706  LOAD_STR                 '|%s"%s"'
              708  LOAD_STR                 ' '
              710  LOAD_FAST                'indent'
              712  LOAD_CONST               2
              714  BINARY_ADD       
              716  BINARY_MULTIPLY  
              718  LOAD_FAST                'element'
              720  LOAD_ATTR                text
              722  BUILD_TUPLE_2         2 
              724  BINARY_MODULO    
              726  CALL_METHOD_1         1  ''
              728  POP_TOP          
            730_0  COME_FROM           698  '698'

 L. 124       730  LOAD_FAST                'indent'
              732  LOAD_CONST               2
              734  INPLACE_ADD      
              736  STORE_FAST               'indent'

 L. 125       738  LOAD_FAST                'element'
              740  GET_ITER         
              742  FOR_ITER            760  'to 760'
              744  STORE_FAST               'child'

 L. 126       746  LOAD_DEREF               'serializeElement'
              748  LOAD_FAST                'child'
              750  LOAD_FAST                'indent'
              752  CALL_FUNCTION_2       2  ''
              754  POP_TOP          
          756_758  JUMP_BACK           742  'to 742'

 L. 127       760  LOAD_GLOBAL              hasattr
              762  LOAD_FAST                'element'
              764  LOAD_STR                 'tail'
              766  CALL_FUNCTION_2       2  ''
            768_0  COME_FROM           258  '258'
          768_770  POP_JUMP_IF_FALSE   808  'to 808'
              772  LOAD_FAST                'element'
              774  LOAD_ATTR                tail
          776_778  POP_JUMP_IF_FALSE   808  'to 808'

 L. 128       780  LOAD_DEREF               'rv'
              782  LOAD_METHOD              append
              784  LOAD_STR                 '|%s"%s"'
              786  LOAD_STR                 ' '
              788  LOAD_FAST                'indent'
              790  LOAD_CONST               2
              792  BINARY_SUBTRACT  
              794  BINARY_MULTIPLY  
              796  LOAD_FAST                'element'
              798  LOAD_ATTR                tail
              800  BUILD_TUPLE_2         2 
              802  BINARY_MODULO    
              804  CALL_METHOD_1         1  ''
              806  POP_TOP          
            808_0  COME_FROM           776  '776'
            808_1  COME_FROM           768  '768'
            808_2  COME_FROM           380  '380'
            808_3  COME_FROM           352  '352'
            808_4  COME_FROM           344  '344'
            808_5  COME_FROM           296  '296'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 768_770

    serializeElement(element, 0)
    return '\n'.join(rv)


def tostring(element):
    """Serialize an element and its child nodes to a string"""
    rv = []

    def serializeElement(element):
        if not hasattr(element, 'tag'):
            if element.docinfo.internalDTD:
                if element.docinfo.doctype:
                    dtd_str = element.docinfo.doctype
                else:
                    dtd_str = '<!DOCTYPE %s>' % element.docinfo.root_name
                rv.append(dtd_str)
            serializeElement(element.getroot())
        else:
            if element.tag == comment_type:
                rv.append('<!--%s-->' % (element.text,))
            else:
                if not element.attrib:
                    rv.append('<%s>' % (element.tag,))
                else:
                    attr = ' '.join(['%s="%s"' % (name, value) for name, value in element.attrib.items()])
                    rv.append('<%s %s>' % (element.tag, attr))
                if element.text:
                    rv.append(element.text)
                for child in element:
                    serializeElement(child)
                else:
                    rv.append('</%s>' % (element.tag,))

        if hasattr(element, 'tail'):
            if element.tail:
                rv.append(element.tail)

    serializeElement(element)
    return ''.join(rv)


class TreeBuilder(base.TreeBuilder):
    documentClass = Document
    doctypeClass = DocumentType
    elementClass = None
    commentClass = None
    fragmentClass = Document
    implementation = etree

    def __init__(self, namespaceHTMLElements, fullTree=False):
        builder = etree_builders.getETreeModule(etree, fullTree=fullTree)
        infosetFilter = self.infosetFilter = _ihatexml.InfosetFilter(preventDoubleDashComments=True)
        self.namespaceHTMLElements = namespaceHTMLElements

        class Attributes(dict):

            def __init__(self, element, value=None):
                if value is None:
                    value = {}
                self._element = element
                dict.__init__(self, value)
                for key, value in self.items():
                    if isinstance(key, tuple):
                        name = '{%s}%s' % (key[2], infosetFilter.coerceAttribute(key[1]))
                    else:
                        name = infosetFilter.coerceAttribute(key)
                    self._element._element.attrib[name] = value

            def __setitem__(self, key, value):
                dict.__setitem__(self, key, value)
                if isinstance(key, tuple):
                    name = '{%s}%s' % (key[2], infosetFilter.coerceAttribute(key[1]))
                else:
                    name = infosetFilter.coerceAttribute(key)
                self._element._element.attrib[name] = value

        class Element(builder.Element):

            def __init__(self, name, namespace):
                name = infosetFilter.coerceElement(name)
                builder.Element.__init__(self, name, namespace=namespace)
                self._attributes = Attributes(self)

            def _setName(self, name):
                self._name = infosetFilter.coerceElement(name)
                self._element.tag = self._getETreeTag(self._name, self._namespace)

            def _getName(self):
                return infosetFilter.fromXmlName(self._name)

            name = property(_getName, _setName)

            def _getAttributes(self):
                return self._attributes

            def _setAttributes(self, attributes):
                self._attributes = Attributes(self, attributes)

            attributes = property(_getAttributes, _setAttributes)

            def insertText(self, data, insertBefore=None):
                data = infosetFilter.coerceCharacters(data)
                builder.Element.insertText(self, data, insertBefore)

            def appendChild(self, child):
                builder.Element.appendChild(self, child)

        class Comment(builder.Comment):

            def __init__(self, data):
                data = infosetFilter.coerceComment(data)
                builder.Comment.__init__(self, data)

            def _setData(self, data):
                data = infosetFilter.coerceComment(data)
                self._element.text = data

            def _getData(self):
                return self._element.text

            data = property(_getData, _setData)

        self.elementClass = Element
        self.commentClass = Comment
        base.TreeBuilder.__init__(self, namespaceHTMLElements)

    def reset(self):
        base.TreeBuilder.reset(self)
        self.insertComment = self.insertCommentInitial
        self.initial_comments = []
        self.doctype = None

    def testSerializer(self, element):
        return testSerializer(element)

    def getDocument(self):
        if fullTree:
            return self.document._elementTree
        return self.document._elementTree.getroot()

    def getFragment(self):
        fragment = []
        element = self.openElements[0]._element
        if element.text:
            fragment.append(element.text)
        fragment.extend(list(element))
        if element.tail:
            fragment.append(element.tail)
        return fragment

    def insertDoctype(self, token):
        name = token['name']
        publicId = token['publicId']
        systemId = token['systemId']
        if not name:
            warnings.warn('lxml cannot represent empty doctype', DataLossWarning)
            self.doctype = None
        else:
            coercedName = self.infosetFilter.coerceElement(name)
            if coercedName != name:
                warnings.warn('lxml cannot represent non-xml doctype', DataLossWarning)
            doctype = self.doctypeClass(coercedName, publicId, systemId)
            self.doctype = doctype

    def insertCommentInitial(self, data, parent=None):
        if not parent is None:
            assert parent is self.document
        assert self.document._elementTree is None
        self.initial_comments.append(data)

    def insertCommentMain(self, data, parent=None):
        if parent == self.document:
            if self.document._elementTree.getroot()[(-1)].tag == comment_type:
                warnings.warn('lxml cannot represent adjacent comments beyond the root elements', DataLossWarning)
        super(TreeBuilder, self).insertComment(data, parent)

    def insertRoot(self, token):
        docStr = ''
        if self.doctype:
            if not self.doctype.name:
                raise AssertionError
            else:
                docStr += '<!DOCTYPE %s' % self.doctype.name
                if self.doctype.publicId is not None or self.doctype.systemId is not None:
                    docStr += ' PUBLIC "%s" ' % self.infosetFilter.coercePubid(self.doctype.publicId or '')
                    if self.doctype.systemId:
                        sysid = self.doctype.systemId
                        if sysid.find("'") >= 0:
                            if sysid.find('"') >= 0:
                                warnings.warn('DOCTYPE system cannot contain single and double quotes', DataLossWarning)
                                sysid = sysid.replace("'", 'U00027')
                        if sysid.find("'") >= 0:
                            docStr += '"%s"' % sysid
                        else:
                            docStr += "'%s'" % sysid
                    else:
                        docStr += "''"
            docStr += '>'
            if self.doctype.name != token['name']:
                warnings.warn('lxml cannot represent doctype with a different name to the root element', DataLossWarning)
        docStr += '<THIS_SHOULD_NEVER_APPEAR_PUBLICLY/>'
        root = etree.fromstring(docStr)
        for comment_token in self.initial_comments:
            comment = self.commentClass(comment_token['data'])
            root.addprevious(comment._element)
        else:
            self.document = self.documentClass()
            self.document._elementTree = root.getroottree()
            name = token['name']
            namespace = token.get('namespace', self.defaultNamespace)
            if namespace is None:
                etree_tag = name
            else:
                etree_tag = '{%s}%s' % (namespace, name)
            root.tag = etree_tag
            root_element = self.elementClass(name, namespace)
            root_element._element = root
            self.document._childNodes.append(root_element)
            self.openElements.append(root_element)
            self.insertComment = self.insertCommentMain