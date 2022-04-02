# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_http.py
"""HTTP related handlers.

Note that some other HTTP handlers live in more specific modules: _auth.py,
_gzip.py, etc.

Copyright 2002-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""
from __future__ import absolute_import
import logging, socket, time
from io import BytesIO
from . import _rfc3986, _sockettimeout
from ._headersutil import is_html
from ._request import Request
from ._response import response_seek_wrapper
from ._urllib2_fork import BaseHandler, HTTPError
from ._equiv import HTTPEquivParser
from .polyglot import create_response_info, RobotFileParser, is_py2, as_unicode
debug = logging.getLogger('mechanize').debug
debug_robots = logging.getLogger('mechanize.robots').debug

def parse_head(fileobj):
    """Return a list of key, value pairs."""
    p = HTTPEquivParser(fileobj.read(4096))
    return p()


class HTTPEquivProcessor(BaseHandler):
    __doc__ = 'Append META HTTP-EQUIV headers to regular HTTP headers.'
    handler_order = 300

    def http_response(self, request, response):
        if not hasattr(response, 'seek'):
            response = response_seek_wrapper(response)
        http_message = response.info()
        url = response.geturl()
        ct_hdrs = http_message.getheaders('content-type')
        if is_html(ct_hdrs, url, True):
            try:
                try:
                    html_headers = parse_head(response)
                finally:
                    response.seek(0)

            except Exception:
                pass
            else:
                for hdr, val in html_headers:
                    if is_py2:
                        http_message.dict[hdr.lower()] = val
                        text = hdr + b': ' + val
                        for line in text.split(b'\n'):
                            http_message.headers.append(line + b'\n')

                    else:
                        hdr = hdr.decode('iso-8859-1')
                        http_message[hdr] = val.decode('iso-8859-1')

            return response

    https_response = http_response


class MechanizeRobotFileParser(RobotFileParser):

    def __init__(self, url='', opener=None):
        RobotFileParser.__init__(self, url)
        self._opener = opener
        self._timeout = _sockettimeout._GLOBAL_DEFAULT_TIMEOUT

    def set_opener(self, opener=None):
        from . import _opener
        if opener is None:
            opener = _opener.OpenerDirector()
        self._opener = opener

    def set_timeout(self, timeout):
        self._timeout = timeout

    def read--- This code section failed: ---

 L.  93         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _opener
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  94        10  LOAD_FAST                'self'
               12  LOAD_METHOD              set_opener
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L.  95        18  LOAD_GLOBAL              Request
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                url
               24  LOAD_CONST               True
               26  LOAD_CONST               False

 L.  96        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _timeout

 L.  95        32  LOAD_CONST               ('unverifiable', 'visit', 'timeout')
               34  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               36  STORE_FAST               'req'

 L.  97        38  SETUP_FINALLY        56  'to 56'

 L.  98        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _opener
               44  LOAD_METHOD              open
               46  LOAD_FAST                'req'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'f'
               52  POP_BLOCK        
               54  JUMP_FORWARD        158  'to 158'
             56_0  COME_FROM_FINALLY    38  '38'

 L.  99        56  DUP_TOP          
               58  LOAD_GLOBAL              HTTPError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    92  'to 92'
               64  POP_TOP          
               66  STORE_FAST               'err'
               68  POP_TOP          
               70  SETUP_FINALLY        80  'to 80'

 L. 100        72  LOAD_FAST                'err'
               74  STORE_FAST               'f'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_FINALLY    70  '70'
               80  LOAD_CONST               None
               82  STORE_FAST               'err'
               84  DELETE_FAST              'err'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD        158  'to 158'
             92_0  COME_FROM            62  '62'

 L. 101        92  DUP_TOP          
               94  LOAD_GLOBAL              IOError
               96  LOAD_GLOBAL              socket
               98  LOAD_ATTR                error
              100  LOAD_GLOBAL              OSError
              102  BUILD_TUPLE_3         3 
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   156  'to 156'
              108  POP_TOP          
              110  STORE_FAST               'exc'
              112  POP_TOP          
              114  SETUP_FINALLY       144  'to 144'

 L. 102       116  LOAD_GLOBAL              debug_robots
              118  LOAD_STR                 'ignoring error opening %r: %s'

 L. 103       120  LOAD_FAST                'self'
              122  LOAD_ATTR                url
              124  LOAD_FAST                'exc'
              126  BUILD_TUPLE_2         2 

 L. 102       128  BINARY_MODULO    
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          

 L. 104       134  POP_BLOCK        
              136  POP_EXCEPT       
              138  CALL_FINALLY        144  'to 144'
              140  LOAD_CONST               None
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM_FINALLY   114  '114'
              144  LOAD_CONST               None
              146  STORE_FAST               'exc'
              148  DELETE_FAST              'exc'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           106  '106'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM            90  '90'
            158_2  COME_FROM            54  '54'

 L. 105       158  BUILD_LIST_0          0 
              160  STORE_FAST               'lines'

 L. 106       162  LOAD_FAST                'f'
              164  LOAD_METHOD              readline
              166  CALL_METHOD_0         0  ''
              168  STORE_FAST               'line'
            170_0  COME_FROM           196  '196'

 L. 107       170  LOAD_FAST                'line'
              172  POP_JUMP_IF_FALSE   198  'to 198'

 L. 108       174  LOAD_FAST                'lines'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'line'
              180  LOAD_METHOD              strip
              182  CALL_METHOD_0         0  ''
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 109       188  LOAD_FAST                'f'
              190  LOAD_METHOD              readline
              192  CALL_METHOD_0         0  ''
              194  STORE_FAST               'line'
              196  JUMP_BACK           170  'to 170'
            198_0  COME_FROM           172  '172'

 L. 110       198  LOAD_FAST                'f'
              200  LOAD_ATTR                code
              202  STORE_FAST               'status'

 L. 111       204  LOAD_FAST                'status'
              206  LOAD_CONST               401
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_TRUE    220  'to 220'
              212  LOAD_FAST                'status'
              214  LOAD_CONST               403
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   236  'to 236'
            220_0  COME_FROM           210  '210'

 L. 112       220  LOAD_CONST               True
              222  LOAD_FAST                'self'
              224  STORE_ATTR               disallow_all

 L. 113       226  LOAD_GLOBAL              debug_robots
              228  LOAD_STR                 'disallow all'
              230  CALL_FUNCTION_1       1  ''
              232  POP_TOP          
              234  JUMP_FORWARD        320  'to 320'
            236_0  COME_FROM           218  '218'

 L. 114       236  LOAD_FAST                'status'
              238  LOAD_CONST               400
              240  COMPARE_OP               >=
          242_244  POP_JUMP_IF_FALSE   262  'to 262'

 L. 115       246  LOAD_CONST               True
              248  LOAD_FAST                'self'
              250  STORE_ATTR               allow_all

 L. 116       252  LOAD_GLOBAL              debug_robots
              254  LOAD_STR                 'allow all'
              256  CALL_FUNCTION_1       1  ''
              258  POP_TOP          
              260  JUMP_FORWARD        320  'to 320'
            262_0  COME_FROM           242  '242'

 L. 117       262  LOAD_FAST                'status'
              264  LOAD_CONST               200
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   320  'to 320'
              272  LOAD_FAST                'lines'
          274_276  POP_JUMP_IF_FALSE   320  'to 320'

 L. 118       278  LOAD_GLOBAL              debug_robots
              280  LOAD_STR                 'parse lines'
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          

 L. 119       286  LOAD_GLOBAL              is_py2
          288_290  POP_JUMP_IF_FALSE   304  'to 304'

 L. 120       292  LOAD_FAST                'self'
              294  LOAD_METHOD              parse
              296  LOAD_FAST                'lines'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          
              302  JUMP_FORWARD        320  'to 320'
            304_0  COME_FROM           288  '288'

 L. 122       304  LOAD_FAST                'self'
              306  LOAD_METHOD              parse
              308  LOAD_GLOBAL              map
              310  LOAD_GLOBAL              as_unicode
              312  LOAD_FAST                'lines'
              314  CALL_FUNCTION_2       2  ''
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
            320_0  COME_FROM           302  '302'
            320_1  COME_FROM           274  '274'
            320_2  COME_FROM           268  '268'
            320_3  COME_FROM           260  '260'
            320_4  COME_FROM           234  '234'

Parse error at or near `CALL_FINALLY' instruction at offset 138


class RobotExclusionError(HTTPError):

    def __init__(self, request, *args):
        (HTTPError.__init__)(self, *args)
        self.request = request


class HTTPRobotRulesProcessor(BaseHandler):
    handler_order = 800
    http_response_class = None

    def __init__(self, rfp_class=MechanizeRobotFileParser):
        self.rfp_class = rfp_class
        self.rfp = None
        self._host = None

    def __copy__(self):
        return self.__class__(self.rfp_class)

    def http_request(self, request):
        scheme = request.get_type()
        if scheme not in ('http', 'https'):
            return request
        if request.get_selector() == '/robots.txt':
            return request
        host = request.get_host()
        origin_req = getattr(request, '_origin_req', None)
        if origin_req is not None:
            if origin_req.get_selector() == '/robots.txt':
                if origin_req.get_host() == host:
                    return request
        if host != self._host:
            self.rfp = self.rfp_class()
            try:
                self.rfp.set_opener(self.parent)
            except AttributeError:
                debug('%r instance does not support set_opener' % self.rfp.__class__)
            else:
                self.rfp.set_url(scheme + '://' + host + '/robots.txt')
                self.rfp.set_timeout(request.timeout)
                self.rfp.read()
                self._host = host
            ua = request.get_header('User-agent', '')
            if self.rfp.can_fetch(ua, request.get_full_url()):
                return request
        factory = self.http_response_class or create_response_info
        msg = b'request disallowed by robots.txt'
        raise RobotExclusionError(request, request.get_full_url(), 403, msg, factory(BytesIO()), BytesIO(msg))

    https_request = http_request


class HTTPRefererProcessor(BaseHandler):
    __doc__ = "Add Referer header to requests.\n\n    This only makes sense if you use each RefererProcessor for a single\n    chain of requests only (so, for example, if you use a single\n    HTTPRefererProcessor to fetch a series of URLs extracted from a single\n    page, this will break).\n\n    There's a proper implementation of this in mechanize.Browser.\n\n    "

    def __init__(self):
        self.referer = None

    def http_request(self, request):
        if self.referer is not None:
            if not request.has_header('Referer'):
                request.add_unredirected_header('Referer', self.referer)
            return request

    def http_response(self, request, response):
        self.referer = response.geturl()
        return response

    https_request = http_request
    https_response = http_response


def clean_refresh_url(url):
    if not (url.startswith('"') and url.endswith('"')):
        if not url.startswith("'") or url.endswith("'"):
            url = url[1:-1]
        return _rfc3986.clean_url(url, 'utf-8')


def parse_refresh_header(refresh):
    """
    >>> parse_refresh_header("1; url=http://example.com/")
    (1.0, 'http://example.com/')
    >>> parse_refresh_header("1; url='http://example.com/'")
    (1.0, 'http://example.com/')
    >>> parse_refresh_header("1")
    (1.0, None)
    >>> parse_refresh_header("blah")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: invalid literal for float(): blah

    """
    ii = refresh.find(';')
    if ii != -1:
        pause, newurl_spec = float(refresh[:ii]), refresh[ii + 1:]
        jj = newurl_spec.find('=')
        key = None
        if jj != -1:
            key, newurl = newurl_spec[:jj], newurl_spec[jj + 1:]
            newurl = clean_refresh_url(newurl)
        if key is None or key.strip().lower() != 'url':
            raise ValueError()
    else:
        pause, newurl = float(refresh), None
    return (pause, newurl)


class HTTPRefreshProcessor(BaseHandler):
    __doc__ = 'Perform HTTP Refresh redirections.\n\n    Note that if a non-200 HTTP code has occurred (for example, a 30x\n    redirect), this processor will do nothing.\n\n    By default, only zero-time Refresh headers are redirected.  Use the\n    max_time attribute / constructor argument to allow Refresh with longer\n    pauses.  Use the honor_time attribute / constructor argument to control\n    whether the requested pause is honoured (with a time.sleep()) or\n    skipped in favour of immediate redirection.\n\n    Public attributes:\n\n    max_time: see above\n    honor_time: see above\n\n    '
    handler_order = 1000

    def __init__(self, max_time=0, honor_time=True):
        self.max_time = max_time
        self.honor_time = honor_time
        self._sleep = time.sleep

    def __copy__(self):
        return self.__class__(self.max_time, self.honor_time)

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()
        if not code == 200 or 'refresh' in hdrs:
            refresh = hdrs.getheaders('refresh')[0]
            try:
                pause, newurl = parse_refresh_header(refresh)
            except ValueError:
                debug('bad Refresh header: %r' % refresh)
                return response
            else:
                if newurl is None:
                    newurl = response.geturl()
                if self.max_time is None or pause <= self.max_time:
                    if pause > 0.001:
                        if self.honor_time:
                            self._sleep(pause)
                    hdrs['location'] = newurl
                    response = self.parent.error('http', request, response, 'refresh', msg, hdrs)
                else:
                    debug('Refresh header ignored: %r' % refresh)
            return response

    https_response = http_response