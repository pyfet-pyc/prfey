# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: attr\_compat.py
from __future__ import absolute_import, division, print_function
import platform, sys, types, warnings
PY2 = sys.version_info[0] == 2
PYPY = platform.python_implementation() == 'PyPy'
if PYPY or sys.version_info[:2] >= (3, 6):
    ordered_dict = dict
else:
    from collections import OrderedDict
    ordered_dict = OrderedDict
if PY2:
    from collections import Mapping, Sequence
    from UserDict import IterableUserDict

    def isclass(klass):
        return isinstance(klass, (type, types.ClassType))


    def new_class(name, bases, kwds, exec_body):
        """
        A minimal stub of types.new_class that we need for make_class.
        """
        ns = {}
        exec_body(ns)
        return type(name, bases, ns)


    TYPE = 'type'

    def iteritems(d):
        return d.iteritems()


    class ReadOnlyDict(IterableUserDict):
        __doc__ = '\n        Best-effort read-only dict wrapper.\n        '

        def __setitem__(self, key, val):
            raise TypeError("'mappingproxy' object does not support item assignment")

        def update(self, _):
            raise AttributeError("'mappingproxy' object has no attribute 'update'")

        def __delitem__(self, _):
            raise TypeError("'mappingproxy' object does not support item deletion")

        def clear(self):
            raise AttributeError("'mappingproxy' object has no attribute 'clear'")

        def pop(self, key, default=None):
            raise AttributeError("'mappingproxy' object has no attribute 'pop'")

        def popitem(self):
            raise AttributeError("'mappingproxy' object has no attribute 'popitem'")

        def setdefault(self, key, default=None):
            raise AttributeError("'mappingproxy' object has no attribute 'setdefault'")

        def __repr__(self):
            return 'mappingproxy(' + repr(self.data) + ')'


    def metadata_proxy(d):
        res = ReadOnlyDict()
        res.data.update(d)
        return res


    def just_warn(*args, **kw):
        """
        We only warn on Python 3 because we are not aware of any concrete
        consequences of not setting the cell on Python 2.
        """
        pass


else:
    from collections.abc import Mapping, Sequence

    def just_warn(*args, **kw):
        """
        We only warn on Python 3 because we are not aware of any concrete
        consequences of not setting the cell on Python 2.
        """
        warnings.warn("Running interpreter doesn't sufficiently support code object introspection.  Some features like bare super() or accessing __class__ will not work with slotted classes.",
          RuntimeWarning,
          stacklevel=2)


    def isclass(klass):
        return isinstance(klass, type)


    TYPE = 'class'

    def iteritems(d):
        return d.items()


    new_class = types.new_class

    def metadata_proxy(d):
        return types.MappingProxyType(dict(d))


def make_set_closure_cell--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL              PYPY
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 148         4  LOAD_CODE                <code_object set_closure_cell>
                6  LOAD_STR                 'make_set_closure_cell.<locals>.set_closure_cell'
                8  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               10  STORE_FAST               'set_closure_cell'

 L. 151        12  LOAD_FAST                'set_closure_cell'
               14  RETURN_VALUE     
             16_0  COME_FROM             2  '2'

 L. 156        16  LOAD_CODE                <code_object set_first_cellvar_to>
               18  LOAD_STR                 'make_set_closure_cell.<locals>.set_first_cellvar_to'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'set_first_cellvar_to'

 L. 166        24  SETUP_FINALLY       274  'to 274'

 L. 169        26  LOAD_GLOBAL              PY2
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 170        30  LOAD_FAST                'set_first_cellvar_to'
               32  LOAD_ATTR                func_code
               34  STORE_FAST               'co'
               36  JUMP_FORWARD         44  'to 44'
             38_0  COME_FROM            28  '28'

 L. 172        38  LOAD_FAST                'set_first_cellvar_to'
               40  LOAD_ATTR                __code__
               42  STORE_FAST               'co'
             44_0  COME_FROM            36  '36'

 L. 173        44  LOAD_FAST                'co'
               46  LOAD_ATTR                co_cellvars
               48  LOAD_CONST               ('x',)
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_TRUE     64  'to 64'
               54  LOAD_FAST                'co'
               56  LOAD_ATTR                co_freevars
               58  LOAD_CONST               ()
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE    68  'to 68'
             64_0  COME_FROM            52  '52'

 L. 174        64  LOAD_GLOBAL              AssertionError
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            62  '62'

 L. 178        68  LOAD_GLOBAL              sys
               70  LOAD_ATTR                version_info
               72  LOAD_CONST               (3, 8)
               74  COMPARE_OP               >=
               76  POP_JUMP_IF_FALSE    98  'to 98'

 L. 182        78  LOAD_FAST                'co'
               80  LOAD_ATTR                replace

 L. 183        82  LOAD_FAST                'co'
               84  LOAD_ATTR                co_freevars
               86  LOAD_FAST                'co'
               88  LOAD_ATTR                co_cellvars

 L. 182        90  LOAD_CONST               ('co_cellvars', 'co_freevars')
               92  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               94  STORE_DEREF              'set_first_freevar_code'
               96  JUMP_FORWARD        194  'to 194'
             98_0  COME_FROM            76  '76'

 L. 186        98  LOAD_FAST                'co'
              100  LOAD_ATTR                co_argcount
              102  BUILD_LIST_1          1 
              104  STORE_FAST               'args'

 L. 187       106  LOAD_GLOBAL              PY2
              108  POP_JUMP_IF_TRUE    122  'to 122'

 L. 188       110  LOAD_FAST                'args'
              112  LOAD_METHOD              append
              114  LOAD_FAST                'co'
              116  LOAD_ATTR                co_kwonlyargcount
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
            122_0  COME_FROM           108  '108'

 L. 189       122  LOAD_FAST                'args'
              124  LOAD_METHOD              extend

 L. 191       126  LOAD_FAST                'co'
              128  LOAD_ATTR                co_nlocals

 L. 192       130  LOAD_FAST                'co'
              132  LOAD_ATTR                co_stacksize

 L. 193       134  LOAD_FAST                'co'
              136  LOAD_ATTR                co_flags

 L. 194       138  LOAD_FAST                'co'
              140  LOAD_ATTR                co_code

 L. 195       142  LOAD_FAST                'co'
              144  LOAD_ATTR                co_consts

 L. 196       146  LOAD_FAST                'co'
              148  LOAD_ATTR                co_names

 L. 197       150  LOAD_FAST                'co'
              152  LOAD_ATTR                co_varnames

 L. 198       154  LOAD_FAST                'co'
              156  LOAD_ATTR                co_filename

 L. 199       158  LOAD_FAST                'co'
              160  LOAD_ATTR                co_name

 L. 200       162  LOAD_FAST                'co'
              164  LOAD_ATTR                co_firstlineno

 L. 201       166  LOAD_FAST                'co'
              168  LOAD_ATTR                co_lnotab

 L. 203       170  LOAD_FAST                'co'
              172  LOAD_ATTR                co_cellvars

 L. 204       174  LOAD_FAST                'co'
              176  LOAD_ATTR                co_freevars

 L. 190       178  BUILD_LIST_13        13 

 L. 189       180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 207       184  LOAD_GLOBAL              types
              186  LOAD_ATTR                CodeType
              188  LOAD_FAST                'args'
              190  CALL_FUNCTION_EX      0  'positional arguments only'
              192  STORE_DEREF              'set_first_freevar_code'
            194_0  COME_FROM            96  '96'

 L. 209       194  LOAD_CLOSURE             'set_first_freevar_code'
              196  BUILD_TUPLE_1         1 
              198  LOAD_CODE                <code_object set_closure_cell>
              200  LOAD_STR                 'make_set_closure_cell.<locals>.set_closure_cell'
              202  MAKE_FUNCTION_8          'closure'
              204  STORE_FAST               'set_closure_cell'

 L. 220       206  LOAD_CODE                <code_object make_func_with_cell>
              208  LOAD_STR                 'make_set_closure_cell.<locals>.make_func_with_cell'
              210  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              212  STORE_FAST               'make_func_with_cell'

 L. 228       214  LOAD_GLOBAL              PY2
              216  POP_JUMP_IF_FALSE   232  'to 232'

 L. 229       218  LOAD_FAST                'make_func_with_cell'
              220  CALL_FUNCTION_0       0  ''
              222  LOAD_ATTR                func_closure
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  STORE_FAST               'cell'
              230  JUMP_FORWARD        244  'to 244'
            232_0  COME_FROM           216  '216'

 L. 231       232  LOAD_FAST                'make_func_with_cell'
              234  CALL_FUNCTION_0       0  ''
              236  LOAD_ATTR                __closure__
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  STORE_FAST               'cell'
            244_0  COME_FROM           230  '230'

 L. 232       244  LOAD_FAST                'set_closure_cell'
              246  LOAD_FAST                'cell'
              248  LOAD_CONST               100
              250  CALL_FUNCTION_2       2  ''
              252  POP_TOP          

 L. 233       254  LOAD_FAST                'cell'
              256  LOAD_ATTR                cell_contents
              258  LOAD_CONST               100
              260  COMPARE_OP               !=
          262_264  POP_JUMP_IF_FALSE   270  'to 270'

 L. 234       266  LOAD_GLOBAL              AssertionError
              268  RAISE_VARARGS_1       1  'exception instance'
            270_0  COME_FROM           262  '262'
              270  POP_BLOCK        
              272  JUMP_FORWARD        298  'to 298'
            274_0  COME_FROM_FINALLY    24  '24'

 L. 236       274  DUP_TOP          
              276  LOAD_GLOBAL              Exception
          278_280  <121>               296  ''
              282  POP_TOP          
              284  POP_TOP          
              286  POP_TOP          

 L. 237       288  LOAD_GLOBAL              just_warn
              290  ROT_FOUR         
              292  POP_EXCEPT       
              294  RETURN_VALUE     
              296  <48>             
            298_0  COME_FROM           272  '272'

 L. 239       298  LOAD_FAST                'set_closure_cell'
              300  RETURN_VALUE     

Parse error at or near `<121>' instruction at offset 278_280


set_closure_cell = make_set_closure_cell()