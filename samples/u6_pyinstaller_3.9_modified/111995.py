# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\mfc\dialog.py
""" Base class for Dialogs.  Also contains a few useful utility functions
"""
import win32ui, win32con
from pywin.mfc import window

def dllFromDll--- This code section failed: ---

 L.  14         0  LOAD_FAST                'dllid'
                2  LOAD_CONST               None
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  15         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  16        12  LOAD_GLOBAL              type
               14  LOAD_STR                 ''
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_GLOBAL              type
               20  LOAD_FAST                'dllid'
               22  CALL_FUNCTION_1       1  ''
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  17        28  LOAD_GLOBAL              win32ui
               30  LOAD_METHOD              LoadLibrary
               32  LOAD_FAST                'dllid'
               34  CALL_METHOD_1         1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM            26  '26'

 L.  19        38  SETUP_FINALLY        52  'to 52'

 L.  20        40  LOAD_FAST                'dllid'
               42  LOAD_METHOD              GetFileName
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  JUMP_FORWARD         78  'to 78'
             52_0  COME_FROM_FINALLY    38  '38'

 L.  21        52  DUP_TOP          
               54  LOAD_GLOBAL              AttributeError
               56  <121>                76  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  22        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'DLL parameter must be None, a filename or a dll object'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            50  '50'

 L.  23        78  LOAD_FAST                'dllid'
               80  RETURN_VALUE     

Parse error at or near `<121>' instruction at offset 56


class Dialog(window.Wnd):
    __doc__ = ' Base class for a dialog'

    def __init__(self, id, dllid=None):
        """ id is the resource ID, or a template
                        dllid may be None, a dll object, or a string with a dll name """
        self.dll = dllFromDll(dllid)
        if type(id) == type([]):
            dlg = win32ui.CreateDialogIndirectid
        else:
            dlg = win32ui.CreateDialog(id, self.dll)
        window.Wnd.__init__(self, dlg)
        self.HookCommands
        self.bHaveInit = None

    def HookCommands(self):
        pass

    def OnAttachedObjectDeath(self):
        self.data = self._obj_.data
        window.Wnd.OnAttachedObjectDeathself

    def OnOK(self):
        self._obj_.OnOK

    def OnCancel(self):
        self._obj_.OnCancel

    def OnInitDialog(self):
        self.bHaveInit = 1
        if self._obj_.data:
            self._obj_.UpdateData0
        return 1

    def OnDestroy(self, msg):
        self.dll = None

    def AddDDX(self, *args):
        self._obj_.datalist.appendargs

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        self._obj_.data[key] = item

    def keys(self):
        return list(self.data.keys)

    def items(self):
        return list(self.data.items)

    def values(self):
        return list(self.data.values)

    def has_key--- This code section failed: ---

 L.  72         0  LOAD_FAST                'key'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                data
                6  <118>                 0  ''
                8  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class PrintDialog(Dialog):
    __doc__ = ' Base class for a print dialog'

    def __init__(self, pInfo, dlgID, printSetupOnly=0, flags=win32ui.PD_ALLPAGES | win32ui.PD_USEDEVMODECOPIES | win32ui.PD_NOPAGENUMS | win32ui.PD_HIDEPRINTTOFILE | win32ui.PD_NOSELECTION, parent=None, dllid=None):
        self.dll = dllFromDll(dllid)
        if type(dlgID) == type([]):
            raise TypeError('dlgID parameter must be an integer resource ID')
        dlg = win32ui.CreatePrintDialog(dlgID, printSetupOnly, flags, parent, self.dll)
        window.Wnd.__init__(self, dlg)
        self.HookCommands
        self.bHaveInit = None
        self.pInfo = pInfo
        flags = pInfo.GetFlags
        self['toFile'] = flags & win32ui.PD_PRINTTOFILE != 0
        self['direct'] = pInfo.GetDirect
        self['preview'] = pInfo.GetPreview
        self['continuePrinting'] = pInfo.GetContinuePrinting
        self['curPage'] = pInfo.GetCurPage
        self['numPreviewPages'] = pInfo.GetNumPreviewPages
        self['userData'] = pInfo.GetUserData
        self['draw'] = pInfo.GetDraw
        self['pageDesc'] = pInfo.GetPageDesc
        self['minPage'] = pInfo.GetMinPage
        self['maxPage'] = pInfo.GetMaxPage
        self['offsetPage'] = pInfo.GetOffsetPage
        self['fromPage'] = pInfo.GetFromPage
        self['toPage'] = pInfo.GetToPage
        self['copies'] = 0
        self['deviceName'] = ''
        self['driverName'] = ''
        self['printAll'] = 0
        self['printCollate'] = 0
        self['printRange'] = 0
        self['printSelection'] = 0

    def OnInitDialog(self):
        self.pInfo.CreatePrinterDC
        return self._obj_.OnInitDialog

    def OnCancel(self):
        del self.pInfo

    def OnOK(self):
        """DoModal has finished. Can now access the users choices"""
        self._obj_.OnOK
        pInfo = self.pInfo
        flags = pInfo.GetFlags
        self['toFile'] = flags & win32ui.PD_PRINTTOFILE != 0
        self['direct'] = pInfo.GetDirect
        self['preview'] = pInfo.GetPreview
        self['continuePrinting'] = pInfo.GetContinuePrinting
        self['curPage'] = pInfo.GetCurPage
        self['numPreviewPages'] = pInfo.GetNumPreviewPages
        self['userData'] = pInfo.GetUserData
        self['draw'] = pInfo.GetDraw
        self['pageDesc'] = pInfo.GetPageDesc
        self['minPage'] = pInfo.GetMinPage
        self['maxPage'] = pInfo.GetMaxPage
        self['offsetPage'] = pInfo.GetOffsetPage
        self['fromPage'] = pInfo.GetFromPage
        self['toPage'] = pInfo.GetToPage
        self['copies'] = pInfo.GetCopies
        self['deviceName'] = pInfo.GetDeviceName
        self['driverName'] = pInfo.GetDriverName
        self['printAll'] = pInfo.PrintAll
        self['printCollate'] = pInfo.PrintCollate
        self['printRange'] = pInfo.PrintRange
        self['printSelection'] = pInfo.PrintSelection
        del self.pInfo


class PropertyPage(Dialog):
    __doc__ = ' Base class for a Property Page'

    def __init__(self, id, dllid=None, caption=0):
        """ id is the resource ID
                        dllid may be None, a dll object, or a string with a dll name """
        self.dll = dllFromDll(dllid)
        if self.dll:
            oldRes = win32ui.SetResourceself.dll
        elif type(id) == type([]):
            dlg = win32ui.CreatePropertyPageIndirectid
        else:
            dlg = win32ui.CreatePropertyPage(id, caption)
        if self.dll:
            win32ui.SetResourceoldRes
        window.Wnd.__init__(self, dlg)
        self.HookCommands


class PropertySheet(window.Wnd):

    def __init__--- This code section failed: ---

 L. 178         0  LOAD_GLOBAL              dllFromDll
                2  LOAD_FAST                'dll'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_FAST                'self'
                8  STORE_ATTR               dll

 L. 179        10  LOAD_GLOBAL              win32ui
               12  LOAD_METHOD              CreatePropertySheet
               14  LOAD_FAST                'caption'
               16  CALL_METHOD_1         1  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               sheet

 L. 180        22  LOAD_GLOBAL              window
               24  LOAD_ATTR                Wnd
               26  LOAD_METHOD              __init__
               28  LOAD_FAST                'self'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                sheet
               34  CALL_METHOD_2         2  ''
               36  POP_TOP          

 L. 181        38  LOAD_FAST                'pageList'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 182        46  LOAD_FAST                'self'
               48  LOAD_METHOD              AddPage
               50  LOAD_FAST                'pageList'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            44  '44'

Parse error at or near `<117>' instruction at offset 42

    def OnInitDialog(self):
        return self._obj_.OnInitDialog

    def DoModal(self):
        if self.dll:
            oldRes = win32ui.SetResourceself.dll
        rc = self.sheet.DoModal
        if self.dll:
            win32ui.SetResourceoldRes
        return rc

    def AddPage--- This code section failed: ---

 L. 196         0  LOAD_FAST                'self'
                2  LOAD_ATTR                dll
                4  POP_JUMP_IF_FALSE    18  'to 18'

 L. 197         6  LOAD_GLOBAL              win32ui
                8  LOAD_METHOD              SetResource
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                dll
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'oldRes'
             18_0  COME_FROM             4  '4'

 L. 198        18  SETUP_FINALLY        36  'to 36'

 L. 199        20  LOAD_FAST                'pages'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  POP_TOP          

 L. 200        28  LOAD_CONST               1
               30  STORE_FAST               'isSeq'
               32  POP_BLOCK        
               34  JUMP_FORWARD         62  'to 62'
             36_0  COME_FROM_FINALLY    18  '18'

 L. 201        36  DUP_TOP          
               38  LOAD_GLOBAL              TypeError
               40  LOAD_GLOBAL              KeyError
               42  BUILD_TUPLE_2         2 
               44  <121>                60  ''
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 202        52  LOAD_CONST               0
               54  STORE_FAST               'isSeq'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            34  '34'

 L. 203        62  LOAD_FAST                'isSeq'
               64  POP_JUMP_IF_FALSE    88  'to 88'

 L. 204        66  LOAD_FAST                'pages'
               68  GET_ITER         
               70  FOR_ITER             86  'to 86'
               72  STORE_FAST               'page'

 L. 205        74  LOAD_FAST                'self'
               76  LOAD_METHOD              DoAddSinglePage
               78  LOAD_FAST                'page'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            70  'to 70'
               86  JUMP_FORWARD         98  'to 98'
             88_0  COME_FROM            64  '64'

 L. 207        88  LOAD_FAST                'self'
               90  LOAD_METHOD              DoAddSinglePage
               92  LOAD_FAST                'pages'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
             98_0  COME_FROM            86  '86'

 L. 208        98  LOAD_FAST                'self'
              100  LOAD_ATTR                dll
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 209       104  LOAD_GLOBAL              win32ui
              106  LOAD_METHOD              SetResource
              108  LOAD_FAST                'oldRes'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
            114_0  COME_FROM           102  '102'

Parse error at or near `<121>' instruction at offset 44

    def DoAddSinglePage(self, page):
        """Page may be page, or int ID. Assumes DLL setup """
        if type(page) == type(0):
            self.sheet.AddPagewin32ui.CreatePropertyPagepage
        else:
            self.sheet.AddPagepage


def GetSimpleInput--- This code section failed: ---

 L. 223         0  LOAD_FAST                'title'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'
                8  LOAD_GLOBAL              win32ui
               10  LOAD_METHOD              GetMainFrame
               12  CALL_METHOD_0         0  ''
               14  LOAD_METHOD              GetWindowText
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'title'
             20_0  COME_FROM             6  '6'

 L. 225        20  LOAD_GLOBAL              Dialog
               22  STORE_DEREF              'DlgBaseClass'

 L. 226        24  LOAD_BUILD_CLASS 
               26  LOAD_CLOSURE             'DlgBaseClass'
               28  BUILD_TUPLE_1         1 
               30  LOAD_CODE                <code_object DlgSimpleInput>
               32  LOAD_STR                 'DlgSimpleInput'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_STR                 'DlgSimpleInput'
               38  LOAD_DEREF               'DlgBaseClass'
               40  CALL_FUNCTION_3       3  ''
               42  STORE_FAST               'DlgSimpleInput'

 L. 238        44  LOAD_FAST                'DlgSimpleInput'
               46  LOAD_FAST                'prompt'
               48  LOAD_FAST                'defValue'
               50  LOAD_FAST                'title'
               52  CALL_FUNCTION_3       3  ''
               54  STORE_FAST               'dlg'

 L. 239        56  LOAD_FAST                'dlg'
               58  LOAD_METHOD              DoModal
               60  CALL_METHOD_0         0  ''
               62  LOAD_GLOBAL              win32con
               64  LOAD_ATTR                IDOK
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L. 240        70  LOAD_CONST               None
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 241        74  LOAD_FAST                'dlg'
               76  LOAD_STR                 'result'
               78  BINARY_SUBSCR    
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1