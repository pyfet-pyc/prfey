# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multidict\_multidict_py.py
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

    def getall--- This code section failed: ---

 L.  54         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _title
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_DEREF              'identity'

 L.  55        10  LOAD_CLOSURE             'identity'
               12  BUILD_TUPLE_1         1 
               14  LOAD_LISTCOMP            '<code_object <listcomp>>'
               16  LOAD_STR                 '_Base.getall.<locals>.<listcomp>'
               18  MAKE_FUNCTION_8          'closure'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _impl
               24  LOAD_ATTR                _items
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'res'

 L.  56        32  LOAD_FAST                'res'
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L.  57        36  LOAD_FAST                'res'
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L.  58        40  LOAD_FAST                'res'
               42  POP_JUMP_IF_TRUE     56  'to 56'
               44  LOAD_FAST                'default'
               46  LOAD_GLOBAL              _marker
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L.  59        52  LOAD_FAST                'default'
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'
             56_1  COME_FROM            42  '42'

 L.  60        56  LOAD_GLOBAL              KeyError
               58  LOAD_STR                 'Key not found: %r'
               60  LOAD_FAST                'key'
               62  BINARY_MODULO    
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 48

    def getone--- This code section failed: ---

 L.  64         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _title
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'identity'

 L.  65        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _impl
               14  LOAD_ATTR                _items
               16  GET_ITER         
             18_0  COME_FROM            44  '44'
             18_1  COME_FROM            34  '34'
               18  FOR_ITER             46  'to 46'
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'i'
               24  STORE_FAST               'k'
               26  STORE_FAST               'v'

 L.  66        28  LOAD_FAST                'i'
               30  LOAD_FAST                'identity'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L.  67        36  LOAD_FAST                'v'
               38  ROT_TWO          
               40  POP_TOP          
               42  RETURN_VALUE     
               44  JUMP_BACK            18  'to 18'
             46_0  COME_FROM            18  '18'

 L.  68        46  LOAD_FAST                'default'
               48  LOAD_GLOBAL              _marker
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.  69        54  LOAD_FAST                'default'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.  70        58  LOAD_GLOBAL              KeyError
               60  LOAD_STR                 'Key not found: %r'
               62  LOAD_FAST                'key'
               64  BINARY_MODULO    
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 50

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

    def popone--- This code section failed: ---

 L. 297         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _title
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'identity'

 L. 298        10  LOAD_GLOBAL              range
               12  LOAD_GLOBAL              len
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _impl
               18  LOAD_ATTR                _items
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
             26_0  COME_FROM            94  '94'
             26_1  COME_FROM            48  '48'
               26  FOR_ITER             96  'to 96'
               28  STORE_FAST               'i'

 L. 299        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _impl
               34  LOAD_ATTR                _items
               36  LOAD_FAST                'i'
               38  BINARY_SUBSCR    
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  LOAD_FAST                'identity'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 300        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _impl
               54  LOAD_ATTR                _items
               56  LOAD_FAST                'i'
               58  BINARY_SUBSCR    
               60  LOAD_CONST               2
               62  BINARY_SUBSCR    
               64  STORE_FAST               'value'

 L. 301        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _impl
               70  LOAD_ATTR                _items
               72  LOAD_FAST                'i'
               74  DELETE_SUBSCR    

 L. 302        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _impl
               80  LOAD_METHOD              incr_version
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

 L. 303        86  LOAD_FAST                'value'
               88  ROT_TWO          
               90  POP_TOP          
               92  RETURN_VALUE     
               94  JUMP_BACK            26  'to 26'
             96_0  COME_FROM            26  '26'

 L. 304        96  LOAD_FAST                'default'
               98  LOAD_GLOBAL              _marker
              100  <117>                 0  ''
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 305       104  LOAD_GLOBAL              KeyError
              106  LOAD_FAST                'key'
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
              112  JUMP_FORWARD        118  'to 118'
            114_0  COME_FROM           102  '102'

 L. 307       114  LOAD_FAST                'default'
              116  RETURN_VALUE     
            118_0  COME_FROM           112  '112'

Parse error at or near `<117>' instruction at offset 100

    pop = popone

    def popall--- This code section failed: ---

 L. 319         0  LOAD_CONST               False
                2  STORE_FAST               'found'

 L. 320         4  LOAD_FAST                'self'
                6  LOAD_METHOD              _title
                8  LOAD_FAST                'key'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'identity'

 L. 321        14  BUILD_LIST_0          0 
               16  STORE_FAST               'ret'

 L. 322        18  LOAD_GLOBAL              range
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _impl
               26  LOAD_ATTR                _items
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  BINARY_SUBTRACT  
               34  LOAD_CONST               -1
               36  LOAD_CONST               -1
               38  CALL_FUNCTION_3       3  ''
               40  GET_ITER         
             42_0  COME_FROM           108  '108'
             42_1  COME_FROM            68  '68'
               42  FOR_ITER            110  'to 110'
               44  STORE_FAST               'i'

 L. 323        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _impl
               50  LOAD_ATTR                _items
               52  LOAD_FAST                'i'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'item'

 L. 324        58  LOAD_FAST                'item'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  LOAD_FAST                'identity'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE_BACK    42  'to 42'

 L. 325        70  LOAD_FAST                'ret'
               72  LOAD_METHOD              append
               74  LOAD_FAST                'item'
               76  LOAD_CONST               2
               78  BINARY_SUBSCR    
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 326        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _impl
               88  LOAD_ATTR                _items
               90  LOAD_FAST                'i'
               92  DELETE_SUBSCR    

 L. 327        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _impl
               98  LOAD_METHOD              incr_version
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 328       104  LOAD_CONST               True
              106  STORE_FAST               'found'
              108  JUMP_BACK            42  'to 42'
            110_0  COME_FROM            42  '42'

 L. 329       110  LOAD_FAST                'found'
              112  POP_JUMP_IF_TRUE    138  'to 138'

 L. 330       114  LOAD_FAST                'default'
              116  LOAD_GLOBAL              _marker
              118  <117>                 0  ''
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 331       122  LOAD_GLOBAL              KeyError
              124  LOAD_FAST                'key'
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
              130  JUMP_FORWARD        150  'to 150'
            132_0  COME_FROM           120  '120'

 L. 333       132  LOAD_FAST                'default'
              134  RETURN_VALUE     
              136  JUMP_FORWARD        150  'to 150'
            138_0  COME_FROM           112  '112'

 L. 335       138  LOAD_FAST                'ret'
              140  LOAD_METHOD              reverse
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 336       146  LOAD_FAST                'ret'
              148  RETURN_VALUE     
            150_0  COME_FROM           136  '136'
            150_1  COME_FROM           130  '130'

Parse error at or near `<117>' instruction at offset 118

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

    def _update_items--- This code section failed: ---

 L. 352         0  LOAD_FAST                'items'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 353         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 354         8  BUILD_MAP_0           0 
               10  STORE_FAST               'used_keys'

 L. 355        12  LOAD_FAST                'items'
               14  GET_ITER         
             16_0  COME_FROM           156  '156'
             16_1  COME_FROM           116  '116'
               16  FOR_ITER            158  'to 158'
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'identity'
               22  STORE_FAST               'key'
               24  STORE_FAST               'value'

 L. 356        26  LOAD_FAST                'used_keys'
               28  LOAD_METHOD              get
               30  LOAD_FAST                'identity'
               32  LOAD_CONST               0
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'start'

 L. 357        38  LOAD_GLOBAL              range
               40  LOAD_FAST                'start'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _impl
               48  LOAD_ATTR                _items
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_2       2  ''
               54  GET_ITER         
             56_0  COME_FROM           118  '118'
             56_1  COME_FROM            82  '82'
               56  FOR_ITER            120  'to 120'
               58  STORE_FAST               'i'

 L. 358        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _impl
               64  LOAD_ATTR                _items
               66  LOAD_FAST                'i'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'item'

 L. 359        72  LOAD_FAST                'item'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'identity'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE_BACK    56  'to 56'

 L. 360        84  LOAD_FAST                'i'
               86  LOAD_CONST               1
               88  BINARY_ADD       
               90  LOAD_FAST                'used_keys'
               92  LOAD_FAST                'identity'
               94  STORE_SUBSCR     

 L. 361        96  LOAD_FAST                'identity'
               98  LOAD_FAST                'key'
              100  LOAD_FAST                'value'
              102  BUILD_TUPLE_3         3 
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _impl
              108  LOAD_ATTR                _items
              110  LOAD_FAST                'i'
              112  STORE_SUBSCR     

 L. 362       114  POP_TOP          
              116  BREAK_LOOP           16  'to 16'
              118  JUMP_BACK            56  'to 56'
            120_0  COME_FROM            56  '56'

 L. 364       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _impl
              124  LOAD_ATTR                _items
              126  LOAD_METHOD              append
              128  LOAD_FAST                'identity'
              130  LOAD_FAST                'key'
              132  LOAD_FAST                'value'
              134  BUILD_TUPLE_3         3 
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L. 365       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _impl
              146  LOAD_ATTR                _items
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'used_keys'
              152  LOAD_FAST                'identity'
              154  STORE_SUBSCR     
              156  JUMP_BACK            16  'to 16'
            158_0  COME_FROM            16  '16'

 L. 368       158  LOAD_CONST               0
              160  STORE_FAST               'i'
            162_0  COME_FROM           256  '256'
            162_1  COME_FROM           246  '246'
            162_2  COME_FROM           226  '226'

 L. 369       162  LOAD_FAST                'i'
              164  LOAD_GLOBAL              len
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _impl
              170  LOAD_ATTR                _items
              172  CALL_FUNCTION_1       1  ''
              174  COMPARE_OP               <
          176_178  POP_JUMP_IF_FALSE   258  'to 258'

 L. 370       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _impl
              184  LOAD_ATTR                _items
              186  LOAD_FAST                'i'
              188  BINARY_SUBSCR    
              190  STORE_FAST               'item'

 L. 371       192  LOAD_FAST                'item'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  STORE_FAST               'identity'

 L. 372       200  LOAD_FAST                'used_keys'
              202  LOAD_METHOD              get
              204  LOAD_FAST                'identity'
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'pos'

 L. 373       210  LOAD_FAST                'pos'
              212  LOAD_CONST               None
              214  <117>                 0  ''
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 374       218  LOAD_FAST                'i'
              220  LOAD_CONST               1
              222  INPLACE_ADD      
              224  STORE_FAST               'i'

 L. 375       226  JUMP_BACK           162  'to 162'
            228_0  COME_FROM           216  '216'

 L. 376       228  LOAD_FAST                'i'
              230  LOAD_FAST                'pos'
              232  COMPARE_OP               >=
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L. 377       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _impl
              240  LOAD_ATTR                _items
              242  LOAD_FAST                'i'
              244  DELETE_SUBSCR    
              246  JUMP_BACK           162  'to 162'
            248_0  COME_FROM           234  '234'

 L. 379       248  LOAD_FAST                'i'
              250  LOAD_CONST               1
              252  INPLACE_ADD      
              254  STORE_FAST               'i'
              256  JUMP_BACK           162  'to 162'
            258_0  COME_FROM           176  '176'

 L. 381       258  LOAD_FAST                'self'
              260  LOAD_ATTR                _impl
              262  LOAD_METHOD              incr_version
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

Parse error at or near `<117>' instruction at offset 214

    def _replace--- This code section failed: ---

 L. 384         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _key
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'key'

 L. 385        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _title
               14  LOAD_FAST                'key'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'identity'

 L. 386        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _impl
               24  LOAD_ATTR                _items
               26  STORE_FAST               'items'

 L. 388        28  LOAD_GLOBAL              range
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'items'
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
             40_0  COME_FROM            96  '96'
             40_1  COME_FROM            62  '62'
               40  FOR_ITER             98  'to 98'
               42  STORE_FAST               'i'

 L. 389        44  LOAD_FAST                'items'
               46  LOAD_FAST                'i'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'item'

 L. 390        52  LOAD_FAST                'item'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'identity'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L. 391        64  LOAD_FAST                'identity'
               66  LOAD_FAST                'key'
               68  LOAD_FAST                'value'
               70  BUILD_TUPLE_3         3 
               72  LOAD_FAST                'items'
               74  LOAD_FAST                'i'
               76  STORE_SUBSCR     

 L. 393        78  LOAD_FAST                'i'
               80  STORE_FAST               'rgt'

 L. 394        82  LOAD_FAST                'self'
               84  LOAD_ATTR                _impl
               86  LOAD_METHOD              incr_version
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          

 L. 395        92  POP_TOP          
               94  BREAK_LOOP          132  'to 132'
               96  JUMP_BACK            40  'to 40'
             98_0  COME_FROM            40  '40'

 L. 397        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _impl
              102  LOAD_ATTR                _items
              104  LOAD_METHOD              append
              106  LOAD_FAST                'identity'
              108  LOAD_FAST                'key'
              110  LOAD_FAST                'value'
              112  BUILD_TUPLE_3         3 
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 398       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _impl
              122  LOAD_METHOD              incr_version
              124  CALL_METHOD_0         0  ''
              126  POP_TOP          

 L. 399       128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM            94  '94'

 L. 402       132  LOAD_FAST                'rgt'
              134  LOAD_CONST               1
              136  BINARY_ADD       
              138  STORE_FAST               'i'
            140_0  COME_FROM           188  '188'
            140_1  COME_FROM           178  '178'

 L. 403       140  LOAD_FAST                'i'
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'items'
              146  CALL_FUNCTION_1       1  ''
              148  COMPARE_OP               <
              150  POP_JUMP_IF_FALSE   190  'to 190'

 L. 404       152  LOAD_FAST                'items'
              154  LOAD_FAST                'i'
              156  BINARY_SUBSCR    
              158  STORE_FAST               'item'

 L. 405       160  LOAD_FAST                'item'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_FAST                'identity'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   180  'to 180'

 L. 406       172  LOAD_FAST                'items'
              174  LOAD_FAST                'i'
              176  DELETE_SUBSCR    
              178  JUMP_BACK           140  'to 140'
            180_0  COME_FROM           170  '170'

 L. 408       180  LOAD_FAST                'i'
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

    def __contains__--- This code section failed: ---

 L. 446         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'item'
                4  LOAD_GLOBAL              tuple
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     24  'to 24'
               10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'item'
               14  LOAD_GLOBAL              list
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'
             24_1  COME_FROM             8  '8'

 L. 447        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'item'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               2
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  <74>             
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 448        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _impl
               44  LOAD_ATTR                _items
               46  GET_ITER         
             48_0  COME_FROM            88  '88'
             48_1  COME_FROM            80  '80'
             48_2  COME_FROM            68  '68'
               48  FOR_ITER             90  'to 90'
               50  UNPACK_SEQUENCE_3     3 
               52  STORE_FAST               'i'
               54  STORE_FAST               'k'
               56  STORE_FAST               'v'

 L. 449        58  LOAD_FAST                'item'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  LOAD_FAST                'k'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE_BACK    48  'to 48'
               70  LOAD_FAST                'item'
               72  LOAD_CONST               1
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'v'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE_BACK    48  'to 48'

 L. 450        82  POP_TOP          
               84  LOAD_CONST               True
               86  RETURN_VALUE     
               88  JUMP_BACK            48  'to 48'
             90_0  COME_FROM            48  '48'

 L. 451        90  LOAD_CONST               False
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

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