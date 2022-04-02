# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: dist\obf\temp\pytransform.py
import os, platform, sys, struct
from ctypes import cdll, c_char, c_char_p, c_int, c_void_p, pythonapi, py_object, PYFUNCTYPE, CFUNCTYPE
from fnmatch import fnmatch
plat_path = 'platforms'
plat_table = (('windows', ('windows', 'cygwin-*')), ('darwin', ('darwin', 'ios')),
              ('linux', ('linux*',)), ('freebsd', ('freebsd*', 'openbsd*')), ('poky', ('poky',)))
arch_table = (('x86', ('i?86',)), ('x86_64', ('x64', 'x86_64', 'amd64', 'intel')),
              ('arm', ('armv5',)), ('armv6', ('armv6l',)), ('armv7', ('armv7l',)),
              ('aarch32', ('aarch32',)), ('aarch64', ('aarch64', 'arm64')))
HT_HARDDISK, HT_IFMAC, HT_IPV4, HT_IPV6, HT_DOMAIN = range(5)
_pytransform = None

class PytransformError(Exception):
    pass


def dllmethod(func):

    def wrap(*args, **kwargs):
        return func(*args, **kwargs)

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


def get_hd_info(hdtype, size=256):
    if hdtype not in range(HT_DOMAIN + 1):
        raise RuntimeError('Invalid parameter hdtype: %s' % hdtype)
    t_buf = c_char * size
    buf = t_buf()
    if _pytransform.get_hd_info(hdtype, buf, size) == -1:
        raise PytransformError('Get hardware information failed')
    return buf.value.decode()


def show_hd_info():
    return _pytransform.show_hd_info()


def get_license_info():
    info = {'EXPIRED':None, 
     'HARDDISK':None, 
     'IFMAC':None, 
     'IFIPV4':None, 
     'DOMAIN':None, 
     'DATA':None, 
     'CODE':None}
    rcode = get_registration_code().decode()
    index = 0
    if rcode.startswith('*TIME:'):
        from time import ctime
        index = rcode.find('\n')
        info['EXPIRED'] = ctime(float(rcode[6:index]))
        index += 1
    if rcode[index:].startswith('*FLAGS:'):
        index += len('*FLAGS:') + 1
        info['FLAGS'] = ord(rcode[(index - 1)])
    prev = None
    start = index
    for k in ('HARDDISK', 'IFMAC', 'IFIPV4', 'DOMAIN', 'FIXKEY', 'CODE'):
        index = rcode.find('*%s:' % k)
        if index > -1:
            if prev is not None:
                info[prev] = rcode[start:index]
            prev = k
            start = index + len(k) + 2
        info['CODE'] = rcode[start:]
        i = info['CODE'].find(';')
        if i > 0:
            info['DATA'] = info['CODE'][i + 1:]
            info['CODE'] = info['CODE'][:i]
        return info


def get_license_code():
    return get_license_info()['CODE']


def _match_features(patterns, s):
    for pat in patterns:
        if fnmatch(s, pat):
            return True


def _gnu_get_libc_version--- This code section failed: ---

 L. 190         0  SETUP_FINALLY        46  'to 46'

 L. 191         2  LOAD_GLOBAL              CFUNCTYPE
                4  LOAD_GLOBAL              c_char_p
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'prototype'

 L. 192        10  LOAD_FAST                'prototype'
               12  LOAD_STR                 'gnu_get_libc_version'
               14  LOAD_GLOBAL              cdll
               16  LOAD_METHOD              LoadLibrary
               18  LOAD_STR                 ''
               20  CALL_METHOD_1         1  ''
               22  BUILD_TUPLE_2         2 
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'ver'

 L. 193        30  LOAD_FAST                'ver'
               32  LOAD_METHOD              decode
               34  CALL_METHOD_0         0  ''
               36  LOAD_METHOD              split
               38  LOAD_STR                 '.'
               40  CALL_METHOD_1         1  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY     0  '0'

 L. 194        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    64  'to 64'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 195        60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            52  '52'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_TOP' instruction at offset 56


def format_platform(platid=None):
    if platid:
        return os.path.normpath(platid)
        plat = platform.system().lower()
        mach = platform.machine().lower()
        for alias, platlist in plat_table:
            if _match_features(platlist, plat):
                plat = alias
                break
            if plat == 'linux':
                cname, cver = platform.libc_ver()
                if cname == 'musl':
                    plat = 'alpine'
            elif cname == 'libc':
                plat = 'android'

    else:
        if cname == 'glibc':
            v = _gnu_get_libc_version()
            if v:
                if len(v) >= 2:
                    if int(v[0]) * 100 + int(v[1]) < 214:
                        plat = 'centos6'
        else:
            for alias, archlist in arch_table:
                if _match_features(archlist, mach):
                    mach = alias
                    break
            else:
                if plat == 'windows':
                    if mach == 'x86_64':
                        bitness = struct.calcsize('P'.encode()) * 8
                        if bitness == 32:
                            mach = 'x86'

        return os.path.join(plat, mach)


def _load_library(path=None, is_runtime=0, platid=None, suffix=''):
    path = os.path.dirname(__file__) if path is None else os.path.normpath(path)
    plat = platform.system().lower()
    name = '_pytransform' + suffix
    if plat == 'linux':
        filename = os.path.abspath(os.path.join(path, name + '.so'))
    else:
        if plat == 'darwin':
            filename = os.path.join(path, name + '.dylib')
        else:
            if plat == 'windows':
                filename = os.path.join(path, name + '.dll')
            else:
                if plat == 'freebsd':
                    filename = os.path.join(path, name + '.so')
                else:
                    raise PytransformError('Platform %s not supported' % plat)
    if not ((platid is not None or os.path.exists)(filename) and is_runtime):
        libpath = platid if (platid is not None and os.path.isabs(platid)) else (os.path.join(path, plat_path, format_platform(platid)))
        filename = os.path.join(libpath, os.path.basename(filename))
    if not os.path.exists(filename):
        raise PytransformError('Could not find "%s"' % filename)
    try:
        m = cdll.LoadLibrary(filename)
    except Exception as e:
        try:
            if sys.flags.debug:
                print('Load %s failed:\n%s' % (filename, e))
            raise
        finally:
            e = None
            del e

    else:
        if not os.path.abspath('.') == os.path.abspath(path):
            m.set_option(1, path.encode() if sys.version_info[0] == 3 else path)
        m.set_option(2, sys.byteorder.encode())
        if sys.flags.debug:
            m.set_option(3, c_char_p(1))
        m.set_option(4, c_char_p(not is_runtime))
        if suffix:
            m.set_option(6, suffix.encode())
        return m


def pyarmor_init(path=None, is_runtime=0, platid=None, suffix=''):
    global _pytransform
    _pytransform = _load_library(path, is_runtime, platid, suffix)
    return init_pytransform()


def pyarmor_runtime(path=None, suffix=''):
    pyarmor_init(path, is_runtime=1, suffix=suffix)
    init_runtime()


def generate_capsule(licfile):
    prikey, pubkey, prolic = _generate_project_capsule()
    capkey, newkey = _generate_pytransform_key(licfile, pubkey)
    return (prikey, pubkey, capkey, newkey, prolic)


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
    return (prikey, pubkey, capkey, prolic)


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