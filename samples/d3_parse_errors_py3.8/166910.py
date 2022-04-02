# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\safearray.py
import threading, array
from ctypes import POINTER, Structure, byref, cast, c_long, memmove, pointer, sizeof
from comtypes import _safearray, IUnknown, com_interface_registry, npsupport
from comtypes.patcher import Patch
numpy = npsupport.numpy
_safearray_type_cache = {}

class _SafeArrayAsNdArrayContextManager(object):
    __doc__ = 'Context manager allowing safe arrays to be extracted as ndarrays.\n\n    This is thread-safe.\n\n    Example\n    -------\n\n    This works in python >= 2.5\n    >>> with safearray_as_ndarray:\n    >>>     my_arr = com_object.AsSafeArray\n    >>> type(my_arr)\n    numpy.ndarray\n\n    '
    thread_local = threading.local()

    def __enter__(self):
        try:
            self.thread_local.count += 1
        except AttributeError:
            self.thread_local.count = 1

    def __exit__(self, exc_type, exc_value, traceback):
        self.thread_local.count -= 1

    def __bool__(self):
        """True if context manager is currently entered on given thread.

        """
        return bool(getattr(self.thread_local, 'count', 0))


safearray_as_ndarray = _SafeArrayAsNdArrayContextManager()

def _midlSAFEARRAY(itemtype):
    """This function mimics the 'SAFEARRAY(aType)' IDL idiom.  It
    returns a subtype of SAFEARRAY, instances will be built with a
    typecode VT_...  corresponding to the aType, which must be one of
    the supported ctypes.
    """
    try:
        return POINTER(_safearray_type_cache[itemtype])
    except KeyError:
        sa_type = _make_safearray_type(itemtype)
        _safearray_type_cache[itemtype] = sa_type
        return POINTER(sa_type)


def _make_safearray_type(itemtype):
    from comtypes.automation import _ctype_to_vartype, VT_RECORD, VT_UNKNOWN, IDispatch, VT_DISPATCH
    meta = type(_safearray.tagSAFEARRAY)
    sa_type = meta.__new__(meta, 'SAFEARRAY_%s' % itemtype.__name__, (
     _safearray.tagSAFEARRAY,), {})
    try:
        vartype = _ctype_to_vartype[itemtype]
        extra = None
    except KeyError:
        if issubclass(itemtype, Structure):
            try:
                guids = itemtype._recordinfo_
            except AttributeError:
                extra = None
            else:
                from comtypes.typeinfo import GetRecordInfoFromGuids
                extra = GetRecordInfoFromGuids(*guids)
            vartype = VT_RECORD
        elif issubclass(itemtype, POINTER(IDispatch)):
            vartype = VT_DISPATCH
            extra = pointer(itemtype._iid_)
        elif issubclass(itemtype, POINTER(IUnknown)):
            vartype = VT_UNKNOWN
            extra = pointer(itemtype._iid_)
        else:
            raise TypeError(itemtype)
    else:

        @Patch(POINTER(sa_type))
        class _(object):
            _itemtype_ = itemtype
            _vartype_ = vartype
            _needsfree = False

            @classmethod
            def create(cls, value, extra=None):
                """Create a POINTER(SAFEARRAY_...) instance of the correct
            type; value is an object containing the items to store.

            Python lists, tuples, and array.array instances containing
            compatible item types can be passed to create
            one-dimensional arrays.  To create multidimensional arrys,
            numpy arrays must be passed.
            """
                if npsupport.isndarray(value):
                    return cls.create_from_ndarray(value, extra)
                pa = _safearray.SafeArrayCreateVectorEx(cls._vartype_, 0, len(value), extra)
                if not pa:
                    if cls._vartype_ == VT_RECORD:
                        if extra is None:
                            raise TypeError('Cannot create SAFEARRAY type VT_RECORD without IRecordInfo.')
                    raise MemoryError()
                pa = cast(pa, cls)
                ptr = POINTER(cls._itemtype_)()
                _safearray.SafeArrayAccessData(pa, byref(ptr))
                try:
                    if isinstance(value, array.array):
                        addr, n = value.buffer_info()
                        nbytes = len(value) * sizeof(cls._itemtype_)
                        memmove(ptr, addr, nbytes)
                    else:
                        for index, item in enumerate(value):
                            ptr[index] = item

                finally:
                    _safearray.SafeArrayUnaccessData(pa)

                return pa

            @classmethod
            def create_from_ndarray(cls, value, extra, lBound=0):
                from comtypes.automation import VARIANT
                if cls._itemtype_ is VARIANT:
                    if value.dtype != npsupport.VARIANT_dtype:
                        value = _ndarray_to_variant_array(value)
                else:
                    ai = value.__array_interface__
                    if ai['version'] != 3:
                        raise TypeError('only __array_interface__ version 3 supported')
                    if cls._itemtype_ != numpy.ctypeslib._typecodes[ai['typestr']]:
                        raise TypeError('Wrong array item type')
                if not value.flags.f_contiguous:
                    value = numpy.array(value, order='F')
                rgsa = (_safearray.SAFEARRAYBOUND * value.ndim)()
                nitems = 1
                for i, d in enumerate(value.shape):
                    nitems *= d
                    rgsa[i].cElements = d
                    rgsa[i].lBound = lBound
                else:
                    pa = _safearray.SafeArrayCreateEx(cls._vartype_, value.ndim, rgsa, extra)
                    if not pa:
                        if cls._vartype_ == VT_RECORD:
                            if extra is None:
                                raise TypeError('Cannot create SAFEARRAY type VT_RECORD without IRecordInfo.')
                        raise MemoryError()
                    pa = cast(pa, cls)
                    ptr = POINTER(cls._itemtype_)()
                    _safearray.SafeArrayAccessData(pa, byref(ptr))
                    try:
                        nbytes = nitems * sizeof(cls._itemtype_)
                        memmove(ptr, value.ctypes.data, nbytes)
                    finally:
                        _safearray.SafeArrayUnaccessData(pa)

                    return pa

            @classmethod
            def from_param(cls, value):
                if not isinstance(value, cls):
                    value = cls.create(value, extra)
                    value._needsfree = True
                return value

            def __getitem__(self, index):
                if index != 0:
                    raise IndexError('Only index 0 allowed')
                return self.unpack()

            def __setitem__(self, index, value):
                raise TypeError('Setting items not allowed')

            def __ctypes_from_outparam__(self):
                self._needsfree = True
                return self[0]

            def __del__(self, _SafeArrayDestroy=_safearray.SafeArrayDestroy):
                if self._needsfree:
                    _SafeArrayDestroy(self)

            def _get_size(self, dim):
                """Return the number of elements for dimension 'dim'"""
                ub = _safearray.SafeArrayGetUBound(self, dim) + 1
                lb = _safearray.SafeArrayGetLBound(self, dim)
                return ub - lb

            def unpack(self):
                """Unpack a POINTER(SAFEARRAY_...) into a Python tuple or ndarray."""
                dim = _safearray.SafeArrayGetDim(self)
                if dim == 1:
                    num_elements = self._get_size(1)
                    result = self._get_elements_raw(num_elements)
                    if safearray_as_ndarray:
                        import numpy
                        return numpy.asarray(result)
                    return tuple(result)
                if dim == 2:
                    rows, cols = self._get_size(1), self._get_size(2)
                    result = self._get_elements_raw(rows * cols)
                    if safearray_as_ndarray:
                        import numpy
                        return numpy.asarray(result).reshape((cols, rows)).T
                    result = [tuple(result[r::rows]) for r in range(rows)]
                    return tuple(result)
                lowerbounds = [_safearray.SafeArrayGetLBound(self, d) for d in range(1, dim + 1)]
                indexes = (c_long * dim)(*lowerbounds)
                upperbounds = [_safearray.SafeArrayGetUBound(self, d) for d in range(1, dim + 1)]
                row = self._get_row(0, indexes, lowerbounds, upperbounds)
                if safearray_as_ndarray:
                    import numpy
                    return numpy.asarray(row)
                return row

            def _get_elements_raw--- This code section failed: ---

 L. 273         0  LOAD_CONST               0
                2  LOAD_CONST               ('VARIANT',)
                4  IMPORT_NAME_ATTR         comtypes.automation
                6  IMPORT_FROM              VARIANT
                8  STORE_FAST               'VARIANT'
               10  POP_TOP          

 L. 277        12  LOAD_GLOBAL              POINTER
               14  LOAD_DEREF               'self'
               16  LOAD_ATTR                _itemtype_
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_0       0  ''
               22  STORE_FAST               'ptr'

 L. 278        24  LOAD_GLOBAL              _safearray
               26  LOAD_METHOD              SafeArrayAccessData
               28  LOAD_DEREF               'self'
               30  LOAD_GLOBAL              byref
               32  LOAD_FAST                'ptr'
               34  CALL_FUNCTION_1       1  ''
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L. 279     40_42  SETUP_FINALLY       338  'to 338'

 L. 280        44  LOAD_DEREF               'self'
               46  LOAD_ATTR                _itemtype_
               48  LOAD_FAST                'VARIANT'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    82  'to 82'

 L. 283        54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 '_make_safearray_type.<locals>._._get_elements_raw.<locals>.<listcomp>'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               60  LOAD_FAST                'ptr'
               62  LOAD_CONST               None
               64  LOAD_FAST                'num_elements'
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  POP_BLOCK        
            76_78  CALL_FINALLY        338  'to 338'
               80  RETURN_VALUE     
             82_0  COME_FROM            52  '52'

 L. 284        82  LOAD_GLOBAL              issubclass
               84  LOAD_DEREF               'self'
               86  LOAD_ATTR                _itemtype_
               88  LOAD_GLOBAL              POINTER
               90  LOAD_GLOBAL              IUnknown
               92  CALL_FUNCTION_1       1  ''
               94  CALL_FUNCTION_2       2  ''
               96  POP_JUMP_IF_FALSE   204  'to 204'

 L. 285        98  LOAD_GLOBAL              _safearray
              100  LOAD_METHOD              SafeArrayGetIID
              102  LOAD_DEREF               'self'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'iid'

 L. 286       108  LOAD_GLOBAL              com_interface_registry
              110  LOAD_GLOBAL              str
              112  LOAD_FAST                'iid'
              114  CALL_FUNCTION_1       1  ''
              116  BINARY_SUBSCR    
              118  STORE_FAST               'itf'

 L. 289       120  LOAD_FAST                'ptr'
              122  LOAD_CONST               None
              124  LOAD_FAST                'num_elements'
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  STORE_FAST               'elems'

 L. 290       132  BUILD_LIST_0          0 
              134  STORE_FAST               'result'

 L. 293       136  LOAD_FAST                'elems'
              138  GET_ITER         
            140_0  COME_FROM           194  '194'
            140_1  COME_FROM           176  '176'
              140  FOR_ITER            196  'to 196'
              142  STORE_FAST               'p'

 L. 294       144  LOAD_GLOBAL              bool
              146  LOAD_FAST                'p'
              148  CALL_FUNCTION_1       1  ''
              150  POP_JUMP_IF_FALSE   178  'to 178'

 L. 295       152  LOAD_FAST                'p'
              154  LOAD_METHOD              AddRef
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          

 L. 296       160  LOAD_FAST                'result'
              162  LOAD_METHOD              append
              164  LOAD_FAST                'p'
              166  LOAD_METHOD              QueryInterface
              168  LOAD_FAST                'itf'
              170  CALL_METHOD_1         1  ''
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK           140  'to 140'
            178_0  COME_FROM           150  '150'

 L. 299       178  LOAD_FAST                'result'
              180  LOAD_METHOD              append
              182  LOAD_GLOBAL              POINTER
              184  LOAD_FAST                'itf'
              186  CALL_FUNCTION_1       1  ''
              188  CALL_FUNCTION_0       0  ''
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK           140  'to 140'
            196_0  COME_FROM           140  '140'

 L. 300       196  LOAD_FAST                'result'
              198  POP_BLOCK        
              200  CALL_FINALLY        338  'to 338'
              202  RETURN_VALUE     
            204_0  COME_FROM            96  '96'

 L. 305       204  LOAD_GLOBAL              issubclass
              206  LOAD_DEREF               'self'
              208  LOAD_ATTR                _itemtype_
              210  LOAD_GLOBAL              Structure
              212  CALL_FUNCTION_2       2  ''
          214_216  POP_JUMP_IF_TRUE    292  'to 292'

 L. 310       218  LOAD_GLOBAL              safearray_as_ndarray
          220_222  POP_JUMP_IF_FALSE   276  'to 276'
              224  LOAD_DEREF               'self'
              226  LOAD_ATTR                _itemtype_

 L. 311       228  LOAD_GLOBAL              list
              230  LOAD_GLOBAL              numpy
              232  LOAD_ATTR                ctypeslib
              234  LOAD_ATTR                _typecodes
              236  LOAD_METHOD              values
              238  CALL_METHOD_0         0  ''
              240  CALL_FUNCTION_1       1  ''

 L. 310       242  COMPARE_OP               in
          244_246  POP_JUMP_IF_FALSE   276  'to 276'

 L. 312       248  LOAD_GLOBAL              numpy
              250  LOAD_ATTR                ctypeslib
              252  LOAD_METHOD              as_array
              254  LOAD_FAST                'ptr'

 L. 313       256  LOAD_FAST                'num_elements'
              258  BUILD_TUPLE_1         1 

 L. 312       260  CALL_METHOD_2         2  ''
              262  STORE_FAST               'arr'

 L. 314       264  LOAD_FAST                'arr'
              266  LOAD_METHOD              copy
              268  CALL_METHOD_0         0  ''
              270  POP_BLOCK        
              272  CALL_FINALLY        338  'to 338'
              274  RETURN_VALUE     
            276_0  COME_FROM           244  '244'
            276_1  COME_FROM           220  '220'

 L. 315       276  LOAD_FAST                'ptr'
              278  LOAD_CONST               None
              280  LOAD_FAST                'num_elements'
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  POP_BLOCK        
              288  CALL_FINALLY        338  'to 338'
              290  RETURN_VALUE     
            292_0  COME_FROM           214  '214'

 L. 317       292  LOAD_CLOSURE             'self'
              294  BUILD_TUPLE_1         1 
              296  LOAD_CODE                <code_object keep_safearray>
              298  LOAD_STR                 '_make_safearray_type.<locals>._._get_elements_raw.<locals>.keep_safearray'
              300  MAKE_FUNCTION_8          'closure'
              302  STORE_DEREF              'keep_safearray'

 L. 320       304  LOAD_CLOSURE             'keep_safearray'
              306  BUILD_TUPLE_1         1 
              308  LOAD_LISTCOMP            '<code_object <listcomp>>'
              310  LOAD_STR                 '_make_safearray_type.<locals>._._get_elements_raw.<locals>.<listcomp>'
              312  MAKE_FUNCTION_8          'closure'
              314  LOAD_FAST                'ptr'
              316  LOAD_CONST               None
              318  LOAD_FAST                'num_elements'
              320  BUILD_SLICE_2         2 
              322  BINARY_SUBSCR    
              324  GET_ITER         
              326  CALL_FUNCTION_1       1  ''
              328  POP_BLOCK        
              330  CALL_FINALLY        338  'to 338'
              332  RETURN_VALUE     
              334  POP_BLOCK        
              336  BEGIN_FINALLY    
            338_0  COME_FROM           330  '330'
            338_1  COME_FROM           288  '288'
            338_2  COME_FROM           272  '272'
            338_3  COME_FROM           200  '200'
            338_4  COME_FROM            76  '76'
            338_5  COME_FROM_FINALLY    40  '40'

 L. 322       338  LOAD_GLOBAL              _safearray
              340  LOAD_METHOD              SafeArrayUnaccessData
              342  LOAD_DEREF               'self'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 76_78

            def _get_row(self, dim, indices, lowerbounds, upperbounds):
                restore = indices[dim]
                result = []
                obj = self._itemtype_()
                pobj = byref(obj)
                if dim + 1 == len(indices):
                    for i in range(indices[dim], upperbounds[dim] + 1):
                        indices[dim] = i
                        _safearray.SafeArrayGetElement(self, indices, pobj)
                        result.append(obj.value)

                else:
                    pass
                for i in range(indices[dim], upperbounds[dim] + 1):
                    indices[dim] = i
                    result.append(self._get_row(dim + 1, indices, lowerbounds, upperbounds))
                else:
                    indices[dim] = restore
                    return tuple(result)

        @Patch(POINTER(POINTER(sa_type)))
        class __(object):

            @classmethod
            def from_param(cls, value):
                if isinstance(value, cls._type_):
                    return byref(value)
                return byref(cls._type_.create(value, extra))

            def __setitem__(self, index, value):
                pa = self._type_.create(value, extra)
                super(POINTER(POINTER(sa_type)), self).__setitem__(index, pa)

        return sa_type


def _ndarray_to_variant_array(value):
    """ Convert an ndarray to VARIANT_dtype array """
    if npsupport.VARIANT_dtype is None:
        msg = 'VARIANT ndarrays require NumPy 1.7 or newer.'
        raise RuntimeError(msg)
    if numpy.issubdtype(value.dtype, npsupport.datetime64):
        return _datetime64_ndarray_to_variant_array(value)
    from comtypes.automation import VARIANT
    varr = numpy.zeros((value.shape), (npsupport.VARIANT_dtype), order='F')
    varr.flat = [VARIANT(v) for v in value.flat]
    return varr


def _datetime64_ndarray_to_variant_array(value):
    """ Convert an ndarray of datetime64 to VARIANT_dtype array """
    from comtypes.automation import VT_DATE
    value = numpy.array(value, 'datetime64[ns]')
    value = value - npsupport.com_null_date64
    value = value / numpy.timedelta64(1, 'D')
    varr = numpy.zeros((value.shape), (npsupport.VARIANT_dtype), order='F')
    varr['vt'] = VT_DATE
    varr['_']['VT_R8'].flat = value.flat
    return varr