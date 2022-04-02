# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\windows_utils.py
"""Various Windows specific bits and pieces."""
import sys
if sys.platform != 'win32':
    raise ImportError('win32 only')
import _winapi, itertools, msvcrt, os, subprocess, tempfile, warnings
__all__ = ('pipe', 'Popen', 'PIPE', 'PipeHandle')
BUFSIZE = 8192
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT
_mmap_counter = itertools.count()

def pipe--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL              tempfile
                2  LOAD_ATTR                mktemp

 L.  35         4  LOAD_STR                 '\\\\.\\pipe\\python-pipe-{:d}-{:d}-'
                6  LOAD_METHOD              format

 L.  36         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              getpid
               12  CALL_METHOD_0         0  ''
               14  LOAD_GLOBAL              next
               16  LOAD_GLOBAL              _mmap_counter
               18  CALL_FUNCTION_1       1  ''

 L.  35        20  CALL_METHOD_2         2  ''

 L.  34        22  LOAD_CONST               ('prefix',)
               24  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               26  STORE_FAST               'address'

 L.  38        28  LOAD_FAST                'duplex'
               30  POP_JUMP_IF_FALSE    62  'to 62'

 L.  39        32  LOAD_GLOBAL              _winapi
               34  LOAD_ATTR                PIPE_ACCESS_DUPLEX
               36  STORE_FAST               'openmode'

 L.  40        38  LOAD_GLOBAL              _winapi
               40  LOAD_ATTR                GENERIC_READ
               42  LOAD_GLOBAL              _winapi
               44  LOAD_ATTR                GENERIC_WRITE
               46  BINARY_OR        
               48  STORE_FAST               'access'

 L.  41        50  LOAD_FAST                'bufsize'
               52  LOAD_FAST                'bufsize'
               54  ROT_TWO          
               56  STORE_FAST               'obsize'
               58  STORE_FAST               'ibsize'
               60  JUMP_FORWARD         84  'to 84'
             62_0  COME_FROM            30  '30'

 L.  43        62  LOAD_GLOBAL              _winapi
               64  LOAD_ATTR                PIPE_ACCESS_INBOUND
               66  STORE_FAST               'openmode'

 L.  44        68  LOAD_GLOBAL              _winapi
               70  LOAD_ATTR                GENERIC_WRITE
               72  STORE_FAST               'access'

 L.  45        74  LOAD_CONST               0
               76  LOAD_FAST                'bufsize'
               78  ROT_TWO          
               80  STORE_FAST               'obsize'
               82  STORE_FAST               'ibsize'
             84_0  COME_FROM            60  '60'

 L.  47        84  LOAD_FAST                'openmode'
               86  LOAD_GLOBAL              _winapi
               88  LOAD_ATTR                FILE_FLAG_FIRST_PIPE_INSTANCE
               90  INPLACE_OR       
               92  STORE_FAST               'openmode'

 L.  49        94  LOAD_FAST                'overlapped'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L.  50       102  LOAD_FAST                'openmode'
              104  LOAD_GLOBAL              _winapi
              106  LOAD_ATTR                FILE_FLAG_OVERLAPPED
              108  INPLACE_OR       
              110  STORE_FAST               'openmode'
            112_0  COME_FROM           100  '100'

 L.  52       112  LOAD_FAST                'overlapped'
              114  LOAD_CONST               1
              116  BINARY_SUBSCR    
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L.  53       120  LOAD_GLOBAL              _winapi
              122  LOAD_ATTR                FILE_FLAG_OVERLAPPED
              124  STORE_FAST               'flags_and_attribs'
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM           118  '118'

 L.  55       128  LOAD_CONST               0
              130  STORE_FAST               'flags_and_attribs'
            132_0  COME_FROM           126  '126'

 L.  57       132  LOAD_CONST               None
              134  DUP_TOP          
              136  STORE_FAST               'h1'
              138  STORE_FAST               'h2'

 L.  58       140  SETUP_FINALLY       234  'to 234'

 L.  59       142  LOAD_GLOBAL              _winapi
              144  LOAD_METHOD              CreateNamedPipe

 L.  60       146  LOAD_FAST                'address'
              148  LOAD_FAST                'openmode'
              150  LOAD_GLOBAL              _winapi
              152  LOAD_ATTR                PIPE_WAIT

 L.  61       154  LOAD_CONST               1
              156  LOAD_FAST                'obsize'
              158  LOAD_FAST                'ibsize'
              160  LOAD_GLOBAL              _winapi
              162  LOAD_ATTR                NMPWAIT_WAIT_FOREVER
              164  LOAD_GLOBAL              _winapi
              166  LOAD_ATTR                NULL

 L.  59       168  CALL_METHOD_8         8  ''
              170  STORE_FAST               'h1'

 L.  63       172  LOAD_GLOBAL              _winapi
              174  LOAD_METHOD              CreateFile

 L.  64       176  LOAD_FAST                'address'
              178  LOAD_FAST                'access'
              180  LOAD_CONST               0
              182  LOAD_GLOBAL              _winapi
              184  LOAD_ATTR                NULL
              186  LOAD_GLOBAL              _winapi
              188  LOAD_ATTR                OPEN_EXISTING

 L.  65       190  LOAD_FAST                'flags_and_attribs'
              192  LOAD_GLOBAL              _winapi
              194  LOAD_ATTR                NULL

 L.  63       196  CALL_METHOD_7         7  ''
              198  STORE_FAST               'h2'

 L.  67       200  LOAD_GLOBAL              _winapi
              202  LOAD_ATTR                ConnectNamedPipe
              204  LOAD_FAST                'h1'
              206  LOAD_CONST               True
              208  LOAD_CONST               ('overlapped',)
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  STORE_FAST               'ov'

 L.  68       214  LOAD_FAST                'ov'
              216  LOAD_METHOD              GetOverlappedResult
              218  LOAD_CONST               True
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          

 L.  69       224  LOAD_FAST                'h1'
              226  LOAD_FAST                'h2'
              228  BUILD_TUPLE_2         2 
              230  POP_BLOCK        
              232  RETURN_VALUE     
            234_0  COME_FROM_FINALLY   140  '140'

 L.  70       234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L.  71       240  LOAD_FAST                'h1'
              242  LOAD_CONST               None
              244  <117>                 1  ''
          246_248  POP_JUMP_IF_FALSE   260  'to 260'

 L.  72       250  LOAD_GLOBAL              _winapi
              252  LOAD_METHOD              CloseHandle
              254  LOAD_FAST                'h1'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
            260_0  COME_FROM           246  '246'

 L.  73       260  LOAD_FAST                'h2'
              262  LOAD_CONST               None
              264  <117>                 1  ''
          266_268  POP_JUMP_IF_FALSE   280  'to 280'

 L.  74       270  LOAD_GLOBAL              _winapi
              272  LOAD_METHOD              CloseHandle
              274  LOAD_FAST                'h2'
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
            280_0  COME_FROM           266  '266'

 L.  75       280  RAISE_VARARGS_0       0  'reraise'
              282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
              286  <48>             
            288_0  COME_FROM           284  '284'

Parse error at or near `<117>' instruction at offset 244


class PipeHandle:
    __doc__ = 'Wrapper for an overlapped pipe handle which is vaguely file-object like.\n\n    The IOCP event loop can use these instead of socket objects.\n    '

    def __init__(self, handle):
        self._handle = handle

    def __repr__--- This code section failed: ---

 L.  90         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handle
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  91        10  LOAD_STR                 'handle='
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _handle
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  STORE_FAST               'handle'
               22  JUMP_FORWARD         28  'to 28'
             24_0  COME_FROM             8  '8'

 L.  93        24  LOAD_STR                 'closed'
               26  STORE_FAST               'handle'
             28_0  COME_FROM            22  '22'

 L.  94        28  LOAD_STR                 '<'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                __class__
               34  LOAD_ATTR                __name__
               36  FORMAT_VALUE          0  ''
               38  LOAD_STR                 ' '
               40  LOAD_FAST                'handle'
               42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 '>'
               46  BUILD_STRING_5        5 
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @property
    def handle(self):
        return self._handle

    def fileno--- This code section failed: ---

 L. 101         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handle
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 102        10  LOAD_GLOBAL              ValueError
               12  LOAD_STR                 'I/O operation on closed pipe'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 103        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _handle
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def close--- This code section failed: ---

 L. 106         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handle
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 107        10  LOAD_FAST                'CloseHandle'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _handle
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 108        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _handle
             26_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def __del__--- This code section failed: ---

 L. 111         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handle
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L. 112        10  LOAD_FAST                '_warn'
               12  LOAD_STR                 'unclosed '
               14  LOAD_FAST                'self'
               16  FORMAT_VALUE          2  '!r'
               18  BUILD_STRING_2        2 
               20  LOAD_GLOBAL              ResourceWarning
               22  LOAD_FAST                'self'
               24  LOAD_CONST               ('source',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  POP_TOP          

 L. 113        30  LOAD_FAST                'self'
               32  LOAD_METHOD              close
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
             38_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()


class Popen(subprocess.Popen):
    __doc__ = 'Replacement for subprocess.Popen using overlapped pipe handles.\n\n    The stdin, stdout, stderr are None or instances of PipeHandle.\n    '

    def __init__--- This code section failed: ---

 L. 131         0  LOAD_FAST                'kwds'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'universal_newlines'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 132        14  LOAD_FAST                'kwds'
               16  LOAD_METHOD              get
               18  LOAD_STR                 'bufsize'
               20  LOAD_CONST               0
               22  CALL_METHOD_2         2  ''
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  <74>             
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L. 133        34  LOAD_CONST               None
               36  DUP_TOP          
               38  STORE_FAST               'stdin_rfd'
               40  DUP_TOP          
               42  STORE_FAST               'stdout_wfd'
               44  STORE_FAST               'stderr_wfd'

 L. 134        46  LOAD_CONST               None
               48  DUP_TOP          
               50  STORE_FAST               'stdin_wh'
               52  DUP_TOP          
               54  STORE_FAST               'stdout_rh'
               56  STORE_FAST               'stderr_rh'

 L. 135        58  LOAD_FAST                'stdin'
               60  LOAD_GLOBAL              PIPE
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    98  'to 98'

 L. 136        66  LOAD_GLOBAL              pipe
               68  LOAD_CONST               (False, True)
               70  LOAD_CONST               True
               72  LOAD_CONST               ('overlapped', 'duplex')
               74  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'stdin_rh'
               80  STORE_FAST               'stdin_wh'

 L. 137        82  LOAD_GLOBAL              msvcrt
               84  LOAD_METHOD              open_osfhandle
               86  LOAD_FAST                'stdin_rh'
               88  LOAD_GLOBAL              os
               90  LOAD_ATTR                O_RDONLY
               92  CALL_METHOD_2         2  ''
               94  STORE_FAST               'stdin_rfd'
               96  JUMP_FORWARD        102  'to 102'
             98_0  COME_FROM            64  '64'

 L. 139        98  LOAD_FAST                'stdin'
              100  STORE_FAST               'stdin_rfd'
            102_0  COME_FROM            96  '96'

 L. 140       102  LOAD_FAST                'stdout'
              104  LOAD_GLOBAL              PIPE
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   138  'to 138'

 L. 141       110  LOAD_GLOBAL              pipe
              112  LOAD_CONST               (True, False)
              114  LOAD_CONST               ('overlapped',)
              116  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              118  UNPACK_SEQUENCE_2     2 
              120  STORE_FAST               'stdout_rh'
              122  STORE_FAST               'stdout_wh'

 L. 142       124  LOAD_GLOBAL              msvcrt
              126  LOAD_METHOD              open_osfhandle
              128  LOAD_FAST                'stdout_wh'
              130  LOAD_CONST               0
              132  CALL_METHOD_2         2  ''
              134  STORE_FAST               'stdout_wfd'
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM           108  '108'

 L. 144       138  LOAD_FAST                'stdout'
              140  STORE_FAST               'stdout_wfd'
            142_0  COME_FROM           136  '136'

 L. 145       142  LOAD_FAST                'stderr'
              144  LOAD_GLOBAL              PIPE
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   178  'to 178'

 L. 146       150  LOAD_GLOBAL              pipe
              152  LOAD_CONST               (True, False)
              154  LOAD_CONST               ('overlapped',)
              156  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              158  UNPACK_SEQUENCE_2     2 
              160  STORE_FAST               'stderr_rh'
              162  STORE_FAST               'stderr_wh'

 L. 147       164  LOAD_GLOBAL              msvcrt
              166  LOAD_METHOD              open_osfhandle
              168  LOAD_FAST                'stderr_wh'
              170  LOAD_CONST               0
              172  CALL_METHOD_2         2  ''
              174  STORE_FAST               'stderr_wfd'
              176  JUMP_FORWARD        196  'to 196'
            178_0  COME_FROM           148  '148'

 L. 148       178  LOAD_FAST                'stderr'
              180  LOAD_GLOBAL              STDOUT
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   192  'to 192'

 L. 149       186  LOAD_FAST                'stdout_wfd'
              188  STORE_FAST               'stderr_wfd'
              190  JUMP_FORWARD        196  'to 196'
            192_0  COME_FROM           184  '184'

 L. 151       192  LOAD_FAST                'stderr'
              194  STORE_FAST               'stderr_wfd'
            196_0  COME_FROM           190  '190'
            196_1  COME_FROM           176  '176'

 L. 152       196  SETUP_FINALLY       404  'to 404'
              198  SETUP_FINALLY       232  'to 232'

 L. 153       200  LOAD_GLOBAL              super
              202  CALL_FUNCTION_0       0  ''
              204  LOAD_ATTR                __init__
              206  LOAD_FAST                'args'
              208  BUILD_TUPLE_1         1 
              210  LOAD_FAST                'stdin_rfd'
              212  LOAD_FAST                'stdout_wfd'

 L. 154       214  LOAD_FAST                'stderr_wfd'

 L. 153       216  LOAD_CONST               ('stdin', 'stdout', 'stderr')
              218  BUILD_CONST_KEY_MAP_3     3 

 L. 154       220  LOAD_FAST                'kwds'

 L. 153       222  <164>                 1  ''
              224  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              226  POP_TOP          
              228  POP_BLOCK        
              230  JUMP_FORWARD        280  'to 280'
            232_0  COME_FROM_FINALLY   198  '198'

 L. 155       232  POP_TOP          
              234  POP_TOP          
              236  POP_TOP          

 L. 156       238  LOAD_FAST                'stdin_wh'
              240  LOAD_FAST                'stdout_rh'
              242  LOAD_FAST                'stderr_rh'
              244  BUILD_TUPLE_3         3 
              246  GET_ITER         
            248_0  COME_FROM           258  '258'
              248  FOR_ITER            272  'to 272'
              250  STORE_FAST               'h'

 L. 157       252  LOAD_FAST                'h'
              254  LOAD_CONST               None
              256  <117>                 1  ''
              258  POP_JUMP_IF_FALSE   248  'to 248'

 L. 158       260  LOAD_GLOBAL              _winapi
              262  LOAD_METHOD              CloseHandle
              264  LOAD_FAST                'h'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  JUMP_BACK           248  'to 248'

 L. 159       272  RAISE_VARARGS_0       0  'reraise'
              274  POP_EXCEPT       
              276  JUMP_FORWARD        340  'to 340'
              278  <48>             
            280_0  COME_FROM           230  '230'

 L. 161       280  LOAD_FAST                'stdin_wh'
              282  LOAD_CONST               None
              284  <117>                 1  ''
          286_288  POP_JUMP_IF_FALSE   300  'to 300'

 L. 162       290  LOAD_GLOBAL              PipeHandle
              292  LOAD_FAST                'stdin_wh'
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_FAST                'self'
              298  STORE_ATTR               stdin
            300_0  COME_FROM           286  '286'

 L. 163       300  LOAD_FAST                'stdout_rh'
              302  LOAD_CONST               None
              304  <117>                 1  ''
          306_308  POP_JUMP_IF_FALSE   320  'to 320'

 L. 164       310  LOAD_GLOBAL              PipeHandle
              312  LOAD_FAST                'stdout_rh'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_FAST                'self'
              318  STORE_ATTR               stdout
            320_0  COME_FROM           306  '306'

 L. 165       320  LOAD_FAST                'stderr_rh'
              322  LOAD_CONST               None
              324  <117>                 1  ''
          326_328  POP_JUMP_IF_FALSE   340  'to 340'

 L. 166       330  LOAD_GLOBAL              PipeHandle
              332  LOAD_FAST                'stderr_rh'
              334  CALL_FUNCTION_1       1  ''
              336  LOAD_FAST                'self'
              338  STORE_ATTR               stderr
            340_0  COME_FROM           326  '326'
            340_1  COME_FROM           276  '276'
              340  POP_BLOCK        

 L. 168       342  LOAD_FAST                'stdin'
              344  LOAD_GLOBAL              PIPE
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   362  'to 362'

 L. 169       352  LOAD_GLOBAL              os
              354  LOAD_METHOD              close
              356  LOAD_FAST                'stdin_rfd'
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
            362_0  COME_FROM           348  '348'

 L. 170       362  LOAD_FAST                'stdout'
              364  LOAD_GLOBAL              PIPE
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   382  'to 382'

 L. 171       372  LOAD_GLOBAL              os
              374  LOAD_METHOD              close
              376  LOAD_FAST                'stdout_wfd'
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
            382_0  COME_FROM           368  '368'

 L. 172       382  LOAD_FAST                'stderr'
              384  LOAD_GLOBAL              PIPE
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   466  'to 466'

 L. 173       392  LOAD_GLOBAL              os
              394  LOAD_METHOD              close
              396  LOAD_FAST                'stderr_wfd'
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          
              402  JUMP_FORWARD        466  'to 466'
            404_0  COME_FROM_FINALLY   196  '196'

 L. 168       404  LOAD_FAST                'stdin'
              406  LOAD_GLOBAL              PIPE
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   424  'to 424'

 L. 169       414  LOAD_GLOBAL              os
              416  LOAD_METHOD              close
              418  LOAD_FAST                'stdin_rfd'
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           410  '410'

 L. 170       424  LOAD_FAST                'stdout'
              426  LOAD_GLOBAL              PIPE
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   444  'to 444'

 L. 171       434  LOAD_GLOBAL              os
              436  LOAD_METHOD              close
              438  LOAD_FAST                'stdout_wfd'
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          
            444_0  COME_FROM           430  '430'

 L. 172       444  LOAD_FAST                'stderr'
              446  LOAD_GLOBAL              PIPE
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_FALSE   464  'to 464'

 L. 173       454  LOAD_GLOBAL              os
              456  LOAD_METHOD              close
              458  LOAD_FAST                'stderr_wfd'
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
            464_0  COME_FROM           450  '450'
              464  <48>             
            466_0  COME_FROM           402  '402'
            466_1  COME_FROM           388  '388'

Parse error at or near `None' instruction at offset -1