# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\mfc\window.py
from . import object
import win32ui, win32con

class Wnd(object.CmdTarget):

    def __init__(self, initobj=None):
        object.CmdTarget.__init__(self, initobj)
        if self._obj_:
            self._obj_.HookMessage(self.OnDestroy, win32con.WM_DESTROY)

    def OnDestroy(self, msg):
        pass


class FrameWnd(Wnd):

    def __init__(self, wnd):
        Wnd.__init__(self, wnd)


class MDIChildWnd(FrameWnd):

    def __init__--- This code section failed: ---

 L.  30         0  LOAD_FAST                'wnd'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  31         8  LOAD_GLOBAL              win32ui
               10  LOAD_METHOD              CreateMDIChild
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'wnd'
             16_0  COME_FROM             6  '6'

 L.  32        16  LOAD_GLOBAL              FrameWnd
               18  LOAD_METHOD              __init__
               20  LOAD_FAST                'self'
               22  LOAD_FAST                'wnd'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def OnCreateClient--- This code section failed: ---

 L.  34         0  LOAD_FAST                'context'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    32  'to 32'
                8  LOAD_FAST                'context'
               10  LOAD_ATTR                template
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L.  35        18  LOAD_FAST                'context'
               20  LOAD_ATTR                template
               22  LOAD_METHOD              CreateView
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'context'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          
             32_0  COME_FROM            16  '16'
             32_1  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


class MDIFrameWnd(FrameWnd):

    def __init__--- This code section failed: ---

 L.  39         0  LOAD_FAST                'wnd'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  40         8  LOAD_GLOBAL              win32ui
               10  LOAD_METHOD              CreateMDIFrame
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'wnd'
             16_0  COME_FROM             6  '6'

 L.  41        16  LOAD_GLOBAL              FrameWnd
               18  LOAD_METHOD              __init__
               20  LOAD_FAST                'self'
               22  LOAD_FAST                'wnd'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

Parse error at or near `None' instruction at offset -1