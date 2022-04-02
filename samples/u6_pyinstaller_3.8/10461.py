# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: fake_useragent\fake.py
from __future__ import absolute_import, unicode_literals
import random
from threading import Lock
from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger
from fake_useragent.utils import load, load_cached, str_types, update

class FakeUserAgent(object):

    def __init__(self, cache=True, use_cache_server=True, path=settings.DB, fallback=None, verify_ssl=True, safe_attrs=tuple()):
        if not isinstance(cache, bool):
            raise AssertionError('cache must be True or False')
        else:
            self.cache = cache
            assert isinstance(use_cache_server, bool), 'use_cache_server must be True or False'
            self.use_cache_server = use_cache_server
            assert isinstance(path, str_types), 'path must be string or unicode'
            self.path = path
            if fallback is not None:
                assert isinstance(fallback, str_types), 'fallback must be string or unicode'
            self.fallback = fallback
            assert isinstance(verify_ssl, bool), 'verify_ssl must be True or False'
            self.verify_ssl = verify_ssl
            assert isinstance(safe_attrs, (list, set, tuple)), 'safe_attrs must be list\\tuple\\set of strings or unicode'
            if safe_attrs:
                str_types_safe_attrs = [isinstance(attr, str_types) for attr in safe_attrs]
                if not all(str_types_safe_attrs):
                    raise AssertionError('safe_attrs must be list\\tuple\\set of strings or unicode')
        self.safe_attrs = set(safe_attrs)
        self.data = {}
        self.data_randomize = []
        self.data_browsers = {}
        self.load()

    def load(self):
        try:
            with self.load.lock:
                if self.cache:
                    self.data = load_cached((self.path),
                      use_cache_server=(self.use_cache_server),
                      verify_ssl=(self.verify_ssl))
                else:
                    self.data = load(use_cache_server=(self.use_cache_server),
                      verify_ssl=(self.verify_ssl))
                self.data_randomize = list(self.data['randomize'].values())
                self.data_browsers = self.data['browsers']
        except FakeUserAgentError:
            if self.fallback is None:
                raise
            else:
                logger.warning('Error occurred during fetching data, but was suppressed with fallback.')

    load.lock = Lock()

    def update(self, cache=None):
        with self.update.lock:
            if cache is not None:
                assert isinstance(cache, bool), 'cache must be True or False'
                self.cache = cache
            if self.cache:
                update((self.path),
                  use_cache_server=(self.use_cache_server),
                  verify_ssl=(self.verify_ssl))
            self.load()

    update.lock = Lock()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__--- This code section failed: ---

 L. 122         0  LOAD_FAST                'attr'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                safe_attrs
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 123        10  LOAD_GLOBAL              super
               12  LOAD_GLOBAL              UserAgent
               14  LOAD_FAST                'self'
               16  CALL_FUNCTION_2       2  ''
               18  LOAD_METHOD              __getattr__
               20  LOAD_FAST                'attr'
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
             26_0  COME_FROM             8  '8'

 L. 125        26  SETUP_FINALLY       122  'to 122'

 L. 126        28  LOAD_GLOBAL              settings
               30  LOAD_ATTR                REPLACEMENTS
               32  LOAD_METHOD              items
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
               38  FOR_ITER             60  'to 60'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'value'
               44  STORE_FAST               'replacement'

 L. 127        46  LOAD_FAST                'attr'
               48  LOAD_METHOD              replace
               50  LOAD_FAST                'value'
               52  LOAD_FAST                'replacement'
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'attr'
               58  JUMP_BACK            38  'to 38'

 L. 129        60  LOAD_FAST                'attr'
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'attr'

 L. 131        68  LOAD_FAST                'attr'
               70  LOAD_STR                 'random'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L. 132        76  LOAD_GLOBAL              random
               78  LOAD_METHOD              choice
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                data_randomize
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'browser'
               88  JUMP_FORWARD        104  'to 104'
             90_0  COME_FROM            74  '74'

 L. 134        90  LOAD_GLOBAL              settings
               92  LOAD_ATTR                SHORTCUTS
               94  LOAD_METHOD              get
               96  LOAD_FAST                'attr'
               98  LOAD_FAST                'attr'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'browser'
            104_0  COME_FROM            88  '88'

 L. 136       104  LOAD_GLOBAL              random
              106  LOAD_METHOD              choice
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                data_browsers
              112  LOAD_FAST                'browser'
              114  BINARY_SUBSCR    
              116  CALL_METHOD_1         1  ''
              118  POP_BLOCK        
              120  RETURN_VALUE     
            122_0  COME_FROM_FINALLY    26  '26'

 L. 137       122  DUP_TOP          
              124  LOAD_GLOBAL              KeyError
              126  LOAD_GLOBAL              IndexError
              128  BUILD_TUPLE_2         2 
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   184  'to 184'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 138       140  LOAD_FAST                'self'
              142  LOAD_ATTR                fallback
              144  LOAD_CONST               None
              146  COMPARE_OP               is
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L. 139       150  LOAD_GLOBAL              FakeUserAgentError
              152  LOAD_STR                 'Error occurred during getting browser'
              154  CALL_FUNCTION_1       1  ''
              156  RAISE_VARARGS_1       1  'exception instance'
              158  JUMP_FORWARD        180  'to 180'
            160_0  COME_FROM           148  '148'

 L. 141       160  LOAD_GLOBAL              logger
              162  LOAD_METHOD              warning

 L. 142       164  LOAD_STR                 'Error occurred during getting browser, but was suppressed with fallback.'

 L. 141       166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 146       170  LOAD_FAST                'self'
              172  LOAD_ATTR                fallback
              174  ROT_FOUR         
              176  POP_EXCEPT       
              178  RETURN_VALUE     
            180_0  COME_FROM           158  '158'
              180  POP_EXCEPT       
              182  JUMP_FORWARD        186  'to 186'
            184_0  COME_FROM           132  '132'
              184  END_FINALLY      
            186_0  COME_FROM           182  '182'

Parse error at or near `POP_TOP' instruction at offset 136


UserAgent = FakeUserAgent