# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pyreadline\modes\vi.py
from __future__ import print_function, unicode_literals, absolute_import
import os
import pyreadline.logger as logger
from pyreadline.logger import log
import pyreadline.lineeditor.lineobj as lineobj
import pyreadline.lineeditor.history as history
from . import basemode

class ViMode(basemode.BaseMode):
    mode = 'vi'

    def __init__(self, rlobj):
        super(ViMode, self).__init__(rlobj)
        self._ViMode__vi_insert_mode = None

    def __repr__(self):
        return '<ViMode>'

    def process_keyevent(self, keyinfo):

        def nop(e):
            pass

        keytuple = keyinfo.tuple()
        if keytuple in self.exit_dispatch:
            if lineobj.EndOfLine(self.l_buffer) == 0:
                raise EOFError
        dispatch_func = self.key_dispatch.get(keytuple, self.vi_key)
        log('readline from keyboard:%s->%s' % (keytuple, dispatch_func))
        r = None
        if dispatch_func:
            r = dispatch_func(keyinfo)
            self.l_buffer.push_undo()
        self.previous_func = dispatch_func
        if r:
            self._update_line()
            return True
        return False

    def init_editing_mode(self, e):
        """Initialize vi editingmode"""
        self.show_all_if_ambiguous = 'on'
        self.key_dispatch = {}
        self._ViMode__vi_insert_mode = None
        self._vi_command = None
        self._vi_command_edit = None
        self._vi_key_find_char = None
        self._vi_key_find_direction = True
        self._vi_yank_buffer = None
        self._vi_multiplier1 = ''
        self._vi_multiplier2 = ''
        self._vi_undo_stack = []
        self._vi_undo_cursor = -1
        self._vi_current = None
        self._vi_search_text = ''
        self._vi_search_position = 0
        self.vi_save_line()
        self.vi_set_insert_mode(True)
        for c in range(ord(' '), 127):
            self._bind_key('%s' % chr(c), self.vi_key)

        self._bind_key('BackSpace', self.vi_backspace)
        self._bind_key('Escape', self.vi_escape)
        self._bind_key('Return', self.vi_accept_line)
        self._bind_key('Left', self.backward_char)
        self._bind_key('Right', self.forward_char)
        self._bind_key('Home', self.beginning_of_line)
        self._bind_key('End', self.end_of_line)
        self._bind_key('Delete', self.delete_char)
        self._bind_key('Control-d', self.vi_eof)
        self._bind_key('Control-z', self.vi_eof)
        self._bind_key('Control-r', self.vi_redo)
        self._bind_key('Up', self.vi_arrow_up)
        self._bind_key('Control-p', self.vi_up)
        self._bind_key('Down', self.vi_arrow_down)
        self._bind_key('Control-n', self.vi_down)
        self._bind_key('Tab', self.vi_complete)

    def vi_key(self, e):
        if not self._vi_command:
            self._vi_command = ViCommand(self)
        elif self._vi_command.is_end:
            if self._vi_command.is_edit:
                self._vi_command_edit = self._vi_command
            self._vi_command = ViCommand(self)
        self._vi_command.add_char(e.char)

    def vi_error(self):
        self._bell()

    def vi_get_is_insert_mode(self):
        return self._ViMode__vi_insert_mode

    vi_is_insert_mode = property(vi_get_is_insert_mode)

    def vi_escape(self, e):
        if self.vi_is_insert_mode:
            if self._vi_command:
                self._vi_command.add_char(e.char)
            else:
                self._vi_command = ViCommand(self)
            self.vi_set_insert_mode(False)
            self.l_buffer.point = lineobj.PrevChar
        elif self._vi_command and self._vi_command.is_replace_one:
            self._vi_command.add_char(e.char)
        else:
            self.vi_error()

    def vi_backspace(self, e):
        if self._vi_command:
            self._vi_command.add_char(e.char)
        else:
            self._vi_do_backspace(self._vi_command)

    def _vi_do_backspace(self, vi_cmd):
        if self.vi_is_insert_mode or (self._vi_command and self._vi_command.is_search):
            if self.l_buffer.point > 0:
                self.l_buffer.point -= 1
                if self.l_buffer.overwrite:
                    try:
                        prev = self._vi_undo_stack[self._vi_undo_cursor][1][self.l_buffer.point]
                        self.l_buffer.line_buffer[self.l_buffer.point] = prev
                    except IndexError:
                        del self.l_buffer.line_buffer[self.l_buffer.point]

                else:
                    self.vi_save_line()
                    del self.l_buffer.line_buffer[self.l_buffer.point]

    def vi_accept_line(self, e):
        if self._vi_command:
            if self._vi_command.is_search:
                self._vi_command.do_search()
                return False
        self._vi_command = None
        self.vi_set_insert_mode(True)
        self._vi_undo_stack = []
        self._vi_undo_cursor = -1
        self._vi_current = None
        if self.l_buffer.line_buffer:
            self.add_history(self.l_buffer.copy())
        return self.accept_line(e)

    def vi_eof(self, e):
        raise EOFError

    def vi_set_insert_mode(self, value):
        if self._ViMode__vi_insert_mode == value:
            return
        self._ViMode__vi_insert_mode = value
        if value:
            self.vi_save_line()
            self.cursor_size = 25
        else:
            self.cursor_size = 100

    def vi_undo_restart(self):
        tpl_undo = (self.l_buffer.point, self.l_buffer.line_buffer[:])
        self._vi_undo_stack = [tpl_undo]
        self._vi_undo_cursor = 0

    def vi_save_line(self):
        if self._vi_undo_stack:
            if self._vi_undo_cursor >= 0:
                del self._vi_undo_stack[self._vi_undo_cursor + 1:]
        tpl_undo = (
         self.l_buffer.point, self.l_buffer.line_buffer[:])
        if not self._vi_undo_stack or self._vi_undo_stack[self._vi_undo_cursor][1] != tpl_undo[1]:
            self._vi_undo_stack.append(tpl_undo)
            self._vi_undo_cursor += 1

    def vi_undo_prepare(self):
        if self._vi_undo_cursor == len(self._vi_undo_stack) - 1:
            self.vi_save_line()

    def vi_undo(self, do_pop=True):
        self.vi_undo_prepare()
        if not self._vi_undo_stack or self._vi_undo_cursor <= 0:
            self.vi_error()
            return
        self._vi_undo_cursor -= 1
        self.vi_undo_assign()

    def vi_undo_all(self):
        self.vi_undo_prepare()
        if self._vi_undo_cursor > 0:
            self._vi_undo_cursor = 0
            self.vi_undo_assign()
        else:
            self.vi_error()

    def vi_undo_assign(self):
        tpl_undo = self._vi_undo_stack[self._vi_undo_cursor]
        self.l_buffer.line_buffer = tpl_undo[1][:]
        self.l_buffer.point = tpl_undo[0]

    def vi_redo(self, e):
        if self._vi_undo_cursor >= len(self._vi_undo_stack) - 1:
            self.vi_error()
            return
        self._vi_undo_cursor += 1
        self.vi_undo_assign()

    def vi_search(self, rng):
        for i in rng:
            line_history = self._history.history[i]
            pos = line_history.get_line_text().find(self._vi_search_text)
            if pos >= 0:
                self._vi_search_position = i
                self._history.history_cursor = i
                self.l_buffer.line_buffer = list(line_history.line_buffer)
                self.l_buffer.point = pos
                self.vi_undo_restart()
                return True

        self._bell()
        return False

    def vi_search_first(self):
        text = ''.join(self.l_buffer.line_buffer[1:])
        if text:
            self._vi_search_text = text
            self._vi_search_position = len(self._history.history) - 1
        elif self._vi_search_text:
            self._vi_search_position -= 1
        else:
            self.vi_error()
            self.vi_undo()
            return
        if not self.vi_search(list(range(self._vi_search_position, -1, -1))):
            self.vi_undo()

    def vi_search_again_backward(self):
        self.vi_search(list(range(self._vi_search_position - 1, -1, -1)))

    def vi_search_again_forward(self):
        self.vi_search(list(range(self._vi_search_position + 1, len(self._history.history))))

    def vi_up(self, e):
        if self._history.history_cursor == len(self._history.history):
            self._vi_current = self.l_buffer.line_buffer[:]
        self._history.previous_history(self.l_buffer)
        if self.vi_is_insert_mode:
            self.end_of_line(e)
        else:
            self.beginning_of_line(e)
        self.vi_undo_restart()

    def vi_down(self, e):
        if self._history.history_cursor >= len(self._history.history):
            self.vi_error()
            return
        if self._history.history_cursor < len(self._history.history) - 1:
            self._history.next_history(self.l_buffer)
            if self.vi_is_insert_mode:
                self.end_of_line(e)
            else:
                self.beginning_of_line(e)
            self.vi_undo_restart()
        elif self._vi_current is not None:
            self._history.history_cursor = len(self._history.history)
            self.l_buffer.line_buffer = self._vi_current
            self.end_of_line(e)
            if not self.vi_is_insert_mode:
                if self.l_buffer.point > 0:
                    self.l_buffer.point -= 1
            self._vi_current = None
        else:
            self.vi_error()
            return

    def vi_arrow_up(self, e):
        self.vi_set_insert_mode(True)
        self.vi_up(e)
        self.vi_save_line()

    def vi_arrow_down(self, e):
        self.vi_set_insert_mode(True)
        self.vi_down(e)
        self.vi_save_line()

    def vi_complete(self, e):
        text = self.l_buffer.get_line_text()
        if text:
            if not text.isspace():
                return self.complete(e)
            return self.vi_key(e)


_VI_BEGIN = 'vi_begin'
_VI_MULTI1 = 'vi_multi1'
_VI_ACTION = 'vi_action'
_VI_MULTI2 = 'vi_multi2'
_VI_MOTION = 'vi_motion'
_VI_MOTION_ARGUMENT = 'vi_motion_argument'
_VI_REPLACE_ONE = 'vi_replace_one'
_VI_TEXT = 'vi_text'
_VI_SEARCH = 'vi_search'
_VI_END = 'vi_end'

class ViCommand:

    def __init__(self, readline):
        self.readline = readline
        self.lst_char = []
        self.state = _VI_BEGIN
        self.action = self.movement
        self.motion = None
        self.motion_argument = None
        self.text = None
        self.pos_motion = None
        self.is_edit = False
        self.is_overwrite = False
        self.is_error = False
        self.is_star = False
        self.delete_left = 0
        self.delete_right = 0
        self.readline._vi_multiplier1 = ''
        self.readline._vi_multiplier2 = ''
        self.set_override_multiplier(0)
        self.skip_multipler = False
        self.tabstop = 4
        self.dct_fcn = {ord('$'): self.key_dollar, 
         ord('^'): self.key_hat, 
         ord(';'): self.key_semicolon, 
         ord(','): self.key_comma, 
         ord('%'): self.key_percent, 
         ord('.'): self.key_dot, 
         ord('/'): self.key_slash, 
         ord('*'): self.key_star, 
         ord('|'): self.key_bar, 
         ord('~'): self.key_tilde, 
         8: self.key_backspace}

    def add_char(self, char):
        self.lst_char.append(char)
        if self.state == _VI_BEGIN:
            if self.readline.vi_is_insert_mode:
                self.readline.vi_save_line()
                self.state = _VI_TEXT
        if self.state == _VI_SEARCH:
            if char == '\x08':
                self.key_backspace(char)
            else:
                self.set_text(char)
            return
        if self.state == _VI_TEXT:
            if char == '\x1b':
                self.escape(char)
            elif char == '\t':
                ts = self.tabstop
                ws = ' ' * (ts - self.readline.l_buffer.point % ts)
                self.set_text(ws)
            elif char == '\x08':
                self.key_backspace(char)
            else:
                self.set_text(char)
            return
        if self.state == _VI_MOTION_ARGUMENT:
            self.set_motion_argument(char)
            return
        if self.state == _VI_REPLACE_ONE:
            self.replace_one(char)
            return
        try:
            fcn_instance = self.dct_fcn[ord(char)]
        except:
            fcn_instance = getattr(self, 'key_%s' % char, None)

        if fcn_instance:
            fcn_instance(char)
            return
        if char.isdigit():
            self.key_digit(char)
            return
        self.error()

    def set_text(self, text):
        if self.text is None:
            self.text = text
        else:
            self.text += text
        self.set_buffer(text)

    def set_buffer(self, text):
        for char in text:
            if not self.char_isprint(char):
                continue
            else:
                if self.is_overwrite:
                    if self.readline.l_buffer.point < len(self.readline.l_buffer.line_buffer):
                        self.readline.l_buffer.line_buffer[self.readline.l_buffer.point] = char
                    else:
                        self.readline.l_buffer.line_buffer.append(char)
                else:
                    self.readline.l_buffer.line_buffer.insert(self.readline.l_buffer.point, char)
                self.readline.l_buffer.point += 1

    def replace_one(self, char):
        if char == '\x1b':
            self.end()
            return
        self.is_edit = True
        self.readline.vi_save_line()
        times = self.get_multiplier()
        cursor = self.readline.l_buffer.point
        self.readline.l_buffer.line_buffer[cursor:cursor + times] = char * times
        if times > 1:
            self.readline.l_buffer.point += times - 1
        self.end()

    def char_isprint(self, char):
        return ord(char) >= ord(' ') and ord(char) <= ord('~')

    def key_dollar(self, char):
        self.motion = self.motion_end_in_line
        self.delete_right = 1
        self.state = _VI_MOTION
        self.apply()

    def key_hat(self, char):
        self.motion = self.motion_beginning_of_line
        self.state = _VI_MOTION
        self.apply()

    def key_0(self, char):
        if self.state in [_VI_BEGIN, _VI_ACTION]:
            self.key_hat(char)
        else:
            self.key_digit(char)

    def key_digit(self, char):
        if self.state in [_VI_BEGIN, _VI_MULTI1]:
            self.readline._vi_multiplier1 += char
            self.readline._vi_multiplier2 = ''
            self.state = _VI_MULTI1
        elif self.state in [_VI_ACTION, _VI_MULTI2]:
            self.readline._vi_multiplier2 += char
            self.state = _VI_MULTI2

    def key_w(self, char):
        if self.action == self.change:
            self.key_e(char)
            return
        self.motion = self.motion_word_short
        self.state = _VI_MOTION
        self.apply()

    def key_W(self, char):
        if self.action == self.change:
            self.key_E(char)
            return
        self.motion = self.motion_word_long
        self.state = _VI_MOTION
        self.apply()

    def key_e(self, char):
        self.motion = self.motion_end_short
        self.state = _VI_MOTION
        self.delete_right = 1
        self.apply()

    def key_E(self, char):
        self.motion = self.motion_end_long
        self.state = _VI_MOTION
        self.delete_right = 1
        self.apply()

    def key_b(self, char):
        self.motion = self.motion_back_short
        self.state = _VI_MOTION
        self.apply()

    def key_B(self, char):
        self.motion = self.motion_back_long
        self.state = _VI_MOTION
        self.apply()

    def key_f(self, char):
        self.readline._vi_key_find_direction = True
        self.motion = self.motion_find_char_forward
        self.delete_right = 1
        self.state = _VI_MOTION_ARGUMENT

    def key_F(self, char):
        self.readline._vi_key_find_direction = False
        self.motion = self.motion_find_char_backward
        self.delete_left = 1
        self.state = _VI_MOTION_ARGUMENT

    def key_t(self, char):
        self.motion = self.motion_to_char_forward
        self.delete_right = 1
        self.state = _VI_MOTION_ARGUMENT

    def key_T(self, char):
        self.motion = self.motion_to_char_backward
        self.state = _VI_MOTION_ARGUMENT

    def key_j(self, char):
        self.readline.vi_down(ViEvent(char))
        self.state = _VI_END

    def key_k(self, char):
        self.readline.vi_up(ViEvent(char))
        self.state = _VI_END

    def key_semicolon(self, char):
        if self.readline._vi_key_find_char is None:
            self.error()
            return
        if self.readline._vi_key_find_direction:
            self.motion = self.motion_find_char_forward
        else:
            self.motion = self.motion_find_char_backward
        self.set_motion_argument(self.readline._vi_key_find_char)

    def key_comma(self, char):
        if self.readline._vi_key_find_char is None:
            self.error()
            return
        if self.readline._vi_key_find_direction:
            self.motion = self.motion_find_char_backward
        else:
            self.motion = self.motion_find_char_forward
        self.set_motion_argument(self.readline._vi_key_find_char)

    def key_percent(self, char):
        """find matching <([{}])>"""
        self.motion = self.motion_matching
        self.delete_right = 1
        self.state = _VI_MOTION
        self.apply()

    def key_dot(self, char):
        vi_cmd_edit = self.readline._vi_command_edit
        if not vi_cmd_edit:
            return
        if vi_cmd_edit.is_star:
            self.key_star(char)
            return
        if self.has_multiplier():
            count = self.get_multiplier()
        else:
            count = 0
        vi_cmd = ViCommand(self.readline)
        if count >= 1:
            vi_cmd.set_override_multiplier(count)
            vi_cmd_edit.set_override_multiplier(count)
        elif vi_cmd_edit.override_multiplier:
            vi_cmd.set_override_multiplier(vi_cmd_edit.override_multiplier)
        for char in vi_cmd_edit.lst_char:
            vi_cmd.add_char(char)

        if vi_cmd_edit.is_overwrite:
            if self.readline.l_buffer.point > 0:
                self.readline.l_buffer.point -= 1
        self.readline.vi_set_insert_mode(False)
        self.end()

    def key_slash(self, char):
        self.readline.vi_save_line()
        self.readline.l_buffer.line_buffer = ['/']
        self.readline.l_buffer.point = 1
        self.state = _VI_SEARCH

    def key_star(self, char):
        self.is_star = True
        self.is_edit = True
        self.readline.vi_save_line()
        completions = self.readline._get_completions()
        if completions:
            text = ' '.join(completions) + ' '
            self.readline.l_buffer.line_buffer[self.readline.begidx:self.readline.endidx + 1] = list(text)
            prefix_len = self.readline.endidx - self.readline.begidx
            self.readline.l_buffer.point += len(text) - prefix_len
            self.readline.vi_set_insert_mode(True)
        else:
            self.error()
        self.state = _VI_TEXT

    def key_bar(self, char):
        self.motion = self.motion_column
        self.state = _VI_MOTION
        self.apply()

    def key_tilde(self, char):
        self.is_edit = True
        self.readline.vi_save_line()
        for i in range(self.get_multiplier()):
            try:
                c = self.readline.l_buffer.line_buffer[self.readline.l_buffer.point]
                if c.isupper():
                    self.readline.l_buffer.line_buffer[self.readline.l_buffer.point] = c.lower()
                elif c.islower():
                    self.readline.l_buffer.line_buffer[self.readline.l_buffer.point] = c.upper()
                self.readline.l_buffer.point += 1
            except IndexError:
                break

        self.end()

    def key_h(self, char):
        self.motion = self.motion_left
        self.state = _VI_MOTION
        self.apply()

    def key_backspace(self, char):
        if self.state in [_VI_TEXT, _VI_SEARCH]:
            if not self.text or len(self.text):
                self.text = self.text[:-1]
                try:
                    self.lst_char.pop()
                    self.lst_char.pop()
                except IndexError:
                    pass

        else:
            self.key_h(char)
        self.readline._vi_do_backspace(self)
        if self.state == _VI_SEARCH:
            if not self.readline.l_buffer.line_buffer:
                self.state = _VI_BEGIN

    def key_l(self, char):
        self.motion = self.motion_right
        self.state = _VI_MOTION
        self.apply()

    def key_i(self, char):
        self.is_edit = True
        self.state = _VI_TEXT
        self.readline.vi_set_insert_mode(True)

    def key_I(self, char):
        self.is_edit = True
        self.state = _VI_TEXT
        self.readline.vi_set_insert_mode(True)
        self.readline.l_buffer.point = 0

    def key_a(self, char):
        self.is_edit = True
        self.state = _VI_TEXT
        self.readline.vi_set_insert_mode(True)
        if len(self.readline.l_buffer.line_buffer):
            self.readline.l_buffer.point += 1

    def key_A(self, char):
        self.is_edit = True
        self.state = _VI_TEXT
        self.readline.vi_set_insert_mode(True)
        self.readline.l_buffer.point = len(self.readline.l_buffer.line_buffer)

    def key_d(self, char):
        self.is_edit = True
        self.state = _VI_ACTION
        self.action = self.delete

    def key_D(self, char):
        self.is_edit = True
        self.state = _VI_ACTION
        self.action = self.delete_end_of_line
        self.apply()

    def key_x(self, char):
        self.is_edit = True
        self.state = _VI_ACTION
        self.action = self.delete_char
        self.apply()

    def key_X(self, char):
        self.is_edit = True
        self.state = _VI_ACTION
        self.action = self.delete_prev_char
        self.apply()

    def key_s(self, char):
        self.is_edit = True
        i1 = self.readline.l_buffer.point
        i2 = self.readline.l_buffer.point + self.get_multiplier()
        self.skip_multipler = True
        self.readline.vi_set_insert_mode(True)
        del self.readline.l_buffer.line_buffer[i1:i2]
        self.state = _VI_TEXT

    def key_S(self, char):
        self.is_edit = True
        self.readline.vi_set_insert_mode(True)
        self.readline.l_buffer.line_buffer = []
        self.readline.l_buffer.point = 0
        self.state = _VI_TEXT

    def key_c(self, char):
        self.is_edit = True
        self.state = _VI_ACTION
        self.action = self.change

    def key_C(self, char):
        self.is_edit = True
        self.readline.vi_set_insert_mode(True)
        del self.readline.l_buffer.line_buffer[self.readline.l_buffer.point:]
        self.state = _VI_TEXT

    def key_r(self, char):
        self.state = _VI_REPLACE_ONE

    def key_R(self, char):
        self.is_edit = True
        self.is_overwrite = True
        self.readline.l_buffer.overwrite = True
        self.readline.vi_set_insert_mode(True)
        self.state = _VI_TEXT

    def key_y(self, char):
        self._state = _VI_ACTION
        self.action = self.yank

    def key_Y(self, char):
        self.readline._vi_yank_buffer = self.readline.l_buffer.get_line_text()
        self.end()

    def key_p(self, char):
        if not self.readline._vi_yank_buffer:
            return
        self.is_edit = True
        self.readline.vi_save_line()
        self.readline.l_buffer.point += 1
        self.readline.l_buffer.insert_text(self.readline._vi_yank_buffer * self.get_multiplier())
        self.readline.l_buffer.point -= 1
        self.state = _VI_END

    def key_P(self, char):
        if not self.readline._vi_yank_buffer:
            return
        self.is_edit = True
        self.readline.vi_save_line()
        self.readline.l_buffer.insert_text(self.readline._vi_yank_buffer * self.get_multiplier())
        self.readline.l_buffer.point -= 1
        self.state = _VI_END

    def key_u(self, char):
        self.readline.vi_undo()
        self.state = _VI_END

    def key_U(self, char):
        self.readline.vi_undo_all()
        self.state = _VI_END

    def key_v(self, char):
        editor = ViExternalEditor(self.readline.l_buffer.line_buffer)
        self.readline.l_buffer.line_buffer = list(editor.result)
        self.readline.l_buffer.point = 0
        self.is_edit = True
        self.state = _VI_END

    def error(self):
        self.readline._bell()
        self.is_error = True

    def state_is_end(self):
        return self.state == _VI_END

    is_end = property(state_is_end)

    def state_is_search(self):
        return self.state == _VI_SEARCH

    is_search = property(state_is_search)

    def state_is_replace_one(self):
        return self.state == _VI_REPLACE_ONE

    is_replace_one = property(state_is_replace_one)

    def do_search(self):
        self.readline.vi_search_first()
        self.state = _VI_END

    def key_n(self, char):
        self.readline.vi_search_again_backward()
        self.state = _VI_END

    def key_N(self, char):
        self.readline.vi_search_again_forward()
        self.state = _VI_END

    def motion_beginning_of_line(self, line, index=0, count=1, **kw):
        return 0

    def motion_end_in_line(self, line, index=0, count=1, **kw):
        return max(0, len(self.readline.l_buffer.line_buffer) - 1)

    def motion_word_short(self, line, index=0, count=1, **kw):
        return vi_pos_word_short(line, index, count)

    def motion_word_long(self, line, index=0, count=1, **kw):
        return vi_pos_word_long(line, index, count)

    def motion_end_short(self, line, index=0, count=1, **kw):
        return vi_pos_end_short(line, index, count)

    def motion_end_long(self, line, index=0, count=1, **kw):
        return vi_pos_end_long(line, index, count)

    def motion_back_short(self, line, index=0, count=1, **kw):
        return vi_pos_back_short(line, index, count)

    def motion_back_long(self, line, index=0, count=1, **kw):
        return vi_pos_back_long(line, index, count)

    def motion_find_char_forward(self, line, index=0, count=1, char=None):
        self.readline._vi_key_find_char = char
        return vi_pos_find_char_forward(line, char, index, count)

    def motion_find_char_backward(self, line, index=0, count=1, char=None):
        self.readline._vi_key_find_char = char
        return vi_pos_find_char_backward(line, char, index, count)

    def motion_to_char_forward(self, line, index=0, count=1, char=None):
        return vi_pos_to_char_forward(line, char, index, count)

    def motion_to_char_backward(self, line, index=0, count=1, char=None):
        return vi_pos_to_char_backward(line, char, index, count)

    def motion_left(self, line, index=0, count=1, char=None):
        return max(0, index - count)

    def motion_right(self, line, index=0, count=1, char=None):
        return min(len(line), index + count)

    def motion_matching(self, line, index=0, count=1, char=None):
        return vi_pos_matching(line, index)

    def motion_column(self, line, index=0, count=1, char=None):
        return max(0, count - 1)

    def has_multiplier(self):
        return self.override_multiplier or self.readline._vi_multiplier1 or self.readline._vi_multiplier2

    def get_multiplier(self):
        if self.override_multiplier:
            return int(self.override_multiplier)
        if self.readline._vi_multiplier1 == '':
            m1 = 1
        else:
            m1 = int(self.readline._vi_multiplier1)
        if self.readline._vi_multiplier2 == '':
            m2 = 1
        else:
            m2 = int(self.readline._vi_multiplier2)
        return m1 * m2

    def set_override_multiplier(self, count):
        self.override_multiplier = count

    def apply(self):
        if self.motion:
            self.pos_motion = self.motion((self.readline.l_buffer.line_buffer), (self.readline.l_buffer.point), (self.get_multiplier()),
              char=(self.motion_argument))
            if self.pos_motion < 0:
                self.error()
                return
        self.action()
        if self.state != _VI_TEXT:
            self.end()

    def movement(self):
        if self.pos_motion <= len(self.readline.l_buffer.line_buffer):
            self.readline.l_buffer.point = self.pos_motion
        else:
            self.readline.l_buffer.point = len(self.readline.l_buffer.line_buffer) - 1

    def yank(self):
        if self.pos_motion > self.readline.l_buffer.point:
            s = self.readline.l_buffer.line_buffer[self.readline.l_buffer.point:self.pos_motion + self.delete_right]
        else:
            index = max(0, self.pos_motion - self.delete_left)
            s = self.readline.l_buffer.line_buffer[index:self.readline.l_buffer.point + self.delete_right]
        self.readline._vi_yank_buffer = s

    def delete(self):
        self.readline.vi_save_line()
        self.yank()
        if self.pos_motion > self.readline.l_buffer.point:
            del self.readline.l_buffer.line_buffer[self.readline.l_buffer.point:self.pos_motion + self.delete_right]
            if self.readline.l_buffer.point > len(self.readline.l_buffer.line_buffer):
                self.readline.l_buffer.point = len(self.readline.l_buffer.line_buffer)
        else:
            index = max(0, self.pos_motion - self.delete_left)
            del self.readline.l_buffer.line_buffer[index:self.readline.l_buffer.point + self.delete_right]
            self.readline.l_buffer.point = index

    def delete_end_of_line(self):
        self.readline.vi_save_line()
        line_text = self.readline.l_buffer.get_line_text()
        line_text = line_text[:self.readline.l_buffer.point]
        self.readline.l_buffer.set_line(line_text)
        if self.readline.l_buffer.point > 0:
            self.readline.l_buffer.point -= 1

    def delete_char(self):
        self.pos_motion = self.readline.l_buffer.point + self.get_multiplier()
        self.delete()
        end = max(0, len(self.readline.l_buffer) - 1)
        if self.readline.l_buffer.point > end:
            self.readline.l_buffer.point = end

    def delete_prev_char(self):
        self.pos_motion = self.readline.l_buffer.point - self.get_multiplier()
        self.delete()

    def change(self):
        self.readline.vi_set_insert_mode(True)
        self.delete()
        self.skip_multipler = True
        self.state = _VI_TEXT

    def escape(self, char):
        if self.state == _VI_TEXT:
            if not self.skip_multipler:
                times = self.get_multiplier()
                if times > 1:
                    if self.text:
                        extra = self.text * (times - 1)
                        self.set_buffer(extra)
        self.state = _VI_END

    def set_motion_argument(self, char):
        self.motion_argument = char
        self.apply()

    def end(self):
        self.state = _VI_END
        if self.readline.l_buffer.point >= len(self.readline.l_buffer.line_buffer):
            self.readline.l_buffer.point = max(0, len(self.readline.l_buffer.line_buffer) - 1)


class ViExternalEditor:

    def __init__(self, line):
        if type(line) is type([]):
            line = ''.join(line)
        file_tmp = self.get_tempfile()
        fp_tmp = self.file_open(file_tmp, 'w')
        fp_tmp.write(line)
        fp_tmp.close()
        self.run_editor(file_tmp)
        fp_tmp = self.file_open(file_tmp, 'r')
        self.result = fp_tmp.read()
        fp_tmp.close()
        self.file_remove(file_tmp)

    def get_tempfile(self):
        import tempfile
        return tempfile.mktemp(prefix='readline-', suffix='.py')

    def file_open(self, filename, mode):
        return file(filename, mode)

    def file_remove(self, filename):
        os.remove(filename)

    def get_editor(self):
        try:
            return os.environ['EDITOR']
        except KeyError:
            return 'notepad'

    def run_editor(self, filename):
        cmd = '%s %s' % (self.get_editor(), filename)
        self.run_command(cmd)

    def run_command(self, command):
        os.system(command)


class ViEvent:

    def __init__(self, char):
        self.char = char


def vi_is_word(char):
    log('xx vi_is_word: type(%s), %s' % (type(char), char))
    return char.isalpha() or char.isdigit() or char == '_'


def vi_is_space(char):
    return char.isspace()


def vi_is_word_or_space(char):
    return vi_is_word(char) or vi_is_space(char)


def vi_pos_word_short(line, index=0, count=1):
    try:
        for i in range(count):
            in_word = vi_is_word(line[index])
            if not in_word:
                while not vi_is_word(line[index]):
                    index += 1

            else:
                while vi_is_word(line[index]):
                    index += 1

            while vi_is_space(line[index]):
                index += 1

        return index
    except IndexError:
        return len(line)


def vi_pos_word_long(line, index=0, count=1):
    try:
        for i in range(count):
            in_space = vi_is_space(line[index])
            if not in_space:
                while not vi_is_space(line[index]):
                    index += 1

            while vi_is_space(line[index]):
                index += 1

        return index
    except IndexError:
        return len(line)


def vi_pos_end_short--- This code section failed: ---

 L.1036         0  SETUP_EXCEPT        132  'to 132'

 L.1037         2  SETUP_LOOP          124  'to 124'
                4  LOAD_GLOBAL              range
                6  LOAD_FAST                'count'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  GET_ITER         
             12_0  COME_FROM           120  '120'
             12_1  COME_FROM            92  '92'
               12  FOR_ITER            122  'to 122'
               14  STORE_FAST               'i'

 L.1038        16  LOAD_FAST                'index'
               18  LOAD_CONST               1
               20  INPLACE_ADD      
               22  STORE_FAST               'index'

 L.1039        24  SETUP_LOOP           50  'to 50'
             26_0  COME_FROM            46  '46'
               26  LOAD_GLOBAL              vi_is_space
               28  LOAD_FAST                'line'
               30  LOAD_FAST                'index'
               32  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.1040        38  LOAD_FAST                'index'
               40  LOAD_CONST               1
               42  INPLACE_ADD      
               44  STORE_FAST               'index'
               46  JUMP_BACK            26  'to 26'
             48_0  COME_FROM            36  '36'
               48  POP_BLOCK        
             50_0  COME_FROM_LOOP       24  '24'

 L.1041        50  LOAD_GLOBAL              vi_is_word
               52  LOAD_FAST                'line'
               54  LOAD_FAST                'index'
               56  BINARY_SUBSCR    
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  STORE_FAST               'in_word'

 L.1042        62  LOAD_FAST                'in_word'
               64  POP_JUMP_IF_TRUE     94  'to 94'

 L.1043        66  SETUP_LOOP          120  'to 120'
             68_0  COME_FROM            88  '88'
               68  LOAD_GLOBAL              vi_is_word_or_space
               70  LOAD_FAST                'line'
               72  LOAD_FAST                'index'
               74  BINARY_SUBSCR    
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_JUMP_IF_TRUE     90  'to 90'

 L.1044        80  LOAD_FAST                'index'
               82  LOAD_CONST               1
               84  INPLACE_ADD      
               86  STORE_FAST               'index'
               88  JUMP_BACK            68  'to 68'
             90_0  COME_FROM            78  '78'
               90  POP_BLOCK        
               92  JUMP_BACK            12  'to 12'
             94_0  COME_FROM            64  '64'

 L.1046        94  SETUP_LOOP          120  'to 120'
             96_0  COME_FROM           116  '116'
               96  LOAD_GLOBAL              vi_is_word
               98  LOAD_FAST                'line'
              100  LOAD_FAST                'index'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L.1047       108  LOAD_FAST                'index'
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  STORE_FAST               'index'
              116  JUMP_BACK            96  'to 96'
            118_0  COME_FROM           106  '106'
              118  POP_BLOCK        
            120_0  COME_FROM_LOOP       94  '94'
            120_1  COME_FROM_LOOP       66  '66'
              120  JUMP_BACK            12  'to 12'
              122  POP_BLOCK        
            124_0  COME_FROM_LOOP        2  '2'

 L.1048       124  LOAD_FAST                'index'
              126  LOAD_CONST               1
              128  BINARY_SUBTRACT  
              130  RETURN_VALUE     
            132_0  COME_FROM_EXCEPT      0  '0'

 L.1049       132  DUP_TOP          
              134  LOAD_GLOBAL              IndexError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   164  'to 164'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L.1050       146  LOAD_GLOBAL              max
              148  LOAD_CONST               0
              150  LOAD_GLOBAL              len
              152  LOAD_FAST                'line'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  LOAD_CONST               1
              158  BINARY_SUBTRACT  
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  RETURN_VALUE     
            164_0  COME_FROM           138  '138'
              164  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 92


def vi_pos_end_long(line, index=0, count=1):
    try:
        for i in range(count):
            index += 1
            while vi_is_space(line[index]):
                index += 1

            while not vi_is_space(line[index]):
                index += 1

        return index - 1
    except IndexError:
        return max(0, len(line) - 1)


class vi_list(list):
    __doc__ = 'This is a list that cannot have a negative index'

    def __getitem__(self, key):
        try:
            if int(key) < 0:
                raise IndexError
        except ValueError:
            pass

        return list.__getitem__(self, key)


def vi_pos_back_short--- This code section failed: ---

 L.1075         0  LOAD_GLOBAL              vi_list
                2  LOAD_FAST                'line'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'line'

 L.1076         8  SETUP_EXCEPT        140  'to 140'

 L.1077        10  SETUP_LOOP          132  'to 132'
               12  LOAD_GLOBAL              range
               14  LOAD_FAST                'count'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  GET_ITER         
             20_0  COME_FROM           128  '128'
             20_1  COME_FROM           100  '100'
               20  FOR_ITER            130  'to 130'
               22  STORE_FAST               'i'

 L.1078        24  LOAD_FAST                'index'
               26  LOAD_CONST               1
               28  INPLACE_SUBTRACT 
               30  STORE_FAST               'index'

 L.1079        32  SETUP_LOOP           58  'to 58'
             34_0  COME_FROM            54  '54'
               34  LOAD_GLOBAL              vi_is_space
               36  LOAD_FAST                'line'
               38  LOAD_FAST                'index'
               40  BINARY_SUBSCR    
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L.1080        46  LOAD_FAST                'index'
               48  LOAD_CONST               1
               50  INPLACE_SUBTRACT 
               52  STORE_FAST               'index'
               54  JUMP_BACK            34  'to 34'
             56_0  COME_FROM            44  '44'
               56  POP_BLOCK        
             58_0  COME_FROM_LOOP       32  '32'

 L.1081        58  LOAD_GLOBAL              vi_is_word
               60  LOAD_FAST                'line'
               62  LOAD_FAST                'index'
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  STORE_FAST               'in_word'

 L.1082        70  LOAD_FAST                'in_word'
               72  POP_JUMP_IF_FALSE   102  'to 102'

 L.1083        74  SETUP_LOOP          128  'to 128'
             76_0  COME_FROM            96  '96'
               76  LOAD_GLOBAL              vi_is_word
               78  LOAD_FAST                'line'
               80  LOAD_FAST                'index'
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  POP_JUMP_IF_FALSE    98  'to 98'

 L.1084        88  LOAD_FAST                'index'
               90  LOAD_CONST               1
               92  INPLACE_SUBTRACT 
               94  STORE_FAST               'index'
               96  JUMP_BACK            76  'to 76'
             98_0  COME_FROM            86  '86'
               98  POP_BLOCK        
              100  JUMP_BACK            20  'to 20'
            102_0  COME_FROM            72  '72'

 L.1086       102  SETUP_LOOP          128  'to 128'
            104_0  COME_FROM           124  '124'
              104  LOAD_GLOBAL              vi_is_word_or_space
              106  LOAD_FAST                'line'
              108  LOAD_FAST                'index'
              110  BINARY_SUBSCR    
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  POP_JUMP_IF_TRUE    126  'to 126'

 L.1087       116  LOAD_FAST                'index'
              118  LOAD_CONST               1
              120  INPLACE_SUBTRACT 
              122  STORE_FAST               'index'
              124  JUMP_BACK           104  'to 104'
            126_0  COME_FROM           114  '114'
              126  POP_BLOCK        
            128_0  COME_FROM_LOOP      102  '102'
            128_1  COME_FROM_LOOP       74  '74'
              128  JUMP_BACK            20  'to 20'
              130  POP_BLOCK        
            132_0  COME_FROM_LOOP       10  '10'

 L.1088       132  LOAD_FAST                'index'
              134  LOAD_CONST               1
              136  BINARY_ADD       
              138  RETURN_VALUE     
            140_0  COME_FROM_EXCEPT      8  '8'

 L.1089       140  DUP_TOP          
              142  LOAD_GLOBAL              IndexError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   158  'to 158'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L.1090       154  LOAD_CONST               0
              156  RETURN_VALUE     
            158_0  COME_FROM           146  '146'
              158  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 100


def vi_pos_back_long(line, index=0, count=1):
    line = vi_list(line)
    try:
        for i in range(count):
            index -= 1
            while vi_is_space(line[index]):
                index -= 1

            while not vi_is_space(line[index]):
                index -= 1

        return index + 1
    except IndexError:
        return 0


def vi_pos_find_char_forward(line, char, index=0, count=1):
    try:
        for i in range(count):
            index += 1
            while line[index] != char:
                index += 1

        return index
    except IndexError:
        return -1


def vi_pos_find_char_backward(line, char, index=0, count=1):
    try:
        for i in range(count):
            index -= 1
            while True:
                if index < 0:
                    return -1
                if line[index] == char:
                    break
                else:
                    index -= 1

        return index
    except IndexError:
        return -1


def vi_pos_to_char_forward(line, char, index=0, count=1):
    index = vi_pos_find_char_forward(line, char, index, count)
    if index > 0:
        return index - 1
    return index


def vi_pos_to_char_backward(line, char, index=0, count=1):
    index = vi_pos_find_char_backward(line, char, index, count)
    if index >= 0:
        return index + 1
    return index


_vi_dct_matching = {'<':('>', 1), 
 '>':('<', -1),  '(':(')', 1), 
 ')':('(', -1),  '[':(']', 1), 
 ']':('[', -1),  '{':('}', 1), 
 '}':('{', -1)}

def vi_pos_matching(line, index=0):
    """find matching <([{}])>"""
    anchor = None
    target = None
    delta = 1
    count = 0
    try:
        while True:
            if anchor is None:
                try:
                    target, delta = _vi_dct_matching[line[index]]
                    anchor = line[index]
                    count = 1
                except KeyError:
                    index += 1
                    continue

            else:
                if index < 0:
                    return -1
                if line[index] == anchor:
                    count += 1
                elif line[index] == target:
                    count -= 1
                    if count == 0:
                        return index
            index += delta

    except IndexError:
        return -1