# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\http_exceptions.py
"""Low-level http related exceptions."""
from typing import Optional, Union
from .typedefs import _CIMultiDict
__all__ = ('HttpProcessingError', )

class HttpProcessingError(Exception):
    __doc__ = 'HTTP error.\n\n    Shortcut for raising HTTP errors with custom code, message and headers.\n\n    code: HTTP Error code.\n    message: (optional) Error message.\n    headers: (optional) Headers to be sent in response, a list of pairs\n    '
    code = 0
    message = ''
    headers = None

    def __init__--- This code section failed: ---

 L.  32         0  LOAD_FAST                'code'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  33         8  LOAD_FAST                'code'
               10  LOAD_FAST                'self'
               12  STORE_ATTR               code
             14_0  COME_FROM             6  '6'

 L.  34        14  LOAD_FAST                'headers'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               headers

 L.  35        20  LOAD_FAST                'message'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               message

Parse error at or near `None' instruction at offset -1

    def __str__(self) -> str:
        return f"{self.code}, message={self.message!r}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"


class BadHttpMessage(HttpProcessingError):
    code = 400
    message = 'Bad Request'

    def __init__(self, message, *, headers=None):
        super().__init__(message=message, headers=headers)
        self.args = (message,)


class HttpBadRequest(BadHttpMessage):
    code = 400
    message = 'Bad Request'


class PayloadEncodingError(BadHttpMessage):
    __doc__ = 'Base class for payload errors'


class ContentEncodingError(PayloadEncodingError):
    __doc__ = 'Content encoding error.'


class TransferEncodingError(PayloadEncodingError):
    __doc__ = 'transfer encoding error.'


class ContentLengthError(PayloadEncodingError):
    __doc__ = 'Not enough data for satisfy content length header.'


class LineTooLong(BadHttpMessage):

    def __init__(self, line, limit='Unknown', actual_size='Unknown'):
        super().__init__(f"Got more than {limit} bytes ({actual_size}) when reading {line}.")
        self.args = (
         line, limit, actual_size)


class InvalidHeader(BadHttpMessage):

    def __init__(self, hdr):
        if isinstance(hdr, bytes):
            hdr = hdr.decode('utf-8', 'surrogateescape')
        super().__init__(f"Invalid HTTP Header: {hdr}")
        self.hdr = hdr
        self.args = (hdr,)


class BadStatusLine(BadHttpMessage):

    def __init__(self, line=''):
        if not isinstance(line, str):
            line = repr(line)
        super().__init__(f"Bad status line {line!r}")
        self.args = (line,)
        self.line = line


class InvalidURLError(BadHttpMessage):
    pass