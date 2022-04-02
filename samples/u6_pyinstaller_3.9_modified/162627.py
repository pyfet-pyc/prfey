# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\_methods.py
"""
Array methods which are called by both the C-code for the method
and the Python code for the NumPy-namespace function

"""
import warnings
from contextlib import nullcontext
import numpy.core as mu
import numpy.core as um
from numpy.core.multiarray import asanyarray
import numpy.core as nt
from numpy.core import _exceptions
from numpy._globals import _NoValue
from numpy.compat import pickle, os_fspath
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


def _any--- This code section failed: ---

 L.  56         0  LOAD_FAST                'where'
                2  LOAD_CONST               True
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  57         8  LOAD_GLOBAL              umr_any
               10  LOAD_FAST                'a'
               12  LOAD_FAST                'axis'
               14  LOAD_FAST                'dtype'
               16  LOAD_FAST                'out'
               18  LOAD_FAST                'keepdims'
               20  CALL_FUNCTION_5       5  ''
               22  RETURN_VALUE     
             24_0  COME_FROM             6  '6'

 L.  58        24  LOAD_GLOBAL              umr_any
               26  LOAD_FAST                'a'
               28  LOAD_FAST                'axis'
               30  LOAD_FAST                'dtype'
               32  LOAD_FAST                'out'
               34  LOAD_FAST                'keepdims'
               36  LOAD_FAST                'where'
               38  LOAD_CONST               ('where',)
               40  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _all--- This code section failed: ---

 L.  62         0  LOAD_FAST                'where'
                2  LOAD_CONST               True
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  63         8  LOAD_GLOBAL              umr_all
               10  LOAD_FAST                'a'
               12  LOAD_FAST                'axis'
               14  LOAD_FAST                'dtype'
               16  LOAD_FAST                'out'
               18  LOAD_FAST                'keepdims'
               20  CALL_FUNCTION_5       5  ''
               22  RETURN_VALUE     
             24_0  COME_FROM             6  '6'

 L.  64        24  LOAD_GLOBAL              umr_all
               26  LOAD_FAST                'a'
               28  LOAD_FAST                'axis'
               30  LOAD_FAST                'dtype'
               32  LOAD_FAST                'out'
               34  LOAD_FAST                'keepdims'
               36  LOAD_FAST                'where'
               38  LOAD_CONST               ('where',)
               40  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _count_reduce_items--- This code section failed: ---

 L.  68         0  LOAD_FAST                'where'
                2  LOAD_CONST               True
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    94  'to 94'

 L.  70         8  LOAD_FAST                'axis'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    32  'to 32'

 L.  71        16  LOAD_GLOBAL              tuple
               18  LOAD_GLOBAL              range
               20  LOAD_FAST                'arr'
               22  LOAD_ATTR                ndim
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'axis'
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            14  '14'

 L.  72        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'axis'
               36  LOAD_GLOBAL              tuple
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     48  'to 48'

 L.  73        42  LOAD_FAST                'axis'
               44  BUILD_TUPLE_1         1 
               46  STORE_FAST               'axis'
             48_0  COME_FROM            40  '40'
             48_1  COME_FROM            30  '30'

 L.  74        48  LOAD_GLOBAL              nt
               50  LOAD_METHOD              intp
               52  LOAD_CONST               1
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'items'

 L.  75        58  LOAD_FAST                'axis'
               60  GET_ITER         
               62  FOR_ITER             92  'to 92'
               64  STORE_FAST               'ax'

 L.  76        66  LOAD_FAST                'items'
               68  LOAD_FAST                'arr'
               70  LOAD_ATTR                shape
               72  LOAD_GLOBAL              mu
               74  LOAD_METHOD              normalize_axis_index
               76  LOAD_FAST                'ax'
               78  LOAD_FAST                'arr'
               80  LOAD_ATTR                ndim
               82  CALL_METHOD_2         2  ''
               84  BINARY_SUBSCR    
               86  INPLACE_MULTIPLY 
               88  STORE_FAST               'items'
               90  JUMP_BACK            62  'to 62'
               92  JUMP_FORWARD        132  'to 132'
             94_0  COME_FROM             6  '6'

 L.  82        94  LOAD_CONST               0
               96  LOAD_CONST               ('broadcast_to',)
               98  IMPORT_NAME_ATTR         numpy.lib.stride_tricks
              100  IMPORT_FROM              broadcast_to
              102  STORE_FAST               'broadcast_to'
              104  POP_TOP          

 L.  84       106  LOAD_GLOBAL              umr_sum
              108  LOAD_FAST                'broadcast_to'
              110  LOAD_FAST                'where'
              112  LOAD_FAST                'arr'
              114  LOAD_ATTR                shape
              116  CALL_FUNCTION_2       2  ''
              118  LOAD_FAST                'axis'
              120  LOAD_GLOBAL              nt
              122  LOAD_ATTR                intp
              124  LOAD_CONST               None

 L.  85       126  LOAD_FAST                'keepdims'

 L.  84       128  CALL_FUNCTION_5       5  ''
              130  STORE_FAST               'items'
            132_0  COME_FROM            92  '92'

 L.  86       132  LOAD_FAST                'items'
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _clip_dep_is_scalar_nan--- This code section failed: ---

 L.  93         0  LOAD_CONST               0
                2  LOAD_CONST               ('ndim',)
                4  IMPORT_NAME_ATTR         numpy.core.fromnumeric
                6  IMPORT_FROM              ndim
                8  STORE_FAST               'ndim'
               10  POP_TOP          

 L.  94        12  LOAD_FAST                'ndim'
               14  LOAD_FAST                'a'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               0
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L.  95        24  LOAD_CONST               False
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.  96        28  SETUP_FINALLY        42  'to 42'

 L.  97        30  LOAD_GLOBAL              um
               32  LOAD_METHOD              isnan
               34  LOAD_FAST                'a'
               36  CALL_METHOD_1         1  ''
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    28  '28'

 L.  98        42  DUP_TOP          
               44  LOAD_GLOBAL              TypeError
               46  <121>                60  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  99        54  POP_EXCEPT       
               56  LOAD_CONST               False
               58  RETURN_VALUE     
               60  <48>             

Parse error at or near `<121>' instruction at offset 46


def _clip_dep_is_byte_swapped(a):
    if isinstanceamu.ndarray:
        return not a.dtype.isnative
    return False


def _clip_dep_invoke_with_casting--- This code section failed: ---

 L. 108         0  LOAD_FAST                'casting'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 109         8  LOAD_FAST                'ufunc'
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

 L. 112        28  SETUP_FINALLY        50  'to 50'

 L. 113        30  LOAD_FAST                'ufunc'
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

 L. 114        50  DUP_TOP          
               52  LOAD_GLOBAL              _exceptions
               54  LOAD_ATTR                _UFuncOutputCastingError
               56  <121>               134  ''
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY       126  'to 126'

 L. 116        66  LOAD_GLOBAL              warnings
               68  LOAD_ATTR                warn

 L. 117        70  LOAD_STR                 'Converting the output of clip from {!r} to {!r} is deprecated. Pass `casting="unsafe"` explicitly to silence this warning, or correct the type of the variables.'
               72  LOAD_METHOD              format

 L. 119        74  LOAD_FAST                'e'
               76  LOAD_ATTR                from_
               78  LOAD_FAST                'e'
               80  LOAD_ATTR                to

 L. 117        82  CALL_METHOD_2         2  ''

 L. 120        84  LOAD_GLOBAL              DeprecationWarning

 L. 121        86  LOAD_CONST               2

 L. 116        88  LOAD_CONST               ('stacklevel',)
               90  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               92  POP_TOP          

 L. 123        94  LOAD_FAST                'ufunc'
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

 L. 126         0  LOAD_FAST                'min'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_FAST                'max'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 127        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'One of max or min must be given'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 132        24  LOAD_GLOBAL              _clip_dep_is_byte_swapped
               26  LOAD_FAST                'a'
               28  CALL_FUNCTION_1       1  ''
               30  POP_JUMP_IF_TRUE    106  'to 106'
               32  LOAD_GLOBAL              _clip_dep_is_byte_swapped
               34  LOAD_FAST                'out'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_TRUE    106  'to 106'

 L. 133        40  LOAD_CONST               False
               42  STORE_FAST               'using_deprecated_nan'

 L. 134        44  LOAD_GLOBAL              _clip_dep_is_scalar_nan
               46  LOAD_FAST                'min'
               48  CALL_FUNCTION_1       1  ''
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 135        52  LOAD_GLOBAL              float
               54  LOAD_STR                 'inf'
               56  CALL_FUNCTION_1       1  ''
               58  UNARY_NEGATIVE   
               60  STORE_FAST               'min'

 L. 136        62  LOAD_CONST               True
               64  STORE_FAST               'using_deprecated_nan'
             66_0  COME_FROM            50  '50'

 L. 137        66  LOAD_GLOBAL              _clip_dep_is_scalar_nan
               68  LOAD_FAST                'max'
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 138        74  LOAD_GLOBAL              float
               76  LOAD_STR                 'inf'
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'max'

 L. 139        82  LOAD_CONST               True
               84  STORE_FAST               'using_deprecated_nan'
             86_0  COME_FROM            72  '72'

 L. 140        86  LOAD_FAST                'using_deprecated_nan'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 141        90  LOAD_GLOBAL              warnings
               92  LOAD_ATTR                warn

 L. 142        94  LOAD_STR                 'Passing `np.nan` to mean no clipping in np.clip has always been unreliable, and is now deprecated. In future, this will always return nan, like it already does when min or max are arrays that contain nan. To skip a bound, pass either None or an np.inf of an appropriate sign.'

 L. 148        96  LOAD_GLOBAL              DeprecationWarning

 L. 149        98  LOAD_CONST               2

 L. 141       100  LOAD_CONST               ('stacklevel',)
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  POP_TOP          
            106_0  COME_FROM            88  '88'
            106_1  COME_FROM            38  '38'
            106_2  COME_FROM            30  '30'

 L. 152       106  LOAD_FAST                'min'
              108  LOAD_CONST               None
              110  <117>                 0  ''
              112  POP_JUMP_IF_FALSE   142  'to 142'

 L. 153       114  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 154       116  LOAD_GLOBAL              um
              118  LOAD_ATTR                minimum
              120  LOAD_FAST                'a'
              122  LOAD_FAST                'max'

 L. 153       124  BUILD_TUPLE_3         3 

 L. 154       126  LOAD_FAST                'out'
              128  LOAD_FAST                'casting'

 L. 153       130  LOAD_CONST               ('out', 'casting')
              132  BUILD_CONST_KEY_MAP_2     2 

 L. 154       134  LOAD_FAST                'kwargs'

 L. 153       136  <164>                 1  ''
              138  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              140  RETURN_VALUE     
            142_0  COME_FROM           112  '112'

 L. 155       142  LOAD_FAST                'max'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   178  'to 178'

 L. 156       150  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 157       152  LOAD_GLOBAL              um
              154  LOAD_ATTR                maximum
              156  LOAD_FAST                'a'
              158  LOAD_FAST                'min'

 L. 156       160  BUILD_TUPLE_3         3 

 L. 157       162  LOAD_FAST                'out'
              164  LOAD_FAST                'casting'

 L. 156       166  LOAD_CONST               ('out', 'casting')
              168  BUILD_CONST_KEY_MAP_2     2 

 L. 157       170  LOAD_FAST                'kwargs'

 L. 156       172  <164>                 1  ''
              174  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              176  RETURN_VALUE     
            178_0  COME_FROM           148  '148'

 L. 159       178  LOAD_GLOBAL              _clip_dep_invoke_with_casting

 L. 160       180  LOAD_GLOBAL              um
              182  LOAD_ATTR                clip
              184  LOAD_FAST                'a'
              186  LOAD_FAST                'min'
              188  LOAD_FAST                'max'

 L. 159       190  BUILD_TUPLE_4         4 

 L. 160       192  LOAD_FAST                'out'
              194  LOAD_FAST                'casting'

 L. 159       196  LOAD_CONST               ('out', 'casting')
              198  BUILD_CONST_KEY_MAP_2     2 

 L. 160       200  LOAD_FAST                'kwargs'

 L. 159       202  <164>                 1  ''
              204  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              206  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _mean--- This code section failed: ---

 L. 163         0  LOAD_GLOBAL              asanyarray
                2  LOAD_FAST                'a'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'arr'

 L. 165         8  LOAD_CONST               False
               10  STORE_FAST               'is_float16_result'

 L. 167        12  LOAD_GLOBAL              _count_reduce_items
               14  LOAD_FAST                'arr'
               16  LOAD_FAST                'axis'
               18  LOAD_FAST                'keepdims'
               20  LOAD_FAST                'where'
               22  LOAD_CONST               ('keepdims', 'where')
               24  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               26  STORE_FAST               'rcount'

 L. 168        28  LOAD_FAST                'where'
               30  LOAD_CONST               True
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  LOAD_FAST                'rcount'
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    78  'to 78'
               44  JUMP_FORWARD         62  'to 62'
             46_0  COME_FROM            34  '34'
               46  LOAD_GLOBAL              umr_any
               48  LOAD_FAST                'rcount'
               50  LOAD_CONST               0
               52  COMPARE_OP               ==
               54  LOAD_CONST               None
               56  LOAD_CONST               ('axis',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  POP_JUMP_IF_FALSE    78  'to 78'
             62_0  COME_FROM            44  '44'

 L. 169        62  LOAD_GLOBAL              warnings
               64  LOAD_ATTR                warn
               66  LOAD_STR                 'Mean of empty slice.'
               68  LOAD_GLOBAL              RuntimeWarning
               70  LOAD_CONST               2
               72  LOAD_CONST               ('stacklevel',)
               74  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               76  POP_TOP          
             78_0  COME_FROM            60  '60'
             78_1  COME_FROM            42  '42'

 L. 172        78  LOAD_FAST                'dtype'
               80  LOAD_CONST               None
               82  <117>                 0  ''
               84  POP_JUMP_IF_FALSE   150  'to 150'

 L. 173        86  LOAD_GLOBAL              issubclass
               88  LOAD_FAST                'arr'
               90  LOAD_ATTR                dtype
               92  LOAD_ATTR                type
               94  LOAD_GLOBAL              nt
               96  LOAD_ATTR                integer
               98  LOAD_GLOBAL              nt
              100  LOAD_ATTR                bool_
              102  BUILD_TUPLE_2         2 
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   120  'to 120'

 L. 174       108  LOAD_GLOBAL              mu
              110  LOAD_METHOD              dtype
              112  LOAD_STR                 'f8'
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'dtype'
              118  JUMP_FORWARD        150  'to 150'
            120_0  COME_FROM           106  '106'

 L. 175       120  LOAD_GLOBAL              issubclass
              122  LOAD_FAST                'arr'
              124  LOAD_ATTR                dtype
              126  LOAD_ATTR                type
              128  LOAD_GLOBAL              nt
              130  LOAD_ATTR                float16
              132  CALL_FUNCTION_2       2  ''
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L. 176       136  LOAD_GLOBAL              mu
              138  LOAD_METHOD              dtype
              140  LOAD_STR                 'f4'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'dtype'

 L. 177       146  LOAD_CONST               True
              148  STORE_FAST               'is_float16_result'
            150_0  COME_FROM           134  '134'
            150_1  COME_FROM           118  '118'
            150_2  COME_FROM            84  '84'

 L. 179       150  LOAD_GLOBAL              umr_sum
              152  LOAD_FAST                'arr'
              154  LOAD_FAST                'axis'
              156  LOAD_FAST                'dtype'
              158  LOAD_FAST                'out'
              160  LOAD_FAST                'keepdims'
              162  LOAD_FAST                'where'
              164  LOAD_CONST               ('where',)
              166  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              168  STORE_FAST               'ret'

 L. 180       170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'ret'
              174  LOAD_GLOBAL              mu
              176  LOAD_ATTR                ndarray
              178  CALL_FUNCTION_2       2  ''
              180  POP_JUMP_IF_FALSE   228  'to 228'

 L. 181       182  LOAD_GLOBAL              um
              184  LOAD_ATTR                true_divide

 L. 182       186  LOAD_FAST                'ret'
              188  LOAD_FAST                'rcount'
              190  LOAD_FAST                'ret'
              192  LOAD_STR                 'unsafe'
              194  LOAD_CONST               False

 L. 181       196  LOAD_CONST               ('out', 'casting', 'subok')
              198  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              200  STORE_FAST               'ret'

 L. 183       202  LOAD_FAST                'is_float16_result'
              204  POP_JUMP_IF_FALSE   226  'to 226'
              206  LOAD_FAST                'out'
              208  LOAD_CONST               None
              210  <117>                 0  ''
              212  POP_JUMP_IF_FALSE   226  'to 226'

 L. 184       214  LOAD_FAST                'arr'
              216  LOAD_ATTR                dtype
              218  LOAD_METHOD              type
              220  LOAD_FAST                'ret'
              222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'ret'
            226_0  COME_FROM           212  '212'
            226_1  COME_FROM           204  '204'
              226  JUMP_FORWARD        290  'to 290'
            228_0  COME_FROM           180  '180'

 L. 185       228  LOAD_GLOBAL              hasattr
              230  LOAD_FAST                'ret'
              232  LOAD_STR                 'dtype'
              234  CALL_FUNCTION_2       2  ''
          236_238  POP_JUMP_IF_FALSE   282  'to 282'

 L. 186       240  LOAD_FAST                'is_float16_result'
          242_244  POP_JUMP_IF_FALSE   264  'to 264'

 L. 187       246  LOAD_FAST                'arr'
              248  LOAD_ATTR                dtype
              250  LOAD_METHOD              type
              252  LOAD_FAST                'ret'
              254  LOAD_FAST                'rcount'
              256  BINARY_TRUE_DIVIDE
              258  CALL_METHOD_1         1  ''
              260  STORE_FAST               'ret'
              262  JUMP_FORWARD        280  'to 280'
            264_0  COME_FROM           242  '242'

 L. 189       264  LOAD_FAST                'ret'
              266  LOAD_ATTR                dtype
              268  LOAD_METHOD              type
              270  LOAD_FAST                'ret'
              272  LOAD_FAST                'rcount'
              274  BINARY_TRUE_DIVIDE
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'ret'
            280_0  COME_FROM           262  '262'
              280  JUMP_FORWARD        290  'to 290'
            282_0  COME_FROM           236  '236'

 L. 191       282  LOAD_FAST                'ret'
              284  LOAD_FAST                'rcount'
              286  BINARY_TRUE_DIVIDE
              288  STORE_FAST               'ret'
            290_0  COME_FROM           280  '280'
            290_1  COME_FROM           226  '226'

 L. 193       290  LOAD_FAST                'ret'
              292  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32


def _var--- This code section failed: ---

 L. 197         0  LOAD_GLOBAL              asanyarray
                2  LOAD_FAST                'a'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'arr'

 L. 199         8  LOAD_GLOBAL              _count_reduce_items
               10  LOAD_FAST                'arr'
               12  LOAD_FAST                'axis'
               14  LOAD_FAST                'keepdims'
               16  LOAD_FAST                'where'
               18  LOAD_CONST               ('keepdims', 'where')
               20  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               22  STORE_FAST               'rcount'

 L. 201        24  LOAD_FAST                'where'
               26  LOAD_CONST               True
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    42  'to 42'
               32  LOAD_FAST                'ddof'
               34  LOAD_FAST                'rcount'
               36  COMPARE_OP               >=
               38  POP_JUMP_IF_FALSE    74  'to 74'
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM            30  '30'
               42  LOAD_GLOBAL              umr_any
               44  LOAD_FAST                'ddof'
               46  LOAD_FAST                'rcount'
               48  COMPARE_OP               >=
               50  LOAD_CONST               None
               52  LOAD_CONST               ('axis',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  POP_JUMP_IF_FALSE    74  'to 74'
             58_0  COME_FROM            40  '40'

 L. 202        58  LOAD_GLOBAL              warnings
               60  LOAD_ATTR                warn
               62  LOAD_STR                 'Degrees of freedom <= 0 for slice'
               64  LOAD_GLOBAL              RuntimeWarning

 L. 203        66  LOAD_CONST               2

 L. 202        68  LOAD_CONST               ('stacklevel',)
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  POP_TOP          
             74_0  COME_FROM            56  '56'
             74_1  COME_FROM            38  '38'

 L. 206        74  LOAD_FAST                'dtype'
               76  LOAD_CONST               None
               78  <117>                 0  ''
               80  POP_JUMP_IF_FALSE   114  'to 114'
               82  LOAD_GLOBAL              issubclass
               84  LOAD_FAST                'arr'
               86  LOAD_ATTR                dtype
               88  LOAD_ATTR                type
               90  LOAD_GLOBAL              nt
               92  LOAD_ATTR                integer
               94  LOAD_GLOBAL              nt
               96  LOAD_ATTR                bool_
               98  BUILD_TUPLE_2         2 
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 207       104  LOAD_GLOBAL              mu
              106  LOAD_METHOD              dtype
              108  LOAD_STR                 'f8'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'dtype'
            114_0  COME_FROM           102  '102'
            114_1  COME_FROM            80  '80'

 L. 212       114  LOAD_GLOBAL              umr_sum
              116  LOAD_FAST                'arr'
              118  LOAD_FAST                'axis'
              120  LOAD_FAST                'dtype'
              122  LOAD_CONST               True
              124  LOAD_FAST                'where'
              126  LOAD_CONST               ('keepdims', 'where')
              128  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              130  STORE_FAST               'arrmean'

 L. 215       132  LOAD_FAST                'rcount'
              134  LOAD_ATTR                ndim
              136  LOAD_CONST               0
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   148  'to 148'

 L. 217       142  LOAD_FAST                'rcount'
              144  STORE_FAST               'div'
              146  JUMP_FORWARD        160  'to 160'
            148_0  COME_FROM           140  '140'

 L. 220       148  LOAD_FAST                'rcount'
              150  LOAD_METHOD              reshape
              152  LOAD_FAST                'arrmean'
              154  LOAD_ATTR                shape
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'div'
            160_0  COME_FROM           146  '146'

 L. 221       160  LOAD_GLOBAL              isinstance
              162  LOAD_FAST                'arrmean'
              164  LOAD_GLOBAL              mu
              166  LOAD_ATTR                ndarray
              168  CALL_FUNCTION_2       2  ''
              170  POP_JUMP_IF_FALSE   194  'to 194'

 L. 222       172  LOAD_GLOBAL              um
              174  LOAD_ATTR                true_divide
              176  LOAD_FAST                'arrmean'
              178  LOAD_FAST                'div'
              180  LOAD_FAST                'arrmean'
              182  LOAD_STR                 'unsafe'

 L. 223       184  LOAD_CONST               False

 L. 222       186  LOAD_CONST               ('out', 'casting', 'subok')
              188  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              190  STORE_FAST               'arrmean'
              192  JUMP_FORWARD        210  'to 210'
            194_0  COME_FROM           170  '170'

 L. 225       194  LOAD_FAST                'arrmean'
              196  LOAD_ATTR                dtype
              198  LOAD_METHOD              type
              200  LOAD_FAST                'arrmean'
              202  LOAD_FAST                'rcount'
              204  BINARY_TRUE_DIVIDE
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'arrmean'
            210_0  COME_FROM           192  '192'

 L. 230       210  LOAD_GLOBAL              asanyarray
              212  LOAD_FAST                'arr'
              214  LOAD_FAST                'arrmean'
              216  BINARY_SUBTRACT  
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'x'

 L. 232       222  LOAD_GLOBAL              issubclass
              224  LOAD_FAST                'arr'
              226  LOAD_ATTR                dtype
              228  LOAD_ATTR                type
              230  LOAD_GLOBAL              nt
              232  LOAD_ATTR                floating
              234  LOAD_GLOBAL              nt
              236  LOAD_ATTR                integer
              238  BUILD_TUPLE_2         2 
              240  CALL_FUNCTION_2       2  ''
          242_244  POP_JUMP_IF_FALSE   264  'to 264'

 L. 233       246  LOAD_GLOBAL              um
              248  LOAD_ATTR                multiply
              250  LOAD_FAST                'x'
              252  LOAD_FAST                'x'
              254  LOAD_FAST                'x'
              256  LOAD_CONST               ('out',)
              258  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              260  STORE_FAST               'x'
              262  JUMP_FORWARD        368  'to 368'
            264_0  COME_FROM           242  '242'

 L. 235       264  LOAD_FAST                'x'
              266  LOAD_ATTR                dtype
              268  LOAD_GLOBAL              _complex_to_float
              270  <118>                 0  ''
          272_274  POP_JUMP_IF_FALSE   344  'to 344'

 L. 236       276  LOAD_FAST                'x'
              278  LOAD_ATTR                view
              280  LOAD_GLOBAL              _complex_to_float
              282  LOAD_FAST                'x'
              284  LOAD_ATTR                dtype
              286  BINARY_SUBSCR    
              288  LOAD_CONST               (2,)
              290  BUILD_TUPLE_2         2 
              292  LOAD_CONST               ('dtype',)
              294  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              296  STORE_FAST               'xv'

 L. 237       298  LOAD_GLOBAL              um
              300  LOAD_ATTR                multiply
              302  LOAD_FAST                'xv'
              304  LOAD_FAST                'xv'
              306  LOAD_FAST                'xv'
              308  LOAD_CONST               ('out',)
              310  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              312  POP_TOP          

 L. 238       314  LOAD_GLOBAL              um
              316  LOAD_ATTR                add
              318  LOAD_FAST                'xv'
              320  LOAD_CONST               (Ellipsis, 0)
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'xv'
              326  LOAD_CONST               (Ellipsis, 1)
              328  BINARY_SUBSCR    
              330  LOAD_FAST                'x'
              332  LOAD_ATTR                real
              334  LOAD_CONST               ('out',)
              336  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              338  LOAD_ATTR                real
              340  STORE_FAST               'x'
              342  JUMP_FORWARD        368  'to 368'
            344_0  COME_FROM           272  '272'

 L. 242       344  LOAD_GLOBAL              um
              346  LOAD_ATTR                multiply
              348  LOAD_FAST                'x'
              350  LOAD_GLOBAL              um
              352  LOAD_METHOD              conjugate
              354  LOAD_FAST                'x'
              356  CALL_METHOD_1         1  ''
              358  LOAD_FAST                'x'
              360  LOAD_CONST               ('out',)
              362  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              364  LOAD_ATTR                real
              366  STORE_FAST               'x'
            368_0  COME_FROM           342  '342'
            368_1  COME_FROM           262  '262'

 L. 244       368  LOAD_GLOBAL              umr_sum
              370  LOAD_FAST                'x'
              372  LOAD_FAST                'axis'
              374  LOAD_FAST                'dtype'
              376  LOAD_FAST                'out'
              378  LOAD_FAST                'keepdims'
              380  LOAD_FAST                'where'
              382  LOAD_CONST               ('keepdims', 'where')
              384  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              386  STORE_FAST               'ret'

 L. 247       388  LOAD_GLOBAL              um
              390  LOAD_METHOD              maximum
              392  LOAD_FAST                'rcount'
              394  LOAD_FAST                'ddof'
              396  BINARY_SUBTRACT  
              398  LOAD_CONST               0
              400  CALL_METHOD_2         2  ''
              402  STORE_FAST               'rcount'

 L. 250       404  LOAD_GLOBAL              isinstance
              406  LOAD_FAST                'ret'
              408  LOAD_GLOBAL              mu
              410  LOAD_ATTR                ndarray
              412  CALL_FUNCTION_2       2  ''
          414_416  POP_JUMP_IF_FALSE   440  'to 440'

 L. 251       418  LOAD_GLOBAL              um
              420  LOAD_ATTR                true_divide

 L. 252       422  LOAD_FAST                'ret'
              424  LOAD_FAST                'rcount'
              426  LOAD_FAST                'ret'
              428  LOAD_STR                 'unsafe'
              430  LOAD_CONST               False

 L. 251       432  LOAD_CONST               ('out', 'casting', 'subok')
              434  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              436  STORE_FAST               'ret'
              438  JUMP_FORWARD        478  'to 478'
            440_0  COME_FROM           414  '414'

 L. 253       440  LOAD_GLOBAL              hasattr
              442  LOAD_FAST                'ret'
              444  LOAD_STR                 'dtype'
              446  CALL_FUNCTION_2       2  ''
          448_450  POP_JUMP_IF_FALSE   470  'to 470'

 L. 254       452  LOAD_FAST                'ret'
              454  LOAD_ATTR                dtype
              456  LOAD_METHOD              type
              458  LOAD_FAST                'ret'
              460  LOAD_FAST                'rcount'
              462  BINARY_TRUE_DIVIDE
              464  CALL_METHOD_1         1  ''
              466  STORE_FAST               'ret'
              468  JUMP_FORWARD        478  'to 478'
            470_0  COME_FROM           448  '448'

 L. 256       470  LOAD_FAST                'ret'
              472  LOAD_FAST                'rcount'
              474  BINARY_TRUE_DIVIDE
              476  STORE_FAST               'ret'
            478_0  COME_FROM           468  '468'
            478_1  COME_FROM           438  '438'

 L. 258       478  LOAD_FAST                'ret'
              480  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


def _std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True):
    ret = _var(a, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims,
      where=where)
    if isinstanceretmu.ndarray:
        ret = um.sqrt(ret, out=ret)
    else:
        if hasattrret'dtype':
            ret = ret.dtype.type(um.sqrt(ret))
        else:
            ret = um.sqrt(ret)
    return ret


def _ptp(a, axis=None, out=None, keepdims=False):
    return um.subtract(umr_maximumaaxisNoneoutkeepdims, umr_minimumaaxisNoneNonekeepdims, out)


def _dump--- This code section failed: ---

 L. 282         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'file'
                4  LOAD_STR                 'write'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 283        10  LOAD_GLOBAL              nullcontext
               12  LOAD_FAST                'file'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'ctx'
               18  JUMP_FORWARD         34  'to 34'
             20_0  COME_FROM             8  '8'

 L. 285        20  LOAD_GLOBAL              open
               22  LOAD_GLOBAL              os_fspath
               24  LOAD_FAST                'file'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_STR                 'wb'
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'ctx'
             34_0  COME_FROM            18  '18'

 L. 286        34  LOAD_FAST                'ctx'
               36  SETUP_WITH           70  'to 70'
               38  STORE_FAST               'f'

 L. 287        40  LOAD_GLOBAL              pickle
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