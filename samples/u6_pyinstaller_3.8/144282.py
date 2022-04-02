# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\_collections.py
from collections import Mapping, MutableMapping
try:
    from threading import RLock
except ImportError:

    class RLock:

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_value, traceback):
            pass


else:
    try:
        from collections import OrderedDict
    except ImportError:
        from packages.ordered_dict import OrderedDict
    else:
        from packages.six import iterkeys, itervalues, PY3
        __all__ = [
         'RecentlyUsedContainer', 'HTTPHeaderDict']
        _Null = object()

        class RecentlyUsedContainer(MutableMapping):
            __doc__ = '\n    Provides a thread-safe dict-like container which maintains up to\n    ``maxsize`` keys while throwing away the least-recently-used keys beyond\n    ``maxsize``.\n\n    :param maxsize:\n        Maximum number of recent elements to retain.\n\n    :param dispose_func:\n        Every time an item is evicted from the container,\n        ``dispose_func(value)`` is called.  Callback which will get called\n    '
            ContainerCls = OrderedDict

            def __init__(self, maxsize=10, dispose_func=None):
                self._maxsize = maxsize
                self.dispose_func = dispose_func
                self._container = self.ContainerCls()
                self.lock = RLock()

            def __getitem__--- This code section failed: ---

 L.  51         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           46  'to 46'
                6  POP_TOP          

 L.  52         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _container
               12  LOAD_METHOD              pop
               14  LOAD_FAST                'key'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'item'

 L.  53        20  LOAD_FAST                'item'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _container
               26  LOAD_FAST                'key'
               28  STORE_SUBSCR     

 L.  54        30  LOAD_FAST                'item'
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH        4  '4'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 34

            def __setitem__(self, key, value):
                evicted_value = _Null
                with self.lock:
                    evicted_value = self._container.get(key, _Null)
                    self._container[key] = value
                    if len(self._container) > self._maxsize:
                        _key, evicted_value = self._container.popitem(last=False)
                if self.dispose_func:
                    if evicted_value is not _Null:
                        self.dispose_funcevicted_value

            def __delitem__(self, key):
                with self.lock:
                    value = self._container.popkey
                if self.dispose_func:
                    self.dispose_funcvalue

            def __len__--- This code section failed: ---

 L.  79         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           30  'to 30'
                6  POP_TOP          

 L.  80         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _container
               14  CALL_FUNCTION_1       1  ''
               16  POP_BLOCK        
               18  ROT_TWO          
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  RETURN_VALUE     
             30_0  COME_FROM_WITH        4  '4'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 18

            def __iter__(self):
                raise NotImplementedError('Iteration over this class is unlikely to be threadsafe.')

            def clear(self):
                with self.lock:
                    values = list(itervalues(self._container))
                    self._container.clear()
                if self.dispose_func:
                    for value in values:
                        self.dispose_funcvalue

            def keys--- This code section failed: ---

 L.  96         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L.  97         8  LOAD_GLOBAL              list
               10  LOAD_GLOBAL              iterkeys
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _container
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22


        _dict_setitem = dict.__setitem__
        _dict_getitem = dict.__getitem__
        _dict_delitem = dict.__delitem__
        _dict_contains = dict.__contains__
        _dict_setdefault = dict.setdefault

        class HTTPHeaderDict(dict):
            __doc__ = "\n    :param headers:\n        An iterable of field-value pairs. Must not contain multiple field names\n        when compared case-insensitively.\n\n    :param kwargs:\n        Additional field-value pairs to pass in to ``dict.update``.\n\n    A ``dict`` like container for storing HTTP Headers.\n\n    Field names are stored and compared case-insensitively in compliance with\n    RFC 7230. Iteration provides the first case-sensitive key seen for each\n    case-insensitive pair.\n\n    Using ``__setitem__`` syntax overwrites fields that compare equal\n    case-insensitively in order to maintain ``dict``'s api. For fields that\n    compare equal, instead create a new ``HTTPHeaderDict`` and use ``.add``\n    in a loop.\n\n    If multiple fields that are equal case-insensitively are passed to the\n    constructor or ``.update``, the behavior is undefined and some will be\n    lost.\n\n    >>> headers = HTTPHeaderDict()\n    >>> headers.add('Set-Cookie', 'foo=bar')\n    >>> headers.add('set-cookie', 'baz=quxx')\n    >>> headers['content-length'] = '7'\n    >>> headers['SET-cookie']\n    'foo=bar, baz=quxx'\n    >>> headers['Content-Length']\n    '7'\n    "

            def __init__(self, headers=None, **kwargs):
                dict.__init__self
                if headers is not None:
                    if isinstance(headers, HTTPHeaderDict):
                        self._copy_fromheaders
                    else:
                        self.extendheaders
                if kwargs:
                    self.extendkwargs

            def __setitem__(self, key, val):
                return _dict_setitem(self, key.lower(), (key, val))

            def __getitem__(self, key):
                val = _dict_getitem(self, key.lower())
                return ', '.joinval[1:]

            def __delitem__(self, key):
                return _dict_delitem(self, key.lower())

            def __contains__(self, key):
                return _dict_contains(self, key.lower())

            def __eq__(self, other):
                if not isinstance(other, Mapping):
                    if not hasattr(other, 'keys'):
                        return False
                if not isinstance(other, type(self)):
                    other = type(self)(other)
                return dict(((k1, self[k1]) for k1 in self)) == dict(((k2, other[k2]) for k2 in other))

            def __ne__(self, other):
                return not self.__eq__other

            values = MutableMapping.values
            get = MutableMapping.get
            update = MutableMapping.update
            if not PY3:
                iterkeys = MutableMapping.iterkeys
                itervalues = MutableMapping.itervalues
            _HTTPHeaderDict__marker = object()

            def pop(self, key, default=_HTTPHeaderDict__marker):
                """D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
          If key is not found, d is returned if given, otherwise KeyError is raised.
        """
                try:
                    value = self[key]
                except KeyError:
                    if default is self._HTTPHeaderDict__marker:
                        raise
                    return default
                else:
                    del self[key]
                    return value

            def discard(self, key):
                try:
                    del self[key]
                except KeyError:
                    pass

            def add(self, key, val):
                """Adds a (name, value) pair, doesn't overwrite the value if it already
        exists.

        >>> headers = HTTPHeaderDict(foo='bar')
        >>> headers.add('Foo', 'baz')
        >>> headers['foo']
        'bar, baz'
        """
                key_lower = key.lower()
                new_vals = (key, val)
                vals = _dict_setdefault(self, key_lower, new_vals)
                if new_vals is not vals:
                    if isinstance(vals, list):
                        vals.appendval
                    else:
                        _dict_setitem(self, key_lower, [vals[0], vals[1], val])

            def extend(self, *args, **kwargs):
                """Generic import function for any type of header-like object.
        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
                if len(args) > 1:
                    raise TypeError('extend() takes at most 1 positional arguments ({} given)'.formatlen(args))
                other = args[0] if len(args) >= 1 else ()
                if isinstance(other, HTTPHeaderDict):
                    for key, val in other.iteritems():
                        self.add(key, val)

                else:
                    if isinstance(other, Mapping):
                        for key in other:
                            self.add(key, other[key])

                    else:
                        if hasattr(other, 'keys'):
                            for key in other.keys():
                                self.add(key, other[key])

                        else:
                            for key, value in other:
                                self.add(key, value)
                            else:
                                for key, value in kwargs.items():
                                    self.add(key, value)

            def getlist(self, key):
                """Returns a list of all the values for the named field. Returns an
        empty list if the key doesn't exist."""
                try:
                    vals = _dict_getitem(self, key.lower())
                except KeyError:
                    return []
                else:
                    if isinstance(vals, tuple):
                        return [
                         vals[1]]
                    return vals[1:]

            getheaders = getlist
            getallmatchingheaders = getlist
            iget = getlist

            def __repr__(self):
                return '%s(%s)' % (type(self).__name__, dict(self.itermerged()))

            def _copy_from(self, other):
                for key in other:
                    val = _dict_getitem(other, key)
                    if isinstance(val, list):
                        val = list(val)
                    _dict_setitem(self, key, val)

            def copy(self):
                clone = type(self)()
                clone._copy_fromself
                return clone

            def iteritems(self):
                """Iterate over all header lines, including duplicate ones."""
                for key in self:
                    vals = _dict_getitem(self, key)
                    for val in vals[1:]:
                        (yield (
                         vals[0], val))

            def itermerged(self):
                """Iterate over all headers, merging duplicate ones together."""
                for key in self:
                    val = _dict_getitem(self, key)
                    (yield (val[0], ', '.joinval[1:]))

            def items(self):
                return list(self.iteritems())

            @classmethod
            def from_httplib(cls, message):
                """Read headers from a Python 2 httplib message object."""
                headers = []
                for line in message.headers:
                    if line.startswith(' ', '\t'):
                        key, value = headers[(-1)]
                        headers[-1] = (key, value + '\r\n' + line.rstrip())
                    else:
                        key, value = line.split(':', 1)
                        headers.append(key, value.strip())
                else:
                    return cls(headers)