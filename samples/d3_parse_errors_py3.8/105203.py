# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\keyboard\_xorg.py
"""
The keyboard implementation for *Xorg*.
"""
import enum, threading, Xlib.display, Xlib.ext, Xlib.ext.xtest, Xlib.X, Xlib.XK, Xlib.protocol, Xlib.keysymdef.xkb
from pynput._util import NotifierMixin
from pynput._util.xorg import alt_mask, alt_gr_mask, display_manager, index_to_shift, keyboard_mapping, ListenerMixin, numlock_mask, shift_to_index, symbol_to_keysym
from pynput._util.xorg_keysyms import CHARS, DEAD_KEYS, KEYPAD_KEYS, KEYSYMS, SYMBOLS
from . import _base

class KeyCode(_base.KeyCode):
    _PLATFORM_EXTENSIONS = ('_symbol', )
    _symbol = None

    @classmethod
    def _from_symbol(cls, symbol, **kwargs):
        """Creates a key from a symbol.

        :param str symbol: The symbol name.

        :return: a key code
        """
        keysym = Xlib.XK.string_to_keysym(symbol)
        if keysym:
            return (cls.from_vk)(keysym, _symbol=symbol, **kwargs)
        if not keysym:
            try:
                symbol = 'XK_' + symbol
                return (cls.from_vk)(
 getattr(Xlib.keysymdef.xkb, symbol, 0), _symbol=symbol, **kwargs)
            except:
                return (cls.from_vk)(
 SYMBOLS.get(symbol, (0, ))[0], _symbol=symbol, **kwargs)

    @classmethod
    def _from_media(cls, name, **kwargs):
        """Creates a media key from a partial name.

        :param str name: The name. The actual symbol name will be this string
            with ``'XF86Audio'`` prepended.

        :return: a key code
        """
        return (cls._from_symbol)(('XF86Audio' + name), **kwargs)


class Key(enum.Enum):
    alt = KeyCode._from_symbol('Alt_L')
    alt_l = KeyCode._from_symbol('Alt_L')
    alt_r = KeyCode._from_symbol('Alt_R')
    alt_gr = KeyCode._from_symbol('Mode_switch')
    backspace = KeyCode._from_symbol('BackSpace')
    caps_lock = KeyCode._from_symbol('Caps_Lock')
    cmd = KeyCode._from_symbol('Super_L')
    cmd_l = KeyCode._from_symbol('Super_L')
    cmd_r = KeyCode._from_symbol('Super_R')
    ctrl = KeyCode._from_symbol('Control_L')
    ctrl_l = KeyCode._from_symbol('Control_L')
    ctrl_r = KeyCode._from_symbol('Control_R')
    delete = KeyCode._from_symbol('Delete')
    down = KeyCode._from_symbol('Down')
    end = KeyCode._from_symbol('End')
    enter = KeyCode._from_symbol('Return')
    esc = KeyCode._from_symbol('Escape')
    f1 = KeyCode._from_symbol('F1')
    f2 = KeyCode._from_symbol('F2')
    f3 = KeyCode._from_symbol('F3')
    f4 = KeyCode._from_symbol('F4')
    f5 = KeyCode._from_symbol('F5')
    f6 = KeyCode._from_symbol('F6')
    f7 = KeyCode._from_symbol('F7')
    f8 = KeyCode._from_symbol('F8')
    f9 = KeyCode._from_symbol('F9')
    f10 = KeyCode._from_symbol('F10')
    f11 = KeyCode._from_symbol('F11')
    f12 = KeyCode._from_symbol('F12')
    f13 = KeyCode._from_symbol('F13')
    f14 = KeyCode._from_symbol('F14')
    f15 = KeyCode._from_symbol('F15')
    f16 = KeyCode._from_symbol('F16')
    f17 = KeyCode._from_symbol('F17')
    f18 = KeyCode._from_symbol('F18')
    f19 = KeyCode._from_symbol('F19')
    f20 = KeyCode._from_symbol('F20')
    home = KeyCode._from_symbol('Home')
    left = KeyCode._from_symbol('Left')
    page_down = KeyCode._from_symbol('Page_Down')
    page_up = KeyCode._from_symbol('Page_Up')
    right = KeyCode._from_symbol('Right')
    shift = KeyCode._from_symbol('Shift_L')
    shift_l = KeyCode._from_symbol('Shift_L')
    shift_r = KeyCode._from_symbol('Shift_R')
    space = KeyCode._from_symbol('space', char=' ')
    tab = KeyCode._from_symbol('Tab')
    up = KeyCode._from_symbol('Up')
    media_play_pause = KeyCode._from_media('Play')
    media_volume_mute = KeyCode._from_media('Mute')
    media_volume_down = KeyCode._from_media('LowerVolume')
    media_volume_up = KeyCode._from_media('RaiseVolume')
    media_previous = KeyCode._from_media('Prev')
    media_next = KeyCode._from_media('Next')
    insert = KeyCode._from_symbol('Insert')
    menu = KeyCode._from_symbol('Menu')
    num_lock = KeyCode._from_symbol('Num_Lock')
    pause = KeyCode._from_symbol('Pause')
    print_screen = KeyCode._from_symbol('Print')
    scroll_lock = KeyCode._from_symbol('Scroll_Lock')


class Controller(NotifierMixin, _base.Controller):
    _KeyCode = KeyCode
    _Key = Key
    CTRL_MASK = Xlib.X.ControlMask
    SHIFT_MASK = Xlib.X.ShiftMask

    def __init__(self, *args, **kwargs):
        (super(Controller, self).__init__)(*args, **kwargs)
        self._display = Xlib.display.Display()
        self._keyboard_mapping = None
        self._borrows = {}
        self._borrow_lock = threading.RLock()
        self.ALT_MASK = alt_mask(self._display)
        self.ALT_GR_MASK = alt_gr_mask(self._display)

    def __del__(self):
        if self._display:
            self._display.close()

    @property
    def keyboard_mapping(self):
        """A mapping from *keysyms* to *key codes*.

        Each value is the tuple ``(key_code, shift_state)``. By sending an
        event with the specified *key code* and shift state, the specified
        *keysym* will be touched.
        """
        if not self._keyboard_mapping:
            self._update_keyboard_mapping()
        return self._keyboard_mapping

    def _handle(self, key, is_press):
        """Resolves a key identifier and sends a keyboard event.

        :param event: The *X* keyboard event.

        :param int keysym: The keysym to handle.
        """
        event = Xlib.display.event.KeyPress if is_press else Xlib.display.event.KeyRelease
        keysym = self._keysym(key)
        if keysym is None:
            raise self.InvalidKeyException(key)
        if key.vk is not None:
            with display_manager(self._display) as dm:
                Xlib.ext.xtest.fake_input(dm, Xlib.X.KeyPress if is_press else Xlib.X.KeyRelease, dm.keysym_to_keycode(key.vk))
        else:
            pass
        try:
            keycode, shift_state = self.keyboard_mapping[keysym]
            self._send_key(event, keycode, shift_state)
        except KeyError:
            with self._borrow_lock:
                keycode, index, count = self._borrows[keysym]
                self._send_key(event, keycode, index_to_shift(self._display, index))
                count += 1 if is_press else -1
                self._borrows[keysym] = (keycode, index, count)
        else:
            self._emit('_on_fake_event', key, is_press)

    def _keysym(self, key):
        """Converts a key to a *keysym*.

        :param KeyCode key: The key code to convert.
        """
        if key.is_dead:
            return self._resolve_dead(key)
        return None or self._resolve_special(key) or self._resolve_normal(key) or self._resolve_borrowed(key) or self._resolve_borrowing(key)

    def _send_key(self, event, keycode, shift_state):
        """Sends a single keyboard event.

        :param event: The *X* keyboard event.

        :param int keycode: The calculated keycode.

        :param int shift_state: The shift state. The actual value used is
            :attr:`shift_state` or'd with this value.
        """
        with display_manager(self._display) as dm:
            with self.modifiers as modifiers:
                window = dm.get_input_focus().focus
                send_event = getattr(window, 'send_event', lambda event: dm.send_event(window, event))
                send_event(event(detail=keycode,
                  state=(shift_state | self._shift_mask(modifiers)),
                  time=0,
                  root=(dm.screen().root),
                  window=window,
                  same_screen=0,
                  child=(Xlib.X.NONE),
                  root_x=0,
                  root_y=0,
                  event_x=0,
                  event_y=0))

    def _resolve_dead--- This code section failed: ---

 L. 305         0  SETUP_FINALLY        24  'to 24'

 L. 306         2  LOAD_GLOBAL              SYMBOLS
                4  LOAD_GLOBAL              CHARS
                6  LOAD_FAST                'key'
                8  LOAD_ATTR                combining
               10  BINARY_SUBSCR    
               12  BINARY_SUBSCR    
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'keysym'
               18  STORE_FAST               '_'
               20  POP_BLOCK        
               22  JUMP_FORWARD         38  'to 38'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 307        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 308        30  POP_EXCEPT       
               32  LOAD_CONST               None
               34  RETURN_VALUE     
               36  END_FINALLY      
             38_0  COME_FROM            22  '22'

 L. 311        38  LOAD_FAST                'keysym'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                keyboard_mapping
               44  COMPARE_OP               not-in
               46  POP_JUMP_IF_FALSE    52  'to 52'

 L. 312        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'

 L. 314        52  LOAD_FAST                'keysym'
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 32

    def _resolve_special(self, key):
        """Tries to resolve a special key.

        A special key has the :attr:`~KeyCode.vk` attribute set.

        :param KeyCode key: The key to resolve.
        """
        if not key.vk:
            return
        return key.vk

    def _resolve_normal(self, key):
        """Tries to resolve a normal key.

        A normal key exists on the keyboard, and is typed by pressing
        and releasing a simple key, possibly in combination with a modifier.

        :param KeyCode key: The key to resolve.
        """
        keysym = self._key_to_keysym(key)
        if keysym is None:
            return
        if keysym not in self.keyboard_mapping:
            return
        return keysym

    def _resolve_borrowed--- This code section failed: ---

 L. 353         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _key_to_keysym
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'keysym'

 L. 354        10  LOAD_FAST                'keysym'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 355        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 357        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _borrow_lock
               26  SETUP_WITH           58  'to 58'
               28  POP_TOP          

 L. 358        30  LOAD_FAST                'keysym'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _borrows
               36  COMPARE_OP               not-in
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L. 359        40  POP_BLOCK        
               42  BEGIN_FINALLY    
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  POP_FINALLY           0  ''
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            38  '38'
               54  POP_BLOCK        
               56  BEGIN_FINALLY    
             58_0  COME_FROM_WITH       26  '26'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

 L. 361        64  LOAD_FAST                'keysym'
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 42

    def _resolve_borrowing--- This code section failed: ---

 L. 371         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              _key_to_keysym
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  ''
                8  STORE_DEREF              'keysym'

 L. 372        10  LOAD_DEREF               'keysym'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 373        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 375        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                _display
               26  LOAD_METHOD              get_keyboard_mapping
               28  LOAD_CONST               8
               30  LOAD_CONST               247
               32  CALL_METHOD_2         2  ''
               34  STORE_DEREF              'mapping'

 L. 377        36  LOAD_CODE                <code_object i2kc>
               38  LOAD_STR                 'Controller._resolve_borrowing.<locals>.i2kc'
               40  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               42  STORE_DEREF              'i2kc'

 L. 380        44  LOAD_CODE                <code_object kc2i>
               46  LOAD_STR                 'Controller._resolve_borrowing.<locals>.kc2i'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  STORE_DEREF              'kc2i'

 L. 384        52  LOAD_CLOSURE             'kc2i'
               54  LOAD_CLOSURE             'mapping'
               56  LOAD_CLOSURE             'self'
               58  BUILD_TUPLE_3         3 
               60  LOAD_CODE                <code_object reuse>
               62  LOAD_STR                 'Controller._resolve_borrowing.<locals>.reuse'
               64  MAKE_FUNCTION_8          'closure'
               66  STORE_FAST               'reuse'

 L. 394        68  LOAD_CLOSURE             'i2kc'
               70  LOAD_CLOSURE             'mapping'
               72  BUILD_TUPLE_2         2 
               74  LOAD_CODE                <code_object borrow>
               76  LOAD_STR                 'Controller._resolve_borrowing.<locals>.borrow'
               78  MAKE_FUNCTION_8          'closure'
               80  STORE_FAST               'borrow'

 L. 400        82  LOAD_CLOSURE             'self'
               84  BUILD_TUPLE_1         1 
               86  LOAD_CODE                <code_object overwrite>
               88  LOAD_STR                 'Controller._resolve_borrowing.<locals>.overwrite'
               90  MAKE_FUNCTION_8          'closure'
               92  STORE_FAST               'overwrite'

 L. 407        94  LOAD_CLOSURE             'kc2i'
               96  LOAD_CLOSURE             'keysym'
               98  LOAD_CLOSURE             'mapping'
              100  LOAD_CLOSURE             'self'
              102  BUILD_TUPLE_4         4 
              104  LOAD_CODE                <code_object register>
              106  LOAD_STR                 'Controller._resolve_borrowing.<locals>.register'
              108  MAKE_FUNCTION_8          'closure'
              110  STORE_FAST               'register'

 L. 415       112  SETUP_FINALLY       188  'to 188'

 L. 416       114  LOAD_GLOBAL              display_manager
              116  LOAD_DEREF               'self'
              118  LOAD_ATTR                _display
              120  CALL_FUNCTION_1       1  ''
              122  SETUP_WITH          176  'to 176'
              124  STORE_FAST               'dm'
              126  LOAD_DEREF               'self'
              128  LOAD_ATTR                _borrow_lock
              130  SETUP_WITH          166  'to 166'
              132  STORE_FAST               '_'

 L. 419       134  LOAD_FAST                'register'
              136  LOAD_FAST                'dm'
              138  BUILD_TUPLE_1         1 

 L. 420       140  LOAD_FAST                'reuse'
              142  CALL_FUNCTION_0       0  ''
              144  JUMP_IF_TRUE_OR_POP   156  'to 156'

 L. 421       146  LOAD_FAST                'borrow'
              148  CALL_FUNCTION_0       0  ''

 L. 420       150  JUMP_IF_TRUE_OR_POP   156  'to 156'

 L. 422       152  LOAD_FAST                'overwrite'
              154  CALL_FUNCTION_0       0  ''
            156_0  COME_FROM           150  '150'
            156_1  COME_FROM           144  '144'

 L. 419       156  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              158  CALL_FUNCTION_EX      0  'positional arguments only'
              160  POP_TOP          
              162  POP_BLOCK        
              164  BEGIN_FINALLY    
            166_0  COME_FROM_WITH      130  '130'
              166  WITH_CLEANUP_START
              168  WITH_CLEANUP_FINISH
              170  END_FINALLY      
              172  POP_BLOCK        
              174  BEGIN_FINALLY    
            176_0  COME_FROM_WITH      122  '122'
              176  WITH_CLEANUP_START
              178  WITH_CLEANUP_FINISH
              180  END_FINALLY      

 L. 423       182  LOAD_DEREF               'keysym'
              184  POP_BLOCK        
              186  RETURN_VALUE     
            188_0  COME_FROM_FINALLY   112  '112'

 L. 425       188  DUP_TOP          
              190  LOAD_GLOBAL              TypeError
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   208  'to 208'
              196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L. 426       202  POP_EXCEPT       
              204  LOAD_CONST               None
              206  RETURN_VALUE     
            208_0  COME_FROM           194  '194'
              208  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 204

    def _key_to_keysym--- This code section failed: ---

 L. 436         0  LOAD_GLOBAL              CHARS
                2  LOAD_METHOD              get
                4  LOAD_FAST                'key'
                6  LOAD_ATTR                char
                8  LOAD_CONST               None
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'symbol'

 L. 437        14  LOAD_FAST                'symbol'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 438        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 441        26  SETUP_FINALLY        38  'to 38'

 L. 442        28  LOAD_GLOBAL              symbol_to_keysym
               30  LOAD_FAST                'symbol'
               32  CALL_FUNCTION_1       1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY    26  '26'

 L. 443        38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 444        44  SETUP_FINALLY        64  'to 64'

 L. 445        46  LOAD_GLOBAL              SYMBOLS
               48  LOAD_FAST                'symbol'
               50  BINARY_SUBSCR    
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  POP_BLOCK        
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY    44  '44'

 L. 446        64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 447        70  POP_EXCEPT       
               72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  RETURN_VALUE     
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'

Parse error at or near `SETUP_FINALLY' instruction at offset 44

    def _shift_mask(self, modifiers):
        """The *X* modifier mask to apply for a set of modifiers.

        :param set modifiers: A set of active modifiers for which to get the
            shift mask.
        """
        return 0 | (self.ALT_MASK if Key.alt in modifiers else 0) | (self.ALT_GR_MASK if Key.alt_gr in modifiers else 0) | (self.CTRL_MASK if Key.ctrl in modifiers else 0) | (self.SHIFT_MASK if Key.shift in modifiers else 0)

    def _update_keyboard_mapping(self):
        """Updates the keyboard mapping.
        """
        with display_manager(self._display) as dm:
            self._keyboard_mapping = keyboard_mapping(dm)


@Controller._receiver
class Listener(ListenerMixin, _base.Listener):
    _EVENTS = (
     Xlib.X.KeyPress,
     Xlib.X.KeyRelease)
    _SPECIAL_KEYS = {key:key.value.vk for key in Key}
    _KEYPAD_KEYS = {KEYPAD_KEYS['KP_0']: KeyCode.from_char('0'), 
     KEYPAD_KEYS['KP_1']: KeyCode.from_char('1'), 
     KEYPAD_KEYS['KP_2']: KeyCode.from_char('2'), 
     KEYPAD_KEYS['KP_3']: KeyCode.from_char('3'), 
     KEYPAD_KEYS['KP_4']: KeyCode.from_char('4'), 
     KEYPAD_KEYS['KP_5']: KeyCode.from_char('5'), 
     KEYPAD_KEYS['KP_6']: KeyCode.from_char('6'), 
     KEYPAD_KEYS['KP_7']: KeyCode.from_char('7'), 
     KEYPAD_KEYS['KP_8']: KeyCode.from_char('8'), 
     KEYPAD_KEYS['KP_9']: KeyCode.from_char('9'), 
     KEYPAD_KEYS['KP_Add']: KeyCode.from_char('+'), 
     KEYPAD_KEYS['KP_Decimal']: KeyCode.from_char(','), 
     KEYPAD_KEYS['KP_Delete']: Key.delete, 
     KEYPAD_KEYS['KP_Divide']: KeyCode.from_char('/'), 
     KEYPAD_KEYS['KP_Down']: Key.down, 
     KEYPAD_KEYS['KP_End']: Key.end, 
     KEYPAD_KEYS['KP_Enter']: Key.enter, 
     KEYPAD_KEYS['KP_Equal']: KeyCode.from_char('='), 
     KEYPAD_KEYS['KP_F1']: Key.f1, 
     KEYPAD_KEYS['KP_F2']: Key.f2, 
     KEYPAD_KEYS['KP_F3']: Key.f3, 
     KEYPAD_KEYS['KP_F4']: Key.f4, 
     KEYPAD_KEYS['KP_Home']: Key.home, 
     KEYPAD_KEYS['KP_Insert']: Key.insert, 
     KEYPAD_KEYS['KP_Left']: Key.left, 
     KEYPAD_KEYS['KP_Multiply']: KeyCode.from_char('*'), 
     KEYPAD_KEYS['KP_Page_Down']: Key.page_down, 
     KEYPAD_KEYS['KP_Page_Up']: Key.page_up, 
     KEYPAD_KEYS['KP_Right']: Key.right, 
     KEYPAD_KEYS['KP_Space']: Key.space, 
     KEYPAD_KEYS['KP_Subtract']: KeyCode.from_char('-'), 
     KEYPAD_KEYS['KP_Tab']: Key.tab, 
     KEYPAD_KEYS['KP_Up']: Key.up}

    def __init__(self, *args, **kwargs):
        (super(Listener, self).__init__)(*args, **kwargs)
        self._keyboard_mapping = None

    def _run(self):
        with self._receive():
            super(Listener, self)._run()

    def _initialize(self, display):
        min_keycode = display.display.info.min_keycode
        keycode_count = display.display.info.max_keycode - min_keycode + 1
        self._keyboard_mapping = display.get_keyboard_mapping(min_keycode, keycode_count)

    def _handle(self, display, event):
        try:
            key = self._event_to_key(display, event)
        except IndexError:
            key = None
        else:
            if event.type == Xlib.X.KeyPress:
                self.on_press(key)
            elif event.type == Xlib.X.KeyRelease:
                self.on_release(key)

    def _suppress_start(self, display):
        display.screen().root.grab_keyboard(self._event_mask, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync, Xlib.X.CurrentTime)

    def _suppress_stop(self, display):
        display.ungrab_keyboard(Xlib.X.CurrentTime)

    def _on_fake_event(self, key, is_press):
        """The handler for fake press events sent by the controllers.

        :param KeyCode key: The key pressed.

        :param bool is_press: Whether this is a press event.
        """
        self.on_press if is_press else self.on_release(self._SPECIAL_KEYS.get(key.vk, key))

    def _keycode_to_keysym(self, display, keycode, index):
        """Converts a keycode and shift state index to a keysym.

        This method uses a simplified version of the *X* convention to locate
        the correct keysym in the display table: since this method is only used
        to locate special keys, alphanumeric keys are not treated specially.

        :param display: The current *X* display.

        :param keycode: The keycode.

        :param index: The shift state index.

        :return: a keysym
        """
        keysym = display.keycode_to_keysym(keycode, index)
        if keysym:
            return keysym
        if index & 2:
            return self._keycode_to_keysym(display, keycode, index & -3)
        if index & 1:
            return self._keycode_to_keysym(display, keycode, index & -2)
        return 0

    def _event_to_key--- This code section failed: ---

 L. 608         0  LOAD_FAST                'event'
                2  LOAD_ATTR                detail
                4  STORE_FAST               'keycode'

 L. 609         6  LOAD_GLOBAL              shift_to_index
                8  LOAD_FAST                'display'
               10  LOAD_FAST                'event'
               12  LOAD_ATTR                state
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'index'

 L. 612        18  LOAD_FAST                'self'
               20  LOAD_METHOD              _keycode_to_keysym
               22  LOAD_FAST                'display'
               24  LOAD_FAST                'keycode'
               26  LOAD_FAST                'index'
               28  CALL_METHOD_3         3  ''
               30  STORE_FAST               'keysym'

 L. 613        32  LOAD_FAST                'keysym'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _SPECIAL_KEYS
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 614        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _SPECIAL_KEYS
               46  LOAD_FAST                'keysym'
               48  BINARY_SUBSCR    
               50  RETURN_VALUE     
             52_0  COME_FROM            40  '40'

 L. 615        52  LOAD_FAST                'keysym'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _KEYPAD_KEYS
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE   120  'to 120'

 L. 618        62  SETUP_FINALLY       100  'to 100'

 L. 619        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _KEYPAD_KEYS

 L. 620        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _keycode_to_keysym

 L. 621        72  LOAD_FAST                'display'

 L. 622        74  LOAD_FAST                'keycode'

 L. 623        76  LOAD_GLOBAL              bool
               78  LOAD_FAST                'event'
               80  LOAD_ATTR                state
               82  LOAD_GLOBAL              numlock_mask
               84  LOAD_FAST                'display'
               86  CALL_FUNCTION_1       1  ''
               88  BINARY_AND       
               90  CALL_FUNCTION_1       1  ''

 L. 620        92  CALL_METHOD_3         3  ''

 L. 619        94  BINARY_SUBSCR    
               96  POP_BLOCK        
               98  RETURN_VALUE     
            100_0  COME_FROM_FINALLY    62  '62'

 L. 624       100  DUP_TOP          
              102  LOAD_GLOBAL              KeyError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   118  'to 118'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 626       114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM           106  '106'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            60  '60'

 L. 629       120  LOAD_GLOBAL              KEYSYMS
              122  LOAD_METHOD              get
              124  LOAD_FAST                'keysym'
              126  LOAD_CONST               None
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'name'

 L. 630       132  LOAD_FAST                'name'
              134  LOAD_CONST               None
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   224  'to 224'
              140  LOAD_FAST                'name'
              142  LOAD_GLOBAL              SYMBOLS
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   224  'to 224'

 L. 631       148  LOAD_FAST                'index'
              150  LOAD_CONST               1
              152  BINARY_AND       
              154  POP_JUMP_IF_FALSE   172  'to 172'
              156  LOAD_GLOBAL              SYMBOLS
              158  LOAD_FAST                'name'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               1
              164  BINARY_SUBSCR    
              166  LOAD_METHOD              upper
              168  CALL_METHOD_0         0  ''
              170  JUMP_FORWARD        182  'to 182'
            172_0  COME_FROM           154  '154'
              172  LOAD_GLOBAL              SYMBOLS
              174  LOAD_FAST                'name'
              176  BINARY_SUBSCR    
              178  LOAD_CONST               1
              180  BINARY_SUBSCR    
            182_0  COME_FROM           170  '170'
              182  STORE_FAST               'char'

 L. 632       184  LOAD_FAST                'char'
              186  LOAD_GLOBAL              DEAD_KEYS
              188  COMPARE_OP               in
              190  POP_JUMP_IF_FALSE   210  'to 210'

 L. 633       192  LOAD_GLOBAL              KeyCode
              194  LOAD_ATTR                from_dead
              196  LOAD_GLOBAL              DEAD_KEYS
              198  LOAD_FAST                'char'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'keysym'
              204  LOAD_CONST               ('vk',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  RETURN_VALUE     
            210_0  COME_FROM           190  '190'

 L. 635       210  LOAD_GLOBAL              KeyCode
              212  LOAD_ATTR                from_char
              214  LOAD_FAST                'char'
              216  LOAD_FAST                'keysym'
              218  LOAD_CONST               ('vk',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  RETURN_VALUE     
            224_0  COME_FROM           146  '146'
            224_1  COME_FROM           138  '138'

 L. 638       224  LOAD_GLOBAL              KeyCode
              226  LOAD_METHOD              from_vk
              228  LOAD_FAST                'keysym'
              230  CALL_METHOD_1         1  ''
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 118_0