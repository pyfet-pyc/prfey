# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\mfc\thread.py
from . import object
import win32ui

class WinThread(object.CmdTarget):

    def __init__--- This code section failed: ---

 L.   8         0  LOAD_FAST                'initObj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.   9         8  LOAD_GLOBAL              win32ui
               10  LOAD_METHOD              CreateThread
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'initObj'
             16_0  COME_FROM             6  '6'

 L.  10        16  LOAD_GLOBAL              object
               18  LOAD_ATTR                CmdTarget
               20  LOAD_METHOD              __init__
               22  LOAD_FAST                'self'
               24  LOAD_FAST                'initObj'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def InitInstance(self):
        pass

    def ExitInstance(self):
        pass


class WinApp(WinThread):

    def __init__--- This code section failed: ---

 L.  20         0  LOAD_FAST                'initApp'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  21         8  LOAD_GLOBAL              win32ui
               10  LOAD_METHOD              GetApp
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'initApp'
             16_0  COME_FROM             6  '6'

 L.  22        16  LOAD_GLOBAL              WinThread
               18  LOAD_METHOD              __init__
               20  LOAD_FAST                'self'
               22  LOAD_FAST                'initApp'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1