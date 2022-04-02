# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\future\backports\datetime.py
"""Concrete date/time and related types.

See http://www.iana.org/time-zones/repository/tz-link.html for
time zone and DST data sources.
"""
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future.builtins import str
from future.builtins import bytes
from future.builtins import map
from future.builtins import round
from future.builtins import int
from future.builtins import object
from future.utils import native_str, PY2
import time as _time, math as _math

def _cmp(x, y):
    if x == y:
        return 0
    if x > y:
        return 1
    return -1


MINYEAR = 1
MAXYEAR = 9999
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = [
 None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = [
 None]
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim

del dbm
del dim

def _is_leap(year):
    """year -> 1 if leap year, else 0."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_before_year(year):
    """year -> number of days before January 1st of year."""
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


def _days_in_month--- This code section failed: ---

 L.  57         0  LOAD_CONST               1
                3  LOAD_FAST             1  'month'
                6  DUP_TOP          
                7  ROT_THREE        
                8  COMPARE_OP            1  <=
               11  JUMP_IF_FALSE_OR_POP    23  'to 23'
               14  LOAD_CONST               12
               17  COMPARE_OP            1  <=
               20  JUMP_FORWARD          2  'to 25'
             23_0  COME_FROM            11  '11'
               23  ROT_TWO          
               24  POP_TOP          
             25_0  COME_FROM            20  '20'
               25  POP_JUMP_IF_TRUE     37  'to 37'
               28  LOAD_ASSERT              AssertionError
               31  LOAD_FAST             1  'month'
               34  RAISE_VARARGS_2       2  None

 L.  58        37  LOAD_FAST             1  'month'
               40  LOAD_CONST               2
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_FALSE    65  'to 65'
               49  LOAD_GLOBAL           1  '_is_leap'
               52  LOAD_FAST             0  'year'
               55  CALL_FUNCTION_1       1  None
             58_0  COME_FROM            46  '46'
               58  POP_JUMP_IF_FALSE    65  'to 65'

 L.  59        61  LOAD_CONST               29
               64  RETURN_END_IF    
             65_0  COME_FROM            58  '58'

 L.  60        65  LOAD_GLOBAL           2  '_DAYS_IN_MONTH'
               68  LOAD_FAST             1  'month'
               71  BINARY_SUBSCR    
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 72


def _days_before_month--- This code section failed: ---

 L.  64         0  LOAD_CONST               1
                3  LOAD_FAST             1  'month'
                6  DUP_TOP          
                7  ROT_THREE        
                8  COMPARE_OP            1  <=
               11  JUMP_IF_FALSE_OR_POP    23  'to 23'
               14  LOAD_CONST               12
               17  COMPARE_OP            1  <=
               20  JUMP_FORWARD          2  'to 25'
             23_0  COME_FROM            11  '11'
               23  ROT_TWO          
               24  POP_TOP          
             25_0  COME_FROM            20  '20'
               25  POP_JUMP_IF_TRUE     37  'to 37'
               28  LOAD_ASSERT              AssertionError
               31  LOAD_CONST               'month must be in 1..12'
               34  RAISE_VARARGS_2       2  None

 L.  65        37  LOAD_GLOBAL           1  '_DAYS_BEFORE_MONTH'
               40  LOAD_FAST             1  'month'
               43  BINARY_SUBSCR    
               44  LOAD_FAST             1  'month'
               47  LOAD_CONST               2
               50  COMPARE_OP            4  >
               53  JUMP_IF_FALSE_OR_POP    65  'to 65'
               56  LOAD_GLOBAL           2  '_is_leap'
               59  LOAD_FAST             0  'year'
               62  CALL_FUNCTION_1       1  None
             65_0  COME_FROM            53  '53'
               65  BINARY_ADD       
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 66


def _ymd2ord--- This code section failed: ---

 L.  69         0  LOAD_CONST               1
                3  LOAD_FAST             1  'month'
                6  DUP_TOP          
                7  ROT_THREE        
                8  COMPARE_OP            1  <=
               11  JUMP_IF_FALSE_OR_POP    23  'to 23'
               14  LOAD_CONST               12
               17  COMPARE_OP            1  <=
               20  JUMP_FORWARD          2  'to 25'
             23_0  COME_FROM            11  '11'
               23  ROT_TWO          
               24  POP_TOP          
             25_0  COME_FROM            20  '20'
               25  POP_JUMP_IF_TRUE     37  'to 37'
               28  LOAD_ASSERT              AssertionError
               31  LOAD_CONST               'month must be in 1..12'
               34  RAISE_VARARGS_2       2  None

 L.  70        37  LOAD_GLOBAL           1  '_days_in_month'
               40  LOAD_FAST             0  'year'
               43  LOAD_FAST             1  'month'
               46  CALL_FUNCTION_2       2  None
               49  STORE_FAST            3  'dim'

 L.  71        52  LOAD_CONST               1
               55  LOAD_FAST             2  'day'
               58  DUP_TOP          
               59  ROT_THREE        
               60  COMPARE_OP            1  <=
               63  JUMP_IF_FALSE_OR_POP    75  'to 75'
               66  LOAD_FAST             3  'dim'
               69  COMPARE_OP            1  <=
               72  JUMP_FORWARD          2  'to 77'
             75_0  COME_FROM            63  '63'
               75  ROT_TWO          
               76  POP_TOP          
             77_0  COME_FROM            72  '72'
               77  POP_JUMP_IF_TRUE     93  'to 93'
               80  LOAD_ASSERT              AssertionError
               83  LOAD_CONST               'day must be in 1..%d'
               86  LOAD_FAST             3  'dim'
               89  BINARY_MODULO    
               90  RAISE_VARARGS_2       2  None

 L.  73        93  LOAD_GLOBAL           2  '_days_before_year'
               96  LOAD_FAST             0  'year'
               99  CALL_FUNCTION_1       1  None
              102  LOAD_GLOBAL           3  '_days_before_month'
              105  LOAD_FAST             0  'year'
              108  LOAD_FAST             1  'month'
              111  CALL_FUNCTION_2       2  None
              114  BINARY_ADD       

 L.  74       115  LOAD_FAST             2  'day'
              118  BINARY_ADD       
              119  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 119


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)
assert _DI4Y == 4 * 365 + 1
assert _DI400Y == 4 * _DI100Y + 1
assert _DI100Y == 25 * _DI4Y - 1

def _ord2ymd(n):
    """ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."""
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400 + 1
    n100, n = divmod(n, _DI100Y)
    n4, n = divmod(n, _DI4Y)
    n1, n = divmod(n, 365)
    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        assert n == 0
        return (
         year - 1, 12, 31)
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == _is_leap(year)
    month = n + 50 >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
    if preceding > n:
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
    n -= preceding
    assert 0 <= n < _days_in_month(year, month)
    return (
     year, month, n + 1)


_MONTHNAMES = [
 None, b'Jan', b'Feb', b'Mar', b'Apr', b'May', b'Jun',
 b'Jul', b'Aug', b'Sep', b'Oct', b'Nov', b'Dec']
_DAYNAMES = [None, b'Mon', b'Tue', b'Wed', b'Thu', b'Fri', b'Sat', b'Sun']

def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 6) % 7
    dnum = _days_before_month(y, m) + d
    return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _format_time(hh, mm, ss, us):
    result = b'%02d:%02d:%02d' % (hh, mm, ss)
    if us:
        result += b'.%06d' % us
    return result


def _wrap_strftime--- This code section failed: ---

 L. 175         0  LOAD_CONST               None
                3  STORE_FAST            3  'freplace'

 L. 176         6  LOAD_CONST               None
                9  STORE_FAST            4  'zreplace'

 L. 177        12  LOAD_CONST               None
               15  STORE_FAST            5  'Zreplace'

 L. 180        18  BUILD_LIST_0          0 
               21  STORE_FAST            6  'newformat'

 L. 181        24  LOAD_FAST             6  'newformat'
               27  LOAD_ATTR             1  'append'
               30  STORE_FAST            7  'push'

 L. 182        33  LOAD_CONST               0
               36  LOAD_GLOBAL           2  'len'
               39  LOAD_FAST             1  'format'
               42  CALL_FUNCTION_1       1  None
               45  ROT_TWO          
               46  STORE_FAST            8  'i'
               49  STORE_FAST            9  'n'

 L. 183        52  SETUP_LOOP          549  'to 604'
               55  LOAD_FAST             8  'i'
               58  LOAD_FAST             9  'n'
               61  COMPARE_OP            0  <
               64  POP_JUMP_IF_FALSE   603  'to 603'

 L. 184        67  LOAD_FAST             1  'format'
               70  LOAD_FAST             8  'i'
               73  BINARY_SUBSCR    
               74  STORE_FAST           10  'ch'

 L. 185        77  LOAD_FAST             8  'i'
               80  LOAD_CONST               1
               83  INPLACE_ADD      
               84  STORE_FAST            8  'i'

 L. 186        87  LOAD_FAST            10  'ch'
               90  LOAD_CONST               '%'
               93  COMPARE_OP            2  ==
               96  POP_JUMP_IF_FALSE   590  'to 590'

 L. 187        99  LOAD_FAST             8  'i'
              102  LOAD_FAST             9  'n'
              105  COMPARE_OP            0  <
              108  POP_JUMP_IF_FALSE   577  'to 577'

 L. 188       111  LOAD_FAST             1  'format'
              114  LOAD_FAST             8  'i'
              117  BINARY_SUBSCR    
              118  STORE_FAST           10  'ch'

 L. 189       121  LOAD_FAST             8  'i'
              124  LOAD_CONST               1
              127  INPLACE_ADD      
              128  STORE_FAST            8  'i'

 L. 190       131  LOAD_FAST            10  'ch'
              134  LOAD_CONST               'f'
              137  COMPARE_OP            2  ==
              140  POP_JUMP_IF_FALSE   196  'to 196'

 L. 191       143  LOAD_FAST             3  'freplace'
              146  LOAD_CONST               None
              149  COMPARE_OP            8  is
              152  POP_JUMP_IF_FALSE   180  'to 180'

 L. 192       155  LOAD_CONST               '%06d'
              158  LOAD_GLOBAL           3  'getattr'
              161  LOAD_FAST             0  'object'

 L. 193       164  LOAD_CONST               'microsecond'
              167  LOAD_CONST               0
              170  CALL_FUNCTION_3       3  None
              173  BINARY_MODULO    
              174  STORE_FAST            3  'freplace'
              177  JUMP_FORWARD          0  'to 180'
            180_0  COME_FROM           177  '177'

 L. 194       180  LOAD_FAST             6  'newformat'
              183  LOAD_ATTR             1  'append'
              186  LOAD_FAST             3  'freplace'
              189  CALL_FUNCTION_1       1  None
              192  POP_TOP          
              193  JUMP_ABSOLUTE       587  'to 587'

 L. 195       196  LOAD_FAST            10  'ch'
              199  LOAD_CONST               'z'
              202  COMPARE_OP            2  ==
              205  POP_JUMP_IF_FALSE   442  'to 442'

 L. 196       208  LOAD_FAST             4  'zreplace'
              211  LOAD_CONST               None
              214  COMPARE_OP            8  is
              217  POP_JUMP_IF_FALSE   408  'to 408'

 L. 197       220  LOAD_CONST               ''
              223  STORE_FAST            4  'zreplace'

 L. 198       226  LOAD_GLOBAL           4  'hasattr'
              229  LOAD_FAST             0  'object'
              232  LOAD_CONST               'utcoffset'
              235  CALL_FUNCTION_2       2  None
              238  POP_JUMP_IF_FALSE   408  'to 408'

 L. 199       241  LOAD_FAST             0  'object'
              244  LOAD_ATTR             5  'utcoffset'
              247  CALL_FUNCTION_0       0  None
              250  STORE_FAST           11  'offset'

 L. 200       253  LOAD_FAST            11  'offset'
              256  LOAD_CONST               None
              259  COMPARE_OP            9  is-not
              262  POP_JUMP_IF_FALSE   405  'to 405'

 L. 201       265  LOAD_CONST               '+'
              268  STORE_FAST           12  'sign'

 L. 202       271  LOAD_FAST            11  'offset'
              274  LOAD_ATTR             6  'days'
              277  LOAD_CONST               0
              280  COMPARE_OP            0  <
              283  POP_JUMP_IF_FALSE   302  'to 302'

 L. 203       286  LOAD_FAST            11  'offset'
              289  UNARY_NEGATIVE   
              290  STORE_FAST           11  'offset'

 L. 204       293  LOAD_CONST               '-'
              296  STORE_FAST           12  'sign'
              299  JUMP_FORWARD          0  'to 302'
            302_0  COME_FROM           299  '299'

 L. 205       302  LOAD_GLOBAL           7  'divmod'
              305  LOAD_FAST            11  'offset'
              308  LOAD_GLOBAL           8  'timedelta'
              311  LOAD_CONST               'hours'
              314  LOAD_CONST               1
              317  CALL_FUNCTION_256   256  None
              320  CALL_FUNCTION_2       2  None
              323  UNPACK_SEQUENCE_2     2 
              326  STORE_FAST           13  'h'
              329  STORE_FAST           14  'm'

 L. 206       332  LOAD_FAST            14  'm'
              335  LOAD_GLOBAL           8  'timedelta'
              338  LOAD_CONST               'minutes'
              341  LOAD_CONST               1
              344  CALL_FUNCTION_256   256  None
              347  BINARY_MODULO    
              348  UNARY_NOT        
              349  POP_JUMP_IF_TRUE    361  'to 361'
              352  LOAD_ASSERT              AssertionError
              355  LOAD_CONST               'whole minute'
              358  RAISE_VARARGS_2       2  None

 L. 207       361  LOAD_FAST            14  'm'
              364  LOAD_GLOBAL           8  'timedelta'
              367  LOAD_CONST               'minutes'
              370  LOAD_CONST               1
              373  CALL_FUNCTION_256   256  None
              376  INPLACE_FLOOR_DIVIDE
              377  STORE_FAST           14  'm'

 L. 208       380  LOAD_CONST               '%c%02d%02d'
              383  LOAD_FAST            12  'sign'
              386  LOAD_FAST            13  'h'
              389  LOAD_FAST            14  'm'
              392  BUILD_TUPLE_3         3 
              395  BINARY_MODULO    
              396  STORE_FAST            4  'zreplace'
              399  JUMP_ABSOLUTE       405  'to 405'
              402  JUMP_ABSOLUTE       408  'to 408'
              405  JUMP_FORWARD          0  'to 408'
            408_0  COME_FROM           405  '405'

 L. 209       408  LOAD_CONST               '%'
              411  LOAD_FAST             4  'zreplace'
              414  COMPARE_OP            7  not-in
              417  POP_JUMP_IF_TRUE    426  'to 426'
              420  LOAD_ASSERT              AssertionError
              423  RAISE_VARARGS_1       1  None

 L. 210       426  LOAD_FAST             6  'newformat'
              429  LOAD_ATTR             1  'append'
              432  LOAD_FAST             4  'zreplace'
              435  CALL_FUNCTION_1       1  None
              438  POP_TOP          
              439  JUMP_ABSOLUTE       587  'to 587'

 L. 211       442  LOAD_FAST            10  'ch'
              445  LOAD_CONST               'Z'
              448  COMPARE_OP            2  ==
              451  POP_JUMP_IF_FALSE   554  'to 554'

 L. 212       454  LOAD_FAST             5  'Zreplace'
              457  LOAD_CONST               None
              460  COMPARE_OP            8  is
              463  POP_JUMP_IF_FALSE   538  'to 538'

 L. 213       466  LOAD_CONST               ''
              469  STORE_FAST            5  'Zreplace'

 L. 214       472  LOAD_GLOBAL           4  'hasattr'
              475  LOAD_FAST             0  'object'
              478  LOAD_CONST               'tzname'
              481  CALL_FUNCTION_2       2  None
              484  POP_JUMP_IF_FALSE   538  'to 538'

 L. 215       487  LOAD_FAST             0  'object'
              490  LOAD_ATTR            10  'tzname'
              493  CALL_FUNCTION_0       0  None
              496  STORE_FAST           15  's'

 L. 216       499  LOAD_FAST            15  's'
              502  LOAD_CONST               None
              505  COMPARE_OP            9  is-not
              508  POP_JUMP_IF_FALSE   535  'to 535'

 L. 218       511  LOAD_FAST            15  's'
              514  LOAD_ATTR            11  'replace'
              517  LOAD_CONST               '%'
              520  LOAD_CONST               '%%'
              523  CALL_FUNCTION_2       2  None
              526  STORE_FAST            5  'Zreplace'
              529  JUMP_ABSOLUTE       535  'to 535'
              532  JUMP_ABSOLUTE       538  'to 538'
              535  JUMP_FORWARD          0  'to 538'
            538_0  COME_FROM           535  '535'

 L. 219       538  LOAD_FAST             6  'newformat'
              541  LOAD_ATTR             1  'append'
              544  LOAD_FAST             5  'Zreplace'
              547  CALL_FUNCTION_1       1  None
              550  POP_TOP          
              551  JUMP_ABSOLUTE       587  'to 587'

 L. 221       554  LOAD_FAST             7  'push'
              557  LOAD_CONST               '%'
              560  CALL_FUNCTION_1       1  None
              563  POP_TOP          

 L. 222       564  LOAD_FAST             7  'push'
              567  LOAD_FAST            10  'ch'
              570  CALL_FUNCTION_1       1  None
              573  POP_TOP          
              574  JUMP_ABSOLUTE       600  'to 600'

 L. 224       577  LOAD_FAST             7  'push'
              580  LOAD_CONST               '%'
              583  CALL_FUNCTION_1       1  None
              586  POP_TOP          
              587  JUMP_BACK            55  'to 55'

 L. 226       590  LOAD_FAST             7  'push'
              593  LOAD_FAST            10  'ch'
              596  CALL_FUNCTION_1       1  None
              599  POP_TOP          
              600  JUMP_BACK            55  'to 55'
              603  POP_BLOCK        
            604_0  COME_FROM            52  '52'

 L. 227       604  LOAD_CONST               ''
              607  LOAD_ATTR            12  'join'
              610  LOAD_FAST             6  'newformat'
              613  CALL_FUNCTION_1       1  None
              616  STORE_FAST            6  'newformat'

 L. 228       619  LOAD_GLOBAL          13  '_time'
              622  LOAD_ATTR            14  'strftime'
              625  LOAD_FAST             6  'newformat'
              628  LOAD_FAST             2  'timetuple'
              631  CALL_FUNCTION_2       2  None
              634  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 603


def _call_tzinfo_method(tzinfo, methname, tzinfoarg):
    if tzinfo is None:
        return
    else:
        return getattr(tzinfo, methname)(tzinfoarg)


def _check_tzname(name):
    if name is not None and not isinstance(name, str):
        raise TypeError(b"tzinfo.tzname() must return None or string, not '%s'" % type(name))
    return


def _check_utc_offset(name, offset):
    assert name in ('utcoffset', 'dst')
    if offset is None:
        return
    else:
        if not isinstance(offset, timedelta):
            raise TypeError(b"tzinfo.%s() must return None or timedelta, not '%s'" % (
             name, type(offset)))
        if offset % timedelta(minutes=1) or offset.microseconds:
            raise ValueError(b'tzinfo.%s() must return a whole number of minutes, got %s' % (
             name, offset))
        if not -timedelta(1) < offset < timedelta(1):
            raise ValueError(b'%s()=%s, must be must be strictly between -timedelta(hours=24) and timedelta(hours=24)' % (
             name, offset))
        return


def _check_date_fields(year, month, day):
    if not isinstance(year, int):
        raise TypeError(b'int expected')
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError(b'year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not 1 <= month <= 12:
        raise ValueError(b'month must be in 1..12', month)
    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError(b'day must be in 1..%d' % dim, day)


def _check_time_fields(hour, minute, second, microsecond):
    if not isinstance(hour, int):
        raise TypeError(b'int expected')
    if not 0 <= hour <= 23:
        raise ValueError(b'hour must be in 0..23', hour)
    if not 0 <= minute <= 59:
        raise ValueError(b'minute must be in 0..59', minute)
    if not 0 <= second <= 59:
        raise ValueError(b'second must be in 0..59', second)
    if not 0 <= microsecond <= 999999:
        raise ValueError(b'microsecond must be in 0..999999', microsecond)


def _check_tzinfo_arg(tz):
    if tz is not None and not isinstance(tz, tzinfo):
        raise TypeError(b'tzinfo argument must be None or of a tzinfo subclass')
    return


def _cmperror(x, y):
    raise TypeError(b"can't compare '%s' to '%s'" % (
     type(x).__name__, type(y).__name__))


class timedelta(object):
    """Represent the difference between two datetime objects.

    Supported operators:

    - add, subtract timedelta
    - unary plus, minus, abs
    - compare to timedelta
    - multiply, divide by int

    In addition, datetime supports subtraction of two datetime objects
    returning a timedelta, and addition or subtraction of a datetime
    and a timedelta giving a datetime.

    Representation: (days, seconds, microseconds).  Why?  Because I
    felt like it.
    """
    __slots__ = ('_days', '_seconds', '_microseconds')

    def __new__(cls, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        if isinstance(days, float):
            dayfrac, days = _math.modf(days)
            daysecondsfrac, daysecondswhole = _math.modf(dayfrac * 86400.0)
            assert daysecondswhole == int(daysecondswhole)
            s = int(daysecondswhole)
            assert days == int(days)
            d = int(days)
        else:
            daysecondsfrac = 0.0
            d = days
        assert isinstance(daysecondsfrac, float)
        assert abs(daysecondsfrac) <= 1.0
        assert isinstance(d, int)
        assert abs(s) <= 86400
        if isinstance(seconds, float):
            secondsfrac, seconds = _math.modf(seconds)
            assert seconds == int(seconds)
            seconds = int(seconds)
            secondsfrac += daysecondsfrac
            assert abs(secondsfrac) <= 2.0
        else:
            secondsfrac = daysecondsfrac
        assert isinstance(secondsfrac, float)
        assert abs(secondsfrac) <= 2.0
        assert isinstance(seconds, int)
        days, seconds = divmod(seconds, 86400)
        d += days
        s += int(seconds)
        assert isinstance(s, int)
        assert abs(s) <= 172800
        usdouble = secondsfrac * 1000000.0
        assert abs(usdouble) < 2100000.0
        if isinstance(microseconds, float):
            microseconds += usdouble
            microseconds = round(microseconds, 0)
            seconds, microseconds = divmod(microseconds, 1000000.0)
            assert microseconds == int(microseconds)
            assert seconds == int(seconds)
            days, seconds = divmod(seconds, 86400.0)
            assert days == int(days)
            assert seconds == int(seconds)
            d += int(days)
            s += int(seconds)
            assert isinstance(s, int)
            assert abs(s) <= 259200
        else:
            seconds, microseconds = divmod(microseconds, 1000000)
            days, seconds = divmod(seconds, 86400)
            d += days
            s += int(seconds)
            assert isinstance(s, int)
            assert abs(s) <= 259200
            microseconds = float(microseconds)
            microseconds += usdouble
            microseconds = round(microseconds, 0)
        assert abs(s) <= 259200
        assert abs(microseconds) < 3100000.0
        assert isinstance(microseconds, float)
        assert int(microseconds) == microseconds
        us = int(microseconds)
        seconds, us = divmod(us, 1000000)
        s += seconds
        assert isinstance(s, int)
        days, s = divmod(s, 86400)
        d += days
        assert isinstance(d, int)
        assert isinstance(s, int) and 0 <= s < 86400
        assert isinstance(us, int) and 0 <= us < 1000000
        self = object.__new__(cls)
        self._days = d
        self._seconds = s
        self._microseconds = us
        if abs(d) > 999999999:
            raise OverflowError(b'timedelta # of days is too large: %d' % d)
        return self

    def __repr__(self):
        if self._microseconds:
            return b'%s(%d, %d, %d)' % (b'datetime.' + self.__class__.__name__,
             self._days,
             self._seconds,
             self._microseconds)
        if self._seconds:
            return b'%s(%d, %d)' % (b'datetime.' + self.__class__.__name__,
             self._days,
             self._seconds)
        return b'%s(%d)' % (b'datetime.' + self.__class__.__name__, self._days)

    def __str__(self):
        mm, ss = divmod(self._seconds, 60)
        hh, mm = divmod(mm, 60)
        s = b'%d:%02d:%02d' % (hh, mm, ss)
        if self._days:

            def plural(n):
                return (
                 n, abs(n) != 1 and b's' or b'')

            s = b'%d day%s, ' % plural(self._days) + s
        if self._microseconds:
            s = s + b'.%06d' % self._microseconds
        return s

    def total_seconds(self):
        """Total seconds in the duration."""
        return ((self.days * 86400 + self.seconds) * 1000000 + self.microseconds) / 1000000

    @property
    def days(self):
        """days"""
        return self._days

    @property
    def seconds(self):
        """seconds"""
        return self._seconds

    @property
    def microseconds(self):
        """microseconds"""
        return self._microseconds

    def __add__(self, other):
        if isinstance(other, timedelta):
            return timedelta(self._days + other._days, self._seconds + other._seconds, self._microseconds + other._microseconds)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return timedelta(self._days - other._days, self._seconds - other._seconds, self._microseconds - other._microseconds)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, timedelta):
            return -self + other
        return NotImplemented

    def __neg__(self):
        return timedelta(-self._days, -self._seconds, -self._microseconds)

    def __pos__(self):
        return self

    def __abs__(self):
        if self._days < 0:
            return -self
        else:
            return self

    def __mul__(self, other):
        if isinstance(other, int):
            return timedelta(self._days * other, self._seconds * other, self._microseconds * other)
        if isinstance(other, float):
            a, b = other.as_integer_ratio()
            return self * a / b
        return NotImplemented

    __rmul__ = __mul__

    def _to_microseconds(self):
        return (self._days * 86400 + self._seconds) * 1000000 + self._microseconds

    def __floordiv__(self, other):
        if not isinstance(other, (int, timedelta)):
            return NotImplemented
        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec // other._to_microseconds()
        if isinstance(other, int):
            return timedelta(0, 0, usec // other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float, timedelta)):
            return NotImplemented
        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec / other._to_microseconds()
        if isinstance(other, int):
            return timedelta(0, 0, usec / other)
        if isinstance(other, float):
            a, b = other.as_integer_ratio()
            return timedelta(0, 0, b * usec / a)

    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = self._to_microseconds() % other._to_microseconds()
            return timedelta(0, 0, r)
        return NotImplemented

    def __divmod__(self, other):
        if isinstance(other, timedelta):
            q, r = divmod(self._to_microseconds(), other._to_microseconds())
            return (
             q, timedelta(0, 0, r))
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) == 0
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) != 0
        else:
            return True

    def __le__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) <= 0
        _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) < 0
        _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) >= 0
        _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) > 0
        _cmperror(self, other)

    def _cmp(self, other):
        assert isinstance(other, timedelta)
        return _cmp(self._getstate(), other._getstate())

    def __hash__(self):
        return hash(self._getstate())

    def __bool__(self):
        return self._days != 0 or self._seconds != 0 or self._microseconds != 0

    def _getstate(self):
        return (
         self._days, self._seconds, self._microseconds)

    def __reduce__(self):
        return (
         self.__class__, self._getstate())


timedelta.min = timedelta(-999999999)
timedelta.max = timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)
timedelta.resolution = timedelta(microseconds=1)

class date(object):
    """Concrete date type.

    Constructors:

    __new__()
    fromtimestamp()
    today()
    fromordinal()

    Operators:

    __repr__, __str__
    __cmp__, __hash__
    __add__, __radd__, __sub__ (add/radd only with timedelta arg)

    Methods:

    timetuple()
    toordinal()
    weekday()
    isoweekday(), isocalendar(), isoformat()
    ctime()
    strftime()

    Properties (readonly):
    year, month, day
    """
    __slots__ = ('_year', '_month', '_day')

    def __new__(cls, year, month=None, day=None):
        """Constructor.

        Arguments:

        year, month, day (required, base 1)
        """
        if isinstance(year, bytes) and len(year) == 4 and 1 <= year[2] <= 12 and month is None:
            self = object.__new__(cls)
            self.__setstate(year)
            return self
        else:
            _check_date_fields(year, month, day)
            self = object.__new__(cls)
            self._year = year
            self._month = month
            self._day = day
            return self

    @classmethod
    def fromtimestamp(cls, t):
        """Construct a date from a POSIX timestamp (like time.time())."""
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.localtime(t)
        return cls(y, m, d)

    @classmethod
    def today(cls):
        """Construct a date from time.time()."""
        t = _time.time()
        return cls.fromtimestamp(t)

    @classmethod
    def fromordinal(cls, n):
        """Contruct a date from a proleptic Gregorian ordinal.

        January 1 of year 1 is day 1.  Only the year, month and day are
        non-zero in the result.
        """
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> dt = datetime(2010, 1, 1)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0)'

        >>> dt = datetime(2010, 1, 1, tzinfo=timezone.utc)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)'
        """
        return b'%s(%d, %d, %d)' % (b'datetime.' + self.__class__.__name__,
         self._year,
         self._month,
         self._day)

    def ctime(self):
        """Return ctime() style string."""
        weekday = self.toordinal() % 7 or 7
        return b'%s %s %2d 00:00:00 %04d' % (
         _DAYNAMES[weekday],
         _MONTHNAMES[self._month],
         self._day, self._year)

    def strftime(self, fmt):
        """Format using strftime()."""
        return _wrap_strftime(self, fmt, self.timetuple())

    def __format__(self, fmt):
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD'.

        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        return b'%04d-%02d-%02d' % (self._year, self._month, self._day)

    __str__ = isoformat

    @property
    def year(self):
        """year (1-9999)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month

    @property
    def day(self):
        """day (1-31)"""
        return self._day

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        return _build_struct_time(self._year, self._month, self._day, 0, 0, 0, -1)

    def toordinal(self):
        """Return proleptic Gregorian ordinal for the year, month and day.

        January 1 of year 1 is day 1.  Only the year, month and day values
        contribute to the result.
        """
        return _ymd2ord(self._year, self._month, self._day)

    def replace(self, year=None, month=None, day=None):
        """Return a new date with new values for the specified fields."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        _check_date_fields(year, month, day)
        return date(year, month, day)

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, date):
            return self._cmp(other) != 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, date)
        y, m, d = self._year, self._month, self._day
        y2, m2, d2 = other._year, other._month, other._day
        return _cmp((y, m, d), (y2, m2, d2))

    def __hash__(self):
        """Hash."""
        return hash(self._getstate())

    def __add__(self, other):
        """Add a date to a timedelta."""
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days
            if 0 < o <= _MAXORDINAL:
                return date.fromordinal(o)
            raise OverflowError(b'result out of range')
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two dates, or a date and a timedelta."""
        if isinstance(other, timedelta):
            return self + timedelta(-other.days)
        if isinstance(other, date):
            days1 = self.toordinal()
            days2 = other.toordinal()
            return timedelta(days1 - days2)
        return NotImplemented

    def weekday(self):
        """Return day of the week, where Monday == 0 ... Sunday == 6."""
        return (self.toordinal() + 6) % 7

    def isoweekday(self):
        """Return day of the week, where Monday == 1 ... Sunday == 7."""
        return self.toordinal() % 7 or 7

    def isocalendar(self):
        """Return a 3-tuple containing ISO year, week number, and weekday.

        The first ISO week of the year is the (Mon-Sun) week
        containing the year's first Thursday; everything else derives
        from that.

        The first week is 1; Monday is 1 ... Sunday is 7.

        ISO calendar algorithm taken from
        http://www.phys.uu.nl/~vgent/calendar/isocalendar.htm
        """
        year = self._year
        week1monday = _isoweek1monday(year)
        today = _ymd2ord(self._year, self._month, self._day)
        week, day = divmod(today - week1monday, 7)
        if week < 0:
            year -= 1
            week1monday = _isoweek1monday(year)
            week, day = divmod(today - week1monday, 7)
        elif week >= 52:
            if today >= _isoweek1monday(year + 1):
                year += 1
                week = 0
        return (
         year, week + 1, day + 1)

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        return (bytes([yhi, ylo, self._month, self._day]),)

    def __setstate(self, string):
        if len(string) != 4 or not 1 <= string[2] <= 12:
            raise TypeError(b'not enough arguments')
        yhi, ylo, self._month, self._day = string
        self._year = yhi * 256 + ylo

    def __reduce__(self):
        return (
         self.__class__, self._getstate())


_date_class = date
date.min = date(1, 1, 1)
date.max = date(9999, 12, 31)
date.resolution = timedelta(days=1)

class tzinfo(object):
    """Abstract base class for time zone info classes.

    Subclasses must override the name(), utcoffset() and dst() methods.
    """
    __slots__ = ()

    def tzname(self, dt):
        """datetime -> string name of time zone."""
        raise NotImplementedError(b'tzinfo subclass must override tzname()')

    def utcoffset(self, dt):
        """datetime -> minutes east of UTC (negative for west of UTC)"""
        raise NotImplementedError(b'tzinfo subclass must override utcoffset()')

    def dst(self, dt):
        """datetime -> DST offset in minutes east of UTC.

        Return 0 if DST not in effect.  utcoffset() must include the DST
        offset.
        """
        raise NotImplementedError(b'tzinfo subclass must override dst()')

    def fromutc(self, dt):
        """datetime in UTC -> datetime in local time."""
        if not isinstance(dt, datetime):
            raise TypeError(b'fromutc() requires a datetime argument')
        if dt.tzinfo is not self:
            raise ValueError(b'dt.tzinfo is not self')
        dtoff = dt.utcoffset()
        if dtoff is None:
            raise ValueError(b'fromutc() requires a non-None utcoffset() result')
        dtdst = dt.dst()
        if dtdst is None:
            raise ValueError(b'fromutc() requires a non-None dst() result')
        delta = dtoff - dtdst
        if delta:
            dt += delta
            dtdst = dt.dst()
            if dtdst is None:
                raise ValueError(b'fromutc(): dt.dst gave inconsistent results; cannot convert')
        return dt + dtdst

    def __reduce__(self):
        getinitargs = getattr(self, b'__getinitargs__', None)
        if getinitargs:
            args = getinitargs()
        else:
            args = ()
        getstate = getattr(self, b'__getstate__', None)
        if getstate:
            state = getstate()
        else:
            state = getattr(self, b'__dict__', None) or None
        if state is None:
            return (self.__class__, args)
        else:
            return (
             self.__class__, args, state)
            return


_tzinfo_class = tzinfo

class time(object):
    """Time with time zone.

    Constructors:

    __new__()

    Operators:

    __repr__, __str__
    __cmp__, __hash__

    Methods:

    strftime()
    isoformat()
    utcoffset()
    tzname()
    dst()

    Properties (readonly):
    hour, minute, second, microsecond, tzinfo
    """

    def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        """Constructor.

        Arguments:

        hour, minute (required)
        second, microsecond (default to zero)
        tzinfo (default to None)
        """
        self = object.__new__(cls)
        if isinstance(hour, bytes) and len(hour) == 6:
            self.__setstate(hour, minute or None)
            return self
        else:
            _check_tzinfo_arg(tzinfo)
            _check_time_fields(hour, minute, second, microsecond)
            self._hour = hour
            self._minute = minute
            self._second = second
            self._microsecond = microsecond
            self._tzinfo = tzinfo
            return self

    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    @property
    def tzinfo(self):
        """timezone info object"""
        return self._tzinfo

    def __eq__(self, other):
        if isinstance(other, time):
            return self._cmp(other, allow_mixed=True) == 0
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, time):
            return self._cmp(other, allow_mixed=True) != 0
        else:
            return True

    def __le__(self, other):
        if isinstance(other, time):
            return self._cmp(other) <= 0
        _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, time):
            return self._cmp(other) < 0
        _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, time):
            return self._cmp(other) >= 0
        _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, time):
            return self._cmp(other) > 0
        _cmperror(self, other)

    def _cmp(self, other, allow_mixed=False):
        assert isinstance(other, time)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = otoff = None
        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff
        if base_compare:
            return _cmp((self._hour, self._minute, self._second,
             self._microsecond), (
             other._hour, other._minute, other._second,
             other._microsecond))
        else:
            if myoff is None or otoff is None:
                if allow_mixed:
                    return 2
                raise TypeError(b'cannot compare naive and aware times')
            myhhmm = self._hour * 60 + self._minute - myoff // timedelta(minutes=1)
            othhmm = other._hour * 60 + other._minute - otoff // timedelta(minutes=1)
            return _cmp((myhhmm, self._second, self._microsecond), (
             othhmm, other._second, other._microsecond))

    def __hash__--- This code section failed: ---

 L.1131         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'utcoffset'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            1  'tzoff'

 L.1132        12  LOAD_FAST             1  'tzoff'
               15  POP_JUMP_IF_TRUE     38  'to 38'

 L.1133        18  LOAD_GLOBAL           1  'hash'
               21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             2  '_getstate'
               27  CALL_FUNCTION_0       0  None
               30  LOAD_CONST               0
               33  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  None
               37  RETURN_END_IF    
             38_0  COME_FROM            15  '15'

 L.1134        38  LOAD_GLOBAL           3  'divmod'
               41  LOAD_GLOBAL           4  'timedelta'
               44  LOAD_CONST               'hours'
               47  LOAD_FAST             0  'self'
               50  LOAD_ATTR             5  'hour'
               53  LOAD_CONST               'minutes'
               56  LOAD_FAST             0  'self'
               59  LOAD_ATTR             6  'minute'
               62  CALL_FUNCTION_512   512  None
               65  LOAD_FAST             1  'tzoff'
               68  BINARY_SUBTRACT  

 L.1135        69  LOAD_GLOBAL           4  'timedelta'
               72  LOAD_CONST               'hours'
               75  LOAD_CONST               1
               78  CALL_FUNCTION_256   256  None
               81  CALL_FUNCTION_2       2  None
               84  UNPACK_SEQUENCE_2     2 
               87  STORE_FAST            2  'h'
               90  STORE_FAST            3  'm'

 L.1136        93  LOAD_FAST             3  'm'
               96  LOAD_GLOBAL           4  'timedelta'
               99  LOAD_CONST               'minutes'
              102  LOAD_CONST               1
              105  CALL_FUNCTION_256   256  None
              108  BINARY_MODULO    
              109  UNARY_NOT        
              110  POP_JUMP_IF_TRUE    122  'to 122'
              113  LOAD_ASSERT              AssertionError
              116  LOAD_CONST               'whole minute'
              119  RAISE_VARARGS_2       2  None

 L.1137       122  LOAD_FAST             3  'm'
              125  LOAD_GLOBAL           4  'timedelta'
              128  LOAD_CONST               'minutes'
              131  LOAD_CONST               1
              134  CALL_FUNCTION_256   256  None
              137  INPLACE_FLOOR_DIVIDE
              138  STORE_FAST            3  'm'

 L.1138       141  LOAD_CONST               0
              144  LOAD_FAST             2  'h'
              147  DUP_TOP          
              148  ROT_THREE        
              149  COMPARE_OP            1  <=
              152  JUMP_IF_FALSE_OR_POP   164  'to 164'
              155  LOAD_CONST               24
              158  COMPARE_OP            0  <
              161  JUMP_FORWARD          2  'to 166'
            164_0  COME_FROM           152  '152'
              164  ROT_TWO          
              165  POP_TOP          
            166_0  COME_FROM           161  '161'
              166  POP_JUMP_IF_FALSE   200  'to 200'

 L.1139       169  LOAD_GLOBAL           1  'hash'
              172  LOAD_GLOBAL           8  'time'
              175  LOAD_FAST             2  'h'
              178  LOAD_FAST             3  'm'
              181  LOAD_FAST             0  'self'
              184  LOAD_ATTR             9  'second'
              187  LOAD_FAST             0  'self'
              190  LOAD_ATTR            10  'microsecond'
              193  CALL_FUNCTION_4       4  None
              196  CALL_FUNCTION_1       1  None
              199  RETURN_END_IF    
            200_0  COME_FROM           166  '166'

 L.1140       200  LOAD_GLOBAL           1  'hash'
              203  LOAD_FAST             2  'h'
              206  LOAD_FAST             3  'm'
              209  LOAD_FAST             0  'self'
              212  LOAD_ATTR             9  'second'
              215  LOAD_FAST             0  'self'
              218  LOAD_ATTR            10  'microsecond'
              221  BUILD_TUPLE_4         4 
              224  CALL_FUNCTION_1       1  None
              227  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 227

    def _tzstr--- This code section failed: ---

 L.1146         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'utcoffset'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            2  'off'

 L.1147        12  LOAD_FAST             2  'off'
               15  LOAD_CONST               None
               18  COMPARE_OP            9  is-not
               21  POP_JUMP_IF_FALSE   198  'to 198'

 L.1148        24  LOAD_FAST             2  'off'
               27  LOAD_ATTR             2  'days'
               30  LOAD_CONST               0
               33  COMPARE_OP            0  <
               36  POP_JUMP_IF_FALSE    55  'to 55'

 L.1149        39  LOAD_CONST               '-'
               42  STORE_FAST            3  'sign'

 L.1150        45  LOAD_FAST             2  'off'
               48  UNARY_NEGATIVE   
               49  STORE_FAST            2  'off'
               52  JUMP_FORWARD          6  'to 61'

 L.1152        55  LOAD_CONST               '+'
               58  STORE_FAST            3  'sign'
             61_0  COME_FROM            52  '52'

 L.1153        61  LOAD_GLOBAL           3  'divmod'
               64  LOAD_FAST             2  'off'
               67  LOAD_GLOBAL           4  'timedelta'
               70  LOAD_CONST               'hours'
               73  LOAD_CONST               1
               76  CALL_FUNCTION_256   256  None
               79  CALL_FUNCTION_2       2  None
               82  UNPACK_SEQUENCE_2     2 
               85  STORE_FAST            4  'hh'
               88  STORE_FAST            5  'mm'

 L.1154        91  LOAD_FAST             5  'mm'
               94  LOAD_GLOBAL           4  'timedelta'
               97  LOAD_CONST               'minutes'
              100  LOAD_CONST               1
              103  CALL_FUNCTION_256   256  None
              106  BINARY_MODULO    
              107  UNARY_NOT        
              108  POP_JUMP_IF_TRUE    120  'to 120'
              111  LOAD_ASSERT              AssertionError
              114  LOAD_CONST               'whole minute'
              117  RAISE_VARARGS_2       2  None

 L.1155       120  LOAD_FAST             5  'mm'
              123  LOAD_GLOBAL           4  'timedelta'
              126  LOAD_CONST               'minutes'
              129  LOAD_CONST               1
              132  CALL_FUNCTION_256   256  None
              135  INPLACE_FLOOR_DIVIDE
              136  STORE_FAST            5  'mm'

 L.1156       139  LOAD_CONST               0
              142  LOAD_FAST             4  'hh'
              145  DUP_TOP          
              146  ROT_THREE        
              147  COMPARE_OP            1  <=
              150  JUMP_IF_FALSE_OR_POP   162  'to 162'
              153  LOAD_CONST               24
              156  COMPARE_OP            0  <
              159  JUMP_FORWARD          2  'to 164'
            162_0  COME_FROM           150  '150'
              162  ROT_TWO          
              163  POP_TOP          
            164_0  COME_FROM           159  '159'
              164  POP_JUMP_IF_TRUE    173  'to 173'
              167  LOAD_ASSERT              AssertionError
              170  RAISE_VARARGS_1       1  None

 L.1157       173  LOAD_CONST               '%s%02d%s%02d'
              176  LOAD_FAST             3  'sign'
              179  LOAD_FAST             4  'hh'
              182  LOAD_FAST             1  'sep'
              185  LOAD_FAST             5  'mm'
              188  BUILD_TUPLE_4         4 
              191  BINARY_MODULO    
              192  STORE_FAST            2  'off'
              195  JUMP_FORWARD          0  'to 198'
            198_0  COME_FROM           195  '195'

 L.1158       198  LOAD_FAST             2  'off'
              201  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 198

    def __repr__(self):
        """Convert to formal string, for repr()."""
        if self._microsecond != 0:
            s = b', %d, %d' % (self._second, self._microsecond)
        elif self._second != 0:
            s = b', %d' % self._second
        else:
            s = b''
        s = b'%s(%d, %d%s)' % (b'datetime.' + self.__class__.__name__,
         self._hour, self._minute, s)
        if self._tzinfo is not None:
            assert s[-1:] == b')'
            s = s[:-1] + b', tzinfo=%r' % self._tzinfo + b')'
        return s

    def isoformat(self):
        """Return the time formatted according to ISO.

        This is 'HH:MM:SS.mmmmmm+zz:zz', or 'HH:MM:SS+zz:zz' if
        self.microsecond == 0.
        """
        s = _format_time(self._hour, self._minute, self._second, self._microsecond)
        tz = self._tzstr()
        if tz:
            s += tz
        return s

    __str__ = isoformat

    def strftime(self, fmt):
        """Format using strftime().  The date part of the timestamp passed
        to underlying strftime should not be used.
        """
        timetuple = (
         1900, 1, 1,
         self._hour, self._minute, self._second,
         0, 1, -1)
        return _wrap_strftime(self, fmt, timetuple)

    def __format__(self, fmt):
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def utcoffset(self):
        """Return the timezone offset in minutes east of UTC (negative west of
        UTC)."""
        if self._tzinfo is None:
            return
        else:
            offset = self._tzinfo.utcoffset(None)
            _check_utc_offset(b'utcoffset', offset)
            return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        if self._tzinfo is None:
            return
        else:
            name = self._tzinfo.tzname(None)
            _check_tzname(name)
            return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (in minutes
        eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return
        else:
            offset = self._tzinfo.dst(None)
            _check_utc_offset(b'dst', offset)
            return offset

    def replace(self, hour=None, minute=None, second=None, microsecond=None, tzinfo=True):
        """Return a new time with new values for the specified fields."""
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        _check_time_fields(hour, minute, second, microsecond)
        _check_tzinfo_arg(tzinfo)
        return time(hour, minute, second, microsecond, tzinfo)

    def __bool__(self):
        if self.second or self.microsecond:
            return True
        offset = self.utcoffset() or timedelta(0)
        return timedelta(hours=self.hour, minutes=self.minute) != offset

    def _getstate(self):
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        basestate = bytes([self._hour, self._minute, self._second,
         us1, us2, us3])
        if self._tzinfo is None:
            return (basestate,)
        else:
            return (
             basestate, self._tzinfo)
            return

    def __setstate(self, string, tzinfo):
        if len(string) != 6 or string[0] >= 24:
            raise TypeError(b'an integer is required')
        self._hour, self._minute, self._second, us1, us2, us3 = string
        self._microsecond = (us1 << 8 | us2) << 8 | us3
        if tzinfo is None or isinstance(tzinfo, _tzinfo_class):
            self._tzinfo = tzinfo
        else:
            raise TypeError(b'bad tzinfo state arg %r' % tzinfo)
        return

    def __reduce__(self):
        return (
         time, self._getstate())


_time_class = time
time.min = time(0, 0, 0)
time.max = time(23, 59, 59, 999999)
time.resolution = timedelta(microseconds=1)

class datetime(date):
    """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

    The year, month and day arguments are required. tzinfo may be None, or an
    instance of a tzinfo subclass. The remaining arguments may be ints.
    """
    __slots__ = date.__slots__ + ('_hour', '_minute', '_second', '_microsecond', '_tzinfo')

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        if isinstance(year, bytes) and len(year) == 10:
            self = date.__new__(cls, year[:4])
            self.__setstate(year, month)
            return self
        _check_tzinfo_arg(tzinfo)
        _check_time_fields(hour, minute, second, microsecond)
        self = date.__new__(cls, year, month, day)
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        return self

    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    @property
    def tzinfo(self):
        """timezone info object"""
        return self._tzinfo

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        _check_tzinfo_arg(tz)
        converter = _time.localtime if tz is None else _time.gmtime
        t, frac = divmod(t, 1.0)
        us = int(frac * 1000000.0)
        if us == 1000000:
            t += 1
            us = 0
        y, m, d, hh, mm, ss, weekday, jday, dst = converter(t)
        ss = min(ss, 59)
        result = cls(y, m, d, hh, mm, ss, us, tz)
        if tz is not None:
            result = tz.fromutc(result)
        return result

    @classmethod
    def utcfromtimestamp(cls, t):
        """Construct a UTC datetime from a POSIX timestamp (like time.time())."""
        t, frac = divmod(t, 1.0)
        us = int(frac * 1000000.0)
        if us == 1000000:
            t += 1
            us = 0
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(t)
        ss = min(ss, 59)
        return cls(y, m, d, hh, mm, ss, us)

    @classmethod
    def now(cls, tz=None):
        """Construct a datetime from time.time() and optional time zone info."""
        t = _time.time()
        return cls.fromtimestamp(t, tz)

    @classmethod
    def utcnow(cls):
        """Construct a UTC datetime from time.time()."""
        t = _time.time()
        return cls.utcfromtimestamp(t)

    @classmethod
    def combine(cls, date, time):
        """Construct a datetime from a given date and a given time."""
        if not isinstance(date, _date_class):
            raise TypeError(b'date argument must be a date instance')
        if not isinstance(time, _time_class):
            raise TypeError(b'time argument must be a time instance')
        return cls(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond, time.tzinfo)

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        dst = self.dst()
        if dst is None:
            dst = -1
        elif dst:
            dst = 1
        else:
            dst = 0
        return _build_struct_time(self.year, self.month, self.day, self.hour, self.minute, self.second, dst)

    def timestamp(self):
        """Return POSIX timestamp as float"""
        if self._tzinfo is None:
            return _time.mktime((self.year, self.month, self.day,
             self.hour, self.minute, self.second,
             -1, -1, -1)) + self.microsecond / 1000000.0
        else:
            return (self - _EPOCH).total_seconds()
            return

    def utctimetuple(self):
        """Return UTC time tuple compatible with time.gmtime()."""
        offset = self.utcoffset()
        if offset:
            self -= offset
        y, m, d = self.year, self.month, self.day
        hh, mm, ss = self.hour, self.minute, self.second
        return _build_struct_time(y, m, d, hh, mm, ss, 0)

    def date(self):
        """Return the date part."""
        return date(self._year, self._month, self._day)

    def time(self):
        """Return the time part, with tzinfo None."""
        return time(self.hour, self.minute, self.second, self.microsecond)

    def timetz(self):
        """Return the time part, with same tzinfo."""
        return time(self.hour, self.minute, self.second, self.microsecond, self._tzinfo)

    def replace(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, tzinfo=True):
        """Return a new datetime with new values for the specified fields."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        _check_date_fields(year, month, day)
        _check_time_fields(hour, minute, second, microsecond)
        _check_tzinfo_arg(tzinfo)
        return datetime(year, month, day, hour, minute, second, microsecond, tzinfo)

    def astimezone(self, tz=None):
        if tz is None:
            if self.tzinfo is None:
                raise ValueError(b'astimezone() requires an aware datetime')
            ts = (self - _EPOCH) // timedelta(seconds=1)
            localtm = _time.localtime(ts)
            local = datetime(*localtm[:6])
            try:
                gmtoff = localtm.tm_gmtoff
                zone = localtm.tm_zone
            except AttributeError:
                delta = local - datetime(*_time.gmtime(ts)[:6])
                dst = _time.daylight and localtm.tm_isdst > 0
                gmtoff = -(_time.altzone if dst else _time.timezone)
                if delta == timedelta(seconds=gmtoff):
                    tz = timezone(delta, _time.tzname[dst])
                else:
                    tz = timezone(delta)
            else:
                tz = timezone(timedelta(seconds=gmtoff), zone)

        elif not isinstance(tz, tzinfo):
            raise TypeError(b'tz argument must be an instance of tzinfo')
        mytz = self.tzinfo
        if mytz is None:
            raise ValueError(b'astimezone() requires an aware datetime')
        if tz is mytz:
            return self
        else:
            myoffset = self.utcoffset()
            if myoffset is None:
                raise ValueError(b'astimezone() requires an aware datetime')
            utc = (self - myoffset).replace(tzinfo=tz)
            return tz.fromutc(utc)

    def ctime(self):
        """Return ctime() style string."""
        weekday = self.toordinal() % 7 or 7
        return b'%s %s %2d %02d:%02d:%02d %04d' % (
         _DAYNAMES[weekday],
         _MONTHNAMES[self._month],
         self._day,
         self._hour, self._minute, self._second,
         self._year)

    def isoformat--- This code section failed: ---

 L.1563         0  LOAD_CONST               '%04d-%02d-%02d%c'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             0  '_year'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             1  '_month'
               15  LOAD_FAST             0  'self'
               18  LOAD_ATTR             2  '_day'

 L.1564        21  LOAD_FAST             1  'sep'
               24  BUILD_TUPLE_4         4 
               27  BINARY_MODULO    

 L.1565        28  LOAD_GLOBAL           3  '_format_time'
               31  LOAD_FAST             0  'self'
               34  LOAD_ATTR             4  '_hour'
               37  LOAD_FAST             0  'self'
               40  LOAD_ATTR             5  '_minute'
               43  LOAD_FAST             0  'self'
               46  LOAD_ATTR             6  '_second'

 L.1566        49  LOAD_FAST             0  'self'
               52  LOAD_ATTR             7  '_microsecond'
               55  CALL_FUNCTION_4       4  None
               58  BINARY_ADD       
               59  STORE_FAST            2  's'

 L.1567        62  LOAD_FAST             0  'self'
               65  LOAD_ATTR             8  'utcoffset'
               68  CALL_FUNCTION_0       0  None
               71  STORE_FAST            3  'off'

 L.1568        74  LOAD_FAST             3  'off'
               77  LOAD_CONST               None
               80  COMPARE_OP            9  is-not
               83  POP_JUMP_IF_FALSE   227  'to 227'

 L.1569        86  LOAD_FAST             3  'off'
               89  LOAD_ATTR            10  'days'
               92  LOAD_CONST               0
               95  COMPARE_OP            0  <
               98  POP_JUMP_IF_FALSE   117  'to 117'

 L.1570       101  LOAD_CONST               '-'
              104  STORE_FAST            4  'sign'

 L.1571       107  LOAD_FAST             3  'off'
              110  UNARY_NEGATIVE   
              111  STORE_FAST            3  'off'
              114  JUMP_FORWARD          6  'to 123'

 L.1573       117  LOAD_CONST               '+'
              120  STORE_FAST            4  'sign'
            123_0  COME_FROM           114  '114'

 L.1574       123  LOAD_GLOBAL          11  'divmod'
              126  LOAD_FAST             3  'off'
              129  LOAD_GLOBAL          12  'timedelta'
              132  LOAD_CONST               'hours'
              135  LOAD_CONST               1
              138  CALL_FUNCTION_256   256  None
              141  CALL_FUNCTION_2       2  None
              144  UNPACK_SEQUENCE_2     2 
              147  STORE_FAST            5  'hh'
              150  STORE_FAST            6  'mm'

 L.1575       153  LOAD_FAST             6  'mm'
              156  LOAD_GLOBAL          12  'timedelta'
              159  LOAD_CONST               'minutes'
              162  LOAD_CONST               1
              165  CALL_FUNCTION_256   256  None
              168  BINARY_MODULO    
              169  UNARY_NOT        
              170  POP_JUMP_IF_TRUE    182  'to 182'
              173  LOAD_ASSERT              AssertionError
              176  LOAD_CONST               'whole minute'
              179  RAISE_VARARGS_2       2  None

 L.1576       182  LOAD_FAST             6  'mm'
              185  LOAD_GLOBAL          12  'timedelta'
              188  LOAD_CONST               'minutes'
              191  LOAD_CONST               1
              194  CALL_FUNCTION_256   256  None
              197  INPLACE_FLOOR_DIVIDE
              198  STORE_FAST            6  'mm'

 L.1577       201  LOAD_FAST             2  's'
              204  LOAD_CONST               '%s%02d:%02d'
              207  LOAD_FAST             4  'sign'
              210  LOAD_FAST             5  'hh'
              213  LOAD_FAST             6  'mm'
              216  BUILD_TUPLE_3         3 
              219  BINARY_MODULO    
              220  INPLACE_ADD      
              221  STORE_FAST            2  's'
              224  JUMP_FORWARD          0  'to 227'
            227_0  COME_FROM           224  '224'

 L.1578       227  LOAD_FAST             2  's'
              230  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 227

    def __repr__(self):
        """Convert to formal string, for repr()."""
        L = [
         self._year, self._month, self._day,
         self._hour, self._minute, self._second, self._microsecond]
        if L[(-1)] == 0:
            del L[-1]
        if L[(-1)] == 0:
            del L[-1]
        s = (b', ').join(map(str, L))
        s = b'%s(%s)' % (b'datetime.' + self.__class__.__name__, s)
        if self._tzinfo is not None:
            assert s[-1:] == b')'
            s = s[:-1] + b', tzinfo=%r' % self._tzinfo + b')'
        return s

    def __str__(self):
        """Convert to string, for str()."""
        return self.isoformat(sep=b' ')

    @classmethod
    def strptime(cls, date_string, format):
        """string, format -> new datetime parsed from a string (like time.strptime())."""
        import _strptime
        return _strptime._strptime_datetime(cls, date_string, format)

    def utcoffset(self):
        """Return the timezone offset in minutes east of UTC (negative west of
        UTC)."""
        if self._tzinfo is None:
            return
        else:
            offset = self._tzinfo.utcoffset(self)
            _check_utc_offset(b'utcoffset', offset)
            return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        name = _call_tzinfo_method(self._tzinfo, b'tzname', self)
        _check_tzname(name)
        return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (in minutes
        eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return
        else:
            offset = self._tzinfo.dst(self)
            _check_utc_offset(b'dst', offset)
            return offset

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other, allow_mixed=True) == 0
        else:
            if not isinstance(other, date):
                return NotImplemented
            return False

    def __ne__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other, allow_mixed=True) != 0
        else:
            if not isinstance(other, date):
                return NotImplemented
            return True

    def __le__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) <= 0
        if not isinstance(other, date):
            return NotImplemented
        _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) < 0
        if not isinstance(other, date):
            return NotImplemented
        _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) >= 0
        if not isinstance(other, date):
            return NotImplemented
        _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) > 0
        if not isinstance(other, date):
            return NotImplemented
        _cmperror(self, other)

    def _cmp(self, other, allow_mixed=False):
        assert isinstance(other, datetime)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = otoff = None
        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff
        if base_compare:
            return _cmp((self._year, self._month, self._day,
             self._hour, self._minute, self._second,
             self._microsecond), (
             other._year, other._month, other._day,
             other._hour, other._minute, other._second,
             other._microsecond))
        else:
            if myoff is None or otoff is None:
                if allow_mixed:
                    return 2
                raise TypeError(b'cannot compare naive and aware datetimes')
            diff = self - other
            if diff.days < 0:
                return -1
            return diff and 1 or 0

    def __add__(self, other):
        """Add a datetime and a timedelta."""
        if not isinstance(other, timedelta):
            return NotImplemented
        delta = timedelta(self.toordinal(), hours=self._hour, minutes=self._minute, seconds=self._second, microseconds=self._microsecond)
        delta += other
        hour, rem = divmod(delta.seconds, 3600)
        minute, second = divmod(rem, 60)
        if 0 < delta.days <= _MAXORDINAL:
            return datetime.combine(date.fromordinal(delta.days), time(hour, minute, second, delta.microseconds, tzinfo=self._tzinfo))
        raise OverflowError(b'result out of range')

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two datetimes, or a datetime and a timedelta."""
        if not isinstance(other, datetime):
            if isinstance(other, timedelta):
                return self + -other
            return NotImplemented
        days1 = self.toordinal()
        days2 = other.toordinal()
        secs1 = self._second + self._minute * 60 + self._hour * 3600
        secs2 = other._second + other._minute * 60 + other._hour * 3600
        base = timedelta(days1 - days2, secs1 - secs2, self._microsecond - other._microsecond)
        if self._tzinfo is other._tzinfo:
            return base
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            if myoff == otoff:
                return base
            if myoff is None or otoff is None:
                raise TypeError(b'cannot mix naive and timezone-aware time')
            return base + otoff - myoff

    def __hash__(self):
        tzoff = self.utcoffset()
        if tzoff is None:
            return hash(self._getstate()[0])
        else:
            days = _ymd2ord(self.year, self.month, self.day)
            seconds = self.hour * 3600 + self.minute * 60 + self.second
            return hash(timedelta(days, seconds, self.microsecond) - tzoff)

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        basestate = bytes([yhi, ylo, self._month, self._day,
         self._hour, self._minute, self._second,
         us1, us2, us3])
        if self._tzinfo is None:
            return (basestate,)
        else:
            return (
             basestate, self._tzinfo)
            return

    def __setstate(self, string, tzinfo):
        yhi, ylo, self._month, self._day, self._hour, self._minute, self._second, us1, us2, us3 = string
        self._year = yhi * 256 + ylo
        self._microsecond = (us1 << 8 | us2) << 8 | us3
        if tzinfo is None or isinstance(tzinfo, _tzinfo_class):
            self._tzinfo = tzinfo
        else:
            raise TypeError(b'bad tzinfo state arg %r' % tzinfo)
        return

    def __reduce__(self):
        return (
         self.__class__, self._getstate())


datetime.min = datetime(1, 1, 1)
datetime.max = datetime(9999, 12, 31, 23, 59, 59, 999999)
datetime.resolution = timedelta(microseconds=1)

def _isoweek1monday(year):
    THURSDAY = 3
    firstday = _ymd2ord(year, 1, 1)
    firstweekday = (firstday + 6) % 7
    week1monday = firstday - firstweekday
    if firstweekday > THURSDAY:
        week1monday += 7
    return week1monday


class timezone(tzinfo):
    __slots__ = ('_offset', '_name')
    _Omitted = object()

    def __new__(cls, offset, name=_Omitted):
        if not isinstance(offset, timedelta):
            raise TypeError(b'offset must be a timedelta')
        if name is cls._Omitted:
            if not offset:
                return cls.utc
            name = None
        elif not isinstance(name, str):
            if PY2 and isinstance(name, native_str):
                name = name.decode()
            else:
                raise TypeError(b'name must be a string')
        if not cls._minoffset <= offset <= cls._maxoffset:
            raise ValueError(b'offset must be a timedelta strictly between -timedelta(hours=24) and timedelta(hours=24).')
        if offset.microseconds != 0 or offset.seconds % 60 != 0:
            raise ValueError(b'offset must be a timedelta representing a whole number of minutes')
        return cls._create(offset, name)

    @classmethod
    def _create(cls, offset, name=None):
        self = tzinfo.__new__(cls)
        self._offset = offset
        self._name = name
        return self

    def __getinitargs__(self):
        """pickle support"""
        if self._name is None:
            return (self._offset,)
        else:
            return (
             self._offset, self._name)

    def __eq__(self, other):
        if type(other) != timezone:
            return False
        return self._offset == other._offset

    def __hash__(self):
        return hash(self._offset)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> tz = timezone.utc
        >>> repr(tz)
        'datetime.timezone.utc'
        >>> tz = timezone(timedelta(hours=-5), 'EST')
        >>> repr(tz)
        "datetime.timezone(datetime.timedelta(-1, 68400), 'EST')"
        """
        if self is self.utc:
            return b'datetime.timezone.utc'
        else:
            if self._name is None:
                return b'%s(%r)' % (b'datetime.' + self.__class__.__name__,
                 self._offset)
            return b'%s(%r, %r)' % (b'datetime.' + self.__class__.__name__,
             self._offset, self._name)

    def __str__(self):
        return self.tzname(None)

    def utcoffset(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return self._offset
        else:
            raise TypeError(b'utcoffset() argument must be a datetime instance or None')
            return

    def tzname(self, dt):
        if isinstance(dt, datetime) or dt is None:
            if self._name is None:
                return self._name_from_offset(self._offset)
            return self._name
        else:
            raise TypeError(b'tzname() argument must be a datetime instance or None')
            return

    def dst(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return
        raise TypeError(b'dst() argument must be a datetime instance or None')
        return

    def fromutc(self, dt):
        if isinstance(dt, datetime):
            if dt.tzinfo is not self:
                raise ValueError(b'fromutc: dt.tzinfo is not self')
            return dt + self._offset
        raise TypeError(b'fromutc() argument must be a datetime instance or None')

    _maxoffset = timedelta(hours=23, minutes=59)
    _minoffset = -_maxoffset

    @staticmethod
    def _name_from_offset(delta):
        if delta < timedelta(0):
            sign = b'-'
            delta = -delta
        else:
            sign = b'+'
        hours, rest = divmod(delta, timedelta(hours=1))
        minutes = rest // timedelta(minutes=1)
        return (b'UTC{}{:02d}:{:02d}').format(sign, hours, minutes)


timezone.utc = timezone._create(timedelta(0))
timezone.min = timezone._create(timezone._minoffset)
timezone.max = timezone._create(timezone._maxoffset)
_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
try:
    from _datetime import *
except ImportError:
    pass
else:
    del _DAYNAMES
    del _DAYS_BEFORE_MONTH
    del _DAYS_IN_MONTH
    del _DI100Y
    del _DI400Y
    del _DI4Y
    del _MAXORDINAL
    del _MONTHNAMES
    del _build_struct_time
    del _call_tzinfo_method
    del _check_date_fields
    del _check_time_fields
    del _check_tzinfo_arg
    del _check_tzname
    del _check_utc_offset
    del _cmp
    del _cmperror
    del _date_class
    del _days_before_month
    del _days_before_year
    del _days_in_month
    del _format_time
    del _is_leap
    del _isoweek1monday
    del _math
    del _ord2ymd
    del _time
    del _time_class
    del _tzinfo_class
    del _wrap_strftime
    del _ymd2ord
    from _datetime import __doc__