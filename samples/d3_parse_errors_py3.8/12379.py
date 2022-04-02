# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: sysconfig.py
"""Access to Python's configuration information."""
import os, sys
from os.path import pardir, realpath
__all__ = [
 'get_config_h_filename',
 'get_config_var',
 'get_config_vars',
 'get_makefile_filename',
 'get_path',
 'get_path_names',
 'get_paths',
 'get_platform',
 'get_python_version',
 'get_scheme_names',
 'parse_config_h']
_INSTALL_SCHEMES = {'posix_prefix':{'stdlib':'{installed_base}/lib/python{py_version_short}', 
  'platstdlib':'{platbase}/lib/python{py_version_short}', 
  'purelib':'{base}/lib/python{py_version_short}/site-packages', 
  'platlib':'{platbase}/lib/python{py_version_short}/site-packages', 
  'include':'{installed_base}/include/python{py_version_short}{abiflags}', 
  'platinclude':'{installed_platbase}/include/python{py_version_short}{abiflags}', 
  'scripts':'{base}/bin', 
  'data':'{base}'}, 
 'posix_home':{'stdlib':'{installed_base}/lib/python', 
  'platstdlib':'{base}/lib/python', 
  'purelib':'{base}/lib/python', 
  'platlib':'{base}/lib/python', 
  'include':'{installed_base}/include/python', 
  'platinclude':'{installed_base}/include/python', 
  'scripts':'{base}/bin', 
  'data':'{base}'}, 
 'nt':{'stdlib':'{installed_base}/Lib', 
  'platstdlib':'{base}/Lib', 
  'purelib':'{base}/Lib/site-packages', 
  'platlib':'{base}/Lib/site-packages', 
  'include':'{installed_base}/Include', 
  'platinclude':'{installed_base}/Include', 
  'scripts':'{base}/Scripts', 
  'data':'{base}'}, 
 'nt_user':{'stdlib':'{userbase}/Python{py_version_nodot}', 
  'platstdlib':'{userbase}/Python{py_version_nodot}', 
  'purelib':'{userbase}/Python{py_version_nodot}/site-packages', 
  'platlib':'{userbase}/Python{py_version_nodot}/site-packages', 
  'include':'{userbase}/Python{py_version_nodot}/Include', 
  'scripts':'{userbase}/Python{py_version_nodot}/Scripts', 
  'data':'{userbase}'}, 
 'posix_user':{'stdlib':'{userbase}/lib/python{py_version_short}', 
  'platstdlib':'{userbase}/lib/python{py_version_short}', 
  'purelib':'{userbase}/lib/python{py_version_short}/site-packages', 
  'platlib':'{userbase}/lib/python{py_version_short}/site-packages', 
  'include':'{userbase}/include/python{py_version_short}', 
  'scripts':'{userbase}/bin', 
  'data':'{userbase}'}, 
 'osx_framework_user':{'stdlib':'{userbase}/lib/python', 
  'platstdlib':'{userbase}/lib/python', 
  'purelib':'{userbase}/lib/python/site-packages', 
  'platlib':'{userbase}/lib/python/site-packages', 
  'include':'{userbase}/include', 
  'scripts':'{userbase}/bin', 
  'data':'{userbase}'}}
_SCHEME_KEYS = ('stdlib', 'platstdlib', 'purelib', 'platlib', 'include', 'scripts',
                'data')
_PY_VERSION = sys.version.split()[0]
_PY_VERSION_SHORT = '%d.%d' % sys.version_info[:2]
_PY_VERSION_SHORT_NO_DOT = '%d%d' % sys.version_info[:2]
_PREFIX = os.path.normpath(sys.prefix)
_BASE_PREFIX = os.path.normpath(sys.base_prefix)
_EXEC_PREFIX = os.path.normpath(sys.exec_prefix)
_BASE_EXEC_PREFIX = os.path.normpath(sys.base_exec_prefix)
_CONFIG_VARS = None
_USER_BASE = None

def _safe_realpath(path):
    try:
        return realpath(path)
    except OSError:
        return path


if sys.executable:
    _PROJECT_BASE = os.path.dirname(_safe_realpath(sys.executable))
else:
    _PROJECT_BASE = _safe_realpath(os.getcwd())
if os.name == 'nt':
    if _PROJECT_BASE.lower().endswith(('\\pcbuild\\win32', '\\pcbuild\\amd64')):
        _PROJECT_BASE = _safe_realpath(os.path.join(_PROJECT_BASE, pardir, pardir))
if '_PYTHON_PROJECT_BASE' in os.environ:
    _PROJECT_BASE = _safe_realpath(os.environ['_PYTHON_PROJECT_BASE'])

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
            if os.path.normcase(d).startswith(os.path.normcase(os.path.join(_PREFIX, 'PCbuild'))):
                return _PREFIX
        return d


    _PROJECT_BASE = _fix_pcbuild(_PROJECT_BASE)
    _sys_home = _fix_pcbuild(_sys_home)

def is_python_build(check_home=False):
    if check_home:
        if _sys_home:
            return _is_python_source_dir(_sys_home)
    return _is_python_source_dir(_PROJECT_BASE)


_PYTHON_BUILD = is_python_build(True)
if _PYTHON_BUILD:
    for scheme in ('posix_prefix', 'posix_home'):
        _INSTALL_SCHEMES[scheme]['include'] = '{srcdir}/Include'
        _INSTALL_SCHEMES[scheme]['platinclude'] = '{projectbase}/.'
    else:

        def _subst_vars--- This code section failed: ---

 L. 152         0  SETUP_FINALLY        16  'to 16'

 L. 153         2  LOAD_FAST                's'
                4  LOAD_ATTR                format
                6  BUILD_TUPLE_0         0 
                8  LOAD_FAST                'local_vars'
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 154        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE   104  'to 104'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 155        30  SETUP_FINALLY        52  'to 52'

 L. 156        32  LOAD_FAST                's'
               34  LOAD_ATTR                format
               36  BUILD_TUPLE_0         0 
               38  LOAD_GLOBAL              os
               40  LOAD_ATTR                environ
               42  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               44  POP_BLOCK        
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    30  '30'

 L. 157        52  DUP_TOP          
               54  LOAD_GLOBAL              KeyError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    98  'to 98'
               60  POP_TOP          
               62  STORE_FAST               'var'
               64  POP_TOP          
               66  SETUP_FINALLY        86  'to 86'

 L. 158        68  LOAD_GLOBAL              AttributeError
               70  LOAD_STR                 '{%s}'
               72  LOAD_FAST                'var'
               74  BINARY_MODULO    
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               None
               80  RAISE_VARARGS_2       2  'exception instance with __cause__'
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM_FINALLY    66  '66'
               86  LOAD_CONST               None
               88  STORE_FAST               'var'
               90  DELETE_FAST              'var'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            58  '58'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            22  '22'
              104  END_FINALLY      
            106_0  COME_FROM           102  '102'

Parse error at or near `ROT_FOUR' instruction at offset 46


        def _extend_dict(target_dict, other_dict):
            target_keys = target_dict.keys()
            for key, value in other_dict.items():
                if key in target_keys:
                    pass
                else:
                    target_dict[key] = value


        def _expand_vars(scheme, vars):
            res = {}
            if vars is None:
                vars = {}
            _extend_dict(vars, get_config_vars())
            for key, value in _INSTALL_SCHEMES[scheme].items():
                if os.name in ('posix', 'nt'):
                    value = os.path.expanduser(value)
                else:
                    res[key] = os.path.normpath(_subst_vars(value, vars))
            else:
                return res


        def _get_default_scheme():
            if os.name == 'posix':
                return 'posix_prefix'
            return os.name


        def _getuserbase():
            env_base = os.environ.get('PYTHONUSERBASE', None)
            if env_base:
                return env_base

            def joinuser(*args):
                return os.path.expanduser((os.path.join)(*args))

            if os.name == 'nt':
                base = os.environ.get('APPDATA') or '~'
                return joinuser(base, 'Python')
            if sys.platform == 'darwin':
                if sys._framework:
                    return joinuser('~', 'Library', sys._framework, '%d.%d' % sys.version_info[:2])
            return joinuser('~', '.local')


        def _parse_makefile(filename, vars=None):
            """Parse a Makefile-style file.

    A dictionary containing name/value pairs is returned.  If an
    optional dictionary is passed in as the second argument, it is
    used instead of a new dictionary.
    """
            import re
            _variable_rx = re.compile('([a-zA-Z][a-zA-Z0-9_]+)\\s*=\\s*(.*)')
            _findvar1_rx = re.compile('\\$\\(([A-Za-z][A-Za-z0-9_]*)\\)')
            _findvar2_rx = re.compile('\\${([A-Za-z][A-Za-z0-9_]*)}')
            if vars is None:
                vars = {}
            done = {}
            notdone = {}
            with open(filename, errors='surrogateescape') as f:
                lines = f.readlines()
            for line in lines:
                if not line.startswith('#'):
                    if line.strip() == '':
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
            else:
                variables = list(notdone.keys())
                renamed_variables = ('CFLAGS', 'LDFLAGS', 'CPPFLAGS')
                while len(variables) > 0:
                    for name in tuple(variables):
                        value = notdone[name]
                        m1 = _findvar1_rx.search(value)
                        m2 = _findvar2_rx.search(value)
                        if m1 and m2:
                            m = m1 if m1.start() < m2.start() else m2
                        else:
                            m = m1 if m1 else m2
                        if m is not None:
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
                                    variables.remove(name)
                                    if name.startswith('PY_') and name[3:] in renamed_variables:
                                        name = name[3:]
                                        if name not in done:
                                            done[name] = value
                                    else:
                                        done[name] = value
                                        variables.remove(name)

                for k, v in done.items():
                    if isinstance(v, str):
                        done[k] = v.strip()
                else:
                    vars.update(done)
                    return vars


        def get_makefile_filename():
            """Return the path of the Makefile."""
            if _PYTHON_BUILD:
                return os.path.join(_sys_home or _PROJECT_BASE, 'Makefile')
            if hasattr(sys, 'abiflags'):
                config_dir_name = 'config-%s%s' % (_PY_VERSION_SHORT, sys.abiflags)
            else:
                config_dir_name = 'config'
            if hasattr(sys.implementation, '_multiarch'):
                config_dir_name += '-%s' % sys.implementation._multiarch
            return os.path.join(get_path('stdlib'), config_dir_name, 'Makefile')


        def _get_sysconfigdata_name():
            return os.environ.get('_PYTHON_SYSCONFIGDATA_NAME', '_sysconfigdata_{abi}_{platform}_{multiarch}'.format(abi=(sys.abiflags),
              platform=(sys.platform),
              multiarch=(getattr(sys.implementation, '_multiarch', ''))))


        def _generate_posix_vars():
            """Generate the Python module containing build-time variables."""
            import pprint
            vars = {}
            makefile = get_makefile_filename()
            try:
                _parse_makefile(makefile, vars)
            except OSError as e:
                try:
                    msg = 'invalid Python installation: unable to open %s' % makefile
                    if hasattr(e, 'strerror'):
                        msg = msg + ' (%s)' % e.strerror
                    raise OSError(msg)
                finally:
                    e = None
                    del e

            else:
                config_h = get_config_h_filename()
                try:
                    with open(config_h) as f:
                        parse_config_h(f, vars)
                except OSError as e:
                    try:
                        msg = 'invalid Python installation: unable to open %s' % config_h
                        if hasattr(e, 'strerror'):
                            msg = msg + ' (%s)' % e.strerror
                        raise OSError(msg)
                    finally:
                        e = None
                        del e

                else:
                    if _PYTHON_BUILD:
                        vars['BLDSHARED'] = vars['LDSHARED']
                    name = _get_sysconfigdata_name()
                    if 'darwin' in sys.platform:
                        import types
                        module = types.ModuleType(name)
                        module.build_time_vars = vars
                        sys.modules[name] = module
                    pybuilddir = 'build/lib.%s-%s' % (get_platform(), _PY_VERSION_SHORT)
                    if hasattr(sys, 'gettotalrefcount'):
                        pybuilddir += '-pydebug'
                    os.makedirs(pybuilddir, exist_ok=True)
                    destfile = os.path.join(pybuilddir, name + '.py')
                    with open(destfile, 'w', encoding='utf8') as f:
                        f.write('# system configuration generated and used by the sysconfig module\n')
                        f.write('build_time_vars = ')
                        pprint.pprint(vars, stream=f)
                    with open('pybuilddir.txt', 'w', encoding='utf8') as f:
                        f.write(pybuilddir)


        def _init_posix(vars):
            """Initialize the module as appropriate for POSIX systems."""
            name = _get_sysconfigdata_name()
            _temp = __import__(name, globals(), locals(), ['build_time_vars'], 0)
            build_time_vars = _temp.build_time_vars
            vars.update(build_time_vars)


        def _init_non_posix(vars):
            """Initialize the module as appropriate for NT"""
            import _imp
            vars['LIBDEST'] = get_path('stdlib')
            vars['BINLIBDEST'] = get_path('platstdlib')
            vars['INCLUDEPY'] = get_path('include')
            vars['EXT_SUFFIX'] = _imp.extension_suffixes()[0]
            vars['EXE'] = '.exe'
            vars['VERSION'] = _PY_VERSION_SHORT_NO_DOT
            vars['BINDIR'] = os.path.dirname(_safe_realpath(sys.executable))


        def parse_config_h--- This code section failed: ---

 L. 450         0  LOAD_FAST                'vars'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 451         8  BUILD_MAP_0           0 
               10  STORE_FAST               'vars'
             12_0  COME_FROM             6  '6'

 L. 452        12  LOAD_CONST               0
               14  LOAD_CONST               None
               16  IMPORT_NAME              re
               18  STORE_FAST               're'

 L. 453        20  LOAD_FAST                're'
               22  LOAD_METHOD              compile
               24  LOAD_STR                 '#define ([A-Z][A-Za-z0-9_]+) (.*)\n'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'define_rx'

 L. 454        30  LOAD_FAST                're'
               32  LOAD_METHOD              compile
               34  LOAD_STR                 '/[*] #undef ([A-Z][A-Za-z0-9_]+) [*]/\n'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'undef_rx'
             40_0  COME_FROM           156  '156'
             40_1  COME_FROM           140  '140'
             40_2  COME_FROM           126  '126'

 L. 457        40  LOAD_FAST                'fp'
               42  LOAD_METHOD              readline
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'line'

 L. 458        48  LOAD_FAST                'line'
               50  POP_JUMP_IF_TRUE     54  'to 54'

 L. 459        52  JUMP_FORWARD        158  'to 158'
             54_0  COME_FROM            50  '50'

 L. 460        54  LOAD_FAST                'define_rx'
               56  LOAD_METHOD              match
               58  LOAD_FAST                'line'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'm'

 L. 461        64  LOAD_FAST                'm'
               66  POP_JUMP_IF_FALSE   128  'to 128'

 L. 462        68  LOAD_FAST                'm'
               70  LOAD_METHOD              group
               72  LOAD_CONST               1
               74  LOAD_CONST               2
               76  CALL_METHOD_2         2  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'n'
               82  STORE_FAST               'v'

 L. 463        84  SETUP_FINALLY        98  'to 98'

 L. 464        86  LOAD_GLOBAL              int
               88  LOAD_FAST                'v'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'v'
               94  POP_BLOCK        
               96  JUMP_FORWARD        118  'to 118'
             98_0  COME_FROM_FINALLY    84  '84'

 L. 465        98  DUP_TOP          
              100  LOAD_GLOBAL              ValueError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   116  'to 116'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 466       112  POP_EXCEPT       
              114  BREAK_LOOP          118  'to 118'
            116_0  COME_FROM           104  '104'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            96  '96'

 L. 467       118  LOAD_FAST                'v'
              120  LOAD_FAST                'vars'
              122  LOAD_FAST                'n'
              124  STORE_SUBSCR     
              126  JUMP_BACK            40  'to 40'
            128_0  COME_FROM            66  '66'

 L. 469       128  LOAD_FAST                'undef_rx'
              130  LOAD_METHOD              match
              132  LOAD_FAST                'line'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'm'

 L. 470       138  LOAD_FAST                'm'
              140  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L. 471       142  LOAD_CONST               0
              144  LOAD_FAST                'vars'
              146  LOAD_FAST                'm'
              148  LOAD_METHOD              group
              150  LOAD_CONST               1
              152  CALL_METHOD_1         1  ''
              154  STORE_SUBSCR     
              156  JUMP_BACK            40  'to 40'
            158_0  COME_FROM            52  '52'

 L. 472       158  LOAD_FAST                'vars'
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 116


        def get_config_h_filename():
            """Return the path of pyconfig.h."""
            if _PYTHON_BUILD:
                if os.name == 'nt':
                    inc_dir = os.path.join(_sys_home or _PROJECT_BASE, 'PC')
                else:
                    inc_dir = _sys_home or _PROJECT_BASE
            else:
                inc_dir = get_path('platinclude')
            return os.path.join(inc_dir, 'pyconfig.h')


        def get_scheme_names():
            """Return a tuple containing the schemes names."""
            return tuple(sorted(_INSTALL_SCHEMES))


        def get_path_names():
            """Return a tuple containing the paths names."""
            return _SCHEME_KEYS


        def get_paths(scheme=_get_default_scheme(), vars=None, expand=True):
            """Return a mapping containing an install scheme.

    ``scheme`` is the install scheme name. If not provided, it will
    return the default scheme for the current platform.
    """
            if expand:
                return _expand_vars(scheme, vars)
            return _INSTALL_SCHEMES[scheme]


        def get_path(name, scheme=_get_default_scheme(), vars=None, expand=True):
            """Return a path corresponding to the scheme.

    ``scheme`` is the install scheme name.
    """
            return get_paths(scheme, vars, expand)[name]


        def get_config_vars(*args):
            """With no arguments, return a dictionary of all configuration
    variables relevant for the current platform.

    On Unix, this means every variable defined in Python's installed Makefile;
    On Windows it's a much smaller set.

    With arguments, return a list of values that result from looking up
    each argument in the configuration variable dictionary.
    """
            global _CONFIG_VARS
            if _CONFIG_VARS is None:
                _CONFIG_VARS = {}
                _CONFIG_VARS['prefix'] = _PREFIX
                _CONFIG_VARS['exec_prefix'] = _EXEC_PREFIX
                _CONFIG_VARS['py_version'] = _PY_VERSION
                _CONFIG_VARS['py_version_short'] = _PY_VERSION_SHORT
                _CONFIG_VARS['py_version_nodot'] = _PY_VERSION_SHORT_NO_DOT
                _CONFIG_VARS['installed_base'] = _BASE_PREFIX
                _CONFIG_VARS['base'] = _PREFIX
                _CONFIG_VARS['installed_platbase'] = _BASE_EXEC_PREFIX
                _CONFIG_VARS['platbase'] = _EXEC_PREFIX
                _CONFIG_VARS['projectbase'] = _PROJECT_BASE
                try:
                    _CONFIG_VARS['abiflags'] = sys.abiflags
                except AttributeError:
                    _CONFIG_VARS['abiflags'] = ''
                else:
                    if os.name == 'nt':
                        _init_non_posix(_CONFIG_VARS)
                    if os.name == 'posix':
                        _init_posix(_CONFIG_VARS)
                    SO = _CONFIG_VARS.get('EXT_SUFFIX')
                    if SO is not None:
                        _CONFIG_VARS['SO'] = SO
                    _CONFIG_VARS['userbase'] = _getuserbase()
                    srcdir = _CONFIG_VARS.get('srcdir', _PROJECT_BASE)
                    if os.name == 'posix':
                        if _PYTHON_BUILD:
                            base = os.path.dirname(get_makefile_filename())
                            srcdir = os.path.join(base, srcdir)
                        else:
                            srcdir = os.path.dirname(get_makefile_filename())
                    _CONFIG_VARS['srcdir'] = _safe_realpath(srcdir)
                    if sys.platform == 'darwin':
                        import _osx_support
                        _osx_support.customize_config_vars(_CONFIG_VARS)
                if args:
                    vals = []
                    for name in args:
                        vals.append(_CONFIG_VARS.get(name))
                    else:
                        return vals

                return _CONFIG_VARS


        def get_config_var(name):
            """Return the value of a single variable using the dictionary returned by
    'get_config_vars()'.

    Equivalent to get_config_vars().get(name)
    """
            if name == 'SO':
                import warnings
                warnings.warn('SO is deprecated, use EXT_SUFFIX', DeprecationWarning, 2)
            return get_config_vars().get(name)


        def get_platform():
            """Return a string that identifies the current platform.

    This is used mainly to distinguish platform-specific build directories and
    platform-specific built distributions.  Typically includes the OS name and
    version and the architecture (as supplied by 'os.uname()'), although the
    exact information included depends on the OS; on Linux, the kernel version
    isn't particularly important.

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
            if not (os.name != 'posix' or hasattr(os, 'uname')):
                return sys.platform
            if '_PYTHON_HOST_PLATFORM' in os.environ:
                return os.environ['_PYTHON_HOST_PLATFORM']
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
                    import re
                    rel_re = re.compile('[\\d.]+')
                    m = rel_re.match(release)
                    if m:
                        release = m.group()
                elif osname[:6] == 'darwin':
                    import _osx_support
                    osname, release, machine = _osx_support.get_platform_osx(get_config_vars(), osname, release, machine)
            return '%s-%s-%s' % (osname, release, machine)


        def get_python_version():
            return _PY_VERSION_SHORT


        def _print_dict(title, data):
            for index, (key, value) in enumerate(sorted(data.items())):
                if index == 0:
                    print('%s: ' % title)
                else:
                    print('\t%s = "%s"' % (key, value))


        def _main():
            """Display all information sysconfig detains."""
            if '--generate-posix-vars' in sys.argv:
                _generate_posix_vars()
                return
            print('Platform: "%s"' % get_platform())
            print('Python version: "%s"' % get_python_version())
            print('Current installation scheme: "%s"' % _get_default_scheme())
            print()
            _print_dict('Paths', get_paths())
            print()
            _print_dict('Variables', get_config_vars())


        if __name__ == '__main__':
            _main()