# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\misc_util.py
import os, re, sys, copy, glob, atexit, tempfile, subprocess, shutil, multiprocessing, textwrap, importlib.util, distutils
from distutils.errors import DistutilsError
try:
    from threading import local as tlocal
except ImportError:
    from dummy_threading import local as tlocal
else:
    _tdata = tlocal()
    _tmpdirs = []

    def clean_up_temporary_directory():
        if _tmpdirs is not None:
            for d in _tmpdirs:
                try:
                    shutil.rmtree(d)
                except OSError:
                    pass


    atexit.register(clean_up_temporary_directory)
    from numpy.compat import npy_load_module
    __all__ = [
     'Configuration', 'get_numpy_include_dirs', 'default_config_dict',
     'dict_append', 'appendpath', 'generate_config_py',
     'get_cmd', 'allpath', 'get_mathlibs',
     'terminal_has_colors', 'red_text', 'green_text', 'yellow_text',
     'blue_text', 'cyan_text', 'cyg2win32', 'mingw32', 'all_strings',
     'has_f_sources', 'has_cxx_sources', 'filter_sources',
     'get_dependencies', 'is_local_src_dir', 'get_ext_source_files',
     'get_script_files', 'get_lib_source_files', 'get_data_files',
     'dot_join', 'get_frame', 'minrelpath', 'njoin',
     'is_sequence', 'is_string', 'as_list', 'gpaths', 'get_language',
     'quote_args', 'get_build_architecture', 'get_info', 'get_pkg_info',
     'get_num_build_jobs']

    class InstallableLib:
        __doc__ = '\n    Container to hold information on an installable library.\n\n    Parameters\n    ----------\n    name : str\n        Name of the installed library.\n    build_info : dict\n        Dictionary holding build information.\n    target_dir : str\n        Absolute path specifying where to install the library.\n\n    See Also\n    --------\n    Configuration.add_installed_library\n\n    Notes\n    -----\n    The three parameters are stored as attributes with the same names.\n\n    '

        def __init__(self, name, build_info, target_dir):
            self.name = name
            self.build_info = build_info
            self.target_dir = target_dir


    def get_num_build_jobs():
        """
    Get number of parallel build jobs set by the --parallel command line
    argument of setup.py
    If the command did not receive a setting the environment variable
    NPY_NUM_BUILD_JOBS is checked. If that is unset, return the number of
    processors on the system, with a maximum of 8 (to prevent
    overloading the system if there a lot of CPUs).

    Returns
    -------
    out : int
        number of parallel jobs that can be run

    """
        from numpy.distutils.core import get_distribution
        try:
            cpu_count = len(os.sched_getaffinity(0))
        except AttributeError:
            cpu_count = multiprocessing.cpu_count()
        else:
            cpu_count = min(cpu_count, 8)
            envjobs = int(os.environ.get('NPY_NUM_BUILD_JOBS', cpu_count))
            dist = get_distribution()
            if dist is None:
                return envjobs
            cmdattr = (
             getattr(dist.get_command_obj('build'), 'parallel', None),
             getattr(dist.get_command_obj('build_ext'), 'parallel', None),
             getattr(dist.get_command_obj('build_clib'), 'parallel', None))
            if all((x is None for x in cmdattr)):
                return envjobs
            return max((x for x in cmdattr if x is not None))


    def quote_args(args):
        args = list(args)
        for i in range(len(args)):
            a = args[i]
            if ' ' in a:
                if a[0] not in '"\'':
                    args[i] = '"%s"' % a
        else:
            return args


    def allpath(name):
        """Convert a /-separated pathname to one using the OS's path separator."""
        splitted = name.split('/')
        return (os.path.join)(*splitted)


    def rel_path(path, parent_path):
        """Return path relative to parent_path."""
        pd = os.path.realpath(os.path.abspath(parent_path))
        apath = os.path.realpath(os.path.abspath(path))
        if len(apath) < len(pd):
            return path
        if apath == pd:
            return ''
        if pd == apath[:len(pd)]:
            assert apath[len(pd)] in (os.sep,), repr((path, apath[len(pd)]))
            path = apath[len(pd) + 1:]
        return path


    def get_path_from_frame(frame, parent_path=None):
        """Return path of the module given a frame object from the call stack.

    Returned path is relative to parent_path when given,
    otherwise it is absolute path.
    """
        try:
            caller_file = eval('__file__', frame.f_globals, frame.f_locals)
            d = os.path.dirname(os.path.abspath(caller_file))
        except NameError:
            caller_name = eval('__name__', frame.f_globals, frame.f_locals)
            __import__(caller_name)
            mod = sys.modules[caller_name]
            if hasattr(mod, '__file__'):
                d = os.path.dirname(os.path.abspath(mod.__file__))
            else:
                d = os.path.abspath('.')
        else:
            if parent_path is not None:
                d = rel_path(d, parent_path)
            else:
                return d or '.'


    def njoin(*path):
        """Join two or more pathname components +
    - convert a /-separated pathname to one using the OS's path separator.
    - resolve `..` and `.` from path.

    Either passing n arguments as in njoin('a','b'), or a sequence
    of n names as in njoin(['a','b']) is handled, or a mixture of such arguments.
    """
        paths = []
        for p in path:
            if is_sequence(p):
                paths.append(njoin(*p))
            else:
                assert is_string(p)
                paths.append(p)
        else:
            path = paths
            if not path:
                joined = ''
            else:
                joined = (os.path.join)(*path)
            if os.path.sep != '/':
                joined = joined.replace('/', os.path.sep)
            return minrelpath(joined)


    def get_mathlibs(path=None):
        """Return the MATHLIB line from numpyconfig.h
    """
        if path is not None:
            config_file = os.path.join(path, '_numpyconfig.h')
        else:
            dirs = get_numpy_include_dirs()
            for path in dirs:
                fn = os.path.join(path, '_numpyconfig.h')
                if os.path.exists(fn):
                    config_file = fn
                    break
            else:
                raise DistutilsError('_numpyconfig.h not found in numpy include dirs %r' % (
                 dirs,))

        with open(config_file) as fid:
            mathlibs = []
            s = '#define MATHLIB'
            for line in fid:
                if line.startswith(s):
                    value = line[len(s):].strip()
                    if value:
                        mathlibs.extend(value.split(','))

        return mathlibs


    def minrelpath(path):
        """Resolve `..` and '.' from path.
    """
        if not is_string(path):
            return path
        if '.' not in path:
            return path
        l = path.split(os.sep)
        while True:
            if l:
                try:
                    i = l.index('.', 1)
                except ValueError:
                    break
                else:
                    del l[i]

        j = 1
        while True:
            if l:
                try:
                    i = l.index('..', j)
                except ValueError:
                    break
                else:
                    if l[(i - 1)] == '..':
                        j += 1
                    else:
                        del l[i]
                        del l[i - 1]
                        j = 1

        if not l:
            return ''
        return os.sep.join(l)


    def sorted_glob(fileglob):
        """sorts output of python glob for https://bugs.python.org/issue30461
    to allow extensions to have reproducible build results"""
        return sorted(glob.glob(fileglob))


    def _fix_paths(paths, local_path, include_non_existing):
        assert is_sequence(paths), repr(type(paths))
        new_paths = []
        if is_string(paths):
            raise AssertionError(repr(paths))
        for n in paths:
            if is_string(n):
                if '*' in n or '?' in n:
                    p = sorted_glob(n)
                    p2 = sorted_glob(njoin(local_path, n))
                    if p2:
                        new_paths.extend(p2)
                    elif p:
                        new_paths.extend(p)
                    else:
                        if include_non_existing:
                            new_paths.append(n)
                        print('could not resolve pattern in %r: %r' % (
                         local_path, n))
                else:
                    n2 = njoin(local_path, n)
                    if os.path.exists(n2):
                        new_paths.append(n2)
                    else:
                        if os.path.exists(n):
                            new_paths.append(n)
                        elif include_non_existing:
                            new_paths.append(n)
                        os.path.exists(n) or print('non-existing path in %r: %r' % (
                         local_path, n))
            else:
                if is_sequence(n):
                    new_paths.extend(_fix_paths(n, local_path, include_non_existing))
                else:
                    new_paths.append(n)
        else:
            return [minrelpath(p) for p in new_paths]


    def gpaths(paths, local_path='', include_non_existing=True):
        """Apply glob to paths and prepend local_path if needed.
    """
        if is_string(paths):
            paths = (
             paths,)
        return _fix_paths(paths, local_path, include_non_existing)


    def make_temp_file(suffix='', prefix='', text=True):
        if not hasattr(_tdata, 'tempdir'):
            _tdata.tempdir = tempfile.mkdtemp()
            _tmpdirs.append(_tdata.tempdir)
        fid, name = tempfile.mkstemp(suffix=suffix, prefix=prefix,
          dir=(_tdata.tempdir),
          text=text)
        fo = os.fdopen(fid, 'w')
        return (
         fo, name)


    def terminal_has_colors--- This code section failed: ---

 L. 320         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'cygwin'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'
               10  LOAD_STR                 'USE_COLOR'
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  COMPARE_OP               not-in
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 329        20  LOAD_CONST               0
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM             8  '8'

 L. 330        24  LOAD_GLOBAL              hasattr
               26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                stdout
               30  LOAD_STR                 'isatty'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE   192  'to 192'
               36  LOAD_GLOBAL              sys
               38  LOAD_ATTR                stdout
               40  LOAD_METHOD              isatty
               42  CALL_METHOD_0         0  ''
               44  POP_JUMP_IF_FALSE   192  'to 192'

 L. 331        46  SETUP_FINALLY       172  'to 172'

 L. 332        48  LOAD_CONST               0
               50  LOAD_CONST               None
               52  IMPORT_NAME              curses
               54  STORE_FAST               'curses'

 L. 333        56  LOAD_FAST                'curses'
               58  LOAD_METHOD              setupterm
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 334        64  LOAD_FAST                'curses'
               66  LOAD_METHOD              tigetnum
               68  LOAD_STR                 'colors'
               70  CALL_METHOD_1         1  ''
               72  LOAD_CONST               0
               74  COMPARE_OP               >=
               76  POP_JUMP_IF_FALSE   168  'to 168'

 L. 335        78  LOAD_FAST                'curses'
               80  LOAD_METHOD              tigetnum
               82  LOAD_STR                 'pairs'
               84  CALL_METHOD_1         1  ''
               86  LOAD_CONST               0
               88  COMPARE_OP               >=

 L. 334        90  POP_JUMP_IF_FALSE   168  'to 168'

 L. 336        92  LOAD_FAST                'curses'
               94  LOAD_METHOD              tigetstr
               96  LOAD_STR                 'setf'
               98  CALL_METHOD_1         1  ''
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not

 L. 334       104  POP_JUMP_IF_FALSE   120  'to 120'

 L. 337       106  LOAD_FAST                'curses'
              108  LOAD_METHOD              tigetstr
              110  LOAD_STR                 'setb'
              112  CALL_METHOD_1         1  ''
              114  LOAD_CONST               None
              116  COMPARE_OP               is-not

 L. 334       118  POP_JUMP_IF_TRUE    162  'to 162'
            120_0  COME_FROM           104  '104'

 L. 338       120  LOAD_FAST                'curses'
              122  LOAD_METHOD              tigetstr
              124  LOAD_STR                 'setaf'
              126  CALL_METHOD_1         1  ''
              128  LOAD_CONST               None
              130  COMPARE_OP               is-not

 L. 334       132  POP_JUMP_IF_FALSE   148  'to 148'

 L. 339       134  LOAD_FAST                'curses'
              136  LOAD_METHOD              tigetstr
              138  LOAD_STR                 'setab'
              140  CALL_METHOD_1         1  ''
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not

 L. 334       146  POP_JUMP_IF_TRUE    162  'to 162'
            148_0  COME_FROM           132  '132'

 L. 340       148  LOAD_FAST                'curses'
              150  LOAD_METHOD              tigetstr
              152  LOAD_STR                 'scp'
              154  CALL_METHOD_1         1  ''
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not

 L. 334       160  POP_JUMP_IF_FALSE   168  'to 168'
            162_0  COME_FROM           146  '146'
            162_1  COME_FROM           118  '118'

 L. 341       162  POP_BLOCK        
              164  LOAD_CONST               1
              166  RETURN_VALUE     
            168_0  COME_FROM           160  '160'
            168_1  COME_FROM            90  '90'
            168_2  COME_FROM            76  '76'
              168  POP_BLOCK        
              170  JUMP_FORWARD        192  'to 192'
            172_0  COME_FROM_FINALLY    46  '46'

 L. 342       172  DUP_TOP          
              174  LOAD_GLOBAL              Exception
              176  COMPARE_OP               exception-match
              178  POP_JUMP_IF_FALSE   190  'to 190'
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          

 L. 343       186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           178  '178'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           170  '170'
            192_2  COME_FROM            44  '44'
            192_3  COME_FROM            34  '34'

 L. 344       192  LOAD_CONST               0
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 164


    if terminal_has_colors():
        _colour_codes = dict(black=0, red=1, green=2, yellow=3, blue=4,
          magenta=5,
          cyan=6,
          white=7,
          default=9)

        def colour_text(s, fg=None, bg=None, bold=False):
            seq = []
            if bold:
                seq.append('1')
            if fg:
                fgcode = 30 + _colour_codes.get(fg.lower(), 0)
                seq.append(str(fgcode))
            if bg:
                bgcode = 40 + _colour_codes.get(fg.lower(), 7)
                seq.append(str(bgcode))
            if seq:
                return '\x1b[%sm%s\x1b[0m' % (';'.join(seq), s)
            return s


    else:

        def colour_text(s, fg=None, bg=None):
            return s


    def default_text(s):
        return colour_text(s, 'default')


    def red_text(s):
        return colour_text(s, 'red')


    def green_text(s):
        return colour_text(s, 'green')


    def yellow_text(s):
        return colour_text(s, 'yellow')


    def cyan_text(s):
        return colour_text(s, 'cyan')


    def blue_text(s):
        return colour_text(s, 'blue')


    def cyg2win32(path):
        if sys.platform == 'cygwin':
            if path.startswith('/cygdrive'):
                path = path[10] + ':' + os.path.normcase(path[11:])
        return path


    def mingw32():
        """Return true when using mingw32 environment.
    """
        if sys.platform == 'win32':
            if os.environ.get('OSTYPE', '') == 'msys':
                return True
            if os.environ.get('MSYSTEM', '') == 'MINGW32':
                return True
        return False


    def msvc_runtime_version():
        """Return version of MSVC runtime library, as defined by __MSC_VER__ macro"""
        msc_pos = sys.version.find('MSC v.')
        if msc_pos != -1:
            msc_ver = int(sys.version[msc_pos + 6:msc_pos + 10])
        else:
            msc_ver = None
        return msc_ver


    def msvc_runtime_library():
        """Return name of MSVC runtime library if Python was built with MSVC >= 7"""
        ver = msvc_runtime_major()
        if ver:
            if ver < 140:
                return 'msvcr%i' % ver
            return 'vcruntime%i' % ver
        else:
            return


    def msvc_runtime_major():
        """Return major version of MSVC runtime coded like get_build_msvc_version"""
        major = {1300:70,  1310:71, 
         1400:80, 
         1500:90, 
         1600:100, 
         1900:140}.get(msvc_runtime_version(), None)
        return major


    cxx_ext_match = re.compile('.*[.](cpp|cxx|cc)\\Z', re.I).match
    fortran_ext_match = re.compile('.*[.](f90|f95|f77|for|ftn|f)\\Z', re.I).match
    f90_ext_match = re.compile('.*[.](f90|f95)\\Z', re.I).match
    f90_module_name_match = re.compile('\\s*module\\s*(?P<name>[\\w_]+)', re.I).match

    def _get_f90_modules(source):
        """Return a list of Fortran f90 module names that
    given source file defines.
    """
        if not f90_ext_match(source):
            return []
        modules = []
        with open(source, 'r') as f:
            for line in f:
                m = f90_module_name_match(line)
                if m:
                    name = m.group('name')
                    modules.append(name)

        return modules


    def is_string(s):
        return isinstance(s, str)


    def all_strings(lst):
        """Return True if all items in lst are string objects. """
        for item in lst:
            if not is_string(item):
                return False
        else:
            return True


    def is_sequence(seq):
        if is_string(seq):
            return False
        try:
            len(seq)
        except Exception:
            return False
        else:
            return True


    def is_glob_pattern(s):
        return (is_string(s)) and (('*' in s) or ('?' in s))


    def as_list(seq):
        if is_sequence(seq):
            return list(seq)
        return [
         seq]


    def get_language(sources):
        """Determine language value (c,f77,f90) from sources """
        language = None
        for source in sources:
            if isinstance(source, str):
                if f90_ext_match(source):
                    language = 'f90'
                    break
                else:
                    if fortran_ext_match(source):
                        language = 'f77'
        else:
            return language


    def has_f_sources(sources):
        """Return True if sources contains Fortran files """
        for source in sources:
            if fortran_ext_match(source):
                return True
        else:
            return False


    def has_cxx_sources(sources):
        """Return True if sources contains C++ files """
        for source in sources:
            if cxx_ext_match(source):
                return True
        else:
            return False


    def filter_sources(sources):
        """Return four lists of filenames containing
    C, C++, Fortran, and Fortran 90 module sources,
    respectively.
    """
        c_sources = []
        cxx_sources = []
        f_sources = []
        fmodule_sources = []
        for source in sources:
            if fortran_ext_match(source):
                modules = _get_f90_modules(source)
                if modules:
                    fmodule_sources.append(source)
                else:
                    f_sources.append(source)
            else:
                if cxx_ext_match(source):
                    cxx_sources.append(source)
                else:
                    c_sources.append(source)

        return (
         c_sources, cxx_sources, f_sources, fmodule_sources)


    def _get_headers(directory_list):
        headers = []
        for d in directory_list:
            head = sorted_glob(os.path.join(d, '*.h'))
            headers.extend(head)
        else:
            return headers


    def _get_directories(list_of_sources):
        direcs = []
        for f in list_of_sources:
            d = os.path.split(f)
            if d[0] != '':
                if d[0] not in direcs:
                    direcs.append(d[0])
        else:
            return direcs


    def _commandline_dep_string(cc_args, extra_postargs, pp_opts):
        """
    Return commandline representation used to determine if a file needs
    to be recompiled
    """
        cmdline = 'commandline: '
        cmdline += ' '.join(cc_args)
        cmdline += ' '.join(extra_postargs)
        cmdline += ' '.join(pp_opts) + '\n'
        return cmdline


    def get_dependencies(sources):
        return _get_headers(_get_directories(sources))


    def is_local_src_dir(directory):
        """Return true if directory is local directory.
    """
        if not is_string(directory):
            return False
        abs_dir = os.path.abspath(directory)
        c = os.path.commonprefix([os.getcwd(), abs_dir])
        new_dir = abs_dir[len(c):].split(os.sep)
        if new_dir:
            if not new_dir[0]:
                new_dir = new_dir[1:]
            if new_dir:
                if new_dir[0] == 'build':
                    return False
            new_dir = os.sep.join(new_dir)
            return os.path.isdir(new_dir)


    def general_source_files(top_path):
        pruned_directories = {'CVS':1,  '.svn':1,  'build':1}
        prune_file_pat = re.compile('(?:[~#]|\\.py[co]|\\.o)$')
        for dirpath, dirnames, filenames in os.walk(top_path, topdown=True):
            pruned = [d for d in dirnames if d not in pruned_directories]
            dirnames[:] = pruned
            for f in filenames:
                if not prune_file_pat.search(f):
                    yield os.path.join(dirpath, f)


    def general_source_directories_files(top_path):
        """Return a directory name relative to top_path and
    files contained.
    """
        pruned_directories = [
         'CVS', '.svn', 'build']
        prune_file_pat = re.compile('(?:[~#]|\\.py[co]|\\.o)$')
        for dirpath, dirnames, filenames in os.walk(top_path, topdown=True):
            pruned = [d for d in dirnames if d not in pruned_directories]
            dirnames[:] = pruned
            for d in dirnames:
                dpath = os.path.join(dirpath, d)
                rpath = rel_path(dpath, top_path)
                files = []
                for f in os.listdir(dpath):
                    fn = os.path.join(dpath, f)
                    if os.path.isfile(fn):
                        if not prune_file_pat.search(fn):
                            files.append(fn)
                    yield (
                     rpath, files)

        else:
            dpath = top_path
            rpath = rel_path(dpath, top_path)
            filenames = [os.path.join(dpath, f) for f in os.listdir(dpath) if not prune_file_pat.search(f)]
            files = [f for f in filenames if os.path.isfile(f)]
            yield (rpath, files)


    def get_ext_source_files(ext):
        filenames = []
        sources = [_m for _m in ext.sources if is_string(_m)]
        filenames.extend(sources)
        filenames.extend(get_dependencies(sources))
        for d in ext.depends:
            if is_local_src_dir(d):
                filenames.extend(list(general_source_files(d)))
            else:
                if os.path.isfile(d):
                    filenames.append(d)
        else:
            return filenames


    def get_script_files(scripts):
        scripts = [_m for _m in scripts if is_string(_m)]
        return scripts


    def get_lib_source_files(lib):
        filenames = []
        sources = lib[1].get('sources', [])
        sources = [_m for _m in sources if is_string(_m)]
        filenames.extend(sources)
        filenames.extend(get_dependencies(sources))
        depends = lib[1].get('depends', [])
        for d in depends:
            if is_local_src_dir(d):
                filenames.extend(list(general_source_files(d)))
            else:
                if os.path.isfile(d):
                    filenames.append(d)
        else:
            return filenames


    def get_shared_lib_extension(is_python_ext=False):
        """Return the correct file extension for shared libraries.

    Parameters
    ----------
    is_python_ext : bool, optional
        Whether the shared library is a Python extension.  Default is False.

    Returns
    -------
    so_ext : str
        The shared library extension.

    Notes
    -----
    For Python shared libs, `so_ext` will typically be '.so' on Linux and OS X,
    and '.pyd' on Windows.  For Python >= 3.2 `so_ext` has a tag prepended on
    POSIX systems according to PEP 3149.  For Python 3.2 this is implemented on
    Linux, but not on OS X.

    """
        confvars = distutils.sysconfig.get_config_vars()
        so_ext = confvars.get('EXT_SUFFIX', None)
        if so_ext is None:
            so_ext = confvars.get('SO', '')
        if is_python_ext or sys.platform.startswith('linux') or sys.platform.startswith('gnukfreebsd'):
            so_ext = '.so'
        elif sys.platform.startswith('darwin'):
            so_ext = '.dylib'
        elif sys.platform.startswith('win'):
            so_ext = '.dll'
        elif 'SOABI' in confvars:
            so_ext = so_ext.replace('.' + confvars.get('SOABI'), '', 1)
        return so_ext


    def get_data_files(data):
        if is_string(data):
            return [data]
        sources = data[1]
        filenames = []
        for s in sources:
            if hasattr(s, '__call__'):
                pass
            else:
                if is_local_src_dir(s):
                    filenames.extend(list(general_source_files(s)))
                else:
                    if is_string(s):
                        if os.path.isfile(s):
                            filenames.append(s)
                        else:
                            print('Not existing data file:', s)
                    else:
                        raise TypeError(repr(s))

        return filenames


    def dot_join(*args):
        return '.'.join([a for a in args if a])


    def get_frame(level=0):
        """Return frame object from call stack with given level.
    """
        try:
            return sys._getframe(level + 1)
        except AttributeError:
            frame = sys.exc_info()[2].tb_frame
            for _ in range(level + 1):
                frame = frame.f_back

            return frame


    class Configuration:
        _list_keys = [
         'packages', 'ext_modules', 'data_files', 'include_dirs',
         'libraries', 'headers', 'scripts', 'py_modules',
         'installed_libraries', 'define_macros']
        _dict_keys = ['package_dir', 'installed_pkg_config']
        _extra_keys = ['name', 'version']
        numpy_include_dirs = []

        def __init__--- This code section failed: ---

 L. 758         0  LOAD_GLOBAL              dot_join
                2  LOAD_FAST                'parent_name'
                4  LOAD_FAST                'package_name'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               name

 L. 759        12  LOAD_CONST               None
               14  LOAD_FAST                'self'
               16  STORE_ATTR               version

 L. 761        18  LOAD_GLOBAL              get_frame
               20  LOAD_FAST                'caller_level'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'caller_frame'

 L. 762        26  LOAD_GLOBAL              get_path_from_frame
               28  LOAD_FAST                'caller_frame'
               30  LOAD_FAST                'top_path'
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_FAST                'self'
               36  STORE_ATTR               local_path

 L. 767        38  LOAD_FAST                'top_path'
               40  LOAD_CONST               None
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    58  'to 58'

 L. 768        46  LOAD_FAST                'self'
               48  LOAD_ATTR                local_path
               50  STORE_FAST               'top_path'

 L. 769        52  LOAD_STR                 ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               local_path
             58_0  COME_FROM            44  '44'

 L. 770        58  LOAD_FAST                'package_path'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 771        66  LOAD_FAST                'self'
               68  LOAD_ATTR                local_path
               70  STORE_FAST               'package_path'
               72  JUMP_FORWARD        106  'to 106'
             74_0  COME_FROM            64  '64'

 L. 772        74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              isdir
               80  LOAD_GLOBAL              njoin
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                local_path
               86  LOAD_FAST                'package_path'
               88  CALL_FUNCTION_2       2  ''
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L. 773        94  LOAD_GLOBAL              njoin
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                local_path
              100  LOAD_FAST                'package_path'
              102  CALL_FUNCTION_2       2  ''
              104  STORE_FAST               'package_path'
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            72  '72'

 L. 774       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              isdir
              112  LOAD_FAST                'package_path'
              114  JUMP_IF_TRUE_OR_POP   118  'to 118'
              116  LOAD_STR                 '.'
            118_0  COME_FROM           114  '114'
              118  CALL_METHOD_1         1  ''
              120  POP_JUMP_IF_TRUE    136  'to 136'

 L. 775       122  LOAD_GLOBAL              ValueError
              124  LOAD_STR                 '%r is not a directory'
              126  LOAD_FAST                'package_path'
              128  BUILD_TUPLE_1         1 
              130  BINARY_MODULO    
              132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           120  '120'

 L. 776       136  LOAD_FAST                'top_path'
              138  LOAD_FAST                'self'
              140  STORE_ATTR               top_path

 L. 777       142  LOAD_FAST                'package_path'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               package_path

 L. 779       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_ATTR                join
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                name
              158  LOAD_METHOD              split
              160  LOAD_STR                 '.'
              162  CALL_METHOD_1         1  ''
              164  CALL_FUNCTION_EX      0  'positional arguments only'
              166  LOAD_FAST                'self'
              168  STORE_ATTR               path_in_package

 L. 781       170  LOAD_FAST                'self'
              172  LOAD_ATTR                _list_keys
              174  LOAD_CONST               None
              176  LOAD_CONST               None
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  LOAD_FAST                'self'
              184  STORE_ATTR               list_keys

 L. 782       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _dict_keys
              190  LOAD_CONST               None
              192  LOAD_CONST               None
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'self'
              200  STORE_ATTR               dict_keys

 L. 784       202  LOAD_FAST                'self'
              204  LOAD_ATTR                list_keys
              206  GET_ITER         
            208_0  COME_FROM           246  '246'
              208  FOR_ITER            248  'to 248'
              210  STORE_FAST               'n'

 L. 785       212  LOAD_GLOBAL              copy
              214  LOAD_METHOD              copy
              216  LOAD_FAST                'attrs'
              218  LOAD_METHOD              get
              220  LOAD_FAST                'n'
              222  BUILD_LIST_0          0 
              224  CALL_METHOD_2         2  ''
              226  CALL_METHOD_1         1  ''
              228  STORE_FAST               'v'

 L. 786       230  LOAD_GLOBAL              setattr
              232  LOAD_FAST                'self'
              234  LOAD_FAST                'n'
              236  LOAD_GLOBAL              as_list
              238  LOAD_FAST                'v'
              240  CALL_FUNCTION_1       1  ''
              242  CALL_FUNCTION_3       3  ''
              244  POP_TOP          
              246  JUMP_BACK           208  'to 208'
            248_0  COME_FROM           208  '208'

 L. 788       248  LOAD_FAST                'self'
              250  LOAD_ATTR                dict_keys
              252  GET_ITER         
            254_0  COME_FROM           288  '288'
              254  FOR_ITER            290  'to 290'
              256  STORE_FAST               'n'

 L. 789       258  LOAD_GLOBAL              copy
              260  LOAD_METHOD              copy
              262  LOAD_FAST                'attrs'
              264  LOAD_METHOD              get
              266  LOAD_FAST                'n'
              268  BUILD_MAP_0           0 
              270  CALL_METHOD_2         2  ''
              272  CALL_METHOD_1         1  ''
              274  STORE_FAST               'v'

 L. 790       276  LOAD_GLOBAL              setattr
              278  LOAD_FAST                'self'
              280  LOAD_FAST                'n'
              282  LOAD_FAST                'v'
              284  CALL_FUNCTION_3       3  ''
              286  POP_TOP          
              288  JUMP_BACK           254  'to 254'
            290_0  COME_FROM           254  '254'

 L. 792       290  LOAD_FAST                'self'
              292  LOAD_ATTR                list_keys
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                dict_keys
              298  BINARY_ADD       
              300  STORE_FAST               'known_keys'

 L. 793       302  LOAD_FAST                'self'
              304  LOAD_ATTR                _extra_keys
              306  LOAD_CONST               None
              308  LOAD_CONST               None
              310  BUILD_SLICE_2         2 
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'self'
              316  STORE_ATTR               extra_keys

 L. 794       318  LOAD_FAST                'attrs'
              320  LOAD_METHOD              keys
              322  CALL_METHOD_0         0  ''
              324  GET_ITER         
            326_0  COME_FROM           428  '428'
            326_1  COME_FROM           414  '414'
            326_2  COME_FROM           388  '388'
            326_3  COME_FROM           340  '340'
              326  FOR_ITER            432  'to 432'
              328  STORE_FAST               'n'

 L. 795       330  LOAD_FAST                'n'
              332  LOAD_FAST                'known_keys'
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   344  'to 344'

 L. 796   340_342  JUMP_BACK           326  'to 326'
            344_0  COME_FROM           336  '336'

 L. 797       344  LOAD_FAST                'attrs'
              346  LOAD_FAST                'n'
              348  BINARY_SUBSCR    
              350  STORE_FAST               'a'

 L. 798       352  LOAD_GLOBAL              setattr
              354  LOAD_FAST                'self'
              356  LOAD_FAST                'n'
              358  LOAD_FAST                'a'
              360  CALL_FUNCTION_3       3  ''
              362  POP_TOP          

 L. 799       364  LOAD_GLOBAL              isinstance
              366  LOAD_FAST                'a'
              368  LOAD_GLOBAL              list
              370  CALL_FUNCTION_2       2  ''
          372_374  POP_JUMP_IF_FALSE   390  'to 390'

 L. 800       376  LOAD_FAST                'self'
              378  LOAD_ATTR                list_keys
              380  LOAD_METHOD              append
              382  LOAD_FAST                'n'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          
              388  JUMP_BACK           326  'to 326'
            390_0  COME_FROM           372  '372'

 L. 801       390  LOAD_GLOBAL              isinstance
              392  LOAD_FAST                'a'
              394  LOAD_GLOBAL              dict
              396  CALL_FUNCTION_2       2  ''
          398_400  POP_JUMP_IF_FALSE   416  'to 416'

 L. 802       402  LOAD_FAST                'self'
              404  LOAD_ATTR                dict_keys
              406  LOAD_METHOD              append
              408  LOAD_FAST                'n'
              410  CALL_METHOD_1         1  ''
              412  POP_TOP          
              414  JUMP_BACK           326  'to 326'
            416_0  COME_FROM           398  '398'

 L. 804       416  LOAD_FAST                'self'
              418  LOAD_ATTR                extra_keys
              420  LOAD_METHOD              append
              422  LOAD_FAST                'n'
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          
          428_430  JUMP_BACK           326  'to 326'
            432_0  COME_FROM           326  '326'

 L. 806       432  LOAD_GLOBAL              os
              434  LOAD_ATTR                path
              436  LOAD_METHOD              exists
              438  LOAD_GLOBAL              njoin
              440  LOAD_FAST                'package_path'
              442  LOAD_STR                 '__init__.py'
              444  CALL_FUNCTION_2       2  ''
              446  CALL_METHOD_1         1  ''
          448_450  POP_JUMP_IF_FALSE   478  'to 478'

 L. 807       452  LOAD_FAST                'self'
              454  LOAD_ATTR                packages
              456  LOAD_METHOD              append
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                name
              462  CALL_METHOD_1         1  ''
              464  POP_TOP          

 L. 808       466  LOAD_FAST                'package_path'
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                package_dir
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                name
              476  STORE_SUBSCR     
            478_0  COME_FROM           448  '448'

 L. 810       478  LOAD_GLOBAL              dict

 L. 811       480  LOAD_CONST               False

 L. 812       482  LOAD_CONST               False

 L. 813       484  LOAD_CONST               False

 L. 814       486  LOAD_CONST               False

 L. 810       488  LOAD_CONST               ('ignore_setup_xxx_py', 'assume_default_configuration', 'delegate_options_to_subpackages', 'quiet')
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              492  LOAD_FAST                'self'
              494  STORE_ATTR               options

 L. 817       496  LOAD_CONST               None
              498  STORE_FAST               'caller_instance'

 L. 818       500  LOAD_GLOBAL              range
              502  LOAD_CONST               1
              504  LOAD_CONST               3
              506  CALL_FUNCTION_2       2  ''
              508  GET_ITER         
            510_0  COME_FROM           610  '610'
            510_1  COME_FROM           606  '606'
            510_2  COME_FROM           586  '586'
              510  FOR_ITER            614  'to 614'
              512  STORE_FAST               'i'

 L. 819       514  SETUP_FINALLY       528  'to 528'

 L. 820       516  LOAD_GLOBAL              get_frame
              518  LOAD_FAST                'i'
              520  CALL_FUNCTION_1       1  ''
              522  STORE_FAST               'f'
              524  POP_BLOCK        
              526  JUMP_FORWARD        558  'to 558'
            528_0  COME_FROM_FINALLY   514  '514'

 L. 821       528  DUP_TOP          
              530  LOAD_GLOBAL              ValueError
              532  COMPARE_OP               exception-match
          534_536  POP_JUMP_IF_FALSE   556  'to 556'
              538  POP_TOP          
              540  POP_TOP          
              542  POP_TOP          

 L. 822       544  POP_EXCEPT       
              546  POP_TOP          
          548_550  JUMP_FORWARD        614  'to 614'
              552  POP_EXCEPT       
              554  JUMP_FORWARD        558  'to 558'
            556_0  COME_FROM           534  '534'
              556  END_FINALLY      
            558_0  COME_FROM           554  '554'
            558_1  COME_FROM           526  '526'

 L. 823       558  SETUP_FINALLY       588  'to 588'

 L. 824       560  LOAD_GLOBAL              eval
              562  LOAD_STR                 'self'
              564  LOAD_FAST                'f'
              566  LOAD_ATTR                f_globals
              568  LOAD_FAST                'f'
              570  LOAD_ATTR                f_locals
              572  CALL_FUNCTION_3       3  ''
              574  STORE_FAST               'caller_instance'

 L. 825       576  POP_BLOCK        
              578  POP_TOP          
          580_582  JUMP_FORWARD        614  'to 614'
              584  POP_BLOCK        
              586  JUMP_BACK           510  'to 510'
            588_0  COME_FROM_FINALLY   558  '558'

 L. 826       588  DUP_TOP          
              590  LOAD_GLOBAL              NameError
              592  COMPARE_OP               exception-match
          594_596  POP_JUMP_IF_FALSE   608  'to 608'
              598  POP_TOP          
              600  POP_TOP          
              602  POP_TOP          

 L. 827       604  POP_EXCEPT       
              606  JUMP_BACK           510  'to 510'
            608_0  COME_FROM           594  '594'
              608  END_FINALLY      
          610_612  JUMP_BACK           510  'to 510'
            614_0  COME_FROM           580  '580'
            614_1  COME_FROM           548  '548'
            614_2  COME_FROM           510  '510'

 L. 828       614  LOAD_GLOBAL              isinstance
              616  LOAD_FAST                'caller_instance'
              618  LOAD_FAST                'self'
              620  LOAD_ATTR                __class__
              622  CALL_FUNCTION_2       2  ''
          624_626  POP_JUMP_IF_FALSE   654  'to 654'

 L. 829       628  LOAD_FAST                'caller_instance'
              630  LOAD_ATTR                options
              632  LOAD_STR                 'delegate_options_to_subpackages'
              634  BINARY_SUBSCR    
          636_638  POP_JUMP_IF_FALSE   654  'to 654'

 L. 830       640  LOAD_FAST                'self'
              642  LOAD_ATTR                set_options
              644  BUILD_TUPLE_0         0 
              646  LOAD_FAST                'caller_instance'
              648  LOAD_ATTR                options
              650  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              652  POP_TOP          
            654_0  COME_FROM           636  '636'
            654_1  COME_FROM           624  '624'

 L. 832       654  LOAD_FAST                'setup_name'
              656  LOAD_FAST                'self'
              658  STORE_ATTR               setup_name

Parse error at or near `JUMP_FORWARD' instruction at offset 548_550

        def todict(self):
            """
        Return a dictionary compatible with the keyword arguments of distutils
        setup function.

        Examples
        --------
        >>> setup(**config.todict())                           #doctest: +SKIP
        """
            self._optimize_data_files()
            d = {}
            known_keys = self.list_keys + self.dict_keys + self.extra_keys
            for n in known_keys:
                a = getattr(self, n)
                if a:
                    d[n] = a
            else:
                return d

        def info(self, message):
            if not self.options['quiet']:
                print(message)

        def warn(self, message):
            sys.stderr.write('Warning: %s\n' % (message,))

        def set_options(self, **options):
            """
        Configure Configuration instance.

        The following options are available:
         - ignore_setup_xxx_py
         - assume_default_configuration
         - delegate_options_to_subpackages
         - quiet

        """
            for key, value in options.items():
                if key in self.options:
                    self.options[key] = value
                else:
                    raise ValueError('Unknown option: ' + key)

        def get_distribution(self):
            """Return the distutils distribution object for self."""
            from numpy.distutils.core import get_distribution
            return get_distribution()

        def _wildcard_get_subpackage(self, subpackage_name, parent_name, caller_level=1):
            l = subpackage_name.split('.')
            subpackage_path = njoin([self.local_path] + l)
            dirs = [_m for _m in sorted_glob(subpackage_path) if os.path.isdir(_m)]
            config_list = []
            for d in dirs:
                if not os.path.isfile(njoin(d, '__init__.py')):
                    pass
                else:
                    if 'build' in d.split(os.sep):
                        pass
                    else:
                        n = '.'.join(d.split(os.sep)[-len(l):])
                        c = self.get_subpackage(n, parent_name=parent_name,
                          caller_level=(caller_level + 1))
                        config_list.extend(c)
            else:
                return config_list

        def _get_configuration_from_setup_py(self, setup_py, subpackage_name, subpackage_path, parent_name, caller_level=1):
            sys.path.insert(0, os.path.dirname(setup_py))
            try:
                setup_name = os.path.splitext(os.path.basename(setup_py))[0]
                n = dot_join(self.name, subpackage_name, setup_name)
                setup_module = npy_load_module('_'.join(n.split('.')), setup_py, ('.py',
                                                                                  'U',
                                                                                  1))
                if not hasattr(setup_module, 'configuration'):
                    if not self.options['assume_default_configuration']:
                        self.warn('Assuming default configuration (%s does not define configuration())' % setup_module)
                    config = Configuration(subpackage_name, parent_name, (self.top_path),
                      subpackage_path, caller_level=(caller_level + 1))
                else:
                    pn = dot_join(*[parent_name] + subpackage_name.split('.')[:-1])
                    args = (pn,)
                    if setup_module.configuration.__code__.co_argcount > 1:
                        args = args + (self.top_path,)
                    config = (setup_module.configuration)(*args)
                if config.name != dot_join(parent_name, subpackage_name):
                    self.warn('Subpackage %r configuration returned as %r' % (
                     dot_join(parent_name, subpackage_name), config.name))
            finally:
                del sys.path[0]

            return config

        def get_subpackage(self, subpackage_name, subpackage_path=None, parent_name=None, caller_level=1):
            """Return list of subpackage configurations.

        Parameters
        ----------
        subpackage_name : str or None
            Name of the subpackage to get the configuration. '*' in
            subpackage_name is handled as a wildcard.
        subpackage_path : str
            If None, then the path is assumed to be the local path plus the
            subpackage_name. If a setup.py file is not found in the
            subpackage_path, then a default configuration is used.
        parent_name : str
            Parent name.
        """
            if subpackage_name is None:
                if subpackage_path is None:
                    raise ValueError('either subpackage_name or subpackage_path must be specified')
                subpackage_name = os.path.basename(subpackage_path)
            l = subpackage_name.split('.')
            if subpackage_path is None:
                if '*' in subpackage_name:
                    return self._wildcard_get_subpackage(subpackage_name, parent_name,
                      caller_level=(caller_level + 1))
            assert '*' not in subpackage_name, repr((subpackage_name, subpackage_path, parent_name))
            if subpackage_path is None:
                subpackage_path = njoin([self.local_path] + l)
            else:
                subpackage_path = njoin([subpackage_path] + l[:-1])
                subpackage_path = self.paths([subpackage_path])[0]
            setup_py = njoin(subpackage_path, self.setup_name)
            if not self.options['ignore_setup_xxx_py']:
                if not os.path.isfile(setup_py):
                    setup_py = njoin(subpackage_path, 'setup_%s.py' % subpackage_name)
                if not os.path.isfile(setup_py):
                    if not self.options['assume_default_configuration']:
                        self.warn('Assuming default configuration (%s/{setup_%s,setup}.py was not found)' % (
                         os.path.dirname(setup_py), subpackage_name))
                    config = Configuration(subpackage_name, parent_name, (self.top_path),
                      subpackage_path, caller_level=(caller_level + 1))
                else:
                    config = self._get_configuration_from_setup_py(setup_py,
                      subpackage_name,
                      subpackage_path,
                      parent_name,
                      caller_level=(caller_level + 1))
                if config:
                    return [config]
                return []

        def add_subpackage(self, subpackage_name, subpackage_path=None, standalone=False):
            """Add a sub-package to the current Configuration instance.

        This is useful in a setup.py script for adding sub-packages to a
        package.

        Parameters
        ----------
        subpackage_name : str
            name of the subpackage
        subpackage_path : str
            if given, the subpackage path such as the subpackage is in
            subpackage_path / subpackage_name. If None,the subpackage is
            assumed to be located in the local path / subpackage_name.
        standalone : bool
        """
            if standalone:
                parent_name = None
            else:
                parent_name = self.name
            config_list = self.get_subpackage(subpackage_name, subpackage_path, parent_name=parent_name,
              caller_level=2)
            if not config_list:
                self.warn('No configuration returned, assuming unavailable.')
            for config in config_list:
                d = config
                if isinstance(config, Configuration):
                    d = config.todict()
                else:
                    assert isinstance(d, dict), repr(type(d))
                    self.info('Appending %s configuration to %s' % (
                     d.get('name'), self.name))
                    (self.dict_append)(**d)
            else:
                dist = self.get_distribution()
                if dist is not None:
                    self.warn('distutils distribution has been initialized, it may be too late to add a subpackage ' + subpackage_name)

        def add_data_dir(self, data_path):
            """Recursively add files under data_path to data_files list.

        Recursively add files under data_path to the list of data_files to be
        installed (and distributed). The data_path can be either a relative
        path-name, or an absolute path-name, or a 2-tuple where the first
        argument shows where in the install directory the data directory
        should be installed to.

        Parameters
        ----------
        data_path : seq or str
            Argument can be either

                * 2-sequence (<datadir suffix>, <path to data directory>)
                * path to data directory where python datadir suffix defaults
                  to package dir.

        Notes
        -----
        Rules for installation paths::

            foo/bar -> (foo/bar, foo/bar) -> parent/foo/bar
            (gun, foo/bar) -> parent/gun
            foo/* -> (foo/a, foo/a), (foo/b, foo/b) -> parent/foo/a, parent/foo/b
            (gun, foo/*) -> (gun, foo/a), (gun, foo/b) -> gun
            (gun/*, foo/*) -> parent/gun/a, parent/gun/b
            /foo/bar -> (bar, /foo/bar) -> parent/bar
            (gun, /foo/bar) -> parent/gun
            (fun/*/gun/*, sun/foo/bar) -> parent/fun/foo/gun/bar

        Examples
        --------
        For example suppose the source directory contains fun/foo.dat and
        fun/bar/car.dat:

        >>> self.add_data_dir('fun')                       #doctest: +SKIP
        >>> self.add_data_dir(('sun', 'fun'))              #doctest: +SKIP
        >>> self.add_data_dir(('gun', '/full/path/to/fun'))#doctest: +SKIP

        Will install data-files to the locations::

            <package install directory>/
              fun/
                foo.dat
                bar/
                  car.dat
              sun/
                foo.dat
                bar/
                  car.dat
              gun/
                foo.dat
                car.dat

        """
            if is_sequence(data_path):
                d, data_path = data_path
            else:
                d = None
            if is_sequence(data_path):
                [self.add_data_dir((d, p)) for p in data_path]
                return
            if not is_string(data_path):
                raise TypeError('not a string: %r' % (data_path,))
            if d is None:
                if os.path.isabs(data_path):
                    return self.add_data_dir((os.path.basename(data_path), data_path))
                return self.add_data_dir((data_path, data_path))
            paths = self.paths(data_path, include_non_existing=False)
            if is_glob_pattern(data_path):
                if is_glob_pattern(d):
                    pattern_list = allpath(d).split(os.sep)
                    pattern_list.reverse()
                    rl = list(range(len(pattern_list) - 1))
                    rl.reverse()
                    for i in rl:
                        if not pattern_list[i]:
                            del pattern_list[i]
                    else:
                        for path in paths:
                            if not os.path.isdir(path):
                                print('Not a directory, skipping', path)
                            else:
                                rpath = rel_path(path, self.local_path)
                                path_list = rpath.split(os.sep)
                                path_list.reverse()
                                target_list = []
                                i = 0
                                for s in pattern_list:
                                    if is_glob_pattern(s):
                                        if i >= len(path_list):
                                            raise ValueError('cannot fill pattern %r with %r' % (
                                             d, path))
                                        target_list.append(path_list[i])
                                    else:
                                        assert s == path_list[i], repr((s, path_list[i], data_path, d, path, rpath))
                                        target_list.append(s)
                                    i += 1
                                else:
                                    if path_list[i:]:
                                        self.warn('mismatch of pattern_list=%s and path_list=%s' % (
                                         pattern_list, path_list))
                                    target_list.reverse()
                                    self.add_data_dir((os.sep.join(target_list), path))

                else:
                    pass
                for path in paths:
                    self.add_data_dir((d, path))
                else:
                    return

            if is_glob_pattern(d):
                raise AssertionError(repr(d))
            dist = self.get_distribution()
            if dist is not None and dist.data_files is not None:
                data_files = dist.data_files
            else:
                data_files = self.data_files
            for path in paths:
                for d1, f in list(general_source_directories_files(path)):
                    target_path = os.path.join(self.path_in_package, d, d1)
                    data_files.append((target_path, f))

        def _optimize_data_files(self):
            data_dict = {}
            for p, files in self.data_files:
                if p not in data_dict:
                    data_dict[p] = set()
                else:
                    for f in files:
                        data_dict[p].add(f)

            else:
                self.data_files[:] = [(
                 p, list(files)) for p, files in data_dict.items()]

        def add_data_files(self, *files):
            r"""Add data files to configuration data_files.

        Parameters
        ----------
        files : sequence
            Argument(s) can be either

                * 2-sequence (<datadir prefix>,<path to data file(s)>)
                * paths to data files where python datadir prefix defaults
                  to package dir.

        Notes
        -----
        The form of each element of the files sequence is very flexible
        allowing many combinations of where to get the files from the package
        and where they should ultimately be installed on the system. The most
        basic usage is for an element of the files argument sequence to be a
        simple filename. This will cause that file from the local path to be
        installed to the installation path of the self.name package (package
        path). The file argument can also be a relative path in which case the
        entire relative path will be installed into the package directory.
        Finally, the file can be an absolute path name in which case the file
        will be found at the absolute path name but installed to the package
        path.

        This basic behavior can be augmented by passing a 2-tuple in as the
        file argument. The first element of the tuple should specify the
        relative path (under the package install directory) where the
        remaining sequence of files should be installed to (it has nothing to
        do with the file-names in the source distribution). The second element
        of the tuple is the sequence of files that should be installed. The
        files in this sequence can be filenames, relative paths, or absolute
        paths. For absolute paths the file will be installed in the top-level
        package installation directory (regardless of the first argument).
        Filenames and relative path names will be installed in the package
        install directory under the path name given as the first element of
        the tuple.

        Rules for installation paths:

          #. file.txt -> (., file.txt)-> parent/file.txt
          #. foo/file.txt -> (foo, foo/file.txt) -> parent/foo/file.txt
          #. /foo/bar/file.txt -> (., /foo/bar/file.txt) -> parent/file.txt
          #. ``*``.txt -> parent/a.txt, parent/b.txt
          #. foo/``*``.txt`` -> parent/foo/a.txt, parent/foo/b.txt
          #. ``*/*.txt`` -> (``*``, ``*``/``*``.txt) -> parent/c/a.txt, parent/d/b.txt
          #. (sun, file.txt) -> parent/sun/file.txt
          #. (sun, bar/file.txt) -> parent/sun/file.txt
          #. (sun, /foo/bar/file.txt) -> parent/sun/file.txt
          #. (sun, ``*``.txt) -> parent/sun/a.txt, parent/sun/b.txt
          #. (sun, bar/``*``.txt) -> parent/sun/a.txt, parent/sun/b.txt
          #. (sun/``*``, ``*``/``*``.txt) -> parent/sun/c/a.txt, parent/d/b.txt

        An additional feature is that the path to a data-file can actually be
        a function that takes no arguments and returns the actual path(s) to
        the data-files. This is useful when the data files are generated while
        building the package.

        Examples
        --------
        Add files to the list of data_files to be included with the package.

            >>> self.add_data_files('foo.dat',
            ...     ('fun', ['gun.dat', 'nun/pun.dat', '/tmp/sun.dat']),
            ...     'bar/cat.dat',
            ...     '/full/path/to/can.dat')                   #doctest: +SKIP

        will install these data files to::

            <package install directory>/
             foo.dat
             fun/
               gun.dat
               nun/
                 pun.dat
             sun.dat
             bar/
               car.dat
             can.dat

        where <package install directory> is the package (or sub-package)
        directory such as '/usr/lib/python2.4/site-packages/mypackage' ('C:
        \Python2.4 \Lib \site-packages \mypackage') or
        '/usr/lib/python2.4/site- packages/mypackage/mysubpackage' ('C:
        \Python2.4 \Lib \site-packages \mypackage \mysubpackage').
        """
            if len(files) > 1:
                for f in files:
                    self.add_data_files(f)
                else:
                    return

            assert len(files) == 1
            if is_sequence(files[0]):
                d, files = files[0]
            else:
                d = None
            if is_string(files):
                filepat = files
            elif is_sequence(files):
                if len(files) == 1:
                    filepat = files[0]
                else:
                    for f in files:
                        self.add_data_files((d, f))
                    else:
                        return

            else:
                raise TypeError(repr(type(files)))
            if d is None:
                if hasattr(filepat, '__call__'):
                    d = ''
                elif os.path.isabs(filepat):
                    d = ''
                else:
                    d = os.path.dirname(filepat)
                self.add_data_files((d, files))
                return
            paths = self.paths(filepat, include_non_existing=False)
            if is_glob_pattern(filepat):
                if is_glob_pattern(d):
                    pattern_list = d.split(os.sep)
                    pattern_list.reverse()
                    for path in paths:
                        path_list = path.split(os.sep)
                        path_list.reverse()
                        path_list.pop()
                        target_list = []
                        i = 0
                        for s in pattern_list:
                            if is_glob_pattern(s):
                                target_list.append(path_list[i])
                                i += 1
                            else:
                                target_list.append(s)
                            target_list.reverse()
                            self.add_data_files((os.sep.join(target_list), path))

                else:
                    self.add_data_files((d, paths))
                return
            if is_glob_pattern(d):
                raise AssertionError(repr((d, filepat)))
            dist = self.get_distribution()
            if dist is not None and dist.data_files is not None:
                data_files = dist.data_files
            else:
                data_files = self.data_files
            data_files.append((os.path.join(self.path_in_package, d), paths))

        def add_define_macros(self, macros):
            """Add define macros to configuration

        Add the given sequence of macro name and value duples to the beginning
        of the define_macros list This list will be visible to all extension
        modules of the current package.
        """
            dist = self.get_distribution()
            if dist is not None:
                if not hasattr(dist, 'define_macros'):
                    dist.define_macros = []
                dist.define_macros.extend(macros)
            else:
                self.define_macros.extend(macros)

        def add_include_dirs(self, *paths):
            """Add paths to configuration include directories.

        Add the given sequence of paths to the beginning of the include_dirs
        list. This list will be visible to all extension modules of the
        current package.
        """
            include_dirs = self.paths(paths)
            dist = self.get_distribution()
            if dist is not None:
                if dist.include_dirs is None:
                    dist.include_dirs = []
                dist.include_dirs.extend(include_dirs)
            else:
                self.include_dirs.extend(include_dirs)

        def add_headers(self, *files):
            """Add installable headers to configuration.

        Add the given sequence of files to the beginning of the headers list.
        By default, headers will be installed under <python-
        include>/<self.name.replace('.','/')>/ directory. If an item of files
        is a tuple, then its first argument specifies the actual installation
        location relative to the <python-include> path.

        Parameters
        ----------
        files : str or seq
            Argument(s) can be either:

                * 2-sequence (<includedir suffix>,<path to header file(s)>)
                * path(s) to header file(s) where python includedir suffix will
                  default to package name.
        """
            headers = []
            for path in files:
                if is_string(path):
                    [headers.append((self.name, p)) for p in self.paths(path)]
                else:
                    if not isinstance(path, (tuple, list)) or len(path) != 2:
                        raise TypeError(repr(path))
                    [headers.append((path[0], p)) for p in self.paths(path[1])]
            else:
                dist = self.get_distribution()
                if dist is not None:
                    if dist.headers is None:
                        dist.headers = []
                    dist.headers.extend(headers)
                else:
                    self.headers.extend(headers)

        def paths(self, *paths, **kws):
            """Apply glob to paths and prepend local_path if needed.

        Applies glob.glob(...) to each path in the sequence (if needed) and
        pre-pends the local_path if needed. Because this is called on all
        source lists, this allows wildcard characters to be specified in lists
        of sources for extension modules and libraries and scripts and allows
        path-names be relative to the source directory.

        """
            include_non_existing = kws.get('include_non_existing', True)
            return gpaths(paths, local_path=(self.local_path),
              include_non_existing=include_non_existing)

        def _fix_paths_dict(self, kw):
            for k in kw.keys():
                v = kw[k]
                if k in ('sources', 'depends', 'include_dirs', 'library_dirs', 'module_dirs',
                         'extra_objects'):
                    new_v = self.paths(v)
                    kw[k] = new_v

        def add_extension(self, name, sources, **kw):
            """Add extension to configuration.

        Create and add an Extension instance to the ext_modules list. This
        method also takes the following optional keyword arguments that are
        passed on to the Extension constructor.

        Parameters
        ----------
        name : str
            name of the extension
        sources : seq
            list of the sources. The list of sources may contain functions
            (called source generators) which must take an extension instance
            and a build directory as inputs and return a source file or list of
            source files or None. If None is returned then no sources are
            generated. If the Extension instance has no sources after
            processing all source generators, then no extension module is
            built.
        include_dirs :
        define_macros :
        undef_macros :
        library_dirs :
        libraries :
        runtime_library_dirs :
        extra_objects :
        extra_compile_args :
        extra_link_args :
        extra_f77_compile_args :
        extra_f90_compile_args :
        export_symbols :
        swig_opts :
        depends :
            The depends list contains paths to files or directories that the
            sources of the extension module depend on. If any path in the
            depends list is newer than the extension module, then the module
            will be rebuilt.
        language :
        f2py_options :
        module_dirs :
        extra_info : dict or list
            dict or list of dict of keywords to be appended to keywords.

        Notes
        -----
        The self.paths(...) method is applied to all lists that may contain
        paths.
        """
            ext_args = copy.copy(kw)
            ext_args['name'] = dot_join(self.name, name)
            ext_args['sources'] = sources
            if 'extra_info' in ext_args:
                extra_info = ext_args['extra_info']
                del ext_args['extra_info']
                if isinstance(extra_info, dict):
                    extra_info = [
                     extra_info]
                for info in extra_info:
                    if not isinstance(info, dict):
                        raise AssertionError(repr(info))
                    else:
                        dict_append(ext_args, **info)

            self._fix_paths_dict(ext_args)
            libraries = ext_args.get('libraries', [])
            libnames = []
            ext_args['libraries'] = []
            for libname in libraries:
                if isinstance(libname, tuple):
                    self._fix_paths_dict(libname[1])
                else:
                    if '@' in libname:
                        lname, lpath = libname.split('@', 1)
                        lpath = os.path.abspath(njoin(self.local_path, lpath))
                        if os.path.isdir(lpath):
                            c = self.get_subpackage(None, lpath, caller_level=2)
                            if isinstance(c, Configuration):
                                c = c.todict()
                            for l in [l[0] for l in c.get('libraries', [])]:
                                llname = l.split('__OF__', 1)[0]
                                if llname == lname:
                                    c.pop('name', None)
                                    dict_append(ext_args, **c)
                                    break

                    libnames.append(libname)
            else:
                ext_args['libraries'] = libnames + ext_args['libraries']
                ext_args['define_macros'] = self.define_macros + ext_args.get('define_macros', [])
                from numpy.distutils.core import Extension
                ext = Extension(**ext_args)
                self.ext_modules.append(ext)
                dist = self.get_distribution()
                if dist is not None:
                    self.warn('distutils distribution has been initialized, it may be too late to add an extension ' + name)
                return ext

        def add_library(self, name, sources, **build_info):
            """
        Add library to configuration.

        Parameters
        ----------
        name : str
            Name of the extension.
        sources : sequence
            List of the sources. The list of sources may contain functions
            (called source generators) which must take an extension instance
            and a build directory as inputs and return a source file or list of
            source files or None. If None is returned then no sources are
            generated. If the Extension instance has no sources after
            processing all source generators, then no extension module is
            built.
        build_info : dict, optional
            The following keys are allowed:

                * depends
                * macros
                * include_dirs
                * extra_compiler_args
                * extra_f77_compile_args
                * extra_f90_compile_args
                * f2py_options
                * language

        """
            self._add_library(name, sources, None, build_info)
            dist = self.get_distribution()
            if dist is not None:
                self.warn('distutils distribution has been initialized, it may be too late to add a library ' + name)

        def _add_library(self, name, sources, install_dir, build_info):
            """Common implementation for add_library and add_installed_library. Do
        not use directly"""
            build_info = copy.copy(build_info)
            build_info['sources'] = sources
            if 'depends' not in build_info:
                build_info['depends'] = []
            self._fix_paths_dict(build_info)
            self.libraries.append((name, build_info))

        def add_installed_library(self, name, sources, install_dir, build_info=None):
            """
        Similar to add_library, but the specified library is installed.

        Most C libraries used with `distutils` are only used to build python
        extensions, but libraries built through this method will be installed
        so that they can be reused by third-party packages.

        Parameters
        ----------
        name : str
            Name of the installed library.
        sources : sequence
            List of the library's source files. See `add_library` for details.
        install_dir : str
            Path to install the library, relative to the current sub-package.
        build_info : dict, optional
            The following keys are allowed:

                * depends
                * macros
                * include_dirs
                * extra_compiler_args
                * extra_f77_compile_args
                * extra_f90_compile_args
                * f2py_options
                * language

        Returns
        -------
        None

        See Also
        --------
        add_library, add_npy_pkg_config, get_info

        Notes
        -----
        The best way to encode the options required to link against the specified
        C libraries is to use a "libname.ini" file, and use `get_info` to
        retrieve the required options (see `add_npy_pkg_config` for more
        information).

        """
            if not build_info:
                build_info = {}
            install_dir = os.path.join(self.package_path, install_dir)
            self._add_library(name, sources, install_dir, build_info)
            self.installed_libraries.append(InstallableLib(name, build_info, install_dir))

        def add_npy_pkg_config(self, template, install_dir, subst_dict=None):
            """
        Generate and install a npy-pkg config file from a template.

        The config file generated from `template` is installed in the
        given install directory, using `subst_dict` for variable substitution.

        Parameters
        ----------
        template : str
            The path of the template, relatively to the current package path.
        install_dir : str
            Where to install the npy-pkg config file, relatively to the current
            package path.
        subst_dict : dict, optional
            If given, any string of the form ``@key@`` will be replaced by
            ``subst_dict[key]`` in the template file when installed. The install
            prefix is always available through the variable ``@prefix@``, since the
            install prefix is not easy to get reliably from setup.py.

        See also
        --------
        add_installed_library, get_info

        Notes
        -----
        This works for both standard installs and in-place builds, i.e. the
        ``@prefix@`` refer to the source directory for in-place builds.

        Examples
        --------
        ::

            config.add_npy_pkg_config('foo.ini.in', 'lib', {'foo': bar})

        Assuming the foo.ini.in file has the following content::

            [meta]
            Name=@foo@
            Version=1.0
            Description=dummy description

            [default]
            Cflags=-I@prefix@/include
            Libs=

        The generated file will have the following content::

            [meta]
            Name=bar
            Version=1.0
            Description=dummy description

            [default]
            Cflags=-Iprefix_dir/include
            Libs=

        and will be installed as foo.ini in the 'lib' subpath.

        When cross-compiling with numpy distutils, it might be necessary to
        use modified npy-pkg-config files.  Using the default/generated files
        will link with the host libraries (i.e. libnpymath.a).  For
        cross-compilation you of-course need to link with target libraries,
        while using the host Python installation.

        You can copy out the numpy/core/lib/npy-pkg-config directory, add a
        pkgdir value to the .ini files and set NPY_PKG_CONFIG_PATH environment
        variable to point to the directory with the modified npy-pkg-config
        files.

        Example npymath.ini modified for cross-compilation::

            [meta]
            Name=npymath
            Description=Portable, core math library implementing C99 standard
            Version=0.1

            [variables]
            pkgname=numpy.core
            pkgdir=/build/arm-linux-gnueabi/sysroot/usr/lib/python3.7/site-packages/numpy/core
            prefix=${pkgdir}
            libdir=${prefix}/lib
            includedir=${prefix}/include

            [default]
            Libs=-L${libdir} -lnpymath
            Cflags=-I${includedir}
            Requires=mlib

            [msvc]
            Libs=/LIBPATH:${libdir} npymath.lib
            Cflags=/INCLUDE:${includedir}
            Requires=mlib

        """
            if subst_dict is None:
                subst_dict = {}
            template = os.path.join(self.package_path, template)
            if self.name in self.installed_pkg_config:
                self.installed_pkg_config[self.name].append((template, install_dir,
                 subst_dict))
            else:
                self.installed_pkg_config[self.name] = [
                 (
                  template, install_dir,
                  subst_dict)]

        def add_scripts(self, *files):
            """Add scripts to configuration.

        Add the sequence of files to the beginning of the scripts list.
        Scripts will be installed under the <prefix>/bin/ directory.

        """
            scripts = self.paths(files)
            dist = self.get_distribution()
            if dist is not None:
                if dist.scripts is None:
                    dist.scripts = []
                dist.scripts.extend(scripts)
            else:
                self.scripts.extend(scripts)

        def dict_append--- This code section failed: ---

 L.1741         0  LOAD_FAST                'self'
                2  LOAD_ATTR                list_keys
                4  GET_ITER         
              6_0  COME_FROM            38  '38'
                6  FOR_ITER             40  'to 40'
                8  STORE_FAST               'key'

 L.1742        10  LOAD_GLOBAL              getattr
               12  LOAD_FAST                'self'
               14  LOAD_FAST                'key'
               16  CALL_FUNCTION_2       2  ''
               18  STORE_FAST               'a'

 L.1743        20  LOAD_FAST                'a'
               22  LOAD_METHOD              extend
               24  LOAD_FAST                'dict'
               26  LOAD_METHOD              get
               28  LOAD_FAST                'key'
               30  BUILD_LIST_0          0 
               32  CALL_METHOD_2         2  ''
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK             6  'to 6'
             40_0  COME_FROM             6  '6'

 L.1744        40  LOAD_FAST                'self'
               42  LOAD_ATTR                dict_keys
               44  GET_ITER         
             46_0  COME_FROM            78  '78'
               46  FOR_ITER             80  'to 80'
               48  STORE_FAST               'key'

 L.1745        50  LOAD_GLOBAL              getattr
               52  LOAD_FAST                'self'
               54  LOAD_FAST                'key'
               56  CALL_FUNCTION_2       2  ''
               58  STORE_FAST               'a'

 L.1746        60  LOAD_FAST                'a'
               62  LOAD_METHOD              update
               64  LOAD_FAST                'dict'
               66  LOAD_METHOD              get
               68  LOAD_FAST                'key'
               70  BUILD_MAP_0           0 
               72  CALL_METHOD_2         2  ''
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_BACK            46  'to 46'
             80_0  COME_FROM            46  '46'

 L.1747        80  LOAD_FAST                'self'
               82  LOAD_ATTR                list_keys
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                dict_keys
               88  BINARY_ADD       
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                extra_keys
               94  BINARY_ADD       
               96  STORE_FAST               'known_keys'

 L.1748        98  LOAD_FAST                'dict'
              100  LOAD_METHOD              keys
              102  CALL_METHOD_0         0  ''
              104  GET_ITER         
            106_0  COME_FROM           276  '276'
            106_1  COME_FROM           262  '262'
            106_2  COME_FROM           250  '250'
            106_3  COME_FROM           208  '208'
            106_4  COME_FROM           146  '146'
              106  FOR_ITER            278  'to 278'
              108  STORE_FAST               'key'

 L.1749       110  LOAD_FAST                'key'
              112  LOAD_FAST                'known_keys'
              114  COMPARE_OP               not-in
              116  POP_JUMP_IF_FALSE   210  'to 210'

 L.1750       118  LOAD_GLOBAL              getattr
              120  LOAD_FAST                'self'
              122  LOAD_FAST                'key'
              124  LOAD_CONST               None
              126  CALL_FUNCTION_3       3  ''
              128  STORE_FAST               'a'

 L.1751       130  LOAD_FAST                'a'
              132  POP_JUMP_IF_FALSE   148  'to 148'
              134  LOAD_FAST                'a'
              136  LOAD_FAST                'dict'
              138  LOAD_FAST                'key'
              140  BINARY_SUBSCR    
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   148  'to 148'

 L.1751       146  JUMP_BACK           106  'to 106'
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           132  '132'

 L.1752       148  LOAD_FAST                'self'
              150  LOAD_METHOD              warn
              152  LOAD_STR                 'Inheriting attribute %r=%r from %r'

 L.1753       154  LOAD_FAST                'key'
              156  LOAD_FAST                'dict'
              158  LOAD_FAST                'key'
              160  BINARY_SUBSCR    
              162  LOAD_FAST                'dict'
              164  LOAD_METHOD              get
              166  LOAD_STR                 'name'
              168  LOAD_STR                 '?'
              170  CALL_METHOD_2         2  ''
              172  BUILD_TUPLE_3         3 

 L.1752       174  BINARY_MODULO    
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.1754       180  LOAD_GLOBAL              setattr
              182  LOAD_FAST                'self'
              184  LOAD_FAST                'key'
              186  LOAD_FAST                'dict'
              188  LOAD_FAST                'key'
              190  BINARY_SUBSCR    
              192  CALL_FUNCTION_3       3  ''
              194  POP_TOP          

 L.1755       196  LOAD_FAST                'self'
              198  LOAD_ATTR                extra_keys
              200  LOAD_METHOD              append
              202  LOAD_FAST                'key'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
              208  JUMP_BACK           106  'to 106'
            210_0  COME_FROM           116  '116'

 L.1756       210  LOAD_FAST                'key'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                extra_keys
              216  COMPARE_OP               in
              218  POP_JUMP_IF_FALSE   252  'to 252'

 L.1757       220  LOAD_FAST                'self'
              222  LOAD_METHOD              info
              224  LOAD_STR                 'Ignoring attempt to set %r (from %r to %r)'

 L.1758       226  LOAD_FAST                'key'
              228  LOAD_GLOBAL              getattr
              230  LOAD_FAST                'self'
              232  LOAD_FAST                'key'
              234  CALL_FUNCTION_2       2  ''
              236  LOAD_FAST                'dict'
              238  LOAD_FAST                'key'
              240  BINARY_SUBSCR    
              242  BUILD_TUPLE_3         3 

 L.1757       244  BINARY_MODULO    
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  JUMP_BACK           106  'to 106'
            252_0  COME_FROM           218  '218'

 L.1759       252  LOAD_FAST                'key'
              254  LOAD_FAST                'known_keys'
              256  COMPARE_OP               in
          258_260  POP_JUMP_IF_FALSE   264  'to 264'

 L.1761       262  JUMP_BACK           106  'to 106'
            264_0  COME_FROM           258  '258'

 L.1763       264  LOAD_GLOBAL              ValueError
              266  LOAD_STR                 "Don't know about key=%r"
              268  LOAD_FAST                'key'
              270  BINARY_MODULO    
              272  CALL_FUNCTION_1       1  ''
              274  RAISE_VARARGS_1       1  'exception instance'
              276  JUMP_BACK           106  'to 106'
            278_0  COME_FROM           106  '106'

Parse error at or near `LOAD_FAST' instruction at offset 210

        def __str__(self):
            from pprint import pformat
            known_keys = self.list_keys + self.dict_keys + self.extra_keys
            s = '<-----\n'
            s += 'Configuration of ' + self.name + ':\n'
            known_keys.sort()
            for k in known_keys:
                a = getattr(self, k, None)
                if a:
                    s += '%s = %s\n' % (k, pformat(a))
            else:
                s += '----->'
                return s

        def get_config_cmd(self):
            """
        Returns the numpy.distutils config command instance.
        """
            cmd = get_cmd('config')
            cmd.ensure_finalized()
            cmd.dump_source = 0
            cmd.noisy = 0
            old_path = os.environ.get('PATH')
            if old_path:
                path = os.pathsep.join(['.', old_path])
                os.environ['PATH'] = path
            return cmd

        def get_build_temp_dir(self):
            """
        Return a path to a temporary directory where temporary files should be
        placed.
        """
            cmd = get_cmd('build')
            cmd.ensure_finalized()
            return cmd.build_temp

        def have_f77c(self):
            """Check for availability of Fortran 77 compiler.

        Use it inside source generating function to ensure that
        setup distribution instance has been initialized.

        Notes
        -----
        True if a Fortran 77 compiler is available (because a simple Fortran 77
        code was able to be compiled successfully).
        """
            simple_fortran_subroutine = '\n        subroutine simple\n        end\n        '
            config_cmd = self.get_config_cmd()
            flag = config_cmd.try_compile(simple_fortran_subroutine, lang='f77')
            return flag

        def have_f90c(self):
            """Check for availability of Fortran 90 compiler.

        Use it inside source generating function to ensure that
        setup distribution instance has been initialized.

        Notes
        -----
        True if a Fortran 90 compiler is available (because a simple Fortran
        90 code was able to be compiled successfully)
        """
            simple_fortran_subroutine = '\n        subroutine simple\n        end\n        '
            config_cmd = self.get_config_cmd()
            flag = config_cmd.try_compile(simple_fortran_subroutine, lang='f90')
            return flag

        def append_to(self, extlib):
            """Append libraries, include_dirs to extension or library item.
        """
            if is_sequence(extlib):
                lib_name, build_info = extlib
                dict_append(build_info, libraries=(self.libraries),
                  include_dirs=(self.include_dirs))
            else:
                from numpy.distutils.core import Extension
                assert isinstance(extlib, Extension), repr(extlib)
                extlib.libraries.extend(self.libraries)
                extlib.include_dirs.extend(self.include_dirs)

        def _get_svn_revision(self, path):
            """Return path's SVN revision number.
        """
            try:
                output = subprocess.check_output(['svnversion'], cwd=path)
            except (subprocess.CalledProcessError, OSError):
                pass
            else:
                m = re.match(b'(?P<revision>\\d+)', output)
                if m:
                    return int(m.group('revision'))
            if sys.platform == 'win32' and os.environ.get('SVN_ASP_DOT_NET_HACK', None):
                entries = njoin(path, '_svn', 'entries')
            else:
                entries = njoin(path, '.svn', 'entries')
            if os.path.isfile(entries):
                with open(entries) as f:
                    fstr = f.read()
                if fstr[:5] == '<?xml':
                    m = re.search('revision="(?P<revision>\\d+)"', fstr)
                    if m:
                        return int(m.group('revision'))
                else:
                    m = re.search('dir[\\n\\r]+(?P<revision>\\d+)', fstr)
                    if m:
                        return int(m.group('revision'))

        def _get_hg_revision--- This code section failed: ---

 L.1885         0  SETUP_FINALLY        26  'to 26'

 L.1886         2  LOAD_GLOBAL              subprocess
                4  LOAD_ATTR                check_output

 L.1887         6  LOAD_STR                 'hg'
                8  LOAD_STR                 'identify'
               10  LOAD_STR                 '--num'
               12  BUILD_LIST_3          3 

 L.1887        14  LOAD_FAST                'path'

 L.1886        16  LOAD_CONST               ('cwd',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  STORE_FAST               'output'
               22  POP_BLOCK        
               24  JUMP_FORWARD         52  'to 52'
             26_0  COME_FROM_FINALLY     0  '0'

 L.1888        26  DUP_TOP          
               28  LOAD_GLOBAL              subprocess
               30  LOAD_ATTR                CalledProcessError
               32  LOAD_GLOBAL              OSError
               34  BUILD_TUPLE_2         2 
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    50  'to 50'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.1889        46  POP_EXCEPT       
               48  JUMP_FORWARD         82  'to 82'
             50_0  COME_FROM            38  '38'
               50  END_FINALLY      
             52_0  COME_FROM            24  '24'

 L.1891        52  LOAD_GLOBAL              re
               54  LOAD_METHOD              match
               56  LOAD_CONST               b'(?P<revision>\\d+)'
               58  LOAD_FAST                'output'
               60  CALL_METHOD_2         2  ''
               62  STORE_FAST               'm'

 L.1892        64  LOAD_FAST                'm'
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L.1893        68  LOAD_GLOBAL              int
               70  LOAD_FAST                'm'
               72  LOAD_METHOD              group
               74  LOAD_STR                 'revision'
               76  CALL_METHOD_1         1  ''
               78  CALL_FUNCTION_1       1  ''
               80  RETURN_VALUE     
             82_0  COME_FROM            66  '66'
             82_1  COME_FROM            48  '48'

 L.1895        82  LOAD_GLOBAL              njoin
               84  LOAD_FAST                'path'
               86  LOAD_STR                 '.hg'
               88  LOAD_STR                 'branch'
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'branch_fn'

 L.1896        94  LOAD_GLOBAL              njoin
               96  LOAD_FAST                'path'
               98  LOAD_STR                 '.hg'
              100  LOAD_STR                 'branch.cache'
              102  CALL_FUNCTION_3       3  ''
              104  STORE_FAST               'branch_cache_fn'

 L.1898       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              isfile
              112  LOAD_FAST                'branch_fn'
              114  CALL_METHOD_1         1  ''
          116_118  POP_JUMP_IF_FALSE   280  'to 280'

 L.1899       120  LOAD_CONST               None
              122  STORE_FAST               'branch0'

 L.1900       124  LOAD_GLOBAL              open
              126  LOAD_FAST                'branch_fn'
              128  CALL_FUNCTION_1       1  ''
              130  SETUP_WITH          150  'to 150'
              132  STORE_FAST               'f'

 L.1901       134  LOAD_FAST                'f'
              136  LOAD_METHOD              read
              138  CALL_METHOD_0         0  ''
              140  LOAD_METHOD              strip
              142  CALL_METHOD_0         0  ''
              144  STORE_FAST               'revision0'
              146  POP_BLOCK        
              148  BEGIN_FINALLY    
            150_0  COME_FROM_WITH      130  '130'
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      

 L.1903       156  BUILD_MAP_0           0 
              158  STORE_FAST               'branch_map'

 L.1904       160  LOAD_GLOBAL              open
              162  LOAD_FAST                'branch_cache_fn'
              164  LOAD_STR                 'r'
              166  CALL_FUNCTION_2       2  ''
              168  SETUP_WITH          264  'to 264'
              170  STORE_FAST               'f'

 L.1905       172  LOAD_FAST                'f'
              174  GET_ITER         
            176_0  COME_FROM           258  '258'
            176_1  COME_FROM           242  '242'
              176  FOR_ITER            260  'to 260'
              178  STORE_FAST               'line'

 L.1906       180  LOAD_FAST                'line'
              182  LOAD_METHOD              split
              184  CALL_METHOD_0         0  ''
              186  LOAD_CONST               None
              188  LOAD_CONST               2
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  UNPACK_SEQUENCE_2     2 
              196  STORE_FAST               'branch1'
              198  STORE_FAST               'revision1'

 L.1907       200  LOAD_FAST                'revision1'
              202  LOAD_FAST                'revision0'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   212  'to 212'

 L.1908       208  LOAD_FAST                'branch1'
              210  STORE_FAST               'branch0'
            212_0  COME_FROM           206  '206'

 L.1909       212  SETUP_FINALLY       226  'to 226'

 L.1910       214  LOAD_GLOBAL              int
              216  LOAD_FAST                'revision1'
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'revision1'
              222  POP_BLOCK        
              224  JUMP_FORWARD        250  'to 250'
            226_0  COME_FROM_FINALLY   212  '212'

 L.1911       226  DUP_TOP          
              228  LOAD_GLOBAL              ValueError
              230  COMPARE_OP               exception-match
              232  POP_JUMP_IF_FALSE   248  'to 248'
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L.1912       240  POP_EXCEPT       
              242  JUMP_BACK           176  'to 176'
              244  POP_EXCEPT       
              246  JUMP_FORWARD        250  'to 250'
            248_0  COME_FROM           232  '232'
              248  END_FINALLY      
            250_0  COME_FROM           246  '246'
            250_1  COME_FROM           224  '224'

 L.1913       250  LOAD_FAST                'revision1'
              252  LOAD_FAST                'branch_map'
              254  LOAD_FAST                'branch1'
              256  STORE_SUBSCR     
              258  JUMP_BACK           176  'to 176'
            260_0  COME_FROM           176  '176'
              260  POP_BLOCK        
              262  BEGIN_FINALLY    
            264_0  COME_FROM_WITH      168  '168'
              264  WITH_CLEANUP_START
              266  WITH_CLEANUP_FINISH
              268  END_FINALLY      

 L.1915       270  LOAD_FAST                'branch_map'
              272  LOAD_METHOD              get
              274  LOAD_FAST                'branch0'
              276  CALL_METHOD_1         1  ''
              278  RETURN_VALUE     
            280_0  COME_FROM           116  '116'

Parse error at or near `COME_FROM' instruction at offset 248_0

        def get_version(self, version_file=None, version_variable=None):
            """Try to get version string of a package.

        Return a version string of the current package or None if the version
        information could not be detected.

        Notes
        -----
        This method scans files named
        __version__.py, <packagename>_version.py, version.py, and
        __svn_version__.py for string variables version, __version__, and
        <packagename>_version, until a version number is found.
        """
            version = getattr(self, 'version', None)
            if version is not None:
                return version
            if version_file is None:
                files = [
                 '__version__.py',
                 self.name.split('.')[(-1)] + '_version.py',
                 'version.py',
                 '__svn_version__.py',
                 '__hg_version__.py']
            else:
                files = [
                 version_file]
            if version_variable is None:
                version_vars = [
                 'version',
                 '__version__',
                 self.name.split('.')[(-1)] + '_version']
            else:
                version_vars = [
                 version_variable]
            for f in files:
                fn = njoin(self.local_path, f)
                if os.path.isfile(fn):
                    info = ('.py', 'U', 1)
                    name = os.path.splitext(os.path.basename(fn))[0]
                    n = dot_join(self.name, name)
                try:
                    version_module = npy_load_module('_'.join(n.split('.')), fn, info)
                except ImportError as e:
                    try:
                        self.warn(str(e))
                        version_module = None
                    finally:
                        e = None
                        del e

                else:
                    if version_module is None:
                        pass
                    else:
                        for a in version_vars:
                            version = getattr(version_module, a, None)
                            if version is not None:
                                break
                        else:
                            if version is not None:
                                break

            else:
                if version is not None:
                    self.version = version
                    return version
                revision = self._get_svn_revision(self.local_path)
                if revision is None:
                    revision = self._get_hg_revision(self.local_path)
                if revision is not None:
                    version = str(revision)
                    self.version = version
                return version

        def make_svn_version_py(self, delete=True):
            """Appends a data function to the data_files list that will generate
        __svn_version__.py file to the current package directory.

        Generate package __svn_version__.py file from SVN revision number,
        it will be removed after python exits but will be available
        when sdist, etc commands are executed.

        Notes
        -----
        If __svn_version__.py existed before, nothing is done.

        This is
        intended for working with source directories that are in an SVN
        repository.
        """
            target = njoin(self.local_path, '__svn_version__.py')
            revision = self._get_svn_revision(self.local_path)
            if os.path.isfile(target) or (revision is None):
                return

            def generate_svn_version_py():
                if not os.path.isfile(target):
                    version = str(revision)
                    self.info('Creating %s (version=%r)' % (target, version))
                    with open(target, 'w') as f:
                        f.write('version = %r\n' % version)

                def rm_file(f=target, p=self.info):
                    if delete:
                        try:
                            os.remove(f)
                            p('removed ' + f)
                        except OSError:
                            pass

                        try:
                            os.remove(f + 'c')
                            p('removed ' + f + 'c')
                        except OSError:
                            pass

                atexit.register(rm_file)
                return target

            self.add_data_files(('', generate_svn_version_py()))

        def make_hg_version_py(self, delete=True):
            """Appends a data function to the data_files list that will generate
        __hg_version__.py file to the current package directory.

        Generate package __hg_version__.py file from Mercurial revision,
        it will be removed after python exits but will be available
        when sdist, etc commands are executed.

        Notes
        -----
        If __hg_version__.py existed before, nothing is done.

        This is intended for working with source directories that are
        in an Mercurial repository.
        """
            target = njoin(self.local_path, '__hg_version__.py')
            revision = self._get_hg_revision(self.local_path)
            if os.path.isfile(target) or (revision is None):
                return

            def generate_hg_version_py():
                if not os.path.isfile(target):
                    version = str(revision)
                    self.info('Creating %s (version=%r)' % (target, version))
                    with open(target, 'w') as f:
                        f.write('version = %r\n' % version)

                def rm_file(f=target, p=self.info):
                    if delete:
                        try:
                            os.remove(f)
                            p('removed ' + f)
                        except OSError:
                            pass

                        try:
                            os.remove(f + 'c')
                            p('removed ' + f + 'c')
                        except OSError:
                            pass

                atexit.register(rm_file)
                return target

            self.add_data_files(('', generate_hg_version_py()))

        def make_config_py(self, name='__config__'):
            """Generate package __config__.py file containing system_info
        information used during building the package.

        This file is installed to the
        package installation directory.

        """
            self.py_modules.append((self.name, name, generate_config_py))

        def get_info(self, *names):
            """Get resources information.

        Return information (from system_info.get_info) for all of the names in
        the argument list in a single dictionary.
        """
            from .system_info import get_info, dict_append
            info_dict = {}
            for a in names:
                dict_append(info_dict, **get_info(a))
            else:
                return info_dict


    def get_cmd(cmdname, _cache={}):
        if cmdname not in _cache:
            import distutils.core
            dist = distutils.core._setup_distribution
            if dist is None:
                from distutils.errors import DistutilsInternalError
                raise DistutilsInternalError('setup distribution instance not initialized')
            cmd = dist.get_command_obj(cmdname)
            _cache[cmdname] = cmd
        return _cache[cmdname]


    def get_numpy_include_dirs():
        include_dirs = Configuration.numpy_include_dirs[:]
        if not include_dirs:
            import numpy
            include_dirs = [
             numpy.get_include()]
        return include_dirs


    def get_npy_pkg_dir():
        """Return the path where to find the npy-pkg-config directory.

    If the NPY_PKG_CONFIG_PATH environment variable is set, the value of that
    is returned.  Otherwise, a path inside the location of the numpy module is
    returned.

    The NPY_PKG_CONFIG_PATH can be useful when cross-compiling, maintaining
    customized npy-pkg-config .ini files for the cross-compilation
    environment, and using them when cross-compiling.

    """
        d = os.environ.get('NPY_PKG_CONFIG_PATH')
        if d is not None:
            return d
        spec = importlib.util.find_spec('numpy')
        d = os.path.join(os.path.dirname(spec.origin), 'core', 'lib', 'npy-pkg-config')
        return d


    def get_pkg_info(pkgname, dirs=None):
        """
    Return library info for the given package.

    Parameters
    ----------
    pkgname : str
        Name of the package (should match the name of the .ini file, without
        the extension, e.g. foo for the file foo.ini).
    dirs : sequence, optional
        If given, should be a sequence of additional directories where to look
        for npy-pkg-config files. Those directories are searched prior to the
        NumPy directory.

    Returns
    -------
    pkginfo : class instance
        The `LibraryInfo` instance containing the build information.

    Raises
    ------
    PkgNotFound
        If the package is not found.

    See Also
    --------
    Configuration.add_npy_pkg_config, Configuration.add_installed_library,
    get_info

    """
        from numpy.distutils.npy_pkg_config import read_config
        if dirs:
            dirs.append(get_npy_pkg_dir())
        else:
            dirs = [
             get_npy_pkg_dir()]
        return read_config(pkgname, dirs)


    def get_info(pkgname, dirs=None):
        """
    Return an info dict for a given C library.

    The info dict contains the necessary options to use the C library.

    Parameters
    ----------
    pkgname : str
        Name of the package (should match the name of the .ini file, without
        the extension, e.g. foo for the file foo.ini).
    dirs : sequence, optional
        If given, should be a sequence of additional directories where to look
        for npy-pkg-config files. Those directories are searched prior to the
        NumPy directory.

    Returns
    -------
    info : dict
        The dictionary with build information.

    Raises
    ------
    PkgNotFound
        If the package is not found.

    See Also
    --------
    Configuration.add_npy_pkg_config, Configuration.add_installed_library,
    get_pkg_info

    Examples
    --------
    To get the necessary information for the npymath library from NumPy:

    >>> npymath_info = np.distutils.misc_util.get_info('npymath')
    >>> npymath_info                                    #doctest: +SKIP
    {'define_macros': [], 'libraries': ['npymath'], 'library_dirs':
    ['.../numpy/core/lib'], 'include_dirs': ['.../numpy/core/include']}

    This info dict can then be used as input to a `Configuration` instance::

      config.add_extension('foo', sources=['foo.c'], extra_info=npymath_info)

    """
        from numpy.distutils.npy_pkg_config import parse_flags
        pkg_info = get_pkg_info(pkgname, dirs)
        info = parse_flags(pkg_info.cflags())
        for k, v in parse_flags(pkg_info.libs()).items():
            info[k].extend(v)
        else:
            info['define_macros'] = info['macros']
            del info['macros']
            del info['ignored']
            return info


    def is_bootstrapping--- This code section failed: ---

 L.2233         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              builtins
                6  STORE_FAST               'builtins'

 L.2235         8  SETUP_FINALLY        22  'to 22'

 L.2236        10  LOAD_FAST                'builtins'
               12  LOAD_ATTR                __NUMPY_SETUP__
               14  POP_TOP          

 L.2237        16  POP_BLOCK        
               18  LOAD_CONST               True
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     8  '8'

 L.2238        22  DUP_TOP          
               24  LOAD_GLOBAL              AttributeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    42  'to 42'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.2239        36  POP_EXCEPT       
               38  LOAD_CONST               False
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'
               42  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 22


    def default_config_dict(name=None, parent_name=None, local_path=None):
        """Return a configuration dictionary for usage in
    configuration() function defined in file setup_<name>.py.
    """
        import warnings
        warnings.warn(('Use Configuration(%r,%r,top_path=%r) instead of deprecated default_config_dict(%r,%r,%r)' % (
         name, parent_name, local_path,
         name, parent_name, local_path)),
          stacklevel=2)
        c = Configuration(name, parent_name, local_path)
        return c.todict()


    def dict_append(d, **kws):
        for k, v in kws.items():
            if k in d:
                ov = d[k]
                if isinstance(ov, str):
                    d[k] = v
                else:
                    d[k].extend(v)
            else:
                d[k] = v


    def appendpath(prefix, path):
        if os.path.sep != '/':
            prefix = prefix.replace('/', os.path.sep)
            path = path.replace('/', os.path.sep)
        drive = ''
        if os.path.isabs(path):
            drive = os.path.splitdrive(prefix)[0]
            absprefix = os.path.splitdrive(os.path.abspath(prefix))[1]
            pathdrive, path = os.path.splitdrive(path)
            d = os.path.commonprefix([absprefix, path])
            if os.path.join(absprefix[:len(d)], absprefix[len(d):]) != absprefix or (os.path.join(path[:len(d)], path[len(d):]) != path):
                d = os.path.dirname(d)
            subpath = path[len(d):]
            if os.path.isabs(subpath):
                subpath = subpath[1:]
        else:
            subpath = path
        return os.path.normpath(njoin(drive + prefix, subpath))


    def generate_config_py(target):
        """Generate config.py file containing system_info information
    used during building the package.

    Usage:
        config['py_modules'].append((packagename, '__config__',generate_config_py))
    """
        import numpy.distutils.system_info as system_info
        from distutils.dir_util import mkpath
        mkpath(os.path.dirname(target))
        with open(target, 'w') as f:
            f.write("# This file is generated by numpy's %s\n" % os.path.basename(sys.argv[0]))
            f.write('# It contains system_info results at the time of building this package.\n')
            f.write('__all__ = ["get_info","show"]\n\n')
            f.write(textwrap.dedent("\n            import os\n            import sys\n\n            extra_dll_dir = os.path.join(os.path.dirname(__file__), '.libs')\n\n            if sys.platform == 'win32' and os.path.isdir(extra_dll_dir):\n                if sys.version_info >= (3, 8):\n                    os.add_dll_directory(extra_dll_dir)\n                else:\n                    os.environ.setdefault('PATH', '')\n                    os.environ['PATH'] += os.pathsep + extra_dll_dir\n\n            "))
            for k, i in system_info.saved_results.items():
                f.write('%s=%r\n' % (k, i))
            else:
                f.write(textwrap.dedent('\n            def get_info(name):\n                g = globals()\n                return g.get(name, g.get(name + "_info", {}))\n\n            def show():\n                """\n                Show libraries in the system on which NumPy was built.\n\n                Print information about various resources (libraries, library\n                directories, include directories, etc.) in the system on which\n                NumPy was built.\n\n                See Also\n                --------\n                get_include : Returns the directory containing NumPy C\n                              header files.\n\n                Notes\n                -----\n                Classes specifying the information to be printed are defined\n                in the `numpy.distutils.system_info` module.\n\n                Information may include:\n\n                * ``language``: language used to write the libraries (mostly\n                  C or f77)\n                * ``libraries``: names of libraries found in the system\n                * ``library_dirs``: directories containing the libraries\n                * ``include_dirs``: directories containing library header files\n                * ``src_dirs``: directories containing library source files\n                * ``define_macros``: preprocessor macros used by\n                  ``distutils.setup``\n\n                Examples\n                --------\n                >>> import numpy as np\n                >>> np.show_config()\n                blas_opt_info:\n                    language = c\n                    define_macros = [(\'HAVE_CBLAS\', None)]\n                    libraries = [\'openblas\', \'openblas\']\n                    library_dirs = [\'/usr/local/lib\']\n                """\n                for name,info_dict in globals().items():\n                    if name[0] == "_" or type(info_dict) is not type({}): continue\n                    print(name + ":")\n                    if not info_dict:\n                        print("  NOT AVAILABLE")\n                    for k,v in info_dict.items():\n                        v = str(v)\n                        if k == "sources" and len(v) > 200:\n                            v = v[:60] + " ...\\n... " + v[-60:]\n                        print("    %s = %s" % (k,v))\n                    '))

        return target


    def msvc_version(compiler):
        """Return version major and minor of compiler instance if it is
    MSVC, raise an exception otherwise."""
        if not compiler.compiler_type == 'msvc':
            raise ValueError('Compiler instance is not msvc (%s)' % compiler.compiler_type)
        return compiler._MSVCCompiler__version


    def get_build_architecture():
        from distutils.msvccompiler import get_build_architecture
        return get_build_architecture()