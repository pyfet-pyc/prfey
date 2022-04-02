# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyasn1\type\namedval.py
from pyasn1 import error
__all__ = [
 'NamedValues']

class NamedValues(object):
    __doc__ = "Create named values object.\n\n    The |NamedValues| object represents a collection of string names\n    associated with numeric IDs. These objects are used for giving\n    names to otherwise numerical values.\n\n    |NamedValues| objects are immutable and duck-type Python\n    :class:`dict` object mapping ID to name and vice-versa.\n\n    Parameters\n    ----------\n    *args: variable number of two-element :py:class:`tuple`\n\n        name: :py:class:`str`\n            Value label\n\n        value: :py:class:`int`\n            Numeric value\n\n    Keyword Args\n    ------------\n    name: :py:class:`str`\n        Value label\n\n    value: :py:class:`int`\n        Numeric value\n\n    Examples\n    --------\n\n    .. code-block:: pycon\n\n        >>> nv = NamedValues('a', 'b', ('c', 0), d=1)\n        >>> nv\n        >>> {'c': 0, 'd': 1, 'a': 2, 'b': 3}\n        >>> nv[0]\n        'c'\n        >>> nv['a']\n        2\n    "

    def __init__--- This code section failed: ---

 L.  56         0  BUILD_MAP_0           0 
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _NamedValues__names

 L.  57         6  BUILD_MAP_0           0 
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _NamedValues__numbers

 L.  59        12  BUILD_LIST_0          0 
               14  STORE_FAST               'anonymousNames'

 L.  61        16  LOAD_FAST                'args'
               18  GET_ITER         
               20  FOR_ITER            176  'to 176'
               22  STORE_FAST               'namedValue'

 L.  62        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'namedValue'
               28  LOAD_GLOBAL              tuple
               30  LOAD_GLOBAL              list
               32  BUILD_TUPLE_2         2 
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    88  'to 88'

 L.  63        38  SETUP_FINALLY        52  'to 52'

 L.  64        40  LOAD_FAST                'namedValue'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'name'
               46  STORE_FAST               'number'
               48  POP_BLOCK        
               50  JUMP_ABSOLUTE       100  'to 100'
             52_0  COME_FROM_FINALLY    38  '38'

 L.  66        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  <121>                84  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  67        64  LOAD_GLOBAL              error
               66  LOAD_METHOD              PyAsn1Error
               68  LOAD_STR                 'Not a proper attribute-value pair %r'
               70  LOAD_FAST                'namedValue'
               72  BUILD_TUPLE_1         1 
               74  BINARY_MODULO    
               76  CALL_METHOD_1         1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
               80  POP_EXCEPT       
               82  JUMP_ABSOLUTE       100  'to 100'
               84  <48>             
               86  BREAK_LOOP          100  'to 100'
             88_0  COME_FROM            36  '36'

 L.  70        88  LOAD_FAST                'anonymousNames'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'namedValue'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L.  71        98  JUMP_BACK            20  'to 20'
            100_0  COME_FROM_EXCEPT_CLAUSE    86  '86'
            100_1  COME_FROM_EXCEPT_CLAUSE    82  '82'

 L.  73       100  LOAD_FAST                'name'
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _NamedValues__names
              106  <118>                 0  ''
              108  POP_JUMP_IF_FALSE   126  'to 126'

 L.  74       110  LOAD_GLOBAL              error
              112  LOAD_METHOD              PyAsn1Error
              114  LOAD_STR                 'Duplicate name %s'
              116  LOAD_FAST                'name'
              118  BUILD_TUPLE_1         1 
              120  BINARY_MODULO    
              122  CALL_METHOD_1         1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           108  '108'

 L.  76       126  LOAD_FAST                'number'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                _NamedValues__numbers
              132  <118>                 0  ''
              134  POP_JUMP_IF_FALSE   154  'to 154'

 L.  77       136  LOAD_GLOBAL              error
              138  LOAD_METHOD              PyAsn1Error
              140  LOAD_STR                 'Duplicate number  %s=%s'
              142  LOAD_FAST                'name'
              144  LOAD_FAST                'number'
              146  BUILD_TUPLE_2         2 
              148  BINARY_MODULO    
              150  CALL_METHOD_1         1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           134  '134'

 L.  79       154  LOAD_FAST                'number'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _NamedValues__names
              160  LOAD_FAST                'name'
              162  STORE_SUBSCR     

 L.  80       164  LOAD_FAST                'name'
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _NamedValues__numbers
              170  LOAD_FAST                'number'
              172  STORE_SUBSCR     
              174  JUMP_BACK            20  'to 20'

 L.  82       176  LOAD_FAST                'kwargs'
              178  LOAD_METHOD              items
              180  CALL_METHOD_0         0  ''
              182  GET_ITER         
              184  FOR_ITER            268  'to 268'
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'name'
              190  STORE_FAST               'number'

 L.  83       192  LOAD_FAST                'name'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                _NamedValues__names
              198  <118>                 0  ''
              200  POP_JUMP_IF_FALSE   218  'to 218'

 L.  84       202  LOAD_GLOBAL              error
              204  LOAD_METHOD              PyAsn1Error
              206  LOAD_STR                 'Duplicate name %s'
              208  LOAD_FAST                'name'
              210  BUILD_TUPLE_1         1 
              212  BINARY_MODULO    
              214  CALL_METHOD_1         1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           200  '200'

 L.  86       218  LOAD_FAST                'number'
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                _NamedValues__numbers
              224  <118>                 0  ''
              226  POP_JUMP_IF_FALSE   246  'to 246'

 L.  87       228  LOAD_GLOBAL              error
              230  LOAD_METHOD              PyAsn1Error
              232  LOAD_STR                 'Duplicate number  %s=%s'
              234  LOAD_FAST                'name'
              236  LOAD_FAST                'number'
              238  BUILD_TUPLE_2         2 
              240  BINARY_MODULO    
              242  CALL_METHOD_1         1  ''
              244  RAISE_VARARGS_1       1  'exception instance'
            246_0  COME_FROM           226  '226'

 L.  89       246  LOAD_FAST                'number'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                _NamedValues__names
              252  LOAD_FAST                'name'
              254  STORE_SUBSCR     

 L.  90       256  LOAD_FAST                'name'
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                _NamedValues__numbers
              262  LOAD_FAST                'number'
              264  STORE_SUBSCR     
              266  JUMP_BACK           184  'to 184'

 L.  92       268  LOAD_FAST                'anonymousNames'
          270_272  POP_JUMP_IF_FALSE   370  'to 370'

 L.  94       274  LOAD_FAST                'self'
              276  LOAD_ATTR                _NamedValues__numbers
          278_280  POP_JUMP_IF_FALSE   298  'to 298'
              282  LOAD_GLOBAL              max
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                _NamedValues__numbers
              288  CALL_FUNCTION_1       1  ''
              290  LOAD_CONST               1
              292  BINARY_ADD       
          294_296  JUMP_IF_TRUE_OR_POP   300  'to 300'
            298_0  COME_FROM           278  '278'
              298  LOAD_CONST               0
            300_0  COME_FROM           294  '294'
              300  STORE_FAST               'number'

 L.  96       302  LOAD_FAST                'anonymousNames'
              304  GET_ITER         
              306  FOR_ITER            370  'to 370'
              308  STORE_FAST               'name'

 L.  98       310  LOAD_FAST                'name'
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                _NamedValues__names
              316  <118>                 0  ''
          318_320  POP_JUMP_IF_FALSE   338  'to 338'

 L.  99       322  LOAD_GLOBAL              error
              324  LOAD_METHOD              PyAsn1Error
              326  LOAD_STR                 'Duplicate name %s'
              328  LOAD_FAST                'name'
              330  BUILD_TUPLE_1         1 
              332  BINARY_MODULO    
              334  CALL_METHOD_1         1  ''
              336  RAISE_VARARGS_1       1  'exception instance'
            338_0  COME_FROM           318  '318'

 L. 101       338  LOAD_FAST                'number'
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                _NamedValues__names
              344  LOAD_FAST                'name'
              346  STORE_SUBSCR     

 L. 102       348  LOAD_FAST                'name'
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                _NamedValues__numbers
              354  LOAD_FAST                'number'
              356  STORE_SUBSCR     

 L. 104       358  LOAD_FAST                'number'
              360  LOAD_CONST               1
              362  INPLACE_ADD      
              364  STORE_FAST               'number'
          366_368  JUMP_BACK           306  'to 306'
            370_0  COME_FROM           270  '270'

Parse error at or near `<121>' instruction at offset 56

    def __repr__(self):
        representation = ', '.join['%s=%d' % x for x in self.items]
        if len(representation) > 64:
            representation = representation[:32] + '...' + representation[-32:]
        return '<%s object, enums %s>' % (
         self.__class__.__name__, representation)

    def __eq__(self, other):
        return dict(self) == other

    def __ne__(self, other):
        return dict(self) != other

    def __lt__(self, other):
        return dict(self) < other

    def __le__(self, other):
        return dict(self) <= other

    def __gt__(self, other):
        return dict(self) > other

    def __ge__(self, other):
        return dict(self) >= other

    def __hash__(self):
        return hash(self.items)

    def __getitem__--- This code section failed: ---

 L. 139         0  SETUP_FINALLY        14  'to 14'

 L. 140         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _NamedValues__numbers
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 142        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                40  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 143        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _NamedValues__names
               30  LOAD_FAST                'key'
               32  BINARY_SUBSCR    
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             

Parse error at or near `<121>' instruction at offset 18

    def __len__(self):
        return len(self._NamedValues__names)

    def __contains__--- This code section failed: ---

 L. 149         0  LOAD_FAST                'key'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _NamedValues__names
                6  <118>                 0  ''
                8  JUMP_IF_TRUE_OR_POP    18  'to 18'
               10  LOAD_FAST                'key'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _NamedValues__numbers
               16  <118>                 0  ''
             18_0  COME_FROM             8  '8'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __iter__(self):
        return iter(self._NamedValues__names)

    def values(self):
        return iter(self._NamedValues__numbers)

    def keys(self):
        return iter(self._NamedValues__names)

    def items(self):
        for name in self._NamedValues__names:
            (yield (
             name, self._NamedValues__names[name]))

    def __add__(self, namedValues):
        return (self.__class__)(*tuple(self.items) + tuple(namedValues.items))

    def clone--- This code section failed: ---

 L. 172         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwargs'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  STORE_FAST               'new'

 L. 173        16  LOAD_FAST                'self'
               18  LOAD_FAST                'new'
               20  BINARY_ADD       
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def getName--- This code section failed: ---

 L. 178         0  LOAD_FAST                'value'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _NamedValues__numbers
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 179        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _NamedValues__numbers
               14  LOAD_FAST                'value'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def getValue--- This code section failed: ---

 L. 182         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _NamedValues__names
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 183        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _NamedValues__names
               14  LOAD_FAST                'name'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def getValues--- This code section failed: ---

 L. 186         0  SETUP_FINALLY        22  'to 22'

 L. 187         2  LOAD_CLOSURE             'self'
                4  BUILD_TUPLE_1         1 
                6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 'NamedValues.getValues.<locals>.<listcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_FAST                'names'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 189        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  <121>                66  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 190        34  LOAD_GLOBAL              error
               36  LOAD_METHOD              PyAsn1Error

 L. 191        38  LOAD_STR                 'Unknown bit identifier(s): %s'
               40  LOAD_GLOBAL              set
               42  LOAD_FAST                'names'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_METHOD              difference
               48  LOAD_DEREF               'self'
               50  LOAD_ATTR                _NamedValues__names
               52  CALL_METHOD_1         1  ''
               54  BUILD_TUPLE_1         1 
               56  BINARY_MODULO    

 L. 190        58  CALL_METHOD_1         1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
               66  <48>             
             68_0  COME_FROM            64  '64'

Parse error at or near `<121>' instruction at offset 26