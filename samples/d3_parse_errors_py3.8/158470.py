# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\py33compat.py
import dis, array, collections
try:
    import html
except ImportError:
    html = None
else:
    from setuptools.extern import six
    from setuptools.extern.six.moves import html_parser
    __metaclass__ = type
    OpArg = collections.namedtuple('OpArg', 'opcode arg')

    class Bytecode_compat:

        def __init__(self, code):
            self.code = code

        def __iter__--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              array
                2  LOAD_METHOD              array
                4  LOAD_STR                 'b'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                code
               10  LOAD_ATTR                co_code
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'bytes'

 L.  26        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                code
               22  LOAD_ATTR                co_code
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'eof'

 L.  28        28  LOAD_CONST               0
               30  STORE_FAST               'ptr'

 L.  29        32  LOAD_CONST               0
               34  STORE_FAST               'extended_arg'
             36_0  COME_FROM           162  '162'
             36_1  COME_FROM           134  '134'

 L.  31        36  LOAD_FAST                'ptr'
               38  LOAD_FAST                'eof'
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE   164  'to 164'

 L.  33        44  LOAD_FAST                'bytes'
               46  LOAD_FAST                'ptr'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'op'

 L.  35        52  LOAD_FAST                'op'
               54  LOAD_GLOBAL              dis
               56  LOAD_ATTR                HAVE_ARGUMENT
               58  COMPARE_OP               >=
               60  POP_JUMP_IF_FALSE   138  'to 138'

 L.  37        62  LOAD_FAST                'bytes'
               64  LOAD_FAST                'ptr'
               66  LOAD_CONST               1
               68  BINARY_ADD       
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'bytes'
               74  LOAD_FAST                'ptr'
               76  LOAD_CONST               2
               78  BINARY_ADD       
               80  BINARY_SUBSCR    
               82  LOAD_CONST               256
               84  BINARY_MULTIPLY  
               86  BINARY_ADD       
               88  LOAD_FAST                'extended_arg'
               90  BINARY_ADD       
               92  STORE_FAST               'arg'

 L.  38        94  LOAD_FAST                'ptr'
               96  LOAD_CONST               3
               98  INPLACE_ADD      
              100  STORE_FAST               'ptr'

 L.  40       102  LOAD_FAST                'op'
              104  LOAD_GLOBAL              dis
              106  LOAD_ATTR                EXTENDED_ARG
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   150  'to 150'

 L.  41       112  LOAD_GLOBAL              six
              114  LOAD_ATTR                integer_types
              116  LOAD_CONST               -1
              118  BINARY_SUBSCR    
              120  STORE_FAST               'long_type'

 L.  42       122  LOAD_FAST                'arg'
              124  LOAD_FAST                'long_type'
              126  LOAD_CONST               65536
              128  CALL_FUNCTION_1       1  ''
              130  BINARY_MULTIPLY  
              132  STORE_FAST               'extended_arg'

 L.  43       134  JUMP_BACK            36  'to 36'
              136  BREAK_LOOP          150  'to 150'
            138_0  COME_FROM            60  '60'

 L.  46       138  LOAD_CONST               None
              140  STORE_FAST               'arg'

 L.  47       142  LOAD_FAST                'ptr'
              144  LOAD_CONST               1
              146  INPLACE_ADD      
              148  STORE_FAST               'ptr'
            150_0  COME_FROM           136  '136'
            150_1  COME_FROM           110  '110'

 L.  49       150  LOAD_GLOBAL              OpArg
              152  LOAD_FAST                'op'
              154  LOAD_FAST                'arg'
              156  CALL_FUNCTION_2       2  ''
              158  YIELD_VALUE      
              160  POP_TOP          
              162  JUMP_BACK            36  'to 36'
            164_0  COME_FROM            42  '42'

Parse error at or near `JUMP_BACK' instruction at offset 162


    Bytecode = getattr(dis, 'Bytecode', Bytecode_compat)
    unescape = getattr(html, 'unescape', None)
    if unescape is None:
        unescape = html_parser.HTMLParser().unescape