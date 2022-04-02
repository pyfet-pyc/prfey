# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32ctypes\pywin32\win32api.py
""" A module, encapsulating the Windows Win32 API. """
from __future__ import absolute_import
from win32ctypes.core import _common, _dll, _resource, _system_information, _backend, _time
import win32ctypes.pywin32.pywintypes as _pywin32error
LOAD_LIBRARY_AS_DATAFILE = 2
LANG_NEUTRAL = 0

def LoadLibraryEx--- This code section failed: ---

 L.  40         0  LOAD_FAST                'handle'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     16  'to 16'

 L.  41         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'handle != 0 not supported'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  42        16  LOAD_GLOBAL              _pywin32error
               18  CALL_FUNCTION_0       0  ''
               20  SETUP_WITH           52  'to 52'
               22  POP_TOP          

 L.  43        24  LOAD_GLOBAL              _dll
               26  LOAD_METHOD              _LoadLibraryEx
               28  LOAD_FAST                'fileName'
               30  LOAD_CONST               0
               32  LOAD_FAST                'flags'
               34  CALL_METHOD_3         3  ''
               36  POP_BLOCK        
               38  ROT_TWO          
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  RETURN_VALUE     
             52_0  COME_FROM_WITH       20  '20'
               52  <49>             
               54  POP_JUMP_IF_TRUE     58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          
               64  POP_EXCEPT       
               66  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 40


def EnumResourceTypes--- This code section failed: ---

 L.  60         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'resource_types'

 L.  62         4  LOAD_CLOSURE             'resource_types'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object callback>
               10  LOAD_STR                 'EnumResourceTypes.<locals>.callback'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_FAST               'callback'

 L.  66        16  LOAD_GLOBAL              _pywin32error
               18  CALL_FUNCTION_0       0  ''
               20  SETUP_WITH           58  'to 58'
               22  POP_TOP          

 L.  67        24  LOAD_GLOBAL              _resource
               26  LOAD_METHOD              _EnumResourceTypes

 L.  68        28  LOAD_FAST                'hModule'
               30  LOAD_GLOBAL              _resource
               32  LOAD_METHOD              ENUMRESTYPEPROC
               34  LOAD_FAST                'callback'
               36  CALL_METHOD_1         1  ''
               38  LOAD_CONST               0

 L.  67        40  CALL_METHOD_3         3  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  LOAD_CONST               None
               48  DUP_TOP          
               50  DUP_TOP          
               52  CALL_FUNCTION_3       3  ''
               54  POP_TOP          
               56  JUMP_FORWARD         74  'to 74'
             58_0  COME_FROM_WITH       20  '20'
               58  <49>             
               60  POP_JUMP_IF_TRUE     64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          
               70  POP_EXCEPT       
               72  POP_TOP          
             74_0  COME_FROM            56  '56'

 L.  69        74  LOAD_DEREF               'resource_types'
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 48


def EnumResourceNames--- This code section failed: ---

 L.  89         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'resource_names'

 L.  91         4  LOAD_CLOSURE             'resource_names'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object callback>
               10  LOAD_STR                 'EnumResourceNames.<locals>.callback'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_FAST               'callback'

 L.  95        16  LOAD_GLOBAL              _pywin32error
               18  CALL_FUNCTION_0       0  ''
               20  SETUP_WITH           60  'to 60'
               22  POP_TOP          

 L.  96        24  LOAD_GLOBAL              _resource
               26  LOAD_METHOD              _EnumResourceNames

 L.  97        28  LOAD_FAST                'hModule'
               30  LOAD_FAST                'resType'
               32  LOAD_GLOBAL              _resource
               34  LOAD_METHOD              ENUMRESNAMEPROC
               36  LOAD_FAST                'callback'
               38  CALL_METHOD_1         1  ''
               40  LOAD_CONST               0

 L.  96        42  CALL_METHOD_4         4  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  LOAD_CONST               None
               50  DUP_TOP          
               52  DUP_TOP          
               54  CALL_FUNCTION_3       3  ''
               56  POP_TOP          
               58  JUMP_FORWARD         76  'to 76'
             60_0  COME_FROM_WITH       20  '20'
               60  <49>             
               62  POP_JUMP_IF_TRUE     66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          
               72  POP_EXCEPT       
               74  POP_TOP          
             76_0  COME_FROM            58  '58'

 L.  98        76  LOAD_DEREF               'resource_names'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 50


def EnumResourceLanguages--- This code section failed: ---

 L. 121         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'resource_languages'

 L. 123         4  LOAD_CLOSURE             'resource_languages'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object callback>
               10  LOAD_STR                 'EnumResourceLanguages.<locals>.callback'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_FAST               'callback'

 L. 127        16  LOAD_GLOBAL              _pywin32error
               18  CALL_FUNCTION_0       0  ''
               20  SETUP_WITH           62  'to 62'
               22  POP_TOP          

 L. 128        24  LOAD_GLOBAL              _resource
               26  LOAD_METHOD              _EnumResourceLanguages

 L. 129        28  LOAD_FAST                'hModule'
               30  LOAD_FAST                'lpType'
               32  LOAD_FAST                'lpName'
               34  LOAD_GLOBAL              _resource
               36  LOAD_METHOD              ENUMRESLANGPROC
               38  LOAD_FAST                'callback'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               0

 L. 128        44  CALL_METHOD_5         5  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  LOAD_CONST               None
               52  DUP_TOP          
               54  DUP_TOP          
               56  CALL_FUNCTION_3       3  ''
               58  POP_TOP          
               60  JUMP_FORWARD         78  'to 78'
             62_0  COME_FROM_WITH       20  '20'
               62  <49>             
               64  POP_JUMP_IF_TRUE     68  'to 68'
               66  <48>             
             68_0  COME_FROM            64  '64'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          
               74  POP_EXCEPT       
               76  POP_TOP          
             78_0  COME_FROM            60  '60'

 L. 130        78  LOAD_DEREF               'resource_languages'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 52


def LoadResource--- This code section failed: ---

 L. 157         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH          114  'to 114'
                6  POP_TOP          

 L. 158         8  LOAD_GLOBAL              _resource
               10  LOAD_METHOD              _FindResourceEx
               12  LOAD_FAST                'hModule'
               14  LOAD_FAST                'type'
               16  LOAD_FAST                'name'
               18  LOAD_FAST                'language'
               20  CALL_METHOD_4         4  ''
               22  STORE_FAST               'hrsrc'

 L. 159        24  LOAD_GLOBAL              _resource
               26  LOAD_METHOD              _SizeofResource
               28  LOAD_FAST                'hModule'
               30  LOAD_FAST                'hrsrc'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'size'

 L. 160        36  LOAD_GLOBAL              _resource
               38  LOAD_METHOD              _LoadResource
               40  LOAD_FAST                'hModule'
               42  LOAD_FAST                'hrsrc'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'hglob'

 L. 161        48  LOAD_GLOBAL              _backend
               50  LOAD_STR                 'ctypes'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L. 162        56  LOAD_GLOBAL              _common
               58  LOAD_METHOD              cast

 L. 163        60  LOAD_GLOBAL              _resource
               62  LOAD_METHOD              _LockResource
               64  LOAD_FAST                'hglob'
               66  CALL_METHOD_1         1  ''
               68  LOAD_GLOBAL              _common
               70  LOAD_ATTR                c_char_p

 L. 162        72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'pointer'
               76  JUMP_FORWARD         88  'to 88'
             78_0  COME_FROM            54  '54'

 L. 165        78  LOAD_GLOBAL              _resource
               80  LOAD_METHOD              _LockResource
               82  LOAD_FAST                'hglob'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'pointer'
             88_0  COME_FROM            76  '76'

 L. 166        88  LOAD_GLOBAL              _common
               90  LOAD_METHOD              _PyBytes_FromStringAndSize
               92  LOAD_FAST                'pointer'
               94  LOAD_FAST                'size'
               96  CALL_METHOD_2         2  ''
               98  POP_BLOCK        
              100  ROT_TWO          
              102  LOAD_CONST               None
              104  DUP_TOP          
              106  DUP_TOP          
              108  CALL_FUNCTION_3       3  ''
              110  POP_TOP          
              112  RETURN_VALUE     
            114_0  COME_FROM_WITH        4  '4'
              114  <49>             
              116  POP_JUMP_IF_TRUE    120  'to 120'
              118  <48>             
            120_0  COME_FROM           116  '116'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          
              126  POP_EXCEPT       
              128  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 102


def FreeLibrary--- This code section failed: ---

 L. 180         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           32  'to 32'
                6  POP_TOP          

 L. 181         8  LOAD_GLOBAL              _dll
               10  LOAD_METHOD              _FreeLibrary
               12  LOAD_FAST                'hModule'
               14  CALL_METHOD_1         1  ''
               16  POP_BLOCK        
               18  ROT_TWO          
               20  LOAD_CONST               None
               22  DUP_TOP          
               24  DUP_TOP          
               26  CALL_FUNCTION_3       3  ''
               28  POP_TOP          
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        4  '4'
               32  <49>             
               34  POP_JUMP_IF_TRUE     38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          
               44  POP_EXCEPT       
               46  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 20


def GetTickCount():
    """ The number of milliseconds that have elapsed since startup

    Returns
    -------
    counts : int
        The millisecond counts since system startup.
    """
    return _time._GetTickCount()


def BeginUpdateResource--- This code section failed: ---

 L. 211         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 212         8  LOAD_GLOBAL              _resource
               10  LOAD_METHOD              _BeginUpdateResource
               12  LOAD_FAST                'filename'
               14  LOAD_FAST                'delete'
               16  CALL_METHOD_2         2  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 22


def EndUpdateResource--- This code section failed: ---

 L. 228         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 229         8  LOAD_GLOBAL              _resource
               10  LOAD_METHOD              _EndUpdateResource
               12  LOAD_FAST                'handle'
               14  LOAD_FAST                'discard'
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  JUMP_FORWARD         50  'to 50'
             34_0  COME_FROM_WITH        4  '4'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          
             50_0  COME_FROM            32  '32'

Parse error at or near `DUP_TOP' instruction at offset 24


def UpdateResource--- This code section failed: ---

 L. 262         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           86  'to 86'
                6  POP_TOP          

 L. 263         8  SETUP_FINALLY        22  'to 22'

 L. 264        10  LOAD_GLOBAL              bytes
               12  LOAD_FAST                'data'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'lp_data'
               18  POP_BLOCK        
               20  JUMP_FORWARD         48  'to 48'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 265        22  DUP_TOP          
               24  LOAD_GLOBAL              UnicodeEncodeError
               26  <121>                46  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 266        34  LOAD_GLOBAL              TypeError

 L. 267        36  LOAD_STR                 "a bytes-like object is required, not a 'unicode'"

 L. 266        38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            20  '20'

 L. 268        48  LOAD_GLOBAL              _resource
               50  LOAD_METHOD              _UpdateResource

 L. 269        52  LOAD_FAST                'handle'
               54  LOAD_FAST                'type'
               56  LOAD_FAST                'name'
               58  LOAD_FAST                'language'
               60  LOAD_FAST                'lp_data'
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'lp_data'
               66  CALL_FUNCTION_1       1  ''

 L. 268        68  CALL_METHOD_6         6  ''
               70  POP_TOP          
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH        4  '4'
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

Parse error at or near `<121>' instruction at offset 26


def GetWindowsDirectory--- This code section failed: ---

 L. 281         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 283         8  LOAD_GLOBAL              str
               10  LOAD_GLOBAL              _system_information
               12  LOAD_METHOD              _GetWindowsDirectory
               14  CALL_METHOD_0         0  ''
               16  CALL_FUNCTION_1       1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 22


def GetSystemDirectory--- This code section failed: ---

 L. 295         0  LOAD_GLOBAL              _pywin32error
                2  CALL_FUNCTION_0       0  ''
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 297         8  LOAD_GLOBAL              str
               10  LOAD_GLOBAL              _system_information
               12  LOAD_METHOD              _GetSystemDirectory
               14  CALL_METHOD_0         0  ''
               16  CALL_FUNCTION_1       1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  LOAD_CONST               None
               24  DUP_TOP          
               26  DUP_TOP          
               28  CALL_FUNCTION_3       3  ''
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  <49>             
               36  POP_JUMP_IF_TRUE     40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          
               46  POP_EXCEPT       
               48  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 22