# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\view.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from .errors import UnexpectedQuoteError, InvalidEndOfQuotedStringError, ExpectedClosingQuoteError
_quotes = {'"':'"', 
 '‘':'’', 
 '‚':'‛', 
 '“':'”', 
 '„':'‟', 
 '⹂':'⹂', 
 '「':'」', 
 '『':'』', 
 '〝':'〞', 
 '﹁':'﹂', 
 '﹃':'﹄', 
 '＂':'＂', 
 '｢':'｣', 
 '«':'»', 
 '‹':'›', 
 '《':'》', 
 '〈':'〉'}
_all_quotes = set(_quotes.keys()) | set(_quotes.values())

class StringView:

    def __init__(self, buffer):
        self.index = 0
        self.buffer = buffer
        self.end = len(buffer)
        self.previous = 0

    @property
    def current(self):
        if self.eof:
            return
        return self.buffer[self.index]

    @property
    def eof(self):
        return self.index >= self.end

    def undo(self):
        self.index = self.previous

    def skip_ws--- This code section failed: ---

 L.  70         0  LOAD_CONST               0
                2  STORE_FAST               'pos'

 L.  71         4  LOAD_FAST                'self'
                6  LOAD_ATTR                eof
                8  POP_JUMP_IF_TRUE     78  'to 78'

 L.  72        10  SETUP_FINALLY        52  'to 52'

 L.  73        12  LOAD_FAST                'self'
               14  LOAD_ATTR                buffer
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                index
               20  LOAD_FAST                'pos'
               22  BINARY_ADD       
               24  BINARY_SUBSCR    
               26  STORE_FAST               'current'

 L.  74        28  LOAD_FAST                'current'
               30  LOAD_METHOD              isspace
               32  CALL_METHOD_0         0  ''
               34  POP_JUMP_IF_TRUE     40  'to 40'

 L.  75        36  POP_BLOCK        
               38  BREAK_LOOP           78  'to 78'
             40_0  COME_FROM            34  '34'

 L.  76        40  LOAD_FAST                'pos'
               42  LOAD_CONST               1
               44  INPLACE_ADD      
               46  STORE_FAST               'pos'
               48  POP_BLOCK        
               50  JUMP_BACK             4  'to 4'
             52_0  COME_FROM_FINALLY    10  '10'

 L.  77        52  DUP_TOP          
               54  LOAD_GLOBAL              IndexError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    74  'to 74'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  78        66  POP_EXCEPT       
               68  BREAK_LOOP           78  'to 78'
               70  POP_EXCEPT       
               72  JUMP_BACK             4  'to 4'
             74_0  COME_FROM            58  '58'
               74  END_FINALLY      
               76  JUMP_BACK             4  'to 4'
             78_0  COME_FROM_EXCEPT_CLAUSE    68  '68'
             78_1  COME_FROM_EXCEPT_CLAUSE     8  '8'

 L.  80        78  LOAD_FAST                'self'
               80  LOAD_ATTR                index
               82  LOAD_FAST                'self'
               84  STORE_ATTR               previous

 L.  81        86  LOAD_FAST                'self'
               88  DUP_TOP          
               90  LOAD_ATTR                index
               92  LOAD_FAST                'pos'
               94  INPLACE_ADD      
               96  ROT_TWO          
               98  STORE_ATTR               index

 L.  82       100  LOAD_FAST                'self'
              102  LOAD_ATTR                previous
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                index
              108  COMPARE_OP               !=
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 78_1

    def skip_string(self, string):
        strlen = len(string)
        if self.buffer[self.index:self.index + strlen] == string:
            self.previous = self.index
            self.index += strlen
            return True
        return False

    def read_rest(self):
        result = self.buffer[self.index:]
        self.previous = self.index
        self.index = self.end
        return result

    def read(self, n):
        result = self.buffer[self.index:self.index + n]
        self.previous = self.index
        self.index += n
        return result

    def get(self):
        try:
            result = self.buffer[(self.index + 1)]
        except IndexError:
            result = None
        else:
            self.previous = self.index
            self.index += 1
            return result

    def get_word--- This code section failed: ---

 L. 115         0  LOAD_CONST               0
                2  STORE_FAST               'pos'

 L. 116         4  LOAD_FAST                'self'
                6  LOAD_ATTR                eof
                8  POP_JUMP_IF_TRUE     78  'to 78'

 L. 117        10  SETUP_FINALLY        52  'to 52'

 L. 118        12  LOAD_FAST                'self'
               14  LOAD_ATTR                buffer
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                index
               20  LOAD_FAST                'pos'
               22  BINARY_ADD       
               24  BINARY_SUBSCR    
               26  STORE_FAST               'current'

 L. 119        28  LOAD_FAST                'current'
               30  LOAD_METHOD              isspace
               32  CALL_METHOD_0         0  ''
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 120        36  POP_BLOCK        
               38  BREAK_LOOP           78  'to 78'
             40_0  COME_FROM            34  '34'

 L. 121        40  LOAD_FAST                'pos'
               42  LOAD_CONST               1
               44  INPLACE_ADD      
               46  STORE_FAST               'pos'
               48  POP_BLOCK        
               50  JUMP_BACK             4  'to 4'
             52_0  COME_FROM_FINALLY    10  '10'

 L. 122        52  DUP_TOP          
               54  LOAD_GLOBAL              IndexError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    74  'to 74'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 123        66  POP_EXCEPT       
               68  BREAK_LOOP           78  'to 78'
               70  POP_EXCEPT       
               72  JUMP_BACK             4  'to 4'
             74_0  COME_FROM            58  '58'
               74  END_FINALLY      
               76  JUMP_BACK             4  'to 4'
             78_0  COME_FROM_EXCEPT_CLAUSE    68  '68'
             78_1  COME_FROM_EXCEPT_CLAUSE     8  '8'

 L. 124        78  LOAD_FAST                'self'
               80  LOAD_ATTR                index
               82  LOAD_FAST                'self'
               84  STORE_ATTR               previous

 L. 125        86  LOAD_FAST                'self'
               88  LOAD_ATTR                buffer
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                index
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                index
               98  LOAD_FAST                'pos'
              100  BINARY_ADD       
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  STORE_FAST               'result'

 L. 126       108  LOAD_FAST                'self'
              110  DUP_TOP          
              112  LOAD_ATTR                index
              114  LOAD_FAST                'pos'
              116  INPLACE_ADD      
              118  ROT_TWO          
              120  STORE_ATTR               index

 L. 127       122  LOAD_FAST                'result'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 78_1

    def get_quoted_word(self):
        current = self.current
        if current is None:
            return
        close_quote = _quotes.get(current)
        is_quoted = bool(close_quote)
        if is_quoted:
            result = []
            _escaped_quotes = (
             current, close_quote)
        else:
            result = [
             current]
            _escaped_quotes = _all_quotes
            while not self.eof:
                current = self.get()
                if not current:
                    if is_quoted:
                        raise ExpectedClosingQuoteError(close_quote)
                    return ''.join(result)
                    if current == '\\':
                        next_char = self.get()
                        if not next_char:
                            if is_quoted:
                                raise ExpectedClosingQuoteError(close_quote)
                            return ''.join(result)
                        if next_char in _escaped_quotes:
                            result.append(next_char)
                    else:
                        self.undo()
                        result.append(current)
                elif not is_quoted:
                    if current in _all_quotes:
                        raise UnexpectedQuoteError(current)
                    elif is_quoted and current == close_quote:
                        next_char = self.get()
                        valid_eof = not next_char or next_char.isspace()
                        if not valid_eof:
                            raise InvalidEndOfQuotedStringError(next_char)
                        return ''.join(result)
                    if current.isspace():
                        if not is_quoted:
                            return ''.join(result)
                    result.append(current)

    def __repr__(self):
        return '<StringView pos: {0.index} prev: {0.previous} end: {0.end} eof: {0.eof}>'.format(self)