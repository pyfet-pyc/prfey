# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\unix_events.py
"""Selector event loop for Unix with signal handling."""
import errno, io, itertools, os, selectors, signal, socket, stat, subprocess, sys, threading, warnings
from . import base_events
from . import base_subprocess
from . import constants
from . import coroutines
from . import events
from . import exceptions
from . import futures
from . import selector_events
from . import tasks
from . import transports
from .log import logger
__all__ = ('SelectorEventLoop', 'AbstractChildWatcher', 'SafeChildWatcher', 'FastChildWatcher',
           'PidfdChildWatcher', 'MultiLoopChildWatcher', 'ThreadedChildWatcher',
           'DefaultEventLoopPolicy')
if sys.platform == 'win32':
    raise ImportError('Signals are not really supported on Windows')

def _sighandler_noop(signum, frame):
    """Dummy signal handler."""
    pass


class _UnixSelectorEventLoop(selector_events.BaseSelectorEventLoop):
    __doc__ = 'Unix event loop.\n\n    Adds signal handling and UNIX Domain Socket support to SelectorEventLoop.\n    '

    def __init__(self, selector=None):
        super().__init__(selector)
        self._signal_handlers = {}

    def close(self):
        super().close()
        if not sys.is_finalizing():
            for sig in list(self._signal_handlers):
                self.remove_signal_handler(sig)

        elif self._signal_handlers:
            warnings.warn(f"Closing the loop {self!r} on interpreter shutdown stage, skipping signal handlers removal", ResourceWarning,
              source=self)
            self._signal_handlers.clear()

    def _process_self_data(self, data):
        for signum in data:
            if not signum:
                pass
            else:
                self._handle_signal(signum)

    def add_signal_handler--- This code section failed: ---

 L.  84         0  LOAD_GLOBAL              coroutines
                2  LOAD_METHOD              iscoroutine
                4  LOAD_FAST                'callback'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     20  'to 20'

 L.  85        10  LOAD_GLOBAL              coroutines
               12  LOAD_METHOD              iscoroutinefunction
               14  LOAD_FAST                'callback'
               16  CALL_METHOD_1         1  ''

 L.  84        18  POP_JUMP_IF_FALSE    28  'to 28'
             20_0  COME_FROM             8  '8'

 L.  86        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'coroutines cannot be used with add_signal_handler()'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L.  88        28  LOAD_FAST                'self'
               30  LOAD_METHOD              _check_signal
               32  LOAD_FAST                'sig'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L.  89        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _check_closed
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          

 L.  90        46  SETUP_FINALLY        68  'to 68'

 L.  95        48  LOAD_GLOBAL              signal
               50  LOAD_METHOD              set_wakeup_fd
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _csock
               56  LOAD_METHOD              fileno
               58  CALL_METHOD_0         0  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  POP_BLOCK        
               66  JUMP_FORWARD        120  'to 120'
             68_0  COME_FROM_FINALLY    46  '46'

 L.  96        68  DUP_TOP          
               70  LOAD_GLOBAL              ValueError
               72  LOAD_GLOBAL              OSError
               74  BUILD_TUPLE_2         2 
               76  <121>               118  ''
               78  POP_TOP          
               80  STORE_FAST               'exc'
               82  POP_TOP          
               84  SETUP_FINALLY       110  'to 110'

 L.  97        86  LOAD_GLOBAL              RuntimeError
               88  LOAD_GLOBAL              str
               90  LOAD_FAST                'exc'
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
               98  POP_BLOCK        
              100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  STORE_FAST               'exc'
              106  DELETE_FAST              'exc'
              108  JUMP_FORWARD        120  'to 120'
            110_0  COME_FROM_FINALLY    84  '84'
              110  LOAD_CONST               None
              112  STORE_FAST               'exc'
              114  DELETE_FAST              'exc'
              116  <48>             
              118  <48>             
            120_0  COME_FROM           108  '108'
            120_1  COME_FROM            66  '66'

 L.  99       120  LOAD_GLOBAL              events
              122  LOAD_METHOD              Handle
              124  LOAD_FAST                'callback'
              126  LOAD_FAST                'args'
              128  LOAD_FAST                'self'
              130  LOAD_CONST               None
              132  CALL_METHOD_4         4  ''
              134  STORE_FAST               'handle'

 L. 100       136  LOAD_FAST                'handle'
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _signal_handlers
              142  LOAD_FAST                'sig'
              144  STORE_SUBSCR     

 L. 102       146  SETUP_FINALLY       176  'to 176'

 L. 106       148  LOAD_GLOBAL              signal
              150  LOAD_METHOD              signal
              152  LOAD_FAST                'sig'
              154  LOAD_GLOBAL              _sighandler_noop
              156  CALL_METHOD_2         2  ''
              158  POP_TOP          

 L. 109       160  LOAD_GLOBAL              signal
              162  LOAD_METHOD              siginterrupt
              164  LOAD_FAST                'sig'
              166  LOAD_CONST               False
              168  CALL_METHOD_2         2  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        334  'to 334'
            176_0  COME_FROM_FINALLY   146  '146'

 L. 110       176  DUP_TOP          
              178  LOAD_GLOBAL              OSError
          180_182  <121>               332  ''
              184  POP_TOP          
              186  STORE_FAST               'exc'
              188  POP_TOP          
              190  SETUP_FINALLY       324  'to 324'

 L. 111       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _signal_handlers
              196  LOAD_FAST                'sig'
              198  DELETE_SUBSCR    

 L. 112       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _signal_handlers
          204_206  POP_JUMP_IF_TRUE    278  'to 278'

 L. 113       208  SETUP_FINALLY       224  'to 224'

 L. 114       210  LOAD_GLOBAL              signal
              212  LOAD_METHOD              set_wakeup_fd
              214  LOAD_CONST               -1
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          
              220  POP_BLOCK        
              222  JUMP_FORWARD        278  'to 278'
            224_0  COME_FROM_FINALLY   208  '208'

 L. 115       224  DUP_TOP          
              226  LOAD_GLOBAL              ValueError
              228  LOAD_GLOBAL              OSError
              230  BUILD_TUPLE_2         2 
          232_234  <121>               276  ''
              236  POP_TOP          
              238  STORE_FAST               'nexc'
              240  POP_TOP          
              242  SETUP_FINALLY       268  'to 268'

 L. 116       244  LOAD_GLOBAL              logger
              246  LOAD_METHOD              info
              248  LOAD_STR                 'set_wakeup_fd(-1) failed: %s'
              250  LOAD_FAST                'nexc'
              252  CALL_METHOD_2         2  ''
              254  POP_TOP          
              256  POP_BLOCK        
              258  POP_EXCEPT       
              260  LOAD_CONST               None
              262  STORE_FAST               'nexc'
              264  DELETE_FAST              'nexc'
              266  JUMP_FORWARD        278  'to 278'
            268_0  COME_FROM_FINALLY   242  '242'
              268  LOAD_CONST               None
              270  STORE_FAST               'nexc'
              272  DELETE_FAST              'nexc'
              274  <48>             
              276  <48>             
            278_0  COME_FROM           266  '266'
            278_1  COME_FROM           222  '222'
            278_2  COME_FROM           204  '204'

 L. 118       278  LOAD_FAST                'exc'
              280  LOAD_ATTR                errno
              282  LOAD_GLOBAL              errno
              284  LOAD_ATTR                EINVAL
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   310  'to 310'

 L. 119       292  LOAD_GLOBAL              RuntimeError
              294  LOAD_STR                 'sig '
              296  LOAD_FAST                'sig'
              298  FORMAT_VALUE          0  ''
              300  LOAD_STR                 ' cannot be caught'
              302  BUILD_STRING_3        3 
              304  CALL_FUNCTION_1       1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           288  '288'

 L. 121       310  RAISE_VARARGS_0       0  'reraise'
            312_0  COME_FROM           308  '308'
              312  POP_BLOCK        
              314  POP_EXCEPT       
              316  LOAD_CONST               None
              318  STORE_FAST               'exc'
              320  DELETE_FAST              'exc'
              322  JUMP_FORWARD        334  'to 334'
            324_0  COME_FROM_FINALLY   190  '190'
              324  LOAD_CONST               None
              326  STORE_FAST               'exc'
              328  DELETE_FAST              'exc'
              330  <48>             
              332  <48>             
            334_0  COME_FROM           322  '322'
            334_1  COME_FROM           174  '174'

Parse error at or near `<121>' instruction at offset 76

    def _handle_signal--- This code section failed: ---

 L. 125         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _signal_handlers
                4  LOAD_METHOD              get
                6  LOAD_FAST                'sig'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'handle'

 L. 126        12  LOAD_FAST                'handle'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 127        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 128        24  LOAD_FAST                'handle'
               26  LOAD_ATTR                _cancelled
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 129        30  LOAD_FAST                'self'
               32  LOAD_METHOD              remove_signal_handler
               34  LOAD_FAST                'sig'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
               40  JUMP_FORWARD         52  'to 52'
             42_0  COME_FROM            28  '28'

 L. 131        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _add_callback_signalsafe
               46  LOAD_FAST                'handle'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            40  '40'

Parse error at or near `<117>' instruction at offset 16

    def remove_signal_handler--- This code section failed: ---

 L. 138         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_signal
                4  LOAD_FAST                'sig'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 139        10  SETUP_FINALLY        24  'to 24'

 L. 140        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _signal_handlers
               16  LOAD_FAST                'sig'
               18  DELETE_SUBSCR    
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY    10  '10'

 L. 141        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 142        36  POP_EXCEPT       
               38  LOAD_CONST               False
               40  RETURN_VALUE     
               42  <48>             
             44_0  COME_FROM            22  '22'

 L. 144        44  LOAD_FAST                'sig'
               46  LOAD_GLOBAL              signal
               48  LOAD_ATTR                SIGINT
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 145        54  LOAD_GLOBAL              signal
               56  LOAD_ATTR                default_int_handler
               58  STORE_FAST               'handler'
               60  JUMP_FORWARD         68  'to 68'
             62_0  COME_FROM            52  '52'

 L. 147        62  LOAD_GLOBAL              signal
               64  LOAD_ATTR                SIG_DFL
               66  STORE_FAST               'handler'
             68_0  COME_FROM            60  '60'

 L. 149        68  SETUP_FINALLY        86  'to 86'

 L. 150        70  LOAD_GLOBAL              signal
               72  LOAD_METHOD              signal
               74  LOAD_FAST                'sig'
               76  LOAD_FAST                'handler'
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          
               82  POP_BLOCK        
               84  JUMP_FORWARD        154  'to 154'
             86_0  COME_FROM_FINALLY    68  '68'

 L. 151        86  DUP_TOP          
               88  LOAD_GLOBAL              OSError
               90  <121>               152  ''
               92  POP_TOP          
               94  STORE_FAST               'exc'
               96  POP_TOP          
               98  SETUP_FINALLY       144  'to 144'

 L. 152       100  LOAD_FAST                'exc'
              102  LOAD_ATTR                errno
              104  LOAD_GLOBAL              errno
              106  LOAD_ATTR                EINVAL
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   130  'to 130'

 L. 153       112  LOAD_GLOBAL              RuntimeError
              114  LOAD_STR                 'sig '
              116  LOAD_FAST                'sig'
              118  FORMAT_VALUE          0  ''
              120  LOAD_STR                 ' cannot be caught'
              122  BUILD_STRING_3        3 
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM           110  '110'

 L. 155       130  RAISE_VARARGS_0       0  'reraise'
            132_0  COME_FROM           128  '128'
              132  POP_BLOCK        
              134  POP_EXCEPT       
              136  LOAD_CONST               None
              138  STORE_FAST               'exc'
              140  DELETE_FAST              'exc'
              142  JUMP_FORWARD        154  'to 154'
            144_0  COME_FROM_FINALLY    98  '98'
              144  LOAD_CONST               None
              146  STORE_FAST               'exc'
              148  DELETE_FAST              'exc'
              150  <48>             
              152  <48>             
            154_0  COME_FROM           142  '142'
            154_1  COME_FROM            84  '84'

 L. 157       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _signal_handlers
              158  POP_JUMP_IF_TRUE    228  'to 228'

 L. 158       160  SETUP_FINALLY       176  'to 176'

 L. 159       162  LOAD_GLOBAL              signal
              164  LOAD_METHOD              set_wakeup_fd
              166  LOAD_CONST               -1
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        228  'to 228'
            176_0  COME_FROM_FINALLY   160  '160'

 L. 160       176  DUP_TOP          
              178  LOAD_GLOBAL              ValueError
              180  LOAD_GLOBAL              OSError
              182  BUILD_TUPLE_2         2 
              184  <121>               226  ''
              186  POP_TOP          
              188  STORE_FAST               'exc'
              190  POP_TOP          
              192  SETUP_FINALLY       218  'to 218'

 L. 161       194  LOAD_GLOBAL              logger
              196  LOAD_METHOD              info
              198  LOAD_STR                 'set_wakeup_fd(-1) failed: %s'
              200  LOAD_FAST                'exc'
              202  CALL_METHOD_2         2  ''
              204  POP_TOP          
              206  POP_BLOCK        
              208  POP_EXCEPT       
              210  LOAD_CONST               None
              212  STORE_FAST               'exc'
              214  DELETE_FAST              'exc'
              216  JUMP_FORWARD        228  'to 228'
            218_0  COME_FROM_FINALLY   192  '192'
              218  LOAD_CONST               None
              220  STORE_FAST               'exc'
              222  DELETE_FAST              'exc'
              224  <48>             
              226  <48>             
            228_0  COME_FROM           216  '216'
            228_1  COME_FROM           174  '174'
            228_2  COME_FROM           158  '158'

 L. 163       228  LOAD_CONST               True
              230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 28

    def _check_signal--- This code section failed: ---

 L. 171         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'sig'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     24  'to 24'

 L. 172        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'sig must be an int, not '
               14  LOAD_FAST                'sig'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             8  '8'

 L. 174        24  LOAD_FAST                'sig'
               26  LOAD_GLOBAL              signal
               28  LOAD_METHOD              valid_signals
               30  CALL_METHOD_0         0  ''
               32  <118>                 1  ''
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L. 175        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'invalid signal number '
               40  LOAD_FAST                'sig'
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_2        2 
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            34  '34'

Parse error at or near `<118>' instruction at offset 32

    def _make_read_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixReadPipeTransport(self, pipe, protocol, waiter, extra)

    def _make_write_pipe_transport(self, pipe, protocol, waiter=None, extra=None):
        return _UnixWritePipeTransport(self, pipe, protocol, waiter, extra)

    async def _make_subprocess_transport--- This code section failed: ---

 L. 188         0  LOAD_GLOBAL              events
                2  LOAD_METHOD              get_child_watcher
                4  CALL_METHOD_0         0  ''
                6  SETUP_WITH          184  'to 184'
                8  STORE_FAST               'watcher'

 L. 189        10  LOAD_FAST                'watcher'
               12  LOAD_METHOD              is_active
               14  CALL_METHOD_0         0  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L. 194        18  LOAD_GLOBAL              RuntimeError
               20  LOAD_STR                 'asyncio.get_child_watcher() is not activated, subprocess support is not installed.'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 196        26  LOAD_FAST                'self'
               28  LOAD_METHOD              create_future
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'waiter'

 L. 197        34  LOAD_GLOBAL              _UnixSubprocessTransport
               36  LOAD_FAST                'self'
               38  LOAD_FAST                'protocol'
               40  LOAD_FAST                'args'
               42  LOAD_FAST                'shell'

 L. 198        44  LOAD_FAST                'stdin'
               46  LOAD_FAST                'stdout'
               48  LOAD_FAST                'stderr'
               50  LOAD_FAST                'bufsize'

 L. 197        52  BUILD_TUPLE_8         8 

 L. 199        54  LOAD_FAST                'waiter'
               56  LOAD_FAST                'extra'

 L. 197        58  LOAD_CONST               ('waiter', 'extra')
               60  BUILD_CONST_KEY_MAP_2     2 

 L. 200        62  LOAD_FAST                'kwargs'

 L. 197        64  <164>                 1  ''
               66  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               68  STORE_FAST               'transp'

 L. 202        70  LOAD_FAST                'watcher'
               72  LOAD_METHOD              add_child_handler
               74  LOAD_FAST                'transp'
               76  LOAD_METHOD              get_pid
               78  CALL_METHOD_0         0  ''

 L. 203        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _child_watcher_callback
               84  LOAD_FAST                'transp'

 L. 202        86  CALL_METHOD_3         3  ''
               88  POP_TOP          

 L. 204        90  SETUP_FINALLY       106  'to 106'

 L. 205        92  LOAD_FAST                'waiter'
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  POP_TOP          
              102  POP_BLOCK        
              104  JUMP_FORWARD        170  'to 170'
            106_0  COME_FROM_FINALLY    90  '90'

 L. 206       106  DUP_TOP          
              108  LOAD_GLOBAL              SystemExit
              110  LOAD_GLOBAL              KeyboardInterrupt
              112  BUILD_TUPLE_2         2 
              114  <121>               128  ''
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 207       122  RAISE_VARARGS_0       0  'reraise'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        170  'to 170'

 L. 208       128  DUP_TOP          
              130  LOAD_GLOBAL              BaseException
              132  <121>               168  ''
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 209       140  LOAD_FAST                'transp'
              142  LOAD_METHOD              close
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

 L. 210       148  LOAD_FAST                'transp'
              150  LOAD_METHOD              _wait
              152  CALL_METHOD_0         0  ''
              154  GET_AWAITABLE    
              156  LOAD_CONST               None
              158  YIELD_FROM       
              160  POP_TOP          

 L. 211       162  RAISE_VARARGS_0       0  'reraise'
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
              168  <48>             
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           126  '126'
            170_2  COME_FROM           104  '104'
              170  POP_BLOCK        
              172  LOAD_CONST               None
              174  DUP_TOP          
              176  DUP_TOP          
              178  CALL_FUNCTION_3       3  ''
              180  POP_TOP          
              182  JUMP_FORWARD        200  'to 200'
            184_0  COME_FROM_WITH        6  '6'
              184  <49>             
              186  POP_JUMP_IF_TRUE    190  'to 190'
              188  <48>             
            190_0  COME_FROM           186  '186'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          
              196  POP_EXCEPT       
              198  POP_TOP          
            200_0  COME_FROM           182  '182'

 L. 213       200  LOAD_FAST                'transp'
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 64

    def _child_watcher_callback(self, pid, returncode, transp):
        self.call_soon_threadsafetransp._process_exitedreturncode

    async def create_unix_connection--- This code section failed: ---

 L. 223         0  LOAD_FAST                'server_hostname'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     22  'to 22'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'server_hostname'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'
             22_1  COME_FROM             6  '6'

 L. 224        22  LOAD_FAST                'ssl'
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 225        26  LOAD_FAST                'server_hostname'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    76  'to 76'

 L. 226        34  LOAD_GLOBAL              ValueError

 L. 227        36  LOAD_STR                 'you have to pass server_hostname when using ssl'

 L. 226        38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM            24  '24'

 L. 229        44  LOAD_FAST                'server_hostname'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L. 230        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'server_hostname is only meaningful with ssl'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 231        60  LOAD_FAST                'ssl_handshake_timeout'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L. 232        68  LOAD_GLOBAL              ValueError

 L. 233        70  LOAD_STR                 'ssl_handshake_timeout is only meaningful with ssl'

 L. 232        72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            42  '42'
             76_2  COME_FROM            32  '32'

 L. 235        76  LOAD_FAST                'path'
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_FALSE   186  'to 186'

 L. 236        84  LOAD_FAST                'sock'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 237        92  LOAD_GLOBAL              ValueError

 L. 238        94  LOAD_STR                 'path and sock can not be specified at the same time'

 L. 237        96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'

 L. 240       100  LOAD_GLOBAL              os
              102  LOAD_METHOD              fspath
              104  LOAD_FAST                'path'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'path'

 L. 241       110  LOAD_GLOBAL              socket
              112  LOAD_METHOD              socket
              114  LOAD_GLOBAL              socket
              116  LOAD_ATTR                AF_UNIX
              118  LOAD_GLOBAL              socket
              120  LOAD_ATTR                SOCK_STREAM
              122  LOAD_CONST               0
              124  CALL_METHOD_3         3  ''
              126  STORE_FAST               'sock'

 L. 242       128  SETUP_FINALLY       162  'to 162'

 L. 243       130  LOAD_FAST                'sock'
              132  LOAD_METHOD              setblocking
              134  LOAD_CONST               False
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L. 244       140  LOAD_FAST                'self'
              142  LOAD_METHOD              sock_connect
              144  LOAD_FAST                'sock'
              146  LOAD_FAST                'path'
              148  CALL_METHOD_2         2  ''
              150  GET_AWAITABLE    
              152  LOAD_CONST               None
              154  YIELD_FROM       
              156  POP_TOP          
              158  POP_BLOCK        
              160  JUMP_FORWARD        250  'to 250'
            162_0  COME_FROM_FINALLY   128  '128'

 L. 245       162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 246       168  LOAD_FAST                'sock'
              170  LOAD_METHOD              close
              172  CALL_METHOD_0         0  ''
              174  POP_TOP          

 L. 247       176  RAISE_VARARGS_0       0  'reraise'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        250  'to 250'
              182  <48>             
              184  JUMP_FORWARD        250  'to 250'
            186_0  COME_FROM            82  '82'

 L. 250       186  LOAD_FAST                'sock'
              188  LOAD_CONST               None
              190  <117>                 0  ''
              192  POP_JUMP_IF_FALSE   202  'to 202'

 L. 251       194  LOAD_GLOBAL              ValueError
              196  LOAD_STR                 'no path and sock were specified'
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           192  '192'

 L. 252       202  LOAD_FAST                'sock'
              204  LOAD_ATTR                family
              206  LOAD_GLOBAL              socket
              208  LOAD_ATTR                AF_UNIX
              210  COMPARE_OP               !=
              212  POP_JUMP_IF_TRUE    226  'to 226'

 L. 253       214  LOAD_FAST                'sock'
              216  LOAD_ATTR                type
              218  LOAD_GLOBAL              socket
              220  LOAD_ATTR                SOCK_STREAM
              222  COMPARE_OP               !=

 L. 252       224  POP_JUMP_IF_FALSE   240  'to 240'
            226_0  COME_FROM           212  '212'

 L. 254       226  LOAD_GLOBAL              ValueError

 L. 255       228  LOAD_STR                 'A UNIX Domain Stream Socket was expected, got '
              230  LOAD_FAST                'sock'
              232  FORMAT_VALUE          2  '!r'
              234  BUILD_STRING_2        2 

 L. 254       236  CALL_FUNCTION_1       1  ''
              238  RAISE_VARARGS_1       1  'exception instance'
            240_0  COME_FROM           224  '224'

 L. 256       240  LOAD_FAST                'sock'
              242  LOAD_METHOD              setblocking
              244  LOAD_CONST               False
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
            250_0  COME_FROM           184  '184'
            250_1  COME_FROM           180  '180'
            250_2  COME_FROM           160  '160'

 L. 258       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _create_connection_transport

 L. 259       254  LOAD_FAST                'sock'
              256  LOAD_FAST                'protocol_factory'
              258  LOAD_FAST                'ssl'
              260  LOAD_FAST                'server_hostname'

 L. 260       262  LOAD_FAST                'ssl_handshake_timeout'

 L. 258       264  LOAD_CONST               ('ssl_handshake_timeout',)
              266  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              268  GET_AWAITABLE    
              270  LOAD_CONST               None
              272  YIELD_FROM       
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'transport'
              278  STORE_FAST               'protocol'

 L. 261       280  LOAD_FAST                'transport'
              282  LOAD_FAST                'protocol'
              284  BUILD_TUPLE_2         2 
              286  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    async def create_unix_server--- This code section failed: ---

 L. 268         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ssl'
                4  LOAD_GLOBAL              bool
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 269        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'ssl argument must be an SSLContext or None'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 271        18  LOAD_FAST                'ssl_handshake_timeout'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  LOAD_FAST                'ssl'
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 272        30  LOAD_GLOBAL              ValueError

 L. 273        32  LOAD_STR                 'ssl_handshake_timeout is only meaningful with ssl'

 L. 272        34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            24  '24'

 L. 275        38  LOAD_FAST                'path'
               40  LOAD_CONST               None
               42  <117>                 1  ''
            44_46  POP_JUMP_IF_FALSE   330  'to 330'

 L. 276        48  LOAD_FAST                'sock'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L. 277        56  LOAD_GLOBAL              ValueError

 L. 278        58  LOAD_STR                 'path and sock can not be specified at the same time'

 L. 277        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'

 L. 280        64  LOAD_GLOBAL              os
               66  LOAD_METHOD              fspath
               68  LOAD_FAST                'path'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'path'

 L. 281        74  LOAD_GLOBAL              socket
               76  LOAD_METHOD              socket
               78  LOAD_GLOBAL              socket
               80  LOAD_ATTR                AF_UNIX
               82  LOAD_GLOBAL              socket
               84  LOAD_ATTR                SOCK_STREAM
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'sock'

 L. 284        90  LOAD_FAST                'path'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  LOAD_CONST               (0, '\x00')
               98  <118>                 1  ''
              100  POP_JUMP_IF_FALSE   202  'to 202'

 L. 285       102  SETUP_FINALLY       136  'to 136'

 L. 286       104  LOAD_GLOBAL              stat
              106  LOAD_METHOD              S_ISSOCK
              108  LOAD_GLOBAL              os
              110  LOAD_METHOD              stat
              112  LOAD_FAST                'path'
              114  CALL_METHOD_1         1  ''
              116  LOAD_ATTR                st_mode
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 287       122  LOAD_GLOBAL              os
              124  LOAD_METHOD              remove
              126  LOAD_FAST                'path'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
            132_0  COME_FROM           120  '120'
              132  POP_BLOCK        
              134  JUMP_FORWARD        202  'to 202'
            136_0  COME_FROM_FINALLY   102  '102'

 L. 288       136  DUP_TOP          
              138  LOAD_GLOBAL              FileNotFoundError
              140  <121>               152  ''
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L. 289       148  POP_EXCEPT       
              150  JUMP_FORWARD        202  'to 202'

 L. 290       152  DUP_TOP          
              154  LOAD_GLOBAL              OSError
              156  <121>               200  ''
              158  POP_TOP          
              160  STORE_FAST               'err'
              162  POP_TOP          
              164  SETUP_FINALLY       192  'to 192'

 L. 292       166  LOAD_GLOBAL              logger
              168  LOAD_METHOD              error
              170  LOAD_STR                 'Unable to check or remove stale UNIX socket %r: %r'

 L. 293       172  LOAD_FAST                'path'
              174  LOAD_FAST                'err'

 L. 292       176  CALL_METHOD_3         3  ''
              178  POP_TOP          
              180  POP_BLOCK        
              182  POP_EXCEPT       
              184  LOAD_CONST               None
              186  STORE_FAST               'err'
              188  DELETE_FAST              'err'
              190  JUMP_FORWARD        202  'to 202'
            192_0  COME_FROM_FINALLY   164  '164'
              192  LOAD_CONST               None
              194  STORE_FAST               'err'
              196  DELETE_FAST              'err'
              198  <48>             
              200  <48>             
            202_0  COME_FROM           190  '190'
            202_1  COME_FROM           150  '150'
            202_2  COME_FROM           134  '134'
            202_3  COME_FROM           100  '100'

 L. 295       202  SETUP_FINALLY       218  'to 218'

 L. 296       204  LOAD_FAST                'sock'
              206  LOAD_METHOD              bind
              208  LOAD_FAST                'path'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
              214  POP_BLOCK        
              216  JUMP_FORWARD        328  'to 328'
            218_0  COME_FROM_FINALLY   202  '202'

 L. 297       218  DUP_TOP          
              220  LOAD_GLOBAL              OSError
          222_224  <121>               306  ''
              226  POP_TOP          
              228  STORE_FAST               'exc'
              230  POP_TOP          
              232  SETUP_FINALLY       298  'to 298'

 L. 298       234  LOAD_FAST                'sock'
              236  LOAD_METHOD              close
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          

 L. 299       242  LOAD_FAST                'exc'
              244  LOAD_ATTR                errno
              246  LOAD_GLOBAL              errno
              248  LOAD_ATTR                EADDRINUSE
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   284  'to 284'

 L. 302       256  LOAD_STR                 'Address '
              258  LOAD_FAST                'path'
              260  FORMAT_VALUE          2  '!r'
              262  LOAD_STR                 ' is already in use'
              264  BUILD_STRING_3        3 
              266  STORE_FAST               'msg'

 L. 303       268  LOAD_GLOBAL              OSError
              270  LOAD_GLOBAL              errno
              272  LOAD_ATTR                EADDRINUSE
              274  LOAD_FAST                'msg'
              276  CALL_FUNCTION_2       2  ''
              278  LOAD_CONST               None
              280  RAISE_VARARGS_2       2  'exception instance with __cause__'
              282  JUMP_FORWARD        286  'to 286'
            284_0  COME_FROM           252  '252'

 L. 305       284  RAISE_VARARGS_0       0  'reraise'
            286_0  COME_FROM           282  '282'
              286  POP_BLOCK        
              288  POP_EXCEPT       
              290  LOAD_CONST               None
              292  STORE_FAST               'exc'
              294  DELETE_FAST              'exc'
              296  JUMP_FORWARD        328  'to 328'
            298_0  COME_FROM_FINALLY   232  '232'
              298  LOAD_CONST               None
              300  STORE_FAST               'exc'
              302  DELETE_FAST              'exc'
              304  <48>             

 L. 306       306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 307       312  LOAD_FAST                'sock'
              314  LOAD_METHOD              close
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          

 L. 308       320  RAISE_VARARGS_0       0  'reraise'
              322  POP_EXCEPT       
              324  JUMP_FORWARD        328  'to 328'
              326  <48>             
            328_0  COME_FROM           324  '324'
            328_1  COME_FROM           296  '296'
            328_2  COME_FROM           216  '216'
              328  JUMP_FORWARD        390  'to 390'
            330_0  COME_FROM            44  '44'

 L. 310       330  LOAD_FAST                'sock'
              332  LOAD_CONST               None
              334  <117>                 0  ''
          336_338  POP_JUMP_IF_FALSE   348  'to 348'

 L. 311       340  LOAD_GLOBAL              ValueError

 L. 312       342  LOAD_STR                 'path was not specified, and no sock specified'

 L. 311       344  CALL_FUNCTION_1       1  ''
              346  RAISE_VARARGS_1       1  'exception instance'
            348_0  COME_FROM           336  '336'

 L. 314       348  LOAD_FAST                'sock'
              350  LOAD_ATTR                family
              352  LOAD_GLOBAL              socket
              354  LOAD_ATTR                AF_UNIX
              356  COMPARE_OP               !=
          358_360  POP_JUMP_IF_TRUE    376  'to 376'

 L. 315       362  LOAD_FAST                'sock'
              364  LOAD_ATTR                type
              366  LOAD_GLOBAL              socket
              368  LOAD_ATTR                SOCK_STREAM
              370  COMPARE_OP               !=

 L. 314   372_374  POP_JUMP_IF_FALSE   390  'to 390'
            376_0  COME_FROM           358  '358'

 L. 316       376  LOAD_GLOBAL              ValueError

 L. 317       378  LOAD_STR                 'A UNIX Domain Stream Socket was expected, got '
              380  LOAD_FAST                'sock'
              382  FORMAT_VALUE          2  '!r'
              384  BUILD_STRING_2        2 

 L. 316       386  CALL_FUNCTION_1       1  ''
              388  RAISE_VARARGS_1       1  'exception instance'
            390_0  COME_FROM           372  '372'
            390_1  COME_FROM           328  '328'

 L. 319       390  LOAD_FAST                'sock'
              392  LOAD_METHOD              setblocking
              394  LOAD_CONST               False
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          

 L. 320       400  LOAD_GLOBAL              base_events
              402  LOAD_METHOD              Server
              404  LOAD_FAST                'self'
              406  LOAD_FAST                'sock'
              408  BUILD_LIST_1          1 
              410  LOAD_FAST                'protocol_factory'

 L. 321       412  LOAD_FAST                'ssl'
              414  LOAD_FAST                'backlog'
              416  LOAD_FAST                'ssl_handshake_timeout'

 L. 320       418  CALL_METHOD_6         6  ''
              420  STORE_FAST               'server'

 L. 322       422  LOAD_FAST                'start_serving'
          424_426  POP_JUMP_IF_FALSE   456  'to 456'

 L. 323       428  LOAD_FAST                'server'
              430  LOAD_METHOD              _start_serving
              432  CALL_METHOD_0         0  ''
              434  POP_TOP          

 L. 326       436  LOAD_GLOBAL              tasks
              438  LOAD_ATTR                sleep
              440  LOAD_CONST               0
              442  LOAD_FAST                'self'
              444  LOAD_CONST               ('loop',)
              446  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              448  GET_AWAITABLE    
              450  LOAD_CONST               None
              452  YIELD_FROM       
              454  POP_TOP          
            456_0  COME_FROM           424  '424'

 L. 328       456  LOAD_FAST                'server'
              458  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    async def _sock_sendfile_native--- This code section failed: ---

 L. 331         0  SETUP_FINALLY        12  'to 12'

 L. 332         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                sendfile
                6  POP_TOP          
                8  POP_BLOCK        
               10  JUMP_FORWARD         40  'to 40'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 333        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                38  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 334        24  LOAD_GLOBAL              exceptions
               26  LOAD_METHOD              SendfileNotAvailableError

 L. 335        28  LOAD_STR                 'os.sendfile() is not available'

 L. 334        30  CALL_METHOD_1         1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM            10  '10'

 L. 336        40  SETUP_FINALLY        54  'to 54'

 L. 337        42  LOAD_FAST                'file'
               44  LOAD_METHOD              fileno
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'fileno'
               50  POP_BLOCK        
               52  JUMP_FORWARD        106  'to 106'
             54_0  COME_FROM_FINALLY    40  '40'

 L. 338        54  DUP_TOP          
               56  LOAD_GLOBAL              AttributeError
               58  LOAD_GLOBAL              io
               60  LOAD_ATTR                UnsupportedOperation
               62  BUILD_TUPLE_2         2 
               64  <121>               104  ''
               66  POP_TOP          
               68  STORE_FAST               'err'
               70  POP_TOP          
               72  SETUP_FINALLY        96  'to 96'

 L. 339        74  LOAD_GLOBAL              exceptions
               76  LOAD_METHOD              SendfileNotAvailableError
               78  LOAD_STR                 'not a regular file'
               80  CALL_METHOD_1         1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'err'
               92  DELETE_FAST              'err'
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM_FINALLY    72  '72'
               96  LOAD_CONST               None
               98  STORE_FAST               'err'
              100  DELETE_FAST              'err'
              102  <48>             
              104  <48>             
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            52  '52'

 L. 340       106  SETUP_FINALLY       124  'to 124'

 L. 341       108  LOAD_GLOBAL              os
              110  LOAD_METHOD              fstat
              112  LOAD_FAST                'fileno'
              114  CALL_METHOD_1         1  ''
              116  LOAD_ATTR                st_size
              118  STORE_FAST               'fsize'
              120  POP_BLOCK        
              122  JUMP_FORWARD        152  'to 152'
            124_0  COME_FROM_FINALLY   106  '106'

 L. 342       124  DUP_TOP          
              126  LOAD_GLOBAL              OSError
              128  <121>               150  ''
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 343       136  LOAD_GLOBAL              exceptions
              138  LOAD_METHOD              SendfileNotAvailableError
              140  LOAD_STR                 'not a regular file'
              142  CALL_METHOD_1         1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
              150  <48>             
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           122  '122'

 L. 344       152  LOAD_FAST                'count'
              154  POP_JUMP_IF_FALSE   160  'to 160'
              156  LOAD_FAST                'count'
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           154  '154'
              160  LOAD_FAST                'fsize'
            162_0  COME_FROM           158  '158'
              162  STORE_FAST               'blocksize'

 L. 345       164  LOAD_FAST                'blocksize'
              166  POP_JUMP_IF_TRUE    172  'to 172'

 L. 346       168  LOAD_CONST               0
              170  RETURN_VALUE     
            172_0  COME_FROM           166  '166'

 L. 348       172  LOAD_FAST                'self'
              174  LOAD_METHOD              create_future
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'fut'

 L. 349       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _sock_sendfile_native_impl
              184  LOAD_FAST                'fut'
              186  LOAD_CONST               None
              188  LOAD_FAST                'sock'
              190  LOAD_FAST                'fileno'

 L. 350       192  LOAD_FAST                'offset'
              194  LOAD_FAST                'count'
              196  LOAD_FAST                'blocksize'
              198  LOAD_CONST               0

 L. 349       200  CALL_METHOD_8         8  ''
              202  POP_TOP          

 L. 351       204  LOAD_FAST                'fut'
              206  GET_AWAITABLE    
              208  LOAD_CONST               None
              210  YIELD_FROM       
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 16

    def _sock_sendfile_native_impl--- This code section failed: ---

 L. 355         0  LOAD_FAST                'sock'
                2  LOAD_METHOD              fileno
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'fd'

 L. 356         8  LOAD_FAST                'registered_fd'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 361        16  LOAD_FAST                'self'
               18  LOAD_METHOD              remove_writer
               20  LOAD_FAST                'registered_fd'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L. 362        26  LOAD_FAST                'fut'
               28  LOAD_METHOD              cancelled
               30  CALL_METHOD_0         0  ''
               32  POP_JUMP_IF_FALSE    52  'to 52'

 L. 363        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _sock_sendfile_update_filepos
               38  LOAD_FAST                'fileno'
               40  LOAD_FAST                'offset'
               42  LOAD_FAST                'total_sent'
               44  CALL_METHOD_3         3  ''
               46  POP_TOP          

 L. 364        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            32  '32'

 L. 365        52  LOAD_FAST                'count'
               54  POP_JUMP_IF_FALSE   100  'to 100'

 L. 366        56  LOAD_FAST                'count'
               58  LOAD_FAST                'total_sent'
               60  BINARY_SUBTRACT  
               62  STORE_FAST               'blocksize'

 L. 367        64  LOAD_FAST                'blocksize'
               66  LOAD_CONST               0
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE   100  'to 100'

 L. 368        72  LOAD_FAST                'self'
               74  LOAD_METHOD              _sock_sendfile_update_filepos
               76  LOAD_FAST                'fileno'
               78  LOAD_FAST                'offset'
               80  LOAD_FAST                'total_sent'
               82  CALL_METHOD_3         3  ''
               84  POP_TOP          

 L. 369        86  LOAD_FAST                'fut'
               88  LOAD_METHOD              set_result
               90  LOAD_FAST                'total_sent'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 370        96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            70  '70'
            100_1  COME_FROM            54  '54'

 L. 372       100  SETUP_FINALLY       124  'to 124'

 L. 373       102  LOAD_GLOBAL              os
              104  LOAD_METHOD              sendfile
              106  LOAD_FAST                'fd'
              108  LOAD_FAST                'fileno'
              110  LOAD_FAST                'offset'
              112  LOAD_FAST                'blocksize'
              114  CALL_METHOD_4         4  ''
              116  STORE_FAST               'sent'
              118  POP_BLOCK        
          120_122  JUMP_FORWARD        448  'to 448'
            124_0  COME_FROM_FINALLY   100  '100'

 L. 374       124  DUP_TOP          
              126  LOAD_GLOBAL              BlockingIOError
              128  LOAD_GLOBAL              InterruptedError
              130  BUILD_TUPLE_2         2 
              132  <121>               196  ''
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 375       140  LOAD_FAST                'registered_fd'
              142  LOAD_CONST               None
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   160  'to 160'

 L. 376       148  LOAD_FAST                'self'
              150  LOAD_METHOD              _sock_add_cancellation_callback
              152  LOAD_FAST                'fut'
              154  LOAD_FAST                'sock'
              156  CALL_METHOD_2         2  ''
              158  POP_TOP          
            160_0  COME_FROM           146  '146'

 L. 377       160  LOAD_FAST                'self'
              162  LOAD_METHOD              add_writer
              164  LOAD_FAST                'fd'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _sock_sendfile_native_impl
              170  LOAD_FAST                'fut'

 L. 378       172  LOAD_FAST                'fd'
              174  LOAD_FAST                'sock'
              176  LOAD_FAST                'fileno'

 L. 379       178  LOAD_FAST                'offset'
              180  LOAD_FAST                'count'
              182  LOAD_FAST                'blocksize'
              184  LOAD_FAST                'total_sent'

 L. 377       186  CALL_METHOD_10       10  ''
              188  POP_TOP          
              190  POP_EXCEPT       
          192_194  JUMP_FORWARD        552  'to 552'

 L. 380       196  DUP_TOP          
              198  LOAD_GLOBAL              OSError
          200_202  <121>               362  ''
              204  POP_TOP          
              206  STORE_FAST               'exc'
              208  POP_TOP          
              210  SETUP_FINALLY       354  'to 354'

 L. 381       212  LOAD_FAST                'registered_fd'
              214  LOAD_CONST               None
              216  <117>                 1  ''
          218_220  POP_JUMP_IF_FALSE   272  'to 272'

 L. 382       222  LOAD_FAST                'exc'
              224  LOAD_ATTR                errno
              226  LOAD_GLOBAL              errno
              228  LOAD_ATTR                ENOTCONN
              230  COMPARE_OP               ==

 L. 381   232_234  POP_JUMP_IF_FALSE   272  'to 272'

 L. 383       236  LOAD_GLOBAL              type
              238  LOAD_FAST                'exc'
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_GLOBAL              ConnectionError
              244  <117>                 1  ''

 L. 381   246_248  POP_JUMP_IF_FALSE   272  'to 272'

 L. 388       250  LOAD_GLOBAL              ConnectionError

 L. 389       252  LOAD_STR                 'socket is not connected'
              254  LOAD_GLOBAL              errno
              256  LOAD_ATTR                ENOTCONN

 L. 388       258  CALL_FUNCTION_2       2  ''
              260  STORE_FAST               'new_exc'

 L. 390       262  LOAD_FAST                'exc'
              264  LOAD_FAST                'new_exc'
              266  STORE_ATTR               __cause__

 L. 391       268  LOAD_FAST                'new_exc'
              270  STORE_FAST               'exc'
            272_0  COME_FROM           246  '246'
            272_1  COME_FROM           232  '232'
            272_2  COME_FROM           218  '218'

 L. 392       272  LOAD_FAST                'total_sent'
              274  LOAD_CONST               0
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   318  'to 318'

 L. 397       282  LOAD_GLOBAL              exceptions
              284  LOAD_METHOD              SendfileNotAvailableError

 L. 398       286  LOAD_STR                 'os.sendfile call failed'

 L. 397       288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'err'

 L. 399       292  LOAD_FAST                'self'
              294  LOAD_METHOD              _sock_sendfile_update_filepos
              296  LOAD_FAST                'fileno'
              298  LOAD_FAST                'offset'
              300  LOAD_FAST                'total_sent'
              302  CALL_METHOD_3         3  ''
              304  POP_TOP          

 L. 400       306  LOAD_FAST                'fut'
              308  LOAD_METHOD              set_exception
              310  LOAD_FAST                'err'
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          
              316  JUMP_FORWARD        342  'to 342'
            318_0  COME_FROM           278  '278'

 L. 402       318  LOAD_FAST                'self'
              320  LOAD_METHOD              _sock_sendfile_update_filepos
              322  LOAD_FAST                'fileno'
              324  LOAD_FAST                'offset'
              326  LOAD_FAST                'total_sent'
              328  CALL_METHOD_3         3  ''
              330  POP_TOP          

 L. 403       332  LOAD_FAST                'fut'
              334  LOAD_METHOD              set_exception
              336  LOAD_FAST                'exc'
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          
            342_0  COME_FROM           316  '316'
              342  POP_BLOCK        
              344  POP_EXCEPT       
              346  LOAD_CONST               None
              348  STORE_FAST               'exc'
              350  DELETE_FAST              'exc'
              352  JUMP_FORWARD        552  'to 552'
            354_0  COME_FROM_FINALLY   210  '210'
              354  LOAD_CONST               None
              356  STORE_FAST               'exc'
              358  DELETE_FAST              'exc'
              360  <48>             

 L. 404       362  DUP_TOP          
              364  LOAD_GLOBAL              SystemExit
              366  LOAD_GLOBAL              KeyboardInterrupt
              368  BUILD_TUPLE_2         2 
          370_372  <121>               386  ''
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 405       380  RAISE_VARARGS_0       0  'reraise'
              382  POP_EXCEPT       
              384  JUMP_FORWARD        552  'to 552'

 L. 406       386  DUP_TOP          
              388  LOAD_GLOBAL              BaseException
          390_392  <121>               446  ''
              394  POP_TOP          
              396  STORE_FAST               'exc'
              398  POP_TOP          
              400  SETUP_FINALLY       438  'to 438'

 L. 407       402  LOAD_FAST                'self'
              404  LOAD_METHOD              _sock_sendfile_update_filepos
              406  LOAD_FAST                'fileno'
              408  LOAD_FAST                'offset'
              410  LOAD_FAST                'total_sent'
              412  CALL_METHOD_3         3  ''
              414  POP_TOP          

 L. 408       416  LOAD_FAST                'fut'
              418  LOAD_METHOD              set_exception
              420  LOAD_FAST                'exc'
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          
              426  POP_BLOCK        
              428  POP_EXCEPT       
              430  LOAD_CONST               None
              432  STORE_FAST               'exc'
              434  DELETE_FAST              'exc'
              436  JUMP_FORWARD        552  'to 552'
            438_0  COME_FROM_FINALLY   400  '400'
              438  LOAD_CONST               None
              440  STORE_FAST               'exc'
              442  DELETE_FAST              'exc'
              444  <48>             
              446  <48>             
            448_0  COME_FROM           120  '120'

 L. 410       448  LOAD_FAST                'sent'
              450  LOAD_CONST               0
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   484  'to 484'

 L. 412       458  LOAD_FAST                'self'
              460  LOAD_METHOD              _sock_sendfile_update_filepos
              462  LOAD_FAST                'fileno'
              464  LOAD_FAST                'offset'
              466  LOAD_FAST                'total_sent'
              468  CALL_METHOD_3         3  ''
              470  POP_TOP          

 L. 413       472  LOAD_FAST                'fut'
              474  LOAD_METHOD              set_result
              476  LOAD_FAST                'total_sent'
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          
              482  JUMP_FORWARD        552  'to 552'
            484_0  COME_FROM           454  '454'

 L. 415       484  LOAD_FAST                'offset'
              486  LOAD_FAST                'sent'
              488  INPLACE_ADD      
              490  STORE_FAST               'offset'

 L. 416       492  LOAD_FAST                'total_sent'
              494  LOAD_FAST                'sent'
              496  INPLACE_ADD      
              498  STORE_FAST               'total_sent'

 L. 417       500  LOAD_FAST                'registered_fd'
              502  LOAD_CONST               None
              504  <117>                 0  ''
          506_508  POP_JUMP_IF_FALSE   522  'to 522'

 L. 418       510  LOAD_FAST                'self'
              512  LOAD_METHOD              _sock_add_cancellation_callback
              514  LOAD_FAST                'fut'
              516  LOAD_FAST                'sock'
              518  CALL_METHOD_2         2  ''
              520  POP_TOP          
            522_0  COME_FROM           506  '506'

 L. 419       522  LOAD_FAST                'self'
              524  LOAD_METHOD              add_writer
              526  LOAD_FAST                'fd'
              528  LOAD_FAST                'self'
              530  LOAD_ATTR                _sock_sendfile_native_impl
              532  LOAD_FAST                'fut'

 L. 420       534  LOAD_FAST                'fd'
              536  LOAD_FAST                'sock'
              538  LOAD_FAST                'fileno'

 L. 421       540  LOAD_FAST                'offset'
              542  LOAD_FAST                'count'
              544  LOAD_FAST                'blocksize'
              546  LOAD_FAST                'total_sent'

 L. 419       548  CALL_METHOD_10       10  ''
              550  POP_TOP          
            552_0  COME_FROM           482  '482'
            552_1  COME_FROM           436  '436'
            552_2  COME_FROM           384  '384'
            552_3  COME_FROM           352  '352'
            552_4  COME_FROM           192  '192'

Parse error at or near `<117>' instruction at offset 12

    def _sock_sendfile_update_filepos(self, fileno, offset, total_sent):
        if total_sent > 0:
            os.lseekfilenooffsetos.SEEK_SET

    def _sock_add_cancellation_callback(self, fut, sock):

        def cb(fut):
            if fut.cancelled():
                fd = sock.fileno()
                if fd != -1:
                    self.remove_writer(fd)

        fut.add_done_callback(cb)


class _UnixReadPipeTransport(transports.ReadTransport):
    max_size = 262144

    def __init__--- This code section failed: ---

 L. 441         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 442        12  LOAD_FAST                'pipe'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _extra
               18  LOAD_STR                 'pipe'
               20  STORE_SUBSCR     

 L. 443        22  LOAD_FAST                'loop'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _loop

 L. 444        28  LOAD_FAST                'pipe'
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _pipe

 L. 445        34  LOAD_FAST                'pipe'
               36  LOAD_METHOD              fileno
               38  CALL_METHOD_0         0  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _fileno

 L. 446        44  LOAD_FAST                'protocol'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _protocol

 L. 447        50  LOAD_CONST               False
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _closing

 L. 448        56  LOAD_CONST               False
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _paused

 L. 450        62  LOAD_GLOBAL              os
               64  LOAD_METHOD              fstat
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                _fileno
               70  CALL_METHOD_1         1  ''
               72  LOAD_ATTR                st_mode
               74  STORE_FAST               'mode'

 L. 451        76  LOAD_GLOBAL              stat
               78  LOAD_METHOD              S_ISFIFO
               80  LOAD_FAST                'mode'
               82  CALL_METHOD_1         1  ''
               84  POP_JUMP_IF_TRUE    132  'to 132'

 L. 452        86  LOAD_GLOBAL              stat
               88  LOAD_METHOD              S_ISSOCK
               90  LOAD_FAST                'mode'
               92  CALL_METHOD_1         1  ''

 L. 451        94  POP_JUMP_IF_TRUE    132  'to 132'

 L. 453        96  LOAD_GLOBAL              stat
               98  LOAD_METHOD              S_ISCHR
              100  LOAD_FAST                'mode'
              102  CALL_METHOD_1         1  ''

 L. 451       104  POP_JUMP_IF_TRUE    132  'to 132'

 L. 454       106  LOAD_CONST               None
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _pipe

 L. 455       112  LOAD_CONST               None
              114  LOAD_FAST                'self'
              116  STORE_ATTR               _fileno

 L. 456       118  LOAD_CONST               None
              120  LOAD_FAST                'self'
              122  STORE_ATTR               _protocol

 L. 457       124  LOAD_GLOBAL              ValueError
              126  LOAD_STR                 'Pipe transport is for pipes/sockets only.'
              128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           104  '104'
            132_1  COME_FROM            94  '94'
            132_2  COME_FROM            84  '84'

 L. 459       132  LOAD_GLOBAL              os
              134  LOAD_METHOD              set_blocking
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                _fileno
              140  LOAD_CONST               False
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          

 L. 461       146  LOAD_FAST                'self'
              148  LOAD_ATTR                _loop
              150  LOAD_METHOD              call_soon
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _protocol
              156  LOAD_ATTR                connection_made
              158  LOAD_FAST                'self'
              160  CALL_METHOD_2         2  ''
              162  POP_TOP          

 L. 463       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _loop
              168  LOAD_METHOD              call_soon
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _loop
              174  LOAD_ATTR                _add_reader

 L. 464       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _fileno
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                _read_ready

 L. 463       184  CALL_METHOD_3         3  ''
              186  POP_TOP          

 L. 465       188  LOAD_FAST                'waiter'
              190  LOAD_CONST               None
              192  <117>                 1  ''
              194  POP_JUMP_IF_FALSE   214  'to 214'

 L. 467       196  LOAD_FAST                'self'
              198  LOAD_ATTR                _loop
              200  LOAD_METHOD              call_soon
              202  LOAD_GLOBAL              futures
              204  LOAD_ATTR                _set_result_unless_cancelled

 L. 468       206  LOAD_FAST                'waiter'
              208  LOAD_CONST               None

 L. 467       210  CALL_METHOD_3         3  ''
              212  POP_TOP          
            214_0  COME_FROM           194  '194'

Parse error at or near `<117>' instruction at offset 192

    def __repr__--- This code section failed: ---

 L. 471         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'info'

 L. 472        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pipe
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 473        20  LOAD_FAST                'info'
               22  LOAD_METHOD              append
               24  LOAD_STR                 'closed'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            18  '18'

 L. 474        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _closing
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 475        38  LOAD_FAST                'info'
               40  LOAD_METHOD              append
               42  LOAD_STR                 'closing'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'
             48_1  COME_FROM            30  '30'

 L. 476        48  LOAD_FAST                'info'
               50  LOAD_METHOD              append
               52  LOAD_STR                 'fd='
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _fileno
               58  FORMAT_VALUE          0  ''
               60  BUILD_STRING_2        2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 477        66  LOAD_GLOBAL              getattr
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _loop
               72  LOAD_STR                 '_selector'
               74  LOAD_CONST               None
               76  CALL_FUNCTION_3       3  ''
               78  STORE_FAST               'selector'

 L. 478        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _pipe
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   144  'to 144'
               90  LOAD_FAST                'selector'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   144  'to 144'

 L. 479        98  LOAD_GLOBAL              selector_events
              100  LOAD_METHOD              _test_selector_event

 L. 480       102  LOAD_FAST                'selector'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _fileno
              108  LOAD_GLOBAL              selectors
              110  LOAD_ATTR                EVENT_READ

 L. 479       112  CALL_METHOD_3         3  ''
              114  STORE_FAST               'polling'

 L. 481       116  LOAD_FAST                'polling'
              118  POP_JUMP_IF_FALSE   132  'to 132'

 L. 482       120  LOAD_FAST                'info'
              122  LOAD_METHOD              append
              124  LOAD_STR                 'polling'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  JUMP_FORWARD        176  'to 176'
            132_0  COME_FROM           118  '118'

 L. 484       132  LOAD_FAST                'info'
              134  LOAD_METHOD              append
              136  LOAD_STR                 'idle'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_FORWARD        176  'to 176'
            144_0  COME_FROM            96  '96'
            144_1  COME_FROM            88  '88'

 L. 485       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _pipe
              148  LOAD_CONST               None
              150  <117>                 1  ''
              152  POP_JUMP_IF_FALSE   166  'to 166'

 L. 486       154  LOAD_FAST                'info'
              156  LOAD_METHOD              append
              158  LOAD_STR                 'open'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_FORWARD        176  'to 176'
            166_0  COME_FROM           152  '152'

 L. 488       166  LOAD_FAST                'info'
              168  LOAD_METHOD              append
              170  LOAD_STR                 'closed'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
            176_0  COME_FROM           164  '164'
            176_1  COME_FROM           142  '142'
            176_2  COME_FROM           130  '130'

 L. 489       176  LOAD_STR                 '<{}>'
              178  LOAD_METHOD              format
              180  LOAD_STR                 ' '
              182  LOAD_METHOD              join
              184  LOAD_FAST                'info'
              186  CALL_METHOD_1         1  ''
              188  CALL_METHOD_1         1  ''
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def _read_ready--- This code section failed: ---

 L. 492         0  SETUP_FINALLY        22  'to 22'

 L. 493         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              read
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _fileno
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                max_size
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'data'
               18  POP_BLOCK        
               20  JUMP_FORWARD         90  'to 90'
             22_0  COME_FROM_FINALLY     0  '0'

 L. 494        22  DUP_TOP          
               24  LOAD_GLOBAL              BlockingIOError
               26  LOAD_GLOBAL              InterruptedError
               28  BUILD_TUPLE_2         2 
               30  <121>                42  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 495        38  POP_EXCEPT       
               40  JUMP_FORWARD        182  'to 182'

 L. 496        42  DUP_TOP          
               44  LOAD_GLOBAL              OSError
               46  <121>                88  ''
               48  POP_TOP          
               50  STORE_FAST               'exc'
               52  POP_TOP          
               54  SETUP_FINALLY        80  'to 80'

 L. 497        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _fatal_error
               60  LOAD_FAST                'exc'
               62  LOAD_STR                 'Fatal read error on pipe transport'
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  STORE_FAST               'exc'
               76  DELETE_FAST              'exc'
               78  JUMP_FORWARD        182  'to 182'
             80_0  COME_FROM_FINALLY    54  '54'
               80  LOAD_CONST               None
               82  STORE_FAST               'exc'
               84  DELETE_FAST              'exc'
               86  <48>             
               88  <48>             
             90_0  COME_FROM            20  '20'

 L. 499        90  LOAD_FAST                'data'
               92  POP_JUMP_IF_FALSE   108  'to 108'

 L. 500        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _protocol
               98  LOAD_METHOD              data_received
              100  LOAD_FAST                'data'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  JUMP_FORWARD        182  'to 182'
            108_0  COME_FROM            92  '92'

 L. 502       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _loop
              112  LOAD_METHOD              get_debug
              114  CALL_METHOD_0         0  ''
              116  POP_JUMP_IF_FALSE   130  'to 130'

 L. 503       118  LOAD_GLOBAL              logger
              120  LOAD_METHOD              info
              122  LOAD_STR                 '%r was closed by peer'
              124  LOAD_FAST                'self'
              126  CALL_METHOD_2         2  ''
              128  POP_TOP          
            130_0  COME_FROM           116  '116'

 L. 504       130  LOAD_CONST               True
              132  LOAD_FAST                'self'
              134  STORE_ATTR               _closing

 L. 505       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _loop
              140  LOAD_METHOD              _remove_reader
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _fileno
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 506       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _loop
              154  LOAD_METHOD              call_soon
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _protocol
              160  LOAD_ATTR                eof_received
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 507       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _loop
              170  LOAD_METHOD              call_soon
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _call_connection_lost
              176  LOAD_CONST               None
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          
            182_0  COME_FROM           106  '106'
            182_1  COME_FROM            78  '78'
            182_2  COME_FROM            40  '40'

Parse error at or near `<121>' instruction at offset 30

    def pause_reading(self):
        if self._closing or (self._paused):
            return
        self._paused = True
        self._loop._remove_reader(self._fileno)
        if self._loop.get_debug():
            logger.debug'%r pauses reading'self

    def resume_reading(self):
        if not (self._closing or self._paused):
            return
        self._paused = False
        self._loop._add_readerself._filenoself._read_ready
        if self._loop.get_debug():
            logger.debug'%r resumes reading'self

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close(self):
        if not self._closing:
            self._close(None)

    def __del__--- This code section failed: ---

 L. 539         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pipe
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    40  'to 40'

 L. 540        10  LOAD_FAST                '_warn'
               12  LOAD_STR                 'unclosed transport '
               14  LOAD_FAST                'self'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  LOAD_GLOBAL              ResourceWarning
               22  LOAD_FAST                'self'
               24  LOAD_CONST               ('source',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  POP_TOP          

 L. 541        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _pipe
               34  LOAD_METHOD              close
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
             40_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError) and exc.errno == errno.EIO:
            if self._loop.get_debug():
                logger.debug('%r: %s', self, message, exc_info=True)
        else:
            self._loop.call_exception_handler({'message':message, 
             'exception':exc, 
             'transport':self, 
             'protocol':self._protocol})
        self._close(exc)

    def _close(self, exc):
        self._closing = True
        self._loop._remove_reader(self._fileno)
        self._loop.call_soonself._call_connection_lostexc

    def _call_connection_lost--- This code section failed: ---

 L. 563         0  SETUP_FINALLY        46  'to 46'

 L. 564         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _protocol
                6  LOAD_METHOD              connection_lost
                8  LOAD_FAST                'exc'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        

 L. 566        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _pipe
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          

 L. 567        26  LOAD_CONST               None
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _pipe

 L. 568        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _protocol

 L. 569        38  LOAD_CONST               None
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _loop
               44  JUMP_FORWARD         76  'to 76'
             46_0  COME_FROM_FINALLY     0  '0'

 L. 566        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _pipe
               50  LOAD_METHOD              close
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L. 567        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _pipe

 L. 568        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _protocol

 L. 569        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _loop
               74  <48>             
             76_0  COME_FROM            44  '44'

Parse error at or near `POP_TOP' instruction at offset 24


class _UnixWritePipeTransport(transports._FlowControlMixin, transports.WriteTransport):

    def __init__--- This code section failed: ---

 L. 576         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  LOAD_FAST                'loop'
               10  CALL_METHOD_2         2  ''
               12  POP_TOP          

 L. 577        14  LOAD_FAST                'pipe'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _extra
               20  LOAD_STR                 'pipe'
               22  STORE_SUBSCR     

 L. 578        24  LOAD_FAST                'pipe'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _pipe

 L. 579        30  LOAD_FAST                'pipe'
               32  LOAD_METHOD              fileno
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _fileno

 L. 580        40  LOAD_FAST                'protocol'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _protocol

 L. 581        46  LOAD_GLOBAL              bytearray
               48  CALL_FUNCTION_0       0  ''
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _buffer

 L. 582        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _conn_lost

 L. 583        60  LOAD_CONST               False
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _closing

 L. 585        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              fstat
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _fileno
               74  CALL_METHOD_1         1  ''
               76  LOAD_ATTR                st_mode
               78  STORE_FAST               'mode'

 L. 586        80  LOAD_GLOBAL              stat
               82  LOAD_METHOD              S_ISCHR
               84  LOAD_FAST                'mode'
               86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'is_char'

 L. 587        90  LOAD_GLOBAL              stat
               92  LOAD_METHOD              S_ISFIFO
               94  LOAD_FAST                'mode'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'is_fifo'

 L. 588       100  LOAD_GLOBAL              stat
              102  LOAD_METHOD              S_ISSOCK
              104  LOAD_FAST                'mode'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'is_socket'

 L. 589       110  LOAD_FAST                'is_char'
              112  POP_JUMP_IF_TRUE    148  'to 148'
              114  LOAD_FAST                'is_fifo'
              116  POP_JUMP_IF_TRUE    148  'to 148'
              118  LOAD_FAST                'is_socket'
              120  POP_JUMP_IF_TRUE    148  'to 148'

 L. 590       122  LOAD_CONST               None
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _pipe

 L. 591       128  LOAD_CONST               None
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _fileno

 L. 592       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _protocol

 L. 593       140  LOAD_GLOBAL              ValueError
              142  LOAD_STR                 'Pipe transport is only for pipes, sockets and character devices'
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           120  '120'
            148_1  COME_FROM           116  '116'
            148_2  COME_FROM           112  '112'

 L. 596       148  LOAD_GLOBAL              os
              150  LOAD_METHOD              set_blocking
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _fileno
              156  LOAD_CONST               False
              158  CALL_METHOD_2         2  ''
              160  POP_TOP          

 L. 597       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _loop
              166  LOAD_METHOD              call_soon
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _protocol
              172  LOAD_ATTR                connection_made
              174  LOAD_FAST                'self'
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          

 L. 602       180  LOAD_FAST                'is_socket'
              182  POP_JUMP_IF_TRUE    200  'to 200'
              184  LOAD_FAST                'is_fifo'
              186  POP_JUMP_IF_FALSE   224  'to 224'
              188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                platform
              192  LOAD_METHOD              startswith
              194  LOAD_STR                 'aix'
              196  CALL_METHOD_1         1  ''
              198  POP_JUMP_IF_TRUE    224  'to 224'
            200_0  COME_FROM           182  '182'

 L. 604       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _loop
              204  LOAD_METHOD              call_soon
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _loop
              210  LOAD_ATTR                _add_reader

 L. 605       212  LOAD_FAST                'self'
              214  LOAD_ATTR                _fileno
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                _read_ready

 L. 604       220  CALL_METHOD_3         3  ''
              222  POP_TOP          
            224_0  COME_FROM           198  '198'
            224_1  COME_FROM           186  '186'

 L. 607       224  LOAD_FAST                'waiter'
              226  LOAD_CONST               None
              228  <117>                 1  ''
              230  POP_JUMP_IF_FALSE   250  'to 250'

 L. 609       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _loop
              236  LOAD_METHOD              call_soon
              238  LOAD_GLOBAL              futures
              240  LOAD_ATTR                _set_result_unless_cancelled

 L. 610       242  LOAD_FAST                'waiter'
              244  LOAD_CONST               None

 L. 609       246  CALL_METHOD_3         3  ''
              248  POP_TOP          
            250_0  COME_FROM           230  '230'

Parse error at or near `<117>' instruction at offset 228

    def __repr__--- This code section failed: ---

 L. 613         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'info'

 L. 614        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pipe
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 615        20  LOAD_FAST                'info'
               22  LOAD_METHOD              append
               24  LOAD_STR                 'closed'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            18  '18'

 L. 616        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _closing
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 617        38  LOAD_FAST                'info'
               40  LOAD_METHOD              append
               42  LOAD_STR                 'closing'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'
             48_1  COME_FROM            30  '30'

 L. 618        48  LOAD_FAST                'info'
               50  LOAD_METHOD              append
               52  LOAD_STR                 'fd='
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _fileno
               58  FORMAT_VALUE          0  ''
               60  BUILD_STRING_2        2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 619        66  LOAD_GLOBAL              getattr
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _loop
               72  LOAD_STR                 '_selector'
               74  LOAD_CONST               None
               76  CALL_FUNCTION_3       3  ''
               78  STORE_FAST               'selector'

 L. 620        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _pipe
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   168  'to 168'
               90  LOAD_FAST                'selector'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   168  'to 168'

 L. 621        98  LOAD_GLOBAL              selector_events
              100  LOAD_METHOD              _test_selector_event

 L. 622       102  LOAD_FAST                'selector'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _fileno
              108  LOAD_GLOBAL              selectors
              110  LOAD_ATTR                EVENT_WRITE

 L. 621       112  CALL_METHOD_3         3  ''
              114  STORE_FAST               'polling'

 L. 623       116  LOAD_FAST                'polling'
              118  POP_JUMP_IF_FALSE   132  'to 132'

 L. 624       120  LOAD_FAST                'info'
              122  LOAD_METHOD              append
              124  LOAD_STR                 'polling'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
              130  JUMP_FORWARD        142  'to 142'
            132_0  COME_FROM           118  '118'

 L. 626       132  LOAD_FAST                'info'
              134  LOAD_METHOD              append
              136  LOAD_STR                 'idle'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
            142_0  COME_FROM           130  '130'

 L. 628       142  LOAD_FAST                'self'
              144  LOAD_METHOD              get_write_buffer_size
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'bufsize'

 L. 629       150  LOAD_FAST                'info'
              152  LOAD_METHOD              append
              154  LOAD_STR                 'bufsize='
              156  LOAD_FAST                'bufsize'
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_2        2 
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
              166  JUMP_FORWARD        200  'to 200'
            168_0  COME_FROM            96  '96'
            168_1  COME_FROM            88  '88'

 L. 630       168  LOAD_FAST                'self'
              170  LOAD_ATTR                _pipe
              172  LOAD_CONST               None
              174  <117>                 1  ''
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L. 631       178  LOAD_FAST                'info'
              180  LOAD_METHOD              append
              182  LOAD_STR                 'open'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  JUMP_FORWARD        200  'to 200'
            190_0  COME_FROM           176  '176'

 L. 633       190  LOAD_FAST                'info'
              192  LOAD_METHOD              append
              194  LOAD_STR                 'closed'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           188  '188'
            200_1  COME_FROM           166  '166'

 L. 634       200  LOAD_STR                 '<{}>'
              202  LOAD_METHOD              format
              204  LOAD_STR                 ' '
              206  LOAD_METHOD              join
              208  LOAD_FAST                'info'
              210  CALL_METHOD_1         1  ''
              212  CALL_METHOD_1         1  ''
              214  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def get_write_buffer_size(self):
        return len(self._buffer)

    def _read_ready(self):
        if self._loop.get_debug():
            logger.info'%r was closed by peer'self
        if self._buffer:
            self._close(BrokenPipeError())
        else:
            self._close()

    def write--- This code section failed: ---

 L. 649         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              bytearray
                8  LOAD_GLOBAL              memoryview
               10  BUILD_TUPLE_3         3 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     28  'to 28'
               16  <74>             
               18  LOAD_GLOBAL              repr
               20  LOAD_FAST                'data'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            14  '14'

 L. 650        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'data'
               32  LOAD_GLOBAL              bytearray
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 651        38  LOAD_GLOBAL              memoryview
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'data'
             46_0  COME_FROM            36  '36'

 L. 652        46  LOAD_FAST                'data'
               48  POP_JUMP_IF_TRUE     54  'to 54'

 L. 653        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 655        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _conn_lost
               58  POP_JUMP_IF_TRUE     66  'to 66'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _closing
               64  POP_JUMP_IF_FALSE   106  'to 106'
             66_0  COME_FROM            58  '58'

 L. 656        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _conn_lost
               70  LOAD_GLOBAL              constants
               72  LOAD_ATTR                LOG_THRESHOLD_FOR_CONNLOST_WRITES
               74  COMPARE_OP               >=
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 657        78  LOAD_GLOBAL              logger
               80  LOAD_METHOD              warning
               82  LOAD_STR                 'pipe closed by peer or os.write(pipe, data) raised exception.'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            76  '76'

 L. 659        88  LOAD_FAST                'self'
               90  DUP_TOP          
               92  LOAD_ATTR                _conn_lost
               94  LOAD_CONST               1
               96  INPLACE_ADD      
               98  ROT_TWO          
              100  STORE_ATTR               _conn_lost

 L. 660       102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            64  '64'

 L. 662       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _buffer
          110_112  POP_JUMP_IF_TRUE    306  'to 306'

 L. 664       114  SETUP_FINALLY       134  'to 134'

 L. 665       116  LOAD_GLOBAL              os
              118  LOAD_METHOD              write
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _fileno
              124  LOAD_FAST                'data'
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'n'
              130  POP_BLOCK        
              132  JUMP_FORWARD        244  'to 244'
            134_0  COME_FROM_FINALLY   114  '114'

 L. 666       134  DUP_TOP          
              136  LOAD_GLOBAL              BlockingIOError
              138  LOAD_GLOBAL              InterruptedError
              140  BUILD_TUPLE_2         2 
              142  <121>               158  ''
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 667       150  LOAD_CONST               0
              152  STORE_FAST               'n'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        244  'to 244'

 L. 668       158  DUP_TOP          
              160  LOAD_GLOBAL              SystemExit
              162  LOAD_GLOBAL              KeyboardInterrupt
              164  BUILD_TUPLE_2         2 
              166  <121>               180  ''
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L. 669       174  RAISE_VARARGS_0       0  'reraise'
              176  POP_EXCEPT       
              178  JUMP_FORWARD        244  'to 244'

 L. 670       180  DUP_TOP          
              182  LOAD_GLOBAL              BaseException
              184  <121>               242  ''
              186  POP_TOP          
              188  STORE_FAST               'exc'
              190  POP_TOP          
              192  SETUP_FINALLY       234  'to 234'

 L. 671       194  LOAD_FAST                'self'
              196  DUP_TOP          
              198  LOAD_ATTR                _conn_lost
              200  LOAD_CONST               1
              202  INPLACE_ADD      
              204  ROT_TWO          
              206  STORE_ATTR               _conn_lost

 L. 672       208  LOAD_FAST                'self'
              210  LOAD_METHOD              _fatal_error
              212  LOAD_FAST                'exc'
              214  LOAD_STR                 'Fatal write error on pipe transport'
              216  CALL_METHOD_2         2  ''
              218  POP_TOP          

 L. 673       220  POP_BLOCK        
              222  POP_EXCEPT       
              224  LOAD_CONST               None
              226  STORE_FAST               'exc'
              228  DELETE_FAST              'exc'
              230  LOAD_CONST               None
              232  RETURN_VALUE     
            234_0  COME_FROM_FINALLY   192  '192'
              234  LOAD_CONST               None
              236  STORE_FAST               'exc'
              238  DELETE_FAST              'exc'
              240  <48>             
              242  <48>             
            244_0  COME_FROM           178  '178'
            244_1  COME_FROM           156  '156'
            244_2  COME_FROM           132  '132'

 L. 674       244  LOAD_FAST                'n'
              246  LOAD_GLOBAL              len
              248  LOAD_FAST                'data'
              250  CALL_FUNCTION_1       1  ''
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   262  'to 262'

 L. 675       258  LOAD_CONST               None
              260  RETURN_VALUE     
            262_0  COME_FROM           254  '254'

 L. 676       262  LOAD_FAST                'n'
              264  LOAD_CONST               0
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 677       272  LOAD_GLOBAL              memoryview
              274  LOAD_FAST                'data'
              276  CALL_FUNCTION_1       1  ''
              278  LOAD_FAST                'n'
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  STORE_FAST               'data'
            288_0  COME_FROM           268  '268'

 L. 678       288  LOAD_FAST                'self'
              290  LOAD_ATTR                _loop
              292  LOAD_METHOD              _add_writer
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                _fileno
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                _write_ready
              302  CALL_METHOD_2         2  ''
              304  POP_TOP          
            306_0  COME_FROM           110  '110'

 L. 680       306  LOAD_FAST                'self'
              308  DUP_TOP          
              310  LOAD_ATTR                _buffer
              312  LOAD_FAST                'data'
              314  INPLACE_ADD      
              316  ROT_TWO          
              318  STORE_ATTR               _buffer

 L. 681       320  LOAD_FAST                'self'
              322  LOAD_METHOD              _maybe_pause_protocol
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _write_ready--- This code section failed: ---

 L. 684         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _buffer
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  <74>             
                8  LOAD_STR                 'Data should not be empty'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 686        14  SETUP_FINALLY        36  'to 36'

 L. 687        16  LOAD_GLOBAL              os
               18  LOAD_METHOD              write
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _fileno
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _buffer
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'n'
               32  POP_BLOCK        
               34  JUMP_FORWARD        164  'to 164'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 688        36  DUP_TOP          
               38  LOAD_GLOBAL              BlockingIOError
               40  LOAD_GLOBAL              InterruptedError
               42  BUILD_TUPLE_2         2 
               44  <121>                56  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 689        52  POP_EXCEPT       
               54  JUMP_FORWARD        266  'to 266'

 L. 690        56  DUP_TOP          
               58  LOAD_GLOBAL              SystemExit
               60  LOAD_GLOBAL              KeyboardInterrupt
               62  BUILD_TUPLE_2         2 
               64  <121>                78  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 691        72  RAISE_VARARGS_0       0  'reraise'
               74  POP_EXCEPT       
               76  JUMP_FORWARD        266  'to 266'

 L. 692        78  DUP_TOP          
               80  LOAD_GLOBAL              BaseException
               82  <121>               162  ''
               84  POP_TOP          
               86  STORE_FAST               'exc'
               88  POP_TOP          
               90  SETUP_FINALLY       154  'to 154'

 L. 693        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _buffer
               96  LOAD_METHOD              clear
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          

 L. 694       102  LOAD_FAST                'self'
              104  DUP_TOP          
              106  LOAD_ATTR                _conn_lost
              108  LOAD_CONST               1
              110  INPLACE_ADD      
              112  ROT_TWO          
              114  STORE_ATTR               _conn_lost

 L. 697       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _loop
              120  LOAD_METHOD              _remove_writer
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                _fileno
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 698       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _fatal_error
              134  LOAD_FAST                'exc'
              136  LOAD_STR                 'Fatal write error on pipe transport'
              138  CALL_METHOD_2         2  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  POP_EXCEPT       
              146  LOAD_CONST               None
              148  STORE_FAST               'exc'
              150  DELETE_FAST              'exc'
              152  JUMP_FORWARD        266  'to 266'
            154_0  COME_FROM_FINALLY    90  '90'
              154  LOAD_CONST               None
              156  STORE_FAST               'exc'
              158  DELETE_FAST              'exc'
              160  <48>             
              162  <48>             
            164_0  COME_FROM            34  '34'

 L. 700       164  LOAD_FAST                'n'
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _buffer
              172  CALL_FUNCTION_1       1  ''
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   244  'to 244'

 L. 701       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _buffer
              182  LOAD_METHOD              clear
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          

 L. 702       188  LOAD_FAST                'self'
              190  LOAD_ATTR                _loop
              192  LOAD_METHOD              _remove_writer
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                _fileno
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 703       202  LOAD_FAST                'self'
              204  LOAD_METHOD              _maybe_resume_protocol
              206  CALL_METHOD_0         0  ''
              208  POP_TOP          

 L. 704       210  LOAD_FAST                'self'
              212  LOAD_ATTR                _closing
              214  POP_JUMP_IF_FALSE   240  'to 240'

 L. 705       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _loop
              220  LOAD_METHOD              _remove_reader
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                _fileno
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 706       230  LOAD_FAST                'self'
              232  LOAD_METHOD              _call_connection_lost
              234  LOAD_CONST               None
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           214  '214'

 L. 707       240  LOAD_CONST               None
              242  RETURN_VALUE     
            244_0  COME_FROM           176  '176'

 L. 708       244  LOAD_FAST                'n'
              246  LOAD_CONST               0
              248  COMPARE_OP               >
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L. 709       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _buffer
              258  LOAD_CONST               None
              260  LOAD_FAST                'n'
              262  BUILD_SLICE_2         2 
              264  DELETE_SUBSCR    
            266_0  COME_FROM           250  '250'
            266_1  COME_FROM           152  '152'
            266_2  COME_FROM            76  '76'
            266_3  COME_FROM            54  '54'

Parse error at or near `None' instruction at offset -1

    def can_write_eof(self):
        return True

    def write_eof--- This code section failed: ---

 L. 715         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closing
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 716         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 717        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pipe
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 718        20  LOAD_CONST               True
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _closing

 L. 719        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _buffer
               30  POP_JUMP_IF_TRUE     62  'to 62'

 L. 720        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _loop
               36  LOAD_METHOD              _remove_reader
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _fileno
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 721        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _loop
               50  LOAD_METHOD              call_soon
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _call_connection_lost
               56  LOAD_CONST               None
               58  CALL_METHOD_2         2  ''
               60  POP_TOP          
             62_0  COME_FROM            30  '30'

Parse error at or near `<74>' instruction at offset 16

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closing

    def close--- This code section failed: ---

 L. 733         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pipe
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closing
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L. 735        16  LOAD_FAST                'self'
               18  LOAD_METHOD              write_eof
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def __del__--- This code section failed: ---

 L. 738         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pipe
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    40  'to 40'

 L. 739        10  LOAD_FAST                '_warn'
               12  LOAD_STR                 'unclosed transport '
               14  LOAD_FAST                'self'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  LOAD_GLOBAL              ResourceWarning
               22  LOAD_FAST                'self'
               24  LOAD_CONST               ('source',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  POP_TOP          

 L. 740        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _pipe
               34  LOAD_METHOD              close
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
             40_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def abort(self):
        self._close(None)

    def _fatal_error(self, exc, message='Fatal error on pipe transport'):
        if isinstance(exc, OSError):
            if self._loop.get_debug():
                logger.debug('%r: %s', self, message, exc_info=True)
        else:
            self._loop.call_exception_handler({'message':message, 
             'exception':exc, 
             'transport':self, 
             'protocol':self._protocol})
        self._close(exc)

    def _close(self, exc=None):
        self._closing = True
        if self._buffer:
            self._loop._remove_writer(self._fileno)
        self._buffer.clear()
        self._loop._remove_reader(self._fileno)
        self._loop.call_soonself._call_connection_lostexc

    def _call_connection_lost--- This code section failed: ---

 L. 768         0  SETUP_FINALLY        46  'to 46'

 L. 769         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _protocol
                6  LOAD_METHOD              connection_lost
                8  LOAD_FAST                'exc'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        

 L. 771        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _pipe
               20  LOAD_METHOD              close
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          

 L. 772        26  LOAD_CONST               None
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _pipe

 L. 773        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _protocol

 L. 774        38  LOAD_CONST               None
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _loop
               44  JUMP_FORWARD         76  'to 76'
             46_0  COME_FROM_FINALLY     0  '0'

 L. 771        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _pipe
               50  LOAD_METHOD              close
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L. 772        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _pipe

 L. 773        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _protocol

 L. 774        68  LOAD_CONST               None
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _loop
               74  <48>             
             76_0  COME_FROM            44  '44'

Parse error at or near `POP_TOP' instruction at offset 24


class _UnixSubprocessTransport(base_subprocess.BaseSubprocessTransport):

    def _start--- This code section failed: ---

 L. 780         0  LOAD_CONST               None
                2  STORE_FAST               'stdin_w'

 L. 781         4  LOAD_FAST                'stdin'
                6  LOAD_GLOBAL              subprocess
                8  LOAD_ATTR                PIPE
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L. 787        14  LOAD_GLOBAL              socket
               16  LOAD_METHOD              socketpair
               18  CALL_METHOD_0         0  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'stdin'
               24  STORE_FAST               'stdin_w'
             26_0  COME_FROM            12  '12'

 L. 788        26  SETUP_FINALLY       132  'to 132'

 L. 789        28  LOAD_GLOBAL              subprocess
               30  LOAD_ATTR                Popen

 L. 790        32  LOAD_FAST                'args'

 L. 789        34  BUILD_TUPLE_1         1 

 L. 790        36  LOAD_FAST                'shell'
               38  LOAD_FAST                'stdin'
               40  LOAD_FAST                'stdout'
               42  LOAD_FAST                'stderr'

 L. 791        44  LOAD_CONST               False
               46  LOAD_FAST                'bufsize'

 L. 789        48  LOAD_CONST               ('shell', 'stdin', 'stdout', 'stderr', 'universal_newlines', 'bufsize')
               50  BUILD_CONST_KEY_MAP_6     6 

 L. 791        52  LOAD_FAST                'kwargs'

 L. 789        54  <164>                 1  ''
               56  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _proc

 L. 792        62  LOAD_FAST                'stdin_w'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE   104  'to 104'

 L. 793        70  LOAD_FAST                'stdin'
               72  LOAD_METHOD              close
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          

 L. 794        78  LOAD_GLOBAL              open
               80  LOAD_FAST                'stdin_w'
               82  LOAD_METHOD              detach
               84  CALL_METHOD_0         0  ''
               86  LOAD_STR                 'wb'
               88  LOAD_FAST                'bufsize'
               90  LOAD_CONST               ('buffering',)
               92  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _proc
               98  STORE_ATTR               stdin

 L. 795       100  LOAD_CONST               None
              102  STORE_FAST               'stdin_w'
            104_0  COME_FROM            68  '68'
              104  POP_BLOCK        

 L. 797       106  LOAD_FAST                'stdin_w'
              108  LOAD_CONST               None
              110  <117>                 1  ''
              112  POP_JUMP_IF_FALSE   158  'to 158'

 L. 798       114  LOAD_FAST                'stdin'
              116  LOAD_METHOD              close
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          

 L. 799       122  LOAD_FAST                'stdin_w'
              124  LOAD_METHOD              close
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          
              130  JUMP_FORWARD        158  'to 158'
            132_0  COME_FROM_FINALLY    26  '26'

 L. 797       132  LOAD_FAST                'stdin_w'
              134  LOAD_CONST               None
              136  <117>                 1  ''
              138  POP_JUMP_IF_FALSE   156  'to 156'

 L. 798       140  LOAD_FAST                'stdin'
              142  LOAD_METHOD              close
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

 L. 799       148  LOAD_FAST                'stdin_w'
              150  LOAD_METHOD              close
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          
            156_0  COME_FROM           138  '138'
              156  <48>             
            158_0  COME_FROM           130  '130'
            158_1  COME_FROM           112  '112'

Parse error at or near `<164>' instruction at offset 54


class AbstractChildWatcher:
    __doc__ = 'Abstract base class for monitoring child processes.\n\n    Objects derived from this class monitor a collection of subprocesses and\n    report their termination or interruption by a signal.\n\n    New callbacks are registered with .add_child_handler(). Starting a new\n    process must be done within a \'with\' block to allow the watcher to suspend\n    its activity until the new process if fully registered (this is needed to\n    prevent a race condition in some implementations).\n\n    Example:\n        with watcher:\n            proc = subprocess.Popen("sleep 1")\n            watcher.add_child_handler(proc.pid, callback)\n\n    Notes:\n        Implementations of this class must be thread-safe.\n\n        Since child watcher objects may catch the SIGCHLD signal and call\n        waitpid(-1), there should be only one active object per process.\n    '

    def add_child_handler(self, pid, callback, *args):
        """Register a new child handler.

        Arrange for callback(pid, returncode, *args) to be called when
        process 'pid' terminates. Specifying another callback for the same
        process replaces the previous handler.

        Note: callback() must be thread-safe.
        """
        raise NotImplementedError()

    def remove_child_handler(self, pid):
        """Removes the handler for process 'pid'.

        The function returns True if the handler was successfully removed,
        False if there was nothing to remove."""
        raise NotImplementedError()

    def attach_loop(self, loop):
        """Attach the watcher to an event loop.

        If the watcher was previously attached to an event loop, then it is
        first detached before attaching to the new loop.

        Note: loop may be None.
        """
        raise NotImplementedError()

    def close(self):
        """Close the watcher.

        This must be called to make sure that any underlying resource is freed.
        """
        raise NotImplementedError()

    def is_active(self):
        """Return ``True`` if the watcher is active and is used by the event loop.

        Return True if the watcher is installed and ready to handle process exit
        notifications.

        """
        raise NotImplementedError()

    def __enter__(self):
        """Enter the watcher's context and allow starting new processes

        This function must return self"""
        raise NotImplementedError()

    def __exit__(self, a, b, c):
        """Exit the watcher's context"""
        raise NotImplementedError()


class PidfdChildWatcher(AbstractChildWatcher):
    __doc__ = 'Child watcher implementation using Linux\'s pid file descriptors.\n\n    This child watcher polls process file descriptors (pidfds) to await child\n    process termination. In some respects, PidfdChildWatcher is a "Goldilocks"\n    child watcher implementation. It doesn\'t require signals or threads, doesn\'t\n    interfere with any processes launched outside the event loop, and scales\n    linearly with the number of subprocesses launched by the event loop. The\n    main disadvantage is that pidfds are specific to Linux, and only work on\n    recent (5.3+) kernels.\n    '

    def __init__(self):
        self._loop = None
        self._callbacks = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def is_active--- This code section failed: ---

 L. 904         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  JUMP_IF_FALSE_OR_POP    18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              is_running
               16  CALL_METHOD_0         0  ''
             18_0  COME_FROM             8  '8'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def close(self):
        self.attach_loop(None)

    def attach_loop--- This code section failed: ---

 L. 910         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    36  'to 36'
               10  LOAD_FAST                'loop'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    36  'to 36'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _callbacks
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 911        24  LOAD_GLOBAL              warnings
               26  LOAD_METHOD              warn

 L. 912        28  LOAD_STR                 'A loop is being detached from a child watcher with pending handlers'

 L. 914        30  LOAD_GLOBAL              RuntimeWarning

 L. 911        32  CALL_METHOD_2         2  ''
               34  POP_TOP          
             36_0  COME_FROM            22  '22'
             36_1  COME_FROM            16  '16'
             36_2  COME_FROM             8  '8'

 L. 915        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _callbacks
               40  LOAD_METHOD              values
               42  CALL_METHOD_0         0  ''
               44  GET_ITER         
             46_0  COME_FROM            78  '78'
               46  FOR_ITER             80  'to 80'
               48  UNPACK_SEQUENCE_3     3 
               50  STORE_FAST               'pidfd'
               52  STORE_FAST               '_'
               54  STORE_FAST               '_'

 L. 916        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _loop
               60  LOAD_METHOD              _remove_reader
               62  LOAD_FAST                'pidfd'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 917        68  LOAD_GLOBAL              os
               70  LOAD_METHOD              close
               72  LOAD_FAST                'pidfd'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_BACK            46  'to 46'
             80_0  COME_FROM            46  '46'

 L. 918        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _callbacks
               84  LOAD_METHOD              clear
               86  CALL_METHOD_0         0  ''
               88  POP_TOP          

 L. 919        90  LOAD_FAST                'loop'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _loop

Parse error at or near `None' instruction at offset -1

    def add_child_handler--- This code section failed: ---

 L. 922         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _callbacks
                4  LOAD_METHOD              get
                6  LOAD_FAST                'pid'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'existing'

 L. 923        12  LOAD_FAST                'existing'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    42  'to 42'

 L. 924        20  LOAD_FAST                'existing'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  LOAD_FAST                'callback'
               28  LOAD_FAST                'args'
               30  BUILD_TUPLE_3         3 
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _callbacks
               36  LOAD_FAST                'pid'
               38  STORE_SUBSCR     
               40  JUMP_FORWARD         86  'to 86'
             42_0  COME_FROM            18  '18'

 L. 926        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              pidfd_open
               46  LOAD_FAST                'pid'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'pidfd'

 L. 927        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _loop
               56  LOAD_METHOD              _add_reader
               58  LOAD_FAST                'pidfd'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _do_wait
               64  LOAD_FAST                'pid'
               66  CALL_METHOD_3         3  ''
               68  POP_TOP          

 L. 928        70  LOAD_FAST                'pidfd'
               72  LOAD_FAST                'callback'
               74  LOAD_FAST                'args'
               76  BUILD_TUPLE_3         3 
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _callbacks
               82  LOAD_FAST                'pid'
               84  STORE_SUBSCR     
             86_0  COME_FROM            40  '40'

Parse error at or near `<117>' instruction at offset 16

    def _do_wait--- This code section failed: ---

 L. 931         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _callbacks
                4  LOAD_METHOD              pop
                6  LOAD_FAST                'pid'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'pidfd'
               14  STORE_FAST               'callback'
               16  STORE_FAST               'args'

 L. 932        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _loop
               22  LOAD_METHOD              _remove_reader
               24  LOAD_FAST                'pidfd'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 933        30  SETUP_FINALLY        52  'to 52'

 L. 934        32  LOAD_GLOBAL              os
               34  LOAD_METHOD              waitpid
               36  LOAD_FAST                'pid'
               38  LOAD_CONST               0
               40  CALL_METHOD_2         2  ''
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               '_'
               46  STORE_FAST               'status'
               48  POP_BLOCK        
               50  JUMP_FORWARD         86  'to 86'
             52_0  COME_FROM_FINALLY    30  '30'

 L. 935        52  DUP_TOP          
               54  LOAD_GLOBAL              ChildProcessError
               56  <121>                84  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 938        64  LOAD_CONST               255
               66  STORE_FAST               'returncode'

 L. 939        68  LOAD_GLOBAL              logger
               70  LOAD_METHOD              warning

 L. 940        72  LOAD_STR                 'child process pid %d exit status already read:  will report returncode 255'

 L. 942        74  LOAD_FAST                'pid'

 L. 939        76  CALL_METHOD_2         2  ''
               78  POP_TOP          
               80  POP_EXCEPT       
               82  JUMP_FORWARD         94  'to 94'
               84  <48>             
             86_0  COME_FROM            50  '50'

 L. 944        86  LOAD_GLOBAL              _compute_returncode
               88  LOAD_FAST                'status'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'returncode'
             94_0  COME_FROM            82  '82'

 L. 946        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              close
               98  LOAD_FAST                'pidfd'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 947       104  LOAD_FAST                'callback'
              106  LOAD_FAST                'pid'
              108  LOAD_FAST                'returncode'
              110  BUILD_LIST_2          2 
              112  LOAD_FAST                'args'
              114  CALL_FINALLY        117  'to 117'
              116  WITH_CLEANUP_FINISH
              118  CALL_FUNCTION_EX      0  'positional arguments only'
              120  POP_TOP          

Parse error at or near `<121>' instruction at offset 56

    def remove_child_handler--- This code section failed: ---

 L. 950         0  SETUP_FINALLY        24  'to 24'

 L. 951         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_METHOD              pop
                8  LOAD_FAST                'pid'
               10  CALL_METHOD_1         1  ''
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'pidfd'
               16  STORE_FAST               '_'
               18  STORE_FAST               '_'
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 952        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 953        36  POP_EXCEPT       
               38  LOAD_CONST               False
               40  RETURN_VALUE     
               42  <48>             
             44_0  COME_FROM            22  '22'

 L. 954        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _loop
               48  LOAD_METHOD              _remove_reader
               50  LOAD_FAST                'pidfd'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 955        56  LOAD_GLOBAL              os
               58  LOAD_METHOD              close
               60  LOAD_FAST                'pidfd'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 956        66  LOAD_CONST               True
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 28


def _compute_returncode(status):
    if os.WIFSIGNALED(status):
        return -os.WTERMSIG(status)
    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)
    return status


class BaseChildWatcher(AbstractChildWatcher):

    def __init__(self):
        self._loop = None
        self._callbacks = {}

    def close(self):
        self.attach_loop(None)

    def is_active--- This code section failed: ---

 L. 983         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  JUMP_IF_FALSE_OR_POP    18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _loop
               14  LOAD_METHOD              is_running
               16  CALL_METHOD_0         0  ''
             18_0  COME_FROM             8  '8'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _do_waitpid(self, expected_pid):
        raise NotImplementedError()

    def _do_waitpid_all(self):
        raise NotImplementedError()

    def attach_loop--- This code section failed: ---

 L. 992         0  LOAD_FAST                'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     24  'to 24'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'loop'
               12  LOAD_GLOBAL              events
               14  LOAD_ATTR                AbstractEventLoop
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM             6  '6'

 L. 994        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _loop
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    60  'to 60'
               34  LOAD_FAST                'loop'
               36  LOAD_CONST               None
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    60  'to 60'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _callbacks
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L. 995        48  LOAD_GLOBAL              warnings
               50  LOAD_METHOD              warn

 L. 996        52  LOAD_STR                 'A loop is being detached from a child watcher with pending handlers'

 L. 998        54  LOAD_GLOBAL              RuntimeWarning

 L. 995        56  CALL_METHOD_2         2  ''
               58  POP_TOP          
             60_0  COME_FROM            46  '46'
             60_1  COME_FROM            40  '40'
             60_2  COME_FROM            32  '32'

 L.1000        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _loop
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    84  'to 84'

 L.1001        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _loop
               74  LOAD_METHOD              remove_signal_handler
               76  LOAD_GLOBAL              signal
               78  LOAD_ATTR                SIGCHLD
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
             84_0  COME_FROM            68  '68'

 L.1003        84  LOAD_FAST                'loop'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _loop

 L.1004        90  LOAD_FAST                'loop'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   122  'to 122'

 L.1005        98  LOAD_FAST                'loop'
              100  LOAD_METHOD              add_signal_handler
              102  LOAD_GLOBAL              signal
              104  LOAD_ATTR                SIGCHLD
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _sig_chld
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          

 L.1009       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _do_waitpid_all
              118  CALL_METHOD_0         0  ''
              120  POP_TOP          
            122_0  COME_FROM            96  '96'

Parse error at or near `None' instruction at offset -1

    def _sig_chld--- This code section failed: ---

 L.1012         0  SETUP_FINALLY        14  'to 14'

 L.1013         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _do_waitpid_all
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         90  'to 90'
             14_0  COME_FROM_FINALLY     0  '0'

 L.1014        14  DUP_TOP          
               16  LOAD_GLOBAL              SystemExit
               18  LOAD_GLOBAL              KeyboardInterrupt
               20  BUILD_TUPLE_2         2 
               22  <121>                36  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1015        30  RAISE_VARARGS_0       0  'reraise'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         90  'to 90'

 L.1016        36  DUP_TOP          
               38  LOAD_GLOBAL              BaseException
               40  <121>                88  ''
               42  POP_TOP          
               44  STORE_FAST               'exc'
               46  POP_TOP          
               48  SETUP_FINALLY        80  'to 80'

 L.1020        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _loop
               54  LOAD_METHOD              call_exception_handler

 L.1021        56  LOAD_STR                 'Unknown exception in SIGCHLD handler'

 L.1022        58  LOAD_FAST                'exc'

 L.1020        60  LOAD_CONST               ('message', 'exception')
               62  BUILD_CONST_KEY_MAP_2     2 
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  STORE_FAST               'exc'
               76  DELETE_FAST              'exc'
               78  JUMP_FORWARD         90  'to 90'
             80_0  COME_FROM_FINALLY    48  '48'
               80  LOAD_CONST               None
               82  STORE_FAST               'exc'
               84  DELETE_FAST              'exc'
               86  <48>             
               88  <48>             
             90_0  COME_FROM            78  '78'
             90_1  COME_FROM            34  '34'
             90_2  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 22


class SafeChildWatcher(BaseChildWatcher):
    __doc__ = "'Safe' child watcher implementation.\n\n    This implementation avoids disrupting other code spawning processes by\n    polling explicitly each process in the SIGCHLD handler instead of calling\n    os.waitpid(-1).\n\n    This is a safe solution but it has a significant overhead when handling a\n    big number of children (O(n) each time SIGCHLD is raised)\n    "

    def close(self):
        self._callbacks.clear()
        super().close()

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def add_child_handler(self, pid, callback, *args):
        self._callbacks[pid] = (
         callback, args)
        self._do_waitpid(pid)

    def remove_child_handler--- This code section failed: ---

 L.1054         0  SETUP_FINALLY        16  'to 16'

 L.1055         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L.1056        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1057        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                34  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1058        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
               34  <48>             

Parse error at or near `DUP_TOP' instruction at offset 16

    def _do_waitpid_all(self):
        for pid in list(self._callbacks):
            self._do_waitpid(pid)

    def _do_waitpid--- This code section failed: ---

 L.1066         0  LOAD_FAST                'expected_pid'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L.1068        12  SETUP_FINALLY        36  'to 36'

 L.1069        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              waitpid
               18  LOAD_FAST                'expected_pid'
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                WNOHANG
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'pid'
               30  STORE_FAST               'status'
               32  POP_BLOCK        
               34  JUMP_FORWARD         74  'to 74'
             36_0  COME_FROM_FINALLY    12  '12'

 L.1070        36  DUP_TOP          
               38  LOAD_GLOBAL              ChildProcessError
               40  <121>                72  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1073        48  LOAD_FAST                'expected_pid'
               50  STORE_FAST               'pid'

 L.1074        52  LOAD_CONST               255
               54  STORE_FAST               'returncode'

 L.1075        56  LOAD_GLOBAL              logger
               58  LOAD_METHOD              warning

 L.1076        60  LOAD_STR                 'Unknown child process pid %d, will report returncode 255'

 L.1077        62  LOAD_FAST                'pid'

 L.1075        64  CALL_METHOD_2         2  ''
               66  POP_TOP          
               68  POP_EXCEPT       
               70  JUMP_FORWARD        118  'to 118'
               72  <48>             
             74_0  COME_FROM            34  '34'

 L.1079        74  LOAD_FAST                'pid'
               76  LOAD_CONST               0
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L.1081        82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'

 L.1083        86  LOAD_GLOBAL              _compute_returncode
               88  LOAD_FAST                'status'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'returncode'

 L.1084        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _loop
               98  LOAD_METHOD              get_debug
              100  CALL_METHOD_0         0  ''
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L.1085       104  LOAD_GLOBAL              logger
              106  LOAD_METHOD              debug
              108  LOAD_STR                 'process %s exited with returncode %s'

 L.1086       110  LOAD_FAST                'expected_pid'
              112  LOAD_FAST                'returncode'

 L.1085       114  CALL_METHOD_3         3  ''
              116  POP_TOP          
            118_0  COME_FROM           102  '102'
            118_1  COME_FROM            70  '70'

 L.1088       118  SETUP_FINALLY       140  'to 140'

 L.1089       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _callbacks
              124  LOAD_METHOD              pop
              126  LOAD_FAST                'pid'
              128  CALL_METHOD_1         1  ''
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'callback'
              134  STORE_FAST               'args'
              136  POP_BLOCK        
              138  JUMP_FORWARD        184  'to 184'
            140_0  COME_FROM_FINALLY   118  '118'

 L.1090       140  DUP_TOP          
              142  LOAD_GLOBAL              KeyError
              144  <121>               182  ''
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L.1093       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _loop
              156  LOAD_METHOD              get_debug
              158  CALL_METHOD_0         0  ''
              160  POP_JUMP_IF_FALSE   178  'to 178'

 L.1094       162  LOAD_GLOBAL              logger
              164  LOAD_ATTR                warning
              166  LOAD_STR                 'Child watcher got an unexpected pid: %r'

 L.1095       168  LOAD_FAST                'pid'
              170  LOAD_CONST               True

 L.1094       172  LOAD_CONST               ('exc_info',)
              174  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              176  POP_TOP          
            178_0  COME_FROM           160  '160'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        202  'to 202'
              182  <48>             
            184_0  COME_FROM           138  '138'

 L.1097       184  LOAD_FAST                'callback'
              186  LOAD_FAST                'pid'
              188  LOAD_FAST                'returncode'
              190  BUILD_LIST_2          2 
              192  LOAD_FAST                'args'
              194  CALL_FINALLY        197  'to 197'
              196  WITH_CLEANUP_FINISH
              198  CALL_FUNCTION_EX      0  'positional arguments only'
              200  POP_TOP          
            202_0  COME_FROM           180  '180'

Parse error at or near `None' instruction at offset -1


class FastChildWatcher(BaseChildWatcher):
    __doc__ = "'Fast' child watcher implementation.\n\n    This implementation reaps every terminated processes by calling\n    os.waitpid(-1) directly, possibly breaking other code spawning processes\n    and waiting for their termination.\n\n    There is no noticeable overhead when handling a big number of children\n    (O(1) each time a child terminates).\n    "

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._zombies = {}
        self._forks = 0

    def close(self):
        self._callbacks.clear()
        self._zombies.clear()
        super().close()

    def __enter__--- This code section failed: ---

 L.1122         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           40  'to 40'
                6  POP_TOP          

 L.1123         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _forks
               14  LOAD_CONST               1
               16  INPLACE_ADD      
               18  ROT_TWO          
               20  STORE_ATTR               _forks

 L.1125        22  LOAD_FAST                'self'
               24  POP_BLOCK        
               26  ROT_TWO          
               28  LOAD_CONST               None
               30  DUP_TOP          
               32  DUP_TOP          
               34  CALL_FUNCTION_3       3  ''
               36  POP_TOP          
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH        4  '4'
               40  <49>             
               42  POP_JUMP_IF_TRUE     46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          
               52  POP_EXCEPT       
               54  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 28

    def __exit__--- This code section failed: ---

 L.1128         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           84  'to 84'
                6  POP_TOP          

 L.1129         8  LOAD_FAST                'self'
               10  DUP_TOP          
               12  LOAD_ATTR                _forks
               14  LOAD_CONST               1
               16  INPLACE_SUBTRACT 
               18  ROT_TWO          
               20  STORE_ATTR               _forks

 L.1131        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _forks
               26  POP_JUMP_IF_TRUE     34  'to 34'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _zombies
               32  POP_JUMP_IF_TRUE     50  'to 50'
             34_0  COME_FROM            26  '26'

 L.1132        34  POP_BLOCK        
               36  LOAD_CONST               None
               38  DUP_TOP          
               40  DUP_TOP          
               42  CALL_FUNCTION_3       3  ''
               44  POP_TOP          
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            32  '32'

 L.1134        50  LOAD_GLOBAL              str
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _zombies
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'collateral_victims'

 L.1135        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _zombies
               64  LOAD_METHOD              clear
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          
               70  POP_BLOCK        
               72  LOAD_CONST               None
               74  DUP_TOP          
               76  DUP_TOP          
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_FORWARD        100  'to 100'
             84_0  COME_FROM_WITH        4  '4'
               84  <49>             
               86  POP_JUMP_IF_TRUE     90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          
               96  POP_EXCEPT       
               98  POP_TOP          
            100_0  COME_FROM            82  '82'

 L.1137       100  LOAD_GLOBAL              logger
              102  LOAD_METHOD              warning

 L.1138       104  LOAD_STR                 'Caught subprocesses termination from unknown pids: %s'

 L.1139       106  LOAD_FAST                'collateral_victims'

 L.1137       108  CALL_METHOD_2         2  ''
              110  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 36

    def add_child_handler--- This code section failed: ---

 L.1142         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _forks
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  <74>             
                8  LOAD_STR                 'Must use the context manager'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L.1144        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _lock
               18  SETUP_WITH          100  'to 100'
               20  POP_TOP          

 L.1145        22  SETUP_FINALLY        40  'to 40'

 L.1146        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _zombies
               28  LOAD_METHOD              pop
               30  LOAD_FAST                'pid'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'returncode'
               36  POP_BLOCK        
               38  JUMP_FORWARD         86  'to 86'
             40_0  COME_FROM_FINALLY    22  '22'

 L.1147        40  DUP_TOP          
               42  LOAD_GLOBAL              KeyError
               44  <121>                84  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.1149        52  LOAD_FAST                'callback'
               54  LOAD_FAST                'args'
               56  BUILD_TUPLE_2         2 
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _callbacks
               62  LOAD_FAST                'pid'
               64  STORE_SUBSCR     

 L.1150        66  POP_EXCEPT       
               68  POP_BLOCK        
               70  LOAD_CONST               None
               72  DUP_TOP          
               74  DUP_TOP          
               76  CALL_FUNCTION_3       3  ''
               78  POP_TOP          
               80  LOAD_CONST               None
               82  RETURN_VALUE     
               84  <48>             
             86_0  COME_FROM            38  '38'
               86  POP_BLOCK        
               88  LOAD_CONST               None
               90  DUP_TOP          
               92  DUP_TOP          
               94  CALL_FUNCTION_3       3  ''
               96  POP_TOP          
               98  JUMP_FORWARD        116  'to 116'
            100_0  COME_FROM_WITH       18  '18'
              100  <49>             
              102  POP_JUMP_IF_TRUE    106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          
              112  POP_EXCEPT       
              114  POP_TOP          
            116_0  COME_FROM            98  '98'

 L.1153       116  LOAD_FAST                'callback'
              118  LOAD_FAST                'pid'
              120  LOAD_FAST                'returncode'
              122  BUILD_LIST_2          2 
              124  LOAD_FAST                'args'
              126  CALL_FINALLY        129  'to 129'
              128  WITH_CLEANUP_FINISH
              130  CALL_FUNCTION_EX      0  'positional arguments only'
              132  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def remove_child_handler--- This code section failed: ---

 L.1156         0  SETUP_FINALLY        16  'to 16'

 L.1157         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L.1158        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1159        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                34  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1160        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
               34  <48>             

Parse error at or near `DUP_TOP' instruction at offset 16

    def _do_waitpid_all--- This code section failed: ---
              0_0  COME_FROM           268  '268'
              0_1  COME_FROM           248  '248'
              0_2  COME_FROM           160  '160'

 L.1166         0  SETUP_FINALLY        24  'to 24'

 L.1167         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              waitpid
                6  LOAD_CONST               -1
                8  LOAD_GLOBAL              os
               10  LOAD_ATTR                WNOHANG
               12  CALL_METHOD_2         2  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'pid'
               18  STORE_FAST               'status'
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     0  '0'

 L.1168        24  DUP_TOP          
               26  LOAD_GLOBAL              ChildProcessError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.1170        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
               42  <48>             
             44_0  COME_FROM            22  '22'

 L.1172        44  LOAD_FAST                'pid'
               46  LOAD_CONST               0
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L.1174        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L.1176        56  LOAD_GLOBAL              _compute_returncode
               58  LOAD_FAST                'status'
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'returncode'

 L.1178        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _lock
               68  SETUP_WITH          210  'to 210'
               70  POP_TOP          

 L.1179        72  SETUP_FINALLY        94  'to 94'

 L.1180        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _callbacks
               78  LOAD_METHOD              pop
               80  LOAD_FAST                'pid'
               82  CALL_METHOD_1         1  ''
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'callback'
               88  STORE_FAST               'args'
               90  POP_BLOCK        
               92  JUMP_FORWARD        172  'to 172'
             94_0  COME_FROM_FINALLY    72  '72'

 L.1181        94  DUP_TOP          
               96  LOAD_GLOBAL              KeyError
               98  <121>               170  ''
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.1183       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _forks
              110  POP_JUMP_IF_FALSE   162  'to 162'

 L.1185       112  LOAD_FAST                'returncode'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _zombies
              118  LOAD_FAST                'pid'
              120  STORE_SUBSCR     

 L.1186       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _loop
              126  LOAD_METHOD              get_debug
              128  CALL_METHOD_0         0  ''
              130  POP_JUMP_IF_FALSE   146  'to 146'

 L.1187       132  LOAD_GLOBAL              logger
              134  LOAD_METHOD              debug
              136  LOAD_STR                 'unknown process %s exited with returncode %s'

 L.1189       138  LOAD_FAST                'pid'
              140  LOAD_FAST                'returncode'

 L.1187       142  CALL_METHOD_3         3  ''
              144  POP_TOP          
            146_0  COME_FROM           130  '130'

 L.1190       146  POP_EXCEPT       
              148  POP_BLOCK        
              150  LOAD_CONST               None
              152  DUP_TOP          
              154  DUP_TOP          
              156  CALL_FUNCTION_3       3  ''
              158  POP_TOP          
              160  JUMP_BACK             0  'to 0'
            162_0  COME_FROM           110  '110'

 L.1191       162  LOAD_CONST               None
              164  STORE_FAST               'callback'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        196  'to 196'
              170  <48>             
            172_0  COME_FROM            92  '92'

 L.1193       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _loop
              176  LOAD_METHOD              get_debug
              178  CALL_METHOD_0         0  ''
              180  POP_JUMP_IF_FALSE   196  'to 196'

 L.1194       182  LOAD_GLOBAL              logger
              184  LOAD_METHOD              debug
              186  LOAD_STR                 'process %s exited with returncode %s'

 L.1195       188  LOAD_FAST                'pid'
              190  LOAD_FAST                'returncode'

 L.1194       192  CALL_METHOD_3         3  ''
              194  POP_TOP          
            196_0  COME_FROM           180  '180'
            196_1  COME_FROM           168  '168'
              196  POP_BLOCK        
              198  LOAD_CONST               None
              200  DUP_TOP          
              202  DUP_TOP          
              204  CALL_FUNCTION_3       3  ''
              206  POP_TOP          
              208  JUMP_FORWARD        226  'to 226'
            210_0  COME_FROM_WITH       68  '68'
              210  <49>             
              212  POP_JUMP_IF_TRUE    216  'to 216'
              214  <48>             
            216_0  COME_FROM           212  '212'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          
              222  POP_EXCEPT       
              224  POP_TOP          
            226_0  COME_FROM           208  '208'

 L.1197       226  LOAD_FAST                'callback'
              228  LOAD_CONST               None
              230  <117>                 0  ''
              232  POP_JUMP_IF_FALSE   250  'to 250'

 L.1198       234  LOAD_GLOBAL              logger
              236  LOAD_METHOD              warning

 L.1199       238  LOAD_STR                 'Caught subprocess termination from unknown pid: %d -> %d'

 L.1200       240  LOAD_FAST                'pid'
              242  LOAD_FAST                'returncode'

 L.1198       244  CALL_METHOD_3         3  ''
              246  POP_TOP          
              248  JUMP_BACK             0  'to 0'
            250_0  COME_FROM           232  '232'

 L.1202       250  LOAD_FAST                'callback'
              252  LOAD_FAST                'pid'
              254  LOAD_FAST                'returncode'
              256  BUILD_LIST_2          2 
              258  LOAD_FAST                'args'
              260  CALL_FINALLY        263  'to 263'
              262  WITH_CLEANUP_FINISH
              264  CALL_FUNCTION_EX      0  'positional arguments only'
              266  POP_TOP          
              268  JUMP_BACK             0  'to 0'

Parse error at or near `<121>' instruction at offset 28


class MultiLoopChildWatcher(AbstractChildWatcher):
    __doc__ = "A watcher that doesn't require running loop in the main thread.\n\n    This implementation registers a SIGCHLD signal handler on\n    instantiation (which may conflict with other code that\n    install own handler for this signal).\n\n    The solution is safe but it has a significant overhead when\n    handling a big number of processes (*O(n)* each time a\n    SIGCHLD is received).\n    "

    def __init__(self):
        self._callbacks = {}
        self._saved_sighandler = None

    def is_active--- This code section failed: ---

 L.1229         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _saved_sighandler
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def close--- This code section failed: ---

 L.1232         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _callbacks
                4  LOAD_METHOD              clear
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L.1233        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _saved_sighandler
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    76  'to 76'

 L.1234        20  LOAD_GLOBAL              signal
               22  LOAD_METHOD              getsignal
               24  LOAD_GLOBAL              signal
               26  LOAD_ATTR                SIGCHLD
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'handler'

 L.1235        32  LOAD_FAST                'handler'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _sig_chld
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L.1236        42  LOAD_GLOBAL              logger
               44  LOAD_METHOD              warning
               46  LOAD_STR                 'SIGCHLD handler was changed by outside code'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  JUMP_FORWARD         70  'to 70'
             54_0  COME_FROM            40  '40'

 L.1238        54  LOAD_GLOBAL              signal
               56  LOAD_METHOD              signal
               58  LOAD_GLOBAL              signal
               60  LOAD_ATTR                SIGCHLD
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _saved_sighandler
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          
             70_0  COME_FROM            52  '52'

 L.1239        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _saved_sighandler
             76_0  COME_FROM            18  '18'

Parse error at or near `<117>' instruction at offset 16

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_child_handler(self, pid, callback, *args):
        loop = events.get_running_loop()
        self._callbacks[pid] = (loop, callback, args)
        self._do_waitpid(pid)

    def remove_child_handler--- This code section failed: ---

 L.1255         0  SETUP_FINALLY        16  'to 16'

 L.1256         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _callbacks
                6  LOAD_FAST                'pid'
                8  DELETE_SUBSCR    

 L.1257        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.1258        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  <121>                34  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1259        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
               34  <48>             

Parse error at or near `DUP_TOP' instruction at offset 16

    def attach_loop--- This code section failed: ---

 L.1266         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _saved_sighandler
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L.1267        10  LOAD_GLOBAL              signal
               12  LOAD_METHOD              signal
               14  LOAD_GLOBAL              signal
               16  LOAD_ATTR                SIGCHLD
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _sig_chld
               22  CALL_METHOD_2         2  ''
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _saved_sighandler

 L.1268        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _saved_sighandler
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    56  'to 56'

 L.1269        38  LOAD_GLOBAL              logger
               40  LOAD_METHOD              warning
               42  LOAD_STR                 'Previous SIGCHLD handler was set by non-Python code, restore to default handler on watcher close.'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L.1271        48  LOAD_GLOBAL              signal
               50  LOAD_ATTR                SIG_DFL
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _saved_sighandler
             56_0  COME_FROM            36  '36'

 L.1274        56  LOAD_GLOBAL              signal
               58  LOAD_METHOD              siginterrupt
               60  LOAD_GLOBAL              signal
               62  LOAD_ATTR                SIGCHLD
               64  LOAD_CONST               False
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          
             70_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def _do_waitpid_all(self):
        for pid in list(self._callbacks):
            self._do_waitpid(pid)

    def _do_waitpid--- This code section failed: ---

 L.1281         0  LOAD_FAST                'expected_pid'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L.1283        12  SETUP_FINALLY        36  'to 36'

 L.1284        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              waitpid
               18  LOAD_FAST                'expected_pid'
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                WNOHANG
               24  CALL_METHOD_2         2  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'pid'
               30  STORE_FAST               'status'
               32  POP_BLOCK        
               34  JUMP_FORWARD         78  'to 78'
             36_0  COME_FROM_FINALLY    12  '12'

 L.1285        36  DUP_TOP          
               38  LOAD_GLOBAL              ChildProcessError
               40  <121>                76  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1288        48  LOAD_FAST                'expected_pid'
               50  STORE_FAST               'pid'

 L.1289        52  LOAD_CONST               255
               54  STORE_FAST               'returncode'

 L.1290        56  LOAD_GLOBAL              logger
               58  LOAD_METHOD              warning

 L.1291        60  LOAD_STR                 'Unknown child process pid %d, will report returncode 255'

 L.1292        62  LOAD_FAST                'pid'

 L.1290        64  CALL_METHOD_2         2  ''
               66  POP_TOP          

 L.1293        68  LOAD_CONST               False
               70  STORE_FAST               'debug_log'
               72  POP_EXCEPT       
               74  JUMP_FORWARD        102  'to 102'
               76  <48>             
             78_0  COME_FROM            34  '34'

 L.1295        78  LOAD_FAST                'pid'
               80  LOAD_CONST               0
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L.1297        86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'

 L.1299        90  LOAD_GLOBAL              _compute_returncode
               92  LOAD_FAST                'status'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'returncode'

 L.1300        98  LOAD_CONST               True
              100  STORE_FAST               'debug_log'
            102_0  COME_FROM            74  '74'

 L.1301       102  SETUP_FINALLY       126  'to 126'

 L.1302       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _callbacks
              108  LOAD_METHOD              pop
              110  LOAD_FAST                'pid'
              112  CALL_METHOD_1         1  ''
              114  UNPACK_SEQUENCE_3     3 
              116  STORE_FAST               'loop'
              118  STORE_FAST               'callback'
              120  STORE_FAST               'args'
              122  POP_BLOCK        
              124  JUMP_FORWARD        160  'to 160'
            126_0  COME_FROM_FINALLY   102  '102'

 L.1303       126  DUP_TOP          
              128  LOAD_GLOBAL              KeyError
              130  <121>               158  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L.1306       138  LOAD_GLOBAL              logger
              140  LOAD_ATTR                warning
              142  LOAD_STR                 'Child watcher got an unexpected pid: %r'

 L.1307       144  LOAD_FAST                'pid'
              146  LOAD_CONST               True

 L.1306       148  LOAD_CONST               ('exc_info',)
              150  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              152  POP_TOP          
              154  POP_EXCEPT       
              156  JUMP_FORWARD        232  'to 232'
              158  <48>             
            160_0  COME_FROM           124  '124'

 L.1309       160  LOAD_FAST                'loop'
              162  LOAD_METHOD              is_closed
              164  CALL_METHOD_0         0  ''
              166  POP_JUMP_IF_FALSE   184  'to 184'

 L.1310       168  LOAD_GLOBAL              logger
              170  LOAD_METHOD              warning
              172  LOAD_STR                 'Loop %r that handles pid %r is closed'
              174  LOAD_FAST                'loop'
              176  LOAD_FAST                'pid'
              178  CALL_METHOD_3         3  ''
              180  POP_TOP          
              182  JUMP_FORWARD        232  'to 232'
            184_0  COME_FROM           166  '166'

 L.1312       184  LOAD_FAST                'debug_log'
              186  POP_JUMP_IF_FALSE   210  'to 210'
              188  LOAD_FAST                'loop'
              190  LOAD_METHOD              get_debug
              192  CALL_METHOD_0         0  ''
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L.1313       196  LOAD_GLOBAL              logger
              198  LOAD_METHOD              debug
              200  LOAD_STR                 'process %s exited with returncode %s'

 L.1314       202  LOAD_FAST                'expected_pid'
              204  LOAD_FAST                'returncode'

 L.1313       206  CALL_METHOD_3         3  ''
              208  POP_TOP          
            210_0  COME_FROM           194  '194'
            210_1  COME_FROM           186  '186'

 L.1315       210  LOAD_FAST                'loop'
              212  LOAD_ATTR                call_soon_threadsafe
              214  LOAD_FAST                'callback'
              216  LOAD_FAST                'pid'
              218  LOAD_FAST                'returncode'
              220  BUILD_LIST_3          3 
              222  LOAD_FAST                'args'
              224  CALL_FINALLY        227  'to 227'
              226  WITH_CLEANUP_FINISH
              228  CALL_FUNCTION_EX      0  'positional arguments only'
              230  POP_TOP          
            232_0  COME_FROM           182  '182'
            232_1  COME_FROM           156  '156'

Parse error at or near `None' instruction at offset -1

    def _sig_chld--- This code section failed: ---

 L.1318         0  SETUP_FINALLY        14  'to 14'

 L.1319         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _do_waitpid_all
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         68  'to 68'
             14_0  COME_FROM_FINALLY     0  '0'

 L.1320        14  DUP_TOP          
               16  LOAD_GLOBAL              SystemExit
               18  LOAD_GLOBAL              KeyboardInterrupt
               20  BUILD_TUPLE_2         2 
               22  <121>                36  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1321        30  RAISE_VARARGS_0       0  'reraise'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         68  'to 68'

 L.1322        36  DUP_TOP          
               38  LOAD_GLOBAL              BaseException
               40  <121>                66  ''
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1323        48  LOAD_GLOBAL              logger
               50  LOAD_ATTR                warning
               52  LOAD_STR                 'Unknown exception in SIGCHLD handler'
               54  LOAD_CONST               True
               56  LOAD_CONST               ('exc_info',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  POP_TOP          
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
               66  <48>             
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            34  '34'
             68_2  COME_FROM            12  '12'

Parse error at or near `<121>' instruction at offset 22


class ThreadedChildWatcher(AbstractChildWatcher):
    __doc__ = "Threaded child watcher implementation.\n\n    The watcher uses a thread per process\n    for waiting for the process finish.\n\n    It doesn't require subscription on POSIX signal\n    but a thread creation is not free.\n\n    The watcher has O(1) complexity, its performance doesn't depend\n    on amount of spawn processes.\n    "

    def __init__(self):
        self._pid_counter = itertools.count(0)
        self._threads = {}

    def is_active(self):
        return True

    def close(self):
        self._join_threads()

    def _join_threads(self):
        """Internal: Join all non-daemon threads"""
        threads = [thread for thread in list(self._threads.values()) if thread.is_alive() if not thread.daemon]
        for thread in threads:
            thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self, _warn=warnings.warn):
        threads = [thread for thread in list(self._threads.values()) if thread.is_alive()]
        if threads:
            _warn(f"{self.__class__} has registered but not finished child processes", ResourceWarning,
              source=self)

    def add_child_handler(self, pid, callback, *args):
        loop = events.get_running_loop()
        thread = threading.Thread(target=(self._do_waitpid), name=f"waitpid-{next(self._pid_counter)}",
          args=(
         loop, pid, callback, args),
          daemon=True)
        self._threads[pid] = thread
        thread.start()

    def remove_child_handler(self, pid):
        return True

    def attach_loop(self, loop):
        pass

    def _do_waitpid--- This code section failed: ---

 L.1389         0  LOAD_FAST                'expected_pid'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     12  'to 12'
                8  <74>             
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             6  '6'

 L.1391        12  SETUP_FINALLY        34  'to 34'

 L.1392        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              waitpid
               18  LOAD_FAST                'expected_pid'
               20  LOAD_CONST               0
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'pid'
               28  STORE_FAST               'status'
               30  POP_BLOCK        
               32  JUMP_FORWARD         72  'to 72'
             34_0  COME_FROM_FINALLY    12  '12'

 L.1393        34  DUP_TOP          
               36  LOAD_GLOBAL              ChildProcessError
               38  <121>                70  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.1396        46  LOAD_FAST                'expected_pid'
               48  STORE_FAST               'pid'

 L.1397        50  LOAD_CONST               255
               52  STORE_FAST               'returncode'

 L.1398        54  LOAD_GLOBAL              logger
               56  LOAD_METHOD              warning

 L.1399        58  LOAD_STR                 'Unknown child process pid %d, will report returncode 255'

 L.1400        60  LOAD_FAST                'pid'

 L.1398        62  CALL_METHOD_2         2  ''
               64  POP_TOP          
               66  POP_EXCEPT       
               68  JUMP_FORWARD        102  'to 102'
               70  <48>             
             72_0  COME_FROM            32  '32'

 L.1402        72  LOAD_GLOBAL              _compute_returncode
               74  LOAD_FAST                'status'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'returncode'

 L.1403        80  LOAD_FAST                'loop'
               82  LOAD_METHOD              get_debug
               84  CALL_METHOD_0         0  ''
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L.1404        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              debug
               92  LOAD_STR                 'process %s exited with returncode %s'

 L.1405        94  LOAD_FAST                'expected_pid'
               96  LOAD_FAST                'returncode'

 L.1404        98  CALL_METHOD_3         3  ''
              100  POP_TOP          
            102_0  COME_FROM            86  '86'
            102_1  COME_FROM            68  '68'

 L.1407       102  LOAD_FAST                'loop'
              104  LOAD_METHOD              is_closed
              106  CALL_METHOD_0         0  ''
              108  POP_JUMP_IF_FALSE   126  'to 126'

 L.1408       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              warning
              114  LOAD_STR                 'Loop %r that handles pid %r is closed'
              116  LOAD_FAST                'loop'
              118  LOAD_FAST                'pid'
              120  CALL_METHOD_3         3  ''
              122  POP_TOP          
              124  JUMP_FORWARD        148  'to 148'
            126_0  COME_FROM           108  '108'

 L.1410       126  LOAD_FAST                'loop'
              128  LOAD_ATTR                call_soon_threadsafe
              130  LOAD_FAST                'callback'
              132  LOAD_FAST                'pid'
              134  LOAD_FAST                'returncode'
              136  BUILD_LIST_3          3 
              138  LOAD_FAST                'args'
              140  CALL_FINALLY        143  'to 143'
              142  WITH_CLEANUP_FINISH
              144  CALL_FUNCTION_EX      0  'positional arguments only'
              146  POP_TOP          
            148_0  COME_FROM           124  '124'

 L.1412       148  LOAD_FAST                'self'
              150  LOAD_ATTR                _threads
              152  LOAD_METHOD              pop
              154  LOAD_FAST                'expected_pid'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

Parse error at or near `None' instruction at offset -1


class _UnixDefaultEventLoopPolicy(events.BaseDefaultEventLoopPolicy):
    __doc__ = 'UNIX event loop policy with a watcher for child processes.'
    _loop_factory = _UnixSelectorEventLoop

    def __init__(self):
        super().__init__()
        self._watcher = None

    def _init_watcher--- This code section failed: ---

 L.1424         0  LOAD_GLOBAL              events
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           72  'to 72'
                6  POP_TOP          

 L.1425         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _watcher
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    58  'to 58'

 L.1426        18  LOAD_GLOBAL              ThreadedChildWatcher
               20  CALL_FUNCTION_0       0  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _watcher

 L.1427        26  LOAD_GLOBAL              threading
               28  LOAD_METHOD              current_thread
               30  CALL_METHOD_0         0  ''
               32  LOAD_GLOBAL              threading
               34  LOAD_METHOD              main_thread
               36  CALL_METHOD_0         0  ''
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L.1428        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _watcher
               46  LOAD_METHOD              attach_loop
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _local
               52  LOAD_ATTR                _loop
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
             58_0  COME_FROM            40  '40'
             58_1  COME_FROM            16  '16'
               58  POP_BLOCK        
               60  LOAD_CONST               None
               62  DUP_TOP          
               64  DUP_TOP          
               66  CALL_FUNCTION_3       3  ''
               68  POP_TOP          
               70  JUMP_FORWARD         88  'to 88'
             72_0  COME_FROM_WITH        4  '4'
               72  <49>             
               74  POP_JUMP_IF_TRUE     78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          
               84  POP_EXCEPT       
               86  POP_TOP          
             88_0  COME_FROM            70  '70'

Parse error at or near `<117>' instruction at offset 14

    def set_event_loop--- This code section failed: ---

 L.1438         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              set_event_loop
                6  LOAD_FAST                'loop'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L.1440        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _watcher
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    50  'to 50'

 L.1441        22  LOAD_GLOBAL              threading
               24  LOAD_METHOD              current_thread
               26  CALL_METHOD_0         0  ''
               28  LOAD_GLOBAL              threading
               30  LOAD_METHOD              main_thread
               32  CALL_METHOD_0         0  ''
               34  <117>                 0  ''

 L.1440        36  POP_JUMP_IF_FALSE    50  'to 50'

 L.1442        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _watcher
               42  LOAD_METHOD              attach_loop
               44  LOAD_FAST                'loop'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
             50_0  COME_FROM            36  '36'
             50_1  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def get_child_watcher--- This code section failed: ---

 L.1449         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _watcher
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1450        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _init_watcher
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L.1452        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _watcher
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def set_child_watcher--- This code section failed: ---

 L.1457         0  LOAD_FAST                'watcher'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     22  'to 22'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'watcher'
               12  LOAD_GLOBAL              AbstractChildWatcher
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  <74>             
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'
             22_1  COME_FROM             6  '6'

 L.1459        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _watcher
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L.1460        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _watcher
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          
             42_0  COME_FROM            30  '30'

 L.1462        42  LOAD_FAST                'watcher'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _watcher

Parse error at or near `None' instruction at offset -1


SelectorEventLoop = _UnixSelectorEventLoop
DefaultEventLoopPolicy = _UnixDefaultEventLoopPolicy