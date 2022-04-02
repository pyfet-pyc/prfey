# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: ast.py
"""
    ast
    ~~~

    The `ast` module helps Python applications to process trees of the Python
    abstract syntax grammar.  The abstract syntax itself might change with
    each Python release; this module helps to find out programmatically what
    the current grammar looks like and allows modifications of it.

    An abstract syntax tree can be generated by passing `ast.PyCF_ONLY_AST` as
    a flag to the `compile()` builtin function or by using the `parse()`
    function from this module.  The result will be a tree of objects whose
    classes all inherit from `ast.AST`.

    A modified abstract syntax tree can be compiled into a Python code object
    using the built-in `compile()` function.

    Additionally various helper functions are provided that make working with
    the trees simpler.  The main intention of the helper functions and this
    module in general is to provide an easy to use interface for libraries
    that work tightly with the python syntax (template engines for example).

    :copyright: Copyright 2008 by Armin Ronacher.
    :license: Python License.
"""
from _ast import *

def parse(source, filename='<unknown>', mode='exec', *, type_comments=False, feature_version=None):
    """
    Parse the source into an AST node.
    Equivalent to compile(source, filename, mode, PyCF_ONLY_AST).
    Pass type_comments=True to get back type comments where the syntax allows.
    """
    flags = PyCF_ONLY_AST
    if type_comments:
        flags |= PyCF_TYPE_COMMENTS
    elif isinstance(feature_version, tuple):
        major, minor = feature_version
        assert major == 3
        feature_version = minor
    else:
        if feature_version is None:
            feature_version = -1
    return compile(source, filename, mode, flags, _feature_version=feature_version)


def literal_eval(node_or_string):
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, bytes, numbers, tuples, lists, dicts,
    sets, booleans, and None.
    """
    if isinstance(node_or_string, str):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body

    def _convert_num(node):
        if isinstance(node, Constant):
            if type(node.value) in (int, float, complex):
                return node.value
        raise ValueError('malformed node or string: ' + repr(node))

    def _convert_signed_num(node):
        if isinstance(node, UnaryOp):
            if isinstance(node.op, (UAdd, USub)):
                operand = _convert_num(node.operand)
                if isinstance(node.op, UAdd):
                    return +operand
                return -operand
        return _convert_num(node)

    def _convert(node):
        if isinstance(node, Constant):
            return node.value
            if isinstance(node, Tuple):
                return tuple(map(_convert, node.elts))
            if isinstance(node, List):
                return list(map(_convert, node.elts))
            if isinstance(node, Set):
                return set(map(_convert, node.elts))
            if isinstance(node, Dict):
                return dict(zip(map(_convert, node.keys), map(_convert, node.values)))
        elif isinstance(node, BinOp):
            if isinstance(node.op, (Add, Sub)):
                left = _convert_signed_num(node.left)
                right = _convert_num(node.right)
                if isinstance(left, (int, float)):
                    if isinstance(right, complex):
                        if isinstance(node.op, Add):
                            return left + right
                        return left - right
        return _convert_signed_num(node)

    return _convert(node_or_string)


def dump(node, annotate_fields=True, include_attributes=False):
    """
    Return a formatted dump of the tree in node.  This is mainly useful for
    debugging purposes.  If annotate_fields is true (by default),
    the returned string will show the names and the values for fields.
    If annotate_fields is false, the result string will be more compact by
    omitting unambiguous field names.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    include_attributes can be set to true.
    """

    def _format(node):
        if isinstance(node, AST):
            args = []
            keywords = annotate_fields
            for field in node._fields:
                try:
                    value = getattr(node, field)
                except AttributeError:
                    keywords = True
                else:
                    if keywords:
                        args.append('%s=%s' % (field, _format(value)))
                    else:
                        args.append(_format(value))
            else:
                if include_attributes:
                    if node._attributes:
                        for a in node._attributes:
                            try:
                                args.append('%s=%s' % (a, _format(getattr(node, a))))
                            except AttributeError:
                                pass

                return '%s(%s)' % (node.__class__.__name__, ', '.join(args))

        if isinstance(node, list):
            return '[%s]' % ', '.join((_format(x) for x in node))
        return repr(node)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)


def copy_location(new_node, old_node):
    """
    Copy source location (`lineno`, `col_offset`, `end_lineno`, and `end_col_offset`
    attributes) from *old_node* to *new_node* if possible, and return *new_node*.
    """
    for attr in ('lineno', 'col_offset', 'end_lineno', 'end_col_offset'):
        if attr in old_node._attributes and attr in new_node._attributes and hasattr(old_node, attr):
            setattr(new_node, attr, getattr(old_node, attr))
        return new_node


def fix_missing_locations(node):
    """
    When you compile a node tree with compile(), the compiler expects lineno and
    col_offset attributes for every node that supports them.  This is rather
    tedious to fill in for generated nodes, so this helper adds these attributes
    recursively where not already set, by setting them to the values of the
    parent node.  It works recursively starting at *node*.
    """

    def _fix(node, lineno, col_offset, end_lineno, end_col_offset):
        if 'lineno' in node._attributes:
            if not hasattr(node, 'lineno'):
                node.lineno = lineno
            else:
                lineno = node.lineno
        elif 'end_lineno' in node._attributes:
            if not hasattr(node, 'end_lineno'):
                node.end_lineno = end_lineno
            else:
                end_lineno = node.end_lineno
        else:
            if 'col_offset' in node._attributes:
                if not hasattr(node, 'col_offset'):
                    node.col_offset = col_offset
                else:
                    col_offset = node.col_offset
            if 'end_col_offset' in node._attributes:
                node.end_col_offset = hasattr(node, 'end_col_offset') or end_col_offset
            else:
                end_col_offset = node.end_col_offset
        for child in iter_child_nodes(node):
            _fix(child, lineno, col_offset, end_lineno, end_col_offset)

    _fix(node, 1, 0, 1, 0)
    return node


def increment_lineno(node, n=1):
    """
    Increment the line number and end line number of each node in the tree
    starting at *node* by *n*. This is useful to "move code" to a different
    location in a file.
    """
    for child in walk(node):
        if 'lineno' in child._attributes:
            child.lineno = getattr(child, 'lineno', 0) + n
        if 'end_lineno' in child._attributes:
            child.end_lineno = getattr(child, 'end_lineno', 0) + n
        return node


def iter_fields(node):
    """
    Yield a tuple of ``(fieldname, value)`` for each field in ``node._fields``
    that is present on *node*.
    """
    for field in node._fields:
        try:
            (yield (
             field, getattr(node, field)))
        except AttributeError:
            pass


def iter_child_nodes(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for name, field in iter_fields(node):
        if isinstance(field, AST):
            (yield field)
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, AST):
                    (yield item)


def get_docstring(node, clean=True):
    """
    Return the docstring for the given node or None if no docstring can
    be found.  If the node provided does not have docstrings a TypeError
    will be raised.

    If *clean* is `True`, all tabs are expanded to spaces and any whitespace
    that can be uniformly removed from the second line onwards is removed.
    """
    if not isinstance(node, (AsyncFunctionDef, FunctionDef, ClassDef, Module)):
        raise TypeError("%r can't have docstrings" % node.__class__.__name__)
    elif node.body:
        if not isinstance(node.body[0], Expr):
            return
        node = node.body[0].value
        if isinstance(node, Str):
            text = node.s
    elif isinstance(node, Constant) and isinstance(node.value, str):
        text = node.value
    else:
        return
    if clean:
        import inspect
        text = inspect.cleandoc(text)
    return text


def _splitlines_no_ff(source):
    """Split a string into lines ignoring form feed and other chars.

    This mimics how the Python parser splits source code.
    """
    idx = 0
    lines = []
    next_line = ''
    while idx < len(source):
        c = source[idx]
        next_line += c
        idx += 1
        if c == '\r':
            if idx < len(source):
                if source[idx] == '\n':
                    next_line += '\n'
                    idx += 1
        if c in '\r\n':
            lines.append(next_line)
            next_line = ''

    if next_line:
        lines.append(next_line)
    return lines


def _pad_whitespace(source):
    """Replace all chars except '\x0c     ' in a line with spaces."""
    result = ''
    for c in source:
        if c in '\x0c\t':
            result += c
        else:
            result += ' '
    else:
        return result


def get_source_segment(source, node, *, padded=False):
    """Get source code segment of the *source* that generated *node*.

    If some location information (`lineno`, `end_lineno`, `col_offset`,
    or `end_col_offset`) is missing, return None.

    If *padded* is `True`, the first line of a multi-line statement will
    be padded with spaces to match its original position.
    """
    try:
        lineno = node.lineno - 1
        end_lineno = node.end_lineno - 1
        col_offset = node.col_offset
        end_col_offset = node.end_col_offset
    except AttributeError:
        return
    else:
        lines = _splitlines_no_ff(source)
        if end_lineno == lineno:
            return lines[lineno].encode()[col_offset:end_col_offset].decode()
        elif padded:
            padding = _pad_whitespace(lines[lineno].encode()[:col_offset].decode())
        else:
            padding = ''
        first = padding + lines[lineno].encode()[col_offset:].decode()
        last = lines[end_lineno].encode()[:end_col_offset].decode()
        lines = lines[lineno + 1:end_lineno]
        lines.insert(0, first)
        lines.append(last)
        return ''.join(lines)


def walk(node):
    """
    Recursively yield all descendant nodes in the tree starting at *node*
    (including *node* itself), in no specified order.  This is useful if you
    only want to modify nodes in place and don't care about the context.
    """
    from collections import deque
    todo = deque([node])
    while todo:
        node = todo.popleft()
        todo.extend(iter_child_nodes(node))
        (yield node)


class NodeVisitor(object):
    __doc__ = "\n    A node visitor base class that walks the abstract syntax tree and calls a\n    visitor function for every node found.  This function may return a value\n    which is forwarded by the `visit` method.\n\n    This class is meant to be subclassed, with the subclass adding visitor\n    methods.\n\n    Per default the visitor functions for the nodes are ``'visit_'`` +\n    class name of the node.  So a `TryFinally` node visit function would\n    be `visit_TryFinally`.  This behavior can be changed by overriding\n    the `visit` method.  If no visitor function exists for a node\n    (return value `None`) the `generic_visit` visitor is used instead.\n\n    Don't use the `NodeVisitor` if you want to apply changes to nodes during\n    traversing.  For this a special visitor exists (`NodeTransformer`) that\n    allows modifications.\n    "

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)

            elif isinstance(value, AST):
                self.visit(value)

    def visit_Constant(self, node):
        value = node.value
        type_name = _const_node_type_names.get(type(value))
        if type_name is None:
            for cls, name in _const_node_type_names.items():
                if isinstance(value, cls):
                    type_name = name
                    break

        if type_name is not None:
            method = 'visit_' + type_name
            try:
                visitor = getattr(self, method)
            except AttributeError:
                pass
            else:
                import warnings
                warnings.warn(f"{method} is deprecated; add visit_Constant", PendingDeprecationWarning, 2)
                return visitor(node)
        return self.generic_visit(node)


class NodeTransformer(NodeVisitor):
    __doc__ = "\n    A :class:`NodeVisitor` subclass that walks the abstract syntax tree and\n    allows modification of nodes.\n\n    The `NodeTransformer` will walk the AST and use the return value of the\n    visitor methods to replace or remove the old node.  If the return value of\n    the visitor method is ``None``, the node will be removed from its location,\n    otherwise it is replaced with the return value.  The return value may be the\n    original node in which case no replacement takes place.\n\n    Here is an example transformer that rewrites all occurrences of name lookups\n    (``foo``) to ``data['foo']``::\n\n       class RewriteName(NodeTransformer):\n\n           def visit_Name(self, node):\n               return copy_location(Subscript(\n                   value=Name(id='data', ctx=Load()),\n                   slice=Index(value=Str(s=node.id)),\n                   ctx=node.ctx\n               ), node)\n\n    Keep in mind that if the node you're operating on has child nodes you must\n    either transform the child nodes yourself or call the :meth:`generic_visit`\n    method for the node first.\n\n    For nodes that were part of a collection of statements (that applies to all\n    statement nodes), the visitor may also return a list of nodes rather than\n    just a single node.\n\n    Usually you use the transformer like this::\n\n       node = YourTransformer().visit(node)\n    "

    def generic_visit--- This code section failed: ---

 L. 431         0  LOAD_GLOBAL              iter_fields
                2  LOAD_FAST                'node'
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
              8_0  COME_FROM           126  '126'
                8  FOR_ITER            172  'to 172'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'field'
               14  STORE_FAST               'old_value'

 L. 432        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'old_value'
               20  LOAD_GLOBAL              list
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE   118  'to 118'

 L. 433        26  BUILD_LIST_0          0 
               28  STORE_FAST               'new_values'

 L. 434        30  LOAD_FAST                'old_value'
               32  GET_ITER         
               34  FOR_ITER            104  'to 104'
               36  STORE_FAST               'value'

 L. 435        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'value'
               42  LOAD_GLOBAL              AST
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    92  'to 92'

 L. 436        48  LOAD_FAST                'self'
               50  LOAD_METHOD              visit
               52  LOAD_FAST                'value'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'value'

 L. 437        58  LOAD_FAST                'value'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 438        66  JUMP_BACK            34  'to 34'
               68  JUMP_FORWARD         92  'to 92'
             70_0  COME_FROM            64  '64'

 L. 439        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'value'
               74  LOAD_GLOBAL              AST
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_TRUE     92  'to 92'

 L. 440        80  LOAD_FAST                'new_values'
               82  LOAD_METHOD              extend
               84  LOAD_FAST                'value'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L. 441        90  JUMP_BACK            34  'to 34'
             92_0  COME_FROM            78  '78'
             92_1  COME_FROM            68  '68'
             92_2  COME_FROM            46  '46'

 L. 442        92  LOAD_FAST                'new_values'
               94  LOAD_METHOD              append
               96  LOAD_FAST                'value'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  JUMP_BACK            34  'to 34'

 L. 443       104  LOAD_FAST                'new_values'
              106  LOAD_FAST                'old_value'
              108  LOAD_CONST               None
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  STORE_SUBSCR     
              116  JUMP_BACK             8  'to 8'
            118_0  COME_FROM            24  '24'

 L. 444       118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'old_value'
              122  LOAD_GLOBAL              AST
              124  CALL_FUNCTION_2       2  ''
              126  POP_JUMP_IF_FALSE     8  'to 8'

 L. 445       128  LOAD_FAST                'self'
              130  LOAD_METHOD              visit
              132  LOAD_FAST                'old_value'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'new_node'

 L. 446       138  LOAD_FAST                'new_node'
              140  LOAD_CONST               None
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   158  'to 158'

 L. 447       146  LOAD_GLOBAL              delattr
              148  LOAD_FAST                'node'
              150  LOAD_FAST                'field'
              152  CALL_FUNCTION_2       2  ''
              154  POP_TOP          
              156  JUMP_BACK             8  'to 8'
            158_0  COME_FROM           144  '144'

 L. 449       158  LOAD_GLOBAL              setattr
              160  LOAD_FAST                'node'
              162  LOAD_FAST                'field'
              164  LOAD_FAST                'new_node'
              166  CALL_FUNCTION_3       3  ''
              168  POP_TOP          
              170  JUMP_BACK             8  'to 8'

 L. 450       172  LOAD_FAST                'node'
              174  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 68


def _getter(self):
    return self.value


def _setter(self, value):
    self.value = value


Constant.n = property(_getter, _setter)
Constant.s = property(_getter, _setter)

class _ABC(type):

    def __instancecheck__(cls, inst):
        if not isinstance(inst, Constant):
            return False
        if cls in _const_types:
            try:
                value = inst.value
            except AttributeError:
                return False
            else:
                return isinstance(value, _const_types[cls]) and not isinstance(value, _const_types_not.get(cls, ()))
        return type.__instancecheck__(cls, inst)


def _new(cls, *args, **kwargs):
    if cls in _const_types:
        return Constant(*args, **kwargs)
    return (Constant.__new__)(cls, *args, **kwargs)


class Num(Constant, metaclass=_ABC):
    _fields = ('n', )
    __new__ = _new


class Str(Constant, metaclass=_ABC):
    _fields = ('s', )
    __new__ = _new


class Bytes(Constant, metaclass=_ABC):
    _fields = ('s', )
    __new__ = _new


class NameConstant(Constant, metaclass=_ABC):
    __new__ = _new


class Ellipsis(Constant, metaclass=_ABC):
    _fields = ()

    def __new__(cls, *args, **kwargs):
        if cls is Ellipsis:
            return Constant(Ellipsis, *args, **kwargs)
        return (Constant.__new__)(cls, *args, **kwargs)


_const_types = {Num: (int, float, complex), 
 Str: (str,), 
 Bytes: (bytes,), 
 NameConstant: (type(None), bool), 
 Ellipsis: (type(...),)}
_const_types_not = {Num: (bool,)}
_const_node_type_names = {bool: 'NameConstant', 
 type(None): 'NameConstant', 
 int: 'Num', 
 float: 'Num', 
 complex: 'Num', 
 str: 'Str', 
 bytes: 'Bytes', 
 type(...): 'Ellipsis'}