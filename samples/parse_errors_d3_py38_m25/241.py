# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: typing.py
"""
The typing module: Support for gradual typing as defined by PEP 484.

At large scale, the structure of the module is following:
* Imports and exports, all public names should be explicitly added to __all__.
* Internal helper functions: these should never be used in code outside this module.
* _SpecialForm and its instances (special forms): Any, NoReturn, ClassVar, Union, Optional
* Two classes whose instances can be type arguments in addition to types: ForwardRef and TypeVar
* The core of internal generics API: _GenericAlias and _VariadicGenericAlias, the latter is
  currently only used by Tuple and Callable. All subscripted types like X[int], Union[int, str],
  etc., are instances of either of these classes.
* The public counterpart of the generics API consists of two classes: Generic and Protocol.
* Public helper functions: get_type_hints, overload, cast, no_type_check,
  no_type_check_decorator.
* Generic aliases for collections.abc ABCs and few additional protocols.
* Special types: NewType, NamedTuple, TypedDict.
* Wrapper submodules for re and io related types.
"""
from abc import abstractmethod, ABCMeta
import collections, collections.abc, contextlib, functools, operator, re as stdlib_re, sys, types
from types import WrapperDescriptorType, MethodWrapperType, MethodDescriptorType
__all__ = [
 'Any',
 'Callable',
 'ClassVar',
 'Final',
 'ForwardRef',
 'Generic',
 'Literal',
 'Optional',
 'Protocol',
 'Tuple',
 'Type',
 'TypeVar',
 'Union',
 'AbstractSet',
 'ByteString',
 'Container',
 'ContextManager',
 'Hashable',
 'ItemsView',
 'Iterable',
 'Iterator',
 'KeysView',
 'Mapping',
 'MappingView',
 'MutableMapping',
 'MutableSequence',
 'MutableSet',
 'Sequence',
 'Sized',
 'ValuesView',
 'Awaitable',
 'AsyncIterator',
 'AsyncIterable',
 'Coroutine',
 'Collection',
 'AsyncGenerator',
 'AsyncContextManager',
 'Reversible',
 'SupportsAbs',
 'SupportsBytes',
 'SupportsComplex',
 'SupportsFloat',
 'SupportsIndex',
 'SupportsInt',
 'SupportsRound',
 'ChainMap',
 'Counter',
 'Deque',
 'Dict',
 'DefaultDict',
 'List',
 'OrderedDict',
 'Set',
 'FrozenSet',
 'NamedTuple',
 'TypedDict',
 'Generator',
 'AnyStr',
 'cast',
 'final',
 'get_args',
 'get_origin',
 'get_type_hints',
 'NewType',
 'no_type_check',
 'no_type_check_decorator',
 'NoReturn',
 'overload',
 'runtime_checkable',
 'Text',
 'TYPE_CHECKING']

def _type_check(arg, msg, is_argument=True):
    """Check that the argument is a type, and return it (internal helper).

    As a special case, accept None and return type(None) instead. Also wrap strings
    into ForwardRef instances. Consider several corner cases, for example plain
    special forms like Union are not valid, while Union[int, str] is OK, etc.
    The msg argument is a human-readable error message, e.g::

        "Union[arg, ...]: arg should be a type."

    We append the repr() of the actual value (truncated to 100 chars).
    """
    invalid_generic_forms = (
     Generic, Protocol)
    if is_argument:
        invalid_generic_forms = invalid_generic_forms + (ClassVar, Final)
    if arg is None:
        return type(None)
    if isinstance(arg, str):
        return ForwardRef(arg)
    if isinstance(arg, _GenericAlias):
        if arg.__origin__ in invalid_generic_forms:
            raise TypeError(f"{arg} is not valid as type argument")
    if isinstance(arg, _SpecialForm) and arg not in (Any, NoReturn) or arg in (Generic, Protocol):
        raise TypeError(f"Plain {arg} is not valid as type argument")
    if isinstance(arg, (type, TypeVar, ForwardRef)):
        return arg
    if not callable(arg):
        raise TypeError(f"{msg} Got {arg!r:.100}.")
    return arg


def _type_repr(obj):
    """Return the repr() of an object, special-casing types (internal helper).

    If obj is a type, we return a shorter version than the default
    type.__repr__, based on the module and qualified name, which is
    typically enough to uniquely identify a type.  For everything
    else, we fall back on repr(obj).
    """
    if isinstance(obj, type):
        if obj.__module__ == 'builtins':
            return obj.__qualname__
        return f"{obj.__module__}.{obj.__qualname__}"
    if obj is ...:
        return '...'
    if isinstance(obj, types.FunctionType):
        return obj.__name__
    return repr(obj)


def _collect_type_vars(types):
    """Collect all type variable contained in types in order of
    first appearance (lexicographic order). For example::

        _collect_type_vars((T, List[S, T])) == (T, S)
    """
    tvars = []
    for t in types:
        if isinstance(t, TypeVar):
            if t not in tvars:
                tvars.append(t)
        if isinstance(t, _GenericAlias):
            if not t._special:
                tvars.extend([t for t in t.__parameters__ if t not in tvars])
    else:
        return tuple(tvars)


def _subs_tvars(tp, tvars, subs):
    """Substitute type variables 'tvars' with substitutions 'subs'.
    These two must have the same length.
    """
    if not isinstance(tp, _GenericAlias):
        return tp
    new_args = list(tp.__args__)
    for a, arg in enumerate(tp.__args__):
        if isinstance(arg, TypeVar):
            for i, tvar in enumerate(tvars):
                if arg == tvar:
                    new_args[a] = subs[i]
            else:
                new_args[a] = _subs_tvars(arg, tvars, subs)

    else:
        if tp.__origin__ is Union:
            return Union[tuple(new_args)]
        return tp.copy_with(tuple(new_args))


def _check_generic(cls, parameters):
    """Check correct count for parameters of a generic cls (internal helper).
    This gives a nice error message in case of count mismatch.
    """
    if not cls.__parameters__:
        raise TypeError(f"{cls} is not a generic class")
    alen = len(parameters)
    elen = len(cls.__parameters__)
    if alen != elen:
        raise TypeError(f"Too {'many' if alen > elen else 'few'} parameters for {cls}; actual {alen}, expected {elen}")


def _remove_dups_flatten(parameters):
    """An internal helper for Union creation and substitution: flatten Unions
    among parameters, then remove duplicates.
    """
    params = []
    for p in parameters:
        if isinstance(p, _GenericAlias) and p.__origin__ is Union:
            params.extend(p.__args__)
        else:
            if isinstance(p, tuple):
                if len(p) > 0 and p[0] is Union:
                    params.extend(p[1:])
                else:
                    params.append(p)
    else:
        all_params = set(params)
        if len(all_params) < len(params):
            new_params = []
            for t in params:
                if t in all_params:
                    new_params.append(t)
                    all_params.remove(t)
            else:
                params = new_params
                if all_params:
                    raise AssertionError(all_params)

        return tuple(params)


_cleanups = []

def _tp_cache(func):
    """Internal wrapper caching __getitem__ of generic types with a fallback to
    original function for non-hashable arguments.
    """
    cached = functools.lru_cache()(func)
    _cleanups.append(cached.cache_clear)

    @functools.wraps(func)
    def inner--- This code section failed: ---

 L. 257         0  SETUP_FINALLY        14  'to 14'

 L. 258         2  LOAD_DEREF               'cached'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kwds'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 259        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 260        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 261        34  LOAD_DEREF               'func'
               36  LOAD_FAST                'args'
               38  LOAD_FAST                'kwds'
               40  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0

    return inner


def _eval_type(t, globalns, localns):
    """Evaluate all forward reverences in the given type t.
    For use of globalns and localns see the docstring for get_type_hints().
    """
    if isinstance(t, ForwardRef):
        return t._evaluate(globalns, localns)
    if isinstance(t, _GenericAlias):
        ev_args = tuple((_eval_type(a, globalns, localns) for a in t.__args__))
        if ev_args == t.__args__:
            return t
        res = t.copy_with(ev_args)
        res._special = t._special
        return res
    return t


class _Final:
    __doc__ = 'Mixin to prohibit subclassing'
    __slots__ = ('__weakref__', )

    def __init_subclass__(self, *args, **kwds):
        if '_root' not in kwds:
            raise TypeError('Cannot subclass special typing classes')


class _Immutable:
    __doc__ = 'Mixin to indicate that object should not be copied.'

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class _SpecialForm(_Final, _Immutable, _root=True):
    __doc__ = 'Internal indicator of special typing constructs.\n    See _doc instance attribute for specific docs.\n    '
    __slots__ = ('_name', '_doc')

    def __new__(cls, *args, **kwds):
        if len(args) == 3:
            if isinstance(args[0], str):
                if isinstance(args[1], tuple):
                    raise TypeError(f"Cannot subclass {cls!r}")
        return super().__new__(cls)

    def __init__(self, name, doc):
        self._name = name
        self._doc = doc

    def __eq__(self, other):
        if not isinstance(other, _SpecialForm):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash((self._name,))

    def __repr__(self):
        return 'typing.' + self._name

    def __reduce__(self):
        return self._name

    def __call__(self, *args, **kwds):
        raise TypeError(f"Cannot instantiate {self!r}")

    def __instancecheck__(self, obj):
        raise TypeError(f"{self} cannot be used with isinstance()")

    def __subclasscheck__(self, cls):
        raise TypeError(f"{self} cannot be used with issubclass()")

    @_tp_cache
    def __getitem__(self, parameters):
        if self._name in ('ClassVar', 'Final'):
            item = _type_check(parameters, f"{self._name} accepts only single type.")
            return _GenericAlias(self, (item,))
        if self._name == 'Union':
            if parameters == ():
                raise TypeError('Cannot take a Union of no types.')
            if not isinstance(parameters, tuple):
                parameters = (
                 parameters,)
            msg = 'Union[arg, ...]: each arg must be a type.'
            parameters = tuple((_type_check(p, msg) for p in parameters))
            parameters = _remove_dups_flatten(parameters)
            if len(parameters) == 1:
                return parameters[0]
            return _GenericAlias(self, parameters)
        if self._name == 'Optional':
            arg = _type_check(parameters, 'Optional[t] requires a single type.')
            return Union[(arg, type(None))]
        if self._name == 'Literal':
            return _GenericAlias(self, parameters)
        raise TypeError(f"{self} is not subscriptable")


Any = _SpecialForm('Any', doc='Special type indicating an unconstrained type.\n\n    - Any is compatible with every type.\n    - Any assumed to have all methods.\n    - All values assumed to be instances of Any.\n\n    Note that all the above statements are true from the point of view of\n    static type checkers. At runtime, Any should not be used with instance\n    or class checks.\n    ')
NoReturn = _SpecialForm('NoReturn', doc="Special type indicating functions that never return.\n    Example::\n\n      from typing import NoReturn\n\n      def stop() -> NoReturn:\n          raise Exception('no way')\n\n    This type is invalid in other positions, e.g., ``List[NoReturn]``\n    will fail in static type checkers.\n    ")
ClassVar = _SpecialForm('ClassVar', doc='Special type construct to mark class variables.\n\n    An annotation wrapped in ClassVar indicates that a given\n    attribute is intended to be used as a class variable and\n    should not be set on instances of that class. Usage::\n\n      class Starship:\n          stats: ClassVar[Dict[str, int]] = {} # class variable\n          damage: int = 10                     # instance variable\n\n    ClassVar accepts only types and cannot be further subscribed.\n\n    Note that ClassVar is not a class itself, and should not\n    be used with isinstance() or issubclass().\n    ')
Final = _SpecialForm('Final', doc='Special typing construct to indicate final names to type checkers.\n\n    A final name cannot be re-assigned or overridden in a subclass.\n    For example:\n\n      MAX_SIZE: Final = 9000\n      MAX_SIZE += 1  # Error reported by type checker\n\n      class Connection:\n          TIMEOUT: Final[int] = 10\n\n      class FastConnector(Connection):\n          TIMEOUT = 1  # Error reported by type checker\n\n    There is no runtime checking of these properties.\n    ')
Union = _SpecialForm('Union', doc='Union type; Union[X, Y] means either X or Y.\n\n    To define a union, use e.g. Union[int, str].  Details:\n    - The arguments must be types and there must be at least one.\n    - None as an argument is a special case and is replaced by\n      type(None).\n    - Unions of unions are flattened, e.g.::\n\n        Union[Union[int, str], float] == Union[int, str, float]\n\n    - Unions of a single argument vanish, e.g.::\n\n        Union[int] == int  # The constructor actually returns int\n\n    - Redundant arguments are skipped, e.g.::\n\n        Union[int, str, int] == Union[int, str]\n\n    - When comparing unions, the argument order is ignored, e.g.::\n\n        Union[int, str] == Union[str, int]\n\n    - You cannot subclass or instantiate a union.\n    - You can use Optional[X] as a shorthand for Union[X, None].\n    ')
Optional = _SpecialForm('Optional', doc='Optional type.\n\n    Optional[X] is equivalent to Union[X, None].\n    ')
Literal = _SpecialForm('Literal', doc="Special typing form to define literal types (a.k.a. value types).\n\n    This form can be used to indicate to type checkers that the corresponding\n    variable or function parameter has a value equivalent to the provided\n    literal (or one of several literals):\n\n      def validate_simple(data: Any) -> Literal[True]:  # always returns True\n          ...\n\n      MODE = Literal['r', 'rb', 'w', 'wb']\n      def open_helper(file: str, mode: MODE) -> str:\n          ...\n\n      open_helper('/some/path', 'r')  # Passes type check\n      open_helper('/other/path', 'typo')  # Error in type checker\n\n   Literal[...] cannot be subclassed. At runtime, an arbitrary value\n   is allowed as type argument to Literal[...], but type checkers may\n   impose restrictions.\n    ")

class ForwardRef(_Final, _root=True):
    __doc__ = 'Internal wrapper to hold a forward reference.'
    __slots__ = ('__forward_arg__', '__forward_code__', '__forward_evaluated__', '__forward_value__',
                 '__forward_is_argument__')

    def __init__(self, arg, is_argument=True):
        if not isinstance(arg, str):
            raise TypeError(f"Forward reference must be a string -- got {arg!r}")
        try:
            code = compile(arg, '<string>', 'eval')
        except SyntaxError:
            raise SyntaxError(f"Forward reference must be an expression -- got {arg!r}")
        else:
            self.__forward_arg__ = arg
            self.__forward_code__ = code
            self.__forward_evaluated__ = False
            self.__forward_value__ = None
            self.__forward_is_argument__ = is_argument

    def _evaluate(self, globalns, localns):
        if not self.__forward_evaluated__ or localns is not globalns:
            if globalns is None and localns is None:
                globalns = localns = {}
            elif globalns is None:
                globalns = localns
            elif localns is None:
                localns = globalns
            self.__forward_value__ = _type_check((eval(self.__forward_code__, globalns, localns)),
              'Forward references must evaluate to types.',
              is_argument=(self.__forward_is_argument__))
            self.__forward_evaluated__ = True
        return self.__forward_value__

    def __eq__(self, other):
        if not isinstance(other, ForwardRef):
            return NotImplemented
        if self.__forward_evaluated__:
            if other.__forward_evaluated__:
                return self.__forward_arg__ == other.__forward_arg__ and self.__forward_value__ == other.__forward_value__
        return self.__forward_arg__ == other.__forward_arg__

    def __hash__(self):
        return hash(self.__forward_arg__)

    def __repr__(self):
        return f"ForwardRef({self.__forward_arg__!r})"


class TypeVar(_Final, _Immutable, _root=True):
    __doc__ = "Type variable.\n\n    Usage::\n\n      T = TypeVar('T')  # Can be anything\n      A = TypeVar('A', str, bytes)  # Must be str or bytes\n\n    Type variables exist primarily for the benefit of static type\n    checkers.  They serve as the parameters for generic types as well\n    as for generic function definitions.  See class Generic for more\n    information on generic types.  Generic functions work as follows:\n\n      def repeat(x: T, n: int) -> List[T]:\n          '''Return a list containing n references to x.'''\n          return [x]*n\n\n      def longest(x: A, y: A) -> A:\n          '''Return the longest of two strings.'''\n          return x if len(x) >= len(y) else y\n\n    The latter example's signature is essentially the overloading\n    of (str, str) -> str and (bytes, bytes) -> bytes.  Also note\n    that if the arguments are instances of some subclass of str,\n    the return type is still plain str.\n\n    At runtime, isinstance(x, T) and issubclass(C, T) will raise TypeError.\n\n    Type variables defined with covariant=True or contravariant=True\n    can be used to declare covariant or contravariant generic types.\n    See PEP 484 for more details. By default generic types are invariant\n    in all type variables.\n\n    Type variables can be introspected. e.g.:\n\n      T.__name__ == 'T'\n      T.__constraints__ == ()\n      T.__covariant__ == False\n      T.__contravariant__ = False\n      A.__constraints__ == (str, bytes)\n\n    Note that only type variables defined in global scope can be pickled.\n    "
    __slots__ = ('__name__', '__bound__', '__constraints__', '__covariant__', '__contravariant__')

    def __init__(self, name, *constraints, bound=None, covariant=False, contravariant=False):
        self.__name__ = name
        if covariant:
            if contravariant:
                raise ValueError('Bivariant types are not supported.')
        self.__covariant__ = bool(covariant)
        self.__contravariant__ = bool(contravariant)
        if constraints:
            if bound is not None:
                raise TypeError('Constraints cannot be combined with bound=...')
        if constraints:
            if len(constraints) == 1:
                raise TypeError('A single constraint is not allowed')
        msg = 'TypeVar(name, constraint, ...): constraints must be types.'
        self.__constraints__ = tuple((_type_check(t, msg) for t in constraints))
        if bound:
            self.__bound__ = _type_check(bound, 'Bound must be a type.')
        else:
            self.__bound__ = None
        def_mod = sys._getframe(1).f_globals['__name__']
        if def_mod != 'typing':
            self.__module__ = def_mod

    def __repr__(self):
        if self.__covariant__:
            prefix = '+'
        elif self.__contravariant__:
            prefix = '-'
        else:
            prefix = '~'
        return prefix + self.__name__

    def __reduce__(self):
        return self.__name__


_normalize_alias = {'list':'List', 
 'tuple':'Tuple', 
 'dict':'Dict', 
 'set':'Set', 
 'frozenset':'FrozenSet', 
 'deque':'Deque', 
 'defaultdict':'DefaultDict', 
 'type':'Type', 
 'Set':'AbstractSet'}

def _is_dunder(attr):
    return attr.startswith('__') and attr.endswith('__')


class _GenericAlias(_Final, _root=True):
    __doc__ = "The central part of internal API.\n\n    This represents a generic version of type 'origin' with type arguments 'params'.\n    There are two kind of these aliases: user defined and special. The special ones\n    are wrappers around builtin collections and ABCs in collections.abc. These must\n    have 'name' always set. If 'inst' is False, then the alias can't be instantiated,\n    this is used by e.g. typing.List and typing.Dict.\n    "

    def __init__(self, origin, params, *, inst=True, special=False, name=None):
        self._inst = inst
        self._special = special
        if special:
            if name is None:
                orig_name = origin.__name__
                name = _normalize_alias.get(orig_name, orig_name)
        self._name = name
        if not isinstance(params, tuple):
            params = (
             params,)
        self.__origin__ = origin
        self.__args__ = tuple(((... if a is _TypingEllipsis else () if a is _TypingEmpty else a) for a in params))
        self.__parameters__ = _collect_type_vars(params)
        self.__slots__ = None
        if not name:
            self.__module__ = origin.__module__

    @_tp_cache
    def __getitem__(self, params):
        if self.__origin__ in (Generic, Protocol):
            raise TypeError(f"Cannot subscript already-subscripted {self}")
        if not isinstance(params, tuple):
            params = (
             params,)
        msg = 'Parameters to generic types must be types.'
        params = tuple((_type_check(p, msg) for p in params))
        _check_generic(self, params)
        return _subs_tvars(self, self.__parameters__, params)

    def copy_with(self, params):
        return _GenericAlias((self.__origin__), params, name=(self._name), inst=(self._inst))

    def __repr__(self):
        if not self._name != 'Callable':
            if not len(self.__args__) == 2 or self.__args__[0] is Ellipsis:
                if self._name:
                    name = 'typing.' + self._name
                else:
                    name = _type_repr(self.__origin__)
                if not self._special:
                    args = f"[{', '.join([_type_repr(a) for a in self.__args__])}]"
                else:
                    args = ''
                return f"{name}{args}"
            if self._special:
                return 'typing.Callable'
            return f"typing.Callable[[{', '.join([_type_repr(a) for a in self.__args__[:-1]])}], {_type_repr(self.__args__[(-1)])}]"

    def __eq__(self, other):
        if not isinstance(other, _GenericAlias):
            return NotImplemented
        if self.__origin__ != other.__origin__:
            return False
        if self.__origin__ is Union:
            if other.__origin__ is Union:
                return frozenset(self.__args__) == frozenset(other.__args__)
        return self.__args__ == other.__args__

    def __hash__(self):
        if self.__origin__ is Union:
            return hash((Union, frozenset(self.__args__)))
        return hash((self.__origin__, self.__args__))

    def __call__(self, *args, **kwargs):
        if not self._inst:
            raise TypeError(f"Type {self._name} cannot be instantiated; use {self._name.lower()}() instead")
        result = (self.__origin__)(*args, **kwargs)
        try:
            result.__orig_class__ = self
        except AttributeError:
            pass
        else:
            return result

    def __mro_entries__(self, bases):
        if self._name:
            res = []
            if self.__origin__ not in bases:
                res.append(self.__origin__)
            i = bases.index(self)
            if not any((isinstance(b, _GenericAlias) or issubclass(b, Generic) for b in bases[i + 1:])):
                res.append(Generic)
            return tuple(res)
        if self.__origin__ is Generic:
            if Protocol in bases:
                return ()
            i = bases.index(self)
            for b in bases[i + 1:]:
                if isinstance(b, _GenericAlias):
                    if b is not self:
                        return ()

            return (
             self.__origin__,)

    def __getattr__(self, attr):
        if '__origin__' in self.__dict__:
            if not _is_dunder(attr):
                return getattr(self.__origin__, attr)
        raise AttributeError(attr)

    def __setattr__(self, attr, val):
        if _is_dunder(attr) or attr in ('_name', '_inst', '_special'):
            super().__setattr__(attr, val)
        else:
            setattr(self.__origin__, attr, val)

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(self, cls):
        if self._special:
            if not isinstance(cls, _GenericAlias):
                return issubclass(cls, self.__origin__)
            if cls._special:
                return issubclass(cls.__origin__, self.__origin__)
        raise TypeError('Subscripted generics cannot be used with class and instance checks')

    def __reduce__(self):
        if self._special:
            return self._name
        if self._name:
            origin = globals()[self._name]
        else:
            origin = self.__origin__
        if not (origin is Callable and len(self.__args__) == 2 and self.__args__[0] is Ellipsis):
            args = (list(self.__args__[:-1]), self.__args__[(-1)])
        else:
            args = tuple(self.__args__)
        if len(args) == 1:
            if not isinstance(args[0], tuple):
                args, = args
            return (operator.getitem, (origin, args))


class _VariadicGenericAlias(_GenericAlias, _root=True):
    __doc__ = 'Same as _GenericAlias above but for variadic aliases. Currently,\n    this is used only by special internal aliases: Tuple and Callable.\n    '

    def __getitem__(self, params):
        if not (self._name != 'Callable' or self._special):
            return self.__getitem_inner__(params)
        if not isinstance(params, tuple) or len(params) != 2:
            raise TypeError('Callable must be used as Callable[[arg, ...], result].')
        args, result = params
        if args is Ellipsis:
            params = (
             Ellipsis, result)
        else:
            if not isinstance(args, list):
                raise TypeError(f"Callable[args, result]: args must be a list. Got {args}")
            params = (tuple(args), result)
        return self.__getitem_inner__(params)

    @_tp_cache
    def __getitem_inner__(self, params):
        if self.__origin__ is tuple:
            if self._special:
                if params == ():
                    return self.copy_with((_TypingEmpty,))
                if not isinstance(params, tuple):
                    params = (
                     params,)
                if len(params) == 2:
                    if params[1] is ...:
                        msg = 'Tuple[t, ...]: t must be a type.'
                        p = _type_check(params[0], msg)
                        return self.copy_with((p, _TypingEllipsis))
                msg = 'Tuple[t0, t1, ...]: each t must be a type.'
                params = tuple((_type_check(p, msg) for p in params))
                return self.copy_with(params)
        if self.__origin__ is collections.abc.Callable:
            if self._special:
                args, result = params
                msg = 'Callable[args, result]: result must be a type.'
                result = _type_check(result, msg)
                if args is Ellipsis:
                    return self.copy_with((_TypingEllipsis, result))
                msg = 'Callable[[arg, ...], result]: each arg must be a type.'
                args = tuple((_type_check(arg, msg) for arg in args))
                params = args + (result,)
                return self.copy_with(params)
        return super().__getitem__(params)


class Generic:
    __doc__ = 'Abstract base class for generic types.\n\n    A generic type is typically declared by inheriting from\n    this class parameterized with one or more type variables.\n    For example, a generic mapping type might be defined as::\n\n      class Mapping(Generic[KT, VT]):\n          def __getitem__(self, key: KT) -> VT:\n              ...\n          # Etc.\n\n    This class can then be used as follows::\n\n      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:\n          try:\n              return mapping[key]\n          except KeyError:\n              return default\n    '
    __slots__ = ()
    _is_protocol = False

    def __new__(cls, *args, **kwds):
        if cls in (Generic, Protocol):
            raise TypeError(f"Type {cls.__name__} cannot be instantiated; it can be used only as a base class")
        if super().__new__ is object.__new__ and cls.__init__ is not object.__init__:
            obj = super().__new__(cls)
        else:
            obj = (super().__new__)(cls, *args, **kwds)
        return obj

    @_tp_cache
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (
             params,)
        if not params:
            if cls is not Tuple:
                raise TypeError(f"Parameter list to {cls.__qualname__}[...] cannot be empty")
        msg = 'Parameters to generic types must be types.'
        params = tuple((_type_check(p, msg) for p in params))
        if cls in (Generic, Protocol):
            if not all((isinstance(p, TypeVar) for p in params)):
                raise TypeError(f"Parameters to {cls.__name__}[...] must all be type variables")
            if len(set(params)) != len(params):
                raise TypeError(f"Parameters to {cls.__name__}[...] must all be unique")
        else:
            _check_generic(cls, params)
        return _GenericAlias(cls, params)

    def __init_subclass__(cls, *args, **kwargs):
        (super().__init_subclass__)(*args, **kwargs)
        tvars = []
        if '__orig_bases__' in cls.__dict__:
            error = Generic in cls.__orig_bases__
        else:
            error = Generic in cls.__bases__ and cls.__name__ != 'Protocol'
        if error:
            raise TypeError('Cannot inherit from plain Generic')
        if '__orig_bases__' in cls.__dict__:
            tvars = _collect_type_vars(cls.__orig_bases__)
            gvars = None
            for base in cls.__orig_bases__:
                if isinstance(base, _GenericAlias):
                    if base.__origin__ is Generic:
                        if gvars is not None:
                            raise TypeError('Cannot inherit from Generic[...] multiple types.')
                        else:
                            gvars = base.__parameters__
            else:
                if gvars is not None:
                    tvarset = set(tvars)
                    gvarset = set(gvars)
                    if not tvarset <= gvarset:
                        s_vars = ', '.join((str(t) for t in tvars if t not in gvarset))
                        s_args = ', '.join((str(g) for g in gvars))
                        raise TypeError(f"Some type variables ({s_vars}) are not listed in Generic[{s_args}]")
                    tvars = gvars

        cls.__parameters__ = tuple(tvars)


class _TypingEmpty:
    __doc__ = 'Internal placeholder for () or []. Used by TupleMeta and CallableMeta\n    to allow empty list/tuple in specific places, without allowing them\n    to sneak in where prohibited.\n    '


class _TypingEllipsis:
    __doc__ = 'Internal placeholder for ... (ellipsis).'


_TYPING_INTERNALS = [
 '__parameters__', '__orig_bases__', '__orig_class__',
 '_is_protocol', '_is_runtime_protocol']
_SPECIAL_NAMES = [
 '__abstractmethods__', '__annotations__', '__dict__', '__doc__',
 '__init__', '__module__', '__new__', '__slots__',
 '__subclasshook__', '__weakref__']
EXCLUDED_ATTRIBUTES = _TYPING_INTERNALS + _SPECIAL_NAMES + ['_MutableMapping__marker']

def _get_protocol_attrs(cls):
    """Collect protocol members from a protocol class objects.

    This includes names actually defined in the class dictionary, as well
    as names that appear in annotations. Special names (above) are skipped.
    """
    attrs = set()
    for base in cls.__mro__[:-1]:
        if base.__name__ in ('Protocol', 'Generic'):
            pass
        else:
            annotations = getattr(base, '__annotations__', {})
            for attr in list(base.__dict__.keys()) + list(annotations.keys()):
                if not attr.startswith('_abc_'):
                    if attr not in EXCLUDED_ATTRIBUTES:
                        attrs.add(attr)

            return attrs


def _is_callable_members_only(cls):
    return all((callable(getattr(cls, attr, None)) for attr in _get_protocol_attrs(cls)))


def _no_init(self, *args, **kwargs):
    if type(self)._is_protocol:
        raise TypeError('Protocols cannot be instantiated')


def _allow_reckless_class_cheks--- This code section failed: ---

 L. 988         0  SETUP_FINALLY        24  'to 24'

 L. 989         2  LOAD_GLOBAL              sys
                4  LOAD_METHOD              _getframe
                6  LOAD_CONST               3
                8  CALL_METHOD_1         1  ''
               10  LOAD_ATTR                f_globals
               12  LOAD_STR                 '__name__'
               14  BINARY_SUBSCR    
               16  LOAD_CONST               ('abc', 'functools')
               18  COMPARE_OP               in
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 990        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  LOAD_GLOBAL              ValueError
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 991        42  POP_EXCEPT       
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'
               48  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 44


_PROTO_WHITELIST = {'collections.abc':[
  'Callable', 'Awaitable', 'Iterable', 'Iterator', 'AsyncIterable',
  'Hashable', 'Sized', 'Container', 'Collection', 'Reversible'], 
 'contextlib':[
  'AbstractContextManager', 'AbstractAsyncContextManager']}

class _ProtocolMeta(ABCMeta):

    def __instancecheck__(cls, instance):
        if not getattr(cls, '_is_protocol', False) or _is_callable_members_only(cls):
            if issubclass(instance.__class__, cls):
                return True
        if cls._is_protocol:
            if all((hasattr(instance, attr) and (not callable(getattr(cls, attr, None)) or getattr(instance, attr) is not None) for attr in _get_protocol_attrs(cls))):
                return True
        return super().__instancecheck__(instance)


class Protocol(Generic, metaclass=_ProtocolMeta):
    __doc__ = 'Base class for protocol classes.\n\n    Protocol classes are defined as::\n\n        class Proto(Protocol):\n            def meth(self) -> int:\n                ...\n\n    Such classes are primarily used with static type checkers that recognize\n    structural subtyping (static duck-typing), for example::\n\n        class C:\n            def meth(self) -> int:\n                return 0\n\n        def func(x: Proto) -> int:\n            return x.meth()\n\n        func(C())  # Passes static type check\n\n    See PEP 544 for details. Protocol classes decorated with\n    @typing.runtime_checkable act as simple-minded runtime protocols that check\n    only the presence of given attributes, ignoring their type signatures.\n    Protocol classes can be generic, they are defined as::\n\n        class GenProto(Protocol[T]):\n            def meth(self) -> T:\n                ...\n    '
    __slots__ = ()
    _is_protocol = True
    _is_runtime_protocol = False

    def __init_subclass__(cls, *args, **kwargs):
        (super().__init_subclass__)(*args, **kwargs)
        if not cls.__dict__.get('_is_protocol', False):
            cls._is_protocol = any((b is Protocol for b in cls.__bases__))

        def _proto_hook--- This code section failed: ---

 L.1066         0  LOAD_DEREF               'cls'
                2  LOAD_ATTR                __dict__
                4  LOAD_METHOD              get
                6  LOAD_STR                 '_is_protocol'
                8  LOAD_CONST               False
               10  CALL_METHOD_2         2  ''
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L.1067        14  LOAD_GLOBAL              NotImplemented
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L.1070        18  LOAD_GLOBAL              getattr
               20  LOAD_DEREF               'cls'
               22  LOAD_STR                 '_is_runtime_protocol'
               24  LOAD_CONST               False
               26  CALL_FUNCTION_3       3  ''
               28  POP_JUMP_IF_TRUE     48  'to 48'

 L.1071        30  LOAD_GLOBAL              _allow_reckless_class_cheks
               32  CALL_FUNCTION_0       0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.1072        36  LOAD_GLOBAL              NotImplemented
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.1073        40  LOAD_GLOBAL              TypeError
               42  LOAD_STR                 'Instance and class checks can only be used with @runtime_checkable protocols'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            28  '28'

 L.1075        48  LOAD_GLOBAL              _is_callable_members_only
               50  LOAD_DEREF               'cls'
               52  CALL_FUNCTION_1       1  ''
               54  POP_JUMP_IF_TRUE     74  'to 74'

 L.1076        56  LOAD_GLOBAL              _allow_reckless_class_cheks
               58  CALL_FUNCTION_0       0  ''
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L.1077        62  LOAD_GLOBAL              NotImplemented
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L.1078        66  LOAD_GLOBAL              TypeError
               68  LOAD_STR                 "Protocols with non-method members don't support issubclass()"
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            54  '54'

 L.1080        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'other'
               78  LOAD_GLOBAL              type
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_TRUE     92  'to 92'

 L.1082        84  LOAD_GLOBAL              TypeError
               86  LOAD_STR                 'issubclass() arg 1 must be a class'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L.1085        92  LOAD_GLOBAL              _get_protocol_attrs
               94  LOAD_DEREF               'cls'
               96  CALL_FUNCTION_1       1  ''
               98  GET_ITER         
            100_0  COME_FROM           218  '218'
            100_1  COME_FROM           206  '206'
            100_2  COME_FROM           152  '152'
              100  FOR_ITER            220  'to 220'
              102  STORE_FAST               'attr'

 L.1086       104  LOAD_FAST                'other'
              106  LOAD_ATTR                __mro__
              108  GET_ITER         
            110_0  COME_FROM           208  '208'
            110_1  COME_FROM           202  '202'
            110_2  COME_FROM           196  '196'
            110_3  COME_FROM           186  '186'
            110_4  COME_FROM           178  '178'
              110  FOR_ITER            210  'to 210'
              112  STORE_FAST               'base'

 L.1088       114  LOAD_FAST                'attr'
              116  LOAD_FAST                'base'
              118  LOAD_ATTR                __dict__
              120  COMPARE_OP               in
              122  POP_JUMP_IF_FALSE   154  'to 154'

 L.1089       124  LOAD_FAST                'base'
              126  LOAD_ATTR                __dict__
              128  LOAD_FAST                'attr'
              130  BINARY_SUBSCR    
              132  LOAD_CONST               None
              134  COMPARE_OP               is
              136  POP_JUMP_IF_FALSE   150  'to 150'

 L.1090       138  LOAD_GLOBAL              NotImplemented
              140  ROT_TWO          
              142  POP_TOP          
              144  ROT_TWO          
              146  POP_TOP          
              148  RETURN_VALUE     
            150_0  COME_FROM           136  '136'

 L.1091       150  POP_TOP          
              152  JUMP_BACK           100  'to 100'
            154_0  COME_FROM           122  '122'

 L.1094       154  LOAD_GLOBAL              getattr
              156  LOAD_FAST                'base'
              158  LOAD_STR                 '__annotations__'
              160  BUILD_MAP_0           0 
              162  CALL_FUNCTION_3       3  ''
              164  STORE_FAST               'annotations'

 L.1095       166  LOAD_GLOBAL              isinstance
              168  LOAD_FAST                'annotations'
              170  LOAD_GLOBAL              collections
              172  LOAD_ATTR                abc
              174  LOAD_ATTR                Mapping
              176  CALL_FUNCTION_2       2  ''
              178  POP_JUMP_IF_FALSE_BACK   110  'to 110'

 L.1096       180  LOAD_FAST                'attr'
              182  LOAD_FAST                'annotations'
              184  COMPARE_OP               in

 L.1095       186  POP_JUMP_IF_FALSE_BACK   110  'to 110'

 L.1097       188  LOAD_GLOBAL              issubclass
              190  LOAD_FAST                'other'
              192  LOAD_GLOBAL              Generic
              194  CALL_FUNCTION_2       2  ''

 L.1095       196  POP_JUMP_IF_FALSE_BACK   110  'to 110'

 L.1097       198  LOAD_FAST                'other'
              200  LOAD_ATTR                _is_protocol

 L.1095       202  POP_JUMP_IF_FALSE_BACK   110  'to 110'

 L.1098       204  POP_TOP          
              206  BREAK_LOOP          100  'to 100'
              208  JUMP_BACK           110  'to 110'
            210_0  COME_FROM           110  '110'

 L.1100       210  LOAD_GLOBAL              NotImplemented
              212  ROT_TWO          
              214  POP_TOP          
              216  RETURN_VALUE     
              218  JUMP_BACK           100  'to 100'
            220_0  COME_FROM           100  '100'

 L.1101       220  LOAD_CONST               True
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 152

        if '__subclasshook__' not in cls.__dict__:
            cls.__subclasshook__ = _proto_hook
        if not cls._is_protocol:
            return
        for base in cls.__bases__:
            if not base in (object, Generic):
                if not (base.__module__ in _PROTO_WHITELIST and base.__name__ in _PROTO_WHITELIST[base.__module__]):
                    if not (issubclass(base, Generic) and base._is_protocol):
                        raise TypeError('Protocols can only inherit from other protocols, got %r' % base)
        else:
            cls.__init__ = _no_init


def runtime_checkable(cls):
    """Mark a protocol class as a runtime protocol.

    Such protocol can be used with isinstance() and issubclass().
    Raise TypeError if applied to a non-protocol class.
    This allows a simple-minded structural check very similar to
    one trick ponies in collections.abc such as Iterable.
    For example::

        @runtime_checkable
        class Closable(Protocol):
            def close(self): ...

        assert isinstance(open('/some/file'), Closable)

    Warning: this will check only the presence of the required methods,
    not their type signatures!
    """
    if not (issubclass(cls, Generic) and cls._is_protocol):
        raise TypeError('@runtime_checkable can be only applied to protocol classes, got %r' % cls)
    cls._is_runtime_protocol = True
    return cls


def cast(typ, val):
    """Cast a value to a type.

    This returns the value unchanged.  To the type checker this
    signals that the return value has the designated type, but at
    runtime we intentionally don't check anything (we want this
    to be as fast as possible).
    """
    return val


def _get_defaults(func):
    """Internal helper to extract the default arguments, by name."""
    try:
        code = func.__code__
    except AttributeError:
        return {}
    else:
        pos_count = code.co_argcount
        arg_names = code.co_varnames
        arg_names = arg_names[:pos_count]
        defaults = func.__defaults__ or ()
        kwdefaults = func.__kwdefaults__
        res = dict(kwdefaults) if kwdefaults else {}
        pos_offset = pos_count - len(defaults)
        for name, value in zip(arg_names[pos_offset:], defaults):
            if not name not in res:
                raise AssertionError
            else:
                res[name] = value
        else:
            return res


_allowed_types = (types.FunctionType, types.BuiltinFunctionType,
 types.MethodType, types.ModuleType,
 WrapperDescriptorType, MethodWrapperType, MethodDescriptorType)

def get_type_hints(obj, globalns=None, localns=None):
    """Return type hints for an object.

    This is often the same as obj.__annotations__, but it handles
    forward references encoded as string literals, and if necessary
    adds Optional[t] if a default value equal to None is set.

    The argument may be a module, class, method, or function. The annotations
    are returned as a dictionary. For classes, annotations include also
    inherited members.

    TypeError is raised if the argument is not of a type that can contain
    annotations, and an empty dictionary is returned if no annotations are
    present.

    BEWARE -- the behavior of globalns and localns is counterintuitive
    (unless you are familiar with how eval() and exec() work).  The
    search order is locals first, then globals.

    - If no dict arguments are passed, an attempt is made to use the
      globals from obj (or the respective module's globals for classes),
      and these are also used as the locals.  If the object does not appear
      to have globals, an empty dictionary is used.

    - If one dict argument is passed, it is used for both globals and
      locals.

    - If two dict arguments are passed, they specify globals and
      locals, respectively.
    """
    if getattr(obj, '__no_type_check__', None):
        return {}
    if isinstance(obj, type):
        hints = {}
        for base in reversed(obj.__mro__):
            if globalns is None:
                base_globals = sys.modules[base.__module__].__dict__
            else:
                base_globals = globalns
            ann = base.__dict__.get('__annotations__', {})
            for name, value in ann.items():
                if value is None:
                    value = type(None)
                else:
                    if isinstance(value, str):
                        value = ForwardRef(value, is_argument=False)
                    value = _eval_type(value, base_globals, localns)
                    hints[name] = value

        else:
            return hints

    if globalns is None:
        if isinstance(obj, types.ModuleType):
            globalns = obj.__dict__
        else:
            nsobj = obj
            while True:
                if hasattr(nsobj, '__wrapped__'):
                    nsobj = nsobj.__wrapped__

            globalns = getattr(nsobj, '__globals__', {})
        if localns is None:
            localns = globalns
    elif localns is None:
        localns = globalns
    hints = getattr(obj, '__annotations__', None)
    if hints is None:
        if isinstance(obj, _allowed_types):
            return {}
        raise TypeError('{!r} is not a module, class, method, or function.'.format(obj))
    defaults = _get_defaults(obj)
    hints = dict(hints)
    for name, value in hints.items():
        if value is None:
            value = type(None)
        else:
            if isinstance(value, str):
                value = ForwardRef(value)
            value = _eval_type(value, globalns, localns)
            if name in defaults:
                if defaults[name] is None:
                    value = Optional[value]
            hints[name] = value
    else:
        return hints


def get_origin(tp):
    """Get the unsubscripted version of a type.

    This supports generic types, Callable, Tuple, Union, Literal, Final and ClassVar.
    Return None for unsupported types. Examples::

        get_origin(Literal[42]) is Literal
        get_origin(int) is None
        get_origin(ClassVar[int]) is ClassVar
        get_origin(Generic) is Generic
        get_origin(Generic[T]) is Generic
        get_origin(Union[T, int]) is Union
        get_origin(List[Tuple[T, T]][int]) == list
    """
    if isinstance(tp, _GenericAlias):
        return tp.__origin__
    if tp is Generic:
        return Generic


def get_args(tp):
    """Get type arguments with all substitutions performed.

    For unions, basic simplifications used by Union constructor are performed.
    Examples::
        get_args(Dict[str, int]) == (str, int)
        get_args(int) == ()
        get_args(Union[int, Union[T, int], str][int]) == (int, str)
        get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])
        get_args(Callable[[], T][int]) == ([], int)
    """
    if isinstance(tp, _GenericAlias):
        res = tp.__args__
        if get_origin(tp) is collections.abc.Callable:
            if res[0] is not Ellipsis:
                res = (
                 list(res[:-1]), res[(-1)])
        return res
    return ()


def no_type_check(arg):
    """Decorator to indicate that annotations are not type hints.

    The argument must be a class or function; if it is a class, it
    applies recursively to all methods and classes defined in that class
    (but not to methods defined in its superclasses or subclasses).

    This mutates the function(s) or class(es) in place.
    """
    if isinstance(arg, type):
        arg_attrs = arg.__dict__.copy()
        for attr, val in arg.__dict__.items():
            if val in arg.__bases__ + (arg,):
                arg_attrs.pop(attr)
            for obj in arg_attrs.values():
                if isinstance(obj, types.FunctionType):
                    obj.__no_type_check__ = True
                if isinstance(obj, type):
                    no_type_check(obj)

        else:
            try:
                arg.__no_type_check__ = True
            except TypeError:
                pass

        return arg


def no_type_check_decorator(decorator):
    """Decorator to give another decorator the @no_type_check effect.

    This wraps the decorator with something that wraps the decorated
    function in @no_type_check.
    """

    @functools.wraps(decorator)
    def wrapped_decorator(*args, **kwds):
        func = decorator(*args, **kwds)
        func = no_type_check(func)
        return func

    return wrapped_decorator


def _overload_dummy(*args, **kwds):
    """Helper for @overload to raise when called."""
    raise NotImplementedError('You should not call an overloaded function. A series of @overload-decorated functions outside a stub module should always be followed by an implementation that is not @overload-ed.')


def overload(func):
    """Decorator for overloaded functions/methods.

    In a stub file, place two or more stub definitions for the same
    function in a row, each decorated with @overload.  For example:

      @overload
      def utf8(value: None) -> None: ...
      @overload
      def utf8(value: bytes) -> bytes: ...
      @overload
      def utf8(value: str) -> bytes: ...

    In a non-stub file (i.e. a regular .py file), do the same but
    follow it with an implementation.  The implementation should *not*
    be decorated with @overload.  For example:

      @overload
      def utf8(value: None) -> None: ...
      @overload
      def utf8(value: bytes) -> bytes: ...
      @overload
      def utf8(value: str) -> bytes: ...
      def utf8(value):
          # implementation goes here
    """
    return _overload_dummy


def final(f):
    """A decorator to indicate final methods and final classes.

    Use this decorator to indicate to type checkers that the decorated
    method cannot be overridden, and decorated class cannot be subclassed.
    For example:

      class Base:
          @final
          def done(self) -> None:
              ...
      class Sub(Base):
          def done(self) -> None:  # Error reported by type checker
                ...

      @final
      class Leaf:
          ...
      class Other(Leaf):  # Error reported by type checker
          ...

    There is no runtime checking of these properties.
    """
    return f


T = TypeVar('T')
KT = TypeVar('KT')
VT = TypeVar('VT')
T_co = TypeVar('T_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
VT_co = TypeVar('VT_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)
CT_co = TypeVar('CT_co', covariant=True, bound=type)
AnyStr = TypeVar('AnyStr', bytes, str)

def _alias(origin, params, inst=True):
    return _GenericAlias(origin, params, special=True, inst=inst)


Hashable = _alias(collections.abc.Hashable, ())
Awaitable = _alias(collections.abc.Awaitable, T_co)
Coroutine = _alias(collections.abc.Coroutine, (T_co, T_contra, V_co))
AsyncIterable = _alias(collections.abc.AsyncIterable, T_co)
AsyncIterator = _alias(collections.abc.AsyncIterator, T_co)
Iterable = _alias(collections.abc.Iterable, T_co)
Iterator = _alias(collections.abc.Iterator, T_co)
Reversible = _alias(collections.abc.Reversible, T_co)
Sized = _alias(collections.abc.Sized, ())
Container = _alias(collections.abc.Container, T_co)
Collection = _alias(collections.abc.Collection, T_co)
Callable = _VariadicGenericAlias((collections.abc.Callable), (), special=True)
Callable.__doc__ = 'Callable type; Callable[[int], str] is a function of (int) -> str.\n\n    The subscription syntax must always be used with exactly two\n    values: the argument list and the return type.  The argument list\n    must be a list of types or ellipsis; the return type must be a single type.\n\n    There is no syntax to indicate optional or keyword arguments,\n    such function types are rarely used as callback types.\n    '
AbstractSet = _alias(collections.abc.Set, T_co)
MutableSet = _alias(collections.abc.MutableSet, T)
Mapping = _alias(collections.abc.Mapping, (KT, VT_co))
MutableMapping = _alias(collections.abc.MutableMapping, (KT, VT))
Sequence = _alias(collections.abc.Sequence, T_co)
MutableSequence = _alias(collections.abc.MutableSequence, T)
ByteString = _alias(collections.abc.ByteString, ())
Tuple = _VariadicGenericAlias(tuple, (), inst=False, special=True)
Tuple.__doc__ = 'Tuple type; Tuple[X, Y] is the cross-product type of X and Y.\n\n    Example: Tuple[T1, T2] is a tuple of two elements corresponding\n    to type variables T1 and T2.  Tuple[int, float, str] is a tuple\n    of an int, a float and a string.\n\n    To specify a variable-length tuple of homogeneous type, use Tuple[T, ...].\n    '
List = _alias(list, T, inst=False)
Deque = _alias(collections.deque, T)
Set = _alias(set, T, inst=False)
FrozenSet = _alias(frozenset, T_co, inst=False)
MappingView = _alias(collections.abc.MappingView, T_co)
KeysView = _alias(collections.abc.KeysView, KT)
ItemsView = _alias(collections.abc.ItemsView, (KT, VT_co))
ValuesView = _alias(collections.abc.ValuesView, VT_co)
ContextManager = _alias(contextlib.AbstractContextManager, T_co)
AsyncContextManager = _alias(contextlib.AbstractAsyncContextManager, T_co)
Dict = _alias(dict, (KT, VT), inst=False)
DefaultDict = _alias(collections.defaultdict, (KT, VT))
OrderedDict = _alias(collections.OrderedDict, (KT, VT))
Counter = _alias(collections.Counter, T)
ChainMap = _alias(collections.ChainMap, (KT, VT))
Generator = _alias(collections.abc.Generator, (T_co, T_contra, V_co))
AsyncGenerator = _alias(collections.abc.AsyncGenerator, (T_co, T_contra))
Type = _alias(type, CT_co, inst=False)
Type.__doc__ = "A special construct usable to annotate class objects.\n\n    For example, suppose we have the following classes::\n\n      class User: ...  # Abstract base for User classes\n      class BasicUser(User): ...\n      class ProUser(User): ...\n      class TeamUser(User): ...\n\n    And a function that takes a class argument that's a subclass of\n    User and returns an instance of the corresponding class::\n\n      U = TypeVar('U', bound=User)\n      def new_user(user_class: Type[U]) -> U:\n          user = user_class()\n          # (Here we could write the user object to a database)\n          return user\n\n      joe = new_user(BasicUser)\n\n    At this point the type checker knows that joe has type BasicUser.\n    "

@runtime_checkable
class SupportsInt(Protocol):
    __doc__ = 'An ABC with one abstract method __int__.'
    __slots__ = ()

    @abstractmethod
    def __int__(self) -> int:
        pass


@runtime_checkable
class SupportsFloat(Protocol):
    __doc__ = 'An ABC with one abstract method __float__.'
    __slots__ = ()

    @abstractmethod
    def __float__(self) -> float:
        pass


@runtime_checkable
class SupportsComplex(Protocol):
    __doc__ = 'An ABC with one abstract method __complex__.'
    __slots__ = ()

    @abstractmethod
    def __complex__(self) -> complex:
        pass


@runtime_checkable
class SupportsBytes(Protocol):
    __doc__ = 'An ABC with one abstract method __bytes__.'
    __slots__ = ()

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass


@runtime_checkable
class SupportsIndex(Protocol):
    __doc__ = 'An ABC with one abstract method __index__.'
    __slots__ = ()

    @abstractmethod
    def __index__(self) -> int:
        pass


@runtime_checkable
class SupportsAbs(Protocol[T_co]):
    __doc__ = 'An ABC with one abstract method __abs__ that is covariant in its return type.'
    __slots__ = ()

    @abstractmethod
    def __abs__(self) -> T_co:
        pass


@runtime_checkable
class SupportsRound(Protocol[T_co]):
    __doc__ = 'An ABC with one abstract method __round__ that is covariant in its return type.'
    __slots__ = ()

    @abstractmethod
    def __round__(self, ndigits: int=0) -> T_co:
        pass


def _make_nmtuple(name, types):
    msg = "NamedTuple('Name', [(f0, t0), (f1, t1), ...]); each t must be a type"
    types = [(n, _type_check(t, msg)) for n, t in types]
    nm_tpl = collections.namedtuple(name, [n for n, t in types])
    nm_tpl.__annotations__ = nm_tpl._field_types = dict(types)
    try:
        nm_tpl.__module__ = sys._getframe(2).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    else:
        return nm_tpl


_prohibited = ('__new__', '__init__', '__slots__', '__getnewargs__', '_fields', '_field_defaults',
               '_field_types', '_make', '_replace', '_asdict', '_source')
_special = ('__module__', '__name__', '__annotations__')

class NamedTupleMeta(type):

    def __new__(cls, typename, bases, ns):
        if ns.get('_root', False):
            return super().__new__(cls, typename, bases, ns)
        types = ns.get('__annotations__', {})
        nm_tpl = _make_nmtuple(typename, types.items())
        defaults = []
        defaults_dict = {}
        for field_name in types:
            if field_name in ns:
                default_value = ns[field_name]
                defaults.append(default_value)
                defaults_dict[field_name] = default_value
            else:
                if defaults:
                    raise TypeError('Non-default namedtuple field {field_name} cannot follow default field(s) {default_names}'.format(field_name=field_name,
                      default_names=(', '.join(defaults_dict.keys()))))
        else:
            nm_tpl.__new__.__annotations__ = dict(types)
            nm_tpl.__new__.__defaults__ = tuple(defaults)
            nm_tpl._field_defaults = defaults_dict
            for key in ns:
                if key in _prohibited:
                    raise AttributeError('Cannot overwrite NamedTuple attribute ' + key)
                else:
                    if key not in _special:
                        if key not in nm_tpl._fields:
                            setattr(nm_tpl, key, ns[key])
            else:
                return nm_tpl


class NamedTuple(metaclass=NamedTupleMeta):
    __doc__ = "Typed version of namedtuple.\n\n    Usage in Python versions >= 3.6::\n\n        class Employee(NamedTuple):\n            name: str\n            id: int\n\n    This is equivalent to::\n\n        Employee = collections.namedtuple('Employee', ['name', 'id'])\n\n    The resulting class has an extra __annotations__ attribute, giving a\n    dict that maps field names to types.  (The field names are also in\n    the _fields attribute, which is part of the namedtuple API.)\n    Alternative equivalent keyword syntax is also accepted::\n\n        Employee = NamedTuple('Employee', name=str, id=int)\n\n    In Python versions <= 3.5 use::\n\n        Employee = NamedTuple('Employee', [('name', str), ('id', int)])\n    "
    _root = True

    def __new__(*args, **kwargs):
        if not args:
            raise TypeError('NamedTuple.__new__(): not enough arguments')
        cls, *args = args
        if args:
            typename, *args = args
        elif 'typename' in kwargs:
            typename = kwargs.pop('typename')
            import warnings
            warnings.warn("Passing 'typename' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            raise TypeError("NamedTuple.__new__() missing 1 required positional argument: 'typename'")
        if args:
            try:
                fields, = args
            except ValueError:
                raise TypeError(f"NamedTuple.__new__() takes from 2 to 3 positional arguments but {len(args) + 2} were given") from None

        elif 'fields' in kwargs and len(kwargs) == 1:
            fields = kwargs.pop('fields')
            import warnings
            warnings.warn("Passing 'fields' as keyword argument is deprecated", DeprecationWarning,
              stacklevel=2)
        else:
            fields = None
        if fields is None:
            fields = kwargs.items()
        elif kwargs:
            raise TypeError('Either list of fields or keywords can be provided to NamedTuple, not both')
        return _make_nmtuple(typename, fields)

    __new__.__text_signature__ = '($cls, typename, fields=None, /, **kwargs)'


def _dict_new(cls, *args, **kwargs):
    return dict(*args, **kwargs)


def _typeddict_new(cls, typename, fields=None, *, total=True, **kwargs):
    if fields is None:
        fields = kwargs
    elif kwargs:
        raise TypeError('TypedDict takes either a dict or keyword arguments, but not both')
    ns = {'__annotations__':dict(fields), 
     '__total__':total}
    try:
        ns['__module__'] = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    else:
        return _TypedDictMeta(typename, (), ns)


def _check_fails(cls, other):
    raise TypeError('TypedDict does not support instance and class checks')


class _TypedDictMeta(type):

    def __new__(cls, name, bases, ns, total=True):
        """Create new typed dict class object.

        This method is called directly when TypedDict is subclassed,
        or via _typeddict_new when TypedDict is instantiated. This way
        TypedDict supports all three syntax forms described in its docstring.
        Subclasses and instances of TypedDict return actual dictionaries
        via _dict_new.
        """
        ns['__new__'] = _typeddict_new if name == 'TypedDict' else _dict_new
        tp_dict = super(_TypedDictMeta, cls).__new__(cls, name, (dict,), ns)
        anns = ns.get('__annotations__', {})
        msg = "TypedDict('Name', {f0: t0, f1: t1, ...}); each t must be a type"
        anns = {_type_check(tp, msg):n for n, tp in anns.items()}
        for base in bases:
            anns.update(base.__dict__.get('__annotations__', {}))
        else:
            tp_dict.__annotations__ = anns
            if not hasattr(tp_dict, '__total__'):
                tp_dict.__total__ = total
            return tp_dict

    __instancecheck__ = __subclasscheck__ = _check_fails


class TypedDict(dict, metaclass=_TypedDictMeta):
    __doc__ = "A simple typed namespace. At runtime it is equivalent to a plain dict.\n\n    TypedDict creates a dictionary type that expects all of its\n    instances to have a certain set of keys, where each key is\n    associated with a value of a consistent type. This expectation\n    is not checked at runtime but is only enforced by type checkers.\n    Usage::\n\n        class Point2D(TypedDict):\n            x: int\n            y: int\n            label: str\n\n        a: Point2D = {'x': 1, 'y': 2, 'label': 'good'}  # OK\n        b: Point2D = {'z': 3, 'label': 'bad'}           # Fails type check\n\n        assert Point2D(x=1, y=2, label='first') == dict(x=1, y=2, label='first')\n\n    The type info can be accessed via Point2D.__annotations__. TypedDict\n    supports two additional equivalent forms::\n\n        Point2D = TypedDict('Point2D', x=int, y=int, label=str)\n        Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})\n\n    By default, all keys must be present in a TypedDict. It is possible\n    to override this by specifying totality.\n    Usage::\n\n        class point2D(TypedDict, total=False):\n            x: int\n            y: int\n\n    This means that a point2D TypedDict can have any of the keys omitted.A type\n    checker is only expected to support a literal False or True as the value of\n    the total argument. True is the default, and makes all items defined in the\n    class body be required.\n\n    The class syntax is only supported in Python 3.6+, while two other\n    syntax forms work for Python 2.7 and 3.2+\n    "


def NewType(name, tp):
    """NewType creates simple unique types with almost zero
    runtime overhead. NewType(name, tp) is considered a subtype of tp
    by static type checkers. At runtime, NewType(name, tp) returns
    a dummy function that simply returns its argument. Usage::

        UserId = NewType('UserId', int)

        def name_by_id(user_id: UserId) -> str:
            ...

        UserId('user')          # Fails type check

        name_by_id(42)          # Fails type check
        name_by_id(UserId(42))  # OK

        num = UserId(5) + 1     # type: int
    """

    def new_type(x):
        return x

    new_type.__name__ = name
    new_type.__supertype__ = tp
    return new_type


Text = str
TYPE_CHECKING = False

class IO(Generic[AnyStr]):
    __doc__ = 'Generic base class for TextIO and BinaryIO.\n\n    This is an abstract, generic version of the return of open().\n\n    NOTE: This does not distinguish between the different possible\n    classes (text vs. binary, read vs. write vs. read/write,\n    append-only, unbuffered).  The TextIO and BinaryIO subclasses\n    below capture the distinctions between text vs. binary, which is\n    pervasive in the interface; however we currently do not offer a\n    way to track the other distinctions in the type system.\n    '
    __slots__ = ()

    @property
    @abstractmethod
    def mode(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @property
    @abstractmethod
    def closed(self) -> bool:
        pass

    @abstractmethod
    def fileno(self) -> int:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass

    @abstractmethod
    def isatty(self) -> bool:
        pass

    @abstractmethod
    def read(self, n: int=-1) -> AnyStr:
        pass

    @abstractmethod
    def readable(self) -> bool:
        pass

    @abstractmethod
    def readline(self, limit: int=-1) -> AnyStr:
        pass

    @abstractmethod
    def readlines(self, hint: int=-1) -> List[AnyStr]:
        pass

    @abstractmethod
    def seek(self, offset: int, whence: int=0) -> int:
        pass

    @abstractmethod
    def seekable(self) -> bool:
        pass

    @abstractmethod
    def tell(self) -> int:
        pass

    @abstractmethod
    def truncate(self, size: int=None) -> int:
        pass

    @abstractmethod
    def writable(self) -> bool:
        pass

    @abstractmethod
    def write(self, s: AnyStr) -> int:
        pass

    @abstractmethod
    def writelines(self, lines: List[AnyStr]) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> 'IO[AnyStr]':
        pass

    @abstractmethod
    def __exit__(self, type, value, traceback) -> None:
        pass


class BinaryIO(IO[bytes]):
    __doc__ = 'Typed version of the return of open() in binary mode.'
    __slots__ = ()

    @abstractmethod
    def write(self, s: Union[(bytes, bytearray)]) -> int:
        pass

    @abstractmethod
    def __enter__(self) -> 'BinaryIO':
        pass


class TextIO(IO[str]):
    __doc__ = 'Typed version of the return of open() in text mode.'
    __slots__ = ()

    @property
    @abstractmethod
    def buffer(self) -> BinaryIO:
        pass

    @property
    @abstractmethod
    def encoding(self) -> str:
        pass

    @property
    @abstractmethod
    def errors(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def line_buffering(self) -> bool:
        pass

    @property
    @abstractmethod
    def newlines(self) -> Any:
        pass

    @abstractmethod
    def __enter__(self) -> 'TextIO':
        pass


class io:
    __doc__ = 'Wrapper namespace for IO generic classes.'
    __all__ = [
     'IO', 'TextIO', 'BinaryIO']
    IO = IO
    TextIO = TextIO
    BinaryIO = BinaryIO


io.__name__ = __name__ + '.io'
sys.modules[io.__name__] = io
Pattern = _alias(stdlib_re.Pattern, AnyStr)
Match = _alias(stdlib_re.Match, AnyStr)

class re:
    __doc__ = 'Wrapper namespace for re type aliases.'
    __all__ = [
     'Pattern', 'Match']
    Pattern = Pattern
    Match = Match


re.__name__ = __name__ + '.re'
sys.modules[re.__name__] = re