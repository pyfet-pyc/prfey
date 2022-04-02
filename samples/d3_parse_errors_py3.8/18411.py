# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\Crypto\Util\_raw_api.py
import abc, sys
from Crypto.Util.py3compat import byte_string
from Crypto.Util._file_system import pycryptodome_filename
if sys.version_info[0] < 3:
    import imp
    extension_suffixes = []
    for ext, mod, typ in imp.get_suffixes():
        if typ == imp.C_EXTENSION:
            extension_suffixes.append(ext)

else:
    from importlib import machinery
    extension_suffixes = machinery.EXTENSION_SUFFIXES
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    _buffer_type = bytearray
else:
    _buffer_type = (
     bytearray, memoryview)

class _VoidPointer(object):

    @abc.abstractmethod
    def get(self):
        """Return the memory location we point to"""
        pass

    @abc.abstractmethod
    def address_of(self):
        """Return a raw pointer to this pointer"""
        pass


try:
    if sys.version_info[0] == 2:
        if sys.version_info[1] < 7:
            raise ImportError('CFFI is only supported with Python 2.7+')
    if '__pypy__' not in sys.builtin_module_names:
        if sys.flags.optimize == 2:
            raise ImportError('CFFI with optimize=2 fails due to pycparser bug.')
    from cffi import FFI
    ffi = FFI()
    null_pointer = ffi.NULL
    uint8_t_type = ffi.typeof(ffi.new('const uint8_t*'))
    _Array = ffi.new('uint8_t[1]').__class__.__bases__

    def load_lib(name, cdecl):
        """Load a shared library and return a handle to it.

        @name,  either an absolute path or the name of a library
                in the system search path.

        @cdecl, the C function declarations.
        """
        lib = ffi.dlopen(name)
        ffi.cdef(cdecl)
        return lib


    def c_ulong(x):
        """Convert a Python integer to unsigned long"""
        return x


    c_ulonglong = c_ulong
    c_uint = c_ulong

    def c_size_t(x):
        """Convert a Python integer to size_t"""
        return x


    def create_string_buffer(init_or_size, size=None):
        """Allocate the given amount of bytes (initially set to 0)"""
        if isinstance(init_or_size, bytes):
            size = max(len(init_or_size) + 1, size)
            result = ffi.new('uint8_t[]', size)
            result[:] = init_or_size
        else:
            if size:
                raise ValueError('Size must be specified once only')
            result = ffi.new('uint8_t[]', init_or_size)
        return result


    def get_c_string(c_string):
        """Convert a C string into a Python byte sequence"""
        return ffi.string(c_string)


    def get_raw_buffer(buf):
        """Convert a C buffer into a Python byte sequence"""
        return ffi.buffer(buf)[:]


    def c_uint8_ptr(data):
        if isinstance(data, _buffer_type):
            return ffi.cast(uint8_t_type, ffi.from_buffer(data))
        if byte_string(data) or (isinstance(data, _Array)):
            return data
        raise TypeError('Object type %s cannot be passed to C code' % type(data))


    class VoidPointer_cffi(_VoidPointer):
        __doc__ = 'Model a newly allocated pointer to void'

        def __init__(self):
            self._pp = ffi.new('void *[1]')

        def get(self):
            return self._pp[0]

        def address_of(self):
            return self._pp


    def VoidPointer():
        return VoidPointer_cffi()


    backend = 'cffi'
except ImportError:
    import ctypes
    from ctypes import CDLL, c_void_p, byref, c_ulong, c_ulonglong, c_size_t, create_string_buffer, c_ubyte, c_uint
    from ctypes.util import find_library
    from ctypes import Array as _Array
    null_pointer = None

    def load_lib(name, cdecl):
        import platform
        bits, linkage = platform.architecture()
        if '.' not in name:
            if not linkage.startswith('Win'):
                full_name = find_library(name)
                if full_name is None:
                    raise OSError("Cannot load library '%s'" % name)
                name = full_name
            return CDLL(name)


    def get_c_string(c_string):
        return c_string.value


    def get_raw_buffer(buf):
        return buf.raw


    if sys.version_info[0] == 2 and sys.version_info[1] == 6:
        _c_ssize_t = c_size_t
    else:
        _c_ssize_t = ctypes.c_ssize_t
    _PyBUF_SIMPLE = 0
    _PyObject_GetBuffer = ctypes.pythonapi.PyObject_GetBuffer
    _PyBuffer_Release = ctypes.pythonapi.PyBuffer_Release
    _py_object = ctypes.py_object
    _c_ssize_p = ctypes.POINTER(_c_ssize_t)

    class _Py_buffer(ctypes.Structure):
        _fields_ = [
         (
          'buf', c_void_p),
         (
          'obj', ctypes.py_object),
         (
          'len', _c_ssize_t),
         (
          'itemsize', _c_ssize_t),
         (
          'readonly', ctypes.c_int),
         (
          'ndim', ctypes.c_int),
         (
          'format', ctypes.c_char_p),
         (
          'shape', _c_ssize_p),
         (
          'strides', _c_ssize_p),
         (
          'suboffsets', _c_ssize_p),
         (
          'internal', c_void_p)]
        if sys.version_info[0] == 2:
            _fields_.insert(-1, ('smalltable', _c_ssize_t * 2))


    def c_uint8_ptr--- This code section failed: ---

 L. 226         0  LOAD_GLOBAL              byte_string
                2  LOAD_FAST                'data'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     18  'to 18'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'data'
               12  LOAD_GLOBAL              _Array
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'
             18_0  COME_FROM             6  '6'

 L. 227        18  LOAD_FAST                'data'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 228        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'data'
               26  LOAD_GLOBAL              _buffer_type
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE   106  'to 106'

 L. 229        32  LOAD_GLOBAL              _py_object
               34  LOAD_FAST                'data'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'obj'

 L. 230        40  LOAD_GLOBAL              _Py_buffer
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'buf'

 L. 231        46  LOAD_GLOBAL              _PyObject_GetBuffer
               48  LOAD_FAST                'obj'
               50  LOAD_GLOBAL              byref
               52  LOAD_FAST                'buf'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_GLOBAL              _PyBUF_SIMPLE
               58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          

 L. 232        62  SETUP_FINALLY        90  'to 90'

 L. 233        64  LOAD_GLOBAL              c_ubyte
               66  LOAD_FAST                'buf'
               68  LOAD_ATTR                len
               70  BINARY_MULTIPLY  
               72  STORE_FAST               'buffer_type'

 L. 234        74  LOAD_FAST                'buffer_type'
               76  LOAD_METHOD              from_address
               78  LOAD_FAST                'buf'
               80  LOAD_ATTR                buf
               82  CALL_METHOD_1         1  ''
               84  POP_BLOCK        
               86  CALL_FINALLY         90  'to 90'
               88  RETURN_VALUE     
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM_FINALLY    62  '62'

 L. 236        90  LOAD_GLOBAL              _PyBuffer_Release
               92  LOAD_GLOBAL              byref
               94  LOAD_FAST                'buf'
               96  CALL_FUNCTION_1       1  ''
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          
              102  END_FINALLY      
              104  JUMP_FORWARD        122  'to 122'
            106_0  COME_FROM            30  '30'

 L. 238       106  LOAD_GLOBAL              TypeError
              108  LOAD_STR                 'Object type %s cannot be passed to C code'
              110  LOAD_GLOBAL              type
              112  LOAD_FAST                'data'
              114  CALL_FUNCTION_1       1  ''
              116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           104  '104'

Parse error at or near `CALL_FINALLY' instruction at offset 86


    class VoidPointer_ctypes(_VoidPointer):
        __doc__ = 'Model a newly allocated pointer to void'

        def __init__(self):
            self._p = c_void_p()

        def get(self):
            return self._p

        def address_of(self):
            return byref(self._p)


    def VoidPointer():
        return VoidPointer_ctypes()


    backend = 'ctypes'
    del ctypes
else:

    class SmartPointer(object):
        __doc__ = 'Class to hold a non-managed piece of memory'

        def __init__(self, raw_pointer, destructor):
            self._raw_pointer = raw_pointer
            self._destructor = destructor

        def get(self):
            return self._raw_pointer

        def release(self):
            rp, self._raw_pointer = self._raw_pointer, None
            return rp

        def __del__(self):
            try:
                if self._raw_pointer is not None:
                    self._destructor(self._raw_pointer)
                    self._raw_pointer = None
            except AttributeError:
                pass


    def load_pycryptodome_raw_lib--- This code section failed: ---

 L. 293         0  LOAD_FAST                'name'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'split'

 L. 294        10  LOAD_FAST                'split'
               12  LOAD_CONST               None
               14  LOAD_CONST               -1
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_FAST                'split'
               22  LOAD_CONST               -1
               24  BINARY_SUBSCR    
               26  ROT_TWO          
               28  STORE_FAST               'dir_comps'
               30  STORE_FAST               'basename'

 L. 295        32  BUILD_LIST_0          0 
               34  STORE_FAST               'attempts'

 L. 296        36  LOAD_GLOBAL              extension_suffixes
               38  GET_ITER         
             40_0  COME_FROM           132  '132'
             40_1  COME_FROM           128  '128'
               40  FOR_ITER            134  'to 134'
               42  STORE_FAST               'ext'

 L. 297        44  SETUP_FINALLY        76  'to 76'

 L. 298        46  LOAD_FAST                'basename'
               48  LOAD_FAST                'ext'
               50  BINARY_ADD       
               52  STORE_FAST               'filename'

 L. 299        54  LOAD_GLOBAL              load_lib
               56  LOAD_GLOBAL              pycryptodome_filename
               58  LOAD_FAST                'dir_comps'
               60  LOAD_FAST                'filename'
               62  CALL_FUNCTION_2       2  ''

 L. 300        64  LOAD_FAST                'cdecl'

 L. 299        66  CALL_FUNCTION_2       2  ''
               68  POP_BLOCK        
               70  ROT_TWO          
               72  POP_TOP          
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    44  '44'

 L. 301        76  DUP_TOP          
               78  LOAD_GLOBAL              OSError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   130  'to 130'
               84  POP_TOP          
               86  STORE_FAST               'exp'
               88  POP_TOP          
               90  SETUP_FINALLY       118  'to 118'

 L. 302        92  LOAD_FAST                'attempts'
               94  LOAD_METHOD              append
               96  LOAD_STR                 "Trying '%s': %s"
               98  LOAD_FAST                'filename'
              100  LOAD_GLOBAL              str
              102  LOAD_FAST                'exp'
              104  CALL_FUNCTION_1       1  ''
              106  BUILD_TUPLE_2         2 
              108  BINARY_MODULO    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_FINALLY    90  '90'
              118  LOAD_CONST               None
              120  STORE_FAST               'exp'
              122  DELETE_FAST              'exp'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_BACK            40  'to 40'
            130_0  COME_FROM            82  '82'
              130  END_FINALLY      
              132  JUMP_BACK            40  'to 40'
            134_0  COME_FROM            40  '40'

 L. 303       134  LOAD_GLOBAL              OSError
              136  LOAD_STR                 "Cannot load native module '%s': %s"
              138  LOAD_FAST                'name'
              140  LOAD_STR                 ', '
              142  LOAD_METHOD              join
              144  LOAD_FAST                'attempts'
              146  CALL_METHOD_1         1  ''
              148  BUILD_TUPLE_2         2 
              150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 70


if sys.version_info[:2] != (2, 6):

    def is_buffer(x):
        """Return True if object x supports the buffer interface"""
        return isinstance(x, (bytes, bytearray, memoryview))


    def is_writeable_buffer(x):
        return (isinstance(x, bytearray)) or ((isinstance(x, memoryview)) and (not x.readonly))


else:

    def is_buffer(x):
        return isinstance(x, (bytes, bytearray))


    def is_writeable_buffer(x):
        return isinstance(x, bytearray)