# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: mss\linux.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import ctypes, ctypes.util, os, threading
from types import SimpleNamespace
from typing import TYPE_CHECKING
from .base import MSSBase, lock
from .exception import ScreenShotError
if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Union
    from .models import Monitor, Monitors
    from .screenshot import ScreenShot
__all__ = ('MSS', )
ERROR = SimpleNamespace(details=None)
PLAINMASK = 16777215
ZPIXMAP = 2

class Display(ctypes.Structure):
    __doc__ = '\n    Structure that serves as the connection to the X server\n    and that contains all the information about that X server.\n    '


class Event(ctypes.Structure):
    __doc__ = '\n    XErrorEvent to debug eventual errors.\n    https://tronche.com/gui/x/xlib/event-handling/protocol-errors/default-handlers.html\n    '
    _fields_ = [
     (
      'type', ctypes.c_int),
     (
      'display', ctypes.POINTER(Display)),
     (
      'serial', ctypes.c_ulong),
     (
      'error_code', ctypes.c_ubyte),
     (
      'request_code', ctypes.c_ubyte),
     (
      'minor_code', ctypes.c_ubyte),
     (
      'resourceid', ctypes.c_void_p)]


class XWindowAttributes(ctypes.Structure):
    __doc__ = ' Attributes for the specified window. '
    _fields_ = [
     (
      'x', ctypes.c_int32),
     (
      'y', ctypes.c_int32),
     (
      'width', ctypes.c_int32),
     (
      'height', ctypes.c_int32),
     (
      'border_width', ctypes.c_int32),
     (
      'depth', ctypes.c_int32),
     (
      'visual', ctypes.c_ulong),
     (
      'root', ctypes.c_ulong),
     (
      'class', ctypes.c_int32),
     (
      'bit_gravity', ctypes.c_int32),
     (
      'win_gravity', ctypes.c_int32),
     (
      'backing_store', ctypes.c_int32),
     (
      'backing_planes', ctypes.c_ulong),
     (
      'backing_pixel', ctypes.c_ulong),
     (
      'save_under', ctypes.c_int32),
     (
      'colourmap', ctypes.c_ulong),
     (
      'mapinstalled', ctypes.c_uint32),
     (
      'map_state', ctypes.c_uint32),
     (
      'all_event_masks', ctypes.c_ulong),
     (
      'your_event_mask', ctypes.c_ulong),
     (
      'do_not_propagate_mask', ctypes.c_ulong),
     (
      'override_redirect', ctypes.c_int32),
     (
      'screen', ctypes.c_ulong)]


class XImage(ctypes.Structure):
    __doc__ = "\n    Description of an image as it exists in the client's memory.\n    https://tronche.com/gui/x/xlib/graphics/images.html\n    "
    _fields_ = [
     (
      'width', ctypes.c_int),
     (
      'height', ctypes.c_int),
     (
      'xoffset', ctypes.c_int),
     (
      'format', ctypes.c_int),
     (
      'data', ctypes.c_void_p),
     (
      'byte_order', ctypes.c_int),
     (
      'bitmap_unit', ctypes.c_int),
     (
      'bitmap_bit_order', ctypes.c_int),
     (
      'bitmap_pad', ctypes.c_int),
     (
      'depth', ctypes.c_int),
     (
      'bytes_per_line', ctypes.c_int),
     (
      'bits_per_pixel', ctypes.c_int),
     (
      'red_mask', ctypes.c_ulong),
     (
      'green_mask', ctypes.c_ulong),
     (
      'blue_mask', ctypes.c_ulong)]


class XRRModeInfo(ctypes.Structure):
    __doc__ = ' Voilà, voilà. '


class XRRScreenResources(ctypes.Structure):
    __doc__ = '\n    Structure that contains arrays of XIDs that point to the\n    available outputs and associated CRTCs.\n    '
    _fields_ = [
     (
      'timestamp', ctypes.c_ulong),
     (
      'configTimestamp', ctypes.c_ulong),
     (
      'ncrtc', ctypes.c_int),
     (
      'crtcs', ctypes.POINTER(ctypes.c_long)),
     (
      'noutput', ctypes.c_int),
     (
      'outputs', ctypes.POINTER(ctypes.c_long)),
     (
      'nmode', ctypes.c_int),
     (
      'modes', ctypes.POINTER(XRRModeInfo))]


class XRRCrtcInfo(ctypes.Structure):
    __doc__ = ' Structure that contains CRTC information. '
    _fields_ = [
     (
      'timestamp', ctypes.c_ulong),
     (
      'x', ctypes.c_int),
     (
      'y', ctypes.c_int),
     (
      'width', ctypes.c_int),
     (
      'height', ctypes.c_int),
     (
      'mode', ctypes.c_long),
     (
      'rotation', ctypes.c_int),
     (
      'noutput', ctypes.c_int),
     (
      'outputs', ctypes.POINTER(ctypes.c_long)),
     (
      'rotations', ctypes.c_ushort),
     (
      'npossible', ctypes.c_int),
     (
      'possible', ctypes.POINTER(ctypes.c_long))]


@ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(Display), ctypes.POINTER(Event))
def error_handler(_, event):
    """ Specifies the program's supplied error handler. """
    evt = event.contents
    ERROR.details = {'type':evt.type, 
     'serial':evt.serial, 
     'error_code':evt.error_code, 
     'request_code':evt.request_code, 
     'minor_code':evt.minor_code}
    return 0


def validate(retval, func, args):
    """ Validate the returned value of a Xlib or XRANDR function. """
    if retval != 0:
        if not ERROR.details:
            return args
    err = '{}() failed'.format(func.__name__)
    details = {'retval':retval,  'args':args}
    raise ScreenShotError(err, details=details)


class MSS(MSSBase):
    __doc__ = '\n    Multiple ScreenShots implementation for GNU/Linux.\n    It uses intensively the Xlib and its Xrandr extension.\n    '
    __slots__ = {
     'drawable', 'root', 'xlib', 'xrandr'}
    _display_dict = {}

    def __init__(self, display=None):
        """ GNU/Linux initialisations. """
        super().__init__()
        if not display:
            try:
                display = os.environ['DISPLAY'].encode('utf-8')
            except KeyError:
                raise ScreenShotError('$DISPLAY not set.')

        if not isinstance(display, bytes):
            display = display.encode('utf-8')
        if b':' not in display:
            raise ScreenShotError('Bad display value: {!r}.'.format(display))
        x11 = ctypes.util.find_library('X11')
        if not x11:
            raise ScreenShotError('No X11 library found.')
        self.xlib = ctypes.cdll.LoadLibrary(x11)
        self.xlib.XSetErrorHandler(error_handler)
        xrandr = ctypes.util.find_library('Xrandr')
        if not xrandr:
            raise ScreenShotError('No Xrandr extension found.')
        self.xrandr = ctypes.cdll.LoadLibrary(xrandr)
        self._set_cfunctions()
        self.root = self.xlib.XDefaultRootWindow(self._get_display(display))
        if not self.has_extension('RANDR'):
            raise ScreenShotError('No Xrandr extension found.')
        self.drawable = ctypes.cast(self.root, ctypes.POINTER(Display))

    def has_extension--- This code section failed: ---

 L. 236         0  LOAD_GLOBAL              lock
                2  SETUP_WITH          134  'to 134'
                4  POP_TOP          

 L. 237         6  LOAD_GLOBAL              ctypes
                8  LOAD_ATTR                byref
               10  STORE_FAST               'byref'

 L. 238        12  LOAD_GLOBAL              ctypes
               14  LOAD_ATTR                c_int
               16  STORE_FAST               'c_int'

 L. 239        18  LOAD_FAST                'c_int'
               20  CALL_FUNCTION_0       0  ''
               22  STORE_FAST               'major_opcode_return'

 L. 240        24  LOAD_FAST                'c_int'
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'first_event_return'

 L. 241        30  LOAD_FAST                'c_int'
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'first_error_return'

 L. 243        36  SETUP_FINALLY        84  'to 84'

 L. 244        38  LOAD_FAST                'self'
               40  LOAD_ATTR                xlib
               42  LOAD_METHOD              XQueryExtension

 L. 245        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _get_display
               48  CALL_METHOD_0         0  ''

 L. 246        50  LOAD_FAST                'extension'
               52  LOAD_METHOD              encode
               54  LOAD_STR                 'latin1'
               56  CALL_METHOD_1         1  ''

 L. 247        58  LOAD_FAST                'byref'
               60  LOAD_FAST                'major_opcode_return'
               62  CALL_FUNCTION_1       1  ''

 L. 248        64  LOAD_FAST                'byref'
               66  LOAD_FAST                'first_event_return'
               68  CALL_FUNCTION_1       1  ''

 L. 249        70  LOAD_FAST                'byref'
               72  LOAD_FAST                'first_error_return'
               74  CALL_FUNCTION_1       1  ''

 L. 244        76  CALL_METHOD_5         5  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  JUMP_FORWARD        116  'to 116'
             84_0  COME_FROM_FINALLY    36  '36'

 L. 251        84  DUP_TOP          
               86  LOAD_GLOBAL              ScreenShotError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   114  'to 114'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 252        98  POP_EXCEPT       
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
              104  WITH_CLEANUP_START
              106  WITH_CLEANUP_FINISH
              108  POP_FINALLY           0  ''
              110  LOAD_CONST               False
              112  RETURN_VALUE     
            114_0  COME_FROM            90  '90'
              114  END_FINALLY      
            116_0  COME_FROM            82  '82'

 L. 254       116  POP_BLOCK        
              118  BEGIN_FINALLY    
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  POP_FINALLY           0  ''
              126  LOAD_CONST               True
              128  RETURN_VALUE     
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_WITH        2  '2'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 102

    def _get_display(self, disp=None):
        """
        Retrieve a thread-safe display from XOpenDisplay().
        In multithreading, if the thread who creates *display* is dead, *display* will
        no longer be valid to grab the screen. The *display* attribute is replaced
        with *_display_dict* to maintain the *display* values in multithreading.
        Since the current thread and main thread are always alive, reuse their
        *display* value first.
        """
        cur_thread, main_thread = threading.current_thread(), threading.main_thread()
        display = MSS._display_dict.get(cur_thread) or MSS._display_dict.get(main_thread)
        if not display:
            display = MSS._display_dict[cur_thread] = self.xlib.XOpenDisplay(disp)
        return display

    def _set_cfunctions(self):
        """
        Set all ctypes functions and attach them to attributes.
        See https://tronche.com/gui/x/xlib/function-index.html for details.
        """

        def cfactory(func, argtypes, restype, attr=self.xlib):
            """ Factorize ctypes creations. """
            self._cfactory(attr=attr,
              errcheck=validate,
              func=func,
              argtypes=argtypes,
              restype=restype)

        void = ctypes.c_void_p
        c_int = ctypes.c_int
        uint = ctypes.c_uint
        ulong = ctypes.c_ulong
        c_long = ctypes.c_long
        char_p = ctypes.c_char_p
        pointer = ctypes.POINTER
        cfactory('XSetErrorHandler', [void], c_int)
        cfactory('XGetErrorText', [pointer(Display), c_int, char_p, c_int], void)
        cfactory('XOpenDisplay', [char_p], pointer(Display))
        cfactory('XDefaultRootWindow', [pointer(Display)], pointer(XWindowAttributes))
        cfactory('XGetWindowAttributes', [
         pointer(Display), pointer(XWindowAttributes), pointer(XWindowAttributes)], c_int)
        cfactory('XGetImage', [
         pointer(Display),
         pointer(Display),
         c_int,
         c_int,
         uint,
         uint,
         ulong,
         c_int], pointer(XImage))
        cfactory('XDestroyImage', [pointer(XImage)], void)
        cfactory('XQueryExtension', [
         pointer(Display), char_p, pointer(c_int), pointer(c_int), pointer(c_int)], uint)
        try:
            cfactory('XRRGetScreenResourcesCurrent',
              [
             pointer(Display), pointer(Display)],
              (pointer(XRRScreenResources)),
              attr=(self.xrandr))
        except AttributeError:
            cfactory('XRRGetScreenResources',
              [
             pointer(Display), pointer(Display)],
              (pointer(XRRScreenResources)),
              attr=(self.xrandr))
            self.xrandr.XRRGetScreenResourcesCurrent = self.xrandr.XRRGetScreenResources
        else:
            cfactory('XRRGetCrtcInfo',
              [
             pointer(Display), pointer(XRRScreenResources), c_long],
              (pointer(XRRCrtcInfo)),
              attr=(self.xrandr))
            cfactory('XRRFreeScreenResources',
              [
             pointer(XRRScreenResources)],
              void,
              attr=(self.xrandr))
            cfactory('XRRFreeCrtcInfo', [pointer(XRRCrtcInfo)], void, attr=(self.xrandr))

    def get_error_details(self):
        """ Get more information about the latest X server error. """
        details = {}
        if ERROR.details:
            details = {'xerror_details': ERROR.details}
            ERROR.details = None
            xserver_error = ctypes.create_string_buffer(1024)
            self.xlib.XGetErrorText(self._get_display(), details.get('xerror_details', {}).get('error_code', 0), xserver_error, len(xserver_error))
            xerror = xserver_error.value.decode('utf-8')
            if xerror != '0':
                details['xerror'] = xerror
        return details

    def _monitors_impl(self):
        """ Get positions of monitors. It will populate self._monitors. """
        display = self._get_display()
        int_ = int
        xrandr = self.xrandr
        gwa = XWindowAttributes()
        self.xlib.XGetWindowAttributes(display, self.root, ctypes.byref(gwa))
        self._monitors.append({'left':int_(gwa.x), 
         'top':int_(gwa.y), 
         'width':int_(gwa.width), 
         'height':int_(gwa.height)})
        mon = xrandr.XRRGetScreenResourcesCurrent(display, self.drawable).contents
        crtcs = mon.crtcs
        for idx in range(mon.ncrtc):
            crtc = xrandr.XRRGetCrtcInfo(display, mon, crtcs[idx]).contents
            if crtc.noutput == 0:
                xrandr.XRRFreeCrtcInfo(crtc)
            else:
                self._monitors.append({'left':int_(crtc.x), 
                 'top':int_(crtc.y), 
                 'width':int_(crtc.width), 
                 'height':int_(crtc.height)})
                xrandr.XRRFreeCrtcInfo(crtc)
        else:
            xrandr.XRRFreeScreenResources(mon)

    def _grab_impl(self, monitor):
        """ Retrieve all pixels from a monitor. Pixels have to be RGB. """
        ximage = self.xlib.XGetImage(self._get_display(), self.drawable, monitor['left'], monitor['top'], monitor['width'], monitor['height'], PLAINMASK, ZPIXMAP)
        try:
            bits_per_pixel = ximage.contents.bits_per_pixel
            if bits_per_pixel != 32:
                raise ScreenShotError('[XImage] bits per pixel value not (yet?) implemented: {}.'.format(bits_per_pixel))
            raw_data = ctypes.cast(ximage.contents.data, ctypes.POINTER(ctypes.c_ubyte * monitor['height'] * monitor['width'] * 4))
            data = bytearray(raw_data.contents)
        finally:
            self.xlib.XDestroyImage(ximage)

        return self.cls_image(data, monitor)