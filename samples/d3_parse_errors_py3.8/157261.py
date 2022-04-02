# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\lib\index_tricks.py
import functools, sys, math, warnings
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
                if isinstance(step, (_nx.complexfloating, complex)):
                    size.append(int(abs(step)))
                    typ = float
                else:
                    size.append(int(math.ceil((key[k].stop - start) / (step * 1.0))))
                if not isinstance(step, (_nx.floating, float)):
                    if not isinstance(start, (_nx.floating, float)):
                        if isinstance(key[k].stop, (_nx.floating, float)):
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
                        if isinstance(step, (_nx.complexfloating, complex)):
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
            if isinstance(step, (_nx.complexfloating, complex)):
                step = abs(step)
                length = int(step)
                if step != 1:
                    step = (key.stop - start) / float(step - 1)
                stop = key.stop + step
                return _nx.arange(0, length, 1, float) * step + start
            return _nx.arange(start, stop, step)


class MGridClass(nd_grid):
    __doc__ = '\n    `nd_grid` instance which returns a dense multi-dimensional "meshgrid".\n\n    An instance of `numpy.lib.index_tricks.nd_grid` which returns an dense\n    (or fleshed out) mesh-grid when indexed, so that each returned argument\n    has the same shape.  The dimensions and number of the output arrays are\n    equal to the number of indexing dimensions.  If the step length is not a\n    complex number, then the stop is not inclusive.\n\n    However, if the step length is a **complex number** (e.g. 5j), then\n    the integer part of its magnitude is interpreted as specifying the\n    number of points to create between the start and stop values, where\n    the stop value **is inclusive**.\n\n    Returns\n    -------\n    mesh-grid `ndarrays` all of the same dimensions\n\n    See Also\n    --------\n    numpy.lib.index_tricks.nd_grid : class of `ogrid` and `mgrid` objects\n    ogrid : like mgrid but returns open (not fleshed out) mesh grids\n    r_ : array concatenator\n\n    Examples\n    --------\n    >>> np.mgrid[0:5,0:5]\n    array([[[0, 0, 0, 0, 0],\n            [1, 1, 1, 1, 1],\n            [2, 2, 2, 2, 2],\n            [3, 3, 3, 3, 3],\n            [4, 4, 4, 4, 4]],\n           [[0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4],\n            [0, 1, 2, 3, 4]]])\n    >>> np.mgrid[-1:1:5j]\n    array([-1. , -0.5,  0. ,  0.5,  1. ])\n\n    '

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

 L. 319         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L. 320        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              _getframe
               14  CALL_METHOD_0         0  ''
               16  LOAD_ATTR                f_back
               18  STORE_FAST               'frame'

 L. 321        20  LOAD_GLOBAL              matrixlib
               22  LOAD_METHOD              bmat
               24  LOAD_FAST                'key'
               26  LOAD_FAST                'frame'
               28  LOAD_ATTR                f_globals
               30  LOAD_FAST                'frame'
               32  LOAD_ATTR                f_locals
               34  CALL_METHOD_3         3  ''
               36  STORE_FAST               'mymat'

 L. 322        38  LOAD_FAST                'mymat'
               40  RETURN_VALUE     
             42_0  COME_FROM             8  '8'

 L. 324        42  LOAD_GLOBAL              isinstance
               44  LOAD_FAST                'key'
               46  LOAD_GLOBAL              tuple
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_TRUE     58  'to 58'

 L. 325        52  LOAD_FAST                'key'
               54  BUILD_TUPLE_1         1 
               56  STORE_FAST               'key'
             58_0  COME_FROM            50  '50'

 L. 328        58  LOAD_FAST                'self'
               60  LOAD_ATTR                trans1d
               62  STORE_FAST               'trans1d'

 L. 329        64  LOAD_FAST                'self'
               66  LOAD_ATTR                ndmin
               68  STORE_FAST               'ndmin'

 L. 330        70  LOAD_FAST                'self'
               72  LOAD_ATTR                matrix
               74  STORE_FAST               'matrix'

 L. 331        76  LOAD_FAST                'self'
               78  LOAD_ATTR                axis
               80  STORE_FAST               'axis'

 L. 333        82  BUILD_LIST_0          0 
               84  STORE_FAST               'objs'

 L. 334        86  BUILD_LIST_0          0 
               88  STORE_FAST               'scalars'

 L. 335        90  BUILD_LIST_0          0 
               92  STORE_FAST               'arraytypes'

 L. 336        94  BUILD_LIST_0          0 
               96  STORE_FAST               'scalartypes'

 L. 338        98  LOAD_GLOBAL              enumerate
              100  LOAD_FAST                'key'
              102  CALL_FUNCTION_1       1  ''
              104  GET_ITER         
            106_0  COME_FROM           756  '756'
            106_1  COME_FROM           742  '742'
            106_2  COME_FROM           730  '730'
            106_3  COME_FROM           482  '482'
            106_4  COME_FROM           412  '412'
            106_5  COME_FROM           334  '334'
          106_108  FOR_ITER            758  'to 758'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'k'
              114  STORE_FAST               'item'

 L. 339       116  LOAD_CONST               False
              118  STORE_FAST               'scalar'

 L. 340       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'item'
              124  LOAD_GLOBAL              slice
              126  CALL_FUNCTION_2       2  ''
          128_130  POP_JUMP_IF_FALSE   282  'to 282'

 L. 341       132  LOAD_FAST                'item'
              134  LOAD_ATTR                step
              136  STORE_FAST               'step'

 L. 342       138  LOAD_FAST                'item'
              140  LOAD_ATTR                start
              142  STORE_FAST               'start'

 L. 343       144  LOAD_FAST                'item'
              146  LOAD_ATTR                stop
              148  STORE_FAST               'stop'

 L. 344       150  LOAD_FAST                'start'
              152  LOAD_CONST               None
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 345       158  LOAD_CONST               0
              160  STORE_FAST               'start'
            162_0  COME_FROM           156  '156'

 L. 346       162  LOAD_FAST                'step'
              164  LOAD_CONST               None
              166  COMPARE_OP               is
              168  POP_JUMP_IF_FALSE   174  'to 174'

 L. 347       170  LOAD_CONST               1
              172  STORE_FAST               'step'
            174_0  COME_FROM           168  '168'

 L. 348       174  LOAD_GLOBAL              isinstance
              176  LOAD_FAST                'step'
              178  LOAD_GLOBAL              _nx
              180  LOAD_ATTR                complexfloating
              182  LOAD_GLOBAL              complex
              184  BUILD_TUPLE_2         2 
              186  CALL_FUNCTION_2       2  ''
              188  POP_JUMP_IF_FALSE   218  'to 218'

 L. 349       190  LOAD_GLOBAL              int
              192  LOAD_GLOBAL              abs
              194  LOAD_FAST                'step'
              196  CALL_FUNCTION_1       1  ''
              198  CALL_FUNCTION_1       1  ''
              200  STORE_FAST               'size'

 L. 350       202  LOAD_GLOBAL              linspace
              204  LOAD_FAST                'start'
              206  LOAD_FAST                'stop'
              208  LOAD_FAST                'size'
              210  LOAD_CONST               ('num',)
              212  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              214  STORE_FAST               'newobj'
              216  JUMP_FORWARD        232  'to 232'
            218_0  COME_FROM           188  '188'

 L. 352       218  LOAD_GLOBAL              _nx
              220  LOAD_METHOD              arange
              222  LOAD_FAST                'start'
              224  LOAD_FAST                'stop'
              226  LOAD_FAST                'step'
              228  CALL_METHOD_3         3  ''
              230  STORE_FAST               'newobj'
            232_0  COME_FROM           216  '216'

 L. 353       232  LOAD_FAST                'ndmin'
              234  LOAD_CONST               1
              236  COMPARE_OP               >
          238_240  POP_JUMP_IF_FALSE   718  'to 718'

 L. 354       242  LOAD_GLOBAL              array
              244  LOAD_FAST                'newobj'
              246  LOAD_CONST               False
              248  LOAD_FAST                'ndmin'
              250  LOAD_CONST               ('copy', 'ndmin')
              252  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              254  STORE_FAST               'newobj'

 L. 355       256  LOAD_FAST                'trans1d'
              258  LOAD_CONST               -1
              260  COMPARE_OP               !=
          262_264  POP_JUMP_IF_FALSE   718  'to 718'

 L. 356       266  LOAD_FAST                'newobj'
              268  LOAD_METHOD              swapaxes
              270  LOAD_CONST               -1
              272  LOAD_FAST                'trans1d'
              274  CALL_METHOD_2         2  ''
              276  STORE_FAST               'newobj'
          278_280  JUMP_FORWARD        718  'to 718'
            282_0  COME_FROM           128  '128'

 L. 357       282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'item'
              286  LOAD_GLOBAL              str
              288  CALL_FUNCTION_2       2  ''
          290_292  POP_JUMP_IF_FALSE   524  'to 524'

 L. 358       294  LOAD_FAST                'k'
              296  LOAD_CONST               0
              298  COMPARE_OP               !=
          300_302  POP_JUMP_IF_FALSE   312  'to 312'

 L. 359       304  LOAD_GLOBAL              ValueError
              306  LOAD_STR                 'special directives must be the first entry.'
              308  CALL_FUNCTION_1       1  ''
              310  RAISE_VARARGS_1       1  'exception instance'
            312_0  COME_FROM           300  '300'

 L. 361       312  LOAD_FAST                'item'
              314  LOAD_CONST               ('r', 'c')
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   336  'to 336'

 L. 362       322  LOAD_CONST               True
              324  STORE_FAST               'matrix'

 L. 363       326  LOAD_FAST                'item'
              328  LOAD_STR                 'c'
              330  COMPARE_OP               ==
              332  STORE_FAST               'col'

 L. 364       334  JUMP_BACK           106  'to 106'
            336_0  COME_FROM           318  '318'

 L. 365       336  LOAD_STR                 ','
              338  LOAD_FAST                'item'
              340  COMPARE_OP               in
          342_344  POP_JUMP_IF_FALSE   470  'to 470'

 L. 366       346  LOAD_FAST                'item'
              348  LOAD_METHOD              split
              350  LOAD_STR                 ','
              352  CALL_METHOD_1         1  ''
              354  STORE_FAST               'vec'

 L. 367       356  SETUP_FINALLY       418  'to 418'

 L. 368       358  LOAD_LISTCOMP            '<code_object <listcomp>>'
              360  LOAD_STR                 'AxisConcatenator.__getitem__.<locals>.<listcomp>'
              362  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              364  LOAD_FAST                'vec'
              366  LOAD_CONST               None
              368  LOAD_CONST               2
              370  BUILD_SLICE_2         2 
              372  BINARY_SUBSCR    
              374  GET_ITER         
              376  CALL_FUNCTION_1       1  ''
              378  UNPACK_SEQUENCE_2     2 
              380  STORE_FAST               'axis'
              382  STORE_FAST               'ndmin'

 L. 369       384  LOAD_GLOBAL              len
              386  LOAD_FAST                'vec'
              388  CALL_FUNCTION_1       1  ''
              390  LOAD_CONST               3
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   410  'to 410'

 L. 370       398  LOAD_GLOBAL              int
              400  LOAD_FAST                'vec'
              402  LOAD_CONST               2
              404  BINARY_SUBSCR    
              406  CALL_FUNCTION_1       1  ''
              408  STORE_FAST               'trans1d'
            410_0  COME_FROM           394  '394'

 L. 371       410  POP_BLOCK        
              412  JUMP_BACK           106  'to 106'
              414  POP_BLOCK        
              416  JUMP_FORWARD        470  'to 470'
            418_0  COME_FROM_FINALLY   356  '356'

 L. 372       418  DUP_TOP          
              420  LOAD_GLOBAL              Exception
              422  COMPARE_OP               exception-match
          424_426  POP_JUMP_IF_FALSE   468  'to 468'
              428  POP_TOP          
              430  STORE_FAST               'e'
              432  POP_TOP          
              434  SETUP_FINALLY       456  'to 456'

 L. 373       436  LOAD_GLOBAL              ValueError

 L. 374       438  LOAD_STR                 'unknown special directive {!r}'
              440  LOAD_METHOD              format
              442  LOAD_FAST                'item'
              444  CALL_METHOD_1         1  ''

 L. 373       446  CALL_FUNCTION_1       1  ''

 L. 375       448  LOAD_FAST                'e'

 L. 373       450  RAISE_VARARGS_2       2  'exception instance with __cause__'
              452  POP_BLOCK        
              454  BEGIN_FINALLY    
            456_0  COME_FROM_FINALLY   434  '434'
              456  LOAD_CONST               None
              458  STORE_FAST               'e'
              460  DELETE_FAST              'e'
              462  END_FINALLY      
              464  POP_EXCEPT       
              466  JUMP_FORWARD        470  'to 470'
            468_0  COME_FROM           424  '424'
              468  END_FINALLY      
            470_0  COME_FROM           466  '466'
            470_1  COME_FROM           416  '416'
            470_2  COME_FROM           342  '342'

 L. 376       470  SETUP_FINALLY       488  'to 488'

 L. 377       472  LOAD_GLOBAL              int
              474  LOAD_FAST                'item'
              476  CALL_FUNCTION_1       1  ''
              478  STORE_FAST               'axis'

 L. 378       480  POP_BLOCK        
              482  JUMP_BACK           106  'to 106'
              484  POP_BLOCK        
              486  JUMP_FORWARD        522  'to 522'
            488_0  COME_FROM_FINALLY   470  '470'

 L. 379       488  DUP_TOP          
              490  LOAD_GLOBAL              ValueError
              492  LOAD_GLOBAL              TypeError
              494  BUILD_TUPLE_2         2 
              496  COMPARE_OP               exception-match
          498_500  POP_JUMP_IF_FALSE   520  'to 520'
              502  POP_TOP          
              504  POP_TOP          
              506  POP_TOP          

 L. 380       508  LOAD_GLOBAL              ValueError
              510  LOAD_STR                 'unknown special directive'
              512  CALL_FUNCTION_1       1  ''
              514  RAISE_VARARGS_1       1  'exception instance'
              516  POP_EXCEPT       
              518  JUMP_FORWARD        522  'to 522'
            520_0  COME_FROM           498  '498'
              520  END_FINALLY      
            522_0  COME_FROM           518  '518'
            522_1  COME_FROM           486  '486'
              522  JUMP_FORWARD        718  'to 718'
            524_0  COME_FROM           290  '290'

 L. 381       524  LOAD_GLOBAL              type
              526  LOAD_FAST                'item'
              528  CALL_FUNCTION_1       1  ''
              530  LOAD_GLOBAL              ScalarType
              532  COMPARE_OP               in
          534_536  POP_JUMP_IF_FALSE   582  'to 582'

 L. 382       538  LOAD_GLOBAL              array
              540  LOAD_FAST                'item'
              542  LOAD_FAST                'ndmin'
              544  LOAD_CONST               ('ndmin',)
              546  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              548  STORE_FAST               'newobj'

 L. 383       550  LOAD_FAST                'scalars'
              552  LOAD_METHOD              append
              554  LOAD_GLOBAL              len
              556  LOAD_FAST                'objs'
              558  CALL_FUNCTION_1       1  ''
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          

 L. 384       564  LOAD_CONST               True
              566  STORE_FAST               'scalar'

 L. 385       568  LOAD_FAST                'scalartypes'
              570  LOAD_METHOD              append
              572  LOAD_FAST                'newobj'
              574  LOAD_ATTR                dtype
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
              580  JUMP_FORWARD        718  'to 718'
            582_0  COME_FROM           534  '534'

 L. 387       582  LOAD_GLOBAL              ndim
              584  LOAD_FAST                'item'
              586  CALL_FUNCTION_1       1  ''
              588  STORE_FAST               'item_ndim'

 L. 388       590  LOAD_GLOBAL              array
              592  LOAD_FAST                'item'
              594  LOAD_CONST               False
              596  LOAD_CONST               True
              598  LOAD_FAST                'ndmin'
              600  LOAD_CONST               ('copy', 'subok', 'ndmin')
              602  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              604  STORE_FAST               'newobj'

 L. 389       606  LOAD_FAST                'trans1d'
              608  LOAD_CONST               -1
              610  COMPARE_OP               !=
          612_614  POP_JUMP_IF_FALSE   718  'to 718'
              616  LOAD_FAST                'item_ndim'
              618  LOAD_FAST                'ndmin'
              620  COMPARE_OP               <
          622_624  POP_JUMP_IF_FALSE   718  'to 718'

 L. 390       626  LOAD_FAST                'ndmin'
              628  LOAD_FAST                'item_ndim'
              630  BINARY_SUBTRACT  
              632  STORE_FAST               'k2'

 L. 391       634  LOAD_FAST                'trans1d'
              636  STORE_FAST               'k1'

 L. 392       638  LOAD_FAST                'k1'
              640  LOAD_CONST               0
              642  COMPARE_OP               <
          644_646  POP_JUMP_IF_FALSE   660  'to 660'

 L. 393       648  LOAD_FAST                'k1'
              650  LOAD_FAST                'k2'
              652  LOAD_CONST               1
              654  BINARY_ADD       
              656  INPLACE_ADD      
              658  STORE_FAST               'k1'
            660_0  COME_FROM           644  '644'

 L. 394       660  LOAD_GLOBAL              list
              662  LOAD_GLOBAL              range
              664  LOAD_FAST                'ndmin'
              666  CALL_FUNCTION_1       1  ''
              668  CALL_FUNCTION_1       1  ''
              670  STORE_FAST               'defaxes'

 L. 395       672  LOAD_FAST                'defaxes'
              674  LOAD_CONST               None
              676  LOAD_FAST                'k1'
              678  BUILD_SLICE_2         2 
              680  BINARY_SUBSCR    
              682  LOAD_FAST                'defaxes'
              684  LOAD_FAST                'k2'
              686  LOAD_CONST               None
              688  BUILD_SLICE_2         2 
              690  BINARY_SUBSCR    
              692  BINARY_ADD       
              694  LOAD_FAST                'defaxes'
              696  LOAD_FAST                'k1'
              698  LOAD_FAST                'k2'
              700  BUILD_SLICE_2         2 
              702  BINARY_SUBSCR    
              704  BINARY_ADD       
              706  STORE_FAST               'axes'

 L. 396       708  LOAD_FAST                'newobj'
              710  LOAD_METHOD              transpose
              712  LOAD_FAST                'axes'
              714  CALL_METHOD_1         1  ''
              716  STORE_FAST               'newobj'
            718_0  COME_FROM           622  '622'
            718_1  COME_FROM           612  '612'
            718_2  COME_FROM           580  '580'
            718_3  COME_FROM           522  '522'
            718_4  COME_FROM           278  '278'
            718_5  COME_FROM           262  '262'
            718_6  COME_FROM           238  '238'

 L. 397       718  LOAD_FAST                'objs'
              720  LOAD_METHOD              append
              722  LOAD_FAST                'newobj'
              724  CALL_METHOD_1         1  ''
              726  POP_TOP          

 L. 398       728  LOAD_FAST                'scalar'
              730  POP_JUMP_IF_TRUE_BACK   106  'to 106'
              732  LOAD_GLOBAL              isinstance
              734  LOAD_FAST                'newobj'
              736  LOAD_GLOBAL              _nx
              738  LOAD_ATTR                ndarray
              740  CALL_FUNCTION_2       2  ''
              742  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 399       744  LOAD_FAST                'arraytypes'
              746  LOAD_METHOD              append
              748  LOAD_FAST                'newobj'
              750  LOAD_ATTR                dtype
              752  CALL_METHOD_1         1  ''
              754  POP_TOP          
              756  JUMP_BACK           106  'to 106'
            758_0  COME_FROM           106  '106'

 L. 402       758  LOAD_GLOBAL              find_common_type
              760  LOAD_FAST                'arraytypes'
              762  LOAD_FAST                'scalartypes'
              764  CALL_FUNCTION_2       2  ''
              766  STORE_FAST               'final_dtype'

 L. 403       768  LOAD_FAST                'final_dtype'
              770  LOAD_CONST               None
              772  COMPARE_OP               is-not
          774_776  POP_JUMP_IF_FALSE   808  'to 808'

 L. 404       778  LOAD_FAST                'scalars'
              780  GET_ITER         
            782_0  COME_FROM           804  '804'
              782  FOR_ITER            808  'to 808'
              784  STORE_FAST               'k'

 L. 405       786  LOAD_FAST                'objs'
              788  LOAD_FAST                'k'
              790  BINARY_SUBSCR    
              792  LOAD_METHOD              astype
              794  LOAD_FAST                'final_dtype'
              796  CALL_METHOD_1         1  ''
              798  LOAD_FAST                'objs'
              800  LOAD_FAST                'k'
              802  STORE_SUBSCR     
          804_806  JUMP_BACK           782  'to 782'
            808_0  COME_FROM           782  '782'
            808_1  COME_FROM           774  '774'

 L. 407       808  LOAD_FAST                'self'
              810  LOAD_ATTR                concatenate
              812  LOAD_GLOBAL              tuple
              814  LOAD_FAST                'objs'
              816  CALL_FUNCTION_1       1  ''
              818  LOAD_FAST                'axis'
              820  LOAD_CONST               ('axis',)
              822  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              824  STORE_FAST               'res'

 L. 409       826  LOAD_FAST                'matrix'
          828_830  POP_JUMP_IF_FALSE   870  'to 870'

 L. 410       832  LOAD_FAST                'res'
              834  LOAD_ATTR                ndim
              836  STORE_FAST               'oldndim'

 L. 411       838  LOAD_FAST                'self'
              840  LOAD_METHOD              makemat
              842  LOAD_FAST                'res'
              844  CALL_METHOD_1         1  ''
              846  STORE_FAST               'res'

 L. 412       848  LOAD_FAST                'oldndim'
              850  LOAD_CONST               1
              852  COMPARE_OP               ==
          854_856  POP_JUMP_IF_FALSE   870  'to 870'
              858  LOAD_FAST                'col'
          860_862  POP_JUMP_IF_FALSE   870  'to 870'

 L. 413       864  LOAD_FAST                'res'
              866  LOAD_ATTR                T
              868  STORE_FAST               'res'
            870_0  COME_FROM           860  '860'
            870_1  COME_FROM           854  '854'
            870_2  COME_FROM           828  '828'

 L. 414       870  LOAD_FAST                'res'
              872  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 414

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
    __doc__ = '\n    An N-dimensional iterator object to index arrays.\n\n    Given the shape of an array, an `ndindex` instance iterates over\n    the N-dimensional index of the array. At each iteration a tuple\n    of indices is returned, the last dimension is iterated over first.\n\n    Parameters\n    ----------\n    shape : ints, or a single tuple of ints\n        The size of each dimension of the array can be passed as \n        individual parameters or as the elements of a tuple.\n\n    See Also\n    --------\n    ndenumerate, flatiter\n\n    Examples\n    --------\n    # dimensions as individual arguments\n    >>> for index in np.ndindex(3, 2, 1):\n    ...     print(index)\n    (0, 0, 0)\n    (0, 1, 0)\n    (1, 0, 0)\n    (1, 1, 0)\n    (2, 0, 0)\n    (2, 1, 0)\n\n    # same dimensions - but in a tuple (3, 2, 1)\n    >>> for index in np.ndindex((3, 2, 1)):\n    ...     print(index)\n    (0, 0, 0)\n    (0, 1, 0)\n    (1, 0, 0)\n    (1, 1, 0)\n    (2, 0, 0)\n    (2, 1, 0)\n\n    '

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

        .. deprecated:: 1.20.0
            This method has been advised against since numpy 1.8.0, but only
            started emitting DeprecationWarning as of this version.
        """
        warnings.warn('`ndindex.ndincr()` is deprecated, use `next(ndindex)` instead',
          DeprecationWarning,
          stacklevel=2)
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

    val : scalar or array_like
      Value(s) to write on the diagonal. If `val` is scalar, the value is
      written along the diagonal. If array-like, the flattened `val` is
      written along the diagonal, repeating if necessary to fill all
      diagonal entries.

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

    See Also
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