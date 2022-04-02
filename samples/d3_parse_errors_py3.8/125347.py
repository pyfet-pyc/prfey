# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\lib\index_tricks.py
import functools, sys, math
import numpy.core.numeric as _nx
from numpy.core.numeric import asarray, ScalarType, array, alltrue, cumprod, arange, ndim
from numpy.core.numerictypes import find_common_type, issubdtype
import numpy.matrixlib as matrixlib
from .function_base import diff
from numpy.core.multiarray import ravel_multi_index, unravel_index
from numpy.core.overrides import set_module
from numpy.core import overrides, linspace
from numpy.lib.stride_tricks import as_strided
array_function_dispatch = functools.partial((overrides.array_function_dispatch),
  module='numpy')
__all__ = [
 'ravel_multi_index', 'unravel_index', 'mgrid', 'ogrid', 'r_', 'c_',
 's_', 'index_exp', 'ix_', 'ndenumerate', 'ndindex', 'fill_diagonal',
 'diag_indices', 'diag_indices_from']

def _ix__dispatcher(*args):
    return args


@array_function_dispatch(_ix__dispatcher)
def ix_(*args):
    """
    Construct an open mesh from multiple sequences.

    This function takes N 1-D sequences and returns N outputs with N
    dimensions each, such that the shape is 1 in all but one dimension
    and the dimension with the non-unit shape value cycles through all
    N dimensions.

    Using `ix_` one can quickly construct index arrays that will index
    the cross product. ``a[np.ix_([1,3],[2,5])]`` returns the array
    ``[[a[1,2] a[1,5]], [a[3,2] a[3,5]]]``.

    Parameters
    ----------
    args : 1-D sequences
        Each sequence should be of integer or boolean type.
        Boolean sequences will be interpreted as boolean masks for the
        corresponding dimension (equivalent to passing in
        ``np.nonzero(boolean_sequence)``).

    Returns
    -------
    out : tuple of ndarrays
        N arrays with N dimensions each, with N the number of input
        sequences. Together these arrays form an open mesh.

    See Also
    --------
    ogrid, mgrid, meshgrid

    Examples
    --------
    >>> a = np.arange(10).reshape(2, 5)
    >>> a
    array([[0, 1, 2, 3, 4],
           [5, 6, 7, 8, 9]])
    >>> ixgrid = np.ix_([0, 1], [2, 4])
    >>> ixgrid
    (array([[0],
           [1]]), array([[2, 4]]))
    >>> ixgrid[0].shape, ixgrid[1].shape
    ((2, 1), (1, 2))
    >>> a[ixgrid]
    array([[2, 4],
           [7, 9]])

    >>> ixgrid = np.ix_([True, True], [2, 4])
    >>> a[ixgrid]
    array([[2, 4],
           [7, 9]])
    >>> ixgrid = np.ix_([True, True], [False, False, True, False, True])
    >>> a[ixgrid]
    array([[2, 4],
           [7, 9]])

    """
    out = []
    nd = len(args)
    for k, new in enumerate(args):
        if not isinstance(new, _nx.ndarray):
            new = asarray(new)
            if new.size == 0:
                new = new.astype(_nx.intp)
        if new.ndim != 1:
            raise ValueError('Cross index must be 1 dimensional')
        else:
            if issubdtype(new.dtype, _nx.bool_):
                new, = new.nonzero()
            new = new.reshape((1, ) * k + (new.size,) + (1, ) * (nd - k - 1))
            out.append(new)
    else:
        return tuple(out)


class nd_grid:
    __doc__ = '\n    Construct a multi-dimensional "meshgrid".\n\n    ``grid = nd_grid()`` creates an instance which will return a mesh-grid\n    when indexed.  The dimension and number of the output arrays are equal\n    to the number of indexing dimensions.  If the step length is not a\n    complex number, then the stop is not inclusive.\n\n    However, if the step length is a **complex number** (e.g. 5j), then the\n    integer part of its magnitude is interpreted as specifying the\n    number of points to create between the start and stop values, where\n    the stop value **is inclusive**.\n\n    If instantiated with an argument of ``sparse=True``, the mesh-grid is\n    open (or not fleshed out) so that only one-dimension of each returned\n    argument is greater than 1.\n\n    Parameters\n    ----------\n    sparse : bool, optional\n        Whether the grid is sparse or not. Default is False.\n\n    Notes\n    -----\n    Two instances of `nd_grid` are made available in the NumPy namespace,\n    `mgrid` and `ogrid`, approximately defined as::\n\n        mgrid = nd_grid(sparse=False)\n        ogrid = nd_grid(sparse=True)\n\n    Users should use these pre-defined instances instead of using `nd_grid`\n    directly.\n    '

    def __init__(self, sparse=False):
        self.sparse = sparse

    def __getitem__(self, key):
        try:
            size = []
            typ = int
            for k in range(len(key)):
                step = key[k].step
                start = key[k].start
                if start is None:
                    start = 0
                if step is None:
                    step = 1
                if isinstance(step, complex):
                    size.append(int(abs(step)))
                    typ = float
                else:
                    size.append(int(math.ceil((key[k].stop - start) / (step * 1.0))))
                if not isinstance(step, float):
                    if not isinstance(start, float):
                        if isinstance(key[k].stop, float):
                            pass
                typ = float
            else:
                if self.sparse:
                    nn = [_nx.arange(_x, dtype=_t) for _x, _t in zip(size, (typ,) * len(size))]
                else:
                    nn = _nx.indices(size, typ)
                for k in range(len(size)):
                    step = key[k].step
                    start = key[k].start
                    if start is None:
                        start = 0
                    else:
                        if step is None:
                            step = 1
                        if isinstance(step, complex):
                            step = int(abs(step))
                            if step != 1:
                                step = (key[k].stop - start) / float(step - 1)
                        nn[k] = nn[k] * step + start
                else:
                    if self.sparse:
                        slobj = [
                         _nx.newaxis] * len(size)
                        for k in range(len(size)):
                            slobj[k] = slice(None, None)
                            nn[k] = nn[k][tuple(slobj)]
                            slobj[k] = _nx.newaxis

            return nn
        except (IndexError, TypeError):
            step = key.step
            stop = key.stop
            start = key.start
            if start is None:
                start = 0
            if isinstance(step, complex):
                step = abs(step)
                length = int(step)
                if step != 1:
                    step = (key.stop - start) / float(step - 1)
                stop = key.stop + step
                return _nx.arange(0, length, 1, float) * step + start
            return _nx.arange(start, stop, step)


class MGridClass(nd_grid):
    __doc__ = '\n    `nd_grid` instance which returns a dense multi-dimensional "meshgrid".\n\n    An instance of `numpy.lib.index_tricks.nd_grid` which returns an dense\n    (or fleshed out) mesh-grid when indexed, so that each returned argument\n    has the same shape.  The dimensions and number of the output arrays are\n    equal to the number of indexing dimensions.  If the step length is not a\n    complex number, then the stop is not inclusive.\n\n    However, if the step length is a **complex number** (e.g. 5j), then\n    the integer part of its magnitude is interpreted as specifying the\n    number of points to create between the start and stop values, where\n    the stop value **is inclusive**.\n\n    Returns\n    ----------\n    mesh-grid `ndarrays` all of the same dimensions\n\n    See Also\n    --------\n    numpy.lib.index_tricks.nd_grid : class of `ogrid` and `mgrid` objects\n    ogrid : like mgrid but returns open (not fleshed out) mesh grids\n    r_ : array concatenator\n\n    Examples\n    --------\n    >>> np.mgrid[0:5,0:5]\n    array([[[0, 0, 0, 0, 0],\n            [1, 1, 1, 1, 1],\n            [2, 2, 2, 2, 2],\n            [3, 3, 3, 3, 3],\n            [4, 4, 4, 4, 4]],\n           [[0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4]]])\n    >>> np.mgrid[-1:1:5j]\n    array([-1. , -0.5,  0. ,  0.5,  1. ])\n\n    '

    def __init__(self):
        super(MGridClass, self).__init__(sparse=False)


mgrid = MGridClass()

class OGridClass(nd_grid):
    __doc__ = '\n    `nd_grid` instance which returns an open multi-dimensional "meshgrid".\n\n    An instance of `numpy.lib.index_tricks.nd_grid` which returns an open\n    (i.e. not fleshed out) mesh-grid when indexed, so that only one dimension\n    of each returned array is greater than 1.  The dimension and number of the\n    output arrays are equal to the number of indexing dimensions.  If the step\n    length is not a complex number, then the stop is not inclusive.\n\n    However, if the step length is a **complex number** (e.g. 5j), then\n    the integer part of its magnitude is interpreted as specifying the\n    number of points to create between the start and stop values, where\n    the stop value **is inclusive**.\n\n    Returns\n    -------\n    mesh-grid\n        `ndarrays` with only one dimension not equal to 1\n\n    See Also\n    --------\n    np.lib.index_tricks.nd_grid : class of `ogrid` and `mgrid` objects\n    mgrid : like `ogrid` but returns dense (or fleshed out) mesh grids\n    r_ : array concatenator\n\n    Examples\n    --------\n    >>> from numpy import ogrid\n    >>> ogrid[-1:1:5j]\n    array([-1. , -0.5,  0. ,  0.5,  1. ])\n    >>> ogrid[0:5,0:5]\n    [array([[0],\n            [1],\n            [2],\n            [3],\n            [4]]), array([[0, 1, 2, 3, 4]])]\n\n    '

    def __init__(self):
        super(OGridClass, self).__init__(sparse=True)


ogrid = OGridClass()

class AxisConcatenator:
    __doc__ = '\n    Translates slice objects to concatenation along an axis.\n\n    For detailed documentation on usage, see `r_`.\n    '
    concatenate = staticmethod(_nx.concatenate)
    makemat = staticmethod(matrixlib.matrix)

    def __init__(self, axis=0, matrix=False, ndmin=1, trans1d=-1):
        self.axis = axis
        self.matrix = matrix
        self.trans1d = trans1d
        self.ndmin = ndmin

    def __getitem__--- This code section failed: ---

 L. 318         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L. 319        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              _getframe
               14  CALL_METHOD_0         0  ''
               16  LOAD_ATTR                f_back
               18  STORE_FAST               'frame'

 L. 320        20  LOAD_GLOBAL              matrixlib
               22  LOAD_METHOD              bmat
               24  LOAD_FAST                'key'
               26  LOAD_FAST                'frame'
               28  LOAD_ATTR                f_globals
               30  LOAD_FAST                'frame'
               32  LOAD_ATTR                f_locals
               34  CALL_METHOD_3         3  ''
               36  STORE_FAST               'mymat'

 L. 321        38  LOAD_FAST                'mymat'
               40  RETURN_VALUE     
             42_0  COME_FROM             8  '8'

 L. 323        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'key'
               46  LOAD_GLOBAL              tuple
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     58  'to 58'

 L. 324        52  LOAD_FAST                'key'
               54  BUILD_TUPLE_1         1 
               56  STORE_FAST               'key'
             58_0  COME_FROM            50  '50'

 L. 327        58  LOAD_FAST                'self'
               60  LOAD_ATTR                trans1d
               62  STORE_FAST               'trans1d'

 L. 328        64  LOAD_FAST                'self'
               66  LOAD_ATTR                ndmin
               68  STORE_FAST               'ndmin'

 L. 329        70  LOAD_FAST                'self'
               72  LOAD_ATTR                matrix
               74  STORE_FAST               'matrix'

 L. 330        76  LOAD_FAST                'self'
               78  LOAD_ATTR                axis
               80  STORE_FAST               'axis'

 L. 332        82  BUILD_LIST_0          0 
               84  STORE_FAST               'objs'

 L. 333        86  BUILD_LIST_0          0 
               88  STORE_FAST               'scalars'

 L. 334        90  BUILD_LIST_0          0 
               92  STORE_FAST               'arraytypes'

 L. 335        94  BUILD_LIST_0          0 
               96  STORE_FAST               'scalartypes'

 L. 337        98  LOAD_GLOBAL              enumerate
              100  LOAD_FAST                'key'
              102  CALL_FUNCTION_1       1  ''
              104  GET_ITER         
            106_0  COME_FROM           750  '750'
            106_1  COME_FROM           736  '736'
            106_2  COME_FROM           724  '724'
            106_3  COME_FROM           476  '476'
            106_4  COME_FROM           406  '406'
            106_5  COME_FROM           328  '328'
          106_108  FOR_ITER            752  'to 752'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'k'
              114  STORE_FAST               'item'

 L. 338       116  LOAD_CONST               False
              118  STORE_FAST               'scalar'

 L. 339       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'item'
              124  LOAD_GLOBAL              slice
              126  CALL_FUNCTION_2       2  ''
          128_130  POP_JUMP_IF_FALSE   276  'to 276'

 L. 340       132  LOAD_FAST                'item'
              134  LOAD_ATTR                step
              136  STORE_FAST               'step'

 L. 341       138  LOAD_FAST                'item'
              140  LOAD_ATTR                start
              142  STORE_FAST               'start'

 L. 342       144  LOAD_FAST                'item'
              146  LOAD_ATTR                stop
              148  STORE_FAST               'stop'

 L. 343       150  LOAD_FAST                'start'
              152  LOAD_CONST               None
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 344       158  LOAD_CONST               0
              160  STORE_FAST               'start'
            162_0  COME_FROM           156  '156'

 L. 345       162  LOAD_FAST                'step'
              164  LOAD_CONST               None
              166  COMPARE_OP               is
              168  POP_JUMP_IF_FALSE   174  'to 174'

 L. 346       170  LOAD_CONST               1
              172  STORE_FAST               'step'
            174_0  COME_FROM           168  '168'

 L. 347       174  LOAD_GLOBAL              isinstance
              176  LOAD_FAST                'step'
              178  LOAD_GLOBAL              complex
              180  CALL_FUNCTION_2       2  ''
              182  POP_JUMP_IF_FALSE   212  'to 212'

 L. 348       184  LOAD_GLOBAL              int
              186  LOAD_GLOBAL              abs
              188  LOAD_FAST                'step'
              190  CALL_FUNCTION_1       1  ''
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'size'

 L. 349       196  LOAD_GLOBAL              linspace
              198  LOAD_FAST                'start'
              200  LOAD_FAST                'stop'
              202  LOAD_FAST                'size'
              204  LOAD_CONST               ('num',)
              206  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              208  STORE_FAST               'newobj'
              210  JUMP_FORWARD        226  'to 226'
            212_0  COME_FROM           182  '182'

 L. 351       212  LOAD_GLOBAL              _nx
              214  LOAD_METHOD              arange
              216  LOAD_FAST                'start'
              218  LOAD_FAST                'stop'
              220  LOAD_FAST                'step'
              222  CALL_METHOD_3         3  ''
              224  STORE_FAST               'newobj'
            226_0  COME_FROM           210  '210'

 L. 352       226  LOAD_FAST                'ndmin'
              228  LOAD_CONST               1
              230  COMPARE_OP               >
          232_234  POP_JUMP_IF_FALSE   712  'to 712'

 L. 353       236  LOAD_GLOBAL              array
              238  LOAD_FAST                'newobj'
              240  LOAD_CONST               False
              242  LOAD_FAST                'ndmin'
              244  LOAD_CONST               ('copy', 'ndmin')
              246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              248  STORE_FAST               'newobj'

 L. 354       250  LOAD_FAST                'trans1d'
              252  LOAD_CONST               -1
              254  COMPARE_OP               !=
          256_258  POP_JUMP_IF_FALSE   712  'to 712'

 L. 355       260  LOAD_FAST                'newobj'
              262  LOAD_METHOD              swapaxes
              264  LOAD_CONST               -1
              266  LOAD_FAST                'trans1d'
              268  CALL_METHOD_2         2  ''
              270  STORE_FAST               'newobj'
          272_274  JUMP_FORWARD        712  'to 712'
            276_0  COME_FROM           128  '128'

 L. 356       276  LOAD_GLOBAL              isinstance
              278  LOAD_FAST                'item'
              280  LOAD_GLOBAL              str
              282  CALL_FUNCTION_2       2  ''
          284_286  POP_JUMP_IF_FALSE   518  'to 518'

 L. 357       288  LOAD_FAST                'k'
              290  LOAD_CONST               0
              292  COMPARE_OP               !=
          294_296  POP_JUMP_IF_FALSE   306  'to 306'

 L. 358       298  LOAD_GLOBAL              ValueError
              300  LOAD_STR                 'special directives must be the first entry.'
              302  CALL_FUNCTION_1       1  ''
              304  RAISE_VARARGS_1       1  'exception instance'
            306_0  COME_FROM           294  '294'

 L. 360       306  LOAD_FAST                'item'
              308  LOAD_CONST               ('r', 'c')
              310  COMPARE_OP               in
          312_314  POP_JUMP_IF_FALSE   330  'to 330'

 L. 361       316  LOAD_CONST               True
              318  STORE_FAST               'matrix'

 L. 362       320  LOAD_FAST                'item'
              322  LOAD_STR                 'c'
              324  COMPARE_OP               ==
              326  STORE_FAST               'col'

 L. 363       328  JUMP_BACK           106  'to 106'
            330_0  COME_FROM           312  '312'

 L. 364       330  LOAD_STR                 ','
              332  LOAD_FAST                'item'
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   464  'to 464'

 L. 365       340  LOAD_FAST                'item'
              342  LOAD_METHOD              split
              344  LOAD_STR                 ','
              346  CALL_METHOD_1         1  ''
              348  STORE_FAST               'vec'

 L. 366       350  SETUP_FINALLY       412  'to 412'

 L. 367       352  LOAD_LISTCOMP            '<code_object <listcomp>>'
              354  LOAD_STR                 'AxisConcatenator.__getitem__.<locals>.<listcomp>'
              356  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              358  LOAD_FAST                'vec'
              360  LOAD_CONST               None
              362  LOAD_CONST               2
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    
              368  GET_ITER         
              370  CALL_FUNCTION_1       1  ''
              372  UNPACK_SEQUENCE_2     2 
              374  STORE_FAST               'axis'
              376  STORE_FAST               'ndmin'

 L. 368       378  LOAD_GLOBAL              len
              380  LOAD_FAST                'vec'
              382  CALL_FUNCTION_1       1  ''
              384  LOAD_CONST               3
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   404  'to 404'

 L. 369       392  LOAD_GLOBAL              int
              394  LOAD_FAST                'vec'
              396  LOAD_CONST               2
              398  BINARY_SUBSCR    
              400  CALL_FUNCTION_1       1  ''
              402  STORE_FAST               'trans1d'
            404_0  COME_FROM           388  '388'

 L. 370       404  POP_BLOCK        
              406  JUMP_BACK           106  'to 106'
              408  POP_BLOCK        
              410  JUMP_FORWARD        464  'to 464'
            412_0  COME_FROM_FINALLY   350  '350'

 L. 371       412  DUP_TOP          
              414  LOAD_GLOBAL              Exception
              416  COMPARE_OP               exception-match
          418_420  POP_JUMP_IF_FALSE   462  'to 462'
              422  POP_TOP          
              424  STORE_FAST               'e'
              426  POP_TOP          
              428  SETUP_FINALLY       450  'to 450'

 L. 372       430  LOAD_GLOBAL              ValueError

 L. 373       432  LOAD_STR                 'unknown special directive {!r}'
              434  LOAD_METHOD              format
              436  LOAD_FAST                'item'
              438  CALL_METHOD_1         1  ''

 L. 372       440  CALL_FUNCTION_1       1  ''

 L. 374       442  LOAD_FAST                'e'

 L. 372       444  RAISE_VARARGS_2       2  'exception instance with __cause__'
              446  POP_BLOCK        
              448  BEGIN_FINALLY    
            450_0  COME_FROM_FINALLY   428  '428'
              450  LOAD_CONST               None
              452  STORE_FAST               'e'
              454  DELETE_FAST              'e'
              456  END_FINALLY      
              458  POP_EXCEPT       
              460  JUMP_FORWARD        464  'to 464'
            462_0  COME_FROM           418  '418'
              462  END_FINALLY      
            464_0  COME_FROM           460  '460'
            464_1  COME_FROM           410  '410'
            464_2  COME_FROM           336  '336'

 L. 375       464  SETUP_FINALLY       482  'to 482'

 L. 376       466  LOAD_GLOBAL              int
              468  LOAD_FAST                'item'
              470  CALL_FUNCTION_1       1  ''
              472  STORE_FAST               'axis'

 L. 377       474  POP_BLOCK        
              476  JUMP_BACK           106  'to 106'
              478  POP_BLOCK        
              480  JUMP_FORWARD        516  'to 516'
            482_0  COME_FROM_FINALLY   464  '464'

 L. 378       482  DUP_TOP          
              484  LOAD_GLOBAL              ValueError
              486  LOAD_GLOBAL              TypeError
              488  BUILD_TUPLE_2         2 
              490  COMPARE_OP               exception-match
          492_494  POP_JUMP_IF_FALSE   514  'to 514'
              496  POP_TOP          
              498  POP_TOP          
              500  POP_TOP          

 L. 379       502  LOAD_GLOBAL              ValueError
              504  LOAD_STR                 'unknown special directive'
              506  CALL_FUNCTION_1       1  ''
              508  RAISE_VARARGS_1       1  'exception instance'
              510  POP_EXCEPT       
              512  JUMP_FORWARD        516  'to 516'
            514_0  COME_FROM           492  '492'
              514  END_FINALLY      
            516_0  COME_FROM           512  '512'
            516_1  COME_FROM           480  '480'
              516  JUMP_FORWARD        712  'to 712'
            518_0  COME_FROM           284  '284'

 L. 380       518  LOAD_GLOBAL              type
              520  LOAD_FAST                'item'
              522  CALL_FUNCTION_1       1  ''
              524  LOAD_GLOBAL              ScalarType
              526  COMPARE_OP               in
          528_530  POP_JUMP_IF_FALSE   576  'to 576'

 L. 381       532  LOAD_GLOBAL              array
              534  LOAD_FAST                'item'
              536  LOAD_FAST                'ndmin'
              538  LOAD_CONST               ('ndmin',)
              540  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              542  STORE_FAST               'newobj'

 L. 382       544  LOAD_FAST                'scalars'
              546  LOAD_METHOD              append
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                'objs'
              552  CALL_FUNCTION_1       1  ''
              554  CALL_METHOD_1         1  ''
              556  POP_TOP          

 L. 383       558  LOAD_CONST               True
              560  STORE_FAST               'scalar'

 L. 384       562  LOAD_FAST                'scalartypes'
              564  LOAD_METHOD              append
              566  LOAD_FAST                'newobj'
              568  LOAD_ATTR                dtype
              570  CALL_METHOD_1         1  ''
              572  POP_TOP          
              574  JUMP_FORWARD        712  'to 712'
            576_0  COME_FROM           528  '528'

 L. 386       576  LOAD_GLOBAL              ndim
              578  LOAD_FAST                'item'
              580  CALL_FUNCTION_1       1  ''
              582  STORE_FAST               'item_ndim'

 L. 387       584  LOAD_GLOBAL              array
              586  LOAD_FAST                'item'
              588  LOAD_CONST               False
              590  LOAD_CONST               True
              592  LOAD_FAST                'ndmin'
              594  LOAD_CONST               ('copy', 'subok', 'ndmin')
              596  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              598  STORE_FAST               'newobj'

 L. 388       600  LOAD_FAST                'trans1d'
              602  LOAD_CONST               -1
              604  COMPARE_OP               !=
          606_608  POP_JUMP_IF_FALSE   712  'to 712'
              610  LOAD_FAST                'item_ndim'
              612  LOAD_FAST                'ndmin'
              614  COMPARE_OP               <
          616_618  POP_JUMP_IF_FALSE   712  'to 712'

 L. 389       620  LOAD_FAST                'ndmin'
              622  LOAD_FAST                'item_ndim'
              624  BINARY_SUBTRACT  
              626  STORE_FAST               'k2'

 L. 390       628  LOAD_FAST                'trans1d'
              630  STORE_FAST               'k1'

 L. 391       632  LOAD_FAST                'k1'
              634  LOAD_CONST               0
              636  COMPARE_OP               <
          638_640  POP_JUMP_IF_FALSE   654  'to 654'

 L. 392       642  LOAD_FAST                'k1'
              644  LOAD_FAST                'k2'
              646  LOAD_CONST               1
              648  BINARY_ADD       
              650  INPLACE_ADD      
              652  STORE_FAST               'k1'
            654_0  COME_FROM           638  '638'

 L. 393       654  LOAD_GLOBAL              list
              656  LOAD_GLOBAL              range
              658  LOAD_FAST                'ndmin'
              660  CALL_FUNCTION_1       1  ''
              662  CALL_FUNCTION_1       1  ''
              664  STORE_FAST               'defaxes'

 L. 394       666  LOAD_FAST                'defaxes'
              668  LOAD_CONST               None
              670  LOAD_FAST                'k1'
              672  BUILD_SLICE_2         2 
              674  BINARY_SUBSCR    
              676  LOAD_FAST                'defaxes'
              678  LOAD_FAST                'k2'
              680  LOAD_CONST               None
              682  BUILD_SLICE_2         2 
              684  BINARY_SUBSCR    
              686  BINARY_ADD       
              688  LOAD_FAST                'defaxes'
              690  LOAD_FAST                'k1'
              692  LOAD_FAST                'k2'
              694  BUILD_SLICE_2         2 
              696  BINARY_SUBSCR    
              698  BINARY_ADD       
              700  STORE_FAST               'axes'

 L. 395       702  LOAD_FAST                'newobj'
              704  LOAD_METHOD              transpose
              706  LOAD_FAST                'axes'
              708  CALL_METHOD_1         1  ''
              710  STORE_FAST               'newobj'
            712_0  COME_FROM           616  '616'
            712_1  COME_FROM           606  '606'
            712_2  COME_FROM           574  '574'
            712_3  COME_FROM           516  '516'
            712_4  COME_FROM           272  '272'
            712_5  COME_FROM           256  '256'
            712_6  COME_FROM           232  '232'

 L. 396       712  LOAD_FAST                'objs'
              714  LOAD_METHOD              append
              716  LOAD_FAST                'newobj'
              718  CALL_METHOD_1         1  ''
              720  POP_TOP          

 L. 397       722  LOAD_FAST                'scalar'
              724  POP_JUMP_IF_TRUE_BACK   106  'to 106'
              726  LOAD_GLOBAL              isinstance
              728  LOAD_FAST                'newobj'
              730  LOAD_GLOBAL              _nx
              732  LOAD_ATTR                ndarray
              734  CALL_FUNCTION_2       2  ''
              736  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 398       738  LOAD_FAST                'arraytypes'
              740  LOAD_METHOD              append
              742  LOAD_FAST                'newobj'
              744  LOAD_ATTR                dtype
              746  CALL_METHOD_1         1  ''
              748  POP_TOP          
              750  JUMP_BACK           106  'to 106'
            752_0  COME_FROM           106  '106'

 L. 401       752  LOAD_GLOBAL              find_common_type
              754  LOAD_FAST                'arraytypes'
              756  LOAD_FAST                'scalartypes'
              758  CALL_FUNCTION_2       2  ''
              760  STORE_FAST               'final_dtype'

 L. 402       762  LOAD_FAST                'final_dtype'
              764  LOAD_CONST               None
              766  COMPARE_OP               is-not
          768_770  POP_JUMP_IF_FALSE   802  'to 802'

 L. 403       772  LOAD_FAST                'scalars'
              774  GET_ITER         
            776_0  COME_FROM           798  '798'
              776  FOR_ITER            802  'to 802'
              778  STORE_FAST               'k'

 L. 404       780  LOAD_FAST                'objs'
              782  LOAD_FAST                'k'
              784  BINARY_SUBSCR    
              786  LOAD_METHOD              astype
              788  LOAD_FAST                'final_dtype'
              790  CALL_METHOD_1         1  ''
              792  LOAD_FAST                'objs'
              794  LOAD_FAST                'k'
              796  STORE_SUBSCR     
          798_800  JUMP_BACK           776  'to 776'
            802_0  COME_FROM           776  '776'
            802_1  COME_FROM           768  '768'

 L. 406       802  LOAD_FAST                'self'
              804  LOAD_ATTR                concatenate
              806  LOAD_GLOBAL              tuple
              808  LOAD_FAST                'objs'
              810  CALL_FUNCTION_1       1  ''
              812  LOAD_FAST                'axis'
              814  LOAD_CONST               ('axis',)
              816  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              818  STORE_FAST               'res'

 L. 408       820  LOAD_FAST                'matrix'
          822_824  POP_JUMP_IF_FALSE   864  'to 864'

 L. 409       826  LOAD_FAST                'res'
              828  LOAD_ATTR                ndim
              830  STORE_FAST               'oldndim'

 L. 410       832  LOAD_FAST                'self'
              834  LOAD_METHOD              makemat
              836  LOAD_FAST                'res'
              838  CALL_METHOD_1         1  ''
              840  STORE_FAST               'res'

 L. 411       842  LOAD_FAST                'oldndim'
              844  LOAD_CONST               1
              846  COMPARE_OP               ==
          848_850  POP_JUMP_IF_FALSE   864  'to 864'
              852  LOAD_FAST                'col'
          854_856  POP_JUMP_IF_FALSE   864  'to 864'

 L. 412       858  LOAD_FAST                'res'
              860  LOAD_ATTR                T
              862  STORE_FAST               'res'
            864_0  COME_FROM           854  '854'
            864_1  COME_FROM           848  '848'
            864_2  COME_FROM           822  '822'

 L. 413       864  LOAD_FAST                'res'
              866  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 408

    def __len__(self):
        return 0


class RClass(AxisConcatenator):
    __doc__ = "\n    Translates slice objects to concatenation along the first axis.\n\n    This is a simple way to build up arrays quickly. There are two use cases.\n\n    1. If the index expression contains comma separated arrays, then stack\n       them along their first axis.\n    2. If the index expression contains slice notation or scalars then create\n       a 1-D array with a range indicated by the slice notation.\n\n    If slice notation is used, the syntax ``start:stop:step`` is equivalent\n    to ``np.arange(start, stop, step)`` inside of the brackets. However, if\n    ``step`` is an imaginary number (i.e. 100j) then its integer portion is\n    interpreted as a number-of-points desired and the start and stop are\n    inclusive. In other words ``start:stop:stepj`` is interpreted as\n    ``np.linspace(start, stop, step, endpoint=1)`` inside of the brackets.\n    After expansion of slice notation, all comma separated sequences are\n    concatenated together.\n\n    Optional character strings placed as the first element of the index\n    expression can be used to change the output. The strings 'r' or 'c' result\n    in matrix output. If the result is 1-D and 'r' is specified a 1 x N (row)\n    matrix is produced. If the result is 1-D and 'c' is specified, then a N x 1\n    (column) matrix is produced. If the result is 2-D then both provide the\n    same matrix result.\n\n    A string integer specifies which axis to stack multiple comma separated\n    arrays along. A string of two comma-separated integers allows indication\n    of the minimum number of dimensions to force each entry into as the\n    second integer (the axis to concatenate along is still the first integer).\n\n    A string with three comma-separated integers allows specification of the\n    axis to concatenate along, the minimum number of dimensions to force the\n    entries to, and which axis should contain the start of the arrays which\n    are less than the specified number of dimensions. In other words the third\n    integer allows you to specify where the 1's should be placed in the shape\n    of the arrays that have their shapes upgraded. By default, they are placed\n    in the front of the shape tuple. The third argument allows you to specify\n    where the start of the array should be instead. Thus, a third argument of\n    '0' would place the 1's at the end of the array shape. Negative integers\n    specify where in the new shape tuple the last dimension of upgraded arrays\n    should be placed, so the default is '-1'.\n\n    Parameters\n    ----------\n    Not a function, so takes no parameters\n\n\n    Returns\n    -------\n    A concatenated ndarray or matrix.\n\n    See Also\n    --------\n    concatenate : Join a sequence of arrays along an existing axis.\n    c_ : Translates slice objects to concatenation along the second axis.\n\n    Examples\n    --------\n    >>> np.r_[np.array([1,2,3]), 0, 0, np.array([4,5,6])]\n    array([1, 2, 3, ..., 4, 5, 6])\n    >>> np.r_[-1:1:6j, [0]*3, 5, 6]\n    array([-1. , -0.6, -0.2,  0.2,  0.6,  1. ,  0. ,  0. ,  0. ,  5. ,  6. ])\n\n    String integers specify the axis to concatenate along or the minimum\n    number of dimensions to force entries into.\n\n    >>> a = np.array([[0, 1, 2], [3, 4, 5]])\n    >>> np.r_['-1', a, a] # concatenate along last axis\n    array([[0, 1, 2, 0, 1, 2],\n           [3, 4, 5, 3, 4, 5]])\n    >>> np.r_['0,2', [1,2,3], [4,5,6]] # concatenate along first axis, dim>=2\n    array([[1, 2, 3],\n           [4, 5, 6]])\n\n    >>> np.r_['0,2,0', [1,2,3], [4,5,6]]\n    array([[1],\n           [2],\n           [3],\n           [4],\n           [5],\n           [6]])\n    >>> np.r_['1,2,0', [1,2,3], [4,5,6]]\n    array([[1, 4],\n           [2, 5],\n           [3, 6]])\n\n    Using 'r' or 'c' as a first string argument creates a matrix.\n\n    >>> np.r_['r',[1,2,3], [4,5,6]]\n    matrix([[1, 2, 3, 4, 5, 6]])\n\n    "

    def __init__(self):
        AxisConcatenator.__init__(self, 0)


r_ = RClass()

class CClass(AxisConcatenator):
    __doc__ = "\n    Translates slice objects to concatenation along the second axis.\n\n    This is short-hand for ``np.r_['-1,2,0', index expression]``, which is\n    useful because of its common occurrence. In particular, arrays will be\n    stacked along their last axis after being upgraded to at least 2-D with\n    1's post-pended to the shape (column vectors made out of 1-D arrays).\n    \n    See Also\n    --------\n    column_stack : Stack 1-D arrays as columns into a 2-D array.\n    r_ : For more detailed documentation.\n\n    Examples\n    --------\n    >>> np.c_[np.array([1,2,3]), np.array([4,5,6])]\n    array([[1, 4],\n           [2, 5],\n           [3, 6]])\n    >>> np.c_[np.array([[1,2,3]]), 0, 0, np.array([[4,5,6]])]\n    array([[1, 2, 3, ..., 4, 5, 6]])\n\n    "

    def __init__(self):
        AxisConcatenator.__init__(self, (-1), ndmin=2, trans1d=0)


c_ = CClass()

@set_module('numpy')
class ndenumerate:
    __doc__ = '\n    Multidimensional index iterator.\n\n    Return an iterator yielding pairs of array coordinates and values.\n\n    Parameters\n    ----------\n    arr : ndarray\n      Input array.\n\n    See Also\n    --------\n    ndindex, flatiter\n\n    Examples\n    --------\n    >>> a = np.array([[1, 2], [3, 4]])\n    >>> for index, x in np.ndenumerate(a):\n    ...     print(index, x)\n    (0, 0) 1\n    (0, 1) 2\n    (1, 0) 3\n    (1, 1) 4\n\n    '

    def __init__(self, arr):
        self.iter = asarray(arr).flat

    def __next__(self):
        """
        Standard iterator method, returns the index tuple and array value.

        Returns
        -------
        coords : tuple of ints
            The indices of the current iteration.
        val : scalar
            The array element of the current iteration.

        """
        return (
         self.iter.coords, next(self.iter))

    def __iter__(self):
        return self


@set_module('numpy')
class ndindex:
    __doc__ = '\n    An N-dimensional iterator object to index arrays.\n\n    Given the shape of an array, an `ndindex` instance iterates over\n    the N-dimensional index of the array. At each iteration a tuple\n    of indices is returned, the last dimension is iterated over first.\n\n    Parameters\n    ----------\n    `*args` : ints\n      The size of each dimension of the array.\n\n    See Also\n    --------\n    ndenumerate, flatiter\n\n    Examples\n    --------\n    >>> for index in np.ndindex(3, 2, 1):\n    ...     print(index)\n    (0, 0, 0)\n    (0, 1, 0)\n    (1, 0, 0)\n    (1, 1, 0)\n    (2, 0, 0)\n    (2, 1, 0)\n\n    '

    def __init__(self, *shape):
        if len(shape) == 1:
            if isinstance(shape[0], tuple):
                shape = shape[0]
        x = as_strided((_nx.zeros(1)), shape=shape, strides=(_nx.zeros_like(shape)))
        self._it = _nx.nditer(x, flags=['multi_index', 'zerosize_ok'], order='C')

    def __iter__(self):
        return self

    def ndincr(self):
        """
        Increment the multi-dimensional index by one.

        This method is for backward compatibility only: do not use.
        """
        next(self)

    def __next__(self):
        """
        Standard iterator method, updates the index and returns the index
        tuple.

        Returns
        -------
        val : tuple of ints
            Returns a tuple containing the indices of the current
            iteration.

        """
        next(self._it)
        return self._it.multi_index


class IndexExpression:
    __doc__ = "\n    A nicer way to build up index tuples for arrays.\n\n    .. note::\n       Use one of the two predefined instances `index_exp` or `s_`\n       rather than directly using `IndexExpression`.\n\n    For any index combination, including slicing and axis insertion,\n    ``a[indices]`` is the same as ``a[np.index_exp[indices]]`` for any\n    array `a`. However, ``np.index_exp[indices]`` can be used anywhere\n    in Python code and returns a tuple of slice objects that can be\n    used in the construction of complex index expressions.\n\n    Parameters\n    ----------\n    maketuple : bool\n        If True, always returns a tuple.\n\n    See Also\n    --------\n    index_exp : Predefined instance that always returns a tuple:\n       `index_exp = IndexExpression(maketuple=True)`.\n    s_ : Predefined instance without tuple conversion:\n       `s_ = IndexExpression(maketuple=False)`.\n\n    Notes\n    -----\n    You can do all this with `slice()` plus a few special objects,\n    but there's a lot to remember and this version is simpler because\n    it uses the standard array indexing syntax.\n\n    Examples\n    --------\n    >>> np.s_[2::2]\n    slice(2, None, 2)\n    >>> np.index_exp[2::2]\n    (slice(2, None, 2),)\n\n    >>> np.array([0, 1, 2, 3, 4])[np.s_[2::2]]\n    array([2, 4])\n\n    "

    def __init__(self, maketuple):
        self.maketuple = maketuple

    def __getitem__(self, item):
        if self.maketuple:
            if not isinstance(item, tuple):
                return (
                 item,)
            return item


index_exp = IndexExpression(maketuple=True)
s_ = IndexExpression(maketuple=False)

def _fill_diagonal_dispatcher(a, val, wrap=None):
    return (
     a,)


@array_function_dispatch(_fill_diagonal_dispatcher)
def fill_diagonal(a, val, wrap=False):
    """Fill the main diagonal of the given array of any dimensionality.

    For an array `a` with ``a.ndim >= 2``, the diagonal is the list of
    locations with indices ``a[i, ..., i]`` all identical. This function
    modifies the input array in-place, it does not return a value.

    Parameters
    ----------
    a : array, at least 2-D.
      Array whose diagonal is to be filled, it gets modified in-place.

    val : scalar
      Value to be written on the diagonal, its type must be compatible with
      that of the array a.

    wrap : bool
      For tall matrices in NumPy version up to 1.6.2, the
      diagonal "wrapped" after N columns. You can have this behavior
      with this option. This affects only tall matrices.

    See also
    --------
    diag_indices, diag_indices_from

    Notes
    -----
    .. versionadded:: 1.4.0

    This functionality can be obtained via `diag_indices`, but internally
    this version uses a much faster implementation that never constructs the
    indices and uses simple slicing.

    Examples
    --------
    >>> a = np.zeros((3, 3), int)
    >>> np.fill_diagonal(a, 5)
    >>> a
    array([[5, 0, 0],
           [0, 5, 0],
           [0, 0, 5]])

    The same function can operate on a 4-D array:

    >>> a = np.zeros((3, 3, 3, 3), int)
    >>> np.fill_diagonal(a, 4)

    We only show a few blocks for clarity:

    >>> a[0, 0]
    array([[4, 0, 0],
           [0, 0, 0],
           [0, 0, 0]])
    >>> a[1, 1]
    array([[0, 0, 0],
           [0, 4, 0],
           [0, 0, 0]])
    >>> a[2, 2]
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 4]])

    The wrap option affects only tall matrices:

    >>> # tall matrices no wrap
    >>> a = np.zeros((5, 3), int)
    >>> np.fill_diagonal(a, 4)
    >>> a
    array([[4, 0, 0],
           [0, 4, 0],
           [0, 0, 4],
           [0, 0, 0],
           [0, 0, 0]])

    >>> # tall matrices wrap
    >>> a = np.zeros((5, 3), int)
    >>> np.fill_diagonal(a, 4, wrap=True)
    >>> a
    array([[4, 0, 0],
           [0, 4, 0],
           [0, 0, 4],
           [0, 0, 0],
           [4, 0, 0]])

    >>> # wide matrices
    >>> a = np.zeros((3, 5), int)
    >>> np.fill_diagonal(a, 4, wrap=True)
    >>> a
    array([[4, 0, 0, 0, 0],
           [0, 4, 0, 0, 0],
           [0, 0, 4, 0, 0]])

    The anti-diagonal can be filled by reversing the order of elements
    using either `numpy.flipud` or `numpy.fliplr`.

    >>> a = np.zeros((3, 3), int);
    >>> np.fill_diagonal(np.fliplr(a), [1,2,3])  # Horizontal flip
    >>> a
    array([[0, 0, 1],
           [0, 2, 0],
           [3, 0, 0]])
    >>> np.fill_diagonal(np.flipud(a), [1,2,3])  # Vertical flip
    >>> a
    array([[0, 0, 3],
           [0, 2, 0],
           [1, 0, 0]])

    Note that the order in which the diagonal is filled varies depending
    on the flip function.
    """
    if a.ndim < 2:
        raise ValueError('array must be at least 2-d')
    end = None
    if a.ndim == 2:
        step = a.shape[1] + 1
        end = (wrap or a.shape[1]) * a.shape[1]
    else:
        if not alltrue(diff(a.shape) == 0):
            raise ValueError('All dimensions of input must be of equal length')
        step = 1 + cumprod(a.shape[:-1]).sum()
    a.flat[:end:step] = val


@set_module('numpy')
def diag_indices(n, ndim=2):
    """
    Return the indices to access the main diagonal of an array.

    This returns a tuple of indices that can be used to access the main
    diagonal of an array `a` with ``a.ndim >= 2`` dimensions and shape
    (n, n, ..., n). For ``a.ndim = 2`` this is the usual diagonal, for
    ``a.ndim > 2`` this is the set of indices to access ``a[i, i, ..., i]``
    for ``i = [0..n-1]``.

    Parameters
    ----------
    n : int
      The size, along each dimension, of the arrays for which the returned
      indices can be used.

    ndim : int, optional
      The number of dimensions.

    See also
    --------
    diag_indices_from

    Notes
    -----
    .. versionadded:: 1.4.0

    Examples
    --------
    Create a set of indices to access the diagonal of a (4, 4) array:

    >>> di = np.diag_indices(4)
    >>> di
    (array([0, 1, 2, 3]), array([0, 1, 2, 3]))
    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> a[di] = 100
    >>> a
    array([[100,   1,   2,   3],
           [  4, 100,   6,   7],
           [  8,   9, 100,  11],
           [ 12,  13,  14, 100]])

    Now, we create indices to manipulate a 3-D array:

    >>> d3 = np.diag_indices(2, 3)
    >>> d3
    (array([0, 1]), array([0, 1]), array([0, 1]))

    And use it to set the diagonal of an array of zeros to 1:

    >>> a = np.zeros((2, 2, 2), dtype=int)
    >>> a[d3] = 1
    >>> a
    array([[[1, 0],
            [0, 0]],
           [[0, 0],
            [0, 1]]])

    """
    idx = arange(n)
    return (
     idx,) * ndim


def _diag_indices_from(arr):
    return (
     arr,)


@array_function_dispatch(_diag_indices_from)
def diag_indices_from(arr):
    """
    Return the indices to access the main diagonal of an n-dimensional array.

    See `diag_indices` for full details.

    Parameters
    ----------
    arr : array, at least 2-D

    See Also
    --------
    diag_indices

    Notes
    -----
    .. versionadded:: 1.4.0

    """
    if not arr.ndim >= 2:
        raise ValueError('input array must be at least 2-d')
    if not alltrue(diff(arr.shape) == 0):
        raise ValueError('All dimensions of input must be of equal length')
    return diag_indices(arr.shape[0], arr.ndim)