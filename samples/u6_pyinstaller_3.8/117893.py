# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bson\son.py
"""Tools for creating and manipulating SON, the Serialized Ocument Notation.

Regular dictionaries can be used instead of SON objects, but not when the order
of keys is important. A SON object can be used just like a normal Python
dictionary."""
import copy, re
from bson.py3compat import abc, iteritems
RE_TYPE = type(re.compile(''))

class SON(dict):
    __doc__ = 'SON data.\n\n    A subclass of dict that maintains ordering of keys and provides a\n    few extra niceties for dealing with SON. SON provides an API\n    similar to collections.OrderedDict from Python 2.7+.\n    '

    def __init__(self, data=None, **kwargs):
        self._SON__keys = []
        dict.__init__(self)
        self.update(data)
        self.update(kwargs)

    def __new__(cls, *args, **kwargs):
        instance = (super(SON, cls).__new__)(cls, *args, **kwargs)
        instance._SON__keys = []
        return instance

    def __repr__(self):
        result = []
        for key in self._SON__keys:
            result.append('(%r, %r)' % (key, self[key]))
        else:
            return 'SON([%s])' % ', '.join(result)

    def __setitem__(self, key, value):
        if key not in self._SON__keys:
            self._SON__keys.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        self._SON__keys.remove(key)
        dict.__delitem__(self, key)

    def keys(self):
        return list(self._SON__keys)

    def copy(self):
        other = SON()
        other.update(self)
        return other

    def __iter__(self):
        for k in self._SON__keys:
            (yield k)

    def has_key(self, key):
        return key in self._SON__keys

    def iteritems(self):
        for k in self:
            (yield (
             k, self[k]))

    def iterkeys(self):
        return self.__iter__()

    def itervalues(self):
        for _, v in self.iteritems():
            (yield v)

    def values(self):
        return [v for _, v in self.iteritems()]

    def items(self):
        return [(
         key, self[key]) for key in self]

    def clear(self):
        self._SON__keys = []
        super(SON, self).clear()

    def setdefault--- This code section failed: ---

 L. 108         0  SETUP_FINALLY        12  'to 12'

 L. 109         2  LOAD_FAST                'self'
                4  LOAD_FAST                'key'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 110        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 111        26  LOAD_FAST                'default'
               28  LOAD_FAST                'self'
               30  LOAD_FAST                'key'
               32  STORE_SUBSCR     
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            18  '18'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'

 L. 112        40  LOAD_FAST                'default'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError('pop expected at most 2 arguments, got ' + repr(1 + len(args)))
        try:
            value = self[key]
        except KeyError:
            if args:
                return args[0]
            raise
        else:
            del self[key]
            return value

    def popitem(self):
        try:
            k, v = next(self.iteritems())
        except StopIteration:
            raise KeyError('container is empty')
        else:
            del self[k]
            return (k, v)

    def update(self, other=None, **kwargs):
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):
            for k, v in other.iteritems():
                self[k] = v

        else:
            if hasattr(other, 'keys'):
                for k in other.keys():
                    self[k] = other[k]

            else:
                for k, v in other:
                    self[k] = v
                else:
                    if kwargs:
                        self.update(kwargs)

    def get--- This code section failed: ---

 L. 152         0  SETUP_FINALLY        12  'to 12'

 L. 153         2  LOAD_FAST                'self'
                4  LOAD_FAST                'key'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 154        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    34  'to 34'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 155        26  LOAD_FAST                'default'
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22

    def __eq__(self, other):
        """Comparison to another SON is order-sensitive while comparison to a
        regular dictionary is order-insensitive.
        """
        if isinstance(other, SON):
            return len(self) == len(other) and self.items() == other.items()
        return self.to_dict() == other

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self._SON__keys)

    def to_dict(self):
        """Convert a SON document to a normal Python dictionary instance.

        This is trickier than just *dict(...)* because it needs to be
        recursive.
        """

        def transform_value(value):
            if isinstance(value, list):
                return [transform_value(v) for v in value]
            if isinstance(value, abc.Mapping):
                return dict([(
                 k, transform_value(v)) for k, v in iteritems(value)])
            return value

        return transform_value(dict(self))

    def __deepcopy__(self, memo):
        out = SON()
        val_id = id(self)
        if val_id in memo:
            return memo.get(val_id)
        memo[val_id] = out
        for k, v in self.iteritems():
            if not isinstance(v, RE_TYPE):
                v = copy.deepcopy(v, memo)
            out[k] = v
        else:
            return out