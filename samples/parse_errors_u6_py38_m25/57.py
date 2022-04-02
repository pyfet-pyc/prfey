# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: plistlib.py
r"""plistlib.py -- a tool to generate and parse MacOSX .plist files.

The property list (.plist) file format is a simple XML pickle supporting
basic object types, like dictionaries, lists, numbers and strings.
Usually the top level object is a dictionary.

To write out a plist file, use the dump(value, file)
function. 'value' is the top level object, 'file' is
a (writable) file object.

To parse a plist from a file, use the load(file) function,
with a (readable) file object as the only argument. It
returns the top level object (again, usually a dictionary).

To work with plist data in bytes objects, you can use loads()
and dumps().

Values can be strings, integers, floats, booleans, tuples, lists,
dictionaries (but only with string keys), Data, bytes, bytearray, or
datetime.datetime objects.

Generate Plist example:

    pl = dict(
        aString = "Doodah",
        aList = ["A", "B", 12, 32.1, [1, 2, 3]],
        aFloat = 0.1,
        anInt = 728,
        aDict = dict(
            anotherString = "<hello & hi there!>",
            aUnicodeValue = "M\xe4ssig, Ma\xdf",
            aTrueValue = True,
            aFalseValue = False,
        ),
        someData = b"<binary gunk>",
        someMoreData = b"<lots of binary gunk>" * 10,
        aDate = datetime.datetime.fromtimestamp(time.mktime(time.gmtime())),
    )
    with open(fileName, 'wb') as fp:
        dump(pl, fp)

Parse Plist example:

    with open(fileName, 'rb') as fp:
        pl = load(fp)
    print(pl["aKey"])
"""
__all__ = [
 'readPlist', 'writePlist', 'readPlistFromBytes', 'writePlistToBytes',
 'Data', 'InvalidFileException', 'FMT_XML', 'FMT_BINARY',
 'load', 'dump', 'loads', 'dumps', 'UID']
import binascii, codecs, contextlib, datetime, enum
from io import BytesIO
import itertools, os, re, struct
from warnings import warn
from xml.parsers.expat import ParserCreate
PlistFormat = enum.Enum('PlistFormat', 'FMT_XML FMT_BINARY', module=__name__)
globals().update(PlistFormat.__members__)

@contextlib.contextmanager
def _maybe_open(pathOrFile, mode):
    if isinstance(pathOrFile, str):
        with open(pathOrFile, mode) as (fp):
            yield fp
    else:
        yield pathOrFile


def readPlist--- This code section failed: ---

 L.  96         0  LOAD_GLOBAL              warn
                2  LOAD_STR                 'The readPlist function is deprecated, use load() instead'

 L.  97         4  LOAD_GLOBAL              DeprecationWarning

 L.  97         6  LOAD_CONST               2

 L.  96         8  CALL_FUNCTION_3       3  ''
               10  POP_TOP          

 L.  99        12  LOAD_GLOBAL              _maybe_open
               14  LOAD_FAST                'pathOrFile'
               16  LOAD_STR                 'rb'
               18  CALL_FUNCTION_2       2  ''
               20  SETUP_WITH           50  'to 50'
               22  STORE_FAST               'fp'

 L. 100        24  LOAD_GLOBAL              load
               26  LOAD_FAST                'fp'
               28  LOAD_CONST               None
               30  LOAD_CONST               False
               32  LOAD_CONST               ('fmt', 'use_builtin_types')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH       20  '20'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38


def writePlist(value, pathOrFile):
    """
    Write 'value' to a .plist file. 'pathOrFile' may either be a
    file name or a (writable) file object.

    This function is deprecated, use dump instead.
    """
    warn('The writePlist function is deprecated, use dump() instead', DeprecationWarning, 2)
    with _maybe_open(pathOrFile, 'wb') as (fp):
        dump(value, fp, fmt=FMT_XML, sort_keys=True, skipkeys=False)


def readPlistFromBytes(data):
    """
    Read a plist data from a bytes object. Return the root object.

    This function is deprecated, use loads instead.
    """
    warn('The readPlistFromBytes function is deprecated, use loads() instead', DeprecationWarning, 2)
    return load((BytesIO(data)), fmt=None, use_builtin_types=False)


def writePlistToBytes(value):
    """
    Return 'value' as a plist-formatted bytes object.

    This function is deprecated, use dumps instead.
    """
    warn('The writePlistToBytes function is deprecated, use dumps() instead', DeprecationWarning, 2)
    f = BytesIO()
    dump(value, f, fmt=FMT_XML, sort_keys=True, skipkeys=False)
    return f.getvalue()


class Data:
    __doc__ = '\n    Wrapper for binary data.\n\n    This class is deprecated, use a bytes object instead.\n    '

    def __init__(self, data):
        if not isinstance(data, bytes):
            raise TypeError('data must be as bytes')
        self.data = data

    @classmethod
    def fromBase64(cls, data):
        return cls(_decode_base64(data))

    def asBase64(self, maxlinelength=76):
        return _encode_base64(self.data, maxlinelength)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        if isinstance(other, bytes):
            return self.data == other
        return NotImplemented

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.data))


class UID:

    def __init__(self, data):
        if not isinstance(data, int):
            raise TypeError('data must be an int')
        if data >= 18446744073709551616:
            raise ValueError('UIDs cannot be >= 2**64')
        if data < 0:
            raise ValueError('UIDs must be positive')
        self.data = data

    def __index__(self):
        return self.data

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.data))

    def __reduce__(self):
        return (
         self.__class__, (self.data,))

    def __eq__(self, other):
        if not isinstance(other, UID):
            return NotImplemented
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)


PLISTHEADER = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
_controlCharPat = re.compile('[\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\x0b\\x0c\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a\\x1b\\x1c\\x1d\\x1e\\x1f]')

def _encode_base64(s, maxlinelength=76):
    maxbinsize = maxlinelength // 4 * 3
    pieces = []
    for i in range(0, len(s), maxbinsize):
        chunk = s[i:i + maxbinsize]
        pieces.append(binascii.b2a_base64(chunk))
    else:
        return (b'').join(pieces)


def _decode_base64(s):
    if isinstance(s, str):
        return binascii.a2b_base64(s.encode('utf-8'))
    return binascii.a2b_base64(s)


_dateParser = re.compile('(?P<year>\\d\\d\\d\\d)(?:-(?P<month>\\d\\d)(?:-(?P<day>\\d\\d)(?:T(?P<hour>\\d\\d)(?::(?P<minute>\\d\\d)(?::(?P<second>\\d\\d))?)?)?)?)?Z', re.ASCII)

def _date_from_string(s):
    order = ('year', 'month', 'day', 'hour', 'minute', 'second')
    gd = _dateParser.match(s).groupdict()
    lst = []
    for key in order:
        val = gd[key]
        if val is None:
            break
        lst.append(int(val))
    else:
        return (datetime.datetime)(*lst)


def _date_to_string(d):
    return '%04d-%02d-%02dT%02d:%02d:%02dZ' % (
     d.year, d.month, d.day,
     d.hour, d.minute, d.second)


def _escape(text):
    m = _controlCharPat.search(text)
    if m is not None:
        raise ValueError("strings can't contains control characters; use bytes instead")
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


class _PlistParser:

    def __init__(self, use_builtin_types, dict_type):
        self.stack = []
        self.current_key = None
        self.root = None
        self._use_builtin_types = use_builtin_types
        self._dict_type = dict_type

    def parse(self, fileobj):
        self.parser = ParserCreate()
        self.parser.StartElementHandler = self.handle_begin_element
        self.parser.EndElementHandler = self.handle_end_element
        self.parser.CharacterDataHandler = self.handle_data
        self.parser.ParseFile(fileobj)
        return self.root

    def handle_begin_element(self, element, attrs):
        self.data = []
        handler = getattr(self, 'begin_' + element, None)
        if handler is not None:
            handler(attrs)

    def handle_end_element(self, element):
        handler = getattr(self, 'end_' + element, None)
        if handler is not None:
            handler()

    def handle_data(self, data):
        self.data.append(data)

    def add_object(self, value):
        if self.current_key is not None:
            if not isinstance(self.stack[(-1)], type({})):
                raise ValueError('unexpected element at line %d' % self.parser.CurrentLineNumber)
            self.stack[(-1)][self.current_key] = value
            self.current_key = None
        else:
            if not self.stack:
                self.root = value
            else:
                if not isinstance(self.stack[(-1)], type([])):
                    raise ValueError('unexpected element at line %d' % self.parser.CurrentLineNumber)
                self.stack[(-1)].append(value)

    def get_data(self):
        data = ''.join(self.data)
        self.data = []
        return data

    def begin_dict(self, attrs):
        d = self._dict_type()
        self.add_object(d)
        self.stack.append(d)

    def end_dict(self):
        if self.current_key:
            raise ValueError("missing value for key '%s' at line %d" % (
             self.current_key, self.parser.CurrentLineNumber))
        self.stack.pop()

    def end_key(self):
        if not (self.current_key or isinstance(self.stack[(-1)], type({}))):
            raise ValueError('unexpected key at line %d' % self.parser.CurrentLineNumber)
        self.current_key = self.get_data()

    def begin_array(self, attrs):
        a = []
        self.add_object(a)
        self.stack.append(a)

    def end_array(self):
        self.stack.pop()

    def end_true(self):
        self.add_object(True)

    def end_false(self):
        self.add_object(False)

    def end_integer(self):
        self.add_object(int(self.get_data()))

    def end_real(self):
        self.add_object(float(self.get_data()))

    def end_string(self):
        self.add_object(self.get_data())

    def end_data(self):
        if self._use_builtin_types:
            self.add_object(_decode_base64(self.get_data()))
        else:
            self.add_object(Data.fromBase64(self.get_data()))

    def end_date(self):
        self.add_object(_date_from_string(self.get_data()))


class _DumbXMLWriter:

    def __init__(self, file, indent_level=0, indent='\t'):
        self.file = file
        self.stack = []
        self._indent_level = indent_level
        self.indent = indent

    def begin_element(self, element):
        self.stack.append(element)
        self.writeln('<%s>' % element)
        self._indent_level += 1

    def end_element(self, element):
        assert self._indent_level > 0
        assert self.stack.pop() == element
        self._indent_level -= 1
        self.writeln('</%s>' % element)

    def simple_element(self, element, value=None):
        if value is not None:
            value = _escape(value)
            self.writeln('<%s>%s</%s>' % (element, value, element))
        else:
            self.writeln('<%s/>' % element)

    def writeln(self, line):
        if line:
            if isinstance(line, str):
                line = line.encode('utf-8')
            self.file.write(self._indent_level * self.indent)
            self.file.write(line)
        self.file.write(b'\n')


class _PlistWriter(_DumbXMLWriter):

    def __init__(self, file, indent_level=0, indent=b'\t', writeHeader=1, sort_keys=True, skipkeys=False):
        if writeHeader:
            file.write(PLISTHEADER)
        _DumbXMLWriter.__init__(self, file, indent_level, indent)
        self._sort_keys = sort_keys
        self._skipkeys = skipkeys

    def write(self, value):
        self.writeln('<plist version="1.0">')
        self.write_value(value)
        self.writeln('</plist>')

    def write_value(self, value):
        if isinstance(value, str):
            self.simple_element('string', value)
        else:
            if value is True:
                self.simple_element('true')
            else:
                if value is False:
                    self.simple_element('false')
                else:
                    if isinstance(value, int):
                        if -9223372036854775808 <= value < 18446744073709551616:
                            self.simple_element('integer', '%d' % value)
                        else:
                            raise OverflowError(value)
                    else:
                        if isinstance(value, float):
                            self.simple_element('real', repr(value))
                        else:
                            if isinstance(value, dict):
                                self.write_dict(value)
                            else:
                                if isinstance(value, Data):
                                    self.write_data(value)
                                else:
                                    if isinstance(value, (bytes, bytearray)):
                                        self.write_bytes(value)
                                    else:
                                        if isinstance(value, datetime.datetime):
                                            self.simple_element('date', _date_to_string(value))
                                        else:
                                            if isinstance(value, (tuple, list)):
                                                self.write_array(value)
                                            else:
                                                raise TypeError('unsupported type: %s' % type(value))

    def write_data(self, data):
        self.write_bytes(data.data)

    def write_bytes(self, data):
        self.begin_element('data')
        self._indent_level -= 1
        maxlinelength = max(16, 76 - len(self.indent.replace(b'\t', b'        ') * self._indent_level))
        for line in _encode_base64(data, maxlinelength).split(b'\n'):
            if line:
                self.writeln(line)
            self._indent_level += 1
            self.end_element('data')

    def write_dict(self, d):
        if d:
            self.begin_element('dict')
            if self._sort_keys:
                items = sorted(d.items())
            else:
                items = d.items()
            for key, value in items:
                if not isinstance(key, str):
                    if self._skipkeys:
                        pass
                    else:
                        raise TypeError('keys must be strings')
                self.simple_element('key', key)
                self.write_value(value)
            else:
                self.end_element('dict')

        else:
            self.simple_element('dict')

    def write_array(self, array):
        if array:
            self.begin_element('array')
            for value in array:
                self.write_value(value)
            else:
                self.end_element('array')

        else:
            self.simple_element('array')


def _is_fmt_xml(header):
    prefixes = (b'<?xml', b'<plist')
    for pfx in prefixes:
        if header.startswith(pfx):
            return True

    for bom, encoding in (
     (
      codecs.BOM_UTF8, 'utf-8'),
     (
      codecs.BOM_UTF16_BE, 'utf-16-be'),
     (
      codecs.BOM_UTF16_LE, 'utf-16-le')):
        if not header.startswith(bom):
            pass
        else:
            for start in prefixes:
                prefix = bom + start.decode('ascii').encode(encoding)
                if header[:len(prefix)] == prefix:
                    return True
            else:
                return False


class InvalidFileException(ValueError):

    def __init__(self, message='Invalid file'):
        ValueError.__init__(self, message)


_BINARY_FORMAT = {1:'B', 
 2:'H',  4:'L',  8:'Q'}
_undefined = object()

class _BinaryPlistParser:
    __doc__ = '\n    Read or write a binary plist file, following the description of the binary\n    format.  Raise InvalidFileException in case of error, otherwise return the\n    root object.\n\n    see also: http://opensource.apple.com/source/CF/CF-744.18/CFBinaryPList.c\n    '

    def __init__(self, use_builtin_types, dict_type):
        self._use_builtin_types = use_builtin_types
        self._dict_type = dict_type

    def parse--- This code section failed: ---

 L. 571         0  SETUP_FINALLY       128  'to 128'

 L. 577         2  LOAD_FAST                'fp'
                4  LOAD_FAST                'self'
                6  STORE_ATTR               _fp

 L. 578         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _fp
               12  LOAD_METHOD              seek
               14  LOAD_CONST               -32
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                SEEK_END
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          

 L. 579        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _fp
               28  LOAD_METHOD              read
               30  LOAD_CONST               32
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'trailer'

 L. 580        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'trailer'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               32
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 581        48  LOAD_GLOBAL              InvalidFileException
               50  CALL_FUNCTION_0       0  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            46  '46'

 L. 585        54  LOAD_GLOBAL              struct
               56  LOAD_METHOD              unpack
               58  LOAD_STR                 '>6xBBQQQ'
               60  LOAD_FAST                'trailer'
               62  CALL_METHOD_2         2  ''

 L. 582        64  UNPACK_SEQUENCE_5     5 

 L. 583        66  STORE_FAST               'offset_size'

 L. 583        68  LOAD_FAST                'self'
               70  STORE_ATTR               _ref_size

 L. 583        72  STORE_FAST               'num_objects'

 L. 583        74  STORE_FAST               'top_object'

 L. 584        76  STORE_FAST               'offset_table_offset'

 L. 586        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _fp
               82  LOAD_METHOD              seek
               84  LOAD_FAST                'offset_table_offset'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 587        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _read_ints
               94  LOAD_FAST                'num_objects'
               96  LOAD_FAST                'offset_size'
               98  CALL_METHOD_2         2  ''
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _object_offsets

 L. 588       104  LOAD_GLOBAL              _undefined
              106  BUILD_LIST_1          1 
              108  LOAD_FAST                'num_objects'
              110  BINARY_MULTIPLY  
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _objects

 L. 589       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _read_object
              120  LOAD_FAST                'top_object'
              122  CALL_METHOD_1         1  ''
              124  POP_BLOCK        
              126  RETURN_VALUE     
            128_0  COME_FROM_FINALLY     0  '0'

 L. 591       128  DUP_TOP          
              130  LOAD_GLOBAL              OSError
              132  LOAD_GLOBAL              IndexError
              134  LOAD_GLOBAL              struct
              136  LOAD_ATTR                error
              138  LOAD_GLOBAL              OverflowError

 L. 592       140  LOAD_GLOBAL              UnicodeDecodeError

 L. 591       142  BUILD_TUPLE_5         5 
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   164  'to 164'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 593       154  LOAD_GLOBAL              InvalidFileException
              156  CALL_FUNCTION_0       0  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           146  '146'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'

Parse error at or near `POP_TOP' instruction at offset 150

    def _get_size(self, tokenL):
        """ return the size of the next object."""
        if tokenL == 15:
            m = self._fp.read(1)[0] & 3
            s = 1 << m
            f = '>' + _BINARY_FORMAT[s]
            return struct.unpack(f, self._fp.read(s))[0]
        return tokenL

    def _read_ints(self, n, size):
        data = self._fp.read(size * n)
        if size in _BINARY_FORMAT:
            return struct.unpack('>' + _BINARY_FORMAT[size] * n, data)
        if not size or len(data) != size * n:
            raise InvalidFileException()
        return tuple((int.from_bytes(data[i:i + size], 'big') for i in range(0, size * n, size)))

    def _read_refs(self, n):
        return self._read_ints(n, self._ref_size)

    def _read_object--- This code section failed: ---

 L. 624         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _objects
                4  LOAD_FAST                'ref'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'result'

 L. 625        10  LOAD_FAST                'result'
               12  LOAD_GLOBAL              _undefined
               14  COMPARE_OP               is-not
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 626        18  LOAD_FAST                'result'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 628        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                _object_offsets
               26  LOAD_FAST                'ref'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'offset'

 L. 629        32  LOAD_DEREF               'self'
               34  LOAD_ATTR                _fp
               36  LOAD_METHOD              seek
               38  LOAD_FAST                'offset'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 630        44  LOAD_DEREF               'self'
               46  LOAD_ATTR                _fp
               48  LOAD_METHOD              read
               50  LOAD_CONST               1
               52  CALL_METHOD_1         1  ''
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  STORE_FAST               'token'

 L. 631        60  LOAD_FAST                'token'
               62  LOAD_CONST               240
               64  BINARY_AND       
               66  LOAD_FAST                'token'
               68  LOAD_CONST               15
               70  BINARY_AND       
               72  ROT_TWO          
               74  STORE_FAST               'tokenH'
               76  STORE_FAST               'tokenL'

 L. 633        78  LOAD_FAST                'token'
               80  LOAD_CONST               0
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 634        86  LOAD_CONST               None
               88  STORE_FAST               'result'
            90_92  JUMP_FORWARD        690  'to 690'
             94_0  COME_FROM            84  '84'

 L. 636        94  LOAD_FAST                'token'
               96  LOAD_CONST               8
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L. 637       102  LOAD_CONST               False
              104  STORE_FAST               'result'
          106_108  JUMP_FORWARD        690  'to 690'
            110_0  COME_FROM           100  '100'

 L. 639       110  LOAD_FAST                'token'
              112  LOAD_CONST               9
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 640       118  LOAD_CONST               True
              120  STORE_FAST               'result'
          122_124  JUMP_FORWARD        690  'to 690'
            126_0  COME_FROM           116  '116'

 L. 645       126  LOAD_FAST                'token'
              128  LOAD_CONST               15
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 646       134  LOAD_CONST               b''
              136  STORE_FAST               'result'
          138_140  JUMP_FORWARD        690  'to 690'
            142_0  COME_FROM           132  '132'

 L. 648       142  LOAD_FAST                'tokenH'
              144  LOAD_CONST               16
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   186  'to 186'

 L. 649       150  LOAD_GLOBAL              int
              152  LOAD_ATTR                from_bytes
              154  LOAD_DEREF               'self'
              156  LOAD_ATTR                _fp
              158  LOAD_METHOD              read
              160  LOAD_CONST               1
              162  LOAD_FAST                'tokenL'
              164  BINARY_LSHIFT    
              166  CALL_METHOD_1         1  ''

 L. 650       168  LOAD_STR                 'big'

 L. 650       170  LOAD_FAST                'tokenL'
              172  LOAD_CONST               3
              174  COMPARE_OP               >=

 L. 649       176  LOAD_CONST               ('signed',)
              178  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              180  STORE_FAST               'result'
          182_184  JUMP_FORWARD        690  'to 690'
            186_0  COME_FROM           148  '148'

 L. 652       186  LOAD_FAST                'token'
              188  LOAD_CONST               34
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   222  'to 222'

 L. 653       194  LOAD_GLOBAL              struct
              196  LOAD_METHOD              unpack
              198  LOAD_STR                 '>f'
              200  LOAD_DEREF               'self'
              202  LOAD_ATTR                _fp
              204  LOAD_METHOD              read
              206  LOAD_CONST               4
              208  CALL_METHOD_1         1  ''
              210  CALL_METHOD_2         2  ''
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  STORE_FAST               'result'
          218_220  JUMP_FORWARD        690  'to 690'
            222_0  COME_FROM           192  '192'

 L. 655       222  LOAD_FAST                'token'
              224  LOAD_CONST               35
              226  COMPARE_OP               ==
          228_230  POP_JUMP_IF_FALSE   260  'to 260'

 L. 656       232  LOAD_GLOBAL              struct
              234  LOAD_METHOD              unpack
              236  LOAD_STR                 '>d'
              238  LOAD_DEREF               'self'
              240  LOAD_ATTR                _fp
              242  LOAD_METHOD              read
              244  LOAD_CONST               8
              246  CALL_METHOD_1         1  ''
              248  CALL_METHOD_2         2  ''
              250  LOAD_CONST               0
              252  BINARY_SUBSCR    
              254  STORE_FAST               'result'
          256_258  JUMP_FORWARD        690  'to 690'
            260_0  COME_FROM           228  '228'

 L. 658       260  LOAD_FAST                'token'
              262  LOAD_CONST               51
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   324  'to 324'

 L. 659       270  LOAD_GLOBAL              struct
              272  LOAD_METHOD              unpack
              274  LOAD_STR                 '>d'
              276  LOAD_DEREF               'self'
              278  LOAD_ATTR                _fp
              280  LOAD_METHOD              read
              282  LOAD_CONST               8
              284  CALL_METHOD_1         1  ''
              286  CALL_METHOD_2         2  ''
              288  LOAD_CONST               0
              290  BINARY_SUBSCR    
              292  STORE_FAST               'f'

 L. 662       294  LOAD_GLOBAL              datetime
              296  LOAD_METHOD              datetime
              298  LOAD_CONST               2001
              300  LOAD_CONST               1
              302  LOAD_CONST               1
              304  CALL_METHOD_3         3  ''

 L. 663       306  LOAD_GLOBAL              datetime
              308  LOAD_ATTR                timedelta
              310  LOAD_FAST                'f'
              312  LOAD_CONST               ('seconds',)
              314  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 662       316  BINARY_ADD       
              318  STORE_FAST               'result'
          320_322  JUMP_FORWARD        690  'to 690'
            324_0  COME_FROM           266  '266'

 L. 665       324  LOAD_FAST                'tokenH'
              326  LOAD_CONST               64
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   386  'to 386'

 L. 666       334  LOAD_DEREF               'self'
              336  LOAD_METHOD              _get_size
              338  LOAD_FAST                'tokenL'
              340  CALL_METHOD_1         1  ''
              342  STORE_FAST               's'

 L. 667       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                _use_builtin_types
          348_350  POP_JUMP_IF_FALSE   366  'to 366'

 L. 668       352  LOAD_DEREF               'self'
              354  LOAD_ATTR                _fp
              356  LOAD_METHOD              read
              358  LOAD_FAST                's'
              360  CALL_METHOD_1         1  ''
              362  STORE_FAST               'result'
              364  JUMP_FORWARD        690  'to 690'
            366_0  COME_FROM           348  '348'

 L. 670       366  LOAD_GLOBAL              Data
              368  LOAD_DEREF               'self'
              370  LOAD_ATTR                _fp
              372  LOAD_METHOD              read
              374  LOAD_FAST                's'
              376  CALL_METHOD_1         1  ''
              378  CALL_FUNCTION_1       1  ''
              380  STORE_FAST               'result'
          382_384  JUMP_FORWARD        690  'to 690'
            386_0  COME_FROM           330  '330'

 L. 672       386  LOAD_FAST                'tokenH'
              388  LOAD_CONST               80
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   428  'to 428'

 L. 673       396  LOAD_DEREF               'self'
              398  LOAD_METHOD              _get_size
              400  LOAD_FAST                'tokenL'
              402  CALL_METHOD_1         1  ''
              404  STORE_FAST               's'

 L. 674       406  LOAD_DEREF               'self'
              408  LOAD_ATTR                _fp
              410  LOAD_METHOD              read
              412  LOAD_FAST                's'
              414  CALL_METHOD_1         1  ''
              416  LOAD_METHOD              decode
              418  LOAD_STR                 'ascii'
              420  CALL_METHOD_1         1  ''
              422  STORE_FAST               'result'
          424_426  JUMP_FORWARD        690  'to 690'
            428_0  COME_FROM           392  '392'

 L. 676       428  LOAD_FAST                'tokenH'
              430  LOAD_CONST               96
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE   472  'to 472'

 L. 677       438  LOAD_DEREF               'self'
              440  LOAD_METHOD              _get_size
              442  LOAD_FAST                'tokenL'
              444  CALL_METHOD_1         1  ''
              446  STORE_FAST               's'

 L. 678       448  LOAD_DEREF               'self'
              450  LOAD_ATTR                _fp
              452  LOAD_METHOD              read
              454  LOAD_FAST                's'
              456  LOAD_CONST               2
              458  BINARY_MULTIPLY  
              460  CALL_METHOD_1         1  ''
              462  LOAD_METHOD              decode
              464  LOAD_STR                 'utf-16be'
              466  CALL_METHOD_1         1  ''
              468  STORE_FAST               'result'
              470  JUMP_FORWARD        690  'to 690'
            472_0  COME_FROM           434  '434'

 L. 680       472  LOAD_FAST                'tokenH'
              474  LOAD_CONST               128
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   512  'to 512'

 L. 682       482  LOAD_GLOBAL              UID
              484  LOAD_GLOBAL              int
              486  LOAD_METHOD              from_bytes
              488  LOAD_DEREF               'self'
              490  LOAD_ATTR                _fp
              492  LOAD_METHOD              read
              494  LOAD_CONST               1
              496  LOAD_FAST                'tokenL'
              498  BINARY_ADD       
              500  CALL_METHOD_1         1  ''
              502  LOAD_STR                 'big'
              504  CALL_METHOD_2         2  ''
              506  CALL_FUNCTION_1       1  ''
              508  STORE_FAST               'result'
              510  JUMP_FORWARD        690  'to 690'
            512_0  COME_FROM           478  '478'

 L. 684       512  LOAD_FAST                'tokenH'
              514  LOAD_CONST               160
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   582  'to 582'

 L. 685       522  LOAD_DEREF               'self'
              524  LOAD_METHOD              _get_size
              526  LOAD_FAST                'tokenL'
              528  CALL_METHOD_1         1  ''
              530  STORE_FAST               's'

 L. 686       532  LOAD_DEREF               'self'
              534  LOAD_METHOD              _read_refs
              536  LOAD_FAST                's'
              538  CALL_METHOD_1         1  ''
              540  STORE_FAST               'obj_refs'

 L. 687       542  BUILD_LIST_0          0 
              544  STORE_FAST               'result'

 L. 688       546  LOAD_FAST                'result'
              548  LOAD_DEREF               'self'
              550  LOAD_ATTR                _objects
              552  LOAD_FAST                'ref'
              554  STORE_SUBSCR     

 L. 689       556  LOAD_FAST                'result'
              558  LOAD_METHOD              extend
              560  LOAD_CLOSURE             'self'
              562  BUILD_TUPLE_1         1 
              564  LOAD_GENEXPR             '<code_object <genexpr>>'
              566  LOAD_STR                 '_BinaryPlistParser._read_object.<locals>.<genexpr>'
              568  MAKE_FUNCTION_8          'closure'
              570  LOAD_FAST                'obj_refs'
              572  GET_ITER         
              574  CALL_FUNCTION_1       1  ''
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
              580  JUMP_FORWARD        690  'to 690'
            582_0  COME_FROM           518  '518'

 L. 697       582  LOAD_FAST                'tokenH'
              584  LOAD_CONST               208
              586  COMPARE_OP               ==
          588_590  POP_JUMP_IF_FALSE   684  'to 684'

 L. 698       592  LOAD_DEREF               'self'
              594  LOAD_METHOD              _get_size
              596  LOAD_FAST                'tokenL'
              598  CALL_METHOD_1         1  ''
              600  STORE_FAST               's'

 L. 699       602  LOAD_DEREF               'self'
              604  LOAD_METHOD              _read_refs
              606  LOAD_FAST                's'
              608  CALL_METHOD_1         1  ''
              610  STORE_FAST               'key_refs'

 L. 700       612  LOAD_DEREF               'self'
              614  LOAD_METHOD              _read_refs
              616  LOAD_FAST                's'
              618  CALL_METHOD_1         1  ''
              620  STORE_FAST               'obj_refs'

 L. 701       622  LOAD_DEREF               'self'
              624  LOAD_METHOD              _dict_type
              626  CALL_METHOD_0         0  ''
              628  STORE_FAST               'result'

 L. 702       630  LOAD_FAST                'result'
              632  LOAD_DEREF               'self'
              634  LOAD_ATTR                _objects
              636  LOAD_FAST                'ref'
              638  STORE_SUBSCR     

 L. 703       640  LOAD_GLOBAL              zip
              642  LOAD_FAST                'key_refs'
              644  LOAD_FAST                'obj_refs'
              646  CALL_FUNCTION_2       2  ''
              648  GET_ITER         
              650  FOR_ITER            682  'to 682'
              652  UNPACK_SEQUENCE_2     2 
              654  STORE_FAST               'k'
              656  STORE_FAST               'o'

 L. 704       658  LOAD_DEREF               'self'
              660  LOAD_METHOD              _read_object
              662  LOAD_FAST                'o'
              664  CALL_METHOD_1         1  ''
              666  LOAD_FAST                'result'
              668  LOAD_DEREF               'self'
            670_0  COME_FROM           364  '364'
              670  LOAD_METHOD              _read_object
              672  LOAD_FAST                'k'
              674  CALL_METHOD_1         1  ''
              676  STORE_SUBSCR     
          678_680  JUMP_BACK           650  'to 650'
              682  JUMP_FORWARD        690  'to 690'
            684_0  COME_FROM           588  '588'

 L. 707       684  LOAD_GLOBAL              InvalidFileException
              686  CALL_FUNCTION_0       0  ''
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           682  '682'
            690_1  COME_FROM           580  '580'
            690_2  COME_FROM           510  '510'
            690_3  COME_FROM           470  '470'
            690_4  COME_FROM           424  '424'
            690_5  COME_FROM           382  '382'
            690_6  COME_FROM           320  '320'
            690_7  COME_FROM           256  '256'
            690_8  COME_FROM           218  '218'
            690_9  COME_FROM           182  '182'
           690_10  COME_FROM           138  '138'
           690_11  COME_FROM           122  '122'
           690_12  COME_FROM           106  '106'
           690_13  COME_FROM            90  '90'

 L. 709       690  LOAD_FAST                'result'
              692  LOAD_DEREF               'self'
              694  LOAD_ATTR                _objects
              696  LOAD_FAST                'ref'
              698  STORE_SUBSCR     

 L. 710       700  LOAD_FAST                'result'
              702  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 670_0


def _count_to_size(count):
    if count < 256:
        return 1
    if count < 65536:
        return 2
    if count << 1 << 32:
        return 4
    return 8


_scalars = (
 str, int, float, datetime.datetime, bytes)

class _BinaryPlistWriter(object):

    def __init__(self, fp, sort_keys, skipkeys):
        self._fp = fp
        self._sort_keys = sort_keys
        self._skipkeys = skipkeys

    def write(self, value):
        self._objlist = []
        self._objtable = {}
        self._objidtable = {}
        self._flatten(value)
        num_objects = len(self._objlist)
        self._object_offsets = [0] * num_objects
        self._ref_size = _count_to_size(num_objects)
        self._ref_format = _BINARY_FORMAT[self._ref_size]
        self._fp.write(b'bplist00')
        for obj in self._objlist:
            self._write_object(obj)
        else:
            top_object = self._getrefnum(value)
            offset_table_offset = self._fp.tell()
            offset_size = _count_to_size(offset_table_offset)
            offset_format = '>' + _BINARY_FORMAT[offset_size] * num_objects
            self._fp.write((struct.pack)(offset_format, *self._object_offsets))
            sort_version = 0
            trailer = (
             sort_version, offset_size, self._ref_size, num_objects,
             top_object, offset_table_offset)
            self._fp.write((struct.pack)(*('>5xBBBQQQ', ), *trailer))

    def _flatten(self, value):
        if isinstance(value, _scalars):
            if (
             type(value), value) in self._objtable:
                return
        elif isinstance(value, Data):
            if (
             type(value.data), value.data) in self._objtable:
                return
            else:
                if id(value) in self._objidtable:
                    return
        else:
            refnum = len(self._objlist)
            self._objlist.append(value)
            if isinstance(value, _scalars):
                self._objtable[(type(value), value)] = refnum
            else:
                if isinstance(value, Data):
                    self._objtable[(type(value.data), value.data)] = refnum
                else:
                    self._objidtable[id(value)] = refnum
        if isinstance(value, dict):
            keys = []
            values = []
            items = value.items()
            if self._sort_keys:
                items = sorted(items)
            for k, v in items:
                if not isinstance(k, str):
                    if self._skipkeys:
                        pass
                    else:
                        raise TypeError('keys must be strings')
                keys.append(k)
                values.append(v)
            else:
                for o in itertools.chain(keys, values):
                    self._flatten(o)

        else:
            if isinstance(value, (list, tuple)):
                for o in value:
                    self._flatten(o)

    def _getrefnum(self, value):
        if isinstance(value, _scalars):
            return self._objtable[(type(value), value)]
        if isinstance(value, Data):
            return self._objtable[(type(value.data), value.data)]
        return self._objidtable[id(value)]

    def _write_size(self, token, size):
        if size < 15:
            self._fp.write(struct.pack('>B', token | size))
        else:
            if size < 256:
                self._fp.write(struct.pack('>BBB', token | 15, 16, size))
            else:
                if size < 65536:
                    self._fp.write(struct.pack('>BBH', token | 15, 17, size))
                else:
                    if size < 4294967296:
                        self._fp.write(struct.pack('>BBL', token | 15, 18, size))
                    else:
                        self._fp.write(struct.pack('>BBQ', token | 15, 19, size))

    def _write_object--- This code section failed: ---

 L. 851         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              _getrefnum
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'ref'

 L. 852        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                _fp
               14  LOAD_METHOD              tell
               16  CALL_METHOD_0         0  ''
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                _object_offsets
               22  LOAD_FAST                'ref'
               24  STORE_SUBSCR     

 L. 853        26  LOAD_FAST                'value'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    50  'to 50'

 L. 854        34  LOAD_DEREF               'self'
               36  LOAD_ATTR                _fp
               38  LOAD_METHOD              write
               40  LOAD_CONST               b'\x00'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
            46_48  JUMP_FORWARD       1182  'to 1182'
             50_0  COME_FROM            32  '32'

 L. 856        50  LOAD_FAST                'value'
               52  LOAD_CONST               False
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    74  'to 74'

 L. 857        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _fp
               62  LOAD_METHOD              write
               64  LOAD_CONST               b'\x08'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
            70_72  JUMP_FORWARD       1182  'to 1182'
             74_0  COME_FROM            56  '56'

 L. 859        74  LOAD_FAST                'value'
               76  LOAD_CONST               True
               78  COMPARE_OP               is
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L. 860        82  LOAD_DEREF               'self'
               84  LOAD_ATTR                _fp
               86  LOAD_METHOD              write
               88  LOAD_CONST               b'\t'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
            94_96  JUMP_FORWARD       1182  'to 1182'
             98_0  COME_FROM            80  '80'

 L. 862        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'value'
              102  LOAD_GLOBAL              int
              104  CALL_FUNCTION_2       2  ''
          106_108  POP_JUMP_IF_FALSE   364  'to 364'

 L. 863       110  LOAD_FAST                'value'
              112  LOAD_CONST               0
              114  COMPARE_OP               <
              116  POP_JUMP_IF_FALSE   180  'to 180'

 L. 864       118  SETUP_FINALLY       146  'to 146'

 L. 865       120  LOAD_DEREF               'self'
              122  LOAD_ATTR                _fp
              124  LOAD_METHOD              write
              126  LOAD_GLOBAL              struct
              128  LOAD_METHOD              pack
              130  LOAD_STR                 '>Bq'
              132  LOAD_CONST               19
              134  LOAD_FAST                'value'
              136  CALL_METHOD_3         3  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  JUMP_FORWARD        178  'to 178'
            146_0  COME_FROM_FINALLY   118  '118'

 L. 866       146  DUP_TOP          
              148  LOAD_GLOBAL              struct
              150  LOAD_ATTR                error
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   176  'to 176'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 867       162  LOAD_GLOBAL              OverflowError
              164  LOAD_FAST                'value'
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_CONST               None
              170  RAISE_VARARGS_2       2  'exception instance with __cause__'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           154  '154'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           144  '144'
              178  JUMP_FORWARD       1182  'to 1182'
            180_0  COME_FROM           116  '116'

 L. 868       180  LOAD_FAST                'value'
              182  LOAD_CONST               256
              184  COMPARE_OP               <
              186  POP_JUMP_IF_FALSE   212  'to 212'

 L. 869       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                _fp
              192  LOAD_METHOD              write
              194  LOAD_GLOBAL              struct
              196  LOAD_METHOD              pack
              198  LOAD_STR                 '>BB'
              200  LOAD_CONST               16
              202  LOAD_FAST                'value'
              204  CALL_METHOD_3         3  ''
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
              210  JUMP_FORWARD       1182  'to 1182'
            212_0  COME_FROM           186  '186'

 L. 870       212  LOAD_FAST                'value'
              214  LOAD_CONST               65536
              216  COMPARE_OP               <
              218  POP_JUMP_IF_FALSE   244  'to 244'

 L. 871       220  LOAD_DEREF               'self'
              222  LOAD_ATTR                _fp
              224  LOAD_METHOD              write
              226  LOAD_GLOBAL              struct
              228  LOAD_METHOD              pack
              230  LOAD_STR                 '>BH'
              232  LOAD_CONST               17
              234  LOAD_FAST                'value'
              236  CALL_METHOD_3         3  ''
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  JUMP_FORWARD       1182  'to 1182'
            244_0  COME_FROM           218  '218'

 L. 872       244  LOAD_FAST                'value'
              246  LOAD_CONST               4294967296
              248  COMPARE_OP               <
          250_252  POP_JUMP_IF_FALSE   278  'to 278'

 L. 873       254  LOAD_DEREF               'self'
              256  LOAD_ATTR                _fp
              258  LOAD_METHOD              write
              260  LOAD_GLOBAL              struct
              262  LOAD_METHOD              pack
              264  LOAD_STR                 '>BL'
              266  LOAD_CONST               18
              268  LOAD_FAST                'value'
              270  CALL_METHOD_3         3  ''
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_FORWARD       1182  'to 1182'
            278_0  COME_FROM           250  '250'

 L. 874       278  LOAD_FAST                'value'
              280  LOAD_CONST               9223372036854775808
              282  COMPARE_OP               <
          284_286  POP_JUMP_IF_FALSE   312  'to 312'

 L. 875       288  LOAD_DEREF               'self'
              290  LOAD_ATTR                _fp
              292  LOAD_METHOD              write
              294  LOAD_GLOBAL              struct
              296  LOAD_METHOD              pack
              298  LOAD_STR                 '>BQ'
              300  LOAD_CONST               19
              302  LOAD_FAST                'value'
              304  CALL_METHOD_3         3  ''
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_FORWARD       1182  'to 1182'
            312_0  COME_FROM           284  '284'

 L. 876       312  LOAD_FAST                'value'
              314  LOAD_CONST               18446744073709551616
              316  COMPARE_OP               <
          318_320  POP_JUMP_IF_FALSE   352  'to 352'

 L. 877       322  LOAD_DEREF               'self'
              324  LOAD_ATTR                _fp
              326  LOAD_METHOD              write
              328  LOAD_CONST               b'\x14'
              330  LOAD_FAST                'value'
              332  LOAD_ATTR                to_bytes
              334  LOAD_CONST               16
              336  LOAD_STR                 'big'
              338  LOAD_CONST               True
              340  LOAD_CONST               ('signed',)
              342  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              344  BINARY_ADD       
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
              350  JUMP_FORWARD       1182  'to 1182'
            352_0  COME_FROM           318  '318'

 L. 879       352  LOAD_GLOBAL              OverflowError
              354  LOAD_FAST                'value'
              356  CALL_FUNCTION_1       1  ''
              358  RAISE_VARARGS_1       1  'exception instance'
          360_362  JUMP_FORWARD       1182  'to 1182'
            364_0  COME_FROM           106  '106'

 L. 881       364  LOAD_GLOBAL              isinstance
              366  LOAD_FAST                'value'
              368  LOAD_GLOBAL              float
              370  CALL_FUNCTION_2       2  ''
          372_374  POP_JUMP_IF_FALSE   402  'to 402'

 L. 882       376  LOAD_DEREF               'self'
              378  LOAD_ATTR                _fp
              380  LOAD_METHOD              write
              382  LOAD_GLOBAL              struct
              384  LOAD_METHOD              pack
              386  LOAD_STR                 '>Bd'
              388  LOAD_CONST               35
              390  LOAD_FAST                'value'
              392  CALL_METHOD_3         3  ''
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
          398_400  JUMP_FORWARD       1182  'to 1182'
            402_0  COME_FROM           372  '372'

 L. 884       402  LOAD_GLOBAL              isinstance
              404  LOAD_FAST                'value'
              406  LOAD_GLOBAL              datetime
              408  LOAD_ATTR                datetime
              410  CALL_FUNCTION_2       2  ''
          412_414  POP_JUMP_IF_FALSE   464  'to 464'

 L. 885       416  LOAD_FAST                'value'
              418  LOAD_GLOBAL              datetime
              420  LOAD_METHOD              datetime
              422  LOAD_CONST               2001
              424  LOAD_CONST               1
              426  LOAD_CONST               1
              428  CALL_METHOD_3         3  ''
              430  BINARY_SUBTRACT  
              432  LOAD_METHOD              total_seconds
              434  CALL_METHOD_0         0  ''
              436  STORE_FAST               'f'

 L. 886       438  LOAD_DEREF               'self'
              440  LOAD_ATTR                _fp
              442  LOAD_METHOD              write
              444  LOAD_GLOBAL              struct
              446  LOAD_METHOD              pack
              448  LOAD_STR                 '>Bd'
              450  LOAD_CONST               51
              452  LOAD_FAST                'f'
              454  CALL_METHOD_3         3  ''
              456  CALL_METHOD_1         1  ''
              458  POP_TOP          
          460_462  JUMP_FORWARD       1182  'to 1182'
            464_0  COME_FROM           412  '412'

 L. 888       464  LOAD_GLOBAL              isinstance
              466  LOAD_FAST                'value'
              468  LOAD_GLOBAL              Data
              470  CALL_FUNCTION_2       2  ''
          472_474  POP_JUMP_IF_FALSE   512  'to 512'

 L. 889       476  LOAD_DEREF               'self'
              478  LOAD_METHOD              _write_size
              480  LOAD_CONST               64
              482  LOAD_GLOBAL              len
              484  LOAD_FAST                'value'
              486  LOAD_ATTR                data
              488  CALL_FUNCTION_1       1  ''
              490  CALL_METHOD_2         2  ''
              492  POP_TOP          

 L. 890       494  LOAD_DEREF               'self'
              496  LOAD_ATTR                _fp
              498  LOAD_METHOD              write
              500  LOAD_FAST                'value'
              502  LOAD_ATTR                data
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
          508_510  JUMP_FORWARD       1182  'to 1182'
            512_0  COME_FROM           472  '472'

 L. 892       512  LOAD_GLOBAL              isinstance
              514  LOAD_FAST                'value'
              516  LOAD_GLOBAL              bytes
              518  LOAD_GLOBAL              bytearray
              520  BUILD_TUPLE_2         2 
              522  CALL_FUNCTION_2       2  ''
          524_526  POP_JUMP_IF_FALSE   560  'to 560'

 L. 893       528  LOAD_DEREF               'self'
              530  LOAD_METHOD              _write_size
              532  LOAD_CONST               64
              534  LOAD_GLOBAL              len
              536  LOAD_FAST                'value'
              538  CALL_FUNCTION_1       1  ''
              540  CALL_METHOD_2         2  ''
              542  POP_TOP          

 L. 894       544  LOAD_DEREF               'self'
              546  LOAD_ATTR                _fp
              548  LOAD_METHOD              write
              550  LOAD_FAST                'value'
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          
          556_558  JUMP_FORWARD       1182  'to 1182'
            560_0  COME_FROM           524  '524'

 L. 896       560  LOAD_GLOBAL              isinstance
              562  LOAD_FAST                'value'
              564  LOAD_GLOBAL              str
              566  CALL_FUNCTION_2       2  ''
          568_570  POP_JUMP_IF_FALSE   672  'to 672'

 L. 897       572  SETUP_FINALLY       604  'to 604'

 L. 898       574  LOAD_FAST                'value'
              576  LOAD_METHOD              encode
              578  LOAD_STR                 'ascii'
              580  CALL_METHOD_1         1  ''
              582  STORE_FAST               't'

 L. 899       584  LOAD_DEREF               'self'
              586  LOAD_METHOD              _write_size
              588  LOAD_CONST               80
              590  LOAD_GLOBAL              len
              592  LOAD_FAST                'value'
              594  CALL_FUNCTION_1       1  ''
              596  CALL_METHOD_2         2  ''
              598  POP_TOP          
              600  POP_BLOCK        
              602  JUMP_FORWARD        656  'to 656'
            604_0  COME_FROM_FINALLY   572  '572'

 L. 900       604  DUP_TOP          
              606  LOAD_GLOBAL              UnicodeEncodeError
              608  COMPARE_OP               exception-match
          610_612  POP_JUMP_IF_FALSE   654  'to 654'
              614  POP_TOP          
              616  POP_TOP          
              618  POP_TOP          

 L. 901       620  LOAD_FAST                'value'
              622  LOAD_METHOD              encode
              624  LOAD_STR                 'utf-16be'
              626  CALL_METHOD_1         1  ''
              628  STORE_FAST               't'

 L. 902       630  LOAD_DEREF               'self'
              632  LOAD_METHOD              _write_size
              634  LOAD_CONST               96
              636  LOAD_GLOBAL              len
              638  LOAD_FAST                't'
              640  CALL_FUNCTION_1       1  ''
              642  LOAD_CONST               2
              644  BINARY_FLOOR_DIVIDE
              646  CALL_METHOD_2         2  ''
              648  POP_TOP          
              650  POP_EXCEPT       
              652  JUMP_FORWARD        656  'to 656'
            654_0  COME_FROM           610  '610'
              654  END_FINALLY      
            656_0  COME_FROM           652  '652'
            656_1  COME_FROM           602  '602'

 L. 904       656  LOAD_DEREF               'self'
              658  LOAD_ATTR                _fp
              660  LOAD_METHOD              write
              662  LOAD_FAST                't'
              664  CALL_METHOD_1         1  ''
              666  POP_TOP          
          668_670  JUMP_FORWARD       1182  'to 1182'
            672_0  COME_FROM           568  '568'

 L. 906       672  LOAD_GLOBAL              isinstance
              674  LOAD_FAST                'value'
              676  LOAD_GLOBAL              UID
              678  CALL_FUNCTION_2       2  ''
          680_682  POP_JUMP_IF_FALSE   862  'to 862'

 L. 907       684  LOAD_FAST                'value'
              686  LOAD_ATTR                data
              688  LOAD_CONST               0
              690  COMPARE_OP               <
          692_694  POP_JUMP_IF_FALSE   706  'to 706'

 L. 908       696  LOAD_GLOBAL              ValueError
              698  LOAD_STR                 'UIDs must be positive'
              700  CALL_FUNCTION_1       1  ''
              702  RAISE_VARARGS_1       1  'exception instance'
              704  JUMP_FORWARD       1182  'to 1182'
            706_0  COME_FROM           692  '692'

 L. 909       706  LOAD_FAST                'value'
              708  LOAD_ATTR                data
              710  LOAD_CONST               256
              712  COMPARE_OP               <
          714_716  POP_JUMP_IF_FALSE   742  'to 742'

 L. 910       718  LOAD_DEREF               'self'
              720  LOAD_ATTR                _fp
              722  LOAD_METHOD              write
              724  LOAD_GLOBAL              struct
              726  LOAD_METHOD              pack
              728  LOAD_STR                 '>BB'
              730  LOAD_CONST               128
              732  LOAD_FAST                'value'
              734  CALL_METHOD_3         3  ''
              736  CALL_METHOD_1         1  ''
              738  POP_TOP          
              740  JUMP_FORWARD       1182  'to 1182'
            742_0  COME_FROM           714  '714'

 L. 911       742  LOAD_FAST                'value'
              744  LOAD_ATTR                data
              746  LOAD_CONST               65536
              748  COMPARE_OP               <
          750_752  POP_JUMP_IF_FALSE   778  'to 778'

 L. 912       754  LOAD_DEREF               'self'
              756  LOAD_ATTR                _fp
              758  LOAD_METHOD              write
              760  LOAD_GLOBAL              struct
              762  LOAD_METHOD              pack
              764  LOAD_STR                 '>BH'
              766  LOAD_CONST               129
              768  LOAD_FAST                'value'
              770  CALL_METHOD_3         3  ''
              772  CALL_METHOD_1         1  ''
              774  POP_TOP          
              776  JUMP_FORWARD       1182  'to 1182'
            778_0  COME_FROM           750  '750'

 L. 913       778  LOAD_FAST                'value'
              780  LOAD_ATTR                data
              782  LOAD_CONST               4294967296
              784  COMPARE_OP               <
          786_788  POP_JUMP_IF_FALSE   814  'to 814'

 L. 914       790  LOAD_DEREF               'self'
              792  LOAD_ATTR                _fp
              794  LOAD_METHOD              write
              796  LOAD_GLOBAL              struct
              798  LOAD_METHOD              pack
              800  LOAD_STR                 '>BL'
              802  LOAD_CONST               131
              804  LOAD_FAST                'value'
              806  CALL_METHOD_3         3  ''
              808  CALL_METHOD_1         1  ''
              810  POP_TOP          
              812  JUMP_FORWARD       1182  'to 1182'
            814_0  COME_FROM           786  '786'

 L. 915       814  LOAD_FAST                'value'
              816  LOAD_ATTR                data
              818  LOAD_CONST               18446744073709551616
              820  COMPARE_OP               <
          822_824  POP_JUMP_IF_FALSE   850  'to 850'

 L. 916       826  LOAD_DEREF               'self'
              828  LOAD_ATTR                _fp
              830  LOAD_METHOD              write
              832  LOAD_GLOBAL              struct
              834  LOAD_METHOD              pack
              836  LOAD_STR                 '>BQ'
              838  LOAD_CONST               135
              840  LOAD_FAST                'value'
              842  CALL_METHOD_3         3  ''
              844  CALL_METHOD_1         1  ''
              846  POP_TOP          
              848  JUMP_FORWARD       1182  'to 1182'
            850_0  COME_FROM           822  '822'

 L. 918       850  LOAD_GLOBAL              OverflowError
              852  LOAD_FAST                'value'
              854  CALL_FUNCTION_1       1  ''
              856  RAISE_VARARGS_1       1  'exception instance'
          858_860  JUMP_FORWARD       1182  'to 1182'
            862_0  COME_FROM           680  '680'

 L. 920       862  LOAD_GLOBAL              isinstance
              864  LOAD_FAST                'value'
              866  LOAD_GLOBAL              list
              868  LOAD_GLOBAL              tuple
              870  BUILD_TUPLE_2         2 
              872  CALL_FUNCTION_2       2  ''
          874_876  POP_JUMP_IF_FALSE   952  'to 952'

 L. 921       878  LOAD_CLOSURE             'self'
              880  BUILD_TUPLE_1         1 
              882  LOAD_LISTCOMP            '<code_object <listcomp>>'
              884  LOAD_STR                 '_BinaryPlistWriter._write_object.<locals>.<listcomp>'
              886  MAKE_FUNCTION_8          'closure'
              888  LOAD_FAST                'value'
              890  GET_ITER         
              892  CALL_FUNCTION_1       1  ''
              894  STORE_FAST               'refs'

 L. 922       896  LOAD_GLOBAL              len
              898  LOAD_FAST                'refs'
              900  CALL_FUNCTION_1       1  ''
              902  STORE_FAST               's'

 L. 923       904  LOAD_DEREF               'self'
              906  LOAD_METHOD              _write_size
              908  LOAD_CONST               160
              910  LOAD_FAST                's'
              912  CALL_METHOD_2         2  ''
              914  POP_TOP          

 L. 924       916  LOAD_DEREF               'self'
              918  LOAD_ATTR                _fp
              920  LOAD_METHOD              write
              922  LOAD_GLOBAL              struct
              924  LOAD_ATTR                pack
              926  LOAD_STR                 '>'
              928  LOAD_DEREF               'self'
              930  LOAD_ATTR                _ref_format
              932  LOAD_FAST                's'
              934  BINARY_MULTIPLY  
              936  BINARY_ADD       
              938  BUILD_TUPLE_1         1 
              940  LOAD_FAST                'refs'
              942  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              944  CALL_FUNCTION_EX      0  'positional arguments only'
              946  CALL_METHOD_1         1  ''
              948  POP_TOP          
              950  JUMP_FORWARD       1182  'to 1182'
            952_0  COME_FROM           874  '874'

 L. 926       952  LOAD_GLOBAL              isinstance
              954  LOAD_FAST                'value'
              956  LOAD_GLOBAL              dict
              958  CALL_FUNCTION_2       2  ''
          960_962  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 927       964  BUILD_LIST_0          0 
              966  BUILD_LIST_0          0 
              968  ROT_TWO          
              970  STORE_FAST               'keyRefs'
              972  STORE_FAST               'valRefs'

 L. 929       974  LOAD_DEREF               'self'
              976  LOAD_ATTR                _sort_keys
          978_980  POP_JUMP_IF_FALSE   996  'to 996'

 L. 930       982  LOAD_GLOBAL              sorted
              984  LOAD_FAST                'value'
              986  LOAD_METHOD              items
              988  CALL_METHOD_0         0  ''
              990  CALL_FUNCTION_1       1  ''
              992  STORE_FAST               'rootItems'
              994  JUMP_FORWARD       1004  'to 1004'
            996_0  COME_FROM           978  '978'

 L. 932       996  LOAD_FAST                'value'
            998_0  COME_FROM           178  '178'
              998  LOAD_METHOD              items
             1000  CALL_METHOD_0         0  ''
             1002  STORE_FAST               'rootItems'
           1004_0  COME_FROM           994  '994'

 L. 934      1004  LOAD_FAST                'rootItems'
             1006  GET_ITER         
             1008  FOR_ITER           1084  'to 1084'
             1010  UNPACK_SEQUENCE_2     2 
             1012  STORE_FAST               'k'
             1014  STORE_FAST               'v'

 L. 935      1016  LOAD_GLOBAL              isinstance
             1018  LOAD_FAST                'k'
             1020  LOAD_GLOBAL              str
             1022  CALL_FUNCTION_2       2  ''
         1024_1026  POP_JUMP_IF_TRUE   1048  'to 1048'

 L. 936      1028  LOAD_DEREF               'self'
           1030_0  COME_FROM           210  '210'
             1030  LOAD_ATTR                _skipkeys
         1032_1034  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 937  1036_1038  JUMP_BACK          1008  'to 1008'
           1040_0  COME_FROM          1032  '1032'

 L. 938      1040  LOAD_GLOBAL              TypeError
             1042  LOAD_STR                 'keys must be strings'
             1044  CALL_FUNCTION_1       1  ''
             1046  RAISE_VARARGS_1       1  'exception instance'
           1048_0  COME_FROM          1024  '1024'

 L. 939      1048  LOAD_FAST                'keyRefs'
             1050  LOAD_METHOD              append
             1052  LOAD_DEREF               'self'
             1054  LOAD_METHOD              _getrefnum
             1056  LOAD_FAST                'k'
             1058  CALL_METHOD_1         1  ''
             1060  CALL_METHOD_1         1  ''
           1062_0  COME_FROM           740  '740'
           1062_1  COME_FROM           242  '242'
             1062  POP_TOP          

 L. 940      1064  LOAD_FAST                'valRefs'
             1066  LOAD_METHOD              append
             1068  LOAD_DEREF               'self'
             1070  LOAD_METHOD              _getrefnum
             1072  LOAD_FAST                'v'
             1074  CALL_METHOD_1         1  ''
             1076  CALL_METHOD_1         1  ''
             1078  POP_TOP          
         1080_1082  JUMP_BACK          1008  'to 1008'

 L. 942      1084  LOAD_GLOBAL              len
             1086  LOAD_FAST                'keyRefs'
             1088  CALL_FUNCTION_1       1  ''
             1090  STORE_FAST               's'

 L. 943      1092  LOAD_DEREF               'self'
             1094  LOAD_METHOD              _write_size
           1096_0  COME_FROM           276  '276'
             1096  LOAD_CONST               208
           1098_0  COME_FROM           776  '776'
             1098  LOAD_FAST                's'
             1100  CALL_METHOD_2         2  ''
             1102  POP_TOP          

 L. 944      1104  LOAD_DEREF               'self'
             1106  LOAD_ATTR                _fp
             1108  LOAD_METHOD              write
             1110  LOAD_GLOBAL              struct
             1112  LOAD_ATTR                pack
             1114  LOAD_STR                 '>'
             1116  LOAD_DEREF               'self'
             1118  LOAD_ATTR                _ref_format
             1120  LOAD_FAST                's'
             1122  BINARY_MULTIPLY  
             1124  BINARY_ADD       
             1126  BUILD_TUPLE_1         1 
             1128  LOAD_FAST                'keyRefs'
           1130_0  COME_FROM           310  '310'
             1130  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
             1132  CALL_FUNCTION_EX      0  'positional arguments only'
           1134_0  COME_FROM           812  '812'
             1134  CALL_METHOD_1         1  ''
             1136  POP_TOP          

 L. 945      1138  LOAD_DEREF               'self'
             1140  LOAD_ATTR                _fp
             1142  LOAD_METHOD              write
             1144  LOAD_GLOBAL              struct
             1146  LOAD_ATTR                pack
             1148  LOAD_STR                 '>'
             1150  LOAD_DEREF               'self'
             1152  LOAD_ATTR                _ref_format
             1154  LOAD_FAST                's'
             1156  BINARY_MULTIPLY  
             1158  BINARY_ADD       
             1160  BUILD_TUPLE_1         1 
             1162  LOAD_FAST                'valRefs'
             1164  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
             1166  CALL_FUNCTION_EX      0  'positional arguments only'
             1168  CALL_METHOD_1         1  ''
           1170_0  COME_FROM           848  '848'
           1170_1  COME_FROM           350  '350'
             1170  POP_TOP          
             1172  JUMP_FORWARD       1182  'to 1182'
           1174_0  COME_FROM           960  '960'

 L. 948      1174  LOAD_GLOBAL              TypeError
             1176  LOAD_FAST                'value'
             1178  CALL_FUNCTION_1       1  ''
             1180  RAISE_VARARGS_1       1  'exception instance'
           1182_0  COME_FROM          1172  '1172'
           1182_1  COME_FROM           950  '950'
           1182_2  COME_FROM           858  '858'
           1182_3  COME_FROM           668  '668'
           1182_4  COME_FROM           556  '556'
           1182_5  COME_FROM           508  '508'
           1182_6  COME_FROM           460  '460'
           1182_7  COME_FROM           398  '398'
           1182_8  COME_FROM           360  '360'
           1182_9  COME_FROM            94  '94'
          1182_10  COME_FROM            70  '70'
          1182_11  COME_FROM            46  '46'

Parse error at or near `LOAD_METHOD' instruction at offset 998


def _is_fmt_binary(header):
    return header[:8] == b'bplist00'


_FORMATS = {FMT_XML: dict(detect=_is_fmt_xml,
            parser=_PlistParser,
            writer=_PlistWriter), 
 
 FMT_BINARY: dict(detect=_is_fmt_binary,
               parser=_BinaryPlistParser,
               writer=_BinaryPlistWriter)}

def load(fp, *, fmt=None, use_builtin_types=True, dict_type=dict):
    """Read a .plist file. 'fp' should be a readable and binary file object.
    Return the unpacked root object (which usually is a dictionary).
    """
    if fmt is None:
        header = fp.read(32)
        fp.seek(0)
        for info in _FORMATS.values():
            if info['detect'](header):
                P = info['parser']
                break
        else:
            raise InvalidFileException()

    else:
        P = _FORMATS[fmt]['parser']
    p = P(use_builtin_types=use_builtin_types, dict_type=dict_type)
    return p.parse(fp)


def loads(value, *, fmt=None, use_builtin_types=True, dict_type=dict):
    """Read a .plist file from a bytes object.
    Return the unpacked root object (which usually is a dictionary).
    """
    fp = BytesIO(value)
    return load(fp,
      fmt=fmt, use_builtin_types=use_builtin_types, dict_type=dict_type)


def dump(value, fp, *, fmt=FMT_XML, sort_keys=True, skipkeys=False):
    """Write 'value' to a .plist file. 'fp' should be a writable,
    binary file object.
    """
    if fmt not in _FORMATS:
        raise ValueError('Unsupported format: %r' % (fmt,))
    writer = _FORMATS[fmt]['writer'](fp, sort_keys=sort_keys, skipkeys=skipkeys)
    writer.write(value)


def dumps(value, *, fmt=FMT_XML, skipkeys=False, sort_keys=True):
    """Return a bytes object with the contents for a .plist file.
    """
    fp = BytesIO()
    dump(value, fp, fmt=fmt, skipkeys=skipkeys, sort_keys=sort_keys)
    return fp.getvalue()