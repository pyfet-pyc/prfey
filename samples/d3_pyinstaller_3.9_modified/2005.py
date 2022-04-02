# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\lib\mixins.py
"""Mixin classes for custom array types that don't inherit from ndarray."""
import numpy.core as um
__all__ = [
 'NDArrayOperatorsMixin']

def _disables_array_ufunc--- This code section failed: ---

 L.  10         0  SETUP_FINALLY        14  'to 14'

 L.  11         2  LOAD_FAST                'obj'
                4  LOAD_ATTR                __array_ufunc__
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  12        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  <121>                32  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  13        26  POP_EXCEPT       
               28  LOAD_CONST               False
               30  RETURN_VALUE     
               32  <48>             

Parse error at or near `<117>' instruction at offset 8


def _binary_method(ufunc, name):
    """Implement a forward binary method with a ufunc, e.g., __add__."""

    def func(self, other):
        if _disables_array_ufunc(other):
            return NotImplemented
        return ufunc(self, other)

    func.__name__ = '__{}__'.format(name)
    return func


def _reflected_binary_method(ufunc, name):
    """Implement a reflected binary method with a ufunc, e.g., __radd__."""

    def func(self, other):
        if _disables_array_ufunc(other):
            return NotImplemented
        return ufunc(other, self)

    func.__name__ = '__r{}__'.format(name)
    return func


def _inplace_binary_method(ufunc, name):
    """Implement an in-place binary method with a ufunc, e.g., __iadd__."""

    def func(self, other):
        return ufunc(self, other, out=(self,))

    func.__name__ = '__i{}__'.format(name)
    return func


def _numeric_methods(ufunc, name):
    """Implement forward, reflected and inplace binary methods with a ufunc."""
    return (
     _binary_method(ufunc, name),
     _reflected_binary_method(ufunc, name),
     _inplace_binary_method(ufunc, name))


def _unary_method(ufunc, name):
    """Implement a unary special method with a ufunc."""

    def func(self):
        return ufunc(self)

    func.__name__ = '__{}__'.format(name)
    return func


class NDArrayOperatorsMixin:
    __doc__ = "Mixin defining all operator special methods using __array_ufunc__.\n\n    This class implements the special methods for almost all of Python's\n    builtin operators defined in the `operator` module, including comparisons\n    (``==``, ``>``, etc.) and arithmetic (``+``, ``*``, ``-``, etc.), by\n    deferring to the ``__array_ufunc__`` method, which subclasses must\n    implement.\n\n    It is useful for writing classes that do not inherit from `numpy.ndarray`,\n    but that should support arithmetic and numpy universal functions like\n    arrays as described in `A Mechanism for Overriding Ufuncs\n    <../../neps/nep-0013-ufunc-overrides.html>`_.\n\n    As an trivial example, consider this implementation of an ``ArrayLike``\n    class that simply wraps a NumPy array and ensures that the result of any\n    arithmetic operation is also an ``ArrayLike`` object::\n\n        class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin):\n            def __init__(self, value):\n                self.value = np.asarray(value)\n\n            # One might also consider adding the built-in list type to this\n            # list, to support operations like np.add(array_like, list)\n            _HANDLED_TYPES = (np.ndarray, numbers.Number)\n\n            def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):\n                out = kwargs.get('out', ())\n                for x in inputs + out:\n                    # Only support operations with instances of _HANDLED_TYPES.\n                    # Use ArrayLike instead of type(self) for isinstance to\n                    # allow subclasses that don't override __array_ufunc__ to\n                    # handle ArrayLike objects.\n                    if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):\n                        return NotImplemented\n\n                # Defer to the implementation of the ufunc on unwrapped values.\n                inputs = tuple(x.value if isinstance(x, ArrayLike) else x\n                               for x in inputs)\n                if out:\n                    kwargs['out'] = tuple(\n                        x.value if isinstance(x, ArrayLike) else x\n                        for x in out)\n                result = getattr(ufunc, method)(*inputs, **kwargs)\n\n                if type(result) is tuple:\n                    # multiple return values\n                    return tuple(type(self)(x) for x in result)\n                elif method == 'at':\n                    # no return value\n                    return None\n                else:\n                    # one return value\n                    return type(self)(result)\n\n            def __repr__(self):\n                return '%s(%r)' % (type(self).__name__, self.value)\n\n    In interactions between ``ArrayLike`` objects and numbers or numpy arrays,\n    the result is always another ``ArrayLike``:\n\n        >>> x = ArrayLike([1, 2, 3])\n        >>> x - 1\n        ArrayLike(array([0, 1, 2]))\n        >>> 1 - x\n        ArrayLike(array([ 0, -1, -2]))\n        >>> np.arange(3) - x\n        ArrayLike(array([-1, -1, -1]))\n        >>> x - np.arange(3)\n        ArrayLike(array([1, 1, 1]))\n\n    Note that unlike ``numpy.ndarray``, ``ArrayLike`` does not allow operations\n    with arbitrary, unrecognized types. This ensures that interactions with\n    ArrayLike preserve a well-defined casting hierarchy.\n\n    .. versionadded:: 1.13\n    "
    __lt__ = _binary_method(um.less, 'lt')
    __le__ = _binary_method(um.less_equal, 'le')
    __eq__ = _binary_method(um.equal, 'eq')
    __ne__ = _binary_method(um.not_equal, 'ne')
    __gt__ = _binary_method(um.greater, 'gt')
    __ge__ = _binary_method(um.greater_equal, 'ge')
    __add__, __radd__, __iadd__ = _numeric_methods(um.add, 'add')
    __sub__, __rsub__, __isub__ = _numeric_methods(um.subtract, 'sub')
    __mul__, __rmul__, __imul__ = _numeric_methods(um.multiply, 'mul')
    __matmul__, __rmatmul__, __imatmul__ = _numeric_methods(um.matmul, 'matmul')
    __truediv__, __rtruediv__, __itruediv__ = _numeric_methods(um.true_divide, 'truediv')
    __floordiv__, __rfloordiv__, __ifloordiv__ = _numeric_methods(um.floor_divide, 'floordiv')
    __mod__, __rmod__, __imod__ = _numeric_methods(um.remainder, 'mod')
    __divmod__ = _binary_method(um.divmod, 'divmod')
    __rdivmod__ = _reflected_binary_method(um.divmod, 'divmod')
    __pow__, __rpow__, __ipow__ = _numeric_methods(um.power, 'pow')
    __lshift__, __rlshift__, __ilshift__ = _numeric_methods(um.left_shift, 'lshift')
    __rshift__, __rrshift__, __irshift__ = _numeric_methods(um.right_shift, 'rshift')
    __and__, __rand__, __iand__ = _numeric_methods(um.bitwise_and, 'and')
    __xor__, __rxor__, __ixor__ = _numeric_methods(um.bitwise_xor, 'xor')
    __or__, __ror__, __ior__ = _numeric_methods(um.bitwise_or, 'or')
    __neg__ = _unary_method(um.negative, 'neg')
    __pos__ = _unary_method(um.positive, 'pos')
    __abs__ = _unary_method(um.absolute, 'abs')
    __invert__ = _unary_method(um.invert, 'invert')