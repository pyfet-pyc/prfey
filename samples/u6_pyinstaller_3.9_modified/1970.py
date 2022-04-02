# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\einsumfunc.py
"""
Implementation of optimized einsum.

"""
import itertools, operator
from numpy.core.multiarray import c_einsum
from numpy.core.numeric import asanyarray, tensordot
from numpy.core.overrides import array_function_dispatch
__all__ = [
 'einsum', 'einsum_path']
einsum_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
einsum_symbols_set = set(einsum_symbols)

def _flop_count(idx_contraction, inner, num_terms, size_dictionary):
    """
    Computes the number of FLOPS in the contraction.

    Parameters
    ----------
    idx_contraction : iterable
        The indices involved in the contraction
    inner : bool
        Does this contraction require an inner product?
    num_terms : int
        The number of terms in a contraction
    size_dictionary : dict
        The size of each of the indices in idx_contraction

    Returns
    -------
    flop_count : int
        The total number of FLOPS required for the contraction.

    Examples
    --------

    >>> _flop_count('abc', False, 1, {'a': 2, 'b':3, 'c':5})
    30

    >>> _flop_count('abc', True, 2, {'a': 2, 'b':3, 'c':5})
    60

    """
    overall_size = _compute_size_by_dict(idx_contraction, size_dictionary)
    op_factor = max(1, num_terms - 1)
    if inner:
        op_factor += 1
    return overall_size * op_factor


def _compute_size_by_dict(indices, idx_dict):
    """
    Computes the product of the elements in indices based on the dictionary
    idx_dict.

    Parameters
    ----------
    indices : iterable
        Indices to base the product on.
    idx_dict : dictionary
        Dictionary of index sizes

    Returns
    -------
    ret : int
        The resulting product.

    Examples
    --------
    >>> _compute_size_by_dict('abbc', {'a': 2, 'b':3, 'c':5})
    90

    """
    ret = 1
    for i in indices:
        ret *= idx_dict[i]
    else:
        return ret


def _find_contraction--- This code section failed: ---

 L. 128         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'idx_contract'

 L. 129         6  LOAD_FAST                'output_set'
                8  LOAD_METHOD              copy
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'idx_remain'

 L. 130        14  BUILD_LIST_0          0 
               16  STORE_FAST               'remaining'

 L. 131        18  LOAD_GLOBAL              enumerate
               20  LOAD_FAST                'input_sets'
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
               26  FOR_ITER             72  'to 72'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'ind'
               32  STORE_FAST               'value'

 L. 132        34  LOAD_FAST                'ind'
               36  LOAD_FAST                'positions'
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 133        42  LOAD_FAST                'idx_contract'
               44  LOAD_FAST                'value'
               46  INPLACE_OR       
               48  STORE_FAST               'idx_contract'
               50  JUMP_BACK            26  'to 26'
             52_0  COME_FROM            40  '40'

 L. 135        52  LOAD_FAST                'remaining'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'value'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L. 136        62  LOAD_FAST                'idx_remain'
               64  LOAD_FAST                'value'
               66  INPLACE_OR       
               68  STORE_FAST               'idx_remain'
               70  JUMP_BACK            26  'to 26'

 L. 138        72  LOAD_FAST                'idx_remain'
               74  LOAD_FAST                'idx_contract'
               76  BINARY_AND       
               78  STORE_FAST               'new_result'

 L. 139        80  LOAD_FAST                'idx_contract'
               82  LOAD_FAST                'new_result'
               84  BINARY_SUBTRACT  
               86  STORE_FAST               'idx_removed'

 L. 140        88  LOAD_FAST                'remaining'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'new_result'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 142        98  LOAD_FAST                'new_result'
              100  LOAD_FAST                'remaining'
              102  LOAD_FAST                'idx_removed'
              104  LOAD_FAST                'idx_contract'
              106  BUILD_TUPLE_4         4 
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 38


def _optimal_path(input_sets, output_set, idx_dict, memory_limit):
    """
    Computes all possible pair contractions, sieves the results based
    on ``memory_limit`` and returns the lowest cost path. This algorithm
    scales factorial with respect to the elements in the list ``input_sets``.

    Parameters
    ----------
    input_sets : list
        List of sets that represent the lhs side of the einsum subscript
    output_set : set
        Set that represents the rhs side of the overall einsum subscript
    idx_dict : dictionary
        Dictionary of index sizes
    memory_limit : int
        The maximum number of elements in a temporary array

    Returns
    -------
    path : list
        The optimal contraction order within the memory limit constraint.

    Examples
    --------
    >>> isets = [set('abd'), set('ac'), set('bdc')]
    >>> oset = set()
    >>> idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
    >>> _optimal_path(isets, oset, idx_sizes, 5000)
    [(0, 2), (0, 1)]
    """
    full_results = [
     (
      0, [], input_sets)]
    for iteration in range(len(input_sets) - 1):
        iter_results = []

    for curr in full_results:
        cost, positions, remaining = curr
        for con in itertools.combinations(range(len(input_sets) - iteration), 2):
            cont = _find_contraction(con, remaining, output_set)
            new_result, new_input_sets, idx_removed, idx_contract = cont
            new_size = _compute_size_by_dict(new_result, idx_dict)
            if new_size > memory_limit:
                pass
            else:
                total_cost = cost + _flop_count(idx_contract, idx_removed, len(con), idx_dict)
                new_pos = positions + [con]
                iter_results.append(total_cost, new_pos, new_input_sets)

        if iter_results:
            full_results = iter_results
        else:
            path = min(full_results, key=(lambda x: x[0]))[1]
            path += [tuple(range(len(input_sets) - iteration))]
            return path
    else:
        if len(full_results) == 0:
            return [
             tuple(range(len(input_sets)))]
        path = min(full_results, key=(lambda x: x[0]))[1]
        return path


def _parse_possible_contraction(positions, input_sets, output_set, idx_dict, memory_limit, path_cost, naive_cost):
    """Compute the cost (removed size + flops) and resultant indices for
    performing the contraction specified by ``positions``.

    Parameters
    ----------
    positions : tuple of int
        The locations of the proposed tensors to contract.
    input_sets : list of sets
        The indices found on each tensors.
    output_set : set
        The output indices of the expression.
    idx_dict : dict
        Mapping of each index to its size.
    memory_limit : int
        The total allowed size for an intermediary tensor.
    path_cost : int
        The contraction cost so far.
    naive_cost : int
        The cost of the unoptimized expression.

    Returns
    -------
    cost : (int, int)
        A tuple containing the size of any indices removed, and the flop cost.
    positions : tuple of int
        The locations of the proposed tensors to contract.
    new_input_sets : list of sets
        The resulting new list of indices if this proposed contraction is performed.

    """
    contract = _find_contraction(positions, input_sets, output_set)
    idx_result, new_input_sets, idx_removed, idx_contract = contract
    new_size = _compute_size_by_dict(idx_result, idx_dict)
    if new_size > memory_limit:
        return
    old_sizes = (_compute_size_by_dict(input_sets[p], idx_dict) for p in positions)
    removed_size = sum(old_sizes) - new_size
    cost = _flop_count(idx_contract, idx_removed, len(positions), idx_dict)
    sort = (-removed_size, cost)
    if path_cost + cost > naive_cost:
        return
    return [sort, positions, new_input_sets]


def _update_other_results--- This code section failed: ---

 L. 291         0  LOAD_FAST                'best'
                2  LOAD_CONST               1
                4  BINARY_SUBSCR    
                6  STORE_FAST               'best_con'

 L. 292         8  LOAD_FAST                'best_con'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'bx'
               14  STORE_FAST               'by'

 L. 293        16  BUILD_LIST_0          0 
               18  STORE_FAST               'mod_results'

 L. 295        20  LOAD_FAST                'results'
               22  GET_ITER         
             24_0  COME_FROM            44  '44'
               24  FOR_ITER            210  'to 210'
               26  UNPACK_SEQUENCE_3     3 
               28  STORE_FAST               'cost'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'x'
               34  STORE_FAST               'y'
               36  STORE_FAST               'con_sets'

 L. 298        38  LOAD_FAST                'x'
               40  LOAD_FAST                'best_con'
               42  <118>                 0  ''
               44  POP_JUMP_IF_TRUE     24  'to 24'
               46  LOAD_FAST                'y'
               48  LOAD_FAST                'best_con'
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L. 299        54  JUMP_BACK            24  'to 24'
             56_0  COME_FROM            52  '52'

 L. 302        56  LOAD_FAST                'con_sets'
               58  LOAD_FAST                'by'
               60  LOAD_GLOBAL              int
               62  LOAD_FAST                'by'
               64  LOAD_FAST                'x'
               66  COMPARE_OP               >
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_SUBTRACT  
               72  LOAD_GLOBAL              int
               74  LOAD_FAST                'by'
               76  LOAD_FAST                'y'
               78  COMPARE_OP               >
               80  CALL_FUNCTION_1       1  ''
               82  BINARY_SUBTRACT  
               84  DELETE_SUBSCR    

 L. 303        86  LOAD_FAST                'con_sets'
               88  LOAD_FAST                'bx'
               90  LOAD_GLOBAL              int
               92  LOAD_FAST                'bx'
               94  LOAD_FAST                'x'
               96  COMPARE_OP               >
               98  CALL_FUNCTION_1       1  ''
              100  BINARY_SUBTRACT  
              102  LOAD_GLOBAL              int
              104  LOAD_FAST                'bx'
              106  LOAD_FAST                'y'
              108  COMPARE_OP               >
              110  CALL_FUNCTION_1       1  ''
              112  BINARY_SUBTRACT  
              114  DELETE_SUBSCR    

 L. 304       116  LOAD_FAST                'con_sets'
              118  LOAD_METHOD              insert
              120  LOAD_CONST               -1
              122  LOAD_FAST                'best'
              124  LOAD_CONST               2
              126  BINARY_SUBSCR    
              128  LOAD_CONST               -1
              130  BINARY_SUBSCR    
              132  CALL_METHOD_2         2  ''
              134  POP_TOP          

 L. 307       136  LOAD_FAST                'x'
              138  LOAD_GLOBAL              int
              140  LOAD_FAST                'x'
              142  LOAD_FAST                'bx'
              144  COMPARE_OP               >
              146  CALL_FUNCTION_1       1  ''
              148  BINARY_SUBTRACT  
              150  LOAD_GLOBAL              int
              152  LOAD_FAST                'x'
              154  LOAD_FAST                'by'
              156  COMPARE_OP               >
              158  CALL_FUNCTION_1       1  ''
              160  BINARY_SUBTRACT  
              162  LOAD_FAST                'y'
              164  LOAD_GLOBAL              int
              166  LOAD_FAST                'y'
              168  LOAD_FAST                'bx'
              170  COMPARE_OP               >
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_SUBTRACT  
              176  LOAD_GLOBAL              int
              178  LOAD_FAST                'y'
              180  LOAD_FAST                'by'
              182  COMPARE_OP               >
              184  CALL_FUNCTION_1       1  ''
              186  BINARY_SUBTRACT  
              188  BUILD_TUPLE_2         2 
              190  STORE_FAST               'mod_con'

 L. 308       192  LOAD_FAST                'mod_results'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'cost'
              198  LOAD_FAST                'mod_con'
              200  LOAD_FAST                'con_sets'
              202  BUILD_TUPLE_3         3 
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
              208  JUMP_BACK            24  'to 24'

 L. 310       210  LOAD_FAST                'mod_results'
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 42


def _greedy_path--- This code section failed: ---

 L. 348         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'input_sets'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    18  'to 18'

 L. 349        12  LOAD_CONST               (0,)
               14  BUILD_LIST_1          1 
               16  RETURN_VALUE     
             18_0  COME_FROM            10  '10'

 L. 350        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'input_sets'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               2
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    36  'to 36'

 L. 351        30  LOAD_CONST               (0, 1)
               32  BUILD_LIST_1          1 
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'

 L. 354        36  LOAD_GLOBAL              _find_contraction
               38  LOAD_GLOBAL              range
               40  LOAD_GLOBAL              len
               42  LOAD_FAST                'input_sets'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'input_sets'
               50  LOAD_FAST                'output_set'
               52  CALL_FUNCTION_3       3  ''
               54  STORE_FAST               'contract'

 L. 355        56  LOAD_FAST                'contract'
               58  UNPACK_SEQUENCE_4     4 
               60  STORE_FAST               'idx_result'
               62  STORE_FAST               'new_input_sets'
               64  STORE_FAST               'idx_removed'
               66  STORE_FAST               'idx_contract'

 L. 356        68  LOAD_GLOBAL              _flop_count
               70  LOAD_FAST                'idx_contract'
               72  LOAD_FAST                'idx_removed'
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'input_sets'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'idx_dict'
               82  CALL_FUNCTION_4       4  ''
               84  STORE_FAST               'naive_cost'

 L. 359        86  LOAD_GLOBAL              itertools
               88  LOAD_METHOD              combinations
               90  LOAD_GLOBAL              range
               92  LOAD_GLOBAL              len
               94  LOAD_FAST                'input_sets'
               96  CALL_FUNCTION_1       1  ''
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               2
              102  CALL_METHOD_2         2  ''
              104  STORE_FAST               'comb_iter'

 L. 360       106  BUILD_LIST_0          0 
              108  STORE_FAST               'known_contractions'

 L. 362       110  LOAD_CONST               0
              112  STORE_FAST               'path_cost'

 L. 363       114  BUILD_LIST_0          0 
              116  STORE_FAST               'path'

 L. 365       118  LOAD_GLOBAL              range
              120  LOAD_GLOBAL              len
              122  LOAD_FAST                'input_sets'
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_CONST               1
              128  BINARY_SUBTRACT  
              130  CALL_FUNCTION_1       1  ''
              132  GET_ITER         
          134_136  FOR_ITER            436  'to 436'
              138  STORE_FAST               'iteration'

 L. 368       140  LOAD_FAST                'comb_iter'
              142  GET_ITER         
            144_0  COME_FROM           202  '202'
              144  FOR_ITER            216  'to 216'
              146  STORE_FAST               'positions'

 L. 371       148  LOAD_FAST                'input_sets'
              150  LOAD_FAST                'positions'
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              isdisjoint
              160  LOAD_FAST                'input_sets'
              162  LOAD_FAST                'positions'
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    
              168  BINARY_SUBSCR    
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   176  'to 176'

 L. 372       174  JUMP_BACK           144  'to 144'
            176_0  COME_FROM           172  '172'

 L. 374       176  LOAD_GLOBAL              _parse_possible_contraction
              178  LOAD_FAST                'positions'
              180  LOAD_FAST                'input_sets'
              182  LOAD_FAST                'output_set'
              184  LOAD_FAST                'idx_dict'
              186  LOAD_FAST                'memory_limit'
              188  LOAD_FAST                'path_cost'

 L. 375       190  LOAD_FAST                'naive_cost'

 L. 374       192  CALL_FUNCTION_7       7  ''
              194  STORE_FAST               'result'

 L. 376       196  LOAD_FAST                'result'
              198  LOAD_CONST               None
              200  <117>                 1  ''
              202  POP_JUMP_IF_FALSE   144  'to 144'

 L. 377       204  LOAD_FAST                'known_contractions'
              206  LOAD_METHOD              append
              208  LOAD_FAST                'result'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
              214  JUMP_BACK           144  'to 144'

 L. 380       216  LOAD_GLOBAL              len
              218  LOAD_FAST                'known_contractions'
              220  CALL_FUNCTION_1       1  ''
              222  LOAD_CONST               0
              224  COMPARE_OP               ==
          226_228  POP_JUMP_IF_FALSE   336  'to 336'

 L. 383       230  LOAD_GLOBAL              itertools
              232  LOAD_METHOD              combinations
              234  LOAD_GLOBAL              range
              236  LOAD_GLOBAL              len
              238  LOAD_FAST                'input_sets'
              240  CALL_FUNCTION_1       1  ''
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               2
              246  CALL_METHOD_2         2  ''
              248  GET_ITER         
            250_0  COME_FROM           280  '280'
              250  FOR_ITER            294  'to 294'
              252  STORE_FAST               'positions'

 L. 384       254  LOAD_GLOBAL              _parse_possible_contraction
              256  LOAD_FAST                'positions'
              258  LOAD_FAST                'input_sets'
              260  LOAD_FAST                'output_set'
              262  LOAD_FAST                'idx_dict'
              264  LOAD_FAST                'memory_limit'

 L. 385       266  LOAD_FAST                'path_cost'
              268  LOAD_FAST                'naive_cost'

 L. 384       270  CALL_FUNCTION_7       7  ''
              272  STORE_FAST               'result'

 L. 386       274  LOAD_FAST                'result'
              276  LOAD_CONST               None
              278  <117>                 1  ''
              280  POP_JUMP_IF_FALSE   250  'to 250'

 L. 387       282  LOAD_FAST                'known_contractions'
              284  LOAD_METHOD              append
              286  LOAD_FAST                'result'
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          
              292  JUMP_BACK           250  'to 250'

 L. 390       294  LOAD_GLOBAL              len
              296  LOAD_FAST                'known_contractions'
              298  CALL_FUNCTION_1       1  ''
              300  LOAD_CONST               0
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   336  'to 336'

 L. 391       308  LOAD_FAST                'path'
              310  LOAD_METHOD              append
              312  LOAD_GLOBAL              tuple
              314  LOAD_GLOBAL              range
              316  LOAD_GLOBAL              len
              318  LOAD_FAST                'input_sets'
              320  CALL_FUNCTION_1       1  ''
              322  CALL_FUNCTION_1       1  ''
              324  CALL_FUNCTION_1       1  ''
              326  CALL_METHOD_1         1  ''
              328  POP_TOP          

 L. 392       330  POP_TOP          
          332_334  JUMP_ABSOLUTE       436  'to 436'
            336_0  COME_FROM           304  '304'
            336_1  COME_FROM           226  '226'

 L. 395       336  LOAD_GLOBAL              min
              338  LOAD_FAST                'known_contractions'
              340  LOAD_LAMBDA              '<code_object <lambda>>'
              342  LOAD_STR                 '_greedy_path.<locals>.<lambda>'
              344  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              346  LOAD_CONST               ('key',)
              348  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              350  STORE_FAST               'best'

 L. 398       352  LOAD_GLOBAL              _update_other_results
              354  LOAD_FAST                'known_contractions'
              356  LOAD_FAST                'best'
              358  CALL_FUNCTION_2       2  ''
              360  STORE_FAST               'known_contractions'

 L. 402       362  LOAD_FAST                'best'
              364  LOAD_CONST               2
              366  BINARY_SUBSCR    
              368  STORE_FAST               'input_sets'

 L. 403       370  LOAD_GLOBAL              len
              372  LOAD_FAST                'input_sets'
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_CONST               1
              378  BINARY_SUBTRACT  
              380  STORE_DEREF              'new_tensor_pos'

 L. 404       382  LOAD_CLOSURE             'new_tensor_pos'
              384  BUILD_TUPLE_1         1 
              386  LOAD_GENEXPR             '<code_object <genexpr>>'
              388  LOAD_STR                 '_greedy_path.<locals>.<genexpr>'
              390  MAKE_FUNCTION_8          'closure'
              392  LOAD_GLOBAL              range
              394  LOAD_DEREF               'new_tensor_pos'
              396  CALL_FUNCTION_1       1  ''
              398  GET_ITER         
              400  CALL_FUNCTION_1       1  ''
              402  STORE_FAST               'comb_iter'

 L. 407       404  LOAD_FAST                'path'
              406  LOAD_METHOD              append
              408  LOAD_FAST                'best'
              410  LOAD_CONST               1
              412  BINARY_SUBSCR    
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          

 L. 408       418  LOAD_FAST                'path_cost'
              420  LOAD_FAST                'best'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_CONST               1
              428  BINARY_SUBSCR    
              430  INPLACE_ADD      
              432  STORE_FAST               'path_cost'
              434  JUMP_BACK           134  'to 134'

 L. 410       436  LOAD_FAST                'path'
              438  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 200


def _can_dot--- This code section failed: ---

 L. 457         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'idx_removed'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 458        12  LOAD_CONST               False
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 461        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'inputs'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_CONST               2
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 462        28  LOAD_CONST               False
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 464        32  LOAD_FAST                'inputs'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'input_left'
               38  STORE_FAST               'input_right'

 L. 466        40  LOAD_GLOBAL              set
               42  LOAD_FAST                'input_left'
               44  LOAD_FAST                'input_right'
               46  BINARY_ADD       
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
             52_0  COME_FROM           134  '134'
               52  FOR_ITER            144  'to 144'
               54  STORE_FAST               'c'

 L. 468        56  LOAD_FAST                'input_left'
               58  LOAD_METHOD              count
               60  LOAD_FAST                'c'
               62  CALL_METHOD_1         1  ''
               64  LOAD_FAST                'input_right'
               66  LOAD_METHOD              count
               68  LOAD_FAST                'c'
               70  CALL_METHOD_1         1  ''
               72  ROT_TWO          
               74  STORE_FAST               'nl'
               76  STORE_FAST               'nr'

 L. 469        78  LOAD_FAST                'nl'
               80  LOAD_CONST               1
               82  COMPARE_OP               >
               84  POP_JUMP_IF_TRUE    106  'to 106'
               86  LOAD_FAST                'nr'
               88  LOAD_CONST               1
               90  COMPARE_OP               >
               92  POP_JUMP_IF_TRUE    106  'to 106'
               94  LOAD_FAST                'nl'
               96  LOAD_FAST                'nr'
               98  BINARY_ADD       
              100  LOAD_CONST               2
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   112  'to 112'
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            84  '84'

 L. 470       106  POP_TOP          
              108  LOAD_CONST               False
              110  RETURN_VALUE     
            112_0  COME_FROM           104  '104'

 L. 475       112  LOAD_FAST                'nl'
              114  LOAD_FAST                'nr'
              116  BINARY_ADD       
              118  LOAD_CONST               1
              120  BINARY_SUBTRACT  
              122  LOAD_GLOBAL              int
              124  LOAD_FAST                'c'
              126  LOAD_FAST                'result'
              128  <118>                 0  ''
              130  CALL_FUNCTION_1       1  ''
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE    52  'to 52'

 L. 476       136  POP_TOP          
              138  LOAD_CONST               False
              140  RETURN_VALUE     
              142  JUMP_BACK            52  'to 52'

 L. 479       144  LOAD_GLOBAL              set
              146  LOAD_FAST                'input_left'
              148  CALL_FUNCTION_1       1  ''
              150  STORE_FAST               'set_left'

 L. 480       152  LOAD_GLOBAL              set
              154  LOAD_FAST                'input_right'
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'set_right'

 L. 481       160  LOAD_FAST                'set_left'
              162  LOAD_FAST                'idx_removed'
              164  BINARY_SUBTRACT  
              166  STORE_FAST               'keep_left'

 L. 482       168  LOAD_FAST                'set_right'
              170  LOAD_FAST                'idx_removed'
              172  BINARY_SUBTRACT  
              174  STORE_FAST               'keep_right'

 L. 483       176  LOAD_GLOBAL              len
              178  LOAD_FAST                'idx_removed'
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'rs'

 L. 490       184  LOAD_FAST                'input_left'
              186  LOAD_FAST                'input_right'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   196  'to 196'

 L. 491       192  LOAD_CONST               True
              194  RETURN_VALUE     
            196_0  COME_FROM           190  '190'

 L. 494       196  LOAD_FAST                'set_left'
              198  LOAD_FAST                'set_right'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   208  'to 208'

 L. 495       204  LOAD_CONST               False
              206  RETURN_VALUE     
            208_0  COME_FROM           202  '202'

 L. 500       208  LOAD_FAST                'input_left'
              210  LOAD_FAST                'rs'
              212  UNARY_NEGATIVE   
              214  LOAD_CONST               None
              216  BUILD_SLICE_2         2 
              218  BINARY_SUBSCR    
              220  LOAD_FAST                'input_right'
              222  LOAD_CONST               None
              224  LOAD_FAST                'rs'
              226  BUILD_SLICE_2         2 
              228  BINARY_SUBSCR    
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   238  'to 238'

 L. 501       234  LOAD_CONST               True
              236  RETURN_VALUE     
            238_0  COME_FROM           232  '232'

 L. 504       238  LOAD_FAST                'input_left'
              240  LOAD_CONST               None
              242  LOAD_FAST                'rs'
              244  BUILD_SLICE_2         2 
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'input_right'
              250  LOAD_FAST                'rs'
              252  UNARY_NEGATIVE   
              254  LOAD_CONST               None
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   270  'to 270'

 L. 505       266  LOAD_CONST               True
              268  RETURN_VALUE     
            270_0  COME_FROM           262  '262'

 L. 508       270  LOAD_FAST                'input_left'
              272  LOAD_FAST                'rs'
              274  UNARY_NEGATIVE   
              276  LOAD_CONST               None
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'input_right'
              284  LOAD_FAST                'rs'
              286  UNARY_NEGATIVE   
              288  LOAD_CONST               None
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   304  'to 304'

 L. 509       300  LOAD_CONST               True
              302  RETURN_VALUE     
            304_0  COME_FROM           296  '296'

 L. 512       304  LOAD_FAST                'input_left'
              306  LOAD_CONST               None
              308  LOAD_FAST                'rs'
              310  BUILD_SLICE_2         2 
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'input_right'
              316  LOAD_CONST               None
              318  LOAD_FAST                'rs'
              320  BUILD_SLICE_2         2 
              322  BINARY_SUBSCR    
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   334  'to 334'

 L. 513       330  LOAD_CONST               True
              332  RETURN_VALUE     
            334_0  COME_FROM           326  '326'

 L. 516       334  LOAD_FAST                'keep_left'
          336_338  POP_JUMP_IF_FALSE   346  'to 346'
              340  LOAD_FAST                'keep_right'
          342_344  POP_JUMP_IF_TRUE    350  'to 350'
            346_0  COME_FROM           336  '336'

 L. 517       346  LOAD_CONST               False
              348  RETURN_VALUE     
            350_0  COME_FROM           342  '342'

 L. 520       350  LOAD_CONST               True
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 128


def _parse_einsum_input--- This code section failed: ---

 L. 550         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'operands'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 551        12  LOAD_GLOBAL              ValueError
               14  LOAD_STR                 'No input operands'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L. 553        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'operands'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  LOAD_GLOBAL              str
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE   116  'to 116'

 L. 554        34  LOAD_FAST                'operands'
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              replace
               42  LOAD_STR                 ' '
               44  LOAD_STR                 ''
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'subscripts'

 L. 555        50  LOAD_LISTCOMP            '<code_object <listcomp>>'
               52  LOAD_STR                 '_parse_einsum_input.<locals>.<listcomp>'
               54  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               56  LOAD_FAST                'operands'
               58  LOAD_CONST               1
               60  LOAD_CONST               None
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'operands'

 L. 558        72  LOAD_FAST                'subscripts'
               74  GET_ITER         
             76_0  COME_FROM            96  '96'
               76  FOR_ITER            112  'to 112'
               78  STORE_FAST               's'

 L. 559        80  LOAD_FAST                's'
               82  LOAD_STR                 '.,->'
               84  <118>                 0  ''
               86  POP_JUMP_IF_FALSE    90  'to 90'

 L. 560        88  JUMP_BACK            76  'to 76'
             90_0  COME_FROM            86  '86'

 L. 561        90  LOAD_FAST                's'
               92  LOAD_GLOBAL              einsum_symbols
               94  <118>                 1  ''
               96  POP_JUMP_IF_FALSE    76  'to 76'

 L. 562        98  LOAD_GLOBAL              ValueError
              100  LOAD_STR                 'Character %s is not a valid symbol.'
              102  LOAD_FAST                's'
              104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
              110  JUMP_BACK            76  'to 76'
          112_114  JUMP_FORWARD        504  'to 504'
            116_0  COME_FROM            32  '32'

 L. 565       116  LOAD_GLOBAL              list
              118  LOAD_FAST                'operands'
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'tmp_operands'

 L. 566       124  BUILD_LIST_0          0 
              126  STORE_FAST               'operand_list'

 L. 567       128  BUILD_LIST_0          0 
              130  STORE_FAST               'subscript_list'

 L. 568       132  LOAD_GLOBAL              range
              134  LOAD_GLOBAL              len
              136  LOAD_FAST                'operands'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_CONST               2
              142  BINARY_FLOOR_DIVIDE
              144  CALL_FUNCTION_1       1  ''
              146  GET_ITER         
              148  FOR_ITER            186  'to 186'
              150  STORE_FAST               'p'

 L. 569       152  LOAD_FAST                'operand_list'
              154  LOAD_METHOD              append
              156  LOAD_FAST                'tmp_operands'
              158  LOAD_METHOD              pop
              160  LOAD_CONST               0
              162  CALL_METHOD_1         1  ''
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 570       168  LOAD_FAST                'subscript_list'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'tmp_operands'
              174  LOAD_METHOD              pop
              176  LOAD_CONST               0
              178  CALL_METHOD_1         1  ''
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK           148  'to 148'

 L. 572       186  LOAD_GLOBAL              len
              188  LOAD_FAST                'tmp_operands'
              190  CALL_FUNCTION_1       1  ''
              192  POP_JUMP_IF_FALSE   202  'to 202'
              194  LOAD_FAST                'tmp_operands'
              196  LOAD_CONST               -1
              198  BINARY_SUBSCR    
              200  JUMP_FORWARD        204  'to 204'
            202_0  COME_FROM           192  '192'
              202  LOAD_CONST               None
            204_0  COME_FROM           200  '200'
              204  STORE_FAST               'output_list'

 L. 573       206  LOAD_LISTCOMP            '<code_object <listcomp>>'
              208  LOAD_STR                 '_parse_einsum_input.<locals>.<listcomp>'
              210  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              212  LOAD_FAST                'operand_list'
              214  GET_ITER         
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'operands'

 L. 574       220  LOAD_STR                 ''
              222  STORE_FAST               'subscripts'

 L. 575       224  LOAD_GLOBAL              len
              226  LOAD_FAST                'subscript_list'
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_CONST               1
              232  BINARY_SUBTRACT  
              234  STORE_FAST               'last'

 L. 576       236  LOAD_GLOBAL              enumerate
              238  LOAD_FAST                'subscript_list'
              240  CALL_FUNCTION_1       1  ''
              242  GET_ITER         
            244_0  COME_FROM           366  '366'
              244  FOR_ITER            378  'to 378'
              246  UNPACK_SEQUENCE_2     2 
              248  STORE_FAST               'num'
              250  STORE_FAST               'sub'

 L. 577       252  LOAD_FAST                'sub'
              254  GET_ITER         
              256  FOR_ITER            360  'to 360'
              258  STORE_FAST               's'

 L. 578       260  LOAD_FAST                's'
              262  LOAD_GLOBAL              Ellipsis
              264  <117>                 0  ''
          266_268  POP_JUMP_IF_FALSE   280  'to 280'

 L. 579       270  LOAD_FAST                'subscripts'
              272  LOAD_STR                 '...'
              274  INPLACE_ADD      
              276  STORE_FAST               'subscripts'
              278  JUMP_BACK           256  'to 256'
            280_0  COME_FROM           266  '266'

 L. 581       280  SETUP_FINALLY       296  'to 296'

 L. 582       282  LOAD_GLOBAL              operator
              284  LOAD_METHOD              index
              286  LOAD_FAST                's'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               's'
              292  POP_BLOCK        
              294  JUMP_FORWARD        344  'to 344'
            296_0  COME_FROM_FINALLY   280  '280'

 L. 583       296  DUP_TOP          
              298  LOAD_GLOBAL              TypeError
          300_302  <121>               342  ''
              304  POP_TOP          
              306  STORE_FAST               'e'
              308  POP_TOP          
              310  SETUP_FINALLY       334  'to 334'

 L. 584       312  LOAD_GLOBAL              TypeError
              314  LOAD_STR                 'For this input type lists must contain either int or Ellipsis'
              316  CALL_FUNCTION_1       1  ''

 L. 585       318  LOAD_FAST                'e'

 L. 584       320  RAISE_VARARGS_2       2  'exception instance with __cause__'
              322  POP_BLOCK        
              324  POP_EXCEPT       
              326  LOAD_CONST               None
              328  STORE_FAST               'e'
              330  DELETE_FAST              'e'
              332  JUMP_FORWARD        344  'to 344'
            334_0  COME_FROM_FINALLY   310  '310'
              334  LOAD_CONST               None
              336  STORE_FAST               'e'
              338  DELETE_FAST              'e'
              340  <48>             
              342  <48>             
            344_0  COME_FROM           332  '332'
            344_1  COME_FROM           294  '294'

 L. 586       344  LOAD_FAST                'subscripts'
              346  LOAD_GLOBAL              einsum_symbols
              348  LOAD_FAST                's'
              350  BINARY_SUBSCR    
              352  INPLACE_ADD      
              354  STORE_FAST               'subscripts'
          356_358  JUMP_BACK           256  'to 256'

 L. 587       360  LOAD_FAST                'num'
              362  LOAD_FAST                'last'
              364  COMPARE_OP               !=
              366  POP_JUMP_IF_FALSE   244  'to 244'

 L. 588       368  LOAD_FAST                'subscripts'
              370  LOAD_STR                 ','
              372  INPLACE_ADD      
              374  STORE_FAST               'subscripts'
              376  JUMP_BACK           244  'to 244'

 L. 590       378  LOAD_FAST                'output_list'
              380  LOAD_CONST               None
              382  <117>                 1  ''
          384_386  POP_JUMP_IF_FALSE   504  'to 504'

 L. 591       388  LOAD_FAST                'subscripts'
              390  LOAD_STR                 '->'
              392  INPLACE_ADD      
              394  STORE_FAST               'subscripts'

 L. 592       396  LOAD_FAST                'output_list'
              398  GET_ITER         
              400  FOR_ITER            504  'to 504'
              402  STORE_FAST               's'

 L. 593       404  LOAD_FAST                's'
              406  LOAD_GLOBAL              Ellipsis
              408  <117>                 0  ''
          410_412  POP_JUMP_IF_FALSE   424  'to 424'

 L. 594       414  LOAD_FAST                'subscripts'
              416  LOAD_STR                 '...'
              418  INPLACE_ADD      
              420  STORE_FAST               'subscripts'
              422  JUMP_BACK           400  'to 400'
            424_0  COME_FROM           410  '410'

 L. 596       424  SETUP_FINALLY       440  'to 440'

 L. 597       426  LOAD_GLOBAL              operator
              428  LOAD_METHOD              index
              430  LOAD_FAST                's'
              432  CALL_METHOD_1         1  ''
              434  STORE_FAST               's'
              436  POP_BLOCK        
              438  JUMP_FORWARD        488  'to 488'
            440_0  COME_FROM_FINALLY   424  '424'

 L. 598       440  DUP_TOP          
              442  LOAD_GLOBAL              TypeError
          444_446  <121>               486  ''
              448  POP_TOP          
              450  STORE_FAST               'e'
              452  POP_TOP          
              454  SETUP_FINALLY       478  'to 478'

 L. 599       456  LOAD_GLOBAL              TypeError
              458  LOAD_STR                 'For this input type lists must contain either int or Ellipsis'
              460  CALL_FUNCTION_1       1  ''

 L. 600       462  LOAD_FAST                'e'

 L. 599       464  RAISE_VARARGS_2       2  'exception instance with __cause__'
              466  POP_BLOCK        
              468  POP_EXCEPT       
              470  LOAD_CONST               None
              472  STORE_FAST               'e'
              474  DELETE_FAST              'e'
              476  JUMP_FORWARD        488  'to 488'
            478_0  COME_FROM_FINALLY   454  '454'
              478  LOAD_CONST               None
              480  STORE_FAST               'e'
              482  DELETE_FAST              'e'
              484  <48>             
              486  <48>             
            488_0  COME_FROM           476  '476'
            488_1  COME_FROM           438  '438'

 L. 601       488  LOAD_FAST                'subscripts'
              490  LOAD_GLOBAL              einsum_symbols
              492  LOAD_FAST                's'
              494  BINARY_SUBSCR    
              496  INPLACE_ADD      
              498  STORE_FAST               'subscripts'
          500_502  JUMP_BACK           400  'to 400'
            504_0  COME_FROM           384  '384'
            504_1  COME_FROM           112  '112'

 L. 603       504  LOAD_STR                 '-'
              506  LOAD_FAST                'subscripts'
              508  <118>                 0  ''
          510_512  POP_JUMP_IF_TRUE    524  'to 524'
              514  LOAD_STR                 '>'
              516  LOAD_FAST                'subscripts'
              518  <118>                 0  ''
          520_522  POP_JUMP_IF_FALSE   584  'to 584'
            524_0  COME_FROM           510  '510'

 L. 604       524  LOAD_FAST                'subscripts'
              526  LOAD_METHOD              count
              528  LOAD_STR                 '-'
              530  CALL_METHOD_1         1  ''
              532  LOAD_CONST               1
              534  COMPARE_OP               >
          536_538  JUMP_IF_TRUE_OR_POP   552  'to 552'
              540  LOAD_FAST                'subscripts'
              542  LOAD_METHOD              count
              544  LOAD_STR                 '>'
              546  CALL_METHOD_1         1  ''
              548  LOAD_CONST               1
              550  COMPARE_OP               >
            552_0  COME_FROM           536  '536'
              552  STORE_FAST               'invalid'

 L. 605       554  LOAD_FAST                'invalid'
          556_558  POP_JUMP_IF_TRUE    576  'to 576'
              560  LOAD_FAST                'subscripts'
              562  LOAD_METHOD              count
              564  LOAD_STR                 '->'
              566  CALL_METHOD_1         1  ''
              568  LOAD_CONST               1
              570  COMPARE_OP               !=
          572_574  POP_JUMP_IF_FALSE   584  'to 584'
            576_0  COME_FROM           556  '556'

 L. 606       576  LOAD_GLOBAL              ValueError
              578  LOAD_STR                 "Subscripts can only contain one '->'."
              580  CALL_FUNCTION_1       1  ''
              582  RAISE_VARARGS_1       1  'exception instance'
            584_0  COME_FROM           572  '572'
            584_1  COME_FROM           520  '520'

 L. 609       584  LOAD_STR                 '.'
              586  LOAD_FAST                'subscripts'
              588  <118>                 0  ''
          590_592  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 610       594  LOAD_FAST                'subscripts'
              596  LOAD_METHOD              replace
              598  LOAD_STR                 '.'
              600  LOAD_STR                 ''
              602  CALL_METHOD_2         2  ''
              604  LOAD_METHOD              replace
              606  LOAD_STR                 ','
              608  LOAD_STR                 ''
              610  CALL_METHOD_2         2  ''
              612  LOAD_METHOD              replace
              614  LOAD_STR                 '->'
              616  LOAD_STR                 ''
              618  CALL_METHOD_2         2  ''
              620  STORE_FAST               'used'

 L. 611       622  LOAD_GLOBAL              list
              624  LOAD_GLOBAL              einsum_symbols_set
              626  LOAD_GLOBAL              set
              628  LOAD_FAST                'used'
              630  CALL_FUNCTION_1       1  ''
              632  BINARY_SUBTRACT  
              634  CALL_FUNCTION_1       1  ''
              636  STORE_FAST               'unused'

 L. 612       638  LOAD_STR                 ''
              640  LOAD_METHOD              join
              642  LOAD_FAST                'unused'
              644  CALL_METHOD_1         1  ''
              646  STORE_FAST               'ellipse_inds'

 L. 613       648  LOAD_CONST               0
              650  STORE_FAST               'longest'

 L. 615       652  LOAD_STR                 '->'
              654  LOAD_FAST                'subscripts'
              656  <118>                 0  ''
          658_660  POP_JUMP_IF_FALSE   692  'to 692'

 L. 616       662  LOAD_FAST                'subscripts'
              664  LOAD_METHOD              split
              666  LOAD_STR                 '->'
              668  CALL_METHOD_1         1  ''
              670  UNPACK_SEQUENCE_2     2 
              672  STORE_FAST               'input_tmp'
              674  STORE_FAST               'output_sub'

 L. 617       676  LOAD_FAST                'input_tmp'
              678  LOAD_METHOD              split
              680  LOAD_STR                 ','
              682  CALL_METHOD_1         1  ''
              684  STORE_FAST               'split_subscripts'

 L. 618       686  LOAD_CONST               True
              688  STORE_FAST               'out_sub'
              690  JUMP_FORWARD        706  'to 706'
            692_0  COME_FROM           658  '658'

 L. 620       692  LOAD_FAST                'subscripts'
              694  LOAD_METHOD              split
              696  LOAD_STR                 ','
              698  CALL_METHOD_1         1  ''
              700  STORE_FAST               'split_subscripts'

 L. 621       702  LOAD_CONST               False
              704  STORE_FAST               'out_sub'
            706_0  COME_FROM           690  '690'

 L. 623       706  LOAD_GLOBAL              enumerate
              708  LOAD_FAST                'split_subscripts'
              710  CALL_FUNCTION_1       1  ''
              712  GET_ITER         
            714_0  COME_FROM           728  '728'
              714  FOR_ITER            922  'to 922'
              716  UNPACK_SEQUENCE_2     2 
              718  STORE_FAST               'num'
              720  STORE_FAST               'sub'

 L. 624       722  LOAD_STR                 '.'
              724  LOAD_FAST                'sub'
              726  <118>                 0  ''
          728_730  POP_JUMP_IF_FALSE   714  'to 714'

 L. 625       732  LOAD_FAST                'sub'
              734  LOAD_METHOD              count
              736  LOAD_STR                 '.'
              738  CALL_METHOD_1         1  ''
              740  LOAD_CONST               3
              742  COMPARE_OP               !=
          744_746  POP_JUMP_IF_TRUE    764  'to 764'
              748  LOAD_FAST                'sub'
              750  LOAD_METHOD              count
              752  LOAD_STR                 '...'
              754  CALL_METHOD_1         1  ''
              756  LOAD_CONST               1
              758  COMPARE_OP               !=
          760_762  POP_JUMP_IF_FALSE   772  'to 772'
            764_0  COME_FROM           744  '744'

 L. 626       764  LOAD_GLOBAL              ValueError
              766  LOAD_STR                 'Invalid Ellipses.'
              768  CALL_FUNCTION_1       1  ''
              770  RAISE_VARARGS_1       1  'exception instance'
            772_0  COME_FROM           760  '760'

 L. 629       772  LOAD_FAST                'operands'
              774  LOAD_FAST                'num'
              776  BINARY_SUBSCR    
              778  LOAD_ATTR                shape
              780  LOAD_CONST               ()
              782  COMPARE_OP               ==
          784_786  POP_JUMP_IF_FALSE   794  'to 794'

 L. 630       788  LOAD_CONST               0
              790  STORE_FAST               'ellipse_count'
              792  JUMP_FORWARD        826  'to 826'
            794_0  COME_FROM           784  '784'

 L. 632       794  LOAD_GLOBAL              max
              796  LOAD_FAST                'operands'
              798  LOAD_FAST                'num'
              800  BINARY_SUBSCR    
              802  LOAD_ATTR                ndim
              804  LOAD_CONST               1
              806  CALL_FUNCTION_2       2  ''
              808  STORE_FAST               'ellipse_count'

 L. 633       810  LOAD_FAST                'ellipse_count'
              812  LOAD_GLOBAL              len
              814  LOAD_FAST                'sub'
              816  CALL_FUNCTION_1       1  ''
              818  LOAD_CONST               3
              820  BINARY_SUBTRACT  
              822  INPLACE_SUBTRACT 
              824  STORE_FAST               'ellipse_count'
            826_0  COME_FROM           792  '792'

 L. 635       826  LOAD_FAST                'ellipse_count'
              828  LOAD_FAST                'longest'
              830  COMPARE_OP               >
          832_834  POP_JUMP_IF_FALSE   840  'to 840'

 L. 636       836  LOAD_FAST                'ellipse_count'
              838  STORE_FAST               'longest'
            840_0  COME_FROM           832  '832'

 L. 638       840  LOAD_FAST                'ellipse_count'
              842  LOAD_CONST               0
              844  COMPARE_OP               <
          846_848  POP_JUMP_IF_FALSE   860  'to 860'

 L. 639       850  LOAD_GLOBAL              ValueError
              852  LOAD_STR                 'Ellipses lengths do not match.'
              854  CALL_FUNCTION_1       1  ''
              856  RAISE_VARARGS_1       1  'exception instance'
              858  JUMP_BACK           714  'to 714'
            860_0  COME_FROM           846  '846'

 L. 640       860  LOAD_FAST                'ellipse_count'
              862  LOAD_CONST               0
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_FALSE   888  'to 888'

 L. 641       870  LOAD_FAST                'sub'
              872  LOAD_METHOD              replace
              874  LOAD_STR                 '...'
              876  LOAD_STR                 ''
              878  CALL_METHOD_2         2  ''
              880  LOAD_FAST                'split_subscripts'
              882  LOAD_FAST                'num'
              884  STORE_SUBSCR     
              886  JUMP_BACK           714  'to 714'
            888_0  COME_FROM           866  '866'

 L. 643       888  LOAD_FAST                'ellipse_inds'
              890  LOAD_FAST                'ellipse_count'
              892  UNARY_NEGATIVE   
              894  LOAD_CONST               None
              896  BUILD_SLICE_2         2 
              898  BINARY_SUBSCR    
              900  STORE_FAST               'rep_inds'

 L. 644       902  LOAD_FAST                'sub'
              904  LOAD_METHOD              replace
              906  LOAD_STR                 '...'
              908  LOAD_FAST                'rep_inds'
              910  CALL_METHOD_2         2  ''
              912  LOAD_FAST                'split_subscripts'
              914  LOAD_FAST                'num'
              916  STORE_SUBSCR     
          918_920  JUMP_BACK           714  'to 714'

 L. 646       922  LOAD_STR                 ','
              924  LOAD_METHOD              join
              926  LOAD_FAST                'split_subscripts'
              928  CALL_METHOD_1         1  ''
              930  STORE_FAST               'subscripts'

 L. 647       932  LOAD_FAST                'longest'
              934  LOAD_CONST               0
              936  COMPARE_OP               ==
          938_940  POP_JUMP_IF_FALSE   948  'to 948'

 L. 648       942  LOAD_STR                 ''
              944  STORE_FAST               'out_ellipse'
              946  JUMP_FORWARD        962  'to 962'
            948_0  COME_FROM           938  '938'

 L. 650       948  LOAD_FAST                'ellipse_inds'
              950  LOAD_FAST                'longest'
              952  UNARY_NEGATIVE   
              954  LOAD_CONST               None
              956  BUILD_SLICE_2         2 
              958  BINARY_SUBSCR    
              960  STORE_FAST               'out_ellipse'
            962_0  COME_FROM           946  '946'

 L. 652       962  LOAD_FAST                'out_sub'
          964_966  POP_JUMP_IF_FALSE   990  'to 990'

 L. 653       968  LOAD_FAST                'subscripts'
              970  LOAD_STR                 '->'
              972  LOAD_FAST                'output_sub'
              974  LOAD_METHOD              replace
              976  LOAD_STR                 '...'
              978  LOAD_FAST                'out_ellipse'
              980  CALL_METHOD_2         2  ''
              982  BINARY_ADD       
              984  INPLACE_ADD      
              986  STORE_FAST               'subscripts'
              988  JUMP_FORWARD       1114  'to 1114'
            990_0  COME_FROM           964  '964'

 L. 656       990  LOAD_STR                 ''
              992  STORE_FAST               'output_subscript'

 L. 657       994  LOAD_FAST                'subscripts'
              996  LOAD_METHOD              replace
              998  LOAD_STR                 ','
             1000  LOAD_STR                 ''
             1002  CALL_METHOD_2         2  ''
             1004  STORE_FAST               'tmp_subscripts'

 L. 658      1006  LOAD_GLOBAL              sorted
             1008  LOAD_GLOBAL              set
             1010  LOAD_FAST                'tmp_subscripts'
             1012  CALL_FUNCTION_1       1  ''
             1014  CALL_FUNCTION_1       1  ''
             1016  GET_ITER         
           1018_0  COME_FROM          1056  '1056'
             1018  FOR_ITER           1072  'to 1072'
             1020  STORE_FAST               's'

 L. 659      1022  LOAD_FAST                's'
             1024  LOAD_GLOBAL              einsum_symbols
             1026  <118>                 1  ''
         1028_1030  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 660      1032  LOAD_GLOBAL              ValueError
             1034  LOAD_STR                 'Character %s is not a valid symbol.'
             1036  LOAD_FAST                's'
             1038  BINARY_MODULO    
             1040  CALL_FUNCTION_1       1  ''
             1042  RAISE_VARARGS_1       1  'exception instance'
           1044_0  COME_FROM          1028  '1028'

 L. 661      1044  LOAD_FAST                'tmp_subscripts'
             1046  LOAD_METHOD              count
             1048  LOAD_FAST                's'
             1050  CALL_METHOD_1         1  ''
             1052  LOAD_CONST               1
             1054  COMPARE_OP               ==
         1056_1058  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 662      1060  LOAD_FAST                'output_subscript'
             1062  LOAD_FAST                's'
             1064  INPLACE_ADD      
             1066  STORE_FAST               'output_subscript'
         1068_1070  JUMP_BACK          1018  'to 1018'

 L. 663      1072  LOAD_STR                 ''
             1074  LOAD_METHOD              join
             1076  LOAD_GLOBAL              sorted
             1078  LOAD_GLOBAL              set
             1080  LOAD_FAST                'output_subscript'
             1082  CALL_FUNCTION_1       1  ''

 L. 664      1084  LOAD_GLOBAL              set
             1086  LOAD_FAST                'out_ellipse'
             1088  CALL_FUNCTION_1       1  ''

 L. 663      1090  BINARY_SUBTRACT  
             1092  CALL_FUNCTION_1       1  ''
             1094  CALL_METHOD_1         1  ''
             1096  STORE_FAST               'normal_inds'

 L. 666      1098  LOAD_FAST                'subscripts'
             1100  LOAD_STR                 '->'
             1102  LOAD_FAST                'out_ellipse'
             1104  BINARY_ADD       
             1106  LOAD_FAST                'normal_inds'
             1108  BINARY_ADD       
             1110  INPLACE_ADD      
             1112  STORE_FAST               'subscripts'
           1114_0  COME_FROM           988  '988'
           1114_1  COME_FROM           590  '590'

 L. 669      1114  LOAD_STR                 '->'
             1116  LOAD_FAST                'subscripts'
             1118  <118>                 0  ''
         1120_1122  POP_JUMP_IF_FALSE  1140  'to 1140'

 L. 670      1124  LOAD_FAST                'subscripts'
             1126  LOAD_METHOD              split
             1128  LOAD_STR                 '->'
             1130  CALL_METHOD_1         1  ''
             1132  UNPACK_SEQUENCE_2     2 
             1134  STORE_FAST               'input_subscripts'
             1136  STORE_FAST               'output_subscript'
             1138  JUMP_FORWARD       1226  'to 1226'
           1140_0  COME_FROM          1120  '1120'

 L. 672      1140  LOAD_FAST                'subscripts'
             1142  STORE_FAST               'input_subscripts'

 L. 674      1144  LOAD_FAST                'subscripts'
             1146  LOAD_METHOD              replace
             1148  LOAD_STR                 ','
             1150  LOAD_STR                 ''
             1152  CALL_METHOD_2         2  ''
             1154  STORE_FAST               'tmp_subscripts'

 L. 675      1156  LOAD_STR                 ''
             1158  STORE_FAST               'output_subscript'

 L. 676      1160  LOAD_GLOBAL              sorted
             1162  LOAD_GLOBAL              set
             1164  LOAD_FAST                'tmp_subscripts'
             1166  CALL_FUNCTION_1       1  ''
             1168  CALL_FUNCTION_1       1  ''
             1170  GET_ITER         
           1172_0  COME_FROM          1210  '1210'
             1172  FOR_ITER           1226  'to 1226'
             1174  STORE_FAST               's'

 L. 677      1176  LOAD_FAST                's'
             1178  LOAD_GLOBAL              einsum_symbols
             1180  <118>                 1  ''
         1182_1184  POP_JUMP_IF_FALSE  1198  'to 1198'

 L. 678      1186  LOAD_GLOBAL              ValueError
             1188  LOAD_STR                 'Character %s is not a valid symbol.'
             1190  LOAD_FAST                's'
             1192  BINARY_MODULO    
             1194  CALL_FUNCTION_1       1  ''
             1196  RAISE_VARARGS_1       1  'exception instance'
           1198_0  COME_FROM          1182  '1182'

 L. 679      1198  LOAD_FAST                'tmp_subscripts'
             1200  LOAD_METHOD              count
             1202  LOAD_FAST                's'
             1204  CALL_METHOD_1         1  ''
             1206  LOAD_CONST               1
             1208  COMPARE_OP               ==
         1210_1212  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 680      1214  LOAD_FAST                'output_subscript'
             1216  LOAD_FAST                's'
             1218  INPLACE_ADD      
             1220  STORE_FAST               'output_subscript'
         1222_1224  JUMP_BACK          1172  'to 1172'
           1226_0  COME_FROM          1138  '1138'

 L. 683      1226  LOAD_FAST                'output_subscript'
             1228  GET_ITER         
           1230_0  COME_FROM          1240  '1240'
             1230  FOR_ITER           1260  'to 1260'
             1232  STORE_FAST               'char'

 L. 684      1234  LOAD_FAST                'char'
             1236  LOAD_FAST                'input_subscripts'
             1238  <118>                 1  ''
         1240_1242  POP_JUMP_IF_FALSE  1230  'to 1230'

 L. 685      1244  LOAD_GLOBAL              ValueError
             1246  LOAD_STR                 'Output character %s did not appear in the input'

 L. 686      1248  LOAD_FAST                'char'

 L. 685      1250  BINARY_MODULO    
             1252  CALL_FUNCTION_1       1  ''
             1254  RAISE_VARARGS_1       1  'exception instance'
         1256_1258  JUMP_BACK          1230  'to 1230'

 L. 689      1260  LOAD_GLOBAL              len
             1262  LOAD_FAST                'input_subscripts'
             1264  LOAD_METHOD              split
             1266  LOAD_STR                 ','
             1268  CALL_METHOD_1         1  ''
             1270  CALL_FUNCTION_1       1  ''
             1272  LOAD_GLOBAL              len
             1274  LOAD_FAST                'operands'
             1276  CALL_FUNCTION_1       1  ''
             1278  COMPARE_OP               !=
         1280_1282  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 690      1284  LOAD_GLOBAL              ValueError
             1286  LOAD_STR                 'Number of einsum subscripts must be equal to the number of operands.'
             1288  CALL_FUNCTION_1       1  ''
             1290  RAISE_VARARGS_1       1  'exception instance'
           1292_0  COME_FROM          1280  '1280'

 L. 693      1292  LOAD_FAST                'input_subscripts'
             1294  LOAD_FAST                'output_subscript'
             1296  LOAD_FAST                'operands'
             1298  BUILD_TUPLE_3         3 
             1300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 84


def _einsum_path_dispatcher(*operands, optimize=None, einsum_call=None):
    return operands


@array_function_dispatch(_einsum_path_dispatcher, module='numpy')
def einsum_path--- This code section failed: ---

 L. 818         0  LOAD_FAST                'optimize'
                2  STORE_FAST               'path_type'

 L. 819         4  LOAD_FAST                'path_type'
                6  LOAD_CONST               True
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 820        12  LOAD_STR                 'greedy'
               14  STORE_FAST               'path_type'
             16_0  COME_FROM            10  '10'

 L. 821        16  LOAD_FAST                'path_type'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 822        24  LOAD_CONST               False
               26  STORE_FAST               'path_type'
             28_0  COME_FROM            22  '22'

 L. 824        28  LOAD_CONST               None
               30  STORE_FAST               'memory_limit'

 L. 827        32  LOAD_FAST                'path_type'
               34  LOAD_CONST               False
               36  <117>                 0  ''
               38  POP_JUMP_IF_TRUE    156  'to 156'
               40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'path_type'
               44  LOAD_GLOBAL              str
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L. 828        50  JUMP_FORWARD        156  'to 156'
             52_0  COME_FROM            48  '48'

 L. 831        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'path_type'
               56  CALL_FUNCTION_1       1  ''
               58  POP_JUMP_IF_FALSE    74  'to 74'
               60  LOAD_FAST                'path_type'
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  LOAD_STR                 'einsum_path'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    74  'to 74'

 L. 832        72  JUMP_FORWARD        156  'to 156'
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            58  '58'

 L. 835        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'path_type'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_CONST               2
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   140  'to 140'
               86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'path_type'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_GLOBAL              str
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L. 836       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'path_type'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_GLOBAL              int
              110  LOAD_GLOBAL              float
              112  BUILD_TUPLE_2         2 
              114  CALL_FUNCTION_2       2  ''

 L. 835       116  POP_JUMP_IF_FALSE   140  'to 140'

 L. 837       118  LOAD_GLOBAL              int
              120  LOAD_FAST                'path_type'
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'memory_limit'

 L. 838       130  LOAD_FAST                'path_type'
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  STORE_FAST               'path_type'
              138  JUMP_FORWARD        156  'to 156'
            140_0  COME_FROM           116  '116'
            140_1  COME_FROM            98  '98'
            140_2  COME_FROM            84  '84'

 L. 841       140  LOAD_GLOBAL              TypeError
              142  LOAD_STR                 'Did not understand the path: %s'
              144  LOAD_GLOBAL              str
              146  LOAD_FAST                'path_type'
              148  CALL_FUNCTION_1       1  ''
              150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           138  '138'
            156_1  COME_FROM            72  '72'
            156_2  COME_FROM            50  '50'
            156_3  COME_FROM            38  '38'

 L. 844       156  LOAD_FAST                'einsum_call'
              158  STORE_FAST               'einsum_call_arg'

 L. 847       160  LOAD_GLOBAL              _parse_einsum_input
              162  LOAD_FAST                'operands'
              164  CALL_FUNCTION_1       1  ''
              166  UNPACK_SEQUENCE_3     3 
              168  STORE_FAST               'input_subscripts'
              170  STORE_FAST               'output_subscript'
              172  STORE_FAST               'operands'

 L. 850       174  LOAD_FAST                'input_subscripts'
              176  LOAD_METHOD              split
              178  LOAD_STR                 ','
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'input_list'

 L. 851       184  LOAD_LISTCOMP            '<code_object <listcomp>>'
              186  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              188  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              190  LOAD_FAST                'input_list'
              192  GET_ITER         
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'input_sets'

 L. 852       198  LOAD_GLOBAL              set
              200  LOAD_FAST                'output_subscript'
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'output_set'

 L. 853       206  LOAD_GLOBAL              set
              208  LOAD_FAST                'input_subscripts'
              210  LOAD_METHOD              replace
              212  LOAD_STR                 ','
              214  LOAD_STR                 ''
              216  CALL_METHOD_2         2  ''
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'indices'

 L. 856       222  BUILD_MAP_0           0 
              224  STORE_DEREF              'dimension_dict'

 L. 857       226  LOAD_LISTCOMP            '<code_object <listcomp>>'
              228  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              230  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              232  LOAD_GLOBAL              range
              234  LOAD_GLOBAL              len
              236  LOAD_FAST                'input_list'
              238  CALL_FUNCTION_1       1  ''
              240  CALL_FUNCTION_1       1  ''
              242  GET_ITER         
              244  CALL_FUNCTION_1       1  ''
              246  STORE_FAST               'broadcast_indices'

 L. 858       248  LOAD_GLOBAL              enumerate
              250  LOAD_FAST                'input_list'
              252  CALL_FUNCTION_1       1  ''
              254  GET_ITER         
              256  FOR_ITER            458  'to 458'
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'tnum'
              262  STORE_FAST               'term'

 L. 859       264  LOAD_FAST                'operands'
              266  LOAD_FAST                'tnum'
              268  BINARY_SUBSCR    
              270  LOAD_ATTR                shape
              272  STORE_FAST               'sh'

 L. 860       274  LOAD_GLOBAL              len
              276  LOAD_FAST                'sh'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_GLOBAL              len
              282  LOAD_FAST                'term'
              284  CALL_FUNCTION_1       1  ''
              286  COMPARE_OP               !=
          288_290  POP_JUMP_IF_FALSE   312  'to 312'

 L. 861       292  LOAD_GLOBAL              ValueError
              294  LOAD_STR                 'Einstein sum subscript %s does not contain the correct number of indices for operand %d.'

 L. 863       296  LOAD_FAST                'input_subscripts'
              298  LOAD_FAST                'tnum'
              300  BINARY_SUBSCR    
              302  LOAD_FAST                'tnum'
              304  BUILD_TUPLE_2         2 

 L. 861       306  BINARY_MODULO    
              308  CALL_FUNCTION_1       1  ''
              310  RAISE_VARARGS_1       1  'exception instance'
            312_0  COME_FROM           288  '288'

 L. 864       312  LOAD_GLOBAL              enumerate
              314  LOAD_FAST                'term'
              316  CALL_FUNCTION_1       1  ''
              318  GET_ITER         
              320  FOR_ITER            454  'to 454'
              322  UNPACK_SEQUENCE_2     2 
              324  STORE_FAST               'cnum'
              326  STORE_FAST               'char'

 L. 865       328  LOAD_FAST                'sh'
              330  LOAD_FAST                'cnum'
              332  BINARY_SUBSCR    
              334  STORE_FAST               'dim'

 L. 868       336  LOAD_FAST                'dim'
              338  LOAD_CONST               1
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   360  'to 360'

 L. 869       346  LOAD_FAST                'broadcast_indices'
              348  LOAD_FAST                'tnum'
              350  BINARY_SUBSCR    
              352  LOAD_METHOD              append
              354  LOAD_FAST                'char'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          
            360_0  COME_FROM           342  '342'

 L. 871       360  LOAD_FAST                'char'
              362  LOAD_DEREF               'dimension_dict'
              364  LOAD_METHOD              keys
              366  CALL_METHOD_0         0  ''
              368  <118>                 0  ''
          370_372  POP_JUMP_IF_FALSE   442  'to 442'

 L. 873       374  LOAD_DEREF               'dimension_dict'
              376  LOAD_FAST                'char'
              378  BINARY_SUBSCR    
              380  LOAD_CONST               1
              382  COMPARE_OP               ==
          384_386  POP_JUMP_IF_FALSE   398  'to 398'

 L. 874       388  LOAD_FAST                'dim'
              390  LOAD_DEREF               'dimension_dict'
              392  LOAD_FAST                'char'
              394  STORE_SUBSCR     
              396  JUMP_FORWARD        440  'to 440'
            398_0  COME_FROM           384  '384'

 L. 875       398  LOAD_FAST                'dim'
              400  LOAD_CONST               1
              402  LOAD_DEREF               'dimension_dict'
              404  LOAD_FAST                'char'
              406  BINARY_SUBSCR    
              408  BUILD_TUPLE_2         2 
              410  <118>                 1  ''
          412_414  POP_JUMP_IF_FALSE   450  'to 450'

 L. 876       416  LOAD_GLOBAL              ValueError
              418  LOAD_STR                 "Size of label '%s' for operand %d (%d) does not match previous terms (%d)."

 L. 878       420  LOAD_FAST                'char'
              422  LOAD_FAST                'tnum'
              424  LOAD_DEREF               'dimension_dict'
              426  LOAD_FAST                'char'
              428  BINARY_SUBSCR    
              430  LOAD_FAST                'dim'
              432  BUILD_TUPLE_4         4 

 L. 876       434  BINARY_MODULO    
              436  CALL_FUNCTION_1       1  ''
              438  RAISE_VARARGS_1       1  'exception instance'
            440_0  COME_FROM           396  '396'
              440  JUMP_BACK           320  'to 320'
            442_0  COME_FROM           370  '370'

 L. 880       442  LOAD_FAST                'dim'
              444  LOAD_DEREF               'dimension_dict'
              446  LOAD_FAST                'char'
              448  STORE_SUBSCR     
            450_0  COME_FROM           412  '412'
          450_452  JUMP_BACK           320  'to 320'
          454_456  JUMP_BACK           256  'to 256'

 L. 883       458  LOAD_LISTCOMP            '<code_object <listcomp>>'
              460  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              462  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              464  LOAD_FAST                'broadcast_indices'
              466  GET_ITER         
              468  CALL_FUNCTION_1       1  ''
              470  STORE_FAST               'broadcast_indices'

 L. 886       472  LOAD_CLOSURE             'dimension_dict'
              474  BUILD_TUPLE_1         1 
              476  LOAD_LISTCOMP            '<code_object <listcomp>>'
              478  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              480  MAKE_FUNCTION_8          'closure'

 L. 887       482  LOAD_FAST                'input_list'
              484  LOAD_FAST                'output_subscript'
              486  BUILD_LIST_1          1 
              488  BINARY_ADD       

 L. 886       490  GET_ITER         
              492  CALL_FUNCTION_1       1  ''
              494  STORE_FAST               'size_list'

 L. 888       496  LOAD_GLOBAL              max
              498  LOAD_FAST                'size_list'
              500  CALL_FUNCTION_1       1  ''
              502  STORE_FAST               'max_size'

 L. 890       504  LOAD_FAST                'memory_limit'
              506  LOAD_CONST               None
              508  <117>                 0  ''
          510_512  POP_JUMP_IF_FALSE   520  'to 520'

 L. 891       514  LOAD_FAST                'max_size'
              516  STORE_FAST               'memory_arg'
              518  JUMP_FORWARD        524  'to 524'
            520_0  COME_FROM           510  '510'

 L. 893       520  LOAD_FAST                'memory_limit'
              522  STORE_FAST               'memory_arg'
            524_0  COME_FROM           518  '518'

 L. 897       524  LOAD_GLOBAL              sum
              526  LOAD_GENEXPR             '<code_object <genexpr>>'
              528  LOAD_STR                 'einsum_path.<locals>.<genexpr>'
              530  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              532  LOAD_FAST                'input_sets'
              534  GET_ITER         
              536  CALL_FUNCTION_1       1  ''
              538  CALL_FUNCTION_1       1  ''
              540  LOAD_GLOBAL              len
              542  LOAD_FAST                'indices'
              544  CALL_FUNCTION_1       1  ''
              546  BINARY_SUBTRACT  
              548  LOAD_CONST               0
              550  COMPARE_OP               >
              552  STORE_FAST               'inner_product'

 L. 898       554  LOAD_GLOBAL              _flop_count
              556  LOAD_FAST                'indices'
              558  LOAD_FAST                'inner_product'
              560  LOAD_GLOBAL              len
              562  LOAD_FAST                'input_list'
              564  CALL_FUNCTION_1       1  ''
              566  LOAD_DEREF               'dimension_dict'
              568  CALL_FUNCTION_4       4  ''
              570  STORE_FAST               'naive_cost'

 L. 901       572  LOAD_FAST                'path_type'
              574  LOAD_CONST               False
              576  <117>                 0  ''
          578_580  POP_JUMP_IF_TRUE    606  'to 606'
              582  LOAD_GLOBAL              len
              584  LOAD_FAST                'input_list'
              586  CALL_FUNCTION_1       1  ''
              588  LOAD_CONST               (1, 2)
              590  <118>                 0  ''
          592_594  POP_JUMP_IF_TRUE    606  'to 606'
              596  LOAD_FAST                'indices'
              598  LOAD_FAST                'output_set'
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   626  'to 626'
            606_0  COME_FROM           592  '592'
            606_1  COME_FROM           578  '578'

 L. 903       606  LOAD_GLOBAL              tuple
              608  LOAD_GLOBAL              range
              610  LOAD_GLOBAL              len
              612  LOAD_FAST                'input_list'
              614  CALL_FUNCTION_1       1  ''
              616  CALL_FUNCTION_1       1  ''
              618  CALL_FUNCTION_1       1  ''
              620  BUILD_LIST_1          1 
              622  STORE_FAST               'path'
              624  JUMP_FORWARD        716  'to 716'
            626_0  COME_FROM           602  '602'

 L. 904       626  LOAD_FAST                'path_type'
              628  LOAD_STR                 'greedy'
              630  COMPARE_OP               ==
          632_634  POP_JUMP_IF_FALSE   652  'to 652'

 L. 905       636  LOAD_GLOBAL              _greedy_path
              638  LOAD_FAST                'input_sets'
              640  LOAD_FAST                'output_set'
              642  LOAD_DEREF               'dimension_dict'
              644  LOAD_FAST                'memory_arg'
              646  CALL_FUNCTION_4       4  ''
              648  STORE_FAST               'path'
              650  JUMP_FORWARD        716  'to 716'
            652_0  COME_FROM           632  '632'

 L. 906       652  LOAD_FAST                'path_type'
              654  LOAD_STR                 'optimal'
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   678  'to 678'

 L. 907       662  LOAD_GLOBAL              _optimal_path
              664  LOAD_FAST                'input_sets'
              666  LOAD_FAST                'output_set'
              668  LOAD_DEREF               'dimension_dict'
              670  LOAD_FAST                'memory_arg'
              672  CALL_FUNCTION_4       4  ''
              674  STORE_FAST               'path'
              676  JUMP_FORWARD        716  'to 716'
            678_0  COME_FROM           658  '658'

 L. 908       678  LOAD_FAST                'path_type'
              680  LOAD_CONST               0
              682  BINARY_SUBSCR    
              684  LOAD_STR                 'einsum_path'
              686  COMPARE_OP               ==
          688_690  POP_JUMP_IF_FALSE   706  'to 706'

 L. 909       692  LOAD_FAST                'path_type'
              694  LOAD_CONST               1
              696  LOAD_CONST               None
              698  BUILD_SLICE_2         2 
              700  BINARY_SUBSCR    
              702  STORE_FAST               'path'
              704  JUMP_FORWARD        716  'to 716'
            706_0  COME_FROM           688  '688'

 L. 911       706  LOAD_GLOBAL              KeyError
              708  LOAD_STR                 'Path name %s not found'
              710  LOAD_FAST                'path_type'
              712  CALL_FUNCTION_2       2  ''
              714  RAISE_VARARGS_1       1  'exception instance'
            716_0  COME_FROM           704  '704'
            716_1  COME_FROM           676  '676'
            716_2  COME_FROM           650  '650'
            716_3  COME_FROM           624  '624'

 L. 913       716  BUILD_LIST_0          0 
              718  BUILD_LIST_0          0 
              720  BUILD_LIST_0          0 
              722  BUILD_LIST_0          0 
              724  BUILD_TUPLE_4         4 
              726  UNPACK_SEQUENCE_4     4 
              728  STORE_FAST               'cost_list'
              730  STORE_FAST               'scale_list'
              732  STORE_FAST               'size_list'
              734  STORE_FAST               'contraction_list'

 L. 916       736  LOAD_GLOBAL              enumerate
              738  LOAD_FAST                'path'
              740  CALL_FUNCTION_1       1  ''
              742  GET_ITER         
          744_746  FOR_ITER           1088  'to 1088'
              748  UNPACK_SEQUENCE_2     2 
              750  STORE_FAST               'cnum'
              752  STORE_FAST               'contract_inds'

 L. 918       754  LOAD_GLOBAL              tuple
              756  LOAD_GLOBAL              sorted
              758  LOAD_GLOBAL              list
              760  LOAD_FAST                'contract_inds'
              762  CALL_FUNCTION_1       1  ''
              764  LOAD_CONST               True
              766  LOAD_CONST               ('reverse',)
              768  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              770  CALL_FUNCTION_1       1  ''
              772  STORE_FAST               'contract_inds'

 L. 920       774  LOAD_GLOBAL              _find_contraction
              776  LOAD_FAST                'contract_inds'
              778  LOAD_FAST                'input_sets'
              780  LOAD_FAST                'output_set'
              782  CALL_FUNCTION_3       3  ''
              784  STORE_FAST               'contract'

 L. 921       786  LOAD_FAST                'contract'
              788  UNPACK_SEQUENCE_4     4 
              790  STORE_FAST               'out_inds'
              792  STORE_FAST               'input_sets'
              794  STORE_FAST               'idx_removed'
              796  STORE_FAST               'idx_contract'

 L. 923       798  LOAD_GLOBAL              _flop_count
              800  LOAD_FAST                'idx_contract'
              802  LOAD_FAST                'idx_removed'
              804  LOAD_GLOBAL              len
              806  LOAD_FAST                'contract_inds'
              808  CALL_FUNCTION_1       1  ''
              810  LOAD_DEREF               'dimension_dict'
              812  CALL_FUNCTION_4       4  ''
              814  STORE_FAST               'cost'

 L. 924       816  LOAD_FAST                'cost_list'
              818  LOAD_METHOD              append
              820  LOAD_FAST                'cost'
              822  CALL_METHOD_1         1  ''
              824  POP_TOP          

 L. 925       826  LOAD_FAST                'scale_list'
              828  LOAD_METHOD              append
              830  LOAD_GLOBAL              len
              832  LOAD_FAST                'idx_contract'
              834  CALL_FUNCTION_1       1  ''
              836  CALL_METHOD_1         1  ''
              838  POP_TOP          

 L. 926       840  LOAD_FAST                'size_list'
              842  LOAD_METHOD              append
              844  LOAD_GLOBAL              _compute_size_by_dict
              846  LOAD_FAST                'out_inds'
              848  LOAD_DEREF               'dimension_dict'
              850  CALL_FUNCTION_2       2  ''
              852  CALL_METHOD_1         1  ''
              854  POP_TOP          

 L. 928       856  LOAD_GLOBAL              set
              858  CALL_FUNCTION_0       0  ''
              860  STORE_FAST               'bcast'

 L. 929       862  BUILD_LIST_0          0 
              864  STORE_FAST               'tmp_inputs'

 L. 930       866  LOAD_FAST                'contract_inds'
              868  GET_ITER         
              870  FOR_ITER            908  'to 908'
              872  STORE_FAST               'x'

 L. 931       874  LOAD_FAST                'tmp_inputs'
              876  LOAD_METHOD              append
              878  LOAD_FAST                'input_list'
              880  LOAD_METHOD              pop
              882  LOAD_FAST                'x'
              884  CALL_METHOD_1         1  ''
              886  CALL_METHOD_1         1  ''
              888  POP_TOP          

 L. 932       890  LOAD_FAST                'bcast'
              892  LOAD_FAST                'broadcast_indices'
              894  LOAD_METHOD              pop
              896  LOAD_FAST                'x'
              898  CALL_METHOD_1         1  ''
              900  INPLACE_OR       
              902  STORE_FAST               'bcast'
          904_906  JUMP_BACK           870  'to 870'

 L. 934       908  LOAD_FAST                'bcast'
              910  LOAD_FAST                'idx_removed'
              912  BINARY_SUBTRACT  
              914  STORE_FAST               'new_bcast_inds'

 L. 937       916  LOAD_GLOBAL              len
              918  LOAD_FAST                'idx_removed'
              920  LOAD_FAST                'bcast'
              922  BINARY_AND       
              924  CALL_FUNCTION_1       1  ''
          926_928  POP_JUMP_IF_TRUE    944  'to 944'

 L. 938       930  LOAD_GLOBAL              _can_dot
              932  LOAD_FAST                'tmp_inputs'
              934  LOAD_FAST                'out_inds'
              936  LOAD_FAST                'idx_removed'
              938  CALL_FUNCTION_3       3  ''
              940  STORE_FAST               'do_blas'
              942  JUMP_FORWARD        948  'to 948'
            944_0  COME_FROM           926  '926'

 L. 940       944  LOAD_CONST               False
              946  STORE_FAST               'do_blas'
            948_0  COME_FROM           942  '942'

 L. 943       948  LOAD_FAST                'cnum'
              950  LOAD_GLOBAL              len
              952  LOAD_FAST                'path'
              954  CALL_FUNCTION_1       1  ''
              956  BINARY_SUBTRACT  
              958  LOAD_CONST               -1
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE   972  'to 972'

 L. 944       966  LOAD_FAST                'output_subscript'
              968  STORE_FAST               'idx_result'
              970  JUMP_FORWARD       1014  'to 1014'
            972_0  COME_FROM           962  '962'

 L. 946       972  LOAD_CLOSURE             'dimension_dict'
              974  BUILD_TUPLE_1         1 
              976  LOAD_LISTCOMP            '<code_object <listcomp>>'
              978  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              980  MAKE_FUNCTION_8          'closure'
              982  LOAD_FAST                'out_inds'
              984  GET_ITER         
              986  CALL_FUNCTION_1       1  ''
              988  STORE_FAST               'sort_result'

 L. 947       990  LOAD_STR                 ''
              992  LOAD_METHOD              join
              994  LOAD_LISTCOMP            '<code_object <listcomp>>'
              996  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              998  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1000  LOAD_GLOBAL              sorted
             1002  LOAD_FAST                'sort_result'
             1004  CALL_FUNCTION_1       1  ''
             1006  GET_ITER         
             1008  CALL_FUNCTION_1       1  ''
             1010  CALL_METHOD_1         1  ''
             1012  STORE_FAST               'idx_result'
           1014_0  COME_FROM           970  '970'

 L. 949      1014  LOAD_FAST                'input_list'
             1016  LOAD_METHOD              append
             1018  LOAD_FAST                'idx_result'
             1020  CALL_METHOD_1         1  ''
             1022  POP_TOP          

 L. 950      1024  LOAD_FAST                'broadcast_indices'
             1026  LOAD_METHOD              append
             1028  LOAD_FAST                'new_bcast_inds'
             1030  CALL_METHOD_1         1  ''
             1032  POP_TOP          

 L. 951      1034  LOAD_STR                 ','
             1036  LOAD_METHOD              join
             1038  LOAD_FAST                'tmp_inputs'
             1040  CALL_METHOD_1         1  ''
             1042  LOAD_STR                 '->'
             1044  BINARY_ADD       
             1046  LOAD_FAST                'idx_result'
             1048  BINARY_ADD       
             1050  STORE_FAST               'einsum_str'

 L. 953      1052  LOAD_FAST                'contract_inds'
             1054  LOAD_FAST                'idx_removed'
             1056  LOAD_FAST                'einsum_str'
             1058  LOAD_FAST                'input_list'
             1060  LOAD_CONST               None
             1062  LOAD_CONST               None
             1064  BUILD_SLICE_2         2 
             1066  BINARY_SUBSCR    
             1068  LOAD_FAST                'do_blas'
             1070  BUILD_TUPLE_5         5 
             1072  STORE_FAST               'contraction'

 L. 954      1074  LOAD_FAST                'contraction_list'
             1076  LOAD_METHOD              append
             1078  LOAD_FAST                'contraction'
             1080  CALL_METHOD_1         1  ''
             1082  POP_TOP          
         1084_1086  JUMP_BACK           744  'to 744'

 L. 956      1088  LOAD_GLOBAL              sum
             1090  LOAD_FAST                'cost_list'
             1092  CALL_FUNCTION_1       1  ''
             1094  LOAD_CONST               1
             1096  BINARY_ADD       
             1098  STORE_FAST               'opt_cost'

 L. 958      1100  LOAD_FAST                'einsum_call_arg'
         1102_1104  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 959      1106  LOAD_FAST                'operands'
             1108  LOAD_FAST                'contraction_list'
             1110  BUILD_TUPLE_2         2 
             1112  RETURN_VALUE     
           1114_0  COME_FROM          1102  '1102'

 L. 962      1114  LOAD_FAST                'input_subscripts'
             1116  LOAD_STR                 '->'
             1118  BINARY_ADD       
             1120  LOAD_FAST                'output_subscript'
             1122  BINARY_ADD       
             1124  STORE_FAST               'overall_contraction'

 L. 963      1126  LOAD_CONST               ('scaling', 'current', 'remaining')
             1128  STORE_FAST               'header'

 L. 965      1130  LOAD_FAST                'naive_cost'
             1132  LOAD_FAST                'opt_cost'
             1134  BINARY_TRUE_DIVIDE
             1136  STORE_FAST               'speedup'

 L. 966      1138  LOAD_GLOBAL              max
             1140  LOAD_FAST                'size_list'
             1142  CALL_FUNCTION_1       1  ''
             1144  STORE_FAST               'max_i'

 L. 968      1146  LOAD_STR                 '  Complete contraction:  %s\n'
             1148  LOAD_FAST                'overall_contraction'
             1150  BINARY_MODULO    
             1152  STORE_FAST               'path_print'

 L. 969      1154  LOAD_FAST                'path_print'
             1156  LOAD_STR                 '         Naive scaling:  %d\n'
             1158  LOAD_GLOBAL              len
             1160  LOAD_FAST                'indices'
             1162  CALL_FUNCTION_1       1  ''
             1164  BINARY_MODULO    
             1166  INPLACE_ADD      
             1168  STORE_FAST               'path_print'

 L. 970      1170  LOAD_FAST                'path_print'
             1172  LOAD_STR                 '     Optimized scaling:  %d\n'
             1174  LOAD_GLOBAL              max
             1176  LOAD_FAST                'scale_list'
             1178  CALL_FUNCTION_1       1  ''
             1180  BINARY_MODULO    
             1182  INPLACE_ADD      
             1184  STORE_FAST               'path_print'

 L. 971      1186  LOAD_FAST                'path_print'
             1188  LOAD_STR                 '      Naive FLOP count:  %.3e\n'
             1190  LOAD_FAST                'naive_cost'
             1192  BINARY_MODULO    
             1194  INPLACE_ADD      
             1196  STORE_FAST               'path_print'

 L. 972      1198  LOAD_FAST                'path_print'
             1200  LOAD_STR                 '  Optimized FLOP count:  %.3e\n'
             1202  LOAD_FAST                'opt_cost'
             1204  BINARY_MODULO    
             1206  INPLACE_ADD      
             1208  STORE_FAST               'path_print'

 L. 973      1210  LOAD_FAST                'path_print'
             1212  LOAD_STR                 '   Theoretical speedup:  %3.3f\n'
             1214  LOAD_FAST                'speedup'
             1216  BINARY_MODULO    
             1218  INPLACE_ADD      
             1220  STORE_FAST               'path_print'

 L. 974      1222  LOAD_FAST                'path_print'
             1224  LOAD_STR                 '  Largest intermediate:  %.3e elements\n'
             1226  LOAD_FAST                'max_i'
             1228  BINARY_MODULO    
             1230  INPLACE_ADD      
             1232  STORE_FAST               'path_print'

 L. 975      1234  LOAD_FAST                'path_print'
             1236  LOAD_STR                 '--------------------------------------------------------------------------\n'
             1238  INPLACE_ADD      
             1240  STORE_FAST               'path_print'

 L. 976      1242  LOAD_FAST                'path_print'
             1244  LOAD_STR                 '%6s %24s %40s\n'
             1246  LOAD_FAST                'header'
             1248  BINARY_MODULO    
             1250  INPLACE_ADD      
             1252  STORE_FAST               'path_print'

 L. 977      1254  LOAD_FAST                'path_print'
             1256  LOAD_STR                 '--------------------------------------------------------------------------'
             1258  INPLACE_ADD      
             1260  STORE_FAST               'path_print'

 L. 979      1262  LOAD_GLOBAL              enumerate
             1264  LOAD_FAST                'contraction_list'
             1266  CALL_FUNCTION_1       1  ''
             1268  GET_ITER         
             1270  FOR_ITER           1340  'to 1340'
             1272  UNPACK_SEQUENCE_2     2 
             1274  STORE_FAST               'n'
             1276  STORE_FAST               'contraction'

 L. 980      1278  LOAD_FAST                'contraction'
             1280  UNPACK_SEQUENCE_5     5 
             1282  STORE_FAST               'inds'
             1284  STORE_FAST               'idx_rm'
             1286  STORE_FAST               'einsum_str'
             1288  STORE_FAST               'remaining'
             1290  STORE_FAST               'blas'

 L. 981      1292  LOAD_STR                 ','
             1294  LOAD_METHOD              join
             1296  LOAD_FAST                'remaining'
             1298  CALL_METHOD_1         1  ''
             1300  LOAD_STR                 '->'
             1302  BINARY_ADD       
             1304  LOAD_FAST                'output_subscript'
             1306  BINARY_ADD       
             1308  STORE_FAST               'remaining_str'

 L. 982      1310  LOAD_FAST                'scale_list'
             1312  LOAD_FAST                'n'
             1314  BINARY_SUBSCR    
             1316  LOAD_FAST                'einsum_str'
             1318  LOAD_FAST                'remaining_str'
             1320  BUILD_TUPLE_3         3 
             1322  STORE_FAST               'path_run'

 L. 983      1324  LOAD_FAST                'path_print'
             1326  LOAD_STR                 '\n%4d    %24s %40s'
             1328  LOAD_FAST                'path_run'
             1330  BINARY_MODULO    
             1332  INPLACE_ADD      
             1334  STORE_FAST               'path_print'
         1336_1338  JUMP_BACK          1270  'to 1270'

 L. 985      1340  LOAD_STR                 'einsum_path'
             1342  BUILD_LIST_1          1 
             1344  LOAD_FAST                'path'
             1346  BINARY_ADD       
             1348  STORE_FAST               'path'

 L. 986      1350  LOAD_FAST                'path'
             1352  LOAD_FAST                'path_print'
             1354  BUILD_TUPLE_2         2 
             1356  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 8


def _einsum_dispatcher(*operands, out=None, optimize=None, **kwargs):
    (yield from operands)
    (yield out)


@array_function_dispatch(_einsum_dispatcher, module='numpy')
def einsum--- This code section failed: ---

 L.1344         0  LOAD_FAST                'out'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  STORE_FAST               'specified_out'

 L.1347         8  LOAD_FAST                'optimize'
               10  LOAD_CONST               False
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    42  'to 42'

 L.1348        16  LOAD_FAST                'specified_out'
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.1349        20  LOAD_FAST                'out'
               22  LOAD_FAST                'kwargs'
               24  LOAD_STR                 'out'
               26  STORE_SUBSCR     
             28_0  COME_FROM            18  '18'

 L.1350        28  LOAD_GLOBAL              c_einsum
               30  LOAD_DEREF               'operands'
               32  BUILD_MAP_0           0 
               34  LOAD_FAST                'kwargs'
               36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  RETURN_VALUE     
             42_0  COME_FROM            14  '14'

 L.1354        42  BUILD_LIST_0          0 
               44  LOAD_CONST               ('dtype', 'order', 'casting')
               46  CALL_FINALLY         49  'to 49'
               48  STORE_DEREF              'valid_einsum_kwargs'

 L.1355        50  LOAD_CLOSURE             'valid_einsum_kwargs'
               52  BUILD_TUPLE_1         1 
               54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 'einsum.<locals>.<listcomp>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_FAST                'kwargs'
               62  LOAD_METHOD              items
               64  CALL_METHOD_0         0  ''
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'unknown_kwargs'

 L.1357        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'unknown_kwargs'
               76  CALL_FUNCTION_1       1  ''
               78  POP_JUMP_IF_FALSE    92  'to 92'

 L.1358        80  LOAD_GLOBAL              TypeError
               82  LOAD_STR                 'Did not understand the following kwargs: %s'

 L.1359        84  LOAD_FAST                'unknown_kwargs'

 L.1358        86  BINARY_MODULO    
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            78  '78'

 L.1363        92  LOAD_GLOBAL              einsum_path
               94  LOAD_DEREF               'operands'
               96  LOAD_FAST                'optimize'

 L.1364        98  LOAD_CONST               True

 L.1363       100  LOAD_CONST               ('optimize', 'einsum_call')
              102  BUILD_CONST_KEY_MAP_2     2 
              104  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_DEREF              'operands'
              110  STORE_FAST               'contraction_list'

 L.1367       112  LOAD_GLOBAL              enumerate
              114  LOAD_FAST                'contraction_list'
              116  CALL_FUNCTION_1       1  ''
              118  GET_ITER         
          120_122  FOR_ITER            440  'to 440'
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'num'
              128  STORE_FAST               'contraction'

 L.1368       130  LOAD_FAST                'contraction'
              132  UNPACK_SEQUENCE_5     5 
              134  STORE_FAST               'inds'
              136  STORE_FAST               'idx_rm'
              138  STORE_FAST               'einsum_str'
              140  STORE_FAST               'remaining'
              142  STORE_FAST               'blas'

 L.1369       144  LOAD_CLOSURE             'operands'
              146  BUILD_TUPLE_1         1 
              148  LOAD_LISTCOMP            '<code_object <listcomp>>'
              150  LOAD_STR                 'einsum.<locals>.<listcomp>'
              152  MAKE_FUNCTION_8          'closure'
              154  LOAD_FAST                'inds'
              156  GET_ITER         
              158  CALL_FUNCTION_1       1  ''
              160  STORE_FAST               'tmp_operands'

 L.1372       162  LOAD_FAST                'specified_out'
              164  JUMP_IF_FALSE_OR_POP   180  'to 180'
              166  LOAD_FAST                'num'
              168  LOAD_CONST               1
              170  BINARY_ADD       
              172  LOAD_GLOBAL              len
              174  LOAD_FAST                'contraction_list'
              176  CALL_FUNCTION_1       1  ''
              178  COMPARE_OP               ==
            180_0  COME_FROM           164  '164'
              180  STORE_FAST               'handle_out'

 L.1375       182  LOAD_FAST                'blas'
          184_186  POP_JUMP_IF_FALSE   388  'to 388'

 L.1377       188  LOAD_FAST                'einsum_str'
              190  LOAD_METHOD              split
              192  LOAD_STR                 '->'
              194  CALL_METHOD_1         1  ''
              196  UNPACK_SEQUENCE_2     2 
              198  STORE_FAST               'input_str'
              200  STORE_FAST               'results_index'

 L.1378       202  LOAD_FAST                'input_str'
              204  LOAD_METHOD              split
              206  LOAD_STR                 ','
              208  CALL_METHOD_1         1  ''
              210  UNPACK_SEQUENCE_2     2 
              212  STORE_FAST               'input_left'
              214  STORE_FAST               'input_right'

 L.1380       216  LOAD_FAST                'input_left'
              218  LOAD_FAST                'input_right'
              220  BINARY_ADD       
              222  STORE_FAST               'tensor_result'

 L.1381       224  LOAD_FAST                'idx_rm'
              226  GET_ITER         
              228  FOR_ITER            246  'to 246'
              230  STORE_FAST               's'

 L.1382       232  LOAD_FAST                'tensor_result'
              234  LOAD_METHOD              replace
              236  LOAD_FAST                's'
              238  LOAD_STR                 ''
              240  CALL_METHOD_2         2  ''
              242  STORE_FAST               'tensor_result'
              244  JUMP_BACK           228  'to 228'

 L.1385       246  BUILD_LIST_0          0 
              248  BUILD_LIST_0          0 
              250  ROT_TWO          
              252  STORE_FAST               'left_pos'
              254  STORE_FAST               'right_pos'

 L.1386       256  LOAD_GLOBAL              sorted
              258  LOAD_FAST                'idx_rm'
              260  CALL_FUNCTION_1       1  ''
              262  GET_ITER         
              264  FOR_ITER            304  'to 304'
              266  STORE_FAST               's'

 L.1387       268  LOAD_FAST                'left_pos'
              270  LOAD_METHOD              append
              272  LOAD_FAST                'input_left'
              274  LOAD_METHOD              find
              276  LOAD_FAST                's'
              278  CALL_METHOD_1         1  ''
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          

 L.1388       284  LOAD_FAST                'right_pos'
              286  LOAD_METHOD              append
              288  LOAD_FAST                'input_right'
              290  LOAD_METHOD              find
              292  LOAD_FAST                's'
              294  CALL_METHOD_1         1  ''
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
          300_302  JUMP_BACK           264  'to 264'

 L.1391       304  LOAD_GLOBAL              tensordot
              306  LOAD_FAST                'tmp_operands'
              308  LOAD_STR                 'axes'
              310  LOAD_GLOBAL              tuple
              312  LOAD_FAST                'left_pos'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_GLOBAL              tuple
              318  LOAD_FAST                'right_pos'
              320  CALL_FUNCTION_1       1  ''
              322  BUILD_TUPLE_2         2 
              324  BUILD_MAP_1           1 
              326  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              328  STORE_FAST               'new_view'

 L.1394       330  LOAD_FAST                'tensor_result'
              332  LOAD_FAST                'results_index'
              334  COMPARE_OP               !=
          336_338  POP_JUMP_IF_TRUE    346  'to 346'
              340  LOAD_FAST                'handle_out'
          342_344  POP_JUMP_IF_FALSE   424  'to 424'
            346_0  COME_FROM           336  '336'

 L.1395       346  LOAD_FAST                'handle_out'
          348_350  POP_JUMP_IF_FALSE   360  'to 360'

 L.1396       352  LOAD_FAST                'out'
              354  LOAD_FAST                'kwargs'
              356  LOAD_STR                 'out'
              358  STORE_SUBSCR     
            360_0  COME_FROM           348  '348'

 L.1397       360  LOAD_GLOBAL              c_einsum
              362  LOAD_FAST                'tensor_result'
              364  LOAD_STR                 '->'
              366  BINARY_ADD       
              368  LOAD_FAST                'results_index'
              370  BINARY_ADD       
              372  LOAD_FAST                'new_view'
              374  BUILD_TUPLE_2         2 
              376  BUILD_MAP_0           0 
              378  LOAD_FAST                'kwargs'
              380  <164>                 1  ''
              382  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              384  STORE_FAST               'new_view'
              386  JUMP_FORWARD        424  'to 424'
            388_0  COME_FROM           184  '184'

 L.1402       388  LOAD_FAST                'handle_out'
          390_392  POP_JUMP_IF_FALSE   402  'to 402'

 L.1403       394  LOAD_FAST                'out'
              396  LOAD_FAST                'kwargs'
              398  LOAD_STR                 'out'
              400  STORE_SUBSCR     
            402_0  COME_FROM           390  '390'

 L.1406       402  LOAD_GLOBAL              c_einsum
              404  LOAD_FAST                'einsum_str'
              406  BUILD_LIST_1          1 
              408  LOAD_FAST                'tmp_operands'
              410  CALL_FINALLY        413  'to 413'
              412  WITH_CLEANUP_FINISH
              414  BUILD_MAP_0           0 
              416  LOAD_FAST                'kwargs'
              418  <164>                 1  ''
              420  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              422  STORE_FAST               'new_view'
            424_0  COME_FROM           386  '386'
            424_1  COME_FROM           342  '342'

 L.1409       424  LOAD_DEREF               'operands'
              426  LOAD_METHOD              append
              428  LOAD_FAST                'new_view'
              430  CALL_METHOD_1         1  ''
              432  POP_TOP          

 L.1410       434  DELETE_FAST              'tmp_operands'
              436  DELETE_FAST              'new_view'
              438  JUMP_BACK           120  'to 120'

 L.1412       440  LOAD_FAST                'specified_out'
          442_444  POP_JUMP_IF_FALSE   450  'to 450'

 L.1413       446  LOAD_FAST                'out'
              448  RETURN_VALUE     
            450_0  COME_FROM           442  '442'

 L.1415       450  LOAD_DEREF               'operands'
              452  LOAD_CONST               0
              454  BINARY_SUBSCR    
              456  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1