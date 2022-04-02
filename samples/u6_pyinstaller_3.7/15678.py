# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\extractor\common.py
"""Common classes and constants used by extractor modules."""
import re, time, netrc, queue, logging, datetime, requests, threading
from .message import Message
from .. import config, text, util, exception, cloudflare

class Extractor:
    category = ''
    subcategory = ''
    basecategory = ''
    categorytransfer = False
    directory_fmt = ('{category}', )
    filename_fmt = '{filename}.{extension}'
    archive_fmt = ''
    cookiedomain = ''
    root = ''
    test = None
    request_interval = 0.0
    request_interval_min = 0.0
    request_timestamp = 0.0

    def __init__(self, match):
        self.session = requests.Session()
        self.log = logging.getLogger(self.category)
        self.url = match.string
        self._cookiefile = None
        self._cookiejar = self.session.cookies
        self._parentdir = ''
        self._cfgpath = (
         'extractor', self.category, self.subcategory)
        self._write_pages = self.config('write-pages', False)
        self._retries = self.config('retries', 4)
        self._timeout = self.config('timeout', 30)
        self._verify = self.config('verify', True)
        self.request_interval = self.config('sleep-request', self.request_interval)
        if self._retries < 0:
            self._retries = float('inf')
        if self.request_interval < self.request_interval_min:
            self.request_interval = self.request_interval_min
        if self.basecategory:
            self.config = self._config_shared
            self.config_accumulate = self._config_shared_accumulate
        self._init_headers()
        self._init_cookies()
        self._init_proxies()

    @classmethod
    def from_url(cls, url):
        if isinstance(cls.pattern, str):
            cls.pattern = re.compile(cls.pattern)
        match = cls.pattern.match(url)
        if match:
            return cls(match)

    def __iter__(self):
        return self.items()

    def items(self):
        yield (
         Message.Version, 1)

    def skip(self, num):
        return 0

    def config(self, key, default=None):
        return config.interpolate(self._cfgpath, key, default)

    def config_accumulate(self, key):
        return config.accumulate(self._cfgpath, key)

    def _config_shared(self, key, default=None):
        return config.interpolate_common(('extractor', ), (
         (
          self.category, self.subcategory),
         (
          self.basecategory, self.subcategory)), key, default)

    def _config_shared_accumulate(self, key):
        values = config.accumulate(self._cfgpath, key)
        conf = config.get(('extractor', ), self.basecategory)
        if conf:
            values[:0] = config.accumulate((self.subcategory,), key, conf=conf)
        return values

    def request--- This code section failed: ---

 L. 106         0  LOAD_CONST               1
                2  STORE_FAST               'tries'

 L. 107         4  LOAD_FAST                'retries'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    18  'to 18'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _retries
               16  JUMP_FORWARD         20  'to 20'
             18_0  COME_FROM            10  '10'
               18  LOAD_FAST                'retries'
             20_0  COME_FROM            16  '16'
               20  STORE_FAST               'retries'

 L. 108        22  LOAD_FAST                'session'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    36  'to 36'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                session
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            28  '28'
               36  LOAD_FAST                'session'
             38_0  COME_FROM            34  '34'
               38  STORE_FAST               'session'

 L. 109        40  LOAD_FAST                'kwargs'
               42  LOAD_METHOD              setdefault
               44  LOAD_STR                 'timeout'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _timeout
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  POP_TOP          

 L. 110        54  LOAD_FAST                'kwargs'
               56  LOAD_METHOD              setdefault
               58  LOAD_STR                 'verify'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _verify
               64  CALL_METHOD_2         2  '2 positional arguments'
               66  POP_TOP          

 L. 111        68  LOAD_CONST               None
               70  STORE_FAST               'response'

 L. 113        72  LOAD_FAST                'self'
               74  LOAD_ATTR                request_interval
               76  POP_JUMP_IF_FALSE   130  'to 130'

 L. 114        78  LOAD_FAST                'self'
               80  LOAD_ATTR                request_interval

 L. 115        82  LOAD_GLOBAL              time
               84  LOAD_METHOD              time
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  LOAD_GLOBAL              Extractor
               90  LOAD_ATTR                request_timestamp
               92  BINARY_SUBTRACT  
               94  BINARY_SUBTRACT  
               96  STORE_FAST               'seconds'

 L. 116        98  LOAD_FAST                'seconds'
              100  LOAD_CONST               0.0
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   130  'to 130'

 L. 117       106  LOAD_FAST                'self'
              108  LOAD_ATTR                log
              110  LOAD_METHOD              debug
              112  LOAD_STR                 'Sleeping for %.5s seconds'
              114  LOAD_FAST                'seconds'
              116  CALL_METHOD_2         2  '2 positional arguments'
              118  POP_TOP          

 L. 118       120  LOAD_GLOBAL              time
              122  LOAD_METHOD              sleep
              124  LOAD_FAST                'seconds'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  POP_TOP          
            130_0  COME_FROM           104  '104'
            130_1  COME_FROM            76  '76'

 L. 120   130_132  SETUP_LOOP          692  'to 692'

 L. 121   134_136  SETUP_FINALLY       616  'to 616'
              138  SETUP_EXCEPT        160  'to 160'

 L. 122       140  LOAD_FAST                'session'
              142  LOAD_ATTR                request
              144  LOAD_FAST                'method'
              146  LOAD_FAST                'url'
              148  BUILD_TUPLE_2         2 
              150  LOAD_FAST                'kwargs'
              152  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              154  STORE_FAST               'response'
              156  POP_BLOCK        
              158  JUMP_FORWARD        274  'to 274'
            160_0  COME_FROM_EXCEPT    138  '138'

 L. 123       160  DUP_TOP          
              162  LOAD_GLOBAL              requests
              164  LOAD_ATTR                exceptions
              166  LOAD_ATTR                ConnectionError

 L. 124       168  LOAD_GLOBAL              requests
              170  LOAD_ATTR                exceptions
              172  LOAD_ATTR                Timeout

 L. 125       174  LOAD_GLOBAL              requests
              176  LOAD_ATTR                exceptions
              178  LOAD_ATTR                ChunkedEncodingError

 L. 126       180  LOAD_GLOBAL              requests
              182  LOAD_ATTR                exceptions
              184  LOAD_ATTR                ContentDecodingError
              186  BUILD_TUPLE_4         4 
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   222  'to 222'
              192  POP_TOP          
              194  STORE_FAST               'exc'
              196  POP_TOP          
              198  SETUP_FINALLY       208  'to 208'

 L. 127       200  LOAD_FAST                'exc'
              202  STORE_FAST               'msg'
              204  POP_BLOCK        
              206  LOAD_CONST               None
            208_0  COME_FROM_FINALLY   198  '198'
              208  LOAD_CONST               None
              210  STORE_FAST               'exc'
              212  DELETE_FAST              'exc'
              214  END_FINALLY      
              216  POP_EXCEPT       
          218_220  JUMP_FORWARD        612  'to 612'
            222_0  COME_FROM           190  '190'

 L. 128       222  DUP_TOP          
              224  LOAD_GLOBAL              requests
              226  LOAD_ATTR                exceptions
              228  LOAD_ATTR                RequestException
              230  COMPARE_OP               exception-match
          232_234  POP_JUMP_IF_FALSE   272  'to 272'
              236  POP_TOP          
              238  STORE_FAST               'exc'
              240  POP_TOP          
              242  SETUP_FINALLY       258  'to 258'

 L. 129       244  LOAD_GLOBAL              exception
              246  LOAD_METHOD              HttpError
              248  LOAD_FAST                'exc'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  RAISE_VARARGS_1       1  'exception instance'
              254  POP_BLOCK        
              256  LOAD_CONST               None
            258_0  COME_FROM_FINALLY   242  '242'
              258  LOAD_CONST               None
              260  STORE_FAST               'exc'
              262  DELETE_FAST              'exc'
              264  END_FINALLY      
              266  POP_EXCEPT       
          268_270  JUMP_FORWARD        612  'to 612'
            272_0  COME_FROM           232  '232'
              272  END_FINALLY      
            274_0  COME_FROM           158  '158'

 L. 131       274  LOAD_FAST                'response'
              276  LOAD_ATTR                status_code
              278  STORE_FAST               'code'

 L. 132       280  LOAD_FAST                'self'
              282  LOAD_ATTR                _write_pages
          284_286  POP_JUMP_IF_FALSE   298  'to 298'

 L. 133       288  LOAD_FAST                'self'
              290  LOAD_METHOD              _dump_response
              292  LOAD_FAST                'response'
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          
            298_0  COME_FROM           284  '284'

 L. 134       298  LOAD_CONST               200
              300  LOAD_FAST                'code'
              302  DUP_TOP          
              304  ROT_THREE        
              306  COMPARE_OP               <=
          308_310  POP_JUMP_IF_FALSE   322  'to 322'
              312  LOAD_CONST               400
              314  COMPARE_OP               <
          316_318  POP_JUMP_IF_TRUE    420  'to 420'
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           308  '308'
              322  POP_TOP          
            324_0  COME_FROM           320  '320'
              324  LOAD_FAST                'fatal'
              326  LOAD_CONST               None
              328  COMPARE_OP               is
          330_332  POP_JUMP_IF_FALSE   360  'to 360'

 L. 135       334  LOAD_CONST               400
              336  LOAD_FAST                'code'
              338  DUP_TOP          
              340  ROT_THREE        
              342  COMPARE_OP               <=
          344_346  POP_JUMP_IF_FALSE   358  'to 358'
              348  LOAD_CONST               500
              350  COMPARE_OP               <
          352_354  POP_JUMP_IF_TRUE    420  'to 420'
              356  JUMP_FORWARD        360  'to 360'
            358_0  COME_FROM           344  '344'
              358  POP_TOP          
            360_0  COME_FROM           356  '356'
            360_1  COME_FROM           330  '330'
              360  LOAD_FAST                'fatal'
          362_364  POP_JUMP_IF_TRUE    436  'to 436'

 L. 136       366  LOAD_CONST               400
              368  LOAD_FAST                'code'
              370  DUP_TOP          
              372  ROT_THREE        
              374  COMPARE_OP               <=
          376_378  POP_JUMP_IF_FALSE   390  'to 390'
              380  LOAD_CONST               429
              382  COMPARE_OP               <
          384_386  POP_JUMP_IF_TRUE    420  'to 420'
              388  JUMP_FORWARD        392  'to 392'
            390_0  COME_FROM           376  '376'
              390  POP_TOP          
            392_0  COME_FROM           388  '388'
              392  LOAD_CONST               431
              394  LOAD_FAST                'code'
              396  DUP_TOP          
              398  ROT_THREE        
              400  COMPARE_OP               <=
          402_404  POP_JUMP_IF_FALSE   416  'to 416'
              406  LOAD_CONST               500
              408  COMPARE_OP               <
          410_412  POP_JUMP_IF_FALSE   436  'to 436'
              414  JUMP_FORWARD        420  'to 420'
            416_0  COME_FROM           402  '402'
              416  POP_TOP          
              418  JUMP_FORWARD        436  'to 436'
            420_0  COME_FROM           414  '414'
            420_1  COME_FROM           384  '384'
            420_2  COME_FROM           352  '352'
            420_3  COME_FROM           316  '316'

 L. 137       420  LOAD_FAST                'encoding'
          422_424  POP_JUMP_IF_FALSE   432  'to 432'

 L. 138       426  LOAD_FAST                'encoding'
              428  LOAD_FAST                'response'
              430  STORE_ATTR               encoding
            432_0  COME_FROM           422  '422'

 L. 139       432  LOAD_FAST                'response'
              434  RETURN_VALUE     
            436_0  COME_FROM           418  '418'
            436_1  COME_FROM           410  '410'
            436_2  COME_FROM           362  '362'

 L. 140       436  LOAD_FAST                'notfound'
          438_440  POP_JUMP_IF_FALSE   462  'to 462'
              442  LOAD_FAST                'code'
              444  LOAD_CONST               404
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   462  'to 462'

 L. 141       452  LOAD_GLOBAL              exception
              454  LOAD_METHOD              NotFoundError
              456  LOAD_FAST                'notfound'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  RAISE_VARARGS_1       1  'exception instance'
            462_0  COME_FROM           448  '448'
            462_1  COME_FROM           438  '438'

 L. 143       462  LOAD_FAST                'response'
              464  LOAD_ATTR                reason
              466  STORE_FAST               'reason'

 L. 144       468  LOAD_GLOBAL              cloudflare
              470  LOAD_METHOD              is_challenge
              472  LOAD_FAST                'response'
              474  CALL_METHOD_1         1  '1 positional argument'
          476_478  POP_JUMP_IF_FALSE   542  'to 542'

 L. 145       480  LOAD_FAST                'self'
              482  LOAD_ATTR                log
              484  LOAD_METHOD              info
              486  LOAD_STR                 'Solving Cloudflare challenge'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  POP_TOP          

 L. 146       492  LOAD_GLOBAL              cloudflare
              494  LOAD_METHOD              solve_challenge

 L. 147       496  LOAD_FAST                'session'
              498  LOAD_FAST                'response'
              500  LOAD_FAST                'kwargs'
              502  CALL_METHOD_3         3  '3 positional arguments'
              504  UNPACK_SEQUENCE_3     3 
              506  STORE_FAST               'response'
              508  STORE_FAST               'domain'
              510  STORE_FAST               'cookies'

 L. 148       512  LOAD_FAST                'cookies'
          514_516  POP_JUMP_IF_FALSE   542  'to 542'

 L. 149       518  LOAD_GLOBAL              cloudflare
              520  LOAD_ATTR                cookies
              522  LOAD_METHOD              update

 L. 150       524  LOAD_FAST                'self'
              526  LOAD_ATTR                category
              528  LOAD_FAST                'domain'
              530  LOAD_FAST                'cookies'
              532  BUILD_TUPLE_2         2 
              534  CALL_METHOD_2         2  '2 positional arguments'
              536  POP_TOP          

 L. 151       538  LOAD_FAST                'response'
              540  RETURN_VALUE     
            542_0  COME_FROM           514  '514'
            542_1  COME_FROM           476  '476'

 L. 152       542  LOAD_GLOBAL              cloudflare
              544  LOAD_METHOD              is_captcha
              546  LOAD_FAST                'response'
              548  CALL_METHOD_1         1  '1 positional argument'
          550_552  POP_JUMP_IF_FALSE   566  'to 566'

 L. 153       554  LOAD_FAST                'self'
              556  LOAD_ATTR                log
              558  LOAD_METHOD              warning
              560  LOAD_STR                 'Cloudflare CAPTCHA'
              562  CALL_METHOD_1         1  '1 positional argument'
              564  POP_TOP          
            566_0  COME_FROM           550  '550'

 L. 155       566  LOAD_STR                 "'{} {}' for '{}'"
              568  LOAD_METHOD              format
              570  LOAD_FAST                'code'
              572  LOAD_FAST                'reason'
              574  LOAD_FAST                'url'
              576  CALL_METHOD_3         3  '3 positional arguments'
              578  STORE_FAST               'msg'

 L. 156       580  LOAD_FAST                'code'
              582  LOAD_CONST               500
              584  COMPARE_OP               <
          586_588  POP_JUMP_IF_FALSE   612  'to 612'
              590  LOAD_FAST                'code'
              592  LOAD_CONST               429
              594  COMPARE_OP               !=
          596_598  POP_JUMP_IF_FALSE   612  'to 612'
              600  LOAD_FAST                'code'
              602  LOAD_CONST               430
              604  COMPARE_OP               !=
          606_608  POP_JUMP_IF_FALSE   612  'to 612'

 L. 157       610  BREAK_LOOP       
            612_0  COME_FROM           606  '606'
            612_1  COME_FROM           596  '596'
            612_2  COME_FROM           586  '586'
            612_3  COME_FROM           268  '268'
            612_4  COME_FROM           218  '218'
              612  POP_BLOCK        
              614  LOAD_CONST               None
            616_0  COME_FROM_FINALLY   134  '134'

 L. 159       616  LOAD_GLOBAL              time
              618  LOAD_METHOD              time
              620  CALL_METHOD_0         0  '0 positional arguments'
              622  LOAD_GLOBAL              Extractor
              624  STORE_ATTR               request_timestamp
              626  END_FINALLY      

 L. 161       628  LOAD_FAST                'self'
              630  LOAD_ATTR                log
              632  LOAD_METHOD              debug
              634  LOAD_STR                 '%s (%s/%s)'
              636  LOAD_FAST                'msg'
              638  LOAD_FAST                'tries'
              640  LOAD_FAST                'retries'
              642  LOAD_CONST               1
              644  BINARY_ADD       
              646  CALL_METHOD_4         4  '4 positional arguments'
              648  POP_TOP          

 L. 162       650  LOAD_FAST                'tries'
              652  LOAD_FAST                'retries'
              654  COMPARE_OP               >
          656_658  POP_JUMP_IF_FALSE   662  'to 662'

 L. 163       660  BREAK_LOOP       
            662_0  COME_FROM           656  '656'

 L. 164       662  LOAD_GLOBAL              time
              664  LOAD_METHOD              sleep
              666  LOAD_GLOBAL              max
              668  LOAD_FAST                'tries'
              670  LOAD_FAST                'self'
              672  LOAD_ATTR                request_interval
              674  CALL_FUNCTION_2       2  '2 positional arguments'
              676  CALL_METHOD_1         1  '1 positional argument'
              678  POP_TOP          

 L. 165       680  LOAD_FAST                'tries'
              682  LOAD_CONST               1
              684  INPLACE_ADD      
              686  STORE_FAST               'tries'
              688  JUMP_BACK           134  'to 134'
              690  POP_BLOCK        
            692_0  COME_FROM_LOOP      130  '130'

 L. 167       692  LOAD_GLOBAL              exception
              694  LOAD_METHOD              HttpError
              696  LOAD_FAST                'msg'
              698  LOAD_FAST                'response'
              700  CALL_METHOD_2         2  '2 positional arguments'
              702  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `LOAD_FAST' instruction at offset 436

    def wait(self, *, seconds=None, until=None, adjust=1.0, reason='rate limit reset'):
        now = time.time()
        if seconds:
            seconds = float(seconds)
            until = now + seconds
        else:
            if until:
                if isinstance(until, datetime.datetime):
                    epoch = datetime.datetime(1970, 1, 1)
                    until = (until - epoch) / datetime.timedelta(0, 1)
                else:
                    until = float(until)
                seconds = until - now
            else:
                raise ValueError("Either 'seconds' or 'until' is required")
        seconds += adjust
        if seconds <= 0.0:
            return
        if reason:
            t = datetime.datetime.fromtimestamp(until).time()
            isotime = '{:02}:{:02}:{:02}'.format(t.hour, t.minute, t.second)
            self.log.info('Waiting until %s for %s.', isotime, reason)
        time.sleep(seconds)

    def _get_auth_info(self):
        """Return authentication information as (username, password) tuple"""
        username = self.config('username')
        password = None
        if username:
            password = self.config('password')
        else:
            if self.config('netrc', False):
                try:
                    info = netrc.netrc().authenticators(self.category)
                    username, _, password = info
                except (OSError, netrc.NetrcParseError) as exc:
                    try:
                        self.log.error('netrc: %s', exc)
                    finally:
                        exc = None
                        del exc

                except TypeError:
                    self.log.warning('netrc: No authentication info')

        return (
         username, password)

    def _init_headers(self):
        """Initialize HTTP headers for the 'session' object"""
        headers = self.session.headers
        headers.clear()
        headers['User-Agent'] = self.config('user-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0')
        headers['Accept'] = '*/*'
        headers['Accept-Language'] = 'en-US,en;q=0.5'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests'] = '1'

    def _init_proxies(self):
        """Update the session's proxy map"""
        proxies = self.config('proxy')
        if proxies:
            if isinstance(proxies, str):
                proxies = {'http':proxies, 
                 'https':proxies}
            elif isinstance(proxies, dict):
                for scheme, proxy in proxies.items():
                    if '://' not in proxy:
                        proxies[scheme] = 'http://' + proxy.lstrip('/')

                self.session.proxies = proxies
            else:
                self.log.warning('invalid proxy specifier: %s', proxies)

    def _init_cookies(self):
        """Populate the session's cookiejar"""
        if self.cookiedomain is None:
            return
            cookies = self.config('cookies')
            if cookies:
                if isinstance(cookies, dict):
                    self._update_cookies_dict(cookies, self.cookiedomain)
        elif isinstance(cookies, str):
            cookiefile = util.expand_path(cookies)
            try:
                with open(cookiefile) as (fp):
                    cookies = util.load_cookiestxt(fp)
            except Exception as exc:
                try:
                    self.log.warning('cookies: %s', exc)
                finally:
                    exc = None
                    del exc

            else:
                self._update_cookies(cookies)
                self._cookiefile = cookiefile
        else:
            self.log.warning("expected 'dict' or 'str' value for 'cookies' option, got '%s' (%s)", cookies.__class__.__name__, cookies)
        cookies = cloudflare.cookies(self.category)
        if cookies:
            domain, cookies = cookies
            self._update_cookies_dict(cookies, domain)

    def _store_cookies(self):
        """Store the session's cookiejar in a cookies.txt file"""
        if self._cookiefile:
            if self.config('cookies-update', True):
                try:
                    with open(self._cookiefile, 'w') as (fp):
                        util.save_cookiestxt(fp, self._cookiejar)
                except OSError as exc:
                    try:
                        self.log.warning('cookies: %s', exc)
                    finally:
                        exc = None
                        del exc

    def _update_cookies(self, cookies, *, domain=''):
        """Update the session's cookiejar with 'cookies'"""
        if isinstance(cookies, dict):
            self._update_cookies_dict(cookies, domain or self.cookiedomain)
        else:
            setcookie = self._cookiejar.set_cookie
        try:
            cookies = iter(cookies)
        except TypeError:
            setcookie(cookies)
        else:
            for cookie in cookies:
                setcookie(cookie)

    def _update_cookies_dict(self, cookiedict, domain):
        """Update cookiejar with name-value pairs from a dict"""
        setcookie = self._cookiejar.set
        for name, value in cookiedict.items():
            setcookie(name, value, domain=domain)

    def _check_cookies(self, cookienames, *, domain=None):
        """Check if all 'cookienames' are in the session's cookiejar"""
        if not self._cookiejar:
            return False
        if domain is None:
            domain = self.cookiedomain
        names = set(cookienames)
        now = time.time()
        for cookie in self._cookiejar:
            if cookie.name in names and cookie.domain == domain:
                if cookie.expires:
                    if cookie.expires < now:
                        self.log.warning("Cookie '%s' has expired", cookie.name)
                names.discard(cookie.name)
                return names or True

        return False

    def _get_date_min_max(self, dmin=None, dmax=None):
        """Retrieve and parse 'date-min' and 'date-max' config values"""

        def get(key, default):
            ts = self.config(key, default)
            if isinstance(ts, str):
                try:
                    ts = int(datetime.datetime.strptime(ts, fmt).timestamp())
                except ValueError as exc:
                    try:
                        self.log.warning("Unable to parse '%s': %s", key, exc)
                        ts = default
                    finally:
                        exc = None
                        del exc

            return ts

        fmt = self.config('date-format', '%Y-%m-%dT%H:%M:%S')
        return (get('date-min', dmin), get('date-max', dmax))

    def _dispatch_extractors(self, extractor_data, default=()):
        """ """
        extractors = {data[0].subcategory:data for data in extractor_data}
        include = self.config('include', default) or ()
        if include == 'all':
            include = extractors
        else:
            if isinstance(include, str):
                include = include.split(',')
        result = [
         (
          Message.Version, 1)]
        for category in include:
            if category in extractors:
                extr, url = extractors[category]
                result.append((Message.Queue, url, {'_extractor': extr}))

        return iter(result)

    @classmethod
    def _get_tests(cls):
        """Yield an extractor's test cases as (URL, RESULTS) tuples"""
        tests = cls.test
        if not tests:
            return
        if len(tests) == 2:
            if not tests[1] or isinstance(tests[1], dict):
                tests = (
                 tests,)
        for test in tests:
            if isinstance(test, str):
                test = (
                 test, None)
            yield test

    def _dump_response(self, response, history=True):
        """Write the response content to a .dump file in the current directory.

        The file name is derived from the response url,
        replacing special characters with "_"
        """
        if history:
            for resp in response.history:
                self._dump_response(resp, False)

        elif hasattr(Extractor, '_dump_index'):
            Extractor._dump_index += 1
        else:
            Extractor._dump_index = 1
            Extractor._dump_sanitize = re.compile('[\\\\\\\\|/<>:\\"?*&=#]+').sub
        fname = '{:>02}_{}'.format(Extractor._dump_index, Extractor._dump_sanitize('_', response.url))[:250]
        try:
            with open(fname + '.dump', 'wb') as (fp):
                util.dump_response(response,
                  fp, headers=(self._write_pages == 'all'))
        except Exception as e:
            try:
                self.log.warning('Failed to dump HTTP request (%s: %s)', e.__class__.__name__, e)
            finally:
                e = None
                del e


class GalleryExtractor(Extractor):
    subcategory = 'gallery'
    filename_fmt = '{category}_{gallery_id}_{num:>03}.{extension}'
    directory_fmt = ('{category}', '{gallery_id} {title}')
    archive_fmt = '{gallery_id}_{num}'
    enum = 'num'

    def __init__(self, match, url=None):
        Extractor.__init__(self, match)
        self.gallery_url = self.root + match.group(1) if url is None else url

    def items(self):
        self.login()
        page = self.request((self.gallery_url), notfound=(self.subcategory)).text
        data = self.metadata(page)
        imgs = self.images(page)
        if 'count' in data:
            images = zip(range(1, data['count'] + 1), imgs)
        else:
            try:
                data['count'] = len(imgs)
            except TypeError:
                pass

            images = enumerate(imgs, 1)
        yield (Message.Version, 1)
        yield (Message.Directory, data)
        for data[self.enum], (url, imgdata) in images:
            if imgdata:
                data.update(imgdata)
                if 'extension' not in imgdata:
                    text.nameext_from_url(url, data)
            else:
                text.nameext_from_url(url, data)
            yield (
             Message.Url, url, data)

    def login(self):
        """Login and set necessary cookies"""
        pass

    def metadata(self, page):
        """Return a dict with general metadata"""
        pass

    def images(self, page):
        """Return a list of all (image-url, metadata)-tuples"""
        pass


class ChapterExtractor(GalleryExtractor):
    subcategory = 'chapter'
    directory_fmt = ('{category}', '{manga}', '{volume:?v/ />02}c{chapter:>03}{chapter_minor:?//}{title:?: //}')
    filename_fmt = '{manga}_c{chapter:>03}{chapter_minor:?//}_{page:>03}.{extension}'
    archive_fmt = '{manga}_{chapter}{chapter_minor}_{page}'
    enum = 'page'


class MangaExtractor(Extractor):
    subcategory = 'manga'
    categorytransfer = True
    chapterclass = None
    reverse = True

    def __init__(self, match, url=None):
        Extractor.__init__(self, match)
        self.manga_url = url or self.root + match.group(1)
        if self.config('chapter-reverse', False):
            self.reverse = not self.reverse

    def items(self):
        self.login()
        page = self.request(self.manga_url).text
        chapters = self.chapters(page)
        if self.reverse:
            chapters.reverse()
        yield (Message.Version, 1)
        for chapter, data in chapters:
            data['_extractor'] = self.chapterclass
            yield (Message.Queue, chapter, data)

    def login(self):
        """Login and set necessary cookies"""
        pass

    def chapters(self, page):
        """Return a list of all (chapter-url, metadata)-tuples"""
        pass


class AsynchronousMixin:
    __doc__ = 'Run info extraction in a separate thread'

    def __iter__(self):
        messages = queue.Queue(5)
        thread = threading.Thread(target=(self.async_items),
          args=(
         messages,),
          daemon=True)
        thread.start()
        while True:
            msg = messages.get()
            if msg is None:
                thread.join()
                return
            if isinstance(msg, Exception):
                thread.join()
                raise msg
            yield msg
            messages.task_done()

    def async_items(self, messages):
        try:
            for msg in self.items():
                messages.put(msg)

        except Exception as exc:
            try:
                messages.put(exc)
            finally:
                exc = None
                del exc

        messages.put(None)


def generate_extractors(extractor_data, symtable, classes):
    """Dynamically generate Extractor classes"""
    extractors = config.get(('extractor', ), classes[0].basecategory)
    ckey = extractor_data.get('_ckey')
    prev = None
    if extractors:
        extractor_data.update(extractors)
    for category, info in extractor_data.items():
        if isinstance(info, dict):
            if 'root' not in info:
                continue
            root = info['root']
            domain = root[root.index(':') + 3:]
            pattern = info.get('pattern') or re.escape(domain)
            name = (info.get('name') or category).capitalize()
            for cls in classes:

                class Extr(cls):
                    pass

                Extr.__module__ = cls.__module__
                Extr.__name__ = Extr.__qualname__ = name + cls.subcategory.capitalize() + 'Extractor'
                Extr.__doc__ = 'Extractor for ' + cls.subcategory + 's from ' + domain
                Extr.category = category
                Extr.pattern = '(?:https?://)?' + pattern + cls.pattern_fmt
                Extr.test = info.get('test-' + cls.subcategory)
                Extr.root = root
                if 'extra' in info:
                    for key, value in info['extra'].items():
                        setattr(Extr, key, value)

                if prev:
                    if ckey:
                        setattr(Extr, ckey, prev)
                symtable[Extr.__name__] = prev = Extr


pyopenssl = config.get((), 'pyopenssl', False)
if not pyopenssl:
    try:
        from requests.packages.urllib3.contrib import pyopenssl
        pyopenssl.extract_from_urllib3()
    except ImportError:
        pass

del pyopenssl
ciphers = config.get((), 'ciphers', True)
if ciphers:
    if ciphers is True:
        ciphers = 'TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:AES128-SHA:AES256-SHA:DES-CBC3-SHA'
    else:
        if isinstance(ciphers, list):
            ciphers = ':'.join(ciphers)
        from requests.packages.urllib3.util import ssl_
        ssl_.DEFAULT_CIPHERS = ciphers
        del ssl_
del ciphers