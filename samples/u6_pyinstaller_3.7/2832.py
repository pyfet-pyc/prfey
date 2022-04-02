# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
            return [start]
        elif isinstance(pattern[0], tuple):
            match_nodes = []
            for alternative in pattern[0]:
                end_nodes = self.add(alternative, start=start)
                for end in end_nodes:
                    match_nodes.extend(self.add(pattern[1:], end))

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
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  STORE_FAST               'results'

 L. 101        14  SETUP_LOOP          252  'to 252'
               16  LOAD_FAST                'leaves'
               18  GET_ITER         
               20  FOR_ITER            250  'to 250'
               22  STORE_FAST               'leaf'

 L. 102        24  LOAD_FAST                'leaf'
               26  STORE_FAST               'current_ast_node'

 L. 103        28  SETUP_LOOP          248  'to 248'
               30  LOAD_FAST                'current_ast_node'
               32  POP_JUMP_IF_FALSE   246  'to 246'

 L. 104        34  LOAD_CONST               True
               36  LOAD_FAST                'current_ast_node'
               38  STORE_ATTR               was_checked

 L. 105        40  SETUP_LOOP           86  'to 86'
               42  LOAD_FAST                'current_ast_node'
               44  LOAD_ATTR                children
               46  GET_ITER         
             48_0  COME_FROM            72  '72'
             48_1  COME_FROM            62  '62'
               48  FOR_ITER             84  'to 84'
               50  STORE_FAST               'child'

 L. 107        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'child'
               56  LOAD_GLOBAL              pytree
               58  LOAD_ATTR                Leaf
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  POP_JUMP_IF_FALSE    48  'to 48'
               64  LOAD_FAST                'child'
               66  LOAD_ATTR                value
               68  LOAD_STR                 ';'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    48  'to 48'

 L. 108        74  LOAD_CONST               False
               76  LOAD_FAST                'current_ast_node'
               78  STORE_ATTR               was_checked

 L. 109        80  BREAK_LOOP       
               82  JUMP_BACK            48  'to 48'
               84  POP_BLOCK        
             86_0  COME_FROM_LOOP       40  '40'

 L. 110        86  LOAD_FAST                'current_ast_node'
               88  LOAD_ATTR                type
               90  LOAD_CONST               1
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 112        96  LOAD_FAST                'current_ast_node'
               98  LOAD_ATTR                value
              100  STORE_FAST               'node_token'
              102  JUMP_FORWARD        110  'to 110'
            104_0  COME_FROM            94  '94'

 L. 114       104  LOAD_FAST                'current_ast_node'
              106  LOAD_ATTR                type
              108  STORE_FAST               'node_token'
            110_0  COME_FROM           102  '102'

 L. 116       110  LOAD_FAST                'node_token'
              112  LOAD_FAST                'current_ac_node'
              114  LOAD_ATTR                transition_table
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   162  'to 162'

 L. 118       120  LOAD_FAST                'current_ac_node'
              122  LOAD_ATTR                transition_table
              124  LOAD_FAST                'node_token'
              126  BINARY_SUBSCR    
              128  STORE_FAST               'current_ac_node'

 L. 119       130  SETUP_LOOP          238  'to 238'
              132  LOAD_FAST                'current_ac_node'
              134  LOAD_ATTR                fixers
              136  GET_ITER         
              138  FOR_ITER            158  'to 158'
              140  STORE_FAST               'fixer'

 L. 120       142  LOAD_FAST                'results'
              144  LOAD_FAST                'fixer'
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              append
              150  LOAD_FAST                'current_ast_node'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          
              156  JUMP_BACK           138  'to 138'
              158  POP_BLOCK        
              160  JUMP_FORWARD        238  'to 238'
            162_0  COME_FROM           118  '118'

 L. 123       162  LOAD_FAST                'self'
              164  LOAD_ATTR                root
              166  STORE_FAST               'current_ac_node'

 L. 124       168  LOAD_FAST                'current_ast_node'
              170  LOAD_ATTR                parent
              172  LOAD_CONST               None
              174  COMPARE_OP               is-not
              176  POP_JUMP_IF_FALSE   188  'to 188'

 L. 125       178  LOAD_FAST                'current_ast_node'
              180  LOAD_ATTR                parent
              182  LOAD_ATTR                was_checked
              184  POP_JUMP_IF_FALSE   188  'to 188'

 L. 127       186  BREAK_LOOP       
            188_0  COME_FROM           184  '184'
            188_1  COME_FROM           176  '176'

 L. 130       188  LOAD_FAST                'node_token'
              190  LOAD_FAST                'current_ac_node'
              192  LOAD_ATTR                transition_table
              194  COMPARE_OP               in
              196  POP_JUMP_IF_FALSE   238  'to 238'

 L. 132       198  LOAD_FAST                'current_ac_node'
              200  LOAD_ATTR                transition_table
              202  LOAD_FAST                'node_token'
              204  BINARY_SUBSCR    
              206  STORE_FAST               'current_ac_node'

 L. 133       208  SETUP_LOOP          238  'to 238'
              210  LOAD_FAST                'current_ac_node'
              212  LOAD_ATTR                fixers
              214  GET_ITER         
              216  FOR_ITER            236  'to 236'
              218  STORE_FAST               'fixer'

 L. 134       220  LOAD_FAST                'results'
              222  LOAD_FAST                'fixer'
              224  BINARY_SUBSCR    
              226  LOAD_METHOD              append
              228  LOAD_FAST                'current_ast_node'
              230  CALL_METHOD_1         1  '1 positional argument'
              232  POP_TOP          
              234  JUMP_BACK           216  'to 216'
              236  POP_BLOCK        
            238_0  COME_FROM_LOOP      208  '208'
            238_1  COME_FROM           196  '196'
            238_2  COME_FROM           160  '160'
            238_3  COME_FROM_LOOP      130  '130'

 L. 136       238  LOAD_FAST                'current_ast_node'
              240  LOAD_ATTR                parent
              242  STORE_FAST               'current_ast_node'
              244  JUMP_BACK            30  'to 30'
            246_0  COME_FROM            32  '32'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP       28  '28'
              248  JUMP_BACK            20  'to 20'
              250  POP_BLOCK        
            252_0  COME_FROM_LOOP       14  '14'

 L. 137       252  LOAD_FAST                'results'
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 238_3

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

    return _type_reprs.setdefault(type_num, type_num)