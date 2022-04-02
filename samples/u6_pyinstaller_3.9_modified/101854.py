# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\dom\expatbuilder.py
"""Facility to use the Expat parser to load a minidom instance
from a string or file.

This avoids all the overhead of SAX and pulldom to gain performance.
"""
from xml.dom import xmlbuilder, minidom, Node
from xml.dom import EMPTY_NAMESPACE, EMPTY_PREFIX, XMLNS_NAMESPACE
from xml.parsers import expat
from xml.dom.minidom import _append_child, _set_attribute_node
import xml.dom.NodeFilter as NodeFilter
TEXT_NODE = Node.TEXT_NODE
CDATA_SECTION_NODE = Node.CDATA_SECTION_NODE
DOCUMENT_NODE = Node.DOCUMENT_NODE
FILTER_ACCEPT = xmlbuilder.DOMBuilderFilter.FILTER_ACCEPT
FILTER_REJECT = xmlbuilder.DOMBuilderFilter.FILTER_REJECT
FILTER_SKIP = xmlbuilder.DOMBuilderFilter.FILTER_SKIP
FILTER_INTERRUPT = xmlbuilder.DOMBuilderFilter.FILTER_INTERRUPT
theDOMImplementation = minidom.getDOMImplementation()
_typeinfo_map = {'CDATA':minidom.TypeInfo(None, 'cdata'), 
 'ENUM':minidom.TypeInfo(None, 'enumeration'), 
 'ENTITY':minidom.TypeInfo(None, 'entity'), 
 'ENTITIES':minidom.TypeInfo(None, 'entities'), 
 'ID':minidom.TypeInfo(None, 'id'), 
 'IDREF':minidom.TypeInfo(None, 'idref'), 
 'IDREFS':minidom.TypeInfo(None, 'idrefs'), 
 'NMTOKEN':minidom.TypeInfo(None, 'nmtoken'), 
 'NMTOKENS':minidom.TypeInfo(None, 'nmtokens')}

class ElementInfo(object):
    __slots__ = ('_attr_info', '_model', 'tagName')

    def __init__(self, tagName, model=None):
        self.tagName = tagName
        self._attr_info = []
        self._model = model

    def __getstate__(self):
        return (
         self._attr_info, self._model, self.tagName)

    def __setstate__(self, state):
        self._attr_info, self._model, self.tagName = state

    def getAttributeType(self, aname):
        for info in self._attr_info:
            if info[1] == aname:
                t = info[(-2)]
                if t[0] == '(':
                    return _typeinfo_map['ENUM']
                return _typeinfo_map[info[(-2)]]
            return minidom._no_type

    def getAttributeTypeNS(self, namespaceURI, localName):
        return minidom._no_type

    def isElementContent--- This code section failed: ---

 L.  88         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _model
                4  POP_JUMP_IF_FALSE    36  'to 36'

 L.  89         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _model
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'type'

 L.  90        16  LOAD_FAST                'type'
               18  LOAD_GLOBAL              expat
               20  LOAD_ATTR                model
               22  LOAD_ATTR                XML_CTYPE_ANY

 L.  91        24  LOAD_GLOBAL              expat
               26  LOAD_ATTR                model
               28  LOAD_ATTR                XML_CTYPE_MIXED

 L.  90        30  BUILD_TUPLE_2         2 
               32  <118>                 1  ''
               34  RETURN_VALUE     
             36_0  COME_FROM             4  '4'

 L.  93        36  LOAD_CONST               False
               38  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 32

    def isEmpty(self):
        if self._model:
            return self._model[0] == expat.model.XML_CTYPE_EMPTY
        return False

    def isId(self, aname):
        for info in self._attr_info:
            if info[1] == aname:
                return info[(-2)] == 'ID'
            return False

    def isIdNS(self, euri, ename, auri, aname):
        return self.isId((auri, aname))


def _intern(builder, s):
    return builder._intern_setdefault(s, s)


def _parse_ns_name--- This code section failed: ---

 L. 115         0  LOAD_STR                 ' '
                2  LOAD_FAST                'name'
                4  <118>                 0  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L. 116        12  LOAD_FAST                'name'
               14  LOAD_METHOD              split
               16  LOAD_STR                 ' '
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'parts'

 L. 117        22  LOAD_FAST                'builder'
               24  LOAD_ATTR                _intern_setdefault
               26  STORE_FAST               'intern'

 L. 118        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'parts'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               3
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    94  'to 94'

 L. 119        40  LOAD_FAST                'parts'
               42  UNPACK_SEQUENCE_3     3 
               44  STORE_FAST               'uri'
               46  STORE_FAST               'localname'
               48  STORE_FAST               'prefix'

 L. 120        50  LOAD_FAST                'intern'
               52  LOAD_FAST                'prefix'
               54  LOAD_FAST                'prefix'
               56  CALL_FUNCTION_2       2  ''
               58  STORE_FAST               'prefix'

 L. 121        60  LOAD_STR                 '%s:%s'
               62  LOAD_FAST                'prefix'
               64  LOAD_FAST                'localname'
               66  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               70  STORE_FAST               'qname'

 L. 122        72  LOAD_FAST                'intern'
               74  LOAD_FAST                'qname'
               76  LOAD_FAST                'qname'
               78  CALL_FUNCTION_2       2  ''
               80  STORE_FAST               'qname'

 L. 123        82  LOAD_FAST                'intern'
               84  LOAD_FAST                'localname'
               86  LOAD_FAST                'localname'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'localname'
               92  JUMP_FORWARD        146  'to 146'
             94_0  COME_FROM            38  '38'

 L. 124        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'parts'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               2
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   134  'to 134'

 L. 125       106  LOAD_FAST                'parts'
              108  UNPACK_SEQUENCE_2     2 
              110  STORE_FAST               'uri'
              112  STORE_FAST               'localname'

 L. 126       114  LOAD_GLOBAL              EMPTY_PREFIX
              116  STORE_FAST               'prefix'

 L. 127       118  LOAD_FAST                'intern'
              120  LOAD_FAST                'localname'
              122  LOAD_FAST                'localname'
              124  CALL_FUNCTION_2       2  ''
              126  DUP_TOP          
              128  STORE_FAST               'qname'
              130  STORE_FAST               'localname'
              132  JUMP_FORWARD        146  'to 146'
            134_0  COME_FROM           104  '104'

 L. 129       134  LOAD_GLOBAL              ValueError
              136  LOAD_STR                 'Unsupported syntax: spaces in URIs not supported: %r'
              138  LOAD_FAST                'name'
              140  BINARY_MODULO    
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           132  '132'
            146_1  COME_FROM            92  '92'

 L. 130       146  LOAD_FAST                'intern'
              148  LOAD_FAST                'uri'
              150  LOAD_FAST                'uri'
              152  CALL_FUNCTION_2       2  ''
              154  LOAD_FAST                'localname'
              156  LOAD_FAST                'prefix'
              158  LOAD_FAST                'qname'
              160  BUILD_TUPLE_4         4 
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class ExpatBuilder:
    __doc__ = 'Document builder that uses Expat to build a ParsedXML.DOM document\n    instance.'

    def __init__--- This code section failed: ---

 L. 138         0  LOAD_FAST                'options'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 139         8  LOAD_GLOBAL              xmlbuilder
               10  LOAD_METHOD              Options
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'options'
             16_0  COME_FROM             6  '6'

 L. 140        16  LOAD_FAST                'options'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _options

 L. 141        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _options
               26  LOAD_ATTR                filter
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    50  'to 50'

 L. 142        34  LOAD_GLOBAL              FilterVisibilityController
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _options
               40  LOAD_ATTR                filter
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _filter
               48  JUMP_FORWARD         62  'to 62'
             50_0  COME_FROM            32  '32'

 L. 144        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _filter

 L. 147        56  LOAD_GLOBAL              id
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _finish_start_element
             62_0  COME_FROM            48  '48'

 L. 148        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _parser

 L. 149        68  LOAD_FAST                'self'
               70  LOAD_METHOD              reset
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def createParser(self):
        """Create a new parser object."""
        return expat.ParserCreate()

    def getParser(self):
        """Return the parser object, creating a new one if needed."""
        if not self._parser:
            self._parser = self.createParser()
            self._intern_setdefault = self._parser.intern.setdefault
            self._parser.buffer_text = True
            self._parser.ordered_attributes = True
            self._parser.specified_attributes = True
            self.install(self._parser)
        return self._parser

    def reset(self):
        """Free all data structures used during DOM construction."""
        self.document = theDOMImplementation.createDocument(EMPTY_NAMESPACE, None, None)
        self.curNode = self.document
        self._elem_info = self.document._elem_info
        self._cdata = False

    def install(self, parser):
        """Install the callbacks needed to build the DOM into the parser."""
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.StartElementHandler = self.first_element_handler
        parser.EndElementHandler = self.end_element_handler
        parser.ProcessingInstructionHandler = self.pi_handler
        if self._options.entities:
            parser.EntityDeclHandler = self.entity_decl_handler
        else:
            parser.NotationDeclHandler = self.notation_decl_handler
            if self._options.comments:
                parser.CommentHandler = self.comment_handler
            if self._options.cdata_sections:
                parser.StartCdataSectionHandler = self.start_cdata_section_handler
                parser.EndCdataSectionHandler = self.end_cdata_section_handler
                parser.CharacterDataHandler = self.character_data_handler_cdata
            else:
                parser.CharacterDataHandler = self.character_data_handler
        parser.ExternalEntityRefHandler = self.external_entity_ref_handler
        parser.XmlDeclHandler = self.xml_decl_handler
        parser.ElementDeclHandler = self.element_decl_handler
        parser.AttlistDeclHandler = self.attlist_decl_handler

    def parseFile--- This code section failed: ---

 L. 200         0  LOAD_FAST                'self'
                2  LOAD_METHOD              getParser
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'parser'

 L. 201         8  LOAD_CONST               True
               10  STORE_FAST               'first_buffer'

 L. 202        12  SETUP_FINALLY        86  'to 86'

 L. 204        14  LOAD_FAST                'file'
               16  LOAD_METHOD              read
               18  LOAD_CONST               16384
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'buffer'

 L. 205        24  LOAD_FAST                'buffer'
               26  POP_JUMP_IF_TRUE     30  'to 30'

 L. 206        28  BREAK_LOOP           70  'to 70'
             30_0  COME_FROM            26  '26'

 L. 207        30  LOAD_FAST                'parser'
               32  LOAD_METHOD              Parse
               34  LOAD_FAST                'buffer'
               36  LOAD_CONST               False
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          

 L. 208        42  LOAD_FAST                'first_buffer'
               44  POP_JUMP_IF_FALSE    64  'to 64'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                document
               50  LOAD_ATTR                documentElement
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L. 209        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _setup_subset
               58  LOAD_FAST                'buffer'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            44  '44'

 L. 210        64  LOAD_CONST               False
               66  STORE_FAST               'first_buffer'
               68  JUMP_BACK            14  'to 14'

 L. 211        70  LOAD_FAST                'parser'
               72  LOAD_METHOD              Parse
               74  LOAD_CONST               b''
               76  LOAD_CONST               True
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          
               82  POP_BLOCK        
               84  JUMP_FORWARD        104  'to 104'
             86_0  COME_FROM_FINALLY    12  '12'

 L. 212        86  DUP_TOP          
               88  LOAD_GLOBAL              ParseEscape
               90  <121>               102  ''
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 213        98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
              102  <48>             
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            84  '84'

 L. 214       104  LOAD_FAST                'self'
              106  LOAD_ATTR                document
              108  STORE_FAST               'doc'

 L. 215       110  LOAD_FAST                'self'
              112  LOAD_METHOD              reset
              114  CALL_METHOD_0         0  ''
              116  POP_TOP          

 L. 216       118  LOAD_CONST               None
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _parser

 L. 217       124  LOAD_FAST                'doc'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 90

    def parseString--- This code section failed: ---

 L. 221         0  LOAD_FAST                'self'
                2  LOAD_METHOD              getParser
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'parser'

 L. 222         8  SETUP_FINALLY        36  'to 36'

 L. 223        10  LOAD_FAST                'parser'
               12  LOAD_METHOD              Parse
               14  LOAD_FAST                'string'
               16  LOAD_CONST               True
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          

 L. 224        22  LOAD_FAST                'self'
               24  LOAD_METHOD              _setup_subset
               26  LOAD_FAST                'string'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_FORWARD         54  'to 54'
             36_0  COME_FROM_FINALLY     8  '8'

 L. 225        36  DUP_TOP          
               38  LOAD_GLOBAL              ParseEscape
               40  <121>                52  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 226        48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  <48>             
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            34  '34'

 L. 227        54  LOAD_FAST                'self'
               56  LOAD_ATTR                document
               58  STORE_FAST               'doc'

 L. 228        60  LOAD_FAST                'self'
               62  LOAD_METHOD              reset
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L. 229        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _parser

 L. 230        74  LOAD_FAST                'doc'
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 40

    def _setup_subset(self, buffer):
        """Load the internal subset if there might be one."""
        if self.document.doctype:
            extractor = InternalSubsetExtractor()
            extractor.parseString(buffer)
            subset = extractor.getSubset()
            self.document.doctype.internalSubset = subset

    def start_doctype_decl_handler--- This code section failed: ---

 L. 242         0  LOAD_FAST                'self'
                2  LOAD_ATTR                document
                4  LOAD_ATTR                implementation
                6  LOAD_METHOD              createDocumentType

 L. 243         8  LOAD_FAST                'doctypeName'
               10  LOAD_FAST                'publicId'
               12  LOAD_FAST                'systemId'

 L. 242        14  CALL_METHOD_3         3  ''
               16  STORE_FAST               'doctype'

 L. 244        18  LOAD_FAST                'self'
               20  LOAD_ATTR                document
               22  LOAD_FAST                'doctype'
               24  STORE_ATTR               ownerDocument

 L. 245        26  LOAD_GLOBAL              _append_child
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                document
               32  LOAD_FAST                'doctype'
               34  CALL_FUNCTION_2       2  ''
               36  POP_TOP          

 L. 246        38  LOAD_FAST                'doctype'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                document
               44  STORE_ATTR               doctype

 L. 247        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _filter
               50  POP_JUMP_IF_FALSE   106  'to 106'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _filter
               56  LOAD_METHOD              acceptNode
               58  LOAD_FAST                'doctype'
               60  CALL_METHOD_1         1  ''
               62  LOAD_GLOBAL              FILTER_REJECT
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE   106  'to 106'

 L. 248        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                document
               74  STORE_ATTR               doctype

 L. 249        76  LOAD_FAST                'self'
               78  LOAD_ATTR                document
               80  LOAD_ATTR                childNodes
               82  LOAD_CONST               -1
               84  DELETE_SUBSCR    

 L. 250        86  LOAD_CONST               None
               88  STORE_FAST               'doctype'

 L. 251        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _parser
               96  STORE_ATTR               EntityDeclHandler

 L. 252        98  LOAD_CONST               None
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                _parser
              104  STORE_ATTR               NotationDeclHandler
            106_0  COME_FROM            66  '66'
            106_1  COME_FROM            50  '50'

 L. 253       106  LOAD_FAST                'has_internal_subset'
              108  POP_JUMP_IF_FALSE   160  'to 160'

 L. 254       110  LOAD_FAST                'doctype'
              112  LOAD_CONST               None
              114  <117>                 1  ''
              116  POP_JUMP_IF_FALSE   134  'to 134'

 L. 255       118  BUILD_LIST_0          0 
              120  LOAD_FAST                'doctype'
              122  LOAD_ATTR                entities
              124  STORE_ATTR               _seq

 L. 256       126  BUILD_LIST_0          0 
              128  LOAD_FAST                'doctype'
              130  LOAD_ATTR                notations
              132  STORE_ATTR               _seq
            134_0  COME_FROM           116  '116'

 L. 257       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _parser
              140  STORE_ATTR               CommentHandler

 L. 258       142  LOAD_CONST               None
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                _parser
              148  STORE_ATTR               ProcessingInstructionHandler

 L. 259       150  LOAD_FAST                'self'
              152  LOAD_ATTR                end_doctype_decl_handler
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _parser
              158  STORE_ATTR               EndDoctypeDeclHandler
            160_0  COME_FROM           108  '108'

Parse error at or near `<117>' instruction at offset 114

    def end_doctype_decl_handler(self):
        if self._options.comments:
            self._parser.CommentHandler = self.comment_handler
        self._parser.ProcessingInstructionHandler = self.pi_handler
        if not self._elem_info:
            if not self._filter:
                self._finish_end_element = id

    def pi_handler(self, target, data):
        node = self.document.createProcessingInstruction(target, data)
        _append_child(self.curNode, node)
        if self._filter:
            if self._filter.acceptNode(node) == FILTER_REJECT:
                self.curNode.removeChild(node)

    def character_data_handler_cdata(self, data):
        childNodes = self.curNode.childNodes
        if self._cdata:
            if self._cdata_continue:
                if childNodes[(-1)].nodeType == CDATA_SECTION_NODE:
                    childNodes[(-1)].appendData(data)
                    return None
            node = self.document.createCDATASection(data)
            self._cdata_continue = True
        else:
            if childNodes:
                if childNodes[(-1)].nodeType == TEXT_NODE:
                    node = childNodes[(-1)]
                    value = node.data + data
                    node.data = value
                    return
            node = minidom.Text()
            node.data = data
            node.ownerDocument = self.document
        _append_child(self.curNode, node)

    def character_data_handler(self, data):
        childNodes = self.curNode.childNodes
        if childNodes:
            if childNodes[(-1)].nodeType == TEXT_NODE:
                node = childNodes[(-1)]
                node.data = node.data + data
                return
        node = minidom.Text()
        node.data = node.data + data
        node.ownerDocument = self.document
        _append_child(self.curNode, node)

    def entity_decl_handler--- This code section failed: ---

 L. 307         0  LOAD_FAST                'is_parameter_entity'
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L. 309         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 310         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _options
               12  LOAD_ATTR                entities
               14  POP_JUMP_IF_TRUE     20  'to 20'

 L. 311        16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 312        20  LOAD_FAST                'self'
               22  LOAD_ATTR                document
               24  LOAD_METHOD              _create_entity
               26  LOAD_FAST                'entityName'
               28  LOAD_FAST                'publicId'

 L. 313        30  LOAD_FAST                'systemId'
               32  LOAD_FAST                'notationName'

 L. 312        34  CALL_METHOD_4         4  ''
               36  STORE_FAST               'node'

 L. 314        38  LOAD_FAST                'value'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    70  'to 70'

 L. 317        46  LOAD_FAST                'self'
               48  LOAD_ATTR                document
               50  LOAD_METHOD              createTextNode
               52  LOAD_FAST                'value'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'child'

 L. 318        58  LOAD_FAST                'node'
               60  LOAD_ATTR                childNodes
               62  LOAD_METHOD              append
               64  LOAD_FAST                'child'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
             70_0  COME_FROM            44  '44'

 L. 319        70  LOAD_FAST                'self'
               72  LOAD_ATTR                document
               74  LOAD_ATTR                doctype
               76  LOAD_ATTR                entities
               78  LOAD_ATTR                _seq
               80  LOAD_METHOD              append
               82  LOAD_FAST                'node'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 320        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _filter
               92  POP_JUMP_IF_FALSE   124  'to 124'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _filter
               98  LOAD_METHOD              acceptNode
              100  LOAD_FAST                'node'
              102  CALL_METHOD_1         1  ''
              104  LOAD_GLOBAL              FILTER_REJECT
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 321       110  LOAD_FAST                'self'
              112  LOAD_ATTR                document
              114  LOAD_ATTR                doctype
              116  LOAD_ATTR                entities
              118  LOAD_ATTR                _seq
              120  LOAD_CONST               -1
              122  DELETE_SUBSCR    
            124_0  COME_FROM           108  '108'
            124_1  COME_FROM            92  '92'

Parse error at or near `<117>' instruction at offset 42

    def notation_decl_handler(self, notationName, base, systemId, publicId):
        node = self.document._create_notation(notationName, publicId, systemId)
        self.document.doctype.notations._seq.append(node)
        if self._filter:
            if self._filter.acceptNode(node) == FILTER_ACCEPT:
                del self.document.doctype.notations._seq[-1]

    def comment_handler(self, data):
        node = self.document.createComment(data)
        _append_child(self.curNode, node)
        if self._filter:
            if self._filter.acceptNode(node) == FILTER_REJECT:
                self.curNode.removeChild(node)

    def start_cdata_section_handler(self):
        self._cdata = True
        self._cdata_continue = False

    def end_cdata_section_handler(self):
        self._cdata = False
        self._cdata_continue = False

    def external_entity_ref_handler(self, context, base, systemId, publicId):
        return 1

    def first_element_handler--- This code section failed: ---

 L. 347         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _filter
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _elem_info
               14  POP_JUMP_IF_TRUE     22  'to 22'

 L. 348        16  LOAD_GLOBAL              id
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _finish_end_element
             22_0  COME_FROM            14  '14'
             22_1  COME_FROM             8  '8'

 L. 349        22  LOAD_FAST                'self'
               24  LOAD_ATTR                start_element_handler
               26  LOAD_FAST                'self'
               28  LOAD_METHOD              getParser
               30  CALL_METHOD_0         0  ''
               32  STORE_ATTR               StartElementHandler

 L. 350        34  LOAD_FAST                'self'
               36  LOAD_METHOD              start_element_handler
               38  LOAD_FAST                'name'
               40  LOAD_FAST                'attributes'
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def start_element_handler--- This code section failed: ---

 L. 353         0  LOAD_FAST                'self'
                2  LOAD_ATTR                document
                4  LOAD_METHOD              createElement
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'node'

 L. 354        12  LOAD_GLOBAL              _append_child
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                curNode
               18  LOAD_FAST                'node'
               20  CALL_FUNCTION_2       2  ''
               22  POP_TOP          

 L. 355        24  LOAD_FAST                'node'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               curNode

 L. 357        30  LOAD_FAST                'attributes'
               32  POP_JUMP_IF_FALSE   112  'to 112'

 L. 358        34  LOAD_GLOBAL              range
               36  LOAD_CONST               0
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'attributes'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_CONST               2
               46  CALL_FUNCTION_3       3  ''
               48  GET_ITER         
               50  FOR_ITER            112  'to 112'
               52  STORE_FAST               'i'

 L. 359        54  LOAD_GLOBAL              minidom
               56  LOAD_METHOD              Attr
               58  LOAD_FAST                'attributes'
               60  LOAD_FAST                'i'
               62  BINARY_SUBSCR    
               64  LOAD_GLOBAL              EMPTY_NAMESPACE

 L. 360        66  LOAD_CONST               None
               68  LOAD_GLOBAL              EMPTY_PREFIX

 L. 359        70  CALL_METHOD_4         4  ''
               72  STORE_FAST               'a'

 L. 361        74  LOAD_FAST                'attributes'
               76  LOAD_FAST                'i'
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  BINARY_SUBSCR    
               84  STORE_FAST               'value'

 L. 362        86  LOAD_FAST                'value'
               88  LOAD_FAST                'a'
               90  STORE_ATTR               value

 L. 363        92  LOAD_FAST                'self'
               94  LOAD_ATTR                document
               96  LOAD_FAST                'a'
               98  STORE_ATTR               ownerDocument

 L. 364       100  LOAD_GLOBAL              _set_attribute_node
              102  LOAD_FAST                'node'
              104  LOAD_FAST                'a'
              106  CALL_FUNCTION_2       2  ''
              108  POP_TOP          
              110  JUMP_BACK            50  'to 50'
            112_0  COME_FROM            32  '32'

 L. 366       112  LOAD_FAST                'node'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                document
              118  LOAD_ATTR                documentElement
              120  <117>                 1  ''
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L. 367       124  LOAD_FAST                'self'
              126  LOAD_METHOD              _finish_start_element
              128  LOAD_FAST                'node'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
            134_0  COME_FROM           122  '122'

Parse error at or near `<117>' instruction at offset 120

    def _finish_start_element--- This code section failed: ---

 L. 370         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _filter
                4  POP_JUMP_IF_FALSE   102  'to 102'

 L. 373         6  LOAD_FAST                'node'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                document
               12  LOAD_ATTR                documentElement
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 374        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 375        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _filter
               26  LOAD_METHOD              startContainer
               28  LOAD_FAST                'node'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'filt'

 L. 376        34  LOAD_FAST                'filt'
               36  LOAD_GLOBAL              FILTER_REJECT
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 378        42  LOAD_GLOBAL              Rejecter
               44  LOAD_FAST                'self'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM            40  '40'

 L. 379        52  LOAD_FAST                'filt'
               54  LOAD_GLOBAL              FILTER_SKIP
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 382        60  LOAD_GLOBAL              Skipper
               62  LOAD_FAST                'self'
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          
               68  JUMP_FORWARD         74  'to 74'
             70_0  COME_FROM            58  '58'

 L. 384        70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'
             74_1  COME_FROM            50  '50'

 L. 385        74  LOAD_FAST                'node'
               76  LOAD_ATTR                parentNode
               78  LOAD_FAST                'self'
               80  STORE_ATTR               curNode

 L. 386        82  LOAD_FAST                'node'
               84  LOAD_ATTR                parentNode
               86  LOAD_METHOD              removeChild
               88  LOAD_FAST                'node'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 387        94  LOAD_FAST                'node'
               96  LOAD_METHOD              unlink
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
            102_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 14

    def end_element_handler(self, name):
        curNode = self.curNode
        self.curNode = curNode.parentNode
        self._finish_end_element(curNode)

    def _finish_end_element--- This code section failed: ---

 L. 398         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _elem_info
                4  LOAD_METHOD              get
                6  LOAD_FAST                'curNode'
                8  LOAD_ATTR                tagName
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'info'

 L. 399        14  LOAD_FAST                'info'
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L. 400        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _handle_white_text_nodes
               22  LOAD_FAST                'curNode'
               24  LOAD_FAST                'info'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          
             30_0  COME_FROM            16  '16'

 L. 401        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _filter
               34  POP_JUMP_IF_FALSE    88  'to 88'

 L. 402        36  LOAD_FAST                'curNode'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                document
               42  LOAD_ATTR                documentElement
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 403        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 404        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _filter
               56  LOAD_METHOD              acceptNode
               58  LOAD_FAST                'curNode'
               60  CALL_METHOD_1         1  ''
               62  LOAD_GLOBAL              FILTER_REJECT
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    88  'to 88'

 L. 405        68  LOAD_FAST                'self'
               70  LOAD_ATTR                curNode
               72  LOAD_METHOD              removeChild
               74  LOAD_FAST                'curNode'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 406        80  LOAD_FAST                'curNode'
               82  LOAD_METHOD              unlink
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          
             88_0  COME_FROM            66  '66'
             88_1  COME_FROM            34  '34'

Parse error at or near `<117>' instruction at offset 44

    def _handle_white_text_nodes(self, node, info):
        return self._options.whitespace_in_element_content or info.isElementContent() or None
        L = []
        for child in node.childNodes:
            if child.nodeType == TEXT_NODE:
                child.data.strip() or L.append(child)
        else:
            for child in L:
                node.removeChild(child)

    def element_decl_handler--- This code section failed: ---

 L. 426         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _elem_info
                4  LOAD_METHOD              get
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'info'

 L. 427        12  LOAD_FAST                'info'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 428        20  LOAD_GLOBAL              ElementInfo
               22  LOAD_FAST                'name'
               24  LOAD_FAST                'model'
               26  CALL_FUNCTION_2       2  ''
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _elem_info
               32  LOAD_FAST                'name'
               34  STORE_SUBSCR     
               36  JUMP_FORWARD         58  'to 58'
             38_0  COME_FROM            18  '18'

 L. 430        38  LOAD_FAST                'info'
               40  LOAD_ATTR                _model
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  <74>             
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            46  '46'

 L. 431        52  LOAD_FAST                'model'
               54  LOAD_FAST                'info'
               56  STORE_ATTR               _model
             58_0  COME_FROM            36  '36'

Parse error at or near `<117>' instruction at offset 16

    def attlist_decl_handler--- This code section failed: ---

 L. 434         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _elem_info
                4  LOAD_METHOD              get
                6  LOAD_FAST                'elem'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'info'

 L. 435        12  LOAD_FAST                'info'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 436        20  LOAD_GLOBAL              ElementInfo
               22  LOAD_FAST                'elem'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'info'

 L. 437        28  LOAD_FAST                'info'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _elem_info
               34  LOAD_FAST                'elem'
               36  STORE_SUBSCR     
             38_0  COME_FROM            18  '18'

 L. 438        38  LOAD_FAST                'info'
               40  LOAD_ATTR                _attr_info
               42  LOAD_METHOD              append

 L. 439        44  LOAD_CONST               None
               46  LOAD_FAST                'name'
               48  LOAD_CONST               None
               50  LOAD_CONST               None
               52  LOAD_FAST                'default'
               54  LOAD_CONST               0
               56  LOAD_FAST                'type'
               58  LOAD_FAST                'required'
               60  BUILD_LIST_8          8 

 L. 438        62  CALL_METHOD_1         1  ''
               64  POP_TOP          

Parse error at or near `<117>' instruction at offset 16

    def xml_decl_handler(self, version, encoding, standalone):
        self.document.version = version
        self.document.encoding = encoding
        if standalone >= 0:
            if standalone:
                self.document.standalone = True
            else:
                self.document.standalone = False


_ALLOWED_FILTER_RETURNS = (
 FILTER_ACCEPT, FILTER_REJECT, FILTER_SKIP)

class FilterVisibilityController(object):
    __doc__ = 'Wrapper around a DOMBuilderFilter which implements the checks\n    to make the whatToShow filter attribute work.'
    __slots__ = ('filter', )

    def __init__(self, filter):
        self.filter = filter

    def startContainer--- This code section failed: ---

 L. 466         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _nodetype_mask
                4  LOAD_FAST                'node'
                6  LOAD_ATTR                nodeType
                8  BINARY_SUBSCR    
               10  STORE_FAST               'mask'

 L. 467        12  LOAD_FAST                'self'
               14  LOAD_ATTR                filter
               16  LOAD_ATTR                whatToShow
               18  LOAD_FAST                'mask'
               20  BINARY_AND       
               22  POP_JUMP_IF_FALSE    76  'to 76'

 L. 468        24  LOAD_FAST                'self'
               26  LOAD_ATTR                filter
               28  LOAD_METHOD              startContainer
               30  LOAD_FAST                'node'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'val'

 L. 469        36  LOAD_FAST                'val'
               38  LOAD_GLOBAL              FILTER_INTERRUPT
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 470        44  LOAD_GLOBAL              ParseEscape
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 471        48  LOAD_FAST                'val'
               50  LOAD_GLOBAL              _ALLOWED_FILTER_RETURNS
               52  <118>                 1  ''
               54  POP_JUMP_IF_FALSE    72  'to 72'

 L. 472        56  LOAD_GLOBAL              ValueError

 L. 473        58  LOAD_STR                 'startContainer() returned illegal value: '
               60  LOAD_GLOBAL              repr
               62  LOAD_FAST                'val'
               64  CALL_FUNCTION_1       1  ''
               66  BINARY_ADD       

 L. 472        68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            54  '54'

 L. 474        72  LOAD_FAST                'val'
               74  RETURN_VALUE     
             76_0  COME_FROM            22  '22'

 L. 476        76  LOAD_GLOBAL              FILTER_ACCEPT
               78  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 52

    def acceptNode--- This code section failed: ---

 L. 479         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _nodetype_mask
                4  LOAD_FAST                'node'
                6  LOAD_ATTR                nodeType
                8  BINARY_SUBSCR    
               10  STORE_FAST               'mask'

 L. 480        12  LOAD_FAST                'self'
               14  LOAD_ATTR                filter
               16  LOAD_ATTR                whatToShow
               18  LOAD_FAST                'mask'
               20  BINARY_AND       
               22  POP_JUMP_IF_FALSE   124  'to 124'

 L. 481        24  LOAD_FAST                'self'
               26  LOAD_ATTR                filter
               28  LOAD_METHOD              acceptNode
               30  LOAD_FAST                'node'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'val'

 L. 482        36  LOAD_FAST                'val'
               38  LOAD_GLOBAL              FILTER_INTERRUPT
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 483        44  LOAD_GLOBAL              ParseEscape
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 484        48  LOAD_FAST                'val'
               50  LOAD_GLOBAL              FILTER_SKIP
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    96  'to 96'

 L. 486        56  LOAD_FAST                'node'
               58  LOAD_ATTR                parentNode
               60  STORE_FAST               'parent'

 L. 487        62  LOAD_FAST                'node'
               64  LOAD_ATTR                childNodes
               66  LOAD_CONST               None
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  GET_ITER         
               76  FOR_ITER             92  'to 92'
               78  STORE_FAST               'child'

 L. 488        80  LOAD_FAST                'parent'
               82  LOAD_METHOD              appendChild
               84  LOAD_FAST                'child'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  JUMP_BACK            76  'to 76'

 L. 490        92  LOAD_GLOBAL              FILTER_REJECT
               94  RETURN_VALUE     
             96_0  COME_FROM            54  '54'

 L. 491        96  LOAD_FAST                'val'
               98  LOAD_GLOBAL              _ALLOWED_FILTER_RETURNS
              100  <118>                 1  ''
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L. 492       104  LOAD_GLOBAL              ValueError

 L. 493       106  LOAD_STR                 'acceptNode() returned illegal value: '
              108  LOAD_GLOBAL              repr
              110  LOAD_FAST                'val'
              112  CALL_FUNCTION_1       1  ''
              114  BINARY_ADD       

 L. 492       116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           102  '102'

 L. 494       120  LOAD_FAST                'val'
              122  RETURN_VALUE     
            124_0  COME_FROM            22  '22'

 L. 496       124  LOAD_GLOBAL              FILTER_ACCEPT
              126  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 100

    _nodetype_mask = {Node.ELEMENT_NODE: NodeFilter.SHOW_ELEMENT, 
     Node.ATTRIBUTE_NODE: NodeFilter.SHOW_ATTRIBUTE, 
     Node.TEXT_NODE: NodeFilter.SHOW_TEXT, 
     Node.CDATA_SECTION_NODE: NodeFilter.SHOW_CDATA_SECTION, 
     Node.ENTITY_REFERENCE_NODE: NodeFilter.SHOW_ENTITY_REFERENCE, 
     Node.ENTITY_NODE: NodeFilter.SHOW_ENTITY, 
     Node.PROCESSING_INSTRUCTION_NODE: NodeFilter.SHOW_PROCESSING_INSTRUCTION, 
     Node.COMMENT_NODE: NodeFilter.SHOW_COMMENT, 
     Node.DOCUMENT_NODE: NodeFilter.SHOW_DOCUMENT, 
     Node.DOCUMENT_TYPE_NODE: NodeFilter.SHOW_DOCUMENT_TYPE, 
     Node.DOCUMENT_FRAGMENT_NODE: NodeFilter.SHOW_DOCUMENT_FRAGMENT, 
     Node.NOTATION_NODE: NodeFilter.SHOW_NOTATION}


class FilterCrutch(object):
    __slots__ = ('_builder', '_level', '_old_start', '_old_end')

    def __init__(self, builder):
        self._level = 0
        self._builder = builder
        parser = builder._parser
        self._old_start = parser.StartElementHandler
        self._old_end = parser.EndElementHandler
        parser.StartElementHandler = self.start_element_handler
        parser.EndElementHandler = self.end_element_handler


class Rejecter(FilterCrutch):
    __slots__ = ()

    def __init__(self, builder):
        FilterCrutch.__init__(self, builder)
        parser = builder._parser
        for name in ('ProcessingInstructionHandler', 'CommentHandler', 'CharacterDataHandler',
                     'StartCdataSectionHandler', 'EndCdataSectionHandler', 'ExternalEntityRefHandler'):
            setattr(parser, name, None)

    def start_element_handler(self, *args):
        self._level = self._level + 1

    def end_element_handler(self, *args):
        if self._level == 0:
            parser = self._builder._parser
            self._builder.install(parser)
            parser.StartElementHandler = self._old_start
            parser.EndElementHandler = self._old_end
        else:
            self._level = self._level - 1


class Skipper(FilterCrutch):
    __slots__ = ()

    def start_element_handler--- This code section failed: ---

 L. 558         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _builder
                4  LOAD_ATTR                curNode
                6  STORE_FAST               'node'

 L. 559         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _old_start
               12  LOAD_FAST                'args'
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  POP_TOP          

 L. 560        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _builder
               22  LOAD_ATTR                curNode
               24  LOAD_FAST                'node'
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 561        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _level
               34  LOAD_CONST               1
               36  BINARY_ADD       
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _level
             42_0  COME_FROM            28  '28'

Parse error at or near `<117>' instruction at offset 26

    def end_element_handler(self, *args):
        if self._level == 0:
            self._builder._parser.StartElementHandler = self._old_start
            self._builder._parser.EndElementHandler = self._old_end
            self._builder = None
        else:
            self._level = self._level - 1
            (self._old_end)(*args)


_FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID = 'http://xml.python.org/entities/fragment-builder/internal'
_FRAGMENT_BUILDER_TEMPLATE = '<!DOCTYPE wrapper\n  %%s [\n  <!ENTITY fragment-builder-internal\n    SYSTEM "%s">\n%%s\n]>\n<wrapper %%s\n>&fragment-builder-internal;</wrapper>' % _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID

class FragmentBuilder(ExpatBuilder):
    __doc__ = 'Builder which constructs document fragments given XML source\n    text and a context node.\n\n    The context node is expected to provide information about the\n    namespace declarations which are in scope at the start of the\n    fragment.\n    '

    def __init__(self, context, options=None):
        if context.nodeType == DOCUMENT_NODE:
            self.originalDocument = context
            self.context = context
        else:
            self.originalDocument = context.ownerDocument
            self.context = context
        ExpatBuilder.__init__(self, options)

    def reset(self):
        ExpatBuilder.reset(self)
        self.fragment = None

    def parseFile(self, file):
        """Parse a document fragment from a file object, returning the
        fragment node."""
        return self.parseString(file.read())

    def parseString--- This code section failed: ---

 L. 624         0  LOAD_FAST                'string'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _source

 L. 625         6  LOAD_FAST                'self'
                8  LOAD_METHOD              getParser
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'parser'

 L. 626        14  LOAD_FAST                'self'
               16  LOAD_ATTR                originalDocument
               18  LOAD_ATTR                doctype
               20  STORE_FAST               'doctype'

 L. 627        22  LOAD_STR                 ''
               24  STORE_FAST               'ident'

 L. 628        26  LOAD_FAST                'doctype'
               28  POP_JUMP_IF_FALSE    86  'to 86'

 L. 629        30  LOAD_FAST                'doctype'
               32  LOAD_ATTR                internalSubset
               34  JUMP_IF_TRUE_OR_POP    42  'to 42'
               36  LOAD_FAST                'self'
               38  LOAD_METHOD              _getDeclarations
               40  CALL_METHOD_0         0  ''
             42_0  COME_FROM            34  '34'
               42  STORE_FAST               'subset'

 L. 630        44  LOAD_FAST                'doctype'
               46  LOAD_ATTR                publicId
               48  POP_JUMP_IF_FALSE    68  'to 68'

 L. 631        50  LOAD_STR                 'PUBLIC "%s" "%s"'

 L. 632        52  LOAD_FAST                'doctype'
               54  LOAD_ATTR                publicId
               56  LOAD_FAST                'doctype'
               58  LOAD_ATTR                systemId
               60  BUILD_TUPLE_2         2 

 L. 631        62  BINARY_MODULO    
               64  STORE_FAST               'ident'
               66  JUMP_ABSOLUTE        90  'to 90'
             68_0  COME_FROM            48  '48'

 L. 633        68  LOAD_FAST                'doctype'
               70  LOAD_ATTR                systemId
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 634        74  LOAD_STR                 'SYSTEM "%s"'
               76  LOAD_FAST                'doctype'
               78  LOAD_ATTR                systemId
               80  BINARY_MODULO    
               82  STORE_FAST               'ident'
               84  JUMP_FORWARD         90  'to 90'
             86_0  COME_FROM            28  '28'

 L. 636        86  LOAD_STR                 ''
               88  STORE_FAST               'subset'
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            72  '72'

 L. 637        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _getNSattrs
               94  CALL_METHOD_0         0  ''
               96  STORE_FAST               'nsattrs'

 L. 638        98  LOAD_GLOBAL              _FRAGMENT_BUILDER_TEMPLATE
              100  LOAD_FAST                'ident'
              102  LOAD_FAST                'subset'
              104  LOAD_FAST                'nsattrs'
              106  BUILD_TUPLE_3         3 
              108  BINARY_MODULO    
              110  STORE_FAST               'document'

 L. 639       112  SETUP_FINALLY       130  'to 130'

 L. 640       114  LOAD_FAST                'parser'
              116  LOAD_METHOD              Parse
              118  LOAD_FAST                'document'
              120  LOAD_CONST               True
              122  CALL_METHOD_2         2  ''
              124  POP_TOP          
              126  POP_BLOCK        
              128  JUMP_FORWARD        152  'to 152'
            130_0  COME_FROM_FINALLY   112  '112'

 L. 641       130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 642       136  LOAD_FAST                'self'
              138  LOAD_METHOD              reset
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          

 L. 643       144  RAISE_VARARGS_0       0  'reraise'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
              150  <48>             
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           128  '128'

 L. 644       152  LOAD_FAST                'self'
              154  LOAD_ATTR                fragment
              156  STORE_FAST               'fragment'

 L. 645       158  LOAD_FAST                'self'
              160  LOAD_METHOD              reset
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L. 647       166  LOAD_FAST                'fragment'
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<48>' instruction at offset 150

    def _getDeclarations(self):
        """Re-create the internal subset from the DocumentType node.

        This is only needed if we don't already have the
        internalSubset as a string.
        """
        doctype = self.context.ownerDocument.doctype
        s = ''
        if doctype:
            for i in range(doctype.notations.length):
                notation = doctype.notations.item(i)
                if s:
                    s = s + '\n  '
                s = '%s<!NOTATION %s' % (s, notation.nodeName)
                if notation.publicId:
                    s = '%s PUBLIC "%s"\n             "%s">' % (
                     s, notation.publicId, notation.systemId)
                else:
                    s = '%s SYSTEM "%s">' % (s, notation.systemId)
            else:
                for i in range(doctype.entities.length):
                    entity = doctype.entities.item(i)
                    if s:
                        s = s + '\n  '
                    else:
                        s = '%s<!ENTITY %s' % (s, entity.nodeName)
                        if entity.publicId:
                            s = '%s PUBLIC "%s"\n             "%s"' % (
                             s, entity.publicId, entity.systemId)
                        else:
                            if entity.systemId:
                                s = '%s SYSTEM "%s"' % (s, entity.systemId)
                            else:
                                s = '%s "%s"' % (s, entity.firstChild.data)
                    if entity.notationName:
                        s = '%s NOTATION %s' % (s, entity.notationName)
                    s = s + '>'

        return s

    def _getNSattrs(self):
        return ''

    def external_entity_ref_handler--- This code section failed: ---

 L. 689         0  LOAD_FAST                'systemId'
                2  LOAD_GLOBAL              _FRAGMENT_BUILDER_INTERNAL_SYSTEM_ID
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE   122  'to 122'

 L. 692         8  LOAD_FAST                'self'
               10  LOAD_ATTR                document
               12  STORE_FAST               'old_document'

 L. 693        14  LOAD_FAST                'self'
               16  LOAD_ATTR                curNode
               18  STORE_FAST               'old_cur_node'

 L. 694        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _parser
               24  LOAD_METHOD              ExternalEntityParserCreate
               26  LOAD_FAST                'context'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'parser'

 L. 696        32  LOAD_FAST                'self'
               34  LOAD_ATTR                originalDocument
               36  LOAD_FAST                'self'
               38  STORE_ATTR               document

 L. 697        40  LOAD_FAST                'self'
               42  LOAD_ATTR                document
               44  LOAD_METHOD              createDocumentFragment
               46  CALL_METHOD_0         0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               fragment

 L. 698        52  LOAD_FAST                'self'
               54  LOAD_ATTR                fragment
               56  LOAD_FAST                'self'
               58  STORE_ATTR               curNode

 L. 699        60  SETUP_FINALLY        98  'to 98'

 L. 700        62  LOAD_FAST                'parser'
               64  LOAD_METHOD              Parse
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _source
               70  LOAD_CONST               True
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  POP_BLOCK        

 L. 702        78  LOAD_FAST                'old_cur_node'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               curNode

 L. 703        84  LOAD_FAST                'old_document'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               document

 L. 704        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _source
               96  JUMP_FORWARD        118  'to 118'
             98_0  COME_FROM_FINALLY    60  '60'

 L. 702        98  LOAD_FAST                'old_cur_node'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               curNode

 L. 703       104  LOAD_FAST                'old_document'
              106  LOAD_FAST                'self'
              108  STORE_ATTR               document

 L. 704       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _source
              116  <48>             
            118_0  COME_FROM            96  '96'

 L. 705       118  LOAD_CONST               -1
              120  RETURN_VALUE     
            122_0  COME_FROM             6  '6'

 L. 707       122  LOAD_GLOBAL              ExpatBuilder
              124  LOAD_METHOD              external_entity_ref_handler

 L. 708       126  LOAD_FAST                'self'
              128  LOAD_FAST                'context'
              130  LOAD_FAST                'base'
              132  LOAD_FAST                'systemId'
              134  LOAD_FAST                'publicId'

 L. 707       136  CALL_METHOD_5         5  ''
              138  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 78


class Namespaces:
    __doc__ = 'Mix-in class for builders; adds support for namespaces.'

    def _initNamespaces(self):
        self._ns_ordered_prefixes = []

    def createParser(self):
        """Create a new namespace-handling parser."""
        parser = expat.ParserCreate(namespace_separator=' ')
        parser.namespace_prefixes = True
        return parser

    def install(self, parser):
        """Insert the namespace-handlers onto the parser."""
        ExpatBuilder.install(self, parser)
        if self._options.namespace_declarations:
            parser.StartNamespaceDeclHandler = self.start_namespace_decl_handler

    def start_namespace_decl_handler(self, prefix, uri):
        """Push this namespace declaration on our storage."""
        self._ns_ordered_prefixes.append((prefix, uri))

    def start_element_handler--- This code section failed: ---

 L. 737         0  LOAD_STR                 ' '
                2  LOAD_FAST                'name'
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 738         8  LOAD_GLOBAL              _parse_ns_name
               10  LOAD_FAST                'self'
               12  LOAD_FAST                'name'
               14  CALL_FUNCTION_2       2  ''
               16  UNPACK_SEQUENCE_4     4 
               18  STORE_FAST               'uri'
               20  STORE_FAST               'localname'
               22  STORE_FAST               'prefix'
               24  STORE_FAST               'qname'
               26  JUMP_FORWARD         44  'to 44'
             28_0  COME_FROM             6  '6'

 L. 740        28  LOAD_GLOBAL              EMPTY_NAMESPACE
               30  STORE_FAST               'uri'

 L. 741        32  LOAD_FAST                'name'
               34  STORE_FAST               'qname'

 L. 742        36  LOAD_CONST               None
               38  STORE_FAST               'localname'

 L. 743        40  LOAD_GLOBAL              EMPTY_PREFIX
               42  STORE_FAST               'prefix'
             44_0  COME_FROM            26  '26'

 L. 744        44  LOAD_GLOBAL              minidom
               46  LOAD_METHOD              Element
               48  LOAD_FAST                'qname'
               50  LOAD_FAST                'uri'
               52  LOAD_FAST                'prefix'
               54  LOAD_FAST                'localname'
               56  CALL_METHOD_4         4  ''
               58  STORE_FAST               'node'

 L. 745        60  LOAD_FAST                'self'
               62  LOAD_ATTR                document
               64  LOAD_FAST                'node'
               66  STORE_ATTR               ownerDocument

 L. 746        68  LOAD_GLOBAL              _append_child
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                curNode
               74  LOAD_FAST                'node'
               76  CALL_FUNCTION_2       2  ''
               78  POP_TOP          

 L. 747        80  LOAD_FAST                'node'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               curNode

 L. 749        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _ns_ordered_prefixes
               90  POP_JUMP_IF_FALSE   192  'to 192'

 L. 750        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _ns_ordered_prefixes
               96  GET_ITER         
               98  FOR_ITER            180  'to 180'
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'prefix'
              104  STORE_FAST               'uri'

 L. 751       106  LOAD_FAST                'prefix'
              108  POP_JUMP_IF_FALSE   138  'to 138'

 L. 752       110  LOAD_GLOBAL              minidom
              112  LOAD_METHOD              Attr
              114  LOAD_GLOBAL              _intern
              116  LOAD_FAST                'self'
              118  LOAD_STR                 'xmlns:'
              120  LOAD_FAST                'prefix'
              122  BINARY_ADD       
              124  CALL_FUNCTION_2       2  ''

 L. 753       126  LOAD_GLOBAL              XMLNS_NAMESPACE
              128  LOAD_FAST                'prefix'
              130  LOAD_STR                 'xmlns'

 L. 752       132  CALL_METHOD_4         4  ''
              134  STORE_FAST               'a'
              136  JUMP_FORWARD        154  'to 154'
            138_0  COME_FROM           108  '108'

 L. 755       138  LOAD_GLOBAL              minidom
              140  LOAD_METHOD              Attr
              142  LOAD_STR                 'xmlns'
              144  LOAD_GLOBAL              XMLNS_NAMESPACE

 L. 756       146  LOAD_STR                 'xmlns'
              148  LOAD_GLOBAL              EMPTY_PREFIX

 L. 755       150  CALL_METHOD_4         4  ''
              152  STORE_FAST               'a'
            154_0  COME_FROM           136  '136'

 L. 757       154  LOAD_FAST                'uri'
              156  LOAD_FAST                'a'
              158  STORE_ATTR               value

 L. 758       160  LOAD_FAST                'self'
              162  LOAD_ATTR                document
              164  LOAD_FAST                'a'
              166  STORE_ATTR               ownerDocument

 L. 759       168  LOAD_GLOBAL              _set_attribute_node
              170  LOAD_FAST                'node'
              172  LOAD_FAST                'a'
              174  CALL_FUNCTION_2       2  ''
              176  POP_TOP          
              178  JUMP_BACK            98  'to 98'

 L. 760       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _ns_ordered_prefixes
              184  LOAD_CONST               None
              186  LOAD_CONST               None
              188  BUILD_SLICE_2         2 
              190  DELETE_SUBSCR    
            192_0  COME_FROM            90  '90'

 L. 762       192  LOAD_FAST                'attributes'
          194_196  POP_JUMP_IF_FALSE   382  'to 382'

 L. 763       198  LOAD_FAST                'node'
              200  LOAD_METHOD              _ensure_attributes
              202  CALL_METHOD_0         0  ''
              204  POP_TOP          

 L. 764       206  LOAD_FAST                'node'
              208  LOAD_ATTR                _attrs
              210  STORE_FAST               '_attrs'

 L. 765       212  LOAD_FAST                'node'
              214  LOAD_ATTR                _attrsNS
              216  STORE_FAST               '_attrsNS'

 L. 766       218  LOAD_GLOBAL              range
              220  LOAD_CONST               0
              222  LOAD_GLOBAL              len
              224  LOAD_FAST                'attributes'
              226  CALL_FUNCTION_1       1  ''
              228  LOAD_CONST               2
              230  CALL_FUNCTION_3       3  ''
              232  GET_ITER         
              234  FOR_ITER            382  'to 382'
              236  STORE_FAST               'i'

 L. 767       238  LOAD_FAST                'attributes'
              240  LOAD_FAST                'i'
              242  BINARY_SUBSCR    
              244  STORE_FAST               'aname'

 L. 768       246  LOAD_FAST                'attributes'
              248  LOAD_FAST                'i'
              250  LOAD_CONST               1
              252  BINARY_ADD       
              254  BINARY_SUBSCR    
              256  STORE_FAST               'value'

 L. 769       258  LOAD_STR                 ' '
              260  LOAD_FAST                'aname'
              262  <118>                 0  ''
          264_266  POP_JUMP_IF_FALSE   324  'to 324'

 L. 770       268  LOAD_GLOBAL              _parse_ns_name
              270  LOAD_FAST                'self'
              272  LOAD_FAST                'aname'
              274  CALL_FUNCTION_2       2  ''
              276  UNPACK_SEQUENCE_4     4 
              278  STORE_FAST               'uri'
              280  STORE_FAST               'localname'
              282  STORE_FAST               'prefix'
              284  STORE_FAST               'qname'

 L. 771       286  LOAD_GLOBAL              minidom
              288  LOAD_METHOD              Attr
              290  LOAD_FAST                'qname'
              292  LOAD_FAST                'uri'
              294  LOAD_FAST                'localname'
              296  LOAD_FAST                'prefix'
              298  CALL_METHOD_4         4  ''
              300  STORE_FAST               'a'

 L. 772       302  LOAD_FAST                'a'
              304  LOAD_FAST                '_attrs'
              306  LOAD_FAST                'qname'
              308  STORE_SUBSCR     

 L. 773       310  LOAD_FAST                'a'
              312  LOAD_FAST                '_attrsNS'
              314  LOAD_FAST                'uri'
              316  LOAD_FAST                'localname'
              318  BUILD_TUPLE_2         2 
              320  STORE_SUBSCR     
              322  JUMP_FORWARD        360  'to 360'
            324_0  COME_FROM           264  '264'

 L. 775       324  LOAD_GLOBAL              minidom
              326  LOAD_METHOD              Attr
              328  LOAD_FAST                'aname'
              330  LOAD_GLOBAL              EMPTY_NAMESPACE

 L. 776       332  LOAD_FAST                'aname'
              334  LOAD_GLOBAL              EMPTY_PREFIX

 L. 775       336  CALL_METHOD_4         4  ''
              338  STORE_FAST               'a'

 L. 777       340  LOAD_FAST                'a'
              342  LOAD_FAST                '_attrs'
              344  LOAD_FAST                'aname'
              346  STORE_SUBSCR     

 L. 778       348  LOAD_FAST                'a'
              350  LOAD_FAST                '_attrsNS'
              352  LOAD_GLOBAL              EMPTY_NAMESPACE
              354  LOAD_FAST                'aname'
              356  BUILD_TUPLE_2         2 
              358  STORE_SUBSCR     
            360_0  COME_FROM           322  '322'

 L. 779       360  LOAD_FAST                'self'
              362  LOAD_ATTR                document
              364  LOAD_FAST                'a'
              366  STORE_ATTR               ownerDocument

 L. 780       368  LOAD_FAST                'value'
              370  LOAD_FAST                'a'
              372  STORE_ATTR               value

 L. 781       374  LOAD_FAST                'node'
              376  LOAD_FAST                'a'
              378  STORE_ATTR               ownerElement
              380  JUMP_BACK           234  'to 234'
            382_0  COME_FROM           194  '194'

Parse error at or near `None' instruction at offset -1

    def end_element_handler--- This code section failed: ---

 L. 790         0  LOAD_FAST                'self'
                2  LOAD_ATTR                curNode
                4  STORE_FAST               'curNode'

 L. 791         6  LOAD_STR                 ' '
                8  LOAD_FAST                'name'
               10  <118>                 0  ''
               12  POP_JUMP_IF_FALSE    72  'to 72'

 L. 792        14  LOAD_GLOBAL              _parse_ns_name
               16  LOAD_FAST                'self'
               18  LOAD_FAST                'name'
               20  CALL_FUNCTION_2       2  ''
               22  UNPACK_SEQUENCE_4     4 
               24  STORE_FAST               'uri'
               26  STORE_FAST               'localname'
               28  STORE_FAST               'prefix'
               30  STORE_FAST               'qname'

 L. 793        32  LOAD_FAST                'curNode'
               34  LOAD_ATTR                namespaceURI
               36  LOAD_FAST                'uri'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L. 794        42  LOAD_FAST                'curNode'
               44  LOAD_ATTR                localName
               46  LOAD_FAST                'localname'
               48  COMPARE_OP               ==

 L. 793        50  POP_JUMP_IF_FALSE    62  'to 62'

 L. 795        52  LOAD_FAST                'curNode'
               54  LOAD_ATTR                prefix
               56  LOAD_FAST                'prefix'
               58  COMPARE_OP               ==

 L. 793        60  POP_JUMP_IF_TRUE    108  'to 108'
             62_0  COME_FROM            50  '50'
             62_1  COME_FROM            40  '40'
               62  <74>             

 L. 796        64  LOAD_STR                 'element stack messed up! (namespace)'

 L. 793        66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  JUMP_FORWARD        108  'to 108'
             72_0  COME_FROM            12  '12'

 L. 798        72  LOAD_FAST                'curNode'
               74  LOAD_ATTR                nodeName
               76  LOAD_FAST                'name'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_TRUE     90  'to 90'
               82  <74>             

 L. 799        84  LOAD_STR                 'element stack messed up - bad nodeName'

 L. 798        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'

 L. 800        90  LOAD_FAST                'curNode'
               92  LOAD_ATTR                namespaceURI
               94  LOAD_GLOBAL              EMPTY_NAMESPACE
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  <74>             

 L. 801       102  LOAD_STR                 'element stack messed up - bad namespaceURI'

 L. 800       104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            98  '98'
            108_1  COME_FROM            70  '70'
            108_2  COME_FROM            60  '60'

 L. 802       108  LOAD_FAST                'curNode'
              110  LOAD_ATTR                parentNode
              112  LOAD_FAST                'self'
              114  STORE_ATTR               curNode

 L. 803       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _finish_end_element
              120  LOAD_FAST                'curNode'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

Parse error at or near `<118>' instruction at offset 10


class ExpatBuilderNS(Namespaces, ExpatBuilder):
    __doc__ = 'Document builder that supports namespaces.'

    def reset(self):
        ExpatBuilder.reset(self)
        self._initNamespaces()


class FragmentBuilderNS(Namespaces, FragmentBuilder):
    __doc__ = 'Fragment builder that supports namespaces.'

    def reset(self):
        FragmentBuilder.reset(self)
        self._initNamespaces()

    def _getNSattrs--- This code section failed: ---

 L. 829         0  LOAD_STR                 ''
                2  STORE_FAST               'attrs'

 L. 830         4  LOAD_FAST                'self'
                6  LOAD_ATTR                context
                8  STORE_FAST               'context'

 L. 831        10  BUILD_LIST_0          0 
               12  STORE_FAST               'L'

 L. 832        14  LOAD_FAST                'context'
               16  POP_JUMP_IF_FALSE   126  'to 126'

 L. 833        18  LOAD_GLOBAL              hasattr
               20  LOAD_FAST                'context'
               22  LOAD_STR                 '_ns_prefix_uri'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE   118  'to 118'

 L. 834        28  LOAD_FAST                'context'
               30  LOAD_ATTR                _ns_prefix_uri
               32  LOAD_METHOD              items
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
               38  FOR_ITER            118  'to 118'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'prefix'
               44  STORE_FAST               'uri'

 L. 836        46  LOAD_FAST                'prefix'
               48  LOAD_FAST                'L'
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L. 837        54  JUMP_BACK            38  'to 38'
             56_0  COME_FROM            52  '52'

 L. 838        56  LOAD_FAST                'L'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'prefix'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 839        66  LOAD_FAST                'prefix'
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L. 840        70  LOAD_STR                 'xmlns:'
               72  LOAD_FAST                'prefix'
               74  BINARY_ADD       
               76  STORE_FAST               'declname'
               78  JUMP_FORWARD         84  'to 84'
             80_0  COME_FROM            68  '68'

 L. 842        80  LOAD_STR                 'xmlns'
               82  STORE_FAST               'declname'
             84_0  COME_FROM            78  '78'

 L. 843        84  LOAD_FAST                'attrs'
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 844        88  LOAD_STR                 "%s\n    %s='%s'"
               90  LOAD_FAST                'attrs'
               92  LOAD_FAST                'declname'
               94  LOAD_FAST                'uri'
               96  BUILD_TUPLE_3         3 
               98  BINARY_MODULO    
              100  STORE_FAST               'attrs'
              102  JUMP_BACK            38  'to 38'
            104_0  COME_FROM            86  '86'

 L. 846       104  LOAD_STR                 " %s='%s'"
              106  LOAD_FAST                'declname'
              108  LOAD_FAST                'uri'
              110  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              114  STORE_FAST               'attrs'
              116  JUMP_BACK            38  'to 38'
            118_0  COME_FROM            26  '26'

 L. 847       118  LOAD_FAST                'context'
              120  LOAD_ATTR                parentNode
              122  STORE_FAST               'context'
              124  JUMP_BACK            14  'to 14'
            126_0  COME_FROM            16  '16'

 L. 848       126  LOAD_FAST                'attrs'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 50


class ParseEscape(Exception):
    __doc__ = 'Exception raised to short-circuit parsing in InternalSubsetExtractor.'


class InternalSubsetExtractor(ExpatBuilder):
    __doc__ = 'XML processor which can rip out the internal document type subset.'
    subset = None

    def getSubset(self):
        """Return the internal subset as a string."""
        return self.subset

    def parseFile--- This code section failed: ---

 L. 865         0  SETUP_FINALLY        18  'to 18'

 L. 866         2  LOAD_GLOBAL              ExpatBuilder
                4  LOAD_METHOD              parseFile
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'file'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         36  'to 36'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 867        18  DUP_TOP          
               20  LOAD_GLOBAL              ParseEscape
               22  <121>                34  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 868        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'
             36_1  COME_FROM            16  '16'

Parse error at or near `<121>' instruction at offset 22

    def parseString--- This code section failed: ---

 L. 871         0  SETUP_FINALLY        18  'to 18'

 L. 872         2  LOAD_GLOBAL              ExpatBuilder
                4  LOAD_METHOD              parseString
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'string'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         36  'to 36'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 873        18  DUP_TOP          
               20  LOAD_GLOBAL              ParseEscape
               22  <121>                34  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 874        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'
             36_1  COME_FROM            16  '16'

Parse error at or near `<121>' instruction at offset 22

    def install(self, parser):
        parser.StartDoctypeDeclHandler = self.start_doctype_decl_handler
        parser.StartElementHandler = self.start_element_handler

    def start_doctype_decl_handler(self, name, publicId, systemId, has_internal_subset):
        if has_internal_subset:
            parser = self.getParser()
            self.subset = []
            parser.DefaultHandler = self.subset.append
            parser.EndDoctypeDeclHandler = self.end_doctype_decl_handler
        else:
            raise ParseEscape()

    def end_doctype_decl_handler(self):
        s = ''.join(self.subset).replace('\r\n', '\n').replace('\r', '\n')
        self.subset = s
        raise ParseEscape()

    def start_element_handler(self, name, attrs):
        raise ParseEscape()


def parse--- This code section failed: ---

 L. 904         0  LOAD_FAST                'namespaces'
                2  POP_JUMP_IF_FALSE    12  'to 12'

 L. 905         4  LOAD_GLOBAL              ExpatBuilderNS
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'builder'
               10  JUMP_FORWARD         18  'to 18'
             12_0  COME_FROM             2  '2'

 L. 907        12  LOAD_GLOBAL              ExpatBuilder
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'builder'
             18_0  COME_FROM            10  '10'

 L. 909        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'file'
               22  LOAD_GLOBAL              str
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    82  'to 82'

 L. 910        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'file'
               32  LOAD_STR                 'rb'
               34  CALL_FUNCTION_2       2  ''
               36  SETUP_WITH           64  'to 64'
               38  STORE_FAST               'fp'

 L. 911        40  LOAD_FAST                'builder'
               42  LOAD_METHOD              parseFile
               44  LOAD_FAST                'fp'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'result'
               50  POP_BLOCK        
               52  LOAD_CONST               None
               54  DUP_TOP          
               56  DUP_TOP          
               58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          
               62  JUMP_ABSOLUTE        92  'to 92'
             64_0  COME_FROM_WITH       36  '36'
               64  <49>             
               66  POP_JUMP_IF_TRUE     70  'to 70'
               68  <48>             
             70_0  COME_FROM            66  '66'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          
               76  POP_EXCEPT       
               78  POP_TOP          
               80  JUMP_FORWARD         92  'to 92'
             82_0  COME_FROM            26  '26'

 L. 913        82  LOAD_FAST                'builder'
               84  LOAD_METHOD              parseFile
               86  LOAD_FAST                'file'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'result'
             92_0  COME_FROM            80  '80'

 L. 914        92  LOAD_FAST                'result'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 54


def parseString(string, namespaces=True):
    """Parse a document from a string, returning the resulting
    Document node.
    """
    if namespaces:
        builder = ExpatBuilderNS()
    else:
        builder = ExpatBuilder()
    return builder.parseString(string)


def parseFragment--- This code section failed: ---

 L. 935         0  LOAD_FAST                'namespaces'
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L. 936         4  LOAD_GLOBAL              FragmentBuilderNS
                6  LOAD_FAST                'context'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'builder'
               12  JUMP_FORWARD         22  'to 22'
             14_0  COME_FROM             2  '2'

 L. 938        14  LOAD_GLOBAL              FragmentBuilder
               16  LOAD_FAST                'context'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'builder'
             22_0  COME_FROM            12  '12'

 L. 940        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'file'
               26  LOAD_GLOBAL              str
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    86  'to 86'

 L. 941        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'file'
               36  LOAD_STR                 'rb'
               38  CALL_FUNCTION_2       2  ''
               40  SETUP_WITH           68  'to 68'
               42  STORE_FAST               'fp'

 L. 942        44  LOAD_FAST                'builder'
               46  LOAD_METHOD              parseFile
               48  LOAD_FAST                'fp'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'result'
               54  POP_BLOCK        
               56  LOAD_CONST               None
               58  DUP_TOP          
               60  DUP_TOP          
               62  CALL_FUNCTION_3       3  ''
               64  POP_TOP          
               66  JUMP_ABSOLUTE        96  'to 96'
             68_0  COME_FROM_WITH       40  '40'
               68  <49>             
               70  POP_JUMP_IF_TRUE     74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          
               80  POP_EXCEPT       
               82  POP_TOP          
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM            30  '30'

 L. 944        86  LOAD_FAST                'builder'
               88  LOAD_METHOD              parseFile
               90  LOAD_FAST                'file'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'result'
             96_0  COME_FROM            84  '84'

 L. 945        96  LOAD_FAST                'result'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 58


def parseFragmentString(string, context, namespaces=True):
    """Parse a fragment of a document from a string, given the context
    from which it was originally extracted.  context should be the
    parent of the node(s) which are in the fragment.
    """
    if namespaces:
        builder = FragmentBuilderNS(context)
    else:
        builder = FragmentBuilder(context)
    return builder.parseString(string)


def makeBuilder(options):
    """Create a builder based on an Options object."""
    if options.namespaces:
        return ExpatBuilderNS(options)
    return ExpatBuilder(options)