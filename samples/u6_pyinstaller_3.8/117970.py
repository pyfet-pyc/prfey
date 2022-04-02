# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\http.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import asyncio, json, logging, sys
import urllib.parse as _uriquote
import weakref, aiohttp
from .errors import HTTPException, Forbidden, NotFound, LoginFailure, GatewayNotFound
from . import __version__, utils
log = logging.getLogger(__name__)

async def json_or_text(response):
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['content-type'] == 'application/json':
            return json.loads(text)
    except KeyError:
        pass
    else:
        return text


class Route:
    BASE = 'https://discordapp.com/api/v7'

    def __init__(self, method, path, **parameters):
        self.path = path
        self.method = method
        url = self.BASE + self.path
        if parameters:
            self.url = (url.format)(**)
        else:
            self.url = url
        self.channel_id = parameters.get('channel_id')
        self.guild_id = parameters.get('guild_id')

    @property
    def bucket(self):
        return '{0.channel_id}:{0.guild_id}:{0.path}'.format(self)


class MaybeUnlock:

    def __init__(self, lock):
        self.lock = lock
        self._unlock = True

    def __enter__(self):
        return self

    def defer(self):
        self._unlock = False

    def __exit__(self, type, value, traceback):
        if self._unlock:
            self.lock.release()


class HTTPClient:
    __doc__ = 'Represents an HTTP client sending HTTP requests to the Discord API.'
    SUCCESS_LOG = '{method} {url} has received {text}'
    REQUEST_LOG = '{method} {url} with {json} has returned {status}'

    def __init__(self, connector=None, *, proxy=None, proxy_auth=None, loop=None, unsync_clock=True):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.connector = connector
        self._HTTPClient__session = None
        self._locks = weakref.WeakValueDictionary()
        self._global_over = asyncio.Event()
        self._global_over.set()
        self.token = None
        self.bot_token = False
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.use_clock = not unsync_clock
        user_agent = 'DiscordBot (https://github.com/Rapptz/discord.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    def recreate(self):
        if self._HTTPClient__session.closed:
            self._HTTPClient__session = aiohttp.ClientSession(connector=(self.connector))

    async def request--- This code section failed: ---

 L. 115         0  LOAD_FAST                'route'
                2  LOAD_ATTR                bucket
                4  STORE_FAST               'bucket'

 L. 116         6  LOAD_FAST                'route'
                8  LOAD_ATTR                method
               10  STORE_FAST               'method'

 L. 117        12  LOAD_FAST                'route'
               14  LOAD_ATTR                url
               16  STORE_FAST               'url'

 L. 119        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _locks
               22  LOAD_METHOD              get
               24  LOAD_FAST                'bucket'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'lock'

 L. 120        30  LOAD_FAST                'lock'
               32  LOAD_CONST               None
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    64  'to 64'

 L. 121        38  LOAD_GLOBAL              asyncio
               40  LOAD_METHOD              Lock
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'lock'

 L. 122        46  LOAD_FAST                'bucket'
               48  LOAD_CONST               None
               50  COMPARE_OP               is-not
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L. 123        54  LOAD_FAST                'lock'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _locks
               60  LOAD_FAST                'bucket'
               62  STORE_SUBSCR     
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            36  '36'

 L. 127        64  LOAD_FAST                'self'
               66  LOAD_ATTR                user_agent

 L. 128        68  LOAD_STR                 'millisecond'

 L. 126        70  LOAD_CONST               ('User-Agent', 'X-Ratelimit-Precision')
               72  BUILD_CONST_KEY_MAP_2     2 
               74  STORE_FAST               'headers'

 L. 131        76  LOAD_FAST                'self'
               78  LOAD_ATTR                token
               80  LOAD_CONST               None
               82  COMPARE_OP               is-not
               84  POP_JUMP_IF_FALSE   112  'to 112'

 L. 132        86  LOAD_FAST                'self'
               88  LOAD_ATTR                bot_token
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  LOAD_STR                 'Bot '
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                token
               98  BINARY_ADD       
              100  JUMP_FORWARD        106  'to 106'
            102_0  COME_FROM            90  '90'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                token
            106_0  COME_FROM           100  '100'
              106  LOAD_FAST                'headers'
              108  LOAD_STR                 'Authorization'
              110  STORE_SUBSCR     
            112_0  COME_FROM            84  '84'

 L. 134       112  LOAD_STR                 'json'
              114  LOAD_FAST                'kwargs'
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   148  'to 148'

 L. 135       120  LOAD_STR                 'application/json'
              122  LOAD_FAST                'headers'
              124  LOAD_STR                 'Content-Type'
              126  STORE_SUBSCR     

 L. 136       128  LOAD_GLOBAL              utils
              130  LOAD_METHOD              to_json
              132  LOAD_FAST                'kwargs'
              134  LOAD_METHOD              pop
              136  LOAD_STR                 'json'
              138  CALL_METHOD_1         1  ''
              140  CALL_METHOD_1         1  ''
              142  LOAD_FAST                'kwargs'
              144  LOAD_STR                 'data'
              146  STORE_SUBSCR     
            148_0  COME_FROM           118  '118'

 L. 138       148  SETUP_FINALLY       164  'to 164'

 L. 139       150  LOAD_FAST                'kwargs'
              152  LOAD_METHOD              pop
              154  LOAD_STR                 'reason'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'reason'
              160  POP_BLOCK        
              162  JUMP_FORWARD        184  'to 184'
            164_0  COME_FROM_FINALLY   148  '148'

 L. 140       164  DUP_TOP          
              166  LOAD_GLOBAL              KeyError
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   182  'to 182'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 141       178  POP_EXCEPT       
              180  JUMP_FORWARD        204  'to 204'
            182_0  COME_FROM           170  '170'
              182  END_FINALLY      
            184_0  COME_FROM           162  '162'

 L. 143       184  LOAD_FAST                'reason'
              186  POP_JUMP_IF_FALSE   204  'to 204'

 L. 144       188  LOAD_GLOBAL              _uriquote
              190  LOAD_FAST                'reason'
              192  LOAD_STR                 '/ '
              194  LOAD_CONST               ('safe',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  LOAD_FAST                'headers'
              200  LOAD_STR                 'X-Audit-Log-Reason'
              202  STORE_SUBSCR     
            204_0  COME_FROM           186  '186'
            204_1  COME_FROM           180  '180'

 L. 146       204  LOAD_FAST                'headers'
              206  LOAD_FAST                'kwargs'
              208  LOAD_STR                 'headers'
              210  STORE_SUBSCR     

 L. 149       212  LOAD_FAST                'self'
              214  LOAD_ATTR                proxy
              216  LOAD_CONST               None
              218  COMPARE_OP               is-not
              220  POP_JUMP_IF_FALSE   232  'to 232'

 L. 150       222  LOAD_FAST                'self'
              224  LOAD_ATTR                proxy
              226  LOAD_FAST                'kwargs'
              228  LOAD_STR                 'proxy'
              230  STORE_SUBSCR     
            232_0  COME_FROM           220  '220'

 L. 151       232  LOAD_FAST                'self'
              234  LOAD_ATTR                proxy_auth
              236  LOAD_CONST               None
              238  COMPARE_OP               is-not
              240  POP_JUMP_IF_FALSE   252  'to 252'

 L. 152       242  LOAD_FAST                'self'
              244  LOAD_ATTR                proxy_auth
              246  LOAD_FAST                'kwargs'
              248  LOAD_STR                 'proxy_auth'
              250  STORE_SUBSCR     
            252_0  COME_FROM           240  '240'

 L. 154       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _global_over
              256  LOAD_METHOD              is_set
              258  CALL_METHOD_0         0  ''
          260_262  POP_JUMP_IF_TRUE    280  'to 280'

 L. 156       264  LOAD_FAST                'self'
              266  LOAD_ATTR                _global_over
              268  LOAD_METHOD              wait
              270  CALL_METHOD_0         0  ''
              272  GET_AWAITABLE    
              274  LOAD_CONST               None
              276  YIELD_FROM       
              278  POP_TOP          
            280_0  COME_FROM           260  '260'

 L. 158       280  LOAD_FAST                'lock'
              282  LOAD_METHOD              acquire
              284  CALL_METHOD_0         0  ''
              286  GET_AWAITABLE    
              288  LOAD_CONST               None
              290  YIELD_FROM       
              292  POP_TOP          

 L. 159       294  LOAD_GLOBAL              MaybeUnlock
              296  LOAD_FAST                'lock'
              298  CALL_FUNCTION_1       1  ''
          300_302  SETUP_WITH          918  'to 918'
              304  STORE_FAST               'maybe_lock'

 L. 160       306  LOAD_GLOBAL              range
              308  LOAD_CONST               5
              310  CALL_FUNCTION_1       1  ''
              312  GET_ITER         
          314_316  FOR_ITER            904  'to 904'
              318  STORE_FAST               'tries'

 L. 161       320  LOAD_FAST                'files'
          322_324  POP_JUMP_IF_FALSE   350  'to 350'

 L. 162       326  LOAD_FAST                'files'
              328  GET_ITER         
              330  FOR_ITER            350  'to 350'
              332  STORE_FAST               'f'

 L. 163       334  LOAD_FAST                'f'
              336  LOAD_ATTR                reset
              338  LOAD_FAST                'tries'
              340  LOAD_CONST               ('seek',)
              342  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              344  POP_TOP          
          346_348  JUMP_BACK           330  'to 330'
            350_0  COME_FROM           322  '322'

 L. 165       350  LOAD_FAST                'self'
              352  LOAD_ATTR                _HTTPClient__session
              354  LOAD_ATTR                request
              356  LOAD_FAST                'method'
              358  LOAD_FAST                'url'
              360  BUILD_TUPLE_2         2 
              362  LOAD_FAST                'kwargs'
              364  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              366  BEFORE_ASYNC_WITH
              368  GET_AWAITABLE    
              370  LOAD_CONST               None
              372  YIELD_FROM       
          374_376  SETUP_ASYNC_WITH    888  'to 888'
              378  STORE_FAST               'r'

 L. 166       380  LOAD_GLOBAL              log
              382  LOAD_METHOD              debug
              384  LOAD_STR                 '%s %s with %s has returned %s'
              386  LOAD_FAST                'method'
              388  LOAD_FAST                'url'
              390  LOAD_FAST                'kwargs'
              392  LOAD_METHOD              get
              394  LOAD_STR                 'data'
              396  CALL_METHOD_1         1  ''
              398  LOAD_FAST                'r'
              400  LOAD_ATTR                status
              402  CALL_METHOD_5         5  ''
              404  POP_TOP          

 L. 169       406  LOAD_GLOBAL              json_or_text
              408  LOAD_FAST                'r'
              410  CALL_FUNCTION_1       1  ''
              412  GET_AWAITABLE    
              414  LOAD_CONST               None
              416  YIELD_FROM       
              418  STORE_FAST               'data'

 L. 172       420  LOAD_FAST                'r'
              422  LOAD_ATTR                headers
              424  LOAD_METHOD              get
              426  LOAD_STR                 'X-Ratelimit-Remaining'
              428  CALL_METHOD_1         1  ''
              430  STORE_FAST               'remaining'

 L. 173       432  LOAD_FAST                'remaining'
              434  LOAD_STR                 '0'
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   508  'to 508'
              442  LOAD_FAST                'r'
              444  LOAD_ATTR                status
              446  LOAD_CONST               429
              448  COMPARE_OP               !=
          450_452  POP_JUMP_IF_FALSE   508  'to 508'

 L. 175       454  LOAD_GLOBAL              utils
              456  LOAD_ATTR                _parse_ratelimit_header
              458  LOAD_FAST                'r'
              460  LOAD_FAST                'self'
              462  LOAD_ATTR                use_clock
              464  LOAD_CONST               ('use_clock',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  STORE_FAST               'delta'

 L. 176       470  LOAD_GLOBAL              log
              472  LOAD_METHOD              debug
              474  LOAD_STR                 'A rate limit bucket has been exhausted (bucket: %s, retry: %s).'
              476  LOAD_FAST                'bucket'
              478  LOAD_FAST                'delta'
              480  CALL_METHOD_3         3  ''
              482  POP_TOP          

 L. 177       484  LOAD_FAST                'maybe_lock'
              486  LOAD_METHOD              defer
              488  CALL_METHOD_0         0  ''
              490  POP_TOP          

 L. 178       492  LOAD_FAST                'self'
              494  LOAD_ATTR                loop
              496  LOAD_METHOD              call_later
              498  LOAD_FAST                'delta'
              500  LOAD_FAST                'lock'
              502  LOAD_ATTR                release
              504  CALL_METHOD_2         2  ''
              506  POP_TOP          
            508_0  COME_FROM           450  '450'
            508_1  COME_FROM           438  '438'

 L. 181       508  LOAD_CONST               300
              510  LOAD_FAST                'r'
              512  LOAD_ATTR                status
              514  DUP_TOP          
              516  ROT_THREE        
              518  COMPARE_OP               >
          520_522  POP_JUMP_IF_FALSE   534  'to 534'
              524  LOAD_CONST               200
              526  COMPARE_OP               >=
          528_530  POP_JUMP_IF_FALSE   592  'to 592'
              532  JUMP_FORWARD        538  'to 538'
            534_0  COME_FROM           520  '520'
              534  POP_TOP          
              536  JUMP_FORWARD        592  'to 592'
            538_0  COME_FROM           532  '532'

 L. 182       538  LOAD_GLOBAL              log
              540  LOAD_METHOD              debug
              542  LOAD_STR                 '%s %s has received %s'
              544  LOAD_FAST                'method'
              546  LOAD_FAST                'url'
              548  LOAD_FAST                'data'
              550  CALL_METHOD_4         4  ''
              552  POP_TOP          

 L. 183       554  LOAD_FAST                'data'
              556  POP_BLOCK        
              558  ROT_TWO          
              560  BEGIN_FINALLY    
              562  WITH_CLEANUP_START
              564  GET_AWAITABLE    
              566  LOAD_CONST               None
              568  YIELD_FROM       
              570  WITH_CLEANUP_FINISH
              572  POP_FINALLY           0  ''
              574  ROT_TWO          
              576  POP_TOP          
              578  POP_BLOCK        
              580  ROT_TWO          
              582  BEGIN_FINALLY    
              584  WITH_CLEANUP_START
              586  WITH_CLEANUP_FINISH
              588  POP_FINALLY           0  ''
              590  RETURN_VALUE     
            592_0  COME_FROM           536  '536'
            592_1  COME_FROM           528  '528'

 L. 186       592  LOAD_FAST                'r'
              594  LOAD_ATTR                status
              596  LOAD_CONST               429
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   770  'to 770'

 L. 187       604  LOAD_FAST                'r'
              606  LOAD_ATTR                headers
              608  LOAD_METHOD              get
              610  LOAD_STR                 'Via'
              612  CALL_METHOD_1         1  ''
          614_616  POP_JUMP_IF_TRUE    628  'to 628'

 L. 189       618  LOAD_GLOBAL              HTTPException
              620  LOAD_FAST                'r'
              622  LOAD_FAST                'data'
              624  CALL_FUNCTION_2       2  ''
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           614  '614'

 L. 191       628  LOAD_STR                 'We are being rate limited. Retrying in %.2f seconds. Handled under the bucket "%s"'
              630  STORE_FAST               'fmt'

 L. 194       632  LOAD_FAST                'data'
              634  LOAD_STR                 'retry_after'
              636  BINARY_SUBSCR    
              638  LOAD_CONST               1000.0
              640  BINARY_TRUE_DIVIDE
              642  STORE_FAST               'retry_after'

 L. 195       644  LOAD_GLOBAL              log
              646  LOAD_METHOD              warning
              648  LOAD_FAST                'fmt'
              650  LOAD_FAST                'retry_after'
              652  LOAD_FAST                'bucket'
              654  CALL_METHOD_3         3  ''
              656  POP_TOP          

 L. 198       658  LOAD_FAST                'data'
              660  LOAD_METHOD              get
              662  LOAD_STR                 'global'
              664  LOAD_CONST               False
              666  CALL_METHOD_2         2  ''
              668  STORE_FAST               'is_global'

 L. 199       670  LOAD_FAST                'is_global'
          672_674  POP_JUMP_IF_FALSE   698  'to 698'

 L. 200       676  LOAD_GLOBAL              log
              678  LOAD_METHOD              warning
              680  LOAD_STR                 'Global rate limit has been hit. Retrying in %.2f seconds.'
              682  LOAD_FAST                'retry_after'
              684  CALL_METHOD_2         2  ''
              686  POP_TOP          

 L. 201       688  LOAD_FAST                'self'
              690  LOAD_ATTR                _global_over
              692  LOAD_METHOD              clear
              694  CALL_METHOD_0         0  ''
              696  POP_TOP          
            698_0  COME_FROM           672  '672'

 L. 203       698  LOAD_GLOBAL              asyncio
              700  LOAD_METHOD              sleep
              702  LOAD_FAST                'retry_after'
              704  CALL_METHOD_1         1  ''
              706  GET_AWAITABLE    
              708  LOAD_CONST               None
              710  YIELD_FROM       
              712  POP_TOP          

 L. 204       714  LOAD_GLOBAL              log
              716  LOAD_METHOD              debug
              718  LOAD_STR                 'Done sleeping for the rate limit. Retrying...'
              720  CALL_METHOD_1         1  ''
              722  POP_TOP          

 L. 208       724  LOAD_FAST                'is_global'
          726_728  POP_JUMP_IF_FALSE   750  'to 750'

 L. 209       730  LOAD_FAST                'self'
              732  LOAD_ATTR                _global_over
              734  LOAD_METHOD              set
              736  CALL_METHOD_0         0  ''
              738  POP_TOP          

 L. 210       740  LOAD_GLOBAL              log
              742  LOAD_METHOD              debug
              744  LOAD_STR                 'Global rate limit is now over.'
              746  CALL_METHOD_1         1  ''
              748  POP_TOP          
            750_0  COME_FROM           726  '726'

 L. 212       750  POP_BLOCK        
              752  BEGIN_FINALLY    
              754  WITH_CLEANUP_START
              756  GET_AWAITABLE    
              758  LOAD_CONST               None
              760  YIELD_FROM       
              762  WITH_CLEANUP_FINISH
              764  POP_FINALLY           0  ''
          766_768  JUMP_BACK           314  'to 314'
            770_0  COME_FROM           600  '600'

 L. 215       770  LOAD_FAST                'r'
              772  LOAD_ATTR                status
              774  LOAD_CONST               {500, 502}
              776  COMPARE_OP               in
          778_780  POP_JUMP_IF_FALSE   826  'to 826'

 L. 216       782  LOAD_GLOBAL              asyncio
              784  LOAD_METHOD              sleep
              786  LOAD_CONST               1
              788  LOAD_FAST                'tries'
              790  LOAD_CONST               2
              792  BINARY_MULTIPLY  
              794  BINARY_ADD       
              796  CALL_METHOD_1         1  ''
              798  GET_AWAITABLE    
              800  LOAD_CONST               None
              802  YIELD_FROM       
              804  POP_TOP          

 L. 217       806  POP_BLOCK        
              808  BEGIN_FINALLY    
              810  WITH_CLEANUP_START
              812  GET_AWAITABLE    
              814  LOAD_CONST               None
              816  YIELD_FROM       
              818  WITH_CLEANUP_FINISH
              820  POP_FINALLY           0  ''
          822_824  JUMP_BACK           314  'to 314'
            826_0  COME_FROM           778  '778'

 L. 220       826  LOAD_FAST                'r'
              828  LOAD_ATTR                status
              830  LOAD_CONST               403
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   850  'to 850'

 L. 221       838  LOAD_GLOBAL              Forbidden
              840  LOAD_FAST                'r'
              842  LOAD_FAST                'data'
              844  CALL_FUNCTION_2       2  ''
              846  RAISE_VARARGS_1       1  'exception instance'
              848  JUMP_FORWARD        884  'to 884'
            850_0  COME_FROM           834  '834'

 L. 222       850  LOAD_FAST                'r'
              852  LOAD_ATTR                status
              854  LOAD_CONST               404
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   874  'to 874'

 L. 223       862  LOAD_GLOBAL              NotFound
              864  LOAD_FAST                'r'
              866  LOAD_FAST                'data'
              868  CALL_FUNCTION_2       2  ''
              870  RAISE_VARARGS_1       1  'exception instance'
              872  JUMP_FORWARD        884  'to 884'
            874_0  COME_FROM           858  '858'

 L. 225       874  LOAD_GLOBAL              HTTPException
              876  LOAD_FAST                'r'
              878  LOAD_FAST                'data'
              880  CALL_FUNCTION_2       2  ''
              882  RAISE_VARARGS_1       1  'exception instance'
            884_0  COME_FROM           872  '872'
            884_1  COME_FROM           848  '848'
              884  POP_BLOCK        
              886  BEGIN_FINALLY    
            888_0  COME_FROM_ASYNC_WITH   374  '374'
              888  WITH_CLEANUP_START
              890  GET_AWAITABLE    
              892  LOAD_CONST               None
              894  YIELD_FROM       
              896  WITH_CLEANUP_FINISH
              898  END_FINALLY      
          900_902  JUMP_BACK           314  'to 314'

 L. 228       904  LOAD_GLOBAL              HTTPException
              906  LOAD_FAST                'r'
              908  LOAD_FAST                'data'
              910  CALL_FUNCTION_2       2  ''
              912  RAISE_VARARGS_1       1  'exception instance'
              914  POP_BLOCK        
              916  BEGIN_FINALLY    
            918_0  COME_FROM_WITH      300  '300'
              918  WITH_CLEANUP_START
              920  WITH_CLEANUP_FINISH
              922  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 558

    async def get_from_cdn--- This code section failed: ---

 L. 231         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _HTTPClient__session
                4  LOAD_METHOD              get
                6  LOAD_FAST                'url'
                8  CALL_METHOD_1         1  ''
               10  BEFORE_ASYNC_WITH
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  SETUP_ASYNC_WITH    122  'to 122'
               20  STORE_FAST               'resp'

 L. 232        22  LOAD_FAST                'resp'
               24  LOAD_ATTR                status
               26  LOAD_CONST               200
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    64  'to 64'

 L. 233        32  LOAD_FAST                'resp'
               34  LOAD_METHOD              read
               36  CALL_METHOD_0         0  ''
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            30  '30'

 L. 234        64  LOAD_FAST                'resp'
               66  LOAD_ATTR                status
               68  LOAD_CONST               404
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 235        74  LOAD_GLOBAL              NotFound
               76  LOAD_FAST                'resp'
               78  LOAD_STR                 'asset not found'
               80  CALL_FUNCTION_2       2  ''
               82  RAISE_VARARGS_1       1  'exception instance'
               84  JUMP_FORWARD        118  'to 118'
             86_0  COME_FROM            72  '72'

 L. 236        86  LOAD_FAST                'resp'
               88  LOAD_ATTR                status
               90  LOAD_CONST               403
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 237        96  LOAD_GLOBAL              Forbidden
               98  LOAD_FAST                'resp'
              100  LOAD_STR                 'cannot retrieve asset'
              102  CALL_FUNCTION_2       2  ''
              104  RAISE_VARARGS_1       1  'exception instance'
              106  JUMP_FORWARD        118  'to 118'
            108_0  COME_FROM            94  '94'

 L. 239       108  LOAD_GLOBAL              HTTPException
              110  LOAD_FAST                'resp'
              112  LOAD_STR                 'failed to get asset'
              114  CALL_FUNCTION_2       2  ''
              116  RAISE_VARARGS_1       1  'exception instance'
            118_0  COME_FROM           106  '106'
            118_1  COME_FROM            84  '84'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_ASYNC_WITH    18  '18'
              122  WITH_CLEANUP_START
              124  GET_AWAITABLE    
              126  LOAD_CONST               None
              128  YIELD_FROM       
              130  WITH_CLEANUP_FINISH
              132  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 46

    async def close(self):
        if self._HTTPClient__session:
            await self._HTTPClient__session.close()

    def _token(self, token, *, bot=True):
        self.token = token
        self.bot_token = bot
        self._ack_token = None

    async def static_login(self, token, *, bot):
        self._HTTPClient__session = aiohttp.ClientSession(connector=(self.connector))
        old_token, old_bot = self.token, self.bot_token
        self._token(token, bot=bot)
        try:
            data = await self.request(Route('GET', '/users/@me'))
        except HTTPException as exc:
            try:
                self._token(old_token, bot=old_bot)
                if exc.response.status == 401:
                    raise LoginFailure('Improper token has been passed.') from exc
                raise
            finally:
                exc = None
                del exc

        else:
            return data

    def logout(self):
        return self.request(Route('POST', '/auth/logout'))

    def start_group(self, user_id, recipients):
        payload = {'recipients': recipients}
        return self.request(Route('POST', '/users/{user_id}/channels', user_id=user_id), json=payload)

    def leave_group(self, channel_id):
        return self.request(Route('DELETE', '/channels/{channel_id}', channel_id=channel_id))

    def add_group_recipient(self, channel_id, user_id):
        r = Route('PUT', '/channels/{channel_id}/recipients/{user_id}', channel_id=channel_id, user_id=user_id)
        return self.request(r)

    def remove_group_recipient(self, channel_id, user_id):
        r = Route('DELETE', '/channels/{channel_id}/recipients/{user_id}', channel_id=channel_id, user_id=user_id)
        return self.request(r)

    def edit_group--- This code section failed: ---

 L. 294         0  LOAD_CONST               ('name', 'icon')
                2  STORE_DEREF              'valid_keys'

 L. 295         4  LOAD_CLOSURE             'valid_keys'
                6  BUILD_TUPLE_1         1 
                8  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               10  LOAD_STR                 'HTTPClient.edit_group.<locals>.<dictcomp>'
               12  MAKE_FUNCTION_8          'closure'

 L. 296        14  LOAD_FAST                'options'
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''

 L. 295        20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'payload'

 L. 299        26  LOAD_FAST                'self'
               28  LOAD_ATTR                request
               30  LOAD_GLOBAL              Route
               32  LOAD_STR                 'PATCH'
               34  LOAD_STR                 '/channels/{channel_id}'
               36  LOAD_FAST                'channel_id'
               38  LOAD_CONST               ('channel_id',)
               40  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               42  LOAD_FAST                'payload'
               44  LOAD_CONST               ('json',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 8

    def convert_group(self, channel_id):
        return self.request(Route('POST', '/channels/{channel_id}/convert', channel_id=channel_id))

    def start_private_message(self, user_id):
        payload = {'recipient_id': user_id}
        return self.request((Route('POST', '/users/@me/channels')), json=payload)

    def send_message(self, channel_id, content, *, tts=False, embed=None, nonce=None):
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
        payload = {}
        if content:
            payload['content'] = content
        if tts:
            payload['tts'] = True
        if embed:
            payload['embed'] = embed
        if nonce:
            payload['nonce'] = nonce
        return self.request(r, json=payload)

    def send_typing(self, channel_id):
        return self.request(Route('POST', '/channels/{channel_id}/typing', channel_id=channel_id))

    def send_files(self, channel_id, *, files, content=None, tts=False, embed=None, nonce=None):
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)
        form = aiohttp.FormData()
        payload = {'tts': tts}
        if content:
            payload['content'] = content
        if embed:
            payload['embed'] = embed
        if nonce:
            payload['nonce'] = nonce
        form.add_field'payload_json'utils.to_json(payload)
        if len(files) == 1:
            file = files[0]
            form.add_field('file', (file.fp), filename=(file.filename), content_type='application/octet-stream')
        else:
            for index, file in enumerate(files):
                form.add_field(('file%s' % index), (file.fp), filename=(file.filename), content_type='application/octet-stream')
            else:
                return self.request(r, data=form, files=files)

    async def ack_message(self, channel_id, message_id):
        r = Route('POST', '/channels/{channel_id}/messages/{message_id}/ack', channel_id=channel_id, message_id=message_id)
        data = await self.request(r, json={'token': self._ack_token})
        self._ack_token = data['token']

    def ack_guild(self, guild_id):
        return self.request(Route('POST', '/guilds/{guild_id}/ack', guild_id=guild_id))

    def delete_message(self, channel_id, message_id, *, reason=None):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r, reason=reason)

    def delete_messages(self, channel_id, message_ids, *, reason=None):
        r = Route('POST', '/channels/{channel_id}/messages/bulk_delete', channel_id=channel_id)
        payload = {'messages': message_ids}
        return self.request(r, json=payload, reason=reason)

    def edit_message(self, channel_id, message_id, **fields):
        r = Route('PATCH', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r, json=fields)

    def add_reaction(self, channel_id, message_id, emoji):
        r = Route('PUT', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', channel_id=channel_id,
          message_id=message_id,
          emoji=emoji)
        return self.request(r)

    def remove_reaction(self, channel_id, message_id, emoji, member_id):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{member_id}', channel_id=channel_id,
          message_id=message_id,
          member_id=member_id,
          emoji=emoji)
        return self.request(r)

    def remove_own_reaction(self, channel_id, message_id, emoji):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', channel_id=channel_id,
          message_id=message_id,
          emoji=emoji)
        return self.request(r)

    def get_reaction_users(self, channel_id, message_id, emoji, limit, after=None):
        r = Route('GET', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}', channel_id=channel_id,
          message_id=message_id,
          emoji=emoji)
        params = {'limit': limit}
        if after:
            params['after'] = after
        return self.request(r, params=params)

    def clear_reactions(self, channel_id, message_id):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions', channel_id=channel_id,
          message_id=message_id)
        return self.request(r)

    def clear_single_reaction(self, channel_id, message_id, emoji):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}', channel_id=channel_id,
          message_id=message_id,
          emoji=emoji)
        return self.request(r)

    def get_message(self, channel_id, message_id):
        r = Route('GET', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r)

    def get_channel(self, channel_id):
        r = Route('GET', '/channels/{channel_id}', channel_id=channel_id)
        return self.request(r)

    def logs_from(self, channel_id, limit, before=None, after=None, around=None):
        params = {'limit': limit}
        if before is not None:
            params['before'] = before
        if after is not None:
            params['after'] = after
        if around is not None:
            params['around'] = around
        return self.request(Route('GET', '/channels/{channel_id}/messages', channel_id=channel_id), params=params)

    def publish_message(self, channel_id, message_id):
        return self.request(Route('POST', '/channels/{channel_id}/messages/{message_id}/crosspost', channel_id=channel_id,
          message_id=message_id))

    def pin_message(self, channel_id, message_id):
        return self.request(Route('PUT', '/channels/{channel_id}/pins/{message_id}', channel_id=channel_id,
          message_id=message_id))

    def unpin_message(self, channel_id, message_id):
        return self.request(Route('DELETE', '/channels/{channel_id}/pins/{message_id}', channel_id=channel_id,
          message_id=message_id))

    def pins_from(self, channel_id):
        return self.request(Route('GET', '/channels/{channel_id}/pins', channel_id=channel_id))

    def kick(self, user_id, guild_id, reason=None):
        r = Route('DELETE', '/guilds/{guild_id}/members/{user_id}', guild_id=guild_id, user_id=user_id)
        if reason:
            r.url = '{0.url}?reason={1}'.formatr_uriquote(reason)
        return self.request(r)

    def ban(self, user_id, guild_id, delete_message_days=1, reason=None):
        r = Route('PUT', '/guilds/{guild_id}/bans/{user_id}', guild_id=guild_id, user_id=user_id)
        params = {'delete-message-days': delete_message_days}
        if reason:
            r.url = '{0.url}?reason={1}'.formatr_uriquote(reason)
        return self.request(r, params=params)

    def unban(self, user_id, guild_id, *, reason=None):
        r = Route('DELETE', '/guilds/{guild_id}/bans/{user_id}', guild_id=guild_id, user_id=user_id)
        return self.request(r, reason=reason)

    def guild_voice_state(self, user_id, guild_id, *, mute=None, deafen=None, reason=None):
        r = Route('PATCH', '/guilds/{guild_id}/members/{user_id}', guild_id=guild_id, user_id=user_id)
        payload = {}
        if mute is not None:
            payload['mute'] = mute
        if deafen is not None:
            payload['deaf'] = deafen
        return self.request(r, json=payload, reason=reason)

    def edit_profile(self, password, username, avatar, **fields):
        payload = {'password':password, 
         'username':username, 
         'avatar':avatar}
        if 'email' in fields:
            payload['email'] = fields['email']
        if 'new_password' in fields:
            payload['new_password'] = fields['new_password']
        return self.request((Route('PATCH', '/users/@me')), json=payload)

    def change_my_nickname(self, guild_id, nickname, *, reason=None):
        r = Route('PATCH', '/guilds/{guild_id}/members/@me/nick', guild_id=guild_id)
        payload = {'nick': nickname}
        return self.request(r, json=payload, reason=reason)

    def change_nickname(self, guild_id, user_id, nickname, *, reason=None):
        r = Route('PATCH', '/guilds/{guild_id}/members/{user_id}', guild_id=guild_id, user_id=user_id)
        payload = {'nick': nickname}
        return self.request(r, json=payload, reason=reason)

    def edit_member(self, guild_id, user_id, *, reason=None, **fields):
        r = Route('PATCH', '/guilds/{guild_id}/members/{user_id}', guild_id=guild_id, user_id=user_id)
        return self.request(r, json=fields, reason=reason)

    def edit_channel--- This code section failed: ---

 L. 525         0  LOAD_GLOBAL              Route
                2  LOAD_STR                 'PATCH'
                4  LOAD_STR                 '/channels/{channel_id}'
                6  LOAD_FAST                'channel_id'
                8  LOAD_CONST               ('channel_id',)
               10  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               12  STORE_FAST               'r'

 L. 526        14  LOAD_CONST               ('name', 'parent_id', 'topic', 'bitrate', 'nsfw', 'user_limit', 'position', 'permission_overwrites', 'rate_limit_per_user')
               16  STORE_DEREF              'valid_keys'

 L. 528        18  LOAD_CLOSURE             'valid_keys'
               20  BUILD_TUPLE_1         1 
               22  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               24  LOAD_STR                 'HTTPClient.edit_channel.<locals>.<dictcomp>'
               26  MAKE_FUNCTION_8          'closure'

 L. 529        28  LOAD_FAST                'options'
               30  LOAD_METHOD              items
               32  CALL_METHOD_0         0  ''

 L. 528        34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'payload'

 L. 532        40  LOAD_FAST                'self'
               42  LOAD_ATTR                request
               44  LOAD_FAST                'r'
               46  LOAD_FAST                'reason'
               48  LOAD_FAST                'payload'
               50  LOAD_CONST               ('reason', 'json')
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 22

    def bulk_channel_update(self, guild_id, data, *, reason=None):
        r = Route('PATCH', '/guilds/{guild_id}/channels', guild_id=guild_id)
        return self.request(r, json=data, reason=reason)

    def create_channel--- This code section failed: ---

 L. 540         0  LOAD_STR                 'type'

 L. 540         2  LOAD_FAST                'channel_type'

 L. 539         4  BUILD_MAP_1           1 
                6  STORE_FAST               'payload'

 L. 543         8  LOAD_CONST               ('name', 'parent_id', 'topic', 'bitrate', 'nsfw', 'user_limit', 'position', 'permission_overwrites', 'rate_limit_per_user')
               10  STORE_DEREF              'valid_keys'

 L. 545        12  LOAD_FAST                'payload'
               14  LOAD_METHOD              update
               16  LOAD_CLOSURE             'valid_keys'
               18  BUILD_TUPLE_1         1 
               20  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               22  LOAD_STR                 'HTTPClient.create_channel.<locals>.<dictcomp>'
               24  MAKE_FUNCTION_8          'closure'

 L. 546        26  LOAD_FAST                'options'
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  ''

 L. 545        32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 549        40  LOAD_FAST                'self'
               42  LOAD_ATTR                request
               44  LOAD_GLOBAL              Route
               46  LOAD_STR                 'POST'
               48  LOAD_STR                 '/guilds/{guild_id}/channels'
               50  LOAD_FAST                'guild_id'
               52  LOAD_CONST               ('guild_id',)
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  LOAD_FAST                'payload'
               58  LOAD_FAST                'reason'
               60  LOAD_CONST               ('json', 'reason')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 20

    def delete_channel(self, channel_id, *, reason=None):
        return self.request(Route('DELETE', '/channels/{channel_id}', channel_id=channel_id), reason=reason)

    def create_webhook(self, channel_id, *, name, avatar=None, reason=None):
        payload = {'name': name}
        if avatar is not None:
            payload['avatar'] = avatar
        r = Route('POST', '/channels/{channel_id}/webhooks', channel_id=channel_id)
        return self.request(r, json=payload, reason=reason)

    def channel_webhooks(self, channel_id):
        return self.request(Route('GET', '/channels/{channel_id}/webhooks', channel_id=channel_id))

    def guild_webhooks(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/webhooks', guild_id=guild_id))

    def get_webhook(self, webhook_id):
        return self.request(Route('GET', '/webhooks/{webhook_id}', webhook_id=webhook_id))

    def follow_webhook(self, channel_id, webhook_channel_id):
        payload = {'webhook_channel_id': str(webhook_channel_id)}
        return self.request(Route('POST', '/channels/{channel_id}/followers', channel_id=channel_id), json=payload)

    def get_guilds(self, limit, before=None, after=None):
        params = {'limit': limit}
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        return self.request((Route('GET', '/users/@me/guilds')), params=params)

    def leave_guild(self, guild_id):
        return self.request(Route('DELETE', '/users/@me/guilds/{guild_id}', guild_id=guild_id))

    def get_guild(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}', guild_id=guild_id))

    def delete_guild(self, guild_id):
        return self.request(Route('DELETE', '/guilds/{guild_id}', guild_id=guild_id))

    def create_guild(self, name, region, icon):
        payload = {'name':name, 
         'icon':icon, 
         'region':region}
        return self.request((Route('POST', '/guilds')), json=payload)

    def edit_guild--- This code section failed: ---

 L. 614         0  LOAD_CONST               ('name', 'region', 'icon', 'afk_timeout', 'owner_id', 'afk_channel_id', 'splash', 'verification_level', 'system_channel_id', 'default_message_notifications', 'description', 'explicit_content_filter', 'banner', 'system_channel_flags')
                2  STORE_DEREF              'valid_keys'

 L. 620         4  LOAD_CLOSURE             'valid_keys'
                6  BUILD_TUPLE_1         1 
                8  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               10  LOAD_STR                 'HTTPClient.edit_guild.<locals>.<dictcomp>'
               12  MAKE_FUNCTION_8          'closure'

 L. 621        14  LOAD_FAST                'fields'
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''

 L. 620        20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'payload'

 L. 624        26  LOAD_FAST                'self'
               28  LOAD_ATTR                request
               30  LOAD_GLOBAL              Route
               32  LOAD_STR                 'PATCH'
               34  LOAD_STR                 '/guilds/{guild_id}'
               36  LOAD_FAST                'guild_id'
               38  LOAD_CONST               ('guild_id',)
               40  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               42  LOAD_FAST                'payload'
               44  LOAD_FAST                'reason'
               46  LOAD_CONST               ('json', 'reason')
               48  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 8

    def get_bans(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/bans', guild_id=guild_id))

    def get_ban(self, user_id, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/bans/{user_id}', guild_id=guild_id, user_id=user_id))

    def get_vanity_code(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/vanity-url', guild_id=guild_id))

    def change_vanity_code(self, guild_id, code, *, reason=None):
        payload = {'code': code}
        return self.request(Route('PATCH', '/guilds/{guild_id}/vanity-url', guild_id=guild_id), json=payload, reason=reason)

    def get_all_guild_channels(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/channels', guild_id=guild_id))

    def get_members(self, guild_id, limit, after):
        params = {'limit': limit}
        if after:
            params['after'] = after
        r = Route('GET', '/guilds/{guild_id}/members', guild_id=guild_id)
        return self.request(r, params=params)

    def get_member(self, guild_id, member_id):
        return self.request(Route('GET', '/guilds/{guild_id}/members/{member_id}', guild_id=guild_id, member_id=member_id))

    def prune_members(self, guild_id, days, compute_prune_count, *, reason=None):
        params = {'days':days, 
         'compute_prune_count':'true' if compute_prune_count else 'false'}
        return self.request(Route('POST', '/guilds/{guild_id}/prune', guild_id=guild_id), params=params, reason=reason)

    def estimate_pruned_members(self, guild_id, days):
        params = {'days': days}
        return self.request(Route('GET', '/guilds/{guild_id}/prune', guild_id=guild_id), params=params)

    def get_all_custom_emojis(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/emojis', guild_id=guild_id))

    def get_custom_emoji(self, guild_id, emoji_id):
        return self.request(Route('GET', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id))

    def create_custom_emoji(self, guild_id, name, image, *, roles=None, reason=None):
        payload = {'name':name, 
         'image':image, 
         'roles':roles or []}
        r = Route('POST', '/guilds/{guild_id}/emojis', guild_id=guild_id)
        return self.request(r, json=payload, reason=reason)

    def delete_custom_emoji(self, guild_id, emoji_id, *, reason=None):
        r = Route('DELETE', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id)
        return self.request(r, reason=reason)

    def edit_custom_emoji(self, guild_id, emoji_id, *, name, roles=None, reason=None):
        payload = {'name':name, 
         'roles':roles or []}
        r = Route('PATCH', '/guilds/{guild_id}/emojis/{emoji_id}', guild_id=guild_id, emoji_id=emoji_id)
        return self.request(r, json=payload, reason=reason)

    def get_audit_logs(self, guild_id, limit=100, before=None, after=None, user_id=None, action_type=None):
        params = {'limit': limit}
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if user_id:
            params['user_id'] = user_id
        if action_type:
            params['action_type'] = action_type
        r = Route('GET', '/guilds/{guild_id}/audit-logs', guild_id=guild_id)
        return self.request(r, params=params)

    def get_widget(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/widget.json', guild_id=guild_id))

    def create_invite(self, channel_id, *, reason=None, **options):
        r = Route('POST', '/channels/{channel_id}/invites', channel_id=channel_id)
        payload = {'max_age':options.get'max_age'0, 
         'max_uses':options.get'max_uses'0, 
         'temporary':options.get'temporary'False, 
         'unique':options.get'unique'True}
        return self.request(r, reason=reason, json=payload)

    def get_invite(self, invite_id, *, with_counts=True):
        params = {'with_counts': int(with_counts)}
        return self.request(Route('GET', '/invite/{invite_id}', invite_id=invite_id), params=params)

    def invites_from(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/invites', guild_id=guild_id))

    def invites_from_channel(self, channel_id):
        return self.request(Route('GET', '/channels/{channel_id}/invites', channel_id=channel_id))

    def delete_invite(self, invite_id, *, reason=None):
        return self.request(Route('DELETE', '/invite/{invite_id}', invite_id=invite_id), reason=reason)

    def get_roles(self, guild_id):
        return self.request(Route('GET', '/guilds/{guild_id}/roles', guild_id=guild_id))

    def edit_role--- This code section failed: ---

 L. 747         0  LOAD_GLOBAL              Route
                2  LOAD_STR                 'PATCH'
                4  LOAD_STR                 '/guilds/{guild_id}/roles/{role_id}'
                6  LOAD_FAST                'guild_id'
                8  LOAD_FAST                'role_id'
               10  LOAD_CONST               ('guild_id', 'role_id')
               12  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               14  STORE_FAST               'r'

 L. 748        16  LOAD_CONST               ('name', 'permissions', 'color', 'hoist', 'mentionable')
               18  STORE_DEREF              'valid_keys'

 L. 749        20  LOAD_CLOSURE             'valid_keys'
               22  BUILD_TUPLE_1         1 
               24  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               26  LOAD_STR                 'HTTPClient.edit_role.<locals>.<dictcomp>'
               28  MAKE_FUNCTION_8          'closure'

 L. 750        30  LOAD_FAST                'fields'
               32  LOAD_METHOD              items
               34  CALL_METHOD_0         0  ''

 L. 749        36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'payload'

 L. 752        42  LOAD_FAST                'self'
               44  LOAD_ATTR                request
               46  LOAD_FAST                'r'
               48  LOAD_FAST                'payload'
               50  LOAD_FAST                'reason'
               52  LOAD_CONST               ('json', 'reason')
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 24

    def delete_role(self, guild_id, role_id, *, reason=None):
        r = Route('DELETE', '/guilds/{guild_id}/roles/{role_id}', guild_id=guild_id, role_id=role_id)
        return self.request(r, reason=reason)

    def replace_roles(self, user_id, guild_id, role_ids, *, reason=None):
        return self.edit_member(guild_id=guild_id, user_id=user_id, roles=role_ids, reason=reason)

    def create_role(self, guild_id, *, reason=None, **fields):
        r = Route('POST', '/guilds/{guild_id}/roles', guild_id=guild_id)
        return self.request(r, json=fields, reason=reason)

    def move_role_position(self, guild_id, positions, *, reason=None):
        r = Route('PATCH', '/guilds/{guild_id}/roles', guild_id=guild_id)
        return self.request(r, json=positions, reason=reason)

    def add_role(self, guild_id, user_id, role_id, *, reason=None):
        r = Route('PUT', '/guilds/{guild_id}/members/{user_id}/roles/{role_id}', guild_id=guild_id,
          user_id=user_id,
          role_id=role_id)
        return self.request(r, reason=reason)

    def remove_role(self, guild_id, user_id, role_id, *, reason=None):
        r = Route('DELETE', '/guilds/{guild_id}/members/{user_id}/roles/{role_id}', guild_id=guild_id,
          user_id=user_id,
          role_id=role_id)
        return self.request(r, reason=reason)

    def edit_channel_permissions(self, channel_id, target, allow, deny, type, *, reason=None):
        payload = {'id':target, 
         'allow':allow, 
         'deny':deny, 
         'type':type}
        r = Route('PUT', '/channels/{channel_id}/permissions/{target}', channel_id=channel_id, target=target)
        return self.request(r, json=payload, reason=reason)

    def delete_channel_permissions(self, channel_id, target, *, reason=None):
        r = Route('DELETE', '/channels/{channel_id}/permissions/{target}', channel_id=channel_id, target=target)
        return self.request(r, reason=reason)

    def move_member(self, user_id, guild_id, channel_id, *, reason=None):
        return self.edit_member(guild_id=guild_id, user_id=user_id, channel_id=channel_id, reason=reason)

    def remove_relationship(self, user_id):
        r = Route('DELETE', '/users/@me/relationships/{user_id}', user_id=user_id)
        return self.request(r)

    def add_relationship(self, user_id, type=None):
        r = Route('PUT', '/users/@me/relationships/{user_id}', user_id=user_id)
        payload = {}
        if type is not None:
            payload['type'] = type
        return self.request(r, json=payload)

    def send_friend_request(self, username, discriminator):
        r = Route('POST', '/users/@me/relationships')
        payload = {'username':username, 
         'discriminator':int(discriminator)}
        return self.request(r, json=payload)

    def application_info(self):
        return self.request(Route('GET', '/oauth2/applications/@me'))

    async def get_gateway(self, *, encoding='json', v=6, zlib=True):
        try:
            data = await self.request(Route('GET', '/gateway'))
        except HTTPException as exc:
            try:
                raise GatewayNotFound() from exc
            finally:
                exc = None
                del exc

        else:
            if zlib:
                value = '{0}?encoding={1}&v={2}&compress=zlib-stream'
            else:
                value = '{0}?encoding={1}&v={2}'
            return value.format(data['url'], encoding, v)

    async def get_bot_gateway(self, *, encoding='json', v=6, zlib=True):
        try:
            data = await self.request(Route('GET', '/gateway/bot'))
        except HTTPException as exc:
            try:
                raise GatewayNotFound() from exc
            finally:
                exc = None
                del exc

        else:
            if zlib:
                value = '{0}?encoding={1}&v={2}&compress=zlib-stream'
            else:
                value = '{0}?encoding={1}&v={2}'
            return (
             data['shards'], value.format(data['url'], encoding, v))

    def get_user(self, user_id):
        return self.request(Route('GET', '/users/{user_id}', user_id=user_id))

    def get_user_profile(self, user_id):
        return self.request(Route('GET', '/users/{user_id}/profile', user_id=user_id))

    def get_mutual_friends(self, user_id):
        return self.request(Route('GET', '/users/{user_id}/relationships', user_id=user_id))

    def change_hypesquad_house(self, house_id):
        payload = {'house_id': house_id}
        return self.request((Route('POST', '/hypesquad/online')), json=payload)

    def leave_hypesquad_house(self):
        return self.request(Route('DELETE', '/hypesquad/online'))

    def edit_settings(self, **payload):
        return self.request((Route('PATCH', '/users/@me/settings')), json=payload)