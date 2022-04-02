# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymysql\converters.py
from ._compat import PY2, text_type, long_type, JYTHON, IRONPYTHON, unichr
import datetime
from decimal import Decimal
import re, time
from .constants import FIELD_TYPE, FLAG
from .charset import charset_by_id, charset_to_encoding

def escape_item(val, charset, mapping=None):
    if mapping is None:
        mapping = encoders
    else:
        encoder = mapping.get(type(val))
        if not encoder:
            try:
                encoder = mapping[text_type]
            except KeyError:
                raise TypeError('no default type converter defined')
            else:
                if encoder in (escape_dict, escape_sequence):
                    val = encoder(val, charset, mapping)
        else:
            pass
        val = encoder(val, mapping)
    return val


def escape_dict(val, charset, mapping=None):
    n = {}
    for k, v in val.items():
        quoted = escape_item(v, charset, mapping)
        n[k] = quoted
    else:
        return n


def escape_sequence(val, charset, mapping=None):
    n = []
    for item in val:
        quoted = escape_item(item, charset, mapping)
        n.append(quoted)
    else:
        return '(' + ','.join(n) + ')'


def escape_set(val, charset, mapping=None):
    return ','.join([escape_item(x, charset, mapping) for x in val])


def escape_bool(value, mapping=None):
    return str(int(value))


def escape_object(value, mapping=None):
    return str(value)


def escape_int(value, mapping=None):
    return str(value)


def escape_float(value, mapping=None):
    return '%.15g' % value


_escape_table = [unichr(x) for x in range(128)]
_escape_table[0] = '\\0'
_escape_table[ord('\\')] = '\\\\'
_escape_table[ord('\n')] = '\\n'
_escape_table[ord('\r')] = '\\r'
_escape_table[ord('\x1a')] = '\\Z'
_escape_table[ord('"')] = '\\"'
_escape_table[ord("'")] = "\\'"

def _escape_unicode(value, mapping=None):
    """escapes *value* without adding quote.

    Value should be unicode
    """
    return value.translate(_escape_table)


if PY2:

    def escape_string(value, mapping=None):
        """escape_string escapes *value* but not surround it with quotes.

        Value should be bytes or unicode.
        """
        if isinstance(value, unicode):
            return _escape_unicode(value)
        assert isinstance(value, (bytes, bytearray))
        value = value.replace('\\', '\\\\')
        value = value.replace('\x00', '\\0')
        value = value.replace('\n', '\\n')
        value = value.replace('\r', '\\r')
        value = value.replace('\x1a', '\\Z')
        value = value.replace("'", "\\'")
        value = value.replace('"', '\\"')
        return value


    def escape_bytes_prefixed(value, mapping=None):
        assert isinstance(value, (bytes, bytearray))
        return b"_binary'%s'" % escape_string(value)


    def escape_bytes(value, mapping=None):
        assert isinstance(value, (bytes, bytearray))
        return b"'%s'" % escape_string(value)


else:
    escape_string = _escape_unicode
    _escape_bytes_table = _escape_table + [chr(i) for i in range(56448, 56576)]

    def escape_bytes_prefixed(value, mapping=None):
        return "_binary'%s'" % value.decode('latin1').translate(_escape_bytes_table)


    def escape_bytes(value, mapping=None):
        return "'%s'" % value.decode('latin1').translate(_escape_bytes_table)


def escape_unicode(value, mapping=None):
    return "'%s'" % _escape_unicode(value)


def escape_str(value, mapping=None):
    return "'%s'" % escape_string(str(value), mapping)


def escape_None(value, mapping=None):
    return 'NULL'


def escape_timedelta(obj, mapping=None):
    seconds = int(obj.seconds) % 60
    minutes = int(obj.seconds // 60) % 60
    hours = int(obj.seconds // 3600) % 24 + int(obj.days) * 24
    if obj.microseconds:
        fmt = "'{0:02d}:{1:02d}:{2:02d}.{3:06d}'"
    else:
        fmt = "'{0:02d}:{1:02d}:{2:02d}'"
    return fmt.format(hours, minutes, seconds, obj.microseconds)


def escape_time(obj, mapping=None):
    if obj.microsecond:
        fmt = "'{0.hour:02}:{0.minute:02}:{0.second:02}.{0.microsecond:06}'"
    else:
        fmt = "'{0.hour:02}:{0.minute:02}:{0.second:02}'"
    return fmt.format(obj)


def escape_datetime(obj, mapping=None):
    if obj.microsecond:
        fmt = "'{0.year:04}-{0.month:02}-{0.day:02} {0.hour:02}:{0.minute:02}:{0.second:02}.{0.microsecond:06}'"
    else:
        fmt = "'{0.year:04}-{0.month:02}-{0.day:02} {0.hour:02}:{0.minute:02}:{0.second:02}'"
    return fmt.format(obj)


def escape_date(obj, mapping=None):
    fmt = "'{0.year:04}-{0.month:02}-{0.day:02}'"
    return fmt.format(obj)


def escape_struct_time(obj, mapping=None):
    return escape_datetime((datetime.datetime)(*obj[:6]))


def _convert_second_fraction(s):
    if not s:
        return 0
    s = s.ljust(6, '0')
    return int(s[:6])


DATETIME_RE = re.compile('(\\d{1,4})-(\\d{1,2})-(\\d{1,2})[T ](\\d{1,2}):(\\d{1,2}):(\\d{1,2})(?:.(\\d{1,6}))?')

def convert_datetime--- This code section failed: ---

 L. 183         0  LOAD_GLOBAL              PY2
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'obj'
                8  LOAD_GLOBAL              bytes
               10  LOAD_GLOBAL              bytearray
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 184        18  LOAD_FAST                'obj'
               20  LOAD_METHOD              decode
               22  LOAD_STR                 'ascii'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'obj'
             28_0  COME_FROM            16  '16'
             28_1  COME_FROM             2  '2'

 L. 186        28  LOAD_GLOBAL              DATETIME_RE
               30  LOAD_METHOD              match
               32  LOAD_FAST                'obj'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'm'

 L. 187        38  LOAD_FAST                'm'
               40  POP_JUMP_IF_TRUE     50  'to 50'

 L. 188        42  LOAD_GLOBAL              convert_date
               44  LOAD_FAST                'obj'
               46  CALL_FUNCTION_1       1  ''
               48  RETURN_VALUE     
             50_0  COME_FROM            40  '40'

 L. 190        50  SETUP_FINALLY       102  'to 102'

 L. 191        52  LOAD_GLOBAL              list
               54  LOAD_FAST                'm'
               56  LOAD_METHOD              groups
               58  CALL_METHOD_0         0  ''
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'groups'

 L. 192        64  LOAD_GLOBAL              _convert_second_fraction
               66  LOAD_FAST                'groups'
               68  LOAD_CONST               -1
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_FAST                'groups'
               76  LOAD_CONST               -1
               78  STORE_SUBSCR     

 L. 193        80  LOAD_GLOBAL              datetime
               82  LOAD_ATTR                datetime
               84  LOAD_LISTCOMP            '<code_object <listcomp>>'
               86  LOAD_STR                 'convert_datetime.<locals>.<listcomp>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_FAST                'groups'
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  CALL_FUNCTION_EX      0  'positional arguments only'
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY    50  '50'

 L. 194       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 195       116  LOAD_GLOBAL              convert_date
              118  LOAD_FAST                'obj'
              120  CALL_FUNCTION_1       1  ''
              122  ROT_FOUR         
              124  POP_EXCEPT       
              126  RETURN_VALUE     
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 112


TIMEDELTA_RE = re.compile('(-)?(\\d{1,3}):(\\d{1,2}):(\\d{1,2})(?:.(\\d{1,6}))?')

def convert_timedelta--- This code section failed: ---

 L. 217         0  LOAD_GLOBAL              PY2
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'obj'
                8  LOAD_GLOBAL              bytes
               10  LOAD_GLOBAL              bytearray
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 218        18  LOAD_FAST                'obj'
               20  LOAD_METHOD              decode
               22  LOAD_STR                 'ascii'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'obj'
             28_0  COME_FROM            16  '16'
             28_1  COME_FROM             2  '2'

 L. 220        28  LOAD_GLOBAL              TIMEDELTA_RE
               30  LOAD_METHOD              match
               32  LOAD_FAST                'obj'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'm'

 L. 221        38  LOAD_FAST                'm'
               40  POP_JUMP_IF_TRUE     46  'to 46'

 L. 222        42  LOAD_FAST                'obj'
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L. 224        46  SETUP_FINALLY       156  'to 156'

 L. 225        48  LOAD_GLOBAL              list
               50  LOAD_FAST                'm'
               52  LOAD_METHOD              groups
               54  CALL_METHOD_0         0  ''
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'groups'

 L. 226        60  LOAD_GLOBAL              _convert_second_fraction
               62  LOAD_FAST                'groups'
               64  LOAD_CONST               -1
               66  BINARY_SUBSCR    
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'groups'
               72  LOAD_CONST               -1
               74  STORE_SUBSCR     

 L. 227        76  LOAD_FAST                'groups'
               78  LOAD_CONST               0
               80  BINARY_SUBSCR    
               82  POP_JUMP_IF_FALSE    88  'to 88'
               84  LOAD_CONST               -1
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            82  '82'
               88  LOAD_CONST               1
             90_0  COME_FROM            86  '86'
               90  STORE_FAST               'negate'

 L. 228        92  LOAD_FAST                'groups'
               94  LOAD_CONST               1
               96  LOAD_CONST               None
               98  BUILD_SLICE_2         2 
              100  BINARY_SUBSCR    
              102  UNPACK_SEQUENCE_4     4 
              104  STORE_FAST               'hours'
              106  STORE_FAST               'minutes'
              108  STORE_FAST               'seconds'
              110  STORE_FAST               'microseconds'

 L. 230       112  LOAD_GLOBAL              datetime
              114  LOAD_ATTR                timedelta

 L. 231       116  LOAD_GLOBAL              int
              118  LOAD_FAST                'hours'
              120  CALL_FUNCTION_1       1  ''

 L. 232       122  LOAD_GLOBAL              int
              124  LOAD_FAST                'minutes'
              126  CALL_FUNCTION_1       1  ''

 L. 233       128  LOAD_GLOBAL              int
              130  LOAD_FAST                'seconds'
              132  CALL_FUNCTION_1       1  ''

 L. 234       134  LOAD_GLOBAL              int
              136  LOAD_FAST                'microseconds'
              138  CALL_FUNCTION_1       1  ''

 L. 230       140  LOAD_CONST               ('hours', 'minutes', 'seconds', 'microseconds')
              142  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 235       144  LOAD_FAST                'negate'

 L. 230       146  BINARY_MULTIPLY  
              148  STORE_FAST               'tdelta'

 L. 236       150  LOAD_FAST                'tdelta'
              152  POP_BLOCK        
              154  RETURN_VALUE     
            156_0  COME_FROM_FINALLY    46  '46'

 L. 237       156  DUP_TOP          
              158  LOAD_GLOBAL              ValueError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   178  'to 178'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 238       170  LOAD_FAST                'obj'
              172  ROT_FOUR         
              174  POP_EXCEPT       
              176  RETURN_VALUE     
            178_0  COME_FROM           162  '162'
              178  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 166


TIME_RE = re.compile('(\\d{1,2}):(\\d{1,2}):(\\d{1,2})(?:.(\\d{1,6}))?')

def convert_time--- This code section failed: ---

 L. 265         0  LOAD_GLOBAL              PY2
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'obj'
                8  LOAD_GLOBAL              bytes
               10  LOAD_GLOBAL              bytearray
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 266        18  LOAD_FAST                'obj'
               20  LOAD_METHOD              decode
               22  LOAD_STR                 'ascii'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'obj'
             28_0  COME_FROM            16  '16'
             28_1  COME_FROM             2  '2'

 L. 268        28  LOAD_GLOBAL              TIME_RE
               30  LOAD_METHOD              match
               32  LOAD_FAST                'obj'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'm'

 L. 269        38  LOAD_FAST                'm'
               40  POP_JUMP_IF_TRUE     46  'to 46'

 L. 270        42  LOAD_FAST                'obj'
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L. 272        46  SETUP_FINALLY       124  'to 124'

 L. 273        48  LOAD_GLOBAL              list
               50  LOAD_FAST                'm'
               52  LOAD_METHOD              groups
               54  CALL_METHOD_0         0  ''
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'groups'

 L. 274        60  LOAD_GLOBAL              _convert_second_fraction
               62  LOAD_FAST                'groups'
               64  LOAD_CONST               -1
               66  BINARY_SUBSCR    
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'groups'
               72  LOAD_CONST               -1
               74  STORE_SUBSCR     

 L. 275        76  LOAD_FAST                'groups'
               78  UNPACK_SEQUENCE_4     4 
               80  STORE_FAST               'hours'
               82  STORE_FAST               'minutes'
               84  STORE_FAST               'seconds'
               86  STORE_FAST               'microseconds'

 L. 276        88  LOAD_GLOBAL              datetime
               90  LOAD_ATTR                time
               92  LOAD_GLOBAL              int
               94  LOAD_FAST                'hours'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_GLOBAL              int
              100  LOAD_FAST                'minutes'
              102  CALL_FUNCTION_1       1  ''

 L. 277       104  LOAD_GLOBAL              int
              106  LOAD_FAST                'seconds'
              108  CALL_FUNCTION_1       1  ''

 L. 277       110  LOAD_GLOBAL              int
              112  LOAD_FAST                'microseconds'
              114  CALL_FUNCTION_1       1  ''

 L. 276       116  LOAD_CONST               ('hour', 'minute', 'second', 'microsecond')
              118  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY    46  '46'

 L. 278       124  DUP_TOP          
              126  LOAD_GLOBAL              ValueError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 279       138  LOAD_FAST                'obj'
              140  ROT_FOUR         
              142  POP_EXCEPT       
              144  RETURN_VALUE     
            146_0  COME_FROM           130  '130'
              146  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 134


def convert_date--- This code section failed: ---

 L. 296         0  LOAD_GLOBAL              PY2
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'obj'
                8  LOAD_GLOBAL              bytes
               10  LOAD_GLOBAL              bytearray
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 297        18  LOAD_FAST                'obj'
               20  LOAD_METHOD              decode
               22  LOAD_STR                 'ascii'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'obj'
             28_0  COME_FROM            16  '16'
             28_1  COME_FROM             2  '2'

 L. 298        28  SETUP_FINALLY        60  'to 60'

 L. 299        30  LOAD_GLOBAL              datetime
               32  LOAD_ATTR                date
               34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 'convert_date.<locals>.<listcomp>'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  LOAD_FAST                'obj'
               42  LOAD_METHOD              split
               44  LOAD_STR                 '-'
               46  LOAD_CONST               2
               48  CALL_METHOD_2         2  ''
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_EX      0  'positional arguments only'
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    28  '28'

 L. 300        60  DUP_TOP          
               62  LOAD_GLOBAL              ValueError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    82  'to 82'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 301        74  LOAD_FAST                'obj'
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  RETURN_VALUE     
             82_0  COME_FROM            66  '66'
               82  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 70


def convert_mysql_timestamp--- This code section failed: ---

 L. 325         0  LOAD_GLOBAL              PY2
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'timestamp'
                8  LOAD_GLOBAL              bytes
               10  LOAD_GLOBAL              bytearray
               12  BUILD_TUPLE_2         2 
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 326        18  LOAD_FAST                'timestamp'
               20  LOAD_METHOD              decode
               22  LOAD_STR                 'ascii'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'timestamp'
             28_0  COME_FROM            16  '16'
             28_1  COME_FROM             2  '2'

 L. 327        28  LOAD_FAST                'timestamp'
               30  LOAD_CONST               4
               32  BINARY_SUBSCR    
               34  LOAD_STR                 '-'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 328        40  LOAD_GLOBAL              convert_datetime
               42  LOAD_FAST                'timestamp'
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            38  '38'

 L. 329        48  LOAD_FAST                'timestamp'
               50  LOAD_STR                 '0'
               52  LOAD_CONST               14
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'timestamp'
               58  CALL_FUNCTION_1       1  ''
               60  BINARY_SUBTRACT  
               62  BINARY_MULTIPLY  
               64  INPLACE_ADD      
               66  STORE_FAST               'timestamp'

 L. 331        68  LOAD_GLOBAL              int
               70  LOAD_FAST                'timestamp'
               72  LOAD_CONST               None
               74  LOAD_CONST               4
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_GLOBAL              int
               84  LOAD_FAST                'timestamp'
               86  LOAD_CONST               4
               88  LOAD_CONST               6
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_GLOBAL              int
               98  LOAD_FAST                'timestamp'
              100  LOAD_CONST               6
              102  LOAD_CONST               8
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  CALL_FUNCTION_1       1  ''

 L. 332       110  LOAD_GLOBAL              int
              112  LOAD_FAST                'timestamp'
              114  LOAD_CONST               8
              116  LOAD_CONST               10
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  CALL_FUNCTION_1       1  ''

 L. 332       124  LOAD_GLOBAL              int
              126  LOAD_FAST                'timestamp'
              128  LOAD_CONST               10
              130  LOAD_CONST               12
              132  BUILD_SLICE_2         2 
              134  BINARY_SUBSCR    
              136  CALL_FUNCTION_1       1  ''

 L. 332       138  LOAD_GLOBAL              int
              140  LOAD_FAST                'timestamp'
              142  LOAD_CONST               12
              144  LOAD_CONST               14
              146  BUILD_SLICE_2         2 
              148  BINARY_SUBSCR    
              150  CALL_FUNCTION_1       1  ''

 L. 331       152  BUILD_TUPLE_6         6 

 L. 330       154  UNPACK_SEQUENCE_6     6 
              156  STORE_FAST               'year'
              158  STORE_FAST               'month'
              160  STORE_FAST               'day'
              162  STORE_FAST               'hour'
              164  STORE_FAST               'minute'
              166  STORE_FAST               'second'

 L. 333       168  SETUP_FINALLY       192  'to 192'

 L. 334       170  LOAD_GLOBAL              datetime
              172  LOAD_METHOD              datetime
              174  LOAD_FAST                'year'
              176  LOAD_FAST                'month'
              178  LOAD_FAST                'day'
              180  LOAD_FAST                'hour'
              182  LOAD_FAST                'minute'
              184  LOAD_FAST                'second'
              186  CALL_METHOD_6         6  ''
              188  POP_BLOCK        
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY   168  '168'

 L. 335       192  DUP_TOP          
              194  LOAD_GLOBAL              ValueError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   214  'to 214'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 336       206  LOAD_FAST                'timestamp'
              208  ROT_FOUR         
              210  POP_EXCEPT       
              212  RETURN_VALUE     
            214_0  COME_FROM           198  '198'
              214  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 202


def convert_set(s):
    if isinstance(s, (bytes, bytearray)):
        return set(s.split(b','))
    return set(s.split(','))


def through(x):
    return x


convert_bit = through
encoders = {bool: escape_bool, 
 int: escape_int, 
 long_type: escape_int, 
 float: escape_float, 
 str: escape_str, 
 text_type: escape_unicode, 
 tuple: escape_sequence, 
 list: escape_sequence, 
 set: escape_sequence, 
 frozenset: escape_sequence, 
 dict: escape_dict, 
 type(None): escape_None, 
 datetime.date: escape_date, 
 datetime.datetime: escape_datetime, 
 datetime.timedelta: escape_timedelta, 
 datetime.time: escape_time, 
 time.struct_time: escape_struct_time, 
 Decimal: escape_object}
if not PY2 or JYTHON or IRONPYTHON:
    encoders[bytes] = escape_bytes
decoders = {FIELD_TYPE.BIT: convert_bit, 
 FIELD_TYPE.TINY: int, 
 FIELD_TYPE.SHORT: int, 
 FIELD_TYPE.LONG: int, 
 FIELD_TYPE.FLOAT: float, 
 FIELD_TYPE.DOUBLE: float, 
 FIELD_TYPE.LONGLONG: int, 
 FIELD_TYPE.INT24: int, 
 FIELD_TYPE.YEAR: int, 
 FIELD_TYPE.TIMESTAMP: convert_mysql_timestamp, 
 FIELD_TYPE.DATETIME: convert_datetime, 
 FIELD_TYPE.TIME: convert_timedelta, 
 FIELD_TYPE.DATE: convert_date, 
 FIELD_TYPE.SET: convert_set, 
 FIELD_TYPE.BLOB: through, 
 FIELD_TYPE.TINY_BLOB: through, 
 FIELD_TYPE.MEDIUM_BLOB: through, 
 FIELD_TYPE.LONG_BLOB: through, 
 FIELD_TYPE.STRING: through, 
 FIELD_TYPE.VAR_STRING: through, 
 FIELD_TYPE.VARCHAR: through, 
 FIELD_TYPE.DECIMAL: Decimal, 
 FIELD_TYPE.NEWDECIMAL: Decimal}
conversions = encoders.copy()
conversions.update(decoders)
Thing2Literal = escape_str