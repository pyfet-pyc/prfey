# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Network\Information.py
import json, datetime, platform, subprocess, urllib.request

def Windows():
    System = platform.system()
    Release = platform.release()
    Version = System + ' ' + Release
    return Version


def Computer(Win32, Value):
    a = subprocess.check_output(('wmic ' + Win32 + ' get ' + Value), shell=True,
      stderr=(subprocess.DEVNULL),
      stdin=(subprocess.DEVNULL))
    b = a.decode('utf-8')
    c = b.split('\n')
    return c[1]


def RAM():
    Size = Computer('ComputerSystem', 'TotalPhysicalMemory')
    intSize = int(Size) / 1024 / 1024 / 1024
    return intSize


def SystemTime():
    Today = datetime.datetime.today()
    SystemTime = str(Today.hour) + ':' + str(Today.minute) + ':' + str(Today.second)
    return SystemTime


def Geolocation--- This code section failed: ---

 L.  48         0  SETUP_FINALLY        34  'to 34'

 L.  49         2  LOAD_GLOBAL              urllib
                4  LOAD_ATTR                request
                6  LOAD_METHOD              urlopen
                8  LOAD_STR                 'http://ip-api.com/json/'
               10  LOAD_FAST                'Ip'
               12  FORMAT_VALUE          0  ''
               14  BUILD_STRING_2        2 
               16  CALL_METHOD_1         1  ''
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  LOAD_METHOD              decode
               24  LOAD_STR                 'utf-8'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'Result'
               30  POP_BLOCK        
               32  JUMP_FORWARD         48  'to 48'
             34_0  COME_FROM_FINALLY     0  '0'

 L.  50        34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  51        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
               46  <48>             
             48_0  COME_FROM            32  '32'

 L.  53        48  LOAD_GLOBAL              json
               50  LOAD_METHOD              loads
               52  LOAD_FAST                'Result'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'Result'

 L.  54        58  LOAD_FAST                'Result'
               60  LOAD_FAST                'Value'
               62  BINARY_SUBSCR    
               64  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 42