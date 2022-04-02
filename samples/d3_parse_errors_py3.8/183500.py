# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\bindings\openssl\binding.py
from __future__ import absolute_import, division, print_function
import collections, threading, types, warnings, cryptography
from cryptography import utils
from cryptography.exceptions import InternalError
from cryptography.hazmat.bindings._openssl import ffi, lib
from cryptography.hazmat.bindings.openssl._conditional import CONDITIONAL_NAMES
_OpenSSLErrorWithText = collections.namedtuple('_OpenSSLErrorWithText', ['code', 'lib', 'func', 'reason', 'reason_text'])

class _OpenSSLError(object):

    def __init__(self, code, lib, func, reason):
        self._code = code
        self._lib = lib
        self._func = func
        self._reason = reason

    def _lib_reason_match(self, lib, reason):
        return lib == self.lib and reason == self.reason

    code = utils.read_only_property('_code')
    lib = utils.read_only_property('_lib')
    func = utils.read_only_property('_func')
    reason = utils.read_only_property('_reason')


def _consume_errors(lib):
    errors = []
    while True:
        code = lib.ERR_get_error()
        if code == 0:
            pass
        else:
            err_lib = lib.ERR_GET_LIB(code)
            err_func = lib.ERR_GET_FUNC(code)
            err_reason = lib.ERR_GET_REASON(code)
            errors.append(_OpenSSLError(code, err_lib, err_func, err_reason))

    return errors


def _openssl_assert(lib, ok):
    if not ok:
        errors = _consume_errors(lib)
        errors_with_text = []
        for err in errors:
            buf = ffi.new('char[]', 256)
            lib.ERR_error_string_n(err.code, buf, len(buf))
            err_text_reason = ffi.string(buf)
            errors_with_text.append(_OpenSSLErrorWithText(err.code, err.lib, err.func, err.reason, err_text_reason))
        else:
            raise InternalError('Unknown OpenSSL error. This error is commonly encountered when another library is not cleaning up the OpenSSL error stack. If you are using cryptography with another library that uses OpenSSL try disabling it before reporting a bug. Otherwise please file an issue at https://github.com/pyca/cryptography/issues with information on how to reproduce this. ({0!r})'.format(errors_with_text), errors_with_text)


def build_conditional_library(lib, conditional_names):
    conditional_lib = types.ModuleType('lib')
    conditional_lib._original_lib = lib
    excluded_names = set()
    for condition, names_cb in conditional_names.items():
        if not getattr(lib, condition):
            excluded_names.update(names_cb())
    else:
        for attr in dir(lib):
            if attr not in excluded_names:
                setattr(conditional_lib, attr, getattr(lib, attr))
        else:
            return conditional_lib


class Binding(object):
    __doc__ = '\n    OpenSSL API wrapper.\n    '
    lib = None
    ffi = ffi
    _lib_loaded = False
    _init_lock = threading.Lock()
    _lock_init_lock = threading.Lock()

    def __init__(self):
        self._ensure_ffi_initialized()

    @classmethod
    def _register_osrandom_engine(cls):
        cls.lib.ERR_clear_error()
        if cls.lib.Cryptography_HAS_ENGINE:
            result = cls.lib.Cryptography_add_osrandom_engine()
            _openssl_assert(cls.lib, result in (1, 2))

    @classmethod
    def _ensure_ffi_initialized(cls):
        with cls._init_lock:
            if not cls._lib_loaded:
                cls.lib = build_conditional_library(lib, CONDITIONAL_NAMES)
                cls._lib_loaded = True
                cls.lib.SSL_library_init()
                cls.lib.OpenSSL_add_all_algorithms()
                cls.lib.SSL_load_error_strings()
                cls._register_osrandom_engine()

    @classmethod
    def init_static_locks--- This code section failed: ---

 L. 138         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                _lock_init_lock
                4  SETUP_WITH           92  'to 92'
                6  POP_TOP          

 L. 139         8  LOAD_FAST                'cls'
               10  LOAD_METHOD              _ensure_ffi_initialized
               12  CALL_METHOD_0         0  ''
               14  POP_TOP          

 L. 142        16  LOAD_GLOBAL              __import__
               18  LOAD_STR                 '_ssl'
               20  CALL_FUNCTION_1       1  ''
               22  POP_TOP          

 L. 144        24  LOAD_FAST                'cls'
               26  LOAD_ATTR                lib
               28  LOAD_ATTR                Cryptography_HAS_LOCKING_CALLBACKS
               30  POP_JUMP_IF_FALSE    50  'to 50'

 L. 145        32  LOAD_FAST                'cls'
               34  LOAD_ATTR                lib
               36  LOAD_METHOD              CRYPTO_get_locking_callback
               38  CALL_METHOD_0         0  ''
               40  LOAD_FAST                'cls'
               42  LOAD_ATTR                ffi
               44  LOAD_ATTR                NULL
               46  COMPARE_OP               !=

 L. 144        48  POP_JUMP_IF_FALSE    64  'to 64'
             50_0  COME_FROM            30  '30'

 L. 146        50  POP_BLOCK        
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            48  '48'

 L. 150        64  LOAD_GLOBAL              lib
               66  LOAD_METHOD              Cryptography_setup_ssl_threads
               68  CALL_METHOD_0         0  ''
               70  STORE_FAST               'res'

 L. 151        72  LOAD_GLOBAL              _openssl_assert
               74  LOAD_FAST                'cls'
               76  LOAD_ATTR                lib
               78  LOAD_FAST                'res'
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  CALL_FUNCTION_2       2  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH        4  '4'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 52


def _verify_openssl_version(lib):
    if lib.CRYPTOGRAPHY_OPENSSL_LESS_THAN_102:
        if not lib.CRYPTOGRAPHY_IS_LIBRESSL:
            warnings.warn('OpenSSL version 1.0.1 is no longer supported by the OpenSSL project, please upgrade. The next version of cryptography will drop support for it.', utils.CryptographyDeprecationWarning)


def _verify_package_version(version):
    so_package_version = ffi.string(lib.CRYPTOGRAPHY_PACKAGE_VERSION)
    if version.encode('ascii') != so_package_version:
        raise ImportError('The version of cryptography does not match the loaded shared object. This can happen if you have multiple copies of cryptography installed in your Python path. Please try creating a new virtual environment to resolve this issue. Loaded python version: {}, shared object version: {}'.format(version, so_package_version))


_verify_package_version(cryptography.__version__)
Binding.init_static_locks()
_verify_openssl_version(Binding.lib)