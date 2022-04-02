# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\multidict\_multidict_py.py
import sys
from array import array
from collections import abc
from ._abc import MultiMapping, MutableMultiMapping
_marker = object()

class istr(str):
    __doc__ = 'Case insensitive str.'
    __is_istr__ = True


upstr = istr

def getversion(md):
    if not isinstance(md, _Base):
        raise TypeError('Parameter should be multidict or proxy')
    return md._impl._version


_version = array('Q', [0])

class _Impl:
    __slots__ = ('_items', '_version')

    def __init__(self):
        self._items = []
        self.incr_version()

    def incr_version(self):
        global _version
        v = _version
        v[0] += 1
        self._version = v[0]

    if sys.implementation.name != 'pypy':

        def __sizeof__(self):
            return object.__sizeof__(self) + sys.getsizeof(self._items)


class _Base:

    def _title(self, key):
        return key

    def getall(self, key, default=_marker):
        """Return a list of all values matching the key."""
        identity = self._title(key)
        res = [v for i, k, v in self._impl._items if i == identity]
        if res:
            return res
        if not res:
            if default is not _marker:
                return default
        raise KeyError('Key not found: %r' % key)

    def getone(self, key, default=_marker):
        """Get first value matching the key."""
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return v
        else:
            if default is not _marker:
                return default
            raise KeyError('Key not found: %r' % key)

    def __getitem__(self, key):
        return self.getone(key)

    def get(self, key, default=None):
        """Get first value matching the key.

        The method is alias for .getone().
        """
        return self.getone(key, default)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._impl._items)

    def keys(self):
        """Return a new view of the dictionary's keys."""
        return _KeysView(self._impl)

    def items(self):
        """Return a new view of the dictionary's items *(key, value) pairs)."""
        return _ItemsView(self._impl)

    def values(self):
        """Return a new view of the dictionary's values."""
        return _ValuesView(self._impl)

    def __eq__(self, other):
        if not isinstance(other, abc.Mapping):
            return NotImplemented
        if isinstance(other, _Base):
            lft = self._impl._items
            rht = other._impl._items
            if len(lft) != len(rht):
                return False
            for (i1, k2, v1), (i2, k2, v2) in zip(lft, rht):
                if not i1 != i2:
                    if v1 != v2:
                        pass
                return False
            else:
                return True

        if len(self._impl._items) != len(other):
            return False
        for k, v in self.items():
            nv = other.get(k, _marker)
            if v != nv:
                return False
        else:
            return True

    def __contains__(self, key):
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return True
        else:
            return False

    def __repr__(self):
        body = ', '.join(("'{}': {!r}".format(k, v) for k, v in self.items()))
        return '<{}({})>'.format(self.__class__.__name__, body)


class MultiDictProxy(_Base, MultiMapping):
    __doc__ = 'Read-only proxy for MultiDict instance.'

    def __init__(self, arg):
        if not isinstance(arg, (MultiDict, MultiDictProxy)):
            raise TypeError('ctor requires MultiDict or MultiDictProxy instance, not {}'.format(type(arg)))
        self._impl = arg._impl

    def __reduce__(self):
        raise TypeError("can't pickle {} objects".format(self.__class__.__name__))

    def copy(self):
        """Return a copy of itself."""
        return MultiDict(self.items())


class CIMultiDictProxy(MultiDictProxy):
    __doc__ = 'Read-only proxy for CIMultiDict instance.'

    def __init__(self, arg):
        if not isinstance(arg, (CIMultiDict, CIMultiDictProxy)):
            raise TypeError('ctor requires CIMultiDict or CIMultiDictProxy instance, not {}'.format(type(arg)))
        self._impl = arg._impl

    def _title(self, key):
        return key.title()

    def copy(self):
        """Return a copy of itself."""
        return CIMultiDict(self.items())


class MultiDict(_Base, MutableMultiMapping):
    __doc__ = 'Dictionary with the support for duplicate keys.'

    def __init__(self, *args, **kwargs):
        self._impl = _Impl()
        self._extend(args, kwargs, self.__class__.__name__, self._extend_items)

    if sys.implementation.name != 'pypy':

        def __sizeof__(self):
            return object.__sizeof__(self) + sys.getsizeof(self._impl)

    def __reduce__(self):
        return (
         self.__class__, (list(self.items()),))

    def _title(self, key):
        return key

    def _key(self, key):
        if isinstance(key, str):
            return key
        raise TypeError('MultiDict keys should be either str or subclasses of str')

    def add(self, key, value):
        identity = self._title(key)
        self._impl._items.append((identity, self._key(key), value))
        self._impl.incr_version()

    def copy(self):
        """Return a copy of itself."""
        cls = self.__class__
        return cls(self.items())

    __copy__ = copy

    def extend(self, *args, **kwargs):
        """Extend current MultiDict with more values.

        This method must be used instead of update.
        """
        self._extend(args, kwargs, 'extend', self._extend_items)

    def _extend(self, args, kwargs, name, method):
        if len(args) > 1:
            raise TypeError('{} takes at most 1 positional argument ({} given)'.format(name, len(args)))
        if args:
            arg = args[0]
            if isinstance(args[0], (MultiDict, MultiDictProxy)) and not kwargs:
                items = arg._impl._items
            else:
                if hasattr(arg, 'items'):
                    arg = arg.items()
                if kwargs:
                    arg = list(arg)
                    arg.extend(list(kwargs.items()))
                items = []
                for item in arg:
                    if not len(item) == 2:
                        raise TypeError('{} takes either dict or list of (key, value) tuples'.format(name))
                    else:
                        items.append((self._title(item[0]), self._key(item[0]), item[1]))
                else:
                    method(items)

        else:
            method([(
             self._title(key), self._key(key), value) for key, value in kwargs.items()])

    def _extend_items(self, items):
        for identity, key, value in items:
            self.add(key, value)

    def clear(self):
        """Remove all items from MultiDict."""
        self._impl._items.clear()
        self._impl.incr_version()

    def __setitem__(self, key, value):
        self._replace(key, value)

    def __delitem__(self, key):
        identity = self._title(key)
        items = self._impl._items
        found = False
        for i in range(len(items) - 1, -1, -1):
            if items[i][0] == identity:
                del items[i]
                found = True
        else:
            if not found:
                raise KeyError(key)
            else:
                self._impl.incr_version()

    def setdefault(self, key, default=None):
        """Return value for key, set value to default if key is not present."""
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return v
        else:
            self.add(key, default)
            return default

    def popone(self, key, default=_marker):
        """Remove specified key and return the corresponding value.

        If key is not found, d is returned if given, otherwise
        KeyError is raised.

        """
        identity = self._title(key)
        for i in range(len(self._impl._items)):
            if self._impl._items[i][0] == identity:
                value = self._impl._items[i][2]
                del self._impl._items[i]
                self._impl.incr_version()
                return value
        else:
            if default is _marker:
                raise KeyError(key)
            else:
                return default

    pop = popone

    def popall(self, key, default=_marker):
        """Remove all occurrences of key and return the list of corresponding
        values.

        If key is not found, default is returned if given, otherwise
        KeyError is raised.

        """
        found = False
        identity = self._title(key)
        ret = []
        for i in range(len(self._impl._items) - 1, -1, -1):
            item = self._impl._items[i]
            if item[0] == identity:
                ret.append(item[2])
                del self._impl._items[i]
                self._impl.incr_version()
                found = True
        else:
            if not found:
                if default is _marker:
                    raise KeyError(key)
                else:
                    return default
            else:
                ret.reverse()
                return ret

    def popitem(self):
        """Remove and return an arbitrary (key, value) pair."""
        if self._impl._items:
            i = self._impl._items.pop(0)
            self._impl.incr_version()
            return (
             i[1], i[2])
        raise KeyError('empty multidict')

    def update(self, *args, **kwargs):
        """Update the dictionary from *other*, overwriting existing keys."""
        self._extend(args, kwargs, 'update', self._update_items)

    def _update_items(self, items):
        if not items:
            return
        used_keys = {}
        for identity, key, value in items:
            start = used_keys.get(identity, 0)
            for i in range(start, len(self._impl._items)):
                item = self._impl._items[i]
                if item[0] == identity:
                    used_keys[identity] = i + 1
                    self._impl._items[i] = (identity, key, value)
                    break
            else:
                self._impl._items.append((identity, key, value))
                used_keys[identity] = len(self._impl._items)

        else:
            i = 0
            while True:
                if i < len(self._impl._items):
                    item = self._impl._items[i]
                    identity = item[0]
                    pos = used_keys.get(identity)
                    if pos is None:
                        i += 1
                    else:
                        if i >= pos:
                            del self._impl._items[i]
                        else:
                            i += 1

            self._impl.incr_version()

    def _replace--- This code section failed: ---

 L. 382         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _key
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'key'

 L. 383        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _title
               14  LOAD_FAST                'key'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'identity'

 L. 384        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _impl
               24  LOAD_ATTR                _items
               26  STORE_FAST               'items'

 L. 386        28  LOAD_GLOBAL              range
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'items'
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
             40_0  COME_FROM            96  '96'
             40_1  COME_FROM            62  '62'
               40  FOR_ITER             98  'to 98'
               42  STORE_FAST               'i'

 L. 387        44  LOAD_FAST                'items'
               46  LOAD_FAST                'i'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'item'

 L. 388        52  LOAD_FAST                'item'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'identity'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L. 389        64  LOAD_FAST                'identity'
               66  LOAD_FAST                'key'
               68  LOAD_FAST                'value'
               70  BUILD_TUPLE_3         3 
               72  LOAD_FAST                'items'
               74  LOAD_FAST                'i'
               76  STORE_SUBSCR     

 L. 391        78  LOAD_FAST                'i'
               80  STORE_FAST               'rgt'

 L. 392        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _impl
               86  LOAD_METHOD              incr_version
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          

 L. 393        92  POP_TOP          
               94  BREAK_LOOP          132  'to 132'
               96  JUMP_BACK            40  'to 40'
             98_0  COME_FROM            40  '40'

 L. 395        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _impl
              102  LOAD_ATTR                _items
              104  LOAD_METHOD              append
              106  LOAD_FAST                'identity'
              108  LOAD_FAST                'key'
              110  LOAD_FAST                'value'
              112  BUILD_TUPLE_3         3 
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 396       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _impl
              122  LOAD_METHOD              incr_version
              124  CALL_METHOD_0         0  ''
              126  POP_TOP          

 L. 397       128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM            94  '94'

 L. 400       132  LOAD_FAST                'rgt'
              134  LOAD_CONST               1
              136  BINARY_ADD       
              138  STORE_FAST               'i'
            140_0  COME_FROM           188  '188'
            140_1  COME_FROM           178  '178'

 L. 401       140  LOAD_FAST                'i'
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'items'
              146  CALL_FUNCTION_1       1  ''
              148  COMPARE_OP               <
              150  POP_JUMP_IF_FALSE   190  'to 190'

 L. 402       152  LOAD_FAST                'items'
              154  LOAD_FAST                'i'
              156  BINARY_SUBSCR    
              158  STORE_FAST               'item'

 L. 403       160  LOAD_FAST                'item'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_FAST                'identity'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   180  'to 180'

 L. 404       172  LOAD_FAST                'items'
              174  LOAD_FAST                'i'
              176  DELETE_SUBSCR    
              178  JUMP_BACK           140  'to 140'
            180_0  COME_FROM           170  '170'

 L. 406       180  LOAD_FAST                'i'
              182  LOAD_CONST               1
              184  INPLACE_ADD      
              186  STORE_FAST               'i'
              188  JUMP_BACK           140  'to 140'
            190_0  COME_FROM           150  '150'

Parse error at or near `JUMP_BACK' instruction at offset 188


class CIMultiDict(MultiDict):
    __doc__ = 'Dictionary with the support for duplicate case-insensitive keys.'

    def _title(self, key):
        return key.title()


class _Iter:
    __slots__ = ('_size', '_iter')

    def __init__(self, size, iterator):
        self._size = size
        self._iter = iterator

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def __length_hint__(self):
        return self._size


class _ViewBase:

    def __init__(self, impl):
        self._impl = impl
        self._version = impl._version

    def __len__(self):
        return len(self._impl._items)


class _ItemsView(_ViewBase, abc.ItemsView):

    def __contains__(self, item):
        if not isinstance(item, tuple):
            assert isinstance(item, list)
            assert len(item) == 2
            for i, k, v in self._impl._items:
                if item[0] == k:
                    if item[1] == v:
                        return True

            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for i, k, v in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            else:
                yield (
                 k, v)

    def __repr__(self):
        lst = []
        for item in self._impl._items:
            lst.append('{!r}: {!r}'.format(item[1], item[2]))
        else:
            body = ', '.join(lst)
            return '{}({})'.format(self.__class__.__name__, body)


class _ValuesView(_ViewBase, abc.ValuesView):

    def __contains__(self, value):
        for item in self._impl._items:
            if item[2] == value:
                return True
        else:
            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for item in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            else:
                yield item[2]

    def __repr__(self):
        lst = []
        for item in self._impl._items:
            lst.append('{!r}'.format(item[2]))
        else:
            body = ', '.join(lst)
            return '{}({})'.format(self.__class__.__name__, body)


class _KeysView(_ViewBase, abc.KeysView):

    def __contains__(self, key):
        for item in self._impl._items:
            if item[1] == key:
                return True
        else:
            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for item in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            else:
                yield item[1]

    def __repr__(self):
        lst = []
        for item in self._impl._items:
            lst.append('{!r}'.format(item[1]))
        else:
            body = ', '.join(lst)
            return '{}({})'.format(self.__class__.__name__, body)