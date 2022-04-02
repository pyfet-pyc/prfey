# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def add(self, pattern, start):
        """Recursively adds a linear pattern to the AC automaton"""
        if not pattern:
            return [
             start]
        if isinstance(pattern[0], tuple):
            match_nodes = []
            for alternative in pattern[0]:
                end_nodes = self.add(alternative, start=start)
                for end in end_nodes:
                    match_nodes.extend(self.add(pattern[1:], end))

            else:
                return match_nodes

        if pattern[0] not in start.transition_table:
            next_node = BMNode()
            start.transition_table[pattern[0]] = next_node
        else:
            next_node = start.transition_table[pattern[0]]
        if pattern[1:]:
            end_nodes = self.add((pattern[1:]), start=next_node)
        else:
            end_nodes = [
             next_node]
        return end_nodes

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
             18_0  COME_FROM           232  '232'
             18_1  COME_FROM           176  '176'
             18_2  COME_FROM            28  '28'
               18  FOR_ITER            234  'to 234'
               20  STORE_FAST               'leaf'

 L. 102        22  LOAD_FAST                'leaf'
               24  STORE_FAST               'current_ast_node'
             26_0  COME_FROM           230  '230'

 L. 103        26  LOAD_FAST                'current_ast_node'
               28  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 104        30  LOAD_CONST               True
               32  LOAD_FAST                'current_ast_node'
               34  STORE_ATTR               was_checked

 L. 105        36  LOAD_FAST                'current_ast_node'
               38  LOAD_ATTR                children
               40  GET_ITER         
             42_0  COME_FROM            78  '78'
             42_1  COME_FROM            66  '66'
             42_2  COME_FROM            56  '56'
               42  FOR_ITER             80  'to 80'
               44  STORE_FAST               'child'

 L. 107        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'child'
               50  LOAD_GLOBAL              pytree
               52  LOAD_ATTR                Leaf
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE_BACK    42  'to 42'
               58  LOAD_FAST                'child'
               60  LOAD_ATTR                value
               62  LOAD_STR                 ';'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE_BACK    42  'to 42'

 L. 108        68  LOAD_CONST               False
               70  LOAD_FAST                'current_ast_node'
               72  STORE_ATTR               was_checked

 L. 109        74  POP_TOP          
               76  BREAK_LOOP           80  'to 80'
               78  JUMP_BACK            42  'to 42'
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            42  '42'

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
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   152  'to 152'

 L. 118       114  LOAD_FAST                'current_ac_node'
              116  LOAD_ATTR                transition_table
              118  LOAD_FAST                'node_token'
              120  BINARY_SUBSCR    
              122  STORE_FAST               'current_ac_node'

 L. 119       124  LOAD_FAST                'current_ac_node'
              126  LOAD_ATTR                fixers
              128  GET_ITER         
            130_0  COME_FROM           148  '148'
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
            150_0  COME_FROM           130  '130'
              150  JUMP_FORWARD        224  'to 224'
            152_0  COME_FROM           112  '112'

 L. 123       152  LOAD_FAST                'self'
              154  LOAD_ATTR                root
              156  STORE_FAST               'current_ac_node'

 L. 124       158  LOAD_FAST                'current_ast_node'
              160  LOAD_ATTR                parent
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
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
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   224  'to 224'

 L. 132       188  LOAD_FAST                'current_ac_node'
              190  LOAD_ATTR                transition_table
              192  LOAD_FAST                'node_token'
              194  BINARY_SUBSCR    
              196  STORE_FAST               'current_ac_node'

 L. 133       198  LOAD_FAST                'current_ac_node'
              200  LOAD_ATTR                fixers
              202  GET_ITER         
            204_0  COME_FROM           222  '222'
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
            224_0  COME_FROM           204  '204'
            224_1  COME_FROM           186  '186'
            224_2  COME_FROM           150  '150'

 L. 136       224  LOAD_FAST                'current_ast_node'
              226  LOAD_ATTR                parent
              228  STORE_FAST               'current_ast_node'
              230  JUMP_BACK            26  'to 26'
              232  JUMP_BACK            18  'to 18'
            234_0  COME_FROM            18  '18'

 L. 137       234  LOAD_FAST                'results'
              236  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 234

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
                else:
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

        return _type_reprs.setdefault(type_num, type_num)