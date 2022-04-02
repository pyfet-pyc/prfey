# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\command\install.py
"""distutils.command.install

Implements the Distutils 'install' command."""
import sys, os
from distutils import log
from distutils.core import Command
from distutils.debug import DEBUG
from distutils.sysconfig import get_config_vars
from distutils.errors import DistutilsPlatformError
from distutils.file_util import write_file
from distutils.util import convert_path, subst_vars, change_root
from distutils.util import get_platform
from distutils.errors import DistutilsOptionError
from site import USER_BASE
from site import USER_SITE
HAS_USER_SITE = True
WINDOWS_SCHEME = {'purelib':'$base/Lib/site-packages', 
 'platlib':'$base/Lib/site-packages', 
 'headers':'$base/Include/$dist_name', 
 'scripts':'$base/Scripts', 
 'data':'$base'}
INSTALL_SCHEMES = {'unix_prefix':{'purelib':'$base/lib/python$py_version_short/site-packages', 
  'platlib':'$platbase/lib/python$py_version_short/site-packages', 
  'headers':'$base/include/python$py_version_short$abiflags/$dist_name', 
  'scripts':'$base/bin', 
  'data':'$base'}, 
 'unix_home':{'purelib':'$base/lib/python', 
  'platlib':'$base/lib/python', 
  'headers':'$base/include/python/$dist_name', 
  'scripts':'$base/bin', 
  'data':'$base'}, 
 'nt':WINDOWS_SCHEME}
if HAS_USER_SITE:
    INSTALL_SCHEMES['nt_user'] = {'purelib':'$usersite',  'platlib':'$usersite', 
     'headers':'$userbase/Python$py_version_nodot/Include/$dist_name', 
     'scripts':'$userbase/Python$py_version_nodot/Scripts', 
     'data':'$userbase'}
    INSTALL_SCHEMES['unix_user'] = {'purelib':'$usersite', 
     'platlib':'$usersite', 
     'headers':'$userbase/include/python$py_version_short$abiflags/$dist_name', 
     'scripts':'$userbase/bin', 
     'data':'$userbase'}
SCHEME_KEYS = ('purelib', 'platlib', 'headers', 'scripts', 'data')

class install(Command):
    description = 'install everything from build directory'
    user_options = [
     ('prefix=', None, 'installation prefix'),
     ('exec-prefix=', None, '(Unix only) prefix for platform-specific files'),
     ('home=', None, '(Unix only) home directory to install under'),
     ('install-base=', None, 'base installation directory (instead of --prefix or --home)'),
     ('install-platbase=', None, 'base installation directory for platform-specific files (instead of --exec-prefix or --home)'),
     ('root=', None, 'install everything relative to this alternate root directory'),
     ('install-purelib=', None, 'installation directory for pure Python module distributions'),
     ('install-platlib=', None, 'installation directory for non-pure module distributions'),
     ('install-lib=', None, 'installation directory for all module distributions (overrides --install-purelib and --install-platlib)'),
     ('install-headers=', None, 'installation directory for C/C++ headers'),
     ('install-scripts=', None, 'installation directory for Python scripts'),
     ('install-data=', None, 'installation directory for data files'),
     ('compile', 'c', 'compile .py to .pyc [default]'),
     ('no-compile', None, "don't compile .py files"),
     ('optimize=', 'O', 'also compile with optimization: -O1 for "python -O", -O2 for "python -OO", and -O0 to disable [default: -O0]'),
     ('force', 'f', 'force installation (overwrite any existing files)'),
     ('skip-build', None, 'skip rebuilding everything (for testing/debugging)'),
     ('record=', None, 'filename in which to record list of installed files')]
    boolean_options = [
     'compile', 'force', 'skip-build']
    if HAS_USER_SITE:
        user_options.append(('user', None,
         "install in user site-package '%s'" % USER_SITE))
        boolean_options.append('user')
    negative_opt = {'no-compile': 'compile'}

    def initialize_options(self):
        """Initializes options."""
        self.prefix = None
        self.exec_prefix = None
        self.home = None
        self.user = 0
        self.install_base = None
        self.install_platbase = None
        self.root = None
        self.install_purelib = None
        self.install_platlib = None
        self.install_headers = None
        self.install_lib = None
        self.install_scripts = None
        self.install_data = None
        self.install_userbase = USER_BASE
        self.install_usersite = USER_SITE
        self.compile = None
        self.optimize = None
        self.extra_path = None
        self.install_path_file = 1
        self.force = 0
        self.skip_build = 0
        self.warn_dir = 1
        self.build_base = None
        self.build_lib = None
        self.record = None

    def finalize_options--- This code section failed: ---

 L. 240         0  LOAD_FAST                'self'
                2  LOAD_ATTR                prefix
                4  POP_JUMP_IF_TRUE     18  'to 18'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                exec_prefix
               10  POP_JUMP_IF_TRUE     18  'to 18'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                home
               16  POP_JUMP_IF_FALSE    38  'to 38'
             18_0  COME_FROM            10  '10'
             18_1  COME_FROM             4  '4'

 L. 241        18  LOAD_FAST                'self'
               20  LOAD_ATTR                install_base

 L. 240        22  POP_JUMP_IF_TRUE     30  'to 30'

 L. 241        24  LOAD_FAST                'self'
               26  LOAD_ATTR                install_platbase

 L. 240        28  POP_JUMP_IF_FALSE    38  'to 38'
             30_0  COME_FROM            22  '22'

 L. 242        30  LOAD_GLOBAL              DistutilsOptionError

 L. 243        32  LOAD_STR                 'must supply either prefix/exec-prefix/home or install-base/install-platbase -- not both'

 L. 242        34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            16  '16'

 L. 246        38  LOAD_FAST                'self'
               40  LOAD_ATTR                home
               42  POP_JUMP_IF_FALSE    64  'to 64'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                prefix
               48  POP_JUMP_IF_TRUE     56  'to 56'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                exec_prefix
               54  POP_JUMP_IF_FALSE    64  'to 64'
             56_0  COME_FROM            48  '48'

 L. 247        56  LOAD_GLOBAL              DistutilsOptionError

 L. 248        58  LOAD_STR                 'must supply either home or prefix/exec-prefix -- not both'

 L. 247        60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            42  '42'

 L. 250        64  LOAD_FAST                'self'
               66  LOAD_ATTR                user
               68  POP_JUMP_IF_FALSE   108  'to 108'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                prefix
               74  POP_JUMP_IF_TRUE    100  'to 100'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                exec_prefix
               80  POP_JUMP_IF_TRUE    100  'to 100'
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                home
               86  POP_JUMP_IF_TRUE    100  'to 100'

 L. 251        88  LOAD_FAST                'self'
               90  LOAD_ATTR                install_base

 L. 250        92  POP_JUMP_IF_TRUE    100  'to 100'

 L. 251        94  LOAD_FAST                'self'
               96  LOAD_ATTR                install_platbase

 L. 250        98  POP_JUMP_IF_FALSE   108  'to 108'
            100_0  COME_FROM            92  '92'
            100_1  COME_FROM            86  '86'
            100_2  COME_FROM            80  '80'
            100_3  COME_FROM            74  '74'

 L. 252       100  LOAD_GLOBAL              DistutilsOptionError
              102  LOAD_STR                 "can't combine user with prefix, exec_prefix/home, or install_(plat)base"
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            98  '98'
            108_1  COME_FROM            68  '68'

 L. 256       108  LOAD_GLOBAL              os
              110  LOAD_ATTR                name
              112  LOAD_STR                 'posix'
              114  COMPARE_OP               !=
              116  POP_JUMP_IF_FALSE   140  'to 140'

 L. 257       118  LOAD_FAST                'self'
              120  LOAD_ATTR                exec_prefix
              122  POP_JUMP_IF_FALSE   140  'to 140'

 L. 258       124  LOAD_FAST                'self'
              126  LOAD_METHOD              warn
              128  LOAD_STR                 'exec-prefix option ignored on this platform'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L. 259       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               exec_prefix
            140_0  COME_FROM           122  '122'
            140_1  COME_FROM           116  '116'

 L. 269       140  LOAD_FAST                'self'
              142  LOAD_METHOD              dump_dirs
              144  LOAD_STR                 'pre-finalize_{unix,other}'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 271       150  LOAD_GLOBAL              os
              152  LOAD_ATTR                name
              154  LOAD_STR                 'posix'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L. 272       160  LOAD_FAST                'self'
              162  LOAD_METHOD              finalize_unix
              164  CALL_METHOD_0         0  ''
              166  POP_TOP          
              168  JUMP_FORWARD        178  'to 178'
            170_0  COME_FROM           158  '158'

 L. 274       170  LOAD_FAST                'self'
              172  LOAD_METHOD              finalize_other
              174  CALL_METHOD_0         0  ''
              176  POP_TOP          
            178_0  COME_FROM           168  '168'

 L. 276       178  LOAD_FAST                'self'
              180  LOAD_METHOD              dump_dirs
              182  LOAD_STR                 'post-finalize_{unix,other}()'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 283       188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                version
              192  LOAD_METHOD              split
              194  CALL_METHOD_0         0  ''
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  STORE_FAST               'py_version'

 L. 284       202  LOAD_GLOBAL              get_config_vars
              204  LOAD_STR                 'prefix'
              206  LOAD_STR                 'exec_prefix'
              208  CALL_FUNCTION_2       2  ''
              210  UNPACK_SEQUENCE_2     2 
              212  STORE_FAST               'prefix'
              214  STORE_FAST               'exec_prefix'

 L. 285       216  SETUP_FINALLY       228  'to 228'

 L. 286       218  LOAD_GLOBAL              sys
              220  LOAD_ATTR                abiflags
              222  STORE_FAST               'abiflags'
              224  POP_BLOCK        
              226  JUMP_FORWARD        252  'to 252'
            228_0  COME_FROM_FINALLY   216  '216'

 L. 287       228  DUP_TOP          
              230  LOAD_GLOBAL              AttributeError
              232  COMPARE_OP               exception-match
              234  POP_JUMP_IF_FALSE   250  'to 250'
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          

 L. 289       242  LOAD_STR                 ''
              244  STORE_FAST               'abiflags'
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           234  '234'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           226  '226'

 L. 290       252  LOAD_FAST                'self'
              254  LOAD_ATTR                distribution
              256  LOAD_METHOD              get_name
              258  CALL_METHOD_0         0  ''

 L. 291       260  LOAD_FAST                'self'
              262  LOAD_ATTR                distribution
              264  LOAD_METHOD              get_version
              266  CALL_METHOD_0         0  ''

 L. 292       268  LOAD_FAST                'self'
              270  LOAD_ATTR                distribution
              272  LOAD_METHOD              get_fullname
              274  CALL_METHOD_0         0  ''

 L. 293       276  LOAD_FAST                'py_version'

 L. 294       278  LOAD_STR                 '%d.%d'
              280  LOAD_GLOBAL              sys
              282  LOAD_ATTR                version_info
              284  LOAD_CONST               None
              286  LOAD_CONST               2
              288  BUILD_SLICE_2         2 
              290  BINARY_SUBSCR    
              292  BINARY_MODULO    

 L. 295       294  LOAD_STR                 '%d%d'
              296  LOAD_GLOBAL              sys
              298  LOAD_ATTR                version_info
              300  LOAD_CONST               None
              302  LOAD_CONST               2
              304  BUILD_SLICE_2         2 
              306  BINARY_SUBSCR    
              308  BINARY_MODULO    

 L. 296       310  LOAD_FAST                'prefix'

 L. 297       312  LOAD_FAST                'prefix'

 L. 298       314  LOAD_FAST                'exec_prefix'

 L. 299       316  LOAD_FAST                'exec_prefix'

 L. 300       318  LOAD_FAST                'abiflags'

 L. 290       320  LOAD_CONST               ('dist_name', 'dist_version', 'dist_fullname', 'py_version', 'py_version_short', 'py_version_nodot', 'sys_prefix', 'prefix', 'sys_exec_prefix', 'exec_prefix', 'abiflags')
              322  BUILD_CONST_KEY_MAP_11    11 
              324  LOAD_FAST                'self'
              326  STORE_ATTR               config_vars

 L. 303       328  LOAD_GLOBAL              HAS_USER_SITE
          330_332  POP_JUMP_IF_FALSE   358  'to 358'

 L. 304       334  LOAD_FAST                'self'
              336  LOAD_ATTR                install_userbase
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                config_vars
              342  LOAD_STR                 'userbase'
              344  STORE_SUBSCR     

 L. 305       346  LOAD_FAST                'self'
              348  LOAD_ATTR                install_usersite
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                config_vars
              354  LOAD_STR                 'usersite'
              356  STORE_SUBSCR     
            358_0  COME_FROM           330  '330'

 L. 307       358  LOAD_FAST                'self'
              360  LOAD_METHOD              expand_basedirs
              362  CALL_METHOD_0         0  ''
              364  POP_TOP          

 L. 309       366  LOAD_FAST                'self'
              368  LOAD_METHOD              dump_dirs
              370  LOAD_STR                 'post-expand_basedirs()'
              372  CALL_METHOD_1         1  ''
              374  POP_TOP          

 L. 313       376  LOAD_FAST                'self'
              378  LOAD_ATTR                install_base
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                config_vars
              384  LOAD_STR                 'base'
              386  STORE_SUBSCR     

 L. 314       388  LOAD_FAST                'self'
              390  LOAD_ATTR                install_platbase
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                config_vars
              396  LOAD_STR                 'platbase'
              398  STORE_SUBSCR     

 L. 316       400  LOAD_GLOBAL              DEBUG
          402_404  POP_JUMP_IF_FALSE   436  'to 436'

 L. 317       406  LOAD_CONST               0
              408  LOAD_CONST               ('pprint',)
              410  IMPORT_NAME              pprint
              412  IMPORT_FROM              pprint
              414  STORE_FAST               'pprint'
              416  POP_TOP          

 L. 318       418  LOAD_GLOBAL              print
              420  LOAD_STR                 'config vars:'
              422  CALL_FUNCTION_1       1  ''
              424  POP_TOP          

 L. 319       426  LOAD_FAST                'pprint'
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                config_vars
              432  CALL_FUNCTION_1       1  ''
              434  POP_TOP          
            436_0  COME_FROM           402  '402'

 L. 323       436  LOAD_FAST                'self'
              438  LOAD_METHOD              expand_dirs
              440  CALL_METHOD_0         0  ''
              442  POP_TOP          

 L. 325       444  LOAD_FAST                'self'
              446  LOAD_METHOD              dump_dirs
              448  LOAD_STR                 'post-expand_dirs()'
              450  CALL_METHOD_1         1  ''
              452  POP_TOP          

 L. 328       454  LOAD_FAST                'self'
              456  LOAD_ATTR                user
          458_460  POP_JUMP_IF_FALSE   470  'to 470'

 L. 329       462  LOAD_FAST                'self'
              464  LOAD_METHOD              create_home_path
              466  CALL_METHOD_0         0  ''
              468  POP_TOP          
            470_0  COME_FROM           458  '458'

 L. 335       470  LOAD_FAST                'self'
              472  LOAD_ATTR                install_lib
              474  LOAD_CONST               None
              476  COMPARE_OP               is
          478_480  POP_JUMP_IF_FALSE   510  'to 510'

 L. 336       482  LOAD_FAST                'self'
              484  LOAD_ATTR                distribution
              486  LOAD_ATTR                ext_modules
          488_490  POP_JUMP_IF_FALSE   502  'to 502'

 L. 337       492  LOAD_FAST                'self'
              494  LOAD_ATTR                install_platlib
              496  LOAD_FAST                'self'
              498  STORE_ATTR               install_lib
              500  JUMP_FORWARD        510  'to 510'
            502_0  COME_FROM           488  '488'

 L. 339       502  LOAD_FAST                'self'
              504  LOAD_ATTR                install_purelib
              506  LOAD_FAST                'self'
              508  STORE_ATTR               install_lib
            510_0  COME_FROM           500  '500'
            510_1  COME_FROM           478  '478'

 L. 344       510  LOAD_FAST                'self'
              512  LOAD_METHOD              convert_paths
              514  LOAD_STR                 'lib'
              516  LOAD_STR                 'purelib'
              518  LOAD_STR                 'platlib'

 L. 345       520  LOAD_STR                 'scripts'

 L. 345       522  LOAD_STR                 'data'

 L. 345       524  LOAD_STR                 'headers'

 L. 346       526  LOAD_STR                 'userbase'

 L. 346       528  LOAD_STR                 'usersite'

 L. 344       530  CALL_METHOD_8         8  ''
              532  POP_TOP          

 L. 353       534  LOAD_FAST                'self'
              536  LOAD_METHOD              handle_extra_path
              538  CALL_METHOD_0         0  ''
              540  POP_TOP          

 L. 354       542  LOAD_FAST                'self'
              544  LOAD_ATTR                install_lib
              546  LOAD_FAST                'self'
              548  STORE_ATTR               install_libbase

 L. 355       550  LOAD_GLOBAL              os
              552  LOAD_ATTR                path
              554  LOAD_METHOD              join
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                install_lib
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                extra_dirs
              564  CALL_METHOD_2         2  ''
              566  LOAD_FAST                'self'
              568  STORE_ATTR               install_lib

 L. 359       570  LOAD_FAST                'self'
              572  LOAD_ATTR                root
              574  LOAD_CONST               None
              576  COMPARE_OP               is-not
          578_580  POP_JUMP_IF_FALSE   604  'to 604'

 L. 360       582  LOAD_FAST                'self'
              584  LOAD_METHOD              change_roots
              586  LOAD_STR                 'libbase'
              588  LOAD_STR                 'lib'
              590  LOAD_STR                 'purelib'
              592  LOAD_STR                 'platlib'

 L. 361       594  LOAD_STR                 'scripts'

 L. 361       596  LOAD_STR                 'data'

 L. 361       598  LOAD_STR                 'headers'

 L. 360       600  CALL_METHOD_7         7  ''
              602  POP_TOP          
            604_0  COME_FROM           578  '578'

 L. 363       604  LOAD_FAST                'self'
              606  LOAD_METHOD              dump_dirs
              608  LOAD_STR                 'after prepending root'
              610  CALL_METHOD_1         1  ''
              612  POP_TOP          

 L. 366       614  LOAD_FAST                'self'
              616  LOAD_METHOD              set_undefined_options
              618  LOAD_STR                 'build'

 L. 367       620  LOAD_CONST               ('build_base', 'build_base')

 L. 368       622  LOAD_CONST               ('build_lib', 'build_lib')

 L. 366       624  CALL_METHOD_3         3  ''
              626  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 624

    def dump_dirs(self, msg):
        """Dumps the list of user options."""
        if not DEBUG:
            return
        from distutils.fancy_getopt import longopt_xlate
        log.debug(msg + ':')
        for opt in self.user_options:
            opt_name = opt[0]
            if opt_name[(-1)] == '=':
                opt_name = opt_name[0:-1]
            elif opt_name in self.negative_opt:
                opt_name = self.negative_opt[opt_name]
                opt_name = opt_name.translate(longopt_xlate)
                val = not getattrselfopt_name
            else:
                opt_name = opt_name.translate(longopt_xlate)
                val = getattrselfopt_name
            log.debug'  %s: %s'opt_nameval

    def finalize_unix--- This code section failed: ---

 L. 394         0  LOAD_FAST                'self'
                2  LOAD_ATTR                install_base
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                install_platbase
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE    92  'to 92'
             20_0  COME_FROM             8  '8'

 L. 395        20  LOAD_FAST                'self'
               22  LOAD_ATTR                install_lib
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    50  'to 50'

 L. 396        30  LOAD_FAST                'self'
               32  LOAD_ATTR                install_purelib
               34  LOAD_CONST               None
               36  COMPARE_OP               is

 L. 395        38  POP_JUMP_IF_FALSE    50  'to 50'

 L. 397        40  LOAD_FAST                'self'
               42  LOAD_ATTR                install_platlib
               44  LOAD_CONST               None
               46  COMPARE_OP               is

 L. 395        48  POP_JUMP_IF_TRUE     80  'to 80'
             50_0  COME_FROM            38  '38'
             50_1  COME_FROM            28  '28'

 L. 398        50  LOAD_FAST                'self'
               52  LOAD_ATTR                install_headers
               54  LOAD_CONST               None
               56  COMPARE_OP               is

 L. 395        58  POP_JUMP_IF_TRUE     80  'to 80'

 L. 399        60  LOAD_FAST                'self'
               62  LOAD_ATTR                install_scripts
               64  LOAD_CONST               None
               66  COMPARE_OP               is

 L. 395        68  POP_JUMP_IF_TRUE     80  'to 80'

 L. 400        70  LOAD_FAST                'self'
               72  LOAD_ATTR                install_data
               74  LOAD_CONST               None
               76  COMPARE_OP               is

 L. 395        78  POP_JUMP_IF_FALSE    88  'to 88'
             80_0  COME_FROM            68  '68'
             80_1  COME_FROM            58  '58'
             80_2  COME_FROM            48  '48'

 L. 401        80  LOAD_GLOBAL              DistutilsOptionError

 L. 402        82  LOAD_STR                 'install-base or install-platbase supplied, but installation scheme is incomplete'

 L. 401        84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
             88_0  COME_FROM            78  '78'

 L. 404        88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            18  '18'

 L. 406        92  LOAD_FAST                'self'
               94  LOAD_ATTR                user
               96  POP_JUMP_IF_FALSE   142  'to 142'

 L. 407        98  LOAD_FAST                'self'
              100  LOAD_ATTR                install_userbase
              102  LOAD_CONST               None
              104  COMPARE_OP               is
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L. 408       108  LOAD_GLOBAL              DistutilsPlatformError

 L. 409       110  LOAD_STR                 'User base directory is not specified'

 L. 408       112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           106  '106'

 L. 410       116  LOAD_FAST                'self'
              118  LOAD_ATTR                install_userbase
              120  DUP_TOP          
              122  LOAD_FAST                'self'
              124  STORE_ATTR               install_base
              126  LOAD_FAST                'self'
              128  STORE_ATTR               install_platbase

 L. 411       130  LOAD_FAST                'self'
              132  LOAD_METHOD              select_scheme
              134  LOAD_STR                 'unix_user'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  JUMP_FORWARD        286  'to 286'
            142_0  COME_FROM            96  '96'

 L. 412       142  LOAD_FAST                'self'
              144  LOAD_ATTR                home
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   178  'to 178'

 L. 413       152  LOAD_FAST                'self'
              154  LOAD_ATTR                home
              156  DUP_TOP          
              158  LOAD_FAST                'self'
              160  STORE_ATTR               install_base
              162  LOAD_FAST                'self'
              164  STORE_ATTR               install_platbase

 L. 414       166  LOAD_FAST                'self'
              168  LOAD_METHOD              select_scheme
              170  LOAD_STR                 'unix_home'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_FORWARD        286  'to 286'
            178_0  COME_FROM           150  '150'

 L. 416       178  LOAD_FAST                'self'
              180  LOAD_ATTR                prefix
              182  LOAD_CONST               None
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   240  'to 240'

 L. 417       188  LOAD_FAST                'self'
              190  LOAD_ATTR                exec_prefix
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   206  'to 206'

 L. 418       198  LOAD_GLOBAL              DistutilsOptionError

 L. 419       200  LOAD_STR                 'must not supply exec-prefix without prefix'

 L. 418       202  CALL_FUNCTION_1       1  ''
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           196  '196'

 L. 421       206  LOAD_GLOBAL              os
              208  LOAD_ATTR                path
              210  LOAD_METHOD              normpath
              212  LOAD_GLOBAL              sys
              214  LOAD_ATTR                prefix
              216  CALL_METHOD_1         1  ''
              218  LOAD_FAST                'self'
              220  STORE_ATTR               prefix

 L. 422       222  LOAD_GLOBAL              os
              224  LOAD_ATTR                path
              226  LOAD_METHOD              normpath
              228  LOAD_GLOBAL              sys
              230  LOAD_ATTR                exec_prefix
              232  CALL_METHOD_1         1  ''
              234  LOAD_FAST                'self'
              236  STORE_ATTR               exec_prefix
              238  JUMP_FORWARD        260  'to 260'
            240_0  COME_FROM           186  '186'

 L. 425       240  LOAD_FAST                'self'
              242  LOAD_ATTR                exec_prefix
              244  LOAD_CONST               None
              246  COMPARE_OP               is
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 426       252  LOAD_FAST                'self'
              254  LOAD_ATTR                prefix
              256  LOAD_FAST                'self'
              258  STORE_ATTR               exec_prefix
            260_0  COME_FROM           248  '248'
            260_1  COME_FROM           238  '238'

 L. 428       260  LOAD_FAST                'self'
              262  LOAD_ATTR                prefix
              264  LOAD_FAST                'self'
              266  STORE_ATTR               install_base

 L. 429       268  LOAD_FAST                'self'
              270  LOAD_ATTR                exec_prefix
              272  LOAD_FAST                'self'
              274  STORE_ATTR               install_platbase

 L. 430       276  LOAD_FAST                'self'
              278  LOAD_METHOD              select_scheme
              280  LOAD_STR                 'unix_prefix'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
            286_0  COME_FROM           176  '176'
            286_1  COME_FROM           140  '140'

Parse error at or near `COME_FROM' instruction at offset 286_0

    def finalize_other(self):
        """Finalizes options for non-posix platforms"""
        if self.user:
            if self.install_userbase is None:
                raise DistutilsPlatformError('User base directory is not specified')
            self.install_base = self.install_platbase = self.install_userbase
            self.select_scheme(os.name + '_user')
        else:
            if self.home is not None:
                self.install_base = self.install_platbase = self.home
                self.select_scheme('unix_home')
            else:
                if self.prefix is None:
                    self.prefix = os.path.normpath(sys.prefix)
                self.install_base = self.install_platbase = self.prefix
        try:
            self.select_scheme(os.name)
        except KeyError:
            raise DistutilsPlatformError("I don't know how to install stuff on '%s'" % os.name)

    def select_scheme(self, name):
        """Sets the install directories by applying the install schemes."""
        scheme = INSTALL_SCHEMES[name]
        for key in SCHEME_KEYS:
            attrname = 'install_' + key
            if getattrselfattrname is None:
                setattr(self, attrname, scheme[key])

    def _expand_attrs(self, attrs):
        for attr in attrs:
            val = getattrselfattr
            if val is not None and not os.name == 'posix':
                if os.name == 'nt':
                    val = os.path.expanduser(val)
                val = subst_varsvalself.config_vars
                setattr(self, attr, val)

    def expand_basedirs(self):
        """Calls `os.path.expanduser` on install_base, install_platbase and
        root."""
        self._expand_attrs(['install_base', 'install_platbase', 'root'])

    def expand_dirs(self):
        """Calls `os.path.expanduser` on install dirs."""
        self._expand_attrs(['install_purelib', 'install_platlib',
         'install_lib', 'install_headers',
         'install_scripts', 'install_data'])

    def convert_paths(self, *names):
        """Call `convert_path` over `names`."""
        for name in names:
            attr = 'install_' + name
            setattr(self, attr, convert_path(getattrselfattr))

    def handle_extra_path(self):
        """Set `path_file` and `extra_dirs` using `extra_path`."""
        if self.extra_path is None:
            self.extra_path = self.distribution.extra_path
        elif self.extra_path is not None:
            log.warn('Distribution option extra_path is deprecated. See issue27919 for details.')
            if isinstanceself.extra_pathstr:
                self.extra_path = self.extra_path.split(',')
            elif len(self.extra_path) == 1:
                path_file = extra_dirs = self.extra_path[0]
            else:
                if len(self.extra_path) == 2:
                    path_file, extra_dirs = self.extra_path
                else:
                    raise DistutilsOptionError("'extra_path' option must be a list, tuple, or comma-separated string with 1 or 2 elements")
            extra_dirs = convert_path(extra_dirs)
        else:
            path_file = None
            extra_dirs = ''
        self.path_file = path_file
        self.extra_dirs = extra_dirs

    def change_roots(self, *names):
        """Change the install directories pointed by name using root."""
        for name in names:
            attr = 'install_' + name
            setattr(self, attr, change_rootself.rootgetattrselfattr)

    def create_home_path(self):
        """Create directories under ~."""
        if not self.user:
            return
        home = convert_path(os.path.expanduser('~'))
        for name, path in self.config_vars.items:
            if path.startswith(home):
                os.path.isdir(path) or self.debug_print("os.makedirs('%s', 0o700)" % path)
                os.makedirspath448

    def run(self):
        """Runs the command."""
        if not self.skip_build:
            self.run_command('build')
            build_plat = self.distribution.get_command_obj('build').plat_name
            if self.warn_dir:
                if build_plat != get_platform():
                    raise DistutilsPlatformError("Can't install when cross-compiling")
        else:
            for cmd_name in self.get_sub_commands:
                self.run_command(cmd_name)
            else:
                if self.path_file:
                    self.create_path_file
                else:
                    if self.record:
                        outputs = self.get_outputs
                        if self.root:
                            root_len = len(self.root)
                            for counter in range(len(outputs)):
                                outputs[counter] = outputs[counter][root_len:]

                        else:
                            self.executewrite_file(
                             self.record, outputs)("writing list of installed files to '%s'" % self.record)
                    sys_path = mapos.path.normpathsys.path
                    sys_path = mapos.path.normcasesys_path
                    install_lib = os.path.normcase(os.path.normpath(self.install_lib))
                    if not (self.warn_dir):
                        if install_lib not in sys_path:
                            log.debug"modules installed to '%s', which is not in Python's module search path (sys.path) -- you'll have to change the search path yourself"self.install_lib

    def create_path_file(self):
        """Creates the .pth file"""
        filename = os.path.joinself.install_libbase(self.path_file + '.pth')
        if self.install_path_file:
            self.executewrite_file(
             filename, [self.extra_dirs])('creating %s' % filename)
        else:
            self.warn("path file '%s' not created" % filename)

    def get_outputs(self):
        """Assembles the outputs of all the sub-commands."""
        outputs = []
        for cmd_name in self.get_sub_commands:
            cmd = self.get_finalized_command(cmd_name)
            for filename in cmd.get_outputs:
                if filename not in outputs:
                    outputs.append(filename)
            else:
                if self.path_file:
                    if self.install_path_file:
                        outputs.append(os.path.joinself.install_libbase(self.path_file + '.pth'))
                return outputs

    def get_inputs(self):
        """Returns the inputs of all the sub-commands"""
        inputs = []
        for cmd_name in self.get_sub_commands:
            cmd = self.get_finalized_command(cmd_name)
            inputs.extend(cmd.get_inputs)
        else:
            return inputs

    def has_lib(self):
        """Returns true if the current distribution has any Python
        modules to install."""
        return self.distribution.has_pure_modules or self.distribution.has_ext_modules

    def has_headers(self):
        """Returns true if the current distribution has any headers to
        install."""
        return self.distribution.has_headers

    def has_scripts(self):
        """Returns true if the current distribution has any scripts to.
        install."""
        return self.distribution.has_scripts

    def has_data(self):
        """Returns true if the current distribution has any data to.
        install."""
        return self.distribution.has_data_files

    sub_commands = [
     (
      'install_lib', has_lib),
     (
      'install_headers', has_headers),
     (
      'install_scripts', has_scripts),
     (
      'install_data', has_data),
     (
      'install_egg_info', lambda self: True)]