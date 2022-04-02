# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\keyboard\__init__.py
"""
The module containing keyboard classes.

See the documentation for more information.
"""
import itertools, os, sys
if os.environ.get('__PYNPUT_GENERATE_DOCUMENTATION') == 'yes':
    from ._base import KeyCode, Key, Controller, Listener
else:
    KeyCode = None
    Key = None
    Controller = None
    Listener = None
from pynput._util import Events
if sys.platform == 'darwin':
    if not KeyCode:
        if not Key:
            if not Controller:
                if not Listener:
                    from ._darwin import KeyCode, Key, Controller, Listener
else:
    if sys.platform == 'win32':
        if not KeyCode:
            if not Key:
                if not Controller:
                    if not Listener:
                        from ._win32 import KeyCode, Key, Controller, Listener
    else:
        if not KeyCode:
            if not (Key or Controller):
                if not Listener:
                    try:
                        from ._xorg import KeyCode, Key, Controller, Listener
                    except ImportError:
                        raise

        if not (KeyCode and Key and Controller and Listener):
            raise ImportError('this platform is not supported')
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
            def parse--- This code section failed: ---

 L. 154         0  LOAD_CLOSURE             'keys'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object parts>
                6  LOAD_STR                 'HotKey.parse.<locals>.parts'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'parts'

 L. 165        12  LOAD_CODE                <code_object parse>
               14  LOAD_STR                 'HotKey.parse.<locals>.parse'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  STORE_DEREF              'parse'

 L. 177        20  LOAD_GLOBAL              list
               22  LOAD_FAST                'parts'
               24  CALL_FUNCTION_0       0  ''
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'raw_parts'

 L. 178        30  LOAD_CLOSURE             'parse'
               32  BUILD_TUPLE_1         1 
               34  LOAD_SETCOMP             '<code_object <setcomp>>'
               36  LOAD_STR                 'HotKey.parse.<locals>.<setcomp>'
               38  MAKE_FUNCTION_8          'closure'

 L. 180        40  LOAD_FAST                'raw_parts'

 L. 178        42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'parsed_parts'

 L. 183        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'raw_parts'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'parsed_parts'
               58  CALL_FUNCTION_1       1  ''
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 184        64  LOAD_GLOBAL              ValueError
               66  LOAD_DEREF               'keys'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
               72  JUMP_FORWARD         78  'to 78'
             74_0  COME_FROM            62  '62'

 L. 186        74  LOAD_FAST                'parsed_parts'
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

Parse error at or near `LOAD_SETCOMP' instruction at offset 34

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
                            self._on_activate()

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
                self._hotkeys = [HotKey(HotKey.parse(key), value) for key, value in hotkeys.items()]
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