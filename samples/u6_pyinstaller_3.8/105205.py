# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\mouse\_base.py
"""
This module contains the base implementation.

The actual interface to mouse classes is defined here, but the implementation
is located in a platform dependent module.
"""
import enum
from pynput._util import AbstractListener
from pynput import _logger

class Button(enum.Enum):
    __doc__ = 'The various buttons.\n\n    The actual values for these items differ between platforms. Some\n    platforms may have additional buttons, but these are guaranteed to be\n    present everywhere.\n    '
    unknown = 0
    left = 1
    middle = 2
    right = 3


class Controller(object):
    __doc__ = 'A controller for sending virtual mouse events to the system.\n    '

    def __init__(self):
        self._log = _logger(self.__class__)

    @property
    def position(self):
        """The current position of the mouse pointer.

        This is the tuple ``(x, y)``, and setting it will move the pointer.
        """
        return self._position_get()

    @position.setter
    def position(self, pos):
        self._position_set(pos)

    def scroll(self, dx, dy):
        """Sends scroll events.

        :param int dx: The horizontal scroll. The units of scrolling is
            undefined.

        :param int dy: The vertical scroll. The units of scrolling is
            undefined.

        :raises ValueError: if the values are invalid, for example out of
            bounds
        """
        self._scroll(dx, dy)

    def press(self, button):
        """Emits a button press event at the current position.

        :param Button button: The button to press.
        """
        self._press(button)

    def release(self, button):
        """Emits a button release event at the current position.

        :param Button button: The button to release.
        """
        self._release(button)

    def move(self, dx, dy):
        """Moves the mouse pointer a number of pixels from its current
        position.

        :param int x: The horizontal offset.

        :param int dy: The vertical offset.

        :raises ValueError: if the values are invalid, for example out of
            bounds
        """
        self.position = tuple((sum(i) for i in zip(self.position, (dx, dy))))

    def click(self, button, count=1):
        """Emits a button click event at the current position.

        The default implementation sends a series of press and release events.

        :param Button button: The button to click.

        :param int count: The number of clicks to send.
        """
        with self as (controller):
            for _ in range(count):
                controller.press(button)
                controller.release(button)

    def __enter__(self):
        """Begins a series of clicks.

        In the default :meth:`click` implementation, the return value of this
        method is used for the calls to :meth:`press` and :meth:`release`
        instead of ``self``.

        The default implementation is a no-op.
        """
        return self

    def __exit__(self, exc_type, value, traceback):
        """Ends a series of clicks.
        """
        pass

    def _position_get(self):
        """The implementation of the getter for :attr:`position`.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _position_set(self, pos):
        """The implementation of the setter for :attr:`position`.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _scroll(self, dx, dy):
        """The implementation of the :meth:`scroll` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _press(self, button):
        """The implementation of the :meth:`press` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _release(self, button):
        """The implementation of the :meth:`release` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()


class Listener(AbstractListener):
    __doc__ = 'A listener for mouse events.\n\n    Instances of this class can be used as context managers. This is equivalent\n    to the following code::\n\n        listener.start()\n        try:\n            listener.wait()\n            with_statements()\n        finally:\n            listener.stop()\n\n    This class inherits from :class:`threading.Thread` and supports all its\n    methods. It will set :attr:`daemon` to ``True`` when created.\n\n    :param callable on_move: The callback to call when mouse move events occur.\n\n        It will be called with the arguments ``(x, y)``, which is the new\n        pointer position. If this callback raises :class:`StopException` or\n        returns ``False``, the listener is stopped.\n\n    :param callable on_click: The callback to call when a mouse button is\n        clicked.\n\n        It will be called with the arguments ``(x, y, button, pressed)``,\n        where ``(x, y)`` is the new pointer position, ``button`` is one of the\n        :class:`Button` values and ``pressed`` is whether the button was\n        pressed.\n\n        If this callback raises :class:`StopException` or returns ``False``,\n        the listener is stopped.\n\n    :param callable on_scroll: The callback to call when mouse scroll\n        events occur.\n\n        It will be called with the arguments ``(x, y, dx, dy)``, where\n        ``(x, y)`` is the new pointer position, and ``(dx, dy)`` is the scroll\n        vector.\n\n        If this callback raises :class:`StopException` or returns ``False``,\n        the listener is stopped.\n\n    :param bool suppress: Whether to suppress events. Setting this to ``True``\n        will prevent the input events from being passed to the rest of the\n        system.\n\n    :param kwargs: Any non-standard platform dependent options. These should be\n        prefixed with the platform name thus: ``darwin_``, ``xorg_`` or\n        ``win32_``.\n\n        Supported values are:\n\n        ``darwin_intercept``\n            A callable taking the arguments ``(event_type, event)``, where\n            ``event_type`` is any mouse related event type constant, and\n            ``event`` is a ``CGEventRef``.\n\n            This callable can freely modify the event using functions like\n            ``Quartz.CGEventSetIntegerValueField``. If this callable does not\n            return the event, the event is suppressed system wide.\n\n        ``win32_event_filter``\n            A callable taking the arguments ``(msg, data)``, where ``msg`` is\n            the current message, and ``data`` associated data as a\n            `MSLLHOOKSTRUCT <https://msdn.microsoft.com/en-us/library/windows/desktop/ms644970(v=vs.85).aspx>`_.\n\n            If this callback returns ``False``, the event will not\n            be propagated to the listener callback.\n\n            If ``self.suppress_event()`` is called, the event is suppressed\n            system wide.\n    '

    def __init__--- This code section failed: ---

 L. 254         0  LOAD_GLOBAL              _logger
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __class__
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _log

 L. 255        12  LOAD_FAST                'self'
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

 L. 256        44  LOAD_CLOSURE             'prefix'
               46  BUILD_TUPLE_1         1 
               48  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               50  LOAD_STR                 'Listener.__init__.<locals>.<dictcomp>'
               52  MAKE_FUNCTION_8          'closure'

 L. 258        54  LOAD_FAST                'kwargs'
               56  LOAD_METHOD              items
               58  CALL_METHOD_0         0  ''

 L. 256        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _options

 L. 260        68  LOAD_GLOBAL              super
               70  LOAD_GLOBAL              Listener
               72  LOAD_FAST                'self'
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_ATTR                __init__

 L. 261        78  LOAD_FAST                'on_move'

 L. 261        80  LOAD_FAST                'on_click'

 L. 261        82  LOAD_FAST                'on_scroll'

 L. 262        84  LOAD_FAST                'suppress'

 L. 260        86  LOAD_CONST               ('on_move', 'on_click', 'on_scroll', 'suppress')
               88  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               90  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 48