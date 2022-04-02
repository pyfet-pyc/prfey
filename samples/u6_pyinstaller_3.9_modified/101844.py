# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\response.py
from __future__ import absolute_import
from email.errors import MultipartInvariantViolationDefect, StartBoundaryNotFoundDefect
from ..exceptions import HeaderParsingError
import packages.six.moves as httplib

def is_fp_closed--- This code section failed: ---

 L.  17         0  SETUP_FINALLY        12  'to 12'

 L.  20         2  LOAD_FAST                'obj'
                4  LOAD_METHOD              isclosed
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  21        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                28  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  22        24  POP_EXCEPT       
               26  JUMP_FORWARD         30  'to 30'
               28  <48>             
             30_0  COME_FROM            26  '26'

 L.  24        30  SETUP_FINALLY        40  'to 40'

 L.  26        32  LOAD_FAST                'obj'
               34  LOAD_ATTR                closed
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    30  '30'

 L.  27        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  <121>                56  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  28        52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'

 L.  30        58  SETUP_FINALLY        72  'to 72'

 L.  33        60  LOAD_FAST                'obj'
               62  LOAD_ATTR                fp
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    58  '58'

 L.  34        72  DUP_TOP          
               74  LOAD_GLOBAL              AttributeError
               76  <121>                88  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L.  35        84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'

 L.  37        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'Unable to determine whether fp is closed.'
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 16


def assert_header_parsing(headers):
    """
    Asserts whether all headers have been successfully parsed.
    Extracts encountered errors from the result of parsing headers.

    Only works on Python 3.

    :param http.client.HTTPMessage headers: Headers to verify.

    :raises urllib3.exceptions.HeaderParsingError:
        If parsing errors are found.
    """
    if not isinstance(headers, httplib.HTTPMessage):
        raise TypeError('expected httplib.Message, got {0}.'.format(type(headers)))
    defects = getattr(headers, 'defects', None)
    get_payload = getattr(headers, 'get_payload', None)
    unparsed_data = None
    if get_payload:
        if not headers.is_multipart:
            payload = get_payload()
            if isinstance(payload, (bytes, str)):
                unparsed_data = payload
    if defects:
        defects = [defect for defect in defects if not isinstance(defect, (StartBoundaryNotFoundDefect, MultipartInvariantViolationDefect))]
    if defects or unparsed_data:
        raise HeaderParsingError(defects=defects, unparsed_data=unparsed_data)


def is_response_to_head(response):
    """
    Checks whether the request of a response has been a HEAD-request.
    Handles the quirks of AppEngine.

    :param http.client.HTTPResponse response:
        Response to check if the originating request
        used 'HEAD' as a method.
    """
    method = response._method
    if isinstance(method, int):
        return method == 3
    return method.upper == 'HEAD'