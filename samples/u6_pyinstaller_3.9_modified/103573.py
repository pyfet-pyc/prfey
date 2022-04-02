# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\pytree.py
"""
Python parse tree definitions.

This is a very concrete parse tree; we need to keep every token and
even the comments and whitespace between tokens.

There's also a pattern matching implementation here.
"""
__author__ = 'Guido van Rossum <guido@python.org>'
import sys
from io import StringIO
HUGE = 2147483647
_type_reprs = {}

def type_repr(type_num):
    global _type_reprs
    if not _type_reprs:
        from .pygram import python_symbols
        for name, val in python_symbols.__dict__.items():
            if type(val) == int:
                _type_reprs[val] = name

    return _type_reprs.setdefault(type_num, type_num)


class Base(object):
    __doc__ = '\n    Abstract base class for Node and Leaf.\n\n    This provides some default functionality and boilerplate using the\n    template pattern.\n\n    A node may be a subnode of at most one parent.\n    '
    type = None
    parent = None
    children = ()
    was_changed = False
    was_checked = False

    def __new__--- This code section failed: ---

 L.  51         0  LOAD_FAST                'cls'
                2  LOAD_GLOBAL              Base
                4  <117>                 1  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'Cannot instantiate Base'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  52        16  LOAD_GLOBAL              object
               18  LOAD_METHOD              __new__
               20  LOAD_FAST                'cls'
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __eq__--- This code section failed: ---

 L.  60         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_FAST                'other'
                6  LOAD_ATTR                __class__
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L.  61        12  LOAD_GLOBAL              NotImplemented
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  62        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _eq
               20  LOAD_FAST                'other'
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    __hash__ = None

    def _eq(self, other):
        """
        Compare two nodes for equality.

        This is called by __eq__ and __ne__.  It is only called if the two nodes
        have the same type.  This must be implemented by the concrete subclass.
        Nodes should be considered equal if they have the same structure,
        ignoring the prefix string and other context information.
        """
        raise NotImplementedError

    def clone(self):
        """
        Return a cloned (deep) copy of self.

        This must be implemented by the concrete subclass.
        """
        raise NotImplementedError

    def post_order(self):
        """
        Return a post-order iterator for the tree.

        This must be implemented by the concrete subclass.
        """
        raise NotImplementedError

    def pre_order(self):
        """
        Return a pre-order iterator for the tree.

        This must be implemented by the concrete subclass.
        """
        raise NotImplementedError

    def replace--- This code section failed: ---

 L. 103         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     22  'to 22'
               10  <74>             
               12  LOAD_GLOBAL              str
               14  LOAD_FAST                'self'
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             8  '8'

 L. 104        22  LOAD_FAST                'new'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  <74>             
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L. 105        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'new'
               38  LOAD_GLOBAL              list
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_TRUE     50  'to 50'

 L. 106        44  LOAD_FAST                'new'
               46  BUILD_LIST_1          1 
               48  STORE_FAST               'new'
             50_0  COME_FROM            42  '42'

 L. 107        50  BUILD_LIST_0          0 
               52  STORE_FAST               'l_children'

 L. 108        54  LOAD_CONST               False
               56  STORE_FAST               'found'

 L. 109        58  LOAD_FAST                'self'
               60  LOAD_ATTR                parent
               62  LOAD_ATTR                children
               64  GET_ITER         
               66  FOR_ITER            136  'to 136'
               68  STORE_FAST               'ch'

 L. 110        70  LOAD_FAST                'ch'
               72  LOAD_FAST                'self'
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE   124  'to 124'

 L. 111        78  LOAD_FAST                'found'
               80  POP_JUMP_IF_FALSE   100  'to 100'
               82  <74>             
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                parent
               88  LOAD_ATTR                children
               90  LOAD_FAST                'self'
               92  LOAD_FAST                'new'
               94  BUILD_TUPLE_3         3 
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            80  '80'

 L. 112       100  LOAD_FAST                'new'
              102  LOAD_CONST               None
              104  <117>                 1  ''
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 113       108  LOAD_FAST                'l_children'
              110  LOAD_METHOD              extend
              112  LOAD_FAST                'new'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
            118_0  COME_FROM           106  '106'

 L. 114       118  LOAD_CONST               True
              120  STORE_FAST               'found'
              122  JUMP_BACK            66  'to 66'
            124_0  COME_FROM            76  '76'

 L. 116       124  LOAD_FAST                'l_children'
              126  LOAD_METHOD              append
              128  LOAD_FAST                'ch'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            66  'to 66'

 L. 117       136  LOAD_FAST                'found'
              138  POP_JUMP_IF_TRUE    156  'to 156'
              140  <74>             
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                children
              146  LOAD_FAST                'self'
              148  LOAD_FAST                'new'
              150  BUILD_TUPLE_3         3 
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           138  '138'

 L. 118       156  LOAD_FAST                'self'
              158  LOAD_ATTR                parent
              160  LOAD_METHOD              changed
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L. 119       166  LOAD_FAST                'l_children'
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                parent
              172  STORE_ATTR               children

 L. 120       174  LOAD_FAST                'new'
              176  GET_ITER         
              178  FOR_ITER            192  'to 192'
              180  STORE_FAST               'x'

 L. 121       182  LOAD_FAST                'self'
              184  LOAD_ATTR                parent
              186  LOAD_FAST                'x'
              188  STORE_ATTR               parent
              190  JUMP_BACK           178  'to 178'

 L. 122       192  LOAD_CONST               None
              194  LOAD_FAST                'self'
              196  STORE_ATTR               parent

Parse error at or near `None' instruction at offset -1

    def get_lineno(self):
        """Return the line number which generated the invocant node."""
        node = self
        while not isinstancenodeLeaf:
            if not node.children:
                return
                node = node.children[0]

        return node.lineno

    def changed(self):
        if self.parent:
            self.parent.changed()
        self.was_changed = True

    def remove--- This code section failed: ---

 L. 143         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  POP_JUMP_IF_FALSE    70  'to 70'

 L. 144         6  LOAD_GLOBAL              enumerate
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parent
               12  LOAD_ATTR                children
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
             18_0  COME_FROM            32  '32'
               18  FOR_ITER             70  'to 70'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'i'
               24  STORE_FAST               'node'

 L. 145        26  LOAD_FAST                'node'
               28  LOAD_FAST                'self'
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    18  'to 18'

 L. 146        34  LOAD_FAST                'self'
               36  LOAD_ATTR                parent
               38  LOAD_METHOD              changed
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          

 L. 147        44  LOAD_FAST                'self'
               46  LOAD_ATTR                parent
               48  LOAD_ATTR                children
               50  LOAD_FAST                'i'
               52  DELETE_SUBSCR    

 L. 148        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               parent

 L. 149        60  LOAD_FAST                'i'
               62  ROT_TWO          
               64  POP_TOP          
               66  RETURN_VALUE     
               68  JUMP_BACK            18  'to 18'
             70_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 30

    @property
    def next_sibling--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 158        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 161        14  LOAD_GLOBAL              enumerate
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                parent
               20  LOAD_ATTR                children
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
             26_0  COME_FROM            40  '40'
               26  FOR_ITER             90  'to 90'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'i'
               32  STORE_FAST               'child'

 L. 162        34  LOAD_FAST                'child'
               36  LOAD_FAST                'self'
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    26  'to 26'

 L. 163        42  SETUP_FINALLY        66  'to 66'

 L. 164        44  LOAD_FAST                'self'
               46  LOAD_ATTR                parent
               48  LOAD_ATTR                children
               50  LOAD_FAST                'i'
               52  LOAD_CONST               1
               54  BINARY_ADD       
               56  BINARY_SUBSCR    
               58  POP_BLOCK        
               60  ROT_TWO          
               62  POP_TOP          
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    42  '42'

 L. 165        66  DUP_TOP          
               68  LOAD_GLOBAL              IndexError
               70  <121>                86  ''
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 166        78  POP_EXCEPT       
               80  POP_TOP          
               82  LOAD_CONST               None
               84  RETURN_VALUE     
               86  <48>             
               88  JUMP_BACK            26  'to 26'

Parse error at or near `None' instruction at offset -1

    @property
    def prev_sibling--- This code section failed: ---

 L. 174         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 175        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 178        14  LOAD_GLOBAL              enumerate
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                parent
               20  LOAD_ATTR                children
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
             26_0  COME_FROM            40  '40'
               26  FOR_ITER             78  'to 78'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'i'
               32  STORE_FAST               'child'

 L. 179        34  LOAD_FAST                'child'
               36  LOAD_FAST                'self'
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    26  'to 26'

 L. 180        42  LOAD_FAST                'i'
               44  LOAD_CONST               0
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    56  'to 56'

 L. 181        50  POP_TOP          
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            48  '48'

 L. 182        56  LOAD_FAST                'self'
               58  LOAD_ATTR                parent
               60  LOAD_ATTR                children
               62  LOAD_FAST                'i'
               64  LOAD_CONST               1
               66  BINARY_SUBTRACT  
               68  BINARY_SUBSCR    
               70  ROT_TWO          
               72  POP_TOP          
               74  RETURN_VALUE     
               76  JUMP_BACK            26  'to 26'

Parse error at or near `None' instruction at offset -1

    def leaves(self):
        for child in self.children:
            (yield from child.leaves())

        if False:
            yield None

    def depth--- This code section failed: ---

 L. 189         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 190        10  LOAD_CONST               0
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 191        14  LOAD_CONST               1
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                parent
               20  LOAD_METHOD              depth
               22  CALL_METHOD_0         0  ''
               24  BINARY_ADD       
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def get_suffix--- This code section failed: ---

 L. 198         0  LOAD_FAST                'self'
                2  LOAD_ATTR                next_sibling
                4  STORE_FAST               'next_sib'

 L. 199         6  LOAD_FAST                'next_sib'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 200        14  LOAD_STR                 ''
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 201        18  LOAD_FAST                'next_sib'
               20  LOAD_ATTR                prefix
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    if sys.version_info < (3, 0):

        def __str__(self):
            return str(self).encode'ascii'


class Node(Base):
    __doc__ = 'Concrete implementation for interior nodes.'

    def __init__--- This code section failed: ---

 L. 223         0  LOAD_FAST                'type'
                2  LOAD_CONST               256
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_FAST                'type'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 224        16  LOAD_FAST                'type'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               type

 L. 225        22  LOAD_GLOBAL              list
               24  LOAD_FAST                'children'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_FAST                'self'
               30  STORE_ATTR               children

 L. 226        32  LOAD_FAST                'self'
               34  LOAD_ATTR                children
               36  GET_ITER         
               38  FOR_ITER             72  'to 72'
               40  STORE_FAST               'ch'

 L. 227        42  LOAD_FAST                'ch'
               44  LOAD_ATTR                parent
               46  LOAD_CONST               None
               48  <117>                 0  ''
               50  POP_JUMP_IF_TRUE     64  'to 64'
               52  <74>             
               54  LOAD_GLOBAL              repr
               56  LOAD_FAST                'ch'
               58  CALL_FUNCTION_1       1  ''
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            50  '50'

 L. 228        64  LOAD_FAST                'self'
               66  LOAD_FAST                'ch'
               68  STORE_ATTR               parent
               70  JUMP_BACK            38  'to 38'

 L. 229        72  LOAD_FAST                'prefix'
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_FALSE    86  'to 86'

 L. 230        80  LOAD_FAST                'prefix'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               prefix
             86_0  COME_FROM            78  '78'

 L. 231        86  LOAD_FAST                'fixers_applied'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 232        90  LOAD_FAST                'fixers_applied'
               92  LOAD_CONST               None
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'self'
              102  STORE_ATTR               fixers_applied
              104  JUMP_FORWARD        112  'to 112'
            106_0  COME_FROM            88  '88'

 L. 234       106  LOAD_CONST               None
              108  LOAD_FAST                'self'
              110  STORE_ATTR               fixers_applied
            112_0  COME_FROM           104  '104'

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        """Return a canonical string representation."""
        return '%s(%s, %r)' % (self.__class__.__name__,
         type_repr(self.type),
         self.children)

    def __unicode__(self):
        """
        Return a pretty string representation.

        This reproduces the input source exactly.
        """
        return ''.joinmapstrself.children

    if sys.version_info > (3, 0):
        __str__ = __unicode__

    def _eq(self, other):
        """Compare two nodes for equality."""
        return (
         self.type, self.children) == (other.type, other.children)

    def clone(self):
        """Return a cloned (deep) copy of self."""
        return Node((self.type), [ch.clone() for ch in self.children], fixers_applied=(self.fixers_applied))

    def post_order(self):
        """Return a post-order iterator for the tree."""
        for child in self.children:
            (yield from child.post_order())
        else:
            (yield self)

    def pre_order(self):
        """Return a pre-order iterator for the tree."""
        (yield self)
        for child in self.children:
            (yield from child.pre_order())

    @property
    def prefix(self):
        """
        The whitespace and comments preceding this node in the input.
        """
        if not self.children:
            return ''
        return self.children[0].prefix

    @prefix.setter
    def prefix(self, prefix):
        if self.children:
            self.children[0].prefix = prefix

    def set_child(self, i, child):
        """
        Equivalent to 'node.children[i] = child'. This method also sets the
        child's parent attribute appropriately.
        """
        child.parent = self
        self.children[i].parent = None
        self.children[i] = child
        self.changed()

    def insert_child(self, i, child):
        """
        Equivalent to 'node.children.insert(i, child)'. This method also sets
        the child's parent attribute appropriately.
        """
        child.parent = self
        self.children.insert(i, child)
        self.changed()

    def append_child(self, child):
        """
        Equivalent to 'node.children.append(child)'. This method also sets the
        child's parent attribute appropriately.
        """
        child.parent = self
        self.children.appendchild
        self.changed()


class Leaf(Base):
    __doc__ = 'Concrete implementation for leaf nodes.'
    _prefix = ''
    lineno = 0
    column = 0

    def __init__--- This code section failed: ---

 L. 336         0  LOAD_CONST               0
                2  LOAD_FAST                'type'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_CONST               256
               14  COMPARE_OP               <
               16  POP_JUMP_IF_TRUE     30  'to 30'
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM            10  '10'
               20  POP_TOP          
             22_0  COME_FROM            18  '18'
               22  <74>             
               24  LOAD_FAST                'type'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L. 337        30  LOAD_FAST                'context'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    56  'to 56'

 L. 338        38  LOAD_FAST                'context'
               40  UNPACK_SEQUENCE_2     2 
               42  LOAD_FAST                'self'
               44  STORE_ATTR               _prefix
               46  UNPACK_SEQUENCE_2     2 
               48  LOAD_FAST                'self'
               50  STORE_ATTR               lineno
               52  LOAD_FAST                'self'
               54  STORE_ATTR               column
             56_0  COME_FROM            36  '36'

 L. 339        56  LOAD_FAST                'type'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               type

 L. 340        62  LOAD_FAST                'value'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               value

 L. 341        68  LOAD_FAST                'prefix'
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    82  'to 82'

 L. 342        76  LOAD_FAST                'prefix'
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _prefix
             82_0  COME_FROM            74  '74'

 L. 343        82  LOAD_FAST                'fixers_applied'
               84  LOAD_CONST               None
               86  LOAD_CONST               None
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'self'
               94  STORE_ATTR               fixers_applied

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        """Return a canonical string representation."""
        return '%s(%r, %r)' % (self.__class__.__name__,
         self.type,
         self.value)

    def __unicode__(self):
        """
        Return a pretty string representation.

        This reproduces the input source exactly.
        """
        return self.prefix + str(self.value)

    if sys.version_info > (3, 0):
        __str__ = __unicode__

    def _eq(self, other):
        """Compare two nodes for equality."""
        return (
         self.type, self.value) == (other.type, other.value)

    def clone(self):
        """Return a cloned (deep) copy of self."""
        return Leaf((self.type), (self.value), (
         self.prefix, (self.lineno, self.column)),
          fixers_applied=(self.fixers_applied))

    def leaves(self):
        (yield self)

    def post_order(self):
        """Return a post-order iterator for the tree."""
        (yield self)

    def pre_order(self):
        """Return a pre-order iterator for the tree."""
        (yield self)

    @property
    def prefix(self):
        """
        The whitespace and comments preceding this token in the input.
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self.changed()
        self._prefix = prefix


def convert--- This code section failed: ---

 L. 403         0  LOAD_FAST                'raw_node'
                2  UNPACK_SEQUENCE_4     4 
                4  STORE_FAST               'type'
                6  STORE_FAST               'value'
                8  STORE_FAST               'context'
               10  STORE_FAST               'children'

 L. 404        12  LOAD_FAST                'children'
               14  POP_JUMP_IF_TRUE     26  'to 26'
               16  LOAD_FAST                'type'
               18  LOAD_FAST                'gr'
               20  LOAD_ATTR                number2symbol
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    60  'to 60'
             26_0  COME_FROM            14  '14'

 L. 407        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'children'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               1
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 408        38  LOAD_FAST                'children'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  RETURN_VALUE     
             46_0  COME_FROM            36  '36'

 L. 409        46  LOAD_GLOBAL              Node
               48  LOAD_FAST                'type'
               50  LOAD_FAST                'children'
               52  LOAD_FAST                'context'
               54  LOAD_CONST               ('context',)
               56  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               58  RETURN_VALUE     
             60_0  COME_FROM            24  '24'

 L. 411        60  LOAD_GLOBAL              Leaf
               62  LOAD_FAST                'type'
               64  LOAD_FAST                'value'
               66  LOAD_FAST                'context'
               68  LOAD_CONST               ('context',)
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 22


class BasePattern(object):
    __doc__ = '\n    A pattern is a tree matching pattern.\n\n    It looks for a specific node type (token or symbol), and\n    optionally for a specific content.\n\n    This is an abstract base class.  There are three concrete\n    subclasses:\n\n    - LeafPattern matches a single leaf node;\n    - NodePattern matches a single node (usually non-leaf);\n    - WildcardPattern matches a sequence of nodes of variable length.\n    '
    type = None
    content = None
    name = None

    def __new__--- This code section failed: ---

 L. 437         0  LOAD_FAST                'cls'
                2  LOAD_GLOBAL              BasePattern
                4  <117>                 1  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'Cannot instantiate BasePattern'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 438        16  LOAD_GLOBAL              object
               18  LOAD_METHOD              __new__
               20  LOAD_FAST                'cls'
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __repr__--- This code section failed: ---

 L. 441         0  LOAD_GLOBAL              type_repr
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                type
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                content
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                name
               16  BUILD_LIST_3          3 
               18  STORE_FAST               'args'

 L. 442        20  LOAD_FAST                'args'
               22  POP_JUMP_IF_FALSE    44  'to 44'
               24  LOAD_FAST                'args'
               26  LOAD_CONST               -1
               28  BINARY_SUBSCR    
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 443        36  LOAD_FAST                'args'
               38  LOAD_CONST               -1
               40  DELETE_SUBSCR    
               42  JUMP_BACK            20  'to 20'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            22  '22'

 L. 444        44  LOAD_STR                 '%s(%s)'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                __class__
               50  LOAD_ATTR                __name__
               52  LOAD_STR                 ', '
               54  LOAD_METHOD              join
               56  LOAD_GLOBAL              map
               58  LOAD_GLOBAL              repr
               60  LOAD_FAST                'args'
               62  CALL_FUNCTION_2       2  ''
               64  CALL_METHOD_1         1  ''
               66  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    def optimize(self):
        """
        A subclass can define this as a hook for optimizations.

        Returns either self or another node with the same effect.
        """
        return self

    def match--- This code section failed: ---

 L. 465         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'
               10  LOAD_FAST                'node'
               12  LOAD_ATTR                type
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                type
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 466        22  LOAD_CONST               False
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'
             26_1  COME_FROM             8  '8'

 L. 467        26  LOAD_FAST                'self'
               28  LOAD_ATTR                content
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    82  'to 82'

 L. 468        36  LOAD_CONST               None
               38  STORE_FAST               'r'

 L. 469        40  LOAD_FAST                'results'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 470        48  BUILD_MAP_0           0 
               50  STORE_FAST               'r'
             52_0  COME_FROM            46  '46'

 L. 471        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _submatch
               56  LOAD_FAST                'node'
               58  LOAD_FAST                'r'
               60  CALL_METHOD_2         2  ''
               62  POP_JUMP_IF_TRUE     68  'to 68'

 L. 472        64  LOAD_CONST               False
               66  RETURN_VALUE     
             68_0  COME_FROM            62  '62'

 L. 473        68  LOAD_FAST                'r'
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L. 474        72  LOAD_FAST                'results'
               74  LOAD_METHOD              update
               76  LOAD_FAST                'r'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            70  '70'
             82_1  COME_FROM            34  '34'

 L. 475        82  LOAD_FAST                'results'
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   106  'to 106'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                name
               94  POP_JUMP_IF_FALSE   106  'to 106'

 L. 476        96  LOAD_FAST                'node'
               98  LOAD_FAST                'results'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                name
              104  STORE_SUBSCR     
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            88  '88'

 L. 477       106  LOAD_CONST               True
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def match_seq(self, nodes, results=None):
        """
        Does this pattern exactly match a sequence of nodes?

        Default implementation for non-wildcard patterns.
        """
        if len(nodes) != 1:
            return False
        return self.match(nodes[0], results)

    def generate_matches(self, nodes):
        """
        Generator yielding all matches for this pattern.

        Default implementation for non-wildcard patterns.
        """
        r = {}
        if nodes:
            if self.match(nodes[0], r):
                (yield (
                 1, r))


class LeafPattern(BasePattern):

    def __init__--- This code section failed: ---

 L. 514         0  LOAD_FAST                'type'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    38  'to 38'

 L. 515         8  LOAD_CONST               0
               10  LOAD_FAST                'type'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               <=
               18  POP_JUMP_IF_FALSE    28  'to 28'
               20  LOAD_CONST               256
               22  COMPARE_OP               <
               24  POP_JUMP_IF_TRUE     38  'to 38'
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            18  '18'
               28  POP_TOP          
             30_0  COME_FROM            26  '26'
               30  <74>             
               32  LOAD_FAST                'type'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            24  '24'
             38_1  COME_FROM             6  '6'

 L. 516        38  LOAD_FAST                'content'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    68  'to 68'

 L. 517        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'content'
               50  LOAD_GLOBAL              str
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     68  'to 68'
               56  <74>             
               58  LOAD_GLOBAL              repr
               60  LOAD_FAST                'content'
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            54  '54'
             68_1  COME_FROM            44  '44'

 L. 518        68  LOAD_FAST                'type'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               type

 L. 519        74  LOAD_FAST                'content'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               content

 L. 520        80  LOAD_FAST                'name'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               name

Parse error at or near `None' instruction at offset -1

    def match(self, node, results=None):
        """Override match() to insist on a leaf node."""
        if not isinstancenodeLeaf:
            return False
        return BasePattern.match(self, node, results)

    def _submatch(self, node, results=None):
        """
        Match the pattern's content to the node's children.

        This assumes the node type matches and self.content is not None.

        Returns True if it matches, False if not.

        If results is not None, it must be a dict which will be
        updated with the nodes matching named subpatterns.

        When returning False, the results dict may still be updated.
        """
        return self.content == node.value


class NodePattern(BasePattern):
    wildcards = False

    def __init__--- This code section failed: ---

 L. 564         0  LOAD_FAST                'type'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 565         8  LOAD_FAST                'type'
               10  LOAD_CONST               256
               12  COMPARE_OP               >=
               14  POP_JUMP_IF_TRUE     24  'to 24'
               16  <74>             
               18  LOAD_FAST                'type'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 566        24  LOAD_FAST                'content'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE   118  'to 118'

 L. 567        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'content'
               36  LOAD_GLOBAL              str
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  <74>             
               44  LOAD_GLOBAL              repr
               46  LOAD_FAST                'content'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            40  '40'

 L. 568        54  LOAD_GLOBAL              list
               56  LOAD_FAST                'content'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'content'

 L. 569        62  LOAD_GLOBAL              enumerate
               64  LOAD_FAST                'content'
               66  CALL_FUNCTION_1       1  ''
               68  GET_ITER         
             70_0  COME_FROM           108  '108'
               70  FOR_ITER            118  'to 118'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'i'
               76  STORE_FAST               'item'

 L. 570        78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'item'
               82  LOAD_GLOBAL              BasePattern
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_TRUE    100  'to 100'
               88  <74>             
               90  LOAD_FAST                'i'
               92  LOAD_FAST                'item'
               94  BUILD_TUPLE_2         2 
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            86  '86'

 L. 571       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'item'
              104  LOAD_GLOBAL              WildcardPattern
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_FALSE    70  'to 70'

 L. 572       110  LOAD_CONST               True
              112  LOAD_FAST                'self'
              114  STORE_ATTR               wildcards
              116  JUMP_BACK            70  'to 70'
            118_0  COME_FROM            30  '30'

 L. 573       118  LOAD_FAST                'type'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               type

 L. 574       124  LOAD_FAST                'content'
              126  LOAD_FAST                'self'
              128  STORE_ATTR               content

 L. 575       130  LOAD_FAST                'name'
              132  LOAD_FAST                'self'
              134  STORE_ATTR               name

Parse error at or near `None' instruction at offset -1

    def _submatch--- This code section failed: ---

 L. 590         0  LOAD_FAST                'self'
                2  LOAD_ATTR                wildcards
                4  POP_JUMP_IF_FALSE    72  'to 72'

 L. 591         6  LOAD_GLOBAL              generate_matches
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                content
               12  LOAD_FAST                'node'
               14  LOAD_ATTR                children
               16  CALL_FUNCTION_2       2  ''
               18  GET_ITER         
             20_0  COME_FROM            40  '40'
               20  FOR_ITER             68  'to 68'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'c'
               26  STORE_FAST               'r'

 L. 592        28  LOAD_FAST                'c'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'node'
               34  LOAD_ATTR                children
               36  CALL_FUNCTION_1       1  ''
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    20  'to 20'

 L. 593        42  LOAD_FAST                'results'
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 594        50  LOAD_FAST                'results'
               52  LOAD_METHOD              update
               54  LOAD_FAST                'r'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            48  '48'

 L. 595        60  POP_TOP          
               62  LOAD_CONST               True
               64  RETURN_VALUE     
               66  JUMP_BACK            20  'to 20'

 L. 596        68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM             4  '4'

 L. 597        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                content
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'node'
               84  LOAD_ATTR                children
               86  CALL_FUNCTION_1       1  ''
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE    96  'to 96'

 L. 598        92  LOAD_CONST               False
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'

 L. 599        96  LOAD_GLOBAL              zip
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                content
              102  LOAD_FAST                'node'
              104  LOAD_ATTR                children
              106  CALL_FUNCTION_2       2  ''
              108  GET_ITER         
            110_0  COME_FROM           128  '128'
              110  FOR_ITER            138  'to 138'
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'subpattern'
              116  STORE_FAST               'child'

 L. 600       118  LOAD_FAST                'subpattern'
              120  LOAD_METHOD              match
              122  LOAD_FAST                'child'
              124  LOAD_FAST                'results'
              126  CALL_METHOD_2         2  ''
              128  POP_JUMP_IF_TRUE    110  'to 110'

 L. 601       130  POP_TOP          
              132  LOAD_CONST               False
              134  RETURN_VALUE     
              136  JUMP_BACK           110  'to 110'

 L. 602       138  LOAD_CONST               True
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46


class WildcardPattern(BasePattern):
    __doc__ = '\n    A wildcard pattern can match zero or more nodes.\n\n    This has all the flexibility needed to implement patterns like:\n\n    .*      .+      .?      .{m,n}\n    (a b c | d e | f)\n    (...)*  (...)+  (...)?  (...){m,n}\n\n    except it always uses non-greedy matching.\n    '

    def __init__--- This code section failed: ---

 L. 642         0  LOAD_CONST               0
                2  LOAD_FAST                'min'
                4  DUP_TOP          
                6  ROT_THREE        
                8  COMPARE_OP               <=
               10  POP_JUMP_IF_FALSE    30  'to 30'
               12  LOAD_FAST                'max'
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               <=
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_GLOBAL              HUGE
               24  COMPARE_OP               <=
               26  POP_JUMP_IF_TRUE     44  'to 44'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            10  '10'
               30  POP_TOP          
             32_0  COME_FROM            28  '28'
               32  <74>             
               34  LOAD_FAST                'min'
               36  LOAD_FAST                'max'
               38  BUILD_TUPLE_2         2 
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            26  '26'

 L. 643        44  LOAD_FAST                'content'
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_FALSE   116  'to 116'

 L. 644        52  LOAD_GLOBAL              tuple
               54  LOAD_GLOBAL              map
               56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'content'
               60  CALL_FUNCTION_2       2  ''
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'content'

 L. 646        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'content'
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_TRUE     86  'to 86'
               74  <74>             
               76  LOAD_GLOBAL              repr
               78  LOAD_FAST                'content'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            72  '72'

 L. 647        86  LOAD_FAST                'content'
               88  GET_ITER         
             90_0  COME_FROM           100  '100'
               90  FOR_ITER            116  'to 116'
               92  STORE_FAST               'alt'

 L. 648        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'alt'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_TRUE     90  'to 90'
              102  <74>             
              104  LOAD_GLOBAL              repr
              106  LOAD_FAST                'alt'
              108  CALL_FUNCTION_1       1  ''
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  JUMP_BACK            90  'to 90'
            116_0  COME_FROM            50  '50'

 L. 649       116  LOAD_FAST                'content'
              118  LOAD_FAST                'self'
              120  STORE_ATTR               content

 L. 650       122  LOAD_FAST                'min'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               min

 L. 651       128  LOAD_FAST                'max'
              130  LOAD_FAST                'self'
              132  STORE_ATTR               max

 L. 652       134  LOAD_FAST                'name'
              136  LOAD_FAST                'self'
              138  STORE_ATTR               name

Parse error at or near `None' instruction at offset -1

    def optimize--- This code section failed: ---

 L. 656         0  LOAD_CONST               None
                2  STORE_FAST               'subpattern'

 L. 657         4  LOAD_FAST                'self'
                6  LOAD_ATTR                content
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    60  'to 60'

 L. 658        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                content
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_CONST               1
               24  COMPARE_OP               ==

 L. 657        26  POP_JUMP_IF_FALSE    60  'to 60'

 L. 658        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                content
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               1
               42  COMPARE_OP               ==

 L. 657        44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 659        46  LOAD_FAST                'self'
               48  LOAD_ATTR                content
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  STORE_FAST               'subpattern'
             60_0  COME_FROM            44  '44'
             60_1  COME_FROM            26  '26'
             60_2  COME_FROM            12  '12'

 L. 660        60  LOAD_FAST                'self'
               62  LOAD_ATTR                min
               64  LOAD_CONST               1
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   130  'to 130'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                max
               74  LOAD_CONST               1
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   130  'to 130'

 L. 661        80  LOAD_FAST                'self'
               82  LOAD_ATTR                content
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L. 662        90  LOAD_GLOBAL              NodePattern
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                name
               96  LOAD_CONST               ('name',)
               98  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              100  RETURN_VALUE     
            102_0  COME_FROM            88  '88'

 L. 663       102  LOAD_FAST                'subpattern'
              104  LOAD_CONST               None
              106  <117>                 1  ''
              108  POP_JUMP_IF_FALSE   130  'to 130'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                name
              114  LOAD_FAST                'subpattern'
              116  LOAD_ATTR                name
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 664       122  LOAD_FAST                'subpattern'
              124  LOAD_METHOD              optimize
              126  CALL_METHOD_0         0  ''
              128  RETURN_VALUE     
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM           108  '108'
            130_2  COME_FROM            78  '78'
            130_3  COME_FROM            68  '68'

 L. 665       130  LOAD_FAST                'self'
              132  LOAD_ATTR                min
              134  LOAD_CONST               1
              136  COMPARE_OP               <=
              138  POP_JUMP_IF_FALSE   206  'to 206'
              140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'subpattern'
              144  LOAD_GLOBAL              WildcardPattern
              146  CALL_FUNCTION_2       2  ''
              148  POP_JUMP_IF_FALSE   206  'to 206'

 L. 666       150  LOAD_FAST                'subpattern'
              152  LOAD_ATTR                min
              154  LOAD_CONST               1
              156  COMPARE_OP               <=

 L. 665       158  POP_JUMP_IF_FALSE   206  'to 206'

 L. 666       160  LOAD_FAST                'self'
              162  LOAD_ATTR                name
              164  LOAD_FAST                'subpattern'
              166  LOAD_ATTR                name
              168  COMPARE_OP               ==

 L. 665       170  POP_JUMP_IF_FALSE   206  'to 206'

 L. 667       172  LOAD_GLOBAL              WildcardPattern
              174  LOAD_FAST                'subpattern'
              176  LOAD_ATTR                content

 L. 668       178  LOAD_FAST                'self'
              180  LOAD_ATTR                min
              182  LOAD_FAST                'subpattern'
              184  LOAD_ATTR                min
              186  BINARY_MULTIPLY  

 L. 669       188  LOAD_FAST                'self'
              190  LOAD_ATTR                max
              192  LOAD_FAST                'subpattern'
              194  LOAD_ATTR                max
              196  BINARY_MULTIPLY  

 L. 670       198  LOAD_FAST                'subpattern'
              200  LOAD_ATTR                name

 L. 667       202  CALL_FUNCTION_4       4  ''
              204  RETURN_VALUE     
            206_0  COME_FROM           170  '170'
            206_1  COME_FROM           158  '158'
            206_2  COME_FROM           148  '148'
            206_3  COME_FROM           138  '138'

 L. 671       206  LOAD_FAST                'self'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def match(self, node, results=None):
        """Does this pattern exactly match a node?"""
        return self.match_seq([node], results)

    def match_seq--- This code section failed: ---

 L. 679         0  LOAD_FAST                'self'
                2  LOAD_METHOD              generate_matches
                4  LOAD_FAST                'nodes'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            28  '28'
               10  FOR_ITER             76  'to 76'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'c'
               16  STORE_FAST               'r'

 L. 680        18  LOAD_FAST                'c'
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'nodes'
               24  CALL_FUNCTION_1       1  ''
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    10  'to 10'

 L. 681        30  LOAD_FAST                'results'
               32  LOAD_CONST               None
               34  <117>                 1  ''
               36  POP_JUMP_IF_FALSE    68  'to 68'

 L. 682        38  LOAD_FAST                'results'
               40  LOAD_METHOD              update
               42  LOAD_FAST                'r'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 683        48  LOAD_FAST                'self'
               50  LOAD_ATTR                name
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L. 684        54  LOAD_GLOBAL              list
               56  LOAD_FAST                'nodes'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'results'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                name
               66  STORE_SUBSCR     
             68_0  COME_FROM            52  '52'
             68_1  COME_FROM            36  '36'

 L. 685        68  POP_TOP          
               70  LOAD_CONST               True
               72  RETURN_VALUE     
               74  JUMP_BACK            10  'to 10'

 L. 686        76  LOAD_CONST               False
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 34

    def generate_matches--- This code section failed: ---

 L. 700         0  LOAD_FAST                'self'
                2  LOAD_ATTR                content
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    84  'to 84'

 L. 702        10  LOAD_GLOBAL              range
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                min
               16  LOAD_CONST               1
               18  LOAD_GLOBAL              min
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'nodes'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                max
               30  CALL_FUNCTION_2       2  ''
               32  BINARY_ADD       
               34  CALL_FUNCTION_2       2  ''
               36  GET_ITER         
               38  FOR_ITER             82  'to 82'
               40  STORE_FAST               'count'

 L. 703        42  BUILD_MAP_0           0 
               44  STORE_FAST               'r'

 L. 704        46  LOAD_FAST                'self'
               48  LOAD_ATTR                name
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L. 705        52  LOAD_FAST                'nodes'
               54  LOAD_CONST               None
               56  LOAD_FAST                'count'
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'r'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                name
               68  STORE_SUBSCR     
             70_0  COME_FROM            50  '50'

 L. 706        70  LOAD_FAST                'count'
               72  LOAD_FAST                'r'
               74  BUILD_TUPLE_2         2 
               76  YIELD_VALUE      
               78  POP_TOP          
               80  JUMP_BACK            38  'to 38'
               82  JUMP_FORWARD        312  'to 312'
             84_0  COME_FROM             8  '8'

 L. 707        84  LOAD_FAST                'self'
               86  LOAD_ATTR                name
               88  LOAD_STR                 'bare_name'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   108  'to 108'

 L. 708        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _bare_name_matches
               98  LOAD_FAST                'nodes'
              100  CALL_METHOD_1         1  ''
              102  YIELD_VALUE      
              104  POP_TOP          
              106  JUMP_FORWARD        312  'to 312'
            108_0  COME_FROM            92  '92'

 L. 714       108  LOAD_GLOBAL              hasattr
              110  LOAD_GLOBAL              sys
              112  LOAD_STR                 'getrefcount'
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   132  'to 132'

 L. 715       118  LOAD_GLOBAL              sys
              120  LOAD_ATTR                stderr
              122  STORE_FAST               'save_stderr'

 L. 716       124  LOAD_GLOBAL              StringIO
              126  CALL_FUNCTION_0       0  ''
              128  LOAD_GLOBAL              sys
              130  STORE_ATTR               stderr
            132_0  COME_FROM           116  '116'

 L. 717       132  SETUP_FINALLY       292  'to 292'
              134  SETUP_FINALLY       196  'to 196'

 L. 718       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _recursive_matches
              140  LOAD_FAST                'nodes'
              142  LOAD_CONST               0
              144  CALL_METHOD_2         2  ''
              146  GET_ITER         
              148  FOR_ITER            192  'to 192'
              150  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'count'
              154  STORE_FAST               'r'

 L. 719       156  LOAD_FAST                'self'
              158  LOAD_ATTR                name
              160  POP_JUMP_IF_FALSE   180  'to 180'

 L. 720       162  LOAD_FAST                'nodes'
              164  LOAD_CONST               None
              166  LOAD_FAST                'count'
              168  BUILD_SLICE_2         2 
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'r'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                name
              178  STORE_SUBSCR     
            180_0  COME_FROM           160  '160'

 L. 721       180  LOAD_FAST                'count'
              182  LOAD_FAST                'r'
              184  BUILD_TUPLE_2         2 
              186  YIELD_VALUE      
              188  POP_TOP          
              190  JUMP_BACK           148  'to 148'
              192  POP_BLOCK        
              194  JUMP_FORWARD        270  'to 270'
            196_0  COME_FROM_FINALLY   134  '134'

 L. 722       196  DUP_TOP          
              198  LOAD_GLOBAL              RuntimeError
          200_202  <121>               268  ''
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 725       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _iterative_matches
              214  LOAD_FAST                'nodes'
              216  CALL_METHOD_1         1  ''
              218  GET_ITER         
              220  FOR_ITER            264  'to 264'
              222  UNPACK_SEQUENCE_2     2 
              224  STORE_FAST               'count'
              226  STORE_FAST               'r'

 L. 726       228  LOAD_FAST                'self'
              230  LOAD_ATTR                name
              232  POP_JUMP_IF_FALSE   252  'to 252'

 L. 727       234  LOAD_FAST                'nodes'
              236  LOAD_CONST               None
              238  LOAD_FAST                'count'
              240  BUILD_SLICE_2         2 
              242  BINARY_SUBSCR    
              244  LOAD_FAST                'r'
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                name
              250  STORE_SUBSCR     
            252_0  COME_FROM           232  '232'

 L. 728       252  LOAD_FAST                'count'
              254  LOAD_FAST                'r'
              256  BUILD_TUPLE_2         2 
              258  YIELD_VALUE      
              260  POP_TOP          
              262  JUMP_BACK           220  'to 220'
              264  POP_EXCEPT       
              266  JUMP_FORWARD        270  'to 270'
              268  <48>             
            270_0  COME_FROM           266  '266'
            270_1  COME_FROM           194  '194'
              270  POP_BLOCK        

 L. 730       272  LOAD_GLOBAL              hasattr
              274  LOAD_GLOBAL              sys
              276  LOAD_STR                 'getrefcount'
              278  CALL_FUNCTION_2       2  ''
          280_282  POP_JUMP_IF_FALSE   312  'to 312'

 L. 731       284  LOAD_FAST                'save_stderr'
              286  LOAD_GLOBAL              sys
              288  STORE_ATTR               stderr
              290  JUMP_FORWARD        312  'to 312'
            292_0  COME_FROM_FINALLY   132  '132'

 L. 730       292  LOAD_GLOBAL              hasattr
              294  LOAD_GLOBAL              sys
              296  LOAD_STR                 'getrefcount'
              298  CALL_FUNCTION_2       2  ''
          300_302  POP_JUMP_IF_FALSE   310  'to 310'

 L. 731       304  LOAD_FAST                'save_stderr'
              306  LOAD_GLOBAL              sys
              308  STORE_ATTR               stderr
            310_0  COME_FROM           300  '300'
              310  <48>             
            312_0  COME_FROM           290  '290'
            312_1  COME_FROM           280  '280'
            312_2  COME_FROM           106  '106'
            312_3  COME_FROM            82  '82'

Parse error at or near `None' instruction at offset -1

    def _iterative_matches(self, nodes):
        """Helper to iteratively yield the matches."""
        nodelen = len(nodes)
        if 0 >= self.min:
            (yield (
             0, {}))
        results = []
        for alt in self.content:
            for c, r in generate_matchesaltnodes:
                (yield (
                 c, r))
                results.append(c, r)

        else:
            while results:
                new_results = []
                for c0, r0 in results:
                    if c0 < nodelen and c0 <= self.max:
                        for alt in self.content:
                            for c1, r1 in generate_matchesaltnodes[c0:]:
                                if c1 > 0:
                                    r = {}
                                    r.updater0
                                    r.updater1
                                    (yield (c0 + c1, r))
                                    new_results.append(c0 + c1, r)
                            else:
                                results = new_results

    def _bare_name_matches--- This code section failed: ---

 L. 764         0  LOAD_CONST               0
                2  STORE_FAST               'count'

 L. 765         4  BUILD_MAP_0           0 
                6  STORE_FAST               'r'

 L. 766         8  LOAD_CONST               False
               10  STORE_FAST               'done'

 L. 767        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'nodes'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'max'

 L. 768        20  LOAD_FAST                'done'
               22  POP_JUMP_IF_TRUE     86  'to 86'
               24  LOAD_FAST                'count'
               26  LOAD_FAST                'max'
               28  COMPARE_OP               <
               30  POP_JUMP_IF_FALSE    86  'to 86'

 L. 769        32  LOAD_CONST               True
               34  STORE_FAST               'done'

 L. 770        36  LOAD_FAST                'self'
               38  LOAD_ATTR                content
               40  GET_ITER         
             42_0  COME_FROM            64  '64'
               42  FOR_ITER             84  'to 84'
               44  STORE_FAST               'leaf'

 L. 771        46  LOAD_FAST                'leaf'
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  LOAD_METHOD              match
               54  LOAD_FAST                'nodes'
               56  LOAD_FAST                'count'
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'r'
               62  CALL_METHOD_2         2  ''
               64  POP_JUMP_IF_FALSE    42  'to 42'

 L. 772        66  LOAD_FAST                'count'
               68  LOAD_CONST               1
               70  INPLACE_ADD      
               72  STORE_FAST               'count'

 L. 773        74  LOAD_CONST               False
               76  STORE_FAST               'done'

 L. 774        78  POP_TOP          
               80  CONTINUE             20  'to 20'
               82  JUMP_BACK            42  'to 42'
               84  JUMP_BACK            20  'to 20'
             86_0  COME_FROM            30  '30'
             86_1  COME_FROM            22  '22'

 L. 775        86  LOAD_FAST                'nodes'
               88  LOAD_CONST               None
               90  LOAD_FAST                'count'
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'r'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                name
              102  STORE_SUBSCR     

 L. 776       104  LOAD_FAST                'count'
              106  LOAD_FAST                'r'
              108  BUILD_TUPLE_2         2 
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 80

    def _recursive_matches--- This code section failed: ---

 L. 780         0  LOAD_FAST                'self'
                2  LOAD_ATTR                content
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 781        14  LOAD_FAST                'count'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                min
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 782        24  LOAD_CONST               0
               26  BUILD_MAP_0           0 
               28  BUILD_TUPLE_2         2 
               30  YIELD_VALUE      
               32  POP_TOP          
             34_0  COME_FROM            22  '22'

 L. 783        34  LOAD_FAST                'count'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                max
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE   148  'to 148'

 L. 784        44  LOAD_FAST                'self'
               46  LOAD_ATTR                content
               48  GET_ITER         
               50  FOR_ITER            148  'to 148'
               52  STORE_FAST               'alt'

 L. 785        54  LOAD_GLOBAL              generate_matches
               56  LOAD_FAST                'alt'
               58  LOAD_FAST                'nodes'
               60  CALL_FUNCTION_2       2  ''
               62  GET_ITER         
               64  FOR_ITER            146  'to 146'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'c0'
               70  STORE_FAST               'r0'

 L. 786        72  LOAD_FAST                'self'
               74  LOAD_METHOD              _recursive_matches
               76  LOAD_FAST                'nodes'
               78  LOAD_FAST                'c0'
               80  LOAD_CONST               None
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'count'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  CALL_METHOD_2         2  ''
               94  GET_ITER         
               96  FOR_ITER            144  'to 144'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'c1'
              102  STORE_FAST               'r1'

 L. 787       104  BUILD_MAP_0           0 
              106  STORE_FAST               'r'

 L. 788       108  LOAD_FAST                'r'
              110  LOAD_METHOD              update
              112  LOAD_FAST                'r0'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 789       118  LOAD_FAST                'r'
              120  LOAD_METHOD              update
              122  LOAD_FAST                'r1'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 790       128  LOAD_FAST                'c0'
              130  LOAD_FAST                'c1'
              132  BINARY_ADD       
              134  LOAD_FAST                'r'
              136  BUILD_TUPLE_2         2 
              138  YIELD_VALUE      
              140  POP_TOP          
              142  JUMP_BACK            96  'to 96'
              144  JUMP_BACK            64  'to 64'
              146  JUMP_BACK            50  'to 50'
            148_0  COME_FROM            42  '42'

Parse error at or near `None' instruction at offset -1


class NegatedPattern(BasePattern):

    def __init__--- This code section failed: ---

 L. 804         0  LOAD_FAST                'content'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L. 805         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'content'
               12  LOAD_GLOBAL              BasePattern
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     30  'to 30'
               18  <74>             
               20  LOAD_GLOBAL              repr
               22  LOAD_FAST                'content'
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'
             30_1  COME_FROM             6  '6'

 L. 806        30  LOAD_FAST                'content'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               content

Parse error at or near `None' instruction at offset -1

    def match(self, node):
        return False

    def match_seq(self, nodes):
        return len(nodes) == 0

    def generate_matches--- This code section failed: ---

 L. 817         0  LOAD_FAST                'self'
                2  LOAD_ATTR                content
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 819        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'nodes'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    70  'to 70'

 L. 820        22  LOAD_CONST               0
               24  BUILD_MAP_0           0 
               26  BUILD_TUPLE_2         2 
               28  YIELD_VALUE      
               30  POP_TOP          
               32  JUMP_FORWARD         70  'to 70'
             34_0  COME_FROM             8  '8'

 L. 823        34  LOAD_FAST                'self'
               36  LOAD_ATTR                content
               38  LOAD_METHOD              generate_matches
               40  LOAD_FAST                'nodes'
               42  CALL_METHOD_1         1  ''
               44  GET_ITER         
               46  FOR_ITER             60  'to 60'
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'c'
               52  STORE_FAST               'r'

 L. 824        54  POP_TOP          
               56  LOAD_CONST               None
               58  RETURN_VALUE     

 L. 825        60  LOAD_CONST               0
               62  BUILD_MAP_0           0 
               64  BUILD_TUPLE_2         2 
               66  YIELD_VALUE      
               68  POP_TOP          
             70_0  COME_FROM            32  '32'
             70_1  COME_FROM            20  '20'

Parse error at or near `None' instruction at offset -1


def generate_matches(patterns, nodes):
    """
    Generator yielding matches for a sequence of patterns and nodes.

    Args:
        patterns: a sequence of patterns
        nodes: a sequence of nodes

    Yields:
        (count, results) tuples where:
        count: the entire sequence of patterns matches nodes[:count];
        results: dict containing named submatches.
        """
    if not patterns:
        (yield (
         0, {}))
    else:
        p, rest = patterns[0], patterns[1:]
    for c0, r0 in p.generate_matchesnodes:
        if not rest:
            (yield (
             c0, r0))
        else:
            for c1, r1 in generate_matchesrestnodes[c0:]:
                r = {}
                r.updater0
                r.updater1
                (yield (c0 + c1, r))