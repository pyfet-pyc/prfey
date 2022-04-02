# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_exceptions.py
import warnings
from typing import Any, Dict, Iterable, List, Optional, Set
from yarl import URL
from .typedefs import LooseHeaders, StrOrURL
from .web_response import Response
__all__ = ('HTTPException', 'HTTPError', 'HTTPRedirection', 'HTTPSuccessful', 'HTTPOk',
           'HTTPCreated', 'HTTPAccepted', 'HTTPNonAuthoritativeInformation', 'HTTPNoContent',
           'HTTPResetContent', 'HTTPPartialContent', 'HTTPMultipleChoices', 'HTTPMovedPermanently',
           'HTTPFound', 'HTTPSeeOther', 'HTTPNotModified', 'HTTPUseProxy', 'HTTPTemporaryRedirect',
           'HTTPPermanentRedirect', 'HTTPClientError', 'HTTPBadRequest', 'HTTPUnauthorized',
           'HTTPPaymentRequired', 'HTTPForbidden', 'HTTPNotFound', 'HTTPMethodNotAllowed',
           'HTTPNotAcceptable', 'HTTPProxyAuthenticationRequired', 'HTTPRequestTimeout',
           'HTTPConflict', 'HTTPGone', 'HTTPLengthRequired', 'HTTPPreconditionFailed',
           'HTTPRequestEntityTooLarge', 'HTTPRequestURITooLong', 'HTTPUnsupportedMediaType',
           'HTTPRequestRangeNotSatisfiable', 'HTTPExpectationFailed', 'HTTPMisdirectedRequest',
           'HTTPUnprocessableEntity', 'HTTPFailedDependency', 'HTTPUpgradeRequired',
           'HTTPPreconditionRequired', 'HTTPTooManyRequests', 'HTTPRequestHeaderFieldsTooLarge',
           'HTTPUnavailableForLegalReasons', 'HTTPServerError', 'HTTPInternalServerError',
           'HTTPNotImplemented', 'HTTPBadGateway', 'HTTPServiceUnavailable', 'HTTPGatewayTimeout',
           'HTTPVersionNotSupported', 'HTTPVariantAlsoNegotiates', 'HTTPInsufficientStorage',
           'HTTPNotExtended', 'HTTPNetworkAuthenticationRequired')

class HTTPException(Response, Exception):
    status_code = -1
    empty_body = False
    __http_exception__ = True

    def __init__--- This code section failed: ---

 L.  94         0  LOAD_FAST                'body'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  95         8  LOAD_GLOBAL              warnings
               10  LOAD_METHOD              warn

 L.  96        12  LOAD_STR                 'body argument is deprecated for http web exceptions'

 L.  97        14  LOAD_GLOBAL              DeprecationWarning

 L.  95        16  CALL_METHOD_2         2  ''
               18  POP_TOP          
             20_0  COME_FROM             6  '6'

 L.  99        20  LOAD_GLOBAL              Response
               22  LOAD_ATTR                __init__

 L. 100        24  LOAD_FAST                'self'

 L. 101        26  LOAD_FAST                'self'
               28  LOAD_ATTR                status_code

 L. 102        30  LOAD_FAST                'headers'

 L. 103        32  LOAD_FAST                'reason'

 L. 104        34  LOAD_FAST                'body'

 L. 105        36  LOAD_FAST                'text'

 L. 106        38  LOAD_FAST                'content_type'

 L.  99        40  LOAD_CONST               ('status', 'headers', 'reason', 'body', 'text', 'content_type')
               42  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               44  POP_TOP          

 L. 108        46  LOAD_GLOBAL              Exception
               48  LOAD_METHOD              __init__
               50  LOAD_FAST                'self'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                reason
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L. 109        60  LOAD_FAST                'self'
               62  LOAD_ATTR                body
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_FALSE    96  'to 96'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                empty_body
               74  POP_JUMP_IF_TRUE     96  'to 96'

 L. 110        76  LOAD_FAST                'self'
               78  LOAD_ATTR                status
               80  FORMAT_VALUE          0  ''
               82  LOAD_STR                 ': '
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                reason
               88  FORMAT_VALUE          0  ''
               90  BUILD_STRING_3        3 
               92  LOAD_FAST                'self'
               94  STORE_ATTR               text
             96_0  COME_FROM            74  '74'
             96_1  COME_FROM            68  '68'

Parse error at or near `None' instruction at offset -1

    def __bool__(self) -> bool:
        return True


class HTTPError(HTTPException):
    __doc__ = 'Base class for exceptions with status codes in the 400s and 500s.'


class HTTPRedirection(HTTPException):
    __doc__ = 'Base class for exceptions with status codes in the 300s.'


class HTTPSuccessful(HTTPException):
    __doc__ = 'Base class for exceptions with status codes in the 200s.'


class HTTPOk(HTTPSuccessful):
    status_code = 200


class HTTPCreated(HTTPSuccessful):
    status_code = 201


class HTTPAccepted(HTTPSuccessful):
    status_code = 202


class HTTPNonAuthoritativeInformation(HTTPSuccessful):
    status_code = 203


class HTTPNoContent(HTTPSuccessful):
    status_code = 204
    empty_body = True


class HTTPResetContent(HTTPSuccessful):
    status_code = 205
    empty_body = True


class HTTPPartialContent(HTTPSuccessful):
    status_code = 206


class _HTTPMove(HTTPRedirection):

    def __init__(self, location, *, headers=None, reason=None, body=None, text=None, content_type=None):
        if not location:
            raise ValueError('HTTP redirects need a location to redirect to.')
        super().__init__(headers=headers,
          reason=reason,
          body=body,
          text=text,
          content_type=content_type)
        self.headers['Location'] = str(URL(location))
        self.location = location


class HTTPMultipleChoices(_HTTPMove):
    status_code = 300


class HTTPMovedPermanently(_HTTPMove):
    status_code = 301


class HTTPFound(_HTTPMove):
    status_code = 302


class HTTPSeeOther(_HTTPMove):
    status_code = 303


class HTTPNotModified(HTTPRedirection):
    status_code = 304
    empty_body = True


class HTTPUseProxy(_HTTPMove):
    status_code = 305


class HTTPTemporaryRedirect(_HTTPMove):
    status_code = 307


class HTTPPermanentRedirect(_HTTPMove):
    status_code = 308


class HTTPClientError(HTTPError):
    pass


class HTTPBadRequest(HTTPClientError):
    status_code = 400


class HTTPUnauthorized(HTTPClientError):
    status_code = 401


class HTTPPaymentRequired(HTTPClientError):
    status_code = 402


class HTTPForbidden(HTTPClientError):
    status_code = 403


class HTTPNotFound(HTTPClientError):
    status_code = 404


class HTTPMethodNotAllowed(HTTPClientError):
    status_code = 405

    def __init__(self, method, allowed_methods, *, headers=None, reason=None, body=None, text=None, content_type=None):
        allow = ','.join(sorted(allowed_methods))
        super().__init__(headers=headers,
          reason=reason,
          body=body,
          text=text,
          content_type=content_type)
        self.headers['Allow'] = allow
        self.allowed_methods = set(allowed_methods)
        self.method = method.upper()


class HTTPNotAcceptable(HTTPClientError):
    status_code = 406


class HTTPProxyAuthenticationRequired(HTTPClientError):
    status_code = 407


class HTTPRequestTimeout(HTTPClientError):
    status_code = 408


class HTTPConflict(HTTPClientError):
    status_code = 409


class HTTPGone(HTTPClientError):
    status_code = 410


class HTTPLengthRequired(HTTPClientError):
    status_code = 411


class HTTPPreconditionFailed(HTTPClientError):
    status_code = 412


class HTTPRequestEntityTooLarge(HTTPClientError):
    status_code = 413

    def __init__--- This code section failed: ---

 L. 312         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              setdefault

 L. 313         4  LOAD_STR                 'text'

 L. 314         6  LOAD_STR                 'Maximum request body size {} exceeded, actual body size {}'
                8  LOAD_METHOD              format

 L. 315        10  LOAD_FAST                'max_size'
               12  LOAD_FAST                'actual_size'

 L. 314        14  CALL_METHOD_2         2  ''

 L. 312        16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L. 317        20  LOAD_GLOBAL              super
               22  CALL_FUNCTION_0       0  ''
               24  LOAD_ATTR                __init__
               26  BUILD_TUPLE_0         0 
               28  BUILD_MAP_0           0 
               30  LOAD_FAST                'kwargs'
               32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          

Parse error at or near `<164>' instruction at offset 32


class HTTPRequestURITooLong(HTTPClientError):
    status_code = 414


class HTTPUnsupportedMediaType(HTTPClientError):
    status_code = 415


class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    status_code = 416


class HTTPExpectationFailed(HTTPClientError):
    status_code = 417


class HTTPMisdirectedRequest(HTTPClientError):
    status_code = 421


class HTTPUnprocessableEntity(HTTPClientError):
    status_code = 422


class HTTPFailedDependency(HTTPClientError):
    status_code = 424


class HTTPUpgradeRequired(HTTPClientError):
    status_code = 426


class HTTPPreconditionRequired(HTTPClientError):
    status_code = 428


class HTTPTooManyRequests(HTTPClientError):
    status_code = 429


class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    status_code = 431


class HTTPUnavailableForLegalReasons(HTTPClientError):
    status_code = 451

    def __init__(self, link, *, headers=None, reason=None, body=None, text=None, content_type=None):
        super().__init__(headers=headers,
          reason=reason,
          body=body,
          text=text,
          content_type=content_type)
        self.headers['Link'] = '<%s>; rel="blocked-by"' % link
        self.link = link


class HTTPServerError(HTTPError):
    pass


class HTTPInternalServerError(HTTPServerError):
    status_code = 500


class HTTPNotImplemented(HTTPServerError):
    status_code = 501


class HTTPBadGateway(HTTPServerError):
    status_code = 502


class HTTPServiceUnavailable(HTTPServerError):
    status_code = 503


class HTTPGatewayTimeout(HTTPServerError):
    status_code = 504


class HTTPVersionNotSupported(HTTPServerError):
    status_code = 505


class HTTPVariantAlsoNegotiates(HTTPServerError):
    status_code = 506


class HTTPInsufficientStorage(HTTPServerError):
    status_code = 507


class HTTPNotExtended(HTTPServerError):
    status_code = 510


class HTTPNetworkAuthenticationRequired(HTTPServerError):
    status_code = 511