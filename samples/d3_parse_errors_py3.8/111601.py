# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: tkinter\filedialog.py
"""File selection dialog classes.

Classes:

- FileDialog
- LoadFileDialog
- SaveFileDialog

This module also presents tk common file dialogues, it provides interfaces
to the native file dialogues available in Tk 4.2 and newer, and the
directory dialogue available in Tk 8.3 and newer.
These interfaces were written by Fredrik Lundh, May 1997.
"""
from tkinter import *
from tkinter.dialog import Dialog
from tkinter import commondialog
import os, fnmatch
dialogstates = {}

class FileDialog:
    __doc__ = "Standard file selection dialog -- no checks on selected file.\n\n    Usage:\n\n        d = FileDialog(master)\n        fname = d.go(dir_or_file, pattern, default, key)\n        if fname is None: ...canceled...\n        else: ...open file...\n\n    All arguments to go() are optional.\n\n    The 'key' argument specifies a key in the global dictionary\n    'dialogstates', which keeps track of the values for the directory\n    and pattern arguments, overriding the values passed in (it does\n    not keep track of the default argument!).  If no key is specified,\n    the dialog keeps no memory of previous state.  Note that memory is\n    kept even when the dialog is canceled.  (All this emulates the\n    behavior of the Macintosh file selection dialogs.)\n\n    "
    title = 'File Selection Dialog'

    def __init__(self, master, title=None):
        if title is None:
            title = self.title
        self.master = master
        self.directory = None
        self.top = Toplevel(master)
        self.top.title(title)
        self.top.iconname(title)
        self.botframe = Frame(self.top)
        self.botframe.pack(side=BOTTOM, fill=X)
        self.selection = Entry(self.top)
        self.selection.pack(side=BOTTOM, fill=X)
        self.selection.bind('<Return>', self.ok_event)
        self.filter = Entry(self.top)
        self.filter.pack(side=TOP, fill=X)
        self.filter.bind('<Return>', self.filter_command)
        self.midframe = Frame(self.top)
        self.midframe.pack(expand=YES, fill=BOTH)
        self.filesbar = Scrollbar(self.midframe)
        self.filesbar.pack(side=RIGHT, fill=Y)
        self.files = Listbox((self.midframe), exportselection=0, yscrollcommand=(
         self.filesbar, 'set'))
        self.files.pack(side=RIGHT, expand=YES, fill=BOTH)
        btags = self.files.bindtags()
        self.files.bindtags(btags[1:] + btags[:1])
        self.files.bind('<ButtonRelease-1>', self.files_select_event)
        self.files.bind('<Double-ButtonRelease-1>', self.files_double_event)
        self.filesbar.config(command=(self.files, 'yview'))
        self.dirsbar = Scrollbar(self.midframe)
        self.dirsbar.pack(side=LEFT, fill=Y)
        self.dirs = Listbox((self.midframe), exportselection=0, yscrollcommand=(
         self.dirsbar, 'set'))
        self.dirs.pack(side=LEFT, expand=YES, fill=BOTH)
        self.dirsbar.config(command=(self.dirs, 'yview'))
        btags = self.dirs.bindtags()
        self.dirs.bindtags(btags[1:] + btags[:1])
        self.dirs.bind('<ButtonRelease-1>', self.dirs_select_event)
        self.dirs.bind('<Double-ButtonRelease-1>', self.dirs_double_event)
        self.ok_button = Button((self.botframe), text='OK',
          command=(self.ok_command))
        self.ok_button.pack(side=LEFT)
        self.filter_button = Button((self.botframe), text='Filter',
          command=(self.filter_command))
        self.filter_button.pack(side=LEFT, expand=YES)
        self.cancel_button = Button((self.botframe), text='Cancel',
          command=(self.cancel_command))
        self.cancel_button.pack(side=RIGHT)
        self.top.protocol('WM_DELETE_WINDOW', self.cancel_command)
        self.top.bind('<Alt-w>', self.cancel_command)
        self.top.bind('<Alt-W>', self.cancel_command)

    def go(self, dir_or_file=os.curdir, pattern='*', default='', key=None):
        if key and key in dialogstates:
            self.directory, pattern = dialogstates[key]
        else:
            dir_or_file = os.path.expanduser(dir_or_file)
            if os.path.isdir(dir_or_file):
                self.directory = dir_or_file
            else:
                self.directory, default = os.path.split(dir_or_file)
        self.set_filter(self.directory, pattern)
        self.set_selection(default)
        self.filter_command()
        self.selection.focus_set()
        self.top.wait_visibility()
        self.top.grab_set()
        self.how = None
        self.master.mainloop()
        if key:
            directory, pattern = self.get_filter()
            if self.how:
                directory = os.path.dirname(self.how)
            dialogstates[key] = (
             directory, pattern)
        self.top.destroy()
        return self.how

    def quit(self, how=None):
        self.how = how
        self.master.quit()

    def dirs_double_event(self, event):
        self.filter_command()

    def dirs_select_event(self, event):
        dir, pat = self.get_filter()
        subdir = self.dirs.get('active')
        dir = os.path.normpath(os.path.join(self.directory, subdir))
        self.set_filter(dir, pat)

    def files_double_event(self, event):
        self.ok_command()

    def files_select_event(self, event):
        file = self.files.get('active')
        self.set_selection(file)

    def ok_event(self, event):
        self.ok_command()

    def ok_command(self):
        self.quit(self.get_selection())

    def filter_command--- This code section failed: ---

 L. 166         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_filter
                4  CALL_METHOD_0         0  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'dir'
               10  STORE_FAST               'pat'

 L. 167        12  SETUP_FINALLY        28  'to 28'

 L. 168        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              listdir
               18  LOAD_FAST                'dir'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'names'
               24  POP_BLOCK        
               26  JUMP_FORWARD         60  'to 60'
             28_0  COME_FROM_FINALLY    12  '12'

 L. 169        28  DUP_TOP          
               30  LOAD_GLOBAL              OSError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    58  'to 58'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 170        42  LOAD_FAST                'self'
               44  LOAD_ATTR                master
               46  LOAD_METHOD              bell
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L. 171        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            34  '34'
               58  END_FINALLY      
             60_0  COME_FROM            26  '26'

 L. 172        60  LOAD_FAST                'dir'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               directory

 L. 173        66  LOAD_FAST                'self'
               68  LOAD_METHOD              set_filter
               70  LOAD_FAST                'dir'
               72  LOAD_FAST                'pat'
               74  CALL_METHOD_2         2  ''
               76  POP_TOP          

 L. 174        78  LOAD_FAST                'names'
               80  LOAD_METHOD              sort
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

 L. 175        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                pardir
               90  BUILD_LIST_1          1 
               92  STORE_FAST               'subdirs'

 L. 176        94  BUILD_LIST_0          0 
               96  STORE_FAST               'matchingfiles'

 L. 177        98  LOAD_FAST                'names'
              100  GET_ITER         
            102_0  COME_FROM           166  '166'
            102_1  COME_FROM           154  '154'
            102_2  COME_FROM           142  '142'
              102  FOR_ITER            168  'to 168'
              104  STORE_FAST               'name'

 L. 178       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              join
              112  LOAD_FAST                'dir'
              114  LOAD_FAST                'name'
              116  CALL_METHOD_2         2  ''
              118  STORE_FAST               'fullname'

 L. 179       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_METHOD              isdir
              126  LOAD_FAST                'fullname'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_FALSE   144  'to 144'

 L. 180       132  LOAD_FAST                'subdirs'
              134  LOAD_METHOD              append
              136  LOAD_FAST                'name'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK           102  'to 102'
            144_0  COME_FROM           130  '130'

 L. 181       144  LOAD_GLOBAL              fnmatch
              146  LOAD_METHOD              fnmatch
              148  LOAD_FAST                'name'
              150  LOAD_FAST                'pat'
              152  CALL_METHOD_2         2  ''
              154  POP_JUMP_IF_FALSE_BACK   102  'to 102'

 L. 182       156  LOAD_FAST                'matchingfiles'
              158  LOAD_METHOD              append
              160  LOAD_FAST                'name'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
              166  JUMP_BACK           102  'to 102'
            168_0  COME_FROM           102  '102'

 L. 183       168  LOAD_FAST                'self'
              170  LOAD_ATTR                dirs
              172  LOAD_METHOD              delete
              174  LOAD_CONST               0
              176  LOAD_GLOBAL              END
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          

 L. 184       182  LOAD_FAST                'subdirs'
              184  GET_ITER         
            186_0  COME_FROM           204  '204'
              186  FOR_ITER            206  'to 206'
              188  STORE_FAST               'name'

 L. 185       190  LOAD_FAST                'self'
              192  LOAD_ATTR                dirs
              194  LOAD_METHOD              insert
              196  LOAD_GLOBAL              END
              198  LOAD_FAST                'name'
              200  CALL_METHOD_2         2  ''
              202  POP_TOP          
              204  JUMP_BACK           186  'to 186'
            206_0  COME_FROM           186  '186'

 L. 186       206  LOAD_FAST                'self'
              208  LOAD_ATTR                files
              210  LOAD_METHOD              delete
              212  LOAD_CONST               0
              214  LOAD_GLOBAL              END
              216  CALL_METHOD_2         2  ''
              218  POP_TOP          

 L. 187       220  LOAD_FAST                'matchingfiles'
              222  GET_ITER         
            224_0  COME_FROM           242  '242'
              224  FOR_ITER            244  'to 244'
              226  STORE_FAST               'name'

 L. 188       228  LOAD_FAST                'self'
              230  LOAD_ATTR                files
              232  LOAD_METHOD              insert
              234  LOAD_GLOBAL              END
              236  LOAD_FAST                'name'
              238  CALL_METHOD_2         2  ''
              240  POP_TOP          
              242  JUMP_BACK           224  'to 224'
            244_0  COME_FROM           224  '224'

 L. 189       244  LOAD_GLOBAL              os
              246  LOAD_ATTR                path
              248  LOAD_METHOD              split
              250  LOAD_FAST                'self'
              252  LOAD_METHOD              get_selection
              254  CALL_METHOD_0         0  ''
              256  CALL_METHOD_1         1  ''
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'head'
              262  STORE_FAST               'tail'

 L. 190       264  LOAD_FAST                'tail'
              266  LOAD_GLOBAL              os
              268  LOAD_ATTR                curdir
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   280  'to 280'

 L. 190       276  LOAD_STR                 ''
              278  STORE_FAST               'tail'
            280_0  COME_FROM           272  '272'

 L. 191       280  LOAD_FAST                'self'
              282  LOAD_METHOD              set_selection
              284  LOAD_FAST                'tail'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 54

    def get_filter(self):
        filter = self.filter.get()
        filter = os.path.expanduser(filter)
        if filter[-1:] == os.sep or (os.path.isdir(filter)):
            filter = os.path.join(filter, '*')
        return os.path.split(filter)

    def get_selection(self):
        file = self.selection.get()
        file = os.path.expanduser(file)
        return file

    def cancel_command(self, event=None):
        self.quit()

    def set_filter(self, dir, pat):
        if not os.path.isabs(dir):
            try:
                pwd = os.getcwd()
            except OSError:
                pwd = None
            else:
                if pwd:
                    dir = os.path.join(pwd, dir)
                    dir = os.path.normpath(dir)
        self.filter.delete(0, END)
        self.filter.insert(END, os.path.join(dir or os.curdir, pat or '*'))

    def set_selection(self, file):
        self.selection.delete(0, END)
        self.selection.insert(END, os.path.join(self.directory, file))


class LoadFileDialog(FileDialog):
    __doc__ = 'File selection dialog which checks that the file exists.'
    title = 'Load File Selection Dialog'

    def ok_command(self):
        file = self.get_selection()
        if not os.path.isfile(file):
            self.master.bell()
        else:
            self.quit(file)


class SaveFileDialog(FileDialog):
    __doc__ = 'File selection dialog which checks that the file may be created.'
    title = 'Save File Selection Dialog'

    def ok_command(self):
        file = self.get_selection()
        if os.path.exists(file):
            if os.path.isdir(file):
                self.master.bell()
                return
            d = Dialog((self.top), title='Overwrite Existing File Question',
              text=('Overwrite existing file %r?' % (file,)),
              bitmap='questhead',
              default=1,
              strings=('Yes', 'Cancel'))
            if d.num != 0:
                return
        else:
            head, tail = os.path.split(file)
            if not os.path.isdir(head):
                self.master.bell()
                return
        self.quit(file)


class _Dialog(commondialog.Dialog):

    def _fixoptions(self):
        try:
            self.options['filetypes'] = tuple(self.options['filetypes'])
        except KeyError:
            pass

    def _fixresult(self, widget, result):
        if result:
            try:
                result = result.string
            except AttributeError:
                pass
            else:
                path, file = os.path.split(result)
                self.options['initialdir'] = path
                self.options['initialfile'] = file
            self.filename = result
            return result


class Open(_Dialog):
    __doc__ = 'Ask for a filename to open'
    command = 'tk_getOpenFile'

    def _fixresult(self, widget, result):
        if isinstance(result, tuple):
            result = tuple([getattr(r, 'string', r) for r in result])
            if result:
                path, file = os.path.split(result[0])
                self.options['initialdir'] = path
            return result
        if not widget.tk.wantobjects():
            if 'multiple' in self.options:
                return self._fixresult(widget, widget.tk.splitlist(result))
        return _Dialog._fixresult(self, widget, result)


class SaveAs(_Dialog):
    __doc__ = 'Ask for a filename to save as'
    command = 'tk_getSaveFile'


class Directory(commondialog.Dialog):
    __doc__ = 'Ask for a directory'
    command = 'tk_chooseDirectory'

    def _fixresult(self, widget, result):
        if result:
            try:
                result = result.string
            except AttributeError:
                pass
            else:
                self.options['initialdir'] = result
            self.directory = result
            return result


def askopenfilename(**options):
    """Ask for a filename to open"""
    return Open(**options).show()


def asksaveasfilename(**options):
    """Ask for a filename to save as"""
    return SaveAs(**options).show()


def askopenfilenames(**options):
    """Ask for multiple filenames to open

    Returns a list of filenames or empty list if
    cancel button selected
    """
    options['multiple'] = 1
    return Open(**options).show()


def askopenfile(mode='r', **options):
    """Ask for a filename to open, and returned the opened file"""
    filename = Open(**options).show()
    if filename:
        return open(filename, mode)


def askopenfiles(mode='r', **options):
    """Ask for multiple filenames and return the open file
    objects

    returns a list of open file objects or an empty list if
    cancel selected
    """
    files = askopenfilenames(**options)
    if files:
        ofiles = []
        for filename in files:
            ofiles.append(open(filename, mode))
        else:
            files = ofiles

    return files


def asksaveasfile(mode='w', **options):
    """Ask for a filename to save as, and returned the opened file"""
    filename = SaveAs(**options).show()
    if filename:
        return open(filename, mode)


def askdirectory(**options):
    """Ask for a directory, and return the file name"""
    return Directory(**options).show()


def test():
    """Simple test program."""
    root = Tk()
    root.withdraw()
    fd = LoadFileDialog(root)
    loadfile = fd.go(key='test')
    fd = SaveFileDialog(root)
    savefile = fd.go(key='test')
    print(loadfile, savefile)
    enc = 'utf-8'
    import sys
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
        enc = locale.nl_langinfo(locale.CODESET)
    except (ImportError, AttributeError):
        pass
    else:
        openfilename = askopenfilename(filetypes=[('all files', '*')])
        try:
            fp = open(openfilename, 'r')
            fp.close()
        except:
            print('Could not open File: ')
            print(sys.exc_info()[1])
        else:
            print('open', openfilename.encode(enc))
            saveasfilename = asksaveasfilename()
            print('saveas', saveasfilename.encode(enc))


if __name__ == '__main__':
    test()