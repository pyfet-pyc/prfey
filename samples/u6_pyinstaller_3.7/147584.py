# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

    return ret


def _find_contraction(positions, input_sets, output_set):
    """
    Finds the contraction for a given set of input and output sets.

    Parameters
    ----------
    positions : iterable
        Integer positions of terms used in the contraction.
    input_sets : list
        List of sets that represent the lhs side of the einsum subscript
    output_set : set
        Set that represents the rhs side of the overall einsum subscript

    Returns
    -------
    new_result : set
        The indices of the resulting contraction
    remaining : list
        List of sets that have not been contracted, the new set is appended to
        the end of this list
    idx_removed : set
        Indices removed from the entire contraction
    idx_contraction : set
        The indices used in the current contraction

    Examples
    --------

    # A simple dot product test case
    >>> pos = (0, 1)
    >>> isets = [set('ab'), set('bc')]
    >>> oset = set('ac')
    >>> _find_contraction(pos, isets, oset)
    ({'a', 'c'}, [{'a', 'c'}], {'b'}, {'a', 'b', 'c'})

    # A more complex case with additional terms in the contraction
    >>> pos = (0, 2)
    >>> isets = [set('abd'), set('ac'), set('bdc')]
    >>> oset = set('ac')
    >>> _find_contraction(pos, isets, oset)
    ({'a', 'c'}, [{'a', 'c'}, {'a', 'c'}], {'b', 'd'}, {'a', 'b', 'c', 'd'})
    """
    idx_contract = set()
    idx_remain = output_set.copy()
    remaining = []
    for ind, value in enumerate(input_sets):
        if ind in positions:
            idx_contract |= value
        else:
            remaining.append(value)
            idx_remain |= value

    new_result = idx_remain & idx_contract
    idx_removed = idx_contract - new_result
    remaining.append(new_result)
    return (
     new_result, remaining, idx_removed, idx_contract)


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
                    continue
                total_cost = cost + _flop_count(idx_contract, idx_removed, len(con), idx_dict)
                new_pos = positions + [con]
                iter_results.append((total_cost, new_pos, new_input_sets))

        if iter_results:
            full_results = iter_results
        else:
            path = min(full_results, key=(lambda x: x[0]))[1]
            path += [tuple(range(len(input_sets) - iteration))]
            return path

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


def _update_other_results(results, best):
    """Update the positions and provisional input_sets of ``results`` based on
    performing the contraction result ``best``. Remove any involving the tensors
    contracted.

    Parameters
    ----------
    results : list
        List of contraction results produced by ``_parse_possible_contraction``.
    best : list
        The best contraction of ``results`` i.e. the one that will be performed.

    Returns
    -------
    mod_results : list
        The list of modified results, updated with outcome of ``best`` contraction.
    """
    best_con = best[1]
    bx, by = best_con
    mod_results = []
    for cost, (x, y), con_sets in results:
        if not x in best_con:
            if y in best_con:
                continue
            del con_sets[by - int(by > x) - int(by > y)]
            del con_sets[bx - int(bx > x) - int(bx > y)]
            con_sets.insert(-1, best[2][(-1)])
            mod_con = (
             x - int(x > bx) - int(x > by), y - int(y > bx) - int(y > by))
            mod_results.append((cost, mod_con, con_sets))

    return mod_results


def _greedy_path(input_sets, output_set, idx_dict, memory_limit):
    """
    Finds the path by contracting the best pair until the input list is
    exhausted. The best pair is found by minimizing the tuple
    ``(-prod(indices_removed), cost)``.  What this amounts to is prioritizing
    matrix multiplication or inner product operations, then Hadamard like
    operations, and finally outer operations. Outer products are limited by
    ``memory_limit``. This algorithm scales cubically with respect to the
    number of elements in the list ``input_sets``.

    Parameters
    ----------
    input_sets : list
        List of sets that represent the lhs side of the einsum subscript
    output_set : set
        Set that represents the rhs side of the overall einsum subscript
    idx_dict : dictionary
        Dictionary of index sizes
    memory_limit_limit : int
        The maximum number of elements in a temporary array

    Returns
    -------
    path : list
        The greedy contraction order within the memory limit constraint.

    Examples
    --------
    >>> isets = [set('abd'), set('ac'), set('bdc')]
    >>> oset = set()
    >>> idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
    >>> _greedy_path(isets, oset, idx_sizes, 5000)
    [(0, 2), (0, 1)]
    """
    if len(input_sets) == 1:
        return [
         (0, )]
    if len(input_sets) == 2:
        return [
         (0, 1)]
    contract = _find_contraction(range(len(input_sets)), input_sets, output_set)
    idx_result, new_input_sets, idx_removed, idx_contract = contract
    naive_cost = _flop_count(idx_contract, idx_removed, len(input_sets), idx_dict)
    comb_iter = itertools.combinations(range(len(input_sets)), 2)
    known_contractions = []
    path_cost = 0
    path = []
    for iteration in range(len(input_sets) - 1):
        for positions in comb_iter:
            if input_sets[positions[0]].isdisjoint(input_sets[positions[1]]):
                continue
            result = _parse_possible_contraction(positions, input_sets, output_set, idx_dict, memory_limit, path_cost, naive_cost)
            if result is not None:
                known_contractions.append(result)

        if len(known_contractions) == 0:
            for positions in itertools.combinations(range(len(input_sets)), 2):
                result = _parse_possible_contraction(positions, input_sets, output_set, idx_dict, memory_limit, path_cost, naive_cost)
                if result is not None:
                    known_contractions.append(result)

            if len(known_contractions) == 0:
                path.append(tuple(range(len(input_sets))))
                break
        best = min(known_contractions, key=(lambda x: x[0]))
        known_contractions = _update_other_results(known_contractions, best)
        input_sets = best[2]
        new_tensor_pos = len(input_sets) - 1
        comb_iter = ((i, new_tensor_pos) for i in range(new_tensor_pos))
        path.append(best[1])
        path_cost += best[0][1]

    return path


def _can_dot(inputs, result, idx_removed):
    """
    Checks if we can use BLAS (np.tensordot) call and its beneficial to do so.

    Parameters
    ----------
    inputs : list of str
        Specifies the subscripts for summation.
    result : str
        Resulting summation.
    idx_removed : set
        Indices that are removed in the summation

    Returns
    -------
    type : bool
        Returns true if BLAS should and can be used, else False

    Notes
    -----
    If the operations is BLAS level 1 or 2 and is not already aligned
    we default back to einsum as the memory movement to copy is more
    costly than the operation itself.

    Examples
    --------

    # Standard GEMM operation
    >>> _can_dot(['ij', 'jk'], 'ik', set('j'))
    True

    # Can use the standard BLAS, but requires odd data movement
    >>> _can_dot(['ijj', 'jk'], 'ik', set('j'))
    False

    # DDOT where the memory is not aligned
    >>> _can_dot(['ijk', 'ikj'], '', set('ijk'))
    False

    """
    if len(idx_removed) == 0:
        return False
    else:
        if len(inputs) != 2:
            return False
        input_left, input_right = inputs
        for c in set(input_left + input_right):
            nl, nr = input_left.count(c), input_right.count(c)
            if not nl > 1:
                if nr > 1 or nl + nr > 2:
                    return False
                if nl + nr - 1 == int(c in result):
                    return False

        set_left = set(input_left)
        set_right = set(input_right)
        keep_left = set_left - idx_removed
        keep_right = set_right - idx_removed
        rs = len(idx_removed)
        if input_left == input_right:
            return True
        if set_left == set_right:
            return False
        if input_left[-rs:] == input_right[:rs]:
            return True
        if input_left[:rs] == input_right[-rs:]:
            return True
        if input_left[-rs:] == input_right[-rs:]:
            return True
        if input_left[:rs] == input_right[:rs]:
            return True
        return keep_left and keep_right or False
    return True


def _parse_einsum_input(operands):
    """
    A reproduction of einsum c side einsum parsing in python.

    Returns
    -------
    input_strings : str
        Parsed input strings
    output_string : str
        Parsed output string
    operands : list of array_like
        The operands to use in the numpy contraction

    Examples
    --------
    The operand list is simplified to reduce printing:

    >>> np.random.seed(123)
    >>> a = np.random.rand(4, 4)
    >>> b = np.random.rand(4, 4, 4)
    >>> _parse_einsum_input(('...a,...a->...', a, b))
    ('za,xza', 'xz', [a, b]) # may vary

    >>> _parse_einsum_input((a, [Ellipsis, 0], b, [Ellipsis, 0]))
    ('za,xza', 'xz', [a, b]) # may vary
    """
    if len(operands) == 0:
        raise ValueError('No input operands')
    if isinstance(operands[0], str):
        subscripts = operands[0].replace(' ', '')
        operands = [asanyarray(v) for v in operands[1:]]
        for s in subscripts:
            if s in '.,->':
                continue
            if s not in einsum_symbols:
                raise ValueError('Character %s is not a valid symbol.' % s)

    else:
        tmp_operands = list(operands)
        operand_list = []
        subscript_list = []
        for p in range(len(operands) // 2):
            operand_list.append(tmp_operands.pop(0))
            subscript_list.append(tmp_operands.pop(0))

        output_list = tmp_operands[(-1)] if len(tmp_operands) else None
        operands = [asanyarray(v) for v in operand_list]
        subscripts = ''
        last = len(subscript_list) - 1
        for num, sub in enumerate(subscript_list):
            for s in sub:
                if s is Ellipsis:
                    subscripts += '...'
                else:
                    try:
                        s = operator.index(s)
                    except TypeError as e:
                        try:
                            raise TypeError('For this input type lists must contain either int or Ellipsis') from e
                        finally:
                            e = None
                            del e

                    subscripts += einsum_symbols[s]

            if num != last:
                subscripts += ','

        if output_list is not None:
            subscripts += '->'
            for s in output_list:
                if s is Ellipsis:
                    subscripts += '...'
                else:
                    try:
                        s = operator.index(s)
                    except TypeError as e:
                        try:
                            raise TypeError('For this input type lists must contain either int or Ellipsis') from e
                        finally:
                            e = None
                            del e

                    subscripts += einsum_symbols[s]

        elif not '-' in subscripts:
            if '>' in subscripts:
                invalid = subscripts.count('-') > 1 or subscripts.count('>') > 1
                if invalid or subscripts.count('->') != 1:
                    raise ValueError("Subscripts can only contain one '->'.")
            if '.' in subscripts:
                used = subscripts.replace('.', '').replace(',', '').replace('->', '')
                unused = list(einsum_symbols_set - set(used))
                ellipse_inds = ''.join(unused)
                longest = 0
                if '->' in subscripts:
                    input_tmp, output_sub = subscripts.split('->')
                    split_subscripts = input_tmp.split(',')
                    out_sub = True
                else:
                    split_subscripts = subscripts.split(',')
                    out_sub = False
                for num, sub in enumerate(split_subscripts):
                    if '.' in sub and not sub.count('.') != 3:
                        if sub.count('...') != 1:
                            raise ValueError('Invalid Ellipses.')
                        if operands[num].shape == ():
                            ellipse_count = 0
                        else:
                            ellipse_count = max(operands[num].ndim, 1)
                            ellipse_count -= len(sub) - 3
                        if ellipse_count > longest:
                            longest = ellipse_count
                        if ellipse_count < 0:
                            raise ValueError('Ellipses lengths do not match.')
                        elif ellipse_count == 0:
                            split_subscripts[num] = sub.replace('...', '')
                        else:
                            rep_inds = ellipse_inds[-ellipse_count:]
                            split_subscripts[num] = sub.replace('...', rep_inds)

                subscripts = ','.join(split_subscripts)
                if longest == 0:
                    out_ellipse = ''
                else:
                    out_ellipse = ellipse_inds[-longest:]
                if out_sub:
                    subscripts += '->' + output_sub.replace('...', out_ellipse)
                else:
                    output_subscript = ''
                    tmp_subscripts = subscripts.replace(',', '')
                    for s in sorted(set(tmp_subscripts)):
                        if s not in einsum_symbols:
                            raise ValueError('Character %s is not a valid symbol.' % s)
                        if tmp_subscripts.count(s) == 1:
                            output_subscript += s

                    normal_inds = ''.join(sorted(set(output_subscript) - set(out_ellipse)))
                    subscripts += '->' + out_ellipse + normal_inds
            if '->' in subscripts:
                input_subscripts, output_subscript = subscripts.split('->')
        else:
            input_subscripts = subscripts
            tmp_subscripts = subscripts.replace(',', '')
            output_subscript = ''
            for s in sorted(set(tmp_subscripts)):
                if s not in einsum_symbols:
                    raise ValueError('Character %s is not a valid symbol.' % s)
                if tmp_subscripts.count(s) == 1:
                    output_subscript += s

        for char in output_subscript:
            if char not in input_subscripts:
                raise ValueError('Output character %s did not appear in the input' % char)

        if len(input_subscripts.split(',')) != len(operands):
            raise ValueError('Number of einsum subscripts must be equal to the number of operands.')
        return (
         input_subscripts, output_subscript, operands)


def _einsum_path_dispatcher(*operands, optimize=None, einsum_call=None):
    return operands


@array_function_dispatch(_einsum_path_dispatcher, module='numpy')
def einsum_path--- This code section failed: ---

 L. 818         0  LOAD_FAST                'optimize'
                2  STORE_FAST               'path_type'

 L. 819         4  LOAD_FAST                'path_type'
                6  LOAD_CONST               True
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 820        12  LOAD_STR                 'greedy'
               14  STORE_FAST               'path_type'
             16_0  COME_FROM            10  '10'

 L. 821        16  LOAD_FAST                'path_type'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 822        24  LOAD_CONST               False
               26  STORE_FAST               'path_type'
             28_0  COME_FROM            22  '22'

 L. 824        28  LOAD_CONST               None
               30  STORE_FAST               'memory_limit'

 L. 827        32  LOAD_FAST                'path_type'
               34  LOAD_CONST               False
               36  COMPARE_OP               is
               38  POP_JUMP_IF_TRUE    156  'to 156'
               40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'path_type'
               44  LOAD_GLOBAL              str
               46  CALL_FUNCTION_2       2  '2 positional arguments'
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L. 828        50  JUMP_FORWARD        156  'to 156'
             52_0  COME_FROM            48  '48'

 L. 831        52  LOAD_GLOBAL              len
               54  LOAD_FAST                'path_type'
               56  CALL_FUNCTION_1       1  '1 positional argument'
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
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  LOAD_CONST               2
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   140  'to 140'
               86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'path_type'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_GLOBAL              str
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L. 836       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'path_type'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_GLOBAL              int
              110  LOAD_GLOBAL              float
              112  BUILD_TUPLE_2         2 
              114  CALL_FUNCTION_2       2  '2 positional arguments'
              116  POP_JUMP_IF_FALSE   140  'to 140'

 L. 837       118  LOAD_GLOBAL              int
              120  LOAD_FAST                'path_type'
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_1       1  '1 positional argument'
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
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  BINARY_MODULO    
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           138  '138'
            156_1  COME_FROM            72  '72'
            156_2  COME_FROM            50  '50'
            156_3  COME_FROM            38  '38'

 L. 844       156  LOAD_FAST                'einsum_call'
              158  STORE_FAST               'einsum_call_arg'

 L. 847       160  LOAD_GLOBAL              _parse_einsum_input
              162  LOAD_FAST                'operands'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  UNPACK_SEQUENCE_3     3 
              168  STORE_FAST               'input_subscripts'
              170  STORE_FAST               'output_subscript'
              172  STORE_FAST               'operands'

 L. 850       174  LOAD_FAST                'input_subscripts'
              176  LOAD_METHOD              split
              178  LOAD_STR                 ','
              180  CALL_METHOD_1         1  '1 positional argument'
              182  STORE_FAST               'input_list'

 L. 851       184  LOAD_LISTCOMP            '<code_object <listcomp>>'
              186  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              188  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              190  LOAD_FAST                'input_list'
              192  GET_ITER         
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  STORE_FAST               'input_sets'

 L. 852       198  LOAD_GLOBAL              set
              200  LOAD_FAST                'output_subscript'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  STORE_FAST               'output_set'

 L. 853       206  LOAD_GLOBAL              set
              208  LOAD_FAST                'input_subscripts'
              210  LOAD_METHOD              replace
              212  LOAD_STR                 ','
              214  LOAD_STR                 ''
              216  CALL_METHOD_2         2  '2 positional arguments'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_FAST               'indices'

 L. 856       222  BUILD_MAP_0           0 
              224  STORE_DEREF              'dimension_dict'

 L. 857       226  LOAD_LISTCOMP            '<code_object <listcomp>>'
              228  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              230  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              232  LOAD_GLOBAL              range
              234  LOAD_GLOBAL              len
              236  LOAD_FAST                'input_list'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  GET_ITER         
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  STORE_FAST               'broadcast_indices'

 L. 858       248  SETUP_LOOP          466  'to 466'
              250  LOAD_GLOBAL              enumerate
              252  LOAD_FAST                'input_list'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  GET_ITER         
              258  FOR_ITER            464  'to 464'
              260  UNPACK_SEQUENCE_2     2 
              262  STORE_FAST               'tnum'
              264  STORE_FAST               'term'

 L. 859       266  LOAD_FAST                'operands'
              268  LOAD_FAST                'tnum'
              270  BINARY_SUBSCR    
              272  LOAD_ATTR                shape
              274  STORE_FAST               'sh'

 L. 860       276  LOAD_GLOBAL              len
              278  LOAD_FAST                'sh'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  LOAD_GLOBAL              len
              284  LOAD_FAST                'term'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  COMPARE_OP               !=
          290_292  POP_JUMP_IF_FALSE   314  'to 314'

 L. 861       294  LOAD_GLOBAL              ValueError
              296  LOAD_STR                 'Einstein sum subscript %s does not contain the correct number of indices for operand %d.'

 L. 863       298  LOAD_FAST                'input_subscripts'
              300  LOAD_FAST                'tnum'
              302  BINARY_SUBSCR    
              304  LOAD_FAST                'tnum'
              306  BUILD_TUPLE_2         2 
              308  BINARY_MODULO    
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  RAISE_VARARGS_1       1  'exception instance'
            314_0  COME_FROM           290  '290'

 L. 864       314  SETUP_LOOP          460  'to 460'
              316  LOAD_GLOBAL              enumerate
              318  LOAD_FAST                'term'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  GET_ITER         
              324  FOR_ITER            458  'to 458'
              326  UNPACK_SEQUENCE_2     2 
              328  STORE_FAST               'cnum'
              330  STORE_FAST               'char'

 L. 865       332  LOAD_FAST                'sh'
              334  LOAD_FAST                'cnum'
              336  BINARY_SUBSCR    
              338  STORE_FAST               'dim'

 L. 868       340  LOAD_FAST                'dim'
              342  LOAD_CONST               1
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   364  'to 364'

 L. 869       350  LOAD_FAST                'broadcast_indices'
              352  LOAD_FAST                'tnum'
              354  BINARY_SUBSCR    
              356  LOAD_METHOD              append
              358  LOAD_FAST                'char'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  POP_TOP          
            364_0  COME_FROM           346  '346'

 L. 871       364  LOAD_FAST                'char'
              366  LOAD_DEREF               'dimension_dict'
              368  LOAD_METHOD              keys
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  COMPARE_OP               in
          374_376  POP_JUMP_IF_FALSE   446  'to 446'

 L. 873       378  LOAD_DEREF               'dimension_dict'
              380  LOAD_FAST                'char'
              382  BINARY_SUBSCR    
              384  LOAD_CONST               1
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_FALSE   402  'to 402'

 L. 874       392  LOAD_FAST                'dim'
              394  LOAD_DEREF               'dimension_dict'
              396  LOAD_FAST                'char'
              398  STORE_SUBSCR     
              400  JUMP_FORWARD        444  'to 444'
            402_0  COME_FROM           388  '388'

 L. 875       402  LOAD_FAST                'dim'
              404  LOAD_CONST               1
              406  LOAD_DEREF               'dimension_dict'
              408  LOAD_FAST                'char'
              410  BINARY_SUBSCR    
              412  BUILD_TUPLE_2         2 
              414  COMPARE_OP               not-in
          416_418  POP_JUMP_IF_FALSE   454  'to 454'

 L. 876       420  LOAD_GLOBAL              ValueError
              422  LOAD_STR                 "Size of label '%s' for operand %d (%d) does not match previous terms (%d)."

 L. 878       424  LOAD_FAST                'char'
              426  LOAD_FAST                'tnum'
              428  LOAD_DEREF               'dimension_dict'
              430  LOAD_FAST                'char'
              432  BINARY_SUBSCR    
              434  LOAD_FAST                'dim'
              436  BUILD_TUPLE_4         4 
              438  BINARY_MODULO    
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  RAISE_VARARGS_1       1  'exception instance'
            444_0  COME_FROM           400  '400'
              444  JUMP_BACK           324  'to 324'
            446_0  COME_FROM           374  '374'

 L. 880       446  LOAD_FAST                'dim'
              448  LOAD_DEREF               'dimension_dict'
              450  LOAD_FAST                'char'
              452  STORE_SUBSCR     
            454_0  COME_FROM           416  '416'
          454_456  JUMP_BACK           324  'to 324'
              458  POP_BLOCK        
            460_0  COME_FROM_LOOP      314  '314'
          460_462  JUMP_BACK           258  'to 258'
              464  POP_BLOCK        
            466_0  COME_FROM_LOOP      248  '248'

 L. 883       466  LOAD_LISTCOMP            '<code_object <listcomp>>'
              468  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              470  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              472  LOAD_FAST                'broadcast_indices'
              474  GET_ITER         
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  STORE_FAST               'broadcast_indices'

 L. 886       480  LOAD_CLOSURE             'dimension_dict'
              482  BUILD_TUPLE_1         1 
              484  LOAD_LISTCOMP            '<code_object <listcomp>>'
              486  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              488  MAKE_FUNCTION_8          'closure'

 L. 887       490  LOAD_FAST                'input_list'
              492  LOAD_FAST                'output_subscript'
              494  BUILD_LIST_1          1 
              496  BINARY_ADD       
              498  GET_ITER         
              500  CALL_FUNCTION_1       1  '1 positional argument'
              502  STORE_FAST               'size_list'

 L. 888       504  LOAD_GLOBAL              max
              506  LOAD_FAST                'size_list'
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  STORE_FAST               'max_size'

 L. 890       512  LOAD_FAST                'memory_limit'
              514  LOAD_CONST               None
              516  COMPARE_OP               is
          518_520  POP_JUMP_IF_FALSE   528  'to 528'

 L. 891       522  LOAD_FAST                'max_size'
              524  STORE_FAST               'memory_arg'
              526  JUMP_FORWARD        532  'to 532'
            528_0  COME_FROM           518  '518'

 L. 893       528  LOAD_FAST                'memory_limit'
              530  STORE_FAST               'memory_arg'
            532_0  COME_FROM           526  '526'

 L. 897       532  LOAD_GLOBAL              sum
              534  LOAD_GENEXPR             '<code_object <genexpr>>'
              536  LOAD_STR                 'einsum_path.<locals>.<genexpr>'
              538  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              540  LOAD_FAST                'input_sets'
              542  GET_ITER         
              544  CALL_FUNCTION_1       1  '1 positional argument'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                'indices'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  BINARY_SUBTRACT  
              556  LOAD_CONST               0
              558  COMPARE_OP               >
              560  STORE_FAST               'inner_product'

 L. 898       562  LOAD_GLOBAL              _flop_count
              564  LOAD_FAST                'indices'
              566  LOAD_FAST                'inner_product'
              568  LOAD_GLOBAL              len
              570  LOAD_FAST                'input_list'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  LOAD_DEREF               'dimension_dict'
              576  CALL_FUNCTION_4       4  '4 positional arguments'
              578  STORE_FAST               'naive_cost'

 L. 901       580  LOAD_FAST                'path_type'
              582  LOAD_CONST               False
              584  COMPARE_OP               is
          586_588  POP_JUMP_IF_TRUE    614  'to 614'
              590  LOAD_GLOBAL              len
              592  LOAD_FAST                'input_list'
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  LOAD_CONST               (1, 2)
              598  COMPARE_OP               in
          600_602  POP_JUMP_IF_TRUE    614  'to 614'
              604  LOAD_FAST                'indices'
              606  LOAD_FAST                'output_set'
              608  COMPARE_OP               ==
          610_612  POP_JUMP_IF_FALSE   634  'to 634'
            614_0  COME_FROM           600  '600'
            614_1  COME_FROM           586  '586'

 L. 903       614  LOAD_GLOBAL              tuple
              616  LOAD_GLOBAL              range
              618  LOAD_GLOBAL              len
              620  LOAD_FAST                'input_list'
              622  CALL_FUNCTION_1       1  '1 positional argument'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  BUILD_LIST_1          1 
              630  STORE_FAST               'path'
              632  JUMP_FORWARD        724  'to 724'
            634_0  COME_FROM           610  '610'

 L. 904       634  LOAD_FAST                'path_type'
              636  LOAD_STR                 'greedy'
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   660  'to 660'

 L. 905       644  LOAD_GLOBAL              _greedy_path
              646  LOAD_FAST                'input_sets'
              648  LOAD_FAST                'output_set'
              650  LOAD_DEREF               'dimension_dict'
              652  LOAD_FAST                'memory_arg'
              654  CALL_FUNCTION_4       4  '4 positional arguments'
              656  STORE_FAST               'path'
              658  JUMP_FORWARD        724  'to 724'
            660_0  COME_FROM           640  '640'

 L. 906       660  LOAD_FAST                'path_type'
              662  LOAD_STR                 'optimal'
              664  COMPARE_OP               ==
          666_668  POP_JUMP_IF_FALSE   686  'to 686'

 L. 907       670  LOAD_GLOBAL              _optimal_path
              672  LOAD_FAST                'input_sets'
              674  LOAD_FAST                'output_set'
              676  LOAD_DEREF               'dimension_dict'
              678  LOAD_FAST                'memory_arg'
              680  CALL_FUNCTION_4       4  '4 positional arguments'
              682  STORE_FAST               'path'
              684  JUMP_FORWARD        724  'to 724'
            686_0  COME_FROM           666  '666'

 L. 908       686  LOAD_FAST                'path_type'
              688  LOAD_CONST               0
              690  BINARY_SUBSCR    
              692  LOAD_STR                 'einsum_path'
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   714  'to 714'

 L. 909       700  LOAD_FAST                'path_type'
              702  LOAD_CONST               1
              704  LOAD_CONST               None
              706  BUILD_SLICE_2         2 
              708  BINARY_SUBSCR    
              710  STORE_FAST               'path'
              712  JUMP_FORWARD        724  'to 724'
            714_0  COME_FROM           696  '696'

 L. 911       714  LOAD_GLOBAL              KeyError
              716  LOAD_STR                 'Path name %s not found'
              718  LOAD_FAST                'path_type'
              720  CALL_FUNCTION_2       2  '2 positional arguments'
              722  RAISE_VARARGS_1       1  'exception instance'
            724_0  COME_FROM           712  '712'
            724_1  COME_FROM           684  '684'
            724_2  COME_FROM           658  '658'
            724_3  COME_FROM           632  '632'

 L. 913       724  BUILD_LIST_0          0 
              726  BUILD_LIST_0          0 
              728  BUILD_LIST_0          0 
              730  BUILD_LIST_0          0 
              732  BUILD_TUPLE_4         4 
              734  UNPACK_SEQUENCE_4     4 
              736  STORE_FAST               'cost_list'
              738  STORE_FAST               'scale_list'
              740  STORE_FAST               'size_list'
              742  STORE_FAST               'contraction_list'

 L. 916   744_746  SETUP_LOOP         1106  'to 1106'
              748  LOAD_GLOBAL              enumerate
              750  LOAD_FAST                'path'
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  GET_ITER         
          756_758  FOR_ITER           1104  'to 1104'
              760  UNPACK_SEQUENCE_2     2 
              762  STORE_FAST               'cnum'
              764  STORE_FAST               'contract_inds'

 L. 918       766  LOAD_GLOBAL              tuple
              768  LOAD_GLOBAL              sorted
              770  LOAD_GLOBAL              list
              772  LOAD_FAST                'contract_inds'
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  LOAD_CONST               True
              778  LOAD_CONST               ('reverse',)
              780  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              782  CALL_FUNCTION_1       1  '1 positional argument'
              784  STORE_FAST               'contract_inds'

 L. 920       786  LOAD_GLOBAL              _find_contraction
              788  LOAD_FAST                'contract_inds'
              790  LOAD_FAST                'input_sets'
              792  LOAD_FAST                'output_set'
              794  CALL_FUNCTION_3       3  '3 positional arguments'
              796  STORE_FAST               'contract'

 L. 921       798  LOAD_FAST                'contract'
              800  UNPACK_SEQUENCE_4     4 
              802  STORE_FAST               'out_inds'
              804  STORE_FAST               'input_sets'
              806  STORE_FAST               'idx_removed'
              808  STORE_FAST               'idx_contract'

 L. 923       810  LOAD_GLOBAL              _flop_count
              812  LOAD_FAST                'idx_contract'
              814  LOAD_FAST                'idx_removed'
              816  LOAD_GLOBAL              len
              818  LOAD_FAST                'contract_inds'
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  LOAD_DEREF               'dimension_dict'
              824  CALL_FUNCTION_4       4  '4 positional arguments'
              826  STORE_FAST               'cost'

 L. 924       828  LOAD_FAST                'cost_list'
              830  LOAD_METHOD              append
              832  LOAD_FAST                'cost'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  POP_TOP          

 L. 925       838  LOAD_FAST                'scale_list'
              840  LOAD_METHOD              append
              842  LOAD_GLOBAL              len
              844  LOAD_FAST                'idx_contract'
              846  CALL_FUNCTION_1       1  '1 positional argument'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          

 L. 926       852  LOAD_FAST                'size_list'
              854  LOAD_METHOD              append
              856  LOAD_GLOBAL              _compute_size_by_dict
              858  LOAD_FAST                'out_inds'
              860  LOAD_DEREF               'dimension_dict'
              862  CALL_FUNCTION_2       2  '2 positional arguments'
              864  CALL_METHOD_1         1  '1 positional argument'
              866  POP_TOP          

 L. 928       868  LOAD_GLOBAL              set
              870  CALL_FUNCTION_0       0  '0 positional arguments'
              872  STORE_FAST               'bcast'

 L. 929       874  BUILD_LIST_0          0 
              876  STORE_FAST               'tmp_inputs'

 L. 930       878  SETUP_LOOP          924  'to 924'
              880  LOAD_FAST                'contract_inds'
              882  GET_ITER         
              884  FOR_ITER            922  'to 922'
              886  STORE_FAST               'x'

 L. 931       888  LOAD_FAST                'tmp_inputs'
              890  LOAD_METHOD              append
              892  LOAD_FAST                'input_list'
              894  LOAD_METHOD              pop
              896  LOAD_FAST                'x'
              898  CALL_METHOD_1         1  '1 positional argument'
              900  CALL_METHOD_1         1  '1 positional argument'
              902  POP_TOP          

 L. 932       904  LOAD_FAST                'bcast'
              906  LOAD_FAST                'broadcast_indices'
              908  LOAD_METHOD              pop
              910  LOAD_FAST                'x'
              912  CALL_METHOD_1         1  '1 positional argument'
              914  INPLACE_OR       
              916  STORE_FAST               'bcast'
          918_920  JUMP_BACK           884  'to 884'
              922  POP_BLOCK        
            924_0  COME_FROM_LOOP      878  '878'

 L. 934       924  LOAD_FAST                'bcast'
              926  LOAD_FAST                'idx_removed'
              928  BINARY_SUBTRACT  
              930  STORE_FAST               'new_bcast_inds'

 L. 937       932  LOAD_GLOBAL              len
              934  LOAD_FAST                'idx_removed'
              936  LOAD_FAST                'bcast'
              938  BINARY_AND       
              940  CALL_FUNCTION_1       1  '1 positional argument'
          942_944  POP_JUMP_IF_TRUE    960  'to 960'

 L. 938       946  LOAD_GLOBAL              _can_dot
              948  LOAD_FAST                'tmp_inputs'
              950  LOAD_FAST                'out_inds'
              952  LOAD_FAST                'idx_removed'
              954  CALL_FUNCTION_3       3  '3 positional arguments'
              956  STORE_FAST               'do_blas'
              958  JUMP_FORWARD        964  'to 964'
            960_0  COME_FROM           942  '942'

 L. 940       960  LOAD_CONST               False
              962  STORE_FAST               'do_blas'
            964_0  COME_FROM           958  '958'

 L. 943       964  LOAD_FAST                'cnum'
              966  LOAD_GLOBAL              len
              968  LOAD_FAST                'path'
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  BINARY_SUBTRACT  
              974  LOAD_CONST               -1
              976  COMPARE_OP               ==
          978_980  POP_JUMP_IF_FALSE   988  'to 988'

 L. 944       982  LOAD_FAST                'output_subscript'
              984  STORE_FAST               'idx_result'
              986  JUMP_FORWARD       1030  'to 1030'
            988_0  COME_FROM           978  '978'

 L. 946       988  LOAD_CLOSURE             'dimension_dict'
              990  BUILD_TUPLE_1         1 
              992  LOAD_LISTCOMP            '<code_object <listcomp>>'
              994  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              996  MAKE_FUNCTION_8          'closure'
              998  LOAD_FAST                'out_inds'
             1000  GET_ITER         
             1002  CALL_FUNCTION_1       1  '1 positional argument'
             1004  STORE_FAST               'sort_result'

 L. 947      1006  LOAD_STR                 ''
             1008  LOAD_METHOD              join
             1010  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1012  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
             1014  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1016  LOAD_GLOBAL              sorted
             1018  LOAD_FAST                'sort_result'
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  GET_ITER         
             1024  CALL_FUNCTION_1       1  '1 positional argument'
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  STORE_FAST               'idx_result'
           1030_0  COME_FROM           986  '986'

 L. 949      1030  LOAD_FAST                'input_list'
             1032  LOAD_METHOD              append
             1034  LOAD_FAST                'idx_result'
             1036  CALL_METHOD_1         1  '1 positional argument'
             1038  POP_TOP          

 L. 950      1040  LOAD_FAST                'broadcast_indices'
             1042  LOAD_METHOD              append
             1044  LOAD_FAST                'new_bcast_inds'
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  POP_TOP          

 L. 951      1050  LOAD_STR                 ','
             1052  LOAD_METHOD              join
             1054  LOAD_FAST                'tmp_inputs'
             1056  CALL_METHOD_1         1  '1 positional argument'
             1058  LOAD_STR                 '->'
             1060  BINARY_ADD       
             1062  LOAD_FAST                'idx_result'
             1064  BINARY_ADD       
             1066  STORE_FAST               'einsum_str'

 L. 953      1068  LOAD_FAST                'contract_inds'
             1070  LOAD_FAST                'idx_removed'
             1072  LOAD_FAST                'einsum_str'
             1074  LOAD_FAST                'input_list'
             1076  LOAD_CONST               None
             1078  LOAD_CONST               None
             1080  BUILD_SLICE_2         2 
             1082  BINARY_SUBSCR    
             1084  LOAD_FAST                'do_blas'
             1086  BUILD_TUPLE_5         5 
             1088  STORE_FAST               'contraction'

 L. 954      1090  LOAD_FAST                'contraction_list'
             1092  LOAD_METHOD              append
             1094  LOAD_FAST                'contraction'
             1096  CALL_METHOD_1         1  '1 positional argument'
             1098  POP_TOP          
         1100_1102  JUMP_BACK           756  'to 756'
             1104  POP_BLOCK        
           1106_0  COME_FROM_LOOP      744  '744'

 L. 956      1106  LOAD_GLOBAL              sum
             1108  LOAD_FAST                'cost_list'
             1110  CALL_FUNCTION_1       1  '1 positional argument'
             1112  LOAD_CONST               1
             1114  BINARY_ADD       
             1116  STORE_FAST               'opt_cost'

 L. 958      1118  LOAD_FAST                'einsum_call_arg'
         1120_1122  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 959      1124  LOAD_FAST                'operands'
             1126  LOAD_FAST                'contraction_list'
             1128  BUILD_TUPLE_2         2 
             1130  RETURN_VALUE     
           1132_0  COME_FROM          1120  '1120'

 L. 962      1132  LOAD_FAST                'input_subscripts'
             1134  LOAD_STR                 '->'
             1136  BINARY_ADD       
             1138  LOAD_FAST                'output_subscript'
             1140  BINARY_ADD       
             1142  STORE_FAST               'overall_contraction'

 L. 963      1144  LOAD_CONST               ('scaling', 'current', 'remaining')
             1146  STORE_FAST               'header'

 L. 965      1148  LOAD_FAST                'naive_cost'
             1150  LOAD_FAST                'opt_cost'
             1152  BINARY_TRUE_DIVIDE
             1154  STORE_FAST               'speedup'

 L. 966      1156  LOAD_GLOBAL              max
             1158  LOAD_FAST                'size_list'
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  STORE_FAST               'max_i'

 L. 968      1164  LOAD_STR                 '  Complete contraction:  %s\n'
             1166  LOAD_FAST                'overall_contraction'
             1168  BINARY_MODULO    
             1170  STORE_FAST               'path_print'

 L. 969      1172  LOAD_FAST                'path_print'
             1174  LOAD_STR                 '         Naive scaling:  %d\n'
             1176  LOAD_GLOBAL              len
             1178  LOAD_FAST                'indices'
             1180  CALL_FUNCTION_1       1  '1 positional argument'
             1182  BINARY_MODULO    
             1184  INPLACE_ADD      
             1186  STORE_FAST               'path_print'

 L. 970      1188  LOAD_FAST                'path_print'
             1190  LOAD_STR                 '     Optimized scaling:  %d\n'
             1192  LOAD_GLOBAL              max
             1194  LOAD_FAST                'scale_list'
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  BINARY_MODULO    
             1200  INPLACE_ADD      
             1202  STORE_FAST               'path_print'

 L. 971      1204  LOAD_FAST                'path_print'
             1206  LOAD_STR                 '      Naive FLOP count:  %.3e\n'
             1208  LOAD_FAST                'naive_cost'
             1210  BINARY_MODULO    
             1212  INPLACE_ADD      
             1214  STORE_FAST               'path_print'

 L. 972      1216  LOAD_FAST                'path_print'
             1218  LOAD_STR                 '  Optimized FLOP count:  %.3e\n'
             1220  LOAD_FAST                'opt_cost'
             1222  BINARY_MODULO    
             1224  INPLACE_ADD      
             1226  STORE_FAST               'path_print'

 L. 973      1228  LOAD_FAST                'path_print'
             1230  LOAD_STR                 '   Theoretical speedup:  %3.3f\n'
             1232  LOAD_FAST                'speedup'
             1234  BINARY_MODULO    
             1236  INPLACE_ADD      
             1238  STORE_FAST               'path_print'

 L. 974      1240  LOAD_FAST                'path_print'
             1242  LOAD_STR                 '  Largest intermediate:  %.3e elements\n'
             1244  LOAD_FAST                'max_i'
             1246  BINARY_MODULO    
             1248  INPLACE_ADD      
             1250  STORE_FAST               'path_print'

 L. 975      1252  LOAD_FAST                'path_print'
             1254  LOAD_STR                 '--------------------------------------------------------------------------\n'
             1256  INPLACE_ADD      
             1258  STORE_FAST               'path_print'

 L. 976      1260  LOAD_FAST                'path_print'
             1262  LOAD_STR                 '%6s %24s %40s\n'
             1264  LOAD_FAST                'header'
             1266  BINARY_MODULO    
             1268  INPLACE_ADD      
             1270  STORE_FAST               'path_print'

 L. 977      1272  LOAD_FAST                'path_print'
             1274  LOAD_STR                 '--------------------------------------------------------------------------'
             1276  INPLACE_ADD      
             1278  STORE_FAST               'path_print'

 L. 979      1280  SETUP_LOOP         1362  'to 1362'
             1282  LOAD_GLOBAL              enumerate
             1284  LOAD_FAST                'contraction_list'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  GET_ITER         
             1290  FOR_ITER           1360  'to 1360'
             1292  UNPACK_SEQUENCE_2     2 
             1294  STORE_FAST               'n'
             1296  STORE_FAST               'contraction'

 L. 980      1298  LOAD_FAST                'contraction'
             1300  UNPACK_SEQUENCE_5     5 
             1302  STORE_FAST               'inds'
             1304  STORE_FAST               'idx_rm'
             1306  STORE_FAST               'einsum_str'
             1308  STORE_FAST               'remaining'
             1310  STORE_FAST               'blas'

 L. 981      1312  LOAD_STR                 ','
             1314  LOAD_METHOD              join
             1316  LOAD_FAST                'remaining'
             1318  CALL_METHOD_1         1  '1 positional argument'
             1320  LOAD_STR                 '->'
             1322  BINARY_ADD       
             1324  LOAD_FAST                'output_subscript'
             1326  BINARY_ADD       
             1328  STORE_FAST               'remaining_str'

 L. 982      1330  LOAD_FAST                'scale_list'
             1332  LOAD_FAST                'n'
             1334  BINARY_SUBSCR    
             1336  LOAD_FAST                'einsum_str'
             1338  LOAD_FAST                'remaining_str'
             1340  BUILD_TUPLE_3         3 
             1342  STORE_FAST               'path_run'

 L. 983      1344  LOAD_FAST                'path_print'
             1346  LOAD_STR                 '\n%4d    %24s %40s'
             1348  LOAD_FAST                'path_run'
             1350  BINARY_MODULO    
             1352  INPLACE_ADD      
             1354  STORE_FAST               'path_print'
         1356_1358  JUMP_BACK          1290  'to 1290'
             1360  POP_BLOCK        
           1362_0  COME_FROM_LOOP     1280  '1280'

 L. 985      1362  LOAD_STR                 'einsum_path'
             1364  BUILD_LIST_1          1 
             1366  LOAD_FAST                'path'
             1368  BINARY_ADD       
             1370  STORE_FAST               'path'

 L. 986      1372  LOAD_FAST                'path'
             1374  LOAD_FAST                'path_print'
             1376  BUILD_TUPLE_2         2 
             1378  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 454_0


def _einsum_dispatcher(*operands, out=None, optimize=None, **kwargs):
    yield from operands
    yield out


@array_function_dispatch(_einsum_dispatcher, module='numpy')
def einsum(*operands, out=None, optimize=False, **kwargs):
    """
    einsum(subscripts, *operands, out=None, dtype=None, order='K',
           casting='safe', optimize=False)

    Evaluates the Einstein summation convention on the operands.

    Using the Einstein summation convention, many common multi-dimensional,
    linear algebraic array operations can be represented in a simple fashion.
    In *implicit* mode `einsum` computes these values.

    In *explicit* mode, `einsum` provides further flexibility to compute
    other array operations that might not be considered classical Einstein
    summation operations, by disabling, or forcing summation over specified
    subscript labels.

    See the notes and examples for clarification.

    Parameters
    ----------
    subscripts : str
        Specifies the subscripts for summation as comma separated list of
        subscript labels. An implicit (classical Einstein summation)
        calculation is performed unless the explicit indicator '->' is
        included as well as subscript labels of the precise output form.
    operands : list of array_like
        These are the arrays for the operation.
    out : ndarray, optional
        If provided, the calculation is done into this array.
    dtype : {data-type, None}, optional
        If provided, forces the calculation to use the data type specified.
        Note that you may have to also give a more liberal `casting`
        parameter to allow the conversions. Default is None.
    order : {'C', 'F', 'A', 'K'}, optional
        Controls the memory layout of the output. 'C' means it should
        be C contiguous. 'F' means it should be Fortran contiguous,
        'A' means it should be 'F' if the inputs are all 'F', 'C' otherwise.
        'K' means it should be as close to the layout as the inputs as
        is possible, including arbitrarily permuted axes.
        Default is 'K'.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur.  Setting this to
        'unsafe' is not recommended, as it can adversely affect accumulations.

          * 'no' means the data types should not be cast at all.
          * 'equiv' means only byte-order changes are allowed.
          * 'safe' means only casts which can preserve values are allowed.
          * 'same_kind' means only safe casts or casts within a kind,
            like float64 to float32, are allowed.
          * 'unsafe' means any data conversions may be done.

        Default is 'safe'.
    optimize : {False, True, 'greedy', 'optimal'}, optional
        Controls if intermediate optimization should occur. No optimization
        will occur if False and True will default to the 'greedy' algorithm.
        Also accepts an explicit contraction list from the ``np.einsum_path``
        function. See ``np.einsum_path`` for more details. Defaults to False.

    Returns
    -------
    output : ndarray
        The calculation based on the Einstein summation convention.

    See Also
    --------
    einsum_path, dot, inner, outer, tensordot, linalg.multi_dot

    einops:
        similar verbose interface is provided by
        `einops <https://github.com/arogozhnikov/einops>`_ package to cover
        additional operations: transpose, reshape/flatten, repeat/tile,
        squeeze/unsqueeze and reductions.

    opt_einsum:
        `opt_einsum <https://optimized-einsum.readthedocs.io/en/stable/>`_
        optimizes contraction order for einsum-like expressions
        in backend-agnostic manner.

    Notes
    -----
    .. versionadded:: 1.6.0

    The Einstein summation convention can be used to compute
    many multi-dimensional, linear algebraic array operations. `einsum`
    provides a succinct way of representing these.

    A non-exhaustive list of these operations,
    which can be computed by `einsum`, is shown below along with examples:

    * Trace of an array, :py:func:`numpy.trace`.
    * Return a diagonal, :py:func:`numpy.diag`.
    * Array axis summations, :py:func:`numpy.sum`.
    * Transpositions and permutations, :py:func:`numpy.transpose`.
    * Matrix multiplication and dot product, :py:func:`numpy.matmul` :py:func:`numpy.dot`.
    * Vector inner and outer products, :py:func:`numpy.inner` :py:func:`numpy.outer`.
    * Broadcasting, element-wise and scalar multiplication, :py:func:`numpy.multiply`.
    * Tensor contractions, :py:func:`numpy.tensordot`.
    * Chained array operations, in efficient calculation order, :py:func:`numpy.einsum_path`.

    The subscripts string is a comma-separated list of subscript labels,
    where each label refers to a dimension of the corresponding operand.
    Whenever a label is repeated it is summed, so ``np.einsum('i,i', a, b)``
    is equivalent to :py:func:`np.inner(a,b) <numpy.inner>`. If a label
    appears only once, it is not summed, so ``np.einsum('i', a)`` produces a
    view of ``a`` with no changes. A further example ``np.einsum('ij,jk', a, b)``
    describes traditional matrix multiplication and is equivalent to
    :py:func:`np.matmul(a,b) <numpy.matmul>`. Repeated subscript labels in one
    operand take the diagonal. For example, ``np.einsum('ii', a)`` is equivalent
    to :py:func:`np.trace(a) <numpy.trace>`.

    In *implicit mode*, the chosen subscripts are important
    since the axes of the output are reordered alphabetically.  This
    means that ``np.einsum('ij', a)`` doesn't affect a 2D array, while
    ``np.einsum('ji', a)`` takes its transpose. Additionally,
    ``np.einsum('ij,jk', a, b)`` returns a matrix multiplication, while,
    ``np.einsum('ij,jh', a, b)`` returns the transpose of the
    multiplication since subscript 'h' precedes subscript 'i'.

    In *explicit mode* the output can be directly controlled by
    specifying output subscript labels.  This requires the
    identifier '->' as well as the list of output subscript labels.
    This feature increases the flexibility of the function since
    summing can be disabled or forced when required. The call
    ``np.einsum('i->', a)`` is like :py:func:`np.sum(a, axis=-1) <numpy.sum>`,
    and ``np.einsum('ii->i', a)`` is like :py:func:`np.diag(a) <numpy.diag>`.
    The difference is that `einsum` does not allow broadcasting by default.
    Additionally ``np.einsum('ij,jh->ih', a, b)`` directly specifies the
    order of the output subscript labels and therefore returns matrix
    multiplication, unlike the example above in implicit mode.

    To enable and control broadcasting, use an ellipsis.  Default
    NumPy-style broadcasting is done by adding an ellipsis
    to the left of each term, like ``np.einsum('...ii->...i', a)``.
    To take the trace along the first and last axes,
    you can do ``np.einsum('i...i', a)``, or to do a matrix-matrix
    product with the left-most indices instead of rightmost, one can do
    ``np.einsum('ij...,jk...->ik...', a, b)``.

    When there is only one operand, no axes are summed, and no output
    parameter is provided, a view into the operand is returned instead
    of a new array.  Thus, taking the diagonal as ``np.einsum('ii->i', a)``
    produces a view (changed in version 1.10.0).

    `einsum` also provides an alternative way to provide the subscripts
    and operands as ``einsum(op0, sublist0, op1, sublist1, ..., [sublistout])``.
    If the output shape is not provided in this format `einsum` will be
    calculated in implicit mode, otherwise it will be performed explicitly.
    The examples below have corresponding `einsum` calls with the two
    parameter methods.

    .. versionadded:: 1.10.0

    Views returned from einsum are now writeable whenever the input array
    is writeable. For example, ``np.einsum('ijk...->kji...', a)`` will now
    have the same effect as :py:func:`np.swapaxes(a, 0, 2) <numpy.swapaxes>`
    and ``np.einsum('ii->i', a)`` will return a writeable view of the diagonal
    of a 2D array.

    .. versionadded:: 1.12.0

    Added the ``optimize`` argument which will optimize the contraction order
    of an einsum expression. For a contraction with three or more operands this
    can greatly increase the computational efficiency at the cost of a larger
    memory footprint during computation.

    Typically a 'greedy' algorithm is applied which empirical tests have shown
    returns the optimal path in the majority of cases. In some cases 'optimal'
    will return the superlative path through a more expensive, exhaustive search.
    For iterative calculations it may be advisable to calculate the optimal path
    once and reuse that path by supplying it as an argument. An example is given
    below.

    See :py:func:`numpy.einsum_path` for more details.

    Examples
    --------
    >>> a = np.arange(25).reshape(5,5)
    >>> b = np.arange(5)
    >>> c = np.arange(6).reshape(2,3)

    Trace of a matrix:

    >>> np.einsum('ii', a)
    60
    >>> np.einsum(a, [0,0])
    60
    >>> np.trace(a)
    60

    Extract the diagonal (requires explicit form):

    >>> np.einsum('ii->i', a)
    array([ 0,  6, 12, 18, 24])
    >>> np.einsum(a, [0,0], [0])
    array([ 0,  6, 12, 18, 24])
    >>> np.diag(a)
    array([ 0,  6, 12, 18, 24])

    Sum over an axis (requires explicit form):

    >>> np.einsum('ij->i', a)
    array([ 10,  35,  60,  85, 110])
    >>> np.einsum(a, [0,1], [0])
    array([ 10,  35,  60,  85, 110])
    >>> np.sum(a, axis=1)
    array([ 10,  35,  60,  85, 110])

    For higher dimensional arrays summing a single axis can be done with ellipsis:

    >>> np.einsum('...j->...', a)
    array([ 10,  35,  60,  85, 110])
    >>> np.einsum(a, [Ellipsis,1], [Ellipsis])
    array([ 10,  35,  60,  85, 110])

    Compute a matrix transpose, or reorder any number of axes:

    >>> np.einsum('ji', c)
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.einsum('ij->ji', c)
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.einsum(c, [1,0])
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.transpose(c)
    array([[0, 3],
           [1, 4],
           [2, 5]])

    Vector inner products:

    >>> np.einsum('i,i', b, b)
    30
    >>> np.einsum(b, [0], b, [0])
    30
    >>> np.inner(b,b)
    30

    Matrix vector multiplication:

    >>> np.einsum('ij,j', a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum(a, [0,1], b, [1])
    array([ 30,  80, 130, 180, 230])
    >>> np.dot(a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum('...j,j', a, b)
    array([ 30,  80, 130, 180, 230])

    Broadcasting and scalar multiplication:

    >>> np.einsum('..., ...', 3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(',ij', 3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(3, [Ellipsis], c, [Ellipsis])
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.multiply(3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])

    Vector outer product:

    >>> np.einsum('i,j', np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.einsum(np.arange(2)+1, [0], b, [1])
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.outer(np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])

    Tensor contraction:

    >>> a = np.arange(60.).reshape(3,4,5)
    >>> b = np.arange(24.).reshape(4,3,2)
    >>> np.einsum('ijk,jil->kl', a, b)
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])
    >>> np.einsum(a, [0,1,2], b, [1,0,3], [2,3])
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])
    >>> np.tensordot(a,b, axes=([1,0],[0,1]))
    array([[4400., 4730.],
           [4532., 4874.],
           [4664., 5018.],
           [4796., 5162.],
           [4928., 5306.]])

    Writeable returned arrays (since version 1.10.0):

    >>> a = np.zeros((3, 3))
    >>> np.einsum('ii->i', a)[:] = 1
    >>> a
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    Example of ellipsis use:

    >>> a = np.arange(6).reshape((3,2))
    >>> b = np.arange(12).reshape((4,3))
    >>> np.einsum('ki,jk->ij', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])
    >>> np.einsum('ki,...k->i...', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])
    >>> np.einsum('k...,jk', a, b)
    array([[10, 28, 46, 64],
           [13, 40, 67, 94]])

    Chained array operations. For more complicated contractions, speed ups
    might be achieved by repeatedly computing a 'greedy' path or pre-computing the
    'optimal' path and repeatedly applying it, using an
    `einsum_path` insertion (since version 1.12.0). Performance improvements can be
    particularly significant with larger arrays:

    >>> a = np.ones(64).reshape(2,4,8)

    Basic `einsum`: ~1520ms  (benchmarked on 3.1GHz Intel i5.)

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a)

    Sub-optimal `einsum` (due to repeated path calculation time): ~330ms

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize='optimal')

    Greedy `einsum` (faster optimal path approximation): ~160ms

    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize='greedy')

    Optimal `einsum` (best usage pattern in some use cases): ~110ms

    >>> path = np.einsum_path('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize='optimal')[0]
    >>> for iteration in range(500):
    ...     _ = np.einsum('ijk,ilm,njm,nlk,abc->',a,a,a,a,a, optimize=path)

    """
    specified_out = out is not None
    if optimize is False:
        if specified_out:
            kwargs['out'] = out
        return c_einsum(*operands, **kwargs)
    valid_einsum_kwargs = [
     'dtype', 'order', 'casting']
    unknown_kwargs = [k for k, v in kwargs.items() if k not in valid_einsum_kwargs]
    if len(unknown_kwargs):
        raise TypeError('Did not understand the following kwargs: %s' % unknown_kwargs)
    else:
        operands, contraction_list = einsum_path(*operands, optimize=optimize, einsum_call=True)
        output_order = kwargs.pop('order', 'K')
        if output_order.upper() == 'A':
            if all((arr.flags.f_contiguous for arr in operands)):
                output_order = 'F'
            else:
                output_order = 'C'
    for num, contraction in enumerate(contraction_list):
        inds, idx_rm, einsum_str, remaining, blas = contraction
        tmp_operands = [operands.pop(x) for x in inds]
        handle_out = specified_out and num + 1 == len(contraction_list)
        if blas:
            input_str, results_index = einsum_str.split('->')
            input_left, input_right = input_str.split(',')
            tensor_result = input_left + input_right
            for s in idx_rm:
                tensor_result = tensor_result.replace(s, '')

            left_pos, right_pos = [], []
            for s in sorted(idx_rm):
                left_pos.append(input_left.find(s))
                right_pos.append(input_right.find(s))

            new_view = tensordot(*tmp_operands, **{'axes': (tuple(left_pos), tuple(right_pos))})
            if tensor_result != results_index or handle_out:
                if handle_out:
                    kwargs['out'] = out
                new_view = c_einsum((tensor_result + '->' + results_index), new_view, **kwargs)
        else:
            if handle_out:
                kwargs['out'] = out
            new_view = c_einsum(einsum_str, *tmp_operands, **kwargs)
        operands.append(new_view)
        del tmp_operands
        del new_view

    if specified_out:
        return out
    return asanyarray((operands[0]), order=output_order)