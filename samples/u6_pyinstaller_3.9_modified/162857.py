# uncompyle6 version 3.7.4
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
            116_0  COME_FROM_EXCEPT_CLAUSE    42  '42'

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
            30_32  FOR_ITER            518  'to 518'
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
             94_0  COME_FROM           230  '230'
            94_96  FOR_ITER            516  'to 516'
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
              230  POP_JUMP_IF_FALSE    94  'to 94'

 L. 110       232  LOAD_GLOBAL              EnumKeys
              234  LOAD_FAST                'key3'
              236  CALL_FUNCTION_1       1  ''
              238  GET_ITER         
          240_242  FOR_ITER            514  'to 514'
              244  UNPACK_SEQUENCE_2     2 
              246  STORE_FAST               'lcid'
              248  STORE_FAST               'crap'

 L. 111       250  SETUP_FINALLY       264  'to 264'

 L. 112       252  LOAD_GLOBAL              int
              254  LOAD_FAST                'lcid'
              256  CALL_FUNCTION_1       1  ''
              258  STORE_FAST               'lcid'
              260  POP_BLOCK        
              262  JUMP_FORWARD        288  'to 288'
            264_0  COME_FROM_FINALLY   250  '250'

 L. 113       264  DUP_TOP          
              266  LOAD_GLOBAL              ValueError
          268_270  <121>               286  ''
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 114       278  POP_EXCEPT       
              280  JUMP_BACK           240  'to 240'
              282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
              286  <48>             
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           262  '262'

 L. 116       288  SETUP_FINALLY       312  'to 312'

 L. 117       290  LOAD_GLOBAL              win32api
              292  LOAD_METHOD              RegOpenKey
              294  LOAD_FAST                'key3'
              296  LOAD_STR                 '%s\\win32'
              298  LOAD_FAST                'lcid'
              300  BUILD_TUPLE_1         1 
              302  BINARY_MODULO    
              304  CALL_METHOD_2         2  ''
              306  STORE_FAST               'key4'
              308  POP_BLOCK        
              310  JUMP_FORWARD        386  'to 386'
            312_0  COME_FROM_FINALLY   288  '288'

 L. 118       312  DUP_TOP          
              314  LOAD_GLOBAL              win32api
              316  LOAD_ATTR                error
          318_320  <121>               384  ''
              322  POP_TOP          
              324  POP_TOP          
              326  POP_TOP          

 L. 119       328  SETUP_FINALLY       352  'to 352'

 L. 120       330  LOAD_GLOBAL              win32api
              332  LOAD_METHOD              RegOpenKey
              334  LOAD_FAST                'key3'
              336  LOAD_STR                 '%s\\win64'
              338  LOAD_FAST                'lcid'
              340  BUILD_TUPLE_1         1 
              342  BINARY_MODULO    
              344  CALL_METHOD_2         2  ''
              346  STORE_FAST               'key4'
              348  POP_BLOCK        
              350  JUMP_FORWARD        380  'to 380'
            352_0  COME_FROM_FINALLY   328  '328'

 L. 121       352  DUP_TOP          
              354  LOAD_GLOBAL              win32api
              356  LOAD_ATTR                error
          358_360  <121>               378  ''
              362  POP_TOP          
              364  POP_TOP          
              366  POP_TOP          

 L. 122       368  POP_EXCEPT       
              370  POP_EXCEPT       
              372  JUMP_BACK           240  'to 240'
              374  POP_EXCEPT       
              376  JUMP_FORWARD        380  'to 380'
              378  <48>             
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           350  '350'
              380  POP_EXCEPT       
              382  JUMP_FORWARD        386  'to 386'
              384  <48>             
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           310  '310'

 L. 123       386  SETUP_FINALLY       430  'to 430'

 L. 124       388  LOAD_GLOBAL              win32api
              390  LOAD_METHOD              RegQueryValueEx
              392  LOAD_FAST                'key4'
              394  LOAD_CONST               None
              396  CALL_METHOD_2         2  ''
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'dll'
              402  STORE_FAST               'typ'

 L. 125       404  LOAD_FAST                'typ'
              406  LOAD_GLOBAL              win32con
              408  LOAD_ATTR                REG_EXPAND_SZ
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   426  'to 426'

 L. 126       416  LOAD_GLOBAL              win32api
              418  LOAD_METHOD              ExpandEnvironmentStrings
              420  LOAD_FAST                'dll'
              422  CALL_METHOD_1         1  ''
              424  STORE_FAST               'dll'
            426_0  COME_FROM           412  '412'
              426  POP_BLOCK        
              428  JUMP_FORWARD        456  'to 456'
            430_0  COME_FROM_FINALLY   386  '386'

 L. 127       430  DUP_TOP          
              432  LOAD_GLOBAL              win32api
              434  LOAD_ATTR                error
          436_438  <121>               454  ''
              440  POP_TOP          
              442  POP_TOP          
              444  POP_TOP          

 L. 128       446  LOAD_CONST               None
              448  STORE_FAST               'dll'
              450  POP_EXCEPT       
              452  JUMP_FORWARD        456  'to 456'
              454  <48>             
            456_0  COME_FROM           452  '452'
            456_1  COME_FROM           428  '428'

 L. 129       456  LOAD_GLOBAL              TypelibSpec
              458  LOAD_FAST                'iid'
              460  LOAD_FAST                'lcid'
              462  LOAD_FAST                'major'
              464  LOAD_FAST                'minor'
              466  LOAD_FAST                'flags'
              468  CALL_FUNCTION_5       5  ''
              470  STORE_FAST               'spec'

 L. 130       472  LOAD_FAST                'dll'
              474  LOAD_FAST                'spec'
              476  STORE_ATTR               dll

 L. 131       478  LOAD_FAST                'tlbdesc'
              480  LOAD_FAST                'spec'
              482  STORE_ATTR               desc

 L. 132       484  LOAD_FAST                'tlbdesc'
              486  LOAD_STR                 ' ('
              488  BINARY_ADD       
              490  LOAD_FAST                'version'
              492  BINARY_ADD       
              494  LOAD_STR                 ')'
              496  BINARY_ADD       
              498  LOAD_FAST                'spec'
              500  STORE_ATTR               ver_desc

 L. 133       502  LOAD_FAST                'results'
              504  LOAD_METHOD              append
              506  LOAD_FAST                'spec'
              508  CALL_METHOD_1         1  ''
              510  POP_TOP          
              512  JUMP_BACK           240  'to 240'
              514  JUMP_BACK            94  'to 94'
              516  JUMP_BACK            30  'to 30'

 L. 134       518  LOAD_FAST                'results'
              520  RETURN_VALUE     
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
        return ret


def SelectTlb--- This code section failed: ---

 L. 149         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         pywin.dialogs.list
                6  STORE_FAST               'pywin'

 L. 150         8  LOAD_GLOBAL              EnumTlbs
               10  LOAD_FAST                'excludeFlags'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'items'

 L. 152        16  LOAD_FAST                'items'
               18  GET_ITER         
               20  FOR_ITER             54  'to 54'
               22  STORE_FAST               'i'

 L. 153        24  LOAD_GLOBAL              int
               26  LOAD_FAST                'i'
               28  LOAD_ATTR                major
               30  LOAD_CONST               16
               32  CALL_FUNCTION_2       2  ''
               34  LOAD_FAST                'i'
               36  STORE_ATTR               major

 L. 154        38  LOAD_GLOBAL              int
               40  LOAD_FAST                'i'
               42  LOAD_ATTR                minor
               44  LOAD_CONST               16
               46  CALL_FUNCTION_2       2  ''
               48  LOAD_FAST                'i'
               50  STORE_ATTR               minor
               52  JUMP_BACK            20  'to 20'

 L. 155        54  LOAD_FAST                'items'
               56  LOAD_METHOD              sort
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 156        62  LOAD_FAST                'pywin'
               64  LOAD_ATTR                dialogs
               66  LOAD_ATTR                list
               68  LOAD_METHOD              SelectFromLists
               70  LOAD_FAST                'title'
               72  LOAD_FAST                'items'
               74  LOAD_STR                 'Type Library'
               76  BUILD_LIST_1          1 
               78  CALL_METHOD_3         3  ''
               80  STORE_FAST               'rc'

 L. 157        82  LOAD_FAST                'rc'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L. 158        90  LOAD_CONST               None
               92  RETURN_VALUE     
             94_0  COME_FROM            88  '88'

 L. 159        94  LOAD_FAST                'items'
               96  LOAD_FAST                'rc'
               98  BINARY_SUBSCR    
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 86


if __name__ == '__main__':
    print(SelectTlb().__dict__)