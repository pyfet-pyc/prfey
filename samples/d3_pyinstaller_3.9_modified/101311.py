# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PaletteFile.py
from ._binary import o8

class PaletteFile:
    __doc__ = 'File handler for Teragon-style palette files.'
    rawmode = 'RGB'

    def __init__--- This code section failed: ---

 L.  26         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'PaletteFile.__init__.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_GLOBAL              range
                8  LOAD_CONST               256
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               palette
             20_0  COME_FROM           196  '196'
             20_1  COME_FROM           164  '164'
             20_2  COME_FROM           158  '158'
             20_3  COME_FROM            50  '50'

 L.  30        20  LOAD_FAST                'fp'
               22  LOAD_METHOD              readline
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               's'

 L.  32        28  LOAD_FAST                's'
               30  POP_JUMP_IF_TRUE     34  'to 34'

 L.  33        32  JUMP_FORWARD        198  'to 198'
             34_0  COME_FROM            30  '30'

 L.  34        34  LOAD_FAST                's'
               36  LOAD_CONST               0
               38  LOAD_CONST               1
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_CONST               b'#'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    52  'to 52'

 L.  35        50  JUMP_BACK            20  'to 20'
             52_0  COME_FROM            48  '48'

 L.  36        52  LOAD_GLOBAL              len
               54  LOAD_FAST                's'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_CONST               100
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L.  37        64  LOAD_GLOBAL              SyntaxError
               66  LOAD_STR                 'bad palette file'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'

 L.  39        72  LOAD_LISTCOMP            '<code_object <listcomp>>'
               74  LOAD_STR                 'PaletteFile.__init__.<locals>.<listcomp>'
               76  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               78  LOAD_FAST                's'
               80  LOAD_METHOD              split
               82  CALL_METHOD_0         0  ''
               84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'v'

 L.  40        90  SETUP_FINALLY       108  'to 108'

 L.  41        92  LOAD_FAST                'v'
               94  UNPACK_SEQUENCE_4     4 
               96  STORE_FAST               'i'
               98  STORE_FAST               'r'
              100  STORE_FAST               'g'
              102  STORE_FAST               'b'
              104  POP_BLOCK        
              106  JUMP_FORWARD        142  'to 142'
            108_0  COME_FROM_FINALLY    90  '90'

 L.  42       108  DUP_TOP          
              110  LOAD_GLOBAL              ValueError
              112  <121>               140  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  43       120  LOAD_FAST                'v'
              122  UNPACK_SEQUENCE_2     2 
              124  STORE_FAST               'i'
              126  STORE_FAST               'r'

 L.  44       128  LOAD_FAST                'r'
              130  DUP_TOP          
              132  STORE_FAST               'g'
              134  STORE_FAST               'b'
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM           106  '106'

 L.  46       142  LOAD_CONST               0
              144  LOAD_FAST                'i'
              146  DUP_TOP          
              148  ROT_THREE        
              150  COMPARE_OP               <=
              152  POP_JUMP_IF_FALSE   162  'to 162'
              154  LOAD_CONST               255
              156  COMPARE_OP               <=
              158  POP_JUMP_IF_FALSE_BACK    20  'to 20'
              160  JUMP_FORWARD        166  'to 166'
            162_0  COME_FROM           152  '152'
              162  POP_TOP          
              164  JUMP_BACK            20  'to 20'
            166_0  COME_FROM           160  '160'

 L.  47       166  LOAD_GLOBAL              o8
              168  LOAD_FAST                'r'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_GLOBAL              o8
              174  LOAD_FAST                'g'
              176  CALL_FUNCTION_1       1  ''
              178  BINARY_ADD       
              180  LOAD_GLOBAL              o8
              182  LOAD_FAST                'b'
              184  CALL_FUNCTION_1       1  ''
              186  BINARY_ADD       
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                palette
              192  LOAD_FAST                'i'
              194  STORE_SUBSCR     
              196  JUMP_BACK            20  'to 20'
            198_0  COME_FROM            32  '32'

 L.  49       198  LOAD_CONST               b''
              200  LOAD_METHOD              join
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                palette
              206  CALL_METHOD_1         1  ''
              208  LOAD_FAST                'self'
              210  STORE_ATTR               palette

Parse error at or near `<121>' instruction at offset 112

    def getpalette(self):
        return (
         self.palette, self.rawmode)