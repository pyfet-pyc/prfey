# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyttsx3\__init__.py
from .engine import Engine
import weakref
_activeEngines = weakref.WeakValueDictionary()

def init--- This code section failed: ---

 L.  19         0  SETUP_FINALLY        14  'to 14'

 L.  20         2  LOAD_GLOBAL              _activeEngines
                4  LOAD_FAST                'driverName'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'eng'
               10  POP_BLOCK        
               12  JUMP_FORWARD         50  'to 50'
             14_0  COME_FROM_FINALLY     0  '0'

 L.  21        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                48  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  22        26  LOAD_GLOBAL              Engine
               28  LOAD_FAST                'driverName'
               30  LOAD_FAST                'debug'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'eng'

 L.  23        36  LOAD_FAST                'eng'
               38  LOAD_GLOBAL              _activeEngines
               40  LOAD_FAST                'driverName'
               42  STORE_SUBSCR     
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            12  '12'

 L.  24        50  LOAD_FAST                'eng'
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 18


def speak(text):
    engine = init()
    engine.say(text)
    engine.runAndWait()