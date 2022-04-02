# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
                if i1 != i2 or v1 != v2:
                    return False
                return True

        if len(self._impl._items) != len(other):
            return False
        for k, v in self.items():
            nv = other.get(k, _marker)
            if v != nv:
                return False
            return True

    def __contains__(self, key):
        identity = self._title(key)
        for i, k, v in self._impl._items:
            if i == identity:
                return True
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
        return (self.__class__, (list(self.items()),))

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
        elif args:
            arg = args[0]
            if isinstance(args[0], (MultiDict, MultiDictProxy)):
                items = kwargs or arg._impl._items
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
            return (i[1], i[2])
        raise KeyError('empty multidict')

    def update(self, *args, **kwargs):
        """Update the dictionary from *other*, overwriting existing keys."""
        self._extend(args, kwargs, 'update', self._update_items)

    def _update_items--- This code section failed: ---

 L. 350         0  LOAD_FAST                'items'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 351         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 352         8  BUILD_MAP_0           0 
               10  STORE_FAST               'used_keys'

 L. 353        12  LOAD_FAST                'items'
               14  GET_ITER         
               16  FOR_ITER            158  'to 158'
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'identity'
               22  STORE_FAST               'key'
               24  STORE_FAST               'value'

 L. 354        26  LOAD_FAST                'used_keys'
               28  LOAD_METHOD              get
               30  LOAD_FAST                'identity'
               32  LOAD_CONST               0
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'start'

 L. 355        38  LOAD_GLOBAL              range
               40  LOAD_FAST                'start'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _impl
               48  LOAD_ATTR                _items
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_2       2  ''
               54  GET_ITER         
             56_0  COME_FROM            82  '82'
               56  FOR_ITER            120  'to 120'
               58  STORE_FAST               'i'

 L. 356        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _impl
               64  LOAD_ATTR                _items
               66  LOAD_FAST                'i'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'item'

 L. 357        72  LOAD_FAST                'item'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'identity'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    56  'to 56'

 L. 358        84  LOAD_FAST                'i'
               86  LOAD_CONST               1
               88  BINARY_ADD       
               90  LOAD_FAST                'used_keys'
               92  LOAD_FAST                'identity'
               94  STORE_SUBSCR     

 L. 359        96  LOAD_FAST                'identity'
               98  LOAD_FAST                'key'
              100  LOAD_FAST                'value'
              102  BUILD_TUPLE_3         3 
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _impl
              108  LOAD_ATTR                _items
              110  LOAD_FAST                'i'
              112  STORE_SUBSCR     

 L. 360       114  POP_TOP          
              116  CONTINUE             16  'to 16'
              118  JUMP_BACK            56  'to 56'

 L. 362       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _impl
              124  LOAD_ATTR                _items
              126  LOAD_METHOD              append
              128  LOAD_FAST                'identity'
              130  LOAD_FAST                'key'
              132  LOAD_FAST                'value'
              134  BUILD_TUPLE_3         3 
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L. 363       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _impl
              146  LOAD_ATTR                _items
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'used_keys'
              152  LOAD_FAST                'identity'
              154  STORE_SUBSCR     
              156  JUMP_BACK            16  'to 16'

 L. 366       158  LOAD_CONST               0
              160  STORE_FAST               'i'

 L. 367       162  LOAD_FAST                'i'
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _impl
              170  LOAD_ATTR                _items
              172  CALL_FUNCTION_1       1  ''
              174  COMPARE_OP               <
          176_178  POP_JUMP_IF_FALSE   258  'to 258'

 L. 368       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _impl
              184  LOAD_ATTR                _items
              186  LOAD_FAST                'i'
              188  BINARY_SUBSCR    
              190  STORE_FAST               'item'

 L. 369       192  LOAD_FAST                'item'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  STORE_FAST               'identity'

 L. 370       200  LOAD_FAST                'used_keys'
              202  LOAD_METHOD              get
              204  LOAD_FAST                'identity'
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'pos'

 L. 371       210  LOAD_FAST                'pos'
              212  LOAD_CONST               None
              214  COMPARE_OP               is
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 372       218  LOAD_FAST                'i'
              220  LOAD_CONST               1
              222  INPLACE_ADD      
              224  STORE_FAST               'i'

 L. 373       226  JUMP_BACK           162  'to 162'
            228_0  COME_FROM           216  '216'

 L. 374       228  LOAD_FAST                'i'
              230  LOAD_FAST                'pos'
              232  COMPARE_OP               >=
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L. 375       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _impl
              240  LOAD_ATTR                _items
              242  LOAD_FAST                'i'
              244  DELETE_SUBSCR    
              246  JUMP_BACK           162  'to 162'
            248_0  COME_FROM           234  '234'

 L. 377       248  LOAD_FAST                'i'
              250  LOAD_CONST               1
              252  INPLACE_ADD      
              254  STORE_FAST               'i'
              256  JUMP_BACK           162  'to 162'
            258_0  COME_FROM           176  '176'

 L. 379       258  LOAD_FAST                'self'
              260  LOAD_ATTR                _impl
              262  LOAD_METHOD              incr_version
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

Parse error at or near `CONTINUE' instruction at offset 116

    def _replace(self, key, value):
        key = self._key(key)
        identity = self._title(key)
        items = self._impl._items
        for i in range(len(items)):
            item = items[i]
            if item[0] == identity:
                items[i] = (
                 identity, key, value)
                rgt = i
                self._impl.incr_version()
                break
        else:
            self._impl._items.append((identity, key, value))
            self._impl.incr_version()
            return None
            i = rgt + 1
            while i < len(items):
                item = items[i]
                if item[0] == identity:
                    del items[i]
                else:
                    i += 1


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
            if item[0] == k and item[1] == v:
                return True
            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for i, k, v in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            (yield (
             k, v))

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
            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for item in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            (yield item[2])

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
            return False

    def __iter__(self):
        return _Iter(len(self), self._iter())

    def _iter(self):
        for item in self._impl._items:
            if self._version != self._impl._version:
                raise RuntimeError('Dictionary changed during iteration')
            (yield item[1])

    def __repr__(self):
        lst = []
        for item in self._impl._items:
            lst.append('{!r}'.format(item[1]))
        else:
            body = ', '.join(lst)
            return '{}({})'.format(self.__class__.__name__, body)