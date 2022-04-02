# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\sax\_exceptions.py
"""Different kinds of SAX Exceptions"""
import sys
if sys.platform[:4] == 'java':
    from java.lang import Exception
del sys

class SAXException(Exception):
    __doc__ = 'Encapsulate an XML error or warning. This class can contain\n    basic error or warning information from either the XML parser or\n    the application: you can subclass it to provide additional\n    functionality, or to add localization. Note that although you will\n    receive a SAXException as the argument to the handlers in the\n    ErrorHandler interface, you are not actually required to raise\n    the exception; instead, you can simply read the information in\n    it.'

    def __init__(self, msg, exception=None):
        """Creates an exception. The message is required, but the exception
        is optional."""
        self._msg = msg
        self._exception = exception
        Exception.__init__(self, msg)

    def getMessage(self):
        """Return a message for this exception."""
        return self._msg

    def getException(self):
        """Return the embedded exception, or None if there was none."""
        return self._exception

    def __str__(self):
        """Create a string representation of the exception."""
        return self._msg

    def __getitem__(self, ix):
        """Avoids weird error messages if someone does exception[ix] by
        mistake, since Exception has __getitem__ defined."""
        raise AttributeError('__getitem__')


class SAXParseException(SAXException):
    __doc__ = 'Encapsulate an XML parse error or warning.\n\n    This exception will include information for locating the error in\n    the original XML document. Note that although the application will\n    receive a SAXParseException as the argument to the handlers in the\n    ErrorHandler interface, the application is not actually required\n    to raise the exception; instead, it can simply read the\n    information in it and take a different action.\n\n    Since this exception is a subclass of SAXException, it inherits\n    the ability to wrap another exception.'

    def __init__(self, msg, exception, locator):
        """Creates the exception. The exception parameter is allowed to be None."""
        SAXException.__init__(self, msg, exception)
        self._locator = locator
        self._systemId = self._locator.getSystemId()
        self._colnum = self._locator.getColumnNumber()
        self._linenum = self._locator.getLineNumber()

    def getColumnNumber(self):
        """The column number of the end of the text where the exception
        occurred."""
        return self._colnum

    def getLineNumber(self):
        """The line number of the end of the text where the exception occurred."""
        return self._linenum

    def getPublicId(self):
        """Get the public identifier of the entity where the exception occurred."""
        return self._locator.getPublicId()

    def getSystemId(self):
        """Get the system identifier of the entity where the exception occurred."""
        return self._systemId

    def __str__--- This code section failed: ---

 L.  91         0  LOAD_FAST                'self'
                2  LOAD_METHOD              getSystemId
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'sysid'

 L.  92         8  LOAD_FAST                'sysid'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  93        16  LOAD_STR                 '<unknown>'
               18  STORE_FAST               'sysid'
             20_0  COME_FROM            14  '14'

 L.  94        20  LOAD_FAST                'self'
               22  LOAD_METHOD              getLineNumber
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'linenum'

 L.  95        28  LOAD_FAST                'linenum'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.  96        36  LOAD_STR                 '?'
               38  STORE_FAST               'linenum'
             40_0  COME_FROM            34  '34'

 L.  97        40  LOAD_FAST                'self'
               42  LOAD_METHOD              getColumnNumber
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'colnum'

 L.  98        48  LOAD_FAST                'colnum'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.  99        56  LOAD_STR                 '?'
               58  STORE_FAST               'colnum'
             60_0  COME_FROM            54  '54'

 L. 100        60  LOAD_STR                 '%s:%s:%s: %s'
               62  LOAD_FAST                'sysid'
               64  LOAD_FAST                'linenum'
               66  LOAD_FAST                'colnum'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _msg
               72  BUILD_TUPLE_4         4 
               74  BINARY_MODULO    
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 12


class SAXNotRecognizedException(SAXException):
    __doc__ = 'Exception class for an unrecognized identifier.\n\n    An XMLReader will raise this exception when it is confronted with an\n    unrecognized feature or property. SAX applications and extensions may\n    use this class for similar purposes.'


class SAXNotSupportedException(SAXException):
    __doc__ = 'Exception class for an unsupported operation.\n\n    An XMLReader will raise this exception when a service it cannot\n    perform is requested (specifically setting a state or value). SAX\n    applications and extensions may use this class for similar\n    purposes.'


class SAXReaderNotAvailable(SAXNotSupportedException):
    __doc__ = 'Exception class for a missing driver.\n\n    An XMLReader module (driver) should raise this exception when it\n    is first imported, e.g. when a support module cannot be imported.\n    It also may be raised during parsing, e.g. if executing an external\n    program is not permitted.'