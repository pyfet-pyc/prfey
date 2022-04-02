# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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


def _count_reduce_items--- This code section failed: ---

 L.  60         0  LOAD_FAST                'axis'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.  61         8  LOAD_GLOBAL              tuple
               10  LOAD_GLOBAL              range
               12  LOAD_FAST                'arr'
               14  LOAD_ATTR                ndim
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'axis'
             22_0  COME_FROM             6  '6'

 L.  62        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'axis'
               26  LOAD_GLOBAL              tuple
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     38  'to 38'

 L.  63        32  LOAD_FAST                'axis'
               34  BUILD_TUPLE_1         1 
               36  STORE_FAST               'axis'
             38_0  COME_FROM            30  '30'

 L.  64        38  LOAD_CONST               1
               40  STORE_FAST               'items'

 L.  65        42  LOAD_FAST                'axis'
               44  GET_ITER         
             46_0  COME_FROM            74  '74'
               46  FOR_ITER             76  'to 76'
               48  STORE_FAST               'ax'

 L.  66        50  LOAD_FAST                'items'
               52  LOAD_FAST                'arr'
               54  LOAD_ATTR                shape
               56  LOAD_GLOBAL              mu
               58  LOAD_METHOD              normalize_axis_index
               60  LOAD_FAST                'ax'
               62  LOAD_FAST                'arr'
               64  LOAD_ATTR                ndim
               66  CALL_METHOD_2         2  ''
               68  BINARY_SUBSCR    
               70  INPLACE_MULTIPLY 
               72  STORE_FAST               'items'
               74  JUMP_BACK            46  'to 46'
             76_0  COME_FROM            46  '46'

 L.  67        76  LOAD_FAST                'items'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


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
               46  <121>                60  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  80        54  POP_EXCEPT       
               56  LOAD_CONST               False
               58  RETURN_VALUE     
               60  <48>             

Parse error at or near `<121>' instruction at offset 46


def _clip_dep_is_byte_swapped(a):
    if isinstanceamu.ndarray:
        return not a.dtype.isnative
    return False


def _clip_dep_invoke_with_casting--- This code section failed: ---

 L.  89         0  LOAD_FAST                'casting'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L.  90         8  LOAD_FAST                'ufunc'
               10  LOAD_FAST                'args'
               12  LOAD_FAST                'out'
               14  LOAD_FAST                'casting'
               16  LOAD_CONST               ('out', 'casting')
               18  BUILD_CONST_KEY_MAP_2     2 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
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
               42  <164>                 1  ''
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    28  '28'

 L.  95        50  DUP_TOP          
               52  LOAD_GLOBAL              _exceptions
               54  LOAD_ATTR                _UFuncOutputCastingError
               56  <121>               134  ''
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY       126  'to 126'

 L.  97        66  LOAD_GLOBAL              warnings
               68  LOAD_ATTR                warn

 L.  98        70  LOAD_STR                 'Converting the output of clip from {!r} to {!r} is deprecated. Pass `casting="unsafe"` explicitly to silence this warning, or correct the type of the variables.'
               72  LOAD_METHOD              format

 L. 100        74  LOAD_FAST                'e'
               76  LOAD_ATTR                from_
               78  LOAD_FAST                'e'
               80  LOAD_ATTR                to

 L.  98        82  CALL_METHOD_2         2  ''

 L. 101        84  LOAD_GLOBAL              DeprecationWarning

 L. 102        86  LOAD_CONST               2

 L.  97        88  LOAD_CONST               ('stacklevel',)
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  POP_TOP          

 L. 104        94  LOAD_FAST                'ufunc'
               96  LOAD_FAST                'args'
               98  LOAD_FAST                'out'
              100  LOAD_STR                 'unsafe'
              102  LOAD_CONST               ('out', 'casting')
              104  BUILD_CONST_KEY_MAP_2     2 
              106  LOAD_FAST                'kwargs'
              108  <164>                 1  ''
              110  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              112  POP_BLOCK        
              114  ROT_FOUR         
              116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  STORE_FAST               'e'
              122  DELETE_FAST              'e'
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY    64  '64'
              126  LOAD_CONST               None
              128  STORE_FAST               'e'
              130  DELETE_FAST              'e'
              132  <48>             
              134  <48>             

Parse error at or near `None' instruction at offset -1


def _clip--- This code section failed: ---

 L. 107         0  LOAD_FAST                'min'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_FAST                'max'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 108        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'One of max or min must be given'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 113        24  LOAD_GLOBAL              _clip_dep_is_byte_swapped
               26  LOAD_FAST                'a'
               28  CALL_FUNCTION_1       1  ''
               30  POP_JUMP_IF_TRUE    106  'to 106'
               32  LOAD_GLOBAL              _clip_dep_is_byte_swapped
               34  LOAD_FAST                'out'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_TRUE    106  'to 106'

 L. 114        40  LOAD_CONST               False
               42  STORE_FAST               'using_deprecated_nan'

 L. 115        44  LOAD_GLOBAL              _clip_dep_is_scalar_nan
               46  LOAD_FAST                'min'
               48  CALL_FUNCTION_1       1  ''
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 116        52  LOAD_GLOBAL              float
               54  LOAD_STR                 'inf'
               56  CALL_FUNCTION_1       1  ''
               58  UNARY_NEGATIVE   
               60  STORE_FAST               'min'

 L. 117        62  LOAD_CONST               True
               64  STORE_FAST               'using_deprecated_nan'
             66_0  COME_FROM            50  '50'

 L. 118        66  LOAD_GLOBAL              _clip_dep_is_scalar_nan
               68  LOAD_FAST                'max'
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 119        74  LOAD_GLOBAL              float
               76  LOAD_STR                 'inf'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'max'

 L. 120        82  LOAD_CONST               True
               84  STORE_FAST               'using_deprecated_nan'
             86_0  COME_FROM            72  '72'

 L. 121        86  LOAD_FAST                'using_deprecated_nan'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 122        90  LOAD_GLOBAL              warnings
               92  LOAD_ATTR                warn

 L. 123        94  LOAD_STR                 'Passing `np.nan` to mean no clipping in np.clip has always been unreliable, and is now deprecated. In future, this will always return nan, like it already does when min or max are arrays that contain nan. To skip a bound, pass either None or an np.inf of an appropriate sign.'

 L. 129        96  LOAD_GLOBAL              DeprecationWarning

 L. 130        98  LOAD_CONST               2

 L. 122       100  LOAD_CONST               ('stacklevel',)
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  POP_TOP          
            106_0  COME_FROM            88  '88'
            106_1  COME_FROM            38  '38'
            106_2  COME_FROM            30  '30'

 L. 133       106  LOAD_FAST                'min'
              108  LOAD_CONST               None
              110  <117>                 0  ''
              112  POP_JUMP_IF_FALSE   142  'to 142'

 L. 134       114  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 135       116  LOAD_GLOBAL              um
              118  LOAD_ATTR                minimum
              120  LOAD_FAST                'a'
              122  LOAD_FAST                'max'

 L. 134       124  BUILD_TUPLE_3         3 

 L. 135       126  LOAD_FAST                'out'
              128  LOAD_FAST                'casting'

 L. 134       130  LOAD_CONST               ('out', 'casting')
              132  BUILD_CONST_KEY_MAP_2     2 

 L. 135       134  LOAD_FAST                'kwargs'

 L. 134       136  <164>                 1  ''
              138  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              140  RETURN_VALUE     
            142_0  COME_FROM           112  '112'

 L. 136       142  LOAD_FAST                'max'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   178  'to 178'

 L. 137       150  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 138       152  LOAD_GLOBAL              um
              154  LOAD_ATTR                maximum
              156  LOAD_FAST                'a'
              158  LOAD_FAST                'min'

 L. 137       160  BUILD_TUPLE_3         3 

 L. 138       162  LOAD_FAST                'out'
              164  LOAD_FAST                'casting'

 L. 137       166  LOAD_CONST               ('out', 'casting')
              168  BUILD_CONST_KEY_MAP_2     2 

 L. 138       170  LOAD_FAST                'kwargs'

 L. 137       172  <164>                 1  ''
              174  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              176  RETURN_VALUE     
            178_0  COME_FROM           148  '148'

 L. 140       178  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 141       180  LOAD_GLOBAL              um
              182  LOAD_ATTR                clip
              184  LOAD_FAST                'a'
              186  LOAD_FAST                'min'
              188  LOAD_FAST                'max'

 L. 140       190  BUILD_TUPLE_4         4 

 L. 141       192  LOAD_FAST                'out'
              194  LOAD_FAST                'casting'

 L. 140       196  LOAD_CONST               ('out', 'casting')
              198  BUILD_CONST_KEY_MAP_2     2 

 L. 141       200  LOAD_FAST                'kwargs'

 L. 140       202  <164>                 1  ''
              204  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              206  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _mean--- This code section failed: ---

 L. 144         0  LOAD_GLOBAL              asanyarray
                2  LOAD_FAST                'a'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'arr'

 L. 146         8  LOAD_CONST               False
               10  STORE_FAST               'is_float16_result'

 L. 147        12  LOAD_GLOBAL              _count_reduce_items
               14  LOAD_FAST                'arr'
               16  LOAD_FAST                'axis'
               18  CALL_FUNCTION_2       2  ''
               20  STORE_FAST               'rcount'

 L. 149        22  LOAD_FAST                'rcount'
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    46  'to 46'

 L. 150        30  LOAD_GLOBAL              warnings
               32  LOAD_ATTR                warn
               34  LOAD_STR                 'Mean of empty slice.'
               36  LOAD_GLOBAL              RuntimeWarning
               38  LOAD_CONST               2
               40  LOAD_CONST               ('stacklevel',)
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  POP_TOP          
             46_0  COME_FROM            28  '28'

 L. 153        46  LOAD_FAST                'dtype'
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_FALSE   118  'to 118'

 L. 154        54  LOAD_GLOBAL              issubclass
               56  LOAD_FAST                'arr'
               58  LOAD_ATTR                dtype
               60  LOAD_ATTR                type
               62  LOAD_GLOBAL              nt
               64  LOAD_ATTR                integer
               66  LOAD_GLOBAL              nt
               68  LOAD_ATTR                bool_
               70  BUILD_TUPLE_2         2 
               72  CALL_FUNCTION_2       2  ''
               74  POP_JUMP_IF_FALSE    88  'to 88'

 L. 155        76  LOAD_GLOBAL              mu
               78  LOAD_METHOD              dtype
               80  LOAD_STR                 'f8'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'dtype'
               86  JUMP_FORWARD        118  'to 118'
             88_0  COME_FROM            74  '74'

 L. 156        88  LOAD_GLOBAL              issubclass
               90  LOAD_FAST                'arr'
               92  LOAD_ATTR                dtype
               94  LOAD_ATTR                type
               96  LOAD_GLOBAL              nt
               98  LOAD_ATTR                float16
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L. 157       104  LOAD_GLOBAL              mu
              106  LOAD_METHOD              dtype
              108  LOAD_STR                 'f4'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'dtype'

 L. 158       114  LOAD_CONST               True
              116  STORE_FAST               'is_float16_result'
            118_0  COME_FROM           102  '102'
            118_1  COME_FROM            86  '86'
            118_2  COME_FROM            52  '52'

 L. 160       118  LOAD_GLOBAL              umr_sum
              120  LOAD_FAST                'arr'
              122  LOAD_FAST                'axis'
              124  LOAD_FAST                'dtype'
              126  LOAD_FAST                'out'
              128  LOAD_FAST                'keepdims'
              130  CALL_FUNCTION_5       5  ''
              132  STORE_FAST               'ret'

 L. 161       134  LOAD_GLOBAL              isinstance
              136  LOAD_FAST                'ret'
              138  LOAD_GLOBAL              mu
              140  LOAD_ATTR                ndarray
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   192  'to 192'

 L. 162       146  LOAD_GLOBAL              um
              148  LOAD_ATTR                true_divide

 L. 163       150  LOAD_FAST                'ret'
              152  LOAD_FAST                'rcount'
              154  LOAD_FAST                'ret'
              156  LOAD_STR                 'unsafe'
              158  LOAD_CONST               False

 L. 162       160  LOAD_CONST               ('out', 'casting', 'subok')
              162  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              164  STORE_FAST               'ret'

 L. 164       166  LOAD_FAST                'is_float16_result'
              168  POP_JUMP_IF_FALSE   250  'to 250'
              170  LOAD_FAST                'out'
              172  LOAD_CONST               None
              174  <117>                 0  ''
              176  POP_JUMP_IF_FALSE   250  'to 250'

 L. 165       178  LOAD_FAST                'arr'
              180  LOAD_ATTR                dtype
              182  LOAD_METHOD              type
              184  LOAD_FAST                'ret'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'ret'
              190  JUMP_FORWARD        250  'to 250'
            192_0  COME_FROM           144  '144'

 L. 166       192  LOAD_GLOBAL              hasattr
              194  LOAD_FAST                'ret'
              196  LOAD_STR                 'dtype'
              198  CALL_FUNCTION_2       2  ''
              200  POP_JUMP_IF_FALSE   242  'to 242'

 L. 167       202  LOAD_FAST                'is_float16_result'
              204  POP_JUMP_IF_FALSE   224  'to 224'

 L. 168       206  LOAD_FAST                'arr'
              208  LOAD_ATTR                dtype
              210  LOAD_METHOD              type
              212  LOAD_FAST                'ret'
              214  LOAD_FAST                'rcount'
              216  BINARY_TRUE_DIVIDE
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'ret'
              222  JUMP_FORWARD        250  'to 250'
            224_0  COME_FROM           204  '204'

 L. 170       224  LOAD_FAST                'ret'
              226  LOAD_ATTR                dtype
              228  LOAD_METHOD              type
              230  LOAD_FAST                'ret'
              232  LOAD_FAST                'rcount'
              234  BINARY_TRUE_DIVIDE
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'ret'
              240  JUMP_FORWARD        250  'to 250'
            242_0  COME_FROM           200  '200'

 L. 172       242  LOAD_FAST                'ret'
              244  LOAD_FAST                'rcount'
              246  BINARY_TRUE_DIVIDE
              248  STORE_FAST               'ret'
            250_0  COME_FROM           240  '240'
            250_1  COME_FROM           222  '222'
            250_2  COME_FROM           190  '190'
            250_3  COME_FROM           176  '176'
            250_4  COME_FROM           168  '168'

 L. 174       250  LOAD_FAST                'ret'
              252  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 50


def _var--- This code section failed: ---

 L. 177         0  LOAD_GLOBAL              asanyarray
                2  LOAD_FAST                'a'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'arr'

 L. 179         8  LOAD_GLOBAL              _count_reduce_items
               10  LOAD_FAST                'arr'
               12  LOAD_FAST                'axis'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'rcount'

 L. 181        18  LOAD_FAST                'ddof'
               20  LOAD_FAST                'rcount'
               22  COMPARE_OP               >=
               24  POP_JUMP_IF_FALSE    42  'to 42'

 L. 182        26  LOAD_GLOBAL              warnings
               28  LOAD_ATTR                warn
               30  LOAD_STR                 'Degrees of freedom <= 0 for slice'
               32  LOAD_GLOBAL              RuntimeWarning

 L. 183        34  LOAD_CONST               2

 L. 182        36  LOAD_CONST               ('stacklevel',)
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  POP_TOP          
             42_0  COME_FROM            24  '24'

 L. 186        42  LOAD_FAST                'dtype'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    82  'to 82'
               50  LOAD_GLOBAL              issubclass
               52  LOAD_FAST                'arr'
               54  LOAD_ATTR                dtype
               56  LOAD_ATTR                type
               58  LOAD_GLOBAL              nt
               60  LOAD_ATTR                integer
               62  LOAD_GLOBAL              nt
               64  LOAD_ATTR                bool_
               66  BUILD_TUPLE_2         2 
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L. 187        72  LOAD_GLOBAL              mu
               74  LOAD_METHOD              dtype
               76  LOAD_STR                 'f8'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'dtype'
             82_0  COME_FROM            70  '70'
             82_1  COME_FROM            48  '48'

 L. 192        82  LOAD_GLOBAL              umr_sum
               84  LOAD_FAST                'arr'
               86  LOAD_FAST                'axis'
               88  LOAD_FAST                'dtype'
               90  LOAD_CONST               True
               92  LOAD_CONST               ('keepdims',)
               94  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               96  STORE_FAST               'arrmean'

 L. 193        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'arrmean'
              102  LOAD_GLOBAL              mu
              104  LOAD_ATTR                ndarray
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_FALSE   132  'to 132'

 L. 194       110  LOAD_GLOBAL              um
              112  LOAD_ATTR                true_divide

 L. 195       114  LOAD_FAST                'arrmean'
              116  LOAD_FAST                'rcount'
              118  LOAD_FAST                'arrmean'
              120  LOAD_STR                 'unsafe'
              122  LOAD_CONST               False

 L. 194       124  LOAD_CONST               ('out', 'casting', 'subok')
              126  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              128  STORE_FAST               'arrmean'
              130  JUMP_FORWARD        148  'to 148'
            132_0  COME_FROM           108  '108'

 L. 197       132  LOAD_FAST                'arrmean'
              134  LOAD_ATTR                dtype
              136  LOAD_METHOD              type
              138  LOAD_FAST                'arrmean'
              140  LOAD_FAST                'rcount'
              142  BINARY_TRUE_DIVIDE
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'arrmean'
            148_0  COME_FROM           130  '130'

 L. 202       148  LOAD_GLOBAL              asanyarray
              150  LOAD_FAST                'arr'
              152  LOAD_FAST                'arrmean'
              154  BINARY_SUBTRACT  
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'x'

 L. 204       160  LOAD_GLOBAL              issubclass
              162  LOAD_FAST                'arr'
              164  LOAD_ATTR                dtype
              166  LOAD_ATTR                type
              168  LOAD_GLOBAL              nt
              170  LOAD_ATTR                floating
              172  LOAD_GLOBAL              nt
              174  LOAD_ATTR                integer
              176  BUILD_TUPLE_2         2 
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L. 205       182  LOAD_GLOBAL              um
              184  LOAD_ATTR                multiply
              186  LOAD_FAST                'x'
              188  LOAD_FAST                'x'
              190  LOAD_FAST                'x'
              192  LOAD_CONST               ('out',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              196  STORE_FAST               'x'
              198  JUMP_FORWARD        304  'to 304'
            200_0  COME_FROM           180  '180'

 L. 207       200  LOAD_FAST                'x'
              202  LOAD_ATTR                dtype
              204  LOAD_GLOBAL              _complex_to_float
              206  <118>                 0  ''
          208_210  POP_JUMP_IF_FALSE   280  'to 280'

 L. 208       212  LOAD_FAST                'x'
              214  LOAD_ATTR                view
              216  LOAD_GLOBAL              _complex_to_float
              218  LOAD_FAST                'x'
              220  LOAD_ATTR                dtype
              222  BINARY_SUBSCR    
              224  LOAD_CONST               (2,)
              226  BUILD_TUPLE_2         2 
              228  LOAD_CONST               ('dtype',)
              230  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              232  STORE_FAST               'xv'

 L. 209       234  LOAD_GLOBAL              um
              236  LOAD_ATTR                multiply
              238  LOAD_FAST                'xv'
              240  LOAD_FAST                'xv'
              242  LOAD_FAST                'xv'
              244  LOAD_CONST               ('out',)
              246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              248  POP_TOP          

 L. 210       250  LOAD_GLOBAL              um
              252  LOAD_ATTR                add
              254  LOAD_FAST                'xv'
              256  LOAD_CONST               (Ellipsis, 0)
              258  BINARY_SUBSCR    
              260  LOAD_FAST                'xv'
              262  LOAD_CONST               (Ellipsis, 1)
              264  BINARY_SUBSCR    
              266  LOAD_FAST                'x'
              268  LOAD_ATTR                real
              270  LOAD_CONST               ('out',)
              272  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              274  LOAD_ATTR                real
              276  STORE_FAST               'x'
              278  JUMP_FORWARD        304  'to 304'
            280_0  COME_FROM           208  '208'

 L. 214       280  LOAD_GLOBAL              um
              282  LOAD_ATTR                multiply
              284  LOAD_FAST                'x'
              286  LOAD_GLOBAL              um
              288  LOAD_METHOD              conjugate
              290  LOAD_FAST                'x'
              292  CALL_METHOD_1         1  ''
              294  LOAD_FAST                'x'
              296  LOAD_CONST               ('out',)
              298  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              300  LOAD_ATTR                real
              302  STORE_FAST               'x'
            304_0  COME_FROM           278  '278'
            304_1  COME_FROM           198  '198'

 L. 216       304  LOAD_GLOBAL              umr_sum
              306  LOAD_FAST                'x'
              308  LOAD_FAST                'axis'
              310  LOAD_FAST                'dtype'
              312  LOAD_FAST                'out'
              314  LOAD_FAST                'keepdims'
              316  CALL_FUNCTION_5       5  ''
              318  STORE_FAST               'ret'

 L. 219       320  LOAD_GLOBAL              max
              322  LOAD_FAST                'rcount'
              324  LOAD_FAST                'ddof'
              326  BINARY_SUBTRACT  
              328  LOAD_CONST               0
              330  BUILD_LIST_2          2 
              332  CALL_FUNCTION_1       1  ''
              334  STORE_FAST               'rcount'

 L. 222       336  LOAD_GLOBAL              isinstance
              338  LOAD_FAST                'ret'
              340  LOAD_GLOBAL              mu
              342  LOAD_ATTR                ndarray
              344  CALL_FUNCTION_2       2  ''
          346_348  POP_JUMP_IF_FALSE   372  'to 372'

 L. 223       350  LOAD_GLOBAL              um
              352  LOAD_ATTR                true_divide

 L. 224       354  LOAD_FAST                'ret'
              356  LOAD_FAST                'rcount'
              358  LOAD_FAST                'ret'
              360  LOAD_STR                 'unsafe'
              362  LOAD_CONST               False

 L. 223       364  LOAD_CONST               ('out', 'casting', 'subok')
              366  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              368  STORE_FAST               'ret'
              370  JUMP_FORWARD        410  'to 410'
            372_0  COME_FROM           346  '346'

 L. 225       372  LOAD_GLOBAL              hasattr
              374  LOAD_FAST                'ret'
              376  LOAD_STR                 'dtype'
              378  CALL_FUNCTION_2       2  ''
          380_382  POP_JUMP_IF_FALSE   402  'to 402'

 L. 226       384  LOAD_FAST                'ret'
              386  LOAD_ATTR                dtype
              388  LOAD_METHOD              type
              390  LOAD_FAST                'ret'
              392  LOAD_FAST                'rcount'
              394  BINARY_TRUE_DIVIDE
              396  CALL_METHOD_1         1  ''
              398  STORE_FAST               'ret'
              400  JUMP_FORWARD        410  'to 410'
            402_0  COME_FROM           380  '380'

 L. 228       402  LOAD_FAST                'ret'
              404  LOAD_FAST                'rcount'
              406  BINARY_TRUE_DIVIDE
              408  STORE_FAST               'ret'
            410_0  COME_FROM           400  '400'
            410_1  COME_FROM           370  '370'

 L. 230       410  LOAD_FAST                'ret'
              412  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46


def _std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False):
    ret = _var(a, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims)
    if isinstanceretmu.ndarray:
        ret = um.sqrt(ret, out=ret)
    elif hasattrret'dtype':
        ret = ret.dtype.type(um.sqrt(ret))
    else:
        ret = um.sqrt(ret)
    return ret


def _ptp(a, axis=None, out=None, keepdims=False):
    return um.subtract(umr_maximum(a, axis, None, out, keepdims), umr_minimum(a, axis, None, None, keepdims), out)


def _dump--- This code section failed: ---

 L. 253         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'file'
                4  LOAD_STR                 'write'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 254        10  LOAD_GLOBAL              contextlib_nullcontext
               12  LOAD_FAST                'file'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'ctx'
               18  JUMP_FORWARD         34  'to 34'
             20_0  COME_FROM             8  '8'

 L. 256        20  LOAD_GLOBAL              open
               22  LOAD_GLOBAL              os_fspath
               24  LOAD_FAST                'file'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_STR                 'wb'
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'ctx'
             34_0  COME_FROM            18  '18'

 L. 257        34  LOAD_FAST                'ctx'
               36  SETUP_WITH           70  'to 70'
               38  STORE_FAST               'f'

 L. 258        40  LOAD_GLOBAL              pickle
               42  LOAD_ATTR                dump
               44  LOAD_FAST                'self'
               46  LOAD_FAST                'f'
               48  LOAD_FAST                'protocol'
               50  LOAD_CONST               ('protocol',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  POP_TOP          
               56  POP_BLOCK        
               58  LOAD_CONST               None
               60  DUP_TOP          
               62  DUP_TOP          
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          
               68  JUMP_FORWARD         86  'to 86'
             70_0  COME_FROM_WITH       36  '36'
               70  <49>             
               72  POP_JUMP_IF_TRUE     76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          
               82  POP_EXCEPT       
               84  POP_TOP          
             86_0  COME_FROM            68  '68'

Parse error at or near `DUP_TOP' instruction at offset 60


def _dumps(self, protocol=2):
    return pickle.dumps(self, protocol=protocol)