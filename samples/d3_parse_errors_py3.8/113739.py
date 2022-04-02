# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\yaml\error.py
__all__ = ['Mark', 'YAMLError', 'MarkedYAMLError']

class Mark:

    def __init__(self, name, index, line, column, buffer, pointer):
        self.name = name
        self.index = index
        self.line = line
        self.column = column
        self.buffer = buffer
        self.pointer = pointer

    def get_snippet--- This code section failed: ---

 L.  15         0  LOAD_FAST                'self'
                2  LOAD_ATTR                buffer
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  16        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  17        14  LOAD_STR                 ''
               16  STORE_FAST               'head'

 L.  18        18  LOAD_FAST                'self'
               20  LOAD_ATTR                pointer
               22  STORE_FAST               'start'
             24_0  COME_FROM            94  '94'
             24_1  COME_FROM            78  '78'

 L.  19        24  LOAD_FAST                'start'
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE    96  'to 96'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                buffer
               36  LOAD_FAST                'start'
               38  LOAD_CONST               1
               40  BINARY_SUBTRACT  
               42  BINARY_SUBSCR    
               44  LOAD_STR                 '\x00\r\n\x85\u2028\u2029'
               46  COMPARE_OP               not-in
               48  POP_JUMP_IF_FALSE    96  'to 96'

 L.  20        50  LOAD_FAST                'start'
               52  LOAD_CONST               1
               54  INPLACE_SUBTRACT 
               56  STORE_FAST               'start'

 L.  21        58  LOAD_FAST                'self'
               60  LOAD_ATTR                pointer
               62  LOAD_FAST                'start'
               64  BINARY_SUBTRACT  
               66  LOAD_FAST                'max_length'
               68  LOAD_CONST               2
               70  BINARY_TRUE_DIVIDE
               72  LOAD_CONST               1
               74  BINARY_SUBTRACT  
               76  COMPARE_OP               >
               78  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L.  22        80  LOAD_STR                 ' ... '
               82  STORE_FAST               'head'

 L.  23        84  LOAD_FAST                'start'
               86  LOAD_CONST               5
               88  INPLACE_ADD      
               90  STORE_FAST               'start'

 L.  24        92  JUMP_FORWARD         96  'to 96'
               94  JUMP_BACK            24  'to 24'
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            48  '48'
             96_2  COME_FROM            30  '30'

 L.  25        96  LOAD_STR                 ''
               98  STORE_FAST               'tail'

 L.  26       100  LOAD_FAST                'self'
              102  LOAD_ATTR                pointer
              104  STORE_FAST               'end'
            106_0  COME_FROM           178  '178'
            106_1  COME_FROM           162  '162'

 L.  27       106  LOAD_FAST                'end'
              108  LOAD_GLOBAL              len
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                buffer
              114  CALL_FUNCTION_1       1  ''
              116  COMPARE_OP               <
              118  POP_JUMP_IF_FALSE   180  'to 180'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                buffer
              124  LOAD_FAST                'end'
              126  BINARY_SUBSCR    
              128  LOAD_STR                 '\x00\r\n\x85\u2028\u2029'
              130  COMPARE_OP               not-in
              132  POP_JUMP_IF_FALSE   180  'to 180'

 L.  28       134  LOAD_FAST                'end'
              136  LOAD_CONST               1
              138  INPLACE_ADD      
              140  STORE_FAST               'end'

 L.  29       142  LOAD_FAST                'end'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                pointer
              148  BINARY_SUBTRACT  
              150  LOAD_FAST                'max_length'
              152  LOAD_CONST               2
              154  BINARY_TRUE_DIVIDE
              156  LOAD_CONST               1
              158  BINARY_SUBTRACT  
              160  COMPARE_OP               >
              162  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L.  30       164  LOAD_STR                 ' ... '
              166  STORE_FAST               'tail'

 L.  31       168  LOAD_FAST                'end'
              170  LOAD_CONST               5
              172  INPLACE_SUBTRACT 
              174  STORE_FAST               'end'

 L.  32       176  JUMP_FORWARD        180  'to 180'
              178  JUMP_BACK           106  'to 106'
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           132  '132'
            180_2  COME_FROM           118  '118'

 L.  33       180  LOAD_FAST                'self'
              182  LOAD_ATTR                buffer
              184  LOAD_FAST                'start'
              186  LOAD_FAST                'end'
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  STORE_FAST               'snippet'

 L.  34       194  LOAD_STR                 ' '
              196  LOAD_FAST                'indent'
              198  BINARY_MULTIPLY  
              200  LOAD_FAST                'head'
              202  BINARY_ADD       
              204  LOAD_FAST                'snippet'
              206  BINARY_ADD       
              208  LOAD_FAST                'tail'
              210  BINARY_ADD       
              212  LOAD_STR                 '\n'
              214  BINARY_ADD       

 L.  35       216  LOAD_STR                 ' '
              218  LOAD_FAST                'indent'
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                pointer
              224  BINARY_ADD       
              226  LOAD_FAST                'start'
              228  BINARY_SUBTRACT  
              230  LOAD_GLOBAL              len
              232  LOAD_FAST                'head'
              234  CALL_FUNCTION_1       1  ''
              236  BINARY_ADD       
              238  BINARY_MULTIPLY  

 L.  34       240  BINARY_ADD       

 L.  35       242  LOAD_STR                 '^'

 L.  34       244  BINARY_ADD       
              246  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 94

    def __str__(self):
        snippet = self.get_snippet()
        where = '  in "%s", line %d, column %d' % (
         self.name, self.line + 1, self.column + 1)
        if snippet is not None:
            where += ':\n' + snippet
        return where


class YAMLError(Exception):
    pass


class MarkedYAMLError(YAMLError):

    def __init__(self, context=None, context_mark=None, problem=None, problem_mark=None, note=None):
        self.context = context
        self.context_mark = context_mark
        self.problem = problem
        self.problem_mark = problem_mark
        self.note = note

    def __str__(self):
        lines = []
        if self.context is not None:
            lines.append(self.context)
        if self.context_mark is not None:
            if self.problem is None or (self.problem_mark is None or self.context_mark.name != self.problem_mark.name or self.context_mark.line != self.problem_mark.line or self.context_mark.column != self.problem_mark.column):
                lines.append(str(self.context_mark))
            if self.problem is not None:
                lines.append(self.problem)
            if self.problem_mark is not None:
                lines.append(str(self.problem_mark))
            if self.note is not None:
                lines.append(self.note)
            return '\n'.join(lines)