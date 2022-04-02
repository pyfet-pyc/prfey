# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\core\_methods.py
"""
Array methods which are called by both the C-code for the method
and the Python code for the NumPy-namespace function

"""
import warnings
import numpy.core as mu
import numpy.core as um
from numpy.core._asarray import asanyarray
import numpy.core as nt
from numpy.core import _exceptions
from numpy._globals import _NoValue
from numpy.compat import pickle, os_fspath, contextlib_nullcontext
umr_maximum = um.maximum.reduce
umr_minimum = um.minimum.reduce
umr_sum = um.add.reduce
umr_prod = um.multiply.reduce
umr_any = um.logical_or.reduce
umr_all = um.logical_and.reduce
_complex_to_float = {nt.dtype(nt.csingle): nt.dtype(nt.single), 
 nt.dtype(nt.cdouble): nt.dtype(nt.double)}
if nt.dtype(nt.longdouble) != nt.dtype(nt.double):
    _complex_to_float.update({nt.dtype(nt.clongdouble): nt.dtype(nt.longdouble)})

def _amax(a, axis=None, out=None, keepdims=False, initial=_NoValue, where=True):
    return umr_maximum(a, axis, None, out, keepdims, initial, where)


def _amin(a, axis=None, out=None, keepdims=False, initial=_NoValue, where=True):
    return umr_minimum(a, axis, None, out, keepdims, initial, where)


def _sum(a, axis=None, dtype=None, out=None, keepdims=False, initial=_NoValue, where=True):
    return umr_sum(a, axis, dtype, out, keepdims, initial, where)


def _prod(a, axis=None, dtype=None, out=None, keepdims=False, initial=_NoValue, where=True):
    return umr_prod(a, axis, dtype, out, keepdims, initial, where)


def _any(a, axis=None, dtype=None, out=None, keepdims=False):
    return umr_any(a, axis, dtype, out, keepdims)


def _all(a, axis=None, dtype=None, out=None, keepdims=False):
    return umr_all(a, axis, dtype, out, keepdims)


def _count_reduce_items(arr, axis):
    if axis is None:
        axis = tuple(range(arr.ndim))
    if not isinstance(axis, tuple):
        axis = (
         axis,)
    items = 1
    for ax in axis:
        items *= arr.shape[mu.normalize_axis_index(ax, arr.ndim)]
    else:
        return items


def _clip_dep_is_scalar_nan--- This code section failed: ---

 L.  74         0  LOAD_CONST               0
                2  LOAD_CONST               ('ndim',)
                4  IMPORT_NAME_ATTR         numpy.core.fromnumeric
                6  IMPORT_FROM              ndim
                8  STORE_FAST               'ndim'
               10  POP_TOP          

 L.  75        12  LOAD_FAST                'ndim'
               14  LOAD_FAST                'a'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               0
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L.  76        24  LOAD_CONST               False
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.  77        28  SETUP_FINALLY        42  'to 42'

 L.  78        30  LOAD_GLOBAL              um
               32  LOAD_METHOD              isnan
               34  LOAD_FAST                'a'
               36  CALL_METHOD_1         1  ''
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    28  '28'

 L.  79        42  DUP_TOP          
               44  LOAD_GLOBAL              TypeError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  80        56  POP_EXCEPT       
               58  LOAD_CONST               False
               60  RETURN_VALUE     
             62_0  COME_FROM            48  '48'
               62  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 58


def _clip_dep_is_byte_swapped(a):
    if isinstance(a, mu.ndarray):
        return not a.dtype.isnative
    return False


def _clip_dep_invoke_with_casting--- This code section failed: ---

 L.  89         0  LOAD_FAST                'casting'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L.  90         8  LOAD_FAST                'ufunc'
               10  LOAD_FAST                'args'
               12  LOAD_FAST                'out'
               14  LOAD_FAST                'casting'
               16  LOAD_CONST               ('out', 'casting')
               18  BUILD_CONST_KEY_MAP_2     2 
               20  LOAD_FAST                'kwargs'
               22  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  RETURN_VALUE     
             28_0  COME_FROM             6  '6'

 L.  93        28  SETUP_FINALLY        50  'to 50'

 L.  94        30  LOAD_FAST                'ufunc'
               32  LOAD_FAST                'args'
               34  LOAD_STR                 'out'
               36  LOAD_FAST                'out'
               38  BUILD_MAP_1           1 
               40  LOAD_FAST                'kwargs'
               42  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    28  '28'

 L.  95        50  DUP_TOP          
               52  LOAD_GLOBAL              _exceptions
               54  LOAD_ATTR                _UFuncOutputCastingError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE   136  'to 136'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY       124  'to 124'

 L.  97        68  LOAD_GLOBAL              warnings
               70  LOAD_ATTR                warn

 L.  98        72  LOAD_STR                 'Converting the output of clip from {!r} to {!r} is deprecated. Pass `casting="unsafe"` explicitly to silence this warning, or correct the type of the variables.'
               74  LOAD_METHOD              format

 L. 100        76  LOAD_FAST                'e'
               78  LOAD_ATTR                from_

 L. 100        80  LOAD_FAST                'e'
               82  LOAD_ATTR                to

 L.  98        84  CALL_METHOD_2         2  ''

 L. 101        86  LOAD_GLOBAL              DeprecationWarning

 L. 102        88  LOAD_CONST               2

 L.  97        90  LOAD_CONST               ('stacklevel',)
               92  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               94  POP_TOP          

 L. 104        96  LOAD_FAST                'ufunc'
               98  LOAD_FAST                'args'
              100  LOAD_FAST                'out'
              102  LOAD_STR                 'unsafe'
              104  LOAD_CONST               ('out', 'casting')
              106  BUILD_CONST_KEY_MAP_2     2 
              108  LOAD_FAST                'kwargs'
              110  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              112  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              114  ROT_FOUR         
              116  POP_BLOCK        
              118  POP_EXCEPT       
              120  CALL_FINALLY        124  'to 124'
              122  RETURN_VALUE     
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM_FINALLY    66  '66'
              124  LOAD_CONST               None
              126  STORE_FAST               'e'
              128  DELETE_FAST              'e'
              130  END_FINALLY      
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM            58  '58'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'

Parse error at or near `POP_BLOCK' instruction at offset 116


def _clip(a, min=None, max=None, out=None, *, casting=None, **kwargs):
    if min is None:
        if max is None:
            raise ValueError('One of max or min must be given')
    if not _clip_dep_is_byte_swapped(a):
        if not _clip_dep_is_byte_swapped(out):
            using_deprecated_nan = False
            if _clip_dep_is_scalar_nan(min):
                min = -float('inf')
                using_deprecated_nan = True
            if _clip_dep_is_scalar_nan(max):
                max = float('inf')
                using_deprecated_nan = True
            if using_deprecated_nan:
                warnings.warn('Passing `np.nan` to mean no clipping in np.clip has always been unreliable, and is now deprecated. In future, this will always return nan, like it already does when min or max are arrays that contain nan. To skip a bound, pass either None or an np.inf of an appropriate sign.',
                  DeprecationWarning,
                  stacklevel=2)
        if min is None:
            return _clip_dep_invoke_with_casting(
 um.minimum, a, max, out=out, 
             casting=casting, **kwargs)
        if max is None:
            return _clip_dep_invoke_with_casting(
 um.maximum, a, min, out=out, 
             casting=casting, **kwargs)
        return _clip_dep_invoke_with_casting(
 um.clip, a, min, max, out=out, 
         casting=casting, **kwargs)


def _mean(a, axis=None, dtype=None, out=None, keepdims=False):
    arr = asanyarray(a)
    is_float16_result = False
    rcount = _count_reduce_items(arr, axis)
    if rcount == 0:
        warnings.warn('Mean of empty slice.', RuntimeWarning, stacklevel=2)
    if dtype is None:
        if issubclass(arr.dtype.type, (nt.integer, nt.bool_)):
            dtype = mu.dtype('f8')
        elif issubclass(arr.dtype.type, nt.float16):
            dtype = mu.dtype('f4')
            is_float16_result = True
    ret = umr_sum(arr, axis, dtype, out, keepdims)
    if isinstance(ret, mu.ndarray):
        ret = um.true_divide(ret,
          rcount, out=ret, casting='unsafe', subok=False)
        if not is_float16_result or out is None:
            ret = arr.dtype.type(ret)
    elif hasattr(ret, 'dtype'):
        if is_float16_result:
            ret = arr.dtype.type(ret / rcount)
        else:
            ret = ret.dtype.type(ret / rcount)
    else:
        ret = ret / rcount
    return ret


def _var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False):
    arr = asanyarray(a)
    rcount = _count_reduce_items(arr, axis)
    if ddof >= rcount:
        warnings.warn('Degrees of freedom <= 0 for slice', RuntimeWarning, stacklevel=2)
    if dtype is None:
        if issubclass(arr.dtype.type, (nt.integer, nt.bool_)):
            dtype = mu.dtype('f8')
    arrmean = umr_sum(arr, axis, dtype, keepdims=True)
    if isinstance(arrmean, mu.ndarray):
        arrmean = um.true_divide(arrmean,
          rcount, out=arrmean, casting='unsafe', subok=False)
    else:
        arrmean = arrmean.dtype.type(arrmean / rcount)
    x = asanyarray(arr - arrmean)
    if issubclass(arr.dtype.type, (nt.floating, nt.integer)):
        x = um.multiply(x, x, out=x)
    elif x.dtype in _complex_to_float:
        xv = x.view(dtype=(_complex_to_float[x.dtype], (2, )))
        um.multiply(xv, xv, out=xv)
        x = um.add((xv[(Ellipsis, 0)]), (xv[(Ellipsis, 1)]), out=(x.real)).real
    else:
        x = um.multiply(x, (um.conjugate(x)), out=x).real
    ret = umr_sum(x, axis, dtype, out, keepdims)
    rcount = max([rcount - ddof, 0])
    if isinstance(ret, mu.ndarray):
        ret = um.true_divide(ret,
          rcount, out=ret, casting='unsafe', subok=False)
    elif hasattr(ret, 'dtype'):
        ret = ret.dtype.type(ret / rcount)
    else:
        ret = ret / rcount
    return ret


def _std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False):
    ret = _var(a, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims)
    if isinstance(ret, mu.ndarray):
        ret = um.sqrt(ret, out=ret)
    elif hasattr(ret, 'dtype'):
        ret = ret.dtype.type(um.sqrt(ret))
    else:
        ret = um.sqrt(ret)
    return ret


def _ptp(a, axis=None, out=None, keepdims=False):
    return um.subtract(umr_maximum(a, axis, None, out, keepdims), umr_minimum(a, axis, None, None, keepdims), out)


def _dump(self, file, protocol=2):
    if hasattr(file, 'write'):
        ctx = contextlib_nullcontext(file)
    else:
        ctx = open(os_fspath(file), 'wb')
    with ctx as f:
        pickle.dump(self, f, protocol=protocol)


def _dumps(self, protocol=2):
    return pickle.dumps(self, protocol=protocol)