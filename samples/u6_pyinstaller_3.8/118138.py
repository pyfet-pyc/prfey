# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\_utils.py
from __future__ import absolute_import, division, unicode_literals
from types import ModuleType
from six import text_type
try:
    import xml.etree.cElementTree as default_etree
except ImportError:
    import xml.etree.ElementTree as default_etree
else:
    __all__ = [
     'default_etree', 'MethodDispatcher', 'isSurrogatePair',
     'surrogatePairToCodepoint', 'moduleFactoryFactory',
     'supports_lone_surrogates']
    try:
        _x = eval('"\\uD800"')
        if not isinstance(_x, text_type):
            _x = eval('u"\\uD800"')
            assert isinstance(_x, text_type)
    except:
        supports_lone_surrogates = False
    else:
        supports_lone_surrogates = True

    class MethodDispatcher(dict):
        __doc__ = 'Dict with 2 special properties:\n\n    On initiation, keys that are lists, sets or tuples are converted to\n    multiple keys so accessing any one of the items in the original\n    list-like object returns the matching value\n\n    md = MethodDispatcher({("foo", "bar"):"baz"})\n    md["foo"] == "baz"\n\n    A default value which can be set through the default attribute.\n    '

        def __init__(self, items=()):
            _dictEntries = []
            for name, value in items:
                if isinstance(name, (list, tuple, frozenset, set)):
                    for item in name:
                        _dictEntries.append((item, value))

                else:
                    _dictEntries.append((name, value))
            else:
                dict.__init__(self, _dictEntries)
                assert len(self) == len(_dictEntries)
                self.default = None

        def __getitem__(self, key):
            return dict.get(self, key, self.default)


    def isSurrogatePair(data):
        return len(data) == 2 and ord(data[0]) >= 55296 and ord(data[0]) <= 56319 and ord(data[1]) >= 56320 and ord(data[1]) <= 57343


    def surrogatePairToCodepoint(data):
        char_val = 65536 + (ord(data[0]) - 55296) * 1024 + (ord(data[1]) - 56320)
        return char_val


    def moduleFactoryFactory(factory):
        moduleCache = {}

        def moduleFactory--- This code section failed: ---

 L.  90         0  LOAD_GLOBAL              isinstance
                2  LOAD_GLOBAL              ModuleType
                4  LOAD_ATTR                __name__
                6  LOAD_GLOBAL              type
                8  LOAD_STR                 ''
               10  CALL_FUNCTION_1       1  ''
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L.  91        16  LOAD_STR                 '_%s_factory'
               18  LOAD_FAST                'baseModule'
               20  LOAD_ATTR                __name__
               22  BINARY_MODULO    
               24  STORE_FAST               'name'
               26  JUMP_FORWARD         38  'to 38'
             28_0  COME_FROM            14  '14'

 L.  93        28  LOAD_CONST               b'_%s_factory'
               30  LOAD_FAST                'baseModule'
               32  LOAD_ATTR                __name__
               34  BINARY_MODULO    
               36  STORE_FAST               'name'
             38_0  COME_FROM            26  '26'

 L.  95        38  LOAD_GLOBAL              tuple
               40  LOAD_FAST                'kwargs'
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'kwargs_tuple'

 L.  97        50  SETUP_FINALLY        70  'to 70'

 L.  98        52  LOAD_DEREF               'moduleCache'
               54  LOAD_FAST                'name'
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'args'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'kwargs_tuple'
               64  BINARY_SUBSCR    
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    50  '50'

 L.  99        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   216  'to 216'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 100        84  LOAD_GLOBAL              ModuleType
               86  LOAD_FAST                'name'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'mod'

 L. 101        92  LOAD_DEREF               'factory'
               94  LOAD_FAST                'baseModule'
               96  BUILD_TUPLE_1         1 
               98  LOAD_FAST                'args'
              100  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              102  LOAD_FAST                'kwargs'
              104  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              106  STORE_FAST               'objs'

 L. 102       108  LOAD_FAST                'mod'
              110  LOAD_ATTR                __dict__
              112  LOAD_METHOD              update
              114  LOAD_FAST                'objs'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 103       120  LOAD_STR                 'name'
              122  LOAD_DEREF               'moduleCache'
              124  COMPARE_OP               not-in
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L. 104       128  BUILD_MAP_0           0 
              130  LOAD_DEREF               'moduleCache'
              132  LOAD_FAST                'name'
              134  STORE_SUBSCR     
            136_0  COME_FROM           126  '126'

 L. 105       136  LOAD_STR                 'args'
              138  LOAD_DEREF               'moduleCache'
              140  LOAD_FAST                'name'
              142  BINARY_SUBSCR    
              144  COMPARE_OP               not-in
              146  POP_JUMP_IF_FALSE   160  'to 160'

 L. 106       148  BUILD_MAP_0           0 
              150  LOAD_DEREF               'moduleCache'
              152  LOAD_FAST                'name'
              154  BINARY_SUBSCR    
              156  LOAD_FAST                'args'
              158  STORE_SUBSCR     
            160_0  COME_FROM           146  '146'

 L. 107       160  LOAD_STR                 'kwargs'
              162  LOAD_DEREF               'moduleCache'
              164  LOAD_FAST                'name'
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'args'
              170  BINARY_SUBSCR    
              172  COMPARE_OP               not-in
              174  POP_JUMP_IF_FALSE   192  'to 192'

 L. 108       176  BUILD_MAP_0           0 
              178  LOAD_DEREF               'moduleCache'
              180  LOAD_FAST                'name'
              182  BINARY_SUBSCR    
              184  LOAD_FAST                'args'
              186  BINARY_SUBSCR    
              188  LOAD_FAST                'kwargs_tuple'
              190  STORE_SUBSCR     
            192_0  COME_FROM           174  '174'

 L. 109       192  LOAD_FAST                'mod'
              194  LOAD_DEREF               'moduleCache'
              196  LOAD_FAST                'name'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'args'
              202  BINARY_SUBSCR    
              204  LOAD_FAST                'kwargs_tuple'
              206  STORE_SUBSCR     

 L. 110       208  LOAD_FAST                'mod'
              210  ROT_FOUR         
              212  POP_EXCEPT       
              214  RETURN_VALUE     
            216_0  COME_FROM            76  '76'
              216  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 80

        return moduleFactory


    def memoize(func):
        cache = {}

        def wrapped(*args, **kwargs):
            key = (
             tuple(args), tuple(kwargs.items))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]

        return wrapped