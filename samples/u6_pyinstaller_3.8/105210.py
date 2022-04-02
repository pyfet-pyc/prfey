# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\_util\darwin.py
"""
Utility functions and classes for the *Darwin* backend.
"""
import contextlib, ctypes, ctypes.util, six, objc, CoreFoundation, Quartz
from . import AbstractListener
OBJC = ctypes.PyDLL(objc._objc.__file__)
OBJC.PyObjCObject_New.restype = ctypes.py_object
OBJC.PyObjCObject_New.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]

def _wrap_value(value):
    """Converts a pointer to a *Python objc* value.

    :param value: The pointer to convert.

    :return: a wrapped value
    """
    return OBJC.PyObjCObject_New(value, 0, 1)


@contextlib.contextmanager
def _wrapped(value):
    """A context manager that converts a raw pointer to a *Python objc* value.

    When the block is exited, the value is released.

    :param value: The raw value to wrap.
    """
    wrapped_value = _wrap_value(value)
    try:
        (yield value)
    finally:
        CoreFoundation.CFRelease(wrapped_value)


class CarbonExtra(object):
    __doc__ = 'A class exposing some missing functionality from *Carbon* as class\n    attributes.\n    '
    _Carbon = ctypes.cdll.LoadLibrary(ctypes.util.find_library('Carbon'))
    _Carbon.TISCopyCurrentKeyboardInputSource.argtypes = []
    _Carbon.TISCopyCurrentKeyboardInputSource.restype = ctypes.c_void_p
    _Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource.argtypes = []
    _Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource.restype = ctypes.c_void_p
    _Carbon.TISGetInputSourceProperty.argtypes = [
     ctypes.c_void_p, ctypes.c_void_p]
    _Carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p
    _Carbon.LMGetKbdType.argtypes = []
    _Carbon.LMGetKbdType.restype = ctypes.c_uint32
    _Carbon.UCKeyTranslate.argtypes = [
     ctypes.c_void_p,
     ctypes.c_uint16,
     ctypes.c_uint16,
     ctypes.c_uint32,
     ctypes.c_uint32,
     ctypes.c_uint32,
     ctypes.POINTER(ctypes.c_uint32),
     ctypes.c_uint8,
     ctypes.POINTER(ctypes.c_uint8),
     ctypes.c_uint16 * 4]
    _Carbon.UCKeyTranslate.restype = ctypes.c_uint32
    TISCopyCurrentKeyboardInputSource = _Carbon.TISCopyCurrentKeyboardInputSource
    TISCopyCurrentASCIICapableKeyboardLayoutInputSource = _Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource
    kTISPropertyUnicodeKeyLayoutData = ctypes.c_void_p.in_dll(_Carbon, 'kTISPropertyUnicodeKeyLayoutData')
    TISGetInputSourceProperty = _Carbon.TISGetInputSourceProperty
    LMGetKbdType = _Carbon.LMGetKbdType
    kUCKeyActionDisplay = 3
    kUCKeyTranslateNoDeadKeysBit = 0
    UCKeyTranslate = _Carbon.UCKeyTranslate


@contextlib.contextmanager
def keycode_context--- This code section failed: ---

 L. 130         0  LOAD_CONST               (None, None)
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'keyboard_type'
                6  STORE_FAST               'layout_data'

 L. 132         8  LOAD_GLOBAL              CarbonExtra
               10  LOAD_ATTR                TISCopyCurrentKeyboardInputSource

 L. 133        12  LOAD_GLOBAL              CarbonExtra
               14  LOAD_ATTR                TISCopyCurrentASCIICapableKeyboardLayoutInputSource

 L. 131        16  BUILD_TUPLE_2         2 
               18  GET_ITER         
               20  FOR_ITER            124  'to 124'
               22  STORE_FAST               'source'

 L. 134        24  LOAD_GLOBAL              _wrapped
               26  LOAD_FAST                'source'
               28  CALL_FUNCTION_0       0  ''
               30  CALL_FUNCTION_1       1  ''
               32  SETUP_WITH          116  'to 116'
               34  STORE_FAST               'keyboard'

 L. 135        36  LOAD_GLOBAL              CarbonExtra
               38  LOAD_METHOD              LMGetKbdType
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'keyboard_type'

 L. 136        44  LOAD_GLOBAL              _wrap_value
               46  LOAD_GLOBAL              CarbonExtra
               48  LOAD_METHOD              TISGetInputSourceProperty

 L. 137        50  LOAD_FAST                'keyboard'

 L. 138        52  LOAD_GLOBAL              CarbonExtra
               54  LOAD_ATTR                kTISPropertyUnicodeKeyLayoutData

 L. 136        56  CALL_METHOD_2         2  ''
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'layout'

 L. 139        62  LOAD_FAST                'layout'
               64  POP_JUMP_IF_FALSE    78  'to 78'
               66  LOAD_FAST                'layout'
               68  LOAD_METHOD              bytes
               70  CALL_METHOD_0         0  ''
               72  LOAD_METHOD              tobytes
               74  CALL_METHOD_0         0  ''
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            64  '64'
               78  LOAD_CONST               None
             80_0  COME_FROM            76  '76'
               80  STORE_FAST               'layout_data'

 L. 140        82  LOAD_FAST                'keyboard'
               84  LOAD_CONST               None
               86  COMPARE_OP               is-not
               88  POP_JUMP_IF_FALSE   112  'to 112'
               90  LOAD_FAST                'layout_data'
               92  LOAD_CONST               None
               94  COMPARE_OP               is-not
               96  POP_JUMP_IF_FALSE   112  'to 112'

 L. 141        98  POP_BLOCK        
              100  BEGIN_FINALLY    
              102  WITH_CLEANUP_START
              104  WITH_CLEANUP_FINISH
              106  POP_FINALLY           0  ''
              108  POP_TOP          
              110  BREAK_LOOP          124  'to 124'
            112_0  COME_FROM            96  '96'
            112_1  COME_FROM            88  '88'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_WITH       32  '32'
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  END_FINALLY      
              122  JUMP_BACK            20  'to 20'

 L. 142       124  LOAD_FAST                'keyboard_type'
              126  LOAD_FAST                'layout_data'
              128  BUILD_TUPLE_2         2 
              130  YIELD_VALUE      
              132  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 100


def keycode_to_string(context, keycode, modifier_state=0):
    """Converts a keycode to a string.
    """
    LENGTH = 4
    keyboard_type, layout_data = context
    dead_key_state = ctypes.c_uint32
    length = ctypes.c_uint8
    unicode_string = (ctypes.c_uint16 * LENGTH)
    CarbonExtra.UCKeyTranslate(layout_data, keycode, CarbonExtra.kUCKeyActionDisplay, modifier_state, keyboard_type, CarbonExtra.kUCKeyTranslateNoDeadKeysBit, ctypes.byref(dead_key_state), LENGTH, ctypes.byref(length), unicode_string)
    return ''.join((six.unichr(unicode_string[i]) for i in range(length.value)))


def get_unicode_to_keycode_map--- This code section failed: ---

 L. 176         0  LOAD_GLOBAL              keycode_context
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           42  'to 42'
                6  STORE_DEREF              'context'

 L. 177         8  LOAD_CLOSURE             'context'
               10  BUILD_TUPLE_1         1 
               12  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               14  LOAD_STR                 'get_unicode_to_keycode_map.<locals>.<dictcomp>'
               16  MAKE_FUNCTION_8          'closure'

 L. 179        18  LOAD_GLOBAL              range
               20  LOAD_CONST               128
               22  CALL_FUNCTION_1       1  ''

 L. 177        24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH        4  '4'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 12


class ListenerMixin(object):
    __doc__ = 'A mixin for *Quartz* event listeners.\n\n    Subclasses should set a value for :attr:`_EVENTS` and implement\n    :meth:`_handle`.\n    '
    _EVENTS = tuple

    def _run--- This code section failed: ---

 L. 192         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _loop

 L. 193         6  SETUP_FINALLY       192  'to 192'

 L. 194         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _create_event_tap
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'tap'

 L. 195        16  LOAD_FAST                'tap'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    40  'to 40'

 L. 196        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _mark_ready
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          

 L. 197        32  POP_BLOCK        
               34  CALL_FINALLY        192  'to 192'
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            22  '22'

 L. 199        40  LOAD_GLOBAL              Quartz
               42  LOAD_METHOD              CFMachPortCreateRunLoopSource

 L. 200        44  LOAD_CONST               None

 L. 200        46  LOAD_FAST                'tap'

 L. 200        48  LOAD_CONST               0

 L. 199        50  CALL_METHOD_3         3  ''
               52  STORE_FAST               'loop_source'

 L. 201        54  LOAD_GLOBAL              Quartz
               56  LOAD_METHOD              CFRunLoopGetCurrent
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _loop

 L. 203        64  LOAD_GLOBAL              Quartz
               66  LOAD_METHOD              CFRunLoopAddSource

 L. 204        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _loop

 L. 204        72  LOAD_FAST                'loop_source'

 L. 204        74  LOAD_GLOBAL              Quartz
               76  LOAD_ATTR                kCFRunLoopDefaultMode

 L. 203        78  CALL_METHOD_3         3  ''
               80  POP_TOP          

 L. 205        82  LOAD_GLOBAL              Quartz
               84  LOAD_METHOD              CGEventTapEnable
               86  LOAD_FAST                'tap'
               88  LOAD_CONST               True
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          

 L. 207        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _mark_ready
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          

 L. 210       102  SETUP_FINALLY       176  'to 176'

 L. 211       104  LOAD_FAST                'self'
              106  LOAD_ATTR                running
              108  POP_JUMP_IF_FALSE   172  'to 172'

 L. 212       110  LOAD_GLOBAL              Quartz
              112  LOAD_METHOD              CFRunLoopRunInMode

 L. 213       114  LOAD_GLOBAL              Quartz
              116  LOAD_ATTR                kCFRunLoopDefaultMode

 L. 213       118  LOAD_CONST               1

 L. 213       120  LOAD_CONST               False

 L. 212       122  CALL_METHOD_3         3  ''
              124  STORE_FAST               'result'

 L. 214       126  SETUP_FINALLY       146  'to 146'

 L. 215       128  LOAD_FAST                'result'
              130  LOAD_GLOBAL              Quartz
              132  LOAD_ATTR                kCFRunLoopRunTimedOut
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_FALSE   142  'to 142'

 L. 216       138  POP_BLOCK        
              140  BREAK_LOOP          172  'to 172'
            142_0  COME_FROM           136  '136'
              142  POP_BLOCK        
              144  JUMP_BACK           104  'to 104'
            146_0  COME_FROM_FINALLY   126  '126'

 L. 217       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   168  'to 168'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L. 219       160  POP_EXCEPT       
              162  BREAK_LOOP          172  'to 172'
              164  POP_EXCEPT       
              166  JUMP_BACK           104  'to 104'
            168_0  COME_FROM           152  '152'
              168  END_FINALLY      
              170  JUMP_BACK           104  'to 104'
            172_0  COME_FROM_EXCEPT_CLAUSE   162  '162'
            172_1  COME_FROM_EXCEPT_CLAUSE   108  '108'
              172  POP_BLOCK        
              174  JUMP_FORWARD        188  'to 188'
            176_0  COME_FROM_FINALLY   102  '102'

 L. 221       176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 223       182  POP_EXCEPT       
              184  JUMP_FORWARD        188  'to 188'
              186  END_FINALLY      
            188_0  COME_FROM           184  '184'
            188_1  COME_FROM           174  '174'
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM            34  '34'
            192_1  COME_FROM_FINALLY     6  '6'

 L. 227       192  LOAD_CONST               None
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _loop
              198  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 34

    def _stop_platform(self):
        try:
            if self._loop is not None:
                Quartz.CFRunLoopStop(self._loop)
        except AttributeError:
            pass

    def _create_event_tap--- This code section failed: ---

 L. 244         0  LOAD_GLOBAL              Quartz
                2  LOAD_METHOD              CGEventTapCreate

 L. 245         4  LOAD_GLOBAL              Quartz
                6  LOAD_ATTR                kCGSessionEventTap

 L. 246         8  LOAD_GLOBAL              Quartz
               10  LOAD_ATTR                kCGHeadInsertEventTap

 L. 249        12  LOAD_FAST                'self'
               14  LOAD_ATTR                suppress

 L. 247        16  POP_JUMP_IF_TRUE     34  'to 34'

 L. 250        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _intercept
               22  LOAD_CONST               None
               24  COMPARE_OP               is

 L. 247        26  POP_JUMP_IF_FALSE    34  'to 34'
               28  LOAD_GLOBAL              Quartz
               30  LOAD_ATTR                kCGEventTapOptionListenOnly
               32  JUMP_FORWARD         38  'to 38'
             34_0  COME_FROM            26  '26'
             34_1  COME_FROM            16  '16'

 L. 251        34  LOAD_GLOBAL              Quartz
               36  LOAD_ATTR                kCGEventTapOptionDefault
             38_0  COME_FROM            32  '32'

 L. 252        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _EVENTS

 L. 253        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _handler

 L. 254        46  LOAD_CONST               None

 L. 244        48  CALL_METHOD_6         6  ''
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 34_1

    @AbstractListener._emitter
    def _handler(self, proxy, event_type, event, refcon):
        """The callback registered with *Mac OSX* for mouse events.

        This method will call the callbacks registered on initialisation.
        """
        self._handle(proxy, event_type, event, refcon)
        if self._intercept is not None:
            return self._intercept(event_type, event)
        if self.suppress:
            return

    def _handle(self, proxy, event_type, event, refcon):
        """The device specific callback handler.

        This method calls the appropriate callback registered when this
        listener was created based on the event.
        """
        raise NotImplementedError