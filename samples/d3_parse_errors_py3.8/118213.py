# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_html.py
from __future__ import absolute_import
import codecs, copy, re
from ._form import parse_forms
from ._headersutil import is_html as _is_html
from ._headersutil import split_header_words
from ._rfc3986 import clean_url, urljoin
from .polyglot import is_string
DEFAULT_ENCODING = 'utf-8'
_encoding_pats = ('<\\?[^<>]+encoding\\s*=\\s*[\\\'"](.*?)[\\\'"][^<>]*>', '<meta\\s+charset=[\'"]([-_a-z0-9]+)[\'"][^<>]*>(?:\\s*</meta>){0,1}',
                  '<meta\\s+?[^<>]*?content\\s*=\\s*[\'"][^\'"]*?charset=([-_a-z0-9]+)[^\'"]*?[\'"][^<>]*>(?:\\s*</meta>){0,1}')

def compile_pats(binary):
    for raw in _encoding_pats:
        if binary:
            raw = raw.encode('ascii')
        else:
            yield re.compile(raw, flags=(re.IGNORECASE))


class LazyEncodingPats(object):

    def __call__(self, binary=False):
        attr = 'binary_pats' if binary else 'unicode_pats'
        pats = getattr(self, attr, None)
        if pats is None:
            pats = tuple(compile_pats(binary))
            setattr(self, attr, pats)
        for pat in pats:
            yield pat


lazy_encoding_pats = LazyEncodingPats()

def find_declared_encoding(raw, limit=51200):
    prefix = raw[:limit]
    is_binary = isinstance(raw, bytes)
    for pat in lazy_encoding_pats(is_binary):
        m = pat.search(prefix)
        if m is not None:
            ans = m.group(1)
            if is_binary:
                ans = ans.decode('ascii', 'replace')
                return ans


def elem_text(elem):
    if elem.text:
        yield elem.text
    for child in elem:
        for text in elem_text(child):
            yield text
        else:
            if child.tail:
                yield child.tail


def iterlinks(root, base_url):
    link_tags = {'a':'href', 
     'area':'href',  'iframe':'src'}
    for tag in root.iter('*'):
        if not is_string(tag.tag):
            pass
        else:
            q = tag.tag.lower()
            attr = link_tags.get(q)
            if attr is not None:
                val = tag.get(attr)
                if val:
                    url = clean_url(val)
                    yield Link(base_url, url, compress_whitespace(''.join(elem_text(tag))), q, tag.items())
            else:
                if q == 'base':
                    href = tag.get('href')
                    if href:
                        base_url = href


def compress_whitespace(text):
    return re.sub('\\s+', ' ', text or '').strip()


def get_encoding_from_response--- This code section failed: ---

 L.  96         0  LOAD_FAST                'response'
                2  POP_JUMP_IF_FALSE   122  'to 122'

 L.  97         4  LOAD_FAST                'response'
                6  LOAD_METHOD              info
                8  CALL_METHOD_0         0  ''
               10  LOAD_METHOD              getheaders
               12  LOAD_STR                 'content-type'
               14  CALL_METHOD_1         1  ''
               16  GET_ITER         
             18_0  COME_FROM           120  '120'
               18  FOR_ITER            122  'to 122'
               20  STORE_FAST               'ct'

 L.  98        22  LOAD_GLOBAL              split_header_words
               24  LOAD_FAST                'ct'
               26  BUILD_LIST_1          1 
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  GET_ITER         
             36_0  COME_FROM           118  '118'
             36_1  COME_FROM           114  '114'
             36_2  COME_FROM           110  '110'
             36_3  COME_FROM            50  '50'
               36  FOR_ITER            120  'to 120'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'k'
               42  STORE_FAST               'v'

 L.  99        44  LOAD_FAST                'k'
               46  LOAD_STR                 'charset'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE_BACK    36  'to 36'

 L. 100        52  LOAD_FAST                'verify'
               54  POP_JUMP_IF_TRUE     68  'to 68'

 L. 101        56  LOAD_FAST                'v'
               58  ROT_TWO          
               60  POP_TOP          
               62  ROT_TWO          
               64  POP_TOP          
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'

 L. 102        68  SETUP_FINALLY        94  'to 94'

 L. 103        70  LOAD_GLOBAL              codecs
               72  LOAD_METHOD              lookup
               74  LOAD_FAST                'v'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 104        80  LOAD_FAST                'v'
               82  POP_BLOCK        
               84  ROT_TWO          
               86  POP_TOP          
               88  ROT_TWO          
               90  POP_TOP          
               92  RETURN_VALUE     
             94_0  COME_FROM_FINALLY    68  '68'

 L. 105        94  DUP_TOP          
               96  LOAD_GLOBAL              LookupError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   116  'to 116'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 106       108  POP_EXCEPT       
              110  JUMP_BACK            36  'to 36'
              112  POP_EXCEPT       
              114  JUMP_BACK            36  'to 36'
            116_0  COME_FROM           100  '100'
              116  END_FINALLY      
              118  JUMP_BACK            36  'to 36'
            120_0  COME_FROM            36  '36'
              120  JUMP_BACK            18  'to 18'
            122_0  COME_FROM            18  '18'
            122_1  COME_FROM             2  '2'

Parse error at or near `ROT_TWO' instruction at offset 84


class EncodingFinder:

    def __init__(self, default_encoding):
        self._default_encoding = default_encoding

    def encoding(self, response):
        return get_encoding_from_response(response) or self._default_encoding


class ResponseTypeFinder:

    def __init__(self, allow_xhtml):
        self._allow_xhtml = allow_xhtml

    def is_html(self, response, encoding):
        ct_hdrs = response.info().getheaders('content-type')
        url = response.geturl()
        return _is_html(ct_hdrs, url, self._allow_xhtml)


class Link:
    __doc__ = '\n    A link in a HTML document\n\n    :ivar absolute_url: The absolutized link URL\n    :ivar url: The link URL\n    :ivar base_url: The base URL against which this link is resolved\n    :ivar text: The link text\n    :ivar tag: The link tag name\n    :ivar attrs: The tag attributes\n\n    '

    def __init__(self, base_url, url, text, tag, attrs):
        assert None not in (url, tag, attrs)
        self.base_url = base_url
        self.absolute_url = urljoin(base_url, url)
        self.url, self.text, self.tag, self.attrs = (url, text, tag, attrs)
        self.text = self.text

    def __eq__--- This code section failed: ---

 L. 148         0  SETUP_FINALLY        70  'to 70'

 L. 149         2  LOAD_CONST               ('url', 'text', 'tag')
                4  GET_ITER         
              6_0  COME_FROM            38  '38'
              6_1  COME_FROM            28  '28'
                6  FOR_ITER             40  'to 40'
                8  STORE_FAST               'name'

 L. 150        10  LOAD_GLOBAL              getattr
               12  LOAD_FAST                'self'
               14  LOAD_FAST                'name'
               16  CALL_FUNCTION_2       2  ''
               18  LOAD_GLOBAL              getattr
               20  LOAD_FAST                'other'
               22  LOAD_FAST                'name'
               24  CALL_FUNCTION_2       2  ''
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE_BACK     6  'to 6'

 L. 151        30  POP_TOP          
               32  POP_BLOCK        
               34  LOAD_CONST               False
               36  RETURN_VALUE     
               38  JUMP_BACK             6  'to 6'
             40_0  COME_FROM             6  '6'

 L. 152        40  LOAD_GLOBAL              dict
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                attrs
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              dict
               50  LOAD_FAST                'other'
               52  LOAD_ATTR                attrs
               54  CALL_FUNCTION_1       1  ''
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 153        60  POP_BLOCK        
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM            58  '58'
               66  POP_BLOCK        
               68  JUMP_FORWARD         92  'to 92'
             70_0  COME_FROM_FINALLY     0  '0'

 L. 154        70  DUP_TOP          
               72  LOAD_GLOBAL              AttributeError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    90  'to 90'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 155        84  POP_EXCEPT       
               86  LOAD_CONST               False
               88  RETURN_VALUE     
             90_0  COME_FROM            76  '76'
               90  END_FINALLY      
             92_0  COME_FROM            68  '68'

 L. 156        92  LOAD_CONST               True
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 32

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Link(base_url=%r, url=%r, text=%r, tag=%r, attrs=%r)' % (
         self.base_url, self.url, self.text, self.tag, self.attrs)


def content_parser(data, url=None, response_info=None, transport_encoding=None, default_encoding=DEFAULT_ENCODING, is_html=True):
    """
    Parse data (a bytes object) into an etree representation such as
    :py:mod:`xml.etree.ElementTree` or `lxml.etree`

    :param bytes data: The data to parse
    :param url: The URL of the document being parsed or None
    :param response_info: Information about the document
        (contains all HTTP headers as :class:`HTTPMessage`)
    :param transport_encoding: The character encoding for the document being
        parsed as specified in the HTTP headers or None.
    :param default_encoding: The character encoding to use if no encoding
        could be detected and no transport_encoding is specified
    :param is_html: If the document is to be parsed as HTML.
    """
    if not is_html:
        return
    try:
        from html5_parser import parse
    except Exception:
        from html5lib import parse
        kw = {'namespaceHTMLElements': False}
        if transport_encoding:
            if isinstance(data, bytes):
                kw['transport_encoding'] = transport_encoding
        return parse(data, **kw)
    else:
        return parse(data, transport_encoding=transport_encoding)


def get_title(root):
    for title in root.iter('title'):
        text = compress_whitespace(title.text)
        if text:
            return text


lazy = object()

class Factory:
    __doc__ = 'Factory for forms, links, etc.\n\n    This interface may expand in future.\n\n    Public methods:\n\n    set_request_class(request_class)\n    set_response(response)\n    forms()\n    links()\n\n    Public attributes:\n\n    Note that accessing these attributes may raise ParseError.\n\n    encoding: string specifying the encoding of response if it contains a text\n     document (this value is left unspecified for documents that do not have\n     an encoding, e.g. an image file)\n    is_html: true if response contains an HTML document (XHTML may be\n     regarded as HTML too)\n    title: page title, or None if no title or not HTML\n    global_form: form object containing all controls that are not descendants\n     of any FORM element, or None if the forms_factory does not support\n     supplying a global form\n\n    '

    def __init__(self, default_encoding=DEFAULT_ENCODING, allow_xhtml=False):
        """

        Pass keyword arguments only.

        """
        self._encoding_finder = EncodingFinder(default_encoding)
        self.form_encoding = default_encoding
        self._response_type_finder = ResponseTypeFinder(allow_xhtml=allow_xhtml)
        self._content_parser = content_parser
        self._current_forms = self._current_links = self._current_title = lazy
        self._current_global_form = self._root = lazy
        self._raw_data = b''
        self.is_html, self.encoding = False, DEFAULT_ENCODING
        self.set_response(None)

    def set_content_parser(self, val):
        self._content_parser = val

    def set_request_class(self, request_class):
        """Set request class (mechanize.Request by default).

        HTMLForm instances returned by .forms() will return instances of this
        class when .click()ed.

        """
        self._request_class = request_class

    def set_response(self, response):
        """Set response.

        The response must either be None or implement the same interface as
        objects returned by mechanize.urlopen().

        """
        self._response = copy.copy(response)
        self._current_forms = self._current_links = self._current_title = lazy
        self._current_global_form = self._root = lazy
        self.encoding = self._encoding_finder.encoding(self._response)
        self.is_html = self._response_type_finder.is_html(self._response, self.encoding) if self._response else False

    @property
    def root(self):
        if self._root is lazy:
            response = self._response
            raw = self._response.read() if self._response else b''
            default_encoding = self._encoding_finder._default_encoding
            transport_encoding = get_encoding_from_response(response, verify=False)
            declared_encoding = find_declared_encoding(raw)
            self.form_encoding = declared_encoding or transport_encoding or default_encoding
            self._root = self._content_parser(raw,
              url=(response.geturl() if response else None),
              response_info=(response.info() if response else None),
              default_encoding=default_encoding,
              is_html=(self.is_html),
              transport_encoding=transport_encoding)
        return self._root

    @property
    def title(self):
        if self._current_title is lazy:
            self._current_title = get_title(self.root) if self.root is not None else None
        return self._current_title or ''

    @property
    def global_form(self):
        if self._current_global_form is lazy:
            self.forms()
        return self._current_global_form

    def forms(self):
        """ Return tuple of HTMLForm-like objects. """
        if self._current_forms is lazy:
            self._current_forms, self._current_global_form = self._get_forms()
        return self._current_forms

    def links(self):
        """Return tuple of mechanize.Link-like objects.  """
        if self._current_links is lazy:
            self._current_links = self._get_links()
        return self._get_links()

    def _get_links(self):
        if self.root is None:
            return ()
        return tuple(iterlinks(self.root, self._response.geturl()))

    def _get_forms(self):
        if self.root is None:
            return ((), None)
        return parse_forms((self.root), (self._response.geturl()),
          (self._request_class), encoding=(self.form_encoding))