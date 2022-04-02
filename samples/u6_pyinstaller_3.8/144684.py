# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: _threading_local.py
"""Thread-local objects.

(Note that this module provides a Python version of the threading.local
 class.  Depending on the version of Python you're using, there may be a
 faster one available.  You should always import the `local` class from
 `threading`.)

Thread-local objects support the management of thread-local data.
If you have data that you want to be local to a thread, simply create
a thread-local object and use its attributes:

  >>> mydata = local()
  >>> mydata.number = 42
  >>> mydata.number
  42

You can also access the local-object's dictionary:

  >>> mydata.__dict__
  {'number': 42}
  >>> mydata.__dict__.setdefault('widgets', [])
  []
  >>> mydata.widgets
  []

What's important about thread-local objects is that their data are
local to a thread. If we access the data in a different thread:

  >>> log = []
  >>> def f():
  ...     items = sorted(mydata.__dict__.items())
  ...     log.append(items)
  ...     mydata.number = 11
  ...     log.append(mydata.number)

  >>> import threading
  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()
  >>> log
  [[], 11]

we get different data.  Furthermore, changes made in the other thread
don't affect data seen in this thread:

  >>> mydata.number
  42

Of course, values you get from a local object, including a __dict__
attribute, are for whatever thread was current at the time the
attribute was read.  For that reason, you generally don't want to save
these values across threads, as they apply only to the thread they
came from.

You can create custom local objects by subclassing the local class:

  >>> class MyLocal(local):
  ...     number = 2
  ...     def __init__(self, /, **kw):
  ...         self.__dict__.update(kw)
  ...     def squared(self):
  ...         return self.number ** 2

This can be useful to support default values, methods and
initialization.  Note that if you define an __init__ method, it will be
called each time the local object is used in a separate thread.  This
is necessary to initialize each thread's dictionary.

Now if we create a local object:

  >>> mydata = MyLocal(color='red')

Now we have a default number:

  >>> mydata.number
  2

an initial color:

  >>> mydata.color
  'red'
  >>> del mydata.color

And a method that operates on the data:

  >>> mydata.squared()
  4

As before, we can access the data in a separate thread:

  >>> log = []
  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()
  >>> log
  [[('color', 'red')], 11]

without affecting this thread's data:

  >>> mydata.number
  2
  >>> mydata.color
  Traceback (most recent call last):
  ...
  AttributeError: 'MyLocal' object has no attribute 'color'

Note that subclasses can define slots, but they are not thread
local. They are shared across threads:

  >>> class MyLocal(local):
  ...     __slots__ = 'number'

  >>> mydata = MyLocal()
  >>> mydata.number = 42
  >>> mydata.color = 'red'

So, the separate thread:

  >>> thread = threading.Thread(target=f)
  >>> thread.start()
  >>> thread.join()

affects what we see:

  >>> mydata.number
  11

>>> del mydata
"""
from weakref import ref
from contextlib import contextmanager
__all__ = [
 'local']

class _localimpl:
    __doc__ = 'A class managing thread-local dicts'
    __slots__ = ('key', 'dicts', 'localargs', 'locallock', '__weakref__')

    def __init__(self):
        self.key = '_threading_local._localimpl.' + str(id(self))
        self.dicts = {}

    def get_dict(self):
        """Return the dict for the current thread. Raises KeyError if none
        defined."""
        thread = current_thread()
        return self.dicts[id(thread)][1]

    def create_dict(self):
        """Create a new dict for the current thread, and return it."""
        localdict = {}
        key = self.key
        thread = current_thread()
        idt = id(thread)

        def local_deleted(_, key=key):
            thread = wrthread()
            if thread is not None:
                del thread.__dict__[key]

        def thread_deleted(_, idt=idt):
            local = wrlocal()
            if local is not None:
                dct = local.dicts.pop(idt)

        wrlocal = ref(self, local_deleted)
        wrthread = ref(thread, thread_deleted)
        thread.__dict__[key] = wrlocal
        self.dicts[idt] = (wrthread, localdict)
        return localdict


@contextmanager
def _patch(self):
    impl = object.__getattribute__(self, '_local__impl')
    try:
        dct = impl.get_dict()
    except KeyError:
        dct = impl.create_dict()
        args, kw = impl.localargs
        (self.__init__)(*args, **kw)
    else:
        with impl.locallock:
            object.__setattr__(self, '__dict__', dct)
            (yield)


class local:
    __slots__ = ('_local__impl', '__dict__')

    def __new__(cls, *args, **kw):
        if args or kw:
            if cls.__init__ is object.__init__:
                raise TypeError('Initialization arguments are not supported')
        self = object.__new__(cls)
        impl = _localimpl()
        impl.localargs = (args, kw)
        impl.locallock = RLock()
        object.__setattr__(self, '_local__impl', impl)
        impl.create_dict()
        return self

    def __getattribute__--- This code section failed: ---

 L. 222         0  LOAD_GLOBAL              _patch
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           34  'to 34'
                8  POP_TOP          

 L. 223        10  LOAD_GLOBAL              object
               12  LOAD_METHOD              __getattribute__
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'name'
               18  CALL_METHOD_2         2  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        6  '6'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22

    def __setattr__--- This code section failed: ---

 L. 226         0  LOAD_FAST                'name'
                2  LOAD_STR                 '__dict__'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 227         8  LOAD_GLOBAL              AttributeError

 L. 228        10  LOAD_STR                 "%r object attribute '__dict__' is read-only"

 L. 229        12  LOAD_FAST                'self'
               14  LOAD_ATTR                __class__
               16  LOAD_ATTR                __name__

 L. 228        18  BINARY_MODULO    

 L. 227        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             6  '6'

 L. 230        24  LOAD_GLOBAL              _patch
               26  LOAD_FAST                'self'
               28  CALL_FUNCTION_1       1  ''
               30  SETUP_WITH           60  'to 60'
               32  POP_TOP          

 L. 231        34  LOAD_GLOBAL              object
               36  LOAD_METHOD              __setattr__
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'name'
               42  LOAD_FAST                'value'
               44  CALL_METHOD_3         3  ''
               46  POP_BLOCK        
               48  ROT_TWO          
               50  BEGIN_FINALLY    
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  POP_FINALLY           0  ''
               58  RETURN_VALUE     
             60_0  COME_FROM_WITH       30  '30'
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 48

    def __delattr__--- This code section failed: ---

 L. 234         0  LOAD_FAST                'name'
                2  LOAD_STR                 '__dict__'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 235         8  LOAD_GLOBAL              AttributeError

 L. 236        10  LOAD_STR                 "%r object attribute '__dict__' is read-only"

 L. 237        12  LOAD_FAST                'self'
               14  LOAD_ATTR                __class__
               16  LOAD_ATTR                __name__

 L. 236        18  BINARY_MODULO    

 L. 235        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             6  '6'

 L. 238        24  LOAD_GLOBAL              _patch
               26  LOAD_FAST                'self'
               28  CALL_FUNCTION_1       1  ''
               30  SETUP_WITH           58  'to 58'
               32  POP_TOP          

 L. 239        34  LOAD_GLOBAL              object
               36  LOAD_METHOD              __delattr__
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'name'
               42  CALL_METHOD_2         2  ''
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH       30  '30'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 46


from threading import current_thread, RLock