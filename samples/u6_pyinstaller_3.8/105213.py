# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\_util\xorg.py
"""
Utility functions and classes for the *Xorg* backend.
"""
import contextlib, functools, itertools, operator, Xlib.display, Xlib.threaded, Xlib.XK
from . import AbstractListener
from .xorg_keysyms import SYMBOLS

def _check():
    display = Xlib.display.Display()
    display.close()


_check()
del _check

class X11Error(Exception):
    __doc__ = 'An error that is thrown at the end of a code block managed by a\n    :func:`display_manager` if an *X11* error occurred.\n    '


@contextlib.contextmanager
def display_manager(display):
    """Traps *X* errors and raises an :class:``X11Error`` at the end if any
    error occurred.

    This handler also ensures that the :class:`Xlib.display.Display` being
    managed is sync'd.

    :param Xlib.display.Display display: The *X* display.

    :return: the display
    :rtype: Xlib.display.Display
    """
    errors = []

    def handler(*args):
        errors.append(args)

    old_handler = display.set_error_handler(handler)
    try:
        yield display
        display.sync()
    finally:
        display.set_error_handler(old_handler)

    if errors:
        raise X11Error(errors)


def _find_mask(display, symbol):
    """Returns the mode flags to use for a modifier symbol.

    :param Xlib.display.Display display: The *X* display.

    :param str symbol: The name of the symbol.

    :return: the modifier mask
    """
    modifier_keycode = display.keysym_to_keycode(Xlib.XK.string_to_keysym(symbol))
    for index, keycodes in enumerate(display.get_modifier_mapping()):
        for keycode in keycodes:
            if keycode == modifier_keycode:
                return 1 << index
        else:
            return 0


def alt_mask(display):
    """Returns the *alt* mask flags.

    The first time this function is called for a display, the value is cached.
    Subsequent calls will return the cached value.

    :param Xlib.display.Display display: The *X* display.

    :return: the modifier mask
    """
    if not hasattr(display, '__alt_mask'):
        display.__alt_mask = _find_mask(display, 'Alt_L')
    return display.__alt_mask


def alt_gr_mask(display):
    """Returns the *alt* mask flags.

    The first time this function is called for a display, the value is cached.
    Subsequent calls will return the cached value.

    :param Xlib.display.Display display: The *X* display.

    :return: the modifier mask
    """
    if not hasattr(display, '__altgr_mask'):
        display.__altgr_mask = _find_mask(display, 'Mode_switch')
    return display.__altgr_mask


def numlock_mask(display):
    """Returns the *numlock* mask flags.

    The first time this function is called for a display, the value is cached.
    Subsequent calls will return the cached value.

    :param Xlib.display.Display display: The *X* display.

    :return: the modifier mask
    """
    if not hasattr(display, '__numlock_mask'):
        display.__numlock_mask = _find_mask(display, 'Num_Lock')
    return display.__numlock_mask


def keysym_is_latin_upper(keysym):
    """Determines whether a *keysym* is an upper case *latin* character.

    This is true only if ``XK_A`` <= ``keysym`` <= ` XK_Z``.

    :param in keysym: The *keysym* to check.
    """
    return Xlib.XK.XK_A <= keysym <= Xlib.XK.XK_Z


def keysym_is_latin_lower(keysym):
    """Determines whether a *keysym* is a lower case *latin* character.

    This is true only if ``XK_a`` <= ``keysym`` <= ` XK_z``.

    :param in keysym: The *keysym* to check.
    """
    return Xlib.XK.XK_a <= keysym <= Xlib.XK.XK_z


def keysym_group(ks1, ks2):
    """Generates a group from two *keysyms*.

    The implementation of this function comes from:

        Within each group, if the second element of the group is ``NoSymbol``,
        then the group should be treated as if the second element were the same
        as the first element, except when the first element is an alphabetic
        *KeySym* ``K`` for which both lowercase and uppercase forms are
        defined.

        In that case, the group should be treated as if the first element were
        the lowercase form of ``K`` and the second element were the uppercase
        form of ``K``.

    This function assumes that *alphabetic* means *latin*; this assumption
    appears to be consistent with observations of the return values from
    ``XGetKeyboardMapping``.

    :param ks1: The first *keysym*.

    :param ks2: The second *keysym*.

    :return: a tuple conforming to the description above
    """
    if ks2 == Xlib.XK.NoSymbol:
        if keysym_is_latin_upper(ks1):
            return (
             Xlib.XK.XK_a + ks1 - Xlib.XK.XK_A, ks1)
        if keysym_is_latin_lower(ks1):
            return (
             ks1, Xlib.XK.XK_A + ks1 - Xlib.XK.XK_a)
        return (ks1, ks1)
    else:
        return (
         ks1, ks2)


def keysym_normalize(keysym):
    """Normalises a list of *keysyms*.

    The implementation of this function comes from:

        If the list (ignoring trailing ``NoSymbol`` entries) is a single
        *KeySym* ``K``, then the list is treated as if it were the list
        ``K NoSymbol K NoSymbol``.

        If the list (ignoring trailing ``NoSymbol`` entries) is a pair of
        *KeySyms* ``K1 K2``, then the list is treated as if it were the list
        ``K1 K2 K1 K2``.

        If the list (ignoring trailing ``NoSymbol`` entries) is a triple of
        *KeySyms* ``K1 K2 K3``, then the list is treated as if it were the list
        ``K1 K2 K3 NoSymbol``.

    This function will also group the *keysyms* using :func:`keysym_group`.

    :param keysyms: A list of keysyms.

    :return: the tuple ``(group_1, group_2)`` or ``None``
    """
    stripped = list(reversed(list(itertools.dropwhile(lambda n: n == Xlib.XK.NoSymbol, reversed(keysym)))))
    if not stripped:
        return
    if len(stripped) == 1:
        return (keysym_group(stripped[0], Xlib.XK.NoSymbol),
         keysym_group(stripped[0], Xlib.XK.NoSymbol))
    if len(stripped) == 2:
        return (keysym_group(stripped[0], stripped[1]),
         keysym_group(stripped[0], stripped[1]))
    if len(stripped) == 3:
        return (keysym_group(stripped[0], stripped[1]),
         keysym_group(stripped[2], Xlib.XK.NoSymbol))
    if len(stripped) >= 6:
        return (
         keysym_group(stripped[0], stripped[1]),
         keysym_group(stripped[4], stripped[5]))
    return (
     keysym_group(stripped[0], stripped[1]),
     keysym_group(stripped[2], stripped[3]))


def index_to_shift(display, index):
    """Converts an index in a *key code* list to the corresponding shift state.

    :param Xlib.display.Display display: The display for which to retrieve the
        shift mask.

    :param int index: The keyboard mapping *key code* index.

    :return: a shift mask
    """
    return (1 if index & 1 else 0) | (alt_gr_mask(display) if index & 2 else 0)


def shift_to_index(display, shift):
    """Converts an index in a *key code* list to the corresponding shift state.

    :param Xlib.display.Display display: The display for which to retrieve the
        shift mask.

    :param int index: The keyboard mapping *key code* index.

    :retur: a shift mask
    """
    return (1 if shift & 1 else 0) + (2 if shift & alt_gr_mask(display) else 0)


def keyboard_mapping(display):
    """Generates a mapping from *keysyms* to *key codes* and required
    modifier shift states.

    :param Xlib.display.Display display: The display for which to retrieve the
        keyboard mapping.

    :return: the keyboard mapping
    """
    mapping = {}
    shift_mask = 1
    group_mask = alt_gr_mask(display)
    min_keycode = display.display.info.min_keycode
    keycode_count = display.display.info.max_keycode - min_keycode + 1
    for index, keysyms in enumerate(display.get_keyboard_mapping(min_keycode, keycode_count)):
        key_code = index + min_keycode
        normalized = keysym_normalize(keysyms)
        if not normalized:
            pass
        else:
            for groups, group in zip(normalized, (False, True)):
                for keysym, shift in zip(groups, (False, True)):
                    if not keysym:
                        pass
                    else:
                        shift_state = 0 | (shift_mask if shift else 0) | (group_mask if group else 0)
                        if keysym in mapping and mapping[keysym][1] < shift_state:
                            pass
                        else:
                            mapping[keysym] = (
                             key_code, shift_state)

            else:
                return mapping


def symbol_to_keysym--- This code section failed: ---

 L. 344         0  LOAD_GLOBAL              Xlib
                2  LOAD_ATTR                XK
                4  LOAD_METHOD              string_to_keysym
                6  LOAD_FAST                'symbol'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'keysym'

 L. 345        12  LOAD_FAST                'keysym'
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 346        16  LOAD_FAST                'keysym'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 349        20  LOAD_FAST                'keysym'
               22  POP_JUMP_IF_TRUE     84  'to 84'

 L. 350        24  SETUP_FINALLY        48  'to 48'

 L. 351        26  LOAD_GLOBAL              getattr
               28  LOAD_GLOBAL              Xlib
               30  LOAD_ATTR                keysymdef
               32  LOAD_ATTR                xkb
               34  LOAD_STR                 'XK_'
               36  LOAD_FAST                'symbol'
               38  BINARY_ADD       
               40  LOAD_CONST               0
               42  CALL_FUNCTION_3       3  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    24  '24'

 L. 352        48  DUP_TOP          
               50  LOAD_GLOBAL              AttributeError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    82  'to 82'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 353        62  LOAD_GLOBAL              SYMBOLS
               64  LOAD_METHOD              get
               66  LOAD_FAST                'symbol'
               68  LOAD_CONST               (0,)
               70  CALL_METHOD_2         2  ''
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  RETURN_VALUE     
             82_0  COME_FROM            54  '54'
               82  END_FINALLY      
             84_0  COME_FROM            22  '22'

Parse error at or near `POP_TOP' instruction at offset 58


class ListenerMixin(object):
    __doc__ = 'A mixin for *X* event listeners.\n\n    Subclasses should set a value for :attr:`_EVENTS` and implement\n    :meth:`_handle`.\n    '
    _EVENTS = tuple()
    _EVENT_PARSER = Xlib.protocol.rq.EventField(None)

    def _run(self):
        self._display_stop = Xlib.display.Display()
        self._display_record = Xlib.display.Display()
        with display_manager(self._display_stop) as (dm):
            self._context = dm.record_create_context(0, [
             Xlib.ext.record.AllClients], [
             {'core_requests':(0, 0), 
              'core_replies':(0, 0), 
              'ext_requests':(0, 0, 0, 0), 
              'ext_replies':(0, 0, 0, 0), 
              'delivered_events':(0, 0), 
              'device_events':self._EVENTS, 
              'errors':(0, 0), 
              'client_started':False, 
              'client_died':False}])
        try:
            try:
                self._initialize(self._display_stop)
                self._mark_ready()
                if self.suppress:
                    with display_manager(self._display_record) as (dm):
                        self._suppress_start(dm)
                self._display_record.record_enable_context(self._context, self._handler)
            except:
                pass

        finally:
            if self.suppress:
                with display_manager(self._display_stop) as (dm):
                    self._suppress_stop(dm)
            self._display_record.record_free_context(self._context)
            self._display_stop.close()
            self._display_record.close()

    def _stop_platform(self):
        if not hasattr(self, '_context'):
            self.wait()
        try:
            with display_manager(self._display_stop) as (dm):
                dm.record_disable_context(self._context)
        except:
            pass

    def _suppress_start(self, display):
        """Starts suppressing events.

        :param Xlib.display.Display display: The display for which to suppress
            events.
        """
        raise NotImplementedError()

    def _suppress_stop(self, display):
        """Starts suppressing events.

        :param Xlib.display.Display display: The display for which to suppress
            events.
        """
        raise NotImplementedError()

    @property
    def _event_mask(self):
        """The event mask.
        """
        return functools.reduce(operator.__or__, self._EVENTS, 0)

    @AbstractListener._emitter
    def _handler(self, events):
        """The callback registered with *X* for mouse events.

        This method will parse the response and call the callbacks registered
        on initialisation.

        :param events: The events passed by *X*. This is a binary block
            parsable by :attr:`_EVENT_PARSER`.
        """
        if not self.running:
            raise self.StopException()
        else:
            data = events.data
            while data:
                if len(data):
                    event, data = self._EVENT_PARSER.parse_binary_value(data, self._display_record.display, None, None)
                    self._handle(self._display_stop, event)

    def _initialize(self, display):
        """Initialises this listener.

        This method is called immediately before the event loop, from the
        handler thread.

        :param display: The display being used.
        """
        pass

    def _handle(self, display, event):
        """The device specific callback handler.

        This method calls the appropriate callback registered when this
        listener was created based on the event.

        :param display: The display being used.

        :param event: The event.
        """
        pass