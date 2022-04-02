# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: cgi.py
"""Support module for CGI (Common Gateway Interface) scripts.

This module defines a number of utilities for use by CGI scripts
written in Python.
"""
__version__ = '2.6'
from io import StringIO, BytesIO, TextIOWrapper
from collections.abc import Mapping
import sys, os, urllib.parse
from email.parser import FeedParser
from email.message import Message
import html, locale, tempfile
__all__ = [
 'MiniFieldStorage', 'FieldStorage', 'parse', 'parse_multipart',
 'parse_header', 'test', 'print_exception', 'print_environ',
 'print_form', 'print_directory', 'print_arguments',
 'print_environ_usage']
logfile = ''
logfp = None

def initlog(*allargs):
    """Write a log message, if there is a log file.

    Even though this function is called initlog(), you should always
    use log(); log is a variable that is set either to initlog
    (initially), to dolog (once the log file has been opened), or to
    nolog (when logging is disabled).

    The first argument is a format string; the remaining arguments (if
    any) are arguments to the % operator, so e.g.
        log("%s: %s", "a", "b")
    will write "a: b" to the log file, followed by a newline.

    If the global logfp is not None, it should be a file object to
    which log data is written.

    If the global logfp is None, the global logfile may be a string
    giving a filename to open, in append mode.  This file should be
    world writable!!!  If the file can't be opened, logging is
    silently disabled (since there is no safe place where we could
    send an error message).

    """
    global log
    global logfile
    global logfp
    if logfile and not logfp:
        try:
            logfp = open(logfile, 'a')
        except OSError:
            pass

    if not logfp:
        log = nolog
    else:
        log = dolog
    log(*allargs)


def dolog(fmt, *args):
    """Write a log message to the log file.  See initlog() for docs."""
    logfp.write(fmt % args + '\n')


def nolog(*allargs):
    """Dummy function, assigned to log when logging is disabled."""
    pass


def closelog():
    """Close the log file."""
    global log
    global logfile
    global logfp
    logfile = ''
    if logfp:
        logfp.close()
        logfp = None
    log = initlog


log = initlog
maxlen = 0

def parse(fp=None, environ=os.environ, keep_blank_values=0, strict_parsing=0):
    """Parse a query in the environment or from a file (default stdin)

        Arguments, all optional:

        fp              : file pointer; default: sys.stdin.buffer

        environ         : environment dictionary; default: os.environ

        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
    """
    global maxlen
    if fp is None:
        fp = sys.stdin
    if hasattr(fp, 'encoding'):
        encoding = fp.encoding
    else:
        encoding = 'latin-1'
    if isinstance(fp, TextIOWrapper):
        fp = fp.buffer
    if 'REQUEST_METHOD' not in environ:
        environ['REQUEST_METHOD'] = 'GET'
    if environ['REQUEST_METHOD'] == 'POST':
        ctype, pdict = parse_header(environ['CONTENT_TYPE'])
        if ctype == 'multipart/form-data':
            return parse_multipart(fp, pdict)
        if ctype == 'application/x-www-form-urlencoded':
            clength = int(environ['CONTENT_LENGTH'])
            if maxlen:
                if clength > maxlen:
                    raise ValueError('Maximum content length exceeded')
            qs = fp.read(clength).decode(encoding)
        else:
            qs = ''
        if 'QUERY_STRING' in environ:
            if qs:
                qs = qs + '&'
            qs = qs + environ['QUERY_STRING']
        elif sys.argv[1:]:
            if qs:
                qs = qs + '&'
            qs = qs + sys.argv[1]
        environ['QUERY_STRING'] = qs
    elif 'QUERY_STRING' in environ:
        qs = environ['QUERY_STRING']
    else:
        if sys.argv[1:]:
            qs = sys.argv[1]
        else:
            qs = ''
        environ['QUERY_STRING'] = qs
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing, encoding=encoding)


def parse_multipart(fp, pdict, encoding='utf-8', errors='replace'):
    """Parse multipart input.

    Arguments:
    fp   : input file
    pdict: dictionary containing other parameters of content-type header
    encoding, errors: request encoding and error handler, passed to
        FieldStorage

    Returns a dictionary just like parse_qs(): keys are the field names, each
    value is a list of values for that field. For non-file fields, the value
    is a list of strings.
    """
    boundary = pdict['boundary'].decode('ascii')
    ctype = 'multipart/form-data; boundary={}'.format(boundary)
    headers = Message()
    headers.set_type(ctype)
    headers['Content-Length'] = pdict['CONTENT-LENGTH']
    fs = FieldStorage(fp, headers=headers, encoding=encoding, errors=errors, environ={'REQUEST_METHOD': 'POST'})
    return {fs.getlist(k):k for k in fs}


def _parseparam(s):
    while True:
        if s[:1] == ';':
            s = s[1:]
            end = s.find(';')
        else:
            while end > 0:
                if (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
                    end = s.find(';', end + 1)

            if end < 0:
                end = len(s)
            f = s[:end]
            yield f.strip()
            s = s[end:]


def parse_header(line):
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    """
    parts = _parseparam(';' + line)
    key = parts.__next__()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2:
                if value[0] == value[(-1)] == '"':
                    value = value[1:-1]
                    value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    else:
        return (
         key, pdict)


class MiniFieldStorage:
    __doc__ = 'Like FieldStorage, for use when no file uploads are possible.'
    filename = None
    list = None
    type = None
    file = None
    type_options = {}
    disposition = None
    disposition_options = {}
    headers = {}

    def __init__(self, name, value):
        """Constructor from field name and value."""
        self.name = name
        self.value = value

    def __repr__(self):
        """Return printable representation."""
        return 'MiniFieldStorage(%r, %r)' % (self.name, self.value)


class FieldStorage:
    __doc__ = "Store a sequence of fields, reading multipart/form-data.\n\n    This class provides naming, typing, files stored on disk, and\n    more.  At the top level, it is accessible like a dictionary, whose\n    keys are the field names.  (Note: None can occur as a field name.)\n    The items are either a Python list (if there's multiple values) or\n    another FieldStorage or MiniFieldStorage object.  If it's a single\n    object, it has the following attributes:\n\n    name: the field name, if specified; otherwise None\n\n    filename: the filename, if specified; otherwise None; this is the\n        client side filename, *not* the file name on which it is\n        stored (that's a temporary file you don't deal with)\n\n    value: the value as a *string*; for file uploads, this\n        transparently reads the file every time you request the value\n        and returns *bytes*\n\n    file: the file(-like) object from which you can read the data *as\n        bytes* ; None if the data is stored a simple string\n\n    type: the content-type, or None if not specified\n\n    type_options: dictionary of options specified on the content-type\n        line\n\n    disposition: content-disposition, or None if not specified\n\n    disposition_options: dictionary of corresponding options\n\n    headers: a dictionary(-like) object (sometimes email.message.Message or a\n        subclass thereof) containing *all* headers\n\n    The class is subclassable, mostly for the purpose of overriding\n    the make_file() method, which is called internally to come up with\n    a file open for reading and writing.  This makes it possible to\n    override the default choice of storing all files in a temporary\n    directory and unlinking them as soon as they have been opened.\n\n    "

    def __init__(self, fp=None, headers=None, outerboundary=b'', environ=os.environ, keep_blank_values=0, strict_parsing=0, limit=None, encoding='utf-8', errors='replace', max_num_fields=None):
        """Constructor.  Read multipart/* until last part.

        Arguments, all optional:

        fp              : file pointer; default: sys.stdin.buffer
            (not used when the request method is GET)
            Can be :
            1. a TextIOWrapper object
            2. an object whose read() and readline() methods return bytes

        headers         : header dictionary-like object; default:
            taken from environ as per CGI spec

        outerboundary   : terminating multipart boundary
            (for internal use only)

        environ         : environment dictionary; default: os.environ

        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        limit : used internally to read parts of multipart/form-data forms,
            to exit from the reading loop when reached. It is the difference
            between the form content-length and the number of bytes already
            read

        encoding, errors : the encoding and error handler used to decode the
            binary stream to strings. Must be the same as the charset defined
            for the page sending the form (content-type : meta http-equiv or
            header)

        max_num_fields: int. If set, then __init__ throws a ValueError
            if there are more than n fields read by parse_qsl().

        """
        method = 'GET'
        self.keep_blank_values = keep_blank_values
        self.strict_parsing = strict_parsing
        self.max_num_fields = max_num_fields
        if 'REQUEST_METHOD' in environ:
            method = environ['REQUEST_METHOD'].upper()
        self.qs_on_post = None
        if method == 'GET' or (method == 'HEAD'):
            if 'QUERY_STRING' in environ:
                qs = environ['QUERY_STRING']
            elif sys.argv[1:]:
                qs = sys.argv[1]
            else:
                qs = ''
            qs = qs.encode(locale.getpreferredencoding(), 'surrogateescape')
            fp = BytesIO(qs)
            if headers is None:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
        if headers is None:
            headers = {}
            if method == 'POST':
                headers['content-type'] = 'application/x-www-form-urlencoded'
            if 'CONTENT_TYPE' in environ:
                headers['content-type'] = environ['CONTENT_TYPE']
            if 'QUERY_STRING' in environ:
                self.qs_on_post = environ['QUERY_STRING']
            if 'CONTENT_LENGTH' in environ:
                headers['content-length'] = environ['CONTENT_LENGTH']
        elif not isinstance(headers, (Mapping, Message)):
            raise TypeError('headers must be mapping or an instance of email.message.Message')
        self.headers = headers
        if fp is None:
            self.fp = sys.stdin.buffer
        elif isinstance(fp, TextIOWrapper):
            self.fp = fp.buffer
        else:
            if not (hasattr(fp, 'read') and hasattr(fp, 'readline')):
                raise TypeError('fp must be file pointer')
            self.fp = fp
        self.encoding = encoding
        self.errors = errors
        if not isinstance(outerboundary, bytes):
            raise TypeError('outerboundary must be bytes, not %s' % type(outerboundary).__name__)
        self.outerboundary = outerboundary
        self.bytes_read = 0
        self.limit = limit
        cdisp, pdict = '', {}
        if 'content-disposition' in self.headers:
            cdisp, pdict = parse_header(self.headers['content-disposition'])
        self.disposition = cdisp
        self.disposition_options = pdict
        self.name = None
        if 'name' in pdict:
            self.name = pdict['name']
        self.filename = None
        if 'filename' in pdict:
            self.filename = pdict['filename']
        self._binary_file = self.filename is not None
        if 'content-type' in self.headers:
            ctype, pdict = parse_header(self.headers['content-type'])
        elif self.outerboundary or method != 'POST':
            ctype, pdict = 'text/plain', {}
        else:
            ctype, pdict = 'application/x-www-form-urlencoded', {}
        self.type = ctype
        self.type_options = pdict
        if 'boundary' in pdict:
            self.innerboundary = pdict['boundary'].encode(self.encoding, self.errors)
        else:
            self.innerboundary = b''
        clen = -1
        if 'content-length' in self.headers:
            try:
                clen = int(self.headers['content-length'])
            except ValueError:
                pass
            else:
                if maxlen:
                    if clen > maxlen:
                        raise ValueError('Maximum content length exceeded')
            self.length = clen
            if self.limit is None:
                if clen >= 0:
                    self.limit = clen
        self.list = self.file = None
        self.done = 0
        if ctype == 'application/x-www-form-urlencoded':
            self.read_urlencoded()
        elif ctype[:10] == 'multipart/':
            self.read_multi(environ, keep_blank_values, strict_parsing)
        else:
            self.read_single()

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.file.close()

    def __repr__(self):
        """Return a printable representation."""
        return 'FieldStorage(%r, %r, %r)' % (
         self.name, self.filename, self.value)

    def __iter__(self):
        return iter(self.keys())

    def __getattr__(self, name):
        if name != 'value':
            raise AttributeError(name)
        if self.file:
            self.file.seek(0)
            value = self.file.read()
            self.file.seek(0)
        elif self.list is not None:
            value = self.list
        else:
            value = None
        return value

    def __getitem__(self, key):
        """Dictionary style indexing."""
        if self.list is None:
            raise TypeError('not indexable')
        found = []
        for item in self.list:
            if item.name == key:
                found.append(item)
        else:
            if not found:
                raise KeyError(key)
            if len(found) == 1:
                return found[0]
            return found

    def getvalue(self, key, default=None):
        """Dictionary style get() method, including 'value' lookup."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return [x.value for x in value]
            return value.value
        else:
            return default

    def getfirst(self, key, default=None):
        """ Return the first value received."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return value[0].value
            return value.value
        else:
            return default

    def getlist(self, key):
        """ Return list of received values."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return [x.value for x in value]
            return [
             value.value]
        else:
            return []

    def keys(self):
        """Dictionary style keys() method."""
        if self.list is None:
            raise TypeError('not indexable')
        return list(set((item.name for item in self.list)))

    def __contains__(self, key):
        """Dictionary style __contains__ method."""
        if self.list is None:
            raise TypeError('not indexable')
        return any((item.name == key for item in self.list))

    def __len__(self):
        """Dictionary style len(x) support."""
        return len(self.keys())

    def __bool__(self):
        if self.list is None:
            raise TypeError('Cannot be converted to bool.')
        return bool(self.list)

    def read_urlencoded(self):
        """Internal: read data in query string format."""
        qs = self.fp.read(self.length)
        if not isinstance(qs, bytes):
            raise ValueError('%s should return bytes, got %s' % (
             self.fp, type(qs).__name__))
        qs = qs.decode(self.encoding, self.errors)
        if self.qs_on_post:
            qs += '&' + self.qs_on_post
        query = urllib.parse.parse_qsl(qs,
          (self.keep_blank_values), (self.strict_parsing), encoding=(self.encoding),
          errors=(self.errors),
          max_num_fields=(self.max_num_fields))
        self.list = [MiniFieldStorage(key, value) for key, value in query]
        self.skip_lines()

    FieldStorageClass = None

    def read_multi--- This code section failed: ---

 L. 597         0  LOAD_FAST                'self'
                2  LOAD_ATTR                innerboundary
                4  STORE_FAST               'ib'

 L. 598         6  LOAD_GLOBAL              valid_boundary
                8  LOAD_FAST                'ib'
               10  CALL_FUNCTION_1       1  ''
               12  POP_JUMP_IF_TRUE     28  'to 28'

 L. 599        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'Invalid boundary in multipart form: %r'
               18  LOAD_FAST                'ib'
               20  BUILD_TUPLE_1         1 
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            12  '12'

 L. 600        28  BUILD_LIST_0          0 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               list

 L. 601        34  LOAD_FAST                'self'
               36  LOAD_ATTR                qs_on_post
               38  POP_JUMP_IF_FALSE    98  'to 98'

 L. 602        40  LOAD_GLOBAL              urllib
               42  LOAD_ATTR                parse
               44  LOAD_ATTR                parse_qsl

 L. 603        46  LOAD_FAST                'self'
               48  LOAD_ATTR                qs_on_post

 L. 603        50  LOAD_FAST                'self'
               52  LOAD_ATTR                keep_blank_values

 L. 603        54  LOAD_FAST                'self'
               56  LOAD_ATTR                strict_parsing

 L. 604        58  LOAD_FAST                'self'
               60  LOAD_ATTR                encoding

 L. 604        62  LOAD_FAST                'self'
               64  LOAD_ATTR                errors

 L. 605        66  LOAD_FAST                'self'
               68  LOAD_ATTR                max_num_fields

 L. 602        70  LOAD_CONST               ('encoding', 'errors', 'max_num_fields')
               72  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               74  STORE_FAST               'query'

 L. 606        76  LOAD_FAST                'self'
               78  LOAD_ATTR                list
               80  LOAD_METHOD              extend
               82  LOAD_GENEXPR             '<code_object <genexpr>>'
               84  LOAD_STR                 'FieldStorage.read_multi.<locals>.<genexpr>'
               86  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               88  LOAD_FAST                'query'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
             98_0  COME_FROM            38  '38'

 L. 608        98  LOAD_FAST                'self'
              100  LOAD_ATTR                FieldStorageClass
              102  JUMP_IF_TRUE_OR_POP   108  'to 108'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                __class__
            108_0  COME_FROM           102  '102'
              108  STORE_FAST               'klass'

 L. 609       110  LOAD_FAST                'self'
              112  LOAD_ATTR                fp
              114  LOAD_METHOD              readline
              116  CALL_METHOD_0         0  ''
              118  STORE_FAST               'first_line'

 L. 610       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'first_line'
              124  LOAD_GLOBAL              bytes
              126  CALL_FUNCTION_2       2  ''
              128  POP_JUMP_IF_TRUE    154  'to 154'

 L. 611       130  LOAD_GLOBAL              ValueError
              132  LOAD_STR                 '%s should return bytes, got %s'

 L. 612       134  LOAD_FAST                'self'
              136  LOAD_ATTR                fp
              138  LOAD_GLOBAL              type
              140  LOAD_FAST                'first_line'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_ATTR                __name__
              146  BUILD_TUPLE_2         2 

 L. 611       148  BINARY_MODULO    
              150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           128  '128'

 L. 613       154  LOAD_FAST                'self'
              156  DUP_TOP          
              158  LOAD_ATTR                bytes_read
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'first_line'
              164  CALL_FUNCTION_1       1  ''
              166  INPLACE_ADD      
              168  ROT_TWO          
              170  STORE_ATTR               bytes_read
            172_0  COME_FROM           222  '222'

 L. 616       172  LOAD_FAST                'first_line'
              174  LOAD_METHOD              strip
              176  CALL_METHOD_0         0  ''
              178  LOAD_CONST               b'--'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                innerboundary
              184  BINARY_ADD       
              186  COMPARE_OP               !=
              188  POP_JUMP_IF_FALSE   224  'to 224'

 L. 617       190  LOAD_FAST                'first_line'

 L. 616       192  POP_JUMP_IF_FALSE   224  'to 224'

 L. 618       194  LOAD_FAST                'self'
              196  LOAD_ATTR                fp
              198  LOAD_METHOD              readline
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'first_line'

 L. 619       204  LOAD_FAST                'self'
              206  DUP_TOP          
              208  LOAD_ATTR                bytes_read
              210  LOAD_GLOBAL              len
              212  LOAD_FAST                'first_line'
              214  CALL_FUNCTION_1       1  ''
              216  INPLACE_ADD      
              218  ROT_TWO          
              220  STORE_ATTR               bytes_read
              222  JUMP_BACK           172  'to 172'
            224_0  COME_FROM           192  '192'
            224_1  COME_FROM           188  '188'

 L. 622       224  LOAD_FAST                'self'
              226  LOAD_ATTR                max_num_fields
              228  STORE_FAST               'max_num_fields'

 L. 623       230  LOAD_FAST                'max_num_fields'
              232  LOAD_CONST               None
              234  COMPARE_OP               is-not
              236  POP_JUMP_IF_FALSE   252  'to 252'

 L. 624       238  LOAD_FAST                'max_num_fields'
              240  LOAD_GLOBAL              len
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                list
              246  CALL_FUNCTION_1       1  ''
              248  INPLACE_SUBTRACT 
              250  STORE_FAST               'max_num_fields'
            252_0  COME_FROM           560  '560'
            252_1  COME_FROM           554  '554'
            252_2  COME_FROM           548  '548'
            252_3  COME_FROM           236  '236'

 L. 627       252  LOAD_GLOBAL              FeedParser
              254  CALL_FUNCTION_0       0  ''
              256  STORE_FAST               'parser'

 L. 628       258  LOAD_CONST               b''
              260  STORE_FAST               'hdr_text'
            262_0  COME_FROM           294  '294'
            262_1  COME_FROM           286  '286'

 L. 630       262  LOAD_FAST                'self'
              264  LOAD_ATTR                fp
              266  LOAD_METHOD              readline
              268  CALL_METHOD_0         0  ''
              270  STORE_FAST               'data'

 L. 631       272  LOAD_FAST                'hdr_text'
              274  LOAD_FAST                'data'
              276  INPLACE_ADD      
              278  STORE_FAST               'hdr_text'

 L. 632       280  LOAD_FAST                'data'
              282  LOAD_METHOD              strip
              284  CALL_METHOD_0         0  ''
          286_288  POP_JUMP_IF_TRUE_BACK   262  'to 262'

 L. 633   290_292  JUMP_FORWARD        298  'to 298'
          294_296  JUMP_BACK           262  'to 262'
            298_0  COME_FROM           290  '290'

 L. 634       298  LOAD_FAST                'hdr_text'
          300_302  POP_JUMP_IF_TRUE    308  'to 308'

 L. 635   304_306  JUMP_FORWARD        562  'to 562'
            308_0  COME_FROM           300  '300'

 L. 637       308  LOAD_FAST                'self'
              310  DUP_TOP          
              312  LOAD_ATTR                bytes_read
              314  LOAD_GLOBAL              len
              316  LOAD_FAST                'hdr_text'
              318  CALL_FUNCTION_1       1  ''
              320  INPLACE_ADD      
              322  ROT_TWO          
              324  STORE_ATTR               bytes_read

 L. 638       326  LOAD_FAST                'parser'
              328  LOAD_METHOD              feed
              330  LOAD_FAST                'hdr_text'
              332  LOAD_METHOD              decode
              334  LOAD_FAST                'self'
              336  LOAD_ATTR                encoding
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                errors
              342  CALL_METHOD_2         2  ''
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          

 L. 639       348  LOAD_FAST                'parser'
              350  LOAD_METHOD              close
              352  CALL_METHOD_0         0  ''
              354  STORE_FAST               'headers'

 L. 642       356  LOAD_STR                 'content-length'
              358  LOAD_FAST                'headers'
              360  COMPARE_OP               in
          362_364  POP_JUMP_IF_FALSE   372  'to 372'

 L. 643       366  LOAD_FAST                'headers'
              368  LOAD_STR                 'content-length'
              370  DELETE_SUBSCR    
            372_0  COME_FROM           362  '362'

 L. 645       372  LOAD_FAST                'self'
              374  LOAD_ATTR                limit
              376  LOAD_CONST               None
              378  COMPARE_OP               is
          380_382  POP_JUMP_IF_FALSE   388  'to 388'
              384  LOAD_CONST               None
              386  JUMP_FORWARD        398  'to 398'
            388_0  COME_FROM           380  '380'

 L. 646       388  LOAD_FAST                'self'
              390  LOAD_ATTR                limit
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                bytes_read
              396  BINARY_SUBTRACT  
            398_0  COME_FROM           386  '386'

 L. 645       398  STORE_FAST               'limit'

 L. 647       400  LOAD_FAST                'klass'
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                fp
              406  LOAD_FAST                'headers'
              408  LOAD_FAST                'ib'
              410  LOAD_FAST                'environ'
              412  LOAD_FAST                'keep_blank_values'

 L. 648       414  LOAD_FAST                'strict_parsing'

 L. 648       416  LOAD_FAST                'limit'

 L. 649       418  LOAD_FAST                'self'
              420  LOAD_ATTR                encoding

 L. 649       422  LOAD_FAST                'self'
              424  LOAD_ATTR                errors

 L. 649       426  LOAD_FAST                'max_num_fields'

 L. 647       428  CALL_FUNCTION_10     10  ''
              430  STORE_FAST               'part'

 L. 651       432  LOAD_FAST                'max_num_fields'
              434  LOAD_CONST               None
              436  COMPARE_OP               is-not
          438_440  POP_JUMP_IF_FALSE   490  'to 490'

 L. 652       442  LOAD_FAST                'max_num_fields'
              444  LOAD_CONST               1
              446  INPLACE_SUBTRACT 
              448  STORE_FAST               'max_num_fields'

 L. 653       450  LOAD_FAST                'part'
              452  LOAD_ATTR                list
          454_456  POP_JUMP_IF_FALSE   472  'to 472'

 L. 654       458  LOAD_FAST                'max_num_fields'
              460  LOAD_GLOBAL              len
              462  LOAD_FAST                'part'
              464  LOAD_ATTR                list
              466  CALL_FUNCTION_1       1  ''
              468  INPLACE_SUBTRACT 
              470  STORE_FAST               'max_num_fields'
            472_0  COME_FROM           454  '454'

 L. 655       472  LOAD_FAST                'max_num_fields'
              474  LOAD_CONST               0
              476  COMPARE_OP               <
          478_480  POP_JUMP_IF_FALSE   490  'to 490'

 L. 656       482  LOAD_GLOBAL              ValueError
              484  LOAD_STR                 'Max number of fields exceeded'
              486  CALL_FUNCTION_1       1  ''
              488  RAISE_VARARGS_1       1  'exception instance'
            490_0  COME_FROM           478  '478'
            490_1  COME_FROM           438  '438'

 L. 658       490  LOAD_FAST                'self'
              492  DUP_TOP          
              494  LOAD_ATTR                bytes_read
              496  LOAD_FAST                'part'
              498  LOAD_ATTR                bytes_read
              500  INPLACE_ADD      
              502  ROT_TWO          
              504  STORE_ATTR               bytes_read

 L. 659       506  LOAD_FAST                'self'
              508  LOAD_ATTR                list
              510  LOAD_METHOD              append
              512  LOAD_FAST                'part'
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          

 L. 660       518  LOAD_FAST                'part'
              520  LOAD_ATTR                done
          522_524  POP_JUMP_IF_TRUE    562  'to 562'
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                bytes_read
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                length
              534  DUP_TOP          
              536  ROT_THREE        
              538  COMPARE_OP               >=
          540_542  POP_JUMP_IF_FALSE   552  'to 552'
              544  LOAD_CONST               0
              546  COMPARE_OP               >
              548  POP_JUMP_IF_FALSE_BACK   252  'to 252'
              550  JUMP_FORWARD        562  'to 562'
            552_0  COME_FROM           540  '540'
              552  POP_TOP          
              554  JUMP_BACK           252  'to 252'

 L. 661   556_558  JUMP_FORWARD        562  'to 562'
              560  JUMP_BACK           252  'to 252'
            562_0  COME_FROM           556  '556'
            562_1  COME_FROM           550  '550'
            562_2  COME_FROM           522  '522'
            562_3  COME_FROM           304  '304'

 L. 662       562  LOAD_FAST                'self'
              564  LOAD_METHOD              skip_lines
              566  CALL_METHOD_0         0  ''
              568  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 294_296

    def read_single(self):
        """Internal: read an atomic part."""
        if self.length >= 0:
            self.read_binary()
            self.skip_lines()
        else:
            self.read_lines()
        self.file.seek(0)

    bufsize = 8192

    def read_binary(self):
        """Internal: read binary data."""
        self.file = self.make_file()
        todo = self.length
        if todo >= 0:
            while True:
                if todo > 0:
                    data = self.fp.read(min(todo, self.bufsize))
                    if not isinstance(data, bytes):
                        raise ValueError('%s should return bytes, got %s' % (
                         self.fp, type(data).__name__))
                    else:
                        self.bytes_read += len(data)
                        if not data:
                            self.done = -1
                        else:
                            self.file.write(data)
                            todo = todo - len(data)

    def read_lines(self):
        """Internal: read lines until EOF or outerboundary."""
        if self._binary_file:
            self.file = self._FieldStorage__file = BytesIO()
        else:
            self.file = self._FieldStorage__file = StringIO()
        if self.outerboundary:
            self.read_lines_to_outerboundary()
        else:
            self.read_lines_to_eof()

    def __write(self, line):
        """line is always bytes, not string"""
        if self._FieldStorage__file is not None:
            if self._FieldStorage__file.tell() + len(line) > 1000:
                self.file = self.make_file()
                data = self._FieldStorage__file.getvalue()
                self.file.write(data)
                self._FieldStorage__file = None
        if self._binary_file:
            self.file.write(line)
        else:
            self.file.write(line.decode(self.encoding, self.errors))

    def read_lines_to_eof(self):
        """Internal: read lines until EOF."""
        while True:
            line = self.fp.readline(65536)
            self.bytes_read += len(line)
            if not line:
                self.done = -1
            else:
                self._FieldStorage__write(line)

    def read_lines_to_outerboundary(self):
        """Internal: read lines until outerboundary.
        Data is read as bytes: boundaries and line ends must be converted
        to bytes for comparisons.
        """
        next_boundary = b'--' + self.outerboundary
        last_boundary = next_boundary + b'--'
        delim = b''
        last_line_lfend = True
        _read = 0
        while True:
            if self.limit is not None and _read >= self.limit:
                pass
            else:
                line = self.fp.readline(65536)
                self.bytes_read += len(line)
                _read += len(line)
                if not line:
                    self.done = -1
                else:
                    if delim == b'\r':
                        line = delim + line
                        delim = b''
                    if line.startswith(b'--') and last_line_lfend:
                        strippedline = line.rstrip()
                        if strippedline == next_boundary:
                            pass
                        elif strippedline == last_boundary:
                            self.done = 1
                    else:
                        pass
                    odelim = delim
                    if line.endswith(b'\r\n'):
                        delim = b'\r\n'
                        line = line[:-2]
                        last_line_lfend = True
                    elif line.endswith(b'\n'):
                        delim = b'\n'
                        line = line[:-1]
                        last_line_lfend = True
                    elif line.endswith(b'\r'):
                        delim = b'\r'
                        line = line[:-1]
                        last_line_lfend = False
                    else:
                        delim = b''
                        last_line_lfend = False
                    self._FieldStorage__write(odelim + line)

    def skip_lines(self):
        """Internal: skip lines until outer boundary if defined."""
        if not self.outerboundary or self.done:
            return
        next_boundary = b'--' + self.outerboundary
        last_boundary = next_boundary + b'--'
        last_line_lfend = True
        while True:
            line = self.fp.readline(65536)
            self.bytes_read += len(line)
            if not line:
                self.done = -1
            else:
                if line.endswith(b'--') and last_line_lfend:
                    strippedline = line.strip()
                    if strippedline == next_boundary:
                        pass
                    elif strippedline == last_boundary:
                        self.done = 1
                else:
                    pass
                last_line_lfend = line.endswith(b'\n')

    def make_file(self):
        """Overridable: return a readable & writable file.

        The file will be used as follows:
        - data is written to it
        - seek(0)
        - data is read from it

        The file is opened in binary mode for files, in text mode
        for other fields

        This version opens a temporary file for reading and writing,
        and immediately deletes (unlinks) it.  The trick (on Unix!) is
        that the file can still be used, but it can't be opened by
        another process, and it will automatically be deleted when it
        is closed or when the current process terminates.

        If you want a more permanent file, you derive a class which
        overrides this method.  If you want a visible temporary file
        that is nevertheless automatically deleted when the script
        terminates, try defining a __del__ method in a derived class
        which unlinks the temporary files you have created.

        """
        if self._binary_file:
            return tempfile.TemporaryFile('wb+')
        return tempfile.TemporaryFile('w+', encoding=(self.encoding),
          newline='\n')


def test(environ=os.environ):
    """Robust test CGI script, usable as main program.

    Write minimal HTTP headers and dump all information provided to
    the script in HTML form.

    """
    global maxlen
    print('Content-type: text/html')
    print()
    sys.stderr = sys.stdout
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
        print_environ_usage()

        def f():
            exec('testing print_exception() -- <I>italics?</I>')

        def g(f=f):
            f()

        print('<H3>What follows is a test, not an actual exception:</H3>')
        g()
    except:
        print_exception()
    else:
        print('<H1>Second try with a small maxlen...</H1>')
        maxlen = 50
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
    except:
        print_exception()


def print_exception(type=None, value=None, tb=None, limit=None):
    if type is None:
        type, value, tb = sys.exc_info()
    import traceback
    print()
    print('<H3>Traceback (most recent call last):</H3>')
    list = traceback.format_tb(tb, limit) + traceback.format_exception_only(type, value)
    print('<PRE>%s<B>%s</B></PRE>' % (
     html.escape(''.join(list[:-1])),
     html.escape(list[(-1)])))
    del tb


def print_environ(environ=os.environ):
    """Dump the shell environment as HTML."""
    keys = sorted(environ.keys())
    print()
    print('<H3>Shell Environment:</H3>')
    print('<DL>')
    for key in keys:
        print('<DT>', html.escape(key), '<DD>', html.escape(environ[key]))
    else:
        print('</DL>')
        print()


def print_form(form):
    """Dump the contents of a form as HTML."""
    keys = sorted(form.keys())
    print()
    print('<H3>Form Contents:</H3>')
    if not keys:
        print('<P>No form fields.')
    print('<DL>')
    for key in keys:
        print(('<DT>' + html.escape(key) + ':'), end=' ')
        value = form[key]
        print('<i>' + html.escape(repr(type(value))) + '</i>')
        print('<DD>' + html.escape(repr(value)))
    else:
        print('</DL>')
        print()


def print_directory():
    """Dump the current directory as HTML."""
    print()
    print('<H3>Current Working Directory:</H3>')
    try:
        pwd = os.getcwd()
    except OSError as msg:
        try:
            print('OSError:', html.escape(str(msg)))
        finally:
            msg = None
            del msg

    else:
        print(html.escape(pwd))
    print()


def print_arguments():
    print()
    print('<H3>Command Line Arguments:</H3>')
    print()
    print(sys.argv)
    print()


def print_environ_usage():
    """Dump a list of environment variables used by CGI as HTML."""
    print('\n<H3>These environment variables could have been set:</H3>\n<UL>\n<LI>AUTH_TYPE\n<LI>CONTENT_LENGTH\n<LI>CONTENT_TYPE\n<LI>DATE_GMT\n<LI>DATE_LOCAL\n<LI>DOCUMENT_NAME\n<LI>DOCUMENT_ROOT\n<LI>DOCUMENT_URI\n<LI>GATEWAY_INTERFACE\n<LI>LAST_MODIFIED\n<LI>PATH\n<LI>PATH_INFO\n<LI>PATH_TRANSLATED\n<LI>QUERY_STRING\n<LI>REMOTE_ADDR\n<LI>REMOTE_HOST\n<LI>REMOTE_IDENT\n<LI>REMOTE_USER\n<LI>REQUEST_METHOD\n<LI>SCRIPT_NAME\n<LI>SERVER_NAME\n<LI>SERVER_PORT\n<LI>SERVER_PROTOCOL\n<LI>SERVER_ROOT\n<LI>SERVER_SOFTWARE\n</UL>\nIn addition, HTTP headers sent by the server may be passed in the\nenvironment as well.  Here are some common variable names:\n<UL>\n<LI>HTTP_ACCEPT\n<LI>HTTP_CONNECTION\n<LI>HTTP_HOST\n<LI>HTTP_PRAGMA\n<LI>HTTP_REFERER\n<LI>HTTP_USER_AGENT\n</UL>\n')


def valid_boundary(s):
    import re
    if isinstance(s, bytes):
        _vb_pattern = b'^[ -~]{0,200}[!-~]$'
    else:
        _vb_pattern = '^[ -~]{0,200}[!-~]$'
    return re.match(_vb_pattern, s)


if __name__ == '__main__':
    test()