# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cffi\api.py
import sys, types
from .lock import allocate_lock
from .error import CDefError
from . import model
try:
    callable
except NameError:
    from collections import Callable
    callable = lambda x: isinstance(x, Callable)
else:
    try:
        basestring
    except NameError:
        basestring = str
    else:
        _unspecified = object()

        class FFI(object):
            __doc__ = '\n    The main top-level class that you instantiate once, or once per module.\n\n    Example usage:\n\n        ffi = FFI()\n        ffi.cdef("""\n            int printf(const char *, ...);\n        """)\n\n        C = ffi.dlopen(None)   # standard library\n        -or-\n        C = ffi.verify()  # use a C compiler: verify the decl above is right\n\n        C.printf("hello, %s!\\n", ffi.new("char[]", "world"))\n    '

            def __init__(self, backend=None):
                """Create an FFI instance.  The 'backend' argument is used to
        select a non-default backend, mostly for tests.
        """
                if backend is None:
                    import _cffi_backend as backend
                    from . import __version__
                    if backend.__version__ != __version__:
                        if hasattr(backend, '__file__'):
                            raise Exception("Version mismatch: this is the 'cffi' package version %s, located in %r.  When we import the top-level '_cffi_backend' extension module, we get version %s, located in %r.  The two versions should be equal; check your installation." % (
                             __version__, __file__,
                             backend.__version__, backend.__file__))
                        else:
                            raise Exception("Version mismatch: this is the 'cffi' package version %s, located in %r.  This interpreter comes with a built-in '_cffi_backend' module, which is version %s.  The two versions should be equal; check your installation." % (
                             __version__, __file__, backend.__version__))
                from . import cparser
                self._backend = backend
                self._lock = allocate_lock()
                self._parser = cparser.Parser()
                self._cached_btypes = {}
                self._parsed_types = types.ModuleType('parsed_types').__dict__
                self._new_types = types.ModuleType('new_types').__dict__
                self._function_caches = []
                self._libraries = []
                self._cdefsources = []
                self._included_ffis = []
                self._windows_unicode = None
                self._init_once_cache = {}
                self._cdef_version = None
                self._embedding = None
                self._typecache = model.get_typecache(backend)
                if hasattr(backend, 'set_ffi'):
                    backend.set_ffi(self)
                for name in list(backend.__dict__):
                    if name.startswith('RTLD_'):
                        setattr(self, name, getattr(backend, name))
                else:
                    with self._lock:
                        self.BVoidP = self._get_cached_btype(model.voidp_type)
                        self.BCharA = self._get_cached_btype(model.char_array_type)
                    if isinstance(backend, types.ModuleType):
                        FFI.NULL = hasattr(FFI, 'NULL') or self.cast(self.BVoidP, 0)
                        FFI.CData, FFI.CType = backend._get_types()
                    else:
                        self.NULL = self.cast(self.BVoidP, 0)
                        self.CData, self.CType = backend._get_types()
                    self.buffer = backend.buffer

            def cdef(self, csource, override=False, packed=False, pack=None):
                """Parse the given C source.  This registers all declared functions,
        types, and global variables.  The functions and global variables can
        then be accessed via either 'ffi.dlopen()' or 'ffi.verify()'.
        The types can be used in 'ffi.new()' and other functions.
        If 'packed' is specified as True, all structs declared inside this
        cdef are packed, i.e. laid out without any field alignment at all.
        Alternatively, 'pack' can be a small integer, and requests for
        alignment greater than that are ignored (pack=1 is equivalent to
        packed=True).
        """
                self._cdef(csource, override=override, packed=packed, pack=pack)

            def embedding_api(self, csource, packed=False, pack=None):
                self._cdef(csource, packed=packed, pack=pack, dllexport=True)
                if self._embedding is None:
                    self._embedding = ''

            def _cdef(self, csource, override=False, **options):
                if not isinstance(csource, str):
                    if not isinstance(csource, basestring):
                        raise TypeError('cdef() argument must be a string')
                    csource = csource.encode('ascii')
                with self._lock:
                    self._cdef_version = object()
                    (self._parser.parse)(csource, override=override, **options)
                    self._cdefsources.append(csource)
                    if override:
                        for cache in self._function_caches:
                            cache.clear()

                    finishlist = self._parser._recomplete
                    if finishlist:
                        self._parser._recomplete = []
                        for tp in finishlist:
                            tp.finish_backend_type(self, finishlist)

            def dlopen(self, name, flags=0):
                """Load and return a dynamic library identified by 'name'.
        The standard C library can be loaded by passing None.
        Note that functions and types declared by 'ffi.cdef()' are not
        linked to a particular library, just like C headers; in the
        library we only look for the actual (untyped) symbols.
        """
                if not isinstance(name, basestring):
                    assert name is None
                with self._lock:
                    lib, function_cache = _make_ffi_library(self, name, flags)
                    self._function_caches.append(function_cache)
                    self._libraries.append(lib)
                return lib

            def dlclose(self, lib):
                """Close a library obtained with ffi.dlopen().  After this call,
        access to functions or variables from the library will fail
        (possibly with a segmentation fault).
        """
                type(lib).__cffi_close__(lib)

            def _typeof_locked(self, cdecl):
                key = cdecl
                if key in self._parsed_types:
                    return self._parsed_types[key]
                if not isinstance(cdecl, str):
                    cdecl = cdecl.encode('ascii')
                type = self._parser.parse_type(cdecl)
                really_a_function_type = type.is_raw_function
                if really_a_function_type:
                    type = type.as_function_pointer()
                btype = self._get_cached_btype(type)
                result = (btype, really_a_function_type)
                self._parsed_types[key] = result
                return result

            def _typeof(self, cdecl, consider_function_as_funcptr=False):
                try:
                    result = self._parsed_types[cdecl]
                except KeyError:
                    with self._lock:
                        result = self._typeof_locked(cdecl)
                else:
                    btype, really_a_function_type = result
                    if really_a_function_type:
                        if not consider_function_as_funcptr:
                            raise CDefError('the type %r is a function type, not a pointer-to-function type' % (
                             cdecl,))
                    return btype

            def typeof--- This code section failed: ---

 L. 195         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'cdecl'
                4  LOAD_GLOBAL              basestring
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 196        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _typeof
               14  LOAD_FAST                'cdecl'
               16  CALL_METHOD_1         1  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 197        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'cdecl'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                CData
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L. 198        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _backend
               36  LOAD_METHOD              typeof
               38  LOAD_FAST                'cdecl'
               40  CALL_METHOD_1         1  ''
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'

 L. 199        44  LOAD_GLOBAL              isinstance
               46  LOAD_FAST                'cdecl'
               48  LOAD_GLOBAL              types
               50  LOAD_ATTR                BuiltinFunctionType
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    76  'to 76'

 L. 200        56  LOAD_GLOBAL              _builtin_function_type
               58  LOAD_FAST                'cdecl'
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'res'

 L. 201        64  LOAD_FAST                'res'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 202        72  LOAD_FAST                'res'
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            54  '54'

 L. 203        76  LOAD_GLOBAL              isinstance
               78  LOAD_FAST                'cdecl'
               80  LOAD_GLOBAL              types
               82  LOAD_ATTR                FunctionType
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   136  'to 136'

 L. 204        88  LOAD_GLOBAL              hasattr
               90  LOAD_FAST                'cdecl'
               92  LOAD_STR                 '_cffi_base_type'
               94  CALL_FUNCTION_2       2  ''

 L. 203        96  POP_JUMP_IF_FALSE   136  'to 136'

 L. 205        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _lock
              102  SETUP_WITH          130  'to 130'
              104  POP_TOP          

 L. 206       106  LOAD_FAST                'self'
              108  LOAD_METHOD              _get_cached_btype
              110  LOAD_FAST                'cdecl'
              112  LOAD_ATTR                _cffi_base_type
              114  CALL_METHOD_1         1  ''
              116  POP_BLOCK        
              118  ROT_TWO          
              120  BEGIN_FINALLY    
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  POP_FINALLY           0  ''
              128  RETURN_VALUE     
            130_0  COME_FROM_WITH      102  '102'
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  END_FINALLY      
            136_0  COME_FROM            96  '96'
            136_1  COME_FROM            86  '86'

 L. 207       136  LOAD_GLOBAL              TypeError
              138  LOAD_GLOBAL              type
              140  LOAD_FAST                'cdecl'
              142  CALL_FUNCTION_1       1  ''
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 118

            def sizeof(self, cdecl):
                """Return the size in bytes of the argument.  It can be a
        string naming a C type, or a 'cdata' instance.
        """
                if isinstance(cdecl, basestring):
                    BType = self._typeof(cdecl)
                    return self._backend.sizeof(BType)
                return self._backend.sizeof(cdecl)

            def alignof(self, cdecl):
                """Return the natural alignment size in bytes of the C type
        given as a string.
        """
                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl)
                return self._backend.alignof(cdecl)

            def offsetof(self, cdecl, *fields_or_indexes):
                """Return the offset of the named field inside the given
        structure or array, which must be given as a C type name.
        You can give several field names in case of nested structures.
        You can also give numeric values which correspond to array
        items, in case of an array type.
        """
                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl)
                return (self._typeoffsetof)(cdecl, *fields_or_indexes)[1]

            def new(self, cdecl, init=None):
                """Allocate an instance according to the specified C type and
        return a pointer to it.  The specified C type must be either a
        pointer or an array: ``new('X *')`` allocates an X and returns
        a pointer to it, whereas ``new('X[n]')`` allocates an array of
        n X'es and returns an array referencing it (which works
        mostly like a pointer, like in C).  You can also use
        ``new('X[]', n)`` to allocate an array of a non-constant
        length n.

        The memory is initialized following the rules of declaring a
        global variable in C: by default it is zero-initialized, but
        an explicit initializer can be given which can be used to
        fill all or part of the memory.

        When the returned <cdata> object goes out of scope, the memory
        is freed.  In other words the returned <cdata> object has
        ownership of the value of type 'cdecl' that it points to.  This
        means that the raw data can be used as long as this object is
        kept alive, but must not be used for a longer time.  Be careful
        about that when copying the pointer to the memory somewhere
        else, e.g. into another structure.
        """
                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl)
                return self._backend.newp(cdecl, init)

            def new_allocator(self, alloc=None, free=None, should_clear_after_alloc=True):
                """Return a new allocator, i.e. a function that behaves like ffi.new()
        but uses the provided low-level 'alloc' and 'free' functions.

        'alloc' is called with the size as argument.  If it returns NULL, a
        MemoryError is raised.  'free' is called with the result of 'alloc'
        as argument.  Both can be either Python function or directly C
        functions.  If 'free' is None, then no free function is called.
        If both 'alloc' and 'free' are None, the default is used.

        If 'should_clear_after_alloc' is set to False, then the memory
        returned by 'alloc' is assumed to be already cleared (or you are
        fine with garbage); otherwise CFFI will clear it.
        """
                compiled_ffi = self._backend.FFI()
                allocator = compiled_ffi.new_allocator(alloc, free, should_clear_after_alloc)

                def allocate(cdecl, init=None):
                    if isinstance(cdecl, basestring):
                        cdecl = self._typeof(cdecl)
                    return allocator(cdecl, init)

                return allocate

            def cast(self, cdecl, source):
                """Similar to a C cast: returns an instance of the named C
        type initialized with the given 'source'.  The source is
        casted between integers or pointers of any type.
        """
                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl)
                return self._backend.cast(cdecl, source)

            def string(self, cdata, maxlen=-1):
                """Return a Python string (or unicode string) from the 'cdata'.
        If 'cdata' is a pointer or array of characters or bytes, returns
        the null-terminated string.  The returned string extends until
        the first null character, or at most 'maxlen' characters.  If
        'cdata' is an array then 'maxlen' defaults to its length.

        If 'cdata' is a pointer or array of wchar_t, returns a unicode
        string following the same rules.

        If 'cdata' is a single character or byte or a wchar_t, returns
        it as a string or unicode string.

        If 'cdata' is an enum, returns the value of the enumerator as a
        string, or 'NUMBER' if the value is out of range.
        """
                return self._backend.string(cdata, maxlen)

            def unpack(self, cdata, length):
                """Unpack an array of C data of the given length,
        returning a Python string/unicode/list.

        If 'cdata' is a pointer to 'char', returns a byte string.
        It does not stop at the first null.  This is equivalent to:
        ffi.buffer(cdata, length)[:]

        If 'cdata' is a pointer to 'wchar_t', returns a unicode string.
        'length' is measured in wchar_t's; it is not the size in bytes.

        If 'cdata' is a pointer to anything else, returns a list of
        'length' items.  This is a faster equivalent to:
        [cdata[i] for i in range(length)]
        """
                return self._backend.unpack(cdata, length)

            def from_buffer(self, cdecl, python_buffer=_unspecified, require_writable=False):
                """Return a cdata of the given type pointing to the data of the
        given Python object, which must support the buffer interface.
        Note that this is not meant to be used on the built-in types
        str or unicode (you can build 'char[]' arrays explicitly)
        but only on objects containing large quantities of raw data
        in some other format, like 'array.array' or numpy arrays.

        The first argument is optional and default to 'char[]'.
        """
                if python_buffer is _unspecified:
                    cdecl, python_buffer = self.BCharA, cdecl
                else:
                    if isinstance(cdecl, basestring):
                        cdecl = self._typeof(cdecl)
                return self._backend.from_buffer(cdecl, python_buffer, require_writable)

            def memmove(self, dest, src, n):
                """ffi.memmove(dest, src, n) copies n bytes of memory from src to dest.

        Like the C function memmove(), the memory areas may overlap;
        apart from that it behaves like the C function memcpy().

        'src' can be any cdata ptr or array, or any Python buffer object.
        'dest' can be any cdata ptr or array, or a writable Python buffer
        object.  The size to copy, 'n', is always measured in bytes.

        Unlike other methods, this one supports all Python buffer including
        byte strings and bytearrays---but it still does not support
        non-contiguous buffers.
        """
                return self._backend.memmove(dest, src, n)

            def callback(self, cdecl, python_callable=None, error=None, onerror=None):
                """Return a callback object or a decorator making such a
        callback object.  'cdecl' must name a C function pointer type.
        The callback invokes the specified 'python_callable' (which may
        be provided either directly or via a decorator).  Important: the
        callback object must be manually kept alive for as long as the
        callback may be invoked from the C level.
        """

                def callback_decorator_wrap(python_callable):
                    if not callable(python_callable):
                        raise TypeError("the 'python_callable' argument is not callable")
                    return self._backend.callback(cdecl, python_callable, error, onerror)

                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl, consider_function_as_funcptr=True)
                if python_callable is None:
                    return callback_decorator_wrap
                return callback_decorator_wrap(python_callable)

            def getctype(self, cdecl, replace_with=''):
                """Return a string giving the C type 'cdecl', which may be itself
        a string or a <ctype> object.  If 'replace_with' is given, it gives
        extra text to append (or insert for more complicated C types), like
        a variable name, or '*' to get actually the C type 'pointer-to-cdecl'.
        """
                if isinstance(cdecl, basestring):
                    cdecl = self._typeof(cdecl)
                replace_with = replace_with.strip()
                if replace_with.startswith('*') and '&[' in self._backend.getcname(cdecl, '&'):
                    replace_with = '(%s)' % replace_with
                else:
                    if replace_with and replace_with[0] not in '[(':
                        replace_with = ' ' + replace_with
                return self._backend.getcname(cdecl, replace_with)

            def gc(self, cdata, destructor, size=0):
                """Return a new cdata object that points to the same
        data.  Later, when this new cdata object is garbage-collected,
        'destructor(old_cdata_object)' will be called.

        The optional 'size' gives an estimate of the size, used to
        trigger the garbage collection more eagerly.  So far only used
        on PyPy.  It tells the GC that the returned object keeps alive
        roughly 'size' bytes of external memory.
        """
                return self._backend.gcp(cdata, destructor, size)

            def _get_cached_btype(self, type):
                assert self._lock.acquire(False) is False
                try:
                    BType = self._cached_btypes[type]
                except KeyError:
                    finishlist = []
                    BType = type.get_cached_btype(self, finishlist)
                    for type in finishlist:
                        type.finish_backend_type(self, finishlist)

                else:
                    return BType

            def verify(self, source='', tmpdir=None, **kwargs):
                """Verify that the current ffi signatures compile on this
        machine, and return a dynamic library object.  The dynamic
        library can be used to call functions and access global
        variables declared in this 'ffi'.  The library is compiled
        by the C compiler: it gives you C-level API compatibility
        (including calling macros).  This is unlike 'ffi.dlopen()',
        which requires binary compatibility in the signatures.
        """
                from .verifier import Verifier, _caller_dir_pycache
                if self._windows_unicode:
                    self._apply_windows_unicode(kwargs)
                tmpdir = tmpdir or _caller_dir_pycache()
                self.verifier = Verifier(self, source, tmpdir, **kwargs)
                lib = self.verifier.load_library()
                self._libraries.append(lib)
                return lib

            def _get_errno(self):
                return self._backend.get_errno()

            def _set_errno(self, errno):
                self._backend.set_errno(errno)

            errno = property(_get_errno, _set_errno, None, "the value of 'errno' from/to the C calls")

            def getwinerror(self, code=-1):
                return self._backend.getwinerror(code)

            def _pointer_to--- This code section failed: ---

 L. 482         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           32  'to 32'
                6  POP_TOP          

 L. 483         8  LOAD_GLOBAL              model
               10  LOAD_METHOD              pointer_cache
               12  LOAD_FAST                'self'
               14  LOAD_FAST                'ctype'
               16  CALL_METHOD_2         2  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

            def addressof(self, cdata, *fields_or_indexes):
                """Return the address of a <cdata 'struct-or-union'>.
        If 'fields_or_indexes' are given, returns the address of that
        field or array item in the structure or array, recursively in
        case of nested structures.
        """
                try:
                    ctype = self._backend.typeof(cdata)
                except TypeError:
                    if '__addressof__' in type(cdata).__dict__:
                        return (type(cdata).__addressof__)(cdata, *fields_or_indexes)
                    raise
                else:
                    if fields_or_indexes:
                        ctype, offset = (self._typeoffsetof)(ctype, *fields_or_indexes)
                    else:
                        if ctype.kind == 'pointer':
                            raise TypeError('addressof(pointer)')
                        offset = 0
                    ctypeptr = self._pointer_to(ctype)
                    return self._backend.rawaddressof(ctypeptr, cdata, offset)

            def _typeoffsetof(self, ctype, field_or_index, *fields_or_indexes):
                ctype, offset = self._backend.typeoffsetof(ctype, field_or_index)
                for field1 in fields_or_indexes:
                    ctype, offset1 = self._backend.typeoffsetof(ctype, field1, 1)
                    offset += offset1
                else:
                    return (
                     ctype, offset)

            def include(self, ffi_to_include):
                """Includes the typedefs, structs, unions and enums defined
        in another FFI instance.  Usage is similar to a #include in C,
        where a part of the program might include types defined in
        another part for its own usage.  Note that the include()
        method has no effect on functions, constants and global
        variables, which must anyway be accessed directly from the
        lib object returned by the original FFI instance.
        """
                if not isinstance(ffi_to_include, FFI):
                    raise TypeError('ffi.include() expects an argument that is also of type cffi.FFI, not %r' % (
                     type(ffi_to_include).__name__,))
                if ffi_to_include is self:
                    raise ValueError('self.include(self)')
                with ffi_to_include._lock:
                    with self._lock:
                        self._parser.include(ffi_to_include._parser)
                        self._cdefsources.append('[')
                        self._cdefsources.extend(ffi_to_include._cdefsources)
                        self._cdefsources.append(']')
                        self._included_ffis.append(ffi_to_include)

            def new_handle(self, x):
                return self._backend.newp_handle(self.BVoidP, x)

            def from_handle(self, x):
                return self._backend.from_handle(x)

            def release(self, x):
                self._backend.release(x)

            def set_unicode(self, enabled_flag):
                """Windows: if 'enabled_flag' is True, enable the UNICODE and
        _UNICODE defines in C, and declare the types like TCHAR and LPTCSTR
        to be (pointers to) wchar_t.  If 'enabled_flag' is False,
        declare these types to be (pointers to) plain 8-bit characters.
        This is mostly for backward compatibility; you usually want True.
        """
                if self._windows_unicode is not None:
                    raise ValueError('set_unicode() can only be called once')
                else:
                    enabled_flag = bool(enabled_flag)
                    if enabled_flag:
                        self.cdef('typedef wchar_t TBYTE;typedef wchar_t TCHAR;typedef const wchar_t *LPCTSTR;typedef const wchar_t *PCTSTR;typedef wchar_t *LPTSTR;typedef wchar_t *PTSTR;typedef TBYTE *PTBYTE;typedef TCHAR *PTCHAR;')
                    else:
                        self.cdef('typedef char TBYTE;typedef char TCHAR;typedef const char *LPCTSTR;typedef const char *PCTSTR;typedef char *LPTSTR;typedef char *PTSTR;typedef TBYTE *PTBYTE;typedef TCHAR *PTCHAR;')
                self._windows_unicode = enabled_flag

            def _apply_windows_unicode(self, kwds):
                defmacros = kwds.get('define_macros', ())
                if not isinstance(defmacros, (list, tuple)):
                    raise TypeError("'define_macros' must be a list or tuple")
                defmacros = list(defmacros) + [('UNICODE', '1'),
                 ('_UNICODE', '1')]
                kwds['define_macros'] = defmacros

            def _apply_embedding_fix(self, kwds):

                def ensure(key, value):
                    lst = kwds.setdefault(key, [])
                    if value not in lst:
                        lst.append(value)

                if '__pypy__' in sys.builtin_module_names:
                    import os
                    if sys.platform == 'win32':
                        pythonlib = 'python{0[0]}{0[1]}'.format(sys.version_info)
                        if hasattr(sys, 'prefix'):
                            ensure('library_dirs', os.path.join(sys.prefix, 'libs'))
                        else:
                            if sys.version_info < (3, ):
                                pythonlib = 'pypy-c'
                            else:
                                pythonlib = 'pypy3-c'
                            if hasattr(sys, 'prefix'):
                                ensure('library_dirs', os.path.join(sys.prefix, 'bin'))
                        if hasattr(sys, 'prefix'):
                            ensure('library_dirs', os.path.join(sys.prefix, 'pypy', 'goal'))
                    else:
                        pass
                if sys.platform == 'win32':
                    template = 'python%d%d'
                    if hasattr(sys, 'gettotalrefcount'):
                        template += '_d'
                else:
                    try:
                        import sysconfig
                    except ImportError:
                        from distutils import sysconfig
                    else:
                        template = 'python%d.%d'
                        if sysconfig.get_config_var('DEBUG_EXT'):
                            template += sysconfig.get_config_var('DEBUG_EXT')
                        pythonlib = template % (
                         sys.hexversion >> 24, sys.hexversion >> 16 & 255)
                        if hasattr(sys, 'abiflags'):
                            pythonlib += sys.abiflags
                        ensure('libraries', pythonlib)
                        if sys.platform == 'win32':
                            ensure('extra_link_args', '/MANIFEST')

            def set_source(self, module_name, source, source_extension='.c', **kwds):
                import os
                if hasattr(self, '_assigned_source'):
                    raise ValueError('set_source() cannot be called several times per ffi object')
                if not isinstance(module_name, basestring):
                    raise TypeError("'module_name' must be a string")
                if (os.sep in module_name or os).altsep:
                    if os.altsep in module_name:
                        raise ValueError("'module_name' must not contain '/': use a dotted name to make a 'package.module' location")
                self._assigned_source = (
                 str(module_name), source,
                 source_extension, kwds)

            def set_source_pkgconfig(self, module_name, pkgconfig_libs, source, source_extension='.c', **kwds):
                from . import pkgconfig
                if not isinstance(pkgconfig_libs, list):
                    raise TypeError('the pkgconfig_libs argument must be a list of package names')
                kwds2 = pkgconfig.flags_from_pkgconfig(pkgconfig_libs)
                pkgconfig.merge_flags(kwds, kwds2)
                (self.set_source)(module_name, source, source_extension, **kwds)

            def distutils_extension(self, tmpdir='build', verbose=True):
                from distutils.dir_util import mkpath
                from .recompiler import recompile
                if not hasattr(self, '_assigned_source'):
                    if hasattr(self, 'verifier'):
                        return self.verifier.get_extension()
                    raise ValueError('set_source() must be called before distutils_extension()')
                else:
                    module_name, source, source_extension, kwds = self._assigned_source
                    if source is None:
                        raise TypeError('distutils_extension() is only for C extension modules, not for dlopen()-style pure Python modules')
                    mkpath(tmpdir)
                    ext, updated = recompile(self, module_name,
 source, tmpdir=tmpdir, 
                     extradir=tmpdir, source_extension=source_extension, 
                     call_c_compiler=False, **kwds)
                    if verbose:
                        if updated:
                            sys.stderr.write('regenerated: %r\n' % (ext.sources[0],))
                        else:
                            sys.stderr.write('not modified: %r\n' % (ext.sources[0],))
                return ext

            def emit_c_code(self, filename):
                from .recompiler import recompile
                if not hasattr(self, '_assigned_source'):
                    raise ValueError('set_source() must be called before emit_c_code()')
                module_name, source, source_extension, kwds = self._assigned_source
                if source is None:
                    raise TypeError('emit_c_code() is only for C extension modules, not for dlopen()-style pure Python modules')
                recompile(self, module_name, source, c_file=filename, 
                 call_c_compiler=False, **kwds)

            def emit_python_code(self, filename):
                from .recompiler import recompile
                if not hasattr(self, '_assigned_source'):
                    raise ValueError('set_source() must be called before emit_c_code()')
                module_name, source, source_extension, kwds = self._assigned_source
                if source is not None:
                    raise TypeError('emit_python_code() is only for dlopen()-style pure Python modules, not for C extension modules')
                recompile(self, module_name, source, c_file=filename, 
                 call_c_compiler=False, **kwds)

            def compile(self, tmpdir='.', verbose=0, target=None, debug=None):
                """The 'target' argument gives the final file name of the
        compiled DLL.  Use '*' to force distutils' choice, suitable for
        regular CPython C API modules.  Use a file name ending in '.*'
        to ask for the system's default extension for dynamic libraries
        (.so/.dll/.dylib).

        The default is '*' when building a non-embedded C API extension,
        and (module_name + '.*') when building an embedded library.
        """
                from .recompiler import recompile
                if not hasattr(self, '_assigned_source'):
                    raise ValueError('set_source() must be called before compile()')
                module_name, source, source_extension, kwds = self._assigned_source
                return recompile(self, module_name, source, tmpdir=tmpdir, target=target, 
                 source_extension=source_extension, compiler_verbose=verbose, 
                 debug=debug, **kwds)

            def init_once--- This code section failed: ---

 L. 731         0  SETUP_FINALLY        16  'to 16'

 L. 732         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _init_once_cache
                6  LOAD_FAST                'tag'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'x'
               12  POP_BLOCK        
               14  JUMP_FORWARD         56  'to 56'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 733        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    54  'to 54'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 734        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _init_once_cache
               34  LOAD_METHOD              setdefault
               36  LOAD_FAST                'tag'
               38  LOAD_CONST               False
               40  LOAD_GLOBAL              allocate_lock
               42  CALL_FUNCTION_0       0  ''
               44  BUILD_TUPLE_2         2 
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'x'
               50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            22  '22'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            14  '14'

 L. 736        56  LOAD_FAST                'x'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 737        64  LOAD_FAST                'x'
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  RETURN_VALUE     
             72_0  COME_FROM            62  '62'

 L. 739        72  LOAD_FAST                'x'
               74  LOAD_CONST               1
               76  BINARY_SUBSCR    
               78  SETUP_WITH          144  'to 144'
               80  POP_TOP          

 L. 741        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _init_once_cache
               86  LOAD_FAST                'tag'
               88  BINARY_SUBSCR    
               90  STORE_FAST               'x'

 L. 742        92  LOAD_FAST                'x'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  POP_JUMP_IF_FALSE   120  'to 120'

 L. 743       100  LOAD_FAST                'x'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  POP_BLOCK        
              108  ROT_TWO          
              110  BEGIN_FINALLY    
              112  WITH_CLEANUP_START
              114  WITH_CLEANUP_FINISH
              116  POP_FINALLY           0  ''
              118  RETURN_VALUE     
            120_0  COME_FROM            98  '98'

 L. 745       120  LOAD_FAST                'func'
              122  CALL_FUNCTION_0       0  ''
              124  STORE_FAST               'result'

 L. 746       126  LOAD_CONST               True
              128  LOAD_FAST                'result'
              130  BUILD_TUPLE_2         2 
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                _init_once_cache
              136  LOAD_FAST                'tag'
              138  STORE_SUBSCR     
              140  POP_BLOCK        
              142  BEGIN_FINALLY    
            144_0  COME_FROM_WITH       78  '78'
              144  WITH_CLEANUP_START
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      

 L. 747       150  LOAD_FAST                'result'
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 108

            def embedding_init_code(self, pysource):
                if self._embedding:
                    raise ValueError('embedding_init_code() can only be called once')
                import re
                match = re.match('\\s*\\n', pysource)
                if match:
                    pysource = pysource[match.end():]
                lines = pysource.splitlines() or ['']
                prefix = re.match('\\s*', lines[0]).group()
                for i in range(1, len(lines)):
                    line = lines[i]
                    if line.rstrip():
                        while True:
                            prefix = line.startswith(prefix) or prefix[:-1]

                    i = len(prefix)
                    lines = [line[i:] + '\n' for line in lines]
                    pysource = ''.join(lines)
                    compile(pysource, 'cffi_init', 'exec')
                    self._embedding = pysource

            def def_extern(self, *args, **kwds):
                raise ValueError('ffi.def_extern() is only available on API-mode FFI objects')

            def list_types(self):
                """Returns the user type names known to this FFI instance.
        This returns a tuple containing three lists of names:
        (typedef_names, names_of_structs, names_of_unions)
        """
                typedefs = []
                structs = []
                unions = []
                for key in self._parser._declarations:
                    if key.startswith('typedef '):
                        typedefs.append(key[8:])
                    elif key.startswith('struct '):
                        structs.append(key[7:])
                    else:
                        if key.startswith('union '):
                            unions.append(key[6:])
                        typedefs.sort()
                        structs.sort()
                        unions.sort()
                        return (typedefs, structs, unions)


        def _load_backend_lib(backend, name, flags):
            import os
            if name is None:
                if sys.platform != 'win32':
                    return backend.load_library(None, flags)
                name = 'c'
            first_error = None
            if '.' in name or '/' in name or os.sep in name:
                try:
                    return backend.load_library(name, flags)
                            except OSError as e:
                    try:
                        first_error = e
                    finally:
                        e = None
                        del e

            import ctypes.util
            path = ctypes.util.find_library(name)
            if path is None:
                if name == 'c':
                    if sys.platform == 'win32':
                        if sys.version_info >= (3, ):
                            raise OSError('dlopen(None) cannot work on Windows for Python 3 (see http://bugs.python.org/issue23606)')
                msg = 'ctypes.util.find_library() did not manage to locate a library called %r' % (
                 name,)
                if first_error is not None:
                    msg = '%s.  Additionally, %s' % (first_error, msg)
                raise OSError(msg)
            return backend.load_library(path, flags)


        def _make_ffi_library(ffi, libname, flags):
            backend = ffi._backend
            backendlib = _load_backend_lib(backend, libname, flags)

            def accessor_function(name):
                key = 'function ' + name
                tp, _ = ffi._parser._declarations[key]
                BType = ffi._get_cached_btype(tp)
                value = backendlib.load_function(BType, name)
                library.__dict__[name] = value

            def accessor_variable(name):
                key = 'variable ' + name
                tp, _ = ffi._parser._declarations[key]
                BType = ffi._get_cached_btype(tp)
                read_variable = backendlib.read_variable
                write_variable = backendlib.write_variable
                setattr(FFILibrary, name, property(lambda self: read_variable(BType, name), lambda self, value: write_variable(BType, name, value)))

            def addressof_var--- This code section failed: ---

 L. 848         0  SETUP_FINALLY        12  'to 12'

 L. 849         2  LOAD_DEREF               'addr_variables'
                4  LOAD_FAST                'name'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 850        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE   140  'to 140'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 851        26  LOAD_DEREF               'ffi'
               28  LOAD_ATTR                _lock
               30  SETUP_WITH          122  'to 122'
               32  POP_TOP          

 L. 852        34  LOAD_FAST                'name'
               36  LOAD_DEREF               'addr_variables'
               38  COMPARE_OP               not-in
               40  POP_JUMP_IF_FALSE   118  'to 118'

 L. 853        42  LOAD_STR                 'variable '
               44  LOAD_FAST                'name'
               46  BINARY_ADD       
               48  STORE_FAST               'key'

 L. 854        50  LOAD_DEREF               'ffi'
               52  LOAD_ATTR                _parser
               54  LOAD_ATTR                _declarations
               56  LOAD_FAST                'key'
               58  BINARY_SUBSCR    
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'tp'
               64  STORE_FAST               '_'

 L. 855        66  LOAD_DEREF               'ffi'
               68  LOAD_METHOD              _get_cached_btype
               70  LOAD_FAST                'tp'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'BType'

 L. 856        76  LOAD_FAST                'BType'
               78  LOAD_ATTR                kind
               80  LOAD_STR                 'array'
               82  COMPARE_OP               !=
               84  POP_JUMP_IF_FALSE    98  'to 98'

 L. 857        86  LOAD_GLOBAL              model
               88  LOAD_METHOD              pointer_cache
               90  LOAD_DEREF               'ffi'
               92  LOAD_FAST                'BType'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'BType'
             98_0  COME_FROM            84  '84'

 L. 858        98  LOAD_DEREF               'backendlib'
              100  LOAD_METHOD              load_function
              102  LOAD_FAST                'BType'
              104  LOAD_FAST                'name'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'p'

 L. 859       110  LOAD_FAST                'p'
              112  LOAD_DEREF               'addr_variables'
              114  LOAD_FAST                'name'
              116  STORE_SUBSCR     
            118_0  COME_FROM            40  '40'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_WITH       30  '30'
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  END_FINALLY      

 L. 860       128  LOAD_DEREF               'addr_variables'
              130  LOAD_FAST                'name'
              132  BINARY_SUBSCR    
              134  ROT_FOUR         
              136  POP_EXCEPT       
              138  RETURN_VALUE     
            140_0  COME_FROM            18  '18'
              140  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22

            def accessor_constant(name):
                raise NotImplementedError("non-integer constant '%s' cannot be accessed from a dlopen() library" % (
                 name,))

            def accessor_int_constant(name):
                library.__dict__[name] = ffi._parser._int_constants[name]

            accessors = {}
            accessors_version = [
             False]
            addr_variables = {}

            def update_accessors():
                if accessors_version[0] is ffi._cdef_version:
                    return
                for key, (tp, _) in ffi._parser._declarations.items():
                    if not isinstance(tp, model.EnumType):
                        tag, name = key.split(' ', 1)
                        if tag == 'function':
                            accessors[name] = accessor_function
                        elif tag == 'variable':
                            accessors[name] = accessor_variable
                        elif tag == 'constant':
                            accessors[name] = accessor_constant
                    else:
                        for i, enumname in enumerate(tp.enumerators):

                            def accessor_enum(name, tp=tp, i=i):
                                tp.check_not_partial()
                                library.__dict__[name] = tp.enumvalues[i]

                            accessors[enumname] = accessor_enum

                for name in ffi._parser._int_constants:
                    accessors.setdefault(name, accessor_int_constant)
                else:
                    accessors_version[0] = ffi._cdef_version

            def make_accessor--- This code section failed: ---

 L. 897         0  LOAD_DEREF               'ffi'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           88  'to 88'
                6  POP_TOP          

 L. 898         8  LOAD_FAST                'name'
               10  LOAD_DEREF               'library'
               12  LOAD_ATTR                __dict__
               14  COMPARE_OP               in
               16  POP_JUMP_IF_TRUE     28  'to 28'
               18  LOAD_FAST                'name'
               20  LOAD_DEREF               'FFILibrary'
               22  LOAD_ATTR                __dict__
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    42  'to 42'
             28_0  COME_FROM            16  '16'

 L. 899        28  POP_BLOCK        
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'

 L. 900        42  LOAD_FAST                'name'
               44  LOAD_DEREF               'accessors'
               46  COMPARE_OP               not-in
               48  POP_JUMP_IF_FALSE    72  'to 72'

 L. 901        50  LOAD_DEREF               'update_accessors'
               52  CALL_FUNCTION_0       0  ''
               54  POP_TOP          

 L. 902        56  LOAD_FAST                'name'
               58  LOAD_DEREF               'accessors'
               60  COMPARE_OP               not-in
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 903        64  LOAD_GLOBAL              AttributeError
               66  LOAD_FAST                'name'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM            48  '48'

 L. 904        72  LOAD_DEREF               'accessors'
               74  LOAD_FAST                'name'
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'name'
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_WITH        4  '4'
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30

            class FFILibrary(object):

                def __getattr__(self, name):
                    make_accessor(name)
                    return getattr(self, name)

                def __setattr__(self, name, value):
                    try:
                        property = getattr(self.__class__, name)
                    except AttributeError:
                        make_accessor(name)
                        setattr(self, name, value)
                    else:
                        property.__set__(self, value)

                def __dir__--- This code section failed: ---

 L. 919         0  LOAD_DEREF               'ffi'
                2  LOAD_ATTR                _lock
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 920         8  LOAD_DEREF               'update_accessors'
               10  CALL_FUNCTION_0       0  ''
               12  POP_TOP          

 L. 921        14  LOAD_DEREF               'accessors'
               16  LOAD_METHOD              keys
               18  CALL_METHOD_0         0  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22

                def __addressof__(self, name):
                    if name in library.__dict__:
                        return library.__dict__[name]
                    if name in FFILibrary.__dict__:
                        return addressof_var(name)
                    make_accessor(name)
                    if name in library.__dict__:
                        return library.__dict__[name]
                    if name in FFILibrary.__dict__:
                        return addressof_var(name)
                    raise AttributeError("cffi library has no function or global variable named '%s'" % (
                     name,))

                def __cffi_close__(self):
                    backendlib.close_lib()
                    self.__dict__.clear()

            if libname is not None:
                try:
                    if not isinstance(libname, str):
                        libname = libname.encode('utf-8')
                    FFILibrary.__name__ = 'FFILibrary_%s' % libname
                except UnicodeError:
                    pass

            library = FFILibrary()
            return (library, library.__dict__)


        def _builtin_function_type--- This code section failed: ---

 L. 951         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L. 952         8  SETUP_FINALLY        46  'to 46'

 L. 953        10  LOAD_FAST                'sys'
               12  LOAD_ATTR                modules
               14  LOAD_FAST                'func'
               16  LOAD_ATTR                __module__
               18  BINARY_SUBSCR    
               20  STORE_FAST               'module'

 L. 954        22  LOAD_FAST                'module'
               24  LOAD_ATTR                _cffi_original_ffi
               26  STORE_FAST               'ffi'

 L. 955        28  LOAD_FAST                'module'
               30  LOAD_ATTR                _cffi_types_of_builtin_funcs
               32  STORE_FAST               'types_of_builtin_funcs'

 L. 956        34  LOAD_FAST                'types_of_builtin_funcs'
               36  LOAD_FAST                'func'
               38  BINARY_SUBSCR    
               40  STORE_FAST               'tp'
               42  POP_BLOCK        
               44  JUMP_FORWARD         74  'to 74'
             46_0  COME_FROM_FINALLY     8  '8'

 L. 957        46  DUP_TOP          
               48  LOAD_GLOBAL              KeyError
               50  LOAD_GLOBAL              AttributeError
               52  LOAD_GLOBAL              TypeError
               54  BUILD_TUPLE_3         3 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 958        66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  RETURN_VALUE     
             72_0  COME_FROM            58  '58'
               72  END_FINALLY      
             74_0  COME_FROM            44  '44'

 L. 960        74  LOAD_FAST                'ffi'
               76  LOAD_ATTR                _lock
               78  SETUP_WITH          104  'to 104'
               80  POP_TOP          

 L. 961        82  LOAD_FAST                'ffi'
               84  LOAD_METHOD              _get_cached_btype
               86  LOAD_FAST                'tp'
               88  CALL_METHOD_1         1  ''
               90  POP_BLOCK        
               92  ROT_TWO          
               94  BEGIN_FINALLY    
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  POP_FINALLY           0  ''
              102  RETURN_VALUE     
            104_0  COME_FROM_WITH       78  '78'
              104  WITH_CLEANUP_START
              106  WITH_CLEANUP_FINISH
              108  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 92