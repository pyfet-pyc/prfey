# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\urllib3\util\response.py
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
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  22        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L.  24        32  SETUP_FINALLY        42  'to 42'

 L.  26        34  LOAD_FAST                'obj'
               36  LOAD_ATTR                closed
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    32  '32'

 L.  27        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    60  'to 60'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  28        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            48  '48'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

 L.  30        62  SETUP_FINALLY        76  'to 76'

 L.  33        64  LOAD_FAST                'obj'
               66  LOAD_ATTR                fp
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_BLOCK        
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    62  '62'

 L.  34        76  DUP_TOP          
               78  LOAD_GLOBAL              AttributeError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    94  'to 94'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  35        90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            82  '82'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'

 L.  37        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'Unable to determine whether fp is closed.'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 22


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