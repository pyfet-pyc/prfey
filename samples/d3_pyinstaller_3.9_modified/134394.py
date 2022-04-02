# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\_cmp.py
from __future__ import absolute_import, division, print_function
import functools
from ._compat import new_class
from ._make import _make_ne
_operation_names = {'eq':'==', 
 'lt':'<',  'le':'<=',  'gt':'>',  'ge':'>='}

def cmp_using--- This code section failed: ---

 L.  50         0  LOAD_STR                 'value'
                2  BUILD_LIST_1          1 

 L.  51         4  LOAD_GLOBAL              _make_init
                6  CALL_FUNCTION_0       0  ''

 L.  52         8  BUILD_LIST_0          0 

 L.  53        10  LOAD_GLOBAL              _is_comparable_to

 L.  49        12  LOAD_CONST               ('__slots__', '__init__', '_requirements', '_is_comparable_to')
               14  BUILD_CONST_KEY_MAP_4     4 
               16  STORE_DEREF              'body'

 L.  57        18  LOAD_CONST               0
               20  STORE_FAST               'num_order_functions'

 L.  58        22  LOAD_CONST               False
               24  STORE_FAST               'has_eq_function'

 L.  60        26  LOAD_FAST                'eq'
               28  LOAD_CONST               None
               30  <117>                 1  ''
               32  POP_JUMP_IF_FALSE    62  'to 62'

 L.  61        34  LOAD_CONST               True
               36  STORE_FAST               'has_eq_function'

 L.  62        38  LOAD_GLOBAL              _make_operator
               40  LOAD_STR                 'eq'
               42  LOAD_FAST                'eq'
               44  CALL_FUNCTION_2       2  ''
               46  LOAD_DEREF               'body'
               48  LOAD_STR                 '__eq__'
               50  STORE_SUBSCR     

 L.  63        52  LOAD_GLOBAL              _make_ne
               54  CALL_FUNCTION_0       0  ''
               56  LOAD_DEREF               'body'
               58  LOAD_STR                 '__ne__'
               60  STORE_SUBSCR     
             62_0  COME_FROM            32  '32'

 L.  65        62  LOAD_FAST                'lt'
               64  LOAD_CONST               None
               66  <117>                 1  ''
               68  POP_JUMP_IF_FALSE    92  'to 92'

 L.  66        70  LOAD_FAST                'num_order_functions'
               72  LOAD_CONST               1
               74  INPLACE_ADD      
               76  STORE_FAST               'num_order_functions'

 L.  67        78  LOAD_GLOBAL              _make_operator
               80  LOAD_STR                 'lt'
               82  LOAD_FAST                'lt'
               84  CALL_FUNCTION_2       2  ''
               86  LOAD_DEREF               'body'
               88  LOAD_STR                 '__lt__'
               90  STORE_SUBSCR     
             92_0  COME_FROM            68  '68'

 L.  69        92  LOAD_FAST                'le'
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   122  'to 122'

 L.  70       100  LOAD_FAST                'num_order_functions'
              102  LOAD_CONST               1
              104  INPLACE_ADD      
              106  STORE_FAST               'num_order_functions'

 L.  71       108  LOAD_GLOBAL              _make_operator
              110  LOAD_STR                 'le'
              112  LOAD_FAST                'le'
              114  CALL_FUNCTION_2       2  ''
              116  LOAD_DEREF               'body'
              118  LOAD_STR                 '__le__'
              120  STORE_SUBSCR     
            122_0  COME_FROM            98  '98'

 L.  73       122  LOAD_FAST                'gt'
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_FALSE   152  'to 152'

 L.  74       130  LOAD_FAST                'num_order_functions'
              132  LOAD_CONST               1
              134  INPLACE_ADD      
              136  STORE_FAST               'num_order_functions'

 L.  75       138  LOAD_GLOBAL              _make_operator
              140  LOAD_STR                 'gt'
              142  LOAD_FAST                'gt'
              144  CALL_FUNCTION_2       2  ''
              146  LOAD_DEREF               'body'
              148  LOAD_STR                 '__gt__'
              150  STORE_SUBSCR     
            152_0  COME_FROM           128  '128'

 L.  77       152  LOAD_FAST                'ge'
              154  LOAD_CONST               None
              156  <117>                 1  ''
              158  POP_JUMP_IF_FALSE   182  'to 182'

 L.  78       160  LOAD_FAST                'num_order_functions'
              162  LOAD_CONST               1
              164  INPLACE_ADD      
              166  STORE_FAST               'num_order_functions'

 L.  79       168  LOAD_GLOBAL              _make_operator
              170  LOAD_STR                 'ge'
              172  LOAD_FAST                'ge'
              174  CALL_FUNCTION_2       2  ''
              176  LOAD_DEREF               'body'
              178  LOAD_STR                 '__ge__'
              180  STORE_SUBSCR     
            182_0  COME_FROM           158  '158'

 L.  81       182  LOAD_GLOBAL              new_class
              184  LOAD_FAST                'class_name'
              186  LOAD_GLOBAL              object
              188  BUILD_TUPLE_1         1 
              190  BUILD_MAP_0           0 
              192  LOAD_CLOSURE             'body'
              194  BUILD_TUPLE_1         1 
              196  LOAD_LAMBDA              '<code_object <lambda>>'
              198  LOAD_STR                 'cmp_using.<locals>.<lambda>'
              200  MAKE_FUNCTION_8          'closure'
              202  CALL_FUNCTION_4       4  ''
              204  STORE_FAST               'type_'

 L.  84       206  LOAD_FAST                'require_same_type'
              208  POP_JUMP_IF_FALSE   222  'to 222'

 L.  85       210  LOAD_FAST                'type_'
              212  LOAD_ATTR                _requirements
              214  LOAD_METHOD              append
              216  LOAD_GLOBAL              _check_same_type
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
            222_0  COME_FROM           208  '208'

 L.  88       222  LOAD_CONST               0
              224  LOAD_FAST                'num_order_functions'
              226  DUP_TOP          
              228  ROT_THREE        
              230  COMPARE_OP               <
              232  POP_JUMP_IF_FALSE   244  'to 244'
              234  LOAD_CONST               4
              236  COMPARE_OP               <
          238_240  POP_JUMP_IF_FALSE   272  'to 272'
              242  JUMP_FORWARD        248  'to 248'
            244_0  COME_FROM           232  '232'
              244  POP_TOP          
              246  JUMP_FORWARD        272  'to 272'
            248_0  COME_FROM           242  '242'

 L.  89       248  LOAD_FAST                'has_eq_function'
          250_252  POP_JUMP_IF_TRUE    262  'to 262'

 L.  92       254  LOAD_GLOBAL              ValueError

 L.  93       256  LOAD_STR                 'eq must be define is order to complete ordering from lt, le, gt, ge.'

 L.  92       258  CALL_FUNCTION_1       1  ''
              260  RAISE_VARARGS_1       1  'exception instance'
            262_0  COME_FROM           250  '250'

 L.  96       262  LOAD_GLOBAL              functools
              264  LOAD_METHOD              total_ordering
              266  LOAD_FAST                'type_'
              268  CALL_METHOD_1         1  ''
              270  STORE_FAST               'type_'
            272_0  COME_FROM           246  '246'
            272_1  COME_FROM           238  '238'

 L.  98       272  LOAD_FAST                'type_'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30


def _make_init():
    """
    Create __init__ method.
    """

    def __init__(self, value):
        """
        Initialize object with *value*.
        """
        self.value = value

    return __init__


def _make_operator(name, func):
    """
    Create operator method.
    """

    def method--- This code section failed: ---

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _is_comparable_to
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 122        10  LOAD_GLOBAL              NotImplemented
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 124        14  LOAD_DEREF               'func'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                value
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                value
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'result'

 L. 125        28  LOAD_FAST                'result'
               30  LOAD_GLOBAL              NotImplemented
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 126        36  LOAD_GLOBAL              NotImplemented
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 128        40  LOAD_FAST                'result'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    method.__name__ = '__%s__' % (name,)
    method.__doc__ = 'Return a %s b.  Computed by attrs.' % (
     _operation_names[name],)
    return method


def _is_comparable_to(self, other):
    """
    Check whether `other` is comparable to `self`.
    """
    for func in self._requirements:
        if not funcselfother:
            return False
    else:
        return True


def _check_same_type--- This code section failed: ---

 L. 152         0  LOAD_FAST                'other'
                2  LOAD_ATTR                value
                4  LOAD_ATTR                __class__
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                value
               10  LOAD_ATTR                __class__
               12  <117>                 0  ''
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1