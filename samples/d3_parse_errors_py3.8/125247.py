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
 'load_library', 'ndpointer', 'ctypes_load_library',
 'c_intp', 'as_ctypes', 'as_array']
import os
from numpy import integer, ndarray, dtype as _dtype, deprecate, array, frombuffer
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


        ctypes_load_library = _dummy
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

 L. 119         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                __version__
                4  LOAD_STR                 '1.0.1'
                6  COMPARE_OP               <
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 120        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              warnings
               16  STORE_FAST               'warnings'

 L. 121        18  LOAD_FAST                'warnings'
               20  LOAD_ATTR                warn
               22  LOAD_STR                 'All features of ctypes interface may not work with ctypes < 1.0.1'

 L. 122        24  LOAD_CONST               2

 L. 121        26  LOAD_CONST               ('stacklevel',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  POP_TOP          
             32_0  COME_FROM             8  '8'

 L. 124        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              splitext
               38  LOAD_FAST                'libname'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               1
               44  BINARY_SUBSCR    
               46  STORE_FAST               'ext'

 L. 125        48  LOAD_FAST                'ext'
               50  POP_JUMP_IF_TRUE    116  'to 116'

 L. 129        52  LOAD_CONST               0
               54  LOAD_CONST               ('get_shared_lib_extension',)
               56  IMPORT_NAME_ATTR         numpy.distutils.misc_util
               58  IMPORT_FROM              get_shared_lib_extension
               60  STORE_FAST               'get_shared_lib_extension'
               62  POP_TOP          

 L. 130        64  LOAD_FAST                'get_shared_lib_extension'
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'so_ext'

 L. 131        70  LOAD_FAST                'libname'
               72  LOAD_FAST                'so_ext'
               74  BINARY_ADD       
               76  BUILD_LIST_1          1 
               78  STORE_FAST               'libname_ext'

 L. 134        80  LOAD_FAST                'get_shared_lib_extension'
               82  LOAD_CONST               True
               84  LOAD_CONST               ('is_python_ext',)
               86  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               88  STORE_FAST               'so_ext2'

 L. 135        90  LOAD_FAST                'so_ext2'
               92  LOAD_FAST                'so_ext'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_TRUE    122  'to 122'

 L. 136        98  LOAD_FAST                'libname_ext'
              100  LOAD_METHOD              insert
              102  LOAD_CONST               0
              104  LOAD_FAST                'libname'
              106  LOAD_FAST                'so_ext2'
              108  BINARY_ADD       
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          
              114  JUMP_FORWARD        122  'to 122'
            116_0  COME_FROM            50  '50'

 L. 138       116  LOAD_FAST                'libname'
              118  BUILD_LIST_1          1 
              120  STORE_FAST               'libname_ext'
            122_0  COME_FROM           114  '114'
            122_1  COME_FROM            96  '96'

 L. 140       122  LOAD_GLOBAL              os
              124  LOAD_ATTR                path
              126  LOAD_METHOD              abspath
              128  LOAD_FAST                'loader_path'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'loader_path'

 L. 141       134  LOAD_GLOBAL              os
              136  LOAD_ATTR                path
              138  LOAD_METHOD              isdir
              140  LOAD_FAST                'loader_path'
              142  CALL_METHOD_1         1  ''
              144  POP_JUMP_IF_TRUE    160  'to 160'

 L. 142       146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              dirname
              152  LOAD_FAST                'loader_path'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'libdir'
              158  JUMP_FORWARD        164  'to 164'
            160_0  COME_FROM           144  '144'

 L. 144       160  LOAD_FAST                'loader_path'
              162  STORE_FAST               'libdir'
            164_0  COME_FROM           158  '158'

 L. 146       164  LOAD_FAST                'libname_ext'
              166  GET_ITER         
            168_0  COME_FROM           238  '238'
            168_1  COME_FROM           234  '234'
            168_2  COME_FROM           196  '196'
              168  FOR_ITER            240  'to 240'
              170  STORE_FAST               'ln'

 L. 147       172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              join
              178  LOAD_FAST                'libdir'
              180  LOAD_FAST                'ln'
              182  CALL_METHOD_2         2  ''
              184  STORE_FAST               'libpath'

 L. 148       186  LOAD_GLOBAL              os
              188  LOAD_ATTR                path
              190  LOAD_METHOD              exists
              192  LOAD_FAST                'libpath'
              194  CALL_METHOD_1         1  ''
              196  POP_JUMP_IF_FALSE_BACK   168  'to 168'

 L. 149       198  SETUP_FINALLY       216  'to 216'

 L. 150       200  LOAD_GLOBAL              ctypes
              202  LOAD_ATTR                cdll
              204  LOAD_FAST                'libpath'
              206  BINARY_SUBSCR    
              208  POP_BLOCK        
              210  ROT_TWO          
              212  POP_TOP          
              214  RETURN_VALUE     
            216_0  COME_FROM_FINALLY   198  '198'

 L. 151       216  DUP_TOP          
              218  LOAD_GLOBAL              OSError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   236  'to 236'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 153       230  RAISE_VARARGS_0       0  'reraise'
              232  POP_EXCEPT       
              234  JUMP_BACK           168  'to 168'
            236_0  COME_FROM           222  '222'
              236  END_FINALLY      
              238  JUMP_BACK           168  'to 168'
            240_0  COME_FROM           168  '168'

 L. 155       240  LOAD_GLOBAL              OSError
              242  LOAD_STR                 'no file with expected extension'
              244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 210


        ctypes_load_library = deprecate(load_library, 'ctypes_load_library', 'load_library')

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

 L. 283         0  LOAD_FAST                'dtype'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 284         8  LOAD_GLOBAL              _dtype
               10  LOAD_FAST                'dtype'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'dtype'
             16_0  COME_FROM             6  '6'

 L. 287        16  LOAD_CONST               None
               18  STORE_FAST               'num'

 L. 288        20  LOAD_FAST                'flags'
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE   166  'to 166'

 L. 289        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'flags'
               32  LOAD_GLOBAL              str
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    50  'to 50'

 L. 290        38  LOAD_FAST                'flags'
               40  LOAD_METHOD              split
               42  LOAD_STR                 ','
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'flags'
               48  JUMP_FORWARD        102  'to 102'
             50_0  COME_FROM            36  '36'

 L. 291        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'flags'
               54  LOAD_GLOBAL              int
               56  LOAD_GLOBAL              integer
               58  BUILD_TUPLE_2         2 
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 292        64  LOAD_FAST                'flags'
               66  STORE_FAST               'num'

 L. 293        68  LOAD_GLOBAL              _flags_fromnum
               70  LOAD_FAST                'num'
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'flags'
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM            62  '62'

 L. 294        78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'flags'
               82  LOAD_GLOBAL              flagsobj
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L. 295        88  LOAD_FAST                'flags'
               90  LOAD_ATTR                num
               92  STORE_FAST               'num'

 L. 296        94  LOAD_GLOBAL              _flags_fromnum
               96  LOAD_FAST                'num'
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'flags'
            102_0  COME_FROM            86  '86'
            102_1  COME_FROM            76  '76'
            102_2  COME_FROM            48  '48'

 L. 297       102  LOAD_FAST                'num'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   166  'to 166'

 L. 298       110  SETUP_FINALLY       130  'to 130'

 L. 299       112  LOAD_LISTCOMP            '<code_object <listcomp>>'
              114  LOAD_STR                 'ndpointer.<locals>.<listcomp>'
              116  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              118  LOAD_FAST                'flags'
              120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'flags'
              126  POP_BLOCK        
              128  JUMP_FORWARD        158  'to 158'
            130_0  COME_FROM_FINALLY   110  '110'

 L. 300       130  DUP_TOP          
              132  LOAD_GLOBAL              Exception
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   156  'to 156'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 301       144  LOAD_GLOBAL              TypeError
              146  LOAD_STR                 'invalid flags specification'
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
            156_0  COME_FROM           136  '136'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'
            158_1  COME_FROM           128  '128'

 L. 302       158  LOAD_GLOBAL              _num_fromflags
              160  LOAD_FAST                'flags'
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'num'
            166_0  COME_FROM           108  '108'
            166_1  COME_FROM            26  '26'

 L. 305       166  LOAD_FAST                'shape'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   214  'to 214'

 L. 306       174  SETUP_FINALLY       188  'to 188'

 L. 307       176  LOAD_GLOBAL              tuple
              178  LOAD_FAST                'shape'
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'shape'
              184  POP_BLOCK        
              186  JUMP_FORWARD        214  'to 214'
            188_0  COME_FROM_FINALLY   174  '174'

 L. 308       188  DUP_TOP          
              190  LOAD_GLOBAL              TypeError
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   212  'to 212'
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 310       202  LOAD_FAST                'shape'
              204  BUILD_TUPLE_1         1 
              206  STORE_FAST               'shape'
              208  POP_EXCEPT       
              210  JUMP_FORWARD        214  'to 214'
            212_0  COME_FROM           194  '194'
              212  END_FINALLY      
            214_0  COME_FROM           210  '210'
            214_1  COME_FROM           186  '186'
            214_2  COME_FROM           172  '172'

 L. 312       214  LOAD_FAST                'dtype'
              216  LOAD_FAST                'ndim'
              218  LOAD_FAST                'shape'
              220  LOAD_FAST                'num'
              222  BUILD_TUPLE_4         4 
              224  STORE_FAST               'cache_key'

 L. 314       226  SETUP_FINALLY       238  'to 238'

 L. 315       228  LOAD_GLOBAL              _pointer_type_cache
              230  LOAD_FAST                'cache_key'
              232  BINARY_SUBSCR    
              234  POP_BLOCK        
              236  RETURN_VALUE     
            238_0  COME_FROM_FINALLY   226  '226'

 L. 316       238  DUP_TOP          
              240  LOAD_GLOBAL              KeyError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   258  'to 258'
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 317       254  POP_EXCEPT       
              256  JUMP_FORWARD        260  'to 260'
            258_0  COME_FROM           244  '244'
              258  END_FINALLY      
            260_0  COME_FROM           256  '256'

 L. 320       260  LOAD_FAST                'dtype'
              262  LOAD_CONST               None
              264  COMPARE_OP               is
          266_268  POP_JUMP_IF_FALSE   276  'to 276'

 L. 321       270  LOAD_STR                 'any'
              272  STORE_FAST               'name'
              274  JUMP_FORWARD        308  'to 308'
            276_0  COME_FROM           266  '266'

 L. 322       276  LOAD_FAST                'dtype'
              278  LOAD_ATTR                names
              280  LOAD_CONST               None
              282  COMPARE_OP               is-not
          284_286  POP_JUMP_IF_FALSE   302  'to 302'

 L. 323       288  LOAD_GLOBAL              str
              290  LOAD_GLOBAL              id
              292  LOAD_FAST                'dtype'
              294  CALL_FUNCTION_1       1  ''
              296  CALL_FUNCTION_1       1  ''
              298  STORE_FAST               'name'
              300  JUMP_FORWARD        308  'to 308'
            302_0  COME_FROM           284  '284'

 L. 325       302  LOAD_FAST                'dtype'
              304  LOAD_ATTR                str
              306  STORE_FAST               'name'
            308_0  COME_FROM           300  '300'
            308_1  COME_FROM           274  '274'

 L. 326       308  LOAD_FAST                'ndim'
              310  LOAD_CONST               None
              312  COMPARE_OP               is-not
          314_316  POP_JUMP_IF_FALSE   330  'to 330'

 L. 327       318  LOAD_FAST                'name'
              320  LOAD_STR                 '_%dd'
              322  LOAD_FAST                'ndim'
              324  BINARY_MODULO    
              326  INPLACE_ADD      
              328  STORE_FAST               'name'
            330_0  COME_FROM           314  '314'

 L. 328       330  LOAD_FAST                'shape'
              332  LOAD_CONST               None
              334  COMPARE_OP               is-not
          336_338  POP_JUMP_IF_FALSE   368  'to 368'

 L. 329       340  LOAD_FAST                'name'
              342  LOAD_STR                 '_'
              344  LOAD_STR                 'x'
              346  LOAD_METHOD              join
              348  LOAD_GENEXPR             '<code_object <genexpr>>'
              350  LOAD_STR                 'ndpointer.<locals>.<genexpr>'
              352  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              354  LOAD_FAST                'shape'
              356  GET_ITER         
              358  CALL_FUNCTION_1       1  ''
              360  CALL_METHOD_1         1  ''
              362  BINARY_ADD       
              364  INPLACE_ADD      
              366  STORE_FAST               'name'
            368_0  COME_FROM           336  '336'

 L. 330       368  LOAD_FAST                'flags'
              370  LOAD_CONST               None
              372  COMPARE_OP               is-not
          374_376  POP_JUMP_IF_FALSE   396  'to 396'

 L. 331       378  LOAD_FAST                'name'
              380  LOAD_STR                 '_'
              382  LOAD_STR                 '_'
              384  LOAD_METHOD              join
              386  LOAD_FAST                'flags'
              388  CALL_METHOD_1         1  ''
              390  BINARY_ADD       
              392  INPLACE_ADD      
              394  STORE_FAST               'name'
            396_0  COME_FROM           374  '374'

 L. 333       396  LOAD_FAST                'dtype'
              398  LOAD_CONST               None
              400  COMPARE_OP               is-not
          402_404  POP_JUMP_IF_FALSE   422  'to 422'
              406  LOAD_FAST                'shape'
              408  LOAD_CONST               None
              410  COMPARE_OP               is-not
          412_414  POP_JUMP_IF_FALSE   422  'to 422'

 L. 334       416  LOAD_GLOBAL              _concrete_ndptr
              418  STORE_FAST               'base'
              420  JUMP_FORWARD        426  'to 426'
            422_0  COME_FROM           412  '412'
            422_1  COME_FROM           402  '402'

 L. 336       422  LOAD_GLOBAL              _ndptr
              424  STORE_FAST               'base'
            426_0  COME_FROM           420  '420'

 L. 338       426  LOAD_GLOBAL              type
              428  LOAD_STR                 'ndpointer_%s'
              430  LOAD_FAST                'name'
              432  BINARY_MODULO    
              434  LOAD_FAST                'base'
              436  BUILD_TUPLE_1         1 

 L. 339       438  LOAD_FAST                'dtype'

 L. 340       440  LOAD_FAST                'shape'

 L. 341       442  LOAD_FAST                'ndim'

 L. 342       444  LOAD_FAST                'num'

 L. 339       446  LOAD_CONST               ('_dtype_', '_shape_', '_ndim_', '_flags_')
              448  BUILD_CONST_KEY_MAP_4     4 

 L. 338       450  CALL_FUNCTION_3       3  ''
              452  STORE_FAST               'klass'

 L. 343       454  LOAD_FAST                'klass'
              456  LOAD_GLOBAL              _pointer_type_cache
              458  LOAD_FAST                'cache_key'
              460  STORE_SUBSCR     

 L. 344       462  LOAD_FAST                'klass'
              464  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 258_0


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
            except KeyError:
                raise NotImplementedError('Converting {!r} to a ctypes type'.formatdtype)
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