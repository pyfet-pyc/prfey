# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\pkgconfig.py
import sys, os, subprocess
from .error import PkgConfigError

def merge_flags--- This code section failed: ---

 L.  14         0  LOAD_FAST                'cfg2'
                2  LOAD_METHOD              items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM           100  '100'
              8_1  COME_FROM            32  '32'
                8  FOR_ITER            102  'to 102'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'key'
               14  STORE_FAST               'value'

 L.  15        16  LOAD_FAST                'key'
               18  LOAD_FAST                'cfg1'
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L.  16        24  LOAD_FAST                'value'
               26  LOAD_FAST                'cfg1'
               28  LOAD_FAST                'key'
               30  STORE_SUBSCR     
               32  JUMP_BACK             8  'to 8'
             34_0  COME_FROM            22  '22'

 L.  18        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'cfg1'
               38  LOAD_FAST                'key'
               40  BINARY_SUBSCR    
               42  LOAD_GLOBAL              list
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     62  'to 62'

 L.  19        48  LOAD_GLOBAL              TypeError
               50  LOAD_STR                 'cfg1[%r] should be a list of strings'
               52  LOAD_FAST                'key'
               54  BUILD_TUPLE_1         1 
               56  BINARY_MODULO    
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            46  '46'

 L.  20        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'value'
               66  LOAD_GLOBAL              list
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_TRUE     86  'to 86'

 L.  21        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 'cfg2[%r] should be a list of strings'
               76  LOAD_FAST                'key'
               78  BUILD_TUPLE_1         1 
               80  BINARY_MODULO    
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            70  '70'

 L.  22        86  LOAD_FAST                'cfg1'
               88  LOAD_FAST                'key'
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              extend
               94  LOAD_FAST                'value'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_BACK             8  'to 8'
            102_0  COME_FROM             8  '8'

 L.  23       102  LOAD_FAST                'cfg1'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def call--- This code section failed: ---

 L.  29         0  LOAD_STR                 'pkg-config'
                2  LOAD_STR                 '--print-errors'
                4  BUILD_LIST_2          2 
                6  STORE_FAST               'a'

 L.  30         8  LOAD_FAST                'a'
               10  LOAD_METHOD              append
               12  LOAD_FAST                'flag'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L.  31        18  LOAD_FAST                'a'
               20  LOAD_METHOD              append
               22  LOAD_FAST                'libname'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  32        28  SETUP_FINALLY        54  'to 54'

 L.  33        30  LOAD_GLOBAL              subprocess
               32  LOAD_ATTR                Popen
               34  LOAD_FAST                'a'
               36  LOAD_GLOBAL              subprocess
               38  LOAD_ATTR                PIPE
               40  LOAD_GLOBAL              subprocess
               42  LOAD_ATTR                PIPE
               44  LOAD_CONST               ('stdout', 'stderr')
               46  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               48  STORE_FAST               'pc'
               50  POP_BLOCK        
               52  JUMP_FORWARD        112  'to 112'
             54_0  COME_FROM_FINALLY    28  '28'

 L.  34        54  DUP_TOP          
               56  LOAD_GLOBAL              EnvironmentError
               58  <121>               110  ''
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY       102  'to 102'

 L.  35        68  LOAD_GLOBAL              PkgConfigError
               70  LOAD_STR                 'cannot run pkg-config: %s'
               72  LOAD_GLOBAL              str
               74  LOAD_FAST                'e'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_METHOD              strip
               80  CALL_METHOD_0         0  ''
               82  BUILD_TUPLE_1         1 
               84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_BLOCK        
               92  POP_EXCEPT       
               94  LOAD_CONST               None
               96  STORE_FAST               'e'
               98  DELETE_FAST              'e'
              100  JUMP_FORWARD        112  'to 112'
            102_0  COME_FROM_FINALLY    66  '66'
              102  LOAD_CONST               None
              104  STORE_FAST               'e'
              106  DELETE_FAST              'e'
              108  <48>             
              110  <48>             
            112_0  COME_FROM           100  '100'
            112_1  COME_FROM            52  '52'

 L.  37       112  LOAD_FAST                'pc'
              114  LOAD_METHOD              communicate
              116  CALL_METHOD_0         0  ''
              118  UNPACK_SEQUENCE_2     2 
              120  STORE_FAST               'bout'
              122  STORE_FAST               'berr'

 L.  38       124  LOAD_FAST                'pc'
              126  LOAD_ATTR                returncode
              128  LOAD_CONST               0
              130  COMPARE_OP               !=
              132  POP_JUMP_IF_FALSE   180  'to 180'

 L.  39       134  SETUP_FINALLY       150  'to 150'

 L.  40       136  LOAD_FAST                'berr'
              138  LOAD_METHOD              decode
              140  LOAD_FAST                'encoding'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'berr'
              146  POP_BLOCK        
              148  JUMP_FORWARD        168  'to 168'
            150_0  COME_FROM_FINALLY   134  '134'

 L.  41       150  DUP_TOP          
              152  LOAD_GLOBAL              Exception
              154  <121>               166  ''
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L.  42       162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           148  '148'

 L.  43       168  LOAD_GLOBAL              PkgConfigError
              170  LOAD_FAST                'berr'
              172  LOAD_METHOD              strip
              174  CALL_METHOD_0         0  ''
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'
            180_0  COME_FROM           132  '132'

 L.  45       180  LOAD_GLOBAL              sys
              182  LOAD_ATTR                version_info
              184  LOAD_CONST               (3,)
              186  COMPARE_OP               >=
              188  POP_JUMP_IF_FALSE   254  'to 254'
              190  LOAD_GLOBAL              isinstance
              192  LOAD_FAST                'bout'
              194  LOAD_GLOBAL              str
              196  CALL_FUNCTION_2       2  ''
              198  POP_JUMP_IF_TRUE    254  'to 254'

 L.  46       200  SETUP_FINALLY       216  'to 216'

 L.  47       202  LOAD_FAST                'bout'
              204  LOAD_METHOD              decode
              206  LOAD_FAST                'encoding'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'bout'
              212  POP_BLOCK        
              214  JUMP_FORWARD        254  'to 254'
            216_0  COME_FROM_FINALLY   200  '200'

 L.  48       216  DUP_TOP          
              218  LOAD_GLOBAL              UnicodeDecodeError
              220  <121>               252  ''
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L.  49       228  LOAD_GLOBAL              PkgConfigError
              230  LOAD_STR                 'pkg-config %s %s returned bytes that cannot be decoded with encoding %r:\n%r'

 L.  51       232  LOAD_FAST                'flag'
              234  LOAD_FAST                'libname'
              236  LOAD_FAST                'encoding'
              238  LOAD_FAST                'bout'
              240  BUILD_TUPLE_4         4 

 L.  49       242  BINARY_MODULO    
              244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'
              248  POP_EXCEPT       
              250  JUMP_FORWARD        254  'to 254'
              252  <48>             
            254_0  COME_FROM           250  '250'
            254_1  COME_FROM           214  '214'
            254_2  COME_FROM           198  '198'
            254_3  COME_FROM           188  '188'

 L.  53       254  LOAD_GLOBAL              os
              256  LOAD_ATTR                altsep
              258  LOAD_STR                 '\\'
              260  COMPARE_OP               !=
          262_264  POP_JUMP_IF_FALSE   294  'to 294'
              266  LOAD_STR                 '\\'
              268  LOAD_FAST                'bout'
              270  <118>                 0  ''
          272_274  POP_JUMP_IF_FALSE   294  'to 294'

 L.  54       276  LOAD_GLOBAL              PkgConfigError
              278  LOAD_STR                 'pkg-config %s %s returned an unsupported backslash-escaped output:\n%r'

 L.  56       280  LOAD_FAST                'flag'
              282  LOAD_FAST                'libname'
              284  LOAD_FAST                'bout'
              286  BUILD_TUPLE_3         3 

 L.  54       288  BINARY_MODULO    
              290  CALL_FUNCTION_1       1  ''
              292  RAISE_VARARGS_1       1  'exception instance'
            294_0  COME_FROM           272  '272'
            294_1  COME_FROM           262  '262'

 L.  57       294  LOAD_FAST                'bout'
              296  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 58


def flags_from_pkgconfig(libs):
    """Return compiler line flags for FFI.set_source based on pkg-config output

    Usage
        ...
        ffibuilder.set_source("_foo", pkgconfig = ["libfoo", "libbar >= 1.8.3"])

    If pkg-config is installed on build machine, then arguments include_dirs,
    library_dirs, libraries, define_macros, extra_compile_args and
    extra_link_args are extended with an output of pkg-config for libfoo and
    libbar.

    Raises PkgConfigError in case the pkg-config call fails.
    """

    def get_include_dirs(string):
        return [x[2:] for x in string.split() if x.startswith'-I']

    def get_library_dirs(string):
        return [x[2:] for x in string.split() if x.startswith'-L']

    def get_libraries(string):
        return [x[2:] for x in string.split() if x.startswith'-l']

    def get_macros(string):

        def _macro--- This code section failed: ---

 L.  87         0  LOAD_FAST                'x'
                2  LOAD_CONST               2
                4  LOAD_CONST               None
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  STORE_FAST               'x'

 L.  88        12  LOAD_STR                 '='
               14  LOAD_FAST                'x'
               16  <118>                 0  ''
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L.  89        20  LOAD_GLOBAL              tuple
               22  LOAD_FAST                'x'
               24  LOAD_METHOD              split
               26  LOAD_STR                 '='
               28  LOAD_CONST               1
               30  CALL_METHOD_2         2  ''
               32  CALL_FUNCTION_1       1  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'

 L.  91        36  LOAD_FAST                'x'
               38  LOAD_CONST               None
               40  BUILD_TUPLE_2         2 
               42  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 16

        return [_macro(x) for x in string.split() if x.startswith'-D']

    def get_other_cflags(string):
        return [x for x in string.split() if not x.startswith'-I' if not x.startswith'-D']

    def get_other_libs(string):
        return [x for x in string.split() if not x.startswith'-L' if not x.startswith'-l']

    def kwargs(libname):
        fse = sys.getfilesystemencoding()
        all_cflags = calllibname'--cflags'
        all_libs = calllibname'--libs'
        return {'include_dirs':get_include_dirs(all_cflags), 
         'library_dirs':get_library_dirs(all_libs), 
         'libraries':get_libraries(all_libs), 
         'define_macros':get_macros(all_cflags), 
         'extra_compile_args':get_other_cflags(all_cflags), 
         'extra_link_args':get_other_libs(all_libs)}

    ret = {}
    for libname in libs:
        lib_flags = kwargs(libname)
        merge_flagsretlib_flags
    else:
        return ret