# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def __new__(cls, *args, **kwds):
        """Constructor that prevents Base from being instantiated."""
        assert cls is not Base, 'Cannot instantiate Base'
        return object.__new__(cls)

    def __eq__(self, other):
        """
        Compare two nodes for equality.

        This calls the method _eq().
        """
        if self.__class__ is not other.__class__:
            return NotImplemented
        return self._eq(other)

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

    def replace(self, new):
        """Replace this node with a new one in the parent."""
        assert self.parent is not None, str(self)
        assert new is not None
        if not isinstance(new, list):
            new = [
             new]
        l_children = []
        found = False
        for ch in self.parent.children:
            if ch is self:
                if found:
                    raise AssertionError((self.parent.children, self, new))
                else:
                    if new is not None:
                        l_children.extend(new)
                    found = True
            else:
                l_children.append(ch)
        else:
            assert found, (self.children, self, new)
            self.parent.changed()
            self.parent.children = l_children
            for x in new:
                x.parent = self.parent
            else:
                self.parent = None

    def get_lineno(self):
        """Return the line number which generated the invocant node."""
        node = self
        while True:
            if not isinstance(node, Leaf):
                if not node.children:
                    return
                node = node.children[0]

        return node.lineno

    def changed(self):
        if self.parent:
            self.parent.changed()
        self.was_changed = True

    def remove(self):
        """
        Remove the node from the tree. Returns the position of the node in its
        parent's children before it was removed.
        """
        if self.parent:
            for i, node in enumerate(self.parent.children):
                if node is self:
                    self.parent.changed()
                    del self.parent.children[i]
                    self.parent = None
                    return i

    @property
    def next_sibling--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parent
                4  LOAD_CONST               None
                6  COMPARE_OP               is
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
             26_0  COME_FROM            90  '90'
             26_1  COME_FROM            40  '40'
               26  FOR_ITER             92  'to 92'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'i'
               32  STORE_FAST               'child'

 L. 162        34  LOAD_FAST                'child'
               36  LOAD_FAST                'self'
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE_BACK    26  'to 26'

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
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    88  'to 88'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 166        80  POP_EXCEPT       
               82  POP_TOP          
               84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            72  '72'
               88  END_FINALLY      
               90  JUMP_BACK            26  'to 26'
             92_0  COME_FROM            26  '26'

Parse error at or near `ROT_TWO' instruction at offset 60

    @property
    def prev_sibling(self):
        """
        The node immediately preceding the invocant in their parent's children
        list. If the invocant does not have a previous sibling, it is None.
        """
        if self.parent is None:
            return
        for i, child in enumerate(self.parent.children):
            if child is self:
                if i == 0:
                    return None
                else:
                    return self.parent.children[(i - 1)]

    def leaves(self):
        for child in self.children:
            yield from child.leaves()

        if False:
            yield None

    def depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()

    def get_suffix(self):
        """
        Return the string immediately following the invocant node. This is
        effectively equivalent to node.next_sibling.prefix
        """
        next_sib = self.next_sibling
        if next_sib is None:
            return ''
        return next_sib.prefix

    if sys.version_info < (3, 0):

        def __str__(self):
            return str(self).encode('ascii')


class Node(Base):
    __doc__ = 'Concrete implementation for interior nodes.'

    def __init__(self, type, children, context=None, prefix=None, fixers_applied=None):
        """
        Initializer.

        Takes a type constant (a symbol number >= 256), a sequence of
        child nodes, and an optional context keyword argument.

        As a side effect, the parent pointers of the children are updated.
        """
        assert type >= 256, type
        self.type = type
        self.children = list(children)
        for ch in self.children:
            if not ch.parent is None:
                raise AssertionError(repr(ch))
            else:
                ch.parent = self
        else:
            if prefix is not None:
                self.prefix = prefix
            if fixers_applied:
                self.fixers_applied = fixers_applied[:]
            else:
                self.fixers_applied = None

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
        return ''.join(map(str, self.children))

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
            yield from child.post_order()
        else:
            yield self

    def pre_order(self):
        """Return a pre-order iterator for the tree."""
        yield self
        for child in self.children:
            yield from child.pre_order()

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
        self.children.append(child)
        self.changed()


class Leaf(Base):
    __doc__ = 'Concrete implementation for leaf nodes.'
    _prefix = ''
    lineno = 0
    column = 0

    def __init__(self, type, value, context=None, prefix=None, fixers_applied=[]):
        """
        Initializer.

        Takes a type constant (a token number < 256), a string value, and an
        optional context keyword argument.
        """
        if not 0 <= type < 256:
            raise AssertionError(type)
        if context is not None:
            self._prefix, (self.lineno, self.column) = context
        self.type = type
        self.value = value
        if prefix is not None:
            self._prefix = prefix
        self.fixers_applied = fixers_applied[:]

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
        yield self

    def post_order(self):
        """Return a post-order iterator for the tree."""
        yield self

    def pre_order(self):
        """Return a pre-order iterator for the tree."""
        yield self

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


def convert(gr, raw_node):
    """
    Convert raw node information to a Node or Leaf instance.

    This is passed to the parser driver which calls it whenever a reduction of a
    grammar rule produces a new complete node, so that the tree is build
    strictly bottom-up.
    """
    type, value, context, children = raw_node
    if children or (type in gr.number2symbol):
        if len(children) == 1:
            return children[0]
        return Node(type, children, context=context)
    return Leaf(type, value, context=context)


class BasePattern(object):
    __doc__ = '\n    A pattern is a tree matching pattern.\n\n    It looks for a specific node type (token or symbol), and\n    optionally for a specific content.\n\n    This is an abstract base class.  There are three concrete\n    subclasses:\n\n    - LeafPattern matches a single leaf node;\n    - NodePattern matches a single node (usually non-leaf);\n    - WildcardPattern matches a sequence of nodes of variable length.\n    '
    type = None
    content = None
    name = None

    def __new__(cls, *args, **kwds):
        """Constructor that prevents BasePattern from being instantiated."""
        assert cls is not BasePattern, 'Cannot instantiate BasePattern'
        return object.__new__(cls)

    def __repr__(self):
        args = [
         type_repr(self.type), self.content, self.name]
        while args:
            if args[(-1)] is None:
                del args[-1]

        return '%s(%s)' % (self.__class__.__name__, ', '.join(map(repr, args)))

    def optimize(self):
        """
        A subclass can define this as a hook for optimizations.

        Returns either self or another node with the same effect.
        """
        return self

    def match(self, node, results=None):
        """
        Does this pattern exactly match a node?

        Returns True if it matches, False if not.

        If results is not None, it must be a dict which will be
        updated with the nodes matching named subpatterns.

        Default implementation for non-wildcard patterns.
        """
        if self.type is not None:
            if node.type != self.type:
                return False
        if self.content is not None:
            r = None
            if results is not None:
                r = {}
            if not self._submatch(node, r):
                return False
            if r:
                results.update(r)
        if results is not None:
            if self.name:
                results[self.name] = node
        return True

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
                yield (
                 1, r)


class LeafPattern(BasePattern):

    def __init__(self, type=None, content=None, name=None):
        """
        Initializer.  Takes optional type, content, and name.

        The type, if given must be a token type (< 256).  If not given,
        this matches any *leaf* node; the content may still be required.

        The content, if given, must be a string.

        If a name is given, the matching node is stored in the results
        dict under that key.
        """
        if type is not None:
            if not 0 <= type < 256:
                raise AssertionError(type)
        if content is not None:
            assert isinstance(content, str), repr(content)
        self.type = type
        self.content = content
        self.name = name

    def match(self, node, results=None):
        """Override match() to insist on a leaf node."""
        if not isinstance(node, Leaf):
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

    def __init__(self, type=None, content=None, name=None):
        """
        Initializer.  Takes optional type, content, and name.

        The type, if given, must be a symbol type (>= 256).  If the
        type is None this matches *any* single node (leaf or not),
        except if content is not None, in which it only matches
        non-leaf nodes that also match the content pattern.

        The content, if not None, must be a sequence of Patterns that
        must match the node's children exactly.  If the content is
        given, the type must not be None.

        If a name is given, the matching node is stored in the results
        dict under that key.
        """
        if type is not None:
            assert type >= 256, type
            if content is not None:
                if isinstance(content, str):
                    raise AssertionError(repr(content))
                content = list(content)
                for i, item in enumerate(content):
                    assert isinstance(item, BasePattern), (i, item)
                    if isinstance(item, WildcardPattern):
                        self.wildcards = True

        self.type = type
        self.content = content
        self.name = name

    def _submatch(self, node, results=None):
        """
        Match the pattern's content to the node's children.

        This assumes the node type matches and self.content is not None.

        Returns True if it matches, False if not.

        If results is not None, it must be a dict which will be
        updated with the nodes matching named subpatterns.

        When returning False, the results dict may still be updated.
        """
        if self.wildcards:
            for c, r in generate_matches(self.content, node.children):
                if c == len(node.children):
                    if results is not None:
                        results.update(r)
                    else:
                        return True
                return False

            if len(self.content) != len(node.children):
                return False
            for subpattern, child in zip(self.content, node.children):
                if not subpattern.match(child, results):
                    return False

            return True


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
               32  LOAD_GLOBAL              AssertionError
               34  LOAD_FAST                'min'
               36  LOAD_FAST                'max'
               38  BUILD_TUPLE_2         2 
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            26  '26'

 L. 643        44  LOAD_FAST                'content'
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
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
               74  LOAD_ASSERT              AssertionError
               76  LOAD_GLOBAL              repr
               78  LOAD_FAST                'content'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            72  '72'

 L. 647        86  LOAD_FAST                'content'
               88  GET_ITER         
             90_0  COME_FROM           114  '114'
             90_1  COME_FROM           100  '100'
               90  FOR_ITER            116  'to 116'
               92  STORE_FAST               'alt'

 L. 648        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'alt'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_TRUE_BACK    90  'to 90'
              102  LOAD_GLOBAL              AssertionError
              104  LOAD_GLOBAL              repr
              106  LOAD_FAST                'alt'
              108  CALL_FUNCTION_1       1  ''
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
              114  JUMP_BACK            90  'to 90'
            116_0  COME_FROM            90  '90'
            116_1  COME_FROM            50  '50'

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

    def optimize(self):
        """Optimize certain stacked wildcard patterns."""
        subpattern = None
        if self.content is not None:
            if len(self.content) == 1:
                if len(self.content[0]) == 1:
                    subpattern = self.content[0][0]
        if self.min == 1:
            if self.max == 1:
                if self.content is None:
                    return NodePattern(name=(self.name))
                if subpattern is not None:
                    if self.name == subpattern.name:
                        return subpattern.optimize()
        if self.min <= 1:
            if isinstance(subpattern, WildcardPattern):
                if subpattern.min <= 1:
                    if self.name == subpattern.name:
                        return WildcardPattern(subpattern.content, self.min * subpattern.min, self.max * subpattern.max, subpattern.name)
        return self

    def match(self, node, results=None):
        """Does this pattern exactly match a node?"""
        return self.match_seq([node], results)

    def match_seq(self, nodes, results=None):
        """Does this pattern exactly match a sequence of nodes?"""
        for c, r in self.generate_matches(nodes):
            if c == len(nodes):
                if results is not None:
                    results.update(r)
                    if self.name:
                        results[self.name] = list(nodes)
                else:
                    return True
        else:
            return False

    def generate_matches(self, nodes):
        """
        Generator yielding matches for a sequence of nodes.

        Args:
            nodes: sequence of nodes

        Yields:
            (count, results) tuples where:
            count: the match comprises nodes[:count];
            results: dict containing named submatches.
        """
        if self.content is None:
            for count in range(self.min, 1 + min(len(nodes), self.max)):
                r = {}
                if self.name:
                    r[self.name] = nodes[:count]
                else:
                    yield (
                     count, r)

        elif self.name == 'bare_name':
            yield self._bare_name_matches(nodes)
        else:
            if hasattr(sys, 'getrefcount'):
                save_stderr = sys.stderr
                sys.stderr = StringIO()
            try:
                try:
                    for count, r in self._recursive_matches(nodes, 0):
                        if self.name:
                            r[self.name] = nodes[:count]
                        else:
                            yield (
                             count, r)

                except RuntimeError:
                    for count, r in self._iterative_matches(nodes):
                        if self.name:
                            r[self.name] = nodes[:count]
                        else:
                            yield (
                             count, r)

            finally:
                if hasattr(sys, 'getrefcount'):
                    sys.stderr = save_stderr

    def _iterative_matches(self, nodes):
        """Helper to iteratively yield the matches."""
        nodelen = len(nodes)
        if 0 >= self.min:
            yield (
             0, {})
        results = []
        for alt in self.content:
            for c, r in generate_matches(alt, nodes):
                yield (
                 c, r)
                results.append((c, r))

        else:
            while True:
                if results:
                    new_results = []
                    for c0, r0 in results:
                        if c0 < nodelen:
                            if c0 <= self.max:
                                for alt in self.content:
                                    for c1, r1 in generate_matches(alt, nodes[c0:]):
                                        if c1 > 0:
                                            r = {}
                                            r.update(r0)
                                            r.update(r1)
                                            yield (c0 + c1, r)
                                            new_results.append((c0 + c1, r))

                    else:
                        results = new_results

    def _bare_name_matches(self, nodes):
        """Special optimized matcher for bare_name."""
        count = 0
        r = {}
        done = False
        max = len(nodes)
        while not done or count < max:
            done = True
            for leaf in self.content:
                if leaf[0].match(nodes[count], r):
                    count += 1
                    done = False
                    break

        r[self.name] = nodes[:count]
        return (
         count, r)

    def _recursive_matches(self, nodes, count):
        """Helper to recursively yield the matches."""
        assert self.content is not None
        if count >= self.min:
            yield (
             0, {})
        if count < self.max:
            for alt in self.content:
                for c0, r0 in generate_matches(alt, nodes):
                    for c1, r1 in self._recursive_matches(nodes[c0:], count + 1):
                        r = {}
                        r.update(r0)
                        r.update(r1)
                        yield (c0 + c1, r)


class NegatedPattern(BasePattern):

    def __init__(self, content=None):
        """
        Initializer.

        The argument is either a pattern or None.  If it is None, this
        only matches an empty sequence (effectively '$' in regex
        lingo).  If it is not None, this matches whenever the argument
        pattern doesn't have any matches.
        """
        if content is not None:
            assert isinstance(content, BasePattern), repr(content)
        self.content = content

    def match(self, node):
        return False

    def match_seq(self, nodes):
        return len(nodes) == 0

    def generate_matches(self, nodes):
        if self.content is None:
            if len(nodes) == 0:
                yield (
                 0, {})
        else:
            for c, r in self.content.generate_matches(nodes):
                return None

            yield (
             0, {})


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
        yield (
         0, {})
    else:
        p, rest = patterns[0], patterns[1:]
        for c0, r0 in p.generate_matches(nodes):
            if not rest:
                yield (
                 c0, r0)
            else:
                for c1, r1 in generate_matches(rest, nodes[c0:]):
                    r = {}
                    r.update(r0)
                    r.update(r1)
                    yield (c0 + c1, r)