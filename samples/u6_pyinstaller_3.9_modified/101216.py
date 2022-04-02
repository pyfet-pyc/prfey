# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: email\errors.py
"""email package exception classes."""

class MessageError(Exception):
    __doc__ = 'Base class for errors in the email package.'


class MessageParseError(MessageError):
    __doc__ = 'Base class for message parsing errors.'


class HeaderParseError(MessageParseError):
    __doc__ = 'Error while parsing headers.'


class BoundaryError(MessageParseError):
    __doc__ = "Couldn't find terminating boundary."


class MultipartConversionError(MessageError, TypeError):
    __doc__ = 'Conversion to a multipart is prohibited.'


class CharsetError(MessageError):
    __doc__ = 'An illegal charset was given.'


class MessageDefect(ValueError):
    __doc__ = 'Base class for a message defect.'

    def __init__--- This code section failed: ---

 L.  37         0  LOAD_FAST                'line'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  38         8  LOAD_GLOBAL              super
               10  CALL_FUNCTION_0       0  ''
               12  LOAD_METHOD              __init__
               14  LOAD_FAST                'line'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          
             20_0  COME_FROM             6  '6'

 L.  39        20  LOAD_FAST                'line'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               line

Parse error at or near `None' instruction at offset -1


class NoBoundaryInMultipartDefect(MessageDefect):
    __doc__ = 'A message claimed to be a multipart but had no boundary parameter.'


class StartBoundaryNotFoundDefect(MessageDefect):
    __doc__ = 'The claimed start boundary was never found.'


class CloseBoundaryNotFoundDefect(MessageDefect):
    __doc__ = 'A start boundary was found, but not the corresponding close boundary.'


class FirstHeaderLineIsContinuationDefect(MessageDefect):
    __doc__ = 'A message had a continuation line as its first header line.'


class MisplacedEnvelopeHeaderDefect(MessageDefect):
    __doc__ = "A 'Unix-from' header was found in the middle of a header block."


class MissingHeaderBodySeparatorDefect(MessageDefect):
    __doc__ = 'Found line with no leading whitespace and no colon before blank line.'


MalformedHeaderDefect = MissingHeaderBodySeparatorDefect

class MultipartInvariantViolationDefect(MessageDefect):
    __doc__ = 'A message claimed to be a multipart but no subparts were found.'


class InvalidMultipartContentTransferEncodingDefect(MessageDefect):
    __doc__ = 'An invalid content transfer encoding was set on the multipart itself.'


class UndecodableBytesDefect(MessageDefect):
    __doc__ = 'Header contained bytes that could not be decoded'


class InvalidBase64PaddingDefect(MessageDefect):
    __doc__ = 'base64 encoded sequence had an incorrect length'


class InvalidBase64CharactersDefect(MessageDefect):
    __doc__ = 'base64 encoded sequence had characters not in base64 alphabet'


class InvalidBase64LengthDefect(MessageDefect):
    __doc__ = 'base64 encoded sequence had invalid length (1 mod 4)'


class HeaderDefect(MessageDefect):
    __doc__ = 'Base class for a header defect.'

    def __init__--- This code section failed: ---

 L.  85         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'args'
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kw'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  POP_TOP          

Parse error at or near `None' instruction at offset -1


class InvalidHeaderDefect(HeaderDefect):
    __doc__ = 'Header is not valid, message gives details.'


class HeaderMissingRequiredValue(HeaderDefect):
    __doc__ = 'A header that must have a value had none'


class NonPrintableDefect(HeaderDefect):
    __doc__ = 'ASCII characters outside the ascii-printable range found'

    def __init__(self, non_printables):
        super.__init__non_printables
        self.non_printables = non_printables

    def __str__(self):
        return 'the following ASCII non-printables found in header: {}'.formatself.non_printables


class ObsoleteHeaderDefect(HeaderDefect):
    __doc__ = 'Header uses syntax declared obsolete by RFC 5322'


class NonASCIILocalPartDefect(HeaderDefect):
    __doc__ = 'local_part contains non-ASCII characters'