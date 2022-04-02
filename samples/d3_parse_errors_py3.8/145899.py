# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\msvc.py
"""
Improved support for Microsoft Visual C++ compilers.

Known supported compilers:
--------------------------
Microsoft Visual C++ 9.0:
    Microsoft Visual C++ Compiler for Python 2.7 (x86, amd64)
    Microsoft Windows SDK 6.1 (x86, x64, ia64)
    Microsoft Windows SDK 7.0 (x86, x64, ia64)

Microsoft Visual C++ 10.0:
    Microsoft Windows SDK 7.1 (x86, x64, ia64)

Microsoft Visual C++ 14.X:
    Microsoft Visual C++ Build Tools 2015 (x86, x64, arm)
    Microsoft Visual Studio Build Tools 2017 (x86, x64, arm, arm64)
    Microsoft Visual Studio Build Tools 2019 (x86, x64, arm, arm64)

This may also support compilers shipped with compatible Visual Studio versions.
"""
import json
from io import open
from os import listdir, pathsep
from os.path import join, isfile, isdir, dirname
import sys, platform, itertools, subprocess, distutils.errors
from setuptools.extern.packaging.version import LegacyVersion
from setuptools.extern.six.moves import filterfalse
from .monkey import get_unpatched
if platform.system() == 'Windows':
    from setuptools.extern.six.moves import winreg
    from os import environ
else:

    class winreg:
        HKEY_USERS = None
        HKEY_CURRENT_USER = None
        HKEY_LOCAL_MACHINE = None
        HKEY_CLASSES_ROOT = None


    environ = dict()
_msvc9_suppress_errors = (
 ImportError,
 distutils.errors.DistutilsPlatformError)
try:
    from distutils.msvc9compiler import Reg
except _msvc9_suppress_errors:
    pass
else:

    def msvc9_find_vcvarsall(version):
        """
    Patched "distutils.msvc9compiler.find_vcvarsall" to use the standalone
    compiler build for Python
    (VCForPython / Microsoft Visual C++ Compiler for Python 2.7).

    Fall back to original behavior when the standalone compiler is not
    available.

    Redirect the path of "vcvarsall.bat".

    Parameters
    ----------
    version: float
        Required Microsoft Visual C++ version.

    Return
    ------
    str
        vcvarsall.bat path
    """
        vc_base = 'Software\\%sMicrosoft\\DevDiv\\VCForPython\\%0.1f'
        key = vc_base % ('', version)
        try:
            productdir = Reg.get_value(key, 'installdir')
        except KeyError:
            try:
                key = vc_base % ('Wow6432Node\\', version)
                productdir = Reg.get_value(key, 'installdir')
            except KeyError:
                productdir = None

        else:
            if productdir:
                vcvarsall = join(productdir, 'vcvarsall.bat')
                if isfile(vcvarsall):
                    return vcvarsall
            return get_unpatched(msvc9_find_vcvarsall)(version)


    def msvc9_query_vcvarsall--- This code section failed: ---

 L. 128         0  SETUP_FINALLY        30  'to 30'

 L. 129         2  LOAD_GLOBAL              get_unpatched
                4  LOAD_GLOBAL              msvc9_query_vcvarsall
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'orig'

 L. 130        10  LOAD_FAST                'orig'
               12  LOAD_FAST                'ver'
               14  LOAD_FAST                'arch'
               16  BUILD_TUPLE_2         2 
               18  LOAD_FAST                'args'
               20  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               22  LOAD_FAST                'kwargs'
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L. 131        30  DUP_TOP          
               32  LOAD_GLOBAL              distutils
               34  LOAD_ATTR                errors
               36  LOAD_ATTR                DistutilsPlatformError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 133        48  POP_EXCEPT       
               50  JUMP_FORWARD         72  'to 72'
             52_0  COME_FROM            40  '40'

 L. 134        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    70  'to 70'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 136        66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            58  '58'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            50  '50'

 L. 139        72  SETUP_FINALLY        90  'to 90'

 L. 140        74  LOAD_GLOBAL              EnvironmentInfo
               76  LOAD_FAST                'arch'
               78  LOAD_FAST                'ver'
               80  CALL_FUNCTION_2       2  ''
               82  LOAD_METHOD              return_env
               84  CALL_METHOD_0         0  ''
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    72  '72'

 L. 141        90  DUP_TOP          
               92  LOAD_GLOBAL              distutils
               94  LOAD_ATTR                errors
               96  LOAD_ATTR                DistutilsPlatformError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   140  'to 140'
              102  POP_TOP          
              104  STORE_FAST               'exc'
              106  POP_TOP          
              108  SETUP_FINALLY       128  'to 128'

 L. 142       110  LOAD_GLOBAL              _augment_exception
              112  LOAD_FAST                'exc'
              114  LOAD_FAST                'ver'
              116  LOAD_FAST                'arch'
              118  CALL_FUNCTION_3       3  ''
              120  POP_TOP          

 L. 143       122  RAISE_VARARGS_0       0  'reraise'
              124  POP_BLOCK        
              126  BEGIN_FINALLY    
            128_0  COME_FROM_FINALLY   108  '108'
              128  LOAD_CONST               None
              130  STORE_FAST               'exc'
              132  DELETE_FAST              'exc'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           100  '100'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'

Parse error at or near `COME_FROM' instruction at offset 52_0


    def _msvc14_find_vc2015--- This code section failed: ---

 L. 148         0  SETUP_FINALLY        32  'to 32'

 L. 149         2  LOAD_GLOBAL              winreg
                4  LOAD_METHOD              OpenKey

 L. 150         6  LOAD_GLOBAL              winreg
                8  LOAD_ATTR                HKEY_LOCAL_MACHINE

 L. 151        10  LOAD_STR                 'Software\\Microsoft\\VisualStudio\\SxS\\VC7'

 L. 152        12  LOAD_CONST               0

 L. 153        14  LOAD_GLOBAL              winreg
               16  LOAD_ATTR                KEY_READ
               18  LOAD_GLOBAL              winreg
               20  LOAD_ATTR                KEY_WOW64_32KEY
               22  BINARY_OR        

 L. 149        24  CALL_METHOD_4         4  ''
               26  STORE_FAST               'key'
               28  POP_BLOCK        
               30  JUMP_FORWARD         54  'to 54'
             32_0  COME_FROM_FINALLY     0  '0'

 L. 155        32  DUP_TOP          
               34  LOAD_GLOBAL              OSError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 156        46  POP_EXCEPT       
               48  LOAD_CONST               (None, None)
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      
             54_0  COME_FROM            30  '30'

 L. 158        54  LOAD_CONST               0
               56  STORE_FAST               'best_version'

 L. 159        58  LOAD_CONST               None
               60  STORE_FAST               'best_dir'

 L. 160        62  LOAD_FAST                'key'
               64  SETUP_WITH          230  'to 230'
               66  POP_TOP          

 L. 161        68  LOAD_GLOBAL              itertools
               70  LOAD_METHOD              count
               72  CALL_METHOD_0         0  ''
               74  GET_ITER         
             76_0  COME_FROM           224  '224'
             76_1  COME_FROM           212  '212'
             76_2  COME_FROM           204  '204'
             76_3  COME_FROM           190  '190'
             76_4  COME_FROM           150  '150'
             76_5  COME_FROM           142  '142'
             76_6  COME_FROM           132  '132'
               76  FOR_ITER            226  'to 226'
               78  STORE_FAST               'i'

 L. 162        80  SETUP_FINALLY       104  'to 104'

 L. 163        82  LOAD_GLOBAL              winreg
               84  LOAD_METHOD              EnumValue
               86  LOAD_FAST                'key'
               88  LOAD_FAST                'i'
               90  CALL_METHOD_2         2  ''
               92  UNPACK_SEQUENCE_3     3 
               94  STORE_FAST               'v'
               96  STORE_FAST               'vc_dir'
               98  STORE_FAST               'vt'
              100  POP_BLOCK        
              102  JUMP_FORWARD        130  'to 130'
            104_0  COME_FROM_FINALLY    80  '80'

 L. 164       104  DUP_TOP          
              106  LOAD_GLOBAL              OSError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   128  'to 128'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 165       118  POP_EXCEPT       
              120  POP_TOP          
              122  JUMP_FORWARD        226  'to 226'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           110  '110'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           102  '102'

 L. 166       130  LOAD_FAST                'v'
              132  POP_JUMP_IF_FALSE_BACK    76  'to 76'
              134  LOAD_FAST                'vt'
              136  LOAD_GLOBAL              winreg
              138  LOAD_ATTR                REG_SZ
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE_BACK    76  'to 76'
              144  LOAD_GLOBAL              isdir
              146  LOAD_FAST                'vc_dir'
              148  CALL_FUNCTION_1       1  ''
              150  POP_JUMP_IF_FALSE_BACK    76  'to 76'

 L. 167       152  SETUP_FINALLY       170  'to 170'

 L. 168       154  LOAD_GLOBAL              int
              156  LOAD_GLOBAL              float
              158  LOAD_FAST                'v'
              160  CALL_FUNCTION_1       1  ''
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'version'
              166  POP_BLOCK        
              168  JUMP_FORWARD        198  'to 198'
            170_0  COME_FROM_FINALLY   152  '152'

 L. 169       170  DUP_TOP          
              172  LOAD_GLOBAL              ValueError
              174  LOAD_GLOBAL              TypeError
              176  BUILD_TUPLE_2         2 
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   196  'to 196'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 170       188  POP_EXCEPT       
              190  JUMP_BACK            76  'to 76'
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           180  '180'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           168  '168'

 L. 171       198  LOAD_FAST                'version'
              200  LOAD_CONST               14
              202  COMPARE_OP               >=
              204  POP_JUMP_IF_FALSE_BACK    76  'to 76'
              206  LOAD_FAST                'version'
              208  LOAD_FAST                'best_version'
              210  COMPARE_OP               >
              212  POP_JUMP_IF_FALSE_BACK    76  'to 76'

 L. 172       214  LOAD_FAST                'version'
              216  LOAD_FAST                'vc_dir'
              218  ROT_TWO          
              220  STORE_FAST               'best_version'
              222  STORE_FAST               'best_dir'
              224  JUMP_BACK            76  'to 76'
            226_0  COME_FROM           122  '122'
            226_1  COME_FROM            76  '76'
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM_WITH       64  '64'
              230  WITH_CLEANUP_START
              232  WITH_CLEANUP_FINISH
              234  END_FINALLY      

 L. 173       236  LOAD_FAST                'best_version'
              238  LOAD_FAST                'best_dir'
              240  BUILD_TUPLE_2         2 
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 122


    def _msvc14_find_vc2017():
        """Python 3.8 "distutils/_msvccompiler.py" backport

    Returns "15, path" based on the result of invoking vswhere.exe
    If no install is found, returns "None, None"

    The version is returned to avoid unnecessarily changing the function
    result. It may be ignored when the path is not None.

    If vswhere.exe is not available, by definition, VS 2017 is not
    installed.
    """
        root = environ.get('ProgramFiles(x86)') or environ.get('ProgramFiles')
        if not root:
            return (None, None)
        try:
            path = subprocess.check_output([
             join(root, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe'),
             '-latest',
             '-prerelease',
             '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
             '-property', 'installationPath',
             '-products', '*']).decode(encoding='mbcs',
              errors='strict').strip()
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
            return (None, None)
        else:
            path = join(path, 'VC', 'Auxiliary', 'Build')
            if isdir(path):
                return (15, path)
            else:
                return (None, None)


    PLAT_SPEC_TO_RUNTIME = {'x86':'x86', 
     'x86_amd64':'x64', 
     'x86_arm':'arm', 
     'x86_arm64':'arm64'}

    def _msvc14_find_vcvarsall(plat_spec):
        """Python 3.8 "distutils/_msvccompiler.py" backport"""
        _, best_dir = _msvc14_find_vc2017()
        vcruntime = None
        if plat_spec in PLAT_SPEC_TO_RUNTIME:
            vcruntime_plat = PLAT_SPEC_TO_RUNTIME[plat_spec]
        else:
            vcruntime_plat = 'x64' if 'amd64' in plat_spec else 'x86'
        if best_dir:
            vcredist = join(best_dir, '..', '..', 'redist', 'MSVC', '**', vcruntime_plat, 'Microsoft.VC14*.CRT', 'vcruntime140.dll')
            try:
                import glob
                vcruntime = glob.glob(vcredist, recursive=True)[(-1)]
            except (ImportError, OSError, LookupError):
                vcruntime = None
            else:
                if not best_dir:
                    best_version, best_dir = _msvc14_find_vc2015()
                    if best_version:
                        vcruntime = join(best_dir, 'redist', vcruntime_plat, 'Microsoft.VC140.CRT', 'vcruntime140.dll')
                if not best_dir:
                    return (None, None)
                vcvarsall = join(best_dir, 'vcvarsall.bat')
                if not isfile(vcvarsall):
                    return (None, None)
                if not (vcruntime and isfile(vcruntime)):
                    vcruntime = None
            return (vcvarsall, vcruntime)


    def _msvc14_get_vc_env(plat_spec):
        """Python 3.8 "distutils/_msvccompiler.py" backport"""
        if 'DISTUTILS_USE_SDK' in environ:
            return {value:key.lower() for key, value in environ.items()}
        vcvarsall, vcruntime = _msvc14_find_vcvarsall(plat_spec)
        if not vcvarsall:
            raise distutils.errors.DistutilsPlatformError('Unable to find vcvarsall.bat')
        try:
            out = subprocess.check_output(('cmd /u /c "{}" {} && set'.format(vcvarsall, plat_spec)),
              stderr=(subprocess.STDOUT)).decode('utf-16le',
              errors='replace')
        except subprocess.CalledProcessError as exc:
            try:
                raise distutils.errors.DistutilsPlatformError('Error executing {}'.format(exc.cmd))
            finally:
                exc = None
                del exc

        else:
            env = {value:key.lower() for key, _, value in (line.partition('=') for line in out.splitlines()) if key if value if value}
            if vcruntime:
                env['py_vcruntime_redist'] = vcruntime
            else:
                return env


    def msvc14_get_vc_env(plat_spec):
        """
    Patched "distutils._msvccompiler._get_vc_env" for support extra
    Microsoft Visual C++ 14.X compilers.

    Set environment without use of "vcvarsall.bat".

    Parameters
    ----------
    plat_spec: str
        Target architecture.

    Return
    ------
    dict
        environment
    """
        try:
            return _msvc14_get_vc_env(plat_spec)
            except distutils.errors.DistutilsPlatformError as exc:
            try:
                _augment_exception(exc, 14.0)
                raise
            finally:
                exc = None
                del exc


    def msvc14_gen_lib_options(*args, **kwargs):
        """
    Patched "distutils._msvccompiler.gen_lib_options" for fix
    compatibility between "numpy.distutils" and "distutils._msvccompiler"
    (for Numpy < 1.11.2)
    """
        if 'numpy.distutils' in sys.modules:
            import numpy as np
            if LegacyVersion(np.__version__) < LegacyVersion('1.11.2'):
                return (np.distutils.ccompiler.gen_lib_options)(*args, **kwargs)
        return (get_unpatched(msvc14_gen_lib_options))(*args, **kwargs)


    def _augment_exception(exc, version, arch=''):
        """
    Add details to the exception message to help guide the user
    as to what action will resolve it.
    """
        message = exc.args[0]
        if 'vcvarsall' in message.lower() or ('visual c' in message.lower()):
            tmpl = 'Microsoft Visual C++ {version:0.1f} is required.'
            message = (tmpl.format)(**locals())
            msdownload = 'www.microsoft.com/download/details.aspx?id=%d'
            if version == 9.0:
                if arch.lower().find('ia64') > -1:
                    message += ' Get it with "Microsoft Windows SDK 7.0"'
                else:
                    message += ' Get it from http://aka.ms/vcpython27'
            elif version == 10.0:
                message += ' Get it with "Microsoft Windows SDK 7.1": '
                message += msdownload % 8279
            elif version >= 14.0:
                message += ' Get it with "Build Tools for Visual Studio": https://visualstudio.microsoft.com/downloads/'
        exc.args = (message,)


    class PlatformInfo:
        __doc__ = '\n    Current and Target Architectures information.\n\n    Parameters\n    ----------\n    arch: str\n        Target architecture.\n    '
        current_cpu = environ.get('processor_architecture', '').lower()

        def __init__(self, arch):
            self.arch = arch.lower().replace('x64', 'amd64')

        @property
        def target_cpu(self):
            """
        Return Target CPU architecture.

        Return
        ------
        str
            Target CPU
        """
            return self.arch[self.arch.find('_') + 1:]

        def target_is_x86(self):
            """
        Return True if target CPU is x86 32 bits..

        Return
        ------
        bool
            CPU is x86 32 bits
        """
            return self.target_cpu == 'x86'

        def current_is_x86(self):
            """
        Return True if current CPU is x86 32 bits..

        Return
        ------
        bool
            CPU is x86 32 bits
        """
            return self.current_cpu == 'x86'

        def current_dir(self, hidex86=False, x64=False):
            """
        Current platform specific subfolder.

        Parameters
        ----------
        hidex86: bool
            return '' and not '\x86' if architecture is x86.
        x64: bool
            return 'd' and not '\x07md64' if architecture is amd64.

        Return
        ------
        str
            subfolder: '        arget', or '' (see hidex86 parameter)
        """
            if self.current_cpu == 'x86':
                if hidex86:
                    return ''
            if self.current_cpu == 'amd64':
                if x64:
                    return '\\x64'
            return '\\%s' % self.current_cpu

        def target_dir(self, hidex86=False, x64=False):
            r"""
        Target platform specific subfolder.

        Parameters
        ----------
        hidex86: bool
            return '' and not '\x86' if architecture is x86.
        x64: bool
            return '\x64' and not '\amd64' if architecture is amd64.

        Return
        ------
        str
            subfolder: '\current', or '' (see hidex86 parameter)
        """
            if self.target_cpu == 'x86':
                if hidex86:
                    return ''
            if self.target_cpu == 'amd64':
                if x64:
                    return '\\x64'
            return '\\%s' % self.target_cpu

        def cross_dir(self, forcex86=False):
            r"""
        Cross platform specific subfolder.

        Parameters
        ----------
        forcex86: bool
            Use 'x86' as current architecture even if current architecture is
            not x86.

        Return
        ------
        str
            subfolder: '' if target architecture is current architecture,
            '\current_target' if not.
        """
            current = 'x86' if forcex86 else self.current_cpu
            if self.target_cpu == current:
                return ''
            return self.target_dir().replace('\\', '\\%s_' % current)


    class RegistryInfo:
        __doc__ = '\n    Microsoft Visual Studio related registry information.\n\n    Parameters\n    ----------\n    platform_info: PlatformInfo\n        "PlatformInfo" instance.\n    '
        HKEYS = (
         winreg.HKEY_USERS,
         winreg.HKEY_CURRENT_USER,
         winreg.HKEY_LOCAL_MACHINE,
         winreg.HKEY_CLASSES_ROOT)

        def __init__(self, platform_info):
            self.pi = platform_info

        @property
        def visualstudio(self):
            """
        Microsoft Visual Studio root registry key.

        Return
        ------
        str
            Registry key
        """
            return 'VisualStudio'

        @property
        def sxs(self):
            """
        Microsoft Visual Studio SxS registry key.

        Return
        ------
        str
            Registry key
        """
            return join(self.visualstudio, 'SxS')

        @property
        def vc(self):
            """
        Microsoft Visual C++ VC7 registry key.

        Return
        ------
        str
            Registry key
        """
            return join(self.sxs, 'VC7')

        @property
        def vs(self):
            """
        Microsoft Visual Studio VS7 registry key.

        Return
        ------
        str
            Registry key
        """
            return join(self.sxs, 'VS7')

        @property
        def vc_for_python(self):
            """
        Microsoft Visual C++ for Python registry key.

        Return
        ------
        str
            Registry key
        """
            return 'DevDiv\\VCForPython'

        @property
        def microsoft_sdk(self):
            """
        Microsoft SDK registry key.

        Return
        ------
        str
            Registry key
        """
            return 'Microsoft SDKs'

        @property
        def windows_sdk(self):
            """
        Microsoft Windows/Platform SDK registry key.

        Return
        ------
        str
            Registry key
        """
            return join(self.microsoft_sdk, 'Windows')

        @property
        def netfx_sdk(self):
            """
        Microsoft .NET Framework SDK registry key.

        Return
        ------
        str
            Registry key
        """
            return join(self.microsoft_sdk, 'NETFXSDK')

        @property
        def windows_kits_roots(self):
            """
        Microsoft Windows Kits Roots registry key.

        Return
        ------
        str
            Registry key
        """
            return 'Windows Kits\\Installed Roots'

        def microsoft(self, key, x86=False):
            """
        Return key in Microsoft software registry.

        Parameters
        ----------
        key: str
            Registry key path where look.
        x86: str
            Force x86 software registry.

        Return
        ------
        str
            Registry key
        """
            node64 = '' if (self.pi.current_is_x86() or x86) else 'Wow6432Node'
            return join('Software', node64, 'Microsoft', key)

        def lookup--- This code section failed: ---

 L. 644         0  LOAD_GLOBAL              winreg
                2  LOAD_ATTR                KEY_READ
                4  STORE_FAST               'key_read'

 L. 645         6  LOAD_GLOBAL              winreg
                8  LOAD_ATTR                OpenKey
               10  STORE_FAST               'openkey'

 L. 646        12  LOAD_FAST                'self'
               14  LOAD_ATTR                microsoft
               16  STORE_FAST               'ms'

 L. 647        18  LOAD_FAST                'self'
               20  LOAD_ATTR                HKEYS
               22  GET_ITER         
             24_0  COME_FROM           196  '196'
             24_1  COME_FROM           192  '192'
             24_2  COME_FROM           140  '140'
             24_3  COME_FROM           128  '128'
               24  FOR_ITER            198  'to 198'
               26  STORE_FAST               'hkey'

 L. 648        28  SETUP_FINALLY        52  'to 52'

 L. 649        30  LOAD_FAST                'openkey'
               32  LOAD_FAST                'hkey'
               34  LOAD_FAST                'ms'
               36  LOAD_FAST                'key'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               0
               42  LOAD_FAST                'key_read'
               44  CALL_FUNCTION_4       4  ''
               46  STORE_FAST               'bkey'
               48  POP_BLOCK        
               50  JUMP_FORWARD        148  'to 148'
             52_0  COME_FROM_FINALLY    28  '28'

 L. 650        52  DUP_TOP          
               54  LOAD_GLOBAL              OSError
               56  LOAD_GLOBAL              IOError
               58  BUILD_TUPLE_2         2 
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   146  'to 146'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 651        70  LOAD_FAST                'self'
               72  LOAD_ATTR                pi
               74  LOAD_METHOD              current_is_x86
               76  CALL_METHOD_0         0  ''
               78  POP_JUMP_IF_TRUE    138  'to 138'

 L. 652        80  SETUP_FINALLY       106  'to 106'

 L. 653        82  LOAD_FAST                'openkey'
               84  LOAD_FAST                'hkey'
               86  LOAD_FAST                'ms'
               88  LOAD_FAST                'key'
               90  LOAD_CONST               True
               92  CALL_FUNCTION_2       2  ''
               94  LOAD_CONST               0
               96  LOAD_FAST                'key_read'
               98  CALL_FUNCTION_4       4  ''
              100  STORE_FAST               'bkey'
              102  POP_BLOCK        
              104  JUMP_FORWARD        142  'to 142'
            106_0  COME_FROM_FINALLY    80  '80'

 L. 654       106  DUP_TOP          
              108  LOAD_GLOBAL              OSError
              110  LOAD_GLOBAL              IOError
              112  BUILD_TUPLE_2         2 
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   134  'to 134'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 655       124  POP_EXCEPT       
              126  POP_EXCEPT       
              128  JUMP_BACK            24  'to 24'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           116  '116'
              134  END_FINALLY      
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM            78  '78'

 L. 657       138  POP_EXCEPT       
              140  JUMP_BACK            24  'to 24'
            142_0  COME_FROM           136  '136'
            142_1  COME_FROM           132  '132'
            142_2  COME_FROM           104  '104'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            62  '62'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            50  '50'

 L. 658       148  SETUP_FINALLY       172  'to 172'

 L. 659       150  LOAD_GLOBAL              winreg
              152  LOAD_METHOD              QueryValueEx
              154  LOAD_FAST                'bkey'
              156  LOAD_FAST                'name'
              158  CALL_METHOD_2         2  ''
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  POP_BLOCK        
              166  ROT_TWO          
              168  POP_TOP          
              170  RETURN_VALUE     
            172_0  COME_FROM_FINALLY   148  '148'

 L. 660       172  DUP_TOP          
              174  LOAD_GLOBAL              OSError
              176  LOAD_GLOBAL              IOError
              178  BUILD_TUPLE_2         2 
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   194  'to 194'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 661       190  POP_EXCEPT       
              192  JUMP_BACK            24  'to 24'
            194_0  COME_FROM           182  '182'
              194  END_FINALLY      
              196  JUMP_BACK            24  'to 24'
            198_0  COME_FROM            24  '24'

Parse error at or near `END_FINALLY' instruction at offset 134


    class SystemInfo:
        __doc__ = '\n    Microsoft Windows and Visual Studio related system information.\n\n    Parameters\n    ----------\n    registry_info: RegistryInfo\n        "RegistryInfo" instance.\n    vc_ver: float\n        Required Microsoft Visual C++ version.\n    '
        WinDir = environ.get('WinDir', '')
        ProgramFiles = environ.get('ProgramFiles', '')
        ProgramFilesx86 = environ.get('ProgramFiles(x86)', ProgramFiles)

        def __init__(self, registry_info, vc_ver=None):
            self.ri = registry_info
            self.pi = self.ri.pi
            self.known_vs_paths = self.find_programdata_vs_vers()
            self.vs_ver = self.vc_ver = vc_ver or self._find_latest_available_vs_ver()

        def _find_latest_available_vs_ver(self):
            """
        Find the latest VC version

        Return
        ------
        float
            version
        """
            reg_vc_vers = self.find_reg_vs_vers()
            if not reg_vc_vers:
                if not self.known_vs_paths:
                    raise distutils.errors.DistutilsPlatformError('No Microsoft Visual C++ version found')
                vc_vers = set(reg_vc_vers)
                vc_vers.update(self.known_vs_paths)
                return sorted(vc_vers)[(-1)]

        def find_reg_vs_vers--- This code section failed: ---

 L. 720         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ri
                4  LOAD_ATTR                microsoft
                6  STORE_FAST               'ms'

 L. 721         8  LOAD_FAST                'self'
               10  LOAD_ATTR                ri
               12  LOAD_ATTR                vc
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                ri
               18  LOAD_ATTR                vc_for_python
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                ri
               24  LOAD_ATTR                vs
               26  BUILD_TUPLE_3         3 
               28  STORE_FAST               'vckeys'

 L. 722        30  BUILD_LIST_0          0 
               32  STORE_FAST               'vs_vers'

 L. 723        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ri
               38  LOAD_ATTR                HKEYS
               40  GET_ITER         
             42_0  COME_FROM           282  '282'
               42  FOR_ITER            284  'to 284'
               44  STORE_FAST               'hkey'

 L. 724        46  LOAD_FAST                'vckeys'
               48  GET_ITER         
             50_0  COME_FROM           280  '280'
             50_1  COME_FROM           102  '102'
               50  FOR_ITER            282  'to 282'
               52  STORE_FAST               'key'

 L. 725        54  SETUP_FINALLY        82  'to 82'

 L. 726        56  LOAD_GLOBAL              winreg
               58  LOAD_METHOD              OpenKey
               60  LOAD_FAST                'hkey'
               62  LOAD_FAST                'ms'
               64  LOAD_FAST                'key'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               0
               70  LOAD_GLOBAL              winreg
               72  LOAD_ATTR                KEY_READ
               74  CALL_METHOD_4         4  ''
               76  STORE_FAST               'bkey'
               78  POP_BLOCK        
               80  JUMP_FORWARD        110  'to 110'
             82_0  COME_FROM_FINALLY    54  '54'

 L. 727        82  DUP_TOP          
               84  LOAD_GLOBAL              OSError
               86  LOAD_GLOBAL              IOError
               88  BUILD_TUPLE_2         2 
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   108  'to 108'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 728       100  POP_EXCEPT       
              102  JUMP_BACK            50  'to 50'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            92  '92'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            80  '80'

 L. 729       110  LOAD_GLOBAL              winreg
              112  LOAD_METHOD              QueryInfoKey
              114  LOAD_FAST                'bkey'
              116  CALL_METHOD_1         1  ''
              118  UNPACK_SEQUENCE_3     3 
              120  STORE_FAST               'subkeys'
              122  STORE_FAST               'values'
              124  STORE_FAST               '_'

 L. 730       126  LOAD_GLOBAL              range
              128  LOAD_FAST                'values'
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
            134_0  COME_FROM           202  '202'
            134_1  COME_FROM           198  '198'
            134_2  COME_FROM           180  '180'
              134  FOR_ITER            204  'to 204'
              136  STORE_FAST               'i'

 L. 731       138  SETUP_FINALLY       182  'to 182'

 L. 732       140  LOAD_GLOBAL              float
              142  LOAD_GLOBAL              winreg
              144  LOAD_METHOD              EnumValue
              146  LOAD_FAST                'bkey'
              148  LOAD_FAST                'i'
              150  CALL_METHOD_2         2  ''
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'ver'

 L. 733       160  LOAD_FAST                'ver'
              162  LOAD_FAST                'vs_vers'
              164  COMPARE_OP               not-in
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 734       168  LOAD_FAST                'vs_vers'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'ver'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'
              178  POP_BLOCK        
              180  JUMP_BACK           134  'to 134'
            182_0  COME_FROM_FINALLY   138  '138'

 L. 735       182  DUP_TOP          
              184  LOAD_GLOBAL              ValueError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   200  'to 200'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 736       196  POP_EXCEPT       
              198  JUMP_BACK           134  'to 134'
            200_0  COME_FROM           188  '188'
              200  END_FINALLY      
              202  JUMP_BACK           134  'to 134'
            204_0  COME_FROM           134  '134'

 L. 737       204  LOAD_GLOBAL              range
              206  LOAD_FAST                'subkeys'
              208  CALL_FUNCTION_1       1  ''
              210  GET_ITER         
            212_0  COME_FROM           278  '278'
            212_1  COME_FROM           274  '274'
            212_2  COME_FROM           254  '254'
              212  FOR_ITER            280  'to 280'
              214  STORE_FAST               'i'

 L. 738       216  SETUP_FINALLY       256  'to 256'

 L. 739       218  LOAD_GLOBAL              float
              220  LOAD_GLOBAL              winreg
              222  LOAD_METHOD              EnumKey
              224  LOAD_FAST                'bkey'
              226  LOAD_FAST                'i'
              228  CALL_METHOD_2         2  ''
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'ver'

 L. 740       234  LOAD_FAST                'ver'
              236  LOAD_FAST                'vs_vers'
              238  COMPARE_OP               not-in
              240  POP_JUMP_IF_FALSE   252  'to 252'

 L. 741       242  LOAD_FAST                'vs_vers'
              244  LOAD_METHOD              append
              246  LOAD_FAST                'ver'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
            252_0  COME_FROM           240  '240'
              252  POP_BLOCK        
              254  JUMP_BACK           212  'to 212'
            256_0  COME_FROM_FINALLY   216  '216'

 L. 742       256  DUP_TOP          
              258  LOAD_GLOBAL              ValueError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   276  'to 276'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 743       272  POP_EXCEPT       
              274  JUMP_BACK           212  'to 212'
            276_0  COME_FROM           262  '262'
              276  END_FINALLY      
              278  JUMP_BACK           212  'to 212'
            280_0  COME_FROM           212  '212'
              280  JUMP_BACK            50  'to 50'
            282_0  COME_FROM            50  '50'
              282  JUMP_BACK            42  'to 42'
            284_0  COME_FROM            42  '42'

 L. 744       284  LOAD_GLOBAL              sorted
              286  LOAD_FAST                'vs_vers'
              288  CALL_FUNCTION_1       1  ''
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 108_0

        def find_programdata_vs_vers--- This code section failed: ---

 L. 756         0  BUILD_MAP_0           0 
                2  STORE_FAST               'vs_versions'

 L. 758         4  LOAD_STR                 'C:\\ProgramData\\Microsoft\\VisualStudio\\Packages\\_Instances'

 L. 757         6  STORE_FAST               'instances_dir'

 L. 760         8  SETUP_FINALLY        22  'to 22'

 L. 761        10  LOAD_GLOBAL              listdir
               12  LOAD_FAST                'instances_dir'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'hashed_names'
               18  POP_BLOCK        
               20  JUMP_FORWARD         50  'to 50'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 763        22  DUP_TOP          
               24  LOAD_GLOBAL              OSError
               26  LOAD_GLOBAL              IOError
               28  BUILD_TUPLE_2         2 
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    48  'to 48'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 765        40  LOAD_FAST                'vs_versions'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'
               48  END_FINALLY      
             50_0  COME_FROM            20  '20'

 L. 767        50  LOAD_FAST                'hashed_names'
               52  GET_ITER         
             54_0  COME_FROM           182  '182'
             54_1  COME_FROM           178  '178'
             54_2  COME_FROM           174  '174'
             54_3  COME_FROM           150  '150'
               54  FOR_ITER            184  'to 184'
               56  STORE_FAST               'name'

 L. 768        58  SETUP_FINALLY       152  'to 152'

 L. 770        60  LOAD_GLOBAL              join
               62  LOAD_FAST                'instances_dir'
               64  LOAD_FAST                'name'
               66  LOAD_STR                 'state.json'
               68  CALL_FUNCTION_3       3  ''
               70  STORE_FAST               'state_path'

 L. 771        72  LOAD_GLOBAL              open
               74  LOAD_FAST                'state_path'
               76  LOAD_STR                 'rt'
               78  LOAD_STR                 'utf-8'
               80  LOAD_CONST               ('encoding',)
               82  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               84  SETUP_WITH          102  'to 102'
               86  STORE_FAST               'state_file'

 L. 772        88  LOAD_GLOBAL              json
               90  LOAD_METHOD              load
               92  LOAD_FAST                'state_file'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'state'
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM_WITH       84  '84'
              102  WITH_CLEANUP_START
              104  WITH_CLEANUP_FINISH
              106  END_FINALLY      

 L. 773       108  LOAD_FAST                'state'
              110  LOAD_STR                 'installationPath'
              112  BINARY_SUBSCR    
              114  STORE_FAST               'vs_path'

 L. 776       116  LOAD_GLOBAL              listdir
              118  LOAD_GLOBAL              join
              120  LOAD_FAST                'vs_path'
              122  LOAD_STR                 'VC\\Tools\\MSVC'
              124  CALL_FUNCTION_2       2  ''
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          

 L. 780       130  LOAD_FAST                'vs_path'

 L. 779       132  LOAD_FAST                'vs_versions'
              134  LOAD_FAST                'self'
              136  LOAD_METHOD              _as_float_version

 L. 780       138  LOAD_FAST                'state'
              140  LOAD_STR                 'installationVersion'
              142  BINARY_SUBSCR    

 L. 779       144  CALL_METHOD_1         1  ''
              146  STORE_SUBSCR     
              148  POP_BLOCK        
              150  JUMP_BACK            54  'to 54'
            152_0  COME_FROM_FINALLY    58  '58'

 L. 782       152  DUP_TOP          
              154  LOAD_GLOBAL              OSError
              156  LOAD_GLOBAL              IOError
              158  LOAD_GLOBAL              KeyError
              160  BUILD_TUPLE_3         3 
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   180  'to 180'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L. 784       172  POP_EXCEPT       
              174  JUMP_BACK            54  'to 54'
              176  POP_EXCEPT       
              178  JUMP_BACK            54  'to 54'
            180_0  COME_FROM           164  '164'
              180  END_FINALLY      
              182  JUMP_BACK            54  'to 54'
            184_0  COME_FROM            54  '54'

 L. 786       184  LOAD_FAST                'vs_versions'
              186  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 178

        @staticmethod
        def _as_float_version(version):
            """
        Return a string version as a simplified float version (major.minor)

        Parameters
        ----------
        version: str
            Version.

        Return
        ------
        float
            version
        """
            return float('.'.join(version.split('.')[:2]))

        @property
        def VSInstallDir(self):
            """
        Microsoft Visual Studio directory.

        Return
        ------
        str
            path
        """
            default = join(self.ProgramFilesx86, 'Microsoft Visual Studio %0.1f' % self.vs_ver)
            return self.ri.lookup(self.ri.vs, '%0.1f' % self.vs_ver) or default

        @property
        def VCInstallDir(self):
            """
        Microsoft Visual C++ directory.

        Return
        ------
        str
            path
        """
            path = self._guess_vc() or self._guess_vc_legacy()
            if not isdir(path):
                msg = 'Microsoft Visual C++ directory not found'
                raise distutils.errors.DistutilsPlatformError(msg)
            return path

        def _guess_vc--- This code section failed: ---

 L. 849         0  LOAD_FAST                'self'
                2  LOAD_ATTR                vs_ver
                4  LOAD_CONST               14.0
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 850        10  LOAD_STR                 ''
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 852        14  SETUP_FINALLY        32  'to 32'

 L. 854        16  LOAD_FAST                'self'
               18  LOAD_ATTR                known_vs_paths
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                vs_ver
               24  BINARY_SUBSCR    
               26  STORE_FAST               'vs_dir'
               28  POP_BLOCK        
               30  JUMP_FORWARD         58  'to 58'
             32_0  COME_FROM_FINALLY    14  '14'

 L. 855        32  DUP_TOP          
               34  LOAD_GLOBAL              KeyError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 857        46  LOAD_FAST                'self'
               48  LOAD_ATTR                VSInstallDir
               50  STORE_FAST               'vs_dir'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            38  '38'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            30  '30'

 L. 859        58  LOAD_GLOBAL              join
               60  LOAD_FAST                'vs_dir'
               62  LOAD_STR                 'VC\\Tools\\MSVC'
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'guess_vc'

 L. 862        68  SETUP_FINALLY       106  'to 106'

 L. 864        70  LOAD_GLOBAL              listdir
               72  LOAD_FAST                'guess_vc'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               -1
               78  BINARY_SUBSCR    
               80  STORE_FAST               'vc_ver'

 L. 865        82  LOAD_FAST                'self'
               84  LOAD_METHOD              _as_float_version
               86  LOAD_FAST                'vc_ver'
               88  CALL_METHOD_1         1  ''
               90  LOAD_FAST                'self'
               92  STORE_ATTR               vc_ver

 L. 866        94  LOAD_GLOBAL              join
               96  LOAD_FAST                'guess_vc'
               98  LOAD_FAST                'vc_ver'
              100  CALL_FUNCTION_2       2  ''
              102  POP_BLOCK        
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    68  '68'

 L. 867       106  DUP_TOP          
              108  LOAD_GLOBAL              OSError
              110  LOAD_GLOBAL              IOError
              112  LOAD_GLOBAL              IndexError
              114  BUILD_TUPLE_3         3 
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   132  'to 132'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L. 868       126  POP_EXCEPT       
              128  LOAD_STR                 ''
              130  RETURN_VALUE     
            132_0  COME_FROM           118  '118'
              132  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 128

        def _guess_vc_legacy(self):
            """
        Locate Visual C++ for versions prior to 2017.

        Return
        ------
        str
            path
        """
            default = join(self.ProgramFilesx86, 'Microsoft Visual Studio %0.1f\\VC' % self.vs_ver)
            reg_path = join(self.ri.vc_for_python, '%0.1f' % self.vs_ver)
            python_vc = self.ri.lookup(reg_path, 'installdir')
            default_vc = join(python_vc, 'VC') if python_vc else default
            return self.ri.lookup(self.ri.vc, '%0.1f' % self.vs_ver) or default_vc

        @property
        def WindowsSdkVersion(self):
            """
        Microsoft Windows SDK versions for specified MSVC++ version.

        Return
        ------
        tuple of str
            versions
        """
            if self.vs_ver <= 9.0:
                return ('7.0', '6.1', '6.0a')
            if self.vs_ver == 10.0:
                return ('7.1', '7.0a')
            if self.vs_ver == 11.0:
                return ('8.0', '8.0a')
            if self.vs_ver == 12.0:
                return ('8.1', '8.1a')
            if self.vs_ver >= 14.0:
                return ('10.0', '8.1')

        @property
        def WindowsSdkLastVersion(self):
            """
        Microsoft Windows SDK last version.

        Return
        ------
        str
            version
        """
            return self._use_last_dir_name(join(self.WindowsSdkDir, 'lib'))

        @property
        def WindowsSdkDir(self):
            """
        Microsoft Windows SDK directory.

        Return
        ------
        str
            path
        """
            sdkdir = ''
            for ver in self.WindowsSdkVersion:
                loc = join(self.ri.windows_sdk, 'v%s' % ver)
                sdkdir = self.ri.lookup(loc, 'installationfolder')
                if sdkdir:
                    break
            else:
                if not (sdkdir and isdir(sdkdir)):
                    path = join(self.ri.vc_for_python, '%0.1f' % self.vc_ver)
                    install_base = self.ri.lookup(path, 'installdir')
                    if install_base:
                        sdkdir = join(install_base, 'WinSDK')
                if not (sdkdir and isdir(sdkdir)):
                    for ver in self.WindowsSdkVersion:
                        intver = ver[:ver.rfind('.')]
                        path = 'Microsoft SDKs\\Windows Kits\\%s' % intver
                        d = join(self.ProgramFiles, path)
                        if isdir(d):
                            sdkdir = d
                    else:
                        if not (sdkdir and isdir(sdkdir)):
                            for ver in self.WindowsSdkVersion:
                                path = 'Microsoft SDKs\\Windows\\v%s' % ver
                                d = join(self.ProgramFiles, path)
                                if isdir(d):
                                    sdkdir = d
                            else:
                                if not sdkdir:
                                    sdkdir = join(self.VCInstallDir, 'PlatformSDK')

                    return sdkdir

        @property
        def WindowsSDKExecutablePath(self):
            """
        Microsoft Windows SDK executable directory.

        Return
        ------
        str
            path
        """
            if self.vs_ver <= 11.0:
                netfxver = 35
                arch = ''
            else:
                netfxver = 40
                hidex86 = True if self.vs_ver <= 12.0 else False
                arch = self.pi.current_dir(x64=True, hidex86=hidex86)
            fx = 'WinSDK-NetFx%dTools%s' % (netfxver, arch.replace('\\', '-'))
            regpaths = []
            if self.vs_ver >= 14.0:
                for ver in self.NetFxSdkVersion:
                    regpaths += [joinself.ri.netfx_sdkverfx]

            for ver in self.WindowsSdkVersion:
                regpaths += [joinself.ri.windows_sdk('v%sA' % ver)fx]
            else:
                for path in regpaths:
                    execpath = self.ri.lookup(path, 'installationfolder')
                    if execpath:
                        return execpath

        @property
        def FSharpInstallDir(self):
            """
        Microsoft Visual F# directory.

        Return
        ------
        str
            path
        """
            path = join(self.ri.visualstudio, '%0.1f\\Setup\\F#' % self.vs_ver)
            return self.ri.lookup(path, 'productdir') or ''

        @property
        def UniversalCRTSdkDir(self):
            """
        Microsoft Universal CRT SDK directory.

        Return
        ------
        str
            path
        """
            vers = ('10', '81') if self.vs_ver >= 14.0 else ()
            for ver in vers:
                sdkdir = self.ri.lookup(self.ri.windows_kits_roots, 'kitsroot%s' % ver)
                if sdkdir:
                    return sdkdir or ''

        @property
        def UniversalCRTSdkLastVersion(self):
            """
        Microsoft Universal C Runtime SDK last version.

        Return
        ------
        str
            version
        """
            return self._use_last_dir_name(join(self.UniversalCRTSdkDir, 'lib'))

        @property
        def NetFxSdkVersion(self):
            """
        Microsoft .NET Framework SDK versions.

        Return
        ------
        tuple of str
            versions
        """
            if self.vs_ver >= 14.0:
                return ('4.7.2', '4.7.1', '4.7', '4.6.2', '4.6.1', '4.6', '4.5.2',
                        '4.5.1', '4.5')
            return ()

        @property
        def NetFxSdkDir(self):
            """
        Microsoft .NET Framework SDK directory.

        Return
        ------
        str
            path
        """
            sdkdir = ''
            for ver in self.NetFxSdkVersion:
                loc = join(self.ri.netfx_sdk, ver)
                sdkdir = self.ri.lookup(loc, 'kitsinstallationfolder')
                if sdkdir:
                    break
            else:
                return sdkdir

        @property
        def FrameworkDir32(self):
            """
        Microsoft .NET Framework 32bit directory.

        Return
        ------
        str
            path
        """
            guess_fw = join(self.WinDir, 'Microsoft.NET\\Framework')
            return self.ri.lookup(self.ri.vc, 'frameworkdir32') or guess_fw

        @property
        def FrameworkDir64(self):
            """
        Microsoft .NET Framework 64bit directory.

        Return
        ------
        str
            path
        """
            guess_fw = join(self.WinDir, 'Microsoft.NET\\Framework64')
            return self.ri.lookup(self.ri.vc, 'frameworkdir64') or guess_fw

        @property
        def FrameworkVersion32(self):
            """
        Microsoft .NET Framework 32bit versions.

        Return
        ------
        tuple of str
            versions
        """
            return self._find_dot_net_versions(32)

        @property
        def FrameworkVersion64(self):
            """
        Microsoft .NET Framework 64bit versions.

        Return
        ------
        tuple of str
            versions
        """
            return self._find_dot_net_versions(64)

        def _find_dot_net_versions(self, bits):
            """
        Find Microsoft .NET Framework versions.

        Parameters
        ----------
        bits: int
            Platform number of bits: 32 or 64.

        Return
        ------
        tuple of str
            versions
        """
            reg_ver = self.ri.lookup(self.ri.vc, 'frameworkver%d' % bits)
            dot_net_dir = getattr(self, 'FrameworkDir%d' % bits)
            ver = reg_ver or self._use_last_dir_name(dot_net_dir, 'v') or ''
            if self.vs_ver >= 12.0:
                return (ver, 'v4.0')
            if self.vs_ver >= 10.0:
                return ('v4.0.30319' if ver.lower()[:2] != 'v4' else ver, 'v3.5')
            if self.vs_ver == 9.0:
                return ('v3.5', 'v2.0.50727')
            if self.vs_ver == 8.0:
                return ('v3.0', 'v2.0.50727')

        @staticmethod
        def _use_last_dir_name(path, prefix=''):
            """
        Return name of the last dir in path or '' if no dir found.

        Parameters
        ----------
        path: str
            Use dirs in this path
        prefix: str
            Use only dirs starting by this prefix

        Return
        ------
        str
            name
        """
            matching_dirs = (dir_name for dir_name in reversed(listdir(path)) if isdir(join(path, dir_name)) if dir_name.startswith(prefix))
            return next(matching_dirs, None) or ''


    class EnvironmentInfo:
        __doc__ = '\n    Return environment variables for specified Microsoft Visual C++ version\n    and platform : Lib, Include, Path and libpath.\n\n    This function is compatible with Microsoft Visual C++ 9.0 to 14.X.\n\n    Script created by analysing Microsoft environment configuration files like\n    "vcvars[...].bat", "SetEnv.Cmd", "vcbuildtools.bat", ...\n\n    Parameters\n    ----------\n    arch: str\n        Target architecture.\n    vc_ver: float\n        Required Microsoft Visual C++ version. If not set, autodetect the last\n        version.\n    vc_min_ver: float\n        Minimum Microsoft Visual C++ version.\n    '

        def __init__(self, arch, vc_ver=None, vc_min_ver=0):
            self.pi = PlatformInfo(arch)
            self.ri = RegistryInfo(self.pi)
            self.si = SystemInfo(self.ri, vc_ver)
            if self.vc_ver < vc_min_ver:
                err = 'No suitable Microsoft Visual C++ version found'
                raise distutils.errors.DistutilsPlatformError(err)

        @property
        def vs_ver(self):
            """
        Microsoft Visual Studio.

        Return
        ------
        float
            version
        """
            return self.si.vs_ver

        @property
        def vc_ver(self):
            """
        Microsoft Visual C++ version.

        Return
        ------
        float
            version
        """
            return self.si.vc_ver

        @property
        def VSTools(self):
            """
        Microsoft Visual Studio Tools.

        Return
        ------
        list of str
            paths
        """
            paths = [
             'Common7\\IDE', 'Common7\\Tools']
            if self.vs_ver >= 14.0:
                arch_subdir = self.pi.current_dir(hidex86=True, x64=True)
                paths += ['Common7\\IDE\\CommonExtensions\\Microsoft\\TestWindow']
                paths += ['Team Tools\\Performance Tools']
                paths += ['Team Tools\\Performance Tools%s' % arch_subdir]
            return [join(self.si.VSInstallDir, path) for path in paths]

        @property
        def VCIncludes(self):
            """
        Microsoft Visual C++ & Microsoft Foundation Class Includes.

        Return
        ------
        list of str
            paths
        """
            return [
             join(self.si.VCInstallDir, 'Include'),
             join(self.si.VCInstallDir, 'ATLMFC\\Include')]

        @property
        def VCLibraries(self):
            """
        Microsoft Visual C++ & Microsoft Foundation Class Libraries.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver >= 15.0:
                arch_subdir = self.pi.target_dir(x64=True)
            else:
                arch_subdir = self.pi.target_dir(hidex86=True)
            paths = [
             'Lib%s' % arch_subdir, 'ATLMFC\\Lib%s' % arch_subdir]
            if self.vs_ver >= 14.0:
                paths += ['Lib\\store%s' % arch_subdir]
            return [join(self.si.VCInstallDir, path) for path in paths]

        @property
        def VCStoreRefs(self):
            """
        Microsoft Visual C++ store references Libraries.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver < 14.0:
                return []
            return [join(self.si.VCInstallDir, 'Lib\\store\\references')]

        @property
        def VCTools(self):
            """
        Microsoft Visual C++ Tools.

        Return
        ------
        list of str
            paths
        """
            si = self.si
            tools = [join(si.VCInstallDir, 'VCPackages')]
            forcex86 = True if self.vs_ver <= 10.0 else False
            arch_subdir = self.pi.cross_dir(forcex86)
            if arch_subdir:
                tools += [join(si.VCInstallDir, 'Bin%s' % arch_subdir)]
            if self.vs_ver == 14.0:
                path = 'Bin%s' % self.pi.current_dir(hidex86=True)
                tools += [join(si.VCInstallDir, path)]
            elif self.vs_ver >= 15.0:
                host_dir = 'bin\\HostX86%s' if self.pi.current_is_x86() else 'bin\\HostX64%s'
                tools += [
                 join(si.VCInstallDir, host_dir % self.pi.target_dir(x64=True))]
                if self.pi.current_cpu != self.pi.target_cpu:
                    tools += [
                     join(si.VCInstallDir, host_dir % self.pi.current_dir(x64=True))]
            else:
                tools += [join(si.VCInstallDir, 'Bin')]
            return tools

        @property
        def OSLibraries(self):
            """
        Microsoft Windows SDK Libraries.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver <= 10.0:
                arch_subdir = self.pi.target_dir(hidex86=True, x64=True)
                return [
                 join(self.si.WindowsSdkDir, 'Lib%s' % arch_subdir)]
            arch_subdir = self.pi.target_dir(x64=True)
            lib = join(self.si.WindowsSdkDir, 'lib')
            libver = self._sdk_subdir
            return [
             join(lib, '%sum%s' % (libver, arch_subdir))]

        @property
        def OSIncludes(self):
            """
        Microsoft Windows SDK Include.

        Return
        ------
        list of str
            paths
        """
            include = join(self.si.WindowsSdkDir, 'include')
            if self.vs_ver <= 10.0:
                return [include, join(include, 'gl')]
            if self.vs_ver >= 14.0:
                sdkver = self._sdk_subdir
            else:
                sdkver = ''
            return [join(include, '%sshared' % sdkver),
             join(include, '%sum' % sdkver),
             join(include, '%swinrt' % sdkver)]

        @property
        def OSLibpath(self):
            """
        Microsoft Windows SDK Libraries Paths.

        Return
        ------
        list of str
            paths
        """
            ref = join(self.si.WindowsSdkDir, 'References')
            libpath = []
            if self.vs_ver <= 9.0:
                libpath += self.OSLibraries
            if self.vs_ver >= 11.0:
                libpath += [join(ref, 'CommonConfiguration\\Neutral')]
            if self.vs_ver >= 14.0:
                libpath += [
                 ref,
                 join(self.si.WindowsSdkDir, 'UnionMetadata'),
                 joinref'Windows.Foundation.UniversalApiContract''1.0.0.0',
                 joinref'Windows.Foundation.FoundationContract''1.0.0.0',
                 joinref'Windows.Networking.Connectivity.WwanContract''1.0.0.0',
                 join(self.si.WindowsSdkDir, 'ExtensionSDKs', 'Microsoft.VCLibs', '%0.1f' % self.vs_ver, 'References', 'CommonConfiguration', 'neutral')]
            return libpath

        @property
        def SdkTools(self):
            """
        Microsoft Windows SDK Tools.

        Return
        ------
        list of str
            paths
        """
            return list(self._sdk_tools())

        def _sdk_tools(self):
            """
        Microsoft Windows SDK Tools paths generator.

        Return
        ------
        generator of str
            paths
        """
            if self.vs_ver < 15.0:
                bin_dir = 'Bin' if self.vs_ver <= 11.0 else 'Bin\\x86'
                yield join(self.si.WindowsSdkDir, bin_dir)
            if not self.pi.current_is_x86():
                arch_subdir = self.pi.current_dir(x64=True)
                path = 'Bin%s' % arch_subdir
                yield join(self.si.WindowsSdkDir, path)
            if self.vs_ver in (10.0, 11.0):
                if self.pi.target_is_x86():
                    arch_subdir = ''
                else:
                    arch_subdir = self.pi.current_dir(hidex86=True, x64=True)
                path = 'Bin\\NETFX 4.0 Tools%s' % arch_subdir
                yield join(self.si.WindowsSdkDir, path)
            elif self.vs_ver >= 15.0:
                path = join(self.si.WindowsSdkDir, 'Bin')
                arch_subdir = self.pi.current_dir(x64=True)
                sdkver = self.si.WindowsSdkLastVersion
                yield join(path, '%s%s' % (sdkver, arch_subdir))
            if self.si.WindowsSDKExecutablePath:
                yield self.si.WindowsSDKExecutablePath

        @property
        def _sdk_subdir(self):
            """
        Microsoft Windows SDK version subdir.

        Return
        ------
        str
            subdir
        """
            ucrtver = self.si.WindowsSdkLastVersion
            if ucrtver:
                return '%s\\' % ucrtver
            return ''

        @property
        def SdkSetup(self):
            """
        Microsoft Windows SDK Setup.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver > 9.0:
                return []
            return [
             join(self.si.WindowsSdkDir, 'Setup')]

        @property
        def FxTools(self):
            """
        Microsoft .NET Framework Tools.

        Return
        ------
        list of str
            paths
        """
            pi = self.pi
            si = self.si
            if self.vs_ver <= 10.0:
                include32 = True
                include64 = not pi.target_is_x86() and not pi.current_is_x86()
            else:
                include32 = pi.target_is_x86() or pi.current_is_x86()
                include64 = pi.current_cpu == 'amd64' or pi.target_cpu == 'amd64'
            tools = []
            if include32:
                tools += [join(si.FrameworkDir32, ver) for ver in si.FrameworkVersion32]
            if include64:
                tools += [join(si.FrameworkDir64, ver) for ver in si.FrameworkVersion64]
            return tools

        @property
        def NetFxSDKLibraries(self):
            """
        Microsoft .Net Framework SDK Libraries.

        Return
        ------
        list of str
            paths
        """
            if not (self.vs_ver < 14.0 or self.si.NetFxSdkDir):
                return []
            arch_subdir = self.pi.target_dir(x64=True)
            return [
             join(self.si.NetFxSdkDir, 'lib\\um%s' % arch_subdir)]

        @property
        def NetFxSDKIncludes(self):
            """
        Microsoft .Net Framework SDK Includes.

        Return
        ------
        list of str
            paths
        """
            if not (self.vs_ver < 14.0 or self.si.NetFxSdkDir):
                return []
            return [
             join(self.si.NetFxSdkDir, 'include\\um')]

        @property
        def VsTDb(self):
            """
        Microsoft Visual Studio Team System Database.

        Return
        ------
        list of str
            paths
        """
            return [
             join(self.si.VSInstallDir, 'VSTSDB\\Deploy')]

        @property
        def MSBuild(self):
            """
        Microsoft Build Engine.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver < 12.0:
                return []
            if self.vs_ver < 15.0:
                base_path = self.si.ProgramFilesx86
                arch_subdir = self.pi.current_dir(hidex86=True)
            else:
                base_path = self.si.VSInstallDir
                arch_subdir = ''
            path = 'MSBuild\\%0.1f\\bin%s' % (self.vs_ver, arch_subdir)
            build = [join(base_path, path)]
            if self.vs_ver >= 15.0:
                build += [joinbase_pathpath'Roslyn']
            return build

        @property
        def HTMLHelpWorkshop(self):
            """
        Microsoft HTML Help Workshop.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver < 11.0:
                return []
            return [
             join(self.si.ProgramFilesx86, 'HTML Help Workshop')]

        @property
        def UCRTLibraries(self):
            """
        Microsoft Universal C Runtime SDK Libraries.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver < 14.0:
                return []
            arch_subdir = self.pi.target_dir(x64=True)
            lib = join(self.si.UniversalCRTSdkDir, 'lib')
            ucrtver = self._ucrt_subdir
            return [
             join(lib, '%sucrt%s' % (ucrtver, arch_subdir))]

        @property
        def UCRTIncludes(self):
            """
        Microsoft Universal C Runtime SDK Include.

        Return
        ------
        list of str
            paths
        """
            if self.vs_ver < 14.0:
                return []
            include = join(self.si.UniversalCRTSdkDir, 'include')
            return [
             join(include, '%sucrt' % self._ucrt_subdir)]

        @property
        def _ucrt_subdir(self):
            """
        Microsoft Universal C Runtime SDK version subdir.

        Return
        ------
        str
            subdir
        """
            ucrtver = self.si.UniversalCRTSdkLastVersion
            if ucrtver:
                return '%s\\' % ucrtver
            return ''

        @property
        def FSharp(self):
            """
        Microsoft Visual F#.

        Return
        ------
        list of str
            paths
        """
            if 11.0 > self.vs_ver > 12.0:
                return []
            return [
             self.si.FSharpInstallDir]

        @property
        def VCRuntimeRedist(self):
            """
        Microsoft Visual C++ runtime redistributable dll.

        Return
        ------
        str
            path
        """
            vcruntime = 'vcruntime%d0.dll' % self.vc_ver
            arch_subdir = self.pi.target_dir(x64=True).strip('\\')
            prefixes = []
            tools_path = self.si.VCInstallDir
            redist_path = dirname(tools_path.replace('\\Tools', '\\Redist'))
            if isdir(redist_path):
                redist_path = join(redist_path, listdir(redist_path)[(-1)])
                prefixes += [redist_path, join(redist_path, 'onecore')]
            prefixes += [join(tools_path, 'redist')]
            crt_dirs = (
             'Microsoft.VC%d.CRT' % (self.vc_ver * 10),
             'Microsoft.VC%d.CRT' % (int(self.vs_ver) * 10))
            for prefix, crt_dir in itertools.product(prefixes, crt_dirs):
                path = join(prefix, arch_subdir, crt_dir, vcruntime)
                if isfile(path):
                    return path

        def return_env(self, exists=True):
            """
        Return environment dict.

        Parameters
        ----------
        exists: bool
            It True, only return existing paths.

        Return
        ------
        dict
            environment
        """
            env = dict(include=(self._build_paths('include', [
             self.VCIncludes,
             self.OSIncludes,
             self.UCRTIncludes,
             self.NetFxSDKIncludes], exists)),
              lib=(self._build_paths('lib', [
             self.VCLibraries,
             self.OSLibraries,
             self.FxTools,
             self.UCRTLibraries,
             self.NetFxSDKLibraries], exists)),
              libpath=(self._build_paths('libpath', [
             self.VCLibraries,
             self.FxTools,
             self.VCStoreRefs,
             self.OSLibpath], exists)),
              path=(self._build_paths('path', [
             self.VCTools,
             self.VSTools,
             self.VsTDb,
             self.SdkTools,
             self.SdkSetup,
             self.FxTools,
             self.MSBuild,
             self.HTMLHelpWorkshop,
             self.FSharp], exists)))
            if self.vs_ver >= 14:
                if isfile(self.VCRuntimeRedist):
                    env['py_vcruntime_redist'] = self.VCRuntimeRedist
            return env

        def _build_paths(self, name, spec_path_lists, exists):
            """
        Given an environment variable name and specified paths,
        return a pathsep-separated string of paths containing
        unique, extant, directories from those paths and from
        the environment variable. Raise an error if no paths
        are resolved.

        Parameters
        ----------
        name: str
            Environment variable name
        spec_path_lists: list of str
            Paths
        exists: bool
            It True, only return existing paths.

        Return
        ------
        str
            Pathsep-separated paths
        """
            spec_paths = itertools.chain.from_iterable(spec_path_lists)
            env_paths = environ.get(name, '').split(pathsep)
            paths = itertools.chain(spec_paths, env_paths)
            extant_paths = list(filter(isdir, paths)) if exists else paths
            if not extant_paths:
                msg = '%s environment variable is empty' % name.upper()
                raise distutils.errors.DistutilsPlatformError(msg)
            unique_paths = self._unique_everseen(extant_paths)
            return pathsep.join(unique_paths)

        @staticmethod
        def _unique_everseen(iterable, key=None):
            """
        List unique elements, preserving order.
        Remember all elements ever seen.

        _unique_everseen('AAAABBBCCDAABBB') --> A B C D

        _unique_everseen('ABBCcAD', str.lower) --> A B C D
        """
            seen = set()
            seen_add = seen.add
            if key is None:
                for element in filterfalse(seen.__contains__, iterable):
                    seen_add(element)
                    yield element

            else:
                for element in iterable:
                    k = key(element)
                    if k not in seen:
                        seen_add(k)
                        yield element