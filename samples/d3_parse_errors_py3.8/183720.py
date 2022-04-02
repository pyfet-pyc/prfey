# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\ccompiler.py
from __future__ import division, absolute_import, print_function
import os, re, sys, types, shlex, time, subprocess
from copy import copy
from distutils import ccompiler
from distutils.ccompiler import *
from distutils.errors import DistutilsExecError, DistutilsModuleError, DistutilsPlatformError, CompileError
from distutils.sysconfig import customize_compiler
from distutils.version import LooseVersion
from numpy.distutils import log
from numpy.distutils.compat import get_exception
from numpy.distutils.exec_command import filepath_from_subprocess_output, forward_bytes_to_stdout
from numpy.distutils.misc_util import cyg2win32, is_sequence, mingw32, get_num_build_jobs, _commandline_dep_string
try:
    import threading
except ImportError:
    import dummy_threading as threading
else:
    _job_semaphore = None
    _global_lock = threading.Lock()
    _processing_files = set()

    def _needs_build--- This code section failed: ---

 L.  51         0  LOAD_FAST                'obj'
                2  LOAD_STR                 '.d'
                4  BINARY_ADD       
                6  STORE_FAST               'dep_file'

 L.  52         8  LOAD_GLOBAL              os
               10  LOAD_ATTR                path
               12  LOAD_METHOD              exists
               14  LOAD_FAST                'dep_file'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'

 L.  53        20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  60        24  LOAD_GLOBAL              open
               26  LOAD_FAST                'dep_file'
               28  LOAD_STR                 'r'
               30  CALL_FUNCTION_2       2  ''
               32  SETUP_WITH           48  'to 48'
               34  STORE_FAST               'f'

 L.  61        36  LOAD_FAST                'f'
               38  LOAD_METHOD              readlines
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'lines'
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       32  '32'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

 L.  63        54  LOAD_GLOBAL              _commandline_dep_string
               56  LOAD_FAST                'cc_args'
               58  LOAD_FAST                'extra_postargs'
               60  LOAD_FAST                'pp_opts'
               62  CALL_FUNCTION_3       3  ''
               64  STORE_FAST               'cmdline'

 L.  64        66  LOAD_FAST                'lines'
               68  LOAD_CONST               -1
               70  BINARY_SUBSCR    
               72  STORE_FAST               'last_cmdline'

 L.  65        74  LOAD_FAST                'last_cmdline'
               76  LOAD_FAST                'cmdline'
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L.  66        82  LOAD_CONST               True
               84  RETURN_VALUE     
             86_0  COME_FROM            80  '80'

 L.  68        86  LOAD_STR                 ''
               88  LOAD_METHOD              join
               90  LOAD_FAST                'lines'
               92  LOAD_CONST               None
               94  LOAD_CONST               -1
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'contents'

 L.  69       104  LOAD_LISTCOMP            '<code_object <listcomp>>'
              106  LOAD_STR                 '_needs_build.<locals>.<listcomp>'
              108  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              110  LOAD_GLOBAL              shlex
              112  LOAD_ATTR                split
              114  LOAD_FAST                'contents'
              116  LOAD_CONST               True
              118  LOAD_CONST               ('posix',)
              120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              122  GET_ITER         
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'deps'

 L.  72       128  SETUP_FINALLY       180  'to 180'

 L.  73       130  LOAD_GLOBAL              os
              132  LOAD_METHOD              stat
              134  LOAD_FAST                'obj'
              136  CALL_METHOD_1         1  ''
              138  LOAD_ATTR                st_mtime
              140  STORE_FAST               't_obj'

 L.  77       142  LOAD_FAST                'deps'
              144  GET_ITER         
            146_0  COME_FROM           174  '174'
            146_1  COME_FROM           164  '164'
              146  FOR_ITER            176  'to 176'
              148  STORE_FAST               'f'

 L.  78       150  LOAD_GLOBAL              os
              152  LOAD_METHOD              stat
              154  LOAD_FAST                'f'
              156  CALL_METHOD_1         1  ''
              158  LOAD_ATTR                st_mtime
              160  LOAD_FAST                't_obj'
              162  COMPARE_OP               >
              164  POP_JUMP_IF_FALSE_BACK   146  'to 146'

 L.  79       166  POP_TOP          
              168  POP_BLOCK        
              170  LOAD_CONST               True
              172  RETURN_VALUE     
              174  JUMP_BACK           146  'to 146'
            176_0  COME_FROM           146  '146'
              176  POP_BLOCK        
              178  JUMP_FORWARD        202  'to 202'
            180_0  COME_FROM_FINALLY   128  '128'

 L.  80       180  DUP_TOP          
              182  LOAD_GLOBAL              OSError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   200  'to 200'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L.  82       194  POP_EXCEPT       
              196  LOAD_CONST               True
              198  RETURN_VALUE     
            200_0  COME_FROM           186  '186'
              200  END_FINALLY      
            202_0  COME_FROM           178  '178'

 L.  84       202  LOAD_CONST               False
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 168


    def replace_method(klass, method_name, func):
        if sys.version_info[0] < 3:
            m = types.MethodType(func, None, klass)
        else:
            m = lambda self, *args, **kw: func(self, *args, **kw)
        setattr(klass, method_name, m)


    def CCompiler_find_executables(self):
        """
    Does nothing here, but is called by the get_version method and can be
    overridden by subclasses. In particular it is redefined in the `FCompiler`
    class where more documentation can be found.

    """
        pass


    replace_method(CCompiler, 'find_executables', CCompiler_find_executables)

    def CCompiler_spawn(self, cmd, display=None):
        """
    Execute a command in a sub-process.

    Parameters
    ----------
    cmd : str
        The command to execute.
    display : str or sequence of str, optional
        The text to add to the log file kept by `numpy.distutils`.
        If not given, `display` is equal to `cmd`.

    Returns
    -------
    None

    Raises
    ------
    DistutilsExecError
        If the command failed, i.e. the exit status was not 0.

    """
        if display is None:
            display = cmd
            if is_sequence(display):
                display = ' '.join(list(display))
        log.info(display)
        try:
            if self.verbose:
                subprocess.check_output(cmd)
            else:
                subprocess.check_output(cmd, stderr=(subprocess.STDOUT))
        except subprocess.CalledProcessError as exc:
            try:
                o = exc.output
                s = exc.returncode
            finally:
                exc = None
                del exc

        except OSError:
            o = b''
            s = 127
        else:
            return
        if is_sequence(cmd):
            cmd = ' '.join(list(cmd))
        if self.verbose:
            forward_bytes_to_stdout(o)
        if re.search(b'Too many open files', o):
            msg = '\nTry rerunning setup command until build succeeds.'
        else:
            msg = ''
        raise DistutilsExecError('Command "%s" failed with exit status %d%s' % (
         cmd, s, msg))


    replace_method(CCompiler, 'spawn', CCompiler_spawn)

    def CCompiler_object_filenames(self, source_filenames, strip_dir=0, output_dir=''):
        """
    Return the name of the object files for the given source files.

    Parameters
    ----------
    source_filenames : list of str
        The list of paths to source files. Paths can be either relative or
        absolute, this is handled transparently.
    strip_dir : bool, optional
        Whether to strip the directory from the returned paths. If True,
        the file name prepended by `output_dir` is returned. Default is False.
    output_dir : str, optional
        If given, this path is prepended to the returned paths to the
        object files.

    Returns
    -------
    obj_names : list of str
        The list of paths to the object files corresponding to the source
        files in `source_filenames`.

    """
        if output_dir is None:
            output_dir = ''
        obj_names = []
        for src_name in source_filenames:
            base, ext = os.path.splitext(os.path.normpath(src_name))
            base = os.path.splitdrive(base)[1]
            base = base[os.path.isabs(base):]
            if base.startswith('..'):
                i = base.rfind('..') + 2
                d = base[:i]
                d = os.path.basename(os.path.abspath(d))
                base = d + base[i:]
            else:
                if ext not in self.src_extensions:
                    raise UnknownFileError("unknown file type '%s' (from '%s')" % (ext, src_name))
                if strip_dir:
                    base = os.path.basename(base)
                obj_name = os.path.join(output_dir, base + self.obj_extension)
                obj_names.append(obj_name)
        else:
            return obj_names


    replace_method(CCompiler, 'object_filenames', CCompiler_object_filenames)

    def CCompiler_compile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
        """
    Compile one or more source files.

    Please refer to the Python distutils API reference for more details.

    Parameters
    ----------
    sources : list of str
        A list of filenames
    output_dir : str, optional
        Path to the output directory.
    macros : list of tuples
        A list of macro definitions.
    include_dirs : list of str, optional
        The directories to add to the default include file search path for
        this compilation only.
    debug : bool, optional
        Whether or not to output debug symbols in or alongside the object
        file(s).
    extra_preargs, extra_postargs : ?
        Extra pre- and post-arguments.
    depends : list of str, optional
        A list of file names that all targets depend on.

    Returns
    -------
    objects : list of str
        A list of object file names, one per source file `sources`.

    Raises
    ------
    CompileError
        If compilation fails.

    """
        global _job_semaphore
        jobs = get_num_build_jobs()
        with _global_lock:
            if _job_semaphore is None:
                _job_semaphore = threading.Semaphore(jobs)
        if not sources:
            return []
        if sys.version_info[0] < 3:
            from .fcompiler import FCompiler, is_f_file, has_f90_header
        else:
            from numpy.distutils.fcompiler import FCompiler, is_f_file, has_f90_header
        if isinstanceselfFCompiler:
            display = []
            for fc in ('f77', 'f90', 'fix'):
                fcomp = getattrself('compiler_' + fc)
                if fcomp is None:
                    pass
                else:
                    display.append('Fortran %s compiler: %s' % (fc, ' '.join(fcomp)))
            else:
                display = '\n'.join(display)

        else:
            ccomp = self.compiler_so
            display = 'C compiler: %s\n' % (' '.join(ccomp),)
        log.info(display)
        macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
        cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
        display = "compile options: '%s'" % ' '.join(cc_args)
        if extra_postargs:
            display += "\nextra options: '%s'" % ' '.join(extra_postargs)
        log.info(display)

        def single_compile--- This code section failed: ---

 L. 308         0  LOAD_FAST                'args'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'obj'
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'src'
               10  STORE_FAST               'ext'

 L. 309        12  LOAD_GLOBAL              _needs_build
               14  LOAD_FAST                'obj'
               16  LOAD_DEREF               'cc_args'
               18  LOAD_DEREF               'extra_postargs'
               20  LOAD_DEREF               'pp_opts'
               22  CALL_FUNCTION_4       4  ''
               24  POP_JUMP_IF_TRUE     30  'to 30'

 L. 310        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            86  '86'
             30_1  COME_FROM            24  '24'

 L. 316        30  LOAD_GLOBAL              _global_lock
               32  SETUP_WITH           70  'to 70'
               34  POP_TOP          

 L. 318        36  LOAD_FAST                'obj'
               38  LOAD_GLOBAL              _processing_files
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_FALSE    66  'to 66'

 L. 319        44  LOAD_GLOBAL              _processing_files
               46  LOAD_METHOD              add
               48  LOAD_FAST                'obj'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 320        54  POP_BLOCK        
               56  BEGIN_FINALLY    
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  POP_FINALLY           0  ''
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM            42  '42'
               66  POP_BLOCK        
               68  BEGIN_FINALLY    
             70_0  COME_FROM_WITH       32  '32'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

 L. 322        76  LOAD_GLOBAL              time
               78  LOAD_METHOD              sleep
               80  LOAD_CONST               0.1
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  JUMP_BACK            30  'to 30'
             88_0  COME_FROM            64  '64'

 L. 324        88  SETUP_FINALLY       130  'to 130'

 L. 326        90  LOAD_GLOBAL              _job_semaphore
               92  SETUP_WITH          120  'to 120'
               94  POP_TOP          

 L. 327        96  LOAD_DEREF               'self'
               98  LOAD_METHOD              _compile
              100  LOAD_FAST                'obj'
              102  LOAD_FAST                'src'
              104  LOAD_FAST                'ext'
              106  LOAD_DEREF               'cc_args'
              108  LOAD_DEREF               'extra_postargs'
              110  LOAD_DEREF               'pp_opts'
              112  CALL_METHOD_6         6  ''
              114  POP_TOP          
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM_WITH       92  '92'
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  END_FINALLY      
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_FINALLY    88  '88'

 L. 330       130  LOAD_GLOBAL              _global_lock
              132  SETUP_WITH          150  'to 150'
              134  POP_TOP          

 L. 331       136  LOAD_GLOBAL              _processing_files
              138  LOAD_METHOD              remove
              140  LOAD_FAST                'obj'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
              146  POP_BLOCK        
              148  BEGIN_FINALLY    
            150_0  COME_FROM_WITH      132  '132'
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      
              156  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 56

        if isinstanceselfFCompiler:
            objects_to_build = list(build.keys())
            f77_objects, other_objects = [], []
            for obj in objects:
                if obj in objects_to_build:
                    src, ext = build[obj]
                    if self.compiler_type == 'absoft':
                        obj = cyg2win32(obj)
                        src = cyg2win32(src)
                    if is_f_file(src):
                        if not has_f90_header(src):
                            f77_objects.append((obj, (src, ext)))
                        other_objects.append((obj, (src, ext)))
            else:
                build_items = f77_objects
                for o in other_objects:
                    single_compile(o)

        else:
            build_items = build.items()
        if len(build) > 1 and jobs > 1:
            import multiprocessing.pool
            pool = multiprocessing.pool.ThreadPool(jobs)
            pool.map(single_compile, build_items)
            pool.close()
        else:
            pass
        for o in build_items:
            single_compile(o)
        else:
            return objects


    replace_method(CCompiler, 'compile', CCompiler_compile)

    def CCompiler_customize_cmd(self, cmd, ignore=()):
        """
    Customize compiler using distutils command.

    Parameters
    ----------
    cmd : class instance
        An instance inheriting from `distutils.cmd.Command`.
    ignore : sequence of str, optional
        List of `CCompiler` commands (without ``'set_'``) that should not be
        altered. Strings that are checked for are:
        ``('include_dirs', 'define', 'undef', 'libraries', 'library_dirs',
        'rpath', 'link_objects')``.

    Returns
    -------
    None

    """
        log.info('customize %s using %s' % (self.__class__.__name__,
         cmd.__class__.__name__))

        def allow(attr):
            return getattr(cmd, attr, None) is not None and attr not in ignore

        if allow('include_dirs'):
            self.set_include_dirs(cmd.include_dirs)
        if allow('define'):
            for name, value in cmd.define:
                self.define_macro(name, value)
            else:
                if allow('undef'):
                    for macro in cmd.undef:
                        self.undefine_macro(macro)
                    else:
                        if allow('libraries'):
                            self.set_libraries(self.libraries + cmd.libraries)
                        if allow('library_dirs'):
                            self.set_library_dirs(self.library_dirs + cmd.library_dirs)
                        if allow('rpath'):
                            self.set_runtime_library_dirs(cmd.rpath)

                if allow('link_objects'):
                    self.set_link_objects(cmd.link_objects)


    replace_method(CCompiler, 'customize_cmd', CCompiler_customize_cmd)

    def _compiler_to_string(compiler):
        props = []
        mx = 0
        keys = list(compiler.executables.keys())
        for key in ('version', 'libraries', 'library_dirs', 'object_switch', 'compile_switch',
                    'include_dirs', 'define', 'undef', 'rpath', 'link_objects'):
            if key not in keys:
                keys.append(key)
        else:
            for key in keys:
                if hasattrcompilerkey:
                    v = getattrcompilerkey
                    mx = maxmxlen(key)
                    props.append((key, repr(v)))
            else:
                fmt = '%-' + repr(mx + 1) + 's = %s'
                lines = [fmt % prop for prop in props]
                return '\n'.join(lines)


    def CCompiler_show_customization(self):
        """
    Print the compiler customizations to stdout.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    Printing is only done if the distutils log threshold is < 2.

    """
        try:
            self.get_version()
        except Exception:
            pass
        else:
            if log._global_log.threshold < 2:
                print('********************************************************************************')
                print(self.__class__)
                print(_compiler_to_string(self))
                print('********************************************************************************')


    replace_method(CCompiler, 'show_customization', CCompiler_show_customization)

    def CCompiler_customize(self, dist, need_cxx=0):
        """
    Do any platform-specific customization of a compiler instance.

    This method calls `distutils.sysconfig.customize_compiler` for
    platform-specific customization, as well as optionally remove a flag
    to suppress spurious warnings in case C++ code is being compiled.

    Parameters
    ----------
    dist : object
        This parameter is not used for anything.
    need_cxx : bool, optional
        Whether or not C++ has to be compiled. If so (True), the
        ``"-Wstrict-prototypes"`` option is removed to prevent spurious
        warnings. Default is False.

    Returns
    -------
    None

    Notes
    -----
    All the default options used by distutils can be extracted with::

      from distutils import sysconfig
      sysconfig.get_config_vars('CC', 'CXX', 'OPT', 'BASECFLAGS',
                                'CCSHARED', 'LDSHARED', 'SO')

    """
        log.info('customize %s' % self.__class__.__name__)
        customize_compiler(self)
        if need_cxx:
            try:
                self.compiler_so.remove('-Wstrict-prototypes')
            except (AttributeError, ValueError):
                pass
            else:
                if hasattrself'compiler' and 'cc' in self.compiler[0]:
                    if not self.compiler_cxx:
                        if self.compiler[0].startswith('gcc'):
                            a, b = ('gcc', 'g++')
                        else:
                            a, b = ('cc', 'c++')
                        self.compiler_cxx = [
                         self.compiler[0].replace(a, b)] + self.compiler[1:]
                else:
                    if hasattrself'compiler':
                        log.warn('#### %s #######' % (self.compiler,))
                    if not hasattrself'compiler_cxx':
                        log.warn('Missing compiler_cxx fix for ' + self.__class__.__name__)
        if not hasattrself'compiler' or 'gcc' in self.compiler[0] or 'g++' in self.compiler[0] or 'clang' in self.compiler[0]:
            self._auto_depends = True
        elif os.name == 'posix':
            import tempfile, shutil
            tmpdir = tempfile.mkdtemp()
            try:
                try:
                    fn = os.path.join(tmpdir, 'file.c')
                    with openfn'w' as f:
                        f.write('int a;\n')
                    self.compile([fn], output_dir=tmpdir, extra_preargs=[
                     '-MMD', '-MF', fn + '.d'])
                    self._auto_depends = True
                except CompileError:
                    self._auto_depends = False

            finally:
                shutil.rmtree(tmpdir)


    replace_method(CCompiler, 'customize', CCompiler_customize)

    def simple_version_match(pat='[-.\\d]+', ignore='', start=''):
        r"""
    Simple matching of version numbers, for use in CCompiler and FCompiler.

    Parameters
    ----------
    pat : str, optional
        A regular expression matching version numbers.
        Default is ``r'[-.\d]+'``.
    ignore : str, optional
        A regular expression matching patterns to skip.
        Default is ``''``, in which case nothing is skipped.
    start : str, optional
        A regular expression matching the start of where to start looking
        for version numbers.
        Default is ``''``, in which case searching is started at the
        beginning of the version string given to `matcher`.

    Returns
    -------
    matcher : callable
        A function that is appropriate to use as the ``.version_match``
        attribute of a `CCompiler` class. `matcher` takes a single parameter,
        a version string.

    """

        def matcher--- This code section failed: ---

 L. 584         0  LOAD_FAST                'version_string'
                2  LOAD_METHOD              replace
                4  LOAD_STR                 '\n'
                6  LOAD_STR                 ' '
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'version_string'

 L. 585        12  LOAD_CONST               0
               14  STORE_FAST               'pos'

 L. 586        16  LOAD_DEREF               'start'
               18  POP_JUMP_IF_FALSE    48  'to 48'

 L. 587        20  LOAD_GLOBAL              re
               22  LOAD_METHOD              match
               24  LOAD_DEREF               'start'
               26  LOAD_FAST                'version_string'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'm'

 L. 588        32  LOAD_FAST                'm'
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L. 589        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 590        40  LOAD_FAST                'm'
               42  LOAD_METHOD              end
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'pos'
             48_0  COME_FROM           110  '110'
             48_1  COME_FROM           106  '106'
             48_2  COME_FROM            18  '18'

 L. 592        48  LOAD_GLOBAL              re
               50  LOAD_METHOD              search
               52  LOAD_DEREF               'pat'
               54  LOAD_FAST                'version_string'
               56  LOAD_FAST                'pos'
               58  LOAD_CONST               None
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'm'

 L. 593        68  LOAD_FAST                'm'
               70  POP_JUMP_IF_TRUE     76  'to 76'

 L. 594        72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

 L. 595        76  LOAD_DEREF               'ignore'
               78  POP_JUMP_IF_FALSE   112  'to 112'
               80  LOAD_GLOBAL              re
               82  LOAD_METHOD              match
               84  LOAD_DEREF               'ignore'
               86  LOAD_FAST                'm'
               88  LOAD_METHOD              group
               90  LOAD_CONST               0
               92  CALL_METHOD_1         1  ''
               94  CALL_METHOD_2         2  ''
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L. 596        98  LOAD_FAST                'm'
              100  LOAD_METHOD              end
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'pos'

 L. 597       106  JUMP_BACK            48  'to 48'

 L. 598       108  BREAK_LOOP          112  'to 112'
              110  JUMP_BACK            48  'to 48'
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            96  '96'
            112_2  COME_FROM            78  '78'

 L. 599       112  LOAD_FAST                'm'
              114  LOAD_METHOD              group
              116  LOAD_CONST               0
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 112

        return matcher


    def CCompiler_get_version--- This code section failed: ---

 L. 622         0  LOAD_FAST                'force'
                2  POP_JUMP_IF_TRUE     20  'to 20'
                4  LOAD_GLOBAL              hasattr
                6  LOAD_FAST                'self'
                8  LOAD_STR                 'version'
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L. 623        14  LOAD_FAST                'self'
               16  LOAD_ATTR                version
               18  RETURN_VALUE     
             20_0  COME_FROM            12  '12'
             20_1  COME_FROM             2  '2'

 L. 624        20  LOAD_FAST                'self'
               22  LOAD_METHOD              find_executables
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 625        28  SETUP_FINALLY        40  'to 40'

 L. 626        30  LOAD_FAST                'self'
               32  LOAD_ATTR                version_cmd
               34  STORE_FAST               'version_cmd'
               36  POP_BLOCK        
               38  JUMP_FORWARD         62  'to 62'
             40_0  COME_FROM_FINALLY    28  '28'

 L. 627        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    60  'to 60'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 628        54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            46  '46'
               60  END_FINALLY      
             62_0  COME_FROM            38  '38'

 L. 629        62  LOAD_FAST                'version_cmd'
               64  POP_JUMP_IF_FALSE    74  'to 74'
               66  LOAD_FAST                'version_cmd'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  POP_JUMP_IF_TRUE     78  'to 78'
             74_0  COME_FROM            64  '64'

 L. 630        74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L. 631        78  SETUP_FINALLY        90  'to 90'

 L. 632        80  LOAD_FAST                'self'
               82  LOAD_ATTR                version_match
               84  STORE_FAST               'matcher'
               86  POP_BLOCK        
               88  JUMP_FORWARD        158  'to 158'
             90_0  COME_FROM_FINALLY    78  '78'

 L. 633        90  DUP_TOP          
               92  LOAD_GLOBAL              AttributeError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   156  'to 156'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 634       104  SETUP_FINALLY       116  'to 116'

 L. 635       106  LOAD_FAST                'self'
              108  LOAD_ATTR                version_pattern
              110  STORE_DEREF              'pat'
              112  POP_BLOCK        
              114  JUMP_FORWARD        140  'to 140'
            116_0  COME_FROM_FINALLY   104  '104'

 L. 636       116  DUP_TOP          
              118  LOAD_GLOBAL              AttributeError
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   138  'to 138'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 637       130  POP_EXCEPT       
              132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  RETURN_VALUE     
            138_0  COME_FROM           122  '122'
              138  END_FINALLY      
            140_0  COME_FROM           114  '114'

 L. 638       140  LOAD_CLOSURE             'pat'
              142  BUILD_TUPLE_1         1 
              144  LOAD_CODE                <code_object matcher>
              146  LOAD_STR                 'CCompiler_get_version.<locals>.matcher'
              148  MAKE_FUNCTION_8          'closure'
              150  STORE_FAST               'matcher'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM            96  '96'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM            88  '88'

 L. 645       158  SETUP_FINALLY       180  'to 180'

 L. 646       160  LOAD_GLOBAL              subprocess
              162  LOAD_ATTR                check_output
              164  LOAD_FAST                'version_cmd'
              166  LOAD_GLOBAL              subprocess
              168  LOAD_ATTR                STDOUT
              170  LOAD_CONST               ('stderr',)
              172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              174  STORE_FAST               'output'
              176  POP_BLOCK        
              178  JUMP_FORWARD        256  'to 256'
            180_0  COME_FROM_FINALLY   158  '158'

 L. 647       180  DUP_TOP          
              182  LOAD_GLOBAL              subprocess
              184  LOAD_ATTR                CalledProcessError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   226  'to 226'
              190  POP_TOP          
              192  STORE_FAST               'exc'
              194  POP_TOP          
              196  SETUP_FINALLY       214  'to 214'

 L. 648       198  LOAD_FAST                'exc'
              200  LOAD_ATTR                output
              202  STORE_FAST               'output'

 L. 649       204  LOAD_FAST                'exc'
              206  LOAD_ATTR                returncode
              208  STORE_FAST               'status'
              210  POP_BLOCK        
              212  BEGIN_FINALLY    
            214_0  COME_FROM_FINALLY   196  '196'
              214  LOAD_CONST               None
              216  STORE_FAST               'exc'
              218  DELETE_FAST              'exc'
              220  END_FINALLY      
              222  POP_EXCEPT       
              224  JUMP_FORWARD        268  'to 268'
            226_0  COME_FROM           188  '188'

 L. 650       226  DUP_TOP          
              228  LOAD_GLOBAL              OSError
              230  COMPARE_OP               exception-match
          232_234  POP_JUMP_IF_FALSE   254  'to 254'
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          

 L. 653       242  LOAD_CONST               127
              244  STORE_FAST               'status'

 L. 654       246  LOAD_CONST               b''
              248  STORE_FAST               'output'
              250  POP_EXCEPT       
              252  JUMP_FORWARD        268  'to 268'
            254_0  COME_FROM           232  '232'
              254  END_FINALLY      
            256_0  COME_FROM           178  '178'

 L. 658       256  LOAD_GLOBAL              filepath_from_subprocess_output
              258  LOAD_FAST                'output'
              260  CALL_FUNCTION_1       1  ''
              262  STORE_FAST               'output'

 L. 659       264  LOAD_CONST               0
              266  STORE_FAST               'status'
            268_0  COME_FROM           252  '252'
            268_1  COME_FROM           224  '224'

 L. 661       268  LOAD_CONST               None
              270  STORE_FAST               'version'

 L. 662       272  LOAD_FAST                'status'
              274  LOAD_FAST                'ok_status'
              276  COMPARE_OP               in
          278_280  POP_JUMP_IF_FALSE   304  'to 304'

 L. 663       282  LOAD_FAST                'matcher'
              284  LOAD_FAST                'output'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'version'

 L. 664       290  LOAD_FAST                'version'
          292_294  POP_JUMP_IF_FALSE   304  'to 304'

 L. 665       296  LOAD_GLOBAL              LooseVersion
              298  LOAD_FAST                'version'
              300  CALL_FUNCTION_1       1  ''
              302  STORE_FAST               'version'
            304_0  COME_FROM           292  '292'
            304_1  COME_FROM           278  '278'

 L. 666       304  LOAD_FAST                'version'
              306  LOAD_FAST                'self'
              308  STORE_ATTR               version

 L. 667       310  LOAD_FAST                'version'
              312  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 134


    replace_method(CCompiler, 'get_version', CCompiler_get_version)

    def CCompiler_cxx_compiler(self):
        """
    Return the C++ compiler.

    Parameters
    ----------
    None

    Returns
    -------
    cxx : class instance
        The C++ compiler, as a `CCompiler` instance.

    """
        if self.compiler_type in ('msvc', 'intelw', 'intelemw'):
            return self
        cxx = copy(self)
        cxx.compiler_so = [cxx.compiler_cxx[0]] + cxx.compiler_so[1:]
        if sys.platform.startswith('aix') and 'ld_so_aix' in cxx.linker_so[0]:
            cxx.linker_so = [cxx.linker_so[0], cxx.compiler_cxx[0]] + cxx.linker_so[2:]
        else:
            cxx.linker_so = [
             cxx.compiler_cxx[0]] + cxx.linker_so[1:]
        return cxx


    replace_method(CCompiler, 'cxx_compiler', CCompiler_cxx_compiler)
    compiler_class['intel'] = ('intelccompiler', 'IntelCCompiler', 'Intel C Compiler for 32-bit applications')
    compiler_class['intele'] = ('intelccompiler', 'IntelItaniumCCompiler', 'Intel C Itanium Compiler for Itanium-based applications')
    compiler_class['intelem'] = ('intelccompiler', 'IntelEM64TCCompiler', 'Intel C Compiler for 64-bit applications')
    compiler_class['intelw'] = ('intelccompiler', 'IntelCCompilerW', 'Intel C Compiler for 32-bit applications on Windows')
    compiler_class['intelemw'] = ('intelccompiler', 'IntelEM64TCCompilerW', 'Intel C Compiler for 64-bit applications on Windows')
    compiler_class['pathcc'] = ('pathccompiler', 'PathScaleCCompiler', 'PathScale Compiler for SiCortex-based applications')
    ccompiler._default_compilers += (('linux.*', 'intel'), ('linux.*', 'intele'), ('linux.*', 'intelem'),
                                     ('linux.*', 'pathcc'), ('nt', 'intelw'), ('nt', 'intelemw'))
    if sys.platform == 'win32':
        compiler_class['mingw32'] = ('mingw32ccompiler', 'Mingw32CCompiler', 'Mingw32 port of GNU C Compiler for Win32(for MSC built Python)')
        if mingw32():
            log.info('Setting mingw32 as default compiler for nt.')
            ccompiler._default_compilers = (('nt', 'mingw32'), ) + ccompiler._default_compilers
    _distutils_new_compiler = new_compiler

    def new_compiler(plat=None, compiler=None, verbose=None, dry_run=0, force=0):
        if verbose is None:
            verbose = log.get_threshold() <= log.INFO
        if plat is None:
            plat = os.name
        try:
            if compiler is None:
                compiler = get_default_compiler(plat)
            module_name, class_name, long_description = compiler_class[compiler]
        except KeyError:
            msg = "don't know how to compile C/C++ code on platform '%s'" % plat
            if compiler is not None:
                msg = msg + " with '%s' compiler" % compiler
            raise DistutilsPlatformError(msg)
        else:
            module_name = 'numpy.distutils.' + module_name
        try:
            __import__(module_name)
        except ImportError:
            msg = str(get_exception())
            log.info('%s in numpy.distutils; trying from distutils', str(msg))
            module_name = module_name[6:]
            try:
                __import__(module_name)
            except ImportError:
                msg = str(get_exception())
                raise DistutilsModuleError("can't compile C/C++ code: unable to load module '%s'" % module_name)

        else:
            try:
                module = sys.modules[module_name]
                klass = vars(module)[class_name]
            except KeyError:
                raise DistutilsModuleError("can't compile C/C++ code: unable to find class '%s' in module '%s'" % (
                 class_name, module_name))
            else:
                compiler = klass(None, dry_run, force)
                compiler.verbose = verbose
                log.debug('new_compiler returns %s' % klass)
                return compiler


    ccompiler.new_compiler = new_compiler
    _distutils_gen_lib_options = gen_lib_options

    def gen_lib_options(compiler, library_dirs, runtime_library_dirs, libraries):
        r = _distutils_gen_lib_optionscompilerlibrary_dirsruntime_library_dirslibraries
        lib_opts = []
        for i in r:
            if is_sequence(i):
                lib_opts.extend(list(i))
            else:
                lib_opts.append(i)
        else:
            return lib_opts


    ccompiler.gen_lib_options = gen_lib_options
    for _cc in ('msvc9', 'msvc', '_msvc', 'bcpp', 'cygwinc', 'emxc', 'unixc'):
        _m = sys.modules.get('distutils.' + _cc + 'compiler')
        if _m is not None:
            setattr(_m, 'gen_lib_options', gen_lib_options)