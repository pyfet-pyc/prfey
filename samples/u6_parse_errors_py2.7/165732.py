# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\future\backports\http\cookiejar.py
r"""HTTP cookie handling for web clients.

This is a backport of the Py3.3 ``http.cookiejar`` module for
python-future.

This module has (now fairly distant) origins in Gisle Aas' Perl module
HTTP::Cookies, from the libwww-perl library.

Docstrings, comments and debug strings in this code refer to the
attributes of the HTTP cookie system as cookie-attributes, to distinguish
them clearly from Python attributes.

Class diagram (note that BSDDBCookieJar and the MSIE* classes are not
distributed with the Python standard library, but are available from
http://wwwsearch.sf.net/):

                        CookieJar____
                        /     \      \
            FileCookieJar      \      \
             /    |   \         \      \
 MozillaCookieJar | LWPCookieJar \      \
                  |               |      \
                  |   ---MSIEBase |       \
                  |  /      |     |        \
                  | /   MSIEDBCookieJar BSDDBCookieJar
                  |/
               MSIECookieJar

"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future.builtins import filter, int, map, open, str
from future.utils import as_native_str
__all__ = [
 b'Cookie', b'CookieJar', b'CookiePolicy', b'DefaultCookiePolicy',
 b'FileCookieJar', b'LWPCookieJar', b'LoadError', b'MozillaCookieJar']
import copy, datetime, re
re.ASCII = 0
import time
from future.backports.urllib.parse import urlparse, urlsplit, quote
from future.backports.http.client import HTTP_PORT
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

from calendar import timegm
debug = False
logger = None

def _debug(*args):
    global logger
    if not debug:
        return
    if not logger:
        import logging
        logger = logging.getLogger(b'http.cookiejar')
    return logger.debug(*args)


DEFAULT_HTTP_PORT = str(HTTP_PORT)
MISSING_FILENAME_TEXT = b'a filename was not supplied (nor was the CookieJar instance initialised with one)'

def _warn_unhandled_exception():
    import io, warnings, traceback
    f = io.StringIO()
    traceback.print_exc(None, f)
    msg = f.getvalue()
    warnings.warn(b'http.cookiejar bug!\n%s' % msg, stacklevel=2)
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
 b'Mon', b'Tue', b'Wed', b'Thu', b'Fri', b'Sat', b'Sun']
MONTHS = [b'Jan', b'Feb', b'Mar', b'Apr', b'May', b'Jun',
 b'Jul', b'Aug', b'Sep', b'Oct', b'Nov', b'Dec']
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
        dt = datetime.datetime.utcnow()
    else:
        dt = datetime.datetime.utcfromtimestamp(t)
    return b'%04d-%02d-%02d %02d:%02d:%02dZ' % (
     dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def time2netscape(t=None):
    """Return a string representing time in seconds since epoch, t.

    If the function is called without an argument, it will use the current
    time.

    The format of the returned string is like this:

    Wed, DD-Mon-YYYY HH:MM:SS GMT

    """
    if t is None:
        dt = datetime.datetime.utcnow()
    else:
        dt = datetime.datetime.utcfromtimestamp(t)
    return b'%s %02d-%s-%04d %02d:%02d:%02d GMT' % (
     DAYS[dt.weekday()], dt.day, MONTHS[(dt.month - 1)],
     dt.year, dt.hour, dt.minute, dt.second)


UTC_ZONES = {b'GMT': None, b'UTC': None, b'UT': None, b'Z': None}
TIMEZONE_RE = re.compile(b'^([-+])?(\\d\\d?):?(\\d\\d)?$', re.ASCII)

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
            if m.group(1) == b'-':
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
            tz = b'UTC'
        tz = tz.upper()
        offset = offset_from_tz_string(tz)
        if offset is None:
            return
        t = t - offset
    return t


STRICT_DATE_RE = re.compile(b'^[SMTWF][a-z][a-z], (\\d\\d) ([JFMASOND][a-z][a-z]) (\\d\\d\\d\\d) (\\d\\d):(\\d\\d):(\\d\\d) GMT$', re.ASCII)
WEEKDAY_RE = re.compile(b'^(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*,?\\s*', re.I | re.ASCII)
LOOSE_HTTP_DATE_RE = re.compile(b'^\n    (\\d\\d?)            # day\n       (?:\\s+|[-\\/])\n    (\\w+)              # month\n        (?:\\s+|[-\\/])\n    (\\d+)              # year\n    (?:\n          (?:\\s+|:)    # separator before clock\n       (\\d\\d?):(\\d\\d)  # hour:min\n       (?::(\\d\\d))?    # optional seconds\n    )?                 # optional clock\n       \\s*\n    ([-+]?\\d{2,4}|(?![APap][Mm]\\b)[A-Za-z]+)? # timezone\n       \\s*\n    (?:\\(\\w+\\))?       # ASCII representation of timezone in parens.\n       \\s*$', re.X | re.ASCII)

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
        text = WEEKDAY_RE.sub(b'', text, 1)
        day, mon, yr, hr, min, sec, tz = [
         None] * 7
        m = LOOSE_HTTP_DATE_RE.search(text)
        if m is not None:
            day, mon, yr, hr, min, sec, tz = m.groups()
        else:
            return
        return _str2time(day, mon, yr, hr, min, sec, tz)


ISO_DATE_RE = re.compile(b'^\n    (\\d{4})              # year\n       [-\\/]?\n    (\\d\\d?)              # numerical month\n       [-\\/]?\n    (\\d\\d?)              # day\n   (?:\n         (?:\\s+|[-:Tt])  # separator before clock\n      (\\d\\d?):?(\\d\\d)    # hour:min\n      (?::?(\\d\\d(?:\\.\\d*)?))?  # optional seconds (and fractional)\n   )?                    # optional clock\n      \\s*\n   ([-+]?\\d\\d?:?(:?\\d\\d)?\n    |Z|z)?               # timezone  (Z is "zero meridian", i.e. GMT)\n      \\s*$', re.X | re.ASCII)

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


HEADER_TOKEN_RE = re.compile(b'^\\s*([^=\\s;,]+)')
HEADER_QUOTED_VALUE_RE = re.compile(b'^\\s*=\\s*\\"([^\\"\\\\]*(?:\\\\.[^\\"\\\\]*)*)\\"')
HEADER_VALUE_RE = re.compile(b'^\\s*=\\s*([^\\s;,]*)')
HEADER_ESCAPE_RE = re.compile(b'\\\\(.)')

def split_header_words--- This code section failed: ---

 L. 390         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'header_values'
                6  LOAD_GLOBAL           1  'str'
                9  CALL_FUNCTION_2       2  None
               12  UNARY_NOT        
               13  POP_JUMP_IF_TRUE     22  'to 22'
               16  LOAD_ASSERT              AssertionError
               19  RAISE_VARARGS_1       1  None

 L. 391        22  BUILD_LIST_0          0 
               25  STORE_FAST            1  'result'

 L. 392        28  SETUP_LOOP          404  'to 435'
               31  LOAD_FAST             0  'header_values'
               34  GET_ITER         
               35  FOR_ITER            396  'to 434'
               38  STORE_FAST            2  'text'

 L. 393        41  LOAD_FAST             2  'text'
               44  STORE_FAST            3  'orig_text'

 L. 394        47  BUILD_LIST_0          0 
               50  STORE_FAST            4  'pairs'

 L. 395        53  SETUP_LOOP          353  'to 409'
               56  LOAD_FAST             2  'text'
               59  POP_JUMP_IF_FALSE   408  'to 408'

 L. 396        62  LOAD_GLOBAL           3  'HEADER_TOKEN_RE'
               65  LOAD_ATTR             4  'search'
               68  LOAD_FAST             2  'text'
               71  CALL_FUNCTION_1       1  None
               74  STORE_FAST            5  'm'

 L. 397        77  LOAD_FAST             5  'm'
               80  POP_JUMP_IF_FALSE   270  'to 270'

 L. 398        83  LOAD_GLOBAL           5  'unmatched'
               86  LOAD_FAST             5  'm'
               89  CALL_FUNCTION_1       1  None
               92  STORE_FAST            2  'text'

 L. 399        95  LOAD_FAST             5  'm'
               98  LOAD_ATTR             6  'group'
              101  LOAD_CONST               1
              104  CALL_FUNCTION_1       1  None
              107  STORE_FAST            6  'name'

 L. 400       110  LOAD_GLOBAL           7  'HEADER_QUOTED_VALUE_RE'
              113  LOAD_ATTR             4  'search'
              116  LOAD_FAST             2  'text'
              119  CALL_FUNCTION_1       1  None
              122  STORE_FAST            5  'm'

 L. 401       125  LOAD_FAST             5  'm'
              128  POP_JUMP_IF_FALSE   179  'to 179'

 L. 402       131  LOAD_GLOBAL           5  'unmatched'
              134  LOAD_FAST             5  'm'
              137  CALL_FUNCTION_1       1  None
              140  STORE_FAST            2  'text'

 L. 403       143  LOAD_FAST             5  'm'
              146  LOAD_ATTR             6  'group'
              149  LOAD_CONST               1
              152  CALL_FUNCTION_1       1  None
              155  STORE_FAST            7  'value'

 L. 404       158  LOAD_GLOBAL           8  'HEADER_ESCAPE_RE'
              161  LOAD_ATTR             9  'sub'
              164  LOAD_CONST               '\\1'
              167  LOAD_FAST             7  'value'
              170  CALL_FUNCTION_2       2  None
              173  STORE_FAST            7  'value'
              176  JUMP_FORWARD         69  'to 248'

 L. 406       179  LOAD_GLOBAL          10  'HEADER_VALUE_RE'
              182  LOAD_ATTR             4  'search'
              185  LOAD_FAST             2  'text'
              188  CALL_FUNCTION_1       1  None
              191  STORE_FAST            5  'm'

 L. 407       194  LOAD_FAST             5  'm'
              197  POP_JUMP_IF_FALSE   242  'to 242'

 L. 408       200  LOAD_GLOBAL           5  'unmatched'
              203  LOAD_FAST             5  'm'
              206  CALL_FUNCTION_1       1  None
              209  STORE_FAST            2  'text'

 L. 409       212  LOAD_FAST             5  'm'
              215  LOAD_ATTR             6  'group'
              218  LOAD_CONST               1
              221  CALL_FUNCTION_1       1  None
              224  STORE_FAST            7  'value'

 L. 410       227  LOAD_FAST             7  'value'
              230  LOAD_ATTR            11  'rstrip'
              233  CALL_FUNCTION_0       0  None
              236  STORE_FAST            7  'value'
              239  JUMP_FORWARD          6  'to 248'

 L. 413       242  LOAD_CONST               None
              245  STORE_FAST            7  'value'
            248_0  COME_FROM           239  '239'
            248_1  COME_FROM           176  '176'

 L. 414       248  LOAD_FAST             4  'pairs'
              251  LOAD_ATTR            13  'append'
              254  LOAD_FAST             6  'name'
              257  LOAD_FAST             7  'value'
              260  BUILD_TUPLE_2         2 
              263  CALL_FUNCTION_1       1  None
              266  POP_TOP          
              267  JUMP_BACK            56  'to 56'

 L. 415       270  LOAD_FAST             2  'text'
              273  LOAD_ATTR            14  'lstrip'
              276  CALL_FUNCTION_0       0  None
              279  LOAD_ATTR            15  'startswith'
              282  LOAD_CONST               ','
              285  CALL_FUNCTION_1       1  None
              288  POP_JUMP_IF_FALSE   338  'to 338'

 L. 417       291  LOAD_FAST             2  'text'
              294  LOAD_ATTR            14  'lstrip'
              297  CALL_FUNCTION_0       0  None
              300  LOAD_CONST               1
              303  SLICE+1          
              304  STORE_FAST            2  'text'

 L. 418       307  LOAD_FAST             4  'pairs'
              310  POP_JUMP_IF_FALSE   329  'to 329'
              313  LOAD_FAST             1  'result'
              316  LOAD_ATTR            13  'append'
              319  LOAD_FAST             4  'pairs'
              322  CALL_FUNCTION_1       1  None
              325  POP_TOP          
              326  JUMP_FORWARD          0  'to 329'
            329_0  COME_FROM           326  '326'

 L. 419       329  BUILD_LIST_0          0 
              332  STORE_FAST            4  'pairs'
              335  JUMP_BACK            56  'to 56'

 L. 422       338  LOAD_GLOBAL          16  're'
              341  LOAD_ATTR            17  'subn'
              344  LOAD_CONST               '^[=\\s;]*'
              347  LOAD_CONST               ''
              350  LOAD_FAST             2  'text'
              353  CALL_FUNCTION_3       3  None
              356  UNPACK_SEQUENCE_2     2 
              359  STORE_FAST            8  'non_junk'
              362  STORE_FAST            9  'nr_junk_chars'

 L. 423       365  LOAD_FAST             9  'nr_junk_chars'
              368  LOAD_CONST               0
              371  COMPARE_OP            4  >
              374  POP_JUMP_IF_TRUE    399  'to 399'
              377  LOAD_ASSERT              AssertionError

 L. 424       380  LOAD_CONST               "split_header_words bug: '%s', '%s', %s"

 L. 425       383  LOAD_FAST             3  'orig_text'
              386  LOAD_FAST             2  'text'
              389  LOAD_FAST             4  'pairs'
              392  BUILD_TUPLE_3         3 
              395  BINARY_MODULO    
              396  RAISE_VARARGS_2       2  None

 L. 426       399  LOAD_FAST             8  'non_junk'
              402  STORE_FAST            2  'text'
              405  JUMP_BACK            56  'to 56'
              408  POP_BLOCK        
            409_0  COME_FROM            53  '53'

 L. 427       409  LOAD_FAST             4  'pairs'
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

 L. 428       435  LOAD_FAST             1  'result'
              438  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 408


HEADER_JOIN_ESCAPE_RE = re.compile(b'([\\"\\\\])')

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
                if not re.search(b'^\\w+$', v):
                    v = HEADER_JOIN_ESCAPE_RE.sub(b'\\\\\\1', v)
                    v = b'"%s"' % v
                k = b'%s=%s' % (k, v)
            attr.append(k)

        if attr:
            headers.append((b'; ').join(attr))

    return (b', ').join(headers)


def strip_quotes(text):
    if text.startswith(b'"'):
        text = text[1:]
    if text.endswith(b'"'):
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
        for ii, param in enumerate(re.split(b';\\s*', ns_header)):
            param = param.rstrip()
            if param == b'':
                continue
            if b'=' not in param:
                k, v = param, None
            else:
                k, v = re.split(b'\\s*=\\s*', param, 1)
                k = k.lstrip()
            if ii != 0:
                lc = k.lower()
                if lc in known_attrs:
                    k = lc
                if k == b'version':
                    v = strip_quotes(v)
                    version_set = True
                if k == b'expires':
                    v = http2time(strip_quotes(v))
            pairs.append((k, v))

        if pairs:
            if not version_set:
                pairs.append(('version', '0'))
            result.append(pairs)

    return result


IPV4_RE = re.compile(b'\\.\\d+$', re.ASCII)

def is_HDN(text):
    """Return True if text is a host domain name."""
    if IPV4_RE.search(text):
        return False
    if text == b'':
        return False
    if text[0] == b'.' or text[(-1)] == b'.':
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
    if not B.startswith(b'.'):
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
    initial_dot = B.startswith(b'.')
    if initial_dot and A.endswith(B):
        return True
    if not initial_dot and A == B:
        return True
    return False


cut_port_re = re.compile(b':\\d+$', re.ASCII)

def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    url = request.get_full_url()
    host = urlparse(url)[1]
    if host == b'':
        host = request.get_header(b'Host', b'')
    host = cut_port_re.sub(b'', host, 1)
    return host.lower()


def eff_request_host(request):
    """Return a tuple (request-host, effective request-host name).

    As defined by RFC 2965, except both are lowercased.

    """
    erhn = req_host = request_host(request)
    if req_host.find(b'.') == -1 and not IPV4_RE.search(req_host):
        erhn = req_host + b'.local'
    return (
     req_host, erhn)


def request_path(request):
    """Path component of request-URI, as defined by RFC 2965."""
    url = request.get_full_url()
    parts = urlsplit(url)
    path = escape_path(parts.path)
    if not path.startswith(b'/'):
        path = b'/' + path
    return path


def request_port(request):
    host = request.host
    i = host.find(b':')
    if i >= 0:
        port = host[i + 1:]
        try:
            int(port)
        except ValueError:
            _debug(b"nonnumeric port: '%s'", port)
            return

    else:
        port = DEFAULT_HTTP_PORT
    return port


HTTP_PATH_SAFE = b"%/;:@&=+$,!~*'()"
ESCAPED_CHAR_RE = re.compile(b'%([0-9a-fA-F][0-9a-fA-F])')

def uppercase_escaped_char(match):
    return b'%%%s' % match.group(1).upper()


def escape_path(path):
    """Escape any invalid characters in HTTP URL, and uppercase all escapes."""
    path = quote(path, HTTP_PATH_SAFE)
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
    i = h.find(b'.')
    if i >= 0:
        b = h[i + 1:]
        i = b.find(b'.')
        if is_HDN(h) and (i >= 0 or b == b'local'):
            return b'.' + b
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


class Cookie(object):
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
            raise ValueError(b'if port is None, port_specified must be false')
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
            p = b''
        else:
            p = b':' + self.port
        limit = self.domain + p + self.path
        if self.value is not None:
            namevalue = b'%s=%s' % (self.name, self.value)
        else:
            namevalue = self.name
        return b'<Cookie %s for %s>' % (namevalue, limit)

    @as_native_str()
    def __repr__(self):
        args = []
        for name in ('version', 'name', 'value', 'port', 'port_specified', 'domain',
                     'domain_specified', 'domain_initial_dot', 'path', 'path_specified',
                     'secure', 'expires', 'discard', 'comment', 'comment_url'):
            attr = getattr(self, name)
            if isinstance(attr, str):
                attr = str(attr)
            args.append(str(b'%s=%s') % (name, repr(attr)))

        args.append(b'rest=%s' % repr(self._rest))
        args.append(b'rfc2109=%s' % repr(self.rfc2109))
        return b'Cookie(%s)' % (b', ').join(args)


class CookiePolicy(object):
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
        _debug(b' - checking cookie %s=%s', cookie.name, cookie.value)
        assert cookie.name is not None
        for n in ('version', 'verifiability', 'name', 'path', 'domain', 'port'):
            fn_name = b'set_ok_' + n
            fn = getattr(self, fn_name)
            if not fn(cookie, request):
                return False

        return True

    def set_ok_version(self, cookie, request):
        if cookie.version is None:
            _debug(b'   Set-Cookie2 without version attribute (%s=%s)', cookie.name, cookie.value)
            return False
        else:
            if cookie.version > 0 and not self.rfc2965:
                _debug(b'   RFC 2965 cookies are switched off')
                return False
            if cookie.version == 0 and not self.netscape:
                _debug(b'   Netscape cookies are switched off')
                return False
            return True

    def set_ok_verifiability(self, cookie, request):
        if request.unverifiable and is_third_party(request):
            if cookie.version > 0 and self.strict_rfc2965_unverifiable:
                _debug(b'   third-party RFC 2965 cookie during unverifiable transaction')
                return False
            if cookie.version == 0 and self.strict_ns_unverifiable:
                _debug(b'   third-party Netscape cookie during unverifiable transaction')
                return False
        return True

    def set_ok_name(self, cookie, request):
        if cookie.version == 0 and self.strict_ns_set_initial_dollar and cookie.name.startswith(b'$'):
            _debug(b"   illegal name (starts with '$'): '%s'", cookie.name)
            return False
        return True

    def set_ok_path(self, cookie, request):
        if cookie.path_specified:
            req_path = request_path(request)
            if (cookie.version > 0 or cookie.version == 0 and self.strict_ns_set_path) and not req_path.startswith(cookie.path):
                _debug(b'   path attribute %s is not a prefix of request path %s', cookie.path, req_path)
                return False
        return True

    def set_ok_domain(self, cookie, request):
        if self.is_blocked(cookie.domain):
            _debug(b'   domain %s is in user block-list', cookie.domain)
            return False
        if self.is_not_allowed(cookie.domain):
            _debug(b'   domain %s is not in user allow-list', cookie.domain)
            return False
        if cookie.domain_specified:
            req_host, erhn = eff_request_host(request)
            domain = cookie.domain
            if self.strict_domain and domain.count(b'.') >= 2:
                i = domain.rfind(b'.')
                j = domain.rfind(b'.', 0, i)
                if j == 0:
                    tld = domain[i + 1:]
                    sld = domain[j + 1:i]
                    if sld.lower() in ('co', 'ac', 'com', 'edu', 'org', 'net', 'gov',
                                       'mil', 'int', 'aero', 'biz', 'cat', 'coop',
                                       'info', 'jobs', 'mobi', 'museum', 'name',
                                       'pro', 'travel', 'eu') and len(tld) == 2:
                        _debug(b'   country-code second level domain %s', domain)
                        return False
            if domain.startswith(b'.'):
                undotted_domain = domain[1:]
            else:
                undotted_domain = domain
            embedded_dots = undotted_domain.find(b'.') >= 0
            if not embedded_dots and domain != b'.local':
                _debug(b'   non-local domain %s contains no embedded dot', domain)
                return False
            if cookie.version == 0 and not erhn.endswith(domain) and not erhn.startswith(b'.'):
                if not (b'.' + erhn).endswith(domain):
                    _debug(b'   effective request-host %s (even with added initial dot) does not end with %s', erhn, domain)
                    return False
            if cookie.version > 0 or self.strict_ns_domain & self.DomainRFC2965Match:
                if not domain_match(erhn, domain):
                    _debug(b'   effective request-host %s does not domain-match %s', erhn, domain)
                    return False
            if cookie.version > 0 or self.strict_ns_domain & self.DomainStrictNoDots:
                host_prefix = req_host[:-len(domain)]
                if host_prefix.find(b'.') >= 0 and not IPV4_RE.search(req_host):
                    _debug(b'   host prefix %s for domain %s contains a dot', host_prefix, domain)
                    return False
        return True

    def set_ok_port(self, cookie, request):
        if cookie.port_specified:
            req_port = request_port(request)
            if req_port is None:
                req_port = b'80'
            else:
                req_port = str(req_port)
            for p in cookie.port.split(b','):
                try:
                    int(p)
                except ValueError:
                    _debug(b'   bad port %s (not numeric)', p)
                    return False

                if p == req_port:
                    break
            else:
                _debug(b'   request port (%s) not found in %s', req_port, cookie.port)
                return False

        return True

    def return_ok(self, cookie, request):
        """
        If you override .return_ok(), be sure to call this method.  If it
        returns false, so should your subclass (assuming your subclass wants to
        be more strict about which cookies to return).

        """
        _debug(b' - checking cookie %s=%s', cookie.name, cookie.value)
        for n in ('version', 'verifiability', 'secure', 'expires', 'port', 'domain'):
            fn_name = b'return_ok_' + n
            fn = getattr(self, fn_name)
            if not fn(cookie, request):
                return False

        return True

    def return_ok_version(self, cookie, request):
        if cookie.version > 0 and not self.rfc2965:
            _debug(b'   RFC 2965 cookies are switched off')
            return False
        if cookie.version == 0 and not self.netscape:
            _debug(b'   Netscape cookies are switched off')
            return False
        return True

    def return_ok_verifiability(self, cookie, request):
        if request.unverifiable and is_third_party(request):
            if cookie.version > 0 and self.strict_rfc2965_unverifiable:
                _debug(b'   third-party RFC 2965 cookie during unverifiable transaction')
                return False
            if cookie.version == 0 and self.strict_ns_unverifiable:
                _debug(b'   third-party Netscape cookie during unverifiable transaction')
                return False
        return True

    def return_ok_secure(self, cookie, request):
        if cookie.secure and request.type != b'https':
            _debug(b'   secure cookie with non-secure request')
            return False
        return True

    def return_ok_expires(self, cookie, request):
        if cookie.is_expired(self._now):
            _debug(b'   cookie expired')
            return False
        return True

    def return_ok_port(self, cookie, request):
        if cookie.port:
            req_port = request_port(request)
            if req_port is None:
                req_port = b'80'
            for p in cookie.port.split(b','):
                if p == req_port:
                    break
            else:
                _debug(b'   request port %s does not match cookie port %s', req_port, cookie.port)
                return False

        return True

    def return_ok_domain(self, cookie, request):
        req_host, erhn = eff_request_host(request)
        domain = cookie.domain
        if cookie.version == 0 and self.strict_ns_domain & self.DomainStrictNonDomain and not cookie.domain_specified and domain != erhn:
            _debug(b'   cookie with unspecified domain does not string-compare equal to request domain')
            return False
        if cookie.version > 0 and not domain_match(erhn, domain):
            _debug(b'   effective request-host name %s does not domain-match RFC 2965 cookie domain %s', erhn, domain)
            return False
        if cookie.version == 0 and not (b'.' + erhn).endswith(domain):
            _debug(b'   request-host %s does not match Netscape cookie domain %s', req_host, domain)
            return False
        return True

    def domain_return_ok(self, domain, request):
        req_host, erhn = eff_request_host(request)
        if not req_host.startswith(b'.'):
            req_host = b'.' + req_host
        if not erhn.startswith(b'.'):
            erhn = b'.' + erhn
        if not (req_host.endswith(domain) or erhn.endswith(domain)):
            return False
        if self.is_blocked(domain):
            _debug(b'   domain %s is in user block-list', domain)
            return False
        if self.is_not_allowed(domain):
            _debug(b'   domain %s is not in user allow-list', domain)
            return False
        return True

    def path_return_ok(self, path, request):
        _debug(b'- checking cookie path=%s', path)
        req_path = request_path(request)
        if not req_path.startswith(path):
            _debug(b'  %s does not path-match %s', req_path, path)
            return False
        return True


def vals_sorted_by_key(adict):
    keys = sorted(adict.keys())
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


class Absent(object):
    pass


class CookieJar(object):
    """Collection of HTTP cookies.

    You may not need to know about this class: try
    urllib.request.build_opener(HTTPCookieProcessor).open(url).
    """
    non_word_re = re.compile(b'\\W')
    quote_re = re.compile(b'([\\"\\\\])')
    strict_domain_re = re.compile(b'\\.?[^.]*')
    domain_re = re.compile(b'[^.]*')
    dots_re = re.compile(b'^\\.+')
    magic_re = re.compile(b'^\\#LWP-Cookies-(\\d+\\.\\d+)', re.ASCII)

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
        _debug(b'Checking %s for cookies to return', domain)
        cookies_by_path = self._cookies[domain]
        for path in cookies_by_path.keys():
            if not self._policy.path_return_ok(path, request):
                continue
            cookies_by_name = cookies_by_path[path]
            for cookie in cookies_by_name.values():
                if not self._policy.return_ok(cookie, request):
                    _debug(b'   not returning cookie')
                    continue
                _debug(b"   it's a match")
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
        cookies.sort(key=lambda a: len(a.path), reverse=True)
        version_set = False
        attrs = []
        for cookie in cookies:
            version = cookie.version
            if not version_set:
                version_set = True
                if version > 0:
                    attrs.append(b'$Version=%s' % version)
            if cookie.value is not None and self.non_word_re.search(cookie.value) and version > 0:
                value = self.quote_re.sub(b'\\\\\\1', cookie.value)
            else:
                value = cookie.value
            if cookie.value is None:
                attrs.append(cookie.name)
            else:
                attrs.append(b'%s=%s' % (cookie.name, value))
            if version > 0:
                if cookie.path_specified:
                    attrs.append(b'$Path="%s"' % cookie.path)
                if cookie.domain.startswith(b'.'):
                    domain = cookie.domain
                    if not cookie.domain_initial_dot and domain.startswith(b'.'):
                        domain = domain[1:]
                    attrs.append(b'$Domain="%s"' % domain)
                if cookie.port is not None:
                    p = b'$Port'
                    if cookie.port_specified:
                        p = p + b'="%s"' % cookie.port
                    attrs.append(p)

        return attrs

    def add_cookie_header(self, request):
        """Add correct Cookie: header to request (urllib.request.Request object).

        The Cookie2 header is also added unless policy.hide_cookie2 is true.

        """
        _debug(b'add_cookie_header')
        self._cookies_lock.acquire()
        try:
            self._policy._now = self._now = int(time.time())
            cookies = self._cookies_for_request(request)
            attrs = self._cookie_attrs(cookies)
            if attrs:
                if not request.has_header(b'Cookie'):
                    request.add_unredirected_header(b'Cookie', (b'; ').join(attrs))
            if self._policy.rfc2965 and not self._policy.hide_cookie2 and not request.has_header(b'Cookie2'):
                for cookie in cookies:
                    if cookie.version != 1:
                        request.add_unredirected_header(b'Cookie2', b'$Version="1"')
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
                if k == b'domain':
                    if v is None:
                        _debug(b'   missing value for domain attribute')
                        bad_cookie = True
                        break
                    v = v.lower()
                if k == b'expires':
                    if max_age_set:
                        continue
                    if v is None:
                        _debug(b'   missing or invalid value for expires attribute: treating as session cookie')
                        continue
                if k == b'max-age':
                    max_age_set = True
                    try:
                        v = int(v)
                    except ValueError:
                        _debug(b'   missing or invalid (non-numeric) value for max-age attribute')
                        bad_cookie = True
                        break

                    k = b'expires'
                    v = self._now + v
                if k in value_attrs or k in boolean_attrs:
                    if v is None and k not in ('port', 'comment', 'commenturl'):
                        _debug(b'   missing value for %s attribute' % k)
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
        domain = standard.get(b'domain', Absent)
        path = standard.get(b'path', Absent)
        port = standard.get(b'port', Absent)
        expires = standard.get(b'expires', Absent)
        version = standard.get(b'version', None)
        if version is not None:
            try:
                version = int(version)
            except ValueError:
                return

        secure = standard.get(b'secure', False)
        discard = standard.get(b'discard', False)
        comment = standard.get(b'comment', None)
        comment_url = standard.get(b'commenturl', None)
        if path is not Absent and path != b'':
            path_specified = True
            path = escape_path(path)
        else:
            path_specified = False
            path = request_path(request)
            i = path.rfind(b'/')
            if i != -1:
                if version == 0:
                    path = path[:i]
                else:
                    path = path[:i + 1]
            if len(path) == 0:
                path = b'/'
        domain_specified = domain is not Absent
        domain_initial_dot = False
        if domain_specified:
            domain_initial_dot = bool(domain.startswith(b'.'))
        if domain is Absent:
            req_host, erhn = eff_request_host(request)
            domain = erhn
        else:
            if not domain.startswith(b'.'):
                domain = b'.' + domain
            port_specified = False
            if port is not Absent:
                if port is None:
                    port = request_port(request)
                else:
                    port_specified = True
                    port = re.sub(b'\\s+', b'', port)
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

                _debug(b"Expiring cookie, domain='%s', path='%s', name='%s'", domain, path, name)
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
        rfc2109_as_ns = getattr(self._policy, b'rfc2109_as_netscape', None)
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
        rfc2965_hdrs = headers.get_all(b'Set-Cookie2', [])
        ns_hdrs = headers.get_all(b'Set-Cookie', [])
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
        _debug(b'extract_cookies: %s', response.info())
        self._cookies_lock.acquire()
        try:
            self._policy._now = self._now = int(time.time())
            for cookie in self.make_cookies(response, request):
                if self._policy.set_ok(cookie, request):
                    _debug(b' setting cookie: %s', cookie)
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
                raise ValueError(b'domain and path must be given to remove a cookie by name')
            del self._cookies[domain][path][name]
        elif path is not None:
            if domain is None:
                raise ValueError(b'domain must be given to remove cookies by path')
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

    @as_native_str()
    def __repr__(self):
        r = []
        for cookie in self:
            r.append(repr(cookie))

        return b'<%s[%s]>' % (self.__class__, (b', ').join(r))

    def __str__(self):
        r = []
        for cookie in self:
            r.append(str(cookie))

        return b'<%s[%s]>' % (self.__class__, (b', ').join(r))


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
                filename + b''
            except:
                raise ValueError(b'filename must be string-like')

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


def lwp_cookie_str(cookie):
    """Return string representation of Cookie in an the LWP cookie file format.

    Actually, the format is extended a bit -- see module docstring.

    """
    h = [
     (
      cookie.name, cookie.value),
     (
      b'path', cookie.path),
     (
      b'domain', cookie.domain)]
    if cookie.port is not None:
        h.append((b'port', cookie.port))
    if cookie.path_specified:
        h.append(('path_spec', None))
    if cookie.port_specified:
        h.append(('port_spec', None))
    if cookie.domain_initial_dot:
        h.append(('domain_dot', None))
    if cookie.secure:
        h.append(('secure', None))
    if cookie.expires:
        h.append((b'expires',
         time2isoz(float(cookie.expires))))
    if cookie.discard:
        h.append(('discard', None))
    if cookie.comment:
        h.append((b'comment', cookie.comment))
    if cookie.comment_url:
        h.append((b'commenturl', cookie.comment_url))
    keys = sorted(cookie._rest.keys())
    for k in keys:
        h.append((k, str(cookie._rest[k])))

    h.append((b'version', str(cookie.version)))
    return join_header_words([h])


class LWPCookieJar(FileCookieJar):
    """
    The LWPCookieJar saves a sequence of "Set-Cookie3" lines.
    "Set-Cookie3" is the format used by the libwww-perl libary, not known
    to be compatible with any browser, but which is easy to read and
    doesn't lose information about RFC 2965 cookies.

    Additional methods

    as_lwp_str(ignore_discard=True, ignore_expired=True)

    """

    def as_lwp_str(self, ignore_discard=True, ignore_expires=True):
        r"""Return cookies as a string of "\n"-separated "Set-Cookie3" headers.

        ignore_discard and ignore_expires: see docstring for FileCookieJar.save

        """
        now = time.time()
        r = []
        for cookie in self:
            if not ignore_discard and cookie.discard:
                continue
            if not ignore_expires and cookie.is_expired(now):
                continue
            r.append(b'Set-Cookie3: %s' % lwp_cookie_str(cookie))

        return (b'\n').join(r + [b''])

    def save(self, filename=None, ignore_discard=False, ignore_expires=False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        f = open(filename, b'w')
        try:
            f.write(b'#LWP-Cookies-2.0\n')
            f.write(self.as_lwp_str(ignore_discard, ignore_expires))
        finally:
            f.close()

        return

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        magic = f.readline()
        if not self.magic_re.search(magic):
            msg = b'%r does not look like a Set-Cookie3 (LWP) format file' % filename
            raise LoadError(msg)
        now = time.time()
        header = b'Set-Cookie3:'
        boolean_attrs = ('port_spec', 'path_spec', 'domain_dot', 'secure', 'discard')
        value_attrs = ('version', 'port', 'path', 'domain', 'expires', 'comment', 'commenturl')
        try:
            while 1:
                line = f.readline()
                if line == b'':
                    break
                if not line.startswith(header):
                    continue
                line = line[len(header):].strip()
                for data in split_header_words([line]):
                    name, value = data[0]
                    standard = {}
                    rest = {}
                    for k in boolean_attrs:
                        standard[k] = False

                    for k, v in data[1:]:
                        if k is not None:
                            lc = k.lower()
                        else:
                            lc = None
                        if lc in value_attrs or lc in boolean_attrs:
                            k = lc
                        if k in boolean_attrs:
                            if v is None:
                                v = True
                            standard[k] = v
                        elif k in value_attrs:
                            standard[k] = v
                        else:
                            rest[k] = v

                    h = standard.get
                    expires = h(b'expires')
                    discard = h(b'discard')
                    if expires is not None:
                        expires = iso2time(expires)
                    if expires is None:
                        discard = True
                    domain = h(b'domain')
                    domain_specified = domain.startswith(b'.')
                    c = Cookie(h(b'version'), name, value, h(b'port'), h(b'port_spec'), domain, domain_specified, h(b'domain_dot'), h(b'path'), h(b'path_spec'), h(b'secure'), expires, discard, h(b'comment'), h(b'commenturl'), rest)
                    if not ignore_discard and c.discard:
                        continue
                    if not ignore_expires and c.is_expired(now):
                        continue
                    self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            _warn_unhandled_exception()
            raise LoadError(b'invalid Set-Cookie3 format file %r: %r' % (
             filename, line))

        return


class MozillaCookieJar(FileCookieJar):
    """

    WARNING: you may want to backup your browser's cookies file if you use
    this class to save cookies.  I *think* it works, but there have been
    bugs in the past!

    This class differs from CookieJar only in the format it uses to save and
    load cookies to and from a file.  This class uses the Mozilla/Netscape
    `cookies.txt' format.  lynx uses this file format, too.

    Don't expect cookies saved while the browser is running to be noticed by
    the browser (in fact, Mozilla on unix will overwrite your saved cookies if
    you change them on disk while it's running; on Windows, you probably can't
    save at all while the browser is running).

    Note that the Mozilla/Netscape format will downgrade RFC2965 cookies to
    Netscape cookies on saving.

    In particular, the cookie version and port number information is lost,
    together with information about whether or not Path, Port and Discard were
    specified by the Set-Cookie2 (or Set-Cookie) header, and whether or not the
    domain as set in the HTTP header started with a dot (yes, I'm aware some
    domains in Netscape files start with a dot and some don't -- trust me, you
    really don't want to know any more about this).

    Note that though Mozilla and Netscape use the same format, they use
    slightly different headers.  The class saves cookies using the Netscape
    header by default (Mozilla can cope with that).

    """
    magic_re = re.compile(b'#( Netscape)? HTTP Cookie File')
    header = b'# Netscape HTTP Cookie File\n# http://www.netscape.com/newsref/std/cookie_spec.html\n# This is a generated file!  Do not edit.\n\n'

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        now = time.time()
        magic = f.readline()
        if not self.magic_re.search(magic):
            f.close()
            raise LoadError(b'%r does not look like a Netscape format cookies file' % filename)
        try:
            while 1:
                line = f.readline()
                if line == b'':
                    break
                if line.endswith(b'\n'):
                    line = line[:-1]
                if line.strip().startswith(('#', '$')) or line.strip() == b'':
                    continue
                domain, domain_specified, path, secure, expires, name, value = line.split(b'\t')
                secure = secure == b'TRUE'
                domain_specified = domain_specified == b'TRUE'
                if name == b'':
                    name = value
                    value = None
                initial_dot = domain.startswith(b'.')
                assert domain_specified == initial_dot
                discard = False
                if expires == b'':
                    expires = None
                    discard = True
                c = Cookie(0, name, value, None, False, domain, domain_specified, initial_dot, path, False, secure, expires, discard, None, None, {})
                if not ignore_discard and c.discard:
                    continue
                if not ignore_expires and c.is_expired(now):
                    continue
                self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            _warn_unhandled_exception()
            raise LoadError(b'invalid Netscape format cookies file %r: %r' % (
             filename, line))

        return

    def save(self, filename=None, ignore_discard=False, ignore_expires=False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        f = open(filename, b'w')
        try:
            f.write(self.header)
            now = time.time()
            for cookie in self:
                if not ignore_discard and cookie.discard:
                    continue
                if not ignore_expires and cookie.is_expired(now):
                    continue
                if cookie.secure:
                    secure = b'TRUE'
                else:
                    secure = b'FALSE'
                if cookie.domain.startswith(b'.'):
                    initial_dot = b'TRUE'
                else:
                    initial_dot = b'FALSE'
                if cookie.expires is not None:
                    expires = str(cookie.expires)
                else:
                    expires = b''
                if cookie.value is None:
                    name = b''
                    value = cookie.name
                else:
                    name = cookie.name
                    value = cookie.value
                f.write((b'\t').join([cookie.domain, initial_dot, cookie.path,
                 secure, expires, name, value]) + b'\n')

        finally:
            f.close()

        return