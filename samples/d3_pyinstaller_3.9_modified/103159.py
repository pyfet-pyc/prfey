# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\sax\xmlreader.py
"""An XML Reader is the SAX 2 name for an XML parser. XML Parsers
should be based on this code. """
from . import handler
from ._exceptions import SAXNotSupportedException, SAXNotRecognizedException

class XMLReader:
    __doc__ = "Interface for reading an XML document using callbacks.\n\n    XMLReader is the interface that an XML parser's SAX2 driver must\n    implement. This interface allows an application to set and query\n    features and properties in the parser, to register event handlers\n    for document processing, and to initiate a document parse.\n\n    All SAX interfaces are assumed to be synchronous: the parse\n    methods must not return until parsing is complete, and readers\n    must wait for an event-handler callback to return before reporting\n    the next event."

    def __init__(self):
        self._cont_handler = handler.ContentHandler()
        self._dtd_handler = handler.DTDHandler()
        self._ent_handler = handler.EntityResolver()
        self._err_handler = handler.ErrorHandler()

    def parse(self, source):
        """Parse an XML document from a system identifier or an InputSource."""
        raise NotImplementedError('This method must be implemented!')

    def getContentHandler(self):
        """Returns the current ContentHandler."""
        return self._cont_handler

    def setContentHandler(self, handler):
        """Registers a new object to receive document content events."""
        self._cont_handler = handler

    def getDTDHandler(self):
        """Returns the current DTD handler."""
        return self._dtd_handler

    def setDTDHandler(self, handler):
        """Register an object to receive basic DTD-related events."""
        self._dtd_handler = handler

    def getEntityResolver(self):
        """Returns the current EntityResolver."""
        return self._ent_handler

    def setEntityResolver(self, resolver):
        """Register an object to resolve external entities."""
        self._ent_handler = resolver

    def getErrorHandler(self):
        """Returns the current ErrorHandler."""
        return self._err_handler

    def setErrorHandler(self, handler):
        """Register an object to receive error-message events."""
        self._err_handler = handler

    def setLocale(self, locale):
        """Allow an application to set the locale for errors and warnings.

        SAX parsers are not required to provide localization for errors
        and warnings; if they cannot support the requested locale,
        however, they must raise a SAX exception. Applications may
        request a locale change in the middle of a parse."""
        raise SAXNotSupportedException('Locale support not implemented')

    def getFeature(self, name):
        """Looks up and returns the state of a SAX2 feature."""
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def setFeature(self, name, state):
        """Sets the state of a SAX2 feature."""
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def getProperty(self, name):
        """Looks up and returns the value of a SAX2 property."""
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def setProperty(self, name, value):
        """Sets the value of a SAX2 property."""
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)


class IncrementalParser(XMLReader):
    __doc__ = 'This interface adds three extra methods to the XMLReader\n    interface that allow XML parsers to support incremental\n    parsing. Support for this interface is optional, since not all\n    underlying XML parsers support this functionality.\n\n    When the parser is instantiated it is ready to begin accepting\n    data from the feed method immediately. After parsing has been\n    finished with a call to close the reset method must be called to\n    make the parser ready to accept new data, either from feed or\n    using the parse method.\n\n    Note that these methods must _not_ be called during parsing, that\n    is, after parse has been called and before it returns.\n\n    By default, the class also implements the parse method of the XMLReader\n    interface using the feed, close and reset methods of the\n    IncrementalParser interface as a convenience to SAX 2.0 driver\n    writers.'

    def __init__(self, bufsize=65536):
        self._bufsize = bufsize
        XMLReader.__init__(self)

    def parse--- This code section failed: ---

 L. 116         0  LOAD_CONST               1
                2  LOAD_CONST               ('saxutils',)
                4  IMPORT_NAME              
                6  IMPORT_FROM              saxutils
                8  STORE_FAST               'saxutils'
               10  POP_TOP          

 L. 117        12  LOAD_FAST                'saxutils'
               14  LOAD_METHOD              prepare_input_source
               16  LOAD_FAST                'source'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'source'

 L. 119        22  LOAD_FAST                'self'
               24  LOAD_METHOD              prepareParser
               26  LOAD_FAST                'source'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 120        32  LOAD_FAST                'source'
               34  LOAD_METHOD              getCharacterStream
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'file'

 L. 121        40  LOAD_FAST                'file'
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 122        48  LOAD_FAST                'source'
               50  LOAD_METHOD              getByteStream
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'file'
             56_0  COME_FROM            46  '46'

 L. 123        56  LOAD_FAST                'file'
               58  LOAD_METHOD              read
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _bufsize
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'buffer'
             68_0  COME_FROM            94  '94'

 L. 124        68  LOAD_FAST                'buffer'
               70  POP_JUMP_IF_FALSE    96  'to 96'

 L. 125        72  LOAD_FAST                'self'
               74  LOAD_METHOD              feed
               76  LOAD_FAST                'buffer'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 126        82  LOAD_FAST                'file'
               84  LOAD_METHOD              read
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _bufsize
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'buffer'
               94  JUMP_BACK            68  'to 68'
             96_0  COME_FROM            70  '70'

 L. 127        96  LOAD_FAST                'self'
               98  LOAD_METHOD              close
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

Parse error at or near `<117>' instruction at offset 44

    def feed(self, data):
        """This method gives the raw XML data in the data parameter to
        the parser and makes it parse the data, emitting the
        corresponding events. It is allowed for XML constructs to be
        split across several calls to feed.

        feed may raise SAXException."""
        raise NotImplementedError('This method must be implemented!')

    def prepareParser(self, source):
        """This method is called by the parse implementation to allow
        the SAX 2.0 driver to prepare itself for parsing."""
        raise NotImplementedError('prepareParser must be overridden!')

    def close(self):
        """This method is called when the entire XML document has been
        passed to the parser through the feed method, to notify the
        parser that there are no more data. This allows the parser to
        do the final checks on the document and empty the internal
        data buffer.

        The parser will not be ready to parse another document until
        the reset method has been called.

        close may raise SAXException."""
        raise NotImplementedError('This method must be implemented!')

    def reset(self):
        """This method is called after close has been called to reset
        the parser so that it is ready to parse new documents. The
        results of calling parse or feed after close without calling
        reset are undefined."""
        raise NotImplementedError('This method must be implemented!')


class Locator:
    __doc__ = 'Interface for associating a SAX event with a document\n    location. A locator object will return valid results only during\n    calls to DocumentHandler methods; at any other time, the\n    results are unpredictable.'

    def getColumnNumber(self):
        """Return the column number where the current event ends."""
        return -1

    def getLineNumber(self):
        """Return the line number where the current event ends."""
        return -1

    def getPublicId(self):
        """Return the public identifier for the current event."""
        pass

    def getSystemId(self):
        """Return the system identifier for the current event."""
        pass


class InputSource:
    __doc__ = 'Encapsulation of the information needed by the XMLReader to\n    read entities.\n\n    This class may include information about the public identifier,\n    system identifier, byte stream (possibly with character encoding\n    information) and/or the character stream of an entity.\n\n    Applications will create objects of this class for use in the\n    XMLReader.parse method and for returning from\n    EntityResolver.resolveEntity.\n\n    An InputSource belongs to the application, the XMLReader is not\n    allowed to modify InputSource objects passed to it from the\n    application, although it may make copies and modify those.'

    def __init__(self, system_id=None):
        self._InputSource__system_id = system_id
        self._InputSource__public_id = None
        self._InputSource__encoding = None
        self._InputSource__bytefile = None
        self._InputSource__charfile = None

    def setPublicId(self, public_id):
        """Sets the public identifier of this InputSource."""
        self._InputSource__public_id = public_id

    def getPublicId(self):
        """Returns the public identifier of this InputSource."""
        return self._InputSource__public_id

    def setSystemId(self, system_id):
        """Sets the system identifier of this InputSource."""
        self._InputSource__system_id = system_id

    def getSystemId(self):
        """Returns the system identifier of this InputSource."""
        return self._InputSource__system_id

    def setEncoding(self, encoding):
        """Sets the character encoding of this InputSource.

        The encoding must be a string acceptable for an XML encoding
        declaration (see section 4.3.3 of the XML recommendation).

        The encoding attribute of the InputSource is ignored if the
        InputSource also contains a character stream."""
        self._InputSource__encoding = encoding

    def getEncoding(self):
        """Get the character encoding of this InputSource."""
        return self._InputSource__encoding

    def setByteStream(self, bytefile):
        """Set the byte stream (a Python file-like object which does
        not perform byte-to-character conversion) for this input
        source.

        The SAX parser will ignore this if there is also a character
        stream specified, but it will use a byte stream in preference
        to opening a URI connection itself.

        If the application knows the character encoding of the byte
        stream, it should set it with the setEncoding method."""
        self._InputSource__bytefile = bytefile

    def getByteStream(self):
        """Get the byte stream for this input source.

        The getEncoding method will return the character encoding for
        this byte stream, or None if unknown."""
        return self._InputSource__bytefile

    def setCharacterStream(self, charfile):
        """Set the character stream for this input source. (The stream
        must be a Python 2.0 Unicode-wrapped file-like that performs
        conversion to Unicode strings.)

        If there is a character stream specified, the SAX parser will
        ignore any byte stream and will not attempt to open a URI
        connection to the system identifier."""
        self._InputSource__charfile = charfile

    def getCharacterStream(self):
        """Get the character stream for this input source."""
        return self._InputSource__charfile


class AttributesImpl:

    def __init__(self, attrs):
        """Non-NS-aware implementation.

        attrs should be of the form {name : value}."""
        self._attrs = attrs

    def getLength(self):
        return len(self._attrs)

    def getType(self, name):
        return 'CDATA'

    def getValue(self, name):
        return self._attrs[name]

    def getValueByQName(self, name):
        return self._attrs[name]

    def getNameByQName--- This code section failed: ---

 L. 299         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _attrs
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 300        10  LOAD_GLOBAL              KeyError
               12  LOAD_FAST                'name'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 301        18  LOAD_FAST                'name'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def getQNameByName--- This code section failed: ---

 L. 304         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _attrs
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 305        10  LOAD_GLOBAL              KeyError
               12  LOAD_FAST                'name'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 306        18  LOAD_FAST                'name'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def getNames(self):
        return list(self._attrs.keys())

    def getQNames(self):
        return list(self._attrs.keys())

    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, name):
        return self._attrs[name]

    def keys(self):
        return list(self._attrs.keys())

    def __contains__--- This code section failed: ---

 L. 324         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _attrs
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get(self, name, alternative=None):
        return self._attrs.get(name, alternative)

    def copy(self):
        return self.__class__(self._attrs)

    def items(self):
        return list(self._attrs.items())

    def values(self):
        return list(self._attrs.values())


class AttributesNSImpl(AttributesImpl):

    def __init__(self, attrs, qnames):
        """NS-aware implementation.

        attrs should be of the form {(ns_uri, lname): value, ...}.
        qnames of the form {(ns_uri, lname): qname, ...}."""
        self._attrs = attrs
        self._qnames = qnames

    def getValueByQName(self, name):
        for nsname, qname in self._qnames.items():
            if qname == name:
                return self._attrs[nsname]
        else:
            raise KeyError(name)

    def getNameByQName(self, name):
        for nsname, qname in self._qnames.items():
            if qname == name:
                return nsname
        else:
            raise KeyError(name)

    def getQNameByName(self, name):
        return self._qnames[name]

    def getQNames(self):
        return list(self._qnames.values())

    def copy(self):
        return self.__class__(self._attrs, self._qnames)


def _test():
    XMLReader()
    IncrementalParser()
    Locator()


if __name__ == '__main__':
    _test()