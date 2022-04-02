# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: colorama\winterm.py
from . import win32

class WinColor(object):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    MAGENTA = 5
    YELLOW = 6
    GREY = 7


class WinStyle(object):
    NORMAL = 0
    BRIGHT = 8
    BRIGHT_BACKGROUND = 128


class WinTerm(object):

    def __init__(self):
        self._default = win32.GetConsoleScreenBufferInfo(win32.STDOUT).wAttributes
        self.set_attrs(self._default)
        self._default_fore = self._fore
        self._default_back = self._back
        self._default_style = self._style
        self._light = 0

    def get_attrs(self):
        return self._fore + self._back * 16 + (self._style | self._light)

    def set_attrs(self, value):
        self._fore = value & 7
        self._back = value >> 4 & 7
        self._style = value & (WinStyle.BRIGHT | WinStyle.BRIGHT_BACKGROUND)

    def reset_all(self, on_stderr=None):
        self.set_attrs(self._default)
        self.set_console(attrs=(self._default))
        self._light = 0

    def fore--- This code section failed: ---

 L.  50         0  LOAD_FAST                'fore'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  51         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _default_fore
               12  STORE_FAST               'fore'
             14_0  COME_FROM             6  '6'

 L.  52        14  LOAD_FAST                'fore'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _fore

 L.  54        20  LOAD_FAST                'light'
               22  POP_JUMP_IF_FALSE    42  'to 42'

 L.  55        24  LOAD_FAST                'self'
               26  DUP_TOP          
               28  LOAD_ATTR                _light
               30  LOAD_GLOBAL              WinStyle
               32  LOAD_ATTR                BRIGHT
               34  INPLACE_OR       
               36  ROT_TWO          
               38  STORE_ATTR               _light
               40  JUMP_FORWARD         60  'to 60'
             42_0  COME_FROM            22  '22'

 L.  57        42  LOAD_FAST                'self'
               44  DUP_TOP          
               46  LOAD_ATTR                _light
               48  LOAD_GLOBAL              WinStyle
               50  LOAD_ATTR                BRIGHT
               52  UNARY_INVERT     
               54  INPLACE_AND      
               56  ROT_TWO          
               58  STORE_ATTR               _light
             60_0  COME_FROM            40  '40'

 L.  58        60  LOAD_FAST                'self'
               62  LOAD_ATTR                set_console
               64  LOAD_FAST                'on_stderr'
               66  LOAD_CONST               ('on_stderr',)
               68  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               70  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def back--- This code section failed: ---

 L.  61         0  LOAD_FAST                'back'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  62         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _default_back
               12  STORE_FAST               'back'
             14_0  COME_FROM             6  '6'

 L.  63        14  LOAD_FAST                'back'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _back

 L.  65        20  LOAD_FAST                'light'
               22  POP_JUMP_IF_FALSE    42  'to 42'

 L.  66        24  LOAD_FAST                'self'
               26  DUP_TOP          
               28  LOAD_ATTR                _light
               30  LOAD_GLOBAL              WinStyle
               32  LOAD_ATTR                BRIGHT_BACKGROUND
               34  INPLACE_OR       
               36  ROT_TWO          
               38  STORE_ATTR               _light
               40  JUMP_FORWARD         60  'to 60'
             42_0  COME_FROM            22  '22'

 L.  68        42  LOAD_FAST                'self'
               44  DUP_TOP          
               46  LOAD_ATTR                _light
               48  LOAD_GLOBAL              WinStyle
               50  LOAD_ATTR                BRIGHT_BACKGROUND
               52  UNARY_INVERT     
               54  INPLACE_AND      
               56  ROT_TWO          
               58  STORE_ATTR               _light
             60_0  COME_FROM            40  '40'

 L.  69        60  LOAD_FAST                'self'
               62  LOAD_ATTR                set_console
               64  LOAD_FAST                'on_stderr'
               66  LOAD_CONST               ('on_stderr',)
               68  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               70  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def style--- This code section failed: ---

 L.  72         0  LOAD_FAST                'style'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.  73         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _default_style
               12  STORE_FAST               'style'
             14_0  COME_FROM             6  '6'

 L.  74        14  LOAD_FAST                'style'
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _style

 L.  75        20  LOAD_FAST                'self'
               22  LOAD_ATTR                set_console
               24  LOAD_FAST                'on_stderr'
               26  LOAD_CONST               ('on_stderr',)
               28  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               30  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def set_console--- This code section failed: ---

 L.  78         0  LOAD_FAST                'attrs'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  79         8  LOAD_FAST                'self'
               10  LOAD_METHOD              get_attrs
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'attrs'
             16_0  COME_FROM             6  '6'

 L.  80        16  LOAD_GLOBAL              win32
               18  LOAD_ATTR                STDOUT
               20  STORE_FAST               'handle'

 L.  81        22  LOAD_FAST                'on_stderr'
               24  POP_JUMP_IF_FALSE    32  'to 32'

 L.  82        26  LOAD_GLOBAL              win32
               28  LOAD_ATTR                STDERR
               30  STORE_FAST               'handle'
             32_0  COME_FROM            24  '24'

 L.  83        32  LOAD_GLOBAL              win32
               34  LOAD_METHOD              SetConsoleTextAttribute
               36  LOAD_FAST                'handle'
               38  LOAD_FAST                'attrs'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def get_position(self, handle):
        position = win32.GetConsoleScreenBufferInfo(handle).dwCursorPosition
        position.X += 1
        position.Y += 1
        return position

    def set_cursor_position--- This code section failed: ---

 L.  94         0  LOAD_FAST                'position'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  97         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  98        12  LOAD_GLOBAL              win32
               14  LOAD_ATTR                STDOUT
               16  STORE_FAST               'handle'

 L.  99        18  LOAD_FAST                'on_stderr'
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 100        22  LOAD_GLOBAL              win32
               24  LOAD_ATTR                STDERR
               26  STORE_FAST               'handle'
             28_0  COME_FROM            20  '20'

 L. 101        28  LOAD_GLOBAL              win32
               30  LOAD_METHOD              SetConsoleCursorPosition
               32  LOAD_FAST                'handle'
               34  LOAD_FAST                'position'
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def cursor_adjust(self, x, y, on_stderr=False):
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        position = self.get_position(handle)
        adjusted_position = (position.Y + y, position.X + x)
        win32.SetConsoleCursorPosition(handle, adjusted_position, adjust=False)

    def erase_screen(self, mode=0, on_stderr=False):
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        csbi = win32.GetConsoleScreenBufferInfo(handle)
        cells_in_screen = csbi.dwSize.X * csbi.dwSize.Y
        cells_before_cursor = csbi.dwSize.X * csbi.dwCursorPosition.Y + csbi.dwCursorPosition.X
        if mode == 0:
            from_coord = csbi.dwCursorPosition
            cells_to_erase = cells_in_screen - cells_before_cursor
        elif mode == 1:
            from_coord = win32.COORD00
            cells_to_erase = cells_before_cursor
        elif mode == 2:
            from_coord = win32.COORD00
            cells_to_erase = cells_in_screen
        else:
            return
        win32.FillConsoleOutputCharacter(handle, ' ', cells_to_erase, from_coord)
        win32.FillConsoleOutputAttribute(handle, self.get_attrs, cells_to_erase, from_coord)
        if mode == 2:
            win32.SetConsoleCursorPositionhandle(1, 1)

    def erase_line(self, mode=0, on_stderr=False):
        handle = win32.STDOUT
        if on_stderr:
            handle = win32.STDERR
        csbi = win32.GetConsoleScreenBufferInfo(handle)
        if mode == 0:
            from_coord = csbi.dwCursorPosition
            cells_to_erase = csbi.dwSize.X - csbi.dwCursorPosition.X
        elif mode == 1:
            from_coord = win32.COORD0csbi.dwCursorPosition.Y
            cells_to_erase = csbi.dwCursorPosition.X
        elif mode == 2:
            from_coord = win32.COORD0csbi.dwCursorPosition.Y
            cells_to_erase = csbi.dwSize.X
        else:
            return
        win32.FillConsoleOutputCharacter(handle, ' ', cells_to_erase, from_coord)
        win32.FillConsoleOutputAttribute(handle, self.get_attrs, cells_to_erase, from_coord)

    def set_title(self, title):
        win32.SetConsoleTitle(title)