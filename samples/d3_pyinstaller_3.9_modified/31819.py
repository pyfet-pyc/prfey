# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: simplejson\encoder.py
"""Implementation of JSONEncoder
"""
from __future__ import absolute_import
import re
from operator import itemgetter
import decimal
from .compat import unichr, binary_type, text_type, string_types, integer_types, PY3

def _import_speedups--- This code section failed: ---

 L.  10         0  SETUP_FINALLY        28  'to 28'

 L.  11         2  LOAD_CONST               1
                4  LOAD_CONST               ('_speedups',)
                6  IMPORT_NAME              
                8  IMPORT_FROM              _speedups
               10  STORE_FAST               '_speedups'
               12  POP_TOP          

 L.  12        14  LOAD_FAST                '_speedups'
               16  LOAD_ATTR                encode_basestring_ascii
               18  LOAD_FAST                '_speedups'
               20  LOAD_ATTR                make_encoder
               22  BUILD_TUPLE_2         2 
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     0  '0'

 L.  13        28  DUP_TOP          
               30  LOAD_GLOBAL              ImportError
               32  <121>                46  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  14        40  POP_EXCEPT       
               42  LOAD_CONST               (None, None)
               44  RETURN_VALUE     
               46  <48>             

Parse error at or near `<121>' instruction at offset 32


c_encode_basestring_ascii, c_make_encoder = _import_speedups()
from .decoder import PosInf
from .raw_json import RawJSON
ESCAPE = re.compile('[\\x00-\\x1f\\\\"]')
ESCAPE_ASCII = re.compile('([\\\\"]|[^\\ -~])')
HAS_UTF8 = re.compile('[\\x80-\\xff]')
ESCAPE_DCT = {'\\':'\\\\', 
 '"':'\\"', 
 '\x08':'\\b', 
 '\x0c':'\\f', 
 '\n':'\\n', 
 '\r':'\\r', 
 '\t':'\\t'}
for i in range(32):
    ESCAPE_DCT.setdefault(chr(i), '\\u%04x' % (i,))
else:
    FLOAT_REPR = repr

    def encode_basestring--- This code section failed: ---

 L.  42         0  LOAD_FAST                '_PY3'
                2  POP_JUMP_IF_FALSE    50  'to 50'

 L.  43         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                's'
                8  LOAD_GLOBAL              bytes
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.  44        14  LOAD_GLOBAL              str
               16  LOAD_FAST                's'
               18  LOAD_STR                 'utf-8'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               's'
               24  JUMP_FORWARD        138  'to 138'
             26_0  COME_FROM            12  '12'

 L.  45        26  LOAD_GLOBAL              type
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_GLOBAL              str
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   138  'to 138'

 L.  48        38  LOAD_GLOBAL              str
               40  LOAD_METHOD              __str__
               42  LOAD_FAST                's'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               's'
               48  JUMP_FORWARD        138  'to 138'
             50_0  COME_FROM             2  '2'

 L.  50        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                's'
               54  LOAD_GLOBAL              str
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  LOAD_GLOBAL              HAS_UTF8
               62  LOAD_METHOD              search
               64  LOAD_FAST                's'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.  51        74  LOAD_GLOBAL              unicode
               76  LOAD_FAST                's'
               78  LOAD_STR                 'utf-8'
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               's'
               84  JUMP_FORWARD        138  'to 138'
             86_0  COME_FROM            72  '72'
             86_1  COME_FROM            58  '58'

 L.  52        86  LOAD_GLOBAL              type
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_GLOBAL              str
               94  LOAD_GLOBAL              unicode
               96  BUILD_TUPLE_2         2 
               98  <118>                 1  ''
              100  POP_JUMP_IF_FALSE   138  'to 138'

 L.  56       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                's'
              106  LOAD_GLOBAL              str
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L.  57       112  LOAD_GLOBAL              str
              114  LOAD_METHOD              __str__
              116  LOAD_FAST                's'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               's'
              122  JUMP_FORWARD        138  'to 138'
            124_0  COME_FROM           110  '110'

 L.  59       124  LOAD_GLOBAL              unicode
              126  LOAD_METHOD              __getnewargs__
              128  LOAD_FAST                's'
              130  CALL_METHOD_1         1  ''
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  STORE_FAST               's'
            138_0  COME_FROM           122  '122'
            138_1  COME_FROM           100  '100'
            138_2  COME_FROM            84  '84'
            138_3  COME_FROM            48  '48'
            138_4  COME_FROM            36  '36'
            138_5  COME_FROM            24  '24'

 L.  60       138  LOAD_CODE                <code_object replace>
              140  LOAD_STR                 'encode_basestring.<locals>.replace'
              142  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              144  STORE_FAST               'replace'

 L.  62       146  LOAD_FAST                '_q'
              148  LOAD_GLOBAL              ESCAPE
              150  LOAD_METHOD              sub
              152  LOAD_FAST                'replace'
              154  LOAD_FAST                's'
              156  CALL_METHOD_2         2  ''
              158  BINARY_ADD       
              160  LOAD_FAST                '_q'
              162  BINARY_ADD       
              164  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34


    def py_encode_basestring_ascii--- This code section failed: ---

 L.  69         0  LOAD_FAST                '_PY3'
                2  POP_JUMP_IF_FALSE    50  'to 50'

 L.  70         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                's'
                8  LOAD_GLOBAL              bytes
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.  71        14  LOAD_GLOBAL              str
               16  LOAD_FAST                's'
               18  LOAD_STR                 'utf-8'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               's'
               24  JUMP_FORWARD        138  'to 138'
             26_0  COME_FROM            12  '12'

 L.  72        26  LOAD_GLOBAL              type
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_GLOBAL              str
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE   138  'to 138'

 L.  75        38  LOAD_GLOBAL              str
               40  LOAD_METHOD              __str__
               42  LOAD_FAST                's'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               's'
               48  JUMP_FORWARD        138  'to 138'
             50_0  COME_FROM             2  '2'

 L.  77        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                's'
               54  LOAD_GLOBAL              str
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  LOAD_GLOBAL              HAS_UTF8
               62  LOAD_METHOD              search
               64  LOAD_FAST                's'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.  78        74  LOAD_GLOBAL              unicode
               76  LOAD_FAST                's'
               78  LOAD_STR                 'utf-8'
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               's'
               84  JUMP_FORWARD        138  'to 138'
             86_0  COME_FROM            72  '72'
             86_1  COME_FROM            58  '58'

 L.  79        86  LOAD_GLOBAL              type
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_GLOBAL              str
               94  LOAD_GLOBAL              unicode
               96  BUILD_TUPLE_2         2 
               98  <118>                 1  ''
              100  POP_JUMP_IF_FALSE   138  'to 138'

 L.  83       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                's'
              106  LOAD_GLOBAL              str
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L.  84       112  LOAD_GLOBAL              str
              114  LOAD_METHOD              __str__
              116  LOAD_FAST                's'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               's'
              122  JUMP_FORWARD        138  'to 138'
            124_0  COME_FROM           110  '110'

 L.  86       124  LOAD_GLOBAL              unicode
              126  LOAD_METHOD              __getnewargs__
              128  LOAD_FAST                's'
              130  CALL_METHOD_1         1  ''
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  STORE_FAST               's'
            138_0  COME_FROM           122  '122'
            138_1  COME_FROM           100  '100'
            138_2  COME_FROM            84  '84'
            138_3  COME_FROM            48  '48'
            138_4  COME_FROM            36  '36'
            138_5  COME_FROM            24  '24'

 L.  87       138  LOAD_CODE                <code_object replace>
              140  LOAD_STR                 'py_encode_basestring_ascii.<locals>.replace'
              142  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              144  STORE_FAST               'replace'

 L. 103       146  LOAD_STR                 '"'
              148  LOAD_GLOBAL              str
              150  LOAD_GLOBAL              ESCAPE_ASCII
              152  LOAD_METHOD              sub
              154  LOAD_FAST                'replace'
              156  LOAD_FAST                's'
              158  CALL_METHOD_2         2  ''
              160  CALL_FUNCTION_1       1  ''
              162  BINARY_ADD       
              164  LOAD_STR                 '"'
              166  BINARY_ADD       
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34


    encode_basestring_ascii = c_encode_basestring_ascii or py_encode_basestring_ascii

    class JSONEncoder(object):
        __doc__ = 'Extensible JSON <http://json.org> encoder for Python data structures.\n\n    Supports the following objects and types by default:\n\n    +-------------------+---------------+\n    | Python            | JSON          |\n    +===================+===============+\n    | dict, namedtuple  | object        |\n    +-------------------+---------------+\n    | list, tuple       | array         |\n    +-------------------+---------------+\n    | str, unicode      | string        |\n    +-------------------+---------------+\n    | int, long, float  | number        |\n    +-------------------+---------------+\n    | True              | true          |\n    +-------------------+---------------+\n    | False             | false         |\n    +-------------------+---------------+\n    | None              | null          |\n    +-------------------+---------------+\n\n    To extend this to recognize other objects, subclass and implement a\n    ``.default()`` method with another method that returns a serializable\n    object for ``o`` if possible, otherwise it should call the superclass\n    implementation (to raise ``TypeError``).\n\n    '
        item_separator = ', '
        key_separator = ': '

        def __init__--- This code section failed: ---

 L. 229         0  LOAD_FAST                'skipkeys'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               skipkeys

 L. 230         6  LOAD_FAST                'ensure_ascii'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               ensure_ascii

 L. 231        12  LOAD_FAST                'check_circular'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               check_circular

 L. 232        18  LOAD_FAST                'allow_nan'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               allow_nan

 L. 233        24  LOAD_FAST                'sort_keys'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               sort_keys

 L. 234        30  LOAD_FAST                'use_decimal'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               use_decimal

 L. 235        36  LOAD_FAST                'namedtuple_as_object'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               namedtuple_as_object

 L. 236        42  LOAD_FAST                'tuple_as_array'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               tuple_as_array

 L. 237        48  LOAD_FAST                'iterable_as_array'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               iterable_as_array

 L. 238        54  LOAD_FAST                'bigint_as_string'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               bigint_as_string

 L. 239        60  LOAD_FAST                'item_sort_key'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               item_sort_key

 L. 240        66  LOAD_FAST                'for_json'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               for_json

 L. 241        72  LOAD_FAST                'ignore_nan'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               ignore_nan

 L. 242        78  LOAD_FAST                'int_as_string_bitcount'
               80  LOAD_FAST                'self'
               82  STORE_ATTR               int_as_string_bitcount

 L. 243        84  LOAD_FAST                'indent'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   110  'to 110'
               92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                'indent'
               96  LOAD_GLOBAL              string_types
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_TRUE    110  'to 110'

 L. 244       102  LOAD_FAST                'indent'
              104  LOAD_STR                 ' '
              106  BINARY_MULTIPLY  
              108  STORE_FAST               'indent'
            110_0  COME_FROM           100  '100'
            110_1  COME_FROM            90  '90'

 L. 245       110  LOAD_FAST                'indent'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               indent

 L. 246       116  LOAD_FAST                'separators'
              118  LOAD_CONST               None
              120  <117>                 1  ''
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L. 247       124  LOAD_FAST                'separators'
              126  UNPACK_SEQUENCE_2     2 
              128  LOAD_FAST                'self'
              130  STORE_ATTR               item_separator
              132  LOAD_FAST                'self'
              134  STORE_ATTR               key_separator
              136  JUMP_FORWARD        152  'to 152'
            138_0  COME_FROM           122  '122'

 L. 248       138  LOAD_FAST                'indent'
              140  LOAD_CONST               None
              142  <117>                 1  ''
              144  POP_JUMP_IF_FALSE   152  'to 152'

 L. 249       146  LOAD_STR                 ','
              148  LOAD_FAST                'self'
              150  STORE_ATTR               item_separator
            152_0  COME_FROM           144  '144'
            152_1  COME_FROM           136  '136'

 L. 250       152  LOAD_FAST                'default'
              154  LOAD_CONST               None
              156  <117>                 1  ''
              158  POP_JUMP_IF_FALSE   166  'to 166'

 L. 251       160  LOAD_FAST                'default'
              162  LOAD_FAST                'self'
              164  STORE_ATTR               default
            166_0  COME_FROM           158  '158'

 L. 252       166  LOAD_FAST                'encoding'
              168  LOAD_FAST                'self'
              170  STORE_ATTR               encoding

Parse error at or near `<117>' instruction at offset 88

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
                return JSONEncoder.default(self, o)

        """
            raise TypeError('Object of type %s is not JSON serializable' % o.__class__.__name__)

        def encode--- This code section failed: ---

 L. 284         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'o'
                4  LOAD_GLOBAL              binary_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L. 285        10  LOAD_FAST                'self'
               12  LOAD_ATTR                encoding
               14  STORE_FAST               '_encoding'

 L. 286        16  LOAD_FAST                '_encoding'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  LOAD_FAST                '_encoding'
               26  LOAD_STR                 'utf-8'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_TRUE     42  'to 42'

 L. 287        32  LOAD_GLOBAL              text_type
               34  LOAD_FAST                'o'
               36  LOAD_FAST                '_encoding'
               38  CALL_FUNCTION_2       2  ''
               40  STORE_FAST               'o'
             42_0  COME_FROM            30  '30'
             42_1  COME_FROM            22  '22'
             42_2  COME_FROM             8  '8'

 L. 288        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'o'
               46  LOAD_GLOBAL              string_types
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 289        52  LOAD_FAST                'self'
               54  LOAD_ATTR                ensure_ascii
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 290        58  LOAD_GLOBAL              encode_basestring_ascii
               60  LOAD_FAST                'o'
               62  CALL_FUNCTION_1       1  ''
               64  RETURN_VALUE     
             66_0  COME_FROM            56  '56'

 L. 292        66  LOAD_GLOBAL              encode_basestring
               68  LOAD_FAST                'o'
               70  CALL_FUNCTION_1       1  ''
               72  RETURN_VALUE     
             74_0  COME_FROM            50  '50'

 L. 296        74  LOAD_FAST                'self'
               76  LOAD_ATTR                iterencode
               78  LOAD_FAST                'o'
               80  LOAD_CONST               True
               82  LOAD_CONST               ('_one_shot',)
               84  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               86  STORE_FAST               'chunks'

 L. 297        88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'chunks'
               92  LOAD_GLOBAL              list
               94  LOAD_GLOBAL              tuple
               96  BUILD_TUPLE_2         2 
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_TRUE    110  'to 110'

 L. 298       102  LOAD_GLOBAL              list
              104  LOAD_FAST                'chunks'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'chunks'
            110_0  COME_FROM           100  '100'

 L. 299       110  LOAD_FAST                'self'
              112  LOAD_ATTR                ensure_ascii
              114  POP_JUMP_IF_FALSE   126  'to 126'

 L. 300       116  LOAD_STR                 ''
              118  LOAD_METHOD              join
              120  LOAD_FAST                'chunks'
              122  CALL_METHOD_1         1  ''
              124  RETURN_VALUE     
            126_0  COME_FROM           114  '114'

 L. 302       126  LOAD_STR                 ''
              128  LOAD_METHOD              join
              130  LOAD_FAST                'chunks'
              132  CALL_METHOD_1         1  ''
              134  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 20

        def iterencode--- This code section failed: ---

 L. 314         0  LOAD_FAST                'self'
                2  LOAD_ATTR                check_circular
                4  POP_JUMP_IF_FALSE    12  'to 12'

 L. 315         6  BUILD_MAP_0           0 
                8  STORE_FAST               'markers'
               10  JUMP_FORWARD         16  'to 16'
             12_0  COME_FROM             4  '4'

 L. 317        12  LOAD_CONST               None
               14  STORE_FAST               'markers'
             16_0  COME_FROM            10  '10'

 L. 318        16  LOAD_FAST                'self'
               18  LOAD_ATTR                ensure_ascii
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 319        22  LOAD_GLOBAL              encode_basestring_ascii
               24  STORE_FAST               '_encoder'
               26  JUMP_FORWARD         32  'to 32'
             28_0  COME_FROM            20  '20'

 L. 321        28  LOAD_GLOBAL              encode_basestring
               30  STORE_FAST               '_encoder'
             32_0  COME_FROM            26  '26'

 L. 322        32  LOAD_FAST                'self'
               34  LOAD_ATTR                encoding
               36  LOAD_STR                 'utf-8'
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE    68  'to 68'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                encoding
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    68  'to 68'

 L. 323        52  LOAD_FAST                '_encoder'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                encoding
               58  BUILD_TUPLE_2         2 
               60  LOAD_CODE                <code_object _encoder>
               62  LOAD_STR                 'JSONEncoder.iterencode.<locals>._encoder'
               64  MAKE_FUNCTION_1          'default'
               66  STORE_FAST               '_encoder'
             68_0  COME_FROM            50  '50'
             68_1  COME_FROM            40  '40'

 L. 328        68  LOAD_FAST                'self'
               70  LOAD_ATTR                allow_nan
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                ignore_nan

 L. 329        76  LOAD_GLOBAL              FLOAT_REPR
               78  LOAD_GLOBAL              PosInf
               80  LOAD_GLOBAL              PosInf
               82  UNARY_NEGATIVE   

 L. 328        84  BUILD_TUPLE_5         5 
               86  LOAD_CODE                <code_object floatstr>
               88  LOAD_STR                 'JSONEncoder.iterencode.<locals>.floatstr'
               90  MAKE_FUNCTION_1          'default'
               92  STORE_FAST               'floatstr'

 L. 355        94  BUILD_MAP_0           0 
               96  STORE_FAST               'key_memo'

 L. 357        98  LOAD_FAST                'self'
              100  LOAD_ATTR                bigint_as_string
              102  POP_JUMP_IF_FALSE   108  'to 108'
              104  LOAD_CONST               53
              106  JUMP_FORWARD        112  'to 112'
            108_0  COME_FROM           102  '102'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                int_as_string_bitcount
            112_0  COME_FROM           106  '106'

 L. 356       112  STORE_FAST               'int_as_string_bitcount'

 L. 358       114  LOAD_FAST                '_one_shot'
              116  POP_JUMP_IF_FALSE   216  'to 216'
              118  LOAD_GLOBAL              c_make_encoder
              120  LOAD_CONST               None
              122  <117>                 1  ''
              124  POP_JUMP_IF_FALSE   216  'to 216'

 L. 359       126  LOAD_FAST                'self'
              128  LOAD_ATTR                indent
              130  LOAD_CONST               None
              132  <117>                 0  ''

 L. 358       134  POP_JUMP_IF_FALSE   216  'to 216'

 L. 360       136  LOAD_GLOBAL              c_make_encoder

 L. 361       138  LOAD_FAST                'markers'
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                default
              144  LOAD_FAST                '_encoder'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                indent

 L. 362       150  LOAD_FAST                'self'
              152  LOAD_ATTR                key_separator
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                item_separator
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                sort_keys

 L. 363       162  LOAD_FAST                'self'
              164  LOAD_ATTR                skipkeys
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                allow_nan
              170  LOAD_FAST                'key_memo'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                use_decimal

 L. 364       176  LOAD_FAST                'self'
              178  LOAD_ATTR                namedtuple_as_object
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                tuple_as_array

 L. 365       184  LOAD_FAST                'int_as_string_bitcount'

 L. 366       186  LOAD_FAST                'self'
              188  LOAD_ATTR                item_sort_key
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                encoding
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                for_json

 L. 367       198  LOAD_FAST                'self'
              200  LOAD_ATTR                ignore_nan
              202  LOAD_GLOBAL              decimal
              204  LOAD_ATTR                Decimal
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                iterable_as_array

 L. 360       210  CALL_FUNCTION_20     20  ''
              212  STORE_FAST               '_iterencode'
              214  JUMP_FORWARD        290  'to 290'
            216_0  COME_FROM           134  '134'
            216_1  COME_FROM           124  '124'
            216_2  COME_FROM           116  '116'

 L. 369       216  LOAD_GLOBAL              _make_iterencode

 L. 370       218  LOAD_FAST                'markers'
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                default
              224  LOAD_FAST                '_encoder'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                indent
              230  LOAD_FAST                'floatstr'

 L. 371       232  LOAD_FAST                'self'
              234  LOAD_ATTR                key_separator
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                item_separator
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                sort_keys

 L. 372       244  LOAD_FAST                'self'
              246  LOAD_ATTR                skipkeys
              248  LOAD_FAST                '_one_shot'
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                use_decimal

 L. 373       254  LOAD_FAST                'self'
              256  LOAD_ATTR                namedtuple_as_object
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                tuple_as_array

 L. 374       262  LOAD_FAST                'int_as_string_bitcount'

 L. 375       264  LOAD_FAST                'self'
              266  LOAD_ATTR                item_sort_key
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                encoding
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                for_json

 L. 376       276  LOAD_FAST                'self'
              278  LOAD_ATTR                iterable_as_array
              280  LOAD_GLOBAL              decimal
              282  LOAD_ATTR                Decimal

 L. 369       284  LOAD_CONST               ('Decimal',)
              286  CALL_FUNCTION_KW_19    19  '19 total positional and keyword args'
              288  STORE_FAST               '_iterencode'
            290_0  COME_FROM           214  '214'

 L. 377       290  SETUP_FINALLY       312  'to 312'

 L. 378       292  LOAD_FAST                '_iterencode'
              294  LOAD_FAST                'o'
              296  LOAD_CONST               0
              298  CALL_FUNCTION_2       2  ''
              300  POP_BLOCK        

 L. 380       302  LOAD_FAST                'key_memo'
              304  LOAD_METHOD              clear
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          

 L. 378       310  RETURN_VALUE     
            312_0  COME_FROM_FINALLY   290  '290'

 L. 380       312  LOAD_FAST                'key_memo'
              314  LOAD_METHOD              clear
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          
              320  <48>             

Parse error at or near `<117>' instruction at offset 48


    class JSONEncoderForHTML(JSONEncoder):
        __doc__ = 'An encoder that produces JSON safe to embed in HTML.\n\n    To embed JSON content in, say, a script tag on a web page, the\n    characters &, < and > should be escaped. They cannot be escaped\n    with the usual entities (e.g. &amp;) because they are not expanded\n    within <script> tags.\n\n    This class also escapes the line separator and paragraph separator\n    characters U+2028 and U+2029, irrespective of the ensure_ascii setting,\n    as these characters are not valid in JavaScript strings (see\n    http://timelessrepo.com/json-isnt-a-javascript-subset).\n    '

        def encode(self, o):
            chunks = self.iterencode(o, True)
            if self.ensure_ascii:
                return ''.join(chunks)
            return ''.join(chunks)

        def iterencode(self, o, _one_shot=False):
            chunks = superJSONEncoderForHTMLself.iterencode(o, _one_shot)
            for chunk in chunks:
                chunk = chunk.replace('&', '\\u0026')
                chunk = chunk.replace('<', '\\u003c')
                chunk = chunk.replace('>', '\\u003e')
                if not self.ensure_ascii:
                    chunk = chunk.replace('\u2028', '\\u2028')
                    chunk = chunk.replace('\u2029', '\\u2029')
                else:
                    yield chunk


    def _make_iterencode--- This code section failed: ---

 L. 441         0  LOAD_DEREF               '_use_decimal'
                2  POP_JUMP_IF_FALSE    18  'to 18'
                4  LOAD_DEREF               'Decimal'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 442        12  LOAD_GLOBAL              decimal
               14  LOAD_ATTR                Decimal
               16  STORE_DEREF              'Decimal'
             18_0  COME_FROM            10  '10'
             18_1  COME_FROM             2  '2'

 L. 443        18  LOAD_DEREF               '_item_sort_key'
               20  POP_JUMP_IF_FALSE    40  'to 40'
               22  LOAD_GLOBAL              callable
               24  LOAD_DEREF               '_item_sort_key'
               26  CALL_FUNCTION_1       1  ''
               28  POP_JUMP_IF_TRUE     40  'to 40'

 L. 444        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'item_sort_key must be None or callable'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
               38  JUMP_FORWARD         56  'to 56'
             40_0  COME_FROM            28  '28'
             40_1  COME_FROM            20  '20'

 L. 445        40  LOAD_FAST                '_sort_keys'
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  LOAD_DEREF               '_item_sort_key'
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 446        48  LOAD_GLOBAL              itemgetter
               50  LOAD_CONST               0
               52  CALL_FUNCTION_1       1  ''
               54  STORE_DEREF              '_item_sort_key'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            42  '42'
             56_2  COME_FROM            38  '38'

 L. 448        56  LOAD_DEREF               '_int_as_string_bitcount'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    90  'to 90'

 L. 449        64  LOAD_DEREF               '_int_as_string_bitcount'
               66  LOAD_CONST               0
               68  COMPARE_OP               <=

 L. 448        70  POP_JUMP_IF_TRUE     82  'to 82'

 L. 450        72  LOAD_DEREF               'isinstance'
               74  LOAD_DEREF               '_int_as_string_bitcount'
               76  LOAD_DEREF               'integer_types'
               78  CALL_FUNCTION_2       2  ''

 L. 448        80  POP_JUMP_IF_TRUE     90  'to 90'
             82_0  COME_FROM            70  '70'

 L. 451        82  LOAD_GLOBAL              TypeError
               84  LOAD_STR                 'int_as_string_bitcount must be a positive integer'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'
             90_1  COME_FROM            62  '62'

 L. 453        90  LOAD_CLOSURE             '_int_as_string_bitcount'
               92  LOAD_CLOSURE             'integer_types'
               94  LOAD_CLOSURE             'str'
               96  BUILD_TUPLE_3         3 
               98  LOAD_CODE                <code_object _encode_int>
              100  LOAD_STR                 '_make_iterencode.<locals>._encode_int'
              102  MAKE_FUNCTION_8          'closure'
              104  STORE_DEREF              '_encode_int'

 L. 471       106  LOAD_CLOSURE             'Decimal'
              108  LOAD_CLOSURE             'ValueError'
              110  LOAD_CLOSURE             '_PY3'
              112  LOAD_CLOSURE             '_encode_int'
              114  LOAD_CLOSURE             '_encoder'
              116  LOAD_CLOSURE             '_encoding'
              118  LOAD_CLOSURE             '_floatstr'
              120  LOAD_CLOSURE             '_for_json'
              122  LOAD_CLOSURE             '_indent'
              124  LOAD_CLOSURE             '_item_separator'
              126  LOAD_CLOSURE             '_iterencode'
              128  LOAD_CLOSURE             '_iterencode_dict'
              130  LOAD_CLOSURE             '_iterencode_list'
              132  LOAD_CLOSURE             '_namedtuple_as_object'
              134  LOAD_CLOSURE             '_tuple_as_array'
              136  LOAD_CLOSURE             '_use_decimal'
              138  LOAD_CLOSURE             'dict'
              140  LOAD_CLOSURE             'float'
              142  LOAD_CLOSURE             'id'
              144  LOAD_CLOSURE             'integer_types'
              146  LOAD_CLOSURE             'isinstance'
              148  LOAD_CLOSURE             'list'
              150  LOAD_CLOSURE             'markers'
              152  LOAD_CLOSURE             'str'
              154  LOAD_CLOSURE             'string_types'
              156  LOAD_CLOSURE             'tuple'
              158  BUILD_TUPLE_26       26 
              160  LOAD_CODE                <code_object _iterencode_list>
              162  LOAD_STR                 '_make_iterencode.<locals>._iterencode_list'
              164  MAKE_FUNCTION_8          'closure'
              166  STORE_DEREF              '_iterencode_list'

 L. 544       168  LOAD_CLOSURE             'Decimal'
              170  LOAD_CLOSURE             '_PY3'
              172  LOAD_CLOSURE             '_encoding'
              174  LOAD_CLOSURE             '_floatstr'
              176  LOAD_CLOSURE             '_skipkeys'
              178  LOAD_CLOSURE             '_use_decimal'
              180  LOAD_CLOSURE             'float'
              182  LOAD_CLOSURE             'integer_types'
              184  LOAD_CLOSURE             'isinstance'
              186  LOAD_CLOSURE             'str'
              188  LOAD_CLOSURE             'string_types'
              190  BUILD_TUPLE_11       11 
              192  LOAD_CODE                <code_object _stringify_key>
              194  LOAD_STR                 '_make_iterencode.<locals>._stringify_key'
              196  MAKE_FUNCTION_8          'closure'
              198  STORE_DEREF              '_stringify_key'

 L. 571       200  LOAD_CLOSURE             'Decimal'
              202  LOAD_CLOSURE             'ValueError'
              204  LOAD_CLOSURE             '_PY3'
              206  LOAD_CLOSURE             '_encode_int'
              208  LOAD_CLOSURE             '_encoder'
              210  LOAD_CLOSURE             '_encoding'
              212  LOAD_CLOSURE             '_floatstr'
              214  LOAD_CLOSURE             '_for_json'
              216  LOAD_CLOSURE             '_indent'
              218  LOAD_CLOSURE             '_item_separator'
              220  LOAD_CLOSURE             '_item_sort_key'
              222  LOAD_CLOSURE             '_iterencode'
              224  LOAD_CLOSURE             '_iterencode_dict'
              226  LOAD_CLOSURE             '_iterencode_list'
              228  LOAD_CLOSURE             '_key_separator'
              230  LOAD_CLOSURE             '_namedtuple_as_object'
              232  LOAD_CLOSURE             '_stringify_key'
              234  LOAD_CLOSURE             '_tuple_as_array'
              236  LOAD_CLOSURE             '_use_decimal'
              238  LOAD_CLOSURE             'dict'
              240  LOAD_CLOSURE             'float'
              242  LOAD_CLOSURE             'id'
              244  LOAD_CLOSURE             'integer_types'
              246  LOAD_CLOSURE             'isinstance'
              248  LOAD_CLOSURE             'list'
              250  LOAD_CLOSURE             'markers'
              252  LOAD_CLOSURE             'str'
              254  LOAD_CLOSURE             'string_types'
              256  LOAD_CLOSURE             'tuple'
              258  BUILD_TUPLE_29       29 
              260  LOAD_CODE                <code_object _iterencode_dict>
              262  LOAD_STR                 '_make_iterencode.<locals>._iterencode_dict'
              264  MAKE_FUNCTION_8          'closure'
              266  STORE_DEREF              '_iterencode_dict'

 L. 661       268  LOAD_CLOSURE             'Decimal'
              270  LOAD_CLOSURE             'ValueError'
              272  LOAD_CLOSURE             '_PY3'
              274  LOAD_CLOSURE             '_default'
              276  LOAD_CLOSURE             '_encode_int'
              278  LOAD_CLOSURE             '_encoder'
              280  LOAD_CLOSURE             '_encoding'
              282  LOAD_CLOSURE             '_floatstr'
              284  LOAD_CLOSURE             '_for_json'
              286  LOAD_CLOSURE             '_iterable_as_array'
              288  LOAD_CLOSURE             '_iterencode'
              290  LOAD_CLOSURE             '_iterencode_dict'
              292  LOAD_CLOSURE             '_iterencode_list'
              294  LOAD_CLOSURE             '_namedtuple_as_object'
              296  LOAD_CLOSURE             '_tuple_as_array'
              298  LOAD_CLOSURE             '_use_decimal'
              300  LOAD_CLOSURE             'dict'
              302  LOAD_CLOSURE             'float'
              304  LOAD_CLOSURE             'id'
              306  LOAD_CLOSURE             'integer_types'
              308  LOAD_CLOSURE             'isinstance'
              310  LOAD_CLOSURE             'iter'
              312  LOAD_CLOSURE             'list'
              314  LOAD_CLOSURE             'markers'
              316  LOAD_CLOSURE             'str'
              318  LOAD_CLOSURE             'string_types'
              320  LOAD_CLOSURE             'tuple'
              322  BUILD_TUPLE_27       27 
              324  LOAD_CODE                <code_object _iterencode>
              326  LOAD_STR                 '_make_iterencode.<locals>._iterencode'
              328  MAKE_FUNCTION_8          'closure'
              330  STORE_DEREF              '_iterencode'

 L. 722       332  LOAD_DEREF               '_iterencode'
              334  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1