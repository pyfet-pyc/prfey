# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: Core\Network\Location.py
import re, json, subprocess, urllib.request
macRegex = re.compile('[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$')
Command = 'chcp 65001 && ipconfig | findstr /i "Default Gateway"'
subprocess.check_output(Command, shell=True,
  stderr=(subprocess.DEVNULL),
  stdin=(subprocess.DEVNULL))

def GetMacByIP():
    a = subprocess.check_output('arp -a', shell=True,
      stderr=(subprocess.DEVNULL),
      stdin=(subprocess.DEVNULL))
    b = a.decode(encoding='cp866')
    c = b.find('')
    d = b[c:].split(' ')
    for b in d:
        if macRegex.match(b):
            return b.replace('-', ':')


def GetLocationByBSSID--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        34  'to 34'

 L.  39         2  LOAD_GLOBAL              urllib
                4  LOAD_ATTR                request
                6  LOAD_METHOD              urlopen
                8  LOAD_STR                 'http://api.mylnikov.org/geolocation/wifi?bssid='
               10  LOAD_FAST                'BSSID'
               12  FORMAT_VALUE          0  ''
               14  BUILD_STRING_2        2 
               16  CALL_METHOD_1         1  ''
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  LOAD_METHOD              decode
               24  LOAD_STR                 'utf8'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'Result'
               30  POP_BLOCK        
               32  JUMP_FORWARD         48  'to 48'
             34_0  COME_FROM_FINALLY     0  '0'

 L.  40        34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  41        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
               46  END_FINALLY      
             48_0  COME_FROM            32  '32'

 L.  43        48  LOAD_GLOBAL              json
               50  LOAD_METHOD              loads
               52  LOAD_FAST                'Result'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'Result'

 L.  44        58  LOAD_FAST                'Result'
               60  LOAD_STR                 'data'
               62  BINARY_SUBSCR    
               64  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 42