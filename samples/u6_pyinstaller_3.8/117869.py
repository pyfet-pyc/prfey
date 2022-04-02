# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\attr\_make.py
from __future__ import absolute_import, division, print_function
import copy, linecache, sys, threading, uuid, warnings
from operator import itemgetter
from . import _config
from ._compat import PY2, isclass, iteritems, metadata_proxy, ordered_dict, set_closure_cell
from .exceptions import DefaultAlreadySetError, FrozenInstanceError, NotAnAttrsClassError, PythonTooOldError, UnannotatedAttributeError
_obj_setattr = object.__setattr__
_init_converter_pat = '__attr_converter_{}'
_init_factory_pat = '__attr_factory_{}'
_tuple_property_pat = '    {attr_name} = _attrs_property(_attrs_itemgetter({index}))'
_classvar_prefixes = ('typing.ClassVar', 't.ClassVar', 'ClassVar')
_hash_cache_field = '_attrs_cached_hash'
_empty_metadata_singleton = metadata_proxy({})
_sentinel = object()

class _Nothing(object):
    __doc__ = '\n    Sentinel class to indicate the lack of a value when ``None`` is ambiguous.\n\n    ``_Nothing`` is a singleton. There is only ever one of it.\n    '
    _singleton = None

    def __new__(cls):
        if _Nothing._singleton is None:
            _Nothing._singleton = super(_Nothing, cls).__new__(cls)
        return _Nothing._singleton

    def __repr__(self):
        return 'NOTHING'


NOTHING = _Nothing()

def attrib(default=NOTHING, validator=None, repr=True, cmp=None, hash=None, init=True, metadata=None, type=None, converter=None, factory=None, kw_only=False, eq=None, order=None):
    r"""
    Create a new attribute on a class.

    ..  warning::

        Does *not* do anything unless the class is also decorated with
        `attr.s`!

    :param default: A value that is used if an ``attrs``-generated ``__init__``
        is used and no value is passed while instantiating or the attribute is
        excluded using ``init=False``.

        If the value is an instance of `Factory`, its callable will be
        used to construct a new value (useful for mutable data types like lists
        or dicts).

        If a default is not set (or set manually to ``attr.NOTHING``), a value
        *must* be supplied when instantiating; otherwise a `TypeError`
        will be raised.

        The default can also be set using decorator notation as shown below.

    :type default: Any value

    :param callable factory: Syntactic sugar for
        ``default=attr.Factory(callable)``.

    :param validator: `callable` that is called by ``attrs``-generated
        ``__init__`` methods after the instance has been initialized.  They
        receive the initialized instance, the `Attribute`, and the
        passed value.

        The return value is *not* inspected so the validator has to throw an
        exception itself.

        If a ``list`` is passed, its items are treated as validators and must
        all pass.

        Validators can be globally disabled and re-enabled using
        `get_run_validators`.

        The validator can also be set using decorator notation as shown below.

    :type validator: ``callable`` or a ``list`` of ``callable``\ s.

    :param repr: Include this attribute in the generated ``__repr__``
        method. If ``True``, include the attribute; if ``False``, omit it. By
        default, the built-in ``repr()`` function is used. To override how the
        attribute value is formatted, pass a ``callable`` that takes a single
        value and returns a string. Note that the resulting string is used
        as-is, i.e. it will be used directly *instead* of calling ``repr()``
        (the default).
    :type repr: a ``bool`` or a ``callable`` to use a custom function.
    :param bool eq: If ``True`` (default), include this attribute in the
        generated ``__eq__`` and ``__ne__`` methods that check two instances
        for equality.
    :param bool order: If ``True`` (default), include this attributes in the
        generated ``__lt__``, ``__le__``, ``__gt__`` and ``__ge__`` methods.
    :param bool cmp: Setting to ``True`` is equivalent to setting ``eq=True,
        order=True``. Deprecated in favor of *eq* and *order*.
    :param hash: Include this attribute in the generated ``__hash__``
        method.  If ``None`` (default), mirror *eq*'s value.  This is the
        correct behavior according the Python spec.  Setting this value to
        anything else than ``None`` is *discouraged*.
    :type hash: ``bool`` or ``None``
    :param bool init: Include this attribute in the generated ``__init__``
        method.  It is possible to set this to ``False`` and set a default
        value.  In that case this attributed is unconditionally initialized
        with the specified default value or factory.
    :param callable converter: `callable` that is called by
        ``attrs``-generated ``__init__`` methods to converter attribute's value
        to the desired format.  It is given the passed-in value, and the
        returned value will be used as the new value of the attribute.  The
        value is converted before being passed to the validator, if any.
    :param metadata: An arbitrary mapping, to be used by third-party
        components.  See `extending_metadata`.
    :param type: The type of the attribute.  In Python 3.6 or greater, the
        preferred method to specify the type is using a variable annotation
        (see `PEP 526 <https://www.python.org/dev/peps/pep-0526/>`_).
        This argument is provided for backward compatibility.
        Regardless of the approach used, the type will be stored on
        ``Attribute.type``.

        Please note that ``attrs`` doesn't do anything with this metadata by
        itself. You can use it as part of your own code or for
        `static type checking <types>`.
    :param kw_only: Make this attribute keyword-only (Python 3+)
        in the generated ``__init__`` (if ``init`` is ``False``, this
        parameter is ignored).

    .. versionadded:: 15.2.0 *convert*
    .. versionadded:: 16.3.0 *metadata*
    .. versionchanged:: 17.1.0 *validator* can be a ``list`` now.
    .. versionchanged:: 17.1.0
       *hash* is ``None`` and therefore mirrors *eq* by default.
    .. versionadded:: 17.3.0 *type*
    .. deprecated:: 17.4.0 *convert*
    .. versionadded:: 17.4.0 *converter* as a replacement for the deprecated
       *convert* to achieve consistency with other noun-based arguments.
    .. versionadded:: 18.1.0
       ``factory=f`` is syntactic sugar for ``default=attr.Factory(f)``.
    .. versionadded:: 18.2.0 *kw_only*
    .. versionchanged:: 19.2.0 *convert* keyword argument removed
    .. versionchanged:: 19.2.0 *repr* also accepts a custom callable.
    .. deprecated:: 19.2.0 *cmp* Removal on or after 2021-06-01.
    .. versionadded:: 19.2.0 *eq* and *order*
    """
    eq, order = _determine_eq_order(cmp, eq, order)
    if hash is not None:
        if hash is not True:
            if hash is not False:
                raise TypeError('Invalid value for hash.  Must be True, False, or None.')
    if factory is not None:
        if default is not NOTHING:
            raise ValueError('The `default` and `factory` arguments are mutually exclusive.')
        if not callable(factory):
            raise ValueError('The `factory` argument must be a callable.')
        default = Factory(factory)
    if metadata is None:
        metadata = {}
    return _CountingAttr(default=default,
      validator=validator,
      repr=repr,
      cmp=None,
      hash=hash,
      init=init,
      converter=converter,
      metadata=metadata,
      type=type,
      kw_only=kw_only,
      eq=eq,
      order=order)


def _make_attr_tuple_class(cls_name, attr_names):
    """
    Create a tuple subclass to hold `Attribute`s for an `attrs` class.

    The subclass is a bare tuple with properties for names.

    class MyClassAttributes(tuple):
        __slots__ = ()
        x = property(itemgetter(0))
    """
    attr_class_name = '{}Attributes'.format(cls_name)
    attr_class_template = [
     'class {}(tuple):'.format(attr_class_name),
     '    __slots__ = ()']
    if attr_names:
        for i, attr_name in enumerate(attr_names):
            attr_class_template.append(_tuple_property_pat.format(index=i, attr_name=attr_name))

    else:
        attr_class_template.append('    pass')
    globs = {'_attrs_itemgetter':itemgetter, 
     '_attrs_property':property}
    eval(compile('\n'.join(attr_class_template), '', 'exec'), globs)
    return globs[attr_class_name]


_Attributes = _make_attr_tuple_class('_Attributes', [
 'attrs',
 'base_attrs',
 'base_attrs_map'])

def _is_class_var(annot):
    """
    Check whether *annot* is a typing.ClassVar.

    The string comparison hack is used to avoid evaluating all string
    annotations which would put attrs-based classes at a performance
    disadvantage compared to plain old classes.
    """
    return str(annot).startswith(_classvar_prefixes)


def _get_annotations(cls):
    """
    Get annotations for *cls*.
    """
    anns = getattr(cls, '__annotations__', None)
    if anns is None:
        return {}
    for base_cls in cls.__mro__[1:]:
        if anns is getattr(base_cls, '__annotations__', None):
            return {}
        return anns


def _counter_getter(e):
    """
    Key function for sorting to avoid re-creating a lambda for every class.
    """
    return e[1].counter


def _transform_attrs(cls, these, auto_attribs, kw_only):
    """
    Transform all `_CountingAttr`s on a class into `Attribute`s.

    If *these* is passed, use that and don't look for them on the class.

    Return an `_Attributes`.
    """
    cd = cls.__dict__
    anns = _get_annotations(cls)
    if these is not None:
        ca_list = [(
         name, ca) for name, ca in iteritems(these)]
        if not isinstance(these, ordered_dict):
            ca_list.sort(key=_counter_getter)
    else:
        if auto_attribs is True:
            ca_names = {name for name, attr in cd.items() if isinstance(attr, _CountingAttr) if isinstance(attr, _CountingAttr)}
            ca_list = []
            annot_names = set()
            for attr_name, type in anns.items():
                if _is_class_var(type):
                    pass
                else:
                    annot_names.add(attr_name)
                    a = cd.get(attr_name, NOTHING)
                    if not isinstance(a, _CountingAttr):
                        if a is NOTHING:
                            a = attrib()
                        else:
                            a = attrib(default=a)
                    ca_list.append((attr_name, a))
            else:
                unannotated = ca_names - annot_names
                if len(unannotated) > 0:
                    raise UnannotatedAttributeError('The following `attr.ib`s lack a type annotation: ' + ', '.join(sorted(unannotated, key=(lambda n: cd.get(n).counter))) + '.')
                else:
                    ca_list = sorted(((
                     name, attr) for name, attr in cd.items() if isinstance(attr, _CountingAttr)),
                      key=(lambda e: e[1].counter))

        else:
            own_attrs = [Attribute.from_counting_attr(name=attr_name,
              ca=ca,
              type=(anns.get(attr_name))) for attr_name, ca in ca_list]
            base_attrs = []
            base_attr_map = {}
            taken_attr_names = {a:a.name for a in own_attrs}
            for base_cls in cls.__mro__[1:-1]:
                sub_attrs = getattr(base_cls, '__attrs_attrs__', None)
                if sub_attrs is not None:
                    for a in sub_attrs:
                        prev_a = taken_attr_names.get(a.name)
                        if prev_a is None:
                            base_attrs.append(a)
                            taken_attr_names[a.name] = a
                            base_attr_map[a.name] = base_cls
                    else:
                        attr_names = [a.name for a in base_attrs + own_attrs]
                        AttrsClass = _make_attr_tuple_class(cls.__name__, attr_names)

                    if kw_only:
                        own_attrs = [a._assoc(kw_only=True) for a in own_attrs]
                        base_attrs = [a._assoc(kw_only=True) for a in base_attrs]

        attrs = AttrsClass(base_attrs + own_attrs)
        had_default = False
        for a in (a for a in attrs if a.init is not False if a.kw_only is False):
            if had_default is True:
                if a.default is NOTHING:
                    raise ValueError('No mandatory attributes allowed after an attribute with a default value or factory.  Attribute in question: %r' % (
                     a,))
                if had_default is False and a.default is not NOTHING:
                    had_default = True
            return _Attributes((attrs, base_attrs, base_attr_map))


def _frozen_setattrs(self, name, value):
    """
    Attached to frozen classes as __setattr__.
    """
    raise FrozenInstanceError()


def _frozen_delattrs(self, name):
    """
    Attached to frozen classes as __delattr__.
    """
    raise FrozenInstanceError()


class _ClassBuilder(object):
    __doc__ = '\n    Iteratively build *one* class.\n    '
    __slots__ = ('_cls', '_cls_dict', '_attrs', '_base_names', '_attr_names', '_slots',
                 '_frozen', '_weakref_slot', '_cache_hash', '_has_post_init', '_delete_attribs',
                 '_base_attr_map', '_is_exc')

    def __init__(self, cls, these, slots, frozen, weakref_slot, auto_attribs, kw_only, cache_hash, is_exc):
        attrs, base_attrs, base_map = _transform_attrs(cls, these, auto_attribs, kw_only)
        self._cls = cls
        self._cls_dict = dict(cls.__dict__) if slots else {}
        self._attrs = attrs
        self._base_names = set((a.name for a in base_attrs))
        self._base_attr_map = base_map
        self._attr_names = tuple((a.name for a in attrs))
        self._slots = slots
        self._frozen = frozen or _has_frozen_base_class(cls)
        self._weakref_slot = weakref_slot
        self._cache_hash = cache_hash
        self._has_post_init = bool(getattr(cls, '__attrs_post_init__', False))
        self._delete_attribs = not bool(these)
        self._is_exc = is_exc
        self._cls_dict['__attrs_attrs__'] = self._attrs
        if frozen:
            self._cls_dict['__setattr__'] = _frozen_setattrs
            self._cls_dict['__delattr__'] = _frozen_delattrs

    def __repr__(self):
        return '<_ClassBuilder(cls={cls})>'.format(cls=(self._cls.__name__))

    def build_class(self):
        """
        Finalize class based on the accumulated configuration.

        Builder cannot be used after calling this method.
        """
        if self._slots is True:
            return self._create_slots_class()
        return self._patch_original_class()

    def _patch_original_class(self):
        """
        Apply accumulated methods and return the class.
        """
        cls = self._cls
        base_names = self._base_names
        if self._delete_attribs:
            for name in self._attr_names:
                if name not in base_names and getattr(cls, name, _sentinel) is not _sentinel:
                    try:
                        delattr(cls, name)
                    except AttributeError:
                        pass

        for name, value in self._cls_dict.items():
            setattr(cls, name, value)
        else:
            if self._cache_hash:
                existing_set_state_method = getattr(cls, '__setstate__', None)
                if existing_set_state_method:
                    raise NotImplementedError('Currently you cannot use hash caching if you specify your own __setstate__ method.See https://github.com/python-attrs/attrs/issues/494 .')

                def cache_hash_set_state(chss_self, _):
                    setattr(chss_self, _hash_cache_field, None)

                setattr(cls, '__setstate__', cache_hash_set_state)
            return cls

    def _create_slots_class--- This code section failed: ---

 L. 552         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _base_names
                4  STORE_DEREF              'base_names'

 L. 553         6  LOAD_CLOSURE             'self'
                8  BUILD_TUPLE_1         1 
               10  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               12  LOAD_STR                 '_ClassBuilder._create_slots_class.<locals>.<dictcomp>'
               14  MAKE_FUNCTION_8          'closure'

 L. 555        16  LOAD_GLOBAL              iteritems
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                _cls_dict
               22  CALL_FUNCTION_1       1  ''

 L. 553        24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'cd'

 L. 559        30  LOAD_CONST               False
               32  STORE_FAST               'weakref_inherited'

 L. 562        34  LOAD_DEREF               'self'
               36  LOAD_ATTR                _cls
               38  LOAD_ATTR                __mro__
               40  LOAD_CONST               1
               42  LOAD_CONST               -1
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  GET_ITER         
             50_0  COME_FROM            68  '68'
               50  FOR_ITER             80  'to 80'
               52  STORE_FAST               'base_cls'

 L. 563        54  LOAD_STR                 '__weakref__'
               56  LOAD_GLOBAL              getattr
               58  LOAD_FAST                'base_cls'
               60  LOAD_STR                 '__dict__'
               62  LOAD_CONST               ()
               64  CALL_FUNCTION_3       3  ''
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE    50  'to 50'

 L. 564        70  LOAD_CONST               True
               72  STORE_FAST               'weakref_inherited'

 L. 565        74  POP_TOP          
               76  BREAK_LOOP           80  'to 80'
               78  JUMP_BACK            50  'to 50'

 L. 567        80  LOAD_DEREF               'self'
               82  LOAD_ATTR                _attr_names
               84  STORE_FAST               'names'

 L. 569        86  LOAD_DEREF               'self'
               88  LOAD_ATTR                _weakref_slot

 L. 568        90  POP_JUMP_IF_FALSE   130  'to 130'

 L. 570        92  LOAD_STR                 '__weakref__'
               94  LOAD_GLOBAL              getattr
               96  LOAD_DEREF               'self'
               98  LOAD_ATTR                _cls
              100  LOAD_STR                 '__slots__'
              102  LOAD_CONST               ()
              104  CALL_FUNCTION_3       3  ''
              106  COMPARE_OP               not-in

 L. 568       108  POP_JUMP_IF_FALSE   130  'to 130'

 L. 571       110  LOAD_STR                 '__weakref__'
              112  LOAD_FAST                'names'
              114  COMPARE_OP               not-in

 L. 568       116  POP_JUMP_IF_FALSE   130  'to 130'

 L. 572       118  LOAD_FAST                'weakref_inherited'

 L. 568       120  POP_JUMP_IF_TRUE    130  'to 130'

 L. 574       122  LOAD_FAST                'names'
              124  LOAD_CONST               ('__weakref__',)
              126  INPLACE_ADD      
              128  STORE_FAST               'names'
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM           116  '116'
            130_2  COME_FROM           108  '108'
            130_3  COME_FROM            90  '90'

 L. 578       130  LOAD_CLOSURE             'base_names'
              132  BUILD_TUPLE_1         1 
              134  LOAD_LISTCOMP            '<code_object <listcomp>>'
              136  LOAD_STR                 '_ClassBuilder._create_slots_class.<locals>.<listcomp>'
              138  MAKE_FUNCTION_8          'closure'
              140  LOAD_FAST                'names'
              142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'slot_names'

 L. 579       148  LOAD_DEREF               'self'
              150  LOAD_ATTR                _cache_hash
              152  POP_JUMP_IF_FALSE   164  'to 164'

 L. 580       154  LOAD_FAST                'slot_names'
              156  LOAD_METHOD              append
              158  LOAD_GLOBAL              _hash_cache_field
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
            164_0  COME_FROM           152  '152'

 L. 581       164  LOAD_GLOBAL              tuple
              166  LOAD_FAST                'slot_names'
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_FAST                'cd'
              172  LOAD_STR                 '__slots__'
              174  STORE_SUBSCR     

 L. 583       176  LOAD_GLOBAL              getattr
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                _cls
              182  LOAD_STR                 '__qualname__'
              184  LOAD_CONST               None
              186  CALL_FUNCTION_3       3  ''
              188  STORE_FAST               'qualname'

 L. 584       190  LOAD_FAST                'qualname'
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   206  'to 206'

 L. 585       198  LOAD_FAST                'qualname'
              200  LOAD_FAST                'cd'
              202  LOAD_STR                 '__qualname__'
              204  STORE_SUBSCR     
            206_0  COME_FROM           196  '196'

 L. 588       206  LOAD_GLOBAL              tuple
              208  LOAD_GENEXPR             '<code_object <genexpr>>'
              210  LOAD_STR                 '_ClassBuilder._create_slots_class.<locals>.<genexpr>'
              212  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 589       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                _attr_names

 L. 588       218  GET_ITER         
              220  CALL_FUNCTION_1       1  ''
              222  CALL_FUNCTION_1       1  ''
              224  STORE_DEREF              'state_attr_names'

 L. 592       226  LOAD_CLOSURE             'state_attr_names'
              228  BUILD_TUPLE_1         1 
              230  LOAD_CODE                <code_object slots_getstate>
              232  LOAD_STR                 '_ClassBuilder._create_slots_class.<locals>.slots_getstate'
              234  MAKE_FUNCTION_8          'closure'
              236  STORE_FAST               'slots_getstate'

 L. 598       238  LOAD_DEREF               'self'
              240  LOAD_ATTR                _cache_hash
              242  STORE_DEREF              'hash_caching_enabled'

 L. 600       244  LOAD_CLOSURE             'hash_caching_enabled'
              246  LOAD_CLOSURE             'state_attr_names'
              248  BUILD_TUPLE_2         2 
              250  LOAD_CODE                <code_object slots_setstate>
              252  LOAD_STR                 '_ClassBuilder._create_slots_class.<locals>.slots_setstate'
              254  MAKE_FUNCTION_8          'closure'
              256  STORE_FAST               'slots_setstate'

 L. 616       258  LOAD_FAST                'slots_getstate'
              260  LOAD_FAST                'cd'
              262  LOAD_STR                 '__getstate__'
              264  STORE_SUBSCR     

 L. 617       266  LOAD_FAST                'slots_setstate'
              268  LOAD_FAST                'cd'
              270  LOAD_STR                 '__setstate__'
              272  STORE_SUBSCR     

 L. 620       274  LOAD_GLOBAL              type
              276  LOAD_DEREF               'self'
              278  LOAD_ATTR                _cls
              280  CALL_FUNCTION_1       1  ''
              282  LOAD_DEREF               'self'
              284  LOAD_ATTR                _cls
              286  LOAD_ATTR                __name__
              288  LOAD_DEREF               'self'
              290  LOAD_ATTR                _cls
              292  LOAD_ATTR                __bases__
              294  LOAD_FAST                'cd'
              296  CALL_FUNCTION_3       3  ''
              298  STORE_FAST               'cls'

 L. 628       300  LOAD_FAST                'cls'
              302  LOAD_ATTR                __dict__
              304  LOAD_METHOD              values
              306  CALL_METHOD_0         0  ''
              308  GET_ITER         
              310  FOR_ITER            408  'to 408'
              312  STORE_FAST               'item'

 L. 629       314  LOAD_GLOBAL              isinstance
              316  LOAD_FAST                'item'
              318  LOAD_GLOBAL              classmethod
              320  LOAD_GLOBAL              staticmethod
              322  BUILD_TUPLE_2         2 
              324  CALL_FUNCTION_2       2  ''
          326_328  POP_JUMP_IF_FALSE   346  'to 346'

 L. 632       330  LOAD_GLOBAL              getattr
              332  LOAD_FAST                'item'
              334  LOAD_ATTR                __func__
              336  LOAD_STR                 '__closure__'
              338  LOAD_CONST               None
              340  CALL_FUNCTION_3       3  ''
              342  STORE_FAST               'closure_cells'
              344  JUMP_FORWARD        358  'to 358'
            346_0  COME_FROM           326  '326'

 L. 634       346  LOAD_GLOBAL              getattr
              348  LOAD_FAST                'item'
              350  LOAD_STR                 '__closure__'
              352  LOAD_CONST               None
              354  CALL_FUNCTION_3       3  ''
              356  STORE_FAST               'closure_cells'
            358_0  COME_FROM           344  '344'

 L. 636       358  LOAD_FAST                'closure_cells'
          360_362  POP_JUMP_IF_TRUE    368  'to 368'

 L. 637   364_366  JUMP_BACK           310  'to 310'
            368_0  COME_FROM           360  '360'

 L. 638       368  LOAD_FAST                'closure_cells'
              370  GET_ITER         
            372_0  COME_FROM           386  '386'
              372  FOR_ITER            404  'to 404'
              374  STORE_FAST               'cell'

 L. 639       376  LOAD_FAST                'cell'
              378  LOAD_ATTR                cell_contents
              380  LOAD_DEREF               'self'
              382  LOAD_ATTR                _cls
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_FALSE   372  'to 372'

 L. 640       390  LOAD_GLOBAL              set_closure_cell
              392  LOAD_FAST                'cell'
              394  LOAD_FAST                'cls'
              396  CALL_FUNCTION_2       2  ''
              398  POP_TOP          
          400_402  JUMP_BACK           372  'to 372'
          404_406  JUMP_BACK           310  'to 310'

 L. 642       408  LOAD_FAST                'cls'
              410  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 10

    def add_repr(self, ns):
        self._cls_dict['__repr__'] = self._add_method_dunders(_make_repr((self._attrs), ns=ns))
        return self

    def add_str(self):
        repr = self._cls_dict.get('__repr__')
        if repr is None:
            raise ValueError('__str__ can only be generated if a __repr__ exists.')

        def __str__(self):
            return self.__repr__()

        self._cls_dict['__str__'] = self._add_method_dunders(__str__)
        return self

    def make_unhashable(self):
        self._cls_dict['__hash__'] = None
        return self

    def add_hash(self):
        self._cls_dict['__hash__'] = self._add_method_dunders(_make_hash((self._cls),
          (self._attrs),
          frozen=(self._frozen),
          cache_hash=(self._cache_hash)))
        return self

    def add_init(self):
        self._cls_dict['__init__'] = self._add_method_dunders(_make_init(self._cls, self._attrs, self._has_post_init, self._frozen, self._slots, self._cache_hash, self._base_attr_map, self._is_exc))
        return self

    def add_eq(self):
        cd = self._cls_dict
        cd['__eq__'], cd['__ne__'] = (self._add_method_dunders(meth) for meth in _make_eq(self._cls, self._attrs))
        return self

    def add_order(self):
        cd = self._cls_dict
        cd['__lt__'], cd['__le__'], cd['__gt__'], cd['__ge__'] = (self._add_method_dunders(meth) for meth in _make_order(self._cls, self._attrs))
        return self

    def _add_method_dunders(self, method):
        """
        Add __module__ and __qualname__ to a *method* if possible.
        """
        try:
            method.__module__ = self._cls.__module__
        except AttributeError:
            pass
        else:
            try:
                method.__qualname__ = '.'.join((
                 self._cls.__qualname__, method.__name__))
            except AttributeError:
                pass
            else:
                return method


_CMP_DEPRECATION = 'The usage of `cmp` is deprecated and will be removed on or after 2021-06-01.  Please use `eq` and `order` instead.'

def _determine_eq_order(cmp, eq, order):
    """
    Validate the combination of *cmp*, *eq*, and *order*. Derive the effective
    values of eq and order.
    """
    if cmp is not None:
        if any((eq is not None, order is not None)):
            raise ValueError("Don't mix `cmp` with `eq' and `order`.")
    else:
        if cmp is not None:
            warnings.warn(_CMP_DEPRECATION, DeprecationWarning, stacklevel=3)
            return (
             cmp, cmp)
        if eq is None:
            eq = True
        if order is None:
            order = eq
        if eq is False and order is True:
            raise ValueError('`order` can only be True if `eq` is True too.')
    return (
     eq, order)


def attrs(maybe_cls=None, these=None, repr_ns=None, repr=True, cmp=None, hash=None, init=True, slots=False, frozen=False, weakref_slot=True, str=False, auto_attribs=False, kw_only=False, cache_hash=False, auto_exc=False, eq=None, order=None):
    r"""
    A class decorator that adds `dunder
    <https://wiki.python.org/moin/DunderAlias>`_\ -methods according to the
    specified attributes using `attr.ib` or the *these* argument.

    :param these: A dictionary of name to `attr.ib` mappings.  This is
        useful to avoid the definition of your attributes within the class body
        because you can't (e.g. if you want to add ``__repr__`` methods to
        Django models) or don't want to.

        If *these* is not ``None``, ``attrs`` will *not* search the class body
        for attributes and will *not* remove any attributes from it.

        If *these* is an ordered dict (`dict` on Python 3.6+,
        `collections.OrderedDict` otherwise), the order is deduced from
        the order of the attributes inside *these*.  Otherwise the order
        of the definition of the attributes is used.

    :type these: `dict` of `str` to `attr.ib`

    :param str repr_ns: When using nested classes, there's no way in Python 2
        to automatically detect that.  Therefore it's possible to set the
        namespace explicitly for a more meaningful ``repr`` output.
    :param bool repr: Create a ``__repr__`` method with a human readable
        representation of ``attrs`` attributes..
    :param bool str: Create a ``__str__`` method that is identical to
        ``__repr__``.  This is usually not necessary except for
        `Exception`\ s.
    :param bool eq: If ``True`` or ``None`` (default), add ``__eq__`` and
        ``__ne__`` methods that check two instances for equality.

        They compare the instances as if they were tuples of their ``attrs``
        attributes, but only iff the types of both classes are *identical*!
    :type eq: `bool` or `None`
    :param bool order: If ``True``, add ``__lt__``, ``__le__``, ``__gt__``,
        and ``__ge__`` methods that behave like *eq* above and allow instances
        to be ordered. If ``None`` (default) mirror value of *eq*.
    :type order: `bool` or `None`
    :param cmp: Setting to ``True`` is equivalent to setting ``eq=True,
        order=True``. Deprecated in favor of *eq* and *order*, has precedence
        over them for backward-compatibility though. Must not be mixed with
        *eq* or *order*.
    :type cmp: `bool` or `None`
    :param hash: If ``None`` (default), the ``__hash__`` method is generated
        according how *eq* and *frozen* are set.

        1. If *both* are True, ``attrs`` will generate a ``__hash__`` for you.
        2. If *eq* is True and *frozen* is False, ``__hash__`` will be set to
           None, marking it unhashable (which it is).
        3. If *eq* is False, ``__hash__`` will be left untouched meaning the
           ``__hash__`` method of the base class will be used (if base class is
           ``object``, this means it will fall back to id-based hashing.).

        Although not recommended, you can decide for yourself and force
        ``attrs`` to create one (e.g. if the class is immutable even though you
        didn't freeze it programmatically) by passing ``True`` or not.  Both of
        these cases are rather special and should be used carefully.

        See our documentation on `hashing`, Python's documentation on
        `object.__hash__`, and the `GitHub issue that led to the default \
        behavior <https://github.com/python-attrs/attrs/issues/136>`_ for more
        details.
    :type hash: ``bool`` or ``None``
    :param bool init: Create a ``__init__`` method that initializes the
        ``attrs`` attributes.  Leading underscores are stripped for the
        argument name.  If a ``__attrs_post_init__`` method exists on the
        class, it will be called after the class is fully initialized.
    :param bool slots: Create a `slotted class <slotted classes>` that's more
        memory-efficient.
    :param bool frozen: Make instances immutable after initialization.  If
        someone attempts to modify a frozen instance,
        `attr.exceptions.FrozenInstanceError` is raised.

        Please note:

            1. This is achieved by installing a custom ``__setattr__`` method
               on your class, so you can't implement your own.

            2. True immutability is impossible in Python.

            3. This *does* have a minor a runtime performance `impact
               <how-frozen>` when initializing new instances.  In other words:
               ``__init__`` is slightly slower with ``frozen=True``.

            4. If a class is frozen, you cannot modify ``self`` in
               ``__attrs_post_init__`` or a self-written ``__init__``. You can
               circumvent that limitation by using
               ``object.__setattr__(self, "attribute_name", value)``.

    :param bool weakref_slot: Make instances weak-referenceable.  This has no
        effect unless ``slots`` is also enabled.
    :param bool auto_attribs: If True, collect `PEP 526`_-annotated attributes
        (Python 3.6 and later only) from the class body.

        In this case, you **must** annotate every field.  If ``attrs``
        encounters a field that is set to an `attr.ib` but lacks a type
        annotation, an `attr.exceptions.UnannotatedAttributeError` is
        raised.  Use ``field_name: typing.Any = attr.ib(...)`` if you don't
        want to set a type.

        If you assign a value to those attributes (e.g. ``x: int = 42``), that
        value becomes the default value like if it were passed using
        ``attr.ib(default=42)``.  Passing an instance of `Factory` also
        works as expected.

        Attributes annotated as `typing.ClassVar`, and attributes that are
        neither annotated nor set to an `attr.ib` are **ignored**.

        .. _`PEP 526`: https://www.python.org/dev/peps/pep-0526/
    :param bool kw_only: Make all attributes keyword-only (Python 3+)
        in the generated ``__init__`` (if ``init`` is ``False``, this
        parameter is ignored).
    :param bool cache_hash: Ensure that the object's hash code is computed
        only once and stored on the object.  If this is set to ``True``,
        hashing must be either explicitly or implicitly enabled for this
        class.  If the hash code is cached, avoid any reassignments of
        fields involved in hash code computation or mutations of the objects
        those fields point to after object creation.  If such changes occur,
        the behavior of the object's hash code is undefined.
    :param bool auto_exc: If the class subclasses `BaseException`
        (which implicitly includes any subclass of any exception), the
        following happens to behave like a well-behaved Python exceptions
        class:

        - the values for *eq*, *order*, and *hash* are ignored and the
          instances compare and hash by the instance's ids (N.B. ``attrs`` will
          *not* remove existing implementations of ``__hash__`` or the equality
          methods. It just won't add own ones.),
        - all attributes that are either passed into ``__init__`` or have a
          default value are additionally available as a tuple in the ``args``
          attribute,
        - the value of *str* is ignored leaving ``__str__`` to base classes.

    .. versionadded:: 16.0.0 *slots*
    .. versionadded:: 16.1.0 *frozen*
    .. versionadded:: 16.3.0 *str*
    .. versionadded:: 16.3.0 Support for ``__attrs_post_init__``.
    .. versionchanged:: 17.1.0
       *hash* supports ``None`` as value which is also the default now.
    .. versionadded:: 17.3.0 *auto_attribs*
    .. versionchanged:: 18.1.0
       If *these* is passed, no attributes are deleted from the class body.
    .. versionchanged:: 18.1.0 If *these* is ordered, the order is retained.
    .. versionadded:: 18.2.0 *weakref_slot*
    .. deprecated:: 18.2.0
       ``__lt__``, ``__le__``, ``__gt__``, and ``__ge__`` now raise a
       `DeprecationWarning` if the classes compared are subclasses of
       each other. ``__eq`` and ``__ne__`` never tried to compared subclasses
       to each other.
    .. versionchanged:: 19.2.0
       ``__lt__``, ``__le__``, ``__gt__``, and ``__ge__`` now do not consider
       subclasses comparable anymore.
    .. versionadded:: 18.2.0 *kw_only*
    .. versionadded:: 18.2.0 *cache_hash*
    .. versionadded:: 19.1.0 *auto_exc*
    .. deprecated:: 19.2.0 *cmp* Removal on or after 2021-06-01.
    .. versionadded:: 19.2.0 *eq* and *order*
    """
    eq, order = _determine_eq_order(cmp, eq, order)

    def wrap(cls):
        if getattr(cls, '__class__', None) is None:
            raise TypeError('attrs only works with new-style classes.')
        else:
            is_exc = auto_exc is True and issubclass(cls, BaseException)
            builder = _ClassBuilder(cls, these, slots, frozen, weakref_slot, auto_attribs, kw_only, cache_hash, is_exc)
            if repr is True:
                builder.add_repr(repr_ns)
            if str is True:
                builder.add_str()
            if eq is True:
                if not is_exc:
                    builder.add_eq()
            if order is True:
                if not is_exc:
                    builder.add_order()
            if hash is not True and hash is not False and hash is not None:
                raise TypeError('Invalid value for hash.  Must be True, False, or None.')
            else:
                pass
            if not (hash is False or hash) is None or eq is False or is_exc:
                if cache_hash:
                    raise TypeError('Invalid value for cache_hash.  To use hash caching, hashing must be either explicitly or implicitly enabled.')
                elif not (hash is True or hash) is None or eq is True and frozen is True:
                    builder.add_hash()
                else:
                    if cache_hash:
                        raise TypeError('Invalid value for cache_hash.  To use hash caching, hashing must be either explicitly or implicitly enabled.')
                    builder.make_unhashable()
        if init is True:
            builder.add_init()
        else:
            if cache_hash:
                raise TypeError('Invalid value for cache_hash.  To use hash caching, init must be True.')
            return builder.build_class()

    if maybe_cls is None:
        return wrap
    return wrap(maybe_cls)


_attrs = attrs
if PY2:

    def _has_frozen_base_class(cls):
        """
        Check whether *cls* has a frozen ancestor by looking at its
        __setattr__.
        """
        return getattr(cls.__setattr__, '__module__', None) == _frozen_setattrs.__module__ and cls.__setattr__.__name__ == _frozen_setattrs.__name__


else:

    def _has_frozen_base_class(cls):
        """
        Check whether *cls* has a frozen ancestor by looking at its
        __setattr__.
        """
        return cls.__setattr__ == _frozen_setattrs


def _attrs_to_tuple(obj, attrs):
    """
    Create a tuple of all values of *obj*'s *attrs*.
    """
    return tuple((getattr(obj, a.name) for a in attrs))


def _generate_unique_filename(cls, func_name):
    """
    Create a "filename" suitable for a function being generated.
    """
    unique_id = uuid.uuid4()
    extra = ''
    count = 1
    while True:
        unique_filename = '<attrs generated {0} {1}.{2}{3}>'.format(func_name, cls.__module__, getattr(cls, '__qualname__', cls.__name__), extra)
        cache_line = (
         1, None, (str(unique_id),), unique_filename)
        if linecache.cache.setdefault(unique_filename, cache_line) == cache_line:
            return unique_filename
        count += 1
        extra = '-{0}'.format(count)


def _make_hash(cls, attrs, frozen, cache_hash):
    attrs = tuple((a for a in attrs if a.hash is True or a.hash is None and a.eq is True))
    tab = '        '
    unique_filename = _generate_unique_filename(cls, 'hash')
    type_hash = hash(unique_filename)
    method_lines = [
     'def __hash__(self):']

    def append_hash_computation_lines(prefix, indent):
        method_lines.extend([
         indent + prefix + 'hash((', indent + '        %d,' % (type_hash,)])
        for a in attrs:
            method_lines.append(indent + '        self.%s,' % a.name)
        else:
            method_lines.append(indent + '    ))')

    if cache_hash:
        method_lines.append(tab + 'if self.%s is None:' % _hash_cache_field)
        if frozen:
            append_hash_computation_lines("object.__setattr__(self, '%s', " % _hash_cache_field, tab * 2)
            method_lines.append(tab * 2 + ')')
        else:
            append_hash_computation_lines('self.%s = ' % _hash_cache_field, tab * 2)
        method_lines.append(tab + 'return self.%s' % _hash_cache_field)
    else:
        append_hash_computation_lines('return ', tab)
    script = '\n'.join(method_lines)
    globs = {}
    locs = {}
    bytecode = compile(script, unique_filename, 'exec')
    eval(bytecode, globs, locs)
    linecache.cache[unique_filename] = (
     len(script),
     None,
     script.splitlines(True),
     unique_filename)
    return locs['__hash__']


def _add_hash(cls, attrs):
    """
    Add a hash method to *cls*.
    """
    cls.__hash__ = _make_hash(cls, attrs, frozen=False, cache_hash=False)
    return cls


def __ne__(self, other):
    """
    Check equality and either forward a NotImplemented or return the result
    negated.
    """
    result = self.__eq__(other)
    if result is NotImplemented:
        return NotImplemented
    return not result


def _make_eq(cls, attrs):
    attrs = [a for a in attrs if a.eq]
    unique_filename = _generate_unique_filename(cls, 'eq')
    lines = [
     'def __eq__(self, other):',
     '    if other.__class__ is not self.__class__:',
     '        return NotImplemented']
    if attrs:
        lines.append('    return  (')
        others = ['    ) == (']
        for a in attrs:
            lines.append('        self.%s,' % (a.name,))
            others.append('        other.%s,' % (a.name,))
        else:
            lines += others + ['    )']

    else:
        lines.append('    return True')
    script = '\n'.join(lines)
    globs = {}
    locs = {}
    bytecode = compile(script, unique_filename, 'exec')
    eval(bytecode, globs, locs)
    linecache.cache[unique_filename] = (
     len(script),
     None,
     script.splitlines(True),
     unique_filename)
    return (
     locs['__eq__'], __ne__)


def _make_order(cls, attrs):
    attrs = [a for a in attrs if a.order]

    def attrs_to_tuple(obj):
        return _attrs_to_tuple(obj, attrs)

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) < attrs_to_tuple(other)
        return NotImplemented

    def __le__(self, other):
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) <= attrs_to_tuple(other)
        return NotImplemented

    def __gt__(self, other):
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) > attrs_to_tuple(other)
        return NotImplemented

    def __ge__(self, other):
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) >= attrs_to_tuple(other)
        return NotImplemented

    return (
     __lt__, __le__, __gt__, __ge__)


def _add_eq(cls, attrs=None):
    """
    Add equality methods to *cls* with *attrs*.
    """
    if attrs is None:
        attrs = cls.__attrs_attrs__
    cls.__eq__, cls.__ne__ = _make_eq(cls, attrs)
    return cls


_already_repring = threading.local()

def _make_repr(attrs, ns):
    """
    Make a repr method that includes relevant *attrs*, adding *ns* to the full
    name.
    """
    attr_names_with_reprs = tuple(((
     a.name, repr if a.repr is True else a.repr) for a in attrs if a.repr is not False))

    def __repr__--- This code section failed: ---

 L.1288         0  SETUP_FINALLY        12  'to 12'

 L.1289         2  LOAD_GLOBAL              _already_repring
                4  LOAD_ATTR                working_set
                6  STORE_FAST               'working_set'
                8  POP_BLOCK        
               10  JUMP_FORWARD         44  'to 44'
             12_0  COME_FROM_FINALLY     0  '0'

 L.1290        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    42  'to 42'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.1291        26  LOAD_GLOBAL              set
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'working_set'

 L.1292        32  LOAD_FAST                'working_set'
               34  LOAD_GLOBAL              _already_repring
               36  STORE_ATTR               working_set
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            18  '18'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            10  '10'

 L.1294        44  LOAD_GLOBAL              id
               46  LOAD_FAST                'self'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_FAST                'working_set'
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.1295        56  LOAD_STR                 '...'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.1296        60  LOAD_FAST                'self'
               62  LOAD_ATTR                __class__
               64  STORE_FAST               'real_cls'

 L.1297        66  LOAD_DEREF               'ns'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE   120  'to 120'

 L.1298        74  LOAD_GLOBAL              getattr
               76  LOAD_FAST                'real_cls'
               78  LOAD_STR                 '__qualname__'
               80  LOAD_CONST               None
               82  CALL_FUNCTION_3       3  ''
               84  STORE_FAST               'qualname'

 L.1299        86  LOAD_FAST                'qualname'
               88  LOAD_CONST               None
               90  COMPARE_OP               is-not
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L.1300        94  LOAD_FAST                'qualname'
               96  LOAD_METHOD              rsplit
               98  LOAD_STR                 '>.'
              100  LOAD_CONST               1
              102  CALL_METHOD_2         2  ''
              104  LOAD_CONST               -1
              106  BINARY_SUBSCR    
              108  STORE_FAST               'class_name'
              110  JUMP_ABSOLUTE       134  'to 134'
            112_0  COME_FROM            92  '92'

 L.1302       112  LOAD_FAST                'real_cls'
              114  LOAD_ATTR                __name__
              116  STORE_FAST               'class_name'
              118  JUMP_FORWARD        134  'to 134'
            120_0  COME_FROM            72  '72'

 L.1304       120  LOAD_DEREF               'ns'
              122  LOAD_STR                 '.'
              124  BINARY_ADD       
              126  LOAD_FAST                'real_cls'
              128  LOAD_ATTR                __name__
              130  BINARY_ADD       
              132  STORE_FAST               'class_name'
            134_0  COME_FROM           118  '118'

 L.1310       134  LOAD_FAST                'working_set'
              136  LOAD_METHOD              add
              138  LOAD_GLOBAL              id
              140  LOAD_FAST                'self'
              142  CALL_FUNCTION_1       1  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L.1311       148  SETUP_FINALLY       242  'to 242'

 L.1312       150  LOAD_FAST                'class_name'
              152  LOAD_STR                 '('
              154  BUILD_LIST_2          2 
              156  STORE_FAST               'result'

 L.1313       158  LOAD_CONST               True
              160  STORE_FAST               'first'

 L.1314       162  LOAD_DEREF               'attr_names_with_reprs'
              164  GET_ITER         
              166  FOR_ITER            224  'to 224'
              168  UNPACK_SEQUENCE_2     2 
              170  STORE_FAST               'name'
              172  STORE_FAST               'attr_repr'

 L.1315       174  LOAD_FAST                'first'
              176  POP_JUMP_IF_FALSE   184  'to 184'

 L.1316       178  LOAD_CONST               False
              180  STORE_FAST               'first'
              182  JUMP_FORWARD        194  'to 194'
            184_0  COME_FROM           176  '176'

 L.1318       184  LOAD_FAST                'result'
              186  LOAD_METHOD              append
              188  LOAD_STR                 ', '
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
            194_0  COME_FROM           182  '182'

 L.1319       194  LOAD_FAST                'result'
              196  LOAD_METHOD              extend

 L.1320       198  LOAD_FAST                'name'
              200  LOAD_STR                 '='
              202  LOAD_FAST                'attr_repr'
              204  LOAD_GLOBAL              getattr
              206  LOAD_FAST                'self'
              208  LOAD_FAST                'name'
              210  LOAD_GLOBAL              NOTHING
              212  CALL_FUNCTION_3       3  ''
              214  CALL_FUNCTION_1       1  ''
              216  BUILD_TUPLE_3         3 

 L.1319       218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_BACK           166  'to 166'

 L.1322       224  LOAD_STR                 ''
              226  LOAD_METHOD              join
              228  LOAD_FAST                'result'
              230  CALL_METHOD_1         1  ''
              232  LOAD_STR                 ')'
              234  BINARY_ADD       
              236  POP_BLOCK        
              238  CALL_FINALLY        242  'to 242'
              240  RETURN_VALUE     
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM_FINALLY   148  '148'

 L.1324       242  LOAD_FAST                'working_set'
              244  LOAD_METHOD              remove
              246  LOAD_GLOBAL              id
              248  LOAD_FAST                'self'
              250  CALL_FUNCTION_1       1  ''
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 238

    return __repr__


def _add_repr(cls, ns=None, attrs=None):
    """
    Add a repr method to *cls*.
    """
    if attrs is None:
        attrs = cls.__attrs_attrs__
    cls.__repr__ = _make_repr(attrs, ns)
    return cls


def _make_init(cls, attrs, post_init, frozen, slots, cache_hash, base_attr_map, is_exc):
    attrs = [a for a in attrs if not a.init if a.default is not NOTHING]
    unique_filename = _generate_unique_filename(cls, 'init')
    script, globs, annotations = _attrs_to_init_script(attrs, frozen, slots, post_init, cache_hash, base_attr_map, is_exc)
    locs = {}
    bytecode = compile(script, unique_filename, 'exec')
    attr_dict = dict(((a.name, a) for a in attrs))
    globs.update({'NOTHING':NOTHING,  'attr_dict':attr_dict})
    if frozen is True:
        globs['_cached_setattr'] = _obj_setattr
    eval(bytecode, globs, locs)
    linecache.cache[unique_filename] = (
     len(script),
     None,
     script.splitlines(True),
     unique_filename)
    __init__ = locs['__init__']
    __init__.__annotations__ = annotations
    return __init__


def fields(cls):
    """
    Return the tuple of ``attrs`` attributes for a class.

    The tuple also allows accessing the fields by their names (see below for
    examples).

    :param type cls: Class to introspect.

    :raise TypeError: If *cls* is not a class.
    :raise attr.exceptions.NotAnAttrsClassError: If *cls* is not an ``attrs``
        class.

    :rtype: tuple (with name accessors) of `attr.Attribute`

    ..  versionchanged:: 16.2.0 Returned tuple allows accessing the fields
        by name.
    """
    if not isclass(cls):
        raise TypeError('Passed object must be a class.')
    attrs = getattr(cls, '__attrs_attrs__', None)
    if attrs is None:
        raise NotAnAttrsClassError('{cls!r} is not an attrs-decorated class.'.format(cls=cls))
    return attrs


def fields_dict(cls):
    r"""
    Return an ordered dictionary of ``attrs`` attributes for a class, whose
    keys are the attribute names.

    :param type cls: Class to introspect.

    :raise TypeError: If *cls* is not a class.
    :raise attr.exceptions.NotAnAttrsClassError: If *cls* is not an ``attrs``
        class.

    :rtype: an ordered dict where keys are attribute names and values are
        `attr.Attribute`\ s. This will be a `dict` if it's
        naturally ordered like on Python 3.6+ or an
        :class:`~collections.OrderedDict` otherwise.

    .. versionadded:: 18.1.0
    """
    if not isclass(cls):
        raise TypeError('Passed object must be a class.')
    attrs = getattr(cls, '__attrs_attrs__', None)
    if attrs is None:
        raise NotAnAttrsClassError('{cls!r} is not an attrs-decorated class.'.format(cls=cls))
    return ordered_dict(((a.name, a) for a in attrs))


def validate(inst):
    """
    Validate all attributes on *inst* that have a validator.

    Leaves all exceptions through.

    :param inst: Instance of a class with ``attrs`` attributes.
    """
    if _config._run_validators is False:
        return
    for a in fields(inst.__class__):
        v = a.validator
        if v is not None:
            v(inst, a, getattr(inst, a.name))


def _is_slot_cls(cls):
    return '__slots__' in cls.__dict__


def _is_slot_attr(a_name, base_attr_map):
    """
    Check if the attribute name comes from a slot class.
    """
    return a_name in base_attr_map and _is_slot_cls(base_attr_map[a_name])


def _attrs_to_init_script--- This code section failed: ---

 L.1472         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L.1473         4  LOAD_GLOBAL              any
                6  LOAD_CLOSURE             'base_attr_map'
                8  BUILD_TUPLE_1         1 
               10  LOAD_GENEXPR             '<code_object <genexpr>>'
               12  LOAD_STR                 '_attrs_to_init_script.<locals>.<genexpr>'
               14  MAKE_FUNCTION_8          'closure'

 L.1474        16  LOAD_FAST                'attrs'

 L.1473        18  GET_ITER         
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'any_slot_ancestors'

 L.1476        26  LOAD_FAST                'frozen'
               28  LOAD_CONST               True
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE   120  'to 120'

 L.1477        34  LOAD_FAST                'slots'
               36  LOAD_CONST               True
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE    70  'to 70'

 L.1478        42  LOAD_FAST                'lines'
               44  LOAD_METHOD              append

 L.1482        46  LOAD_STR                 '_setattr = _cached_setattr.__get__(self, self.__class__)'

 L.1478        48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L.1485        52  LOAD_CODE                <code_object fmt_setter>
               54  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               58  STORE_FAST               'fmt_setter'

 L.1491        60  LOAD_CODE                <code_object fmt_setter_with_converter>
               62  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter_with_converter'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  STORE_FAST               'fmt_setter_with_converter'
               68  JUMP_ABSOLUTE       136  'to 136'
             70_0  COME_FROM            40  '40'

 L.1504        70  LOAD_FAST                'lines'
               72  LOAD_METHOD              append
               74  LOAD_STR                 '_inst_dict = self.__dict__'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.1505        80  LOAD_FAST                'any_slot_ancestors'
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L.1506        84  LOAD_FAST                'lines'
               86  LOAD_METHOD              append

 L.1509        88  LOAD_STR                 '_setattr = _cached_setattr.__get__(self, self.__class__)'

 L.1506        90  CALL_METHOD_1         1  ''
               92  POP_TOP          
             94_0  COME_FROM            82  '82'

 L.1512        94  LOAD_CLOSURE             'base_attr_map'
               96  BUILD_TUPLE_1         1 
               98  LOAD_CODE                <code_object fmt_setter>
              100  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter'
              102  MAKE_FUNCTION_8          'closure'
              104  STORE_FAST               'fmt_setter'

 L.1525       106  LOAD_CLOSURE             'base_attr_map'
              108  BUILD_TUPLE_1         1 
              110  LOAD_CODE                <code_object fmt_setter_with_converter>
              112  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter_with_converter'
              114  MAKE_FUNCTION_8          'closure'
              116  STORE_FAST               'fmt_setter_with_converter'
              118  JUMP_FORWARD        136  'to 136'
            120_0  COME_FROM            32  '32'

 L.1539       120  LOAD_CODE                <code_object fmt_setter>
              122  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter'
              124  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              126  STORE_FAST               'fmt_setter'

 L.1545       128  LOAD_CODE                <code_object fmt_setter_with_converter>
              130  LOAD_STR                 '_attrs_to_init_script.<locals>.fmt_setter_with_converter'
              132  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              134  STORE_FAST               'fmt_setter_with_converter'
            136_0  COME_FROM           118  '118'

 L.1553       136  BUILD_LIST_0          0 
              138  STORE_FAST               'args'

 L.1554       140  BUILD_LIST_0          0 
              142  STORE_FAST               'kw_only_args'

 L.1555       144  BUILD_LIST_0          0 
              146  STORE_FAST               'attrs_to_validate'

 L.1559       148  BUILD_MAP_0           0 
              150  STORE_FAST               'names_for_globals'

 L.1560       152  LOAD_STR                 'return'
              154  LOAD_CONST               None
              156  BUILD_MAP_1           1 
              158  STORE_FAST               'annotations'

 L.1562       160  LOAD_FAST                'attrs'
              162  GET_ITER         
            164_0  COME_FROM           954  '954'
            164_1  COME_FROM           944  '944'
            164_2  COME_FROM           934  '934'
          164_166  FOR_ITER            968  'to 968'
              168  STORE_FAST               'a'

 L.1563       170  LOAD_FAST                'a'
              172  LOAD_ATTR                validator
              174  POP_JUMP_IF_FALSE   186  'to 186'

 L.1564       176  LOAD_FAST                'attrs_to_validate'
              178  LOAD_METHOD              append
              180  LOAD_FAST                'a'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
            186_0  COME_FROM           174  '174'

 L.1565       186  LOAD_FAST                'a'
              188  LOAD_ATTR                name
              190  STORE_FAST               'attr_name'

 L.1566       192  LOAD_FAST                'a'
              194  LOAD_ATTR                name
              196  LOAD_METHOD              lstrip
              198  LOAD_STR                 '_'
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'arg_name'

 L.1567       204  LOAD_GLOBAL              isinstance
              206  LOAD_FAST                'a'
              208  LOAD_ATTR                default
              210  LOAD_GLOBAL              Factory
              212  CALL_FUNCTION_2       2  ''
              214  STORE_FAST               'has_factory'

 L.1568       216  LOAD_FAST                'has_factory'
              218  POP_JUMP_IF_FALSE   234  'to 234'
              220  LOAD_FAST                'a'
              222  LOAD_ATTR                default
              224  LOAD_ATTR                takes_self
              226  POP_JUMP_IF_FALSE   234  'to 234'

 L.1569       228  LOAD_STR                 'self'
              230  STORE_FAST               'maybe_self'
              232  JUMP_FORWARD        238  'to 238'
            234_0  COME_FROM           226  '226'
            234_1  COME_FROM           218  '218'

 L.1571       234  LOAD_STR                 ''
              236  STORE_FAST               'maybe_self'
            238_0  COME_FROM           232  '232'

 L.1572       238  LOAD_FAST                'a'
              240  LOAD_ATTR                init
              242  LOAD_CONST               False
              244  COMPARE_OP               is
          246_248  POP_JUMP_IF_FALSE   458  'to 458'

 L.1573       250  LOAD_FAST                'has_factory'
          252_254  POP_JUMP_IF_FALSE   370  'to 370'

 L.1574       256  LOAD_GLOBAL              _init_factory_pat
              258  LOAD_METHOD              format
              260  LOAD_FAST                'a'
              262  LOAD_ATTR                name
              264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'init_factory_name'

 L.1575       268  LOAD_FAST                'a'
              270  LOAD_ATTR                converter
              272  LOAD_CONST               None
              274  COMPARE_OP               is-not
          276_278  POP_JUMP_IF_FALSE   330  'to 330'

 L.1576       280  LOAD_FAST                'lines'
              282  LOAD_METHOD              append

 L.1577       284  LOAD_FAST                'fmt_setter_with_converter'

 L.1578       286  LOAD_FAST                'attr_name'

 L.1579       288  LOAD_FAST                'init_factory_name'
              290  LOAD_STR                 '({0})'
              292  LOAD_METHOD              format
              294  LOAD_FAST                'maybe_self'
              296  CALL_METHOD_1         1  ''
              298  BINARY_ADD       

 L.1577       300  CALL_FUNCTION_2       2  ''

 L.1576       302  CALL_METHOD_1         1  ''
              304  POP_TOP          

 L.1582       306  LOAD_GLOBAL              _init_converter_pat
              308  LOAD_METHOD              format
              310  LOAD_FAST                'a'
              312  LOAD_ATTR                name
              314  CALL_METHOD_1         1  ''
              316  STORE_FAST               'conv_name'

 L.1583       318  LOAD_FAST                'a'
              320  LOAD_ATTR                converter
              322  LOAD_FAST                'names_for_globals'
              324  LOAD_FAST                'conv_name'
              326  STORE_SUBSCR     
              328  JUMP_FORWARD        356  'to 356'
            330_0  COME_FROM           276  '276'

 L.1585       330  LOAD_FAST                'lines'
              332  LOAD_METHOD              append

 L.1586       334  LOAD_FAST                'fmt_setter'

 L.1587       336  LOAD_FAST                'attr_name'

 L.1588       338  LOAD_FAST                'init_factory_name'
              340  LOAD_STR                 '({0})'
              342  LOAD_METHOD              format
              344  LOAD_FAST                'maybe_self'
              346  CALL_METHOD_1         1  ''
              348  BINARY_ADD       

 L.1586       350  CALL_FUNCTION_2       2  ''

 L.1585       352  CALL_METHOD_1         1  ''
              354  POP_TOP          
            356_0  COME_FROM           328  '328'

 L.1591       356  LOAD_FAST                'a'
              358  LOAD_ATTR                default
              360  LOAD_ATTR                factory
              362  LOAD_FAST                'names_for_globals'
              364  LOAD_FAST                'init_factory_name'
              366  STORE_SUBSCR     
              368  JUMP_FORWARD        926  'to 926'
            370_0  COME_FROM           252  '252'

 L.1593       370  LOAD_FAST                'a'
              372  LOAD_ATTR                converter
              374  LOAD_CONST               None
              376  COMPARE_OP               is-not
          378_380  POP_JUMP_IF_FALSE   430  'to 430'

 L.1594       382  LOAD_FAST                'lines'
              384  LOAD_METHOD              append

 L.1595       386  LOAD_FAST                'fmt_setter_with_converter'

 L.1596       388  LOAD_FAST                'attr_name'

 L.1597       390  LOAD_STR                 "attr_dict['{attr_name}'].default"
              392  LOAD_ATTR                format

 L.1598       394  LOAD_FAST                'attr_name'

 L.1597       396  LOAD_CONST               ('attr_name',)
              398  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.1595       400  CALL_FUNCTION_2       2  ''

 L.1594       402  CALL_METHOD_1         1  ''
              404  POP_TOP          

 L.1602       406  LOAD_GLOBAL              _init_converter_pat
              408  LOAD_METHOD              format
              410  LOAD_FAST                'a'
              412  LOAD_ATTR                name
              414  CALL_METHOD_1         1  ''
              416  STORE_FAST               'conv_name'

 L.1603       418  LOAD_FAST                'a'
              420  LOAD_ATTR                converter
              422  LOAD_FAST                'names_for_globals'
              424  LOAD_FAST                'conv_name'
              426  STORE_SUBSCR     
              428  JUMP_FORWARD        926  'to 926'
            430_0  COME_FROM           378  '378'

 L.1605       430  LOAD_FAST                'lines'
              432  LOAD_METHOD              append

 L.1606       434  LOAD_FAST                'fmt_setter'

 L.1607       436  LOAD_FAST                'attr_name'

 L.1608       438  LOAD_STR                 "attr_dict['{attr_name}'].default"
              440  LOAD_ATTR                format

 L.1609       442  LOAD_FAST                'attr_name'

 L.1608       444  LOAD_CONST               ('attr_name',)
              446  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.1606       448  CALL_FUNCTION_2       2  ''

 L.1605       450  CALL_METHOD_1         1  ''
              452  POP_TOP          
          454_456  JUMP_FORWARD        926  'to 926'
            458_0  COME_FROM           246  '246'

 L.1613       458  LOAD_FAST                'a'
              460  LOAD_ATTR                default
              462  LOAD_GLOBAL              NOTHING
              464  COMPARE_OP               is-not
          466_468  POP_JUMP_IF_FALSE   588  'to 588'
              470  LOAD_FAST                'has_factory'
          472_474  POP_JUMP_IF_TRUE    588  'to 588'

 L.1614       476  LOAD_STR                 "{arg_name}=attr_dict['{attr_name}'].default"
              478  LOAD_ATTR                format

 L.1615       480  LOAD_FAST                'arg_name'

 L.1615       482  LOAD_FAST                'attr_name'

 L.1614       484  LOAD_CONST               ('arg_name', 'attr_name')
              486  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              488  STORE_FAST               'arg'

 L.1617       490  LOAD_FAST                'a'
              492  LOAD_ATTR                kw_only
          494_496  POP_JUMP_IF_FALSE   510  'to 510'

 L.1618       498  LOAD_FAST                'kw_only_args'
              500  LOAD_METHOD              append
              502  LOAD_FAST                'arg'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
              508  JUMP_FORWARD        520  'to 520'
            510_0  COME_FROM           494  '494'

 L.1620       510  LOAD_FAST                'args'
              512  LOAD_METHOD              append
              514  LOAD_FAST                'arg'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          
            520_0  COME_FROM           508  '508'

 L.1621       520  LOAD_FAST                'a'
              522  LOAD_ATTR                converter
              524  LOAD_CONST               None
              526  COMPARE_OP               is-not
          528_530  POP_JUMP_IF_FALSE   568  'to 568'

 L.1622       532  LOAD_FAST                'lines'
              534  LOAD_METHOD              append
              536  LOAD_FAST                'fmt_setter_with_converter'
              538  LOAD_FAST                'attr_name'
              540  LOAD_FAST                'arg_name'
              542  CALL_FUNCTION_2       2  ''
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          

 L.1625       548  LOAD_FAST                'a'
              550  LOAD_ATTR                converter

 L.1623       552  LOAD_FAST                'names_for_globals'

 L.1624       554  LOAD_GLOBAL              _init_converter_pat
              556  LOAD_METHOD              format
              558  LOAD_FAST                'a'
              560  LOAD_ATTR                name
              562  CALL_METHOD_1         1  ''

 L.1623       564  STORE_SUBSCR     
              566  JUMP_FORWARD        926  'to 926'
            568_0  COME_FROM           528  '528'

 L.1627       568  LOAD_FAST                'lines'
              570  LOAD_METHOD              append
              572  LOAD_FAST                'fmt_setter'
              574  LOAD_FAST                'attr_name'
              576  LOAD_FAST                'arg_name'
              578  CALL_FUNCTION_2       2  ''
              580  CALL_METHOD_1         1  ''
              582  POP_TOP          
          584_586  JUMP_FORWARD        926  'to 926'
            588_0  COME_FROM           472  '472'
            588_1  COME_FROM           466  '466'

 L.1628       588  LOAD_FAST                'has_factory'
          590_592  POP_JUMP_IF_FALSE   832  'to 832'

 L.1629       594  LOAD_STR                 '{arg_name}=NOTHING'
              596  LOAD_ATTR                format
              598  LOAD_FAST                'arg_name'
              600  LOAD_CONST               ('arg_name',)
              602  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              604  STORE_FAST               'arg'

 L.1630       606  LOAD_FAST                'a'
              608  LOAD_ATTR                kw_only
          610_612  POP_JUMP_IF_FALSE   626  'to 626'

 L.1631       614  LOAD_FAST                'kw_only_args'
              616  LOAD_METHOD              append
              618  LOAD_FAST                'arg'
              620  CALL_METHOD_1         1  ''
              622  POP_TOP          
              624  JUMP_FORWARD        636  'to 636'
            626_0  COME_FROM           610  '610'

 L.1633       626  LOAD_FAST                'args'
              628  LOAD_METHOD              append
              630  LOAD_FAST                'arg'
              632  CALL_METHOD_1         1  ''
              634  POP_TOP          
            636_0  COME_FROM           624  '624'

 L.1634       636  LOAD_FAST                'lines'
              638  LOAD_METHOD              append

 L.1635       640  LOAD_STR                 'if {arg_name} is not NOTHING:'
              642  LOAD_ATTR                format
              644  LOAD_FAST                'arg_name'
              646  LOAD_CONST               ('arg_name',)
              648  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.1634       650  CALL_METHOD_1         1  ''
              652  POP_TOP          

 L.1637       654  LOAD_GLOBAL              _init_factory_pat
              656  LOAD_METHOD              format
              658  LOAD_FAST                'a'
              660  LOAD_ATTR                name
              662  CALL_METHOD_1         1  ''
              664  STORE_FAST               'init_factory_name'

 L.1638       666  LOAD_FAST                'a'
              668  LOAD_ATTR                converter
              670  LOAD_CONST               None
              672  COMPARE_OP               is-not
          674_676  POP_JUMP_IF_FALSE   758  'to 758'

 L.1639       678  LOAD_FAST                'lines'
              680  LOAD_METHOD              append

 L.1640       682  LOAD_STR                 '    '
              684  LOAD_FAST                'fmt_setter_with_converter'
              686  LOAD_FAST                'attr_name'
              688  LOAD_FAST                'arg_name'
              690  CALL_FUNCTION_2       2  ''
              692  BINARY_ADD       

 L.1639       694  CALL_METHOD_1         1  ''
              696  POP_TOP          

 L.1642       698  LOAD_FAST                'lines'
              700  LOAD_METHOD              append
              702  LOAD_STR                 'else:'
              704  CALL_METHOD_1         1  ''
              706  POP_TOP          

 L.1643       708  LOAD_FAST                'lines'
              710  LOAD_METHOD              append

 L.1644       712  LOAD_STR                 '    '

 L.1645       714  LOAD_FAST                'fmt_setter_with_converter'

 L.1646       716  LOAD_FAST                'attr_name'

 L.1647       718  LOAD_FAST                'init_factory_name'
              720  LOAD_STR                 '({0})'
              722  LOAD_METHOD              format
              724  LOAD_FAST                'maybe_self'
              726  CALL_METHOD_1         1  ''
              728  BINARY_ADD       

 L.1645       730  CALL_FUNCTION_2       2  ''

 L.1644       732  BINARY_ADD       

 L.1643       734  CALL_METHOD_1         1  ''
              736  POP_TOP          

 L.1652       738  LOAD_FAST                'a'
              740  LOAD_ATTR                converter

 L.1650       742  LOAD_FAST                'names_for_globals'

 L.1651       744  LOAD_GLOBAL              _init_converter_pat
              746  LOAD_METHOD              format
              748  LOAD_FAST                'a'
              750  LOAD_ATTR                name
              752  CALL_METHOD_1         1  ''

 L.1650       754  STORE_SUBSCR     
              756  JUMP_FORWARD        818  'to 818'
            758_0  COME_FROM           674  '674'

 L.1654       758  LOAD_FAST                'lines'
              760  LOAD_METHOD              append
              762  LOAD_STR                 '    '
              764  LOAD_FAST                'fmt_setter'
              766  LOAD_FAST                'attr_name'
              768  LOAD_FAST                'arg_name'
              770  CALL_FUNCTION_2       2  ''
              772  BINARY_ADD       
              774  CALL_METHOD_1         1  ''
              776  POP_TOP          

 L.1655       778  LOAD_FAST                'lines'
              780  LOAD_METHOD              append
              782  LOAD_STR                 'else:'
              784  CALL_METHOD_1         1  ''
              786  POP_TOP          

 L.1656       788  LOAD_FAST                'lines'
              790  LOAD_METHOD              append

 L.1657       792  LOAD_STR                 '    '

 L.1658       794  LOAD_FAST                'fmt_setter'

 L.1659       796  LOAD_FAST                'attr_name'

 L.1660       798  LOAD_FAST                'init_factory_name'
              800  LOAD_STR                 '({0})'
              802  LOAD_METHOD              format
              804  LOAD_FAST                'maybe_self'
              806  CALL_METHOD_1         1  ''
              808  BINARY_ADD       

 L.1658       810  CALL_FUNCTION_2       2  ''

 L.1657       812  BINARY_ADD       

 L.1656       814  CALL_METHOD_1         1  ''
              816  POP_TOP          
            818_0  COME_FROM           756  '756'

 L.1663       818  LOAD_FAST                'a'
              820  LOAD_ATTR                default
              822  LOAD_ATTR                factory
              824  LOAD_FAST                'names_for_globals'
              826  LOAD_FAST                'init_factory_name'
              828  STORE_SUBSCR     
              830  JUMP_FORWARD        926  'to 926'
            832_0  COME_FROM           590  '590'

 L.1665       832  LOAD_FAST                'a'
              834  LOAD_ATTR                kw_only
          836_838  POP_JUMP_IF_FALSE   852  'to 852'

 L.1666       840  LOAD_FAST                'kw_only_args'
              842  LOAD_METHOD              append
              844  LOAD_FAST                'arg_name'
              846  CALL_METHOD_1         1  ''
              848  POP_TOP          
              850  JUMP_FORWARD        862  'to 862'
            852_0  COME_FROM           836  '836'

 L.1668       852  LOAD_FAST                'args'
              854  LOAD_METHOD              append
              856  LOAD_FAST                'arg_name'
              858  CALL_METHOD_1         1  ''
              860  POP_TOP          
            862_0  COME_FROM           850  '850'

 L.1669       862  LOAD_FAST                'a'
              864  LOAD_ATTR                converter
              866  LOAD_CONST               None
              868  COMPARE_OP               is-not
          870_872  POP_JUMP_IF_FALSE   910  'to 910'

 L.1670       874  LOAD_FAST                'lines'
              876  LOAD_METHOD              append
              878  LOAD_FAST                'fmt_setter_with_converter'
              880  LOAD_FAST                'attr_name'
              882  LOAD_FAST                'arg_name'
              884  CALL_FUNCTION_2       2  ''
              886  CALL_METHOD_1         1  ''
              888  POP_TOP          

 L.1673       890  LOAD_FAST                'a'
              892  LOAD_ATTR                converter

 L.1671       894  LOAD_FAST                'names_for_globals'

 L.1672       896  LOAD_GLOBAL              _init_converter_pat
            898_0  COME_FROM           428  '428'
              898  LOAD_METHOD              format
              900  LOAD_FAST                'a'
              902  LOAD_ATTR                name
              904  CALL_METHOD_1         1  ''
            906_0  COME_FROM           566  '566'

 L.1671       906  STORE_SUBSCR     
              908  JUMP_FORWARD        926  'to 926'
            910_0  COME_FROM           870  '870'

 L.1675       910  LOAD_FAST                'lines'
              912  LOAD_METHOD              append
              914  LOAD_FAST                'fmt_setter'
              916  LOAD_FAST                'attr_name'
              918  LOAD_FAST                'arg_name'
              920  CALL_FUNCTION_2       2  ''
              922  CALL_METHOD_1         1  ''
              924  POP_TOP          
            926_0  COME_FROM           908  '908'
            926_1  COME_FROM           830  '830'
            926_2  COME_FROM           584  '584'
            926_3  COME_FROM           454  '454'

 L.1677       926  LOAD_FAST                'a'
              928  LOAD_ATTR                init
              930  LOAD_CONST               True
              932  COMPARE_OP               is
              934  POP_JUMP_IF_FALSE   164  'to 164'
              936  LOAD_FAST                'a'
              938  LOAD_ATTR                converter
              940  LOAD_CONST               None
              942  COMPARE_OP               is
              944  POP_JUMP_IF_FALSE   164  'to 164'
              946  LOAD_FAST                'a'
              948  LOAD_ATTR                type
              950  LOAD_CONST               None
              952  COMPARE_OP               is-not
              954  POP_JUMP_IF_FALSE   164  'to 164'

 L.1678       956  LOAD_FAST                'a'
              958  LOAD_ATTR                type
              960  LOAD_FAST                'annotations'
              962  LOAD_FAST                'arg_name'
              964  STORE_SUBSCR     
              966  JUMP_BACK           164  'to 164'

 L.1680       968  LOAD_FAST                'attrs_to_validate'
          970_972  POP_JUMP_IF_FALSE  1068  'to 1068'

 L.1681       974  LOAD_GLOBAL              _config
              976  LOAD_FAST                'names_for_globals'
              978  LOAD_STR                 '_config'
              980  STORE_SUBSCR     

 L.1682       982  LOAD_FAST                'lines'
              984  LOAD_METHOD              append
              986  LOAD_STR                 'if _config._run_validators is True:'
              988  CALL_METHOD_1         1  ''
              990  POP_TOP          

 L.1683       992  LOAD_FAST                'attrs_to_validate'
              994  GET_ITER         
              996  FOR_ITER           1068  'to 1068'
              998  STORE_FAST               'a'

 L.1684      1000  LOAD_STR                 '__attr_validator_{}'
             1002  LOAD_METHOD              format
             1004  LOAD_FAST                'a'
             1006  LOAD_ATTR                name
             1008  CALL_METHOD_1         1  ''
             1010  STORE_FAST               'val_name'

 L.1685      1012  LOAD_STR                 '__attr_{}'
             1014  LOAD_METHOD              format
             1016  LOAD_FAST                'a'
             1018  LOAD_ATTR                name
             1020  CALL_METHOD_1         1  ''
             1022  STORE_FAST               'attr_name'

 L.1686      1024  LOAD_FAST                'lines'
             1026  LOAD_METHOD              append

 L.1687      1028  LOAD_STR                 '    {}(self, {}, self.{})'
             1030  LOAD_METHOD              format
             1032  LOAD_FAST                'val_name'
             1034  LOAD_FAST                'attr_name'
             1036  LOAD_FAST                'a'
             1038  LOAD_ATTR                name
             1040  CALL_METHOD_3         3  ''

 L.1686      1042  CALL_METHOD_1         1  ''
             1044  POP_TOP          

 L.1689      1046  LOAD_FAST                'a'
             1048  LOAD_ATTR                validator
             1050  LOAD_FAST                'names_for_globals'
             1052  LOAD_FAST                'val_name'
             1054  STORE_SUBSCR     

 L.1690      1056  LOAD_FAST                'a'
             1058  LOAD_FAST                'names_for_globals'
             1060  LOAD_FAST                'attr_name'
             1062  STORE_SUBSCR     
         1064_1066  JUMP_BACK           996  'to 996'
           1068_0  COME_FROM           970  '970'

 L.1691      1068  LOAD_FAST                'post_init'
         1070_1072  POP_JUMP_IF_FALSE  1084  'to 1084'

 L.1692      1074  LOAD_FAST                'lines'
             1076  LOAD_METHOD              append
             1078  LOAD_STR                 'self.__attrs_post_init__()'
             1080  CALL_METHOD_1         1  ''
             1082  POP_TOP          
           1084_0  COME_FROM          1070  '1070'

 L.1699      1084  LOAD_FAST                'cache_hash'
         1086_1088  POP_JUMP_IF_FALSE  1136  'to 1136'

 L.1700      1090  LOAD_FAST                'frozen'
         1092_1094  POP_JUMP_IF_FALSE  1114  'to 1114'

 L.1701      1096  LOAD_FAST                'slots'
         1098_1100  POP_JUMP_IF_FALSE  1108  'to 1108'

 L.1703      1102  LOAD_STR                 "_setattr('%s', %s)"
             1104  STORE_FAST               'init_hash_cache'
             1106  JUMP_FORWARD       1112  'to 1112'
           1108_0  COME_FROM          1098  '1098'

 L.1706      1108  LOAD_STR                 "_inst_dict['%s'] = %s"
             1110  STORE_FAST               'init_hash_cache'
           1112_0  COME_FROM          1106  '1106'
             1112  JUMP_FORWARD       1118  'to 1118'
           1114_0  COME_FROM          1092  '1092'

 L.1708      1114  LOAD_STR                 'self.%s = %s'
             1116  STORE_FAST               'init_hash_cache'
           1118_0  COME_FROM          1112  '1112'

 L.1709      1118  LOAD_FAST                'lines'
             1120  LOAD_METHOD              append
             1122  LOAD_FAST                'init_hash_cache'
             1124  LOAD_GLOBAL              _hash_cache_field
             1126  LOAD_STR                 'None'
             1128  BUILD_TUPLE_2         2 
             1130  BINARY_MODULO    
             1132  CALL_METHOD_1         1  ''
             1134  POP_TOP          
           1136_0  COME_FROM          1086  '1086'

 L.1713      1136  LOAD_FAST                'is_exc'
         1138_1140  POP_JUMP_IF_FALSE  1178  'to 1178'

 L.1714      1142  LOAD_STR                 ','
             1144  LOAD_METHOD              join
             1146  LOAD_GENEXPR             '<code_object <genexpr>>'
             1148  LOAD_STR                 '_attrs_to_init_script.<locals>.<genexpr>'
             1150  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1152  LOAD_FAST                'attrs'
             1154  GET_ITER         
             1156  CALL_FUNCTION_1       1  ''
             1158  CALL_METHOD_1         1  ''
             1160  STORE_FAST               'vals'

 L.1716      1162  LOAD_FAST                'lines'
             1164  LOAD_METHOD              append
             1166  LOAD_STR                 'BaseException.__init__(self, %s)'
             1168  LOAD_FAST                'vals'
             1170  BUILD_TUPLE_1         1 
             1172  BINARY_MODULO    
             1174  CALL_METHOD_1         1  ''
             1176  POP_TOP          
           1178_0  COME_FROM          1138  '1138'

 L.1718      1178  LOAD_STR                 ', '
             1180  LOAD_METHOD              join
             1182  LOAD_FAST                'args'
             1184  CALL_METHOD_1         1  ''
             1186  STORE_FAST               'args'

 L.1719      1188  LOAD_FAST                'kw_only_args'
         1190_1192  POP_JUMP_IF_FALSE  1242  'to 1242'

 L.1720      1194  LOAD_GLOBAL              PY2
         1196_1198  POP_JUMP_IF_FALSE  1208  'to 1208'

 L.1721      1200  LOAD_GLOBAL              PythonTooOldError

 L.1722      1202  LOAD_STR                 'Keyword-only arguments only work on Python 3 and later.'

 L.1721      1204  CALL_FUNCTION_1       1  ''
             1206  RAISE_VARARGS_1       1  'exception instance'
           1208_0  COME_FROM          1196  '1196'

 L.1725      1208  LOAD_FAST                'args'
             1210  LOAD_STR                 '{leading_comma}*, {kw_only_args}'
             1212  LOAD_ATTR                format

 L.1726      1214  LOAD_FAST                'args'
         1216_1218  POP_JUMP_IF_FALSE  1224  'to 1224'
             1220  LOAD_STR                 ', '
             1222  JUMP_FORWARD       1226  'to 1226'
           1224_0  COME_FROM          1216  '1216'
             1224  LOAD_STR                 ''
           1226_0  COME_FROM          1222  '1222'

 L.1727      1226  LOAD_STR                 ', '
             1228  LOAD_METHOD              join
             1230  LOAD_FAST                'kw_only_args'
             1232  CALL_METHOD_1         1  ''

 L.1725      1234  LOAD_CONST               ('leading_comma', 'kw_only_args')
             1236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1238  INPLACE_ADD      
             1240  STORE_FAST               'args'
           1242_0  COME_FROM          1190  '1190'

 L.1730      1242  LOAD_STR                 'def __init__(self, {args}):\n    {lines}\n'
             1244  LOAD_ATTR                format

 L.1734      1246  LOAD_FAST                'args'

 L.1734      1248  LOAD_FAST                'lines'
         1250_1252  POP_JUMP_IF_FALSE  1264  'to 1264'
             1254  LOAD_STR                 '\n    '
             1256  LOAD_METHOD              join
             1258  LOAD_FAST                'lines'
             1260  CALL_METHOD_1         1  ''
             1262  JUMP_FORWARD       1266  'to 1266'
           1264_0  COME_FROM          1250  '1250'
             1264  LOAD_STR                 'pass'
           1266_0  COME_FROM          1262  '1262'

 L.1730      1266  LOAD_CONST               ('args', 'lines')
             1268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.1736      1270  LOAD_FAST                'names_for_globals'

 L.1737      1272  LOAD_FAST                'annotations'

 L.1729      1274  BUILD_TUPLE_3         3 
             1276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 898_0


class Attribute(object):
    __doc__ = '\n    *Read-only* representation of an attribute.\n\n    :attribute name: The name of the attribute.\n\n    Plus *all* arguments of `attr.ib` (except for ``factory``\n    which is only syntactic sugar for ``default=Factory(...)``.\n\n    For the version history of the fields, see `attr.ib`.\n    '
    __slots__ = ('name', 'default', 'validator', 'repr', 'eq', 'order', 'hash', 'init',
                 'metadata', 'type', 'converter', 'kw_only')

    def __init__(self, name, default, validator, repr, cmp, hash, init, metadata=None, type=None, converter=None, kw_only=False, eq=None, order=None):
        eq, order = _determine_eq_order(cmp, eq, order)
        bound_setattr = _obj_setattr.__get__(self, Attribute)
        bound_setattr('name', name)
        bound_setattr('default', default)
        bound_setattr('validator', validator)
        bound_setattr('repr', repr)
        bound_setattr('eq', eq)
        bound_setattr('order', order)
        bound_setattr('hash', hash)
        bound_setattr('init', init)
        bound_setattr('converter', converter)
        bound_setattr('metadata', metadata_proxy(metadata) if metadata else _empty_metadata_singleton)
        bound_setattr('type', type)
        bound_setattr('kw_only', kw_only)

    def __setattr__(self, name, value):
        raise FrozenInstanceError()

    @classmethod
    def from_counting_attr--- This code section failed: ---

 L.1817         0  LOAD_FAST                'type'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.1818         8  LOAD_DEREF               'ca'
               10  LOAD_ATTR                type
               12  STORE_FAST               'type'
               14  JUMP_FORWARD         34  'to 34'
             16_0  COME_FROM             6  '6'

 L.1819        16  LOAD_DEREF               'ca'
               18  LOAD_ATTR                type
               20  LOAD_CONST               None
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L.1820        26  LOAD_GLOBAL              ValueError

 L.1821        28  LOAD_STR                 'Type annotation and type argument cannot both be present'

 L.1820        30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            14  '14'

 L.1823        34  LOAD_CLOSURE             'ca'
               36  BUILD_TUPLE_1         1 
               38  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               40  LOAD_STR                 'Attribute.from_counting_attr.<locals>.<dictcomp>'
               42  MAKE_FUNCTION_8          'closure'

 L.1825        44  LOAD_GLOBAL              Attribute
               46  LOAD_ATTR                __slots__

 L.1823        48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'inst_dict'

 L.1834        54  LOAD_FAST                'cls'
               56  BUILD_TUPLE_0         0 

 L.1835        58  LOAD_FAST                'name'

 L.1836        60  LOAD_DEREF               'ca'
               62  LOAD_ATTR                _validator

 L.1837        64  LOAD_DEREF               'ca'
               66  LOAD_ATTR                _default

 L.1838        68  LOAD_FAST                'type'

 L.1839        70  LOAD_CONST               None

 L.1834        72  LOAD_CONST               ('name', 'validator', 'default', 'type', 'cmp')
               74  BUILD_CONST_KEY_MAP_5     5 

 L.1840        76  LOAD_FAST                'inst_dict'

 L.1834        78  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               80  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 38

    @property
    def cmp(self):
        """
        Simulate the presence of a cmp attribute and warn.
        """
        warnings.warn(_CMP_DEPRECATION, DeprecationWarning, stacklevel=2)
        return self.eq and self.order

    def _assoc(self, **changes):
        """
        Copy *self* and apply *changes*.
        """
        new = copy.copy(self)
        new._setattrs(changes.items())
        return new

    def __getstate__(self):
        """
        Play nice with pickle.
        """
        return tuple(((getattr(self, name) if name != 'metadata' else dict(self.metadata)) for name in self.__slots__))

    def __setstate__(self, state):
        """
        Play nice with pickle.
        """
        self._setattrs(zip(self.__slots__, state))

    def _setattrs(self, name_values_pairs):
        bound_setattr = _obj_setattr.__get__(self, Attribute)
        for name, value in name_values_pairs:
            if name != 'metadata':
                bound_setattr(name, value)
            else:
                bound_setattr(name, metadata_proxy(value) if value else _empty_metadata_singleton)


_a = [Attribute(name=name,
  default=NOTHING,
  validator=None,
  repr=True,
  cmp=None,
  eq=True,
  order=False,
  hash=(name != 'metadata'),
  init=True) for name in Attribute.__slots__]
Attribute = _add_hash(_add_eq(_add_repr(Attribute, attrs=_a), attrs=_a),
  attrs=[a for a in _a if a.hash])

class _CountingAttr(object):
    __doc__ = '\n    Intermediate representation of attributes that uses a counter to preserve\n    the order in which the attributes have been defined.\n\n    *Internal* data structure of the attrs library.  Running into is most\n    likely the result of a bug like a forgotten `@attr.s` decorator.\n    '
    __slots__ = ('counter', '_default', 'repr', 'eq', 'order', 'hash', 'init', 'metadata',
                 '_validator', 'converter', 'type', 'kw_only')
    __attrs_attrs__ = tuple((Attribute(name=name,
      default=NOTHING,
      validator=None,
      repr=True,
      cmp=None,
      hash=True,
      init=True,
      kw_only=False,
      eq=True,
      order=False) for name in ('counter', '_default', 'repr', 'eq', 'order', 'hash',
                                'init'))) + (
     Attribute(name='metadata',
       default=None,
       validator=None,
       repr=True,
       cmp=None,
       hash=False,
       init=True,
       kw_only=False,
       eq=True,
       order=False),)
    cls_counter = 0

    def __init__(self, default, validator, repr, cmp, hash, init, converter, metadata, type, kw_only, eq, order):
        _CountingAttr.cls_counter += 1
        self.counter = _CountingAttr.cls_counter
        self._default = default
        if validator and isinstance(validator, (list, tuple)):
            self._validator = and_(*validator)
        else:
            self._validator = validator
        self.repr = repr
        self.eq = eq
        self.order = order
        self.hash = hash
        self.init = init
        self.converter = converter
        self.metadata = metadata
        self.type = type
        self.kw_only = kw_only

    def validator(self, meth):
        """
        Decorator that adds *meth* to the list of validators.

        Returns *meth* unchanged.

        .. versionadded:: 17.1.0
        """
        if self._validator is None:
            self._validator = meth
        else:
            self._validator = and_(self._validator, meth)
        return meth

    def default(self, meth):
        """
        Decorator that allows to set the default for an attribute.

        Returns *meth* unchanged.

        :raises DefaultAlreadySetError: If default has been set before.

        .. versionadded:: 17.1.0
        """
        if self._default is not NOTHING:
            raise DefaultAlreadySetError()
        self._default = Factory(meth, takes_self=True)
        return meth


_CountingAttr = _add_eq(_add_repr(_CountingAttr))

@attrs(slots=True, init=False, hash=True)
class Factory(object):
    __doc__ = '\n    Stores a factory callable.\n\n    If passed as the default value to `attr.ib`, the factory is used to\n    generate a new value.\n\n    :param callable factory: A callable that takes either none or exactly one\n        mandatory positional argument depending on *takes_self*.\n    :param bool takes_self: Pass the partially initialized instance that is\n        being initialized as a positional argument.\n\n    .. versionadded:: 17.1.0  *takes_self*\n    '
    factory = attrib()
    takes_self = attrib()

    def __init__(self, factory, takes_self=False):
        """
        `Factory` is part of the default machinery so if we want a default
        value here, we have to implement it ourselves.
        """
        self.factory = factory
        self.takes_self = takes_self


def make_class(name, attrs, bases=(
 object,), **attributes_arguments):
    """
    A quick way to create a new class called *name* with *attrs*.

    :param name: The name for the new class.
    :type name: str

    :param attrs: A list of names or a dictionary of mappings of names to
        attributes.

        If *attrs* is a list or an ordered dict (`dict` on Python 3.6+,
        `collections.OrderedDict` otherwise), the order is deduced from
        the order of the names or attributes inside *attrs*.  Otherwise the
        order of the definition of the attributes is used.
    :type attrs: `list` or `dict`

    :param tuple bases: Classes that the new class will subclass.

    :param attributes_arguments: Passed unmodified to `attr.s`.

    :return: A new class with *attrs*.
    :rtype: type

    .. versionadded:: 17.1.0 *bases*
    .. versionchanged:: 18.1.0 If *attrs* is ordered, the order is retained.
    """
    if isinstance(attrs, dict):
        cls_dict = attrs
    else:
        if isinstance(attrs, (list, tuple)):
            cls_dict = dict(((a, attrib()) for a in attrs))
        else:
            raise TypeError('attrs argument must be a dict or a list.')
    post_init = cls_dict.pop('__attrs_post_init__', None)
    type_ = type(name, bases, {} if post_init is None else {'__attrs_post_init__': post_init})
    try:
        type_.__module__ = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass
    else:
        cmp = attributes_arguments.pop('cmp', None)
        attributes_arguments['eq'], attributes_arguments['order'] = _determine_eq_order(cmp, attributes_arguments.get('eq'), attributes_arguments.get('order'))
        return _attrs(these=cls_dict, **attributes_arguments)(type_)


@attrs(slots=True, hash=True)
class _AndValidator(object):
    __doc__ = '\n    Compose many validators to a single one.\n    '
    _validators = attrib()

    def __call__(self, inst, attr, value):
        for v in self._validators:
            v(inst, attr, value)


def and_(*validators):
    """
    A validator that composes multiple validators into one.

    When called on a value, it runs all wrapped validators.

    :param validators: Arbitrary number of validators.
    :type validators: callables

    .. versionadded:: 17.1.0
    """
    vals = []
    for validator in validators:
        vals.extend(validator._validators if isinstance(validator, _AndValidator) else [
         validator])
    else:
        return _AndValidator(tuple(vals))