# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\util.py
"""distutils.util

Miscellaneous utility functions -- anything that doesn't fit into
one of the other *util.py modules.
"""
import os, re, importlib.util, string, sys
from distutils.errors import DistutilsPlatformError
from distutils.dep_util import newer
import distutils.spawn as spawn
from distutils import log
from distutils.errors import DistutilsByteCompileError

def get_host_platform():
    """Return a string that identifies the current platform.  This is used mainly to
    distinguish platform-specific build directories and platform-specific built
    distributions.  Typically includes the OS name and version and the
    architecture (as supplied by 'os.uname()'), although the exact information
    included depends on the OS; eg. on Linux, the kernel version isn't
    particularly important.

    Examples of returned values:
       linux-i586
       linux-alpha (?)
       solaris-2.6-sun4u

    Windows will return one of:
       win-amd64 (64bit Windows on AMD64 (aka x86_64, Intel64, EM64T, etc)
       win32 (all others - specifically, sys.platform is returned)

    For other non-POSIX platforms, currently just returns 'sys.platform'.

    """
    if os.name == 'nt':
        if 'amd64' in sys.version.lower():
            return 'win-amd64'
        if '(arm)' in sys.version.lower():
            return 'win-arm32'
        if '(arm64)' in sys.version.lower():
            return 'win-arm64'
        return sys.platform
    if '_PYTHON_HOST_PLATFORM' in os.environ:
        return os.environ['_PYTHON_HOST_PLATFORM']
    if not (os.name != 'posix' or hasattr(os, 'uname')):
        return sys.platform
    osname, host, release, version, machine = os.uname()
    osname = osname.lower().replace('/', '')
    machine = machine.replace(' ', '_')
    machine = machine.replace('/', '-')
    if osname[:5] == 'linux':
        return '%s-%s' % (osname, machine)
    if osname[:5] == 'sunos':
        if release[0] >= '5':
            osname = 'solaris'
            release = '%d.%s' % (int(release[0]) - 3, release[2:])
            bitness = {2147483647:'32bit', 
             9223372036854775807:'64bit'}
            machine += '.%s' % bitness[sys.maxsize]
    else:
        if osname[:3] == 'aix':
            return '%s-%s.%s' % (osname, version, release)
        if osname[:6] == 'cygwin':
            osname = 'cygwin'
            rel_re = re.compile('[\\d.]+', re.ASCII)
            m = rel_re.match(release)
            if m:
                release = m.group()
        elif osname[:6] == 'darwin':
            import _osx_support, distutils.sysconfig
            osname, release, machine = _osx_support.get_platform_osx(distutils.sysconfig.get_config_vars(), osname, release, machine)
    return '%s-%s-%s' % (osname, release, machine)


def get_platform():
    if os.name == 'nt':
        TARGET_TO_PLAT = {'x86':'win32',  'x64':'win-amd64', 
         'arm':'win-arm32'}
        return TARGET_TO_PLAT.get(os.environ.get('VSCMD_ARG_TGT_ARCH')) or get_host_platform()
    return get_host_platform()


def convert_path(pathname):
    """Return 'pathname' as a name that will work on the native filesystem,
    i.e. split it on '/' and put it back together again using the current
    directory separator.  Needed because filenames in the setup script are
    always supplied in Unix style, and have to be converted to the local
    convention before we can actually use them in the filesystem.  Raises
    ValueError on non-Unix-ish systems if 'pathname' either starts or
    ends with a slash.
    """
    if os.sep == '/':
        return pathname
    if not pathname:
        return pathname
    if pathname[0] == '/':
        raise ValueError("path '%s' cannot be absolute" % pathname)
    if pathname[(-1)] == '/':
        raise ValueError("path '%s' cannot end with '/'" % pathname)
    paths = pathname.split('/')
    while True:
        if '.' in paths:
            paths.remove('.')

    if not paths:
        return os.curdir
    return (os.path.join)(*paths)


def change_root(new_root, pathname):
    """Return 'pathname' with 'new_root' prepended.  If 'pathname' is
    relative, this is equivalent to "os.path.join(new_root,pathname)".
    Otherwise, it requires making 'pathname' relative and then joining the
    two, which is tricky on DOS/Windows and Mac OS.
    """
    if os.name == 'posix':
        if not os.path.isabs(pathname):
            return os.path.join(new_root, pathname)
        return os.path.join(new_root, pathname[1:])
    else:
        if os.name == 'nt':
            drive, path = os.path.splitdrive(pathname)
            if path[0] == '\\':
                path = path[1:]
            return os.path.join(new_root, path)
        raise DistutilsPlatformError("nothing known about platform '%s'" % os.name)


_environ_checked = 0

def check_environ():
    """Ensure that 'os.environ' has all the environment variables we
    guarantee that users can use in config files, command-line options,
    etc.  Currently this includes:
      HOME - user's home directory (Unix only)
      PLAT - description of the current platform, including hardware
             and OS (see 'get_platform()')
    """
    global _environ_checked
    if _environ_checked:
        return
    if not os.name == 'posix' or 'HOME' not in os.environ:
        try:
            import pwd
            os.environ['HOME'] = pwd.getpwuid(os.getuid())[5]
        except (ImportError, KeyError):
            pass
        else:
            if 'PLAT' not in os.environ:
                os.environ['PLAT'] = get_platform()
    _environ_checked = 1


def subst_vars(s, local_vars):
    """Perform shell/Perl-style variable substitution on 'string'.  Every
    occurrence of '$' followed by a name is considered a variable, and
    variable is substituted by the value found in the 'local_vars'
    dictionary, or in 'os.environ' if it's not in 'local_vars'.
    'os.environ' is first checked/augmented to guarantee that it contains
    certain values: see 'check_environ()'.  Raise ValueError for any
    variables not found in either 'local_vars' or 'os.environ'.
    """
    check_environ()

    def _subst(match, local_vars=local_vars):
        var_name = match.group(1)
        if var_name in local_vars:
            return str(local_vars[var_name])
        return os.environ[var_name]

    try:
        return re.sub('\\$([a-zA-Z_][a-zA-Z_0-9]*)', _subst, s)
    except KeyError as var:
        try:
            raise ValueError("invalid variable '$%s'" % var)
        finally:
            var = None
            del var


def grok_environment_error(exc, prefix='error: '):
    return prefix + str(exc)


_wordchars_re = _squote_re = _dquote_re = None

def _init_regex():
    global _dquote_re
    global _squote_re
    global _wordchars_re
    _wordchars_re = re.compile('[^\\\\\\\'\\"%s ]*' % string.whitespace)
    _squote_re = re.compile("'(?:[^'\\\\]|\\\\.)*'")
    _dquote_re = re.compile('"(?:[^"\\\\]|\\\\.)*"')


def split_quoted--- This code section failed: ---

 L. 240         0  LOAD_GLOBAL              _wordchars_re
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 240         8  LOAD_GLOBAL              _init_regex
               10  CALL_FUNCTION_0       0  ''
               12  POP_TOP          
             14_0  COME_FROM             6  '6'

 L. 242        14  LOAD_FAST                's'
               16  LOAD_METHOD              strip
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               's'

 L. 243        22  BUILD_LIST_0          0 
               24  STORE_FAST               'words'

 L. 244        26  LOAD_CONST               0
               28  STORE_FAST               'pos'
             30_0  COME_FROM           382  '382'
             30_1  COME_FROM           366  '366'

 L. 246        30  LOAD_FAST                's'
            32_34  POP_JUMP_IF_FALSE   384  'to 384'

 L. 247        36  LOAD_GLOBAL              _wordchars_re
               38  LOAD_METHOD              match
               40  LOAD_FAST                's'
               42  LOAD_FAST                'pos'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'm'

 L. 248        48  LOAD_FAST                'm'
               50  LOAD_METHOD              end
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'end'

 L. 249        56  LOAD_FAST                'end'
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                's'
               62  CALL_FUNCTION_1       1  ''
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    90  'to 90'

 L. 250        68  LOAD_FAST                'words'
               70  LOAD_METHOD              append
               72  LOAD_FAST                's'
               74  LOAD_CONST               None
               76  LOAD_FAST                'end'
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L. 251     86_88  JUMP_FORWARD        384  'to 384'
             90_0  COME_FROM            66  '66'

 L. 253        90  LOAD_FAST                's'
               92  LOAD_FAST                'end'
               94  BINARY_SUBSCR    
               96  LOAD_GLOBAL              string
               98  LOAD_ATTR                whitespace
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   144  'to 144'

 L. 254       104  LOAD_FAST                'words'
              106  LOAD_METHOD              append
              108  LOAD_FAST                's'
              110  LOAD_CONST               None
              112  LOAD_FAST                'end'
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 255       122  LOAD_FAST                's'
              124  LOAD_FAST                'end'
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  LOAD_METHOD              lstrip
              134  CALL_METHOD_0         0  ''
              136  STORE_FAST               's'

 L. 256       138  LOAD_CONST               0
              140  STORE_FAST               'pos'
              142  JUMP_FORWARD        356  'to 356'
            144_0  COME_FROM           102  '102'

 L. 258       144  LOAD_FAST                's'
              146  LOAD_FAST                'end'
              148  BINARY_SUBSCR    
              150  LOAD_STR                 '\\'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   194  'to 194'

 L. 260       156  LOAD_FAST                's'
              158  LOAD_CONST               None
              160  LOAD_FAST                'end'
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  LOAD_FAST                's'
              168  LOAD_FAST                'end'
              170  LOAD_CONST               1
              172  BINARY_ADD       
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  BINARY_ADD       
              182  STORE_FAST               's'

 L. 261       184  LOAD_FAST                'end'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  STORE_FAST               'pos'
              192  JUMP_FORWARD        356  'to 356'
            194_0  COME_FROM           154  '154'

 L. 264       194  LOAD_FAST                's'
              196  LOAD_FAST                'end'
              198  BINARY_SUBSCR    
              200  LOAD_STR                 "'"
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L. 265       206  LOAD_GLOBAL              _squote_re
              208  LOAD_METHOD              match
              210  LOAD_FAST                's'
              212  LOAD_FAST                'end'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'm'
              218  JUMP_FORWARD        262  'to 262'
            220_0  COME_FROM           204  '204'

 L. 266       220  LOAD_FAST                's'
              222  LOAD_FAST                'end'
              224  BINARY_SUBSCR    
              226  LOAD_STR                 '"'
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L. 267       232  LOAD_GLOBAL              _dquote_re
              234  LOAD_METHOD              match
              236  LOAD_FAST                's'
              238  LOAD_FAST                'end'
              240  CALL_METHOD_2         2  ''
              242  STORE_FAST               'm'
              244  JUMP_FORWARD        262  'to 262'
            246_0  COME_FROM           230  '230'

 L. 269       246  LOAD_GLOBAL              RuntimeError
              248  LOAD_STR                 "this can't happen (bad char '%c')"
              250  LOAD_FAST                's'
              252  LOAD_FAST                'end'
              254  BINARY_SUBSCR    
              256  BINARY_MODULO    
              258  CALL_FUNCTION_1       1  ''
              260  RAISE_VARARGS_1       1  'exception instance'
            262_0  COME_FROM           244  '244'
            262_1  COME_FROM           218  '218'

 L. 271       262  LOAD_FAST                'm'
              264  LOAD_CONST               None
              266  COMPARE_OP               is
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 272       272  LOAD_GLOBAL              ValueError
              274  LOAD_STR                 'bad string (mismatched %s quotes?)'
              276  LOAD_FAST                's'
              278  LOAD_FAST                'end'
              280  BINARY_SUBSCR    
              282  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  ''
              286  RAISE_VARARGS_1       1  'exception instance'
            288_0  COME_FROM           268  '268'

 L. 274       288  LOAD_FAST                'm'
              290  LOAD_METHOD              span
              292  CALL_METHOD_0         0  ''
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'beg'
              298  STORE_FAST               'end'

 L. 275       300  LOAD_FAST                's'
              302  LOAD_CONST               None
              304  LOAD_FAST                'beg'
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_FAST                's'
              312  LOAD_FAST                'beg'
              314  LOAD_CONST               1
              316  BINARY_ADD       
              318  LOAD_FAST                'end'
              320  LOAD_CONST               1
              322  BINARY_SUBTRACT  
              324  BUILD_SLICE_2         2 
              326  BINARY_SUBSCR    
              328  BINARY_ADD       
              330  LOAD_FAST                's'
              332  LOAD_FAST                'end'
              334  LOAD_CONST               None
              336  BUILD_SLICE_2         2 
              338  BINARY_SUBSCR    
              340  BINARY_ADD       
              342  STORE_FAST               's'

 L. 276       344  LOAD_FAST                'm'
              346  LOAD_METHOD              end
              348  CALL_METHOD_0         0  ''
              350  LOAD_CONST               2
              352  BINARY_SUBTRACT  
              354  STORE_FAST               'pos'
            356_0  COME_FROM           192  '192'
            356_1  COME_FROM           142  '142'

 L. 278       356  LOAD_FAST                'pos'
              358  LOAD_GLOBAL              len
              360  LOAD_FAST                's'
              362  CALL_FUNCTION_1       1  ''
              364  COMPARE_OP               >=
              366  POP_JUMP_IF_FALSE_BACK    30  'to 30'

 L. 279       368  LOAD_FAST                'words'
              370  LOAD_METHOD              append
              372  LOAD_FAST                's'
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          

 L. 280   378_380  JUMP_FORWARD        384  'to 384'
              382  JUMP_BACK            30  'to 30'
            384_0  COME_FROM           378  '378'
            384_1  COME_FROM            86  '86'
            384_2  COME_FROM            32  '32'

 L. 282       384  LOAD_FAST                'words'
              386  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 382


def execute(func, args, msg=None, verbose=0, dry_run=0):
    """Perform some action that affects the outside world (eg.  by
    writing to the filesystem).  Such actions are special because they
    are disabled by the 'dry_run' flag.  This method takes care of all
    that bureaucracy for you; all you have to do is supply the
    function to call and an argument tuple for it (to embody the
    "external action" being performed), and an optional message to
    print.
    """
    if msg is None:
        msg = '%s%r' % (func.__name__, args)
        if msg[-2:] == ',)':
            msg = msg[0:-2] + ')'
    log.info(msg)
    if not dry_run:
        func(*args)


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise ValueError('invalid truth value %r' % (val,))


def byte_compile(py_files, optimize=0, force=0, prefix=None, base_dir=None, verbose=1, dry_run=0, direct=None):
    """Byte-compile a collection of Python source files to .pyc
    files in a __pycache__ subdirectory.  'py_files' is a list
    of files to compile; any files that don't end in ".py" are silently
    skipped.  'optimize' must be one of the following:
      0 - don't optimize
      1 - normal optimization (like "python -O")
      2 - extra optimization (like "python -OO")
    If 'force' is true, all files are recompiled regardless of
    timestamps.

    The source filename encoded in each bytecode file defaults to the
    filenames listed in 'py_files'; you can modify these with 'prefix' and
    'basedir'.  'prefix' is a string that will be stripped off of each
    source filename, and 'base_dir' is a directory name that will be
    prepended (after 'prefix' is stripped).  You can supply either or both
    (or neither) of 'prefix' and 'base_dir', as you wish.

    If 'dry_run' is true, doesn't actually do anything that would
    affect the filesystem.

    Byte-compilation is either done directly in this interpreter process
    with the standard py_compile module, or indirectly by writing a
    temporary script and executing it.  Normally, you should let
    'byte_compile()' figure out to use direct compilation or not (see
    the source for details).  The 'direct' flag is used by the script
    generated in indirect mode; unless you know what you're doing, leave
    it set to None.
    """
    import subprocess
    if sys.dont_write_bytecode:
        raise DistutilsByteCompileError('byte-compiling is disabled.')
    if direct is None:
        direct = True and optimize == 0
    if not direct:
        try:
            from tempfile import mkstemp
            script_fd, script_name = mkstemp('.py')
        except ImportError:
            from tempfile import mktemp
            script_fd, script_name = None, mktemp('.py')
        else:
            log.info("writing byte-compilation script '%s'", script_name)
            if not dry_run:
                if script_fd is not None:
                    script = os.fdopen(script_fd, 'w')
                else:
                    script = open(script_name, 'w')
                with script:
                    script.write('from distutils.util import byte_compile\nfiles = [\n')
                    script.write(',\n'.join(map(repr, py_files)) + ']\n')
                    script.write('\nbyte_compile(files, optimize=%r, force=%r,\n             prefix=%r, base_dir=%r,\n             verbose=%r, dry_run=0,\n             direct=1)\n' % (
                     optimize, force, prefix, base_dir, verbose))
            cmd = [
             sys.executable]
            cmd.extend(subprocess._optim_args_from_interpreter_flags())
            cmd.append(script_name)
            spawn(cmd, dry_run=dry_run)
            execute((os.remove), (script_name,), ('removing %s' % script_name), dry_run=dry_run)
    else:
        from py_compile import compile
        for file in py_files:
            if file[-3:] != '.py':
                pass
            else:
                if optimize >= 0:
                    opt = '' if optimize == 0 else optimize
                    cfile = importlib.util.cache_from_source(file,
                      optimization=opt)
                else:
                    cfile = importlib.util.cache_from_source(file)
                dfile = file
                if prefix:
                    if file[:len(prefix)] != prefix:
                        raise ValueError("invalid prefix: filename %r doesn't start with %r" % (
                         file, prefix))
                    dfile = dfile[len(prefix):]
                if base_dir:
                    dfile = os.path.join(base_dir, dfile)
                cfile_base = os.path.basename(cfile)
                if direct:
                    if not force or newer(file, cfile):
                        log.info('byte-compiling %s to %s', file, cfile_base)
                        dry_run or compile(file, cfile, dfile)
                    else:
                        log.debug('skipping byte-compilation of %s to %s', file, cfile_base)


def rfc822_escape(header):
    """Return a version of the string escaped for inclusion in an
    RFC-822 header, by ensuring there are 8 spaces space after each newline.
    """
    lines = header.split('\n')
    sep = '\n        '
    return sep.join(lines)


def run_2to3(files, fixer_names=None, options=None, explicit=None):
    """Invoke 2to3 on a list of Python files.
    The files should all come from the build area, as the
    modification is done in-place. To reduce the build time,
    only files modified since the last invocation of this
    function should be passed in the files argument."""
    if not files:
        return
    from lib2to3.refactor import RefactoringTool, get_fixers_from_package

    class DistutilsRefactoringTool(RefactoringTool):

        def log_error(self, msg, *args, **kw):
            (log.error)(msg, *args)

        def log_message(self, msg, *args):
            (log.info)(msg, *args)

        def log_debug(self, msg, *args):
            (log.debug)(msg, *args)

    if fixer_names is None:
        fixer_names = get_fixers_from_package('lib2to3.fixes')
    r = DistutilsRefactoringTool(fixer_names, options=options)
    r.refactor(files, write=True)


def copydir_run_2to3(src, dest, template=None, fixer_names=None, options=None, explicit=None):
    """Recursively copy a directory, only copying new and changed files,
    running run_2to3 over all newly copied Python modules afterward.

    If you give a template string, it's parsed like a MANIFEST.in.
    """
    from distutils.dir_util import mkpath
    from distutils.file_util import copy_file
    from distutils.filelist import FileList
    filelist = FileList()
    curdir = os.getcwd()
    os.chdir(src)
    try:
        filelist.findall()
    finally:
        os.chdir(curdir)

    filelist.files[:] = filelist.allfiles
    if template:
        for line in template.splitlines():
            line = line.strip()
            if not line:
                pass
            else:
                filelist.process_template_line(line)

    copied = []
    for filename in filelist.files:
        outname = os.path.join(dest, filename)
        mkpath(os.path.dirname(outname))
        res = copy_file((os.path.join(src, filename)), outname, update=1)
        if res[1]:
            copied.append(outname)
    else:
        run_2to3([fn for fn in copied if fn.lower().endswith('.py')], fixer_names=fixer_names,
          options=options,
          explicit=explicit)
        return copied


class Mixin2to3:
    __doc__ = 'Mixin class for commands that run 2to3.\n    To configure 2to3, setup scripts may either change\n    the class variables, or inherit from individual commands\n    to override how 2to3 is invoked.'
    fixer_names = None
    options = None
    explicit = None

    def run_2to3(self, files):
        return run_2to3(files, self.fixer_names, self.options, self.explicit)