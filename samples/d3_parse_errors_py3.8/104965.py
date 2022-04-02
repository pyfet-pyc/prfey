# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: click.py
import time
from pynput.mouse import Controller, Button
from pynput import keyboard
mouse = Controller()

class MouseCtrl:

    def __init__(self):
        pass

    def mouseLClick(self):
        return mouse.click(Button.left)

    def mouseRClick(self):
        return mouse.click(Button.right)


print('v - refresh\nb - purchase\nesc - quit program')
typeGet = (int(input('Iter?: ')) or 0) * 75

def on_release--- This code section failed: ---

 L.  14         0  SETUP_FINALLY       144  'to 144'

 L.  15         2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              keyboard
                6  LOAD_ATTR                Key
                8  LOAD_ATTR                esc
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L.  17        14  POP_BLOCK        
               16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            12  '12'

 L.  18        20  LOAD_FAST                'key'
               22  LOAD_ATTR                char
               24  LOAD_STR                 'v'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    72  'to 72'

 L.  19        30  LOAD_GLOBAL              print
               32  LOAD_STR                 'Refreshed screen'
               34  CALL_FUNCTION_1       1  ''
               36  POP_TOP          

 L.  20        38  LOAD_CONST               (761, 34)
               40  LOAD_GLOBAL              mouse
               42  STORE_ATTR               position

 L.  21        44  LOAD_GLOBAL              MouseCtrl
               46  CALL_FUNCTION_0       0  ''
               48  LOAD_METHOD              mouseLClick
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L.  22        54  LOAD_CONST               (942, 36)
               56  LOAD_GLOBAL              mouse
               58  STORE_ATTR               position

 L.  23        60  LOAD_GLOBAL              MouseCtrl
               62  CALL_FUNCTION_0       0  ''
               64  LOAD_METHOD              mouseLClick
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          
               70  JUMP_FORWARD        140  'to 140'
             72_0  COME_FROM            28  '28'

 L.  24        72  LOAD_FAST                'key'
               74  LOAD_ATTR                char
               76  LOAD_STR                 'b'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   140  'to 140'

 L.  25        82  LOAD_GLOBAL              print
               84  LOAD_STR                 'Purchasing'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          

 L.  26        90  LOAD_CONST               1759
               92  LOAD_CONST               182
               94  LOAD_GLOBAL              typeGet
               96  BINARY_ADD       
               98  BUILD_TUPLE_2         2 
              100  LOAD_GLOBAL              mouse
              102  STORE_ATTR               position

 L.  27       104  LOAD_GLOBAL              MouseCtrl
              106  CALL_FUNCTION_0       0  ''
              108  LOAD_METHOD              mouseLClick
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          

 L.  28       114  LOAD_GLOBAL              time
              116  LOAD_METHOD              sleep
              118  LOAD_CONST               0.1
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  29       124  LOAD_CONST               (863, 616)
              126  LOAD_GLOBAL              mouse
              128  STORE_ATTR               position

 L.  30       130  LOAD_GLOBAL              MouseCtrl
              132  CALL_FUNCTION_0       0  ''
              134  LOAD_METHOD              mouseLClick
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          
            140_0  COME_FROM            80  '80'
            140_1  COME_FROM            70  '70'
              140  POP_BLOCK        
              142  JUMP_FORWARD        156  'to 156'
            144_0  COME_FROM_FINALLY     0  '0'

 L.  32       144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L.  33       150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'
            156_1  COME_FROM           142  '142'

Parse error at or near `LOAD_CONST' instruction at offset 16


with keyboard.Listener(on_release=on_release) as listener:
    listener.join()
listener = keyboard.Listener(on_release=on_release)
listener.start()