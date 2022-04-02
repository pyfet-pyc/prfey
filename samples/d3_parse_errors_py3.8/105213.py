# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
            return (Xlib.XK.XK_a + ks1 - Xlib.XK.XK_A, ks1)
        if keysym_is_latin_lower(ks1):
            return (ks1, Xlib.XK.XK_A + ks1 - Xlib.XK.XK_a)
        return (
         ks1, ks1)
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
        return (
         keysym_group(stripped[0], Xlib.XK.NoSymbol),
         keysym_group(stripped[0], Xlib.XK.NoSymbol))
    if len(stripped) == 2:
        return (
         keysym_group(stripped[0], stripped[1]),
         keysym_group(stripped[0], stripped[1]))
    if len(stripped) == 3:
        return (
         keysym_group(stripped[0], stripped[1]),
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


def keyboard_mapping--- This code section failed: ---

 L. 302         0  BUILD_MAP_0           0 
                2  STORE_FAST               'mapping'

 L. 304         4  LOAD_CONST               1
                6  STORE_FAST               'shift_mask'

 L. 305         8  LOAD_GLOBAL              alt_gr_mask
               10  LOAD_FAST                'display'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'group_mask'

 L. 308        16  LOAD_FAST                'display'
               18  LOAD_ATTR                display
               20  LOAD_ATTR                info
               22  LOAD_ATTR                min_keycode
               24  STORE_FAST               'min_keycode'

 L. 309        26  LOAD_FAST                'display'
               28  LOAD_ATTR                display
               30  LOAD_ATTR                info
               32  LOAD_ATTR                max_keycode
               34  LOAD_FAST                'min_keycode'
               36  BINARY_SUBTRACT  
               38  LOAD_CONST               1
               40  BINARY_ADD       
               42  STORE_FAST               'keycode_count'

 L. 310        44  LOAD_GLOBAL              enumerate
               46  LOAD_FAST                'display'
               48  LOAD_METHOD              get_keyboard_mapping

 L. 311        50  LOAD_FAST                'min_keycode'

 L. 311        52  LOAD_FAST                'keycode_count'

 L. 310        54  CALL_METHOD_2         2  ''
               56  CALL_FUNCTION_1       1  ''
               58  GET_ITER         
             60_0  COME_FROM           202  '202'
             60_1  COME_FROM            88  '88'
               60  FOR_ITER            204  'to 204'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'index'
               66  STORE_FAST               'keysyms'

 L. 312        68  LOAD_FAST                'index'
               70  LOAD_FAST                'min_keycode'
               72  BINARY_ADD       
               74  STORE_FAST               'key_code'

 L. 315        76  LOAD_GLOBAL              keysym_normalize
               78  LOAD_FAST                'keysyms'
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'normalized'

 L. 316        84  LOAD_FAST                'normalized'
               86  POP_JUMP_IF_TRUE     90  'to 90'

 L. 317        88  JUMP_BACK            60  'to 60'
             90_0  COME_FROM            86  '86'

 L. 320        90  LOAD_GLOBAL              zip
               92  LOAD_FAST                'normalized'
               94  LOAD_CONST               (False, True)
               96  CALL_FUNCTION_2       2  ''
               98  GET_ITER         
            100_0  COME_FROM           200  '200'
              100  FOR_ITER            202  'to 202'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'groups'
              106  STORE_FAST               'group'

 L. 321       108  LOAD_GLOBAL              zip
              110  LOAD_FAST                'groups'
              112  LOAD_CONST               (False, True)
              114  CALL_FUNCTION_2       2  ''
              116  GET_ITER         
            118_0  COME_FROM           198  '198'
            118_1  COME_FROM           184  '184'
            118_2  COME_FROM           130  '130'
              118  FOR_ITER            200  'to 200'
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'keysym'
              124  STORE_FAST               'shift'

 L. 322       126  LOAD_FAST                'keysym'
              128  POP_JUMP_IF_TRUE    132  'to 132'

 L. 323       130  JUMP_BACK           118  'to 118'
            132_0  COME_FROM           128  '128'

 L. 324       132  LOAD_CONST               0

 L. 325       134  LOAD_FAST                'shift'
              136  POP_JUMP_IF_FALSE   142  'to 142'
              138  LOAD_FAST                'shift_mask'
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM           136  '136'
              142  LOAD_CONST               0
            144_0  COME_FROM           140  '140'

 L. 324       144  BINARY_OR        

 L. 326       146  LOAD_FAST                'group'
              148  POP_JUMP_IF_FALSE   154  'to 154'
              150  LOAD_FAST                'group_mask'
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           148  '148'
              154  LOAD_CONST               0
            156_0  COME_FROM           152  '152'

 L. 324       156  BINARY_OR        
              158  STORE_FAST               'shift_state'

 L. 329       160  LOAD_FAST                'keysym'
              162  LOAD_FAST                'mapping'
              164  COMPARE_OP               in
              166  POP_JUMP_IF_FALSE   186  'to 186'
              168  LOAD_FAST                'mapping'
              170  LOAD_FAST                'keysym'
              172  BINARY_SUBSCR    
              174  LOAD_CONST               1
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'shift_state'
              180  COMPARE_OP               <
              182  POP_JUMP_IF_FALSE   186  'to 186'

 L. 330       184  JUMP_BACK           118  'to 118'
            186_0  COME_FROM           182  '182'
            186_1  COME_FROM           166  '166'

 L. 331       186  LOAD_FAST                'key_code'
              188  LOAD_FAST                'shift_state'
              190  BUILD_TUPLE_2         2 
              192  LOAD_FAST                'mapping'
              194  LOAD_FAST                'keysym'
              196  STORE_SUBSCR     
              198  JUMP_BACK           118  'to 118'
            200_0  COME_FROM           118  '118'
              200  JUMP_BACK           100  'to 100'
            202_0  COME_FROM           100  '100'
              202  JUMP_BACK            60  'to 60'
            204_0  COME_FROM            60  '60'

 L. 333       204  LOAD_FAST                'mapping'
              206  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 200


def symbol_to_keysym(symbol):
    """Converts a symbol name to a *keysym*.

    :param str symbol: The name of the symbol.

    :return: the corresponding *keysym*, or ``0`` if it cannot be found
    """
    keysym = Xlib.XK.string_to_keysym(symbol)
    if keysym:
        return keysym
    if not keysym:
        try:
            return getattr(Xlib.keysymdef.xkb, 'XK_' + symbol, 0)
        except AttributeError:
            return SYMBOLS.get(symbol, (0, ))[0]


class ListenerMixin(object):
    __doc__ = 'A mixin for *X* event listeners.\n\n    Subclasses should set a value for :attr:`_EVENTS` and implement\n    :meth:`_handle`.\n    '
    _EVENTS = tuple()
    _EVENT_PARSER = Xlib.protocol.rq.EventField(None)

    def _run(self):
        self._display_stop = Xlib.display.Display()
        self._display_record = Xlib.display.Display()
        with display_manager(self._display_stop) as dm:
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
                    with display_manager(self._display_record) as dm:
                        self._suppress_start(dm)
                self._display_record.record_enable_context(self._context, self._handler)
            except:
                pass

        finally:
            if self.suppress:
                with display_manager(self._display_stop) as dm:
                    self._suppress_stop(dm)
            self._display_record.record_free_context(self._context)
            self._display_stop.close()
            self._display_record.close()

    def _stop_platform(self):
        if not hasattr(self, '_context'):
            self.wait()
        try:
            with display_manager(self._display_stop) as dm:
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