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

def parse(fp=None, environ=os.environ, keep_blank_values=0, strict_parsing=0, separator='&'):
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

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.
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
            return parse_multipart(fp, pdict, separator=separator)
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
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing, encoding=encoding,
      separator=separator)


def parse_multipart(fp, pdict, encoding='utf-8', errors='replace', separator='&'):
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
    try:
        headers['Content-Length'] = pdict['CONTENT-LENGTH']
    except KeyError:
        pass
    else:
        fs = FieldStorage(fp, headers=headers, encoding=encoding, errors=errors, environ={'REQUEST_METHOD': 'POST'},
          separator=separator)
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

    def __init__(self, fp=None, headers=None, outerboundary=b'', environ=os.environ, keep_blank_values=0, strict_parsing=0, limit=None, encoding='utf-8', errors='replace', max_num_fields=None, separator='&'):
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
        self.separator = separator
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
          max_num_fields=(self.max_num_fields),
          separator=(self.separator))
        self.list = [MiniFieldStorage(key, value) for key, value in query]
        self.skip_lines()

    FieldStorageClass = None

    def read_multi--- This code section failed: ---

 L. 605         0  LOAD_FAST                'self'
                2  LOAD_ATTR                innerboundary
                4  STORE_FAST               'ib'

 L. 606         6  LOAD_GLOBAL              valid_boundary
                8  LOAD_FAST                'ib'
               10  CALL_FUNCTION_1       1  ''
               12  POP_JUMP_IF_TRUE     28  'to 28'

 L. 607        14  LOAD_GLOBAL              ValueError
               16  LOAD_STR                 'Invalid boundary in multipart form: %r'
               18  LOAD_FAST                'ib'
               20  BUILD_TUPLE_1         1 
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            12  '12'

 L. 608        28  BUILD_LIST_0          0 
               30  LOAD_FAST                'self'
               32  STORE_ATTR               list

 L. 609        34  LOAD_FAST                'self'
               36  LOAD_ATTR                qs_on_post
               38  POP_JUMP_IF_FALSE   102  'to 102'

 L. 610        40  LOAD_GLOBAL              urllib
               42  LOAD_ATTR                parse
               44  LOAD_ATTR                parse_qsl

 L. 611        46  LOAD_FAST                'self'
               48  LOAD_ATTR                qs_on_post

 L. 611        50  LOAD_FAST                'self'
               52  LOAD_ATTR                keep_blank_values

 L. 611        54  LOAD_FAST                'self'
               56  LOAD_ATTR                strict_parsing

 L. 612        58  LOAD_FAST                'self'
               60  LOAD_ATTR                encoding

 L. 612        62  LOAD_FAST                'self'
               64  LOAD_ATTR                errors

 L. 613        66  LOAD_FAST                'self'
               68  LOAD_ATTR                max_num_fields

 L. 613        70  LOAD_FAST                'self'
               72  LOAD_ATTR                separator

 L. 610        74  LOAD_CONST               ('encoding', 'errors', 'max_num_fields', 'separator')
               76  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               78  STORE_FAST               'query'

 L. 614        80  LOAD_FAST                'self'
               82  LOAD_ATTR                list
               84  LOAD_METHOD              extend
               86  LOAD_GENEXPR             '<code_object <genexpr>>'
               88  LOAD_STR                 'FieldStorage.read_multi.<locals>.<genexpr>'
               90  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               92  LOAD_FAST                'query'
               94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
            102_0  COME_FROM            38  '38'

 L. 616       102  LOAD_FAST                'self'
              104  LOAD_ATTR                FieldStorageClass
              106  JUMP_IF_TRUE_OR_POP   112  'to 112'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                __class__
            112_0  COME_FROM           106  '106'
              112  STORE_FAST               'klass'

 L. 617       114  LOAD_FAST                'self'
              116  LOAD_ATTR                fp
              118  LOAD_METHOD              readline
              120  CALL_METHOD_0         0  ''
              122  STORE_FAST               'first_line'

 L. 618       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'first_line'
              128  LOAD_GLOBAL              bytes
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_TRUE    158  'to 158'

 L. 619       134  LOAD_GLOBAL              ValueError
              136  LOAD_STR                 '%s should return bytes, got %s'

 L. 620       138  LOAD_FAST                'self'
              140  LOAD_ATTR                fp
              142  LOAD_GLOBAL              type
              144  LOAD_FAST                'first_line'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_ATTR                __name__
              150  BUILD_TUPLE_2         2 

 L. 619       152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           132  '132'

 L. 621       158  LOAD_FAST                'self'
              160  DUP_TOP          
              162  LOAD_ATTR                bytes_read
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'first_line'
              168  CALL_FUNCTION_1       1  ''
              170  INPLACE_ADD      
              172  ROT_TWO          
              174  STORE_ATTR               bytes_read
            176_0  COME_FROM           226  '226'

 L. 624       176  LOAD_FAST                'first_line'
              178  LOAD_METHOD              strip
              180  CALL_METHOD_0         0  ''
              182  LOAD_CONST               b'--'
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                innerboundary
              188  BINARY_ADD       
              190  COMPARE_OP               !=
              192  POP_JUMP_IF_FALSE   228  'to 228'

 L. 625       194  LOAD_FAST                'first_line'

 L. 624       196  POP_JUMP_IF_FALSE   228  'to 228'

 L. 626       198  LOAD_FAST                'self'
              200  LOAD_ATTR                fp
              202  LOAD_METHOD              readline
              204  CALL_METHOD_0         0  ''
              206  STORE_FAST               'first_line'

 L. 627       208  LOAD_FAST                'self'
              210  DUP_TOP          
              212  LOAD_ATTR                bytes_read
              214  LOAD_GLOBAL              len
              216  LOAD_FAST                'first_line'
              218  CALL_FUNCTION_1       1  ''
              220  INPLACE_ADD      
              222  ROT_TWO          
              224  STORE_ATTR               bytes_read
              226  JUMP_BACK           176  'to 176'
            228_0  COME_FROM           196  '196'
            228_1  COME_FROM           192  '192'

 L. 630       228  LOAD_FAST                'self'
              230  LOAD_ATTR                max_num_fields
              232  STORE_FAST               'max_num_fields'

 L. 631       234  LOAD_FAST                'max_num_fields'
              236  LOAD_CONST               None
              238  COMPARE_OP               is-not
          240_242  POP_JUMP_IF_FALSE   258  'to 258'

 L. 632       244  LOAD_FAST                'max_num_fields'
              246  LOAD_GLOBAL              len
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                list
              252  CALL_FUNCTION_1       1  ''
              254  INPLACE_SUBTRACT 
              256  STORE_FAST               'max_num_fields'
            258_0  COME_FROM           572  '572'
            258_1  COME_FROM           566  '566'
            258_2  COME_FROM           558  '558'
            258_3  COME_FROM           240  '240'

 L. 635       258  LOAD_GLOBAL              FeedParser
              260  CALL_FUNCTION_0       0  ''
              262  STORE_FAST               'parser'

 L. 636       264  LOAD_CONST               b''
              266  STORE_FAST               'hdr_text'
            268_0  COME_FROM           300  '300'
            268_1  COME_FROM           292  '292'

 L. 638       268  LOAD_FAST                'self'
              270  LOAD_ATTR                fp
              272  LOAD_METHOD              readline
              274  CALL_METHOD_0         0  ''
              276  STORE_FAST               'data'

 L. 639       278  LOAD_FAST                'hdr_text'
              280  LOAD_FAST                'data'
              282  INPLACE_ADD      
              284  STORE_FAST               'hdr_text'

 L. 640       286  LOAD_FAST                'data'
              288  LOAD_METHOD              strip
              290  CALL_METHOD_0         0  ''
          292_294  POP_JUMP_IF_TRUE_BACK   268  'to 268'

 L. 641   296_298  JUMP_FORWARD        304  'to 304'
          300_302  JUMP_BACK           268  'to 268'
            304_0  COME_FROM           296  '296'

 L. 642       304  LOAD_FAST                'hdr_text'
          306_308  POP_JUMP_IF_TRUE    314  'to 314'

 L. 643   310_312  JUMP_FORWARD        576  'to 576'
            314_0  COME_FROM           306  '306'

 L. 645       314  LOAD_FAST                'self'
              316  DUP_TOP          
              318  LOAD_ATTR                bytes_read
              320  LOAD_GLOBAL              len
              322  LOAD_FAST                'hdr_text'
              324  CALL_FUNCTION_1       1  ''
              326  INPLACE_ADD      
              328  ROT_TWO          
              330  STORE_ATTR               bytes_read

 L. 646       332  LOAD_FAST                'parser'
              334  LOAD_METHOD              feed
              336  LOAD_FAST                'hdr_text'
              338  LOAD_METHOD              decode
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                encoding
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                errors
              348  CALL_METHOD_2         2  ''
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          

 L. 647       354  LOAD_FAST                'parser'
              356  LOAD_METHOD              close
              358  CALL_METHOD_0         0  ''
              360  STORE_FAST               'headers'

 L. 650       362  LOAD_STR                 'content-length'
              364  LOAD_FAST                'headers'
              366  COMPARE_OP               in
          368_370  POP_JUMP_IF_FALSE   378  'to 378'

 L. 651       372  LOAD_FAST                'headers'
              374  LOAD_STR                 'content-length'
              376  DELETE_SUBSCR    
            378_0  COME_FROM           368  '368'

 L. 653       378  LOAD_FAST                'self'
              380  LOAD_ATTR                limit
              382  LOAD_CONST               None
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_FALSE   394  'to 394'
              390  LOAD_CONST               None
              392  JUMP_FORWARD        404  'to 404'
            394_0  COME_FROM           386  '386'

 L. 654       394  LOAD_FAST                'self'
              396  LOAD_ATTR                limit
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                bytes_read
              402  BINARY_SUBTRACT  
            404_0  COME_FROM           392  '392'

 L. 653       404  STORE_FAST               'limit'

 L. 655       406  LOAD_FAST                'klass'
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                fp
              412  LOAD_FAST                'headers'
              414  LOAD_FAST                'ib'
              416  LOAD_FAST                'environ'
              418  LOAD_FAST                'keep_blank_values'

 L. 656       420  LOAD_FAST                'strict_parsing'

 L. 656       422  LOAD_FAST                'limit'

 L. 657       424  LOAD_FAST                'self'
              426  LOAD_ATTR                encoding

 L. 657       428  LOAD_FAST                'self'
              430  LOAD_ATTR                errors

 L. 657       432  LOAD_FAST                'max_num_fields'

 L. 657       434  LOAD_FAST                'self'
              436  LOAD_ATTR                separator

 L. 655       438  CALL_FUNCTION_11     11  ''
              440  STORE_FAST               'part'

 L. 659       442  LOAD_FAST                'max_num_fields'
              444  LOAD_CONST               None
              446  COMPARE_OP               is-not
          448_450  POP_JUMP_IF_FALSE   500  'to 500'

 L. 660       452  LOAD_FAST                'max_num_fields'
              454  LOAD_CONST               1
              456  INPLACE_SUBTRACT 
              458  STORE_FAST               'max_num_fields'

 L. 661       460  LOAD_FAST                'part'
              462  LOAD_ATTR                list
          464_466  POP_JUMP_IF_FALSE   482  'to 482'

 L. 662       468  LOAD_FAST                'max_num_fields'
              470  LOAD_GLOBAL              len
              472  LOAD_FAST                'part'
              474  LOAD_ATTR                list
              476  CALL_FUNCTION_1       1  ''
              478  INPLACE_SUBTRACT 
              480  STORE_FAST               'max_num_fields'
            482_0  COME_FROM           464  '464'

 L. 663       482  LOAD_FAST                'max_num_fields'
              484  LOAD_CONST               0
              486  COMPARE_OP               <
          488_490  POP_JUMP_IF_FALSE   500  'to 500'

 L. 664       492  LOAD_GLOBAL              ValueError
              494  LOAD_STR                 'Max number of fields exceeded'
              496  CALL_FUNCTION_1       1  ''
              498  RAISE_VARARGS_1       1  'exception instance'
            500_0  COME_FROM           488  '488'
            500_1  COME_FROM           448  '448'

 L. 666       500  LOAD_FAST                'self'
              502  DUP_TOP          
              504  LOAD_ATTR                bytes_read
              506  LOAD_FAST                'part'
              508  LOAD_ATTR                bytes_read
              510  INPLACE_ADD      
              512  ROT_TWO          
              514  STORE_ATTR               bytes_read

 L. 667       516  LOAD_FAST                'self'
              518  LOAD_ATTR                list
              520  LOAD_METHOD              append
              522  LOAD_FAST                'part'
              524  CALL_METHOD_1         1  ''
              526  POP_TOP          

 L. 668       528  LOAD_FAST                'part'
              530  LOAD_ATTR                done
          532_534  POP_JUMP_IF_TRUE    576  'to 576'
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                bytes_read
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                length
              544  DUP_TOP          
              546  ROT_THREE        
              548  COMPARE_OP               >=
          550_552  POP_JUMP_IF_FALSE   564  'to 564'
              554  LOAD_CONST               0
              556  COMPARE_OP               >
          558_560  POP_JUMP_IF_FALSE_BACK   258  'to 258'
              562  JUMP_FORWARD        576  'to 576'
            564_0  COME_FROM           550  '550'
              564  POP_TOP          
              566  JUMP_BACK           258  'to 258'

 L. 669   568_570  JUMP_FORWARD        576  'to 576'
          572_574  JUMP_BACK           258  'to 258'
            576_0  COME_FROM           568  '568'
            576_1  COME_FROM           562  '562'
            576_2  COME_FROM           532  '532'
            576_3  COME_FROM           310  '310'

 L. 670       576  LOAD_FAST                'self'
              578  LOAD_METHOD              skip_lines
              580  CALL_METHOD_0         0  ''
              582  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 300_302

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
            line = 0 <= self.limit <= _read if self.limit is not None else self.fp.readline(65536)
            self.bytes_read += len(line)
            _read += len(line)
            if not line:
                self.done = -1
            else:
                pass
            if delim == b'\r':
                line = delim + line
                delim = b''
            else:
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