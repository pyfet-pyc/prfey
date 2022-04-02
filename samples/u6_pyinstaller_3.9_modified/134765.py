# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\dialogs\status.py
from pywin.mfc import dialog
from pywin.mfc.thread import WinThread
import threading, win32ui, win32con, win32api, time

def MakeProgressDlgTemplate(caption, staticText=''):
    style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE
    w = 215
    h = 36
    h = 40
    dlg = [
     [
      caption,
      (
       0, 0, w, h),
      style,
      None,
      (8, 'MS Sans Serif')]]
    s = win32con.WS_TABSTOP | cs
    dlg.append([130, staticText, 1000, (7, 7, w - 7, h - 32), cs | win32con.SS_LEFT])
    return dlg


class CStatusProgressDialog(dialog.Dialog):

    def __init__(self, title, msg='', maxticks=100, tickincr=1):
        self.initMsg = msg
        templ = MakeProgressDlgTemplate(title, msg)
        dialog.Dialog.__init__(self, templ)
        self.maxticks = maxticks
        self.tickincr = tickincr
        self.pbar = None

    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        self.static = self.GetDlgItem(1000)
        self.pbar = win32ui.CreateProgressCtrl()
        self.pbar.CreateWindow(win32con.WS_CHILD | win32con.WS_VISIBLE, (10, 30, 310,
                                                                         44), self, 1001)
        self.pbar.SetRange(0, self.maxticks)
        self.pbar.SetStep(self.tickincr)
        self.progress = 0
        self.pincr = 5
        return rc

    def Close(self):
        self.EndDialog(0)

    def SetMaxTicks--- This code section failed: ---

 L.  70         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pbar
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  71        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pbar
               14  LOAD_METHOD              SetRange
               16  LOAD_CONST               0
               18  LOAD_FAST                'maxticks'
               20  CALL_METHOD_2         2  ''
               22  POP_TOP          
             24_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def Tick--- This code section failed: ---

 L.  74         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pbar
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.  75        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pbar
               14  LOAD_METHOD              StepIt
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          
             20_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def SetTitle(self, text):
        self.SetWindowText(text)

    def SetText(self, text):
        self.SetDlgItemText(1000, text)

    def Set--- This code section failed: ---

 L.  84         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pbar
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    44  'to 44'

 L.  85        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pbar
               14  LOAD_METHOD              SetPos
               16  LOAD_FAST                'pos'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L.  86        22  LOAD_FAST                'max'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L.  87        30  LOAD_FAST                'self'
               32  LOAD_ATTR                pbar
               34  LOAD_METHOD              SetRange
               36  LOAD_CONST               0
               38  LOAD_FAST                'max'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
             44_0  COME_FROM            28  '28'
             44_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


MYWM_SETTITLE = win32con.WM_USER + 10
MYWM_SETMSG = win32con.WM_USER + 11
MYWM_TICK = win32con.WM_USER + 12
MYWM_SETMAXTICKS = win32con.WM_USER + 13
MYWM_SET = win32con.WM_USER + 14

class CThreadedStatusProcessDialog(CStatusProgressDialog):

    def __init__(self, title, msg='', maxticks=100, tickincr=1):
        self.title = title
        self.msg = msg
        self.threadid = win32api.GetCurrentThreadId()
        CStatusProgressDialog.__init__(self, title, msg, maxticks, tickincr)

    def OnInitDialog(self):
        rc = CStatusProgressDialog.OnInitDialog(self)
        self.HookMessage(self.OnTitle, MYWM_SETTITLE)
        self.HookMessage(self.OnMsg, MYWM_SETMSG)
        self.HookMessage(self.OnTick, MYWM_TICK)
        self.HookMessage(self.OnMaxTicks, MYWM_SETMAXTICKS)
        self.HookMessage(self.OnSet, MYWM_SET)
        return rc

    def _Send--- This code section failed: ---

 L. 114         0  SETUP_FINALLY        16  'to 16'

 L. 115         2  LOAD_FAST                'self'
                4  LOAD_METHOD              PostMessage
                6  LOAD_FAST                'msg'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         36  'to 36'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 116        16  DUP_TOP          
               18  LOAD_GLOBAL              win32ui
               20  LOAD_ATTR                error
               22  <121>                34  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 119        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  <48>             
             36_0  COME_FROM            32  '32'
             36_1  COME_FROM            14  '14'

Parse error at or near `<121>' instruction at offset 22

    def OnTitle(self, msg):
        CStatusProgressDialog.SetTitle(self, self.title)

    def OnMsg(self, msg):
        CStatusProgressDialog.SetText(self, self.msg)

    def OnTick(self, msg):
        CStatusProgressDialog.Tick(self)

    def OnMaxTicks(self, msg):
        CStatusProgressDialog.SetMaxTicks(self, self.maxticks)

    def OnSet(self, msg):
        CStatusProgressDialog.Set(self, self.pos, self.max)

    def Close--- This code section failed: ---

 L. 137         0  LOAD_FAST                'self'
                2  LOAD_ATTR                threadid
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  <74>             
                8  LOAD_STR                 'No thread!'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 138        14  LOAD_GLOBAL              win32api
               16  LOAD_METHOD              PostThreadMessage
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                threadid
               22  LOAD_GLOBAL              win32con
               24  LOAD_ATTR                WM_QUIT
               26  LOAD_CONST               0
               28  LOAD_CONST               0
               30  CALL_METHOD_4         4  ''
               32  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def SetMaxTicks(self, maxticks):
        self.maxticks = maxticks
        self._Send(MYWM_SETMAXTICKS)

    def SetTitle(self, title):
        self.title = title
        self._Send(MYWM_SETTITLE)

    def SetText(self, text):
        self.msg = text
        self._Send(MYWM_SETMSG)

    def Tick(self):
        self._Send(MYWM_TICK)

    def Set(self, pos, max=None):
        self.pos = pos
        self.max = max
        self._Send(MYWM_SET)


class ProgressThread(WinThread):

    def __init__(self, title, msg='', maxticks=100, tickincr=1):
        self.title = title
        self.msg = msg
        self.maxticks = maxticks
        self.tickincr = tickincr
        self.dialog = None
        WinThread.__init__(self)
        self.createdEvent = threading.Event()

    def InitInstance--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              CThreadedStatusProcessDialog
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                title
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                msg
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                maxticks
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                tickincr
               18  CALL_FUNCTION_4       4  ''
               20  LOAD_FAST                'self'
               22  STORE_ATTR               dialog

 L. 168        24  LOAD_FAST                'self'
               26  LOAD_ATTR                dialog
               28  LOAD_METHOD              CreateWindow
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L. 169        34  SETUP_FINALLY        50  'to 50'

 L. 170        36  LOAD_FAST                'self'
               38  LOAD_ATTR                dialog
               40  LOAD_METHOD              SetForegroundWindow
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD         70  'to 70'
             50_0  COME_FROM_FINALLY    34  '34'

 L. 171        50  DUP_TOP          
               52  LOAD_GLOBAL              win32ui
               54  LOAD_ATTR                error
               56  <121>                68  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 172        64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
               68  <48>             
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            48  '48'

 L. 173        70  LOAD_FAST                'self'
               72  LOAD_ATTR                createdEvent
               74  LOAD_METHOD              set
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 174        80  LOAD_GLOBAL              WinThread
               82  LOAD_METHOD              InitInstance
               84  LOAD_FAST                'self'
               86  CALL_METHOD_1         1  ''
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56

    def ExitInstance(self):
        return 0


def StatusProgressDialog(title, msg='', maxticks=100, parent=None):
    d = CStatusProgressDialog(title, msg, maxticks)
    d.CreateWindow(parent)
    return d


def ThreadedStatusProgressDialog(title, msg='', maxticks=100):
    t = ProgressThread(title, msg, maxticks)
    t.CreateThread()
    end_time = time.time() + 10
    while time.time() < end_time:
        if t.createdEvent.isSet():
            break
        win32ui.PumpWaitingMessages()
        time.sleep(0.1)

    return t.dialog


def demo():
    d = StatusProgressDialog('A Demo', 'Doing something...')
    import win32api
    for i in range(100):
        if i == 50:
            d.SetText('Getting there...')
        if i == 90:
            d.SetText('Nearly done...')
        win32api.Sleep(20)
        d.Tick()
    else:
        d.Close()


def thread_demo():
    d = ThreadedStatusProgressDialog('A threaded demo', 'Doing something')
    import win32api
    for i in range(100):
        if i == 50:
            d.SetText('Getting there...')
        if i == 90:
            d.SetText('Nearly done...')
        win32api.Sleep(20)
        d.Tick()
    else:
        d.Close()


if __name__ == '__main__':
    thread_demo()