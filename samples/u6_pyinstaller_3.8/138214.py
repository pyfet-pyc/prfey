# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\lineeditor\history.py
from __future__ import print_function, unicode_literals, absolute_import
import re, operator, string, sys, os
from pyreadline.unicode_helper import ensure_unicode, ensure_str
if 'pyreadline' in sys.modules:
    pyreadline = sys.modules['pyreadline']
else:
    import pyreadline
from . import lineobj

class EscapeHistory(Exception):
    pass


from pyreadline.logger import log

class LineHistory(object):

    def __init__(self):
        self.history = []
        self._history_length = 100
        self._history_cursor = 0
        self.history_filename = os.path.expanduser(ensure_str('~/.history'))
        self.lastcommand = None
        self.query = ''
        self.last_search_for = ''

    def get_current_history_length(self):
        """Return the number of lines currently in the history.
        (This is different from get_history_length(), which returns 
        the maximum number of lines that will be written to a history file.)"""
        value = len(self.history)
        log('get_current_history_length:%d' % value)
        return value

    def get_history_length(self):
        """Return the desired length of the history file. Negative values imply
        unlimited history file size."""
        value = self._history_length
        log('get_history_length:%d' % value)
        return value

    def get_history_item(self, index):
        """Return the current contents of history item at index (starts with index 1)."""
        item = self.history[(index - 1)]
        log('get_history_item: index:%d item:%r' % (index, item))
        return item.get_line_text()

    def set_history_length(self, value):
        log('set_history_length: old:%d new:%d' % (self._history_length, value))
        self._history_length = value

    def get_history_cursor(self):
        value = self._history_cursor
        log('get_history_cursor:%d' % value)
        return value

    def set_history_cursor(self, value):
        log('set_history_cursor: old:%d new:%d' % (self._history_cursor, value))
        self._history_cursor = value

    history_length = property(get_history_length, set_history_length)
    history_cursor = property(get_history_cursor, set_history_cursor)

    def clear_history(self):
        """Clear readline history."""
        self.history[:] = []
        self.history_cursor = 0

    def read_history_file(self, filename=None):
        """Load a readline history file."""
        if filename is None:
            filename = self.history_filename
        try:
            for line in open(filename, 'r'):
                self.add_history(lineobj.ReadLineTextBuffer(ensure_unicode(line.rstrip())))

        except IOError:
            self.history = []
            self.history_cursor = 0

    def write_history_file(self, filename=None):
        """Save a readline history file."""
        if filename is None:
            filename = self.history_filename
        fp = open(filename, 'wb')
        for line in self.history[-self.history_length:]:
            fp.write(ensure_str(line.get_line_text()))
            fp.write('\n'.encode('ascii'))
        else:
            fp.close()

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed."""
        line = ensure_unicode(line)
        if not hasattr(line, 'get_line_text'):
            line = lineobj.ReadLineTextBuffer(line)
        if not line.get_line_text():
            pass
        else:
            if len(self.history) > 0 and self.history[(-1)].get_line_text() == line.get_line_text():
                pass
            else:
                self.history.append(line)
            self.history_cursor = len(self.history)

    def previous_history(self, current):
        """Move back through the history list, fetching the previous command. """
        if self.history_cursor == len(self.history):
            self.history.append(current.copy())
        if self.history_cursor > 0:
            self.history_cursor -= 1
            current.set_line(self.history[self.history_cursor].get_line_text())
            current.point = lineobj.EndOfLine

    def next_history(self, current):
        """Move forward through the history list, fetching the next command. """
        if self.history_cursor < len(self.history) - 1:
            self.history_cursor += 1
            current.set_line(self.history[self.history_cursor].get_line_text())

    def beginning_of_history(self):
        """Move to the first line in the history."""
        self.history_cursor = 0
        if len(self.history) > 0:
            self.l_buffer = self.history[0]

    def end_of_history(self, current):
        """Move to the end of the input history, i.e., the line currently
        being entered."""
        self.history_cursor = len(self.history)
        current.set_line(self.history[(-1)].get_line_text())

    def reverse_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = self.history_cursor
        origpos = startpos
        result = lineobj.ReadLineTextBuffer('')
        for idx, line in list(enumerate(self.history))[startpos:0:-1]:
            if searchfor in line:
                startpos = idx
                break
            if self.last_search_for == searchfor and startpos > 0:
                startpos -= 1
                for idx, line in list(enumerate(self.history))[startpos:0:-1]:
                    if searchfor in line:
                        startpos = idx
                        break

            else:
                if self.history:
                    result = self.history[startpos].get_line_text()
                else:
                    result = ''
                self.history_cursor = startpos
                self.last_search_for = searchfor
                log('reverse_search_history: old:%d new:%d result:%r' % (origpos, self.history_cursor, result))
                return result

    def forward_search_history(self, searchfor, startpos=None):
        if startpos is None:
            startpos = min(self.history_cursor, max(0, self.get_current_history_length() - 1))
        origpos = startpos
        result = lineobj.ReadLineTextBuffer('')
        for idx, line in list(enumerate(self.history))[startpos:]:
            if searchfor in line:
                startpos = idx
                break
            if self.last_search_for == searchfor and startpos < self.get_current_history_length() - 1:
                startpos += 1
                for idx, line in list(enumerate(self.history))[startpos:]:
                    if searchfor in line:
                        startpos = idx
                        break

            else:
                if self.history:
                    result = self.history[startpos].get_line_text()
                else:
                    result = ''
                self.history_cursor = startpos
                self.last_search_for = searchfor
                return result

    def _search--- This code section failed: ---

 L. 200       0_2  SETUP_FINALLY       448  'to 448'

 L. 201         4  LOAD_FAST                'self'
                6  LOAD_ATTR                lastcommand
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                history_search_forward
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    54  'to 54'

 L. 202        16  LOAD_FAST                'self'
               18  LOAD_ATTR                lastcommand
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                history_search_backward
               24  COMPARE_OP               !=

 L. 201        26  POP_JUMP_IF_FALSE    54  'to 54'

 L. 203        28  LOAD_STR                 ''
               30  LOAD_METHOD              join
               32  LOAD_FAST                'partial'
               34  LOAD_CONST               0
               36  LOAD_FAST                'partial'
               38  LOAD_ATTR                point
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              get_line_text
               46  CALL_METHOD_0         0  ''
               48  CALL_METHOD_1         1  ''
               50  LOAD_FAST                'self'
               52  STORE_ATTR               query
             54_0  COME_FROM            26  '26'
             54_1  COME_FROM            14  '14'

 L. 204        54  LOAD_GLOBAL              max
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                history_cursor
               60  LOAD_CONST               0
               62  CALL_FUNCTION_2       2  ''
               64  STORE_FAST               'hcstart'

 L. 205        66  LOAD_FAST                'self'
               68  LOAD_ATTR                history_cursor
               70  LOAD_FAST                'direction'
               72  BINARY_ADD       
               74  STORE_FAST               'hc'

 L. 206        76  LOAD_FAST                'direction'
               78  LOAD_CONST               0
               80  COMPARE_OP               <
               82  POP_JUMP_IF_FALSE    92  'to 92'
               84  LOAD_FAST                'hc'
               86  LOAD_CONST               0
               88  COMPARE_OP               >=
               90  POP_JUMP_IF_TRUE    114  'to 114'
             92_0  COME_FROM            82  '82'
               92  LOAD_FAST                'direction'
               94  LOAD_CONST               0
               96  COMPARE_OP               >
               98  POP_JUMP_IF_FALSE   230  'to 230'
              100  LOAD_FAST                'hc'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                history
              108  CALL_FUNCTION_1       1  ''
              110  COMPARE_OP               <
              112  POP_JUMP_IF_FALSE   230  'to 230'
            114_0  COME_FROM            90  '90'

 L. 207       114  LOAD_FAST                'self'
              116  LOAD_ATTR                history
              118  LOAD_FAST                'hc'
              120  BINARY_SUBSCR    
              122  STORE_FAST               'h'

 L. 208       124  LOAD_FAST                'self'
              126  LOAD_ATTR                query
              128  POP_JUMP_IF_TRUE    164  'to 164'

 L. 209       130  LOAD_FAST                'hc'
              132  LOAD_FAST                'self'
              134  STORE_ATTR               history_cursor

 L. 210       136  LOAD_GLOBAL              lineobj
              138  LOAD_ATTR                ReadLineTextBuffer
              140  LOAD_FAST                'h'
              142  LOAD_GLOBAL              len
              144  LOAD_FAST                'h'
              146  LOAD_METHOD              get_line_text
              148  CALL_METHOD_0         0  ''
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               ('point',)
              154  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              156  STORE_FAST               'result'

 L. 211       158  LOAD_FAST                'result'
              160  POP_BLOCK        
              162  RETURN_VALUE     
            164_0  COME_FROM           128  '128'

 L. 212       164  LOAD_FAST                'h'
              166  LOAD_METHOD              get_line_text
              168  CALL_METHOD_0         0  ''
              170  LOAD_METHOD              startswith
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                query
              176  CALL_METHOD_1         1  ''
              178  POP_JUMP_IF_FALSE   220  'to 220'
              180  LOAD_FAST                'h'
              182  LOAD_FAST                'partial'
              184  LOAD_METHOD              get_line_text
              186  CALL_METHOD_0         0  ''
              188  COMPARE_OP               !=
              190  POP_JUMP_IF_FALSE   220  'to 220'

 L. 213       192  LOAD_FAST                'hc'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               history_cursor

 L. 214       198  LOAD_GLOBAL              lineobj
              200  LOAD_ATTR                ReadLineTextBuffer
              202  LOAD_FAST                'h'
              204  LOAD_FAST                'partial'
              206  LOAD_ATTR                point
              208  LOAD_CONST               ('point',)
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  STORE_FAST               'result'

 L. 215       214  LOAD_FAST                'result'
              216  POP_BLOCK        
              218  RETURN_VALUE     
            220_0  COME_FROM           190  '190'
            220_1  COME_FROM           178  '178'

 L. 216       220  LOAD_FAST                'hc'
              222  LOAD_FAST                'direction'
              224  INPLACE_ADD      
              226  STORE_FAST               'hc'
              228  JUMP_BACK            76  'to 76'
            230_0  COME_FROM           112  '112'
            230_1  COME_FROM            98  '98'

 L. 218       230  LOAD_GLOBAL              len
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                history
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_CONST               0
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   246  'to 246'

 L. 219       244  JUMP_FORWARD        416  'to 416'
            246_0  COME_FROM           242  '242'

 L. 220       246  LOAD_FAST                'hc'
              248  LOAD_GLOBAL              len
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                history
              254  CALL_FUNCTION_1       1  ''
              256  COMPARE_OP               >=
          258_260  POP_JUMP_IF_FALSE   298  'to 298'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                query
          266_268  POP_JUMP_IF_TRUE    298  'to 298'

 L. 221       270  LOAD_GLOBAL              len
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                history
              276  CALL_FUNCTION_1       1  ''
              278  LOAD_FAST                'self'
              280  STORE_ATTR               history_cursor

 L. 222       282  LOAD_GLOBAL              lineobj
              284  LOAD_ATTR                ReadLineTextBuffer
              286  LOAD_STR                 ''
              288  LOAD_CONST               0
              290  LOAD_CONST               ('point',)
              292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              294  POP_BLOCK        
              296  RETURN_VALUE     
            298_0  COME_FROM           266  '266'
            298_1  COME_FROM           258  '258'

 L. 223       298  LOAD_FAST                'self'
              300  LOAD_ATTR                history
              302  LOAD_GLOBAL              max
              304  LOAD_GLOBAL              min
              306  LOAD_FAST                'hcstart'
              308  LOAD_GLOBAL              len
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                history
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_CONST               1
              318  BINARY_SUBTRACT  
              320  CALL_FUNCTION_2       2  ''
              322  LOAD_CONST               0
              324  CALL_FUNCTION_2       2  ''
              326  BINARY_SUBSCR    
              328  LOAD_METHOD              get_line_text
              330  CALL_METHOD_0         0  ''
              332  LOAD_METHOD              startswith

 L. 224       334  LOAD_FAST                'self'
              336  LOAD_ATTR                query

 L. 223       338  CALL_METHOD_1         1  ''
          340_342  POP_JUMP_IF_FALSE   398  'to 398'

 L. 224       344  LOAD_FAST                'self'
              346  LOAD_ATTR                query

 L. 223   348_350  POP_JUMP_IF_FALSE   398  'to 398'

 L. 225       352  LOAD_GLOBAL              lineobj
              354  LOAD_ATTR                ReadLineTextBuffer
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                history

 L. 226       360  LOAD_GLOBAL              max
              362  LOAD_GLOBAL              min
              364  LOAD_FAST                'hcstart'
              366  LOAD_GLOBAL              len
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                history
              372  CALL_FUNCTION_1       1  ''
              374  LOAD_CONST               1
              376  BINARY_SUBTRACT  
              378  CALL_FUNCTION_2       2  ''
              380  LOAD_CONST               0
              382  CALL_FUNCTION_2       2  ''

 L. 225       384  BINARY_SUBSCR    

 L. 227       386  LOAD_FAST                'partial'
              388  LOAD_ATTR                point

 L. 225       390  LOAD_CONST               ('point',)
              392  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              394  POP_BLOCK        
              396  RETURN_VALUE     
            398_0  COME_FROM           348  '348'
            398_1  COME_FROM           340  '340'

 L. 229       398  LOAD_GLOBAL              lineobj
              400  LOAD_ATTR                ReadLineTextBuffer
              402  LOAD_FAST                'partial'

 L. 230       404  LOAD_FAST                'partial'
              406  LOAD_ATTR                point

 L. 229       408  LOAD_CONST               ('point',)
              410  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              412  POP_BLOCK        
              414  RETURN_VALUE     
            416_0  COME_FROM           244  '244'

 L. 231       416  LOAD_GLOBAL              lineobj
              418  LOAD_ATTR                ReadLineTextBuffer
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                query

 L. 232       424  LOAD_GLOBAL              min
              426  LOAD_GLOBAL              len
              428  LOAD_FAST                'self'
              430  LOAD_ATTR                query
              432  CALL_FUNCTION_1       1  ''

 L. 233       434  LOAD_FAST                'partial'
              436  LOAD_ATTR                point

 L. 232       438  CALL_FUNCTION_2       2  ''

 L. 231       440  LOAD_CONST               ('point',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  POP_BLOCK        
              446  RETURN_VALUE     
            448_0  COME_FROM_FINALLY     0  '0'

 L. 234       448  DUP_TOP          
              450  LOAD_GLOBAL              IndexError
              452  COMPARE_OP               exception-match
          454_456  POP_JUMP_IF_FALSE   470  'to 470'
              458  POP_TOP          
              460  POP_TOP          
              462  POP_TOP          

 L. 235       464  RAISE_VARARGS_0       0  'reraise'
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
            470_0  COME_FROM           454  '454'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'

Parse error at or near `POP_TOP' instruction at offset 460

    def history_search_forward(self, partial):
        """Search forward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""
        q = self._search(1, partial)
        return q

    def history_search_backward(self, partial):
        """Search backward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""
        q = self._search(-1, partial)
        return q


if __name__ == '__main__':
    q = LineHistory()
    r = LineHistory()
    s = LineHistory()
    RL = lineobj.ReadLineTextBuffer
    q.add_history(RL('aaaa'))
    q.add_history(RL('aaba'))
    q.add_history(RL('aaca'))
    q.add_history(RL('akca'))
    q.add_history(RL('bbb'))
    q.add_history(RL('ako'))
    r.add_history(RL('ako'))