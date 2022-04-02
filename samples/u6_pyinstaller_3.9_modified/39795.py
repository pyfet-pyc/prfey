# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: yarl\_url.py
import functools, sys, warnings
from collections.abc import Mapping, Sequence
from ipaddress import ip_address
from urllib.parse import SplitResult, parse_qsl, urljoin, urlsplit, urlunsplit, quote
from multidict import MultiDict, MultiDictProxy
import idna, math
from ._quoting import _Quoter, _Unquoter
DEFAULT_PORTS = {'http':80, 
 'https':443,  'ws':80,  'wss':443}
sentinel = object()

def rewrite_module(obj: object) -> object:
    obj.__module__ = 'yarl'
    return obj


class cached_property:
    __doc__ = 'Use as a class method decorator.  It operates almost exactly like\n    the Python `@property` decorator, but it puts the result of the\n    method it decorates into the instance dict after the first call,\n    effectively replacing the function it decorates with an instance\n    variable.  It is, in Python parlance, a data descriptor.\n\n    '

    def __init__--- This code section failed: ---

 L.  37         0  LOAD_FAST                'wrapped'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               wrapped

 L.  38         6  SETUP_FINALLY        20  'to 20'

 L.  39         8  LOAD_FAST                'wrapped'
               10  LOAD_ATTR                __doc__
               12  LOAD_FAST                'self'
               14  STORE_ATTR               __doc__
               16  POP_BLOCK        
               18  JUMP_FORWARD         44  'to 44'
             20_0  COME_FROM_FINALLY     6  '6'

 L.  40        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  <121>                42  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  41        32  LOAD_STR                 ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               __doc__
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            18  '18'

 L.  42        44  LOAD_FAST                'wrapped'
               46  LOAD_ATTR                __name__
               48  LOAD_FAST                'self'
               50  STORE_ATTR               name

Parse error at or near `<121>' instruction at offset 24

    def __get__--- This code section failed: ---

 L.  45         0  LOAD_FAST                'inst'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  46         8  LOAD_FAST                'self'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  47        12  LOAD_FAST                'inst'
               14  LOAD_ATTR                _cache
               16  LOAD_METHOD              get
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                name
               22  LOAD_FAST                '_sentinel'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'val'

 L.  48        28  LOAD_FAST                'val'
               30  LOAD_FAST                '_sentinel'
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.  49        36  LOAD_FAST                'val'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.  50        40  LOAD_FAST                'self'
               42  LOAD_METHOD              wrapped
               44  LOAD_FAST                'inst'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'val'

 L.  51        50  LOAD_FAST                'val'
               52  LOAD_FAST                'inst'
               54  LOAD_ATTR                _cache
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                name
               60  STORE_SUBSCR     

 L.  52        62  LOAD_FAST                'val'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __set__(self, inst, value):
        raise AttributeError('cached property is read-only')


@rewrite_module
class URL:
    __slots__ = ('_cache', '_val')
    _QUOTER = _Quoter(requote=False)
    _REQUOTER = _Quoter()
    _PATH_QUOTER = _Quoter(safe='@:', protected='/+', requote=False)
    _PATH_REQUOTER = _Quoter(safe='@:', protected='/+')
    _QUERY_QUOTER = _Quoter(safe='?/:@', protected='=+&;', qs=True, requote=False)
    _QUERY_REQUOTER = _Quoter(safe='?/:@', protected='=+&;', qs=True)
    _QUERY_PART_QUOTER = _Quoter(safe='?/:@', qs=True, requote=False)
    _FRAGMENT_QUOTER = _Quoter(safe='?/:@', requote=False)
    _FRAGMENT_REQUOTER = _Quoter(safe='?/:@')
    _UNQUOTER = _Unquoter()
    _PATH_UNQUOTER = _Unquoter(unsafe='+')
    _QS_UNQUOTER = _Unquoter(qs=True)

    def __new__--- This code section failed: ---

 L. 146         0  LOAD_FAST                'strict'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 147         8  LOAD_GLOBAL              warnings
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'strict parameter is ignored'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          
             18_0  COME_FROM             6  '6'

 L. 148        18  LOAD_GLOBAL              type
               20  LOAD_FAST                'val'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'cls'
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    34  'to 34'

 L. 149        30  LOAD_FAST                'val'
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L. 150        34  LOAD_GLOBAL              type
               36  LOAD_FAST                'val'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_GLOBAL              str
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 151        46  LOAD_GLOBAL              urlsplit
               48  LOAD_FAST                'val'
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'val'
               54  JUMP_FORWARD        114  'to 114'
             56_0  COME_FROM            44  '44'

 L. 152        56  LOAD_GLOBAL              type
               58  LOAD_FAST                'val'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_GLOBAL              SplitResult
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 153        68  LOAD_FAST                'encoded'
               70  POP_JUMP_IF_TRUE    114  'to 114'

 L. 154        72  LOAD_GLOBAL              ValueError
               74  LOAD_STR                 'Cannot apply decoding to SplitResult'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  JUMP_FORWARD        114  'to 114'
             82_0  COME_FROM            66  '66'

 L. 155        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'val'
               86  LOAD_GLOBAL              str
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L. 156        92  LOAD_GLOBAL              urlsplit
               94  LOAD_GLOBAL              str
               96  LOAD_FAST                'val'
               98  CALL_FUNCTION_1       1  ''
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'val'
              104  JUMP_FORWARD        114  'to 114'
            106_0  COME_FROM            90  '90'

 L. 158       106  LOAD_GLOBAL              TypeError
              108  LOAD_STR                 'Constructor parameter should be str'
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'
            114_1  COME_FROM            80  '80'
            114_2  COME_FROM            70  '70'
            114_3  COME_FROM            54  '54'

 L. 160       114  LOAD_FAST                'encoded'
          116_118  POP_JUMP_IF_TRUE    336  'to 336'

 L. 161       120  LOAD_FAST                'val'
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  POP_JUMP_IF_TRUE    138  'to 138'

 L. 162       128  LOAD_STR                 ''
              130  STORE_FAST               'netloc'

 L. 163       132  LOAD_STR                 ''
              134  STORE_FAST               'host'
              136  JUMP_FORWARD        244  'to 244'
            138_0  COME_FROM           126  '126'

 L. 165       138  LOAD_FAST                'val'
              140  LOAD_ATTR                hostname
              142  STORE_FAST               'host'

 L. 166       144  LOAD_FAST                'host'
              146  LOAD_CONST               None
              148  <117>                 0  ''
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 167       152  LOAD_GLOBAL              ValueError
              154  LOAD_STR                 'Invalid URL: host is required for absolute urls'
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           150  '150'

 L. 169       160  SETUP_FINALLY       172  'to 172'

 L. 170       162  LOAD_FAST                'val'
              164  LOAD_ATTR                port
              166  STORE_FAST               'port'
              168  POP_BLOCK        
              170  JUMP_FORWARD        218  'to 218'
            172_0  COME_FROM_FINALLY   160  '160'

 L. 171       172  DUP_TOP          
              174  LOAD_GLOBAL              ValueError
              176  <121>               216  ''
              178  POP_TOP          
              180  STORE_FAST               'e'
              182  POP_TOP          
              184  SETUP_FINALLY       208  'to 208'

 L. 172       186  LOAD_GLOBAL              ValueError

 L. 173       188  LOAD_STR                 "Invalid URL: port can't be converted to integer"

 L. 172       190  CALL_FUNCTION_1       1  ''

 L. 174       192  LOAD_FAST                'e'

 L. 172       194  RAISE_VARARGS_2       2  'exception instance with __cause__'
              196  POP_BLOCK        
              198  POP_EXCEPT       
              200  LOAD_CONST               None
              202  STORE_FAST               'e'
              204  DELETE_FAST              'e'
              206  JUMP_FORWARD        218  'to 218'
            208_0  COME_FROM_FINALLY   184  '184'
              208  LOAD_CONST               None
              210  STORE_FAST               'e'
              212  DELETE_FAST              'e'
              214  <48>             
              216  <48>             
            218_0  COME_FROM           206  '206'
            218_1  COME_FROM           170  '170'

 L. 176       218  LOAD_FAST                'cls'
              220  LOAD_ATTR                _make_netloc

 L. 177       222  LOAD_FAST                'val'
              224  LOAD_ATTR                username
              226  LOAD_FAST                'val'
              228  LOAD_ATTR                password
              230  LOAD_FAST                'host'
              232  LOAD_FAST                'port'
              234  LOAD_CONST               True
              236  LOAD_CONST               True

 L. 176       238  LOAD_CONST               ('encode', 'requote')
              240  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              242  STORE_FAST               'netloc'
            244_0  COME_FROM           136  '136'

 L. 179       244  LOAD_FAST                'cls'
              246  LOAD_METHOD              _PATH_REQUOTER
              248  LOAD_FAST                'val'
              250  LOAD_CONST               2
              252  BINARY_SUBSCR    
              254  CALL_METHOD_1         1  ''
              256  STORE_FAST               'path'

 L. 180       258  LOAD_FAST                'netloc'
          260_262  POP_JUMP_IF_FALSE   274  'to 274'

 L. 181       264  LOAD_FAST                'cls'
              266  LOAD_METHOD              _normalize_path
              268  LOAD_FAST                'path'
              270  CALL_METHOD_1         1  ''
              272  STORE_FAST               'path'
            274_0  COME_FROM           260  '260'

 L. 183       274  LOAD_FAST                'cls'
              276  LOAD_ATTR                _validate_authority_uri_abs_path
              278  LOAD_FAST                'host'
              280  LOAD_FAST                'path'
              282  LOAD_CONST               ('host', 'path')
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  POP_TOP          

 L. 184       288  LOAD_FAST                'cls'
              290  LOAD_METHOD              _QUERY_REQUOTER
              292  LOAD_FAST                'val'
              294  LOAD_CONST               3
              296  BINARY_SUBSCR    
              298  CALL_METHOD_1         1  ''
              300  STORE_FAST               'query'

 L. 185       302  LOAD_FAST                'cls'
              304  LOAD_METHOD              _FRAGMENT_REQUOTER
              306  LOAD_FAST                'val'
              308  LOAD_CONST               4
              310  BINARY_SUBSCR    
              312  CALL_METHOD_1         1  ''
              314  STORE_FAST               'fragment'

 L. 186       316  LOAD_GLOBAL              SplitResult
              318  LOAD_FAST                'val'
              320  LOAD_CONST               0
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'netloc'
              326  LOAD_FAST                'path'
              328  LOAD_FAST                'query'
              330  LOAD_FAST                'fragment'
              332  CALL_FUNCTION_5       5  ''
              334  STORE_FAST               'val'
            336_0  COME_FROM           116  '116'

 L. 188       336  LOAD_GLOBAL              object
              338  LOAD_METHOD              __new__
              340  LOAD_FAST                'cls'
              342  CALL_METHOD_1         1  ''
              344  STORE_FAST               'self'

 L. 189       346  LOAD_FAST                'val'
              348  LOAD_FAST                'self'
              350  STORE_ATTR               _val

 L. 190       352  BUILD_MAP_0           0 
              354  LOAD_FAST                'self'
              356  STORE_ATTR               _cache

 L. 191       358  LOAD_FAST                'self'
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def build--- This code section failed: ---

 L. 211         0  LOAD_FAST                'authority'
                2  POP_JUMP_IF_FALSE    28  'to 28'
                4  LOAD_FAST                'user'
                6  POP_JUMP_IF_TRUE     20  'to 20'
                8  LOAD_FAST                'password'
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_FAST                'host'
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  LOAD_FAST                'port'
               18  POP_JUMP_IF_FALSE    28  'to 28'
             20_0  COME_FROM            14  '14'
             20_1  COME_FROM            10  '10'
             20_2  COME_FROM             6  '6'

 L. 212        20  LOAD_GLOBAL              ValueError

 L. 213        22  LOAD_STR                 'Can\'t mix "authority" with "user", "password", "host" or "port".'

 L. 212        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             2  '2'

 L. 215        28  LOAD_FAST                'port'
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  LOAD_FAST                'host'
               34  POP_JUMP_IF_TRUE     44  'to 44'

 L. 216        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'Can\'t build URL with "port" but without "host".'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            30  '30'

 L. 217        44  LOAD_FAST                'query'
               46  POP_JUMP_IF_FALSE    60  'to 60'
               48  LOAD_FAST                'query_string'
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L. 218        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'Only one of "query" or "query_string" should be passed'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            46  '46'

 L. 220        60  LOAD_FAST                'scheme'
               62  LOAD_CONST               None
               64  <117>                 0  ''

 L. 219        66  POP_JUMP_IF_TRUE    100  'to 100'

 L. 221        68  LOAD_FAST                'authority'
               70  LOAD_CONST               None
               72  <117>                 0  ''

 L. 219        74  POP_JUMP_IF_TRUE    100  'to 100'

 L. 222        76  LOAD_FAST                'path'
               78  LOAD_CONST               None
               80  <117>                 0  ''

 L. 219        82  POP_JUMP_IF_TRUE    100  'to 100'

 L. 223        84  LOAD_FAST                'query_string'
               86  LOAD_CONST               None
               88  <117>                 0  ''

 L. 219        90  POP_JUMP_IF_TRUE    100  'to 100'

 L. 224        92  LOAD_FAST                'fragment'
               94  LOAD_CONST               None
               96  <117>                 0  ''

 L. 219        98  POP_JUMP_IF_FALSE   108  'to 108'
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            82  '82'
            100_2  COME_FROM            74  '74'
            100_3  COME_FROM            66  '66'

 L. 226       100  LOAD_GLOBAL              TypeError

 L. 227       102  LOAD_STR                 'NoneType is illegal for "scheme", "authority", "path", "query_string", and "fragment" args, use empty string instead.'

 L. 226       104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            98  '98'

 L. 231       108  LOAD_FAST                'authority'
              110  POP_JUMP_IF_FALSE   168  'to 168'

 L. 232       112  LOAD_FAST                'encoded'
              114  POP_JUMP_IF_FALSE   122  'to 122'

 L. 233       116  LOAD_FAST                'authority'
              118  STORE_FAST               'netloc'
              120  JUMP_ABSOLUTE       216  'to 216'
            122_0  COME_FROM           114  '114'

 L. 235       122  LOAD_GLOBAL              SplitResult
              124  LOAD_STR                 ''
              126  LOAD_FAST                'authority'
              128  LOAD_STR                 ''
              130  LOAD_STR                 ''
              132  LOAD_STR                 ''
              134  CALL_FUNCTION_5       5  ''
              136  STORE_FAST               'tmp'

 L. 236       138  LOAD_FAST                'cls'
              140  LOAD_ATTR                _make_netloc

 L. 237       142  LOAD_FAST                'tmp'
              144  LOAD_ATTR                username
              146  LOAD_FAST                'tmp'
              148  LOAD_ATTR                password
              150  LOAD_FAST                'tmp'
              152  LOAD_ATTR                hostname
              154  LOAD_FAST                'tmp'
              156  LOAD_ATTR                port
              158  LOAD_CONST               True

 L. 236       160  LOAD_CONST               ('encode',)
              162  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              164  STORE_FAST               'netloc'
              166  JUMP_FORWARD        216  'to 216'
            168_0  COME_FROM           110  '110'

 L. 239       168  LOAD_FAST                'user'
              170  POP_JUMP_IF_TRUE    190  'to 190'
              172  LOAD_FAST                'password'
              174  POP_JUMP_IF_TRUE    190  'to 190'
              176  LOAD_FAST                'host'
              178  POP_JUMP_IF_TRUE    190  'to 190'
              180  LOAD_FAST                'port'
              182  POP_JUMP_IF_TRUE    190  'to 190'

 L. 240       184  LOAD_STR                 ''
              186  STORE_FAST               'netloc'
              188  JUMP_FORWARD        216  'to 216'
            190_0  COME_FROM           182  '182'
            190_1  COME_FROM           178  '178'
            190_2  COME_FROM           174  '174'
            190_3  COME_FROM           170  '170'

 L. 242       190  LOAD_FAST                'cls'
              192  LOAD_ATTR                _make_netloc

 L. 243       194  LOAD_FAST                'user'
              196  LOAD_FAST                'password'
              198  LOAD_FAST                'host'
              200  LOAD_FAST                'port'
              202  LOAD_FAST                'encoded'
              204  UNARY_NOT        
              206  LOAD_FAST                'encoded'
              208  UNARY_NOT        

 L. 242       210  LOAD_CONST               ('encode', 'encode_host')
              212  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              214  STORE_FAST               'netloc'
            216_0  COME_FROM           188  '188'
            216_1  COME_FROM           166  '166'

 L. 245       216  LOAD_FAST                'encoded'
          218_220  POP_JUMP_IF_TRUE    280  'to 280'

 L. 246       222  LOAD_FAST                'cls'
              224  LOAD_METHOD              _PATH_QUOTER
              226  LOAD_FAST                'path'
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'path'

 L. 247       232  LOAD_FAST                'netloc'
              234  POP_JUMP_IF_FALSE   246  'to 246'

 L. 248       236  LOAD_FAST                'cls'
              238  LOAD_METHOD              _normalize_path
              240  LOAD_FAST                'path'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'path'
            246_0  COME_FROM           234  '234'

 L. 250       246  LOAD_FAST                'cls'
              248  LOAD_ATTR                _validate_authority_uri_abs_path
              250  LOAD_FAST                'host'
              252  LOAD_FAST                'path'
              254  LOAD_CONST               ('host', 'path')
              256  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              258  POP_TOP          

 L. 251       260  LOAD_FAST                'cls'
              262  LOAD_METHOD              _QUERY_QUOTER
              264  LOAD_FAST                'query_string'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'query_string'

 L. 252       270  LOAD_FAST                'cls'
              272  LOAD_METHOD              _FRAGMENT_QUOTER
              274  LOAD_FAST                'fragment'
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'fragment'
            280_0  COME_FROM           218  '218'

 L. 254       280  LOAD_FAST                'cls'

 L. 255       282  LOAD_GLOBAL              SplitResult
              284  LOAD_FAST                'scheme'
              286  LOAD_FAST                'netloc'
              288  LOAD_FAST                'path'
              290  LOAD_FAST                'query_string'
              292  LOAD_FAST                'fragment'
              294  CALL_FUNCTION_5       5  ''
              296  LOAD_CONST               True

 L. 254       298  LOAD_CONST               ('encoded',)
              300  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              302  STORE_FAST               'url'

 L. 258       304  LOAD_FAST                'query'
          306_308  POP_JUMP_IF_FALSE   320  'to 320'

 L. 259       310  LOAD_FAST                'url'
              312  LOAD_METHOD              with_query
              314  LOAD_FAST                'query'
              316  CALL_METHOD_1         1  ''
              318  RETURN_VALUE     
            320_0  COME_FROM           306  '306'

 L. 261       320  LOAD_FAST                'url'
              322  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 64

    def __init_subclass__(cls):
        raise TypeError('Inheritance a class {!r} from URL is forbidden'.format(cls))

    def __str__(self):
        val = self._val
        if not val.path:
            if self.is_absolute():
                if val.query or val.fragment:
                    val = val._replace(path='/')
        return urlunsplit(val)

    def __repr__(self):
        return "{}('{}')".formatself.__class__.__name__str(self)

    def __eq__--- This code section failed: ---

 L. 276         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              URL
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 277        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 279        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _val
               20  STORE_FAST               'val1'

 L. 280        22  LOAD_FAST                'val1'
               24  LOAD_ATTR                path
               26  POP_JUMP_IF_TRUE     48  'to 48'
               28  LOAD_FAST                'self'
               30  LOAD_METHOD              is_absolute
               32  CALL_METHOD_0         0  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 281        36  LOAD_FAST                'val1'
               38  LOAD_ATTR                _replace
               40  LOAD_STR                 '/'
               42  LOAD_CONST               ('path',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  STORE_FAST               'val1'
             48_0  COME_FROM            34  '34'
             48_1  COME_FROM            26  '26'

 L. 283        48  LOAD_FAST                'other'
               50  LOAD_ATTR                _val
               52  STORE_FAST               'val2'

 L. 284        54  LOAD_FAST                'val2'
               56  LOAD_ATTR                path
               58  POP_JUMP_IF_TRUE     80  'to 80'
               60  LOAD_FAST                'other'
               62  LOAD_METHOD              is_absolute
               64  CALL_METHOD_0         0  ''
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 285        68  LOAD_FAST                'val2'
               70  LOAD_ATTR                _replace
               72  LOAD_STR                 '/'
               74  LOAD_CONST               ('path',)
               76  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               78  STORE_FAST               'val2'
             80_0  COME_FROM            66  '66'
             80_1  COME_FROM            58  '58'

 L. 287        80  LOAD_FAST                'val1'
               82  LOAD_FAST                'val2'
               84  COMPARE_OP               ==
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __hash__--- This code section failed: ---

 L. 290         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cache
                4  LOAD_METHOD              get
                6  LOAD_STR                 'hash'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'ret'

 L. 291        12  LOAD_FAST                'ret'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    70  'to 70'

 L. 292        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _val
               24  STORE_FAST               'val'

 L. 293        26  LOAD_FAST                'val'
               28  LOAD_ATTR                path
               30  POP_JUMP_IF_TRUE     52  'to 52'
               32  LOAD_FAST                'self'
               34  LOAD_METHOD              is_absolute
               36  CALL_METHOD_0         0  ''
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L. 294        40  LOAD_FAST                'val'
               42  LOAD_ATTR                _replace
               44  LOAD_STR                 '/'
               46  LOAD_CONST               ('path',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  STORE_FAST               'val'
             52_0  COME_FROM            38  '38'
             52_1  COME_FROM            30  '30'

 L. 295        52  LOAD_GLOBAL              hash
               54  LOAD_FAST                'val'
               56  CALL_FUNCTION_1       1  ''
               58  DUP_TOP          
               60  STORE_FAST               'ret'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _cache
               66  LOAD_STR                 'hash'
               68  STORE_SUBSCR     
             70_0  COME_FROM            18  '18'

 L. 296        70  LOAD_FAST                'ret'
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def __le__--- This code section failed: ---

 L. 299         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              URL
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 300        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 301        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _val
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                _val
               24  COMPARE_OP               <=
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __lt__--- This code section failed: ---

 L. 304         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              URL
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 305        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 306        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _val
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                _val
               24  COMPARE_OP               <
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __ge__--- This code section failed: ---

 L. 309         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              URL
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 310        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 311        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _val
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                _val
               24  COMPARE_OP               >=
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __gt__--- This code section failed: ---

 L. 314         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              URL
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 315        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 316        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _val
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                _val
               24  COMPARE_OP               >
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __truediv__(self, name):
        name = self._PATH_QUOTER(name)
        if name.startswith('/'):
            raise ValueError('Appending path {!r} starting from slash is forbidden'.format(name))
        else:
            path = self._val.path
            if path == '/':
                new_path = '/' + name
            else:
                if not path:
                    new_path = self.is_absolute() or name
                else:
                    parts = path.rstrip('/').split('/')
                    parts.append(name)
                    new_path = '/'.join(parts)
        if self.is_absolute():
            new_path = self._normalize_path(new_path)
        return URL(self._val._replace(path=new_path, query='', fragment=''),
          encoded=True)

    def __mod__(self, query):
        return self.update_query(query)

    def __bool__(self) -> bool:
        return bool(self._val.netloc or self._val.path or self._val.query or self._val.fragment)

    def __getstate__(self):
        return (
         self._val,)

    def __setstate__--- This code section failed: ---

 L. 351         0  LOAD_FAST                'state'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    42  'to 42'
               12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'state'
               16  LOAD_CONST               1
               18  BINARY_SUBSCR    
               20  LOAD_GLOBAL              dict
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    42  'to 42'

 L. 353        26  LOAD_FAST                'state'
               28  LOAD_CONST               1
               30  BINARY_SUBSCR    
               32  LOAD_STR                 '_val'
               34  BINARY_SUBSCR    
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _val
               40  JUMP_FORWARD         52  'to 52'
             42_0  COME_FROM            24  '24'
             42_1  COME_FROM            10  '10'

 L. 355        42  LOAD_FAST                'state'
               44  UNPACK_EX_1+0           
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _val
               50  STORE_FAST               'unused'
             52_0  COME_FROM            40  '40'

 L. 356        52  BUILD_MAP_0           0 
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _cache

Parse error at or near `None' instruction at offset -1

    def is_absolute--- This code section failed: ---

 L. 365         0  LOAD_FAST                'self'
                2  LOAD_ATTR                raw_host
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def is_default_port--- This code section failed: ---

 L. 375         0  LOAD_FAST                'self'
                2  LOAD_ATTR                port
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 376        10  LOAD_CONST               False
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 377        14  LOAD_GLOBAL              DEFAULT_PORTS
               16  LOAD_METHOD              get
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                scheme
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'default'

 L. 378        26  LOAD_FAST                'default'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 379        34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 380        38  LOAD_FAST                'self'
               40  LOAD_ATTR                port
               42  LOAD_FAST                'default'
               44  COMPARE_OP               ==
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def origin(self):
        """Return an URL with scheme, host and port parts only.

        user, password, path, query and fragment are removed.

        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute')
        if not self._val.scheme:
            raise ValueError('URL should have scheme')
        v = self._val
        netloc = self._make_netloc(None, None, v.hostname, v.port)
        val = v._replace(netloc=netloc, path='', query='', fragment='')
        return URL(val, encoded=True)

    def relative(self):
        """Return a relative part of the URL.

        scheme, user, password, host and port are removed.

        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute')
        val = self._val._replace(scheme='', netloc='')
        return URL(val, encoded=True)

    @property
    def scheme(self):
        """Scheme for absolute URLs.

        Empty string for relative URLs or URLs starting with //

        """
        return self._val.scheme

    @property
    def raw_authority(self):
        """Encoded authority part of URL.

        Empty string for relative URLs.

        """
        return self._val.netloc

    @cached_property
    def authority(self):
        """Decoded authority part of URL.

        Empty string for relative URLs.

        """
        return self._make_netloc((self.user),
          (self.password), (self.host), (self.port), encode_host=False)

    @property
    def raw_user(self):
        """Encoded user part of URL.

        None if user is missing.

        """
        ret = self._val.username
        if not ret:
            return
        return ret

    @cached_property
    def user(self):
        """Decoded user part of URL.

        None if user is missing.

        """
        return self._UNQUOTER(self.raw_user)

    @property
    def raw_password(self):
        """Encoded password part of URL.

        None if password is missing.

        """
        return self._val.password

    @cached_property
    def password(self):
        """Decoded password part of URL.

        None if password is missing.

        """
        return self._UNQUOTER(self.raw_password)

    @property
    def raw_host(self):
        """Encoded host part of URL.

        None for relative URLs.

        """
        return self._val.hostname

    @cached_property
    def host--- This code section failed: ---

 L. 496         0  LOAD_FAST                'self'
                2  LOAD_ATTR                raw_host
                4  STORE_FAST               'raw'

 L. 497         6  LOAD_FAST                'raw'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 498        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 499        18  LOAD_STR                 '%'
               20  LOAD_FAST                'raw'
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 503        26  LOAD_FAST                'raw'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 504        30  LOAD_GLOBAL              _idna_decode
               32  LOAD_FAST                'raw'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    @property
    def port(self):
        """Port part of URL, with scheme-based fallback.

        None for relative URLs or URLs without explicit port and
        scheme without default port substitution.

        """
        return self._val.port or DEFAULT_PORTS.get(self._val.scheme)

    @property
    def explicit_port(self):
        """Port part of URL, without scheme-based fallback.

        None for relative URLs or URLs without explicit port.

        """
        return self._val.port

    @property
    def raw_path(self):
        """Encoded path of URL.

        / for absolute URLs without path part.

        """
        ret = self._val.path
        if not ret:
            if self.is_absolute():
                ret = '/'
        return ret

    @cached_property
    def path(self):
        """Decoded path of URL.

        / for absolute URLs without path part.

        """
        return self._PATH_UNQUOTER(self.raw_path)

    @cached_property
    def query(self):
        """A MultiDictProxy representing parsed query parameters in decoded
        representation.

        Empty value if URL has no query part.

        """
        ret = MultiDict(parse_qsl((self.raw_query_string), keep_blank_values=True))
        return MultiDictProxy(ret)

    @property
    def raw_query_string(self):
        """Encoded query part of URL.

        Empty string if query is missing.

        """
        return self._val.query

    @cached_property
    def query_string(self):
        """Decoded query part of URL.

        Empty string if query is missing.

        """
        return self._QS_UNQUOTER(self.raw_query_string)

    @cached_property
    def path_qs(self):
        """Decoded path of URL with query."""
        if not self.query_string:
            return self.path
        return '{}?{}'.formatself.pathself.query_string

    @cached_property
    def raw_path_qs(self):
        """Encoded path of URL with query."""
        if not self.raw_query_string:
            return self.raw_path
        return '{}?{}'.formatself.raw_pathself.raw_query_string

    @property
    def raw_fragment(self):
        """Encoded fragment part of URL.

        Empty string if fragment is missing.

        """
        return self._val.fragment

    @cached_property
    def fragment(self):
        """Decoded fragment part of URL.

        Empty string if fragment is missing.

        """
        return self._UNQUOTER(self.raw_fragment)

    @cached_property
    def raw_parts(self):
        """A tuple containing encoded *path* parts.

        ('/',) for absolute URLs if *path* is missing.

        """
        path = self._val.path
        if self.is_absolute():
            if not path:
                parts = [
                 '/']
            else:
                parts = [
                 '/'] + path[1:].split('/')
        elif path.startswith('/'):
            parts = [
             '/'] + path[1:].split('/')
        else:
            parts = path.split('/')
        return tuple(parts)

    @cached_property
    def parts(self):
        """A tuple containing decoded *path* parts.

        ('/',) for absolute URLs if *path* is missing.

        """
        return tuple((self._UNQUOTER(part) for part in self.raw_parts))

    @cached_property
    def parent(self):
        """A new URL with last part of path removed and cleaned up query and
        fragment.

        """
        path = self.raw_path
        if not path or path == '/':
            if self.raw_fragment or self.raw_query_string:
                return URL(self._val._replace(query='', fragment=''), encoded=True)
            return self
        parts = path.split('/')
        val = self._val._replace(path=('/'.join(parts[:-1])), query='', fragment='')
        return URL(val, encoded=True)

    @cached_property
    def raw_name(self):
        """The last part of raw_parts."""
        parts = self.raw_parts
        if self.is_absolute():
            parts = parts[1:]
            if not parts:
                return ''
            return parts[(-1)]
        else:
            return parts[(-1)]

    @cached_property
    def name(self):
        """The last part of parts."""
        return self._UNQUOTER(self.raw_name)

    @staticmethod
    def _validate_authority_uri_abs_path(host, path):
        """Ensure that path in URL with authority starts with a leading slash.

        Raise ValueError if not.
        """
        if len(host) > 0:
            if len(path) > 0:
                if not path.startswith('/'):
                    raise ValueError("Path in a URL with authority should start with a slash ('/') if set")

    @classmethod
    def _normalize_path--- This code section failed: ---

 L. 684         0  LOAD_FAST                'path'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'segments'

 L. 685        10  BUILD_LIST_0          0 
               12  STORE_FAST               'resolved_path'

 L. 687        14  LOAD_FAST                'segments'
               16  GET_ITER         
               18  FOR_ITER             88  'to 88'
               20  STORE_FAST               'seg'

 L. 688        22  LOAD_FAST                'seg'
               24  LOAD_STR                 '..'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    64  'to 64'

 L. 689        30  SETUP_FINALLY        44  'to 44'

 L. 690        32  LOAD_FAST                'resolved_path'
               34  LOAD_METHOD              pop
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_ABSOLUTE        86  'to 86'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 691        44  DUP_TOP          
               46  LOAD_GLOBAL              IndexError
               48  <121>                60  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 695        56  POP_EXCEPT       
               58  JUMP_ABSOLUTE        86  'to 86'
               60  <48>             
               62  JUMP_BACK            18  'to 18'
             64_0  COME_FROM            28  '28'

 L. 696        64  LOAD_FAST                'seg'
               66  LOAD_STR                 '.'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 697        72  CONTINUE             18  'to 18'
               74  JUMP_BACK            18  'to 18'
             76_0  COME_FROM            70  '70'

 L. 699        76  LOAD_FAST                'resolved_path'
               78  LOAD_METHOD              append
               80  LOAD_FAST                'seg'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM_EXCEPT_CLAUSE    58  '58'
               86  JUMP_BACK            18  'to 18'

 L. 701        88  LOAD_FAST                'segments'
               90  LOAD_CONST               -1
               92  BINARY_SUBSCR    
               94  LOAD_CONST               ('.', '..')
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE   110  'to 110'

 L. 705       100  LOAD_FAST                'resolved_path'
              102  LOAD_METHOD              append
              104  LOAD_STR                 ''
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
            110_0  COME_FROM            98  '98'

 L. 707       110  LOAD_STR                 '/'
              112  LOAD_METHOD              join
              114  LOAD_FAST                'resolved_path'
              116  CALL_METHOD_1         1  ''
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 48

    if sys.version_info >= (3, 7):

        @classmethod
        def _encode_host--- This code section failed: ---

 L. 713         0  SETUP_FINALLY        30  'to 30'

 L. 714         2  LOAD_FAST                'host'
                4  LOAD_METHOD              partition
                6  LOAD_STR                 '%'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'ip'
               14  STORE_FAST               'sep'
               16  STORE_FAST               'zone'

 L. 715        18  LOAD_GLOBAL              ip_address
               20  LOAD_FAST                'ip'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'ip'
               26  POP_BLOCK        
               28  JUMP_FORWARD         84  'to 84'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 716        30  DUP_TOP          
               32  LOAD_GLOBAL              ValueError
               34  <121>                82  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 717        42  LOAD_FAST                'host'
               44  LOAD_METHOD              lower
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'host'

 L. 722        50  LOAD_FAST                'human'
               52  POP_JUMP_IF_TRUE     62  'to 62'
               54  LOAD_FAST                'host'
               56  LOAD_METHOD              isascii
               58  CALL_METHOD_0         0  ''
               60  POP_JUMP_IF_FALSE    70  'to 70'
             62_0  COME_FROM            52  '52'

 L. 723        62  LOAD_FAST                'host'
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
             70_0  COME_FROM            60  '60'

 L. 724        70  LOAD_GLOBAL              _idna_encode
               72  LOAD_FAST                'host'
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'host'
               78  POP_EXCEPT       
               80  JUMP_FORWARD        128  'to 128'
               82  <48>             
             84_0  COME_FROM            28  '28'

 L. 726        84  LOAD_FAST                'ip'
               86  LOAD_ATTR                compressed
               88  STORE_FAST               'host'

 L. 727        90  LOAD_FAST                'sep'
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L. 728        94  LOAD_FAST                'host'
               96  LOAD_STR                 '%'
               98  LOAD_FAST                'zone'
              100  BINARY_ADD       
              102  INPLACE_ADD      
              104  STORE_FAST               'host'
            106_0  COME_FROM            92  '92'

 L. 729       106  LOAD_FAST                'ip'
              108  LOAD_ATTR                version
              110  LOAD_CONST               6
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L. 730       116  LOAD_STR                 '['
              118  LOAD_FAST                'host'
              120  BINARY_ADD       
              122  LOAD_STR                 ']'
              124  BINARY_ADD       
              126  STORE_FAST               'host'
            128_0  COME_FROM           114  '114'
            128_1  COME_FROM            80  '80'

 L. 731       128  LOAD_FAST                'host'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    else:

        @classmethod
        def _encode_host--- This code section failed: ---

 L. 737         0  SETUP_FINALLY        30  'to 30'

 L. 738         2  LOAD_FAST                'host'
                4  LOAD_METHOD              partition
                6  LOAD_STR                 '%'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'ip'
               14  STORE_FAST               'sep'
               16  STORE_FAST               'zone'

 L. 739        18  LOAD_GLOBAL              ip_address
               20  LOAD_FAST                'ip'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'ip'
               26  POP_BLOCK        
               28  JUMP_FORWARD        106  'to 106'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 740        30  DUP_TOP          
               32  LOAD_GLOBAL              ValueError
               34  <121>               104  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 741        42  LOAD_FAST                'host'
               44  LOAD_METHOD              lower
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'host'

 L. 742        50  LOAD_FAST                'human'
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 743        54  LOAD_FAST                'host'
               56  ROT_FOUR         
               58  POP_EXCEPT       
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 745        62  LOAD_FAST                'host'
               64  GET_ITER         
             66_0  COME_FROM            76  '76'
               66  FOR_ITER             84  'to 84'
               68  STORE_FAST               'char'

 L. 746        70  LOAD_FAST                'char'
               72  LOAD_STR                 '\x7f'
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE    66  'to 66'

 L. 747        78  POP_TOP          
               80  BREAK_LOOP           92  'to 92'
               82  JUMP_BACK            66  'to 66'

 L. 749        84  LOAD_FAST                'host'
               86  ROT_FOUR         
               88  POP_EXCEPT       
               90  RETURN_VALUE     

 L. 750        92  LOAD_GLOBAL              _idna_encode
               94  LOAD_FAST                'host'
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'host'
              100  POP_EXCEPT       
              102  JUMP_FORWARD        150  'to 150'
              104  <48>             
            106_0  COME_FROM            28  '28'

 L. 752       106  LOAD_FAST                'ip'
              108  LOAD_ATTR                compressed
              110  STORE_FAST               'host'

 L. 753       112  LOAD_FAST                'sep'
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L. 754       116  LOAD_FAST                'host'
              118  LOAD_STR                 '%'
              120  LOAD_FAST                'zone'
              122  BINARY_ADD       
              124  INPLACE_ADD      
              126  STORE_FAST               'host'
            128_0  COME_FROM           114  '114'

 L. 755       128  LOAD_FAST                'ip'
              130  LOAD_ATTR                version
              132  LOAD_CONST               6
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   150  'to 150'

 L. 756       138  LOAD_STR                 '['
              140  LOAD_FAST                'host'
              142  BINARY_ADD       
              144  LOAD_STR                 ']'
              146  BINARY_ADD       
              148  STORE_FAST               'host'
            150_0  COME_FROM           136  '136'
            150_1  COME_FROM           102  '102'

 L. 757       150  LOAD_FAST                'host'
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    @classmethod
    def _make_netloc--- This code section failed: ---

 L. 763         0  LOAD_FAST                'requote'
                2  POP_JUMP_IF_FALSE    10  'to 10'
                4  LOAD_FAST                'cls'
                6  LOAD_ATTR                _REQUOTER
                8  JUMP_FORWARD         14  'to 14'
             10_0  COME_FROM             2  '2'
               10  LOAD_FAST                'cls'
               12  LOAD_ATTR                _QUOTER
             14_0  COME_FROM             8  '8'
               14  STORE_FAST               'quoter'

 L. 764        16  LOAD_FAST                'encode_host'
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 765        20  LOAD_FAST                'cls'
               22  LOAD_METHOD              _encode_host
               24  LOAD_FAST                'host'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'ret'
               30  JUMP_FORWARD         36  'to 36'
             32_0  COME_FROM            18  '18'

 L. 767        32  LOAD_FAST                'host'
               34  STORE_FAST               'ret'
             36_0  COME_FROM            30  '30'

 L. 768        36  LOAD_FAST                'port'
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L. 769        40  LOAD_FAST                'ret'
               42  LOAD_STR                 ':'
               44  BINARY_ADD       
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'port'
               50  CALL_FUNCTION_1       1  ''
               52  BINARY_ADD       
               54  STORE_FAST               'ret'
             56_0  COME_FROM            38  '38'

 L. 770        56  LOAD_FAST                'password'
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE   112  'to 112'

 L. 771        64  LOAD_FAST                'user'
               66  POP_JUMP_IF_TRUE     74  'to 74'

 L. 772        68  LOAD_STR                 ''
               70  STORE_FAST               'user'
               72  JUMP_FORWARD         86  'to 86'
             74_0  COME_FROM            66  '66'

 L. 774        74  LOAD_FAST                'encode'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 775        78  LOAD_FAST                'quoter'
               80  LOAD_FAST                'user'
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'user'
             86_0  COME_FROM            76  '76'
             86_1  COME_FROM            72  '72'

 L. 776        86  LOAD_FAST                'encode'
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 777        90  LOAD_FAST                'quoter'
               92  LOAD_FAST                'password'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'password'
             98_0  COME_FROM            88  '88'

 L. 778        98  LOAD_FAST                'user'
              100  LOAD_STR                 ':'
              102  BINARY_ADD       
              104  LOAD_FAST                'password'
              106  BINARY_ADD       
              108  STORE_FAST               'user'
              110  JUMP_FORWARD        128  'to 128'
            112_0  COME_FROM            62  '62'

 L. 779       112  LOAD_FAST                'user'
              114  POP_JUMP_IF_FALSE   128  'to 128'
              116  LOAD_FAST                'encode'
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 780       120  LOAD_FAST                'quoter'
              122  LOAD_FAST                'user'
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'user'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           114  '114'
            128_2  COME_FROM           110  '110'

 L. 781       128  LOAD_FAST                'user'
              130  POP_JUMP_IF_FALSE   144  'to 144'

 L. 782       132  LOAD_FAST                'user'
              134  LOAD_STR                 '@'
              136  BINARY_ADD       
              138  LOAD_FAST                'ret'
              140  BINARY_ADD       
              142  STORE_FAST               'ret'
            144_0  COME_FROM           130  '130'

 L. 783       144  LOAD_FAST                'ret'
              146  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 60

    def with_scheme(self, scheme):
        """Return a new URL with scheme replaced."""
        if not isinstance(scheme, str):
            raise TypeError('Invalid scheme type')
        if not self.is_absolute():
            raise ValueError('scheme replacement is not allowed for relative URLs')
        return URL(self._val._replace(scheme=(scheme.lower())), encoded=True)

    def with_user--- This code section failed: ---

 L. 803         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _val
                4  STORE_FAST               'val'

 L. 804         6  LOAD_FAST                'user'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L. 805        14  LOAD_CONST               None
               16  STORE_FAST               'password'
               18  JUMP_FORWARD         56  'to 56'
             20_0  COME_FROM            12  '12'

 L. 806        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'user'
               24  LOAD_GLOBAL              str
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    48  'to 48'

 L. 807        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _QUOTER
               34  LOAD_FAST                'user'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'user'

 L. 808        40  LOAD_FAST                'val'
               42  LOAD_ATTR                password
               44  STORE_FAST               'password'
               46  JUMP_FORWARD         56  'to 56'
             48_0  COME_FROM            28  '28'

 L. 810        48  LOAD_GLOBAL              TypeError
               50  LOAD_STR                 'Invalid user type'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            18  '18'

 L. 811        56  LOAD_FAST                'self'
               58  LOAD_METHOD              is_absolute
               60  CALL_METHOD_0         0  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 812        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'user replacement is not allowed for relative URLs'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L. 813        72  LOAD_GLOBAL              URL

 L. 814        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _val
               78  LOAD_ATTR                _replace

 L. 815        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _make_netloc
               84  LOAD_FAST                'user'
               86  LOAD_FAST                'password'
               88  LOAD_FAST                'val'
               90  LOAD_ATTR                hostname
               92  LOAD_FAST                'val'
               94  LOAD_ATTR                port
               96  CALL_METHOD_4         4  ''

 L. 814        98  LOAD_CONST               ('netloc',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 817       102  LOAD_CONST               True

 L. 813       104  LOAD_CONST               ('encoded',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def with_password--- This code section failed: ---

 L. 829         0  LOAD_FAST                'password'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    10  'to 10'

 L. 830         8  JUMP_FORWARD         40  'to 40'
             10_0  COME_FROM             6  '6'

 L. 831        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'password'
               14  LOAD_GLOBAL              str
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 832        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _QUOTER
               24  LOAD_FAST                'password'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'password'
               30  JUMP_FORWARD         40  'to 40'
             32_0  COME_FROM            18  '18'

 L. 834        32  LOAD_GLOBAL              TypeError
               34  LOAD_STR                 'Invalid password type'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM             8  '8'

 L. 835        40  LOAD_FAST                'self'
               42  LOAD_METHOD              is_absolute
               44  CALL_METHOD_0         0  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 836        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'password replacement is not allowed for relative URLs'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

 L. 837        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _val
               60  STORE_FAST               'val'

 L. 838        62  LOAD_GLOBAL              URL

 L. 839        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _val
               68  LOAD_ATTR                _replace

 L. 840        70  LOAD_FAST                'self'
               72  LOAD_METHOD              _make_netloc
               74  LOAD_FAST                'val'
               76  LOAD_ATTR                username
               78  LOAD_FAST                'password'
               80  LOAD_FAST                'val'
               82  LOAD_ATTR                hostname
               84  LOAD_FAST                'val'
               86  LOAD_ATTR                port
               88  CALL_METHOD_4         4  ''

 L. 839        90  LOAD_CONST               ('netloc',)
               92  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 842        94  LOAD_CONST               True

 L. 838        96  LOAD_CONST               ('encoded',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def with_host(self, host):
        """Return a new URL with host replaced.

        Autoencode host if needed.

        Changing host for relative URLs is not allowed, use .join()
        instead.

        """
        if not isinstance(host, str):
            raise TypeError('Invalid host type')
        else:
            if not self.is_absolute():
                raise ValueError('host replacement is not allowed for relative URLs')
            assert host, 'host removing is not allowed'
        val = self._val
        return URL(self._val._replace(netloc=(self._make_netloc(val.username, val.password, host, val.port))),
          encoded=True)

    def with_port--- This code section failed: ---

 L. 876         0  LOAD_FAST                'port'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    36  'to 36'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'port'
               12  LOAD_GLOBAL              int
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     36  'to 36'

 L. 877        18  LOAD_GLOBAL              TypeError
               20  LOAD_STR                 'port should be int or None, got {}'
               22  LOAD_METHOD              format
               24  LOAD_GLOBAL              type
               26  LOAD_FAST                'port'
               28  CALL_FUNCTION_1       1  ''
               30  CALL_METHOD_1         1  ''
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            16  '16'
             36_1  COME_FROM             6  '6'

 L. 878        36  LOAD_FAST                'self'
               38  LOAD_METHOD              is_absolute
               40  CALL_METHOD_0         0  ''
               42  POP_JUMP_IF_TRUE     52  'to 52'

 L. 879        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'port replacement is not allowed for relative URLs'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'

 L. 880        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _val
               56  STORE_FAST               'val'

 L. 881        58  LOAD_GLOBAL              URL

 L. 882        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _val
               64  LOAD_ATTR                _replace

 L. 883        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _make_netloc

 L. 884        70  LOAD_FAST                'val'
               72  LOAD_ATTR                username
               74  LOAD_FAST                'val'
               76  LOAD_ATTR                password
               78  LOAD_FAST                'val'
               80  LOAD_ATTR                hostname
               82  LOAD_FAST                'port'
               84  LOAD_CONST               True

 L. 883        86  LOAD_CONST               ('encode',)
               88  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L. 882        90  LOAD_CONST               ('netloc',)
               92  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 887        94  LOAD_CONST               True

 L. 881        96  LOAD_CONST               ('encoded',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def with_path(self, path, *, encoded=False):
        """Return a new URL with path replaced."""
        if not encoded:
            path = self._PATH_QUOTER(path)
            if self.is_absolute():
                path = self._normalize_path(path)
        elif len(path) > 0 and path[0] != '/':
            path = '/' + path
        return URL(self._val._replace(path=path, query='', fragment=''), encoded=True)

    @classmethod
    def _query_seq_pairs(cls, quoter, pairs):
        for key, val in pairs:
            if isinstance(val, (list, tuple)):
                for v in val:
                    (yield quoter(key) + '=' + quoter(cls._query_var(v)))

            else:
                (yield quoter(key) + '=' + quoter(cls._query_var(val)))

    @staticmethod
    def _query_var--- This code section failed: ---

 L. 911         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'v'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'cls'

 L. 912         8  LOAD_GLOBAL              issubclass
               10  LOAD_FAST                'cls'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 913        18  LOAD_FAST                'v'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 914        22  LOAD_GLOBAL              issubclass
               24  LOAD_FAST                'cls'
               26  LOAD_GLOBAL              float
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    80  'to 80'

 L. 915        32  LOAD_GLOBAL              math
               34  LOAD_METHOD              isinf
               36  LOAD_FAST                'v'
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 916        42  LOAD_GLOBAL              ValueError
               44  LOAD_STR                 "float('inf') is not supported"
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L. 917        50  LOAD_GLOBAL              math
               52  LOAD_METHOD              isnan
               54  LOAD_FAST                'v'
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 918        60  LOAD_GLOBAL              ValueError
               62  LOAD_STR                 "float('nan') is not supported"
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 919        68  LOAD_GLOBAL              str
               70  LOAD_GLOBAL              float
               72  LOAD_FAST                'v'
               74  CALL_FUNCTION_1       1  ''
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            30  '30'

 L. 920        80  LOAD_GLOBAL              issubclass
               82  LOAD_FAST                'cls'
               84  LOAD_GLOBAL              int
               86  CALL_FUNCTION_2       2  ''
               88  POP_JUMP_IF_FALSE   110  'to 110'
               90  LOAD_FAST                'cls'
               92  LOAD_GLOBAL              bool
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 921        98  LOAD_GLOBAL              str
              100  LOAD_GLOBAL              int
              102  LOAD_FAST                'v'
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''
              108  RETURN_VALUE     
            110_0  COME_FROM            96  '96'
            110_1  COME_FROM            88  '88'

 L. 922       110  LOAD_GLOBAL              TypeError

 L. 923       112  LOAD_STR                 'Invalid variable type: value should be str, int or float, got {!r} of type {}'
              114  LOAD_METHOD              format

 L. 925       116  LOAD_FAST                'v'
              118  LOAD_FAST                'cls'

 L. 923       120  CALL_METHOD_2         2  ''

 L. 922       122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 94

    def _get_str_query--- This code section failed: ---

 L. 929         0  LOAD_FAST                'kwargs'
                2  POP_JUMP_IF_FALSE    30  'to 30'

 L. 930         4  LOAD_GLOBAL              len
                6  LOAD_FAST                'args'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_CONST               0
               12  COMPARE_OP               >
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 931        16  LOAD_GLOBAL              ValueError

 L. 932        18  LOAD_STR                 'Either kwargs or single query parameter must be present'

 L. 931        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 934        24  LOAD_FAST                'kwargs'
               26  STORE_FAST               'query'
               28  JUMP_FORWARD         60  'to 60'
             30_0  COME_FROM             2  '2'

 L. 935        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'args'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               1
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 936        42  LOAD_FAST                'args'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  STORE_FAST               'query'
               50  JUMP_FORWARD         60  'to 60'
             52_0  COME_FROM            40  '40'

 L. 938        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'Either kwargs or single query parameter must be present'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            28  '28'

 L. 940        60  LOAD_FAST                'query'
               62  LOAD_CONST               None
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    74  'to 74'

 L. 941        68  LOAD_STR                 ''
               70  STORE_FAST               'query'
               72  JUMP_FORWARD        214  'to 214'
             74_0  COME_FROM            66  '66'

 L. 942        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'query'
               78  LOAD_GLOBAL              Mapping
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE   114  'to 114'

 L. 943        84  LOAD_DEREF               'self'
               86  LOAD_ATTR                _QUERY_PART_QUOTER
               88  STORE_DEREF              'quoter'

 L. 944        90  LOAD_STR                 '&'
               92  LOAD_METHOD              join
               94  LOAD_DEREF               'self'
               96  LOAD_METHOD              _query_seq_pairs
               98  LOAD_DEREF               'quoter'
              100  LOAD_FAST                'query'
              102  LOAD_METHOD              items
              104  CALL_METHOD_0         0  ''
              106  CALL_METHOD_2         2  ''
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'query'
              112  JUMP_FORWARD        214  'to 214'
            114_0  COME_FROM            82  '82'

 L. 945       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'query'
              118  LOAD_GLOBAL              str
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_FALSE   136  'to 136'

 L. 946       124  LOAD_DEREF               'self'
              126  LOAD_METHOD              _QUERY_QUOTER
              128  LOAD_FAST                'query'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'query'
              134  JUMP_FORWARD        214  'to 214'
            136_0  COME_FROM           122  '122'

 L. 947       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'query'
              140  LOAD_GLOBAL              bytes
              142  LOAD_GLOBAL              bytearray
              144  LOAD_GLOBAL              memoryview
              146  BUILD_TUPLE_3         3 
              148  CALL_FUNCTION_2       2  ''
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 948       152  LOAD_GLOBAL              TypeError

 L. 949       154  LOAD_STR                 'Invalid query type: bytes, bytearray and memoryview are forbidden'

 L. 948       156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  JUMP_FORWARD        214  'to 214'
            162_0  COME_FROM           150  '150'

 L. 951       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'query'
              166  LOAD_GLOBAL              Sequence
              168  CALL_FUNCTION_2       2  ''
              170  POP_JUMP_IF_FALSE   206  'to 206'

 L. 952       172  LOAD_DEREF               'self'
              174  LOAD_ATTR                _QUERY_PART_QUOTER
              176  STORE_DEREF              'quoter'

 L. 957       178  LOAD_STR                 '&'
              180  LOAD_METHOD              join
              182  LOAD_CLOSURE             'quoter'
              184  LOAD_CLOSURE             'self'
              186  BUILD_TUPLE_2         2 
              188  LOAD_GENEXPR             '<code_object <genexpr>>'
              190  LOAD_STR                 'URL._get_str_query.<locals>.<genexpr>'
              192  MAKE_FUNCTION_8          'closure'

 L. 958       194  LOAD_FAST                'query'

 L. 957       196  GET_ITER         
              198  CALL_FUNCTION_1       1  ''
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'query'
              204  JUMP_FORWARD        214  'to 214'
            206_0  COME_FROM           170  '170'

 L. 961       206  LOAD_GLOBAL              TypeError

 L. 962       208  LOAD_STR                 'Invalid query type: only str, mapping or sequence of (key, value) pairs is allowed'

 L. 961       210  CALL_FUNCTION_1       1  ''
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           204  '204'
            214_1  COME_FROM           160  '160'
            214_2  COME_FROM           134  '134'
            214_3  COME_FROM           112  '112'
            214_4  COME_FROM            72  '72'

 L. 966       214  LOAD_FAST                'query'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 64

    def with_query--- This code section failed: ---

 L. 983         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _get_str_query
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwargs'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'new_query'

 L. 984        16  LOAD_GLOBAL              URL

 L. 985        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _val
               22  LOAD_ATTR                _replace
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _val
               28  LOAD_ATTR                path
               30  LOAD_FAST                'new_query'
               32  LOAD_CONST               ('path', 'query')
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               36  LOAD_CONST               True

 L. 984        38  LOAD_CONST               ('encoded',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def update_query--- This code section failed: ---

 L. 990         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _get_str_query
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwargs'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               's'

 L. 991        16  LOAD_GLOBAL              MultiDict
               18  LOAD_GLOBAL              parse_qsl
               20  LOAD_FAST                's'
               22  LOAD_CONST               True
               24  LOAD_CONST               ('keep_blank_values',)
               26  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'new_query'

 L. 992        32  LOAD_GLOBAL              MultiDict
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                query
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'query'

 L. 993        42  LOAD_FAST                'query'
               44  LOAD_METHOD              update
               46  LOAD_FAST                'new_query'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 995        52  LOAD_GLOBAL              URL
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _val
               58  LOAD_ATTR                _replace
               60  LOAD_FAST                'self'
               62  LOAD_METHOD              _get_str_query
               64  LOAD_FAST                'query'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               ('query',)
               70  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               72  LOAD_CONST               True
               74  LOAD_CONST               ('encoded',)
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def with_fragment--- This code section failed: ---

 L.1006         0  LOAD_FAST                'fragment'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1007         8  LOAD_STR                 ''
               10  STORE_FAST               'raw_fragment'
               12  JUMP_FORWARD         44  'to 44'
             14_0  COME_FROM             6  '6'

 L.1008        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'fragment'
               18  LOAD_GLOBAL              str
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     34  'to 34'

 L.1009        24  LOAD_GLOBAL              TypeError
               26  LOAD_STR                 'Invalid fragment type'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
               32  JUMP_FORWARD         44  'to 44'
             34_0  COME_FROM            22  '22'

 L.1011        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _FRAGMENT_QUOTER
               38  LOAD_FAST                'fragment'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'raw_fragment'
             44_0  COME_FROM            32  '32'
             44_1  COME_FROM            12  '12'

 L.1012        44  LOAD_FAST                'self'
               46  LOAD_ATTR                raw_fragment
               48  LOAD_FAST                'raw_fragment'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.1013        54  LOAD_FAST                'self'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.1014        58  LOAD_GLOBAL              URL
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _val
               64  LOAD_ATTR                _replace
               66  LOAD_FAST                'raw_fragment'
               68  LOAD_CONST               ('fragment',)
               70  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               72  LOAD_CONST               True
               74  LOAD_CONST               ('encoded',)
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def with_name--- This code section failed: ---

 L.1025         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'name'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.1026        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'Invalid name type'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.1027        18  LOAD_STR                 '/'
               20  LOAD_FAST                'name'
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L.1028        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'Slash in name is not allowed'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L.1029        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _PATH_QUOTER
               38  LOAD_FAST                'name'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'name'

 L.1030        44  LOAD_FAST                'name'
               46  LOAD_CONST               ('.', '..')
               48  <118>                 0  ''
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L.1031        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 '. and .. values are forbidden'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L.1032        60  LOAD_GLOBAL              list
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                raw_parts
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'parts'

 L.1033        70  LOAD_FAST                'self'
               72  LOAD_METHOD              is_absolute
               74  CALL_METHOD_0         0  ''
               76  POP_JUMP_IF_FALSE   120  'to 120'

 L.1034        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'parts'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L.1035        90  LOAD_FAST                'parts'
               92  LOAD_METHOD              append
               94  LOAD_FAST                'name'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_FORWARD        110  'to 110'
            102_0  COME_FROM            88  '88'

 L.1037       102  LOAD_FAST                'name'
              104  LOAD_FAST                'parts'
              106  LOAD_CONST               -1
              108  STORE_SUBSCR     
            110_0  COME_FROM           100  '100'

 L.1038       110  LOAD_STR                 ''
              112  LOAD_FAST                'parts'
              114  LOAD_CONST               0
              116  STORE_SUBSCR     
              118  JUMP_FORWARD        148  'to 148'
            120_0  COME_FROM            76  '76'

 L.1040       120  LOAD_FAST                'name'
              122  LOAD_FAST                'parts'
              124  LOAD_CONST               -1
              126  STORE_SUBSCR     

 L.1041       128  LOAD_FAST                'parts'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  LOAD_STR                 '/'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.1042       140  LOAD_STR                 ''
              142  LOAD_FAST                'parts'
              144  LOAD_CONST               0
              146  STORE_SUBSCR     
            148_0  COME_FROM           138  '138'
            148_1  COME_FROM           118  '118'

 L.1043       148  LOAD_GLOBAL              URL

 L.1044       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _val
              154  LOAD_ATTR                _replace
              156  LOAD_STR                 '/'
              158  LOAD_METHOD              join
              160  LOAD_FAST                'parts'
              162  CALL_METHOD_1         1  ''
              164  LOAD_STR                 ''
              166  LOAD_STR                 ''
              168  LOAD_CONST               ('path', 'query', 'fragment')
              170  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.1045       172  LOAD_CONST               True

 L.1043       174  LOAD_CONST               ('encoded',)
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def join(self, url):
        """Join URLs

        Construct a full (“absolute”) URL by combining a “base URL”
        (self) with another URL (url).

        Informally, this uses components of the base URL, in
        particular the addressing scheme, the network location and
        (part of) the path, to provide missing components in the
        relative URL.

        """
        if not isinstance(url, URL):
            raise TypeError('url should be URL')
        return URL((urljoin(str(self), str(url))), encoded=True)

    def human_repr(self):
        """Return decoded human readable string for URL representation."""
        user = _human_quote(self.user, '#/:?@')
        password = _human_quote(self.password, '#/:?@')
        host = self.host
        if host:
            host = self._encode_host((self.host), human=True)
        path = _human_quote(self.path, '#?')
        query_string = '&'.join(('{}={}'.format_human_quote(k, '#&+;=')_human_quote(v, '#&+;=') for k, v in self.query.items()))
        fragment = _human_quote(self.fragment, '')
        return urlunsplit(SplitResultself.schemeself._make_netloc(user,
          password,
          host,
          (self._val.port),
          encode_host=False)pathquery_stringfragment)


def _human_quote--- This code section failed: ---

 L.1096         0  LOAD_FAST                's'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.1097         4  LOAD_FAST                's'
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.1098         8  LOAD_STR                 '%'
               10  LOAD_FAST                'unsafe'
               12  BINARY_ADD       
               14  GET_ITER         
             16_0  COME_FROM            26  '26'
               16  FOR_ITER             52  'to 52'
               18  STORE_FAST               'c'

 L.1099        20  LOAD_FAST                'c'
               22  LOAD_FAST                's'
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    16  'to 16'

 L.1100        28  LOAD_FAST                's'
               30  LOAD_METHOD              replace
               32  LOAD_FAST                'c'
               34  LOAD_STR                 '%{:02X}'
               36  LOAD_METHOD              format
               38  LOAD_GLOBAL              ord
               40  LOAD_FAST                'c'
               42  CALL_FUNCTION_1       1  ''
               44  CALL_METHOD_1         1  ''
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               's'
               50  JUMP_BACK            16  'to 16'

 L.1101        52  LOAD_FAST                's'
               54  LOAD_METHOD              isprintable
               56  CALL_METHOD_0         0  ''
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L.1102        60  LOAD_FAST                's'
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L.1103        64  LOAD_STR                 ''
               66  LOAD_METHOD              join
               68  LOAD_GENEXPR             '<code_object <genexpr>>'
               70  LOAD_STR                 '_human_quote.<locals>.<genexpr>'
               72  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               74  LOAD_FAST                's'
               76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  CALL_METHOD_1         1  ''
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24


_MAXCACHE = 256

@functools.lru_cache(_MAXCACHE)
def _idna_decode--- This code section failed: ---

 L.1111         0  SETUP_FINALLY        20  'to 20'

 L.1112         2  LOAD_GLOBAL              idna
                4  LOAD_METHOD              decode
                6  LOAD_FAST                'raw'
                8  LOAD_METHOD              encode
               10  LOAD_STR                 'ascii'
               12  CALL_METHOD_1         1  ''
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.1113        20  DUP_TOP          
               22  LOAD_GLOBAL              UnicodeError
               24  <121>                52  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.1114        32  LOAD_FAST                'raw'
               34  LOAD_METHOD              encode
               36  LOAD_STR                 'ascii'
               38  CALL_METHOD_1         1  ''
               40  LOAD_METHOD              decode
               42  LOAD_STR                 'idna'
               44  CALL_METHOD_1         1  ''
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
               52  <48>             

Parse error at or near `<121>' instruction at offset 24


@functools.lru_cache(_MAXCACHE)
def _idna_encode--- This code section failed: ---

 L.1119         0  SETUP_FINALLY        24  'to 24'

 L.1120         2  LOAD_GLOBAL              idna
                4  LOAD_ATTR                encode
                6  LOAD_FAST                'host'
                8  LOAD_CONST               True
               10  LOAD_CONST               ('uts46',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  LOAD_METHOD              decode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.1121        24  DUP_TOP          
               26  LOAD_GLOBAL              UnicodeError
               28  <121>                56  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.1122        36  LOAD_FAST                'host'
               38  LOAD_METHOD              encode
               40  LOAD_STR                 'idna'
               42  CALL_METHOD_1         1  ''
               44  LOAD_METHOD              decode
               46  LOAD_STR                 'ascii'
               48  CALL_METHOD_1         1  ''
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
               56  <48>             

Parse error at or near `<121>' instruction at offset 28


@rewrite_module
def cache_clear():
    global _idna_decode
    global _idna_encode
    _idna_decode.cache_clear()
    _idna_encode.cache_clear()


@rewrite_module
def cache_info():
    return {'idna_encode':_idna_encode.cache_info(), 
     'idna_decode':_idna_decode.cache_info()}


@rewrite_module
def cache_configure(*, idna_encode_size=_MAXCACHE, idna_decode_size=_MAXCACHE):
    global _idna_decode
    global _idna_encode
    _idna_encode = functools.lru_cache(idna_encode_size)(_idna_encode.__wrapped__)
    _idna_decode = functools.lru_cache(idna_decode_size)(_idna_decode.__wrapped__)