# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: lib2to3\btm_utils.py
"""Utility functions used by the btm_matcher module"""
from . import pytree
from .pgen2 import grammar, token
from .pygram import pattern_symbols, python_symbols
syms = pattern_symbols
pysyms = python_symbols
tokens = grammar.opmap
token_labels = token
TYPE_ANY = -1
TYPE_ALTERNATIVES = -2
TYPE_GROUP = -3

class MinNode(object):
    __doc__ = 'This class serves as an intermediate representation of the\n    pattern tree during the conversion to sets of leaf-to-root\n    subpatterns'

    def __init__(self, type=None, name=None):
        self.type = type
        self.name = name
        self.children = []
        self.leaf = False
        self.parent = None
        self.alternatives = []
        self.group = []

    def __repr__(self):
        return str(self.type) + ' ' + str(self.name)

    def leaf_to_root--- This code section failed: ---

 L.  37         0  LOAD_FAST                'self'
                2  STORE_FAST               'node'

 L.  38         4  BUILD_LIST_0          0 
                6  STORE_FAST               'subp'
              8_0  COME_FROM           224  '224'
              8_1  COME_FROM           158  '158'
              8_2  COME_FROM            78  '78'

 L.  39         8  LOAD_FAST                'node'
               10  POP_JUMP_IF_FALSE   226  'to 226'

 L.  40        12  LOAD_FAST                'node'
               14  LOAD_ATTR                type
               16  LOAD_GLOBAL              TYPE_ALTERNATIVES
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    94  'to 94'

 L.  41        22  LOAD_FAST                'node'
               24  LOAD_ATTR                alternatives
               26  LOAD_METHOD              append
               28  LOAD_FAST                'subp'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L.  42        34  LOAD_GLOBAL              len
               36  LOAD_FAST                'node'
               38  LOAD_ATTR                alternatives
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'node'
               46  LOAD_ATTR                children
               48  CALL_FUNCTION_1       1  ''
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    82  'to 82'

 L.  44        54  LOAD_GLOBAL              tuple
               56  LOAD_FAST                'node'
               58  LOAD_ATTR                alternatives
               60  CALL_FUNCTION_1       1  ''
               62  BUILD_LIST_1          1 
               64  STORE_FAST               'subp'

 L.  45        66  BUILD_LIST_0          0 
               68  LOAD_FAST                'node'
               70  STORE_ATTR               alternatives

 L.  46        72  LOAD_FAST                'node'
               74  LOAD_ATTR                parent
               76  STORE_FAST               'node'

 L.  47        78  JUMP_BACK             8  'to 8'
               80  BREAK_LOOP           94  'to 94'
             82_0  COME_FROM            52  '52'

 L.  49        82  LOAD_FAST                'node'
               84  LOAD_ATTR                parent
               86  STORE_FAST               'node'

 L.  50        88  LOAD_CONST               None
               90  STORE_FAST               'subp'

 L.  51        92  JUMP_FORWARD        226  'to 226'
             94_0  COME_FROM            80  '80'
             94_1  COME_FROM            20  '20'

 L.  53        94  LOAD_FAST                'node'
               96  LOAD_ATTR                type
               98  LOAD_GLOBAL              TYPE_GROUP
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   174  'to 174'

 L.  54       104  LOAD_FAST                'node'
              106  LOAD_ATTR                group
              108  LOAD_METHOD              append
              110  LOAD_FAST                'subp'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L.  56       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'node'
              120  LOAD_ATTR                group
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'node'
              128  LOAD_ATTR                children
              130  CALL_FUNCTION_1       1  ''
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   162  'to 162'

 L.  57       136  LOAD_GLOBAL              get_characteristic_subpattern
              138  LOAD_FAST                'node'
              140  LOAD_ATTR                group
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'subp'

 L.  58       146  BUILD_LIST_0          0 
              148  LOAD_FAST                'node'
              150  STORE_ATTR               group

 L.  59       152  LOAD_FAST                'node'
              154  LOAD_ATTR                parent
              156  STORE_FAST               'node'

 L.  60       158  JUMP_BACK             8  'to 8'
              160  BREAK_LOOP          174  'to 174'
            162_0  COME_FROM           134  '134'

 L.  62       162  LOAD_FAST                'node'
              164  LOAD_ATTR                parent
              166  STORE_FAST               'node'

 L.  63       168  LOAD_CONST               None
              170  STORE_FAST               'subp'

 L.  64       172  JUMP_FORWARD        226  'to 226'
            174_0  COME_FROM           160  '160'
            174_1  COME_FROM           102  '102'

 L.  66       174  LOAD_FAST                'node'
              176  LOAD_ATTR                type
              178  LOAD_GLOBAL              token_labels
              180  LOAD_ATTR                NAME
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   206  'to 206'
              186  LOAD_FAST                'node'
              188  LOAD_ATTR                name
              190  POP_JUMP_IF_FALSE   206  'to 206'

 L.  68       192  LOAD_FAST                'subp'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'node'
              198  LOAD_ATTR                name
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  JUMP_FORWARD        218  'to 218'
            206_0  COME_FROM           190  '190'
            206_1  COME_FROM           184  '184'

 L.  70       206  LOAD_FAST                'subp'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'node'
              212  LOAD_ATTR                type
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L.  72       218  LOAD_FAST                'node'
              220  LOAD_ATTR                parent
              222  STORE_FAST               'node'
              224  JUMP_BACK             8  'to 8'
            226_0  COME_FROM           172  '172'
            226_1  COME_FROM            92  '92'
            226_2  COME_FROM            10  '10'

 L.  73       226  LOAD_FAST                'subp'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 92

    def get_linear_subpattern(self):
        """Drives the leaf_to_root method. The reason that
        leaf_to_root must be run multiple times is because we need to
        reject 'group' matches; for example the alternative form
        (a | b c) creates a group [b c] that needs to be matched. Since
        matching multiple linear patterns overcomes the automaton's
        capabilities, leaf_to_root merges each group into a single
        choice based on 'characteristic'ity,

        i.e. (a|b c) -> (a|b) if b more characteristic than c

        Returns: The most 'characteristic'(as defined by
          get_characteristic_subpattern) path for the compiled pattern
          tree.
        """
        for l in self.leaves():
            subp = l.leaf_to_root()
            if subp:
                return subp

    def leaves(self):
        """Generator that returns the leaves of the tree"""
        for child in self.children:
            yield from child.leaves()
        else:
            if not self.children:
                yield self


def reduce_tree(node, parent=None):
    """
    Internal function. Reduces a compiled pattern tree to an
    intermediate representation suitable for feeding the
    automaton. This also trims off any optional pattern elements(like
    [a], a*).
    """
    new_node = None
    if node.type == syms.Matcher:
        node = node.children[0]
    if node.type == syms.Alternatives:
        if len(node.children) <= 2:
            new_node = reduce_tree(node.children[0], parent)
        else:
            new_node = MinNode(type=TYPE_ALTERNATIVES)
            for child in node.children:
                if node.children.indexchild % 2:
                    pass
                else:
                    reduced = reduce_tree(child, new_node)
                    if reduced is not None:
                        new_node.children.appendreduced

    else:
        pass
    if node.type == syms.Alternative:
        if len(node.children) > 1:
            new_node = MinNode(type=TYPE_GROUP)
            for child in node.children:
                reduced = reduce_tree(child, new_node)
                if reduced:
                    new_node.children.appendreduced
            else:
                if not new_node.children:
                    new_node = None

        else:
            new_node = reduce_tree(node.children[0], parent)
    else:
        if node.type == syms.Unit:
            if isinstance(node.children[0], pytree.Leaf):
                if node.children[0].value == '(':
                    return reduce_tree(node.children[1], parent)
            if not (isinstance(node.children[0], pytree.Leaf) and node.children[0].value == '['):
                if len(node.children) > 1:
                    if not hasattr(node.children[1], 'value') or node.children[1].value == '[':
                        return
                leaf = True
                details_node = None
                alternatives_node = None
                has_repeater = False
                repeater_node = None
                has_variable_name = False
            for child in node.children:
                if child.type == syms.Details:
                    leaf = False
                    details_node = child
                elif child.type == syms.Repeater:
                    has_repeater = True
                    repeater_node = child
                elif child.type == syms.Alternatives:
                    alternatives_node = child
                if hasattr(child, 'value'):
                    if child.value == '=':
                        has_variable_name = True
            else:
                if has_variable_name:
                    name_leaf = node.children[2]
                    if not hasattr(name_leaf, 'value') or name_leaf.value == '(':
                        name_leaf = node.children[3]
                else:
                    name_leaf = node.children[0]
                if name_leaf.type == token_labels.NAME:
                    if name_leaf.value == 'any':
                        new_node = MinNode(type=TYPE_ANY)
                    elif hasattr(token_labels, name_leaf.value):
                        new_node = MinNode(type=(getattr(token_labels, name_leaf.value)))
                    else:
                        new_node = MinNode(type=(getattr(pysyms, name_leaf.value)))
                elif name_leaf.type == token_labels.STRING:
                    name = name_leaf.value.strip"'"
                    if name in tokens:
                        new_node = MinNode(type=(tokens[name]))
                    else:
                        new_node = MinNode(type=(token_labels.NAME), name=name)
                elif name_leaf.type == syms.Alternatives:
                    new_node = reduce_tree(alternatives_node, parent)
                if has_repeater:
                    if repeater_node.children[0].value == '*':
                        new_node = None

        else:
            pass
        if repeater_node.children[0].value == '+':
            pass
        else:
            raise NotImplementedError
    if details_node:
        if new_node is not None:
            for child in details_node.children[1:-1]:
                reduced = reduce_tree(child, new_node)
                if reduced is not None:
                    new_node.children.appendreduced
            else:
                if new_node:
                    new_node.parent = parent

        return new_node


def get_characteristic_subpattern(subpatterns):
    """Picks the most characteristic from a list of linear patterns
    Current order used is:
    names > common_names > common_chars
    """
    if not isinstance(subpatterns, list):
        return subpatterns
    if len(subpatterns) == 1:
        return subpatterns[0]
    subpatterns_with_names = []
    subpatterns_with_common_names = []
    common_names = [
     'in', 'for', 'if', 'not', 'None']
    subpatterns_with_common_chars = []
    common_chars = '[]().,:'
    for subpattern in subpatterns:
        if any(rec_test(subpattern, lambda x: type(x) is str)):
            if any(rec_test(subpattern, lambda x: isinstance(x, str) and x in common_chars)):
                subpatterns_with_common_chars.appendsubpattern
            else:
                if any(rec_test(subpattern, lambda x: isinstance(x, str) and x in common_names)):
                    subpatterns_with_common_names.appendsubpattern
                else:
                    subpatterns_with_names.appendsubpattern
    else:
        if subpatterns_with_names:
            subpatterns = subpatterns_with_names
        elif subpatterns_with_common_names:
            subpatterns = subpatterns_with_common_names
        elif subpatterns_with_common_chars:
            subpatterns = subpatterns_with_common_chars
        return max(subpatterns, key=len)


def rec_test(sequence, test_func):
    """Tests test_func on all items of sequence and items of included
    sub-iterables"""
    for x in sequence:
        if isinstance(x, (list, tuple)):
            yield from rec_test(x, test_func)
        else:
            yield test_func(x)