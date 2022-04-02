# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\core\_asarray.py
"""
Functions in the ``as*array`` family that promote array-likes into arrays.

`require` fits this category despite its name not matching this pattern.
"""
from .overrides import array_function_dispatch, set_array_function_like_doc, set_module
from .multiarray import array, asanyarray
__all__ = [
 'require']

def _require_dispatcher(a, dtype=None, requirements=None, *, like=None):
    return (
     like,)


@set_array_function_like_doc
@set_module('numpy')
def require--- This code section failed: ---

 L.  94         0  LOAD_FAST                'like'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L.  95         8  LOAD_GLOBAL              _require_with_like

 L.  96        10  LOAD_FAST                'a'

 L.  97        12  LOAD_FAST                'dtype'

 L.  98        14  LOAD_FAST                'requirements'

 L.  99        16  LOAD_FAST                'like'

 L.  95        18  LOAD_CONST               ('dtype', 'requirements', 'like')
               20  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               22  RETURN_VALUE     
             24_0  COME_FROM             6  '6'

 L. 102        24  LOAD_STR                 'C'
               26  LOAD_STR                 'C'
               28  LOAD_STR                 'C'

 L. 103        30  LOAD_STR                 'F'
               32  LOAD_STR                 'F'
               34  LOAD_STR                 'F'

 L. 104        36  LOAD_STR                 'A'
               38  LOAD_STR                 'A'

 L. 105        40  LOAD_STR                 'W'
               42  LOAD_STR                 'W'

 L. 106        44  LOAD_STR                 'O'
               46  LOAD_STR                 'O'

 L. 107        48  LOAD_STR                 'E'
               50  LOAD_STR                 'E'

 L. 102        52  LOAD_CONST               ('C', 'C_CONTIGUOUS', 'CONTIGUOUS', 'F', 'F_CONTIGUOUS', 'FORTRAN', 'A', 'ALIGNED', 'W', 'WRITEABLE', 'O', 'OWNDATA', 'E', 'ENSUREARRAY')
               54  BUILD_CONST_KEY_MAP_14    14 
               56  STORE_DEREF              'possible_flags'

 L. 108        58  LOAD_FAST                'requirements'
               60  POP_JUMP_IF_TRUE     74  'to 74'

 L. 109        62  LOAD_GLOBAL              asanyarray
               64  LOAD_FAST                'a'
               66  LOAD_FAST                'dtype'
               68  LOAD_CONST               ('dtype',)
               70  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               72  RETURN_VALUE     
             74_0  COME_FROM            60  '60'

 L. 111        74  LOAD_CLOSURE             'possible_flags'
               76  BUILD_TUPLE_1         1 
               78  LOAD_SETCOMP             '<code_object <setcomp>>'
               80  LOAD_STR                 'require.<locals>.<setcomp>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_FAST                'requirements'
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'requirements'

 L. 113        92  LOAD_STR                 'E'
               94  LOAD_FAST                'requirements'
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L. 114       100  LOAD_FAST                'requirements'
              102  LOAD_METHOD              remove
              104  LOAD_STR                 'E'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 115       110  LOAD_CONST               False
              112  STORE_FAST               'subok'
              114  JUMP_FORWARD        120  'to 120'
            116_0  COME_FROM            98  '98'

 L. 117       116  LOAD_CONST               True
              118  STORE_FAST               'subok'
            120_0  COME_FROM           114  '114'

 L. 119       120  LOAD_STR                 'A'
              122  STORE_FAST               'order'

 L. 120       124  LOAD_FAST                'requirements'
              126  LOAD_STR                 'C'
              128  LOAD_STR                 'F'
              130  BUILD_SET_2           2 
              132  COMPARE_OP               >=
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 121       136  LOAD_GLOBAL              ValueError
              138  LOAD_STR                 'Cannot specify both "C" and "F" order'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
              144  JUMP_FORWARD        192  'to 192'
            146_0  COME_FROM           134  '134'

 L. 122       146  LOAD_STR                 'F'
              148  LOAD_FAST                'requirements'
              150  <118>                 0  ''
              152  POP_JUMP_IF_FALSE   170  'to 170'

 L. 123       154  LOAD_STR                 'F'
              156  STORE_FAST               'order'

 L. 124       158  LOAD_FAST                'requirements'
              160  LOAD_METHOD              remove
              162  LOAD_STR                 'F'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_FORWARD        192  'to 192'
            170_0  COME_FROM           152  '152'

 L. 125       170  LOAD_STR                 'C'
              172  LOAD_FAST                'requirements'
              174  <118>                 0  ''
              176  POP_JUMP_IF_FALSE   192  'to 192'

 L. 126       178  LOAD_STR                 'C'
              180  STORE_FAST               'order'

 L. 127       182  LOAD_FAST                'requirements'
              184  LOAD_METHOD              remove
              186  LOAD_STR                 'C'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
            192_0  COME_FROM           176  '176'
            192_1  COME_FROM           168  '168'
            192_2  COME_FROM           144  '144'

 L. 129       192  LOAD_GLOBAL              array
              194  LOAD_FAST                'a'
              196  LOAD_FAST                'dtype'
              198  LOAD_FAST                'order'
              200  LOAD_CONST               False
              202  LOAD_FAST                'subok'
              204  LOAD_CONST               ('dtype', 'order', 'copy', 'subok')
              206  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              208  STORE_FAST               'arr'

 L. 131       210  LOAD_FAST                'requirements'
              212  GET_ITER         
            214_0  COME_FROM           242  '242'
            214_1  COME_FROM           226  '226'
              214  FOR_ITER            244  'to 244'
              216  STORE_FAST               'prop'

 L. 132       218  LOAD_FAST                'arr'
              220  LOAD_ATTR                flags
              222  LOAD_FAST                'prop'
              224  BINARY_SUBSCR    
              226  POP_JUMP_IF_TRUE_BACK   214  'to 214'

 L. 133       228  LOAD_FAST                'arr'
              230  LOAD_METHOD              copy
              232  LOAD_FAST                'order'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'arr'

 L. 134       238  POP_TOP          
              240  BREAK_LOOP          244  'to 244'
              242  JUMP_BACK           214  'to 214'
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           214  '214'

 L. 135       244  LOAD_FAST                'arr'
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


_require_with_like = array_function_dispatch(_require_dispatcher)(require)