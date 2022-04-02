# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\sysconfig.py
"""Provide access to Python's configuration information.  The specific
configuration variables available depend heavily on the platform and
configuration.  The values may be retrieved using
get_config_var(name), and the list of variables is available via
get_config_vars().keys().  Additional convenience functions are also
available.

Written by:   Fred L. Drake, Jr.
Email:        <fdrake@acm.org>
"""
import _imp, os, re, sys
from .errors import DistutilsPlatformError
from .util import get_platform, get_host_platform
PREFIX = os.path.normpath(sys.prefix)
EXEC_PREFIX = os.path.normpath(sys.exec_prefix)
BASE_PREFIX = os.path.normpath(sys.base_prefix)
BASE_EXEC_PREFIX = os.path.normpath(sys.base_exec_prefix)
if '_PYTHON_PROJECT_BASE' in os.environ:
    project_base = os.path.abspath(os.environ['_PYTHON_PROJECT_BASE'])
elif sys.executable:
    project_base = os.path.dirname(os.path.abspath(sys.executable))
else:
    project_base = os.getcwd()

def _is_python_source_dir(d):
    for fn in ('Setup', 'Setup.local'):
        if os.path.isfile(os.path.join(d, 'Modules', fn)):
            return True
    else:
        return False


_sys_home = getattr(sys, '_home', None)
if os.name == 'nt':

    def _fix_pcbuild(d):
        if d:
            if os.path.normcase(d).startswith(os.path.normcase(os.path.join(PREFIX, 'PCbuild'))):
                return PREFIX
        return d


    project_base = _fix_pcbuild(project_base)
    _sys_home = _fix_pcbuild(_sys_home)

def _python_build():
    if _sys_home:
        return _is_python_source_dir(_sys_home)
    return _is_python_source_dir(project_base)


python_build = _python_build()
build_flags = ''
try:
    if not python_build:
        build_flags = sys.abiflags
except AttributeError:
    pass
else:

    def get_python_version():
        """Return a string containing the major and minor Python version,
    leaving off the patchlevel.  Sample return values could be '1.5'
    or '2.2'.
    """
        return '%d.%d' % sys.version_info[:2]


    def get_python_inc(plat_specific=0, prefix=None):
        """Return the directory containing installed Python header files.

    If 'plat_specific' is false (the default), this is the path to the
    non-platform-specific header files, i.e. Python.h and so on;
    otherwise, this is the path to platform-specific header files
    (namely pyconfig.h).

    If 'prefix' is supplied, use it instead of sys.base_prefix or
    sys.base_exec_prefix -- i.e., ignore 'plat_specific'.
    """
        if prefix is None:
            prefix = plat_specific and BASE_EXEC_PREFIX or BASE_PREFIX
        if os.name == 'posix':
            if python_build:
                if plat_specific:
                    return _sys_home or project_base
                incdir = os.path.join(get_config_var('srcdir'), 'Include')
                return os.path.normpath(incdir)
            python_dir = 'python' + get_python_version() + build_flags
            return os.path.join(prefix, 'include', python_dir)
        if os.name == 'nt':
            if python_build:
                return os.path.join(prefix, 'include') + os.path.pathsep + os.path.join(prefix, 'PC')
            return os.path.join(prefix, 'include')
        raise DistutilsPlatformError("I don't know where Python installs its C header files on platform '%s'" % os.name)


    def get_python_lib(plat_specific=0, standard_lib=0, prefix=None):
        """Return the directory containing the Python library (standard or
    site additions).

    If 'plat_specific' is true, return the directory containing
    platform-specific modules, i.e. any module from a non-pure-Python
    module distribution; otherwise, return the platform-shared library
    directory.  If 'standard_lib' is true, return the directory
    containing standard Python library modules; otherwise, return the
    directory for site-specific modules.

    If 'prefix' is supplied, use it instead of sys.base_prefix or
    sys.base_exec_prefix -- i.e., ignore 'plat_specific'.
    """
        if prefix is None:
            if standard_lib:
                prefix = plat_specific and BASE_EXEC_PREFIX or BASE_PREFIX
            else:
                prefix = plat_specific and EXEC_PREFIX or PREFIX
        if os.name == 'posix':
            libpython = os.path.join(prefix, 'lib', 'python' + get_python_version())
            if standard_lib:
                return libpython
            return os.path.join(libpython, 'site-packages')
        elif os.name == 'nt':
            if standard_lib:
                return os.path.join(prefix, 'Lib')
            return os.path.join(prefix, 'Lib', 'site-packages')
        else:
            raise DistutilsPlatformError("I don't know where Python installs its library on platform '%s'" % os.name)


    def customize_compiler(compiler):
        """Do any platform-specific customization of a CCompiler instance.

    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
        global _config_vars
        if compiler.compiler_type == 'unix':
            if sys.platform == 'darwin':
                if not get_config_var('CUSTOMIZED_OSX_COMPILER'):
                    import _osx_support
                    _osx_support.customize_compiler(_config_vars)
                    _config_vars['CUSTOMIZED_OSX_COMPILER'] = 'True'
                cc, cxx, cflags, ccshared, ldshared, shlib_suffix, ar, ar_flags = get_config_vars('CC', 'CXX', 'CFLAGS', 'CCSHARED', 'LDSHARED', 'SHLIB_SUFFIX', 'AR', 'ARFLAGS')
                if 'CC' in os.environ:
                    newcc = os.environ['CC']
                    if sys.platform == 'darwin':
                        if 'LDSHARED' not in os.environ:
                            if ldshared.startswith(cc):
                                ldshared = newcc + ldshared[len(cc):]
                    cc = newcc
                if 'CXX' in os.environ:
                    cxx = os.environ['CXX']
                if 'LDSHARED' in os.environ:
                    ldshared = os.environ['LDSHARED']
                if 'CPP' in os.environ:
                    cpp = os.environ['CPP']
                else:
                    cpp = cc + ' -E'
                if 'LDFLAGS' in os.environ:
                    ldshared = ldshared + ' ' + os.environ['LDFLAGS']
                if 'CFLAGS' in os.environ:
                    cflags = cflags + ' ' + os.environ['CFLAGS']
                    ldshared = ldshared + ' ' + os.environ['CFLAGS']
                if 'CPPFLAGS' in os.environ:
                    cpp = cpp + ' ' + os.environ['CPPFLAGS']
                    cflags = cflags + ' ' + os.environ['CPPFLAGS']
                    ldshared = ldshared + ' ' + os.environ['CPPFLAGS']
                if 'AR' in os.environ:
                    ar = os.environ['AR']
                if 'ARFLAGS' in os.environ:
                    archiver = ar + ' ' + os.environ['ARFLAGS']
                else:
                    archiver = ar + ' ' + ar_flags
                cc_cmd = cc + ' ' + cflags
                compiler.set_executables(preprocessor=cpp,
                  compiler=cc_cmd,
                  compiler_so=(cc_cmd + ' ' + ccshared),
                  compiler_cxx=cxx,
                  linker_so=ldshared,
                  linker_exe=cc,
                  archiver=archiver)
                compiler.shared_lib_extension = shlib_suffix


    def get_config_h_filename():
        """Return full pathname of installed pyconfig.h file."""
        if python_build:
            if os.name == 'nt':
                inc_dir = os.path.join(_sys_home or project_base, 'PC')
            else:
                inc_dir = _sys_home or project_base
        else:
            inc_dir = get_python_inc(plat_specific=1)
        return os.path.join(inc_dir, 'pyconfig.h')


    def get_makefile_filename():
        """Return full pathname of installed Makefile from the Python build."""
        if python_build:
            return os.path.join(_sys_home or project_base, 'Makefile')
        lib_dir = get_python_lib(plat_specific=0, standard_lib=1)
        config_file = 'config-{}{}'.format(get_python_version(), build_flags)
        if hasattr(sys.implementation, '_multiarch'):
            config_file += '-%s' % sys.implementation._multiarch
        return os.path.join(lib_dir, config_file, 'Makefile')


    def parse_config_h--- This code section failed: ---

 L. 271         0  LOAD_FAST                'g'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 272         8  BUILD_MAP_0           0 
               10  STORE_FAST               'g'
             12_0  COME_FROM             6  '6'

 L. 273        12  LOAD_GLOBAL              re
               14  LOAD_METHOD              compile
               16  LOAD_STR                 '#define ([A-Z][A-Za-z0-9_]+) (.*)\n'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'define_rx'

 L. 274        22  LOAD_GLOBAL              re
               24  LOAD_METHOD              compile
               26  LOAD_STR                 '/[*] #undef ([A-Z][A-Za-z0-9_]+) [*]/\n'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'undef_rx'
             32_0  COME_FROM           148  '148'
             32_1  COME_FROM           132  '132'
             32_2  COME_FROM           118  '118'

 L. 277        32  LOAD_FAST                'fp'
               34  LOAD_METHOD              readline
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'line'

 L. 278        40  LOAD_FAST                'line'
               42  POP_JUMP_IF_TRUE     46  'to 46'

 L. 279        44  JUMP_FORWARD        150  'to 150'
             46_0  COME_FROM            42  '42'

 L. 280        46  LOAD_FAST                'define_rx'
               48  LOAD_METHOD              match
               50  LOAD_FAST                'line'
               52  CALL_METHOD_1         1  ''
               54  STORE_FAST               'm'

 L. 281        56  LOAD_FAST                'm'
               58  POP_JUMP_IF_FALSE   120  'to 120'

 L. 282        60  LOAD_FAST                'm'
               62  LOAD_METHOD              group
               64  LOAD_CONST               1
               66  LOAD_CONST               2
               68  CALL_METHOD_2         2  ''
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'n'
               74  STORE_FAST               'v'

 L. 283        76  SETUP_FINALLY        90  'to 90'

 L. 283        78  LOAD_GLOBAL              int
               80  LOAD_FAST                'v'
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'v'
               86  POP_BLOCK        
               88  JUMP_FORWARD        110  'to 110'
             90_0  COME_FROM_FINALLY    76  '76'

 L. 284        90  DUP_TOP          
               92  LOAD_GLOBAL              ValueError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   108  'to 108'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 284       104  POP_EXCEPT       
              106  BREAK_LOOP          110  'to 110'
            108_0  COME_FROM            96  '96'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            88  '88'

 L. 285       110  LOAD_FAST                'v'
              112  LOAD_FAST                'g'
              114  LOAD_FAST                'n'
              116  STORE_SUBSCR     
              118  JUMP_BACK            32  'to 32'
            120_0  COME_FROM            58  '58'

 L. 287       120  LOAD_FAST                'undef_rx'
              122  LOAD_METHOD              match
              124  LOAD_FAST                'line'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'm'

 L. 288       130  LOAD_FAST                'm'
              132  POP_JUMP_IF_FALSE_BACK    32  'to 32'

 L. 289       134  LOAD_CONST               0
              136  LOAD_FAST                'g'
              138  LOAD_FAST                'm'
              140  LOAD_METHOD              group
              142  LOAD_CONST               1
              144  CALL_METHOD_1         1  ''
              146  STORE_SUBSCR     
              148  JUMP_BACK            32  'to 32'
            150_0  COME_FROM            44  '44'

 L. 290       150  LOAD_FAST                'g'
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 108


    _variable_rx = re.compile('([a-zA-Z][a-zA-Z0-9_]+)\\s*=\\s*(.*)')
    _findvar1_rx = re.compile('\\$\\(([A-Za-z][A-Za-z0-9_]*)\\)')
    _findvar2_rx = re.compile('\\${([A-Za-z][A-Za-z0-9_]*)}')

    def parse_makefile(fn, g=None):
        """Parse a Makefile-style file.

    A dictionary containing name/value pairs is returned.  If an
    optional dictionary is passed in as the second argument, it is
    used instead of a new dictionary.
    """
        from distutils.text_file import TextFile
        fp = TextFile(fn, strip_comments=1, skip_blanks=1, join_lines=1, errors='surrogateescape')
        if g is None:
            g = {}
        done = {}
        notdone = {}
        while True:
            while True:
                line = fp.readline()
                if line is None:
                    pass
                else:
                    m = _variable_rx.match(line)
                    if m:
                        n, v = m.group(1, 2)
                        v = v.strip()
                        tmpv = v.replace('$$', '')
                    if '$' in tmpv:
                        notdone[n] = v

            try:
                v = int(v)
            except ValueError:
                done[n] = v.replace('$$', '$')
            else:
                done[n] = v

        renamed_variables = ('CFLAGS', 'LDFLAGS', 'CPPFLAGS')
        while notdone:
            for name in list(notdone):
                value = notdone[name]
                m = _findvar1_rx.search(value) or _findvar2_rx.search(value)
                if m:
                    n = m.group(1)
                    found = True
                    if n in done:
                        item = str(done[n])
                    elif n in notdone:
                        found = False
                    elif n in os.environ:
                        item = os.environ[n]
                    elif n in renamed_variables:
                        if name.startswith('PY_') and name[3:] in renamed_variables:
                            item = ''
                        elif 'PY_' + n in notdone:
                            found = False
                        else:
                            item = str(done[('PY_' + n)])
                    else:
                        done[n] = item = ''
                    if found:
                        after = value[m.end():]
                        value = value[:m.start()] + item + after
                        if '$' in after:
                            notdone[name] = value
                        else:
                            try:
                                value = int(value)
                            except ValueError:
                                done[name] = value.strip()
                            else:
                                done[name] = value
                            del notdone[name]
                            if name.startswith('PY_') and name[3:] in renamed_variables:
                                name = name[3:]
                                if name not in done:
                                    done[name] = value
                            else:
                                del notdone[name]

        fp.close()
        for k, v in done.items():
            if isinstance(v, str):
                done[k] = v.strip()
        else:
            g.update(done)
            return g


    def expand_makefile_vars--- This code section failed: ---
              0_0  COME_FROM            80  '80'
              0_1  COME_FROM            76  '76'

 L. 421         0  LOAD_GLOBAL              _findvar1_rx
                2  LOAD_METHOD              search
                4  LOAD_FAST                's'
                6  CALL_METHOD_1         1  ''
                8  JUMP_IF_TRUE_OR_POP    18  'to 18'
               10  LOAD_GLOBAL              _findvar2_rx
               12  LOAD_METHOD              search
               14  LOAD_FAST                's'
               16  CALL_METHOD_1         1  ''
             18_0  COME_FROM             8  '8'
               18  STORE_FAST               'm'

 L. 422        20  LOAD_FAST                'm'
               22  POP_JUMP_IF_FALSE    82  'to 82'

 L. 423        24  LOAD_FAST                'm'
               26  LOAD_METHOD              span
               28  CALL_METHOD_0         0  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'beg'
               34  STORE_FAST               'end'

 L. 424        36  LOAD_FAST                's'
               38  LOAD_CONST               0
               40  LOAD_FAST                'beg'
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_FAST                'vars'
               48  LOAD_METHOD              get
               50  LOAD_FAST                'm'
               52  LOAD_METHOD              group
               54  LOAD_CONST               1
               56  CALL_METHOD_1         1  ''
               58  CALL_METHOD_1         1  ''
               60  BINARY_ADD       
               62  LOAD_FAST                's'
               64  LOAD_FAST                'end'
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  BINARY_ADD       
               74  STORE_FAST               's'
               76  JUMP_BACK             0  'to 0'

 L. 426        78  JUMP_FORWARD         82  'to 82'
               80  JUMP_BACK             0  'to 0'
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            22  '22'

 L. 427        82  LOAD_FAST                's'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 78


    _config_vars = None

    def _init_posix():
        """Initialize the module as appropriate for POSIX systems."""
        global _config_vars
        name = os.environ.get('_PYTHON_SYSCONFIGDATA_NAME', '_sysconfigdata_{abi}_{platform}_{multiarch}'.format(abi=(sys.abiflags),
          platform=(sys.platform),
          multiarch=(getattr(sys.implementation, '_multiarch', ''))))
        _temp = __import__(name, globals(), locals(), ['build_time_vars'], 0)
        build_time_vars = _temp.build_time_vars
        _config_vars = {}
        _config_vars.update(build_time_vars)


    def _init_nt():
        """Initialize the module as appropriate for NT"""
        global _config_vars
        g = {}
        g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
        g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)
        g['INCLUDEPY'] = get_python_inc(plat_specific=0)
        g['EXT_SUFFIX'] = _imp.extension_suffixes()[0]
        g['EXE'] = '.exe'
        g['VERSION'] = get_python_version().replace('.', '')
        g['BINDIR'] = os.path.dirname(os.path.abspath(sys.executable))
        _config_vars = g


    def get_config_vars(*args):
        """With no arguments, return a dictionary of all configuration
    variables relevant for the current platform.  Generally this includes
    everything needed to build extensions and install both pure modules and
    extensions.  On Unix, this means every variable defined in Python's
    installed Makefile; on Windows it's a much smaller set.

    With arguments, return a list of values that result from looking up
    each argument in the configuration variable dictionary.
    """
        global _config_vars
        if _config_vars is None:
            func = globals().get('_init_' + os.name)
            if func:
                func()
            else:
                _config_vars = {}
            _config_vars['prefix'] = PREFIX
            _config_vars['exec_prefix'] = EXEC_PREFIX
            SO = _config_vars.get('EXT_SUFFIX')
            if SO is not None:
                _config_vars['SO'] = SO
            srcdir = _config_vars.get('srcdir', project_base)
            if os.name == 'posix':
                if python_build:
                    base = os.path.dirname(get_makefile_filename())
                    srcdir = os.path.join(base, srcdir)
                else:
                    srcdir = os.path.dirname(get_makefile_filename())
            _config_vars['srcdir'] = os.path.abspath(os.path.normpath(srcdir))
            if not python_build or os.name == 'posix':
                base = project_base
                if not os.path.isabs(_config_vars['srcdir']):
                    if base != os.getcwd():
                        srcdir = os.path.join(base, _config_vars['srcdir'])
                        _config_vars['srcdir'] = os.path.normpath(srcdir)
                if sys.platform == 'darwin':
                    import _osx_support
                    _osx_support.customize_config_vars(_config_vars)
        if args:
            vals = []
            for name in args:
                vals.append(_config_vars.get(name))
            else:
                return vals

        return _config_vars


    def get_config_var(name):
        """Return the value of a single variable using the dictionary
    returned by 'get_config_vars()'.  Equivalent to
    get_config_vars().get(name)
    """
        if name == 'SO':
            import warnings
            warnings.warn('SO is deprecated, use EXT_SUFFIX', DeprecationWarning, 2)
        return get_config_vars().get(name)