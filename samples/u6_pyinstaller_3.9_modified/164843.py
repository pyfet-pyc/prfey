# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: simplejson\ordered_dict.py
"""Drop-in replacement for collections.OrderedDict by Raymond Hettinger

http://code.activestate.com/recipes/576693/

"""
from UserDict import DictMixin

class OrderedDict(dict, DictMixin):

    def __init__--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'args'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               >
               10  POP_JUMP_IF_FALSE    28  'to 28'

 L.  12        12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 'expected at most 1 arguments, got %d'
               16  LOAD_GLOBAL              len
               18  LOAD_FAST                'args'
               20  CALL_FUNCTION_1       1  ''
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            10  '10'

 L.  13        28  SETUP_FINALLY        40  'to 40'

 L.  14        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _OrderedDict__end
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         66  'to 66'
             40_0  COME_FROM_FINALLY    28  '28'

 L.  15        40  DUP_TOP          
               42  LOAD_GLOBAL              AttributeError
               44  <121>                64  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  16        52  LOAD_FAST                'self'
               54  LOAD_METHOD              clear
               56  CALL_METHOD_0         0  ''
               58  POP_TOP          
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            38  '38'

 L.  17        66  LOAD_FAST                'self'
               68  LOAD_ATTR                update
               70  LOAD_FAST                'args'
               72  BUILD_MAP_0           0 
               74  LOAD_FAST                'kwds'
               76  <164>                 1  ''
               78  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               80  POP_TOP          

Parse error at or near `<121>' instruction at offset 44

    def clear(self):
        self._OrderedDict__end = end = []
        end += [None, end, end]
        self._OrderedDict__map = {}
        dict.clear(self)

    def __setitem__--- This code section failed: ---

 L.  26         0  LOAD_FAST                'key'
                2  LOAD_FAST                'self'
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    54  'to 54'

 L.  27         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _OrderedDict__end
               12  STORE_FAST               'end'

 L.  28        14  LOAD_FAST                'end'
               16  LOAD_CONST               1
               18  BINARY_SUBSCR    
               20  STORE_FAST               'curr'

 L.  29        22  LOAD_FAST                'key'
               24  LOAD_FAST                'curr'
               26  LOAD_FAST                'end'
               28  BUILD_LIST_3          3 
               30  DUP_TOP          
               32  LOAD_FAST                'curr'
               34  LOAD_CONST               2
               36  STORE_SUBSCR     
               38  DUP_TOP          
               40  LOAD_FAST                'end'
               42  LOAD_CONST               1
               44  STORE_SUBSCR     
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _OrderedDict__map
               50  LOAD_FAST                'key'
               52  STORE_SUBSCR     
             54_0  COME_FROM             6  '6'

 L.  30        54  LOAD_GLOBAL              dict
               56  LOAD_METHOD              __setitem__
               58  LOAD_FAST                'self'
               60  LOAD_FAST                'key'
               62  LOAD_FAST                'value'
               64  CALL_METHOD_3         3  ''
               66  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        key, prev, next = self._OrderedDict__map.pop(key)
        prev[2] = next
        next[1] = prev

    def __iter__--- This code section failed: ---

 L.  39         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _OrderedDict__end
                4  STORE_FAST               'end'

 L.  40         6  LOAD_FAST                'end'
                8  LOAD_CONST               2
               10  BINARY_SUBSCR    
               12  STORE_FAST               'curr'

 L.  41        14  LOAD_FAST                'curr'
               16  LOAD_FAST                'end'
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L.  42        22  LOAD_FAST                'curr'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  YIELD_VALUE      
               30  POP_TOP          

 L.  43        32  LOAD_FAST                'curr'
               34  LOAD_CONST               2
               36  BINARY_SUBSCR    
               38  STORE_FAST               'curr'
               40  JUMP_BACK            14  'to 14'
             42_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def __reversed__--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _OrderedDict__end
                4  STORE_FAST               'end'

 L.  47         6  LOAD_FAST                'end'
                8  LOAD_CONST               1
               10  BINARY_SUBSCR    
               12  STORE_FAST               'curr'

 L.  48        14  LOAD_FAST                'curr'
               16  LOAD_FAST                'end'
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    42  'to 42'

 L.  49        22  LOAD_FAST                'curr'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  YIELD_VALUE      
               30  POP_TOP          

 L.  50        32  LOAD_FAST                'curr'
               34  LOAD_CONST               1
               36  BINARY_SUBSCR    
               38  STORE_FAST               'curr'
               40  JUMP_BACK            14  'to 14'
             42_0  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        key = reversed(self).next if last else iter(self).next
        value = self.pop(key)
        return (key, value)

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = (
         self._OrderedDict__map, self._OrderedDict__end)
        del self._OrderedDict__map
        del self._OrderedDict__end
        inst_dict = vars(self).copy
        self._OrderedDict__map, self._OrderedDict__end = tmp
        if inst_dict:
            return (
             self.__class__, (items,), inst_dict)
        return (
         self.__class__, (items,))

    def keys(self):
        return list(self)

    setdefault = DictMixin.setdefault
    update = DictMixin.update
    pop = DictMixin.pop
    values = DictMixin.values
    items = DictMixin.items
    iterkeys = DictMixin.iterkeys
    itervalues = DictMixin.itervalues
    iteritems = DictMixin.iteritems

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items)

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        else:
            return d

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and all((p == q for p, q in zip(self.items, other.items)))
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other