# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\util.py
"""distutils.util

Miscellaneous utility functions -- anything that doesn't fit into
one of the other *util.py modules.
"""
import os, re, importlib.util, string, sys
from distutils.errors import DistutilsPlatformError
from distutils.dep_util import newer
import distutils.spawn as spawn
from distutils import log
from distutils.errors import DistutilsByteCompileError

def get_host_platform--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                name
                4  LOAD_STR                 'nt'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    70  'to 70'

 L.  39        10  LOAD_STR                 'amd64'
               12  LOAD_GLOBAL              sys
               14  LOAD_ATTR                version
               16  LOAD_METHOD              lower
               18  CALL_METHOD_0         0  ''
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L.  40        24  LOAD_STR                 'win-amd64'
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.  41        28  LOAD_STR                 '(arm)'
               30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                version
               34  LOAD_METHOD              lower
               36  CALL_METHOD_0         0  ''
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    46  'to 46'

 L.  42        42  LOAD_STR                 'win-arm32'
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L.  43        46  LOAD_STR                 '(arm64)'
               48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                version
               52  LOAD_METHOD              lower
               54  CALL_METHOD_0         0  ''
               56  <118>                 0  ''
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L.  44        60  LOAD_STR                 'win-arm64'
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L.  45        64  LOAD_GLOBAL              sys
               66  LOAD_ATTR                platform
               68  RETURN_VALUE     
             70_0  COME_FROM             8  '8'

 L.  48        70  LOAD_STR                 '_PYTHON_HOST_PLATFORM'
               72  LOAD_GLOBAL              os
               74  LOAD_ATTR                environ
               76  <118>                 0  ''
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L.  49        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                environ
               84  LOAD_STR                 '_PYTHON_HOST_PLATFORM'
               86  BINARY_SUBSCR    
               88  RETURN_VALUE     
             90_0  COME_FROM            78  '78'

 L.  51        90  LOAD_GLOBAL              os
               92  LOAD_ATTR                name
               94  LOAD_STR                 'posix'
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_TRUE    110  'to 110'
              100  LOAD_GLOBAL              hasattr
              102  LOAD_GLOBAL              os
              104  LOAD_STR                 'uname'
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_TRUE    116  'to 116'
            110_0  COME_FROM            98  '98'

 L.  54       110  LOAD_GLOBAL              sys
              112  LOAD_ATTR                platform
              114  RETURN_VALUE     
            116_0  COME_FROM           108  '108'

 L.  58       116  LOAD_GLOBAL              os
              118  LOAD_METHOD              uname
              120  CALL_METHOD_0         0  ''
              122  UNPACK_SEQUENCE_5     5 
              124  STORE_FAST               'osname'
              126  STORE_FAST               'host'
              128  STORE_FAST               'release'
              130  STORE_FAST               'version'
              132  STORE_FAST               'machine'

 L.  62       134  LOAD_FAST                'osname'
              136  LOAD_METHOD              lower
              138  CALL_METHOD_0         0  ''
              140  LOAD_METHOD              replace
              142  LOAD_STR                 '/'
              144  LOAD_STR                 ''
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'osname'

 L.  63       150  LOAD_FAST                'machine'
              152  LOAD_METHOD              replace
              154  LOAD_STR                 ' '
              156  LOAD_STR                 '_'
              158  CALL_METHOD_2         2  ''
              160  STORE_FAST               'machine'

 L.  64       162  LOAD_FAST                'machine'
              164  LOAD_METHOD              replace
              166  LOAD_STR                 '/'
              168  LOAD_STR                 '-'
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'machine'

 L.  66       174  LOAD_FAST                'osname'
              176  LOAD_CONST               None
              178  LOAD_CONST               5
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  LOAD_STR                 'linux'
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L.  70       190  LOAD_STR                 '%s-%s'
              192  LOAD_FAST                'osname'
              194  LOAD_FAST                'machine'
              196  BUILD_TUPLE_2         2 
              198  BINARY_MODULO    
              200  RETURN_VALUE     
            202_0  COME_FROM           188  '188'

 L.  71       202  LOAD_FAST                'osname'
              204  LOAD_CONST               None
              206  LOAD_CONST               5
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_STR                 'sunos'
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   300  'to 300'

 L.  72       220  LOAD_FAST                'release'
              222  LOAD_CONST               0
              224  BINARY_SUBSCR    
              226  LOAD_STR                 '5'
              228  COMPARE_OP               >=
          230_232  POP_JUMP_IF_FALSE   460  'to 460'

 L.  73       234  LOAD_STR                 'solaris'
              236  STORE_FAST               'osname'

 L.  74       238  LOAD_STR                 '%d.%s'
              240  LOAD_GLOBAL              int
              242  LOAD_FAST                'release'
              244  LOAD_CONST               0
              246  BINARY_SUBSCR    
              248  CALL_FUNCTION_1       1  ''
              250  LOAD_CONST               3
              252  BINARY_SUBTRACT  
              254  LOAD_FAST                'release'
              256  LOAD_CONST               2
              258  LOAD_CONST               None
              260  BUILD_SLICE_2         2 
              262  BINARY_SUBSCR    
              264  BUILD_TUPLE_2         2 
              266  BINARY_MODULO    
              268  STORE_FAST               'release'

 L.  78       270  LOAD_STR                 '32bit'
              272  LOAD_STR                 '64bit'
              274  LOAD_CONST               (2147483647, 9223372036854775807)
              276  BUILD_CONST_KEY_MAP_2     2 
              278  STORE_FAST               'bitness'

 L.  79       280  LOAD_FAST                'machine'
              282  LOAD_STR                 '.%s'
              284  LOAD_FAST                'bitness'
              286  LOAD_GLOBAL              sys
              288  LOAD_ATTR                maxsize
              290  BINARY_SUBSCR    
              292  BINARY_MODULO    
              294  INPLACE_ADD      
              296  STORE_FAST               'machine'
              298  JUMP_FORWARD        460  'to 460'
            300_0  COME_FROM           216  '216'

 L.  81       300  LOAD_FAST                'osname'
              302  LOAD_CONST               None
              304  LOAD_CONST               3
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_STR                 'aix'
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   336  'to 336'

 L.  82       318  LOAD_CONST               0
              320  LOAD_CONST               ('aix_platform',)
              322  IMPORT_NAME              _aix_support
              324  IMPORT_FROM              aix_platform
              326  STORE_FAST               'aix_platform'
              328  POP_TOP          

 L.  83       330  LOAD_FAST                'aix_platform'
              332  CALL_FUNCTION_0       0  ''
              334  RETURN_VALUE     
            336_0  COME_FROM           314  '314'

 L.  84       336  LOAD_FAST                'osname'
              338  LOAD_CONST               None
              340  LOAD_CONST               6
              342  BUILD_SLICE_2         2 
              344  BINARY_SUBSCR    
              346  LOAD_STR                 'cygwin'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   398  'to 398'

 L.  85       354  LOAD_STR                 'cygwin'
              356  STORE_FAST               'osname'

 L.  86       358  LOAD_GLOBAL              re
              360  LOAD_METHOD              compile
              362  LOAD_STR                 '[\\d.]+'
              364  LOAD_GLOBAL              re
              366  LOAD_ATTR                ASCII
              368  CALL_METHOD_2         2  ''
              370  STORE_FAST               'rel_re'

 L.  87       372  LOAD_FAST                'rel_re'
              374  LOAD_METHOD              match
              376  LOAD_FAST                'release'
              378  CALL_METHOD_1         1  ''
              380  STORE_FAST               'm'

 L.  88       382  LOAD_FAST                'm'
          384_386  POP_JUMP_IF_FALSE   460  'to 460'

 L.  89       388  LOAD_FAST                'm'
              390  LOAD_METHOD              group
              392  CALL_METHOD_0         0  ''
              394  STORE_FAST               'release'
              396  JUMP_FORWARD        460  'to 460'
            398_0  COME_FROM           350  '350'

 L.  90       398  LOAD_FAST                'osname'
              400  LOAD_CONST               None
              402  LOAD_CONST               6
              404  BUILD_SLICE_2         2 
              406  BINARY_SUBSCR    
              408  LOAD_STR                 'darwin'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   460  'to 460'

 L.  91       416  LOAD_CONST               0
              418  LOAD_CONST               None
              420  IMPORT_NAME              _osx_support
              422  STORE_FAST               '_osx_support'
              424  LOAD_CONST               0
              426  LOAD_CONST               None
              428  IMPORT_NAME_ATTR         distutils.sysconfig
              430  STORE_FAST               'distutils'

 L.  92       432  LOAD_FAST                '_osx_support'
              434  LOAD_METHOD              get_platform_osx

 L.  93       436  LOAD_FAST                'distutils'
              438  LOAD_ATTR                sysconfig
              440  LOAD_METHOD              get_config_vars
              442  CALL_METHOD_0         0  ''

 L.  94       444  LOAD_FAST                'osname'
              446  LOAD_FAST                'release'
              448  LOAD_FAST                'machine'

 L.  92       450  CALL_METHOD_4         4  ''
              452  UNPACK_SEQUENCE_3     3 
              454  STORE_FAST               'osname'
              456  STORE_FAST               'release'
              458  STORE_FAST               'machine'
            460_0  COME_FROM           412  '412'
            460_1  COME_FROM           396  '396'
            460_2  COME_FROM           384  '384'
            460_3  COME_FROM           298  '298'
            460_4  COME_FROM           230  '230'

 L.  96       460  LOAD_STR                 '%s-%s-%s'
              462  LOAD_FAST                'osname'
              464  LOAD_FAST                'release'
              466  LOAD_FAST                'machine'
              468  BUILD_TUPLE_3         3 
              470  BINARY_MODULO    
              472  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def get_platform():
    if os.name == 'nt':
        TARGET_TO_PLAT = {'x86':'win32',  'x64':'win-amd64', 
         'arm':'win-arm32'}
        return TARGET_TO_PLAT.getos.environ.get'VSCMD_ARG_TGT_ARCH' or get_host_platform
    return get_host_platform


def convert_path--- This code section failed: ---

 L. 118         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                sep
                4  LOAD_STR                 '/'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 119        10  LOAD_FAST                'pathname'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 120        14  LOAD_FAST                'pathname'
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L. 121        18  LOAD_FAST                'pathname'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 122        22  LOAD_FAST                'pathname'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  LOAD_STR                 '/'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 123        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 "path '%s' cannot be absolute"
               38  LOAD_FAST                'pathname'
               40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            32  '32'

 L. 124        46  LOAD_FAST                'pathname'
               48  LOAD_CONST               -1
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '/'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    70  'to 70'

 L. 125        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 "path '%s' cannot end with '/'"
               62  LOAD_FAST                'pathname'
               64  BINARY_MODULO    
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            56  '56'

 L. 127        70  LOAD_FAST                'pathname'
               72  LOAD_METHOD              split
               74  LOAD_STR                 '/'
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'paths'
             80_0  COME_FROM            98  '98'

 L. 128        80  LOAD_STR                 '.'
               82  LOAD_FAST                'paths'
               84  <118>                 0  ''
               86  POP_JUMP_IF_FALSE   100  'to 100'

 L. 129        88  LOAD_FAST                'paths'
               90  LOAD_METHOD              remove
               92  LOAD_STR                 '.'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            80  'to 80'
            100_0  COME_FROM            86  '86'

 L. 130       100  LOAD_FAST                'paths'
              102  POP_JUMP_IF_TRUE    110  'to 110'

 L. 131       104  LOAD_GLOBAL              os
              106  LOAD_ATTR                curdir
              108  RETURN_VALUE     
            110_0  COME_FROM           102  '102'

 L. 132       110  LOAD_GLOBAL              os
              112  LOAD_ATTR                path
              114  LOAD_ATTR                join
              116  LOAD_FAST                'paths'
              118  CALL_FUNCTION_EX      0  'positional arguments only'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 84


def change_root(new_root, pathname):
    """Return 'pathname' with 'new_root' prepended.  If 'pathname' is
    relative, this is equivalent to "os.path.join(new_root,pathname)".
    Otherwise, it requires making 'pathname' relative and then joining the
    two, which is tricky on DOS/Windows and Mac OS.
    """
    if os.name == 'posix':
        if not os.path.isabspathname:
            return os.path.joinnew_rootpathname
        return os.path.joinnew_rootpathname[1:]
    else:
        if os.name == 'nt':
            drive, path = os.path.splitdrivepathname
            if path[0] == '\\':
                path = path[1:]
            return os.path.joinnew_rootpath
        raise DistutilsPlatformError("nothing known about platform '%s'" % os.name)


_environ_checked = 0

def check_environ--- This code section failed: ---

 L. 169         0  LOAD_GLOBAL              _environ_checked
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L. 170         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 172         8  LOAD_GLOBAL              os
               10  LOAD_ATTR                name
               12  LOAD_STR                 'posix'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    88  'to 88'
               18  LOAD_STR                 'HOME'
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                environ
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    88  'to 88'

 L. 173        28  SETUP_FINALLY        66  'to 66'

 L. 174        30  LOAD_CONST               0
               32  LOAD_CONST               None
               34  IMPORT_NAME              pwd
               36  STORE_FAST               'pwd'

 L. 175        38  LOAD_FAST                'pwd'
               40  LOAD_METHOD              getpwuid
               42  LOAD_GLOBAL              os
               44  LOAD_METHOD              getuid
               46  CALL_METHOD_0         0  ''
               48  CALL_METHOD_1         1  ''
               50  LOAD_CONST               5
               52  BINARY_SUBSCR    
               54  LOAD_GLOBAL              os
               56  LOAD_ATTR                environ
               58  LOAD_STR                 'HOME'
               60  STORE_SUBSCR     
               62  POP_BLOCK        
               64  JUMP_FORWARD         88  'to 88'
             66_0  COME_FROM_FINALLY    28  '28'

 L. 176        66  DUP_TOP          
               68  LOAD_GLOBAL              ImportError
               70  LOAD_GLOBAL              KeyError
               72  BUILD_TUPLE_2         2 
               74  <121>                86  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 179        82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
               86  <48>             
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            64  '64'
             88_2  COME_FROM            26  '26'
             88_3  COME_FROM            16  '16'

 L. 181        88  LOAD_STR                 'PLAT'
               90  LOAD_GLOBAL              os
               92  LOAD_ATTR                environ
               94  <118>                 1  ''
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 182        98  LOAD_GLOBAL              get_platform
              100  CALL_FUNCTION_0       0  ''
              102  LOAD_GLOBAL              os
              104  LOAD_ATTR                environ
              106  LOAD_STR                 'PLAT'
              108  STORE_SUBSCR     
            110_0  COME_FROM            96  '96'

 L. 184       110  LOAD_CONST               1
              112  STORE_GLOBAL             _environ_checked

Parse error at or near `<118>' instruction at offset 24


def subst_vars--- This code section failed: ---

 L. 196         0  LOAD_GLOBAL              check_environ
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 197         6  LOAD_FAST                'local_vars'
                8  BUILD_TUPLE_1         1 
               10  LOAD_CODE                <code_object _subst>
               12  LOAD_STR                 'subst_vars.<locals>._subst'
               14  MAKE_FUNCTION_1          'default'
               16  STORE_FAST               '_subst'

 L. 204        18  SETUP_FINALLY        36  'to 36'

 L. 205        20  LOAD_GLOBAL              re
               22  LOAD_METHOD              sub
               24  LOAD_STR                 '\\$([a-zA-Z_][a-zA-Z_0-9]*)'
               26  LOAD_FAST                '_subst'
               28  LOAD_FAST                's'
               30  CALL_METHOD_3         3  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    18  '18'

 L. 206        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  <121>                82  ''
               42  POP_TOP          
               44  STORE_FAST               'var'
               46  POP_TOP          
               48  SETUP_FINALLY        74  'to 74'

 L. 207        50  LOAD_GLOBAL              ValueError
               52  LOAD_STR                 "invalid variable '$%s'"
               54  LOAD_FAST                'var'
               56  BINARY_MODULO    
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_BLOCK        
               64  POP_EXCEPT       
               66  LOAD_CONST               None
               68  STORE_FAST               'var'
               70  DELETE_FAST              'var'
               72  JUMP_FORWARD         84  'to 84'
             74_0  COME_FROM_FINALLY    48  '48'
               74  LOAD_CONST               None
               76  STORE_FAST               'var'
               78  DELETE_FAST              'var'
               80  <48>             
               82  <48>             
             84_0  COME_FROM            72  '72'

Parse error at or near `<121>' instruction at offset 40


def grok_environment_error(exc, prefix='error: '):
    return prefix + str(exc)


_wordchars_re = _squote_re = _dquote_re = None

def _init_regex():
    global _dquote_re
    global _squote_re
    global _wordchars_re
    _wordchars_re = re.compile('[^\\\\\\\'\\"%s ]*' % string.whitespace)
    _squote_re = re.compile"'(?:[^'\\\\]|\\\\.)*'"
    _dquote_re = re.compile'"(?:[^"\\\\]|\\\\.)*"'


def split_quoted--- This code section failed: ---

 L. 241         0  LOAD_GLOBAL              _wordchars_re
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_GLOBAL              _init_regex
               10  CALL_FUNCTION_0       0  ''
               12  POP_TOP          
             14_0  COME_FROM             6  '6'

 L. 243        14  LOAD_FAST                's'
               16  LOAD_METHOD              strip
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               's'

 L. 244        22  BUILD_LIST_0          0 
               24  STORE_FAST               'words'

 L. 245        26  LOAD_CONST               0
               28  STORE_FAST               'pos'
             30_0  COME_FROM           382  '382'
             30_1  COME_FROM           366  '366'

 L. 247        30  LOAD_FAST                's'
            32_34  POP_JUMP_IF_FALSE   384  'to 384'

 L. 248        36  LOAD_GLOBAL              _wordchars_re
               38  LOAD_METHOD              match
               40  LOAD_FAST                's'
               42  LOAD_FAST                'pos'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'm'

 L. 249        48  LOAD_FAST                'm'
               50  LOAD_METHOD              end
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'end'

 L. 250        56  LOAD_FAST                'end'
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                's'
               62  CALL_FUNCTION_1       1  ''
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    90  'to 90'

 L. 251        68  LOAD_FAST                'words'
               70  LOAD_METHOD              append
               72  LOAD_FAST                's'
               74  LOAD_CONST               None
               76  LOAD_FAST                'end'
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L. 252     86_88  JUMP_FORWARD        384  'to 384'
             90_0  COME_FROM            66  '66'

 L. 254        90  LOAD_FAST                's'
               92  LOAD_FAST                'end'
               94  BINARY_SUBSCR    
               96  LOAD_GLOBAL              string
               98  LOAD_ATTR                whitespace
              100  <118>                 0  ''
              102  POP_JUMP_IF_FALSE   144  'to 144'

 L. 255       104  LOAD_FAST                'words'
              106  LOAD_METHOD              append
              108  LOAD_FAST                's'
              110  LOAD_CONST               None
              112  LOAD_FAST                'end'
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 256       122  LOAD_FAST                's'
              124  LOAD_FAST                'end'
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BINARY_SUBSCR    
              132  LOAD_METHOD              lstrip
              134  CALL_METHOD_0         0  ''
              136  STORE_FAST               's'

 L. 257       138  LOAD_CONST               0
              140  STORE_FAST               'pos'
              142  JUMP_FORWARD        356  'to 356'
            144_0  COME_FROM           102  '102'

 L. 259       144  LOAD_FAST                's'
              146  LOAD_FAST                'end'
              148  BINARY_SUBSCR    
              150  LOAD_STR                 '\\'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   194  'to 194'

 L. 261       156  LOAD_FAST                's'
              158  LOAD_CONST               None
              160  LOAD_FAST                'end'
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  LOAD_FAST                's'
              168  LOAD_FAST                'end'
              170  LOAD_CONST               1
              172  BINARY_ADD       
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  BINARY_ADD       
              182  STORE_FAST               's'

 L. 262       184  LOAD_FAST                'end'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  STORE_FAST               'pos'
              192  JUMP_FORWARD        356  'to 356'
            194_0  COME_FROM           154  '154'

 L. 265       194  LOAD_FAST                's'
              196  LOAD_FAST                'end'
              198  BINARY_SUBSCR    
              200  LOAD_STR                 "'"
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L. 266       206  LOAD_GLOBAL              _squote_re
              208  LOAD_METHOD              match
              210  LOAD_FAST                's'
              212  LOAD_FAST                'end'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'm'
              218  JUMP_FORWARD        262  'to 262'
            220_0  COME_FROM           204  '204'

 L. 267       220  LOAD_FAST                's'
              222  LOAD_FAST                'end'
              224  BINARY_SUBSCR    
              226  LOAD_STR                 '"'
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L. 268       232  LOAD_GLOBAL              _dquote_re
              234  LOAD_METHOD              match
              236  LOAD_FAST                's'
              238  LOAD_FAST                'end'
              240  CALL_METHOD_2         2  ''
              242  STORE_FAST               'm'
              244  JUMP_FORWARD        262  'to 262'
            246_0  COME_FROM           230  '230'

 L. 270       246  LOAD_GLOBAL              RuntimeError
              248  LOAD_STR                 "this can't happen (bad char '%c')"
              250  LOAD_FAST                's'
              252  LOAD_FAST                'end'
              254  BINARY_SUBSCR    
              256  BINARY_MODULO    
              258  CALL_FUNCTION_1       1  ''
              260  RAISE_VARARGS_1       1  'exception instance'
            262_0  COME_FROM           244  '244'
            262_1  COME_FROM           218  '218'

 L. 272       262  LOAD_FAST                'm'
              264  LOAD_CONST               None
              266  <117>                 0  ''
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 273       272  LOAD_GLOBAL              ValueError
              274  LOAD_STR                 'bad string (mismatched %s quotes?)'
              276  LOAD_FAST                's'
              278  LOAD_FAST                'end'
              280  BINARY_SUBSCR    
              282  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  ''
              286  RAISE_VARARGS_1       1  'exception instance'
            288_0  COME_FROM           268  '268'

 L. 275       288  LOAD_FAST                'm'
              290  LOAD_METHOD              span
              292  CALL_METHOD_0         0  ''
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'beg'
              298  STORE_FAST               'end'

 L. 276       300  LOAD_FAST                's'
              302  LOAD_CONST               None
              304  LOAD_FAST                'beg'
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_FAST                's'
              312  LOAD_FAST                'beg'
              314  LOAD_CONST               1
              316  BINARY_ADD       
              318  LOAD_FAST                'end'
              320  LOAD_CONST               1
              322  BINARY_SUBTRACT  
              324  BUILD_SLICE_2         2 
              326  BINARY_SUBSCR    
              328  BINARY_ADD       
              330  LOAD_FAST                's'
              332  LOAD_FAST                'end'
              334  LOAD_CONST               None
              336  BUILD_SLICE_2         2 
              338  BINARY_SUBSCR    
              340  BINARY_ADD       
              342  STORE_FAST               's'

 L. 277       344  LOAD_FAST                'm'
              346  LOAD_METHOD              end
              348  CALL_METHOD_0         0  ''
              350  LOAD_CONST               2
              352  BINARY_SUBTRACT  
              354  STORE_FAST               'pos'
            356_0  COME_FROM           192  '192'
            356_1  COME_FROM           142  '142'

 L. 279       356  LOAD_FAST                'pos'
              358  LOAD_GLOBAL              len
              360  LOAD_FAST                's'
              362  CALL_FUNCTION_1       1  ''
              364  COMPARE_OP               >=
              366  POP_JUMP_IF_FALSE_BACK    30  'to 30'

 L. 280       368  LOAD_FAST                'words'
              370  LOAD_METHOD              append
              372  LOAD_FAST                's'
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          

 L. 281   378_380  JUMP_FORWARD        384  'to 384'
              382  JUMP_BACK            30  'to 30'
            384_0  COME_FROM           378  '378'
            384_1  COME_FROM            86  '86'
            384_2  COME_FROM            32  '32'

 L. 283       384  LOAD_FAST                'words'
              386  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def execute--- This code section failed: ---

 L. 297         0  LOAD_FAST                'msg'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    54  'to 54'

 L. 298         8  LOAD_STR                 '%s%r'
               10  LOAD_FAST                'func'
               12  LOAD_ATTR                __name__
               14  LOAD_FAST                'args'
               16  BUILD_TUPLE_2         2 
               18  BINARY_MODULO    
               20  STORE_FAST               'msg'

 L. 299        22  LOAD_FAST                'msg'
               24  LOAD_CONST               -2
               26  LOAD_CONST               None
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  LOAD_STR                 ',)'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    54  'to 54'

 L. 300        38  LOAD_FAST                'msg'
               40  LOAD_CONST               0
               42  LOAD_CONST               -2
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  LOAD_STR                 ')'
               50  BINARY_ADD       
               52  STORE_FAST               'msg'
             54_0  COME_FROM            36  '36'
             54_1  COME_FROM             6  '6'

 L. 302        54  LOAD_GLOBAL              log
               56  LOAD_METHOD              info
               58  LOAD_FAST                'msg'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 303        64  LOAD_FAST                'dry_run'
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L. 304        68  LOAD_FAST                'func'
               70  LOAD_FAST                'args'
               72  CALL_FUNCTION_EX      0  'positional arguments only'
               74  POP_TOP          
             76_0  COME_FROM            66  '66'

Parse error at or near `None' instruction at offset -1


def strtobool--- This code section failed: ---

 L. 314         0  LOAD_FAST                'val'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'val'

 L. 315         8  LOAD_FAST                'val'
               10  LOAD_CONST               ('y', 'yes', 't', 'true', 'on', '1')
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 316        16  LOAD_CONST               1
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 317        20  LOAD_FAST                'val'
               22  LOAD_CONST               ('n', 'no', 'f', 'false', 'off', '0')
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 318        28  LOAD_CONST               0
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 320        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'invalid truth value %r'
               36  LOAD_FAST                'val'
               38  BUILD_TUPLE_1         1 
               40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 12


def byte_compile--- This code section failed: ---

 L. 359         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              subprocess
                6  STORE_FAST               'subprocess'

 L. 362         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                dont_write_bytecode
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 363        14  LOAD_GLOBAL              DistutilsByteCompileError
               16  LOAD_STR                 'byte-compiling is disabled.'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L. 375        22  LOAD_FAST                'direct'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L. 376        30  LOAD_CONST               True
               32  JUMP_IF_FALSE_OR_POP    40  'to 40'
               34  LOAD_FAST                'optimize'
               36  LOAD_CONST               0
               38  COMPARE_OP               ==
             40_0  COME_FROM            32  '32'
               40  STORE_FAST               'direct'
             42_0  COME_FROM            28  '28'

 L. 380        42  LOAD_FAST                'direct'
            44_46  POP_JUMP_IF_TRUE    342  'to 342'

 L. 381        48  SETUP_FINALLY        78  'to 78'

 L. 382        50  LOAD_CONST               0
               52  LOAD_CONST               ('mkstemp',)
               54  IMPORT_NAME              tempfile
               56  IMPORT_FROM              mkstemp
               58  STORE_FAST               'mkstemp'
               60  POP_TOP          

 L. 383        62  LOAD_FAST                'mkstemp'
               64  LOAD_STR                 '.py'
               66  CALL_FUNCTION_1       1  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'script_fd'
               72  STORE_FAST               'script_name'
               74  POP_BLOCK        
               76  JUMP_FORWARD        122  'to 122'
             78_0  COME_FROM_FINALLY    48  '48'

 L. 384        78  DUP_TOP          
               80  LOAD_GLOBAL              ImportError
               82  <121>               120  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 385        90  LOAD_CONST               0
               92  LOAD_CONST               ('mktemp',)
               94  IMPORT_NAME              tempfile
               96  IMPORT_FROM              mktemp
               98  STORE_FAST               'mktemp'
              100  POP_TOP          

 L. 386       102  LOAD_CONST               None
              104  LOAD_FAST                'mktemp'
              106  LOAD_STR                 '.py'
              108  CALL_FUNCTION_1       1  ''
              110  ROT_TWO          
              112  STORE_FAST               'script_fd'
              114  STORE_FAST               'script_name'
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            76  '76'

 L. 387       122  LOAD_GLOBAL              log
              124  LOAD_METHOD              info
              126  LOAD_STR                 "writing byte-compilation script '%s'"
              128  LOAD_FAST                'script_name'
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          

 L. 388       134  LOAD_FAST                'dry_run'
          136_138  POP_JUMP_IF_TRUE    270  'to 270'

 L. 389       140  LOAD_FAST                'script_fd'
              142  LOAD_CONST               None
              144  <117>                 1  ''
              146  POP_JUMP_IF_FALSE   162  'to 162'

 L. 390       148  LOAD_GLOBAL              os
              150  LOAD_METHOD              fdopen
              152  LOAD_FAST                'script_fd'
              154  LOAD_STR                 'w'
              156  CALL_METHOD_2         2  ''
              158  STORE_FAST               'script'
              160  JUMP_FORWARD        172  'to 172'
            162_0  COME_FROM           146  '146'

 L. 392       162  LOAD_GLOBAL              open
              164  LOAD_FAST                'script_name'
              166  LOAD_STR                 'w'
              168  CALL_FUNCTION_2       2  ''
              170  STORE_FAST               'script'
            172_0  COME_FROM           160  '160'

 L. 394       172  LOAD_FAST                'script'
              174  SETUP_WITH          252  'to 252'
              176  POP_TOP          

 L. 395       178  LOAD_FAST                'script'
              180  LOAD_METHOD              write
              182  LOAD_STR                 'from distutils.util import byte_compile\nfiles = [\n'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 414       188  LOAD_FAST                'script'
              190  LOAD_METHOD              write
              192  LOAD_STR                 ',\n'
              194  LOAD_METHOD              join
              196  LOAD_GLOBAL              map
              198  LOAD_GLOBAL              repr
              200  LOAD_FAST                'py_files'
              202  CALL_FUNCTION_2       2  ''
              204  CALL_METHOD_1         1  ''
              206  LOAD_STR                 ']\n'
              208  BINARY_ADD       
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L. 415       214  LOAD_FAST                'script'
              216  LOAD_METHOD              write
              218  LOAD_STR                 '\nbyte_compile(files, optimize=%r, force=%r,\n             prefix=%r, base_dir=%r,\n             verbose=%r, dry_run=0,\n             direct=1)\n'

 L. 420       220  LOAD_FAST                'optimize'
              222  LOAD_FAST                'force'
              224  LOAD_FAST                'prefix'
              226  LOAD_FAST                'base_dir'
              228  LOAD_FAST                'verbose'
              230  BUILD_TUPLE_5         5 

 L. 415       232  BINARY_MODULO    
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          
              238  POP_BLOCK        
              240  LOAD_CONST               None
              242  DUP_TOP          
              244  DUP_TOP          
              246  CALL_FUNCTION_3       3  ''
              248  POP_TOP          
              250  JUMP_FORWARD        270  'to 270'
            252_0  COME_FROM_WITH      174  '174'
              252  <49>             
          254_256  POP_JUMP_IF_TRUE    260  'to 260'
              258  <48>             
            260_0  COME_FROM           254  '254'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          
              266  POP_EXCEPT       
              268  POP_TOP          
            270_0  COME_FROM           250  '250'
            270_1  COME_FROM           136  '136'

 L. 422       270  LOAD_GLOBAL              sys
              272  LOAD_ATTR                executable
              274  BUILD_LIST_1          1 
              276  STORE_FAST               'cmd'

 L. 423       278  LOAD_FAST                'cmd'
              280  LOAD_METHOD              extend
              282  LOAD_FAST                'subprocess'
              284  LOAD_METHOD              _optim_args_from_interpreter_flags
              286  CALL_METHOD_0         0  ''
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          

 L. 424       292  LOAD_FAST                'cmd'
              294  LOAD_METHOD              append
              296  LOAD_FAST                'script_name'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          

 L. 425       302  LOAD_GLOBAL              spawn
              304  LOAD_FAST                'cmd'
              306  LOAD_FAST                'dry_run'
              308  LOAD_CONST               ('dry_run',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  POP_TOP          

 L. 426       314  LOAD_GLOBAL              execute
              316  LOAD_GLOBAL              os
              318  LOAD_ATTR                remove
              320  LOAD_FAST                'script_name'
              322  BUILD_TUPLE_1         1 
              324  LOAD_STR                 'removing %s'
              326  LOAD_FAST                'script_name'
              328  BINARY_MODULO    

 L. 427       330  LOAD_FAST                'dry_run'

 L. 426       332  LOAD_CONST               ('dry_run',)
              334  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              336  POP_TOP          
          338_340  JUMP_FORWARD        614  'to 614'
            342_0  COME_FROM            44  '44'

 L. 434       342  LOAD_CONST               0
              344  LOAD_CONST               ('compile',)
              346  IMPORT_NAME              py_compile
              348  IMPORT_FROM              compile
              350  STORE_FAST               'compile'
              352  POP_TOP          

 L. 436       354  LOAD_FAST                'py_files'
              356  GET_ITER         
            358_0  COME_FROM           610  '610'
            358_1  COME_FROM           594  '594'
            358_2  COME_FROM           540  '540'
            358_3  COME_FROM           380  '380'
              358  FOR_ITER            614  'to 614'
              360  STORE_FAST               'file'

 L. 437       362  LOAD_FAST                'file'
              364  LOAD_CONST               -3
              366  LOAD_CONST               None
              368  BUILD_SLICE_2         2 
              370  BINARY_SUBSCR    
              372  LOAD_STR                 '.py'
              374  COMPARE_OP               !=
          376_378  POP_JUMP_IF_FALSE   384  'to 384'

 L. 440   380_382  JUMP_BACK           358  'to 358'
            384_0  COME_FROM           376  '376'

 L. 445       384  LOAD_FAST                'optimize'
              386  LOAD_CONST               0
              388  COMPARE_OP               >=
          390_392  POP_JUMP_IF_FALSE   430  'to 430'

 L. 446       394  LOAD_FAST                'optimize'
              396  LOAD_CONST               0
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   408  'to 408'
              404  LOAD_STR                 ''
              406  JUMP_FORWARD        410  'to 410'
            408_0  COME_FROM           400  '400'
              408  LOAD_FAST                'optimize'
            410_0  COME_FROM           406  '406'
              410  STORE_FAST               'opt'

 L. 447       412  LOAD_GLOBAL              importlib
              414  LOAD_ATTR                util
              416  LOAD_ATTR                cache_from_source

 L. 448       418  LOAD_FAST                'file'
              420  LOAD_FAST                'opt'

 L. 447       422  LOAD_CONST               ('optimization',)
              424  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              426  STORE_FAST               'cfile'
              428  JUMP_FORWARD        442  'to 442'
            430_0  COME_FROM           390  '390'

 L. 450       430  LOAD_GLOBAL              importlib
              432  LOAD_ATTR                util
              434  LOAD_METHOD              cache_from_source
              436  LOAD_FAST                'file'
              438  CALL_METHOD_1         1  ''
              440  STORE_FAST               'cfile'
            442_0  COME_FROM           428  '428'

 L. 451       442  LOAD_FAST                'file'
              444  STORE_FAST               'dfile'

 L. 452       446  LOAD_FAST                'prefix'
          448_450  POP_JUMP_IF_FALSE   506  'to 506'

 L. 453       452  LOAD_FAST                'file'
              454  LOAD_CONST               None
              456  LOAD_GLOBAL              len
              458  LOAD_FAST                'prefix'
              460  CALL_FUNCTION_1       1  ''
              462  BUILD_SLICE_2         2 
              464  BINARY_SUBSCR    
              466  LOAD_FAST                'prefix'
              468  COMPARE_OP               !=
          470_472  POP_JUMP_IF_FALSE   490  'to 490'

 L. 454       474  LOAD_GLOBAL              ValueError
              476  LOAD_STR                 "invalid prefix: filename %r doesn't start with %r"

 L. 455       478  LOAD_FAST                'file'
              480  LOAD_FAST                'prefix'
              482  BUILD_TUPLE_2         2 

 L. 454       484  BINARY_MODULO    
              486  CALL_FUNCTION_1       1  ''
              488  RAISE_VARARGS_1       1  'exception instance'
            490_0  COME_FROM           470  '470'

 L. 456       490  LOAD_FAST                'dfile'
              492  LOAD_GLOBAL              len
              494  LOAD_FAST                'prefix'
              496  CALL_FUNCTION_1       1  ''
              498  LOAD_CONST               None
              500  BUILD_SLICE_2         2 
              502  BINARY_SUBSCR    
              504  STORE_FAST               'dfile'
            506_0  COME_FROM           448  '448'

 L. 457       506  LOAD_FAST                'base_dir'
          508_510  POP_JUMP_IF_FALSE   526  'to 526'

 L. 458       512  LOAD_GLOBAL              os
              514  LOAD_ATTR                path
              516  LOAD_METHOD              join
              518  LOAD_FAST                'base_dir'
              520  LOAD_FAST                'dfile'
              522  CALL_METHOD_2         2  ''
              524  STORE_FAST               'dfile'
            526_0  COME_FROM           508  '508'

 L. 460       526  LOAD_GLOBAL              os
              528  LOAD_ATTR                path
              530  LOAD_METHOD              basename
              532  LOAD_FAST                'cfile'
              534  CALL_METHOD_1         1  ''
              536  STORE_FAST               'cfile_base'

 L. 461       538  LOAD_FAST                'direct'
          540_542  POP_JUMP_IF_FALSE_BACK   358  'to 358'

 L. 462       544  LOAD_FAST                'force'
          546_548  POP_JUMP_IF_TRUE    562  'to 562'
              550  LOAD_GLOBAL              newer
              552  LOAD_FAST                'file'
              554  LOAD_FAST                'cfile'
              556  CALL_FUNCTION_2       2  ''
          558_560  POP_JUMP_IF_FALSE   596  'to 596'
            562_0  COME_FROM           546  '546'

 L. 463       562  LOAD_GLOBAL              log
              564  LOAD_METHOD              info
              566  LOAD_STR                 'byte-compiling %s to %s'
              568  LOAD_FAST                'file'
              570  LOAD_FAST                'cfile_base'
              572  CALL_METHOD_3         3  ''
              574  POP_TOP          

 L. 464       576  LOAD_FAST                'dry_run'
          578_580  POP_JUMP_IF_TRUE    610  'to 610'

 L. 465       582  LOAD_FAST                'compile'
              584  LOAD_FAST                'file'
              586  LOAD_FAST                'cfile'
              588  LOAD_FAST                'dfile'
              590  CALL_FUNCTION_3       3  ''
              592  POP_TOP          
              594  JUMP_BACK           358  'to 358'
            596_0  COME_FROM           558  '558'

 L. 467       596  LOAD_GLOBAL              log
              598  LOAD_METHOD              debug
              600  LOAD_STR                 'skipping byte-compilation of %s to %s'

 L. 468       602  LOAD_FAST                'file'
              604  LOAD_FAST                'cfile_base'

 L. 467       606  CALL_METHOD_3         3  ''
              608  POP_TOP          
            610_0  COME_FROM           578  '578'
          610_612  JUMP_BACK           358  'to 358'
            614_0  COME_FROM           358  '358'
            614_1  COME_FROM           338  '338'

Parse error at or near `<117>' instruction at offset 26


def rfc822_escape(header):
    """Return a version of the string escaped for inclusion in an
    RFC-822 header, by ensuring there are 8 spaces space after each newline.
    """
    lines = header.split'\n'
    sep = '\n        '
    return sep.joinlines


def run_2to3--- This code section failed: ---

 L. 489         0  LOAD_FAST                'files'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 490         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 493         8  LOAD_CONST               0
               10  LOAD_CONST               ('RefactoringTool', 'get_fixers_from_package')
               12  IMPORT_NAME_ATTR         lib2to3.refactor
               14  IMPORT_FROM              RefactoringTool
               16  STORE_FAST               'RefactoringTool'
               18  IMPORT_FROM              get_fixers_from_package
               20  STORE_FAST               'get_fixers_from_package'
               22  POP_TOP          

 L. 494        24  LOAD_BUILD_CLASS 
               26  LOAD_CODE                <code_object DistutilsRefactoringTool>
               28  LOAD_STR                 'DistutilsRefactoringTool'
               30  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               32  LOAD_STR                 'DistutilsRefactoringTool'
               34  LOAD_FAST                'RefactoringTool'
               36  CALL_FUNCTION_3       3  ''
               38  STORE_FAST               'DistutilsRefactoringTool'

 L. 504        40  LOAD_FAST                'fixer_names'
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 505        48  LOAD_FAST                'get_fixers_from_package'
               50  LOAD_STR                 'lib2to3.fixes'
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'fixer_names'
             56_0  COME_FROM            46  '46'

 L. 506        56  LOAD_FAST                'DistutilsRefactoringTool'
               58  LOAD_FAST                'fixer_names'
               60  LOAD_FAST                'options'
               62  LOAD_CONST               ('options',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  STORE_FAST               'r'

 L. 507        68  LOAD_FAST                'r'
               70  LOAD_ATTR                refactor
               72  LOAD_FAST                'files'
               74  LOAD_CONST               True
               76  LOAD_CONST               ('write',)
               78  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               80  POP_TOP          

Parse error at or near `<117>' instruction at offset 44


def copydir_run_2to3--- This code section failed: ---

 L. 516         0  LOAD_CONST               0
                2  LOAD_CONST               ('mkpath',)
                4  IMPORT_NAME_ATTR         distutils.dir_util
                6  IMPORT_FROM              mkpath
                8  STORE_FAST               'mkpath'
               10  POP_TOP          

 L. 517        12  LOAD_CONST               0
               14  LOAD_CONST               ('copy_file',)
               16  IMPORT_NAME_ATTR         distutils.file_util
               18  IMPORT_FROM              copy_file
               20  STORE_FAST               'copy_file'
               22  POP_TOP          

 L. 518        24  LOAD_CONST               0
               26  LOAD_CONST               ('FileList',)
               28  IMPORT_NAME_ATTR         distutils.filelist
               30  IMPORT_FROM              FileList
               32  STORE_FAST               'FileList'
               34  POP_TOP          

 L. 519        36  LOAD_FAST                'FileList'
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'filelist'

 L. 520        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              getcwd
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'curdir'

 L. 521        50  LOAD_GLOBAL              os
               52  LOAD_METHOD              chdir
               54  LOAD_FAST                'src'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 522        60  SETUP_FINALLY        84  'to 84'

 L. 523        62  LOAD_FAST                'filelist'
               64  LOAD_METHOD              findall
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          
               70  POP_BLOCK        

 L. 525        72  LOAD_GLOBAL              os
               74  LOAD_METHOD              chdir
               76  LOAD_FAST                'curdir'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_FORWARD         96  'to 96'
             84_0  COME_FROM_FINALLY    60  '60'
               84  LOAD_GLOBAL              os
               86  LOAD_METHOD              chdir
               88  LOAD_FAST                'curdir'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  <48>             
             96_0  COME_FROM            82  '82'

 L. 526        96  LOAD_FAST                'filelist'
               98  LOAD_ATTR                allfiles
              100  LOAD_FAST                'filelist'
              102  LOAD_ATTR                files
              104  LOAD_CONST               None
              106  LOAD_CONST               None
              108  BUILD_SLICE_2         2 
              110  STORE_SUBSCR     

 L. 527       112  LOAD_FAST                'template'
              114  POP_JUMP_IF_FALSE   154  'to 154'

 L. 528       116  LOAD_FAST                'template'
              118  LOAD_METHOD              splitlines
              120  CALL_METHOD_0         0  ''
              122  GET_ITER         
            124_0  COME_FROM           152  '152'
            124_1  COME_FROM           140  '140'
              124  FOR_ITER            154  'to 154'
              126  STORE_FAST               'line'

 L. 529       128  LOAD_FAST                'line'
              130  LOAD_METHOD              strip
              132  CALL_METHOD_0         0  ''
              134  STORE_FAST               'line'

 L. 530       136  LOAD_FAST                'line'
              138  POP_JUMP_IF_TRUE    142  'to 142'
              140  JUMP_BACK           124  'to 124'
            142_0  COME_FROM           138  '138'

 L. 531       142  LOAD_FAST                'filelist'
              144  LOAD_METHOD              process_template_line
              146  LOAD_FAST                'line'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  JUMP_BACK           124  'to 124'
            154_0  COME_FROM           124  '124'
            154_1  COME_FROM           114  '114'

 L. 532       154  BUILD_LIST_0          0 
              156  STORE_FAST               'copied'

 L. 533       158  LOAD_FAST                'filelist'
              160  LOAD_ATTR                files
              162  GET_ITER         
            164_0  COME_FROM           240  '240'
            164_1  COME_FROM           228  '228'
              164  FOR_ITER            242  'to 242'
              166  STORE_FAST               'filename'

 L. 534       168  LOAD_GLOBAL              os
              170  LOAD_ATTR                path
              172  LOAD_METHOD              join
              174  LOAD_FAST                'dest'
              176  LOAD_FAST                'filename'
              178  CALL_METHOD_2         2  ''
              180  STORE_FAST               'outname'

 L. 535       182  LOAD_FAST                'mkpath'
              184  LOAD_GLOBAL              os
              186  LOAD_ATTR                path
              188  LOAD_METHOD              dirname
              190  LOAD_FAST                'outname'
              192  CALL_METHOD_1         1  ''
              194  CALL_FUNCTION_1       1  ''
              196  POP_TOP          

 L. 536       198  LOAD_FAST                'copy_file'
              200  LOAD_GLOBAL              os
              202  LOAD_ATTR                path
              204  LOAD_METHOD              join
              206  LOAD_FAST                'src'
              208  LOAD_FAST                'filename'
              210  CALL_METHOD_2         2  ''
              212  LOAD_FAST                'outname'
              214  LOAD_CONST               1
              216  LOAD_CONST               ('update',)
              218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              220  STORE_FAST               'res'

 L. 537       222  LOAD_FAST                'res'
              224  LOAD_CONST               1
              226  BINARY_SUBSCR    
              228  POP_JUMP_IF_FALSE_BACK   164  'to 164'
              230  LOAD_FAST                'copied'
              232  LOAD_METHOD              append
              234  LOAD_FAST                'outname'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
              240  JUMP_BACK           164  'to 164'
            242_0  COME_FROM           164  '164'

 L. 538       242  LOAD_GLOBAL              run_2to3
              244  LOAD_LISTCOMP            '<code_object <listcomp>>'
              246  LOAD_STR                 'copydir_run_2to3.<locals>.<listcomp>'
              248  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              250  LOAD_FAST                'copied'
              252  GET_ITER         
              254  CALL_FUNCTION_1       1  ''

 L. 539       256  LOAD_FAST                'fixer_names'
              258  LOAD_FAST                'options'
              260  LOAD_FAST                'explicit'

 L. 538       262  LOAD_CONST               ('fixer_names', 'options', 'explicit')
              264  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              266  POP_TOP          

 L. 540       268  LOAD_FAST                'copied'
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 80


class Mixin2to3:
    __doc__ = 'Mixin class for commands that run 2to3.\n    To configure 2to3, setup scripts may either change\n    the class variables, or inherit from individual commands\n    to override how 2to3 is invoked.'
    fixer_names = None
    options = None
    explicit = None

    def run_2to3(self, files):
        return run_2to3(files, self.fixer_names, self.options, self.explicit)


# global _environ_checked ## Warning: Unused global