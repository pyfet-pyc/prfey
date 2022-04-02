# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyring\backends\macOS\api.py
import contextlib, ctypes, struct
from ctypes import c_void_p, c_uint16, c_uint32, c_int32, c_char_p, POINTER
sec_keychain_ref = sec_keychain_item_ref = c_void_p
OS_status = c_int32

class error:
    item_not_found = -25300
    keychain_denied = -128
    sec_auth_failed = -25293
    plist_missing = -67030


fw = '/System/Library/Frameworks/{name}.framework/Versions/A/{name}'.format
_sec = ctypes.CDLL(fw(name='Security'))
_core = ctypes.CDLL(fw(name='CoreServices'))
SecKeychainOpen = _sec.SecKeychainOpen
SecKeychainOpen.argtypes = (c_char_p, POINTER(sec_keychain_ref))
SecKeychainOpen.restype = OS_status
SecKeychainCopyDefault = _sec.SecKeychainCopyDefault
SecKeychainCopyDefault.argtypes = (POINTER(sec_keychain_ref),)
SecKeychainCopyDefault.restype = OS_status

class Error(Exception):

    @classmethod
    def raise_for_status(cls, status):
        if status == 0:
            return
        if status == error.item_not_found:
            raise NotFound(status, 'Item not found')
        if status == error.keychain_denied:
            raise KeychainDenied(status, 'Keychain Access Denied')
        if status == error.sec_auth_failed or status == error.plist_missing:
            raise SecAuthFailure(status, 'Security Auth Failure: make sure python is signed with codesign util')
        raise cls(status, 'Unknown Error')


class NotFound(Error):
    pass


class KeychainDenied(Error):
    pass


class SecAuthFailure(Error):
    pass


@contextlib.contextmanager
def open--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              sec_keychain_ref
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'ref'

 L.  66         6  LOAD_FAST                'name'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L.  67        14  LOAD_GLOBAL              SecKeychainCopyDefault
               16  LOAD_FAST                'ref'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'status'
               22  JUMP_FORWARD         40  'to 40'
             24_0  COME_FROM            12  '12'

 L.  69        24  LOAD_GLOBAL              SecKeychainOpen
               26  LOAD_FAST                'name'
               28  LOAD_METHOD              encode
               30  LOAD_STR                 'utf-8'
               32  CALL_METHOD_1         1  ''
               34  LOAD_FAST                'ref'
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'status'
             40_0  COME_FROM            22  '22'

 L.  70        40  LOAD_GLOBAL              Error
               42  LOAD_METHOD              raise_for_status
               44  LOAD_FAST                'status'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L.  71        50  SETUP_FINALLY        72  'to 72'

 L.  72        52  LOAD_FAST                'ref'
               54  YIELD_VALUE      
               56  POP_TOP          
               58  POP_BLOCK        

 L.  74        60  LOAD_GLOBAL              _core
               62  LOAD_METHOD              CFRelease
               64  LOAD_FAST                'ref'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_FORWARD         84  'to 84'
             72_0  COME_FROM_FINALLY    50  '50'
               72  LOAD_GLOBAL              _core
               74  LOAD_METHOD              CFRelease
               76  LOAD_FAST                'ref'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  <48>             
             84_0  COME_FROM            70  '70'

Parse error at or near `<117>' instruction at offset 10


SecKeychainFindGenericPassword = _sec.SecKeychainFindGenericPassword
SecKeychainFindGenericPassword.argtypes = (
 sec_keychain_ref,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 POINTER(c_uint32),
 POINTER(c_void_p),
 POINTER(sec_keychain_item_ref))
SecKeychainFindGenericPassword.restype = OS_status

def find_generic_password--- This code section failed: ---

 L.  92         0  LOAD_FAST                'username'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'username'

 L.  93        10  LOAD_FAST                'service'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'service'

 L.  94        20  LOAD_GLOBAL              open
               22  LOAD_FAST                'kc_name'
               24  CALL_FUNCTION_1       1  ''
               26  SETUP_WITH           86  'to 86'
               28  STORE_FAST               'keychain'

 L.  95        30  LOAD_GLOBAL              c_uint32
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'length'

 L.  96        36  LOAD_GLOBAL              c_void_p
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'data'

 L.  97        42  LOAD_GLOBAL              SecKeychainFindGenericPassword

 L.  98        44  LOAD_FAST                'keychain'
               46  LOAD_GLOBAL              len
               48  LOAD_FAST                'service'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'service'
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'username'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'username'
               62  LOAD_FAST                'length'
               64  LOAD_FAST                'data'
               66  LOAD_CONST               None

 L.  97        68  CALL_FUNCTION_8       8  ''
               70  STORE_FAST               'status'
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH       26  '26'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L. 101       102  LOAD_GLOBAL              Error
              104  LOAD_METHOD              raise_for_status
              106  LOAD_FAST                'status'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 103       112  LOAD_GLOBAL              ctypes
              114  LOAD_METHOD              create_string_buffer
              116  LOAD_FAST                'length'
              118  LOAD_ATTR                value
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'password'

 L. 104       124  LOAD_GLOBAL              ctypes
              126  LOAD_METHOD              memmove
              128  LOAD_FAST                'password'
              130  LOAD_FAST                'data'
              132  LOAD_ATTR                value
              134  LOAD_FAST                'length'
              136  LOAD_ATTR                value
              138  CALL_METHOD_3         3  ''
              140  POP_TOP          

 L. 105       142  LOAD_GLOBAL              SecKeychainItemFreeContent
              144  LOAD_CONST               None
              146  LOAD_FAST                'data'
              148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          

 L. 106       152  LOAD_FAST                'password'
              154  LOAD_ATTR                raw
              156  LOAD_METHOD              decode
              158  LOAD_STR                 'utf-8'
              160  CALL_METHOD_1         1  ''
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 76


SecKeychainFindInternetPassword = _sec.SecKeychainFindInternetPassword
SecKeychainFindInternetPassword.argtypes = (
 sec_keychain_ref,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint16,
 c_uint32,
 c_uint32,
 POINTER(c_uint32),
 POINTER(c_void_p),
 POINTER(sec_keychain_item_ref))
SecKeychainFindInternetPassword.restype = OS_status

class PackedAttributes(type):
    __doc__ = '\n    Take the attributes which use magic words\n    to represent enumerated constants and generate\n    the constants.\n    '

    def __new__(cls, name, bases, dict):
        dict.update(((
         key, cls.unpack(val)) for key, val in dict.items() if not key.startswith('_')))
        return super.__new__(cls, name, bases, dict)

    @staticmethod
    def unpack(word):
        r"""
        >>> PackedAttributes.unpack(0)
        0
        >>> PackedAttributes.unpack('\x00\x00\x00\x01')
        1
        >>> PackedAttributes.unpack('abcd')
        1633837924
        """
        if not isinstance(word, str):
            return word
        val, = struct.unpack('!I', word.encode('ascii'))
        return val


class SecProtocolType(metaclass=PackedAttributes):
    kSecProtocolTypeHTTP = 'http'
    kSecProtocolTypeHTTPS = 'htps'
    kSecProtocolTypeFTP = 'ftp '


class SecAuthenticationType(metaclass=PackedAttributes):
    __doc__ = '\n    >>> SecAuthenticationType.kSecAuthenticationTypeDefault\n    1684434036\n    '
    kSecAuthenticationTypeDefault = 'dflt'
    kSecAuthenticationTypeAny = 0


def find_internet_password--- This code section failed: ---

 L. 178         0  LOAD_FAST                'username'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'username'

 L. 179        10  LOAD_CONST               None
               12  STORE_FAST               'domain'

 L. 180        14  LOAD_FAST                'service'
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'utf-8'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'service'

 L. 181        24  LOAD_CONST               None
               26  STORE_FAST               'path'

 L. 182        28  LOAD_CONST               0
               30  STORE_FAST               'port'

 L. 184        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'kc_name'
               36  CALL_FUNCTION_1       1  ''
               38  SETUP_WITH          116  'to 116'
               40  STORE_FAST               'keychain'

 L. 185        42  LOAD_GLOBAL              c_uint32
               44  CALL_FUNCTION_0       0  ''
               46  STORE_FAST               'length'

 L. 186        48  LOAD_GLOBAL              c_void_p
               50  CALL_FUNCTION_0       0  ''
               52  STORE_FAST               'data'

 L. 187        54  LOAD_GLOBAL              SecKeychainFindInternetPassword

 L. 188        56  LOAD_FAST                'keychain'

 L. 189        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'service'
               62  CALL_FUNCTION_1       1  ''

 L. 190        64  LOAD_FAST                'service'

 L. 191        66  LOAD_CONST               0

 L. 192        68  LOAD_FAST                'domain'

 L. 193        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'username'
               74  CALL_FUNCTION_1       1  ''

 L. 194        76  LOAD_FAST                'username'

 L. 195        78  LOAD_CONST               0

 L. 196        80  LOAD_FAST                'path'

 L. 197        82  LOAD_FAST                'port'

 L. 198        84  LOAD_GLOBAL              SecProtocolType
               86  LOAD_ATTR                kSecProtocolTypeHTTPS

 L. 199        88  LOAD_GLOBAL              SecAuthenticationType
               90  LOAD_ATTR                kSecAuthenticationTypeAny

 L. 200        92  LOAD_FAST                'length'

 L. 201        94  LOAD_FAST                'data'

 L. 202        96  LOAD_CONST               None

 L. 187        98  CALL_FUNCTION_15     15  ''
              100  STORE_FAST               'status'
              102  POP_BLOCK        
              104  LOAD_CONST               None
              106  DUP_TOP          
              108  DUP_TOP          
              110  CALL_FUNCTION_3       3  ''
              112  POP_TOP          
              114  JUMP_FORWARD        132  'to 132'
            116_0  COME_FROM_WITH       38  '38'
              116  <49>             
              118  POP_JUMP_IF_TRUE    122  'to 122'
              120  <48>             
            122_0  COME_FROM           118  '118'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          
              128  POP_EXCEPT       
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L. 205       132  LOAD_GLOBAL              Error
              134  LOAD_METHOD              raise_for_status
              136  LOAD_FAST                'status'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 207       142  LOAD_GLOBAL              ctypes
              144  LOAD_METHOD              create_string_buffer
              146  LOAD_FAST                'length'
              148  LOAD_ATTR                value
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'password'

 L. 208       154  LOAD_GLOBAL              ctypes
              156  LOAD_METHOD              memmove
              158  LOAD_FAST                'password'
              160  LOAD_FAST                'data'
              162  LOAD_ATTR                value
              164  LOAD_FAST                'length'
              166  LOAD_ATTR                value
              168  CALL_METHOD_3         3  ''
              170  POP_TOP          

 L. 209       172  LOAD_GLOBAL              SecKeychainItemFreeContent
              174  LOAD_CONST               None
              176  LOAD_FAST                'data'
              178  CALL_FUNCTION_2       2  ''
              180  POP_TOP          

 L. 210       182  LOAD_FAST                'password'
              184  LOAD_ATTR                raw
              186  LOAD_METHOD              decode
              188  LOAD_STR                 'utf-8'
              190  CALL_METHOD_1         1  ''
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 106


SecKeychainAddGenericPassword = _sec.SecKeychainAddGenericPassword
SecKeychainAddGenericPassword.argtypes = (
 sec_keychain_ref,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 POINTER(sec_keychain_item_ref))
SecKeychainAddGenericPassword.restype = OS_status

def set_generic_password--- This code section failed: ---

 L. 228         0  LOAD_FAST                'username'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'username'

 L. 229        10  LOAD_FAST                'service'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'service'

 L. 230        20  LOAD_FAST                'password'
               22  LOAD_METHOD              encode
               24  LOAD_STR                 'utf-8'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'password'

 L. 231        30  LOAD_GLOBAL              open
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_1       1  ''
               36  SETUP_WITH          178  'to 178'
               38  STORE_FAST               'keychain'

 L. 232        40  LOAD_GLOBAL              sec_keychain_item_ref
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'item'

 L. 233        46  LOAD_GLOBAL              SecKeychainFindGenericPassword

 L. 234        48  LOAD_FAST                'keychain'
               50  LOAD_GLOBAL              len
               52  LOAD_FAST                'service'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_FAST                'service'
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'username'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'username'
               66  LOAD_CONST               None
               68  LOAD_CONST               None
               70  LOAD_FAST                'item'

 L. 233        72  CALL_FUNCTION_8       8  ''
               74  STORE_FAST               'status'

 L. 236        76  LOAD_FAST                'status'
               78  POP_JUMP_IF_FALSE   126  'to 126'

 L. 237        80  LOAD_FAST                'status'
               82  LOAD_GLOBAL              error
               84  LOAD_ATTR                item_not_found
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   154  'to 154'

 L. 238        90  LOAD_GLOBAL              SecKeychainAddGenericPassword

 L. 239        92  LOAD_FAST                'keychain'

 L. 240        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'service'
               98  CALL_FUNCTION_1       1  ''

 L. 241       100  LOAD_FAST                'service'

 L. 242       102  LOAD_GLOBAL              len
              104  LOAD_FAST                'username'
              106  CALL_FUNCTION_1       1  ''

 L. 243       108  LOAD_FAST                'username'

 L. 244       110  LOAD_GLOBAL              len
              112  LOAD_FAST                'password'
              114  CALL_FUNCTION_1       1  ''

 L. 245       116  LOAD_FAST                'password'

 L. 246       118  LOAD_CONST               None

 L. 238       120  CALL_FUNCTION_8       8  ''
              122  STORE_FAST               'status'
              124  JUMP_FORWARD        154  'to 154'
            126_0  COME_FROM            78  '78'

 L. 249       126  LOAD_GLOBAL              SecKeychainItemModifyAttributesAndData

 L. 250       128  LOAD_FAST                'item'
              130  LOAD_CONST               None
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'password'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_FAST                'password'

 L. 249       140  CALL_FUNCTION_4       4  ''
              142  STORE_FAST               'status'

 L. 252       144  LOAD_GLOBAL              _core
              146  LOAD_METHOD              CFRelease
              148  LOAD_FAST                'item'
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
            154_0  COME_FROM           124  '124'
            154_1  COME_FROM            88  '88'

 L. 254       154  LOAD_GLOBAL              Error
              156  LOAD_METHOD              raise_for_status
              158  LOAD_FAST                'status'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  POP_BLOCK        
              166  LOAD_CONST               None
              168  DUP_TOP          
              170  DUP_TOP          
              172  CALL_FUNCTION_3       3  ''
              174  POP_TOP          
              176  JUMP_FORWARD        194  'to 194'
            178_0  COME_FROM_WITH       36  '36'
              178  <49>             
              180  POP_JUMP_IF_TRUE    184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
              184  POP_TOP          
              186  POP_TOP          
              188  POP_TOP          
              190  POP_EXCEPT       
              192  POP_TOP          
            194_0  COME_FROM           176  '176'

Parse error at or near `DUP_TOP' instruction at offset 168


SecKeychainAddInternetPassword = _sec.SecKeychainAddInternetPassword
SecKeychainAddInternetPassword.argtypes = (
 sec_keychain_ref,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint32,
 c_char_p,
 c_uint16,
 c_uint32,
 c_uint32,
 c_uint32,
 c_void_p,
 POINTER(sec_keychain_item_ref))
SecKeychainAddInternetPassword.restype = OS_status

def set_internet_password--- This code section failed: ---

 L. 279         0  LOAD_FAST                'username'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'username'

 L. 280        10  LOAD_CONST               None
               12  STORE_FAST               'domain'

 L. 281        14  LOAD_FAST                'service'
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'utf-8'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'service'

 L. 282        24  LOAD_FAST                'password'
               26  LOAD_METHOD              encode
               28  LOAD_STR                 'utf-8'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'password'

 L. 283        34  LOAD_CONST               None
               36  STORE_FAST               'path'

 L. 284        38  LOAD_CONST               0
               40  STORE_FAST               'port'

 L. 285        42  LOAD_GLOBAL              open
               44  LOAD_FAST                'name'
               46  CALL_FUNCTION_1       1  ''
               48  SETUP_WITH          128  'to 128'
               50  STORE_FAST               'keychain'

 L. 287        52  LOAD_GLOBAL              SecKeychainAddInternetPassword

 L. 288        54  LOAD_FAST                'keychain'

 L. 289        56  LOAD_GLOBAL              len
               58  LOAD_FAST                'service'
               60  CALL_FUNCTION_1       1  ''

 L. 290        62  LOAD_FAST                'service'

 L. 291        64  LOAD_CONST               0

 L. 292        66  LOAD_FAST                'domain'

 L. 293        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'username'
               72  CALL_FUNCTION_1       1  ''

 L. 294        74  LOAD_FAST                'username'

 L. 295        76  LOAD_CONST               0

 L. 296        78  LOAD_FAST                'path'

 L. 297        80  LOAD_FAST                'port'

 L. 298        82  LOAD_GLOBAL              SecProtocolType
               84  LOAD_ATTR                kSecProtocolTypeHTTPS

 L. 299        86  LOAD_GLOBAL              SecAuthenticationType
               88  LOAD_ATTR                kSecAuthenticationTypeAny

 L. 300        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'password'
               94  CALL_FUNCTION_1       1  ''

 L. 301        96  LOAD_FAST                'password'

 L. 302        98  LOAD_CONST               None

 L. 287       100  CALL_FUNCTION_15     15  ''
              102  STORE_FAST               'status'

 L. 305       104  LOAD_GLOBAL              Error
              106  LOAD_METHOD              raise_for_status
              108  LOAD_FAST                'status'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
              114  POP_BLOCK        
              116  LOAD_CONST               None
              118  DUP_TOP          
              120  DUP_TOP          
              122  CALL_FUNCTION_3       3  ''
              124  POP_TOP          
              126  JUMP_FORWARD        144  'to 144'
            128_0  COME_FROM_WITH       48  '48'
              128  <49>             
              130  POP_JUMP_IF_TRUE    134  'to 134'
              132  <48>             
            134_0  COME_FROM           130  '130'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          
              140  POP_EXCEPT       
              142  POP_TOP          
            144_0  COME_FROM           126  '126'

Parse error at or near `DUP_TOP' instruction at offset 118


SecKeychainItemModifyAttributesAndData = _sec.SecKeychainItemModifyAttributesAndData
SecKeychainItemModifyAttributesAndData.argtypes = (
 sec_keychain_item_ref,
 c_void_p,
 c_uint32,
 c_void_p)
SecKeychainItemModifyAttributesAndData.restype = OS_status
SecKeychainItemFreeContent = _sec.SecKeychainItemFreeContent
SecKeychainItemFreeContent.argtypes = (c_void_p, c_void_p)
SecKeychainItemFreeContent.restype = OS_status
SecKeychainItemDelete = _sec.SecKeychainItemDelete
SecKeychainItemDelete.argtypes = (sec_keychain_item_ref,)
SecKeychainItemDelete.restype = OS_status

def delete_generic_password--- This code section failed: ---

 L. 327         0  LOAD_FAST                'username'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'username'

 L. 328        10  LOAD_FAST                'service'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'service'

 L. 329        20  LOAD_GLOBAL              open
               22  LOAD_FAST                'name'
               24  CALL_FUNCTION_1       1  ''
               26  SETUP_WITH           92  'to 92'
               28  STORE_FAST               'keychain'

 L. 330        30  LOAD_GLOBAL              c_uint32
               32  CALL_FUNCTION_0       0  ''
               34  STORE_FAST               'length'

 L. 331        36  LOAD_GLOBAL              c_void_p
               38  CALL_FUNCTION_0       0  ''
               40  STORE_FAST               'data'

 L. 332        42  LOAD_GLOBAL              sec_keychain_item_ref
               44  CALL_FUNCTION_0       0  ''
               46  STORE_FAST               'item'

 L. 333        48  LOAD_GLOBAL              SecKeychainFindGenericPassword

 L. 334        50  LOAD_FAST                'keychain'
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'service'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_FAST                'service'
               60  LOAD_GLOBAL              len
               62  LOAD_FAST                'username'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_FAST                'username'
               68  LOAD_FAST                'length'
               70  LOAD_FAST                'data'
               72  LOAD_FAST                'item'

 L. 333        74  CALL_FUNCTION_8       8  ''
               76  STORE_FAST               'status'
               78  POP_BLOCK        
               80  LOAD_CONST               None
               82  DUP_TOP          
               84  DUP_TOP          
               86  CALL_FUNCTION_3       3  ''
               88  POP_TOP          
               90  JUMP_FORWARD        108  'to 108'
             92_0  COME_FROM_WITH       26  '26'
               92  <49>             
               94  POP_JUMP_IF_TRUE     98  'to 98'
               96  <48>             
             98_0  COME_FROM            94  '94'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          
              104  POP_EXCEPT       
              106  POP_TOP          
            108_0  COME_FROM            90  '90'

 L. 337       108  LOAD_GLOBAL              Error
              110  LOAD_METHOD              raise_for_status
              112  LOAD_FAST                'status'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 339       118  LOAD_GLOBAL              SecKeychainItemDelete
              120  LOAD_FAST                'item'
              122  CALL_FUNCTION_1       1  ''
              124  POP_TOP          

 L. 340       126  LOAD_GLOBAL              _core
              128  LOAD_METHOD              CFRelease
              130  LOAD_FAST                'item'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          

Parse error at or near `DUP_TOP' instruction at offset 82