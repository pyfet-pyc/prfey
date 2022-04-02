# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\base_subprocess.py
import collections, subprocess, warnings
from . import protocols
from . import transports
from .log import logger

class BaseSubprocessTransport(transports.SubprocessTransport):

    def __init__--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L.  16        12  LOAD_CONST               False
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _closed

 L.  17        18  LOAD_FAST                'protocol'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _protocol

 L.  18        24  LOAD_FAST                'loop'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _loop

 L.  19        30  LOAD_CONST               None
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _proc

 L.  20        36  LOAD_CONST               None
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _pid

 L.  21        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _returncode

 L.  22        48  BUILD_LIST_0          0 
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _exit_waiters

 L.  23        54  LOAD_GLOBAL              collections
               56  LOAD_METHOD              deque
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _pending_calls

 L.  24        64  BUILD_MAP_0           0 
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _pipes

 L.  25        70  LOAD_CONST               False
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _finished

 L.  27        76  LOAD_FAST                'stdin'
               78  LOAD_GLOBAL              subprocess
               80  LOAD_ATTR                PIPE
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L.  28        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _pipes
               92  LOAD_CONST               0
               94  STORE_SUBSCR     
             96_0  COME_FROM            84  '84'

 L.  29        96  LOAD_FAST                'stdout'
               98  LOAD_GLOBAL              subprocess
              100  LOAD_ATTR                PIPE
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L.  30       106  LOAD_CONST               None
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                _pipes
              112  LOAD_CONST               1
              114  STORE_SUBSCR     
            116_0  COME_FROM           104  '104'

 L.  31       116  LOAD_FAST                'stderr'
              118  LOAD_GLOBAL              subprocess
              120  LOAD_ATTR                PIPE
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   136  'to 136'

 L.  32       126  LOAD_CONST               None
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _pipes
              132  LOAD_CONST               2
              134  STORE_SUBSCR     
            136_0  COME_FROM           124  '124'

 L.  35       136  SETUP_FINALLY       172  'to 172'

 L.  36       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _start
              142  BUILD_TUPLE_0         0 
              144  LOAD_FAST                'args'
              146  LOAD_FAST                'shell'
              148  LOAD_FAST                'stdin'
              150  LOAD_FAST                'stdout'

 L.  37       152  LOAD_FAST                'stderr'
              154  LOAD_FAST                'bufsize'

 L.  36       156  LOAD_CONST               ('args', 'shell', 'stdin', 'stdout', 'stderr', 'bufsize')
              158  BUILD_CONST_KEY_MAP_6     6 

 L.  37       160  LOAD_FAST                'kwargs'

 L.  36       162  <164>                 1  ''
              164  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              166  POP_TOP          
              168  POP_BLOCK        
              170  JUMP_FORWARD        194  'to 194'
            172_0  COME_FROM_FINALLY   136  '136'

 L.  38       172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L.  39       178  LOAD_FAST                'self'
              180  LOAD_METHOD              close
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          

 L.  40       186  RAISE_VARARGS_0       0  'reraise'
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
              192  <48>             
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           170  '170'

 L.  42       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _proc
              198  LOAD_ATTR                pid
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _pid

 L.  43       204  LOAD_FAST                'self'
              206  LOAD_ATTR                _proc
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                _extra
              212  LOAD_STR                 'subprocess'
              214  STORE_SUBSCR     

 L.  45       216  LOAD_FAST                'self'
              218  LOAD_ATTR                _loop
              220  LOAD_METHOD              get_debug
              222  CALL_METHOD_0         0  ''
          224_226  POP_JUMP_IF_FALSE   272  'to 272'

 L.  46       228  LOAD_GLOBAL              isinstance
              230  LOAD_FAST                'args'
              232  LOAD_GLOBAL              bytes
              234  LOAD_GLOBAL              str
              236  BUILD_TUPLE_2         2 
              238  CALL_FUNCTION_2       2  ''
              240  POP_JUMP_IF_FALSE   248  'to 248'

 L.  47       242  LOAD_FAST                'args'
              244  STORE_FAST               'program'
              246  JUMP_FORWARD        256  'to 256'
            248_0  COME_FROM           240  '240'

 L.  49       248  LOAD_FAST                'args'
              250  LOAD_CONST               0
              252  BINARY_SUBSCR    
              254  STORE_FAST               'program'
            256_0  COME_FROM           246  '246'

 L.  50       256  LOAD_GLOBAL              logger
              258  LOAD_METHOD              debug
              260  LOAD_STR                 'process %r created: pid %s'

 L.  51       262  LOAD_FAST                'program'
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                _pid

 L.  50       268  CALL_METHOD_3         3  ''
              270  POP_TOP          
            272_0  COME_FROM           224  '224'

 L.  53       272  LOAD_FAST                'self'
              274  LOAD_ATTR                _loop
              276  LOAD_METHOD              create_task
              278  LOAD_FAST                'self'
              280  LOAD_METHOD              _connect_pipes
              282  LOAD_FAST                'waiter'
              284  CALL_METHOD_1         1  ''
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

Parse error at or near `<164>' instruction at offset 162

    def __repr__--- This code section failed: ---

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                __name__
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'info'

 L.  57        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _closed
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L.  58        16  LOAD_FAST                'info'
               18  LOAD_METHOD              append
               20  LOAD_STR                 'closed'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L.  59        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _pid
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    54  'to 54'

 L.  60        36  LOAD_FAST                'info'
               38  LOAD_METHOD              append
               40  LOAD_STR                 'pid='
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _pid
               46  FORMAT_VALUE          0  ''
               48  BUILD_STRING_2        2 
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
             54_0  COME_FROM            34  '34'

 L.  61        54  LOAD_FAST                'self'
               56  LOAD_ATTR                _returncode
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    84  'to 84'

 L.  62        64  LOAD_FAST                'info'
               66  LOAD_METHOD              append
               68  LOAD_STR                 'returncode='
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _returncode
               74  FORMAT_VALUE          0  ''
               76  BUILD_STRING_2        2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD        116  'to 116'
             84_0  COME_FROM            62  '62'

 L.  63        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _pid
               88  LOAD_CONST               None
               90  <117>                 1  ''
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L.  64        94  LOAD_FAST                'info'
               96  LOAD_METHOD              append
               98  LOAD_STR                 'running'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_FORWARD        116  'to 116'
            106_0  COME_FROM            92  '92'

 L.  66       106  LOAD_FAST                'info'
              108  LOAD_METHOD              append
              110  LOAD_STR                 'not started'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM           104  '104'
            116_1  COME_FROM            82  '82'

 L.  68       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _pipes
              120  LOAD_METHOD              get
              122  LOAD_CONST               0
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'stdin'

 L.  69       128  LOAD_FAST                'stdin'
              130  LOAD_CONST               None
              132  <117>                 1  ''
              134  POP_JUMP_IF_FALSE   154  'to 154'

 L.  70       136  LOAD_FAST                'info'
              138  LOAD_METHOD              append
              140  LOAD_STR                 'stdin='
              142  LOAD_FAST                'stdin'
              144  LOAD_ATTR                pipe
              146  FORMAT_VALUE          0  ''
              148  BUILD_STRING_2        2 
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
            154_0  COME_FROM           134  '134'

 L.  72       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _pipes
              158  LOAD_METHOD              get
              160  LOAD_CONST               1
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'stdout'

 L.  73       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _pipes
              170  LOAD_METHOD              get
              172  LOAD_CONST               2
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'stderr'

 L.  74       178  LOAD_FAST                'stdout'
              180  LOAD_CONST               None
              182  <117>                 1  ''
              184  POP_JUMP_IF_FALSE   214  'to 214'
              186  LOAD_FAST                'stderr'
              188  LOAD_FAST                'stdout'
              190  <117>                 0  ''
              192  POP_JUMP_IF_FALSE   214  'to 214'

 L.  75       194  LOAD_FAST                'info'
              196  LOAD_METHOD              append
              198  LOAD_STR                 'stdout=stderr='
              200  LOAD_FAST                'stdout'
              202  LOAD_ATTR                pipe
              204  FORMAT_VALUE          0  ''
              206  BUILD_STRING_2        2 
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  JUMP_FORWARD        268  'to 268'
            214_0  COME_FROM           192  '192'
            214_1  COME_FROM           184  '184'

 L.  77       214  LOAD_FAST                'stdout'
              216  LOAD_CONST               None
              218  <117>                 1  ''
              220  POP_JUMP_IF_FALSE   240  'to 240'

 L.  78       222  LOAD_FAST                'info'
              224  LOAD_METHOD              append
              226  LOAD_STR                 'stdout='
              228  LOAD_FAST                'stdout'
              230  LOAD_ATTR                pipe
              232  FORMAT_VALUE          0  ''
              234  BUILD_STRING_2        2 
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
            240_0  COME_FROM           220  '220'

 L.  79       240  LOAD_FAST                'stderr'
              242  LOAD_CONST               None
              244  <117>                 1  ''
          246_248  POP_JUMP_IF_FALSE   268  'to 268'

 L.  80       250  LOAD_FAST                'info'
              252  LOAD_METHOD              append
              254  LOAD_STR                 'stderr='
              256  LOAD_FAST                'stderr'
              258  LOAD_ATTR                pipe
              260  FORMAT_VALUE          0  ''
              262  BUILD_STRING_2        2 
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
            268_0  COME_FROM           246  '246'
            268_1  COME_FROM           212  '212'

 L.  82       268  LOAD_STR                 '<{}>'
              270  LOAD_METHOD              format
              272  LOAD_STR                 ' '
              274  LOAD_METHOD              join
              276  LOAD_FAST                'info'
              278  CALL_METHOD_1         1  ''
              280  CALL_METHOD_1         1  ''
              282  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):
        raise NotImplementedError

    def set_protocol(self, protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_closing(self):
        return self._closed

    def close--- This code section failed: ---

 L.  97         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _closed
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  98         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  99        10  LOAD_CONST               True
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _closed

 L. 101        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _pipes
               20  LOAD_METHOD              values
               22  CALL_METHOD_0         0  ''
               24  GET_ITER         
               26  FOR_ITER             52  'to 52'
               28  STORE_FAST               'proto'

 L. 102        30  LOAD_FAST                'proto'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    40  'to 40'

 L. 103        38  JUMP_BACK            26  'to 26'
             40_0  COME_FROM            36  '36'

 L. 104        40  LOAD_FAST                'proto'
               42  LOAD_ATTR                pipe
               44  LOAD_METHOD              close
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
               50  JUMP_BACK            26  'to 26'

 L. 106        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _proc
               56  LOAD_CONST               None
               58  <117>                 1  ''
               60  POP_JUMP_IF_FALSE   142  'to 142'

 L. 108        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _returncode
               66  LOAD_CONST               None
               68  <117>                 0  ''

 L. 106        70  POP_JUMP_IF_FALSE   142  'to 142'

 L. 111        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _proc
               76  LOAD_METHOD              poll
               78  CALL_METHOD_0         0  ''
               80  LOAD_CONST               None
               82  <117>                 0  ''

 L. 106        84  POP_JUMP_IF_FALSE   142  'to 142'

 L. 113        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _loop
               90  LOAD_METHOD              get_debug
               92  CALL_METHOD_0         0  ''
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 114        96  LOAD_GLOBAL              logger
               98  LOAD_METHOD              warning
              100  LOAD_STR                 'Close running child process: kill %r'
              102  LOAD_FAST                'self'
              104  CALL_METHOD_2         2  ''
              106  POP_TOP          
            108_0  COME_FROM            94  '94'

 L. 116       108  SETUP_FINALLY       124  'to 124'

 L. 117       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _proc
              114  LOAD_METHOD              kill
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        142  'to 142'
            124_0  COME_FROM_FINALLY   108  '108'

 L. 118       124  DUP_TOP          
              126  LOAD_GLOBAL              ProcessLookupError
              128  <121>               140  ''
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 119       136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           122  '122'
            142_2  COME_FROM            84  '84'
            142_3  COME_FROM            70  '70'
            142_4  COME_FROM            60  '60'

Parse error at or near `<117>' instruction at offset 34

    def __del__(self, _warn=warnings.warn):
        if not self._closed:
            _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
            self.close

    def get_pid(self):
        return self._pid

    def get_returncode(self):
        return self._returncode

    def get_pipe_transport--- This code section failed: ---

 L. 135         0  LOAD_FAST                'fd'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _pipes
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 136        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pipes
               14  LOAD_FAST                'fd'
               16  BINARY_SUBSCR    
               18  LOAD_ATTR                pipe
               20  RETURN_VALUE     
             22_0  COME_FROM             8  '8'

 L. 138        22  LOAD_CONST               None
               24  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def _check_proc--- This code section failed: ---

 L. 141         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _proc
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 142        10  LOAD_GLOBAL              ProcessLookupError
               12  CALL_FUNCTION_0       0  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def send_signal(self, signal):
        self._check_proc
        self._proc.send_signalsignal

    def terminate(self):
        self._check_proc
        self._proc.terminate

    def kill(self):
        self._check_proc
        self._proc.kill

    async def _connect_pipes--- This code section failed: ---

 L. 157         0  SETUP_FINALLY       244  'to 244'

 L. 158         2  LOAD_DEREF               'self'
                4  LOAD_ATTR                _proc
                6  STORE_FAST               'proc'

 L. 159         8  LOAD_DEREF               'self'
               10  LOAD_ATTR                _loop
               12  STORE_FAST               'loop'

 L. 161        14  LOAD_FAST                'proc'
               16  LOAD_ATTR                stdin
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    66  'to 66'

 L. 162        24  LOAD_FAST                'loop'
               26  LOAD_METHOD              connect_write_pipe

 L. 163        28  LOAD_CLOSURE             'self'
               30  BUILD_TUPLE_1         1 
               32  LOAD_LAMBDA              '<code_object <lambda>>'
               34  LOAD_STR                 'BaseSubprocessTransport._connect_pipes.<locals>.<lambda>'
               36  MAKE_FUNCTION_8          'closure'

 L. 164        38  LOAD_FAST                'proc'
               40  LOAD_ATTR                stdin

 L. 162        42  CALL_METHOD_2         2  ''
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               '_'
               54  STORE_FAST               'pipe'

 L. 165        56  LOAD_FAST                'pipe'
               58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _pipes
               62  LOAD_CONST               0
               64  STORE_SUBSCR     
             66_0  COME_FROM            22  '22'

 L. 167        66  LOAD_FAST                'proc'
               68  LOAD_ATTR                stdout
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE   118  'to 118'

 L. 168        76  LOAD_FAST                'loop'
               78  LOAD_METHOD              connect_read_pipe

 L. 169        80  LOAD_CLOSURE             'self'
               82  BUILD_TUPLE_1         1 
               84  LOAD_LAMBDA              '<code_object <lambda>>'
               86  LOAD_STR                 'BaseSubprocessTransport._connect_pipes.<locals>.<lambda>'
               88  MAKE_FUNCTION_8          'closure'

 L. 170        90  LOAD_FAST                'proc'
               92  LOAD_ATTR                stdout

 L. 168        94  CALL_METHOD_2         2  ''
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               '_'
              106  STORE_FAST               'pipe'

 L. 171       108  LOAD_FAST                'pipe'
              110  LOAD_DEREF               'self'
              112  LOAD_ATTR                _pipes
              114  LOAD_CONST               1
              116  STORE_SUBSCR     
            118_0  COME_FROM            74  '74'

 L. 173       118  LOAD_FAST                'proc'
              120  LOAD_ATTR                stderr
              122  LOAD_CONST               None
              124  <117>                 1  ''
              126  POP_JUMP_IF_FALSE   170  'to 170'

 L. 174       128  LOAD_FAST                'loop'
              130  LOAD_METHOD              connect_read_pipe

 L. 175       132  LOAD_CLOSURE             'self'
              134  BUILD_TUPLE_1         1 
              136  LOAD_LAMBDA              '<code_object <lambda>>'
              138  LOAD_STR                 'BaseSubprocessTransport._connect_pipes.<locals>.<lambda>'
              140  MAKE_FUNCTION_8          'closure'

 L. 176       142  LOAD_FAST                'proc'
              144  LOAD_ATTR                stderr

 L. 174       146  CALL_METHOD_2         2  ''
              148  GET_AWAITABLE    
              150  LOAD_CONST               None
              152  YIELD_FROM       
              154  UNPACK_SEQUENCE_2     2 
              156  STORE_FAST               '_'
              158  STORE_FAST               'pipe'

 L. 177       160  LOAD_FAST                'pipe'
              162  LOAD_DEREF               'self'
              164  LOAD_ATTR                _pipes
              166  LOAD_CONST               2
              168  STORE_SUBSCR     
            170_0  COME_FROM           126  '126'

 L. 179       170  LOAD_DEREF               'self'
              172  LOAD_ATTR                _pending_calls
              174  LOAD_CONST               None
              176  <117>                 1  ''
              178  POP_JUMP_IF_TRUE    184  'to 184'
              180  <74>             
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'

 L. 181       184  LOAD_FAST                'loop'
              186  LOAD_METHOD              call_soon
              188  LOAD_DEREF               'self'
              190  LOAD_ATTR                _protocol
              192  LOAD_ATTR                connection_made
              194  LOAD_DEREF               'self'
              196  CALL_METHOD_2         2  ''
              198  POP_TOP          

 L. 182       200  LOAD_DEREF               'self'
              202  LOAD_ATTR                _pending_calls
              204  GET_ITER         
              206  FOR_ITER            234  'to 234'
              208  UNPACK_SEQUENCE_2     2 
              210  STORE_FAST               'callback'
              212  STORE_FAST               'data'

 L. 183       214  LOAD_FAST                'loop'
              216  LOAD_ATTR                call_soon
              218  LOAD_FAST                'callback'
              220  BUILD_LIST_1          1 
              222  LOAD_FAST                'data'
              224  CALL_FINALLY        227  'to 227'
              226  WITH_CLEANUP_FINISH
              228  CALL_FUNCTION_EX      0  'positional arguments only'
              230  POP_TOP          
              232  JUMP_BACK           206  'to 206'

 L. 184       234  LOAD_CONST               None
              236  LOAD_DEREF               'self'
              238  STORE_ATTR               _pending_calls
              240  POP_BLOCK        
              242  JUMP_FORWARD        336  'to 336'
            244_0  COME_FROM_FINALLY     0  '0'

 L. 185       244  DUP_TOP          
              246  LOAD_GLOBAL              SystemExit
              248  LOAD_GLOBAL              KeyboardInterrupt
              250  BUILD_TUPLE_2         2 
          252_254  <121>               268  ''
              256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L. 186       262  RAISE_VARARGS_0       0  'reraise'
              264  POP_EXCEPT       
              266  JUMP_FORWARD        366  'to 366'

 L. 187       268  DUP_TOP          
              270  LOAD_GLOBAL              BaseException
          272_274  <121>               334  ''
              276  POP_TOP          
              278  STORE_FAST               'exc'
              280  POP_TOP          
              282  SETUP_FINALLY       326  'to 326'

 L. 188       284  LOAD_FAST                'waiter'
              286  LOAD_CONST               None
              288  <117>                 1  ''
          290_292  POP_JUMP_IF_FALSE   314  'to 314'
              294  LOAD_FAST                'waiter'
              296  LOAD_METHOD              cancelled
              298  CALL_METHOD_0         0  ''
          300_302  POP_JUMP_IF_TRUE    314  'to 314'

 L. 189       304  LOAD_FAST                'waiter'
              306  LOAD_METHOD              set_exception
              308  LOAD_FAST                'exc'
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
            314_0  COME_FROM           300  '300'
            314_1  COME_FROM           290  '290'
              314  POP_BLOCK        
              316  POP_EXCEPT       
              318  LOAD_CONST               None
              320  STORE_FAST               'exc'
              322  DELETE_FAST              'exc'
              324  JUMP_FORWARD        366  'to 366'
            326_0  COME_FROM_FINALLY   282  '282'
              326  LOAD_CONST               None
              328  STORE_FAST               'exc'
              330  DELETE_FAST              'exc'
              332  <48>             
              334  <48>             
            336_0  COME_FROM           242  '242'

 L. 191       336  LOAD_FAST                'waiter'
              338  LOAD_CONST               None
              340  <117>                 1  ''
          342_344  POP_JUMP_IF_FALSE   366  'to 366'
              346  LOAD_FAST                'waiter'
              348  LOAD_METHOD              cancelled
              350  CALL_METHOD_0         0  ''
          352_354  POP_JUMP_IF_TRUE    366  'to 366'

 L. 192       356  LOAD_FAST                'waiter'
              358  LOAD_METHOD              set_result
              360  LOAD_CONST               None
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
            366_0  COME_FROM           352  '352'
            366_1  COME_FROM           342  '342'
            366_2  COME_FROM           324  '324'
            366_3  COME_FROM           266  '266'

Parse error at or near `<117>' instruction at offset 20

    def _call--- This code section failed: ---

 L. 195         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _pending_calls
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L. 196        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _pending_calls
               14  LOAD_METHOD              append
               16  LOAD_FAST                'cb'
               18  LOAD_FAST                'data'
               20  BUILD_TUPLE_2         2 
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM             8  '8'

 L. 198        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _loop
               32  LOAD_ATTR                call_soon
               34  LOAD_FAST                'cb'
               36  BUILD_LIST_1          1 
               38  LOAD_FAST                'data'
               40  CALL_FINALLY         43  'to 43'
               42  WITH_CLEANUP_FINISH
               44  CALL_FUNCTION_EX      0  'positional arguments only'
               46  POP_TOP          
             48_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    def _pipe_connection_lost(self, fd, exc):
        self._callself._protocol.pipe_connection_lostfdexc
        self._try_finish

    def _pipe_data_received(self, fd, data):
        self._callself._protocol.pipe_data_receivedfddata

    def _process_exited--- This code section failed: ---

 L. 208         0  LOAD_FAST                'returncode'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_FAST                'returncode'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 209        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _returncode
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_TRUE     36  'to 36'
               26  <74>             
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _returncode
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            24  '24'

 L. 210        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _loop
               40  LOAD_METHOD              get_debug
               42  CALL_METHOD_0         0  ''
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 211        46  LOAD_GLOBAL              logger
               48  LOAD_METHOD              info
               50  LOAD_STR                 '%r exited with return code %r'
               52  LOAD_FAST                'self'
               54  LOAD_FAST                'returncode'
               56  CALL_METHOD_3         3  ''
               58  POP_TOP          
             60_0  COME_FROM            44  '44'

 L. 212        60  LOAD_FAST                'returncode'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _returncode

 L. 213        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _proc
               70  LOAD_ATTR                returncode
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 216        78  LOAD_FAST                'returncode'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _proc
               84  STORE_ATTR               returncode
             86_0  COME_FROM            76  '76'

 L. 217        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _call
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                _protocol
               94  LOAD_ATTR                process_exited
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 218       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _try_finish
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          

 L. 221       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _exit_waiters
              112  GET_ITER         
            114_0  COME_FROM           124  '124'
              114  FOR_ITER            138  'to 138'
              116  STORE_FAST               'waiter'

 L. 222       118  LOAD_FAST                'waiter'
              120  LOAD_METHOD              cancelled
              122  CALL_METHOD_0         0  ''
              124  POP_JUMP_IF_TRUE    114  'to 114'

 L. 223       126  LOAD_FAST                'waiter'
              128  LOAD_METHOD              set_result
              130  LOAD_FAST                'returncode'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK           114  'to 114'

 L. 224       138  LOAD_CONST               None
              140  LOAD_FAST                'self'
              142  STORE_ATTR               _exit_waiters

Parse error at or near `None' instruction at offset -1

    async def _wait--- This code section failed: ---

 L. 230         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _returncode
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 231        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _returncode
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 233        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _loop
               20  LOAD_METHOD              create_future
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'waiter'

 L. 234        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _exit_waiters
               30  LOAD_METHOD              append
               32  LOAD_FAST                'waiter'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 235        38  LOAD_FAST                'waiter'
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _try_finish--- This code section failed: ---

 L. 238         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _finished
                4  POP_JUMP_IF_FALSE    10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 239        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _returncode
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 240        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 241        24  LOAD_GLOBAL              all
               26  LOAD_GENEXPR             '<code_object <genexpr>>'
               28  LOAD_STR                 'BaseSubprocessTransport._try_finish.<locals>.<genexpr>'
               30  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 242        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _pipes
               36  LOAD_METHOD              values
               38  CALL_METHOD_0         0  ''

 L. 241        40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_FALSE    68  'to 68'

 L. 243        48  LOAD_CONST               True
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _finished

 L. 244        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _call
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                _call_connection_lost
               62  LOAD_CONST               None
               64  CALL_METHOD_2         2  ''
               66  POP_TOP          
             68_0  COME_FROM            46  '46'

Parse error at or near `None' instruction at offset -1

    def _call_connection_lost--- This code section failed: ---

 L. 247         0  SETUP_FINALLY        36  'to 36'

 L. 248         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _protocol
                6  LOAD_METHOD              connection_lost
                8  LOAD_FAST                'exc'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        

 L. 250        16  LOAD_CONST               None
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _loop

 L. 251        22  LOAD_CONST               None
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _proc

 L. 252        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _protocol
               34  JUMP_FORWARD         56  'to 56'
             36_0  COME_FROM_FINALLY     0  '0'

 L. 250        36  LOAD_CONST               None
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _loop

 L. 251        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _proc

 L. 252        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _protocol
               54  <48>             
             56_0  COME_FROM            34  '34'

Parse error at or near `LOAD_FAST' instruction at offset 18


class WriteSubprocessPipeProto(protocols.BaseProtocol):

    def __init__(self, proc, fd):
        self.proc = proc
        self.fd = fd
        self.pipe = None
        self.disconnected = False

    def connection_made(self, transport):
        self.pipe = transport

    def __repr__(self):
        return f"<{self.__class__.__name__} fd={self.fd} pipe={self.pipe!r}>"

    def connection_lost(self, exc):
        self.disconnected = True
        self.proc._pipe_connection_lostself.fdexc
        self.proc = None

    def pause_writing(self):
        self.proc._protocol.pause_writing

    def resume_writing(self):
        self.proc._protocol.resume_writing


class ReadSubprocessPipeProto(WriteSubprocessPipeProto, protocols.Protocol):

    def data_received(self, data):
        self.proc._pipe_data_receivedself.fddata