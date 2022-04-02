# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\dom\xmlbuilder.py
"""Implementation of the DOM Level 3 'LS-Load' feature."""
import copy, warnings, xml.dom
import xml.dom.NodeFilter as NodeFilter
__all__ = [
 'DOMBuilder', 'DOMEntityResolver', 'DOMInputSource']

class Options:
    __doc__ = 'Features object that has variables set for each DOMBuilder feature.\n\n    The DOMBuilder class uses an instance of this class to pass settings to\n    the ExpatBuilder class.\n    '
    namespaces = 1
    namespace_declarations = True
    validation = False
    external_parameter_entities = True
    external_general_entities = True
    external_dtd_subset = True
    validate_if_schema = False
    validate = False
    datatype_normalization = False
    create_entity_ref_nodes = True
    entities = True
    whitespace_in_element_content = True
    cdata_sections = True
    comments = True
    charset_overrides_xml_encoding = True
    infoset = False
    supported_mediatypes_only = False
    errorHandler = None
    filter = None


class DOMBuilder:
    entityResolver = None
    errorHandler = None
    filter = None
    ACTION_REPLACE = 1
    ACTION_APPEND_AS_CHILDREN = 2
    ACTION_INSERT_AFTER = 3
    ACTION_INSERT_BEFORE = 4
    _legal_actions = (
     ACTION_REPLACE, ACTION_APPEND_AS_CHILDREN,
     ACTION_INSERT_AFTER, ACTION_INSERT_BEFORE)

    def __init__(self):
        self._options = Options()

    def _get_entityResolver(self):
        return self.entityResolver

    def _set_entityResolver(self, entityResolver):
        self.entityResolver = entityResolver

    def _get_errorHandler(self):
        return self.errorHandler

    def _set_errorHandler(self, errorHandler):
        self.errorHandler = errorHandler

    def _get_filter(self):
        return self.filter

    def _set_filter(self, filter):
        self.filter = filter

    def setFeature(self, name, state):
        if self.supportsFeature(name):
            state = state and 1 or 0
            try:
                settings = self._settings[(_name_xform(name), state)]
            except KeyError:
                raise xml.dom.NotSupportedErr('unsupported feature: %r' % (name,)) from None
            else:
                for name, value in settings:
                    setattr(self._options, name, value)

        else:
            raise xml.dom.NotFoundErr('unknown feature: ' + repr(name))

    def supportsFeature(self, name):
        return hasattr(self._options, _name_xform(name))

    def canSetFeature(self, name, state):
        key = (
         _name_xform(name), state and 1 or 0)
        return key in self._settings

    _settings = {('namespace_declarations', 0):[
      ('namespace_declarations', 0)], 
     ('namespace_declarations', 1):[
      ('namespace_declarations', 1)], 
     ('validation', 0):[
      ('validation', 0)], 
     ('external_general_entities', 0):[
      ('external_general_entities', 0)], 
     ('external_general_entities', 1):[
      ('external_general_entities', 1)], 
     ('external_parameter_entities', 0):[
      ('external_parameter_entities', 0)], 
     ('external_parameter_entities', 1):[
      ('external_parameter_entities', 1)], 
     ('validate_if_schema', 0):[
      ('validate_if_schema', 0)], 
     ('create_entity_ref_nodes', 0):[
      ('create_entity_ref_nodes', 0)], 
     ('create_entity_ref_nodes', 1):[
      ('create_entity_ref_nodes', 1)], 
     ('entities', 0):[
      ('create_entity_ref_nodes', 0),
      ('entities', 0)], 
     ('entities', 1):[
      ('entities', 1)], 
     ('whitespace_in_element_content', 0):[
      ('whitespace_in_element_content', 0)], 
     ('whitespace_in_element_content', 1):[
      ('whitespace_in_element_content', 1)], 
     ('cdata_sections', 0):[
      ('cdata_sections', 0)], 
     ('cdata_sections', 1):[
      ('cdata_sections', 1)], 
     ('comments', 0):[
      ('comments', 0)], 
     ('comments', 1):[
      ('comments', 1)], 
     ('charset_overrides_xml_encoding', 0):[
      ('charset_overrides_xml_encoding', 0)], 
     ('charset_overrides_xml_encoding', 1):[
      ('charset_overrides_xml_encoding', 1)], 
     ('infoset', 0):[],  ('infoset', 1):[
      ('namespace_declarations', 0),
      ('validate_if_schema', 0),
      ('create_entity_ref_nodes', 0),
      ('entities', 0),
      ('cdata_sections', 0),
      ('datatype_normalization', 1),
      ('whitespace_in_element_content', 1),
      ('comments', 1),
      ('charset_overrides_xml_encoding', 1)], 
     ('supported_mediatypes_only', 0):[
      ('supported_mediatypes_only', 0)], 
     ('namespaces', 0):[
      ('namespaces', 0)], 
     ('namespaces', 1):[
      ('namespaces', 1)]}

    def getFeature--- This code section failed: ---

 L. 164         0  LOAD_GLOBAL              _name_xform
                2  LOAD_FAST                'name'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'xname'

 L. 165         8  SETUP_FINALLY        24  'to 24'

 L. 166        10  LOAD_GLOBAL              getattr
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _options
               16  LOAD_FAST                'xname'
               18  CALL_FUNCTION_2       2  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     8  '8'

 L. 167        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE   136  'to 136'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 168        38  LOAD_FAST                'name'
               40  LOAD_STR                 'infoset'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   112  'to 112'

 L. 169        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _options
               50  STORE_FAST               'options'

 L. 170        52  LOAD_FAST                'options'
               54  LOAD_ATTR                datatype_normalization
               56  JUMP_IF_FALSE_OR_POP   106  'to 106'

 L. 171        58  LOAD_FAST                'options'
               60  LOAD_ATTR                whitespace_in_element_content

 L. 170        62  JUMP_IF_FALSE_OR_POP   106  'to 106'

 L. 172        64  LOAD_FAST                'options'
               66  LOAD_ATTR                comments

 L. 170        68  JUMP_IF_FALSE_OR_POP   106  'to 106'

 L. 173        70  LOAD_FAST                'options'
               72  LOAD_ATTR                charset_overrides_xml_encoding

 L. 170        74  JUMP_IF_FALSE_OR_POP   106  'to 106'

 L. 174        76  LOAD_FAST                'options'
               78  LOAD_ATTR                namespace_declarations
               80  JUMP_IF_TRUE_OR_POP   104  'to 104'

 L. 175        82  LOAD_FAST                'options'
               84  LOAD_ATTR                validate_if_schema

 L. 174        86  JUMP_IF_TRUE_OR_POP   104  'to 104'

 L. 176        88  LOAD_FAST                'options'
               90  LOAD_ATTR                create_entity_ref_nodes

 L. 174        92  JUMP_IF_TRUE_OR_POP   104  'to 104'

 L. 177        94  LOAD_FAST                'options'
               96  LOAD_ATTR                entities

 L. 174        98  JUMP_IF_TRUE_OR_POP   104  'to 104'

 L. 178       100  LOAD_FAST                'options'
              102  LOAD_ATTR                cdata_sections
            104_0  COME_FROM            98  '98'
            104_1  COME_FROM            92  '92'
            104_2  COME_FROM            86  '86'
            104_3  COME_FROM            80  '80'

 L. 174       104  UNARY_NOT        
            106_0  COME_FROM            74  '74'
            106_1  COME_FROM            68  '68'
            106_2  COME_FROM            62  '62'
            106_3  COME_FROM            56  '56'

 L. 170       106  ROT_FOUR         
              108  POP_EXCEPT       
              110  RETURN_VALUE     
            112_0  COME_FROM            44  '44'

 L. 179       112  LOAD_GLOBAL              xml
              114  LOAD_ATTR                dom
              116  LOAD_METHOD              NotFoundErr
              118  LOAD_STR                 'feature %s not known'
              120  LOAD_GLOBAL              repr
              122  LOAD_FAST                'name'
              124  CALL_FUNCTION_1       1  ''
              126  BINARY_MODULO    
              128  CALL_METHOD_1         1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM            30  '30'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'

Parse error at or near `POP_TOP' instruction at offset 34

    def parseURI(self, uri):
        if self.entityResolver:
            input = self.entityResolver.resolveEntity(None, uri)
        else:
            input = DOMEntityResolver().resolveEntity(None, uri)
        return self.parse(input)

    def parse(self, input):
        options = copy.copy(self._options)
        options.filter = self.filter
        options.errorHandler = self.errorHandler
        fp = input.byteStream
        if fp is None:
            if options.systemId:
                import urllib.request
                fp = urllib.request.urlopen(input.systemId)
        return self._parse_bytestream(fp, options)

    def parseWithContext(self, input, cnode, action):
        if action not in self._legal_actions:
            raise ValueError('not a legal action')
        raise NotImplementedError("Haven't written this yet...")

    def _parse_bytestream(self, stream, options):
        import xml.dom.expatbuilder
        builder = xml.dom.expatbuilder.makeBuilder(options)
        return builder.parseFile(stream)


def _name_xform(name):
    return name.lower().replace('-', '_')


class DOMEntityResolver(object):
    __slots__ = ('_opener', )

    def resolveEntity(self, publicId, systemId):
        assert systemId is not None
        source = DOMInputSource()
        source.publicId = publicId
        source.systemId = systemId
        source.byteStream = self._get_opener().open(systemId)
        source.encoding = self._guess_media_encoding(source)
        import posixpath, urllib.parse
        parts = urllib.parse.urlparse(systemId)
        scheme, netloc, path, params, query, fragment = parts
        if path:
            if not path.endswith('/'):
                path = posixpath.dirname(path) + '/'
                parts = (scheme, netloc, path, params, query, fragment)
                source.baseURI = urllib.parse.urlunparse(parts)
        return source

    def _get_opener--- This code section failed: ---

 L. 239         0  SETUP_FINALLY        10  'to 10'

 L. 240         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _opener
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L. 241        10  DUP_TOP          
               12  LOAD_GLOBAL              AttributeError
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    44  'to 44'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 242        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _create_opener
               28  CALL_METHOD_0         0  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _opener

 L. 243        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _opener
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            16  '16'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 20

    def _create_opener(self):
        import urllib.request
        return urllib.request.build_opener()

    def _guess_media_encoding(self, source):
        info = source.byteStream.info()
        if 'Content-Type' in info:
            for param in info.getplist():
                if param.startswith('charset='):
                    return param.split('=', 1)[1].lower()


class DOMInputSource(object):
    __slots__ = ('byteStream', 'characterStream', 'stringData', 'encoding', 'publicId',
                 'systemId', 'baseURI')

    def __init__(self):
        self.byteStream = None
        self.characterStream = None
        self.stringData = None
        self.encoding = None
        self.publicId = None
        self.systemId = None
        self.baseURI = None

    def _get_byteStream(self):
        return self.byteStream

    def _set_byteStream(self, byteStream):
        self.byteStream = byteStream

    def _get_characterStream(self):
        return self.characterStream

    def _set_characterStream(self, characterStream):
        self.characterStream = characterStream

    def _get_stringData(self):
        return self.stringData

    def _set_stringData(self, data):
        self.stringData = data

    def _get_encoding(self):
        return self.encoding

    def _set_encoding(self, encoding):
        self.encoding = encoding

    def _get_publicId(self):
        return self.publicId

    def _set_publicId(self, publicId):
        self.publicId = publicId

    def _get_systemId(self):
        return self.systemId

    def _set_systemId(self, systemId):
        self.systemId = systemId

    def _get_baseURI(self):
        return self.baseURI

    def _set_baseURI(self, uri):
        self.baseURI = uri


class DOMBuilderFilter:
    __doc__ = 'Element filter which can be used to tailor construction of\n    a DOM instance.\n    '
    FILTER_ACCEPT = 1
    FILTER_REJECT = 2
    FILTER_SKIP = 3
    FILTER_INTERRUPT = 4
    whatToShow = NodeFilter.SHOW_ALL

    def _get_whatToShow(self):
        return self.whatToShow

    def acceptNode(self, element):
        return self.FILTER_ACCEPT

    def startContainer(self, element):
        return self.FILTER_ACCEPT


del NodeFilter

class DocumentLS:
    __doc__ = 'Mixin to create documents that conform to the load/save spec.'
    async_ = False

    def _get_async(self):
        return False

    def _set_async(self, flag):
        if flag:
            raise xml.dom.NotSupportedErr('asynchronous document loading is not supported')

    def abort(self):
        raise NotImplementedError("haven't figured out what this means yet")

    def load(self, uri):
        raise NotImplementedError("haven't written this yet")

    def loadXML(self, source):
        raise NotImplementedError("haven't written this yet")

    def saveXML(self, snode):
        if snode is None:
            snode = self
        else:
            if snode.ownerDocument is not self:
                raise xml.dom.WrongDocumentErr()
        return snode.toxml()


class DOMImplementationLS:
    MODE_SYNCHRONOUS = 1
    MODE_ASYNCHRONOUS = 2

    def createDOMBuilder(self, mode, schemaType):
        if schemaType is not None:
            raise xml.dom.NotSupportedErr('schemaType not yet supported')
        if mode == self.MODE_SYNCHRONOUS:
            return DOMBuilder()
        if mode == self.MODE_ASYNCHRONOUS:
            raise xml.dom.NotSupportedErr('asynchronous builders are not supported')
        raise ValueError('unknown value for mode')

    def createDOMWriter(self):
        raise NotImplementedError("the writer interface hasn't been written yet!")

    def createDOMInputSource(self):
        return DOMInputSource()