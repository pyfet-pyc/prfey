# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\cookiejar.py
import asyncio, datetime, os, pathlib, pickle, re
from collections import defaultdict
from http.cookies import BaseCookie, Morsel, SimpleCookie
from typing import DefaultDict, Dict, Iterable, Iterator, Mapping, Optional, Set, Tuple, Union, cast
from yarl import URL
from .abc import AbstractCookieJar
from .helpers import is_ip_address, next_whole_second
from .typedefs import LooseCookies, PathLike
__all__ = ('CookieJar', 'DummyCookieJar')
CookieItem = Union[(str, 'Morsel[str]')]

class CookieJar(AbstractCookieJar):
    __doc__ = 'Implements cookie storage adhering to RFC 6265.'
    DATE_TOKENS_RE = re.compile('[\\x09\\x20-\\x2F\\x3B-\\x40\\x5B-\\x60\\x7B-\\x7E]*(?P<token>[\\x00-\\x08\\x0A-\\x1F\\d:a-zA-Z\\x7F-\\xFF]+)')
    DATE_HMS_TIME_RE = re.compile('(\\d{1,2}):(\\d{1,2}):(\\d{1,2})')
    DATE_DAY_OF_MONTH_RE = re.compile('(\\d{1,2})')
    DATE_MONTH_RE = re.compile('(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)', re.I)
    DATE_YEAR_RE = re.compile('(\\d{2,4})')
    MAX_TIME = datetime.datetime.max.replace(tzinfo=(datetime.timezone.utc))

    def __init__(self, *, unsafe=False, loop=None):
        super().__init__(loop=loop)
        self._cookies = defaultdict(SimpleCookie)
        self._host_only_cookies = set()
        self._unsafe = unsafe
        self._next_expiration = next_whole_second()
        self._expirations = {}

    def save(self, file_path: PathLike) -> None:
        file_path = pathlib.Path(file_path)
        with file_path.open(mode='wb') as f:
            pickle.dump(self._cookies, f, pickle.HIGHEST_PROTOCOL)

    def load(self, file_path: PathLike) -> None:
        file_path = pathlib.Path(file_path)
        with file_path.open(mode='rb') as f:
            self._cookies = pickle.load(f)

    def clear(self) -> None:
        self._cookies.clear()
        self._host_only_cookies.clear()
        self._next_expiration = next_whole_second()
        self._expirations.clear()

    def __iter__(self) -> 'Iterator[Morsel[str]]':
        self._do_expiration()
        for val in self._cookies.values():
            yield from val.values()

        if False:
            yield None

    def __len__(self) -> int:
        return sum((1 for i in self))

    def _do_expiration(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        if self._next_expiration > now:
            return
        if not self._expirations:
            return
        next_expiration = self.MAX_TIME
        to_del = []
        cookies = self._cookies
        expirations = self._expirations
        for (domain, name), when in expirations.items():
            if when <= now:
                cookies[domain].pop(name, None)
                to_del.append((domain, name))
                self._host_only_cookies.discard((domain, name))
            else:
                next_expiration = min(next_expiration, when)
        else:
            for key in to_del:
                del expirations[key]
            else:
                try:
                    self._next_expiration = next_expiration.replace(microsecond=0) + datetime.timedelta(seconds=1)
                except OverflowError:
                    self._next_expiration = self.MAX_TIME

    def _expire_cookie(self, when: datetime.datetime, domain: str, name: str) -> None:
        self._next_expiration = min(self._next_expiration, when)
        self._expirations[(domain, name)] = when

    def update_cookies(self, cookies: LooseCookies, response_url: URL=URL()) -> None:
        """Update cookies."""
        hostname = response_url.raw_host
        if not self._unsafe:
            if is_ip_address(hostname):
                return
        if isinstance(cookies, Mapping):
            cookies = cookies.items()
        for name, cookie in cookies:
            if not isinstance(cookie, Morsel):
                tmp = SimpleCookie()
                tmp[name] = cookie
                cookie = tmp[name]
            domain = cookie['domain']
            if domain.endswith('.'):
                domain = ''
                del cookie['domain']
            if not domain:
                if hostname is not None:
                    self._host_only_cookies.add((hostname, name))
                    domain = cookie['domain'] = hostname
            if domain.startswith('.'):
                domain = domain[1:]
                cookie['domain'] = domain
            if hostname and not self._is_domain_match(domain, hostname):
                pass
            else:
                path = cookie['path']
                if not (path and path.startswith('/')):
                    path = response_url.path
                    if not path.startswith('/'):
                        path = '/'
                    else:
                        path = '/' + path[1:path.rfind('/')]
                    cookie['path'] = path
                max_age = cookie['max-age']
                if max_age:
                    try:
                        delta_seconds = int(max_age)
                        try:
                            max_age_expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=delta_seconds)
                        except OverflowError:
                            max_age_expiration = self.MAX_TIME
                        else:
                            self._expire_cookie(max_age_expiration, domain, name)
                    except ValueError:
                        cookie['max-age'] = ''

                else:
                    expires = cookie['expires']
                    if expires:
                        expire_time = self._parse_date(expires)
                        if expire_time:
                            self._expire_cookie(expire_time, domain, name)
                        else:
                            cookie['expires'] = ''
                self._cookies[domain][name] = cookie
        else:
            self._do_expiration()

    def filter_cookies--- This code section failed: ---

 L. 200         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _do_expiration
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 201         8  LOAD_GLOBAL              URL
               10  LOAD_FAST                'request_url'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'request_url'

 L. 202        16  LOAD_GLOBAL              SimpleCookie
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'filtered'

 L. 203        22  LOAD_FAST                'request_url'
               24  LOAD_ATTR                raw_host
               26  JUMP_IF_TRUE_OR_POP    30  'to 30'
               28  LOAD_STR                 ''
             30_0  COME_FROM            26  '26'
               30  STORE_FAST               'hostname'

 L. 204        32  LOAD_FAST                'request_url'
               34  LOAD_ATTR                scheme
               36  LOAD_CONST               ('https', 'wss')
               38  COMPARE_OP               not-in
               40  STORE_FAST               'is_not_secure'

 L. 206        42  LOAD_FAST                'self'
               44  GET_ITER         
             46_0  COME_FROM           220  '220'
             46_1  COME_FROM           168  '168'
             46_2  COME_FROM           154  '154'
             46_3  COME_FROM           134  '134'
             46_4  COME_FROM           118  '118'
             46_5  COME_FROM            94  '94'
             46_6  COME_FROM            78  '78'
               46  FOR_ITER            222  'to 222'
               48  STORE_FAST               'cookie'

 L. 207        50  LOAD_FAST                'cookie'
               52  LOAD_ATTR                key
               54  STORE_FAST               'name'

 L. 208        56  LOAD_FAST                'cookie'
               58  LOAD_STR                 'domain'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'domain'

 L. 211        64  LOAD_FAST                'domain'
               66  POP_JUMP_IF_TRUE     80  'to 80'

 L. 212        68  LOAD_FAST                'cookie'
               70  LOAD_ATTR                value
               72  LOAD_FAST                'filtered'
               74  LOAD_FAST                'name'
               76  STORE_SUBSCR     

 L. 213        78  JUMP_BACK            46  'to 46'
             80_0  COME_FROM            66  '66'

 L. 215        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _unsafe
               84  POP_JUMP_IF_TRUE     96  'to 96'
               86  LOAD_GLOBAL              is_ip_address
               88  LOAD_FAST                'hostname'
               90  CALL_FUNCTION_1       1  ''
               92  POP_JUMP_IF_FALSE    96  'to 96'

 L. 216        94  JUMP_BACK            46  'to 46'
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            84  '84'

 L. 218        96  LOAD_FAST                'domain'
               98  LOAD_FAST                'name'
              100  BUILD_TUPLE_2         2 
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _host_only_cookies
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 219       110  LOAD_FAST                'domain'
              112  LOAD_FAST                'hostname'
              114  COMPARE_OP               !=
              116  POP_JUMP_IF_FALSE   136  'to 136'

 L. 220       118  JUMP_BACK            46  'to 46'
              120  BREAK_LOOP          136  'to 136'
            122_0  COME_FROM           108  '108'

 L. 221       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _is_domain_match
              126  LOAD_FAST                'domain'
              128  LOAD_FAST                'hostname'
              130  CALL_METHOD_2         2  ''
              132  POP_JUMP_IF_TRUE    136  'to 136'

 L. 222       134  JUMP_BACK            46  'to 46'
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM           120  '120'
            136_2  COME_FROM           116  '116'

 L. 224       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _is_path_match
              140  LOAD_FAST                'request_url'
              142  LOAD_ATTR                path
              144  LOAD_FAST                'cookie'
              146  LOAD_STR                 'path'
              148  BINARY_SUBSCR    
              150  CALL_METHOD_2         2  ''
              152  POP_JUMP_IF_TRUE    156  'to 156'

 L. 225       154  JUMP_BACK            46  'to 46'
            156_0  COME_FROM           152  '152'

 L. 227       156  LOAD_FAST                'is_not_secure'
              158  POP_JUMP_IF_FALSE   170  'to 170'
              160  LOAD_FAST                'cookie'
              162  LOAD_STR                 'secure'
              164  BINARY_SUBSCR    
              166  POP_JUMP_IF_FALSE   170  'to 170'

 L. 228       168  JUMP_BACK            46  'to 46'
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           158  '158'

 L. 232       170  LOAD_GLOBAL              cast
              172  LOAD_STR                 'Morsel[str]'
              174  LOAD_FAST                'cookie'
              176  LOAD_METHOD              get
              178  LOAD_FAST                'cookie'
              180  LOAD_ATTR                key
              182  LOAD_GLOBAL              Morsel
              184  CALL_FUNCTION_0       0  ''
              186  CALL_METHOD_2         2  ''
              188  CALL_FUNCTION_2       2  ''
              190  STORE_FAST               'mrsl_val'

 L. 233       192  LOAD_FAST                'mrsl_val'
              194  LOAD_METHOD              set
              196  LOAD_FAST                'cookie'
              198  LOAD_ATTR                key
              200  LOAD_FAST                'cookie'
              202  LOAD_ATTR                value
              204  LOAD_FAST                'cookie'
              206  LOAD_ATTR                coded_value
              208  CALL_METHOD_3         3  ''
              210  POP_TOP          

 L. 234       212  LOAD_FAST                'mrsl_val'
              214  LOAD_FAST                'filtered'
              216  LOAD_FAST                'name'
              218  STORE_SUBSCR     
              220  JUMP_BACK            46  'to 46'
            222_0  COME_FROM            46  '46'

 L. 236       222  LOAD_FAST                'filtered'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 222

    @staticmethod
    def _is_domain_match(domain: str, hostname: str) -> bool:
        """Implements domain matching adhering to RFC 6265."""
        if hostname == domain:
            return True
        if not hostname.endswith(domain):
            return False
        non_matching = hostname[:-len(domain)]
        if not non_matching.endswith('.'):
            return False
        return not is_ip_address(hostname)

    @staticmethod
    def _is_path_match(req_path: str, cookie_path: str) -> bool:
        """Implements path matching adhering to RFC 6265."""
        if not req_path.startswith('/'):
            req_path = '/'
        if req_path == cookie_path:
            return True
        if not req_path.startswith(cookie_path):
            return False
        if cookie_path.endswith('/'):
            return True
        non_matching = req_path[len(cookie_path):]
        return non_matching.startswith('/')

    @classmethod
    def _parse_date(cls, date_str: str) -> Optional[datetime.datetime]:
        """Implements date string parsing adhering to RFC 6265."""
        if not date_str:
            return
        found_time = False
        found_day = False
        found_month = False
        found_year = False
        hour = minute = second = 0
        day = 0
        month = 0
        year = 0
        for token_match in cls.DATE_TOKENS_RE.finditer(date_str):
            token = token_match.group('token')
            if not found_time:
                time_match = cls.DATE_HMS_TIME_RE.match(token)
                if time_match:
                    found_time = True
                    hour, minute, second = [int(s) for s in time_match.groups()]
            if not found_day:
                day_match = cls.DATE_DAY_OF_MONTH_RE.match(token)
                if day_match:
                    found_day = True
                    day = int(day_match.group())
            if not found_month:
                month_match = cls.DATE_MONTH_RE.match(token)
                if month_match:
                    found_month = True
                    if not month_match.lastindex is not None:
                        raise AssertionError
                    else:
                        month = month_match.lastindex
            if not found_year:
                year_match = cls.DATE_YEAR_RE.match(token)
                if year_match:
                    found_year = True
                    year = int(year_match.group())
        else:
            if 70 <= year <= 99:
                year += 1900
            elif 0 <= year <= 69:
                year += 2000
            if False in (found_day, found_month, found_year, found_time):
                return
            if not 1 <= day <= 31:
                return
            if not year < 1601:
                if hour > 23 or (minute > 59 or second > 59):
                    return
                return datetime.datetime(year, month, day, hour,
                  minute, second, tzinfo=(datetime.timezone.utc))


class DummyCookieJar(AbstractCookieJar):
    __doc__ = 'Implements a dummy cookie storage.\n\n    It can be used with the ClientSession when no cookie processing is needed.\n\n    '

    def __init__(self, *, loop=None):
        super().__init__(loop=loop)

    def __iter__(self) -> 'Iterator[Morsel[str]]':
        pass
        if False:
            yield None

    def __len__(self) -> int:
        return 0

    def clear(self) -> None:
        pass

    def update_cookies(self, cookies: LooseCookies, response_url: URL=URL()) -> None:
        pass

    def filter_cookies(self, request_url: URL) -> 'BaseCookie[str]':
        return SimpleCookie()