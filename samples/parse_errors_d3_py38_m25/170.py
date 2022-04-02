# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xmlrpc\client.py
"""
An XML-RPC client interface for Python.

The marshalling and response parser code can also be used to
implement XML-RPC servers.

Exported exceptions:

  Error          Base class for client errors
  ProtocolError  Indicates an HTTP protocol error
  ResponseError  Indicates a broken response package
  Fault          Indicates an XML-RPC fault package

Exported classes:

  ServerProxy    Represents a logical connection to an XML-RPC server

  MultiCall      Executor of boxcared xmlrpc requests
  DateTime       dateTime wrapper for an ISO 8601 string or time tuple or
                 localtime integer value to generate a "dateTime.iso8601"
                 XML-RPC value
  Binary         binary data wrapper

  Marshaller     Generate an XML-RPC params chunk from a Python data structure
  Unmarshaller   Unmarshal an XML-RPC response from incoming XML event message
  Transport      Handles an HTTP transaction to an XML-RPC server
  SafeTransport  Handles an HTTPS transaction to an XML-RPC server

Exported constants:

  (none)

Exported functions:

  getparser      Create instance of the fastest available parser & attach
                 to an unmarshalling object
  dumps          Convert an argument tuple or a Fault instance to an XML-RPC
                 request (or response, if the methodresponse option is used).
  loads          Convert an XML-RPC packet to unmarshalled data plus a method
                 name (None if not present).
"""
import base64, sys, time
from datetime import datetime
from decimal import Decimal
import http.client, urllib.parse
from xml.parsers import expat
import errno
from io import BytesIO
try:
    import gzip
except ImportError:
    gzip = None
else:

    def escape(s):
        s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        return s.replace('>', '&gt;')


    __version__ = '%d.%d' % sys.version_info[:2]
    MAXINT = 2147483647
    MININT = -2147483648
    PARSE_ERROR = -32700
    SERVER_ERROR = -32600
    APPLICATION_ERROR = -32500
    SYSTEM_ERROR = -32400
    TRANSPORT_ERROR = -32300
    NOT_WELLFORMED_ERROR = -32700
    UNSUPPORTED_ENCODING = -32701
    INVALID_ENCODING_CHAR = -32702
    INVALID_XMLRPC = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_METHOD_PARAMS = -32602
    INTERNAL_ERROR = -32603

    class Error(Exception):
        __doc__ = 'Base class for client errors.'
        __str__ = object.__str__


    class ProtocolError(Error):
        __doc__ = 'Indicates an HTTP protocol error.'

        def __init__(self, url, errcode, errmsg, headers):
            Error.__init__(self)
            self.url = url
            self.errcode = errcode
            self.errmsg = errmsg
            self.headers = headers

        def __repr__(self):
            return '<%s for %s: %s %s>' % (
             self.__class__.__name__, self.url, self.errcode, self.errmsg)


    class ResponseError(Error):
        __doc__ = 'Indicates a broken response package.'


    class Fault(Error):
        __doc__ = 'Indicates an XML-RPC fault package.'

        def __init__(self, faultCode, faultString, **extra):
            Error.__init__(self)
            self.faultCode = faultCode
            self.faultString = faultString

        def __repr__(self):
            return '<%s %s: %r>' % (self.__class__.__name__,
             self.faultCode, self.faultString)


    boolean = Boolean = bool
    _day0 = datetime(1, 1, 1)
    if _day0.strftime('%Y') == '0001':

        def _iso8601_format(value):
            return value.strftime('%Y%m%dT%H:%M:%S')


    elif _day0.strftime('%4Y') == '0001':

        def _iso8601_format(value):
            return value.strftime('%4Y%m%dT%H:%M:%S')


    else:

        def _iso8601_format(value):
            return value.strftime('%Y%m%dT%H:%M:%S').zfill(17)


    del _day0

    def _strftime(value):
        if isinstance(value, datetime):
            return _iso8601_format(value)
        if not isinstance(value, (tuple, time.struct_time)):
            if value == 0:
                value = time.time()
            value = time.localtime(value)
        return '%04d%02d%02dT%02d:%02d:%02d' % value[:6]


    class DateTime:
        __doc__ = "DateTime wrapper for an ISO 8601 string or time tuple or\n    localtime integer value to generate 'dateTime.iso8601' XML-RPC\n    value.\n    "

        def __init__(self, value=0):
            if isinstance(value, str):
                self.value = value
            else:
                self.value = _strftime(value)

        def make_comparable(self, other):
            if isinstance(other, DateTime):
                s = self.value
                o = other.value
            elif isinstance(other, datetime):
                s = self.value
                o = _iso8601_format(other)
            elif isinstance(other, str):
                s = self.value
                o = other
            elif hasattr(other, 'timetuple'):
                s = self.timetuple()
                o = other.timetuple()
            else:
                otype = (hasattr(other, '__class__')) and (other.__class__.__name__) or (type(other))
                raise TypeError("Can't compare %s and %s" % (
                 self.__class__.__name__, otype))
            return (s, o)

        def __lt__(self, other):
            s, o = self.make_comparable(other)
            return s < o

        def __le__(self, other):
            s, o = self.make_comparable(other)
            return s <= o

        def __gt__(self, other):
            s, o = self.make_comparable(other)
            return s > o

        def __ge__(self, other):
            s, o = self.make_comparable(other)
            return s >= o

        def __eq__(self, other):
            s, o = self.make_comparable(other)
            return s == o

        def timetuple(self):
            return time.strptime(self.value, '%Y%m%dT%H:%M:%S')

        def __str__(self):
            return self.value

        def __repr__(self):
            return '<%s %r at %#x>' % (self.__class__.__name__, self.value, id(self))

        def decode(self, data):
            self.value = str(data).strip()

        def encode(self, out):
            out.write('<value><dateTime.iso8601>')
            out.write(self.value)
            out.write('</dateTime.iso8601></value>\n')


    def _datetime(data):
        value = DateTime()
        value.decode(data)
        return value


    def _datetime_type(data):
        return datetime.strptime(data, '%Y%m%dT%H:%M:%S')


    class Binary:
        __doc__ = 'Wrapper for binary data.'

        def __init__(self, data=None):
            if data is None:
                data = b''
            else:
                if not isinstance(data, (bytes, bytearray)):
                    raise TypeError('expected bytes or bytearray, not %s' % data.__class__.__name__)
                data = bytes(data)
            self.data = data

        def __str__(self):
            return str(self.data, 'latin-1')

        def __eq__(self, other):
            if isinstance(other, Binary):
                other = other.data
            return self.data == other

        def decode(self, data):
            self.data = base64.decodebytes(data)

        def encode(self, out):
            out.write('<value><base64>\n')
            encoded = base64.encodebytes(self.data)
            out.write(encoded.decode('ascii'))
            out.write('</base64></value>\n')


    def _binary(data):
        value = Binary()
        value.decode(data)
        return value


    WRAPPERS = (
     DateTime, Binary)

    class ExpatParser:

        def __init__(self, target):
            self._parser = parser = expat.ParserCreate(None, None)
            self._target = target
            parser.StartElementHandler = target.start
            parser.EndElementHandler = target.end
            parser.CharacterDataHandler = target.data
            encoding = None
            target.xml(encoding, None)

        def feed(self, data):
            self._parser.Parse(data, 0)

        def close(self):
            try:
                parser = self._parser
            except AttributeError:
                pass
            else:
                del self._target
                del self._parser
                parser.Parse(b'', True)


    class Marshaller:
        __doc__ = 'Generate an XML-RPC params chunk from a Python data structure.\n\n    Create a Marshaller instance for each set of parameters, and use\n    the "dumps" method to convert your data (represented as a tuple)\n    to an XML-RPC params chunk.  To write a fault response, pass a\n    Fault instance instead.  You may prefer to use the "dumps" module\n    function for this purpose.\n    '

        def __init__(self, encoding=None, allow_none=False):
            self.memo = {}
            self.data = None
            self.encoding = encoding
            self.allow_none = allow_none

        dispatch = {}

        def dumps(self, values):
            out = []
            write = out.append
            dump = self._Marshaller__dump
            if isinstance(values, Fault):
                write('<fault>\n')
                dump({'faultCode':values.faultCode,  'faultString':values.faultString}, write)
                write('</fault>\n')
            else:
                write('<params>\n')
                for v in values:
                    write('<param>\n')
                    dump(v, write)
                    write('</param>\n')
                else:
                    write('</params>\n')

            result = ''.join(out)
            return result

        def __dump(self, value, write):
            try:
                f = self.dispatch[type(value)]
            except KeyError:
                if not hasattr(value, '__dict__'):
                    raise TypeError('cannot marshal %s objects' % type(value))
                else:
                    for type_ in type(value).__mro__:
                        if type_ in self.dispatch.keys():
                            raise TypeError('cannot marshal %s objects' % type(value))
                    else:
                        f = self.dispatch['_arbitrary_instance']

            else:
                f(self, value, write)

        def dump_nil(self, value, write):
            if not self.allow_none:
                raise TypeError('cannot marshal None unless allow_none is enabled')
            write('<value><nil/></value>')

        dispatch[type(None)] = dump_nil

        def dump_bool(self, value, write):
            write('<value><boolean>')
            write(value and '1' or '0')
            write('</boolean></value>\n')

        dispatch[bool] = dump_bool

        def dump_long(self, value, write):
            if value > MAXINT or (value < MININT):
                raise OverflowError('int exceeds XML-RPC limits')
            write('<value><int>')
            write(str(int(value)))
            write('</int></value>\n')

        dispatch[int] = dump_long
        dump_int = dump_long

        def dump_double(self, value, write):
            write('<value><double>')
            write(repr(value))
            write('</double></value>\n')

        dispatch[float] = dump_double

        def dump_unicode(self, value, write, escape=escape):
            write('<value><string>')
            write(escape(value))
            write('</string></value>\n')

        dispatch[str] = dump_unicode

        def dump_bytes(self, value, write):
            write('<value><base64>\n')
            encoded = base64.encodebytes(value)
            write(encoded.decode('ascii'))
            write('</base64></value>\n')

        dispatch[bytes] = dump_bytes
        dispatch[bytearray] = dump_bytes

        def dump_array(self, value, write):
            i = id(value)
            if i in self.memo:
                raise TypeError('cannot marshal recursive sequences')
            self.memo[i] = None
            dump = self._Marshaller__dump
            write('<value><array><data>\n')
            for v in value:
                dump(v, write)
            else:
                write('</data></array></value>\n')
                del self.memo[i]

        dispatch[tuple] = dump_array
        dispatch[list] = dump_array

        def dump_struct(self, value, write, escape=escape):
            i = id(value)
            if i in self.memo:
                raise TypeError('cannot marshal recursive dictionaries')
            self.memo[i] = None
            dump = self._Marshaller__dump
            write('<value><struct>\n')
            for k, v in value.items():
                write('<member>\n')
                if not isinstance(k, str):
                    raise TypeError('dictionary key must be string')
                else:
                    write('<name>%s</name>\n' % escape(k))
                    dump(v, write)
                    write('</member>\n')
            else:
                write('</struct></value>\n')
                del self.memo[i]

        dispatch[dict] = dump_struct

        def dump_datetime(self, value, write):
            write('<value><dateTime.iso8601>')
            write(_strftime(value))
            write('</dateTime.iso8601></value>\n')

        dispatch[datetime] = dump_datetime

        def dump_instance(self, value, write):
            if value.__class__ in WRAPPERS:
                self.write = write
                value.encode(self)
                del self.write
            else:
                self.dump_struct(value.__dict__, write)

        dispatch[DateTime] = dump_instance
        dispatch[Binary] = dump_instance
        dispatch['_arbitrary_instance'] = dump_instance


    class Unmarshaller:
        __doc__ = 'Unmarshal an XML-RPC response, based on incoming XML event\n    messages (start, data, end).  Call close() to get the resulting\n    data structure.\n\n    Note that this reader is fairly tolerant, and gladly accepts bogus\n    XML-RPC data without complaining (but not bogus XML).\n    '

        def __init__(self, use_datetime=False, use_builtin_types=False):
            self._type = None
            self._stack = []
            self._marks = []
            self._data = []
            self._value = False
            self._methodname = None
            self._encoding = 'utf-8'
            self.append = self._stack.append
            self._use_datetime = use_builtin_types or use_datetime
            self._use_bytes = use_builtin_types

        def close(self):
            if self._type is None or (self._marks):
                raise ResponseError()
            if self._type == 'fault':
                raise Fault(**self._stack[0])
            return tuple(self._stack)

        def getmethodname(self):
            return self._methodname

        def xml(self, encoding, standalone):
            self._encoding = encoding

        def start(self, tag, attrs):
            if ':' in tag:
                tag = tag.split(':')[(-1)]
            if tag == 'array' or (tag == 'struct'):
                self._marks.append(len(self._stack))
            self._data = []
            if self._value:
                if tag not in self.dispatch:
                    raise ResponseError('unknown tag %r' % tag)
            self._value = tag == 'value'

        def data(self, text):
            self._data.append(text)

        def end--- This code section failed: ---

 L. 684         0  SETUP_FINALLY        16  'to 16'

 L. 685         2  LOAD_FAST                'self'
                4  LOAD_ATTR                dispatch
                6  LOAD_FAST                'tag'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'f'
               12  POP_BLOCK        
               14  JUMP_FORWARD        100  'to 100'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 686        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    98  'to 98'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 687        30  LOAD_STR                 ':'
               32  LOAD_FAST                'tag'
               34  COMPARE_OP               not-in
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 688        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 689        44  SETUP_FINALLY        70  'to 70'

 L. 690        46  LOAD_FAST                'self'
               48  LOAD_ATTR                dispatch
               50  LOAD_FAST                'tag'
               52  LOAD_METHOD              split
               54  LOAD_STR                 ':'
               56  CALL_METHOD_1         1  ''
               58  LOAD_CONST               -1
               60  BINARY_SUBSCR    
               62  BINARY_SUBSCR    
               64  STORE_FAST               'f'
               66  POP_BLOCK        
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM_FINALLY    44  '44'

 L. 691        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    92  'to 92'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 692        84  POP_EXCEPT       
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            76  '76'
               92  END_FINALLY      
             94_0  COME_FROM            68  '68'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            22  '22'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            14  '14'

 L. 693       100  LOAD_FAST                'f'
              102  LOAD_FAST                'self'
              104  LOAD_STR                 ''
              106  LOAD_METHOD              join
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _data
              112  CALL_METHOD_1         1  ''
              114  CALL_FUNCTION_2       2  ''
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 40

        def end_dispatch--- This code section failed: ---

 L. 700         0  SETUP_FINALLY        16  'to 16'

 L. 701         2  LOAD_FAST                'self'
                4  LOAD_ATTR                dispatch
                6  LOAD_FAST                'tag'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'f'
               12  POP_BLOCK        
               14  JUMP_FORWARD        100  'to 100'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 702        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    98  'to 98'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 703        30  LOAD_STR                 ':'
               32  LOAD_FAST                'tag'
               34  COMPARE_OP               not-in
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 704        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 705        44  SETUP_FINALLY        70  'to 70'

 L. 706        46  LOAD_FAST                'self'
               48  LOAD_ATTR                dispatch
               50  LOAD_FAST                'tag'
               52  LOAD_METHOD              split
               54  LOAD_STR                 ':'
               56  CALL_METHOD_1         1  ''
               58  LOAD_CONST               -1
               60  BINARY_SUBSCR    
               62  BINARY_SUBSCR    
               64  STORE_FAST               'f'
               66  POP_BLOCK        
               68  JUMP_FORWARD         94  'to 94'
             70_0  COME_FROM_FINALLY    44  '44'

 L. 707        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    92  'to 92'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 708        84  POP_EXCEPT       
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            76  '76'
               92  END_FINALLY      
             94_0  COME_FROM            68  '68'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            22  '22'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            14  '14'

 L. 709       100  LOAD_FAST                'f'
              102  LOAD_FAST                'self'
              104  LOAD_FAST                'data'
              106  CALL_FUNCTION_2       2  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 40

        dispatch = {}

        def end_nil(self, data):
            self.append(None)
            self._value = 0

        dispatch['nil'] = end_nil

        def end_boolean(self, data):
            if data == '0':
                self.append(False)
            elif data == '1':
                self.append(True)
            else:
                raise TypeError('bad boolean value')
            self._value = 0

        dispatch['boolean'] = end_boolean

        def end_int(self, data):
            self.append(int(data))
            self._value = 0

        dispatch['i1'] = end_int
        dispatch['i2'] = end_int
        dispatch['i4'] = end_int
        dispatch['i8'] = end_int
        dispatch['int'] = end_int
        dispatch['biginteger'] = end_int

        def end_double(self, data):
            self.append(float(data))
            self._value = 0

        dispatch['double'] = end_double
        dispatch['float'] = end_double

        def end_bigdecimal(self, data):
            self.append(Decimal(data))
            self._value = 0

        dispatch['bigdecimal'] = end_bigdecimal

        def end_string(self, data):
            if self._encoding:
                data = data.decode(self._encoding)
            self.append(data)
            self._value = 0

        dispatch['string'] = end_string
        dispatch['name'] = end_string

        def end_array(self, data):
            mark = self._marks.pop()
            self._stack[mark:] = [
             self._stack[mark:]]
            self._value = 0

        dispatch['array'] = end_array

        def end_struct(self, data):
            mark = self._marks.pop()
            dict = {}
            items = self._stack[mark:]
            for i in range(0, len(items), 2):
                dict[items[i]] = items[(i + 1)]
            else:
                self._stack[mark:] = [
                 dict]
                self._value = 0

        dispatch['struct'] = end_struct

        def end_base64(self, data):
            value = Binary()
            value.decode(data.encode('ascii'))
            if self._use_bytes:
                value = value.data
            self.append(value)
            self._value = 0

        dispatch['base64'] = end_base64

        def end_dateTime(self, data):
            value = DateTime()
            value.decode(data)
            if self._use_datetime:
                value = _datetime_type(data)
            self.append(value)

        dispatch['dateTime.iso8601'] = end_dateTime

        def end_value(self, data):
            if self._value:
                self.end_string(data)

        dispatch['value'] = end_value

        def end_params(self, data):
            self._type = 'params'

        dispatch['params'] = end_params

        def end_fault(self, data):
            self._type = 'fault'

        dispatch['fault'] = end_fault

        def end_methodName(self, data):
            if self._encoding:
                data = data.decode(self._encoding)
            self._methodname = data
            self._type = 'methodName'

        dispatch['methodName'] = end_methodName


    class _MultiCallMethod:

        def __init__(self, call_list, name):
            self._MultiCallMethod__call_list = call_list
            self._MultiCallMethod__name = name

        def __getattr__(self, name):
            return _MultiCallMethod(self._MultiCallMethod__call_list, '%s.%s' % (self._MultiCallMethod__name, name))

        def __call__(self, *args):
            self._MultiCallMethod__call_list.append((self._MultiCallMethod__name, args))


    class MultiCallIterator:
        __doc__ = 'Iterates over the results of a multicall. Exceptions are\n    raised in response to xmlrpc faults.'

        def __init__(self, results):
            self.results = results

        def __getitem__(self, i):
            item = self.results[i]
            if type(item) == type({}):
                raise Fault(item['faultCode'], item['faultString'])
            else:
                if type(item) == type([]):
                    return item[0]
                raise ValueError('unexpected type in multicall result')


    class MultiCall:
        __doc__ = 'server -> an object used to boxcar method calls\n\n    server should be a ServerProxy object.\n\n    Methods can be added to the MultiCall using normal\n    method call syntax e.g.:\n\n    multicall = MultiCall(server_proxy)\n    multicall.add(2,3)\n    multicall.get_address("Guido")\n\n    To execute the multicall, call the MultiCall object e.g.:\n\n    add_result, address = multicall()\n    '

        def __init__(self, server):
            self._MultiCall__server = server
            self._MultiCall__call_list = []

        def __repr__(self):
            return '<%s at %#x>' % (self.__class__.__name__, id(self))

        def __getattr__(self, name):
            return _MultiCallMethod(self._MultiCall__call_list, name)

        def __call__(self):
            marshalled_list = []
            for name, args in self._MultiCall__call_list:
                marshalled_list.append({'methodName':name,  'params':args})
            else:
                return MultiCallIterator(self._MultiCall__server.system.multicall(marshalled_list))


    FastMarshaller = FastParser = FastUnmarshaller = None

    def getparser(use_datetime=False, use_builtin_types=False):
        """getparser() -> parser, unmarshaller

    Create an instance of the fastest available parser, and attach it
    to an unmarshalling object.  Return both objects.
    """
        if FastParser and FastUnmarshaller:
            if use_builtin_types:
                mkdatetime = _datetime_type
                mkbytes = base64.decodebytes
            elif use_datetime:
                mkdatetime = _datetime_type
                mkbytes = _binary
            else:
                mkdatetime = _datetime
                mkbytes = _binary
            target = FastUnmarshaller(True, False, mkbytes, mkdatetime, Fault)
            parser = FastParser(target)
        else:
            target = Unmarshaller(use_datetime=use_datetime, use_builtin_types=use_builtin_types)
            if FastParser:
                parser = FastParser(target)
            else:
                parser = ExpatParser(target)
        return (
         parser, target)


    def dumps(params, methodname=None, methodresponse=None, encoding=None, allow_none=False):
        """data [,options] -> marshalled data

    Convert an argument tuple or a Fault instance to an XML-RPC
    request (or response, if the methodresponse option is used).

    In addition to the data object, the following options can be given
    as keyword arguments:

        methodname: the method name for a methodCall packet

        methodresponse: true to create a methodResponse packet.
        If this option is used with a tuple, the tuple must be
        a singleton (i.e. it can contain only one element).

        encoding: the packet encoding (default is UTF-8)

    All byte strings in the data structure are assumed to use the
    packet encoding.  Unicode strings are automatically converted,
    where necessary.
    """
        assert isinstance(params, (tuple, Fault)), 'argument must be tuple or Fault instance'
        if isinstance(params, Fault):
            methodresponse = 1
        else:
            pass
        if not methodresponse or isinstance(params, tuple):
            assert len(params) == 1, 'response tuple must be a singleton'
            if not encoding:
                encoding = 'utf-8'
            if FastMarshaller:
                m = FastMarshaller(encoding)
            else:
                m = Marshaller(encoding, allow_none)
            data = m.dumps(params)
            if encoding != 'utf-8':
                xmlheader = "<?xml version='1.0' encoding='%s'?>\n" % str(encoding)
            else:
                xmlheader = "<?xml version='1.0'?>\n"
            if methodname:
                data = (
                 xmlheader,
                 '<methodCall>\n<methodName>',
                 methodname, '</methodName>\n',
                 data,
                 '</methodCall>\n')
            elif methodresponse:
                data = (
                 xmlheader,
                 '<methodResponse>\n',
                 data,
                 '</methodResponse>\n')
            else:
                return data
            return ''.join(data)


    def loads(data, use_datetime=False, use_builtin_types=False):
        """data -> unmarshalled data, method name

    Convert an XML-RPC packet to unmarshalled data plus a method
    name (None if not present).

    If the XML-RPC packet represents a fault condition, this function
    raises a Fault exception.
    """
        p, u = getparser(use_datetime=use_datetime, use_builtin_types=use_builtin_types)
        p.feed(data)
        p.close()
        return (
         u.close(), u.getmethodname())


    def gzip_encode(data):
        """data -> gzip encoded data

    Encode data using the gzip content encoding as described in RFC 1952
    """
        if not gzip:
            raise NotImplementedError
        f = BytesIO()
        with gzip.GzipFile(mode='wb', fileobj=f, compresslevel=1) as gzf:
            gzf.write(data)
        return f.getvalue()


    def gzip_decode(data, max_decode=20971520):
        """gzip encoded data -> unencoded data

    Decode data using the gzip content encoding as described in RFC 1952
    """
        if not gzip:
            raise NotImplementedError
        with gzip.GzipFile(mode='rb', fileobj=(BytesIO(data))) as gzf:
            try:
                if max_decode < 0:
                    decoded = gzf.read()
                else:
                    decoded = gzf.read(max_decode + 1)
            except OSError:
                raise ValueError('invalid data')

        if max_decode >= 0:
            if len(decoded) > max_decode:
                raise ValueError('max gzipped payload length exceeded')
        return decoded


    class GzipDecodedResponse(gzip.GzipFile if gzip else object):
        __doc__ = 'a file-like object to decode a response encoded with the gzip\n    method, as described in RFC 1952.\n    '

        def __init__(self, response):
            if not gzip:
                raise NotImplementedError
            self.io = BytesIO(response.read())
            gzip.GzipFile.__init__(self, mode='rb', fileobj=(self.io))

        def close(self):
            try:
                gzip.GzipFile.close(self)
            finally:
                self.io.close()


    class _Method:

        def __init__(self, send, name):
            self._Method__send = send
            self._Method__name = name

        def __getattr__(self, name):
            return _Method(self._Method__send, '%s.%s' % (self._Method__name, name))

        def __call__(self, *args):
            return self._Method__send(self._Method__name, args)


    class Transport:
        __doc__ = 'Handles an HTTP transaction to an XML-RPC server.'
        user_agent = 'Python-xmlrpc/%s' % __version__
        accept_gzip_encoding = True
        encode_threshold = None

        def __init__(self, use_datetime=False, use_builtin_types=False, *, headers=()):
            self._use_datetime = use_datetime
            self._use_builtin_types = use_builtin_types
            self._connection = (None, None)
            self._headers = list(headers)
            self._extra_headers = []

        def request--- This code section failed: ---

 L.1151         0  LOAD_CONST               (0, 1)
                2  GET_ITER         
              4_0  COME_FROM           122  '122'
              4_1  COME_FROM           118  '118'
              4_2  COME_FROM            58  '58'
                4  FOR_ITER            124  'to 124'
                6  STORE_FAST               'i'

 L.1152         8  SETUP_FINALLY        32  'to 32'

 L.1153        10  LOAD_FAST                'self'
               12  LOAD_METHOD              single_request
               14  LOAD_FAST                'host'
               16  LOAD_FAST                'handler'
               18  LOAD_FAST                'request_body'
               20  LOAD_FAST                'verbose'
               22  CALL_METHOD_4         4  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     8  '8'

 L.1154        32  DUP_TOP          
               34  LOAD_GLOBAL              http
               36  LOAD_ATTR                client
               38  LOAD_ATTR                RemoteDisconnected
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    60  'to 60'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.1155        50  LOAD_FAST                'i'
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L.1156        54  RAISE_VARARGS_0       0  'reraise'
             56_0  COME_FROM            52  '52'
               56  POP_EXCEPT       
               58  JUMP_BACK             4  'to 4'
             60_0  COME_FROM            42  '42'

 L.1157        60  DUP_TOP          
               62  LOAD_GLOBAL              OSError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   120  'to 120'
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY       108  'to 108'

 L.1158        76  LOAD_FAST                'i'
               78  POP_JUMP_IF_TRUE    102  'to 102'
               80  LOAD_FAST                'e'
               82  LOAD_ATTR                errno
               84  LOAD_GLOBAL              errno
               86  LOAD_ATTR                ECONNRESET
               88  LOAD_GLOBAL              errno
               90  LOAD_ATTR                ECONNABORTED

 L.1159        92  LOAD_GLOBAL              errno
               94  LOAD_ATTR                EPIPE

 L.1158        96  BUILD_TUPLE_3         3 
               98  COMPARE_OP               not-in
              100  POP_JUMP_IF_FALSE   104  'to 104'
            102_0  COME_FROM            78  '78'

 L.1160       102  RAISE_VARARGS_0       0  'reraise'
            104_0  COME_FROM           100  '100'
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_FINALLY    74  '74'
              108  LOAD_CONST               None
              110  STORE_FAST               'e'
              112  DELETE_FAST              'e'
              114  END_FINALLY      
              116  POP_EXCEPT       
              118  JUMP_BACK             4  'to 4'
            120_0  COME_FROM            66  '66'
              120  END_FINALLY      
              122  JUMP_BACK             4  'to 4'
            124_0  COME_FROM             4  '4'

Parse error at or near `POP_TOP' instruction at offset 28

        def single_request(self, host, handler, request_body, verbose=False):
            try:
                http_conn = self.send_requesthosthandlerrequest_bodyverbose
                resp = http_conn.getresponse()
                if resp.status == 200:
                    self.verbose = verbose
                    return self.parse_response(resp)
            except Fault:
                raise
            except Exception:
                self.close()
                raise
            else:
                if resp.getheader('content-length', ''):
                    resp.read()
                raise ProtocolError(host + handler, resp.status, resp.reason, dict(resp.getheaders()))

        def getparser(self):
            return getparser(use_datetime=(self._use_datetime), use_builtin_types=(self._use_builtin_types))

        def get_host_info(self, host):
            x509 = {}
            if isinstance(host, tuple):
                host, x509 = host
            auth, host = urllib.parse._splituser(host)
            if auth:
                auth = urllib.parse.unquote_to_bytes(auth)
                auth = base64.encodebytes(auth).decode('utf-8')
                auth = ''.join(auth.split())
                extra_headers = [
                 (
                  'Authorization', 'Basic ' + auth)]
            else:
                extra_headers = []
            return (host, extra_headers, x509)

        def make_connection(self, host):
            if self._connection:
                if host == self._connection[0]:
                    return self._connection[1]
            chost, self._extra_headers, x509 = self.get_host_info(host)
            self._connection = (host, http.client.HTTPConnection(chost))
            return self._connection[1]

        def close(self):
            host, connection = self._connection
            if connection:
                self._connection = (None, None)
                connection.close()

        def send_request(self, host, handler, request_body, debug):
            connection = self.make_connection(host)
            headers = self._headers + self._extra_headers
            if debug:
                connection.set_debuglevel(1)
            if self.accept_gzip_encoding and gzip:
                connection.putrequest('POST', handler, skip_accept_encoding=True)
                headers.append(('Accept-Encoding', 'gzip'))
            else:
                connection.putrequest('POST', handler)
            headers.append(('Content-Type', 'text/xml'))
            headers.append(('User-Agent', self.user_agent))
            self.send_headers(connection, headers)
            self.send_content(connection, request_body)
            return connection

        def send_headers(self, connection, headers):
            for key, val in headers:
                connection.putheader(key, val)

        def send_content(self, connection, request_body):
            if self.encode_threshold is not None:
                if self.encode_threshold < len(request_body):
                    if gzip:
                        connection.putheader('Content-Encoding', 'gzip')
                        request_body = gzip_encode(request_body)
            connection.putheader('Content-Length', str(len(request_body)))
            connection.endheaders(request_body)

        def parse_response(self, response):
            if hasattr(response, 'getheader'):
                if response.getheader('Content-Encoding', '') == 'gzip':
                    stream = GzipDecodedResponse(response)
                else:
                    stream = response
            else:
                stream = response
            p, u = self.getparser()
            while True:
                data = stream.read(1024)
                if not data:
                    pass
                else:
                    pass
                if self.verbose:
                    print('body:', repr(data))
                else:
                    p.feed(data)

            if stream is not response:
                stream.close()
            p.close()
            return u.close()


    class SafeTransport(Transport):
        __doc__ = 'Handles an HTTPS transaction to an XML-RPC server.'

        def __init__(self, use_datetime=False, use_builtin_types=False, *, headers=(), context=None):
            super().__init__(use_datetime=use_datetime, use_builtin_types=use_builtin_types,
              headers=headers)
            self.context = context

        def make_connection(self, host):
            if self._connection:
                if host == self._connection[0]:
                    return self._connection[1]
            if not hasattr(http.client, 'HTTPSConnection'):
                raise NotImplementedError("your version of http.client doesn't support HTTPS")
            chost, self._extra_headers, x509 = self.get_host_info(host)
            self._connection = (host,
             (http.client.HTTPSConnection)(chost,
 None, context=self.context, **x509 or {}))
            return self._connection[1]


    class ServerProxy:
        __doc__ = 'uri [,options] -> a logical connection to an XML-RPC server\n\n    uri is the connection point on the server, given as\n    scheme://host/target.\n\n    The standard implementation always supports the "http" scheme.  If\n    SSL socket support is available (Python 2.0), it also supports\n    "https".\n\n    If the target part and the slash preceding it are both omitted,\n    "/RPC2" is assumed.\n\n    The following options can be given as keyword arguments:\n\n        transport: a transport factory\n        encoding: the request encoding (default is UTF-8)\n\n    All 8-bit strings passed to the server proxy are assumed to use\n    the given encoding.\n    '

        def __init__(self, uri, transport=None, encoding=None, verbose=False, allow_none=False, use_datetime=False, use_builtin_types=False, *, headers=(), context=None):
            type, uri = urllib.parse._splittype(uri)
            if type not in ('http', 'https'):
                raise OSError('unsupported XML-RPC protocol')
            self._ServerProxy__host, self._ServerProxy__handler = urllib.parse._splithost(uri)
            if not self._ServerProxy__handler:
                self._ServerProxy__handler = '/RPC2'
            if transport is None:
                if type == 'https':
                    handler = SafeTransport
                    extra_kwargs = {'context': context}
                else:
                    handler = Transport
                    extra_kwargs = {}
                transport = handler(use_datetime=use_datetime, use_builtin_types=use_builtin_types, 
                 headers=headers, **extra_kwargs)
            self._ServerProxy__transport = transport
            self._ServerProxy__encoding = encoding or 'utf-8'
            self._ServerProxy__verbose = verbose
            self._ServerProxy__allow_none = allow_none

        def __close(self):
            self._ServerProxy__transport.close()

        def __request(self, methodname, params):
            request = dumps(params, methodname, encoding=(self._ServerProxy__encoding), allow_none=(self._ServerProxy__allow_none)).encode(self._ServerProxy__encoding, 'xmlcharrefreplace')
            response = self._ServerProxy__transport.request((self._ServerProxy__host),
              (self._ServerProxy__handler),
              request,
              verbose=(self._ServerProxy__verbose))
            if len(response) == 1:
                response = response[0]
            return response

        def __repr__(self):
            return '<%s for %s%s>' % (
             self.__class__.__name__, self._ServerProxy__host, self._ServerProxy__handler)

        def __getattr__(self, name):
            return _Method(self._ServerProxy__request, name)

        def __call__(self, attr):
            """A workaround to get special attributes on the ServerProxy
           without interfering with the magic __getattr__
        """
            if attr == 'close':
                return self._ServerProxy__close
            if attr == 'transport':
                return self._ServerProxy__transport
            raise AttributeError('Attribute %r not found' % (attr,))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self._ServerProxy__close()


    Server = ServerProxy
    if __name__ == '__main__':
        server = ServerProxy('http://localhost:8000')
        try:
            print(server.currentTime.getCurrentTime())
        except Error as v:
            try:
                print('ERROR', v)
            finally:
                v = None
                del v

        else:
            multi = MultiCall(server)
            multi.getData()
            multi.pow(2, 9)
            multi.add(1, 2)
        try:
            for response in multi():
                print(response)

        except Error as v:
            try:
                print('ERROR', v)
            finally:
                v = None
                del v