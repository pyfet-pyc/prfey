# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bson\__init__.py
"""BSON (Binary JSON) encoding and decoding.

The mapping from Python types to BSON types is as follows:

=======================================  =============  ===================
Python Type                              BSON Type      Supported Direction
=======================================  =============  ===================
None                                     null           both
bool                                     boolean        both
int [#int]_                              int32 / int64  py -> bson
long                                     int64          py -> bson
`bson.int64.Int64`                       int64          both
float                                    number (real)  both
string                                   string         py -> bson
unicode                                  string         both
list                                     array          both
dict / `SON`                             object         both
datetime.datetime [#dt]_ [#dt2]_         date           both
`bson.regex.Regex`                       regex          both
compiled re [#re]_                       regex          py -> bson
`bson.binary.Binary`                     binary         both
`bson.objectid.ObjectId`                 oid            both
`bson.dbref.DBRef`                       dbref          both
None                                     undefined      bson -> py
unicode                                  code           bson -> py
`bson.code.Code`                         code           py -> bson
unicode                                  symbol         bson -> py
bytes (Python 3) [#bytes]_               binary         both
=======================================  =============  ===================

Note that, when using Python 2.x, to save binary data it must be wrapped as
an instance of `bson.binary.Binary`. Otherwise it will be saved as a BSON
string and retrieved as unicode. Users of Python 3.x can use the Python bytes
type.

.. [#int] A Python int will be saved as a BSON int32 or BSON int64 depending
   on its size. A BSON int32 will always decode to a Python int. A BSON
   int64 will always decode to a :class:`~bson.int64.Int64`.
.. [#dt] datetime.datetime instances will be rounded to the nearest
   millisecond when saved
.. [#dt2] all datetime.datetime instances are treated as *naive*. clients
   should always use UTC.
.. [#re] :class:`~bson.regex.Regex` instances and regular expression
   objects from ``re.compile()`` are both saved as BSON regular expressions.
   BSON regular expressions are decoded as :class:`~bson.regex.Regex`
   instances.
.. [#bytes] The bytes type from Python 3.x is encoded as BSON binary with
   subtype 0. In Python 3.x it will be decoded back to bytes. In Python 2.x
   it will be decoded to an instance of :class:`~bson.binary.Binary` with
   subtype 0.
"""
import calendar, datetime, itertools, platform, re, struct, sys, uuid
from codecs import utf_8_decode as _utf_8_decode, utf_8_encode as _utf_8_encode
from bson.binary import Binary, OLD_UUID_SUBTYPE, JAVA_LEGACY, CSHARP_LEGACY, UUIDLegacy
from bson.code import Code
from bson.codec_options import CodecOptions, DEFAULT_CODEC_OPTIONS, _raw_document_class
from bson.dbref import DBRef
from bson.decimal128 import Decimal128
from bson.errors import InvalidBSON, InvalidDocument, InvalidStringData
from bson.int64 import Int64
from bson.max_key import MaxKey
from bson.min_key import MinKey
from bson.objectid import ObjectId
from bson.py3compat import abc, b, PY3, iteritems, text_type, string_type, reraise
from bson.regex import Regex
from bson.son import SON, RE_TYPE
from bson.timestamp import Timestamp
from bson.tz_util import utc
try:
    from bson import _cbson
    _USE_C = True
except ImportError:
    _USE_C = False
else:
    EPOCH_AWARE = datetime.datetime.fromtimestamp(0, utc)
    EPOCH_NAIVE = datetime.datetime.utcfromtimestamp(0)
    BSONNUM = b'\x01'
    BSONSTR = b'\x02'
    BSONOBJ = b'\x03'
    BSONARR = b'\x04'
    BSONBIN = b'\x05'
    BSONUND = b'\x06'
    BSONOID = b'\x07'
    BSONBOO = b'\x08'
    BSONDAT = b'\t'
    BSONNUL = b'\n'
    BSONRGX = b'\x0b'
    BSONREF = b'\x0c'
    BSONCOD = b'\r'
    BSONSYM = b'\x0e'
    BSONCWS = b'\x0f'
    BSONINT = b'\x10'
    BSONTIM = b'\x11'
    BSONLON = b'\x12'
    BSONDEC = b'\x13'
    BSONMIN = b'\xff'
    BSONMAX = b'\x7f'
    _UNPACK_FLOAT_FROM = struct.Struct('<d').unpack_from
    _UNPACK_INT = struct.Struct('<i').unpack
    _UNPACK_INT_FROM = struct.Struct('<i').unpack_from
    _UNPACK_LENGTH_SUBTYPE_FROM = struct.Struct('<iB').unpack_from
    _UNPACK_LONG_FROM = struct.Struct('<q').unpack_from
    _UNPACK_TIMESTAMP_FROM = struct.Struct('<II').unpack_from
    if PY3:
        _OBJEND = 0

        def _maybe_ord(element_type):
            return ord(element_type)


        def _elt_to_hex(element_type):
            return chr(element_type).encode()


        _supported_buffer_types = (bytes, bytearray)
    else:
        _OBJEND = b'\x00'

        def _maybe_ord(element_type):
            return element_type


        def _elt_to_hex(element_type):
            return element_type


        _supported_buffer_types = (bytes,)
    if platform.python_implementation() == 'Jython':

        def get_data_and_view(data):
            if isinstance(data, _supported_buffer_types):
                return (
                 data, data)
            data = memoryview(data).tobytes()
            return (data, data)


    else:

        def get_data_and_view(data):
            if isinstance(data, _supported_buffer_types):
                return (
                 data, memoryview(data))
            view = memoryview(data)
            return (view.tobytes(), view)


    def _raise_unknown_type(element_type, element_name):
        """Unknown type helper."""
        raise InvalidBSON("Detected unknown BSON type %r for fieldname '%s'. Are you using the latest driver version?" % (
         _elt_to_hex(element_type), element_name))


    def _get_int(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON int32 to python int."""
        return (
         _UNPACK_INT_FROM(data, position)[0], position + 4)


    def _get_c_string(data, view, position, opts):
        """Decode a BSON 'C' string to python unicode string."""
        end = data.index(b'\x00', position)
        return (
         _utf_8_decode(view[position:end], opts.unicode_decode_error_handler, True)[0], end + 1)


    def _get_float(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON double to python float."""
        return (
         _UNPACK_FLOAT_FROM(data, position)[0], position + 8)


    def _get_string(data, view, position, obj_end, opts, dummy):
        """Decode a BSON string to python unicode string."""
        length = _UNPACK_INT_FROM(data, position)[0]
        position += 4
        if length < 1 or obj_end - position < length:
            raise InvalidBSON('invalid string length')
        end = position + length - 1
        if data[end] != _OBJEND:
            raise InvalidBSON('invalid end of string')
        return (_utf_8_decode(view[position:end], opts.unicode_decode_error_handler, True)[0], end + 1)


    def _get_object_size(data, position, obj_end):
        """Validate and return a BSON document's size."""
        try:
            obj_size = _UNPACK_INT_FROM(data, position)[0]
        except struct.error as exc:
            try:
                raise InvalidBSON(str(exc))
            finally:
                exc = None
                del exc

        else:
            end = position + obj_size - 1
            if data[end] != _OBJEND:
                raise InvalidBSON('bad eoo')
            if end >= obj_end:
                raise InvalidBSON('invalid object length')
            if position == 0:
                if obj_size != obj_end:
                    raise InvalidBSON('invalid object length')
            return (
             obj_size, end)


    def _get_object(data, view, position, obj_end, opts, dummy):
        """Decode a BSON subdocument to opts.document_class or bson.dbref.DBRef."""
        obj_size, end = _get_object_size(data, position, obj_end)
        if _raw_document_class(opts.document_class):
            return (
             opts.document_class(data[position:end + 1], opts),
             position + obj_size)
        obj = _elements_to_dict(data, view, position + 4, end, opts)
        position += obj_size
        if '$ref' in obj:
            return (DBRef(obj.pop('$ref'), obj.pop('$id', None), obj.pop('$db', None), obj), position)
        return (
         obj, position)


    def _get_array(data, view, position, obj_end, opts, element_name):
        """Decode a BSON array to python list."""
        size = _UNPACK_INT_FROM(data, position)[0]
        end = position + size - 1
        if data[end] != _OBJEND:
            raise InvalidBSON('bad eoo')
        else:
            position += 4
            end -= 1
            result = []
            append = result.append
            index = data.index
            getter = _ELEMENT_GETTER
            decoder_map = opts.type_registry._decoder_map
            while True:
                if position < end:
                    element_type = data[position]
                    position = index(b'\x00', position) + 1
                    try:
                        value, position = getter[element_type](data, view, position, obj_end, opts, element_name)
                    except KeyError:
                        _raise_unknown_type(element_type, element_name)
                    else:
                        if decoder_map:
                            custom_decoder = decoder_map.get(type(value))
                            if custom_decoder is not None:
                                value = custom_decoder(value)
                        append(value)

        if position != end + 1:
            raise InvalidBSON('bad array length')
        return (
         result, position + 1)


    def _get_binary(data, view, position, obj_end, opts, dummy1):
        """Decode a BSON binary to bson.binary.Binary or python UUID."""
        length, subtype = _UNPACK_LENGTH_SUBTYPE_FROM(data, position)
        position += 5
        if subtype == 2:
            length2 = _UNPACK_INT_FROM(data, position)[0]
            position += 4
            if length2 != length - 4:
                raise InvalidBSON("invalid binary (st 2) - lengths don't match!")
            length = length2
        end = position + length
        if length < 0 or end > obj_end:
            raise InvalidBSON('bad binary object length')
        if subtype == 3:
            uuid_representation = opts.uuid_representation
            if uuid_representation == JAVA_LEGACY:
                java = data[position:end]
                value = uuid.UUID(bytes=(java[0:8][::-1] + java[8:16][::-1]))
            else:
                if uuid_representation == CSHARP_LEGACY:
                    value = uuid.UUID(bytes_le=(data[position:end]))
                else:
                    value = uuid.UUID(bytes=(data[position:end]))
            return (
             value, end)
        if subtype == 4:
            return (
             uuid.UUID(bytes=(data[position:end])), end)
        if PY3 and subtype == 0:
            value = data[position:end]
        else:
            value = Binary(data[position:end], subtype)
        return (
         value, end)


    def _get_oid(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON ObjectId to bson.objectid.ObjectId."""
        end = position + 12
        return (ObjectId(data[position:end]), end)


    def _get_boolean(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON true/false to python True/False."""
        end = position + 1
        boolean_byte = data[position:end]
        if boolean_byte == b'\x00':
            return (
             False, end)
        if boolean_byte == b'\x01':
            return (
             True, end)
        raise InvalidBSON('invalid boolean value: %r' % boolean_byte)


    def _get_date(data, view, position, dummy0, opts, dummy1):
        """Decode a BSON datetime to python datetime.datetime."""
        return (
         _millis_to_datetime(_UNPACK_LONG_FROM(data, position)[0], opts), position + 8)


    def _get_code(data, view, position, obj_end, opts, element_name):
        """Decode a BSON code to bson.code.Code."""
        code, position = _get_string(data, view, position, obj_end, opts, element_name)
        return (Code(code), position)


    def _get_code_w_scope(data, view, position, obj_end, opts, element_name):
        """Decode a BSON code_w_scope to bson.code.Code."""
        code_end = position + _UNPACK_INT_FROM(data, position)[0]
        code, position = _get_string(data, view, position + 4, code_end, opts, element_name)
        scope, position = _get_object(data, view, position, code_end, opts, element_name)
        if position != code_end:
            raise InvalidBSON('scope outside of javascript code boundaries')
        return (
         Code(code, scope), position)


    def _get_regex(data, view, position, dummy0, opts, dummy1):
        """Decode a BSON regex to bson.regex.Regex or a python pattern object."""
        pattern, position = _get_c_string(data, view, position, opts)
        bson_flags, position = _get_c_string(data, view, position, opts)
        bson_re = Regex(pattern, bson_flags)
        return (bson_re, position)


    def _get_ref(data, view, position, obj_end, opts, element_name):
        """Decode (deprecated) BSON DBPointer to bson.dbref.DBRef."""
        collection, position = _get_string(data, view, position, obj_end, opts, element_name)
        oid, position = _get_oid(data, view, position, obj_end, opts, element_name)
        return (DBRef(collection, oid), position)


    def _get_timestamp(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON timestamp to bson.timestamp.Timestamp."""
        inc, timestamp = _UNPACK_TIMESTAMP_FROM(data, position)
        return (Timestamp(timestamp, inc), position + 8)


    def _get_int64(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON int64 to bson.int64.Int64."""
        return (
         Int64(_UNPACK_LONG_FROM(data, position)[0]), position + 8)


    def _get_decimal128(data, view, position, dummy0, dummy1, dummy2):
        """Decode a BSON decimal128 to bson.decimal128.Decimal128."""
        end = position + 16
        return (Decimal128.from_bid(data[position:end]), end)


    _ELEMENT_GETTER = {_maybe_ord(BSONNUM): _get_float, 
     _maybe_ord(BSONSTR): _get_string, 
     _maybe_ord(BSONOBJ): _get_object, 
     _maybe_ord(BSONARR): _get_array, 
     _maybe_ord(BSONBIN): _get_binary, 
     _maybe_ord(BSONUND): lambda u, v, w, x, y, z: (None, w), 
     _maybe_ord(BSONOID): _get_oid, 
     _maybe_ord(BSONBOO): _get_boolean, 
     _maybe_ord(BSONDAT): _get_date, 
     _maybe_ord(BSONNUL): lambda u, v, w, x, y, z: (None, w), 
     _maybe_ord(BSONRGX): _get_regex, 
     _maybe_ord(BSONREF): _get_ref, 
     _maybe_ord(BSONCOD): _get_code, 
     _maybe_ord(BSONSYM): _get_string, 
     _maybe_ord(BSONCWS): _get_code_w_scope, 
     _maybe_ord(BSONINT): _get_int, 
     _maybe_ord(BSONTIM): _get_timestamp, 
     _maybe_ord(BSONLON): _get_int64, 
     _maybe_ord(BSONDEC): _get_decimal128, 
     _maybe_ord(BSONMIN): lambda u, v, w, x, y, z: (MinKey(), w), 
     _maybe_ord(BSONMAX): lambda u, v, w, x, y, z: (MaxKey(), w)}
    if _USE_C:

        def _element_to_dict(data, view, position, obj_end, opts):
            return _cbson._element_to_dict(data, position, obj_end, opts)


    else:

        def _element_to_dict(data, view, position, obj_end, opts):
            """Decode a single key, value pair."""
            element_type = data[position]
            position += 1
            element_name, position = _get_c_string(data, view, position, opts)
            try:
                value, position = _ELEMENT_GETTER[element_type](data, view, position, obj_end, opts, element_name)
            except KeyError:
                _raise_unknown_type(element_type, element_name)
            else:
                if opts.type_registry._decoder_map:
                    custom_decoder = opts.type_registry._decoder_map.get(type(value))
                    if custom_decoder is not None:
                        value = custom_decoder(value)
                return (
                 element_name, value, position)


    def _raw_to_dict(data, position, obj_end, opts, result):
        data, view = get_data_and_view(data)
        return _elements_to_dict(data, view, position, obj_end, opts, result)


    def _elements_to_dict(data, view, position, obj_end, opts, result=None):
        """Decode a BSON document into result."""
        if result is None:
            result = opts.document_class()
        else:
            end = obj_end - 1
            while True:
                if position < end:
                    key, value, position = _element_to_dict(data, view, position, obj_end, opts)
                    result[key] = value

        if position != obj_end:
            raise InvalidBSON('bad object or element length')
        return result


    def _bson_to_dict--- This code section failed: ---

 L. 476         0  LOAD_GLOBAL              get_data_and_view
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'data'
               10  STORE_FAST               'view'

 L. 477        12  SETUP_FINALLY        76  'to 76'

 L. 478        14  LOAD_GLOBAL              _raw_document_class
               16  LOAD_FAST                'opts'
               18  LOAD_ATTR                document_class
               20  CALL_FUNCTION_1       1  ''
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L. 479        24  LOAD_FAST                'opts'
               26  LOAD_METHOD              document_class
               28  LOAD_FAST                'data'
               30  LOAD_FAST                'opts'
               32  CALL_METHOD_2         2  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM            22  '22'

 L. 480        38  LOAD_GLOBAL              _get_object_size
               40  LOAD_FAST                'data'
               42  LOAD_CONST               0
               44  LOAD_GLOBAL              len
               46  LOAD_FAST                'data'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_3       3  ''
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               '_'
               56  STORE_FAST               'end'

 L. 481        58  LOAD_GLOBAL              _elements_to_dict
               60  LOAD_FAST                'data'
               62  LOAD_FAST                'view'
               64  LOAD_CONST               4
               66  LOAD_FAST                'end'
               68  LOAD_FAST                'opts'
               70  CALL_FUNCTION_5       5  ''
               72  POP_BLOCK        
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    12  '12'

 L. 482        76  DUP_TOP          
               78  LOAD_GLOBAL              InvalidBSON
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    96  'to 96'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 483        90  RAISE_VARARGS_0       0  'reraise'
               92  POP_EXCEPT       
               94  JUMP_FORWARD        142  'to 142'
             96_0  COME_FROM            82  '82'

 L. 484        96  DUP_TOP          
               98  LOAD_GLOBAL              Exception
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   140  'to 140'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 486       110  LOAD_GLOBAL              sys
              112  LOAD_METHOD              exc_info
              114  CALL_METHOD_0         0  ''
              116  UNPACK_SEQUENCE_3     3 
              118  STORE_FAST               '_'
              120  STORE_FAST               'exc_value'
              122  STORE_FAST               'exc_tb'

 L. 487       124  LOAD_GLOBAL              reraise
              126  LOAD_GLOBAL              InvalidBSON
              128  LOAD_FAST                'exc_value'
              130  LOAD_FAST                'exc_tb'
              132  CALL_FUNCTION_3       3  ''
              134  POP_TOP          
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           102  '102'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM            94  '94'

Parse error at or near `POP_TOP' instruction at offset 86


    if _USE_C:
        _bson_to_dict = _cbson._bson_to_dict
    else:
        _PACK_FLOAT = struct.Struct('<d').pack
        _PACK_INT = struct.Struct('<i').pack
        _PACK_LENGTH_SUBTYPE = struct.Struct('<iB').pack
        _PACK_LONG = struct.Struct('<q').pack
        _PACK_TIMESTAMP = struct.Struct('<II').pack
        _LIST_NAMES = tuple((b(str(i)) + b'\x00' for i in range(1000)))

        def gen_list_name():
            """Generate "keys" for encoded lists in the sequence
    b"0\x00", b"1\x00", b"2\x00", ...

    The first 1000 keys are returned from a pre-built cache. All
    subsequent keys are generated on the fly.
    """
            for name in _LIST_NAMES:
                (yield name)
            else:
                counter = itertools.count(1000)
                while True:
                    (yield b(str(next(counter))) + b'\x00')


        def _make_c_string_check--- This code section failed: ---

 L. 517         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'string'
                4  LOAD_GLOBAL              bytes
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 518        10  LOAD_CONST               b'\x00'
               12  LOAD_FAST                'string'
               14  COMPARE_OP               in
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 519        18  LOAD_GLOBAL              InvalidDocument
               20  LOAD_STR                 'BSON keys / regex patterns must not contain a NUL character'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 521        26  SETUP_FINALLY        50  'to 50'

 L. 522        28  LOAD_GLOBAL              _utf_8_decode
               30  LOAD_FAST                'string'
               32  LOAD_CONST               None
               34  LOAD_CONST               True
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          

 L. 523        40  LOAD_FAST                'string'
               42  LOAD_CONST               b'\x00'
               44  BINARY_ADD       
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    26  '26'

 L. 524        50  DUP_TOP          
               52  LOAD_GLOBAL              UnicodeError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    80  'to 80'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 525        64  LOAD_GLOBAL              InvalidStringData
               66  LOAD_STR                 'strings in documents must be valid UTF-8: %r'

 L. 526        68  LOAD_FAST                'string'

 L. 525        70  BINARY_MODULO    
               72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_EXCEPT       
               78  JUMP_ABSOLUTE       116  'to 116'
             80_0  COME_FROM            56  '56'
               80  END_FINALLY      
               82  JUMP_FORWARD        116  'to 116'
             84_0  COME_FROM             8  '8'

 L. 528        84  LOAD_STR                 '\x00'
               86  LOAD_FAST                'string'
               88  COMPARE_OP               in
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 529        92  LOAD_GLOBAL              InvalidDocument
               94  LOAD_STR                 'BSON keys / regex patterns must not contain a NUL character'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'

 L. 531       100  LOAD_GLOBAL              _utf_8_encode
              102  LOAD_FAST                'string'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               0
              108  BINARY_SUBSCR    
              110  LOAD_CONST               b'\x00'
              112  BINARY_ADD       
              114  RETURN_VALUE     
            116_0  COME_FROM            82  '82'

Parse error at or near `POP_TOP' instruction at offset 60


        def _make_c_string--- This code section failed: ---

 L. 536         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'string'
                4  LOAD_GLOBAL              bytes
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    68  'to 68'

 L. 537        10  SETUP_FINALLY        34  'to 34'

 L. 538        12  LOAD_GLOBAL              _utf_8_decode
               14  LOAD_FAST                'string'
               16  LOAD_CONST               None
               18  LOAD_CONST               True
               20  CALL_FUNCTION_3       3  ''
               22  POP_TOP          

 L. 539        24  LOAD_FAST                'string'
               26  LOAD_CONST               b'\x00'
               28  BINARY_ADD       
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    10  '10'

 L. 540        34  DUP_TOP          
               36  LOAD_GLOBAL              UnicodeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    64  'to 64'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 541        48  LOAD_GLOBAL              InvalidStringData
               50  LOAD_STR                 'strings in documents must be valid UTF-8: %r'

 L. 542        52  LOAD_FAST                'string'

 L. 541        54  BINARY_MODULO    
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
               60  POP_EXCEPT       
               62  JUMP_ABSOLUTE        84  'to 84'
             64_0  COME_FROM            40  '40'
               64  END_FINALLY      
               66  JUMP_FORWARD         84  'to 84'
             68_0  COME_FROM             8  '8'

 L. 544        68  LOAD_GLOBAL              _utf_8_encode
               70  LOAD_FAST                'string'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_CONST               b'\x00'
               80  BINARY_ADD       
               82  RETURN_VALUE     
             84_0  COME_FROM            66  '66'

Parse error at or near `POP_TOP' instruction at offset 44


        if PY3:

            def _make_name(string):
                """Make a 'C' string suitable for a BSON key."""
                if '\x00' in string:
                    raise InvalidDocument('BSON keys / regex patterns must not contain a NUL character')
                return _utf_8_encode(string)[0] + b'\x00'


        else:
            _make_name = _make_c_string_check

        def _encode_float(name, value, dummy0, dummy1):
            """Encode a float."""
            return b'\x01' + name + _PACK_FLOAT(value)


        if PY3:

            def _encode_bytes(name, value, dummy0, dummy1):
                """Encode a python bytes."""
                return b'\x05' + name + _PACK_INT(len(value)) + b'\x00' + value


        else:

            def _encode_bytes(name, value, dummy0, dummy1):
                """Encode a python str (python 2.x)."""
                try:
                    _utf_8_decode(value, None, True)
                except UnicodeError:
                    raise InvalidStringData('strings in documents must be valid UTF-8: %r' % (
                     value,))
                else:
                    return b'\x02' + name + _PACK_INT(len(value) + 1) + value + b'\x00'


    def _encode_mapping(name, value, check_keys, opts):
        """Encode a mapping type."""
        if _raw_document_class(value):
            return b'\x03' + name + value.raw
        data = (b'').join([_element_to_bson(key, val, check_keys, opts) for key, val in iteritems(value)])
        return b'\x03' + name + _PACK_INT(len(data) + 5) + data + b'\x00'


    def _encode_dbref(name, value, check_keys, opts):
        """Encode bson.dbref.DBRef."""
        buf = bytearray(b'\x03' + name + b'\x00\x00\x00\x00')
        begin = len(buf) - 4
        buf += _name_value_to_bson(b'$ref\x00', value.collection, check_keys, opts)
        buf += _name_value_to_bson(b'$id\x00', value.id, check_keys, opts)
        if value.database is not None:
            buf += _name_value_to_bson(b'$db\x00', value.database, check_keys, opts)
        for key, val in iteritems(value._DBRef__kwargs):
            buf += _element_to_bson(key, val, check_keys, opts)
        else:
            buf += b'\x00'
            buf[begin:begin + 4] = _PACK_INT(len(buf) - begin)
            return bytes(buf)


    def _encode_list(name, value, check_keys, opts):
        """Encode a list/tuple."""
        lname = gen_list_name()
        data = (b'').join([_name_value_to_bson(next(lname), item, check_keys, opts) for item in value])
        return b'\x04' + name + _PACK_INT(len(data) + 5) + data + b'\x00'


    def _encode_text(name, value, dummy0, dummy1):
        """Encode a python unicode (python 2.x) / str (python 3.x)."""
        value = _utf_8_encode(value)[0]
        return b'\x02' + name + _PACK_INT(len(value) + 1) + value + b'\x00'


    def _encode_binary(name, value, dummy0, dummy1):
        """Encode bson.binary.Binary."""
        subtype = value.subtype
        if subtype == 2:
            value = _PACK_INT(len(value)) + value
        return b'\x05' + name + _PACK_LENGTH_SUBTYPE(len(value), subtype) + value


    def _encode_uuid(name, value, dummy, opts):
        """Encode uuid.UUID."""
        uuid_representation = opts.uuid_representation
        if uuid_representation == OLD_UUID_SUBTYPE:
            return b'\x05' + name + b'\x10\x00\x00\x00\x03' + value.bytes
        if uuid_representation == JAVA_LEGACY:
            from_uuid = value.bytes
            data = from_uuid[0:8][::-1] + from_uuid[8:16][::-1]
            return b'\x05' + name + b'\x10\x00\x00\x00\x03' + data
        if uuid_representation == CSHARP_LEGACY:
            return b'\x05' + name + b'\x10\x00\x00\x00\x03' + value.bytes_le
        return b'\x05' + name + b'\x10\x00\x00\x00\x04' + value.bytes


    def _encode_objectid(name, value, dummy0, dummy1):
        """Encode bson.objectid.ObjectId."""
        return b'\x07' + name + value.binary


    def _encode_bool(name, value, dummy0, dummy1):
        """Encode a python boolean (True/False)."""
        return b'\x08' + name + (value and b'\x01' or b'\x00')


    def _encode_datetime(name, value, dummy0, dummy1):
        """Encode datetime.datetime."""
        millis = _datetime_to_millis(value)
        return b'\t' + name + _PACK_LONG(millis)


    def _encode_none(name, dummy0, dummy1, dummy2):
        """Encode python None."""
        return b'\n' + name


    def _encode_regex(name, value, dummy0, dummy1):
        """Encode a python regex or bson.regex.Regex."""
        flags = value.flags
        if flags == 0:
            return b'\x0b' + name + _make_c_string_check(value.pattern) + b'\x00'
        if flags == re.UNICODE:
            return b'\x0b' + name + _make_c_string_check(value.pattern) + b'u\x00'
        sflags = b''
        if flags & re.IGNORECASE:
            sflags += b'i'
        if flags & re.LOCALE:
            sflags += b'l'
        if flags & re.MULTILINE:
            sflags += b'm'
        if flags & re.DOTALL:
            sflags += b's'
        if flags & re.UNICODE:
            sflags += b'u'
        if flags & re.VERBOSE:
            sflags += b'x'
        sflags += b'\x00'
        return b'\x0b' + name + _make_c_string_check(value.pattern) + sflags


    def _encode_code(name, value, dummy, opts):
        """Encode bson.code.Code."""
        cstring = _make_c_string(value)
        cstrlen = len(cstring)
        if value.scope is None:
            return b'\r' + name + _PACK_INT(cstrlen) + cstring
        scope = _dict_to_bson(value.scope, False, opts, False)
        full_length = _PACK_INT(8 + cstrlen + len(scope))
        return b'\x0f' + name + full_length + _PACK_INT(cstrlen) + cstring + scope


    def _encode_int--- This code section failed: ---

 L. 713         0  LOAD_CONST               -2147483648
                2  LOAD_FAST                'value'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_CONST               2147483647
               14  COMPARE_OP               <=
               16  POP_JUMP_IF_FALSE    40  'to 40'
               18  JUMP_FORWARD         24  'to 24'
             20_0  COME_FROM            10  '10'
               20  POP_TOP          
               22  JUMP_FORWARD         40  'to 40'
             24_0  COME_FROM            18  '18'

 L. 714        24  LOAD_CONST               b'\x10'
               26  LOAD_FAST                'name'
               28  BINARY_ADD       
               30  LOAD_GLOBAL              _PACK_INT
               32  LOAD_FAST                'value'
               34  CALL_FUNCTION_1       1  ''
               36  BINARY_ADD       
               38  RETURN_VALUE     
             40_0  COME_FROM            22  '22'
             40_1  COME_FROM            16  '16'

 L. 716        40  SETUP_FINALLY        60  'to 60'

 L. 717        42  LOAD_CONST               b'\x12'
               44  LOAD_FAST                'name'
               46  BINARY_ADD       
               48  LOAD_GLOBAL              _PACK_LONG
               50  LOAD_FAST                'value'
               52  CALL_FUNCTION_1       1  ''
               54  BINARY_ADD       
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    40  '40'

 L. 718        60  DUP_TOP          
               62  LOAD_GLOBAL              struct
               64  LOAD_ATTR                error
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    88  'to 88'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 719        76  LOAD_GLOBAL              OverflowError
               78  LOAD_STR                 'BSON can only handle up to 8-byte ints'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            68  '68'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'

Parse error at or near `POP_TOP' instruction at offset 72


    def _encode_timestamp(name, value, dummy0, dummy1):
        """Encode bson.timestamp.Timestamp."""
        return b'\x11' + name + _PACK_TIMESTAMP(value.inc, value.time)


    def _encode_long--- This code section failed: ---

 L. 729         0  SETUP_FINALLY        20  'to 20'

 L. 730         2  LOAD_CONST               b'\x12'
                4  LOAD_FAST                'name'
                6  BINARY_ADD       
                8  LOAD_GLOBAL              _PACK_LONG
               10  LOAD_FAST                'value'
               12  CALL_FUNCTION_1       1  ''
               14  BINARY_ADD       
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 731        20  DUP_TOP          
               22  LOAD_GLOBAL              struct
               24  LOAD_ATTR                error
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    48  'to 48'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 732        36  LOAD_GLOBAL              OverflowError
               38  LOAD_STR                 'BSON can only handle up to 8-byte ints'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            28  '28'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 32


    def _encode_decimal128(name, value, dummy0, dummy1):
        """Encode bson.decimal128.Decimal128."""
        return b'\x13' + name + value.bid


    def _encode_minkey(name, dummy0, dummy1, dummy2):
        """Encode bson.min_key.MinKey."""
        return b'\xff' + name


    def _encode_maxkey(name, dummy0, dummy1, dummy2):
        """Encode bson.max_key.MaxKey."""
        return b'\x7f' + name


    _ENCODERS = {bool: _encode_bool, 
     bytes: _encode_bytes, 
     datetime.datetime: _encode_datetime, 
     dict: _encode_mapping, 
     float: _encode_float, 
     int: _encode_int, 
     list: _encode_list, 
     text_type: _encode_text, 
     tuple: _encode_list, 
     type(None): _encode_none, 
     uuid.UUID: _encode_uuid, 
     Binary: _encode_binary, 
     Int64: _encode_long, 
     Code: _encode_code, 
     DBRef: _encode_dbref, 
     MaxKey: _encode_maxkey, 
     MinKey: _encode_minkey, 
     ObjectId: _encode_objectid, 
     Regex: _encode_regex, 
     RE_TYPE: _encode_regex, 
     SON: _encode_mapping, 
     Timestamp: _encode_timestamp, 
     UUIDLegacy: _encode_binary, 
     Decimal128: _encode_decimal128, 
     abc.Mapping: _encode_mapping}
    _MARKERS = {5:_encode_binary, 
     7:_encode_objectid, 
     11:_encode_regex, 
     13:_encode_code, 
     17:_encode_timestamp, 
     18:_encode_long, 
     100:_encode_dbref, 
     127:_encode_maxkey, 
     255:_encode_minkey}
    if not PY3:
        _ENCODERS[long] = _encode_long
    _BUILT_IN_TYPES = tuple((t for t in _ENCODERS))

    def _name_value_to_bson--- This code section failed: ---

 L. 811         0  SETUP_FINALLY        26  'to 26'

 L. 812         2  LOAD_GLOBAL              _ENCODERS
                4  LOAD_GLOBAL              type
                6  LOAD_FAST                'value'
                8  CALL_FUNCTION_1       1  ''
               10  BINARY_SUBSCR    
               12  LOAD_FAST                'name'
               14  LOAD_FAST                'value'
               16  LOAD_FAST                'check_keys'
               18  LOAD_FAST                'opts'
               20  CALL_FUNCTION_4       4  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L. 813        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 814        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            32  '32'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

 L. 819        46  LOAD_GLOBAL              getattr
               48  LOAD_FAST                'value'
               50  LOAD_STR                 '_type_marker'
               52  LOAD_CONST               None
               54  CALL_FUNCTION_3       3  ''
               56  STORE_FAST               'marker'

 L. 820        58  LOAD_GLOBAL              isinstance
               60  LOAD_FAST                'marker'
               62  LOAD_GLOBAL              int
               64  CALL_FUNCTION_2       2  ''
               66  POP_JUMP_IF_FALSE   110  'to 110'
               68  LOAD_FAST                'marker'
               70  LOAD_GLOBAL              _MARKERS
               72  COMPARE_OP               in
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L. 821        76  LOAD_GLOBAL              _MARKERS
               78  LOAD_FAST                'marker'
               80  BINARY_SUBSCR    
               82  STORE_FAST               'func'

 L. 823        84  LOAD_FAST                'func'
               86  LOAD_GLOBAL              _ENCODERS
               88  LOAD_GLOBAL              type
               90  LOAD_FAST                'value'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_SUBSCR     

 L. 824        96  LOAD_FAST                'func'
               98  LOAD_FAST                'name'
              100  LOAD_FAST                'value'
              102  LOAD_FAST                'check_keys'
              104  LOAD_FAST                'opts'
              106  CALL_FUNCTION_4       4  ''
              108  RETURN_VALUE     
            110_0  COME_FROM            74  '74'
            110_1  COME_FROM            66  '66'

 L. 828       110  LOAD_FAST                'in_custom_call'
              112  POP_JUMP_IF_TRUE    170  'to 170'
              114  LOAD_FAST                'opts'
              116  LOAD_ATTR                type_registry
              118  LOAD_ATTR                _encoder_map
              120  POP_JUMP_IF_FALSE   170  'to 170'

 L. 829       122  LOAD_FAST                'opts'
              124  LOAD_ATTR                type_registry
              126  LOAD_ATTR                _encoder_map
              128  LOAD_METHOD              get
              130  LOAD_GLOBAL              type
              132  LOAD_FAST                'value'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'custom_encoder'

 L. 830       140  LOAD_FAST                'custom_encoder'
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not
              146  POP_JUMP_IF_FALSE   170  'to 170'

 L. 831       148  LOAD_GLOBAL              _name_value_to_bson

 L. 832       150  LOAD_FAST                'name'

 L. 832       152  LOAD_FAST                'custom_encoder'
              154  LOAD_FAST                'value'
              156  CALL_FUNCTION_1       1  ''

 L. 832       158  LOAD_FAST                'check_keys'

 L. 832       160  LOAD_FAST                'opts'

 L. 833       162  LOAD_CONST               True

 L. 831       164  LOAD_CONST               ('in_custom_call',)
              166  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              168  RETURN_VALUE     
            170_0  COME_FROM           146  '146'
            170_1  COME_FROM           120  '120'
            170_2  COME_FROM           112  '112'

 L. 839       170  LOAD_GLOBAL              _BUILT_IN_TYPES
              172  GET_ITER         
            174_0  COME_FROM           186  '186'
              174  FOR_ITER            228  'to 228'
              176  STORE_FAST               'base'

 L. 840       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'value'
              182  LOAD_FAST                'base'
              184  CALL_FUNCTION_2       2  ''
              186  POP_JUMP_IF_FALSE   174  'to 174'

 L. 841       188  LOAD_GLOBAL              _ENCODERS
              190  LOAD_FAST                'base'
              192  BINARY_SUBSCR    
              194  STORE_FAST               'func'

 L. 843       196  LOAD_FAST                'func'
              198  LOAD_GLOBAL              _ENCODERS
              200  LOAD_GLOBAL              type
              202  LOAD_FAST                'value'
              204  CALL_FUNCTION_1       1  ''
              206  STORE_SUBSCR     

 L. 844       208  LOAD_FAST                'func'
              210  LOAD_FAST                'name'
              212  LOAD_FAST                'value'
              214  LOAD_FAST                'check_keys'
              216  LOAD_FAST                'opts'
              218  CALL_FUNCTION_4       4  ''
              220  ROT_TWO          
              222  POP_TOP          
              224  RETURN_VALUE     
              226  JUMP_BACK           174  'to 174'

 L. 848       228  LOAD_FAST                'opts'
              230  LOAD_ATTR                type_registry
              232  LOAD_ATTR                _fallback_encoder
              234  STORE_FAST               'fallback_encoder'

 L. 849       236  LOAD_FAST                'in_fallback_call'
          238_240  POP_JUMP_IF_TRUE    274  'to 274'
              242  LOAD_FAST                'fallback_encoder'
              244  LOAD_CONST               None
              246  COMPARE_OP               is-not
          248_250  POP_JUMP_IF_FALSE   274  'to 274'

 L. 850       252  LOAD_GLOBAL              _name_value_to_bson

 L. 851       254  LOAD_FAST                'name'

 L. 851       256  LOAD_FAST                'fallback_encoder'
              258  LOAD_FAST                'value'
              260  CALL_FUNCTION_1       1  ''

 L. 851       262  LOAD_FAST                'check_keys'

 L. 851       264  LOAD_FAST                'opts'

 L. 852       266  LOAD_CONST               True

 L. 850       268  LOAD_CONST               ('in_fallback_call',)
              270  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              272  RETURN_VALUE     
            274_0  COME_FROM           248  '248'
            274_1  COME_FROM           238  '238'

 L. 854       274  LOAD_GLOBAL              InvalidDocument

 L. 855       276  LOAD_STR                 'cannot encode object: %r, of type: %r'
              278  LOAD_FAST                'value'
              280  LOAD_GLOBAL              type
              282  LOAD_FAST                'value'
              284  CALL_FUNCTION_1       1  ''
              286  BUILD_TUPLE_2         2 
              288  BINARY_MODULO    

 L. 854       290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 36


    def _element_to_bson(key, value, check_keys, opts):
        """Encode a single key, value pair."""
        if not isinstance(key, string_type):
            raise InvalidDocument('documents must have only string keys, key was %r' % (
             key,))
        if check_keys:
            if key.startswith('$'):
                raise InvalidDocument("key %r must not start with '$'" % (key,))
            if '.' in key:
                raise InvalidDocument("key %r must not contain '.'" % (key,))
        name = _make_name(key)
        return _name_value_to_bson(name, value, check_keys, opts)


    def _dict_to_bson(doc, check_keys, opts, top_level=True):
        """Encode a document to BSON."""
        if _raw_document_class(doc):
            return doc.raw
        try:
            elements = []
            if top_level:
                if '_id' in doc:
                    elements.append(_name_value_to_bson(b'_id\x00', doc['_id'], check_keys, opts))
            for key, value in iteritems(doc):
                if not top_level or key != '_id':
                    elements.append(_element_to_bson(key, value, check_keys, opts))

        except AttributeError:
            raise TypeError('encoder expected a mapping type but got: %r' % (doc,))
        else:
            encoded = (b'').join(elements)
            return _PACK_INT(len(encoded) + 5) + encoded + b'\x00'


    if _USE_C:
        _dict_to_bson = _cbson._dict_to_bson

    def _millis_to_datetime(millis, opts):
        """Convert milliseconds since epoch UTC to datetime."""
        diff = (millis % 1000 + 1000) % 1000
        seconds = (millis - diff) // 1000
        micros = diff * 1000
        if opts.tz_aware:
            dt = EPOCH_AWARE + datetime.timedelta(seconds=seconds, microseconds=micros)
            if opts.tzinfo:
                dt = dt.astimezone(opts.tzinfo)
            return dt
        return EPOCH_NAIVE + datetime.timedelta(seconds=seconds, microseconds=micros)


    def _datetime_to_millis(dtm):
        """Convert datetime to milliseconds since epoch UTC."""
        if dtm.utcoffset() is not None:
            dtm = dtm - dtm.utcoffset()
        return int(calendar.timegm(dtm.timetuple()) * 1000 + dtm.microsecond // 1000)


    _CODEC_OPTIONS_TYPE_ERROR = TypeError('codec_options must be an instance of CodecOptions')

    def encode(document, check_keys=False, codec_options=DEFAULT_CODEC_OPTIONS):
        """Encode a document to BSON.

    A document can be any mapping type (like :class:`dict`).

    Raises :class:`TypeError` if `document` is not a mapping type,
    or contains keys that are not instances of
    :class:`basestring` (:class:`str` in python 3). Raises
    :class:`~bson.errors.InvalidDocument` if `document` cannot be
    converted to :class:`BSON`.

    :Parameters:
      - `document`: mapping type representing a document
      - `check_keys` (optional): check if keys start with '$' or
        contain '.', raising :class:`~bson.errors.InvalidDocument` in
        either case
      - `codec_options` (optional): An instance of
        :class:`~bson.codec_options.CodecOptions`.

    .. versionadded:: 3.9
    """
        if not isinstance(codec_options, CodecOptions):
            raise _CODEC_OPTIONS_TYPE_ERROR
        return _dict_to_bson(document, check_keys, codec_options)


    def decode(data, codec_options=DEFAULT_CODEC_OPTIONS):
        """Decode BSON to a document.

    By default, returns a BSON document represented as a Python
    :class:`dict`. To use a different :class:`MutableMapping` class,
    configure a :class:`~bson.codec_options.CodecOptions`::

        >>> import collections  # From Python standard library.
        >>> import bson
        >>> from bson.codec_options import CodecOptions
        >>> data = bson.encode({'a': 1})
        >>> decoded_doc = bson.decode(data)
        <type 'dict'>
        >>> options = CodecOptions(document_class=collections.OrderedDict)
        >>> decoded_doc = bson.decode(data, codec_options=options)
        >>> type(decoded_doc)
        <class 'collections.OrderedDict'>

    :Parameters:
      - `data`: the BSON to decode. Any bytes-like object that implements
        the buffer protocol.
      - `codec_options` (optional): An instance of
        :class:`~bson.codec_options.CodecOptions`.

    .. versionadded:: 3.9
    """
        if not isinstance(codec_options, CodecOptions):
            raise _CODEC_OPTIONS_TYPE_ERROR
        return _bson_to_dict(data, codec_options)


    def decode_all--- This code section failed: ---

 L.1014         0  LOAD_GLOBAL              get_data_and_view
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'data'
               10  STORE_FAST               'view'

 L.1015        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'codec_options'
               16  LOAD_GLOBAL              CodecOptions
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L.1016        22  LOAD_GLOBAL              _CODEC_OPTIONS_TYPE_ERROR
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.1018        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'data'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'data_len'

 L.1019        34  BUILD_LIST_0          0 
               36  STORE_FAST               'docs'

 L.1020        38  LOAD_CONST               0
               40  STORE_FAST               'position'

 L.1021        42  LOAD_FAST                'data_len'
               44  LOAD_CONST               1
               46  BINARY_SUBTRACT  
               48  STORE_FAST               'end'

 L.1022        50  LOAD_GLOBAL              _raw_document_class
               52  LOAD_FAST                'codec_options'
               54  LOAD_ATTR                document_class
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'use_raw'

 L.1023        60  SETUP_FINALLY       214  'to 214'

 L.1024        62  LOAD_FAST                'position'
               64  LOAD_FAST                'end'
               66  COMPARE_OP               <
               68  POP_JUMP_IF_FALSE   208  'to 208'

 L.1025        70  LOAD_GLOBAL              _UNPACK_INT_FROM
               72  LOAD_FAST                'data'
               74  LOAD_FAST                'position'
               76  CALL_FUNCTION_2       2  ''
               78  LOAD_CONST               0
               80  BINARY_SUBSCR    
               82  STORE_FAST               'obj_size'

 L.1026        84  LOAD_FAST                'data_len'
               86  LOAD_FAST                'position'
               88  BINARY_SUBTRACT  
               90  LOAD_FAST                'obj_size'
               92  COMPARE_OP               <
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L.1027        96  LOAD_GLOBAL              InvalidBSON
               98  LOAD_STR                 'invalid object size'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'

 L.1028       104  LOAD_FAST                'position'
              106  LOAD_FAST                'obj_size'
              108  BINARY_ADD       
              110  LOAD_CONST               1
              112  BINARY_SUBTRACT  
              114  STORE_FAST               'obj_end'

 L.1029       116  LOAD_FAST                'data'
              118  LOAD_FAST                'obj_end'
              120  BINARY_SUBSCR    
              122  LOAD_GLOBAL              _OBJEND
              124  COMPARE_OP               !=
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L.1030       128  LOAD_GLOBAL              InvalidBSON
              130  LOAD_STR                 'bad eoo'
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           126  '126'

 L.1031       136  LOAD_FAST                'use_raw'
              138  POP_JUMP_IF_FALSE   172  'to 172'

 L.1032       140  LOAD_FAST                'docs'
              142  LOAD_METHOD              append

 L.1033       144  LOAD_FAST                'codec_options'
              146  LOAD_METHOD              document_class

 L.1034       148  LOAD_FAST                'data'
              150  LOAD_FAST                'position'
              152  LOAD_FAST                'obj_end'
              154  LOAD_CONST               1
              156  BINARY_ADD       
              158  BUILD_SLICE_2         2 
              160  BINARY_SUBSCR    

 L.1034       162  LOAD_FAST                'codec_options'

 L.1033       164  CALL_METHOD_2         2  ''

 L.1032       166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  JUMP_FORWARD        198  'to 198'
            172_0  COME_FROM           138  '138'

 L.1036       172  LOAD_FAST                'docs'
              174  LOAD_METHOD              append
              176  LOAD_GLOBAL              _elements_to_dict
              178  LOAD_FAST                'data'

 L.1037       180  LOAD_FAST                'view'

 L.1038       182  LOAD_FAST                'position'
              184  LOAD_CONST               4
              186  BINARY_ADD       

 L.1039       188  LOAD_FAST                'obj_end'

 L.1040       190  LOAD_FAST                'codec_options'

 L.1036       192  CALL_FUNCTION_5       5  ''
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          
            198_0  COME_FROM           170  '170'

 L.1041       198  LOAD_FAST                'position'
              200  LOAD_FAST                'obj_size'
              202  INPLACE_ADD      
              204  STORE_FAST               'position'
              206  JUMP_BACK            62  'to 62'
            208_0  COME_FROM            68  '68'

 L.1042       208  LOAD_FAST                'docs'
              210  POP_BLOCK        
              212  RETURN_VALUE     
            214_0  COME_FROM_FINALLY    60  '60'

 L.1043       214  DUP_TOP          
              216  LOAD_GLOBAL              InvalidBSON
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   234  'to 234'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L.1044       228  RAISE_VARARGS_0       0  'reraise'
              230  POP_EXCEPT       
              232  JUMP_FORWARD        282  'to 282'
            234_0  COME_FROM           220  '220'

 L.1045       234  DUP_TOP          
              236  LOAD_GLOBAL              Exception
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   280  'to 280'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L.1047       250  LOAD_GLOBAL              sys
              252  LOAD_METHOD              exc_info
              254  CALL_METHOD_0         0  ''
              256  UNPACK_SEQUENCE_3     3 
              258  STORE_FAST               '_'
              260  STORE_FAST               'exc_value'
              262  STORE_FAST               'exc_tb'

 L.1048       264  LOAD_GLOBAL              reraise
              266  LOAD_GLOBAL              InvalidBSON
              268  LOAD_FAST                'exc_value'
              270  LOAD_FAST                'exc_tb'
              272  CALL_FUNCTION_3       3  ''
              274  POP_TOP          
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           240  '240'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           232  '232'

Parse error at or near `POP_TOP' instruction at offset 224


    if _USE_C:
        decode_all = _cbson.decode_all

    def _decode_selective(rawdoc, fields, codec_options):
        if _raw_document_class(codec_options.document_class):
            doc = {}
        else:
            doc = codec_options.document_class()
        for key, value in iteritems(rawdoc):
            if key in fields:
                if fields[key] == 1:
                    doc[key] = _bson_to_dict(rawdoc.raw, codec_options)[key]
                else:
                    doc[key] = _decode_selective(value, fields[key], codec_options)
            else:
                doc[key] = value
        else:
            return doc


    def _decode_all_selective(data, codec_options, fields):
        """Decode BSON data to a single document while using user-provided
    custom decoding logic.

    `data` must be a string representing a valid, BSON-encoded document.

    :Parameters:
      - `data`: BSON data
      - `codec_options`: An instance of
        :class:`~bson.codec_options.CodecOptions` with user-specified type
        decoders. If no decoders are found, this method is the same as
        ``decode_all``.
      - `fields`: Map of document namespaces where data that needs
        to be custom decoded lives or None. For example, to custom decode a
        list of objects in 'field1.subfield1', the specified value should be
        ``{'field1': {'subfield1': 1}}``. If ``fields``  is an empty map or
        None, this method is the same as ``decode_all``.

    :Returns:
      - `document_list`: Single-member list containing the decoded document.

    .. versionadded:: 3.8
    """
        if not codec_options.type_registry._decoder_map:
            return decode_all(data, codec_options)
        else:
            return fields or decode_all(data, codec_options.with_options(type_registry=None))
        from bson.raw_bson import RawBSONDocument
        internal_codec_options = codec_options.with_options(document_class=RawBSONDocument,
          type_registry=None)
        _doc = _bson_to_dict(data, internal_codec_options)
        return [_decode_selective(_doc, fields, codec_options)]


    def decode_iter(data, codec_options=DEFAULT_CODEC_OPTIONS):
        """Decode BSON data to multiple documents as a generator.

    Works similarly to the decode_all function, but yields one document at a
    time.

    `data` must be a string of concatenated, valid, BSON-encoded
    documents.

    :Parameters:
      - `data`: BSON data
      - `codec_options` (optional): An instance of
        :class:`~bson.codec_options.CodecOptions`.

    .. versionchanged:: 3.0
       Replaced `as_class`, `tz_aware`, and `uuid_subtype` options with
       `codec_options`.

    .. versionadded:: 2.8
    """
        if not isinstance(codec_options, CodecOptions):
            raise _CODEC_OPTIONS_TYPE_ERROR
        else:
            position = 0
            end = len(data) - 1
            while True:
                if position < end:
                    obj_size = _UNPACK_INT_FROM(data, position)[0]
                    elements = data[position:position + obj_size]
                    position += obj_size
                    (yield _bson_to_dict(elements, codec_options))


    def decode_file_iter(file_obj, codec_options=DEFAULT_CODEC_OPTIONS):
        """Decode bson data from a file to multiple documents as a generator.

    Works similarly to the decode_all function, but reads from the file object
    in chunks and parses bson in chunks, yielding one document at a time.

    :Parameters:
      - `file_obj`: A file object containing BSON data.
      - `codec_options` (optional): An instance of
        :class:`~bson.codec_options.CodecOptions`.

    .. versionchanged:: 3.0
       Replaced `as_class`, `tz_aware`, and `uuid_subtype` options with
       `codec_options`.

    .. versionadded:: 2.8
    """
        while True:
            size_data = file_obj.read(4)
            if not size_data:
                break
            else:
                if len(size_data) != 4:
                    raise InvalidBSON('cut off in middle of objsize')
            obj_size = _UNPACK_INT_FROM(size_data, 0)[0] - 4
            elements = size_data + file_obj.read(max(0, obj_size))
            (yield _bson_to_dict(elements, codec_options))


    def is_valid--- This code section failed: ---

 L.1183         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'bson'
                4  LOAD_GLOBAL              bytes
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.1184        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'BSON data must be an instance of a subclass of bytes'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.1186        18  SETUP_FINALLY        36  'to 36'

 L.1187        20  LOAD_GLOBAL              _bson_to_dict
               22  LOAD_FAST                'bson'
               24  LOAD_GLOBAL              DEFAULT_CODEC_OPTIONS
               26  CALL_FUNCTION_2       2  ''
               28  POP_TOP          

 L.1188        30  POP_BLOCK        
               32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    18  '18'

 L.1189        36  DUP_TOP          
               38  LOAD_GLOBAL              Exception
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.1190        50  POP_EXCEPT       
               52  LOAD_CONST               False
               54  RETURN_VALUE     
             56_0  COME_FROM            42  '42'
               56  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 34


    class BSON(bytes):
        __doc__ = 'BSON (Binary JSON) data.\n\n    .. warning:: Using this class to encode and decode BSON adds a performance\n       cost. For better performance use the module level functions\n       :func:`encode` and :func:`decode` instead.\n    '

        @classmethod
        def encode(cls, document, check_keys=False, codec_options=DEFAULT_CODEC_OPTIONS):
            """Encode a document to a new :class:`BSON` instance.

        A document can be any mapping type (like :class:`dict`).

        Raises :class:`TypeError` if `document` is not a mapping type,
        or contains keys that are not instances of
        :class:`basestring` (:class:`str` in python 3). Raises
        :class:`~bson.errors.InvalidDocument` if `document` cannot be
        converted to :class:`BSON`.

        :Parameters:
          - `document`: mapping type representing a document
          - `check_keys` (optional): check if keys start with '$' or
            contain '.', raising :class:`~bson.errors.InvalidDocument` in
            either case
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`.

        .. versionchanged:: 3.0
           Replaced `uuid_subtype` option with `codec_options`.
        """
            return cls(encode(document, check_keys, codec_options))

        def decode(self, codec_options=DEFAULT_CODEC_OPTIONS):
            """Decode this BSON data.

        By default, returns a BSON document represented as a Python
        :class:`dict`. To use a different :class:`MutableMapping` class,
        configure a :class:`~bson.codec_options.CodecOptions`::

            >>> import collections  # From Python standard library.
            >>> import bson
            >>> from bson.codec_options import CodecOptions
            >>> data = bson.BSON.encode({'a': 1})
            >>> decoded_doc = bson.BSON(data).decode()
            <type 'dict'>
            >>> options = CodecOptions(document_class=collections.OrderedDict)
            >>> decoded_doc = bson.BSON(data).decode(codec_options=options)
            >>> type(decoded_doc)
            <class 'collections.OrderedDict'>

        :Parameters:
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`.

        .. versionchanged:: 3.0
           Removed `compile_re` option: PyMongo now always represents BSON
           regular expressions as :class:`~bson.regex.Regex` objects. Use
           :meth:`~bson.regex.Regex.try_compile` to attempt to convert from a
           BSON regular expression to a Python regular expression object.

           Replaced `as_class`, `tz_aware`, and `uuid_subtype` options with
           `codec_options`.

        .. versionchanged:: 2.7
           Added `compile_re` option. If set to False, PyMongo represented BSON
           regular expressions as :class:`~bson.regex.Regex` objects instead of
           attempting to compile BSON regular expressions as Python native
           regular expressions, thus preventing errors for some incompatible
           patterns, see `PYTHON-500`_.

        .. _PYTHON-500: https://jira.mongodb.org/browse/PYTHON-500
        """
            return decode(self, codec_options)


    def has_c():
        """Is the C extension installed?
    """
        return _USE_C