# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\exceptions.py
"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.
"""
import urllib3.exceptions as BaseHTTPError

class RequestException(IOError):
    __doc__ = 'There was an ambiguous exception that occurred while handling your\n    request.\n    '

    def __init__--- This code section failed: ---

 L.  19         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'response'
                6  LOAD_CONST               None
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'response'

 L.  20        12  LOAD_FAST                'response'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               response

 L.  21        18  LOAD_FAST                'kwargs'
               20  LOAD_METHOD              pop
               22  LOAD_STR                 'request'
               24  LOAD_CONST               None
               26  CALL_METHOD_2         2  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               request

 L.  22        32  LOAD_FAST                'response'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    66  'to 66'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                request
               44  POP_JUMP_IF_TRUE     66  'to 66'

 L.  23        46  LOAD_GLOBAL              hasattr
               48  LOAD_FAST                'response'
               50  LOAD_STR                 'request'
               52  CALL_FUNCTION_2       2  ''

 L.  22        54  POP_JUMP_IF_FALSE    66  'to 66'

 L.  24        56  LOAD_FAST                'self'
               58  LOAD_ATTR                response
               60  LOAD_ATTR                request
               62  LOAD_FAST                'self'
               64  STORE_ATTR               request
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            44  '44'
             66_2  COME_FROM            38  '38'

 L.  25        66  LOAD_GLOBAL              super
               68  LOAD_GLOBAL              RequestException
               70  LOAD_FAST                'self'
               72  CALL_FUNCTION_2       2  ''
               74  LOAD_ATTR                __init__
               76  LOAD_FAST                'args'
               78  BUILD_MAP_0           0 
               80  LOAD_FAST                'kwargs'
               82  <164>                 1  ''
               84  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               86  POP_TOP          

Parse error at or near `<117>' instruction at offset 36


class HTTPError(RequestException):
    __doc__ = 'An HTTP error occurred.'


class ConnectionError(RequestException):
    __doc__ = 'A Connection error occurred.'


class ProxyError(ConnectionError):
    __doc__ = 'A proxy error occurred.'


class SSLError(ConnectionError):
    __doc__ = 'An SSL error occurred.'


class Timeout(RequestException):
    __doc__ = 'The request timed out.\n\n    Catching this error will catch both\n    :exc:`~requests.exceptions.ConnectTimeout` and\n    :exc:`~requests.exceptions.ReadTimeout` errors.\n    '


class ConnectTimeout(ConnectionError, Timeout):
    __doc__ = 'The request timed out while trying to connect to the remote server.\n\n    Requests that produced this error are safe to retry.\n    '


class ReadTimeout(Timeout):
    __doc__ = 'The server did not send any data in the allotted amount of time.'


class URLRequired(RequestException):
    __doc__ = 'A valid URL is required to make a request.'


class TooManyRedirects(RequestException):
    __doc__ = 'Too many redirects.'


class MissingSchema(RequestException, ValueError):
    __doc__ = 'The URL schema (e.g. http or https) is missing.'


class InvalidSchema(RequestException, ValueError):
    __doc__ = 'See defaults.py for valid schemas.'


class InvalidURL(RequestException, ValueError):
    __doc__ = 'The URL provided was somehow invalid.'


class InvalidHeader(RequestException, ValueError):
    __doc__ = 'The header value provided was somehow invalid.'


class InvalidProxyURL(InvalidURL):
    __doc__ = 'The proxy URL provided is invalid.'


class ChunkedEncodingError(RequestException):
    __doc__ = 'The server declared chunked encoding but sent an invalid chunk.'


class ContentDecodingError(RequestException, BaseHTTPError):
    __doc__ = 'Failed to decode response content.'


class StreamConsumedError(RequestException, TypeError):
    __doc__ = 'The content for this response was already consumed.'


class RetryError(RequestException):
    __doc__ = 'Custom retries logic failed'


class UnrewindableBodyError(RequestException):
    __doc__ = 'Requests encountered an error when trying to rewind a body.'


class RequestsWarning(Warning):
    __doc__ = 'Base warning for Requests.'


class FileModeWarning(RequestsWarning, DeprecationWarning):
    __doc__ = 'A file was opened in text mode, but Requests determined its binary length.'


class RequestsDependencyWarning(RequestsWarning):
    __doc__ = "An imported dependency doesn't match the expected version range."