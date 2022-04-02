# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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
        if time.tzname != self.tzname or time.daylight != self.daylight:
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

    def __calc_date_time(self):
        time_tuple = time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0))
        date_time = [None, None, None]
        date_time[0] = time.strftime('%c', time_tuple).lower()
        date_time[1] = time.strftime('%x', time_tuple).lower()
        date_time[2] = time.strftime('%X', time_tuple).lower()
        replacement_pairs = [('%', '%%'), (self.f_weekday[2], '%A'),
         (
          self.f_month[3], '%B'), (self.a_weekday[2], '%a'),
         (
          self.a_month[3], '%b'), (self.am_pm[1], '%p'),
         ('1999', '%Y'), ('99', '%y'), ('22', '%H'),
         ('44', '%M'), ('55', '%S'), ('76', '%j'),
         ('17', '%d'), ('03', '%m'), ('3', '%m'),
         ('2', '%w'), ('10', '%I')]
        replacement_pairs.extend([(tz, '%Z') for tz_values in self.timezone for tz in tz_values])
        for offset, directive in ((0, '%c'), (1, '%x'), (2, '%X')):
            current_format = date_time[offset]
            for old, new in replacement_pairs:
                if old:
                    current_format = current_format.replace(old, new)
                time_tuple = time.struct_time((1999, 1, 3, 1, 1, 1, 6, 3, 0))
                if '00' in time.strftime(directive, time_tuple):
                    U_W = '%W'
                else:
                    U_W = '%U'
                date_time[offset] = current_format.replace('11', U_W)
            else:
                self.LC_date_time = date_time[0]
                self.LC_date = date_time[1]
                self.LC_time = date_time[2]

    def __calc_timezone(self):
        try:
            time.tzset()
        except AttributeError:
            pass
        else:
            self.tzname = time.tzname
            self.daylight = time.daylight
            no_saving = frozenset({'utc', 'gmt', self.tzname[0].lower()})
            if self.daylight:
                has_saving = frozenset({self.tzname[1].lower()})
            else:
                has_saving = frozenset()
            self.timezone = (
             no_saving, has_saving)


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

    def __seqToRE(self, to_convert, directive):
        """Convert a list to a regex string for matching a directive.

        Want possible matching values to be from longest to shortest.  This
        prevents the possibility of a match occurring for a value that also
        a substring of a larger value that should have matched (e.g., 'abc'
        matching when 'abcdef' should have been the match).

        """
        to_convert = sorted(to_convert, key=len, reverse=True)
        for value in to_convert:
            if value != '':
                break
            return ''
            regex = '|'.join((re_escape(stuff) for stuff in to_convert))
            regex = '(?P<%s>%s' % (directive, regex)
            return '%s)' % regex

    def pattern(self, format):
        """Return regex pattern for the format string.

        Need to make sure that any characters that might be interpreted as
        regex syntax are escaped.

        """
        processed_format = ''
        regex_chars = re_compile('([\\\\.^$*+?\\(\\){}\\[\\]|])')
        format = regex_chars.sub('\\\\\\1', format)
        whitespace_replacement = re_compile('\\s+')
        format = whitespace_replacement.sub('\\\\s+', format)
        while '%' in format:
            directive_index = format.index('%') + 1
            processed_format = '%s%s%s' % (processed_format,
             format[:directive_index - 1],
             self[format[directive_index]])
            format = format[directive_index + 1:]

        return '%s%s' % (processed_format, format)

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
    return (
     iso_year, ordinal)


def _strptime--- This code section failed: ---

 L. 314         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'data_string'
                4  LOAD_FAST                'format'
                6  BUILD_LIST_2          2 
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
             12_0  COME_FROM            28  '28'
               12  FOR_ITER             56  'to 56'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'index'
               18  STORE_FAST               'arg'

 L. 315        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'arg'
               24  LOAD_GLOBAL              str
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     12  'to 12'

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

 L. 320        56  LOAD_GLOBAL              _cache_lock
               58  SETUP_WITH          298  'to 298'
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
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   250  'to 250'
              184  POP_TOP          
              186  STORE_FAST               'err'
              188  POP_TOP          
              190  SETUP_FINALLY       238  'to 238'

 L. 337       192  LOAD_FAST                'err'
              194  LOAD_ATTR                args
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  STORE_FAST               'bad_directive'

 L. 338       202  LOAD_FAST                'bad_directive'
              204  LOAD_STR                 '\\'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   214  'to 214'

 L. 339       210  LOAD_STR                 '%'
              212  STORE_FAST               'bad_directive'
            214_0  COME_FROM           208  '208'

 L. 340       214  DELETE_FAST              'err'

 L. 341       216  LOAD_GLOBAL              ValueError
              218  LOAD_STR                 "'%s' is a bad directive in format '%s'"

 L. 342       220  LOAD_FAST                'bad_directive'
              222  LOAD_FAST                'format'
              224  BUILD_TUPLE_2         2 

 L. 341       226  BINARY_MODULO    
              228  CALL_FUNCTION_1       1  ''

 L. 342       230  LOAD_CONST               None

 L. 341       232  RAISE_VARARGS_2       2  'exception instance with __cause__'
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_FINALLY   190  '190'
              238  LOAD_CONST               None
              240  STORE_FAST               'err'
              242  DELETE_FAST              'err'
              244  END_FINALLY      
              246  POP_EXCEPT       
              248  JUMP_FORWARD        286  'to 286'
            250_0  COME_FROM           182  '182'

 L. 344       250  DUP_TOP          
              252  LOAD_GLOBAL              IndexError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   284  'to 284'
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
            284_0  COME_FROM           256  '256'
              284  END_FINALLY      
            286_0  COME_FROM           282  '282'
            286_1  COME_FROM           248  '248'
            286_2  COME_FROM           174  '174'

 L. 346       286  LOAD_FAST                'format_regex'
              288  LOAD_GLOBAL              _regex_cache
              290  LOAD_FAST                'format'
              292  STORE_SUBSCR     
            294_0  COME_FROM           156  '156'
              294  POP_BLOCK        
              296  BEGIN_FINALLY    
            298_0  COME_FROM_WITH       58  '58'
              298  WITH_CLEANUP_START
              300  WITH_CLEANUP_FINISH
              302  END_FINALLY      

 L. 347       304  LOAD_FAST                'format_regex'
              306  LOAD_METHOD              match
              308  LOAD_FAST                'data_string'
              310  CALL_METHOD_1         1  ''
              312  STORE_FAST               'found'

 L. 348       314  LOAD_FAST                'found'
          316_318  POP_JUMP_IF_TRUE    336  'to 336'

 L. 349       320  LOAD_GLOBAL              ValueError
              322  LOAD_STR                 'time data %r does not match format %r'

 L. 350       324  LOAD_FAST                'data_string'
              326  LOAD_FAST                'format'
              328  BUILD_TUPLE_2         2 

 L. 349       330  BINARY_MODULO    
              332  CALL_FUNCTION_1       1  ''
              334  RAISE_VARARGS_1       1  'exception instance'
            336_0  COME_FROM           316  '316'

 L. 351       336  LOAD_GLOBAL              len
              338  LOAD_FAST                'data_string'
              340  CALL_FUNCTION_1       1  ''
              342  LOAD_FAST                'found'
              344  LOAD_METHOD              end
              346  CALL_METHOD_0         0  ''
              348  COMPARE_OP               !=
          350_352  POP_JUMP_IF_FALSE   378  'to 378'

 L. 352       354  LOAD_GLOBAL              ValueError
              356  LOAD_STR                 'unconverted data remains: %s'

 L. 353       358  LOAD_FAST                'data_string'
              360  LOAD_FAST                'found'
              362  LOAD_METHOD              end
              364  CALL_METHOD_0         0  ''
              366  LOAD_CONST               None
              368  BUILD_SLICE_2         2 
              370  BINARY_SUBSCR    

 L. 352       372  BINARY_MODULO    
              374  CALL_FUNCTION_1       1  ''
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           350  '350'

 L. 355       378  LOAD_CONST               None
              380  DUP_TOP          
              382  STORE_FAST               'iso_year'
              384  STORE_FAST               'year'

 L. 356       386  LOAD_CONST               1
              388  DUP_TOP          
              390  STORE_FAST               'month'
              392  STORE_FAST               'day'

 L. 357       394  LOAD_CONST               0
              396  DUP_TOP          
              398  STORE_FAST               'hour'
              400  DUP_TOP          
              402  STORE_FAST               'minute'
              404  DUP_TOP          
              406  STORE_FAST               'second'
              408  STORE_FAST               'fraction'

 L. 358       410  LOAD_CONST               -1
              412  STORE_FAST               'tz'

 L. 359       414  LOAD_CONST               None
              416  STORE_FAST               'gmtoff'

 L. 360       418  LOAD_CONST               0
              420  STORE_FAST               'gmtoff_fraction'

 L. 363       422  LOAD_CONST               None
              424  DUP_TOP          
              426  STORE_FAST               'iso_week'
              428  STORE_FAST               'week_of_year'

 L. 364       430  LOAD_CONST               None
              432  STORE_FAST               'week_of_year_start'

 L. 367       434  LOAD_CONST               None
              436  DUP_TOP          
              438  STORE_FAST               'weekday'
              440  STORE_FAST               'julian'

 L. 368       442  LOAD_FAST                'found'
              444  LOAD_METHOD              groupdict
              446  CALL_METHOD_0         0  ''
              448  STORE_FAST               'found_dict'

 L. 369       450  LOAD_FAST                'found_dict'
              452  LOAD_METHOD              keys
              454  CALL_METHOD_0         0  ''
              456  GET_ITER         
            458_0  COME_FROM          1476  '1476'
          458_460  FOR_ITER           1586  'to 1586'
              462  STORE_FAST               'group_key'

 L. 375       464  LOAD_FAST                'group_key'
              466  LOAD_STR                 'y'
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   518  'to 518'

 L. 376       474  LOAD_GLOBAL              int
              476  LOAD_FAST                'found_dict'
              478  LOAD_STR                 'y'
              480  BINARY_SUBSCR    
              482  CALL_FUNCTION_1       1  ''
              484  STORE_FAST               'year'

 L. 380       486  LOAD_FAST                'year'
              488  LOAD_CONST               68
              490  COMPARE_OP               <=
          492_494  POP_JUMP_IF_FALSE   506  'to 506'

 L. 381       496  LOAD_FAST                'year'
              498  LOAD_CONST               2000
              500  INPLACE_ADD      
              502  STORE_FAST               'year'
              504  JUMP_BACK           458  'to 458'
            506_0  COME_FROM           492  '492'

 L. 383       506  LOAD_FAST                'year'
              508  LOAD_CONST               1900
              510  INPLACE_ADD      
              512  STORE_FAST               'year'
          514_516  JUMP_BACK           458  'to 458'
            518_0  COME_FROM           470  '470'

 L. 384       518  LOAD_FAST                'group_key'
              520  LOAD_STR                 'Y'
              522  COMPARE_OP               ==
          524_526  POP_JUMP_IF_FALSE   544  'to 544'

 L. 385       528  LOAD_GLOBAL              int
              530  LOAD_FAST                'found_dict'
              532  LOAD_STR                 'Y'
              534  BINARY_SUBSCR    
              536  CALL_FUNCTION_1       1  ''
              538  STORE_FAST               'year'
          540_542  JUMP_BACK           458  'to 458'
            544_0  COME_FROM           524  '524'

 L. 386       544  LOAD_FAST                'group_key'
              546  LOAD_STR                 'G'
              548  COMPARE_OP               ==
          550_552  POP_JUMP_IF_FALSE   570  'to 570'

 L. 387       554  LOAD_GLOBAL              int
              556  LOAD_FAST                'found_dict'
              558  LOAD_STR                 'G'
              560  BINARY_SUBSCR    
              562  CALL_FUNCTION_1       1  ''
              564  STORE_FAST               'iso_year'
          566_568  JUMP_BACK           458  'to 458'
            570_0  COME_FROM           550  '550'

 L. 388       570  LOAD_FAST                'group_key'
              572  LOAD_STR                 'm'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   596  'to 596'

 L. 389       580  LOAD_GLOBAL              int
              582  LOAD_FAST                'found_dict'
              584  LOAD_STR                 'm'
              586  BINARY_SUBSCR    
              588  CALL_FUNCTION_1       1  ''
              590  STORE_FAST               'month'
          592_594  JUMP_BACK           458  'to 458'
            596_0  COME_FROM           576  '576'

 L. 390       596  LOAD_FAST                'group_key'
              598  LOAD_STR                 'B'
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   630  'to 630'

 L. 391       606  LOAD_FAST                'locale_time'
              608  LOAD_ATTR                f_month
              610  LOAD_METHOD              index
              612  LOAD_FAST                'found_dict'
              614  LOAD_STR                 'B'
              616  BINARY_SUBSCR    
              618  LOAD_METHOD              lower
              620  CALL_METHOD_0         0  ''
              622  CALL_METHOD_1         1  ''
              624  STORE_FAST               'month'
          626_628  JUMP_BACK           458  'to 458'
            630_0  COME_FROM           602  '602'

 L. 392       630  LOAD_FAST                'group_key'
              632  LOAD_STR                 'b'
              634  COMPARE_OP               ==
          636_638  POP_JUMP_IF_FALSE   664  'to 664'

 L. 393       640  LOAD_FAST                'locale_time'
              642  LOAD_ATTR                a_month
              644  LOAD_METHOD              index
              646  LOAD_FAST                'found_dict'
              648  LOAD_STR                 'b'
              650  BINARY_SUBSCR    
              652  LOAD_METHOD              lower
              654  CALL_METHOD_0         0  ''
              656  CALL_METHOD_1         1  ''
              658  STORE_FAST               'month'
          660_662  JUMP_BACK           458  'to 458'
            664_0  COME_FROM           636  '636'

 L. 394       664  LOAD_FAST                'group_key'
              666  LOAD_STR                 'd'
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE   690  'to 690'

 L. 395       674  LOAD_GLOBAL              int
              676  LOAD_FAST                'found_dict'
              678  LOAD_STR                 'd'
              680  BINARY_SUBSCR    
              682  CALL_FUNCTION_1       1  ''
              684  STORE_FAST               'day'
          686_688  JUMP_BACK           458  'to 458'
            690_0  COME_FROM           670  '670'

 L. 396       690  LOAD_FAST                'group_key'
              692  LOAD_STR                 'H'
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   716  'to 716'

 L. 397       700  LOAD_GLOBAL              int
              702  LOAD_FAST                'found_dict'
              704  LOAD_STR                 'H'
              706  BINARY_SUBSCR    
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'hour'
          712_714  JUMP_BACK           458  'to 458'
            716_0  COME_FROM           696  '696'

 L. 398       716  LOAD_FAST                'group_key'
              718  LOAD_STR                 'I'
              720  COMPARE_OP               ==
          722_724  POP_JUMP_IF_FALSE   828  'to 828'

 L. 399       726  LOAD_GLOBAL              int
              728  LOAD_FAST                'found_dict'
              730  LOAD_STR                 'I'
              732  BINARY_SUBSCR    
              734  CALL_FUNCTION_1       1  ''
              736  STORE_FAST               'hour'

 L. 400       738  LOAD_FAST                'found_dict'
              740  LOAD_METHOD              get
              742  LOAD_STR                 'p'
              744  LOAD_STR                 ''
              746  CALL_METHOD_2         2  ''
              748  LOAD_METHOD              lower
              750  CALL_METHOD_0         0  ''
              752  STORE_FAST               'ampm'

 L. 402       754  LOAD_FAST                'ampm'
              756  LOAD_STR                 ''
              758  LOAD_FAST                'locale_time'
              760  LOAD_ATTR                am_pm
              762  LOAD_CONST               0
              764  BINARY_SUBSCR    
              766  BUILD_TUPLE_2         2 
              768  COMPARE_OP               in
          770_772  POP_JUMP_IF_FALSE   790  'to 790'

 L. 406       774  LOAD_FAST                'hour'
              776  LOAD_CONST               12
              778  COMPARE_OP               ==
          780_782  POP_JUMP_IF_FALSE   824  'to 824'

 L. 407       784  LOAD_CONST               0
              786  STORE_FAST               'hour'
              788  JUMP_BACK           458  'to 458'
            790_0  COME_FROM           770  '770'

 L. 408       790  LOAD_FAST                'ampm'
              792  LOAD_FAST                'locale_time'
              794  LOAD_ATTR                am_pm
              796  LOAD_CONST               1
              798  BINARY_SUBSCR    
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 412       806  LOAD_FAST                'hour'
              808  LOAD_CONST               12
              810  COMPARE_OP               !=
          812_814  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 413       816  LOAD_FAST                'hour'
              818  LOAD_CONST               12
              820  INPLACE_ADD      
              822  STORE_FAST               'hour'
            824_0  COME_FROM           780  '780'
          824_826  JUMP_BACK           458  'to 458'
            828_0  COME_FROM           722  '722'

 L. 414       828  LOAD_FAST                'group_key'
              830  LOAD_STR                 'M'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   854  'to 854'

 L. 415       838  LOAD_GLOBAL              int
              840  LOAD_FAST                'found_dict'
              842  LOAD_STR                 'M'
              844  BINARY_SUBSCR    
              846  CALL_FUNCTION_1       1  ''
              848  STORE_FAST               'minute'
          850_852  JUMP_BACK           458  'to 458'
            854_0  COME_FROM           834  '834'

 L. 416       854  LOAD_FAST                'group_key'
              856  LOAD_STR                 'S'
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_FALSE   880  'to 880'

 L. 417       864  LOAD_GLOBAL              int
              866  LOAD_FAST                'found_dict'
              868  LOAD_STR                 'S'
              870  BINARY_SUBSCR    
              872  CALL_FUNCTION_1       1  ''
              874  STORE_FAST               'second'
          876_878  JUMP_BACK           458  'to 458'
            880_0  COME_FROM           860  '860'

 L. 418       880  LOAD_FAST                'group_key'
              882  LOAD_STR                 'f'
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_FALSE   930  'to 930'

 L. 419       890  LOAD_FAST                'found_dict'
              892  LOAD_STR                 'f'
              894  BINARY_SUBSCR    
              896  STORE_FAST               's'

 L. 421       898  LOAD_FAST                's'
              900  LOAD_STR                 '0'
              902  LOAD_CONST               6
              904  LOAD_GLOBAL              len
              906  LOAD_FAST                's'
              908  CALL_FUNCTION_1       1  ''
              910  BINARY_SUBTRACT  
              912  BINARY_MULTIPLY  
              914  INPLACE_ADD      
              916  STORE_FAST               's'

 L. 422       918  LOAD_GLOBAL              int
              920  LOAD_FAST                's'
              922  CALL_FUNCTION_1       1  ''
              924  STORE_FAST               'fraction'
          926_928  JUMP_BACK           458  'to 458'
            930_0  COME_FROM           886  '886'

 L. 423       930  LOAD_FAST                'group_key'
              932  LOAD_STR                 'A'
              934  COMPARE_OP               ==
          936_938  POP_JUMP_IF_FALSE   964  'to 964'

 L. 424       940  LOAD_FAST                'locale_time'
              942  LOAD_ATTR                f_weekday
              944  LOAD_METHOD              index
              946  LOAD_FAST                'found_dict'
              948  LOAD_STR                 'A'
              950  BINARY_SUBSCR    
              952  LOAD_METHOD              lower
              954  CALL_METHOD_0         0  ''
              956  CALL_METHOD_1         1  ''
              958  STORE_FAST               'weekday'
          960_962  JUMP_BACK           458  'to 458'
            964_0  COME_FROM           936  '936'

 L. 425       964  LOAD_FAST                'group_key'
              966  LOAD_STR                 'a'
              968  COMPARE_OP               ==
          970_972  POP_JUMP_IF_FALSE   998  'to 998'

 L. 426       974  LOAD_FAST                'locale_time'
              976  LOAD_ATTR                a_weekday
              978  LOAD_METHOD              index
              980  LOAD_FAST                'found_dict'
              982  LOAD_STR                 'a'
              984  BINARY_SUBSCR    
              986  LOAD_METHOD              lower
              988  CALL_METHOD_0         0  ''
              990  CALL_METHOD_1         1  ''
              992  STORE_FAST               'weekday'
          994_996  JUMP_BACK           458  'to 458'
            998_0  COME_FROM           970  '970'

 L. 427       998  LOAD_FAST                'group_key'
             1000  LOAD_STR                 'w'
             1002  COMPARE_OP               ==
         1004_1006  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 428      1008  LOAD_GLOBAL              int
             1010  LOAD_FAST                'found_dict'
             1012  LOAD_STR                 'w'
             1014  BINARY_SUBSCR    
             1016  CALL_FUNCTION_1       1  ''
             1018  STORE_FAST               'weekday'

 L. 429      1020  LOAD_FAST                'weekday'
             1022  LOAD_CONST               0
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 430      1030  LOAD_CONST               6
             1032  STORE_FAST               'weekday'
             1034  JUMP_BACK           458  'to 458'
           1036_0  COME_FROM          1026  '1026'

 L. 432      1036  LOAD_FAST                'weekday'
             1038  LOAD_CONST               1
             1040  INPLACE_SUBTRACT 
             1042  STORE_FAST               'weekday'
         1044_1046  JUMP_BACK           458  'to 458'
           1048_0  COME_FROM          1004  '1004'

 L. 433      1048  LOAD_FAST                'group_key'
             1050  LOAD_STR                 'u'
             1052  COMPARE_OP               ==
         1054_1056  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 434      1058  LOAD_GLOBAL              int
             1060  LOAD_FAST                'found_dict'
             1062  LOAD_STR                 'u'
             1064  BINARY_SUBSCR    
             1066  CALL_FUNCTION_1       1  ''
             1068  STORE_FAST               'weekday'

 L. 435      1070  LOAD_FAST                'weekday'
             1072  LOAD_CONST               1
             1074  INPLACE_SUBTRACT 
             1076  STORE_FAST               'weekday'
         1078_1080  JUMP_BACK           458  'to 458'
           1082_0  COME_FROM          1054  '1054'

 L. 436      1082  LOAD_FAST                'group_key'
             1084  LOAD_STR                 'j'
             1086  COMPARE_OP               ==
         1088_1090  POP_JUMP_IF_FALSE  1108  'to 1108'

 L. 437      1092  LOAD_GLOBAL              int
             1094  LOAD_FAST                'found_dict'
             1096  LOAD_STR                 'j'
             1098  BINARY_SUBSCR    
             1100  CALL_FUNCTION_1       1  ''
             1102  STORE_FAST               'julian'
         1104_1106  JUMP_BACK           458  'to 458'
           1108_0  COME_FROM          1088  '1088'

 L. 438      1108  LOAD_FAST                'group_key'
             1110  LOAD_CONST               ('U', 'W')
             1112  COMPARE_OP               in
         1114_1116  POP_JUMP_IF_FALSE  1154  'to 1154'

 L. 439      1118  LOAD_GLOBAL              int
             1120  LOAD_FAST                'found_dict'
             1122  LOAD_FAST                'group_key'
             1124  BINARY_SUBSCR    
             1126  CALL_FUNCTION_1       1  ''
             1128  STORE_FAST               'week_of_year'

 L. 440      1130  LOAD_FAST                'group_key'
             1132  LOAD_STR                 'U'
             1134  COMPARE_OP               ==
         1136_1138  POP_JUMP_IF_FALSE  1146  'to 1146'

 L. 442      1140  LOAD_CONST               6
             1142  STORE_FAST               'week_of_year_start'
             1144  JUMP_BACK           458  'to 458'
           1146_0  COME_FROM          1136  '1136'

 L. 445      1146  LOAD_CONST               0
             1148  STORE_FAST               'week_of_year_start'
         1150_1152  JUMP_BACK           458  'to 458'
           1154_0  COME_FROM          1114  '1114'

 L. 446      1154  LOAD_FAST                'group_key'
             1156  LOAD_STR                 'V'
             1158  COMPARE_OP               ==
         1160_1162  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 447      1164  LOAD_GLOBAL              int
             1166  LOAD_FAST                'found_dict'
             1168  LOAD_STR                 'V'
             1170  BINARY_SUBSCR    
             1172  CALL_FUNCTION_1       1  ''
             1174  STORE_FAST               'iso_week'
         1176_1178  JUMP_BACK           458  'to 458'
           1180_0  COME_FROM          1160  '1160'

 L. 448      1180  LOAD_FAST                'group_key'
             1182  LOAD_STR                 'z'
             1184  COMPARE_OP               ==
         1186_1188  POP_JUMP_IF_FALSE  1470  'to 1470'

 L. 449      1190  LOAD_FAST                'found_dict'
             1192  LOAD_STR                 'z'
             1194  BINARY_SUBSCR    
             1196  STORE_FAST               'z'

 L. 450      1198  LOAD_FAST                'z'
             1200  LOAD_STR                 'Z'
             1202  COMPARE_OP               ==
         1204_1206  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 451      1208  LOAD_CONST               0
             1210  STORE_FAST               'gmtoff'
             1212  JUMP_FORWARD       1468  'to 1468'
           1214_0  COME_FROM          1204  '1204'

 L. 453      1214  LOAD_FAST                'z'
             1216  LOAD_CONST               3
             1218  BINARY_SUBSCR    
             1220  LOAD_STR                 ':'
             1222  COMPARE_OP               ==
         1224_1226  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 454      1228  LOAD_FAST                'z'
             1230  LOAD_CONST               None
             1232  LOAD_CONST               3
             1234  BUILD_SLICE_2         2 
             1236  BINARY_SUBSCR    
             1238  LOAD_FAST                'z'
             1240  LOAD_CONST               4
             1242  LOAD_CONST               None
             1244  BUILD_SLICE_2         2 
             1246  BINARY_SUBSCR    
             1248  BINARY_ADD       
             1250  STORE_FAST               'z'

 L. 455      1252  LOAD_GLOBAL              len
             1254  LOAD_FAST                'z'
             1256  CALL_FUNCTION_1       1  ''
             1258  LOAD_CONST               5
             1260  COMPARE_OP               >
         1262_1264  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 456      1266  LOAD_FAST                'z'
             1268  LOAD_CONST               5
             1270  BINARY_SUBSCR    
             1272  LOAD_STR                 ':'
             1274  COMPARE_OP               !=
         1276_1278  POP_JUMP_IF_FALSE  1302  'to 1302'

 L. 457      1280  LOAD_STR                 'Inconsistent use of : in '
             1282  LOAD_FAST                'found_dict'
             1284  LOAD_STR                 'z'
             1286  BINARY_SUBSCR    
             1288  FORMAT_VALUE          0  ''
             1290  BUILD_STRING_2        2 
             1292  STORE_FAST               'msg'

 L. 458      1294  LOAD_GLOBAL              ValueError
             1296  LOAD_FAST                'msg'
             1298  CALL_FUNCTION_1       1  ''
             1300  RAISE_VARARGS_1       1  'exception instance'
           1302_0  COME_FROM          1276  '1276'

 L. 459      1302  LOAD_FAST                'z'
             1304  LOAD_CONST               None
             1306  LOAD_CONST               5
             1308  BUILD_SLICE_2         2 
             1310  BINARY_SUBSCR    
             1312  LOAD_FAST                'z'
             1314  LOAD_CONST               6
             1316  LOAD_CONST               None
             1318  BUILD_SLICE_2         2 
             1320  BINARY_SUBSCR    
             1322  BINARY_ADD       
             1324  STORE_FAST               'z'
           1326_0  COME_FROM          1262  '1262'
           1326_1  COME_FROM          1224  '1224'

 L. 460      1326  LOAD_GLOBAL              int
             1328  LOAD_FAST                'z'
             1330  LOAD_CONST               1
             1332  LOAD_CONST               3
             1334  BUILD_SLICE_2         2 
             1336  BINARY_SUBSCR    
             1338  CALL_FUNCTION_1       1  ''
             1340  STORE_FAST               'hours'

 L. 461      1342  LOAD_GLOBAL              int
             1344  LOAD_FAST                'z'
             1346  LOAD_CONST               3
             1348  LOAD_CONST               5
             1350  BUILD_SLICE_2         2 
             1352  BINARY_SUBSCR    
             1354  CALL_FUNCTION_1       1  ''
             1356  STORE_FAST               'minutes'

 L. 462      1358  LOAD_GLOBAL              int
             1360  LOAD_FAST                'z'
             1362  LOAD_CONST               5
             1364  LOAD_CONST               7
             1366  BUILD_SLICE_2         2 
             1368  BINARY_SUBSCR    
         1370_1372  JUMP_IF_TRUE_OR_POP  1376  'to 1376'
             1374  LOAD_CONST               0
           1376_0  COME_FROM          1370  '1370'
             1376  CALL_FUNCTION_1       1  ''
             1378  STORE_FAST               'seconds'

 L. 463      1380  LOAD_FAST                'hours'
             1382  LOAD_CONST               60
             1384  BINARY_MULTIPLY  
             1386  LOAD_CONST               60
             1388  BINARY_MULTIPLY  
             1390  LOAD_FAST                'minutes'
             1392  LOAD_CONST               60
             1394  BINARY_MULTIPLY  
             1396  BINARY_ADD       
             1398  LOAD_FAST                'seconds'
             1400  BINARY_ADD       
             1402  STORE_FAST               'gmtoff'

 L. 464      1404  LOAD_FAST                'z'
             1406  LOAD_CONST               8
             1408  LOAD_CONST               None
             1410  BUILD_SLICE_2         2 
             1412  BINARY_SUBSCR    
             1414  STORE_FAST               'gmtoff_remainder'

 L. 466      1416  LOAD_STR                 '0'
             1418  LOAD_CONST               6
             1420  LOAD_GLOBAL              len
             1422  LOAD_FAST                'gmtoff_remainder'
             1424  CALL_FUNCTION_1       1  ''
             1426  BINARY_SUBTRACT  
             1428  BINARY_MULTIPLY  
             1430  STORE_FAST               'gmtoff_remainder_padding'

 L. 467      1432  LOAD_GLOBAL              int
             1434  LOAD_FAST                'gmtoff_remainder'
             1436  LOAD_FAST                'gmtoff_remainder_padding'
             1438  BINARY_ADD       
             1440  CALL_FUNCTION_1       1  ''
             1442  STORE_FAST               'gmtoff_fraction'

 L. 468      1444  LOAD_FAST                'z'
             1446  LOAD_METHOD              startswith
             1448  LOAD_STR                 '-'
             1450  CALL_METHOD_1         1  ''
         1452_1454  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 469      1456  LOAD_FAST                'gmtoff'
             1458  UNARY_NEGATIVE   
             1460  STORE_FAST               'gmtoff'

 L. 470      1462  LOAD_FAST                'gmtoff_fraction'
             1464  UNARY_NEGATIVE   
             1466  STORE_FAST               'gmtoff_fraction'
           1468_0  COME_FROM          1212  '1212'
             1468  JUMP_BACK           458  'to 458'
           1470_0  COME_FROM          1186  '1186'

 L. 471      1470  LOAD_FAST                'group_key'
             1472  LOAD_STR                 'Z'
             1474  COMPARE_OP               ==
         1476_1478  POP_JUMP_IF_FALSE   458  'to 458'

 L. 474      1480  LOAD_FAST                'found_dict'
             1482  LOAD_STR                 'Z'
             1484  BINARY_SUBSCR    
             1486  LOAD_METHOD              lower
             1488  CALL_METHOD_0         0  ''
             1490  STORE_FAST               'found_zone'

 L. 475      1492  LOAD_GLOBAL              enumerate
             1494  LOAD_FAST                'locale_time'
             1496  LOAD_ATTR                timezone
             1498  CALL_FUNCTION_1       1  ''
             1500  GET_ITER         
           1502_0  COME_FROM          1516  '1516'
             1502  FOR_ITER           1582  'to 1582'
             1504  UNPACK_SEQUENCE_2     2 
             1506  STORE_FAST               'value'
             1508  STORE_FAST               'tz_values'

 L. 476      1510  LOAD_FAST                'found_zone'
             1512  LOAD_FAST                'tz_values'
             1514  COMPARE_OP               in
         1516_1518  POP_JUMP_IF_FALSE  1502  'to 1502'

 L. 480      1520  LOAD_GLOBAL              time
             1522  LOAD_ATTR                tzname
             1524  LOAD_CONST               0
             1526  BINARY_SUBSCR    
             1528  LOAD_GLOBAL              time
             1530  LOAD_ATTR                tzname
             1532  LOAD_CONST               1
             1534  BINARY_SUBSCR    
             1536  COMPARE_OP               ==
         1538_1540  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 481      1542  LOAD_GLOBAL              time
             1544  LOAD_ATTR                daylight

 L. 480  1546_1548  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 481      1550  LOAD_FAST                'found_zone'
             1552  LOAD_CONST               ('utc', 'gmt')
             1554  COMPARE_OP               not-in

 L. 480  1556_1558  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 482      1560  POP_TOP          
         1562_1564  CONTINUE            458  'to 458'
             1566  JUMP_BACK          1502  'to 1502'
           1568_0  COME_FROM          1556  '1556'
           1568_1  COME_FROM          1546  '1546'
           1568_2  COME_FROM          1538  '1538'

 L. 484      1568  LOAD_FAST                'value'
             1570  STORE_FAST               'tz'

 L. 485      1572  POP_TOP          
         1574_1576  CONTINUE            458  'to 458'
         1578_1580  JUMP_BACK          1502  'to 1502'
           1582_0  COME_FROM          1452  '1452'
           1582_1  COME_FROM           812  '812'
           1582_2  COME_FROM           802  '802'
         1582_1584  JUMP_BACK           458  'to 458'

 L. 488      1586  LOAD_FAST                'year'
             1588  LOAD_CONST               None
             1590  COMPARE_OP               is
         1592_1594  POP_JUMP_IF_FALSE  1654  'to 1654'
             1596  LOAD_FAST                'iso_year'
             1598  LOAD_CONST               None
             1600  COMPARE_OP               is-not
         1602_1604  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 489      1606  LOAD_FAST                'iso_week'
             1608  LOAD_CONST               None
             1610  COMPARE_OP               is
         1612_1614  POP_JUMP_IF_TRUE   1626  'to 1626'
             1616  LOAD_FAST                'weekday'
             1618  LOAD_CONST               None
             1620  COMPARE_OP               is
         1622_1624  POP_JUMP_IF_FALSE  1634  'to 1634'
           1626_0  COME_FROM          1612  '1612'

 L. 490      1626  LOAD_GLOBAL              ValueError
             1628  LOAD_STR                 "ISO year directive '%G' must be used with the ISO week directive '%V' and a weekday directive ('%A', '%a', '%w', or '%u')."
             1630  CALL_FUNCTION_1       1  ''
             1632  RAISE_VARARGS_1       1  'exception instance'
           1634_0  COME_FROM          1622  '1622'

 L. 493      1634  LOAD_FAST                'julian'
             1636  LOAD_CONST               None
             1638  COMPARE_OP               is-not
         1640_1642  POP_JUMP_IF_FALSE  1702  'to 1702'

 L. 494      1644  LOAD_GLOBAL              ValueError
             1646  LOAD_STR                 "Day of the year directive '%j' is not compatible with ISO year directive '%G'. Use '%Y' instead."
             1648  CALL_FUNCTION_1       1  ''
             1650  RAISE_VARARGS_1       1  'exception instance'
             1652  JUMP_FORWARD       1702  'to 1702'
           1654_0  COME_FROM          1602  '1602'
           1654_1  COME_FROM          1592  '1592'

 L. 497      1654  LOAD_FAST                'week_of_year'
             1656  LOAD_CONST               None
             1658  COMPARE_OP               is
         1660_1662  POP_JUMP_IF_FALSE  1702  'to 1702'
             1664  LOAD_FAST                'iso_week'
             1666  LOAD_CONST               None
             1668  COMPARE_OP               is-not
         1670_1672  POP_JUMP_IF_FALSE  1702  'to 1702'

 L. 498      1674  LOAD_FAST                'weekday'
             1676  LOAD_CONST               None
             1678  COMPARE_OP               is
         1680_1682  POP_JUMP_IF_FALSE  1694  'to 1694'

 L. 499      1684  LOAD_GLOBAL              ValueError
             1686  LOAD_STR                 "ISO week directive '%V' must be used with the ISO year directive '%G' and a weekday directive ('%A', '%a', '%w', or '%u')."
             1688  CALL_FUNCTION_1       1  ''
             1690  RAISE_VARARGS_1       1  'exception instance'
             1692  JUMP_FORWARD       1702  'to 1702'
           1694_0  COME_FROM          1680  '1680'

 L. 503      1694  LOAD_GLOBAL              ValueError
             1696  LOAD_STR                 "ISO week directive '%V' is incompatible with the year directive '%Y'. Use the ISO year '%G' instead."
             1698  CALL_FUNCTION_1       1  ''
             1700  RAISE_VARARGS_1       1  'exception instance'
           1702_0  COME_FROM          1692  '1692'
           1702_1  COME_FROM          1670  '1670'
           1702_2  COME_FROM          1660  '1660'
           1702_3  COME_FROM          1652  '1652'
           1702_4  COME_FROM          1640  '1640'

 L. 507      1702  LOAD_CONST               False
             1704  STORE_FAST               'leap_year_fix'

 L. 508      1706  LOAD_FAST                'year'
             1708  LOAD_CONST               None
             1710  COMPARE_OP               is
         1712_1714  POP_JUMP_IF_FALSE  1746  'to 1746'
             1716  LOAD_FAST                'month'
             1718  LOAD_CONST               2
             1720  COMPARE_OP               ==
         1722_1724  POP_JUMP_IF_FALSE  1746  'to 1746'
             1726  LOAD_FAST                'day'
             1728  LOAD_CONST               29
             1730  COMPARE_OP               ==
         1732_1734  POP_JUMP_IF_FALSE  1746  'to 1746'

 L. 509      1736  LOAD_CONST               1904
             1738  STORE_FAST               'year'

 L. 510      1740  LOAD_CONST               True
             1742  STORE_FAST               'leap_year_fix'
             1744  JUMP_FORWARD       1760  'to 1760'
           1746_0  COME_FROM          1732  '1732'
           1746_1  COME_FROM          1722  '1722'
           1746_2  COME_FROM          1712  '1712'

 L. 511      1746  LOAD_FAST                'year'
             1748  LOAD_CONST               None
             1750  COMPARE_OP               is
         1752_1754  POP_JUMP_IF_FALSE  1760  'to 1760'

 L. 512      1756  LOAD_CONST               1900
             1758  STORE_FAST               'year'
           1760_0  COME_FROM          1752  '1752'
           1760_1  COME_FROM          1744  '1744'

 L. 517      1760  LOAD_FAST                'julian'
             1762  LOAD_CONST               None
             1764  COMPARE_OP               is
         1766_1768  POP_JUMP_IF_FALSE  1920  'to 1920'
             1770  LOAD_FAST                'weekday'
             1772  LOAD_CONST               None
             1774  COMPARE_OP               is-not
         1776_1778  POP_JUMP_IF_FALSE  1920  'to 1920'

 L. 518      1780  LOAD_FAST                'week_of_year'
             1782  LOAD_CONST               None
             1784  COMPARE_OP               is-not
         1786_1788  POP_JUMP_IF_FALSE  1824  'to 1824'

 L. 519      1790  LOAD_FAST                'week_of_year_start'
             1792  LOAD_CONST               0
             1794  COMPARE_OP               ==
         1796_1798  POP_JUMP_IF_FALSE  1804  'to 1804'
             1800  LOAD_CONST               True
             1802  JUMP_FORWARD       1806  'to 1806'
           1804_0  COME_FROM          1796  '1796'
             1804  LOAD_CONST               False
           1806_0  COME_FROM          1802  '1802'
             1806  STORE_FAST               'week_starts_Mon'

 L. 520      1808  LOAD_GLOBAL              _calc_julian_from_U_or_W
             1810  LOAD_FAST                'year'
             1812  LOAD_FAST                'week_of_year'
             1814  LOAD_FAST                'weekday'

 L. 521      1816  LOAD_FAST                'week_starts_Mon'

 L. 520      1818  CALL_FUNCTION_4       4  ''
             1820  STORE_FAST               'julian'
             1822  JUMP_FORWARD       1864  'to 1864'
           1824_0  COME_FROM          1786  '1786'

 L. 522      1824  LOAD_FAST                'iso_year'
             1826  LOAD_CONST               None
             1828  COMPARE_OP               is-not
         1830_1832  POP_JUMP_IF_FALSE  1864  'to 1864'
             1834  LOAD_FAST                'iso_week'
             1836  LOAD_CONST               None
             1838  COMPARE_OP               is-not
         1840_1842  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 523      1844  LOAD_GLOBAL              _calc_julian_from_V
             1846  LOAD_FAST                'iso_year'
             1848  LOAD_FAST                'iso_week'
             1850  LOAD_FAST                'weekday'
             1852  LOAD_CONST               1
             1854  BINARY_ADD       
             1856  CALL_FUNCTION_3       3  ''
             1858  UNPACK_SEQUENCE_2     2 
             1860  STORE_FAST               'year'
             1862  STORE_FAST               'julian'
           1864_0  COME_FROM          1840  '1840'
           1864_1  COME_FROM          1830  '1830'
           1864_2  COME_FROM          1822  '1822'

 L. 524      1864  LOAD_FAST                'julian'
             1866  LOAD_CONST               None
             1868  COMPARE_OP               is-not
         1870_1872  POP_JUMP_IF_FALSE  1920  'to 1920'
             1874  LOAD_FAST                'julian'
             1876  LOAD_CONST               0
             1878  COMPARE_OP               <=
         1880_1882  POP_JUMP_IF_FALSE  1920  'to 1920'

 L. 525      1884  LOAD_FAST                'year'
             1886  LOAD_CONST               1
             1888  INPLACE_SUBTRACT 
             1890  STORE_FAST               'year'

 L. 526      1892  LOAD_GLOBAL              calendar
             1894  LOAD_METHOD              isleap
             1896  LOAD_FAST                'year'
             1898  CALL_METHOD_1         1  ''
         1900_1902  POP_JUMP_IF_FALSE  1908  'to 1908'
             1904  LOAD_CONST               366
             1906  JUMP_FORWARD       1910  'to 1910'
           1908_0  COME_FROM          1900  '1900'
             1908  LOAD_CONST               365
           1910_0  COME_FROM          1906  '1906'
             1910  STORE_FAST               'yday'

 L. 527      1912  LOAD_FAST                'julian'
             1914  LOAD_FAST                'yday'
             1916  INPLACE_ADD      
             1918  STORE_FAST               'julian'
           1920_0  COME_FROM          1880  '1880'
           1920_1  COME_FROM          1870  '1870'
           1920_2  COME_FROM          1776  '1776'
           1920_3  COME_FROM          1766  '1766'

 L. 529      1920  LOAD_FAST                'julian'
             1922  LOAD_CONST               None
             1924  COMPARE_OP               is
         1926_1928  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 534      1930  LOAD_GLOBAL              datetime_date
             1932  LOAD_FAST                'year'
             1934  LOAD_FAST                'month'
             1936  LOAD_FAST                'day'
             1938  CALL_FUNCTION_3       3  ''
             1940  LOAD_METHOD              toordinal
             1942  CALL_METHOD_0         0  ''

 L. 535      1944  LOAD_GLOBAL              datetime_date
             1946  LOAD_FAST                'year'
             1948  LOAD_CONST               1
             1950  LOAD_CONST               1
             1952  CALL_FUNCTION_3       3  ''
             1954  LOAD_METHOD              toordinal
             1956  CALL_METHOD_0         0  ''

 L. 534      1958  BINARY_SUBTRACT  

 L. 535      1960  LOAD_CONST               1

 L. 534      1962  BINARY_ADD       
             1964  STORE_FAST               'julian'
             1966  JUMP_FORWARD       2016  'to 2016'
           1968_0  COME_FROM          1926  '1926'

 L. 538      1968  LOAD_GLOBAL              datetime_date
             1970  LOAD_METHOD              fromordinal

 L. 539      1972  LOAD_FAST                'julian'
             1974  LOAD_CONST               1
             1976  BINARY_SUBTRACT  

 L. 540      1978  LOAD_GLOBAL              datetime_date
             1980  LOAD_FAST                'year'
             1982  LOAD_CONST               1
             1984  LOAD_CONST               1
             1986  CALL_FUNCTION_3       3  ''
             1988  LOAD_METHOD              toordinal
             1990  CALL_METHOD_0         0  ''

 L. 539      1992  BINARY_ADD       

 L. 538      1994  CALL_METHOD_1         1  ''
             1996  STORE_FAST               'datetime_result'

 L. 541      1998  LOAD_FAST                'datetime_result'
             2000  LOAD_ATTR                year
             2002  STORE_FAST               'year'

 L. 542      2004  LOAD_FAST                'datetime_result'
             2006  LOAD_ATTR                month
             2008  STORE_FAST               'month'

 L. 543      2010  LOAD_FAST                'datetime_result'
             2012  LOAD_ATTR                day
             2014  STORE_FAST               'day'
           2016_0  COME_FROM          1966  '1966'

 L. 544      2016  LOAD_FAST                'weekday'
             2018  LOAD_CONST               None
             2020  COMPARE_OP               is
         2022_2024  POP_JUMP_IF_FALSE  2042  'to 2042'

 L. 545      2026  LOAD_GLOBAL              datetime_date
             2028  LOAD_FAST                'year'
             2030  LOAD_FAST                'month'
             2032  LOAD_FAST                'day'
             2034  CALL_FUNCTION_3       3  ''
             2036  LOAD_METHOD              weekday
             2038  CALL_METHOD_0         0  ''
             2040  STORE_FAST               'weekday'
           2042_0  COME_FROM          2022  '2022'

 L. 547      2042  LOAD_FAST                'found_dict'
             2044  LOAD_METHOD              get
             2046  LOAD_STR                 'Z'
             2048  CALL_METHOD_1         1  ''
             2050  STORE_FAST               'tzname'

 L. 549      2052  LOAD_FAST                'leap_year_fix'
         2054_2056  POP_JUMP_IF_FALSE  2062  'to 2062'

 L. 553      2058  LOAD_CONST               1900
             2060  STORE_FAST               'year'
           2062_0  COME_FROM          2054  '2054'

 L. 555      2062  LOAD_FAST                'year'
             2064  LOAD_FAST                'month'
             2066  LOAD_FAST                'day'

 L. 556      2068  LOAD_FAST                'hour'

 L. 556      2070  LOAD_FAST                'minute'

 L. 556      2072  LOAD_FAST                'second'

 L. 557      2074  LOAD_FAST                'weekday'

 L. 557      2076  LOAD_FAST                'julian'

 L. 557      2078  LOAD_FAST                'tz'

 L. 557      2080  LOAD_FAST                'tzname'

 L. 557      2082  LOAD_FAST                'gmtoff'

 L. 555      2084  BUILD_TUPLE_11       11 

 L. 557      2086  LOAD_FAST                'fraction'

 L. 557      2088  LOAD_FAST                'gmtoff_fraction'

 L. 555      2090  BUILD_TUPLE_3         3 
             2092  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 1574_1576


def _strptime_time(data_string, format='%a %b %d %H:%M:%S %Y'):
    """Return a time struct based on the input string and the
    format string."""
    tt = _strptime(data_string, format)[0]
    return time.struct_time(tt[:time._STRUCT_TM_ITEMS])


def _strptime_datetime(cls, data_string, format='%a %b %d %H:%M:%S %Y'):
    """Return a class cls instance based on the input string and the
    format string."""
    tt, fraction, gmtoff_fraction = _strptime(data_string, format)
    tzname, gmtoff = tt[-2:]
    args = tt[:6] + (fraction,)
    if gmtoff is not None:
        tzdelta = datetime_timedelta(seconds=gmtoff, microseconds=gmtoff_fraction)
        if tzname:
            tz = datetime_timezone(tzdelta, tzname)
        else:
            tz = datetime_timezone(tzdelta)
        args += (tz,)
    return cls(*args)


# global _TimeRE_cache ## Warning: Unused global
# global _regex_cache ## Warning: Unused global