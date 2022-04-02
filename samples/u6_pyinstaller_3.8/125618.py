# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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

    def Resolve(self):
        if self.dll is None:
            return 0
        tlb = pythoncom.LoadTypeLib(self.dll)
        self.FromTypelib(tlb, None)
        return 1

    def FromTypelib(self, typelib, dllName=None):
        la = typelib.GetLibAttr()
        self.clsid = str(la[0])
        self.lcid = la[1]
        self.major = la[3]
        self.minor = la[4]
        if dllName:
            self.dll = dllName


def EnumKeys(root):
    index = 0
    ret = []
    while True:
        try:
            item = win32api.RegEnumKey(root, index)
        except win32api.error:
            break
        else:
            try:
                val = win32api.RegQueryValue(root, item)
            except win32api.error:
                val = ''
            else:
                ret.append((item, val))
                index = index + 1

    return ret


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
            30_32  FOR_ITER            478  'to 478'
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
               60  JUMP_FORWARD         88  'to 88'
             62_0  COME_FROM_FINALLY    40  '40'

 L.  85        62  DUP_TOP          
               64  LOAD_GLOBAL              win32api
               66  LOAD_ATTR                error
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    86  'to 86'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L.  87        78  POP_EXCEPT       
               80  JUMP_BACK            30  'to 30'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            70  '70'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            60  '60'

 L.  88        88  LOAD_GLOBAL              EnumKeys
               90  LOAD_FAST                'key2'
               92  CALL_FUNCTION_1       1  ''
               94  GET_ITER         
             96_0  COME_FROM           234  '234'
            96_98  FOR_ITER            476  'to 476'
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'version'
              104  STORE_FAST               'tlbdesc'

 L.  89       106  LOAD_FAST                'version'
              108  LOAD_METHOD              split
              110  LOAD_STR                 '.'
              112  LOAD_CONST               1
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'major_minor'

 L.  90       118  LOAD_GLOBAL              len
              120  LOAD_FAST                'major_minor'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_CONST               2
              126  COMPARE_OP               <
              128  POP_JUMP_IF_FALSE   140  'to 140'

 L.  91       130  LOAD_FAST                'major_minor'
              132  LOAD_METHOD              append
              134  LOAD_STR                 '0'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
            140_0  COME_FROM           128  '128'

 L. 101       140  LOAD_FAST                'major_minor'
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  STORE_FAST               'major'

 L. 102       148  LOAD_FAST                'major_minor'
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  STORE_FAST               'minor'

 L. 103       156  LOAD_GLOBAL              win32api
              158  LOAD_METHOD              RegOpenKey
              160  LOAD_FAST                'key2'
              162  LOAD_GLOBAL              str
              164  LOAD_FAST                'version'
              166  CALL_FUNCTION_1       1  ''
              168  CALL_METHOD_2         2  ''
              170  STORE_FAST               'key3'

 L. 104       172  SETUP_FINALLY       194  'to 194'

 L. 106       174  LOAD_GLOBAL              int
              176  LOAD_GLOBAL              win32api
              178  LOAD_METHOD              RegQueryValue
              180  LOAD_FAST                'key3'
              182  LOAD_STR                 'FLAGS'
              184  CALL_METHOD_2         2  ''
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               'flags'
              190  POP_BLOCK        
              192  JUMP_FORWARD        224  'to 224'
            194_0  COME_FROM_FINALLY   172  '172'

 L. 107       194  DUP_TOP          
              196  LOAD_GLOBAL              win32api
              198  LOAD_ATTR                error
              200  LOAD_GLOBAL              ValueError
              202  BUILD_TUPLE_2         2 
              204  COMPARE_OP               exception-match
              206  POP_JUMP_IF_FALSE   222  'to 222'
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          

 L. 108       214  LOAD_CONST               0
              216  STORE_FAST               'flags'
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           206  '206'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           192  '192'

 L. 109       224  LOAD_FAST                'flags'
              226  LOAD_FAST                'excludeFlags'
              228  BINARY_AND       
              230  LOAD_CONST               0
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE    96  'to 96'

 L. 110       236  LOAD_GLOBAL              EnumKeys
              238  LOAD_FAST                'key3'
              240  CALL_FUNCTION_1       1  ''
              242  GET_ITER         
              244  FOR_ITER            474  'to 474'
              246  UNPACK_SEQUENCE_2     2 
              248  STORE_FAST               'lcid'
              250  STORE_FAST               'crap'

 L. 111       252  SETUP_FINALLY       266  'to 266'

 L. 112       254  LOAD_GLOBAL              int
              256  LOAD_FAST                'lcid'
              258  CALL_FUNCTION_1       1  ''
              260  STORE_FAST               'lcid'
              262  POP_BLOCK        
              264  JUMP_FORWARD        292  'to 292'
            266_0  COME_FROM_FINALLY   252  '252'

 L. 113       266  DUP_TOP          
              268  LOAD_GLOBAL              ValueError
              270  COMPARE_OP               exception-match
          272_274  POP_JUMP_IF_FALSE   290  'to 290'
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          

 L. 114       282  POP_EXCEPT       
              284  JUMP_BACK           244  'to 244'
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           272  '272'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'
            292_1  COME_FROM           264  '264'

 L. 116       292  SETUP_FINALLY       316  'to 316'

 L. 117       294  LOAD_GLOBAL              win32api
              296  LOAD_METHOD              RegOpenKey
              298  LOAD_FAST                'key3'
              300  LOAD_STR                 '%s\\win32'
              302  LOAD_FAST                'lcid'
              304  BUILD_TUPLE_1         1 
              306  BINARY_MODULO    
              308  CALL_METHOD_2         2  ''
              310  STORE_FAST               'key4'
              312  POP_BLOCK        
              314  JUMP_FORWARD        344  'to 344'
            316_0  COME_FROM_FINALLY   292  '292'

 L. 118       316  DUP_TOP          
              318  LOAD_GLOBAL              win32api
              320  LOAD_ATTR                error
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   342  'to 342'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 119       334  POP_EXCEPT       
              336  JUMP_BACK           244  'to 244'
              338  POP_EXCEPT       
              340  JUMP_FORWARD        344  'to 344'
            342_0  COME_FROM           324  '324'
              342  END_FINALLY      
            344_0  COME_FROM           340  '340'
            344_1  COME_FROM           314  '314'

 L. 120       344  SETUP_FINALLY       388  'to 388'

 L. 121       346  LOAD_GLOBAL              win32api
              348  LOAD_METHOD              RegQueryValueEx
              350  LOAD_FAST                'key4'
              352  LOAD_CONST               None
              354  CALL_METHOD_2         2  ''
              356  UNPACK_SEQUENCE_2     2 
              358  STORE_FAST               'dll'
              360  STORE_FAST               'typ'

 L. 122       362  LOAD_FAST                'typ'
              364  LOAD_GLOBAL              win32con
              366  LOAD_ATTR                REG_EXPAND_SZ
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   384  'to 384'

 L. 123       374  LOAD_GLOBAL              win32api
              376  LOAD_METHOD              ExpandEnvironmentStrings
              378  LOAD_FAST                'dll'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'dll'
            384_0  COME_FROM           370  '370'
              384  POP_BLOCK        
              386  JUMP_FORWARD        416  'to 416'
            388_0  COME_FROM_FINALLY   344  '344'

 L. 124       388  DUP_TOP          
              390  LOAD_GLOBAL              win32api
              392  LOAD_ATTR                error
              394  COMPARE_OP               exception-match
          396_398  POP_JUMP_IF_FALSE   414  'to 414'
              400  POP_TOP          
              402  POP_TOP          
              404  POP_TOP          

 L. 125       406  LOAD_CONST               None
              408  STORE_FAST               'dll'
              410  POP_EXCEPT       
              412  JUMP_FORWARD        416  'to 416'
            414_0  COME_FROM           396  '396'
              414  END_FINALLY      
            416_0  COME_FROM           412  '412'
            416_1  COME_FROM           386  '386'

 L. 126       416  LOAD_GLOBAL              TypelibSpec
              418  LOAD_FAST                'iid'
              420  LOAD_FAST                'lcid'
              422  LOAD_FAST                'major'
              424  LOAD_FAST                'minor'
              426  LOAD_FAST                'flags'
              428  CALL_FUNCTION_5       5  ''
              430  STORE_FAST               'spec'

 L. 127       432  LOAD_FAST                'dll'
              434  LOAD_FAST                'spec'
              436  STORE_ATTR               dll

 L. 128       438  LOAD_FAST                'tlbdesc'
              440  LOAD_FAST                'spec'
              442  STORE_ATTR               desc

 L. 129       444  LOAD_FAST                'tlbdesc'
              446  LOAD_STR                 ' ('
              448  BINARY_ADD       
              450  LOAD_FAST                'version'
              452  BINARY_ADD       
              454  LOAD_STR                 ')'
              456  BINARY_ADD       
              458  LOAD_FAST                'spec'
              460  STORE_ATTR               ver_desc

 L. 130       462  LOAD_FAST                'results'
              464  LOAD_METHOD              append
              466  LOAD_FAST                'spec'
              468  CALL_METHOD_1         1  ''
              470  POP_TOP          
              472  JUMP_BACK           244  'to 244'
              474  JUMP_BACK            96  'to 96'
              476  JUMP_BACK            30  'to 30'

 L. 131       478  LOAD_FAST                'results'
              480  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 82


def FindTlbsWithDescription(desc):
    """Find all installed type libraries with the specified description
        """
    ret = []
    items = EnumTlbs()
    for item in items:
        if item.desc == desc:
            ret.append(item)
        return ret


def SelectTlb(title='Select Library', excludeFlags=0):
    """Display a list of all the type libraries, and select one.   Returns None if cancelled
        """
    import pywin.dialogs.list
    items = EnumTlbs(excludeFlags)
    for i in items:
        i.major = int(i.major, 16)
        i.minor = int(i.minor, 16)
    else:
        items.sort()
        rc = pywin.dialogs.list.SelectFromLists(title, items, ['Type Library'])
        if rc is None:
            return
        return items[rc]


if __name__ == '__main__':
    print(SelectTlb().__dict__)