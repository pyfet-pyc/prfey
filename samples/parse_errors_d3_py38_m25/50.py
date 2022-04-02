# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: subprocess.py
"""Subprocesses with accessible I/O streams

This module allows you to spawn processes, connect to their
input/output/error pipes, and obtain their return codes.

For a complete description of this module see the Python documentation.

Main API
========
run(...): Runs a command, waits for it to complete, then returns a
          CompletedProcess instance.
Popen(...): A class for flexibly executing a command in a new process

Constants
---------
DEVNULL: Special value that indicates that os.devnull should be used
PIPE:    Special value that indicates a pipe should be created
STDOUT:  Special value that indicates that stderr should go to stdout

Older API
=========
call(...): Runs a command, waits for it to complete, then returns
    the return code.
check_call(...): Same as call() but raises CalledProcessError()
    if return code is not 0
check_output(...): Same as check_call() but returns the contents of
    stdout instead of a return code
getoutput(...): Runs a command in the shell, waits for it to complete,
    then returns the output
getstatusoutput(...): Runs a command in the shell, waits for it to complete,
    then returns a (exitcode, output) tuple
"""
import builtins, errno, io, os, time, signal, sys, threading, warnings, contextlib
from time import monotonic as _time
__all__ = [
 'Popen', 'PIPE', 'STDOUT', 'call', 'check_call', 'getstatusoutput',
 'getoutput', 'check_output', 'run', 'CalledProcessError', 'DEVNULL',
 'SubprocessError', 'TimeoutExpired', 'CompletedProcess']
try:
    import msvcrt, _winapi
    _mswindows = True
except ModuleNotFoundError:
    _mswindows = False
    import _posixsubprocess, select, selectors
else:
    from _winapi import CREATE_NEW_CONSOLE, CREATE_NEW_PROCESS_GROUP, STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE, SW_HIDE, STARTF_USESTDHANDLES, STARTF_USESHOWWINDOW, ABOVE_NORMAL_PRIORITY_CLASS, BELOW_NORMAL_PRIORITY_CLASS, HIGH_PRIORITY_CLASS, IDLE_PRIORITY_CLASS, NORMAL_PRIORITY_CLASS, REALTIME_PRIORITY_CLASS, CREATE_NO_WINDOW, DETACHED_PROCESS, CREATE_DEFAULT_ERROR_MODE, CREATE_BREAKAWAY_FROM_JOB
    __all__.extend(['CREATE_NEW_CONSOLE', 'CREATE_NEW_PROCESS_GROUP',
     'STD_INPUT_HANDLE', 'STD_OUTPUT_HANDLE',
     'STD_ERROR_HANDLE', 'SW_HIDE',
     'STARTF_USESTDHANDLES', 'STARTF_USESHOWWINDOW',
     'STARTUPINFO',
     'ABOVE_NORMAL_PRIORITY_CLASS', 'BELOW_NORMAL_PRIORITY_CLASS',
     'HIGH_PRIORITY_CLASS', 'IDLE_PRIORITY_CLASS',
     'NORMAL_PRIORITY_CLASS', 'REALTIME_PRIORITY_CLASS',
     'CREATE_NO_WINDOW', 'DETACHED_PROCESS',
     'CREATE_DEFAULT_ERROR_MODE', 'CREATE_BREAKAWAY_FROM_JOB'])

class SubprocessError(Exception):
    pass


class CalledProcessError(SubprocessError):
    __doc__ = 'Raised when run() is called with check=True and the process\n    returns a non-zero exit status.\n\n    Attributes:\n      cmd, returncode, stdout, stderr, output\n    '

    def __init__(self, returncode, cmd, output=None, stderr=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr

    def __str__(self):
        if self.returncode and self.returncode < 0:
            try:
                return "Command '%s' died with %r." % (
                 self.cmd, signal.Signals(-self.returncode))
            except ValueError:
                return "Command '%s' died with unknown signal %d." % (
                 self.cmd, -self.returncode)

        else:
            return "Command '%s' returned non-zero exit status %d." % (
             self.cmd, self.returncode)

    @property
    def stdout(self):
        """Alias for output attribute, to match stderr"""
        return self.output

    @stdout.setter
    def stdout(self, value):
        self.output = value


class TimeoutExpired(SubprocessError):
    __doc__ = 'This exception is raised when the timeout expires while waiting for a\n    child process.\n\n    Attributes:\n        cmd, output, stdout, stderr, timeout\n    '

    def __init__(self, cmd, timeout, output=None, stderr=None):
        self.cmd = cmd
        self.timeout = timeout
        self.output = output
        self.stderr = stderr

    def __str__(self):
        return "Command '%s' timed out after %s seconds" % (
         self.cmd, self.timeout)

    @property
    def stdout(self):
        return self.output

    @stdout.setter
    def stdout(self, value):
        self.output = value


if _mswindows:

    class STARTUPINFO:

        def __init__(self, *, dwFlags=0, hStdInput=None, hStdOutput=None, hStdError=None, wShowWindow=0, lpAttributeList=None):
            self.dwFlags = dwFlags
            self.hStdInput = hStdInput
            self.hStdOutput = hStdOutput
            self.hStdError = hStdError
            self.wShowWindow = wShowWindow
            self.lpAttributeList = lpAttributeList or {'handle_list': []}

        def copy(self):
            attr_list = self.lpAttributeList.copy()
            if 'handle_list' in attr_list:
                attr_list['handle_list'] = list(attr_list['handle_list'])
            return STARTUPINFO(dwFlags=(self.dwFlags), hStdInput=(self.hStdInput),
              hStdOutput=(self.hStdOutput),
              hStdError=(self.hStdError),
              wShowWindow=(self.wShowWindow),
              lpAttributeList=attr_list)


    class Handle(int):
        closed = False

        def Close(self, CloseHandle=_winapi.CloseHandle):
            if not self.closed:
                self.closed = True
                CloseHandle(self)

        def Detach(self):
            if not self.closed:
                self.closed = True
                return int(self)
            raise ValueError('already closed')

        def __repr__(self):
            return '%s(%d)' % (self.__class__.__name__, int(self))

        __del__ = Close


else:
    _PIPE_BUF = getattr(select, 'PIPE_BUF', 512)
    if hasattr(selectors, 'PollSelector'):
        _PopenSelector = selectors.PollSelector
    else:
        _PopenSelector = selectors.SelectSelector
if _mswindows:
    _active = None

    def _cleanup():
        pass


else:
    _active = []

    def _cleanup():
        if _active is None:
            return
        for inst in _active[:]:
            res = inst._internal_poll(_deadstate=(sys.maxsize))
            if res is not None:
                try:
                    _active.remove(inst)
                except ValueError:
                    pass


PIPE = -1
STDOUT = -2
DEVNULL = -3

def _optim_args_from_interpreter_flags():
    """Return a list of command-line arguments reproducing the current
    optimization settings in sys.flags."""
    args = []
    value = sys.flags.optimize
    if value > 0:
        args.append('-' + 'O' * value)
    return args


def _args_from_interpreter_flags():
    """Return a list of command-line arguments reproducing the current
    settings in sys.flags, sys.warnoptions and sys._xoptions."""
    flag_opt_map = {'debug':'d', 
     'dont_write_bytecode':'B', 
     'no_site':'S', 
     'verbose':'v', 
     'bytes_warning':'b', 
     'quiet':'q'}
    args = _optim_args_from_interpreter_flags()
    for flag, opt in flag_opt_map.items():
        v = getattr(sys.flags, flag)
        if v > 0:
            args.append('-' + opt * v)
    else:
        if sys.flags.isolated:
            args.append('-I')
        else:
            if sys.flags.ignore_environment:
                args.append('-E')
            if sys.flags.no_user_site:
                args.append('-s')
        warnopts = sys.warnoptions[:]
        bytes_warning = sys.flags.bytes_warning
        xoptions = getattr(sys, '_xoptions', {})
        dev_mode = 'dev' in xoptions
        if bytes_warning > 1:
            warnopts.remove('error::BytesWarning')
        elif bytes_warning:
            warnopts.remove('default::BytesWarning')
        if dev_mode:
            warnopts.remove('default')

    for opt in warnopts:
        args.append('-W' + opt)
    else:
        if dev_mode:
            args.extend(('-X', 'dev'))
        for opt in ('faulthandler', 'tracemalloc', 'importtime', 'showalloccount',
                    'showrefcount', 'utf8'):
            if opt in xoptions:
                value = xoptions[opt]
                if value is True:
                    arg = opt
                else:
                    arg = '%s=%s' % (opt, value)
                args.extend(('-X', arg))
        else:
            return args


def call--- This code section failed: ---

 L. 340         0  LOAD_GLOBAL              Popen
                2  LOAD_FAST                'popenargs'
                4  LOAD_FAST                'kwargs'
                6  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
                8  SETUP_WITH           66  'to 66'
               10  STORE_FAST               'p'

 L. 341        12  SETUP_FINALLY        40  'to 40'

 L. 342        14  LOAD_FAST                'p'
               16  LOAD_ATTR                wait
               18  LOAD_FAST                'timeout'
               20  LOAD_CONST               ('timeout',)
               22  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               24  POP_BLOCK        
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    12  '12'

 L. 343        40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 344        46  LOAD_FAST                'p'
               48  LOAD_METHOD              kill
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 346        54  RAISE_VARARGS_0       0  'reraise'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'
               62  POP_BLOCK        
               64  BEGIN_FINALLY    
             66_0  COME_FROM_WITH        8  '8'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 26


def check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the call function.  Example:

    check_call(["ls", "-l"])
    """
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd)
    return 0


def check_output(*popenargs, timeout=None, **kwargs):
    r"""Run command with arguments and return its output.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    b'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    b'ls: non_existent_file: No such file or directory\n'

    There is an additional optional argument, "input", allowing you to
    pass a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's "stdin" argument, as
    it too will be used internally.  Example:

    >>> check_output(["sed", "-e", "s/foo/bar/"],
    ...              input=b"when in the course of fooman events\n")
    b'when in the course of barman events\n'

    By default, all communication is in bytes, and therefore any "input"
    should be bytes, and the return value will be bytes.  If in text mode,
    any "input" should be a string, and the return value will be a string
    decoded according to locale encoding, or by "encoding" if set. Text mode
    is triggered by setting any of text, encoding, errors or universal_newlines.
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    if 'input' in kwargs:
        if kwargs['input'] is None:
            kwargs['input'] = '' if kwargs.get('universal_newlines', False) else b''
    return run(popenargs, stdout=PIPE, timeout=timeout, check=True, **kwargs).stdout


class CompletedProcess(object):
    __doc__ = 'A process that has finished running.\n\n    This is returned by run().\n\n    Attributes:\n      args: The list or str args passed to run().\n      returncode: The exit code of the process, negative for signals.\n      stdout: The standard output (None if not captured).\n      stderr: The standard error (None if not captured).\n    '

    def __init__(self, args, returncode, stdout=None, stderr=None):
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        args = [
         'args={!r}'.format(self.args),
         'returncode={!r}'.format(self.returncode)]
        if self.stdout is not None:
            args.append('stdout={!r}'.format(self.stdout))
        if self.stderr is not None:
            args.append('stderr={!r}'.format(self.stderr))
        return '{}({})'.format(type(self).__name__, ', '.join(args))

    def check_returncode(self):
        """Raise CalledProcessError if the exit code is non-zero."""
        if self.returncode:
            raise CalledProcessError(self.returncode, self.args, self.stdout, self.stderr)


def run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs):
    """Run command with arguments and return a CompletedProcess instance.

    The returned instance will have attributes args, returncode, stdout and
    stderr. By default, stdout and stderr are not captured, and those attributes
    will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them.

    If check is True and the exit code was non-zero, it raises a
    CalledProcessError. The CalledProcessError object will have the return code
    in the returncode attribute, and output & stderr attributes if those streams
    were captured.

    If timeout is given, and the process takes too long, a TimeoutExpired
    exception will be raised.

    There is an optional argument "input", allowing you to
    pass bytes or a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's "stdin" argument, as
    it will be used internally.

    By default, all communication is in bytes, and therefore any "input" should
    be bytes, and the stdout and stderr will be bytes. If in text mode, any
    "input" should be a string, and stdout and stderr will be strings decoded
    according to locale encoding, or by "encoding" if set. Text mode is
    triggered by setting any of text, encoding, errors or universal_newlines.

    The other arguments are the same as for the Popen constructor.
    """
    if input is not None:
        if kwargs.get('stdin') is not None:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = PIPE
    if capture_output:
        if kwargs.get('stdout') is not None or (kwargs.get('stderr') is not None):
            raise ValueError('stdout and stderr arguments may not be used with capture_output.')
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE
    with Popen(*popenargs, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except TimeoutExpired as exc:
            try:
                process.kill()
                if _mswindows:
                    exc.stdout, exc.stderr = process.communicate()
                else:
                    process.wait()
                raise
            finally:
                exc = None
                del exc

        except:
            process.kill()
            raise
        else:
            retcode = process.poll()
            if check:
                if retcode:
                    raise CalledProcessError(retcode, (process.args), output=stdout,
                      stderr=stderr)
    return CompletedProcess(process.args, retcode, stdout, stderr)


def list2cmdline(seq):
    """
    Translate a sequence of arguments into a command line
    string, using the same rules as the MS C runtime:

    1) Arguments are delimited by white space, which is either a
       space or a tab.

    2) A string surrounded by double quotation marks is
       interpreted as a single argument, regardless of white space
       contained within.  A quoted string can be embedded in an
       argument.

    3) A double quotation mark preceded by a backslash is
       interpreted as a literal double quotation mark.

    4) Backslashes are interpreted literally, unless they
       immediately precede a double quotation mark.

    5) If backslashes immediately precede a double quotation mark,
       every pair of backslashes is interpreted as a literal
       backslash.  If the number of backslashes is odd, the last
       backslash escapes the next double quotation mark as
       described in rule 3.
    """
    result = []
    needquote = False
    for arg in map(os.fsdecode, seq):
        bs_buf = []
        if result:
            result.append(' ')
        needquote = ' ' in arg or '\t' in arg or not arg
        if needquote:
            result.append('"')
        for c in arg:
            if c == '\\':
                bs_buf.append(c)
            else:
                if c == '"':
                    result.append('\\' * len(bs_buf) * 2)
                    bs_buf = []
                    result.append('\\"')
                else:
                    if bs_buf:
                        result.extend(bs_buf)
                        bs_buf = []
                    result.append(c)
                if bs_buf:
                    result.extend(bs_buf)
                if needquote:
                    result.extend(bs_buf)
                    result.append('"')
        else:
            return ''.join(result)


def getstatusoutput(cmd):
    """Return (exitcode, output) of executing cmd in a shell.

    Execute the string 'cmd' in a shell with 'check_output' and
    return a 2-tuple (status, output). The locale encoding is used
    to decode the output and process newlines.

    A trailing newline is stripped from the output.
    The exit status for the command can be interpreted
    according to the rules for the function 'wait'. Example:

    >>> import subprocess
    >>> subprocess.getstatusoutput('ls /bin/ls')
    (0, '/bin/ls')
    >>> subprocess.getstatusoutput('cat /bin/junk')
    (1, 'cat: /bin/junk: No such file or directory')
    >>> subprocess.getstatusoutput('/bin/junk')
    (127, 'sh: /bin/junk: not found')
    >>> subprocess.getstatusoutput('/bin/kill $$')
    (-15, '')
    """
    try:
        data = check_output(cmd, shell=True, text=True, stderr=STDOUT)
        exitcode = 0
    except CalledProcessError as ex:
        try:
            data = ex.output
            exitcode = ex.returncode
        finally:
            ex = None
            del ex

    else:
        if data[-1:] == '\n':
            data = data[:-1]
        else:
            return (
             exitcode, data)


def getoutput(cmd):
    """Return output (stdout or stderr) of executing cmd in a shell.

    Like getstatusoutput(), except the exit status is ignored and the return
    value is a string containing the command's output.  Example:

    >>> import subprocess
    >>> subprocess.getoutput('ls /bin/ls')
    '/bin/ls'
    """
    return getstatusoutput(cmd)[1]


def _use_posix_spawn--- This code section failed: ---

 L. 647         0  LOAD_GLOBAL              _mswindows
                2  POP_JUMP_IF_TRUE     14  'to 14'
                4  LOAD_GLOBAL              hasattr
                6  LOAD_GLOBAL              os
                8  LOAD_STR                 'posix_spawn'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'
             14_0  COME_FROM             2  '2'

 L. 649        14  LOAD_CONST               False
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 651        18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                platform
               22  LOAD_STR                 'darwin'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 653        28  LOAD_CONST               True
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 656        32  SETUP_FINALLY       140  'to 140'

 L. 657        34  LOAD_GLOBAL              os
               36  LOAD_METHOD              confstr
               38  LOAD_STR                 'CS_GNU_LIBC_VERSION'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'ver'

 L. 659        44  LOAD_FAST                'ver'
               46  LOAD_ATTR                split
               48  LOAD_CONST               1
               50  LOAD_CONST               ('maxsplit',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  STORE_FAST               'parts'

 L. 660        56  LOAD_GLOBAL              len
               58  LOAD_FAST                'parts'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_CONST               2
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE    72  'to 72'

 L. 662        68  LOAD_GLOBAL              ValueError
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            66  '66'

 L. 663        72  LOAD_FAST                'parts'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  STORE_FAST               'libc'

 L. 664        80  LOAD_GLOBAL              tuple
               82  LOAD_GLOBAL              map
               84  LOAD_GLOBAL              int
               86  LOAD_FAST                'parts'
               88  LOAD_CONST               1
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              split
               94  LOAD_STR                 '.'
               96  CALL_METHOD_1         1  ''
               98  CALL_FUNCTION_2       2  ''
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'version'

 L. 666       104  LOAD_GLOBAL              sys
              106  LOAD_ATTR                platform
              108  LOAD_STR                 'linux'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   136  'to 136'
              114  LOAD_FAST                'libc'
              116  LOAD_STR                 'glibc'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   136  'to 136'
              122  LOAD_FAST                'version'
              124  LOAD_CONST               (2, 24)
              126  COMPARE_OP               >=
              128  POP_JUMP_IF_FALSE   136  'to 136'

 L. 669       130  POP_BLOCK        
              132  LOAD_CONST               True
              134  RETURN_VALUE     
            136_0  COME_FROM           128  '128'
            136_1  COME_FROM           120  '120'
            136_2  COME_FROM           112  '112'
              136  POP_BLOCK        
              138  JUMP_FORWARD        166  'to 166'
            140_0  COME_FROM_FINALLY    32  '32'

 L. 673       140  DUP_TOP          
              142  LOAD_GLOBAL              AttributeError
              144  LOAD_GLOBAL              ValueError
              146  LOAD_GLOBAL              OSError
              148  BUILD_TUPLE_3         3 
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   164  'to 164'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 675       160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           152  '152'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'
            166_1  COME_FROM           138  '138'

 L. 678       166  LOAD_CONST               False
              168  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 132


_USE_POSIX_SPAWN = _use_posix_spawn()

class Popen(object):
    __doc__ = " Execute a child program in a new process.\n\n    For a complete description of the arguments see the Python documentation.\n\n    Arguments:\n      args: A string, or a sequence of program arguments.\n\n      bufsize: supplied as the buffering argument to the open() function when\n          creating the stdin/stdout/stderr pipe file objects\n\n      executable: A replacement program to execute.\n\n      stdin, stdout and stderr: These specify the executed programs' standard\n          input, standard output and standard error file handles, respectively.\n\n      preexec_fn: (POSIX only) An object to be called in the child process\n          just before the child is executed.\n\n      close_fds: Controls closing or inheriting of file descriptors.\n\n      shell: If true, the command will be executed through the shell.\n\n      cwd: Sets the current directory before the child is executed.\n\n      env: Defines the environment variables for the new process.\n\n      text: If true, decode stdin, stdout and stderr using the given encoding\n          (if set) or the system default otherwise.\n\n      universal_newlines: Alias of text, provided for backwards compatibility.\n\n      startupinfo and creationflags (Windows only)\n\n      restore_signals (POSIX only)\n\n      start_new_session (POSIX only)\n\n      pass_fds (POSIX only)\n\n      encoding and errors: Text mode encoding and error handling to use for\n          file objects stdin, stdout and stderr.\n\n    Attributes:\n        stdin, stdout, stderr, pid, returncode\n    "
    _child_created = False

    def __init__(self, args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None, text=None):
        """Create new Popen instance."""
        _cleanup()
        self._waitpid_lock = threading.Lock()
        self._input = None
        self._communication_started = False
        if bufsize is None:
            bufsize = -1
        if not isinstance(bufsize, int):
            raise TypeError('bufsize must be an integer')
        if _mswindows:
            if preexec_fn is not None:
                raise ValueError('preexec_fn is not supported on Windows platforms')
        elif pass_fds:
            if not close_fds:
                warnings.warn('pass_fds overriding close_fds.', RuntimeWarning)
                close_fds = True
            if startupinfo is not None:
                raise ValueError('startupinfo is only supported on Windows platforms')
            if creationflags != 0:
                raise ValueError('creationflags is only supported on Windows platforms')
        self.args = args
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.pid = None
        self.returncode = None
        self.encoding = encoding
        self.errors = errors
        if text is not None:
            if universal_newlines is not None:
                if bool(universal_newlines) != bool(text):
                    raise SubprocessError('Cannot disambiguate when both text and universal_newlines are supplied but different. Pass one or the other.')
        p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite = self._get_handles(stdin, stdout, stderr)
        if _mswindows:
            if p2cwrite != -1:
                p2cwrite = msvcrt.open_osfhandle(p2cwrite.Detach(), 0)
            if c2pread != -1:
                c2pread = msvcrt.open_osfhandle(c2pread.Detach(), 0)
            if errread != -1:
                errread = msvcrt.open_osfhandle(errread.Detach(), 0)
        self.text_mode = encoding or errors or text or universal_newlines
        self._sigint_wait_secs = 0.25
        self._closed_child_pipe_fds = False
        if self.text_mode:
            if bufsize == 1:
                line_buffering = True
                bufsize = -1
            else:
                line_buffering = False
        try:
            if p2cwrite != -1:
                self.stdin = io.open(p2cwrite, 'wb', bufsize)
                if self.text_mode:
                    self.stdin = io.TextIOWrapper((self.stdin), write_through=True, line_buffering=line_buffering,
                      encoding=encoding,
                      errors=errors)
            if c2pread != -1:
                self.stdout = io.open(c2pread, 'rb', bufsize)
                if self.text_mode:
                    self.stdout = io.TextIOWrapper((self.stdout), encoding=encoding,
                      errors=errors)
            if errread != -1:
                self.stderr = io.open(errread, 'rb', bufsize)
                if self.text_mode:
                    self.stderr = io.TextIOWrapper((self.stderr), encoding=encoding,
                      errors=errors)
            self._execute_child(args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, start_new_session)
        except:
            for f in filter(None, (self.stdin, self.stdout, self.stderr)):
                try:
                    f.close()
                except OSError:
                    pass

            else:
                if not self._closed_child_pipe_fds:
                    to_close = []
                    if stdin == PIPE:
                        to_close.append(p2cread)
                    if stdout == PIPE:
                        to_close.append(c2pwrite)
                    if stderr == PIPE:
                        to_close.append(errwrite)
                    if hasattr(self, '_devnull'):
                        to_close.append(self._devnull)
                    for fd in to_close:
                        try:
                            if _mswindows and isinstance(fd, Handle):
                                fd.Close()
                            else:
                                os.close(fd)
                        except OSError:
                            pass

                    else:
                        raise

    @property
    def universal_newlines(self):
        return self.text_mode

    @universal_newlines.setter
    def universal_newlines(self, universal_newlines):
        self.text_mode = bool(universal_newlines)

    def _translate_newlines(self, data, encoding, errors):
        data = data.decode(encoding, errors)
        return data.replace('\r\n', '\n').replace('\r', '\n')

    def __enter__(self):
        return self

    def __exit__--- This code section failed: ---

 L. 908         0  LOAD_FAST                'self'
                2  LOAD_ATTR                stdout
                4  POP_JUMP_IF_FALSE    16  'to 16'

 L. 909         6  LOAD_FAST                'self'
                8  LOAD_ATTR                stdout
               10  LOAD_METHOD              close
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          
             16_0  COME_FROM             4  '4'

 L. 910        16  LOAD_FAST                'self'
               18  LOAD_ATTR                stderr
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 911        22  LOAD_FAST                'self'
               24  LOAD_ATTR                stderr
               26  LOAD_METHOD              close
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          
             32_0  COME_FROM            20  '20'

 L. 912        32  LOAD_CONST               None
               34  SETUP_FINALLY        56  'to 56'

 L. 913        36  LOAD_FAST                'self'
               38  LOAD_ATTR                stdin
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 914        42  LOAD_FAST                'self'
               44  LOAD_ATTR                stdin
               46  LOAD_METHOD              close
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            40  '40'
               52  POP_BLOCK        
               54  BEGIN_FINALLY    
             56_0  COME_FROM_FINALLY    34  '34'

 L. 916        56  LOAD_FAST                'exc_type'
               58  LOAD_GLOBAL              KeyboardInterrupt
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE   128  'to 128'

 L. 924        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _sigint_wait_secs
               68  LOAD_CONST               0
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE   114  'to 114'

 L. 925        74  SETUP_FINALLY        94  'to 94'

 L. 926        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _wait
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _sigint_wait_secs
               84  LOAD_CONST               ('timeout',)
               86  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               88  POP_TOP          
               90  POP_BLOCK        
               92  JUMP_FORWARD        114  'to 114'
             94_0  COME_FROM_FINALLY    74  '74'

 L. 927        94  DUP_TOP          
               96  LOAD_GLOBAL              TimeoutExpired
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   112  'to 112'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 928       108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM           100  '100'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            92  '92'
            114_2  COME_FROM            72  '72'

 L. 929       114  LOAD_CONST               0
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _sigint_wait_secs

 L. 930       120  POP_FINALLY           0  ''
              122  POP_TOP          
              124  LOAD_CONST               None
              126  RETURN_VALUE     
            128_0  COME_FROM            62  '62'

 L. 933       128  LOAD_FAST                'self'
              130  LOAD_METHOD              wait
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          
              136  END_FINALLY      
              138  POP_TOP          

Parse error at or near `LOAD_FAST' instruction at offset 56

    def __del__(self, _maxsize=sys.maxsize, _warn=warnings.warn):
        if not self._child_created:
            return
        if self.returncode is None:
            _warn(('subprocess %s is still running' % self.pid), ResourceWarning,
              source=self)
        self._internal_poll(_deadstate=_maxsize)
        if self.returncode is None:
            if _active is not None:
                _active.append(self)

    def _get_devnull(self):
        if not hasattr(self, '_devnull'):
            self._devnull = os.open(os.devnull, os.O_RDWR)
        return self._devnull

    def _stdin_write(self, input):
        if input:
            try:
                self.stdin.write(input)
            except BrokenPipeError:
                pass
            except OSError as exc:
                try:
                    if exc.errno == errno.EINVAL:
                        pass
                    else:
                        raise
                finally:
                    exc = None
                    del exc

        try:
            self.stdin.close()
        except BrokenPipeError:
            pass
        except OSError as exc:
            try:
                if exc.errno == errno.EINVAL:
                    pass
                else:
                    raise
            finally:
                exc = None
                del exc

    def communicate(self, input=None, timeout=None):
        """Interact with process: Send data to stdin and close it.
        Read data from stdout and stderr, until end-of-file is
        reached.  Wait for process to terminate.

        The optional "input" argument should be data to be sent to the
        child process, or None, if no data should be sent to the child.
        communicate() returns a tuple (stdout, stderr).

        By default, all communication is in bytes, and therefore any
        "input" should be bytes, and the (stdout, stderr) will be bytes.
        If in text mode (indicated by self.text_mode), any "input" should
        be a string, and (stdout, stderr) will be strings decoded
        according to locale encoding, or by "encoding" if set. Text mode
        is triggered by setting any of text, encoding, errors or
        universal_newlines.
        """
        if self._communication_started:
            if input:
                raise ValueError('Cannot send input after starting communication')
        if timeout is None and (self._communication_started or [
         self.stdin, self.stdout, self.stderr].count(None)) >= 2:
            stdout = None
            stderr = None
            if self.stdin:
                self._stdin_write(input)
            elif self.stdout:
                stdout = self.stdout.read()
                self.stdout.close()
            elif self.stderr:
                stderr = self.stderr.read()
                self.stderr.close()
            self.wait()
        else:
            if timeout is not None:
                endtime = _time() + timeout
            else:
                endtime = None
            try:
                try:
                    stdout, stderr = self._communicate(input, endtime, timeout)
                except KeyboardInterrupt:
                    if timeout is not None:
                        sigint_timeout = min(self._sigint_wait_secs, self._remaining_time(endtime))
                    else:
                        sigint_timeout = self._sigint_wait_secs
                    self._sigint_wait_secs = 0
                    try:
                        self._wait(timeout=sigint_timeout)
                    except TimeoutExpired:
                        pass
                    else:
                        raise

            finally:
                self._communication_started = True

            sts = self.wait(timeout=(self._remaining_time(endtime)))
        return (
         stdout, stderr)

    def poll(self):
        """Check if child process has terminated. Set and return returncode
        attribute."""
        return self._internal_poll()

    def _remaining_time(self, endtime):
        """Convenience for _communicate when computing timeouts."""
        if endtime is None:
            return
        return endtime - _time()

    def _check_timeout(self, endtime, orig_timeout, stdout_seq, stderr_seq, skip_check_and_raise=False):
        """Convenience for checking if a timeout has expired."""
        if endtime is None:
            return
        if skip_check_and_raise or (_time() > endtime):
            raise TimeoutExpired((self.args),
              orig_timeout, output=((b'').join(stdout_seq) if stdout_seq else None),
              stderr=((b'').join(stderr_seq) if stderr_seq else None))

    def wait(self, timeout=None):
        """Wait for child process to terminate; returns self.returncode."""
        if timeout is not None:
            endtime = _time() + timeout
        try:
            return self._wait(timeout=timeout)
        except KeyboardInterrupt:
            if timeout is not None:
                sigint_timeout = min(self._sigint_wait_secs, self._remaining_time(endtime))
            else:
                sigint_timeout = self._sigint_wait_secs
            self._sigint_wait_secs = 0
            try:
                self._wait(timeout=sigint_timeout)
            except TimeoutExpired:
                pass
            else:
                raise

    def _close_pipe_fds(self, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
        devnull_fd = getattr(self, '_devnull', None)
        with contextlib.ExitStack() as stack:
            if _mswindows:
                if p2cread != -1:
                    stack.callback(p2cread.Close)
                if c2pwrite != -1:
                    stack.callback(c2pwrite.Close)
                if errwrite != -1:
                    stack.callback(errwrite.Close)
            else:
                if p2cread != -1:
                    if p2cwrite != -1:
                        if p2cread != devnull_fd:
                            stack.callback(os.close, p2cread)
                if c2pwrite != -1:
                    if c2pread != -1:
                        if c2pwrite != devnull_fd:
                            stack.callback(os.close, c2pwrite)
                if errwrite != -1:
                    if errread != -1:
                        if errwrite != devnull_fd:
                            stack.callback(os.close, errwrite)
            if devnull_fd is not None:
                stack.callback(os.close, devnull_fd)
        self._closed_child_pipe_fds = True

    if _mswindows:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            if stdin is None:
                if stdout is None:
                    if stderr is None:
                        return (-1, -1, -1, -1, -1, -1)
            p2cread, p2cwrite = (-1, -1)
            c2pread, c2pwrite = (-1, -1)
            errread, errwrite = (-1, -1)
            if stdin is None:
                p2cread = _winapi.GetStdHandle(_winapi.STD_INPUT_HANDLE)
                if p2cread is None:
                    p2cread, _ = _winapi.CreatePipe(None, 0)
                    p2cread = Handle(p2cread)
                    _winapi.CloseHandle(_)
            elif stdin == PIPE:
                p2cread, p2cwrite = _winapi.CreatePipe(None, 0)
                p2cread, p2cwrite = Handle(p2cread), Handle(p2cwrite)
            elif stdin == DEVNULL:
                p2cread = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stdin, int):
                p2cread = msvcrt.get_osfhandle(stdin)
            else:
                p2cread = msvcrt.get_osfhandle(stdin.fileno())
            p2cread = self._make_inheritable(p2cread)
            if stdout is None:
                c2pwrite = _winapi.GetStdHandle(_winapi.STD_OUTPUT_HANDLE)
                if c2pwrite is None:
                    _, c2pwrite = _winapi.CreatePipe(None, 0)
                    c2pwrite = Handle(c2pwrite)
                    _winapi.CloseHandle(_)
            elif stdout == PIPE:
                c2pread, c2pwrite = _winapi.CreatePipe(None, 0)
                c2pread, c2pwrite = Handle(c2pread), Handle(c2pwrite)
            elif stdout == DEVNULL:
                c2pwrite = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stdout, int):
                c2pwrite = msvcrt.get_osfhandle(stdout)
            else:
                c2pwrite = msvcrt.get_osfhandle(stdout.fileno())
            c2pwrite = self._make_inheritable(c2pwrite)
            if stderr is None:
                errwrite = _winapi.GetStdHandle(_winapi.STD_ERROR_HANDLE)
                if errwrite is None:
                    _, errwrite = _winapi.CreatePipe(None, 0)
                    errwrite = Handle(errwrite)
                    _winapi.CloseHandle(_)
            elif stderr == PIPE:
                errread, errwrite = _winapi.CreatePipe(None, 0)
                errread, errwrite = Handle(errread), Handle(errwrite)
            elif stderr == STDOUT:
                errwrite = c2pwrite
            elif stderr == DEVNULL:
                errwrite = msvcrt.get_osfhandle(self._get_devnull())
            elif isinstance(stderr, int):
                errwrite = msvcrt.get_osfhandle(stderr)
            else:
                errwrite = msvcrt.get_osfhandle(stderr.fileno())
            errwrite = self._make_inheritable(errwrite)
            return (
             p2cread, p2cwrite,
             c2pread, c2pwrite,
             errread, errwrite)

        def _make_inheritable(self, handle):
            """Return a duplicate of handle, which is inheritable"""
            h = _winapi.DuplicateHandle(_winapi.GetCurrentProcess(), handle, _winapi.GetCurrentProcess(), 0, 1, _winapi.DUPLICATE_SAME_ACCESS)
            return Handle(h)

        def _filter_handle_list(self, handle_list):
            """Filter out console handles that can't be used
            in lpAttributeList["handle_list"] and make sure the list
            isn't empty. This also removes duplicate handles."""
            return list({handle for handle in handle_list if handle & 3 != 3 or _winapi.GetFileType(handle) != _winapi.FILE_TYPE_CHAR if handle & 3 != 3 or _winapi.GetFileType(handle) != _winapi.FILE_TYPE_CHAR})

        def _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, unused_restore_signals, unused_start_new_session):
            """Execute program (MS Windows version)"""
            if pass_fds:
                raise AssertionError('pass_fds not supported on Windows.')
            if isinstance(args, str):
                pass
            elif isinstance(args, bytes):
                if shell:
                    raise TypeError('bytes args is not allowed on Windows')
                args = list2cmdline([args])
            elif isinstance(args, os.PathLike):
                if shell:
                    raise TypeError('path-like args is not allowed when shell is true')
                args = list2cmdline([args])
            else:
                args = list2cmdline(args)
            if executable is not None:
                executable = os.fsdecode(executable)
            if startupinfo is None:
                startupinfo = STARTUPINFO()
            else:
                startupinfo = startupinfo.copy()
            use_std_handles = -1 not in (p2cread, c2pwrite, errwrite)
            if use_std_handles:
                startupinfo.dwFlags |= _winapi.STARTF_USESTDHANDLES
                startupinfo.hStdInput = p2cread
                startupinfo.hStdOutput = c2pwrite
                startupinfo.hStdError = errwrite
            attribute_list = startupinfo.lpAttributeList
            have_handle_list = bool(attribute_list and 'handle_list' in attribute_list and attribute_list['handle_list'])
            if have_handle_list or (use_std_handles and close_fds):
                if attribute_list is None:
                    attribute_list = startupinfo.lpAttributeList = {}
                handle_list = attribute_list['handle_list'] = list(attribute_list.get('handle_list', []))
                if use_std_handles:
                    handle_list += [int(p2cread), int(c2pwrite), int(errwrite)]
                handle_list[:] = self._filter_handle_list(handle_list)
                if handle_list:
                    if not close_fds:
                        warnings.warn("startupinfo.lpAttributeList['handle_list'] overriding close_fds", RuntimeWarning)
                    close_fds = False
            if shell:
                startupinfo.dwFlags |= _winapi.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = _winapi.SW_HIDE
                comspec = os.environ.get('COMSPEC', 'cmd.exe')
                args = '{} /c "{}"'.format(comspec, args)
            if cwd is not None:
                cwd = os.fsdecode(cwd)
            sys.audit('subprocess.Popen', executable, args, cwd, env)
            try:
                hp, ht, pid, tid = _winapi.CreateProcess(executable, args, None, None, int(not close_fds), creationflags, env, cwd, startupinfo)
            finally:
                self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

            self._child_created = True
            self._handle = Handle(hp)
            self.pid = pid
            _winapi.CloseHandle(ht)

        def _internal_poll(self, _deadstate=None, _WaitForSingleObject=_winapi.WaitForSingleObject, _WAIT_OBJECT_0=_winapi.WAIT_OBJECT_0, _GetExitCodeProcess=_winapi.GetExitCodeProcess):
            """Check if child process has terminated.  Returns returncode
            attribute.

            This method is called by __del__, so it can only refer to objects
            in its local scope.

            """
            if self.returncode is None:
                if _WaitForSingleObject(self._handle, 0) == _WAIT_OBJECT_0:
                    self.returncode = _GetExitCodeProcess(self._handle)
            return self.returncode

        def _wait(self, timeout):
            """Internal implementation of wait() on Windows."""
            if timeout is None:
                timeout_millis = _winapi.INFINITE
            else:
                timeout_millis = int(timeout * 1000)
            if self.returncode is None:
                result = _winapi.WaitForSingleObject(self._handle, timeout_millis)
                if result == _winapi.WAIT_TIMEOUT:
                    raise TimeoutExpired(self.args, timeout)
                self.returncode = _winapi.GetExitCodeProcess(self._handle)
            return self.returncode

        def _readerthread(self, fh, buffer):
            buffer.append(fh.read())
            fh.close()

        def _communicate(self, input, endtime, orig_timeout):
            if self.stdout:
                if not hasattr(self, '_stdout_buff'):
                    self._stdout_buff = []
                    self.stdout_thread = threading.Thread(target=(self._readerthread), args=(
                     self.stdout, self._stdout_buff))
                    self.stdout_thread.daemon = True
                    self.stdout_thread.start()
                if self.stderr:
                    if not hasattr(self, '_stderr_buff'):
                        self._stderr_buff = []
                        self.stderr_thread = threading.Thread(target=(self._readerthread), args=(
                         self.stderr, self._stderr_buff))
                        self.stderr_thread.daemon = True
                        self.stderr_thread.start()
                    if self.stdin:
                        self._stdin_write(input)
                    if self.stdout is not None:
                        self.stdout_thread.join(self._remaining_time(endtime))
                        if self.stdout_thread.is_alive():
                            raise TimeoutExpired(self.args, orig_timeout)
                    if self.stderr is not None:
                        self.stderr_thread.join(self._remaining_time(endtime))
                        if self.stderr_thread.is_alive():
                            raise TimeoutExpired(self.args, orig_timeout)
                    stdout = None
                    stderr = None
                    if self.stdout:
                        stdout = self._stdout_buff
                        self.stdout.close()
                    if self.stderr:
                        stderr = self._stderr_buff
                        self.stderr.close()
                    if stdout is not None:
                        stdout = stdout[0]
                    if stderr is not None:
                        stderr = stderr[0]
                return (stdout, stderr)

        def send_signal(self, sig):
            """Send a signal to the process."""
            if self.returncode is not None:
                return
            if sig == signal.SIGTERM:
                self.terminate()
            elif sig == signal.CTRL_C_EVENT:
                os.kill(self.pid, signal.CTRL_C_EVENT)
            elif sig == signal.CTRL_BREAK_EVENT:
                os.kill(self.pid, signal.CTRL_BREAK_EVENT)
            else:
                raise ValueError('Unsupported signal: {}'.format(sig))

        def terminate(self):
            """Terminates the process."""
            if self.returncode is not None:
                return
            try:
                _winapi.TerminateProcess(self._handle, 1)
            except PermissionError:
                rc = _winapi.GetExitCodeProcess(self._handle)
                if rc == _winapi.STILL_ACTIVE:
                    raise
                self.returncode = rc

        kill = terminate
    else:

        def _get_handles(self, stdin, stdout, stderr):
            """Construct and return tuple with IO objects:
            p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite
            """
            p2cread, p2cwrite = (-1, -1)
            c2pread, c2pwrite = (-1, -1)
            errread, errwrite = (-1, -1)
            if stdin is None:
                pass
            elif stdin == PIPE:
                p2cread, p2cwrite = os.pipe()
            elif stdin == DEVNULL:
                p2cread = self._get_devnull()
            elif isinstance(stdin, int):
                p2cread = stdin
            else:
                p2cread = stdin.fileno()
            if stdout is None:
                pass
            elif stdout == PIPE:
                c2pread, c2pwrite = os.pipe()
            elif stdout == DEVNULL:
                c2pwrite = self._get_devnull()
            elif isinstance(stdout, int):
                c2pwrite = stdout
            else:
                c2pwrite = stdout.fileno()
            if stderr is None:
                pass
            elif stderr == PIPE:
                errread, errwrite = os.pipe()
            elif stderr == STDOUT:
                if c2pwrite != -1:
                    errwrite = c2pwrite
                else:
                    errwrite = sys.__stdout__.fileno()
            elif stderr == DEVNULL:
                errwrite = self._get_devnull()
            elif isinstance(stderr, int):
                errwrite = stderr
            else:
                errwrite = stderr.fileno()
            return (
             p2cread, p2cwrite,
             c2pread, c2pwrite,
             errread, errwrite)

        def _posix_spawn(self, args, executable, env, restore_signals, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite):
            """Execute program using os.posix_spawn()."""
            if env is None:
                env = os.environ
            kwargs = {}
            if restore_signals:
                sigset = []
                for signame in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                    signum = getattr(signal, signame, None)
                    if signum is not None:
                        sigset.append(signum)
                    kwargs['setsigdef'] = sigset

            file_actions = []
            for fd in (
             p2cwrite, c2pread, errread):
                if fd != -1:
                    file_actions.append((os.POSIX_SPAWN_CLOSE, fd))
            else:
                for fd, fd2 in (
                 (
                  p2cread, 0),
                 (
                  c2pwrite, 1),
                 (
                  errwrite, 2)):
                    if fd != -1:
                        file_actions.append((os.POSIX_SPAWN_DUP2, fd, fd2))
                else:
                    if file_actions:
                        kwargs['file_actions'] = file_actions
                    self.pid = (os.posix_spawn)(executable, args, env, **kwargs)
                    self._child_created = True
                    self._close_pipe_fds(p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite)

        def _execute_child--- This code section failed: ---

 L.1559         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'args'
                4  LOAD_GLOBAL              str
                6  LOAD_GLOBAL              bytes
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L.1560        14  LOAD_FAST                'args'
               16  BUILD_LIST_1          1 
               18  STORE_FAST               'args'
               20  JUMP_FORWARD         62  'to 62'
             22_0  COME_FROM            12  '12'

 L.1561        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'args'
               26  LOAD_GLOBAL              os
               28  LOAD_ATTR                PathLike
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L.1562        34  LOAD_FAST                'shell'
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L.1563        38  LOAD_GLOBAL              TypeError
               40  LOAD_STR                 'path-like args is not allowed when shell is true'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L.1565        46  LOAD_FAST                'args'
               48  BUILD_LIST_1          1 
               50  STORE_FAST               'args'
               52  JUMP_FORWARD         62  'to 62'
             54_0  COME_FROM            32  '32'

 L.1567        54  LOAD_GLOBAL              list
               56  LOAD_FAST                'args'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'args'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            20  '20'

 L.1569        62  LOAD_FAST                'shell'
               64  POP_JUMP_IF_FALSE   108  'to 108'

 L.1572        66  LOAD_GLOBAL              hasattr
               68  LOAD_GLOBAL              sys
               70  LOAD_STR                 'getandroidapilevel'
               72  CALL_FUNCTION_2       2  ''

 L.1571        74  POP_JUMP_IF_FALSE    80  'to 80'
               76  LOAD_STR                 '/system/bin/sh'
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            74  '74'

 L.1572        80  LOAD_STR                 '/bin/sh'
             82_0  COME_FROM            78  '78'

 L.1571        82  STORE_FAST               'unix_shell'

 L.1573        84  LOAD_FAST                'unix_shell'
               86  LOAD_STR                 '-c'
               88  BUILD_LIST_2          2 
               90  LOAD_FAST                'args'
               92  BINARY_ADD       
               94  STORE_FAST               'args'

 L.1574        96  LOAD_DEREF               'executable'
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L.1575       100  LOAD_DEREF               'executable'
              102  LOAD_FAST                'args'
              104  LOAD_CONST               0
              106  STORE_SUBSCR     
            108_0  COME_FROM            98  '98'
            108_1  COME_FROM            64  '64'

 L.1577       108  LOAD_DEREF               'executable'
              110  LOAD_CONST               None
              112  COMPARE_OP               is
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.1578       116  LOAD_FAST                'args'
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  STORE_DEREF              'executable'
            124_0  COME_FROM           114  '114'

 L.1580       124  LOAD_GLOBAL              sys
              126  LOAD_METHOD              audit
              128  LOAD_STR                 'subprocess.Popen'
              130  LOAD_DEREF               'executable'
              132  LOAD_FAST                'args'
              134  LOAD_FAST                'cwd'
              136  LOAD_FAST                'env'
              138  CALL_METHOD_5         5  ''
              140  POP_TOP          

 L.1582       142  LOAD_GLOBAL              _USE_POSIX_SPAWN
          144_146  POP_JUMP_IF_FALSE   286  'to 286'

 L.1583       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              dirname
              154  LOAD_DEREF               'executable'
              156  CALL_METHOD_1         1  ''

 L.1582   158_160  POP_JUMP_IF_FALSE   286  'to 286'

 L.1584       162  LOAD_FAST                'preexec_fn'
              164  LOAD_CONST               None
              166  COMPARE_OP               is

 L.1582   168_170  POP_JUMP_IF_FALSE   286  'to 286'

 L.1585       172  LOAD_FAST                'close_fds'

 L.1582   174_176  POP_JUMP_IF_TRUE    286  'to 286'

 L.1586       178  LOAD_FAST                'pass_fds'

 L.1582   180_182  POP_JUMP_IF_TRUE    286  'to 286'

 L.1587       184  LOAD_FAST                'cwd'
              186  LOAD_CONST               None
              188  COMPARE_OP               is

 L.1582   190_192  POP_JUMP_IF_FALSE   286  'to 286'

 L.1588       194  LOAD_FAST                'p2cread'
              196  LOAD_CONST               -1
              198  COMPARE_OP               ==

 L.1582       200  POP_JUMP_IF_TRUE    212  'to 212'

 L.1588       202  LOAD_FAST                'p2cread'
              204  LOAD_CONST               2
              206  COMPARE_OP               >

 L.1582   208_210  POP_JUMP_IF_FALSE   286  'to 286'
            212_0  COME_FROM           200  '200'

 L.1589       212  LOAD_FAST                'c2pwrite'
              214  LOAD_CONST               -1
              216  COMPARE_OP               ==

 L.1582       218  POP_JUMP_IF_TRUE    230  'to 230'

 L.1589       220  LOAD_FAST                'c2pwrite'
              222  LOAD_CONST               2
              224  COMPARE_OP               >

 L.1582   226_228  POP_JUMP_IF_FALSE   286  'to 286'
            230_0  COME_FROM           218  '218'

 L.1590       230  LOAD_FAST                'errwrite'
              232  LOAD_CONST               -1
              234  COMPARE_OP               ==

 L.1582       236  POP_JUMP_IF_TRUE    248  'to 248'

 L.1590       238  LOAD_FAST                'errwrite'
              240  LOAD_CONST               2
              242  COMPARE_OP               >

 L.1582   244_246  POP_JUMP_IF_FALSE   286  'to 286'
            248_0  COME_FROM           236  '236'

 L.1591       248  LOAD_FAST                'start_new_session'

 L.1582   250_252  POP_JUMP_IF_TRUE    286  'to 286'

 L.1592       254  LOAD_FAST                'self'
              256  LOAD_METHOD              _posix_spawn
              258  LOAD_FAST                'args'
              260  LOAD_DEREF               'executable'
              262  LOAD_FAST                'env'
              264  LOAD_FAST                'restore_signals'

 L.1593       266  LOAD_FAST                'p2cread'

 L.1593       268  LOAD_FAST                'p2cwrite'

 L.1594       270  LOAD_FAST                'c2pread'

 L.1594       272  LOAD_FAST                'c2pwrite'

 L.1595       274  LOAD_FAST                'errread'

 L.1595       276  LOAD_FAST                'errwrite'

 L.1592       278  CALL_METHOD_10       10  ''
              280  POP_TOP          

 L.1596       282  LOAD_CONST               None
              284  RETURN_VALUE     
            286_0  COME_FROM           250  '250'
            286_1  COME_FROM           244  '244'
            286_2  COME_FROM           226  '226'
            286_3  COME_FROM           208  '208'
            286_4  COME_FROM           190  '190'
            286_5  COME_FROM           180  '180'
            286_6  COME_FROM           174  '174'
            286_7  COME_FROM           168  '168'
            286_8  COME_FROM           158  '158'
            286_9  COME_FROM           144  '144'

 L.1598       286  LOAD_DEREF               'executable'
              288  STORE_FAST               'orig_executable'

 L.1603       290  LOAD_GLOBAL              os
              292  LOAD_METHOD              pipe
              294  CALL_METHOD_0         0  ''
              296  UNPACK_SEQUENCE_2     2 
              298  STORE_FAST               'errpipe_read'
              300  STORE_FAST               'errpipe_write'

 L.1605       302  BUILD_LIST_0          0 
              304  STORE_FAST               'low_fds_to_close'
            306_0  COME_FROM           336  '336'

 L.1606       306  LOAD_FAST                'errpipe_write'
              308  LOAD_CONST               3
              310  COMPARE_OP               <
          312_314  POP_JUMP_IF_FALSE   340  'to 340'

 L.1607       316  LOAD_FAST                'low_fds_to_close'
              318  LOAD_METHOD              append
              320  LOAD_FAST                'errpipe_write'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L.1608       326  LOAD_GLOBAL              os
              328  LOAD_METHOD              dup
              330  LOAD_FAST                'errpipe_write'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'errpipe_write'
          336_338  JUMP_BACK           306  'to 306'
            340_0  COME_FROM           312  '312'

 L.1609       340  LOAD_FAST                'low_fds_to_close'
              342  GET_ITER         
            344_0  COME_FROM           358  '358'
              344  FOR_ITER            362  'to 362'
              346  STORE_FAST               'low_fd'

 L.1610       348  LOAD_GLOBAL              os
              350  LOAD_METHOD              close
              352  LOAD_FAST                'low_fd'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
          358_360  JUMP_BACK           344  'to 344'
            362_0  COME_FROM           344  '344'

 L.1611   362_364  SETUP_FINALLY       696  'to 696'

 L.1612       366  SETUP_FINALLY       606  'to 606'

 L.1618       368  LOAD_FAST                'env'
              370  LOAD_CONST               None
              372  COMPARE_OP               is-not
          374_376  POP_JUMP_IF_FALSE   456  'to 456'

 L.1619       378  BUILD_LIST_0          0 
              380  STORE_FAST               'env_list'

 L.1620       382  LOAD_FAST                'env'
              384  LOAD_METHOD              items
              386  CALL_METHOD_0         0  ''
              388  GET_ITER         
            390_0  COME_FROM           450  '450'
              390  FOR_ITER            454  'to 454'
              392  UNPACK_SEQUENCE_2     2 
              394  STORE_FAST               'k'
              396  STORE_FAST               'v'

 L.1621       398  LOAD_GLOBAL              os
              400  LOAD_METHOD              fsencode
              402  LOAD_FAST                'k'
              404  CALL_METHOD_1         1  ''
              406  STORE_FAST               'k'

 L.1622       408  LOAD_CONST               b'='
              410  LOAD_FAST                'k'
              412  COMPARE_OP               in
          414_416  POP_JUMP_IF_FALSE   426  'to 426'

 L.1623       418  LOAD_GLOBAL              ValueError
              420  LOAD_STR                 'illegal environment variable name'
              422  CALL_FUNCTION_1       1  ''
              424  RAISE_VARARGS_1       1  'exception instance'
            426_0  COME_FROM           414  '414'

 L.1624       426  LOAD_FAST                'env_list'
              428  LOAD_METHOD              append
              430  LOAD_FAST                'k'
              432  LOAD_CONST               b'='
              434  BINARY_ADD       
              436  LOAD_GLOBAL              os
              438  LOAD_METHOD              fsencode
              440  LOAD_FAST                'v'
              442  CALL_METHOD_1         1  ''
              444  BINARY_ADD       
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          
          450_452  JUMP_BACK           390  'to 390'
            454_0  COME_FROM           390  '390'
              454  JUMP_FORWARD        460  'to 460'
            456_0  COME_FROM           374  '374'

 L.1626       456  LOAD_CONST               None
              458  STORE_FAST               'env_list'
            460_0  COME_FROM           454  '454'

 L.1627       460  LOAD_GLOBAL              os
              462  LOAD_METHOD              fsencode
              464  LOAD_DEREF               'executable'
              466  CALL_METHOD_1         1  ''
              468  STORE_DEREF              'executable'

 L.1628       470  LOAD_GLOBAL              os
              472  LOAD_ATTR                path
              474  LOAD_METHOD              dirname
              476  LOAD_DEREF               'executable'
              478  CALL_METHOD_1         1  ''
          480_482  POP_JUMP_IF_FALSE   492  'to 492'

 L.1629       484  LOAD_DEREF               'executable'
              486  BUILD_TUPLE_1         1 
              488  STORE_FAST               'executable_list'
              490  JUMP_FORWARD        520  'to 520'
            492_0  COME_FROM           480  '480'

 L.1632       492  LOAD_GLOBAL              tuple
              494  LOAD_CLOSURE             'executable'
              496  BUILD_TUPLE_1         1 
              498  LOAD_GENEXPR             '<code_object <genexpr>>'
              500  LOAD_STR                 'Popen._execute_child.<locals>.<genexpr>'
              502  MAKE_FUNCTION_8          'closure'

 L.1634       504  LOAD_GLOBAL              os
              506  LOAD_METHOD              get_exec_path
              508  LOAD_FAST                'env'
              510  CALL_METHOD_1         1  ''

 L.1632       512  GET_ITER         
              514  CALL_FUNCTION_1       1  ''
              516  CALL_FUNCTION_1       1  ''
              518  STORE_FAST               'executable_list'
            520_0  COME_FROM           490  '490'

 L.1635       520  LOAD_GLOBAL              set
              522  LOAD_FAST                'pass_fds'
              524  CALL_FUNCTION_1       1  ''
              526  STORE_FAST               'fds_to_keep'

 L.1636       528  LOAD_FAST                'fds_to_keep'
              530  LOAD_METHOD              add
              532  LOAD_FAST                'errpipe_write'
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          

 L.1637       538  LOAD_GLOBAL              _posixsubprocess
              540  LOAD_METHOD              fork_exec

 L.1638       542  LOAD_FAST                'args'

 L.1638       544  LOAD_FAST                'executable_list'

 L.1639       546  LOAD_FAST                'close_fds'

 L.1639       548  LOAD_GLOBAL              tuple
              550  LOAD_GLOBAL              sorted
              552  LOAD_GLOBAL              map
              554  LOAD_GLOBAL              int
              556  LOAD_FAST                'fds_to_keep'
              558  CALL_FUNCTION_2       2  ''
              560  CALL_FUNCTION_1       1  ''
              562  CALL_FUNCTION_1       1  ''

 L.1640       564  LOAD_FAST                'cwd'

 L.1640       566  LOAD_FAST                'env_list'

 L.1641       568  LOAD_FAST                'p2cread'

 L.1641       570  LOAD_FAST                'p2cwrite'

 L.1641       572  LOAD_FAST                'c2pread'

 L.1641       574  LOAD_FAST                'c2pwrite'

 L.1642       576  LOAD_FAST                'errread'

 L.1642       578  LOAD_FAST                'errwrite'

 L.1643       580  LOAD_FAST                'errpipe_read'

 L.1643       582  LOAD_FAST                'errpipe_write'

 L.1644       584  LOAD_FAST                'restore_signals'

 L.1644       586  LOAD_FAST                'start_new_session'

 L.1644       588  LOAD_FAST                'preexec_fn'

 L.1637       590  CALL_METHOD_17       17  ''
              592  LOAD_FAST                'self'
              594  STORE_ATTR               pid

 L.1645       596  LOAD_CONST               True
              598  LOAD_FAST                'self'
              600  STORE_ATTR               _child_created
              602  POP_BLOCK        
              604  BEGIN_FINALLY    
            606_0  COME_FROM_FINALLY   366  '366'

 L.1648       606  LOAD_GLOBAL              os
              608  LOAD_METHOD              close
              610  LOAD_FAST                'errpipe_write'
              612  CALL_METHOD_1         1  ''
              614  POP_TOP          
              616  END_FINALLY      

 L.1650       618  LOAD_FAST                'self'
              620  LOAD_METHOD              _close_pipe_fds
              622  LOAD_FAST                'p2cread'
              624  LOAD_FAST                'p2cwrite'

 L.1651       626  LOAD_FAST                'c2pread'

 L.1651       628  LOAD_FAST                'c2pwrite'

 L.1652       630  LOAD_FAST                'errread'

 L.1652       632  LOAD_FAST                'errwrite'

 L.1650       634  CALL_METHOD_6         6  ''
              636  POP_TOP          

 L.1656       638  LOAD_GLOBAL              bytearray
              640  CALL_FUNCTION_0       0  ''
              642  STORE_FAST               'errpipe_data'
            644_0  COME_FROM           688  '688'
            644_1  COME_FROM           680  '680'

 L.1658       644  LOAD_GLOBAL              os
              646  LOAD_METHOD              read
              648  LOAD_FAST                'errpipe_read'
              650  LOAD_CONST               50000
              652  CALL_METHOD_2         2  ''
              654  STORE_FAST               'part'

 L.1659       656  LOAD_FAST                'errpipe_data'
              658  LOAD_FAST                'part'
              660  INPLACE_ADD      
              662  STORE_FAST               'errpipe_data'

 L.1660       664  LOAD_FAST                'part'
          666_668  POP_JUMP_IF_FALSE   692  'to 692'
              670  LOAD_GLOBAL              len
              672  LOAD_FAST                'errpipe_data'
              674  CALL_FUNCTION_1       1  ''
              676  LOAD_CONST               50000
              678  COMPARE_OP               >
          680_682  POP_JUMP_IF_FALSE_BACK   644  'to 644'

 L.1661   684_686  JUMP_FORWARD        692  'to 692'
          688_690  JUMP_BACK           644  'to 644'
            692_0  COME_FROM           684  '684'
            692_1  COME_FROM           666  '666'
              692  POP_BLOCK        
              694  BEGIN_FINALLY    
            696_0  COME_FROM_FINALLY   362  '362'

 L.1664       696  LOAD_GLOBAL              os
              698  LOAD_METHOD              close
              700  LOAD_FAST                'errpipe_read'
              702  CALL_METHOD_1         1  ''
              704  POP_TOP          
              706  END_FINALLY      

 L.1666       708  LOAD_FAST                'errpipe_data'
          710_712  POP_JUMP_IF_FALSE   982  'to 982'

 L.1667       714  SETUP_FINALLY       770  'to 770'

 L.1668       716  LOAD_GLOBAL              os
              718  LOAD_METHOD              waitpid
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                pid
              724  LOAD_CONST               0
              726  CALL_METHOD_2         2  ''
              728  UNPACK_SEQUENCE_2     2 
              730  STORE_FAST               'pid'
              732  STORE_FAST               'sts'

 L.1669       734  LOAD_FAST                'pid'
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                pid
              740  COMPARE_OP               ==
          742_744  POP_JUMP_IF_FALSE   758  'to 758'

 L.1670       746  LOAD_FAST                'self'
              748  LOAD_METHOD              _handle_exitstatus
              750  LOAD_FAST                'sts'
              752  CALL_METHOD_1         1  ''
              754  POP_TOP          
              756  JUMP_FORWARD        766  'to 766'
            758_0  COME_FROM           742  '742'

 L.1672       758  LOAD_GLOBAL              sys
              760  LOAD_ATTR                maxsize
              762  LOAD_FAST                'self'
              764  STORE_ATTR               returncode
            766_0  COME_FROM           756  '756'
              766  POP_BLOCK        
              768  JUMP_FORWARD        792  'to 792'
            770_0  COME_FROM_FINALLY   714  '714'

 L.1673       770  DUP_TOP          
              772  LOAD_GLOBAL              ChildProcessError
              774  COMPARE_OP               exception-match
          776_778  POP_JUMP_IF_FALSE   790  'to 790'
              780  POP_TOP          
              782  POP_TOP          
              784  POP_TOP          

 L.1674       786  POP_EXCEPT       
              788  BREAK_LOOP          792  'to 792'
            790_0  COME_FROM           776  '776'
              790  END_FINALLY      
            792_0  COME_FROM           788  '788'
            792_1  COME_FROM           768  '768'

 L.1676       792  SETUP_FINALLY       824  'to 824'

 L.1678       794  LOAD_FAST                'errpipe_data'
              796  LOAD_METHOD              split
              798  LOAD_CONST               b':'
              800  LOAD_CONST               2
              802  CALL_METHOD_2         2  ''

 L.1677       804  UNPACK_SEQUENCE_3     3 
              806  STORE_FAST               'exception_name'
              808  STORE_FAST               'hex_errno'
              810  STORE_FAST               'err_msg'

 L.1682       812  LOAD_FAST                'err_msg'
              814  LOAD_METHOD              decode
              816  CALL_METHOD_0         0  ''
              818  STORE_FAST               'err_msg'
              820  POP_BLOCK        
              822  JUMP_FORWARD        868  'to 868'
            824_0  COME_FROM_FINALLY   792  '792'

 L.1683       824  DUP_TOP          
              826  LOAD_GLOBAL              ValueError
              828  COMPARE_OP               exception-match
          830_832  POP_JUMP_IF_FALSE   866  'to 866'
              834  POP_TOP          
              836  POP_TOP          
              838  POP_TOP          

 L.1684       840  LOAD_CONST               b'SubprocessError'
              842  STORE_FAST               'exception_name'

 L.1685       844  LOAD_CONST               b'0'
              846  STORE_FAST               'hex_errno'

 L.1686       848  LOAD_STR                 'Bad exception data from child: {!r}'
              850  LOAD_METHOD              format

 L.1687       852  LOAD_GLOBAL              bytes
              854  LOAD_FAST                'errpipe_data'
              856  CALL_FUNCTION_1       1  ''

 L.1686       858  CALL_METHOD_1         1  ''
              860  STORE_FAST               'err_msg'
              862  POP_EXCEPT       
              864  JUMP_FORWARD        868  'to 868'
            866_0  COME_FROM           830  '830'
              866  END_FINALLY      
            868_0  COME_FROM           864  '864'
            868_1  COME_FROM           822  '822'

 L.1688       868  LOAD_GLOBAL              getattr

 L.1689       870  LOAD_GLOBAL              builtins

 L.1689       872  LOAD_FAST                'exception_name'
              874  LOAD_METHOD              decode
              876  LOAD_STR                 'ascii'
              878  CALL_METHOD_1         1  ''

 L.1690       880  LOAD_GLOBAL              SubprocessError

 L.1688       882  CALL_FUNCTION_3       3  ''
              884  STORE_FAST               'child_exception_type'

 L.1691       886  LOAD_GLOBAL              issubclass
              888  LOAD_FAST                'child_exception_type'
              890  LOAD_GLOBAL              OSError
              892  CALL_FUNCTION_2       2  ''
          894_896  POP_JUMP_IF_FALSE   974  'to 974'
              898  LOAD_FAST                'hex_errno'
          900_902  POP_JUMP_IF_FALSE   974  'to 974'

 L.1692       904  LOAD_GLOBAL              int
              906  LOAD_FAST                'hex_errno'
              908  LOAD_CONST               16
              910  CALL_FUNCTION_2       2  ''
              912  STORE_FAST               'errno_num'

 L.1693       914  LOAD_FAST                'err_msg'
              916  LOAD_STR                 'noexec'
              918  COMPARE_OP               ==
              920  STORE_FAST               'child_exec_never_called'

 L.1694       922  LOAD_FAST                'child_exec_never_called'
          924_926  POP_JUMP_IF_FALSE   938  'to 938'

 L.1695       928  LOAD_STR                 ''
              930  STORE_FAST               'err_msg'

 L.1697       932  LOAD_FAST                'cwd'
              934  STORE_FAST               'err_filename'
              936  JUMP_FORWARD        942  'to 942'
            938_0  COME_FROM           924  '924'

 L.1699       938  LOAD_FAST                'orig_executable'
              940  STORE_FAST               'err_filename'
            942_0  COME_FROM           936  '936'

 L.1700       942  LOAD_FAST                'errno_num'
              944  LOAD_CONST               0
              946  COMPARE_OP               !=
          948_950  POP_JUMP_IF_FALSE   962  'to 962'

 L.1701       952  LOAD_GLOBAL              os
              954  LOAD_METHOD              strerror
              956  LOAD_FAST                'errno_num'
              958  CALL_METHOD_1         1  ''
              960  STORE_FAST               'err_msg'
            962_0  COME_FROM           948  '948'

 L.1702       962  LOAD_FAST                'child_exception_type'
              964  LOAD_FAST                'errno_num'
              966  LOAD_FAST                'err_msg'
              968  LOAD_FAST                'err_filename'
              970  CALL_FUNCTION_3       3  ''
              972  RAISE_VARARGS_1       1  'exception instance'
            974_0  COME_FROM           900  '900'
            974_1  COME_FROM           894  '894'

 L.1703       974  LOAD_FAST                'child_exception_type'
              976  LOAD_FAST                'err_msg'
              978  CALL_FUNCTION_1       1  ''
              980  RAISE_VARARGS_1       1  'exception instance'
            982_0  COME_FROM           710  '710'

Parse error at or near `JUMP_BACK' instruction at offset 688_690

        def _handle_exitstatus(self, sts, _WIFSIGNALED=os.WIFSIGNALED, _WTERMSIG=os.WTERMSIG, _WIFEXITED=os.WIFEXITED, _WEXITSTATUS=os.WEXITSTATUS, _WIFSTOPPED=os.WIFSTOPPED, _WSTOPSIG=os.WSTOPSIG):
            """All callers to this function MUST hold self._waitpid_lock."""
            if _WIFSIGNALED(sts):
                self.returncode = -_WTERMSIG(sts)
            elif _WIFEXITED(sts):
                self.returncode = _WEXITSTATUS(sts)
            elif _WIFSTOPPED(sts):
                self.returncode = -_WSTOPSIG(sts)
            else:
                raise SubprocessError('Unknown child exit status!')

        def _internal_poll--- This code section failed: ---

 L.1733         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE   174  'to 174'

 L.1734        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _waitpid_lock
               14  LOAD_METHOD              acquire
               16  LOAD_CONST               False
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L.1737        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L.1738        26  SETUP_FINALLY       162  'to 162'
               28  SETUP_FINALLY        92  'to 92'

 L.1739        30  LOAD_FAST                'self'
               32  LOAD_ATTR                returncode
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L.1740        40  LOAD_FAST                'self'
               42  LOAD_ATTR                returncode
               44  POP_BLOCK        
               46  POP_BLOCK        
               48  CALL_FINALLY        162  'to 162'
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'

 L.1741        52  LOAD_FAST                '_waitpid'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                pid
               58  LOAD_FAST                '_WNOHANG'
               60  CALL_FUNCTION_2       2  ''
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'pid'
               66  STORE_FAST               'sts'

 L.1742        68  LOAD_FAST                'pid'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                pid
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L.1743        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _handle_exitstatus
               82  LOAD_FAST                'sts'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            76  '76'
               88  POP_BLOCK        
               90  JUMP_FORWARD        158  'to 158'
             92_0  COME_FROM_FINALLY    28  '28'

 L.1744        92  DUP_TOP          
               94  LOAD_GLOBAL              OSError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   156  'to 156'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       144  'to 144'

 L.1745       108  LOAD_FAST                '_deadstate'
              110  LOAD_CONST               None
              112  COMPARE_OP               is-not
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.1746       116  LOAD_FAST                '_deadstate'
              118  LOAD_FAST                'self'
              120  STORE_ATTR               returncode
              122  JUMP_FORWARD        140  'to 140'
            124_0  COME_FROM           114  '114'

 L.1747       124  LOAD_FAST                'e'
              126  LOAD_ATTR                errno
              128  LOAD_FAST                '_ECHILD'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   140  'to 140'

 L.1753       134  LOAD_CONST               0
              136  LOAD_FAST                'self'
              138  STORE_ATTR               returncode
            140_0  COME_FROM           132  '132'
            140_1  COME_FROM           122  '122'
              140  POP_BLOCK        
              142  BEGIN_FINALLY    
            144_0  COME_FROM_FINALLY   106  '106'
              144  LOAD_CONST               None
              146  STORE_FAST               'e'
              148  DELETE_FAST              'e'
              150  END_FINALLY      
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM            98  '98'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM            90  '90'
              158  POP_BLOCK        
              160  BEGIN_FINALLY    
            162_0  COME_FROM            48  '48'
            162_1  COME_FROM_FINALLY    26  '26'

 L.1755       162  LOAD_FAST                'self'
              164  LOAD_ATTR                _waitpid_lock
              166  LOAD_METHOD              release
              168  CALL_METHOD_0         0  ''
              170  POP_TOP          
              172  END_FINALLY      
            174_0  COME_FROM             8  '8'

 L.1756       174  LOAD_FAST                'self'
              176  LOAD_ATTR                returncode
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 46

        def _try_wait(self, wait_flags):
            """All callers to this function MUST hold self._waitpid_lock."""
            try:
                pid, sts = os.waitpid(self.pid, wait_flags)
            except ChildProcessError:
                pid = self.pid
                sts = 0
            else:
                return (
                 pid, sts)

        def _wait--- This code section failed: ---

 L.1774         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L.1775        10  LOAD_FAST                'self'
               12  LOAD_ATTR                returncode
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L.1777        16  LOAD_FAST                'timeout'
               18  LOAD_CONST               None
               20  COMPARE_OP               is-not
               22  POP_JUMP_IF_FALSE   208  'to 208'

 L.1778        24  LOAD_GLOBAL              _time
               26  CALL_FUNCTION_0       0  ''
               28  LOAD_FAST                'timeout'
               30  BINARY_ADD       
               32  STORE_FAST               'endtime'

 L.1781        34  LOAD_CONST               0.0005
               36  STORE_FAST               'delay'
             38_0  COME_FROM           204  '204'

 L.1783        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _waitpid_lock
               42  LOAD_METHOD              acquire
               44  LOAD_CONST               False
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE   148  'to 148'

 L.1784        50  SETUP_FINALLY       136  'to 136'

 L.1785        52  LOAD_FAST                'self'
               54  LOAD_ATTR                returncode
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_FALSE    68  'to 68'

 L.1786        62  POP_BLOCK        
               64  CALL_FINALLY        136  'to 136'
               66  JUMP_FORWARD        206  'to 206'
             68_0  COME_FROM            60  '60'

 L.1787        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _try_wait
               72  LOAD_GLOBAL              os
               74  LOAD_ATTR                WNOHANG
               76  CALL_METHOD_1         1  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'pid'
               82  STORE_FAST               'sts'

 L.1788        84  LOAD_FAST                'pid'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                pid
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    106  'to 106'
               94  LOAD_FAST                'pid'
               96  LOAD_CONST               0
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    106  'to 106'
              102  LOAD_ASSERT              AssertionError
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM           100  '100'
            106_1  COME_FROM            92  '92'

 L.1789       106  LOAD_FAST                'pid'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                pid
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L.1790       116  LOAD_FAST                'self'
              118  LOAD_METHOD              _handle_exitstatus
              120  LOAD_FAST                'sts'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.1791       126  POP_BLOCK        
              128  CALL_FINALLY        136  'to 136'
              130  JUMP_FORWARD        206  'to 206'
            132_0  COME_FROM           114  '114'
              132  POP_BLOCK        
              134  BEGIN_FINALLY    
            136_0  COME_FROM           128  '128'
            136_1  COME_FROM            64  '64'
            136_2  COME_FROM_FINALLY    50  '50'

 L.1793       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _waitpid_lock
              140  LOAD_METHOD              release
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          
              146  END_FINALLY      
            148_0  COME_FROM            48  '48'

 L.1794       148  LOAD_FAST                'self'
              150  LOAD_METHOD              _remaining_time
              152  LOAD_FAST                'endtime'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'remaining'

 L.1795       158  LOAD_FAST                'remaining'
              160  LOAD_CONST               0
              162  COMPARE_OP               <=
              164  POP_JUMP_IF_FALSE   178  'to 178'

 L.1796       166  LOAD_GLOBAL              TimeoutExpired
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                args
              172  LOAD_FAST                'timeout'
              174  CALL_FUNCTION_2       2  ''
              176  RAISE_VARARGS_1       1  'exception instance'
            178_0  COME_FROM           164  '164'

 L.1797       178  LOAD_GLOBAL              min
              180  LOAD_FAST                'delay'
              182  LOAD_CONST               2
              184  BINARY_MULTIPLY  
              186  LOAD_FAST                'remaining'
              188  LOAD_CONST               0.05
              190  CALL_FUNCTION_3       3  ''
              192  STORE_FAST               'delay'

 L.1798       194  LOAD_GLOBAL              time
              196  LOAD_METHOD              sleep
              198  LOAD_FAST                'delay'
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  JUMP_BACK            38  'to 38'
            206_0  COME_FROM           130  '130'
            206_1  COME_FROM            66  '66'
              206  JUMP_FORWARD        300  'to 300'
            208_0  COME_FROM           298  '298'
            208_1  COME_FROM            22  '22'

 L.1800       208  LOAD_FAST                'self'
              210  LOAD_ATTR                returncode
              212  LOAD_CONST               None
              214  COMPARE_OP               is
          216_218  POP_JUMP_IF_FALSE   300  'to 300'

 L.1801       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _waitpid_lock
              224  SETUP_WITH          292  'to 292'
              226  POP_TOP          

 L.1802       228  LOAD_FAST                'self'
              230  LOAD_ATTR                returncode
              232  LOAD_CONST               None
              234  COMPARE_OP               is-not
              236  POP_JUMP_IF_FALSE   252  'to 252'

 L.1803       238  POP_BLOCK        
              240  BEGIN_FINALLY    
              242  WITH_CLEANUP_START
              244  WITH_CLEANUP_FINISH
              246  POP_FINALLY           0  ''
          248_250  JUMP_FORWARD        300  'to 300'
            252_0  COME_FROM           236  '236'

 L.1804       252  LOAD_FAST                'self'
              254  LOAD_METHOD              _try_wait
              256  LOAD_CONST               0
              258  CALL_METHOD_1         1  ''
              260  UNPACK_SEQUENCE_2     2 
              262  STORE_FAST               'pid'
              264  STORE_FAST               'sts'

 L.1808       266  LOAD_FAST                'pid'
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                pid
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   288  'to 288'

 L.1809       278  LOAD_FAST                'self'
              280  LOAD_METHOD              _handle_exitstatus
              282  LOAD_FAST                'sts'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
            288_0  COME_FROM           274  '274'
              288  POP_BLOCK        
              290  BEGIN_FINALLY    
            292_0  COME_FROM_WITH      224  '224'
              292  WITH_CLEANUP_START
              294  WITH_CLEANUP_FINISH
              296  END_FINALLY      
              298  JUMP_BACK           208  'to 208'
            300_0  COME_FROM           248  '248'
            300_1  COME_FROM           216  '216'
            300_2  COME_FROM           206  '206'

 L.1810       300  LOAD_FAST                'self'
              302  LOAD_ATTR                returncode
              304  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 64

        def _communicate(self, input, endtime, orig_timeout):
            if self.stdin and not self._communication_started:
                try:
                    self.stdin.flush()
                except BrokenPipeError:
                    pass
                else:
                    if not input:
                        try:
                            self.stdin.close()
                        except BrokenPipeError:
                            pass

                    stdout = None
                    stderr = None
                    if not self._communication_started:
                        self._fileobj2output = {}
                        if self.stdout:
                            self._fileobj2output[self.stdout] = []
                        if self.stderr:
                            self._fileobj2output[self.stderr] = []
                    if self.stdout:
                        stdout = self._fileobj2output[self.stdout]
                    if self.stderr:
                        stderr = self._fileobj2output[self.stderr]
                    self._save_input(input)
                    if self._input:
                        input_view = memoryview(self._input)
                    with _PopenSelector() as selector:
                        if self.stdin:
                            if input:
                                selector.register(self.stdin, selectors.EVENT_WRITE)
                        if self.stdout:
                            if not self.stdout.closed:
                                selector.register(self.stdout, selectors.EVENT_READ)
                            if self.stderr:
                                if not self.stderr.closed:
                                    selector.register(self.stderr, selectors.EVENT_READ)
                            while selector.get_map():
                                timeout = self._remaining_time(endtime)
                                if timeout is not None:
                                    if timeout < 0:
                                        self._check_timeout(endtime, orig_timeout, stdout,
                                          stderr, skip_check_and_raise=True)
                                        raise RuntimeError('_check_timeout(..., skip_check_and_raise=True) failed to raise TimeoutExpired.')
                                ready = selector.select(timeout)
                                self._check_timeout(endtime, orig_timeout, stdout, stderr)
                                for key, events in ready:
                                    if key.fileobj is self.stdin:
                                        chunk = input_view[self._input_offset:self._input_offset + _PIPE_BUF]
                                        try:
                                            self._input_offset += os.write(key.fd, chunk)
                                        except BrokenPipeError:
                                            selector.unregister(key.fileobj)
                                            key.fileobj.close()
                                        else:
                                            if self._input_offset >= len(self._input):
                                                selector.unregister(key.fileobj)
                                                key.fileobj.close()
                                    else:
                                        if key.fileobj in (self.stdout, self.stderr):
                                            data = os.read(key.fd, 32768)
                                            if not data:
                                                selector.unregister(key.fileobj)
                                                key.fileobj.close()
                                            self._fileobj2output[key.fileobj].append(data)

                    self.wait(timeout=(self._remaining_time(endtime)))
                    if stdout is not None:
                        stdout = (b'').join(stdout)
                    if stderr is not None:
                        stderr = (b'').join(stderr)
                    if self.text_mode:
                        if stdout is not None:
                            stdout = self._translate_newlines(stdout, self.stdout.encoding, self.stdout.errors)
                        if stderr is not None:
                            stderr = self._translate_newlines(stderr, self.stderr.encoding, self.stderr.errors)
                return (
                 stdout, stderr)

        def _save_input(self, input):
            if self.stdin:
                if self._input is None:
                    self._input_offset = 0
                    self._input = input
                    if input is not None:
                        if self.text_mode:
                            self._input = self._input.encode(self.stdin.encoding, self.stdin.errors)

        def send_signal(self, sig):
            """Send a signal to the process."""
            if self.returncode is None:
                os.kill(self.pid, sig)

        def terminate(self):
            """Terminate the process with SIGTERM
            """
            self.send_signal(signal.SIGTERM)

        def kill(self):
            """Kill the process with SIGKILL
            """
            self.send_signal(signal.SIGKILL)