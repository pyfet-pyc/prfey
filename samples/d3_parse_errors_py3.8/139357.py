# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\ctypeslib.py
"""
============================
``ctypes`` Utility Functions
============================

See Also
---------
load_library : Load a C library.
ndpointer : Array restype/argtype with verification.
as_ctypes : Create a ctypes array from an ndarray.
as_array : Create an ndarray from a ctypes array.

References
----------
.. [1] "SciPy Cookbook: ctypes", https://scipy-cookbook.readthedocs.io/items/Ctypes.html

Examples
--------
Load the C library:

>>> _lib = np.ctypeslib.load_library('libmystuff', '.')     #doctest: +SKIP

Our result type, an ndarray that must be of type double, be 1-dimensional
and is C-contiguous in memory:

>>> array_1d_double = np.ctypeslib.ndpointer(
...                          dtype=np.double,
...                          ndim=1, flags='CONTIGUOUS')    #doctest: +SKIP

Our C-function typically takes an array and updates its values
in-place.  For example::

    void foo_func(double* x, int length)
    {
        int i;
        for (i = 0; i < length; i++) {
            x[i] = i*i;
        }
    }

We wrap it using:

>>> _lib.foo_func.restype = None                      #doctest: +SKIP
>>> _lib.foo_func.argtypes = [array_1d_double, c_int] #doctest: +SKIP

Then, we're ready to call ``foo_func``:

>>> out = np.empty(15, dtype=np.double)
>>> _lib.foo_func(out, len(out))                #doctest: +SKIP

"""
__all__ = [
 'load_library', 'ndpointer', 'c_intp', 'as_ctypes', 'as_array']
import os
from numpy import integer, ndarray, dtype as _dtype, array, frombuffer
from numpy.core.multiarray import _flagdict, flagsobj
try:
    import ctypes
except ImportError:
    ctypes = None
else:
    if ctypes is None:

        def _dummy(*args, **kwds):
            """
        Dummy object that raises an ImportError if ctypes is not available.

        Raises
        ------
        ImportError
            If ctypes is not available.

        """
            raise ImportError('ctypes is not available.')


        load_library = _dummy
        as_ctypes = _dummy
        as_array = _dummy
        from numpy import intp as c_intp
        _ndptr_base = object
    else:
        import numpy.core._internal as nic
        c_intp = nic._getintp_ctype()
        del nic
        _ndptr_base = ctypes.c_void_p

        def load_library--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                __version__
                4  LOAD_STR                 '1.0.1'
                6  COMPARE_OP               <
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 118        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              warnings
               16  STORE_FAST               'warnings'

 L. 119        18  LOAD_FAST                'warnings'
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'All features of ctypes interface may not work with ctypes < 1.0.1'

 L. 120        24  LOAD_CONST               2

 L. 119        26  LOAD_CONST               ('stacklevel',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  POP_TOP          
             32_0  COME_FROM             8  '8'

 L. 122        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              splitext
               38  LOAD_FAST                'libname'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               1
               44  BINARY_SUBSCR    
               46  STORE_FAST               'ext'

 L. 123        48  LOAD_FAST                'ext'
               50  POP_JUMP_IF_TRUE    116  'to 116'

 L. 127        52  LOAD_CONST               0
               54  LOAD_CONST               ('get_shared_lib_extension',)
               56  IMPORT_NAME_ATTR         numpy.distutils.misc_util
               58  IMPORT_FROM              get_shared_lib_extension
               60  STORE_FAST               'get_shared_lib_extension'
               62  POP_TOP          

 L. 128        64  LOAD_FAST                'get_shared_lib_extension'
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'so_ext'

 L. 129        70  LOAD_FAST                'libname'
               72  LOAD_FAST                'so_ext'
               74  BINARY_ADD       
               76  BUILD_LIST_1          1 
               78  STORE_FAST               'libname_ext'

 L. 132        80  LOAD_FAST                'get_shared_lib_extension'
               82  LOAD_CONST               True
               84  LOAD_CONST               ('is_python_ext',)
               86  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               88  STORE_FAST               'so_ext2'

 L. 133        90  LOAD_FAST                'so_ext2'
               92  LOAD_FAST                'so_ext'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_TRUE    122  'to 122'

 L. 134        98  LOAD_FAST                'libname_ext'
              100  LOAD_METHOD              insert
              102  LOAD_CONST               0
              104  LOAD_FAST                'libname'
              106  LOAD_FAST                'so_ext2'
              108  BINARY_ADD       
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          
              114  JUMP_FORWARD        122  'to 122'
            116_0  COME_FROM            50  '50'

 L. 136       116  LOAD_FAST                'libname'
              118  BUILD_LIST_1          1 
              120  STORE_FAST               'libname_ext'
            122_0  COME_FROM           114  '114'
            122_1  COME_FROM            96  '96'

 L. 138       122  LOAD_GLOBAL              os
              124  LOAD_ATTR                path
              126  LOAD_METHOD              abspath
              128  LOAD_FAST                'loader_path'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'loader_path'

 L. 139       134  LOAD_GLOBAL              os
              136  LOAD_ATTR                path
              138  LOAD_METHOD              isdir
              140  LOAD_FAST                'loader_path'
              142  CALL_METHOD_1         1  ''
              144  POP_JUMP_IF_TRUE    160  'to 160'

 L. 140       146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              dirname
              152  LOAD_FAST                'loader_path'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'libdir'
              158  JUMP_FORWARD        164  'to 164'
            160_0  COME_FROM           144  '144'

 L. 142       160  LOAD_FAST                'loader_path'
              162  STORE_FAST               'libdir'
            164_0  COME_FROM           158  '158'

 L. 144       164  LOAD_FAST                'libname_ext'
              166  GET_ITER         
            168_0  COME_FROM           238  '238'
            168_1  COME_FROM           234  '234'
            168_2  COME_FROM           196  '196'
              168  FOR_ITER            240  'to 240'
              170  STORE_FAST               'ln'

 L. 145       172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              join
              178  LOAD_FAST                'libdir'
              180  LOAD_FAST                'ln'
              182  CALL_METHOD_2         2  ''
              184  STORE_FAST               'libpath'

 L. 146       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              exists
              192  LOAD_FAST                'libpath'
              194  CALL_METHOD_1         1  ''
              196  POP_JUMP_IF_FALSE_BACK   168  'to 168'

 L. 147       198  SETUP_FINALLY       216  'to 216'

 L. 148       200  LOAD_GLOBAL              ctypes
              202  LOAD_ATTR                cdll
              204  LOAD_FAST                'libpath'
              206  BINARY_SUBSCR    
              208  POP_BLOCK        
              210  ROT_TWO          
              212  POP_TOP          
              214  RETURN_VALUE     
            216_0  COME_FROM_FINALLY   198  '198'

 L. 149       216  DUP_TOP          
              218  LOAD_GLOBAL              OSError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   236  'to 236'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 151       230  RAISE_VARARGS_0       0  'reraise'
              232  POP_EXCEPT       
              234  JUMP_BACK           168  'to 168'
            236_0  COME_FROM           222  '222'
              236  END_FINALLY      
              238  JUMP_BACK           168  'to 168'
            240_0  COME_FROM           168  '168'

 L. 153       240  LOAD_GLOBAL              OSError
              242  LOAD_STR                 'no file with expected extension'
              244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 210


    def _num_fromflags(flaglist):
        num = 0
        for val in flaglist:
            num += _flagdict[val]
        else:
            return num


    _flagnames = ['C_CONTIGUOUS', 'F_CONTIGUOUS', 'ALIGNED', 'WRITEABLE',
     'OWNDATA', 'UPDATEIFCOPY', 'WRITEBACKIFCOPY']

    def _flags_fromnum(num):
        res = []
        for key in _flagnames:
            value = _flagdict[key]
            if num & value:
                res.appendkey
        else:
            return res


    class _ndptr(_ndptr_base):

        @classmethod
        def from_param(cls, obj):
            if not isinstance(obj, ndarray):
                raise TypeError('argument must be an ndarray')
            if cls._dtype_ is not None:
                if obj.dtype != cls._dtype_:
                    raise TypeError('array must have data type %s' % cls._dtype_)
            if cls._ndim_ is not None:
                if obj.ndim != cls._ndim_:
                    raise TypeError('array must have %d dimension(s)' % cls._ndim_)
            if cls._shape_ is not None:
                if obj.shape != cls._shape_:
                    raise TypeError('array must have shape %s' % str(cls._shape_))
            if cls._flags_ is not None:
                if obj.flags.num & cls._flags_ != cls._flags_:
                    raise TypeError('array must have flags %s' % _flags_fromnum(cls._flags_))
            return obj.ctypes


    class _concrete_ndptr(_ndptr):
        __doc__ = '\n    Like _ndptr, but with `_shape_` and `_dtype_` specified.\n\n    Notably, this means the pointer has enough information to reconstruct\n    the array, which is not generally true.\n    '

        def _check_retval_(self):
            """
        This method is called when this class is used as the .restype
        attribute for a shared-library function, to automatically wrap the
        pointer into an array.
        """
            return self.contents

        @property
        def contents(self):
            """
        Get an ndarray viewing the data pointed to by this pointer.

        This mirrors the `contents` attribute of a normal ctypes pointer
        """
            full_dtype = _dtype((self._dtype_, self._shape_))
            full_ctype = ctypes.c_char * full_dtype.itemsize
            buffer = ctypes.castselfctypes.POINTERfull_ctype.contents
            return frombuffer(buffer, dtype=full_dtype).squeeze(axis=0)


    _pointer_type_cache = {}

    def ndpointer--- This code section failed: ---

 L. 279         0  LOAD_FAST                'dtype'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 280         8  LOAD_GLOBAL              _dtype
               10  LOAD_FAST                'dtype'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'dtype'
             16_0  COME_FROM             6  '6'

 L. 283        16  LOAD_CONST               None
               18  STORE_FAST               'num'

 L. 284        20  LOAD_FAST                'flags'
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE   182  'to 182'

 L. 285        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'flags'
               32  LOAD_GLOBAL              str
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    50  'to 50'

 L. 286        38  LOAD_FAST                'flags'
               40  LOAD_METHOD              split
               42  LOAD_STR                 ','
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'flags'
               48  JUMP_FORWARD        102  'to 102'
             50_0  COME_FROM            36  '36'

 L. 287        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'flags'
               54  LOAD_GLOBAL              int
               56  LOAD_GLOBAL              integer
               58  BUILD_TUPLE_2         2 
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 288        64  LOAD_FAST                'flags'
               66  STORE_FAST               'num'

 L. 289        68  LOAD_GLOBAL              _flags_fromnum
               70  LOAD_FAST                'num'
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'flags'
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM            62  '62'

 L. 290        78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'flags'
               82  LOAD_GLOBAL              flagsobj
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L. 291        88  LOAD_FAST                'flags'
               90  LOAD_ATTR                num
               92  STORE_FAST               'num'

 L. 292        94  LOAD_GLOBAL              _flags_fromnum
               96  LOAD_FAST                'num'
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'flags'
            102_0  COME_FROM            86  '86'
            102_1  COME_FROM            76  '76'
            102_2  COME_FROM            48  '48'

 L. 293       102  LOAD_FAST                'num'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   182  'to 182'

 L. 294       110  SETUP_FINALLY       130  'to 130'

 L. 295       112  LOAD_LISTCOMP            '<code_object <listcomp>>'
              114  LOAD_STR                 'ndpointer.<locals>.<listcomp>'
              116  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              118  LOAD_FAST                'flags'
              120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'flags'
              126  POP_BLOCK        
              128  JUMP_FORWARD        174  'to 174'
            130_0  COME_FROM_FINALLY   110  '110'

 L. 296       130  DUP_TOP          
              132  LOAD_GLOBAL              Exception
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   172  'to 172'
              138  POP_TOP          
              140  STORE_FAST               'e'
              142  POP_TOP          
              144  SETUP_FINALLY       160  'to 160'

 L. 297       146  LOAD_GLOBAL              TypeError
              148  LOAD_STR                 'invalid flags specification'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_FAST                'e'
              154  RAISE_VARARGS_2       2  'exception instance with __cause__'
              156  POP_BLOCK        
              158  BEGIN_FINALLY    
            160_0  COME_FROM_FINALLY   144  '144'
              160  LOAD_CONST               None
              162  STORE_FAST               'e'
              164  DELETE_FAST              'e'
              166  END_FINALLY      
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           136  '136'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           128  '128'

 L. 298       174  LOAD_GLOBAL              _num_fromflags
              176  LOAD_FAST                'flags'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'num'
            182_0  COME_FROM           108  '108'
            182_1  COME_FROM            26  '26'

 L. 301       182  LOAD_FAST                'shape'
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   230  'to 230'

 L. 302       190  SETUP_FINALLY       204  'to 204'

 L. 303       192  LOAD_GLOBAL              tuple
              194  LOAD_FAST                'shape'
              196  CALL_FUNCTION_1       1  ''
              198  STORE_FAST               'shape'
              200  POP_BLOCK        
              202  JUMP_FORWARD        230  'to 230'
            204_0  COME_FROM_FINALLY   190  '190'

 L. 304       204  DUP_TOP          
              206  LOAD_GLOBAL              TypeError
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   228  'to 228'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 306       218  LOAD_FAST                'shape'
              220  BUILD_TUPLE_1         1 
              222  STORE_FAST               'shape'
              224  POP_EXCEPT       
              226  JUMP_FORWARD        230  'to 230'
            228_0  COME_FROM           210  '210'
              228  END_FINALLY      
            230_0  COME_FROM           226  '226'
            230_1  COME_FROM           202  '202'
            230_2  COME_FROM           188  '188'

 L. 308       230  LOAD_FAST                'dtype'
              232  LOAD_FAST                'ndim'
              234  LOAD_FAST                'shape'
              236  LOAD_FAST                'num'
              238  BUILD_TUPLE_4         4 
              240  STORE_FAST               'cache_key'

 L. 310       242  SETUP_FINALLY       254  'to 254'

 L. 311       244  LOAD_GLOBAL              _pointer_type_cache
              246  LOAD_FAST                'cache_key'
              248  BINARY_SUBSCR    
              250  POP_BLOCK        
              252  RETURN_VALUE     
            254_0  COME_FROM_FINALLY   242  '242'

 L. 312       254  DUP_TOP          
              256  LOAD_GLOBAL              KeyError
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   274  'to 274'
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L. 313       270  POP_EXCEPT       
              272  JUMP_FORWARD        276  'to 276'
            274_0  COME_FROM           260  '260'
              274  END_FINALLY      
            276_0  COME_FROM           272  '272'

 L. 316       276  LOAD_FAST                'dtype'
              278  LOAD_CONST               None
              280  COMPARE_OP               is
          282_284  POP_JUMP_IF_FALSE   292  'to 292'

 L. 317       286  LOAD_STR                 'any'
              288  STORE_FAST               'name'
              290  JUMP_FORWARD        324  'to 324'
            292_0  COME_FROM           282  '282'

 L. 318       292  LOAD_FAST                'dtype'
              294  LOAD_ATTR                names
              296  LOAD_CONST               None
              298  COMPARE_OP               is-not
          300_302  POP_JUMP_IF_FALSE   318  'to 318'

 L. 319       304  LOAD_GLOBAL              str
              306  LOAD_GLOBAL              id
              308  LOAD_FAST                'dtype'
              310  CALL_FUNCTION_1       1  ''
              312  CALL_FUNCTION_1       1  ''
              314  STORE_FAST               'name'
              316  JUMP_FORWARD        324  'to 324'
            318_0  COME_FROM           300  '300'

 L. 321       318  LOAD_FAST                'dtype'
              320  LOAD_ATTR                str
              322  STORE_FAST               'name'
            324_0  COME_FROM           316  '316'
            324_1  COME_FROM           290  '290'

 L. 322       324  LOAD_FAST                'ndim'
              326  LOAD_CONST               None
              328  COMPARE_OP               is-not
          330_332  POP_JUMP_IF_FALSE   346  'to 346'

 L. 323       334  LOAD_FAST                'name'
              336  LOAD_STR                 '_%dd'
              338  LOAD_FAST                'ndim'
              340  BINARY_MODULO    
              342  INPLACE_ADD      
              344  STORE_FAST               'name'
            346_0  COME_FROM           330  '330'

 L. 324       346  LOAD_FAST                'shape'
              348  LOAD_CONST               None
              350  COMPARE_OP               is-not
          352_354  POP_JUMP_IF_FALSE   384  'to 384'

 L. 325       356  LOAD_FAST                'name'
              358  LOAD_STR                 '_'
              360  LOAD_STR                 'x'
              362  LOAD_METHOD              join
              364  LOAD_GENEXPR             '<code_object <genexpr>>'
              366  LOAD_STR                 'ndpointer.<locals>.<genexpr>'
              368  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              370  LOAD_FAST                'shape'
              372  GET_ITER         
              374  CALL_FUNCTION_1       1  ''
              376  CALL_METHOD_1         1  ''
              378  BINARY_ADD       
              380  INPLACE_ADD      
              382  STORE_FAST               'name'
            384_0  COME_FROM           352  '352'

 L. 326       384  LOAD_FAST                'flags'
              386  LOAD_CONST               None
              388  COMPARE_OP               is-not
          390_392  POP_JUMP_IF_FALSE   412  'to 412'

 L. 327       394  LOAD_FAST                'name'
              396  LOAD_STR                 '_'
              398  LOAD_STR                 '_'
              400  LOAD_METHOD              join
              402  LOAD_FAST                'flags'
              404  CALL_METHOD_1         1  ''
              406  BINARY_ADD       
              408  INPLACE_ADD      
              410  STORE_FAST               'name'
            412_0  COME_FROM           390  '390'

 L. 329       412  LOAD_FAST                'dtype'
              414  LOAD_CONST               None
              416  COMPARE_OP               is-not
          418_420  POP_JUMP_IF_FALSE   438  'to 438'
              422  LOAD_FAST                'shape'
              424  LOAD_CONST               None
              426  COMPARE_OP               is-not
          428_430  POP_JUMP_IF_FALSE   438  'to 438'

 L. 330       432  LOAD_GLOBAL              _concrete_ndptr
              434  STORE_FAST               'base'
              436  JUMP_FORWARD        442  'to 442'
            438_0  COME_FROM           428  '428'
            438_1  COME_FROM           418  '418'

 L. 332       438  LOAD_GLOBAL              _ndptr
              440  STORE_FAST               'base'
            442_0  COME_FROM           436  '436'

 L. 334       442  LOAD_GLOBAL              type
              444  LOAD_STR                 'ndpointer_%s'
              446  LOAD_FAST                'name'
              448  BINARY_MODULO    
              450  LOAD_FAST                'base'
              452  BUILD_TUPLE_1         1 

 L. 335       454  LOAD_FAST                'dtype'

 L. 336       456  LOAD_FAST                'shape'

 L. 337       458  LOAD_FAST                'ndim'

 L. 338       460  LOAD_FAST                'num'

 L. 335       462  LOAD_CONST               ('_dtype_', '_shape_', '_ndim_', '_flags_')
              464  BUILD_CONST_KEY_MAP_4     4 

 L. 334       466  CALL_FUNCTION_3       3  ''
              468  STORE_FAST               'klass'

 L. 339       470  LOAD_FAST                'klass'
              472  LOAD_GLOBAL              _pointer_type_cache
              474  LOAD_FAST                'cache_key'
              476  STORE_SUBSCR     

 L. 340       478  LOAD_FAST                'klass'
              480  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 274_0


    if ctypes is not None:

        def _ctype_ndarray(element_type, shape):
            """ Create an ndarray of the given element type and shape """
            for dim in shape[::-1]:
                element_type = dim * element_type
                element_type.__module__ = None
            else:
                return element_type


        def _get_scalar_type_map():
            """
        Return a dictionary mapping native endian scalar dtype to ctypes types
        """
            ct = ctypes
            simple_types = [
             ct.c_byte, ct.c_short, ct.c_int, ct.c_long, ct.c_longlong,
             ct.c_ubyte, ct.c_ushort, ct.c_uint, ct.c_ulong, ct.c_ulonglong,
             ct.c_float, ct.c_double,
             ct.c_bool]
            return {ctype:_dtype(ctype) for ctype in simple_types}


        _scalar_type_map = _get_scalar_type_map()

        def _ctype_from_dtype_scalar(dtype):
            dtype_with_endian = dtype.newbyteorder'S'.newbyteorder'S'
            dtype_native = dtype.newbyteorder'='
            try:
                ctype = _scalar_type_map[dtype_native]
            except KeyError as e:
                try:
                    raise NotImplementedError('Converting {!r} to a ctypes type'.formatdtype) from None
                finally:
                    e = None
                    del e

            else:
                if dtype_with_endian.byteorder == '>':
                    ctype = ctype.__ctype_be__
                elif dtype_with_endian.byteorder == '<':
                    ctype = ctype.__ctype_le__
                return ctype


        def _ctype_from_dtype_subarray(dtype):
            element_dtype, shape = dtype.subdtype
            ctype = _ctype_from_dtype(element_dtype)
            return _ctype_ndarray(ctype, shape)


        def _ctype_from_dtype_structured(dtype):
            field_data = []
            for name in dtype.names:
                field_dtype, offset = dtype.fields[name][:2]
                field_data.append(offset, name, _ctype_from_dtype(field_dtype))
            else:
                field_data = sorted(field_data, key=(lambda f: f[0]))
                if len(field_data) > 1:
                    if all((offset == 0 for offset, name, ctype in field_data)):
                        size = 0
                        _fields_ = []
                        for offset, name, ctype in field_data:
                            _fields_.append(name, ctype)
                            size = max(size, ctypes.sizeofctype)
                        else:
                            if dtype.itemsize != size:
                                _fields_.append('', ctypes.c_char * dtype.itemsize)
                            return type('union', (ctypes.Union,), dict(_fields_=_fields_,
                              _pack_=1,
                              __module__=None))

                last_offset = 0
                _fields_ = []
                for offset, name, ctype in field_data:
                    padding = offset - last_offset
                    if padding < 0:
                        raise NotImplementedError('Overlapping fields')
                    else:
                        if padding > 0:
                            _fields_.append('', ctypes.c_char * padding)
                        _fields_.append(name, ctype)
                        last_offset = offset + ctypes.sizeofctype
                else:
                    padding = dtype.itemsize - last_offset
                    if padding > 0:
                        _fields_.append('', ctypes.c_char * padding)
                    return type('struct', (ctypes.Structure,), dict(_fields_=_fields_,
                      _pack_=1,
                      __module__=None))


        def _ctype_from_dtype(dtype):
            if dtype.fields is not None:
                return _ctype_from_dtype_structured(dtype)
            if dtype.subdtype is not None:
                return _ctype_from_dtype_subarray(dtype)
            return _ctype_from_dtype_scalar(dtype)


        def as_ctypes_type(dtype):
            r"""
        Convert a dtype into a ctypes type.

        Parameters
        ----------
        dtype : dtype
            The dtype to convert

        Returns
        -------
        ctype
            A ctype scalar, union, array, or struct

        Raises
        ------
        NotImplementedError
            If the conversion is not possible

        Notes
        -----
        This function does not losslessly round-trip in either direction.

        ``np.dtype(as_ctypes_type(dt))`` will:

         - insert padding fields
         - reorder fields to be sorted by offset
         - discard field titles

        ``as_ctypes_type(np.dtype(ctype))`` will:

         - discard the class names of `ctypes.Structure`\ s and
           `ctypes.Union`\ s
         - convert single-element `ctypes.Union`\ s into single-element
           `ctypes.Structure`\ s
         - insert padding fields

        """
            return _ctype_from_dtype(_dtype(dtype))


        def as_array(obj, shape=None):
            """
        Create a numpy array from a ctypes array or POINTER.

        The numpy array shares the memory with the ctypes object.

        The shape parameter must be given if converting from a ctypes POINTER.
        The shape parameter is ignored if converting from a ctypes array
        """
            if isinstance(obj, ctypes._Pointer):
                if shape is None:
                    raise TypeError('as_array() requires a shape argument when called on a pointer')
                p_arr_type = ctypes.POINTER_ctype_ndarray(obj._type_, shape)
                obj = ctypes.castobjp_arr_type.contents
            return array(obj, copy=False)


        def as_ctypes(obj):
            """Create and return a ctypes object from a numpy array.  Actually
        anything that exposes the __array_interface__ is accepted."""
            ai = obj.__array_interface__
            if ai['strides']:
                raise TypeError('strided arrays not supported')
            if ai['version'] != 3:
                raise TypeError('only __array_interface__ version 3 supported')
            addr, readonly = ai['data']
            if readonly:
                raise TypeError('readonly arrays unsupported')
            ctype_scalar = as_ctypes_type(ai['typestr'])
            result_type = _ctype_ndarray(ctype_scalar, ai['shape'])
            result = result_type.from_addressaddr
            result.__keep = obj
            return result