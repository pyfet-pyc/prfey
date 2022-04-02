# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_mechanize.py
"""Stateful programmatic WWW navigation, after Perl's WWW::Mechanize.

Copyright 2003-2006 John J. Lee <jjl@pobox.com>
Copyright 2003 Andy Lester (original Perl code)

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""
from __future__ import absolute_import
import copy, os, re
from . import _request, _response, _rfc3986, _sockettimeout, _urllib2_fork
from ._clientcookie import Cookie
from ._headersutil import normalize_header_name
from ._html import Factory
from ._useragent import UserAgentBase
from .polyglot import pathname2url, HTTPError, is_string, iteritems
from ._response import make_response

class BrowserStateError(Exception):
    pass


class LinkNotFoundError(Exception):
    pass


class FormNotFoundError(Exception):
    pass


def sanepathname2url(path):
    urlpath = pathname2url(path)
    if os.name == 'nt':
        if urlpath.startswith('///'):
            urlpath = urlpath[2:]
    return urlpath


class History:
    __doc__ = '\n\n    Though this will become public, the implied interface is not yet stable.\n\n    '

    def __init__(self):
        self._history = []

    def add(self, request, response):
        self._history.append((request, response))

    def back(self, n, _response):
        response = _response
        while not n > 0:
            if response is None:
                try:
                    request, response = self._history.pop()
                except IndexError:
                    raise BrowserStateError('already at start of history')
                else:
                    n -= 1

        return (
         request, response)

    def clear(self):
        del self._history[:]

    def close(self):
        for request, response in self._history:
            if response is not None:
                response.close()
        else:
            del self._history[:]

    def __copy__(self):
        ans = self.__class__()
        ans._history = self._history[:]
        return ans


class HTTPRefererProcessor(_urllib2_fork.BaseHandler):

    def http_request(self, request):
        if hasattr(request, 'redirect_dict'):
            request = self.parent._add_referer_header(request,
              origin_request=False)
        return request

    https_request = http_request


class Browser(UserAgentBase):
    __doc__ = 'Browser-like class with support for history, forms and links.\n\n    :class:`BrowserStateError` is raised whenever the browser is in the wrong\n    state to complete the requested operation - e.g., when :meth:`back()` is\n    called when the browser history is empty, or when :meth:`follow_link()` is\n    called when the current response does not contain HTML data.\n\n    Public attributes:\n\n    request: current request (:class:`mechanize.Request`)\n\n    form: currently selected form (see :meth:`select_form()`)\n\n    :param history: object implementing the :class:`mechanize.History`\n                    interface.  Note this interface is still experimental\n                    and may change in future. This object is owned\n                    by the browser instance and must not be shared\n                    among browsers.\n    :param request_class: Request class to use. Defaults to\n                            :class:`mechanize.Request`\n    :param content_parser: A function that is responsible for parsing\n        received html/xhtml content. See the builtin\n        :func:`mechanize._html.content_parser()` function for details\n        on the interface this function must support.\n    :param factory_class: HTML Factory class to use. Defaults to\n                            :class:`mechanize.Factory`\n\n    '
    handler_classes = copy.copy(UserAgentBase.handler_classes)
    handler_classes['_referer'] = HTTPRefererProcessor
    default_features = copy.copy(UserAgentBase.default_features)
    default_features.append('_referer')

    def __init__(self, history=None, request_class=None, content_parser=None, factory_class=Factory, allow_xhtml=False):
        """
        Only named arguments should be passed to this constructor.

        """
        self._handle_referer = True
        if history is None:
            history = History()
        self._history = history
        if request_class is None:
            request_class = _request.Request
        factory = factory_class(allow_xhtml=allow_xhtml)
        factory.set_request_class(request_class)
        if content_parser is not None:
            factory.set_content_parser(content_parser)
        self._factory = factory
        self.request_class = request_class
        self.request = None
        self._set_response(None, False)
        UserAgentBase.__init__(self)

    def __copy__(self):
        """
        Clone this browser instance. The clone will share the same, thread-safe
        cookie jar, and have all the same handlers/settings, but will not share
        any other state, making it safe to use in another thread.
        """
        ans = self.__class__()
        self._copy_state(ans)
        ans._handle_referer = self._handle_referer
        for attr in ('_response_type_finder', '_encoding_finder', '_content_parser'):
            setattr(ans._factory, attr, getattr(self._factory, attr))
        else:
            ans.request_class = self.request_class
            ans._history = copy.copy(self._history)
            return ans

    def close(self):
        UserAgentBase.close(self)
        if self._response is not None:
            self._response.close()
        if self._history is not None:
            self._history.close()
            self._history = None
        self.form = None
        self.request = self._response = None
        self.request = self.response = self.set_response = None
        self.geturl = self.reload = self.back = None
        self.clear_history = self.set_cookie = self.links = self.forms = None
        self.viewing_html = self.encoding = self.title = None
        self.select_form = self.click = self.submit = self.click_link = None
        self.follow_link = self.find_link = None

    def set_handle_referer(self, handle):
        """Set whether to add Referer header to each request."""
        self._set_handler('_referer', handle)
        self._handle_referer = bool(handle)

    def _add_referer_header(self, request, origin_request=True):
        if self.request is None:
            return request
            scheme = request.get_type()
            original_scheme = self.request.get_type()
            if scheme not in ('http', 'https'):
                return request
            if not origin_request:
                if not self.request.has_header('Referer'):
                    return request
        elif self._handle_referer:
            if original_scheme in ('http', 'https'):
                parts = original_scheme == 'https' and scheme != 'https' or _rfc3986.urlsplit(self.request.get_full_url())
                parts = parts[:-1] + (None, )
                referer = _rfc3986.urlunsplit(parts)
                request.add_unredirected_header('Referer', referer)
        return request

    def open_novisit(self, url_or_request, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        """Open a URL without visiting it.

        Browser state (including request, response, history, forms and links)
        is left unchanged by calling this function.

        The interface is the same as for :meth:`open()`.

        This is useful for things like fetching images.

        See also :meth:`retrieve()`

        """
        return self._mech_open(url_or_request,
          data, visit=False, timeout=timeout)

    def open(self, url_or_request, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        """
        Open a URL. Loads the page so that you can subsequently use
        :meth:`forms()`, :meth:`links()`, etc. on it.

        :param url_or_request: Either a URL or a :class:`mechanize.Request`
        :param dict data: data to send with a POST request
        :param timeout: Timeout in seconds
        :return: A :class:`mechanize.Response` object
        """
        return self._mech_open(url_or_request, data, timeout=timeout)

    def _mech_open(self, url, data=None, update_history=True, visit=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        try:
            url.get_full_url
        except AttributeError:
            scheme, authority = _rfc3986.urlsplit(url)[:2]
            if scheme is None:
                if self._response is None:
                    raise BrowserStateError("can't fetch relative reference: not viewing any document")
                url = _rfc3986.urljoin(self._response.geturl(), url)
        else:
            request = self._request(url, data, visit, timeout)
            visit = request.visit
            if visit is None:
                visit = True
            if visit:
                self._visit_request(request, update_history)
            success = True
            try:
                response = UserAgentBase.open(self, request, data)
            except HTTPError as error:
                try:
                    success = False
                    if error.fp is None:
                        raise
                    response = error
                finally:
                    error = None
                    del error

            else:
                if visit:
                    self._set_response(response, False)
                    response = copy.copy(self._response)
                else:
                    if response is not None:
                        response = _response.upgrade_response(response)
                    if not success:
                        raise response
                    return response

    def __str__(self):
        text = []
        text.append('<%s ' % self.__class__.__name__)
        if self._response:
            text.append('visiting %s' % self._response.geturl())
        else:
            text.append('(not visiting a URL)')
        if self.form:
            text.append('\n selected form:\n %s\n' % str(self.form))
        text.append('>')
        return ''.join(text)

    def response(self):
        """Return a copy of the current response.

        The returned object has the same interface as the object returned by
        :meth:`.open()`

        """
        return copy.copy(self._response)

    def open_local_file(self, filename):
        path = sanepathname2url(os.path.abspath(filename))
        url = 'file://' + path
        return self.open(url)

    def set_response(self, response):
        """Replace current response with (a copy of) response.

        response may be None.

        This is intended mostly for HTML-preprocessing.
        """
        self._set_response(response, True)

    def _set_response(self, response, close_current):
        if (response is None or hasattr)(response, 'info'):
            if not (hasattr(response, 'geturl') and hasattr(response, 'read')):
                raise ValueError('not a response object')
        else:
            self.form = None
            if response is not None:
                response = _response.upgrade_response(response)
            if close_current and self._response is not None:
                self._response.close()
        self._response = response
        self._factory.set_response(response)

    def visit_response(self, response, request=None):
        """Visit the response, as if it had been :meth:`open()` ed.

        Unlike :meth:`set_response()`, this updates history rather than
        replacing the current response.
        """
        if request is None:
            request = _request.Request(response.geturl())
        self._visit_request(request, True)
        self._set_response(response, False)

    def _visit_request(self, request, update_history):
        if self._response is not None:
            self._response.close()
        if self.request is not None:
            if update_history:
                self._history.add(self.request, self._response)
        self._response = None
        self.request = request

    def set_html(self, html, url='http://example.com/'):
        """Set the response to dummy with given HTML, and URL if given.

        Allows you to then parse that HTML, especially to extract forms
        information. If no URL was given then the default is "example.com".
        """
        response = make_response(html, [('Content-type', 'text/html')], url)
        self._set_response(response, True)

    def geturl(self):
        """Get URL of current document."""
        if self._response is None:
            raise BrowserStateError('not viewing any document')
        return self._response.geturl()

    def reload(self):
        """Reload current document, and return response object."""
        if self.request is None:
            raise BrowserStateError('no URL has yet been .open()ed')
        if self._response is not None:
            self._response.close()
        return self._mech_open((self.request), update_history=False)

    def back(self, n=1):
        """Go back n steps in history, and return response object.

        n: go back this number of steps (default 1 step)

        """
        if self._response is not None:
            self._response.close()
        else:
            self.request, response = self._history.back(n, self._response)
            self.set_response(response)
            return response.read_complete or self.reload()
        return copy.copy(response)

    def clear_history(self):
        self._history.clear()

    def set_cookie(self, cookie_string):
        """Set a cookie.

        Note that it is NOT necessary to call this method under ordinary
        circumstances: cookie handling is normally entirely automatic.  The
        intended use case is rather to simulate the setting of a cookie by
        client script in a web page (e.g. JavaScript).  In that case, use of
        this method is necessary because mechanize currently does not support
        JavaScript, VBScript, etc.

        The cookie is added in the same way as if it had arrived with the
        current response, as a result of the current request.  This means that,
        for example, if it is not appropriate to set the cookie based on the
        current request, no cookie will be set.

        The cookie will be returned automatically with subsequent responses
        made by the Browser instance whenever that's appropriate.

        cookie_string should be a valid value of the Set-Cookie header.

        For example:

        .. code-block:: python

            browser.set_cookie(
                "sid=abcdef; expires=Wednesday, 09-Nov-06 23:12:40 GMT")

        Currently, this method does not allow for adding RFC 2986 cookies.
        This limitation will be lifted if anybody requests it.

        See also :meth:`set_simple_cookie()` for an easier way to set cookies
        without needing to create a Set-Cookie header string.
        """
        if self._response is None:
            raise BrowserStateError('not viewing any document')
        if self.request.get_type() not in ('http', 'https'):
            raise BrowserStateError("can't set cookie for non-HTTP/HTTPS transactions")
        cookiejar = self._ua_handlers['_cookies'].cookiejar
        response = self.response()
        headers = response.info()
        headers['Set-cookie'] = cookie_string
        cookiejar.extract_cookies(response, self.request)

    def set_simple_cookie(self, name, value, domain, path='/'):
        """
        Similar to :meth:`set_cookie()` except that instead of using a
        cookie string, you simply specify the `name`, `value`, `domain`
        and optionally the `path`.
        The created cookie will never expire. For example:

        .. code-block:: python

            browser.set_simple_cookie('some_key', 'some_value', '.example.com',
                                      path='/some-page')
        """
        self.cookiejar.set_cookie(Cookie(0, name, value, None, False, domain, True, False, path, True, False, None, False, None, None, None))

    @property
    def cookiejar--- This code section failed: ---

 L. 490         0  SETUP_FINALLY        16  'to 16'

 L. 491         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _ua_handlers
                6  LOAD_STR                 '_cookies'
                8  BINARY_SUBSCR    
               10  LOAD_ATTR                cookiejar
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 492        16  DUP_TOP          
               18  LOAD_GLOBAL              Exception
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 493        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

Parse error at or near `POP_TOP' instruction at offset 26

    def set_header(self, header, value=None):
        """
        Convenience method to set a header value in `self.addheaders`
        so that the header is sent out with all requests automatically.

        :param header: The header name, e.g. User-Agent
        :param value: The header value. If set to None the header is removed.
        """
        found = False
        header = normalize_header_name(header)
        q = header.lower()
        remove = []
        for i, (k, v) in enumerate(tuple(self.addheaders)):
            if k.lower() == q:
                if value:
                    self.addheaders[i] = (
                     header, value)
                    found = True
                else:
                    remove.append(i)
            if not found:
                self.addheaders.append((header, value))
            if remove:
                for i in reversed(remove):
                    del self.addheaders[i]

    def links(self, **kwds):
        """Return iterable over links (:class:`mechanize.Link` objects)."""
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        links = self._factory.links()
        if kwds:
            return (self._filter_links)(links, **kwds)
        return links

    def forms(self):
        """Return iterable over forms.

        The returned form objects implement the :class:`mechanize.HTMLForm`
        interface.

        """
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        return self._factory.forms()

    def global_form(self):
        """Return the global form object, or None if the factory implementation
        did not supply one.

        The "global" form object contains all controls that are not descendants
        of any FORM element.

        The returned form object implements the :class:`mechanize.HTMLForm`
        interface.

        This is a separate method since the global form is not regarded as part
        of the sequence of forms in the document -- mostly for
        backwards-compatibility.

        """
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        return self._factory.global_form

    def viewing_html(self):
        """Return whether the current response contains HTML data."""
        if self._response is None:
            raise BrowserStateError('not viewing any document')
        return self._factory.is_html

    def encoding(self):
        if self._response is None:
            raise BrowserStateError('not viewing any document')
        return self._factory.encoding

    def title(self):
        """ Return title, or None if there is no title element in the document. """
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        return self._factory.title

    def select_form--- This code section failed: ---

 L. 627         0  LOAD_FAST                'self'
                2  LOAD_METHOD              viewing_html
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 628         8  LOAD_GLOBAL              BrowserStateError
               10  LOAD_STR                 'not viewing HTML'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 629        16  LOAD_FAST                'name'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    52  'to 52'
               24  LOAD_FAST                'predicate'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    52  'to 52'
               32  LOAD_FAST                'nr'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  LOAD_FAST                'attrs'
               42  POP_JUMP_IF_TRUE     52  'to 52'

 L. 630        44  LOAD_GLOBAL              ValueError

 L. 631        46  LOAD_STR                 'at least one argument must be supplied to specify form'

 L. 630        48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'
             52_1  COME_FROM            38  '38'
             52_2  COME_FROM            30  '30'
             52_3  COME_FROM            22  '22'

 L. 633        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _factory
               56  LOAD_ATTR                global_form
               58  STORE_FAST               'global_form'

 L. 634        60  LOAD_FAST                'nr'
               62  LOAD_CONST               None
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE   102  'to 102'
               68  LOAD_FAST                'name'
               70  LOAD_CONST               None
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   102  'to 102'
               76  LOAD_FAST                'predicate'
               78  LOAD_CONST               None
               80  COMPARE_OP               is-not
               82  POP_JUMP_IF_FALSE   102  'to 102'
               84  LOAD_FAST                'predicate'

 L. 635        86  LOAD_FAST                'global_form'

 L. 634        88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 636        92  LOAD_FAST                'global_form'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               form

 L. 637        98  LOAD_CONST               None
              100  RETURN_VALUE     
            102_0  COME_FROM            90  '90'
            102_1  COME_FROM            82  '82'
            102_2  COME_FROM            74  '74'
            102_3  COME_FROM            66  '66'

 L. 639       102  LOAD_CODE                <code_object attr_selector>
              104  LOAD_STR                 'Browser.select_form.<locals>.attr_selector'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  STORE_DEREF              'attr_selector'

 L. 645       110  LOAD_CLOSURE             'attr_selector'
              112  BUILD_TUPLE_1         1 
              114  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              116  LOAD_STR                 'Browser.select_form.<locals>.<dictcomp>'
              118  MAKE_FUNCTION_8          'closure'

 L. 646       120  LOAD_GLOBAL              iteritems
              122  LOAD_FAST                'attrs'
              124  CALL_FUNCTION_1       1  ''

 L. 645       126  GET_ITER         
              128  CALL_FUNCTION_1       1  ''
              130  STORE_DEREF              'attrsq'

 L. 648       132  LOAD_CLOSURE             'attrsq'
              134  BUILD_TUPLE_1         1 
              136  LOAD_CODE                <code_object form_attrs_match>
              138  LOAD_STR                 'Browser.select_form.<locals>.form_attrs_match'
              140  MAKE_FUNCTION_8          'closure'
              142  STORE_FAST               'form_attrs_match'

 L. 655       144  LOAD_FAST                'nr'
              146  STORE_FAST               'orig_nr'

 L. 656       148  LOAD_FAST                'self'
              150  LOAD_METHOD              forms
              152  CALL_METHOD_0         0  ''
              154  GET_ITER         
              156  FOR_ITER            242  'to 242'
              158  STORE_FAST               'form'

 L. 657       160  LOAD_FAST                'name'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE   180  'to 180'
              168  LOAD_FAST                'name'
              170  LOAD_FAST                'form'
              172  LOAD_ATTR                name
              174  COMPARE_OP               !=
              176  POP_JUMP_IF_FALSE   180  'to 180'

 L. 658       178  JUMP_BACK           156  'to 156'
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           166  '166'

 L. 659       180  LOAD_FAST                'predicate'
              182  LOAD_CONST               None
              184  COMPARE_OP               is-not
              186  POP_JUMP_IF_FALSE   198  'to 198'
              188  LOAD_FAST                'predicate'
              190  LOAD_FAST                'form'
              192  CALL_FUNCTION_1       1  ''
              194  POP_JUMP_IF_TRUE    198  'to 198'

 L. 660       196  JUMP_BACK           156  'to 156'
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           186  '186'

 L. 661       198  LOAD_FAST                'nr'
              200  POP_JUMP_IF_FALSE   212  'to 212'

 L. 662       202  LOAD_FAST                'nr'
              204  LOAD_CONST               1
              206  INPLACE_SUBTRACT 
              208  STORE_FAST               'nr'

 L. 663       210  JUMP_BACK           156  'to 156'
            212_0  COME_FROM           200  '200'

 L. 664       212  LOAD_FAST                'attrs'
              214  POP_JUMP_IF_FALSE   228  'to 228'
              216  LOAD_FAST                'form_attrs_match'
              218  LOAD_FAST                'form'
              220  LOAD_ATTR                attrs
              222  CALL_FUNCTION_1       1  ''
              224  POP_JUMP_IF_TRUE    228  'to 228'

 L. 665       226  JUMP_BACK           156  'to 156'
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           214  '214'

 L. 666       228  LOAD_FAST                'form'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               form

 L. 667       234  POP_TOP          
          236_238  BREAK_LOOP          384  'to 384'
              240  JUMP_BACK           156  'to 156'

 L. 670       242  BUILD_LIST_0          0 
              244  STORE_FAST               'description'

 L. 671       246  LOAD_FAST                'name'
              248  LOAD_CONST               None
              250  COMPARE_OP               is-not
          252_254  POP_JUMP_IF_FALSE   270  'to 270'

 L. 672       256  LOAD_FAST                'description'
              258  LOAD_METHOD              append
              260  LOAD_STR                 "name '%s'"
              262  LOAD_FAST                'name'
              264  BINARY_MODULO    
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
            270_0  COME_FROM           252  '252'

 L. 673       270  LOAD_FAST                'predicate'
              272  LOAD_CONST               None
              274  COMPARE_OP               is-not
          276_278  POP_JUMP_IF_FALSE   294  'to 294'

 L. 674       280  LOAD_FAST                'description'
              282  LOAD_METHOD              append
              284  LOAD_STR                 'predicate %s'
              286  LOAD_FAST                'predicate'
              288  BINARY_MODULO    
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          
            294_0  COME_FROM           276  '276'

 L. 675       294  LOAD_FAST                'orig_nr'
              296  LOAD_CONST               None
              298  COMPARE_OP               is-not
          300_302  POP_JUMP_IF_FALSE   318  'to 318'

 L. 676       304  LOAD_FAST                'description'
              306  LOAD_METHOD              append
              308  LOAD_STR                 'nr %d'
              310  LOAD_FAST                'orig_nr'
              312  BINARY_MODULO    
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
            318_0  COME_FROM           300  '300'

 L. 677       318  LOAD_FAST                'attrs'
          320_322  POP_JUMP_IF_FALSE   362  'to 362'

 L. 678       324  LOAD_GLOBAL              iteritems
              326  LOAD_FAST                'attrs'
              328  CALL_FUNCTION_1       1  ''
              330  GET_ITER         
              332  FOR_ITER            362  'to 362'
              334  UNPACK_SEQUENCE_2     2 
              336  STORE_FAST               'k'
              338  STORE_FAST               'v'

 L. 679       340  LOAD_FAST                'description'
              342  LOAD_METHOD              append
              344  LOAD_STR                 '%s = %r'
              346  LOAD_FAST                'k'
              348  LOAD_FAST                'v'
              350  BUILD_TUPLE_2         2 
              352  BINARY_MODULO    
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
          358_360  JUMP_BACK           332  'to 332'
            362_0  COME_FROM           320  '320'

 L. 680       362  LOAD_STR                 ', '
              364  LOAD_METHOD              join
              366  LOAD_FAST                'description'
              368  CALL_METHOD_1         1  ''
              370  STORE_FAST               'description'

 L. 681       372  LOAD_GLOBAL              FormNotFoundError
              374  LOAD_STR                 'no form matching '
              376  LOAD_FAST                'description'
              378  BINARY_ADD       
              380  CALL_FUNCTION_1       1  ''
              382  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 114

    def click(self, *args, **kwds):
        """See :meth:`mechanize.HTMLForm.click()` for documentation."""
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        request = (self.form.click)(*args, **kwds)
        return self._add_referer_header(request)

    def submit(self, *args, **kwds):
        """Submit current form.

        Arguments are as for :meth:`mechanize.HTMLForm.click()`.

        Return value is same as for :meth:`open()`.
        """
        return self.open((self.click)(*args, **kwds))

    def click_link(self, link=None, **kwds):
        """Find a link and return a Request object for it.

        Arguments are as for :meth:`find_link()`, except that a link may be
        supplied as the first argument.

        """
        if not self.viewing_html():
            raise BrowserStateError('not viewing HTML')
        elif not link:
            link = (self.find_link)(**kwds)
        else:
            if kwds:
                raise ValueError('either pass a Link, or keyword arguments, not both')
        request = self.request_class(link.absolute_url)
        return self._add_referer_header(request)

    def follow_link(self, link=None, **kwds):
        """Find a link and :meth:`open()` it.

        Arguments are as for :meth:`click_link()`.

        Return value is same as for :meth:`open()`.

        """
        return self.open((self.click_link)(link, **kwds))

    def find_link--- This code section failed: ---

 L. 785         0  SETUP_FINALLY        42  'to 42'

 L. 786         2  LOAD_GLOBAL              next
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              _filter_links

 L. 787         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _factory
               12  LOAD_METHOD              links
               14  CALL_METHOD_0         0  ''

 L. 787        16  LOAD_FAST                'text'

 L. 787        18  LOAD_FAST                'text_regex'

 L. 787        20  LOAD_FAST                'name'

 L. 787        22  LOAD_FAST                'name_regex'

 L. 787        24  LOAD_FAST                'url'

 L. 788        26  LOAD_FAST                'url_regex'

 L. 788        28  LOAD_FAST                'tag'

 L. 788        30  LOAD_FAST                'predicate'

 L. 788        32  LOAD_FAST                'nr'

 L. 786        34  CALL_METHOD_10       10  ''
               36  CALL_FUNCTION_1       1  ''
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 789        42  DUP_TOP          
               44  LOAD_GLOBAL              StopIteration
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    66  'to 66'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 790        56  LOAD_GLOBAL              LinkNotFoundError
               58  CALL_FUNCTION_0       0  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            48  '48'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'

Parse error at or near `POP_TOP' instruction at offset 52

    def __getattr__(self, name):
        form = self.__dict__.get('form')
        if form is None:
            raise AttributeError('%s instance has no attribute %s (perhaps you forgot to .select_form()?)' % (
             self.__class__, name))
        return getattr(form, name)

    def __getitem__(self, name):
        if self.form is None:
            raise BrowserStateError('No form selected')
        return self.form[name]

    def __setitem__(self, name, val):
        if self.form is None:
            raise BrowserStateError('No form selected')
        self.form[name] = val

    def _filter_links--- This code section failed: ---

 L. 822         0  LOAD_FAST                'self'
                2  LOAD_METHOD              viewing_html
                4  CALL_METHOD_0         0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L. 823         8  LOAD_GLOBAL              BrowserStateError
               10  LOAD_STR                 'not viewing HTML'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 825        16  LOAD_FAST                'nr'
               18  STORE_FAST               'orig_nr'

 L. 827        20  LOAD_FAST                'links'
               22  GET_ITER         
             24_0  COME_FROM           196  '196'
             24_1  COME_FROM           118  '118'
             24_2  COME_FROM            88  '88'
               24  FOR_ITER            278  'to 278'
               26  STORE_FAST               'link'

 L. 828        28  LOAD_FAST                'url'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  LOAD_FAST                'url'
               38  LOAD_FAST                'link'
               40  LOAD_ATTR                url
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    48  'to 48'

 L. 829        46  JUMP_BACK            24  'to 24'
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            34  '34'

 L. 830        48  LOAD_FAST                'url_regex'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE    72  'to 72'
               56  LOAD_GLOBAL              re
               58  LOAD_METHOD              search
               60  LOAD_FAST                'url_regex'
               62  LOAD_FAST                'link'
               64  LOAD_ATTR                url
               66  CALL_METHOD_2         2  ''
               68  POP_JUMP_IF_TRUE     72  'to 72'

 L. 831        70  JUMP_BACK            24  'to 24'
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            54  '54'

 L. 832        72  LOAD_FAST                'text'
               74  LOAD_CONST               None
               76  COMPARE_OP               is-not
               78  POP_JUMP_IF_FALSE   102  'to 102'
               80  LOAD_FAST                'link'
               82  LOAD_ATTR                text
               84  LOAD_CONST               None
               86  COMPARE_OP               is
               88  POP_JUMP_IF_TRUE     24  'to 24'
               90  LOAD_FAST                'text'
               92  LOAD_FAST                'link'
               94  LOAD_ATTR                text
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   102  'to 102'

 L. 833       100  JUMP_BACK            24  'to 24'
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            78  '78'

 L. 835       102  LOAD_FAST                'text_regex'
              104  LOAD_CONST               None
              106  COMPARE_OP               is-not

 L. 834       108  POP_JUMP_IF_FALSE   136  'to 136'

 L. 836       110  LOAD_FAST                'link'
              112  LOAD_ATTR                text
              114  LOAD_CONST               None
              116  COMPARE_OP               is

 L. 834       118  POP_JUMP_IF_TRUE     24  'to 24'

 L. 836       120  LOAD_GLOBAL              re
              122  LOAD_METHOD              search

 L. 837       124  LOAD_FAST                'text_regex'

 L. 837       126  LOAD_FAST                'link'
              128  LOAD_ATTR                text

 L. 836       130  CALL_METHOD_2         2  ''

 L. 834       132  POP_JUMP_IF_TRUE    136  'to 136'

 L. 838       134  JUMP_BACK            24  'to 24'
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           108  '108'

 L. 839       136  LOAD_FAST                'name'
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE   166  'to 166'
              144  LOAD_FAST                'name'
              146  LOAD_GLOBAL              dict
              148  LOAD_FAST                'link'
              150  LOAD_ATTR                attrs
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_METHOD              get
              156  LOAD_STR                 'name'
              158  CALL_METHOD_1         1  ''
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_FALSE   166  'to 166'

 L. 840       164  JUMP_BACK            24  'to 24'
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           142  '142'

 L. 841       166  LOAD_FAST                'name_regex'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   212  'to 212'

 L. 842       174  LOAD_GLOBAL              dict
              176  LOAD_FAST                'link'
              178  LOAD_ATTR                attrs
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_METHOD              get
              184  LOAD_STR                 'name'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'link_name'

 L. 843       190  LOAD_FAST                'link_name'
              192  LOAD_CONST               None
              194  COMPARE_OP               is
              196  POP_JUMP_IF_TRUE     24  'to 24'
              198  LOAD_GLOBAL              re
              200  LOAD_METHOD              search
              202  LOAD_FAST                'name_regex'
              204  LOAD_FAST                'link_name'
              206  CALL_METHOD_2         2  ''
              208  POP_JUMP_IF_TRUE    212  'to 212'

 L. 844       210  JUMP_BACK            24  'to 24'
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           172  '172'

 L. 845       212  LOAD_FAST                'tag'
              214  LOAD_CONST               None
              216  COMPARE_OP               is-not
              218  POP_JUMP_IF_FALSE   232  'to 232'
              220  LOAD_FAST                'tag'
              222  LOAD_FAST                'link'
              224  LOAD_ATTR                tag
              226  COMPARE_OP               !=
              228  POP_JUMP_IF_FALSE   232  'to 232'

 L. 846       230  JUMP_BACK            24  'to 24'
            232_0  COME_FROM           228  '228'
            232_1  COME_FROM           218  '218'

 L. 847       232  LOAD_FAST                'predicate'
              234  LOAD_CONST               None
              236  COMPARE_OP               is-not
              238  POP_JUMP_IF_FALSE   250  'to 250'
              240  LOAD_FAST                'predicate'
              242  LOAD_FAST                'link'
              244  CALL_FUNCTION_1       1  ''
              246  POP_JUMP_IF_TRUE    250  'to 250'

 L. 848       248  JUMP_BACK            24  'to 24'
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           238  '238'

 L. 849       250  LOAD_FAST                'nr'
          252_254  POP_JUMP_IF_FALSE   266  'to 266'

 L. 850       256  LOAD_FAST                'nr'
              258  LOAD_CONST               1
              260  INPLACE_SUBTRACT 
              262  STORE_FAST               'nr'

 L. 851       264  JUMP_BACK            24  'to 24'
            266_0  COME_FROM           252  '252'

 L. 852       266  LOAD_FAST                'link'
              268  YIELD_VALUE      
              270  POP_TOP          

 L. 853       272  LOAD_FAST                'orig_nr'
              274  STORE_FAST               'nr'
              276  JUMP_BACK            24  'to 24'

Parse error at or near `STORE_FAST' instruction at offset 274