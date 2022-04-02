# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: _strptime.py
"""Strptime-related classes and functions.

CLASSES:
    LocaleTime -- Discovers and stores locale-specific time information
    TimeRE -- Creates regexes for pattern matching a string of text containing
                time information

FUNCTIONS:
    _getlang -- Figure out what language is being used for the locale
    strptime -- Calculates the time struct represented by the passed-in string

"""
import time, locale, calendar
from re import compile as re_compile
from re import IGNORECASE
from re import escape as re_escape
from datetime import date as datetime_date, timedelta as datetime_timedelta, timezone as datetime_timezone
from _thread import allocate_lock as _thread_allocate_lock
__all__ = []

def _getlang():
    return locale.getlocale(locale.LC_TIME)


class LocaleTime(object):
    __doc__ = 'Stores and handles locale-specific information related to time.\n\n    ATTRIBUTES:\n        f_weekday -- full weekday names (7-item list)\n        a_weekday -- abbreviated weekday names (7-item list)\n        f_month -- full month names (13-item list; dummy value in [0], which\n                    is added by code)\n        a_month -- abbreviated month names (13-item list, dummy value in\n                    [0], which is added by code)\n        am_pm -- AM/PM representation (2-item list)\n        LC_date_time -- format string for date/time representation (string)\n        LC_date -- format string for date representation (string)\n        LC_time -- format string for time representation (string)\n        timezone -- daylight- and non-daylight-savings timezone representation\n                    (2-item list of sets)\n        lang -- Language used by instance (2-item tuple)\n    '

    def __init__(self):
        """Set all attributes.

        Order of methods called matters for dependency reasons.

        The locale language is set at the offset and then checked again before
        exiting.  This is to make sure that the attributes were not set with a
        mix of information from more than one locale.  This would most likely
        happen when using threads where one thread calls a locale-dependent
        function while another thread changes the locale while the function in
        the other thread is still running.  Proper coding would call for
        locks to prevent changing the locale while locale-dependent code is
        running.  The check here is done in case someone does not think about
        doing this.

        Only other possible issue is if someone changed the timezone and did
        not call tz.tzset .  That is an issue for the programmer, though,
        since changing the timezone is worthless without that call.

        """
        self.lang = _getlang()
        self._LocaleTime__calc_weekday()
        self._LocaleTime__calc_month()
        self._LocaleTime__calc_am_pm()
        self._LocaleTime__calc_timezone()
        self._LocaleTime__calc_date_time()
        if _getlang() != self.lang:
            raise ValueError('locale changed during initialization')
        if time.tzname != self.tzname or (time.daylight != self.daylight):
            raise ValueError('timezone changed during initialization')

    def __calc_weekday(self):
        a_weekday = [calendar.day_abbr[i].lower() for i in range(7)]
        f_weekday = [calendar.day_name[i].lower() for i in range(7)]
        self.a_weekday = a_weekday
        self.f_weekday = f_weekday

    def __calc_month(self):
        a_month = [calendar.month_abbr[i].lower() for i in range(13)]
        f_month = [calendar.month_name[i].lower() for i in range(13)]
        self.a_month = a_month
        self.f_month = f_month

    def __calc_am_pm(self):
        am_pm = []
        for hour in (1, 22):
            time_tuple = time.struct_time((1999, 3, 17, hour, 44, 55, 2, 76, 0))
            am_pm.append(time.strftime('%p', time_tuple).lower())
        else:
            self.am_pm = am_pm

    def __calc_date_time--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              struct_time
                4  LOAD_CONST               (1999, 3, 17, 22, 44, 55, 2, 76, 0)
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'time_tuple'

 L. 116        10  BUILD_LIST_0          0 
               12  LOAD_CONST               (None, None, None)
               14  CALL_FINALLY         17  'to 17'
               16  STORE_FAST               'date_time'

 L. 117        18  LOAD_GLOBAL              time
               20  LOAD_METHOD              strftime
               22  LOAD_STR                 '%c'
               24  LOAD_FAST                'time_tuple'
               26  CALL_METHOD_2         2  ''
               28  LOAD_METHOD              lower
               30  CALL_METHOD_0         0  ''
               32  LOAD_FAST                'date_time'
               34  LOAD_CONST               0
               36  STORE_SUBSCR     

 L. 118        38  LOAD_GLOBAL              time
               40  LOAD_METHOD              strftime
               42  LOAD_STR                 '%x'
               44  LOAD_FAST                'time_tuple'
               46  CALL_METHOD_2         2  ''
               48  LOAD_METHOD              lower
               50  CALL_METHOD_0         0  ''
               52  LOAD_FAST                'date_time'
               54  LOAD_CONST               1
               56  STORE_SUBSCR     

 L. 119        58  LOAD_GLOBAL              time
               60  LOAD_METHOD              strftime
               62  LOAD_STR                 '%X'
               64  LOAD_FAST                'time_tuple'
               66  CALL_METHOD_2         2  ''
               68  LOAD_METHOD              lower
               70  CALL_METHOD_0         0  ''
               72  LOAD_FAST                'date_time'
               74  LOAD_CONST               2
               76  STORE_SUBSCR     

 L. 120        78  LOAD_CONST               ('%', '%%')
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                f_weekday
               84  LOAD_CONST               2
               86  BINARY_SUBSCR    
               88  LOAD_STR                 '%A'
               90  BUILD_TUPLE_2         2 

 L. 121        92  LOAD_FAST                'self'
               94  LOAD_ATTR                f_month
               96  LOAD_CONST               3
               98  BINARY_SUBSCR    
              100  LOAD_STR                 '%B'
              102  BUILD_TUPLE_2         2 
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                a_weekday
              108  LOAD_CONST               2
              110  BINARY_SUBSCR    
              112  LOAD_STR                 '%a'
              114  BUILD_TUPLE_2         2 

 L. 122       116  LOAD_FAST                'self'
              118  LOAD_ATTR                a_month
              120  LOAD_CONST               3
              122  BINARY_SUBSCR    
              124  LOAD_STR                 '%b'
              126  BUILD_TUPLE_2         2 
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                am_pm
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  LOAD_STR                 '%p'
              138  BUILD_TUPLE_2         2 

 L. 123       140  LOAD_CONST               ('1999', '%Y')
              142  LOAD_CONST               ('99', '%y')
              144  LOAD_CONST               ('22', '%H')

 L. 124       146  LOAD_CONST               ('44', '%M')
              148  LOAD_CONST               ('55', '%S')
              150  LOAD_CONST               ('76', '%j')

 L. 125       152  LOAD_CONST               ('17', '%d')
              154  LOAD_CONST               ('03', '%m')
              156  LOAD_CONST               ('3', '%m')

 L. 127       158  LOAD_CONST               ('2', '%w')
              160  LOAD_CONST               ('10', '%I')

 L. 120       162  BUILD_LIST_17        17 
              164  STORE_FAST               'replacement_pairs'

 L. 128       166  LOAD_FAST                'replacement_pairs'
              168  LOAD_METHOD              extend
              170  LOAD_LISTCOMP            '<code_object <listcomp>>'
              172  LOAD_STR                 'LocaleTime.__calc_date_time.<locals>.<listcomp>'
              174  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                timezone
              180  GET_ITER         
              182  CALL_FUNCTION_1       1  ''
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 130       188  LOAD_CONST               ((0, '%c'), (1, '%x'), (2, '%X'))
              190  GET_ITER         
            192_0  COME_FROM           292  '292'
              192  FOR_ITER            294  'to 294'
              194  UNPACK_SEQUENCE_2     2 
              196  STORE_FAST               'offset'
              198  STORE_FAST               'directive'

 L. 131       200  LOAD_FAST                'date_time'
              202  LOAD_FAST                'offset'
              204  BINARY_SUBSCR    
              206  STORE_FAST               'current_format'

 L. 132       208  LOAD_FAST                'replacement_pairs'
              210  GET_ITER         
            212_0  COME_FROM           236  '236'
            212_1  COME_FROM           222  '222'
              212  FOR_ITER            238  'to 238'
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'old'
              218  STORE_FAST               'new'

 L. 137       220  LOAD_FAST                'old'
              222  POP_JUMP_IF_FALSE_BACK   212  'to 212'

 L. 138       224  LOAD_FAST                'current_format'
              226  LOAD_METHOD              replace
              228  LOAD_FAST                'old'
              230  LOAD_FAST                'new'
              232  CALL_METHOD_2         2  ''
              234  STORE_FAST               'current_format'
              236  JUMP_BACK           212  'to 212'
            238_0  COME_FROM           212  '212'

 L. 142       238  LOAD_GLOBAL              time
              240  LOAD_METHOD              struct_time
              242  LOAD_CONST               (1999, 1, 3, 1, 1, 1, 6, 3, 0)
              244  CALL_METHOD_1         1  ''
              246  STORE_FAST               'time_tuple'

 L. 143       248  LOAD_STR                 '00'
              250  LOAD_GLOBAL              time
              252  LOAD_METHOD              strftime
              254  LOAD_FAST                'directive'
              256  LOAD_FAST                'time_tuple'
              258  CALL_METHOD_2         2  ''
              260  <118>                 0  ''
          262_264  POP_JUMP_IF_FALSE   272  'to 272'

 L. 144       266  LOAD_STR                 '%W'
              268  STORE_FAST               'U_W'
              270  JUMP_FORWARD        276  'to 276'
            272_0  COME_FROM           262  '262'

 L. 146       272  LOAD_STR                 '%U'
              274  STORE_FAST               'U_W'
            276_0  COME_FROM           270  '270'

 L. 147       276  LOAD_FAST                'current_format'
              278  LOAD_METHOD              replace
              280  LOAD_STR                 '11'
              282  LOAD_FAST                'U_W'
              284  CALL_METHOD_2         2  ''
              286  LOAD_FAST                'date_time'
              288  LOAD_FAST                'offset'
              290  STORE_SUBSCR     
              292  JUMP_BACK           192  'to 192'
            294_0  COME_FROM           192  '192'

 L. 148       294  LOAD_FAST                'date_time'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  LOAD_FAST                'self'
              302  STORE_ATTR               LC_date_time

 L. 149       304  LOAD_FAST                'date_time'
              306  LOAD_CONST               1
              308  BINARY_SUBSCR    
              310  LOAD_FAST                'self'
              312  STORE_ATTR               LC_date

 L. 150       314  LOAD_FAST                'date_time'
              316  LOAD_CONST               2
              318  BINARY_SUBSCR    
              320  LOAD_FAST                'self'
              322  STORE_ATTR               LC_time

Parse error at or near `CALL_FINALLY' instruction at offset 14

    def __calc_timezone--- This code section failed: ---

 L. 156         0  SETUP_FINALLY        14  'to 14'

 L. 157         2  LOAD_GLOBAL              time
                4  LOAD_METHOD              tzset
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         32  'to 32'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 158        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  <121>                30  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 159        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
               30  <48>             
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM            12  '12'

 L. 160        32  LOAD_GLOBAL              time
               34  LOAD_ATTR                tzname
               36  LOAD_FAST                'self'
               38  STORE_ATTR               tzname

 L. 161        40  LOAD_GLOBAL              time
               42  LOAD_ATTR                daylight
               44  LOAD_FAST                'self'
               46  STORE_ATTR               daylight

 L. 162        48  LOAD_GLOBAL              frozenset
               50  LOAD_STR                 'utc'
               52  LOAD_STR                 'gmt'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                tzname
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  ''
               66  BUILD_SET_3           3 
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'no_saving'

 L. 163        72  LOAD_FAST                'self'
               74  LOAD_ATTR                daylight
               76  POP_JUMP_IF_FALSE   100  'to 100'

 L. 164        78  LOAD_GLOBAL              frozenset
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                tzname
               84  LOAD_CONST               1
               86  BINARY_SUBSCR    
               88  LOAD_METHOD              lower
               90  CALL_METHOD_0         0  ''
               92  BUILD_SET_1           1 
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'has_saving'
               98  JUMP_FORWARD        106  'to 106'
            100_0  COME_FROM            76  '76'

 L. 166       100  LOAD_GLOBAL              frozenset
              102  CALL_FUNCTION_0       0  ''
              104  STORE_FAST               'has_saving'
            106_0  COME_FROM            98  '98'

 L. 167       106  LOAD_FAST                'no_saving'
              108  LOAD_FAST                'has_saving'
              110  BUILD_TUPLE_2         2 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               timezone

Parse error at or near `<121>' instruction at offset 18


class TimeRE(dict):
    __doc__ = 'Handle conversion from format directives to regexes.'

    def __init__(self, locale_time=None):
        """Create keys/values.

        Order of execution is important for dependency reasons.

        """
        if locale_time:
            self.locale_time = locale_time
        else:
            self.locale_time = LocaleTime()
        base = super()
        base.__init__({'d':'(?P<d>3[0-1]|[1-2]\\d|0[1-9]|[1-9]| [1-9])', 
         'f':'(?P<f>[0-9]{1,6})', 
         'H':'(?P<H>2[0-3]|[0-1]\\d|\\d)', 
         'I':'(?P<I>1[0-2]|0[1-9]|[1-9])', 
         'G':'(?P<G>\\d\\d\\d\\d)', 
         'j':'(?P<j>36[0-6]|3[0-5]\\d|[1-2]\\d\\d|0[1-9]\\d|00[1-9]|[1-9]\\d|0[1-9]|[1-9])', 
         'm':'(?P<m>1[0-2]|0[1-9]|[1-9])', 
         'M':'(?P<M>[0-5]\\d|\\d)', 
         'S':'(?P<S>6[0-1]|[0-5]\\d|\\d)', 
         'U':'(?P<U>5[0-3]|[0-4]\\d|\\d)', 
         'w':'(?P<w>[0-6])', 
         'u':'(?P<u>[1-7])', 
         'V':'(?P<V>5[0-3]|0[1-9]|[1-4]\\d|\\d)', 
         'y':'(?P<y>\\d\\d)', 
         'Y':'(?P<Y>\\d\\d\\d\\d)', 
         'z':'(?P<z>[+-]\\d\\d:?[0-5]\\d(:?[0-5]\\d(\\.\\d{1,6})?)?|Z)', 
         'A':self._TimeRE__seqToRE(self.locale_time.f_weekday, 'A'), 
         'a':self._TimeRE__seqToRE(self.locale_time.a_weekday, 'a'), 
         'B':self._TimeRE__seqToRE(self.locale_time.f_month[1:], 'B'), 
         'b':self._TimeRE__seqToRE(self.locale_time.a_month[1:], 'b'), 
         'p':self._TimeRE__seqToRE(self.locale_time.am_pm, 'p'), 
         'Z':self._TimeRE__seqToRE((tz for tz_names in self.locale_time.timezone for tz in tz_names), 'Z'), 
         '%':'%'})
        base.__setitem__('W', base.__getitem__('U').replace('U', 'W'))
        base.__setitem__('c', self.pattern(self.locale_time.LC_date_time))
        base.__setitem__('x', self.pattern(self.locale_time.LC_date))
        base.__setitem__('X', self.pattern(self.locale_time.LC_time))

    def __seqToRE--- This code section failed: ---

 L. 228         0  LOAD_GLOBAL              sorted
                2  LOAD_FAST                'to_convert'
                4  LOAD_GLOBAL              len
                6  LOAD_CONST               True
                8  LOAD_CONST               ('key', 'reverse')
               10  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               12  STORE_FAST               'to_convert'

 L. 229        14  LOAD_FAST                'to_convert'
               16  GET_ITER         
             18_0  COME_FROM            34  '34'
             18_1  COME_FROM            28  '28'
               18  FOR_ITER             36  'to 36'
               20  STORE_FAST               'value'

 L. 230        22  LOAD_FAST                'value'
               24  LOAD_STR                 ''
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 231        30  POP_TOP          
               32  BREAK_LOOP           40  'to 40'
               34  JUMP_BACK            18  'to 18'
             36_0  COME_FROM            18  '18'

 L. 233        36  LOAD_STR                 ''
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'

 L. 234        40  LOAD_STR                 '|'
               42  LOAD_METHOD              join
               44  LOAD_GENEXPR             '<code_object <genexpr>>'
               46  LOAD_STR                 'TimeRE.__seqToRE.<locals>.<genexpr>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_FAST                'to_convert'
               52  GET_ITER         
               54  CALL_FUNCTION_1       1  ''
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'regex'

 L. 235        60  LOAD_STR                 '(?P<%s>%s'
               62  LOAD_FAST                'directive'
               64  LOAD_FAST                'regex'
               66  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               70  STORE_FAST               'regex'

 L. 236        72  LOAD_STR                 '%s)'
               74  LOAD_FAST                'regex'
               76  BINARY_MODULO    
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 78

    def pattern--- This code section failed: ---

 L. 245         0  LOAD_STR                 ''
                2  STORE_FAST               'processed_format'

 L. 249         4  LOAD_GLOBAL              re_compile
                6  LOAD_STR                 '([\\\\.^$*+?\\(\\){}\\[\\]|])'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'regex_chars'

 L. 250        12  LOAD_FAST                'regex_chars'
               14  LOAD_METHOD              sub
               16  LOAD_STR                 '\\\\\\1'
               18  LOAD_FAST                'format'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'format'

 L. 251        24  LOAD_GLOBAL              re_compile
               26  LOAD_STR                 '\\s+'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'whitespace_replacement'

 L. 252        32  LOAD_FAST                'whitespace_replacement'
               34  LOAD_METHOD              sub
               36  LOAD_STR                 '\\\\s+'
               38  LOAD_FAST                'format'
               40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'format'
             44_0  COME_FROM           116  '116'

 L. 253        44  LOAD_STR                 '%'
               46  LOAD_FAST                'format'
               48  <118>                 0  ''
               50  POP_JUMP_IF_FALSE   118  'to 118'

 L. 254        52  LOAD_FAST                'format'
               54  LOAD_METHOD              index
               56  LOAD_STR                 '%'
               58  CALL_METHOD_1         1  ''
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  STORE_FAST               'directive_index'

 L. 255        66  LOAD_STR                 '%s%s%s'
               68  LOAD_FAST                'processed_format'

 L. 256        70  LOAD_FAST                'format'
               72  LOAD_CONST               None
               74  LOAD_FAST                'directive_index'
               76  LOAD_CONST               1
               78  BINARY_SUBTRACT  
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    

 L. 257        84  LOAD_FAST                'self'
               86  LOAD_FAST                'format'
               88  LOAD_FAST                'directive_index'
               90  BINARY_SUBSCR    
               92  BINARY_SUBSCR    

 L. 255        94  BUILD_TUPLE_3         3 
               96  BINARY_MODULO    
               98  STORE_FAST               'processed_format'

 L. 258       100  LOAD_FAST                'format'
              102  LOAD_FAST                'directive_index'
              104  LOAD_CONST               1
              106  BINARY_ADD       
              108  LOAD_CONST               None
              110  BUILD_SLICE_2         2 
              112  BINARY_SUBSCR    
              114  STORE_FAST               'format'
              116  JUMP_BACK            44  'to 44'
            118_0  COME_FROM            50  '50'

 L. 259       118  LOAD_STR                 '%s%s'
              120  LOAD_FAST                'processed_format'
              122  LOAD_FAST                'format'
              124  BUILD_TUPLE_2         2 
              126  BINARY_MODULO    
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 48

    def compile(self, format):
        """Return a compiled re object for the format string."""
        return re_compile(self.pattern(format), IGNORECASE)


_cache_lock = _thread_allocate_lock()
_TimeRE_cache = TimeRE()
_CACHE_MAX_SIZE = 5
_regex_cache = {}

def _calc_julian_from_U_or_W(year, week_of_year, day_of_week, week_starts_Mon):
    """Calculate the Julian day based on the year, week of the year, and day of
    the week, with week_start_day representing whether the week of the year
    assumes the week starts on Sunday or Monday (6 or 0)."""
    first_weekday = datetime_date(year, 1, 1).weekday()
    if not week_starts_Mon:
        first_weekday = (first_weekday + 1) % 7
        day_of_week = (day_of_week + 1) % 7
    week_0_length = (7 - first_weekday) % 7
    if week_of_year == 0:
        return 1 + day_of_week - first_weekday
    days_to_week = week_0_length + 7 * (week_of_year - 1)
    return 1 + days_to_week + day_of_week


def _calc_julian_from_V(iso_year, iso_week, iso_weekday):
    """Calculate the Julian day based on the ISO 8601 year, week, and weekday.
    ISO weeks start on Mondays, with week 01 being the week containing 4 Jan.
    ISO week days range from 1 (Monday) to 7 (Sunday).
    """
    correction = datetime_date(iso_year, 1, 4).isoweekday() + 3
    ordinal = iso_week * 7 + iso_weekday - correction
    if ordinal < 1:
        ordinal += datetime_date(iso_year, 1, 1).toordinal()
        iso_year -= 1
        ordinal -= datetime_date(iso_year, 1, 1).toordinal()
    return (iso_year, ordinal)


def _strptime--- This code section failed: ---

 L. 314         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'data_string'
                4  LOAD_FAST                'format'
                6  BUILD_LIST_2          2 
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM            54  '54'
             12_1  COME_FROM            28  '28'
               12  FOR_ITER             56  'to 56'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'index'
               18  STORE_FAST               'arg'

 L. 315        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'arg'
               24  LOAD_GLOBAL              str
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE_BACK    12  'to 12'

 L. 316        30  LOAD_STR                 'strptime() argument {} must be str, not {}'
               32  STORE_FAST               'msg'

 L. 317        34  LOAD_GLOBAL              TypeError
               36  LOAD_FAST                'msg'
               38  LOAD_METHOD              format
               40  LOAD_FAST                'index'
               42  LOAD_GLOBAL              type
               44  LOAD_FAST                'arg'
               46  CALL_FUNCTION_1       1  ''
               48  CALL_METHOD_2         2  ''
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_BACK            12  'to 12'
             56_0  COME_FROM            12  '12'

 L. 320        56  LOAD_GLOBAL              _cache_lock
               58  SETUP_WITH          308  'to 308'
               60  POP_TOP          

 L. 321        62  LOAD_GLOBAL              _TimeRE_cache
               64  LOAD_ATTR                locale_time
               66  STORE_FAST               'locale_time'

 L. 322        68  LOAD_GLOBAL              _getlang
               70  CALL_FUNCTION_0       0  ''
               72  LOAD_FAST                'locale_time'
               74  LOAD_ATTR                lang
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_TRUE    104  'to 104'

 L. 323        80  LOAD_GLOBAL              time
               82  LOAD_ATTR                tzname
               84  LOAD_FAST                'locale_time'
               86  LOAD_ATTR                tzname
               88  COMPARE_OP               !=

 L. 322        90  POP_JUMP_IF_TRUE    104  'to 104'

 L. 324        92  LOAD_GLOBAL              time
               94  LOAD_ATTR                daylight
               96  LOAD_FAST                'locale_time'
               98  LOAD_ATTR                daylight
              100  COMPARE_OP               !=

 L. 322       102  POP_JUMP_IF_FALSE   124  'to 124'
            104_0  COME_FROM            90  '90'
            104_1  COME_FROM            78  '78'

 L. 325       104  LOAD_GLOBAL              TimeRE
              106  CALL_FUNCTION_0       0  ''
              108  STORE_GLOBAL             _TimeRE_cache

 L. 326       110  LOAD_GLOBAL              _regex_cache
              112  LOAD_METHOD              clear
              114  CALL_METHOD_0         0  ''
              116  POP_TOP          

 L. 327       118  LOAD_GLOBAL              _TimeRE_cache
              120  LOAD_ATTR                locale_time
              122  STORE_FAST               'locale_time'
            124_0  COME_FROM           102  '102'

 L. 328       124  LOAD_GLOBAL              len
              126  LOAD_GLOBAL              _regex_cache
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_GLOBAL              _CACHE_MAX_SIZE
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L. 329       136  LOAD_GLOBAL              _regex_cache
              138  LOAD_METHOD              clear
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          
            144_0  COME_FROM           134  '134'

 L. 330       144  LOAD_GLOBAL              _regex_cache
              146  LOAD_METHOD              get
              148  LOAD_FAST                'format'
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'format_regex'

 L. 331       154  LOAD_FAST                'format_regex'
          156_158  POP_JUMP_IF_TRUE    294  'to 294'

 L. 332       160  SETUP_FINALLY       176  'to 176'

 L. 333       162  LOAD_GLOBAL              _TimeRE_cache
              164  LOAD_METHOD              compile
              166  LOAD_FAST                'format'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'format_regex'
              172  POP_BLOCK        
              174  JUMP_FORWARD        286  'to 286'
            176_0  COME_FROM_FINALLY   160  '160'

 L. 336       176  DUP_TOP          
              178  LOAD_GLOBAL              KeyError
              180  <121>               252  ''
              182  POP_TOP          
              184  STORE_FAST               'err'
              186  POP_TOP          
              188  SETUP_FINALLY       244  'to 244'

 L. 337       190  LOAD_FAST                'err'
              192  LOAD_ATTR                args
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  STORE_FAST               'bad_directive'

 L. 338       200  LOAD_FAST                'bad_directive'
              202  LOAD_STR                 '\\'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   212  'to 212'

 L. 339       208  LOAD_STR                 '%'
              210  STORE_FAST               'bad_directive'
            212_0  COME_FROM           206  '206'

 L. 340       212  DELETE_FAST              'err'

 L. 341       214  LOAD_GLOBAL              ValueError
              216  LOAD_STR                 "'%s' is a bad directive in format '%s'"

 L. 342       218  LOAD_FAST                'bad_directive'
              220  LOAD_FAST                'format'
              222  BUILD_TUPLE_2         2 

 L. 341       224  BINARY_MODULO    
              226  CALL_FUNCTION_1       1  ''

 L. 342       228  LOAD_CONST               None

 L. 341       230  RAISE_VARARGS_2       2  'exception instance with __cause__'
              232  POP_BLOCK        
              234  POP_EXCEPT       
              236  LOAD_CONST               None
              238  STORE_FAST               'err'
              240  DELETE_FAST              'err'
              242  JUMP_FORWARD        286  'to 286'
            244_0  COME_FROM_FINALLY   188  '188'
              244  LOAD_CONST               None
              246  STORE_FAST               'err'
              248  DELETE_FAST              'err'
              250  <48>             

 L. 344       252  DUP_TOP          
              254  LOAD_GLOBAL              IndexError
          256_258  <121>               284  ''
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 345       266  LOAD_GLOBAL              ValueError
              268  LOAD_STR                 "stray %% in format '%s'"
              270  LOAD_FAST                'format'
              272  BINARY_MODULO    
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_CONST               None
              278  RAISE_VARARGS_2       2  'exception instance with __cause__'
              280  POP_EXCEPT       
              282  JUMP_FORWARD        286  'to 286'
              284  <48>             
            286_0  COME_FROM           282  '282'
            286_1  COME_FROM           242  '242'
            286_2  COME_FROM           174  '174'

 L. 346       286  LOAD_FAST                'format_regex'
              288  LOAD_GLOBAL              _regex_cache
              290  LOAD_FAST                'format'
              292  STORE_SUBSCR     
            294_0  COME_FROM           156  '156'
              294  POP_BLOCK        
              296  LOAD_CONST               None
              298  DUP_TOP          
              300  DUP_TOP          
              302  CALL_FUNCTION_3       3  ''
              304  POP_TOP          
              306  JUMP_FORWARD        326  'to 326'
            308_0  COME_FROM_WITH       58  '58'
              308  <49>             
          310_312  POP_JUMP_IF_TRUE    316  'to 316'
              314  <48>             
            316_0  COME_FROM           310  '310'
              316  POP_TOP          
              318  POP_TOP          
              320  POP_TOP          
              322  POP_EXCEPT       
              324  POP_TOP          
            326_0  COME_FROM           306  '306'

 L. 347       326  LOAD_FAST                'format_regex'
              328  LOAD_METHOD              match
              330  LOAD_FAST                'data_string'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'found'

 L. 348       336  LOAD_FAST                'found'
          338_340  POP_JUMP_IF_TRUE    358  'to 358'

 L. 349       342  LOAD_GLOBAL              ValueError
              344  LOAD_STR                 'time data %r does not match format %r'

 L. 350       346  LOAD_FAST                'data_string'
              348  LOAD_FAST                'format'
              350  BUILD_TUPLE_2         2 

 L. 349       352  BINARY_MODULO    
              354  CALL_FUNCTION_1       1  ''
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           338  '338'

 L. 351       358  LOAD_GLOBAL              len
              360  LOAD_FAST                'data_string'
              362  CALL_FUNCTION_1       1  ''
              364  LOAD_FAST                'found'
              366  LOAD_METHOD              end
              368  CALL_METHOD_0         0  ''
              370  COMPARE_OP               !=
          372_374  POP_JUMP_IF_FALSE   400  'to 400'

 L. 352       376  LOAD_GLOBAL              ValueError
              378  LOAD_STR                 'unconverted data remains: %s'

 L. 353       380  LOAD_FAST                'data_string'
              382  LOAD_FAST                'found'
              384  LOAD_METHOD              end
              386  CALL_METHOD_0         0  ''
              388  LOAD_CONST               None
              390  BUILD_SLICE_2         2 
              392  BINARY_SUBSCR    

 L. 352       394  BINARY_MODULO    
              396  CALL_FUNCTION_1       1  ''
              398  RAISE_VARARGS_1       1  'exception instance'
            400_0  COME_FROM           372  '372'

 L. 355       400  LOAD_CONST               None
              402  DUP_TOP          
              404  STORE_FAST               'iso_year'
              406  STORE_FAST               'year'

 L. 356       408  LOAD_CONST               1
              410  DUP_TOP          
              412  STORE_FAST               'month'
              414  STORE_FAST               'day'

 L. 357       416  LOAD_CONST               0
              418  DUP_TOP          
              420  STORE_FAST               'hour'
              422  DUP_TOP          
              424  STORE_FAST               'minute'
              426  DUP_TOP          
              428  STORE_FAST               'second'
              430  STORE_FAST               'fraction'

 L. 358       432  LOAD_CONST               -1
              434  STORE_FAST               'tz'

 L. 359       436  LOAD_CONST               None
              438  STORE_FAST               'gmtoff'

 L. 360       440  LOAD_CONST               0
              442  STORE_FAST               'gmtoff_fraction'

 L. 363       444  LOAD_CONST               None
              446  DUP_TOP          
              448  STORE_FAST               'iso_week'
              450  STORE_FAST               'week_of_year'

 L. 364       452  LOAD_CONST               None
              454  STORE_FAST               'week_of_year_start'

 L. 367       456  LOAD_CONST               None
              458  DUP_TOP          
              460  STORE_FAST               'weekday'
              462  STORE_FAST               'julian'

 L. 368       464  LOAD_FAST                'found'
              466  LOAD_METHOD              groupdict
              468  CALL_METHOD_0         0  ''
              470  STORE_FAST               'found_dict'

 L. 369       472  LOAD_FAST                'found_dict'
              474  LOAD_METHOD              keys
              476  CALL_METHOD_0         0  ''
              478  GET_ITER         
            480_0  COME_FROM          1604  '1604'
            480_1  COME_FROM          1596  '1596'
            480_2  COME_FROM          1584  '1584'
            480_3  COME_FROM          1498  '1498'
            480_4  COME_FROM          1490  '1490'
            480_5  COME_FROM          1198  '1198'
            480_6  COME_FROM          1172  '1172'
            480_7  COME_FROM          1166  '1166'
            480_8  COME_FROM          1126  '1126'
            480_9  COME_FROM          1100  '1100'
           480_10  COME_FROM          1066  '1066'
           480_11  COME_FROM          1056  '1056'
           480_12  COME_FROM          1016  '1016'
           480_13  COME_FROM           982  '982'
           480_14  COME_FROM           948  '948'
           480_15  COME_FROM           898  '898'
           480_16  COME_FROM           872  '872'
           480_17  COME_FROM           846  '846'
           480_18  COME_FROM           810  '810'
           480_19  COME_FROM           734  '734'
           480_20  COME_FROM           708  '708'
           480_21  COME_FROM           682  '682'
           480_22  COME_FROM           648  '648'
           480_23  COME_FROM           614  '614'
           480_24  COME_FROM           588  '588'
           480_25  COME_FROM           562  '562'
           480_26  COME_FROM           536  '536'
           480_27  COME_FROM           526  '526'
          480_482  FOR_ITER           1608  'to 1608'
              484  STORE_FAST               'group_key'

 L. 375       486  LOAD_FAST                'group_key'
              488  LOAD_STR                 'y'
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE   540  'to 540'

 L. 376       496  LOAD_GLOBAL              int
              498  LOAD_FAST                'found_dict'
              500  LOAD_STR                 'y'
              502  BINARY_SUBSCR    
              504  CALL_FUNCTION_1       1  ''
              506  STORE_FAST               'year'

 L. 380       508  LOAD_FAST                'year'
              510  LOAD_CONST               68
              512  COMPARE_OP               <=
          514_516  POP_JUMP_IF_FALSE   528  'to 528'

 L. 381       518  LOAD_FAST                'year'
              520  LOAD_CONST               2000
              522  INPLACE_ADD      
              524  STORE_FAST               'year'
              526  JUMP_BACK           480  'to 480'
            528_0  COME_FROM           514  '514'

 L. 383       528  LOAD_FAST                'year'
              530  LOAD_CONST               1900
              532  INPLACE_ADD      
              534  STORE_FAST               'year'
          536_538  JUMP_BACK           480  'to 480'
            540_0  COME_FROM           492  '492'

 L. 384       540  LOAD_FAST                'group_key'
              542  LOAD_STR                 'Y'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   566  'to 566'

 L. 385       550  LOAD_GLOBAL              int
              552  LOAD_FAST                'found_dict'
              554  LOAD_STR                 'Y'
              556  BINARY_SUBSCR    
              558  CALL_FUNCTION_1       1  ''
              560  STORE_FAST               'year'
          562_564  JUMP_BACK           480  'to 480'
            566_0  COME_FROM           546  '546'

 L. 386       566  LOAD_FAST                'group_key'
              568  LOAD_STR                 'G'
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   592  'to 592'

 L. 387       576  LOAD_GLOBAL              int
              578  LOAD_FAST                'found_dict'
              580  LOAD_STR                 'G'
              582  BINARY_SUBSCR    
              584  CALL_FUNCTION_1       1  ''
              586  STORE_FAST               'iso_year'
          588_590  JUMP_BACK           480  'to 480'
            592_0  COME_FROM           572  '572'

 L. 388       592  LOAD_FAST                'group_key'
              594  LOAD_STR                 'm'
              596  COMPARE_OP               ==
          598_600  POP_JUMP_IF_FALSE   618  'to 618'

 L. 389       602  LOAD_GLOBAL              int
              604  LOAD_FAST                'found_dict'
              606  LOAD_STR                 'm'
              608  BINARY_SUBSCR    
              610  CALL_FUNCTION_1       1  ''
              612  STORE_FAST               'month'
          614_616  JUMP_BACK           480  'to 480'
            618_0  COME_FROM           598  '598'

 L. 390       618  LOAD_FAST                'group_key'
              620  LOAD_STR                 'B'
              622  COMPARE_OP               ==
          624_626  POP_JUMP_IF_FALSE   652  'to 652'

 L. 391       628  LOAD_FAST                'locale_time'
              630  LOAD_ATTR                f_month
              632  LOAD_METHOD              index
              634  LOAD_FAST                'found_dict'
              636  LOAD_STR                 'B'
              638  BINARY_SUBSCR    
              640  LOAD_METHOD              lower
              642  CALL_METHOD_0         0  ''
              644  CALL_METHOD_1         1  ''
              646  STORE_FAST               'month'
          648_650  JUMP_BACK           480  'to 480'
            652_0  COME_FROM           624  '624'

 L. 392       652  LOAD_FAST                'group_key'
              654  LOAD_STR                 'b'
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   686  'to 686'

 L. 393       662  LOAD_FAST                'locale_time'
              664  LOAD_ATTR                a_month
              666  LOAD_METHOD              index
              668  LOAD_FAST                'found_dict'
              670  LOAD_STR                 'b'
              672  BINARY_SUBSCR    
              674  LOAD_METHOD              lower
              676  CALL_METHOD_0         0  ''
              678  CALL_METHOD_1         1  ''
              680  STORE_FAST               'month'
          682_684  JUMP_BACK           480  'to 480'
            686_0  COME_FROM           658  '658'

 L. 394       686  LOAD_FAST                'group_key'
              688  LOAD_STR                 'd'
              690  COMPARE_OP               ==
          692_694  POP_JUMP_IF_FALSE   712  'to 712'

 L. 395       696  LOAD_GLOBAL              int
              698  LOAD_FAST                'found_dict'
              700  LOAD_STR                 'd'
              702  BINARY_SUBSCR    
              704  CALL_FUNCTION_1       1  ''
              706  STORE_FAST               'day'
          708_710  JUMP_BACK           480  'to 480'
            712_0  COME_FROM           692  '692'

 L. 396       712  LOAD_FAST                'group_key'
              714  LOAD_STR                 'H'
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   738  'to 738'

 L. 397       722  LOAD_GLOBAL              int
              724  LOAD_FAST                'found_dict'
              726  LOAD_STR                 'H'
              728  BINARY_SUBSCR    
              730  CALL_FUNCTION_1       1  ''
              732  STORE_FAST               'hour'
          734_736  JUMP_BACK           480  'to 480'
            738_0  COME_FROM           718  '718'

 L. 398       738  LOAD_FAST                'group_key'
              740  LOAD_STR                 'I'
              742  COMPARE_OP               ==
          744_746  POP_JUMP_IF_FALSE   850  'to 850'

 L. 399       748  LOAD_GLOBAL              int
              750  LOAD_FAST                'found_dict'
              752  LOAD_STR                 'I'
              754  BINARY_SUBSCR    
              756  CALL_FUNCTION_1       1  ''
              758  STORE_FAST               'hour'

 L. 400       760  LOAD_FAST                'found_dict'
              762  LOAD_METHOD              get
              764  LOAD_STR                 'p'
              766  LOAD_STR                 ''
              768  CALL_METHOD_2         2  ''
              770  LOAD_METHOD              lower
              772  CALL_METHOD_0         0  ''
              774  STORE_FAST               'ampm'

 L. 402       776  LOAD_FAST                'ampm'
              778  LOAD_STR                 ''
              780  LOAD_FAST                'locale_time'
              782  LOAD_ATTR                am_pm
              784  LOAD_CONST               0
              786  BINARY_SUBSCR    
              788  BUILD_TUPLE_2         2 
              790  <118>                 0  ''
          792_794  POP_JUMP_IF_FALSE   812  'to 812'

 L. 406       796  LOAD_FAST                'hour'
              798  LOAD_CONST               12
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_FALSE   846  'to 846'

 L. 407       806  LOAD_CONST               0
              808  STORE_FAST               'hour'
              810  JUMP_BACK           480  'to 480'
            812_0  COME_FROM           792  '792'

 L. 408       812  LOAD_FAST                'ampm'
              814  LOAD_FAST                'locale_time'
              816  LOAD_ATTR                am_pm
              818  LOAD_CONST               1
              820  BINARY_SUBSCR    
              822  COMPARE_OP               ==
          824_826  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 412       828  LOAD_FAST                'hour'
              830  LOAD_CONST               12
              832  COMPARE_OP               !=
          834_836  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 413       838  LOAD_FAST                'hour'
              840  LOAD_CONST               12
              842  INPLACE_ADD      
              844  STORE_FAST               'hour'
            846_0  COME_FROM           802  '802'
          846_848  JUMP_BACK           480  'to 480'
            850_0  COME_FROM           744  '744'

 L. 414       850  LOAD_FAST                'group_key'
              852  LOAD_STR                 'M'
              854  COMPARE_OP               ==
          856_858  POP_JUMP_IF_FALSE   876  'to 876'

 L. 415       860  LOAD_GLOBAL              int
              862  LOAD_FAST                'found_dict'
              864  LOAD_STR                 'M'
              866  BINARY_SUBSCR    
              868  CALL_FUNCTION_1       1  ''
              870  STORE_FAST               'minute'
          872_874  JUMP_BACK           480  'to 480'
            876_0  COME_FROM           856  '856'

 L. 416       876  LOAD_FAST                'group_key'
              878  LOAD_STR                 'S'
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   902  'to 902'

 L. 417       886  LOAD_GLOBAL              int
              888  LOAD_FAST                'found_dict'
              890  LOAD_STR                 'S'
              892  BINARY_SUBSCR    
              894  CALL_FUNCTION_1       1  ''
              896  STORE_FAST               'second'
          898_900  JUMP_BACK           480  'to 480'
            902_0  COME_FROM           882  '882'

 L. 418       902  LOAD_FAST                'group_key'
              904  LOAD_STR                 'f'
              906  COMPARE_OP               ==
          908_910  POP_JUMP_IF_FALSE   952  'to 952'

 L. 419       912  LOAD_FAST                'found_dict'
              914  LOAD_STR                 'f'
              916  BINARY_SUBSCR    
              918  STORE_FAST               's'

 L. 421       920  LOAD_FAST                's'
              922  LOAD_STR                 '0'
              924  LOAD_CONST               6
              926  LOAD_GLOBAL              len
              928  LOAD_FAST                's'
              930  CALL_FUNCTION_1       1  ''
              932  BINARY_SUBTRACT  
              934  BINARY_MULTIPLY  
              936  INPLACE_ADD      
              938  STORE_FAST               's'

 L. 422       940  LOAD_GLOBAL              int
              942  LOAD_FAST                's'
              944  CALL_FUNCTION_1       1  ''
              946  STORE_FAST               'fraction'
          948_950  JUMP_BACK           480  'to 480'
            952_0  COME_FROM           908  '908'

 L. 423       952  LOAD_FAST                'group_key'
              954  LOAD_STR                 'A'
              956  COMPARE_OP               ==
          958_960  POP_JUMP_IF_FALSE   986  'to 986'

 L. 424       962  LOAD_FAST                'locale_time'
              964  LOAD_ATTR                f_weekday
              966  LOAD_METHOD              index
              968  LOAD_FAST                'found_dict'
              970  LOAD_STR                 'A'
              972  BINARY_SUBSCR    
              974  LOAD_METHOD              lower
              976  CALL_METHOD_0         0  ''
              978  CALL_METHOD_1         1  ''
              980  STORE_FAST               'weekday'
          982_984  JUMP_BACK           480  'to 480'
            986_0  COME_FROM           958  '958'

 L. 425       986  LOAD_FAST                'group_key'
              988  LOAD_STR                 'a'
              990  COMPARE_OP               ==
          992_994  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 426       996  LOAD_FAST                'locale_time'
              998  LOAD_ATTR                a_weekday
             1000  LOAD_METHOD              index
             1002  LOAD_FAST                'found_dict'
             1004  LOAD_STR                 'a'
             1006  BINARY_SUBSCR    
             1008  LOAD_METHOD              lower
             1010  CALL_METHOD_0         0  ''
             1012  CALL_METHOD_1         1  ''
             1014  STORE_FAST               'weekday'
         1016_1018  JUMP_BACK           480  'to 480'
           1020_0  COME_FROM           992  '992'

 L. 427      1020  LOAD_FAST                'group_key'
             1022  LOAD_STR                 'w'
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_FALSE  1070  'to 1070'

 L. 428      1030  LOAD_GLOBAL              int
             1032  LOAD_FAST                'found_dict'
             1034  LOAD_STR                 'w'
             1036  BINARY_SUBSCR    
             1038  CALL_FUNCTION_1       1  ''
             1040  STORE_FAST               'weekday'

 L. 429      1042  LOAD_FAST                'weekday'
             1044  LOAD_CONST               0
             1046  COMPARE_OP               ==
         1048_1050  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 430      1052  LOAD_CONST               6
             1054  STORE_FAST               'weekday'
             1056  JUMP_BACK           480  'to 480'
           1058_0  COME_FROM          1048  '1048'

 L. 432      1058  LOAD_FAST                'weekday'
             1060  LOAD_CONST               1
             1062  INPLACE_SUBTRACT 
             1064  STORE_FAST               'weekday'
         1066_1068  JUMP_BACK           480  'to 480'
           1070_0  COME_FROM          1026  '1026'

 L. 433      1070  LOAD_FAST                'group_key'
             1072  LOAD_STR                 'u'
             1074  COMPARE_OP               ==
         1076_1078  POP_JUMP_IF_FALSE  1104  'to 1104'

 L. 434      1080  LOAD_GLOBAL              int
             1082  LOAD_FAST                'found_dict'
             1084  LOAD_STR                 'u'
             1086  BINARY_SUBSCR    
             1088  CALL_FUNCTION_1       1  ''
             1090  STORE_FAST               'weekday'

 L. 435      1092  LOAD_FAST                'weekday'
             1094  LOAD_CONST               1
             1096  INPLACE_SUBTRACT 
             1098  STORE_FAST               'weekday'
         1100_1102  JUMP_BACK           480  'to 480'
           1104_0  COME_FROM          1076  '1076'

 L. 436      1104  LOAD_FAST                'group_key'
             1106  LOAD_STR                 'j'
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 437      1114  LOAD_GLOBAL              int
             1116  LOAD_FAST                'found_dict'
             1118  LOAD_STR                 'j'
             1120  BINARY_SUBSCR    
             1122  CALL_FUNCTION_1       1  ''
             1124  STORE_FAST               'julian'
         1126_1128  JUMP_BACK           480  'to 480'
           1130_0  COME_FROM          1110  '1110'

 L. 438      1130  LOAD_FAST                'group_key'
             1132  LOAD_CONST               ('U', 'W')
             1134  <118>                 0  ''
         1136_1138  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 439      1140  LOAD_GLOBAL              int
             1142  LOAD_FAST                'found_dict'
             1144  LOAD_FAST                'group_key'
             1146  BINARY_SUBSCR    
             1148  CALL_FUNCTION_1       1  ''
             1150  STORE_FAST               'week_of_year'

 L. 440      1152  LOAD_FAST                'group_key'
             1154  LOAD_STR                 'U'
             1156  COMPARE_OP               ==
         1158_1160  POP_JUMP_IF_FALSE  1168  'to 1168'

 L. 442      1162  LOAD_CONST               6
             1164  STORE_FAST               'week_of_year_start'
             1166  JUMP_BACK           480  'to 480'
           1168_0  COME_FROM          1158  '1158'

 L. 445      1168  LOAD_CONST               0
             1170  STORE_FAST               'week_of_year_start'
         1172_1174  JUMP_BACK           480  'to 480'
           1176_0  COME_FROM          1136  '1136'

 L. 446      1176  LOAD_FAST                'group_key'
             1178  LOAD_STR                 'V'
             1180  COMPARE_OP               ==
         1182_1184  POP_JUMP_IF_FALSE  1202  'to 1202'

 L. 447      1186  LOAD_GLOBAL              int
             1188  LOAD_FAST                'found_dict'
             1190  LOAD_STR                 'V'
             1192  BINARY_SUBSCR    
             1194  CALL_FUNCTION_1       1  ''
             1196  STORE_FAST               'iso_week'
         1198_1200  JUMP_BACK           480  'to 480'
           1202_0  COME_FROM          1182  '1182'

 L. 448      1202  LOAD_FAST                'group_key'
             1204  LOAD_STR                 'z'
             1206  COMPARE_OP               ==
         1208_1210  POP_JUMP_IF_FALSE  1492  'to 1492'

 L. 449      1212  LOAD_FAST                'found_dict'
             1214  LOAD_STR                 'z'
             1216  BINARY_SUBSCR    
             1218  STORE_FAST               'z'

 L. 450      1220  LOAD_FAST                'z'
             1222  LOAD_STR                 'Z'
             1224  COMPARE_OP               ==
         1226_1228  POP_JUMP_IF_FALSE  1236  'to 1236'

 L. 451      1230  LOAD_CONST               0
             1232  STORE_FAST               'gmtoff'
             1234  JUMP_FORWARD       1490  'to 1490'
           1236_0  COME_FROM          1226  '1226'

 L. 453      1236  LOAD_FAST                'z'
             1238  LOAD_CONST               3
             1240  BINARY_SUBSCR    
             1242  LOAD_STR                 ':'
             1244  COMPARE_OP               ==
         1246_1248  POP_JUMP_IF_FALSE  1348  'to 1348'

 L. 454      1250  LOAD_FAST                'z'
             1252  LOAD_CONST               None
             1254  LOAD_CONST               3
             1256  BUILD_SLICE_2         2 
             1258  BINARY_SUBSCR    
             1260  LOAD_FAST                'z'
             1262  LOAD_CONST               4
             1264  LOAD_CONST               None
             1266  BUILD_SLICE_2         2 
             1268  BINARY_SUBSCR    
             1270  BINARY_ADD       
             1272  STORE_FAST               'z'

 L. 455      1274  LOAD_GLOBAL              len
             1276  LOAD_FAST                'z'
             1278  CALL_FUNCTION_1       1  ''
             1280  LOAD_CONST               5
             1282  COMPARE_OP               >
         1284_1286  POP_JUMP_IF_FALSE  1348  'to 1348'

 L. 456      1288  LOAD_FAST                'z'
             1290  LOAD_CONST               5
             1292  BINARY_SUBSCR    
             1294  LOAD_STR                 ':'
             1296  COMPARE_OP               !=
         1298_1300  POP_JUMP_IF_FALSE  1324  'to 1324'

 L. 457      1302  LOAD_STR                 'Inconsistent use of : in '
             1304  LOAD_FAST                'found_dict'
             1306  LOAD_STR                 'z'
             1308  BINARY_SUBSCR    
             1310  FORMAT_VALUE          0  ''
             1312  BUILD_STRING_2        2 
             1314  STORE_FAST               'msg'

 L. 458      1316  LOAD_GLOBAL              ValueError
             1318  LOAD_FAST                'msg'
             1320  CALL_FUNCTION_1       1  ''
             1322  RAISE_VARARGS_1       1  'exception instance'
           1324_0  COME_FROM          1298  '1298'

 L. 459      1324  LOAD_FAST                'z'
             1326  LOAD_CONST               None
             1328  LOAD_CONST               5
             1330  BUILD_SLICE_2         2 
             1332  BINARY_SUBSCR    
             1334  LOAD_FAST                'z'
             1336  LOAD_CONST               6
             1338  LOAD_CONST               None
             1340  BUILD_SLICE_2         2 
             1342  BINARY_SUBSCR    
             1344  BINARY_ADD       
             1346  STORE_FAST               'z'
           1348_0  COME_FROM          1284  '1284'
           1348_1  COME_FROM          1246  '1246'

 L. 460      1348  LOAD_GLOBAL              int
             1350  LOAD_FAST                'z'
             1352  LOAD_CONST               1
             1354  LOAD_CONST               3
             1356  BUILD_SLICE_2         2 
             1358  BINARY_SUBSCR    
             1360  CALL_FUNCTION_1       1  ''
             1362  STORE_FAST               'hours'

 L. 461      1364  LOAD_GLOBAL              int
             1366  LOAD_FAST                'z'
             1368  LOAD_CONST               3
             1370  LOAD_CONST               5
             1372  BUILD_SLICE_2         2 
             1374  BINARY_SUBSCR    
             1376  CALL_FUNCTION_1       1  ''
             1378  STORE_FAST               'minutes'

 L. 462      1380  LOAD_GLOBAL              int
             1382  LOAD_FAST                'z'
             1384  LOAD_CONST               5
             1386  LOAD_CONST               7
             1388  BUILD_SLICE_2         2 
             1390  BINARY_SUBSCR    
         1392_1394  JUMP_IF_TRUE_OR_POP  1398  'to 1398'
             1396  LOAD_CONST               0
           1398_0  COME_FROM          1392  '1392'
             1398  CALL_FUNCTION_1       1  ''
             1400  STORE_FAST               'seconds'

 L. 463      1402  LOAD_FAST                'hours'
             1404  LOAD_CONST               60
             1406  BINARY_MULTIPLY  
             1408  LOAD_CONST               60
             1410  BINARY_MULTIPLY  
             1412  LOAD_FAST                'minutes'
             1414  LOAD_CONST               60
             1416  BINARY_MULTIPLY  
             1418  BINARY_ADD       
             1420  LOAD_FAST                'seconds'
             1422  BINARY_ADD       
             1424  STORE_FAST               'gmtoff'

 L. 464      1426  LOAD_FAST                'z'
             1428  LOAD_CONST               8
             1430  LOAD_CONST               None
             1432  BUILD_SLICE_2         2 
             1434  BINARY_SUBSCR    
             1436  STORE_FAST               'gmtoff_remainder'

 L. 466      1438  LOAD_STR                 '0'
             1440  LOAD_CONST               6
             1442  LOAD_GLOBAL              len
             1444  LOAD_FAST                'gmtoff_remainder'
             1446  CALL_FUNCTION_1       1  ''
             1448  BINARY_SUBTRACT  
             1450  BINARY_MULTIPLY  
             1452  STORE_FAST               'gmtoff_remainder_padding'

 L. 467      1454  LOAD_GLOBAL              int
             1456  LOAD_FAST                'gmtoff_remainder'
             1458  LOAD_FAST                'gmtoff_remainder_padding'
             1460  BINARY_ADD       
             1462  CALL_FUNCTION_1       1  ''
             1464  STORE_FAST               'gmtoff_fraction'

 L. 468      1466  LOAD_FAST                'z'
             1468  LOAD_METHOD              startswith
             1470  LOAD_STR                 '-'
             1472  CALL_METHOD_1         1  ''
         1474_1476  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 469      1478  LOAD_FAST                'gmtoff'
             1480  UNARY_NEGATIVE   
             1482  STORE_FAST               'gmtoff'

 L. 470      1484  LOAD_FAST                'gmtoff_fraction'
             1486  UNARY_NEGATIVE   
             1488  STORE_FAST               'gmtoff_fraction'
           1490_0  COME_FROM          1234  '1234'
             1490  JUMP_BACK           480  'to 480'
           1492_0  COME_FROM          1208  '1208'

 L. 471      1492  LOAD_FAST                'group_key'
             1494  LOAD_STR                 'Z'
             1496  COMPARE_OP               ==
         1498_1500  POP_JUMP_IF_FALSE_BACK   480  'to 480'

 L. 474      1502  LOAD_FAST                'found_dict'
             1504  LOAD_STR                 'Z'
             1506  BINARY_SUBSCR    
             1508  LOAD_METHOD              lower
             1510  CALL_METHOD_0         0  ''
             1512  STORE_FAST               'found_zone'

 L. 475      1514  LOAD_GLOBAL              enumerate
             1516  LOAD_FAST                'locale_time'
             1518  LOAD_ATTR                timezone
             1520  CALL_FUNCTION_1       1  ''
             1522  GET_ITER         
           1524_0  COME_FROM          1600  '1600'
           1524_1  COME_FROM          1588  '1588'
           1524_2  COME_FROM          1538  '1538'
             1524  FOR_ITER           1604  'to 1604'
             1526  UNPACK_SEQUENCE_2     2 
             1528  STORE_FAST               'value'
             1530  STORE_FAST               'tz_values'

 L. 476      1532  LOAD_FAST                'found_zone'
             1534  LOAD_FAST                'tz_values'
             1536  <118>                 0  ''
         1538_1540  POP_JUMP_IF_FALSE_BACK  1524  'to 1524'

 L. 480      1542  LOAD_GLOBAL              time
             1544  LOAD_ATTR                tzname
             1546  LOAD_CONST               0
             1548  BINARY_SUBSCR    
             1550  LOAD_GLOBAL              time
             1552  LOAD_ATTR                tzname
             1554  LOAD_CONST               1
             1556  BINARY_SUBSCR    
             1558  COMPARE_OP               ==
         1560_1562  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 481      1564  LOAD_GLOBAL              time
             1566  LOAD_ATTR                daylight

 L. 480  1568_1570  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 481      1572  LOAD_FAST                'found_zone'
             1574  LOAD_CONST               ('utc', 'gmt')
             1576  <118>                 1  ''

 L. 480  1578_1580  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 482      1582  POP_TOP          
         1584_1586  BREAK_LOOP          480  'to 480'
             1588  JUMP_BACK          1524  'to 1524'
           1590_0  COME_FROM          1578  '1578'
           1590_1  COME_FROM          1568  '1568'
           1590_2  COME_FROM          1560  '1560'

 L. 484      1590  LOAD_FAST                'value'
             1592  STORE_FAST               'tz'

 L. 485      1594  POP_TOP          
         1596_1598  BREAK_LOOP          480  'to 480'
         1600_1602  JUMP_BACK          1524  'to 1524'
           1604_0  COME_FROM          1524  '1524'
           1604_1  COME_FROM          1474  '1474'
           1604_2  COME_FROM           834  '834'
           1604_3  COME_FROM           824  '824'
         1604_1606  JUMP_BACK           480  'to 480'
           1608_0  COME_FROM           480  '480'

 L. 488      1608  LOAD_FAST                'year'
             1610  LOAD_CONST               None
             1612  <117>                 0  ''
         1614_1616  POP_JUMP_IF_FALSE  1676  'to 1676'
             1618  LOAD_FAST                'iso_year'
             1620  LOAD_CONST               None
             1622  <117>                 1  ''
         1624_1626  POP_JUMP_IF_FALSE  1676  'to 1676'

 L. 489      1628  LOAD_FAST                'iso_week'
             1630  LOAD_CONST               None
             1632  <117>                 0  ''
         1634_1636  POP_JUMP_IF_TRUE   1648  'to 1648'
             1638  LOAD_FAST                'weekday'
             1640  LOAD_CONST               None
             1642  <117>                 0  ''
         1644_1646  POP_JUMP_IF_FALSE  1656  'to 1656'
           1648_0  COME_FROM          1634  '1634'

 L. 490      1648  LOAD_GLOBAL              ValueError
             1650  LOAD_STR                 "ISO year directive '%G' must be used with the ISO week directive '%V' and a weekday directive ('%A', '%a', '%w', or '%u')."
             1652  CALL_FUNCTION_1       1  ''
             1654  RAISE_VARARGS_1       1  'exception instance'
           1656_0  COME_FROM          1644  '1644'

 L. 493      1656  LOAD_FAST                'julian'
             1658  LOAD_CONST               None
             1660  <117>                 1  ''
         1662_1664  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 494      1666  LOAD_GLOBAL              ValueError
             1668  LOAD_STR                 "Day of the year directive '%j' is not compatible with ISO year directive '%G'. Use '%Y' instead."
             1670  CALL_FUNCTION_1       1  ''
             1672  RAISE_VARARGS_1       1  'exception instance'
             1674  JUMP_FORWARD       1724  'to 1724'
           1676_0  COME_FROM          1624  '1624'
           1676_1  COME_FROM          1614  '1614'

 L. 497      1676  LOAD_FAST                'week_of_year'
             1678  LOAD_CONST               None
             1680  <117>                 0  ''
         1682_1684  POP_JUMP_IF_FALSE  1724  'to 1724'
             1686  LOAD_FAST                'iso_week'
             1688  LOAD_CONST               None
             1690  <117>                 1  ''
         1692_1694  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 498      1696  LOAD_FAST                'weekday'
             1698  LOAD_CONST               None
             1700  <117>                 0  ''
         1702_1704  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 499      1706  LOAD_GLOBAL              ValueError
             1708  LOAD_STR                 "ISO week directive '%V' must be used with the ISO year directive '%G' and a weekday directive ('%A', '%a', '%w', or '%u')."
             1710  CALL_FUNCTION_1       1  ''
             1712  RAISE_VARARGS_1       1  'exception instance'
             1714  JUMP_FORWARD       1724  'to 1724'
           1716_0  COME_FROM          1702  '1702'

 L. 503      1716  LOAD_GLOBAL              ValueError
             1718  LOAD_STR                 "ISO week directive '%V' is incompatible with the year directive '%Y'. Use the ISO year '%G' instead."
             1720  CALL_FUNCTION_1       1  ''
             1722  RAISE_VARARGS_1       1  'exception instance'
           1724_0  COME_FROM          1714  '1714'
           1724_1  COME_FROM          1692  '1692'
           1724_2  COME_FROM          1682  '1682'
           1724_3  COME_FROM          1674  '1674'
           1724_4  COME_FROM          1662  '1662'

 L. 507      1724  LOAD_CONST               False
             1726  STORE_FAST               'leap_year_fix'

 L. 508      1728  LOAD_FAST                'year'
             1730  LOAD_CONST               None
             1732  <117>                 0  ''
         1734_1736  POP_JUMP_IF_FALSE  1768  'to 1768'
             1738  LOAD_FAST                'month'
             1740  LOAD_CONST               2
             1742  COMPARE_OP               ==
         1744_1746  POP_JUMP_IF_FALSE  1768  'to 1768'
             1748  LOAD_FAST                'day'
             1750  LOAD_CONST               29
             1752  COMPARE_OP               ==
         1754_1756  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 509      1758  LOAD_CONST               1904
             1760  STORE_FAST               'year'

 L. 510      1762  LOAD_CONST               True
             1764  STORE_FAST               'leap_year_fix'
             1766  JUMP_FORWARD       1782  'to 1782'
           1768_0  COME_FROM          1754  '1754'
           1768_1  COME_FROM          1744  '1744'
           1768_2  COME_FROM          1734  '1734'

 L. 511      1768  LOAD_FAST                'year'
             1770  LOAD_CONST               None
             1772  <117>                 0  ''
         1774_1776  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 512      1778  LOAD_CONST               1900
             1780  STORE_FAST               'year'
           1782_0  COME_FROM          1774  '1774'
           1782_1  COME_FROM          1766  '1766'

 L. 517      1782  LOAD_FAST                'julian'
             1784  LOAD_CONST               None
             1786  <117>                 0  ''
         1788_1790  POP_JUMP_IF_FALSE  1942  'to 1942'
             1792  LOAD_FAST                'weekday'
             1794  LOAD_CONST               None
             1796  <117>                 1  ''
         1798_1800  POP_JUMP_IF_FALSE  1942  'to 1942'

 L. 518      1802  LOAD_FAST                'week_of_year'
             1804  LOAD_CONST               None
             1806  <117>                 1  ''
         1808_1810  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 519      1812  LOAD_FAST                'week_of_year_start'
             1814  LOAD_CONST               0
             1816  COMPARE_OP               ==
         1818_1820  POP_JUMP_IF_FALSE  1826  'to 1826'
             1822  LOAD_CONST               True
             1824  JUMP_FORWARD       1828  'to 1828'
           1826_0  COME_FROM          1818  '1818'
             1826  LOAD_CONST               False
           1828_0  COME_FROM          1824  '1824'
             1828  STORE_FAST               'week_starts_Mon'

 L. 520      1830  LOAD_GLOBAL              _calc_julian_from_U_or_W
             1832  LOAD_FAST                'year'
             1834  LOAD_FAST                'week_of_year'
             1836  LOAD_FAST                'weekday'

 L. 521      1838  LOAD_FAST                'week_starts_Mon'

 L. 520      1840  CALL_FUNCTION_4       4  ''
             1842  STORE_FAST               'julian'
             1844  JUMP_FORWARD       1886  'to 1886'
           1846_0  COME_FROM          1808  '1808'

 L. 522      1846  LOAD_FAST                'iso_year'
             1848  LOAD_CONST               None
             1850  <117>                 1  ''
         1852_1854  POP_JUMP_IF_FALSE  1886  'to 1886'
             1856  LOAD_FAST                'iso_week'
             1858  LOAD_CONST               None
             1860  <117>                 1  ''
         1862_1864  POP_JUMP_IF_FALSE  1886  'to 1886'

 L. 523      1866  LOAD_GLOBAL              _calc_julian_from_V
             1868  LOAD_FAST                'iso_year'
             1870  LOAD_FAST                'iso_week'
             1872  LOAD_FAST                'weekday'
             1874  LOAD_CONST               1
             1876  BINARY_ADD       
             1878  CALL_FUNCTION_3       3  ''
             1880  UNPACK_SEQUENCE_2     2 
             1882  STORE_FAST               'year'
             1884  STORE_FAST               'julian'
           1886_0  COME_FROM          1862  '1862'
           1886_1  COME_FROM          1852  '1852'
           1886_2  COME_FROM          1844  '1844'

 L. 524      1886  LOAD_FAST                'julian'
             1888  LOAD_CONST               None
             1890  <117>                 1  ''
         1892_1894  POP_JUMP_IF_FALSE  1942  'to 1942'
             1896  LOAD_FAST                'julian'
             1898  LOAD_CONST               0
             1900  COMPARE_OP               <=
         1902_1904  POP_JUMP_IF_FALSE  1942  'to 1942'

 L. 525      1906  LOAD_FAST                'year'
             1908  LOAD_CONST               1
             1910  INPLACE_SUBTRACT 
             1912  STORE_FAST               'year'

 L. 526      1914  LOAD_GLOBAL              calendar
             1916  LOAD_METHOD              isleap
             1918  LOAD_FAST                'year'
             1920  CALL_METHOD_1         1  ''
         1922_1924  POP_JUMP_IF_FALSE  1930  'to 1930'
             1926  LOAD_CONST               366
             1928  JUMP_FORWARD       1932  'to 1932'
           1930_0  COME_FROM          1922  '1922'
             1930  LOAD_CONST               365
           1932_0  COME_FROM          1928  '1928'
             1932  STORE_FAST               'yday'

 L. 527      1934  LOAD_FAST                'julian'
             1936  LOAD_FAST                'yday'
             1938  INPLACE_ADD      
             1940  STORE_FAST               'julian'
           1942_0  COME_FROM          1902  '1902'
           1942_1  COME_FROM          1892  '1892'
           1942_2  COME_FROM          1798  '1798'
           1942_3  COME_FROM          1788  '1788'

 L. 529      1942  LOAD_FAST                'julian'
             1944  LOAD_CONST               None
             1946  <117>                 0  ''
         1948_1950  POP_JUMP_IF_FALSE  1990  'to 1990'

 L. 534      1952  LOAD_GLOBAL              datetime_date
             1954  LOAD_FAST                'year'
             1956  LOAD_FAST                'month'
             1958  LOAD_FAST                'day'
             1960  CALL_FUNCTION_3       3  ''
             1962  LOAD_METHOD              toordinal
             1964  CALL_METHOD_0         0  ''

 L. 535      1966  LOAD_GLOBAL              datetime_date
             1968  LOAD_FAST                'year'
             1970  LOAD_CONST               1
             1972  LOAD_CONST               1
             1974  CALL_FUNCTION_3       3  ''
             1976  LOAD_METHOD              toordinal
             1978  CALL_METHOD_0         0  ''

 L. 534      1980  BINARY_SUBTRACT  

 L. 535      1982  LOAD_CONST               1

 L. 534      1984  BINARY_ADD       
             1986  STORE_FAST               'julian'
             1988  JUMP_FORWARD       2038  'to 2038'
           1990_0  COME_FROM          1948  '1948'

 L. 538      1990  LOAD_GLOBAL              datetime_date
             1992  LOAD_METHOD              fromordinal

 L. 539      1994  LOAD_FAST                'julian'
             1996  LOAD_CONST               1
             1998  BINARY_SUBTRACT  

 L. 540      2000  LOAD_GLOBAL              datetime_date
             2002  LOAD_FAST                'year'
             2004  LOAD_CONST               1
             2006  LOAD_CONST               1
             2008  CALL_FUNCTION_3       3  ''
             2010  LOAD_METHOD              toordinal
             2012  CALL_METHOD_0         0  ''

 L. 539      2014  BINARY_ADD       

 L. 538      2016  CALL_METHOD_1         1  ''
             2018  STORE_FAST               'datetime_result'

 L. 541      2020  LOAD_FAST                'datetime_result'
             2022  LOAD_ATTR                year
             2024  STORE_FAST               'year'

 L. 542      2026  LOAD_FAST                'datetime_result'
             2028  LOAD_ATTR                month
             2030  STORE_FAST               'month'

 L. 543      2032  LOAD_FAST                'datetime_result'
             2034  LOAD_ATTR                day
             2036  STORE_FAST               'day'
           2038_0  COME_FROM          1988  '1988'

 L. 544      2038  LOAD_FAST                'weekday'
             2040  LOAD_CONST               None
             2042  <117>                 0  ''
         2044_2046  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 545      2048  LOAD_GLOBAL              datetime_date
             2050  LOAD_FAST                'year'
             2052  LOAD_FAST                'month'
             2054  LOAD_FAST                'day'
             2056  CALL_FUNCTION_3       3  ''
             2058  LOAD_METHOD              weekday
             2060  CALL_METHOD_0         0  ''
             2062  STORE_FAST               'weekday'
           2064_0  COME_FROM          2044  '2044'

 L. 547      2064  LOAD_FAST                'found_dict'
             2066  LOAD_METHOD              get
             2068  LOAD_STR                 'Z'
             2070  CALL_METHOD_1         1  ''
             2072  STORE_FAST               'tzname'

 L. 549      2074  LOAD_FAST                'leap_year_fix'
         2076_2078  POP_JUMP_IF_FALSE  2084  'to 2084'

 L. 553      2080  LOAD_CONST               1900
             2082  STORE_FAST               'year'
           2084_0  COME_FROM          2076  '2076'

 L. 555      2084  LOAD_FAST                'year'
             2086  LOAD_FAST                'month'
             2088  LOAD_FAST                'day'

 L. 556      2090  LOAD_FAST                'hour'
             2092  LOAD_FAST                'minute'
             2094  LOAD_FAST                'second'

 L. 557      2096  LOAD_FAST                'weekday'
             2098  LOAD_FAST                'julian'
             2100  LOAD_FAST                'tz'
             2102  LOAD_FAST                'tzname'
             2104  LOAD_FAST                'gmtoff'

 L. 555      2106  BUILD_TUPLE_11       11 

 L. 557      2108  LOAD_FAST                'fraction'
             2110  LOAD_FAST                'gmtoff_fraction'

 L. 555      2112  BUILD_TUPLE_3         3 
             2114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 180


def _strptime_time(data_string, format='%a %b %d %H:%M:%S %Y'):
    """Return a time struct based on the input string and the
    format string."""
    tt = _strptime(data_string, format)[0]
    return time.struct_time(tt[:time._STRUCT_TM_ITEMS])


def _strptime_datetime--- This code section failed: ---

 L. 568         0  LOAD_GLOBAL              _strptime
                2  LOAD_FAST                'data_string'
                4  LOAD_FAST                'format'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'tt'
               12  STORE_FAST               'fraction'
               14  STORE_FAST               'gmtoff_fraction'

 L. 569        16  LOAD_FAST                'tt'
               18  LOAD_CONST               -2
               20  LOAD_CONST               None
               22  BUILD_SLICE_2         2 
               24  BINARY_SUBSCR    
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'tzname'
               30  STORE_FAST               'gmtoff'

 L. 570        32  LOAD_FAST                'tt'
               34  LOAD_CONST               None
               36  LOAD_CONST               6
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'fraction'
               44  BUILD_TUPLE_1         1 
               46  BINARY_ADD       
               48  STORE_FAST               'args'

 L. 571        50  LOAD_FAST                'gmtoff'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE   104  'to 104'

 L. 572        58  LOAD_GLOBAL              datetime_timedelta
               60  LOAD_FAST                'gmtoff'
               62  LOAD_FAST                'gmtoff_fraction'
               64  LOAD_CONST               ('seconds', 'microseconds')
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  STORE_FAST               'tzdelta'

 L. 573        70  LOAD_FAST                'tzname'
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 574        74  LOAD_GLOBAL              datetime_timezone
               76  LOAD_FAST                'tzdelta'
               78  LOAD_FAST                'tzname'
               80  CALL_FUNCTION_2       2  ''
               82  STORE_FAST               'tz'
               84  JUMP_FORWARD         94  'to 94'
             86_0  COME_FROM            72  '72'

 L. 576        86  LOAD_GLOBAL              datetime_timezone
               88  LOAD_FAST                'tzdelta'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'tz'
             94_0  COME_FROM            84  '84'

 L. 577        94  LOAD_FAST                'args'
               96  LOAD_FAST                'tz'
               98  BUILD_TUPLE_1         1 
              100  INPLACE_ADD      
              102  STORE_FAST               'args'
            104_0  COME_FROM            56  '56'

 L. 579       104  LOAD_FAST                'cls'
              106  LOAD_FAST                'args'
              108  CALL_FUNCTION_EX      0  'positional arguments only'
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 54


# global _TimeRE_cache ## Warning: Unused global
# global _regex_cache ## Warning: Unused global