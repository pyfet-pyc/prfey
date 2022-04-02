# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\core\einsumfunc.py
"""
Implementation of optimized einsum.

"""
from __future__ import division, absolute_import, print_function
from numpy.compat import basestring
from numpy.core.multiarray import c_einsum
from numpy.core.numeric import asarray, asanyarray, result_type, tensordot, dot
__all__ = [
 'einsum', 'einsum_path']
einsum_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
einsum_symbols_set = set(einsum_symbols)

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
    >>> oset = set('')
    >>> idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
    >>> _path__optimal_path(isets, oset, idx_sizes, 5000)
    [(0, 2), (0, 1)]
    """
    full_results = [
     (
      0, [], input_sets)]
    for iteration in range(len(input_sets) - 1):
        iter_results = []
        comb_iter = []
        for x in range(len(input_sets) - iteration):
            for y in range(x + 1, len(input_sets) - iteration):
                comb_iter.append((x, y))

        for curr in full_results:
            cost, positions, remaining = curr
            for con in comb_iter:
                cont = _find_contraction(con, remaining, output_set)
                new_result, new_input_sets, idx_removed, idx_contract = cont
                new_size = _compute_size_by_dict(new_result, idx_dict)
                if new_size > memory_limit:
                    continue
                new_cost = _compute_size_by_dict(idx_contract, idx_dict)
                if idx_removed:
                    new_cost *= 2
                new_cost += cost
                new_pos = positions + [con]
                iter_results.append((new_cost, new_pos, new_input_sets))

        if iter_results:
            full_results = iter_results
        else:
            path = min(full_results, key=lambda x: x[0])[1]
            path += [tuple(range(len(input_sets) - iteration))]
            return path

    if len(full_results) == 0:
        return [tuple(range(len(input_sets)))]
    path = min(full_results, key=lambda x: x[0])[1]
    return path


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
    >>> oset = set('')
    >>> idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
    >>> _path__greedy_path(isets, oset, idx_sizes, 5000)
    [(0, 2), (0, 1)]
    """
    if len(input_sets) == 1:
        return [(0, )]
    path = []
    for iteration in range(len(input_sets) - 1):
        iteration_results = []
        comb_iter = []
        for x in range(len(input_sets)):
            for y in range(x + 1, len(input_sets)):
                comb_iter.append((x, y))

        for positions in comb_iter:
            contract = _find_contraction(positions, input_sets, output_set)
            idx_result, new_input_sets, idx_removed, idx_contract = contract
            if _compute_size_by_dict(idx_result, idx_dict) > memory_limit:
                continue
            removed_size = _compute_size_by_dict(idx_removed, idx_dict)
            cost = _compute_size_by_dict(idx_contract, idx_dict)
            sort = (-removed_size, cost)
            iteration_results.append([sort, positions, new_input_sets])

        if len(iteration_results) == 0:
            path.append(tuple(range(len(input_sets))))
            break
        best = min(iteration_results, key=lambda x: x[0])
        path.append(best[1])
        input_sets = best[2]

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
    if len(inputs) != 2:
        return False
    input_left, input_right = inputs
    set_left = set(input_left)
    set_right = set(input_right)
    keep_left = set_left - idx_removed
    keep_right = set_right - idx_removed
    rs = len(idx_removed)
    if not len(set_left & set_right):
        return False
    if len(set_left) != len(input_left) or len(set_right) != len(input_right):
        return False
    if len(keep_left & keep_right):
        return False
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
    if not keep_left or not keep_right:
        return False
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

    >>> a = np.random.rand(4, 4)
    >>> b = np.random.rand(4, 4, 4)
    >>> __parse_einsum_input(('...a,...a->...', a, b))
    ('za,xza', 'xz', [a, b])

    >>> __parse_einsum_input((a, [Ellipsis, 0], b, [Ellipsis, 0]))
    ('za,xza', 'xz', [a, b])
    """
    if len(operands) == 0:
        raise ValueError('No input operands')
    if isinstance(operands[0], basestring):
        subscripts = operands[0].replace(' ', '')
        operands = [asanyarray(v) for v in operands[1:]]
        for s in subscripts:
            if s in '.,->':
                continue
            if s not in einsum_symbols:
                raise ValueError('Character %s is not a valid symbol.' % s)
                continue

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
                elif isinstance(s, int):
                    subscripts += einsum_symbols[s]
                else:
                    raise TypeError('For this input type lists must contain either int or Ellipsis')

            if num != last:
                subscripts += ','
                continue

        if output_list is not None:
            subscripts += '->'
            for s in output_list:
                if s is Ellipsis:
                    subscripts += '...'
                elif isinstance(s, int):
                    subscripts += einsum_symbols[s]
                else:
                    raise TypeError('For this input type lists must contain either int or Ellipsis')

        if '-' in subscripts or '>' in subscripts:
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
                    if '.' in sub:
                        if sub.count('.') != 3 or sub.count('...') != 1:
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
                        else:
                            if ellipse_count == 0:
                                split_subscripts[num] = sub.replace('...', '')
                            else:
                                rep_inds = ellipse_inds[-ellipse_count:]
                                split_subscripts[num] = sub.replace('...', rep_inds)
                                continue

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
                            continue

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
                        continue

    for char in output_subscript:
        if char not in input_subscripts:
            raise ValueError('Output character %s did not appear in the input' % char)
            continue

    if len(input_subscripts.split(',')) != len(operands):
        raise ValueError('Number of einsum subscripts must be equal to the number of operands.')
    return (
     input_subscripts, output_subscript, operands)


def einsum_path--- This code section failed: ---

 L. 652         0  LOAD_STR                 'optimize'
                3  LOAD_STR                 'einsum_call'
                6  BUILD_LIST_2          2 
                9  STORE_DEREF              'valid_contract_kwargs'

 L. 653        12  LOAD_CLOSURE             'valid_contract_kwargs'
               15  BUILD_TUPLE_1         1 
               18  LOAD_LISTCOMP            '<code_object <listcomp>>'
               21  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
               24  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
               27  LOAD_FAST                'kwargs'
               30  LOAD_ATTR                items
               33  CALL_FUNCTION_0       0  '0 positional, 0 named'
               36  GET_ITER         
               37  CALL_FUNCTION_1       1  '1 positional, 0 named'
               40  STORE_FAST               'unknown_kwargs'

 L. 655        43  LOAD_GLOBAL              len
               46  LOAD_FAST                'unknown_kwargs'
               49  CALL_FUNCTION_1       1  '1 positional, 0 named'
               52  POP_JUMP_IF_FALSE    74  'to 74'

 L. 656        55  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 'Did not understand the following kwargs: %s'

 L. 657        61  LOAD_FAST                'unknown_kwargs'
               64  BINARY_MODULO    
               65  CALL_FUNCTION_1       1  '1 positional, 0 named'
               68  RAISE_VARARGS_1       1  'exception'
               71  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            71  '71'

 L. 660        74  LOAD_FAST                'kwargs'
               77  LOAD_ATTR                pop
               80  LOAD_STR                 'optimize'
               83  LOAD_CONST               True
               86  CALL_FUNCTION_2       2  '2 positional, 0 named'
               89  STORE_FAST               'path_type'

 L. 661        92  LOAD_FAST                'path_type'
               95  LOAD_CONST               True
               98  COMPARE_OP               is
              101  POP_JUMP_IF_FALSE   113  'to 113'

 L. 662       104  LOAD_STR                 'greedy'
              107  STORE_FAST               'path_type'
              110  JUMP_FORWARD        113  'to 113'
            113_0  COME_FROM           110  '110'

 L. 663       113  LOAD_FAST                'path_type'
              116  LOAD_CONST               None
              119  COMPARE_OP               is
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L. 664       125  LOAD_CONST               False
              128  STORE_FAST               'path_type'
              131  JUMP_FORWARD        134  'to 134'
            134_0  COME_FROM           131  '131'

 L. 666       134  LOAD_CONST               None
              137  STORE_FAST               'memory_limit'

 L. 669       140  LOAD_FAST                'path_type'
              143  LOAD_CONST               False
              146  COMPARE_OP               is
              149  POP_JUMP_IF_TRUE    314  'to 314'
              152  LOAD_GLOBAL              isinstance
              155  LOAD_FAST                'path_type'
              158  LOAD_GLOBAL              basestring
              161  CALL_FUNCTION_2       2  '2 positional, 0 named'
            164_0  COME_FROM           149  '149'
              164  POP_JUMP_IF_FALSE   170  'to 170'

 L. 670       167  JUMP_FORWARD        314  'to 314'
              170  ELSE                     '314'

 L. 673       170  LOAD_GLOBAL              len
              173  LOAD_FAST                'path_type'
              176  CALL_FUNCTION_1       1  '1 positional, 0 named'
              179  POP_JUMP_IF_FALSE   201  'to 201'
              182  LOAD_FAST                'path_type'
              185  LOAD_CONST               0
              188  BINARY_SUBSCR    
              189  LOAD_STR                 'einsum_path'
              192  COMPARE_OP               ==
            195_0  COME_FROM           179  '179'
              195  POP_JUMP_IF_FALSE   201  'to 201'

 L. 674       198  JUMP_FORWARD        314  'to 314'
              201  ELSE                     '314'

 L. 677       201  LOAD_GLOBAL              len
              204  LOAD_FAST                'path_type'
              207  CALL_FUNCTION_1       1  '1 positional, 0 named'
              210  LOAD_CONST               2
              213  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   292  'to 292'
              219  LOAD_GLOBAL              isinstance
              222  LOAD_FAST                'path_type'
              225  LOAD_CONST               0
              228  BINARY_SUBSCR    
              229  LOAD_GLOBAL              basestring
              232  CALL_FUNCTION_2       2  '2 positional, 0 named'
              235  POP_JUMP_IF_FALSE   292  'to 292'

 L. 678       238  LOAD_GLOBAL              isinstance
              241  LOAD_FAST                'path_type'
              244  LOAD_CONST               1
              247  BINARY_SUBSCR    
              248  LOAD_GLOBAL              int
              251  LOAD_GLOBAL              float
              254  BUILD_TUPLE_2         2 
              257  CALL_FUNCTION_2       2  '2 positional, 0 named'
            260_0  COME_FROM           235  '235'
            260_1  COME_FROM           216  '216'
              260  POP_JUMP_IF_FALSE   292  'to 292'

 L. 679       263  LOAD_GLOBAL              int
              266  LOAD_FAST                'path_type'
              269  LOAD_CONST               1
              272  BINARY_SUBSCR    
              273  CALL_FUNCTION_1       1  '1 positional, 0 named'
              276  STORE_FAST               'memory_limit'

 L. 680       279  LOAD_FAST                'path_type'
              282  LOAD_CONST               0
              285  BINARY_SUBSCR    
              286  STORE_FAST               'path_type'
              289  JUMP_FORWARD        314  'to 314'
              292  ELSE                     '314'

 L. 683       292  LOAD_GLOBAL              TypeError
              295  LOAD_STR                 'Did not understand the path: %s'
              298  LOAD_GLOBAL              str
              301  LOAD_FAST                'path_type'
              304  CALL_FUNCTION_1       1  '1 positional, 0 named'
              307  BINARY_MODULO    
              308  CALL_FUNCTION_1       1  '1 positional, 0 named'
              311  RAISE_VARARGS_1       1  'exception'
            314_0  COME_FROM           289  '289'
            314_1  COME_FROM           198  '198'
            314_2  COME_FROM           167  '167'

 L. 686       314  LOAD_FAST                'kwargs'
              317  LOAD_ATTR                pop
              320  LOAD_STR                 'einsum_call'
              323  LOAD_CONST               False
              326  CALL_FUNCTION_2       2  '2 positional, 0 named'
              329  STORE_FAST               'einsum_call_arg'

 L. 689       332  LOAD_GLOBAL              _parse_einsum_input
              335  LOAD_FAST                'operands'
              338  CALL_FUNCTION_1       1  '1 positional, 0 named'
              341  UNPACK_SEQUENCE_3     3 
              344  STORE_FAST               'input_subscripts'
              347  STORE_FAST               'output_subscript'
              350  STORE_FAST               'operands'

 L. 690       353  LOAD_FAST                'input_subscripts'
              356  LOAD_STR                 '->'
              359  BINARY_ADD       
              360  LOAD_FAST                'output_subscript'
              363  BINARY_ADD       
              364  STORE_FAST               'subscripts'

 L. 693       367  LOAD_FAST                'input_subscripts'
              370  LOAD_ATTR                split
              373  LOAD_STR                 ','
              376  CALL_FUNCTION_1       1  '1 positional, 0 named'
              379  STORE_FAST               'input_list'

 L. 694       382  LOAD_LISTCOMP            '<code_object <listcomp>>'
              385  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
              388  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              391  LOAD_FAST                'input_list'
              394  GET_ITER         
              395  CALL_FUNCTION_1       1  '1 positional, 0 named'
              398  STORE_FAST               'input_sets'

 L. 695       401  LOAD_GLOBAL              set
              404  LOAD_FAST                'output_subscript'
              407  CALL_FUNCTION_1       1  '1 positional, 0 named'
              410  STORE_FAST               'output_set'

 L. 696       413  LOAD_GLOBAL              set
              416  LOAD_FAST                'input_subscripts'
              419  LOAD_ATTR                replace
              422  LOAD_STR                 ','
              425  LOAD_STR                 ''
              428  CALL_FUNCTION_2       2  '2 positional, 0 named'
              431  CALL_FUNCTION_1       1  '1 positional, 0 named'
              434  STORE_FAST               'indices'

 L. 699       437  BUILD_MAP_0           0  ''
              440  STORE_DEREF              'dimension_dict'

 L. 700       443  SETUP_LOOP          694  'to 694'
              446  LOAD_GLOBAL              enumerate
              449  LOAD_FAST                'input_list'
              452  CALL_FUNCTION_1       1  '1 positional, 0 named'
              455  GET_ITER         
              456  FOR_ITER            693  'to 693'
              459  UNPACK_SEQUENCE_2     2 
              462  STORE_FAST               'tnum'
              465  STORE_FAST               'term'

 L. 701       468  LOAD_FAST                'operands'
              471  LOAD_FAST                'tnum'
              474  BINARY_SUBSCR    
              475  LOAD_ATTR                shape
              478  STORE_FAST               'sh'

 L. 702       481  LOAD_GLOBAL              len
              484  LOAD_FAST                'sh'
              487  CALL_FUNCTION_1       1  '1 positional, 0 named'
              490  LOAD_GLOBAL              len
              493  LOAD_FAST                'term'
              496  CALL_FUNCTION_1       1  '1 positional, 0 named'
              499  COMPARE_OP               !=
              502  POP_JUMP_IF_FALSE   534  'to 534'

 L. 703       505  LOAD_GLOBAL              ValueError
              508  LOAD_STR                 'Einstein sum subscript %s does not contain the correct number of indices for operand %d.'

 L. 705       511  LOAD_FAST                'input_subscripts'
              514  LOAD_FAST                'tnum'
              517  BINARY_SUBSCR    
              518  LOAD_FAST                'tnum'
              521  BUILD_TUPLE_2         2 
              524  BINARY_MODULO    
              525  CALL_FUNCTION_1       1  '1 positional, 0 named'
              528  RAISE_VARARGS_1       1  'exception'
              531  JUMP_FORWARD        534  'to 534'
            534_0  COME_FROM           531  '531'

 L. 706       534  SETUP_LOOP          690  'to 690'
              537  LOAD_GLOBAL              enumerate
              540  LOAD_FAST                'term'
              543  CALL_FUNCTION_1       1  '1 positional, 0 named'
              546  GET_ITER         
              547  FOR_ITER            689  'to 689'
              550  UNPACK_SEQUENCE_2     2 
              553  STORE_FAST               'cnum'
              556  STORE_FAST               'char'

 L. 707       559  LOAD_FAST                'sh'
              562  LOAD_FAST                'cnum'
              565  BINARY_SUBSCR    
              566  STORE_FAST               'dim'

 L. 708       569  LOAD_FAST                'char'
              572  LOAD_DEREF               'dimension_dict'
              575  LOAD_ATTR                keys
              578  CALL_FUNCTION_0       0  '0 positional, 0 named'
              581  COMPARE_OP               in
              584  POP_JUMP_IF_FALSE   676  'to 676'

 L. 710       587  LOAD_DEREF               'dimension_dict'
              590  LOAD_FAST                'char'
              593  BINARY_SUBSCR    
              594  LOAD_CONST               1
              597  COMPARE_OP               ==
              600  POP_JUMP_IF_FALSE   616  'to 616'

 L. 711       603  LOAD_FAST                'dim'
              606  LOAD_DEREF               'dimension_dict'
              609  LOAD_FAST                'char'
              612  STORE_SUBSCR     
              613  JUMP_ABSOLUTE       686  'to 686'
              616  ELSE                     '673'

 L. 712       616  LOAD_FAST                'dim'
              619  LOAD_CONST               1
              622  LOAD_DEREF               'dimension_dict'
              625  LOAD_FAST                'char'
              628  BINARY_SUBSCR    
              629  BUILD_TUPLE_2         2 
              632  COMPARE_OP               not-in
              635  POP_JUMP_IF_FALSE   686  'to 686'

 L. 713       638  LOAD_GLOBAL              ValueError
              641  LOAD_STR                 "Size of label '%s' for operand %d (%d) does not match previous terms (%d)."

 L. 715       644  LOAD_FAST                'char'
              647  LOAD_FAST                'tnum'
              650  LOAD_DEREF               'dimension_dict'
              653  LOAD_FAST                'char'
              656  BINARY_SUBSCR    
              657  LOAD_FAST                'dim'
              660  BUILD_TUPLE_4         4 
              663  BINARY_MODULO    
              664  CALL_FUNCTION_1       1  '1 positional, 0 named'
              667  RAISE_VARARGS_1       1  'exception'
              670  JUMP_ABSOLUTE       686  'to 686'
              673  JUMP_BACK           547  'to 547'

 L. 717       676  LOAD_FAST                'dim'
              679  LOAD_DEREF               'dimension_dict'
              682  LOAD_FAST                'char'
              685  STORE_SUBSCR     
              686  JUMP_BACK           547  'to 547'
              689  POP_BLOCK        
            690_0  COME_FROM_LOOP      534  '534'
              690  JUMP_BACK           456  'to 456'
              693  POP_BLOCK        
            694_0  COME_FROM_LOOP      443  '443'

 L. 720       694  BUILD_LIST_0          0 
              697  STORE_FAST               'size_list'

 L. 721       700  SETUP_LOOP          746  'to 746'
              703  LOAD_FAST                'input_list'
              706  LOAD_FAST                'output_subscript'
              709  BUILD_LIST_1          1 
              712  BINARY_ADD       
              713  GET_ITER         
              714  FOR_ITER            745  'to 745'
              717  STORE_FAST               'term'

 L. 722       720  LOAD_FAST                'size_list'
              723  LOAD_ATTR                append
              726  LOAD_GLOBAL              _compute_size_by_dict
              729  LOAD_FAST                'term'
              732  LOAD_DEREF               'dimension_dict'
              735  CALL_FUNCTION_2       2  '2 positional, 0 named'
              738  CALL_FUNCTION_1       1  '1 positional, 0 named'
              741  POP_TOP          
              742  JUMP_BACK           714  'to 714'
              745  POP_BLOCK        
            746_0  COME_FROM_LOOP      700  '700'

 L. 723       746  LOAD_GLOBAL              max
              749  LOAD_FAST                'size_list'
              752  CALL_FUNCTION_1       1  '1 positional, 0 named'
              755  STORE_FAST               'max_size'

 L. 725       758  LOAD_FAST                'memory_limit'
              761  LOAD_CONST               None
              764  COMPARE_OP               is
              767  POP_JUMP_IF_FALSE   779  'to 779'

 L. 726       770  LOAD_FAST                'max_size'
              773  STORE_FAST               'memory_arg'
              776  JUMP_FORWARD        785  'to 785'
              779  ELSE                     '785'

 L. 728       779  LOAD_FAST                'memory_limit'
              782  STORE_FAST               'memory_arg'
            785_0  COME_FROM           776  '776'

 L. 732       785  LOAD_GLOBAL              _compute_size_by_dict
              788  LOAD_FAST                'indices'
              791  LOAD_DEREF               'dimension_dict'
              794  CALL_FUNCTION_2       2  '2 positional, 0 named'
              797  STORE_FAST               'naive_cost'

 L. 733       800  LOAD_FAST                'input_subscripts'
              803  LOAD_ATTR                replace
              806  LOAD_STR                 ','
              809  LOAD_STR                 ''
              812  CALL_FUNCTION_2       2  '2 positional, 0 named'
              815  STORE_FAST               'indices_in_input'

 L. 734       818  LOAD_GLOBAL              max
              821  LOAD_GLOBAL              len
              824  LOAD_FAST                'input_list'
              827  CALL_FUNCTION_1       1  '1 positional, 0 named'
              830  LOAD_CONST               1
              833  BINARY_SUBTRACT  
              834  LOAD_CONST               1
              837  CALL_FUNCTION_2       2  '2 positional, 0 named'
              840  STORE_FAST               'mult'

 L. 735       843  LOAD_GLOBAL              len
              846  LOAD_FAST                'indices_in_input'
              849  CALL_FUNCTION_1       1  '1 positional, 0 named'
              852  LOAD_GLOBAL              len
              855  LOAD_GLOBAL              set
              858  LOAD_FAST                'indices_in_input'
              861  CALL_FUNCTION_1       1  '1 positional, 0 named'
              864  CALL_FUNCTION_1       1  '1 positional, 0 named'
              867  BINARY_SUBTRACT  
              868  POP_JUMP_IF_FALSE   884  'to 884'

 L. 736       871  LOAD_FAST                'mult'
              874  LOAD_CONST               2
              877  INPLACE_MULTIPLY 
              878  STORE_FAST               'mult'
              881  JUMP_FORWARD        884  'to 884'
            884_0  COME_FROM           881  '881'

 L. 737       884  LOAD_FAST                'naive_cost'
              887  LOAD_FAST                'mult'
              890  INPLACE_MULTIPLY 
              891  STORE_FAST               'naive_cost'

 L. 740       894  LOAD_FAST                'path_type'
              897  LOAD_CONST               False
              900  COMPARE_OP               is
              903  POP_JUMP_IF_TRUE    936  'to 936'
              906  LOAD_GLOBAL              len
              909  LOAD_FAST                'input_list'
              912  CALL_FUNCTION_1       1  '1 positional, 0 named'
              915  LOAD_CONST               (1, 2)
              918  COMPARE_OP               in
              921  POP_JUMP_IF_TRUE    936  'to 936'
              924  LOAD_FAST                'indices'
              927  LOAD_FAST                'output_set'
              930  COMPARE_OP               ==
            933_0  COME_FROM           921  '921'
            933_1  COME_FROM           903  '903'
              933  POP_JUMP_IF_FALSE   966  'to 966'

 L. 742       936  LOAD_GLOBAL              tuple
              939  LOAD_GLOBAL              range
              942  LOAD_GLOBAL              len
              945  LOAD_FAST                'input_list'
              948  CALL_FUNCTION_1       1  '1 positional, 0 named'
              951  CALL_FUNCTION_1       1  '1 positional, 0 named'
              954  CALL_FUNCTION_1       1  '1 positional, 0 named'
              957  BUILD_LIST_1          1 
              960  STORE_FAST               'path'
              963  JUMP_FORWARD       1103  'to 1103'
              966  ELSE                     '1103'

 L. 743       966  LOAD_FAST                'path_type'
              969  LOAD_STR                 'greedy'
              972  COMPARE_OP               ==
              975  POP_JUMP_IF_FALSE  1017  'to 1017'

 L. 745       978  LOAD_GLOBAL              min
              981  LOAD_FAST                'memory_arg'
              984  LOAD_FAST                'max_size'
              987  CALL_FUNCTION_2       2  '2 positional, 0 named'
              990  STORE_FAST               'memory_arg'

 L. 746       993  LOAD_GLOBAL              _greedy_path
              996  LOAD_FAST                'input_sets'
              999  LOAD_FAST                'output_set'
             1002  LOAD_DEREF               'dimension_dict'
             1005  LOAD_FAST                'memory_arg'
             1008  CALL_FUNCTION_4       4  '4 positional, 0 named'
             1011  STORE_FAST               'path'
             1014  JUMP_FORWARD       1103  'to 1103'
             1017  ELSE                     '1103'

 L. 747      1017  LOAD_FAST                'path_type'
             1020  LOAD_STR                 'optimal'
             1023  COMPARE_OP               ==
             1026  POP_JUMP_IF_FALSE  1053  'to 1053'

 L. 748      1029  LOAD_GLOBAL              _optimal_path
             1032  LOAD_FAST                'input_sets'
             1035  LOAD_FAST                'output_set'
             1038  LOAD_DEREF               'dimension_dict'
             1041  LOAD_FAST                'memory_arg'
             1044  CALL_FUNCTION_4       4  '4 positional, 0 named'
             1047  STORE_FAST               'path'
             1050  JUMP_FORWARD       1103  'to 1103'
             1053  ELSE                     '1103'

 L. 749      1053  LOAD_FAST                'path_type'
             1056  LOAD_CONST               0
             1059  BINARY_SUBSCR    
             1060  LOAD_STR                 'einsum_path'
             1063  COMPARE_OP               ==
             1066  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 750      1069  LOAD_FAST                'path_type'
             1072  LOAD_CONST               1
             1075  LOAD_CONST               None
             1078  BUILD_SLICE_2         2 
             1081  BINARY_SUBSCR    
             1082  STORE_FAST               'path'
             1085  JUMP_FORWARD       1103  'to 1103'
             1088  ELSE                     '1103'

 L. 752      1088  LOAD_GLOBAL              KeyError
             1091  LOAD_STR                 'Path name %s not found'
             1094  LOAD_FAST                'path_type'
             1097  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1100  RAISE_VARARGS_1       1  'exception'
           1103_0  COME_FROM          1085  '1085'
           1103_1  COME_FROM          1050  '1050'
           1103_2  COME_FROM          1014  '1014'
           1103_3  COME_FROM           963  '963'

 L. 754      1103  BUILD_LIST_0          0 
             1106  BUILD_LIST_0          0 
             1109  BUILD_LIST_0          0 
             1112  BUILD_LIST_0          0 
             1115  BUILD_TUPLE_4         4 
             1118  UNPACK_SEQUENCE_4     4 
             1121  STORE_FAST               'cost_list'
             1124  STORE_FAST               'scale_list'
             1127  STORE_FAST               'size_list'
             1130  STORE_FAST               'contraction_list'

 L. 757      1133  SETUP_LOOP         1549  'to 1549'
             1136  LOAD_GLOBAL              enumerate
             1139  LOAD_FAST                'path'
             1142  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1145  GET_ITER         
             1146  FOR_ITER           1548  'to 1548'
             1149  UNPACK_SEQUENCE_2     2 
             1152  STORE_FAST               'cnum'
             1155  STORE_FAST               'contract_inds'

 L. 759      1158  LOAD_GLOBAL              tuple
             1161  LOAD_GLOBAL              sorted
             1164  LOAD_GLOBAL              list
             1167  LOAD_FAST                'contract_inds'
             1170  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1173  LOAD_STR                 'reverse'
             1176  LOAD_CONST               True
             1179  CALL_FUNCTION_257   257  '1 positional, 1 named'
             1182  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1185  STORE_FAST               'contract_inds'

 L. 761      1188  LOAD_GLOBAL              _find_contraction
             1191  LOAD_FAST                'contract_inds'
             1194  LOAD_FAST                'input_sets'
             1197  LOAD_FAST                'output_set'
             1200  CALL_FUNCTION_3       3  '3 positional, 0 named'
             1203  STORE_FAST               'contract'

 L. 762      1206  LOAD_FAST                'contract'
             1209  UNPACK_SEQUENCE_4     4 
             1212  STORE_FAST               'out_inds'
             1215  STORE_FAST               'input_sets'
             1218  STORE_FAST               'idx_removed'
             1221  STORE_FAST               'idx_contract'

 L. 764      1224  LOAD_GLOBAL              _compute_size_by_dict
             1227  LOAD_FAST                'idx_contract'
             1230  LOAD_DEREF               'dimension_dict'
             1233  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1236  STORE_FAST               'cost'

 L. 765      1239  LOAD_FAST                'idx_removed'
             1242  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 766      1245  LOAD_FAST                'cost'
             1248  LOAD_CONST               2
             1251  INPLACE_MULTIPLY 
             1252  STORE_FAST               'cost'
             1255  JUMP_FORWARD       1258  'to 1258'
           1258_0  COME_FROM          1255  '1255'

 L. 767      1258  LOAD_FAST                'cost_list'
             1261  LOAD_ATTR                append
             1264  LOAD_FAST                'cost'
             1267  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1270  POP_TOP          

 L. 768      1271  LOAD_FAST                'scale_list'
             1274  LOAD_ATTR                append
             1277  LOAD_GLOBAL              len
             1280  LOAD_FAST                'idx_contract'
             1283  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1286  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1289  POP_TOP          

 L. 769      1290  LOAD_FAST                'size_list'
             1293  LOAD_ATTR                append
             1296  LOAD_GLOBAL              _compute_size_by_dict
             1299  LOAD_FAST                'out_inds'
             1302  LOAD_DEREF               'dimension_dict'
             1305  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1308  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1311  POP_TOP          

 L. 771      1312  BUILD_LIST_0          0 
             1315  STORE_FAST               'tmp_inputs'

 L. 772      1318  SETUP_LOOP         1357  'to 1357'
             1321  LOAD_FAST                'contract_inds'
             1324  GET_ITER         
             1325  FOR_ITER           1356  'to 1356'
             1328  STORE_FAST               'x'

 L. 773      1331  LOAD_FAST                'tmp_inputs'
             1334  LOAD_ATTR                append
             1337  LOAD_FAST                'input_list'
             1340  LOAD_ATTR                pop
             1343  LOAD_FAST                'x'
             1346  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1349  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1352  POP_TOP          
             1353  JUMP_BACK          1325  'to 1325'
             1356  POP_BLOCK        
           1357_0  COME_FROM_LOOP     1318  '1318'

 L. 775      1357  LOAD_GLOBAL              _can_dot
             1360  LOAD_FAST                'tmp_inputs'
             1363  LOAD_FAST                'out_inds'
             1366  LOAD_FAST                'idx_removed'
             1369  CALL_FUNCTION_3       3  '3 positional, 0 named'
             1372  STORE_FAST               'do_blas'

 L. 778      1375  LOAD_FAST                'cnum'
             1378  LOAD_GLOBAL              len
             1381  LOAD_FAST                'path'
             1384  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1387  BINARY_SUBTRACT  
             1388  LOAD_CONST               -1
             1391  COMPARE_OP               ==
             1394  POP_JUMP_IF_FALSE  1406  'to 1406'

 L. 779      1397  LOAD_FAST                'output_subscript'
             1400  STORE_FAST               'idx_result'
             1403  JUMP_FORWARD       1465  'to 1465'
             1406  ELSE                     '1465'

 L. 781      1406  LOAD_CLOSURE             'dimension_dict'
             1409  BUILD_TUPLE_1         1 
             1412  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1415  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
             1418  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
             1421  LOAD_FAST                'out_inds'
             1424  GET_ITER         
             1425  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1428  STORE_FAST               'sort_result'

 L. 782      1431  LOAD_STR                 ''
             1434  LOAD_ATTR                join
             1437  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1440  LOAD_STR                 'einsum_path.<locals>.<listcomp>'
             1443  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
             1446  LOAD_GLOBAL              sorted
             1449  LOAD_FAST                'sort_result'
             1452  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1455  GET_ITER         
             1456  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1459  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1462  STORE_FAST               'idx_result'
           1465_0  COME_FROM          1403  '1403'

 L. 784      1465  LOAD_FAST                'input_list'
             1468  LOAD_ATTR                append
             1471  LOAD_FAST                'idx_result'
             1474  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1477  POP_TOP          

 L. 785      1478  LOAD_STR                 ','
             1481  LOAD_ATTR                join
             1484  LOAD_FAST                'tmp_inputs'
             1487  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1490  LOAD_STR                 '->'
             1493  BINARY_ADD       
             1494  LOAD_FAST                'idx_result'
             1497  BINARY_ADD       
             1498  STORE_FAST               'einsum_str'

 L. 787      1501  LOAD_FAST                'contract_inds'
             1504  LOAD_FAST                'idx_removed'
             1507  LOAD_FAST                'einsum_str'
             1510  LOAD_FAST                'input_list'
             1513  LOAD_CONST               None
             1516  LOAD_CONST               None
             1519  BUILD_SLICE_2         2 
             1522  BINARY_SUBSCR    
             1523  LOAD_FAST                'do_blas'
             1526  BUILD_TUPLE_5         5 
             1529  STORE_FAST               'contraction'

 L. 788      1532  LOAD_FAST                'contraction_list'
             1535  LOAD_ATTR                append
             1538  LOAD_FAST                'contraction'
             1541  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1544  POP_TOP          
             1545  JUMP_BACK          1146  'to 1146'
             1548  POP_BLOCK        
           1549_0  COME_FROM_LOOP     1133  '1133'

 L. 790      1549  LOAD_GLOBAL              sum
             1552  LOAD_FAST                'cost_list'
             1555  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1558  LOAD_CONST               1
             1561  BINARY_ADD       
             1562  STORE_FAST               'opt_cost'

 L. 792      1565  LOAD_FAST                'einsum_call_arg'
             1568  POP_JUMP_IF_FALSE  1581  'to 1581'

 L. 793      1571  LOAD_FAST                'operands'
             1574  LOAD_FAST                'contraction_list'
             1577  BUILD_TUPLE_2         2 
             1580  RETURN_END_IF    
           1581_0  COME_FROM          1568  '1568'

 L. 796      1581  LOAD_FAST                'input_subscripts'
             1584  LOAD_STR                 '->'
             1587  BINARY_ADD       
             1588  LOAD_FAST                'output_subscript'
             1591  BINARY_ADD       
             1592  STORE_FAST               'overall_contraction'

 L. 797      1595  LOAD_CONST               ('scaling', 'current', 'remaining')
             1598  STORE_FAST               'header'

 L. 799      1601  LOAD_FAST                'naive_cost'
             1604  LOAD_FAST                'opt_cost'
             1607  BINARY_TRUE_DIVIDE
             1608  STORE_FAST               'speedup'

 L. 800      1611  LOAD_GLOBAL              max
             1614  LOAD_FAST                'size_list'
             1617  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1620  STORE_FAST               'max_i'

 L. 802      1623  LOAD_STR                 '  Complete contraction:  %s\n'
             1626  LOAD_FAST                'overall_contraction'
             1629  BINARY_MODULO    
             1630  STORE_FAST               'path_print'

 L. 803      1633  LOAD_FAST                'path_print'
             1636  LOAD_STR                 '         Naive scaling:  %d\n'
             1639  LOAD_GLOBAL              len
             1642  LOAD_FAST                'indices'
             1645  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1648  BINARY_MODULO    
             1649  INPLACE_ADD      
             1650  STORE_FAST               'path_print'

 L. 804      1653  LOAD_FAST                'path_print'
             1656  LOAD_STR                 '     Optimized scaling:  %d\n'
             1659  LOAD_GLOBAL              max
             1662  LOAD_FAST                'scale_list'
             1665  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1668  BINARY_MODULO    
             1669  INPLACE_ADD      
             1670  STORE_FAST               'path_print'

 L. 805      1673  LOAD_FAST                'path_print'
             1676  LOAD_STR                 '      Naive FLOP count:  %.3e\n'
             1679  LOAD_FAST                'naive_cost'
             1682  BINARY_MODULO    
             1683  INPLACE_ADD      
             1684  STORE_FAST               'path_print'

 L. 806      1687  LOAD_FAST                'path_print'
             1690  LOAD_STR                 '  Optimized FLOP count:  %.3e\n'
             1693  LOAD_FAST                'opt_cost'
             1696  BINARY_MODULO    
             1697  INPLACE_ADD      
             1698  STORE_FAST               'path_print'

 L. 807      1701  LOAD_FAST                'path_print'
             1704  LOAD_STR                 '   Theoretical speedup:  %3.3f\n'
             1707  LOAD_FAST                'speedup'
             1710  BINARY_MODULO    
             1711  INPLACE_ADD      
             1712  STORE_FAST               'path_print'

 L. 808      1715  LOAD_FAST                'path_print'
             1718  LOAD_STR                 '  Largest intermediate:  %.3e elements\n'
             1721  LOAD_FAST                'max_i'
             1724  BINARY_MODULO    
             1725  INPLACE_ADD      
             1726  STORE_FAST               'path_print'

 L. 809      1729  LOAD_FAST                'path_print'
             1732  LOAD_STR                 '-'
             1735  LOAD_CONST               74
             1738  BINARY_MULTIPLY  
             1739  LOAD_STR                 '\n'
             1742  BINARY_ADD       
             1743  INPLACE_ADD      
             1744  STORE_FAST               'path_print'

 L. 810      1747  LOAD_FAST                'path_print'
             1750  LOAD_STR                 '%6s %24s %40s\n'
             1753  LOAD_FAST                'header'
             1756  BINARY_MODULO    
             1757  INPLACE_ADD      
             1758  STORE_FAST               'path_print'

 L. 811      1761  LOAD_FAST                'path_print'
             1764  LOAD_STR                 '-'
             1767  LOAD_CONST               74
             1770  BINARY_MULTIPLY  
             1771  INPLACE_ADD      
             1772  STORE_FAST               'path_print'

 L. 813      1775  SETUP_LOOP         1881  'to 1881'
             1778  LOAD_GLOBAL              enumerate
             1781  LOAD_FAST                'contraction_list'
             1784  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1787  GET_ITER         
             1788  FOR_ITER           1880  'to 1880'
             1791  UNPACK_SEQUENCE_2     2 
             1794  STORE_FAST               'n'
             1797  STORE_FAST               'contraction'

 L. 814      1800  LOAD_FAST                'contraction'
             1803  UNPACK_SEQUENCE_5     5 
             1806  STORE_FAST               'inds'
             1809  STORE_FAST               'idx_rm'
             1812  STORE_FAST               'einsum_str'
             1815  STORE_FAST               'remaining'
             1818  STORE_FAST               'blas'

 L. 815      1821  LOAD_STR                 ','
             1824  LOAD_ATTR                join
             1827  LOAD_FAST                'remaining'
             1830  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1833  LOAD_STR                 '->'
             1836  BINARY_ADD       
             1837  LOAD_FAST                'output_subscript'
             1840  BINARY_ADD       
             1841  STORE_FAST               'remaining_str'

 L. 816      1844  LOAD_FAST                'scale_list'
             1847  LOAD_FAST                'n'
             1850  BINARY_SUBSCR    
             1851  LOAD_FAST                'einsum_str'
             1854  LOAD_FAST                'remaining_str'
             1857  BUILD_TUPLE_3         3 
             1860  STORE_FAST               'path_run'

 L. 817      1863  LOAD_FAST                'path_print'
             1866  LOAD_STR                 '\n%4d    %24s %40s'
             1869  LOAD_FAST                'path_run'
             1872  BINARY_MODULO    
             1873  INPLACE_ADD      
             1874  STORE_FAST               'path_print'
             1877  JUMP_BACK          1788  'to 1788'
             1880  POP_BLOCK        
           1881_0  COME_FROM_LOOP     1775  '1775'

 L. 819      1881  LOAD_STR                 'einsum_path'
             1884  BUILD_LIST_1          1 
             1887  LOAD_FAST                'path'
             1890  BINARY_ADD       
             1891  STORE_FAST               'path'

 L. 820      1894  LOAD_FAST                'path'
             1897  LOAD_FAST                'path_print'
             1900  BUILD_TUPLE_2         2 
             1903  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 164


def einsum(*operands, **kwargs):
    """
    einsum(subscripts, *operands, out=None, dtype=None, order='K',
           casting='safe', optimize=False)

    Evaluates the Einstein summation convention on the operands.

    Using the Einstein summation convention, many common multi-dimensional
    array operations can be represented in a simple fashion.  This function
    provides a way to compute such summations. The best way to understand this
    function is to try the examples below, which show how many common NumPy
    functions can be implemented as calls to `einsum`.

    Parameters
    ----------
    subscripts : str
        Specifies the subscripts for summation.
    operands : list of array_like
        These are the arrays for the operation.
    out : {ndarray, None}, optional
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
        function. See ``np.einsum_path`` for more details. Default is False.

    Returns
    -------
    output : ndarray
        The calculation based on the Einstein summation convention.

    See Also
    --------
    einsum_path, dot, inner, outer, tensordot, linalg.multi_dot

    Notes
    -----
    .. versionadded:: 1.6.0

    The subscripts string is a comma-separated list of subscript labels,
    where each label refers to a dimension of the corresponding operand.
    Repeated subscripts labels in one operand take the diagonal.  For example,
    ``np.einsum('ii', a)`` is equivalent to ``np.trace(a)``.

    Whenever a label is repeated, it is summed, so ``np.einsum('i,i', a, b)``
    is equivalent to ``np.inner(a,b)``.  If a label appears only once,
    it is not summed, so ``np.einsum('i', a)`` produces a view of ``a``
    with no changes.

    The order of labels in the output is by default alphabetical.  This
    means that ``np.einsum('ij', a)`` doesn't affect a 2D array, while
    ``np.einsum('ji', a)`` takes its transpose.

    The output can be controlled by specifying output subscript labels
    as well.  This specifies the label order, and allows summing to
    be disallowed or forced when desired.  The call ``np.einsum('i->', a)``
    is like ``np.sum(a, axis=-1)``, and ``np.einsum('ii->i', a)``
    is like ``np.diag(a)``.  The difference is that `einsum` does not
    allow broadcasting by default.

    To enable and control broadcasting, use an ellipsis.  Default
    NumPy-style broadcasting is done by adding an ellipsis
    to the left of each term, like ``np.einsum('...ii->...i', a)``.
    To take the trace along the first and last axes,
    you can do ``np.einsum('i...i', a)``, or to do a matrix-matrix
    product with the left-most indices instead of rightmost, you can do
    ``np.einsum('ij...,jk...->ik...', a, b)``.

    When there is only one operand, no axes are summed, and no output
    parameter is provided, a view into the operand is returned instead
    of a new array.  Thus, taking the diagonal as ``np.einsum('ii->i', a)``
    produces a view.

    An alternative way to provide the subscripts and operands is as
    ``einsum(op0, sublist0, op1, sublist1, ..., [sublistout])``. The examples
    below have corresponding `einsum` calls with the two parameter methods.

    .. versionadded:: 1.10.0

    Views returned from einsum are now writeable whenever the input array
    is writeable. For example, ``np.einsum('ijk...->kji...', a)`` will now
    have the same effect as ``np.swapaxes(a, 0, 2)`` and
    ``np.einsum('ii->i', a)`` will return a writeable view of the diagonal
    of a 2D array.

    .. versionadded:: 1.12.0

    Added the ``optimize`` argument which will optimize the contraction order
    of an einsum expression. For a contraction with three or more operands this
    can greatly increase the computational efficiency at the cost of a larger
    memory footprint during computation.

    See ``np.einsum_path`` for more details.

    Examples
    --------
    >>> a = np.arange(25).reshape(5,5)
    >>> b = np.arange(5)
    >>> c = np.arange(6).reshape(2,3)

    >>> np.einsum('ii', a)
    60
    >>> np.einsum(a, [0,0])
    60
    >>> np.trace(a)
    60

    >>> np.einsum('ii->i', a)
    array([ 0,  6, 12, 18, 24])
    >>> np.einsum(a, [0,0], [0])
    array([ 0,  6, 12, 18, 24])
    >>> np.diag(a)
    array([ 0,  6, 12, 18, 24])

    >>> np.einsum('ij,j', a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum(a, [0,1], b, [1])
    array([ 30,  80, 130, 180, 230])
    >>> np.dot(a, b)
    array([ 30,  80, 130, 180, 230])
    >>> np.einsum('...j,j', a, b)
    array([ 30,  80, 130, 180, 230])

    >>> np.einsum('ji', c)
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> np.einsum(c, [1,0])
    array([[0, 3],
           [1, 4],
           [2, 5]])
    >>> c.T
    array([[0, 3],
           [1, 4],
           [2, 5]])

    >>> np.einsum('..., ...', 3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(',ij', 3, C)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.einsum(3, [Ellipsis], c, [Ellipsis])
    array([[ 0,  3,  6],
           [ 9, 12, 15]])
    >>> np.multiply(3, c)
    array([[ 0,  3,  6],
           [ 9, 12, 15]])

    >>> np.einsum('i,i', b, b)
    30
    >>> np.einsum(b, [0], b, [0])
    30
    >>> np.inner(b,b)
    30

    >>> np.einsum('i,j', np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.einsum(np.arange(2)+1, [0], b, [1])
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])
    >>> np.outer(np.arange(2)+1, b)
    array([[0, 1, 2, 3, 4],
           [0, 2, 4, 6, 8]])

    >>> np.einsum('i...->...', a)
    array([50, 55, 60, 65, 70])
    >>> np.einsum(a, [0,Ellipsis], [Ellipsis])
    array([50, 55, 60, 65, 70])
    >>> np.sum(a, axis=0)
    array([50, 55, 60, 65, 70])

    >>> a = np.arange(60.).reshape(3,4,5)
    >>> b = np.arange(24.).reshape(4,3,2)
    >>> np.einsum('ijk,jil->kl', a, b)
    array([[ 4400.,  4730.],
           [ 4532.,  4874.],
           [ 4664.,  5018.],
           [ 4796.,  5162.],
           [ 4928.,  5306.]])
    >>> np.einsum(a, [0,1,2], b, [1,0,3], [2,3])
    array([[ 4400.,  4730.],
           [ 4532.,  4874.],
           [ 4664.,  5018.],
           [ 4796.,  5162.],
           [ 4928.,  5306.]])
    >>> np.tensordot(a,b, axes=([1,0],[0,1]))
    array([[ 4400.,  4730.],
           [ 4532.,  4874.],
           [ 4664.,  5018.],
           [ 4796.,  5162.],
           [ 4928.,  5306.]])

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

    >>> # since version 1.10.0
    >>> a = np.zeros((3, 3))
    >>> np.einsum('ii->i', a)[:] = 1
    >>> a
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])

    """
    optimize_arg = kwargs.pop('optimize', False)
    if optimize_arg is False:
        return c_einsum(*operands, **kwargs)
    else:
        valid_einsum_kwargs = [
         'out', 'dtype', 'order', 'casting']
        einsum_kwargs = {k:v for k, v in kwargs.items() if k in valid_einsum_kwargs}
        valid_contract_kwargs = [
         'optimize'] + valid_einsum_kwargs
        unknown_kwargs = [k for k, v in kwargs.items() if k not in valid_contract_kwargs]
        if len(unknown_kwargs):
            raise TypeError('Did not understand the following kwargs: %s' % unknown_kwargs)
        specified_out = False
        out_array = einsum_kwargs.pop('out', None)
        if out_array is not None:
            specified_out = True
        operands, contraction_list = einsum_path(*operands, optimize=optimize_arg, einsum_call=True)
        handle_out = False
        for num, contraction in enumerate(contraction_list):
            inds, idx_rm, einsum_str, remaining, blas = contraction
            tmp_operands = []
            for x in inds:
                tmp_operands.append(operands.pop(x))

            if specified_out:
                if num + 1 == len(contraction_list):
                    handle_out = True
            if blas:
                input_str, results_index = einsum_str.split('->')
                input_left, input_right = input_str.split(',')
                if 1 in tmp_operands[0].shape or 1 in tmp_operands[1].shape:
                    left_dims = {dim:size for dim, size in zip(input_left, tmp_operands[0].shape)}
                    right_dims = {dim:size for dim, size in zip(input_right, tmp_operands[1].shape)}
                    if any(left_dims[ind] != right_dims[ind] for ind in idx_rm):
                        blas = False
                if blas:
                    tensor_result = input_left + input_right
                    for s in idx_rm:
                        tensor_result = tensor_result.replace(s, '')

                    left_pos, right_pos = [], []
                    for s in idx_rm:
                        left_pos.append(input_left.find(s))
                        right_pos.append(input_right.find(s))

                    new_view = tensordot(*tmp_operands, axes=(tuple(left_pos), tuple(right_pos)))
                    if tensor_result != results_index or handle_out:
                        if handle_out:
                            einsum_kwargs['out'] = out_array
                        new_view = c_einsum((tensor_result + '->' + results_index), new_view, **einsum_kwargs)
                else:
                    if handle_out:
                        einsum_kwargs['out'] = out_array
                    new_view = c_einsum(einsum_str, *tmp_operands, **einsum_kwargs)
                operands.append(new_view)
                del tmp_operands
                del new_view

        if specified_out:
            return out_array
        return operands[0]