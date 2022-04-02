# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: copy.py
"""Generic (shallow and deep) copying operations.

Interface summary:

        import copy

        x = copy.copy(y)        # make a shallow copy of y
        x = copy.deepcopy(y)    # make a deep copy of y

For module specific errors, copy.Error is raised.

The difference between shallow and deep copying is only relevant for
compound objects (objects that contain other objects, like lists or
class instances).

- A shallow copy constructs a new compound object and then (to the
  extent possible) inserts *the same objects* into it that the
  original contains.

- A deep copy constructs a new compound object and then, recursively,
  inserts *copies* into it of the objects found in the original.

Two problems often exist with deep copy operations that don't exist
with shallow copy operations:

 a) recursive objects (compound objects that, directly or indirectly,
    contain a reference to themselves) may cause a recursive loop

 b) because deep copy copies *everything* it may copy too much, e.g.
    administrative data structures that should be shared even between
    copies

Python's deep copy operation avoids these problems by:

 a) keeping a table of objects already copied during the current
    copying pass

 b) letting user-defined classes override the copying operation or the
    set of components copied

This version does not copy types like module, class, function, method,
nor stack trace, stack frame, nor file, socket, window, nor array, nor
any similar types.

Classes can use the same interfaces to control copying that they use
to control pickling: they can define methods called __getinitargs__(),
__getstate__() and __setstate__().  See the documentation for module
"pickle" for information on these methods.
"""
import types, weakref
from copyreg import dispatch_table

class Error(Exception):
    pass


error = Error
try:
    from org.python.core import PyStringMap
except ImportError:
    PyStringMap = None
else:
    __all__ = [
     'Error', 'copy', 'deepcopy']

    def copy(x):
        """Shallow copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    """
        cls = type(x)
        copier = _copy_dispatch.get(cls)
        if copier:
            return copier(x)
        if issubclass(cls, type):
            return _copy_immutable(x)
        copier = getattr(cls, '__copy__', None)
        if copier is not None:
            return copier(x)
        reductor = dispatch_table.get(cls)
        if reductor is not None:
            rv = reductor(x)
        else:
            reductor = getattr(x, '__reduce_ex__', None)
            if reductor is not None:
                rv = reductor(4)
            else:
                reductor = getattr(x, '__reduce__', None)
                if reductor:
                    rv = reductor()
                else:
                    raise Error('un(shallow)copyable object of type %s' % cls)
        if isinstance(rv, str):
            return x
        return _reconstruct(x, None, *rv)


    _copy_dispatch = d = {}

    def _copy_immutable(x):
        return x


for t in (
 type(None), int, float, bool, complex, str, tuple,
 bytes, frozenset, type, range, slice, property,
 types.BuiltinFunctionType, type(Ellipsis), type(NotImplemented),
 types.FunctionType, weakref.ref):
    d[t] = _copy_immutable
else:
    t = getattr(types, 'CodeType', None)
    if t is not None:
        d[t] = _copy_immutable
    d[list] = list.copy
    d[dict] = dict.copy
    d[set] = set.copy
    d[bytearray] = bytearray.copy
    if PyStringMap is not None:
        d[PyStringMap] = PyStringMap.copy
    del d
    del t

    def deepcopy(x, memo=None, _nil=[]):
        """Deep copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    """
        if memo is None:
            memo = {}
        d = id(x)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y
        cls = type(x)
        copier = _deepcopy_dispatch.get(cls)
        if copier is not None:
            y = copier(x, memo)
        elif issubclass(cls, type):
            y = _deepcopy_atomic(x, memo)
        else:
            copier = getattr(x, '__deepcopy__', None)
            if copier is not None:
                y = copier(memo)
            else:
                reductor = dispatch_table.get(cls)
                if reductor:
                    rv = reductor(x)
                else:
                    reductor = getattr(x, '__reduce_ex__', None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(x, '__reduce__', None)
                        if reductor:
                            rv = reductor()
                        else:
                            raise Error('un(deep)copyable object of type %s' % cls)
                if isinstance(rv, str):
                    y = x
                else:
                    y = _reconstruct(x, memo, *rv)
        if y is not x:
            memo[d] = y
            _keep_alive(x, memo)
        return y


    _deepcopy_dispatch = d = {}

    def _deepcopy_atomic(x, memo):
        return x


    d[type(None)] = _deepcopy_atomic
    d[type(Ellipsis)] = _deepcopy_atomic
    d[type(NotImplemented)] = _deepcopy_atomic
    d[int] = _deepcopy_atomic
    d[float] = _deepcopy_atomic
    d[bool] = _deepcopy_atomic
    d[complex] = _deepcopy_atomic
    d[bytes] = _deepcopy_atomic
    d[str] = _deepcopy_atomic
    d[types.CodeType] = _deepcopy_atomic
    d[type] = _deepcopy_atomic
    d[types.BuiltinFunctionType] = _deepcopy_atomic
    d[types.FunctionType] = _deepcopy_atomic
    d[weakref.ref] = _deepcopy_atomic
    d[property] = _deepcopy_atomic

    def _deepcopy_list(x, memo, deepcopy=deepcopy):
        y = []
        memo[id(x)] = y
        append = y.append
        for a in x:
            append(deepcopy(a, memo))
        else:
            return y


    d[list] = _deepcopy_list

    def _deepcopy_tuple--- This code section failed: ---

 L. 210         0  LOAD_CLOSURE             'deepcopy'
                2  LOAD_CLOSURE             'memo'
                4  BUILD_TUPLE_2         2 
                6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 '_deepcopy_tuple.<locals>.<listcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_FAST                'x'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'y'

 L. 213        20  SETUP_FINALLY        36  'to 36'

 L. 214        22  LOAD_DEREF               'memo'
               24  LOAD_GLOBAL              id
               26  LOAD_FAST                'x'
               28  CALL_FUNCTION_1       1  ''
               30  BINARY_SUBSCR    
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    20  '20'

 L. 215        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    54  'to 54'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 216        50  POP_EXCEPT       
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            42  '42'
               54  END_FINALLY      
             56_0  COME_FROM            52  '52'

 L. 217        56  LOAD_GLOBAL              zip
               58  LOAD_FAST                'x'
               60  LOAD_FAST                'y'
               62  CALL_FUNCTION_2       2  ''
               64  GET_ITER         
             66_0  COME_FROM            94  '94'
             66_1  COME_FROM            80  '80'
               66  FOR_ITER             96  'to 96'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'k'
               72  STORE_FAST               'j'

 L. 218        74  LOAD_FAST                'k'
               76  LOAD_FAST                'j'
               78  COMPARE_OP               is-not
               80  POP_JUMP_IF_FALSE_BACK    66  'to 66'

 L. 219        82  LOAD_GLOBAL              tuple
               84  LOAD_FAST                'y'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'y'

 L. 220        90  POP_TOP          
               92  BREAK_LOOP          100  'to 100'
               94  JUMP_BACK            66  'to 66'
             96_0  COME_FROM            66  '66'

 L. 222        96  LOAD_FAST                'x'
               98  STORE_FAST               'y'
            100_0  COME_FROM            92  '92'

 L. 223       100  LOAD_FAST                'y'
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 54_0


    d[tuple] = _deepcopy_tuple

    def _deepcopy_dict(x, memo, deepcopy=deepcopy):
        y = {}
        memo[id(x)] = y
        for key, value in x.items():
            y[deepcopy(key, memo)] = deepcopy(value, memo)
        else:
            return y


    d[dict] = _deepcopy_dict
    if PyStringMap is not None:
        d[PyStringMap] = _deepcopy_dict

    def _deepcopy_method(x, memo):
        return type(x)(x.__func__, deepcopy(x.__self__, memo))


    d[types.MethodType] = _deepcopy_method
    del d

    def _keep_alive(x, memo):
        """Keeps a reference to the object x in the memo.

    Because we remember objects by their id, we have
    to assure that possibly temporary objects are kept
    alive by referencing them.
    We store a reference at the id of the memo, which should
    normally not be used unless someone tries to deepcopy
    the memo itself...
    """
        try:
            memo[id(memo)].append(x)
        except KeyError:
            memo[id(memo)] = [
             x]


    def _reconstruct(x, memo, func, args, state=None, listiter=None, dictiter=None, deepcopy=deepcopy):
        deep = memo is not None
        if deep:
            if args:
                args = (deepcopy(arg, memo) for arg in args)
        y = func(*args)
        if deep:
            memo[id(x)] = y
        if state is not None:
            if deep:
                state = deepcopy(state, memo)
            if hasattr(y, '__setstate__'):
                y.__setstate__(state)
            else:
                if isinstance(state, tuple) and len(state) == 2:
                    state, slotstate = state
                else:
                    slotstate = None
                if state is not None:
                    y.__dict__.update(state)
            if slotstate is not None:
                for key, value in slotstate.items():
                    setattr(y, key, value)
                else:
                    if listiter is not None:
                        if deep:
                            for item in listiter:
                                item = deepcopy(item, memo)
                                y.append(item)

                        else:
                            pass
                        for item in listiter:
                            y.append(item)
                        else:
                            if dictiter is not None:
                                if deep:
                                    for key, value in dictiter:
                                        key = deepcopy(key, memo)
                                        value = deepcopy(value, memo)
                                        y[key] = value

                                else:
                                    for key, value in dictiter:
                                        y[key] = value

            return y


    del types
    del weakref
    del PyStringMap