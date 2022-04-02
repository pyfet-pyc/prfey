# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\subprocess.py
__all__ = ('create_subprocess_exec', 'create_subprocess_shell')
import subprocess, warnings
from . import events
from . import protocols
from . import streams
from . import tasks
from .log import logger
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
DEVNULL = subprocess.DEVNULL

class SubprocessStreamProtocol(streams.FlowControlMixin, protocols.SubprocessProtocol):
    __doc__ = 'Like StreamReaderProtocol, but for a subprocess.'

    def __init__(self, limit, loop):
        super().__init__(loop=loop)
        self._limit = limit
        self.stdin = self.stdout = self.stderr = None
        self._transport = None
        self._process_exited = False
        self._pipe_fds = []
        self._stdin_closed = self._loop.create_future()

    def __repr__--- This code section failed: ---

 L.  32         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'info'

 L.  33        10  LOAD_FAST                'self'
               12  LOAD_ATTR                stdin
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L.  34        20  LOAD_FAST                'info'
               22  LOAD_METHOD              append
               24  LOAD_STR                 'stdin='
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                stdin
               30  FORMAT_VALUE          2  '!r'
               32  BUILD_STRING_2        2 
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
             38_0  COME_FROM            18  '18'

 L.  35        38  LOAD_FAST                'self'
               40  LOAD_ATTR                stdout
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    66  'to 66'

 L.  36        48  LOAD_FAST                'info'
               50  LOAD_METHOD              append
               52  LOAD_STR                 'stdout='
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                stdout
               58  FORMAT_VALUE          2  '!r'
               60  BUILD_STRING_2        2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            46  '46'

 L.  37        66  LOAD_FAST                'self'
               68  LOAD_ATTR                stderr
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    94  'to 94'

 L.  38        76  LOAD_FAST                'info'
               78  LOAD_METHOD              append
               80  LOAD_STR                 'stderr='
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                stderr
               86  FORMAT_VALUE          2  '!r'
               88  BUILD_STRING_2        2 
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
             94_0  COME_FROM            74  '74'

 L.  39        94  LOAD_STR                 '<{}>'
               96  LOAD_METHOD              format
               98  LOAD_STR                 ' '
              100  LOAD_METHOD              join
              102  LOAD_FAST                'info'
              104  CALL_METHOD_1         1  ''
              106  CALL_METHOD_1         1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def connection_made--- This code section failed: ---

 L.  42         0  LOAD_FAST                'transport'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _transport

 L.  44         6  LOAD_FAST                'transport'
                8  LOAD_METHOD              get_pipe_transport
               10  LOAD_CONST               1
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'stdout_transport'

 L.  45        16  LOAD_FAST                'stdout_transport'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    68  'to 68'

 L.  46        24  LOAD_GLOBAL              streams
               26  LOAD_ATTR                StreamReader
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _limit

 L.  47        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _loop

 L.  46        36  LOAD_CONST               ('limit', 'loop')
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               stdout

 L.  48        44  LOAD_FAST                'self'
               46  LOAD_ATTR                stdout
               48  LOAD_METHOD              set_transport
               50  LOAD_FAST                'stdout_transport'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L.  49        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _pipe_fds
               60  LOAD_METHOD              append
               62  LOAD_CONST               1
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
             68_0  COME_FROM            22  '22'

 L.  51        68  LOAD_FAST                'transport'
               70  LOAD_METHOD              get_pipe_transport
               72  LOAD_CONST               2
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'stderr_transport'

 L.  52        78  LOAD_FAST                'stderr_transport'
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   130  'to 130'

 L.  53        86  LOAD_GLOBAL              streams
               88  LOAD_ATTR                StreamReader
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _limit

 L.  54        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _loop

 L.  53        98  LOAD_CONST               ('limit', 'loop')
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               stderr

 L.  55       106  LOAD_FAST                'self'
              108  LOAD_ATTR                stderr
              110  LOAD_METHOD              set_transport
              112  LOAD_FAST                'stderr_transport'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L.  56       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _pipe_fds
              122  LOAD_METHOD              append
              124  LOAD_CONST               2
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM            84  '84'

 L.  58       130  LOAD_FAST                'transport'
              132  LOAD_METHOD              get_pipe_transport
              134  LOAD_CONST               0
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'stdin_transport'

 L.  59       140  LOAD_FAST                'stdin_transport'
              142  LOAD_CONST               None
              144  <117>                 1  ''
              146  POP_JUMP_IF_FALSE   170  'to 170'

 L.  60       148  LOAD_GLOBAL              streams
              150  LOAD_ATTR                StreamWriter
              152  LOAD_FAST                'stdin_transport'

 L.  61       154  LOAD_FAST                'self'

 L.  62       156  LOAD_CONST               None

 L.  63       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _loop

 L.  60       162  LOAD_CONST               ('protocol', 'reader', 'loop')
              164  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               stdin
            170_0  COME_FROM           146  '146'

Parse error at or near `<117>' instruction at offset 20

    def pipe_data_received--- This code section failed: ---

 L.  66         0  LOAD_FAST                'fd'
                2  LOAD_CONST               1
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  67         8  LOAD_FAST                'self'
               10  LOAD_ATTR                stdout
               12  STORE_FAST               'reader'
               14  JUMP_FORWARD         36  'to 36'
             16_0  COME_FROM             6  '6'

 L.  68        16  LOAD_FAST                'fd'
               18  LOAD_CONST               2
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.  69        24  LOAD_FAST                'self'
               26  LOAD_ATTR                stderr
               28  STORE_FAST               'reader'
               30  JUMP_FORWARD         36  'to 36'
             32_0  COME_FROM            22  '22'

 L.  71        32  LOAD_CONST               None
               34  STORE_FAST               'reader'
             36_0  COME_FROM            30  '30'
             36_1  COME_FROM            14  '14'

 L.  72        36  LOAD_FAST                'reader'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L.  73        44  LOAD_FAST                'reader'
               46  LOAD_METHOD              feed_data
               48  LOAD_FAST                'data'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            42  '42'

Parse error at or near `<117>' instruction at offset 40

    def pipe_connection_lost--- This code section failed: ---

 L.  76         0  LOAD_FAST                'fd'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    78  'to 78'

 L.  77         8  LOAD_FAST                'self'
               10  LOAD_ATTR                stdin
               12  STORE_FAST               'pipe'

 L.  78        14  LOAD_FAST                'pipe'
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.  79        22  LOAD_FAST                'pipe'
               24  LOAD_METHOD              close
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
             30_0  COME_FROM            20  '20'

 L.  80        30  LOAD_FAST                'self'
               32  LOAD_METHOD              connection_lost
               34  LOAD_FAST                'exc'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L.  81        40  LOAD_FAST                'exc'
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    62  'to 62'

 L.  82        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _stdin_closed
               52  LOAD_METHOD              set_result
               54  LOAD_CONST               None
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  JUMP_FORWARD         74  'to 74'
             62_0  COME_FROM            46  '46'

 L.  84        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _stdin_closed
               66  LOAD_METHOD              set_exception
               68  LOAD_FAST                'exc'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            60  '60'

 L.  85        74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM             6  '6'

 L.  86        78  LOAD_FAST                'fd'
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L.  87        86  LOAD_FAST                'self'
               88  LOAD_ATTR                stdout
               90  STORE_FAST               'reader'
               92  JUMP_FORWARD        114  'to 114'
             94_0  COME_FROM            84  '84'

 L.  88        94  LOAD_FAST                'fd'
               96  LOAD_CONST               2
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L.  89       102  LOAD_FAST                'self'
              104  LOAD_ATTR                stderr
              106  STORE_FAST               'reader'
              108  JUMP_FORWARD        114  'to 114'
            110_0  COME_FROM           100  '100'

 L.  91       110  LOAD_CONST               None
              112  STORE_FAST               'reader'
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM            92  '92'

 L.  92       114  LOAD_FAST                'reader'
              116  LOAD_CONST               None
              118  <117>                 1  ''
              120  POP_JUMP_IF_FALSE   150  'to 150'

 L.  93       122  LOAD_FAST                'exc'
              124  LOAD_CONST               None
              126  <117>                 0  ''
              128  POP_JUMP_IF_FALSE   140  'to 140'

 L.  94       130  LOAD_FAST                'reader'
              132  LOAD_METHOD              feed_eof
              134  CALL_METHOD_0         0  ''
              136  POP_TOP          
              138  JUMP_FORWARD        150  'to 150'
            140_0  COME_FROM           128  '128'

 L.  96       140  LOAD_FAST                'reader'
              142  LOAD_METHOD              set_exception
              144  LOAD_FAST                'exc'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
            150_0  COME_FROM           138  '138'
            150_1  COME_FROM           120  '120'

 L.  98       150  LOAD_FAST                'fd'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _pipe_fds
              156  <118>                 0  ''
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.  99       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _pipe_fds
              164  LOAD_METHOD              remove
              166  LOAD_FAST                'fd'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           158  '158'

 L. 100       172  LOAD_FAST                'self'
              174  LOAD_METHOD              _maybe_close_transport
              176  CALL_METHOD_0         0  ''
              178  POP_TOP          

Parse error at or near `<117>' instruction at offset 18

    def process_exited(self):
        self._process_exited = True
        self._maybe_close_transport()

    def _maybe_close_transport(self):
        if len(self._pipe_fds) == 0:
            if self._process_exited:
                self._transport.close()
                self._transport = None

    def _get_close_waiter--- This code section failed: ---

 L. 112         0  LOAD_FAST                'stream'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                stdin
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 113        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _stdin_closed
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


class Process:

    def __init__(self, transport, protocol, loop):
        self._transport = transport
        self._protocol = protocol
        self._loop = loop
        self.stdin = protocol.stdin
        self.stdout = protocol.stdout
        self.stderr = protocol.stderr
        self.pid = transport.get_pid()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pid}>"

    @property
    def returncode(self):
        return self._transport.get_returncode()

    async def wait(self):
        """Wait until the process exit and return the process return code."""
        return await self._transport._wait()

    def send_signal(self, signal):
        self._transport.send_signalsignal

    def terminate(self):
        self._transport.terminate()

    def kill(self):
        self._transport.kill()

    async def _feed_stdin--- This code section failed: ---

 L. 147         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _loop
                4  LOAD_METHOD              get_debug
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'debug'

 L. 148        10  LOAD_FAST                'self'
               12  LOAD_ATTR                stdin
               14  LOAD_METHOD              write
               16  LOAD_FAST                'input'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 149        22  LOAD_FAST                'debug'
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 150        26  LOAD_GLOBAL              logger
               28  LOAD_METHOD              debug

 L. 151        30  LOAD_STR                 '%r communicate: feed stdin (%s bytes)'
               32  LOAD_FAST                'self'
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'input'
               38  CALL_FUNCTION_1       1  ''

 L. 150        40  CALL_METHOD_3         3  ''
               42  POP_TOP          
             44_0  COME_FROM            24  '24'

 L. 152        44  SETUP_FINALLY        66  'to 66'

 L. 153        46  LOAD_FAST                'self'
               48  LOAD_ATTR                stdin
               50  LOAD_METHOD              drain
               52  CALL_METHOD_0         0  ''
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  POP_TOP          
               62  POP_BLOCK        
               64  JUMP_FORWARD        124  'to 124'
             66_0  COME_FROM_FINALLY    44  '44'

 L. 154        66  DUP_TOP          
               68  LOAD_GLOBAL              BrokenPipeError
               70  LOAD_GLOBAL              ConnectionResetError
               72  BUILD_TUPLE_2         2 
               74  <121>               122  ''
               76  POP_TOP          
               78  STORE_FAST               'exc'
               80  POP_TOP          
               82  SETUP_FINALLY       114  'to 114'

 L. 156        84  LOAD_FAST                'debug'
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L. 157        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              debug
               92  LOAD_STR                 '%r communicate: stdin got %r'
               94  LOAD_FAST                'self'
               96  LOAD_FAST                'exc'
               98  CALL_METHOD_3         3  ''
              100  POP_TOP          
            102_0  COME_FROM            86  '86'
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  STORE_FAST               'exc'
              110  DELETE_FAST              'exc'
              112  JUMP_FORWARD        124  'to 124'
            114_0  COME_FROM_FINALLY    82  '82'
              114  LOAD_CONST               None
              116  STORE_FAST               'exc'
              118  DELETE_FAST              'exc'
              120  <48>             
              122  <48>             
            124_0  COME_FROM           112  '112'
            124_1  COME_FROM            64  '64'

 L. 159       124  LOAD_FAST                'debug'
              126  POP_JUMP_IF_FALSE   140  'to 140'

 L. 160       128  LOAD_GLOBAL              logger
              130  LOAD_METHOD              debug
              132  LOAD_STR                 '%r communicate: close stdin'
              134  LOAD_FAST                'self'
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          
            140_0  COME_FROM           126  '126'

 L. 161       140  LOAD_FAST                'self'
              142  LOAD_ATTR                stdin
              144  LOAD_METHOD              close
              146  CALL_METHOD_0         0  ''
              148  POP_TOP          

Parse error at or near `<121>' instruction at offset 74

    async def _noop(self):
        pass

    async def _read_stream--- This code section failed: ---

 L. 167         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _transport
                4  LOAD_METHOD              get_pipe_transport
                6  LOAD_FAST                'fd'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'transport'

 L. 168        12  LOAD_FAST                'fd'
               14  LOAD_CONST               2
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 169        20  LOAD_FAST                'self'
               22  LOAD_ATTR                stderr
               24  STORE_FAST               'stream'
               26  JUMP_FORWARD         46  'to 46'
             28_0  COME_FROM            18  '18'

 L. 171        28  LOAD_FAST                'fd'
               30  LOAD_CONST               1
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  <74>             
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 172        40  LOAD_FAST                'self'
               42  LOAD_ATTR                stdout
               44  STORE_FAST               'stream'
             46_0  COME_FROM            26  '26'

 L. 173        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _loop
               50  LOAD_METHOD              get_debug
               52  CALL_METHOD_0         0  ''
               54  POP_JUMP_IF_FALSE    86  'to 86'

 L. 174        56  LOAD_FAST                'fd'
               58  LOAD_CONST               1
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    68  'to 68'
               64  LOAD_STR                 'stdout'
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            62  '62'
               68  LOAD_STR                 'stderr'
             70_0  COME_FROM            66  '66'
               70  STORE_FAST               'name'

 L. 175        72  LOAD_GLOBAL              logger
               74  LOAD_METHOD              debug
               76  LOAD_STR                 '%r communicate: read %s'
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'name'
               82  CALL_METHOD_3         3  ''
               84  POP_TOP          
             86_0  COME_FROM            54  '54'

 L. 176        86  LOAD_FAST                'stream'
               88  LOAD_METHOD              read
               90  CALL_METHOD_0         0  ''
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  STORE_FAST               'output'

 L. 177       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _loop
              104  LOAD_METHOD              get_debug
              106  CALL_METHOD_0         0  ''
              108  POP_JUMP_IF_FALSE   140  'to 140'

 L. 178       110  LOAD_FAST                'fd'
              112  LOAD_CONST               1
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   122  'to 122'
              118  LOAD_STR                 'stdout'
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           116  '116'
              122  LOAD_STR                 'stderr'
            124_0  COME_FROM           120  '120'
              124  STORE_FAST               'name'

 L. 179       126  LOAD_GLOBAL              logger
              128  LOAD_METHOD              debug
              130  LOAD_STR                 '%r communicate: close %s'
              132  LOAD_FAST                'self'
              134  LOAD_FAST                'name'
              136  CALL_METHOD_3         3  ''
              138  POP_TOP          
            140_0  COME_FROM           108  '108'

 L. 180       140  LOAD_FAST                'transport'
              142  LOAD_METHOD              close
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          

 L. 181       148  LOAD_FAST                'output'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 36

    async def communicate--- This code section failed: ---

 L. 184         0  LOAD_FAST                'input'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 185         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _feed_stdin
               12  LOAD_FAST                'input'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'stdin'
               18  JUMP_FORWARD         28  'to 28'
             20_0  COME_FROM             6  '6'

 L. 187        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _noop
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'stdin'
             28_0  COME_FROM            18  '18'

 L. 188        28  LOAD_FAST                'self'
               30  LOAD_ATTR                stdout
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    50  'to 50'

 L. 189        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _read_stream
               42  LOAD_CONST               1
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'stdout'
               48  JUMP_FORWARD         58  'to 58'
             50_0  COME_FROM            36  '36'

 L. 191        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _noop
               54  CALL_METHOD_0         0  ''
               56  STORE_FAST               'stdout'
             58_0  COME_FROM            48  '48'

 L. 192        58  LOAD_FAST                'self'
               60  LOAD_ATTR                stderr
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 193        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _read_stream
               72  LOAD_CONST               2
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'stderr'
               78  JUMP_FORWARD         88  'to 88'
             80_0  COME_FROM            66  '66'

 L. 195        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _noop
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'stderr'
             88_0  COME_FROM            78  '78'

 L. 196        88  LOAD_GLOBAL              tasks
               90  LOAD_ATTR                gather
               92  LOAD_FAST                'stdin'
               94  LOAD_FAST                'stdout'
               96  LOAD_FAST                'stderr'

 L. 197        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _loop

 L. 196       102  LOAD_CONST               ('loop',)
              104  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              106  GET_AWAITABLE    
              108  LOAD_CONST               None
              110  YIELD_FROM       
              112  UNPACK_SEQUENCE_3     3 
              114  STORE_FAST               'stdin'
              116  STORE_FAST               'stdout'
              118  STORE_FAST               'stderr'

 L. 198       120  LOAD_FAST                'self'
              122  LOAD_METHOD              wait
              124  CALL_METHOD_0         0  ''
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  POP_TOP          

 L. 199       134  LOAD_FAST                'stdout'
              136  LOAD_FAST                'stderr'
              138  BUILD_TUPLE_2         2 
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


async def create_subprocess_shell--- This code section failed: ---

 L. 205         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 206         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L. 208        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8 and scheduled for removal in Python 3.10.'

 L. 210        24  LOAD_GLOBAL              DeprecationWarning

 L. 211        26  LOAD_CONST               2

 L. 208        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L. 214        34  LOAD_CLOSURE             'limit'
               36  LOAD_CLOSURE             'loop'
               38  BUILD_TUPLE_2         2 
               40  LOAD_LAMBDA              '<code_object <lambda>>'
               42  LOAD_STR                 'create_subprocess_shell.<locals>.<lambda>'
               44  MAKE_FUNCTION_8          'closure'
               46  STORE_FAST               'protocol_factory'

 L. 216        48  LOAD_DEREF               'loop'
               50  LOAD_ATTR                subprocess_shell

 L. 217        52  LOAD_FAST                'protocol_factory'

 L. 218        54  LOAD_FAST                'cmd'

 L. 216        56  BUILD_TUPLE_2         2 

 L. 218        58  LOAD_FAST                'stdin'
               60  LOAD_FAST                'stdout'

 L. 219        62  LOAD_FAST                'stderr'

 L. 216        64  LOAD_CONST               ('stdin', 'stdout', 'stderr')
               66  BUILD_CONST_KEY_MAP_3     3 

 L. 219        68  LOAD_FAST                'kwds'

 L. 216        70  <164>                 1  ''
               72  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               74  GET_AWAITABLE    
               76  LOAD_CONST               None
               78  YIELD_FROM       
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'transport'
               84  STORE_FAST               'protocol'

 L. 220        86  LOAD_GLOBAL              Process
               88  LOAD_FAST                'transport'
               90  LOAD_FAST                'protocol'
               92  LOAD_DEREF               'loop'
               94  CALL_FUNCTION_3       3  ''
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


async def create_subprocess_exec--- This code section failed: ---

 L. 226         0  LOAD_DEREF               'loop'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 227         8  LOAD_GLOBAL              events
               10  LOAD_METHOD              get_event_loop
               12  CALL_METHOD_0         0  ''
               14  STORE_DEREF              'loop'
               16  JUMP_FORWARD         34  'to 34'
             18_0  COME_FROM             6  '6'

 L. 229        18  LOAD_GLOBAL              warnings
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'The loop argument is deprecated since Python 3.8 and scheduled for removal in Python 3.10.'

 L. 231        24  LOAD_GLOBAL              DeprecationWarning

 L. 232        26  LOAD_CONST               2

 L. 229        28  LOAD_CONST               ('stacklevel',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_TOP          
             34_0  COME_FROM            16  '16'

 L. 234        34  LOAD_CLOSURE             'limit'
               36  LOAD_CLOSURE             'loop'
               38  BUILD_TUPLE_2         2 
               40  LOAD_LAMBDA              '<code_object <lambda>>'
               42  LOAD_STR                 'create_subprocess_exec.<locals>.<lambda>'
               44  MAKE_FUNCTION_8          'closure'
               46  STORE_FAST               'protocol_factory'

 L. 236        48  LOAD_DEREF               'loop'
               50  LOAD_ATTR                subprocess_exec

 L. 237        52  LOAD_FAST                'protocol_factory'

 L. 238        54  LOAD_FAST                'program'

 L. 236        56  BUILD_LIST_2          2 

 L. 238        58  LOAD_FAST                'args'

 L. 236        60  CALL_FINALLY         63  'to 63'
               62  WITH_CLEANUP_FINISH

 L. 239        64  LOAD_FAST                'stdin'
               66  LOAD_FAST                'stdout'

 L. 240        68  LOAD_FAST                'stderr'

 L. 236        70  LOAD_CONST               ('stdin', 'stdout', 'stderr')
               72  BUILD_CONST_KEY_MAP_3     3 

 L. 240        74  LOAD_FAST                'kwds'

 L. 236        76  <164>                 1  ''
               78  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'transport'
               90  STORE_FAST               'protocol'

 L. 241        92  LOAD_GLOBAL              Process
               94  LOAD_FAST                'transport'
               96  LOAD_FAST                'protocol'
               98  LOAD_DEREF               'loop'
              100  CALL_FUNCTION_3       3  ''
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1