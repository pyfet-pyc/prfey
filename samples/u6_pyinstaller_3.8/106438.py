# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\_internal_utils.py
"""
requests._internal_utils
~~~~~~~~~~~~~~

Provides utility functions that are consumed internally by Requests
which depend on extremely few external helpers (such as compat)
"""
from .compat import is_py2, builtin_str, str

def to_native_string(string, encoding='ascii'):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    if isinstance(string, builtin_str):
        out = string
    else:
        if is_py2:
            out = string.encode(encoding)
        else:
            out = string.decode(encoding)
    return out


def unicode_is_ascii--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'u_string'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  LOAD_ASSERT              AssertionError
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L.  38        14  SETUP_FINALLY        32  'to 32'

 L.  39        16  LOAD_FAST                'u_string'
               18  LOAD_METHOD              encode
               20  LOAD_STR                 'ascii'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L.  40        26  POP_BLOCK        
               28  LOAD_CONST               True
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    14  '14'

 L.  41        32  DUP_TOP          
               34  LOAD_GLOBAL              UnicodeEncodeError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    52  'to 52'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  42        46  POP_EXCEPT       
               48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'
               52  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 30