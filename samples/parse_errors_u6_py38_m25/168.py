# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pprint.py
"""Support to pretty-print lists, tuples, & dictionaries recursively.

Very simple, but useful, especially in debugging data structures.

Classes
-------

PrettyPrinter()
    Handle pretty-printing operations onto a stream using a configured
    set of formatting parameters.

Functions
---------

pformat()
    Format a Python object into a pretty-printed representation.

pprint()
    Pretty-print a Python object to a stream [default is sys.stdout].

saferepr()
    Generate a 'standard' repr()-like value, but protect against recursive
    data structures.

"""
import collections as _collections, re, sys as _sys, types as _types
from io import StringIO as _StringIO
__all__ = [
 'pprint', 'pformat', 'isreadable', 'isrecursive', 'saferepr',
 'PrettyPrinter', 'pp']

def pprint(object, stream=None, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = PrettyPrinter(stream=stream,
      indent=indent,
      width=width,
      depth=depth,
      compact=compact,
      sort_dicts=sort_dicts)
    printer.pprint(object)


def pformat(object, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True):
    """Format a Python object into a pretty-printed representation."""
    return PrettyPrinter(indent=indent, width=width, depth=depth, compact=compact,
      sort_dicts=sort_dicts).pformat(object)


def pp(object, *args, sort_dicts=False, **kwargs):
    """Pretty-print a Python object"""
    pprint(object, *args, sort_dicts=sort_dicts, **kwargs)


def saferepr(object):
    """Version of repr() which can handle recursive data structures."""
    return _safe_repr(object, {}, None, 0, True)[0]


def isreadable(object):
    """Determine if saferepr(object) is readable by eval()."""
    return _safe_repr(object, {}, None, 0, True)[1]


def isrecursive(object):
    """Determine if object requires a recursive representation."""
    return _safe_repr(object, {}, None, 0, True)[2]


class _safe_key:
    __doc__ = 'Helper function for key functions when sorting unorderable objects.\n\n    The wrapped-object will fallback to a Py2.x style comparison for\n    unorderable types (sorting first comparing the type name and then by\n    the obj ids).  Does not work recursively, so dict.items() must have\n    _safe_key applied to both the key and the value.\n\n    '
    __slots__ = [
     'obj']

    def __init__(self, obj):
        self.obj = obj

    def __lt__--- This code section failed: ---

 L.  93         0  SETUP_FINALLY        16  'to 16'

 L.  94         2  LOAD_FAST                'self'
                4  LOAD_ATTR                obj
                6  LOAD_FAST                'other'
                8  LOAD_ATTR                obj
               10  COMPARE_OP               <
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  95        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    82  'to 82'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  96        30  LOAD_GLOBAL              str
               32  LOAD_GLOBAL              type
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                obj
               38  CALL_FUNCTION_1       1  ''
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_GLOBAL              id
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                obj
               48  CALL_FUNCTION_1       1  ''
               50  BUILD_TUPLE_2         2 

 L.  97        52  LOAD_GLOBAL              str
               54  LOAD_GLOBAL              type
               56  LOAD_FAST                'other'
               58  LOAD_ATTR                obj
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_GLOBAL              id
               66  LOAD_FAST                'other'
               68  LOAD_ATTR                obj
               70  CALL_FUNCTION_1       1  ''
               72  BUILD_TUPLE_2         2 

 L.  96        74  COMPARE_OP               <
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  RETURN_VALUE     
             82_0  COME_FROM            22  '22'
               82  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


def _safe_tuple(t):
    """Helper function for comparing 2-tuples"""
    return (
     _safe_key(t[0]), _safe_key(t[1]))


class PrettyPrinter:

    def __init__(self, indent=1, width=80, depth=None, stream=None, *, compact=False, sort_dicts=True):
        """Handle pretty printing operations onto a stream using a set of
        configured parameters.

        indent
            Number of spaces to indent for each level of nesting.

        width
            Attempted maximum number of columns in the output.

        depth
            The maximum depth to print out nested structures.

        stream
            The desired output stream.  If omitted (or false), the standard
            output stream available at construction will be used.

        compact
            If true, several items will be combined in one line.

        sort_dicts
            If true, dict keys are sorted.

        """
        indent = int(indent)
        width = int(width)
        if indent < 0:
            raise ValueError('indent must be >= 0')
        elif depth is not None:
            if depth <= 0:
                raise ValueError('depth must be > 0')
            else:
                assert width, 'width must be != 0'
            self._depth = depth
            self._indent_per_level = indent
            self._width = width
            if stream is not None:
                self._stream = stream
        else:
            self._stream = _sys.stdout
        self._compact = bool(compact)
        self._sort_dicts = sort_dicts

    def pprint(self, object):
        self._format(object, self._stream, 0, 0, {}, 0)
        self._stream.write('\n')

    def pformat(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]

    def isreadable(self, object):
        s, readable, recursive = self.format(object, {}, 0, 0)
        return readable and not recursive

    def _format(self, object, stream, indent, allowance, context, level):
        objid = id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        rep = self._repr(object, context, level)
        max_width = self._width - indent - allowance
        if len(rep) > max_width:
            p = self._dispatch.get(type(object).__repr__, None)
            if p is not None:
                context[objid] = 1
                p(self, object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
            if isinstance(object, dict):
                context[objid] = 1
                self._pprint_dict(object, stream, indent, allowance, context, level + 1)
                del context[objid]
                return
        stream.write(rep)

    _dispatch = {}

    def _pprint_dict(self, object, stream, indent, allowance, context, level):
        write = stream.write
        write('{')
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        length = len(object)
        if length:
            if self._sort_dicts:
                items = sorted((object.items()), key=_safe_tuple)
            else:
                items = object.items()
            self._format_dict_items(items, stream, indent, allowance + 1, context, level)
        write('}')

    _dispatch[dict.__repr__] = _pprint_dict

    def _pprint_ordered_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        self._format(list(object.items()), stream, indent + len(cls.__name__) + 1, allowance + 1, context, level)
        stream.write(')')

    _dispatch[_collections.OrderedDict.__repr__] = _pprint_ordered_dict

    def _pprint_list(self, object, stream, indent, allowance, context, level):
        stream.write('[')
        self._format_items(object, stream, indent, allowance + 1, context, level)
        stream.write(']')

    _dispatch[list.__repr__] = _pprint_list

    def _pprint_tuple(self, object, stream, indent, allowance, context, level):
        stream.write('(')
        endchar = ',)' if len(object) == 1 else ')'
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(endchar)

    _dispatch[tuple.__repr__] = _pprint_tuple

    def _pprint_set(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        else:
            typ = object.__class__
            if typ is set:
                stream.write('{')
                endchar = '}'
            else:
                stream.write(typ.__name__ + '({')
            endchar = '})'
            indent += len(typ.__name__) + 1
        object = sorted(object, key=_safe_key)
        self._format_items(object, stream, indent, allowance + len(endchar), context, level)
        stream.write(endchar)

    _dispatch[set.__repr__] = _pprint_set
    _dispatch[frozenset.__repr__] = _pprint_set

    def _pprint_str(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if not len(object):
            write(repr(object))
            return None
        chunks = []
        lines = object.splitlines(True)
        if level == 1:
            indent += 1
            allowance += 1
        max_width1 = max_width = self._width - indent
        for i, line in enumerate(lines):
            rep = repr(line)
            if i == len(lines) - 1:
                max_width1 -= allowance
            if len(rep) <= max_width1:
                chunks.append(rep)
        else:
            parts = re.findall('\\S*\\s*', line)
            assert parts
            assert not parts[-1]
            parts.pop()
            max_width2 = max_width
            current = ''

        for j, part in enumerate(parts):
            candidate = current + part
            if j == len(parts) - 1:
                if i == len(lines) - 1:
                    max_width2 -= allowance
                if len(repr(candidate)) > max_width2:
                    if current:
                        chunks.append(repr(current))
                    current = part
            else:
                current = candidate
        else:
            if current:
                chunks.append(repr(current))
            if len(chunks) == 1:
                write(rep)
                return None
            if level == 1:
                write('(')
            for i, rep in enumerate(chunks):
                if i > 0:
                    write('\n' + ' ' * indent)
                write(rep)
            else:
                if level == 1:
                    write(')')

    _dispatch[str.__repr__] = _pprint_str

    def _pprint_bytes(self, object, stream, indent, allowance, context, level):
        write = stream.write
        if len(object) <= 4:
            write(repr(object))
            return None
        parens = level == 1
        if parens:
            indent += 1
            allowance += 1
            write('(')
        delim = ''
        for rep in _wrap_bytes_repr(object, self._width - indent, allowance):
            write(delim)
            write(rep)
            if not delim:
                delim = '\n' + ' ' * indent
        else:
            if parens:
                write(')')

    _dispatch[bytes.__repr__] = _pprint_bytes

    def _pprint_bytearray(self, object, stream, indent, allowance, context, level):
        write = stream.write
        write('bytearray(')
        self._pprint_bytes(bytes(object), stream, indent + 10, allowance + 1, context, level + 1)
        write(')')

    _dispatch[bytearray.__repr__] = _pprint_bytearray

    def _pprint_mappingproxy(self, object, stream, indent, allowance, context, level):
        stream.write('mappingproxy(')
        self._format(object.copy(), stream, indent + 13, allowance + 1, context, level)
        stream.write(')')

    _dispatch[_types.MappingProxyType.__repr__] = _pprint_mappingproxy

    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        delimnl = ',\n' + ' ' * indent
        last_index = len(items) - 1
        for i, (key, ent) in enumerate(items):
            last = i == last_index
            rep = self._repr(key, context, level)
            write(rep)
            write(': ')
            self._format(ent, stream, indent + len(rep) + 2, allowance if last else 1, context, level)
            if not last:
                write(delimnl)

    def _format_items(self, items, stream, indent, allowance, context, level):
        write = stream.write
        indent += self._indent_per_level
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * ' ')
        delimnl = ',\n' + ' ' * indent
        delim = ''
        width = max_width = self._width - indent + 1
        it = iter(items)
        try:
            next_ent = next(it)
        except StopIteration:
            return
        else:
            last = False
            ent = last or next_ent
        try:
            next_ent = next(it)
        except StopIteration:
            last = True
            max_width -= allowance
            width -= allowance
        else:
            if self._compact:
                rep = self._repr(ent, context, level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                if width >= w:
                    width -= w
                    write(delim)
                    delim = ', '
                    write(rep)
            else:
                write(delim)
                delim = delimnl
                self._format(ent, stream, indent, allowance if last else 1, context, level)

    def _repr(self, object, context, level):
        repr, readable, recursive = self.format(object, context.copy(), self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the object represents a recursive construct.
        """
        return _safe_repr(object, context, maxlevels, level, self._sort_dicts)

    def _pprint_default_dict(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        rdf = self._repr(object.default_factory, context, level)
        cls = object.__class__
        indent += len(cls.__name__) + 1
        stream.write('%s(%s,\n%s' % (cls.__name__, rdf, ' ' * indent))
        self._pprint_dict(object, stream, indent, allowance + 1, context, level)
        stream.write(')')

    _dispatch[_collections.defaultdict.__repr__] = _pprint_default_dict

    def _pprint_counter(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(cls.__name__ + '({')
        if self._indent_per_level > 1:
            stream.write((self._indent_per_level - 1) * ' ')
        items = object.most_common()
        self._format_dict_items(items, stream, indent + len(cls.__name__) + 1, allowance + 2, context, level)
        stream.write('})')

    _dispatch[_collections.Counter.__repr__] = _pprint_counter

    def _pprint_chain_map(self, object, stream, indent, allowance, context, level):
        if not len(object.maps):
            stream.write(repr(object))
            return None
        cls = object.__class__
        stream.write(cls.__name__ + '(')
        indent += len(cls.__name__) + 1
        for i, m in enumerate(object.maps):
            if i == len(object.maps) - 1:
                self._format(m, stream, indent, allowance + 1, context, level)
                stream.write(')')
            else:
                self._format(m, stream, indent, 1, context, level)
                stream.write(',\n' + ' ' * indent)

    _dispatch[_collections.ChainMap.__repr__] = _pprint_chain_map

    def _pprint_deque(self, object, stream, indent, allowance, context, level):
        if not len(object):
            stream.write(repr(object))
            return None
        else:
            cls = object.__class__
            stream.write(cls.__name__ + '(')
            indent += len(cls.__name__) + 1
            stream.write('[')
            if object.maxlen is None:
                self._format_items(object, stream, indent, allowance + 2, context, level)
                stream.write('])')
            else:
                self._format_items(object, stream, indent, 2, context, level)
            rml = self._repr(object.maxlen, context, level)
            stream.write('],\n%smaxlen=%s)' % (' ' * indent, rml))

    _dispatch[_collections.deque.__repr__] = _pprint_deque

    def _pprint_user_dict(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserDict.__repr__] = _pprint_user_dict

    def _pprint_user_list(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserList.__repr__] = _pprint_user_list

    def _pprint_user_string(self, object, stream, indent, allowance, context, level):
        self._format(object.data, stream, indent, allowance, context, level - 1)

    _dispatch[_collections.UserString.__repr__] = _pprint_user_string


def _safe_repr(object, context, maxlevels, level, sort_dicts):
    typ = type(object)
    if typ in _builtin_scalars:
        return (
         repr(object), True, False)
        r = getattr(typ, '__repr__', None)
        if issubclass(typ, dict):
            if r is dict.__repr__ and not object:
                return ('{}', True, False)
                objid = id(object)
                if maxlevels:
                    if level >= maxlevels:
                        return (
                         '{...}', False, objid in context)
                if objid in context:
                    return (
                     _recursion(object), False, True)
    else:
        context[objid] = 1
        readable = True
        recursive = False
        components = []
        append = components.append
        level += 1
        if sort_dicts:
            items = sorted((object.items()), key=_safe_tuple)
        else:
            items = object.items()
    for k, v in items:
        krepr, kreadable, krecur = _safe_repr(k, context, maxlevels, level, sort_dicts)
        vrepr, vreadable, vrecur = _safe_repr(v, context, maxlevels, level, sort_dicts)
        append('%s: %s' % (krepr, vrepr))
        readable = readable and kreadable and vreadable
        if not krecur:
            if vrecur:
                recursive = True
            del context[objid]
            return ('{%s}' % ', '.join(components), readable, recursive)
        if issubclass(typ, list) and r is list.__repr__ or issubclass(typ, tuple):
            if r is tuple.__repr__:
                if issubclass(typ, list):
                    if not object:
                        return ('[]', True, False)
                    format = '[%s]'
                else:
                    if len(object) == 1:
                        format = '(%s,)'
                    else:
                        if not object:
                            return ('()', True, False)
                            format = '(%s)'
                        else:
                            objid = id(object)
                            if maxlevels and level >= maxlevels:
                                return (
                                 format % '...', False, objid in context)
                        if objid in context:
                            return (
                             _recursion(object), False, True)
                        context[objid] = 1
                        readable = True
                        recursive = False
                        components = []
                        append = components.append
                        level += 1
                        for o in object:
                            orepr, oreadable, orecur = _safe_repr(o, context, maxlevels, level, sort_dicts)
                            append(orepr)
                            if not oreadable:
                                readable = False
                            if orecur:
                                recursive = True
                            del context[objid]
                            return (format % ', '.join(components), readable, recursive)

        rep = repr(object)
        return (rep, rep and not rep.startswith('<'), False)


_builtin_scalars = frozenset({str, bytes, bytearray, int, float, complex,
 bool, type(None)})

def _recursion(object):
    return '<Recursion on %s with id=%s>' % (
     type(object).__name__, id(object))


def _perfcheck(object=None):
    import time
    if object is None:
        object = [
         (
          'string', (1, 2), [3, 4], {5:6,  7:8})] * 100000
    p = PrettyPrinter()
    t1 = time.perf_counter()
    _safe_repr(object, {}, None, 0, True)
    t2 = time.perf_counter()
    p.pformat(object)
    t3 = time.perf_counter()
    print('_safe_repr:', t2 - t1)
    print('pformat:', t3 - t2)


def _wrap_bytes_repr(object, width, allowance):
    current = b''
    last = len(object) // 4 * 4
    for i in range(0, len(object), 4):
        part = object[i:i + 4]
        candidate = current + part
        if i == last:
            width -= allowance
        if len(repr(candidate)) > width:
            if current:
                (yield repr(current))
            current = part
        else:
            current = candidate
    else:
        if current:
            (yield repr(current))


if __name__ == '__main__':
    _perfcheck()