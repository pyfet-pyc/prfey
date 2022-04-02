# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\btm_matcher.py
"""A bottom-up tree matching algorithm implementation meant to speed
up 2to3's matching process. After the tree patterns are reduced to
their rarest linear path, a linear Aho-Corasick automaton is
created. The linear automaton traverses the linear paths from the
leaves to the root of the AST and returns a set of nodes for further
matching. This reduces significantly the number of candidate nodes."""
__author__ = 'George Boutsioukis <gboutsioukis@gmail.com>'
import logging, itertools
from collections import defaultdict
from . import pytree
from .btm_utils import reduce_tree

class BMNode(object):
    __doc__ = 'Class for a node of the Aho-Corasick automaton used in matching'
    count = itertools.count()

    def __init__(self):
        self.transition_table = {}
        self.fixers = []
        self.id = next(BMNode.count)
        self.content = ''


class BottomMatcher(object):
    __doc__ = 'The main matcher class. After instantiating the patterns should\n    be added using the add_fixer method'

    def __init__(self):
        self.match = set()
        self.root = BMNode()
        self.nodes = [self.root]
        self.fixers = []
        self.logger = logging.getLogger('RefactoringTool')

    def add_fixer(self, fixer):
        """Reduces a fixer's pattern tree to a linear path and adds it
        to the matcher(a common Aho-Corasick automaton). The fixer is
        appended on the matching states and called when they are
        reached"""
        self.fixers.append(fixer)
        tree = reduce_tree(fixer.pattern_tree)
        linear = tree.get_linear_subpattern()
        match_nodes = self.add(linear, start=(self.root))
        for match_node in match_nodes:
            match_node.fixers.append(fixer)

    def add--- This code section failed: ---

 L.  52         0  LOAD_FAST                'pattern'
                2  POP_JUMP_IF_TRUE     10  'to 10'

 L.  54         4  LOAD_FAST                'start'
                6  BUILD_LIST_1          1 
                8  RETURN_VALUE     
             10_0  COME_FROM             2  '2'

 L.  55        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'pattern'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_GLOBAL              tuple
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    96  'to 96'

 L.  58        24  BUILD_LIST_0          0 
               26  STORE_FAST               'match_nodes'

 L.  59        28  LOAD_FAST                'pattern'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  GET_ITER         
               36  FOR_ITER             92  'to 92'
               38  STORE_FAST               'alternative'

 L.  62        40  LOAD_FAST                'self'
               42  LOAD_ATTR                add
               44  LOAD_FAST                'alternative'
               46  LOAD_FAST                'start'
               48  LOAD_CONST               ('start',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  STORE_FAST               'end_nodes'

 L.  63        54  LOAD_FAST                'end_nodes'
               56  GET_ITER         
               58  FOR_ITER             90  'to 90'
               60  STORE_FAST               'end'

 L.  64        62  LOAD_FAST                'match_nodes'
               64  LOAD_METHOD              extend
               66  LOAD_FAST                'self'
               68  LOAD_METHOD              add
               70  LOAD_FAST                'pattern'
               72  LOAD_CONST               1
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'end'
               82  CALL_METHOD_2         2  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  JUMP_BACK            58  'to 58'
               90  JUMP_BACK            36  'to 36'

 L.  65        92  LOAD_FAST                'match_nodes'
               94  RETURN_VALUE     
             96_0  COME_FROM            22  '22'

 L.  69        96  LOAD_FAST                'pattern'
               98  LOAD_CONST               0
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'start'
              104  LOAD_ATTR                transition_table
              106  <118>                 1  ''
              108  POP_JUMP_IF_FALSE   132  'to 132'

 L.  71       110  LOAD_GLOBAL              BMNode
              112  CALL_FUNCTION_0       0  ''
              114  STORE_FAST               'next_node'

 L.  72       116  LOAD_FAST                'next_node'
              118  LOAD_FAST                'start'
              120  LOAD_ATTR                transition_table
              122  LOAD_FAST                'pattern'
              124  LOAD_CONST               0
              126  BINARY_SUBSCR    
              128  STORE_SUBSCR     
              130  JUMP_FORWARD        146  'to 146'
            132_0  COME_FROM           108  '108'

 L.  75       132  LOAD_FAST                'start'
              134  LOAD_ATTR                transition_table
              136  LOAD_FAST                'pattern'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  BINARY_SUBSCR    
              144  STORE_FAST               'next_node'
            146_0  COME_FROM           130  '130'

 L.  77       146  LOAD_FAST                'pattern'
              148  LOAD_CONST               1
              150  LOAD_CONST               None
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  POP_JUMP_IF_FALSE   182  'to 182'

 L.  78       158  LOAD_FAST                'self'
              160  LOAD_ATTR                add
              162  LOAD_FAST                'pattern'
              164  LOAD_CONST               1
              166  LOAD_CONST               None
              168  BUILD_SLICE_2         2 
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'next_node'
              174  LOAD_CONST               ('start',)
              176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              178  STORE_FAST               'end_nodes'
              180  JUMP_FORWARD        188  'to 188'
            182_0  COME_FROM           156  '156'

 L.  80       182  LOAD_FAST                'next_node'
              184  BUILD_LIST_1          1 
              186  STORE_FAST               'end_nodes'
            188_0  COME_FROM           180  '180'

 L.  81       188  LOAD_FAST                'end_nodes'
              190  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 106

    def run--- This code section failed: ---

 L.  99         0  LOAD_FAST                'self'
                2  LOAD_ATTR                root
                4  STORE_FAST               'current_ac_node'

 L. 100         6  LOAD_GLOBAL              defaultdict
                8  LOAD_GLOBAL              list
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'results'

 L. 101        14  LOAD_FAST                'leaves'
               16  GET_ITER         
             18_0  COME_FROM            28  '28'
               18  FOR_ITER            234  'to 234'
               20  STORE_FAST               'leaf'

 L. 102        22  LOAD_FAST                'leaf'
               24  STORE_FAST               'current_ast_node'

 L. 103        26  LOAD_FAST                'current_ast_node'
               28  POP_JUMP_IF_FALSE    18  'to 18'

 L. 104        30  LOAD_CONST               True
               32  LOAD_FAST                'current_ast_node'
               34  STORE_ATTR               was_checked

 L. 105        36  LOAD_FAST                'current_ast_node'
               38  LOAD_ATTR                children
               40  GET_ITER         
             42_0  COME_FROM            66  '66'
             42_1  COME_FROM            56  '56'
               42  FOR_ITER             80  'to 80'
               44  STORE_FAST               'child'

 L. 107        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'child'
               50  LOAD_GLOBAL              pytree
               52  LOAD_ATTR                Leaf
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    42  'to 42'
               58  LOAD_FAST                'child'
               60  LOAD_ATTR                value
               62  LOAD_STR                 ';'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    42  'to 42'

 L. 108        68  LOAD_CONST               False
               70  LOAD_FAST                'current_ast_node'
               72  STORE_ATTR               was_checked

 L. 109        74  POP_TOP          
               76  BREAK_LOOP           80  'to 80'
               78  JUMP_BACK            42  'to 42'

 L. 110        80  LOAD_FAST                'current_ast_node'
               82  LOAD_ATTR                type
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 112        90  LOAD_FAST                'current_ast_node'
               92  LOAD_ATTR                value
               94  STORE_FAST               'node_token'
               96  JUMP_FORWARD        104  'to 104'
             98_0  COME_FROM            88  '88'

 L. 114        98  LOAD_FAST                'current_ast_node'
              100  LOAD_ATTR                type
              102  STORE_FAST               'node_token'
            104_0  COME_FROM            96  '96'

 L. 116       104  LOAD_FAST                'node_token'
              106  LOAD_FAST                'current_ac_node'
              108  LOAD_ATTR                transition_table
              110  <118>                 0  ''
              112  POP_JUMP_IF_FALSE   152  'to 152'

 L. 118       114  LOAD_FAST                'current_ac_node'
              116  LOAD_ATTR                transition_table
              118  LOAD_FAST                'node_token'
              120  BINARY_SUBSCR    
              122  STORE_FAST               'current_ac_node'

 L. 119       124  LOAD_FAST                'current_ac_node'
              126  LOAD_ATTR                fixers
              128  GET_ITER         
              130  FOR_ITER            150  'to 150'
              132  STORE_FAST               'fixer'

 L. 120       134  LOAD_FAST                'results'
              136  LOAD_FAST                'fixer'
              138  BINARY_SUBSCR    
              140  LOAD_METHOD              append
              142  LOAD_FAST                'current_ast_node'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_BACK           130  'to 130'
              150  JUMP_FORWARD        224  'to 224'
            152_0  COME_FROM           112  '112'

 L. 123       152  LOAD_FAST                'self'
              154  LOAD_ATTR                root
              156  STORE_FAST               'current_ac_node'

 L. 124       158  LOAD_FAST                'current_ast_node'
              160  LOAD_ATTR                parent
              162  LOAD_CONST               None
              164  <117>                 1  ''
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 125       168  LOAD_FAST                'current_ast_node'
              170  LOAD_ATTR                parent
              172  LOAD_ATTR                was_checked

 L. 124       174  POP_JUMP_IF_FALSE   178  'to 178'

 L. 127       176  JUMP_BACK            18  'to 18'
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           166  '166'

 L. 130       178  LOAD_FAST                'node_token'
              180  LOAD_FAST                'current_ac_node'
              182  LOAD_ATTR                transition_table
              184  <118>                 0  ''
              186  POP_JUMP_IF_FALSE   224  'to 224'

 L. 132       188  LOAD_FAST                'current_ac_node'
              190  LOAD_ATTR                transition_table
              192  LOAD_FAST                'node_token'
              194  BINARY_SUBSCR    
              196  STORE_FAST               'current_ac_node'

 L. 133       198  LOAD_FAST                'current_ac_node'
              200  LOAD_ATTR                fixers
              202  GET_ITER         
              204  FOR_ITER            224  'to 224'
              206  STORE_FAST               'fixer'

 L. 134       208  LOAD_FAST                'results'
              210  LOAD_FAST                'fixer'
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              append
              216  LOAD_FAST                'current_ast_node'
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_BACK           204  'to 204'
            224_0  COME_FROM           186  '186'
            224_1  COME_FROM           150  '150'

 L. 136       224  LOAD_FAST                'current_ast_node'
              226  LOAD_ATTR                parent
              228  STORE_FAST               'current_ast_node'
              230  JUMP_BACK            26  'to 26'
              232  JUMP_BACK            18  'to 18'

 L. 137       234  LOAD_FAST                'results'
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 110

    def print_ac(self):
        """Prints a graphviz diagram of the BM automaton(for debugging)"""
        print('digraph g{')

        def print_node(node):
            for subnode_key in node.transition_table.keys():
                subnode = node.transition_table[subnode_key]
                print('%d -> %d [label=%s] //%s' % (
                 node.id, subnode.id, type_repr(subnode_key), str(subnode.fixers)))
                if subnode_key == 1:
                    print(subnode.content)
                print_node(subnode)

        print_node(self.root)
        print('}')


_type_reprs = {}

def type_repr(type_num):
    global _type_reprs
    if not _type_reprs:
        from .pygram import python_symbols
        for name, val in python_symbols.__dict__.items():
            if type(val) == int:
                _type_reprs[val] = name

    return _type_reprs.setdefaulttype_numtype_num