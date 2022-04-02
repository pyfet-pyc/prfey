# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
        with file_path.open(mode='wb') as (f):
            pickle.dump(self._cookies, f, pickle.HIGHEST_PROTOCOL)

    def load(self, file_path: PathLike) -> None:
        file_path = pathlib.Path(file_path)
        with file_path.open(mode='rb') as (f):
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
        else:
            return self._expirations or None
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
            else:
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
                if path:
                    if not path.startswith('/'):
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
              120  JUMP_FORWARD        136  'to 136'
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

 L. 236       222  LOAD_FAST                'filtered'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 120

    @staticmethod
    def _is_domain_match(domain: str, hostname: str) -> bool:
        """Implements domain matching adhering to RFC 6265."""
        if hostname == domain:
            return True
        else:
            if not hostname.endswith(domain):
                return False
            non_matching = hostname[:-len(domain)]
            return non_matching.endswith('.') or False
        return not is_ip_address(hostname)

    @staticmethod
    def _is_path_match(req_path: str, cookie_path: str) -> bool:
        """Implements path matching adhering to RFC 6265."""
        if not req_path.startswith('/'):
            req_path = '/'
        else:
            if req_path == cookie_path:
                return True
            return req_path.startswith(cookie_path) or False
        if cookie_path.endswith('/'):
            return True
        non_matching = req_path[len(cookie_path):]
        return non_matching.startswith('/')

    @classmethod
    def _parse_date--- This code section failed: ---

 L. 276         0  LOAD_FAST                'date_str'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 277         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 279         8  LOAD_CONST               False
               10  STORE_FAST               'found_time'

 L. 280        12  LOAD_CONST               False
               14  STORE_FAST               'found_day'

 L. 281        16  LOAD_CONST               False
               18  STORE_FAST               'found_month'

 L. 282        20  LOAD_CONST               False
               22  STORE_FAST               'found_year'

 L. 284        24  LOAD_CONST               0
               26  DUP_TOP          
               28  STORE_FAST               'hour'
               30  DUP_TOP          
               32  STORE_FAST               'minute'
               34  STORE_FAST               'second'

 L. 285        36  LOAD_CONST               0
               38  STORE_FAST               'day'

 L. 286        40  LOAD_CONST               0
               42  STORE_FAST               'month'

 L. 287        44  LOAD_CONST               0
               46  STORE_FAST               'year'

 L. 289        48  LOAD_FAST                'cls'
               50  LOAD_ATTR                DATE_TOKENS_RE
               52  LOAD_METHOD              finditer
               54  LOAD_FAST                'date_str'
               56  CALL_METHOD_1         1  ''
               58  GET_ITER         
             60_0  COME_FROM           226  '226'
             60_1  COME_FROM           210  '210'
               60  FOR_ITER            246  'to 246'
               62  STORE_FAST               'token_match'

 L. 291        64  LOAD_FAST                'token_match'
               66  LOAD_METHOD              group
               68  LOAD_STR                 'token'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'token'

 L. 293        74  LOAD_FAST                'found_time'
               76  POP_JUMP_IF_TRUE    124  'to 124'

 L. 294        78  LOAD_FAST                'cls'
               80  LOAD_ATTR                DATE_HMS_TIME_RE
               82  LOAD_METHOD              match
               84  LOAD_FAST                'token'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'time_match'

 L. 295        90  LOAD_FAST                'time_match'
               92  POP_JUMP_IF_FALSE   124  'to 124'

 L. 296        94  LOAD_CONST               True
               96  STORE_FAST               'found_time'

 L. 297        98  LOAD_LISTCOMP            '<code_object <listcomp>>'
              100  LOAD_STR                 'CookieJar._parse_date.<locals>.<listcomp>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 298       104  LOAD_FAST                'time_match'
              106  LOAD_METHOD              groups
              108  CALL_METHOD_0         0  ''

 L. 297       110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  UNPACK_SEQUENCE_3     3 
              116  STORE_FAST               'hour'
              118  STORE_FAST               'minute'
              120  STORE_FAST               'second'

 L. 299       122  JUMP_BACK            60  'to 60'
            124_0  COME_FROM            92  '92'
            124_1  COME_FROM            76  '76'

 L. 301       124  LOAD_FAST                'found_day'
              126  POP_JUMP_IF_TRUE    162  'to 162'

 L. 302       128  LOAD_FAST                'cls'
              130  LOAD_ATTR                DATE_DAY_OF_MONTH_RE
              132  LOAD_METHOD              match
              134  LOAD_FAST                'token'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'day_match'

 L. 303       140  LOAD_FAST                'day_match'
              142  POP_JUMP_IF_FALSE   162  'to 162'

 L. 304       144  LOAD_CONST               True
              146  STORE_FAST               'found_day'

 L. 305       148  LOAD_GLOBAL              int
              150  LOAD_FAST                'day_match'
              152  LOAD_METHOD              group
              154  CALL_METHOD_0         0  ''
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'day'

 L. 306       160  JUMP_BACK            60  'to 60'
            162_0  COME_FROM           142  '142'
            162_1  COME_FROM           126  '126'

 L. 308       162  LOAD_FAST                'found_month'
              164  POP_JUMP_IF_TRUE    208  'to 208'

 L. 309       166  LOAD_FAST                'cls'
              168  LOAD_ATTR                DATE_MONTH_RE
              170  LOAD_METHOD              match
              172  LOAD_FAST                'token'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'month_match'

 L. 310       178  LOAD_FAST                'month_match'
              180  POP_JUMP_IF_FALSE   208  'to 208'

 L. 311       182  LOAD_CONST               True
              184  STORE_FAST               'found_month'

 L. 312       186  LOAD_FAST                'month_match'
              188  LOAD_ATTR                lastindex
              190  LOAD_CONST               None
              192  COMPARE_OP               is-not
              194  POP_JUMP_IF_TRUE    200  'to 200'
              196  LOAD_ASSERT              AssertionError
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           194  '194'

 L. 313       200  LOAD_FAST                'month_match'
              202  LOAD_ATTR                lastindex
              204  STORE_FAST               'month'

 L. 314       206  JUMP_BACK            60  'to 60'
            208_0  COME_FROM           180  '180'
            208_1  COME_FROM           164  '164'

 L. 316       208  LOAD_FAST                'found_year'
              210  POP_JUMP_IF_TRUE     60  'to 60'

 L. 317       212  LOAD_FAST                'cls'
              214  LOAD_ATTR                DATE_YEAR_RE
              216  LOAD_METHOD              match
              218  LOAD_FAST                'token'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'year_match'

 L. 318       224  LOAD_FAST                'year_match'
              226  POP_JUMP_IF_FALSE    60  'to 60'

 L. 319       228  LOAD_CONST               True
              230  STORE_FAST               'found_year'

 L. 320       232  LOAD_GLOBAL              int
              234  LOAD_FAST                'year_match'
              236  LOAD_METHOD              group
              238  CALL_METHOD_0         0  ''
              240  CALL_FUNCTION_1       1  ''
              242  STORE_FAST               'year'
              244  JUMP_BACK            60  'to 60'

 L. 322       246  LOAD_CONST               70
              248  LOAD_FAST                'year'
              250  DUP_TOP          
              252  ROT_THREE        
              254  COMPARE_OP               <=
          256_258  POP_JUMP_IF_FALSE   270  'to 270'
              260  LOAD_CONST               99
              262  COMPARE_OP               <=
          264_266  POP_JUMP_IF_FALSE   284  'to 284'
              268  JUMP_FORWARD        274  'to 274'
            270_0  COME_FROM           256  '256'
              270  POP_TOP          
              272  JUMP_FORWARD        284  'to 284'
            274_0  COME_FROM           268  '268'

 L. 323       274  LOAD_FAST                'year'
              276  LOAD_CONST               1900
              278  INPLACE_ADD      
              280  STORE_FAST               'year'
              282  JUMP_FORWARD        320  'to 320'
            284_0  COME_FROM           272  '272'
            284_1  COME_FROM           264  '264'

 L. 324       284  LOAD_CONST               0
              286  LOAD_FAST                'year'
              288  DUP_TOP          
              290  ROT_THREE        
              292  COMPARE_OP               <=
          294_296  POP_JUMP_IF_FALSE   308  'to 308'
              298  LOAD_CONST               69
              300  COMPARE_OP               <=
          302_304  POP_JUMP_IF_FALSE   320  'to 320'
              306  JUMP_FORWARD        312  'to 312'
            308_0  COME_FROM           294  '294'
              308  POP_TOP          
              310  JUMP_FORWARD        320  'to 320'
            312_0  COME_FROM           306  '306'

 L. 325       312  LOAD_FAST                'year'
              314  LOAD_CONST               2000
              316  INPLACE_ADD      
              318  STORE_FAST               'year'
            320_0  COME_FROM           310  '310'
            320_1  COME_FROM           302  '302'
            320_2  COME_FROM           282  '282'

 L. 327       320  LOAD_CONST               False
              322  LOAD_FAST                'found_day'
              324  LOAD_FAST                'found_month'
              326  LOAD_FAST                'found_year'
              328  LOAD_FAST                'found_time'
              330  BUILD_TUPLE_4         4 
              332  COMPARE_OP               in
          334_336  POP_JUMP_IF_FALSE   342  'to 342'

 L. 328       338  LOAD_CONST               None
              340  RETURN_VALUE     
            342_0  COME_FROM           334  '334'

 L. 330       342  LOAD_CONST               1
              344  LOAD_FAST                'day'
              346  DUP_TOP          
              348  ROT_THREE        
              350  COMPARE_OP               <=
          352_354  POP_JUMP_IF_FALSE   366  'to 366'
              356  LOAD_CONST               31
              358  COMPARE_OP               <=
          360_362  POP_JUMP_IF_TRUE    372  'to 372'
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           352  '352'
              366  POP_TOP          
            368_0  COME_FROM           364  '364'

 L. 331       368  LOAD_CONST               None
              370  RETURN_VALUE     
            372_0  COME_FROM           360  '360'

 L. 333       372  LOAD_FAST                'year'
              374  LOAD_CONST               1601
              376  COMPARE_OP               <
          378_380  POP_JUMP_IF_TRUE    412  'to 412'
              382  LOAD_FAST                'hour'
              384  LOAD_CONST               23
              386  COMPARE_OP               >
          388_390  POP_JUMP_IF_TRUE    412  'to 412'
              392  LOAD_FAST                'minute'
              394  LOAD_CONST               59
              396  COMPARE_OP               >
          398_400  POP_JUMP_IF_TRUE    412  'to 412'
              402  LOAD_FAST                'second'
              404  LOAD_CONST               59
              406  COMPARE_OP               >
          408_410  POP_JUMP_IF_FALSE   416  'to 416'
            412_0  COME_FROM           398  '398'
            412_1  COME_FROM           388  '388'
            412_2  COME_FROM           378  '378'

 L. 334       412  LOAD_CONST               None
              414  RETURN_VALUE     
            416_0  COME_FROM           408  '408'

 L. 336       416  LOAD_GLOBAL              datetime
              418  LOAD_ATTR                datetime
              420  LOAD_FAST                'year'
              422  LOAD_FAST                'month'
              424  LOAD_FAST                'day'

 L. 337       426  LOAD_FAST                'hour'

 L. 337       428  LOAD_FAST                'minute'

 L. 337       430  LOAD_FAST                'second'

 L. 338       432  LOAD_GLOBAL              datetime
              434  LOAD_ATTR                timezone
              436  LOAD_ATTR                utc

 L. 336       438  LOAD_CONST               ('tzinfo',)
              440  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              442  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 442


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