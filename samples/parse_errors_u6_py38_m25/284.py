# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\sharedctypes.py
import ctypes, weakref
from . import heap
from . import get_context
from .context import reduction, assert_spawning
_ForkingPickler = reduction.ForkingPickler
__all__ = [
 'RawValue', 'RawArray', 'Value', 'Array', 'copy', 'synchronized']
typecode_to_type = {'c':ctypes.c_char, 
 'u':ctypes.c_wchar,  'b':ctypes.c_byte, 
 'B':ctypes.c_ubyte,  'h':ctypes.c_short, 
 'H':ctypes.c_ushort,  'i':ctypes.c_int, 
 'I':ctypes.c_uint,  'l':ctypes.c_long, 
 'L':ctypes.c_ulong,  'q':ctypes.c_longlong, 
 'Q':ctypes.c_ulonglong,  'f':ctypes.c_float, 
 'd':ctypes.c_double}

def _new_value(type_):
    size = ctypes.sizeof(type_)
    wrapper = heap.BufferWrapper(size)
    return rebuild_ctype(type_, wrapper, None)


def RawValue(typecode_or_type, *args):
    """
    Returns a ctypes object allocated from shared memory
    """
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    obj = _new_value(type_)
    ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
    (obj.__init__)(*args)
    return obj


def RawArray(typecode_or_type, size_or_initializer):
    """
    Returns a ctypes array allocated from shared memory
    """
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    if isinstance(size_or_initializer, int):
        type_ = type_ * size_or_initializer
        obj = _new_value(type_)
        ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
        return obj
    type_ = type_ * len(size_or_initializer)
    result = _new_value(type_)
    (result.__init__)(*size_or_initializer)
    return result


def Value(typecode_or_type, *args, lock=True, ctx=None):
    """
    Return a synchronization wrapper for a Value
    """
    obj = RawValue(typecode_or_type, *args)
    if lock is False:
        return obj
    if lock in (True, None):
        ctx = ctx or get_context()
        lock = ctx.RLock()
    if not hasattr(lock, 'acquire'):
        raise AttributeError("%r has no method 'acquire'" % lock)
    return synchronized(obj, lock, ctx=ctx)


def Array(typecode_or_type, size_or_initializer, *, lock=True, ctx=None):
    """
    Return a synchronization wrapper for a RawArray
    """
    obj = RawArray(typecode_or_type, size_or_initializer)
    if lock is False:
        return obj
    if lock in (True, None):
        ctx = ctx or get_context()
        lock = ctx.RLock()
    if not hasattr(lock, 'acquire'):
        raise AttributeError("%r has no method 'acquire'" % lock)
    return synchronized(obj, lock, ctx=ctx)


def copy(obj):
    new_obj = _new_value(type(obj))
    ctypes.pointer(new_obj)[0] = obj
    return new_obj


def synchronized(obj, lock=None, ctx=None):
    if isinstance(obj, SynchronizedBase):
        raise AssertionError('object already synchronized')
    ctx = ctx or get_context()
    if isinstance(obj, ctypes._SimpleCData):
        return Synchronized(obj, lock, ctx)
    if isinstance(obj, ctypes.Array):
        if obj._type_ is ctypes.c_char:
            return SynchronizedString(obj, lock, ctx)
        return SynchronizedArray(obj, lock, ctx)
    cls = type(obj)
    try:
        scls = class_cache[cls]
    except KeyError:
        names = [field[0] for field in cls._fields_]
        d = {make_property(name):name for name in names}
        classname = 'Synchronized' + cls.__name__
        scls = class_cache[cls] = type(classname, (SynchronizedBase,), d)
    else:
        return scls(obj, lock, ctx)


def reduce_ctype(obj):
    assert_spawning(obj)
    if isinstance(obj, ctypes.Array):
        return (
         rebuild_ctype, (obj._type_, obj._wrapper, obj._length_))
    return (rebuild_ctype, (type(obj), obj._wrapper, None))


def rebuild_ctype(type_, wrapper, length):
    if length is not None:
        type_ = type_ * length
    _ForkingPickler.register(type_, reduce_ctype)
    buf = wrapper.create_memoryview()
    obj = type_.from_buffer(buf)
    obj._wrapper = wrapper
    return obj


def make_property--- This code section failed: ---

 L. 149         0  SETUP_FINALLY        12  'to 12'

 L. 150         2  LOAD_GLOBAL              prop_cache
                4  LOAD_FAST                'name'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 151        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    74  'to 74'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 152        26  BUILD_MAP_0           0 
               28  STORE_FAST               'd'

 L. 153        30  LOAD_GLOBAL              exec
               32  LOAD_GLOBAL              template
               34  LOAD_FAST                'name'
               36  BUILD_TUPLE_1         1 
               38  LOAD_CONST               7
               40  BINARY_MULTIPLY  
               42  BINARY_MODULO    
               44  LOAD_FAST                'd'
               46  CALL_FUNCTION_2       2  ''
               48  POP_TOP          

 L. 154        50  LOAD_FAST                'd'
               52  LOAD_FAST                'name'
               54  BINARY_SUBSCR    
               56  LOAD_GLOBAL              prop_cache
               58  LOAD_FAST                'name'
               60  STORE_SUBSCR     

 L. 155        62  LOAD_FAST                'd'
               64  LOAD_FAST                'name'
               66  BINARY_SUBSCR    
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            18  '18'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


template = '\ndef get%s(self):\n    self.acquire()\n    try:\n        return self._obj.%s\n    finally:\n        self.release()\ndef set%s(self, value):\n    self.acquire()\n    try:\n        self._obj.%s = value\n    finally:\n        self.release()\n%s = property(get%s, set%s)\n'
prop_cache = {}
class_cache = weakref.WeakKeyDictionary()

class SynchronizedBase(object):

    def __init__(self, obj, lock=None, ctx=None):
        self._obj = obj
        if lock:
            self._lock = lock
        else:
            ctx = ctx or get_context(force=True)
            self._lock = ctx.RLock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return (self._lock.__exit__)(*args)

    def __reduce__(self):
        assert_spawning(self)
        return (synchronized, (self._obj, self._lock))

    def get_obj(self):
        return self._obj

    def get_lock(self):
        return self._lock

    def __repr__(self):
        return '<%s wrapper for %s>' % (type(self).__name__, self._obj)


class Synchronized(SynchronizedBase):
    value = make_property('value')


class SynchronizedArray(SynchronizedBase):

    def __len__(self):
        return len(self._obj)

    def __getitem__--- This code section failed: ---

 L. 222         0  LOAD_FAST                'self'
                2  SETUP_WITH           28  'to 28'
                4  POP_TOP          

 L. 223         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _obj
               10  LOAD_FAST                'i'
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  ROT_TWO          
               18  BEGIN_FINALLY    
               20  WITH_CLEANUP_START
               22  WITH_CLEANUP_FINISH
               24  POP_FINALLY           0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM_WITH        2  '2'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 16

    def __setitem__(self, i, value):
        with self:
            self._obj[i] = value

    def __getslice__--- This code section failed: ---

 L. 230         0  LOAD_FAST                'self'
                2  SETUP_WITH           32  'to 32'
                4  POP_TOP          

 L. 231         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _obj
               10  LOAD_FAST                'start'
               12  LOAD_FAST                'stop'
               14  BUILD_SLICE_2         2 
               16  BINARY_SUBSCR    
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        2  '2'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    def __setslice__(self, start, stop, values):
        with self:
            self._obj[start:stop] = values


class SynchronizedString(SynchronizedArray):
    value = make_property('value')
    raw = make_property('raw')