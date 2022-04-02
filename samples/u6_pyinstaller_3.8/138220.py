# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\modes\notemacs.py
from __future__ import print_function, unicode_literals, absolute_import
import os
import pyreadline.logger as logger
from pyreadline.logger import log
import pyreadline.lineeditor.lineobj as lineobj
import pyreadline.lineeditor.history as history
from . import basemode

class NotEmacsMode(basemode.BaseMode):
    mode = 'notemacs'

    def __init__(self, rlobj):
        super(NotEmacsMode, self).__init__(rlobj)

    def __repr__(self):
        return '<NotEmacsMode>'

    def _readline_from_keyboard(self):
        c = self.console
        while True:
            self._update_line()
            event = c.getkeypress()
            if self.next_meta:
                self.next_meta = False
                control, meta, shift, code = event.keyinfo
                event.keyinfo = (control, True, shift, code)
            if event.keyinfo in self.exit_dispatch:
                if lineobj.EndOfLine(self.l_buffer) == 0:
                    raise EOFError
            dispatch_func = self.key_dispatch.get(event.keyinfo, self.self_insert)
            log('readline from keyboard:%s' % (event.keyinfo,))
            r = None
            if dispatch_func:
                r = dispatch_func(event)
                self.l_buffer.push_undo()
            self.previous_func = dispatch_func
            if r:
                self._update_line()
                break

    def readline(self, prompt=''):
        """Try to act like GNU readline."""
        if self.first_prompt:
            self.first_prompt = False
            if self.startup_hook:
                try:
                    self.startup_hook()
                except:
                    print('startup hook failed')
                    traceback.print_exc()

            else:
                c = self.console
                self.l_buffer.reset_line()
                self.prompt = prompt
                self._print_prompt()
                if self.pre_input_hook:
                    try:
                        self.pre_input_hook()
                    except:
                        print('pre_input_hook failed')
                        traceback.print_exc()
                        self.pre_input_hook = None

        else:
            log('in readline: %s' % self.paste_line_buffer)
            if len(self.paste_line_buffer) > 0:
                self.l_buffer = lineobj.ReadlineTextBuffer(self.paste_line_buffer[0])
                self._update_line()
                self.paste_line_buffer = self.paste_line_buffer[1:]
                c.write('\r\n')
            else:
                self._readline_from_keyboard()
            c.write('\r\n')
        self.add_history(self.l_buffer.copy())
        log('returning(%s)' % self.l_buffer.get_line_text())
        return self.l_buffer.get_line_text() + '\n'

    def beginning_of_line(self, e):
        """Move to the start of the current line. """
        self.l_buffer.beginning_of_line()

    def end_of_line(self, e):
        """Move to the end of the line. """
        self.l_buffer.end_of_line()

    def forward_char(self, e):
        """Move forward a character. """
        self.l_buffer.forward_char()

    def backward_char(self, e):
        """Move back a character. """
        self.l_buffer.backward_char()

    def forward_word(self, e):
        """Move forward to the end of the next word. Words are composed of
        letters and digits."""
        self.l_buffer.forward_word()

    def backward_word(self, e):
        """Move back to the start of the current or previous word. Words are
        composed of letters and digits."""
        self.l_buffer.backward_word()

    def clear_screen(self, e):
        """Clear the screen and redraw the current line, leaving the current
        line at the top of the screen."""
        self.console.page()

    def redraw_current_line(self, e):
        """Refresh the current line. By default, this is unbound."""
        pass

    def accept_line(self, e):
        """Accept the line regardless of where the cursor is. If this line
        is non-empty, it may be added to the history list for future recall
        with add_history(). If this line is a modified history line, the
        history line is restored to its original state."""
        return True

    def previous_history(self, e):
        """Move back through the history list, fetching the previous command. """
        self._history.previous_history(self.l_buffer)

    def next_history(self, e):
        """Move forward through the history list, fetching the next command. """
        self._history.next_history(self.l_buffer)

    def beginning_of_history(self, e):
        """Move to the first line in the history."""
        self._history.beginning_of_history()

    def end_of_history(self, e):
        """Move to the end of the input history, i.e., the line currently
        being entered."""
        self._history.end_of_history(self.l_buffer)

    def _i_search--- This code section failed: ---

 L. 155         0  LOAD_FAST                'self'
                2  LOAD_ATTR                console
                4  STORE_FAST               'c'

 L. 156         6  LOAD_FAST                'self'
                8  LOAD_METHOD              get_line_buffer
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'line'

 L. 157        14  LOAD_STR                 ''
               16  STORE_FAST               'query'

 L. 158        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _history
               22  LOAD_ATTR                history_cursor
               24  STORE_FAST               'hc_start'

 L. 160        26  LOAD_FAST                'self'
               28  LOAD_ATTR                prompt_end_pos
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'x'
               34  STORE_FAST               'y'

 L. 161        36  LOAD_FAST                'c'
               38  LOAD_METHOD              pos
               40  LOAD_CONST               0
               42  LOAD_FAST                'y'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 162        48  LOAD_FAST                'direction'
               50  LOAD_CONST               0
               52  COMPARE_OP               <
               54  POP_JUMP_IF_FALSE    62  'to 62'

 L. 163        56  LOAD_STR                 'reverse-i-search'
               58  STORE_FAST               'prompt'
               60  JUMP_FORWARD         66  'to 66'
             62_0  COME_FROM            54  '54'

 L. 165        62  LOAD_STR                 'forward-i-search'
               64  STORE_FAST               'prompt'
             66_0  COME_FROM            60  '60'

 L. 167        66  LOAD_FAST                'c'
               68  LOAD_METHOD              write_scrolling
               70  LOAD_STR                 "%s`%s': %s"
               72  LOAD_FAST                'prompt'
               74  LOAD_FAST                'query'
               76  LOAD_FAST                'line'
               78  BUILD_TUPLE_3         3 
               80  BINARY_MODULO    
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'scroll'

 L. 168        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _update_prompt_pos
               90  LOAD_FAST                'scroll'
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 169        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _clear_after
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 171       104  LOAD_FAST                'c'
              106  LOAD_METHOD              getkeypress
              108  CALL_METHOD_0         0  ''
              110  STORE_FAST               'event'

 L. 172       112  LOAD_FAST                'event'
              114  LOAD_ATTR                keysym
              116  LOAD_STR                 'BackSpace'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   166  'to 166'

 L. 173       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'query'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               0
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   156  'to 156'

 L. 174       134  LOAD_FAST                'query'
              136  LOAD_CONST               None
              138  LOAD_CONST               -1
              140  BUILD_SLICE_2         2 
              142  BINARY_SUBSCR    
              144  STORE_FAST               'query'

 L. 175       146  LOAD_FAST                'hc_start'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                _history
              152  STORE_ATTR               history_cursor
              154  JUMP_FORWARD        164  'to 164'
            156_0  COME_FROM           132  '132'

 L. 177       156  LOAD_FAST                'self'
              158  LOAD_METHOD              _bell
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          
            164_0  COME_FROM           154  '154'
              164  JUMP_FORWARD        276  'to 276'
            166_0  COME_FROM           120  '120'

 L. 178       166  LOAD_FAST                'event'
              168  LOAD_ATTR                char
              170  LOAD_GLOBAL              string
              172  LOAD_ATTR                letters
              174  LOAD_GLOBAL              string
              176  LOAD_ATTR                digits
              178  BINARY_ADD       
              180  LOAD_GLOBAL              string
              182  LOAD_ATTR                punctuation
              184  BINARY_ADD       
              186  LOAD_STR                 ' '
              188  BINARY_ADD       
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   214  'to 214'

 L. 179       194  LOAD_FAST                'hc_start'
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                _history
              200  STORE_ATTR               history_cursor

 L. 180       202  LOAD_FAST                'query'
              204  LOAD_FAST                'event'
              206  LOAD_ATTR                char
              208  INPLACE_ADD      
              210  STORE_FAST               'query'
              212  JUMP_FORWARD        276  'to 276'
            214_0  COME_FROM           192  '192'

 L. 181       214  LOAD_FAST                'event'
              216  LOAD_ATTR                keyinfo
              218  LOAD_FAST                'init_event'
              220  LOAD_ATTR                keyinfo
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   252  'to 252'

 L. 182       226  LOAD_FAST                'self'
              228  LOAD_ATTR                _history
              230  DUP_TOP          
              232  LOAD_ATTR                history_cursor
              234  LOAD_FAST                'direction'
              236  INPLACE_ADD      
              238  ROT_TWO          
              240  STORE_ATTR               history_cursor

 L. 183       242  LOAD_FAST                'searchfun'
              244  LOAD_FAST                'query'
              246  CALL_FUNCTION_1       1  ''
              248  STORE_FAST               'line'

 L. 184       250  BREAK_LOOP          276  'to 276'
            252_0  COME_FROM           224  '224'

 L. 186       252  LOAD_FAST                'event'
              254  LOAD_ATTR                keysym
              256  LOAD_STR                 'Return'
              258  COMPARE_OP               !=
          260_262  POP_JUMP_IF_FALSE   286  'to 286'

 L. 187       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _bell
              268  CALL_METHOD_0         0  ''
              270  POP_TOP          

 L. 188   272_274  BREAK_LOOP          286  'to 286'
            276_0  COME_FROM           250  '250'
            276_1  COME_FROM           212  '212'
            276_2  COME_FROM           164  '164'

 L. 189       276  LOAD_FAST                'searchfun'
              278  LOAD_FAST                'query'
              280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'line'
              284  JUMP_BACK            26  'to 26'
            286_0  COME_FROM           260  '260'

 L. 191       286  LOAD_FAST                'self'
              288  LOAD_ATTR                prompt_begin_pos
              290  UNPACK_SEQUENCE_2     2 
              292  STORE_FAST               'px'
              294  STORE_FAST               'py'

 L. 192       296  LOAD_FAST                'c'
              298  LOAD_METHOD              pos
              300  LOAD_CONST               0
              302  LOAD_FAST                'py'
              304  CALL_METHOD_2         2  ''
              306  POP_TOP          

 L. 193       308  LOAD_FAST                'self'
              310  LOAD_ATTR                l_buffer
              312  LOAD_METHOD              set_line
              314  LOAD_FAST                'line'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          

 L. 194       320  LOAD_FAST                'self'
              322  LOAD_METHOD              _print_prompt
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 195       328  LOAD_GLOBAL              len
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                _history
              334  LOAD_ATTR                history
              336  CALL_FUNCTION_1       1  ''
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                _history
              342  STORE_ATTR               history_cursor

Parse error at or near `COME_FROM' instruction at offset 286_0

    def reverse_search_history(self, e):
        """Search backward starting at the current line and moving up
        through the history as necessary. This is an incremental search."""
        self._i_search(self._history.reverse_search_history, -1, e)

    def forward_search_history(self, e):
        """Search forward starting at the current line and moving down
        through the the history as necessary. This is an incremental search."""
        self._i_search(self._history.forward_search_history, 1, e)

    def non_incremental_reverse_search_history(self, e):
        """Search backward starting at the current line and moving up
        through the history as necessary using a non-incremental search for
        a string supplied by the user."""
        self._history.non_incremental_reverse_search_history(self.l_buffer)

    def non_incremental_forward_search_history(self, e):
        """Search forward starting at the current line and moving down
        through the the history as necessary using a non-incremental search
        for a string supplied by the user."""
        self._history.non_incremental_reverse_search_history(self.l_buffer)

    def history_search_forward(self, e):
        """Search forward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""
        self.l_buffer = self._history.history_search_forward(self.l_buffer)

    def history_search_backward(self, e):
        """Search backward through the history for the string of characters
        between the start of the current line and the point. This is a
        non-incremental search. By default, this command is unbound."""
        self.l_buffer = self._history.history_search_backward(self.l_buffer)

    def yank_nth_arg(self, e):
        """Insert the first argument to the previous command (usually the
        second word on the previous line) at point. With an argument n,
        insert the nth word from the previous command (the words in the
        previous command begin with word 0). A negative argument inserts the
        nth word from the end of the previous command."""
        pass

    def yank_last_arg(self, e):
        """Insert last argument to the previous command (the last word of
        the previous history entry). With an argument, behave exactly like
        yank-nth-arg. Successive calls to yank-last-arg move back through
        the history list, inserting the last argument of each line in turn."""
        pass

    def delete_char(self, e):
        """Delete the character at point. If point is at the beginning of
        the line, there are no characters in the line, and the last
        character typed was not bound to delete-char, then return EOF."""
        self.l_buffer.delete_char()

    def backward_delete_char(self, e):
        """Delete the character behind the cursor. A numeric argument means
        to kill the characters instead of deleting them."""
        self.l_buffer.backward_delete_char()

    def forward_backward_delete_char(self, e):
        """Delete the character under the cursor, unless the cursor is at
        the end of the line, in which case the character behind the cursor
        is deleted. By default, this is not bound to a key."""
        pass

    def quoted_insert(self, e):
        """Add the next character typed to the line verbatim. This is how to
        insert key sequences like C-q, for example."""
        e = self.console.getkeypress()
        self.insert_text(e.char)

    def tab_insert(self, e):
        """Insert a tab character. """
        cursor = min(self.l_buffer.point, len(self.l_buffer.line_buffer))
        ws = ' ' * (self.tabstop - cursor % self.tabstop)
        self.insert_text(ws)

    def self_insert(self, e):
        """Insert yourself. """
        if ord(e.char) != 0:
            self.insert_text(e.char)

    def transpose_chars(self, e):
        """Drag the character before the cursor forward over the character
        at the cursor, moving the cursor forward as well. If the insertion
        point is at the end of the line, then this transposes the last two
        characters of the line. Negative arguments have no effect."""
        self.l_buffer.transpose_chars()

    def transpose_words(self, e):
        """Drag the word before point past the word after point, moving
        point past that word as well. If the insertion point is at the end
        of the line, this transposes the last two words on the line."""
        self.l_buffer.transpose_words()

    def upcase_word(self, e):
        """Uppercase the current (or following) word. With a negative
        argument, uppercase the previous word, but do not move the cursor."""
        self.l_buffer.upcase_word()

    def downcase_word(self, e):
        """Lowercase the current (or following) word. With a negative
        argument, lowercase the previous word, but do not move the cursor."""
        self.l_buffer.downcase_word()

    def capitalize_word(self, e):
        """Capitalize the current (or following) word. With a negative
        argument, capitalize the previous word, but do not move the cursor."""
        self.l_buffer.capitalize_word()

    def overwrite_mode(self, e):
        """Toggle overwrite mode. With an explicit positive numeric
        argument, switches to overwrite mode. With an explicit non-positive
        numeric argument, switches to insert mode. This command affects only
        emacs mode; vi mode does overwrite differently. Each call to
        readline() starts in insert mode. In overwrite mode, characters
        bound to self-insert replace the text at point rather than pushing
        the text to the right. Characters bound to backward-delete-char
        replace the character before point with a space."""
        pass

    def kill_line(self, e):
        """Kill the text from point to the end of the line. """
        self.l_buffer.kill_line()

    def backward_kill_line(self, e):
        """Kill backward to the beginning of the line. """
        self.l_buffer.backward_kill_line()

    def unix_line_discard(self, e):
        """Kill backward from the cursor to the beginning of the current line. """
        self.l_buffer.unix_line_discard()

    def kill_whole_line(self, e):
        """Kill all characters on the current line, no matter where point
        is. By default, this is unbound."""
        self.l_buffer.kill_whole_line()

    def kill_word(self, e):
        """Kill from point to the end of the current word, or if between
        words, to the end of the next word. Word boundaries are the same as
        forward-word."""
        self.l_buffer.kill_word()

    def backward_kill_word(self, e):
        """Kill the word behind point. Word boundaries are the same as
        backward-word. """
        self.l_buffer.backward_kill_word()

    def unix_word_rubout(self, e):
        """Kill the word behind point, using white space as a word
        boundary. The killed text is saved on the kill-ring."""
        self.l_buffer.unix_word_rubout()

    def delete_horizontal_space(self, e):
        """Delete all spaces and tabs around point. By default, this is unbound. """
        pass

    def kill_region(self, e):
        """Kill the text in the current region. By default, this command is unbound. """
        pass

    def copy_region_as_kill(self, e):
        """Copy the text in the region to the kill buffer, so it can be
        yanked right away. By default, this command is unbound."""
        pass

    def copy_region_to_clipboard(self, e):
        """Copy the text in the region to the windows clipboard."""
        if self.enable_win32_clipboard:
            mark = min(self.l_buffer.mark, len(self.l_buffer.line_buffer))
            cursor = min(self.l_buffer.point, len(self.l_buffer.line_buffer))
            if self.l_buffer.mark == -1:
                return
            begin = min(cursor, mark)
            end = max(cursor, mark)
            toclipboard = ''.join(self.l_buffer.line_buffer[begin:end])
            clipboard.SetClipboardText(str(toclipboard))

    def copy_backward_word(self, e):
        """Copy the word before point to the kill buffer. The word
        boundaries are the same as backward-word. By default, this command
        is unbound."""
        pass

    def copy_forward_word(self, e):
        """Copy the word following point to the kill buffer. The word
        boundaries are the same as forward-word. By default, this command is
        unbound."""
        pass

    def paste(self, e):
        """Paste windows clipboard"""
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(False)
            self.insert_text(txt)

    def paste_mulitline_code(self, e):
        """Paste windows clipboard"""
        reg = re.compile('\r?\n')
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(False)
            t = reg.split(txt)
            t = [row for row in t if row.strip() != '']
            if t != ['']:
                self.insert_text(t[0])
                self.add_history(self.l_buffer.copy())
                self.paste_line_buffer = t[1:]
                log('multi: %s' % self.paste_line_buffer)
                return True
            return False

    def ipython_paste(self, e):
        """Paste windows clipboard. If enable_ipython_paste_list_of_lists is 
        True then try to convert tabseparated data to repr of list of lists or 
        repr of array"""
        if self.enable_win32_clipboard:
            txt = clipboard.get_clipboard_text_and_convert(self.enable_ipython_paste_list_of_lists)
            if self.enable_ipython_paste_for_paths:
                if len(txt) < 300:
                    if '\t' not in txt:
                        if '\n' not in txt:
                            txt = txt.replace('\\', '/').replace(' ', '\\ ')
            self.insert_text(txt)

    def yank(self, e):
        """Yank the top of the kill ring into the buffer at point. """
        pass

    def yank_pop(self, e):
        """Rotate the kill-ring, and yank the new top. You can only do this
        if the prior command is yank or yank-pop."""
        pass

    def digit_argument(self, e):
        """Add this digit to the argument already accumulating, or start a
        new argument. M-- starts a negative argument."""
        pass

    def universal_argument(self, e):
        """This is another way to specify an argument. If this command is
        followed by one or more digits, optionally with a leading minus
        sign, those digits define the argument. If the command is followed
        by digits, executing universal-argument again ends the numeric
        argument, but is otherwise ignored. As a special case, if this
        command is immediately followed by a character that is neither a
        digit or minus sign, the argument count for the next command is
        multiplied by four. The argument count is initially one, so
        executing this function the first time makes the argument count
        four, a second time makes the argument count sixteen, and so on. By
        default, this is not bound to a key."""
        pass

    def delete_char_or_list(self, e):
        """Deletes the character under the cursor if not at the beginning or
        end of the line (like delete-char). If at the end of the line,
        behaves identically to possible-completions. This command is unbound
        by default."""
        pass

    def start_kbd_macro(self, e):
        """Begin saving the characters typed into the current keyboard macro. """
        pass

    def end_kbd_macro(self, e):
        """Stop saving the characters typed into the current keyboard macro
        and save the definition."""
        pass

    def call_last_kbd_macro(self, e):
        """Re-execute the last keyboard macro defined, by making the
        characters in the macro appear as if typed at the keyboard."""
        pass

    def re_read_init_file(self, e):
        """Read in the contents of the inputrc file, and incorporate any
        bindings or variable assignments found there."""
        pass

    def abort(self, e):
        """Abort the current editing command and ring the terminals bell
             (subject to the setting of bell-style)."""
        self._bell()

    def do_uppercase_version(self, e):
        """If the metafied character x is lowercase, run the command that is
        bound to the corresponding uppercase character."""
        pass

    def prefix_meta(self, e):
        """Metafy the next character typed. This is for keyboards without a
        meta key. Typing ESC f is equivalent to typing M-f. """
        self.next_meta = True

    def undo(self, e):
        """Incremental undo, separately remembered for each line."""
        self.l_buffer.pop_undo()

    def revert_line(self, e):
        """Undo all changes made to this line. This is like executing the
        undo command enough times to get back to the beginning."""
        pass

    def tilde_expand(self, e):
        """Perform tilde expansion on the current word."""
        pass

    def set_mark(self, e):
        """Set the mark to the point. If a numeric argument is supplied, the
        mark is set to that position."""
        self.l_buffer.set_mark()

    def exchange_point_and_mark(self, e):
        """Swap the point with the mark. The current cursor position is set
        to the saved position, and the old cursor position is saved as the
        mark."""
        pass

    def character_search(self, e):
        """A character is read and point is moved to the next occurrence of
        that character. A negative count searches for previous occurrences."""
        pass

    def character_search_backward(self, e):
        """A character is read and point is moved to the previous occurrence
        of that character. A negative count searches for subsequent
        occurrences."""
        pass

    def insert_comment(self, e):
        """Without a numeric argument, the value of the comment-begin
        variable is inserted at the beginning of the current line. If a
        numeric argument is supplied, this command acts as a toggle: if the
        characters at the beginning of the line do not match the value of
        comment-begin, the value is inserted, otherwise the characters in
        comment-begin are deleted from the beginning of the line. In either
        case, the line is accepted as if a newline had been typed."""
        pass

    def dump_functions(self, e):
        """Print all of the functions and their key bindings to the Readline
        output stream. If a numeric argument is supplied, the output is
        formatted in such a way that it can be made part of an inputrc
        file. This command is unbound by default."""
        pass

    def dump_variables(self, e):
        """Print all of the settable variables and their values to the
        Readline output stream. If a numeric argument is supplied, the
        output is formatted in such a way that it can be made part of an
        inputrc file. This command is unbound by default."""
        pass

    def dump_macros(self, e):
        """Print all of the Readline key sequences bound to macros and the
        strings they output. If a numeric argument is supplied, the output
        is formatted in such a way that it can be made part of an inputrc
        file. This command is unbound by default."""
        pass

    def init_editing_mode(self, e):
        """When in vi command mode, this causes a switch to emacs editing
        mode."""
        self._bind_exit_key('Control-d')
        self._bind_exit_key('Control-z')
        self._bind_key('Shift-space', self.self_insert)
        self._bind_key('Control-space', self.self_insert)
        self._bind_key('Return', self.accept_line)
        self._bind_key('Left', self.backward_char)
        self._bind_key('Control-b', self.backward_char)
        self._bind_key('Right', self.forward_char)
        self._bind_key('Control-f', self.forward_char)
        self._bind_key('BackSpace', self.backward_delete_char)
        self._bind_key('Home', self.beginning_of_line)
        self._bind_key('End', self.end_of_line)
        self._bind_key('Delete', self.delete_char)
        self._bind_key('Control-d', self.delete_char)
        self._bind_key('Clear', self.clear_screen)


def commonprefix--- This code section failed: ---

 L. 594         0  LOAD_FAST                'm'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 594         4  LOAD_STR                 ''
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 595         8  LOAD_FAST                'm'
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'prefix'

 L. 596        16  LOAD_FAST                'm'
               18  GET_ITER         
               20  FOR_ITER            116  'to 116'
               22  STORE_FAST               'item'

 L. 597        24  LOAD_GLOBAL              range
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'prefix'
               30  CALL_FUNCTION_1       1  ''
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM            78  '78'
               36  FOR_ITER            114  'to 114'
               38  STORE_FAST               'i'

 L. 598        40  LOAD_FAST                'prefix'
               42  LOAD_CONST               None
               44  LOAD_FAST                'i'
               46  LOAD_CONST               1
               48  BINARY_ADD       
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  LOAD_METHOD              lower
               56  CALL_METHOD_0         0  ''
               58  LOAD_FAST                'item'
               60  LOAD_CONST               None
               62  LOAD_FAST                'i'
               64  LOAD_CONST               1
               66  BINARY_ADD       
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  LOAD_METHOD              lower
               74  CALL_METHOD_0         0  ''
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_FALSE    36  'to 36'

 L. 599        80  LOAD_FAST                'prefix'
               82  LOAD_CONST               None
               84  LOAD_FAST                'i'
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  STORE_FAST               'prefix'

 L. 600        92  LOAD_FAST                'i'
               94  LOAD_CONST               0
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L. 600       100  POP_TOP          
              102  POP_TOP          
              104  LOAD_STR                 ''
              106  RETURN_VALUE     
            108_0  COME_FROM            98  '98'

 L. 601       108  POP_TOP          
              110  CONTINUE             20  'to 20'
              112  JUMP_BACK            36  'to 36'
              114  JUMP_BACK            20  'to 20'

 L. 602       116  LOAD_FAST                'prefix'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 114