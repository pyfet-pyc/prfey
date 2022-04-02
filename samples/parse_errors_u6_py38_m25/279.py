# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
            flags = re.sub('-isysroot [^ \t]*', ' ', flags)
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
    m = re.search('-isysroot\\s+(\\S+)', cflags)
    if m is not None:
        sdk = m.group(1)
        if not os.path.exists(sdk):
            for cv in _UNIVERSAL_CONFIG_VARS:
                if cv in _config_vars and cv not in os.environ:
                    flags = _config_vars[cv]
                    flags = re.sub('-isysroot\\s+\\S+(?:\\s|$)', ' ', flags)
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
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            20  '20'

 L. 322        32  LOAD_STR                 '-arch'
               34  LOAD_FAST                'cc_args'
               36  COMPARE_OP               in
               38  STORE_FAST               'stripArch'

 L. 323        40  LOAD_STR                 '-isysroot'
               42  LOAD_FAST                'cc_args'
               44  COMPARE_OP               in
               46  STORE_FAST               'stripSysroot'
             48_0  COME_FROM            30  '30'

 L. 325        48  LOAD_FAST                'stripArch'
               50  POP_JUMP_IF_TRUE     62  'to 62'
               52  LOAD_STR                 'ARCHFLAGS'
               54  LOAD_GLOBAL              os
               56  LOAD_ATTR                environ
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE   118  'to 118'
             62_0  COME_FROM            50  '50'

 L. 327        62  SETUP_FINALLY        92  'to 92'

 L. 328        64  LOAD_FAST                'compiler_so'
               66  LOAD_METHOD              index
               68  LOAD_STR                 '-arch'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'index'

 L. 330        74  LOAD_FAST                'compiler_so'
               76  LOAD_FAST                'index'
               78  LOAD_FAST                'index'
               80  LOAD_CONST               2
               82  BINARY_ADD       
               84  BUILD_SLICE_2         2 
               86  DELETE_SUBSCR    
               88  POP_BLOCK        
               90  JUMP_BACK            62  'to 62'
             92_0  COME_FROM_FINALLY    62  '62'

 L. 331        92  DUP_TOP          
               94  LOAD_GLOBAL              ValueError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   114  'to 114'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 332       106  POP_EXCEPT       
              108  BREAK_LOOP          118  'to 118'
              110  POP_EXCEPT       
              112  JUMP_BACK            62  'to 62'
            114_0  COME_FROM            98  '98'
              114  END_FINALLY      
              116  JUMP_BACK            62  'to 62'
            118_0  COME_FROM_EXCEPT_CLAUSE   108  '108'
            118_1  COME_FROM_EXCEPT_CLAUSE    60  '60'

 L. 334       118  LOAD_STR                 'ARCHFLAGS'
              120  LOAD_GLOBAL              os
              122  LOAD_ATTR                environ
              124  COMPARE_OP               in
              126  POP_JUMP_IF_FALSE   150  'to 150'
              128  LOAD_FAST                'stripArch'
              130  POP_JUMP_IF_TRUE    150  'to 150'

 L. 337       132  LOAD_FAST                'compiler_so'
              134  LOAD_GLOBAL              os
              136  LOAD_ATTR                environ
              138  LOAD_STR                 'ARCHFLAGS'
              140  BINARY_SUBSCR    
              142  LOAD_METHOD              split
              144  CALL_METHOD_0         0  ''
              146  BINARY_ADD       
              148  STORE_FAST               'compiler_so'
            150_0  COME_FROM           130  '130'
            150_1  COME_FROM           126  '126'

 L. 339       150  LOAD_FAST                'stripSysroot'
              152  POP_JUMP_IF_FALSE   210  'to 210'

 L. 341       154  SETUP_FINALLY       184  'to 184'

 L. 342       156  LOAD_FAST                'compiler_so'
              158  LOAD_METHOD              index
              160  LOAD_STR                 '-isysroot'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'index'

 L. 344       166  LOAD_FAST                'compiler_so'
              168  LOAD_FAST                'index'
              170  LOAD_FAST                'index'
              172  LOAD_CONST               2
              174  BINARY_ADD       
              176  BUILD_SLICE_2         2 
              178  DELETE_SUBSCR    
              180  POP_BLOCK        
              182  JUMP_BACK           154  'to 154'
            184_0  COME_FROM_FINALLY   154  '154'

 L. 345       184  DUP_TOP          
              186  LOAD_GLOBAL              ValueError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   206  'to 206'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 346       198  POP_EXCEPT       
              200  BREAK_LOOP          210  'to 210'
              202  POP_EXCEPT       
              204  JUMP_BACK           154  'to 154'
            206_0  COME_FROM           190  '190'
              206  END_FINALLY      
              208  JUMP_BACK           154  'to 154'
            210_0  COME_FROM_EXCEPT_CLAUSE   200  '200'
            210_1  COME_FROM_EXCEPT_CLAUSE   152  '152'

 L. 351       210  LOAD_CONST               None
              212  STORE_FAST               'sysroot'

 L. 352       214  LOAD_STR                 '-isysroot'
              216  LOAD_FAST                'cc_args'
              218  COMPARE_OP               in
              220  POP_JUMP_IF_FALSE   246  'to 246'

 L. 353       222  LOAD_FAST                'cc_args'
              224  LOAD_METHOD              index
              226  LOAD_STR                 '-isysroot'
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'idx'

 L. 354       232  LOAD_FAST                'cc_args'
              234  LOAD_FAST                'idx'
              236  LOAD_CONST               1
              238  BINARY_ADD       
              240  BINARY_SUBSCR    
              242  STORE_FAST               'sysroot'
              244  JUMP_FORWARD        278  'to 278'
            246_0  COME_FROM           220  '220'

 L. 355       246  LOAD_STR                 '-isysroot'
              248  LOAD_FAST                'compiler_so'
              250  COMPARE_OP               in
          252_254  POP_JUMP_IF_FALSE   278  'to 278'

 L. 356       256  LOAD_FAST                'compiler_so'
              258  LOAD_METHOD              index
              260  LOAD_STR                 '-isysroot'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'idx'

 L. 357       266  LOAD_FAST                'compiler_so'
              268  LOAD_FAST                'idx'
              270  LOAD_CONST               1
              272  BINARY_ADD       
              274  BINARY_SUBSCR    
              276  STORE_FAST               'sysroot'
            278_0  COME_FROM           252  '252'
            278_1  COME_FROM           244  '244'

 L. 359       278  LOAD_FAST                'sysroot'
          280_282  POP_JUMP_IF_FALSE   332  'to 332'
              284  LOAD_GLOBAL              os
              286  LOAD_ATTR                path
              288  LOAD_METHOD              isdir
              290  LOAD_FAST                'sysroot'
              292  CALL_METHOD_1         1  ''
          294_296  POP_JUMP_IF_TRUE    332  'to 332'

 L. 360       298  LOAD_CONST               0
              300  LOAD_CONST               ('log',)
              302  IMPORT_NAME              distutils
              304  IMPORT_FROM              log
              306  STORE_FAST               'log'
              308  POP_TOP          

 L. 361       310  LOAD_FAST                'log'
              312  LOAD_METHOD              warn
              314  LOAD_STR                 "Compiling with an SDK that doesn't seem to exist: %s"

 L. 362       316  LOAD_FAST                'sysroot'

 L. 361       318  CALL_METHOD_2         2  ''
              320  POP_TOP          

 L. 363       322  LOAD_FAST                'log'
              324  LOAD_METHOD              warn
              326  LOAD_STR                 'Please check your Xcode installation'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
            332_0  COME_FROM           294  '294'
            332_1  COME_FROM           280  '280'

 L. 365       332  LOAD_FAST                'compiler_so'
              334  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 118_1


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