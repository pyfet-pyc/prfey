# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: _osx_support.py
"""Shared OS X support functions."""
import os, re, sys
__all__ = [
 'compiler_fixup',
 'customize_config_vars',
 'customize_compiler',
 'get_platform_osx']
_UNIVERSAL_CONFIG_VARS = ('CFLAGS', 'LDFLAGS', 'CPPFLAGS', 'BASECFLAGS', 'BLDSHARED',
                          'LDSHARED', 'CC', 'CXX', 'PY_CFLAGS', 'PY_LDFLAGS', 'PY_CPPFLAGS',
                          'PY_CORE_CFLAGS', 'PY_CORE_LDFLAGS')
_COMPILER_CONFIG_VARS = ('BLDSHARED', 'LDSHARED', 'CC', 'CXX')
_INITPRE = '_OSX_SUPPORT_INITIAL_'

def _find_executable(executable, path=None):
    """Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    base, ext = os.path.splitext(executable)
    if sys.platform == 'win32':
        if ext != '.exe':
            executable = executable + '.exe'
    for p in os.path.isfile(executable) or paths:
        f = os.path.join(p, executable)
        if os.path.isfile(f):
            return f
        return
        return executable


def _read_output--- This code section failed: ---

 L.  61         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              contextlib
                6  STORE_FAST               'contextlib'

 L.  62         8  SETUP_FINALLY        30  'to 30'

 L.  63        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              tempfile
               16  STORE_FAST               'tempfile'

 L.  64        18  LOAD_FAST                'tempfile'
               20  LOAD_METHOD              NamedTemporaryFile
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'fp'
               26  POP_BLOCK        
               28  JUMP_FORWARD         70  'to 70'
             30_0  COME_FROM_FINALLY     8  '8'

 L.  65        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    68  'to 68'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  66        44  LOAD_GLOBAL              open
               46  LOAD_STR                 '/tmp/_osx_support.%s'

 L.  67        48  LOAD_GLOBAL              os
               50  LOAD_METHOD              getpid
               52  CALL_METHOD_0         0  ''

 L.  66        54  BUILD_TUPLE_1         1 
               56  BINARY_MODULO    

 L.  67        58  LOAD_STR                 'w+b'

 L.  66        60  CALL_FUNCTION_2       2  ''
               62  STORE_FAST               'fp'
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            36  '36'
               68  END_FINALLY      
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            28  '28'

 L.  69        70  LOAD_FAST                'contextlib'
               72  LOAD_METHOD              closing
               74  LOAD_FAST                'fp'
               76  CALL_METHOD_1         1  ''
               78  SETUP_WITH          140  'to 140'
               80  STORE_FAST               'fp'

 L.  70        82  LOAD_STR                 "%s 2>/dev/null >'%s'"
               84  LOAD_FAST                'commandstring'
               86  LOAD_FAST                'fp'
               88  LOAD_ATTR                name
               90  BUILD_TUPLE_2         2 
               92  BINARY_MODULO    
               94  STORE_FAST               'cmd'

 L.  71        96  LOAD_GLOBAL              os
               98  LOAD_METHOD              system
              100  LOAD_FAST                'cmd'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_TRUE    124  'to 124'
              106  LOAD_FAST                'fp'
              108  LOAD_METHOD              read
              110  CALL_METHOD_0         0  ''
              112  LOAD_METHOD              decode
              114  LOAD_STR                 'utf-8'
              116  CALL_METHOD_1         1  ''
              118  LOAD_METHOD              strip
              120  CALL_METHOD_0         0  ''
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           104  '104'
              124  LOAD_CONST               None
            126_0  COME_FROM           122  '122'
              126  POP_BLOCK        
              128  ROT_TWO          
              130  BEGIN_FINALLY    
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  POP_FINALLY           0  ''
              138  RETURN_VALUE     
            140_0  COME_FROM_WITH       78  '78'
              140  WITH_CLEANUP_START
              142  WITH_CLEANUP_FINISH
              144  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 128


def _find_build_tool(toolname):
    """Find a build tool on current path or using xcrun"""
    return _find_executable(toolname) or _read_output('/usr/bin/xcrun -find %s' % (toolname,)) or ''


_SYSTEM_VERSION = None

def _get_system_version():
    """Return the OS X system version as a string"""
    global _SYSTEM_VERSION
    if _SYSTEM_VERSION is None:
        _SYSTEM_VERSION = ''
        try:
            f = open('/System/Library/CoreServices/SystemVersion.plist')
        except OSError:
            pass
        else:
            try:
                m = re.search('<key>ProductUserVisibleVersion</key>\\s*<string>(.*?)</string>', f.read)
            finally:
                f.close

            if m is not None:
                _SYSTEM_VERSION = '.'.join(m.group(1).split('.')[:2])
    return _SYSTEM_VERSION


def _remove_original_values(_config_vars):
    """Remove original unmodified values for testing"""
    for k in list(_config_vars):
        if k.startswith(_INITPRE):
            del _config_vars[k]


def _save_modified_value(_config_vars, cv, newvalue):
    """Save modified and original unmodified value of configuration var"""
    oldvalue = _config_vars.get(cv, '')
    if oldvalue != newvalue:
        if _INITPRE + cv not in _config_vars:
            _config_vars[_INITPRE + cv] = oldvalue
    _config_vars[cv] = newvalue


def _supports_universal_builds():
    """Returns True if universal builds are supported on this system"""
    osx_version = _get_system_version()
    if osx_version:
        try:
            osx_version = tuple((int(i) for i in osx_version.split('.')))
        except ValueError:
            osx_version = ''

    if osx_version:
        return bool(osx_version >= (10, 4))
    return False


def _find_appropriate_compiler(_config_vars):
    """Find appropriate C compiler for extension module builds"""
    if 'CC' in os.environ:
        return _config_vars
        cc = oldcc = _config_vars['CC'].split[0]
        cc = _find_executable(cc) or _find_build_tool('clang')
    else:
        if os.path.basename(cc).startswith('gcc'):
            data = _read_output("'%s' --version" % (
             cc.replace("'", '\'"\'"\''),))
            if data:
                if 'llvm-gcc' in data:
                    cc = _find_build_tool('clang')
        else:
            assert cc, 'Cannot locate working compiler'
        if cc != oldcc:
            for cv in _COMPILER_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    cv_split = _config_vars[cv].split
                    cv_split[0] = cc if cv != 'CXX' else cc + '++'
                    _save_modified_value(_config_vars, cv, ' '.join(cv_split))

        return _config_vars


def _remove_universal_flags(_config_vars):
    """Remove all universal build arguments from config vars"""
    for cv in _UNIVERSAL_CONFIG_VARS:
        if cv in _config_vars and cv not in os.environ:
            flags = _config_vars[cv]
            flags = re.sub('-arch\\s+\\w+\\s', ' ', flags, flags=(re.ASCII))
            flags = re.sub('-isysroot\\s*\\S+', ' ', flags)
            _save_modified_value(_config_vars, cv, flags)
        return _config_vars


def _remove_unsupported_archs(_config_vars):
    """Remove any unsupported archs from config vars"""
    if 'CC' in os.environ:
        return _config_vars
    if re.search('-arch\\s+ppc', _config_vars['CFLAGS']) is not None:
        status = os.system("echo 'int main{};' | '%s' -c -arch ppc -x c -o /dev/null /dev/null 2>/dev/null" % (
         _config_vars['CC'].replace("'", '\'"\'"\''),))
        if status:
            for cv in _UNIVERSAL_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    flags = _config_vars[cv]
                    flags = re.sub('-arch\\s+ppc\\w*\\s', ' ', flags)
                    _save_modified_value(_config_vars, cv, flags)

    return _config_vars


def _override_all_archs(_config_vars):
    """Allow override of all archs with ARCHFLAGS env var"""
    if 'ARCHFLAGS' in os.environ:
        arch = os.environ['ARCHFLAGS']
        for cv in _UNIVERSAL_CONFIG_VARS:
            if cv in _config_vars and '-arch' in _config_vars[cv]:
                flags = _config_vars[cv]
                flags = re.sub('-arch\\s+\\w+\\s', ' ', flags)
                flags = flags + ' ' + arch
                _save_modified_value(_config_vars, cv, flags)

    return _config_vars


def _check_for_unavailable_sdk(_config_vars):
    """Remove references to any SDKs not available"""
    cflags = _config_vars.get('CFLAGS', '')
    m = re.search('-isysroot\\s*(\\S+)', cflags)
    if m is not None:
        sdk = m.group(1)
        if not os.path.exists(sdk):
            for cv in _UNIVERSAL_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    flags = _config_vars[cv]
                    flags = re.sub('-isysroot\\s*\\S+(?:\\s|$)', ' ', flags)
                    _save_modified_value(_config_vars, cv, flags)

    return _config_vars


def compiler_fixup--- This code section failed: ---

 L. 313         0  LOAD_CONST               False
                2  DUP_TOP          
                4  STORE_FAST               'stripArch'
                6  STORE_FAST               'stripSysroot'

 L. 315         8  LOAD_GLOBAL              list
               10  LOAD_FAST                'compiler_so'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'compiler_so'

 L. 317        16  LOAD_GLOBAL              _supports_universal_builds
               18  CALL_FUNCTION_0       0  ''
               20  POP_JUMP_IF_TRUE     32  'to 32'

 L. 320        22  LOAD_CONST               True
               24  DUP_TOP          
               26  STORE_FAST               'stripArch'
               28  STORE_FAST               'stripSysroot'
               30  JUMP_FORWARD         58  'to 58'
             32_0  COME_FROM            20  '20'

 L. 322        32  LOAD_STR                 '-arch'
               34  LOAD_FAST                'cc_args'
               36  COMPARE_OP               in
               38  STORE_FAST               'stripArch'

 L. 323        40  LOAD_GLOBAL              any
               42  LOAD_GENEXPR             '<code_object <genexpr>>'
               44  LOAD_STR                 'compiler_fixup.<locals>.<genexpr>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  LOAD_FAST                'cc_args'
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'stripSysroot'
             58_0  COME_FROM            30  '30'

 L. 325        58  LOAD_FAST                'stripArch'
               60  POP_JUMP_IF_TRUE     72  'to 72'
               62  LOAD_STR                 'ARCHFLAGS'
               64  LOAD_GLOBAL              os
               66  LOAD_ATTR                environ
               68  COMPARE_OP               in
               70  POP_JUMP_IF_FALSE   128  'to 128'
             72_0  COME_FROM            60  '60'

 L. 327        72  SETUP_FINALLY       102  'to 102'

 L. 328        74  LOAD_FAST                'compiler_so'
               76  LOAD_METHOD              index
               78  LOAD_STR                 '-arch'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'index'

 L. 330        84  LOAD_FAST                'compiler_so'
               86  LOAD_FAST                'index'
               88  LOAD_FAST                'index'
               90  LOAD_CONST               2
               92  BINARY_ADD       
               94  BUILD_SLICE_2         2 
               96  DELETE_SUBSCR    
               98  POP_BLOCK        
              100  JUMP_BACK            72  'to 72'
            102_0  COME_FROM_FINALLY    72  '72'

 L. 331       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   124  'to 124'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 332       116  POP_EXCEPT       
              118  BREAK_LOOP          128  'to 128'
              120  POP_EXCEPT       
              122  JUMP_BACK            72  'to 72'
            124_0  COME_FROM           108  '108'
              124  END_FINALLY      
              126  JUMP_BACK            72  'to 72'
            128_0  COME_FROM_EXCEPT_CLAUSE   118  '118'
            128_1  COME_FROM_EXCEPT_CLAUSE    70  '70'

 L. 334       128  LOAD_STR                 'ARCHFLAGS'
              130  LOAD_GLOBAL              os
              132  LOAD_ATTR                environ
              134  COMPARE_OP               in
              136  POP_JUMP_IF_FALSE   160  'to 160'
              138  LOAD_FAST                'stripArch'
              140  POP_JUMP_IF_TRUE    160  'to 160'

 L. 337       142  LOAD_FAST                'compiler_so'
              144  LOAD_GLOBAL              os
              146  LOAD_ATTR                environ
              148  LOAD_STR                 'ARCHFLAGS'
              150  BINARY_SUBSCR    
              152  LOAD_METHOD              split
              154  CALL_METHOD_0         0  ''
              156  BINARY_ADD       
              158  STORE_FAST               'compiler_so'
            160_0  COME_FROM           140  '140'
            160_1  COME_FROM           136  '136'

 L. 339       160  LOAD_FAST                'stripSysroot'
              162  POP_JUMP_IF_FALSE   240  'to 240'

 L. 341       164  LOAD_LISTCOMP            '<code_object <listcomp>>'
              166  LOAD_STR                 'compiler_fixup.<locals>.<listcomp>'
              168  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              170  LOAD_GLOBAL              enumerate
              172  LOAD_FAST                'compiler_so'
              174  CALL_FUNCTION_1       1  ''
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'indices'

 L. 342       182  LOAD_FAST                'indices'
              184  POP_JUMP_IF_TRUE    188  'to 188'

 L. 343       186  BREAK_LOOP          240  'to 240'
            188_0  COME_FROM           184  '184'

 L. 344       188  LOAD_FAST                'indices'
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  STORE_FAST               'index'

 L. 345       196  LOAD_FAST                'compiler_so'
              198  LOAD_FAST                'index'
              200  BINARY_SUBSCR    
              202  LOAD_STR                 '-isysroot'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 347       208  LOAD_FAST                'compiler_so'
              210  LOAD_FAST                'index'
              212  LOAD_FAST                'index'
              214  LOAD_CONST               2
              216  BINARY_ADD       
              218  BUILD_SLICE_2         2 
              220  DELETE_SUBSCR    
              222  JUMP_BACK           164  'to 164'
            224_0  COME_FROM           206  '206'

 L. 350       224  LOAD_FAST                'compiler_so'
              226  LOAD_FAST                'index'
              228  LOAD_FAST                'index'
              230  LOAD_CONST               1
              232  BINARY_ADD       
              234  BUILD_SLICE_2         2 
              236  DELETE_SUBSCR    
              238  JUMP_BACK           164  'to 164'
            240_0  COME_FROM           162  '162'

 L. 355       240  LOAD_CONST               None
              242  STORE_FAST               'sysroot'

 L. 356       244  LOAD_FAST                'cc_args'
              246  STORE_FAST               'argvar'

 L. 357       248  LOAD_LISTCOMP            '<code_object <listcomp>>'
              250  LOAD_STR                 'compiler_fixup.<locals>.<listcomp>'
              252  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              254  LOAD_GLOBAL              enumerate
              256  LOAD_FAST                'cc_args'
              258  CALL_FUNCTION_1       1  ''
              260  GET_ITER         
              262  CALL_FUNCTION_1       1  ''
              264  STORE_FAST               'indices'

 L. 358       266  LOAD_FAST                'indices'
          268_270  POP_JUMP_IF_TRUE    294  'to 294'

 L. 359       272  LOAD_FAST                'compiler_so'
              274  STORE_FAST               'argvar'

 L. 360       276  LOAD_LISTCOMP            '<code_object <listcomp>>'
              278  LOAD_STR                 'compiler_fixup.<locals>.<listcomp>'
              280  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              282  LOAD_GLOBAL              enumerate
              284  LOAD_FAST                'compiler_so'
              286  CALL_FUNCTION_1       1  ''
              288  GET_ITER         
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'indices'
            294_0  COME_FROM           268  '268'

 L. 362       294  LOAD_FAST                'indices'
              296  GET_ITER         
              298  FOR_ITER            366  'to 366'
              300  STORE_FAST               'idx'

 L. 363       302  LOAD_FAST                'argvar'
              304  LOAD_FAST                'idx'
              306  BINARY_SUBSCR    
              308  LOAD_STR                 '-isysroot'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   336  'to 336'

 L. 364       316  LOAD_FAST                'argvar'
              318  LOAD_FAST                'idx'
              320  LOAD_CONST               1
              322  BINARY_ADD       
              324  BINARY_SUBSCR    
              326  STORE_FAST               'sysroot'

 L. 365       328  POP_TOP          
          330_332  BREAK_LOOP          366  'to 366'
              334  JUMP_BACK           298  'to 298'
            336_0  COME_FROM           312  '312'

 L. 367       336  LOAD_FAST                'argvar'
              338  LOAD_FAST                'idx'
              340  BINARY_SUBSCR    
              342  LOAD_GLOBAL              len
              344  LOAD_STR                 '-isysroot'
              346  CALL_FUNCTION_1       1  ''
              348  LOAD_CONST               None
              350  BUILD_SLICE_2         2 
              352  BINARY_SUBSCR    
              354  STORE_FAST               'sysroot'

 L. 368       356  POP_TOP          
          358_360  BREAK_LOOP          366  'to 366'
          362_364  JUMP_BACK           298  'to 298'

 L. 370       366  LOAD_FAST                'sysroot'
          368_370  POP_JUMP_IF_FALSE   420  'to 420'
              372  LOAD_GLOBAL              os
              374  LOAD_ATTR                path
              376  LOAD_METHOD              isdir
              378  LOAD_FAST                'sysroot'
              380  CALL_METHOD_1         1  ''
          382_384  POP_JUMP_IF_TRUE    420  'to 420'

 L. 371       386  LOAD_CONST               0
              388  LOAD_CONST               ('log',)
              390  IMPORT_NAME              distutils
              392  IMPORT_FROM              log
              394  STORE_FAST               'log'
              396  POP_TOP          

 L. 372       398  LOAD_FAST                'log'
              400  LOAD_METHOD              warn
              402  LOAD_STR                 "Compiling with an SDK that doesn't seem to exist: %s"

 L. 373       404  LOAD_FAST                'sysroot'

 L. 372       406  CALL_METHOD_2         2  ''
              408  POP_TOP          

 L. 374       410  LOAD_FAST                'log'
              412  LOAD_METHOD              warn
              414  LOAD_STR                 'Please check your Xcode installation'
              416  CALL_METHOD_1         1  ''
              418  POP_TOP          
            420_0  COME_FROM           382  '382'
            420_1  COME_FROM           368  '368'

 L. 376       420  LOAD_FAST                'compiler_so'
              422  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 128_1


def customize_config_vars(_config_vars):
    """Customize Python build configuration variables.

    Called internally from sysconfig with a mutable mapping
    containing name/value pairs parsed from the configured
    makefile used to build this interpreter.  Returns
    the mapping updated as needed to reflect the environment
    in which the interpreter is running; in the case of
    a Python from a binary installer, the installed
    environment may be very different from the build
    environment, i.e. different OS levels, different
    built tools, different available CPU architectures.

    This customization is performed whenever
    distutils.sysconfig.get_config_vars() is first
    called.  It may be used in environments where no
    compilers are present, i.e. when installing pure
    Python dists.  Customization of compiler paths
    and detection of unavailable archs is deferred
    until the first extension module build is
    requested (in distutils.sysconfig.customize_compiler).

    Currently called from distutils.sysconfig
    """
    if not _supports_universal_builds():
        _remove_universal_flags(_config_vars)
    _override_all_archs(_config_vars)
    _check_for_unavailable_sdk(_config_vars)
    return _config_vars


def customize_compiler(_config_vars):
    """Customize compiler path and configuration variables.

    This customization is performed when the first
    extension module build is requested
    in distutils.sysconfig.customize_compiler).
    """
    _find_appropriate_compiler(_config_vars)
    _remove_unsupported_archs(_config_vars)
    _override_all_archs(_config_vars)
    return _config_vars


def get_platform_osx(_config_vars, osname, release, machine):
    """Filter values for get_platform()"""
    macver = _config_vars.get('MACOSX_DEPLOYMENT_TARGET', '')
    macrelease = _get_system_version() or macver
    macver = macver or macrelease
    if macver:
        release = macver
        osname = 'macosx'
        cflags = _config_vars.get(_INITPRE + 'CFLAGS', _config_vars.get('CFLAGS', ''))
        if macrelease:
            try:
                macrelease = tuple((int(i) for i in macrelease.split('.')[0:2]))
            except ValueError:
                macrelease = (10, 0)

        else:
            macrelease = (10, 0)
        if macrelease >= (10, 4) and '-arch' in cflags.strip:
            machine = 'fat'
            archs = re.findall('-arch\\s+(\\S+)', cflags)
            archs = tuple(sorted(set(archs)))
            if len(archs) == 1:
                machine = archs[0]
        elif archs == ('i386', 'ppc'):
            machine = 'fat'
        else:
            if archs == ('i386', 'x86_64'):
                machine = 'intel'
            else:
                if archs == ('i386', 'ppc', 'x86_64'):
                    machine = 'fat3'
                else:
                    if archs == ('ppc64', 'x86_64'):
                        machine = 'fat64'
                    else:
                        if archs == ('i386', 'ppc', 'ppc64', 'x86_64'):
                            machine = 'universal'
                        else:
                            raise ValueError("Don't know machine value for archs=%r" % (archs,))
    else:
        if machine == 'i386':
            if sys.maxsize >= 4294967296:
                machine = 'x86_64'
        elif machine in ('PowerPC', 'Power_Macintosh'):
            if sys.maxsize >= 4294967296:
                machine = 'ppc64'
            else:
                machine = 'ppc'
        return (
         osname, release, machine)