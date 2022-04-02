# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\mouse\_darwin.py
"""
The mouse implementation for *OSX*.
"""
import enum, Quartz
from AppKit import NSEvent
from pynput._util.darwin import ListenerMixin
from . import _base

def _button_value(base_name, mouse_button):
    """Generates the value tuple for a :class:`Button` value.

    :param str base_name: The base name for the button. This shuld be a string
        like ``'kCGEventLeftMouse'``.

    :param int mouse_button: The mouse button ID.

    :return: a value tuple
    """
    return (
     tuple((getattr(Quartz, '%sMouse%s' % (base_name, name)) for name in ('Down', 'Up',
                                                                     'Dragged'))),
     mouse_button)


class Button(enum.Enum):
    __doc__ = 'The various buttons.\n    '
    unknown = None
    left = _button_value('kCGEventLeft', 0)
    middle = _button_value('kCGEventOther', 2)
    right = _button_value('kCGEventRight', 1)


class Controller(_base.Controller):
    _SCROLL_SPEED = 5

    def __init__(self, *args, **kwargs):
        (super(Controller, self).__init__)(*args, **kwargs)
        self._click = None
        self._drag_button = None

    def _position_get(self):
        pos = NSEvent.mouseLocation()
        return (
         pos.x, Quartz.CGDisplayPixelsHigh(0) - pos.y)

    def _position_set(self, pos):
        try:
            (_, _, mouse_type), mouse_button = self._drag_button.value
        except AttributeError:
            mouse_type = Quartz.kCGEventMouseMoved
            mouse_button = 0
        else:
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateMouseEvent(None, mouse_type, pos, mouse_button))

    def _scroll(self, dx, dy):
        dx = int(dx)
        dy = int(dy)
        while True:
            xval = 1 if (dx != 0) or (dy != 0) and (dx > 0) else (-1 if dx < 0 else 0)
            dx -= xval
            yval = 1 if dy > 0 else -1 if dy < 0 else 0
            dy -= yval
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, Quartz.CGEventCreateScrollWheelEvent(None, Quartz.kCGScrollEventUnitPixel, 2, yval * self._SCROLL_SPEED, xval * self._SCROLL_SPEED))

    def _press(self, button):
        (press, _, _), mouse_button = button.value
        event = Quartz.CGEventCreateMouseEvent(None, press, self.position, mouse_button)
        if self._click is not None:
            self._click += 1
            Quartz.CGEventSetIntegerValueField(event, Quartz.kCGMouseEventClickState, self._click)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        self._drag_button = button

    def _release(self, button):
        (_, release, _), mouse_button = button.value
        event = Quartz.CGEventCreateMouseEvent(None, release, self.position, mouse_button)
        if self._click is not None:
            Quartz.CGEventSetIntegerValueField(event, Quartz.kCGMouseEventClickState, self._click)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        if button == self._drag_button:
            self._drag_button = None

    def __enter__(self):
        self._click = 0
        return self

    def __exit__(self, exc_type, value, traceback):
        self._click = None


class Listener(ListenerMixin, _base.Listener):
    _EVENTS = Quartz.CGEventMaskBit(Quartz.kCGEventMouseMoved) | Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseDown) | Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseUp) | Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseDragged) | Quartz.CGEventMaskBit(Quartz.kCGEventRightMouseDown) | Quartz.CGEventMaskBit(Quartz.kCGEventRightMouseUp) | Quartz.CGEventMaskBit(Quartz.kCGEventRightMouseDragged) | Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseDown) | Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseUp) | Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseDragged) | Quartz.CGEventMaskBit(Quartz.kCGEventScrollWheel)

    def __init__(self, *args, **kwargs):
        (super(Listener, self).__init__)(*args, **kwargs)
        self._intercept = self._options.get('intercept', None)

    def _handle--- This code section failed: ---

 L. 185         0  SETUP_FINALLY        20  'to 20'

 L. 186         2  LOAD_GLOBAL              Quartz
                4  LOAD_METHOD              CGEventGetLocation
                6  LOAD_FAST                'event'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'px'
               14  STORE_FAST               'py'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 187        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 189        34  POP_EXCEPT       
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      
             42_0  COME_FROM            18  '18'

 L. 192        42  LOAD_FAST                'event_type'
               44  LOAD_GLOBAL              Quartz
               46  LOAD_ATTR                kCGEventMouseMoved
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L. 193        52  LOAD_FAST                'self'
               54  LOAD_METHOD              on_move
               56  LOAD_FAST                'px'
               58  LOAD_FAST                'py'
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          
               64  JUMP_FORWARD        232  'to 232'
             66_0  COME_FROM            50  '50'

 L. 195        66  LOAD_FAST                'event_type'
               68  LOAD_GLOBAL              Quartz
               70  LOAD_ATTR                kCGEventScrollWheel
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   122  'to 122'

 L. 196        76  LOAD_GLOBAL              Quartz
               78  LOAD_METHOD              CGEventGetIntegerValueField

 L. 197        80  LOAD_FAST                'event'

 L. 198        82  LOAD_GLOBAL              Quartz
               84  LOAD_ATTR                kCGScrollWheelEventDeltaAxis2

 L. 196        86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'dx'

 L. 199        90  LOAD_GLOBAL              Quartz
               92  LOAD_METHOD              CGEventGetIntegerValueField

 L. 200        94  LOAD_FAST                'event'

 L. 201        96  LOAD_GLOBAL              Quartz
               98  LOAD_ATTR                kCGScrollWheelEventDeltaAxis1

 L. 199       100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'dy'

 L. 202       104  LOAD_FAST                'self'
              106  LOAD_METHOD              on_scroll
              108  LOAD_FAST                'px'
              110  LOAD_FAST                'py'
              112  LOAD_FAST                'dx'
              114  LOAD_FAST                'dy'
              116  CALL_METHOD_4         4  ''
              118  POP_TOP          
              120  JUMP_FORWARD        232  'to 232'
            122_0  COME_FROM            74  '74'

 L. 205       122  LOAD_GLOBAL              Button
              124  GET_ITER         
            126_0  COME_FROM           230  '230'
            126_1  COME_FROM           216  '216'
            126_2  COME_FROM           208  '208'
            126_3  COME_FROM           168  '168'
              126  FOR_ITER            232  'to 232'
              128  STORE_FAST               'button'

 L. 206       130  SETUP_FINALLY       152  'to 152'

 L. 207       132  LOAD_FAST                'button'
              134  LOAD_ATTR                value
              136  UNPACK_SEQUENCE_2     2 
              138  UNPACK_SEQUENCE_3     3 
              140  STORE_FAST               'press'
              142  STORE_FAST               'release'
              144  STORE_FAST               'drag'
              146  STORE_FAST               '_'
              148  POP_BLOCK        
              150  JUMP_FORWARD        176  'to 176'
            152_0  COME_FROM_FINALLY   130  '130'

 L. 208       152  DUP_TOP          
              154  LOAD_GLOBAL              TypeError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   174  'to 174'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 210       166  POP_EXCEPT       
              168  JUMP_BACK           126  'to 126'
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           158  '158'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           150  '150'

 L. 214       176  LOAD_FAST                'event_type'
              178  LOAD_FAST                'press'
              180  LOAD_FAST                'release'
              182  BUILD_TUPLE_2         2 
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   210  'to 210'

 L. 215       188  LOAD_FAST                'self'
              190  LOAD_METHOD              on_click
              192  LOAD_FAST                'px'
              194  LOAD_FAST                'py'
              196  LOAD_FAST                'button'
              198  LOAD_FAST                'event_type'
              200  LOAD_FAST                'press'
              202  COMPARE_OP               ==
              204  CALL_METHOD_4         4  ''
              206  POP_TOP          
              208  JUMP_BACK           126  'to 126'
            210_0  COME_FROM           186  '186'

 L. 216       210  LOAD_FAST                'event_type'
              212  LOAD_FAST                'drag'
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE_BACK   126  'to 126'

 L. 217       218  LOAD_FAST                'self'
              220  LOAD_METHOD              on_move
              222  LOAD_FAST                'px'
              224  LOAD_FAST                'py'
              226  CALL_METHOD_2         2  ''
              228  POP_TOP          
              230  JUMP_BACK           126  'to 126'
            232_0  COME_FROM           126  '126'
            232_1  COME_FROM           120  '120'
            232_2  COME_FROM            64  '64'

Parse error at or near `COME_FROM' instruction at offset 174_0