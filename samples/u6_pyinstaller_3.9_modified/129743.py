# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\dialogs\list.py
from pywin.mfc import dialog
import win32ui, win32con, commctrl, win32api

class ListDialog(dialog.Dialog):

    def __init__(self, title, list):
        dialog.Dialog.__init__(self, self._maketemplate(title))
        self.HookMessage(self.on_size, win32con.WM_SIZE)
        self.HookNotify(self.OnListItemChange, commctrl.LVN_ITEMCHANGED)
        self.HookCommand(self.OnListClick, win32ui.IDC_LIST1)
        self.items = list

    def _maketemplate(self, title):
        style = win32con.WS_DLGFRAME | win32con.WS_SYSMENU | win32con.WS_VISIBLE
        ls = win32con.WS_CHILD | win32con.WS_VISIBLE | commctrl.LVS_ALIGNLEFT | commctrl.LVS_REPORT
        bs = win32con.WS_CHILD | win32con.WS_VISIBLE
        return [
         [
          title, (0, 0, 200, 200), style, None, (8, 'MS Sans Serif')],
         [
          'SysListView32', None, win32ui.IDC_LIST1, (0, 0, 200, 200), ls],
         [
          128, 'OK', win32con.IDOK, (10, 0, 50, 14), bs | win32con.BS_DEFPUSHBUTTON],
         [
          128, 'Cancel', win32con.IDCANCEL, (0, 0, 50, 14), bs]]

    def FillList(self):
        size = self.GetWindowRect()
        width = size[2] - size[0] - 10
        itemDetails = (commctrl.LVCFMT_LEFT, width, 'Item', 0)
        self.itemsControl.InsertColumn(0, itemDetails)
        index = 0
        for item in self.items:
            index = self.itemsControl.InsertItem(index + 1, str(item), 0)

    def OnListClick(self, id, code):
        if code == commctrl.NM_DBLCLK:
            self.EndDialog(win32con.IDOK)
        return 1

    def OnListItemChange--- This code section failed: ---

 L.  46         0  LOAD_FAST                'std'
                2  LOAD_FAST                'extra'
                4  ROT_TWO          
                6  UNPACK_SEQUENCE_3     3 
                8  STORE_FAST               'hwndFrom'
               10  STORE_FAST               'idFrom'
               12  STORE_FAST               'code'
               14  UNPACK_SEQUENCE_7     7 
               16  STORE_FAST               'itemNotify'
               18  STORE_FAST               'sub'
               20  STORE_FAST               'newState'
               22  STORE_FAST               'oldState'
               24  STORE_FAST               'change'
               26  STORE_FAST               'point'
               28  STORE_FAST               'lparam'

 L.  47        30  LOAD_FAST                'oldState'
               32  LOAD_GLOBAL              commctrl
               34  LOAD_ATTR                LVIS_SELECTED
               36  BINARY_AND       
               38  LOAD_CONST               0
               40  COMPARE_OP               !=
               42  STORE_FAST               'oldSel'

 L.  48        44  LOAD_FAST                'newState'
               46  LOAD_GLOBAL              commctrl
               48  LOAD_ATTR                LVIS_SELECTED
               50  BINARY_AND       
               52  LOAD_CONST               0
               54  COMPARE_OP               !=
               56  STORE_FAST               'newSel'

 L.  49        58  LOAD_FAST                'oldSel'
               60  LOAD_FAST                'newSel'
               62  COMPARE_OP               !=
               64  POP_JUMP_IF_FALSE   116  'to 116'

 L.  50        66  SETUP_FINALLY        90  'to 90'

 L.  51        68  LOAD_FAST                'itemNotify'
               70  LOAD_FAST                'self'
               72  STORE_ATTR               selecteditem

 L.  52        74  LOAD_FAST                'self'
               76  LOAD_ATTR                butOK
               78  LOAD_METHOD              EnableWindow
               80  LOAD_CONST               1
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  POP_BLOCK        
               88  JUMP_FORWARD        116  'to 116'
             90_0  COME_FROM_FINALLY    66  '66'

 L.  53        90  DUP_TOP          
               92  LOAD_GLOBAL              win32ui
               94  LOAD_ATTR                error
               96  <121>               114  ''
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L.  54       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               selecteditem
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            88  '88'
            116_2  COME_FROM            64  '64'

Parse error at or near `<121>' instruction at offset 96

    def OnInitDialog(self):
        rc = dialog.Dialog.OnInitDialog(self)
        self.itemsControl = self.GetDlgItem(win32ui.IDC_LIST1)
        self.butOK = self.GetDlgItem(win32con.IDOK)
        self.butCancel = self.GetDlgItem(win32con.IDCANCEL)
        self.FillList()
        size = self.GetWindowRect()
        self.LayoutControls(size[2] - size[0], size[3] - size[1])
        self.butOK.EnableWindow(0)
        return rc

    def LayoutControls(self, w, h):
        self.itemsControl.MoveWindow((0, 0, w, h - 30))
        self.butCancel.MoveWindow((10, h - 24, 60, h - 4))
        self.butOK.MoveWindow((w - 60, h - 24, w - 10, h - 4))

    def on_size(self, params):
        lparam = params[3]
        w = win32api.LOWORD(lparam)
        h = win32api.HIWORD(lparam)
        self.LayoutControls(w, h)


class ListsDialog(ListDialog):

    def __init__(self, title, list, colHeadings=[
 'Item']):
        ListDialog.__init__(self, title, list)
        self.colHeadings = colHeadings

    def FillList(self):
        index = 0
        size = self.GetWindowRect()
        width = size[2] - size[0] - 10 - win32api.GetSystemMetrics(win32con.SM_CXVSCROLL)
        numCols = len(self.colHeadings)
        for col in self.colHeadings:
            itemDetails = (
             commctrl.LVCFMT_LEFT, width / numCols, col, 0)
            self.itemsControl.InsertColumn(index, itemDetails)
            index = index + 1
        else:
            index = 0
            for items in self.items:
                index = self.itemsControl.InsertItem(index + 1, str(items[0]), 0)
                for itemno in range(1, numCols):
                    item = items[itemno]
                    self.itemsControl.SetItemText(index, itemno, str(item))


def SelectFromList(title, lst):
    dlg = ListDialog(title, lst)
    if dlg.DoModal() == win32con.IDOK:
        return dlg.selecteditem
    return


def SelectFromLists(title, lists, headings):
    dlg = ListsDialog(title, lists, headings)
    if dlg.DoModal() == win32con.IDOK:
        return dlg.selecteditem
    return


def test--- This code section failed: ---

 L. 119         0  LOAD_GLOBAL              print
                2  LOAD_GLOBAL              SelectFromLists
                4  LOAD_STR                 'Multi-List'
                6  BUILD_LIST_0          0 
                8  LOAD_CONST               (('1', 1, 'a'), ('2', 2, 'b'), ('3', 3, 'c'))
               10  CALL_FINALLY         13  'to 13'
               12  LOAD_STR                 'Col 1'
               14  LOAD_STR                 'Col 2'
               16  BUILD_LIST_2          2 
               18  CALL_FUNCTION_3       3  ''
               20  CALL_FUNCTION_1       1  ''
               22  POP_TOP          

Parse error at or near `None' instruction at offset -1


if __name__ == '__main__':
    test()