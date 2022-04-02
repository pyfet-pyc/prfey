# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\modes\basemode.py
from __future__ import print_function, unicode_literals, absolute_import
import os, re, math, glob, sys, time
from pyreadline.py3k_compat import callable
import pyreadline.logger as logger
from pyreadline.logger import log
from pyreadline.keysyms.common import make_KeyPress_from_keydescr
import pyreadline.lineeditor.lineobj as lineobj
import pyreadline.lineeditor.history as history
import pyreadline.clipboard as clipboard
from pyreadline.error import ReadlineError, GetSetError
from pyreadline.unicode_helper import ensure_str, ensure_unicode
in_ironpython = 'IronPython' in sys.version

class BaseMode(object):
    mode = 'base'

    def __init__(self, rlobj):
        self.argument = 0
        self.rlobj = rlobj
        self.exit_dispatch = {}
        self.key_dispatch = {}
        self.argument = 1
        self.prevargument = None
        self.l_buffer = lineobj.ReadLineTextBuffer('')
        self._history = history.LineHistory()
        self.completer_delims = ' \t\n"\\\'`@$><=;|&{('
        self.show_all_if_ambiguous = 'on'
        self.mark_directories = 'on'
        self.complete_filesystem = 'off'
        self.completer = None
        self.begidx = 0
        self.endidx = 0
        self.tabstop = 4
        self.startup_hook = None
        self.pre_input_hook = None
        self.first_prompt = True
        self.cursor_size = 25
        self.prompt = '>>> '
        self.enable_ipython_paste_for_paths = True
        self.enable_ipython_paste_list_of_lists = True
        self.enable_win32_clipboard = True
        self.paste_line_buffer = []
        self._sub_modes = []

    def __repr__(self):
        return '<BaseMode>'

    def _gs(x):

        def g(self):
            return getattr(self.rlobj, x)

        def s(self, q):
            setattr(self.rlobj, x, q)

        return (
         g, s)

    def _g(x):

        def g(self):
            return getattr(self.rlobj, x)

        return g

    def _argreset(self):
        val = self.argument
        self.argument = 0
        if val == 0:
            val = 1
        return val

    argument_reset = property(_argreset)
    ctrl_c_tap_time_interval = property(*_gs('ctrl_c_tap_time_interval'))
    allow_ctrl_c = property(*_gs('allow_ctrl_c'))
    _print_prompt = property(_g('_print_prompt'))
    _update_line = property(_g('_update_line'))
    console = property(_g('console'))
    prompt_begin_pos = property(_g('prompt_begin_pos'))
    prompt_end_pos = property(_g('prompt_end_pos'))
    _bell = property(_g('_bell'))
    bell_style = property(_g('bell_style'))
    _clear_after = property(_g('_clear_after'))
    _update_prompt_pos = property(_g('_update_prompt_pos'))

    def process_keyevent(self, keyinfo):
        raise NotImplementedError

    def readline_setup(self, prompt=''):
        self.l_buffer.selection_mark = -1
        if self.first_prompt:
            self.first_prompt = False
            if self.startup_hook:
                try:
                    self.startup_hook()
                except:
                    print('startup hook failed')
                    traceback.print_exc()
                else:
                    self.l_buffer.reset_line()
                    self.prompt = prompt
                    if self.pre_input_hook:
                        try:
                            self.pre_input_hook()
                        except:
                            print('pre_input_hook failed')
                            traceback.print_exc()
                            self.pre_input_hook = None

    def finalize(self):
        """Every bindable command should call this function for cleanup. 
        Except those that want to set argument to a non-zero value.
        """
        self.argument = 0

    def add_history(self, text):
        self._history.add_history(lineobj.ReadLineTextBuffer(text))

    def rl_settings_to_string(self):
        out = [
         '%-20s: %s' % ('show all if ambigous', self.show_all_if_ambiguous)]
        out.append('%-20s: %s' % ('mark_directories', self.mark_directories))
        out.append('%-20s: %s' % ('bell_style', self.bell_style))
        out.append('------------- key bindings ------------')
        tablepat = '%-7s %-7s %-7s %-15s %-15s '
        out.append(tablepat % ('Control', 'Meta', 'Shift', 'Keycode/char', 'Function'))
        bindings = [(k[0], k[1], k[2], k[3], v.__name__) for k, v in self.key_dispatch.items()]
        bindings.sort()
        for key in bindings:
            out.append(tablepat % key)
        else:
            return out

    def _bind_key(self, key, func):
        """setup the mapping from key to call the function."""
        if not callable(func):
            print('Trying to bind non method to keystroke:%s,%s' % (key, func))
            raise ReadlineError('Trying to bind non method to keystroke:%s,%s,%s,%s' % (key, func, type(func), type(self._bind_key)))
        keyinfo = make_KeyPress_from_keydescr(key.lower()).tuple()
        log('>>>%s -> %s<<<' % (keyinfo, func.__name__))
        self.key_dispatch[keyinfo] = func

    def _bind_exit_key(self, key):
        """setup the mapping from key to call the function."""
        keyinfo = make_KeyPress_from_keydescr(key.lower()).tuple()
        self.exit_dispatch[keyinfo] = None

    def init_editing_mode(self, e):
        """When in vi command mode, this causes a switch to emacs editing
        mode."""
        raise NotImplementedError

    def _get_completions--- This code section failed: ---

 L. 184         0  BUILD_LIST_0          0 
                2  STORE_FAST               'completions'

 L. 185         4  LOAD_FAST                'self'
                6  LOAD_ATTR                l_buffer
                8  LOAD_ATTR                point
               10  LOAD_FAST                'self'
               12  STORE_ATTR               begidx

 L. 186        14  LOAD_FAST                'self'
               16  LOAD_ATTR                l_buffer
               18  LOAD_ATTR                point
               20  LOAD_FAST                'self'
               22  STORE_ATTR               endidx

 L. 187        24  LOAD_FAST                'self'
               26  LOAD_ATTR                l_buffer
               28  LOAD_ATTR                line_buffer
               30  STORE_FAST               'buf'

 L. 188        32  LOAD_FAST                'self'
               34  LOAD_ATTR                completer
            36_38  POP_JUMP_IF_FALSE   258  'to 258'
             40_0  COME_FROM            96  '96'
             40_1  COME_FROM            78  '78'

 L. 190        40  LOAD_FAST                'self'
               42  LOAD_ATTR                begidx
               44  LOAD_CONST               0
               46  COMPARE_OP               >
               48  POP_JUMP_IF_FALSE    98  'to 98'

 L. 191        50  LOAD_FAST                'self'
               52  DUP_TOP          
               54  LOAD_ATTR                begidx
               56  LOAD_CONST               1
               58  INPLACE_SUBTRACT 
               60  ROT_TWO          
               62  STORE_ATTR               begidx

 L. 192        64  LOAD_FAST                'buf'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                begidx
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                completer_delims
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L. 193        80  LOAD_FAST                'self'
               82  DUP_TOP          
               84  LOAD_ATTR                begidx
               86  LOAD_CONST               1
               88  INPLACE_ADD      
               90  ROT_TWO          
               92  STORE_ATTR               begidx

 L. 194        94  JUMP_FORWARD         98  'to 98'
               96  JUMP_BACK            40  'to 40'
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            48  '48'

 L. 195        98  LOAD_GLOBAL              ensure_str
              100  LOAD_STR                 ''
              102  LOAD_METHOD              join
              104  LOAD_FAST                'buf'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                begidx
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                endidx
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_METHOD_1         1  ''
              120  CALL_FUNCTION_1       1  ''
              122  STORE_FAST               'text'

 L. 196       124  LOAD_GLOBAL              log
              126  LOAD_STR                 'complete text="%s"'
              128  LOAD_GLOBAL              ensure_unicode
              130  LOAD_FAST                'text'
              132  CALL_FUNCTION_1       1  ''
              134  BINARY_MODULO    
              136  CALL_FUNCTION_1       1  ''
              138  POP_TOP          

 L. 197       140  LOAD_CONST               0
              142  STORE_FAST               'i'
            144_0  COME_FROM           234  '234'
            144_1  COME_FROM           232  '232'
            144_2  COME_FROM           220  '220'
            144_3  COME_FROM           212  '212'
            144_4  COME_FROM           208  '208'

 L. 199       144  SETUP_FINALLY       166  'to 166'

 L. 200       146  LOAD_FAST                'self'
              148  LOAD_METHOD              completer
              150  LOAD_GLOBAL              ensure_unicode
              152  LOAD_FAST                'text'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_FAST                'i'
              158  CALL_METHOD_2         2  ''
              160  STORE_FAST               'r'
              162  POP_BLOCK        
              164  JUMP_FORWARD        190  'to 190'
            166_0  COME_FROM_FINALLY   144  '144'

 L. 201       166  DUP_TOP          
              168  LOAD_GLOBAL              IndexError
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   188  'to 188'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 202       180  POP_EXCEPT       
              182  BREAK_LOOP          236  'to 236'
              184  POP_EXCEPT       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           172  '172'
              188  END_FINALLY      
            190_0  COME_FROM           186  '186'
            190_1  COME_FROM           164  '164'

 L. 203       190  LOAD_FAST                'i'
              192  LOAD_CONST               1
              194  INPLACE_ADD      
              196  STORE_FAST               'i'

 L. 204       198  LOAD_FAST                'r'
              200  LOAD_CONST               None
              202  COMPARE_OP               is
              204  POP_JUMP_IF_FALSE   210  'to 210'

 L. 205       206  JUMP_FORWARD        236  'to 236'
              208  JUMP_BACK           144  'to 144'
            210_0  COME_FROM           204  '204'

 L. 206       210  LOAD_FAST                'r'
              212  POP_JUMP_IF_FALSE_BACK   144  'to 144'
              214  LOAD_FAST                'r'
              216  LOAD_FAST                'completions'
              218  COMPARE_OP               not-in
              220  POP_JUMP_IF_FALSE_BACK   144  'to 144'

 L. 207       222  LOAD_FAST                'completions'
              224  LOAD_METHOD              append
              226  LOAD_FAST                'r'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  BREAK_LOOP          144  'to 144'

 L. 209       234  JUMP_BACK           144  'to 144'
            236_0  COME_FROM           206  '206'
            236_1  COME_FROM           182  '182'

 L. 210       236  LOAD_GLOBAL              log
              238  LOAD_STR                 'text completions=<%s>'
              240  LOAD_GLOBAL              list
              242  LOAD_GLOBAL              map
              244  LOAD_GLOBAL              ensure_unicode
              246  LOAD_FAST                'completions'
              248  CALL_FUNCTION_2       2  ''
              250  CALL_FUNCTION_1       1  ''
              252  BINARY_MODULO    
              254  CALL_FUNCTION_1       1  ''
              256  POP_TOP          
            258_0  COME_FROM            36  '36'

 L. 211       258  LOAD_FAST                'self'
              260  LOAD_ATTR                complete_filesystem
              262  LOAD_STR                 'on'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   516  'to 516'
              270  LOAD_FAST                'completions'
          272_274  POP_JUMP_IF_TRUE    516  'to 516'
            276_0  COME_FROM           336  '336'
            276_1  COME_FROM           314  '314'

 L. 213       276  LOAD_FAST                'self'
              278  LOAD_ATTR                begidx
              280  LOAD_CONST               0
              282  COMPARE_OP               >
          284_286  POP_JUMP_IF_FALSE   340  'to 340'

 L. 214       288  LOAD_FAST                'self'
              290  DUP_TOP          
              292  LOAD_ATTR                begidx
              294  LOAD_CONST               1
              296  INPLACE_SUBTRACT 
              298  ROT_TWO          
              300  STORE_ATTR               begidx

 L. 215       302  LOAD_FAST                'buf'
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                begidx
              308  BINARY_SUBSCR    
              310  LOAD_STR                 ' \t\n'
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_FALSE_BACK   276  'to 276'

 L. 216       318  LOAD_FAST                'self'
              320  DUP_TOP          
              322  LOAD_ATTR                begidx
              324  LOAD_CONST               1
              326  INPLACE_ADD      
              328  ROT_TWO          
              330  STORE_ATTR               begidx

 L. 217   332_334  JUMP_FORWARD        340  'to 340'
          336_338  JUMP_BACK           276  'to 276'
            340_0  COME_FROM           332  '332'
            340_1  COME_FROM           284  '284'

 L. 218       340  LOAD_GLOBAL              ensure_str
              342  LOAD_STR                 ''
              344  LOAD_METHOD              join
              346  LOAD_FAST                'buf'
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                begidx
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                endidx
              356  BUILD_SLICE_2         2 
              358  BINARY_SUBSCR    
              360  CALL_METHOD_1         1  ''
              362  CALL_FUNCTION_1       1  ''
              364  STORE_FAST               'text'

 L. 219       366  LOAD_GLOBAL              log
              368  LOAD_STR                 'file complete text="%s"'
              370  LOAD_GLOBAL              ensure_unicode
              372  LOAD_FAST                'text'
              374  CALL_FUNCTION_1       1  ''
              376  BINARY_MODULO    
              378  CALL_FUNCTION_1       1  ''
              380  POP_TOP          

 L. 220       382  LOAD_GLOBAL              list
              384  LOAD_GLOBAL              map
              386  LOAD_GLOBAL              ensure_unicode
              388  LOAD_GLOBAL              glob
              390  LOAD_METHOD              glob
              392  LOAD_GLOBAL              os
              394  LOAD_ATTR                path
              396  LOAD_METHOD              expanduser
              398  LOAD_FAST                'text'
              400  CALL_METHOD_1         1  ''
              402  LOAD_STR                 '*'
              404  LOAD_METHOD              encode
              406  LOAD_STR                 'ascii'
              408  CALL_METHOD_1         1  ''
              410  BINARY_ADD       
              412  CALL_METHOD_1         1  ''
              414  CALL_FUNCTION_2       2  ''
              416  CALL_FUNCTION_1       1  ''
              418  STORE_FAST               'completions'

 L. 221       420  LOAD_FAST                'self'
              422  LOAD_ATTR                mark_directories
              424  LOAD_STR                 'on'
              426  COMPARE_OP               ==
          428_430  POP_JUMP_IF_FALSE   494  'to 494'

 L. 222       432  BUILD_LIST_0          0 
              434  STORE_FAST               'mc'

 L. 223       436  LOAD_FAST                'completions'
              438  GET_ITER         
            440_0  COME_FROM           486  '486'
            440_1  COME_FROM           474  '474'
              440  FOR_ITER            490  'to 490'
              442  STORE_FAST               'f'

 L. 224       444  LOAD_GLOBAL              os
              446  LOAD_ATTR                path
              448  LOAD_METHOD              isdir
              450  LOAD_FAST                'f'
              452  CALL_METHOD_1         1  ''
          454_456  POP_JUMP_IF_FALSE   476  'to 476'

 L. 225       458  LOAD_FAST                'mc'
              460  LOAD_METHOD              append
              462  LOAD_FAST                'f'
              464  LOAD_GLOBAL              os
              466  LOAD_ATTR                sep
              468  BINARY_ADD       
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          
              474  JUMP_BACK           440  'to 440'
            476_0  COME_FROM           454  '454'

 L. 227       476  LOAD_FAST                'mc'
              478  LOAD_METHOD              append
              480  LOAD_FAST                'f'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
          486_488  JUMP_BACK           440  'to 440'
            490_0  COME_FROM           440  '440'

 L. 228       490  LOAD_FAST                'mc'
              492  STORE_FAST               'completions'
            494_0  COME_FROM           428  '428'

 L. 229       494  LOAD_GLOBAL              log
              496  LOAD_STR                 'fnames=<%s>'
              498  LOAD_GLOBAL              list
              500  LOAD_GLOBAL              map
              502  LOAD_GLOBAL              ensure_unicode
              504  LOAD_FAST                'completions'
              506  CALL_FUNCTION_2       2  ''
              508  CALL_FUNCTION_1       1  ''
              510  BINARY_MODULO    
              512  CALL_FUNCTION_1       1  ''
              514  POP_TOP          
            516_0  COME_FROM           272  '272'
            516_1  COME_FROM           266  '266'

 L. 230       516  LOAD_FAST                'completions'
              518  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 96

    def _display_completions(self, completions):
        if not completions:
            return
        self.console.write('\n')
        wmax = max(map(len, completions))
        w, h = self.console.size()
        cols = max(1, int((w - 1) / (wmax + 1)))
        rows = int(math.ceil(float(len(completions)) / cols))
        for row in range(rows):
            s = ''
            for col in range(cols):
                i = col * rows + row
                if i < len(completions):
                    self.console.write(completions[i].ljust(wmax + 1))
            else:
                self.console.write('\n')

        else:
            if in_ironpython:
                self.prompt = sys.ps1
            self._print_prompt()

    def complete(self, e):
        """Attempt to perform completion on the text before point. The
        actual completion performed is application-specific. The default is
        filename completion."""
        completions = self._get_completions()
        if completions:
            cprefix = commonprefix(completions)
            if len(cprefix) > 0:
                rep = [c for c in cprefix]
                point = self.l_buffer.point
                self.l_buffer[self.begidx:self.endidx] = rep
                self.l_buffer.point = point + len(rep) - (self.endidx - self.begidx)
            if len(completions) > 1:
                if self.show_all_if_ambiguous == 'on':
                    self._display_completions(completions)
                else:
                    self._bell()
        else:
            self._bell()
        self.finalize()

    def possible_completions(self, e):
        """List the possible completions of the text before point. """
        completions = self._get_completions()
        self._display_completions(completions)
        self.finalize()

    def insert_completions(self, e):
        """Insert all completions of the text before point that would have
        been generated by possible-completions."""
        completions = self._get_completions()
        b = self.begidx
        e = self.endidx
        for comp in completions:
            rep = [c for c in comp]
            rep.append(' ')
            self.l_buffer[b:e] = rep
            b += len(rep)
            e = b
        else:
            self.line_cursor = b
            self.finalize()

    def menu_complete(self, e):
        """Similar to complete, but replaces the word to be completed with a
        single match from the list of possible completions. Repeated
        execution of menu-complete steps through the list of possible
        completions, inserting each match in turn. At the end of the list of
        completions, the bell is rung (subject to the setting of bell-style)
        and the original text is restored. An argument of n moves n
        positions forward in the list of matches; a negative argument may be
        used to move backward through the list. This command is intended to
        be bound to TAB, but is unbound by default."""
        self.finalize()

    def insert_text(self, string):
        """Insert text into the command line."""
        self.l_buffer.insert_textstringself.argument_reset
        self.finalize()

    def beginning_of_line(self, e):
        """Move to the start of the current line. """
        self.l_buffer.beginning_of_line()
        self.finalize()

    def end_of_line(self, e):
        """Move to the end of the line. """
        self.l_buffer.end_of_line()
        self.finalize()

    def forward_char(self, e):
        """Move forward a character. """
        self.l_buffer.forward_char(self.argument_reset)
        self.finalize()

    def backward_char(self, e):
        """Move back a character. """
        self.l_buffer.backward_char(self.argument_reset)
        self.finalize()

    def forward_word(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word(self.argument_reset)
        self.finalize()

    def backward_word(self, e):
        """Move back to the start of the current or previous word. Words are
        composed of letters and digits."""
        self.l_buffer.backward_word(self.argument_reset)
        self.finalize()

    def forward_word_end(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word_end(self.argument_reset)
        self.finalize()

    def backward_word_end(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.backward_word_end(self.argument_reset)
        self.finalize()

    def beginning_of_line_extend_selection(self, e):
        """Move to the start of the current line. """
        self.l_buffer.beginning_of_line_extend_selection()
        self.finalize()

    def end_of_line_extend_selection(self, e):
        """Move to the end of the line. """
        self.l_buffer.end_of_line_extend_selection()
        self.finalize()

    def forward_char_extend_selection(self, e):
        """Move forward a character. """
        self.l_buffer.forward_char_extend_selection(self.argument_reset)
        self.finalize()

    def backward_char_extend_selection(self, e):
        """Move back a character. """
        self.l_buffer.backward_char_extend_selection(self.argument_reset)
        self.finalize()

    def forward_word_extend_selection(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word_extend_selection(self.argument_reset)
        self.finalize()

    def backward_word_extend_selection(self, e):
        """Move back to the start of the current or previous word. Words are
        composed of letters and digits."""
        self.l_buffer.backward_word_extend_selection(self.argument_reset)
        self.finalize()

    def forward_word_end_extend_selection(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word_end_extend_selection(self.argument_reset)
        self.finalize()

    def backward_word_end_extend_selection(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word_end_extend_selection(self.argument_reset)
        self.finalize()

    def upcase_word(self, e):
        """Uppercase the current (or following) word. With a negative
        argument, uppercase the previous word, but do not move the cursor."""
        self.l_buffer.upcase_word()
        self.finalize()

    def downcase_word(self, e):
        """Lowercase the current (or following) word. With a negative
        argument, lowercase the previous word, but do not move the cursor."""
        self.l_buffer.downcase_word()
        self.finalize()

    def capitalize_word(self, e):
        """Capitalize the current (or following) word. With a negative
        argument, capitalize the previous word, but do not move the cursor."""
        self.l_buffer.capitalize_word()
        self.finalize()

    def clear_screen(self, e):
        """Clear the screen and redraw the current line, leaving the current
        line at the top of the screen."""
        self.console.page()
        self.finalize()

    def redraw_current_line(self, e):
        """Refresh the current line. By default, this is unbound."""
        self.finalize()

    def accept_line(self, e):
        """Accept the line regardless of where the cursor is. If this line
        is non-empty, it may be added to the history list for future recall
        with add_history(). If this line is a modified history line, the
        history line is restored to its original state."""
        self.finalize()
        return True

    def delete_char(self, e):
        """Delete the character at point. If point is at the beginning of
        the line, there are no characters in the line, and the last
        character typed was not bound to delete-char, then return EOF."""
        self.l_buffer.delete_char(self.argument_reset)
        self.finalize()

    def backward_delete_char(self, e):
        """Delete the character behind the cursor. A numeric argument means
        to kill the characters instead of deleting them."""
        self.l_buffer.backward_delete_char(self.argument_reset)
        self.finalize()

    def backward_delete_word(self, e):
        """Delete the character behind the cursor. A numeric argument means
        to kill the characters instead of deleting them."""
        self.l_buffer.backward_delete_word(self.argument_reset)
        self.finalize()

    def forward_delete_word(self, e):
        """Delete the character behind the cursor. A numeric argument means
        to kill the characters instead of deleting them."""
        self.l_buffer.forward_delete_word(self.argument_reset)
        self.finalize()

    def delete_horizontal_space(self, e):
        """Delete all spaces and tabs around point. By default, this is unbound. """
        self.l_buffer.delete_horizontal_space()
        self.finalize()

    def self_insert(self, e):
        """Insert yourself. """
        if e.char:
            if ord(e.char) != 0:
                self.insert_text(e.char)
        self.finalize()

    def paste(self, e):
        """Paste windows clipboard.
        Assume single line strip other lines and end of line markers and trailing spaces"""
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(False)
            txt = txt.split('\n')[0].strip('\r').strip('\n')
            log('paste: >%s<' % list(map(ord, txt)))
            self.insert_text(txt)
        self.finalize()

    def paste_mulitline_code(self, e):
        """Paste windows clipboard as multiline code.
        Removes any empty lines in the code"""
        reg = re.compile('\r?\n')
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(False)
            t = reg.split(txt)
            t = [row for row in t if row.strip() != '']
            if t != ['']:
                self.insert_text(t[0])
                self.add_history(self.l_buffer.copy())
                self.paste_line_buffer = t[1:]
                log('multi: >%s<' % self.paste_line_buffer)
                return True
            return False
        self.finalize()

    def ipython_paste(self, e):
        r"""Paste windows clipboard. If enable_ipython_paste_list_of_lists is 
        True then try to convert tabseparated data to repr of list of lists or 
        repr of array.
        If enable_ipython_paste_for_paths==True then change \ to / and spaces to \space"""
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(self.enable_ipython_paste_list_of_lists)
            if self.enable_ipython_paste_for_paths:
                if len(txt) < 300:
                    if '\t' not in txt:
                        if '\n' not in txt:
                            txt = txt.replace'\\''/'.replace' ''\\ '
            self.insert_text(txt)
        self.finalize()

    def copy_region_to_clipboard(self, e):
        """Copy the text in the region to the windows clipboard."""
        self.l_buffer.copy_region_to_clipboard()
        self.finalize()

    def copy_selection_to_clipboard(self, e):
        """Copy the text in the region to the windows clipboard."""
        self.l_buffer.copy_selection_to_clipboard()
        self.finalize()

    def cut_selection_to_clipboard(self, e):
        """Copy the text in the region to the windows clipboard."""
        self.l_buffer.cut_selection_to_clipboard()
        self.finalize()

    def dump_functions(self, e):
        """Print all of the functions and their key bindings to the Readline
        output stream. If a numeric argument is supplied, the output is
        formatted in such a way that it can be made part of an inputrc
        file. This command is unbound by default."""
        print()
        txt = '\n'.join(self.rl_settings_to_string())
        print(txt)
        self._print_prompt()
        self.finalize()


def commonprefix(m):
    """Given a list of pathnames, returns the longest common leading component"""
    if not m:
        return ''
    prefix = m[0]
    for item in m:
        for i in range(len(prefix)):
            if prefix[:i + 1].lower() != item[:i + 1].lower():
                prefix = prefix[:i]
                if i == 0:
                    return ''
                else:
                    break
        else:
            return prefix