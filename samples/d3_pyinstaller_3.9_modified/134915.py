# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32ctypes\core\cffi\_authentication.py
from __future__ import absolute_import
from weakref import WeakKeyDictionary
from win32ctypes.core.compat import is_text
from ._util import ffi, check_zero, dlls
from ._nl_support import _GetACP
from ._common import _PyBytes_FromStringAndSize
ffi.cdef('\n\ntypedef struct _FILETIME {\n  DWORD dwLowDateTime;\n  DWORD dwHighDateTime;\n} FILETIME, *PFILETIME;\n\ntypedef struct _CREDENTIAL_ATTRIBUTE {\n  LPWSTR Keyword;\n  DWORD  Flags;\n  DWORD  ValueSize;\n  LPBYTE Value;\n} CREDENTIAL_ATTRIBUTE, *PCREDENTIAL_ATTRIBUTE;\n\ntypedef struct _CREDENTIAL {\n  DWORD                 Flags;\n  DWORD                 Type;\n  LPWSTR                TargetName;\n  LPWSTR                Comment;\n  FILETIME              LastWritten;\n  DWORD                 CredentialBlobSize;\n  LPBYTE                CredentialBlob;\n  DWORD                 Persist;\n  DWORD                 AttributeCount;\n  PCREDENTIAL_ATTRIBUTE Attributes;\n  LPWSTR                TargetAlias;\n  LPWSTR                UserName;\n} CREDENTIAL, *PCREDENTIAL;\n\n\nBOOL WINAPI CredReadW(\n    LPCWSTR TargetName, DWORD Type, DWORD Flags, PCREDENTIAL *Credential);\nBOOL WINAPI CredWriteW(PCREDENTIAL Credential, DWORD);\nVOID WINAPI CredFree(PVOID Buffer);\nBOOL WINAPI CredDeleteW(LPCWSTR TargetName, DWORD Type, DWORD Flags);\n\n')
_keep_alive = WeakKeyDictionary()
SUPPORTED_CREDKEYS = set(('Type', 'TargetName', 'Persist', 'UserName', 'Comment', 'CredentialBlob'))

def make_unicode(password):
    """ Convert the input string to unicode.

    """
    if is_text(password):
        return password
    code_page = _GetACP()
    return password.decode(encoding=(str(code_page)), errors='strict')


class _CREDENTIAL(object):

    def __call__(self):
        return ffi.new('PCREDENTIAL')[0]

    @classmethod
    def fromdict--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              set
                2  LOAD_FAST                'credential'
                4  LOAD_METHOD              keys
                6  CALL_METHOD_0         0  ''
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_GLOBAL              SUPPORTED_CREDKEYS
               12  BINARY_SUBTRACT  
               14  STORE_FAST               'unsupported'

 L.  83        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'unsupported'
               20  CALL_FUNCTION_1       1  ''
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L.  84        24  LOAD_GLOBAL              ValueError
               26  LOAD_STR                 'Unsupported keys: {0}'
               28  LOAD_METHOD              format
               30  LOAD_FAST                'unsupported'
               32  CALL_METHOD_1         1  ''
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            22  '22'

 L.  85        38  LOAD_FAST                'flag'
               40  LOAD_CONST               0
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L.  86        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'flag != 0 not yet supported'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'

 L.  88        54  LOAD_FAST                'cls'
               56  CALL_FUNCTION_0       0  ''
               58  STORE_FAST               'factory'

 L.  89        60  LOAD_FAST                'factory'
               62  CALL_FUNCTION_0       0  ''
               64  STORE_FAST               'c_creds'

 L.  91        66  BUILD_LIST_0          0 
               68  STORE_FAST               'values'

 L.  92        70  LOAD_GLOBAL              SUPPORTED_CREDKEYS
               72  GET_ITER         
             74_0  COME_FROM           246  '246'
             74_1  COME_FROM           190  '190'
             74_2  COME_FROM           164  '164'
             74_3  COME_FROM            84  '84'
               74  FOR_ITER            248  'to 248'
               76  STORE_FAST               'key'

 L.  93        78  LOAD_FAST                'key'
               80  LOAD_FAST                'credential'
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE_BACK    74  'to 74'

 L.  94        86  LOAD_FAST                'key'
               88  LOAD_STR                 'CredentialBlob'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   166  'to 166'

 L.  95        94  LOAD_GLOBAL              make_unicode
               96  LOAD_FAST                'credential'
               98  LOAD_STR                 'CredentialBlob'
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'blob'

 L.  96       106  LOAD_GLOBAL              ffi
              108  LOAD_METHOD              new
              110  LOAD_STR                 'wchar_t[]'
              112  LOAD_FAST                'blob'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'blob_data'

 L.  99       118  LOAD_GLOBAL              ffi
              120  LOAD_METHOD              sizeof
              122  LOAD_FAST                'blob_data'
              124  CALL_METHOD_1         1  ''
              126  LOAD_GLOBAL              ffi
              128  LOAD_METHOD              sizeof
              130  LOAD_STR                 'wchar_t'
              132  CALL_METHOD_1         1  ''
              134  BINARY_SUBTRACT  

 L.  98       136  LOAD_FAST                'c_creds'
              138  STORE_ATTR               CredentialBlobSize

 L. 100       140  LOAD_GLOBAL              ffi
              142  LOAD_METHOD              cast
              144  LOAD_STR                 'LPBYTE'
              146  LOAD_FAST                'blob_data'
              148  CALL_METHOD_2         2  ''
              150  LOAD_FAST                'c_creds'
              152  STORE_ATTR               CredentialBlob

 L. 101       154  LOAD_FAST                'values'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'blob_data'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK            74  'to 74'
            166_0  COME_FROM            92  '92'

 L. 102       166  LOAD_FAST                'key'
              168  LOAD_CONST               ('Type', 'Persist')
              170  <118>                 0  ''
              172  POP_JUMP_IF_FALSE   192  'to 192'

 L. 103       174  LOAD_GLOBAL              setattr
              176  LOAD_FAST                'c_creds'
              178  LOAD_FAST                'key'
              180  LOAD_FAST                'credential'
              182  LOAD_FAST                'key'
              184  BINARY_SUBSCR    
              186  CALL_FUNCTION_3       3  ''
              188  POP_TOP          
              190  JUMP_BACK            74  'to 74'
            192_0  COME_FROM           172  '172'

 L. 105       192  LOAD_GLOBAL              make_unicode
              194  LOAD_FAST                'credential'
              196  LOAD_FAST                'key'
              198  BINARY_SUBSCR    
              200  CALL_FUNCTION_1       1  ''
              202  STORE_FAST               'blob'

 L. 106       204  LOAD_GLOBAL              ffi
              206  LOAD_METHOD              new
              208  LOAD_STR                 'wchar_t[]'
              210  LOAD_FAST                'blob'
              212  CALL_METHOD_2         2  ''
              214  STORE_FAST               'value'

 L. 107       216  LOAD_FAST                'values'
              218  LOAD_METHOD              append
              220  LOAD_FAST                'value'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 108       226  LOAD_GLOBAL              setattr
              228  LOAD_FAST                'c_creds'
              230  LOAD_FAST                'key'
              232  LOAD_GLOBAL              ffi
              234  LOAD_METHOD              cast
              236  LOAD_STR                 'LPTSTR'
              238  LOAD_FAST                'value'
              240  CALL_METHOD_2         2  ''
              242  CALL_FUNCTION_3       3  ''
              244  POP_TOP          
              246  JUMP_BACK            74  'to 74'
            248_0  COME_FROM            74  '74'

 L. 110       248  LOAD_GLOBAL              tuple
              250  LOAD_FAST                'values'
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_GLOBAL              _keep_alive
              256  LOAD_FAST                'c_creds'
              258  STORE_SUBSCR     

 L. 111       260  LOAD_FAST                'c_creds'
              262  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 82


CREDENTIAL = _CREDENTIAL()

def PCREDENTIAL--- This code section failed: ---

 L. 118         0  LOAD_GLOBAL              ffi
                2  LOAD_METHOD              new
                4  LOAD_STR                 'PCREDENTIAL'
                6  LOAD_FAST                'value'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'
               14  LOAD_GLOBAL              ffi
               16  LOAD_ATTR                NULL
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM            12  '12'
               20  LOAD_FAST                'value'
             22_0  COME_FROM            18  '18'
               22  CALL_METHOD_2         2  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def PPCREDENTIAL--- This code section failed: ---

 L. 122         0  LOAD_GLOBAL              ffi
                2  LOAD_METHOD              new
                4  LOAD_STR                 'PCREDENTIAL*'
                6  LOAD_FAST                'value'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'
               14  LOAD_GLOBAL              ffi
               16  LOAD_ATTR                NULL
               18  JUMP_FORWARD         22  'to 22'
             20_0  COME_FROM            12  '12'
               20  LOAD_FAST                'value'
             22_0  COME_FROM            18  '18'
               22  CALL_METHOD_2         2  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def credential2dict--- This code section failed: ---

 L. 126         0  BUILD_MAP_0           0 
                2  STORE_FAST               'credentials'

 L. 127         4  LOAD_GLOBAL              SUPPORTED_CREDKEYS
                6  GET_ITER         
              8_0  COME_FROM           104  '104'
                8  FOR_ITER            106  'to 106'
               10  STORE_FAST               'key'

 L. 128        12  LOAD_FAST                'key'
               14  LOAD_STR                 'CredentialBlob'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    36  'to 36'

 L. 129        20  LOAD_GLOBAL              _PyBytes_FromStringAndSize

 L. 130        22  LOAD_FAST                'pc_creds'
               24  LOAD_ATTR                CredentialBlob
               26  LOAD_FAST                'pc_creds'
               28  LOAD_ATTR                CredentialBlobSize

 L. 129        30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'data'
               34  JUMP_FORWARD         96  'to 96'
             36_0  COME_FROM            18  '18'

 L. 131        36  LOAD_FAST                'key'
               38  LOAD_CONST               ('Type', 'Persist')
               40  <118>                 0  ''
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L. 132        44  LOAD_GLOBAL              int
               46  LOAD_GLOBAL              getattr
               48  LOAD_FAST                'pc_creds'
               50  LOAD_FAST                'key'
               52  CALL_FUNCTION_2       2  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'data'
               58  JUMP_FORWARD         96  'to 96'
             60_0  COME_FROM            42  '42'

 L. 134        60  LOAD_GLOBAL              getattr
               62  LOAD_FAST                'pc_creds'
               64  LOAD_FAST                'key'
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'string_pointer'

 L. 135        70  LOAD_FAST                'string_pointer'
               72  LOAD_GLOBAL              ffi
               74  LOAD_ATTR                NULL
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    86  'to 86'

 L. 136        80  LOAD_STR                 ''
               82  STORE_FAST               'data'
               84  JUMP_FORWARD         96  'to 96'
             86_0  COME_FROM            78  '78'

 L. 138        86  LOAD_GLOBAL              ffi
               88  LOAD_METHOD              string
               90  LOAD_FAST                'string_pointer'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'data'
             96_0  COME_FROM            84  '84'
             96_1  COME_FROM            58  '58'
             96_2  COME_FROM            34  '34'

 L. 139        96  LOAD_FAST                'data'
               98  LOAD_FAST                'credentials'
              100  LOAD_FAST                'key'
              102  STORE_SUBSCR     
              104  JUMP_BACK             8  'to 8'
            106_0  COME_FROM             8  '8'

 L. 140       106  LOAD_FAST                'credentials'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 40


def _CredRead(TargetName, Type, Flags, ppCredential):
    target = make_unicode(TargetName)
    value = check_zerodlls.advapi32.CredReadW(target, Type, Flags, ppCredential)'CredRead'
    return value


def _CredWrite(Credential, Flags):
    return check_zerodlls.advapi32.CredWriteWCredentialFlags'CredWrite'


def _CredDelete(TargetName, Type, Flags):
    return check_zerodlls.advapi32.CredDeleteW(make_unicode(TargetName), Type, Flags)'CredDelete'


_CredFree = dlls.advapi32.CredFree