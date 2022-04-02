# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\compat\_inspect.py
"""Subset of inspect module from upstream python

We use this instead of upstream because upstream inspect is slow to import, and
significantly contributes to numpy import times. Importing this copy has almost
no overhead.

"""
import types
__all__ = [
 'getargspec', 'formatargspec']

def ismethod(object):
    """Return true if the object is an instance method.

    Instance method objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this method was defined
        im_class        class object in which this method belongs
        im_func         function object containing implementation of method
        im_self         instance to which this method is bound, or None

    """
    return isinstance(object, types.MethodType)


def isfunction(object):
    """Return true if the object is a user-defined function.

    Function objects provide these attributes:
        __doc__         documentation string
        __name__        name with which this function was defined
        func_code       code object containing compiled function bytecode
        func_defaults   tuple of any default values for arguments
        func_doc        (same as __doc__)
        func_globals    global namespace in which this function was defined
        func_name       (same as __name__)

    """
    return isinstance(object, types.FunctionType)


def iscode(object):
    """Return true if the object is a code object.

    Code objects provide these attributes:
        co_argcount     number of arguments (not including * or ** args)
        co_code         string of raw compiled bytecode
        co_consts       tuple of constants used in the bytecode
        co_filename     name of file in which this code object was created
        co_firstlineno  number of first line in Python source code
        co_flags        bitmap: 1=optimized | 2=newlocals | 4=*arg | 8=**arg
        co_lnotab       encoded mapping of line numbers to bytecode indices
        co_name         name with which this code object was defined
        co_names        tuple of names of local variables
        co_nlocals      number of local variables
        co_stacksize    virtual machine stack space required
        co_varnames     tuple of names of arguments and local variables
        
    """
    return isinstance(object, types.CodeType)


CO_OPTIMIZED, CO_NEWLOCALS, CO_VARARGS, CO_VARKEYWORDS = (1, 2, 4, 8)

def getargs--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              iscode
                2  LOAD_FAST                'co'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.  75         8  LOAD_GLOBAL              TypeError
               10  LOAD_STR                 'arg is not a code object'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  77        16  LOAD_FAST                'co'
               18  LOAD_ATTR                co_argcount
               20  STORE_FAST               'nargs'

 L.  78        22  LOAD_FAST                'co'
               24  LOAD_ATTR                co_varnames
               26  STORE_FAST               'names'

 L.  79        28  LOAD_GLOBAL              list
               30  LOAD_FAST                'names'
               32  LOAD_CONST               None
               34  LOAD_FAST                'nargs'
               36  BUILD_SLICE_2         2 
               38  BINARY_SUBSCR    
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'args'

 L.  84        44  LOAD_GLOBAL              range
               46  LOAD_FAST                'nargs'
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
             52_0  COME_FROM            84  '84'
             52_1  COME_FROM            74  '74'
               52  FOR_ITER             86  'to 86'
               54  STORE_FAST               'i'

 L.  85        56  LOAD_FAST                'args'
               58  LOAD_FAST                'i'
               60  BINARY_SUBSCR    
               62  LOAD_CONST               None
               64  LOAD_CONST               1
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  LOAD_CONST               ('', '.')
               72  <118>                 0  ''
               74  POP_JUMP_IF_FALSE_BACK    52  'to 52'

 L.  86        76  LOAD_GLOBAL              TypeError
               78  LOAD_STR                 'tuple function arguments are not supported'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
               84  JUMP_BACK            52  'to 52'
             86_0  COME_FROM            52  '52'

 L.  87        86  LOAD_CONST               None
               88  STORE_FAST               'varargs'

 L.  88        90  LOAD_FAST                'co'
               92  LOAD_ATTR                co_flags
               94  LOAD_GLOBAL              CO_VARARGS
               96  BINARY_AND       
               98  POP_JUMP_IF_FALSE   118  'to 118'

 L.  89       100  LOAD_FAST                'co'
              102  LOAD_ATTR                co_varnames
              104  LOAD_FAST                'nargs'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'varargs'

 L.  90       110  LOAD_FAST                'nargs'
              112  LOAD_CONST               1
              114  BINARY_ADD       
              116  STORE_FAST               'nargs'
            118_0  COME_FROM            98  '98'

 L.  91       118  LOAD_CONST               None
              120  STORE_FAST               'varkw'

 L.  92       122  LOAD_FAST                'co'
              124  LOAD_ATTR                co_flags
              126  LOAD_GLOBAL              CO_VARKEYWORDS
              128  BINARY_AND       
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L.  93       132  LOAD_FAST                'co'
              134  LOAD_ATTR                co_varnames
              136  LOAD_FAST                'nargs'
              138  BINARY_SUBSCR    
              140  STORE_FAST               'varkw'
            142_0  COME_FROM           130  '130'

 L.  94       142  LOAD_FAST                'args'
              144  LOAD_FAST                'varargs'
              146  LOAD_FAST                'varkw'
              148  BUILD_TUPLE_3         3 
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 72


def getargspec(func):
    """Get the names and default values of a function's arguments.

    A tuple of four things is returned: (args, varargs, varkw, defaults).
    'args' is a list of the argument names (it may contain nested lists).
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'defaults' is an n-tuple of the default values of the last n arguments.

    """
    if ismethod(func):
        func = func.__func__
    if not isfunction(func):
        raise TypeError('arg is not a Python function')
    args, varargs, varkw = getargs(func.__code__)
    return (
     args, varargs, varkw, func.__defaults__)


def getargvalues(frame):
    """Get information about arguments passed into a particular frame.

    A tuple of four things is returned: (args, varargs, varkw, locals).
    'args' is a list of the argument names (it may contain nested lists).
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'locals' is the locals dictionary of the given frame.
    
    """
    args, varargs, varkw = getargs(frame.f_code)
    return (
     args, varargs, varkw, frame.f_locals)


def joinseq(seq):
    if len(seq) == 1:
        return '(' + seq[0] + ',)'
    return '(' + ', '.join(seq) + ')'


def strseq--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'object'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              list
                8  LOAD_GLOBAL              tuple
               10  BUILD_TUPLE_2         2 
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    40  'to 40'

 L. 136        16  LOAD_DEREF               'join'
               18  LOAD_CLOSURE             'convert'
               20  LOAD_CLOSURE             'join'
               22  BUILD_TUPLE_2         2 
               24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'strseq.<locals>.<listcomp>'
               28  MAKE_FUNCTION_8          'closure'
               30  LOAD_FAST                'object'
               32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RETURN_VALUE     
             40_0  COME_FROM            14  '14'

 L. 138        40  LOAD_DEREF               'convert'
               42  LOAD_FAST                'object'
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def formatargspec--- This code section failed: ---

 L. 154         0  BUILD_LIST_0          0 
                2  STORE_FAST               'specs'

 L. 155         4  LOAD_FAST                'defaults'
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 156         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'args'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'defaults'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_SUBTRACT  
               22  STORE_FAST               'firstdefault'
             24_0  COME_FROM             6  '6'

 L. 157        24  LOAD_GLOBAL              range
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'args'
               30  CALL_FUNCTION_1       1  ''
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM            98  '98'
               36  FOR_ITER            100  'to 100'
               38  STORE_FAST               'i'

 L. 158        40  LOAD_GLOBAL              strseq
               42  LOAD_FAST                'args'
               44  LOAD_FAST                'i'
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'formatarg'
               50  LOAD_FAST                'join'
               52  CALL_FUNCTION_3       3  ''
               54  STORE_FAST               'spec'

 L. 159        56  LOAD_FAST                'defaults'
               58  POP_JUMP_IF_FALSE    88  'to 88'
               60  LOAD_FAST                'i'
               62  LOAD_FAST                'firstdefault'
               64  COMPARE_OP               >=
               66  POP_JUMP_IF_FALSE    88  'to 88'

 L. 160        68  LOAD_FAST                'spec'
               70  LOAD_FAST                'formatvalue'
               72  LOAD_FAST                'defaults'
               74  LOAD_FAST                'i'
               76  LOAD_FAST                'firstdefault'
               78  BINARY_SUBTRACT  
               80  BINARY_SUBSCR    
               82  CALL_FUNCTION_1       1  ''
               84  BINARY_ADD       
               86  STORE_FAST               'spec'
             88_0  COME_FROM            66  '66'
             88_1  COME_FROM            58  '58'

 L. 161        88  LOAD_FAST                'specs'
               90  LOAD_METHOD              append
               92  LOAD_FAST                'spec'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            36  'to 36'
            100_0  COME_FROM            36  '36'

 L. 162       100  LOAD_FAST                'varargs'
              102  LOAD_CONST               None
              104  <117>                 1  ''
              106  POP_JUMP_IF_FALSE   122  'to 122'

 L. 163       108  LOAD_FAST                'specs'
              110  LOAD_METHOD              append
              112  LOAD_FAST                'formatvarargs'
              114  LOAD_FAST                'varargs'
              116  CALL_FUNCTION_1       1  ''
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
            122_0  COME_FROM           106  '106'

 L. 164       122  LOAD_FAST                'varkw'
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_FALSE   144  'to 144'

 L. 165       130  LOAD_FAST                'specs'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'formatvarkw'
              136  LOAD_FAST                'varkw'
              138  CALL_FUNCTION_1       1  ''
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           128  '128'

 L. 166       144  LOAD_STR                 '('
              146  LOAD_STR                 ', '
              148  LOAD_METHOD              join
              150  LOAD_FAST                'specs'
              152  CALL_METHOD_1         1  ''
              154  BINARY_ADD       
              156  LOAD_STR                 ')'
              158  BINARY_ADD       
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 104


def formatargvalues(args, varargs, varkw, locals, formatarg=str, formatvarargs=lambda name: '*' + name, formatvarkw=lambda name: '**' + name, formatvalue=lambda value: '=' + repr(value), join=joinseq):
    """Format an argument spec from the 4 values returned by getargvalues.

    The first four arguments are (args, varargs, varkw, locals).  The
    next four arguments are the corresponding optional formatting functions
    that are called to turn names and values into strings.  The ninth
    argument is an optional function to format the sequence of arguments.

    """

    def convert(name, locals=locals, formatarg=formatarg, formatvalue=formatvalue):
        return formatarg(name) + formatvalue(locals[name])

    specs = [strseqargconvertjoin for arg in args]
    if varargs:
        specs.append(formatvarargs(varargs) + formatvalue(locals[varargs]))
    if varkw:
        specs.append(formatvarkw(varkw) + formatvalue(locals[varkw]))
    return '(' + ', '.join(specs) + ')'