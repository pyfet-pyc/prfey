# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\psutil\_compat.py
"""Module which provides compatibility with older Python versions.
This is more future-compatible rather than the opposite (prefer latest
Python 3 way of doing things).
"""
import collections, errno, functools, os, sys, types
__all__ = [
 'PY3',
 'long', 'range', 'super', 'unicode', 'basestring',
 'u', 'b',
 'lru_cache',
 'which', 'get_terminal_size',
 'FileNotFoundError', 'PermissionError', 'ProcessLookupError',
 'InterruptedError', 'ChildProcessError', 'FileExistsError']
PY3 = sys.version_info[0] == 3
_SENTINEL = object()
if PY3:
    long = int
    xrange = range
    unicode = str
    basestring = str
    range = range

    def u(s):
        return s


    def b(s):
        return s.encode('latin-1')


else:
    long = long
    range = xrange
    unicode = unicode
    basestring = basestring

    def u(s):
        return unicode(s, 'unicode_escape')


    def b(s):
        return s


if PY3:
    super = super
else:
    _builtin_super = super

    def super--- This code section failed: ---

 L.  76         0  LOAD_FAST                'type_'
                2  LOAD_GLOBAL              _SENTINEL
                4  COMPARE_OP               is
              6_8  POP_JUMP_IF_FALSE   326  'to 326'

 L.  77        10  LOAD_GLOBAL              sys
               12  LOAD_METHOD              _getframe
               14  LOAD_FAST                'framedepth'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'f'

 L.  78        20  SETUP_FINALLY        44  'to 44'

 L.  80        22  LOAD_FAST                'f'
               24  LOAD_ATTR                f_locals
               26  LOAD_FAST                'f'
               28  LOAD_ATTR                f_code
               30  LOAD_ATTR                co_varnames
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  BINARY_SUBSCR    
               38  STORE_FAST               'type_or_obj'
               40  POP_BLOCK        
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM_FINALLY    20  '20'

 L.  81        44  DUP_TOP          
               46  LOAD_GLOBAL              IndexError
               48  LOAD_GLOBAL              KeyError
               50  BUILD_TUPLE_2         2 
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    74  'to 74'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  82        62  LOAD_GLOBAL              RuntimeError
               64  LOAD_STR                 'super() used in a function with no args'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            54  '54'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            42  '42'

 L.  83        76  SETUP_FINALLY        88  'to 88'

 L.  85        78  LOAD_FAST                'type_or_obj'
               80  LOAD_ATTR                __mro__
               82  STORE_FAST               'mro'
               84  POP_BLOCK        
               86  JUMP_FORWARD        154  'to 154'
             88_0  COME_FROM_FINALLY    76  '76'

 L.  86        88  DUP_TOP          
               90  LOAD_GLOBAL              AttributeError
               92  LOAD_GLOBAL              RuntimeError
               94  BUILD_TUPLE_2         2 
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   152  'to 152'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.  87       106  SETUP_FINALLY       120  'to 120'

 L.  88       108  LOAD_FAST                'type_or_obj'
              110  LOAD_ATTR                __class__
              112  LOAD_ATTR                __mro__
              114  STORE_FAST               'mro'
              116  POP_BLOCK        
              118  JUMP_FORWARD        148  'to 148'
            120_0  COME_FROM_FINALLY   106  '106'

 L.  89       120  DUP_TOP          
              122  LOAD_GLOBAL              AttributeError
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   146  'to 146'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L.  90       134  LOAD_GLOBAL              RuntimeError
              136  LOAD_STR                 'super() used in a non-newstyle class'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           126  '126'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           118  '118'
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM            98  '98'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM            86  '86'

 L.  91       154  LOAD_FAST                'mro'
              156  GET_ITER         
              158  FOR_ITER            318  'to 318'
              160  STORE_FAST               'type_'

 L.  93       162  LOAD_FAST                'type_'
              164  LOAD_ATTR                __dict__
              166  LOAD_METHOD              values
              168  CALL_METHOD_0         0  ''
              170  GET_ITER         
            172_0  COME_FROM           298  '298'
              172  FOR_ITER            308  'to 308'
              174  STORE_FAST               'meth'

 L.  96       176  SETUP_FINALLY       258  'to 258'

 L.  97       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'meth'
              182  LOAD_GLOBAL              types
              184  LOAD_ATTR                FunctionType
              186  CALL_FUNCTION_2       2  ''
              188  POP_JUMP_IF_TRUE    254  'to 254'

 L.  98       190  LOAD_GLOBAL              isinstance
              192  LOAD_FAST                'meth'
              194  LOAD_GLOBAL              property
              196  CALL_FUNCTION_2       2  ''
              198  POP_JUMP_IF_FALSE   208  'to 208'

 L. 102       200  LOAD_FAST                'meth'
              202  LOAD_ATTR                fget
              204  STORE_FAST               'meth'
              206  JUMP_BACK           178  'to 178'
            208_0  COME_FROM           198  '198'

 L. 104       208  SETUP_FINALLY       220  'to 220'

 L. 105       210  LOAD_FAST                'meth'
              212  LOAD_ATTR                __func__
              214  STORE_FAST               'meth'
              216  POP_BLOCK        
              218  JUMP_BACK           178  'to 178'
            220_0  COME_FROM_FINALLY   208  '208'

 L. 106       220  DUP_TOP          
              222  LOAD_GLOBAL              AttributeError
              224  COMPARE_OP               exception-match
              226  POP_JUMP_IF_FALSE   250  'to 250'
              228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L. 107       234  LOAD_FAST                'meth'
              236  LOAD_METHOD              __get__
              238  LOAD_FAST                'type_or_obj'
              240  LOAD_FAST                'type_'
              242  CALL_METHOD_2         2  ''
              244  STORE_FAST               'meth'
              246  POP_EXCEPT       
              248  JUMP_BACK           178  'to 178'
            250_0  COME_FROM           226  '226'
              250  END_FINALLY      
              252  JUMP_BACK           178  'to 178'
            254_0  COME_FROM           188  '188'
              254  POP_BLOCK        
              256  JUMP_FORWARD        288  'to 288'
            258_0  COME_FROM_FINALLY   176  '176'

 L. 108       258  DUP_TOP          
              260  LOAD_GLOBAL              AttributeError
              262  LOAD_GLOBAL              TypeError
              264  BUILD_TUPLE_2         2 
              266  COMPARE_OP               exception-match
          268_270  POP_JUMP_IF_FALSE   286  'to 286'
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 109       278  POP_EXCEPT       
              280  JUMP_BACK           172  'to 172'
              282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
            286_0  COME_FROM           268  '268'
              286  END_FINALLY      
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           256  '256'

 L. 110       288  LOAD_FAST                'meth'
              290  LOAD_ATTR                func_code
              292  LOAD_FAST                'f'
              294  LOAD_ATTR                f_code
              296  COMPARE_OP               is
              298  POP_JUMP_IF_FALSE   172  'to 172'

 L. 111       300  POP_TOP          
          302_304  BREAK_LOOP          310  'to 310'
              306  JUMP_BACK           172  'to 172'

 L. 114       308  JUMP_BACK           158  'to 158'

 L. 115       310  POP_TOP          
          312_314  BREAK_LOOP          326  'to 326'
              316  JUMP_BACK           158  'to 158'

 L. 117       318  LOAD_GLOBAL              RuntimeError
              320  LOAD_STR                 'super() called outside a method'
              322  CALL_FUNCTION_1       1  ''
              324  RAISE_VARARGS_1       1  'exception instance'
            326_0  COME_FROM             6  '6'

 L. 120       326  LOAD_FAST                'type_or_obj'
              328  LOAD_GLOBAL              _SENTINEL
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L. 121       336  LOAD_GLOBAL              _builtin_super
              338  LOAD_FAST                'type_'
              340  LOAD_FAST                'type_or_obj'
              342  CALL_FUNCTION_2       2  ''
              344  RETURN_VALUE     
            346_0  COME_FROM           332  '332'

 L. 122       346  LOAD_GLOBAL              _builtin_super
              348  LOAD_FAST                'type_'
              350  CALL_FUNCTION_1       1  ''
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 282


if PY3:
    FileNotFoundError = FileNotFoundError
    PermissionError = PermissionError
    ProcessLookupError = ProcessLookupError
    InterruptedError = InterruptedError
    ChildProcessError = ChildProcessError
    FileExistsError = FileExistsError
else:
    import platform

    def _instance_checking_exception(base_exception=Exception):

        def wrapped(instance_checker):

            class TemporaryClass(base_exception):

                def __init__(self, *args, **kwargs):
                    if len(args) == 1 and isinstance(args[0], TemporaryClass):
                        unwrap_me = args[0]
                        for attr in dir(unwrap_me):
                            if not attr.startswith('__'):
                                setattr(self, attr, getattr(unwrap_me, attr))

                    else:
                        (super(TemporaryClass, self).__init__)(*args, **kwargs)

                class __metaclass__(type):

                    def __instancecheck__(cls, inst):
                        return instance_checker(inst)

                    def __subclasscheck__(cls, classinfo):
                        value = sys.exc_info()[1]
                        return isinstance(value, cls)

            TemporaryClass.__name__ = instance_checker.__name__
            TemporaryClass.__doc__ = instance_checker.__doc__
            return TemporaryClass

        return wrapped


    @_instance_checking_exception(EnvironmentError)
    def FileNotFoundError(inst):
        return getattr(inst, 'errno', _SENTINEL) == errno.ENOENT


    @_instance_checking_exception(EnvironmentError)
    def ProcessLookupError(inst):
        return getattr(inst, 'errno', _SENTINEL) == errno.ESRCH


    @_instance_checking_exception(EnvironmentError)
    def PermissionError(inst):
        return getattr(inst, 'errno', _SENTINEL) in (
         errno.EACCES, errno.EPERM)


    @_instance_checking_exception(EnvironmentError)
    def InterruptedError(inst):
        return getattr(inst, 'errno', _SENTINEL) == errno.EINTR


    @_instance_checking_exception(EnvironmentError)
    def ChildProcessError(inst):
        return getattr(inst, 'errno', _SENTINEL) == errno.ECHILD


    @_instance_checking_exception(EnvironmentError)
    def FileExistsError(inst):
        return getattr(inst, 'errno', _SENTINEL) == errno.EEXIST


if platform.python_implementation() != 'CPython':
    try:
        raise OSError(errno.EEXIST, 'perm')
    except FileExistsError:
        pass
    except OSError:
        raise RuntimeError('broken or incompatible Python implementation, see: https://github.com/giampaolo/psutil/issues/1659')

try:
    from functools import lru_cache
except ImportError:
    try:
        from threading import RLock
    except ImportError:
        from dummy_threading import RLock
    else:
        _CacheInfo = collections.namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])

        class _HashedSeq(list):
            __slots__ = 'hashvalue'

            def __init__(self, tup, hash=hash):
                self[:] = tup
                self.hashvalue = hash(tup)

            def __hash__(self):
                return self.hashvalue


        def _make_key(args, kwds, typed, kwd_mark=(
 object(),), fasttypes=set((int, str, frozenset, type(None))), sorted=sorted, tuple=tuple, type=type, len=len):
            key = args
            if kwds:
                sorted_items = sorted(kwds.items())
                key += kwd_mark
                for item in sorted_items:
                    key += item

            elif typed:
                key += tuple((type(v) for v in args))
                if kwds:
                    key += tuple((type(v) for k, v in sorted_items))
            elif len(key) == 1 and type(key[0]) in fasttypes:
                return key[0]
            return _HashedSeq(key)


        def lru_cache(maxsize=100, typed=False):
            """Least-recently-used cache decorator, see:
        http://docs.python.org/3/library/functools.html#functools.lru_cache
        """

            def decorating_function(user_function):
                cache = dict()
                stats = [0, 0]
                HITS, MISSES = (0, 1)
                make_key = _make_key
                cache_get = cache.get
                _len = len
                lock = RLock()
                root = []
                root[:] = [root, root, None, None]
                nonlocal_root = [root]
                PREV, NEXT, KEY, RESULT = (0, 1, 2, 3)
                if maxsize == 0:

                    def wrapper(*args, **kwds):
                        result = user_function(*args, **kwds)
                        stats[MISSES] += 1
                        return result

                else:
                    if maxsize is None:

                        def wrapper(*args, **kwds):
                            key = make_key(args, kwds, typed)
                            result = cache_get(key, root)
                            if result is not root:
                                stats[HITS] += 1
                                return result
                            result = user_function(*args, **kwds)
                            cache[key] = result
                            stats[MISSES] += 1
                            return result

                    else:

                        def wrapper--- This code section failed: ---

 L. 282         0  LOAD_FAST                'kwds'
                2  POP_JUMP_IF_TRUE      8  'to 8'
                4  LOAD_DEREF               'typed'
                6  POP_JUMP_IF_FALSE    22  'to 22'
              8_0  COME_FROM             2  '2'

 L. 283         8  LOAD_DEREF               'make_key'
               10  LOAD_FAST                'args'
               12  LOAD_FAST                'kwds'
               14  LOAD_DEREF               'typed'
               16  CALL_FUNCTION_3       3  ''
               18  STORE_FAST               'key'
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM             6  '6'

 L. 285        22  LOAD_FAST                'args'
               24  STORE_FAST               'key'
             26_0  COME_FROM            20  '20'

 L. 286        26  LOAD_DEREF               'lock'
               28  LOAD_METHOD              acquire
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L. 287        34  SETUP_FINALLY       154  'to 154'

 L. 288        36  LOAD_DEREF               'cache_get'
               38  LOAD_FAST                'key'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'link'

 L. 289        44  LOAD_FAST                'link'
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_FALSE   150  'to 150'

 L. 290        52  LOAD_DEREF               'nonlocal_root'
               54  UNPACK_SEQUENCE_1     1 
               56  STORE_FAST               'root'

 L. 291        58  LOAD_FAST                'link'
               60  UNPACK_SEQUENCE_4     4 
               62  STORE_FAST               'link_prev'
               64  STORE_FAST               'link_next'
               66  STORE_FAST               'key'
               68  STORE_FAST               'result'

 L. 292        70  LOAD_FAST                'link_next'
               72  LOAD_FAST                'link_prev'
               74  LOAD_DEREF               'NEXT'
               76  STORE_SUBSCR     

 L. 293        78  LOAD_FAST                'link_prev'
               80  LOAD_FAST                'link_next'
               82  LOAD_DEREF               'PREV'
               84  STORE_SUBSCR     

 L. 294        86  LOAD_FAST                'root'
               88  LOAD_DEREF               'PREV'
               90  BINARY_SUBSCR    
               92  STORE_FAST               'last'

 L. 295        94  LOAD_FAST                'link'
               96  DUP_TOP          
               98  LOAD_FAST                'last'
              100  LOAD_DEREF               'NEXT'
              102  STORE_SUBSCR     
              104  LOAD_FAST                'root'
              106  LOAD_DEREF               'PREV'
              108  STORE_SUBSCR     

 L. 296       110  LOAD_FAST                'last'
              112  LOAD_FAST                'link'
              114  LOAD_DEREF               'PREV'
              116  STORE_SUBSCR     

 L. 297       118  LOAD_FAST                'root'
              120  LOAD_FAST                'link'
              122  LOAD_DEREF               'NEXT'
              124  STORE_SUBSCR     

 L. 298       126  LOAD_DEREF               'stats'
              128  LOAD_DEREF               'HITS'
              130  DUP_TOP_TWO      
              132  BINARY_SUBSCR    
              134  LOAD_CONST               1
              136  INPLACE_ADD      
              138  ROT_THREE        
              140  STORE_SUBSCR     

 L. 299       142  LOAD_FAST                'result'
              144  POP_BLOCK        
              146  CALL_FINALLY        154  'to 154'
              148  RETURN_VALUE     
            150_0  COME_FROM            50  '50'
              150  POP_BLOCK        
              152  BEGIN_FINALLY    
            154_0  COME_FROM           146  '146'
            154_1  COME_FROM_FINALLY    34  '34'

 L. 301       154  LOAD_DEREF               'lock'
              156  LOAD_METHOD              release
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          
              162  END_FINALLY      

 L. 302       164  LOAD_DEREF               'user_function'
              166  LOAD_FAST                'args'
              168  LOAD_FAST                'kwds'
              170  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              172  STORE_FAST               'result'

 L. 303       174  LOAD_DEREF               'lock'
              176  LOAD_METHOD              acquire
              178  CALL_METHOD_0         0  ''
              180  POP_TOP          

 L. 304       182  SETUP_FINALLY       354  'to 354'

 L. 305       184  LOAD_DEREF               'nonlocal_root'
              186  UNPACK_SEQUENCE_1     1 
              188  STORE_FAST               'root'

 L. 306       190  LOAD_FAST                'key'
              192  LOAD_DEREF               'cache'
              194  COMPARE_OP               in
              196  POP_JUMP_IF_FALSE   200  'to 200'

 L. 307       198  JUMP_FORWARD        334  'to 334'
            200_0  COME_FROM           196  '196'

 L. 308       200  LOAD_DEREF               '_len'
              202  LOAD_DEREF               'cache'
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_DEREF               'maxsize'
              208  COMPARE_OP               >=
          210_212  POP_JUMP_IF_FALSE   290  'to 290'

 L. 309       214  LOAD_FAST                'root'
              216  STORE_FAST               'oldroot'

 L. 310       218  LOAD_FAST                'key'
              220  LOAD_FAST                'oldroot'
              222  LOAD_DEREF               'KEY'
              224  STORE_SUBSCR     

 L. 311       226  LOAD_FAST                'result'
              228  LOAD_FAST                'oldroot'
              230  LOAD_DEREF               'RESULT'
              232  STORE_SUBSCR     

 L. 312       234  LOAD_FAST                'oldroot'
              236  LOAD_DEREF               'NEXT'
              238  BINARY_SUBSCR    
              240  DUP_TOP          
              242  STORE_FAST               'root'
              244  LOAD_DEREF               'nonlocal_root'
              246  LOAD_CONST               0
              248  STORE_SUBSCR     

 L. 313       250  LOAD_FAST                'root'
              252  LOAD_DEREF               'KEY'
              254  BINARY_SUBSCR    
              256  STORE_FAST               'oldkey'

 L. 314       258  LOAD_CONST               None
              260  DUP_TOP          
              262  LOAD_FAST                'root'
              264  LOAD_DEREF               'KEY'
              266  STORE_SUBSCR     
              268  LOAD_FAST                'root'
              270  LOAD_DEREF               'RESULT'
              272  STORE_SUBSCR     

 L. 315       274  LOAD_DEREF               'cache'
              276  LOAD_FAST                'oldkey'
              278  DELETE_SUBSCR    

 L. 316       280  LOAD_FAST                'oldroot'
              282  LOAD_DEREF               'cache'
              284  LOAD_FAST                'key'
              286  STORE_SUBSCR     
              288  JUMP_FORWARD        334  'to 334'
            290_0  COME_FROM           210  '210'

 L. 318       290  LOAD_FAST                'root'
              292  LOAD_DEREF               'PREV'
              294  BINARY_SUBSCR    
              296  STORE_FAST               'last'

 L. 319       298  LOAD_FAST                'last'
              300  LOAD_FAST                'root'
              302  LOAD_FAST                'key'
              304  LOAD_FAST                'result'
              306  BUILD_LIST_4          4 
              308  STORE_FAST               'link'

 L. 320       310  LOAD_FAST                'link'
              312  DUP_TOP          
              314  LOAD_FAST                'last'
              316  LOAD_DEREF               'NEXT'
              318  STORE_SUBSCR     
              320  DUP_TOP          
              322  LOAD_FAST                'root'
              324  LOAD_DEREF               'PREV'
              326  STORE_SUBSCR     
              328  LOAD_DEREF               'cache'
              330  LOAD_FAST                'key'
              332  STORE_SUBSCR     
            334_0  COME_FROM           288  '288'
            334_1  COME_FROM           198  '198'

 L. 321       334  LOAD_DEREF               'stats'
              336  LOAD_DEREF               'MISSES'
              338  DUP_TOP_TWO      
              340  BINARY_SUBSCR    
              342  LOAD_CONST               1
              344  INPLACE_ADD      
              346  ROT_THREE        
              348  STORE_SUBSCR     
              350  POP_BLOCK        
              352  BEGIN_FINALLY    
            354_0  COME_FROM_FINALLY   182  '182'

 L. 323       354  LOAD_DEREF               'lock'
              356  LOAD_METHOD              release
              358  CALL_METHOD_0         0  ''
              360  POP_TOP          
              362  END_FINALLY      

 L. 324       364  LOAD_FAST                'result'
              366  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 146

                def cache_info():
                    lock.acquire()
                    try:
                        return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))
                    finally:
                        lock.release()

                def cache_clear():
                    lock.acquire()
                    try:
                        cache.clear()
                        root = nonlocal_root[0]
                        root[:] = [root, root, None, None]
                        stats[:] = [0, 0]
                    finally:
                        lock.release()

                wrapper.__wrapped__ = user_function
                wrapper.cache_info = cache_info
                wrapper.cache_clear = cache_clear
                return functools.update_wrapper(wrapper, user_function)

            return decorating_function


try:
    from shutil import which
except ImportError:

    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.

        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.
        """

        def _access_check(fn, mode):
            return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)

        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return
        if path is None:
            path = os.environ.get('PATH', os.defpath)
        elif not path:
            return
            path = path.split(os.pathsep)
            if sys.platform == 'win32':
                if os.curdir not in path:
                    path.insert(0, os.curdir)
                pathext = os.environ.get('PATHEXT', '').split(os.pathsep)
                if any((cmd.lower().endswith(ext.lower()) for ext in pathext)):
                    files = [
                     cmd]
                else:
                    files = [cmd + ext for ext in pathext]
        else:
            files = [
             cmd]
        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name


try:
    from shutil import get_terminal_size
except ImportError:

    def get_terminal_size--- This code section failed: ---

 L. 411         0  SETUP_FINALLY        30  'to 30'

 L. 412         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              fcntl
                8  STORE_FAST               'fcntl'

 L. 413        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              termios
               16  STORE_FAST               'termios'

 L. 414        18  LOAD_CONST               0
               20  LOAD_CONST               None
               22  IMPORT_NAME              struct
               24  STORE_FAST               'struct'
               26  POP_BLOCK        
               28  JUMP_FORWARD         54  'to 54'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 415        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    52  'to 52'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 416        44  LOAD_FAST                'fallback'
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
             52_0  COME_FROM            36  '36'
               52  END_FINALLY      
             54_0  COME_FROM            28  '28'

 L. 418        54  SETUP_FINALLY        98  'to 98'

 L. 420        56  LOAD_FAST                'struct'
               58  LOAD_METHOD              unpack

 L. 421        60  LOAD_STR                 'hh'

 L. 421        62  LOAD_FAST                'fcntl'
               64  LOAD_METHOD              ioctl
               66  LOAD_CONST               1
               68  LOAD_FAST                'termios'
               70  LOAD_ATTR                TIOCGWINSZ
               72  LOAD_STR                 '1234'
               74  CALL_METHOD_3         3  ''

 L. 420        76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'res'

 L. 422        80  LOAD_FAST                'res'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'res'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  BUILD_TUPLE_2         2 
               94  POP_BLOCK        
               96  RETURN_VALUE     
             98_0  COME_FROM_FINALLY    54  '54'

 L. 423        98  DUP_TOP          
              100  LOAD_GLOBAL              Exception
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   120  'to 120'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 424       112  LOAD_FAST                'fallback'
              114  ROT_FOUR         
              116  POP_EXCEPT       
              118  RETURN_VALUE     
            120_0  COME_FROM           104  '104'
              120  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 108