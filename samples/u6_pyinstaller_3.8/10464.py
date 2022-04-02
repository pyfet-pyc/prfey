# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: fake_useragent\utils.py
from __future__ import absolute_import, unicode_literals
import contextlib, inspect, io, json, os, re, ssl
from fake_useragent.log import logger
try:
    from urllib2 import urlopen, Request, URLError
    from urllib import quote_plus
    str_types = (
     unicode, str)
    text = unicode
except ImportError:
    from urllib.request import urlopen, Request
    from urllib.parse import quote_plus
    from urllib.error import URLError
    str_types = (
     str,)
    text = str

try:
    import socket, gevent.socket
    if socket.socket is gevent.socket.socket:
        from gevent import sleep
    else:
        from time import sleep
except (ImportError, AttributeError):
    from time import sleep
else:
    try:
        urlopen_args = inspect.getfullargspec(urlopen).kwonlyargs
    except AttributeError:
        urlopen_args = inspect.getargspec(urlopen).args
    else:
        urlopen_has_ssl_context = 'context' in urlopen_args

        def get--- This code section failed: ---

 L.  50         0  LOAD_CONST               0
                2  STORE_FAST               'attempt'

 L.  53         4  LOAD_GLOBAL              Request
                6  LOAD_FAST                'url'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'request'

 L.  55        12  LOAD_FAST                'attempt'
               14  LOAD_CONST               1
               16  INPLACE_ADD      
               18  STORE_FAST               'attempt'

 L.  57        20  SETUP_FINALLY       152  'to 152'

 L.  58        22  LOAD_GLOBAL              urlopen_has_ssl_context
               24  POP_JUMP_IF_FALSE    98  'to 98'

 L.  59        26  LOAD_FAST                'verify_ssl'
               28  POP_JUMP_IF_TRUE     40  'to 40'

 L.  60        30  LOAD_GLOBAL              ssl
               32  LOAD_METHOD              _create_unverified_context
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'context'
               38  JUMP_FORWARD         44  'to 44'
             40_0  COME_FROM            28  '28'

 L.  62        40  LOAD_CONST               None
               42  STORE_FAST               'context'
             44_0  COME_FROM            38  '38'

 L.  64        44  LOAD_GLOBAL              contextlib
               46  LOAD_METHOD              closing
               48  LOAD_GLOBAL              urlopen

 L.  65        50  LOAD_FAST                'request'

 L.  66        52  LOAD_GLOBAL              settings
               54  LOAD_ATTR                HTTP_TIMEOUT

 L.  67        56  LOAD_FAST                'context'

 L.  64        58  LOAD_CONST               ('timeout', 'context')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  CALL_METHOD_1         1  ''
               64  SETUP_WITH           90  'to 90'

 L.  68        66  STORE_FAST               'response'

 L.  69        68  LOAD_FAST                'response'
               70  LOAD_METHOD              read
               72  CALL_METHOD_0         0  ''
               74  POP_BLOCK        
               76  ROT_TWO          
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_WITH       64  '64'
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  END_FINALLY      
               96  JUMP_FORWARD        148  'to 148'
             98_0  COME_FROM            24  '24'

 L.  71        98  LOAD_GLOBAL              contextlib
              100  LOAD_METHOD              closing
              102  LOAD_GLOBAL              urlopen

 L.  72       104  LOAD_FAST                'request'

 L.  73       106  LOAD_GLOBAL              settings
              108  LOAD_ATTR                HTTP_TIMEOUT

 L.  71       110  LOAD_CONST               ('timeout',)
              112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              114  CALL_METHOD_1         1  ''
              116  SETUP_WITH          142  'to 142'

 L.  74       118  STORE_FAST               'response'

 L.  75       120  LOAD_FAST                'response'
              122  LOAD_METHOD              read
              124  CALL_METHOD_0         0  ''
              126  POP_BLOCK        
              128  ROT_TWO          
              130  BEGIN_FINALLY    
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  POP_FINALLY           0  ''
              138  POP_BLOCK        
              140  RETURN_VALUE     
            142_0  COME_FROM_WITH      116  '116'
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  END_FINALLY      
            148_0  COME_FROM            96  '96'
              148  POP_BLOCK        
              150  JUMP_BACK             4  'to 4'
            152_0  COME_FROM_FINALLY    20  '20'

 L.  76       152  DUP_TOP          
              154  LOAD_GLOBAL              URLError
              156  LOAD_GLOBAL              OSError
              158  BUILD_TUPLE_2         2 
              160  COMPARE_OP               exception-match
          162_164  POP_JUMP_IF_FALSE   250  'to 250'
              166  POP_TOP          
              168  STORE_FAST               'exc'
              170  POP_TOP          
              172  SETUP_FINALLY       238  'to 238'

 L.  77       174  LOAD_GLOBAL              logger
              176  LOAD_ATTR                debug

 L.  78       178  LOAD_STR                 'Error occurred during fetching %s'

 L.  79       180  LOAD_FAST                'url'

 L.  80       182  LOAD_FAST                'exc'

 L.  77       184  LOAD_CONST               ('exc_info',)
              186  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              188  POP_TOP          

 L.  83       190  LOAD_FAST                'attempt'
              192  LOAD_GLOBAL              settings
              194  LOAD_ATTR                HTTP_RETRIES
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   210  'to 210'

 L.  84       200  LOAD_GLOBAL              FakeUserAgentError
              202  LOAD_STR                 'Maximum amount of retries reached'
              204  CALL_FUNCTION_1       1  ''
              206  RAISE_VARARGS_1       1  'exception instance'
              208  JUMP_FORWARD        234  'to 234'
            210_0  COME_FROM           198  '198'

 L.  86       210  LOAD_GLOBAL              logger
              212  LOAD_METHOD              debug

 L.  87       214  LOAD_STR                 'Sleeping for %s seconds'

 L.  88       216  LOAD_GLOBAL              settings
              218  LOAD_ATTR                HTTP_DELAY

 L.  86       220  CALL_METHOD_2         2  ''
              222  POP_TOP          

 L.  90       224  LOAD_GLOBAL              sleep
              226  LOAD_GLOBAL              settings
              228  LOAD_ATTR                HTTP_DELAY
              230  CALL_FUNCTION_1       1  ''
              232  POP_TOP          
            234_0  COME_FROM           208  '208'
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_FINALLY   172  '172'
              238  LOAD_CONST               None
              240  STORE_FAST               'exc'
              242  DELETE_FAST              'exc'
              244  END_FINALLY      
              246  POP_EXCEPT       
              248  JUMP_BACK             4  'to 4'
            250_0  COME_FROM           162  '162'
              250  END_FINALLY      
              252  JUMP_BACK             4  'to 4'

Parse error at or near `ROT_TWO' instruction at offset 76


        def get_browsers(verify_ssl=True):
            """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
            html = get((settings.BROWSERS_STATS_PAGE), verify_ssl=verify_ssl)
            html = html.decode('utf-8')
            html = html.split('<table class="w3-table-all notranslate">')[1]
            html = html.split('</table>')[0]
            pattern = '\\.asp">(.+?)<'
            browsers = re.findall(pattern, html, re.UNICODE)
            browsers = [settings.OVERRIDES.getbrowserbrowser for browser in browsers]
            pattern = 'td\\sclass="right">(.+?)\\s'
            browsers_statistics = re.findall(pattern, html, re.UNICODE)
            return list(zip(browsers, browsers_statistics))


        def get_browser_versions(browser, verify_ssl=True):
            """
    very very hardcoded/dirty re/split stuff, but no dependencies
    """
            html = get(settings.BROWSER_BASE_PAGE.format(browser=(quote_plus(browser))),
              verify_ssl=verify_ssl)
            html = html.decode('iso-8859-1')
            html = html.split("<div id='liste'>")[1]
            html = html.split('</div>')[0]
            pattern = "\\?id=\\d+\\'>(.+?)</a"
            browsers_iter = re.finditer(pattern, html, re.UNICODE)
            browsers = []
            for browser in browsers_iter:
                if 'more' in browser.group(1).lower:
                    pass
                else:
                    browsers.append(browser.group(1))
                    if len(browsers) == settings.BROWSERS_COUNT_LIMIT:
                        break
                    if not browsers:
                        raise FakeUserAgentError('No browsers version found for {browser}'.format(browser=browser))
                    return browsers


        def load(use_cache_server=True, verify_ssl=True):
            browsers_dict = {}
            randomize_dict = {}
            try:
                for item in get_browsers(verify_ssl=verify_ssl):
                    browser, percent = item
                    browser_key = browser
                    for value, replacement in settings.REPLACEMENTS.items:
                        browser_key = browser_key.replacevaluereplacement

                else:
                    browser_key = browser_key.lower
                    browsers_dict[browser_key] = get_browser_versions(browser,
                      verify_ssl=verify_ssl)
                    for _ in range(int(float(percent) * 10)):
                        randomize_dict[str(len(randomize_dict))] = browser_key

            except Exception as exc:
                try:
                    if not use_cache_server:
                        raise exc
                    logger.warning('Error occurred during loading data. Trying to use cache server %s',
                      (settings.CACHE_SERVER),
                      exc_info=exc)
                    try:
                        ret = json.loads(get((settings.CACHE_SERVER),
                          verify_ssl=verify_ssl).decode('utf-8'))
                    except (TypeError, ValueError):
                        raise FakeUserAgentError('Can not load data from cache server')

                finally:
                    exc = None
                    del exc

            else:
                ret = {'browsers':browsers_dict, 
                 'randomize':randomize_dict}
            if not isinstance(ret, dict):
                raise FakeUserAgentError('Data is not dictionary ', ret)
            for param in ('browsers', 'randomize'):
                if param not in ret:
                    raise FakeUserAgentError('Missing data param: ', param)
                if not isinstance(ret[param], dict):
                    raise FakeUserAgentError('Data param is not dictionary', ret[param])
                if not ret[param]:
                    raise FakeUserAgentError('Data param is empty', ret[param])
                return ret


        def write(path, data):
            with io.open(path, encoding='utf-8', mode='wt') as (fp):
                dumped = json.dumps(data)
                if not isinstance(dumped, text):
                    dumped = dumped.decode('utf-8')
                fp.write(dumped)


        def read--- This code section failed: ---

 L. 229         0  LOAD_GLOBAL              io
                2  LOAD_ATTR                open
                4  LOAD_FAST                'path'
                6  LOAD_STR                 'utf-8'
                8  LOAD_STR                 'rt'
               10  LOAD_CONST               ('encoding', 'mode')
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  SETUP_WITH           44  'to 44'
               16  STORE_FAST               'fp'

 L. 230        18  LOAD_GLOBAL              json
               20  LOAD_METHOD              loads
               22  LOAD_FAST                'fp'
               24  LOAD_METHOD              read
               26  CALL_METHOD_0         0  ''
               28  CALL_METHOD_1         1  ''
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  POP_FINALLY           0  ''
               42  RETURN_VALUE     
             44_0  COME_FROM_WITH       14  '14'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 32


        def exist(path):
            return os.path.isfile(path)


        def rm(path):
            if exist(path):
                os.remove(path)


        def update(path, use_cache_server=True, verify_ssl=True):
            rm(path)
            write(path, load(use_cache_server=use_cache_server, verify_ssl=verify_ssl))


        def load_cached(path, use_cache_server=True, verify_ssl=True):
            if not exist(path):
                update(path, use_cache_server=use_cache_server, verify_ssl=verify_ssl)
            return read(path)


        from fake_useragent import settings
        from fake_useragent.errors import FakeUserAgentError