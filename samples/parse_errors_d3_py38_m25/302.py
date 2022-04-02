# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: inspect.py
"""Get useful information from live Python objects.

This module encapsulates the interface provided by the internal special
attributes (co_*, im_*, tb_*, etc.) in a friendlier fashion.
It also provides some help for examining source code and class layout.

Here are some of the useful functions provided by this module:

    ismodule(), isclass(), ismethod(), isfunction(), isgeneratorfunction(),
        isgenerator(), istraceback(), isframe(), iscode(), isbuiltin(),
        isroutine() - check object types
    getmembers() - get members of an object that satisfy a given condition

    getfile(), getsourcefile(), getsource() - find an object's source code
    getdoc(), getcomments() - get documentation on an object
    getmodule() - determine the module that an object came from
    getclasstree() - arrange classes so as to represent their hierarchy

    getargvalues(), getcallargs() - get info about function arguments
    getfullargspec() - same, with support for Python 3 features
    formatargvalues() - format an argument spec
    getouterframes(), getinnerframes() - get info about frames
    currentframe() - get the current stack frame
    stack(), trace() - get info about frames on the stack or in a traceback

    signature() - get a Signature object for the callable
"""
__author__ = ('Ka-Ping Yee <ping@lfw.org>', 'Yury Selivanov <yselivanov@sprymix.com>')
import abc, dis, collections.abc, enum, importlib.machinery, itertools, linecache, os, re, sys, tokenize, token, types, warnings, functools, builtins
from operator import attrgetter
from collections import namedtuple, OrderedDict
mod_dict = globals()
for k, v in dis.COMPILER_FLAG_NAMES.items():
    mod_dict['CO_' + v] = k
else:
    TPFLAGS_IS_ABSTRACT = 1048576

    def ismodule(object):
        """Return true if the object is a module.

    Module objects provide these attributes:
        __cached__      pathname to byte compiled file
        __doc__         documentation string
        __file__        filename (missing for built-in modules)"""
        return isinstance(object, types.ModuleType)


    def isclass(object):
        """Return true if the object is a class.

    Class objects provide these attributes:
        __doc__         documentation string
        __module__      name of module in which this class was defined"""
        return isinstance(object, type)


    def ismethod(object):
        """Return true if the object is an instance method.

    Instance method objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this method was defined
        __func__        function object containing implementation of method
        __self__        instance to which this method is bound"""
        return isinstance(object, types.MethodType)


    def ismethoddescriptor(object):
        """Return true if the object is a method descriptor.

    But not if ismethod() or isclass() or isfunction() are true.

    This is new in Python 2.2, and, for example, is true of int.__add__.
    An object passing this test has a __get__ attribute but not a __set__
    attribute, but beyond that the set of attributes varies.  __name__ is
    usually sensible, and __doc__ often is.

    Methods implemented via descriptors that also pass one of the other
    tests return false from the ismethoddescriptor() test, simply because
    the other tests promise more -- you can, e.g., count on having the
    __func__ attribute (etc) when an object passes ismethod()."""
        if not isclass(object):
            if ismethod(object) or (isfunction(object)):
                return False
            tp = type(object)
            return hasattr(tp, '__get__') and not hasattr(tp, '__set__')


    def isdatadescriptor(object):
        """Return true if the object is a data descriptor.

    Data descriptors have a __set__ or a __delete__ attribute.  Examples are
    properties (defined in Python) and getsets and members (defined in C).
    Typically, data descriptors will also have __name__ and __doc__ attributes
    (properties, getsets, and members have both of these attributes), but this
    is not guaranteed."""
        if not isclass(object):
            if ismethod(object) or (isfunction(object)):
                return False
            tp = type(object)
            return hasattr(tp, '__set__') or hasattr(tp, '__delete__')


    if hasattr(types, 'MemberDescriptorType'):

        def ismemberdescriptor(object):
            """Return true if the object is a member descriptor.

        Member descriptors are specialized descriptors defined in extension
        modules."""
            return isinstance(object, types.MemberDescriptorType)


    else:

        def ismemberdescriptor(object):
            """Return true if the object is a member descriptor.

        Member descriptors are specialized descriptors defined in extension
        modules."""
            return False


    if hasattr(types, 'GetSetDescriptorType'):

        def isgetsetdescriptor(object):
            """Return true if the object is a getset descriptor.

        getset descriptors are specialized descriptors defined in extension
        modules."""
            return isinstance(object, types.GetSetDescriptorType)


    else:

        def isgetsetdescriptor(object):
            """Return true if the object is a getset descriptor.

        getset descriptors are specialized descriptors defined in extension
        modules."""
            return False


    def isfunction(object):
        """Return true if the object is a user-defined function.

    Function objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this function was defined
        __code__        code object containing compiled function bytecode
        __defaults__    tuple of any default values for arguments
        __globals__     global namespace in which this function was defined
        __annotations__ dict of parameter annotations
        __kwdefaults__  dict of keyword only parameters with defaults"""
        return isinstance(object, types.FunctionType)


    def _has_code_flag(f, flag):
        """Return true if ``f`` is a function (or a method or functools.partial
    wrapper wrapping a function) whose code object has the given ``flag``
    set in its flags."""
        while True:
            if ismethod(f):
                f = f.__func__

        f = functools._unwrap_partial(f)
        if not isfunction(f):
            return False
        return bool(f.__code__.co_flags & flag)


    def isgeneratorfunction(obj):
        """Return true if the object is a user-defined generator function.

    Generator function objects provide the same attributes as functions.
    See help(isfunction) for a list of attributes."""
        return _has_code_flag(obj, CO_GENERATOR)


    def iscoroutinefunction(obj):
        """Return true if the object is a coroutine function.

    Coroutine functions are defined with "async def" syntax.
    """
        return _has_code_flag(obj, CO_COROUTINE)


    def isasyncgenfunction(obj):
        """Return true if the object is an asynchronous generator function.

    Asynchronous generator functions are defined with "async def"
    syntax and have "yield" expressions in their body.
    """
        return _has_code_flag(obj, CO_ASYNC_GENERATOR)


    def isasyncgen(object):
        """Return true if the object is an asynchronous generator."""
        return isinstance(object, types.AsyncGeneratorType)


    def isgenerator(object):
        """Return true if the object is a generator.

    Generator objects provide these attributes:
        __iter__        defined to support iteration over container
        close           raises a new GeneratorExit exception inside the
                        generator to terminate the iteration
        gi_code         code object
        gi_frame        frame object or possibly None once the generator has
                        been exhausted
        gi_running      set to 1 when generator is executing, 0 otherwise
        next            return the next item from the container
        send            resumes the generator and "sends" a value that becomes
                        the result of the current yield-expression
        throw           used to raise an exception inside the generator"""
        return isinstance(object, types.GeneratorType)


    def iscoroutine(object):
        """Return true if the object is a coroutine."""
        return isinstance(object, types.CoroutineType)


    def isawaitable(object):
        """Return true if object can be passed to an ``await`` expression."""
        return isinstance(object, types.CoroutineType) or (isinstance(object, types.GeneratorType)) and (bool(object.gi_code.co_flags & CO_ITERABLE_COROUTINE)) or (isinstance(object, collections.abc.Awaitable))


    def istraceback(object):
        """Return true if the object is a traceback.

    Traceback objects provide these attributes:
        tb_frame        frame object at this level
        tb_lasti        index of last attempted instruction in bytecode
        tb_lineno       current line number in Python source code
        tb_next         next inner traceback object (called by this level)"""
        return isinstance(object, types.TracebackType)


    def isframe(object):
        """Return true if the object is a frame object.

    Frame objects provide these attributes:
        f_back          next outer frame object (this frame's caller)
        f_builtins      built-in namespace seen by this frame
        f_code          code object being executed in this frame
        f_globals       global namespace seen by this frame
        f_lasti         index of last attempted instruction in bytecode
        f_lineno        current line number in Python source code
        f_locals        local namespace seen by this frame
        f_trace         tracing function for this frame, or None"""
        return isinstance(object, types.FrameType)


    def iscode(object):
        """Return true if the object is a code object.

    Code objects provide these attributes:
        co_argcount         number of arguments (not including *, ** args
                            or keyword only arguments)
        co_code             string of raw compiled bytecode
        co_cellvars         tuple of names of cell variables
        co_consts           tuple of constants used in the bytecode
        co_filename         name of file in which this code object was created
        co_firstlineno      number of first line in Python source code
        co_flags            bitmap: 1=optimized | 2=newlocals | 4=*arg | 8=**arg
                            | 16=nested | 32=generator | 64=nofree | 128=coroutine
                            | 256=iterable_coroutine | 512=async_generator
        co_freevars         tuple of names of free variables
        co_posonlyargcount  number of positional only arguments
        co_kwonlyargcount   number of keyword only arguments (not including ** arg)
        co_lnotab           encoded mapping of line numbers to bytecode indices
        co_name             name with which this code object was defined
        co_names            tuple of names of local variables
        co_nlocals          number of local variables
        co_stacksize        virtual machine stack space required
        co_varnames         tuple of names of arguments and local variables"""
        return isinstance(object, types.CodeType)


    def isbuiltin(object):
        """Return true if the object is a built-in function or method.

    Built-in functions and methods provide these attributes:
        __doc__         documentation string
        __name__        original name of this function or method
        __self__        instance to which a method is bound, or None"""
        return isinstance(object, types.BuiltinFunctionType)


    def isroutine(object):
        """Return true if the object is any kind of function or method."""
        return isbuiltin(object) or isfunction(object) or ismethod(object) or ismethoddescriptor(object)


    def isabstract(object):
        """Return true if the object is an abstract base class (ABC)."""
        if not isinstance(object, type):
            return False
        if object.__flags__ & TPFLAGS_IS_ABSTRACT:
            return True
        if not issubclass(type(object), abc.ABCMeta):
            return False
        if hasattr(object, '__abstractmethods__'):
            return False
        for name, value in object.__dict__.items():
            if getattr(value, '__isabstractmethod__', False):
                return True
        else:
            for base in object.__bases__:
                for name in getattr(base, '__abstractmethods__', ()):
                    value = getattr(object, name, None)
                    if getattr(value, '__isabstractmethod__', False):
                        return True
                else:
                    return False


    def getmembers--- This code section failed: ---

 L. 328         0  LOAD_GLOBAL              isclass
                2  LOAD_FAST                'object'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 329         8  LOAD_FAST                'object'
               10  BUILD_TUPLE_1         1 
               12  LOAD_GLOBAL              getmro
               14  LOAD_FAST                'object'
               16  CALL_FUNCTION_1       1  ''
               18  BINARY_ADD       
               20  STORE_FAST               'mro'
               22  JUMP_FORWARD         28  'to 28'
             24_0  COME_FROM             6  '6'

 L. 331        24  LOAD_CONST               ()
               26  STORE_FAST               'mro'
             28_0  COME_FROM            22  '22'

 L. 332        28  BUILD_LIST_0          0 
               30  STORE_FAST               'results'

 L. 333        32  LOAD_GLOBAL              set
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'processed'

 L. 334        38  LOAD_GLOBAL              dir
               40  LOAD_FAST                'object'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'names'

 L. 338        46  SETUP_FINALLY       106  'to 106'

 L. 339        48  LOAD_FAST                'object'
               50  LOAD_ATTR                __bases__
               52  GET_ITER         
             54_0  COME_FROM           100  '100'
               54  FOR_ITER            102  'to 102'
               56  STORE_FAST               'base'

 L. 340        58  LOAD_FAST                'base'
               60  LOAD_ATTR                __dict__
               62  LOAD_METHOD              items
               64  CALL_METHOD_0         0  ''
               66  GET_ITER         
             68_0  COME_FROM            98  '98'
             68_1  COME_FROM            86  '86'
               68  FOR_ITER            100  'to 100'
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'k'
               74  STORE_FAST               'v'

 L. 341        76  LOAD_GLOBAL              isinstance
               78  LOAD_FAST                'v'
               80  LOAD_GLOBAL              types
               82  LOAD_ATTR                DynamicClassAttribute
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE_BACK    68  'to 68'

 L. 342        88  LOAD_FAST                'names'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'k'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            68  'to 68'
            100_0  COME_FROM            68  '68'
              100  JUMP_BACK            54  'to 54'
            102_0  COME_FROM            54  '54'
              102  POP_BLOCK        
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM_FINALLY    46  '46'

 L. 343       106  DUP_TOP          
              108  LOAD_GLOBAL              AttributeError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   124  'to 124'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 344       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           112  '112'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           104  '104'

 L. 345       126  LOAD_FAST                'names'
              128  GET_ITER         
            130_0  COME_FROM           256  '256'
            130_1  COME_FROM           212  '212'
              130  FOR_ITER            258  'to 258'
              132  STORE_FAST               'key'

 L. 349       134  SETUP_FINALLY       162  'to 162'

 L. 350       136  LOAD_GLOBAL              getattr
              138  LOAD_FAST                'object'
              140  LOAD_FAST                'key'
              142  CALL_FUNCTION_2       2  ''
              144  STORE_FAST               'value'

 L. 352       146  LOAD_FAST                'key'
              148  LOAD_FAST                'processed'
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   158  'to 158'

 L. 353       154  LOAD_GLOBAL              AttributeError
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           152  '152'
              158  POP_BLOCK        
              160  JUMP_FORWARD        220  'to 220'
            162_0  COME_FROM_FINALLY   134  '134'

 L. 354       162  DUP_TOP          
              164  LOAD_GLOBAL              AttributeError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   218  'to 218'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L. 355       176  LOAD_FAST                'mro'
              178  GET_ITER         
            180_0  COME_FROM           208  '208'
            180_1  COME_FROM           192  '192'
              180  FOR_ITER            210  'to 210'
              182  STORE_FAST               'base'

 L. 356       184  LOAD_FAST                'key'
              186  LOAD_FAST                'base'
              188  LOAD_ATTR                __dict__
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE_BACK   180  'to 180'

 L. 357       194  LOAD_FAST                'base'
              196  LOAD_ATTR                __dict__
              198  LOAD_FAST                'key'
              200  BINARY_SUBSCR    
              202  STORE_FAST               'value'

 L. 358       204  POP_TOP          
              206  BREAK_LOOP          214  'to 214'
              208  JUMP_BACK           180  'to 180'
            210_0  COME_FROM           180  '180'

 L. 362       210  POP_EXCEPT       
              212  JUMP_BACK           130  'to 130'
            214_0  COME_FROM           206  '206'
              214  POP_EXCEPT       
              216  JUMP_FORWARD        220  'to 220'
            218_0  COME_FROM           168  '168'
              218  END_FINALLY      
            220_0  COME_FROM           216  '216'
            220_1  COME_FROM           160  '160'

 L. 363       220  LOAD_FAST                'predicate'
              222  POP_JUMP_IF_FALSE   232  'to 232'
              224  LOAD_FAST                'predicate'
              226  LOAD_FAST                'value'
              228  CALL_FUNCTION_1       1  ''
              230  POP_JUMP_IF_FALSE   246  'to 246'
            232_0  COME_FROM           222  '222'

 L. 364       232  LOAD_FAST                'results'
              234  LOAD_METHOD              append
              236  LOAD_FAST                'key'
              238  LOAD_FAST                'value'
              240  BUILD_TUPLE_2         2 
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           230  '230'

 L. 365       246  LOAD_FAST                'processed'
              248  LOAD_METHOD              add
              250  LOAD_FAST                'key'
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  JUMP_BACK           130  'to 130'
            258_0  COME_FROM           130  '130'

 L. 366       258  LOAD_FAST                'results'
              260  LOAD_ATTR                sort
              262  LOAD_LAMBDA              '<code_object <lambda>>'
              264  LOAD_STR                 'getmembers.<locals>.<lambda>'
              266  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              268  LOAD_CONST               ('key',)
              270  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              272  POP_TOP          

 L. 367       274  LOAD_FAST                'results'
              276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 212


    Attribute = namedtuple('Attribute', 'name kind defining_class object')

    def classify_class_attrs--- This code section failed: ---

 L. 398         0  LOAD_GLOBAL              getmro
                2  LOAD_FAST                'cls'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'mro'

 L. 399         8  LOAD_GLOBAL              getmro
               10  LOAD_GLOBAL              type
               12  LOAD_FAST                'cls'
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'metamro'

 L. 400        20  LOAD_GLOBAL              tuple
               22  LOAD_GENEXPR             '<code_object <genexpr>>'
               24  LOAD_STR                 'classify_class_attrs.<locals>.<genexpr>'
               26  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               28  LOAD_FAST                'metamro'
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'metamro'

 L. 401        38  LOAD_FAST                'cls'
               40  BUILD_TUPLE_1         1 
               42  LOAD_FAST                'mro'
               44  BINARY_ADD       
               46  STORE_FAST               'class_bases'

 L. 402        48  LOAD_FAST                'class_bases'
               50  LOAD_FAST                'metamro'
               52  BINARY_ADD       
               54  STORE_FAST               'all_bases'

 L. 403        56  LOAD_GLOBAL              dir
               58  LOAD_FAST                'cls'
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'names'

 L. 407        64  LOAD_FAST                'mro'
               66  GET_ITER         
             68_0  COME_FROM           114  '114'
               68  FOR_ITER            116  'to 116'
               70  STORE_FAST               'base'

 L. 408        72  LOAD_FAST                'base'
               74  LOAD_ATTR                __dict__
               76  LOAD_METHOD              items
               78  CALL_METHOD_0         0  ''
               80  GET_ITER         
             82_0  COME_FROM           112  '112'
             82_1  COME_FROM           100  '100'
               82  FOR_ITER            114  'to 114'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'k'
               88  STORE_FAST               'v'

 L. 409        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'v'
               94  LOAD_GLOBAL              types
               96  LOAD_ATTR                DynamicClassAttribute
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_FALSE_BACK    82  'to 82'

 L. 410       102  LOAD_FAST                'names'
              104  LOAD_METHOD              append
              106  LOAD_FAST                'k'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_BACK            82  'to 82'
            114_0  COME_FROM            82  '82'
              114  JUMP_BACK            68  'to 68'
            116_0  COME_FROM            68  '68'

 L. 411       116  BUILD_LIST_0          0 
              118  STORE_FAST               'result'

 L. 412       120  LOAD_GLOBAL              set
              122  CALL_FUNCTION_0       0  ''
              124  STORE_FAST               'processed'

 L. 414       126  LOAD_FAST                'names'
              128  GET_ITER         
            130_0  COME_FROM           590  '590'
            130_1  COME_FROM           442  '442'
          130_132  FOR_ITER            592  'to 592'
              134  STORE_FAST               'name'

 L. 424       136  LOAD_CONST               None
              138  STORE_FAST               'homecls'

 L. 425       140  LOAD_CONST               None
              142  STORE_FAST               'get_obj'

 L. 426       144  LOAD_CONST               None
              146  STORE_FAST               'dict_obj'

 L. 427       148  LOAD_FAST                'name'
              150  LOAD_FAST                'processed'
              152  COMPARE_OP               not-in
          154_156  POP_JUMP_IF_FALSE   378  'to 378'

 L. 428       158  SETUP_FINALLY       190  'to 190'

 L. 429       160  LOAD_FAST                'name'
              162  LOAD_STR                 '__dict__'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L. 430       168  LOAD_GLOBAL              Exception
              170  LOAD_STR                 "__dict__ is special, don't want the proxy"
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'

 L. 431       176  LOAD_GLOBAL              getattr
              178  LOAD_FAST                'cls'
              180  LOAD_FAST                'name'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'get_obj'
              186  POP_BLOCK        
              188  JUMP_FORWARD        224  'to 224'
            190_0  COME_FROM_FINALLY   158  '158'

 L. 432       190  DUP_TOP          
              192  LOAD_GLOBAL              Exception
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   222  'to 222'
              198  POP_TOP          
              200  STORE_FAST               'exc'
              202  POP_TOP          
              204  SETUP_FINALLY       210  'to 210'

 L. 433       206  POP_BLOCK        
              208  BEGIN_FINALLY    
            210_0  COME_FROM_FINALLY   204  '204'
              210  LOAD_CONST               None
              212  STORE_FAST               'exc'
              214  DELETE_FAST              'exc'
              216  END_FINALLY      
              218  POP_EXCEPT       
              220  JUMP_FORWARD        378  'to 378'
            222_0  COME_FROM           196  '196'
              222  END_FINALLY      
            224_0  COME_FROM           188  '188'

 L. 435       224  LOAD_GLOBAL              getattr
              226  LOAD_FAST                'get_obj'
              228  LOAD_STR                 '__objclass__'
              230  LOAD_FAST                'homecls'
              232  CALL_FUNCTION_3       3  ''
              234  STORE_FAST               'homecls'

 L. 436       236  LOAD_FAST                'homecls'
              238  LOAD_FAST                'class_bases'
              240  COMPARE_OP               not-in
          242_244  POP_JUMP_IF_FALSE   378  'to 378'

 L. 439       246  LOAD_CONST               None
              248  STORE_FAST               'homecls'

 L. 440       250  LOAD_CONST               None
              252  STORE_FAST               'last_cls'

 L. 442       254  LOAD_FAST                'class_bases'
              256  GET_ITER         
            258_0  COME_FROM           288  '288'
            258_1  COME_FROM           280  '280'
              258  FOR_ITER            292  'to 292'
              260  STORE_FAST               'srch_cls'

 L. 443       262  LOAD_GLOBAL              getattr
              264  LOAD_FAST                'srch_cls'
              266  LOAD_FAST                'name'
              268  LOAD_CONST               None
              270  CALL_FUNCTION_3       3  ''
              272  STORE_FAST               'srch_obj'

 L. 444       274  LOAD_FAST                'srch_obj'
              276  LOAD_FAST                'get_obj'
              278  COMPARE_OP               is
          280_282  POP_JUMP_IF_FALSE_BACK   258  'to 258'

 L. 445       284  LOAD_FAST                'srch_cls'
              286  STORE_FAST               'last_cls'
          288_290  JUMP_BACK           258  'to 258'
            292_0  COME_FROM           258  '258'

 L. 447       292  LOAD_FAST                'metamro'
              294  GET_ITER         
            296_0  COME_FROM           360  '360'
            296_1  COME_FROM           352  '352'
            296_2  COME_FROM           336  '336'
              296  FOR_ITER            364  'to 364'
              298  STORE_FAST               'srch_cls'

 L. 448       300  SETUP_FINALLY       318  'to 318'

 L. 449       302  LOAD_FAST                'srch_cls'
              304  LOAD_METHOD              __getattr__
              306  LOAD_FAST                'cls'
              308  LOAD_FAST                'name'
              310  CALL_METHOD_2         2  ''
              312  STORE_FAST               'srch_obj'
              314  POP_BLOCK        
              316  JUMP_FORWARD        346  'to 346'
            318_0  COME_FROM_FINALLY   300  '300'

 L. 450       318  DUP_TOP          
              320  LOAD_GLOBAL              AttributeError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   344  'to 344'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 451       334  POP_EXCEPT       
          336_338  JUMP_BACK           296  'to 296'
              340  POP_EXCEPT       
              342  JUMP_FORWARD        346  'to 346'
            344_0  COME_FROM           324  '324'
              344  END_FINALLY      
            346_0  COME_FROM           342  '342'
            346_1  COME_FROM           316  '316'

 L. 452       346  LOAD_FAST                'srch_obj'
              348  LOAD_FAST                'get_obj'
              350  COMPARE_OP               is
          352_354  POP_JUMP_IF_FALSE_BACK   296  'to 296'

 L. 453       356  LOAD_FAST                'srch_cls'
              358  STORE_FAST               'last_cls'
          360_362  JUMP_BACK           296  'to 296'
            364_0  COME_FROM           296  '296'

 L. 454       364  LOAD_FAST                'last_cls'
              366  LOAD_CONST               None
              368  COMPARE_OP               is-not
          370_372  POP_JUMP_IF_FALSE   378  'to 378'

 L. 455       374  LOAD_FAST                'last_cls'
              376  STORE_FAST               'homecls'
            378_0  COME_FROM           370  '370'
            378_1  COME_FROM           242  '242'
            378_2  COME_FROM           220  '220'
            378_3  COME_FROM           154  '154'

 L. 456       378  LOAD_FAST                'all_bases'
              380  GET_ITER         
            382_0  COME_FROM           428  '428'
            382_1  COME_FROM           394  '394'
              382  FOR_ITER            432  'to 432'
              384  STORE_FAST               'base'

 L. 457       386  LOAD_FAST                'name'
              388  LOAD_FAST                'base'
              390  LOAD_ATTR                __dict__
              392  COMPARE_OP               in
          394_396  POP_JUMP_IF_FALSE_BACK   382  'to 382'

 L. 458       398  LOAD_FAST                'base'
              400  LOAD_ATTR                __dict__
              402  LOAD_FAST                'name'
              404  BINARY_SUBSCR    
              406  STORE_FAST               'dict_obj'

 L. 459       408  LOAD_FAST                'homecls'
              410  LOAD_FAST                'metamro'
              412  COMPARE_OP               not-in
          414_416  POP_JUMP_IF_FALSE   422  'to 422'

 L. 460       418  LOAD_FAST                'base'
              420  STORE_FAST               'homecls'
            422_0  COME_FROM           414  '414'

 L. 461       422  POP_TOP          
          424_426  BREAK_LOOP          432  'to 432'
          428_430  JUMP_BACK           382  'to 382'
            432_0  COME_FROM           424  '424'
            432_1  COME_FROM           382  '382'

 L. 462       432  LOAD_FAST                'homecls'
              434  LOAD_CONST               None
              436  COMPARE_OP               is
          438_440  POP_JUMP_IF_FALSE   444  'to 444'

 L. 465       442  JUMP_BACK           130  'to 130'
            444_0  COME_FROM           438  '438'

 L. 466       444  LOAD_FAST                'get_obj'
              446  LOAD_CONST               None
              448  COMPARE_OP               is-not
          450_452  POP_JUMP_IF_FALSE   458  'to 458'
              454  LOAD_FAST                'get_obj'
              456  JUMP_FORWARD        460  'to 460'
            458_0  COME_FROM           450  '450'
              458  LOAD_FAST                'dict_obj'
            460_0  COME_FROM           456  '456'
              460  STORE_FAST               'obj'

 L. 468       462  LOAD_GLOBAL              isinstance
              464  LOAD_FAST                'dict_obj'
              466  LOAD_GLOBAL              staticmethod
              468  LOAD_GLOBAL              types
              470  LOAD_ATTR                BuiltinMethodType
              472  BUILD_TUPLE_2         2 
              474  CALL_FUNCTION_2       2  ''
          476_478  POP_JUMP_IF_FALSE   490  'to 490'

 L. 469       480  LOAD_STR                 'static method'
              482  STORE_FAST               'kind'

 L. 470       484  LOAD_FAST                'dict_obj'
              486  STORE_FAST               'obj'
              488  JUMP_FORWARD        560  'to 560'
            490_0  COME_FROM           476  '476'

 L. 471       490  LOAD_GLOBAL              isinstance
              492  LOAD_FAST                'dict_obj'
              494  LOAD_GLOBAL              classmethod
              496  LOAD_GLOBAL              types
              498  LOAD_ATTR                ClassMethodDescriptorType
              500  BUILD_TUPLE_2         2 
              502  CALL_FUNCTION_2       2  ''
          504_506  POP_JUMP_IF_FALSE   518  'to 518'

 L. 472       508  LOAD_STR                 'class method'
              510  STORE_FAST               'kind'

 L. 473       512  LOAD_FAST                'dict_obj'
              514  STORE_FAST               'obj'
              516  JUMP_FORWARD        560  'to 560'
            518_0  COME_FROM           504  '504'

 L. 474       518  LOAD_GLOBAL              isinstance
              520  LOAD_FAST                'dict_obj'
              522  LOAD_GLOBAL              property
              524  CALL_FUNCTION_2       2  ''
          526_528  POP_JUMP_IF_FALSE   540  'to 540'

 L. 475       530  LOAD_STR                 'property'
              532  STORE_FAST               'kind'

 L. 476       534  LOAD_FAST                'dict_obj'
              536  STORE_FAST               'obj'
              538  JUMP_FORWARD        560  'to 560'
            540_0  COME_FROM           526  '526'

 L. 477       540  LOAD_GLOBAL              isroutine
              542  LOAD_FAST                'obj'
              544  CALL_FUNCTION_1       1  ''
          546_548  POP_JUMP_IF_FALSE   556  'to 556'

 L. 478       550  LOAD_STR                 'method'
              552  STORE_FAST               'kind'
              554  JUMP_FORWARD        560  'to 560'
            556_0  COME_FROM           546  '546'

 L. 480       556  LOAD_STR                 'data'
              558  STORE_FAST               'kind'
            560_0  COME_FROM           554  '554'
            560_1  COME_FROM           538  '538'
            560_2  COME_FROM           516  '516'
            560_3  COME_FROM           488  '488'

 L. 481       560  LOAD_FAST                'result'
              562  LOAD_METHOD              append
              564  LOAD_GLOBAL              Attribute
              566  LOAD_FAST                'name'
              568  LOAD_FAST                'kind'
              570  LOAD_FAST                'homecls'
              572  LOAD_FAST                'obj'
              574  CALL_FUNCTION_4       4  ''
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          

 L. 482       580  LOAD_FAST                'processed'
              582  LOAD_METHOD              add
              584  LOAD_FAST                'name'
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          
              590  JUMP_BACK           130  'to 130'
            592_0  COME_FROM           130  '130'

 L. 483       592  LOAD_FAST                'result'
              594  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 344_0


    def getmro(cls):
        """Return tuple of base classes (including cls) in method resolution order."""
        return cls.__mro__


    def unwrap(func, *, stop=None):
        """Get the object wrapped by *func*.

   Follows the chain of :attr:`__wrapped__` attributes returning the last
   object in the chain.

   *stop* is an optional callback accepting an object in the wrapper chain
   as its sole argument that allows the unwrapping to be terminated early if
   the callback returns a true value. If the callback never returns a true
   value, the last object in the chain is returned as usual. For example,
   :func:`signature` uses this to stop unwrapping if any object in the
   chain has a ``__signature__`` attribute defined.

   :exc:`ValueError` is raised if a cycle is encountered.

    """
        if stop is None:

            def _is_wrapper(f):
                return hasattr(f, '__wrapped__')

        else:

            def _is_wrapper(f):
                return hasattr(f, '__wrapped__') and not stop(f)

        f = func
        memo = {id(f): f}
        recursion_limit = sys.getrecursionlimit()
        while True:
            if _is_wrapper(func):
                func = func.__wrapped__
                id_func = id(func)
                if id_func in memo or (len(memo) >= recursion_limit):
                    raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
                memo[id_func] = func

        return func


    def indentsize(line):
        """Return the indent size, in spaces, at the start of a line of text."""
        expline = line.expandtabs()
        return len(expline) - len(expline.lstrip())


    def _findclass(func):
        cls = sys.modules.get(func.__module__)
        if cls is None:
            return
        for name in func.__qualname__.split('.')[:-1]:
            cls = getattr(cls, name)
        else:
            if not isclass(cls):
                return
            return cls


    def _finddoc--- This code section failed: ---

 L. 545         0  LOAD_GLOBAL              isclass
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE    84  'to 84'

 L. 546         8  LOAD_FAST                'obj'
               10  LOAD_ATTR                __mro__
               12  GET_ITER         
             14_0  COME_FROM            78  '78'
             14_1  COME_FROM            68  '68'
             14_2  COME_FROM            54  '54'
             14_3  COME_FROM            24  '24'
               14  FOR_ITER             80  'to 80'
               16  STORE_FAST               'base'

 L. 547        18  LOAD_FAST                'base'
               20  LOAD_GLOBAL              object
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 548        26  SETUP_FINALLY        38  'to 38'

 L. 549        28  LOAD_FAST                'base'
               30  LOAD_ATTR                __doc__
               32  STORE_FAST               'doc'
               34  POP_BLOCK        
               36  JUMP_FORWARD         62  'to 62'
             38_0  COME_FROM_FINALLY    26  '26'

 L. 550        38  DUP_TOP          
               40  LOAD_GLOBAL              AttributeError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 551        52  POP_EXCEPT       
               54  JUMP_BACK            14  'to 14'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            44  '44'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            36  '36'

 L. 552        62  LOAD_FAST                'doc'
               64  LOAD_CONST               None
               66  COMPARE_OP               is-not
               68  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 553        70  LOAD_FAST                'doc'
               72  ROT_TWO          
               74  POP_TOP          
               76  RETURN_VALUE     
               78  JUMP_BACK            14  'to 14'
             80_0  COME_FROM            14  '14'

 L. 554        80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM             6  '6'

 L. 556        84  LOAD_GLOBAL              ismethod
               86  LOAD_FAST                'obj'
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_FALSE   154  'to 154'

 L. 557        92  LOAD_FAST                'obj'
               94  LOAD_ATTR                __func__
               96  LOAD_ATTR                __name__
               98  STORE_FAST               'name'

 L. 558       100  LOAD_FAST                'obj'
              102  LOAD_ATTR                __self__
              104  STORE_FAST               'self'

 L. 559       106  LOAD_GLOBAL              isclass
              108  LOAD_FAST                'self'
              110  CALL_FUNCTION_1       1  ''
              112  POP_JUMP_IF_FALSE   144  'to 144'

 L. 560       114  LOAD_GLOBAL              getattr
              116  LOAD_GLOBAL              getattr
              118  LOAD_FAST                'self'
              120  LOAD_FAST                'name'
              122  LOAD_CONST               None
              124  CALL_FUNCTION_3       3  ''
              126  LOAD_STR                 '__func__'
              128  CALL_FUNCTION_2       2  ''
              130  LOAD_FAST                'obj'
              132  LOAD_ATTR                __func__
              134  COMPARE_OP               is

 L. 559       136  POP_JUMP_IF_FALSE   144  'to 144'

 L. 562       138  LOAD_FAST                'self'
              140  STORE_FAST               'cls'
              142  JUMP_FORWARD        446  'to 446'
            144_0  COME_FROM           136  '136'
            144_1  COME_FROM           112  '112'

 L. 564       144  LOAD_FAST                'self'
              146  LOAD_ATTR                __class__
              148  STORE_FAST               'cls'
          150_152  JUMP_FORWARD        446  'to 446'
            154_0  COME_FROM            90  '90'

 L. 565       154  LOAD_GLOBAL              isfunction
              156  LOAD_FAST                'obj'
              158  CALL_FUNCTION_1       1  ''
              160  POP_JUMP_IF_FALSE   204  'to 204'

 L. 566       162  LOAD_FAST                'obj'
              164  LOAD_ATTR                __name__
              166  STORE_FAST               'name'

 L. 567       168  LOAD_GLOBAL              _findclass
              170  LOAD_FAST                'obj'
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'cls'

 L. 568       176  LOAD_FAST                'cls'
              178  LOAD_CONST               None
              180  COMPARE_OP               is
              182  POP_JUMP_IF_TRUE    198  'to 198'
              184  LOAD_GLOBAL              getattr
              186  LOAD_FAST                'cls'
              188  LOAD_FAST                'name'
              190  CALL_FUNCTION_2       2  ''
              192  LOAD_FAST                'obj'
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   202  'to 202'
            198_0  COME_FROM           182  '182'

 L. 569       198  LOAD_CONST               None
              200  RETURN_VALUE     
            202_0  COME_FROM           196  '196'
              202  JUMP_FORWARD        446  'to 446'
            204_0  COME_FROM           160  '160'

 L. 570       204  LOAD_GLOBAL              isbuiltin
              206  LOAD_FAST                'obj'
              208  CALL_FUNCTION_1       1  ''
          210_212  POP_JUMP_IF_FALSE   272  'to 272'

 L. 571       214  LOAD_FAST                'obj'
              216  LOAD_ATTR                __name__
              218  STORE_FAST               'name'

 L. 572       220  LOAD_FAST                'obj'
              222  LOAD_ATTR                __self__
              224  STORE_FAST               'self'

 L. 573       226  LOAD_GLOBAL              isclass
              228  LOAD_FAST                'self'
              230  CALL_FUNCTION_1       1  ''
          232_234  POP_JUMP_IF_FALSE   264  'to 264'

 L. 574       236  LOAD_FAST                'self'
              238  LOAD_ATTR                __qualname__
              240  LOAD_STR                 '.'
              242  BINARY_ADD       
              244  LOAD_FAST                'name'
              246  BINARY_ADD       
              248  LOAD_FAST                'obj'
              250  LOAD_ATTR                __qualname__
              252  COMPARE_OP               ==

 L. 573   254_256  POP_JUMP_IF_FALSE   264  'to 264'

 L. 576       258  LOAD_FAST                'self'
              260  STORE_FAST               'cls'
              262  JUMP_FORWARD        270  'to 270'
            264_0  COME_FROM           254  '254'
            264_1  COME_FROM           232  '232'

 L. 578       264  LOAD_FAST                'self'
              266  LOAD_ATTR                __class__
              268  STORE_FAST               'cls'
            270_0  COME_FROM           262  '262'
              270  JUMP_FORWARD        446  'to 446'
            272_0  COME_FROM           210  '210'

 L. 580       272  LOAD_GLOBAL              isinstance
              274  LOAD_FAST                'obj'
              276  LOAD_GLOBAL              property
              278  CALL_FUNCTION_2       2  ''
          280_282  POP_JUMP_IF_FALSE   336  'to 336'

 L. 581       284  LOAD_FAST                'obj'
              286  LOAD_ATTR                fget
              288  STORE_FAST               'func'

 L. 582       290  LOAD_FAST                'func'
              292  LOAD_ATTR                __name__
              294  STORE_FAST               'name'

 L. 583       296  LOAD_GLOBAL              _findclass
              298  LOAD_FAST                'func'
              300  CALL_FUNCTION_1       1  ''
              302  STORE_FAST               'cls'

 L. 584       304  LOAD_FAST                'cls'
              306  LOAD_CONST               None
              308  COMPARE_OP               is
          310_312  POP_JUMP_IF_TRUE    330  'to 330'
              314  LOAD_GLOBAL              getattr
              316  LOAD_FAST                'cls'
              318  LOAD_FAST                'name'
              320  CALL_FUNCTION_2       2  ''
              322  LOAD_FAST                'obj'
              324  COMPARE_OP               is-not
          326_328  POP_JUMP_IF_FALSE   446  'to 446'
            330_0  COME_FROM           310  '310'

 L. 585       330  LOAD_CONST               None
              332  RETURN_VALUE     
              334  JUMP_FORWARD        446  'to 446'
            336_0  COME_FROM           280  '280'

 L. 586       336  LOAD_GLOBAL              ismethoddescriptor
              338  LOAD_FAST                'obj'
              340  CALL_FUNCTION_1       1  ''
          342_344  POP_JUMP_IF_TRUE    356  'to 356'
              346  LOAD_GLOBAL              isdatadescriptor
              348  LOAD_FAST                'obj'
              350  CALL_FUNCTION_1       1  ''
          352_354  POP_JUMP_IF_FALSE   442  'to 442'
            356_0  COME_FROM           342  '342'

 L. 587       356  LOAD_FAST                'obj'
              358  LOAD_ATTR                __name__
              360  STORE_FAST               'name'

 L. 588       362  LOAD_FAST                'obj'
              364  LOAD_ATTR                __objclass__
              366  STORE_FAST               'cls'

 L. 589       368  LOAD_GLOBAL              getattr
              370  LOAD_FAST                'cls'
              372  LOAD_FAST                'name'
              374  CALL_FUNCTION_2       2  ''
              376  LOAD_FAST                'obj'
              378  COMPARE_OP               is-not
          380_382  POP_JUMP_IF_FALSE   388  'to 388'

 L. 590       384  LOAD_CONST               None
              386  RETURN_VALUE     
            388_0  COME_FROM           380  '380'

 L. 591       388  LOAD_GLOBAL              ismemberdescriptor
              390  LOAD_FAST                'obj'
              392  CALL_FUNCTION_1       1  ''
          394_396  POP_JUMP_IF_FALSE   446  'to 446'

 L. 592       398  LOAD_GLOBAL              getattr
              400  LOAD_FAST                'cls'
              402  LOAD_STR                 '__slots__'
              404  LOAD_CONST               None
              406  CALL_FUNCTION_3       3  ''
              408  STORE_FAST               'slots'

 L. 593       410  LOAD_GLOBAL              isinstance
              412  LOAD_FAST                'slots'
              414  LOAD_GLOBAL              dict
              416  CALL_FUNCTION_2       2  ''
          418_420  POP_JUMP_IF_FALSE   446  'to 446'
              422  LOAD_FAST                'name'
              424  LOAD_FAST                'slots'
              426  COMPARE_OP               in
          428_430  POP_JUMP_IF_FALSE   446  'to 446'

 L. 594       432  LOAD_FAST                'slots'
              434  LOAD_FAST                'name'
              436  BINARY_SUBSCR    
              438  RETURN_VALUE     
              440  JUMP_FORWARD        446  'to 446'
            442_0  COME_FROM           352  '352'

 L. 596       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           440  '440'
            446_1  COME_FROM           428  '428'
            446_2  COME_FROM           418  '418'
            446_3  COME_FROM           394  '394'
            446_4  COME_FROM           334  '334'
            446_5  COME_FROM           326  '326'
            446_6  COME_FROM           270  '270'
            446_7  COME_FROM           202  '202'
            446_8  COME_FROM           150  '150'
            446_9  COME_FROM           142  '142'

 L. 597       446  LOAD_FAST                'cls'
              448  LOAD_ATTR                __mro__
              450  GET_ITER         
            452_0  COME_FROM           520  '520'
            452_1  COME_FROM           508  '508'
            452_2  COME_FROM           492  '492'
              452  FOR_ITER            524  'to 524'
              454  STORE_FAST               'base'

 L. 598       456  SETUP_FINALLY       474  'to 474'

 L. 599       458  LOAD_GLOBAL              getattr
              460  LOAD_FAST                'base'
              462  LOAD_FAST                'name'
              464  CALL_FUNCTION_2       2  ''
              466  LOAD_ATTR                __doc__
              468  STORE_FAST               'doc'
              470  POP_BLOCK        
              472  JUMP_FORWARD        502  'to 502'
            474_0  COME_FROM_FINALLY   456  '456'

 L. 600       474  DUP_TOP          
              476  LOAD_GLOBAL              AttributeError
              478  COMPARE_OP               exception-match
          480_482  POP_JUMP_IF_FALSE   500  'to 500'
              484  POP_TOP          
              486  POP_TOP          
              488  POP_TOP          

 L. 601       490  POP_EXCEPT       
          492_494  JUMP_BACK           452  'to 452'
              496  POP_EXCEPT       
              498  JUMP_FORWARD        502  'to 502'
            500_0  COME_FROM           480  '480'
              500  END_FINALLY      
            502_0  COME_FROM           498  '498'
            502_1  COME_FROM           472  '472'

 L. 602       502  LOAD_FAST                'doc'
              504  LOAD_CONST               None
              506  COMPARE_OP               is-not
          508_510  POP_JUMP_IF_FALSE_BACK   452  'to 452'

 L. 603       512  LOAD_FAST                'doc'
              514  ROT_TWO          
              516  POP_TOP          
              518  RETURN_VALUE     
          520_522  JUMP_BACK           452  'to 452'
            524_0  COME_FROM           452  '452'

Parse error at or near `COME_FROM' instruction at offset 60_0


    def getdoc(object):
        """Get the documentation string for an object.

    All tabs are expanded to spaces.  To clean up docstrings that are
    indented to line up with blocks of code, any whitespace than can be
    uniformly removed from the second line onwards is removed."""
        try:
            doc = object.__doc__
        except AttributeError:
            return
        else:
            if doc is None:
                try:
                    doc = _finddoc(object)
                except (AttributeError, TypeError):
                    return
                else:
                    if not isinstance(doc, str):
                        return
                    else:
                        return cleandoc(doc)


    def cleandoc(doc):
        """Clean up indentation from docstrings.

    Any whitespace that can be uniformly removed from the second line
    onwards is removed."""
        try:
            lines = doc.expandtabs().split('\n')
        except UnicodeError:
            return
        else:
            margin = sys.maxsize
            for line in lines[1:]:
                content = len(line.lstrip())
                if content:
                    indent = len(line) - content
                    margin = min(margin, indent)
            else:
                if lines:
                    lines[0] = lines[0].lstrip()

            if margin < sys.maxsize:
                for i in range(1, len(lines)):
                    lines[i] = lines[i][margin:]
                else:
                    while True:
                        if lines:
                            lines[(-1)] or lines.pop()

                    while True:
                        if lines:
                            lines[0] or lines.pop(0)

                return '\n'.join(lines)


    def getfile(object):
        """Work out which source or compiled file an object was defined in."""
        if ismodule(object):
            if getattr(object, '__file__', None):
                return object.__file__
            raise TypeError('{!r} is a built-in module'.format(object))
        if isclass(object):
            if hasattr(object, '__module__'):
                module = sys.modules.get(object.__module__)
                if getattr(module, '__file__', None):
                    return module.__file__
            raise TypeError('{!r} is a built-in class'.format(object))
        if ismethod(object):
            object = object.__func__
        if isfunction(object):
            object = object.__code__
        if istraceback(object):
            object = object.tb_frame
        if isframe(object):
            object = object.f_code
        if iscode(object):
            return object.co_filename
        raise TypeError('module, class, method, function, traceback, frame, or code object was expected, got {}'.format(type(object).__name__))


    def getmodulename(path):
        """Return the module name for a given file, or None."""
        fname = os.path.basename(path)
        suffixes = [(
         -len(suffix), suffix) for suffix in importlib.machinery.all_suffixes()]
        suffixes.sort()
        for neglen, suffix in suffixes:
            if fname.endswith(suffix):
                return fname[:neglen]


    def getsourcefile(object):
        """Return the filename that can be used to locate an object's source.
    Return None if no way can be identified to get the source.
    """
        filename = getfile(object)
        all_bytecode_suffixes = importlib.machinery.DEBUG_BYTECODE_SUFFIXES[:]
        all_bytecode_suffixes += importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES[:]
        if any((filename.endswith(s) for s in all_bytecode_suffixes)):
            filename = os.path.splitext(filename)[0] + importlib.machinery.SOURCE_SUFFIXES[0]
        elif any((filename.endswith(s) for s in importlib.machinery.EXTENSION_SUFFIXES)):
            return
        if os.path.exists(filename):
            return filename
        if getattr(getmodule(object, filename), '__loader__', None) is not None:
            return filename
        if filename in linecache.cache:
            return filename


    def getabsfile(object, _filename=None):
        """Return an absolute path to the source or compiled file for an object.

    The idea is for each object to have a unique origin, so this routine
    normalizes the result as much as possible."""
        if _filename is None:
            _filename = getsourcefile(object) or getfile(object)
        return os.path.normcase(os.path.abspath(_filename))


    modulesbyfile = {}
    _filesbymodname = {}

    def getmodule(object, _filename=None):
        """Return the module an object was defined in, or None if not found."""
        if ismodule(object):
            return object
        if hasattr(object, '__module__'):
            return sys.modules.get(object.__module__)
        if _filename is not None:
            if _filename in modulesbyfile:
                return sys.modules.get(modulesbyfile[_filename])
        try:
            file = getabsfile(object, _filename)
        except TypeError:
            return
        else:
            if file in modulesbyfile:
                return sys.modules.get(modulesbyfile[file])
        for modname, module in list(sys.modules.items()):
            if ismodule(module):
                if hasattr(module, '__file__'):
                    f = module.__file__
                    if f == _filesbymodname.getmodnameNone:
                        pass
                    else:
                        _filesbymodname[modname] = f
                        f = getabsfile(module)
                        modulesbyfile[f] = modulesbyfile[os.path.realpath(f)] = module.__name__
        else:
            if file in modulesbyfile:
                return sys.modules.get(modulesbyfile[file])
            main = sys.modules['__main__']
            if not hasattr(object, '__name__'):
                return
            if hasattr(main, object.__name__):
                mainobject = getattr(main, object.__name__)
                if mainobject is object:
                    return main
            builtin = sys.modules['builtins']
            if hasattr(builtin, object.__name__):
                builtinobject = getattr(builtin, object.__name__)
                if builtinobject is object:
                    return builtin


    def findsource(object):
        """Return the entire source file and starting line number for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of all the lines
    in the file and the line number indexes a line in that list.  An OSError
    is raised if the source code cannot be retrieved."""
        file = getsourcefile(object)
        if file:
            linecache.checkcache(file)
        else:
            file = getfile(object)
            if file.startswith('<') and not file.endswith('>'):
                raise OSError('source code not available')
        module = getmodule(object, file)
        if module:
            lines = linecache.getlinesfilemodule.__dict__
        else:
            lines = linecache.getlines(file)
        if not lines:
            raise OSError('could not get source code')
        if ismodule(object):
            return (lines, 0)
        if isclass(object):
            name = object.__name__
            pat = re.compile('^(\\s*)class\\s*' + name + '\\b')
            candidates = []
            for i in range(len(lines)):
                match = pat.match(lines[i])
                if match:
                    if lines[i][0] == 'c':
                        return (lines, i)
                    else:
                        candidates.append((match.group(1), i))
            else:
                if candidates:
                    candidates.sort()
                    return (
                     lines, candidates[0][1])
                raise OSError('could not find class definition')

        if ismethod(object):
            object = object.__func__
        if isfunction(object):
            object = object.__code__
        if istraceback(object):
            object = object.tb_frame
        if isframe(object):
            object = object.f_code
        if iscode(object):
            if not hasattr(object, 'co_firstlineno'):
                raise OSError('could not find function definition')
            lnum = object.co_firstlineno - 1
            pat = re.compile('^(\\s*def\\s)|(\\s*async\\s+def\\s)|(.*(?<!\\w)lambda(:|\\s))|^(\\s*@)')
            while True:
                lnum = pat.match(lines[lnum]) if lnum > 0 else lnum - 1

            return (lines, lnum)
        raise OSError('could not find code object')


    def getcomments(object):
        """Get lines of comments immediately preceding an object's source code.

    Returns None when source can't be found.
    """
        try:
            lines, lnum = findsource(object)
        except (OSError, TypeError):
            return
        else:
            if ismodule(object):
                start = 0
                if lines:
                    if lines[0][:2] == '#!':
                        start = 1
                        while start < len(lines):
                            if lines[start].strip() in ('', '#'):
                                start = start + 1

                    if start < len(lines):
                        if lines[start][:1] == '#':
                            comments = []
                            end = start
                            while end < len(lines):
                                if lines[end][:1] == '#':
                                    comments.append(lines[end].expandtabs())
                                    end = end + 1

                            return ''.join(comments)
            elif lnum > 0:
                indent = indentsize(lines[lnum])
                end = lnum - 1
                if end >= 0:
                    if lines[end].lstrip()[:1] == '#':
                        if indentsize(lines[end]) == indent:
                            comments = [lines[end].expandtabs().lstrip()]
                            if end > 0:
                                end = end - 1
                                comment = lines[end].expandtabs().lstrip()
                                while comment[:1] == '#':
                                    if indentsize(lines[end]) == indent:
                                        comments[:0] = [
                                         comment]
                                        end = end - 1
                                        if end < 0:
                                            pass
                                        else:
                                            comment = lines[end].expandtabs().lstrip()

                                while comments:
                                    if comments[0].strip() == '#':
                                        comments[:1] = []

                                while comments:
                                    if comments[(-1)].strip() == '#':
                                        comments[-1:] = []

                                return ''.join(comments)


    class EndOfBlock(Exception):
        pass


    class BlockFinder:
        __doc__ = 'Provide a tokeneater() method to detect the end of a code block.'

        def __init__(self):
            self.indent = 0
            self.islambda = False
            self.started = False
            self.passline = False
            self.indecorator = False
            self.decoratorhasargs = False
            self.last = 1

        def tokeneater(self, type, token, srowcol, erowcol, line):
            if not (self.started or self.indecorator):
                if token == '@':
                    self.indecorator = True
                elif token in ('def', 'class', 'lambda'):
                    if token == 'lambda':
                        self.islambda = True
                    self.started = True
                self.passline = True
            elif token == '(':
                if self.indecorator:
                    self.decoratorhasargs = True
            elif token == ')':
                if self.indecorator:
                    self.indecorator = False
                    self.decoratorhasargs = False
            elif type == tokenize.NEWLINE:
                self.passline = False
                self.last = srowcol[0]
                if self.islambda:
                    raise EndOfBlock
                if self.indecorator:
                    if not self.decoratorhasargs:
                        self.indecorator = False
            elif self.passline:
                pass
            elif type == tokenize.INDENT:
                self.indent = self.indent + 1
                self.passline = True
            elif type == tokenize.DEDENT:
                self.indent = self.indent - 1
                if self.indent <= 0:
                    raise EndOfBlock
            elif self.indent == 0:
                if type not in (tokenize.COMMENT, tokenize.NL):
                    raise EndOfBlock


    def getblock(lines):
        """Extract the block of code at the top of the given list of lines."""
        blockfinder = BlockFinder()
        try:
            tokens = tokenize.generate_tokens(iter(lines).__next__)
            for _token in tokens:
                (blockfinder.tokeneater)(*_token)

        except (EndOfBlock, IndentationError):
            pass
        else:
            return lines[:blockfinder.last]


    def getsourcelines(object):
        """Return a list of source lines and starting line number for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a list of the lines
    corresponding to the object and the line number indicates where in the
    original source file the first line of code was found.  An OSError is
    raised if the source code cannot be retrieved."""
        object = unwrap(object)
        lines, lnum = findsource(object)
        if istraceback(object):
            object = object.tb_frame
        if not ismodule(object):
            if not isframe(object) or object.f_code.co_name == '<module>':
                return (
                 lines, 0)
            return (
             getblock(lines[lnum:]), lnum + 1)


    def getsource(object):
        """Return the text of the source code for an object.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a single string.  An
    OSError is raised if the source code cannot be retrieved."""
        lines, lnum = getsourcelines(object)
        return ''.join(lines)


    def walktree(classes, children, parent):
        """Recursive helper function for getclasstree()."""
        results = []
        classes.sort(key=(attrgetter('__module__', '__name__')))
        for c in classes:
            results.append((c, c.__bases__))
            if c in children:
                results.append(walktree(children[c], children, c))
        else:
            return results


    def getclasstree(classes, unique=False):
        """Arrange the given list of classes into a hierarchy of nested lists.

    Where a nested list appears, it contains classes derived from the class
    whose entry immediately precedes the list.  Each entry is a 2-tuple
    containing a class and a tuple of its base classes.  If the 'unique'
    argument is true, exactly one entry appears in the returned structure
    for each class in the given list.  Otherwise, classes using multiple
    inheritance and their descendants will appear multiple times."""
        children = {}
        roots = []
        for c in classes:
            if c.__bases__:
                for parent in c.__bases__:
                    if parent not in children:
                        children[parent] = []
                    elif c not in children[parent]:
                        children[parent].append(c)
                    if unique:
                        if parent in classes:
                            break

            else:
                if c not in roots:
                    roots.append(c)
        else:
            for parent in children:
                if parent not in classes:
                    roots.append(parent)
            else:
                return walktree(roots, children, None)


    Arguments = namedtuple('Arguments', 'args, varargs, varkw')

    def getargs(co):
        """Get information about the arguments accepted by a code object.

    Three things are returned: (args, varargs, varkw), where
    'args' is the list of argument names. Keyword-only arguments are
    appended. 'varargs' and 'varkw' are the names of the * and **
    arguments or None."""
        if not iscode(co):
            raise TypeError('{!r} is not a code object'.format(co))
        names = co.co_varnames
        nargs = co.co_argcount
        nkwargs = co.co_kwonlyargcount
        args = list(names[:nargs])
        kwonlyargs = list(names[nargs:nargs + nkwargs])
        step = 0
        nargs += nkwargs
        varargs = None
        if co.co_flags & CO_VARARGS:
            varargs = co.co_varnames[nargs]
            nargs = nargs + 1
        varkw = None
        if co.co_flags & CO_VARKEYWORDS:
            varkw = co.co_varnames[nargs]
        return Arguments(args + kwonlyargs, varargs, varkw)


    ArgSpec = namedtuple('ArgSpec', 'args varargs keywords defaults')

    def getargspec(func):
        """Get the names and default values of a function's parameters.

    A tuple of four things is returned: (args, varargs, keywords, defaults).
    'args' is a list of the argument names, including keyword-only argument names.
    'varargs' and 'keywords' are the names of the * and ** parameters or None.
    'defaults' is an n-tuple of the default values of the last n parameters.

    This function is deprecated, as it does not support annotations or
    keyword-only parameters and will raise ValueError if either is present
    on the supplied callable.

    For a more structured introspection API, use inspect.signature() instead.

    Alternatively, use getfullargspec() for an API with a similar namedtuple
    based interface, but full support for annotations and keyword-only
    parameters.

    Deprecated since Python 3.5, use `inspect.getfullargspec()`.
    """
        warnings.warn('inspect.getargspec() is deprecated since Python 3.0, use inspect.signature() or inspect.getfullargspec()', DeprecationWarning,
          stacklevel=2)
        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = getfullargspec(func)
        if kwonlyargs or (ann):
            raise ValueError('Function has keyword-only parameters or annotations, use inspect.signature() API which can support them')
        return ArgSpecargsvarargsvarkwdefaults


    FullArgSpec = namedtuple('FullArgSpec', 'args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations')

    def getfullargspec(func):
        """Get the names and default values of a callable object's parameters.

    A tuple of seven things is returned:
    (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations).
    'args' is a list of the parameter names.
    'varargs' and 'varkw' are the names of the * and ** parameters or None.
    'defaults' is an n-tuple of the default values of the last n parameters.
    'kwonlyargs' is a list of keyword-only parameter names.
    'kwonlydefaults' is a dictionary mapping names from kwonlyargs to defaults.
    'annotations' is a dictionary mapping parameter names to annotations.

    Notable differences from inspect.signature():
      - the "self" parameter is always reported, even for bound methods
      - wrapper chains defined by __wrapped__ *not* unwrapped automatically
    """
        try:
            sig = _signature_from_callable(func, follow_wrapper_chains=False,
              skip_bound_arg=False,
              sigcls=Signature)
        except Exception as ex:
            try:
                raise TypeError('unsupported callable') from ex
            finally:
                ex = None
                del ex

        else:
            args = []
            varargs = None
            varkw = None
            posonlyargs = []
            kwonlyargs = []
            defaults = ()
            annotations = {}
            defaults = ()
            kwdefaults = {}
            if sig.return_annotation is not sig.empty:
                annotations['return'] = sig.return_annotation
            for param in sig.parameters.values():
                kind = param.kind
                name = param.name
                if kind is _POSITIONAL_ONLY:
                    posonlyargs.append(name)
                    if param.default is not param.empty:
                        defaults += (param.default,)
                elif kind is _POSITIONAL_OR_KEYWORD:
                    args.append(name)
                    if param.default is not param.empty:
                        defaults += (param.default,)
                elif kind is _VAR_POSITIONAL:
                    varargs = name
                elif kind is _KEYWORD_ONLY:
                    kwonlyargs.append(name)
                    if param.default is not param.empty:
                        kwdefaults[name] = param.default
                elif kind is _VAR_KEYWORD:
                    varkw = name
                if param.annotation is not param.empty:
                    annotations[name] = param.annotation
            else:
                if not kwdefaults:
                    kwdefaults = None
                else:
                    if not defaults:
                        defaults = None
                    return FullArgSpec(posonlyargs + args, varargs, varkw, defaults, kwonlyargs, kwdefaults, annotations)


    ArgInfo = namedtuple('ArgInfo', 'args varargs keywords locals')

    def getargvalues(frame):
        """Get information about arguments passed into a particular frame.

    A tuple of four things is returned: (args, varargs, varkw, locals).
    'args' is a list of the argument names.
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'locals' is the locals dictionary of the given frame."""
        args, varargs, varkw = getargs(frame.f_code)
        return ArgInfoargsvarargsvarkwframe.f_locals


    def formatannotation(annotation, base_module=None):
        if getattr(annotation, '__module__', None) == 'typing':
            return repr(annotation).replace'typing.'''
        if isinstance(annotation, type):
            if annotation.__module__ in ('builtins', base_module):
                return annotation.__qualname__
            return annotation.__module__ + '.' + annotation.__qualname__
        return repr(annotation)


    def formatannotationrelativeto(object):
        module = getattr(object, '__module__', None)

        def _formatannotation(annotation):
            return formatannotation(annotation, module)

        return _formatannotation


    def formatargspec(args, varargs=None, varkw=None, defaults=None, kwonlyargs=(), kwonlydefaults={}, annotations={}, formatarg=str, formatvarargs=lambda name: '*' + name, formatvarkw=lambda name: '**' + name, formatvalue=lambda value: '=' + repr(value), formatreturns=lambda text: ' -> ' + text, formatannotation=formatannotation):
        """Format an argument spec from the values returned by getfullargspec.

    The first seven arguments are (args, varargs, varkw, defaults,
    kwonlyargs, kwonlydefaults, annotations).  The other five arguments
    are the corresponding optional formatting functions that are called to
    turn names and values into strings.  The last argument is an optional
    function to format the sequence of arguments.

    Deprecated since Python 3.5: use the `signature` function and `Signature`
    objects.
    """
        from warnings import warn
        warn('`formatargspec` is deprecated since Python 3.5. Use `signature` and the `Signature` object directly', DeprecationWarning,
          stacklevel=2)

        def formatargandannotation(arg):
            result = formatarg(arg)
            if arg in annotations:
                result += ': ' + formatannotation(annotations[arg])
            return result

        specs = []
        if defaults:
            firstdefault = len(args) - len(defaults)
        for i, arg in enumerate(args):
            spec = formatargandannotation(arg)
            if defaults:
                if i >= firstdefault:
                    spec = spec + formatvalue(defaults[(i - firstdefault)])
            specs.append(spec)
        else:
            if varargs is not None:
                specs.append(formatvarargs(formatargandannotation(varargs)))
            elif kwonlyargs:
                specs.append('*')
            if kwonlyargs:
                for kwonlyarg in kwonlyargs:
                    spec = formatargandannotation(kwonlyarg)
                    if kwonlydefaults:
                        if kwonlyarg in kwonlydefaults:
                            spec += formatvalue(kwonlydefaults[kwonlyarg])
                    specs.append(spec)
                else:
                    if varkw is not None:
                        specs.append(formatvarkw(formatargandannotation(varkw)))
                    result = '(' + ', '.join(specs) + ')'
                    if 'return' in annotations:
                        result += formatreturns(formatannotation(annotations['return']))

                return result


    def formatargvalues(args, varargs, varkw, locals, formatarg=str, formatvarargs=lambda name: '*' + name, formatvarkw=lambda name: '**' + name, formatvalue=lambda value: '=' + repr(value)):
        """Format an argument spec from the 4 values returned by getargvalues.

    The first four arguments are (args, varargs, varkw, locals).  The
    next four arguments are the corresponding optional formatting functions
    that are called to turn names and values into strings.  The ninth
    argument is an optional function to format the sequence of arguments."""

        def convert(name, locals=locals, formatarg=formatarg, formatvalue=formatvalue):
            return formatarg(name) + formatvalue(locals[name])

        specs = []
        for i in range(len(args)):
            specs.append(convert(args[i]))
        else:
            if varargs:
                specs.append(formatvarargs(varargs) + formatvalue(locals[varargs]))
            if varkw:
                specs.append(formatvarkw(varkw) + formatvalue(locals[varkw]))
            return '(' + ', '.join(specs) + ')'


    def _missing_arguments(f_name, argnames, pos, values):
        names = [repr(name) for name in argnames if name not in values]
        missing = len(names)
        if missing == 1:
            s = names[0]
        elif missing == 2:
            s = ('{} and {}'.format)(*names)
        else:
            tail = (', {} and {}'.format)(*names[-2:])
            del names[-2:]
            s = ', '.join(names) + tail
        raise TypeError('%s() missing %i required %s argument%s: %s' % (
         f_name, missing,
         'positional' if pos else 'keyword-only',
         '' if missing == 1 else 's', s))


    def _too_many(f_name, args, kwonly, varargs, defcount, given, values):
        atleast = len(args) - defcount
        kwonly_given = len([arg for arg in kwonly if arg in values])
        if varargs:
            plural = atleast != 1
            sig = 'at least %d' % (atleast,)
        elif defcount:
            plural = True
            sig = 'from %d to %d' % (atleast, len(args))
        else:
            plural = len(args) != 1
            sig = str(len(args))
        kwonly_sig = ''
        if kwonly_given:
            msg = ' positional argument%s (and %d keyword-only argument%s)'
            kwonly_sig = msg % ('s' if given != 1 else '', kwonly_given,
             's' if kwonly_given != 1 else '')
        raise TypeError('%s() takes %s positional argument%s but %d%s %s given' % (
         f_name, sig, 's' if plural else '', given, kwonly_sig,
         'was' if (given == 1) and not kwonly_given else 'were'))


    def getcallargs(func, *positional, **named):
        """Get the mapping of arguments to values.

    A dict is returned, with keys the function argument names (including the
    names of the * and ** arguments, if any), and values the respective bound
    values from 'positional' and 'named'."""
        spec = getfullargspec(func)
        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = spec
        f_name = func.__name__
        arg2value = {}
        if ismethod(func):
            if func.__self__ is not None:
                positional = (
                 func.__self__,) + positional
        num_pos = len(positional)
        num_args = len(args)
        num_defaults = len(defaults) if defaults else 0
        n = min(num_pos, num_args)
        for i in range(n):
            arg2value[args[i]] = positional[i]
        else:
            if varargs:
                arg2value[varargs] = tuple(positional[n:])
            possible_kwargs = set(args + kwonlyargs)
            if varkw:
                arg2value[varkw] = {}
            for kw, value in named.items():
                if kw not in possible_kwargs:
                    if not varkw:
                        raise TypeError('%s() got an unexpected keyword argument %r' % (
                         f_name, kw))
                    else:
                        arg2value[varkw][kw] = value
                else:
                    if kw in arg2value:
                        raise TypeError('%s() got multiple values for argument %r' % (
                         f_name, kw))
                    arg2value[kw] = value
            else:
                if num_pos > num_args:
                    if not varargs:
                        _too_many(f_name, args, kwonlyargs, varargs, num_defaults, num_pos, arg2value)
                    if num_pos < num_args:
                        req = args[:num_args - num_defaults]
                        for arg in req:
                            if arg not in arg2value:
                                _missing_argumentsf_namereqTruearg2value
                        else:
                            for i, arg in enumerate(args[num_args - num_defaults:]):
                                if arg not in arg2value:
                                    arg2value[arg] = defaults[i]

                    missing = 0
                    for kwarg in kwonlyargs:
                        if kwarg not in arg2value:
                            if kwonlydefaults and kwarg in kwonlydefaults:
                                arg2value[kwarg] = kwonlydefaults[kwarg]
                            else:
                                missing += 1
                    else:
                        if missing:
                            _missing_argumentsf_namekwonlyargsFalsearg2value

                    return arg2value


    ClosureVars = namedtuple('ClosureVars', 'nonlocals globals builtins unbound')

    def getclosurevars(func):
        """
    Get the mapping of free variables to their current values.

    Returns a named tuple of dicts mapping the current nonlocal, global
    and builtin references as seen by the body of the function. A final
    set of unbound names that could not be resolved is also provided.
    """
        if ismethod(func):
            func = func.__func__
        if not isfunction(func):
            raise TypeError('{!r} is not a Python function'.format(func))
        code = func.__code__
        if func.__closure__ is None:
            nonlocal_vars = {}
        else:
            nonlocal_vars = {cell.cell_contents:var for var, cell in zip(code.co_freevars, func.__closure__)}
        global_ns = func.__globals__
        builtin_ns = global_ns.get'__builtins__'builtins.__dict__
        if ismodule(builtin_ns):
            builtin_ns = builtin_ns.__dict__
        global_vars = {}
        builtin_vars = {}
        unbound_names = set()
        for name in code.co_names:
            if name in ('None', 'True', 'False'):
                pass
            else:
                try:
                    global_vars[name] = global_ns[name]
                except KeyError:
                    try:
                        builtin_vars[name] = builtin_ns[name]
                    except KeyError:
                        unbound_names.add(name)

        else:
            return ClosureVarsnonlocal_varsglobal_varsbuiltin_varsunbound_names


    Traceback = namedtuple('Traceback', 'filename lineno function code_context index')

    def getframeinfo(frame, context=1):
        """Get information about a frame or traceback object.

    A tuple of five things is returned: the filename, the line number of
    the current line, the function name, a list of lines of context from
    the source code, and the index of the current line within that list.
    The optional second argument specifies the number of lines of context
    to return, which are centered around the current line."""
        if istraceback(frame):
            lineno = frame.tb_lineno
            frame = frame.tb_frame
        else:
            lineno = frame.f_lineno
        if not isframe(frame):
            raise TypeError('{!r} is not a frame or traceback object'.format(frame))
        filename = getsourcefile(frame) or getfile(frame)
        if context > 0:
            start = lineno - 1 - context // 2
            try:
                lines, lnum = findsource(frame)
            except OSError:
                lines = index = None
            else:
                start = max(0, min(start, len(lines) - context))
                lines = lines[start:start + context]
                index = lineno - 1 - start
        else:
            lines = index = None
        return Traceback(filename, lineno, frame.f_code.co_name, lines, index)


    def getlineno(frame):
        """Get the line number from a frame object, allowing for optimization."""
        return frame.f_lineno


    FrameInfo = namedtuple('FrameInfo', ('frame', ) + Traceback._fields)

    def getouterframes(frame, context=1):
        """Get a list of records for a frame and all higher (calling) frames.

    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context."""
        framelist = []
        while True:
            if frame:
                frameinfo = (
                 frame,) + getframeinfo(frame, context)
                framelist.append(FrameInfo(*frameinfo))
                frame = frame.f_back

        return framelist


    def getinnerframes(tb, context=1):
        """Get a list of records for a traceback's frame and all lower frames.

    Each record contains a frame object, filename, line number, function
    name, a list of lines of context, and index within the context."""
        framelist = []
        while True:
            if tb:
                frameinfo = (
                 tb.tb_frame,) + getframeinfo(tb, context)
                framelist.append(FrameInfo(*frameinfo))
                tb = tb.tb_next

        return framelist


    def currentframe():
        """Return the frame of the caller or None if this is not possible."""
        if hasattr(sys, '_getframe'):
            return sys._getframe(1)


    def stack(context=1):
        """Return a list of records for the stack above the caller's frame."""
        return getouterframes(sys._getframe(1), context)


    def trace(context=1):
        """Return a list of records for the stack below the current exception."""
        return getinnerframes(sys.exc_info()[2], context)


    _sentinel = object()

    def _static_getmro(klass):
        return type.__dict__['__mro__'].__get__(klass)


    def _check_instance(obj, attr):
        instance_dict = {}
        try:
            instance_dict = object.__getattribute__obj'__dict__'
        except AttributeError:
            pass
        else:
            return dict.get(instance_dict, attr, _sentinel)


    def _check_class--- This code section failed: ---

 L.1538         0  LOAD_GLOBAL              _static_getmro
                2  LOAD_FAST                'klass'
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
              8_0  COME_FROM            66  '66'
              8_1  COME_FROM            62  '62'
              8_2  COME_FROM            26  '26'
                8  FOR_ITER             68  'to 68'
               10  STORE_FAST               'entry'

 L.1539        12  LOAD_GLOBAL              _shadowed_dict
               14  LOAD_GLOBAL              type
               16  LOAD_FAST                'entry'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_GLOBAL              _sentinel
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L.1540        28  SETUP_FINALLY        46  'to 46'

 L.1541        30  LOAD_FAST                'entry'
               32  LOAD_ATTR                __dict__
               34  LOAD_FAST                'attr'
               36  BINARY_SUBSCR    
               38  POP_BLOCK        
               40  ROT_TWO          
               42  POP_TOP          
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    28  '28'

 L.1542        46  DUP_TOP          
               48  LOAD_GLOBAL              KeyError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    64  'to 64'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.1543        60  POP_EXCEPT       
               62  JUMP_BACK             8  'to 8'
             64_0  COME_FROM            52  '52'
               64  END_FINALLY      
               66  JUMP_BACK             8  'to 8'
             68_0  COME_FROM             8  '8'

 L.1544        68  LOAD_GLOBAL              _sentinel
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 40


    def _is_type(obj):
        try:
            _static_getmro(obj)
        except TypeError:
            return False
        else:
            return True


    def _shadowed_dict(klass):
        dict_attr = type.__dict__['__dict__']
        for entry in _static_getmro(klass):
            try:
                class_dict = dict_attr.__get__(entry)['__dict__']
            except KeyError:
                pass
            else:
                if type(class_dict) is types.GetSetDescriptorType:
                    if not (class_dict.__name__ == '__dict__' and class_dict.__objclass__ is entry):
                        return class_dict
            return _sentinel


    def getattr_static--- This code section failed: ---

 L.1578         0  LOAD_GLOBAL              _sentinel
                2  STORE_FAST               'instance_result'

 L.1579         4  LOAD_GLOBAL              _is_type
                6  LOAD_FAST                'obj'
                8  CALL_FUNCTION_1       1  ''
               10  POP_JUMP_IF_TRUE     62  'to 62'

 L.1580        12  LOAD_GLOBAL              type
               14  LOAD_FAST                'obj'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'klass'

 L.1581        20  LOAD_GLOBAL              _shadowed_dict
               22  LOAD_FAST                'klass'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'dict_attr'

 L.1582        28  LOAD_FAST                'dict_attr'
               30  LOAD_GLOBAL              _sentinel
               32  COMPARE_OP               is
               34  POP_JUMP_IF_TRUE     50  'to 50'

 L.1583        36  LOAD_GLOBAL              type
               38  LOAD_FAST                'dict_attr'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_GLOBAL              types
               44  LOAD_ATTR                MemberDescriptorType
               46  COMPARE_OP               is

 L.1582        48  POP_JUMP_IF_FALSE    66  'to 66'
             50_0  COME_FROM            34  '34'

 L.1584        50  LOAD_GLOBAL              _check_instance
               52  LOAD_FAST                'obj'
               54  LOAD_FAST                'attr'
               56  CALL_FUNCTION_2       2  ''
               58  STORE_FAST               'instance_result'
               60  JUMP_FORWARD         66  'to 66'
             62_0  COME_FROM            10  '10'

 L.1586        62  LOAD_FAST                'obj'
               64  STORE_FAST               'klass'
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM            48  '48'

 L.1588        66  LOAD_GLOBAL              _check_class
               68  LOAD_FAST                'klass'
               70  LOAD_FAST                'attr'
               72  CALL_FUNCTION_2       2  ''
               74  STORE_FAST               'klass_result'

 L.1590        76  LOAD_FAST                'instance_result'
               78  LOAD_GLOBAL              _sentinel
               80  COMPARE_OP               is-not
               82  POP_JUMP_IF_FALSE   132  'to 132'
               84  LOAD_FAST                'klass_result'
               86  LOAD_GLOBAL              _sentinel
               88  COMPARE_OP               is-not
               90  POP_JUMP_IF_FALSE   132  'to 132'

 L.1591        92  LOAD_GLOBAL              _check_class
               94  LOAD_GLOBAL              type
               96  LOAD_FAST                'klass_result'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_STR                 '__get__'
              102  CALL_FUNCTION_2       2  ''
              104  LOAD_GLOBAL              _sentinel
              106  COMPARE_OP               is-not
              108  POP_JUMP_IF_FALSE   132  'to 132'

 L.1592       110  LOAD_GLOBAL              _check_class
              112  LOAD_GLOBAL              type
              114  LOAD_FAST                'klass_result'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_STR                 '__set__'
              120  CALL_FUNCTION_2       2  ''
              122  LOAD_GLOBAL              _sentinel
              124  COMPARE_OP               is-not

 L.1591       126  POP_JUMP_IF_FALSE   132  'to 132'

 L.1593       128  LOAD_FAST                'klass_result'
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'
            132_1  COME_FROM           108  '108'
            132_2  COME_FROM            90  '90'
            132_3  COME_FROM            82  '82'

 L.1595       132  LOAD_FAST                'instance_result'
              134  LOAD_GLOBAL              _sentinel
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L.1596       140  LOAD_FAST                'instance_result'
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'

 L.1597       144  LOAD_FAST                'klass_result'
              146  LOAD_GLOBAL              _sentinel
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L.1598       152  LOAD_FAST                'klass_result'
              154  RETURN_VALUE     
            156_0  COME_FROM           150  '150'

 L.1600       156  LOAD_FAST                'obj'
              158  LOAD_FAST                'klass'
              160  COMPARE_OP               is
              162  POP_JUMP_IF_FALSE   236  'to 236'

 L.1602       164  LOAD_GLOBAL              _static_getmro
              166  LOAD_GLOBAL              type
              168  LOAD_FAST                'klass'
              170  CALL_FUNCTION_1       1  ''
              172  CALL_FUNCTION_1       1  ''
              174  GET_ITER         
            176_0  COME_FROM           234  '234'
            176_1  COME_FROM           230  '230'
            176_2  COME_FROM           194  '194'
              176  FOR_ITER            236  'to 236'
              178  STORE_FAST               'entry'

 L.1603       180  LOAD_GLOBAL              _shadowed_dict
              182  LOAD_GLOBAL              type
              184  LOAD_FAST                'entry'
              186  CALL_FUNCTION_1       1  ''
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_GLOBAL              _sentinel
              192  COMPARE_OP               is
              194  POP_JUMP_IF_FALSE_BACK   176  'to 176'

 L.1604       196  SETUP_FINALLY       214  'to 214'

 L.1605       198  LOAD_FAST                'entry'
              200  LOAD_ATTR                __dict__
              202  LOAD_FAST                'attr'
              204  BINARY_SUBSCR    
              206  POP_BLOCK        
              208  ROT_TWO          
              210  POP_TOP          
              212  RETURN_VALUE     
            214_0  COME_FROM_FINALLY   196  '196'

 L.1606       214  DUP_TOP          
              216  LOAD_GLOBAL              KeyError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   232  'to 232'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L.1607       228  POP_EXCEPT       
              230  JUMP_BACK           176  'to 176'
            232_0  COME_FROM           220  '220'
              232  END_FINALLY      
              234  JUMP_BACK           176  'to 176'
            236_0  COME_FROM           176  '176'
            236_1  COME_FROM           162  '162'

 L.1608       236  LOAD_FAST                'default'
              238  LOAD_GLOBAL              _sentinel
              240  COMPARE_OP               is-not
              242  POP_JUMP_IF_FALSE   248  'to 248'

 L.1609       244  LOAD_FAST                'default'
              246  RETURN_VALUE     
            248_0  COME_FROM           242  '242'

 L.1610       248  LOAD_GLOBAL              AttributeError
              250  LOAD_FAST                'attr'
              252  CALL_FUNCTION_1       1  ''
              254  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 208


    GEN_CREATED = 'GEN_CREATED'
    GEN_RUNNING = 'GEN_RUNNING'
    GEN_SUSPENDED = 'GEN_SUSPENDED'
    GEN_CLOSED = 'GEN_CLOSED'

    def getgeneratorstate(generator):
        """Get current state of a generator-iterator.

    Possible states are:
      GEN_CREATED: Waiting to start execution.
      GEN_RUNNING: Currently being executed by the interpreter.
      GEN_SUSPENDED: Currently suspended at a yield expression.
      GEN_CLOSED: Execution has completed.
    """
        if generator.gi_running:
            return GEN_RUNNING
        if generator.gi_frame is None:
            return GEN_CLOSED
        if generator.gi_frame.f_lasti == -1:
            return GEN_CREATED
        return GEN_SUSPENDED


    def getgeneratorlocals(generator):
        """
    Get the mapping of generator local variables to their current values.

    A dict is returned, with the keys the local variable names and values the
    bound values."""
        if not isgenerator(generator):
            raise TypeError('{!r} is not a Python generator'.format(generator))
        frame = getattr(generator, 'gi_frame', None)
        if frame is not None:
            return generator.gi_frame.f_locals
        return {}


    CORO_CREATED = 'CORO_CREATED'
    CORO_RUNNING = 'CORO_RUNNING'
    CORO_SUSPENDED = 'CORO_SUSPENDED'
    CORO_CLOSED = 'CORO_CLOSED'

    def getcoroutinestate(coroutine):
        """Get current state of a coroutine object.

    Possible states are:
      CORO_CREATED: Waiting to start execution.
      CORO_RUNNING: Currently being executed by the interpreter.
      CORO_SUSPENDED: Currently suspended at an await expression.
      CORO_CLOSED: Execution has completed.
    """
        if coroutine.cr_running:
            return CORO_RUNNING
        if coroutine.cr_frame is None:
            return CORO_CLOSED
        if coroutine.cr_frame.f_lasti == -1:
            return CORO_CREATED
        return CORO_SUSPENDED


    def getcoroutinelocals(coroutine):
        """
    Get the mapping of coroutine local variables to their current values.

    A dict is returned, with the keys the local variable names and values the
    bound values."""
        frame = getattr(coroutine, 'cr_frame', None)
        if frame is not None:
            return frame.f_locals
        return {}


    _WrapperDescriptor = type(type.__call__)
    _MethodWrapper = type(all.__call__)
    _ClassMethodWrapper = type(int.__dict__['from_bytes'])
    _NonUserDefinedCallables = (
     _WrapperDescriptor,
     _MethodWrapper,
     _ClassMethodWrapper,
     types.BuiltinFunctionType)

    def _signature_get_user_defined_method(cls, method_name):
        """Private helper. Checks if ``cls`` has an attribute
    named ``method_name`` and returns it only if it is a
    pure python function.
    """
        try:
            meth = getattr(cls, method_name)
        except AttributeError:
            return
        else:
            if not isinstance(meth, _NonUserDefinedCallables):
                return meth


    def _signature_get_partial(wrapped_sig, partial, extra_args=()):
        """Private helper to calculate how 'wrapped_sig' signature will
    look like after applying a 'functools.partial' object (or alike)
    on it.
    """
        old_params = wrapped_sig.parameters
        new_params = OrderedDict(old_params.items())
        partial_args = partial.args or ()
        partial_keywords = partial.keywords or {}
        if extra_args:
            partial_args = extra_args + partial_args
        try:
            ba = (wrapped_sig.bind_partial)(*partial_args, **partial_keywords)
        except TypeError as ex:
            try:
                msg = 'partial object {!r} has incorrect arguments'.format(partial)
                raise ValueError(msg) from ex
            finally:
                ex = None
                del ex

        else:
            transform_to_kwonly = False
            for param_name, param in old_params.items():
                try:
                    arg_value = ba.arguments[param_name]
                except KeyError:
                    pass
                else:
                    if param.kind is _POSITIONAL_ONLY:
                        new_params.pop(param_name)
                    else:
                        if param.kind is _POSITIONAL_OR_KEYWORD:
                            if param_name in partial_keywords:
                                transform_to_kwonly = True
                                new_params[param_name] = param.replace(default=arg_value)
                            else:
                                new_params.pop(param.name)
                        if param.kind is _KEYWORD_ONLY:
                            new_params[param_name] = param.replace(default=arg_value)
                if transform_to_kwonly:
                    assert param.kind is not _POSITIONAL_ONLY
                    if param.kind is _POSITIONAL_OR_KEYWORD:
                        new_param = new_params[param_name].replace(kind=_KEYWORD_ONLY)
                        new_params[param_name] = new_param
                        new_params.move_to_end(param_name)
                    else:
                        if param.kind in (_KEYWORD_ONLY, _VAR_KEYWORD):
                            new_params.move_to_end(param_name)
                        else:
                            if param.kind is _VAR_POSITIONAL:
                                new_params.pop(param.name)
            else:
                return wrapped_sig.replace(parameters=(new_params.values()))


    def _signature_bound_method(sig):
        """Private helper to transform signatures for unbound
    functions to bound methods.
    """
        params = tuple(sig.parameters.values())
        if not params or params[0].kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
            raise ValueError('invalid method signature')
        kind = params[0].kind
        if kind in (_POSITIONAL_OR_KEYWORD, _POSITIONAL_ONLY):
            params = params[1:]
        elif kind is not _VAR_POSITIONAL:
            raise ValueError('invalid argument type')
        return sig.replace(parameters=params)


    def _signature_is_builtin(obj):
        """Private helper to test if `obj` is a callable that might
    support Argument Clinic's __text_signature__ protocol.
    """
        return isbuiltin(obj) or ismethoddescriptor(obj) or isinstance(obj, _NonUserDefinedCallables) or obj in (type, object)


    def _signature_is_functionlike(obj):
        """Private helper to test if `obj` is a duck type of FunctionType.
    A good example of such objects are functions compiled with
    Cython, which have all attributes that a pure Python function
    would have, but have their code statically compiled.
    """
        if not callable(obj) or isclass(obj):
            return False
        name = getattr(obj, '__name__', None)
        code = getattr(obj, '__code__', None)
        defaults = getattr(obj, '__defaults__', _void)
        kwdefaults = getattr(obj, '__kwdefaults__', _void)
        annotations = getattr(obj, '__annotations__', None)
        if isinstance(code, types.CodeType) and isinstance(name, str) and defaults is None or isinstance(defaults, tuple) and not kwdefaults is None:
            return isinstance(kwdefaults, dict) and isinstance(annotations, dict)


    def _signature_get_bound_param(spec):
        """ Private helper to get first parameter name from a
    __text_signature__ of a builtin method, which should
    be in the following format: '($param1, ...)'.
    Assumptions are that the first argument won't have
    a default value or an annotation.
    """
        assert spec.startswith('($')
        pos = spec.find(',')
        if pos == -1:
            pos = spec.find(')')
        cpos = spec.find(':')
        if not cpos == -1:
            assert cpos > pos
            cpos = spec.find('=')
            if not cpos == -1:
                assert cpos > pos
            return spec[2:pos]


    def _signature_strip_non_python_syntax(signature):
        """
    Private helper function. Takes a signature in Argument Clinic's
    extended signature format.

    Returns a tuple of three things:
      * that signature re-rendered in standard Python syntax,
      * the index of the "self" parameter (generally 0), or None if
        the function does not have a "self" parameter, and
      * the index of the last "positional only" parameter,
        or None if the signature has no positional-only parameters.
    """
        if not signature:
            return (signature, None, None)
        self_parameter = None
        last_positional_only = None
        lines = [l.encode('ascii') for l in signature.split('\n')]
        generator = iter(lines).__next__
        token_stream = tokenize.tokenize(generator)
        delayed_comma = False
        skip_next_comma = False
        text = []
        add = text.append
        current_parameter = 0
        OP = token.OP
        ERRORTOKEN = token.ERRORTOKEN
        t = next(token_stream)
        assert t.type == tokenize.ENCODING
        for t in token_stream:
            type, string = t.type, t.string
            if type == OP:
                if string == ',':
                    if skip_next_comma:
                        skip_next_comma = False
                    else:
                        assert not delayed_comma
                        delayed_comma = True
                        current_parameter += 1
                elif string == '/':
                    assert not skip_next_comma
                    assert last_positional_only is None
                    skip_next_comma = True
                    last_positional_only = current_parameter - 1
                if type == ERRORTOKEN:
                    if string == '$':
                        if not self_parameter is None:
                            raise AssertionError
                        else:
                            self_parameter = current_parameter
            if delayed_comma:
                delayed_comma = False
                if type == OP:
                    if not string == ')':
                        add(', ')
                    add(string)
                    if string == ',':
                        add(' ')
        else:
            clean_signature = ''.join(text)
            return (
             clean_signature, self_parameter, last_positional_only)


    def _signature_fromstr(cls, obj, s, skip_bound_arg=True):
        """Private helper to parse content of '__text_signature__'
    and return a Signature based on it.
    """
        import ast
        Parameter = cls._parameter_cls
        clean_signature, self_parameter, last_positional_only = _signature_strip_non_python_syntax(s)
        program = 'def foo' + clean_signature + ': pass'
        try:
            module = ast.parse(program)
        except SyntaxError:
            module = None
        else:
            if not isinstance(module, ast.Module):
                raise ValueError('{!r} builtin has invalid signature'.format(obj))
            else:
                f = module.body[0]
                parameters = []
                empty = Parameter.empty
                invalid = object()
                module = None
                module_dict = {}
                module_name = getattr(obj, '__module__', None)
                if module_name:
                    module = sys.modules.getmodule_nameNone
                    if module:
                        module_dict = module.__dict__
                sys_module_dict = sys.modules.copy()

                def parse_name(node):
                    assert isinstance(node, ast.arg)
                    if node.annotation is not None:
                        raise ValueError('Annotations are not currently supported')
                    return node.arg

                def wrap_value(s):
                    try:
                        value = eval(s, module_dict)
                    except NameError:
                        try:
                            value = eval(s, sys_module_dict)
                        except NameError:
                            raise RuntimeError()

                    else:
                        if isinstance(value, (str, int, float, bytes, bool, type(None))):
                            return ast.Constant(value)
                        raise RuntimeError()

                class RewriteSymbolics(ast.NodeTransformer):

                    def visit_Attribute(self, node):
                        a = []
                        n = node
                        while True:
                            if isinstance(n, ast.Attribute):
                                a.append(n.attr)
                                n = n.value

                        if not isinstance(n, ast.Name):
                            raise RuntimeError()
                        a.append(n.id)
                        value = '.'.join(reversed(a))
                        return wrap_value(value)

                    def visit_Name(self, node):
                        if not isinstance(node.ctx, ast.Load):
                            raise ValueError()
                        return wrap_value(node.id)

                def p(name_node, default_node, default=empty):
                    name = parse_name(name_node)
                    if name is invalid:
                        return
                    if not default_node or default_node is not _empty:
                        try:
                            default_node = RewriteSymbolics().visit(default_node)
                            o = ast.literal_eval(default_node)
                        except ValueError:
                            o = invalid
                        else:
                            if o is invalid:
                                return
                            default = o if o is not invalid else default
                        parameters.append(Parameter(name, kind, default=default, annotation=empty))

                args = reversed(f.args.args)
                defaults = reversed(f.args.defaults)
                iter = itertools.zip_longest(args, defaults, fillvalue=None)
                if last_positional_only is not None:
                    kind = Parameter.POSITIONAL_ONLY
                else:
                    kind = Parameter.POSITIONAL_OR_KEYWORD
                for i, (name, default) in enumerate(reversed(list(iter))):
                    p(name, default)
                    if i == last_positional_only:
                        kind = Parameter.POSITIONAL_OR_KEYWORD
                else:
                    if f.args.vararg:
                        kind = Parameter.VAR_POSITIONAL
                        p(f.args.vararg, empty)
                    kind = Parameter.KEYWORD_ONLY
                    for name, default in zip(f.args.kwonlyargs, f.args.kw_defaults):
                        p(name, default)
                    else:
                        if f.args.kwarg:
                            kind = Parameter.VAR_KEYWORD
                            p(f.args.kwarg, empty)
                        if self_parameter is not None:
                            assert parameters
                            _self = getattr(obj, '__self__', None)
                            self_isbound = _self is not None
                            self_ismodule = ismodule(_self)
                            if not self_isbound or self_ismodule or skip_bound_arg:
                                parameters.pop(0)
                            else:
                                p = parameters[0].replace(kind=(Parameter.POSITIONAL_ONLY))
                                parameters[0] = p
                        return cls(parameters, return_annotation=(cls.empty))


    def _signature_from_builtin(cls, func, skip_bound_arg=True):
        """Private helper function to get signature for
    builtin callables.
    """
        if not _signature_is_builtin(func):
            raise TypeError('{!r} is not a Python builtin function'.format(func))
        s = getattr(func, '__text_signature__', None)
        if not s:
            raise ValueError('no signature found for builtin {!r}'.format(func))
        return _signature_fromstrclsfuncsskip_bound_arg


    def _signature_from_function(cls, func, skip_bound_arg=True):
        """Private helper: constructs Signature for the given python function."""
        is_duck_function = False
        if not isfunction(func):
            if _signature_is_functionlike(func):
                is_duck_function = True
            else:
                raise TypeError('{!r} is not a Python function'.format(func))
        s = getattr(func, '__text_signature__', None)
        if s:
            return _signature_fromstrclsfuncsskip_bound_arg
        Parameter = cls._parameter_cls
        func_code = func.__code__
        pos_count = func_code.co_argcount
        arg_names = func_code.co_varnames
        posonly_count = func_code.co_posonlyargcount
        positional = arg_names[:pos_count]
        keyword_only_count = func_code.co_kwonlyargcount
        keyword_only = arg_names[pos_count:pos_count + keyword_only_count]
        annotations = func.__annotations__
        defaults = func.__defaults__
        kwdefaults = func.__kwdefaults__
        if defaults:
            pos_default_count = len(defaults)
        else:
            pos_default_count = 0
        parameters = []
        non_default_count = pos_count - pos_default_count
        posonly_left = posonly_count
        for name in positional[:non_default_count]:
            kind = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
            annotation = annotations.getname_empty
            parameters.append(Parameter(name, annotation=annotation, kind=kind))
            if posonly_left:
                posonly_left -= 1
        else:
            for offset, name in enumerate(positional[non_default_count:]):
                kind = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
                annotation = annotations.getname_empty
                parameters.append(Parameter(name, annotation=annotation, kind=kind,
                  default=(defaults[offset])))
                if posonly_left:
                    posonly_left -= 1
            else:
                if func_code.co_flags & CO_VARARGS:
                    name = arg_names[(pos_count + keyword_only_count)]
                    annotation = annotations.getname_empty
                    parameters.append(Parameter(name, annotation=annotation, kind=_VAR_POSITIONAL))
                for name in keyword_only:
                    default = _empty
                    if kwdefaults is not None:
                        default = kwdefaults.getname_empty
                    else:
                        annotation = annotations.getname_empty
                        parameters.append(Parameter(name, annotation=annotation, kind=_KEYWORD_ONLY,
                          default=default))
                else:
                    if func_code.co_flags & CO_VARKEYWORDS:
                        index = pos_count + keyword_only_count
                        if func_code.co_flags & CO_VARARGS:
                            index += 1
                        name = arg_names[index]
                        annotation = annotations.getname_empty
                        parameters.append(Parameter(name, annotation=annotation, kind=_VAR_KEYWORD))
                    return cls(parameters, return_annotation=(annotations.get'return'_empty),
                      __validate_parameters__=is_duck_function)


    def _signature_from_callable(obj, *, follow_wrapper_chains=True, skip_bound_arg=True, sigcls):
        """Private helper function to get signature for arbitrary
    callable objects.
    """
        if not callable(obj):
            raise TypeError('{!r} is not a callable object'.format(obj))
        if isinstance(obj, types.MethodType):
            sig = _signature_from_callable((obj.__func__),
              follow_wrapper_chains=follow_wrapper_chains,
              skip_bound_arg=skip_bound_arg,
              sigcls=sigcls)
            if skip_bound_arg:
                return _signature_bound_method(sig)
            return sig
        if follow_wrapper_chains:
            obj = unwrap(obj, stop=(lambda f: hasattr(f, '__signature__')))
            if isinstance(obj, types.MethodType):
                return _signature_from_callable(obj,
                  follow_wrapper_chains=follow_wrapper_chains,
                  skip_bound_arg=skip_bound_arg,
                  sigcls=sigcls)
        try:
            sig = obj.__signature__
        except AttributeError:
            pass
        else:
            if sig is not None:
                if not isinstance(sig, Signature):
                    raise TypeError('unexpected object {!r} in __signature__ attribute'.format(sig))
                return sig
        try:
            partialmethod = obj._partialmethod
        except AttributeError:
            pass
        else:
            if isinstance(partialmethod, functools.partialmethod):
                wrapped_sig = _signature_from_callable((partialmethod.func),
                  follow_wrapper_chains=follow_wrapper_chains,
                  skip_bound_arg=skip_bound_arg,
                  sigcls=sigcls)
                sig = _signature_get_partial(wrapped_sig, partialmethod, (None, ))
                first_wrapped_param = tuple(wrapped_sig.parameters.values())[0]
                if first_wrapped_param.kind is Parameter.VAR_POSITIONAL:
                    return sig
                sig_params = tuple(sig.parameters.values())
                if sig_params:
                    assert first_wrapped_param is not sig_params[0]
                    new_params = (
                     first_wrapped_param,) + sig_params
                    return sig.replace(parameters=new_params)
        if isfunction(obj) or (_signature_is_functionlike(obj)):
            return _signature_from_function(sigcls, obj, skip_bound_arg=skip_bound_arg)
        if _signature_is_builtin(obj):
            return _signature_from_builtin(sigcls, obj, skip_bound_arg=skip_bound_arg)
        if isinstance(obj, functools.partial):
            wrapped_sig = _signature_from_callable((obj.func),
              follow_wrapper_chains=follow_wrapper_chains,
              skip_bound_arg=skip_bound_arg,
              sigcls=sigcls)
            return _signature_get_partial(wrapped_sig, obj)
        sig = None
        if isinstance(obj, type):
            call = _signature_get_user_defined_method(type(obj), '__call__')
            if call is not None:
                sig = _signature_from_callable(call,
                  follow_wrapper_chains=follow_wrapper_chains,
                  skip_bound_arg=skip_bound_arg,
                  sigcls=sigcls)
            else:
                new = _signature_get_user_defined_method(obj, '__new__')
                if new is not None:
                    sig = _signature_from_callable(new,
                      follow_wrapper_chains=follow_wrapper_chains,
                      skip_bound_arg=skip_bound_arg,
                      sigcls=sigcls)
                else:
                    init = _signature_get_user_defined_method(obj, '__init__')
                    if init is not None:
                        sig = _signature_from_callable(init,
                          follow_wrapper_chains=follow_wrapper_chains,
                          skip_bound_arg=skip_bound_arg,
                          sigcls=sigcls)
            if sig is None:
                for base in obj.__mro__[:-1]:
                    try:
                        text_sig = base.__text_signature__
                    except AttributeError:
                        pass
                    else:
                        if text_sig:
                            return _signature_fromstr(sigcls, obj, text_sig)
                else:
                    if type not in obj.__mro__:
                        if obj.__init__ is object.__init__:
                            if obj.__new__ is object.__new__:
                                return sigcls.from_callable(object)
                        raise ValueError('no signature found for builtin type {!r}'.format(obj))

        else:
            call = (isinstance(obj, _NonUserDefinedCallables) or _signature_get_user_defined_method)(type(obj), '__call__')
        if call is not None:
            try:
                sig = _signature_from_callable(call,
                  follow_wrapper_chains=follow_wrapper_chains,
                  skip_bound_arg=skip_bound_arg,
                  sigcls=sigcls)
            except ValueError as ex:
                try:
                    msg = 'no signature found for {!r}'.format(obj)
                    raise ValueError(msg) from ex
                finally:
                    ex = None
                    del ex

            else:
                if sig is not None:
                    if skip_bound_arg:
                        return _signature_bound_method(sig)
                    return sig
                if isinstance(obj, types.BuiltinFunctionType):
                    msg = 'no signature found for builtin function {!r}'.format(obj)
                    raise ValueError(msg)
        raise ValueError('callable {!r} is not supported by signature'.format(obj))


    class _void:
        __doc__ = 'A private marker - used in Parameter & Signature.'


    class _empty:
        __doc__ = 'Marker object for Signature.empty and Parameter.empty.'


    class _ParameterKind(enum.IntEnum):
        POSITIONAL_ONLY = 0
        POSITIONAL_OR_KEYWORD = 1
        VAR_POSITIONAL = 2
        KEYWORD_ONLY = 3
        VAR_KEYWORD = 4

        def __str__(self):
            return self._name_

        @property
        def description(self):
            return _PARAM_NAME_MAPPING[self]


    _POSITIONAL_ONLY = _ParameterKind.POSITIONAL_ONLY
    _POSITIONAL_OR_KEYWORD = _ParameterKind.POSITIONAL_OR_KEYWORD
    _VAR_POSITIONAL = _ParameterKind.VAR_POSITIONAL
    _KEYWORD_ONLY = _ParameterKind.KEYWORD_ONLY
    _VAR_KEYWORD = _ParameterKind.VAR_KEYWORD
    _PARAM_NAME_MAPPING = {_POSITIONAL_ONLY: 'positional-only', 
     _POSITIONAL_OR_KEYWORD: 'positional or keyword', 
     _VAR_POSITIONAL: 'variadic positional', 
     _KEYWORD_ONLY: 'keyword-only', 
     _VAR_KEYWORD: 'variadic keyword'}

    class Parameter:
        __doc__ = 'Represents a parameter in a function signature.\n\n    Has the following public attributes:\n\n    * name : str\n        The name of the parameter as a string.\n    * default : object\n        The default value for the parameter if specified.  If the\n        parameter has no default value, this attribute is set to\n        `Parameter.empty`.\n    * annotation\n        The annotation for the parameter if specified.  If the\n        parameter has no annotation, this attribute is set to\n        `Parameter.empty`.\n    * kind : str\n        Describes how argument values are bound to the parameter.\n        Possible values: `Parameter.POSITIONAL_ONLY`,\n        `Parameter.POSITIONAL_OR_KEYWORD`, `Parameter.VAR_POSITIONAL`,\n        `Parameter.KEYWORD_ONLY`, `Parameter.VAR_KEYWORD`.\n    '
        __slots__ = ('_name', '_kind', '_default', '_annotation')
        POSITIONAL_ONLY = _POSITIONAL_ONLY
        POSITIONAL_OR_KEYWORD = _POSITIONAL_OR_KEYWORD
        VAR_POSITIONAL = _VAR_POSITIONAL
        KEYWORD_ONLY = _KEYWORD_ONLY
        VAR_KEYWORD = _VAR_KEYWORD
        empty = _empty

        def __init__(self, name, kind, *, default=_empty, annotation=_empty):
            try:
                self._kind = _ParameterKind(kind)
            except ValueError:
                raise ValueError(f"value {kind!r} is not a valid Parameter.kind")
            else:
                if default is not _empty:
                    if self._kind in (_VAR_POSITIONAL, _VAR_KEYWORD):
                        msg = '{} parameters cannot have default values'
                        msg = msg.format(self._kind.description)
                        raise ValueError(msg)
                self._default = default
                self._annotation = annotation
                if name is _empty:
                    raise ValueError('name is a required attribute for Parameter')
                if not isinstance(name, str):
                    msg = 'name must be a str, not a {}'.format(type(name).__name__)
                    raise TypeError(msg)
                if name[0] == '.':
                    if name[1:].isdigit():
                        if self._kind != _POSITIONAL_OR_KEYWORD:
                            msg = 'implicit arguments must be passed as positional or keyword arguments, not {}'
                            msg = msg.format(self._kind.description)
                            raise ValueError(msg)
                        self._kind = _POSITIONAL_ONLY
                        name = 'implicit{}'.format(name[1:])
                if not name.isidentifier():
                    raise ValueError('{!r} is not a valid parameter name'.format(name))
                self._name = name

        def __reduce__(self):
            return (
             type(self),
             (
              self._name, self._kind),
             {'_default':self._default, 
              '_annotation':self._annotation})

        def __setstate__(self, state):
            self._default = state['_default']
            self._annotation = state['_annotation']

        @property
        def name(self):
            return self._name

        @property
        def default(self):
            return self._default

        @property
        def annotation(self):
            return self._annotation

        @property
        def kind(self):
            return self._kind

        def replace(self, *, name=_void, kind=_void, annotation=_void, default=_void):
            """Creates a customized copy of the Parameter."""
            if name is _void:
                name = self._name
            if kind is _void:
                kind = self._kind
            if annotation is _void:
                annotation = self._annotation
            if default is _void:
                default = self._default
            return type(self)(name, kind, default=default, annotation=annotation)

        def __str__(self):
            kind = self.kind
            formatted = self._name
            if self._annotation is not _empty:
                formatted = '{}: {}'.formatformattedformatannotation(self._annotation)
            if self._default is not _empty:
                if self._annotation is not _empty:
                    formatted = '{} = {}'.formatformattedrepr(self._default)
                else:
                    formatted = '{}={}'.formatformattedrepr(self._default)
            if kind == _VAR_POSITIONAL:
                formatted = '*' + formatted
            elif kind == _VAR_KEYWORD:
                formatted = '**' + formatted
            return formatted

        def __repr__(self):
            return '<{} "{}">'.formatself.__class__.__name__self

        def __hash__(self):
            return hash((self.name, self.kind, self.annotation, self.default))

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, Parameter):
                return NotImplemented
            return self._name == other._name and self._kind == other._kind and self._default == other._default and self._annotation == other._annotation


    class BoundArguments:
        __doc__ = "Result of `Signature.bind` call.  Holds the mapping of arguments\n    to the function's parameters.\n\n    Has the following public attributes:\n\n    * arguments : OrderedDict\n        An ordered mutable mapping of parameters' names to arguments' values.\n        Does not contain arguments' default values.\n    * signature : Signature\n        The Signature object that created this instance.\n    * args : tuple\n        Tuple of positional arguments values.\n    * kwargs : dict\n        Dict of keyword arguments values.\n    "
        __slots__ = ('arguments', '_signature', '__weakref__')

        def __init__(self, signature, arguments):
            self.arguments = arguments
            self._signature = signature

        @property
        def signature(self):
            return self._signature

        @property
        def args--- This code section failed: ---

 L.2629         0  BUILD_LIST_0          0 
                2  STORE_FAST               'args'

 L.2630         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _signature
                8  LOAD_ATTR                parameters
               10  LOAD_METHOD              items
               12  CALL_METHOD_0         0  ''
               14  GET_ITER         
             16_0  COME_FROM           116  '116'
             16_1  COME_FROM           104  '104'
             16_2  COME_FROM            80  '80'
               16  FOR_ITER            118  'to 118'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'param_name'
               22  STORE_FAST               'param'

 L.2631        24  LOAD_FAST                'param'
               26  LOAD_ATTR                kind
               28  LOAD_GLOBAL              _VAR_KEYWORD
               30  LOAD_GLOBAL              _KEYWORD_ONLY
               32  BUILD_TUPLE_2         2 
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    42  'to 42'

 L.2632        38  POP_TOP          
               40  BREAK_LOOP          118  'to 118'
             42_0  COME_FROM            36  '36'

 L.2634        42  SETUP_FINALLY        58  'to 58'

 L.2635        44  LOAD_FAST                'self'
               46  LOAD_ATTR                arguments
               48  LOAD_FAST                'param_name'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'arg'
               54  POP_BLOCK        
               56  JUMP_FORWARD         84  'to 84'
             58_0  COME_FROM_FINALLY    42  '42'

 L.2636        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    82  'to 82'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.2639        72  POP_EXCEPT       
               74  POP_TOP          
               76  JUMP_FORWARD        118  'to 118'
               78  POP_EXCEPT       
               80  JUMP_BACK            16  'to 16'
             82_0  COME_FROM            64  '64'
               82  END_FINALLY      
             84_0  COME_FROM            56  '56'

 L.2641        84  LOAD_FAST                'param'
               86  LOAD_ATTR                kind
               88  LOAD_GLOBAL              _VAR_POSITIONAL
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L.2643        94  LOAD_FAST                'args'
               96  LOAD_METHOD              extend
               98  LOAD_FAST                'arg'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_BACK            16  'to 16'
            106_0  COME_FROM            92  '92'

 L.2646       106  LOAD_FAST                'args'
              108  LOAD_METHOD              append
              110  LOAD_FAST                'arg'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  JUMP_BACK            16  'to 16'
            118_0  COME_FROM            76  '76'
            118_1  COME_FROM            40  '40'
            118_2  COME_FROM            16  '16'

 L.2648       118  LOAD_GLOBAL              tuple
              120  LOAD_FAST                'args'
              122  CALL_FUNCTION_1       1  ''
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 76

        @property
        def kwargs(self):
            kwargs = {}
            kwargs_started = False
            for param_name, param in self._signature.parameters.items():
                if not kwargs_started:
                    if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                        kwargs_started = True
                    else:
                        if param_name not in self.arguments:
                            kwargs_started = True
                if not kwargs_started:
                    pass
                else:
                    try:
                        arg = self.arguments[param_name]
                    except KeyError:
                        pass
                    else:
                        if param.kind == _VAR_KEYWORD:
                            kwargs.update(arg)
                        else:
                            kwargs[param_name] = arg
                        return kwargs

        def apply_defaults--- This code section failed: ---

 L.2689         0  LOAD_FAST                'self'
                2  LOAD_ATTR                arguments
                4  STORE_FAST               'arguments'

 L.2690         6  BUILD_LIST_0          0 
                8  STORE_FAST               'new_arguments'

 L.2691        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _signature
               14  LOAD_ATTR                parameters
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''
               20  GET_ITER         
             22_0  COME_FROM           142  '142'
             22_1  COME_FROM           138  '138'
             22_2  COME_FROM           120  '120'
             22_3  COME_FROM            52  '52'
               22  FOR_ITER            144  'to 144'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'name'
               28  STORE_FAST               'param'

 L.2692        30  SETUP_FINALLY        54  'to 54'

 L.2693        32  LOAD_FAST                'new_arguments'
               34  LOAD_METHOD              append
               36  LOAD_FAST                'name'
               38  LOAD_FAST                'arguments'
               40  LOAD_FAST                'name'
               42  BINARY_SUBSCR    
               44  BUILD_TUPLE_2         2 
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  POP_BLOCK        
               52  JUMP_BACK            22  'to 22'
             54_0  COME_FROM_FINALLY    30  '30'

 L.2694        54  DUP_TOP          
               56  LOAD_GLOBAL              KeyError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   140  'to 140'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.2695        68  LOAD_FAST                'param'
               70  LOAD_ATTR                default
               72  LOAD_GLOBAL              _empty
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.2696        78  LOAD_FAST                'param'
               80  LOAD_ATTR                default
               82  STORE_FAST               'val'
               84  JUMP_FORWARD        122  'to 122'
             86_0  COME_FROM            76  '76'

 L.2697        86  LOAD_FAST                'param'
               88  LOAD_ATTR                kind
               90  LOAD_GLOBAL              _VAR_POSITIONAL
               92  COMPARE_OP               is
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L.2698        96  LOAD_CONST               ()
               98  STORE_FAST               'val'
              100  JUMP_FORWARD        122  'to 122'
            102_0  COME_FROM            94  '94'

 L.2699       102  LOAD_FAST                'param'
              104  LOAD_ATTR                kind
              106  LOAD_GLOBAL              _VAR_KEYWORD
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L.2700       112  BUILD_MAP_0           0 
              114  STORE_FAST               'val'
              116  JUMP_FORWARD        122  'to 122'
            118_0  COME_FROM           110  '110'

 L.2704       118  POP_EXCEPT       
              120  JUMP_BACK            22  'to 22'
            122_0  COME_FROM           116  '116'
            122_1  COME_FROM           100  '100'
            122_2  COME_FROM            84  '84'

 L.2705       122  LOAD_FAST                'new_arguments'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'name'
              128  LOAD_FAST                'val'
              130  BUILD_TUPLE_2         2 
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  POP_EXCEPT       
              138  JUMP_BACK            22  'to 22'
            140_0  COME_FROM            60  '60'
              140  END_FINALLY      
              142  JUMP_BACK            22  'to 22'
            144_0  COME_FROM            22  '22'

 L.2706       144  LOAD_GLOBAL              OrderedDict
              146  LOAD_FAST                'new_arguments'
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_FAST                'self'
              152  STORE_ATTR               arguments

Parse error at or near `JUMP_BACK' instruction at offset 138

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, BoundArguments):
                return NotImplemented
            return self.signature == other.signature and self.arguments == other.arguments

        def __setstate__(self, state):
            self._signature = state['_signature']
            self.arguments = state['arguments']

        def __getstate__(self):
            return {'_signature':self._signature, 
             'arguments':self.arguments}

        def __repr__(self):
            args = []
            for arg, value in self.arguments.items():
                args.append('{}={!r}'.formatargvalue)
            else:
                return '<{} ({})>'.formatself.__class__.__name__', '.join(args)


    class Signature:
        __doc__ = "A Signature object represents the overall signature of a function.\n    It stores a Parameter object for each parameter accepted by the\n    function, as well as information specific to the function itself.\n\n    A Signature object has the following public attributes and methods:\n\n    * parameters : OrderedDict\n        An ordered mapping of parameters' names to the corresponding\n        Parameter objects (keyword-only arguments are in the same order\n        as listed in `code.co_varnames`).\n    * return_annotation : object\n        The annotation for the return type of the function if specified.\n        If the function has no annotation for its return type, this\n        attribute is set to `Signature.empty`.\n    * bind(*args, **kwargs) -> BoundArguments\n        Creates a mapping from positional and keyword arguments to\n        parameters.\n    * bind_partial(*args, **kwargs) -> BoundArguments\n        Creates a partial mapping from positional and keyword arguments\n        to parameters (simulating 'functools.partial' behavior.)\n    "
        __slots__ = ('_return_annotation', '_parameters')
        _parameter_cls = Parameter
        _bound_arguments_cls = BoundArguments
        empty = _empty

        def __init__(self, parameters=None, *, return_annotation=_empty, __validate_parameters__=True):
            """Constructs Signature from the given list of Parameter
        objects and 'return_annotation'.  All arguments are optional.
        """
            if parameters is None:
                params = OrderedDict()
            elif __validate_parameters__:
                params = OrderedDict()
                top_kind = _POSITIONAL_ONLY
                kind_defaults = False
                for idx, param in enumerate(parameters):
                    kind = param.kind
                    name = param.name
                    if kind < top_kind:
                        msg = 'wrong parameter order: {} parameter before {} parameter'
                        msg = msg.formattop_kind.descriptionkind.description
                        raise ValueError(msg)
                    elif kind > top_kind:
                        kind_defaults = False
                        top_kind = kind
                    if kind in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD):
                        if param.default is _empty:
                            if kind_defaults:
                                msg = 'non-default argument follows default argument'
                                raise ValueError(msg)
                        else:
                            kind_defaults = True
                    if name in params:
                        msg = 'duplicate parameter name: {!r}'.format(name)
                        raise ValueError(msg)
                    else:
                        params[name] = param

            else:
                params = OrderedDict(((param.name, param) for param in parameters))
            self._parameters = types.MappingProxyType(params)
            self._return_annotation = return_annotation

        @classmethod
        def from_function(cls, func):
            """Constructs Signature for the given python function.

        Deprecated since Python 3.5, use `Signature.from_callable()`.
        """
            warnings.warn('inspect.Signature.from_function() is deprecated since Python 3.5, use Signature.from_callable()', DeprecationWarning,
              stacklevel=2)
            return _signature_from_function(cls, func)

        @classmethod
        def from_builtin(cls, func):
            """Constructs Signature for the given builtin function.

        Deprecated since Python 3.5, use `Signature.from_callable()`.
        """
            warnings.warn('inspect.Signature.from_builtin() is deprecated since Python 3.5, use Signature.from_callable()', DeprecationWarning,
              stacklevel=2)
            return _signature_from_builtin(cls, func)

        @classmethod
        def from_callable(cls, obj, *, follow_wrapped=True):
            """Constructs Signature for the given callable object."""
            return _signature_from_callable(obj, sigcls=cls, follow_wrapper_chains=follow_wrapped)

        @property
        def parameters(self):
            return self._parameters

        @property
        def return_annotation(self):
            return self._return_annotation

        def replace(self, *, parameters=_void, return_annotation=_void):
            """Creates a customized copy of the Signature.
        Pass 'parameters' and/or 'return_annotation' arguments
        to override them in the new copy.
        """
            if parameters is _void:
                parameters = self.parameters.values()
            if return_annotation is _void:
                return_annotation = self._return_annotation
            return type(self)(parameters, return_annotation=return_annotation)

        def _hash_basis(self):
            params = tuple((param for param in self.parameters.values() if param.kind != _KEYWORD_ONLY))
            kwo_params = {param:param.name for param in self.parameters.values() if param.kind == _KEYWORD_ONLY if param.kind == _KEYWORD_ONLY}
            return (
             params, kwo_params, self.return_annotation)

        def __hash__(self):
            params, kwo_params, return_annotation = self._hash_basis()
            kwo_params = frozenset(kwo_params.values())
            return hash((params, kwo_params, return_annotation))

        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, Signature):
                return NotImplemented
            return self._hash_basis() == other._hash_basis()

        def _bind(self, args, kwargs, *, partial=False):
            """Private method. Don't use directly."""
            arguments = OrderedDict()
            parameters = iter(self.parameters.values())
            parameters_ex = ()
            arg_vals = iter(args)
            while True:
                try:
                    arg_val = next(arg_vals)
                except StopIteration:
                    try:
                        param = next(parameters)
                    except StopIteration:
                        break
                    else:
                        if param.kind == _VAR_POSITIONAL:
                            break
                        elif param.name in kwargs:
                            if param.kind == _POSITIONAL_ONLY:
                                msg = '{arg!r} parameter is positional only, but was passed as a keyword'
                                msg = msg.format(arg=(param.name))
                                raise TypeError(msg) from None
                            parameters_ex = (
                             param,)
                            break
                        elif param.kind == _VAR_KEYWORD or param.default is not _empty:
                            parameters_ex = (
                             param,)
                            break
                        elif partial:
                            parameters_ex = (
                             param,)
                            break
                        else:
                            msg = 'missing a required argument: {arg!r}'
                            msg = msg.format(arg=(param.name))
                            raise TypeError(msg) from None
                else:
                    try:
                        param = next(parameters)
                    except StopIteration:
                        raise TypeError('too many positional arguments') from None
                    else:
                        if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                            raise TypeError('too many positional arguments') from None
                        if param.kind == _VAR_POSITIONAL:
                            values = [
                             arg_val]
                            values.extend(arg_vals)
                            arguments[param.name] = tuple(values)
                        else:
                            if param.name in kwargs:
                                if param.kind != _POSITIONAL_ONLY:
                                    raise TypeError('multiple values for argument {arg!r}'.format(arg=(param.name))) from None
                            arguments[param.name] = arg_val

            kwargs_param = None
            for param in itertools.chainparameters_exparameters:
                if param.kind == _VAR_KEYWORD:
                    kwargs_param = param
                else:
                    if param.kind == _VAR_POSITIONAL:
                        pass
                    else:
                        param_name = param.name
                        try:
                            arg_val = kwargs.pop(param_name)
                        except KeyError:
                            if not partial:
                                if param.kind != _VAR_POSITIONAL:
                                    if param.default is _empty:
                                        raise TypeError('missing a required argument: {arg!r}'.format(arg=param_name)) from None
                        else:
                            if param.kind == _POSITIONAL_ONLY:
                                raise TypeError('{arg!r} parameter is positional only, but was passed as a keyword'.format(arg=(param.name)))
                            arguments[param_name] = arg_val
            else:
                if kwargs:
                    if kwargs_param is not None:
                        arguments[kwargs_param.name] = kwargs
                    else:
                        raise TypeError('got an unexpected keyword argument {arg!r}'.format(arg=(next(iter(kwargs)))))
                return self._bound_arguments_clsselfarguments

        def bind(self, *args, **kwargs):
            """Get a BoundArguments object, that maps the passed `args`
        and `kwargs` to the function's signature.  Raises `TypeError`
        if the passed arguments can not be bound.
        """
            return self._bindargskwargs

        def bind_partial(self, *args, **kwargs):
            """Get a BoundArguments object, that partially maps the
        passed `args` and `kwargs` to the function's signature.
        Raises `TypeError` if the passed arguments can not be bound.
        """
            return self._bind(args, kwargs, partial=True)

        def __reduce__(self):
            return (
             type(self),
             (
              tuple(self._parameters.values()),),
             {'_return_annotation': self._return_annotation})

        def __setstate__(self, state):
            self._return_annotation = state['_return_annotation']

        def __repr__(self):
            return '<{} {}>'.formatself.__class__.__name__self

        def __str__(self):
            result = []
            render_pos_only_separator = False
            render_kw_only_separator = True
            for param in self.parameters.values():
                formatted = str(param)
                kind = param.kind
                if kind == _POSITIONAL_ONLY:
                    render_pos_only_separator = True
                elif render_pos_only_separator:
                    result.append('/')
                    render_pos_only_separator = False
                if kind == _VAR_POSITIONAL:
                    render_kw_only_separator = False
                elif kind == _KEYWORD_ONLY:
                    if render_kw_only_separator:
                        result.append('*')
                        render_kw_only_separator = False
                result.append(formatted)
            else:
                if render_pos_only_separator:
                    result.append('/')
                rendered = '({})'.format(', '.join(result))
                if self.return_annotation is not _empty:
                    anno = formatannotation(self.return_annotation)
                    rendered += ' -> {}'.format(anno)
                return rendered


    def signature(obj, *, follow_wrapped=True):
        """Get a signature object for the passed callable."""
        return Signature.from_callable(obj, follow_wrapped=follow_wrapped)


    def _main():
        """ Logic for inspecting an object given at command line """
        import argparse, importlib
        parser = argparse.ArgumentParser()
        parser.add_argument('object',
          help="The object to be analysed. It supports the 'module:qualname' syntax")
        parser.add_argument('-d',
          '--details', action='store_true', help='Display info about the module rather than its source code')
        args = parser.parse_args()
        target = args.object
        mod_name, has_attrs, attrs = target.partition(':')
        try:
            obj = module = importlib.import_module(mod_name)
        except Exception as exc:
            try:
                msg = 'Failed to import {} ({}: {})'.format(mod_name, type(exc).__name__, exc)
                print(msg, file=(sys.stderr))
                sys.exit(2)
            finally:
                exc = None
                del exc

        else:
            if has_attrs:
                parts = attrs.split('.')
                obj = module
                for part in parts:
                    obj = getattr(obj, part)
                else:
                    if module.__name__ in sys.builtin_module_names:
                        print("Can't get info for builtin modules.", file=(sys.stderr))
                        sys.exit(1)

        if args.details:
            print('Target: {}'.format(target))
            print('Origin: {}'.format(getsourcefile(module)))
            print('Cached: {}'.format(module.__cached__))
            if obj is module:
                print('Loader: {}'.format(repr(module.__loader__)))
                if hasattr(module, '__path__'):
                    print('Submodule search path: {}'.format(module.__path__))
            else:
                try:
                    __, lineno = findsource(obj)
                except Exception:
                    pass
                else:
                    print('Line: {}'.format(lineno))
            print('\n')
        else:
            print(getsource(obj))


    if __name__ == '__main__':
        _main()