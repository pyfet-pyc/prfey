# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Other\Rotate.py
import win32api, win32con
Rotations = {'0':win32con.DMDO_DEFAULT, 
 '90':win32con.DMDO_90, 
 '180':win32con.DMDO_180, 
 '270':win32con.DMDO_270}

def DisplayRotate--- This code section failed: ---

 L.  20         0  SETUP_FINALLY        14  'to 14'

 L.  21         2  LOAD_GLOBAL              Rotations
                4  LOAD_FAST                'Degrees'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'RotationValue'
               10  POP_BLOCK        
               12  JUMP_FORWARD         38  'to 38'
             14_0  COME_FROM_FINALLY     0  '0'

 L.  22        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                36  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  23        26  LOAD_GLOBAL              win32con
               28  LOAD_ATTR                DMDO_DEFAULT
               30  STORE_FAST               'RotationValue'
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            12  '12'

 L.  24        38  LOAD_GLOBAL              win32api
               40  LOAD_METHOD              EnumDisplayDevices
               42  LOAD_CONST               None
               44  LOAD_CONST               0
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'Device'

 L.  25        50  LOAD_GLOBAL              win32api
               52  LOAD_METHOD              EnumDisplaySettings
               54  LOAD_FAST                'Device'
               56  LOAD_ATTR                DeviceName
               58  LOAD_GLOBAL              win32con
               60  LOAD_ATTR                ENUM_CURRENT_SETTINGS
               62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'dm'

 L.  26        66  LOAD_FAST                'dm'
               68  LOAD_ATTR                DisplayOrientation
               70  LOAD_FAST                'RotationValue'
               72  BINARY_ADD       
               74  LOAD_CONST               2
               76  BINARY_MODULO    
               78  LOAD_CONST               1
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L.  27        84  LOAD_FAST                'dm'
               86  LOAD_ATTR                PelsHeight
               88  LOAD_FAST                'dm'
               90  LOAD_ATTR                PelsWidth
               92  ROT_TWO          
               94  LOAD_FAST                'dm'
               96  STORE_ATTR               PelsWidth
               98  LOAD_FAST                'dm'
              100  STORE_ATTR               PelsHeight
            102_0  COME_FROM            82  '82'

 L.  28       102  LOAD_FAST                'RotationValue'
              104  LOAD_FAST                'dm'
              106  STORE_ATTR               DisplayOrientation

 L.  29       108  LOAD_GLOBAL              win32api
              110  LOAD_METHOD              ChangeDisplaySettingsEx
              112  LOAD_FAST                'Device'
              114  LOAD_ATTR                DeviceName
              116  LOAD_FAST                'dm'
              118  CALL_METHOD_2         2  ''
              120  POP_TOP          

Parse error at or near `<121>' instruction at offset 18