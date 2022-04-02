# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\wiredata.py
"""DNS Wire Data Helper"""
import dns.exception
from ._compat import binary_type, string_types, PY2

class _SliceUnspecifiedBound(binary_type):

    def __getitem__(self, key):
        return key.stop

    if PY2:

        def __getslice__(self, i, j):
            return self.__getitem__(slice(i, j))


_unspecified_bound = _SliceUnspecifiedBound()[1:]

class WireData(binary_type):

    def __getitem__--- This code section failed: ---

 L.  46         0  SETUP_FINALLY       210  'to 210'

 L.  47         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'key'
                6  LOAD_GLOBAL              slice
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE   192  'to 192'

 L.  51        12  LOAD_FAST                'key'
               14  LOAD_ATTR                start
               16  STORE_FAST               'start'

 L.  52        18  LOAD_FAST                'key'
               20  LOAD_ATTR                stop
               22  STORE_FAST               'stop'

 L.  54        24  LOAD_GLOBAL              PY2
               26  POP_JUMP_IF_FALSE   114  'to 114'

 L.  55        28  LOAD_FAST                'stop'
               30  LOAD_GLOBAL              _unspecified_bound
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L.  57        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'self'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'stop'
             44_0  COME_FROM            34  '34'

 L.  59        44  LOAD_FAST                'start'
               46  LOAD_CONST               0
               48  COMPARE_OP               <
               50  POP_JUMP_IF_TRUE     60  'to 60'
               52  LOAD_FAST                'stop'
               54  LOAD_CONST               0
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE    68  'to 68'
             60_0  COME_FROM            50  '50'

 L.  60        60  LOAD_GLOBAL              dns
               62  LOAD_ATTR                exception
               64  LOAD_ATTR                FormError
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L.  63        68  LOAD_FAST                'start'
               70  LOAD_FAST                'stop'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE   164  'to 164'

 L.  64        76  LOAD_GLOBAL              super
               78  LOAD_GLOBAL              WireData
               80  LOAD_FAST                'self'
               82  CALL_FUNCTION_2       2  ''
               84  LOAD_METHOD              __getitem__
               86  LOAD_FAST                'start'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  65        92  LOAD_GLOBAL              super
               94  LOAD_GLOBAL              WireData
               96  LOAD_FAST                'self'
               98  CALL_FUNCTION_2       2  ''
              100  LOAD_METHOD              __getitem__
              102  LOAD_FAST                'stop'
              104  LOAD_CONST               1
              106  BINARY_SUBTRACT  
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
              112  JUMP_FORWARD        164  'to 164'
            114_0  COME_FROM            26  '26'

 L.  67       114  LOAD_FAST                'start'
              116  LOAD_FAST                'stop'
              118  BUILD_TUPLE_2         2 
              120  GET_ITER         
            122_0  COME_FROM           152  '152'
              122  FOR_ITER            164  'to 164'
              124  STORE_FAST               'index'

 L.  68       126  LOAD_FAST                'index'
              128  LOAD_CONST               None
              130  COMPARE_OP               is
              132  POP_JUMP_IF_FALSE   138  'to 138'

 L.  69       134  CONTINUE            122  'to 122'
              136  JUMP_BACK           122  'to 122'
            138_0  COME_FROM           132  '132'

 L.  70       138  LOAD_GLOBAL              abs
              140  LOAD_FAST                'index'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'self'
              148  CALL_FUNCTION_1       1  ''
              150  COMPARE_OP               >
              152  POP_JUMP_IF_FALSE   122  'to 122'

 L.  71       154  LOAD_GLOBAL              dns
              156  LOAD_ATTR                exception
              158  LOAD_ATTR                FormError
              160  RAISE_VARARGS_1       1  'exception instance'
              162  JUMP_BACK           122  'to 122'
            164_0  COME_FROM           112  '112'
            164_1  COME_FROM            74  '74'

 L.  73       164  LOAD_GLOBAL              WireData
              166  LOAD_GLOBAL              super
              168  LOAD_GLOBAL              WireData
              170  LOAD_FAST                'self'
              172  CALL_FUNCTION_2       2  ''
              174  LOAD_METHOD              __getitem__

 L.  74       176  LOAD_GLOBAL              slice
              178  LOAD_FAST                'start'
              180  LOAD_FAST                'stop'
              182  CALL_FUNCTION_2       2  ''

 L.  73       184  CALL_METHOD_1         1  ''
              186  CALL_FUNCTION_1       1  ''
              188  POP_BLOCK        
              190  RETURN_VALUE     
            192_0  COME_FROM            10  '10'

 L.  75       192  LOAD_GLOBAL              bytearray
              194  LOAD_FAST                'self'
              196  LOAD_METHOD              unwrap
              198  CALL_METHOD_0         0  ''
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_FAST                'key'
              204  BINARY_SUBSCR    
              206  POP_BLOCK        
              208  RETURN_VALUE     
            210_0  COME_FROM_FINALLY     0  '0'

 L.  76       210  DUP_TOP          
              212  LOAD_GLOBAL              IndexError
              214  COMPARE_OP               exception-match
              216  POP_JUMP_IF_FALSE   236  'to 236'
              218  POP_TOP          
              220  POP_TOP          
              222  POP_TOP          

 L.  77       224  LOAD_GLOBAL              dns
              226  LOAD_ATTR                exception
              228  LOAD_ATTR                FormError
              230  RAISE_VARARGS_1       1  'exception instance'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           216  '216'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'

Parse error at or near `POP_TOP' instruction at offset 220

    if PY2:

        def __getslice__(self, i, j):
            return self.__getitem__(slice(i, j))

    def __iter__(self):
        i = 0
        while True:
            try:
                (yield self[i])
                i += 1
            except dns.exception.FormError:
                raise StopIteration

    def unwrap(self):
        return binary_type(self)


def maybe_wrap(wire):
    if isinstance(wire, WireData):
        return wire
    if isinstance(wire, binary_type):
        return WireData(wire)
    if isinstance(wire, string_types):
        return WireData(wire.encode)
    raise ValueError('unhandled type %s' % type(wire))