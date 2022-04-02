# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\client\selecttlb.py
"""Utilities for selecting and enumerating the Type Libraries installed on the system
"""
import win32api, win32con, pythoncom

class TypelibSpec:

    def __init__(self, clsid, lcid, major, minor, flags=0):
        self.clsid = str(clsid)
        self.lcid = int(lcid)
        self.major = major
        self.minor = minor
        self.dll = None
        self.desc = None
        self.ver_desc = None
        self.flags = flags

    def __getitem__(self, item):
        if item == 0:
            return self.ver_desc
        raise IndexError('Cant index me!')

    def __lt__(self, other):
        me = (
         (self.ver_desc or '').lower(), (self.desc or '').lower(), self.major, self.minor)
        them = ((other.ver_desc or '').lower(), (other.desc or '').lower(), other.major, other.minor)
        return me < them

    def __eq__(self, other):
        return (self.ver_desc or '').lower() == (other.ver_desc or '').lower() and (self.desc or '').lower() == (other.desc or '').lower() and self.major == other.major and self.minor == other.minor

    def Resolve--- This code section failed: ---

 L.  38         0  LOAD_FAST                'self'
                2  LOAD_ATTR                dll
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  39        10  LOAD_CONST               0
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  40        14  LOAD_GLOBAL              pythoncom
               16  LOAD_METHOD              LoadTypeLib
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                dll
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'tlb'

 L.  41        26  LOAD_FAST                'self'
               28  LOAD_METHOD              FromTypelib
               30  LOAD_FAST                'tlb'
               32  LOAD_CONST               None
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          

 L.  42        38  LOAD_CONST               1
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def FromTypelib(self, typelib, dllName=None):
        la = typelib.GetLibAttr()
        self.clsid = str(la[0])
        self.lcid = la[1]
        self.major = la[3]
        self.minor = la[4]
        if dllName:
            self.dll = dllName


def EnumKeys--- This code section failed: ---

 L.  54         0  LOAD_CONST               0
                2  STORE_FAST               'index'

 L.  55         4  BUILD_LIST_0          0 
                6  STORE_FAST               'ret'
              8_0  COME_FROM           114  '114'

 L.  57         8  SETUP_FINALLY        26  'to 26'

 L.  58        10  LOAD_GLOBAL              win32api
               12  LOAD_METHOD              RegEnumKey
               14  LOAD_FAST                'root'
               16  LOAD_FAST                'index'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'item'
               22  POP_BLOCK        
               24  JUMP_FORWARD         50  'to 50'
             26_0  COME_FROM_FINALLY     8  '8'

 L.  59        26  DUP_TOP          
               28  LOAD_GLOBAL              win32api
               30  LOAD_ATTR                error
               32  <121>                48  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  60        40  POP_EXCEPT       
               42  BREAK_LOOP          116  'to 116'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            24  '24'

 L.  61        50  SETUP_FINALLY        68  'to 68'

 L.  64        52  LOAD_GLOBAL              win32api
               54  LOAD_METHOD              RegQueryValue
               56  LOAD_FAST                'root'
               58  LOAD_FAST                'item'
               60  CALL_METHOD_2         2  ''
               62  STORE_FAST               'val'
               64  POP_BLOCK        
               66  JUMP_FORWARD         92  'to 92'
             68_0  COME_FROM_FINALLY    50  '50'

 L.  65        68  DUP_TOP          
               70  LOAD_GLOBAL              win32api
               72  LOAD_ATTR                error
               74  <121>                90  ''
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  66        82  LOAD_STR                 ''
               84  STORE_FAST               'val'
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            66  '66'

 L.  68        92  LOAD_FAST                'ret'
               94  LOAD_METHOD              append
               96  LOAD_FAST                'item'
               98  LOAD_FAST                'val'
              100  BUILD_TUPLE_2         2 
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L.  69       106  LOAD_FAST                'index'
              108  LOAD_CONST               1
              110  BINARY_ADD       
              112  STORE_FAST               'index'
              114  JUMP_BACK             8  'to 8'
            116_0  COME_FROM            42  '42'

 L.  70       116  LOAD_FAST                'ret'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 32


FLAG_RESTRICTED = 1
FLAG_CONTROL = 2
FLAG_HIDDEN = 4

def EnumTlbs--- This code section failed: ---

 L.  79         0  LOAD_GLOBAL              win32api
                2  LOAD_METHOD              RegOpenKey
                4  LOAD_GLOBAL              win32con
                6  LOAD_ATTR                HKEY_CLASSES_ROOT
                8  LOAD_STR                 'Typelib'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'key'

 L.  80        14  LOAD_GLOBAL              EnumKeys
               16  LOAD_FAST                'key'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'iids'

 L.  81        22  BUILD_LIST_0          0 
               24  STORE_FAST               'results'

 L.  82        26  LOAD_FAST                'iids'
               28  GET_ITER         
             30_0  COME_FROM           466  '466'
             30_1  COME_FROM            78  '78'
            30_32  FOR_ITER            468  'to 468'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'iid'
               38  STORE_FAST               'crap'

 L.  83        40  SETUP_FINALLY        62  'to 62'

 L.  84        42  LOAD_GLOBAL              win32api
               44  LOAD_METHOD              RegOpenKey
               46  LOAD_FAST                'key'
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'iid'
               52  CALL_FUNCTION_1       1  ''
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'key2'
               58  POP_BLOCK        
               60  JUMP_FORWARD         86  'to 86'
             62_0  COME_FROM_FINALLY    40  '40'

 L.  85        62  DUP_TOP          
               64  LOAD_GLOBAL              win32api
               66  LOAD_ATTR                error
               68  <121>                84  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L.  87        76  POP_EXCEPT       
               78  JUMP_BACK            30  'to 30'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            60  '60'

 L.  88        86  LOAD_GLOBAL              EnumKeys
               88  LOAD_FAST                'key2'
               90  CALL_FUNCTION_1       1  ''
               92  GET_ITER         
             94_0  COME_FROM           464  '464'
             94_1  COME_FROM           230  '230'
            94_96  FOR_ITER            466  'to 466'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'version'
              102  STORE_FAST               'tlbdesc'

 L.  89       104  LOAD_FAST                'version'
              106  LOAD_METHOD              split
              108  LOAD_STR                 '.'
              110  LOAD_CONST               1
              112  CALL_METHOD_2         2  ''
              114  STORE_FAST               'major_minor'

 L.  90       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'major_minor'
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               2
              124  COMPARE_OP               <
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  91       128  LOAD_FAST                'major_minor'
              130  LOAD_METHOD              append
              132  LOAD_STR                 '0'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L. 101       138  LOAD_FAST                'major_minor'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  STORE_FAST               'major'

 L. 102       146  LOAD_FAST                'major_minor'
              148  LOAD_CONST               1
              150  BINARY_SUBSCR    
              152  STORE_FAST               'minor'

 L. 103       154  LOAD_GLOBAL              win32api
              156  LOAD_METHOD              RegOpenKey
              158  LOAD_FAST                'key2'
              160  LOAD_GLOBAL              str
              162  LOAD_FAST                'version'
              164  CALL_FUNCTION_1       1  ''
              166  CALL_METHOD_2         2  ''
              168  STORE_FAST               'key3'

 L. 104       170  SETUP_FINALLY       192  'to 192'

 L. 106       172  LOAD_GLOBAL              int
              174  LOAD_GLOBAL              win32api
              176  LOAD_METHOD              RegQueryValue
              178  LOAD_FAST                'key3'
              180  LOAD_STR                 'FLAGS'
              182  CALL_METHOD_2         2  ''
              184  CALL_FUNCTION_1       1  ''
              186  STORE_FAST               'flags'
              188  POP_BLOCK        
              190  JUMP_FORWARD        220  'to 220'
            192_0  COME_FROM_FINALLY   170  '170'

 L. 107       192  DUP_TOP          
              194  LOAD_GLOBAL              win32api
              196  LOAD_ATTR                error
              198  LOAD_GLOBAL              ValueError
              200  BUILD_TUPLE_2         2 
              202  <121>               218  ''
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 108       210  LOAD_CONST               0
              212  STORE_FAST               'flags'
              214  POP_EXCEPT       
              216  JUMP_FORWARD        220  'to 220'
              218  <48>             
            220_0  COME_FROM           216  '216'
            220_1  COME_FROM           190  '190'

 L. 109       220  LOAD_FAST                'flags'
              222  LOAD_FAST                'excludeFlags'
              224  BINARY_AND       
              226  LOAD_CONST               0
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_FALSE_BACK    94  'to 94'

 L. 110       232  LOAD_GLOBAL              EnumKeys
              234  LOAD_FAST                'key3'
              236  CALL_FUNCTION_1       1  ''
              238  GET_ITER         
            240_0  COME_FROM           462  '462'
            240_1  COME_FROM           328  '328'
            240_2  COME_FROM           278  '278'
              240  FOR_ITER            464  'to 464'
              242  UNPACK_SEQUENCE_2     2 
              244  STORE_FAST               'lcid'
              246  STORE_FAST               'crap'

 L. 111       248  SETUP_FINALLY       262  'to 262'

 L. 112       250  LOAD_GLOBAL              int
              252  LOAD_FAST                'lcid'
              254  CALL_FUNCTION_1       1  ''
              256  STORE_FAST               'lcid'
              258  POP_BLOCK        
              260  JUMP_FORWARD        286  'to 286'
            262_0  COME_FROM_FINALLY   248  '248'

 L. 113       262  DUP_TOP          
              264  LOAD_GLOBAL              ValueError
          266_268  <121>               284  ''
              270  POP_TOP          
              272  POP_TOP          
              274  POP_TOP          

 L. 114       276  POP_EXCEPT       
              278  JUMP_BACK           240  'to 240'
              280  POP_EXCEPT       
              282  JUMP_FORWARD        286  'to 286'
              284  <48>             
            286_0  COME_FROM           282  '282'
            286_1  COME_FROM           260  '260'

 L. 116       286  SETUP_FINALLY       310  'to 310'

 L. 117       288  LOAD_GLOBAL              win32api
              290  LOAD_METHOD              RegOpenKey
              292  LOAD_FAST                'key3'
              294  LOAD_STR                 '%s\\win32'
              296  LOAD_FAST                'lcid'
              298  BUILD_TUPLE_1         1 
              300  BINARY_MODULO    
              302  CALL_METHOD_2         2  ''
              304  STORE_FAST               'key4'
              306  POP_BLOCK        
              308  JUMP_FORWARD        336  'to 336'
            310_0  COME_FROM_FINALLY   286  '286'

 L. 118       310  DUP_TOP          
              312  LOAD_GLOBAL              win32api
              314  LOAD_ATTR                error
          316_318  <121>               334  ''
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L. 119       326  POP_EXCEPT       
              328  JUMP_BACK           240  'to 240'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
              334  <48>             
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           308  '308'

 L. 120       336  SETUP_FINALLY       380  'to 380'

 L. 121       338  LOAD_GLOBAL              win32api
              340  LOAD_METHOD              RegQueryValueEx
              342  LOAD_FAST                'key4'
              344  LOAD_CONST               None
              346  CALL_METHOD_2         2  ''
              348  UNPACK_SEQUENCE_2     2 
              350  STORE_FAST               'dll'
              352  STORE_FAST               'typ'

 L. 122       354  LOAD_FAST                'typ'
              356  LOAD_GLOBAL              win32con
              358  LOAD_ATTR                REG_EXPAND_SZ
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   376  'to 376'

 L. 123       366  LOAD_GLOBAL              win32api
              368  LOAD_METHOD              ExpandEnvironmentStrings
              370  LOAD_FAST                'dll'
              372  CALL_METHOD_1         1  ''
              374  STORE_FAST               'dll'
            376_0  COME_FROM           362  '362'
              376  POP_BLOCK        
              378  JUMP_FORWARD        406  'to 406'
            380_0  COME_FROM_FINALLY   336  '336'

 L. 124       380  DUP_TOP          
              382  LOAD_GLOBAL              win32api
              384  LOAD_ATTR                error
          386_388  <121>               404  ''
              390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L. 125       396  LOAD_CONST               None
              398  STORE_FAST               'dll'
              400  POP_EXCEPT       
              402  JUMP_FORWARD        406  'to 406'
              404  <48>             
            406_0  COME_FROM           402  '402'
            406_1  COME_FROM           378  '378'

 L. 126       406  LOAD_GLOBAL              TypelibSpec
              408  LOAD_FAST                'iid'
              410  LOAD_FAST                'lcid'
              412  LOAD_FAST                'major'
              414  LOAD_FAST                'minor'
              416  LOAD_FAST                'flags'
              418  CALL_FUNCTION_5       5  ''
              420  STORE_FAST               'spec'

 L. 127       422  LOAD_FAST                'dll'
              424  LOAD_FAST                'spec'
              426  STORE_ATTR               dll

 L. 128       428  LOAD_FAST                'tlbdesc'
              430  LOAD_FAST                'spec'
              432  STORE_ATTR               desc

 L. 129       434  LOAD_FAST                'tlbdesc'
              436  LOAD_STR                 ' ('
              438  BINARY_ADD       
              440  LOAD_FAST                'version'
              442  BINARY_ADD       
              444  LOAD_STR                 ')'
              446  BINARY_ADD       
              448  LOAD_FAST                'spec'
              450  STORE_ATTR               ver_desc

 L. 130       452  LOAD_FAST                'results'
              454  LOAD_METHOD              append
              456  LOAD_FAST                'spec'
              458  CALL_METHOD_1         1  ''
              460  POP_TOP          
              462  JUMP_BACK           240  'to 240'
            464_0  COME_FROM           240  '240'
              464  JUMP_BACK            94  'to 94'
            466_0  COME_FROM            94  '94'
              466  JUMP_BACK            30  'to 30'
            468_0  COME_FROM            30  '30'

 L. 131       468  LOAD_FAST                'results'
              470  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 68


def FindTlbsWithDescription(desc):
    """Find all installed type libraries with the specified description
        """
    ret = []
    items = EnumTlbs()
    for item in items:
        if item.desc == desc:
            ret.appenditem
    else:
        return ret


def SelectTlb--- This code section failed: ---

 L. 146         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         pywin.dialogs.list
                6  STORE_FAST               'pywin'

 L. 147         8  LOAD_GLOBAL              EnumTlbs
               10  LOAD_FAST                'excludeFlags'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'items'

 L. 149        16  LOAD_FAST                'items'
               18  GET_ITER         
             20_0  COME_FROM            52  '52'
               20  FOR_ITER             54  'to 54'
               22  STORE_FAST               'i'

 L. 150        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'i'
               28  LOAD_ATTR                major
               30  LOAD_CONST               16
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_FAST                'i'
               36  STORE_ATTR               major

 L. 151        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'i'
               42  LOAD_ATTR                minor
               44  LOAD_CONST               16
               46  CALL_FUNCTION_2       2  ''
               48  LOAD_FAST                'i'
               50  STORE_ATTR               minor
               52  JUMP_BACK            20  'to 20'
             54_0  COME_FROM            20  '20'

 L. 152        54  LOAD_FAST                'items'
               56  LOAD_METHOD              sort
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 153        62  LOAD_FAST                'pywin'
               64  LOAD_ATTR                dialogs
               66  LOAD_ATTR                list
               68  LOAD_METHOD              SelectFromLists
               70  LOAD_FAST                'title'
               72  LOAD_FAST                'items'
               74  LOAD_STR                 'Type Library'
               76  BUILD_LIST_1          1 
               78  CALL_METHOD_3         3  ''
               80  STORE_FAST               'rc'

 L. 154        82  LOAD_FAST                'rc'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L. 155        90  LOAD_CONST               None
               92  RETURN_VALUE     
             94_0  COME_FROM            88  '88'

 L. 156        94  LOAD_FAST                'items'
               96  LOAD_FAST                'rc'
               98  BINARY_SUBSCR    
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 86


if __name__ == '__main__':
    print(SelectTlb().__dict__)