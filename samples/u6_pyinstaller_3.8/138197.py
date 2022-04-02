# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\rlmain.py
from __future__ import print_function, unicode_literals, absolute_import
import sys, os, re, time
from glob import glob
from . import release
from .py3k_compat import callable, execfile
import pyreadline.lineeditor.lineobj as lineobj
import pyreadline.lineeditor.history as history
import pyreadline.clipboard as clipboard
import pyreadline.console as console
import pyreadline.logger as logger
from pyreadline.keysyms.common import make_KeyPress_from_keydescr
from pyreadline.unicode_helper import ensure_unicode, ensure_str
from .logger import log
from .modes import editingmodes
from .error import ReadlineError, GetSetError
in_ironpython = 'IronPython' in sys.version
if in_ironpython:
    import System
    default_prompt = '>>> '
else:
    default_prompt = ''

class MockConsoleError(Exception):
    pass


class MockConsole(object):
    __doc__ = 'object used during refactoring. Should raise errors when someone tries to use it.\n    '

    def __setattr__(self, x):
        raise MockConsoleError('Should not try to get attributes from MockConsole')

    def cursor(self, size=50):
        pass


class BaseReadline(object):

    def __init__(self):
        self.allow_ctrl_c = False
        self.ctrl_c_tap_time_interval = 0.3
        self.debug = False
        self.bell_style = 'none'
        self.mark = -1
        self.console = MockConsole()
        self.disable_readline = False
        self.editingmodes = [mode(self) for mode in editingmodes]
        for mode in self.editingmodes:
            mode.init_editing_mode(None)
        else:
            self.mode = self.editingmodes[0]
            self.read_inputrc()
            log('\n'.join(self.mode.rl_settings_to_string()))
            self.callback = None

    def parse_and_bind--- This code section failed: ---

 L.  72       0_2  SETUP_FINALLY       318  'to 318'

 L.  73         4  LOAD_GLOBAL              log
                6  LOAD_STR                 'parse_and_bind("%s")'
                8  LOAD_FAST                'string'
               10  BINARY_MODULO    
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L.  74        16  LOAD_FAST                'string'
               18  LOAD_METHOD              startswith
               20  LOAD_STR                 '#'
               22  CALL_METHOD_1         1  ''
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L.  75        26  POP_BLOCK        
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            24  '24'

 L.  76        32  LOAD_FAST                'string'
               34  LOAD_METHOD              startswith
               36  LOAD_STR                 'set'
               38  CALL_METHOD_1         1  ''
               40  POP_JUMP_IF_FALSE   166  'to 166'

 L.  77        42  LOAD_GLOBAL              re
               44  LOAD_METHOD              compile
               46  LOAD_STR                 'set\\s+([-a-zA-Z0-9]+)\\s+(.+)\\s*$'
               48  CALL_METHOD_1         1  ''
               50  LOAD_METHOD              match
               52  LOAD_FAST                'string'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'm'

 L.  78        58  LOAD_FAST                'm'
               60  POP_JUMP_IF_FALSE   148  'to 148'

 L.  79        62  LOAD_FAST                'm'
               64  LOAD_METHOD              group
               66  LOAD_CONST               1
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'var_name'

 L.  80        72  LOAD_FAST                'm'
               74  LOAD_METHOD              group
               76  LOAD_CONST               2
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'val'

 L.  81        82  SETUP_FINALLY       110  'to 110'

 L.  82        84  LOAD_GLOBAL              setattr
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                mode
               90  LOAD_FAST                'var_name'
               92  LOAD_METHOD              replace
               94  LOAD_STR                 '-'
               96  LOAD_STR                 '_'
               98  CALL_METHOD_2         2  ''
              100  LOAD_FAST                'val'
              102  CALL_FUNCTION_3       3  ''
              104  POP_TOP          
              106  POP_BLOCK        
              108  JUMP_ABSOLUTE       160  'to 160'
            110_0  COME_FROM_FINALLY    82  '82'

 L.  83       110  DUP_TOP          
              112  LOAD_GLOBAL              AttributeError
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   144  'to 144'
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L.  84       124  LOAD_GLOBAL              log
              126  LOAD_STR                 'unknown var="%s" val="%s"'
              128  LOAD_FAST                'var_name'
              130  LOAD_FAST                'val'
              132  BUILD_TUPLE_2         2 
              134  BINARY_MODULO    
              136  CALL_FUNCTION_1       1  ''
              138  POP_TOP          
              140  POP_EXCEPT       
              142  JUMP_ABSOLUTE       160  'to 160'
            144_0  COME_FROM           116  '116'
              144  END_FINALLY      
              146  JUMP_FORWARD        160  'to 160'
            148_0  COME_FROM            60  '60'

 L.  86       148  LOAD_GLOBAL              log
              150  LOAD_STR                 'bad set "%s"'
              152  LOAD_FAST                'string'
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
            160_0  COME_FROM           146  '146'

 L.  87       160  POP_BLOCK        
              162  LOAD_CONST               None
              164  RETURN_VALUE     
            166_0  COME_FROM            40  '40'

 L.  88       166  LOAD_GLOBAL              re
              168  LOAD_METHOD              compile
              170  LOAD_STR                 '\\s*(.+)\\s*:\\s*([-a-zA-Z]+)\\s*$'
              172  CALL_METHOD_1         1  ''
              174  LOAD_METHOD              match
              176  LOAD_FAST                'string'
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'm'

 L.  89       182  LOAD_FAST                'm'
          184_186  POP_JUMP_IF_FALSE   314  'to 314'

 L.  90       188  LOAD_FAST                'm'
              190  LOAD_METHOD              group
              192  LOAD_CONST               1
              194  CALL_METHOD_1         1  ''
              196  STORE_FAST               'key'

 L.  91       198  LOAD_FAST                'm'
              200  LOAD_METHOD              group
              202  LOAD_CONST               2
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'func_name'

 L.  92       208  LOAD_FAST                'func_name'
              210  LOAD_METHOD              replace
              212  LOAD_STR                 '-'
              214  LOAD_STR                 '_'
              216  CALL_METHOD_2         2  ''
              218  STORE_FAST               'py_name'

 L.  93       220  SETUP_FINALLY       238  'to 238'

 L.  94       222  LOAD_GLOBAL              getattr
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                mode
              228  LOAD_FAST                'py_name'
              230  CALL_FUNCTION_2       2  ''
              232  STORE_FAST               'func'
              234  POP_BLOCK        
              236  JUMP_FORWARD        300  'to 300'
            238_0  COME_FROM_FINALLY   220  '220'

 L.  95       238  DUP_TOP          
              240  LOAD_GLOBAL              AttributeError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   298  'to 298'
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L.  96       254  LOAD_GLOBAL              log
              256  LOAD_STR                 'unknown func key="%s" func="%s"'
              258  LOAD_FAST                'key'
              260  LOAD_FAST                'func_name'
              262  BUILD_TUPLE_2         2 
              264  BINARY_MODULO    
              266  CALL_FUNCTION_1       1  ''
              268  POP_TOP          

 L.  97       270  LOAD_FAST                'self'
              272  LOAD_ATTR                debug
          274_276  POP_JUMP_IF_FALSE   290  'to 290'

 L.  98       278  LOAD_GLOBAL              print
              280  LOAD_STR                 'pyreadline parse_and_bind error, unknown function to bind: "%s"'
              282  LOAD_FAST                'func_name'
              284  BINARY_MODULO    
              286  CALL_FUNCTION_1       1  ''
              288  POP_TOP          
            290_0  COME_FROM           274  '274'

 L.  99       290  POP_EXCEPT       
              292  POP_BLOCK        
              294  LOAD_CONST               None
              296  RETURN_VALUE     
            298_0  COME_FROM           244  '244'
              298  END_FINALLY      
            300_0  COME_FROM           236  '236'

 L. 100       300  LOAD_FAST                'self'
              302  LOAD_ATTR                mode
              304  LOAD_METHOD              _bind_key
              306  LOAD_FAST                'key'
              308  LOAD_FAST                'func'
              310  CALL_METHOD_2         2  ''
              312  POP_TOP          
            314_0  COME_FROM           184  '184'
              314  POP_BLOCK        
              316  JUMP_FORWARD        340  'to 340'
            318_0  COME_FROM_FINALLY     0  '0'

 L. 101       318  POP_TOP          
              320  POP_TOP          
              322  POP_TOP          

 L. 102       324  LOAD_GLOBAL              log
              326  LOAD_STR                 'error'
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          

 L. 103       332  RAISE_VARARGS_0       0  'reraise'
              334  POP_EXCEPT       
              336  JUMP_FORWARD        340  'to 340'
              338  END_FINALLY      
            340_0  COME_FROM           336  '336'
            340_1  COME_FROM           316  '316'

Parse error at or near `LOAD_CONST' instruction at offset 28

    def _set_prompt(self, prompt):
        self.mode.prompt = prompt

    def _get_prompt(self):
        return self.mode.prompt

    prompt = property(_get_prompt, _set_prompt)

    def get_line_buffer(self):
        """Return the current contents of the line buffer."""
        return self.mode.l_buffer.get_line_text()

    def insert_text(self, string):
        """Insert text into the command line."""
        self.mode.insert_text(string)

    def read_init_file(self, filename=None):
        """Parse a readline initialization file. The default filename is the last filename used."""
        log('read_init_file("%s")' % filename)

    def add_history(self, line):
        """Append a line to the history buffer, as if it was the last line typed."""
        self.mode._history.add_history(line)

    def get_current_history_length(self):
        """Return the number of lines currently in the history.
        (This is different from get_history_length(), which returns 
        the maximum number of lines that will be written to a history file.)"""
        return self.mode._history.get_current_history_length()

    def get_history_length(self):
        """Return the desired length of the history file.

        Negative values imply unlimited history file size."""
        return self.mode._history.get_history_length()

    def set_history_length(self, length):
        """Set the number of lines to save in the history file.

        write_history_file() uses this value to truncate the history file
        when saving. Negative values imply unlimited history file size.
        """
        self.mode._history.set_history_length(length)

    def get_history_item(self, index):
        """Return the current contents of history item at index."""
        return self.mode._history.get_history_item(index)

    def clear_history(self):
        """Clear readline history"""
        self.mode._history.clear_history()

    def read_history_file(self, filename=None):
        """Load a readline history file. The default filename is ~/.history."""
        if filename is None:
            filename = self.mode._history.history_filename
        log('read_history_file from %s' % ensure_unicode(filename))
        self.mode._history.read_history_file(filename)

    def write_history_file(self, filename=None):
        """Save a readline history file. The default filename is ~/.history."""
        self.mode._history.write_history_file(filename)

    def set_completer(self, function=None):
        """Set or remove the completer function.

        If function is specified, it will be used as the new completer
        function; if omitted or None, any completer function already
        installed is removed. The completer function is called as
        function(text, state), for state in 0, 1, 2, ..., until it returns a
        non-string value. It should return the next possible completion
        starting with text.
        """
        log('set_completer')
        self.mode.completer = function

    def get_completer(self):
        """Get the completer function. 
        """
        log('get_completer')
        return self.mode.completer

    def get_begidx(self):
        """Get the beginning index of the readline tab-completion scope."""
        return self.mode.begidx

    def get_endidx(self):
        """Get the ending index of the readline tab-completion scope."""
        return self.mode.endidx

    def set_completer_delims(self, string):
        """Set the readline word delimiters for tab-completion."""
        self.mode.completer_delims = string

    def get_completer_delims(self):
        """Get the readline word delimiters for tab-completion."""
        if sys.version_info[0] < 3:
            return self.mode.completer_delims.encode('ascii')
        return self.mode.completer_delims

    def set_startup_hook(self, function=None):
        """Set or remove the startup_hook function.

        If function is specified, it will be used as the new startup_hook
        function; if omitted or None, any hook function already installed is
        removed. The startup_hook function is called with no arguments just
        before readline prints the first prompt.

        """
        self.mode.startup_hook = function

    def set_pre_input_hook(self, function=None):
        """Set or remove the pre_input_hook function.

        If function is specified, it will be used as the new pre_input_hook
        function; if omitted or None, any hook function already installed is
        removed. The pre_input_hook function is called with no arguments
        after the first prompt has been printed and just before readline
        starts reading input characters.

        """
        self.mode.pre_input_hook = function

    def _bell(self):
        pass

    def readline(self, prompt=''):
        raise NotImplementedError

    def process_keyevent(self, keyinfo):
        return self.mode.process_keyevent(keyinfo)

    def readline_setup(self, prompt=''):
        return self.mode.readline_setup(prompt)

    def keyboard_poll(self):
        return self.mode._readline_from_keyboard_poll()

    def callback_handler_install(self, prompt, callback):
        """bool readline_callback_handler_install ( string prompt, callback callback)
        Initializes the readline callback interface and terminal, prints the prompt and returns immediately
        """
        self.callback = callback
        self.readline_setup(prompt)

    def callback_handler_remove(self):
        """Removes a previously installed callback handler and restores terminal settings"""
        self.callback = None

    def callback_read_char(self):
        """Reads a character and informs the readline callback interface when a line is received"""
        if self.keyboard_poll():
            line = self.get_line_buffer() + '\n'
            self.add_history(self.mode.l_buffer)
            self.callback(line)

    def read_inputrc(self, inputrcpath=os.path.expanduser(ensure_str('~/pyreadlineconfig.ini'))):
        modes = dict([(x.mode, x) for x in self.editingmodes])
        mode = self.editingmodes[0].mode

        def setmode(name):
            self.mode = modes[name]

        def bind_key(key, name):
            import types
            if callable(name):
                modes[mode]._bind_keykeytypes.MethodTypenamemodes[mode]
            else:
                if hasattr(modes[mode], name):
                    modes[mode]._bind_keykeygetattr(modes[mode], name)
                else:
                    print("Trying to bind unknown command '%s' to key '%s'" % (name, key))

        def un_bind_key(key):
            keyinfo = make_KeyPress_from_keydescr(key).tuple()
            if keyinfo in modes[mode].key_dispatch:
                del modes[mode].key_dispatch[keyinfo]

        def bind_exit_key(key):
            modes[mode]._bind_exit_key(key)

        def un_bind_exit_key(key):
            keyinfo = make_KeyPress_from_keydescr(key).tuple()
            if keyinfo in modes[mode].exit_dispatch:
                del modes[mode].exit_dispatch[keyinfo]

        def setkill_ring_to_clipboard(killring):
            import pyreadline.lineeditor.lineobj
            pyreadline.lineeditor.lineobj.kill_ring_to_clipboard = killring

        def sethistoryfilename(filename):
            self.mode._history.history_filename = os.path.expanduser(ensure_str(filename))

        def setbellstyle(mode):
            self.bell_style = mode

        def disable_readline(mode):
            self.disable_readline = mode

        def sethistorylength(length):
            self.mode._history.history_length = int(length)

        def allow_ctrl_c(mode):
            log('allow_ctrl_c:%s:%s' % (self.allow_ctrl_c, mode))
            self.allow_ctrl_c = mode

        def setbellstyle(mode):
            self.bell_style = mode

        def show_all_if_ambiguous(mode):
            self.mode.show_all_if_ambiguous = mode

        def ctrl_c_tap_time_interval(mode):
            self.ctrl_c_tap_time_interval = mode

        def mark_directories(mode):
            self.mode.mark_directories = mode

        def completer_delims(delims):
            self.mode.completer_delims = delims

        def complete_filesystem(delims):
            self.mode.complete_filesystem = delims.lower()

        def enable_ipython_paste_for_paths(boolean):
            self.mode.enable_ipython_paste_for_paths = boolean

        def debug_output(on, filename='pyreadline_debug_log.txt'):
            if on in ('on', 'on_nologfile'):
                self.debug = True
            elif on == 'on':
                logger.start_file_log(filename)
                logger.start_socket_log()
                logger.log('STARTING LOG')
            else:
                if on == 'on_nologfile':
                    logger.start_socket_log()
                    logger.log('STARTING LOG')
                else:
                    logger.log('STOPING LOG')
                    logger.stop_file_log()
                    logger.stop_socket_log()

        _color_trtable = {'black':0, 
         'darkred':4,  'darkgreen':2,  'darkyellow':6, 
         'darkblue':1,  'darkmagenta':5,  'darkcyan':3, 
         'gray':7,  'red':12,  'green':10, 
         'yellow':14,  'blue':9,  'magenta':13, 
         'cyan':11,  'white':15}

        def set_prompt_color(color):
            self.prompt_color = self._color_trtable.getcolor.lower()7

        def set_input_color(color):
            self.command_color = self._color_trtable.getcolor.lower()7

        loc = {'branch':release.branch, 
         'version':release.version, 
         'mode':mode, 
         'modes':modes, 
         'set_mode':setmode, 
         'bind_key':bind_key, 
         'disable_readline':disable_readline, 
         'bind_exit_key':bind_exit_key, 
         'un_bind_key':un_bind_key, 
         'un_bind_exit_key':un_bind_exit_key, 
         'bell_style':setbellstyle, 
         'mark_directories':mark_directories, 
         'show_all_if_ambiguous':show_all_if_ambiguous, 
         'completer_delims':completer_delims, 
         'complete_filesystem':complete_filesystem, 
         'debug_output':debug_output, 
         'history_filename':sethistoryfilename, 
         'history_length':sethistorylength, 
         'set_prompt_color':set_prompt_color, 
         'set_input_color':set_input_color, 
         'allow_ctrl_c':allow_ctrl_c, 
         'ctrl_c_tap_time_interval':ctrl_c_tap_time_interval, 
         'kill_ring_to_clipboard':setkill_ring_to_clipboard, 
         'enable_ipython_paste_for_paths':enable_ipython_paste_for_paths}
        if os.path.isfile(inputrcpath):
            try:
                execfile(inputrcpath, loc, loc)
            except Exception as x:
                try:
                    raise
                    import traceback
                    print('Error reading .pyinputrc', file=(sys.stderr))
                    filepath, lineno = traceback.extract_tb(sys.exc_traceback)[1][:2]
                    print(('Line: %s in file %s' % (lineno, filepath)), file=(sys.stderr))
                    print(x, file=(sys.stderr))
                    raise ReadlineError('Error reading .pyinputrc')
                finally:
                    x = None
                    del x


class Readline(BaseReadline):
    __doc__ = 'Baseclass for readline based on a console\n    '

    def __init__(self):
        BaseReadline.__init__(self)
        self.console = console.Console()
        self.selection_color = self.console.saveattr << 4
        self.command_color = None
        self.prompt_color = None
        self.size = self.console.size()

    def _bell(self):
        """ring the bell if requested."""
        if self.bell_style == 'none':
            pass
        elif self.bell_style == 'visible':
            raise NotImplementedError('Bellstyle visible is not implemented yet.')
        else:
            if self.bell_style == 'audible':
                self.console.bell()
            else:
                raise ReadlineError('Bellstyle %s unknown.' % self.bell_style)

    def _clear_after(self):
        c = self.console
        x, y = c.pos()
        w, h = c.size()
        c.rectangle((x, y, w + 1, y + 1))
        c.rectangle((0, y + 1, w, min(y + 3, h)))

    def _set_cursor(self):
        c = self.console
        xc, yc = self.prompt_end_pos
        w, h = c.size()
        xc += self.mode.l_buffer.visible_line_width()
        while xc >= w:
            xc -= w
            yc += 1

        c.posxcyc

    def _print_prompt(self):
        c = self.console
        x, y = c.pos()
        n = c.write_scrollingself.promptself.prompt_color
        self.prompt_begin_pos = (x, y - n)
        self.prompt_end_pos = c.pos()
        self.size = c.size()

    def _update_prompt_pos(self, n):
        if n != 0:
            bx, by = self.prompt_begin_pos
            ex, ey = self.prompt_end_pos
            self.prompt_begin_pos = (bx, by - n)
            self.prompt_end_pos = (ex, ey - n)

    def _update_line(self):
        c = self.console
        l_buffer = self.mode.l_buffer
        c.cursor(0)
        (c.pos)(*self.prompt_begin_pos)
        self._print_prompt()
        ltext = l_buffer.quoted_text()
        if l_buffer.enable_selection and l_buffer.selection_mark >= 0:
            start = len(l_buffer[:l_buffer.selection_mark].quoted_text())
            stop = len(l_buffer[:l_buffer.point].quoted_text())
            if start > stop:
                stop, start = start, stop
            n = c.write_scrollingltext[:start]self.command_color
            n = c.write_scrollingltext[start:stop]self.selection_color
            n = c.write_scrollingltext[stop:]self.command_color
        else:
            n = c.write_scrollingltextself.command_color
        x, y = c.pos()
        w, h = c.size()
        if y >= h - 1 or n > 0:
            c.scroll_window(-1)
            c.scroll((0, 0, w, h), 0, -1)
            n += 1
        else:
            self._update_prompt_pos(n)
            if hasattr(c, 'clear_to_end_of_window'):
                c.clear_to_end_of_window()
            else:
                self._clear_after()
        c.cursor(1, size=(self.mode.cursor_size))
        self._set_cursor()

    def callback_read_char(self):
        """Reads a character and informs the readline callback interface when a line is received"""
        if self.keyboard_poll():
            line = self.get_line_buffer() + '\n'
            self.console.write('\r\n')
            self.add_history(self.mode.l_buffer)
            self.callback(line)

    def event_available(self):
        return self.console.peek() or len(self.paste_line_buffer) > 0

    def _readline_from_keyboard(self):
        while self._readline_from_keyboard_poll():
            break

    def _readline_from_keyboard_poll(self):
        pastebuffer = self.mode.paste_line_buffer
        if len(pastebuffer) > 0:
            self.l_buffer = lineobj.ReadLineTextBuffer(pastebuffer[0])
            self._update_line()
            self.mode.paste_line_buffer = pastebuffer[1:]
            return True
        c = self.console

        def nop(e):
            pass

        try:
            event = c.getkeypress()
        except KeyboardInterrupt:
            event = self.handle_ctrl_c()
        else:
            try:
                result = self.mode.process_keyevent(event.keyinfo)
            except EOFError:
                logger.stop_logging()
                raise
            else:
                self._update_line()
                return result

    def readline_setup(self, prompt=''):
        BaseReadline.readline_setupselfprompt
        self._print_prompt()
        self._update_line()

    def readline(self, prompt=''):
        self.readline_setup(prompt)
        self.ctrl_c_timeout = time.time()
        self._readline_from_keyboard()
        self.console.write('\r\n')
        log('returning(%s)' % self.get_line_buffer())
        return self.get_line_buffer() + '\n'

    def handle_ctrl_c(self):
        from pyreadline.keysyms.common import KeyPress
        from pyreadline.console.event import Event
        log('KBDIRQ')
        event = Event(0, 0)
        event.char = 'c'
        event.keyinfo = KeyPress('c', shift=False, control=True, meta=False,
          keyname=None)
        if self.allow_ctrl_c:
            now = time.time()
            if now - self.ctrl_c_timeout < self.ctrl_c_tap_time_interval:
                log('Raise KeyboardInterrupt')
                raise KeyboardInterrupt
            else:
                self.ctrl_c_timeout = now
        else:
            raise KeyboardInterrupt
        return event