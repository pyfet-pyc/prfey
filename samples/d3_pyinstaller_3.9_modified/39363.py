# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: gen.py
import time, os
start = time.perf_counter()
os.system('cls')
from colorama import Fore
import threading, requests, random, ctypes
from dhooks import Webhook

class GenNitroCode:

    def __init__--- This code section failed: ---

 L.  10         0  LOAD_STR                 ''
                2  LOAD_FAST                'self'
                4  STORE_ATTR               nitroCode

 L.  11         6  BUILD_LIST_0          0 
                8  LOAD_CONST               ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
               10  CALL_FINALLY         13  'to 13'
               12  STORE_FAST               'char'

 L.  12        14  LOAD_GLOBAL              range
               16  LOAD_CONST               16
               18  CALL_FUNCTION_1       1  ''
               20  GET_ITER         
             22_0  COME_FROM            44  '44'
               22  FOR_ITER             46  'to 46'
               24  STORE_FAST               'i'

 L.  13        26  LOAD_FAST                'self'
               28  LOAD_ATTR                nitroCode
               30  LOAD_GLOBAL              random
               32  LOAD_METHOD              choice
               34  LOAD_FAST                'char'
               36  CALL_METHOD_1         1  ''
               38  BINARY_ADD       
               40  LOAD_FAST                'self'
               42  STORE_ATTR               nitroCode
               44  JUMP_BACK            22  'to 22'
             46_0  COME_FROM            22  '22'

Parse error at or near `CALL_FINALLY' instruction at offset 10


def getWebhook--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              open
                2  LOAD_STR                 'webhook-link.txt'
                4  LOAD_STR                 'r'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           42  'to 42'
               10  STORE_FAST               'webhook'

 L.  17        12  LOAD_FAST                'webhook'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'result'

 L.  18        20  LOAD_FAST                'webhook'
               22  LOAD_METHOD              close
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  LOAD_CONST               None
               32  DUP_TOP          
               34  DUP_TOP          
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM_WITH        8  '8'
               42  <49>             
               44  POP_JUMP_IF_TRUE     48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          
               54  POP_EXCEPT       
               56  POP_TOP          
             58_0  COME_FROM            40  '40'

 L.  19        58  LOAD_FAST                'result'
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 32


def getProxies():
    r = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000&ssl=yes')
    proxies = []
    for proxy in r.text.split('\n'):
        proxy = proxy.replace('\r', '')
        if proxy:
            proxies.append(proxy)
    else:
        return proxies


def testNitroCodes--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              getWebhook
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'webhook'

 L.  32         6  LOAD_FAST                'webhook'
                8  LOAD_STR                 'None'
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L.  33        14  LOAD_CONST               False
               16  STORE_FAST               'usingWebhook'
               18  JUMP_FORWARD         24  'to 24'
             20_0  COME_FROM            12  '12'

 L.  35        20  LOAD_CONST               True
               22  STORE_FAST               'usingWebhook'
             24_0  COME_FROM            18  '18'

 L.  36        24  LOAD_CONST               0
               26  STORE_FAST               'testedCodes'

 L.  37        28  LOAD_GLOBAL              range
               30  LOAD_CONST               3
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM           342  '342'
            36_38  FOR_ITER            344  'to 344'
               40  STORE_FAST               'i'

 L.  38        42  LOAD_GLOBAL              getProxies
               44  CALL_FUNCTION_0       0  ''
               46  STORE_FAST               'ProxyList'

 L.  39        48  LOAD_FAST                'ProxyList'
               50  GET_ITER         
             52_0  COME_FROM           340  '340'
            52_54  FOR_ITER            342  'to 342'
               56  STORE_FAST               'proxy'

 L.  40        58  LOAD_FAST                'proxy'
               60  LOAD_FAST                'proxy'
               62  LOAD_CONST               ('http://', 'https://')
               64  BUILD_CONST_KEY_MAP_2     2 
               66  STORE_FAST               'ProxyParameters'

 L.  41        68  LOAD_GLOBAL              range
               70  LOAD_CONST               3
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
             76_0  COME_FROM           338  '338'
            76_78  FOR_ITER            340  'to 340'
               80  STORE_FAST               'i'

 L.  42        82  LOAD_GLOBAL              GenNitroCode
               84  CALL_FUNCTION_0       0  ''
               86  STORE_FAST               'nitrocode'

 L.  43        88  LOAD_GLOBAL              requests
               90  LOAD_ATTR                get
               92  LOAD_STR                 'https://discordapp.com/api/v6/entitlements/gift-codes/'
               94  LOAD_FAST                'nitrocode'
               96  LOAD_ATTR                nitroCode
               98  FORMAT_VALUE          0  ''
              100  BUILD_STRING_2        2 
              102  LOAD_FAST                'ProxyParameters'
              104  LOAD_CONST               5
              106  LOAD_CONST               ('proxies', 'timeout')
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  STORE_FAST               'url'

 L.  44       112  LOAD_FAST                'url'
              114  LOAD_ATTR                status_code
              116  LOAD_CONST               200
              118  COMPARE_OP               ==
          120_122  POP_JUMP_IF_FALSE   276  'to 276'

 L.  45       124  LOAD_FAST                'usingWebhook'
              126  LOAD_CONST               True
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L.  46       132  LOAD_GLOBAL              Webhook
              134  LOAD_FAST                'webhook'
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'hook'

 L.  47       140  LOAD_FAST                'hook'
              142  LOAD_ATTR                send
              144  LOAD_STR                 '@everyone nitro is ready https://discord.gift/'
              146  LOAD_FAST                'nitrocode'
              148  LOAD_ATTR                nitroCode
              150  FORMAT_VALUE          0  ''
              152  BUILD_STRING_2        2 
              154  LOAD_CONST               ('content',)
              156  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              158  POP_TOP          
            160_0  COME_FROM           130  '130'

 L.  48       160  LOAD_GLOBAL              open
              162  LOAD_STR                 'nitroCodes.txt'
              164  LOAD_STR                 'w'
              166  CALL_FUNCTION_2       2  ''
              168  SETUP_WITH          206  'to 206'
              170  STORE_FAST               'nitros'

 L.  49       172  LOAD_FAST                'nitros'
              174  LOAD_METHOD              write
              176  LOAD_FAST                'nitrocode'
              178  LOAD_ATTR                nitroCode
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L.  50       184  LOAD_FAST                'nitros'
              186  LOAD_METHOD              close
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  LOAD_CONST               None
              196  DUP_TOP          
              198  DUP_TOP          
              200  CALL_FUNCTION_3       3  ''
              202  POP_TOP          
              204  JUMP_FORWARD        222  'to 222'
            206_0  COME_FROM_WITH      168  '168'
              206  <49>             
              208  POP_JUMP_IF_TRUE    212  'to 212'
              210  <48>             
            212_0  COME_FROM           208  '208'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          
              218  POP_EXCEPT       
              220  POP_TOP          
            222_0  COME_FROM           204  '204'

 L.  51       222  LOAD_GLOBAL              print
              224  LOAD_GLOBAL              Fore
              226  LOAD_ATTR                WHITE
              228  FORMAT_VALUE          0  ''
              230  LOAD_STR                 '['
              232  LOAD_GLOBAL              Fore
              234  LOAD_ATTR                GREEN
              236  FORMAT_VALUE          0  ''
              238  LOAD_STR                 '!'
              240  LOAD_GLOBAL              Fore
              242  LOAD_ATTR                WHITE
              244  FORMAT_VALUE          0  ''
              246  LOAD_STR                 '] '
              248  LOAD_GLOBAL              Fore
              250  LOAD_ATTR                GREEN
              252  FORMAT_VALUE          0  ''
              254  LOAD_STR                 'VALID CODE'
              256  LOAD_GLOBAL              Fore
              258  LOAD_ATTR                WHITE
              260  FORMAT_VALUE          0  ''
              262  LOAD_STR                 ' : https://discord.gift/'
              264  LOAD_FAST                'nitrocode'
              266  LOAD_ATTR                nitroCode
              268  FORMAT_VALUE          0  ''
              270  BUILD_STRING_11      11 
              272  CALL_FUNCTION_1       1  ''
              274  POP_TOP          
            276_0  COME_FROM           120  '120'

 L.  52       276  LOAD_GLOBAL              print
              278  LOAD_GLOBAL              Fore
              280  LOAD_ATTR                WHITE
              282  FORMAT_VALUE          0  ''
              284  LOAD_STR                 '['
              286  LOAD_GLOBAL              Fore
              288  LOAD_ATTR                RED
              290  FORMAT_VALUE          0  ''
              292  LOAD_STR                 '!'
              294  LOAD_GLOBAL              Fore
              296  LOAD_ATTR                WHITE
              298  FORMAT_VALUE          0  ''
              300  LOAD_STR                 '] '
              302  LOAD_GLOBAL              Fore
              304  LOAD_ATTR                RED
              306  FORMAT_VALUE          0  ''
              308  LOAD_STR                 'INVALID CODE'
              310  LOAD_GLOBAL              Fore
              312  LOAD_ATTR                WHITE
              314  FORMAT_VALUE          0  ''
              316  LOAD_STR                 ' : https://discord.gift/'
              318  LOAD_FAST                'nitrocode'
              320  LOAD_ATTR                nitroCode
              322  FORMAT_VALUE          0  ''
              324  BUILD_STRING_11      11 
              326  CALL_FUNCTION_1       1  ''
              328  POP_TOP          

 L.  53       330  LOAD_FAST                'testedCodes'
              332  LOAD_CONST               1
              334  INPLACE_ADD      
              336  STORE_FAST               'testedCodes'
              338  JUMP_BACK            76  'to 76'
            340_0  COME_FROM            76  '76'
              340  JUMP_BACK            52  'to 52'
            342_0  COME_FROM            52  '52'
              342  JUMP_BACK            36  'to 36'
            344_0  COME_FROM            36  '36'

 L.  54       344  LOAD_GLOBAL              open
              346  LOAD_STR                 'testedCodes.txt'
              348  LOAD_STR                 'r+'
              350  LOAD_STR                 'utf8'
              352  LOAD_CONST               ('encoding',)
              354  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              356  SETUP_WITH          402  'to 402'
              358  STORE_FAST               'file'

 L.  55       360  LOAD_FAST                'file'
              362  LOAD_METHOD              read
              364  CALL_METHOD_0         0  ''
              366  STORE_FAST               'count'

 L.  56       368  LOAD_GLOBAL              int
              370  LOAD_FAST                'count'
              372  CALL_FUNCTION_1       1  ''
              374  LOAD_FAST                'testedCodes'
              376  BINARY_ADD       
              378  STORE_FAST               'newCount'

 L.  57       380  LOAD_FAST                'file'
              382  LOAD_METHOD              close
              384  CALL_METHOD_0         0  ''
              386  POP_TOP          
              388  POP_BLOCK        
              390  LOAD_CONST               None
              392  DUP_TOP          
              394  DUP_TOP          
              396  CALL_FUNCTION_3       3  ''
              398  POP_TOP          
              400  JUMP_FORWARD        420  'to 420'
            402_0  COME_FROM_WITH      356  '356'
              402  <49>             
          404_406  POP_JUMP_IF_TRUE    410  'to 410'
              408  <48>             
            410_0  COME_FROM           404  '404'
              410  POP_TOP          
              412  POP_TOP          
              414  POP_TOP          
              416  POP_EXCEPT       
              418  POP_TOP          
            420_0  COME_FROM           400  '400'

 L.  59       420  LOAD_GLOBAL              open
              422  LOAD_STR                 'testedCodes.txt'
              424  LOAD_STR                 'w'
              426  LOAD_STR                 'utf8'
              428  LOAD_CONST               ('encoding',)
              430  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              432  SETUP_WITH          472  'to 472'
              434  STORE_FAST               'file'

 L.  60       436  LOAD_FAST                'file'
              438  LOAD_METHOD              write
              440  LOAD_GLOBAL              str
              442  LOAD_FAST                'newCount'
              444  CALL_FUNCTION_1       1  ''
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          

 L.  61       450  LOAD_FAST                'file'
              452  LOAD_METHOD              close
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
              458  POP_BLOCK        
              460  LOAD_CONST               None
              462  DUP_TOP          
              464  DUP_TOP          
              466  CALL_FUNCTION_3       3  ''
              468  POP_TOP          
              470  JUMP_FORWARD        490  'to 490'
            472_0  COME_FROM_WITH      432  '432'
              472  <49>             
          474_476  POP_JUMP_IF_TRUE    480  'to 480'
              478  <48>             
            480_0  COME_FROM           474  '474'
              480  POP_TOP          
              482  POP_TOP          
              484  POP_TOP          
              486  POP_EXCEPT       
              488  POP_TOP          
            490_0  COME_FROM           470  '470'

 L.  62       490  LOAD_GLOBAL              testNitroCodes
              492  CALL_FUNCTION_0       0  ''
              494  POP_TOP          

Parse error at or near `DUP_TOP' instruction at offset 196


def main--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                windll
                4  LOAD_ATTR                kernel32
                6  LOAD_METHOD              SetConsoleTitleA
                8  LOAD_STR                 'Nitro generator by Kyu'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L.  66        14  LOAD_GLOBAL              print
               16  LOAD_GLOBAL              Fore
               18  LOAD_ATTR                MAGENTA
               20  FORMAT_VALUE          0  ''
               22  LOAD_STR                 '\ndP       dP    dP dP     dP          888888ba  dP d888888P  888888ba   .88888.            .88888.   88888888b 888888ba  \n88       Y8.  .8P 88     88          88    `8b 88    88     88    `8b d8\'   `8b          d8\'   `88  88        88    `8b \n88  .dP   Y8aa8P  88     88          88     88 88    88    a88aaaa8P\' 88     88          88        a88aaaa    88     88 \n88888"      88    88     88 88888888 88     88 88    88     88   `8b. 88     88 88888888 88   YP88  88        88     88 \n88  `8b.    88    Y8.   .8P          88     88 88    88     88     88 Y8.   .8P          Y8.   .88  88        88     88 \ndP   `YP    dP    `Y88888P\'          dP     dP dP    dP     dP     dP  `8888P\'            `88888\'   88888888P dP     dP \noooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo\n                                                     \n    '
               24  BUILD_STRING_2        2 
               26  CALL_FUNCTION_1       1  ''
               28  POP_TOP          

 L.  76        30  LOAD_GLOBAL              time
               32  LOAD_METHOD              perf_counter
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'finished'

 L.  77        38  LOAD_FAST                'finished'
               40  LOAD_FAST                'start'
               42  BINARY_SUBTRACT  
               44  STORE_FAST               'timeToLoad'

 L.  78        46  LOAD_GLOBAL              print
               48  LOAD_STR                 'PROGRAM CHARGÉ EN '
               50  LOAD_FAST                'timeToLoad'
               52  FORMAT_VALUE          0  ''
               54  LOAD_STR                 's...\n'
               56  BUILD_STRING_3        3 
               58  CALL_FUNCTION_1       1  ''
               60  POP_TOP          

 L.  79        62  LOAD_GLOBAL              print
               64  LOAD_STR                 '[ Threads : 1 - 200 | à partir de 25 attention cpu ]\n'
               66  CALL_FUNCTION_1       1  ''
               68  POP_TOP          

 L.  80        70  LOAD_GLOBAL              print
               72  LOAD_STR                 '[ Veux tu recevoir le code avec un webhook (Y/N) ? ]\n'
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          

 L.  81        78  LOAD_GLOBAL              str
               80  LOAD_GLOBAL              input
               82  LOAD_STR                 '-> '
               84  CALL_FUNCTION_1       1  ''
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'webhook'

 L.  82        90  LOAD_FAST                'webhook'
               92  LOAD_STR                 'Y'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   222  'to 222'

 L.  83        98  LOAD_GLOBAL              str
              100  LOAD_GLOBAL              input
              102  LOAD_STR                 'Webhook link => '
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'webhooklink'

 L.  84       110  LOAD_STR                 'https://discord.com/api/webhooks/'
              112  STORE_FAST               'webhookExample'

 L.  85       114  LOAD_FAST                'webhookExample'
              116  LOAD_FAST                'webhooklink'
              118  <118>                 0  ''
              120  POP_JUMP_IF_FALSE   184  'to 184'

 L.  86       122  LOAD_GLOBAL              open
              124  LOAD_STR                 'webhook-link.txt'
              126  LOAD_STR                 'w'
              128  CALL_FUNCTION_2       2  ''
              130  SETUP_WITH          166  'to 166'
              132  STORE_FAST               'webhookFile'

 L.  87       134  LOAD_FAST                'webhookFile'
              136  LOAD_METHOD              write
              138  LOAD_FAST                'webhooklink'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.  88       144  LOAD_FAST                'webhookFile'
              146  LOAD_METHOD              close
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          
              152  POP_BLOCK        
              154  LOAD_CONST               None
              156  DUP_TOP          
              158  DUP_TOP          
              160  CALL_FUNCTION_3       3  ''
              162  POP_TOP          
              164  JUMP_FORWARD        220  'to 220'
            166_0  COME_FROM_WITH      130  '130'
              166  <49>             
              168  POP_JUMP_IF_TRUE    172  'to 172'
              170  <48>             
            172_0  COME_FROM           168  '168'
              172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          
              178  POP_EXCEPT       
              180  POP_TOP          
              182  JUMP_FORWARD        220  'to 220'
            184_0  COME_FROM           120  '120'

 L.  90       184  LOAD_GLOBAL              print
              186  LOAD_STR                 'Il y a un problème avec ton webhook.'
              188  CALL_FUNCTION_1       1  ''
              190  POP_TOP          

 L.  91       192  LOAD_GLOBAL              time
              194  LOAD_METHOD              sleep
              196  LOAD_CONST               1
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L.  92       202  LOAD_GLOBAL              os
              204  LOAD_METHOD              system
              206  LOAD_STR                 'cls'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          

 L.  93       212  LOAD_GLOBAL              main
              214  LOAD_FAST                'start'
              216  CALL_FUNCTION_1       1  ''
              218  POP_TOP          
            220_0  COME_FROM           182  '182'
            220_1  COME_FROM           164  '164'
              220  JUMP_FORWARD        340  'to 340'
            222_0  COME_FROM            96  '96'

 L.  94       222  LOAD_FAST                'webhook'
              224  LOAD_STR                 'N'
              226  COMPARE_OP               ==
          228_230  POP_JUMP_IF_FALSE   296  'to 296'

 L.  95       232  LOAD_GLOBAL              open
              234  LOAD_STR                 'webhook-link.txt'
              236  LOAD_STR                 'w'
              238  CALL_FUNCTION_2       2  ''
              240  SETUP_WITH          276  'to 276'
              242  STORE_FAST               'webhookFile'

 L.  96       244  LOAD_FAST                'webhookFile'
              246  LOAD_METHOD              write
              248  LOAD_STR                 'None'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L.  97       254  LOAD_FAST                'webhookFile'
              256  LOAD_METHOD              close
              258  CALL_METHOD_0         0  ''
              260  POP_TOP          
              262  POP_BLOCK        
              264  LOAD_CONST               None
              266  DUP_TOP          
              268  DUP_TOP          
              270  CALL_FUNCTION_3       3  ''
              272  POP_TOP          
              274  JUMP_FORWARD        294  'to 294'
            276_0  COME_FROM_WITH      240  '240'
              276  <49>             
          278_280  POP_JUMP_IF_TRUE    284  'to 284'
              282  <48>             
            284_0  COME_FROM           278  '278'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          
              290  POP_EXCEPT       
              292  POP_TOP          
            294_0  COME_FROM           274  '274'
              294  JUMP_FORWARD        340  'to 340'
            296_0  COME_FROM           228  '228'

 L.  99       296  LOAD_GLOBAL              print
              298  LOAD_GLOBAL              Fore
              300  LOAD_ATTR                RED
              302  FORMAT_VALUE          0  ''
              304  LOAD_STR                 '[!] Ta demande est invalide !'
              306  BUILD_STRING_2        2 
              308  CALL_FUNCTION_1       1  ''
              310  POP_TOP          

 L. 100       312  LOAD_GLOBAL              time
              314  LOAD_METHOD              sleep
              316  LOAD_CONST               1
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          

 L. 101       322  LOAD_GLOBAL              os
              324  LOAD_METHOD              system
              326  LOAD_STR                 'cls'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 102       332  LOAD_GLOBAL              main
              334  LOAD_FAST                'start'
              336  CALL_FUNCTION_1       1  ''
              338  POP_TOP          
            340_0  COME_FROM           294  '294'
            340_1  COME_FROM           220  '220'

 L. 104       340  SETUP_FINALLY       450  'to 450'

 L. 105       342  LOAD_GLOBAL              int
              344  LOAD_GLOBAL              input
              346  LOAD_STR                 'Threads => '
              348  CALL_FUNCTION_1       1  ''
              350  CALL_FUNCTION_1       1  ''
              352  STORE_FAST               'threads'

 L. 106       354  LOAD_FAST                'threads'
              356  LOAD_CONST               200
              358  COMPARE_OP               <=
          360_362  POP_JUMP_IF_FALSE   402  'to 402'

 L. 107       364  LOAD_GLOBAL              range
              366  LOAD_FAST                'threads'
              368  CALL_FUNCTION_1       1  ''
              370  GET_ITER         
            372_0  COME_FROM           396  '396'
              372  FOR_ITER            400  'to 400'
              374  STORE_FAST               'i'

 L. 108       376  LOAD_GLOBAL              threading
              378  LOAD_ATTR                Thread
              380  LOAD_GLOBAL              testNitroCodes
              382  LOAD_CONST               ('target',)
              384  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              386  STORE_FAST               'thread'

 L. 109       388  LOAD_FAST                'thread'
              390  LOAD_METHOD              start
              392  CALL_METHOD_0         0  ''
              394  POP_TOP          
          396_398  JUMP_BACK           372  'to 372'
            400_0  COME_FROM           372  '372'
              400  JUMP_FORWARD        446  'to 446'
            402_0  COME_FROM           360  '360'

 L. 111       402  LOAD_GLOBAL              print
              404  LOAD_GLOBAL              Fore
              406  LOAD_ATTR                RED
              408  FORMAT_VALUE          0  ''
              410  LOAD_STR                 '[!] Ta demande est invalide !'
              412  BUILD_STRING_2        2 
              414  CALL_FUNCTION_1       1  ''
              416  POP_TOP          

 L. 112       418  LOAD_GLOBAL              time
              420  LOAD_METHOD              sleep
              422  LOAD_CONST               1
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          

 L. 113       428  LOAD_GLOBAL              os
              430  LOAD_METHOD              system
              432  LOAD_STR                 'cls'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          

 L. 114       438  LOAD_GLOBAL              main
              440  LOAD_FAST                'start'
              442  CALL_FUNCTION_1       1  ''
              444  POP_TOP          
            446_0  COME_FROM           400  '400'
              446  POP_BLOCK        
              448  JUMP_FORWARD        488  'to 488'
            450_0  COME_FROM_FINALLY   340  '340'

 L. 115       450  DUP_TOP          
              452  LOAD_GLOBAL              ValueError
          454_456  <121>               486  ''
              458  POP_TOP          
              460  POP_TOP          
              462  POP_TOP          

 L. 116       464  LOAD_GLOBAL              os
              466  LOAD_METHOD              system
              468  LOAD_STR                 'cls'
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          

 L. 117       474  LOAD_GLOBAL              main
              476  LOAD_FAST                'start'
              478  CALL_FUNCTION_1       1  ''
              480  POP_TOP          
              482  POP_EXCEPT       
              484  JUMP_FORWARD        488  'to 488'
              486  <48>             
            488_0  COME_FROM           484  '484'
            488_1  COME_FROM           448  '448'

Parse error at or near `<118>' instruction at offset 118


main(start)