# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\exec_command.py
"""
exec_command

Implements exec_command function that is (almost) equivalent to
commands.getstatusoutput function but on NT, DOS systems the
returned status is actually correct (though, the returned status
values may be different by a factor). In addition, exec_command
takes keyword arguments for (re-)defining environment variables.

Provides functions:

  exec_command  --- execute command in a specified directory and
                    in the modified environment.
  find_executable --- locate a command using info from environment
                    variable PATH. Equivalent to posix `which`
                    command.

Author: Pearu Peterson <pearu@cens.ioc.ee>
Created: 11 January 2003

Requires: Python 2.x

Successfully tested on:

========  ============  =================================================
os.name   sys.platform  comments
========  ============  =================================================
posix     linux2        Debian (sid) Linux, Python 2.1.3+, 2.2.3+, 2.3.3
                        PyCrust 0.9.3, Idle 1.0.2
posix     linux2        Red Hat 9 Linux, Python 2.1.3, 2.2.2, 2.3.2
posix     sunos5        SunOS 5.9, Python 2.2, 2.3.2
posix     darwin        Darwin 7.2.0, Python 2.3
nt        win32         Windows Me
                        Python 2.3(EE), Idle 1.0, PyCrust 0.7.2
                        Python 2.1.1 Idle 0.8
nt        win32         Windows 98, Python 2.1.1. Idle 0.8
nt        win32         Cygwin 98-4.10, Python 2.1.1(MSC) - echo tests
                        fail i.e. redefining environment variables may
                        not work. FIXED: don't use cygwin echo!
                        Comment: also `cmd /c echo` will not work
                        but redefining environment variables do work.
posix     cygwin        Cygwin 98-4.10, Python 2.3.3(cygming special)
nt        win32         Windows XP, Python 2.3.3
========  ============  =================================================

Known bugs:

* Tests, that send messages to stderr, fail when executed from MSYS prompt
  because the messages are lost at some point.

"""
from __future__ import division, absolute_import, print_function
__all__ = [
 'exec_command', 'find_executable']
import os, sys, subprocess, locale, warnings
from numpy.distutils.misc_util import is_sequence, make_temp_file
from numpy.distutils import log

def filepath_from_subprocess_output(output):
    """
    Convert `bytes` in the encoding used by a subprocess into a filesystem-appropriate `str`.

    Inherited from `exec_command`, and possibly incorrect.
    """
    mylocale = locale.getpreferredencoding(False)
    if mylocale is None:
        mylocale = 'ascii'
    output = output.decode(mylocale, errors='replace')
    output = output.replace('\r\n', '\n')
    if output[-1:] == '\n':
        output = output[:-1]
    if sys.version_info < (3, 0):
        output = output.encode('ascii', errors='replace')
    return output


def forward_bytes_to_stdout(val):
    """
    Forward bytes from a subprocess call to the console, without attempting to
    decode them.

    The assumption is that the subprocess call already returned bytes in
    a suitable encoding.
    """
    if sys.version_info.major < 3:
        sys.stdout.write(val)
    else:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(val)
        else:
            if hasattr(sys.stdout, 'encoding'):
                sys.stdout.write(val.decode(sys.stdout.encoding))
            else:
                sys.stdout.write(val.decode('utf8', errors='replace'))


def temp_file_name():
    warnings.warn('temp_file_name is deprecated since NumPy v1.17, use tempfile.mkstemp instead', DeprecationWarning,
      stacklevel=1)
    fo, name = make_temp_file()
    fo.close()
    return name


def get_pythonexe():
    pythonexe = sys.executable
    if os.name in ('nt', 'dos'):
        fdir, fn = os.path.split(pythonexe)
        fn = fn.upper().replace('PYTHONW', 'PYTHON')
        pythonexe = os.path.join(fdir, fn)
        assert os.path.isfile(pythonexe), '%r is not a file' % (pythonexe,)
    return pythonexe


def find_executable--- This code section failed: ---

 L. 130         0  LOAD_FAST                'exe'
                2  LOAD_FAST                'path'
                4  BUILD_TUPLE_2         2 
                6  STORE_FAST               'key'

 L. 131         8  SETUP_FINALLY        20  'to 20'

 L. 132        10  LOAD_FAST                '_cache'
               12  LOAD_FAST                'key'
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     8  '8'

 L. 133        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    38  'to 38'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 134        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            26  '26'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

 L. 135        40  LOAD_GLOBAL              log
               42  LOAD_METHOD              debug
               44  LOAD_STR                 'find_executable(%r)'
               46  LOAD_FAST                'exe'
               48  BINARY_MODULO    
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 136        54  LOAD_FAST                'exe'
               56  STORE_FAST               'orig_exe'

 L. 138        58  LOAD_FAST                'path'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L. 139        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                environ
               70  LOAD_METHOD              get
               72  LOAD_STR                 'PATH'
               74  LOAD_GLOBAL              os
               76  LOAD_ATTR                defpath
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'path'
             82_0  COME_FROM            64  '64'

 L. 140        82  LOAD_GLOBAL              os
               84  LOAD_ATTR                name
               86  LOAD_STR                 'posix'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 141        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_ATTR                realpath
               98  STORE_FAST               'realpath'
              100  JUMP_FORWARD        110  'to 110'
            102_0  COME_FROM            90  '90'

 L. 143       102  LOAD_LAMBDA              '<code_object <lambda>>'
              104  LOAD_STR                 'find_executable.<locals>.<lambda>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  STORE_FAST               'realpath'
            110_0  COME_FROM           100  '100'

 L. 145       110  LOAD_FAST                'exe'
              112  LOAD_METHOD              startswith
              114  LOAD_STR                 '"'
              116  CALL_METHOD_1         1  ''
              118  POP_JUMP_IF_FALSE   132  'to 132'

 L. 146       120  LOAD_FAST                'exe'
              122  LOAD_CONST               1
              124  LOAD_CONST               -1
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  STORE_FAST               'exe'
            132_0  COME_FROM           118  '118'

 L. 148       132  LOAD_STR                 ''
              134  BUILD_LIST_1          1 
              136  STORE_FAST               'suffixes'

 L. 149       138  LOAD_GLOBAL              os
              140  LOAD_ATTR                name
              142  LOAD_CONST               ('nt', 'dos', 'os2')
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   190  'to 190'

 L. 150       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              splitext
              154  LOAD_FAST                'exe'
              156  CALL_METHOD_1         1  ''
              158  UNPACK_SEQUENCE_2     2 
              160  STORE_FAST               'fn'
              162  STORE_FAST               'ext'

 L. 151       164  LOAD_STR                 '.exe'
              166  LOAD_STR                 '.com'
              168  LOAD_STR                 '.bat'
              170  BUILD_LIST_3          3 
              172  STORE_FAST               'extra_suffixes'

 L. 152       174  LOAD_FAST                'ext'
              176  LOAD_METHOD              lower
              178  CALL_METHOD_0         0  ''
              180  LOAD_FAST                'extra_suffixes'
              182  COMPARE_OP               not-in
              184  POP_JUMP_IF_FALSE   190  'to 190'

 L. 153       186  LOAD_FAST                'extra_suffixes'
              188  STORE_FAST               'suffixes'
            190_0  COME_FROM           184  '184'
            190_1  COME_FROM           146  '146'

 L. 155       190  LOAD_GLOBAL              os
              192  LOAD_ATTR                path
              194  LOAD_METHOD              isabs
              196  LOAD_FAST                'exe'
              198  CALL_METHOD_1         1  ''
              200  POP_JUMP_IF_FALSE   210  'to 210'

 L. 156       202  LOAD_STR                 ''
              204  BUILD_LIST_1          1 
              206  STORE_FAST               'paths'
              208  JUMP_FORWARD        232  'to 232'
            210_0  COME_FROM           200  '200'

 L. 158       210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'find_executable.<locals>.<listcomp>'
              214  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              216  LOAD_FAST                'path'
              218  LOAD_METHOD              split
              220  LOAD_GLOBAL              os
              222  LOAD_ATTR                pathsep
              224  CALL_METHOD_1         1  ''
              226  GET_ITER         
              228  CALL_FUNCTION_1       1  ''
              230  STORE_FAST               'paths'
            232_0  COME_FROM           208  '208'

 L. 160       232  LOAD_FAST                'paths'
              234  GET_ITER         
              236  FOR_ITER            362  'to 362'
              238  STORE_FAST               'path'

 L. 161       240  LOAD_GLOBAL              os
              242  LOAD_ATTR                path
              244  LOAD_METHOD              join
              246  LOAD_FAST                'path'
              248  LOAD_FAST                'exe'
              250  CALL_METHOD_2         2  ''
              252  STORE_FAST               'fn'

 L. 162       254  LOAD_FAST                'suffixes'
              256  GET_ITER         
            258_0  COME_FROM           318  '318'
            258_1  COME_FROM           302  '302'
              258  FOR_ITER            360  'to 360'
              260  STORE_FAST               's'

 L. 163       262  LOAD_FAST                'fn'
              264  LOAD_FAST                's'
              266  BINARY_ADD       
              268  STORE_FAST               'f_ext'

 L. 164       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_METHOD              islink
              276  LOAD_FAST                'f_ext'
              278  CALL_METHOD_1         1  ''
          280_282  POP_JUMP_IF_TRUE    292  'to 292'

 L. 165       284  LOAD_FAST                'realpath'
              286  LOAD_FAST                'f_ext'
              288  CALL_FUNCTION_1       1  ''
              290  STORE_FAST               'f_ext'
            292_0  COME_FROM           280  '280'

 L. 166       292  LOAD_GLOBAL              os
              294  LOAD_ATTR                path
              296  LOAD_METHOD              isfile
              298  LOAD_FAST                'f_ext'
              300  CALL_METHOD_1         1  ''
          302_304  POP_JUMP_IF_FALSE   258  'to 258'
              306  LOAD_GLOBAL              os
              308  LOAD_METHOD              access
              310  LOAD_FAST                'f_ext'
              312  LOAD_GLOBAL              os
              314  LOAD_ATTR                X_OK
              316  CALL_METHOD_2         2  ''
          318_320  POP_JUMP_IF_FALSE   258  'to 258'

 L. 167       322  LOAD_GLOBAL              log
              324  LOAD_METHOD              info
              326  LOAD_STR                 'Found executable %s'
              328  LOAD_FAST                'f_ext'
              330  BINARY_MODULO    
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L. 168       336  LOAD_FAST                'f_ext'
              338  LOAD_FAST                '_cache'
              340  LOAD_FAST                'key'
              342  STORE_SUBSCR     

 L. 169       344  LOAD_FAST                'f_ext'
              346  ROT_TWO          
              348  POP_TOP          
              350  ROT_TWO          
              352  POP_TOP          
              354  RETURN_VALUE     
          356_358  JUMP_BACK           258  'to 258'
              360  JUMP_BACK           236  'to 236'

 L. 171       362  LOAD_GLOBAL              log
              364  LOAD_METHOD              warn
              366  LOAD_STR                 'Could not locate executable %s'
              368  LOAD_FAST                'orig_exe'
              370  BINARY_MODULO    
              372  CALL_METHOD_1         1  ''
              374  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 30


def _preserve_environment(names):
    log.debug('_preserve_environment(%r)' % names)
    env = {os.environ.get(name):name for name in names}
    return env


def _update_environment(**env):
    log.debug('_update_environment(...)')
    for name, value in env.items():
        os.environ[name] = value or ''


def exec_command(command, execute_in='', use_shell=None, use_tee=None, _with_python=1, **env):
    """
    Return (status,output) of executed command.

    .. deprecated:: 1.17
        Use subprocess.Popen instead

    Parameters
    ----------
    command : str
        A concatenated string of executable and arguments.
    execute_in : str
        Before running command ``cd execute_in`` and after ``cd -``.
    use_shell : {bool, None}, optional
        If True, execute ``sh -c command``. Default None (True)
    use_tee : {bool, None}, optional
        If True use tee. Default None (True)

    Returns
    -------
    res : str
        Both stdout and stderr messages.

    Notes
    -----
    On NT, DOS systems the returned status is correct for external commands.
    Wild cards will not work for non-posix systems or when use_shell=0.

    """
    warnings.warn('exec_command is deprecated since NumPy v1.17, use subprocess.Popen instead', DeprecationWarning,
      stacklevel=1)
    log.debug('exec_command(%r,%s)' % (command,
     ','.join(['%s=%r' % kv for kv in env.items()])))
    if use_tee is None:
        use_tee = os.name == 'posix'
    if use_shell is None:
        use_shell = os.name == 'posix'
    execute_in = os.path.abspath(execute_in)
    oldcwd = os.path.abspath(os.getcwd())
    if __name__[-12:] == 'exec_command':
        exec_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        if os.path.isfile('exec_command.py'):
            exec_dir = os.path.abspath('.')
        else:
            exec_dir = os.path.abspath(sys.argv[0])
            if os.path.isfile(exec_dir):
                exec_dir = os.path.dirname(exec_dir)
            elif oldcwd != execute_in:
                os.chdir(execute_in)
                log.debug('New cwd: %s' % execute_in)
            else:
                log.debug('Retaining cwd: %s' % oldcwd)
            oldenv = _preserve_environment(list(env.keys()))
            _update_environment(**env)
            try:
                st = _exec_command(command, use_shell=use_shell, 
                 use_tee=use_tee, **env)
            finally:
                if oldcwd != execute_in:
                    os.chdir(oldcwd)
                    log.debug('Restored cwd to %s' % oldcwd)
                _update_environment(**oldenv)

            return st


def _exec_command(command, use_shell=None, use_tee=None, **env):
    """
    Internal workhorse for exec_command().
    """
    if use_shell is None:
        use_shell = os.name == 'posix'
    if use_tee is None:
        use_tee = os.name == 'posix'
    if os.name == 'posix' and use_shell:
        sh = os.environ.get('SHELL', '/bin/sh')
        if is_sequence(command):
            command = [
             sh, '-c', ' '.join(command)]
        else:
            command = [
             sh, '-c', command]
        use_shell = False
    else:
        if os.name == 'nt':
            if is_sequence(command):
                command = ' '.join((_quote_arg(arg) for arg in command))
        else:
            env = env or None
            try:
                proc = subprocess.Popen(command, shell=use_shell, env=env, stdout=(subprocess.PIPE),
                  stderr=(subprocess.STDOUT),
                  universal_newlines=False)
            except EnvironmentError:
                return (127, '')

        text, err = proc.communicate()
        mylocale = locale.getpreferredencoding(False)
        if mylocale is None:
            mylocale = 'ascii'
        text = text.decode(mylocale, errors='replace')
        text = text.replace('\r\n', '\n')
        if text[-1:] == '\n':
            text = text[:-1]
        if sys.version_info < (3, 0):
            text = text.encode('ascii', errors='replace')
        if use_tee:
            if text:
                print(text)
        return (
         proc.returncode, text)


def _quote_arg(arg):
    """
    Quote the argument for safe use in a shell command line.
    """
    if '"' not in arg:
        if ' ' in arg:
            return '"%s"' % arg
    return arg