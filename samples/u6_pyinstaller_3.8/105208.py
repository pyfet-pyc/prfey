# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\mouse\_xorg.py
"""
The keyboard implementation for *Xorg*.
"""
import enum, Xlib.display, Xlib.ext, Xlib.ext.xtest, Xlib.X, Xlib.protocol
from pynput._util.xorg import display_manager, ListenerMixin
from . import _base
Button = enum.Enum('Button',
  module=__name__,
  names=([
 ('unknown', None),
 ('left', 1),
 ('middle', 2),
 ('right', 3),
 ('scroll_up', 4),
 ('scroll_down', 5),
 ('scroll_left', 6),
 ('scroll_right', 7)] + [(
 'button%d' % i, i) for i in range(8, 31)]))

class Controller(_base.Controller):

    def __init__(self, *args, **kwargs):
        (super(Controller, self).__init__)(*args, **kwargs)
        self._display = Xlib.display.Display()

    def __del__(self):
        if hasattr(self, '_display'):
            self._display.close()

    def _position_get--- This code section failed: ---

 L.  72         0  LOAD_GLOBAL              display_manager
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _display
                6  CALL_FUNCTION_1       1  ''
                8  SETUP_WITH           50  'to 50'
               10  STORE_FAST               'dm'

 L.  73        12  LOAD_FAST                'dm'
               14  LOAD_METHOD              screen
               16  CALL_METHOD_0         0  ''
               18  LOAD_ATTR                root
               20  LOAD_METHOD              query_pointer
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'qp'

 L.  74        26  LOAD_FAST                'qp'
               28  LOAD_ATTR                root_x
               30  LOAD_FAST                'qp'
               32  LOAD_ATTR                root_y
               34  BUILD_TUPLE_2         2 
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_WITH        8  '8'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

    def _position_set(self, pos):
        px, py = (self._check_bounds)(*pos)
        with display_manager(self._display) as (dm):
            Xlib.ext.xtest.fake_input(dm, (Xlib.X.MotionNotify), x=px, y=py)

    def _scroll(self, dx, dy):
        dx, dy = self._check_bounds(dx, dy)
        if dy:
            self.click(button=(Button.scroll_up if dy > 0 else Button.scroll_down),
              count=(abs(dy)))
        if dx:
            self.click(button=(Button.scroll_right if dx > 0 else Button.scroll_left),
              count=(abs(dx)))

    def _press(self, button):
        with display_manager(self._display) as (dm):
            Xlib.ext.xtest.fake_input(dm, Xlib.X.ButtonPress, button.value)

    def _release(self, button):
        with display_manager(self._display) as (dm):
            Xlib.ext.xtest.fake_input(dm, Xlib.X.ButtonRelease, button.value)

    def _check_bounds(self, *args):
        """Checks the arguments and makes sure they are within the bounds of a
        short integer.

        :param args: The values to verify.
        """
        if not all((-32768 <= number <= 32767 for number in args)):
            raise ValueError(args)
        else:
            return tuple((int(p) for p in args))


class Listener(ListenerMixin, _base.Listener):
    _SCROLL_BUTTONS = {Button.scroll_up.value: (0, 1), 
     Button.scroll_down.value: (0, -1), 
     Button.scroll_right.value: (1, 0), 
     Button.scroll_left.value: (-1, 0)}
    _EVENTS = (
     Xlib.X.ButtonPressMask,
     Xlib.X.ButtonReleaseMask)

    def __init__(self, *args, **kwargs):
        (super(Listener, self).__init__)(*args, **kwargs)

    def _handle(self, dummy_display, event):
        px = event.root_x
        py = event.root_y
        if event.type == Xlib.X.ButtonPress:
            scroll = self._SCROLL_BUTTONS.get(event.detail, None)
            if scroll:
                (self.on_scroll)(px, py, *scroll)
            else:
                self.on_click(px, py, self._button(event.detail), True)
        elif event.type == Xlib.X.ButtonRelease:
            if event.detail not in self._SCROLL_BUTTONS:
                self.on_click(px, py, self._button(event.detail), False)
        else:
            self.on_move(px, py)

    def _suppress_start(self, display):
        display.screen().root.grab_pointer(True, self._event_mask, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync, 0, 0, Xlib.X.CurrentTime)

    def _suppress_stop(self, display):
        display.ungrab_pointer(Xlib.X.CurrentTime)

    def _button--- This code section failed: ---

 L. 170         0  SETUP_FINALLY        12  'to 12'

 L. 171         2  LOAD_GLOBAL              Button
                4  LOAD_FAST                'detail'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 172        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    36  'to 36'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 173        26  LOAD_GLOBAL              Button
               28  LOAD_ATTR                unknown
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22