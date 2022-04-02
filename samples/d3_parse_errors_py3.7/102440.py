# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: json\__init__.py
r"""JSON (JavaScript Object Notation) <http://json.org> is a subset of
JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data
interchange format.

:mod:`json` exposes an API familiar to users of the standard library
:mod:`marshal` and :mod:`pickle` modules.  It is derived from a
version of the externally maintained simplejson library.

Encoding basic Python object hierarchies::

    >>> import json
    >>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print(json.dumps("\"foo\bar"))
    "\"foo\bar"
    >>> print(json.dumps('\u1234'))
    "\u1234"
    >>> print(json.dumps('\\'))
    "\\"
    >>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
    {"a": 0, "b": 0, "c": 0}
    >>> from io import StringIO
    >>> io = StringIO()
    >>> json.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Compact encoding::

    >>> import json
    >>> mydict = {'4': 5, '6': 7}
    >>> json.dumps([1,2,3,mydict], separators=(',', ':'))
    '[1,2,3,{"4":5,"6":7}]'

Pretty printing::

    >>> import json
    >>> print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
    {
        "4": 5,
        "6": 7
    }

Decoding JSON::

    >>> import json
    >>> obj = ['foo', {'bar': ['baz', None, 1.0, 2]}]
    >>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]') == obj
    True
    >>> json.loads('"\\"foo\\bar"') == '"foo\x08ar'
    True
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)[0] == 'streaming API'
    True

Specializing JSON object decoding::

    >>> import json
    >>> def as_complex(dct):
    ...     if '__complex__' in dct:
    ...         return complex(dct['real'], dct['imag'])
    ...     return dct
    ...
    >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
    ...     object_hook=as_complex)
    (1+2j)
    >>> from decimal import Decimal
    >>> json.loads('1.1', parse_float=Decimal) == Decimal('1.1')
    True

Specializing JSON object encoding::

    >>> import json
    >>> def encode_complex(obj):
    ...     if isinstance(obj, complex):
    ...         return [obj.real, obj.imag]
    ...     raise TypeError(f'Object of type {obj.__class__.__name__} '
    ...                     f'is not JSON serializable')
    ...
    >>> json.dumps(2 + 1j, default=encode_complex)
    '[2.0, 1.0]'
    >>> json.JSONEncoder(default=encode_complex).encode(2 + 1j)
    '[2.0, 1.0]'
    >>> ''.join(json.JSONEncoder(default=encode_complex).iterencode(2 + 1j))
    '[2.0, 1.0]'

Using json.tool from the shell to validate and pretty-print::

    $ echo '{"json":"obj"}' | python -m json.tool
    {
        "json": "obj"
    }
    $ echo '{ 1.2:3.4}' | python -m json.tool
    Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
"""
__version__ = '2.0.9'
__all__ = [
 'dump', 'dumps', 'load', 'loads',
 'JSONDecoder', 'JSONDecodeError', 'JSONEncoder']
__author__ = 'Bob Ippolito <bob@redivi.com>'
from .decoder import JSONDecoder, JSONDecodeError
from .encoder import JSONEncoder
import codecs
_default_encoder = JSONEncoder(skipkeys=False,
  ensure_ascii=True,
  check_circular=True,
  allow_nan=True,
  indent=None,
  separators=None,
  default=None)

def dump--- This code section failed: ---

 L. 165         0  LOAD_FAST                'skipkeys'
                2  POP_JUMP_IF_TRUE     68  'to 68'
                4  LOAD_FAST                'ensure_ascii'
                6  POP_JUMP_IF_FALSE    68  'to 68'

 L. 166         8  LOAD_FAST                'check_circular'
               10  POP_JUMP_IF_FALSE    68  'to 68'
               12  LOAD_FAST                'allow_nan'
               14  POP_JUMP_IF_FALSE    68  'to 68'

 L. 167        16  LOAD_FAST                'cls'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    68  'to 68'
               24  LOAD_FAST                'indent'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    68  'to 68'
               32  LOAD_FAST                'separators'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    68  'to 68'

 L. 168        40  LOAD_FAST                'default'
               42  LOAD_CONST               None
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    68  'to 68'
               48  LOAD_FAST                'sort_keys'
               50  POP_JUMP_IF_TRUE     68  'to 68'
               52  LOAD_FAST                'kw'
               54  POP_JUMP_IF_TRUE     68  'to 68'

 L. 169        56  LOAD_GLOBAL              _default_encoder
               58  LOAD_METHOD              iterencode
               60  LOAD_FAST                'obj'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  STORE_FAST               'iterable'
               66  JUMP_FORWARD        118  'to 118'
             68_0  COME_FROM            54  '54'
             68_1  COME_FROM            50  '50'
             68_2  COME_FROM            46  '46'
             68_3  COME_FROM            38  '38'
             68_4  COME_FROM            30  '30'
             68_5  COME_FROM            22  '22'
             68_6  COME_FROM            14  '14'
             68_7  COME_FROM            10  '10'
             68_8  COME_FROM             6  '6'
             68_9  COME_FROM             2  '2'

 L. 171        68  LOAD_FAST                'cls'
               70  LOAD_CONST               None
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE    80  'to 80'

 L. 172        76  LOAD_GLOBAL              JSONEncoder
               78  STORE_FAST               'cls'
             80_0  COME_FROM            74  '74'

 L. 173        80  LOAD_FAST                'cls'
               82  BUILD_TUPLE_0         0 
               84  LOAD_FAST                'skipkeys'
               86  LOAD_FAST                'ensure_ascii'

 L. 174        88  LOAD_FAST                'check_circular'
               90  LOAD_FAST                'allow_nan'
               92  LOAD_FAST                'indent'

 L. 175        94  LOAD_FAST                'separators'

 L. 176        96  LOAD_FAST                'default'
               98  LOAD_FAST                'sort_keys'
              100  LOAD_CONST               ('skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'indent', 'separators', 'default', 'sort_keys')
              102  BUILD_CONST_KEY_MAP_8     8 
              104  LOAD_FAST                'kw'
              106  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              108  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              110  LOAD_METHOD              iterencode
              112  LOAD_FAST                'obj'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  STORE_FAST               'iterable'
            118_0  COME_FROM            66  '66'

 L. 179       118  SETUP_LOOP          142  'to 142'
              120  LOAD_FAST                'iterable'
              122  GET_ITER         
            124_0  COME_FROM           138  '138'
              124  FOR_ITER            140  'to 140'
              126  STORE_FAST               'chunk'

 L. 180       128  LOAD_FAST                'fp'
              130  LOAD_METHOD              write
              132  LOAD_FAST                'chunk'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          
              138  JUMP_BACK           124  'to 124'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP      118  '118'

Parse error at or near `POP_BLOCK' instruction at offset 140


def dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
    """Serialize ``obj`` to a JSON formatted ``str``.

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the return value can contain non-ASCII
    characters if they appear in strings contained in ``obj``. Otherwise, all
    such characters are escaped in JSON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
    strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If specified, ``separators`` should be an ``(item_separator, key_separator)``
    tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
    ``(',', ': ')`` otherwise.  To get the most compact JSON representation,
    you should specify ``(',', ':')`` to eliminate whitespace.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``JSONEncoder`` is used.

    """
    if not skipkeys:
        if ensure_ascii:
            if check_circular:
                if allow_nan:
                    if cls is None:
                        if indent is None:
                            if not separators is None or default is None:
                                if not sort_keys:
                                    if not kw:
                                        return _default_encoder.encodeobj
                                if cls is None:
                                    cls = JSONEncoder
        return cls(skipkeys=skipkeys, 
         ensure_ascii=ensure_ascii, check_circular=check_circular, 
         allow_nan=allow_nan, indent=indent, separators=separators, 
         default=default, sort_keys=sort_keys, **kw).encodeobj


_default_decoder = JSONDecoder(object_hook=None, object_pairs_hook=None)

def detect_encoding(b):
    bstartswith = b.startswith
    if bstartswith((codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE)):
        return 'utf-32'
    if bstartswith((codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE)):
        return 'utf-16'
    if bstartswith(codecs.BOM_UTF8):
        return 'utf-8-sig'
    if len(b) >= 4:
        if not b[0]:
            if b[1]:
                return 'utf-16-be'
            return 'utf-32-be'
        if not b[1]:
            if b[2] or (b[3]):
                return 'utf-16-le'
            return 'utf-32-le'
    else:
        pass
    if len(b) == 2:
        if not b[0]:
            return 'utf-16-be'
        if not b[1]:
            return 'utf-16-le'
        return 'utf-8'


def load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. JSON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders.  If ``object_hook``
    is also defined, the ``object_pairs_hook`` takes priority.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``JSONDecoder`` is used.
    """
    return loads(fp.read(), cls=cls, 
     object_hook=object_hook, parse_float=parse_float, 
     parse_int=parse_int, parse_constant=parse_constant, 
     object_pairs_hook=object_pairs_hook, **kw)


def loads(s, *, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. JSON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders.  If ``object_hook``
    is also defined, the ``object_pairs_hook`` takes priority.

    ``parse_float``, if specified, will be called with the string
    of every JSON float to be decoded. By default this is equivalent to
    float(num_str). This can be used to use another datatype or parser
    for JSON floats (e.g. decimal.Decimal).

    ``parse_int``, if specified, will be called with the string
    of every JSON int to be decoded. By default this is equivalent to
    int(num_str). This can be used to use another datatype or parser
    for JSON integers (e.g. float).

    ``parse_constant``, if specified, will be called with one of the
    following strings: -Infinity, Infinity, NaN.
    This can be used to raise an exception if invalid JSON numbers
    are encountered.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``JSONDecoder`` is used.

    The ``encoding`` argument is ignored and deprecated.
    """
    if isinstance(s, str):
        if s.startswith'\ufeff':
            raise JSONDecodeError('Unexpected UTF-8 BOM (decode using utf-8-sig)', s, 0)
    else:
        if not isinstance(s, (bytes, bytearray)):
            raise TypeError(f"the JSON object must be str, bytes or bytearray, not {s.__class__.__name__}")
        s = s.decode(detect_encoding(s), 'surrogatepass')
    if cls is None:
        if object_hook is None:
            if parse_int is None:
                if parse_float is None:
                    if parse_constant is None:
                        if object_pairs_hook is None:
                            if not kw:
                                return _default_decoder.decodes
                            if cls is None:
                                cls = JSONDecoder
                            if object_hook is not None:
                                kw['object_hook'] = object_hook
                        if object_pairs_hook is not None:
                            kw['object_pairs_hook'] = object_pairs_hook
                    if parse_float is not None:
                        kw['parse_float'] = parse_float
                if parse_int is not None:
                    kw['parse_int'] = parse_int
            if parse_constant is not None:
                kw['parse_constant'] = parse_constant
        return cls(**kw).decodes