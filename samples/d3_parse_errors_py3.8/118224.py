# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_util.py
"""Utility functions and date/time routines.

 Copyright 2002-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).
"""
from __future__ import absolute_import
import re, time, warnings
from calendar import timegm

class ExperimentalWarning(UserWarning):
    pass


def experimental(message):
    warnings.warn(message, ExperimentalWarning, stacklevel=3)


def hide_experimental_warnings():
    warnings.filterwarnings('ignore', category=ExperimentalWarning)


def reset_experimental_warnings():
    warnings.filterwarnings('default', category=ExperimentalWarning)


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=3)


def hide_deprecations():
    warnings.filterwarnings('ignore', category=DeprecationWarning)


def reset_deprecations():
    warnings.filterwarnings('default', category=DeprecationWarning)


def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()


def write_file(filename, data):
    f = open(filename, 'wb')
    try:
        f.write(data)
    finally:
        f.close()


def get1(sequence):
    assert len(sequence) == 1
    return sequence[0]


def isstringlike(x):
    try:
        x + ''
    except Exception:
        return False
    else:
        return True


EPOCH = 1970

def my_timegm(tt):
    year, month, mday, hour, min, sec = tt[:6]
    if year >= EPOCH:
        if 1 <= month <= 12:
            if 1 <= mday <= 31:
                if 0 <= hour <= 24:
                    if 0 <= min <= 59:
                        if 0 <= sec <= 61:
                            return timegm(tt)
    return


days = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months_lower = []
for month in months:
    months_lower.append(month.lower())
else:

    def time2isoz(t=None):
        """Return a string representing time in seconds since epoch, t.

    If the function is called without an argument, it will use the current
    time.

    The format of the returned string is like "YYYY-MM-DD hh:mm:ssZ",
    representing Universal Time (UTC, aka GMT).  An example of this format is:

    1994-11-24 08:49:37Z

    """
        if t is None:
            t = time.time()
        year, mon, mday, hour, min, sec = time.gmtime(t)[:6]
        return '%04d-%02d-%02d %02d:%02d:%02dZ' % (
         year, mon, mday, hour, min, sec)


    def time2netscape(t=None):
        """Return a string representing time in seconds since epoch, t.

    If the function is called without an argument, it will use the current
    time.

    The format of the returned string is like this:

    Wed, DD-Mon-YYYY HH:MM:SS GMT

    """
        if t is None:
            t = time.time()
        year, mon, mday, hour, min, sec, wday = time.gmtime(t)[:7]
        return '%s %02d-%s-%04d %02d:%02d:%02d GMT' % (
         days[wday], mday, months[(mon - 1)], year, hour, min, sec)


    UTC_ZONES = {'GMT':None, 
     'UTC':None,  'UT':None,  'Z':None}
    timezone_re = re.compile('^([-+])?(\\d\\d?):?(\\d\\d)?$')

    def offset_from_tz_string(tz):
        offset = None
        if tz in UTC_ZONES:
            offset = 0
        else:
            m = timezone_re.search(tz)
            if m:
                offset = 3600 * int(m.group(2))
                if m.group(3):
                    offset = offset + 60 * int(m.group(3))
                if m.group(1) == '-':
                    offset = -offset
        return offset


    def _str2time--- This code section failed: ---

 L. 155         0  SETUP_FINALLY        24  'to 24'

 L. 156         2  LOAD_GLOBAL              months_lower
                4  LOAD_METHOD              index
                6  LOAD_FAST                'mon'
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  CALL_METHOD_1         1  ''
               14  LOAD_CONST               1
               16  BINARY_ADD       
               18  STORE_FAST               'mon'
               20  POP_BLOCK        
               22  JUMP_FORWARD        118  'to 118'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 157        24  DUP_TOP          
               26  LOAD_GLOBAL              ValueError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE   116  'to 116'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 159        38  SETUP_FINALLY        52  'to 52'

 L. 160        40  LOAD_GLOBAL              int
               42  LOAD_FAST                'mon'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'imon'
               48  POP_BLOCK        
               50  JUMP_FORWARD         76  'to 76'
             52_0  COME_FROM_FINALLY    38  '38'

 L. 161        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    74  'to 74'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 162        66  POP_EXCEPT       
               68  POP_EXCEPT       
               70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            58  '58'
               74  END_FINALLY      
             76_0  COME_FROM            50  '50'

 L. 163        76  LOAD_CONST               1
               78  LOAD_FAST                'imon'
               80  DUP_TOP          
               82  ROT_THREE        
               84  COMPARE_OP               <=
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_CONST               12
               90  COMPARE_OP               <=
               92  POP_JUMP_IF_FALSE   106  'to 106'
               94  JUMP_FORWARD        100  'to 100'
             96_0  COME_FROM            86  '86'
               96  POP_TOP          
               98  JUMP_FORWARD        106  'to 106'
            100_0  COME_FROM            94  '94'

 L. 164       100  LOAD_FAST                'imon'
              102  STORE_FAST               'mon'
              104  JUMP_FORWARD        112  'to 112'
            106_0  COME_FROM            98  '98'
            106_1  COME_FROM            92  '92'

 L. 166       106  POP_EXCEPT       
              108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM           104  '104'
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            30  '30'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            22  '22'

 L. 169       118  LOAD_FAST                'hr'
              120  LOAD_CONST               None
              122  COMPARE_OP               is
              124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 170       126  LOAD_CONST               0
              128  STORE_FAST               'hr'
            130_0  COME_FROM           124  '124'

 L. 171       130  LOAD_FAST                'min'
              132  LOAD_CONST               None
              134  COMPARE_OP               is
              136  POP_JUMP_IF_FALSE   142  'to 142'

 L. 172       138  LOAD_CONST               0
              140  STORE_FAST               'min'
            142_0  COME_FROM           136  '136'

 L. 173       142  LOAD_FAST                'sec'
              144  LOAD_CONST               None
              146  COMPARE_OP               is
              148  POP_JUMP_IF_FALSE   154  'to 154'

 L. 174       150  LOAD_CONST               0
              152  STORE_FAST               'sec'
            154_0  COME_FROM           148  '148'

 L. 176       154  LOAD_GLOBAL              int
              156  LOAD_FAST                'yr'
              158  CALL_FUNCTION_1       1  ''
              160  STORE_FAST               'yr'

 L. 177       162  LOAD_GLOBAL              int
              164  LOAD_FAST                'day'
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'day'

 L. 178       170  LOAD_GLOBAL              int
              172  LOAD_FAST                'hr'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'hr'

 L. 179       178  LOAD_GLOBAL              int
              180  LOAD_FAST                'min'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'min'

 L. 180       186  LOAD_GLOBAL              int
              188  LOAD_FAST                'sec'
              190  CALL_FUNCTION_1       1  ''
              192  STORE_FAST               'sec'

 L. 182       194  LOAD_FAST                'yr'
              196  LOAD_CONST               1000
              198  COMPARE_OP               <
          200_202  POP_JUMP_IF_FALSE   296  'to 296'

 L. 184       204  LOAD_GLOBAL              time
              206  LOAD_METHOD              localtime
              208  LOAD_GLOBAL              time
              210  LOAD_METHOD              time
              212  CALL_METHOD_0         0  ''
              214  CALL_METHOD_1         1  ''
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    
              220  STORE_FAST               'cur_yr'

 L. 185       222  LOAD_FAST                'cur_yr'
              224  LOAD_CONST               100
              226  BINARY_MODULO    
              228  STORE_FAST               'm'

 L. 186       230  LOAD_FAST                'yr'
              232  STORE_FAST               'tmp'

 L. 187       234  LOAD_FAST                'yr'
              236  LOAD_FAST                'cur_yr'
              238  BINARY_ADD       
              240  LOAD_FAST                'm'
              242  BINARY_SUBTRACT  
              244  STORE_FAST               'yr'

 L. 188       246  LOAD_FAST                'm'
              248  LOAD_FAST                'tmp'
              250  BINARY_SUBTRACT  
              252  STORE_FAST               'm'

 L. 189       254  LOAD_GLOBAL              abs
              256  LOAD_FAST                'm'
              258  CALL_FUNCTION_1       1  ''
              260  LOAD_CONST               50
              262  COMPARE_OP               >
          264_266  POP_JUMP_IF_FALSE   296  'to 296'

 L. 190       268  LOAD_FAST                'm'
              270  LOAD_CONST               0
              272  COMPARE_OP               >
          274_276  POP_JUMP_IF_FALSE   288  'to 288'

 L. 191       278  LOAD_FAST                'yr'
              280  LOAD_CONST               100
              282  BINARY_ADD       
              284  STORE_FAST               'yr'
              286  JUMP_FORWARD        296  'to 296'
            288_0  COME_FROM           274  '274'

 L. 193       288  LOAD_FAST                'yr'
              290  LOAD_CONST               100
              292  BINARY_SUBTRACT  
              294  STORE_FAST               'yr'
            296_0  COME_FROM           286  '286'
            296_1  COME_FROM           264  '264'
            296_2  COME_FROM           200  '200'

 L. 196       296  LOAD_GLOBAL              my_timegm
              298  LOAD_FAST                'yr'
              300  LOAD_FAST                'mon'
              302  LOAD_FAST                'day'
              304  LOAD_FAST                'hr'
              306  LOAD_FAST                'min'
              308  LOAD_FAST                'sec'
              310  LOAD_FAST                'tz'
              312  BUILD_TUPLE_7         7 
              314  CALL_FUNCTION_1       1  ''
              316  STORE_FAST               't'

 L. 198       318  LOAD_FAST                't'
              320  LOAD_CONST               None
              322  COMPARE_OP               is-not
          324_326  POP_JUMP_IF_FALSE   380  'to 380'

 L. 200       328  LOAD_FAST                'tz'
              330  LOAD_CONST               None
              332  COMPARE_OP               is
          334_336  POP_JUMP_IF_FALSE   342  'to 342'

 L. 201       338  LOAD_STR                 'UTC'
              340  STORE_FAST               'tz'
            342_0  COME_FROM           334  '334'

 L. 202       342  LOAD_FAST                'tz'
              344  LOAD_METHOD              upper
              346  CALL_METHOD_0         0  ''
              348  STORE_FAST               'tz'

 L. 203       350  LOAD_GLOBAL              offset_from_tz_string
              352  LOAD_FAST                'tz'
              354  CALL_FUNCTION_1       1  ''
              356  STORE_FAST               'offset'

 L. 204       358  LOAD_FAST                'offset'
              360  LOAD_CONST               None
              362  COMPARE_OP               is
          364_366  POP_JUMP_IF_FALSE   372  'to 372'

 L. 205       368  LOAD_CONST               None
              370  RETURN_VALUE     
            372_0  COME_FROM           364  '364'

 L. 206       372  LOAD_FAST                't'
              374  LOAD_FAST                'offset'
              376  BINARY_SUBTRACT  
              378  STORE_FAST               't'
            380_0  COME_FROM           324  '324'

 L. 208       380  LOAD_FAST                't'
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 70


    strict_re = re.compile('^[SMTWF][a-z][a-z], (\\d\\d) ([JFMASOND][a-z][a-z]) (\\d\\d\\d\\d) (\\d\\d):(\\d\\d):(\\d\\d) GMT$')
    wkday_re = re.compile('^(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*,?\\s*', re.I)
    loose_http_re = re.compile('^\n    (\\d\\d?)            # day\n       (?:\\s+|[-\\/])\n    (\\w+)              # month\n        (?:\\s+|[-\\/])\n    (\\d+)              # year\n    (?:\n          (?:\\s+|:)    # separator before clock\n       (\\d\\d?):(\\d\\d)  # hour:min\n       (?::(\\d\\d))?    # optional seconds\n    )?                 # optional clock\n       \\s*\n    ([-+]?\\d{2,4}|(?![APap][Mm]\\b)[A-Za-z]+)? # timezone\n       \\s*\n    (?:\\(\\w+\\))?       # ASCII representation of timezone in parens.\n       \\s*$', re.X)

    def http2time(text):
        """Returns time in seconds since epoch of time represented by a string.

    Return value is an integer.

    None is returned if the format of str is unrecognized, the time is outside
    the representable range, or the timezone string is not recognized.  If the
    string contains no timezone, UTC is assumed.

    The timezone in the string may be numerical (like "-0800" or "+0100") or a
    string timezone (like "UTC", "GMT", "BST" or "EST").  Currently, only the
    timezone strings equivalent to UTC (zero offset) are known to the function.

    The function loosely parses the following formats:

    Wed, 09 Feb 1994 22:23:32 GMT       -- HTTP format
    Tuesday, 08-Feb-94 14:15:29 GMT     -- old rfc850 HTTP format
    Tuesday, 08-Feb-1994 14:15:29 GMT   -- broken rfc850 HTTP format
    09 Feb 1994 22:23:32 GMT            -- HTTP format (no weekday)
    08-Feb-94 14:15:29 GMT              -- rfc850 format (no weekday)
    08-Feb-1994 14:15:29 GMT            -- broken rfc850 format (no weekday)

    The parser ignores leading and trailing whitespace.  The time may be
    absent.

    If the year is given with only 2 digits, the function will select the
    century that makes the year closest to the current date.

    """
        m = strict_re.search(text)
        if m:
            g = m.groups()
            mon = months_lower.index(g[1].lower()) + 1
            tt = (int(g[2]), mon, int(g[0]),
             int(g[3]), int(g[4]), float(g[5]))
            return my_timegm(tt)
        text = text.lstrip()
        text = wkday_re.sub('', text, 1)
        day, mon, yr, hr, min, sec, tz = [
         None] * 7
        m = loose_http_re.search(text)
        if m is not None:
            day, mon, yr, hr, min, sec, tz = m.groups()
        else:
            return
        return _str2time(day, mon, yr, hr, min, sec, tz)


    iso_re = re.compile('^\n    (\\d{4})              # year\n       [-\\/]?\n    (\\d\\d?)              # numerical month\n       [-\\/]?\n    (\\d\\d?)              # day\n   (?:\n         (?:\\s+|[-:Tt])  # separator before clock\n      (\\d\\d?):?(\\d\\d)    # hour:min\n      (?::?(\\d\\d(?:\\.\\d*)?))?  # optional seconds (and fractional)\n   )?                    # optional clock\n      \\s*\n   ([-+]?\\d\\d?:?(:?\\d\\d)?\n    |Z|z)?               # timezone  (Z is "zero meridian", i.e. GMT)\n      \\s*$', re.X)

    def iso2time(text):
        """
    As for http2time, but parses the ISO 8601 formats:

    1994-02-03 14:15:29 -0100    -- ISO 8601 format
    1994-02-03 14:15:29          -- zone is optional
    1994-02-03                   -- only date
    1994-02-03T14:15:29          -- Use T as separator
    19940203T141529Z             -- ISO 8601 compact format
    19940203                     -- only date

    """
        text = text.lstrip()
        day, mon, yr, hr, min, sec, tz = [
         None] * 7
        m = iso_re.search(text)
        if m is not None:
            yr, mon, day, hr, min, sec, tz, _ = m.groups()
        else:
            return
        return _str2time(day, mon, yr, hr, min, sec, tz)