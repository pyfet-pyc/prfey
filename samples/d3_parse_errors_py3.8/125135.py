# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\msvccompiler.py
"""distutils.msvccompiler

Contains MSVCCompiler, an implementation of the abstract CCompiler class
for the Microsoft Visual Studio.
"""
import sys, os
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
_can_read_reg = False
try:
    import winreg
    _can_read_reg = True
    hkey_mod = winreg
    RegOpenKeyEx = winreg.OpenKeyEx
    RegEnumKey = winreg.EnumKey
    RegEnumValue = winreg.EnumValue
    RegError = winreg.error
except ImportError:
    try:
        import win32api, win32con
        _can_read_reg = True
        hkey_mod = win32con
        RegOpenKeyEx = win32api.RegOpenKeyEx
        RegEnumKey = win32api.RegEnumKey
        RegEnumValue = win32api.RegEnumValue
        RegError = win32api.error
    except ImportError:
        log.info("Warning: Can't read registry to find the necessary compiler setting\nMake sure that Python modules winreg, win32api or win32con are installed.")

else:
    if _can_read_reg:
        HKEYS = (
         hkey_mod.HKEY_USERS,
         hkey_mod.HKEY_CURRENT_USER,
         hkey_mod.HKEY_LOCAL_MACHINE,
         hkey_mod.HKEY_CLASSES_ROOT)

    def read_keys(base, key):
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


    def read_values(base, key):
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
                    d[convert_mbcs(name)] = convert_mbcs(value)
                    i += 1

            return d


    def convert_mbcs(s):
        dec = getattr(s, 'decode', None)
        if dec is not None:
            try:
                s = dec('mbcs')
            except UnicodeError:
                pass

            return s


    class MacroExpander:

        def __init__(self, version):
            self.macros = {}
            self.load_macros(version)

        def set_macro--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL              HKEYS
                2  GET_ITER         
              4_0  COME_FROM            44  '44'
              4_1  COME_FROM            20  '20'
                4  FOR_ITER             46  'to 46'
                6  STORE_FAST               'base'

 L. 109         8  LOAD_GLOBAL              read_values
               10  LOAD_FAST                'base'
               12  LOAD_FAST                'path'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'd'

 L. 110        18  LOAD_FAST                'd'
               20  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L. 111        22  LOAD_FAST                'd'
               24  LOAD_FAST                'key'
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                macros
               32  LOAD_STR                 '$(%s)'
               34  LOAD_FAST                'macro'
               36  BINARY_MODULO    
               38  STORE_SUBSCR     

 L. 112        40  POP_TOP          
               42  BREAK_LOOP           46  'to 46'
               44  JUMP_BACK             4  'to 4'
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM             4  '4'

Parse error at or near `COME_FROM' instruction at offset 46_0

        def load_macros--- This code section failed: ---

 L. 115         0  LOAD_STR                 'Software\\Microsoft\\VisualStudio\\%0.1f'
                2  LOAD_FAST                'version'
                4  BINARY_MODULO    
                6  STORE_FAST               'vsbase'

 L. 116         8  LOAD_FAST                'self'
               10  LOAD_METHOD              set_macro
               12  LOAD_STR                 'VCInstallDir'
               14  LOAD_FAST                'vsbase'
               16  LOAD_STR                 '\\Setup\\VC'
               18  BINARY_ADD       
               20  LOAD_STR                 'productdir'
               22  CALL_METHOD_3         3  ''
               24  POP_TOP          

 L. 117        26  LOAD_FAST                'self'
               28  LOAD_METHOD              set_macro
               30  LOAD_STR                 'VSInstallDir'
               32  LOAD_FAST                'vsbase'
               34  LOAD_STR                 '\\Setup\\VS'
               36  BINARY_ADD       
               38  LOAD_STR                 'productdir'
               40  CALL_METHOD_3         3  ''
               42  POP_TOP          

 L. 118        44  LOAD_STR                 'Software\\Microsoft\\.NETFramework'
               46  STORE_FAST               'net'

 L. 119        48  LOAD_FAST                'self'
               50  LOAD_METHOD              set_macro
               52  LOAD_STR                 'FrameworkDir'
               54  LOAD_FAST                'net'
               56  LOAD_STR                 'installroot'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 120        62  SETUP_FINALLY       106  'to 106'

 L. 121        64  LOAD_FAST                'version'
               66  LOAD_CONST               7.0
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    88  'to 88'

 L. 122        72  LOAD_FAST                'self'
               74  LOAD_METHOD              set_macro
               76  LOAD_STR                 'FrameworkSDKDir'
               78  LOAD_FAST                'net'
               80  LOAD_STR                 'sdkinstallrootv1.1'
               82  CALL_METHOD_3         3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        102  'to 102'
             88_0  COME_FROM            70  '70'

 L. 124        88  LOAD_FAST                'self'
               90  LOAD_METHOD              set_macro
               92  LOAD_STR                 'FrameworkSDKDir'
               94  LOAD_FAST                'net'
               96  LOAD_STR                 'sdkinstallroot'
               98  CALL_METHOD_3         3  ''
              100  POP_TOP          
            102_0  COME_FROM            86  '86'
              102  POP_BLOCK        
              104  JUMP_FORWARD        148  'to 148'
            106_0  COME_FROM_FINALLY    62  '62'

 L. 125       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   146  'to 146'
              114  POP_TOP          
              116  STORE_FAST               'exc'
              118  POP_TOP          
              120  SETUP_FINALLY       134  'to 134'

 L. 126       122  LOAD_GLOBAL              DistutilsPlatformError

 L. 127       124  LOAD_STR                 'Python was built with Visual Studio 2003;\nextensions must be built with a compiler than can generate compatible binaries.\nVisual Studio 2003 was not found on this system. If you have Cygwin installed,\nyou can try compiling with MingW32, by passing "-c mingw32" to setup.py.'

 L. 126       126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_FINALLY   120  '120'
              134  LOAD_CONST               None
              136  STORE_FAST               'exc'
              138  DELETE_FAST              'exc'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           112  '112'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           104  '104'

 L. 132       148  LOAD_STR                 'Software\\Microsoft\\NET Framework Setup\\Product'
              150  STORE_FAST               'p'

 L. 133       152  LOAD_GLOBAL              HKEYS
              154  GET_ITER         
            156_0  COME_FROM           242  '242'
            156_1  COME_FROM           192  '192'
              156  FOR_ITER            244  'to 244'
              158  STORE_FAST               'base'

 L. 134       160  SETUP_FINALLY       176  'to 176'

 L. 135       162  LOAD_GLOBAL              RegOpenKeyEx
              164  LOAD_FAST                'base'
              166  LOAD_FAST                'p'
              168  CALL_FUNCTION_2       2  ''
              170  STORE_FAST               'h'
              172  POP_BLOCK        
              174  JUMP_FORWARD        200  'to 200'
            176_0  COME_FROM_FINALLY   160  '160'

 L. 136       176  DUP_TOP          
              178  LOAD_GLOBAL              RegError
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   198  'to 198'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 137       190  POP_EXCEPT       
              192  JUMP_BACK           156  'to 156'
              194  POP_EXCEPT       
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           182  '182'
              198  END_FINALLY      
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           174  '174'

 L. 138       200  LOAD_GLOBAL              RegEnumKey
              202  LOAD_FAST                'h'
              204  LOAD_CONST               0
              206  CALL_FUNCTION_2       2  ''
              208  STORE_FAST               'key'

 L. 139       210  LOAD_GLOBAL              read_values
              212  LOAD_FAST                'base'
              214  LOAD_STR                 '%s\\%s'
              216  LOAD_FAST                'p'
              218  LOAD_FAST                'key'
              220  BUILD_TUPLE_2         2 
              222  BINARY_MODULO    
              224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'd'

 L. 140       228  LOAD_FAST                'd'
              230  LOAD_STR                 'version'
              232  BINARY_SUBSCR    
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                macros
              238  LOAD_STR                 '$(FrameworkVersion)'
              240  STORE_SUBSCR     
              242  JUMP_BACK           156  'to 156'
            244_0  COME_FROM           156  '156'

Parse error at or near `COME_FROM' instruction at offset 198_0

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


    def get_build_architecture():
        """Return the processor architecture.

    Possible results are "Intel" or "AMD64".
    """
        prefix = ' bit ('
        i = sys.version.find(prefix)
        if i == -1:
            return 'Intel'
        j = sys.version.find(')', i)
        return sys.version[i + len(prefix):j]


    def normalize_and_reduce_paths(paths):
        """Return a list of normalized paths with duplicates removed.

    The current order of paths is maintained.
    """
        reduced_paths = []
        for p in paths:
            np = os.path.normpath(p)
            if np not in reduced_paths:
                reduced_paths.append(np)
        else:
            return reduced_paths


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
            self._MSVCCompiler__version = get_build_version()
            self._MSVCCompiler__arch = get_build_architecture()
            if self._MSVCCompiler__arch == 'Intel':
                if self._MSVCCompiler__version >= 7:
                    self._MSVCCompiler__root = 'Software\\Microsoft\\VisualStudio'
                    self._MSVCCompiler__macros = MacroExpander(self._MSVCCompiler__version)
                else:
                    self._MSVCCompiler__root = 'Software\\Microsoft\\Devstudio'
                self._MSVCCompiler__product = 'Visual Studio version %s' % self._MSVCCompiler__version
            else:
                self._MSVCCompiler__product = 'Microsoft SDK compiler %s' % (self._MSVCCompiler__version + 6)
            self.initialized = False

        def initialize(self):
            self._MSVCCompiler__paths = []
            if 'DISTUTILS_USE_SDK' in os.environ and 'MSSdk' in os.environ and self.find_exe('cl.exe'):
                self.cc = 'cl.exe'
                self.linker = 'link.exe'
                self.lib = 'lib.exe'
                self.rc = 'rc.exe'
                self.mc = 'mc.exe'
            else:
                self._MSVCCompiler__paths = self.get_msvc_paths('path')
                if len(self._MSVCCompiler__paths) == 0:
                    raise DistutilsPlatformError("Python was built with %s, and extensions need to be built with the same version of the compiler, but it isn't installed." % self._MSVCCompiler__product)
                self.cc = self.find_exe('cl.exe')
                self.linker = self.find_exe('link.exe')
                self.lib = self.find_exe('lib.exe')
                self.rc = self.find_exe('rc.exe')
                self.mc = self.find_exe('mc.exe')
                self.set_path_env_var('lib')
                self.set_path_env_var('include')
            try:
                for p in os.environ['path'].split(';'):
                    self._MSVCCompiler__paths.append(p)

            except KeyError:
                pass
            else:
                self._MSVCCompiler__paths = normalize_and_reduce_paths(self._MSVCCompiler__paths)
                os.environ['path'] = ';'.join(self._MSVCCompiler__paths)
                self.preprocess_options = None
                if self._MSVCCompiler__arch == 'Intel':
                    self.compile_options = [
                     '/nologo', '/Ox', '/MD', '/W3', '/GX',
                     '/DNDEBUG']
                    self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3', '/GX',
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
                else:
                    self.ldflags_shared_debug = ['/DLL', '/nologo', '/INCREMENTAL:no', '/pdb:None', '/DEBUG']
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
                else:
                    if ext in self._mc_extensions:
                        obj_names.append(os.path.join(output_dir, base + self.res_extension))
                    else:
                        obj_names.append(os.path.join(output_dir, base + self.obj_extension))
            else:
                return obj_names

        def compile--- This code section failed: ---

 L. 347         0  LOAD_FAST                'self'
                2  LOAD_ATTR                initialized
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 348         6  LOAD_FAST                'self'
                8  LOAD_METHOD              initialize
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          
             14_0  COME_FROM             4  '4'

 L. 349        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _setup_compile
               18  LOAD_FAST                'output_dir'
               20  LOAD_FAST                'macros'
               22  LOAD_FAST                'include_dirs'

 L. 350        24  LOAD_FAST                'sources'

 L. 350        26  LOAD_FAST                'depends'

 L. 350        28  LOAD_FAST                'extra_postargs'

 L. 349        30  CALL_METHOD_6         6  ''
               32  STORE_FAST               'compile_info'

 L. 351        34  LOAD_FAST                'compile_info'
               36  UNPACK_SEQUENCE_5     5 
               38  STORE_FAST               'macros'
               40  STORE_FAST               'objects'
               42  STORE_FAST               'extra_postargs'
               44  STORE_FAST               'pp_opts'
               46  STORE_FAST               'build'

 L. 353        48  LOAD_FAST                'extra_preargs'
               50  JUMP_IF_TRUE_OR_POP    54  'to 54'
               52  BUILD_LIST_0          0 
             54_0  COME_FROM            50  '50'
               54  STORE_FAST               'compile_opts'

 L. 354        56  LOAD_FAST                'compile_opts'
               58  LOAD_METHOD              append
               60  LOAD_STR                 '/c'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 355        66  LOAD_FAST                'debug'
               68  POP_JUMP_IF_FALSE    84  'to 84'

 L. 356        70  LOAD_FAST                'compile_opts'
               72  LOAD_METHOD              extend
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                compile_options_debug
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM            68  '68'

 L. 358        84  LOAD_FAST                'compile_opts'
               86  LOAD_METHOD              extend
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                compile_options
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            82  '82'

 L. 360        96  LOAD_FAST                'objects'
               98  GET_ITER         
            100_0  COME_FROM           618  '618'
            100_1  COME_FROM           614  '614'
            100_2  COME_FROM           572  '572'
            100_3  COME_FROM           506  '506'
            100_4  COME_FROM           502  '502'
            100_5  COME_FROM           460  '460'
            100_6  COME_FROM           312  '312'
            100_7  COME_FROM           308  '308'
            100_8  COME_FROM           266  '266'
            100_9  COME_FROM           140  '140'
          100_102  FOR_ITER            620  'to 620'
              104  STORE_FAST               'obj'

 L. 361       106  SETUP_FINALLY       124  'to 124'

 L. 362       108  LOAD_FAST                'build'
              110  LOAD_FAST                'obj'
              112  BINARY_SUBSCR    
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'src'
              118  STORE_FAST               'ext'
              120  POP_BLOCK        
              122  JUMP_FORWARD        148  'to 148'
            124_0  COME_FROM_FINALLY   106  '106'

 L. 363       124  DUP_TOP          
              126  LOAD_GLOBAL              KeyError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   146  'to 146'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 364       138  POP_EXCEPT       
              140  JUMP_BACK           100  'to 100'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           130  '130'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           122  '122'

 L. 365       148  LOAD_FAST                'debug'
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 369       152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              abspath
              158  LOAD_FAST                'src'
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'src'
            164_0  COME_FROM           150  '150'

 L. 371       164  LOAD_FAST                'ext'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _c_extensions
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   186  'to 186'

 L. 372       174  LOAD_STR                 '/Tc'
              176  LOAD_FAST                'src'
              178  BINARY_ADD       
              180  STORE_FAST               'input_opt'
          182_184  JUMP_FORWARD        526  'to 526'
            186_0  COME_FROM           172  '172'

 L. 373       186  LOAD_FAST                'ext'
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                _cpp_extensions
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L. 374       196  LOAD_STR                 '/Tp'
              198  LOAD_FAST                'src'
              200  BINARY_ADD       
              202  STORE_FAST               'input_opt'
          204_206  JUMP_FORWARD        526  'to 526'
            208_0  COME_FROM           194  '194'

 L. 375       208  LOAD_FAST                'ext'
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                _rc_extensions
              214  COMPARE_OP               in
          216_218  POP_JUMP_IF_FALSE   316  'to 316'

 L. 377       220  LOAD_FAST                'src'
              222  STORE_FAST               'input_opt'

 L. 378       224  LOAD_STR                 '/fo'
              226  LOAD_FAST                'obj'
              228  BINARY_ADD       
              230  STORE_FAST               'output_opt'

 L. 379       232  SETUP_FINALLY       268  'to 268'

 L. 380       234  LOAD_FAST                'self'
              236  LOAD_METHOD              spawn
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                rc
              242  BUILD_LIST_1          1 
              244  LOAD_FAST                'pp_opts'
              246  BINARY_ADD       

 L. 381       248  LOAD_FAST                'output_opt'
              250  BUILD_LIST_1          1 

 L. 380       252  BINARY_ADD       

 L. 381       254  LOAD_FAST                'input_opt'
              256  BUILD_LIST_1          1 

 L. 380       258  BINARY_ADD       
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
              264  POP_BLOCK        
              266  JUMP_BACK           100  'to 100'
            268_0  COME_FROM_FINALLY   232  '232'

 L. 382       268  DUP_TOP          
              270  LOAD_GLOBAL              DistutilsExecError
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   310  'to 310'
              278  POP_TOP          
              280  STORE_FAST               'msg'
              282  POP_TOP          
              284  SETUP_FINALLY       298  'to 298'

 L. 383       286  LOAD_GLOBAL              CompileError
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

 L. 384       312  JUMP_BACK           100  'to 100'
              314  JUMP_FORWARD        526  'to 526'
            316_0  COME_FROM           216  '216'

 L. 385       316  LOAD_FAST                'ext'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                _mc_extensions
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   510  'to 510'

 L. 397       328  LOAD_GLOBAL              os
              330  LOAD_ATTR                path
              332  LOAD_METHOD              dirname
              334  LOAD_FAST                'src'
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'h_dir'

 L. 398       340  LOAD_GLOBAL              os
              342  LOAD_ATTR                path
              344  LOAD_METHOD              dirname
              346  LOAD_FAST                'obj'
              348  CALL_METHOD_1         1  ''
              350  STORE_FAST               'rc_dir'

 L. 399       352  SETUP_FINALLY       462  'to 462'

 L. 401       354  LOAD_FAST                'self'
              356  LOAD_METHOD              spawn
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                mc
              362  BUILD_LIST_1          1 

 L. 402       364  LOAD_STR                 '-h'
              366  LOAD_FAST                'h_dir'
              368  LOAD_STR                 '-r'
              370  LOAD_FAST                'rc_dir'
              372  BUILD_LIST_4          4 

 L. 401       374  BINARY_ADD       

 L. 402       376  LOAD_FAST                'src'
              378  BUILD_LIST_1          1 

 L. 401       380  BINARY_ADD       
              382  CALL_METHOD_1         1  ''
              384  POP_TOP          

 L. 403       386  LOAD_GLOBAL              os
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

 L. 404       410  LOAD_GLOBAL              os
              412  LOAD_ATTR                path
              414  LOAD_METHOD              join
              416  LOAD_FAST                'rc_dir'
              418  LOAD_FAST                'base'
              420  LOAD_STR                 '.rc'
              422  BINARY_ADD       
              424  CALL_METHOD_2         2  ''
              426  STORE_FAST               'rc_file'

 L. 406       428  LOAD_FAST                'self'
              430  LOAD_METHOD              spawn
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                rc
              436  BUILD_LIST_1          1 

 L. 407       438  LOAD_STR                 '/fo'
              440  LOAD_FAST                'obj'
              442  BINARY_ADD       
              444  BUILD_LIST_1          1 

 L. 406       446  BINARY_ADD       

 L. 407       448  LOAD_FAST                'rc_file'
              450  BUILD_LIST_1          1 

 L. 406       452  BINARY_ADD       
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
              458  POP_BLOCK        
              460  JUMP_BACK           100  'to 100'
            462_0  COME_FROM_FINALLY   352  '352'

 L. 409       462  DUP_TOP          
              464  LOAD_GLOBAL              DistutilsExecError
              466  COMPARE_OP               exception-match
          468_470  POP_JUMP_IF_FALSE   504  'to 504'
              472  POP_TOP          
              474  STORE_FAST               'msg'
              476  POP_TOP          
              478  SETUP_FINALLY       492  'to 492'

 L. 410       480  LOAD_GLOBAL              CompileError
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

 L. 411       506  JUMP_BACK           100  'to 100'
              508  JUMP_FORWARD        526  'to 526'
            510_0  COME_FROM           324  '324'

 L. 414       510  LOAD_GLOBAL              CompileError
              512  LOAD_STR                 "Don't know how to compile %s to %s"

 L. 415       514  LOAD_FAST                'src'
              516  LOAD_FAST                'obj'
              518  BUILD_TUPLE_2         2 

 L. 414       520  BINARY_MODULO    
              522  CALL_FUNCTION_1       1  ''
              524  RAISE_VARARGS_1       1  'exception instance'
            526_0  COME_FROM           508  '508'
            526_1  COME_FROM           314  '314'
            526_2  COME_FROM           204  '204'
            526_3  COME_FROM           182  '182'

 L. 417       526  LOAD_STR                 '/Fo'
              528  LOAD_FAST                'obj'
              530  BINARY_ADD       
              532  STORE_FAST               'output_opt'

 L. 418       534  SETUP_FINALLY       574  'to 574'

 L. 419       536  LOAD_FAST                'self'
              538  LOAD_METHOD              spawn
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                cc
              544  BUILD_LIST_1          1 
              546  LOAD_FAST                'compile_opts'
              548  BINARY_ADD       
              550  LOAD_FAST                'pp_opts'
              552  BINARY_ADD       

 L. 420       554  LOAD_FAST                'input_opt'
              556  LOAD_FAST                'output_opt'
              558  BUILD_LIST_2          2 

 L. 419       560  BINARY_ADD       

 L. 421       562  LOAD_FAST                'extra_postargs'

 L. 419       564  BINARY_ADD       
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
              570  POP_BLOCK        
              572  JUMP_BACK           100  'to 100'
            574_0  COME_FROM_FINALLY   534  '534'

 L. 422       574  DUP_TOP          
              576  LOAD_GLOBAL              DistutilsExecError
              578  COMPARE_OP               exception-match
          580_582  POP_JUMP_IF_FALSE   616  'to 616'
              584  POP_TOP          
              586  STORE_FAST               'msg'
              588  POP_TOP          
              590  SETUP_FINALLY       604  'to 604'

 L. 423       592  LOAD_GLOBAL              CompileError
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
            620_0  COME_FROM           100  '100'

 L. 425       620  LOAD_FAST                'objects'
              622  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 146_0

        def create_static_lib(self, objects, output_libname, output_dir=None, debug=0, target_lang=None):
            if not self.initialized:
                self.initialize()
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
            objects, output_dir = self._fix_object_args(objects, output_dir)
            fixed_args = self._fix_lib_argslibrarieslibrary_dirsruntime_library_dirs
            libraries, library_dirs, runtime_library_dirs = fixed_args
            if runtime_library_dirs:
                self.warn("I don't know what to do with 'runtime_library_dirs': " + str(runtime_library_dirs))
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
                    if export_symbols is not None:
                        dll_name, dll_ext = os.path.splitext(os.path.basename(output_filename))
                        implib_file = os.path.join(os.path.dirname(objects[0]), self.library_filename(dll_name))
                        ld_args.append('/IMPLIB:' + implib_file)
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
                log.debug('skipping %s (up-to-date)', output_filename)

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
            else:
                for p in os.environ['Path'].split(';'):
                    fn = os.path.join(os.path.abspath(p), exe)
                    if os.path.isfile(fn):
                        return fn
                else:
                    return exe

        def get_msvc_paths--- This code section failed: ---

 L. 593         0  LOAD_GLOBAL              _can_read_reg
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 594         4  BUILD_LIST_0          0 
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 596         8  LOAD_FAST                'path'
               10  LOAD_STR                 ' dirs'
               12  BINARY_ADD       
               14  STORE_FAST               'path'

 L. 597        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _MSVCCompiler__version
               20  LOAD_CONST               7
               22  COMPARE_OP               >=
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 598        26  LOAD_STR                 '%s\\%0.1f\\VC\\VC_OBJECTS_PLATFORM_INFO\\Win32\\Directories'

 L. 599        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _MSVCCompiler__root
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _MSVCCompiler__version
               36  BUILD_TUPLE_2         2 

 L. 598        38  BINARY_MODULO    
               40  STORE_FAST               'key'
               42  JUMP_FORWARD         58  'to 58'
             44_0  COME_FROM            24  '24'

 L. 601        44  LOAD_STR                 '%s\\6.0\\Build System\\Components\\Platforms\\Win32 (%s)\\Directories'

 L. 602        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _MSVCCompiler__root
               50  LOAD_FAST                'platform'
               52  BUILD_TUPLE_2         2 

 L. 601        54  BINARY_MODULO    
               56  STORE_FAST               'key'
             58_0  COME_FROM            42  '42'

 L. 604        58  LOAD_GLOBAL              HKEYS
               60  GET_ITER         
             62_0  COME_FROM           134  '134'
             62_1  COME_FROM            78  '78'
               62  FOR_ITER            136  'to 136'
               64  STORE_FAST               'base'

 L. 605        66  LOAD_GLOBAL              read_values
               68  LOAD_FAST                'base'
               70  LOAD_FAST                'key'
               72  CALL_FUNCTION_2       2  ''
               74  STORE_FAST               'd'

 L. 606        76  LOAD_FAST                'd'
               78  POP_JUMP_IF_FALSE_BACK    62  'to 62'

 L. 607        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _MSVCCompiler__version
               84  LOAD_CONST               7
               86  COMPARE_OP               >=
               88  POP_JUMP_IF_FALSE   116  'to 116'

 L. 608        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _MSVCCompiler__macros
               94  LOAD_METHOD              sub
               96  LOAD_FAST                'd'
               98  LOAD_FAST                'path'
              100  BINARY_SUBSCR    
              102  CALL_METHOD_1         1  ''
              104  LOAD_METHOD              split
              106  LOAD_STR                 ';'
              108  CALL_METHOD_1         1  ''
              110  ROT_TWO          
              112  POP_TOP          
              114  RETURN_VALUE     
            116_0  COME_FROM            88  '88'

 L. 610       116  LOAD_FAST                'd'
              118  LOAD_FAST                'path'
              120  BINARY_SUBSCR    
              122  LOAD_METHOD              split
              124  LOAD_STR                 ';'
              126  CALL_METHOD_1         1  ''
              128  ROT_TWO          
              130  POP_TOP          
              132  RETURN_VALUE     
              134  JUMP_BACK            62  'to 62'
            136_0  COME_FROM            62  '62'

 L. 613       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _MSVCCompiler__version
              140  LOAD_CONST               6
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   190  'to 190'

 L. 614       146  LOAD_GLOBAL              HKEYS
              148  GET_ITER         
            150_0  COME_FROM           188  '188'
            150_1  COME_FROM           172  '172'
              150  FOR_ITER            190  'to 190'
              152  STORE_FAST               'base'

 L. 615       154  LOAD_GLOBAL              read_values
              156  LOAD_FAST                'base'
              158  LOAD_STR                 '%s\\6.0'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _MSVCCompiler__root
              164  BINARY_MODULO    
              166  CALL_FUNCTION_2       2  ''
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE_BACK   150  'to 150'

 L. 616       174  LOAD_FAST                'self'
              176  LOAD_METHOD              warn
              178  LOAD_STR                 'It seems you have Visual Studio 6 installed, but the expected registry settings are not present.\nYou must at least run the Visual Studio GUI once so that these entries are created.'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 620       184  POP_TOP          
              186  BREAK_LOOP          190  'to 190'
              188  JUMP_BACK           150  'to 150'
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           150  '150'
            190_2  COME_FROM           144  '144'

 L. 621       190  BUILD_LIST_0          0 
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 192

        def set_path_env_var(self, name):
            """Set environment variable 'name' to an MSVC path type value.

        This is equivalent to a SET command prior to execution of spawned
        commands.
        """
            if name == 'lib':
                p = self.get_msvc_paths('library')
            else:
                p = self.get_msvc_paths(name)
            if p:
                os.environ[name] = ';'.join(p)


    if get_build_version() >= 8.0:
        log.debug('Importing new compiler from distutils.msvc9compiler')
        OldMSVCCompiler = MSVCCompiler
        from distutils.msvc9compiler import MSVCCompiler
        from distutils.msvc9compiler import MacroExpander