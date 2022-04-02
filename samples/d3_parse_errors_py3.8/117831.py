# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\aiohttp\worker.py
"""Async gunicorn worker for aiohttp.web"""
import asyncio, os, re, signal, sys
from types import FrameType
from typing import Any, Awaitable, Callable, Optional, Union
import gunicorn.config as GunicornAccessLogFormat
from gunicorn.workers import base
from aiohttp import web
from .helpers import set_result
from .web_app import Application
from .web_log import AccessLogger
try:
    import ssl
    SSLContext = ssl.SSLContext
except ImportError:
    ssl = None
    SSLContext = object
else:
    __all__ = ('GunicornWebWorker', 'GunicornUVLoopWebWorker', 'GunicornTokioWebWorker')

    class GunicornWebWorker(base.Worker):
        DEFAULT_AIOHTTP_LOG_FORMAT = AccessLogger.LOG_FORMAT
        DEFAULT_GUNICORN_LOG_FORMAT = GunicornAccessLogFormat.default

        def __init__(self, *args, **kw):
            (super().__init__)(*args, **kw)
            self._task = None
            self.exit_code = 0
            self._notify_waiter = None

        def init_process(self):
            asyncio.get_event_loop().close()
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            super().init_process()

        def run(self) -> None:
            self._task = self.loop.create_task(self._run())
            try:
                self.loop.run_until_complete(self._task)
            except Exception:
                self.log.exception('Exception in gunicorn worker')
            else:
                if sys.version_info >= (3, 6):
                    self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                self.loop.close()
                sys.exit(self.exit_code)

        async def _run--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                wsgi
                6  LOAD_GLOBAL              Application
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  69        12  LOAD_FAST                'self'
               14  LOAD_ATTR                wsgi
               16  STORE_FAST               'app'
               18  JUMP_FORWARD         64  'to 64'
             20_0  COME_FROM            10  '10'

 L.  70        20  LOAD_GLOBAL              asyncio
               22  LOAD_METHOD              iscoroutinefunction
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                wsgi
               28  CALL_METHOD_1         1  ''
               30  POP_JUMP_IF_FALSE    48  'to 48'

 L.  71        32  LOAD_FAST                'self'
               34  LOAD_METHOD              wsgi
               36  CALL_METHOD_0         0  ''
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  STORE_FAST               'app'
               46  JUMP_FORWARD         64  'to 64'
             48_0  COME_FROM            30  '30'

 L.  73        48  LOAD_GLOBAL              RuntimeError
               50  LOAD_STR                 'wsgi app should be either Application or async function returning Application, got {}'
               52  LOAD_METHOD              format

 L.  75        54  LOAD_FAST                'self'
               56  LOAD_ATTR                wsgi

 L.  73        58  CALL_METHOD_1         1  ''
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            46  '46'
             64_1  COME_FROM            18  '18'

 L.  76        64  LOAD_FAST                'self'
               66  LOAD_ATTR                cfg
               68  LOAD_ATTR                accesslog
               70  POP_JUMP_IF_FALSE    80  'to 80'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                log
               76  LOAD_ATTR                access_log
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            70  '70'
               80  LOAD_CONST               None
             82_0  COME_FROM            78  '78'
               82  STORE_FAST               'access_log'

 L.  77        84  LOAD_GLOBAL              web
               86  LOAD_ATTR                AppRunner
               88  LOAD_FAST                'app'

 L.  78        90  LOAD_FAST                'self'
               92  LOAD_ATTR                log

 L.  79        94  LOAD_FAST                'self'
               96  LOAD_ATTR                cfg
               98  LOAD_ATTR                keepalive

 L.  80       100  LOAD_FAST                'access_log'

 L.  81       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _get_valid_log_format

 L.  82       106  LOAD_FAST                'self'
              108  LOAD_ATTR                cfg
              110  LOAD_ATTR                access_log_format

 L.  81       112  CALL_METHOD_1         1  ''

 L.  77       114  LOAD_CONST               ('logger', 'keepalive_timeout', 'access_log', 'access_log_format')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  STORE_FAST               'runner'

 L.  83       120  LOAD_FAST                'runner'
              122  LOAD_METHOD              setup
              124  CALL_METHOD_0         0  ''
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  POP_TOP          

 L.  85       134  LOAD_FAST                'self'
              136  LOAD_ATTR                cfg
              138  LOAD_ATTR                is_ssl
              140  POP_JUMP_IF_FALSE   154  'to 154'
              142  LOAD_FAST                'self'
              144  LOAD_METHOD              _create_ssl_context
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                cfg
              150  CALL_METHOD_1         1  ''
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           140  '140'
              154  LOAD_CONST               None
            156_0  COME_FROM           152  '152'
              156  STORE_FAST               'ctx'

 L.  87       158  LOAD_FAST                'runner'
              160  STORE_FAST               'runner'

 L.  88       162  LOAD_FAST                'runner'
              164  LOAD_CONST               None
              166  COMPARE_OP               is-not
              168  POP_JUMP_IF_TRUE    174  'to 174'
              170  LOAD_ASSERT              AssertionError
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           168  '168'

 L.  89       174  LOAD_FAST                'runner'
              176  LOAD_ATTR                server
              178  STORE_FAST               'server'

 L.  90       180  LOAD_FAST                'server'
              182  LOAD_CONST               None
              184  COMPARE_OP               is-not
              186  POP_JUMP_IF_TRUE    192  'to 192'
              188  LOAD_ASSERT              AssertionError
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           186  '186'

 L.  91       192  LOAD_FAST                'self'
              194  LOAD_ATTR                sockets
              196  GET_ITER         
            198_0  COME_FROM           246  '246'
              198  FOR_ITER            248  'to 248'
              200  STORE_FAST               'sock'

 L.  92       202  LOAD_GLOBAL              web
              204  LOAD_ATTR                SockSite

 L.  93       206  LOAD_FAST                'runner'

 L.  93       208  LOAD_FAST                'sock'

 L.  93       210  LOAD_FAST                'ctx'

 L.  94       212  LOAD_FAST                'self'
              214  LOAD_ATTR                cfg
              216  LOAD_ATTR                graceful_timeout
              218  LOAD_CONST               100
              220  BINARY_TRUE_DIVIDE
              222  LOAD_CONST               95
              224  BINARY_MULTIPLY  

 L.  92       226  LOAD_CONST               ('ssl_context', 'shutdown_timeout')
              228  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              230  STORE_FAST               'site'

 L.  95       232  LOAD_FAST                'site'
              234  LOAD_METHOD              start
              236  CALL_METHOD_0         0  ''
              238  GET_AWAITABLE    
              240  LOAD_CONST               None
              242  YIELD_FROM       
              244  POP_TOP          
              246  JUMP_BACK           198  'to 198'
            248_0  COME_FROM           198  '198'

 L.  98       248  LOAD_GLOBAL              os
              250  LOAD_METHOD              getpid
              252  CALL_METHOD_0         0  ''
              254  STORE_FAST               'pid'

 L.  99       256  SETUP_FINALLY       400  'to 400'
            258_0  COME_FROM           392  '392'
            258_1  COME_FROM           376  '376'
            258_2  COME_FROM           324  '324'

 L. 100       258  LOAD_FAST                'self'
              260  LOAD_ATTR                alive
          262_264  POP_JUMP_IF_FALSE   396  'to 396'

 L. 101       266  LOAD_FAST                'self'
              268  LOAD_METHOD              notify
              270  CALL_METHOD_0         0  ''
              272  POP_TOP          

 L. 103       274  LOAD_FAST                'server'
              276  LOAD_ATTR                requests_count
              278  STORE_FAST               'cnt'

 L. 104       280  LOAD_FAST                'self'
              282  LOAD_ATTR                cfg
              284  LOAD_ATTR                max_requests
          286_288  POP_JUMP_IF_FALSE   326  'to 326'
              290  LOAD_FAST                'cnt'
              292  LOAD_FAST                'self'
              294  LOAD_ATTR                cfg
              296  LOAD_ATTR                max_requests
              298  COMPARE_OP               >
          300_302  POP_JUMP_IF_FALSE   326  'to 326'

 L. 105       304  LOAD_CONST               False
              306  LOAD_FAST                'self'
              308  STORE_ATTR               alive

 L. 106       310  LOAD_FAST                'self'
              312  LOAD_ATTR                log
              314  LOAD_METHOD              info
              316  LOAD_STR                 'Max requests, shutting down: %s'
              318  LOAD_FAST                'self'
              320  CALL_METHOD_2         2  ''
              322  POP_TOP          
              324  JUMP_BACK           258  'to 258'
            326_0  COME_FROM           300  '300'
            326_1  COME_FROM           286  '286'

 L. 108       326  LOAD_FAST                'pid'
              328  LOAD_GLOBAL              os
              330  LOAD_METHOD              getpid
              332  CALL_METHOD_0         0  ''
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   378  'to 378'
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                ppid
              344  LOAD_GLOBAL              os
              346  LOAD_METHOD              getppid
              348  CALL_METHOD_0         0  ''
              350  COMPARE_OP               !=
          352_354  POP_JUMP_IF_FALSE   378  'to 378'

 L. 109       356  LOAD_CONST               False
              358  LOAD_FAST                'self'
              360  STORE_ATTR               alive

 L. 110       362  LOAD_FAST                'self'
              364  LOAD_ATTR                log
              366  LOAD_METHOD              info
              368  LOAD_STR                 'Parent changed, shutting down: %s'
              370  LOAD_FAST                'self'
              372  CALL_METHOD_2         2  ''
              374  POP_TOP          
              376  JUMP_BACK           258  'to 258'
            378_0  COME_FROM           352  '352'
            378_1  COME_FROM           336  '336'

 L. 112       378  LOAD_FAST                'self'
              380  LOAD_METHOD              _wait_next_notify
              382  CALL_METHOD_0         0  ''
              384  GET_AWAITABLE    
              386  LOAD_CONST               None
              388  YIELD_FROM       
              390  POP_TOP          
          392_394  JUMP_BACK           258  'to 258'
            396_0  COME_FROM           262  '262'
              396  POP_BLOCK        
              398  JUMP_FORWARD        422  'to 422'
            400_0  COME_FROM_FINALLY   256  '256'

 L. 113       400  DUP_TOP          
              402  LOAD_GLOBAL              BaseException
              404  COMPARE_OP               exception-match
          406_408  POP_JUMP_IF_FALSE   420  'to 420'
              410  POP_TOP          
              412  POP_TOP          
              414  POP_TOP          

 L. 114       416  POP_EXCEPT       
              418  BREAK_LOOP          422  'to 422'
            420_0  COME_FROM           406  '406'
              420  END_FINALLY      
            422_0  COME_FROM           418  '418'
            422_1  COME_FROM           398  '398'

 L. 116       422  LOAD_FAST                'runner'
              424  LOAD_METHOD              cleanup
              426  CALL_METHOD_0         0  ''
              428  GET_AWAITABLE    
              430  LOAD_CONST               None
              432  YIELD_FROM       
              434  POP_TOP          

Parse error at or near `END_FINALLY' instruction at offset 420

        def _wait_next_notify(self) -> 'asyncio.Future[bool]':
            self._notify_waiter_done()
            loop = self.loop
            assert loop is not None
            self._notify_waiter = waiter = loop.create_future()
            self.loop.call_later(1.0, self._notify_waiter_done, waiter)
            return waiter

        def _notify_waiter_done(self, waiter: 'asyncio.Future[bool]'=None) -> None:
            if waiter is None:
                waiter = self._notify_waiter
            if waiter is not None:
                set_resultwaiterTrue
            if waiter is self._notify_waiter:
                self._notify_waiter = None

        def init_signals(self) -> None:
            self.loop.add_signal_handler(signal.SIGQUIT, self.handle_quit, signal.SIGQUIT, None)
            self.loop.add_signal_handler(signal.SIGTERM, self.handle_exit, signal.SIGTERM, None)
            self.loop.add_signal_handler(signal.SIGINT, self.handle_quit, signal.SIGINT, None)
            self.loop.add_signal_handler(signal.SIGWINCH, self.handle_winch, signal.SIGWINCH, None)
            self.loop.add_signal_handler(signal.SIGUSR1, self.handle_usr1, signal.SIGUSR1, None)
            self.loop.add_signal_handler(signal.SIGABRT, self.handle_abort, signal.SIGABRT, None)
            signal.siginterruptsignal.SIGTERMFalse
            signal.siginterruptsignal.SIGUSR1False

        def handle_quit(self, sig: int, frame: FrameType) -> None:
            self.alive = False
            self.cfg.worker_int(self)
            self._notify_waiter_done()

        def handle_abort(self, sig: int, frame: FrameType) -> None:
            self.alive = False
            self.exit_code = 1
            self.cfg.worker_abort(self)
            sys.exit(1)

        @staticmethod
        def _create_ssl_context(cfg: Any) -> 'SSLContext':
            """ Creates SSLContext instance for usage in asyncio.create_server.

        See ssl.SSLSocket.__init__ for more details.
        """
            if ssl is None:
                raise RuntimeError('SSL is not supported.')
            ctx = ssl.SSLContext(cfg.ssl_version)
            ctx.load_cert_chaincfg.certfilecfg.keyfile
            ctx.verify_mode = cfg.cert_reqs
            if cfg.ca_certs:
                ctx.load_verify_locations(cfg.ca_certs)
            if cfg.ciphers:
                ctx.set_ciphers(cfg.ciphers)
            return ctx

        def _get_valid_log_format(self, source_format: str) -> str:
            if source_format == self.DEFAULT_GUNICORN_LOG_FORMAT:
                return self.DEFAULT_AIOHTTP_LOG_FORMAT
            if re.search'%\\([^\\)]+\\)'source_format:
                raise ValueError("Gunicorn's style options in form of `%(name)s` are not supported for the log formatting. Please use aiohttp's format specification to configure access log formatting: http://docs.aiohttp.org/en/stable/logging.html#format-specification")
            else:
                return source_format


    class GunicornUVLoopWebWorker(GunicornWebWorker):

        def init_process(self):
            import uvloop
            asyncio.get_event_loop().close()
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            super().init_process()


    class GunicornTokioWebWorker(GunicornWebWorker):

        def init_process(self):
            import tokio
            asyncio.get_event_loop().close()
            asyncio.set_event_loop_policy(tokio.EventLoopPolicy())
            super().init_process()