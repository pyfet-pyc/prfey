# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\lib\arrayterator.py
"""
A buffered iterator for big arrays.

This module solves the problem of iterating over a big file-based array
without having to read it into memory. The `Arrayterator` class wraps
an array object, and when iterated it will return sub-arrays with at most
a user-specified number of elements.

"""
from operator import mul
from functools import reduce
__all__ = [
 'Arrayterator']

class Arrayterator:
    __doc__ = '\n    Buffered iterator for big arrays.\n\n    `Arrayterator` creates a buffered iterator for reading big arrays in small\n    contiguous blocks. The class is useful for objects stored in the\n    file system. It allows iteration over the object *without* reading\n    everything in memory; instead, small blocks are read and iterated over.\n\n    `Arrayterator` can be used with any object that supports multidimensional\n    slices. This includes NumPy arrays, but also variables from\n    Scientific.IO.NetCDF or pynetcdf for example.\n\n    Parameters\n    ----------\n    var : array_like\n        The object to iterate over.\n    buf_size : int, optional\n        The buffer size. If `buf_size` is supplied, the maximum amount of\n        data that will be read into memory is `buf_size` elements.\n        Default is None, which will read as many element as possible\n        into memory.\n\n    Attributes\n    ----------\n    var\n    buf_size\n    start\n    stop\n    step\n    shape\n    flat\n\n    See Also\n    --------\n    ndenumerate : Multidimensional array iterator.\n    flatiter : Flat array iterator.\n    memmap : Create a memory-map to an array stored in a binary file on disk.\n\n    Notes\n    -----\n    The algorithm works by first finding a "running dimension", along which\n    the blocks will be extracted. Given an array of dimensions\n    ``(d1, d2, ..., dn)``, e.g. if `buf_size` is smaller than ``d1``, the\n    first dimension will be used. If, on the other hand,\n    ``d1 < buf_size < d1*d2`` the second dimension will be used, and so on.\n    Blocks are extracted along this dimension, and when the last block is\n    returned the process continues from the next dimension, until all\n    elements have been read.\n\n    Examples\n    --------\n    >>> a = np.arange(3 * 4 * 5 * 6).reshape(3, 4, 5, 6)\n    >>> a_itor = np.lib.Arrayterator(a, 2)\n    >>> a_itor.shape\n    (3, 4, 5, 6)\n\n    Now we can iterate over ``a_itor``, and it will return arrays of size\n    two. Since `buf_size` was smaller than any dimension, the first\n    dimension will be iterated over first:\n\n    >>> for subarr in a_itor:\n    ...     if not subarr.all():\n    ...         print(subarr, subarr.shape) # doctest: +SKIP\n    >>> # [[[[0 1]]]] (1, 1, 1, 2)\n\n    '

    def __init__(self, var, buf_size=None):
        self.var = var
        self.buf_size = buf_size
        self.start = [0 for dim in var.shape]
        self.stop = [dim for dim in var.shape]
        self.step = [1 for dim in var.shape]

    def __getattr__(self, attr):
        return getattr(self.var, attr)

    def __getitem__--- This code section failed: ---

 L. 101         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'index'
                4  LOAD_GLOBAL              tuple
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     16  'to 16'

 L. 102        10  LOAD_FAST                'index'
               12  BUILD_TUPLE_1         1 
               14  STORE_FAST               'index'
             16_0  COME_FROM             8  '8'

 L. 103        16  BUILD_LIST_0          0 
               18  STORE_FAST               'fixed'

 L. 104        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'index'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                ndim
               30  ROT_TWO          
               32  STORE_FAST               'length'
               34  STORE_FAST               'dims'

 L. 105        36  LOAD_FAST                'index'
               38  GET_ITER         
             40_0  COME_FROM           134  '134'
             40_1  COME_FROM           122  '122'
             40_2  COME_FROM            88  '88'
               40  FOR_ITER            136  'to 136'
               42  STORE_FAST               'slice_'

 L. 106        44  LOAD_FAST                'slice_'
               46  LOAD_GLOBAL              Ellipsis
               48  <117>                 0  ''
               50  POP_JUMP_IF_FALSE    90  'to 90'

 L. 107        52  LOAD_FAST                'fixed'
               54  LOAD_METHOD              extend
               56  LOAD_GLOBAL              slice
               58  LOAD_CONST               None
               60  CALL_FUNCTION_1       1  ''
               62  BUILD_LIST_1          1 
               64  LOAD_FAST                'dims'
               66  LOAD_FAST                'length'
               68  BINARY_SUBTRACT  
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  BINARY_MULTIPLY  
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 108        80  LOAD_GLOBAL              len
               82  LOAD_FAST                'fixed'
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'length'
               88  JUMP_BACK            40  'to 40'
             90_0  COME_FROM            50  '50'

 L. 109        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'slice_'
               94  LOAD_GLOBAL              int
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   124  'to 124'

 L. 110       100  LOAD_FAST                'fixed'
              102  LOAD_METHOD              append
              104  LOAD_GLOBAL              slice
              106  LOAD_FAST                'slice_'
              108  LOAD_FAST                'slice_'
              110  LOAD_CONST               1
              112  BINARY_ADD       
              114  LOAD_CONST               1
              116  CALL_FUNCTION_3       3  ''
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  JUMP_BACK            40  'to 40'
            124_0  COME_FROM            98  '98'

 L. 112       124  LOAD_FAST                'fixed'
              126  LOAD_METHOD              append
              128  LOAD_FAST                'slice_'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            40  'to 40'
            136_0  COME_FROM            40  '40'

 L. 113       136  LOAD_GLOBAL              tuple
              138  LOAD_FAST                'fixed'
              140  CALL_FUNCTION_1       1  ''
              142  STORE_FAST               'index'

 L. 114       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'index'
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'dims'
              152  COMPARE_OP               <
              154  POP_JUMP_IF_FALSE   182  'to 182'

 L. 115       156  LOAD_FAST                'index'
              158  LOAD_GLOBAL              slice
              160  LOAD_CONST               None
              162  CALL_FUNCTION_1       1  ''
              164  BUILD_TUPLE_1         1 
              166  LOAD_FAST                'dims'
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'index'
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_SUBTRACT  
              176  BINARY_MULTIPLY  
              178  INPLACE_ADD      
              180  STORE_FAST               'index'
            182_0  COME_FROM           154  '154'

 L. 118       182  LOAD_FAST                'self'
              184  LOAD_METHOD              __class__
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                var
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                buf_size
              194  CALL_METHOD_2         2  ''
              196  STORE_FAST               'out'

 L. 119       198  LOAD_GLOBAL              enumerate

 L. 120       200  LOAD_GLOBAL              zip
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                start
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                stop
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                step
              214  LOAD_FAST                'index'
              216  CALL_FUNCTION_4       4  ''

 L. 119       218  CALL_FUNCTION_1       1  ''
              220  GET_ITER         
            222_0  COME_FROM           328  '328'
              222  FOR_ITER            330  'to 330'
              224  UNPACK_SEQUENCE_2     2 
              226  STORE_FAST               'i'
              228  UNPACK_SEQUENCE_4     4 
              230  STORE_FAST               'start'
              232  STORE_FAST               'stop'
              234  STORE_FAST               'step'
              236  STORE_FAST               'slice_'

 L. 121       238  LOAD_FAST                'start'
              240  LOAD_FAST                'slice_'
              242  LOAD_ATTR                start
              244  JUMP_IF_TRUE_OR_POP   248  'to 248'
              246  LOAD_CONST               0
            248_0  COME_FROM           244  '244'
              248  BINARY_ADD       
              250  LOAD_FAST                'out'
              252  LOAD_ATTR                start
              254  LOAD_FAST                'i'
              256  STORE_SUBSCR     

 L. 122       258  LOAD_FAST                'step'
              260  LOAD_FAST                'slice_'
              262  LOAD_ATTR                step
          264_266  JUMP_IF_TRUE_OR_POP   270  'to 270'
              268  LOAD_CONST               1
            270_0  COME_FROM           264  '264'
              270  BINARY_MULTIPLY  
              272  LOAD_FAST                'out'
              274  LOAD_ATTR                step
              276  LOAD_FAST                'i'
              278  STORE_SUBSCR     

 L. 123       280  LOAD_FAST                'start'
              282  LOAD_FAST                'slice_'
              284  LOAD_ATTR                stop
          286_288  JUMP_IF_TRUE_OR_POP   296  'to 296'
              290  LOAD_FAST                'stop'
              292  LOAD_FAST                'start'
              294  BINARY_SUBTRACT  
            296_0  COME_FROM           286  '286'
              296  BINARY_ADD       
              298  LOAD_FAST                'out'
              300  LOAD_ATTR                stop
              302  LOAD_FAST                'i'
              304  STORE_SUBSCR     

 L. 124       306  LOAD_GLOBAL              min
              308  LOAD_FAST                'stop'
              310  LOAD_FAST                'out'
              312  LOAD_ATTR                stop
              314  LOAD_FAST                'i'
              316  BINARY_SUBSCR    
              318  CALL_FUNCTION_2       2  ''
              320  LOAD_FAST                'out'
              322  LOAD_ATTR                stop
              324  LOAD_FAST                'i'
              326  STORE_SUBSCR     
              328  JUMP_BACK           222  'to 222'
            330_0  COME_FROM           222  '222'

 L. 125       330  LOAD_FAST                'out'
              332  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 48

    def __array__(self):
        """
        Return corresponding data.

        """
        slice_ = tuple((slice(*t) for t in zipself.startself.stopself.step))
        return self.var[slice_]

    @property
    def flat(self):
        """
        A 1-D flat iterator for Arrayterator objects.

        This iterator returns elements of the array to be iterated over in
        `Arrayterator` one by one. It is similar to `flatiter`.

        See Also
        --------
        Arrayterator
        flatiter

        Examples
        --------
        >>> a = np.arange(3 * 4 * 5 * 6).reshape(3, 4, 5, 6)
        >>> a_itor = np.lib.Arrayterator(a, 2)

        >>> for subarr in a_itor.flat:
        ...     if not subarr:
        ...         print(subarr, type(subarr))
        ...
        0 <class 'numpy.int64'>

        """
        for block in self:
            yield from block.flat

        if False:
            yield None

    @property
    def shape(self):
        """
        The shape of the array to be iterated over.

        For an example, see `Arrayterator`.

        """
        return tuple(((stop - start - 1) // step + 1 for start, stop, step in zipself.startself.stopself.step))

    def __iter__(self):
        if [dim for dim in self.shape if dim <= 0]:
            return
        start = self.start[:]
        stop = self.stop[:]
        step = self.step[:]
        ndims = self.var.ndim
        while True:
            count = self.buf_size or reduce(mul, self.shape)
            rundim = 0
            for i in range(ndims - 1)(-1)(-1):
                if count == 0:
                    stop[i] = start[i] + 1
                elif count <= self.shape[i]:
                    stop[i] = start[i] + count * step[i]
                    rundim = i
                else:
                    stop[i] = self.stop[i]
                stop[i] = min(self.stop[i], stop[i])
                count = count // self.shape[i]
            else:
                slice_ = tuple((slice(*t) for t in zipstartstopstep))
                yield self.var[slice_]
                start[rundim] = stop[rundim]
                for i in range(ndims - 1)0(-1):
                    if start[i] >= self.stop[i]:
                        start[i] = self.start[i]
                        start[(i - 1)] += self.step[(i - 1)]
                    if start[0] >= self.stop[0]:
                        return