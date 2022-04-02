# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\cookiejar.py
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
    MAX_32BIT_TIME = datetime.datetime.utcfromtimestamp(2147483647)

    def __init__--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_ATTR                __init__
                6  LOAD_FAST                'loop'
                8  LOAD_CONST               ('loop',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  POP_TOP          

 L.  65        14  LOAD_GLOBAL              defaultdict

 L.  66        16  LOAD_GLOBAL              SimpleCookie

 L.  65        18  CALL_FUNCTION_1       1  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _cookies

 L.  68        24  LOAD_GLOBAL              set
               26  CALL_FUNCTION_0       0  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _host_only_cookies

 L.  69        32  LOAD_FAST                'unsafe'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _unsafe

 L.  70        38  LOAD_FAST                'quote_cookie'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _quote_cookie

 L.  71        44  LOAD_GLOBAL              next_whole_second
               46  CALL_FUNCTION_0       0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _next_expiration

 L.  72        52  BUILD_MAP_0           0 
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _expirations

 L.  74        58  LOAD_FAST                'self'
               60  LOAD_ATTR                MAX_TIME
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _max_time

 L.  75        66  SETUP_FINALLY        82  'to 82'

 L.  76        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _max_time
               72  LOAD_METHOD              timestamp
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  JUMP_FORWARD        108  'to 108'
             82_0  COME_FROM_FINALLY    66  '66'

 L.  77        82  DUP_TOP          
               84  LOAD_GLOBAL              OverflowError
               86  <121>               106  ''
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  78        94  LOAD_FAST                'self'
               96  LOAD_ATTR                MAX_32BIT_TIME
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _max_time
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
              106  <48>             
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            80  '80'

Parse error at or near `<121>' instruction at offset 86

    def save--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              pathlib
                2  LOAD_METHOD              Path
                4  LOAD_FAST                'file_path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'file_path'

 L.  82        10  LOAD_FAST                'file_path'
               12  LOAD_ATTR                open
               14  LOAD_STR                 'wb'
               16  LOAD_CONST               ('mode',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  SETUP_WITH           56  'to 56'
               22  STORE_FAST               'f'

 L.  83        24  LOAD_GLOBAL              pickle
               26  LOAD_METHOD              dump
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _cookies
               32  LOAD_FAST                'f'
               34  LOAD_GLOBAL              pickle
               36  LOAD_ATTR                HIGHEST_PROTOCOL
               38  CALL_METHOD_3         3  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  LOAD_CONST               None
               46  DUP_TOP          
               48  DUP_TOP          
               50  CALL_FUNCTION_3       3  ''
               52  POP_TOP          
               54  JUMP_FORWARD         72  'to 72'
             56_0  COME_FROM_WITH       20  '20'
               56  <49>             
               58  POP_JUMP_IF_TRUE     62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          
               68  POP_EXCEPT       
               70  POP_TOP          
             72_0  COME_FROM            54  '54'

Parse error at or near `DUP_TOP' instruction at offset 46

    def load--- This code section failed: ---

 L.  86         0  LOAD_GLOBAL              pathlib
                2  LOAD_METHOD              Path
                4  LOAD_FAST                'file_path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'file_path'

 L.  87        10  LOAD_FAST                'file_path'
               12  LOAD_ATTR                open
               14  LOAD_STR                 'rb'
               16  LOAD_CONST               ('mode',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  SETUP_WITH           50  'to 50'
               22  STORE_FAST               'f'

 L.  88        24  LOAD_GLOBAL              pickle
               26  LOAD_METHOD              load
               28  LOAD_FAST                'f'
               30  CALL_METHOD_1         1  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _cookies
               36  POP_BLOCK        
               38  LOAD_CONST               None
               40  DUP_TOP          
               42  DUP_TOP          
               44  CALL_FUNCTION_3       3  ''
               46  POP_TOP          
               48  JUMP_FORWARD         66  'to 66'
             50_0  COME_FROM_WITH       20  '20'
               50  <49>             
               52  POP_JUMP_IF_TRUE     56  'to 56'
               54  <48>             
             56_0  COME_FROM            52  '52'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          
               62  POP_EXCEPT       
               64  POP_TOP          
             66_0  COME_FROM            48  '48'

Parse error at or near `DUP_TOP' instruction at offset 40

    def clear(self) -> None:
        self._cookies.clear
        self._host_only_cookies.clear
        self._next_expiration = next_whole_second()
        self._expirations.clear

    def __iter__(self) -> 'Iterator[Morsel[str]]':
        self._do_expiration
        for val in self._cookies.values:
            yield from val.values

        if False:
            yield None

    def __len__(self) -> int:
        return sum((1 for i in self))

    def _do_expiration--- This code section failed: ---

 L. 105         0  LOAD_GLOBAL              datetime
                2  LOAD_ATTR                datetime
                4  LOAD_METHOD              now
                6  LOAD_GLOBAL              datetime
                8  LOAD_ATTR                timezone
               10  LOAD_ATTR                utc
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'now'

 L. 106        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _next_expiration
               20  LOAD_FAST                'now'
               22  COMPARE_OP               >
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 107        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 108        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _expirations
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L. 109        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 110        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _max_time
               44  STORE_FAST               'next_expiration'

 L. 111        46  BUILD_LIST_0          0 
               48  STORE_FAST               'to_del'

 L. 112        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _cookies
               54  STORE_FAST               'cookies'

 L. 113        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _expirations
               60  STORE_FAST               'expirations'

 L. 114        62  LOAD_FAST                'expirations'
               64  LOAD_METHOD              items
               66  CALL_METHOD_0         0  ''
               68  GET_ITER         
               70  FOR_ITER            150  'to 150'
               72  UNPACK_SEQUENCE_2     2 
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'domain'
               78  STORE_FAST               'name'
               80  STORE_FAST               'when'

 L. 115        82  LOAD_FAST                'when'
               84  LOAD_FAST                'now'
               86  COMPARE_OP               <=
               88  POP_JUMP_IF_FALSE   138  'to 138'

 L. 116        90  LOAD_FAST                'cookies'
               92  LOAD_FAST                'domain'
               94  BINARY_SUBSCR    
               96  LOAD_METHOD              pop
               98  LOAD_FAST                'name'
              100  LOAD_CONST               None
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L. 117       106  LOAD_FAST                'to_del'
              108  LOAD_METHOD              append
              110  LOAD_FAST                'domain'
              112  LOAD_FAST                'name'
              114  BUILD_TUPLE_2         2 
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 118       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _host_only_cookies
              124  LOAD_METHOD              discard
              126  LOAD_FAST                'domain'
              128  LOAD_FAST                'name'
              130  BUILD_TUPLE_2         2 
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK            70  'to 70'
            138_0  COME_FROM            88  '88'

 L. 120       138  LOAD_GLOBAL              min
              140  LOAD_FAST                'next_expiration'
              142  LOAD_FAST                'when'
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'next_expiration'
              148  JUMP_BACK            70  'to 70'

 L. 121       150  LOAD_FAST                'to_del'
              152  GET_ITER         
              154  FOR_ITER            166  'to 166'
              156  STORE_FAST               'key'

 L. 122       158  LOAD_FAST                'expirations'
              160  LOAD_FAST                'key'
              162  DELETE_SUBSCR    
              164  JUMP_BACK           154  'to 154'

 L. 124       166  SETUP_FINALLY       198  'to 198'

 L. 125       168  LOAD_FAST                'next_expiration'
              170  LOAD_ATTR                replace

 L. 126       172  LOAD_CONST               0

 L. 125       174  LOAD_CONST               ('microsecond',)
              176  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 127       178  LOAD_GLOBAL              datetime
              180  LOAD_ATTR                timedelta
              182  LOAD_CONST               1
              184  LOAD_CONST               ('seconds',)
              186  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 125       188  BINARY_ADD       
              190  LOAD_FAST                'self'
              192  STORE_ATTR               _next_expiration
              194  POP_BLOCK        
              196  JUMP_FORWARD        224  'to 224'
            198_0  COME_FROM_FINALLY   166  '166'

 L. 128       198  DUP_TOP          
              200  LOAD_GLOBAL              OverflowError
              202  <121>               222  ''
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 129       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _max_time
              214  LOAD_FAST                'self'
              216  STORE_ATTR               _next_expiration
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
              222  <48>             
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           196  '196'

Parse error at or near `<121>' instruction at offset 202

    def _expire_cookie(self, when: datetime.datetime, domain: str, name: str) -> None:
        self._next_expiration = minself._next_expirationwhen
        self._expirations[(domain, name)] = when

    def update_cookies--- This code section failed: ---

 L. 137         0  LOAD_FAST                'response_url'
                2  LOAD_ATTR                raw_host
                4  STORE_FAST               'hostname'

 L. 139         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _unsafe
               10  POP_JUMP_IF_TRUE     24  'to 24'
               12  LOAD_GLOBAL              is_ip_address
               14  LOAD_FAST                'hostname'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 141        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM            10  '10'

 L. 143        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'cookies'
               28  LOAD_GLOBAL              Mapping
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 144        34  LOAD_FAST                'cookies'
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'cookies'
             42_0  COME_FROM            32  '32'

 L. 146        42  LOAD_FAST                'cookies'
               44  GET_ITER         
            46_48  FOR_ITER            482  'to 482'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'name'
               54  STORE_FAST               'cookie'

 L. 147        56  LOAD_GLOBAL              isinstance
               58  LOAD_FAST                'cookie'
               60  LOAD_GLOBAL              Morsel
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_TRUE     88  'to 88'

 L. 148        66  LOAD_GLOBAL              SimpleCookie
               68  CALL_FUNCTION_0       0  ''
               70  STORE_FAST               'tmp'

 L. 149        72  LOAD_FAST                'cookie'
               74  LOAD_FAST                'tmp'
               76  LOAD_FAST                'name'
               78  STORE_SUBSCR     

 L. 150        80  LOAD_FAST                'tmp'
               82  LOAD_FAST                'name'
               84  BINARY_SUBSCR    
               86  STORE_FAST               'cookie'
             88_0  COME_FROM            64  '64'

 L. 152        88  LOAD_FAST                'cookie'
               90  LOAD_STR                 'domain'
               92  BINARY_SUBSCR    
               94  STORE_FAST               'domain'

 L. 155        96  LOAD_FAST                'domain'
               98  LOAD_METHOD              endswith
              100  LOAD_STR                 '.'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L. 156       106  LOAD_STR                 ''
              108  STORE_FAST               'domain'

 L. 157       110  LOAD_FAST                'cookie'
              112  LOAD_STR                 'domain'
              114  DELETE_SUBSCR    
            116_0  COME_FROM           104  '104'

 L. 159       116  LOAD_FAST                'domain'
              118  POP_JUMP_IF_TRUE    156  'to 156'
              120  LOAD_FAST                'hostname'
              122  LOAD_CONST               None
              124  <117>                 1  ''
              126  POP_JUMP_IF_FALSE   156  'to 156'

 L. 162       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _host_only_cookies
              132  LOAD_METHOD              add
              134  LOAD_FAST                'hostname'
              136  LOAD_FAST                'name'
              138  BUILD_TUPLE_2         2 
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L. 163       144  LOAD_FAST                'hostname'
              146  DUP_TOP          
              148  STORE_FAST               'domain'
              150  LOAD_FAST                'cookie'
              152  LOAD_STR                 'domain'
              154  STORE_SUBSCR     
            156_0  COME_FROM           126  '126'
            156_1  COME_FROM           118  '118'

 L. 165       156  LOAD_FAST                'domain'
              158  LOAD_METHOD              startswith
              160  LOAD_STR                 '.'
              162  CALL_METHOD_1         1  ''
              164  POP_JUMP_IF_FALSE   186  'to 186'

 L. 167       166  LOAD_FAST                'domain'
              168  LOAD_CONST               1
              170  LOAD_CONST               None
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  STORE_FAST               'domain'

 L. 168       178  LOAD_FAST                'domain'
              180  LOAD_FAST                'cookie'
              182  LOAD_STR                 'domain'
              184  STORE_SUBSCR     
            186_0  COME_FROM           164  '164'

 L. 170       186  LOAD_FAST                'hostname'
              188  POP_JUMP_IF_FALSE   204  'to 204'
              190  LOAD_FAST                'self'
              192  LOAD_METHOD              _is_domain_match
              194  LOAD_FAST                'domain'
              196  LOAD_FAST                'hostname'
              198  CALL_METHOD_2         2  ''
              200  POP_JUMP_IF_TRUE    204  'to 204'

 L. 172       202  JUMP_BACK            46  'to 46'
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           188  '188'

 L. 174       204  LOAD_FAST                'cookie'
              206  LOAD_STR                 'path'
              208  BINARY_SUBSCR    
              210  STORE_FAST               'path'

 L. 175       212  LOAD_FAST                'path'
              214  POP_JUMP_IF_FALSE   228  'to 228'
              216  LOAD_FAST                'path'
              218  LOAD_METHOD              startswith
              220  LOAD_STR                 '/'
              222  CALL_METHOD_1         1  ''
          224_226  POP_JUMP_IF_TRUE    280  'to 280'
            228_0  COME_FROM           214  '214'

 L. 177       228  LOAD_FAST                'response_url'
              230  LOAD_ATTR                path
              232  STORE_FAST               'path'

 L. 178       234  LOAD_FAST                'path'
              236  LOAD_METHOD              startswith
              238  LOAD_STR                 '/'
              240  CALL_METHOD_1         1  ''
              242  POP_JUMP_IF_TRUE    250  'to 250'

 L. 179       244  LOAD_STR                 '/'
              246  STORE_FAST               'path'
              248  JUMP_FORWARD        272  'to 272'
            250_0  COME_FROM           242  '242'

 L. 182       250  LOAD_STR                 '/'
              252  LOAD_FAST                'path'
              254  LOAD_CONST               1
              256  LOAD_FAST                'path'
              258  LOAD_METHOD              rfind
              260  LOAD_STR                 '/'
              262  CALL_METHOD_1         1  ''
              264  BUILD_SLICE_2         2 
              266  BINARY_SUBSCR    
              268  BINARY_ADD       
              270  STORE_FAST               'path'
            272_0  COME_FROM           248  '248'

 L. 183       272  LOAD_FAST                'path'
              274  LOAD_FAST                'cookie'
              276  LOAD_STR                 'path'
              278  STORE_SUBSCR     
            280_0  COME_FROM           224  '224'

 L. 185       280  LOAD_FAST                'cookie'
              282  LOAD_STR                 'max-age'
              284  BINARY_SUBSCR    
              286  STORE_FAST               'max_age'

 L. 186       288  LOAD_FAST                'max_age'
          290_292  POP_JUMP_IF_FALSE   412  'to 412'

 L. 187       294  SETUP_FINALLY       382  'to 382'

 L. 188       296  LOAD_GLOBAL              int
              298  LOAD_FAST                'max_age'
              300  CALL_FUNCTION_1       1  ''
              302  STORE_FAST               'delta_seconds'

 L. 189       304  SETUP_FINALLY       338  'to 338'

 L. 190       306  LOAD_GLOBAL              datetime
              308  LOAD_ATTR                datetime
              310  LOAD_METHOD              now

 L. 191       312  LOAD_GLOBAL              datetime
              314  LOAD_ATTR                timezone
              316  LOAD_ATTR                utc

 L. 190       318  CALL_METHOD_1         1  ''

 L. 192       320  LOAD_GLOBAL              datetime
              322  LOAD_ATTR                timedelta
              324  LOAD_FAST                'delta_seconds'
              326  LOAD_CONST               ('seconds',)
              328  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 190       330  BINARY_ADD       
              332  STORE_FAST               'max_age_expiration'
              334  POP_BLOCK        
              336  JUMP_FORWARD        364  'to 364'
            338_0  COME_FROM_FINALLY   304  '304'

 L. 193       338  DUP_TOP          
              340  LOAD_GLOBAL              OverflowError
          342_344  <121>               362  ''
              346  POP_TOP          
              348  POP_TOP          
              350  POP_TOP          

 L. 194       352  LOAD_FAST                'self'
              354  LOAD_ATTR                _max_time
              356  STORE_FAST               'max_age_expiration'
              358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
              362  <48>             
            364_0  COME_FROM           360  '360'
            364_1  COME_FROM           336  '336'

 L. 195       364  LOAD_FAST                'self'
              366  LOAD_METHOD              _expire_cookie
              368  LOAD_FAST                'max_age_expiration'
              370  LOAD_FAST                'domain'
              372  LOAD_FAST                'name'
              374  CALL_METHOD_3         3  ''
              376  POP_TOP          
              378  POP_BLOCK        
              380  JUMP_FORWARD        410  'to 410'
            382_0  COME_FROM_FINALLY   294  '294'

 L. 196       382  DUP_TOP          
              384  LOAD_GLOBAL              ValueError
          386_388  <121>               408  ''
              390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L. 197       396  LOAD_STR                 ''
              398  LOAD_FAST                'cookie'
              400  LOAD_STR                 'max-age'
              402  STORE_SUBSCR     
              404  POP_EXCEPT       
              406  JUMP_FORWARD        410  'to 410'
              408  <48>             
            410_0  COME_FROM           406  '406'
            410_1  COME_FROM           380  '380'
              410  JUMP_FORWARD        466  'to 466'
            412_0  COME_FROM           290  '290'

 L. 200       412  LOAD_FAST                'cookie'
              414  LOAD_STR                 'expires'
              416  BINARY_SUBSCR    
              418  STORE_FAST               'expires'

 L. 201       420  LOAD_FAST                'expires'
          422_424  POP_JUMP_IF_FALSE   466  'to 466'

 L. 202       426  LOAD_FAST                'self'
              428  LOAD_METHOD              _parse_date
              430  LOAD_FAST                'expires'
              432  CALL_METHOD_1         1  ''
              434  STORE_FAST               'expire_time'

 L. 203       436  LOAD_FAST                'expire_time'
          438_440  POP_JUMP_IF_FALSE   458  'to 458'

 L. 204       442  LOAD_FAST                'self'
              444  LOAD_METHOD              _expire_cookie
              446  LOAD_FAST                'expire_time'
              448  LOAD_FAST                'domain'
              450  LOAD_FAST                'name'
              452  CALL_METHOD_3         3  ''
              454  POP_TOP          
              456  JUMP_FORWARD        466  'to 466'
            458_0  COME_FROM           438  '438'

 L. 206       458  LOAD_STR                 ''
              460  LOAD_FAST                'cookie'
              462  LOAD_STR                 'expires'
              464  STORE_SUBSCR     
            466_0  COME_FROM           456  '456'
            466_1  COME_FROM           422  '422'
            466_2  COME_FROM           410  '410'

 L. 208       466  LOAD_FAST                'cookie'
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                _cookies
              472  LOAD_FAST                'domain'
              474  BINARY_SUBSCR    
              476  LOAD_FAST                'name'
              478  STORE_SUBSCR     
              480  JUMP_BACK            46  'to 46'

 L. 210       482  LOAD_FAST                'self'
              484  LOAD_METHOD              _do_expiration
              486  CALL_METHOD_0         0  ''
              488  POP_TOP          

Parse error at or near `<117>' instruction at offset 124

    def filter_cookies--- This code section failed: ---

 L. 216         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _do_expiration
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 217         8  LOAD_GLOBAL              URL
               10  LOAD_FAST                'request_url'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'request_url'

 L. 219        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _quote_cookie
               20  POP_JUMP_IF_FALSE    28  'to 28'
               22  LOAD_GLOBAL              SimpleCookie
               24  CALL_FUNCTION_0       0  ''
               26  JUMP_FORWARD         32  'to 32'
             28_0  COME_FROM            20  '20'
               28  LOAD_GLOBAL              BaseCookie
               30  CALL_FUNCTION_0       0  ''
             32_0  COME_FROM            26  '26'

 L. 218        32  STORE_FAST               'filtered'

 L. 221        34  LOAD_FAST                'request_url'
               36  LOAD_ATTR                raw_host
               38  JUMP_IF_TRUE_OR_POP    42  'to 42'
               40  LOAD_STR                 ''
             42_0  COME_FROM            38  '38'
               42  STORE_FAST               'hostname'

 L. 222        44  LOAD_FAST                'request_url'
               46  LOAD_ATTR                scheme
               48  LOAD_CONST               ('https', 'wss')
               50  <118>                 1  ''
               52  STORE_FAST               'is_not_secure'

 L. 224        54  LOAD_FAST                'self'
               56  GET_ITER         
               58  FOR_ITER            234  'to 234'
               60  STORE_FAST               'cookie'

 L. 225        62  LOAD_FAST                'cookie'
               64  LOAD_ATTR                key
               66  STORE_FAST               'name'

 L. 226        68  LOAD_FAST                'cookie'
               70  LOAD_STR                 'domain'
               72  BINARY_SUBSCR    
               74  STORE_FAST               'domain'

 L. 229        76  LOAD_FAST                'domain'
               78  POP_JUMP_IF_TRUE     92  'to 92'

 L. 230        80  LOAD_FAST                'cookie'
               82  LOAD_ATTR                value
               84  LOAD_FAST                'filtered'
               86  LOAD_FAST                'name'
               88  STORE_SUBSCR     

 L. 231        90  JUMP_BACK            58  'to 58'
             92_0  COME_FROM            78  '78'

 L. 233        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _unsafe
               96  POP_JUMP_IF_TRUE    108  'to 108'
               98  LOAD_GLOBAL              is_ip_address
              100  LOAD_FAST                'hostname'
              102  CALL_FUNCTION_1       1  ''
              104  POP_JUMP_IF_FALSE   108  'to 108'

 L. 234       106  JUMP_BACK            58  'to 58'
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            96  '96'

 L. 236       108  LOAD_FAST                'domain'
              110  LOAD_FAST                'name'
              112  BUILD_TUPLE_2         2 
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _host_only_cookies
              118  <118>                 0  ''
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L. 237       122  LOAD_FAST                'domain'
              124  LOAD_FAST                'hostname'
              126  COMPARE_OP               !=
              128  POP_JUMP_IF_FALSE   148  'to 148'

 L. 238       130  JUMP_BACK            58  'to 58'
              132  JUMP_FORWARD        148  'to 148'
            134_0  COME_FROM           120  '120'

 L. 239       134  LOAD_FAST                'self'
              136  LOAD_METHOD              _is_domain_match
              138  LOAD_FAST                'domain'
              140  LOAD_FAST                'hostname'
              142  CALL_METHOD_2         2  ''
              144  POP_JUMP_IF_TRUE    148  'to 148'

 L. 240       146  JUMP_BACK            58  'to 58'
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           132  '132'
            148_2  COME_FROM           128  '128'

 L. 242       148  LOAD_FAST                'self'
              150  LOAD_METHOD              _is_path_match
              152  LOAD_FAST                'request_url'
              154  LOAD_ATTR                path
              156  LOAD_FAST                'cookie'
              158  LOAD_STR                 'path'
              160  BINARY_SUBSCR    
              162  CALL_METHOD_2         2  ''
              164  POP_JUMP_IF_TRUE    168  'to 168'

 L. 243       166  JUMP_BACK            58  'to 58'
            168_0  COME_FROM           164  '164'

 L. 245       168  LOAD_FAST                'is_not_secure'
              170  POP_JUMP_IF_FALSE   182  'to 182'
              172  LOAD_FAST                'cookie'
              174  LOAD_STR                 'secure'
              176  BINARY_SUBSCR    
              178  POP_JUMP_IF_FALSE   182  'to 182'

 L. 246       180  JUMP_BACK            58  'to 58'
            182_0  COME_FROM           178  '178'
            182_1  COME_FROM           170  '170'

 L. 250       182  LOAD_GLOBAL              cast
              184  LOAD_STR                 'Morsel[str]'
              186  LOAD_FAST                'cookie'
              188  LOAD_METHOD              get
              190  LOAD_FAST                'cookie'
              192  LOAD_ATTR                key
              194  LOAD_GLOBAL              Morsel
              196  CALL_FUNCTION_0       0  ''
              198  CALL_METHOD_2         2  ''
              200  CALL_FUNCTION_2       2  ''
              202  STORE_FAST               'mrsl_val'

 L. 251       204  LOAD_FAST                'mrsl_val'
              206  LOAD_METHOD              set
              208  LOAD_FAST                'cookie'
              210  LOAD_ATTR                key
              212  LOAD_FAST                'cookie'
              214  LOAD_ATTR                value
              216  LOAD_FAST                'cookie'
              218  LOAD_ATTR                coded_value
              220  CALL_METHOD_3         3  ''
              222  POP_TOP          

 L. 252       224  LOAD_FAST                'mrsl_val'
              226  LOAD_FAST                'filtered'
              228  LOAD_FAST                'name'
              230  STORE_SUBSCR     
              232  JUMP_BACK            58  'to 58'

 L. 254       234  LOAD_FAST                'filtered'
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 50

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

 L. 294         0  LOAD_FAST                'date_str'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 295         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 297         8  LOAD_CONST               False
               10  STORE_FAST               'found_time'

 L. 298        12  LOAD_CONST               False
               14  STORE_FAST               'found_day'

 L. 299        16  LOAD_CONST               False
               18  STORE_FAST               'found_month'

 L. 300        20  LOAD_CONST               False
               22  STORE_FAST               'found_year'

 L. 302        24  LOAD_CONST               0
               26  DUP_TOP          
               28  STORE_FAST               'hour'
               30  DUP_TOP          
               32  STORE_FAST               'minute'
               34  STORE_FAST               'second'

 L. 303        36  LOAD_CONST               0
               38  STORE_FAST               'day'

 L. 304        40  LOAD_CONST               0
               42  STORE_FAST               'month'

 L. 305        44  LOAD_CONST               0
               46  STORE_FAST               'year'

 L. 307        48  LOAD_FAST                'cls'
               50  LOAD_ATTR                DATE_TOKENS_RE
               52  LOAD_METHOD              finditer
               54  LOAD_FAST                'date_str'
               56  CALL_METHOD_1         1  ''
               58  GET_ITER         
             60_0  COME_FROM           226  '226'
             60_1  COME_FROM           210  '210'
               60  FOR_ITER            246  'to 246'
               62  STORE_FAST               'token_match'

 L. 309        64  LOAD_FAST                'token_match'
               66  LOAD_METHOD              group
               68  LOAD_STR                 'token'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'token'

 L. 311        74  LOAD_FAST                'found_time'
               76  POP_JUMP_IF_TRUE    124  'to 124'

 L. 312        78  LOAD_FAST                'cls'
               80  LOAD_ATTR                DATE_HMS_TIME_RE
               82  LOAD_METHOD              match
               84  LOAD_FAST                'token'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'time_match'

 L. 313        90  LOAD_FAST                'time_match'
               92  POP_JUMP_IF_FALSE   124  'to 124'

 L. 314        94  LOAD_CONST               True
               96  STORE_FAST               'found_time'

 L. 315        98  LOAD_LISTCOMP            '<code_object <listcomp>>'
              100  LOAD_STR                 'CookieJar._parse_date.<locals>.<listcomp>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              104  LOAD_FAST                'time_match'
              106  LOAD_METHOD              groups
              108  CALL_METHOD_0         0  ''
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  UNPACK_SEQUENCE_3     3 
              116  STORE_FAST               'hour'
              118  STORE_FAST               'minute'
              120  STORE_FAST               'second'

 L. 316       122  JUMP_BACK            60  'to 60'
            124_0  COME_FROM            92  '92'
            124_1  COME_FROM            76  '76'

 L. 318       124  LOAD_FAST                'found_day'
              126  POP_JUMP_IF_TRUE    162  'to 162'

 L. 319       128  LOAD_FAST                'cls'
              130  LOAD_ATTR                DATE_DAY_OF_MONTH_RE
              132  LOAD_METHOD              match
              134  LOAD_FAST                'token'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'day_match'

 L. 320       140  LOAD_FAST                'day_match'
              142  POP_JUMP_IF_FALSE   162  'to 162'

 L. 321       144  LOAD_CONST               True
              146  STORE_FAST               'found_day'

 L. 322       148  LOAD_GLOBAL              int
              150  LOAD_FAST                'day_match'
              152  LOAD_METHOD              group
              154  CALL_METHOD_0         0  ''
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'day'

 L. 323       160  JUMP_BACK            60  'to 60'
            162_0  COME_FROM           142  '142'
            162_1  COME_FROM           126  '126'

 L. 325       162  LOAD_FAST                'found_month'
              164  POP_JUMP_IF_TRUE    208  'to 208'

 L. 326       166  LOAD_FAST                'cls'
              168  LOAD_ATTR                DATE_MONTH_RE
              170  LOAD_METHOD              match
              172  LOAD_FAST                'token'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'month_match'

 L. 327       178  LOAD_FAST                'month_match'
              180  POP_JUMP_IF_FALSE   208  'to 208'

 L. 328       182  LOAD_CONST               True
              184  STORE_FAST               'found_month'

 L. 329       186  LOAD_FAST                'month_match'
              188  LOAD_ATTR                lastindex
              190  LOAD_CONST               None
              192  <117>                 1  ''
              194  POP_JUMP_IF_TRUE    200  'to 200'
              196  <74>             
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           194  '194'

 L. 330       200  LOAD_FAST                'month_match'
              202  LOAD_ATTR                lastindex
              204  STORE_FAST               'month'

 L. 331       206  JUMP_BACK            60  'to 60'
            208_0  COME_FROM           180  '180'
            208_1  COME_FROM           164  '164'

 L. 333       208  LOAD_FAST                'found_year'
              210  POP_JUMP_IF_TRUE     60  'to 60'

 L. 334       212  LOAD_FAST                'cls'
              214  LOAD_ATTR                DATE_YEAR_RE
              216  LOAD_METHOD              match
              218  LOAD_FAST                'token'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'year_match'

 L. 335       224  LOAD_FAST                'year_match'
              226  POP_JUMP_IF_FALSE    60  'to 60'

 L. 336       228  LOAD_CONST               True
              230  STORE_FAST               'found_year'

 L. 337       232  LOAD_GLOBAL              int
              234  LOAD_FAST                'year_match'
              236  LOAD_METHOD              group
              238  CALL_METHOD_0         0  ''
              240  CALL_FUNCTION_1       1  ''
              242  STORE_FAST               'year'
              244  JUMP_BACK            60  'to 60'

 L. 339       246  LOAD_CONST               70
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

 L. 340       274  LOAD_FAST                'year'
              276  LOAD_CONST               1900
              278  INPLACE_ADD      
              280  STORE_FAST               'year'
              282  JUMP_FORWARD        320  'to 320'
            284_0  COME_FROM           272  '272'
            284_1  COME_FROM           264  '264'

 L. 341       284  LOAD_CONST               0
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

 L. 342       312  LOAD_FAST                'year'
              314  LOAD_CONST               2000
              316  INPLACE_ADD      
              318  STORE_FAST               'year'
            320_0  COME_FROM           310  '310'
            320_1  COME_FROM           302  '302'
            320_2  COME_FROM           282  '282'

 L. 344       320  LOAD_CONST               False
              322  LOAD_FAST                'found_day'
              324  LOAD_FAST                'found_month'
              326  LOAD_FAST                'found_year'
              328  LOAD_FAST                'found_time'
              330  BUILD_TUPLE_4         4 
              332  <118>                 0  ''
          334_336  POP_JUMP_IF_FALSE   342  'to 342'

 L. 345       338  LOAD_CONST               None
              340  RETURN_VALUE     
            342_0  COME_FROM           334  '334'

 L. 347       342  LOAD_CONST               1
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

 L. 348       368  LOAD_CONST               None
              370  RETURN_VALUE     
            372_0  COME_FROM           360  '360'

 L. 350       372  LOAD_FAST                'year'
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

 L. 351       412  LOAD_CONST               None
              414  RETURN_VALUE     
            416_0  COME_FROM           408  '408'

 L. 353       416  LOAD_GLOBAL              datetime
              418  LOAD_ATTR                datetime

 L. 354       420  LOAD_FAST                'year'
              422  LOAD_FAST                'month'
              424  LOAD_FAST                'day'
              426  LOAD_FAST                'hour'
              428  LOAD_FAST                'minute'
              430  LOAD_FAST                'second'
              432  LOAD_GLOBAL              datetime
              434  LOAD_ATTR                timezone
              436  LOAD_ATTR                utc

 L. 353       438  LOAD_CONST               ('tzinfo',)
              440  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              442  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 192


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