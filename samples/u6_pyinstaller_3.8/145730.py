# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\_msvccompiler.py
"""distutils._msvccompiler

Contains MSVCCompiler, an implementation of the abstract CCompiler class
for Microsoft Visual Studio 2015.

The module is compatible with VS 2015 and later. You can find legacy support
for older versions in distutils.msvc9compiler and distutils.msvccompiler.
"""
import os, shutil, stat, subprocess, winreg
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_lib_options
from distutils import log
from distutils.util import get_platform
from itertools import count

def _find_vc2015--- This code section failed: ---

 L.  31         0  SETUP_FINALLY        32  'to 32'

 L.  32         2  LOAD_GLOBAL              winreg
                4  LOAD_ATTR                OpenKeyEx

 L.  33         6  LOAD_GLOBAL              winreg
                8  LOAD_ATTR                HKEY_LOCAL_MACHINE

 L.  34        10  LOAD_STR                 'Software\\Microsoft\\VisualStudio\\SxS\\VC7'

 L.  35        12  LOAD_GLOBAL              winreg
               14  LOAD_ATTR                KEY_READ
               16  LOAD_GLOBAL              winreg
               18  LOAD_ATTR                KEY_WOW64_32KEY
               20  BINARY_OR        

 L.  32        22  LOAD_CONST               ('access',)
               24  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               26  STORE_FAST               'key'
               28  POP_BLOCK        
               30  JUMP_FORWARD         64  'to 64'
             32_0  COME_FROM_FINALLY     0  '0'

 L.  37        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    62  'to 62'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  38        46  LOAD_GLOBAL              log
               48  LOAD_METHOD              debug
               50  LOAD_STR                 'Visual C++ is not registered'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L.  39        56  POP_EXCEPT       
               58  LOAD_CONST               (None, None)
               60  RETURN_VALUE     
             62_0  COME_FROM            38  '38'
               62  END_FINALLY      
             64_0  COME_FROM            30  '30'

 L.  41        64  LOAD_CONST               0
               66  STORE_FAST               'best_version'

 L.  42        68  LOAD_CONST               None
               70  STORE_FAST               'best_dir'

 L.  43        72  LOAD_FAST                'key'
               74  SETUP_WITH          242  'to 242'
               76  POP_TOP          

 L.  44        78  LOAD_GLOBAL              count
               80  CALL_FUNCTION_0       0  ''
               82  GET_ITER         
             84_0  COME_FROM           224  '224'
             84_1  COME_FROM           216  '216'
             84_2  COME_FROM           162  '162'
             84_3  COME_FROM           150  '150'
             84_4  COME_FROM           140  '140'
               84  FOR_ITER            238  'to 238'
               86  STORE_FAST               'i'

 L.  45        88  SETUP_FINALLY       112  'to 112'

 L.  46        90  LOAD_GLOBAL              winreg
               92  LOAD_METHOD              EnumValue
               94  LOAD_FAST                'key'
               96  LOAD_FAST                'i'
               98  CALL_METHOD_2         2  ''
              100  UNPACK_SEQUENCE_3     3 
              102  STORE_FAST               'v'
              104  STORE_FAST               'vc_dir'
              106  STORE_FAST               'vt'
              108  POP_BLOCK        
              110  JUMP_FORWARD        138  'to 138'
            112_0  COME_FROM_FINALLY    88  '88'

 L.  47       112  DUP_TOP          
              114  LOAD_GLOBAL              OSError
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   136  'to 136'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L.  48       126  POP_EXCEPT       
              128  POP_TOP          
              130  BREAK_LOOP          238  'to 238'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           118  '118'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           110  '110'

 L.  49       138  LOAD_FAST                'v'
              140  POP_JUMP_IF_FALSE    84  'to 84'
              142  LOAD_FAST                'vt'
              144  LOAD_GLOBAL              winreg
              146  LOAD_ATTR                REG_SZ
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE    84  'to 84'
              152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              isdir
              158  LOAD_FAST                'vc_dir'
              160  CALL_METHOD_1         1  ''
              162  POP_JUMP_IF_FALSE    84  'to 84'

 L.  50       164  SETUP_FINALLY       182  'to 182'

 L.  51       166  LOAD_GLOBAL              int
              168  LOAD_GLOBAL              float
              170  LOAD_FAST                'v'
              172  CALL_FUNCTION_1       1  ''
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'version'
              178  POP_BLOCK        
              180  JUMP_FORWARD        210  'to 210'
            182_0  COME_FROM_FINALLY   164  '164'

 L.  52       182  DUP_TOP          
              184  LOAD_GLOBAL              ValueError
              186  LOAD_GLOBAL              TypeError
              188  BUILD_TUPLE_2         2 
              190  COMPARE_OP               exception-match
              192  POP_JUMP_IF_FALSE   208  'to 208'
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L.  53       200  POP_EXCEPT       
              202  JUMP_BACK            84  'to 84'
              204  POP_EXCEPT       
              206  JUMP_FORWARD        210  'to 210'
            208_0  COME_FROM           192  '192'
              208  END_FINALLY      
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM           180  '180'

 L.  54       210  LOAD_FAST                'version'
              212  LOAD_CONST               14
              214  COMPARE_OP               >=
              216  POP_JUMP_IF_FALSE    84  'to 84'
              218  LOAD_FAST                'version'
              220  LOAD_FAST                'best_version'
              222  COMPARE_OP               >
              224  POP_JUMP_IF_FALSE    84  'to 84'

 L.  55       226  LOAD_FAST                'version'
              228  LOAD_FAST                'vc_dir'
              230  ROT_TWO          
              232  STORE_FAST               'best_version'
              234  STORE_FAST               'best_dir'
              236  JUMP_BACK            84  'to 84'
              238  POP_BLOCK        
              240  BEGIN_FINALLY    
            242_0  COME_FROM_WITH       74  '74'
              242  WITH_CLEANUP_START
              244  WITH_CLEANUP_FINISH
              246  END_FINALLY      

 L.  56       248  LOAD_FAST                'best_version'
              250  LOAD_FAST                'best_dir'
              252  BUILD_TUPLE_2         2 
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 58


def _find_vc2017():
    """Returns "15, path" based on the result of invoking vswhere.exe
    If no install is found, returns "None, None"

    The version is returned to avoid unnecessarily changing the function
    result. It may be ignored when the path is not None.

    If vswhere.exe is not available, by definition, VS 2017 is not
    installed.
    """
    import json
    root = os.environ.get'ProgramFiles(x86)' or os.environ.get'ProgramFiles'
    if not root:
        return (None, None)
    try:
        path = subprocess.check_output([
         os.path.join(root, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe'),
         '-latest',
         '-prerelease',
         '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
         '-property', 'installationPath',
         '-products', '*'],
          encoding='mbcs',
          errors='strict').strip()
    except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
        return (None, None)
    else:
        path = os.path.join(path, 'VC', 'Auxiliary', 'Build')
        if os.path.isdirpath:
            return (
             15, path)
        return (None, None)


PLAT_SPEC_TO_RUNTIME = {'x86':'x86', 
 'x86_amd64':'x64', 
 'x86_arm':'arm', 
 'x86_arm64':'arm64'}

def _find_vcvarsall(plat_spec):
    _, best_dir = _find_vc2017
    vcruntime = None
    if plat_spec in PLAT_SPEC_TO_RUNTIME:
        vcruntime_plat = PLAT_SPEC_TO_RUNTIME[plat_spec]
    else:
        vcruntime_plat = 'x64' if 'amd64' in plat_spec else 'x86'
    if best_dir:
        vcredist = os.path.join(best_dir, '..', '..', 'redist', 'MSVC', '**', vcruntime_plat, 'Microsoft.VC14*.CRT', 'vcruntime140.dll')
        try:
            import glob
            vcruntime = glob.glob(vcredist, recursive=True)[(-1)]
        except (ImportError, OSError, LookupError):
            vcruntime = None

    if not best_dir:
        best_version, best_dir = _find_vc2015
        if best_version:
            vcruntime = os.path.join(best_dir, 'redist', vcruntime_plat, 'Microsoft.VC140.CRT', 'vcruntime140.dll')
    if not best_dir:
        log.debug'No suitable Visual C++ version found'
        return (None, None)
    vcvarsall = os.path.joinbest_dir'vcvarsall.bat'
    if not os.path.isfilevcvarsall:
        log.debug'%s cannot be found'vcvarsall
        return (None, None)
    if not (vcruntime and os.path.isfilevcruntime):
        log.debug'%s cannot be found'vcruntime
        vcruntime = None
    return (vcvarsall, vcruntime)


def _get_vc_env(plat_spec):
    if os.getenv'DISTUTILS_USE_SDK':
        return {value:key.lower() for key, value in os.environ.items()}
    vcvarsall, vcruntime = _find_vcvarsall(plat_spec)
    if not vcvarsall:
        raise DistutilsPlatformError('Unable to find vcvarsall.bat')
    try:
        out = subprocess.check_output(('cmd /u /c "{}" {} && set'.formatvcvarsallplat_spec),
          stderr=(subprocess.STDOUT)).decode('utf-16le',
          errors='replace')
    except subprocess.CalledProcessError as exc:
        try:
            log.errorexc.output
            raise DistutilsPlatformError('Error executing {}'.formatexc.cmd)
        finally:
            exc = None
            del exc

    else:
        env = {value:key.lower() for key, _, value in (line.partition'=' for line in out.splitlines()) if key if value if value}
        if vcruntime:
            env['py_vcruntime_redist'] = vcruntime
        return env


def _find_exe(exe, paths=None):
    """Return path to an MSVC executable program.

    Tries to find the program in several places: first, one of the
    MSVC program search paths from the registry; next, the directories
    in the PATH environment variable.  If any of those work, return an
    absolute path that is known to exist.  If none of them work, just
    return the original program name, 'exe'.
    """
    if not paths:
        paths = os.getenv'path'.splitos.pathsep
    for p in paths:
        fn = os.path.joinos.path.abspathpexe
        if os.path.isfilefn:
            return fn
        return exe


PLAT_TO_VCVARS = {'win32':'x86', 
 'win-amd64':'x86_amd64', 
 'win-arm32':'x86_arm', 
 'win-arm64':'x86_arm64'}
_BUNDLED_DLLS = frozenset(['vcruntime140.dll'])

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
        self.plat_name = None
        self.initialized = False

    def initialize(self, plat_name=None):
        if self.initialized:
            raise AssertionError("don't init multiple times")
        else:
            if plat_name is None:
                plat_name = get_platform
            if plat_name not in PLAT_TO_VCVARS:
                raise DistutilsPlatformError('--plat-name must be one of {}'.formattuple(PLAT_TO_VCVARS))
            plat_spec = PLAT_TO_VCVARS[plat_name]
            vc_env = _get_vc_env(plat_spec)
            assert vc_env, 'Unable to find a compatible Visual Studio installation.'
        self._paths = vc_env.get'path'''
        paths = self._paths.splitos.pathsep
        self.cc = _find_exe('cl.exe', paths)
        self.linker = _find_exe('link.exe', paths)
        self.lib = _find_exe('lib.exe', paths)
        self.rc = _find_exe('rc.exe', paths)
        self.mc = _find_exe('mc.exe', paths)
        self.mt = _find_exe('mt.exe', paths)
        self._vcruntime_redist = vc_env.get'py_vcruntime_redist'''
        for dir in vc_env.get'include'''.splitos.pathsep:
            if dir:
                self.add_include_dirdir.rstripos.sep
        else:
            for dir in vc_env.get'lib'''.splitos.pathsep:
                if dir:
                    self.add_library_dirdir.rstripos.sep
            else:
                self.preprocess_options = None
                self.compile_options = [
                 '/nologo', '/Ox', '/W3', '/GL', '/DNDEBUG']
                self.compile_options.append('/MD' if self._vcruntime_redist else '/MT')
                self.compile_options_debug = [
                 '/nologo', '/Od', '/MDd', '/Zi', '/W3', '/D_DEBUG']
                ldflags = [
                 '/nologo', '/INCREMENTAL:NO', '/LTCG']
                if not self._vcruntime_redist:
                    ldflags.extend('/nodefaultlib:libucrt.lib', 'ucrt.lib')
                ldflags_debug = [
                 '/nologo', '/INCREMENTAL:NO', '/LTCG', '/DEBUG:FULL']
                self.ldflags_exe = [
                 *ldflags, '/MANIFEST:EMBED,ID=1']
                self.ldflags_exe_debug = [*ldflags_debug, '/MANIFEST:EMBED,ID=1']
                self.ldflags_shared = [*ldflags, '/DLL', '/MANIFEST:EMBED,ID=2', '/MANIFESTUAC:NO']
                self.ldflags_shared_debug = [*ldflags_debug, '/DLL', '/MANIFEST:EMBED,ID=2', '/MANIFESTUAC:NO']
                self.ldflags_static = [*ldflags]
                self.ldflags_static_debug = [*ldflags_debug]
                self._ldflags = {(
 CCompiler.EXECUTABLE, None): self.ldflags_exe, 
                 (
 CCompiler.EXECUTABLE, False): self.ldflags_exe, 
                 (
 CCompiler.EXECUTABLE, True): self.ldflags_exe_debug, 
                 (
 CCompiler.SHARED_OBJECT, None): self.ldflags_shared, 
                 (
 CCompiler.SHARED_OBJECT, False): self.ldflags_shared, 
                 (
 CCompiler.SHARED_OBJECT, True): self.ldflags_shared_debug, 
                 (
 CCompiler.SHARED_LIBRARY, None): self.ldflags_static, 
                 (
 CCompiler.SHARED_LIBRARY, False): self.ldflags_static, 
                 (
 CCompiler.SHARED_LIBRARY, True): self.ldflags_static_debug}
                self.initialized = True

    def object_filenames--- This code section failed: ---

 L. 327         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'MSVCCompiler.object_filenames.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                src_extensions
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''

 L. 328        18  LOAD_CLOSURE             'self'
               20  BUILD_TUPLE_1         1 
               22  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               24  LOAD_STR                 'MSVCCompiler.object_filenames.<locals>.<dictcomp>'
               26  MAKE_FUNCTION_8          'closure'
               28  LOAD_DEREF               'self'
               30  LOAD_ATTR                _rc_extensions
               32  LOAD_DEREF               'self'
               34  LOAD_ATTR                _mc_extensions
               36  BINARY_ADD       
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''

 L. 326        42  BUILD_MAP_UNPACK_2     2 
               44  STORE_DEREF              'ext_map'

 L. 331        46  LOAD_DEREF               'output_dir'
               48  JUMP_IF_TRUE_OR_POP    52  'to 52'
               50  LOAD_STR                 ''
             52_0  COME_FROM            48  '48'
               52  STORE_DEREF              'output_dir'

 L. 333        54  LOAD_CLOSURE             'ext_map'
               56  LOAD_CLOSURE             'output_dir'
               58  LOAD_CLOSURE             'strip_dir'
               60  BUILD_TUPLE_3         3 
               62  LOAD_CODE                <code_object make_out_path>
               64  LOAD_STR                 'MSVCCompiler.object_filenames.<locals>.make_out_path'
               66  MAKE_FUNCTION_8          'closure'
               68  STORE_FAST               'make_out_path'

 L. 352        70  LOAD_GLOBAL              list
               72  LOAD_GLOBAL              map
               74  LOAD_FAST                'make_out_path'
               76  LOAD_FAST                'source_filenames'
               78  CALL_FUNCTION_2       2  ''
               80  CALL_FUNCTION_1       1  ''
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def compile--- This code section failed: ---

 L. 359         0  LOAD_FAST                'self'
                2  LOAD_ATTR                initialized
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 360         6  LOAD_FAST                'self'
                8  LOAD_METHOD              initialize
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          
             14_0  COME_FROM             4  '4'

 L. 361        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _setup_compile
               18  LOAD_FAST                'output_dir'
               20  LOAD_FAST                'macros'
               22  LOAD_FAST                'include_dirs'

 L. 362        24  LOAD_FAST                'sources'

 L. 362        26  LOAD_FAST                'depends'

 L. 362        28  LOAD_FAST                'extra_postargs'

 L. 361        30  CALL_METHOD_6         6  ''
               32  STORE_FAST               'compile_info'

 L. 363        34  LOAD_FAST                'compile_info'
               36  UNPACK_SEQUENCE_5     5 
               38  STORE_FAST               'macros'
               40  STORE_FAST               'objects'
               42  STORE_FAST               'extra_postargs'
               44  STORE_FAST               'pp_opts'
               46  STORE_FAST               'build'

 L. 365        48  LOAD_FAST                'extra_preargs'
               50  JUMP_IF_TRUE_OR_POP    54  'to 54'
               52  BUILD_LIST_0          0 
             54_0  COME_FROM            50  '50'
               54  STORE_FAST               'compile_opts'

 L. 366        56  LOAD_FAST                'compile_opts'
               58  LOAD_METHOD              append
               60  LOAD_STR                 '/c'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 367        66  LOAD_FAST                'debug'
               68  POP_JUMP_IF_FALSE    84  'to 84'

 L. 368        70  LOAD_FAST                'compile_opts'
               72  LOAD_METHOD              extend
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                compile_options_debug
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM            68  '68'

 L. 370        84  LOAD_FAST                'compile_opts'
               86  LOAD_METHOD              extend
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                compile_options
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            82  '82'

 L. 373        96  LOAD_CONST               False
               98  STORE_FAST               'add_cpp_opts'

 L. 375       100  LOAD_FAST                'objects'
              102  GET_ITER         
          104_106  FOR_ITER            642  'to 642'
              108  STORE_FAST               'obj'

 L. 376       110  SETUP_FINALLY       128  'to 128'

 L. 377       112  LOAD_FAST                'build'
              114  LOAD_FAST                'obj'
              116  BINARY_SUBSCR    
              118  UNPACK_SEQUENCE_2     2 
              120  STORE_FAST               'src'
              122  STORE_FAST               'ext'
              124  POP_BLOCK        
              126  JUMP_FORWARD        152  'to 152'
            128_0  COME_FROM_FINALLY   110  '110'

 L. 378       128  DUP_TOP          
              130  LOAD_GLOBAL              KeyError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   150  'to 150'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 379       142  POP_EXCEPT       
              144  JUMP_BACK           104  'to 104'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           134  '134'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           126  '126'

 L. 380       152  LOAD_FAST                'debug'
              154  POP_JUMP_IF_FALSE   168  'to 168'

 L. 384       156  LOAD_GLOBAL              os
              158  LOAD_ATTR                path
              160  LOAD_METHOD              abspath
              162  LOAD_FAST                'src'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'src'
            168_0  COME_FROM           154  '154'

 L. 386       168  LOAD_FAST                'ext'
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _c_extensions
              174  COMPARE_OP               in
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L. 387       178  LOAD_STR                 '/Tc'
              180  LOAD_FAST                'src'
              182  BINARY_ADD       
              184  STORE_FAST               'input_opt'
          186_188  JUMP_FORWARD        514  'to 514'
            190_0  COME_FROM           176  '176'

 L. 388       190  LOAD_FAST                'ext'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                _cpp_extensions
              196  COMPARE_OP               in
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L. 389       200  LOAD_STR                 '/Tp'
              202  LOAD_FAST                'src'
              204  BINARY_ADD       
              206  STORE_FAST               'input_opt'

 L. 390       208  LOAD_CONST               True
              210  STORE_FAST               'add_cpp_opts'
          212_214  JUMP_FORWARD        514  'to 514'
            216_0  COME_FROM           198  '198'

 L. 391       216  LOAD_FAST                'ext'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _rc_extensions
              222  COMPARE_OP               in
          224_226  POP_JUMP_IF_FALSE   320  'to 320'

 L. 393       228  LOAD_FAST                'src'
              230  STORE_FAST               'input_opt'

 L. 394       232  LOAD_STR                 '/fo'
              234  LOAD_FAST                'obj'
              236  BINARY_ADD       
              238  STORE_FAST               'output_opt'

 L. 395       240  SETUP_FINALLY       272  'to 272'

 L. 396       242  LOAD_FAST                'self'
              244  LOAD_METHOD              spawn
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                rc
              250  BUILD_LIST_1          1 
              252  LOAD_FAST                'pp_opts'
              254  BINARY_ADD       
              256  LOAD_FAST                'output_opt'
              258  LOAD_FAST                'input_opt'
              260  BUILD_LIST_2          2 
              262  BINARY_ADD       
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
              268  POP_BLOCK        
              270  JUMP_BACK           104  'to 104'
            272_0  COME_FROM_FINALLY   240  '240'

 L. 397       272  DUP_TOP          
              274  LOAD_GLOBAL              DistutilsExecError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   314  'to 314'
              282  POP_TOP          
              284  STORE_FAST               'msg'
              286  POP_TOP          
              288  SETUP_FINALLY       302  'to 302'

 L. 398       290  LOAD_GLOBAL              CompileError
              292  LOAD_FAST                'msg'
              294  CALL_FUNCTION_1       1  ''
              296  RAISE_VARARGS_1       1  'exception instance'
              298  POP_BLOCK        
              300  BEGIN_FINALLY    
            302_0  COME_FROM_FINALLY   288  '288'
              302  LOAD_CONST               None
              304  STORE_FAST               'msg'
              306  DELETE_FAST              'msg'
              308  END_FINALLY      
              310  POP_EXCEPT       
              312  JUMP_BACK           104  'to 104'
            314_0  COME_FROM           278  '278'
              314  END_FINALLY      

 L. 399       316  JUMP_BACK           104  'to 104'
              318  JUMP_FORWARD        514  'to 514'
            320_0  COME_FROM           224  '224'

 L. 400       320  LOAD_FAST                'ext'
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                _mc_extensions
              326  COMPARE_OP               in
          328_330  POP_JUMP_IF_FALSE   498  'to 498'

 L. 412       332  LOAD_GLOBAL              os
              334  LOAD_ATTR                path
              336  LOAD_METHOD              dirname
              338  LOAD_FAST                'src'
              340  CALL_METHOD_1         1  ''
              342  STORE_FAST               'h_dir'

 L. 413       344  LOAD_GLOBAL              os
              346  LOAD_ATTR                path
              348  LOAD_METHOD              dirname
              350  LOAD_FAST                'obj'
              352  CALL_METHOD_1         1  ''
              354  STORE_FAST               'rc_dir'

 L. 414       356  SETUP_FINALLY       450  'to 450'

 L. 416       358  LOAD_FAST                'self'
              360  LOAD_METHOD              spawn
              362  LOAD_FAST                'self'
              364  LOAD_ATTR                mc
              366  LOAD_STR                 '-h'
              368  LOAD_FAST                'h_dir'
              370  LOAD_STR                 '-r'
              372  LOAD_FAST                'rc_dir'
              374  LOAD_FAST                'src'
              376  BUILD_LIST_6          6 
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          

 L. 417       382  LOAD_GLOBAL              os
              384  LOAD_ATTR                path
              386  LOAD_METHOD              splitext
              388  LOAD_GLOBAL              os
              390  LOAD_ATTR                path
              392  LOAD_METHOD              basename
              394  LOAD_FAST                'src'
              396  CALL_METHOD_1         1  ''
              398  CALL_METHOD_1         1  ''
              400  UNPACK_SEQUENCE_2     2 
              402  STORE_FAST               'base'
              404  STORE_FAST               '_'

 L. 418       406  LOAD_GLOBAL              os
              408  LOAD_ATTR                path
              410  LOAD_METHOD              join
              412  LOAD_FAST                'rc_dir'
              414  LOAD_FAST                'base'
              416  LOAD_STR                 '.rc'
              418  BINARY_ADD       
              420  CALL_METHOD_2         2  ''
              422  STORE_FAST               'rc_file'

 L. 420       424  LOAD_FAST                'self'
              426  LOAD_METHOD              spawn
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                rc
              432  LOAD_STR                 '/fo'
              434  LOAD_FAST                'obj'
              436  BINARY_ADD       
              438  LOAD_FAST                'rc_file'
              440  BUILD_LIST_3          3 
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          
              446  POP_BLOCK        
              448  JUMP_BACK           104  'to 104'
            450_0  COME_FROM_FINALLY   356  '356'

 L. 422       450  DUP_TOP          
              452  LOAD_GLOBAL              DistutilsExecError
              454  COMPARE_OP               exception-match
          456_458  POP_JUMP_IF_FALSE   492  'to 492'
              460  POP_TOP          
              462  STORE_FAST               'msg'
              464  POP_TOP          
              466  SETUP_FINALLY       480  'to 480'

 L. 423       468  LOAD_GLOBAL              CompileError
              470  LOAD_FAST                'msg'
              472  CALL_FUNCTION_1       1  ''
              474  RAISE_VARARGS_1       1  'exception instance'
              476  POP_BLOCK        
              478  BEGIN_FINALLY    
            480_0  COME_FROM_FINALLY   466  '466'
              480  LOAD_CONST               None
              482  STORE_FAST               'msg'
              484  DELETE_FAST              'msg'
              486  END_FINALLY      
              488  POP_EXCEPT       
              490  JUMP_BACK           104  'to 104'
            492_0  COME_FROM           456  '456'
              492  END_FINALLY      

 L. 424       494  JUMP_BACK           104  'to 104'
              496  JUMP_FORWARD        514  'to 514'
            498_0  COME_FROM           328  '328'

 L. 427       498  LOAD_GLOBAL              CompileError
              500  LOAD_STR                 "Don't know how to compile {} to {}"
              502  LOAD_METHOD              format

 L. 428       504  LOAD_FAST                'src'

 L. 428       506  LOAD_FAST                'obj'

 L. 427       508  CALL_METHOD_2         2  ''
              510  CALL_FUNCTION_1       1  ''
              512  RAISE_VARARGS_1       1  'exception instance'
            514_0  COME_FROM           496  '496'
            514_1  COME_FROM           318  '318'
            514_2  COME_FROM           212  '212'
            514_3  COME_FROM           186  '186'

 L. 430       514  LOAD_FAST                'self'
              516  LOAD_ATTR                cc
              518  BUILD_LIST_1          1 
              520  LOAD_FAST                'compile_opts'
              522  BINARY_ADD       
              524  LOAD_FAST                'pp_opts'
              526  BINARY_ADD       
              528  STORE_FAST               'args'

 L. 431       530  LOAD_FAST                'add_cpp_opts'
          532_534  POP_JUMP_IF_FALSE   546  'to 546'

 L. 432       536  LOAD_FAST                'args'
              538  LOAD_METHOD              append
              540  LOAD_STR                 '/EHsc'
              542  CALL_METHOD_1         1  ''
              544  POP_TOP          
            546_0  COME_FROM           532  '532'

 L. 433       546  LOAD_FAST                'args'
              548  LOAD_METHOD              append
              550  LOAD_FAST                'input_opt'
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          

 L. 434       556  LOAD_FAST                'args'
              558  LOAD_METHOD              append
              560  LOAD_STR                 '/Fo'
              562  LOAD_FAST                'obj'
              564  BINARY_ADD       
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          

 L. 435       570  LOAD_FAST                'args'
              572  LOAD_METHOD              extend
              574  LOAD_FAST                'extra_postargs'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          

 L. 437       580  SETUP_FINALLY       596  'to 596'

 L. 438       582  LOAD_FAST                'self'
              584  LOAD_METHOD              spawn
              586  LOAD_FAST                'args'
              588  CALL_METHOD_1         1  ''
              590  POP_TOP          
              592  POP_BLOCK        
              594  JUMP_BACK           104  'to 104'
            596_0  COME_FROM_FINALLY   580  '580'

 L. 439       596  DUP_TOP          
              598  LOAD_GLOBAL              DistutilsExecError
              600  COMPARE_OP               exception-match
          602_604  POP_JUMP_IF_FALSE   638  'to 638'
              606  POP_TOP          
              608  STORE_FAST               'msg'
              610  POP_TOP          
              612  SETUP_FINALLY       626  'to 626'

 L. 440       614  LOAD_GLOBAL              CompileError
              616  LOAD_FAST                'msg'
              618  CALL_FUNCTION_1       1  ''
              620  RAISE_VARARGS_1       1  'exception instance'
              622  POP_BLOCK        
              624  BEGIN_FINALLY    
            626_0  COME_FROM_FINALLY   612  '612'
              626  LOAD_CONST               None
              628  STORE_FAST               'msg'
              630  DELETE_FAST              'msg'
              632  END_FINALLY      
              634  POP_EXCEPT       
              636  JUMP_BACK           104  'to 104'
            638_0  COME_FROM           602  '602'
              638  END_FINALLY      
              640  JUMP_BACK           104  'to 104'

 L. 442       642  LOAD_FAST                'objects'
              644  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 146

    def create_static_lib(self, objects, output_libname, output_dir=None, debug=0, target_lang=None):
        if not self.initialized:
            self.initialize()
        else:
            objects, output_dir = self._fix_object_argsobjectsoutput_dir
            output_filename = self.library_filename(output_libname, output_dir=output_dir)
            if self._need_linkobjectsoutput_filename:
                lib_args = objects + ['/OUT:' + output_filename]
                if debug:
                    pass
                try:
                    log.debug('Executing "%s" %s', self.lib, ' '.joinlib_args)
                    self.spawn([self.lib] + lib_args)
                except DistutilsExecError as msg:
                    try:
                        raise LibError(msg)
                    finally:
                        msg = None
                        del msg

            else:
                log.debug'skipping %s (up-to-date)'output_filename

    def link(self, target_desc, objects, output_filename, output_dir=None, libraries=None, library_dirs=None, runtime_library_dirs=None, export_symbols=None, debug=0, extra_preargs=None, extra_postargs=None, build_temp=None, target_lang=None):
        if not self.initialized:
            self.initialize()
        else:
            objects, output_dir = self._fix_object_argsobjectsoutput_dir
            fixed_args = self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
            libraries, library_dirs, runtime_library_dirs = fixed_args
            if runtime_library_dirs:
                self.warn("I don't know what to do with 'runtime_library_dirs': " + str(runtime_library_dirs))
            lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
            if output_dir is not None:
                output_filename = os.path.joinoutput_diroutput_filename
            if self._need_linkobjectsoutput_filename:
                ldflags = self._ldflags[(target_desc, debug)]
                export_opts = ['/EXPORT:' + sym for sym in export_symbols or []]
                ld_args = ldflags + lib_opts + export_opts + objects + [
                 '/OUT:' + output_filename]
                build_temp = os.path.dirnameobjects[0]
                if export_symbols is not None:
                    dll_name, dll_ext = os.path.splitextos.path.basenameoutput_filename
                    implib_file = os.path.joinbuild_tempself.library_filenamedll_name
                    ld_args.append('/IMPLIB:' + implib_file)
                if extra_preargs:
                    ld_args[:0] = extra_preargs
                if extra_postargs:
                    ld_args.extendextra_postargs
                output_dir = os.path.dirnameos.path.abspathoutput_filename
                self.mkpathoutput_dir
                try:
                    log.debug('Executing "%s" %s', self.linker, ' '.joinld_args)
                    self.spawn([self.linker] + ld_args)
                    self._copy_vcruntimeoutput_dir
                except DistutilsExecError as msg:
                    try:
                        raise LinkError(msg)
                    finally:
                        msg = None
                        del msg

            else:
                log.debug'skipping %s (up-to-date)'output_filename

    def _copy_vcruntime(self, output_dir):
        vcruntime = self._vcruntime_redist
        return vcruntime and os.path.isfilevcruntime or None
        if os.path.basenamevcruntime.lower() in _BUNDLED_DLLS:
            return
        log.debug'Copying "%s"'vcruntime
        vcruntime = shutil.copyvcruntimeoutput_dir
        os.chmodvcruntimestat.S_IWRITE

    def spawn--- This code section failed: ---

 L. 554         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              getenv
                4  LOAD_STR                 'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'old_path'

 L. 555        10  SETUP_FINALLY        40  'to 40'

 L. 556        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _paths
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                environ
               20  LOAD_STR                 'path'
               22  STORE_SUBSCR     

 L. 557        24  LOAD_GLOBAL              super
               26  CALL_FUNCTION_0       0  ''
               28  LOAD_METHOD              spawn
               30  LOAD_FAST                'cmd'
               32  CALL_METHOD_1         1  ''
               34  POP_BLOCK        
               36  CALL_FINALLY         40  'to 40'
               38  RETURN_VALUE     
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM_FINALLY    10  '10'

 L. 559        40  LOAD_FAST                'old_path'
               42  LOAD_GLOBAL              os
               44  LOAD_ATTR                environ
               46  LOAD_STR                 'path'
               48  STORE_SUBSCR     
               50  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 36

    def library_dir_option(self, dir):
        return '/LIBPATH:' + dir

    def runtime_library_dir_option(self, dir):
        raise DistutilsPlatformError("don't know how to set runtime library search path for MSVC")

    def library_option(self, lib):
        return self.library_filenamelib

    def find_library_file(self, dirs, lib, debug=0):
        if debug:
            try_names = [
             lib + '_d', lib]
        else:
            try_names = [
             lib]
        for dir in dirs:
            for name in try_names:
                libfile = os.path.joindirself.library_filenamename
                if os.path.isfilelibfile:
                    return libfile