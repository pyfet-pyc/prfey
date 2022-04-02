# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\urllib3\packages\ordered_dict.py
try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident
else:
    try:
        from _abcoll import KeysView, ValuesView, ItemsView
    except ImportError:
        pass
    else:

        class OrderedDict(dict):
            __doc__ = 'Dictionary that remembers insertion order'

            def __init__(self, *args, **kwds):
                """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        """
                if len(args) > 1:
                    raise TypeError('expected at most 1 arguments, got %d' % len(args))
                try:
                    self._OrderedDict__root
                except AttributeError:
                    self._OrderedDict__root = root = []
                    root[:] = [
                     root, root, None]
                    self._OrderedDict__map = {}
                else:
                    (self._OrderedDict__update)(*args, **kwds)

            def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
                """od.__setitem__(i, y) <==> od[i]=y"""
                if key not in self:
                    root = self._OrderedDict__root
                    last = root[0]
                    last[1] = root[0] = self._OrderedDict__map[key] = [last, root, key]
                dict_setitem(self, key, value)

            def __delitem__(self, key, dict_delitem=dict.__delitem__):
                """od.__delitem__(y) <==> del od[y]"""
                dict_delitem(self, key)
                link_prev, link_next, key = self._OrderedDict__map.pop(key)
                link_prev[1] = link_next
                link_next[0] = link_prev

            def __iter__(self):
                """od.__iter__() <==> iter(od)"""
                root = self._OrderedDict__root
                curr = root[1]
                while True:
                    if curr is not root:
                        yield curr[2]
                        curr = curr[1]

            def __reversed__(self):
                """od.__reversed__() <==> reversed(od)"""
                root = self._OrderedDict__root
                curr = root[0]
                while True:
                    if curr is not root:
                        yield curr[2]
                        curr = curr[0]

            def clear(self):
                """od.clear() -> None.  Remove all items from od."""
                try:
                    for node in self._OrderedDict__map.itervalues():
                        del node[:]
                    else:
                        root = self._OrderedDict__root
                        root[:] = [root, root, None]
                        self._OrderedDict__map.clear()

                except AttributeError:
                    pass
                else:
                    dict.clear(self)

            def popitem(self, last=True):
                """od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        """
                if not self:
                    raise KeyError('dictionary is empty')
                root = self._OrderedDict__root
                if last:
                    link = root[0]
                    link_prev = link[0]
                    link_prev[1] = root
                    root[0] = link_prev
                else:
                    link = root[1]
                    link_next = link[1]
                    root[1] = link_next
                    link_next[0] = root
                key = link[2]
                del self._OrderedDict__map[key]
                value = dict.pop(self, key)
                return (
                 key, value)

            def keys(self):
                """od.keys() -> list of keys in od"""
                return list(self)

            def values(self):
                """od.values() -> list of values in od"""
                return [self[key] for key in self]

            def items(self):
                """od.items() -> list of (key, value) pairs in od"""
                return [(
                 key, self[key]) for key in self]

            def iterkeys(self):
                """od.iterkeys() -> an iterator over the keys in od"""
                return iter(self)

            def itervalues(self):
                """od.itervalues -> an iterator over the values in od"""
                for k in self:
                    yield self[k]

            def iteritems(self):
                """od.iteritems -> an iterator over the (key, value) items in od"""
                for k in self:
                    yield (
                     k, self[k])

            def update(*args, **kwds):
                """od.update(E, **F) -> None.  Update od from dict/iterable E and F.

        If E is a dict instance, does:           for k in E: od[k] = E[k]
        If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
        Or if E is an iterable of items, does:   for k, v in E: od[k] = v
        In either case, this is followed by:     for k, v in F.items(): od[k] = v

        """
                if len(args) > 2:
                    raise TypeError('update() takes at most 2 positional arguments (%d given)' % (
                     len(args),))
                elif not args:
                    raise TypeError('update() takes at least 1 argument (0 given)')
                self = args[0]
                other = ()
                if len(args) == 2:
                    other = args[1]
                if isinstance(other, dict):
                    for key in other:
                        self[key] = other[key]

                elif hasattr(other, 'keys'):
                    for key in other.keys():
                        self[key] = other[key]

                else:
                    pass
                for key, value in other:
                    self[key] = value
                else:
                    for key, value in kwds.items():
                        self[key] = value

            _OrderedDict__update = update
            _OrderedDict__marker = object()

            def pop(self, key, default=_OrderedDict__marker):
                """od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.

        """
                if key in self:
                    result = self[key]
                    del self[key]
                    return result
                if default is self._OrderedDict__marker:
                    raise KeyError(key)
                return default

            def setdefault(self, key, default=None):
                """od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od"""
                if key in self:
                    return self[key]
                self[key] = default
                return default

            def __repr__--- This code section failed: ---

 L. 199         0  LOAD_GLOBAL              id
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              _get_ident
                8  CALL_FUNCTION_0       0  ''
               10  BUILD_TUPLE_2         2 
               12  STORE_FAST               'call_key'

 L. 200        14  LOAD_FAST                'call_key'
               16  LOAD_FAST                '_repr_running'
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 201        22  LOAD_STR                 '...'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 202        26  LOAD_CONST               1
               28  LOAD_FAST                '_repr_running'
               30  LOAD_FAST                'call_key'
               32  STORE_SUBSCR     

 L. 203        34  SETUP_FINALLY        82  'to 82'

 L. 204        36  LOAD_FAST                'self'
               38  POP_JUMP_IF_TRUE     58  'to 58'

 L. 205        40  LOAD_STR                 '%s()'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                __class__
               46  LOAD_ATTR                __name__
               48  BUILD_TUPLE_1         1 
               50  BINARY_MODULO    
               52  POP_BLOCK        
               54  CALL_FINALLY         82  'to 82'
               56  RETURN_VALUE     
             58_0  COME_FROM            38  '38'

 L. 206        58  LOAD_STR                 '%s(%r)'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                __class__
               64  LOAD_ATTR                __name__
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              items
               70  CALL_METHOD_0         0  ''
               72  BUILD_TUPLE_2         2 
               74  BINARY_MODULO    
               76  POP_BLOCK        
               78  CALL_FINALLY         82  'to 82'
               80  RETURN_VALUE     
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            54  '54'
             82_2  COME_FROM_FINALLY    34  '34'

 L. 208        82  LOAD_FAST                '_repr_running'
               84  LOAD_FAST                'call_key'
               86  DELETE_SUBSCR    
               88  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 58

            def __reduce__(self):
                """Return state information for pickling"""
                items = [[
                 k, self[k]] for k in self]
                inst_dict = vars(self).copy()
                for k in vars(OrderedDict()):
                    inst_dict.pop(k, None)
                else:
                    if inst_dict:
                        return (self.__class__, (items,), inst_dict)
                    return (self.__class__, (items,))

            def copy(self):
                """od.copy() -> a shallow copy of od"""
                return self.__class__(self)

            @classmethod
            def fromkeys(cls, iterable, value=None):
                """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        """
                d = cls()
                for key in iterable:
                    d[key] = value
                else:
                    return d

            def __eq__(self, other):
                """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        """
                if isinstance(other, OrderedDict):
                    return len(self) == len(other) and self.items() == other.items()
                return dict.__eq__(self, other)

            def __ne__(self, other):
                return not self == other

            def viewkeys(self):
                """od.viewkeys() -> a set-like object providing a view on od's keys"""
                return KeysView(self)

            def viewvalues(self):
                """od.viewvalues() -> an object providing a view on od's values"""
                return ValuesView(self)

            def viewitems(self):
                """od.viewitems() -> a set-like object providing a view on od's items"""
                return ItemsView(self)