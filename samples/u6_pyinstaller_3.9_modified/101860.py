# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\dom\__init__.py
"""W3C Document Object Model implementation for Python.

The Python mapping of the Document Object Model is documented in the
Python Library Reference in the section on the xml.dom package.

This package contains the following modules:

minidom -- A simple implementation of the Level 1 DOM with namespace
           support added (based on the Level 2 specification) and other
           minor Level 2 functionality.

pulldom -- DOM builder supporting on-demand tree-building for selected
           subtrees of the document.

"""

class Node:
    __doc__ = 'Class giving the NodeType constants.'
    __slots__ = ()
    ELEMENT_NODE = 1
    ATTRIBUTE_NODE = 2
    TEXT_NODE = 3
    CDATA_SECTION_NODE = 4
    ENTITY_REFERENCE_NODE = 5
    ENTITY_NODE = 6
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9
    DOCUMENT_TYPE_NODE = 10
    DOCUMENT_FRAGMENT_NODE = 11
    NOTATION_NODE = 12


INDEX_SIZE_ERR = 1
DOMSTRING_SIZE_ERR = 2
HIERARCHY_REQUEST_ERR = 3
WRONG_DOCUMENT_ERR = 4
INVALID_CHARACTER_ERR = 5
NO_DATA_ALLOWED_ERR = 6
NO_MODIFICATION_ALLOWED_ERR = 7
NOT_FOUND_ERR = 8
NOT_SUPPORTED_ERR = 9
INUSE_ATTRIBUTE_ERR = 10
INVALID_STATE_ERR = 11
SYNTAX_ERR = 12
INVALID_MODIFICATION_ERR = 13
NAMESPACE_ERR = 14
INVALID_ACCESS_ERR = 15
VALIDATION_ERR = 16

class DOMException(Exception):
    __doc__ = 'Abstract base class for DOM exceptions.\n    Exceptions with specific codes are specializations of this class.'

    def __init__--- This code section failed: ---

 L.  67         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_GLOBAL              DOMException
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  68        10  LOAD_GLOBAL              RuntimeError

 L.  69        12  LOAD_STR                 'DOMException should not be instantiated directly'

 L.  68        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  70        18  LOAD_GLOBAL              Exception
               20  LOAD_ATTR                __init__
               22  LOAD_FAST                'self'
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'args'
               28  CALL_FINALLY         31  'to 31'
               30  WITH_CLEANUP_FINISH
               32  BUILD_MAP_0           0 
               34  LOAD_FAST                'kw'
               36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _get_code(self):
        return self.code


class IndexSizeErr(DOMException):
    code = INDEX_SIZE_ERR


class DomstringSizeErr(DOMException):
    code = DOMSTRING_SIZE_ERR


class HierarchyRequestErr(DOMException):
    code = HIERARCHY_REQUEST_ERR


class WrongDocumentErr(DOMException):
    code = WRONG_DOCUMENT_ERR


class InvalidCharacterErr(DOMException):
    code = INVALID_CHARACTER_ERR


class NoDataAllowedErr(DOMException):
    code = NO_DATA_ALLOWED_ERR


class NoModificationAllowedErr(DOMException):
    code = NO_MODIFICATION_ALLOWED_ERR


class NotFoundErr(DOMException):
    code = NOT_FOUND_ERR


class NotSupportedErr(DOMException):
    code = NOT_SUPPORTED_ERR


class InuseAttributeErr(DOMException):
    code = INUSE_ATTRIBUTE_ERR


class InvalidStateErr(DOMException):
    code = INVALID_STATE_ERR


class SyntaxErr(DOMException):
    code = SYNTAX_ERR


class InvalidModificationErr(DOMException):
    code = INVALID_MODIFICATION_ERR


class NamespaceErr(DOMException):
    code = NAMESPACE_ERR


class InvalidAccessErr(DOMException):
    code = INVALID_ACCESS_ERR


class ValidationErr(DOMException):
    code = VALIDATION_ERR


class UserDataHandler:
    __doc__ = 'Class giving the operation constants for UserDataHandler.handle().'
    NODE_CLONED = 1
    NODE_IMPORTED = 2
    NODE_DELETED = 3
    NODE_RENAMED = 4


XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XMLNS_NAMESPACE = 'http://www.w3.org/2000/xmlns/'
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
EMPTY_NAMESPACE = None
EMPTY_PREFIX = None
from .domreg import getDOMImplementation, registerDOMImplementation