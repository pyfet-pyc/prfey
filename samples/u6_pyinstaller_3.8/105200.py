# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\keyboard\_base.py
"""
This module contains the base implementation.

The actual interface to keyboard classes is defined here, but the
implementation is located in a platform dependent module.
"""
import contextlib, enum, threading, unicodedata, six
from pynput._util import AbstractListener
from pynput import _logger

class KeyCode(object):
    __doc__ = '\n    A :class:`KeyCode` represents the description of a key code used by the\n    operating system.\n    '
    _PLATFORM_EXTENSIONS = []

    def __init__(self, vk=None, char=None, is_dead=False, **kwargs):
        self.vk = vk
        self.char = six.text_type(char) if char is not None else None
        self.is_dead = is_dead
        if self.is_dead:
            self.combining = unicodedata.lookup('COMBINING ' + unicodedata.name(self.char))
            assert self.combining, char
        else:
            self.combining = None
        for key in self._PLATFORM_EXTENSIONS:
            setattr(self, key, kwargs.pop(key, None))
        else:
            if kwargs:
                raise ValueError(kwargs)

    def __repr__(self):
        if self.is_dead:
            return '[%s]' % repr(self.char)
        if self.char is not None:
            return repr(self.char)
        return '<%d>' % self.vk

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.char is not None:
            if other.char is not None:
                return self.char == other.char and self.is_dead == other.is_dead
        return self.vk == other.vk

    def __hash__(self):
        return hash(repr(self))

    def join(self, key):
        """Applies this dead key to another key and returns the result.

        Joining a dead key with space (``' '``) or itself yields the non-dead
        version of this key, if one exists; for example,
        ``KeyCode.from_dead('~').join(KeyCode.from_char(' '))`` equals
        ``KeyCode.from_char('~')`` and
        ``KeyCode.from_dead('~').join(KeyCode.from_dead('~'))``.

        :param KeyCode key: The key to join with this key.

        :return: a key code

        :raises ValueError: if the keys cannot be joined
        """
        if not self.is_dead:
            raise ValueError(self)
        else:
            if key.char == ' ' or self == key:
                return self.from_char(self.char)
            if key.char is not None:
                combined = unicodedata.normalize('NFC', key.char + self.combining)
                if combined:
                    return self.from_char(combined)
        raise ValueError(key)

    @classmethod
    def from_vk(cls, vk, **kwargs):
        """Creates a key from a virtual key code.

        :param vk: The virtual key code.

        :param kwargs: Any other parameters to pass.

        :return: a key code
        """
        return cls(vk=vk, **kwargs)

    @classmethod
    def from_char(cls, char, **kwargs):
        """Creates a key from a character.

        :param str char: The character.

        :return: a key code
        """
        return cls(char=char, **kwargs)

    @classmethod
    def from_dead(cls, char, **kwargs):
        """Creates a dead key.

        :param char: The dead key. This should be the unicode character
            representing the stand alone character, such as ``'~'`` for
            *COMBINING TILDE*.

        :return: a key code
        """
        return cls(char=char, is_dead=True, **kwargs)


class Key(enum.Enum):
    __doc__ = 'A class representing various buttons that may not correspond to\n    letters. This includes modifier keys and function keys.\n\n    The actual values for these items differ between platforms. Some platforms\n    may have additional buttons, but these are guaranteed to be present\n    everywhere.\n    '
    alt = 0
    alt_l = 0
    alt_r = 0
    alt_gr = 0
    backspace = 0
    caps_lock = 0
    cmd = 0
    cmd_l = 0
    cmd_r = 0
    ctrl = 0
    ctrl_l = 0
    ctrl_r = 0
    delete = 0
    down = 0
    end = 0
    enter = 0
    esc = 0
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    f5 = 0
    f6 = 0
    f7 = 0
    f8 = 0
    f9 = 0
    f10 = 0
    f11 = 0
    f12 = 0
    f13 = 0
    f14 = 0
    f15 = 0
    f16 = 0
    f17 = 0
    f18 = 0
    f19 = 0
    f20 = 0
    home = 0
    left = 0
    page_down = 0
    page_up = 0
    right = 0
    shift = 0
    shift_l = 0
    shift_r = 0
    space = 0
    tab = 0
    up = 0
    media_play_pause = 0
    media_volume_mute = 0
    media_volume_down = 0
    media_volume_up = 0
    media_previous = 0
    media_next = 0
    insert = 0
    menu = 0
    num_lock = 0
    pause = 0
    print_screen = 0
    scroll_lock = 0


class Controller(object):
    __doc__ = 'A controller for sending virtual keyboard events to the system.\n    '
    _KeyCode = KeyCode
    _Key = Key

    class InvalidKeyException(Exception):
        __doc__ = 'The exception raised when an invalid ``key`` parameter is passed to\n        either :meth:`Controller.press` or :meth:`Controller.release`.\n\n        Its first argument is the ``key`` parameter.\n        '

    class InvalidCharacterException(Exception):
        __doc__ = 'The exception raised when an invalid character is encountered in\n        the string passed to :meth:`Controller.type`.\n\n        Its first argument is the index of the character in the string, and the\n        second the character.\n        '

    def __init__(self):
        self._log = _logger(self.__class__)
        self._modifiers_lock = threading.RLock()
        self._modifiers = set()
        self._caps_lock = False
        self._dead_key = None

    def press(self, key):
        """Presses a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to press.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """
        resolved = self._resolve(key)
        self._update_modifiers(resolved, True)
        if resolved == self._Key.caps_lock.value:
            self._caps_lock = not self._caps_lock
        original = resolved
        if self._dead_key:
            try:
                resolved = self._dead_key.join(resolved)
            except ValueError:
                self._handle(self._dead_key, True)
                self._handle(self._dead_key, False)

        if resolved.is_dead:
            self._dead_key = resolved
            return
        try:
            self._handle(resolved, True)
        except self.InvalidKeyException:
            if resolved != original:
                self._handle(self._dead_key, True)
                self._handle(self._dead_key, False)
                self._handle(original, True)
        else:
            self._dead_key = None

    def release(self, key):
        """Releases a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to release. If this is a string, it is passed to
            :meth:`touches` and the returned releases are used.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """
        resolved = self._resolve(key)
        self._update_modifiers(resolved, False)
        if resolved.is_dead:
            return
        self._handle(resolved, False)

    def touch(self, key, is_press):
        """Calls either :meth:`press` or :meth:`release` depending on the value
        of ``is_press``.

        :param key: The key to press or release.

        :param bool is_press: Whether to press the key.

        :raises InvalidKeyException: if the key is invalid
        """
        if is_press:
            self.press(key)
        else:
            self.release(key)

    @contextlib.contextmanager
    def pressed(self, *args):
        """Executes a block with some keys pressed.

        :param keys: The keys to keep pressed.
        """
        for key in args:
            self.press(key)
        else:
            try:
                (yield)
            finally:
                for key in reversed(args):
                    self.release(key)

    def type(self, string):
        """Types a string.

        This method will send all key presses and releases necessary to type
        all characters in the string.

        :param str string: The string to type.

        :raises InvalidCharacterException: if an untypable character is
            encountered
        """
        from . import _CONTROL_CODES
        for i, character in enumerate(string):
            key = _CONTROL_CODES.get(character, character)
            try:
                self.press(key)
                self.release(key)
            except (ValueError, self.InvalidKeyException):
                raise self.InvalidCharacterException(i, character)

    @property
    @contextlib.contextmanager
    def modifiers(self):
        """The currently pressed modifier keys.

        Please note that this reflects only the internal state of this
        controller, and not the state of the operating system keyboard buffer.
        This property cannot be used to determine whether a key is physically
        pressed.

        Only the generic modifiers will be set; when pressing either
        :attr:`Key.shift_l`, :attr:`Key.shift_r` or :attr:`Key.shift`, only
        :attr:`Key.shift` will be present.

        Use this property within a context block thus::

            with controller.modifiers as modifiers:
                with_block()

        This ensures that the modifiers cannot be modified by another thread.
        """
        with self._modifiers_lock:
            (yield set((self._as_modifier(modifier) for modifier in self._modifiers)))

    @property
    def alt_pressed--- This code section failed: ---

 L. 503         0  LOAD_FAST                'self'
                2  LOAD_ATTR                modifiers
                4  SETUP_WITH           32  'to 32'
                6  STORE_FAST               'modifiers'

 L. 504         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _Key
               12  LOAD_ATTR                alt
               14  LOAD_FAST                'modifiers'
               16  COMPARE_OP               in
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    @property
    def alt_gr_pressed--- This code section failed: ---

 L. 513         0  LOAD_FAST                'self'
                2  LOAD_ATTR                modifiers
                4  SETUP_WITH           32  'to 32'
                6  STORE_FAST               'modifiers'

 L. 514         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _Key
               12  LOAD_ATTR                alt_gr
               14  LOAD_FAST                'modifiers'
               16  COMPARE_OP               in
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    @property
    def ctrl_pressed--- This code section failed: ---

 L. 523         0  LOAD_FAST                'self'
                2  LOAD_ATTR                modifiers
                4  SETUP_WITH           32  'to 32'
                6  STORE_FAST               'modifiers'

 L. 524         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _Key
               12  LOAD_ATTR                ctrl
               14  LOAD_FAST                'modifiers'
               16  COMPARE_OP               in
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20

    @property
    def shift_pressed--- This code section failed: ---

 L. 533         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _caps_lock
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 534         6  LOAD_CONST               True
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 536        10  LOAD_FAST                'self'
               12  LOAD_ATTR                modifiers
               14  SETUP_WITH           42  'to 42'
               16  STORE_FAST               'modifiers'

 L. 537        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _Key
               22  LOAD_ATTR                shift
               24  LOAD_FAST                'modifiers'
               26  COMPARE_OP               in
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH       14  '14'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 30

    def _resolve(self, key):
        """Resolves a key to a :class:`KeyCode` instance.

        This method will convert any key representing a character to uppercase
        if a shift modifier is active.

        :param key: The key to resolve.

        :return: a key code, or ``None`` if it cannot be resolved
        """
        if key in (k for k in self._Key):
            return key.value
        if isinstance(key, six.string_types):
            if len(key) != 1:
                raise ValueError(key)
            return self._KeyCode.from_char(key)
        if isinstance(key, self._KeyCode):
            if key.char is not None:
                if self.shift_pressed:
                    return self._KeyCode(vk=(key.vk), char=(key.char.upper()))
            return key

    def _update_modifiers(self, key, is_press):
        """Updates the current modifier list.

        If ``key`` is not a modifier, no action is taken.

        :param key: The key being pressed or released.
        """
        if self._as_modifier(key):
            with self._modifiers_lock:
                if is_press:
                    self._modifiers.add(key)
                else:
                    try:
                        self._modifiers.remove(key)
                    except KeyError:
                        pass

    def _as_modifier(self, key):
        """Returns a key as the modifier used internally if defined.

        This method will convert values like :attr:`Key.alt_r.value` and
        :attr:`Key.shift_l.value` to :attr:`Key.alt` and :attr:`Key.shift`.

        :param key: The possible modifier key.

        :return: the base modifier key, or ``None`` if ``key`` is not a
            modifier
        """
        from . import _NORMAL_MODIFIERS
        return _NORMAL_MODIFIERS.get(key, None)

    def _handle(self, key, is_press):
        """The platform implementation of the actual emitting of keyboard
        events.

        This is a platform dependent implementation.

        :param Key key: The key to handle.

        :param bool is_press: Whether this is a key press event.
        """
        raise NotImplementedError()


class Listener(AbstractListener):
    __doc__ = 'A listener for keyboard events.\n\n    Instances of this class can be used as context managers. This is equivalent\n    to the following code::\n\n        listener.start()\n        try:\n            listener.wait()\n            with_statements()\n        finally:\n            listener.stop()\n\n    This class inherits from :class:`threading.Thread` and supports all its\n    methods. It will set :attr:`daemon` to ``True`` when created.\n\n    :param callable on_press: The callback to call when a button is pressed.\n\n        It will be called with the argument ``(key)``, where ``key`` is a\n        :class:`KeyCode`, a :class:`Key` or ``None`` if the key is unknown.\n\n    :param callable on_release: The callback to call when a button is released.\n\n        It will be called with the argument ``(key)``, where ``key`` is a\n        :class:`KeyCode`, a :class:`Key` or ``None`` if the key is unknown.\n\n    :param bool suppress: Whether to suppress events. Setting this to ``True``\n        will prevent the input events from being passed to the rest of the\n        system.\n\n    :param kwargs: Any non-standard platform dependent options. These should be\n        prefixed with the platform name thus: ``darwin_``, ``xorg_`` or\n        ``win32_``.\n\n        Supported values are:\n\n        ``darwin_intercept``\n            A callable taking the arguments ``(event_type, event)``, where\n            ``event_type`` is ``Quartz.kCGEventKeyDown`` or\n            ``Quartz.kCGEventKeyDown``, and ``event`` is a ``CGEventRef``.\n\n            This callable can freely modify the event using functions like\n            ``Quartz.CGEventSetIntegerValueField``. If this callable does not\n            return the event, the event is suppressed system wide.\n\n        ``win32_event_filter``\n            A callable taking the arguments ``(msg, data)``, where ``msg`` is\n            the current message, and ``data`` associated data as a\n            `KBLLHOOKSTRUCT <https://msdn.microsoft.com/en-us/library/windows/desktop/ms644967(v=vs.85).aspx>`_.\n\n            If this callback returns ``False``, the event will not be\n            propagated to the listener callback.\n\n            If ``self.suppress_event()`` is called, the event is suppressed\n            system wide.\n    '

    def __init__--- This code section failed: ---

 L. 670         0  LOAD_GLOBAL              _logger
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __class__
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _log

 L. 671        12  LOAD_FAST                'self'
               14  LOAD_ATTR                __class__
               16  LOAD_ATTR                __module__
               18  LOAD_METHOD              rsplit
               20  LOAD_STR                 '.'
               22  LOAD_CONST               1
               24  CALL_METHOD_2         2  ''
               26  LOAD_CONST               -1
               28  BINARY_SUBSCR    
               30  LOAD_CONST               1
               32  LOAD_CONST               None
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  LOAD_STR                 '_'
               40  BINARY_ADD       
               42  STORE_DEREF              'prefix'

 L. 672        44  LOAD_CLOSURE             'prefix'
               46  BUILD_TUPLE_1         1 
               48  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               50  LOAD_STR                 'Listener.__init__.<locals>.<dictcomp>'
               52  MAKE_FUNCTION_8          'closure'

 L. 674        54  LOAD_FAST                'kwargs'
               56  LOAD_METHOD              items
               58  CALL_METHOD_0         0  ''

 L. 672        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _options

 L. 676        68  LOAD_GLOBAL              super
               70  LOAD_GLOBAL              Listener
               72  LOAD_FAST                'self'
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_ATTR                __init__

 L. 677        78  LOAD_FAST                'on_press'

 L. 677        80  LOAD_FAST                'on_release'

 L. 677        82  LOAD_FAST                'suppress'

 L. 676        84  LOAD_CONST               ('on_press', 'on_release', 'suppress')
               86  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               88  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 48

    def canonical(self, key):
        """Performs normalisation of a key.

        This method attempts to convert key events to their canonical form, so
        that events will equal regardless of modifier state.

        This method will convert upper case keys to lower case keys, convert
        any modifiers with a right and left version to the same value, and may
        slao perform additional platform dependent normalisation.

        :param key: The key to normalise.
        :type key: Key or KeyCode

        :return: a key
        :rtype: Key or KeyCode
        """
        from pynput.keyboard import Key, KeyCode, _NORMAL_MODIFIERS
        if isinstance(key, KeyCode):
            if key.char is not None:
                return KeyCode.from_char(key.char.lower())
        if isinstance(key, Key):
            if key.value in _NORMAL_MODIFIERS:
                return _NORMAL_MODIFIERS[key.value]
        return key