# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pycparser\c_ast.py
import sys

def _repr(obj):
    """
    Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return '[' + ',\n '.join((_repr(e).replace('\n', '\n ') for e in obj)) + '\n]'
    return repr(obj)


class Node(object):
    __slots__ = ()

    def __repr__(self):
        """ Generates a python representation of the current node
        """
        result = self.__class__.__name__ + '('
        indent = ''
        separator = ''
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + _repr(getattr(self, name)).replace('\n', '\n  ' + ' ' * (len(name) + len(self.__class__.__name__)))
            separator = ','
            indent = '\n ' + ' ' * len(self.__class__.__name__)
        else:
            result += indent + ')'
            return result

    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show--- This code section failed: ---

 L.  80         0  LOAD_STR                 ' '
                2  LOAD_FAST                'offset'
                4  BINARY_MULTIPLY  
                6  STORE_FAST               'lead'

 L.  81         8  LOAD_FAST                'nodenames'
               10  POP_JUMP_IF_FALSE    52  'to 52'
               12  LOAD_FAST                '_my_node_name'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    52  'to 52'

 L.  82        20  LOAD_FAST                'buf'
               22  LOAD_METHOD              write
               24  LOAD_FAST                'lead'
               26  LOAD_DEREF               'self'
               28  LOAD_ATTR                __class__
               30  LOAD_ATTR                __name__
               32  BINARY_ADD       
               34  LOAD_STR                 ' <'
               36  BINARY_ADD       
               38  LOAD_FAST                '_my_node_name'
               40  BINARY_ADD       
               42  LOAD_STR                 '>: '
               44  BINARY_ADD       
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM            18  '18'
             52_1  COME_FROM            10  '10'

 L.  84        52  LOAD_FAST                'buf'
               54  LOAD_METHOD              write
               56  LOAD_FAST                'lead'
               58  LOAD_DEREF               'self'
               60  LOAD_ATTR                __class__
               62  LOAD_ATTR                __name__
               64  BINARY_ADD       
               66  LOAD_STR                 ': '
               68  BINARY_ADD       
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            50  '50'

 L.  86        74  LOAD_DEREF               'self'
               76  LOAD_ATTR                attr_names
               78  POP_JUMP_IF_FALSE   176  'to 176'

 L.  87        80  LOAD_FAST                'attrnames'
               82  POP_JUMP_IF_FALSE   126  'to 126'

 L.  88        84  LOAD_CLOSURE             'self'
               86  BUILD_TUPLE_1         1 
               88  LOAD_LISTCOMP            '<code_object <listcomp>>'
               90  LOAD_STR                 'Node.show.<locals>.<listcomp>'
               92  MAKE_FUNCTION_8          'closure'
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                attr_names
               98  GET_ITER         
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'nvlist'

 L.  89       104  LOAD_STR                 ', '
              106  LOAD_METHOD              join
              108  LOAD_GENEXPR             '<code_object <genexpr>>'
              110  LOAD_STR                 'Node.show.<locals>.<genexpr>'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  LOAD_FAST                'nvlist'
              116  GET_ITER         
              118  CALL_FUNCTION_1       1  ''
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'attrstr'
              124  JUMP_FORWARD        166  'to 166'
            126_0  COME_FROM            82  '82'

 L.  91       126  LOAD_CLOSURE             'self'
              128  BUILD_TUPLE_1         1 
              130  LOAD_LISTCOMP            '<code_object <listcomp>>'
              132  LOAD_STR                 'Node.show.<locals>.<listcomp>'
              134  MAKE_FUNCTION_8          'closure'
              136  LOAD_DEREF               'self'
              138  LOAD_ATTR                attr_names
              140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'vlist'

 L.  92       146  LOAD_STR                 ', '
              148  LOAD_METHOD              join
              150  LOAD_GENEXPR             '<code_object <genexpr>>'
              152  LOAD_STR                 'Node.show.<locals>.<genexpr>'
              154  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              156  LOAD_FAST                'vlist'
              158  GET_ITER         
              160  CALL_FUNCTION_1       1  ''
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'attrstr'
            166_0  COME_FROM           124  '124'

 L.  93       166  LOAD_FAST                'buf'
              168  LOAD_METHOD              write
              170  LOAD_FAST                'attrstr'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
            176_0  COME_FROM            78  '78'

 L.  95       176  LOAD_FAST                'showcoord'
              178  POP_JUMP_IF_FALSE   196  'to 196'

 L.  96       180  LOAD_FAST                'buf'
              182  LOAD_METHOD              write
              184  LOAD_STR                 ' (at %s)'
              186  LOAD_DEREF               'self'
              188  LOAD_ATTR                coord
              190  BINARY_MODULO    
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
            196_0  COME_FROM           178  '178'

 L.  97       196  LOAD_FAST                'buf'
              198  LOAD_METHOD              write
              200  LOAD_STR                 '\n'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L.  99       206  LOAD_DEREF               'self'
              208  LOAD_METHOD              children
              210  CALL_METHOD_0         0  ''
              212  GET_ITER         
              214  FOR_ITER            250  'to 250'
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'child_name'
              220  STORE_FAST               'child'

 L. 100       222  LOAD_FAST                'child'
              224  LOAD_ATTR                show

 L. 101       226  LOAD_FAST                'buf'

 L. 102       228  LOAD_FAST                'offset'
              230  LOAD_CONST               2
              232  BINARY_ADD       

 L. 103       234  LOAD_FAST                'attrnames'

 L. 104       236  LOAD_FAST                'nodenames'

 L. 105       238  LOAD_FAST                'showcoord'

 L. 106       240  LOAD_FAST                'child_name'

 L. 100       242  LOAD_CONST               ('offset', 'attrnames', 'nodenames', 'showcoord', '_my_node_name')
              244  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              246  POP_TOP          
              248  JUMP_BACK           214  'to 214'

Parse error at or near `<117>' instruction at offset 16


class NodeVisitor(object):
    __doc__ = " A base NodeVisitor class for visiting c_ast nodes.\n        Subclass it and define your own visit_XXX methods, where\n        XXX is the class name you want to visit with these\n        methods.\n\n        For example:\n\n        class ConstantVisitor(NodeVisitor):\n            def __init__(self):\n                self.values = []\n\n            def visit_Constant(self, node):\n                self.values.append(node.value)\n\n        Creates a list of values of all the constant nodes\n        encountered below the given node. To use it:\n\n        cv = ConstantVisitor()\n        cv.visit(node)\n\n        Notes:\n\n        *   generic_visit() will be called for AST nodes for which\n            no visit_XXX method was defined.\n        *   The children of nodes for which a visit_XXX was\n            defined will not be visited - if you need this, call\n            generic_visit() on the node.\n            You can use:\n                NodeVisitor.generic_visit(self, node)\n        *   Modeled after Python's own AST visiting facilities\n            (the ast module of Python 3.0)\n    "
    _method_cache = None

    def visit--- This code section failed: ---

 L. 149         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _method_cache
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 150        10  BUILD_MAP_0           0 
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _method_cache
             16_0  COME_FROM             8  '8'

 L. 152        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _method_cache
               20  LOAD_METHOD              get
               22  LOAD_FAST                'node'
               24  LOAD_ATTR                __class__
               26  LOAD_ATTR                __name__
               28  LOAD_CONST               None
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'visitor'

 L. 153        34  LOAD_FAST                'visitor'
               36  LOAD_CONST               None
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    82  'to 82'

 L. 154        42  LOAD_STR                 'visit_'
               44  LOAD_FAST                'node'
               46  LOAD_ATTR                __class__
               48  LOAD_ATTR                __name__
               50  BINARY_ADD       
               52  STORE_FAST               'method'

 L. 155        54  LOAD_GLOBAL              getattr
               56  LOAD_FAST                'self'
               58  LOAD_FAST                'method'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                generic_visit
               64  CALL_FUNCTION_3       3  ''
               66  STORE_FAST               'visitor'

 L. 156        68  LOAD_FAST                'visitor'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _method_cache
               74  LOAD_FAST                'node'
               76  LOAD_ATTR                __class__
               78  LOAD_ATTR                __name__
               80  STORE_SUBSCR     
             82_0  COME_FROM            40  '40'

 L. 158        82  LOAD_FAST                'visitor'
               84  LOAD_FAST                'node'
               86  CALL_FUNCTION_1       1  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node:
            self.visit(c)


class ArrayDecl(Node):
    __slots__ = ('type', 'dim', 'dim_quals', 'coord', '__weakref__')

    def __init__(self, type, dim, dim_quals, coord=None):
        self.type = type
        self.dim = dim
        self.dim_quals = dim_quals
        self.coord = coord

    def children--- This code section failed: ---

 L. 176         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 177         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 178        30  LOAD_FAST                'self'
               32  LOAD_ATTR                dim
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'dim'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                dim
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 179        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 182         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 183        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 184        18  LOAD_FAST                'self'
               20  LOAD_ATTR                dim
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 185        28  LOAD_FAST                'self'
               30  LOAD_ATTR                dim
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ('dim_quals', )


class ArrayRef(Node):
    __slots__ = ('name', 'subscript', 'coord', '__weakref__')

    def __init__(self, name, subscript, coord=None):
        self.name = name
        self.subscript = subscript
        self.coord = coord

    def children--- This code section failed: ---

 L. 197         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 198         4  LOAD_FAST                'self'
                6  LOAD_ATTR                name
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'name'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                name
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 199        30  LOAD_FAST                'self'
               32  LOAD_ATTR                subscript
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'subscript'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                subscript
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 200        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 203         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 204        10  LOAD_FAST                'self'
               12  LOAD_ATTR                name
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 205        18  LOAD_FAST                'self'
               20  LOAD_ATTR                subscript
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 206        28  LOAD_FAST                'self'
               30  LOAD_ATTR                subscript
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Assignment(Node):
    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')

    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord

    def children--- This code section failed: ---

 L. 219         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 220         4  LOAD_FAST                'self'
                6  LOAD_ATTR                lvalue
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'lvalue'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                lvalue
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 221        30  LOAD_FAST                'self'
               32  LOAD_ATTR                rvalue
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'rvalue'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                rvalue
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 222        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lvalue
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 226        10  LOAD_FAST                'self'
               12  LOAD_ATTR                lvalue
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 227        18  LOAD_FAST                'self'
               20  LOAD_ATTR                rvalue
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 228        28  LOAD_FAST                'self'
               30  LOAD_ATTR                rvalue
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ('op', )


class BinaryOp(Node):
    __slots__ = ('op', 'left', 'right', 'coord', '__weakref__')

    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children--- This code section failed: ---

 L. 241         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 242         4  LOAD_FAST                'self'
                6  LOAD_ATTR                left
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'left'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                left
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 243        30  LOAD_FAST                'self'
               32  LOAD_ATTR                right
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'right'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                right
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 244        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 247         0  LOAD_FAST                'self'
                2  LOAD_ATTR                left
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 248        10  LOAD_FAST                'self'
               12  LOAD_ATTR                left
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 249        18  LOAD_FAST                'self'
               20  LOAD_ATTR                right
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 250        28  LOAD_FAST                'self'
               30  LOAD_ATTR                right
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ('op', )


class Break(Node):
    __slots__ = ('coord', '__weakref__')

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ()


class Case(Node):
    __slots__ = ('expr', 'stmts', 'coord', '__weakref__')

    def __init__(self, expr, stmts, coord=None):
        self.expr = expr
        self.stmts = stmts
        self.coord = coord

    def children--- This code section failed: ---

 L. 276         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 277         4  LOAD_FAST                'self'
                6  LOAD_ATTR                expr
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'expr'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                expr
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 278        30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                stmts
               36  JUMP_IF_TRUE_OR_POP    40  'to 40'
               38  BUILD_LIST_0          0 
             40_0  COME_FROM            36  '36'
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
               44  FOR_ITER             72  'to 72'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'i'
               50  STORE_FAST               'child'

 L. 279        52  LOAD_FAST                'nodelist'
               54  LOAD_METHOD              append
               56  LOAD_STR                 'stmts[%d]'
               58  LOAD_FAST                'i'
               60  BINARY_MODULO    
               62  LOAD_FAST                'child'
               64  BUILD_TUPLE_2         2 
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_BACK            44  'to 44'

 L. 280        72  LOAD_GLOBAL              tuple
               74  LOAD_FAST                'nodelist'
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 283         0  LOAD_FAST                'self'
                2  LOAD_ATTR                expr
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 284        10  LOAD_FAST                'self'
               12  LOAD_ATTR                expr
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 285        18  LOAD_FAST                'self'
               20  LOAD_ATTR                stmts
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_LIST_0          0 
             26_0  COME_FROM            22  '22'
               26  GET_ITER         
               28  FOR_ITER             40  'to 40'
               30  STORE_FAST               'child'

 L. 286        32  LOAD_FAST                'child'
               34  YIELD_VALUE      
               36  POP_TOP          
               38  JUMP_BACK            28  'to 28'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Cast(Node):
    __slots__ = ('to_type', 'expr', 'coord', '__weakref__')

    def __init__(self, to_type, expr, coord=None):
        self.to_type = to_type
        self.expr = expr
        self.coord = coord

    def children--- This code section failed: ---

 L. 298         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 299         4  LOAD_FAST                'self'
                6  LOAD_ATTR                to_type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'to_type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                to_type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 300        30  LOAD_FAST                'self'
               32  LOAD_ATTR                expr
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'expr'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                expr
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 301        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 304         0  LOAD_FAST                'self'
                2  LOAD_ATTR                to_type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 305        10  LOAD_FAST                'self'
               12  LOAD_ATTR                to_type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 306        18  LOAD_FAST                'self'
               20  LOAD_ATTR                expr
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 307        28  LOAD_FAST                'self'
               30  LOAD_ATTR                expr
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Compound(Node):
    __slots__ = ('block_items', 'coord', '__weakref__')

    def __init__(self, block_items, coord=None):
        self.block_items = block_items
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.block_items or []):
            nodelist.append(('block_items[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.block_items or []:
            (yield child)

    attr_names = ()


class CompoundLiteral(Node):
    __slots__ = ('type', 'init', 'coord', '__weakref__')

    def __init__(self, type, init, coord=None):
        self.type = type
        self.init = init
        self.coord = coord

    def children--- This code section failed: ---

 L. 337         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 338         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 339        30  LOAD_FAST                'self'
               32  LOAD_ATTR                init
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'init'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                init
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 340        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 343         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 344        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 345        18  LOAD_FAST                'self'
               20  LOAD_ATTR                init
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 346        28  LOAD_FAST                'self'
               30  LOAD_ATTR                init
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Constant(Node):
    __slots__ = ('type', 'value', 'coord', '__weakref__')

    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ('type', 'value')


class Continue(Node):
    __slots__ = ('coord', '__weakref__')

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ()


class Decl(Node):
    __slots__ = ('name', 'quals', 'storage', 'funcspec', 'type', 'init', 'bitsize',
                 'coord', '__weakref__')

    def __init__(self, name, quals, storage, funcspec, type, init, bitsize, coord=None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.funcspec = funcspec
        self.type = type
        self.init = init
        self.bitsize = bitsize
        self.coord = coord

    def children--- This code section failed: ---

 L. 394         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 395         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 396        30  LOAD_FAST                'self'
               32  LOAD_ATTR                init
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'init'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                init
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 397        56  LOAD_FAST                'self'
               58  LOAD_ATTR                bitsize
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  LOAD_FAST                'nodelist'
               68  LOAD_METHOD              append
               70  LOAD_STR                 'bitsize'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                bitsize
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

 L. 398        82  LOAD_GLOBAL              tuple
               84  LOAD_FAST                'nodelist'
               86  CALL_FUNCTION_1       1  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 401         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 402        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 403        18  LOAD_FAST                'self'
               20  LOAD_ATTR                init
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 404        28  LOAD_FAST                'self'
               30  LOAD_ATTR                init
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

 L. 405        36  LOAD_FAST                'self'
               38  LOAD_ATTR                bitsize
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 406        46  LOAD_FAST                'self'
               48  LOAD_ATTR                bitsize
               50  YIELD_VALUE      
               52  POP_TOP          
             54_0  COME_FROM            44  '44'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', 'quals', 'storage', 'funcspec')


class DeclList(Node):
    __slots__ = ('decls', 'coord', '__weakref__')

    def __init__(self, decls, coord=None):
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(('decls[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.decls or []:
            (yield child)

    attr_names = ()


class Default(Node):
    __slots__ = ('stmts', 'coord', '__weakref__')

    def __init__(self, stmts, coord=None):
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.stmts or []):
            nodelist.append(('stmts[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.stmts or []:
            (yield child)

    attr_names = ()


class DoWhile(Node):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')

    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children--- This code section failed: ---

 L. 454         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 455         4  LOAD_FAST                'self'
                6  LOAD_ATTR                cond
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'cond'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                cond
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 456        30  LOAD_FAST                'self'
               32  LOAD_ATTR                stmt
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'stmt'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                stmt
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 457        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 460         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cond
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 461        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cond
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 462        18  LOAD_FAST                'self'
               20  LOAD_ATTR                stmt
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 463        28  LOAD_FAST                'self'
               30  LOAD_ATTR                stmt
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class EllipsisParam(Node):
    __slots__ = ('coord', '__weakref__')

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ()


class EmptyStatement(Node):
    __slots__ = ('coord', '__weakref__')

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ()


class Enum(Node):
    __slots__ = ('name', 'values', 'coord', '__weakref__')

    def __init__(self, name, values, coord=None):
        self.name = name
        self.values = values
        self.coord = coord

    def children--- This code section failed: ---

 L. 503         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 504         4  LOAD_FAST                'self'
                6  LOAD_ATTR                values
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'values'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                values
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 505        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 508         0  LOAD_FAST                'self'
                2  LOAD_ATTR                values
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 509        10  LOAD_FAST                'self'
               12  LOAD_ATTR                values
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', )


class Enumerator(Node):
    __slots__ = ('name', 'value', 'coord', '__weakref__')

    def __init__(self, name, value, coord=None):
        self.name = name
        self.value = value
        self.coord = coord

    def children--- This code section failed: ---

 L. 521         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 522         4  LOAD_FAST                'self'
                6  LOAD_ATTR                value
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'value'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                value
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 523        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 526         0  LOAD_FAST                'self'
                2  LOAD_ATTR                value
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 527        10  LOAD_FAST                'self'
               12  LOAD_ATTR                value
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', )


class EnumeratorList(Node):
    __slots__ = ('enumerators', 'coord', '__weakref__')

    def __init__(self, enumerators, coord=None):
        self.enumerators = enumerators
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.enumerators or []):
            nodelist.append(('enumerators[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.enumerators or []:
            (yield child)

    attr_names = ()


class ExprList(Node):
    __slots__ = ('exprs', 'coord', '__weakref__')

    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(('exprs[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.exprs or []:
            (yield child)

    attr_names = ()


class FileAST(Node):
    __slots__ = ('ext', 'coord', '__weakref__')

    def __init__(self, ext, coord=None):
        self.ext = ext
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.ext or []):
            nodelist.append(('ext[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.ext or []:
            (yield child)

    attr_names = ()


class For(Node):
    __slots__ = ('init', 'cond', 'next', 'stmt', 'coord', '__weakref__')

    def __init__(self, init, cond, next, stmt, coord=None):
        self.init = init
        self.cond = cond
        self.next = next
        self.stmt = stmt
        self.coord = coord

    def children--- This code section failed: ---

 L. 595         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 596         4  LOAD_FAST                'self'
                6  LOAD_ATTR                init
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'init'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                init
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 597        30  LOAD_FAST                'self'
               32  LOAD_ATTR                cond
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'cond'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                cond
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 598        56  LOAD_FAST                'self'
               58  LOAD_ATTR                next
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  LOAD_FAST                'nodelist'
               68  LOAD_METHOD              append
               70  LOAD_STR                 'next'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                next
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

 L. 599        82  LOAD_FAST                'self'
               84  LOAD_ATTR                stmt
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   108  'to 108'
               92  LOAD_FAST                'nodelist'
               94  LOAD_METHOD              append
               96  LOAD_STR                 'stmt'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                stmt
              102  BUILD_TUPLE_2         2 
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            90  '90'

 L. 600       108  LOAD_GLOBAL              tuple
              110  LOAD_FAST                'nodelist'
              112  CALL_FUNCTION_1       1  ''
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 603         0  LOAD_FAST                'self'
                2  LOAD_ATTR                init
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 604        10  LOAD_FAST                'self'
               12  LOAD_ATTR                init
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 605        18  LOAD_FAST                'self'
               20  LOAD_ATTR                cond
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 606        28  LOAD_FAST                'self'
               30  LOAD_ATTR                cond
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

 L. 607        36  LOAD_FAST                'self'
               38  LOAD_ATTR                next
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 608        46  LOAD_FAST                'self'
               48  LOAD_ATTR                next
               50  YIELD_VALUE      
               52  POP_TOP          
             54_0  COME_FROM            44  '44'

 L. 609        54  LOAD_FAST                'self'
               56  LOAD_ATTR                stmt
               58  LOAD_CONST               None
               60  <117>                 1  ''
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 610        64  LOAD_FAST                'self'
               66  LOAD_ATTR                stmt
               68  YIELD_VALUE      
               70  POP_TOP          
             72_0  COME_FROM            62  '62'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class FuncCall(Node):
    __slots__ = ('name', 'args', 'coord', '__weakref__')

    def __init__(self, name, args, coord=None):
        self.name = name
        self.args = args
        self.coord = coord

    def children--- This code section failed: ---

 L. 622         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 623         4  LOAD_FAST                'self'
                6  LOAD_ATTR                name
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'name'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                name
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 624        30  LOAD_FAST                'self'
               32  LOAD_ATTR                args
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'args'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                args
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 625        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 628         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 629        10  LOAD_FAST                'self'
               12  LOAD_ATTR                name
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 630        18  LOAD_FAST                'self'
               20  LOAD_ATTR                args
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 631        28  LOAD_FAST                'self'
               30  LOAD_ATTR                args
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class FuncDecl(Node):
    __slots__ = ('args', 'type', 'coord', '__weakref__')

    def __init__(self, args, type, coord=None):
        self.args = args
        self.type = type
        self.coord = coord

    def children--- This code section failed: ---

 L. 643         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 644         4  LOAD_FAST                'self'
                6  LOAD_ATTR                args
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'args'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                args
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 645        30  LOAD_FAST                'self'
               32  LOAD_ATTR                type
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'type'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                type
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 646        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 649         0  LOAD_FAST                'self'
                2  LOAD_ATTR                args
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 650        10  LOAD_FAST                'self'
               12  LOAD_ATTR                args
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 651        18  LOAD_FAST                'self'
               20  LOAD_ATTR                type
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 652        28  LOAD_FAST                'self'
               30  LOAD_ATTR                type
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class FuncDef(Node):
    __slots__ = ('decl', 'param_decls', 'body', 'coord', '__weakref__')

    def __init__(self, decl, param_decls, body, coord=None):
        self.decl = decl
        self.param_decls = param_decls
        self.body = body
        self.coord = coord

    def children--- This code section failed: ---

 L. 665         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 666         4  LOAD_FAST                'self'
                6  LOAD_ATTR                decl
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'decl'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                decl
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 667        30  LOAD_FAST                'self'
               32  LOAD_ATTR                body
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'body'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                body
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 668        56  LOAD_GLOBAL              enumerate
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                param_decls
               62  JUMP_IF_TRUE_OR_POP    66  'to 66'
               64  BUILD_LIST_0          0 
             66_0  COME_FROM            62  '62'
               66  CALL_FUNCTION_1       1  ''
               68  GET_ITER         
               70  FOR_ITER             98  'to 98'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'i'
               76  STORE_FAST               'child'

 L. 669        78  LOAD_FAST                'nodelist'
               80  LOAD_METHOD              append
               82  LOAD_STR                 'param_decls[%d]'
               84  LOAD_FAST                'i'
               86  BINARY_MODULO    
               88  LOAD_FAST                'child'
               90  BUILD_TUPLE_2         2 
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  JUMP_BACK            70  'to 70'

 L. 670        98  LOAD_GLOBAL              tuple
              100  LOAD_FAST                'nodelist'
              102  CALL_FUNCTION_1       1  ''
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 673         0  LOAD_FAST                'self'
                2  LOAD_ATTR                decl
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 674        10  LOAD_FAST                'self'
               12  LOAD_ATTR                decl
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 675        18  LOAD_FAST                'self'
               20  LOAD_ATTR                body
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 676        28  LOAD_FAST                'self'
               30  LOAD_ATTR                body
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

 L. 677        36  LOAD_FAST                'self'
               38  LOAD_ATTR                param_decls
               40  JUMP_IF_TRUE_OR_POP    44  'to 44'
               42  BUILD_LIST_0          0 
             44_0  COME_FROM            40  '40'
               44  GET_ITER         
               46  FOR_ITER             58  'to 58'
               48  STORE_FAST               'child'

 L. 678        50  LOAD_FAST                'child'
               52  YIELD_VALUE      
               54  POP_TOP          
               56  JUMP_BACK            46  'to 46'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Goto(Node):
    __slots__ = ('name', 'coord', '__weakref__')

    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ('name', )


class ID(Node):
    __slots__ = ('name', 'coord', '__weakref__')

    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ('name', )


class IdentifierType(Node):
    __slots__ = ('names', 'coord', '__weakref__')

    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ('names', )


class If(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')

    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children--- This code section failed: ---

 L. 739         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 740         4  LOAD_FAST                'self'
                6  LOAD_ATTR                cond
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'cond'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                cond
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 741        30  LOAD_FAST                'self'
               32  LOAD_ATTR                iftrue
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'iftrue'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                iftrue
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 742        56  LOAD_FAST                'self'
               58  LOAD_ATTR                iffalse
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  LOAD_FAST                'nodelist'
               68  LOAD_METHOD              append
               70  LOAD_STR                 'iffalse'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                iffalse
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

 L. 743        82  LOAD_GLOBAL              tuple
               84  LOAD_FAST                'nodelist'
               86  CALL_FUNCTION_1       1  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 746         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cond
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 747        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cond
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 748        18  LOAD_FAST                'self'
               20  LOAD_ATTR                iftrue
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 749        28  LOAD_FAST                'self'
               30  LOAD_ATTR                iftrue
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

 L. 750        36  LOAD_FAST                'self'
               38  LOAD_ATTR                iffalse
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 751        46  LOAD_FAST                'self'
               48  LOAD_ATTR                iffalse
               50  YIELD_VALUE      
               52  POP_TOP          
             54_0  COME_FROM            44  '44'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class InitList(Node):
    __slots__ = ('exprs', 'coord', '__weakref__')

    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(('exprs[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.exprs or []:
            (yield child)

    attr_names = ()


class Label(Node):
    __slots__ = ('name', 'stmt', 'coord', '__weakref__')

    def __init__(self, name, stmt, coord=None):
        self.name = name
        self.stmt = stmt
        self.coord = coord

    def children--- This code section failed: ---

 L. 781         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 782         4  LOAD_FAST                'self'
                6  LOAD_ATTR                stmt
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'stmt'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                stmt
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 783        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 786         0  LOAD_FAST                'self'
                2  LOAD_ATTR                stmt
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 787        10  LOAD_FAST                'self'
               12  LOAD_ATTR                stmt
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', )


class NamedInitializer(Node):
    __slots__ = ('name', 'expr', 'coord', '__weakref__')

    def __init__(self, name, expr, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord

    def children--- This code section failed: ---

 L. 799         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 800         4  LOAD_FAST                'self'
                6  LOAD_ATTR                expr
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'expr'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                expr
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 801        30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                name
               36  JUMP_IF_TRUE_OR_POP    40  'to 40'
               38  BUILD_LIST_0          0 
             40_0  COME_FROM            36  '36'
               40  CALL_FUNCTION_1       1  ''
               42  GET_ITER         
               44  FOR_ITER             72  'to 72'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'i'
               50  STORE_FAST               'child'

 L. 802        52  LOAD_FAST                'nodelist'
               54  LOAD_METHOD              append
               56  LOAD_STR                 'name[%d]'
               58  LOAD_FAST                'i'
               60  BINARY_MODULO    
               62  LOAD_FAST                'child'
               64  BUILD_TUPLE_2         2 
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_BACK            44  'to 44'

 L. 803        72  LOAD_GLOBAL              tuple
               74  LOAD_FAST                'nodelist'
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 806         0  LOAD_FAST                'self'
                2  LOAD_ATTR                expr
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 807        10  LOAD_FAST                'self'
               12  LOAD_ATTR                expr
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 808        18  LOAD_FAST                'self'
               20  LOAD_ATTR                name
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_LIST_0          0 
             26_0  COME_FROM            22  '22'
               26  GET_ITER         
               28  FOR_ITER             40  'to 40'
               30  STORE_FAST               'child'

 L. 809        32  LOAD_FAST                'child'
               34  YIELD_VALUE      
               36  POP_TOP          
               38  JUMP_BACK            28  'to 28'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class ParamList(Node):
    __slots__ = ('params', 'coord', '__weakref__')

    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(('params[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.params or []:
            (yield child)

    attr_names = ()


class PtrDecl(Node):
    __slots__ = ('quals', 'type', 'coord', '__weakref__')

    def __init__(self, quals, type, coord=None):
        self.quals = quals
        self.type = type
        self.coord = coord

    def children--- This code section failed: ---

 L. 839         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 840         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 841        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 844         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 845        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('quals', )


class Return(Node):
    __slots__ = ('expr', 'coord', '__weakref__')

    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children--- This code section failed: ---

 L. 856         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 857         4  LOAD_FAST                'self'
                6  LOAD_ATTR                expr
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'expr'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                expr
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 858        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 861         0  LOAD_FAST                'self'
                2  LOAD_ATTR                expr
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 862        10  LOAD_FAST                'self'
               12  LOAD_ATTR                expr
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Struct(Node):
    __slots__ = ('name', 'decls', 'coord', '__weakref__')

    def __init__(self, name, decls, coord=None):
        self.name = name
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(('decls[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.decls or []:
            (yield child)

    attr_names = ('name', )


class StructRef(Node):
    __slots__ = ('name', 'type', 'field', 'coord', '__weakref__')

    def __init__(self, name, type, field, coord=None):
        self.name = name
        self.type = type
        self.field = field
        self.coord = coord

    def children--- This code section failed: ---

 L. 894         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 895         4  LOAD_FAST                'self'
                6  LOAD_ATTR                name
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'name'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                name
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 896        30  LOAD_FAST                'self'
               32  LOAD_ATTR                field
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'field'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                field
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 897        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 900         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 901        10  LOAD_FAST                'self'
               12  LOAD_ATTR                name
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 902        18  LOAD_FAST                'self'
               20  LOAD_ATTR                field
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 903        28  LOAD_FAST                'self'
               30  LOAD_ATTR                field
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ('type', )


class Switch(Node):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')

    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children--- This code section failed: ---

 L. 915         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 916         4  LOAD_FAST                'self'
                6  LOAD_ATTR                cond
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'cond'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                cond
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 917        30  LOAD_FAST                'self'
               32  LOAD_ATTR                stmt
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'stmt'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                stmt
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 918        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 921         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cond
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 922        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cond
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 923        18  LOAD_FAST                'self'
               20  LOAD_ATTR                stmt
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 924        28  LOAD_FAST                'self'
               30  LOAD_ATTR                stmt
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class TernaryOp(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')

    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children--- This code section failed: ---

 L. 937         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 938         4  LOAD_FAST                'self'
                6  LOAD_ATTR                cond
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'cond'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                cond
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 939        30  LOAD_FAST                'self'
               32  LOAD_ATTR                iftrue
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'iftrue'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                iftrue
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L. 940        56  LOAD_FAST                'self'
               58  LOAD_ATTR                iffalse
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  LOAD_FAST                'nodelist'
               68  LOAD_METHOD              append
               70  LOAD_STR                 'iffalse'
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                iffalse
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

 L. 941        82  LOAD_GLOBAL              tuple
               84  LOAD_FAST                'nodelist'
               86  CALL_FUNCTION_1       1  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 944         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cond
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 945        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cond
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L. 946        18  LOAD_FAST                'self'
               20  LOAD_ATTR                iftrue
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 947        28  LOAD_FAST                'self'
               30  LOAD_ATTR                iftrue
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

 L. 948        36  LOAD_FAST                'self'
               38  LOAD_ATTR                iffalse
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 949        46  LOAD_FAST                'self'
               48  LOAD_ATTR                iffalse
               50  YIELD_VALUE      
               52  POP_TOP          
             54_0  COME_FROM            44  '44'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class TypeDecl(Node):
    __slots__ = ('declname', 'quals', 'type', 'coord', '__weakref__')

    def __init__(self, declname, quals, type, coord=None):
        self.declname = declname
        self.quals = quals
        self.type = type
        self.coord = coord

    def children--- This code section failed: ---

 L. 962         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 963         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 964        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 967         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 968        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('declname', 'quals')


class Typedef(Node):
    __slots__ = ('name', 'quals', 'storage', 'type', 'coord', '__weakref__')

    def __init__(self, name, quals, storage, type, coord=None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.type = type
        self.coord = coord

    def children--- This code section failed: ---

 L. 982         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L. 983         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L. 984        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L. 987         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 988        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', 'quals', 'storage')


class Typename(Node):
    __slots__ = ('name', 'quals', 'type', 'coord', '__weakref__')

    def __init__(self, name, quals, type, coord=None):
        self.name = name
        self.quals = quals
        self.type = type
        self.coord = coord

    def children--- This code section failed: ---

 L.1001         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L.1002         4  LOAD_FAST                'self'
                6  LOAD_ATTR                type
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'type'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                type
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L.1003        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L.1006         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1007        10  LOAD_FAST                'self'
               12  LOAD_ATTR                type
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('name', 'quals')


class UnaryOp(Node):
    __slots__ = ('op', 'expr', 'coord', '__weakref__')

    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children--- This code section failed: ---

 L.1019         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L.1020         4  LOAD_FAST                'self'
                6  LOAD_ATTR                expr
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'expr'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                expr
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L.1021        30  LOAD_GLOBAL              tuple
               32  LOAD_FAST                'nodelist'
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L.1024         0  LOAD_FAST                'self'
                2  LOAD_ATTR                expr
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1025        10  LOAD_FAST                'self'
               12  LOAD_ATTR                expr
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    attr_names = ('op', )


class Union(Node):
    __slots__ = ('name', 'decls', 'coord', '__weakref__')

    def __init__(self, name, decls, coord=None):
        self.name = name
        self.decls = decls
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(('decls[%d]' % i, child))
        else:
            return tuple(nodelist)

    def __iter__(self):
        for child in self.decls or []:
            (yield child)

    attr_names = ('name', )


class While(Node):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')

    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children--- This code section failed: ---

 L.1056         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nodelist'

 L.1057         4  LOAD_FAST                'self'
                6  LOAD_ATTR                cond
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'
               14  LOAD_FAST                'nodelist'
               16  LOAD_METHOD              append
               18  LOAD_STR                 'cond'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                cond
               24  BUILD_TUPLE_2         2 
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            12  '12'

 L.1058        30  LOAD_FAST                'self'
               32  LOAD_ATTR                stmt
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_FAST                'nodelist'
               42  LOAD_METHOD              append
               44  LOAD_STR                 'stmt'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                stmt
               50  BUILD_TUPLE_2         2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            38  '38'

 L.1059        56  LOAD_GLOBAL              tuple
               58  LOAD_FAST                'nodelist'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def __iter__--- This code section failed: ---

 L.1062         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cond
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1063        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cond
               14  YIELD_VALUE      
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

 L.1064        18  LOAD_FAST                'self'
               20  LOAD_ATTR                stmt
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L.1065        28  LOAD_FAST                'self'
               30  LOAD_ATTR                stmt
               32  YIELD_VALUE      
               34  POP_TOP          
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    attr_names = ()


class Pragma(Node):
    __slots__ = ('string', 'coord', '__weakref__')

    def __init__(self, string, coord=None):
        self.string = string
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        pass
        if False:
            yield None

    attr_names = ('string', )