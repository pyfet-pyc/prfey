# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\sax\expatreader.py
"""
SAX driver for the pyexpat C module.  This driver works with
pyexpat.__version__ == '2.22'.
"""
version = '0.20'
from xml.sax._exceptions import *
from xml.sax.handler import feature_validation, feature_namespaces
from xml.sax.handler import feature_namespace_prefixes
from xml.sax.handler import feature_external_ges, feature_external_pes
from xml.sax.handler import feature_string_interning
from xml.sax.handler import property_xml_string, property_interning_dict
import sys
if sys.platform[:4] == 'java':
    raise SAXReaderNotAvailable('expat not available in Java', None)
del sys
try:
    from xml.parsers import expat
except ImportError:
    raise SAXReaderNotAvailable('expat not supported', None)
else:
    if not hasattr(expat, 'ParserCreate'):
        raise SAXReaderNotAvailable('expat not supported', None)
    else:
        from xml.sax import xmlreader, saxutils, handler
        AttributesImpl = xmlreader.AttributesImpl
        AttributesNSImpl = xmlreader.AttributesNSImpl
        try:
            import _weakref
        except ImportError:

            def _mkproxy(o):
                return o


        else:
            import weakref
            _mkproxy = weakref.proxy
            del weakref
            del _weakref

    class _ClosedParser:
        pass


    class ExpatLocator(xmlreader.Locator):
        __doc__ = 'Locator for use with the ExpatParser class.\n\n    This uses a weak reference to the parser object to avoid creating\n    a circular reference between the parser and the content handler.\n    '

        def __init__(self, parser):
            self._ref = _mkproxy(parser)

        def getColumnNumber(self):
            parser = self._ref
            if parser._parser is None:
                return
            return parser._parser.ErrorColumnNumber

        def getLineNumber(self):
            parser = self._ref
            if parser._parser is None:
                return 1
            return parser._parser.ErrorLineNumber

        def getPublicId(self):
            parser = self._ref
            if parser is None:
                return
            return parser._source.getPublicId()

        def getSystemId(self):
            parser = self._ref
            if parser is None:
                return
            return parser._source.getSystemId()


    class ExpatParser(xmlreader.IncrementalParser, xmlreader.Locator):
        __doc__ = 'SAX driver for the pyexpat C module.'

        def __init__(self, namespaceHandling=0, bufsize=65516):
            xmlreader.IncrementalParser.__init__(self, bufsize)
            self._source = xmlreader.InputSource()
            self._parser = None
            self._namespaces = namespaceHandling
            self._lex_handler_prop = None
            self._parsing = 0
            self._entity_stack = []
            self._external_ges = 0
            self._interning = None

        def parse(self, source):
            """Parse an XML document from a URL or an InputSource."""
            source = saxutils.prepare_input_source(source)
            self._source = source
            try:
                self.reset()
                self._cont_handler.setDocumentLocator(ExpatLocator(self))
                xmlreader.IncrementalParser.parse(self, source)
            except:
                self._close_source()
                raise

        def prepareParser(self, source):
            if source.getSystemId() is not None:
                self._parser.SetBase(source.getSystemId())

        def setContentHandler(self, handler):
            xmlreader.IncrementalParser.setContentHandler(self, handler)
            if self._parsing:
                self._reset_cont_handler()

        def getFeature(self, name):
            if name == feature_namespaces:
                return self._namespaces
            if name == feature_string_interning:
                return self._interning is not None
            if name in (feature_validation, feature_external_pes,
             feature_namespace_prefixes):
                return 0
            if name == feature_external_ges:
                return self._external_ges
            raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

        def setFeature(self, name, state):
            if self._parsing:
                raise SAXNotSupportedException('Cannot set features while parsing')
            elif name == feature_namespaces:
                self._namespaces = state
            else:
                if name == feature_external_ges:
                    self._external_ges = state
                else:
                    if name == feature_string_interning:
                        if state:
                            if self._interning is None:
                                self._interning = {}
                        else:
                            self._interning = None
                    else:
                        if name == feature_validation:
                            if state:
                                raise SAXNotSupportedException('expat does not support validation')
                        elif name == feature_external_pes:
                            if state:
                                raise SAXNotSupportedException('expat does not read external parameter entities')
                        elif name == feature_namespace_prefixes:
                            if state:
                                raise SAXNotSupportedException('expat does not report namespace prefixes')
                        else:
                            raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

        def getProperty(self, name):
            if name == handler.property_lexical_handler:
                return self._lex_handler_prop
                if name == property_interning_dict:
                    return self._interning
                if name == property_xml_string:
                    if self._parser:
                        if hasattr(self._parser, 'GetInputContext'):
                            return self._parser.GetInputContext()
                        raise SAXNotRecognizedException('This version of expat does not support getting the XML string')
            else:
                raise SAXNotSupportedException('XML string cannot be returned when not parsing')
            raise SAXNotRecognizedException("Property '%s' not recognized" % name)

        def setProperty(self, name, value):
            if name == handler.property_lexical_handler:
                self._lex_handler_prop = value
                if self._parsing:
                    self._reset_lex_handler_prop()
            elif name == property_interning_dict:
                self._interning = value
            else:
                if name == property_xml_string:
                    raise SAXNotSupportedException("Property '%s' cannot be set" % name)
                else:
                    raise SAXNotRecognizedException("Property '%s' not recognized" % name)

        def feed(self, data, isFinal=0):
            if not self._parsing:
                self.reset()
                self._parsing = 1
                self._cont_handler.startDocument()
            try:
                self._parser.Parse(data, isFinal)
            except expat.error as e:
                try:
                    exc = SAXParseException(expat.ErrorString(e.code), e, self)
                    self._err_handler.fatalError(exc)
                finally:
                    e = None
                    del e

        def _close_source(self):
            source = self._source
            try:
                file = source.getCharacterStream()
                if file is not None:
                    file.close()
            finally:
                file = source.getByteStream()
                if file is not None:
                    file.close()

        def close(self):
            if self._entity_stack or self._parser is None or isinstance(self._parser, _ClosedParser):
                return
            try:
                self.feed('', isFinal=1)
                self._cont_handler.endDocument()
                self._parsing = 0
                self._parser = None
            finally:
                self._parsing = 0
                if self._parser is not None:
                    parser = _ClosedParser()
                    parser.ErrorColumnNumber = self._parser.ErrorColumnNumber
                    parser.ErrorLineNumber = self._parser.ErrorLineNumber
                    self._parser = parser
                self._close_source()

        def _reset_cont_handler(self):
            self._parser.ProcessingInstructionHandler = self._cont_handler.processingInstruction
            self._parser.CharacterDataHandler = self._cont_handler.characters

        def _reset_lex_handler_prop(self):
            lex = self._lex_handler_prop
            parser = self._parser
            if lex is None:
                parser.CommentHandler = None
                parser.StartCdataSectionHandler = None
                parser.EndCdataSectionHandler = None
                parser.StartDoctypeDeclHandler = None
                parser.EndDoctypeDeclHandler = None
            else:
                parser.CommentHandler = lex.comment
                parser.StartCdataSectionHandler = lex.startCDATA
                parser.EndCdataSectionHandler = lex.endCDATA
                parser.StartDoctypeDeclHandler = self.start_doctype_decl
                parser.EndDoctypeDeclHandler = lex.endDTD

        def reset(self):
            if self._namespaces:
                self._parser = expat.ParserCreate((self._source.getEncoding()), ' ', intern=(self._interning))
                self._parser.namespace_prefixes = 1
                self._parser.StartElementHandler = self.start_element_ns
                self._parser.EndElementHandler = self.end_element_ns
            else:
                self._parser = expat.ParserCreate((self._source.getEncoding()), intern=(self._interning))
                self._parser.StartElementHandler = self.start_element
                self._parser.EndElementHandler = self.end_element
            self._reset_cont_handler()
            self._parser.UnparsedEntityDeclHandler = self.unparsed_entity_decl
            self._parser.NotationDeclHandler = self.notation_decl
            self._parser.StartNamespaceDeclHandler = self.start_namespace_decl
            self._parser.EndNamespaceDeclHandler = self.end_namespace_decl
            self._decl_handler_prop = None
            if self._lex_handler_prop:
                self._reset_lex_handler_prop()
            self._parser.ExternalEntityRefHandler = self.external_entity_ref
            try:
                self._parser.SkippedEntityHandler = self.skipped_entity_handler
            except AttributeError:
                pass
            else:
                self._parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE)
                self._parsing = 0
                self._entity_stack = []

        def getColumnNumber(self):
            if self._parser is None:
                return
            return self._parser.ErrorColumnNumber

        def getLineNumber(self):
            if self._parser is None:
                return 1
            return self._parser.ErrorLineNumber

        def getPublicId(self):
            return self._source.getPublicId()

        def getSystemId(self):
            return self._source.getSystemId()

        def start_element(self, name, attrs):
            self._cont_handler.startElement(name, AttributesImpl(attrs))

        def end_element(self, name):
            self._cont_handler.endElement(name)

        def start_element_ns(self, name, attrs):
            pair = name.split()
            if len(pair) == 1:
                pair = (None, name)
            else:
                if len(pair) == 3:
                    pair = (
                     pair[0], pair[1])
                else:
                    pair = tuple(pair)
            newattrs = {}
            qnames = {}
            for aname, value in attrs.items():
                parts = aname.split()
                length = len(parts)
                if length == 1:
                    qname = aname
                    apair = (None, aname)
                else:
                    if length == 3:
                        qname = '%s:%s' % (parts[2], parts[1])
                        apair = (parts[0], parts[1])
                    else:
                        qname = parts[1]
                        apair = tuple(parts)
                newattrs[apair] = value
                qnames[apair] = qname
            else:
                self._cont_handler.startElementNS(pair, None, AttributesNSImpl(newattrs, qnames))

        def end_element_ns(self, name):
            pair = name.split()
            if len(pair) == 1:
                pair = (
                 None, name)
            else:
                if len(pair) == 3:
                    pair = (
                     pair[0], pair[1])
                else:
                    pair = tuple(pair)
            self._cont_handler.endElementNS(pair, None)

        def processing_instruction(self, target, data):
            self._cont_handler.processingInstruction(target, data)

        def character_data(self, data):
            self._cont_handler.characters(data)

        def start_namespace_decl(self, prefix, uri):
            self._cont_handler.startPrefixMapping(prefix, uri)

        def end_namespace_decl(self, prefix):
            self._cont_handler.endPrefixMapping(prefix)

        def start_doctype_decl(self, name, sysid, pubid, has_internal_subset):
            self._lex_handler_prop.startDTD(name, pubid, sysid)

        def unparsed_entity_decl(self, name, base, sysid, pubid, notation_name):
            self._dtd_handler.unparsedEntityDecl(name, pubid, sysid, notation_name)

        def notation_decl(self, name, base, sysid, pubid):
            self._dtd_handler.notationDecl(name, pubid, sysid)

        def external_entity_ref--- This code section failed: ---

 L. 407         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _external_ges
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 408         6  LOAD_CONST               1
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 410        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _ent_handler
               14  LOAD_METHOD              resolveEntity
               16  LOAD_FAST                'pubid'
               18  LOAD_FAST                'sysid'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'source'

 L. 411        24  LOAD_GLOBAL              saxutils
               26  LOAD_METHOD              prepare_input_source
               28  LOAD_FAST                'source'

 L. 412        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _source
               34  LOAD_METHOD              getSystemId
               36  CALL_METHOD_0         0  ''
               38  JUMP_IF_TRUE_OR_POP    42  'to 42'

 L. 413        40  LOAD_STR                 ''
             42_0  COME_FROM            38  '38'

 L. 411        42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'source'

 L. 415        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _entity_stack
               50  LOAD_METHOD              append
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _parser
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _source
               60  BUILD_TUPLE_2         2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 416        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _parser
               70  LOAD_METHOD              ExternalEntityParserCreate
               72  LOAD_FAST                'context'
               74  CALL_METHOD_1         1  ''
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _parser

 L. 417        80  LOAD_FAST                'source'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _source

 L. 419        86  SETUP_FINALLY       106  'to 106'

 L. 420        88  LOAD_GLOBAL              xmlreader
               90  LOAD_ATTR                IncrementalParser
               92  LOAD_METHOD              parse
               94  LOAD_FAST                'self'
               96  LOAD_FAST                'source'
               98  CALL_METHOD_2         2  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  JUMP_FORWARD        120  'to 120'
            106_0  COME_FROM_FINALLY    86  '86'

 L. 421       106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 422       112  POP_EXCEPT       
              114  LOAD_CONST               0
              116  RETURN_VALUE     
              118  END_FINALLY      
            120_0  COME_FROM           104  '104'

 L. 424       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _entity_stack
              124  LOAD_CONST               -1
              126  BINARY_SUBSCR    
              128  UNPACK_SEQUENCE_2     2 
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _parser
              134  LOAD_FAST                'self'
              136  STORE_ATTR               _source

 L. 425       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _entity_stack
              142  LOAD_CONST               -1
              144  DELETE_SUBSCR    

 L. 426       146  LOAD_CONST               1
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 114

        def skipped_entity_handler(self, name, is_pe):
            if is_pe:
                name = '%' + name
            self._cont_handler.skippedEntity(name)


    def create_parser(*args, **kwargs):
        return ExpatParser(*args, **kwargs)


    if __name__ == '__main__':
        import xml.sax.saxutils
        p = create_parser()
        p.setContentHandler(xml.sax.saxutils.XMLGenerator())
        p.setErrorHandler(xml.sax.ErrorHandler())
        p.parse('http://www.ibiblio.org/xml/examples/shakespeare/hamlet.xml')