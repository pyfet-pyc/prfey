# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
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

        def local_deleted--- This code section failed: ---

 L. 172         0  LOAD_DEREF               'wrthread'
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'thread'

 L. 173         6  LOAD_FAST                'thread'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    22  'to 22'

 L. 174        14  LOAD_FAST                'thread'
               16  LOAD_ATTR                __dict__
               18  LOAD_FAST                'key'
               20  DELETE_SUBSCR    
             22_0  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 10

        def thread_deleted--- This code section failed: ---

 L. 180         0  LOAD_DEREF               'wrlocal'
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'local'

 L. 181         6  LOAD_FAST                'local'
                8  LOAD_CONST               None
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L. 182        14  LOAD_FAST                'local'
               16  LOAD_ATTR                dicts
               18  LOAD_METHOD              pop
               20  LOAD_FAST                'idt'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'dct'
             26_0  COME_FROM            12  '12'

Parse error at or near `<117>' instruction at offset 10

        wrlocal = ref(self, local_deleted)
        wrthread = ref(thread, thread_deleted)
        thread.__dict__[key] = wrlocal
        self.dicts[idt] = (wrthread, localdict)
        return localdict


@contextmanager
def _patch--- This code section failed: ---

 L. 192         0  LOAD_GLOBAL              object
                2  LOAD_METHOD              __getattribute__
                4  LOAD_FAST                'self'
                6  LOAD_STR                 '_local__impl'
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'impl'

 L. 193        12  SETUP_FINALLY        26  'to 26'

 L. 194        14  LOAD_FAST                'impl'
               16  LOAD_METHOD              get_dict
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'dct'
               22  POP_BLOCK        
               24  JUMP_FORWARD         78  'to 78'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 195        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  <121>                76  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 196        38  LOAD_FAST                'impl'
               40  LOAD_METHOD              create_dict
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'dct'

 L. 197        46  LOAD_FAST                'impl'
               48  LOAD_ATTR                localargs
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'args'
               54  STORE_FAST               'kw'

 L. 198        56  LOAD_FAST                'self'
               58  LOAD_ATTR                __init__
               60  LOAD_FAST                'args'
               62  BUILD_MAP_0           0 
               64  LOAD_FAST                'kw'
               66  <164>                 1  ''
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  POP_TOP          
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            24  '24'

 L. 199        78  LOAD_FAST                'impl'
               80  LOAD_ATTR                locallock
               82  SETUP_WITH          120  'to 120'
               84  POP_TOP          

 L. 200        86  LOAD_GLOBAL              object
               88  LOAD_METHOD              __setattr__
               90  LOAD_FAST                'self'
               92  LOAD_STR                 '__dict__'
               94  LOAD_FAST                'dct'
               96  CALL_METHOD_3         3  ''
               98  POP_TOP          

 L. 201       100  LOAD_CONST               None
              102  YIELD_VALUE      
              104  POP_TOP          
              106  POP_BLOCK        
              108  LOAD_CONST               None
              110  DUP_TOP          
              112  DUP_TOP          
              114  CALL_FUNCTION_3       3  ''
              116  POP_TOP          
              118  JUMP_FORWARD        136  'to 136'
            120_0  COME_FROM_WITH       82  '82'
              120  <49>             
              122  POP_JUMP_IF_TRUE    126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          
              132  POP_EXCEPT       
              134  POP_TOP          
            136_0  COME_FROM           118  '118'

Parse error at or near `<121>' instruction at offset 30


class local:
    __slots__ = ('_local__impl', '__dict__')

    def __new__--- This code section failed: ---

 L. 208         0  LOAD_FAST                'args'
                2  POP_JUMP_IF_TRUE      8  'to 8'
                4  LOAD_FAST                'kw'
                6  POP_JUMP_IF_FALSE    28  'to 28'
              8_0  COME_FROM             2  '2'
                8  LOAD_FAST                'cls'
               10  LOAD_ATTR                __init__
               12  LOAD_GLOBAL              object
               14  LOAD_ATTR                __init__
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 209        20  LOAD_GLOBAL              TypeError
               22  LOAD_STR                 'Initialization arguments are not supported'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             6  '6'

 L. 210        28  LOAD_GLOBAL              object
               30  LOAD_METHOD              __new__
               32  LOAD_FAST                'cls'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'self'

 L. 211        38  LOAD_GLOBAL              _localimpl
               40  CALL_FUNCTION_0       0  ''
               42  STORE_FAST               'impl'

 L. 212        44  LOAD_FAST                'args'
               46  LOAD_FAST                'kw'
               48  BUILD_TUPLE_2         2 
               50  LOAD_FAST                'impl'
               52  STORE_ATTR               localargs

 L. 213        54  LOAD_GLOBAL              RLock
               56  CALL_FUNCTION_0       0  ''
               58  LOAD_FAST                'impl'
               60  STORE_ATTR               locallock

 L. 214        62  LOAD_GLOBAL              object
               64  LOAD_METHOD              __setattr__
               66  LOAD_FAST                'self'
               68  LOAD_STR                 '_local__impl'
               70  LOAD_FAST                'impl'
               72  CALL_METHOD_3         3  ''
               74  POP_TOP          

 L. 218        76  LOAD_FAST                'impl'
               78  LOAD_METHOD              create_dict
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          

 L. 219        84  LOAD_FAST                'self'
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __getattribute__--- This code section failed: ---

 L. 222         0  LOAD_GLOBAL              _patch
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           36  'to 36'
                8  POP_TOP          

 L. 223        10  LOAD_GLOBAL              object
               12  LOAD_METHOD              __getattribute__
               14  LOAD_FAST                'self'
               16  LOAD_FAST                'name'
               18  CALL_METHOD_2         2  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  LOAD_CONST               None
               26  DUP_TOP          
               28  DUP_TOP          
               30  CALL_FUNCTION_3       3  ''
               32  POP_TOP          
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH        6  '6'
               36  <49>             
               38  POP_JUMP_IF_TRUE     42  'to 42'
               40  <48>             
             42_0  COME_FROM            38  '38'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          
               48  POP_EXCEPT       
               50  POP_TOP          

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
               30  SETUP_WITH           62  'to 62'
               32  POP_TOP          

 L. 231        34  LOAD_GLOBAL              object
               36  LOAD_METHOD              __setattr__
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'name'
               42  LOAD_FAST                'value'
               44  CALL_METHOD_3         3  ''
               46  POP_BLOCK        
               48  ROT_TWO          
               50  LOAD_CONST               None
               52  DUP_TOP          
               54  DUP_TOP          
               56  CALL_FUNCTION_3       3  ''
               58  POP_TOP          
               60  RETURN_VALUE     
             62_0  COME_FROM_WITH       30  '30'
               62  <49>             
               64  POP_JUMP_IF_TRUE     68  'to 68'
               66  <48>             
             68_0  COME_FROM            64  '64'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          
               74  POP_EXCEPT       
               76  POP_TOP          

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
               30  SETUP_WITH           60  'to 60'
               32  POP_TOP          

 L. 239        34  LOAD_GLOBAL              object
               36  LOAD_METHOD              __delattr__
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'name'
               42  CALL_METHOD_2         2  ''
               44  POP_BLOCK        
               46  ROT_TWO          
               48  LOAD_CONST               None
               50  DUP_TOP          
               52  DUP_TOP          
               54  CALL_FUNCTION_3       3  ''
               56  POP_TOP          
               58  RETURN_VALUE     
             60_0  COME_FROM_WITH       30  '30'
               60  <49>             
               62  POP_JUMP_IF_TRUE     66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          
               72  POP_EXCEPT       
               74  POP_TOP          

Parse error at or near `ROT_TWO' instruction at offset 46


from threading import current_thread, RLock