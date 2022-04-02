# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: C:\Users\illwill\Desktop\python\pyInstaller-2.1\MS14-40-x32\build\MS14-40-x32\out00-PYZ.pyz\pickle
"""Create portable serialized representations of Python objects.

See module cPickle for a (much) faster implementation.
See module copy_reg for a mechanism for registering custom picklers.
See module pickletools source for extensive comments.

Classes:

    Pickler
    Unpickler

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    __version__
    format_version
    compatible_formats

"""
__version__ = '$Revision: 72223 $'
from types import *
from copy_reg import dispatch_table
from copy_reg import _extension_registry, _inverted_registry, _extension_cache
import marshal, sys, struct, re
__all__ = [
 'PickleError', 'PicklingError', 'UnpicklingError', 'Pickler',
 'Unpickler', 'dump', 'dumps', 'load', 'loads']
format_version = '2.0'
compatible_formats = ['1.0',
 '1.1',
 '1.2',
 '1.3',
 '2.0']
HIGHEST_PROTOCOL = 2
mloads = marshal.loads

class PickleError(Exception):
    """A common base class for the other pickling exceptions."""
    pass


class PicklingError(PickleError):
    """This exception is raised when an unpicklable object is passed to the
    dump() method.

    """
    pass


class UnpicklingError(PickleError):
    """This exception is raised when there is a problem unpickling an object,
    such as a security violation.

    Note that other exceptions may also be raised during unpickling, including
    (but not necessarily limited to) AttributeError, EOFError, ImportError,
    and IndexError.

    """
    pass


class _Stop(Exception):

    def __init__(self, value):
        self.value = value


try:
    from org.python.core import PyStringMap
except ImportError:
    PyStringMap = None

try:
    UnicodeType
except NameError:
    UnicodeType = None

MARK = '('
STOP = '.'
POP = '0'
POP_MARK = '1'
DUP = '2'
FLOAT = 'F'
INT = 'I'
BININT = 'J'
BININT1 = 'K'
LONG = 'L'
BININT2 = 'M'
NONE = 'N'
PERSID = 'P'
BINPERSID = 'Q'
REDUCE = 'R'
STRING = 'S'
BINSTRING = 'T'
SHORT_BINSTRING = 'U'
UNICODE = 'V'
BINUNICODE = 'X'
APPEND = 'a'
BUILD = 'b'
GLOBAL = 'c'
DICT = 'd'
EMPTY_DICT = '}'
APPENDS = 'e'
GET = 'g'
BINGET = 'h'
INST = 'i'
LONG_BINGET = 'j'
LIST = 'l'
EMPTY_LIST = ']'
OBJ = 'o'
PUT = 'p'
BINPUT = 'q'
LONG_BINPUT = 'r'
SETITEM = 's'
TUPLE = 't'
EMPTY_TUPLE = ')'
SETITEMS = 'u'
BINFLOAT = 'G'
TRUE = 'I01\n'
FALSE = 'I00\n'
PROTO = b'\x80'
NEWOBJ = b'\x81'
EXT1 = b'\x82'
EXT2 = b'\x83'
EXT4 = b'\x84'
TUPLE1 = b'\x85'
TUPLE2 = b'\x86'
TUPLE3 = b'\x87'
NEWTRUE = b'\x88'
NEWFALSE = b'\x89'
LONG1 = b'\x8a'
LONG4 = b'\x8b'
_tuplesize2code = [
 EMPTY_TUPLE, TUPLE1, TUPLE2, TUPLE3]
__all__.extend([ x for x in dir() if re.match('[A-Z][A-Z0-9_]+$', x) ])
del x

class Pickler():

    def __init__(self, file, protocol=None):
        """This takes a file-like object for writing a pickle data stream.

        The optional protocol argument tells the pickler to use the
        given protocol; supported protocols are 0, 1, 2.  The default
        protocol is 0, to be backwards compatible.  (Protocol 0 is the
        only protocol that can be written to a file opened in text
        mode and read back successfully.  When using a protocol higher
        than 0, make sure the file is opened in binary mode, both when
        pickling and unpickling.)

        Protocol 1 is more efficient than protocol 0; protocol 2 is
        more efficient than protocol 1.

        Specifying a negative protocol version selects the highest
        protocol version supported.  The higher the protocol used, the
        more recent the version of Python needed to read the pickle
        produced.

        The file parameter must have a write() method that accepts a single
        string argument.  It can thus be an open file object, a StringIO
        object, or any other custom object that meets this interface.

        """
        if protocol is None:
            protocol = 0
        if protocol < 0:
            protocol = HIGHEST_PROTOCOL
        elif not 0 <= protocol <= HIGHEST_PROTOCOL:
            raise ValueError('pickle protocol must be <= %d' % HIGHEST_PROTOCOL)
        self.write = file.write
        self.memo = {}
        self.proto = int(protocol)
        self.bin = protocol >= 1
        self.fast = 0
        return

    def clear_memo(self):
        """Clears the pickler's "memo".

        The memo is the data structure that remembers which objects the
        pickler has already seen, so that shared or recursive objects are
        pickled by reference and not by value.  This method is useful when
        re-using picklers.

        """
        self.memo.clear()

    def dump(self, obj):
        """Write a pickled representation of obj to the open file."""
        if self.proto >= 2:
            self.write(PROTO + chr(self.proto))
        self.save(obj)
        self.write(STOP)

    def memoize(self, obj):
        """Store an object in the memo."""
        if self.fast:
            return
        assert id(obj) not in self.memo
        memo_len = len(self.memo)
        self.write(self.put(memo_len))
        self.memo[id(obj)] = (memo_len, obj)

    def put(self, i, pack=struct.pack):
        if self.bin:
            if i < 256:
                return BINPUT + chr(i)
            else:
                return LONG_BINPUT + pack('<i', i)

        return PUT + repr(i) + '\n'

    def get(self, i, pack=struct.pack):
        if self.bin:
            if i < 256:
                return BINGET + chr(i)
            else:
                return LONG_BINGET + pack('<i', i)

        return GET + repr(i) + '\n'

    def save(self, obj):
        pid = self.persistent_id(obj)
        if pid:
            self.save_pers(pid)
            return
        else:
            x = self.memo.get(id(obj))
            if x:
                self.write(self.get(x[0]))
                return
            t = type(obj)
            f = self.dispatch.get(t)
            if f:
                f(self, obj)
                return
            try:
                issc = issubclass(t, TypeType)
            except TypeError:
                issc = 0

            if issc:
                self.save_global(obj)
                return
            reduce = dispatch_table.get(t)
            if reduce:
                rv = reduce(obj)
            else:
                reduce = getattr(obj, '__reduce_ex__', None)
                if reduce:
                    rv = reduce(self.proto)
                else:
                    reduce = getattr(obj, '__reduce__', None)
                    if reduce:
                        rv = reduce()
                    else:
                        raise PicklingError("Can't pickle %r object: %r" % (
                         t.__name__, obj))
                if type(rv) is StringType:
                    self.save_global(obj, rv)
                    return
            if type(rv) is not TupleType:
                raise PicklingError('%s must return string or tuple' % reduce)
            l = len(rv)
            if not 2 <= l <= 5:
                raise PicklingError('Tuple returned by %s must have two to five elements' % reduce)
            self.save_reduce(obj=obj, *rv)
            return

    def persistent_id(self, obj):
        return

    def save_pers(self, pid):
        if self.bin:
            self.save(pid)
            self.write(BINPERSID)
        else:
            self.write(PERSID + str(pid) + '\n')

    def save_reduce(self, func, args, state=None, listitems=None, dictitems=None, obj=None):
        if not isinstance(args, TupleType):
            raise PicklingError('args from reduce() should be a tuple')
        if not hasattr(func, '__call__'):
            raise PicklingError('func from reduce should be callable')
        save = self.save
        write = self.write
        if self.proto >= 2 and getattr(func, '__name__', '') == '__newobj__':
            cls = args[0]
            if not hasattr(cls, '__new__'):
                raise PicklingError('args[0] from __newobj__ args has no __new__')
            if obj is not None and cls is not obj.__class__:
                raise PicklingError('args[0] from __newobj__ args has the wrong class')
            args = args[1:]
            save(cls)
            save(args)
            write(NEWOBJ)
        else:
            save(func)
            save(args)
            write(REDUCE)
        if obj is not None:
            self.memoize(obj)
        if listitems is not None:
            self._batch_appends(listitems)
        if dictitems is not None:
            self._batch_setitems(dictitems)
        if state is not None:
            save(state)
            write(BUILD)
        return

    dispatch = {}

    def save_none(self, obj):
        self.write(NONE)

    dispatch[NoneType] = save_none

    def save_bool(self, obj):
        if self.proto >= 2:
            self.write(obj and NEWTRUE or NEWFALSE)
        else:
            self.write(obj and TRUE or FALSE)

    dispatch[bool] = save_bool

    def save_int(self, obj, pack=struct.pack):
        if self.bin:
            if obj >= 0:
                if obj <= 255:
                    self.write(BININT1 + chr(obj))
                    return
                if obj <= 65535:
                    self.write('%c%c%c' % (BININT2, obj & 255, obj >> 8))
                    return
            high_bits = obj >> 31
            if high_bits == 0 or high_bits == -1:
                self.write(BININT + pack('<i', obj))
                return
        self.write(INT + repr(obj) + '\n')

    dispatch[IntType] = save_int

    def save_long(self, obj, pack=struct.pack):
        if self.proto >= 2:
            bytes = encode_long(obj)
            n = len(bytes)
            if n < 256:
                self.write(LONG1 + chr(n) + bytes)
            else:
                self.write(LONG4 + pack('<i', n) + bytes)
            return
        self.write(LONG + repr(obj) + '\n')

    dispatch[LongType] = save_long

    def save_float(self, obj, pack=struct.pack):
        if self.bin:
            self.write(BINFLOAT + pack('>d', obj))
        else:
            self.write(FLOAT + repr(obj) + '\n')

    dispatch[FloatType] = save_float

    def save_string(self, obj, pack=struct.pack):
        if self.bin:
            n = len(obj)
            if n < 256:
                self.write(SHORT_BINSTRING + chr(n) + obj)
            else:
                self.write(BINSTRING + pack('<i', n) + obj)
        else:
            self.write(STRING + repr(obj) + '\n')
        self.memoize(obj)

    dispatch[StringType] = save_string

    def save_unicode(self, obj, pack=struct.pack):
        if self.bin:
            encoding = obj.encode('utf-8')
            n = len(encoding)
            self.write(BINUNICODE + pack('<i', n) + encoding)
        else:
            obj = obj.replace('\\', '\\u005c')
            obj = obj.replace('\n', '\\u000a')
            self.write(UNICODE + obj.encode('raw-unicode-escape') + '\n')
        self.memoize(obj)

    dispatch[UnicodeType] = save_unicode
    if StringType is UnicodeType:

        def save_string(self, obj, pack=struct.pack):
            unicode = obj.isunicode()
            if self.bin:
                if unicode:
                    obj = obj.encode('utf-8')
                l = len(obj)
                if l < 256 and not unicode:
                    self.write(SHORT_BINSTRING + chr(l) + obj)
                else:
                    s = pack('<i', l)
                    if unicode:
                        self.write(BINUNICODE + s + obj)
                    else:
                        self.write(BINSTRING + s + obj)
            elif unicode:
                obj = obj.replace('\\', '\\u005c')
                obj = obj.replace('\n', '\\u000a')
                obj = obj.encode('raw-unicode-escape')
                self.write(UNICODE + obj + '\n')
            else:
                self.write(STRING + repr(obj) + '\n')
            self.memoize(obj)

        dispatch[StringType] = save_string

    def save_tuple(self, obj):
        write = self.write
        proto = self.proto
        n = len(obj)
        if n == 0:
            if proto:
                write(EMPTY_TUPLE)
            else:
                write(MARK + TUPLE)
            return
        save = self.save
        memo = self.memo
        if n <= 3 and proto >= 2:
            for element in obj:
                save(element)

            if id(obj) in memo:
                get = self.get(memo[id(obj)][0])
                write(POP * n + get)
            else:
                write(_tuplesize2code[n])
                self.memoize(obj)
            return
        write(MARK)
        for element in obj:
            save(element)

        if id(obj) in memo:
            get = self.get(memo[id(obj)][0])
            if proto:
                write(POP_MARK + get)
            else:
                write(POP * (n + 1) + get)
            return
        self.write(TUPLE)
        self.memoize(obj)

    dispatch[TupleType] = save_tuple

    def save_empty_tuple(self, obj):
        self.write(EMPTY_TUPLE)

    def save_list(self, obj):
        write = self.write
        if self.bin:
            write(EMPTY_LIST)
        else:
            write(MARK + LIST)
        self.memoize(obj)
        self._batch_appends(iter(obj))

    dispatch[ListType] = save_list
    _BATCHSIZE = 1000

    def _batch_appends(self, items):
        save = self.save
        write = self.write
        if not self.bin:
            for x in items:
                save(x)
                write(APPEND)

            return
        r = xrange(self._BATCHSIZE)
        while items is not None:
            tmp = []
            for i in r:
                try:
                    x = items.next()
                    tmp.append(x)
                except StopIteration:
                    items = None
                    break

            n = len(tmp)
            if n > 1:
                write(MARK)
                for x in tmp:
                    save(x)

                write(APPENDS)
            elif n:
                save(tmp[0])
                write(APPEND)

        return

    def save_dict(self, obj):
        write = self.write
        if self.bin:
            write(EMPTY_DICT)
        else:
            write(MARK + DICT)
        self.memoize(obj)
        self._batch_setitems(obj.iteritems())

    dispatch[DictionaryType] = save_dict
    if PyStringMap is not None:
        dispatch[PyStringMap] = save_dict

    def _batch_setitems(self, items):
        save = self.save
        write = self.write
        if not self.bin:
            for k, v in items:
                save(k)
                save(v)
                write(SETITEM)

            return
        r = xrange(self._BATCHSIZE)
        while items is not None:
            tmp = []
            for i in r:
                try:
                    tmp.append(items.next())
                except StopIteration:
                    items = None
                    break

            n = len(tmp)
            if n > 1:
                write(MARK)
                for k, v in tmp:
                    save(k)
                    save(v)

                write(SETITEMS)
            elif n:
                k, v = tmp[0]
                save(k)
                save(v)
                write(SETITEM)

        return

    def save_inst(self, obj):
        cls = obj.__class__
        memo = self.memo
        write = self.write
        save = self.save
        if hasattr(obj, '__getinitargs__'):
            args = obj.__getinitargs__()
            len(args)
            _keep_alive(args, memo)
        else:
            args = ()
        write(MARK)
        if self.bin:
            save(cls)
            for arg in args:
                save(arg)

            write(OBJ)
        else:
            for arg in args:
                save(arg)

            write(INST + cls.__module__ + '\n' + cls.__name__ + '\n')
        self.memoize(obj)
        try:
            getstate = obj.__getstate__
        except AttributeError:
            stuff = obj.__dict__
        else:
            stuff = getstate()
            _keep_alive(stuff, memo)

        save(stuff)
        write(BUILD)

    dispatch[InstanceType] = save_inst

    def save_global(self, obj, name=None, pack=struct.pack):
        write = self.write
        memo = self.memo
        if name is None:
            name = obj.__name__
        module = getattr(obj, '__module__', None)
        if module is None:
            module = whichmodule(obj, name)
        try:
            __import__(module)
            mod = sys.modules[module]
            klass = getattr(mod, name)
        except (ImportError, KeyError, AttributeError):
            raise PicklingError("Can't pickle %r: it's not found as %s.%s" % (
             obj, module, name))

        if klass is not obj:
            raise PicklingError("Can't pickle %r: it's not the same object as %s.%s" % (
             obj, module, name))
        if self.proto >= 2:
            code = _extension_registry.get((module, name))
            if code:
                assert code > 0
                if code <= 255:
                    write(EXT1 + chr(code))
                elif code <= 65535:
                    write('%c%c%c' % (EXT2, code & 255, code >> 8))
                else:
                    write(EXT4 + pack('<i', code))
                return
        write(GLOBAL + module + '\n' + name + '\n')
        self.memoize(obj)
        return

    dispatch[ClassType] = save_global
    dispatch[FunctionType] = save_global
    dispatch[BuiltinFunctionType] = save_global
    dispatch[TypeType] = save_global


def _keep_alive(x, memo):
    """Keeps a reference to the object x in the memo.

    Because we remember objects by their id, we have
    to assure that possibly temporary objects are kept
    alive by referencing them.
    We store a reference at the id of the memo, which should
    normally not be used unless someone tries to deepcopy
    the memo itself...
    """
    try:
        memo[id(memo)].append(x)
    except KeyError:
        memo[id(memo)] = [
         x]


classmap = {}

def whichmodule(func, funcname):
    """Figure out the module in which a function occurs.

    Search sys.modules for the module.
    Cache in classmap.
    Return a module name.
    If the function cannot be found, return "__main__".
    """
    mod = getattr(func, '__module__', None)
    if mod is not None:
        return mod
    else:
        if func in classmap:
            return classmap[func]
        for name, module in sys.modules.items():
            if module is None:
                continue
            if name != '__main__' and getattr(module, funcname, None) is func:
                break
        else:
            name = '__main__'

        classmap[func] = name
        return name


class Unpickler():

    def __init__(self, file):
        """This takes a file-like object for reading a pickle data stream.

        The protocol version of the pickle is detected automatically, so no
        proto argument is needed.

        The file-like object must have two methods, a read() method that
        takes an integer argument, and a readline() method that requires no
        arguments.  Both methods should return a string.  Thus file-like
        object can be a file object opened for reading, a StringIO object,
        or any other custom object that meets this interface.
        """
        self.readline = file.readline
        self.read = file.read
        self.memo = {}

    def load(self):
        """Read a pickled object representation from the open file.

        Return the reconstituted object hierarchy specified in the file.
        """
        self.mark = object()
        self.stack = []
        self.append = self.stack.append
        read = self.read
        dispatch = self.dispatch
        try:
            while 1:
                key = read(1)
                dispatch[key](self)

        except _Stop as stopinst:
            return stopinst.value

    def marker(self):
        stack = self.stack
        mark = self.mark
        k = len(stack) - 1
        while stack[k] is not mark:
            k = k - 1

        return k

    dispatch = {}

    def load_eof(self):
        raise EOFError

    dispatch[''] = load_eof

    def load_proto(self):
        proto = ord(self.read(1))
        if not 0 <= proto <= 2:
            raise ValueError, 'unsupported pickle protocol: %d' % proto

    dispatch[PROTO] = load_proto

    def load_persid(self):
        pid = self.readline()[:-1]
        self.append(self.persistent_load(pid))

    dispatch[PERSID] = load_persid

    def load_binpersid(self):
        pid = self.stack.pop()
        self.append(self.persistent_load(pid))

    dispatch[BINPERSID] = load_binpersid

    def load_none(self):
        self.append(None)
        return

    dispatch[NONE] = load_none

    def load_false(self):
        self.append(False)

    dispatch[NEWFALSE] = load_false

    def load_true(self):
        self.append(True)

    dispatch[NEWTRUE] = load_true

    def load_int(self):
        data = self.readline()
        if data == FALSE[1:]:
            val = False
        elif data == TRUE[1:]:
            val = True
        else:
            try:
                val = int(data)
            except ValueError:
                val = long(data)

        self.append(val)

    dispatch[INT] = load_int

    def load_binint(self):
        self.append(mloads('i' + self.read(4)))

    dispatch[BININT] = load_binint

    def load_binint1(self):
        self.append(ord(self.read(1)))

    dispatch[BININT1] = load_binint1

    def load_binint2(self):
        self.append(mloads('i' + self.read(2) + '\x00\x00'))

    dispatch[BININT2] = load_binint2

    def load_long(self):
        self.append(long(self.readline()[:-1], 0))

    dispatch[LONG] = load_long

    def load_long1(self):
        n = ord(self.read(1))
        bytes = self.read(n)
        self.append(decode_long(bytes))

    dispatch[LONG1] = load_long1

    def load_long4(self):
        n = mloads('i' + self.read(4))
        bytes = self.read(n)
        self.append(decode_long(bytes))

    dispatch[LONG4] = load_long4

    def load_float(self):
        self.append(float(self.readline()[:-1]))

    dispatch[FLOAT] = load_float

    def load_binfloat(self, unpack=struct.unpack):
        self.append(unpack('>d', self.read(8))[0])

    dispatch[BINFLOAT] = load_binfloat

    def load_string(self):
        rep = self.readline()[:-1]
        for q in '"\'':
            if rep.startswith(q):
                if not rep.endswith(q):
                    raise ValueError, 'insecure string pickle'
                rep = rep[len(q):-len(q)]
                break
        else:
            raise ValueError, 'insecure string pickle'

        self.append(rep.decode('string-escape'))

    dispatch[STRING] = load_string

    def load_binstring(self):
        len = mloads('i' + self.read(4))
        self.append(self.read(len))

    dispatch[BINSTRING] = load_binstring

    def load_unicode(self):
        self.append(unicode(self.readline()[:-1], 'raw-unicode-escape'))

    dispatch[UNICODE] = load_unicode

    def load_binunicode(self):
        len = mloads('i' + self.read(4))
        self.append(unicode(self.read(len), 'utf-8'))

    dispatch[BINUNICODE] = load_binunicode

    def load_short_binstring(self):
        len = ord(self.read(1))
        self.append(self.read(len))

    dispatch[SHORT_BINSTRING] = load_short_binstring

    def load_tuple(self):
        k = self.marker()
        self.stack[k:] = [tuple(self.stack[k + 1:])]

    dispatch[TUPLE] = load_tuple

    def load_empty_tuple(self):
        self.stack.append(())

    dispatch[EMPTY_TUPLE] = load_empty_tuple

    def load_tuple1(self):
        self.stack[-1] = (
         self.stack[(-1)],)

    dispatch[TUPLE1] = load_tuple1

    def load_tuple2(self):
        self.stack[(-2):] = [
         (
          self.stack[(-2)], self.stack[(-1)])]

    dispatch[TUPLE2] = load_tuple2

    def load_tuple3(self):
        self.stack[(-3):] = [
         (
          self.stack[(-3)], self.stack[(-2)], self.stack[(-1)])]

    dispatch[TUPLE3] = load_tuple3

    def load_empty_list(self):
        self.stack.append([])

    dispatch[EMPTY_LIST] = load_empty_list

    def load_empty_dictionary(self):
        self.stack.append({})

    dispatch[EMPTY_DICT] = load_empty_dictionary

    def load_list(self):
        k = self.marker()
        self.stack[k:] = [self.stack[k + 1:]]

    dispatch[LIST] = load_list

    def load_dict(self):
        k = self.marker()
        d = {}
        items = self.stack[k + 1:]
        for i in range(0, len(items), 2):
            key = items[i]
            value = items[(i + 1)]
            d[key] = value

        self.stack[k:] = [
         d]

    dispatch[DICT] = load_dict

    def _instantiate(self, klass, k):
        args = tuple(self.stack[k + 1:])
        del self.stack[k:]
        instantiated = 0
        if not args and type(klass) is ClassType and not hasattr(klass, '__getinitargs__'):
            try:
                value = _EmptyClass()
                value.__class__ = klass
                instantiated = 1
            except RuntimeError:
                pass

        if not instantiated:
            try:
                value = klass(*args)
            except TypeError as err:
                raise TypeError, 'in constructor for %s: %s' % (
                 klass.__name__, str(err)), sys.exc_info()[2]

        self.append(value)

    def load_inst(self):
        module = self.readline()[:-1]
        name = self.readline()[:-1]
        klass = self.find_class(module, name)
        self._instantiate(klass, self.marker())

    dispatch[INST] = load_inst

    def load_obj(self):
        k = self.marker()
        klass = self.stack.pop(k + 1)
        self._instantiate(klass, k)

    dispatch[OBJ] = load_obj

    def load_newobj(self):
        args = self.stack.pop()
        cls = self.stack[(-1)]
        obj = cls.__new__(cls, *args)
        self.stack[-1] = obj

    dispatch[NEWOBJ] = load_newobj

    def load_global(self):
        module = self.readline()[:-1]
        name = self.readline()[:-1]
        klass = self.find_class(module, name)
        self.append(klass)

    dispatch[GLOBAL] = load_global

    def load_ext1(self):
        code = ord(self.read(1))
        self.get_extension(code)

    dispatch[EXT1] = load_ext1

    def load_ext2(self):
        code = mloads('i' + self.read(2) + '\x00\x00')
        self.get_extension(code)

    dispatch[EXT2] = load_ext2

    def load_ext4(self):
        code = mloads('i' + self.read(4))
        self.get_extension(code)

    dispatch[EXT4] = load_ext4

    def get_extension(self, code):
        nil = []
        obj = _extension_cache.get(code, nil)
        if obj is not nil:
            self.append(obj)
            return
        key = _inverted_registry.get(code)
        if not key:
            raise ValueError('unregistered extension code %d' % code)
        obj = self.find_class(*key)
        _extension_cache[code] = obj
        self.append(obj)

    def find_class(self, module, name):
        __import__(module)
        mod = sys.modules[module]
        klass = getattr(mod, name)
        return klass

    def load_reduce(self):
        stack = self.stack
        args = stack.pop()
        func = stack[(-1)]
        value = func(*args)
        stack[-1] = value

    dispatch[REDUCE] = load_reduce

    def load_pop(self):
        del self.stack[-1]

    dispatch[POP] = load_pop

    def load_pop_mark(self):
        k = self.marker()
        del self.stack[k:]

    dispatch[POP_MARK] = load_pop_mark

    def load_dup(self):
        self.append(self.stack[(-1)])

    dispatch[DUP] = load_dup

    def load_get(self):
        self.append(self.memo[self.readline()[:-1]])

    dispatch[GET] = load_get

    def load_binget(self):
        i = ord(self.read(1))
        self.append(self.memo[repr(i)])

    dispatch[BINGET] = load_binget

    def load_long_binget(self):
        i = mloads('i' + self.read(4))
        self.append(self.memo[repr(i)])

    dispatch[LONG_BINGET] = load_long_binget

    def load_put(self):
        self.memo[self.readline()[:-1]] = self.stack[(-1)]

    dispatch[PUT] = load_put

    def load_binput(self):
        i = ord(self.read(1))
        self.memo[repr(i)] = self.stack[(-1)]

    dispatch[BINPUT] = load_binput

    def load_long_binput(self):
        i = mloads('i' + self.read(4))
        self.memo[repr(i)] = self.stack[(-1)]

    dispatch[LONG_BINPUT] = load_long_binput

    def load_append(self):
        stack = self.stack
        value = stack.pop()
        list = stack[(-1)]
        list.append(value)

    dispatch[APPEND] = load_append

    def load_appends(self):
        stack = self.stack
        mark = self.marker()
        list = stack[(mark - 1)]
        list.extend(stack[mark + 1:])
        del stack[mark:]

    dispatch[APPENDS] = load_appends

    def load_setitem(self):
        stack = self.stack
        value = stack.pop()
        key = stack.pop()
        dict = stack[(-1)]
        dict[key] = value

    dispatch[SETITEM] = load_setitem

    def load_setitems(self):
        stack = self.stack
        mark = self.marker()
        dict = stack[(mark - 1)]
        for i in range(mark + 1, len(stack), 2):
            dict[stack[i]] = stack[(i + 1)]

        del stack[mark:]

    dispatch[SETITEMS] = load_setitems

    def load_build(self):
        stack = self.stack
        state = stack.pop()
        inst = stack[(-1)]
        setstate = getattr(inst, '__setstate__', None)
        if setstate:
            setstate(state)
            return
        else:
            slotstate = None
            if isinstance(state, tuple) and len(state) == 2:
                state, slotstate = state
            if state:
                try:
                    d = inst.__dict__
                    try:
                        for k, v in state.iteritems():
                            d[intern(k)] = v

                    except TypeError:
                        d.update(state)

                except RuntimeError:
                    for k, v in state.items():
                        setattr(inst, k, v)

            if slotstate:
                for k, v in slotstate.items():
                    setattr(inst, k, v)

            return

    dispatch[BUILD] = load_build

    def load_mark(self):
        self.append(self.mark)

    dispatch[MARK] = load_mark

    def load_stop(self):
        value = self.stack.pop()
        raise _Stop(value)

    dispatch[STOP] = load_stop


class _EmptyClass():
    pass


import binascii as _binascii

def encode_long--- This code section failed: ---

 L.1290         0  LOAD_FAST             0  'x'
                3  LOAD_CONST               0
                6  COMPARE_OP            2  ==
                9  POP_JUMP_IF_FALSE    16  'to 16'

 L.1291        12  LOAD_CONST               ''
               15  RETURN_END_IF    
             16_0  COME_FROM             9  '9'

 L.1292        16  LOAD_FAST             0  'x'
               19  LOAD_CONST               0
               22  COMPARE_OP            4  >
               25  POP_JUMP_IF_FALSE   168  'to 168'

 L.1293        28  LOAD_GLOBAL           0  'hex'
               31  LOAD_FAST             0  'x'
               34  CALL_FUNCTION_1       1  None
               37  STORE_FAST            1  'ashex'

 L.1294        40  LOAD_FAST             1  'ashex'
               43  LOAD_ATTR             1  'startswith'
               46  LOAD_CONST               '0x'
               49  CALL_FUNCTION_1       1  None
               52  POP_JUMP_IF_TRUE     61  'to 61'
               55  LOAD_ASSERT              AssertionError
               58  RAISE_VARARGS_1       1  None

 L.1295        61  LOAD_CONST               2
               64  LOAD_FAST             1  'ashex'
               67  LOAD_ATTR             3  'endswith'
               70  LOAD_CONST               'L'
               73  CALL_FUNCTION_1       1  None
               76  BINARY_ADD       
               77  STORE_FAST            2  'njunkchars'

 L.1296        80  LOAD_GLOBAL           4  'len'
               83  LOAD_FAST             1  'ashex'
               86  CALL_FUNCTION_1       1  None
               89  LOAD_FAST             2  'njunkchars'
               92  BINARY_SUBTRACT  
               93  STORE_FAST            3  'nibbles'

 L.1297        96  LOAD_FAST             3  'nibbles'
               99  LOAD_CONST               1
              102  BINARY_AND       
              103  POP_JUMP_IF_FALSE   123  'to 123'

 L.1299       106  LOAD_CONST               '0x0'
              109  LOAD_FAST             1  'ashex'
              112  LOAD_CONST               2
              115  SLICE+1          
              116  BINARY_ADD       
              117  STORE_FAST            1  'ashex'
              120  JUMP_ABSOLUTE       432  'to 432'

 L.1300       123  LOAD_GLOBAL           5  'int'
              126  LOAD_FAST             1  'ashex'
              129  LOAD_CONST               2
              132  BINARY_SUBSCR    
              133  LOAD_CONST               16
              136  CALL_FUNCTION_2       2  None
              139  LOAD_CONST               8
              142  COMPARE_OP            5  >=
              145  POP_JUMP_IF_FALSE   432  'to 432'

 L.1302       148  LOAD_CONST               '0x00'
              151  LOAD_FAST             1  'ashex'
              154  LOAD_CONST               2
              157  SLICE+1          
              158  BINARY_ADD       
              159  STORE_FAST            1  'ashex'
              162  JUMP_ABSOLUTE       432  'to 432'
              165  JUMP_FORWARD        264  'to 432'

 L.1307       168  LOAD_GLOBAL           0  'hex'
              171  LOAD_FAST             0  'x'
              174  UNARY_NEGATIVE   
              175  CALL_FUNCTION_1       1  None
              178  STORE_FAST            1  'ashex'

 L.1308       181  LOAD_FAST             1  'ashex'
              184  LOAD_ATTR             1  'startswith'
              187  LOAD_CONST               '0x'
              190  CALL_FUNCTION_1       1  None
              193  POP_JUMP_IF_TRUE    202  'to 202'
              196  LOAD_ASSERT              AssertionError
              199  RAISE_VARARGS_1       1  None

 L.1309       202  LOAD_CONST               2
              205  LOAD_FAST             1  'ashex'
              208  LOAD_ATTR             3  'endswith'
              211  LOAD_CONST               'L'
              214  CALL_FUNCTION_1       1  None
              217  BINARY_ADD       
              218  STORE_FAST            2  'njunkchars'

 L.1310       221  LOAD_GLOBAL           4  'len'
              224  LOAD_FAST             1  'ashex'
              227  CALL_FUNCTION_1       1  None
              230  LOAD_FAST             2  'njunkchars'
              233  BINARY_SUBTRACT  
              234  STORE_FAST            3  'nibbles'

 L.1311       237  LOAD_FAST             3  'nibbles'
              240  LOAD_CONST               1
              243  BINARY_AND       
              244  POP_JUMP_IF_FALSE   260  'to 260'

 L.1313       247  LOAD_FAST             3  'nibbles'
              250  LOAD_CONST               1
              253  INPLACE_ADD      
              254  STORE_FAST            3  'nibbles'
              257  JUMP_FORWARD          0  'to 260'
            260_0  COME_FROM           257  '257'

 L.1314       260  LOAD_FAST             3  'nibbles'
              263  LOAD_CONST               4
              266  BINARY_MULTIPLY  
              267  STORE_FAST            4  'nbits'

 L.1315       270  LOAD_FAST             0  'x'
              273  LOAD_CONST               1
              276  LOAD_FAST             4  'nbits'
              279  BINARY_LSHIFT    
              280  INPLACE_ADD      
              281  STORE_FAST            0  'x'

 L.1316       284  LOAD_FAST             0  'x'
              287  LOAD_CONST               0
              290  COMPARE_OP            4  >
              293  POP_JUMP_IF_TRUE    302  'to 302'
              296  LOAD_ASSERT              AssertionError
              299  RAISE_VARARGS_1       1  None

 L.1317       302  LOAD_GLOBAL           0  'hex'
              305  LOAD_FAST             0  'x'
              308  CALL_FUNCTION_1       1  None
              311  STORE_FAST            1  'ashex'

 L.1318       314  LOAD_CONST               2
              317  LOAD_FAST             1  'ashex'
              320  LOAD_ATTR             3  'endswith'
              323  LOAD_CONST               'L'
              326  CALL_FUNCTION_1       1  None
              329  BINARY_ADD       
              330  STORE_FAST            2  'njunkchars'

 L.1319       333  LOAD_GLOBAL           4  'len'
              336  LOAD_FAST             1  'ashex'
              339  CALL_FUNCTION_1       1  None
              342  LOAD_FAST             2  'njunkchars'
              345  BINARY_SUBTRACT  
              346  STORE_FAST            5  'newnibbles'

 L.1320       349  LOAD_FAST             5  'newnibbles'
              352  LOAD_FAST             3  'nibbles'
              355  COMPARE_OP            0  <
              358  POP_JUMP_IF_FALSE   390  'to 390'

 L.1321       361  LOAD_CONST               '0x'
              364  LOAD_CONST               '0'
              367  LOAD_FAST             3  'nibbles'
              370  LOAD_FAST             5  'newnibbles'
              373  BINARY_SUBTRACT  
              374  BINARY_MULTIPLY  
              375  BINARY_ADD       
              376  LOAD_FAST             1  'ashex'
              379  LOAD_CONST               2
              382  SLICE+1          
              383  BINARY_ADD       
              384  STORE_FAST            1  'ashex'
              387  JUMP_FORWARD          0  'to 390'
            390_0  COME_FROM           387  '387'

 L.1322       390  LOAD_GLOBAL           5  'int'
              393  LOAD_FAST             1  'ashex'
              396  LOAD_CONST               2
              399  BINARY_SUBSCR    
              400  LOAD_CONST               16
              403  CALL_FUNCTION_2       2  None
              406  LOAD_CONST               8
              409  COMPARE_OP            0  <
              412  POP_JUMP_IF_FALSE   432  'to 432'

 L.1324       415  LOAD_CONST               '0xff'
              418  LOAD_FAST             1  'ashex'
              421  LOAD_CONST               2
              424  SLICE+1          
              425  BINARY_ADD       
              426  STORE_FAST            1  'ashex'
              429  JUMP_FORWARD          0  'to 432'
            432_0  COME_FROM           429  '429'
            432_1  COME_FROM           165  '165'

 L.1326       432  LOAD_FAST             1  'ashex'
              435  LOAD_ATTR             3  'endswith'
              438  LOAD_CONST               'L'
              441  CALL_FUNCTION_1       1  None
              444  POP_JUMP_IF_FALSE   463  'to 463'

 L.1327       447  LOAD_FAST             1  'ashex'
              450  LOAD_CONST               2
              453  LOAD_CONST               -1
              456  SLICE+3          
              457  STORE_FAST            1  'ashex'
              460  JUMP_FORWARD         10  'to 473'

 L.1329       463  LOAD_FAST             1  'ashex'
              466  LOAD_CONST               2
              469  SLICE+1          
              470  STORE_FAST            1  'ashex'
            473_0  COME_FROM           460  '460'

 L.1330       473  LOAD_GLOBAL           4  'len'
              476  LOAD_FAST             1  'ashex'
              479  CALL_FUNCTION_1       1  None
              482  LOAD_CONST               1
              485  BINARY_AND       
              486  LOAD_CONST               0
              489  COMPARE_OP            2  ==
              492  POP_JUMP_IF_TRUE    510  'to 510'
              495  LOAD_ASSERT              AssertionError
              498  LOAD_FAST             0  'x'
              501  LOAD_FAST             1  'ashex'
              504  BUILD_TUPLE_2         2 
              507  RAISE_VARARGS_2       2  None

 L.1331       510  LOAD_GLOBAL           6  '_binascii'
              513  LOAD_ATTR             7  'unhexlify'
              516  LOAD_FAST             1  'ashex'
              519  CALL_FUNCTION_1       1  None
              522  STORE_FAST            6  'binary'

 L.1332       525  LOAD_FAST             6  'binary'
              528  LOAD_CONST               None
              531  LOAD_CONST               None
              534  LOAD_CONST               -1
              537  BUILD_SLICE_3         3 
              540  BINARY_SUBSCR    
              541  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 541


def decode_long(data):
    r"""Decode a long from a two's complement little-endian binary string.

    >>> decode_long('')
    0L
    >>> decode_long("\xff\x00")
    255L
    >>> decode_long("\xff\x7f")
    32767L
    >>> decode_long("\x00\xff")
    -256L
    >>> decode_long("\x00\x80")
    -32768L
    >>> decode_long("\x80")
    -128L
    >>> decode_long("\x7f")
    127L
    """
    nbytes = len(data)
    if nbytes == 0:
        return 0
    ashex = _binascii.hexlify(data[::-1])
    n = long(ashex, 16)
    if data[(-1)] >= b'\x80':
        n -= 1 << nbytes * 8
    return n


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def dump(obj, file, protocol=None):
    Pickler(file, protocol).dump(obj)


def dumps(obj, protocol=None):
    file = StringIO()
    Pickler(file, protocol).dump(obj)
    return file.getvalue()


def load(file):
    return Unpickler(file).load()


def loads(str):
    file = StringIO(str)
    return Unpickler(file).load()


def _test():
    import doctest
    return doctest.testmod()


if __name__ == '__main__':
    _test()