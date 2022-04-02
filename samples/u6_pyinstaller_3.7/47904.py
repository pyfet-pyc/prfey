# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: datetime.py
"""Concrete date/time and related types.

See http://www.iana.org/time-zones/repository/tz-link.html for
time zone and DST data sources.
"""
import time as _time, math as _math, sys

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
 -1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = [
 -1]
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


def _days_in_month(year, month):
    """year, month -> number of days in that month in that year."""
    assert 1 <= month <= 12, month
    if month == 2:
        if _is_leap(year):
            return 29
    return _DAYS_IN_MONTH[month]


def _days_before_month(year, month):
    """year, month -> number of days in year preceding first day of month."""
    assert 1 <= month <= 12, 'month must be in 1..12'
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


def _ymd2ord(year, month, day):
    """year, month, day -> ordinal, considering 01-Jan-0001 as day 1."""
    assert 1 <= month <= 12, 'month must be in 1..12'
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, 'day must be in 1..%d' % dim
    return _days_before_year(year) + _days_before_month(year, month) + day


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)
assert _DI4Y == 1461
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
        return (year - 1, 12, 31)
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
 None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
_DAYNAMES = [None, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 6) % 7
    dnum = _days_before_month(y, m) + d
    return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _format_time(hh, mm, ss, us, timespec='auto'):
    specs = {'hours':'{:02d}', 
     'minutes':'{:02d}:{:02d}', 
     'seconds':'{:02d}:{:02d}:{:02d}', 
     'milliseconds':'{:02d}:{:02d}:{:02d}.{:03d}', 
     'microseconds':'{:02d}:{:02d}:{:02d}.{:06d}'}
    if timespec == 'auto':
        timespec = 'microseconds' if us else 'seconds'
    else:
        if timespec == 'milliseconds':
            us //= 1000
        else:
            try:
                fmt = specs[timespec]
            except KeyError:
                raise ValueError('Unknown timespec value')
            else:
                return fmt.format(hh, mm, ss, us)


def _format_offset(off):
    s = ''
    if off is not None:
        if off.days < 0:
            sign = '-'
            off = -off
        else:
            sign = '+'
        hh, mm = divmod(off, timedelta(hours=1))
        mm, ss = divmod(mm, timedelta(minutes=1))
        s += '%s%02d:%02d' % (sign, hh, mm)
        if ss or ss.microseconds:
            s += ':%02d' % ss.seconds
            if ss.microseconds:
                s += '.%06d' % ss.microseconds
    return s


def _wrap_strftime(object, format, timetuple):
    freplace = None
    zreplace = None
    Zreplace = None
    newformat = []
    push = newformat.append
    i, n = 0, len(format)
    while i < n:
        ch = format[i]
        i += 1
        if ch == '%':
            if i < n:
                ch = format[i]
                i += 1
                if ch == 'f':
                    if freplace is None:
                        freplace = '%06d' % getattr(object, 'microsecond', 0)
                    newformat.append(freplace)
            elif ch == 'z':
                if zreplace is None:
                    zreplace = ''
                    if hasattr(object, 'utcoffset'):
                        offset = object.utcoffset()
                        if offset is not None:
                            sign = '+'
                            if offset.days < 0:
                                offset = -offset
                                sign = '-'
                            else:
                                h, rest = divmod(offset, timedelta(hours=1))
                                m, rest = divmod(rest, timedelta(minutes=1))
                                s = rest.seconds
                                u = offset.microseconds
                                if u:
                                    zreplace = '%c%02d%02d%02d.%06d' % (sign, h, m, s, u)
                                else:
                                    if s:
                                        zreplace = '%c%02d%02d%02d' % (sign, h, m, s)
                                    else:
                                        zreplace = '%c%02d%02d' % (sign, h, m)
                    assert '%' not in zreplace
                    newformat.append(zreplace)
                elif ch == 'Z':
                    if Zreplace is None:
                        Zreplace = ''
                        if hasattr(object, 'tzname'):
                            s = object.tzname()
                            if s is not None:
                                Zreplace = s.replace('%', '%%')
                    newformat.append(Zreplace)
                else:
                    push('%')
                    push(ch)
            else:
                push('%')
        else:
            push(ch)

    newformat = ''.join(newformat)
    return _time.strftime(newformat, timetuple)


def _parse_isoformat_date(dtstr):
    year = int(dtstr[0:4])
    if dtstr[4] != '-':
        raise ValueError('Invalid date separator: %s' % dtstr[4])
    month = int(dtstr[5:7])
    if dtstr[7] != '-':
        raise ValueError('Invalid date separator')
    day = int(dtstr[8:10])
    return [
     year, month, day]


def _parse_hh_mm_ss_ff(tstr):
    len_str = len(tstr)
    time_comps = [
     0, 0, 0, 0]
    pos = 0
    for comp in range(0, 3):
        if len_str - pos < 2:
            raise ValueError('Incomplete time component')
        time_comps[comp] = int(tstr[pos:pos + 2])
        pos += 2
        next_char = tstr[pos:pos + 1]
        if not next_char or comp >= 2:
            break
        if next_char != ':':
            raise ValueError('Invalid time separator: %c' % next_char)
        pos += 1

    if pos < len_str:
        if tstr[pos] != '.':
            raise ValueError('Invalid microsecond component')
        else:
            pos += 1
            len_remainder = len_str - pos
            if len_remainder not in (3, 6):
                raise ValueError('Invalid microsecond component')
            time_comps[3] = int(tstr[pos:])
        if len_remainder == 3:
            time_comps[3] *= 1000
    return time_comps


def _parse_isoformat_time(tstr):
    len_str = len(tstr)
    if len_str < 2:
        raise ValueError('Isoformat time too short')
    else:
        tz_pos = tstr.find('-') + 1 or tstr.find('+') + 1
        timestr = tstr[:tz_pos - 1] if tz_pos > 0 else tstr
        time_comps = _parse_hh_mm_ss_ff(timestr)
        tzi = None
        if tz_pos > 0:
            tzstr = tstr[tz_pos:]
            if len(tzstr) not in (5, 8, 15):
                raise ValueError('Malformed time zone string')
            tz_comps = _parse_hh_mm_ss_ff(tzstr)
            if all((x == 0 for x in tz_comps)):
                tzi = timezone.utc
            else:
                tzsign = -1 if tstr[(tz_pos - 1)] == '-' else 1
            td = timedelta(hours=(tz_comps[0]), minutes=(tz_comps[1]), seconds=(tz_comps[2]),
              microseconds=(tz_comps[3]))
            tzi = timezone(tzsign * td)
    time_comps.append(tzi)
    return time_comps


def _check_tzname(name):
    if name is not None:
        if not isinstance(name, str):
            raise TypeError("tzinfo.tzname() must return None or string, not '%s'" % type(name))


def _check_utc_offset(name, offset):
    if not name in ('utcoffset', 'dst'):
        raise AssertionError
    else:
        if offset is None:
            return
        assert isinstance(offset, timedelta), "tzinfo.%s() must return None or timedelta, not '%s'" % (
         name, type(offset))
    if not -timedelta(1) < offset < timedelta(1):
        raise ValueError('%s()=%s, must be strictly between -timedelta(hours=24) and timedelta(hours=24)' % (
         name, offset))


def _check_int_field(value):
    if isinstance(value, int):
        return value
    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value
            raise TypeError('__int__ returned non-int (type %s)' % type(value).__name__)
        raise TypeError('an integer is required (got type %s)' % type(value).__name__)
    raise TypeError('integer argument expected, got float')


def _check_date_fields(year, month, day):
    year = _check_int_field(year)
    month = _check_int_field(month)
    day = _check_int_field(day)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12', month)
    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError('day must be in 1..%d' % dim, day)
    return (
     year, month, day)


def _check_time_fields(hour, minute, second, microsecond, fold):
    hour = _check_int_field(hour)
    minute = _check_int_field(minute)
    second = _check_int_field(second)
    microsecond = _check_int_field(microsecond)
    if not 0 <= hour <= 23:
        raise ValueError('hour must be in 0..23', hour)
    if not 0 <= minute <= 59:
        raise ValueError('minute must be in 0..59', minute)
    if not 0 <= second <= 59:
        raise ValueError('second must be in 0..59', second)
    if not 0 <= microsecond <= 999999:
        raise ValueError('microsecond must be in 0..999999', microsecond)
    if fold not in (0, 1):
        raise ValueError('fold must be either 0 or 1', fold)
    return (
     hour, minute, second, microsecond, fold)


def _check_tzinfo_arg(tz):
    if tz is not None:
        if not isinstance(tz, tzinfo):
            raise TypeError('tzinfo argument must be None or of a tzinfo subclass')


def _cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (
     type(x).__name__, type(y).__name__))


def _divide_and_round(a, b):
    """divide a by b and round result to the nearest integer

    When the ratio is exactly half-way between two integers,
    the even integer is returned.
    """
    q, r = divmod(a, b)
    r *= 2
    greater_than_half = r > b if b > 0 else r < b
    if (greater_than_half or r) == b:
        if q % 2 == 1:
            q += 1
    return q


class timedelta:
    __doc__ = 'Represent the difference between two datetime objects.\n\n    Supported operators:\n\n    - add, subtract timedelta\n    - unary plus, minus, abs\n    - compare to timedelta\n    - multiply, divide by int\n\n    In addition, datetime supports subtraction of two datetime objects\n    returning a timedelta, and addition or subtraction of a datetime\n    and a timedelta giving a datetime.\n\n    Representation: (days, seconds, microseconds).  Why?  Because I\n    felt like it.\n    '
    __slots__ = ('_days', '_seconds', '_microseconds', '_hashcode')

    def __new__--- This code section failed: ---

 L. 487         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'd'
                6  DUP_TOP          
                8  STORE_FAST               's'
               10  STORE_FAST               'us'

 L. 490        12  LOAD_FAST                'days'
               14  LOAD_FAST                'weeks'
               16  LOAD_CONST               7
               18  BINARY_MULTIPLY  
               20  INPLACE_ADD      
               22  STORE_FAST               'days'

 L. 491        24  LOAD_FAST                'seconds'
               26  LOAD_FAST                'minutes'
               28  LOAD_CONST               60
               30  BINARY_MULTIPLY  
               32  LOAD_FAST                'hours'
               34  LOAD_CONST               3600
               36  BINARY_MULTIPLY  
               38  BINARY_ADD       
               40  INPLACE_ADD      
               42  STORE_FAST               'seconds'

 L. 492        44  LOAD_FAST                'microseconds'
               46  LOAD_FAST                'milliseconds'
               48  LOAD_CONST               1000
               50  BINARY_MULTIPLY  
               52  INPLACE_ADD      
               54  STORE_FAST               'microseconds'

 L. 496        56  LOAD_GLOBAL              isinstance
               58  LOAD_FAST                'days'
               60  LOAD_GLOBAL              float
               62  CALL_FUNCTION_2       2  '2 positional arguments'
               64  POP_JUMP_IF_FALSE   148  'to 148'

 L. 497        66  LOAD_GLOBAL              _math
               68  LOAD_METHOD              modf
               70  LOAD_FAST                'days'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'dayfrac'
               78  STORE_FAST               'days'

 L. 498        80  LOAD_GLOBAL              _math
               82  LOAD_METHOD              modf
               84  LOAD_FAST                'dayfrac'
               86  LOAD_CONST               86400.0
               88  BINARY_MULTIPLY  
               90  CALL_METHOD_1         1  '1 positional argument'
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               'daysecondsfrac'
               96  STORE_FAST               'daysecondswhole'

 L. 499        98  LOAD_FAST                'daysecondswhole'
              100  LOAD_GLOBAL              int
              102  LOAD_FAST                'daysecondswhole'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_TRUE    114  'to 114'
              110  LOAD_ASSERT              AssertionError
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           108  '108'

 L. 500       114  LOAD_GLOBAL              int
              116  LOAD_FAST                'daysecondswhole'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  STORE_FAST               's'

 L. 501       122  LOAD_FAST                'days'
              124  LOAD_GLOBAL              int
              126  LOAD_FAST                'days'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_TRUE    138  'to 138'
              134  LOAD_ASSERT              AssertionError
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           132  '132'

 L. 502       138  LOAD_GLOBAL              int
              140  LOAD_FAST                'days'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  STORE_FAST               'd'
              146  JUMP_FORWARD        156  'to 156'
            148_0  COME_FROM            64  '64'

 L. 504       148  LOAD_CONST               0.0
              150  STORE_FAST               'daysecondsfrac'

 L. 505       152  LOAD_FAST                'days'
              154  STORE_FAST               'd'
            156_0  COME_FROM           146  '146'

 L. 506       156  LOAD_GLOBAL              isinstance
              158  LOAD_FAST                'daysecondsfrac'
              160  LOAD_GLOBAL              float
              162  CALL_FUNCTION_2       2  '2 positional arguments'
              164  POP_JUMP_IF_TRUE    170  'to 170'
              166  LOAD_ASSERT              AssertionError
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           164  '164'

 L. 507       170  LOAD_GLOBAL              abs
              172  LOAD_FAST                'daysecondsfrac'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_CONST               1.0
              178  COMPARE_OP               <=
              180  POP_JUMP_IF_TRUE    186  'to 186'
              182  LOAD_ASSERT              AssertionError
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           180  '180'

 L. 508       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'd'
              190  LOAD_GLOBAL              int
              192  CALL_FUNCTION_2       2  '2 positional arguments'
              194  POP_JUMP_IF_TRUE    200  'to 200'
              196  LOAD_ASSERT              AssertionError
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           194  '194'

 L. 509       200  LOAD_GLOBAL              abs
              202  LOAD_FAST                's'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  LOAD_CONST               86400
              208  COMPARE_OP               <=
              210  POP_JUMP_IF_TRUE    216  'to 216'
              212  LOAD_ASSERT              AssertionError
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           210  '210'

 L. 512       216  LOAD_GLOBAL              isinstance
              218  LOAD_FAST                'seconds'
              220  LOAD_GLOBAL              float
              222  CALL_FUNCTION_2       2  '2 positional arguments'
          224_226  POP_JUMP_IF_FALSE   296  'to 296'

 L. 513       228  LOAD_GLOBAL              _math
              230  LOAD_METHOD              modf
              232  LOAD_FAST                'seconds'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  UNPACK_SEQUENCE_2     2 
              238  STORE_FAST               'secondsfrac'
              240  STORE_FAST               'seconds'

 L. 514       242  LOAD_FAST                'seconds'
              244  LOAD_GLOBAL              int
              246  LOAD_FAST                'seconds'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_TRUE    260  'to 260'
              256  LOAD_ASSERT              AssertionError
              258  RAISE_VARARGS_1       1  'exception instance'
            260_0  COME_FROM           252  '252'

 L. 515       260  LOAD_GLOBAL              int
              262  LOAD_FAST                'seconds'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  STORE_FAST               'seconds'

 L. 516       268  LOAD_FAST                'secondsfrac'
              270  LOAD_FAST                'daysecondsfrac'
              272  INPLACE_ADD      
              274  STORE_FAST               'secondsfrac'

 L. 517       276  LOAD_GLOBAL              abs
              278  LOAD_FAST                'secondsfrac'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  LOAD_CONST               2.0
              284  COMPARE_OP               <=
          286_288  POP_JUMP_IF_TRUE    300  'to 300'
              290  LOAD_GLOBAL              AssertionError
              292  RAISE_VARARGS_1       1  'exception instance'
              294  JUMP_FORWARD        300  'to 300'
            296_0  COME_FROM           224  '224'

 L. 519       296  LOAD_FAST                'daysecondsfrac'
              298  STORE_FAST               'secondsfrac'
            300_0  COME_FROM           294  '294'
            300_1  COME_FROM           286  '286'

 L. 521       300  LOAD_GLOBAL              isinstance
              302  LOAD_FAST                'secondsfrac'
              304  LOAD_GLOBAL              float
              306  CALL_FUNCTION_2       2  '2 positional arguments'
          308_310  POP_JUMP_IF_TRUE    316  'to 316'
              312  LOAD_ASSERT              AssertionError
              314  RAISE_VARARGS_1       1  'exception instance'
            316_0  COME_FROM           308  '308'

 L. 522       316  LOAD_GLOBAL              abs
              318  LOAD_FAST                'secondsfrac'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  LOAD_CONST               2.0
              324  COMPARE_OP               <=
          326_328  POP_JUMP_IF_TRUE    334  'to 334'
              330  LOAD_ASSERT              AssertionError
              332  RAISE_VARARGS_1       1  'exception instance'
            334_0  COME_FROM           326  '326'

 L. 524       334  LOAD_GLOBAL              isinstance
              336  LOAD_FAST                'seconds'
              338  LOAD_GLOBAL              int
              340  CALL_FUNCTION_2       2  '2 positional arguments'
          342_344  POP_JUMP_IF_TRUE    350  'to 350'
              346  LOAD_ASSERT              AssertionError
              348  RAISE_VARARGS_1       1  'exception instance'
            350_0  COME_FROM           342  '342'

 L. 525       350  LOAD_GLOBAL              divmod
              352  LOAD_FAST                'seconds'
              354  LOAD_CONST               86400
              356  CALL_FUNCTION_2       2  '2 positional arguments'
              358  UNPACK_SEQUENCE_2     2 
              360  STORE_FAST               'days'
              362  STORE_FAST               'seconds'

 L. 526       364  LOAD_FAST                'd'
              366  LOAD_FAST                'days'
              368  INPLACE_ADD      
              370  STORE_FAST               'd'

 L. 527       372  LOAD_FAST                's'
              374  LOAD_GLOBAL              int
              376  LOAD_FAST                'seconds'
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  INPLACE_ADD      
              382  STORE_FAST               's'

 L. 528       384  LOAD_GLOBAL              isinstance
              386  LOAD_FAST                's'
              388  LOAD_GLOBAL              int
              390  CALL_FUNCTION_2       2  '2 positional arguments'
          392_394  POP_JUMP_IF_TRUE    400  'to 400'
              396  LOAD_ASSERT              AssertionError
              398  RAISE_VARARGS_1       1  'exception instance'
            400_0  COME_FROM           392  '392'

 L. 529       400  LOAD_GLOBAL              abs
              402  LOAD_FAST                's'
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  LOAD_CONST               172800
              408  COMPARE_OP               <=
          410_412  POP_JUMP_IF_TRUE    418  'to 418'
              414  LOAD_ASSERT              AssertionError
              416  RAISE_VARARGS_1       1  'exception instance'
            418_0  COME_FROM           410  '410'

 L. 532       418  LOAD_FAST                'secondsfrac'
              420  LOAD_CONST               1000000.0
              422  BINARY_MULTIPLY  
              424  STORE_FAST               'usdouble'

 L. 533       426  LOAD_GLOBAL              abs
              428  LOAD_FAST                'usdouble'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  LOAD_CONST               2100000.0
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_TRUE    444  'to 444'
              440  LOAD_ASSERT              AssertionError
              442  RAISE_VARARGS_1       1  'exception instance'
            444_0  COME_FROM           436  '436'

 L. 536       444  LOAD_GLOBAL              isinstance
              446  LOAD_FAST                'microseconds'
              448  LOAD_GLOBAL              float
              450  CALL_FUNCTION_2       2  '2 positional arguments'
          452_454  POP_JUMP_IF_FALSE   514  'to 514'

 L. 537       456  LOAD_GLOBAL              round
              458  LOAD_FAST                'microseconds'
              460  LOAD_FAST                'usdouble'
              462  BINARY_ADD       
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  STORE_FAST               'microseconds'

 L. 538       468  LOAD_GLOBAL              divmod
              470  LOAD_FAST                'microseconds'
              472  LOAD_CONST               1000000
              474  CALL_FUNCTION_2       2  '2 positional arguments'
              476  UNPACK_SEQUENCE_2     2 
              478  STORE_FAST               'seconds'
              480  STORE_FAST               'microseconds'

 L. 539       482  LOAD_GLOBAL              divmod
              484  LOAD_FAST                'seconds'
              486  LOAD_CONST               86400
              488  CALL_FUNCTION_2       2  '2 positional arguments'
              490  UNPACK_SEQUENCE_2     2 
              492  STORE_FAST               'days'
              494  STORE_FAST               'seconds'

 L. 540       496  LOAD_FAST                'd'
              498  LOAD_FAST                'days'
              500  INPLACE_ADD      
              502  STORE_FAST               'd'

 L. 541       504  LOAD_FAST                's'
              506  LOAD_FAST                'seconds'
              508  INPLACE_ADD      
              510  STORE_FAST               's'
              512  JUMP_FORWARD        578  'to 578'
            514_0  COME_FROM           452  '452'

 L. 543       514  LOAD_GLOBAL              int
              516  LOAD_FAST                'microseconds'
              518  CALL_FUNCTION_1       1  '1 positional argument'
              520  STORE_FAST               'microseconds'

 L. 544       522  LOAD_GLOBAL              divmod
              524  LOAD_FAST                'microseconds'
              526  LOAD_CONST               1000000
              528  CALL_FUNCTION_2       2  '2 positional arguments'
              530  UNPACK_SEQUENCE_2     2 
              532  STORE_FAST               'seconds'
              534  STORE_FAST               'microseconds'

 L. 545       536  LOAD_GLOBAL              divmod
              538  LOAD_FAST                'seconds'
              540  LOAD_CONST               86400
              542  CALL_FUNCTION_2       2  '2 positional arguments'
              544  UNPACK_SEQUENCE_2     2 
              546  STORE_FAST               'days'
              548  STORE_FAST               'seconds'

 L. 546       550  LOAD_FAST                'd'
              552  LOAD_FAST                'days'
              554  INPLACE_ADD      
              556  STORE_FAST               'd'

 L. 547       558  LOAD_FAST                's'
              560  LOAD_FAST                'seconds'
              562  INPLACE_ADD      
              564  STORE_FAST               's'

 L. 548       566  LOAD_GLOBAL              round
              568  LOAD_FAST                'microseconds'
              570  LOAD_FAST                'usdouble'
              572  BINARY_ADD       
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  STORE_FAST               'microseconds'
            578_0  COME_FROM           512  '512'

 L. 549       578  LOAD_GLOBAL              isinstance
              580  LOAD_FAST                's'
              582  LOAD_GLOBAL              int
              584  CALL_FUNCTION_2       2  '2 positional arguments'
          586_588  POP_JUMP_IF_TRUE    594  'to 594'
              590  LOAD_ASSERT              AssertionError
              592  RAISE_VARARGS_1       1  'exception instance'
            594_0  COME_FROM           586  '586'

 L. 550       594  LOAD_GLOBAL              isinstance
              596  LOAD_FAST                'microseconds'
              598  LOAD_GLOBAL              int
              600  CALL_FUNCTION_2       2  '2 positional arguments'
          602_604  POP_JUMP_IF_TRUE    610  'to 610'
              606  LOAD_ASSERT              AssertionError
              608  RAISE_VARARGS_1       1  'exception instance'
            610_0  COME_FROM           602  '602'

 L. 551       610  LOAD_GLOBAL              abs
              612  LOAD_FAST                's'
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  LOAD_CONST               259200
              618  COMPARE_OP               <=
          620_622  POP_JUMP_IF_TRUE    628  'to 628'
              624  LOAD_ASSERT              AssertionError
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           620  '620'

 L. 552       628  LOAD_GLOBAL              abs
              630  LOAD_FAST                'microseconds'
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  LOAD_CONST               3100000.0
              636  COMPARE_OP               <
          638_640  POP_JUMP_IF_TRUE    646  'to 646'
              642  LOAD_ASSERT              AssertionError
              644  RAISE_VARARGS_1       1  'exception instance'
            646_0  COME_FROM           638  '638'

 L. 555       646  LOAD_GLOBAL              divmod
              648  LOAD_FAST                'microseconds'
              650  LOAD_CONST               1000000
              652  CALL_FUNCTION_2       2  '2 positional arguments'
              654  UNPACK_SEQUENCE_2     2 
              656  STORE_FAST               'seconds'
              658  STORE_FAST               'us'

 L. 556       660  LOAD_FAST                's'
              662  LOAD_FAST                'seconds'
              664  INPLACE_ADD      
              666  STORE_FAST               's'

 L. 557       668  LOAD_GLOBAL              divmod
              670  LOAD_FAST                's'
              672  LOAD_CONST               86400
              674  CALL_FUNCTION_2       2  '2 positional arguments'
              676  UNPACK_SEQUENCE_2     2 
              678  STORE_FAST               'days'
              680  STORE_FAST               's'

 L. 558       682  LOAD_FAST                'd'
              684  LOAD_FAST                'days'
              686  INPLACE_ADD      
              688  STORE_FAST               'd'

 L. 560       690  LOAD_GLOBAL              isinstance
              692  LOAD_FAST                'd'
              694  LOAD_GLOBAL              int
              696  CALL_FUNCTION_2       2  '2 positional arguments'
          698_700  POP_JUMP_IF_TRUE    706  'to 706'
              702  LOAD_ASSERT              AssertionError
              704  RAISE_VARARGS_1       1  'exception instance'
            706_0  COME_FROM           698  '698'

 L. 561       706  LOAD_GLOBAL              isinstance
              708  LOAD_FAST                's'
              710  LOAD_GLOBAL              int
              712  CALL_FUNCTION_2       2  '2 positional arguments'
          714_716  POP_JUMP_IF_FALSE   744  'to 744'
              718  LOAD_CONST               0
              720  LOAD_FAST                's'
              722  DUP_TOP          
              724  ROT_THREE        
              726  COMPARE_OP               <=
          728_730  POP_JUMP_IF_FALSE   742  'to 742'
              732  LOAD_CONST               86400
              734  COMPARE_OP               <
          736_738  POP_JUMP_IF_TRUE    748  'to 748'
              740  JUMP_FORWARD        744  'to 744'
            742_0  COME_FROM           728  '728'
              742  POP_TOP          
            744_0  COME_FROM           740  '740'
            744_1  COME_FROM           714  '714'
              744  LOAD_GLOBAL              AssertionError
              746  RAISE_VARARGS_1       1  'exception instance'
            748_0  COME_FROM           736  '736'

 L. 562       748  LOAD_GLOBAL              isinstance
              750  LOAD_FAST                'us'
              752  LOAD_GLOBAL              int
              754  CALL_FUNCTION_2       2  '2 positional arguments'
          756_758  POP_JUMP_IF_FALSE   786  'to 786'
              760  LOAD_CONST               0
              762  LOAD_FAST                'us'
              764  DUP_TOP          
              766  ROT_THREE        
              768  COMPARE_OP               <=
          770_772  POP_JUMP_IF_FALSE   784  'to 784'
              774  LOAD_CONST               1000000
              776  COMPARE_OP               <
          778_780  POP_JUMP_IF_TRUE    790  'to 790'
              782  JUMP_FORWARD        786  'to 786'
            784_0  COME_FROM           770  '770'
              784  POP_TOP          
            786_0  COME_FROM           782  '782'
            786_1  COME_FROM           756  '756'
              786  LOAD_GLOBAL              AssertionError
              788  RAISE_VARARGS_1       1  'exception instance'
            790_0  COME_FROM           778  '778'

 L. 564       790  LOAD_GLOBAL              abs
              792  LOAD_FAST                'd'
              794  CALL_FUNCTION_1       1  '1 positional argument'
              796  LOAD_CONST               999999999
              798  COMPARE_OP               >
          800_802  POP_JUMP_IF_FALSE   816  'to 816'

 L. 565       804  LOAD_GLOBAL              OverflowError
              806  LOAD_STR                 'timedelta # of days is too large: %d'
              808  LOAD_FAST                'd'
              810  BINARY_MODULO    
              812  CALL_FUNCTION_1       1  '1 positional argument'
              814  RAISE_VARARGS_1       1  'exception instance'
            816_0  COME_FROM           800  '800'

 L. 567       816  LOAD_GLOBAL              object
              818  LOAD_METHOD              __new__
              820  LOAD_FAST                'cls'
              822  CALL_METHOD_1         1  '1 positional argument'
              824  STORE_FAST               'self'

 L. 568       826  LOAD_FAST                'd'
              828  LOAD_FAST                'self'
              830  STORE_ATTR               _days

 L. 569       832  LOAD_FAST                's'
              834  LOAD_FAST                'self'
              836  STORE_ATTR               _seconds

 L. 570       838  LOAD_FAST                'us'
              840  LOAD_FAST                'self'
              842  STORE_ATTR               _microseconds

 L. 571       844  LOAD_CONST               -1
              846  LOAD_FAST                'self'
              848  STORE_ATTR               _hashcode

 L. 572       850  LOAD_FAST                'self'
              852  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 852

    def __repr__(self):
        args = []
        if self._days:
            args.append('days=%d' % self._days)
        if self._seconds:
            args.append('seconds=%d' % self._seconds)
        if self._microseconds:
            args.append('microseconds=%d' % self._microseconds)
        if not args:
            args.append('0')
        return '%s.%s(%s)' % (self.__class__.__module__,
         self.__class__.__qualname__,
         ', '.join(args))

    def __str__(self):
        mm, ss = divmod(self._seconds, 60)
        hh, mm = divmod(mm, 60)
        s = '%d:%02d:%02d' % (hh, mm, ss)
        if self._days:

            def plural(n):
                return (
                 n, abs(n) != 1 and 's' or '')

            s = '%d day%s, ' % plural(self._days) + s
        if self._microseconds:
            s = s + '.%06d' % self._microseconds
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
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            return timedelta(self._days * other, self._seconds * other, self._microseconds * other)
        if isinstance(other, float):
            usec = self._to_microseconds()
            a, b = other.as_integer_ratio()
            return timedelta(0, 0, _divide_and_round(usec * a, b))
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
            return timedelta(0, 0, _divide_and_round(usec, other))
        if isinstance(other, float):
            a, b = other.as_integer_ratio()
            return timedelta(0, 0, _divide_and_round(b * usec, a))

    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = self._to_microseconds() % other._to_microseconds()
            return timedelta(0, 0, r)
        return NotImplemented

    def __divmod__(self, other):
        if isinstance(other, timedelta):
            q, r = divmod(self._to_microseconds(), other._to_microseconds())
            return (q, timedelta(0, 0, r))
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, timedelta):
            return self._cmp(other) == 0
        return False

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
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode

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

class date:
    __doc__ = 'Concrete date type.\n\n    Constructors:\n\n    __new__()\n    fromtimestamp()\n    today()\n    fromordinal()\n\n    Operators:\n\n    __repr__, __str__\n    __eq__, __le__, __lt__, __ge__, __gt__, __hash__\n    __add__, __radd__, __sub__ (add/radd only with timedelta arg)\n\n    Methods:\n\n    timetuple()\n    toordinal()\n    weekday()\n    isoweekday(), isocalendar(), isoformat()\n    ctime()\n    strftime()\n\n    Properties (readonly):\n    year, month, day\n    '
    __slots__ = ('_year', '_month', '_day', '_hashcode')

    def __new__(cls, year, month=None, day=None):
        """Constructor.

        Arguments:

        year, month, day (required, base 1)
        """
        if month is None:
            if isinstance(year, bytes):
                if len(year) == 4:
                    if 1 <= year[2] <= 12:
                        self = object.__new__(cls)
                        self._date__setstate(year)
                        self._hashcode = -1
                        return self
        year, month, day = _check_date_fields(year, month, day)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
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
        """Construct a date from a proleptic Gregorian ordinal.

        January 1 of year 1 is day 1.  Only the year, month and day are
        non-zero in the result.
        """
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a date from the output of date.isoformat()."""
        if not isinstance(date_string, str):
            raise TypeError('fromisoformat: argument must be str')
        try:
            assert len(date_string) == 10
            return cls(*_parse_isoformat_date(date_string))
        except Exception:
            raise ValueError('Invalid isoformat string: %s' % date_string)

    def __repr__(self):
        """Convert to formal string, for repr().

        >>> dt = datetime(2010, 1, 1)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0)'

        >>> dt = datetime(2010, 1, 1, tzinfo=timezone.utc)
        >>> repr(dt)
        'datetime.datetime(2010, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)'
        """
        return '%s.%s(%d, %d, %d)' % (self.__class__.__module__,
         self.__class__.__qualname__,
         self._year,
         self._month,
         self._day)

    def ctime(self):
        """Return ctime() style string."""
        weekday = self.toordinal() % 7 or 7
        return '%s %s %2d 00:00:00 %04d' % (
         _DAYNAMES[weekday],
         _MONTHNAMES[self._month],
         self._day, self._year)

    def strftime(self, fmt):
        """Format using strftime()."""
        return _wrap_strftime(self, fmt, self.timetuple())

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError('must be str, not %s' % type(fmt).__name__)
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
        return '%04d-%02d-%02d' % (self._year, self._month, self._day)

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
        return type(self)(year, month, day)

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
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
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode

    def __add__(self, other):
        """Add a date to a timedelta."""
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days
            if 0 < o <= _MAXORDINAL:
                return date.fromordinal(o)
            raise OverflowError('result out of range')
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
        (used with permission)
        """
        year = self._year
        week1monday = _isoweek1monday(year)
        today = _ymd2ord(self._year, self._month, self._day)
        week, day = divmod(today - week1monday, 7)
        if week < 0:
            year -= 1
            week1monday = _isoweek1monday(year)
            week, day = divmod(today - week1monday, 7)
        else:
            if week >= 52:
                if today >= _isoweek1monday(year + 1):
                    year += 1
                    week = 0
        return (
         year, week + 1, day + 1)

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        return (bytes([yhi, ylo, self._month, self._day]),)

    def __setstate(self, string):
        yhi, ylo, self._month, self._day = string
        self._year = yhi * 256 + ylo

    def __reduce__(self):
        return (
         self.__class__, self._getstate())


_date_class = date
date.min = date(1, 1, 1)
date.max = date(9999, 12, 31)
date.resolution = timedelta(days=1)

class tzinfo:
    __doc__ = 'Abstract base class for time zone info classes.\n\n    Subclasses must override the name(), utcoffset() and dst() methods.\n    '
    __slots__ = ()

    def tzname(self, dt):
        """datetime -> string name of time zone."""
        raise NotImplementedError('tzinfo subclass must override tzname()')

    def utcoffset(self, dt):
        """datetime -> timedelta, positive for east of UTC, negative for west of UTC"""
        raise NotImplementedError('tzinfo subclass must override utcoffset()')

    def dst(self, dt):
        """datetime -> DST offset as timedelta, positive for east of UTC.

        Return 0 if DST not in effect.  utcoffset() must include the DST
        offset.
        """
        raise NotImplementedError('tzinfo subclass must override dst()')

    def fromutc(self, dt):
        """datetime in UTC -> datetime in local time."""
        if not isinstance(dt, datetime):
            raise TypeError('fromutc() requires a datetime argument')
        else:
            if dt.tzinfo is not self:
                raise ValueError('dt.tzinfo is not self')
            dtoff = dt.utcoffset()
            if dtoff is None:
                raise ValueError('fromutc() requires a non-None utcoffset() result')
            dtdst = dt.dst()
            if dtdst is None:
                raise ValueError('fromutc() requires a non-None dst() result')
            delta = dtoff - dtdst
            if delta:
                dt += delta
                dtdst = dt.dst()
                if dtdst is None:
                    raise ValueError('fromutc(): dt.dst gave inconsistent results; cannot convert')
        return dt + dtdst

    def __reduce__(self):
        getinitargs = getattr(self, '__getinitargs__', None)
        if getinitargs:
            args = getinitargs()
        else:
            args = ()
        getstate = getattr(self, '__getstate__', None)
        if getstate:
            state = getstate()
        else:
            state = getattr(self, '__dict__', None) or None
        if state is None:
            return (
             self.__class__, args)
        return (self.__class__, args, state)


_tzinfo_class = tzinfo

class time:
    __doc__ = 'Time with time zone.\n\n    Constructors:\n\n    __new__()\n\n    Operators:\n\n    __repr__, __str__\n    __eq__, __le__, __lt__, __ge__, __gt__, __hash__\n\n    Methods:\n\n    strftime()\n    isoformat()\n    utcoffset()\n    tzname()\n    dst()\n\n    Properties (readonly):\n    hour, minute, second, microsecond, tzinfo, fold\n    '
    __slots__ = ('_hour', '_minute', '_second', '_microsecond', '_tzinfo', '_hashcode',
                 '_fold')

    def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        """Constructor.

        Arguments:

        hour, minute (required)
        second, microsecond (default to zero)
        tzinfo (default to None)
        fold (keyword only, default to zero)
        """
        if isinstance(hour, bytes):
            if len(hour) == 6:
                if hour[0] & 127 < 24:
                    self = object.__new__(cls)
                    self._time__setstate(hour, minute or None)
                    self._hashcode = -1
                    return self
        hour, minute, second, microsecond, fold = _check_time_fields(hour, minute, second, microsecond, fold)
        _check_tzinfo_arg(tzinfo)
        self = object.__new__(cls)
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._hashcode = -1
        self._fold = fold
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

    @property
    def fold(self):
        return self._fold

    def __eq__(self, other):
        if isinstance(other, time):
            return self._cmp(other, allow_mixed=True) == 0
        return False

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
        if not isinstance(other, time):
            raise AssertionError
        else:
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
        if myoff is None or otoff is None:
            if allow_mixed:
                return 2
            raise TypeError('cannot compare naive and aware times')
        myhhmm = self._hour * 60 + self._minute - myoff // timedelta(minutes=1)
        othhmm = other._hour * 60 + other._minute - otoff // timedelta(minutes=1)
        return _cmp((myhhmm, self._second, self._microsecond), (
         othhmm, other._second, other._microsecond))

    def __hash__(self):
        """Hash."""
        if self._hashcode == -1:
            if self.fold:
                t = self.replace(fold=0)
            else:
                t = self
            tzoff = t.utcoffset()
            if not tzoff:
                self._hashcode = hash(t._getstate()[0])
            else:
                h, m = divmod(timedelta(hours=(self.hour), minutes=(self.minute)) - tzoff, timedelta(hours=1))
                if m % timedelta(minutes=1):
                    raise AssertionError('whole minute')
                m //= timedelta(minutes=1)
                if 0 <= h < 24:
                    self._hashcode = hash(time(h, m, self.second, self.microsecond))
                else:
                    self._hashcode = hash((h, m, self.second, self.microsecond))
        return self._hashcode

    def _tzstr(self):
        """Return formatted timezone offset (+xx:xx) or an empty string."""
        off = self.utcoffset()
        return _format_offset(off)

    def __repr__(self):
        """Convert to formal string, for repr()."""
        if self._microsecond != 0:
            s = ', %d, %d' % (self._second, self._microsecond)
        else:
            if self._second != 0:
                s = ', %d' % self._second
            else:
                s = ''
        s = '%s.%s(%d, %d%s)' % (self.__class__.__module__,
         self.__class__.__qualname__,
         self._hour, self._minute, s)
        if self._tzinfo is not None:
            assert s[-1:] == ')'
            s = s[:-1] + ', tzinfo=%r' % self._tzinfo + ')'
        if self._fold:
            assert s[-1:] == ')'
            s = s[:-1] + ', fold=1)'
        return s

    def isoformat(self, timespec='auto'):
        """Return the time formatted according to ISO.

        The full format is 'HH:MM:SS.mmmmmm+zz:zz'. By default, the fractional
        part is omitted if self.microsecond == 0.

        The optional argument timespec specifies the number of additional
        terms of the time to include.
        """
        s = _format_time(self._hour, self._minute, self._second, self._microsecond, timespec)
        tz = self._tzstr()
        if tz:
            s += tz
        return s

    __str__ = isoformat

    @classmethod
    def fromisoformat(cls, time_string):
        """Construct a time from the output of isoformat()."""
        if not isinstance(time_string, str):
            raise TypeError('fromisoformat: argument must be str')
        try:
            return cls(*_parse_isoformat_time(time_string))
        except Exception:
            raise ValueError('Invalid isoformat string: %s' % time_string)

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
        if not isinstance(fmt, str):
            raise TypeError('must be str, not %s' % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def utcoffset(self):
        """Return the timezone offset as timedelta, positive east of UTC
         (negative west of UTC)."""
        if self._tzinfo is None:
            return
        offset = self._tzinfo.utcoffset(None)
        _check_utc_offset('utcoffset', offset)
        return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        if self._tzinfo is None:
            return
        name = self._tzinfo.tzname(None)
        _check_tzname(name)
        return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (as timedelta
        positive eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return
        offset = self._tzinfo.dst(None)
        _check_utc_offset('dst', offset)
        return offset

    def replace(self, hour=None, minute=None, second=None, microsecond=None, tzinfo=True, *, fold=None):
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
        if fold is None:
            fold = self._fold
        return type(self)(hour, minute, second, microsecond, tzinfo, fold=fold)

    def _getstate(self, protocol=3):
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        h = self._hour
        if self._fold:
            if protocol > 3:
                h += 128
        basestate = bytes([h, self._minute, self._second,
         us1, us2, us3])
        if self._tzinfo is None:
            return (
             basestate,)
        return (basestate, self._tzinfo)

    def __setstate(self, string, tzinfo):
        if tzinfo is not None:
            if not isinstance(tzinfo, _tzinfo_class):
                raise TypeError('bad tzinfo state arg')
        else:
            h, self._minute, self._second, us1, us2, us3 = string
            if h > 127:
                self._fold = 1
                self._hour = h - 128
            else:
                self._fold = 0
            self._hour = h
        self._microsecond = (us1 << 8 | us2) << 8 | us3
        self._tzinfo = tzinfo

    def __reduce_ex__(self, protocol):
        return (
         time, self._getstate(protocol))

    def __reduce__(self):
        return self.__reduce_ex__(2)


_time_class = time
time.min = time(0, 0, 0)
time.max = time(23, 59, 59, 999999)
time.resolution = timedelta(microseconds=1)

class datetime(date):
    __doc__ = 'datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\n\n    The year, month and day arguments are required. tzinfo may be None, or an\n    instance of a tzinfo subclass. The remaining arguments may be ints.\n    '
    __slots__ = date.__slots__ + time.__slots__

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        if isinstance(year, bytes):
            if len(year) == 10:
                if 1 <= year[2] & 127 <= 12:
                    self = object.__new__(cls)
                    self._datetime__setstate(year, month)
                    self._hashcode = -1
                    return self
        year, month, day = _check_date_fields(year, month, day)
        hour, minute, second, microsecond, fold = _check_time_fields(hour, minute, second, microsecond, fold)
        _check_tzinfo_arg(tzinfo)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._hashcode = -1
        self._fold = fold
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

    @property
    def fold(self):
        return self._fold

    @classmethod
    def _fromtimestamp(cls, t, utc, tz):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        frac, t = _math.modf(t)
        us = round(frac * 1000000.0)
        if us >= 1000000:
            t += 1
            us -= 1000000
        else:
            if us < 0:
                t -= 1
                us += 1000000
            else:
                converter = _time.gmtime if utc else _time.localtime
                y, m, d, hh, mm, ss, weekday, jday, dst = converter(t)
                ss = min(ss, 59)
                result = cls(y, m, d, hh, mm, ss, us, tz)
                if tz is None:
                    max_fold_seconds = 86400
                    if t < max_fold_seconds:
                        if sys.platform.startswith('win'):
                            return result
                    y, m, d, hh, mm, ss = converter(t - max_fold_seconds)[:6]
                    probe1 = cls(y, m, d, hh, mm, ss, us, tz)
                    trans = result - probe1 - timedelta(0, max_fold_seconds)
                    if trans.days < 0:
                        y, m, d, hh, mm, ss = converter(t + trans // timedelta(0, 1))[:6]
                        probe2 = cls(y, m, d, hh, mm, ss, us, tz)
                        if probe2 == result:
                            result._fold = 1
                else:
                    result = tz.fromutc(result)
            return result

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        _check_tzinfo_arg(tz)
        return cls._fromtimestamp(t, tz is not None, tz)

    @classmethod
    def utcfromtimestamp(cls, t):
        """Construct a naive UTC datetime from a POSIX timestamp."""
        return cls._fromtimestamp(t, True, None)

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
    def combine(cls, date, time, tzinfo=True):
        """Construct a datetime from a given date and a given time."""
        if not isinstance(date, _date_class):
            raise TypeError('date argument must be a date instance')
        if not isinstance(time, _time_class):
            raise TypeError('time argument must be a time instance')
        if tzinfo is True:
            tzinfo = time.tzinfo
        return cls((date.year), (date.month), (date.day), (time.hour),
          (time.minute), (time.second), (time.microsecond), tzinfo,
          fold=(time.fold))

    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a datetime from the output of datetime.isoformat()."""
        if not isinstance(date_string, str):
            raise TypeError('fromisoformat: argument must be str')
        else:
            dstr = date_string[0:10]
            tstr = date_string[11:]
            try:
                date_components = _parse_isoformat_date(dstr)
            except ValueError:
                raise ValueError('Invalid isoformat string: %s' % date_string)

            if tstr:
                try:
                    time_components = _parse_isoformat_time(tstr)
                except ValueError:
                    raise ValueError('Invalid isoformat string: %s' % date_string)

            else:
                time_components = [
                 0, 0, 0, 0, None]
        return cls(*date_components + time_components)

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        dst = self.dst()
        if dst is None:
            dst = -1
        else:
            if dst:
                dst = 1
            else:
                dst = 0
        return _build_struct_time(self.year, self.month, self.day, self.hour, self.minute, self.second, dst)

    def _mktime(self):
        """Return integer POSIX timestamp."""
        epoch = datetime(1970, 1, 1)
        max_fold_seconds = 86400
        t = (self - epoch) // timedelta(0, 1)

        def local(u):
            y, m, d, hh, mm, ss = _time.localtime(u)[:6]
            return (datetime(y, m, d, hh, mm, ss) - epoch) // timedelta(0, 1)

        a = local(t) - t
        u1 = t - a
        t1 = local(u1)
        if t1 == t:
            u2 = u1 + (-max_fold_seconds, max_fold_seconds)[self.fold]
            b = local(u2) - u2
            if a == b:
                return u1
        else:
            b = t1 - u1
            assert a != b
        u2 = t - b
        t2 = local(u2)
        if t2 == t:
            return u2
        if t1 == t:
            return u1
        return (
         max, min)[self.fold](u1, u2)

    def timestamp(self):
        """Return POSIX timestamp as float"""
        if self._tzinfo is None:
            s = self._mktime()
            return s + self.microsecond / 1000000.0
        return (self - _EPOCH).total_seconds()

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
        return time((self.hour), (self.minute), (self.second), (self.microsecond), fold=(self.fold))

    def timetz(self):
        """Return the time part, with same tzinfo."""
        return time((self.hour), (self.minute), (self.second), (self.microsecond), (self._tzinfo),
          fold=(self.fold))

    def replace(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, tzinfo=True, *, fold=None):
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
        if fold is None:
            fold = self.fold
        return type(self)(year, month, day, hour, minute, second, microsecond,
          tzinfo, fold=fold)

    def _local_timezone(self):
        if self.tzinfo is None:
            ts = self._mktime()
        else:
            ts = (self - _EPOCH) // timedelta(seconds=1)
        localtm = _time.localtime(ts)
        local = datetime(*localtm[:6])
        try:
            gmtoff = localtm.tm_gmtoff
            zone = localtm.tm_zone
        except AttributeError:
            delta = local - datetime(*_time.gmtime(ts)[:6])
            zone = _time.strftime('%Z', localtm)
            tz = timezone(delta, zone)
        else:
            tz = timezone(timedelta(seconds=gmtoff), zone)
        return tz

    def astimezone(self, tz=None):
        if tz is None:
            tz = self._local_timezone()
        else:
            if not isinstance(tz, tzinfo):
                raise TypeError('tz argument must be an instance of tzinfo')
            else:
                mytz = self.tzinfo
                if mytz is None:
                    mytz = self._local_timezone()
                    myoffset = mytz.utcoffset(self)
                else:
                    myoffset = mytz.utcoffset(self)
                    if myoffset is None:
                        mytz = self.replace(tzinfo=None)._local_timezone()
                        myoffset = mytz.utcoffset(self)
            if tz is mytz:
                return self
            utc = (self - myoffset).replace(tzinfo=tz)
            return tz.fromutc(utc)

    def ctime(self):
        """Return ctime() style string."""
        weekday = self.toordinal() % 7 or 7
        return '%s %s %2d %02d:%02d:%02d %04d' % (
         _DAYNAMES[weekday],
         _MONTHNAMES[self._month],
         self._day,
         self._hour, self._minute, self._second,
         self._year)

    def isoformat(self, sep='T', timespec='auto'):
        """Return the time formatted according to ISO.

        The full format looks like 'YYYY-MM-DD HH:MM:SS.mmmmmm'.
        By default, the fractional part is omitted if self.microsecond == 0.

        If self.tzinfo is not None, the UTC offset is also attached, giving
        giving a full format of 'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM'.

        Optional argument sep specifies the separator between date and
        time, default 'T'.

        The optional argument timespec specifies the number of additional
        terms of the time to include.
        """
        s = '%04d-%02d-%02d%c' % (self._year, self._month, self._day, sep) + _format_time(self._hour, self._minute, self._second, self._microsecond, timespec)
        off = self.utcoffset()
        tz = _format_offset(off)
        if tz:
            s += tz
        return s

    def __repr__(self):
        """Convert to formal string, for repr()."""
        L = [
         self._year, self._month, self._day,
         self._hour, self._minute, self._second, self._microsecond]
        if L[(-1)] == 0:
            del L[-1]
        if L[(-1)] == 0:
            del L[-1]
        s = '%s.%s(%s)' % (self.__class__.__module__,
         self.__class__.__qualname__,
         ', '.join(map(str, L)))
        if self._tzinfo is not None:
            assert s[-1:] == ')'
            s = s[:-1] + ', tzinfo=%r' % self._tzinfo + ')'
        if self._fold:
            assert s[-1:] == ')'
            s = s[:-1] + ', fold=1)'
        return s

    def __str__(self):
        """Convert to string, for str()."""
        return self.isoformat(sep=' ')

    @classmethod
    def strptime(cls, date_string, format):
        """string, format -> new datetime parsed from a string (like time.strptime())."""
        import _strptime
        return _strptime._strptime_datetime(cls, date_string, format)

    def utcoffset(self):
        """Return the timezone offset as timedelta positive east of UTC (negative west of
        UTC)."""
        if self._tzinfo is None:
            return
        offset = self._tzinfo.utcoffset(self)
        _check_utc_offset('utcoffset', offset)
        return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        if self._tzinfo is None:
            return
        name = self._tzinfo.tzname(self)
        _check_tzname(name)
        return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (as timedelta
        positive eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return
        offset = self._tzinfo.dst(self)
        _check_utc_offset('dst', offset)
        return offset

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other, allow_mixed=True) == 0
        else:
            return isinstance(other, date) or NotImplemented
        return False

    def __le__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) <= 0
        else:
            return isinstance(other, date) or NotImplemented
        _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) < 0
        else:
            return isinstance(other, date) or NotImplemented
        _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) >= 0
        else:
            return isinstance(other, date) or NotImplemented
        _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) > 0
        else:
            return isinstance(other, date) or NotImplemented
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
            if allow_mixed:
                if myoff != self.replace(fold=(not self.fold)).utcoffset():
                    return 2
                if otoff != other.replace(fold=(not other.fold)).utcoffset():
                    return 2
            base_compare = myoff == otoff
        if base_compare:
            return _cmp((self._year, self._month, self._day,
             self._hour, self._minute, self._second,
             self._microsecond), (
             other._year, other._month, other._day,
             other._hour, other._minute, other._second,
             other._microsecond))
        if myoff is None or otoff is None:
            if allow_mixed:
                return 2
            raise TypeError('cannot compare naive and aware datetimes')
        diff = self - other
        if diff.days < 0:
            return -1
        return diff and 1 or 0

    def __add__(self, other):
        """Add a datetime and a timedelta."""
        if not isinstance(other, timedelta):
            return NotImplemented
        delta = timedelta((self.toordinal()), hours=(self._hour),
          minutes=(self._minute),
          seconds=(self._second),
          microseconds=(self._microsecond))
        delta += other
        hour, rem = divmod(delta.seconds, 3600)
        minute, second = divmod(rem, 60)
        if 0 < delta.days <= _MAXORDINAL:
            return datetime.combine(date.fromordinal(delta.days), time(hour, minute, second, (delta.microseconds),
              tzinfo=(self._tzinfo)))
        raise OverflowError('result out of range')

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
        myoff = self.utcoffset()
        otoff = other.utcoffset()
        if myoff == otoff:
            return base
        if myoff is None or otoff is None:
            raise TypeError('cannot mix naive and timezone-aware time')
        return base + otoff - myoff

    def __hash__(self):
        if self._hashcode == -1:
            if self.fold:
                t = self.replace(fold=0)
            else:
                t = self
            tzoff = t.utcoffset()
            if tzoff is None:
                self._hashcode = hash(t._getstate()[0])
            else:
                days = _ymd2ord(self.year, self.month, self.day)
                seconds = self.hour * 3600 + self.minute * 60 + self.second
                self._hashcode = hash(timedelta(days, seconds, self.microsecond) - tzoff)
        return self._hashcode

    def _getstate(self, protocol=3):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        m = self._month
        if self._fold:
            if protocol > 3:
                m += 128
        basestate = bytes([yhi, ylo, m, self._day,
         self._hour, self._minute, self._second,
         us1, us2, us3])
        if self._tzinfo is None:
            return (
             basestate,)
        return (basestate, self._tzinfo)

    def __setstate(self, string, tzinfo):
        if tzinfo is not None:
            if not isinstance(tzinfo, _tzinfo_class):
                raise TypeError('bad tzinfo state arg')
        else:
            yhi, ylo, m, self._day, self._hour, self._minute, self._second, us1, us2, us3 = string
            if m > 127:
                self._fold = 1
                self._month = m - 128
            else:
                self._fold = 0
            self._month = m
        self._year = yhi * 256 + ylo
        self._microsecond = (us1 << 8 | us2) << 8 | us3
        self._tzinfo = tzinfo

    def __reduce_ex__(self, protocol):
        return (
         self.__class__, self._getstate(protocol))

    def __reduce__(self):
        return self.__reduce_ex__(2)


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
            raise TypeError('offset must be a timedelta')
        else:
            if name is cls._Omitted:
                if not offset:
                    return cls.utc
                    name = None
                else:
                    pass
            if not isinstance(name, str):
                raise TypeError('name must be a string')
        if not cls._minoffset <= offset <= cls._maxoffset:
            raise ValueError('offset must be a timedelta strictly between -timedelta(hours=24) and timedelta(hours=24).')
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
            return (
             self._offset,)
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
            return 'datetime.timezone.utc'
        if self._name is None:
            return '%s.%s(%r)' % (self.__class__.__module__,
             self.__class__.__qualname__,
             self._offset)
        return '%s.%s(%r, %r)' % (self.__class__.__module__,
         self.__class__.__qualname__,
         self._offset, self._name)

    def __str__(self):
        return self.tzname(None)

    def utcoffset(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return self._offset
        raise TypeError('utcoffset() argument must be a datetime instance or None')

    def tzname(self, dt):
        if isinstance(dt, datetime) or dt is None:
            if self._name is None:
                return self._name_from_offset(self._offset)
            return self._name
        raise TypeError('tzname() argument must be a datetime instance or None')

    def dst(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return
        raise TypeError('dst() argument must be a datetime instance or None')

    def fromutc(self, dt):
        if isinstance(dt, datetime):
            if dt.tzinfo is not self:
                raise ValueError('fromutc: dt.tzinfo is not self')
            return dt + self._offset
        raise TypeError('fromutc() argument must be a datetime instance or None')

    _maxoffset = timedelta(hours=23, minutes=59)
    _minoffset = -_maxoffset

    @staticmethod
    def _name_from_offset(delta):
        if not delta:
            return 'UTC'
        elif delta < timedelta(0):
            sign = '-'
            delta = -delta
        else:
            sign = '+'
        hours, rest = divmod(delta, timedelta(hours=1))
        minutes, rest = divmod(rest, timedelta(minutes=1))
        seconds = rest.seconds
        microseconds = rest.microseconds
        if microseconds:
            return f"UTC{sign}{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"
        if seconds:
            return f"UTC{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"UTC{sign}{hours:02d}:{minutes:02d}"


timezone.utc = timezone._create(timedelta(0))
timezone.min = timezone._create(timezone._minoffset)
timezone.max = timezone._create(timezone._maxoffset)
_EPOCH = datetime(1970, 1, 1, tzinfo=(timezone.utc))
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
    del _EPOCH
    del _MAXORDINAL
    del _MONTHNAMES
    del _build_struct_time
    del _check_date_fields
    del _check_int_field
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
    del _format_offset
    del _is_leap
    del _isoweek1monday
    del _math
    del _ord2ymd
    del _time
    del _time_class
    del _tzinfo_class
    del _wrap_strftime
    del _ymd2ord
    del _divide_and_round
    del _parse_isoformat_date
    del _parse_isoformat_time
    del _parse_hh_mm_ss_ff
    from _datetime import __doc__