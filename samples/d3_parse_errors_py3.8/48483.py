# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\keyboard\_winkeyboard.py
"""
This is the Windows backend for keyboard events, and is implemented by
invoking the Win32 API through the ctypes module. This is error prone
and can introduce very unpythonic failure modes, such as segfaults and
low level memory leaks. But it is also dependency-free, very performant
well documented on Microsoft's website and scattered examples.

# TODO:
- Keypad numbers still print as numbers even when numlock is off.
- No way to specify if user wants a keypad key or not in `map_char`.
"""
from __future__ import unicode_literals
import re, atexit, traceback
from threading import Lock
from collections import defaultdict
from ._keyboard_event import KeyboardEvent, KEY_DOWN, KEY_UP
from ._canonical_names import normalize_name
try:
    chr = unichr
except NameError:
    pass
else:
    import ctypes
    from ctypes import c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, CFUNCTYPE, POINTER
    from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, HMODULE, LPCWSTR, HINSTANCE, HWND
    LPMSG = POINTER(MSG)
    ULONG_PTR = POINTER(DWORD)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    GetModuleHandleW = kernel32.GetModuleHandleW
    GetModuleHandleW.restype = HMODULE
    GetModuleHandleW.argtypes = [LPCWSTR]
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    VK_PACKET = 231
    INPUT_MOUSE = 0
    INPUT_KEYBOARD = 1
    INPUT_HARDWARE = 2
    KEYEVENTF_KEYUP = 2
    KEYEVENTF_UNICODE = 4

    class KBDLLHOOKSTRUCT(Structure):
        _fields_ = [
         (
          'vk_code', DWORD),
         (
          'scan_code', DWORD),
         (
          'flags', DWORD),
         (
          'time', c_int),
         (
          'dwExtraInfo', ULONG_PTR)]


    class MOUSEINPUT(ctypes.Structure):
        _fields_ = (
         (
          'dx', LONG),
         (
          'dy', LONG),
         (
          'mouseData', DWORD),
         (
          'dwFlags', DWORD),
         (
          'time', DWORD),
         (
          'dwExtraInfo', ULONG_PTR))


    class KEYBDINPUT(ctypes.Structure):
        _fields_ = (
         (
          'wVk', WORD),
         (
          'wScan', WORD),
         (
          'dwFlags', DWORD),
         (
          'time', DWORD),
         (
          'dwExtraInfo', ULONG_PTR))


    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = (
         (
          'uMsg', DWORD),
         (
          'wParamL', WORD),
         (
          'wParamH', WORD))


    class _INPUTunion(ctypes.Union):
        _fields_ = (
         (
          'mi', MOUSEINPUT),
         (
          'ki', KEYBDINPUT),
         (
          'hi', HARDWAREINPUT))


    class INPUT(ctypes.Structure):
        _fields_ = (
         (
          'type', DWORD),
         (
          'union', _INPUTunion))


    LowLevelKeyboardProc = CFUNCTYPE(c_int, WPARAM, LPARAM, POINTER(KBDLLHOOKSTRUCT))
    SetWindowsHookEx = user32.SetWindowsHookExW
    SetWindowsHookEx.argtypes = [c_int, LowLevelKeyboardProc, HINSTANCE, DWORD]
    SetWindowsHookEx.restype = HHOOK
    CallNextHookEx = user32.CallNextHookEx
    CallNextHookEx.restype = c_int
    UnhookWindowsHookEx = user32.UnhookWindowsHookEx
    UnhookWindowsHookEx.argtypes = [HHOOK]
    UnhookWindowsHookEx.restype = BOOL
    GetMessage = user32.GetMessageW
    GetMessage.argtypes = [LPMSG, HWND, c_uint, c_uint]
    GetMessage.restype = BOOL
    TranslateMessage = user32.TranslateMessage
    TranslateMessage.argtypes = [LPMSG]
    TranslateMessage.restype = BOOL
    DispatchMessage = user32.DispatchMessageA
    DispatchMessage.argtypes = [LPMSG]
    keyboard_state_type = c_uint8 * 256
    GetKeyboardState = user32.GetKeyboardState
    GetKeyboardState.argtypes = [keyboard_state_type]
    GetKeyboardState.restype = BOOL
    GetKeyNameText = user32.GetKeyNameTextW
    GetKeyNameText.argtypes = [c_long, LPWSTR, c_int]
    GetKeyNameText.restype = c_int
    MapVirtualKey = user32.MapVirtualKeyW
    MapVirtualKey.argtypes = [c_uint, c_uint]
    MapVirtualKey.restype = c_uint
    ToUnicode = user32.ToUnicode
    ToUnicode.argtypes = [c_uint, c_uint, keyboard_state_type, LPWSTR, c_int, c_uint]
    ToUnicode.restype = c_int
    SendInput = user32.SendInput
    SendInput.argtypes = [c_uint, POINTER(INPUT), c_int]
    SendInput.restype = c_uint
    MAPVK_VK_TO_CHAR = 2
    MAPVK_VK_TO_VSC = 0
    MAPVK_VSC_TO_VK = 1
    MAPVK_VK_TO_VSC_EX = 4
    MAPVK_VSC_TO_VK_EX = 3
    VkKeyScan = user32.VkKeyScanW
    VkKeyScan.argtypes = [WCHAR]
    VkKeyScan.restype = c_short
    LLKHF_INJECTED = 16
    WM_KEYDOWN = 256
    WM_KEYUP = 257
    WM_SYSKEYDOWN = 260
    WM_SYSKEYUP = 261
    keyboard_event_types = {WM_KEYDOWN: KEY_DOWN, 
     WM_KEYUP: KEY_UP, 
     WM_SYSKEYDOWN: KEY_DOWN, 
     WM_SYSKEYUP: KEY_UP}
    official_virtual_keys = {3:('control-break processing', False), 
     8:('backspace', False), 
     9:('tab', False), 
     12:('clear', False), 
     13:('enter', False), 
     16:('shift', False), 
     17:('ctrl', False), 
     18:('alt', False), 
     19:('pause', False), 
     20:('caps lock', False), 
     21:('ime kana mode', False), 
     21:('ime hanguel mode', False), 
     21:('ime hangul mode', False), 
     23:('ime junja mode', False), 
     24:('ime final mode', False), 
     25:('ime hanja mode', False), 
     25:('ime kanji mode', False), 
     27:('esc', False), 
     28:('ime convert', False), 
     29:('ime nonconvert', False), 
     30:('ime accept', False), 
     31:('ime mode change request', False), 
     32:('spacebar', False), 
     33:('page up', False), 
     34:('page down', False), 
     35:('end', False), 
     36:('home', False), 
     37:('left', False), 
     38:('up', False), 
     39:('right', False), 
     40:('down', False), 
     41:('select', False), 
     42:('print', False), 
     43:('execute', False), 
     44:('print screen', False), 
     45:('insert', False), 
     46:('delete', False), 
     47:('help', False), 
     48:('0', False), 
     49:('1', False), 
     50:('2', False), 
     51:('3', False), 
     52:('4', False), 
     53:('5', False), 
     54:('6', False), 
     55:('7', False), 
     56:('8', False), 
     57:('9', False), 
     65:('a', False), 
     66:('b', False), 
     67:('c', False), 
     68:('d', False), 
     69:('e', False), 
     70:('f', False), 
     71:('g', False), 
     72:('h', False), 
     73:('i', False), 
     74:('j', False), 
     75:('k', False), 
     76:('l', False), 
     77:('m', False), 
     78:('n', False), 
     79:('o', False), 
     80:('p', False), 
     81:('q', False), 
     82:('r', False), 
     83:('s', False), 
     84:('t', False), 
     85:('u', False), 
     86:('v', False), 
     87:('w', False), 
     88:('x', False), 
     89:('y', False), 
     90:('z', False), 
     91:('left windows', False), 
     92:('right windows', False), 
     93:('applications', False), 
     95:('sleep', False), 
     96:('0', True), 
     97:('1', True), 
     98:('2', True), 
     99:('3', True), 
     100:('4', True), 
     101:('5', True), 
     102:('6', True), 
     103:('7', True), 
     104:('8', True), 
     105:('9', True), 
     106:('*', True), 
     107:('+', True), 
     108:('separator', True), 
     109:('-', True), 
     110:('decimal', True), 
     111:('/', True), 
     112:('f1', False), 
     113:('f2', False), 
     114:('f3', False), 
     115:('f4', False), 
     116:('f5', False), 
     117:('f6', False), 
     118:('f7', False), 
     119:('f8', False), 
     120:('f9', False), 
     121:('f10', False), 
     122:('f11', False), 
     123:('f12', False), 
     124:('f13', False), 
     125:('f14', False), 
     126:('f15', False), 
     127:('f16', False), 
     128:('f17', False), 
     129:('f18', False), 
     130:('f19', False), 
     131:('f20', False), 
     132:('f21', False), 
     133:('f22', False), 
     134:('f23', False), 
     135:('f24', False), 
     144:('num lock', False), 
     145:('scroll lock', False), 
     160:('left shift', False), 
     161:('right shift', False), 
     162:('left ctrl', False), 
     163:('right ctrl', False), 
     164:('left menu', False), 
     165:('right menu', False), 
     166:('browser back', False), 
     167:('browser forward', False), 
     168:('browser refresh', False), 
     169:('browser stop', False), 
     170:('browser search key', False), 
     171:('browser favorites', False), 
     172:('browser start and home', False), 
     173:('volume mute', False), 
     174:('volume down', False), 
     175:('volume up', False), 
     176:('next track', False), 
     177:('previous track', False), 
     178:('stop media', False), 
     179:('play/pause media', False), 
     180:('start mail', False), 
     181:('select media', False), 
     182:('start application 1', False), 
     183:('start application 2', False), 
     187:('+', False), 
     188:(',', False), 
     189:('-', False), 
     190:('.', False), 
     229:('ime process', False), 
     246:('attn', False), 
     247:('crsel', False), 
     248:('exsel', False), 
     249:('erase eof', False), 
     250:('play', False), 
     251:('zoom', False), 
     252:('reserved ', False), 
     253:('pa1', False), 
     254:('clear', False)}
    tables_lock = Lock()
    to_name = defaultdict(list)
    from_name = defaultdict(list)
    scan_code_to_vk = {}
    distinct_modifiers = [
     (),
     ('shift', ),
     ('alt gr', ),
     ('num lock', ),
     ('shift', 'num lock'),
     ('caps lock', ),
     ('shift', 'caps lock'),
     ('alt gr', 'num lock')]
    name_buffer = ctypes.create_unicode_buffer(32)
    unicode_buffer = ctypes.create_unicode_buffer(32)
    keyboard_state = keyboard_state_type()

    def get_event_names(scan_code, vk, is_extended, modifiers):
        is_keypad = (scan_code, vk, is_extended) in keypad_keys
        is_official = vk in official_virtual_keys
        if is_keypad:
            if is_official:
                yield official_virtual_keys[vk][0]
        keyboard_state[16] = 128 * ('shift' in modifiers)
        keyboard_state[17] = 128 * ('alt gr' in modifiers)
        keyboard_state[18] = 128 * ('alt gr' in modifiers)
        keyboard_state[20] = 1 * ('caps lock' in modifiers)
        keyboard_state[144] = 1 * ('num lock' in modifiers)
        keyboard_state[145] = 1 * ('scroll lock' in modifiers)
        unicode_ret = ToUnicode(vk, scan_code, keyboard_state, unicode_buffer, len(unicode_buffer), 0)
        if unicode_ret:
            if unicode_buffer.value:
                yield unicode_buffer.value
                ToUnicode(vk, scan_code, keyboard_state, unicode_buffer, len(unicode_buffer), 0)
        name_ret = GetKeyNameText(scan_code << 16 | is_extended << 24, name_buffer, 1024)
        if name_ret:
            if name_buffer.value:
                yield name_buffer.value
        char = user32.MapVirtualKeyW(vk, MAPVK_VK_TO_CHAR) & 255
        if char != 0:
            yield chr(char)
        if not is_keypad:
            if is_official:
                yield official_virtual_keys[vk][0]


    def _setup_name_tables--- This code section failed: ---

 L. 388         0  LOAD_GLOBAL              tables_lock
              2_4  SETUP_WITH          304  'to 304'
                6  POP_TOP          

 L. 389         8  LOAD_GLOBAL              to_name
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 389        12  POP_BLOCK        
               14  BEGIN_FINALLY    
               16  WITH_CLEANUP_START
               18  WITH_CLEANUP_FINISH
               20  POP_FINALLY           0  ''
               22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            10  '10'

 L. 393        26  LOAD_LISTCOMP            '<code_object <listcomp>>'
               28  LOAD_STR                 '_setup_name_tables.<locals>.<listcomp>'
               30  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               32  LOAD_GLOBAL              range
               34  LOAD_CONST               256
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'all_scan_codes'

 L. 394        44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               46  LOAD_STR                 '_setup_name_tables.<locals>.<listcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_GLOBAL              range
               52  LOAD_CONST               256
               54  CALL_FUNCTION_1       1  ''
               56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'all_vks'

 L. 395        62  LOAD_FAST                'all_scan_codes'
               64  LOAD_FAST                'all_vks'
               66  BINARY_ADD       
               68  GET_ITER         
             70_0  COME_FROM           234  '234'
             70_1  COME_FROM            96  '96'
               70  FOR_ITER            236  'to 236'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'scan_code'
               76  STORE_FAST               'vk'

 L. 397        78  LOAD_FAST                'scan_code'
               80  LOAD_FAST                'vk'
               82  LOAD_CONST               0
               84  LOAD_CONST               0
               86  LOAD_CONST               0
               88  BUILD_TUPLE_5         5 
               90  LOAD_GLOBAL              to_name
               92  COMPARE_OP               in
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 398        96  JUMP_BACK            70  'to 70'
             98_0  COME_FROM            94  '94'

 L. 400        98  LOAD_FAST                'scan_code'
              100  LOAD_GLOBAL              scan_code_to_vk
              102  COMPARE_OP               not-in
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L. 401       106  LOAD_FAST                'vk'
              108  LOAD_GLOBAL              scan_code_to_vk
              110  LOAD_FAST                'scan_code'
              112  STORE_SUBSCR     
            114_0  COME_FROM           104  '104'

 L. 404       114  LOAD_CONST               (0, 1)
              116  GET_ITER         
            118_0  COME_FROM           232  '232'
              118  FOR_ITER            234  'to 234'
              120  STORE_FAST               'extended'

 L. 405       122  LOAD_GLOBAL              distinct_modifiers
              124  GET_ITER         
            126_0  COME_FROM           230  '230'
            126_1  COME_FROM           156  '156'
              126  FOR_ITER            232  'to 232'
              128  STORE_FAST               'modifiers'

 L. 406       130  LOAD_FAST                'scan_code'
              132  LOAD_FAST                'vk'
              134  LOAD_FAST                'extended'
              136  LOAD_FAST                'modifiers'
              138  BUILD_TUPLE_4         4 
              140  STORE_FAST               'entry'

 L. 408       142  LOAD_GLOBAL              list
              144  LOAD_GLOBAL              get_event_names
              146  LOAD_FAST                'entry'
              148  CALL_FUNCTION_EX      0  'positional arguments only'
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'names'

 L. 409       154  LOAD_FAST                'names'
              156  POP_JUMP_IF_FALSE_BACK   126  'to 126'

 L. 411       158  LOAD_LISTCOMP            '<code_object <listcomp>>'
              160  LOAD_STR                 '_setup_name_tables.<locals>.<listcomp>'
              162  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              164  LOAD_FAST                'names'
              166  GET_ITER         
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'lowercase_names'

 L. 412       172  LOAD_FAST                'names'
              174  LOAD_FAST                'lowercase_names'
              176  BINARY_ADD       
              178  LOAD_GLOBAL              to_name
              180  LOAD_FAST                'entry'
              182  STORE_SUBSCR     

 L. 415       184  LOAD_GLOBAL              enumerate
              186  LOAD_GLOBAL              map
              188  LOAD_GLOBAL              normalize_name
              190  LOAD_FAST                'names'
              192  LOAD_FAST                'lowercase_names'
              194  BINARY_ADD       
              196  CALL_FUNCTION_2       2  ''
              198  CALL_FUNCTION_1       1  ''
              200  GET_ITER         
            202_0  COME_FROM           228  '228'
              202  FOR_ITER            230  'to 230'
              204  UNPACK_SEQUENCE_2     2 
              206  STORE_FAST               'i'
              208  STORE_FAST               'name'

 L. 416       210  LOAD_GLOBAL              from_name
              212  LOAD_FAST                'name'
              214  BINARY_SUBSCR    
              216  LOAD_METHOD              append
              218  LOAD_FAST                'i'
              220  LOAD_FAST                'entry'
              222  BUILD_TUPLE_2         2 
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          
              228  JUMP_BACK           202  'to 202'
            230_0  COME_FROM           202  '202'
              230  JUMP_BACK           126  'to 126'
            232_0  COME_FROM           126  '126'
              232  JUMP_BACK           118  'to 118'
            234_0  COME_FROM           118  '118'
              234  JUMP_BACK            70  'to 70'
            236_0  COME_FROM            70  '70'

 L. 424       236  LOAD_CONST               (0, 1)
              238  GET_ITER         
            240_0  COME_FROM           298  '298'
              240  FOR_ITER            300  'to 300'
              242  STORE_FAST               'extended'

 L. 425       244  LOAD_GLOBAL              distinct_modifiers
              246  GET_ITER         
            248_0  COME_FROM           296  '296'
              248  FOR_ITER            298  'to 298'
              250  STORE_FAST               'modifiers'

 L. 426       252  LOAD_STR                 'alt gr'
              254  BUILD_LIST_1          1 
              256  LOAD_GLOBAL              to_name
              258  LOAD_CONST               541
              260  LOAD_CONST               162
              262  LOAD_FAST                'extended'
              264  LOAD_FAST                'modifiers'
              266  BUILD_TUPLE_4         4 
              268  STORE_SUBSCR     

 L. 427       270  LOAD_GLOBAL              from_name
              272  LOAD_STR                 'alt gr'
              274  BINARY_SUBSCR    
              276  LOAD_METHOD              append
              278  LOAD_CONST               1
              280  LOAD_CONST               541
              282  LOAD_CONST               162
              284  LOAD_FAST                'extended'
              286  LOAD_FAST                'modifiers'
              288  BUILD_TUPLE_4         4 
              290  BUILD_TUPLE_2         2 
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  JUMP_BACK           248  'to 248'
            298_0  COME_FROM           248  '248'
              298  JUMP_BACK           240  'to 240'
            300_0  COME_FROM           240  '240'
              300  POP_BLOCK        
              302  BEGIN_FINALLY    
            304_0  COME_FROM_WITH        2  '2'
              304  WITH_CLEANUP_START
              306  WITH_CLEANUP_FINISH
              308  END_FINALLY      

 L. 429       310  LOAD_GLOBAL              defaultdict
              312  LOAD_LAMBDA              '<code_object <lambda>>'
              314  LOAD_STR                 '_setup_name_tables.<locals>.<lambda>'
              316  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              318  CALL_FUNCTION_1       1  ''
              320  STORE_DEREF              'modifiers_preference'

 L. 430       322  LOAD_DEREF               'modifiers_preference'
              324  LOAD_METHOD              update
              326  LOAD_CONST               0
              328  LOAD_CONST               1
              330  LOAD_CONST               2
              332  LOAD_CONST               3
              334  LOAD_CONST               4
              336  LOAD_CONST               ((), ('shift',), ('alt gr',), ('ctrl',), ('alt',))
              338  BUILD_CONST_KEY_MAP_5     5 
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          

 L. 431       344  LOAD_CLOSURE             'modifiers_preference'
              346  BUILD_TUPLE_1         1 
              348  LOAD_CODE                <code_object order_key>
              350  LOAD_STR                 '_setup_name_tables.<locals>.order_key'
              352  MAKE_FUNCTION_8          'closure'
              354  STORE_FAST               'order_key'

 L. 435       356  LOAD_GLOBAL              list
              358  LOAD_GLOBAL              from_name
              360  LOAD_METHOD              items
              362  CALL_METHOD_0         0  ''
              364  CALL_FUNCTION_1       1  ''
              366  GET_ITER         
            368_0  COME_FROM           396  '396'
              368  FOR_ITER            400  'to 400'
              370  UNPACK_SEQUENCE_2     2 
              372  STORE_FAST               'name'
              374  STORE_FAST               'entries'

 L. 436       376  LOAD_GLOBAL              sorted
              378  LOAD_GLOBAL              set
              380  LOAD_FAST                'entries'
              382  CALL_FUNCTION_1       1  ''
              384  LOAD_FAST                'order_key'
              386  LOAD_CONST               ('key',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  LOAD_GLOBAL              from_name
              392  LOAD_FAST                'name'
              394  STORE_SUBSCR     
          396_398  JUMP_BACK           368  'to 368'
            400_0  COME_FROM           368  '368'

Parse error at or near `BEGIN_FINALLY' instruction at offset 14


    init = _setup_name_tables
    keypad_keys = [
     (126, 194, 0),
     (126, 194, 0),
     (28, 13, 1),
     (28, 13, 1),
     (53, 111, 1),
     (53, 111, 1),
     (55, 106, 0),
     (55, 106, 0),
     (69, 144, 1),
     (69, 144, 1),
     (71, 103, 0),
     (71, 36, 0),
     (72, 104, 0),
     (72, 38, 0),
     (73, 105, 0),
     (73, 33, 0),
     (74, 109, 0),
     (74, 109, 0),
     (75, 100, 0),
     (75, 37, 0),
     (76, 101, 0),
     (76, 12, 0),
     (77, 102, 0),
     (77, 39, 0),
     (78, 107, 0),
     (78, 107, 0),
     (79, 35, 0),
     (79, 97, 0),
     (80, 40, 0),
     (80, 98, 0),
     (81, 34, 0),
     (81, 99, 0),
     (82, 45, 0),
     (82, 96, 0),
     (83, 110, 0),
     (83, 46, 0)]
    shift_is_pressed = False
    altgr_is_pressed = False
    ignore_next_right_alt = False
    shift_vks = set([16, 160, 161])

    def prepare_intercept(callback):
        """
    Registers a Windows low level keyboard hook. The provided callback will
    be invoked for each high-level keyboard event, and is expected to return
    True if the key event should be passed to the next program, or False if
    the event is to be blocked.

    No event is processed until the Windows messages are pumped (see
    start_intercept).
    """
        _setup_name_tables()

        def process_key(event_type, vk, scan_code, is_extended):
            global altgr_is_pressed
            global ignore_next_right_alt
            global shift_is_pressed
            if vk == 165:
                if ignore_next_right_alt:
                    ignore_next_right_alt = False
                    return True
            modifiers = ('shift', ) * shift_is_pressed + ('alt gr', ) * altgr_is_pressed + ('num lock', ) * (user32.GetKeyState(144) & 1) + ('caps lock', ) * (user32.GetKeyState(20) & 1) + ('scroll lock', ) * (user32.GetKeyState(145) & 1)
            entry = (
             scan_code, vk, is_extended, modifiers)
            if entry not in to_name:
                to_name[entry] = list(get_event_names(*entry))
            names = to_name[entry]
            name = names[0] if names else None
            if vk in shift_vks:
                shift_is_pressed = event_type == KEY_DOWN
            if scan_code == 541:
                if vk == 162:
                    ignore_next_right_alt = True
                    altgr_is_pressed = event_type == KEY_DOWN
            is_keypad = (
             scan_code, vk, is_extended) in keypad_keys
            return callback(KeyboardEvent(event_type=event_type, scan_code=(scan_code or -vk), name=name, is_keypad=is_keypad))

        def low_level_keyboard_handler--- This code section failed: ---

 L. 532         0  SETUP_FINALLY        98  'to 98'

 L. 533         2  LOAD_FAST                'lParam'
                4  LOAD_ATTR                contents
                6  LOAD_ATTR                vk_code
                8  STORE_FAST               'vk'

 L. 535        10  LOAD_GLOBAL              LLKHF_INJECTED
               12  LOAD_CONST               32
               14  BINARY_OR        
               16  STORE_FAST               'fake_alt'

 L. 537        18  LOAD_FAST                'vk'
               20  LOAD_GLOBAL              VK_PACKET
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    94  'to 94'
               26  LOAD_FAST                'lParam'
               28  LOAD_ATTR                contents
               30  LOAD_ATTR                flags
               32  LOAD_FAST                'fake_alt'
               34  BINARY_AND       
               36  LOAD_FAST                'fake_alt'
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE    94  'to 94'

 L. 538        42  LOAD_GLOBAL              keyboard_event_types
               44  LOAD_FAST                'wParam'
               46  BINARY_SUBSCR    
               48  STORE_FAST               'event_type'

 L. 539        50  LOAD_FAST                'lParam'
               52  LOAD_ATTR                contents
               54  LOAD_ATTR                flags
               56  LOAD_CONST               1
               58  BINARY_AND       
               60  STORE_FAST               'is_extended'

 L. 540        62  LOAD_FAST                'lParam'
               64  LOAD_ATTR                contents
               66  LOAD_ATTR                scan_code
               68  STORE_FAST               'scan_code'

 L. 541        70  LOAD_DEREF               'process_key'
               72  LOAD_FAST                'event_type'
               74  LOAD_FAST                'vk'
               76  LOAD_FAST                'scan_code'
               78  LOAD_FAST                'is_extended'
               80  CALL_FUNCTION_4       4  ''
               82  STORE_FAST               'should_continue'

 L. 542        84  LOAD_FAST                'should_continue'
               86  POP_JUMP_IF_TRUE     94  'to 94'

 L. 543        88  POP_BLOCK        
               90  LOAD_CONST               -1
               92  RETURN_VALUE     
             94_0  COME_FROM            86  '86'
             94_1  COME_FROM            40  '40'
             94_2  COME_FROM            24  '24'
               94  POP_BLOCK        
               96  JUMP_FORWARD        148  'to 148'
             98_0  COME_FROM_FINALLY     0  '0'

 L. 544        98  DUP_TOP          
              100  LOAD_GLOBAL              Exception
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   146  'to 146'
              106  POP_TOP          
              108  STORE_FAST               'e'
              110  POP_TOP          
              112  SETUP_FINALLY       134  'to 134'

 L. 545       114  LOAD_GLOBAL              print
              116  LOAD_STR                 'Error in keyboard hook:'
              118  CALL_FUNCTION_1       1  ''
              120  POP_TOP          

 L. 546       122  LOAD_GLOBAL              traceback
              124  LOAD_METHOD              print_exc
              126  CALL_METHOD_0         0  ''
              128  POP_TOP          
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM_FINALLY   112  '112'
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           104  '104'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            96  '96'

 L. 548       148  LOAD_GLOBAL              CallNextHookEx
              150  LOAD_CONST               None
              152  LOAD_FAST                'nCode'
              154  LOAD_FAST                'wParam'
              156  LOAD_FAST                'lParam'
              158  CALL_FUNCTION_4       4  ''
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 90

        WH_KEYBOARD_LL = c_int(13)
        keyboard_callback = LowLevelKeyboardProc(low_level_keyboard_handler)
        handle = GetModuleHandleW(None)
        thread_id = DWORD(0)
        keyboard_hook = SetWindowsHookEx(WH_KEYBOARD_LL, keyboard_callback, handle, thread_id)
        atexit.register(UnhookWindowsHookEx, keyboard_callback)


    def listen(callback):
        prepare_intercept(callback)
        msg = LPMSG()
        while True:
            if not GetMessage(msg, 0, 0, 0):
                TranslateMessage(msg)
                DispatchMessage(msg)


    def map_name(name):
        _setup_name_tables()
        entries = from_name.get(name)
        if not entries:
            raise ValueError('Key name {} is not mapped to any known key.'.format(repr(name)))
        for i, entry in entries:
            scan_code, vk, is_extended, modifiers = entry
            yield (scan_code or -vk, modifiers)


    def _send_event(code, event_type):
        if code == 541:
            user32.keybd_event(17, code, event_type, 0)
            user32.keybd_event(18, code, event_type, 0)
        elif code > 0:
            vk = scan_code_to_vk.get(code, 0)
            user32.keybd_event(vk, code, event_type, 0)
        else:
            user32.keybd_event(-code, 0, event_type, 0)


    def press(code):
        _send_eventcode0


    def release(code):
        _send_eventcode2


    def type_unicode(character):
        surrogates = bytearray(character.encode('utf-16le'))
        presses = []
        releases = []
        for i in range(0, len(surrogates), 2):
            higher, lower = surrogates[i:i + 2]
            structure = KEYBDINPUT(0, (lower << 8) + higher, KEYEVENTF_UNICODE, 0, None)
            presses.append(INPUTINPUT_KEYBOARD_INPUTunion(ki=structure))
            structure = KEYBDINPUT(0, (lower << 8) + higher, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)
            releases.append(INPUTINPUT_KEYBOARD_INPUTunion(ki=structure))
        else:
            inputs = presses + releases
            nInputs = len(inputs)
            LPINPUT = INPUT * nInputs
            pInputs = LPINPUT(*inputs)
            cbSize = c_int(ctypes.sizeof(INPUT))
            SendInput(nInputs, pInputs, cbSize)


    if __name__ == '__main__':
        _setup_name_tables()
        import pprint
        pprint.pprint(to_name)
        pprint.pprint(from_name)