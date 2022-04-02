# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mss\linux.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import ctypes, ctypes.util, os, threading
from ctypes import POINTER, CFUNCTYPE, Structure, c_char_p, c_int, c_int32, c_long, c_ubyte, c_uint, c_uint32, c_ulong, c_ushort, c_void_p
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

class Display(Structure):
    __doc__ = '\n    Structure that serves as the connection to the X server\n    and that contains all the information about that X server.\n    '


class Event(Structure):
    __doc__ = '\n    XErrorEvent to debug eventual errors.\n    https://tronche.com/gui/x/xlib/event-handling/protocol-errors/default-handlers.html\n    '
    _fields_ = [
     (
      'type', c_int),
     (
      'display', POINTER(Display)),
     (
      'serial', c_ulong),
     (
      'error_code', c_ubyte),
     (
      'request_code', c_ubyte),
     (
      'minor_code', c_ubyte),
     (
      'resourceid', c_void_p)]


class XWindowAttributes(Structure):
    __doc__ = ' Attributes for the specified window. '
    _fields_ = [
     (
      'x', c_int32),
     (
      'y', c_int32),
     (
      'width', c_int32),
     (
      'height', c_int32),
     (
      'border_width', c_int32),
     (
      'depth', c_int32),
     (
      'visual', c_ulong),
     (
      'root', c_ulong),
     (
      'class', c_int32),
     (
      'bit_gravity', c_int32),
     (
      'win_gravity', c_int32),
     (
      'backing_store', c_int32),
     (
      'backing_planes', c_ulong),
     (
      'backing_pixel', c_ulong),
     (
      'save_under', c_int32),
     (
      'colourmap', c_ulong),
     (
      'mapinstalled', c_uint32),
     (
      'map_state', c_uint32),
     (
      'all_event_masks', c_ulong),
     (
      'your_event_mask', c_ulong),
     (
      'do_not_propagate_mask', c_ulong),
     (
      'override_redirect', c_int32),
     (
      'screen', c_ulong)]


class XImage(Structure):
    __doc__ = "\n    Description of an image as it exists in the client's memory.\n    https://tronche.com/gui/x/xlib/graphics/images.html\n    "
    _fields_ = [
     (
      'width', c_int),
     (
      'height', c_int),
     (
      'xoffset', c_int),
     (
      'format', c_int),
     (
      'data', c_void_p),
     (
      'byte_order', c_int),
     (
      'bitmap_unit', c_int),
     (
      'bitmap_bit_order', c_int),
     (
      'bitmap_pad', c_int),
     (
      'depth', c_int),
     (
      'bytes_per_line', c_int),
     (
      'bits_per_pixel', c_int),
     (
      'red_mask', c_ulong),
     (
      'green_mask', c_ulong),
     (
      'blue_mask', c_ulong)]


class XRRModeInfo(Structure):
    __doc__ = ' Voilà, voilà. '


class XRRScreenResources(Structure):
    __doc__ = '\n    Structure that contains arrays of XIDs that point to the\n    available outputs and associated CRTCs.\n    '
    _fields_ = [
     (
      'timestamp', c_ulong),
     (
      'configTimestamp', c_ulong),
     (
      'ncrtc', c_int),
     (
      'crtcs', POINTER(c_long)),
     (
      'noutput', c_int),
     (
      'outputs', POINTER(c_long)),
     (
      'nmode', c_int),
     (
      'modes', POINTER(XRRModeInfo))]


class XRRCrtcInfo(Structure):
    __doc__ = ' Structure that contains CRTC information. '
    _fields_ = [
     (
      'timestamp', c_ulong),
     (
      'x', c_int),
     (
      'y', c_int),
     (
      'width', c_int),
     (
      'height', c_int),
     (
      'mode', c_long),
     (
      'rotation', c_int),
     (
      'noutput', c_int),
     (
      'outputs', POINTER(c_long)),
     (
      'rotations', c_ushort),
     (
      'npossible', c_int),
     (
      'possible', POINTER(c_long))]


@CFUNCTYPE(c_int, POINTER(Display), POINTER(Event))
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


CFUNCTIONS = {'XDefaultRootWindow':(
  'xlib', [POINTER(Display)], POINTER(XWindowAttributes)), 
 'XDestroyImage':(
  'xlib', [POINTER(XImage)], c_void_p), 
 'XGetErrorText':(
  'xlib', [POINTER(Display), c_int, c_char_p, c_int], c_void_p), 
 'XGetImage':(
  'xlib',
  [
   POINTER(Display),
   POINTER(Display),
   c_int,
   c_int,
   c_uint,
   c_uint,
   c_ulong,
   c_int],
  POINTER(XImage)), 
 'XGetWindowAttributes':(
  'xlib',
  [
   POINTER(Display), POINTER(XWindowAttributes), POINTER(XWindowAttributes)],
  c_int), 
 'XOpenDisplay':(
  'xlib', [c_char_p], POINTER(Display)), 
 'XQueryExtension':(
  'xlib',
  [
   POINTER(Display),
   c_char_p,
   POINTER(c_int),
   POINTER(c_int),
   POINTER(c_int)],
  c_uint), 
 'XRRFreeCrtcInfo':(
  'xrandr', [POINTER(XRRCrtcInfo)], c_void_p), 
 'XRRFreeScreenResources':(
  'xrandr', [POINTER(XRRScreenResources)], c_void_p), 
 'XRRGetCrtcInfo':(
  'xrandr',
  [
   POINTER(Display), POINTER(XRRScreenResources), c_long],
  POINTER(XRRCrtcInfo)), 
 'XRRGetScreenResources':(
  'xrandr',
  [
   POINTER(Display), POINTER(Display)],
  POINTER(XRRScreenResources)), 
 'XRRGetScreenResourcesCurrent':(
  'xrandr',
  [
   POINTER(Display), POINTER(Display)],
  POINTER(XRRScreenResources)), 
 'XSetErrorHandler':(
  'xlib', [c_void_p], c_int)}

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
        self.drawable = ctypes.cast(self.root, POINTER(Display))

    def has_extension--- This code section failed: ---

 L. 317         0  LOAD_GLOBAL              lock
                2  SETUP_WITH          128  'to 128'
                4  POP_TOP          

 L. 318         6  LOAD_GLOBAL              c_int
                8  CALL_FUNCTION_0       0  ''
               10  STORE_FAST               'major_opcode_return'

 L. 319        12  LOAD_GLOBAL              c_int
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'first_event_return'

 L. 320        18  LOAD_GLOBAL              c_int
               20  CALL_FUNCTION_0       0  ''
               22  STORE_FAST               'first_error_return'

 L. 322        24  SETUP_FINALLY        78  'to 78'

 L. 323        26  LOAD_FAST                'self'
               28  LOAD_ATTR                xlib
               30  LOAD_METHOD              XQueryExtension

 L. 324        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _get_display
               36  CALL_METHOD_0         0  ''

 L. 325        38  LOAD_FAST                'extension'
               40  LOAD_METHOD              encode
               42  LOAD_STR                 'latin1'
               44  CALL_METHOD_1         1  ''

 L. 326        46  LOAD_GLOBAL              ctypes
               48  LOAD_METHOD              byref
               50  LOAD_FAST                'major_opcode_return'
               52  CALL_METHOD_1         1  ''

 L. 327        54  LOAD_GLOBAL              ctypes
               56  LOAD_METHOD              byref
               58  LOAD_FAST                'first_event_return'
               60  CALL_METHOD_1         1  ''

 L. 328        62  LOAD_GLOBAL              ctypes
               64  LOAD_METHOD              byref
               66  LOAD_FAST                'first_error_return'
               68  CALL_METHOD_1         1  ''

 L. 323        70  CALL_METHOD_5         5  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD        110  'to 110'
             78_0  COME_FROM_FINALLY    24  '24'

 L. 330        78  DUP_TOP          
               80  LOAD_GLOBAL              ScreenShotError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   108  'to 108'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 331        92  POP_EXCEPT       
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  POP_FINALLY           0  ''
              104  LOAD_CONST               False
              106  RETURN_VALUE     
            108_0  COME_FROM            84  '84'
              108  END_FINALLY      
            110_0  COME_FROM            76  '76'

 L. 333       110  POP_BLOCK        
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  LOAD_CONST               True
              122  RETURN_VALUE     
              124  POP_BLOCK        
              126  BEGIN_FINALLY    
            128_0  COME_FROM_WITH        2  '2'
              128  WITH_CLEANUP_START
              130  WITH_CLEANUP_FINISH
              132  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 96

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
        """ Set all ctypes functions and attach them to attributes. """
        cfactory = self._cfactory
        attrs = {'xlib':self.xlib, 
         'xrandr':self.xrandr}
        for func, (attr, argtypes, restype) in CFUNCTIONS.items():
            try:
                cfactory(attr=(attrs[attr]),
                  errcheck=validate,
                  func=func,
                  argtypes=argtypes,
                  restype=restype)
            except AttributeError:
                pass

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
        try:
            mon = xrandr.XRRGetScreenResourcesCurrent(display, self.drawable).contents
        except AttributeError:
            mon = xrandr.XRRGetScreenResources(display, self.drawable).contents
        else:
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
            raw_data = ctypes.cast(ximage.contents.data, POINTER(c_ubyte * monitor['height'] * monitor['width'] * 4))
            data = bytearray(raw_data.contents)
        finally:
            self.xlib.XDestroyImage(ximage)

        return self.cls_image(data, monitor)