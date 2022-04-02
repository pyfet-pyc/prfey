# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\sax\__init__.py
"""Simple API for XML (SAX) implementation for Python.

This module provides an implementation of the SAX 2 interface;
information about the Java version of the interface can be found at
http://www.megginson.com/SAX/.  The Python version of the interface is
documented at <...>.

This package contains the following modules:

handler -- Base classes and constants which define the SAX 2 API for
           the 'client-side' of SAX for Python.

saxutils -- Implementation of the convenience classes commonly used to
            work with SAX.

xmlreader -- Base classes and constants which define the SAX 2 API for
             the parsers used with SAX for Python.

expatreader -- Driver that allows use of the Expat parser with SAX.
"""
from .xmlreader import InputSource
from .handler import ContentHandler, ErrorHandler
from ._exceptions import SAXException, SAXNotRecognizedException, SAXParseException, SAXNotSupportedException, SAXReaderNotAvailable

def parse(source, handler, errorHandler=ErrorHandler()):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(source)


def parseString(string, handler, errorHandler=ErrorHandler()):
    import io
    if errorHandler is None:
        errorHandler = ErrorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    inpsrc = InputSource()
    if isinstance(string, str):
        inpsrc.setCharacterStream(io.StringIO(string))
    else:
        inpsrc.setByteStream(io.BytesIO(string))
    parser.parse(inpsrc)


default_parser_list = [
 'xml.sax.expatreader']
_false = 0
if _false:
    import xml.sax.expatreader
import os, sys
if not sys.flags.ignore_environment:
    if 'PY_SAX_PARSER' in os.environ:
        default_parser_list = os.environ['PY_SAX_PARSER'].split(',')
del os
_key = 'python.xml.sax.parser'
if sys.platform[:4] == 'java':
    if sys.registry.containsKey(_key):
        default_parser_list = sys.registry.getProperty(_key).split(',')

def make_parser--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'parser_list'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              default_parser_list
                8  BINARY_ADD       
               10  GET_ITER         
             12_0  COME_FROM           104  '104'
             12_1  COME_FROM           100  '100'
             12_2  COME_FROM            82  '82'
               12  FOR_ITER            106  'to 106'
               14  STORE_FAST               'parser_name'

 L.  79        16  SETUP_FINALLY        32  'to 32'

 L.  80        18  LOAD_GLOBAL              _create_parser
               20  LOAD_FAST                'parser_name'
               22  CALL_FUNCTION_1       1  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    16  '16'

 L.  81        32  DUP_TOP          
               34  LOAD_GLOBAL              ImportError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    84  'to 84'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY        72  'to 72'

 L.  82        48  LOAD_CONST               0
               50  LOAD_CONST               None
               52  IMPORT_NAME              sys
               54  STORE_FAST               'sys'

 L.  83        56  LOAD_FAST                'parser_name'
               58  LOAD_FAST                'sys'
               60  LOAD_ATTR                modules
               62  COMPARE_OP               in
               64  POP_JUMP_IF_FALSE    68  'to 68'

 L.  86        66  RAISE_VARARGS_0       0  'reraise'
             68_0  COME_FROM            64  '64'
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    46  '46'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_BACK            12  'to 12'
             84_0  COME_FROM            38  '38'

 L.  87        84  DUP_TOP          
               86  LOAD_GLOBAL              SAXReaderNotAvailable
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  90        98  POP_EXCEPT       
              100  JUMP_BACK            12  'to 12'
            102_0  COME_FROM            90  '90'
              102  END_FINALLY      
              104  JUMP_BACK            12  'to 12'
            106_0  COME_FROM            12  '12'

 L.  92       106  LOAD_GLOBAL              SAXReaderNotAvailable
              108  LOAD_STR                 'No parsers found'
              110  LOAD_CONST               None
              112  CALL_FUNCTION_2       2  ''
              114  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 26


if sys.platform[:4] == 'java':

    def _create_parser(parser_name):
        from org.python.core import imp
        drv_module = imp.importName(parser_name, 0, globals())
        return drv_module.create_parser()


else:

    def _create_parser(parser_name):
        drv_module = __import__(parser_name, {}, {}, ['create_parser'])
        return drv_module.create_parser()


del sys