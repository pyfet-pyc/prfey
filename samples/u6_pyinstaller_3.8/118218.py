# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_response.py
"""Response classes.

The seek_wrapper code is not used if you're using UserAgent with
.set_seekable_responses(False), or if you're using the urllib2-level interface
HTTPEquivProcessor.  Class closeable_response is instantiated by some handlers
(AbstractHTTPHandler), but the closeable_response interface is only depended
upon by Browser-level code.  Function upgrade_response is only used if you're
using Browser.

Copyright 2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""
from __future__ import absolute_import
from functools import partial
import copy
from io import BytesIO
from ._headersutil import normalize_header_name
from .polyglot import HTTPError, create_response_info

def len_of_seekable(file_):
    pos = file_.tell()
    file_.seek(0, 2)
    try:
        return file_.tell()
    finally:
        file_.seek(pos)


class seek_wrapper:
    __doc__ = 'Adds a seek method to a file object.\n\n    This is only designed for seeking on readonly file-like objects.\n\n    Wrapped file-like object must have a read method.  The readline method is\n    only supported if that method is present on the wrapped object.  The\n    readlines method is always supported.  xreadlines and iteration are\n    supported only for Python 2.2 and above.\n\n    Public attributes:\n\n    wrapped: the wrapped file object\n    is_closed: true iff .close() has been called\n\n    WARNING: All other attributes of the wrapped object (ie. those that are not\n    one of wrapped, read, readline, readlines, xreadlines, __iter__ and next)\n    are passed through unaltered, which may or may not make sense for your\n    particular file object.\n\n    '

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self._seek_wrapper__read_complete_state = [False]
        self._seek_wrapper__is_closed_state = [False]
        self._seek_wrapper__have_readline = hasattr(self.wrapped, 'readline')
        self._seek_wrapper__cache = BytesIO()
        self._seek_wrapper__pos = 0

    def invariant(self):
        return self.wrapped.tell() == len(self._seek_wrapper__cache.getvalue())

    def close(self):
        self.wrapped.close()
        self.is_closed = True

    def __getattr__(self, name):
        if name == 'is_closed':
            return self._seek_wrapper__is_closed_state[0]
        if name == 'read_complete':
            return self._seek_wrapper__read_complete_state[0]
        wrapped = self.__dict__.get('wrapped')
        if wrapped:
            return getattr(wrapped, name)
        return getattr(self.__class__, name)

    def __setattr__(self, name, value):
        if name == 'is_closed':
            self._seek_wrapper__is_closed_state[0] = bool(value)
        else:
            if name == 'read_complete':
                self._seek_wrapper__read_complete_state[0] = self.is_closed or bool(value)
            else:
                self.__dict__[name] = value

    def seek(self, offset, whence=0):
        if not whence in (0, 1, 2):
            raise AssertionError
        else:
            if whence == 2:
                if offset < 0:
                    raise ValueError('negative seek offset')
                to_read = None
            else:
                if whence == 0:
                    if offset < 0:
                        raise ValueError('negative seek offset')
                    dest = offset
                else:
                    pos = self._seek_wrapper__pos
                    if pos < offset:
                        raise ValueError('seek to before start of file')
                    dest = pos + offset
                end = len_of_seekable(self._seek_wrapper__cache)
                to_read = dest - end
                if to_read < 0:
                    to_read = 0
            if to_read != 0:
                self._seek_wrapper__cache.seek(0, 2)
                if to_read is None:
                    assert whence == 2
                    self._seek_wrapper__cache.write(self.wrapped.read())
                    self.read_complete = True
                    self._seek_wrapper__pos = self._seek_wrapper__cache.tell() - offset
                else:
                    data = self.wrapped.read(to_read)
                    if not data:
                        self.read_complete = True
                    else:
                        self._seek_wrapper__cache.write(data)
                    self._seek_wrapper__pos = dest
            else:
                self._seek_wrapper__pos = dest

    def tell(self):
        return self._seek_wrapper__pos

    def __copy__(self):
        cpy = self.__class__(self.wrapped)
        cpy._seek_wrapper__cache = self._seek_wrapper__cache
        cpy._seek_wrapper__read_complete_state = self._seek_wrapper__read_complete_state
        cpy._seek_wrapper__is_closed_state = self._seek_wrapper__is_closed_state
        return cpy

    def get_data--- This code section failed: ---

 L. 178         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _seek_wrapper__pos
                4  STORE_FAST               'pos'

 L. 179         6  SETUP_FINALLY        32  'to 32'

 L. 180         8  LOAD_FAST                'self'
               10  LOAD_METHOD              seek
               12  LOAD_CONST               0
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 181        18  LOAD_FAST                'self'
               20  LOAD_METHOD              read
               22  LOAD_CONST               -1
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  CALL_FINALLY         32  'to 32'
               30  RETURN_VALUE     
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM_FINALLY     6  '6'

 L. 183        32  LOAD_FAST                'pos'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _seek_wrapper__pos
               38  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 28

    def read(self, size=-1):
        pos = self._seek_wrapper__pos
        end = len_of_seekable(self._seek_wrapper__cache)
        available = end - pos
        if size <= available:
            if size != -1:
                self._seek_wrapper__cache.seek(pos)
                self._seek_wrapper__pos = pos + size
                return self._seek_wrapper__cache.read(size)
        else:
            self._seek_wrapper__cache.seek(0, 2)
            if size == -1:
                self._seek_wrapper__cache.write(self.wrapped.read())
                self.read_complete = True
            else:
                to_read = size - available
            if not to_read > 0:
                raise AssertionError
            else:
                data = self.wrapped.read(to_read)
                if not data:
                    self.read_complete = True
                else:
                    self._seek_wrapper__cache.write(data)
        self._seek_wrapper__cache.seek(pos)
        data = self._seek_wrapper__cache.read(size)
        self._seek_wrapper__pos = self._seek_wrapper__cache.tell()
        assert self._seek_wrapper__pos == pos + len(data)
        return data

    def readline(self, size=-1):
        if not self._seek_wrapper__have_readline:
            raise NotImplementedError('no readline method on wrapped object')
        else:
            pos = self._seek_wrapper__pos
            self._seek_wrapper__cache.seek(0, 2)
            data = self.wrapped.readline()
            if not data:
                self.read_complete = True
            else:
                self._seek_wrapper__cache.write(data)
            self._seek_wrapper__cache.seek(pos)
            data = self._seek_wrapper__cache.readline()
            if size != -1:
                r = data[:size]
                self._seek_wrapper__pos = pos + size
            else:
                r = data
            self._seek_wrapper__pos = pos + len(data)
        return r

    def readlines(self, sizehint=-1):
        pos = self._seek_wrapper__pos
        self._seek_wrapper__cache.seek(0, 2)
        self._seek_wrapper__cache.write(self.wrapped.read())
        self.read_complete = True
        self._seek_wrapper__cache.seek(pos)
        data = self._seek_wrapper__cache.readlines(sizehint)
        self._seek_wrapper__pos = self._seek_wrapper__cache.tell()
        return data

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    next = __next__
    xreadlines = __iter__

    def __repr__(self):
        return '<%s at %s whose wrapped object = %r>' % (
         self.__class__.__name__, hex(abs(id(self))), self.wrapped)


class response_seek_wrapper(seek_wrapper):
    __doc__ = '\n    Supports copying response objects and setting response body data.\n\n    '

    def __init__(self, wrapped):
        seek_wrapper.__init__(self, wrapped)
        self._headers = self.wrapped.info()

    def __copy__(self):
        cpy = seek_wrapper.__copy__(self)
        cpy._headers = copy.copy(self.info())
        return cpy

    def info(self):
        return self._headers

    def geturl(self):
        return self.wrapped.geturl()

    def set_data(self, data):
        self.seek(0)
        self.read()
        self.close()
        cache = self._seek_wrapper__cache = BytesIO()
        cache.write(data)
        self.seek(0)


class eoffile:

    def read(self, size=-1):
        return b''

    def readline(self, size=-1):
        return b''

    def __iter__(self):
        return self

    def __next__(self):
        return b''

    next = __next__

    def close(self):
        pass


class eofresponse(eoffile):

    def __init__(self, url, headers, code, msg):
        self._url = url
        self._headers = headers
        self.code = code
        self.msg = msg

    def geturl(self):
        return self._url

    def info(self):
        return self._headers


class closeable_response:
    __doc__ = 'Avoids unnecessarily clobbering urllib.addinfourl methods on .close().\n\n    Only supports responses returned by mechanize.HTTPHandler.\n\n    After .close(), the following methods are supported:\n\n    .read()\n    .readline()\n    .info()\n    .geturl()\n    .__iter__()\n    .next()\n    .close()\n\n    and the following attributes are supported:\n\n    .code\n    .msg\n    .http_version\n\n    Also supports pickling (but the stdlib currently does something to prevent\n    it: http://python.org/sf/1144636).\n\n    '
    closeable_response = None

    def __init__(self, fp, headers, url, code=200, msg='OK', http_version=None):
        self._set_fp(fp)
        self._headers = headers
        self._url = url
        self.code = code
        self.msg = msg
        self.http_version = http_version

    def _set_fp(self, fp):
        self.fp = fp
        self.read = self.fp.read
        self.readline = self.fp.readline
        if hasattr(self.fp, 'readlines'):
            self.readlines = self.fp.readlines
        elif hasattr(self.fp, 'fileno'):
            self.fileno = self.fp.fileno
        else:
            self.fileno = lambda : None
        self.__iter__ = self.fp.__iter__
        self.next = partial(next, self.fp)

    def __repr__(self):
        return '<%s at %s whose fp = %r>' % (self.__class__.__name__,
         hex(abs(id(self))), self.fp)

    def info(self):
        return self._headers

    def getcode(self):
        return self.code

    def get_header_values(self, name):
        return self._headers.getheaders(name)

    def get_all_header_names(self, normalize=True):
        ans = []
        for line in self._headers.headers:
            h = line.partition(':')[0]
            if normalize:
                h = normalize_header_name(h)
            ans.append(h)
        else:
            return ans

    def __getitem__(self, name):
        return self._headers[name]

    def get(self, name, default):
        return self._headers.get(name)

    def geturl(self):
        return self._url

    def close(self):
        wrapped = self.fp
        wrapped.close()
        new_wrapped = eofresponse(self._url, self._headers, self.code, self.msg)
        self._set_fp(new_wrapped)


def test_response(data='test data', headers=[], url=None, code=200, msg='OK'):
    return make_response(data, headers, url, code, msg)


def test_html_response(data='test data', headers=[], url=None, code=200, msg='OK'):
    headers += [('Content-type', 'text/html')]
    return make_response(data, headers, url, code, msg)


def make_response(data, headers, url=None, code=200, msg='OK'):
    """Convenient factory for objects implementing response interface.

    data: string containing response body data
    headers: sequence of (name, value) pairs
    url: URL of response
    code: integer response code (e.g. 200)
    msg: string response code message (e.g. "OK")

    """
    mime_headers = make_headers(headers)
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    r = closeable_response(BytesIO(data), mime_headers, url, code, msg)
    return response_seek_wrapper(r)


def make_headers(headers):
    """
    headers: sequence of (name, value) pairs
    """
    hdr_text = []
    for name_value in headers:
        hdr_text.append('%s: %s' % name_value)
    else:
        ans = '\n'.join(hdr_text)
        if not isinstance(ans, bytes):
            ans = ans.encode('iso-8859-1')
        return create_response_info(BytesIO(ans))


def get_seek_wrapper_class(response):
    if isinstance(response, HTTPError):
        if (isinstance(response, seek_wrapper) or response.__class__.__module__) == '__builtin__':
            exc_class_name = response.__class__.__name__
        else:
            exc_class_name = '%s.%s' % (response.__class__.__module__,
             response.__class__.__name__)

        class httperror_seek_wrapper(response_seek_wrapper):
            _exc_class_name = exc_class_name

            def __init__(self, wrapped):
                response_seek_wrapper.__init__(self, wrapped)
                self.hdrs = wrapped.info()
                self.filename = wrapped.geturl()

            def __repr__(self):
                return '<%s (%s instance) at %s whose wrapped object = %r>' % (
                 self.__class__.__name__, self._exc_class_name,
                 hex(abs(id(self))), self.wrapped)

        wrapper_class = httperror_seek_wrapper
    else:
        wrapper_class = response_seek_wrapper
    return wrapper_class


def needs_seek_wrapper(obj):
    return not isinstance(obj, seek_wrapper) and (hasattr(obj, 'seek') or isinstance(obj, HTTPError) or not hasattr(obj, 'get_data'))


def seek_wrapped_response(response):
    """Return a copy of response that supports seekable response interface.

    Accepts responses from both mechanize and urllib2 handlers.

    Copes with both ordinary response instances and HTTPError instances (which
    can't be simply wrapped due to the requirement of preserving the exception
    base class).
    """
    if needs_seek_wrapper(response):
        wrapper_class = get_seek_wrapper_class(response)
        response = wrapper_class(response)
    assert hasattr(response, 'get_data')
    return response


def upgrade_response(response):
    """Return a copy of response that supports Browser response interface.

    Browser response interface is that of "seekable responses"
    (response_seek_wrapper), plus the requirement that responses must be
    useable after .close() (closeable_response).

    Accepts responses from both mechanize and urllib2 handlers.

    Copes with both ordinary response instances and HTTPError instances (which
    can't be simply wrapped due to the requirement of preserving the exception
    base class).
    """
    wrapper_class = get_seek_wrapper_class(response)
    if hasattr(response, 'closeable_response'):
        if needs_seek_wrapper(response):
            response = wrapper_class(response)
        assert hasattr(response, 'get_data')
        return copy.copy(response)
    try:
        code = response.code
    except AttributeError:
        code = None
    else:
        try:
            msg = response.msg
        except AttributeError:
            msg = None
        else:
            data = None
            get_data = getattr(response, 'get_data', None)
            if get_data:
                data = get_data()
            response = closeable_response(response.fp, response.info(), response.geturl(), code, msg)
            response = wrapper_class(response)
            if data:
                response.set_data(data)
            return response