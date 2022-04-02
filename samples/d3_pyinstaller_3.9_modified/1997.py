# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\lib\arraypad.py
"""
The arraypad module contains a group of functions to pad values onto the edges
of an n-dimensional array.

"""
import numpy as np
from numpy.core.overrides import array_function_dispatch
from numpy.lib.index_tricks import ndindex
__all__ = [
 'pad']

def _round_if_needed(arr, dtype):
    """
    Rounds arr inplace if destination dtype is integer.

    Parameters
    ----------
    arr : ndarray
        Input array.
    dtype : dtype
        The dtype of the destination array.
    """
    if np.issubdtype(dtype, np.integer):
        arr.round(out=arr)


def _slice_at_axis(sl, axis):
    """
    Construct tuple of slices to slice an array in the given dimension.

    Parameters
    ----------
    sl : slice
        The slice for the given dimension.
    axis : int
        The axis to which `sl` is applied. All other dimensions are left
        "unsliced".

    Returns
    -------
    sl : tuple of slices
        A tuple with slices matching `shape` in length.

    Examples
    --------
    >>> _slice_at_axis(slice(None, 3, -1), 1)
    (slice(None, None, None), slice(None, 3, -1), (...,))
    """
    return (
     slice(None),) * axis + (sl,) + (Ellipsis, )


def _view_roi(array, original_area_slice, axis):
    """
    Get a view of the current region of interest during iterative padding.

    When padding multiple dimensions iteratively corner values are
    unnecessarily overwritten multiple times. This function reduces the
    working area for the first dimensions so that corners are excluded.

    Parameters
    ----------
    array : ndarray
        The array with the region of interest.
    original_area_slice : tuple of slices
        Denotes the area with original values of the unpadded array.
    axis : int
        The currently padded dimension assuming that `axis` is padded before
        `axis` + 1.

    Returns
    -------
    roi : ndarray
        The region of interest of the original `array`.
    """
    axis += 1
    sl = (slice(None),) * axis + original_area_slice[axis:]
    return array[sl]


def _pad_simple--- This code section failed: ---

 L. 109         0  LOAD_GLOBAL              tuple
                2  LOAD_GENEXPR             '<code_object <genexpr>>'
                4  LOAD_STR                 '_pad_simple.<locals>.<genexpr>'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 111         8  LOAD_GLOBAL              zip
               10  LOAD_FAST                'array'
               12  LOAD_ATTR                shape
               14  LOAD_FAST                'pad_width'
               16  CALL_FUNCTION_2       2  ''

 L. 109        18  GET_ITER         
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'new_shape'

 L. 113        26  LOAD_FAST                'array'
               28  LOAD_ATTR                flags
               30  LOAD_ATTR                fnc
               32  POP_JUMP_IF_FALSE    38  'to 38'
               34  LOAD_STR                 'F'
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            32  '32'
               38  LOAD_STR                 'C'
             40_0  COME_FROM            36  '36'
               40  STORE_FAST               'order'

 L. 114        42  LOAD_GLOBAL              np
               44  LOAD_ATTR                empty
               46  LOAD_FAST                'new_shape'
               48  LOAD_FAST                'array'
               50  LOAD_ATTR                dtype
               52  LOAD_FAST                'order'
               54  LOAD_CONST               ('dtype', 'order')
               56  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               58  STORE_FAST               'padded'

 L. 116        60  LOAD_FAST                'fill_value'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE    78  'to 78'

 L. 117        68  LOAD_FAST                'padded'
               70  LOAD_METHOD              fill
               72  LOAD_FAST                'fill_value'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
             78_0  COME_FROM            66  '66'

 L. 120        78  LOAD_GLOBAL              tuple
               80  LOAD_GENEXPR             '<code_object <genexpr>>'
               82  LOAD_STR                 '_pad_simple.<locals>.<genexpr>'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 122        86  LOAD_GLOBAL              zip
               88  LOAD_FAST                'array'
               90  LOAD_ATTR                shape
               92  LOAD_FAST                'pad_width'
               94  CALL_FUNCTION_2       2  ''

 L. 120        96  GET_ITER         
               98  CALL_FUNCTION_1       1  ''
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'original_area_slice'

 L. 124       104  LOAD_FAST                'array'
              106  LOAD_FAST                'padded'
              108  LOAD_FAST                'original_area_slice'
              110  STORE_SUBSCR     

 L. 126       112  LOAD_FAST                'padded'
              114  LOAD_FAST                'original_area_slice'
              116  BUILD_TUPLE_2         2 
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 64


def _set_pad_area(padded, axis, width_pair, value_pair):
    """
    Set empty-padded area in given dimension.

    Parameters
    ----------
    padded : ndarray
        Array with the pad area which is modified inplace.
    axis : int
        Dimension with the pad area to set.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    value_pair : tuple of scalars or ndarrays
        Values inserted into the pad area on each side. It must match or be
        broadcastable to the shape of `arr`.
    """
    left_slice = _slice_at_axissliceNonewidth_pair[0]axis
    padded[left_slice] = value_pair[0]
    right_slice = _slice_at_axisslice(padded.shape[axis] - width_pair[1])Noneaxis
    padded[right_slice] = value_pair[1]


def _get_edges(padded, axis, width_pair):
    """
    Retrieve edge values from empty-padded array in given dimension.

    Parameters
    ----------
    padded : ndarray
        Empty-padded array.
    axis : int
        Dimension in which the edges are considered.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.

    Returns
    -------
    left_edge, right_edge : ndarray
        Edge values of the valid area in `padded` in the given dimension. Its
        shape will always match `padded` except for the dimension given by
        `axis` which will have a length of 1.
    """
    left_index = width_pair[0]
    left_slice = _slice_at_axissliceleft_index(left_index + 1)axis
    left_edge = padded[left_slice]
    right_index = padded.shape[axis] - width_pair[1]
    right_slice = _slice_at_axisslice(right_index - 1)right_indexaxis
    right_edge = padded[right_slice]
    return (
     left_edge, right_edge)


def _get_linear_ramps(padded, axis, width_pair, end_value_pair):
    """
    Construct linear ramps for empty-padded array in given dimension.

    Parameters
    ----------
    padded : ndarray
        Empty-padded array.
    axis : int
        Dimension in which the ramps are constructed.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    end_value_pair : (scalar, scalar)
        End values for the linear ramps which form the edge of the fully padded
        array. These values are included in the linear ramps.

    Returns
    -------
    left_ramp, right_ramp : ndarray
        Linear ramps to set on both sides of `padded`.
    """
    edge_pair = _get_edges(padded, axis, width_pair)
    left_ramp = np.linspace(start=(end_value_pair[0]),
      stop=(edge_pair[0].squeezeaxis),
      num=(width_pair[0]),
      endpoint=False,
      dtype=(padded.dtype),
      axis=axis)
    right_ramp = np.linspace(start=(end_value_pair[1]),
      stop=(edge_pair[1].squeezeaxis),
      num=(width_pair[1]),
      endpoint=False,
      dtype=(padded.dtype),
      axis=axis)
    right_ramp = right_ramp[_slice_at_axisslice(None, None, -1)axis]
    return (
     left_ramp, right_ramp)


def _get_stats--- This code section failed: ---

 L. 260         0  LOAD_FAST                'width_pair'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'left_index'

 L. 261         8  LOAD_FAST                'padded'
               10  LOAD_ATTR                shape
               12  LOAD_FAST                'axis'
               14  BINARY_SUBSCR    
               16  LOAD_FAST                'width_pair'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  BINARY_SUBTRACT  
               24  STORE_FAST               'right_index'

 L. 263        26  LOAD_FAST                'right_index'
               28  LOAD_FAST                'left_index'
               30  BINARY_SUBTRACT  
               32  STORE_FAST               'max_length'

 L. 266        34  LOAD_FAST                'length_pair'
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'left_length'
               40  STORE_FAST               'right_length'

 L. 267        42  LOAD_FAST                'left_length'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_TRUE     58  'to 58'
               50  LOAD_FAST                'max_length'
               52  LOAD_FAST                'left_length'
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    62  'to 62'
             58_0  COME_FROM            48  '48'

 L. 268        58  LOAD_FAST                'max_length'
               60  STORE_FAST               'left_length'
             62_0  COME_FROM            56  '56'

 L. 269        62  LOAD_FAST                'right_length'
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_TRUE     78  'to 78'
               70  LOAD_FAST                'max_length'
               72  LOAD_FAST                'right_length'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    82  'to 82'
             78_0  COME_FROM            68  '68'

 L. 270        78  LOAD_FAST                'max_length'
               80  STORE_FAST               'right_length'
             82_0  COME_FROM            76  '76'

 L. 272        82  LOAD_FAST                'left_length'
               84  LOAD_CONST               0
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE     98  'to 98'
               90  LOAD_FAST                'right_length'
               92  LOAD_CONST               0
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   122  'to 122'
             98_0  COME_FROM            88  '88'

 L. 273        98  LOAD_FAST                'stat_func'
              100  LOAD_GLOBAL              np
              102  LOAD_ATTR                amax
              104  LOAD_GLOBAL              np
              106  LOAD_ATTR                amin
              108  BUILD_SET_2           2 
              110  <118>                 0  ''

 L. 272       112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 276       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'stat_length of 0 yields no value for padding'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM            96  '96'

 L. 279       122  LOAD_GLOBAL              _slice_at_axis

 L. 280       124  LOAD_GLOBAL              slice
              126  LOAD_FAST                'left_index'
              128  LOAD_FAST                'left_index'
              130  LOAD_FAST                'left_length'
              132  BINARY_ADD       
              134  CALL_FUNCTION_2       2  ''
              136  LOAD_FAST                'axis'

 L. 279       138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'left_slice'

 L. 281       142  LOAD_FAST                'padded'
              144  LOAD_FAST                'left_slice'
              146  BINARY_SUBSCR    
              148  STORE_FAST               'left_chunk'

 L. 282       150  LOAD_FAST                'stat_func'
              152  LOAD_FAST                'left_chunk'
              154  LOAD_FAST                'axis'
              156  LOAD_CONST               True
              158  LOAD_CONST               ('axis', 'keepdims')
              160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              162  STORE_FAST               'left_stat'

 L. 283       164  LOAD_GLOBAL              _round_if_needed
              166  LOAD_FAST                'left_stat'
              168  LOAD_FAST                'padded'
              170  LOAD_ATTR                dtype
              172  CALL_FUNCTION_2       2  ''
              174  POP_TOP          

 L. 285       176  LOAD_FAST                'left_length'
              178  LOAD_FAST                'right_length'
              180  DUP_TOP          
              182  ROT_THREE        
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   196  'to 196'
              188  LOAD_FAST                'max_length'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   208  'to 208'
              194  JUMP_FORWARD        200  'to 200'
            196_0  COME_FROM           186  '186'
              196  POP_TOP          
              198  JUMP_FORWARD        208  'to 208'
            200_0  COME_FROM           194  '194'

 L. 287       200  LOAD_FAST                'left_stat'
              202  LOAD_FAST                'left_stat'
              204  BUILD_TUPLE_2         2 
              206  RETURN_VALUE     
            208_0  COME_FROM           198  '198'
            208_1  COME_FROM           192  '192'

 L. 290       208  LOAD_GLOBAL              _slice_at_axis

 L. 291       210  LOAD_GLOBAL              slice
              212  LOAD_FAST                'right_index'
              214  LOAD_FAST                'right_length'
              216  BINARY_SUBTRACT  
              218  LOAD_FAST                'right_index'
              220  CALL_FUNCTION_2       2  ''
              222  LOAD_FAST                'axis'

 L. 290       224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'right_slice'

 L. 292       228  LOAD_FAST                'padded'
              230  LOAD_FAST                'right_slice'
              232  BINARY_SUBSCR    
              234  STORE_FAST               'right_chunk'

 L. 293       236  LOAD_FAST                'stat_func'
              238  LOAD_FAST                'right_chunk'
              240  LOAD_FAST                'axis'
              242  LOAD_CONST               True
              244  LOAD_CONST               ('axis', 'keepdims')
              246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              248  STORE_FAST               'right_stat'

 L. 294       250  LOAD_GLOBAL              _round_if_needed
              252  LOAD_FAST                'right_stat'
              254  LOAD_FAST                'padded'
              256  LOAD_ATTR                dtype
              258  CALL_FUNCTION_2       2  ''
              260  POP_TOP          

 L. 296       262  LOAD_FAST                'left_stat'
              264  LOAD_FAST                'right_stat'
              266  BUILD_TUPLE_2         2 
              268  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46


def _set_reflect_both(padded, axis, width_pair, method, include_edge=False):
    """
    Pad `axis` of `arr` with reflection.

    Parameters
    ----------
    padded : ndarray
        Input array of arbitrary shape.
    axis : int
        Axis along which to pad `arr`.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    method : str
        Controls method of reflection; options are 'even' or 'odd'.
    include_edge : bool
        If true, edge value is included in reflection, otherwise the edge
        value forms the symmetric axis to the reflection.

    Returns
    -------
    pad_amt : tuple of ints, length 2
        New index positions of padding to do along the `axis`. If these are
        both 0, padding is done in this dimension.
    """
    left_pad, right_pad = width_pair
    old_length = padded.shape[axis] - right_pad - left_pad
    if include_edge:
        edge_offset = 1
    else:
        edge_offset = 0
        old_length -= 1
    if left_pad > 0:
        chunk_length = minold_lengthleft_pad
        stop = left_pad - edge_offset
        start = stop + chunk_length
        left_slice = _slice_at_axisslice(start, stop, -1)axis
        left_chunk = padded[left_slice]
        if method == 'odd':
            edge_slice = _slice_at_axissliceleft_pad(left_pad + 1)axis
            left_chunk = 2 * padded[edge_slice] - left_chunk
        start = left_pad - chunk_length
        stop = left_pad
        pad_area = _slice_at_axisslicestartstopaxis
        padded[pad_area] = left_chunk
        left_pad -= chunk_length
    if right_pad > 0:
        chunk_length = minold_lengthright_pad
        start = -right_pad + edge_offset - 2
        stop = start - chunk_length
        right_slice = _slice_at_axisslice(start, stop, -1)axis
        right_chunk = padded[right_slice]
        if method == 'odd':
            edge_slice = _slice_at_axisslice(-right_pad - 1)(-right_pad)axis
            right_chunk = 2 * padded[edge_slice] - right_chunk
        start = padded.shape[axis] - right_pad
        stop = start + chunk_length
        pad_area = _slice_at_axisslicestartstopaxis
        padded[pad_area] = right_chunk
        right_pad -= chunk_length
    return (
     left_pad, right_pad)


def _set_wrap_both(padded, axis, width_pair):
    """
    Pad `axis` of `arr` with wrapped values.

    Parameters
    ----------
    padded : ndarray
        Input array of arbitrary shape.
    axis : int
        Axis along which to pad `arr`.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.

    Returns
    -------
    pad_amt : tuple of ints, length 2
        New index positions of padding to do along the `axis`. If these are
        both 0, padding is done in this dimension.
    """
    left_pad, right_pad = width_pair
    period = padded.shape[axis] - right_pad - left_pad
    new_left_pad = 0
    new_right_pad = 0
    if left_pad > 0:
        right_slice = _slice_at_axisslice(-right_pad - minperiodleft_pad)(-right_pad if right_pad != 0 else None)axis
        right_chunk = padded[right_slice]
        if left_pad > period:
            pad_area = _slice_at_axisslice(left_pad - period)left_padaxis
            new_left_pad = left_pad - period
        else:
            pad_area = _slice_at_axissliceNoneleft_padaxis
        padded[pad_area] = right_chunk
    if right_pad > 0:
        left_slice = _slice_at_axissliceleft_pad(left_pad + minperiodright_pad)axis
        left_chunk = padded[left_slice]
        if right_pad > period:
            pad_area = _slice_at_axisslice(-right_pad)(-right_pad + period)axis
            new_right_pad = right_pad - period
        else:
            pad_area = _slice_at_axisslice(-right_pad)Noneaxis
        padded[pad_area] = left_chunk
    return (
     new_left_pad, new_right_pad)


def _as_pairs--- This code section failed: ---

 L. 485         0  LOAD_FAST                'x'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 488         8  LOAD_CONST               ((None, None),)
               10  LOAD_FAST                'ndim'
               12  BINARY_MULTIPLY  
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 490        16  LOAD_GLOBAL              np
               18  LOAD_METHOD              array
               20  LOAD_FAST                'x'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'x'

 L. 491        26  LOAD_FAST                'as_index'
               28  POP_JUMP_IF_FALSE    52  'to 52'

 L. 492        30  LOAD_GLOBAL              np
               32  LOAD_METHOD              round
               34  LOAD_FAST                'x'
               36  CALL_METHOD_1         1  ''
               38  LOAD_ATTR                astype
               40  LOAD_GLOBAL              np
               42  LOAD_ATTR                intp
               44  LOAD_CONST               False
               46  LOAD_CONST               ('copy',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  STORE_FAST               'x'
             52_0  COME_FROM            28  '28'

 L. 494        52  LOAD_FAST                'x'
               54  LOAD_ATTR                ndim
               56  LOAD_CONST               3
               58  COMPARE_OP               <
               60  POP_JUMP_IF_FALSE   208  'to 208'

 L. 499        62  LOAD_FAST                'x'
               64  LOAD_ATTR                size
               66  LOAD_CONST               1
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   122  'to 122'

 L. 501        72  LOAD_FAST                'x'
               74  LOAD_METHOD              ravel
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'x'

 L. 502        80  LOAD_FAST                'as_index'
               82  POP_JUMP_IF_FALSE   100  'to 100'
               84  LOAD_FAST                'x'
               86  LOAD_CONST               0
               88  COMPARE_OP               <
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 503        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 "index can't contain negative values"
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            82  '82'

 L. 504       100  LOAD_FAST                'x'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'x'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  BUILD_TUPLE_2         2 
              114  BUILD_TUPLE_1         1 
              116  LOAD_FAST                'ndim'
              118  BINARY_MULTIPLY  
              120  RETURN_VALUE     
            122_0  COME_FROM            70  '70'

 L. 506       122  LOAD_FAST                'x'
              124  LOAD_ATTR                size
              126  LOAD_CONST               2
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   208  'to 208'
              132  LOAD_FAST                'x'
              134  LOAD_ATTR                shape
              136  LOAD_CONST               (2, 1)
              138  COMPARE_OP               !=
              140  POP_JUMP_IF_FALSE   208  'to 208'

 L. 511       142  LOAD_FAST                'x'
              144  LOAD_METHOD              ravel
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'x'

 L. 512       150  LOAD_FAST                'as_index'
              152  POP_JUMP_IF_FALSE   186  'to 186'
              154  LOAD_FAST                'x'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  LOAD_CONST               0
              162  COMPARE_OP               <
              164  POP_JUMP_IF_TRUE    178  'to 178'
              166  LOAD_FAST                'x'
              168  LOAD_CONST               1
              170  BINARY_SUBSCR    
              172  LOAD_CONST               0
              174  COMPARE_OP               <
              176  POP_JUMP_IF_FALSE   186  'to 186'
            178_0  COME_FROM           164  '164'

 L. 513       178  LOAD_GLOBAL              ValueError
              180  LOAD_STR                 "index can't contain negative values"
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           152  '152'

 L. 514       186  LOAD_FAST                'x'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_FAST                'x'
              194  LOAD_CONST               1
              196  BINARY_SUBSCR    
              198  BUILD_TUPLE_2         2 
              200  BUILD_TUPLE_1         1 
              202  LOAD_FAST                'ndim'
              204  BINARY_MULTIPLY  
              206  RETURN_VALUE     
            208_0  COME_FROM           140  '140'
            208_1  COME_FROM           130  '130'
            208_2  COME_FROM            60  '60'

 L. 516       208  LOAD_FAST                'as_index'
              210  POP_JUMP_IF_FALSE   232  'to 232'
              212  LOAD_FAST                'x'
              214  LOAD_METHOD              min
              216  CALL_METHOD_0         0  ''
              218  LOAD_CONST               0
              220  COMPARE_OP               <
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L. 517       224  LOAD_GLOBAL              ValueError
              226  LOAD_STR                 "index can't contain negative values"
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           210  '210'

 L. 521       232  LOAD_GLOBAL              np
              234  LOAD_METHOD              broadcast_to
              236  LOAD_FAST                'x'
              238  LOAD_FAST                'ndim'
              240  LOAD_CONST               2
              242  BUILD_TUPLE_2         2 
              244  CALL_METHOD_2         2  ''
              246  LOAD_METHOD              tolist
              248  CALL_METHOD_0         0  ''
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _pad_dispatcher(array, pad_width, mode=None, **kwargs):
    return (
     array,)


@array_function_dispatch(_pad_dispatcher, module='numpy')
def pad--- This code section failed: ---

 L. 739         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              asarray
                4  LOAD_FAST                'array'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'array'

 L. 740        10  LOAD_GLOBAL              np
               12  LOAD_METHOD              asarray
               14  LOAD_FAST                'pad_width'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'pad_width'

 L. 742        20  LOAD_FAST                'pad_width'
               22  LOAD_ATTR                dtype
               24  LOAD_ATTR                kind
               26  LOAD_STR                 'i'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 743        32  LOAD_GLOBAL              TypeError
               34  LOAD_STR                 '`pad_width` must be of integral type.'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L. 746        40  LOAD_GLOBAL              _as_pairs
               42  LOAD_FAST                'pad_width'
               44  LOAD_FAST                'array'
               46  LOAD_ATTR                ndim
               48  LOAD_CONST               True
               50  LOAD_CONST               ('as_index',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'pad_width'

 L. 748        56  LOAD_GLOBAL              callable
               58  LOAD_FAST                'mode'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_FALSE   184  'to 184'

 L. 750        64  LOAD_FAST                'mode'
               66  STORE_FAST               'function'

 L. 752        68  LOAD_GLOBAL              _pad_simple
               70  LOAD_FAST                'array'
               72  LOAD_FAST                'pad_width'
               74  LOAD_CONST               0
               76  LOAD_CONST               ('fill_value',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'padded'
               84  STORE_FAST               '_'

 L. 755        86  LOAD_GLOBAL              range
               88  LOAD_FAST                'padded'
               90  LOAD_ATTR                ndim
               92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
             96_0  COME_FROM           178  '178'
               96  FOR_ITER            180  'to 180'
               98  STORE_FAST               'axis'

 L. 760       100  LOAD_GLOBAL              np
              102  LOAD_METHOD              moveaxis
              104  LOAD_FAST                'padded'
              106  LOAD_FAST                'axis'
              108  LOAD_CONST               -1
              110  CALL_METHOD_3         3  ''
              112  STORE_FAST               'view'

 L. 764       114  LOAD_GLOBAL              ndindex
              116  LOAD_FAST                'view'
              118  LOAD_ATTR                shape
              120  LOAD_CONST               None
              122  LOAD_CONST               -1
              124  BUILD_SLICE_2         2 
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'inds'

 L. 765       132  LOAD_GENEXPR             '<code_object <genexpr>>'
              134  LOAD_STR                 'pad.<locals>.<genexpr>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              138  LOAD_FAST                'inds'
              140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'inds'

 L. 766       146  LOAD_FAST                'inds'
              148  GET_ITER         
            150_0  COME_FROM           176  '176'
              150  FOR_ITER            178  'to 178'
              152  STORE_FAST               'ind'

 L. 767       154  LOAD_FAST                'function'
              156  LOAD_FAST                'view'
              158  LOAD_FAST                'ind'
              160  BINARY_SUBSCR    
              162  LOAD_FAST                'pad_width'
              164  LOAD_FAST                'axis'
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'axis'
              170  LOAD_FAST                'kwargs'
              172  CALL_FUNCTION_4       4  ''
              174  POP_TOP          
              176  JUMP_BACK           150  'to 150'
            178_0  COME_FROM           150  '150'
              178  JUMP_BACK            96  'to 96'
            180_0  COME_FROM            96  '96'

 L. 769       180  LOAD_FAST                'padded'
              182  RETURN_VALUE     
            184_0  COME_FROM            62  '62'

 L. 773       184  BUILD_LIST_0          0 
              186  BUILD_LIST_0          0 
              188  BUILD_LIST_0          0 

 L. 774       190  LOAD_STR                 'constant_values'
              192  BUILD_LIST_1          1 

 L. 775       194  LOAD_STR                 'end_values'
              196  BUILD_LIST_1          1 

 L. 776       198  LOAD_STR                 'stat_length'
              200  BUILD_LIST_1          1 

 L. 777       202  LOAD_STR                 'stat_length'
              204  BUILD_LIST_1          1 

 L. 778       206  LOAD_STR                 'stat_length'
              208  BUILD_LIST_1          1 

 L. 779       210  LOAD_STR                 'stat_length'
              212  BUILD_LIST_1          1 

 L. 780       214  LOAD_STR                 'reflect_type'
              216  BUILD_LIST_1          1 

 L. 781       218  LOAD_STR                 'reflect_type'
              220  BUILD_LIST_1          1 

 L. 772       222  LOAD_CONST               ('empty', 'edge', 'wrap', 'constant', 'linear_ramp', 'maximum', 'mean', 'median', 'minimum', 'reflect', 'symmetric')
              224  BUILD_CONST_KEY_MAP_11    11 
              226  STORE_FAST               'allowed_kwargs'

 L. 783       228  SETUP_FINALLY       254  'to 254'

 L. 784       230  LOAD_GLOBAL              set
              232  LOAD_FAST                'kwargs'
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_GLOBAL              set
              238  LOAD_FAST                'allowed_kwargs'
              240  LOAD_FAST                'mode'
              242  BINARY_SUBSCR    
              244  CALL_FUNCTION_1       1  ''
              246  BINARY_SUBTRACT  
              248  STORE_FAST               'unsupported_kwargs'
              250  POP_BLOCK        
              252  JUMP_FORWARD        288  'to 288'
            254_0  COME_FROM_FINALLY   228  '228'

 L. 785       254  DUP_TOP          
              256  LOAD_GLOBAL              KeyError
          258_260  <121>               286  ''
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 786       268  LOAD_GLOBAL              ValueError
              270  LOAD_STR                 "mode '{}' is not supported"
              272  LOAD_METHOD              format
              274  LOAD_FAST                'mode'
              276  CALL_METHOD_1         1  ''
              278  CALL_FUNCTION_1       1  ''
              280  RAISE_VARARGS_1       1  'exception instance'
              282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
              286  <48>             
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           252  '252'

 L. 787       288  LOAD_FAST                'unsupported_kwargs'
          290_292  POP_JUMP_IF_FALSE   310  'to 310'

 L. 788       294  LOAD_GLOBAL              ValueError
              296  LOAD_STR                 "unsupported keyword arguments for mode '{}': {}"
              298  LOAD_METHOD              format

 L. 789       300  LOAD_FAST                'mode'
              302  LOAD_FAST                'unsupported_kwargs'

 L. 788       304  CALL_METHOD_2         2  ''
              306  CALL_FUNCTION_1       1  ''
              308  RAISE_VARARGS_1       1  'exception instance'
            310_0  COME_FROM           290  '290'

 L. 791       310  LOAD_GLOBAL              np
              312  LOAD_ATTR                amax
              314  LOAD_GLOBAL              np
              316  LOAD_ATTR                amin

 L. 792       318  LOAD_GLOBAL              np
              320  LOAD_ATTR                mean
              322  LOAD_GLOBAL              np
              324  LOAD_ATTR                median

 L. 791       326  LOAD_CONST               ('maximum', 'minimum', 'mean', 'median')
              328  BUILD_CONST_KEY_MAP_4     4 
              330  STORE_FAST               'stat_functions'

 L. 796       332  LOAD_GLOBAL              _pad_simple
              334  LOAD_FAST                'array'
              336  LOAD_FAST                'pad_width'
              338  CALL_FUNCTION_2       2  ''
              340  UNPACK_SEQUENCE_2     2 
              342  STORE_FAST               'padded'
              344  STORE_FAST               'original_area_slice'

 L. 799       346  LOAD_GLOBAL              range
              348  LOAD_FAST                'padded'
              350  LOAD_ATTR                ndim
              352  CALL_FUNCTION_1       1  ''
              354  STORE_FAST               'axes'

 L. 801       356  LOAD_FAST                'mode'
              358  LOAD_STR                 'constant'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   446  'to 446'

 L. 802       366  LOAD_FAST                'kwargs'
              368  LOAD_METHOD              get
              370  LOAD_STR                 'constant_values'
              372  LOAD_CONST               0
              374  CALL_METHOD_2         2  ''
              376  STORE_FAST               'values'

 L. 803       378  LOAD_GLOBAL              _as_pairs
              380  LOAD_FAST                'values'
              382  LOAD_FAST                'padded'
              384  LOAD_ATTR                ndim
              386  CALL_FUNCTION_2       2  ''
              388  STORE_FAST               'values'

 L. 804       390  LOAD_GLOBAL              zip
              392  LOAD_FAST                'axes'
              394  LOAD_FAST                'pad_width'
              396  LOAD_FAST                'values'
              398  CALL_FUNCTION_3       3  ''
              400  GET_ITER         
            402_0  COME_FROM           438  '438'
              402  FOR_ITER            442  'to 442'
              404  UNPACK_SEQUENCE_3     3 
              406  STORE_FAST               'axis'
              408  STORE_FAST               'width_pair'
              410  STORE_FAST               'value_pair'

 L. 805       412  LOAD_GLOBAL              _view_roi
              414  LOAD_FAST                'padded'
              416  LOAD_FAST                'original_area_slice'
              418  LOAD_FAST                'axis'
              420  CALL_FUNCTION_3       3  ''
              422  STORE_FAST               'roi'

 L. 806       424  LOAD_GLOBAL              _set_pad_area
              426  LOAD_FAST                'roi'
              428  LOAD_FAST                'axis'
              430  LOAD_FAST                'width_pair'
              432  LOAD_FAST                'value_pair'
              434  CALL_FUNCTION_4       4  ''
              436  POP_TOP          
          438_440  JUMP_BACK           402  'to 402'
            442_0  COME_FROM           402  '402'
          442_444  JUMP_FORWARD       1128  'to 1128'
            446_0  COME_FROM           362  '362'

 L. 808       446  LOAD_FAST                'mode'
              448  LOAD_STR                 'empty'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   460  'to 460'

 L. 809   456_458  JUMP_FORWARD       1128  'to 1128'
            460_0  COME_FROM           452  '452'

 L. 811       460  LOAD_FAST                'array'
              462  LOAD_ATTR                size
              464  LOAD_CONST               0
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   538  'to 538'

 L. 815       472  LOAD_GLOBAL              zip
              474  LOAD_FAST                'axes'
              476  LOAD_FAST                'pad_width'
              478  CALL_FUNCTION_2       2  ''
              480  GET_ITER         
            482_0  COME_FROM           530  '530'
            482_1  COME_FROM           512  '512'
            482_2  COME_FROM           502  '502'
              482  FOR_ITER            534  'to 534'
              484  UNPACK_SEQUENCE_2     2 
              486  STORE_FAST               'axis'
              488  STORE_FAST               'width_pair'

 L. 816       490  LOAD_FAST                'array'
              492  LOAD_ATTR                shape
              494  LOAD_FAST                'axis'
              496  BINARY_SUBSCR    
              498  LOAD_CONST               0
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE_BACK   482  'to 482'
              506  LOAD_GLOBAL              any
              508  LOAD_FAST                'width_pair'
              510  CALL_FUNCTION_1       1  ''
          512_514  POP_JUMP_IF_FALSE_BACK   482  'to 482'

 L. 817       516  LOAD_GLOBAL              ValueError

 L. 818       518  LOAD_STR                 "can't extend empty axis {} using modes other than 'constant' or 'empty'"
              520  LOAD_METHOD              format

 L. 819       522  LOAD_FAST                'axis'

 L. 818       524  CALL_METHOD_1         1  ''

 L. 817       526  CALL_FUNCTION_1       1  ''
              528  RAISE_VARARGS_1       1  'exception instance'
          530_532  JUMP_BACK           482  'to 482'
            534_0  COME_FROM           482  '482'
          534_536  JUMP_FORWARD       1128  'to 1128'
            538_0  COME_FROM           468  '468'

 L. 824       538  LOAD_FAST                'mode'
              540  LOAD_STR                 'edge'
              542  COMPARE_OP               ==
          544_546  POP_JUMP_IF_FALSE   612  'to 612'

 L. 825       548  LOAD_GLOBAL              zip
              550  LOAD_FAST                'axes'
              552  LOAD_FAST                'pad_width'
              554  CALL_FUNCTION_2       2  ''
              556  GET_ITER         
            558_0  COME_FROM           604  '604'
              558  FOR_ITER            608  'to 608'
              560  UNPACK_SEQUENCE_2     2 
              562  STORE_FAST               'axis'
              564  STORE_FAST               'width_pair'

 L. 826       566  LOAD_GLOBAL              _view_roi
              568  LOAD_FAST                'padded'
              570  LOAD_FAST                'original_area_slice'
              572  LOAD_FAST                'axis'
              574  CALL_FUNCTION_3       3  ''
              576  STORE_FAST               'roi'

 L. 827       578  LOAD_GLOBAL              _get_edges
              580  LOAD_FAST                'roi'
              582  LOAD_FAST                'axis'
              584  LOAD_FAST                'width_pair'
              586  CALL_FUNCTION_3       3  ''
              588  STORE_FAST               'edge_pair'

 L. 828       590  LOAD_GLOBAL              _set_pad_area
              592  LOAD_FAST                'roi'
              594  LOAD_FAST                'axis'
              596  LOAD_FAST                'width_pair'
              598  LOAD_FAST                'edge_pair'
              600  CALL_FUNCTION_4       4  ''
              602  POP_TOP          
          604_606  JUMP_BACK           558  'to 558'
            608_0  COME_FROM           558  '558'
          608_610  JUMP_FORWARD       1128  'to 1128'
            612_0  COME_FROM           544  '544'

 L. 830       612  LOAD_FAST                'mode'
              614  LOAD_STR                 'linear_ramp'
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   716  'to 716'

 L. 831       622  LOAD_FAST                'kwargs'
              624  LOAD_METHOD              get
              626  LOAD_STR                 'end_values'
              628  LOAD_CONST               0
              630  CALL_METHOD_2         2  ''
              632  STORE_FAST               'end_values'

 L. 832       634  LOAD_GLOBAL              _as_pairs
              636  LOAD_FAST                'end_values'
              638  LOAD_FAST                'padded'
              640  LOAD_ATTR                ndim
              642  CALL_FUNCTION_2       2  ''
              644  STORE_FAST               'end_values'

 L. 833       646  LOAD_GLOBAL              zip
              648  LOAD_FAST                'axes'
              650  LOAD_FAST                'pad_width'
              652  LOAD_FAST                'end_values'
              654  CALL_FUNCTION_3       3  ''
              656  GET_ITER         
            658_0  COME_FROM           708  '708'
              658  FOR_ITER            712  'to 712'
              660  UNPACK_SEQUENCE_3     3 
              662  STORE_FAST               'axis'
              664  STORE_FAST               'width_pair'
              666  STORE_FAST               'value_pair'

 L. 834       668  LOAD_GLOBAL              _view_roi
              670  LOAD_FAST                'padded'
              672  LOAD_FAST                'original_area_slice'
              674  LOAD_FAST                'axis'
              676  CALL_FUNCTION_3       3  ''
              678  STORE_FAST               'roi'

 L. 835       680  LOAD_GLOBAL              _get_linear_ramps
              682  LOAD_FAST                'roi'
              684  LOAD_FAST                'axis'
              686  LOAD_FAST                'width_pair'
              688  LOAD_FAST                'value_pair'
              690  CALL_FUNCTION_4       4  ''
              692  STORE_FAST               'ramp_pair'

 L. 836       694  LOAD_GLOBAL              _set_pad_area
              696  LOAD_FAST                'roi'
              698  LOAD_FAST                'axis'
              700  LOAD_FAST                'width_pair'
              702  LOAD_FAST                'ramp_pair'
              704  CALL_FUNCTION_4       4  ''
              706  POP_TOP          
          708_710  JUMP_BACK           658  'to 658'
            712_0  COME_FROM           658  '658'
          712_714  JUMP_FORWARD       1128  'to 1128'
            716_0  COME_FROM           618  '618'

 L. 838       716  LOAD_FAST                'mode'
              718  LOAD_FAST                'stat_functions'
              720  <118>                 0  ''
          722_724  POP_JUMP_IF_FALSE   834  'to 834'

 L. 839       726  LOAD_FAST                'stat_functions'
              728  LOAD_FAST                'mode'
              730  BINARY_SUBSCR    
              732  STORE_FAST               'func'

 L. 840       734  LOAD_FAST                'kwargs'
              736  LOAD_METHOD              get
              738  LOAD_STR                 'stat_length'
              740  LOAD_CONST               None
              742  CALL_METHOD_2         2  ''
              744  STORE_FAST               'length'

 L. 841       746  LOAD_GLOBAL              _as_pairs
              748  LOAD_FAST                'length'
              750  LOAD_FAST                'padded'
              752  LOAD_ATTR                ndim
              754  LOAD_CONST               True
              756  LOAD_CONST               ('as_index',)
              758  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              760  STORE_FAST               'length'

 L. 842       762  LOAD_GLOBAL              zip
              764  LOAD_FAST                'axes'
              766  LOAD_FAST                'pad_width'
              768  LOAD_FAST                'length'
              770  CALL_FUNCTION_3       3  ''
              772  GET_ITER         
            774_0  COME_FROM           826  '826'
              774  FOR_ITER            830  'to 830'
              776  UNPACK_SEQUENCE_3     3 
              778  STORE_FAST               'axis'
              780  STORE_FAST               'width_pair'
              782  STORE_FAST               'length_pair'

 L. 843       784  LOAD_GLOBAL              _view_roi
              786  LOAD_FAST                'padded'
              788  LOAD_FAST                'original_area_slice'
              790  LOAD_FAST                'axis'
              792  CALL_FUNCTION_3       3  ''
              794  STORE_FAST               'roi'

 L. 844       796  LOAD_GLOBAL              _get_stats
              798  LOAD_FAST                'roi'
              800  LOAD_FAST                'axis'
              802  LOAD_FAST                'width_pair'
              804  LOAD_FAST                'length_pair'
              806  LOAD_FAST                'func'
              808  CALL_FUNCTION_5       5  ''
              810  STORE_FAST               'stat_pair'

 L. 845       812  LOAD_GLOBAL              _set_pad_area
              814  LOAD_FAST                'roi'
              816  LOAD_FAST                'axis'
              818  LOAD_FAST                'width_pair'
              820  LOAD_FAST                'stat_pair'
              822  CALL_FUNCTION_4       4  ''
              824  POP_TOP          
          826_828  JUMP_BACK           774  'to 774'
            830_0  COME_FROM           774  '774'
          830_832  JUMP_FORWARD       1128  'to 1128'
            834_0  COME_FROM           722  '722'

 L. 847       834  LOAD_FAST                'mode'
              836  LOAD_CONST               frozenset({'reflect', 'symmetric'})
              838  <118>                 0  ''
          840_842  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 848       844  LOAD_FAST                'kwargs'
              846  LOAD_METHOD              get
              848  LOAD_STR                 'reflect_type'
              850  LOAD_STR                 'even'
              852  CALL_METHOD_2         2  ''
              854  STORE_FAST               'method'

 L. 849       856  LOAD_FAST                'mode'
              858  LOAD_STR                 'symmetric'
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE   870  'to 870'
              866  LOAD_CONST               True
              868  JUMP_FORWARD        872  'to 872'
            870_0  COME_FROM           862  '862'
              870  LOAD_CONST               False
            872_0  COME_FROM           868  '868'
              872  STORE_FAST               'include_edge'

 L. 850       874  LOAD_GLOBAL              zip
              876  LOAD_FAST                'axes'
              878  LOAD_FAST                'pad_width'
              880  CALL_FUNCTION_2       2  ''
              882  GET_ITER         
            884_0  COME_FROM          1030  '1030'
            884_1  COME_FROM           998  '998'
            884_2  COME_FROM           966  '966'
              884  FOR_ITER           1034  'to 1034'
              886  UNPACK_SEQUENCE_2     2 
              888  STORE_FAST               'axis'
              890  UNPACK_SEQUENCE_2     2 
              892  STORE_FAST               'left_index'
              894  STORE_FAST               'right_index'

 L. 851       896  LOAD_FAST                'array'
              898  LOAD_ATTR                shape
              900  LOAD_FAST                'axis'
              902  BINARY_SUBSCR    
              904  LOAD_CONST               1
              906  COMPARE_OP               ==
          908_910  POP_JUMP_IF_FALSE   970  'to 970'
              912  LOAD_FAST                'left_index'
              914  LOAD_CONST               0
              916  COMPARE_OP               >
          918_920  POP_JUMP_IF_TRUE    932  'to 932'
              922  LOAD_FAST                'right_index'
              924  LOAD_CONST               0
              926  COMPARE_OP               >
          928_930  POP_JUMP_IF_FALSE   970  'to 970'
            932_0  COME_FROM           918  '918'

 L. 854       932  LOAD_GLOBAL              _get_edges
              934  LOAD_FAST                'padded'
              936  LOAD_FAST                'axis'
              938  LOAD_FAST                'left_index'
              940  LOAD_FAST                'right_index'
              942  BUILD_TUPLE_2         2 
              944  CALL_FUNCTION_3       3  ''
              946  STORE_FAST               'edge_pair'

 L. 855       948  LOAD_GLOBAL              _set_pad_area

 L. 856       950  LOAD_FAST                'padded'
              952  LOAD_FAST                'axis'
              954  LOAD_FAST                'left_index'
              956  LOAD_FAST                'right_index'
              958  BUILD_TUPLE_2         2 
              960  LOAD_FAST                'edge_pair'

 L. 855       962  CALL_FUNCTION_4       4  ''
              964  POP_TOP          

 L. 857   966_968  JUMP_BACK           884  'to 884'
            970_0  COME_FROM           928  '928'
            970_1  COME_FROM           908  '908'

 L. 859       970  LOAD_GLOBAL              _view_roi
              972  LOAD_FAST                'padded'
              974  LOAD_FAST                'original_area_slice'
              976  LOAD_FAST                'axis'
              978  CALL_FUNCTION_3       3  ''
              980  STORE_FAST               'roi'
            982_0  COME_FROM          1026  '1026'

 L. 860       982  LOAD_FAST                'left_index'
              984  LOAD_CONST               0
              986  COMPARE_OP               >
          988_990  POP_JUMP_IF_TRUE   1002  'to 1002'
              992  LOAD_FAST                'right_index'
              994  LOAD_CONST               0
              996  COMPARE_OP               >
         998_1000  POP_JUMP_IF_FALSE_BACK   884  'to 884'
           1002_0  COME_FROM           988  '988'

 L. 864      1002  LOAD_GLOBAL              _set_reflect_both

 L. 865      1004  LOAD_FAST                'roi'
             1006  LOAD_FAST                'axis'
             1008  LOAD_FAST                'left_index'
             1010  LOAD_FAST                'right_index'
             1012  BUILD_TUPLE_2         2 

 L. 866      1014  LOAD_FAST                'method'
             1016  LOAD_FAST                'include_edge'

 L. 864      1018  CALL_FUNCTION_5       5  ''
             1020  UNPACK_SEQUENCE_2     2 
             1022  STORE_FAST               'left_index'
             1024  STORE_FAST               'right_index'
         1026_1028  JUMP_BACK           982  'to 982'
         1030_1032  JUMP_BACK           884  'to 884'
           1034_0  COME_FROM           884  '884'
             1034  JUMP_FORWARD       1128  'to 1128'
           1036_0  COME_FROM           840  '840'

 L. 869      1036  LOAD_FAST                'mode'
             1038  LOAD_STR                 'wrap'
             1040  COMPARE_OP               ==
         1042_1044  POP_JUMP_IF_FALSE  1128  'to 1128'

 L. 870      1046  LOAD_GLOBAL              zip
             1048  LOAD_FAST                'axes'
             1050  LOAD_FAST                'pad_width'
             1052  CALL_FUNCTION_2       2  ''
             1054  GET_ITER         
           1056_0  COME_FROM          1124  '1124'
           1056_1  COME_FROM          1096  '1096'
             1056  FOR_ITER           1128  'to 1128'
             1058  UNPACK_SEQUENCE_2     2 
             1060  STORE_FAST               'axis'
             1062  UNPACK_SEQUENCE_2     2 
             1064  STORE_FAST               'left_index'
             1066  STORE_FAST               'right_index'

 L. 871      1068  LOAD_GLOBAL              _view_roi
             1070  LOAD_FAST                'padded'
             1072  LOAD_FAST                'original_area_slice'
             1074  LOAD_FAST                'axis'
             1076  CALL_FUNCTION_3       3  ''
             1078  STORE_FAST               'roi'
           1080_0  COME_FROM          1120  '1120'

 L. 872      1080  LOAD_FAST                'left_index'
             1082  LOAD_CONST               0
             1084  COMPARE_OP               >
         1086_1088  POP_JUMP_IF_TRUE   1100  'to 1100'
             1090  LOAD_FAST                'right_index'
             1092  LOAD_CONST               0
             1094  COMPARE_OP               >
         1096_1098  POP_JUMP_IF_FALSE_BACK  1056  'to 1056'
           1100_0  COME_FROM          1086  '1086'

 L. 876      1100  LOAD_GLOBAL              _set_wrap_both

 L. 877      1102  LOAD_FAST                'roi'
             1104  LOAD_FAST                'axis'
             1106  LOAD_FAST                'left_index'
             1108  LOAD_FAST                'right_index'
             1110  BUILD_TUPLE_2         2 

 L. 876      1112  CALL_FUNCTION_3       3  ''
             1114  UNPACK_SEQUENCE_2     2 
             1116  STORE_FAST               'left_index'
             1118  STORE_FAST               'right_index'
         1120_1122  JUMP_BACK          1080  'to 1080'
         1124_1126  JUMP_BACK          1056  'to 1056'
           1128_0  COME_FROM          1056  '1056'
           1128_1  COME_FROM          1042  '1042'
           1128_2  COME_FROM          1034  '1034'
           1128_3  COME_FROM           830  '830'
           1128_4  COME_FROM           712  '712'
           1128_5  COME_FROM           608  '608'
           1128_6  COME_FROM           534  '534'
           1128_7  COME_FROM           456  '456'
           1128_8  COME_FROM           442  '442'

 L. 879      1128  LOAD_FAST                'padded'
             1130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 258_260