# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\msvc9compiler.py
"""distutils.msvc9compiler

Contains MSVCCompiler, an implementation of the abstract CCompiler class
for the Microsoft Visual Studio 2008.

The module is compatible with VS 2005 and VS 2008. You can find legacy support
for older versions of VS in distutils.msvccompiler.
"""
import os, subprocess, sys, re
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
from distutils.util import get_platform
import winreg
RegOpenKeyEx = winreg.OpenKeyEx
RegEnumKey = winreg.EnumKey
RegEnumValue = winreg.EnumValue
RegError = winreg.error
HKEYS = (
 winreg.HKEY_USERS,
 winreg.HKEY_CURRENT_USER,
 winreg.HKEY_LOCAL_MACHINE,
 winreg.HKEY_CLASSES_ROOT)
NATIVE_WIN64 = sys.platform == 'win32' and sys.maxsize > 4294967296
if NATIVE_WIN64:
    VS_BASE = 'Software\\Wow6432Node\\Microsoft\\VisualStudio\\%0.1f'
    WINSDK_BASE = 'Software\\Wow6432Node\\Microsoft\\Microsoft SDKs\\Windows'
    NET_BASE = 'Software\\Wow6432Node\\Microsoft\\.NETFramework'
else:
    VS_BASE = 'Software\\Microsoft\\VisualStudio\\%0.1f'
    WINSDK_BASE = 'Software\\Microsoft\\Microsoft SDKs\\Windows'
    NET_BASE = 'Software\\Microsoft\\.NETFramework'
PLAT_TO_VCVARS = {'win32':'x86', 
 'win-amd64':'amd64'}

class Reg:
    __doc__ = 'Helper class to read values from the registry\n    '

    def get_value(cls, path, key):
        for base in HKEYS:
            d = cls.read_values(base, path)
            if d and key in d:
                return d[key]
        else:
            raise KeyError(key)

    get_value = classmethod(get_value)

    def read_keys(cls, base, key):
        """Return list of registry keys."""
        try:
            handle = RegOpenKeyEx(base, key)
        except RegError:
            return
        else:
            L = []
            i = 0
            while True:
                try:
                    k = RegEnumKey(handle, i)
                except RegError:
                    break
                else:
                    L.append(k)
                    i += 1

            return L

    read_keys = classmethod(read_keys)

    def read_values(cls, base, key):
        """Return dict of registry keys and values.

        All names are converted to lowercase.
        """
        try:
            handle = RegOpenKeyEx(base, key)
        except RegError:
            return
        else:
            d = {}
            i = 0
            while True:
                try:
                    name, value, type = RegEnumValue(handle, i)
                except RegError:
                    break
                else:
                    name = name.lower()
                    d[cls.convert_mbcs(name)] = cls.convert_mbcs(value)
                    i += 1

            return d

    read_values = classmethod(read_values)

    def convert_mbcs(s):
        dec = getattr(s, 'decode', None)
        if dec is not None:
            try:
                s = dec('mbcs')
            except UnicodeError:
                pass

        return s

    convert_mbcs = staticmethod(convert_mbcs)


class MacroExpander:

    def __init__(self, version):
        self.macros = {}
        self.vsbase = VS_BASE % version
        self.load_macros(version)

    def set_macro(self, macro, path, key):
        self.macros['$(%s)' % macro] = Reg.get_value(path, key)

    def load_macros--- This code section failed: ---

 L. 133         0  LOAD_FAST                'self'
                2  LOAD_METHOD              set_macro
                4  LOAD_STR                 'VCInstallDir'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                vsbase
               10  LOAD_STR                 '\\Setup\\VC'
               12  BINARY_ADD       
               14  LOAD_STR                 'productdir'
               16  CALL_METHOD_3         3  ''
               18  POP_TOP          

 L. 134        20  LOAD_FAST                'self'
               22  LOAD_METHOD              set_macro
               24  LOAD_STR                 'VSInstallDir'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                vsbase
               30  LOAD_STR                 '\\Setup\\VS'
               32  BINARY_ADD       
               34  LOAD_STR                 'productdir'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          

 L. 135        40  LOAD_FAST                'self'
               42  LOAD_METHOD              set_macro
               44  LOAD_STR                 'FrameworkDir'
               46  LOAD_GLOBAL              NET_BASE
               48  LOAD_STR                 'installroot'
               50  CALL_METHOD_3         3  ''
               52  POP_TOP          

 L. 136        54  SETUP_FINALLY        92  'to 92'

 L. 137        56  LOAD_FAST                'version'
               58  LOAD_CONST               8.0
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    80  'to 80'

 L. 138        64  LOAD_FAST                'self'
               66  LOAD_METHOD              set_macro
               68  LOAD_STR                 'FrameworkSDKDir'
               70  LOAD_GLOBAL              NET_BASE

 L. 139        72  LOAD_STR                 'sdkinstallrootv2.0'

 L. 138        74  CALL_METHOD_3         3  ''
               76  POP_TOP          
               78  JUMP_FORWARD         88  'to 88'
             80_0  COME_FROM            62  '62'

 L. 141        80  LOAD_GLOBAL              KeyError
               82  LOAD_STR                 'sdkinstallrootv2.0'
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'
               88  POP_BLOCK        
               90  JUMP_FORWARD        120  'to 120'
             92_0  COME_FROM_FINALLY    54  '54'

 L. 142        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   118  'to 118'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 143       106  LOAD_GLOBAL              DistutilsPlatformError

 L. 144       108  LOAD_STR                 'Python was built with Visual Studio 2008;\nextensions must be built with a compiler than can generate compatible binaries.\nVisual Studio 2008 was not found on this system. If you have Cygwin installed,\nyou can try compiling with MingW32, by passing "-c mingw32" to setup.py.'

 L. 143       110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            98  '98'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            90  '90'

 L. 149       120  LOAD_FAST                'version'
              122  LOAD_CONST               9.0
              124  COMPARE_OP               >=
              126  POP_JUMP_IF_FALSE   160  'to 160'

 L. 150       128  LOAD_FAST                'self'
              130  LOAD_METHOD              set_macro
              132  LOAD_STR                 'FrameworkVersion'
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                vsbase
              138  LOAD_STR                 'clr version'
              140  CALL_METHOD_3         3  ''
              142  POP_TOP          

 L. 151       144  LOAD_FAST                'self'
              146  LOAD_METHOD              set_macro
              148  LOAD_STR                 'WindowsSdkDir'
              150  LOAD_GLOBAL              WINSDK_BASE
              152  LOAD_STR                 'currentinstallfolder'
              154  CALL_METHOD_3         3  ''
              156  POP_TOP          
              158  JUMP_FORWARD        258  'to 258'
            160_0  COME_FROM           126  '126'

 L. 153       160  LOAD_STR                 'Software\\Microsoft\\NET Framework Setup\\Product'
              162  STORE_FAST               'p'

 L. 154       164  LOAD_GLOBAL              HKEYS
              166  GET_ITER         
              168  FOR_ITER            258  'to 258'
              170  STORE_FAST               'base'

 L. 155       172  SETUP_FINALLY       188  'to 188'

 L. 156       174  LOAD_GLOBAL              RegOpenKeyEx
              176  LOAD_FAST                'base'
              178  LOAD_FAST                'p'
              180  CALL_FUNCTION_2       2  ''
              182  STORE_FAST               'h'
              184  POP_BLOCK        
              186  JUMP_FORWARD        212  'to 212'
            188_0  COME_FROM_FINALLY   172  '172'

 L. 157       188  DUP_TOP          
              190  LOAD_GLOBAL              RegError
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   210  'to 210'
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 158       202  POP_EXCEPT       
              204  JUMP_BACK           168  'to 168'
              206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
            210_0  COME_FROM           194  '194'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           186  '186'

 L. 159       212  LOAD_GLOBAL              RegEnumKey
              214  LOAD_FAST                'h'
              216  LOAD_CONST               0
              218  CALL_FUNCTION_2       2  ''
              220  STORE_FAST               'key'

 L. 160       222  LOAD_GLOBAL              Reg
              224  LOAD_METHOD              get_value
              226  LOAD_FAST                'base'
              228  LOAD_STR                 '%s\\%s'
              230  LOAD_FAST                'p'
              232  LOAD_FAST                'key'
              234  BUILD_TUPLE_2         2 
              236  BINARY_MODULO    
              238  CALL_METHOD_2         2  ''
              240  STORE_FAST               'd'

 L. 161       242  LOAD_FAST                'd'
              244  LOAD_STR                 'version'
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                macros
              252  LOAD_STR                 '$(FrameworkVersion)'
              254  STORE_SUBSCR     
              256  JUMP_BACK           168  'to 168'
            258_0  COME_FROM           158  '158'

Parse error at or near `POP_EXCEPT' instruction at offset 206

    def sub(self, s):
        for k, v in self.macros.items():
            s = s.replace(k, v)
        else:
            return s


def get_build_version():
    """Return the version of MSVC that was used to build Python.

    For Python 2.3 and up, the version number is included in
    sys.version.  For earlier versions, assume the compiler is MSVC 6.
    """
    prefix = 'MSC v.'
    i = sys.version.find(prefix)
    if i == -1:
        return 6
    i = i + len(prefix)
    s, rest = sys.version[i:].split(' ', 1)
    majorVersion = int(s[:-2]) - 6
    if majorVersion >= 13:
        majorVersion += 1
    minorVersion = int(s[2:3]) / 10.0
    if majorVersion == 6:
        minorVersion = 0
    if majorVersion >= 6:
        return majorVersion + minorVersion


def normalize_and_reduce_paths(paths):
    """Return a list of normalized paths with duplicates removed.

    The current order of paths is maintained.
    """
    reduced_paths = []
    for p in paths:
        np = os.path.normpath(p)
        if np not in reduced_paths:
            reduced_paths.append(np)
        return reduced_paths


def removeDuplicates(variable):
    """Remove duplicate values of an environment variable.
    """
    oldList = variable.split(os.pathsep)
    newList = []
    for i in oldList:
        if i not in newList:
            newList.append(i)
        newVariable = os.pathsep.join(newList)
        return newVariable


def find_vcvarsall(version):
    """Find the vcvarsall.bat file

    At first it tries to find the productdir of VS 2008 in the registry. If
    that fails it falls back to the VS90COMNTOOLS env var.
    """
    vsbase = VS_BASE % version
    try:
        productdir = Reg.get_value('%s\\Setup\\VC' % vsbase, 'productdir')
    except KeyError:
        log.debug('Unable to find productdir in registry')
        productdir = None
    else:
        if not (productdir and os.path.isdir(productdir)):
            toolskey = 'VS%0.f0COMNTOOLS' % version
            toolsdir = os.environ.get(toolskey, None)
            if toolsdir and os.path.isdir(toolsdir):
                productdir = os.path.join(toolsdir, os.pardir, os.pardir, 'VC')
                productdir = os.path.abspath(productdir)
                if not os.path.isdir(productdir):
                    log.debug('%s is not a valid directory' % productdir)
                    return None
                else:
                    log.debug('Env var %s is not set or invalid' % toolskey)
            else:
                productdir or log.debug('No productdir found')
                return None
            vcvarsall = os.path.join(productdir, 'vcvarsall.bat')
            if os.path.isfile(vcvarsall):
                return vcvarsall
            log.debug('Unable to find vcvarsall.bat')


def query_vcvarsall(version, arch='x86'):
    """Launch vcvarsall.bat and read the settings from its environment
    """
    vcvarsall = find_vcvarsall(version)
    interesting = {'include', 'lib', 'libpath', 'path'}
    result = {}
    if vcvarsall is None:
        raise DistutilsPlatformError('Unable to find vcvarsall.bat')
    log.debug"Calling 'vcvarsall.bat %s' (version=%s)"archversion
    popen = subprocess.Popen(('"%s" %s & set' % (vcvarsall, arch)), stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    try:
        stdout, stderr = popen.communicate()
        if popen.wait() != 0:
            raise DistutilsPlatformError(stderr.decode('mbcs'))
        stdout = stdout.decode('mbcs')
        for line in stdout.split('\n'):
            line = Reg.convert_mbcs(line)
            if '=' not in line:
                pass
            else:
                line = line.strip()
                key, value = line.split('=', 1)
                key = key.lower()
                if key in interesting:
                    if value.endswith(os.pathsep):
                        value = value[:-1]
                    result[key] = removeDuplicates(value)

    finally:
        popen.stdout.close()
        popen.stderr.close()

    if len(result) != len(interesting):
        raise ValueError(str(list(result.keys())))
    return result


VERSION = get_build_version()
if VERSION < 8.0:
    raise DistutilsPlatformError('VC %0.1f is not supported by this module' % VERSION)

class MSVCCompiler(CCompiler):
    __doc__ = 'Concrete class that implements an interface to Microsoft Visual C++,\n       as defined by the CCompiler abstract class.'
    compiler_type = 'msvc'
    executables = {}
    _c_extensions = [
     '.c']
    _cpp_extensions = ['.cc', '.cpp', '.cxx']
    _rc_extensions = ['.rc']
    _mc_extensions = ['.mc']
    src_extensions = _c_extensions + _cpp_extensions + _rc_extensions + _mc_extensions
    res_extension = '.res'
    obj_extension = '.obj'
    static_lib_extension = '.lib'
    shared_lib_extension = '.dll'
    static_lib_format = shared_lib_format = '%s%s'
    exe_extension = '.exe'

    def __init__(self, verbose=0, dry_run=0, force=0):
        CCompiler.__init__(self, verbose, dry_run, force)
        self._MSVCCompiler__version = VERSION
        self._MSVCCompiler__root = 'Software\\Microsoft\\VisualStudio'
        self._MSVCCompiler__paths = []
        self.plat_name = None
        self._MSVCCompiler__arch = None
        self.initialized = False

    def initialize(self, plat_name=None):
        if self.initialized:
            raise AssertionError("don't init multiple times")
        else:
            if plat_name is None:
                plat_name = get_platform()
            ok_plats = ('win32', 'win-amd64')
            if plat_name not in ok_plats:
                raise DistutilsPlatformError('--plat-name must be one of %s' % (
                 ok_plats,))
            if 'DISTUTILS_USE_SDK' in os.environ and 'MSSdk' in os.environ and self.find_exe('cl.exe'):
                self.cc = 'cl.exe'
                self.linker = 'link.exe'
                self.lib = 'lib.exe'
                self.rc = 'rc.exe'
                self.mc = 'mc.exe'
            else:
                if plat_name == get_platform() or plat_name == 'win32':
                    plat_spec = PLAT_TO_VCVARS[plat_name]
                else:
                    plat_spec = PLAT_TO_VCVARS[get_platform()] + '_' + PLAT_TO_VCVARS[plat_name]
                vc_env = query_vcvarsall(VERSION, plat_spec)
                self._MSVCCompiler__paths = vc_env['path'].split(os.pathsep)
                os.environ['lib'] = vc_env['lib']
                os.environ['include'] = vc_env['include']
                if len(self._MSVCCompiler__paths) == 0:
                    raise DistutilsPlatformError("Python was built with %s, and extensions need to be built with the same version of the compiler, but it isn't installed." % self._MSVCCompiler__product)
            self.cc = self.find_exe('cl.exe')
            self.linker = self.find_exe('link.exe')
            self.lib = self.find_exe('lib.exe')
            self.rc = self.find_exe('rc.exe')
            self.mc = self.find_exe('mc.exe')
        try:
            for p in os.environ['path'].split(';'):
                self._MSVCCompiler__paths.append(p)

        except KeyError:
            pass
        else:
            self._MSVCCompiler__paths = normalize_and_reduce_paths(self._MSVCCompiler__paths)
            os.environ['path'] = ';'.join(self._MSVCCompiler__paths)
            self.preprocess_options = None
            if self._MSVCCompiler__arch == 'x86':
                self.compile_options = [
                 '/nologo', '/Ox', '/MD', '/W3',
                 '/DNDEBUG']
                self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3',
                 '/Z7', '/D_DEBUG']
            else:
                self.compile_options = [
                 '/nologo', '/Ox', '/MD', '/W3', '/GS-',
                 '/DNDEBUG']
                self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3', '/GS-',
                 '/Z7', '/D_DEBUG']
            self.ldflags_shared = ['/DLL', '/nologo', '/INCREMENTAL:NO']
            if self._MSVCCompiler__version >= 7:
                self.ldflags_shared_debug = ['/DLL', '/nologo', '/INCREMENTAL:no', '/DEBUG']
            self.ldflags_static = ['/nologo']
            self.initialized = True

    def object_filenames(self, source_filenames, strip_dir=0, output_dir=''):
        if output_dir is None:
            output_dir = ''
        obj_names = []
        for src_name in source_filenames:
            base, ext = os.path.splitext(src_name)
            base = os.path.splitdrive(base)[1]
            base = base[os.path.isabs(base):]
            if ext not in self.src_extensions:
                raise CompileError("Don't know how to compile %s" % src_name)
            if strip_dir:
                base = os.path.basename(base)
            if ext in self._rc_extensions:
                obj_names.append(os.path.join(output_dir, base + self.res_extension))
            elif ext in self._mc_extensions:
                obj_names.append(os.path.join(output_dir, base + self.res_extension))
            else:
                obj_names.append(os.path.join(output_dir, base + self.obj_extension))
        else:
            return obj_names

    def compile--- This code section failed: ---

 L. 460         0  LOAD_FAST                'self'
                2  LOAD_ATTR                initialized
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 461         6  LOAD_FAST                'self'
                8  LOAD_METHOD              initialize
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          
             14_0  COME_FROM             4  '4'

 L. 462        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _setup_compile
               18  LOAD_FAST                'output_dir'
               20  LOAD_FAST                'macros'
               22  LOAD_FAST                'include_dirs'

 L. 463        24  LOAD_FAST                'sources'

 L. 463        26  LOAD_FAST                'depends'

 L. 463        28  LOAD_FAST                'extra_postargs'

 L. 462        30  CALL_METHOD_6         6  ''
               32  STORE_FAST               'compile_info'

 L. 464        34  LOAD_FAST                'compile_info'
               36  UNPACK_SEQUENCE_5     5 
               38  STORE_FAST               'macros'
               40  STORE_FAST               'objects'
               42  STORE_FAST               'extra_postargs'
               44  STORE_FAST               'pp_opts'
               46  STORE_FAST               'build'

 L. 466        48  LOAD_FAST                'extra_preargs'
               50  JUMP_IF_TRUE_OR_POP    54  'to 54'
               52  BUILD_LIST_0          0 
             54_0  COME_FROM            50  '50'
               54  STORE_FAST               'compile_opts'

 L. 467        56  LOAD_FAST                'compile_opts'
               58  LOAD_METHOD              append
               60  LOAD_STR                 '/c'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 468        66  LOAD_FAST                'debug'
               68  POP_JUMP_IF_FALSE    84  'to 84'

 L. 469        70  LOAD_FAST                'compile_opts'
               72  LOAD_METHOD              extend
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                compile_options_debug
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM            68  '68'

 L. 471        84  LOAD_FAST                'compile_opts'
               86  LOAD_METHOD              extend
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                compile_options
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            82  '82'

 L. 473        96  LOAD_FAST                'objects'
               98  GET_ITER         
          100_102  FOR_ITER            620  'to 620'
              104  STORE_FAST               'obj'

 L. 474       106  SETUP_FINALLY       124  'to 124'

 L. 475       108  LOAD_FAST                'build'
              110  LOAD_FAST                'obj'
              112  BINARY_SUBSCR    
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'src'
              118  STORE_FAST               'ext'
              120  POP_BLOCK        
              122  JUMP_FORWARD        148  'to 148'
            124_0  COME_FROM_FINALLY   106  '106'

 L. 476       124  DUP_TOP          
              126  LOAD_GLOBAL              KeyError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 477       138  POP_EXCEPT       
              140  JUMP_BACK           100  'to 100'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           130  '130'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           122  '122'

 L. 478       148  LOAD_FAST                'debug'
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 482       152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              abspath
              158  LOAD_FAST                'src'
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'src'
            164_0  COME_FROM           150  '150'

 L. 484       164  LOAD_FAST                'ext'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _c_extensions
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   186  'to 186'

 L. 485       174  LOAD_STR                 '/Tc'
              176  LOAD_FAST                'src'
              178  BINARY_ADD       
              180  STORE_FAST               'input_opt'
          182_184  JUMP_FORWARD        526  'to 526'
            186_0  COME_FROM           172  '172'

 L. 486       186  LOAD_FAST                'ext'
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                _cpp_extensions
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L. 487       196  LOAD_STR                 '/Tp'
              198  LOAD_FAST                'src'
              200  BINARY_ADD       
              202  STORE_FAST               'input_opt'
          204_206  JUMP_FORWARD        526  'to 526'
            208_0  COME_FROM           194  '194'

 L. 488       208  LOAD_FAST                'ext'
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                _rc_extensions
              214  COMPARE_OP               in
          216_218  POP_JUMP_IF_FALSE   316  'to 316'

 L. 490       220  LOAD_FAST                'src'
              222  STORE_FAST               'input_opt'

 L. 491       224  LOAD_STR                 '/fo'
              226  LOAD_FAST                'obj'
              228  BINARY_ADD       
              230  STORE_FAST               'output_opt'

 L. 492       232  SETUP_FINALLY       268  'to 268'

 L. 493       234  LOAD_FAST                'self'
              236  LOAD_METHOD              spawn
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                rc
              242  BUILD_LIST_1          1 
              244  LOAD_FAST                'pp_opts'
              246  BINARY_ADD       

 L. 494       248  LOAD_FAST                'output_opt'
              250  BUILD_LIST_1          1 

 L. 493       252  BINARY_ADD       

 L. 494       254  LOAD_FAST                'input_opt'
              256  BUILD_LIST_1          1 

 L. 493       258  BINARY_ADD       
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
              264  POP_BLOCK        
              266  JUMP_BACK           100  'to 100'
            268_0  COME_FROM_FINALLY   232  '232'

 L. 495       268  DUP_TOP          
              270  LOAD_GLOBAL              DistutilsExecError
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   310  'to 310'
              278  POP_TOP          
              280  STORE_FAST               'msg'
              282  POP_TOP          
              284  SETUP_FINALLY       298  'to 298'

 L. 496       286  LOAD_GLOBAL              CompileError
              288  LOAD_FAST                'msg'
              290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'
              294  POP_BLOCK        
              296  BEGIN_FINALLY    
            298_0  COME_FROM_FINALLY   284  '284'
              298  LOAD_CONST               None
              300  STORE_FAST               'msg'
              302  DELETE_FAST              'msg'
              304  END_FINALLY      
              306  POP_EXCEPT       
              308  JUMP_BACK           100  'to 100'
            310_0  COME_FROM           274  '274'
              310  END_FINALLY      

 L. 497       312  JUMP_BACK           100  'to 100'
              314  JUMP_FORWARD        526  'to 526'
            316_0  COME_FROM           216  '216'

 L. 498       316  LOAD_FAST                'ext'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _mc_extensions
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   510  'to 510'

 L. 510       328  LOAD_GLOBAL              os
              330  LOAD_ATTR                path
              332  LOAD_METHOD              dirname
              334  LOAD_FAST                'src'
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'h_dir'

 L. 511       340  LOAD_GLOBAL              os
              342  LOAD_ATTR                path
              344  LOAD_METHOD              dirname
              346  LOAD_FAST                'obj'
              348  CALL_METHOD_1         1  ''
              350  STORE_FAST               'rc_dir'

 L. 512       352  SETUP_FINALLY       462  'to 462'

 L. 514       354  LOAD_FAST                'self'
              356  LOAD_METHOD              spawn
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                mc
              362  BUILD_LIST_1          1 

 L. 515       364  LOAD_STR                 '-h'
              366  LOAD_FAST                'h_dir'
              368  LOAD_STR                 '-r'
              370  LOAD_FAST                'rc_dir'
              372  BUILD_LIST_4          4 

 L. 514       374  BINARY_ADD       

 L. 515       376  LOAD_FAST                'src'
              378  BUILD_LIST_1          1 

 L. 514       380  BINARY_ADD       
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          

 L. 516       386  LOAD_GLOBAL              os
              388  LOAD_ATTR                path
              390  LOAD_METHOD              splitext
              392  LOAD_GLOBAL              os
              394  LOAD_ATTR                path
              396  LOAD_METHOD              basename
              398  LOAD_FAST                'src'
              400  CALL_METHOD_1         1  ''
              402  CALL_METHOD_1         1  ''
              404  UNPACK_SEQUENCE_2     2 
              406  STORE_FAST               'base'
              408  STORE_FAST               '_'

 L. 517       410  LOAD_GLOBAL              os
              412  LOAD_ATTR                path
              414  LOAD_METHOD              join
              416  LOAD_FAST                'rc_dir'
              418  LOAD_FAST                'base'
              420  LOAD_STR                 '.rc'
              422  BINARY_ADD       
              424  CALL_METHOD_2         2  ''
              426  STORE_FAST               'rc_file'

 L. 519       428  LOAD_FAST                'self'
              430  LOAD_METHOD              spawn
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                rc
              436  BUILD_LIST_1          1 

 L. 520       438  LOAD_STR                 '/fo'
              440  LOAD_FAST                'obj'
              442  BINARY_ADD       
              444  BUILD_LIST_1          1 

 L. 519       446  BINARY_ADD       

 L. 520       448  LOAD_FAST                'rc_file'
              450  BUILD_LIST_1          1 

 L. 519       452  BINARY_ADD       
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
              458  POP_BLOCK        
              460  JUMP_BACK           100  'to 100'
            462_0  COME_FROM_FINALLY   352  '352'

 L. 522       462  DUP_TOP          
              464  LOAD_GLOBAL              DistutilsExecError
              466  COMPARE_OP               exception-match
          468_470  POP_JUMP_IF_FALSE   504  'to 504'
              472  POP_TOP          
              474  STORE_FAST               'msg'
              476  POP_TOP          
              478  SETUP_FINALLY       492  'to 492'

 L. 523       480  LOAD_GLOBAL              CompileError
              482  LOAD_FAST                'msg'
              484  CALL_FUNCTION_1       1  ''
              486  RAISE_VARARGS_1       1  'exception instance'
              488  POP_BLOCK        
              490  BEGIN_FINALLY    
            492_0  COME_FROM_FINALLY   478  '478'
              492  LOAD_CONST               None
              494  STORE_FAST               'msg'
              496  DELETE_FAST              'msg'
              498  END_FINALLY      
              500  POP_EXCEPT       
              502  JUMP_BACK           100  'to 100'
            504_0  COME_FROM           468  '468'
              504  END_FINALLY      

 L. 524       506  JUMP_BACK           100  'to 100'
              508  JUMP_FORWARD        526  'to 526'
            510_0  COME_FROM           324  '324'

 L. 527       510  LOAD_GLOBAL              CompileError
              512  LOAD_STR                 "Don't know how to compile %s to %s"

 L. 528       514  LOAD_FAST                'src'
              516  LOAD_FAST                'obj'
              518  BUILD_TUPLE_2         2 

 L. 527       520  BINARY_MODULO    
              522  CALL_FUNCTION_1       1  ''
              524  RAISE_VARARGS_1       1  'exception instance'
            526_0  COME_FROM           508  '508'
            526_1  COME_FROM           314  '314'
            526_2  COME_FROM           204  '204'
            526_3  COME_FROM           182  '182'

 L. 530       526  LOAD_STR                 '/Fo'
              528  LOAD_FAST                'obj'
              530  BINARY_ADD       
              532  STORE_FAST               'output_opt'

 L. 531       534  SETUP_FINALLY       574  'to 574'

 L. 532       536  LOAD_FAST                'self'
              538  LOAD_METHOD              spawn
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                cc
              544  BUILD_LIST_1          1 
              546  LOAD_FAST                'compile_opts'
              548  BINARY_ADD       
              550  LOAD_FAST                'pp_opts'
              552  BINARY_ADD       

 L. 533       554  LOAD_FAST                'input_opt'
              556  LOAD_FAST                'output_opt'
              558  BUILD_LIST_2          2 

 L. 532       560  BINARY_ADD       

 L. 534       562  LOAD_FAST                'extra_postargs'

 L. 532       564  BINARY_ADD       
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
              570  POP_BLOCK        
              572  JUMP_BACK           100  'to 100'
            574_0  COME_FROM_FINALLY   534  '534'

 L. 535       574  DUP_TOP          
              576  LOAD_GLOBAL              DistutilsExecError
              578  COMPARE_OP               exception-match
          580_582  POP_JUMP_IF_FALSE   616  'to 616'
              584  POP_TOP          
              586  STORE_FAST               'msg'
              588  POP_TOP          
              590  SETUP_FINALLY       604  'to 604'

 L. 536       592  LOAD_GLOBAL              CompileError
              594  LOAD_FAST                'msg'
              596  CALL_FUNCTION_1       1  ''
              598  RAISE_VARARGS_1       1  'exception instance'
              600  POP_BLOCK        
              602  BEGIN_FINALLY    
            604_0  COME_FROM_FINALLY   590  '590'
              604  LOAD_CONST               None
              606  STORE_FAST               'msg'
              608  DELETE_FAST              'msg'
              610  END_FINALLY      
              612  POP_EXCEPT       
              614  JUMP_BACK           100  'to 100'
            616_0  COME_FROM           580  '580'
              616  END_FINALLY      
              618  JUMP_BACK           100  'to 100'

 L. 538       620  LOAD_FAST                'objects'
              622  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 142

    def create_static_lib(self, objects, output_libname, output_dir=None, debug=0, target_lang=None):
        if not self.initialized:
            self.initialize()
        else:
            objects, output_dir = self._fix_object_args(objects, output_dir)
            output_filename = self.library_filename(output_libname, output_dir=output_dir)
            if self._need_link(objects, output_filename):
                lib_args = objects + ['/OUT:' + output_filename]
                if debug:
                    pass
                try:
                    self.spawn([self.lib] + lib_args)
                except DistutilsExecError as msg:
                    try:
                        raise LibError(msg)
                    finally:
                        msg = None
                        del msg

            else:
                log.debug('skipping %s (up-to-date)', output_filename)

    def link(self, target_desc, objects, output_filename, output_dir=None, libraries=None, library_dirs=None, runtime_library_dirs=None, export_symbols=None, debug=0, extra_preargs=None, extra_postargs=None, build_temp=None, target_lang=None):
        if not self.initialized:
            self.initialize()
        else:
            objects, output_dir = self._fix_object_args(objects, output_dir)
            fixed_args = self._fix_lib_argslibrarieslibrary_dirsruntime_library_dirs
            libraries, library_dirs, runtime_library_dirs = fixed_args
            if runtime_library_dirs:
                self.warn("I don't know what to do with 'runtime_library_dirs': " + str(runtime_library_dirs))
            else:
                lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
                if output_dir is not None:
                    output_filename = os.path.join(output_dir, output_filename)
                if self._need_link(objects, output_filename):
                    if target_desc == CCompiler.EXECUTABLE:
                        if debug:
                            ldflags = self.ldflags_shared_debug[1:]
                        else:
                            ldflags = self.ldflags_shared[1:]
                    elif debug:
                        ldflags = self.ldflags_shared_debug
                    else:
                        ldflags = self.ldflags_shared
                    export_opts = []
                    for sym in export_symbols or []:
                        export_opts.append('/EXPORT:' + sym)
                    else:
                        ld_args = ldflags + lib_opts + export_opts + objects + [
                         '/OUT:' + output_filename]
                        build_temp = os.path.dirname(objects[0])
                        if export_symbols is not None:
                            dll_name, dll_ext = os.path.splitext(os.path.basename(output_filename))
                            implib_file = os.path.join(build_temp, self.library_filename(dll_name))
                            ld_args.append('/IMPLIB:' + implib_file)
                        self.manifest_setup_ldargsoutput_filenamebuild_templd_args
                        if extra_preargs:
                            ld_args[:0] = extra_preargs
                        if extra_postargs:
                            ld_args.extend(extra_postargs)
                        self.mkpath(os.path.dirname(output_filename))
                        try:
                            self.spawn([self.linker] + ld_args)
                        except DistutilsExecError as msg:
                            try:
                                raise LinkError(msg)
                            finally:
                                msg = None
                                del msg

                        else:
                            mfinfo = self.manifest_get_embed_info(target_desc, ld_args)
                            if mfinfo is not None:
                                mffilename, mfid = mfinfo
                                out_arg = '-outputresource:%s;%s' % (output_filename, mfid)
                                try:
                                    self.spawn(['mt.exe', '-nologo', '-manifest',
                                     mffilename, out_arg])
                                except DistutilsExecError as msg:
                                    try:
                                        raise LinkError(msg)
                                    finally:
                                        msg = None
                                        del msg

                else:
                    log.debug('skipping %s (up-to-date)', output_filename)

    def manifest_setup_ldargs(self, output_filename, build_temp, ld_args):
        temp_manifest = os.path.join(build_temp, os.path.basename(output_filename) + '.manifest')
        ld_args.append('/MANIFESTFILE:' + temp_manifest)

    def manifest_get_embed_info(self, target_desc, ld_args):
        for arg in ld_args:
            if arg.startswith('/MANIFESTFILE:'):
                temp_manifest = arg.split(':', 1)[1]
                break
            return
            if target_desc == CCompiler.EXECUTABLE:
                mfid = 1
            else:
                mfid = 2
                temp_manifest = self._remove_visual_c_ref(temp_manifest)
            if temp_manifest is None:
                return
            return (
             temp_manifest, mfid)

    def _remove_visual_c_ref--- This code section failed: ---

 L. 698         0  SETUP_FINALLY       162  'to 162'

 L. 707         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'manifest_file'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'manifest_f'

 L. 708        10  SETUP_FINALLY        24  'to 24'

 L. 709        12  LOAD_FAST                'manifest_f'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'manifest_buf'
               20  POP_BLOCK        
               22  BEGIN_FINALLY    
             24_0  COME_FROM_FINALLY    10  '10'

 L. 711        24  LOAD_FAST                'manifest_f'
               26  LOAD_METHOD              close
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          
               32  END_FINALLY      

 L. 712        34  LOAD_GLOBAL              re
               36  LOAD_METHOD              compile

 L. 713        38  LOAD_STR                 '<assemblyIdentity.*?name=("|\')Microsoft\\.VC\\d{2}\\.CRT("|\').*?(/>|</assemblyIdentity>)'

 L. 715        40  LOAD_GLOBAL              re
               42  LOAD_ATTR                DOTALL

 L. 712        44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'pattern'

 L. 716        48  LOAD_GLOBAL              re
               50  LOAD_METHOD              sub
               52  LOAD_FAST                'pattern'
               54  LOAD_STR                 ''
               56  LOAD_FAST                'manifest_buf'
               58  CALL_METHOD_3         3  ''
               60  STORE_FAST               'manifest_buf'

 L. 717        62  LOAD_STR                 '<dependentAssembly>\\s*</dependentAssembly>'
               64  STORE_FAST               'pattern'

 L. 718        66  LOAD_GLOBAL              re
               68  LOAD_METHOD              sub
               70  LOAD_FAST                'pattern'
               72  LOAD_STR                 ''
               74  LOAD_FAST                'manifest_buf'
               76  CALL_METHOD_3         3  ''
               78  STORE_FAST               'manifest_buf'

 L. 721        80  LOAD_GLOBAL              re
               82  LOAD_METHOD              compile

 L. 722        84  LOAD_STR                 '<assemblyIdentity.*?name=(?:"|\')(.+?)(?:"|\').*?(?:/>|</assemblyIdentity>)'

 L. 723        86  LOAD_GLOBAL              re
               88  LOAD_ATTR                DOTALL

 L. 721        90  CALL_METHOD_2         2  ''
               92  STORE_FAST               'pattern'

 L. 724        94  LOAD_GLOBAL              re
               96  LOAD_METHOD              search
               98  LOAD_FAST                'pattern'
              100  LOAD_FAST                'manifest_buf'
              102  CALL_METHOD_2         2  ''
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   116  'to 116'

 L. 725       110  POP_BLOCK        
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM           108  '108'

 L. 727       116  LOAD_GLOBAL              open
              118  LOAD_FAST                'manifest_file'
              120  LOAD_STR                 'w'
              122  CALL_FUNCTION_2       2  ''
              124  STORE_FAST               'manifest_f'

 L. 728       126  SETUP_FINALLY       148  'to 148'

 L. 729       128  LOAD_FAST                'manifest_f'
              130  LOAD_METHOD              write
              132  LOAD_FAST                'manifest_buf'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L. 730       138  LOAD_FAST                'manifest_file'
              140  POP_BLOCK        
              142  CALL_FINALLY        148  'to 148'
              144  POP_BLOCK        
              146  RETURN_VALUE     
            148_0  COME_FROM           142  '142'
            148_1  COME_FROM_FINALLY   126  '126'

 L. 732       148  LOAD_FAST                'manifest_f'
              150  LOAD_METHOD              close
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          
              156  END_FINALLY      
              158  POP_BLOCK        
              160  JUMP_FORWARD        182  'to 182'
            162_0  COME_FROM_FINALLY     0  '0'

 L. 733       162  DUP_TOP          
              164  LOAD_GLOBAL              OSError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   180  'to 180'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 734       176  POP_EXCEPT       
              178  JUMP_FORWARD        182  'to 182'
            180_0  COME_FROM           168  '168'
              180  END_FINALLY      
            182_0  COME_FROM           178  '178'
            182_1  COME_FROM           160  '160'

Parse error at or near `LOAD_CONST' instruction at offset 112

    def library_dir_option(self, dir):
        return '/LIBPATH:' + dir

    def runtime_library_dir_option(self, dir):
        raise DistutilsPlatformError("don't know how to set runtime library search path for MSVC++")

    def library_option(self, lib):
        return self.library_filename(lib)

    def find_library_file(self, dirs, lib, debug=0):
        if debug:
            try_names = [
             lib + '_d', lib]
        else:
            try_names = [
             lib]
        for dir in dirs:
            for name in try_names:
                libfile = os.path.join(dir, self.library_filename(name))
                if os.path.exists(libfile):
                    return libfile

    def find_exe(self, exe):
        """Return path to an MSVC executable program.

        Tries to find the program in several places: first, one of the
        MSVC program search paths from the registry; next, the directories
        in the PATH environment variable.  If any of those work, return an
        absolute path that is known to exist.  If none of them work, just
        return the original program name, 'exe'.
        """
        for p in self._MSVCCompiler__paths:
            fn = os.path.join(os.path.abspath(p), exe)
            if os.path.isfile(fn):
                return fn
            for p in os.environ['Path'].split(';'):
                fn = os.path.join(os.path.abspath(p), exe)
                if os.path.isfile(fn):
                    return fn
                return exe