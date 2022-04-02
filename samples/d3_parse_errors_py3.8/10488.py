# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: json\encoder.py
"""Implementation of JSONEncoder
"""
import re
try:
    from _json import encode_basestring_ascii as c_encode_basestring_ascii
except ImportError:
    c_encode_basestring_ascii = None
else:
    try:
        from _json import encode_basestring as c_encode_basestring
    except ImportError:
        c_encode_basestring = None
    else:
        try:
            from _json import make_encoder as c_make_encoder
        except ImportError:
            c_make_encoder = None
        else:
            ESCAPE = re.compile('[\\x00-\\x1f\\\\"\\b\\f\\n\\r\\t]')
            ESCAPE_ASCII = re.compile('([\\\\"]|[^\\ -~])')
            HAS_UTF8 = re.compile(b'[\x80-\xff]')
            ESCAPE_DCT = {'\\':'\\\\', 
             '"':'\\"', 
             '\x08':'\\b', 
             '\x0c':'\\f', 
             '\n':'\\n', 
             '\r':'\\r', 
             '\t':'\\t'}
for i in range(32):
    ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))
else:
    INFINITY = float('inf')

    def py_encode_basestring(s):
        """Return a JSON representation of a Python string

    """

        def replace(match):
            return ESCAPE_DCT[match.group(0)]

        return '"' + ESCAPE.sub(replace, s) + '"'


    encode_basestring = c_encode_basestring or py_encode_basestring

    def py_encode_basestring_ascii(s):
        """Return an ASCII-only JSON representation of a Python string

    """

        def replace(match):
            s = match.group(0)
            try:
                return ESCAPE_DCT[s]
            except KeyError:
                n = ord(s)
                if n < 65536:
                    return '\\u{0:04x}'.format(n)
                n -= 65536
                s1 = 55296 | n >> 10 & 1023
                s2 = 56320 | n & 1023
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)

        return '"' + ESCAPE_ASCII.sub(replace, s) + '"'


    encode_basestring_ascii = c_encode_basestring_ascii or py_encode_basestring_ascii

    class JSONEncoder(object):
        __doc__ = 'Extensible JSON <http://json.org> encoder for Python data structures.\n\n    Supports the following objects and types by default:\n\n    +-------------------+---------------+\n    | Python            | JSON          |\n    +===================+===============+\n    | dict              | object        |\n    +-------------------+---------------+\n    | list, tuple       | array         |\n    +-------------------+---------------+\n    | str               | string        |\n    +-------------------+---------------+\n    | int, float        | number        |\n    +-------------------+---------------+\n    | True              | true          |\n    +-------------------+---------------+\n    | False             | false         |\n    +-------------------+---------------+\n    | None              | null          |\n    +-------------------+---------------+\n\n    To extend this to recognize other objects, subclass and implement a\n    ``.default()`` method with another method that returns a serializable\n    object for ``o`` if possible, otherwise it should call the superclass\n    implementation (to raise ``TypeError``).\n\n    '
        item_separator = ', '
        key_separator = ': '

        def __init__(self, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None):
            """Constructor for JSONEncoder, with sensible defaults.

        If skipkeys is false, then it is a TypeError to attempt
        encoding of keys that are not str, int, float or None.  If
        skipkeys is True, such items are simply skipped.

        If ensure_ascii is true, the output is guaranteed to be str
        objects with all incoming non-ASCII characters escaped.  If
        ensure_ascii is false, the output can contain non-ASCII characters.

        If check_circular is true, then lists, dicts, and custom encoded
        objects will be checked for circular references during encoding to
        prevent an infinite recursion (which would cause an OverflowError).
        Otherwise, no such check takes place.

        If allow_nan is true, then NaN, Infinity, and -Infinity will be
        encoded as such.  This behavior is not JSON specification compliant,
        but is consistent with most JavaScript based encoders and decoders.
        Otherwise, it will be a ValueError to encode such floats.

        If sort_keys is true, then the output of dictionaries will be
        sorted by key; this is useful for regression tests to ensure
        that JSON serializations can be compared on a day-to-day basis.

        If indent is a non-negative integer, then JSON array
        elements and object members will be pretty-printed with that
        indent level.  An indent level of 0 will only insert newlines.
        None is the most compact representation.

        If specified, separators should be an (item_separator, key_separator)
        tuple.  The default is (', ', ': ') if *indent* is ``None`` and
        (',', ': ') otherwise.  To get the most compact JSON representation,
        you should specify (',', ':') to eliminate whitespace.

        If specified, default is a function that gets called for objects
        that can't otherwise be serialized.  It should return a JSON encodable
        version of the object or raise a ``TypeError``.

        """
            self.skipkeys = skipkeys
            self.ensure_ascii = ensure_ascii
            self.check_circular = check_circular
            self.allow_nan = allow_nan
            self.sort_keys = sort_keys
            self.indent = indent
            if separators is not None:
                self.item_separator, self.key_separator = separators
            elif indent is not None:
                self.item_separator = ','
            if default is not None:
                self.default = default

        def default(self, o):
            """Implement this method in a subclass such that it returns
        a serializable object for ``o``, or calls the base implementation
        (to raise a ``TypeError``).

        For example, to support arbitrary iterators, you could
        implement default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                # Let the base class default method raise the TypeError
                return JSONEncoder.default(self, o)

        """
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

        def encode(self, o):
            """Return a JSON string representation of a Python data structure.

        >>> from json.encoder import JSONEncoder
        >>> JSONEncoder().encode({"foo": ["bar", "baz"]})
        '{"foo": ["bar", "baz"]}'

        """
            if isinstance(o, str):
                if self.ensure_ascii:
                    return encode_basestring_ascii(o)
                return encode_basestring(o)
            chunks = self.iterencode(o, _one_shot=True)
            if not isinstance(chunks, (list, tuple)):
                chunks = list(chunks)
            return ''.join(chunks)

        def iterencode(self, o, _one_shot=False):
            """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
            if self.check_circular:
                markers = {}
            else:
                markers = None
            if self.ensure_ascii:
                _encoder = encode_basestring_ascii
            else:
                _encoder = encode_basestring

            def floatstr(o, allow_nan=self.allow_nan, _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
                if o != o:
                    text = 'NaN'
                elif o == _inf:
                    text = 'Infinity'
                elif o == _neginf:
                    text = '-Infinity'
                else:
                    return _repr(o)
                if not allow_nan:
                    raise ValueError('Out of range float values are not JSON compliant: ' + repr(o))
                return text

            if _one_shot and c_make_encoder is not None and self.indent is None:
                _iterencode = c_make_encoder(markers, self.default, _encoder, self.indent, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, self.allow_nan)
            else:
                _iterencode = _make_iterencode(markers, self.default, _encoder, self.indent, floatstr, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, _one_shot)
            return _iterencode(o, 0)


    def _make_iterencode(markers, _default, _encoder, _indent, _floatstr, _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot, ValueError=ValueError, dict=dict, float=float, id=id, int=int, isinstance=isinstance, list=list, str=str, tuple=tuple, _intstr=int.__repr__):
        if _indent is not None:
            if not isinstance(_indent, str):
                _indent = ' ' * _indent

            def _iterencode_list(lst, _current_indent_level):
                if not lst:
                    yield '[]'
                    return
                if markers is not None:
                    markerid = id(lst)
                    if markerid in markers:
                        raise ValueError('Circular reference detected')
                    markers[markerid] = lst
                buf = '['
                if _indent is not None:
                    _current_indent_level += 1
                    newline_indent = '\n' + _indent * _current_indent_level
                    separator = _item_separator + newline_indent
                    buf += newline_indent
                else:
                    newline_indent = None
                    separator = _item_separator
                first = True
                for value in lst:
                    if first:
                        first = False
                    else:
                        buf = separator
                    if isinstance(value, str):
                        yield buf + _encoder(value)
                    else:
                        if value is None:
                            yield buf + 'null'
                        else:
                            if value is True:
                                yield buf + 'true'
                            else:
                                if value is False:
                                    yield buf + 'false'
                                else:
                                    if isinstance(value, int):
                                        yield buf + _intstr(value)
                                    else:
                                        if isinstance(value, float):
                                            yield buf + _floatstr(value)
                                        else:
                                            yield buf
                                            if isinstance(value, (list, tuple)):
                                                chunks = _iterencode_list(value, _current_indent_level)
                                            elif isinstance(value, dict):
                                                chunks = _iterencode_dict(value, _current_indent_level)
                                            else:
                                                chunks = _iterencode(value, _current_indent_level)
                                            yield from chunks
                else:
                    if newline_indent is not None:
                        _current_indent_level -= 1
                        yield '\n' + _indent * _current_indent_level
                    yield ']'
                    if markers is not None:
                        del markers[markerid]

            def _iterencode_dict--- This code section failed: ---

 L. 334         0  LOAD_FAST                'dct'
                2  POP_JUMP_IF_TRUE     14  'to 14'

 L. 335         4  LOAD_STR                 '{}'
                6  YIELD_VALUE      
                8  POP_TOP          

 L. 336        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             2  '2'

 L. 337        14  LOAD_DEREF               'markers'
               16  LOAD_CONST               None
               18  COMPARE_OP               is-not
               20  POP_JUMP_IF_FALSE    54  'to 54'

 L. 338        22  LOAD_DEREF               'id'
               24  LOAD_FAST                'dct'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'markerid'

 L. 339        30  LOAD_FAST                'markerid'
               32  LOAD_DEREF               'markers'
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 340        38  LOAD_DEREF               'ValueError'
               40  LOAD_STR                 'Circular reference detected'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 341        46  LOAD_FAST                'dct'
               48  LOAD_DEREF               'markers'
               50  LOAD_FAST                'markerid'
               52  STORE_SUBSCR     
             54_0  COME_FROM            20  '20'

 L. 342        54  LOAD_STR                 '{'
               56  YIELD_VALUE      
               58  POP_TOP          

 L. 343        60  LOAD_DEREF               '_indent'
               62  LOAD_CONST               None
               64  COMPARE_OP               is-not
               66  POP_JUMP_IF_FALSE   104  'to 104'

 L. 344        68  LOAD_FAST                '_current_indent_level'
               70  LOAD_CONST               1
               72  INPLACE_ADD      
               74  STORE_FAST               '_current_indent_level'

 L. 345        76  LOAD_STR                 '\n'
               78  LOAD_DEREF               '_indent'
               80  LOAD_FAST                '_current_indent_level'
               82  BINARY_MULTIPLY  
               84  BINARY_ADD       
               86  STORE_FAST               'newline_indent'

 L. 346        88  LOAD_DEREF               '_item_separator'
               90  LOAD_FAST                'newline_indent'
               92  BINARY_ADD       
               94  STORE_FAST               'item_separator'

 L. 347        96  LOAD_FAST                'newline_indent'
               98  YIELD_VALUE      
              100  POP_TOP          
              102  JUMP_FORWARD        112  'to 112'
            104_0  COME_FROM            66  '66'

 L. 349       104  LOAD_CONST               None
              106  STORE_FAST               'newline_indent'

 L. 350       108  LOAD_DEREF               '_item_separator'
              110  STORE_FAST               'item_separator'
            112_0  COME_FROM           102  '102'

 L. 351       112  LOAD_CONST               True
              114  STORE_FAST               'first'

 L. 352       116  LOAD_DEREF               '_sort_keys'
              118  POP_JUMP_IF_FALSE   134  'to 134'

 L. 353       120  LOAD_GLOBAL              sorted
              122  LOAD_FAST                'dct'
              124  LOAD_METHOD              items
              126  CALL_METHOD_0         0  ''
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'items'
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           118  '118'

 L. 355       134  LOAD_FAST                'dct'
              136  LOAD_METHOD              items
              138  CALL_METHOD_0         0  ''
              140  STORE_FAST               'items'
            142_0  COME_FROM           132  '132'

 L. 356       142  LOAD_FAST                'items'
              144  GET_ITER         
            146_0  COME_FROM           510  '510'
            146_1  COME_FROM           436  '436'
            146_2  COME_FROM           412  '412'
            146_3  COME_FROM           388  '388'
            146_4  COME_FROM           370  '370'
            146_5  COME_FROM           352  '352'
            146_6  COME_FROM           334  '334'
            146_7  COME_FROM           256  '256'
          146_148  FOR_ITER            512  'to 512'
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'key'
              154  STORE_FAST               'value'

 L. 357       156  LOAD_DEREF               'isinstance'
              158  LOAD_FAST                'key'
              160  LOAD_DEREF               'str'
              162  CALL_FUNCTION_2       2  ''
              164  POP_JUMP_IF_FALSE   168  'to 168'

 L. 358       166  JUMP_FORWARD        278  'to 278'
            168_0  COME_FROM           164  '164'

 L. 361       168  LOAD_DEREF               'isinstance'
              170  LOAD_FAST                'key'
              172  LOAD_DEREF               'float'
              174  CALL_FUNCTION_2       2  ''
              176  POP_JUMP_IF_FALSE   188  'to 188'

 L. 363       178  LOAD_DEREF               '_floatstr'
              180  LOAD_FAST                'key'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'key'
              186  JUMP_FORWARD        278  'to 278'
            188_0  COME_FROM           176  '176'

 L. 364       188  LOAD_FAST                'key'
              190  LOAD_CONST               True
              192  COMPARE_OP               is
              194  POP_JUMP_IF_FALSE   202  'to 202'

 L. 365       196  LOAD_STR                 'true'
              198  STORE_FAST               'key'
              200  JUMP_FORWARD        278  'to 278'
            202_0  COME_FROM           194  '194'

 L. 366       202  LOAD_FAST                'key'
              204  LOAD_CONST               False
              206  COMPARE_OP               is
              208  POP_JUMP_IF_FALSE   216  'to 216'

 L. 367       210  LOAD_STR                 'false'
              212  STORE_FAST               'key'
              214  JUMP_FORWARD        278  'to 278'
            216_0  COME_FROM           208  '208'

 L. 368       216  LOAD_FAST                'key'
              218  LOAD_CONST               None
              220  COMPARE_OP               is
              222  POP_JUMP_IF_FALSE   230  'to 230'

 L. 369       224  LOAD_STR                 'null'
              226  STORE_FAST               'key'
              228  JUMP_FORWARD        278  'to 278'
            230_0  COME_FROM           222  '222'

 L. 370       230  LOAD_DEREF               'isinstance'
              232  LOAD_FAST                'key'
              234  LOAD_DEREF               'int'
              236  CALL_FUNCTION_2       2  ''
              238  POP_JUMP_IF_FALSE   250  'to 250'

 L. 372       240  LOAD_DEREF               '_intstr'
              242  LOAD_FAST                'key'
              244  CALL_FUNCTION_1       1  ''
              246  STORE_FAST               'key'
              248  JUMP_FORWARD        278  'to 278'
            250_0  COME_FROM           238  '238'

 L. 373       250  LOAD_DEREF               '_skipkeys'
          252_254  POP_JUMP_IF_FALSE   260  'to 260'

 L. 374       256  JUMP_BACK           146  'to 146'
              258  JUMP_FORWARD        278  'to 278'
            260_0  COME_FROM           252  '252'

 L. 376       260  LOAD_GLOBAL              TypeError
              262  LOAD_STR                 'keys must be str, int, float, bool or None, not '
              264  LOAD_FAST                'key'
              266  LOAD_ATTR                __class__
              268  LOAD_ATTR                __name__
              270  FORMAT_VALUE          0  ''
              272  BUILD_STRING_2        2 
              274  CALL_FUNCTION_1       1  ''
              276  RAISE_VARARGS_1       1  'exception instance'
            278_0  COME_FROM           258  '258'
            278_1  COME_FROM           248  '248'
            278_2  COME_FROM           228  '228'
            278_3  COME_FROM           214  '214'
            278_4  COME_FROM           200  '200'
            278_5  COME_FROM           186  '186'
            278_6  COME_FROM           166  '166'

 L. 378       278  LOAD_FAST                'first'
          280_282  POP_JUMP_IF_FALSE   290  'to 290'

 L. 379       284  LOAD_CONST               False
              286  STORE_FAST               'first'
              288  JUMP_FORWARD        296  'to 296'
            290_0  COME_FROM           280  '280'

 L. 381       290  LOAD_FAST                'item_separator'
              292  YIELD_VALUE      
              294  POP_TOP          
            296_0  COME_FROM           288  '288'

 L. 382       296  LOAD_DEREF               '_encoder'
              298  LOAD_FAST                'key'
              300  CALL_FUNCTION_1       1  ''
              302  YIELD_VALUE      
              304  POP_TOP          

 L. 383       306  LOAD_DEREF               '_key_separator'
              308  YIELD_VALUE      
              310  POP_TOP          

 L. 384       312  LOAD_DEREF               'isinstance'
              314  LOAD_FAST                'value'
              316  LOAD_DEREF               'str'
              318  CALL_FUNCTION_2       2  ''
          320_322  POP_JUMP_IF_FALSE   336  'to 336'

 L. 385       324  LOAD_DEREF               '_encoder'
              326  LOAD_FAST                'value'
              328  CALL_FUNCTION_1       1  ''
              330  YIELD_VALUE      
              332  POP_TOP          
              334  JUMP_BACK           146  'to 146'
            336_0  COME_FROM           320  '320'

 L. 386       336  LOAD_FAST                'value'
              338  LOAD_CONST               None
              340  COMPARE_OP               is
          342_344  POP_JUMP_IF_FALSE   354  'to 354'

 L. 387       346  LOAD_STR                 'null'
              348  YIELD_VALUE      
              350  POP_TOP          
              352  JUMP_BACK           146  'to 146'
            354_0  COME_FROM           342  '342'

 L. 388       354  LOAD_FAST                'value'
              356  LOAD_CONST               True
              358  COMPARE_OP               is
          360_362  POP_JUMP_IF_FALSE   372  'to 372'

 L. 389       364  LOAD_STR                 'true'
              366  YIELD_VALUE      
              368  POP_TOP          
              370  JUMP_BACK           146  'to 146'
            372_0  COME_FROM           360  '360'

 L. 390       372  LOAD_FAST                'value'
              374  LOAD_CONST               False
              376  COMPARE_OP               is
          378_380  POP_JUMP_IF_FALSE   390  'to 390'

 L. 391       382  LOAD_STR                 'false'
              384  YIELD_VALUE      
              386  POP_TOP          
              388  JUMP_BACK           146  'to 146'
            390_0  COME_FROM           378  '378'

 L. 392       390  LOAD_DEREF               'isinstance'
              392  LOAD_FAST                'value'
              394  LOAD_DEREF               'int'
              396  CALL_FUNCTION_2       2  ''
          398_400  POP_JUMP_IF_FALSE   414  'to 414'

 L. 394       402  LOAD_DEREF               '_intstr'
              404  LOAD_FAST                'value'
              406  CALL_FUNCTION_1       1  ''
              408  YIELD_VALUE      
              410  POP_TOP          
              412  JUMP_BACK           146  'to 146'
            414_0  COME_FROM           398  '398'

 L. 395       414  LOAD_DEREF               'isinstance'
              416  LOAD_FAST                'value'
              418  LOAD_DEREF               'float'
              420  CALL_FUNCTION_2       2  ''
          422_424  POP_JUMP_IF_FALSE   438  'to 438'

 L. 397       426  LOAD_DEREF               '_floatstr'
              428  LOAD_FAST                'value'
              430  CALL_FUNCTION_1       1  ''
              432  YIELD_VALUE      
              434  POP_TOP          
              436  JUMP_BACK           146  'to 146'
            438_0  COME_FROM           422  '422'

 L. 399       438  LOAD_DEREF               'isinstance'
              440  LOAD_FAST                'value'
              442  LOAD_DEREF               'list'
              444  LOAD_DEREF               'tuple'
              446  BUILD_TUPLE_2         2 
              448  CALL_FUNCTION_2       2  ''
          450_452  POP_JUMP_IF_FALSE   466  'to 466'

 L. 400       454  LOAD_DEREF               '_iterencode_list'
              456  LOAD_FAST                'value'
              458  LOAD_FAST                '_current_indent_level'
              460  CALL_FUNCTION_2       2  ''
              462  STORE_FAST               'chunks'
              464  JUMP_FORWARD        500  'to 500'
            466_0  COME_FROM           450  '450'

 L. 401       466  LOAD_DEREF               'isinstance'
              468  LOAD_FAST                'value'
              470  LOAD_DEREF               'dict'
              472  CALL_FUNCTION_2       2  ''
          474_476  POP_JUMP_IF_FALSE   490  'to 490'

 L. 402       478  LOAD_DEREF               '_iterencode_dict'
              480  LOAD_FAST                'value'
              482  LOAD_FAST                '_current_indent_level'
              484  CALL_FUNCTION_2       2  ''
              486  STORE_FAST               'chunks'
              488  JUMP_FORWARD        500  'to 500'
            490_0  COME_FROM           474  '474'

 L. 404       490  LOAD_DEREF               '_iterencode'
              492  LOAD_FAST                'value'
              494  LOAD_FAST                '_current_indent_level'
              496  CALL_FUNCTION_2       2  ''
              498  STORE_FAST               'chunks'
            500_0  COME_FROM           488  '488'
            500_1  COME_FROM           464  '464'

 L. 405       500  LOAD_FAST                'chunks'
              502  GET_YIELD_FROM_ITER
              504  LOAD_CONST               None
              506  YIELD_FROM       
              508  POP_TOP          
              510  JUMP_BACK           146  'to 146'
            512_0  COME_FROM           146  '146'

 L. 406       512  LOAD_FAST                'newline_indent'
              514  LOAD_CONST               None
              516  COMPARE_OP               is-not
          518_520  POP_JUMP_IF_FALSE   544  'to 544'

 L. 407       522  LOAD_FAST                '_current_indent_level'
              524  LOAD_CONST               1
              526  INPLACE_SUBTRACT 
              528  STORE_FAST               '_current_indent_level'

 L. 408       530  LOAD_STR                 '\n'
              532  LOAD_DEREF               '_indent'
              534  LOAD_FAST                '_current_indent_level'
              536  BINARY_MULTIPLY  
              538  BINARY_ADD       
              540  YIELD_VALUE      
              542  POP_TOP          
            544_0  COME_FROM           518  '518'

 L. 409       544  LOAD_STR                 '}'
              546  YIELD_VALUE      
              548  POP_TOP          

 L. 410       550  LOAD_DEREF               'markers'
              552  LOAD_CONST               None
              554  COMPARE_OP               is-not
          556_558  POP_JUMP_IF_FALSE   566  'to 566'

 L. 411       560  LOAD_DEREF               'markers'
              562  LOAD_FAST                'markerid'
              564  DELETE_SUBSCR    
            566_0  COME_FROM           556  '556'

Parse error at or near `JUMP_FORWARD' instruction at offset 258

            def _iterencode(o, _current_indent_level):
                if isinstance(o, str):
                    yield _encoder(o)
                elif o is None:
                    yield 'null'
                elif o is True:
                    yield 'true'
                elif o is False:
                    yield 'false'
                elif isinstance(o, int):
                    yield _intstr(o)
                elif isinstance(o, float):
                    yield _floatstr(o)
                elif isinstance(o, (list, tuple)):
                    yield from _iterencode_list(o, _current_indent_level)
                elif isinstance(o, dict):
                    yield from _iterencode_dict(o, _current_indent_level)
                else:
                    if markers is not None:
                        markerid = id(o)
                        if markerid in markers:
                            raise ValueError('Circular reference detected')
                        markers[markerid] = o
                    o = _default(o)
                    yield from _iterencode(o, _current_indent_level)
                    if markers is not None:
                        del markers[markerid]

            return _iterencode