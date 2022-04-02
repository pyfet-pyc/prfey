# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pynput\keyboard\__init__.py
"""
The module containing keyboard classes.

See the documentation for more information.
"""
import itertools
from pynput._util import backend, Events
backend = backend(__name__)
KeyCode = backend.KeyCode
Key = backend.Key
Controller = backend.Controller
Listener = backend.Listener
del backend
_MODIFIER_KEYS = (
 (
  Key.alt_gr, (Key.alt_gr.value,)),
 (
  Key.alt, (Key.alt.value, Key.alt_l.value, Key.alt_r.value)),
 (
  Key.cmd, (Key.cmd.value, Key.cmd_l.value, Key.cmd_r.value)),
 (
  Key.ctrl, (Key.ctrl.value, Key.ctrl_l.value, Key.ctrl_r.value)),
 (
  Key.shift, (Key.shift.value, Key.shift_l.value, Key.shift_r.value)))
_NORMAL_MODIFIERS = {key:value for combination in _MODIFIER_KEYS for key, value in zip(itertools.cycle((combination[0],)), combination[1])}
_CONTROL_CODES = {'\n':Key.enter, 
 '\r':Key.enter, 
 '\t':Key.tab}

class Events(Events):
    __doc__ = 'A keyboard event listener supporting synchronous iteration over the\n    events.\n\n    Possible events are:\n\n    :class:`Events.Press`\n        A key was pressed.\n\n    :class:`Events.Release`\n        A key was releesed.\n    '
    _Listener = Listener

    class Press(Events.Event):
        __doc__ = 'A key press event.\n        '

        def __init__(self, key):
            self.key = key

    class Release(Events.Event):
        __doc__ = 'A key release event.\n        '

        def __init__(self, key):
            self.key = key

    def __init__(self):
        super(Events, self).__init__(on_press=(self.Press),
          on_release=(self.Release))


class HotKey(object):
    __doc__ = 'A combination of keys acting as a hotkey.\n\n    This class acts as a container of hotkey state for a keyboard listener.\n\n    :param set keys: The collection of keys that must be pressed for this\n        hotkey to activate. Please note that a common limitation of the\n        hardware is that at most three simultaneously pressed keys are\n        supported, so using more keys may not work.\n\n    :param callable on_activate: The activation callback.\n    '

    def __init__(self, keys, on_activate):
        self._state = set()
        self._keys = set(keys)
        self._on_activate = on_activate

    @staticmethod
    def parse(keys):
        """Parses a key combination string.

        Key combination strings are sequences of key identifiers separated by
        ``'+'``. Key identifiers are either single characters representing a
        keyboard key, such as ``'a'``, or special key names identified by names
        enclosed by brackets, such as ``'<ctrl>'``.

        Keyboard keys are case-insensitive.

        :raises ValueError: if a part of the keys string is invalid, or if it
            contains multiple equal parts
        """

        def parts():
            start = 0
            for i, c in enumerate(keys):
                if c == '+':
                    if i != start:
                        yield keys[start:i]
                        start = i + 1
            else:
                if start == len(keys):
                    raise ValueError(keys)
                else:
                    yield keys[start:]

        def parse--- This code section failed: ---

 L. 142         0  LOAD_GLOBAL              len
                2  LOAD_FAST                's'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 143        12  LOAD_GLOBAL              KeyCode
               14  LOAD_METHOD              from_char
               16  LOAD_FAST                's'
               18  LOAD_METHOD              lower
               20  CALL_METHOD_0         0  ''
               22  CALL_METHOD_1         1  ''
               24  RETURN_VALUE     
             26_0  COME_FROM            10  '10'

 L. 144        26  LOAD_GLOBAL              len
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               2
               34  COMPARE_OP               >
               36  POP_JUMP_IF_FALSE   158  'to 158'
               38  LOAD_FAST                's'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  LOAD_FAST                's'
               46  LOAD_CONST               -1
               48  BINARY_SUBSCR    
               50  BUILD_TUPLE_2         2 
               52  LOAD_CONST               ('<', '>')
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE   158  'to 158'

 L. 145        58  LOAD_FAST                's'
               60  LOAD_CONST               1
               62  LOAD_CONST               -1
               64  BUILD_SLICE_2         2 
               66  BINARY_SUBSCR    
               68  STORE_FAST               'p'

 L. 146        70  SETUP_FINALLY        86  'to 86'

 L. 147        72  LOAD_GLOBAL              Key
               74  LOAD_FAST                'p'
               76  LOAD_METHOD              lower
               78  CALL_METHOD_0         0  ''
               80  BINARY_SUBSCR    
               82  POP_BLOCK        
               84  RETURN_VALUE     
             86_0  COME_FROM_FINALLY    70  '70'

 L. 148        86  DUP_TOP          
               88  LOAD_GLOBAL              KeyError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   154  'to 154'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 149       100  SETUP_FINALLY       122  'to 122'

 L. 150       102  LOAD_GLOBAL              KeyCode
              104  LOAD_METHOD              from_vk
              106  LOAD_GLOBAL              int
              108  LOAD_FAST                'p'
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''
              114  POP_BLOCK        
              116  ROT_FOUR         
              118  POP_EXCEPT       
              120  RETURN_VALUE     
            122_0  COME_FROM_FINALLY   100  '100'

 L. 151       122  DUP_TOP          
              124  LOAD_GLOBAL              ValueError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   148  'to 148'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 152       136  LOAD_GLOBAL              ValueError
              138  LOAD_FAST                's'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
              144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           128  '128'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        166  'to 166'
            154_0  COME_FROM            92  '92'
              154  END_FINALLY      
              156  JUMP_FORWARD        166  'to 166'
            158_0  COME_FROM            56  '56'
            158_1  COME_FROM            36  '36'

 L. 154       158  LOAD_GLOBAL              ValueError
              160  LOAD_FAST                's'
              162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           156  '156'
            166_1  COME_FROM           152  '152'

Parse error at or near `ROT_FOUR' instruction at offset 116

        raw_parts = list(parts())
        parsed_parts = [parse(s) for s in raw_parts]
        if len(parsed_parts) != len(set(parsed_parts)):
            raise ValueError(keys)
        else:
            return parsed_parts

    def press(self, key):
        """Updates the hotkey state for a pressed key.

        If the key is not currently pressed, but is the last key for the full
        combination, the activation callback will be invoked.

        Please note that the callback will only be invoked once.

        :param key: The key being pressed.
        :type key: Key or KeyCode
        """
        if key in self._keys:
            if key not in self._state:
                self._state.add(key)
                if self._state == self._keys:
                    self._on_activate

    def release(self, key):
        """Updates the hotkey state for a released key.

        :param key: The key being released.
        :type key: Key or KeyCode
        """
        if key in self._state:
            self._state.remove(key)


class GlobalHotKeys(Listener):
    __doc__ = 'A keyboard listener supporting a number of global hotkeys.\n\n    This is a convenience wrapper to simplify registering a number of global\n    hotkeys.\n\n    :param dict hotkeys: A mapping from hotkey description to hotkey action.\n        Keys are strings passed to :meth:`HotKey.parse`.\n\n    :raises ValueError: if any hotkey description is invalid\n    '

    def __init__(self, hotkeys, *args, **kwargs):
        self._hotkeys = [HotKey(HotKey.parse(key), value) for key, value in hotkeys.items]
        (super(GlobalHotKeys, self).__init__)(args, on_press=self._on_press, 
         on_release=self._on_release, **kwargs)

    def _on_press(self, key):
        """The press callback.

        This is automatically registered upon creation.

        :param key: The key provided by the base class.
        """
        for hotkey in self._hotkeys:
            hotkey.press(self.canonical(key))

    def _on_release(self, key):
        """The release callback.

        This is automatically registered upon creation.

        :param key: The key provided by the base class.
        """
        for hotkey in self._hotkeys:
            hotkey.release(self.canonical(key))