# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: C:\Users\Administrator\Desktop\PyInstaller-2.1\send\build\send\out00-PYZ.pyz\cookielib
r"""HTTP cookie handling for web clients.

This module has (now fairly distant) origins in Gisle Aas' Perl module
HTTP::Cookies, from the libwww-perl library.

Docstrings, comments and debug strings in this code refer to the
attributes of the HTTP cookie system as cookie-attributes, to distinguish
them clearly from Python attributes.

Class diagram (note that BSDDBCookieJar and the MSIE* classes are not
distributed with the Python standard library, but are available from
http://wwwsearch.sf.net/):

                        CookieJar____
                        /     \                  FileCookieJar      \                   /    |   \         \       MozillaCookieJar | LWPCookieJar \                        |               |                        |   ---MSIEBase |                         |  /      |     |                          | /   MSIEDBCookieJar BSDDBCookieJar
                  |/
               MSIECookieJar

"""
__all__ = [
 'Cookie', 'CookieJar', 'CookiePolicy', 'DefaultCookiePolicy',
 'FileCookieJar', 'LWPCookieJar', 'lwp_cookie_str', 'LoadError',
 'MozillaCookieJar']
import re, urlparse, copy, time, urllib
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

import httplib
from calendar import timegm
debug = False
logger = None

def _debug(*args):
    global logger
    if not debug:
        return
    if not logger:
        import logging
        logger = logging.getLogger('cookielib')
    return logger.debug(*args)


DEFAULT_HTTP_PORT = str(httplib.HTTP_PORT)
MISSING_FILENAME_TEXT = 'a filename was not supplied (nor was the CookieJar instance initialised with one)'

def _warn_unhandled_exception():
    import warnings, traceback, StringIO
    f = StringIO.StringIO()
    traceback.print_exc(None, f)
    msg = f.getvalue()
    warnings.warn('cookielib bug!\n%s' % msg, stacklevel=2)
    return


EPOCH_YEAR = 1970

def _timegm(tt):
    year, month, mday, hour, min, sec = tt[:6]
    if year >= EPOCH_YEAR and 1 <= month <= 12 and 1 <= mday <= 31 and 0 <= hour <= 24 and 0 <= min <= 59 and 0 <= sec <= 61:
        return timegm(tt)
    else:
        return
        return


DAYS = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTHS_LOWER = []
for month in MONTHS:
    MONTHS_LOWER.append(month.lower())

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
     DAYS[wday], mday, MONTHS[(mon - 1)], year, hour, min, sec)


UTC_ZONES = {'GMT': None, 'UTC': None, 'UT': None, 'Z': None}
TIMEZONE_RE = re.compile('^([-+])?(\\d\\d?):?(\\d\\d)?$')

def offset_from_tz_string(tz):
    offset = None
    if tz in UTC_ZONES:
        offset = 0
    else:
        m = TIMEZONE_RE.search(tz)
        if m:
            offset = 3600 * int(m.group(2))
            if m.group(3):
                offset = offset + 60 * int(m.group(3))
            if m.group(1) == '-':
                offset = -offset
    return offset


def _str2time(day, mon, yr, hr, min, sec, tz):
    try:
        mon = MONTHS_LOWER.index(mon.lower()) + 1
    except ValueError:
        try:
            imon = int(mon)
        except ValueError:
            return

        if 1 <= imon <= 12:
            mon = imon
        else:
            return

    if hr is None:
        hr = 0
    if min is None:
        min = 0
    if sec is None:
        sec = 0
    yr = int(yr)
    day = int(day)
    hr = int(hr)
    min = int(min)
    sec = int(sec)
    if yr < 1000:
        cur_yr = time.localtime(time.time())[0]
        m = cur_yr % 100
        tmp = yr
        yr = yr + cur_yr - m
        m = m - tmp
        if abs(m) > 50:
            if m > 0:
                yr = yr + 100
            else:
                yr = yr - 100
    t = _timegm((yr, mon, day, hr, min, sec, tz))
    if t is not None:
        if tz is None:
            tz = 'UTC'
        tz = tz.upper()
        offset = offset_from_tz_string(tz)
        if offset is None:
            return
        t = t - offset
    return t


STRICT_DATE_RE = re.compile('^[SMTWF][a-z][a-z], (\\d\\d) ([JFMASOND][a-z][a-z]) (\\d\\d\\d\\d) (\\d\\d):(\\d\\d):(\\d\\d) GMT$')
WEEKDAY_RE = re.compile('^(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*,?\\s*', re.I)
LOOSE_HTTP_DATE_RE = re.compile('^\n    (\\d\\d?)            # day\n       (?:\\s+|[-\\/])\n    (\\w+)              # month\n        (?:\\s+|[-\\/])\n    (\\d+)              # year\n    (?:\n          (?:\\s+|:)    # separator before clock\n       (\\d\\d?):(\\d\\d)  # hour:min\n       (?::(\\d\\d))?    # optional seconds\n    )?                 # optional clock\n       \\s*\n    ([-+]?\\d{2,4}|(?![APap][Mm]\\b)[A-Za-z]+)? # timezone\n       \\s*\n    (?:\\(\\w+\\))?       # ASCII representation of timezone in parens.\n       \\s*$', re.X)

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
    m = STRICT_DATE_RE.search(text)
    if m:
        g = m.groups()
        mon = MONTHS_LOWER.index(g[1].lower()) + 1
        tt = (int(g[2]), mon, int(g[0]),
         int(g[3]), int(g[4]), float(g[5]))
        return _timegm(tt)
    else:
        text = text.lstrip()
        text = WEEKDAY_RE.sub('', text, 1)
        day, mon, yr, hr, min, sec, tz = [
         None] * 7
        m = LOOSE_HTTP_DATE_RE.search(text)
        if m is not None:
            day, mon, yr, hr, min, sec, tz = m.groups()
        else:
            return
        return _str2time(day, mon, yr, hr, min, sec, tz)


ISO_DATE_RE = re.compile('^\n    (\\d{4})              # year\n       [-\\/]?\n    (\\d\\d?)              # numerical month\n       [-\\/]?\n    (\\d\\d?)              # day\n   (?:\n         (?:\\s+|[-:Tt])  # separator before clock\n      (\\d\\d?):?(\\d\\d)    # hour:min\n      (?::?(\\d\\d(?:\\.\\d*)?))?  # optional seconds (and fractional)\n   )?                    # optional clock\n      \\s*\n   ([-+]?\\d\\d?:?(:?\\d\\d)?\n    |Z|z)?               # timezone  (Z is "zero meridian", i.e. GMT)\n      \\s*$', re.X)

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
    m = ISO_DATE_RE.search(text)
    if m is not None:
        yr, mon, day, hr, min, sec, tz, _ = m.groups()
    else:
        return
    return _str2time(day, mon, yr, hr, min, sec, tz)


def unmatched(match):
    """Return unmatched part of re.Match object."""
    start, end = match.span(0)
    return match.string[:start] + match.string[end:]


HEADER_TOKEN_RE = re.compile('^\\s*([^=\\s;,]+)')
HEADER_QUOTED_VALUE_RE = re.compile('^\\s*=\\s*\\"([^\\"\\\\]*(?:\\\\.[^\\"\\\\]*)*)\\"')
HEADER_VALUE_RE = re.compile('^\\s*=\\s*([^\\s;,]*)')
HEADER_ESCAPE_RE = re.compile('\\\\(.)')

def split_header_words--- This code section failed: ---

 L. 371         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'header_values'
                6  LOAD_GLOBAL           1  'basestring'
                9  CALL_FUNCTION_2       2  None
               12  UNARY_NOT        
               13  POP_JUMP_IF_TRUE     22  'to 22'
               16  LOAD_ASSERT              AssertionError
               19  RAISE_VARARGS_1       1  None

 L. 372        22  BUILD_LIST_0          0 
               25  STORE_FAST            1  'result'

 L. 373        28  SETUP_LOOP          404  'to 435'
               31  LOAD_FAST             0  'header_values'
               34  GET_ITER         
               35  FOR_ITER            396  'to 434'
               38  STORE_FAST            2  'text'

 L. 374        41  LOAD_FAST             2  'text'
               44  STORE_FAST            3  'orig_text'

 L. 375        47  BUILD_LIST_0          0 
               50  STORE_FAST            4  'pairs'

 L. 376        53  SETUP_LOOP          353  'to 409'
               56  LOAD_FAST             2  'text'
               59  POP_JUMP_IF_FALSE   408  'to 408'

 L. 377        62  LOAD_GLOBAL           3  'HEADER_TOKEN_RE'
               65  LOAD_ATTR             4  'search'
               68  LOAD_FAST             2  'text'
               71  CALL_FUNCTION_1       1  None
               74  STORE_FAST            5  'm'

 L. 378        77  LOAD_FAST             5  'm'
               80  POP_JUMP_IF_FALSE   270  'to 270'

 L. 379        83  LOAD_GLOBAL           5  'unmatched'
               86  LOAD_FAST             5  'm'
               89  CALL_FUNCTION_1       1  None
               92  STORE_FAST            2  'text'

 L. 380        95  LOAD_FAST             5  'm'
               98  LOAD_ATTR             6  'group'
              101  LOAD_CONST               1
              104  CALL_FUNCTION_1       1  None
              107  STORE_FAST            6  'name'

 L. 381       110  LOAD_GLOBAL           7  'HEADER_QUOTED_VALUE_RE'
              113  LOAD_ATTR             4  'search'
              116  LOAD_FAST             2  'text'
              119  CALL_FUNCTION_1       1  None
              122  STORE_FAST            5  'm'

 L. 382       125  LOAD_FAST             5  'm'
              128  POP_JUMP_IF_FALSE   179  'to 179'

 L. 383       131  LOAD_GLOBAL           5  'unmatched'
              134  LOAD_FAST             5  'm'
              137  CALL_FUNCTION_1       1  None
              140  STORE_FAST            2  'text'

 L. 384       143  LOAD_FAST             5  'm'
              146  LOAD_ATTR             6  'group'
              149  LOAD_CONST               1
              152  CALL_FUNCTION_1       1  None
              155  STORE_FAST            7  'value'

 L. 385       158  LOAD_GLOBAL           8  'HEADER_ESCAPE_RE'
              161  LOAD_ATTR             9  'sub'
              164  LOAD_CONST               '\\1'
              167  LOAD_FAST             7  'value'
              170  CALL_FUNCTION_2       2  None
              173  STORE_FAST            7  'value'
              176  JUMP_FORWARD         69  'to 248'

 L. 387       179  LOAD_GLOBAL          10  'HEADER_VALUE_RE'
              182  LOAD_ATTR             4  'search'
              185  LOAD_FAST             2  'text'
              188  CALL_FUNCTION_1       1  None
              191  STORE_FAST            5  'm'

 L. 388       194  LOAD_FAST             5  'm'
              197  POP_JUMP_IF_FALSE   242  'to 242'

 L. 389       200  LOAD_GLOBAL           5  'unmatched'
              203  LOAD_FAST             5  'm'
              206  CALL_FUNCTION_1       1  None
              209  STORE_FAST            2  'text'

 L. 390       212  LOAD_FAST             5  'm'
              215  LOAD_ATTR             6  'group'
              218  LOAD_CONST               1
              221  CALL_FUNCTION_1       1  None
              224  STORE_FAST            7  'value'

 L. 391       227  LOAD_FAST             7  'value'
              230  LOAD_ATTR            11  'rstrip'
              233  CALL_FUNCTION_0       0  None
              236  STORE_FAST            7  'value'
              239  JUMP_FORWARD          6  'to 248'

 L. 394       242  LOAD_CONST               None
              245  STORE_FAST            7  'value'
            248_0  COME_FROM           239  '239'
            248_1  COME_FROM           176  '176'

 L. 395       248  LOAD_FAST             4  'pairs'
              251  LOAD_ATTR            13  'append'
              254  LOAD_FAST             6  'name'
              257  LOAD_FAST             7  'value'
              260  BUILD_TUPLE_2         2 
              263  CALL_FUNCTION_1       1  None
              266  POP_TOP          
              267  JUMP_BACK            56  'to 56'

 L. 396       270  LOAD_FAST             2  'text'
              273  LOAD_ATTR            14  'lstrip'
              276  CALL_FUNCTION_0       0  None
              279  LOAD_ATTR            15  'startswith'
              282  LOAD_CONST               ','
              285  CALL_FUNCTION_1       1  None
              288  POP_JUMP_IF_FALSE   338  'to 338'

 L. 398       291  LOAD_FAST             2  'text'
              294  LOAD_ATTR            14  'lstrip'
              297  CALL_FUNCTION_0       0  None
              300  LOAD_CONST               1
              303  SLICE+1          
              304  STORE_FAST            2  'text'

 L. 399       307  LOAD_FAST             4  'pairs'
              310  POP_JUMP_IF_FALSE   329  'to 329'
              313  LOAD_FAST             1  'result'
              316  LOAD_ATTR            13  'append'
              319  LOAD_FAST             4  'pairs'
              322  CALL_FUNCTION_1       1  None
              325  POP_TOP          
              326  JUMP_FORWARD          0  'to 329'
            329_0  COME_FROM           326  '326'

 L. 400       329  BUILD_LIST_0          0 
              332  STORE_FAST            4  'pairs'
              335  JUMP_BACK            56  'to 56'

 L. 403       338  LOAD_GLOBAL          16  're'
              341  LOAD_ATTR            17  'subn'
              344  LOAD_CONST               '^[=\\s;]*'
              347  LOAD_CONST               ''
              350  LOAD_FAST             2  'text'
              353  CALL_FUNCTION_3       3  None
              356  UNPACK_SEQUENCE_2     2 
              359  STORE_FAST            8  'non_junk'
              362  STORE_FAST            9  'nr_junk_chars'

 L. 404       365  LOAD_FAST             9  'nr_junk_chars'
              368  LOAD_CONST               0
              371  COMPARE_OP            4  >
              374  POP_JUMP_IF_TRUE    399  'to 399'
              377  LOAD_ASSERT              AssertionError

 L. 405       380  LOAD_CONST               "split_header_words bug: '%s', '%s', %s"

 L. 406       383  LOAD_FAST             3  'orig_text'
              386  LOAD_FAST             2  'text'
              389  LOAD_FAST             4  'pairs'
              392  BUILD_TUPLE_3         3 
              395  BINARY_MODULO    
              396  RAISE_VARARGS_2       2  None

 L. 407       399  LOAD_FAST             8  'non_junk'
              402  STORE_FAST            2  'text'
              405  JUMP_BACK            56  'to 56'
              408  POP_BLOCK        
            409_0  COME_FROM            53  '53'

 L. 408       409  LOAD_FAST             4  'pairs'
              412  POP_JUMP_IF_FALSE    35  'to 35'
              415  LOAD_FAST             1  'result'
              418  LOAD_ATTR            13  'append'
              421  LOAD_FAST             4  'pairs'
              424  CALL_FUNCTION_1       1  None
              427  POP_TOP          
              428  JUMP_BACK            35  'to 35'
              431  JUMP_BACK            35  'to 35'
              434  POP_BLOCK        
            435_0  COME_FROM            28  '28'

 L. 409       435  LOAD_FAST             1  'result'
              438  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 408


HEADER_JOIN_ESCAPE_RE = re.compile('([\\"\\\\])')

def join_header_words(lists):
    """Do the inverse (almost) of the conversion done by split_header_words.

    Takes a list of lists of (key, value) pairs and produces a single header
    value.  Attribute values are quoted if needed.

    >>> join_header_words([[("text/plain", None), ("charset", "iso-8859/1")]])
    'text/plain; charset="iso-8859/1"'
    >>> join_header_words([[("text/plain", None)], [("charset", "iso-8859/1")]])
    'text/plain, charset="iso-8859/1"'

    """
    headers = []
    for pairs in lists:
        attr = []
        for k, v in pairs:
            if v is not None:
                if not re.search('^\\w+$', v):
                    v = HEADER_JOIN_ESCAPE_RE.sub('\\\\\\1', v)
                    v = '"%s"' % v
                k = '%s=%s' % (k, v)
            attr.append(k)

        if attr:
            headers.append(('; ').join(attr))

    return (', ').join(headers)


def _strip_quotes(text):
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]
    return text


def parse_ns_headers(ns_headers):
    """Ad-hoc parser for Netscape protocol cookie-attributes.

    The old Netscape cookie format for Set-Cookie can for instance contain
    an unquoted "," in the expires field, so we have to use this ad-hoc
    parser instead of split_header_words.

    XXX This may not make the best possible effort to parse all the crap
    that Netscape Cookie headers contain.  Ronald Tschalar's HTTPClient
    parser is probably better, so could do worse than following that if
    this ever gives any trouble.

    Currently, this is also used for parsing RFC 2109 cookies.

    """
    known_attrs = ('expires', 'domain', 'path', 'secure', 'version', 'port', 'max-age')
    result = []
    for ns_header in ns_headers:
        pairs = []
        version_set = False
        for ii, param in enumerate(re.split(';\\s*', ns_header)):
            param = param.rstrip()
            if param == '':
                continue
            if '=' not in param:
                k, v = param, None
            else:
                k, v = re.split('\\s*=\\s*', param, 1)
                k = k.lstrip()
            if ii != 0:
                lc = k.lower()
                if lc in known_attrs:
                    k = lc
                if k == 'version':
                    v = _strip_quotes(v)
                    version_set = True
                if k == 'expires':
                    v = http2time(_strip_quotes(v))
            pairs.append((k, v))

        if pairs:
            if not version_set:
                pairs.append(('version', '0'))
            result.append(pairs)

    return result


IPV4_RE = re.compile('\\.\\d+$')

def is_HDN(text):
    """Return True if text is a host domain name."""
    if IPV4_RE.search(text):
        return False
    if text == '':
        return False
    if text[0] == '.' or text[(-1)] == '.':
        return False
    return True


def domain_match(A, B):
    """Return True if domain A domain-matches domain B, according to RFC 2965.

    A and B may be host domain names or IP addresses.

    RFC 2965, section 1:

    Host names can be specified either as an IP address or a HDN string.
    Sometimes we compare one host name with another.  (Such comparisons SHALL
    be case-insensitive.)  Host A's name domain-matches host B's if

         *  their host name strings string-compare equal; or

         * A is a HDN string and has the form NB, where N is a non-empty
            name string, B has the form .B', and B' is a HDN string.  (So,
            x.y.com domain-matches .Y.com but not Y.com.)

    Note that domain-match is not a commutative operation: a.b.c.com
    domain-matches .c.com, but not the reverse.

    """
    A = A.lower()
    B = B.lower()
    if A == B:
        return True
    if not is_HDN(A):
        return False
    i = A.rfind(B)
    if i == -1 or i == 0:
        return False
    if not B.startswith('.'):
        return False
    if not is_HDN(B[1:]):
        return False
    return True


def liberal_is_HDN(text):
    """Return True if text is a sort-of-like a host domain name.

    For accepting/blocking domains.

    """
    if IPV4_RE.search(text):
        return False
    return True


def user_domain_match(A, B):
    """For blocking/accepting domains.

    A and B may be host domain names or IP addresses.

    """
    A = A.lower()
    B = B.lower()
    if not (liberal_is_HDN(A) and liberal_is_HDN(B)):
        if A == B:
            return True
        return False
    initial_dot = B.startswith('.')
    if initial_dot and A.endswith(B):
        return True
    if not initial_dot and A == B:
        return True
    return False


cut_port_re = re.compile(':\\d+$')

def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    url = request.get_full_url()
    host = urlparse.urlparse(url)[1]
    if host == '':
        host = request.get_header('Host', '')
    host = cut_port_re.sub('', host, 1)
    return host.lower()


def eff_request_host(request):
    """Return a tuple (request-host, effective request-host name).

    As defined by RFC 2965, except both are lowercased.

    """
    erhn = req_host = request_host(request)
    if req_host.find('.') == -1 and not IPV4_RE.search(req_host):
        erhn = req_host + '.local'
    return (
     req_host, erhn)


def request_path(request):
    """request-URI, as defined by RFC 2965."""
    url = request.get_full_url()
    path, parameters, query, frag = urlparse.urlparse(url)[2:]
    if parameters:
        path = '%s;%s' % (path, parameters)
    path = escape_path(path)
    req_path = urlparse.urlunparse(('', '', path, '', query, frag))
    if not req_path.startswith('/'):
        req_path = '/' + req_path
    return req_path


def request_port(request):
    host = request.get_host()
    i = host.find(':')
    if i >= 0:
        port = host[i + 1:]
        try:
            int(port)
        except ValueError:
            _debug("nonnumeric port: '%s'", port)
            return

    else:
        port = DEFAULT_HTTP_PORT
    return port


HTTP_PATH_SAFE = "%/;:@&=+$,!~*'()"
ESCAPED_CHAR_RE = re.compile('%([0-9a-fA-F][0-9a-fA-F])')

def uppercase_escaped_char(match):
    return '%%%s' % match.group(1).upper()


def escape_path(path):
    """Escape any invalid characters in HTTP URL, and uppercase all escapes."""
    if isinstance(path, unicode):
        path = path.encode('utf-8')
    path = urllib.quote(path, HTTP_PATH_SAFE)
    path = ESCAPED_CHAR_RE.sub(uppercase_escaped_char, path)
    return path


def reach(h):
    """Return reach of host h, as defined by RFC 2965, section 1.

    The reach R of a host name H is defined as follows:

       *  If

          -  H is the host domain name of a host; and,

          -  H has the form A.B; and

          -  A has no embedded (that is, interior) dots; and

          -  B has at least one embedded dot, or B is the string "local".
             then the reach of H is .B.

       *  Otherwise, the reach of H is H.

    >>> reach("www.acme.com")
    '.acme.com'
    >>> reach("acme.com")
    'acme.com'
    >>> reach("acme.local")
    '.local'

    """
    i = h.find('.')
    if i >= 0:
        b = h[i + 1:]
        i = b.find('.')
        if is_HDN(h) and (i >= 0 or b == 'local'):
            return '.' + b
    return h


def is_third_party(request):
    """

    RFC 2965, section 3.3.6:

        An unverifiable transaction is to a third-party host if its request-
        host U does not domain-match the reach R of the request-host O in the
        origin transaction.

    """
    req_host = request_host(request)
    if not domain_match(req_host, reach(request.get_origin_req_host())):
        return True
    else:
        return False


class Cookie():
    """HTTP Cookie.

    This class represents both Netscape and RFC 2965 cookies.

    This is deliberately a very simple class.  It just holds attributes.  It's
    possible to construct Cookie instances that don't comply with the cookie
    standards.  CookieJar.make_cookies is the factory function for Cookie
    objects -- it deals with cookie parsing, supplying defaults, and
    normalising to the representation used in this class.  CookiePolicy is
    responsible for checking them to see whether they should be accepted from
    and returned to the server.

    Note that the port may be present in the headers, but unspecified ("Port"
    rather than"Port=80", for example); if this is the case, port is None.

    """

    def __init__(self, version, name, value, port, port_specified, domain, domain_specified, domain_initial_dot, path, path_specified, secure, expires, discard, comment, comment_url, rest, rfc2109=False):
        if version is not None:
            version = int(version)
        if expires is not None:
            expires = int(expires)
        if port is None and port_specified is True:
            raise ValueError('if port is None, port_specified must be false')
        self.version = version
        self.name = name
        self.value = value
        self.port = port
        self.port_specified = port_specified
        self.domain = domain.lower()
        self.domain_specified = domain_specified
        self.domain_initial_dot = domain_initial_dot
        self.path = path
        self.path_specified = path_specified
        self.secure = secure
        self.expires = expires
        self.discard = discard
        self.comment = comment
        self.comment_url = comment_url
        self.rfc2109 = rfc2109
        self._rest = copy.copy(rest)
        return

    def has_nonstandard_attr(self, name):
        return name in self._rest

    def get_nonstandard_attr(self, name, default=None):
        return self._rest.get(name, default)

    def set_nonstandard_attr(self, name, value):
        self._rest[name] = value

    def is_expired(self, now=None):
        if now is None:
            now = time.time()
        if self.expires is not None and self.expires <= now:
            return True
        else:
            return False

    def __str__(self):
        if self.port is None:
            p = ''
        else:
            p = ':' + self.port
        limit = self.domain + p + self.path
        if self.value is not None:
            namevalue = '%s=%s' % (self.name, self.value)
        else:
            namevalue = self.name
        return '<Cookie %s for %s>' % (namevalue, limit)

    def __repr__(self):
        args = []
        for name in ('version', 'name', 'value', 'port', 'port_specified', 'domain',
                     'domain_specified', 'domain_initial_dot', 'path', 'path_specified',
                     'secure', 'expires', 'discard', 'comment', 'comment_url'):
            attr = getattr(self, name)
            args.append('%s=%s' % (name, repr(attr)))

        args.append('rest=%s' % repr(self._rest))
        args.append('rfc2109=%s' % repr(self.rfc2109))
        return 'Cookie(%s)' % (', ').join(args)


class CookiePolicy():
    """Defines which cookies get accepted from and returned to server.

    May also modify cookies, though this is probably a bad idea.

    The subclass DefaultCookiePolicy defines the standard rules for Netscape
    and RFC 2965 cookies -- override that if you want a customised policy.

    """

    def set_ok(self, cookie, request):
        """Return true if (and only if) cookie should be accepted from server.

        Currently, pre-expired cookies never get this far -- the CookieJar
        class deletes such cookies itself.

        """
        raise NotImplementedError()

    def return_ok(self, cookie, request):
        """Return true if (and only if) cookie should be returned to server."""
        raise NotImplementedError()

    def domain_return_ok(self, domain, request):
        """Return false if cookies should not be returned, given cookie domain.
        """
        return True

    def path_return_ok(self, path, request):
        """Return false if cookies should not be returned, given cookie path.
        """
        return True


class DefaultCookiePolicy(CookiePolicy):
    """Implements the standard rules for accepting and returning cookies."""
    DomainStrictNoDots = 1
    DomainStrictNonDomain = 2
    DomainRFC2965Match = 4
    DomainLiberal = 0
    DomainStrict = DomainStrictNoDots | DomainStrictNonDomain

    def __init__(self, blocked_domains=None, allowed_domains=None, netscape=True, rfc2965=False, rfc2109_as_netscape=None, hide_cookie2=False, strict_domain=False, strict_rfc2965_unverifiable=True, strict_ns_unverifiable=False, strict_ns_domain=DomainLiberal, strict_ns_set_initial_dollar=False, strict_ns_set_path=False):
        """Constructor arguments should be passed as keyword arguments only."""
        self.netscape = netscape
        self.rfc2965 = rfc2965
        self.rfc2109_as_netscape = rfc2109_as_netscape
        self.hide_cookie2 = hide_cookie2
        self.strict_domain = strict_domain
        self.strict_rfc2965_unverifiable = strict_rfc2965_unverifiable
        self.strict_ns_unverifiable = strict_ns_unverifiable
        self.strict_ns_domain = strict_ns_domain
        self.strict_ns_set_initial_dollar = strict_ns_set_initial_dollar
        self.strict_ns_set_path = strict_ns_set_path
        if blocked_domains is not None:
            self._blocked_domains = tuple(blocked_domains)
        else:
            self._blocked_domains = ()
        if allowed_domains is not None:
            allowed_domains = tuple(allowed_domains)
        self._allowed_domains = allowed_domains
        return

    def blocked_domains(self):
        """Return the sequence of blocked domains (as a tuple)."""
        return self._blocked_domains

    def set_blocked_domains(self, blocked_domains):
        """Set the sequence of blocked domains."""
        self._blocked_domains = tuple(blocked_domains)

    def is_blocked(self, domain):
        for blocked_domain in self._blocked_domains:
            if user_domain_match(domain, blocked_domain):
                return True

        return False

    def allowed_domains(self):
        """Return None, or the sequence of allowed domains (as a tuple)."""
        return self._allowed_domains

    def set_allowed_domains(self, allowed_domains):
        """Set the sequence of allowed domains, or None."""
        if allowed_domains is not None:
            allowed_domains = tuple(allowed_domains)
        self._allowed_domains = allowed_domains
        return

    def is_not_allowed(self, domain):
        if self._allowed_domains is None:
            return False
        else:
            for allowed_domain in self._allowed_domains:
                if user_domain_match(domain, allowed_domain):
                    return False

            return True

    def set_ok(self, cookie, request):
        """
        If you override .set_ok(), be sure to call this method.  If it returns
        false, so should your subclass (assuming your subclass wants to be more
        strict about which cookies to accept).

        """
        _debug(' - checking cookie %s=%s', cookie.name, cookie.value)
        assert cookie.name is not None
        for n in ('version', 'verifiability', 'name', 'path', 'domain', 'port'):
            fn_name = 'set_ok_' + n
            fn = getattr(self, fn_name)
            if not fn(cookie, request):
                return False

        return True

    def set_ok_version(self, cookie, request):
        if cookie.version is None:
            _debug('   Set-Cookie2 without version attribute (%s=%s)', cookie.name, cookie.value)
            return False
        else:
            if cookie.version > 0 and not self.rfc2965:
                _debug('   RFC 2965 cookies are switched off')
                return False
            if cookie.version == 0 and not self.netscape:
                _debug('   Netscape cookies are switched off')
                return False
            return True

    def set_ok_verifiability(self, cookie, request):
        if request.is_unverifiable() and is_third_party(request):
            if cookie.version > 0 and self.strict_rfc2965_unverifiable:
                _debug('   third-party RFC 2965 cookie during unverifiable transaction')
                return False
            if cookie.version == 0 and self.strict_ns_unverifiable:
                _debug('   third-party Netscape cookie during unverifiable transaction')
                return False
        return True

    def set_ok_name(self, cookie, request):
        if cookie.version == 0 and self.strict_ns_set_initial_dollar and cookie.name.startswith('$'):
            _debug("   illegal name (starts with '$'): '%s'", cookie.name)
            return False
        return True

    def set_ok_path(self, cookie, request):
        if cookie.path_specified:
            req_path = request_path(request)
            if (cookie.version > 0 or cookie.version == 0 and self.strict_ns_set_path) and not req_path.startswith(cookie.path):
                _debug('   path attribute %s is not a prefix of request path %s', cookie.path, req_path)
                return False
        return True

    def set_ok_domain(self, cookie, request):
        if self.is_blocked(cookie.domain):
            _debug('   domain %s is in user block-list', cookie.domain)
            return False
        if self.is_not_allowed(cookie.domain):
            _debug('   domain %s is not in user allow-list', cookie.domain)
            return False
        if cookie.domain_specified:
            req_host, erhn = eff_request_host(request)
            domain = cookie.domain
            if self.strict_domain and domain.count('.') >= 2:
                i = domain.rfind('.')
                j = domain.rfind('.', 0, i)
                if j == 0:
                    tld = domain[i + 1:]
                    sld = domain[j + 1:i]
                    if sld.lower() in ('co', 'ac', 'com', 'edu', 'org', 'net', 'gov',
                                       'mil', 'int', 'aero', 'biz', 'cat', 'coop',
                                       'info', 'jobs', 'mobi', 'museum', 'name',
                                       'pro', 'travel', 'eu') and len(tld) == 2:
                        _debug('   country-code second level domain %s', domain)
                        return False
            if domain.startswith('.'):
                undotted_domain = domain[1:]
            else:
                undotted_domain = domain
            embedded_dots = undotted_domain.find('.') >= 0
            if not embedded_dots and domain != '.local':
                _debug('   non-local domain %s contains no embedded dot', domain)
                return False
            if cookie.version == 0 and not erhn.endswith(domain) and not erhn.startswith('.'):
                if not ('.' + erhn).endswith(domain):
                    _debug('   effective request-host %s (even with added initial dot) does not end end with %s', erhn, domain)
                    return False
            if cookie.version > 0 or self.strict_ns_domain & self.DomainRFC2965Match:
                if not domain_match(erhn, domain):
                    _debug('   effective request-host %s does not domain-match %s', erhn, domain)
                    return False
            if cookie.version > 0 or self.strict_ns_domain & self.DomainStrictNoDots:
                host_prefix = req_host[:-len(domain)]
                if host_prefix.find('.') >= 0 and not IPV4_RE.search(req_host):
                    _debug('   host prefix %s for domain %s contains a dot', host_prefix, domain)
                    return False
        return True

    def set_ok_port(self, cookie, request):
        if cookie.port_specified:
            req_port = request_port(request)
            if req_port is None:
                req_port = '80'
            else:
                req_port = str(req_port)
            for p in cookie.port.split(','):
                try:
                    int(p)
                except ValueError:
                    _debug('   bad port %s (not numeric)', p)
                    return False

                if p == req_port:
                    break
            else:
                _debug('   request port (%s) not found in %s', req_port, cookie.port)
                return False

        return True

    def return_ok(self, cookie, request):
        """
        If you override .return_ok(), be sure to call this method.  If it
        returns false, so should your subclass (assuming your subclass wants to
        be more strict about which cookies to return).

        """
        _debug(' - checking cookie %s=%s', cookie.name, cookie.value)
        for n in ('version', 'verifiability', 'secure', 'expires', 'port', 'domain'):
            fn_name = 'return_ok_' + n
            fn = getattr(self, fn_name)
            if not fn(cookie, request):
                return False

        return True

    def return_ok_version(self, cookie, request):
        if cookie.version > 0 and not self.rfc2965:
            _debug('   RFC 2965 cookies are switched off')
            return False
        if cookie.version == 0 and not self.netscape:
            _debug('   Netscape cookies are switched off')
            return False
        return True

    def return_ok_verifiability(self, cookie, request):
        if request.is_unverifiable() and is_third_party(request):
            if cookie.version > 0 and self.strict_rfc2965_unverifiable:
                _debug('   third-party RFC 2965 cookie during unverifiable transaction')
                return False
            if cookie.version == 0 and self.strict_ns_unverifiable:
                _debug('   third-party Netscape cookie during unverifiable transaction')
                return False
        return True

    def return_ok_secure(self, cookie, request):
        if cookie.secure and request.get_type() != 'https':
            _debug('   secure cookie with non-secure request')
            return False
        return True

    def return_ok_expires(self, cookie, request):
        if cookie.is_expired(self._now):
            _debug('   cookie expired')
            return False
        return True

    def return_ok_port(self, cookie, request):
        if cookie.port:
            req_port = request_port(request)
            if req_port is None:
                req_port = '80'
            for p in cookie.port.split(','):
                if p == req_port:
                    break
            else:
                _debug('   request port %s does not match cookie port %s', req_port, cookie.port)
                return False

        return True

    def return_ok_domain(self, cookie, request):
        req_host, erhn = eff_request_host(request)
        domain = cookie.domain
        if cookie.version == 0 and self.strict_ns_domain & self.DomainStrictNonDomain and not cookie.domain_specified and domain != erhn:
            _debug('   cookie with unspecified domain does not string-compare equal to request domain')
            return False
        if cookie.version > 0 and not domain_match(erhn, domain):
            _debug('   effective request-host name %s does not domain-match RFC 2965 cookie domain %s', erhn, domain)
            return False
        if cookie.version == 0 and not ('.' + erhn).endswith(domain):
            _debug('   request-host %s does not match Netscape cookie domain %s', req_host, domain)
            return False
        return True

    def domain_return_ok(self, domain, request):
        req_host, erhn = eff_request_host(request)
        if not req_host.startswith('.'):
            req_host = '.' + req_host
        if not erhn.startswith('.'):
            erhn = '.' + erhn
        if not (req_host.endswith(domain) or erhn.endswith(domain)):
            return False
        if self.is_blocked(domain):
            _debug('   domain %s is in user block-list', domain)
            return False
        if self.is_not_allowed(domain):
            _debug('   domain %s is not in user allow-list', domain)
            return False
        return True

    def path_return_ok(self, path, request):
        _debug('- checking cookie path=%s', path)
        req_path = request_path(request)
        if not req_path.startswith(path):
            _debug('  %s does not path-match %s', req_path, path)
            return False
        return True


def vals_sorted_by_key(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)


def deepvalues(mapping):
    """Iterates over nested mapping, depth-first, in sorted order by key."""
    values = vals_sorted_by_key(mapping)
    for obj in values:
        mapping = False
        try:
            obj.items
        except AttributeError:
            pass
        else:
            mapping = True
            for subobj in deepvalues(obj):
                yield subobj

            if not mapping:
                yield obj


class Absent():
    pass


class CookieJar():
    """Collection of HTTP cookies.

    You may not need to know about this class: try
    urllib2.build_opener(HTTPCookieProcessor).open(url).

    """
    non_word_re = re.compile('\\W')
    quote_re = re.compile('([\\"\\\\])')
    strict_domain_re = re.compile('\\.?[^.]*')
    domain_re = re.compile('[^.]*')
    dots_re = re.compile('^\\.+')
    magic_re = '^\\#LWP-Cookies-(\\d+\\.\\d+)'

    def __init__(self, policy=None):
        if policy is None:
            policy = DefaultCookiePolicy()
        self._policy = policy
        self._cookies_lock = _threading.RLock()
        self._cookies = {}
        return

    def set_policy(self, policy):
        self._policy = policy

    def _cookies_for_domain(self, domain, request):
        cookies = []
        if not self._policy.domain_return_ok(domain, request):
            return []
        _debug('Checking %s for cookies to return', domain)
        cookies_by_path = self._cookies[domain]
        for path in cookies_by_path.keys():
            if not self._policy.path_return_ok(path, request):
                continue
            cookies_by_name = cookies_by_path[path]
            for cookie in cookies_by_name.values():
                if not self._policy.return_ok(cookie, request):
                    _debug('   not returning cookie')
                    continue
                _debug("   it's a match")
                cookies.append(cookie)

        return cookies

    def _cookies_for_request(self, request):
        """Return a list of cookies to be returned to server."""
        cookies = []
        for domain in self._cookies.keys():
            cookies.extend(self._cookies_for_domain(domain, request))

        return cookies

    def _cookie_attrs(self, cookies):
        """Return a list of cookie-attributes to be returned to server.

        like ['foo="bar"; $Path="/"', ...]

        The $Version attribute is also added when appropriate (currently only
        once per request).

        """
        cookies.sort(key=lambda arg: len(arg.path), reverse=True)
        version_set = False
        attrs = []
        for cookie in cookies:
            version = cookie.version
            if not version_set:
                version_set = True
                if version > 0:
                    attrs.append('$Version=%s' % version)
            if cookie.value is not None and self.non_word_re.search(cookie.value) and version > 0:
                value = self.quote_re.sub('\\\\\\1', cookie.value)
            else:
                value = cookie.value
            if cookie.value is None:
                attrs.append(cookie.name)
            else:
                attrs.append('%s=%s' % (cookie.name, value))
            if version > 0:
                if cookie.path_specified:
                    attrs.append('$Path="%s"' % cookie.path)
                if cookie.domain.startswith('.'):
                    domain = cookie.domain
                    if not cookie.domain_initial_dot and domain.startswith('.'):
                        domain = domain[1:]
                    attrs.append('$Domain="%s"' % domain)
                if cookie.port is not None:
                    p = '$Port'
                    if cookie.port_specified:
                        p = p + '="%s"' % cookie.port
                    attrs.append(p)

        return attrs

    def add_cookie_header(self, request):
        """Add correct Cookie: header to request (urllib2.Request object).

        The Cookie2 header is also added unless policy.hide_cookie2 is true.

        """
        _debug('add_cookie_header')
        self._cookies_lock.acquire()
        try:
            self._policy._now = self._now = int(time.time())
            cookies = self._cookies_for_request(request)
            attrs = self._cookie_attrs(cookies)
            if attrs:
                if not request.has_header('Cookie'):
                    request.add_unredirected_header('Cookie', ('; ').join(attrs))
            if self._policy.rfc2965 and not self._policy.hide_cookie2 and not request.has_header('Cookie2'):
                for cookie in cookies:
                    if cookie.version != 1:
                        request.add_unredirected_header('Cookie2', '$Version="1"')
                        break

        finally:
            self._cookies_lock.release()

        self.clear_expired_cookies()

    def _normalized_cookie_tuples(self, attrs_set):
        """Return list of tuples containing normalised cookie information.

        attrs_set is the list of lists of key,value pairs extracted from
        the Set-Cookie or Set-Cookie2 headers.

        Tuples are name, value, standard, rest, where name and value are the
        cookie name and value, standard is a dictionary containing the standard
        cookie-attributes (discard, secure, version, expires or max-age,
        domain, path and port) and rest is a dictionary containing the rest of
        the cookie-attributes.

        """
        cookie_tuples = []
        boolean_attrs = ('discard', 'secure')
        value_attrs = ('version', 'expires', 'max-age', 'domain', 'path', 'port', 'comment',
                       'commenturl')
        for cookie_attrs in attrs_set:
            name, value = cookie_attrs[0]
            max_age_set = False
            bad_cookie = False
            standard = {}
            rest = {}
            for k, v in cookie_attrs[1:]:
                lc = k.lower()
                if lc in value_attrs or lc in boolean_attrs:
                    k = lc
                if k in boolean_attrs and v is None:
                    v = True
                if k in standard:
                    continue
                if k == 'domain':
                    if v is None:
                        _debug('   missing value for domain attribute')
                        bad_cookie = True
                        break
                    v = v.lower()
                if k == 'expires':
                    if max_age_set:
                        continue
                    if v is None:
                        _debug('   missing or invalid value for expires attribute: treating as session cookie')
                        continue
                if k == 'max-age':
                    max_age_set = True
                    try:
                        v = int(v)
                    except ValueError:
                        _debug('   missing or invalid (non-numeric) value for max-age attribute')
                        bad_cookie = True
                        break

                    k = 'expires'
                    v = self._now + v
                if k in value_attrs or k in boolean_attrs:
                    if v is None and k not in ('port', 'comment', 'commenturl'):
                        _debug('   missing value for %s attribute' % k)
                        bad_cookie = True
                        break
                    standard[k] = v
                else:
                    rest[k] = v

            if bad_cookie:
                continue
            cookie_tuples.append((name, value, standard, rest))

        return cookie_tuples

    def _cookie_from_cookie_tuple(self, tup, request):
        name, value, standard, rest = tup
        domain = standard.get('domain', Absent)
        path = standard.get('path', Absent)
        port = standard.get('port', Absent)
        expires = standard.get('expires', Absent)
        version = standard.get('version', None)
        if version is not None:
            try:
                version = int(version)
            except ValueError:
                return

        secure = standard.get('secure', False)
        discard = standard.get('discard', False)
        comment = standard.get('comment', None)
        comment_url = standard.get('commenturl', None)
        if path is not Absent and path != '':
            path_specified = True
            path = escape_path(path)
        else:
            path_specified = False
            path = request_path(request)
            i = path.rfind('/')
            if i != -1:
                if version == 0:
                    path = path[:i]
                else:
                    path = path[:i + 1]
            if len(path) == 0:
                path = '/'
        domain_specified = domain is not Absent
        domain_initial_dot = False
        if domain_specified:
            domain_initial_dot = bool(domain.startswith('.'))
        if domain is Absent:
            req_host, erhn = eff_request_host(request)
            domain = erhn
        else:
            if not domain.startswith('.'):
                domain = '.' + domain
            port_specified = False
            if port is not Absent:
                if port is None:
                    port = request_port(request)
                else:
                    port_specified = True
                    port = re.sub('\\s+', '', port)
            else:
                port = None
            if expires is Absent:
                expires = None
                discard = True
            elif expires <= self._now:
                try:
                    self.clear(domain, path, name)
                except KeyError:
                    pass

                _debug("Expiring cookie, domain='%s', path='%s', name='%s'", domain, path, name)
                return
        return Cookie(version, name, value, port, port_specified, domain, domain_specified, domain_initial_dot, path, path_specified, secure, expires, discard, comment, comment_url, rest)

    def _cookies_from_attrs_set(self, attrs_set, request):
        cookie_tuples = self._normalized_cookie_tuples(attrs_set)
        cookies = []
        for tup in cookie_tuples:
            cookie = self._cookie_from_cookie_tuple(tup, request)
            if cookie:
                cookies.append(cookie)

        return cookies

    def _process_rfc2109_cookies(self, cookies):
        rfc2109_as_ns = getattr(self._policy, 'rfc2109_as_netscape', None)
        if rfc2109_as_ns is None:
            rfc2109_as_ns = not self._policy.rfc2965
        for cookie in cookies:
            if cookie.version == 1:
                cookie.rfc2109 = True
                if rfc2109_as_ns:
                    cookie.version = 0

        return

    def make_cookies(self, response, request):
        """Return sequence of Cookie objects extracted from response object."""
        headers = response.info()
        rfc2965_hdrs = headers.getheaders('Set-Cookie2')
        ns_hdrs = headers.getheaders('Set-Cookie')
        rfc2965 = self._policy.rfc2965
        netscape = self._policy.netscape
        if not rfc2965_hdrs and not ns_hdrs or not ns_hdrs and not rfc2965 or not rfc2965_hdrs and not netscape or not netscape and not rfc2965:
            return []
        try:
            cookies = self._cookies_from_attrs_set(split_header_words(rfc2965_hdrs), request)
        except Exception:
            _warn_unhandled_exception()
            cookies = []

        if ns_hdrs and netscape:
            try:
                ns_cookies = self._cookies_from_attrs_set(parse_ns_headers(ns_hdrs), request)
            except Exception:
                _warn_unhandled_exception()
                ns_cookies = []

            self._process_rfc2109_cookies(ns_cookies)
            if rfc2965:
                lookup = {}
                for cookie in cookies:
                    lookup[(cookie.domain, cookie.path, cookie.name)] = None

                def no_matching_rfc2965(ns_cookie, lookup=lookup):
                    key = (ns_cookie.domain, ns_cookie.path, ns_cookie.name)
                    return key not in lookup

                ns_cookies = filter(no_matching_rfc2965, ns_cookies)
            if ns_cookies:
                cookies.extend(ns_cookies)
        return cookies

    def set_cookie_if_ok(self, cookie, request):
        """Set a cookie if policy says it's OK to do so."""
        self._cookies_lock.acquire()
        try:
            self._policy._now = self._now = int(time.time())
            if self._policy.set_ok(cookie, request):
                self.set_cookie(cookie)
        finally:
            self._cookies_lock.release()

    def set_cookie(self, cookie):
        """Set a cookie, without checking whether or not it should be set."""
        c = self._cookies
        self._cookies_lock.acquire()
        try:
            if cookie.domain not in c:
                c[cookie.domain] = {}
            c2 = c[cookie.domain]
            if cookie.path not in c2:
                c2[cookie.path] = {}
            c3 = c2[cookie.path]
            c3[cookie.name] = cookie
        finally:
            self._cookies_lock.release()

    def extract_cookies(self, response, request):
        """Extract cookies from response, where allowable given the request."""
        _debug('extract_cookies: %s', response.info())
        self._cookies_lock.acquire()
        try:
            self._policy._now = self._now = int(time.time())
            for cookie in self.make_cookies(response, request):
                if self._policy.set_ok(cookie, request):
                    _debug(' setting cookie: %s', cookie)
                    self.set_cookie(cookie)

        finally:
            self._cookies_lock.release()

    def clear(self, domain=None, path=None, name=None):
        """Clear some cookies.

        Invoking this method without arguments will clear all cookies.  If
        given a single argument, only cookies belonging to that domain will be
        removed.  If given two arguments, cookies belonging to the specified
        path within that domain are removed.  If given three arguments, then
        the cookie with the specified name, path and domain is removed.

        Raises KeyError if no matching cookie exists.

        """
        if name is not None:
            if domain is None or path is None:
                raise ValueError('domain and path must be given to remove a cookie by name')
            del self._cookies[domain][path][name]
        elif path is not None:
            if domain is None:
                raise ValueError('domain must be given to remove cookies by path')
            del self._cookies[domain][path]
        elif domain is not None:
            del self._cookies[domain]
        else:
            self._cookies = {}
        return

    def clear_session_cookies(self):
        """Discard all session cookies.

        Note that the .save() method won't save session cookies anyway, unless
        you ask otherwise by passing a true ignore_discard argument.

        """
        self._cookies_lock.acquire()
        try:
            for cookie in self:
                if cookie.discard:
                    self.clear(cookie.domain, cookie.path, cookie.name)

        finally:
            self._cookies_lock.release()

    def clear_expired_cookies(self):
        """Discard all expired cookies.

        You probably don't need to call this method: expired cookies are never
        sent back to the server (provided you're using DefaultCookiePolicy),
        this method is called by CookieJar itself every so often, and the
        .save() method won't save expired cookies anyway (unless you ask
        otherwise by passing a true ignore_expires argument).

        """
        self._cookies_lock.acquire()
        try:
            now = time.time()
            for cookie in self:
                if cookie.is_expired(now):
                    self.clear(cookie.domain, cookie.path, cookie.name)

        finally:
            self._cookies_lock.release()

    def __iter__(self):
        return deepvalues(self._cookies)

    def __len__(self):
        """Return number of contained cookies."""
        i = 0
        for cookie in self:
            i = i + 1

        return i

    def __repr__(self):
        r = []
        for cookie in self:
            r.append(repr(cookie))

        return '<%s[%s]>' % (self.__class__, (', ').join(r))

    def __str__(self):
        r = []
        for cookie in self:
            r.append(str(cookie))

        return '<%s[%s]>' % (self.__class__, (', ').join(r))


class LoadError(IOError):
    pass


class FileCookieJar(CookieJar):
    """CookieJar that can be loaded from and saved to a file."""

    def __init__(self, filename=None, delayload=False, policy=None):
        """
        Cookies are NOT loaded from the named file until either the .load() or
        .revert() method is called.

        """
        CookieJar.__init__(self, policy)
        if filename is not None:
            try:
                filename + ''
            except:
                raise ValueError('filename must be string-like')

        self.filename = filename
        self.delayload = bool(delayload)
        return

    def save(self, filename=None, ignore_discard=False, ignore_expires=False):
        """Save cookies to a file."""
        raise NotImplementedError()

    def load(self, filename=None, ignore_discard=False, ignore_expires=False):
        """Load cookies from a file."""
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        f = open(filename)
        try:
            self._really_load(f, filename, ignore_discard, ignore_expires)
        finally:
            f.close()

        return

    def revert(self, filename=None, ignore_discard=False, ignore_expires=False):
        """Clear all cookies and reload cookies from a saved file.

        Raises LoadError (or IOError) if reversion is not successful; the
        object's state will not be altered if this happens.

        """
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        self._cookies_lock.acquire()
        try:
            old_state = copy.deepcopy(self._cookies)
            self._cookies = {}
            try:
                self.load(filename, ignore_discard, ignore_expires)
            except (LoadError, IOError):
                self._cookies = old_state
                raise

        finally:
            self._cookies_lock.release()

        return


from _LWPCookieJar import LWPCookieJar, lwp_cookie_str
from _MozillaCookieJar import MozillaCookieJar