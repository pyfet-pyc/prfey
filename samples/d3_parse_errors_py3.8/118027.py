# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\ipv4.py
"""IPv4 helper functions."""
import struct, dns.exception
from ._compat import binary_type

def inet_ntoa(address):
    """Convert an IPv4 address in binary form to text form.

    *address*, a ``binary``, the IPv4 address in binary form.

    Returns a ``text``.
    """
    if len(address) != 4:
        raise dns.exception.SyntaxError
    if not isinstance(address, bytearray):
        address = bytearray(address)
    return '%u.%u.%u.%u' % (address[0], address[1],
     address[2], address[3])


def inet_aton--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'text'
                4  LOAD_GLOBAL              binary_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.  49        10  LOAD_FAST                'text'
               12  LOAD_METHOD              encode
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'text'
             18_0  COME_FROM             8  '8'

 L.  50        18  LOAD_FAST                'text'
               20  LOAD_METHOD              split
               22  LOAD_CONST               b'.'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'parts'

 L.  51        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'parts'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               4
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  52        40  LOAD_GLOBAL              dns
               42  LOAD_ATTR                exception
               44  LOAD_ATTR                SyntaxError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  53        48  LOAD_FAST                'parts'
               50  GET_ITER         
             52_0  COME_FROM           104  '104'
             52_1  COME_FROM            94  '94'
             52_2  COME_FROM            82  '82'
               52  FOR_ITER            106  'to 106'
               54  STORE_FAST               'part'

 L.  54        56  LOAD_FAST                'part'
               58  LOAD_METHOD              isdigit
               60  CALL_METHOD_0         0  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L.  55        64  LOAD_GLOBAL              dns
               66  LOAD_ATTR                exception
               68  LOAD_ATTR                SyntaxError
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L.  56        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'part'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               1
               80  COMPARE_OP               >
               82  POP_JUMP_IF_FALSE_BACK    52  'to 52'
               84  LOAD_FAST                'part'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  LOAD_STR                 '0'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE_BACK    52  'to 52'

 L.  58        96  LOAD_GLOBAL              dns
               98  LOAD_ATTR                exception
              100  LOAD_ATTR                SyntaxError
              102  RAISE_VARARGS_1       1  'exception instance'
              104  JUMP_BACK            52  'to 52'
            106_0  COME_FROM            52  '52'

 L.  59       106  SETUP_FINALLY       138  'to 138'

 L.  60       108  LOAD_LISTCOMP            '<code_object <listcomp>>'
              110  LOAD_STR                 'inet_aton.<locals>.<listcomp>'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  LOAD_FAST                'parts'
              116  GET_ITER         
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'bytes'

 L.  61       122  LOAD_GLOBAL              struct
              124  LOAD_ATTR                pack
              126  LOAD_CONST               ('BBBB',)
              128  LOAD_FAST                'bytes'
              130  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              132  CALL_FUNCTION_EX      0  'positional arguments only'
              134  POP_BLOCK        
              136  RETURN_VALUE     
            138_0  COME_FROM_FINALLY   106  '106'

 L.  62       138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L.  63       144  LOAD_GLOBAL              dns
              146  LOAD_ATTR                exception
              148  LOAD_ATTR                SyntaxError
              150  RAISE_VARARGS_1       1  'exception instance'
              152  POP_EXCEPT       
              154  JUMP_FORWARD        158  'to 158'
              156  END_FINALLY      
            158_0  COME_FROM           154  '154'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 150