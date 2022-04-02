# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: http\cookiejar.py
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
__all__ = [
 'Cookie', 'CookieJar', 'CookiePolicy', 'DefaultCookiePolicy',
 'FileCookieJar', 'LWPCookieJar', 'LoadError', 'MozillaCookieJar']
import os, copy, datetime, re, time, urllib.parse, urllib.request, threading as _threading, http.client
from calendar import timegm
debug = False
logger = None

def _debug(*args):
    global logger
    if not debug:
        return
    if not logger:
        import logging
        logger = logging.getLogger('http.cookiejar')
    return (logger.debug)(*args)


DEFAULT_HTTP_PORT = str(http.client.HTTP_PORT)
MISSING_FILENAME_TEXT = 'a filename was not supplied (nor was the CookieJar instance initialised with one)'

def _warn_unhandled_exception():
    import io, warnings, traceback
    f = io.StringIO()
    traceback.print_exc(None, f)
    msg = f.getvalue()
    warnings.warn(('http.cookiejar bug!\n%s' % msg), stacklevel=2)


EPOCH_YEAR = 1970

def _timegm(tt):
    year, month, mday, hour, min, sec = tt[:6]
    if year >= EPOCH_YEAR:
        if 1 <= month <= 12:
            if 1 <= mday <= 31:
                if 0 <= hour <= 24:
                    if 0 <= min <= 59:
                        if 0 <= sec <= 61:
                            return timegm(tt)
    return


DAYS = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
MONTHS_LOWER = []
for month in MONTHS:
    MONTHS_LOWER.append(month.lower())
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
            dt = datetime.datetime.utcnow()
        else:
            dt = datetime.datetime.utcfromtimestamp(t)
        return '%04d-%02d-%02d %02d:%02d:%02dZ' % (
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
        return '%s, %02d-%s-%04d %02d:%02d:%02d GMT' % (
         DAYS[dt.weekday()], dt.day, MONTHS[(dt.month - 1)],
         dt.year, dt.hour, dt.minute, dt.second)


    UTC_ZONES = {'GMT':None, 
     'UTC':None,  'UT':None,  'Z':None}
    TIMEZONE_RE = re.compile('^([-+])?(\\d\\d?):?(\\d\\d)?$', re.ASCII)

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


    def _str2time--- This code section failed: ---

 L. 144         0  LOAD_GLOBAL              int
                2  LOAD_FAST                'yr'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'yr'

 L. 145         8  LOAD_FAST                'yr'
               10  LOAD_GLOBAL              datetime
               12  LOAD_ATTR                MAXYEAR
               14  COMPARE_OP               >
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 146        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 150        22  SETUP_FINALLY        46  'to 46'

 L. 151        24  LOAD_GLOBAL              MONTHS_LOWER
               26  LOAD_METHOD              index
               28  LOAD_FAST                'mon'
               30  LOAD_METHOD              lower
               32  CALL_METHOD_0         0  ''
               34  CALL_METHOD_1         1  ''
               36  LOAD_CONST               1
               38  BINARY_ADD       
               40  STORE_FAST               'mon'
               42  POP_BLOCK        
               44  JUMP_FORWARD        140  'to 140'
             46_0  COME_FROM_FINALLY    22  '22'

 L. 152        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   138  'to 138'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 154        60  SETUP_FINALLY        74  'to 74'

 L. 155        62  LOAD_GLOBAL              int
               64  LOAD_FAST                'mon'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'imon'
               70  POP_BLOCK        
               72  JUMP_FORWARD         98  'to 98'
             74_0  COME_FROM_FINALLY    60  '60'

 L. 156        74  DUP_TOP          
               76  LOAD_GLOBAL              ValueError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    96  'to 96'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 157        88  POP_EXCEPT       
               90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            80  '80'
               96  END_FINALLY      
             98_0  COME_FROM            72  '72'

 L. 158        98  LOAD_CONST               1
              100  LOAD_FAST                'imon'
              102  DUP_TOP          
              104  ROT_THREE        
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_FALSE   118  'to 118'
              110  LOAD_CONST               12
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_FALSE   128  'to 128'
              116  JUMP_FORWARD        122  'to 122'
            118_0  COME_FROM           108  '108'
              118  POP_TOP          
              120  JUMP_FORWARD        128  'to 128'
            122_0  COME_FROM           116  '116'

 L. 159       122  LOAD_FAST                'imon'
              124  STORE_FAST               'mon'
              126  JUMP_FORWARD        134  'to 134'
            128_0  COME_FROM           120  '120'
            128_1  COME_FROM           114  '114'

 L. 161       128  POP_EXCEPT       
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           126  '126'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            52  '52'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            44  '44'

 L. 164       140  LOAD_FAST                'hr'
              142  LOAD_CONST               None
              144  COMPARE_OP               is
              146  POP_JUMP_IF_FALSE   152  'to 152'

 L. 164       148  LOAD_CONST               0
              150  STORE_FAST               'hr'
            152_0  COME_FROM           146  '146'

 L. 165       152  LOAD_FAST                'min'
              154  LOAD_CONST               None
              156  COMPARE_OP               is
              158  POP_JUMP_IF_FALSE   164  'to 164'

 L. 165       160  LOAD_CONST               0
              162  STORE_FAST               'min'
            164_0  COME_FROM           158  '158'

 L. 166       164  LOAD_FAST                'sec'
              166  LOAD_CONST               None
              168  COMPARE_OP               is
              170  POP_JUMP_IF_FALSE   176  'to 176'

 L. 166       172  LOAD_CONST               0
              174  STORE_FAST               'sec'
            176_0  COME_FROM           170  '170'

 L. 168       176  LOAD_GLOBAL              int
              178  LOAD_FAST                'day'
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'day'

 L. 169       184  LOAD_GLOBAL              int
              186  LOAD_FAST                'hr'
              188  CALL_FUNCTION_1       1  ''
              190  STORE_FAST               'hr'

 L. 170       192  LOAD_GLOBAL              int
              194  LOAD_FAST                'min'
              196  CALL_FUNCTION_1       1  ''
              198  STORE_FAST               'min'

 L. 171       200  LOAD_GLOBAL              int
              202  LOAD_FAST                'sec'
              204  CALL_FUNCTION_1       1  ''
              206  STORE_FAST               'sec'

 L. 173       208  LOAD_FAST                'yr'
              210  LOAD_CONST               1000
              212  COMPARE_OP               <
          214_216  POP_JUMP_IF_FALSE   310  'to 310'

 L. 175       218  LOAD_GLOBAL              time
              220  LOAD_METHOD              localtime
              222  LOAD_GLOBAL              time
              224  LOAD_METHOD              time
              226  CALL_METHOD_0         0  ''
              228  CALL_METHOD_1         1  ''
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  STORE_FAST               'cur_yr'

 L. 176       236  LOAD_FAST                'cur_yr'
              238  LOAD_CONST               100
              240  BINARY_MODULO    
              242  STORE_FAST               'm'

 L. 177       244  LOAD_FAST                'yr'
              246  STORE_FAST               'tmp'

 L. 178       248  LOAD_FAST                'yr'
              250  LOAD_FAST                'cur_yr'
              252  BINARY_ADD       
              254  LOAD_FAST                'm'
              256  BINARY_SUBTRACT  
              258  STORE_FAST               'yr'

 L. 179       260  LOAD_FAST                'm'
              262  LOAD_FAST                'tmp'
              264  BINARY_SUBTRACT  
              266  STORE_FAST               'm'

 L. 180       268  LOAD_GLOBAL              abs
              270  LOAD_FAST                'm'
              272  CALL_FUNCTION_1       1  ''
              274  LOAD_CONST               50
              276  COMPARE_OP               >
          278_280  POP_JUMP_IF_FALSE   310  'to 310'

 L. 181       282  LOAD_FAST                'm'
              284  LOAD_CONST               0
              286  COMPARE_OP               >
          288_290  POP_JUMP_IF_FALSE   302  'to 302'

 L. 181       292  LOAD_FAST                'yr'
              294  LOAD_CONST               100
              296  BINARY_ADD       
              298  STORE_FAST               'yr'
              300  JUMP_FORWARD        310  'to 310'
            302_0  COME_FROM           288  '288'

 L. 182       302  LOAD_FAST                'yr'
              304  LOAD_CONST               100
              306  BINARY_SUBTRACT  
              308  STORE_FAST               'yr'
            310_0  COME_FROM           300  '300'
            310_1  COME_FROM           278  '278'
            310_2  COME_FROM           214  '214'

 L. 185       310  LOAD_GLOBAL              _timegm
              312  LOAD_FAST                'yr'
              314  LOAD_FAST                'mon'
              316  LOAD_FAST                'day'
              318  LOAD_FAST                'hr'
              320  LOAD_FAST                'min'
              322  LOAD_FAST                'sec'
              324  LOAD_FAST                'tz'
              326  BUILD_TUPLE_7         7 
              328  CALL_FUNCTION_1       1  ''
              330  STORE_FAST               't'

 L. 187       332  LOAD_FAST                't'
              334  LOAD_CONST               None
              336  COMPARE_OP               is-not
          338_340  POP_JUMP_IF_FALSE   394  'to 394'

 L. 189       342  LOAD_FAST                'tz'
              344  LOAD_CONST               None
              346  COMPARE_OP               is
          348_350  POP_JUMP_IF_FALSE   356  'to 356'

 L. 190       352  LOAD_STR                 'UTC'
              354  STORE_FAST               'tz'
            356_0  COME_FROM           348  '348'

 L. 191       356  LOAD_FAST                'tz'
              358  LOAD_METHOD              upper
              360  CALL_METHOD_0         0  ''
              362  STORE_FAST               'tz'

 L. 192       364  LOAD_GLOBAL              offset_from_tz_string
              366  LOAD_FAST                'tz'
              368  CALL_FUNCTION_1       1  ''
              370  STORE_FAST               'offset'

 L. 193       372  LOAD_FAST                'offset'
              374  LOAD_CONST               None
              376  COMPARE_OP               is
          378_380  POP_JUMP_IF_FALSE   386  'to 386'

 L. 194       382  LOAD_CONST               None
              384  RETURN_VALUE     
            386_0  COME_FROM           378  '378'

 L. 195       386  LOAD_FAST                't'
              388  LOAD_FAST                'offset'
              390  BINARY_SUBTRACT  
              392  STORE_FAST               't'
            394_0  COME_FROM           338  '338'

 L. 197       394  LOAD_FAST                't'
              396  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 92


    STRICT_DATE_RE = re.compile('^[SMTWF][a-z][a-z], (\\d\\d) ([JFMASOND][a-z][a-z]) (\\d\\d\\d\\d) (\\d\\d):(\\d\\d):(\\d\\d) GMT$', re.ASCII)
    WEEKDAY_RE = re.compile('^(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)[a-z]*,?\\s*', re.I | re.ASCII)
    LOOSE_HTTP_DATE_RE = re.compile('^\n    (\\d\\d?)            # day\n       (?:\\s+|[-\\/])\n    (\\w+)              # month\n        (?:\\s+|[-\\/])\n    (\\d+)              # year\n    (?:\n          (?:\\s+|:)    # separator before clock\n       (\\d\\d?):(\\d\\d)  # hour:min\n       (?::(\\d\\d))?    # optional seconds\n    )?                 # optional clock\n       \\s*\n    (?:\n       ([-+]?\\d{2,4}|(?![APap][Mm]\\b)[A-Za-z]+) # timezone\n       \\s*\n    )?\n    (?:\n       \\(\\w+\\)         # ASCII representation of timezone in parens.\n       \\s*\n    )?$', re.X | re.ASCII)

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


    ISO_DATE_RE = re.compile('^\n    (\\d{4})              # year\n       [-\\/]?\n    (\\d\\d?)              # numerical month\n       [-\\/]?\n    (\\d\\d?)              # day\n   (?:\n         (?:\\s+|[-:Tt])  # separator before clock\n      (\\d\\d?):?(\\d\\d)    # hour:min\n      (?::?(\\d\\d(?:\\.\\d*)?))?  # optional seconds (and fractional)\n   )?                    # optional clock\n      \\s*\n   (?:\n      ([-+]?\\d\\d?:?(:?\\d\\d)?\n       |Z|z)             # timezone  (Z is "zero meridian", i.e. GMT)\n      \\s*\n   )?$', re.X | re.ASCII)

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

    def split_header_words(header_values):
        r"""Parse header values into a list of lists containing key,value pairs.

    The function knows how to deal with ",", ";" and "=" as well as quoted
    values after "=".  A list of space separated tokens are parsed as if they
    were separated by ";".

    If the header_values passed as argument contains multiple values, then they
    are treated as if they were a single value separated by comma ",".

    This means that this function is useful for parsing header fields that
    follow this syntax (BNF as from the HTTP/1.1 specification, but we relax
    the requirement for tokens).

      headers           = #header
      header            = (token | parameter) *( [";"] (token | parameter))

      token             = 1*<any CHAR except CTLs or separators>
      separators        = "(" | ")" | "<" | ">" | "@"
                        | "," | ";" | ":" | "\" | <">
                        | "/" | "[" | "]" | "?" | "="
                        | "{" | "}" | SP | HT

      quoted-string     = ( <"> *(qdtext | quoted-pair ) <"> )
      qdtext            = <any TEXT except <">>
      quoted-pair       = "\" CHAR

      parameter         = attribute "=" value
      attribute         = token
      value             = token | quoted-string

    Each header is represented by a list of key/value pairs.  The value for a
    simple token (not part of a parameter) is None.  Syntactically incorrect
    headers will not necessarily be parsed as you would want.

    This is easier to describe with some examples:

    >>> split_header_words(['foo="bar"; port="80,81"; discard, bar=baz'])
    [[('foo', 'bar'), ('port', '80,81'), ('discard', None)], [('bar', 'baz')]]
    >>> split_header_words(['text/html; charset="iso-8859-1"'])
    [[('text/html', None), ('charset', 'iso-8859-1')]]
    >>> split_header_words([r'Basic realm="\"foo\bar\""'])
    [[('Basic', None), ('realm', '"foobar"')]]

    """
        assert not isinstance(header_values, str)
        result = []
        for text in header_values:
            orig_text = text
            pairs = []
            if text:
                m = HEADER_TOKEN_RE.search(text)
                if m:
                    text = unmatched(m)
                    name = m.group(1)
                    m = HEADER_QUOTED_VALUE_RE.search(text)
                    if m:
                        text = unmatched(m)
                        value = m.group(1)
                        value = HEADER_ESCAPE_RE.sub('\\1', value)
                    else:
                        m = HEADER_VALUE_RE.search(text)
                        if m:
                            text = unmatched(m)
                            value = m.group(1)
                            value = value.rstrip()
                        else:
                            value = None
                    pairs.append((name, value))
            elif text.lstrip().startswith(','):
                text = text.lstrip()[1:]
                if pairs:
                    result.append(pairs)
                pairs = []
            else:
                non_junk, nr_junk_chars = re.subn('^[=\\s;]*', '', text)
                assert nr_junk_chars > 0, "split_header_words bug: '%s', '%s', %s" % (
                 orig_text, text, pairs)
                text = non_junk
            if pairs:
                result.append(pairs)
            return result


    HEADER_JOIN_ESCAPE_RE = re.compile('([\\"\\\\])')

    def join_header_words(lists):
        """Do the inverse (almost) of the conversion done by split_header_words.

    Takes a list of lists of (key, value) pairs and produces a single header
    value.  Attribute values are quoted if needed.

    >>> join_header_words([[("text/plain", None), ("charset", "iso-8859-1")]])
    'text/plain; charset="iso-8859-1"'
    >>> join_header_words([[("text/plain", None)], [("charset", "iso-8859-1")]])
    'text/plain, charset="iso-8859-1"'

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
        else:
            if attr:
                headers.append('; '.join(attr))
            return ', '.join(headers)


    def strip_quotes(text):
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

        for ii, param in enumerate(ns_header.split(';')):
            param = param.strip()
            key, sep, val = param.partition('=')
            key = key.strip()
            if not key:
                if ii == 0:
                    break
                    break
            else:
                val = val.strip() if sep else None
                if ii != 0:
                    lc = key.lower()
                    if lc in known_attrs:
                        key = lc
                    elif key == 'version':
                        if val is not None:
                            val = strip_quotes(val)
                        version_set = True
                    else:
                        if key == 'expires':
                            if val is not None:
                                val = http2time(strip_quotes(val))
                pairs.append((key, val))
        else:
            if pairs:
                if not version_set:
                    pairs.append(('version', '0'))
                result.append(pairs)
            return result


    IPV4_RE = re.compile('\\.\\d+$', re.ASCII)

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
        else:
            if not is_HDN(A):
                return False
            else:
                i = A.rfind(B)
                if i == -1 or i == 0:
                    return False
                return B.startswith('.') or False
            return is_HDN(B[1:]) or False
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
        if initial_dot:
            if A.endswith(B):
                return True
        if not initial_dot:
            if A == B:
                return True
        return False


    cut_port_re = re.compile(':\\d+$', re.ASCII)

    def request_host(request):
        """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
        url = request.get_full_url()
        host = urllib.parse.urlparse(url)[1]
        if host == '':
            host = request.get_header('Host', '')
        host = cut_port_re.sub('', host, 1)
        return host.lower()


    def eff_request_host(request):
        """Return a tuple (request-host, effective request-host name).

    As defined by RFC 2965, except both are lowercased.

    """
        erhn = req_host = request_host(request)
        if req_host.find('.') == -1:
            if not IPV4_RE.search(req_host):
                erhn = req_host + '.local'
        return (
         req_host, erhn)


    def request_path(request):
        """Path component of request-URI, as defined by RFC 2965."""
        url = request.get_full_url()
        parts = urllib.parse.urlsplit(url)
        path = escape_path(parts.path)
        if not path.startswith('/'):
            path = '/' + path
        return path


    def request_port--- This code section failed: ---

 L. 651         0  LOAD_FAST                'request'
                2  LOAD_ATTR                host
                4  STORE_FAST               'host'

 L. 652         6  LOAD_FAST                'host'
                8  LOAD_METHOD              find
               10  LOAD_STR                 ':'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'i'

 L. 653        16  LOAD_FAST                'i'
               18  LOAD_CONST               0
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_FALSE    88  'to 88'

 L. 654        24  LOAD_FAST                'host'
               26  LOAD_FAST                'i'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  LOAD_CONST               None
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  STORE_FAST               'port'

 L. 655        40  SETUP_FINALLY        54  'to 54'

 L. 656        42  LOAD_GLOBAL              int
               44  LOAD_FAST                'port'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          
               50  POP_BLOCK        
               52  JUMP_ABSOLUTE        92  'to 92'
             54_0  COME_FROM_FINALLY    40  '40'

 L. 657        54  DUP_TOP          
               56  LOAD_GLOBAL              ValueError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    84  'to 84'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 658        68  LOAD_GLOBAL              _debug
               70  LOAD_STR                 "nonnumeric port: '%s'"
               72  LOAD_FAST                'port'
               74  CALL_FUNCTION_2       2  ''
               76  POP_TOP          

 L. 659        78  POP_EXCEPT       
               80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            60  '60'
               84  END_FINALLY      
               86  JUMP_FORWARD         92  'to 92'
             88_0  COME_FROM            22  '22'

 L. 661        88  LOAD_GLOBAL              DEFAULT_HTTP_PORT
               90  STORE_FAST               'port'
             92_0  COME_FROM            86  '86'

 L. 662        92  LOAD_FAST                'port'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 80


    HTTP_PATH_SAFE = "%/;:@&=+$,!~*'()"
    ESCAPED_CHAR_RE = re.compile('%([0-9a-fA-F][0-9a-fA-F])')

    def uppercase_escaped_char(match):
        return '%%%s' % match.group(1).upper()


    def escape_path(path):
        """Escape any invalid characters in HTTP URL, and uppercase all escapes."""
        path = urllib.parse.quote(path, HTTP_PATH_SAFE)
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
            if is_HDN(h):
                if i >= 0 or b == 'local':
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
        if not domain_match(req_host, reach(request.origin_req_host)):
            return True
        return False


    class Cookie:
        __doc__ = 'HTTP Cookie.\n\n    This class represents both Netscape and RFC 2965 cookies.\n\n    This is deliberately a very simple class.  It just holds attributes.  It\'s\n    possible to construct Cookie instances that don\'t comply with the cookie\n    standards.  CookieJar.make_cookies is the factory function for Cookie\n    objects -- it deals with cookie parsing, supplying defaults, and\n    normalising to the representation used in this class.  CookiePolicy is\n    responsible for checking them to see whether they should be accepted from\n    and returned to the server.\n\n    Note that the port may be present in the headers, but unspecified ("Port"\n    rather than"Port=80", for example); if this is the case, port is None.\n\n    '

        def __init__(self, version, name, value, port, port_specified, domain, domain_specified, domain_initial_dot, path, path_specified, secure, expires, discard, comment, comment_url, rest, rfc2109=False):
            if version is not None:
                version = int(version)
            else:
                if expires is not None:
                    expires = int(float(expires))
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

        def has_nonstandard_attr(self, name):
            return name in self._rest

        def get_nonstandard_attr(self, name, default=None):
            return self._rest.get(name, default)

        def set_nonstandard_attr(self, name, value):
            self._rest[name] = value

        def is_expired(self, now=None):
            if now is None:
                now = time.time()
            if self.expires is not None:
                if self.expires <= now:
                    return True
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
            else:
                args.append('rest=%s' % repr(self._rest))
                args.append('rfc2109=%s' % repr(self.rfc2109))
                return '%s(%s)' % (self.__class__.__name__, ', '.join(args))


    class CookiePolicy:
        __doc__ = 'Defines which cookies get accepted from and returned to server.\n\n    May also modify cookies, though this is probably a bad idea.\n\n    The subclass DefaultCookiePolicy defines the standard rules for Netscape\n    and RFC 2965 cookies -- override that if you want a customized policy.\n\n    '

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
        __doc__ = 'Implements the standard rules for accepting and returning cookies.'
        DomainStrictNoDots = 1
        DomainStrictNonDomain = 2
        DomainRFC2965Match = 4
        DomainLiberal = 0
        DomainStrict = DomainStrictNoDots | DomainStrictNonDomain

        def __init__(self, blocked_domains=None, allowed_domains=None, netscape=True, rfc2965=False, rfc2109_as_netscape=None, hide_cookie2=False, strict_domain=False, strict_rfc2965_unverifiable=True, strict_ns_unverifiable=False, strict_ns_domain=DomainLiberal, strict_ns_set_initial_dollar=False, strict_ns_set_path=False, secure_protocols=('https', 'wss')):
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
            self.secure_protocols = secure_protocols
            if blocked_domains is not None:
                self._blocked_domains = tuple(blocked_domains)
            else:
                self._blocked_domains = ()
            if allowed_domains is not None:
                allowed_domains = tuple(allowed_domains)
            self._allowed_domains = allowed_domains

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

        def is_not_allowed(self, domain):
            if self._allowed_domains is None:
                return False
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
                if cookie.version > 0:
                    if not self.rfc2965:
                        _debug('   RFC 2965 cookies are switched off')
                        return False
                if cookie.version == 0:
                    self.netscape or _debug('   Netscape cookies are switched off')
                    return False
            return True

        def set_ok_verifiability(self, cookie, request):
            if request.unverifiable:
                if is_third_party(request):
                    if cookie.version > 0:
                        if self.strict_rfc2965_unverifiable:
                            _debug('   third-party RFC 2965 cookie during unverifiable transaction')
                            return False
                    if cookie.version == 0:
                        if self.strict_ns_unverifiable:
                            _debug('   third-party Netscape cookie during unverifiable transaction')
                            return False
            return True

        def set_ok_name(self, cookie, request):
            if cookie.version == 0:
                if self.strict_ns_set_initial_dollar:
                    if cookie.name.startswith('$'):
                        _debug("   illegal name (starts with '$'): '%s'", cookie.name)
                        return False
            return True

        def set_ok_path(self, cookie, request):
            if cookie.path_specified:
                req_path = request_path(request)
                if (cookie.version > 0 or cookie.version) == 0:
                    if self.strict_ns_set_path:
                        if not self.path_return_ok(cookie.path, request):
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
                if self.strict_domain:
                    if domain.count('.') >= 2:
                        i = domain.rfind('.')
                        j = domain.rfind('.', 0, i)
                        if j == 0:
                            tld = domain[i + 1:]
                            sld = domain[j + 1:i]
                            if sld.lower() in ('co', 'ac', 'com', 'edu', 'org', 'net',
                                               'gov', 'mil', 'int', 'aero', 'biz',
                                               'cat', 'coop', 'info', 'jobs', 'mobi',
                                               'museum', 'name', 'pro', 'travel',
                                               'eu'):
                                if len(tld) == 2:
                                    _debug('   country-code second level domain %s', domain)
                                    return False
                elif domain.startswith('.'):
                    undotted_domain = domain[1:]
                else:
                    undotted_domain = domain
                embedded_dots = undotted_domain.find('.') >= 0
                if not embedded_dots:
                    if domain != '.local':
                        _debug('   non-local domain %s contains no embedded dot', domain)
                        return False
                if cookie.version == 0 and not erhn.endswith(domain) or erhn.startswith('.'):
                    if not ('.' + erhn).endswith(domain):
                        _debug('   effective request-host %s (even with added initial dot) does not end with %s', erhn, domain)
                        return False
                    else:
                        if cookie.version > 0 or self.strict_ns_domain & self.DomainRFC2965Match:
                            if not domain_match(erhn, domain):
                                _debug('   effective request-host %s does not domain-match %s', erhn, domain)
                                return False
                        if cookie.version > 0 or self.strict_ns_domain & self.DomainStrictNoDots:
                            host_prefix = req_host[:-len(domain)]
                            if host_prefix.find('.') >= 0:
                                if not IPV4_RE.search(req_host):
                                    _debug('   host prefix %s for domain %s contains a dot', host_prefix, domain)
                                    return False
            return True

        def set_ok_port--- This code section failed: ---

 L.1068         0  LOAD_FAST                'cookie'
                2  LOAD_ATTR                port_specified
                4  POP_JUMP_IF_FALSE   132  'to 132'

 L.1069         6  LOAD_GLOBAL              request_port
                8  LOAD_FAST                'request'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'req_port'

 L.1070        14  LOAD_FAST                'req_port'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.1071        22  LOAD_STR                 '80'
               24  STORE_FAST               'req_port'
               26  JUMP_FORWARD         36  'to 36'
             28_0  COME_FROM            20  '20'

 L.1073        28  LOAD_GLOBAL              str
               30  LOAD_FAST                'req_port'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'req_port'
             36_0  COME_FROM            26  '26'

 L.1074        36  LOAD_FAST                'cookie'
               38  LOAD_ATTR                port
               40  LOAD_METHOD              split
               42  LOAD_STR                 ','
               44  CALL_METHOD_1         1  ''
               46  GET_ITER         
             48_0  COME_FROM           106  '106'
               48  FOR_ITER            114  'to 114'
               50  STORE_FAST               'p'

 L.1075        52  SETUP_FINALLY        66  'to 66'

 L.1076        54  LOAD_GLOBAL              int
               56  LOAD_FAST                'p'
               58  CALL_FUNCTION_1       1  ''
               60  POP_TOP          
               62  POP_BLOCK        
               64  JUMP_FORWARD        100  'to 100'
             66_0  COME_FROM_FINALLY    52  '52'

 L.1077        66  DUP_TOP          
               68  LOAD_GLOBAL              ValueError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    98  'to 98'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.1078        80  LOAD_GLOBAL              _debug
               82  LOAD_STR                 '   bad port %s (not numeric)'
               84  LOAD_FAST                'p'
               86  CALL_FUNCTION_2       2  ''
               88  POP_TOP          

 L.1079        90  POP_EXCEPT       
               92  POP_TOP          
               94  LOAD_CONST               False
               96  RETURN_VALUE     
             98_0  COME_FROM            72  '72'
               98  END_FINALLY      
            100_0  COME_FROM            64  '64'

 L.1080       100  LOAD_FAST                'p'
              102  LOAD_FAST                'req_port'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE    48  'to 48'

 L.1081       108  POP_TOP          
              110  BREAK_LOOP          132  'to 132'
              112  JUMP_BACK            48  'to 48'

 L.1083       114  LOAD_GLOBAL              _debug
              116  LOAD_STR                 '   request port (%s) not found in %s'

 L.1084       118  LOAD_FAST                'req_port'

 L.1084       120  LOAD_FAST                'cookie'
              122  LOAD_ATTR                port

 L.1083       124  CALL_FUNCTION_3       3  ''
              126  POP_TOP          

 L.1085       128  LOAD_CONST               False
              130  RETURN_VALUE     
            132_0  COME_FROM             4  '4'

 L.1086       132  LOAD_CONST               True
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 92

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
            if cookie.version > 0:
                if not self.rfc2965:
                    _debug('   RFC 2965 cookies are switched off')
                    return False
            if cookie.version == 0:
                if not self.netscape:
                    _debug('   Netscape cookies are switched off')
                    return False
            return True

        def return_ok_verifiability(self, cookie, request):
            if request.unverifiable:
                if is_third_party(request):
                    if cookie.version > 0:
                        if self.strict_rfc2965_unverifiable:
                            _debug('   third-party RFC 2965 cookie during unverifiable transaction')
                            return False
                    if cookie.version == 0:
                        if self.strict_ns_unverifiable:
                            _debug('   third-party Netscape cookie during unverifiable transaction')
                            return False
            return True

        def return_ok_secure(self, cookie, request):
            if cookie.secure:
                if request.type not in self.secure_protocols:
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
                    _debug('   request port %s does not match cookie port %s', req_port, cookie.port)
                    return False

            return True

        def return_ok_domain(self, cookie, request):
            req_host, erhn = eff_request_host(request)
            domain = cookie.domain
            if domain:
                dotdomain = domain.startswith('.') or '.' + domain
            else:
                dotdomain = domain
            if cookie.version == 0:
                if self.strict_ns_domain & self.DomainStrictNonDomain:
                    if not cookie.domain_specified:
                        if domain != erhn:
                            _debug('   cookie with unspecified domain does not string-compare equal to request domain')
                            return False
            if cookie.version > 0:
                if not domain_match(erhn, domain):
                    _debug('   effective request-host name %s does not domain-match RFC 2965 cookie domain %s', erhn, domain)
                    return False
            if cookie.version == 0:
                if not ('.' + erhn).endswith(dotdomain):
                    _debug('   request-host %s does not match Netscape cookie domain %s', req_host, domain)
                    return False
            return True

        def domain_return_ok(self, domain, request):
            req_host, erhn = eff_request_host(request)
            if not req_host.startswith('.'):
                req_host = '.' + req_host
            if not erhn.startswith('.'):
                erhn = '.' + erhn
            if domain:
                dotdomain = domain.startswith('.') or '.' + domain
            else:
                dotdomain = domain
            if not req_host.endswith(dotdomain):
                if not erhn.endswith(dotdomain):
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
            pathlen = len(path)
            if req_path == path:
                return True
            if req_path.startswith(path):
                if path.endswith('/') or req_path[pathlen:pathlen + 1] == '/':
                    return True
            _debug('  %s does not path-match %s', req_path, path)
            return False


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
                (yield from deepvalues(obj))
            if not mapping:
                (yield obj)


    class Absent:
        pass


    class CookieJar:
        __doc__ = 'Collection of HTTP cookies.\n\n    You may not need to know about this class: try\n    urllib.request.build_opener(HTTPCookieProcessor).open(url).\n    '
        non_word_re = re.compile('\\W')
        quote_re = re.compile('([\\"\\\\])')
        strict_domain_re = re.compile('\\.?[^.]*')
        domain_re = re.compile('[^.]*')
        dots_re = re.compile('^\\.+')
        magic_re = re.compile('^\\#LWP-Cookies-(\\d+\\.\\d+)', re.ASCII)

        def __init__(self, policy=None):
            if policy is None:
                policy = DefaultCookiePolicy()
            self._policy = policy
            self._cookies_lock = _threading.RLock()
            self._cookies = {}

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
                    pass
                else:
                    cookies_by_name = cookies_by_path[path]

            for cookie in cookies_by_name.values():
                if not self._policy.return_ok(cookie, request):
                    _debug('   not returning cookie')
                else:
                    _debug("   it's a match")
                    cookies.append(cookie)
            else:
                return cookies

        def _cookies_for_request(self, request):
            """Return a list of cookies to be returned to server."""
            cookies = []
            for domain in self._cookies.keys():
                cookies.extend(self._cookies_for_domain(domain, request))
            else:
                return cookies

        def _cookie_attrs(self, cookies):
            """Return a list of cookie-attributes to be returned to server.

        like ['foo="bar"; $Path="/"', ...]

        The $Version attribute is also added when appropriate (currently only
        once per request).

        """
            cookies.sort(key=(lambda a: len(a.path)), reverse=True)
            version_set = False
            attrs = []
            for cookie in cookies:
                version = cookie.version
                if not version_set:
                    version_set = True
                    if version > 0:
                        attrs.append('$Version=%s' % version)
                if cookie.value is not None:
                    if self.non_word_re.search(cookie.value):
                        if version > 0:
                            value = self.quote_re.sub('\\\\\\1', cookie.value)
                        else:
                            value = cookie.value
                    elif cookie.value is None:
                        attrs.append(cookie.name)
                    else:
                        attrs.append('%s=%s' % (cookie.name, value))
                    if version > 0:
                        if cookie.path_specified:
                            attrs.append('$Path="%s"' % cookie.path)
                        if cookie.domain.startswith('.'):
                            domain = cookie.domain
                            if not cookie.domain_initial_dot:
                                if domain.startswith('.'):
                                    domain = domain[1:]
                            attrs.append('$Domain="%s"' % domain)
                        if cookie.port is not None:
                            p = '$Port'
                            if cookie.port_specified:
                                p = p + '="%s"' % cookie.port
                            attrs.append(p)
                return attrs

        def add_cookie_header(self, request):
            """Add correct Cookie: header to request (urllib.request.Request object).

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
                        request.add_unredirected_header('Cookie', '; '.join(attrs))
                if self._policy.rfc2965:
                    if not self._policy.hide_cookie2:
                        if not request.has_header('Cookie2'):
                            for cookie in cookies:
                                if cookie.version != 1:
                                    request.add_unredirected_header('Cookie2', '$Version="1"')
                                    break

            finally:
                self._cookies_lock.release()

            self.clear_expired_cookies()

        def _normalized_cookie_tuples--- This code section failed: ---

 L.1399         0  BUILD_LIST_0          0 
                2  STORE_FAST               'cookie_tuples'

 L.1401         4  LOAD_CONST               ('discard', 'secure')
                6  STORE_FAST               'boolean_attrs'

 L.1402         8  LOAD_CONST               ('version', 'expires', 'max-age', 'domain', 'path', 'port', 'comment', 'commenturl')
               10  STORE_FAST               'value_attrs'

 L.1407        12  LOAD_FAST                'attrs_set'
               14  GET_ITER         
            16_18  FOR_ITER            398  'to 398'
               20  STORE_FAST               'cookie_attrs'

 L.1408        22  LOAD_FAST                'cookie_attrs'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'name'
               32  STORE_FAST               'value'

 L.1418        34  LOAD_CONST               False
               36  STORE_FAST               'max_age_set'

 L.1420        38  LOAD_CONST               False
               40  STORE_FAST               'bad_cookie'

 L.1422        42  BUILD_MAP_0           0 
               44  STORE_FAST               'standard'

 L.1423        46  BUILD_MAP_0           0 
               48  STORE_FAST               'rest'

 L.1424        50  LOAD_FAST                'cookie_attrs'
               52  LOAD_CONST               1
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  GET_ITER         
            62_64  FOR_ITER            370  'to 370'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'k'
               70  STORE_FAST               'v'

 L.1425        72  LOAD_FAST                'k'
               74  LOAD_METHOD              lower
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'lc'

 L.1427        80  LOAD_FAST                'lc'
               82  LOAD_FAST                'value_attrs'
               84  COMPARE_OP               in
               86  POP_JUMP_IF_TRUE     96  'to 96'
               88  LOAD_FAST                'lc'
               90  LOAD_FAST                'boolean_attrs'
               92  COMPARE_OP               in
               94  POP_JUMP_IF_FALSE   100  'to 100'
             96_0  COME_FROM            86  '86'

 L.1428        96  LOAD_FAST                'lc'
               98  STORE_FAST               'k'
            100_0  COME_FROM            94  '94'

 L.1429       100  LOAD_FAST                'k'
              102  LOAD_FAST                'boolean_attrs'
              104  COMPARE_OP               in
              106  POP_JUMP_IF_FALSE   120  'to 120'
              108  LOAD_FAST                'v'
              110  LOAD_CONST               None
              112  COMPARE_OP               is
              114  POP_JUMP_IF_FALSE   120  'to 120'

 L.1432       116  LOAD_CONST               True
              118  STORE_FAST               'v'
            120_0  COME_FROM           114  '114'
            120_1  COME_FROM           106  '106'

 L.1433       120  LOAD_FAST                'k'
              122  LOAD_FAST                'standard'
              124  COMPARE_OP               in
              126  POP_JUMP_IF_FALSE   130  'to 130'

 L.1435       128  JUMP_BACK            62  'to 62'
            130_0  COME_FROM           126  '126'

 L.1436       130  LOAD_FAST                'k'
              132  LOAD_STR                 'domain'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   172  'to 172'

 L.1437       138  LOAD_FAST                'v'
              140  LOAD_CONST               None
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L.1438       146  LOAD_GLOBAL              _debug
              148  LOAD_STR                 '   missing value for domain attribute'
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L.1439       154  LOAD_CONST               True
              156  STORE_FAST               'bad_cookie'

 L.1440       158  POP_TOP          
          160_162  JUMP_ABSOLUTE       370  'to 370'
            164_0  COME_FROM           144  '144'

 L.1442       164  LOAD_FAST                'v'
              166  LOAD_METHOD              lower
              168  CALL_METHOD_0         0  ''
              170  STORE_FAST               'v'
            172_0  COME_FROM           136  '136'

 L.1443       172  LOAD_FAST                'k'
              174  LOAD_STR                 'expires'
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   204  'to 204'

 L.1444       180  LOAD_FAST                'max_age_set'
              182  POP_JUMP_IF_FALSE   186  'to 186'

 L.1446       184  JUMP_BACK            62  'to 62'
            186_0  COME_FROM           182  '182'

 L.1447       186  LOAD_FAST                'v'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L.1448       194  LOAD_GLOBAL              _debug
              196  LOAD_STR                 '   missing or invalid value for expires attribute: treating as session cookie'
              198  CALL_FUNCTION_1       1  ''
              200  POP_TOP          

 L.1450       202  JUMP_BACK            62  'to 62'
            204_0  COME_FROM           192  '192'
            204_1  COME_FROM           178  '178'

 L.1451       204  LOAD_FAST                'k'
              206  LOAD_STR                 'max-age'
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   288  'to 288'

 L.1452       214  LOAD_CONST               True
              216  STORE_FAST               'max_age_set'

 L.1453       218  SETUP_FINALLY       232  'to 232'

 L.1454       220  LOAD_GLOBAL              int
              222  LOAD_FAST                'v'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'v'
              228  POP_BLOCK        
              230  JUMP_FORWARD        274  'to 274'
            232_0  COME_FROM_FINALLY   218  '218'

 L.1455       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   272  'to 272'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L.1456       248  LOAD_GLOBAL              _debug
              250  LOAD_STR                 '   missing or invalid (non-numeric) value for max-age attribute'
              252  CALL_FUNCTION_1       1  ''
              254  POP_TOP          

 L.1458       256  LOAD_CONST               True
              258  STORE_FAST               'bad_cookie'

 L.1459       260  POP_EXCEPT       
              262  POP_TOP          
          264_266  JUMP_ABSOLUTE       370  'to 370'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           238  '238'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           230  '230'

 L.1464       274  LOAD_STR                 'expires'
              276  STORE_FAST               'k'

 L.1465       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _now
              282  LOAD_FAST                'v'
              284  BINARY_ADD       
              286  STORE_FAST               'v'
            288_0  COME_FROM           210  '210'

 L.1466       288  LOAD_FAST                'k'
              290  LOAD_FAST                'value_attrs'
              292  COMPARE_OP               in
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
              298  LOAD_FAST                'k'
              300  LOAD_FAST                'boolean_attrs'
              302  COMPARE_OP               in
          304_306  POP_JUMP_IF_FALSE   360  'to 360'
            308_0  COME_FROM           294  '294'

 L.1467       308  LOAD_FAST                'v'
              310  LOAD_CONST               None
              312  COMPARE_OP               is
          314_316  POP_JUMP_IF_FALSE   350  'to 350'

 L.1468       318  LOAD_FAST                'k'
              320  LOAD_CONST               ('port', 'comment', 'commenturl')
              322  COMPARE_OP               not-in

 L.1467   324_326  POP_JUMP_IF_FALSE   350  'to 350'

 L.1469       328  LOAD_GLOBAL              _debug
              330  LOAD_STR                 '   missing value for %s attribute'
              332  LOAD_FAST                'k'
              334  BINARY_MODULO    
              336  CALL_FUNCTION_1       1  ''
              338  POP_TOP          

 L.1470       340  LOAD_CONST               True
              342  STORE_FAST               'bad_cookie'

 L.1471       344  POP_TOP          
          346_348  JUMP_ABSOLUTE       370  'to 370'
            350_0  COME_FROM           324  '324'
            350_1  COME_FROM           314  '314'

 L.1472       350  LOAD_FAST                'v'
              352  LOAD_FAST                'standard'
              354  LOAD_FAST                'k'
              356  STORE_SUBSCR     
              358  JUMP_BACK            62  'to 62'
            360_0  COME_FROM           304  '304'

 L.1474       360  LOAD_FAST                'v'
              362  LOAD_FAST                'rest'
              364  LOAD_FAST                'k'
              366  STORE_SUBSCR     
              368  JUMP_BACK            62  'to 62'

 L.1476       370  LOAD_FAST                'bad_cookie'
          372_374  POP_JUMP_IF_FALSE   378  'to 378'

 L.1477       376  JUMP_BACK            16  'to 16'
            378_0  COME_FROM           372  '372'

 L.1479       378  LOAD_FAST                'cookie_tuples'
              380  LOAD_METHOD              append
              382  LOAD_FAST                'name'
              384  LOAD_FAST                'value'
              386  LOAD_FAST                'standard'
              388  LOAD_FAST                'rest'
              390  BUILD_TUPLE_4         4 
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
              396  JUMP_BACK            16  'to 16'

 L.1481       398  LOAD_FAST                'cookie_tuples'
              400  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 160_162

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
                else:
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
                else:
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
            else:
                if expires <= self._now:
                    try:
                        self.clear(domain, path, name)
                    except KeyError:
                        pass
                    else:
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

        def make_cookies--- This code section failed: ---

 L.1599         0  LOAD_FAST                'response'
                2  LOAD_METHOD              info
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'headers'

 L.1600         8  LOAD_FAST                'headers'
               10  LOAD_METHOD              get_all
               12  LOAD_STR                 'Set-Cookie2'
               14  BUILD_LIST_0          0 
               16  CALL_METHOD_2         2  ''
               18  STORE_FAST               'rfc2965_hdrs'

 L.1601        20  LOAD_FAST                'headers'
               22  LOAD_METHOD              get_all
               24  LOAD_STR                 'Set-Cookie'
               26  BUILD_LIST_0          0 
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'ns_hdrs'

 L.1602        32  LOAD_GLOBAL              int
               34  LOAD_GLOBAL              time
               36  LOAD_METHOD              time
               38  CALL_METHOD_0         0  ''
               40  CALL_FUNCTION_1       1  ''
               42  DUP_TOP          
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _policy
               48  STORE_ATTR               _now
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _now

 L.1604        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _policy
               58  LOAD_ATTR                rfc2965
               60  STORE_FAST               'rfc2965'

 L.1605        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _policy
               66  LOAD_ATTR                netscape
               68  STORE_FAST               'netscape'

 L.1607        70  LOAD_FAST                'rfc2965_hdrs'
               72  POP_JUMP_IF_TRUE     78  'to 78'
               74  LOAD_FAST                'ns_hdrs'
               76  POP_JUMP_IF_FALSE   102  'to 102'
             78_0  COME_FROM            72  '72'

 L.1608        78  LOAD_FAST                'ns_hdrs'

 L.1607        80  POP_JUMP_IF_TRUE     86  'to 86'

 L.1608        82  LOAD_FAST                'rfc2965'

 L.1607        84  POP_JUMP_IF_FALSE   102  'to 102'
             86_0  COME_FROM            80  '80'

 L.1609        86  LOAD_FAST                'rfc2965_hdrs'

 L.1607        88  POP_JUMP_IF_TRUE     94  'to 94'

 L.1609        90  LOAD_FAST                'netscape'

 L.1607        92  POP_JUMP_IF_FALSE   102  'to 102'
             94_0  COME_FROM            88  '88'

 L.1610        94  LOAD_FAST                'netscape'

 L.1607        96  POP_JUMP_IF_TRUE    106  'to 106'

 L.1610        98  LOAD_FAST                'rfc2965'

 L.1607       100  POP_JUMP_IF_TRUE    106  'to 106'
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            84  '84'
            102_2  COME_FROM            76  '76'

 L.1611       102  BUILD_LIST_0          0 
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'
            106_1  COME_FROM            96  '96'

 L.1613       106  SETUP_FINALLY       128  'to 128'

 L.1614       108  LOAD_FAST                'self'
              110  LOAD_METHOD              _cookies_from_attrs_set

 L.1615       112  LOAD_GLOBAL              split_header_words
              114  LOAD_FAST                'rfc2965_hdrs'
              116  CALL_FUNCTION_1       1  ''

 L.1615       118  LOAD_FAST                'request'

 L.1614       120  CALL_METHOD_2         2  ''
              122  STORE_FAST               'cookies'
              124  POP_BLOCK        
              126  JUMP_FORWARD        158  'to 158'
            128_0  COME_FROM_FINALLY   106  '106'

 L.1616       128  DUP_TOP          
              130  LOAD_GLOBAL              Exception
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   156  'to 156'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.1617       142  LOAD_GLOBAL              _warn_unhandled_exception
              144  CALL_FUNCTION_0       0  ''
              146  POP_TOP          

 L.1618       148  BUILD_LIST_0          0 
              150  STORE_FAST               'cookies'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           134  '134'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           126  '126'

 L.1620       158  LOAD_FAST                'ns_hdrs'
          160_162  POP_JUMP_IF_FALSE   310  'to 310'
              164  LOAD_FAST                'netscape'
          166_168  POP_JUMP_IF_FALSE   310  'to 310'

 L.1621       170  SETUP_FINALLY       192  'to 192'

 L.1623       172  LOAD_FAST                'self'
              174  LOAD_METHOD              _cookies_from_attrs_set

 L.1624       176  LOAD_GLOBAL              parse_ns_headers
              178  LOAD_FAST                'ns_hdrs'
              180  CALL_FUNCTION_1       1  ''

 L.1624       182  LOAD_FAST                'request'

 L.1623       184  CALL_METHOD_2         2  ''
              186  STORE_FAST               'ns_cookies'
              188  POP_BLOCK        
              190  JUMP_FORWARD        222  'to 222'
            192_0  COME_FROM_FINALLY   170  '170'

 L.1625       192  DUP_TOP          
              194  LOAD_GLOBAL              Exception
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   220  'to 220'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L.1626       206  LOAD_GLOBAL              _warn_unhandled_exception
              208  CALL_FUNCTION_0       0  ''
              210  POP_TOP          

 L.1627       212  BUILD_LIST_0          0 
              214  STORE_FAST               'ns_cookies'
              216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           198  '198'
              220  END_FINALLY      
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           190  '190'

 L.1628       222  LOAD_FAST                'self'
              224  LOAD_METHOD              _process_rfc2109_cookies
              226  LOAD_FAST                'ns_cookies'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          

 L.1636       232  LOAD_FAST                'rfc2965'
          234_236  POP_JUMP_IF_FALSE   294  'to 294'

 L.1637       238  BUILD_MAP_0           0 
              240  STORE_FAST               'lookup'

 L.1638       242  LOAD_FAST                'cookies'
              244  GET_ITER         
              246  FOR_ITER            272  'to 272'
              248  STORE_FAST               'cookie'

 L.1639       250  LOAD_CONST               None
              252  LOAD_FAST                'lookup'
              254  LOAD_FAST                'cookie'
              256  LOAD_ATTR                domain
              258  LOAD_FAST                'cookie'
              260  LOAD_ATTR                path
              262  LOAD_FAST                'cookie'
              264  LOAD_ATTR                name
              266  BUILD_TUPLE_3         3 
              268  STORE_SUBSCR     
              270  JUMP_BACK           246  'to 246'

 L.1641       272  LOAD_FAST                'lookup'
              274  BUILD_TUPLE_1         1 
              276  LOAD_CODE                <code_object no_matching_rfc2965>
              278  LOAD_STR                 'CookieJar.make_cookies.<locals>.no_matching_rfc2965'
              280  MAKE_FUNCTION_1          'default'
              282  STORE_FAST               'no_matching_rfc2965'

 L.1644       284  LOAD_GLOBAL              filter
              286  LOAD_FAST                'no_matching_rfc2965'
              288  LOAD_FAST                'ns_cookies'
              290  CALL_FUNCTION_2       2  ''
              292  STORE_FAST               'ns_cookies'
            294_0  COME_FROM           234  '234'

 L.1646       294  LOAD_FAST                'ns_cookies'
          296_298  POP_JUMP_IF_FALSE   310  'to 310'

 L.1647       300  LOAD_FAST                'cookies'
              302  LOAD_METHOD              extend
              304  LOAD_FAST                'ns_cookies'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
            310_0  COME_FROM           296  '296'
            310_1  COME_FROM           166  '166'
            310_2  COME_FROM           160  '160'

 L.1649       310  LOAD_FAST                'cookies'
              312  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 312

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
            if name is not None and not domain is None:
                if path is None:
                    raise ValueError('domain and path must be given to remove a cookie by name')
                del self._cookies[domain][path][name]
            else:
                if path is not None:
                    if domain is None:
                        raise ValueError('domain must be given to remove cookies by path')
                    del self._cookies[domain][path]
                else:
                    if domain is not None:
                        del self._cookies[domain]
                    else:
                        self._cookies = {}

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
            else:
                return i

        def __repr__(self):
            r = []
            for cookie in self:
                r.append(repr(cookie))
            else:
                return '<%s[%s]>' % (self.__class__.__name__, ', '.join(r))

        def __str__(self):
            r = []
            for cookie in self:
                r.append(str(cookie))
            else:
                return '<%s[%s]>' % (self.__class__.__name__, ', '.join(r))


    class LoadError(OSError):
        pass


    class FileCookieJar(CookieJar):
        __doc__ = 'CookieJar that can be loaded from and saved to a file.'

        def __init__(self, filename=None, delayload=False, policy=None):
            """
        Cookies are NOT loaded from the named file until either the .load() or
        .revert() method is called.

        """
            CookieJar.__init__(self, policy)
            if filename is not None:
                filename = os.fspath(filename)
            self.filename = filename
            self.delayload = bool(delayload)

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
            with open(filename) as (f):
                self._really_load(f, filename, ignore_discard, ignore_expires)

        def revert(self, filename=None, ignore_discard=False, ignore_expires=False):
            """Clear all cookies and reload cookies from a saved file.

        Raises LoadError (or OSError) if reversion is not successful; the
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
                except OSError:
                    self._cookies = old_state
                    raise

            finally:
                self._cookies_lock.release()


    def lwp_cookie_str(cookie):
        """Return string representation of Cookie in the LWP cookie file format.

    Actually, the format is extended a bit -- see module docstring.

    """
        h = [
         (
          cookie.name, cookie.value),
         (
          'path', cookie.path),
         (
          'domain', cookie.domain)]
        if cookie.port is not None:
            h.append(('port', cookie.port))
        if cookie.path_specified:
            h.append(('path_spec', None))
        if cookie.port_specified:
            h.append(('port_spec', None))
        if cookie.domain_initial_dot:
            h.append(('domain_dot', None))
        if cookie.secure:
            h.append(('secure', None))
        if cookie.expires:
            h.append(('expires',
             time2isoz(float(cookie.expires))))
        if cookie.discard:
            h.append(('discard', None))
        if cookie.comment:
            h.append(('comment', cookie.comment))
        if cookie.comment_url:
            h.append(('commenturl', cookie.comment_url))
        keys = sorted(cookie._rest.keys())
        for k in keys:
            h.append((k, str(cookie._rest[k])))
        else:
            h.append(('version', str(cookie.version)))
            return join_header_words([h])


    class LWPCookieJar(FileCookieJar):
        __doc__ = '\n    The LWPCookieJar saves a sequence of "Set-Cookie3" lines.\n    "Set-Cookie3" is the format used by the libwww-perl library, not known\n    to be compatible with any browser, but which is easy to read and\n    doesn\'t lose information about RFC 2965 cookies.\n\n    Additional methods\n\n    as_lwp_str(ignore_discard=True, ignore_expired=True)\n\n    '

        def as_lwp_str(self, ignore_discard=True, ignore_expires=True):
            r"""Return cookies as a string of "\n"-separated "Set-Cookie3" headers.

        ignore_discard and ignore_expires: see docstring for FileCookieJar.save

        """
            now = time.time()
            r = []
            for cookie in self:
                if (ignore_discard or cookie).discard:
                    pass
                elif (ignore_expires or cookie.is_expired)(now):
                    pass
                else:
                    r.append('Set-Cookie3: %s' % lwp_cookie_str(cookie))
            else:
                return '\n'.join(r + [''])

        def save(self, filename=None, ignore_discard=False, ignore_expires=False):
            if filename is None:
                if self.filename is not None:
                    filename = self.filename
                else:
                    raise ValueError(MISSING_FILENAME_TEXT)
            with open(filename, 'w') as (f):
                f.write('#LWP-Cookies-2.0\n')
                f.write(self.as_lwp_str(ignore_discard, ignore_expires))

        def _really_load(self, f, filename, ignore_discard, ignore_expires):
            magic = f.readline()
            if not self.magic_re.search(magic):
                msg = '%r does not look like a Set-Cookie3 (LWP) format file' % filename
                raise LoadError(msg)
            now = time.time()
            header = 'Set-Cookie3:'
            boolean_attrs = ('port_spec', 'path_spec', 'domain_dot', 'secure', 'discard')
            value_attrs = ('version', 'port', 'path', 'domain', 'expires', 'comment',
                           'commenturl')
            try:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    if not line.startswith(header):
                        pass
                    else:
                        line = line[len(header):].strip()
                        for data in split_header_words([line]):
                            name, value = data[0]
                            standard = {}
                            rest = {}
                            for k in boolean_attrs:
                                standard[k] = False
                            else:
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
                                else:
                                    h = standard.get
                                    expires = h('expires')
                                    discard = h('discard')
                                    if expires is not None:
                                        expires = iso2time(expires)
                                    if expires is None:
                                        discard = True
                                    domain = h('domain')
                                    domain_specified = domain.startswith('.')
                                    c = Cookie(h('version'), name, value, h('port'), h('port_spec'), domain, domain_specified, h('domain_dot'), h('path'), h('path_spec'), h('secure'), expires, discard, h('comment'), h('commenturl'), rest)

                            if (ignore_discard or c).discard:
                                pass
                            elif (ignore_expires or c.is_expired)(now):
                                pass
                            else:
                                self.set_cookie(c)

            except OSError:
                raise
            except Exception:
                _warn_unhandled_exception()
                raise LoadError('invalid Set-Cookie3 format file %r: %r' % (
                 filename, line))


    class MozillaCookieJar(FileCookieJar):
        __doc__ = "\n\n    WARNING: you may want to backup your browser's cookies file if you use\n    this class to save cookies.  I *think* it works, but there have been\n    bugs in the past!\n\n    This class differs from CookieJar only in the format it uses to save and\n    load cookies to and from a file.  This class uses the Mozilla/Netscape\n    `cookies.txt' format.  lynx uses this file format, too.\n\n    Don't expect cookies saved while the browser is running to be noticed by\n    the browser (in fact, Mozilla on unix will overwrite your saved cookies if\n    you change them on disk while it's running; on Windows, you probably can't\n    save at all while the browser is running).\n\n    Note that the Mozilla/Netscape format will downgrade RFC2965 cookies to\n    Netscape cookies on saving.\n\n    In particular, the cookie version and port number information is lost,\n    together with information about whether or not Path, Port and Discard were\n    specified by the Set-Cookie2 (or Set-Cookie) header, and whether or not the\n    domain as set in the HTTP header started with a dot (yes, I'm aware some\n    domains in Netscape files start with a dot and some don't -- trust me, you\n    really don't want to know any more about this).\n\n    Note that though Mozilla and Netscape use the same format, they use\n    slightly different headers.  The class saves cookies using the Netscape\n    header by default (Mozilla can cope with that).\n\n    "
        magic_re = re.compile('#( Netscape)? HTTP Cookie File')
        header = '# Netscape HTTP Cookie File\n# http://curl.haxx.se/rfc/cookie_spec.html\n# This is a generated file!  Do not edit.\n\n'

        def _really_load(self, f, filename, ignore_discard, ignore_expires):
            now = time.time()
            magic = f.readline()
            if not self.magic_re.search(magic):
                raise LoadError('%r does not look like a Netscape format cookies file' % filename)
            try:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    if line.endswith('\n'):
                        line = line[:-1]
                    if line.strip().startswith(('#', '$')) or line.strip() == '':
                        pass
                    else:
                        domain, domain_specified, path, secure, expires, name, value = line.split('\t')
                        secure = secure == 'TRUE'
                        domain_specified = domain_specified == 'TRUE'
                        if name == '':
                            name = value
                            value = None
                        initial_dot = domain.startswith('.')
                        assert domain_specified == initial_dot
                        discard = False
                        if expires == '':
                            expires = None
                            discard = True
                        c = Cookie(0, name, value, None, False, domain, domain_specified, initial_dot, path, False, secure, expires, discard, None, None, {})
                        if (ignore_discard or c).discard:
                            pass
                        elif (ignore_expires or c.is_expired)(now):
                            pass
                        else:
                            self.set_cookie(c)

            except OSError:
                raise
            except Exception:
                _warn_unhandled_exception()
                raise LoadError('invalid Netscape format cookies file %r: %r' % (
                 filename, line))

        def save(self, filename=None, ignore_discard=False, ignore_expires=False):
            if filename is None:
                if self.filename is not None:
                    filename = self.filename
                else:
                    raise ValueError(MISSING_FILENAME_TEXT)
            with open(filename, 'w') as (f):
                f.write(self.header)
                now = time.time()
                for cookie in self:
                    if (ignore_discard or cookie).discard:
                        pass
                    elif (ignore_expires or cookie.is_expired)(now):
                        pass
                    else:
                        if cookie.secure:
                            secure = 'TRUE'
                        else:
                            secure = 'FALSE'
                        if cookie.domain.startswith('.'):
                            initial_dot = 'TRUE'
                        else:
                            initial_dot = 'FALSE'
                        if cookie.expires is not None:
                            expires = str(cookie.expires)
                        else:
                            expires = ''
                        if cookie.value is None:
                            name = ''
                            value = cookie.name
                        else:
                            name = cookie.name
                            value = cookie.value
                        f.write('\t'.join([cookie.domain, initial_dot, cookie.path,
                         secure, expires, name, value]) + '\n')