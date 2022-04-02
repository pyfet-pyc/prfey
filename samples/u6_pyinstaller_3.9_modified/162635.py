# uncompyle6 version 3.7.4
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
    left_ramp, right_ramp = (np.linspace(start=end_value,
      stop=(edge.squeezeaxis),
      num=width,
      endpoint=False,
      dtype=(padded.dtype),
      axis=axis) for end_value, edge, width in zip(end_value_pair, edge_pair, width_pair))
    right_ramp = right_ramp[_slice_at_axisslice(None, None, -1)axis]
    return (
     left_ramp, right_ramp)


def _get_stats--- This code section failed: ---

 L. 257         0  LOAD_FAST                'width_pair'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'left_index'

 L. 258         8  LOAD_FAST                'padded'
               10  LOAD_ATTR                shape
               12  LOAD_FAST                'axis'
               14  BINARY_SUBSCR    
               16  LOAD_FAST                'width_pair'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  BINARY_SUBTRACT  
               24  STORE_FAST               'right_index'

 L. 260        26  LOAD_FAST                'right_index'
               28  LOAD_FAST                'left_index'
               30  BINARY_SUBTRACT  
               32  STORE_FAST               'max_length'

 L. 263        34  LOAD_FAST                'length_pair'
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'left_length'
               40  STORE_FAST               'right_length'

 L. 264        42  LOAD_FAST                'left_length'
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_TRUE     58  'to 58'
               50  LOAD_FAST                'max_length'
               52  LOAD_FAST                'left_length'
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    62  'to 62'
             58_0  COME_FROM            48  '48'

 L. 265        58  LOAD_FAST                'max_length'
               60  STORE_FAST               'left_length'
             62_0  COME_FROM            56  '56'

 L. 266        62  LOAD_FAST                'right_length'
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_TRUE     78  'to 78'
               70  LOAD_FAST                'max_length'
               72  LOAD_FAST                'right_length'
               74  COMPARE_OP               <
               76  POP_JUMP_IF_FALSE    82  'to 82'
             78_0  COME_FROM            68  '68'

 L. 267        78  LOAD_FAST                'max_length'
               80  STORE_FAST               'right_length'
             82_0  COME_FROM            76  '76'

 L. 269        82  LOAD_FAST                'left_length'
               84  LOAD_CONST               0
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE     98  'to 98'
               90  LOAD_FAST                'right_length'
               92  LOAD_CONST               0
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   122  'to 122'
             98_0  COME_FROM            88  '88'

 L. 270        98  LOAD_FAST                'stat_func'
              100  LOAD_GLOBAL              np
              102  LOAD_ATTR                amax
              104  LOAD_GLOBAL              np
              106  LOAD_ATTR                amin
              108  BUILD_SET_2           2 
              110  <118>                 0  ''

 L. 269       112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 273       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'stat_length of 0 yields no value for padding'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'
            122_1  COME_FROM            96  '96'

 L. 276       122  LOAD_GLOBAL              _slice_at_axis

 L. 277       124  LOAD_GLOBAL              slice
              126  LOAD_FAST                'left_index'
              128  LOAD_FAST                'left_index'
              130  LOAD_FAST                'left_length'
              132  BINARY_ADD       
              134  CALL_FUNCTION_2       2  ''
              136  LOAD_FAST                'axis'

 L. 276       138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'left_slice'

 L. 278       142  LOAD_FAST                'padded'
              144  LOAD_FAST                'left_slice'
              146  BINARY_SUBSCR    
              148  STORE_FAST               'left_chunk'

 L. 279       150  LOAD_FAST                'stat_func'
              152  LOAD_FAST                'left_chunk'
              154  LOAD_FAST                'axis'
              156  LOAD_CONST               True
              158  LOAD_CONST               ('axis', 'keepdims')
              160  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              162  STORE_FAST               'left_stat'

 L. 280       164  LOAD_GLOBAL              _round_if_needed
              166  LOAD_FAST                'left_stat'
              168  LOAD_FAST                'padded'
              170  LOAD_ATTR                dtype
              172  CALL_FUNCTION_2       2  ''
              174  POP_TOP          

 L. 282       176  LOAD_FAST                'left_length'
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

 L. 284       200  LOAD_FAST                'left_stat'
              202  LOAD_FAST                'left_stat'
              204  BUILD_TUPLE_2         2 
              206  RETURN_VALUE     
            208_0  COME_FROM           198  '198'
            208_1  COME_FROM           192  '192'

 L. 287       208  LOAD_GLOBAL              _slice_at_axis

 L. 288       210  LOAD_GLOBAL              slice
              212  LOAD_FAST                'right_index'
              214  LOAD_FAST                'right_length'
              216  BINARY_SUBTRACT  
              218  LOAD_FAST                'right_index'
              220  CALL_FUNCTION_2       2  ''
              222  LOAD_FAST                'axis'

 L. 287       224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'right_slice'

 L. 289       228  LOAD_FAST                'padded'
              230  LOAD_FAST                'right_slice'
              232  BINARY_SUBSCR    
              234  STORE_FAST               'right_chunk'

 L. 290       236  LOAD_FAST                'stat_func'
              238  LOAD_FAST                'right_chunk'
              240  LOAD_FAST                'axis'
              242  LOAD_CONST               True
              244  LOAD_CONST               ('axis', 'keepdims')
              246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              248  STORE_FAST               'right_stat'

 L. 291       250  LOAD_GLOBAL              _round_if_needed
              252  LOAD_FAST                'right_stat'
              254  LOAD_FAST                'padded'
              256  LOAD_ATTR                dtype
              258  CALL_FUNCTION_2       2  ''
              260  POP_TOP          

 L. 293       262  LOAD_FAST                'left_stat'
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
    return (left_pad, right_pad)


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
    return (new_left_pad, new_right_pad)


def _as_pairs--- This code section failed: ---

 L. 482         0  LOAD_FAST                'x'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 485         8  LOAD_CONST               ((None, None),)
               10  LOAD_FAST                'ndim'
               12  BINARY_MULTIPLY  
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 487        16  LOAD_GLOBAL              np
               18  LOAD_METHOD              array
               20  LOAD_FAST                'x'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'x'

 L. 488        26  LOAD_FAST                'as_index'
               28  POP_JUMP_IF_FALSE    52  'to 52'

 L. 489        30  LOAD_GLOBAL              np
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

 L. 491        52  LOAD_FAST                'x'
               54  LOAD_ATTR                ndim
               56  LOAD_CONST               3
               58  COMPARE_OP               <
               60  POP_JUMP_IF_FALSE   208  'to 208'

 L. 496        62  LOAD_FAST                'x'
               64  LOAD_ATTR                size
               66  LOAD_CONST               1
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   122  'to 122'

 L. 498        72  LOAD_FAST                'x'
               74  LOAD_METHOD              ravel
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'x'

 L. 499        80  LOAD_FAST                'as_index'
               82  POP_JUMP_IF_FALSE   100  'to 100'
               84  LOAD_FAST                'x'
               86  LOAD_CONST               0
               88  COMPARE_OP               <
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 500        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 "index can't contain negative values"
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM            82  '82'

 L. 501       100  LOAD_FAST                'x'
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

 L. 503       122  LOAD_FAST                'x'
              124  LOAD_ATTR                size
              126  LOAD_CONST               2
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   208  'to 208'
              132  LOAD_FAST                'x'
              134  LOAD_ATTR                shape
              136  LOAD_CONST               (2, 1)
              138  COMPARE_OP               !=
              140  POP_JUMP_IF_FALSE   208  'to 208'

 L. 508       142  LOAD_FAST                'x'
              144  LOAD_METHOD              ravel
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'x'

 L. 509       150  LOAD_FAST                'as_index'
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

 L. 510       178  LOAD_GLOBAL              ValueError
              180  LOAD_STR                 "index can't contain negative values"
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           152  '152'

 L. 511       186  LOAD_FAST                'x'
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

 L. 513       208  LOAD_FAST                'as_index'
              210  POP_JUMP_IF_FALSE   232  'to 232'
              212  LOAD_FAST                'x'
              214  LOAD_METHOD              min
              216  CALL_METHOD_0         0  ''
              218  LOAD_CONST               0
              220  COMPARE_OP               <
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L. 514       224  LOAD_GLOBAL              ValueError
              226  LOAD_STR                 "index can't contain negative values"
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           210  '210'

 L. 518       232  LOAD_GLOBAL              np
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

 L. 736         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              asarray
                4  LOAD_FAST                'array'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'array'

 L. 737        10  LOAD_GLOBAL              np
               12  LOAD_METHOD              asarray
               14  LOAD_FAST                'pad_width'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'pad_width'

 L. 739        20  LOAD_FAST                'pad_width'
               22  LOAD_ATTR                dtype
               24  LOAD_ATTR                kind
               26  LOAD_STR                 'i'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L. 740        32  LOAD_GLOBAL              TypeError
               34  LOAD_STR                 '`pad_width` must be of integral type.'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L. 743        40  LOAD_GLOBAL              _as_pairs
               42  LOAD_FAST                'pad_width'
               44  LOAD_FAST                'array'
               46  LOAD_ATTR                ndim
               48  LOAD_CONST               True
               50  LOAD_CONST               ('as_index',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  STORE_FAST               'pad_width'

 L. 745        56  LOAD_GLOBAL              callable
               58  LOAD_FAST                'mode'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_FALSE   184  'to 184'

 L. 747        64  LOAD_FAST                'mode'
               66  STORE_FAST               'function'

 L. 749        68  LOAD_GLOBAL              _pad_simple
               70  LOAD_FAST                'array'
               72  LOAD_FAST                'pad_width'
               74  LOAD_CONST               0
               76  LOAD_CONST               ('fill_value',)
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'padded'
               84  STORE_FAST               '_'

 L. 752        86  LOAD_GLOBAL              range
               88  LOAD_FAST                'padded'
               90  LOAD_ATTR                ndim
               92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
               96  FOR_ITER            180  'to 180'
               98  STORE_FAST               'axis'

 L. 757       100  LOAD_GLOBAL              np
              102  LOAD_METHOD              moveaxis
              104  LOAD_FAST                'padded'
              106  LOAD_FAST                'axis'
              108  LOAD_CONST               -1
              110  CALL_METHOD_3         3  ''
              112  STORE_FAST               'view'

 L. 761       114  LOAD_GLOBAL              ndindex
              116  LOAD_FAST                'view'
              118  LOAD_ATTR                shape
              120  LOAD_CONST               None
              122  LOAD_CONST               -1
              124  BUILD_SLICE_2         2 
              126  BINARY_SUBSCR    
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'inds'

 L. 762       132  LOAD_GENEXPR             '<code_object <genexpr>>'
              134  LOAD_STR                 'pad.<locals>.<genexpr>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              138  LOAD_FAST                'inds'
              140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'inds'

 L. 763       146  LOAD_FAST                'inds'
              148  GET_ITER         
              150  FOR_ITER            178  'to 178'
              152  STORE_FAST               'ind'

 L. 764       154  LOAD_FAST                'function'
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
              178  JUMP_BACK            96  'to 96'

 L. 766       180  LOAD_FAST                'padded'
              182  RETURN_VALUE     
            184_0  COME_FROM            62  '62'

 L. 770       184  BUILD_LIST_0          0 
              186  BUILD_LIST_0          0 
              188  BUILD_LIST_0          0 

 L. 771       190  LOAD_STR                 'constant_values'
              192  BUILD_LIST_1          1 

 L. 772       194  LOAD_STR                 'end_values'
              196  BUILD_LIST_1          1 

 L. 773       198  LOAD_STR                 'stat_length'
              200  BUILD_LIST_1          1 

 L. 774       202  LOAD_STR                 'stat_length'
              204  BUILD_LIST_1          1 

 L. 775       206  LOAD_STR                 'stat_length'
              208  BUILD_LIST_1          1 

 L. 776       210  LOAD_STR                 'stat_length'
              212  BUILD_LIST_1          1 

 L. 777       214  LOAD_STR                 'reflect_type'
              216  BUILD_LIST_1          1 

 L. 778       218  LOAD_STR                 'reflect_type'
              220  BUILD_LIST_1          1 

 L. 769       222  LOAD_CONST               ('empty', 'edge', 'wrap', 'constant', 'linear_ramp', 'maximum', 'mean', 'median', 'minimum', 'reflect', 'symmetric')
              224  BUILD_CONST_KEY_MAP_11    11 
              226  STORE_FAST               'allowed_kwargs'

 L. 780       228  SETUP_FINALLY       254  'to 254'

 L. 781       230  LOAD_GLOBAL              set
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
              252  JUMP_FORWARD        290  'to 290'
            254_0  COME_FROM_FINALLY   228  '228'

 L. 782       254  DUP_TOP          
              256  LOAD_GLOBAL              KeyError
          258_260  <121>               288  ''
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 783       268  LOAD_GLOBAL              ValueError
              270  LOAD_STR                 "mode '{}' is not supported"
              272  LOAD_METHOD              format
              274  LOAD_FAST                'mode'
              276  CALL_METHOD_1         1  ''
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_CONST               None
              282  RAISE_VARARGS_2       2  'exception instance with __cause__'
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
              288  <48>             
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           252  '252'

 L. 784       290  LOAD_FAST                'unsupported_kwargs'
          292_294  POP_JUMP_IF_FALSE   312  'to 312'

 L. 785       296  LOAD_GLOBAL              ValueError
              298  LOAD_STR                 "unsupported keyword arguments for mode '{}': {}"
              300  LOAD_METHOD              format

 L. 786       302  LOAD_FAST                'mode'
              304  LOAD_FAST                'unsupported_kwargs'

 L. 785       306  CALL_METHOD_2         2  ''
              308  CALL_FUNCTION_1       1  ''
              310  RAISE_VARARGS_1       1  'exception instance'
            312_0  COME_FROM           292  '292'

 L. 788       312  LOAD_GLOBAL              np
              314  LOAD_ATTR                amax
              316  LOAD_GLOBAL              np
              318  LOAD_ATTR                amin

 L. 789       320  LOAD_GLOBAL              np
              322  LOAD_ATTR                mean
              324  LOAD_GLOBAL              np
              326  LOAD_ATTR                median

 L. 788       328  LOAD_CONST               ('maximum', 'minimum', 'mean', 'median')
              330  BUILD_CONST_KEY_MAP_4     4 
              332  STORE_FAST               'stat_functions'

 L. 793       334  LOAD_GLOBAL              _pad_simple
              336  LOAD_FAST                'array'
              338  LOAD_FAST                'pad_width'
              340  CALL_FUNCTION_2       2  ''
              342  UNPACK_SEQUENCE_2     2 
              344  STORE_FAST               'padded'
              346  STORE_FAST               'original_area_slice'

 L. 796       348  LOAD_GLOBAL              range
              350  LOAD_FAST                'padded'
              352  LOAD_ATTR                ndim
              354  CALL_FUNCTION_1       1  ''
              356  STORE_FAST               'axes'

 L. 798       358  LOAD_FAST                'mode'
              360  LOAD_STR                 'constant'
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   448  'to 448'

 L. 799       368  LOAD_FAST                'kwargs'
              370  LOAD_METHOD              get
              372  LOAD_STR                 'constant_values'
              374  LOAD_CONST               0
              376  CALL_METHOD_2         2  ''
              378  STORE_FAST               'values'

 L. 800       380  LOAD_GLOBAL              _as_pairs
              382  LOAD_FAST                'values'
              384  LOAD_FAST                'padded'
              386  LOAD_ATTR                ndim
              388  CALL_FUNCTION_2       2  ''
              390  STORE_FAST               'values'

 L. 801       392  LOAD_GLOBAL              zip
              394  LOAD_FAST                'axes'
              396  LOAD_FAST                'pad_width'
              398  LOAD_FAST                'values'
              400  CALL_FUNCTION_3       3  ''
              402  GET_ITER         
              404  FOR_ITER            444  'to 444'
              406  UNPACK_SEQUENCE_3     3 
              408  STORE_FAST               'axis'
              410  STORE_FAST               'width_pair'
              412  STORE_FAST               'value_pair'

 L. 802       414  LOAD_GLOBAL              _view_roi
              416  LOAD_FAST                'padded'
              418  LOAD_FAST                'original_area_slice'
              420  LOAD_FAST                'axis'
              422  CALL_FUNCTION_3       3  ''
              424  STORE_FAST               'roi'

 L. 803       426  LOAD_GLOBAL              _set_pad_area
              428  LOAD_FAST                'roi'
              430  LOAD_FAST                'axis'
              432  LOAD_FAST                'width_pair'
              434  LOAD_FAST                'value_pair'
              436  CALL_FUNCTION_4       4  ''
              438  POP_TOP          
          440_442  JUMP_BACK           404  'to 404'
          444_446  JUMP_FORWARD       1130  'to 1130'
            448_0  COME_FROM           364  '364'

 L. 805       448  LOAD_FAST                'mode'
              450  LOAD_STR                 'empty'
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   462  'to 462'

 L. 806   458_460  BREAK_LOOP         1130  'to 1130'
            462_0  COME_FROM           454  '454'

 L. 808       462  LOAD_FAST                'array'
              464  LOAD_ATTR                size
              466  LOAD_CONST               0
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   540  'to 540'

 L. 812       474  LOAD_GLOBAL              zip
              476  LOAD_FAST                'axes'
              478  LOAD_FAST                'pad_width'
              480  CALL_FUNCTION_2       2  ''
              482  GET_ITER         
            484_0  COME_FROM           514  '514'
            484_1  COME_FROM           504  '504'
              484  FOR_ITER            536  'to 536'
              486  UNPACK_SEQUENCE_2     2 
              488  STORE_FAST               'axis'
              490  STORE_FAST               'width_pair'

 L. 813       492  LOAD_FAST                'array'
              494  LOAD_ATTR                shape
              496  LOAD_FAST                'axis'
              498  BINARY_SUBSCR    
              500  LOAD_CONST               0
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   484  'to 484'
              508  LOAD_GLOBAL              any
              510  LOAD_FAST                'width_pair'
              512  CALL_FUNCTION_1       1  ''
          514_516  POP_JUMP_IF_FALSE   484  'to 484'

 L. 814       518  LOAD_GLOBAL              ValueError

 L. 815       520  LOAD_STR                 "can't extend empty axis {} using modes other than 'constant' or 'empty'"
              522  LOAD_METHOD              format

 L. 816       524  LOAD_FAST                'axis'

 L. 815       526  CALL_METHOD_1         1  ''

 L. 814       528  CALL_FUNCTION_1       1  ''
              530  RAISE_VARARGS_1       1  'exception instance'
          532_534  JUMP_BACK           484  'to 484'
          536_538  JUMP_FORWARD       1130  'to 1130'
            540_0  COME_FROM           470  '470'

 L. 821       540  LOAD_FAST                'mode'
              542  LOAD_STR                 'edge'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   614  'to 614'

 L. 822       550  LOAD_GLOBAL              zip
              552  LOAD_FAST                'axes'
              554  LOAD_FAST                'pad_width'
              556  CALL_FUNCTION_2       2  ''
              558  GET_ITER         
              560  FOR_ITER            610  'to 610'
              562  UNPACK_SEQUENCE_2     2 
              564  STORE_FAST               'axis'
              566  STORE_FAST               'width_pair'

 L. 823       568  LOAD_GLOBAL              _view_roi
              570  LOAD_FAST                'padded'
              572  LOAD_FAST                'original_area_slice'
              574  LOAD_FAST                'axis'
              576  CALL_FUNCTION_3       3  ''
              578  STORE_FAST               'roi'

 L. 824       580  LOAD_GLOBAL              _get_edges
              582  LOAD_FAST                'roi'
              584  LOAD_FAST                'axis'
              586  LOAD_FAST                'width_pair'
              588  CALL_FUNCTION_3       3  ''
              590  STORE_FAST               'edge_pair'

 L. 825       592  LOAD_GLOBAL              _set_pad_area
              594  LOAD_FAST                'roi'
              596  LOAD_FAST                'axis'
              598  LOAD_FAST                'width_pair'
              600  LOAD_FAST                'edge_pair'
              602  CALL_FUNCTION_4       4  ''
              604  POP_TOP          
          606_608  JUMP_BACK           560  'to 560'
          610_612  JUMP_FORWARD       1130  'to 1130'
            614_0  COME_FROM           546  '546'

 L. 827       614  LOAD_FAST                'mode'
              616  LOAD_STR                 'linear_ramp'
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_FALSE   718  'to 718'

 L. 828       624  LOAD_FAST                'kwargs'
              626  LOAD_METHOD              get
              628  LOAD_STR                 'end_values'
              630  LOAD_CONST               0
              632  CALL_METHOD_2         2  ''
              634  STORE_FAST               'end_values'

 L. 829       636  LOAD_GLOBAL              _as_pairs
              638  LOAD_FAST                'end_values'
              640  LOAD_FAST                'padded'
              642  LOAD_ATTR                ndim
              644  CALL_FUNCTION_2       2  ''
              646  STORE_FAST               'end_values'

 L. 830       648  LOAD_GLOBAL              zip
              650  LOAD_FAST                'axes'
              652  LOAD_FAST                'pad_width'
              654  LOAD_FAST                'end_values'
              656  CALL_FUNCTION_3       3  ''
              658  GET_ITER         
              660  FOR_ITER            714  'to 714'
              662  UNPACK_SEQUENCE_3     3 
              664  STORE_FAST               'axis'
              666  STORE_FAST               'width_pair'
              668  STORE_FAST               'value_pair'

 L. 831       670  LOAD_GLOBAL              _view_roi
              672  LOAD_FAST                'padded'
              674  LOAD_FAST                'original_area_slice'
              676  LOAD_FAST                'axis'
              678  CALL_FUNCTION_3       3  ''
              680  STORE_FAST               'roi'

 L. 832       682  LOAD_GLOBAL              _get_linear_ramps
              684  LOAD_FAST                'roi'
              686  LOAD_FAST                'axis'
              688  LOAD_FAST                'width_pair'
              690  LOAD_FAST                'value_pair'
              692  CALL_FUNCTION_4       4  ''
              694  STORE_FAST               'ramp_pair'

 L. 833       696  LOAD_GLOBAL              _set_pad_area
              698  LOAD_FAST                'roi'
              700  LOAD_FAST                'axis'
              702  LOAD_FAST                'width_pair'
              704  LOAD_FAST                'ramp_pair'
              706  CALL_FUNCTION_4       4  ''
              708  POP_TOP          
          710_712  JUMP_BACK           660  'to 660'
          714_716  JUMP_FORWARD       1130  'to 1130'
            718_0  COME_FROM           620  '620'

 L. 835       718  LOAD_FAST                'mode'
              720  LOAD_FAST                'stat_functions'
              722  <118>                 0  ''
          724_726  POP_JUMP_IF_FALSE   836  'to 836'

 L. 836       728  LOAD_FAST                'stat_functions'
              730  LOAD_FAST                'mode'
              732  BINARY_SUBSCR    
              734  STORE_FAST               'func'

 L. 837       736  LOAD_FAST                'kwargs'
              738  LOAD_METHOD              get
              740  LOAD_STR                 'stat_length'
              742  LOAD_CONST               None
              744  CALL_METHOD_2         2  ''
              746  STORE_FAST               'length'

 L. 838       748  LOAD_GLOBAL              _as_pairs
              750  LOAD_FAST                'length'
              752  LOAD_FAST                'padded'
              754  LOAD_ATTR                ndim
              756  LOAD_CONST               True
              758  LOAD_CONST               ('as_index',)
              760  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              762  STORE_FAST               'length'

 L. 839       764  LOAD_GLOBAL              zip
              766  LOAD_FAST                'axes'
              768  LOAD_FAST                'pad_width'
              770  LOAD_FAST                'length'
              772  CALL_FUNCTION_3       3  ''
              774  GET_ITER         
              776  FOR_ITER            832  'to 832'
              778  UNPACK_SEQUENCE_3     3 
              780  STORE_FAST               'axis'
              782  STORE_FAST               'width_pair'
              784  STORE_FAST               'length_pair'

 L. 840       786  LOAD_GLOBAL              _view_roi
              788  LOAD_FAST                'padded'
              790  LOAD_FAST                'original_area_slice'
              792  LOAD_FAST                'axis'
              794  CALL_FUNCTION_3       3  ''
              796  STORE_FAST               'roi'

 L. 841       798  LOAD_GLOBAL              _get_stats
              800  LOAD_FAST                'roi'
              802  LOAD_FAST                'axis'
              804  LOAD_FAST                'width_pair'
              806  LOAD_FAST                'length_pair'
              808  LOAD_FAST                'func'
              810  CALL_FUNCTION_5       5  ''
              812  STORE_FAST               'stat_pair'

 L. 842       814  LOAD_GLOBAL              _set_pad_area
              816  LOAD_FAST                'roi'
              818  LOAD_FAST                'axis'
              820  LOAD_FAST                'width_pair'
              822  LOAD_FAST                'stat_pair'
              824  CALL_FUNCTION_4       4  ''
              826  POP_TOP          
          828_830  JUMP_BACK           776  'to 776'
          832_834  JUMP_FORWARD       1130  'to 1130'
            836_0  COME_FROM           724  '724'

 L. 844       836  LOAD_FAST                'mode'
              838  LOAD_CONST               frozenset({'symmetric', 'reflect'})
              840  <118>                 0  ''
          842_844  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 845       846  LOAD_FAST                'kwargs'
              848  LOAD_METHOD              get
              850  LOAD_STR                 'reflect_type'
              852  LOAD_STR                 'even'
              854  CALL_METHOD_2         2  ''
              856  STORE_FAST               'method'

 L. 846       858  LOAD_FAST                'mode'
              860  LOAD_STR                 'symmetric'
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_FALSE   872  'to 872'
              868  LOAD_CONST               True
              870  JUMP_FORWARD        874  'to 874'
            872_0  COME_FROM           864  '864'
              872  LOAD_CONST               False
            874_0  COME_FROM           870  '870'
              874  STORE_FAST               'include_edge'

 L. 847       876  LOAD_GLOBAL              zip
              878  LOAD_FAST                'axes'
              880  LOAD_FAST                'pad_width'
              882  CALL_FUNCTION_2       2  ''
              884  GET_ITER         
            886_0  COME_FROM          1000  '1000'
              886  FOR_ITER           1036  'to 1036'
              888  UNPACK_SEQUENCE_2     2 
              890  STORE_FAST               'axis'
              892  UNPACK_SEQUENCE_2     2 
              894  STORE_FAST               'left_index'
              896  STORE_FAST               'right_index'

 L. 848       898  LOAD_FAST                'array'
              900  LOAD_ATTR                shape
              902  LOAD_FAST                'axis'
              904  BINARY_SUBSCR    
              906  LOAD_CONST               1
              908  COMPARE_OP               ==
          910_912  POP_JUMP_IF_FALSE   972  'to 972'
              914  LOAD_FAST                'left_index'
              916  LOAD_CONST               0
              918  COMPARE_OP               >
          920_922  POP_JUMP_IF_TRUE    934  'to 934'
              924  LOAD_FAST                'right_index'
              926  LOAD_CONST               0
              928  COMPARE_OP               >
          930_932  POP_JUMP_IF_FALSE   972  'to 972'
            934_0  COME_FROM           920  '920'

 L. 851       934  LOAD_GLOBAL              _get_edges
              936  LOAD_FAST                'padded'
              938  LOAD_FAST                'axis'
              940  LOAD_FAST                'left_index'
              942  LOAD_FAST                'right_index'
              944  BUILD_TUPLE_2         2 
              946  CALL_FUNCTION_3       3  ''
              948  STORE_FAST               'edge_pair'

 L. 852       950  LOAD_GLOBAL              _set_pad_area

 L. 853       952  LOAD_FAST                'padded'
              954  LOAD_FAST                'axis'
              956  LOAD_FAST                'left_index'
              958  LOAD_FAST                'right_index'
              960  BUILD_TUPLE_2         2 
              962  LOAD_FAST                'edge_pair'

 L. 852       964  CALL_FUNCTION_4       4  ''
              966  POP_TOP          

 L. 854   968_970  JUMP_BACK           886  'to 886'
            972_0  COME_FROM           930  '930'
            972_1  COME_FROM           910  '910'

 L. 856       972  LOAD_GLOBAL              _view_roi
              974  LOAD_FAST                'padded'
              976  LOAD_FAST                'original_area_slice'
              978  LOAD_FAST                'axis'
              980  CALL_FUNCTION_3       3  ''
              982  STORE_FAST               'roi'

 L. 857       984  LOAD_FAST                'left_index'
              986  LOAD_CONST               0
              988  COMPARE_OP               >
          990_992  POP_JUMP_IF_TRUE   1004  'to 1004'
              994  LOAD_FAST                'right_index'
              996  LOAD_CONST               0
              998  COMPARE_OP               >
         1000_1002  POP_JUMP_IF_FALSE   886  'to 886'
           1004_0  COME_FROM           990  '990'

 L. 861      1004  LOAD_GLOBAL              _set_reflect_both

 L. 862      1006  LOAD_FAST                'roi'
             1008  LOAD_FAST                'axis'
             1010  LOAD_FAST                'left_index'
             1012  LOAD_FAST                'right_index'
             1014  BUILD_TUPLE_2         2 

 L. 863      1016  LOAD_FAST                'method'
             1018  LOAD_FAST                'include_edge'

 L. 861      1020  CALL_FUNCTION_5       5  ''
             1022  UNPACK_SEQUENCE_2     2 
             1024  STORE_FAST               'left_index'
             1026  STORE_FAST               'right_index'
         1028_1030  JUMP_BACK           984  'to 984'
         1032_1034  JUMP_BACK           886  'to 886'
             1036  JUMP_FORWARD       1130  'to 1130'
           1038_0  COME_FROM           842  '842'

 L. 866      1038  LOAD_FAST                'mode'
             1040  LOAD_STR                 'wrap'
             1042  COMPARE_OP               ==
         1044_1046  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 867      1048  LOAD_GLOBAL              zip
             1050  LOAD_FAST                'axes'
             1052  LOAD_FAST                'pad_width'
             1054  CALL_FUNCTION_2       2  ''
             1056  GET_ITER         
           1058_0  COME_FROM          1098  '1098'
             1058  FOR_ITER           1130  'to 1130'
             1060  UNPACK_SEQUENCE_2     2 
             1062  STORE_FAST               'axis'
             1064  UNPACK_SEQUENCE_2     2 
             1066  STORE_FAST               'left_index'
             1068  STORE_FAST               'right_index'

 L. 868      1070  LOAD_GLOBAL              _view_roi
             1072  LOAD_FAST                'padded'
             1074  LOAD_FAST                'original_area_slice'
             1076  LOAD_FAST                'axis'
             1078  CALL_FUNCTION_3       3  ''
             1080  STORE_FAST               'roi'

 L. 869      1082  LOAD_FAST                'left_index'
             1084  LOAD_CONST               0
             1086  COMPARE_OP               >
         1088_1090  POP_JUMP_IF_TRUE   1102  'to 1102'
             1092  LOAD_FAST                'right_index'
             1094  LOAD_CONST               0
             1096  COMPARE_OP               >
         1098_1100  POP_JUMP_IF_FALSE  1058  'to 1058'
           1102_0  COME_FROM          1088  '1088'

 L. 873      1102  LOAD_GLOBAL              _set_wrap_both

 L. 874      1104  LOAD_FAST                'roi'
             1106  LOAD_FAST                'axis'
             1108  LOAD_FAST                'left_index'
             1110  LOAD_FAST                'right_index'
             1112  BUILD_TUPLE_2         2 

 L. 873      1114  CALL_FUNCTION_3       3  ''
             1116  UNPACK_SEQUENCE_2     2 
             1118  STORE_FAST               'left_index'
             1120  STORE_FAST               'right_index'
         1122_1124  JUMP_BACK          1082  'to 1082'
         1126_1128  JUMP_BACK          1058  'to 1058'
           1130_0  COME_FROM          1044  '1044'
           1130_1  COME_FROM          1036  '1036'
           1130_2  COME_FROM           832  '832'
           1130_3  COME_FROM           714  '714'
           1130_4  COME_FROM           610  '610'
           1130_5  COME_FROM           536  '536'
           1130_6  COME_FROM           458  '458'
           1130_7  COME_FROM           444  '444'

 L. 876      1130  LOAD_FAST                'padded'
             1132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 258_260