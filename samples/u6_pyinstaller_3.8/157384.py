# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\msvc.py
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

Microsoft Visual C++ 14.0:
    Microsoft Visual C++ Build Tools 2015 (x86, x64, arm)
    Microsoft Visual Studio 2017 (x86, x64, arm, arm64)
    Microsoft Visual Studio Build Tools 2017 (x86, x64, arm, arm64)
"""
import os, sys, platform, itertools, distutils.errors
from setuptools.extern.packaging.version import LegacyVersion
from setuptools.extern.six.moves import filterfalse
from .monkey import get_unpatched
if platform.system() == 'Windows':
    from setuptools.extern.six.moves import winreg
    safe_env = os.environ
else:

    class winreg:
        HKEY_USERS = None
        HKEY_CURRENT_USER = None
        HKEY_LOCAL_MACHINE = None
        HKEY_CLASSES_ROOT = None


    safe_env = dict()
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
    compiler build for Python (VCForPython). Fall back to original behavior
    when the standalone compiler is not available.

    Redirect the path of "vcvarsall.bat".

    Known supported compilers
    -------------------------
    Microsoft Visual C++ 9.0:
        Microsoft Visual C++ Compiler for Python 2.7 (x86, amd64)

    Parameters
    ----------
    version: float
        Required Microsoft Visual C++ version.

    Return
    ------
    vcvarsall.bat path: str
    """
        VC_BASE = 'Software\\%sMicrosoft\\DevDiv\\VCForPython\\%0.1f'
        key = VC_BASE % ('', version)
        try:
            productdir = Reg.get_value(key, 'installdir')
        except KeyError:
            try:
                key = VC_BASE % ('Wow6432Node\\', version)
                productdir = Reg.get_value(key, 'installdir')
            except KeyError:
                productdir = None

        else:
            if productdir:
                vcvarsall = os.path.os.path.join(productdir, 'vcvarsall.bat')
                if os.path.isfile(vcvarsall):
                    return vcvarsall
            return get_unpatched(msvc9_find_vcvarsall)(version)


    def msvc9_query_vcvarsall--- This code section failed: ---

 L. 135         0  SETUP_FINALLY        30  'to 30'

 L. 136         2  LOAD_GLOBAL              get_unpatched
                4  LOAD_GLOBAL              msvc9_query_vcvarsall
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'orig'

 L. 137        10  LOAD_FAST                'orig'
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

 L. 138        30  DUP_TOP          
               32  LOAD_GLOBAL              distutils
               34  LOAD_ATTR                errors
               36  LOAD_ATTR                DistutilsPlatformError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    52  'to 52'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 140        48  POP_EXCEPT       
               50  JUMP_FORWARD         72  'to 72'
             52_0  COME_FROM            40  '40'

 L. 141        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    70  'to 70'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 143        66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            58  '58'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            50  '50'

 L. 146        72  SETUP_FINALLY        90  'to 90'

 L. 147        74  LOAD_GLOBAL              EnvironmentInfo
               76  LOAD_FAST                'arch'
               78  LOAD_FAST                'ver'
               80  CALL_FUNCTION_2       2  ''
               82  LOAD_METHOD              return_env
               84  CALL_METHOD_0         0  ''
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    72  '72'

 L. 148        90  DUP_TOP          
               92  LOAD_GLOBAL              distutils
               94  LOAD_ATTR                errors
               96  LOAD_ATTR                DistutilsPlatformError
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   140  'to 140'
              102  POP_TOP          
              104  STORE_FAST               'exc'
              106  POP_TOP          
              108  SETUP_FINALLY       128  'to 128'

 L. 149       110  LOAD_GLOBAL              _augment_exception
              112  LOAD_FAST                'exc'
              114  LOAD_FAST                'ver'
              116  LOAD_FAST                'arch'
              118  CALL_FUNCTION_3       3  ''
              120  POP_TOP          

 L. 150       122  RAISE_VARARGS_0       0  'reraise'
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

Parse error at or near `POP_TOP' instruction at offset 44


    def msvc14_get_vc_env--- This code section failed: ---

 L. 177         0  SETUP_FINALLY        16  'to 16'

 L. 178         2  LOAD_GLOBAL              get_unpatched
                4  LOAD_GLOBAL              msvc14_get_vc_env
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'plat_spec'
               10  CALL_FUNCTION_1       1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 179        16  DUP_TOP          
               18  LOAD_GLOBAL              distutils
               20  LOAD_ATTR                errors
               22  LOAD_ATTR                DistutilsPlatformError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    38  'to 38'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 181        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            26  '26'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

 L. 184        40  SETUP_FINALLY        60  'to 60'

 L. 185        42  LOAD_GLOBAL              EnvironmentInfo
               44  LOAD_FAST                'plat_spec'
               46  LOAD_CONST               14.0
               48  LOAD_CONST               ('vc_min_ver',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  LOAD_METHOD              return_env
               54  CALL_METHOD_0         0  ''
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    40  '40'

 L. 186        60  DUP_TOP          
               62  LOAD_GLOBAL              distutils
               64  LOAD_ATTR                errors
               66  LOAD_ATTR                DistutilsPlatformError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE   108  'to 108'
               72  POP_TOP          
               74  STORE_FAST               'exc'
               76  POP_TOP          
               78  SETUP_FINALLY        96  'to 96'

 L. 187        80  LOAD_GLOBAL              _augment_exception
               82  LOAD_FAST                'exc'
               84  LOAD_CONST               14.0
               86  CALL_FUNCTION_2       2  ''
               88  POP_TOP          

 L. 188        90  RAISE_VARARGS_0       0  'reraise'
               92  POP_BLOCK        
               94  BEGIN_FINALLY    
             96_0  COME_FROM_FINALLY    78  '78'
               96  LOAD_CONST               None
               98  STORE_FAST               'exc'
              100  DELETE_FAST              'exc'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            70  '70'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'

Parse error at or near `POP_TOP' instruction at offset 30


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
        if 'vcvarsall' in message.lower() or 'visual c' in message.lower():
            tmpl = 'Microsoft Visual C++ {version:0.1f} is required.'
            message = (tmpl.format)(**locals())
            msdownload = 'www.microsoft.com/download/details.aspx?id=%d'
            if version == 9.0:
                if arch.lower().find('ia64') > -1:
                    message += ' Get it with "Microsoft Windows SDK 7.0": '
                    message += msdownload % 3138
                else:
                    message += ' Get it from http://aka.ms/vcpython27'
        elif version == 10.0:
            message += ' Get it with "Microsoft Windows SDK 7.1": '
            message += msdownload % 8279
        else:
            if version >= 14.0:
                message += ' Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/'
        exc.args = (message,)


    class PlatformInfo:
        __doc__ = '\n    Current and Target Architectures informations.\n\n    Parameters\n    ----------\n    arch: str\n        Target architecture.\n    '
        current_cpu = safe_env.get('processor_architecture', '').lower()

        def __init__(self, arch):
            self.arch = arch.lower().replace('x64', 'amd64')

        @property
        def target_cpu(self):
            return self.arch[self.arch.find('_') + 1:]

        def target_is_x86(self):
            return self.target_cpu == 'x86'

        def current_is_x86(self):
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
        subfolder: str
            '   arget', or '' (see hidex86 parameter)
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
        subfolder: str
            '\current', or '' (see hidex86 parameter)
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
            Use 'x86' as current architecture even if current acritecture is
            not x86.

        Return
        ------
        subfolder: str
            '' if target architecture is current architecture,
            '\current_target' if not.
        """
            current = 'x86' if forcex86 else self.current_cpu
            if self.target_cpu == current:
                return ''
            return self.target_dir().replace('\\', '\\%s_' % current)


    class RegistryInfo:
        __doc__ = '\n    Microsoft Visual Studio related registry informations.\n\n    Parameters\n    ----------\n    platform_info: PlatformInfo\n        "PlatformInfo" instance.\n    '
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
        """
            return 'VisualStudio'

        @property
        def sxs(self):
            """
        Microsoft Visual Studio SxS registry key.
        """
            return os.path.join(self.visualstudio, 'SxS')

        @property
        def vc(self):
            """
        Microsoft Visual C++ VC7 registry key.
        """
            return os.path.join(self.sxs, 'VC7')

        @property
        def vs(self):
            """
        Microsoft Visual Studio VS7 registry key.
        """
            return os.path.join(self.sxs, 'VS7')

        @property
        def vc_for_python(self):
            """
        Microsoft Visual C++ for Python registry key.
        """
            return 'DevDiv\\VCForPython'

        @property
        def microsoft_sdk(self):
            """
        Microsoft SDK registry key.
        """
            return 'Microsoft SDKs'

        @property
        def windows_sdk(self):
            """
        Microsoft Windows/Platform SDK registry key.
        """
            return os.path.join(self.microsoft_sdk, 'Windows')

        @property
        def netfx_sdk(self):
            """
        Microsoft .NET Framework SDK registry key.
        """
            return os.path.join(self.microsoft_sdk, 'NETFXSDK')

        @property
        def windows_kits_roots(self):
            """
        Microsoft Windows Kits Roots registry key.
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
        str: value
        """
            node64 = '' if (self.pi.current_is_x86() or x86) else 'Wow6432Node'
            return os.path.join('Software', node64, 'Microsoft', key)

        def lookup--- This code section failed: ---

 L. 444         0  LOAD_GLOBAL              winreg
                2  LOAD_ATTR                KEY_READ
                4  STORE_FAST               'KEY_READ'

 L. 445         6  LOAD_GLOBAL              winreg
                8  LOAD_ATTR                OpenKey
               10  STORE_FAST               'openkey'

 L. 446        12  LOAD_FAST                'self'
               14  LOAD_ATTR                microsoft
               16  STORE_FAST               'ms'

 L. 447        18  LOAD_FAST                'self'
               20  LOAD_ATTR                HKEYS
               22  GET_ITER         
               24  FOR_ITER            198  'to 198'
               26  STORE_FAST               'hkey'

 L. 448        28  SETUP_FINALLY        52  'to 52'

 L. 449        30  LOAD_FAST                'openkey'
               32  LOAD_FAST                'hkey'
               34  LOAD_FAST                'ms'
               36  LOAD_FAST                'key'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               0
               42  LOAD_FAST                'KEY_READ'
               44  CALL_FUNCTION_4       4  ''
               46  STORE_FAST               'bkey'
               48  POP_BLOCK        
               50  JUMP_FORWARD        148  'to 148'
             52_0  COME_FROM_FINALLY    28  '28'

 L. 450        52  DUP_TOP          
               54  LOAD_GLOBAL              OSError
               56  LOAD_GLOBAL              IOError
               58  BUILD_TUPLE_2         2 
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   146  'to 146'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 451        70  LOAD_FAST                'self'
               72  LOAD_ATTR                pi
               74  LOAD_METHOD              current_is_x86
               76  CALL_METHOD_0         0  ''
               78  POP_JUMP_IF_TRUE    138  'to 138'

 L. 452        80  SETUP_FINALLY       106  'to 106'

 L. 453        82  LOAD_FAST                'openkey'
               84  LOAD_FAST                'hkey'
               86  LOAD_FAST                'ms'
               88  LOAD_FAST                'key'
               90  LOAD_CONST               True
               92  CALL_FUNCTION_2       2  ''
               94  LOAD_CONST               0
               96  LOAD_FAST                'KEY_READ'
               98  CALL_FUNCTION_4       4  ''
              100  STORE_FAST               'bkey'
              102  POP_BLOCK        
              104  JUMP_ABSOLUTE       142  'to 142'
            106_0  COME_FROM_FINALLY    80  '80'

 L. 454       106  DUP_TOP          
              108  LOAD_GLOBAL              OSError
              110  LOAD_GLOBAL              IOError
              112  BUILD_TUPLE_2         2 
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   134  'to 134'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 455       124  POP_EXCEPT       
              126  POP_EXCEPT       
              128  JUMP_BACK            24  'to 24'
              130  POP_EXCEPT       
              132  JUMP_ABSOLUTE       142  'to 142'
            134_0  COME_FROM           116  '116'
              134  END_FINALLY      
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM            78  '78'

 L. 457       138  POP_EXCEPT       
              140  JUMP_BACK            24  'to 24'
            142_0  COME_FROM           136  '136'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            62  '62'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            50  '50'

 L. 458       148  SETUP_FINALLY       172  'to 172'

 L. 459       150  LOAD_GLOBAL              winreg
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

 L. 460       172  DUP_TOP          
              174  LOAD_GLOBAL              OSError
              176  LOAD_GLOBAL              IOError
              178  BUILD_TUPLE_2         2 
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   194  'to 194'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          

 L. 461       190  POP_EXCEPT       
              192  JUMP_BACK            24  'to 24'
            194_0  COME_FROM           182  '182'
              194  END_FINALLY      
              196  JUMP_BACK            24  'to 24'

Parse error at or near `POP_EXCEPT' instruction at offset 130


    class SystemInfo:
        __doc__ = '\n    Microsoft Windows and Visual Studio related system inormations.\n\n    Parameters\n    ----------\n    registry_info: RegistryInfo\n        "RegistryInfo" instance.\n    vc_ver: float\n        Required Microsoft Visual C++ version.\n    '
        WinDir = safe_env.get('WinDir', '')
        ProgramFiles = safe_env.get('ProgramFiles', '')
        ProgramFilesx86 = safe_env.get('ProgramFiles(x86)', ProgramFiles)

        def __init__(self, registry_info, vc_ver=None):
            self.ri = registry_info
            self.pi = self.ri.pi
            self.vc_ver = vc_ver or self._find_latest_available_vc_ver()

        def _find_latest_available_vc_ver--- This code section failed: ---

 L. 488         0  SETUP_FINALLY        16  'to 16'

 L. 489         2  LOAD_FAST                'self'
                4  LOAD_METHOD              find_available_vc_vers
                6  CALL_METHOD_0         0  ''
                8  LOAD_CONST               -1
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 490        16  DUP_TOP          
               18  LOAD_GLOBAL              IndexError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    50  'to 50'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 491        30  LOAD_STR                 'No Microsoft Visual C++ version found'
               32  STORE_FAST               'err'

 L. 492        34  LOAD_GLOBAL              distutils
               36  LOAD_ATTR                errors
               38  LOAD_METHOD              DistutilsPlatformError
               40  LOAD_FAST                'err'
               42  CALL_METHOD_1         1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            22  '22'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 26

        def find_available_vc_vers--- This code section failed: ---

 L. 498         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ri
                4  LOAD_ATTR                microsoft
                6  STORE_FAST               'ms'

 L. 499         8  LOAD_FAST                'self'
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

 L. 500        30  BUILD_LIST_0          0 
               32  STORE_FAST               'vc_vers'

 L. 501        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ri
               38  LOAD_ATTR                HKEYS
               40  GET_ITER         
               42  FOR_ITER            284  'to 284'
               44  STORE_FAST               'hkey'

 L. 502        46  LOAD_FAST                'vckeys'
               48  GET_ITER         
               50  FOR_ITER            282  'to 282'
               52  STORE_FAST               'key'

 L. 503        54  SETUP_FINALLY        82  'to 82'

 L. 504        56  LOAD_GLOBAL              winreg
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

 L. 505        82  DUP_TOP          
               84  LOAD_GLOBAL              OSError
               86  LOAD_GLOBAL              IOError
               88  BUILD_TUPLE_2         2 
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   108  'to 108'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 506       100  POP_EXCEPT       
              102  JUMP_BACK            50  'to 50'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            92  '92'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            80  '80'

 L. 507       110  LOAD_GLOBAL              winreg
              112  LOAD_METHOD              QueryInfoKey
              114  LOAD_FAST                'bkey'
              116  CALL_METHOD_1         1  ''
              118  UNPACK_SEQUENCE_3     3 
              120  STORE_FAST               'subkeys'
              122  STORE_FAST               'values'
              124  STORE_FAST               '_'

 L. 508       126  LOAD_GLOBAL              range
              128  LOAD_FAST                'values'
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
              134  FOR_ITER            204  'to 204'
              136  STORE_FAST               'i'

 L. 509       138  SETUP_FINALLY       182  'to 182'

 L. 510       140  LOAD_GLOBAL              float
              142  LOAD_GLOBAL              winreg
              144  LOAD_METHOD              EnumValue
              146  LOAD_FAST                'bkey'
              148  LOAD_FAST                'i'
              150  CALL_METHOD_2         2  ''
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'ver'

 L. 511       160  LOAD_FAST                'ver'
              162  LOAD_FAST                'vc_vers'
              164  COMPARE_OP               not-in
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 512       168  LOAD_FAST                'vc_vers'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'ver'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           166  '166'
              178  POP_BLOCK        
              180  JUMP_BACK           134  'to 134'
            182_0  COME_FROM_FINALLY   138  '138'

 L. 513       182  DUP_TOP          
              184  LOAD_GLOBAL              ValueError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   200  'to 200'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 514       196  POP_EXCEPT       
              198  JUMP_BACK           134  'to 134'
            200_0  COME_FROM           188  '188'
              200  END_FINALLY      
              202  JUMP_BACK           134  'to 134'

 L. 515       204  LOAD_GLOBAL              range
              206  LOAD_FAST                'subkeys'
              208  CALL_FUNCTION_1       1  ''
              210  GET_ITER         
              212  FOR_ITER            280  'to 280'
              214  STORE_FAST               'i'

 L. 516       216  SETUP_FINALLY       256  'to 256'

 L. 517       218  LOAD_GLOBAL              float
              220  LOAD_GLOBAL              winreg
              222  LOAD_METHOD              EnumKey
              224  LOAD_FAST                'bkey'
              226  LOAD_FAST                'i'
              228  CALL_METHOD_2         2  ''
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'ver'

 L. 518       234  LOAD_FAST                'ver'
              236  LOAD_FAST                'vc_vers'
              238  COMPARE_OP               not-in
              240  POP_JUMP_IF_FALSE   252  'to 252'

 L. 519       242  LOAD_FAST                'vc_vers'
              244  LOAD_METHOD              append
              246  LOAD_FAST                'ver'
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
            252_0  COME_FROM           240  '240'
              252  POP_BLOCK        
              254  JUMP_BACK           212  'to 212'
            256_0  COME_FROM_FINALLY   216  '216'

 L. 520       256  DUP_TOP          
              258  LOAD_GLOBAL              ValueError
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   276  'to 276'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 521       272  POP_EXCEPT       
              274  JUMP_BACK           212  'to 212'
            276_0  COME_FROM           262  '262'
              276  END_FINALLY      
              278  JUMP_BACK           212  'to 212'
              280  JUMP_BACK            50  'to 50'
              282  JUMP_BACK            42  'to 42'

 L. 522       284  LOAD_GLOBAL              sorted
              286  LOAD_FAST                'vc_vers'
              288  CALL_FUNCTION_1       1  ''
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 104

        @property
        def VSInstallDir(self):
            """
        Microsoft Visual Studio directory.
        """
            name = 'Microsoft Visual Studio %0.1f' % self.vc_ver
            default = os.path.join(self.ProgramFilesx86, name)
            return self.ri.lookup(self.ri.vs, '%0.1f' % self.vc_ver) or default

        @property
        def VCInstallDir(self):
            """
        Microsoft Visual C++ directory.
        """
            self.VSInstallDir
            guess_vc = self._guess_vc() or self._guess_vc_legacy()
            reg_path = os.path.join(self.ri.vc_for_python, '%0.1f' % self.vc_ver)
            python_vc = self.ri.lookup(reg_path, 'installdir')
            default_vc = os.path.join(python_vc, 'VC') if python_vc else guess_vc
            path = self.ri.lookup(self.ri.vc, '%0.1f' % self.vc_ver) or default_vc
            if not os.path.isdir(path):
                msg = 'Microsoft Visual C++ directory not found'
                raise distutils.errors.DistutilsPlatformError(msg)
            return path

        def _guess_vc--- This code section failed: ---

 L. 563         0  LOAD_FAST                'self'
                2  LOAD_ATTR                vc_ver
                4  LOAD_CONST               14.0
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 564        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 566        14  LOAD_STR                 'VC\\Tools\\MSVC'
               16  STORE_FAST               'default'

 L. 567        18  LOAD_GLOBAL              os
               20  LOAD_ATTR                path
               22  LOAD_METHOD              join
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                VSInstallDir
               28  LOAD_FAST                'default'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'guess_vc'

 L. 569        34  SETUP_FINALLY        66  'to 66'

 L. 570        36  LOAD_GLOBAL              os
               38  LOAD_METHOD              listdir
               40  LOAD_FAST                'guess_vc'
               42  CALL_METHOD_1         1  ''
               44  LOAD_CONST               -1
               46  BINARY_SUBSCR    
               48  STORE_FAST               'vc_exact_ver'

 L. 571        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              join
               56  LOAD_FAST                'guess_vc'
               58  LOAD_FAST                'vc_exact_ver'
               60  CALL_METHOD_2         2  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    34  '34'

 L. 572        66  DUP_TOP          
               68  LOAD_GLOBAL              OSError
               70  LOAD_GLOBAL              IOError
               72  LOAD_GLOBAL              IndexError
               74  BUILD_TUPLE_3         3 
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    90  'to 90'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 573        86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            78  '78'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'

Parse error at or near `POP_TOP' instruction at offset 82

        def _guess_vc_legacy(self):
            """
        Locate Visual C for versions prior to 2017
        """
            default = 'Microsoft Visual Studio %0.1f\\VC' % self.vc_ver
            return os.path.join(self.ProgramFilesx86, default)

        @property
        def WindowsSdkVersion(self):
            """
        Microsoft Windows SDK versions for specified MSVC++ version.
        """
            if self.vc_ver <= 9.0:
                return ('7.0', '6.1', '6.0a')
            if self.vc_ver == 10.0:
                return ('7.1', '7.0a')
            if self.vc_ver == 11.0:
                return ('8.0', '8.0a')
            if self.vc_ver == 12.0:
                return ('8.1', '8.1a')
            if self.vc_ver >= 14.0:
                return ('10.0', '8.1')

        @property
        def WindowsSdkLastVersion(self):
            """
        Microsoft Windows SDK last version
        """
            return self._use_last_dir_name(os.path.join(self.WindowsSdkDir, 'lib'))

        @property
        def WindowsSdkDir(self):
            """
        Microsoft Windows SDK directory.
        """
            sdkdir = ''
            for ver in self.WindowsSdkVersion:
                loc = os.path.join(self.ri.windows_sdk, 'v%s' % ver)
                sdkdir = self.ri.lookup(loc, 'installationfolder')
                if sdkdir:
                    break
            else:
                if sdkdir:
                    if not os.path.isdir(sdkdir):
                        path = os.path.join(self.ri.vc_for_python, '%0.1f' % self.vc_ver)
                        install_base = self.ri.lookup(path, 'installdir')
                        if install_base:
                            sdkdir = os.path.join(install_base, 'WinSDK')
                else:
                    for ver in sdkdir and os.path.isdir(sdkdir) or self.WindowsSdkVersion:
                        intver = ver[:ver.rfind('.')]
                        path = 'Microsoft SDKs\\Windows Kits\\%s' % intver
                        d = os.path.join(self.ProgramFiles, path)
                        if os.path.isdir(d):
                            sdkdir = d

            for ver in sdkdir and os.path.isdir(sdkdir) or self.WindowsSdkVersion:
                path = 'Microsoft SDKs\\Windows\\v%s' % ver
                d = os.path.join(self.ProgramFiles, path)
                if os.path.isdir(d):
                    sdkdir = d
                else:
                    if not sdkdir:
                        sdkdir = os.path.join(self.VCInstallDir, 'PlatformSDK')
                    return sdkdir

        @property
        def WindowsSDKExecutablePath(self):
            """
        Microsoft Windows SDK executable directory.
        """
            if self.vc_ver <= 11.0:
                netfxver = 35
                arch = ''
            else:
                netfxver = 40
                hidex86 = True if self.vc_ver <= 12.0 else False
                arch = self.pi.current_dir(x64=True, hidex86=hidex86)
            fx = 'WinSDK-NetFx%dTools%s' % (netfxver, arch.replace('\\', '-'))
            regpaths = []
            if self.vc_ver >= 14.0:
                for ver in self.NetFxSdkVersion:
                    regpaths += [os.path.join(self.ri.netfx_sdk, ver, fx)]

            for ver in self.WindowsSdkVersion:
                regpaths += [os.path.join(self.ri.windows_sdk, 'v%sA' % ver, fx)]
            else:
                for path in regpaths:
                    execpath = self.ri.lookup(path, 'installationfolder')
                    if execpath:
                        break
                    return execpath

        @property
        def FSharpInstallDir(self):
            """
        Microsoft Visual F# directory.
        """
            path = '%0.1f\\Setup\\F#' % self.vc_ver
            path = os.path.join(self.ri.visualstudio, path)
            return self.ri.lookup(path, 'productdir') or ''

        @property
        def UniversalCRTSdkDir(self):
            """
        Microsoft Universal CRT SDK directory.
        """
            if self.vc_ver >= 14.0:
                vers = ('10', '81')
            else:
                vers = ()
            for ver in vers:
                sdkdir = self.ri.lookup(self.ri.windows_kits_roots, 'kitsroot%s' % ver)
                if sdkdir:
                    break
                return sdkdir or ''

        @property
        def UniversalCRTSdkLastVersion(self):
            """
        Microsoft Universal C Runtime SDK last version
        """
            return self._use_last_dir_name(os.path.join(self.UniversalCRTSdkDir, 'lib'))

        @property
        def NetFxSdkVersion(self):
            """
        Microsoft .NET Framework SDK versions.
        """
            if self.vc_ver >= 14.0:
                return ('4.6.1', '4.6')
            return ()

        @property
        def NetFxSdkDir(self):
            """
        Microsoft .NET Framework SDK directory.
        """
            for ver in self.NetFxSdkVersion:
                loc = os.path.join(self.ri.netfx_sdk, ver)
                sdkdir = self.ri.lookup(loc, 'kitsinstallationfolder')
                if sdkdir:
                    break
                return sdkdir or ''

        @property
        def FrameworkDir32(self):
            """
        Microsoft .NET Framework 32bit directory.
        """
            guess_fw = os.path.join(self.WinDir, 'Microsoft.NET\\Framework')
            return self.ri.lookup(self.ri.vc, 'frameworkdir32') or guess_fw

        @property
        def FrameworkDir64(self):
            """
        Microsoft .NET Framework 64bit directory.
        """
            guess_fw = os.path.join(self.WinDir, 'Microsoft.NET\\Framework64')
            return self.ri.lookup(self.ri.vc, 'frameworkdir64') or guess_fw

        @property
        def FrameworkVersion32(self):
            """
        Microsoft .NET Framework 32bit versions.
        """
            return self._find_dot_net_versions(32)

        @property
        def FrameworkVersion64(self):
            """
        Microsoft .NET Framework 64bit versions.
        """
            return self._find_dot_net_versions(64)

        def _find_dot_net_versions(self, bits):
            """
        Find Microsoft .NET Framework versions.

        Parameters
        ----------
        bits: int
            Platform number of bits: 32 or 64.
        """
            reg_ver = self.ri.lookup(self.ri.vc, 'frameworkver%d' % bits)
            dot_net_dir = getattr(self, 'FrameworkDir%d' % bits)
            ver = reg_ver or self._use_last_dir_name(dot_net_dir, 'v') or ''
            if self.vc_ver >= 12.0:
                frameworkver = (
                 ver, 'v4.0')
            else:
                if self.vc_ver >= 10.0:
                    frameworkver = (
                     'v4.0.30319' if ver.lower()[:2] != 'v4' else ver,
                     'v3.5')
                else:
                    if self.vc_ver == 9.0:
                        frameworkver = ('v3.5', 'v2.0.50727')
            if self.vc_ver == 8.0:
                frameworkver = ('v3.0', 'v2.0.50727')
            return frameworkver

        def _use_last_dir_name(self, path, prefix=''):
            """
        Return name of the last dir in path or '' if no dir found.

        Parameters
        ----------
        path: str
            Use dirs in this path
        prefix: str
            Use only dirs startings by this prefix
        """
            matching_dirs = (dir_name for dir_name in reversed(os.listdir(path)) if os.path.isdir(os.path.join(path, dir_name)) if dir_name.startswith(prefix))
            return next(matching_dirs, None) or ''


    class EnvironmentInfo:
        __doc__ = '\n    Return environment variables for specified Microsoft Visual C++ version\n    and platform : Lib, Include, Path and libpath.\n\n    This function is compatible with Microsoft Visual C++ 9.0 to 14.0.\n\n    Script created by analysing Microsoft environment configuration files like\n    "vcvars[...].bat", "SetEnv.Cmd", "vcbuildtools.bat", ...\n\n    Parameters\n    ----------\n    arch: str\n        Target architecture.\n    vc_ver: float\n        Required Microsoft Visual C++ version. If not set, autodetect the last\n        version.\n    vc_min_ver: float\n        Minimum Microsoft Visual C++ version.\n    '

        def __init__(self, arch, vc_ver=None, vc_min_ver=0):
            self.pi = PlatformInfo(arch)
            self.ri = RegistryInfo(self.pi)
            self.si = SystemInfo(self.ri, vc_ver)
            if self.vc_ver < vc_min_ver:
                err = 'No suitable Microsoft Visual C++ version found'
                raise distutils.errors.DistutilsPlatformError(err)

        @property
        def vc_ver(self):
            """
        Microsoft Visual C++ version.
        """
            return self.si.vc_ver

        @property
        def VSTools(self):
            """
        Microsoft Visual Studio Tools
        """
            paths = [
             'Common7\\IDE', 'Common7\\Tools']
            if self.vc_ver >= 14.0:
                arch_subdir = self.pi.current_dir(hidex86=True, x64=True)
                paths += ['Common7\\IDE\\CommonExtensions\\Microsoft\\TestWindow']
                paths += ['Team Tools\\Performance Tools']
                paths += ['Team Tools\\Performance Tools%s' % arch_subdir]
            return [os.path.join(self.si.VSInstallDir, path) for path in paths]

        @property
        def VCIncludes(self):
            """
        Microsoft Visual C++ & Microsoft Foundation Class Includes
        """
            return [
             os.path.join(self.si.VCInstallDir, 'Include'),
             os.path.join(self.si.VCInstallDir, 'ATLMFC\\Include')]

        @property
        def VCLibraries(self):
            """
        Microsoft Visual C++ & Microsoft Foundation Class Libraries
        """
            if self.vc_ver >= 15.0:
                arch_subdir = self.pi.target_dir(x64=True)
            else:
                arch_subdir = self.pi.target_dir(hidex86=True)
            paths = [
             'Lib%s' % arch_subdir, 'ATLMFC\\Lib%s' % arch_subdir]
            if self.vc_ver >= 14.0:
                paths += ['Lib\\store%s' % arch_subdir]
            return [os.path.join(self.si.VCInstallDir, path) for path in paths]

        @property
        def VCStoreRefs(self):
            """
        Microsoft Visual C++ store references Libraries
        """
            if self.vc_ver < 14.0:
                return []
            return [
             os.path.join(self.si.VCInstallDir, 'Lib\\store\\references')]

        @property
        def VCTools(self):
            """
        Microsoft Visual C++ Tools
        """
            si = self.si
            tools = [os.path.join(si.VCInstallDir, 'VCPackages')]
            forcex86 = True if self.vc_ver <= 10.0 else False
            arch_subdir = self.pi.cross_dir(forcex86)
            if arch_subdir:
                tools += [os.path.join(si.VCInstallDir, 'Bin%s' % arch_subdir)]
            elif self.vc_ver == 14.0:
                path = 'Bin%s' % self.pi.current_dir(hidex86=True)
                tools += [os.path.join(si.VCInstallDir, path)]
            else:
                if self.vc_ver >= 15.0:
                    host_dir = 'bin\\HostX86%s' if self.pi.current_is_x86() else 'bin\\HostX64%s'
                    tools += [
                     os.path.join(si.VCInstallDir, host_dir % self.pi.target_dir(x64=True))]
                    if self.pi.current_cpu != self.pi.target_cpu:
                        tools += [
                         os.path.join(si.VCInstallDir, host_dir % self.pi.current_dir(x64=True))]
                else:
                    tools += [os.path.join(si.VCInstallDir, 'Bin')]
            return tools

        @property
        def OSLibraries(self):
            """
        Microsoft Windows SDK Libraries
        """
            if self.vc_ver <= 10.0:
                arch_subdir = self.pi.target_dir(hidex86=True, x64=True)
                return [os.path.join(self.si.WindowsSdkDir, 'Lib%s' % arch_subdir)]
            arch_subdir = self.pi.target_dir(x64=True)
            lib = os.path.join(self.si.WindowsSdkDir, 'lib')
            libver = self._sdk_subdir
            return [os.path.join(lib, '%sum%s' % (libver, arch_subdir))]

        @property
        def OSIncludes(self):
            """
        Microsoft Windows SDK Include
        """
            include = os.path.join(self.si.WindowsSdkDir, 'include')
            if self.vc_ver <= 10.0:
                return [
                 include, os.path.join(include, 'gl')]
            elif self.vc_ver >= 14.0:
                sdkver = self._sdk_subdir
            else:
                sdkver = ''
            return [
             os.path.join(include, '%sshared' % sdkver),
             os.path.join(include, '%sum' % sdkver),
             os.path.join(include, '%swinrt' % sdkver)]

        @property
        def OSLibpath(self):
            """
        Microsoft Windows SDK Libraries Paths
        """
            ref = os.path.join(self.si.WindowsSdkDir, 'References')
            libpath = []
            if self.vc_ver <= 9.0:
                libpath += self.OSLibraries
            if self.vc_ver >= 11.0:
                libpath += [os.path.join(ref, 'CommonConfiguration\\Neutral')]
            if self.vc_ver >= 14.0:
                libpath += [
                 ref,
                 os.path.join(self.si.WindowsSdkDir, 'UnionMetadata'),
                 os.path.join(ref, 'Windows.Foundation.UniversalApiContract', '1.0.0.0'),
                 os.path.join(ref, 'Windows.Foundation.FoundationContract', '1.0.0.0'),
                 os.path.join(ref, 'Windows.Networking.Connectivity.WwanContract', '1.0.0.0'),
                 os.path.join(self.si.WindowsSdkDir, 'ExtensionSDKs', 'Microsoft.VCLibs', '%0.1f' % self.vc_ver, 'References', 'CommonConfiguration', 'neutral')]
            return libpath

        @property
        def SdkTools(self):
            """
        Microsoft Windows SDK Tools
        """
            return list(self._sdk_tools())

        def _sdk_tools(self):
            """
        Microsoft Windows SDK Tools paths generator
        """
            if self.vc_ver < 15.0:
                bin_dir = 'Bin' if self.vc_ver <= 11.0 else 'Bin\\x86'
                (yield os.path.join(self.si.WindowsSdkDir, bin_dir))
            if not self.pi.current_is_x86():
                arch_subdir = self.pi.current_dir(x64=True)
                path = 'Bin%s' % arch_subdir
                (yield os.path.join(self.si.WindowsSdkDir, path))
            if self.vc_ver == 10.0 or self.vc_ver == 11.0:
                if self.pi.target_is_x86():
                    arch_subdir = ''
                else:
                    arch_subdir = self.pi.current_dir(hidex86=True, x64=True)
                path = 'Bin\\NETFX 4.0 Tools%s' % arch_subdir
                (yield os.path.join(self.si.WindowsSdkDir, path))
            else:
                if self.vc_ver >= 15.0:
                    path = os.path.join(self.si.WindowsSdkDir, 'Bin')
                    arch_subdir = self.pi.current_dir(x64=True)
                    sdkver = self.si.WindowsSdkLastVersion
                    (yield os.path.join(path, '%s%s' % (sdkver, arch_subdir)))
                if self.si.WindowsSDKExecutablePath:
                    (yield self.si.WindowsSDKExecutablePath)

        @property
        def _sdk_subdir(self):
            """
        Microsoft Windows SDK version subdir
        """
            ucrtver = self.si.WindowsSdkLastVersion
            if ucrtver:
                return '%s\\' % ucrtver
            return ''

        @property
        def SdkSetup(self):
            """
        Microsoft Windows SDK Setup
        """
            if self.vc_ver > 9.0:
                return []
            return [
             os.path.join(self.si.WindowsSdkDir, 'Setup')]

        @property
        def FxTools(self):
            """
        Microsoft .NET Framework Tools
        """
            pi = self.pi
            si = self.si
            if self.vc_ver <= 10.0:
                include32 = True
                include64 = not pi.target_is_x86() and not pi.current_is_x86()
            else:
                include32 = pi.target_is_x86() or pi.current_is_x86()
                include64 = pi.current_cpu == 'amd64' or pi.target_cpu == 'amd64'
            tools = []
            if include32:
                tools += [os.path.join(si.FrameworkDir32, ver) for ver in si.FrameworkVersion32]
            if include64:
                tools += [os.path.join(si.FrameworkDir64, ver) for ver in si.FrameworkVersion64]
            return tools

        @property
        def NetFxSDKLibraries(self):
            """
        Microsoft .Net Framework SDK Libraries
        """
            return self.vc_ver < 14.0 or self.si.NetFxSdkDir or []
            arch_subdir = self.pi.target_dir(x64=True)
            return [os.path.join(self.si.NetFxSdkDir, 'lib\\um%s' % arch_subdir)]

        @property
        def NetFxSDKIncludes(self):
            """
        Microsoft .Net Framework SDK Includes
        """
            return self.vc_ver < 14.0 or self.si.NetFxSdkDir or []
            return [
             os.path.join(self.si.NetFxSdkDir, 'include\\um')]

        @property
        def VsTDb(self):
            """
        Microsoft Visual Studio Team System Database
        """
            return [
             os.path.join(self.si.VSInstallDir, 'VSTSDB\\Deploy')]

        @property
        def MSBuild(self):
            """
        Microsoft Build Engine
        """
            if self.vc_ver < 12.0:
                return []
            elif self.vc_ver < 15.0:
                base_path = self.si.ProgramFilesx86
                arch_subdir = self.pi.current_dir(hidex86=True)
            else:
                base_path = self.si.VSInstallDir
                arch_subdir = ''
            path = 'MSBuild\\%0.1f\\bin%s' % (self.vc_ver, arch_subdir)
            build = [os.path.join(base_path, path)]
            if self.vc_ver >= 15.0:
                build += [os.path.join(base_path, path, 'Roslyn')]
            return build

        @property
        def HTMLHelpWorkshop(self):
            """
        Microsoft HTML Help Workshop
        """
            if self.vc_ver < 11.0:
                return []
            return [
             os.path.join(self.si.ProgramFilesx86, 'HTML Help Workshop')]

        @property
        def UCRTLibraries(self):
            """
        Microsoft Universal C Runtime SDK Libraries
        """
            if self.vc_ver < 14.0:
                return []
            arch_subdir = self.pi.target_dir(x64=True)
            lib = os.path.join(self.si.UniversalCRTSdkDir, 'lib')
            ucrtver = self._ucrt_subdir
            return [os.path.join(lib, '%sucrt%s' % (ucrtver, arch_subdir))]

        @property
        def UCRTIncludes(self):
            """
        Microsoft Universal C Runtime SDK Include
        """
            if self.vc_ver < 14.0:
                return []
            include = os.path.join(self.si.UniversalCRTSdkDir, 'include')
            return [os.path.join(include, '%sucrt' % self._ucrt_subdir)]

        @property
        def _ucrt_subdir(self):
            """
        Microsoft Universal C Runtime SDK version subdir
        """
            ucrtver = self.si.UniversalCRTSdkLastVersion
            if ucrtver:
                return '%s\\' % ucrtver
            return ''

        @property
        def FSharp(self):
            """
        Microsoft Visual F#
        """
            if self.vc_ver < 11.0:
                if self.vc_ver > 12.0:
                    return []
            return self.si.FSharpInstallDir

        @property
        def VCRuntimeRedist(self):
            """
        Microsoft Visual C++ runtime redistribuable dll
        """
            arch_subdir = self.pi.target_dir(x64=True)
            if self.vc_ver < 15:
                redist_path = self.si.VCInstallDir
                vcruntime = 'redist%s\\Microsoft.VC%d0.CRT\\vcruntime%d0.dll'
            else:
                redist_path = self.si.VCInstallDir.replace('\\Tools', '\\Redist')
                vcruntime = 'onecore%s\\Microsoft.VC%d0.CRT\\vcruntime%d0.dll'
            dll_ver = 14.0 if self.vc_ver == 15 else self.vc_ver
            vcruntime = vcruntime % (arch_subdir, self.vc_ver, dll_ver)
            return os.path.join(redist_path, vcruntime)

        def return_env(self, exists=True):
            """
        Return environment dict.

        Parameters
        ----------
        exists: bool
            It True, only return existing paths.
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
            if self.vc_ver >= 14:
                if os.path.isfile(self.VCRuntimeRedist):
                    env['py_vcruntime_redist'] = self.VCRuntimeRedist
            return env

        def _build_paths(self, name, spec_path_lists, exists):
            """
        Given an environment variable name and specified paths,
        return a pathsep-separated string of paths containing
        unique, extant, directories from those paths and from
        the environment variable. Raise an error if no paths
        are resolved.
        """
            spec_paths = itertools.chain.from_iterable(spec_path_lists)
            env_paths = safe_env.get(name, '').split(os.pathsep)
            paths = itertools.chain(spec_paths, env_paths)
            extant_paths = list(filter(os.path.isdir, paths)) if exists else paths
            if not extant_paths:
                msg = '%s environment variable is empty' % name.upper()
                raise distutils.errors.DistutilsPlatformError(msg)
            unique_paths = self._unique_everseen(extant_paths)
            return os.pathsep.join(unique_paths)

        def _unique_everseen(self, iterable, key=None):
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
                    (yield element)

            else:
                for element in iterable:
                    k = key(element)
                    if k not in seen:
                        seen_add(k)
                        (yield element)