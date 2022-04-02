# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32traceutil.py
import win32trace

def RunAsCollector--- This code section failed: ---

 L.  28         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L.  29         8  SETUP_FINALLY        32  'to 32'

 L.  30        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME              win32api
               16  STORE_FAST               'win32api'

 L.  31        18  LOAD_FAST                'win32api'
               20  LOAD_METHOD              SetConsoleTitle
               22  LOAD_STR                 'Python Trace Collector'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  JUMP_FORWARD         44  'to 44'
             32_0  COME_FROM_FINALLY     8  '8'

 L.  32        32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  33        38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            30  '30'

 L.  34        44  LOAD_GLOBAL              win32trace
               46  LOAD_METHOD              InitRead
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L.  35        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'Collecting Python Trace Output...'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  36        60  SETUP_FINALLY        86  'to 86'
             62_0  COME_FROM            80  '80'

 L.  39        62  LOAD_FAST                'sys'
               64  LOAD_ATTR                stdout
               66  LOAD_METHOD              write
               68  LOAD_GLOBAL              win32trace
               70  LOAD_METHOD              blockingread
               72  LOAD_CONST               500
               74  CALL_METHOD_1         1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            62  'to 62'
               82  POP_BLOCK        
               84  JUMP_FORWARD        112  'to 112'
             86_0  COME_FROM_FINALLY    60  '60'

 L.  40        86  DUP_TOP          
               88  LOAD_GLOBAL              KeyboardInterrupt
               90  <121>               110  ''
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  41        98  LOAD_GLOBAL              print
              100  LOAD_STR                 'Ctrl+C'
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
              110  <48>             
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            84  '84'

Parse error at or near `<48>' instruction at offset 42


def SetupForPrint--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              win32trace
                2  LOAD_METHOD              InitWrite
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  46         8  SETUP_FINALLY        22  'to 22'

 L.  47        10  LOAD_GLOBAL              print
               12  LOAD_STR                 'Redirecting output to win32trace remote collector'
               14  CALL_FUNCTION_1       1  ''
               16  POP_TOP          
               18  POP_BLOCK        
               20  JUMP_FORWARD         34  'to 34'
             22_0  COME_FROM_FINALLY     8  '8'

 L.  48        22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  49        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
               32  <48>             
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM            20  '20'

 L.  50        34  LOAD_GLOBAL              win32trace
               36  LOAD_METHOD              setprint
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

Parse error at or near `<48>' instruction at offset 32


if __name__ == '__main__':
    RunAsCollector()
else:
    SetupForPrint()