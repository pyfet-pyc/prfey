# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: lib2to3\pgen2\literals.py
"""Safely evaluate Python string literals without using eval()."""
import re
simple_escapes = {'a':'\x07', 
 'b':'\x08', 
 'f':'\x0c', 
 'n':'\n', 
 'r':'\r', 
 't':'\t', 
 'v':'\x0b', 
 "'":"'", 
 '"':'"', 
 '\\':'\\'}

def escape--- This code section failed: ---

 L.  20         0  LOAD_FAST                'm'
                2  LOAD_METHOD              group
                4  LOAD_CONST               0
                6  LOAD_CONST               1
                8  CALL_METHOD_2         2  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'all'
               14  STORE_FAST               'tail'

 L.  21        16  LOAD_FAST                'all'
               18  LOAD_METHOD              startswith
               20  LOAD_STR                 '\\'
               22  CALL_METHOD_1         1  ''
               24  POP_JUMP_IF_TRUE     30  'to 30'
               26  <74>             
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            24  '24'

 L.  22        30  LOAD_GLOBAL              simple_escapes
               32  LOAD_METHOD              get
               34  LOAD_FAST                'tail'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'esc'

 L.  23        40  LOAD_FAST                'esc'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L.  24        48  LOAD_FAST                'esc'
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L.  25        52  LOAD_FAST                'tail'
               54  LOAD_METHOD              startswith
               56  LOAD_STR                 'x'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE   148  'to 148'

 L.  26        62  LOAD_FAST                'tail'
               64  LOAD_CONST               1
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  STORE_FAST               'hexes'

 L.  27        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'hexes'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_CONST               2
               82  COMPARE_OP               <
               84  POP_JUMP_IF_FALSE    98  'to 98'

 L.  28        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 "invalid hex string escape ('\\%s')"
               90  LOAD_FAST                'tail'
               92  BINARY_MODULO    
               94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            84  '84'

 L.  29        98  SETUP_FINALLY       114  'to 114'

 L.  30       100  LOAD_GLOBAL              int
              102  LOAD_FAST                'hexes'
              104  LOAD_CONST               16
              106  CALL_FUNCTION_2       2  ''
              108  STORE_FAST               'i'
              110  POP_BLOCK        
              112  JUMP_FORWARD        196  'to 196'
            114_0  COME_FROM_FINALLY    98  '98'

 L.  31       114  DUP_TOP          
              116  LOAD_GLOBAL              ValueError
              118  <121>               144  ''
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L.  32       126  LOAD_GLOBAL              ValueError
              128  LOAD_STR                 "invalid hex string escape ('\\%s')"
              130  LOAD_FAST                'tail'
              132  BINARY_MODULO    
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_CONST               None
              138  RAISE_VARARGS_2       2  'exception instance with __cause__'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        196  'to 196'
              144  <48>             
              146  JUMP_FORWARD        196  'to 196'
            148_0  COME_FROM            60  '60'

 L.  34       148  SETUP_FINALLY       164  'to 164'

 L.  35       150  LOAD_GLOBAL              int
              152  LOAD_FAST                'tail'
              154  LOAD_CONST               8
              156  CALL_FUNCTION_2       2  ''
              158  STORE_FAST               'i'
              160  POP_BLOCK        
              162  JUMP_FORWARD        196  'to 196'
            164_0  COME_FROM_FINALLY   148  '148'

 L.  36       164  DUP_TOP          
              166  LOAD_GLOBAL              ValueError
              168  <121>               194  ''
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L.  37       176  LOAD_GLOBAL              ValueError
              178  LOAD_STR                 "invalid octal string escape ('\\%s')"
              180  LOAD_FAST                'tail'
              182  BINARY_MODULO    
              184  CALL_FUNCTION_1       1  ''
              186  LOAD_CONST               None
              188  RAISE_VARARGS_2       2  'exception instance with __cause__'
              190  POP_EXCEPT       
              192  JUMP_FORWARD        196  'to 196'
              194  <48>             
            196_0  COME_FROM           192  '192'
            196_1  COME_FROM           162  '162'
            196_2  COME_FROM           146  '146'
            196_3  COME_FROM           142  '142'
            196_4  COME_FROM           112  '112'

 L.  38       196  LOAD_GLOBAL              chr
              198  LOAD_FAST                'i'
              200  CALL_FUNCTION_1       1  ''
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 26


def evalString--- This code section failed: ---

 L.  41         0  LOAD_FAST                's'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 "'"
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     40  'to 40'
               10  LOAD_FAST                's'
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 '"'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     40  'to 40'
               20  <74>             
               22  LOAD_GLOBAL              repr
               24  LOAD_FAST                's'
               26  LOAD_CONST               None
               28  LOAD_CONST               1
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            18  '18'
             40_1  COME_FROM             8  '8'

 L.  42        40  LOAD_FAST                's'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  STORE_FAST               'q'

 L.  43        48  LOAD_FAST                's'
               50  LOAD_CONST               None
               52  LOAD_CONST               3
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'q'
               60  LOAD_CONST               3
               62  BINARY_MULTIPLY  
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L.  44        68  LOAD_FAST                'q'
               70  LOAD_CONST               3
               72  BINARY_MULTIPLY  
               74  STORE_FAST               'q'
             76_0  COME_FROM            66  '66'

 L.  45        76  LOAD_FAST                's'
               78  LOAD_METHOD              endswith
               80  LOAD_FAST                'q'
               82  CALL_METHOD_1         1  ''
               84  POP_JUMP_IF_TRUE    112  'to 112'
               86  <74>             
               88  LOAD_GLOBAL              repr
               90  LOAD_FAST                's'
               92  LOAD_GLOBAL              len
               94  LOAD_FAST                'q'
               96  CALL_FUNCTION_1       1  ''
               98  UNARY_NEGATIVE   
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_1       1  ''
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            84  '84'

 L.  46       112  LOAD_GLOBAL              len
              114  LOAD_FAST                's'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_CONST               2
              120  LOAD_GLOBAL              len
              122  LOAD_FAST                'q'
              124  CALL_FUNCTION_1       1  ''
              126  BINARY_MULTIPLY  
              128  COMPARE_OP               >=
              130  POP_JUMP_IF_TRUE    136  'to 136'
              132  <74>             
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           130  '130'

 L.  47       136  LOAD_FAST                's'
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'q'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'q'
              148  CALL_FUNCTION_1       1  ''
              150  UNARY_NEGATIVE   
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  STORE_FAST               's'

 L.  48       158  LOAD_GLOBAL              re
              160  LOAD_METHOD              sub
              162  LOAD_STR                 '\\\\(\\\'|\\"|\\\\|[abfnrtv]|x.{0,2}|[0-7]{1,3})'
              164  LOAD_GLOBAL              escape
              166  LOAD_FAST                's'
              168  CALL_METHOD_3         3  ''
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def test():
    for i in range(256):
        c = chr(i)
        s = repr(c)
        e = evalString(s)
        if e != c:
            print(i, c, s, e)


if __name__ == '__main__':
    test()