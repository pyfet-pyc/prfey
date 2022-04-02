# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: curses\__init__.py
"""curses

The main package for curses support for Python.  Normally used by importing
the package, and perhaps a particular module inside it.

   import curses
   from curses import textpad
   curses.initscr()
   ...

"""
from _curses import *
import os as _os, sys as _sys

def initscr():
    import _curses, curses
    setupterm(term=(_os.environ.get('TERM', 'unknown')), fd=(_sys.__stdout__.fileno()))
    stdscr = _curses.initscr()
    for key, value in _curses.__dict__.items():
        if not key[0:4] == 'ACS_':
            if key in ('LINES', 'COLS'):
                pass
        setattr(curses, key, value)
    else:
        return stdscr


def start_color():
    import _curses, curses
    retval = _curses.start_color()
    if hasattr(_curses, 'COLORS'):
        curses.COLORS = _curses.COLORS
    if hasattr(_curses, 'COLOR_PAIRS'):
        curses.COLOR_PAIRS = _curses.COLOR_PAIRS
    return retval


try:
    has_key
except NameError:
    from .has_key import has_key
else:

    def wrapper--- This code section failed: ---

 L.  71         0  LOAD_FAST                'args'
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L.  72         4  LOAD_FAST                'args'
                6  UNPACK_EX_1+0           
                8  STORE_FAST               'func'
               10  STORE_FAST               'args'
               12  JUMP_FORWARD         74  'to 74'
             14_0  COME_FROM             2  '2'

 L.  73        14  LOAD_STR                 'func'
               16  LOAD_FAST                'kwds'
               18  COMPARE_OP               in
               20  POP_JUMP_IF_FALSE    58  'to 58'

 L.  74        22  LOAD_FAST                'kwds'
               24  LOAD_METHOD              pop
               26  LOAD_STR                 'func'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'func'

 L.  75        32  LOAD_CONST               0
               34  LOAD_CONST               None
               36  IMPORT_NAME              warnings
               38  STORE_FAST               'warnings'

 L.  76        40  LOAD_FAST                'warnings'
               42  LOAD_ATTR                warn
               44  LOAD_STR                 "Passing 'func' as keyword argument is deprecated"

 L.  77        46  LOAD_GLOBAL              DeprecationWarning

 L.  77        48  LOAD_CONST               2

 L.  76        50  LOAD_CONST               ('stacklevel',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  POP_TOP          
               56  JUMP_FORWARD         74  'to 74'
             58_0  COME_FROM            20  '20'

 L.  79        58  LOAD_GLOBAL              TypeError
               60  LOAD_STR                 'wrapper expected at least 1 positional argument, got %d'

 L.  80        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'args'
               66  CALL_FUNCTION_1       1  ''

 L.  79        68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            56  '56'
             74_1  COME_FROM            12  '12'

 L.  82        74  SETUP_FINALLY       148  'to 148'

 L.  84        76  LOAD_GLOBAL              initscr
               78  CALL_FUNCTION_0       0  ''
               80  STORE_FAST               'stdscr'

 L.  88        82  LOAD_GLOBAL              noecho
               84  CALL_FUNCTION_0       0  ''
               86  POP_TOP          

 L.  89        88  LOAD_GLOBAL              cbreak
               90  CALL_FUNCTION_0       0  ''
               92  POP_TOP          

 L.  94        94  LOAD_FAST                'stdscr'
               96  LOAD_METHOD              keypad
               98  LOAD_CONST               1
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 100       104  SETUP_FINALLY       116  'to 116'

 L. 101       106  LOAD_GLOBAL              start_color
              108  CALL_FUNCTION_0       0  ''
              110  POP_TOP          
              112  POP_BLOCK        
              114  JUMP_FORWARD        128  'to 128'
            116_0  COME_FROM_FINALLY   104  '104'

 L. 102       116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 103       122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM           114  '114'

 L. 105       128  LOAD_FAST                'func'
              130  LOAD_FAST                'stdscr'
              132  BUILD_TUPLE_1         1 
              134  LOAD_FAST                'args'
              136  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              138  LOAD_FAST                'kwds'
              140  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              142  POP_BLOCK        
              144  CALL_FINALLY        148  'to 148'
              146  RETURN_VALUE     
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM_FINALLY    74  '74'

 L. 108       148  LOAD_STR                 'stdscr'
              150  LOAD_GLOBAL              locals
              152  CALL_FUNCTION_0       0  ''
              154  COMPARE_OP               in
              156  POP_JUMP_IF_FALSE   186  'to 186'

 L. 109       158  LOAD_FAST                'stdscr'
              160  LOAD_METHOD              keypad
              162  LOAD_CONST               0
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 110       168  LOAD_GLOBAL              echo
              170  CALL_FUNCTION_0       0  ''
              172  POP_TOP          

 L. 111       174  LOAD_GLOBAL              nocbreak
              176  CALL_FUNCTION_0       0  ''
              178  POP_TOP          

 L. 112       180  LOAD_GLOBAL              endwin
              182  CALL_FUNCTION_0       0  ''
              184  POP_TOP          
            186_0  COME_FROM           156  '156'
              186  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 144


    wrapper.__text_signature__ = '(func, /, *args, **kwds)'