# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pytransform.py
import os, platform, sys, struct
from ctypes import cdll, c_char, c_char_p, c_int, c_void_p, pythonapi, py_object, PYFUNCTYPE, CFUNCTYPE
from fnmatch import fnmatch
plat_path = 'platforms'
plat_table = (('windows', ('windows', 'cygwin-*')), ('darwin', ('darwin',)), ('ios', ('ios',)),
              ('linux', ('linux*',)), ('freebsd', ('freebsd*', 'openbsd*', 'isilon onefs')),
              ('poky', ('poky',)))
arch_table = (('x86', ('i?86',)), ('x86_64', ('x64', 'x86_64', 'amd64', 'intel')),
              ('arm', ('armv5',)), ('armv6', ('armv6l',)), ('armv7', ('armv7l',)),
              ('ppc64', ('ppc64le',)), ('mips32', ('mips',)), ('aarch32', ('aarch32',)),
              ('aarch64', ('aarch64', 'arm64')))
HT_HARDDISK, HT_IFMAC, HT_IPV4, HT_IPV6, HT_DOMAIN = range(5)
_pytransform = None

class PytransformError(Exception):
    pass


def dllmethod(func):

    def wrap--- This code section failed: ---

 L.  58         0  LOAD_DEREF               'func'
                2  LOAD_FAST                'args'
                4  BUILD_MAP_0           0 
                6  LOAD_FAST                'kwargs'
                8  <164>                 1  ''
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    return wrap


@dllmethod
def version_info():
    global _pytransform
    prototype = PYFUNCTYPE(py_object)
    dlfunc = prototype(('version_info', _pytransform))
    return dlfunc()


@dllmethod
def init_pytransform():
    major, minor = sys.version_info[0:2]
    prototype = PYFUNCTYPE(c_int, c_int, c_int, c_void_p)
    init_module = prototype(('init_module', _pytransform))
    ret = init_module(major, minor, pythonapi._handle)
    if ret & 61440 == 4096:
        raise PytransformError('Initialize python wrapper failed (%d)' % (ret & 4095))
    return ret


@dllmethod
def init_runtime():
    prototype = PYFUNCTYPE(c_int, c_int, c_int, c_int, c_int)
    _init_runtime = prototype(('init_runtime', _pytransform))
    return _init_runtime(0, 0, 0, 0)


@dllmethod
def encrypt_code_object(pubkey, co, flags, suffix=''):
    _pytransform.set_option(6, suffix.encode())
    prototype = PYFUNCTYPE(py_object, py_object, py_object, c_int)
    dlfunc = prototype(('encrypt_code_object', _pytransform))
    return dlfunc(pubkey, co, flags)


@dllmethod
def generate_license_file(filename, priname, rcode, start=-1, count=1):
    prototype = PYFUNCTYPE(c_int, c_char_p, c_char_p, c_char_p, c_int, c_int)
    dlfunc = prototype(('generate_project_license_files', _pytransform))
    if sys.version_info[0] == 3:
        return dlfunc(filename.encode(), priname.encode(), rcode.encode(), start, count)
    return dlfunc(filename, priname, rcode, start, count)


@dllmethod
def generate_license_key(prikey, keysize, rcode):
    prototype = PYFUNCTYPE(py_object, c_char_p, c_int, c_char_p)
    dlfunc = prototype(('generate_license_key', _pytransform))
    if sys.version_info[0] == 2:
        return dlfunc(prikey, keysize, rcode)
    return dlfunc(prikey, keysize, rcode.encode())


@dllmethod
def get_registration_code():
    prototype = PYFUNCTYPE(py_object)
    dlfunc = prototype(('get_registration_code', _pytransform))
    return dlfunc()


@dllmethod
def get_expired_days():
    prototype = PYFUNCTYPE(py_object)
    dlfunc = prototype(('get_expired_days', _pytransform))
    return dlfunc()


@dllmethod
def clean_obj(obj, kind):
    prototype = PYFUNCTYPE(c_int, py_object, c_int)
    dlfunc = prototype(('clean_obj', _pytransform))
    return dlfunc(obj, kind)


def clean_str--- This code section failed: ---

 L. 138         0  LOAD_CONST               0

 L. 139         2  LOAD_CONST               1

 L. 140         4  LOAD_CONST               2

 L. 137         6  LOAD_CONST               ('str', 'bytearray', 'unicode')
                8  BUILD_CONST_KEY_MAP_3     3 
               10  STORE_FAST               'tdict'

 L. 142        12  LOAD_FAST                'args'
               14  GET_ITER         
             16_0  COME_FROM            66  '66'
               16  FOR_ITER             68  'to 68'
               18  STORE_FAST               'obj'

 L. 143        20  LOAD_FAST                'tdict'
               22  LOAD_METHOD              get
               24  LOAD_GLOBAL              type
               26  LOAD_FAST                'obj'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_ATTR                __name__
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'k'

 L. 144        36  LOAD_FAST                'k'
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L. 145        44  LOAD_GLOBAL              RuntimeError
               46  LOAD_STR                 'Can not clean object: %s'
               48  LOAD_FAST                'obj'
               50  BINARY_MODULO    
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            42  '42'

 L. 146        56  LOAD_GLOBAL              clean_obj
               58  LOAD_FAST                'obj'
               60  LOAD_FAST                'k'
               62  CALL_FUNCTION_2       2  ''
               64  POP_TOP          
               66  JUMP_BACK            16  'to 16'
             68_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 40


def get_hd_info--- This code section failed: ---

 L. 150         0  LOAD_FAST                'hdtype'
                2  LOAD_GLOBAL              range
                4  LOAD_GLOBAL              HT_DOMAIN
                6  LOAD_CONST               1
                8  BINARY_ADD       
               10  CALL_FUNCTION_1       1  ''
               12  <118>                 1  ''
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L. 151        16  LOAD_GLOBAL              RuntimeError
               18  LOAD_STR                 'Invalid parameter hdtype: %s'
               20  LOAD_FAST                'hdtype'
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            14  '14'

 L. 152        28  LOAD_CONST               256
               30  STORE_FAST               'size'

 L. 153        32  LOAD_GLOBAL              c_char
               34  LOAD_FAST                'size'
               36  BINARY_MULTIPLY  
               38  STORE_FAST               't_buf'

 L. 154        40  LOAD_FAST                't_buf'
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'buf'

 L. 155        46  LOAD_GLOBAL              c_char_p
               48  LOAD_FAST                'name'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    60  'to 60'
               56  LOAD_CONST               0
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM            54  '54'

 L. 156        60  LOAD_GLOBAL              hasattr
               62  LOAD_STR                 'name'
               64  LOAD_STR                 'encode'
               66  CALL_FUNCTION_2       2  ''
               68  POP_JUMP_IF_FALSE    80  'to 80'
               70  LOAD_FAST                'name'
               72  LOAD_METHOD              encode
               74  LOAD_STR                 'utf-8'
               76  CALL_METHOD_1         1  ''
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            68  '68'

 L. 157        80  LOAD_FAST                'name'
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            58  '58'

 L. 155        82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'cname'

 L. 158        86  LOAD_GLOBAL              _pytransform
               88  LOAD_METHOD              get_hd_info
               90  LOAD_FAST                'hdtype'
               92  LOAD_FAST                'buf'
               94  LOAD_FAST                'size'
               96  LOAD_FAST                'cname'
               98  CALL_METHOD_4         4  ''
              100  LOAD_CONST               -1
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L. 159       106  LOAD_GLOBAL              PytransformError
              108  LOAD_STR                 'Get hardware information failed'
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'

 L. 160       114  LOAD_FAST                'buf'
              116  LOAD_ATTR                value
              118  LOAD_METHOD              decode
              120  CALL_METHOD_0         0  ''
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def show_hd_info():
    return _pytransform.show_hd_info()


def assert_armored(*names):
    prototype = PYFUNCTYPE(py_object, py_object)
    dlfunc = prototype(('assert_armored', _pytransform))

    def wrapper(func):

        def wrap_execute--- This code section failed: ---

 L. 173         0  LOAD_DEREF               'dlfunc'
                2  LOAD_DEREF               'names'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 174         8  LOAD_DEREF               'func'
               10  LOAD_FAST                'args'
               12  BUILD_MAP_0           0 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 16

        return wrap_execute

    return wrapper


def check_armored--- This code section failed: ---

 L. 180         0  SETUP_FINALLY        34  'to 34'

 L. 181         2  LOAD_GLOBAL              PYFUNCTYPE
                4  LOAD_GLOBAL              py_object
                6  LOAD_GLOBAL              py_object
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'prototype'

 L. 182        12  LOAD_FAST                'prototype'
               14  LOAD_STR                 'assert_armored'
               16  LOAD_GLOBAL              _pytransform
               18  BUILD_TUPLE_2         2 
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_FAST                'names'
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          

 L. 183        28  POP_BLOCK        
               30  LOAD_CONST               True
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     0  '0'

 L. 184        34  DUP_TOP          
               36  LOAD_GLOBAL              RuntimeError
               38  <121>                52  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 185        46  POP_EXCEPT       
               48  LOAD_CONST               False
               50  RETURN_VALUE     
               52  <48>             

Parse error at or near `DUP_TOP' instruction at offset 34


def get_license_info--- This code section failed: ---

 L. 190         0  LOAD_CONST               None

 L. 191         2  LOAD_CONST               None

 L. 192         4  LOAD_CONST               None

 L. 193         6  LOAD_CONST               None

 L. 194         8  LOAD_CONST               None

 L. 195        10  LOAD_CONST               None

 L. 196        12  LOAD_CONST               None

 L. 197        14  LOAD_CONST               None

 L. 189        16  LOAD_CONST               ('ISSUER', 'EXPIRED', 'HARDDISK', 'IFMAC', 'IFIPV4', 'DOMAIN', 'DATA', 'CODE')
               18  BUILD_CONST_KEY_MAP_8     8 
               20  STORE_FAST               'info'

 L. 199        22  LOAD_GLOBAL              get_registration_code
               24  CALL_FUNCTION_0       0  ''
               26  LOAD_METHOD              decode
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'rcode'

 L. 200        32  LOAD_FAST                'rcode'
               34  LOAD_METHOD              startswith
               36  LOAD_STR                 '*VERSION:'
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE   102  'to 102'

 L. 201        42  LOAD_FAST                'rcode'
               44  LOAD_METHOD              find
               46  LOAD_STR                 '\n'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'index'

 L. 202        52  LOAD_FAST                'rcode'
               54  LOAD_CONST               9
               56  LOAD_FAST                'index'
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_METHOD              split
               64  LOAD_STR                 '.'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_METHOD              replace
               74  LOAD_STR                 '-sn-1.txt'
               76  LOAD_STR                 ''
               78  CALL_METHOD_2         2  ''
               80  LOAD_FAST                'info'
               82  LOAD_STR                 'ISSUER'
               84  STORE_SUBSCR     

 L. 203        86  LOAD_FAST                'rcode'
               88  LOAD_FAST                'index'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  STORE_FAST               'rcode'
            102_0  COME_FROM            40  '40'

 L. 205       102  LOAD_CONST               0
              104  STORE_FAST               'index'

 L. 206       106  LOAD_FAST                'rcode'
              108  LOAD_METHOD              startswith
              110  LOAD_STR                 '*TIME:'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_FALSE   170  'to 170'

 L. 207       116  LOAD_CONST               0
              118  LOAD_CONST               ('ctime',)
              120  IMPORT_NAME              time
              122  IMPORT_FROM              ctime
              124  STORE_FAST               'ctime'
              126  POP_TOP          

 L. 208       128  LOAD_FAST                'rcode'
              130  LOAD_METHOD              find
              132  LOAD_STR                 '\n'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'index'

 L. 209       138  LOAD_FAST                'ctime'
              140  LOAD_GLOBAL              float
              142  LOAD_FAST                'rcode'
              144  LOAD_CONST               6
              146  LOAD_FAST                'index'
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  CALL_FUNCTION_1       1  ''
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_FAST                'info'
              158  LOAD_STR                 'EXPIRED'
              160  STORE_SUBSCR     

 L. 210       162  LOAD_FAST                'index'
              164  LOAD_CONST               1
              166  INPLACE_ADD      
              168  STORE_FAST               'index'
            170_0  COME_FROM           114  '114'

 L. 212       170  LOAD_FAST                'rcode'
              172  LOAD_FAST                'index'
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  LOAD_METHOD              startswith
              182  LOAD_STR                 '*FLAGS:'
              184  CALL_METHOD_1         1  ''
              186  POP_JUMP_IF_FALSE   224  'to 224'

 L. 213       188  LOAD_FAST                'index'
              190  LOAD_GLOBAL              len
              192  LOAD_STR                 '*FLAGS:'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               1
              198  BINARY_ADD       
              200  INPLACE_ADD      
              202  STORE_FAST               'index'

 L. 214       204  LOAD_GLOBAL              ord
              206  LOAD_FAST                'rcode'
              208  LOAD_FAST                'index'
              210  LOAD_CONST               1
              212  BINARY_SUBTRACT  
              214  BINARY_SUBSCR    
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_FAST                'info'
              220  LOAD_STR                 'FLAGS'
              222  STORE_SUBSCR     
            224_0  COME_FROM           186  '186'

 L. 216       224  LOAD_CONST               None
              226  STORE_FAST               'prev'

 L. 217       228  LOAD_FAST                'index'
              230  STORE_FAST               'start'

 L. 218       232  LOAD_CONST               ('HARDDISK', 'IFMAC', 'IFIPV4', 'DOMAIN', 'FIXKEY', 'CODE')
              234  GET_ITER         
            236_0  COME_FROM           308  '308'
            236_1  COME_FROM           260  '260'
              236  FOR_ITER            310  'to 310'
              238  STORE_FAST               'k'

 L. 219       240  LOAD_FAST                'rcode'
              242  LOAD_METHOD              find
              244  LOAD_STR                 '*%s:'
              246  LOAD_FAST                'k'
              248  BINARY_MODULO    
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'index'

 L. 220       254  LOAD_FAST                'index'
              256  LOAD_CONST               -1
              258  COMPARE_OP               >
              260  POP_JUMP_IF_FALSE_BACK   236  'to 236'

 L. 221       262  LOAD_FAST                'prev'
              264  LOAD_CONST               None
              266  <117>                 1  ''
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 222       272  LOAD_FAST                'rcode'
              274  LOAD_FAST                'start'
              276  LOAD_FAST                'index'
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'info'
              284  LOAD_FAST                'prev'
              286  STORE_SUBSCR     
            288_0  COME_FROM           268  '268'

 L. 223       288  LOAD_FAST                'k'
              290  STORE_FAST               'prev'

 L. 224       292  LOAD_FAST                'index'
              294  LOAD_GLOBAL              len
              296  LOAD_FAST                'k'
              298  CALL_FUNCTION_1       1  ''
              300  BINARY_ADD       
              302  LOAD_CONST               2
              304  BINARY_ADD       
              306  STORE_FAST               'start'
              308  JUMP_BACK           236  'to 236'
            310_0  COME_FROM           236  '236'

 L. 225       310  LOAD_FAST                'rcode'
              312  LOAD_FAST                'start'
              314  LOAD_CONST               None
              316  BUILD_SLICE_2         2 
              318  BINARY_SUBSCR    
              320  LOAD_FAST                'info'
              322  LOAD_STR                 'CODE'
              324  STORE_SUBSCR     

 L. 226       326  LOAD_FAST                'info'
              328  LOAD_STR                 'CODE'
              330  BINARY_SUBSCR    
              332  LOAD_METHOD              find
              334  LOAD_STR                 ';'
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'i'

 L. 227       340  LOAD_FAST                'i'
              342  LOAD_CONST               0
              344  COMPARE_OP               >
          346_348  POP_JUMP_IF_FALSE   394  'to 394'

 L. 228       350  LOAD_FAST                'info'
              352  LOAD_STR                 'CODE'
              354  BINARY_SUBSCR    
              356  LOAD_FAST                'i'
              358  LOAD_CONST               1
              360  BINARY_ADD       
              362  LOAD_CONST               None
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    
              368  LOAD_FAST                'info'
              370  LOAD_STR                 'DATA'
              372  STORE_SUBSCR     

 L. 229       374  LOAD_FAST                'info'
              376  LOAD_STR                 'CODE'
              378  BINARY_SUBSCR    
              380  LOAD_CONST               None
              382  LOAD_FAST                'i'
              384  BUILD_SLICE_2         2 
              386  BINARY_SUBSCR    
              388  LOAD_FAST                'info'
              390  LOAD_STR                 'CODE'
              392  STORE_SUBSCR     
            394_0  COME_FROM           346  '346'

 L. 230       394  LOAD_FAST                'info'
              396  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 266


def get_license_code():
    return get_license_info()['CODE']


def get_user_data():
    return get_license_info()['DATA']


def _match_features(patterns, s):
    for pat in patterns:
        if fnmatch(s, pat):
            return True


def _gnu_get_libc_version--- This code section failed: ---

 L. 248         0  SETUP_FINALLY        46  'to 46'

 L. 249         2  LOAD_GLOBAL              CFUNCTYPE
                4  LOAD_GLOBAL              c_char_p
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'prototype'

 L. 250        10  LOAD_FAST                'prototype'
               12  LOAD_STR                 'gnu_get_libc_version'
               14  LOAD_GLOBAL              cdll
               16  LOAD_METHOD              LoadLibrary
               18  LOAD_STR                 ''
               20  CALL_METHOD_1         1  ''
               22  BUILD_TUPLE_2         2 
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'ver'

 L. 251        30  LOAD_FAST                'ver'
               32  LOAD_METHOD              decode
               34  CALL_METHOD_0         0  ''
               36  LOAD_METHOD              split
               38  LOAD_STR                 '.'
               40  CALL_METHOD_1         1  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY     0  '0'

 L. 252        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  <121>                62  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 253        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'

Parse error at or near `<121>' instruction at offset 50


def format_platform(platid=None):
    if platid:
        return os.path.normpathplatid
    plat = platform.system().lower()
    mach = platform.machine().lower()
    for alias, platlist in plat_table:
        if _match_features(platlist, plat):
            plat = alias
            break
    else:
        if plat == 'linux':
            cname, cver = platform.libc_ver()
            if cname == 'musl':
                plat = 'musl'
            elif cname == 'libc':
                plat = 'android'
            elif cname == 'glibc':
                v = _gnu_get_libc_version()
                if v:
                    if len(v) >= 2:
                        if int(v[0]) * 100 + int(v[1]) < 214:
                            plat = 'centos6'
        for alias, archlist in arch_table:
            if _match_features(archlist, mach):
                mach = alias
                break
        else:
            if plat == 'windows':
                if mach == 'x86_64':
                    bitness = struct.calcsize'P'.encode() * 8
                    if bitness == 32:
                        mach = 'x86'
            return os.path.join(plat, mach)


def _load_library--- This code section failed: ---

 L. 294         0  LOAD_FAST                'path'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_GLOBAL              os
               10  LOAD_ATTR                path
               12  LOAD_METHOD              dirname
               14  LOAD_GLOBAL              __file__
               16  CALL_METHOD_1         1  ''
               18  JUMP_FORWARD         30  'to 30'
             20_0  COME_FROM             6  '6'

 L. 295        20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              normpath
               26  LOAD_FAST                'path'
               28  CALL_METHOD_1         1  ''
             30_0  COME_FROM            18  '18'

 L. 294        30  STORE_FAST               'path'

 L. 297        32  LOAD_GLOBAL              platform
               34  LOAD_METHOD              system
               36  CALL_METHOD_0         0  ''
               38  LOAD_METHOD              lower
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'plat'

 L. 298        44  LOAD_GLOBAL              plat_table
               46  GET_ITER         
             48_0  COME_FROM            74  '74'
             48_1  COME_FROM            64  '64'
               48  FOR_ITER             76  'to 76'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'alias'
               54  STORE_FAST               'platlist'

 L. 299        56  LOAD_GLOBAL              _match_features
               58  LOAD_FAST                'platlist'
               60  LOAD_FAST                'plat'
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE_BACK    48  'to 48'

 L. 300        66  LOAD_FAST                'alias'
               68  STORE_FAST               'plat'

 L. 301        70  POP_TOP          
               72  BREAK_LOOP           76  'to 76'
               74  JUMP_BACK            48  'to 48'
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            48  '48'

 L. 303        76  LOAD_STR                 '_pytransform'
               78  LOAD_FAST                'suffix'
               80  BINARY_ADD       
               82  STORE_FAST               'name'

 L. 304        84  LOAD_FAST                'plat'
               86  LOAD_STR                 'linux'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   120  'to 120'

 L. 305        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              abspath
               98  LOAD_GLOBAL              os
              100  LOAD_ATTR                path
              102  LOAD_METHOD              join
              104  LOAD_FAST                'path'
              106  LOAD_FAST                'name'
              108  LOAD_STR                 '.so'
              110  BINARY_ADD       
              112  CALL_METHOD_2         2  ''
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'filename'
              118  JUMP_FORWARD        208  'to 208'
            120_0  COME_FROM            90  '90'

 L. 306       120  LOAD_FAST                'plat'
              122  LOAD_CONST               ('darwin', 'ios')
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   148  'to 148'

 L. 307       128  LOAD_GLOBAL              os
              130  LOAD_ATTR                path
              132  LOAD_METHOD              join
              134  LOAD_FAST                'path'
              136  LOAD_FAST                'name'
              138  LOAD_STR                 '.dylib'
              140  BINARY_ADD       
              142  CALL_METHOD_2         2  ''
              144  STORE_FAST               'filename'
              146  JUMP_FORWARD        208  'to 208'
            148_0  COME_FROM           126  '126'

 L. 308       148  LOAD_FAST                'plat'
              150  LOAD_STR                 'windows'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   176  'to 176'

 L. 309       156  LOAD_GLOBAL              os
              158  LOAD_ATTR                path
              160  LOAD_METHOD              join
              162  LOAD_FAST                'path'
              164  LOAD_FAST                'name'
              166  LOAD_STR                 '.dll'
              168  BINARY_ADD       
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'filename'
              174  JUMP_FORWARD        208  'to 208'
            176_0  COME_FROM           154  '154'

 L. 310       176  LOAD_FAST                'plat'
              178  LOAD_CONST               ('freebsd', 'poky')
              180  <118>                 0  ''
              182  POP_JUMP_IF_FALSE   204  'to 204'

 L. 311       184  LOAD_GLOBAL              os
              186  LOAD_ATTR                path
              188  LOAD_METHOD              join
              190  LOAD_FAST                'path'
              192  LOAD_FAST                'name'
              194  LOAD_STR                 '.so'
              196  BINARY_ADD       
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'filename'
              202  JUMP_FORWARD        208  'to 208'
            204_0  COME_FROM           182  '182'

 L. 313       204  LOAD_CONST               None
              206  STORE_FAST               'filename'
            208_0  COME_FROM           202  '202'
            208_1  COME_FROM           174  '174'
            208_2  COME_FROM           146  '146'
            208_3  COME_FROM           118  '118'

 L. 315       208  LOAD_FAST                'platid'
              210  LOAD_CONST               None
              212  <117>                 1  ''
              214  POP_JUMP_IF_FALSE   234  'to 234'
              216  LOAD_GLOBAL              os
              218  LOAD_ATTR                path
              220  LOAD_METHOD              isfile
              222  LOAD_FAST                'platid'
              224  CALL_METHOD_1         1  ''
              226  POP_JUMP_IF_FALSE   234  'to 234'

 L. 316       228  LOAD_FAST                'platid'
              230  STORE_FAST               'filename'
              232  JUMP_FORWARD        334  'to 334'
            234_0  COME_FROM           226  '226'
            234_1  COME_FROM           214  '214'

 L. 317       234  LOAD_FAST                'platid'
              236  LOAD_CONST               None
              238  <117>                 1  ''
          240_242  POP_JUMP_IF_TRUE    264  'to 264'
              244  LOAD_GLOBAL              os
              246  LOAD_ATTR                path
              248  LOAD_METHOD              exists
              250  LOAD_FAST                'filename'
              252  CALL_METHOD_1         1  ''
          254_256  POP_JUMP_IF_FALSE   264  'to 264'
              258  LOAD_FAST                'is_runtime'
          260_262  POP_JUMP_IF_TRUE    334  'to 334'
            264_0  COME_FROM           254  '254'
            264_1  COME_FROM           240  '240'

 L. 318       264  LOAD_FAST                'platid'
              266  LOAD_CONST               None
              268  <117>                 1  ''
          270_272  POP_JUMP_IF_FALSE   292  'to 292'
              274  LOAD_GLOBAL              os
              276  LOAD_ATTR                path
              278  LOAD_METHOD              isabs
              280  LOAD_FAST                'platid'
              282  CALL_METHOD_1         1  ''
          284_286  POP_JUMP_IF_FALSE   292  'to 292'
              288  LOAD_FAST                'platid'
              290  JUMP_FORWARD        310  'to 310'
            292_0  COME_FROM           284  '284'
            292_1  COME_FROM           270  '270'

 L. 319       292  LOAD_GLOBAL              os
              294  LOAD_ATTR                path
              296  LOAD_METHOD              join
              298  LOAD_FAST                'path'
              300  LOAD_GLOBAL              plat_path
              302  LOAD_GLOBAL              format_platform
              304  LOAD_FAST                'platid'
              306  CALL_FUNCTION_1       1  ''
              308  CALL_METHOD_3         3  ''
            310_0  COME_FROM           290  '290'

 L. 318       310  STORE_FAST               'libpath'

 L. 320       312  LOAD_GLOBAL              os
              314  LOAD_ATTR                path
              316  LOAD_METHOD              join
              318  LOAD_FAST                'libpath'
              320  LOAD_GLOBAL              os
              322  LOAD_ATTR                path
              324  LOAD_METHOD              basename
              326  LOAD_FAST                'filename'
              328  CALL_METHOD_1         1  ''
              330  CALL_METHOD_2         2  ''
              332  STORE_FAST               'filename'
            334_0  COME_FROM           260  '260'
            334_1  COME_FROM           232  '232'

 L. 322       334  LOAD_FAST                'filename'
              336  LOAD_CONST               None
              338  <117>                 0  ''
          340_342  POP_JUMP_IF_FALSE   356  'to 356'

 L. 323       344  LOAD_GLOBAL              PytransformError
              346  LOAD_STR                 'Platform %s not supported'
              348  LOAD_FAST                'plat'
              350  BINARY_MODULO    
              352  CALL_FUNCTION_1       1  ''
              354  RAISE_VARARGS_1       1  'exception instance'
            356_0  COME_FROM           340  '340'

 L. 325       356  LOAD_GLOBAL              os
              358  LOAD_ATTR                path
              360  LOAD_METHOD              exists
              362  LOAD_FAST                'filename'
              364  CALL_METHOD_1         1  ''
          366_368  POP_JUMP_IF_TRUE    382  'to 382'

 L. 326       370  LOAD_GLOBAL              PytransformError
              372  LOAD_STR                 'Could not find "%s"'
              374  LOAD_FAST                'filename'
              376  BINARY_MODULO    
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
            382_0  COME_FROM           366  '366'

 L. 328       382  SETUP_FINALLY       398  'to 398'

 L. 329       384  LOAD_GLOBAL              cdll
              386  LOAD_METHOD              LoadLibrary
              388  LOAD_FAST                'filename'
              390  CALL_METHOD_1         1  ''
              392  STORE_FAST               'm'
              394  POP_BLOCK        
              396  JUMP_FORWARD        464  'to 464'
            398_0  COME_FROM_FINALLY   382  '382'

 L. 330       398  DUP_TOP          
              400  LOAD_GLOBAL              Exception
          402_404  <121>               462  ''
              406  POP_TOP          
              408  STORE_FAST               'e'
              410  POP_TOP          
              412  SETUP_FINALLY       454  'to 454'

 L. 331       414  LOAD_GLOBAL              sys
              416  LOAD_ATTR                flags
              418  LOAD_ATTR                debug
          420_422  POP_JUMP_IF_FALSE   440  'to 440'

 L. 332       424  LOAD_GLOBAL              print
              426  LOAD_STR                 'Load %s failed:\n%s'
              428  LOAD_FAST                'filename'
              430  LOAD_FAST                'e'
              432  BUILD_TUPLE_2         2 
              434  BINARY_MODULO    
              436  CALL_FUNCTION_1       1  ''
              438  POP_TOP          
            440_0  COME_FROM           420  '420'

 L. 333       440  RAISE_VARARGS_0       0  'reraise'
              442  POP_BLOCK        
              444  POP_EXCEPT       
              446  LOAD_CONST               None
              448  STORE_FAST               'e'
              450  DELETE_FAST              'e'
              452  JUMP_FORWARD        464  'to 464'
            454_0  COME_FROM_FINALLY   412  '412'
              454  LOAD_CONST               None
              456  STORE_FAST               'e'
              458  DELETE_FAST              'e'
              460  <48>             
              462  <48>             
            464_0  COME_FROM           452  '452'
            464_1  COME_FROM           396  '396'

 L. 339       464  LOAD_GLOBAL              os
              466  LOAD_ATTR                path
              468  LOAD_METHOD              abspath
              470  LOAD_STR                 '.'
              472  CALL_METHOD_1         1  ''
              474  LOAD_GLOBAL              os
              476  LOAD_ATTR                path
              478  LOAD_METHOD              abspath
              480  LOAD_FAST                'path'
              482  CALL_METHOD_1         1  ''
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_TRUE    526  'to 526'

 L. 340       490  LOAD_FAST                'm'
              492  LOAD_METHOD              set_option
              494  LOAD_CONST               1
              496  LOAD_GLOBAL              sys
              498  LOAD_ATTR                version_info
              500  LOAD_CONST               0
              502  BINARY_SUBSCR    
              504  LOAD_CONST               3
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   520  'to 520'
              512  LOAD_FAST                'path'
              514  LOAD_METHOD              encode
              516  CALL_METHOD_0         0  ''
              518  JUMP_FORWARD        522  'to 522'
            520_0  COME_FROM           508  '508'
              520  LOAD_FAST                'path'
            522_0  COME_FROM           518  '518'
              522  CALL_METHOD_2         2  ''
              524  POP_TOP          
            526_0  COME_FROM           486  '486'

 L. 343       526  LOAD_FAST                'm'
              528  LOAD_METHOD              set_option
              530  LOAD_CONST               2
              532  LOAD_GLOBAL              sys
              534  LOAD_ATTR                byteorder
              536  LOAD_METHOD              encode
              538  CALL_METHOD_0         0  ''
              540  CALL_METHOD_2         2  ''
              542  POP_TOP          

 L. 345       544  LOAD_GLOBAL              sys
              546  LOAD_ATTR                flags
              548  LOAD_ATTR                debug
          550_552  POP_JUMP_IF_FALSE   570  'to 570'

 L. 346       554  LOAD_FAST                'm'
              556  LOAD_METHOD              set_option
              558  LOAD_CONST               3
              560  LOAD_GLOBAL              c_char_p
              562  LOAD_CONST               1
              564  CALL_FUNCTION_1       1  ''
              566  CALL_METHOD_2         2  ''
              568  POP_TOP          
            570_0  COME_FROM           550  '550'

 L. 347       570  LOAD_FAST                'm'
              572  LOAD_METHOD              set_option
              574  LOAD_CONST               4
              576  LOAD_GLOBAL              c_char_p
              578  LOAD_FAST                'is_runtime'
              580  UNARY_NOT        
              582  CALL_FUNCTION_1       1  ''
              584  CALL_METHOD_2         2  ''
              586  POP_TOP          

 L. 350       588  LOAD_FAST                'm'
              590  LOAD_METHOD              set_option
              592  LOAD_CONST               5
              594  LOAD_GLOBAL              c_char_p
              596  LOAD_FAST                'advanced'
              598  UNARY_NOT        
              600  CALL_FUNCTION_1       1  ''
              602  CALL_METHOD_2         2  ''
              604  POP_TOP          

 L. 353       606  LOAD_FAST                'suffix'
          608_610  POP_JUMP_IF_FALSE   628  'to 628'

 L. 354       612  LOAD_FAST                'm'
              614  LOAD_METHOD              set_option
              616  LOAD_CONST               6
              618  LOAD_FAST                'suffix'
              620  LOAD_METHOD              encode
              622  CALL_METHOD_0         0  ''
              624  CALL_METHOD_2         2  ''
              626  POP_TOP          
            628_0  COME_FROM           608  '608'

 L. 356       628  LOAD_FAST                'm'
              630  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def pyarmor_init(path=None, is_runtime=0, platid=None, suffix='', advanced=0):
    global _pytransform
    _pytransform = _load_library(path, is_runtime, platid, suffix, advanced)
    return init_pytransform()


def pyarmor_runtime--- This code section failed: ---

 L. 366         0  LOAD_GLOBAL              _pytransform
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 367         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 369        12  SETUP_FINALLY        40  'to 40'

 L. 370        14  LOAD_GLOBAL              pyarmor_init
               16  LOAD_FAST                'path'
               18  LOAD_CONST               1
               20  LOAD_FAST                'suffix'
               22  LOAD_FAST                'advanced'
               24  LOAD_CONST               ('is_runtime', 'suffix', 'advanced')
               26  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               28  POP_TOP          

 L. 371        30  LOAD_GLOBAL              init_runtime
               32  CALL_FUNCTION_0       0  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD        126  'to 126'
             40_0  COME_FROM_FINALLY    12  '12'

 L. 372        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  <121>               124  ''
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY       116  'to 116'

 L. 373        54  LOAD_GLOBAL              sys
               56  LOAD_ATTR                flags
               58  LOAD_ATTR                debug
               60  POP_JUMP_IF_TRUE     72  'to 72'
               62  LOAD_GLOBAL              hasattr
               64  LOAD_GLOBAL              sys
               66  LOAD_STR                 '_catch_pyarmor'
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE    74  'to 74'
             72_0  COME_FROM            60  '60'

 L. 374        72  RAISE_VARARGS_0       0  'reraise'
             74_0  COME_FROM            70  '70'

 L. 375        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                stderr
               78  LOAD_METHOD              write
               80  LOAD_STR                 '%s\n'
               82  LOAD_GLOBAL              str
               84  LOAD_FAST                'e'
               86  CALL_FUNCTION_1       1  ''
               88  BINARY_MODULO    
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 376        94  LOAD_GLOBAL              sys
               96  LOAD_METHOD              exit
               98  LOAD_CONST               1
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  LOAD_CONST               None
              110  STORE_FAST               'e'
              112  DELETE_FAST              'e'
              114  JUMP_FORWARD        126  'to 126'
            116_0  COME_FROM_FINALLY    52  '52'
              116  LOAD_CONST               None
              118  STORE_FAST               'e'
              120  DELETE_FAST              'e'
              122  <48>             
              124  <48>             
            126_0  COME_FROM           114  '114'
            126_1  COME_FROM            38  '38'

Parse error at or near `None' instruction at offset -1


def generate_capsule(licfile):
    prikey, pubkey, prolic = _generate_project_capsule()
    capkey, newkey = _generate_pytransform_key(licfile, pubkey)
    return (
     prikey, pubkey, capkey, newkey, prolic)


@dllmethod
def _generate_project_capsule():
    prototype = PYFUNCTYPE(py_object)
    dlfunc = prototype(('generate_project_capsule', _pytransform))
    return dlfunc()


@dllmethod
def _generate_pytransform_key(licfile, pubkey):
    prototype = PYFUNCTYPE(py_object, c_char_p, py_object)
    dlfunc = prototype(('generate_pytransform_key', _pytransform))
    return dlfunc(licfile.encode() if sys.version_info[0] == 3 else licfile, pubkey)


@dllmethod
def encrypt_project_files(proname, filelist, mode=0):
    prototype = PYFUNCTYPE(c_int, c_char_p, py_object, c_int)
    dlfunc = prototype(('encrypt_project_files', _pytransform))
    return dlfunc(proname.encode(), filelist, mode)


def generate_project_capsule(licfile):
    prikey, pubkey, prolic = _generate_project_capsule()
    capkey = _encode_capsule_key_file(licfile)
    return (
     prikey, pubkey, capkey, prolic)


@dllmethod
def _encode_capsule_key_file(licfile):
    prototype = PYFUNCTYPE(py_object, c_char_p, c_char_p)
    dlfunc = prototype(('encode_capsule_key_file', _pytransform))
    return dlfunc(licfile.encode(), None)


@dllmethod
def encrypt_files(key, filelist, mode=0):
    t_key = c_char * 32
    prototype = PYFUNCTYPE(c_int, t_key, py_object, c_int)
    dlfunc = prototype(('encrypt_files', _pytransform))
    return dlfunc(t_key(*key), filelist, mode)


@dllmethod
def generate_module_key(pubname, key):
    t_key = c_char * 32
    prototype = PYFUNCTYPE(py_object, c_char_p, t_key, c_char_p)
    dlfunc = prototype(('generate_module_key', _pytransform))
    return dlfunc(pubname.encode(), t_key(*key), None)


@dllmethod
def old_init_runtime(systrace=0, sysprofile=1, threadtrace=0, threadprofile=1):
    """Only for old version, before PyArmor 3"""
    pyarmor_init(is_runtime=1)
    prototype = PYFUNCTYPE(c_int, c_int, c_int, c_int, c_int)
    _init_runtime = prototype(('init_runtime', _pytransform))
    return _init_runtime(systrace, sysprofile, threadtrace, threadprofile)


@dllmethod
def import_module(modname, filename):
    """Only for old version, before PyArmor 3"""
    prototype = PYFUNCTYPE(py_object, c_char_p, c_char_p)
    _import_module = prototype(('import_module', _pytransform))
    return _import_module(modname.encode(), filename.encode())


@dllmethod
def exec_file(filename):
    """Only for old version, before PyArmor 3"""
    prototype = PYFUNCTYPE(c_int, c_char_p)
    _exec_file = prototype(('exec_file', _pytransform))
    return _exec_file(filename.encode())