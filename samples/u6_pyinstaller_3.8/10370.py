# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

 L.  36        14  LOAD_GLOBAL              next
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

 L.  60       148  LOAD_FAST                'openmode'

 L.  60       150  LOAD_GLOBAL              _winapi
              152  LOAD_ATTR                PIPE_WAIT

 L.  61       154  LOAD_CONST               1

 L.  61       156  LOAD_FAST                'obsize'

 L.  61       158  LOAD_FAST                'ibsize'

 L.  61       160  LOAD_GLOBAL              _winapi
              162  LOAD_ATTR                NMPWAIT_WAIT_FOREVER

 L.  61       164  LOAD_GLOBAL              _winapi
              166  LOAD_ATTR                NULL

 L.  59       168  CALL_METHOD_8         8  ''
              170  STORE_FAST               'h1'

 L.  63       172  LOAD_GLOBAL              _winapi
              174  LOAD_METHOD              CreateFile

 L.  64       176  LOAD_FAST                'address'

 L.  64       178  LOAD_FAST                'access'

 L.  64       180  LOAD_CONST               0

 L.  64       182  LOAD_GLOBAL              _winapi
              184  LOAD_ATTR                NULL

 L.  64       186  LOAD_GLOBAL              _winapi
              188  LOAD_ATTR                OPEN_EXISTING

 L.  65       190  LOAD_FAST                'flags_and_attribs'

 L.  65       192  LOAD_GLOBAL              _winapi
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
              244  COMPARE_OP               is-not
          246_248  POP_JUMP_IF_FALSE   260  'to 260'

 L.  72       250  LOAD_GLOBAL              _winapi
              252  LOAD_METHOD              CloseHandle
              254  LOAD_FAST                'h1'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          
            260_0  COME_FROM           246  '246'

 L.  73       260  LOAD_FAST                'h2'
              262  LOAD_CONST               None
              264  COMPARE_OP               is-not
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
              286  END_FINALLY      
            288_0  COME_FROM           284  '284'

Parse error at or near `POP_TOP' instruction at offset 258


class PipeHandle:
    __doc__ = 'Wrapper for an overlapped pipe handle which is vaguely file-object like.\n\n    The IOCP event loop can use these instead of socket objects.\n    '

    def __init__(self, handle):
        self._handle = handle

    def __repr__(self):
        if self._handle is not None:
            handle = f"handle={self._handle!r}"
        else:
            handle = 'closed'
        return f"<{self.__class__.__name__} {handle}>"

    @property
    def handle(self):
        return self._handle

    def fileno(self):
        if self._handle is None:
            raise ValueError('I/O operation on closed pipe')
        return self._handle

    def close(self, *, CloseHandle=_winapi.CloseHandle):
        if self._handle is not None:
            CloseHandle(self._handle)
            self._handle = None

    def __del__(self, _warn=warnings.warn):
        if self._handle is not None:
            _warn(f"unclosed {self!r}", ResourceWarning, source=self)
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()


class Popen(subprocess.Popen):
    __doc__ = 'Replacement for subprocess.Popen using overlapped pipe handles.\n\n    The stdin, stdout, stderr are None or instances of PipeHandle.\n    '

    def __init__(self, args, stdin=None, stdout=None, stderr=None, **kwds):
        if kwds.get'universal_newlines':
            raise AssertionError
        elif not kwds.get'bufsize'0 == 0:
            raise AssertionError
        else:
            stdin_rfd = stdout_wfd = stderr_wfd = None
            stdin_wh = stdout_rh = stderr_rh = None
            if stdin == PIPE:
                stdin_rh, stdin_wh = pipe(overlapped=(False, True), duplex=True)
                stdin_rfd = msvcrt.open_osfhandlestdin_rhos.O_RDONLY
            else:
                stdin_rfd = stdin
            if stdout == PIPE:
                stdout_rh, stdout_wh = pipe(overlapped=(True, False))
                stdout_wfd = msvcrt.open_osfhandlestdout_wh0
            else:
                stdout_wfd = stdout
            if stderr == PIPE:
                stderr_rh, stderr_wh = pipe(overlapped=(True, False))
                stderr_wfd = msvcrt.open_osfhandlestderr_wh0
            else:
                if stderr == STDOUT:
                    stderr_wfd = stdout_wfd
                else:
                    stderr_wfd = stderr
        try:
            try:
                (super().__init__)(args, stdin=stdin_rfd, stdout=stdout_wfd, stderr=stderr_wfd, **kwds)
            except:
                for h in (
                 stdin_wh, stdout_rh, stderr_rh):
                    if h is not None:
                        _winapi.CloseHandleh
                else:
                    raise

            else:
                if stdin_wh is not None:
                    self.stdin = PipeHandle(stdin_wh)
                if stdout_rh is not None:
                    self.stdout = PipeHandle(stdout_rh)
            if stderr_rh is not None:
                self.stderr = PipeHandle(stderr_rh)
        finally:
            if stdin == PIPE:
                os.closestdin_rfd
            if stdout == PIPE:
                os.closestdout_wfd
            if stderr == PIPE:
                os.closestderr_wfd