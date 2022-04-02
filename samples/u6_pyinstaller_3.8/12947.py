# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: pyperclip\__init__.py
"""
Pyperclip

A cross-platform clipboard module for Python, with copy & paste functions for plain text.
By Al Sweigart al@inventwithpython.com
BSD License

Usage:
  import pyperclip
  pyperclip.copy('The text to be copied to the clipboard.')
  spam = pyperclip.paste()

  if not pyperclip.is_available():
    print("Copy functionality unavailable!")

On Windows, no additional modules are needed.
On Mac, the pyobjc module is used, falling back to the pbcopy and pbpaste cli
    commands. (These commands should come with OS X.).
On Linux, install xclip, xsel, or wl-clipboard (for "wayland" sessions) via package manager.
For example, in Debian:
    sudo apt-get install xclip
    sudo apt-get install xsel
    sudo apt-get install wl-clipboard

Otherwise on Linux, you will need the gtk or PyQt5/PyQt4 modules installed.

gtk and PyQt4 modules are not available for Python 3,
and this module does not work with PyGObject yet.

Note: There seems to be a way to get gtk on Python 3, according to:
    https://askubuntu.com/questions/697397/python3-is-not-supporting-gtk-module

Cygwin is currently not supported.

Security Note: This module runs programs with these names:
    - which
    - where
    - pbcopy
    - pbpaste
    - xclip
    - xsel
    - wl-copy/wl-paste
    - klipper
    - qdbus
A malicious user could rename or add programs with these names, tricking
Pyperclip into running them with whatever permissions the Python process has.

"""
__version__ = '1.8.2'
import contextlib, ctypes, os, platform, subprocess, sys, time, warnings
from ctypes import c_size_t, sizeof, c_wchar_p, get_errno, c_wchar
HAS_DISPLAY = os.getenv('DISPLAY', False)
EXCEPT_MSG = '\n    Pyperclip could not find a copy/paste mechanism for your system.\n    For more information, please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error '
PY2 = sys.version_info[0] == 2
STR_OR_UNICODE = unicode if PY2 else str
ENCODING = 'utf-8'
try:
    from shutil import which as _executable_exists
except ImportError:
    if platform.system() == 'Windows':
        WHICH_CMD = 'where'
    else:
        WHICH_CMD = 'which'

    def _executable_exists(name):
        return subprocess.call([WHICH_CMD, name], stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE)) == 0


else:

    class PyperclipException(RuntimeError):
        pass


    class PyperclipWindowsException(PyperclipException):

        def __init__(self, message):
            message += ' (%s)' % ctypes.WinError()
            super(PyperclipWindowsException, self).__init__(message)


    class PyperclipTimeoutException(PyperclipException):
        pass


    def _stringifyText(text):
        if PY2:
            acceptedTypes = (
             unicode, str, int, float, bool)
        else:
            acceptedTypes = (
             str, int, float, bool)
        if not isinstance(text, acceptedTypes):
            raise PyperclipException('only str, int, float, and bool values can be copied to the clipboard, not %s' % text.__class__.__name__)
        return STR_OR_UNICODE(text)


    def init_osx_pbcopy_clipboard():

        def copy_osx_pbcopy(text):
            text = _stringifyText(text)
            p = subprocess.Popen(['pbcopy', 'w'], stdin=(subprocess.PIPE),
              close_fds=True)
            p.communicate(input=(text.encode(ENCODING)))

        def paste_osx_pbcopy():
            p = subprocess.Popen(['pbpaste', 'r'], stdout=(subprocess.PIPE),
              close_fds=True)
            stdout, stderr = p.communicate()
            return stdout.decode(ENCODING)

        return (
         copy_osx_pbcopy, paste_osx_pbcopy)


    def init_osx_pyobjc_clipboard():

        def copy_osx_pyobjc(text):
            """Copy string argument to clipboard"""
            text = _stringifyText(text)
            newStr = Foundation.NSString.stringWithString_(text).nsstring()
            newData = newStr.dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
            board = AppKit.NSPasteboard.generalPasteboard()
            board.declareTypes_owner_([AppKit.NSStringPboardType], None)
            board.setData_forType_(newData, AppKit.NSStringPboardType)

        def paste_osx_pyobjc():
            """Returns contents of clipboard"""
            board = AppKit.NSPasteboard.generalPasteboard()
            content = board.stringForType_(AppKit.NSStringPboardType)
            return content

        return (
         copy_osx_pyobjc, paste_osx_pyobjc)


    def init_gtk_clipboard():
        global gtk
        import gtk

        def copy_gtk(text):
            global cb
            text = _stringifyText(text)
            cb = gtk.Clipboard()
            cb.set_text(text)
            cb.store()

        def paste_gtk():
            clipboardContents = gtk.Clipboard().wait_for_text()
            if clipboardContents is None:
                return ''
            return clipboardContents

        return (
         copy_gtk, paste_gtk)


    def init_qt_clipboard():
        global QApplication
        try:
            from qtpy.QtWidgets import QApplication
        except:
            try:
                from PyQt5.QtWidgets import QApplication
            except:
                from PyQt4.QtGui import QApplication

        else:
            app = QApplication.instance()
            if app is None:
                app = QApplication([])

            def copy_qt(text):
                text = _stringifyText(text)
                cb = app.clipboard()
                cb.setText(text)

            def paste_qt():
                cb = app.clipboard()
                return STR_OR_UNICODE(cb.text())

            return (
             copy_qt, paste_qt)


    def init_xclip_clipboard():
        DEFAULT_SELECTION = 'c'
        PRIMARY_SELECTION = 'p'

        def copy_xclip(text, primary=False):
            text = _stringifyText(text)
            selection = DEFAULT_SELECTION
            if primary:
                selection = PRIMARY_SELECTION
            p = subprocess.Popen(['xclip', '-selection', selection], stdin=(subprocess.PIPE),
              close_fds=True)
            p.communicate(input=(text.encode(ENCODING)))

        def paste_xclip(primary=False):
            selection = DEFAULT_SELECTION
            if primary:
                selection = PRIMARY_SELECTION
            p = subprocess.Popen(['xclip', '-selection', selection, '-o'], stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE),
              close_fds=True)
            stdout, stderr = p.communicate()
            return stdout.decode(ENCODING)

        return (
         copy_xclip, paste_xclip)


    def init_xsel_clipboard():
        DEFAULT_SELECTION = '-b'
        PRIMARY_SELECTION = '-p'

        def copy_xsel(text, primary=False):
            text = _stringifyText(text)
            selection_flag = DEFAULT_SELECTION
            if primary:
                selection_flag = PRIMARY_SELECTION
            p = subprocess.Popen(['xsel', selection_flag, '-i'], stdin=(subprocess.PIPE),
              close_fds=True)
            p.communicate(input=(text.encode(ENCODING)))

        def paste_xsel(primary=False):
            selection_flag = DEFAULT_SELECTION
            if primary:
                selection_flag = PRIMARY_SELECTION
            p = subprocess.Popen(['xsel', selection_flag, '-o'], stdout=(subprocess.PIPE),
              close_fds=True)
            stdout, stderr = p.communicate()
            return stdout.decode(ENCODING)

        return (
         copy_xsel, paste_xsel)


    def init_wl_clipboard():
        PRIMARY_SELECTION = '-p'

        def copy_wl(text, primary=False):
            text = _stringifyText(text)
            args = ['wl-copy']
            if primary:
                args.append(PRIMARY_SELECTION)
            elif not text:
                args.append('--clear')
                subprocess.check_call(args, close_fds=True)
            else:
                p = subprocess.Popen(args, stdin=(subprocess.PIPE), close_fds=True)
                p.communicate(input=(text.encode(ENCODING)))

        def paste_wl(primary=False):
            args = ['wl-paste', '-n']
            if primary:
                args.append(PRIMARY_SELECTION)
            p = subprocess.Popen(args, stdout=(subprocess.PIPE), close_fds=True)
            stdout, _stderr = p.communicate()
            return stdout.decode(ENCODING)

        return (
         copy_wl, paste_wl)


    def init_klipper_clipboard():

        def copy_klipper(text):
            text = _stringifyText(text)
            p = subprocess.Popen([
             'qdbus', 'org.kde.klipper', '/klipper', 'setClipboardContents',
             text.encode(ENCODING)],
              stdin=(subprocess.PIPE),
              close_fds=True)
            p.communicate(input=None)

        def paste_klipper():
            p = subprocess.Popen([
             'qdbus', 'org.kde.klipper', '/klipper', 'getClipboardContents'],
              stdout=(subprocess.PIPE),
              close_fds=True)
            stdout, stderr = p.communicate()
            clipboardContents = stdout.decode(ENCODING)
            assert len(clipboardContents) > 0
            assert clipboardContents.endswith('\n')
            if clipboardContents.endswith('\n'):
                clipboardContents = clipboardContents[:-1]
            return clipboardContents

        return (
         copy_klipper, paste_klipper)


    def init_dev_clipboard_clipboard():

        def copy_dev_clipboard(text):
            text = _stringifyText(text)
            if text == '':
                warnings.warn('Pyperclip cannot copy a blank string to the clipboard on Cygwin. This is effectively a no-op.')
            if '\r' in text:
                warnings.warn('Pyperclip cannot handle \\r characters on Cygwin.')
            fo = open('/dev/clipboard', 'wt')
            fo.write(text)
            fo.close()

        def paste_dev_clipboard():
            fo = open('/dev/clipboard', 'rt')
            content = fo.read()
            fo.close()
            return content

        return (
         copy_dev_clipboard, paste_dev_clipboard)


    def init_no_clipboard():

        class ClipboardUnavailable(object):

            def __call__(self, *args, **kwargs):
                raise PyperclipException(EXCEPT_MSG)

            if PY2:

                def __nonzero__(self):
                    return False

            else:

                def __bool__(self):
                    return False

        return (ClipboardUnavailable(), ClipboardUnavailable())


    class CheckedCall(object):

        def __init__(self, f):
            super(CheckedCall, self).__setattr__('f', f)

        def __call__(self, *args):
            ret = (self.f)(*args)
            if not ret:
                if get_errno():
                    raise PyperclipWindowsException('Error calling ' + self.f.__name__)
            return ret

        def __setattr__(self, key, value):
            setattr(self.f, key, value)


    def init_windows_clipboard():
        global BOOL
        global DWORD
        global HANDLE
        global HGLOBAL
        global HINSTANCE
        global HMENU
        global HWND
        global INT
        global LPCSTR
        global LPVOID
        global UINT
        from ctypes.wintypes import HGLOBAL, LPVOID, DWORD, LPCSTR, INT, HWND, HINSTANCE, HMENU, BOOL, UINT, HANDLE
        windll = ctypes.windll
        msvcrt = ctypes.CDLL('msvcrt')
        safeCreateWindowExA = CheckedCall(windll.user32.CreateWindowExA)
        safeCreateWindowExA.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, INT, INT,
         INT, INT, HWND, HMENU, HINSTANCE, LPVOID]
        safeCreateWindowExA.restype = HWND
        safeDestroyWindow = CheckedCall(windll.user32.DestroyWindow)
        safeDestroyWindow.argtypes = [HWND]
        safeDestroyWindow.restype = BOOL
        OpenClipboard = windll.user32.OpenClipboard
        OpenClipboard.argtypes = [HWND]
        OpenClipboard.restype = BOOL
        safeCloseClipboard = CheckedCall(windll.user32.CloseClipboard)
        safeCloseClipboard.argtypes = []
        safeCloseClipboard.restype = BOOL
        safeEmptyClipboard = CheckedCall(windll.user32.EmptyClipboard)
        safeEmptyClipboard.argtypes = []
        safeEmptyClipboard.restype = BOOL
        safeGetClipboardData = CheckedCall(windll.user32.GetClipboardData)
        safeGetClipboardData.argtypes = [UINT]
        safeGetClipboardData.restype = HANDLE
        safeSetClipboardData = CheckedCall(windll.user32.SetClipboardData)
        safeSetClipboardData.argtypes = [UINT, HANDLE]
        safeSetClipboardData.restype = HANDLE
        safeGlobalAlloc = CheckedCall(windll.kernel32.GlobalAlloc)
        safeGlobalAlloc.argtypes = [UINT, c_size_t]
        safeGlobalAlloc.restype = HGLOBAL
        safeGlobalLock = CheckedCall(windll.kernel32.GlobalLock)
        safeGlobalLock.argtypes = [HGLOBAL]
        safeGlobalLock.restype = LPVOID
        safeGlobalUnlock = CheckedCall(windll.kernel32.GlobalUnlock)
        safeGlobalUnlock.argtypes = [HGLOBAL]
        safeGlobalUnlock.restype = BOOL
        wcslen = CheckedCall(msvcrt.wcslen)
        wcslen.argtypes = [c_wchar_p]
        wcslen.restype = UINT
        GMEM_MOVEABLE = 2
        CF_UNICODETEXT = 13

        @contextlib.contextmanager
        def window():
            hwnd = safeCreateWindowExA(0, b'STATIC', None, 0, 0, 0, 0, 0, None, None, None, None)
            try:
                (yield hwnd)
            finally:
                safeDestroyWindow(hwnd)

        @contextlib.contextmanager
        def clipboard(hwnd):
            t = time.time() + 0.5
            success = False
            while time.time() < t:
                success = OpenClipboard(hwnd)
                if success:
                    break
                time.sleep(0.01)

            if not success:
                raise PyperclipWindowsException('Error calling OpenClipboard')
            try:
                (yield)
            finally:
                safeCloseClipboard()

        def copy_windows(text):
            text = _stringifyText(text)
            with window() as (hwnd):
                with clipboard(hwnd):
                    safeEmptyClipboard()
                    if text:
                        count = wcslen(text) + 1
                        handle = safeGlobalAlloc(GMEM_MOVEABLE, count * sizeof(c_wchar))
                        locked_handle = safeGlobalLock(handle)
                        ctypes.memmove(c_wchar_p(locked_handle), c_wchar_p(text), count * sizeof(c_wchar))
                        safeGlobalUnlock(handle)
                        safeSetClipboardData(CF_UNICODETEXT, handle)

        def paste_windows--- This code section failed: ---

 L. 490         0  LOAD_DEREF               'clipboard'
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           58  'to 58'
                8  POP_TOP          

 L. 491        10  LOAD_DEREF               'safeGetClipboardData'
               12  LOAD_DEREF               'CF_UNICODETEXT'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'handle'

 L. 492        18  LOAD_FAST                'handle'
               20  POP_JUMP_IF_TRUE     36  'to 36'

 L. 497        22  POP_BLOCK        
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  LOAD_STR                 ''
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'

 L. 498        36  LOAD_GLOBAL              c_wchar_p
               38  LOAD_FAST                'handle'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_ATTR                value
               44  POP_BLOCK        
               46  ROT_TWO          
               48  BEGIN_FINALLY    
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  POP_FINALLY           0  ''
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH        6  '6'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

        return (
         copy_windows, paste_windows)


    def init_wsl_clipboard():

        def copy_wsl(text):
            text = _stringifyText(text)
            p = subprocess.Popen(['clip.exe'], stdin=(subprocess.PIPE),
              close_fds=True)
            p.communicate(input=(text.encode(ENCODING)))

        def paste_wsl():
            p = subprocess.Popen(['powershell.exe', '-command', 'Get-Clipboard'], stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE),
              close_fds=True)
            stdout, stderr = p.communicate()
            return stdout[:-2].decode(ENCODING)

        return (
         copy_wsl, paste_wsl)


    def determine_clipboard--- This code section failed: ---

 L. 532         0  LOAD_STR                 'cygwin'
                2  LOAD_GLOBAL              platform
                4  LOAD_METHOD              system
                6  CALL_METHOD_0         0  ''
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    46  'to 46'

 L. 535        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              exists
               22  LOAD_STR                 '/dev/clipboard'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_FALSE    74  'to 74'

 L. 536        28  LOAD_GLOBAL              warnings
               30  LOAD_METHOD              warn
               32  LOAD_STR                 "Pyperclip's support for Cygwin is not perfect, see https://github.com/asweigart/pyperclip/issues/55"
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 537        38  LOAD_GLOBAL              init_dev_clipboard_clipboard
               40  CALL_FUNCTION_0       0  ''
               42  RETURN_VALUE     
               44  JUMP_FORWARD         74  'to 74'
             46_0  COME_FROM            14  '14'

 L. 540        46  LOAD_GLOBAL              os
               48  LOAD_ATTR                name
               50  LOAD_STR                 'nt'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_TRUE     68  'to 68'
               56  LOAD_GLOBAL              platform
               58  LOAD_METHOD              system
               60  CALL_METHOD_0         0  ''
               62  LOAD_STR                 'Windows'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    74  'to 74'
             68_0  COME_FROM            54  '54'

 L. 541        68  LOAD_GLOBAL              init_windows_clipboard
               70  CALL_FUNCTION_0       0  ''
               72  RETURN_VALUE     
             74_0  COME_FROM            66  '66'
             74_1  COME_FROM            44  '44'
             74_2  COME_FROM            26  '26'

 L. 543        74  LOAD_GLOBAL              platform
               76  LOAD_METHOD              system
               78  CALL_METHOD_0         0  ''
               80  LOAD_STR                 'Linux'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   154  'to 154'
               86  LOAD_GLOBAL              os
               88  LOAD_ATTR                path
               90  LOAD_METHOD              isfile
               92  LOAD_STR                 '/proc/version'
               94  CALL_METHOD_1         1  ''
               96  POP_JUMP_IF_FALSE   154  'to 154'

 L. 544        98  LOAD_GLOBAL              open
              100  LOAD_STR                 '/proc/version'
              102  LOAD_STR                 'r'
              104  CALL_FUNCTION_2       2  ''
              106  SETUP_WITH          148  'to 148'
              108  STORE_FAST               'f'

 L. 545       110  LOAD_STR                 'microsoft'
              112  LOAD_FAST                'f'
              114  LOAD_METHOD              read
              116  CALL_METHOD_0         0  ''
              118  LOAD_METHOD              lower
              120  CALL_METHOD_0         0  ''
              122  COMPARE_OP               in
              124  POP_JUMP_IF_FALSE   144  'to 144'

 L. 546       126  LOAD_GLOBAL              init_wsl_clipboard
              128  CALL_FUNCTION_0       0  ''
              130  POP_BLOCK        
              132  ROT_TWO          
              134  BEGIN_FINALLY    
              136  WITH_CLEANUP_START
              138  WITH_CLEANUP_FINISH
              140  POP_FINALLY           0  ''
              142  RETURN_VALUE     
            144_0  COME_FROM           124  '124'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM_WITH      106  '106'
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      
            154_0  COME_FROM            96  '96'
            154_1  COME_FROM            84  '84'

 L. 549       154  LOAD_GLOBAL              os
              156  LOAD_ATTR                name
              158  LOAD_STR                 'mac'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_TRUE    176  'to 176'
              164  LOAD_GLOBAL              platform
              166  LOAD_METHOD              system
              168  CALL_METHOD_0         0  ''
              170  LOAD_STR                 'Darwin'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   230  'to 230'
            176_0  COME_FROM           162  '162'

 L. 550       176  SETUP_FINALLY       198  'to 198'

 L. 551       178  LOAD_CONST               0
              180  LOAD_CONST               None
              182  IMPORT_NAME              Foundation
              184  STORE_GLOBAL             Foundation

 L. 552       186  LOAD_CONST               0
              188  LOAD_CONST               None
              190  IMPORT_NAME              AppKit
              192  STORE_GLOBAL             AppKit
              194  POP_BLOCK        
              196  JUMP_FORWARD        224  'to 224'
            198_0  COME_FROM_FINALLY   176  '176'

 L. 553       198  DUP_TOP          
              200  LOAD_GLOBAL              ImportError
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   222  'to 222'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L. 554       212  LOAD_GLOBAL              init_osx_pbcopy_clipboard
              214  CALL_FUNCTION_0       0  ''
              216  ROT_FOUR         
              218  POP_EXCEPT       
              220  RETURN_VALUE     
            222_0  COME_FROM           204  '204'
              222  END_FINALLY      
            224_0  COME_FROM           196  '196'

 L. 556       224  LOAD_GLOBAL              init_osx_pyobjc_clipboard
              226  CALL_FUNCTION_0       0  ''
              228  RETURN_VALUE     
            230_0  COME_FROM           174  '174'

 L. 559       230  LOAD_GLOBAL              HAS_DISPLAY
          232_234  POP_JUMP_IF_FALSE   504  'to 504'

 L. 560       236  SETUP_FINALLY       250  'to 250'

 L. 561       238  LOAD_CONST               0
              240  LOAD_CONST               None
              242  IMPORT_NAME              gtk
              244  STORE_GLOBAL             gtk
              246  POP_BLOCK        
              248  JUMP_FORWARD        272  'to 272'
            250_0  COME_FROM_FINALLY   236  '236'

 L. 562       250  DUP_TOP          
              252  LOAD_GLOBAL              ImportError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   270  'to 270'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L. 563       266  POP_EXCEPT       
              268  JUMP_FORWARD        278  'to 278'
            270_0  COME_FROM           256  '256'
              270  END_FINALLY      
            272_0  COME_FROM           248  '248'

 L. 565       272  LOAD_GLOBAL              init_gtk_clipboard
              274  CALL_FUNCTION_0       0  ''
              276  RETURN_VALUE     
            278_0  COME_FROM           268  '268'

 L. 568       278  LOAD_GLOBAL              os
              280  LOAD_ATTR                environ
              282  LOAD_METHOD              get
              284  LOAD_STR                 'WAYLAND_DISPLAY'
              286  CALL_METHOD_1         1  ''

 L. 567   288_290  POP_JUMP_IF_FALSE   308  'to 308'

 L. 569       292  LOAD_GLOBAL              _executable_exists
              294  LOAD_STR                 'wl-copy'
              296  CALL_FUNCTION_1       1  ''

 L. 567   298_300  POP_JUMP_IF_FALSE   308  'to 308'

 L. 571       302  LOAD_GLOBAL              init_wl_clipboard
              304  CALL_FUNCTION_0       0  ''
              306  RETURN_VALUE     
            308_0  COME_FROM           298  '298'
            308_1  COME_FROM           288  '288'

 L. 572       308  LOAD_GLOBAL              _executable_exists
              310  LOAD_STR                 'xsel'
              312  CALL_FUNCTION_1       1  ''
          314_316  POP_JUMP_IF_FALSE   324  'to 324'

 L. 573       318  LOAD_GLOBAL              init_xsel_clipboard
              320  CALL_FUNCTION_0       0  ''
              322  RETURN_VALUE     
            324_0  COME_FROM           314  '314'

 L. 574       324  LOAD_GLOBAL              _executable_exists
              326  LOAD_STR                 'xclip'
              328  CALL_FUNCTION_1       1  ''
          330_332  POP_JUMP_IF_FALSE   340  'to 340'

 L. 575       334  LOAD_GLOBAL              init_xclip_clipboard
              336  CALL_FUNCTION_0       0  ''
              338  RETURN_VALUE     
            340_0  COME_FROM           330  '330'

 L. 576       340  LOAD_GLOBAL              _executable_exists
              342  LOAD_STR                 'klipper'
              344  CALL_FUNCTION_1       1  ''
          346_348  POP_JUMP_IF_FALSE   366  'to 366'
              350  LOAD_GLOBAL              _executable_exists
              352  LOAD_STR                 'qdbus'
              354  CALL_FUNCTION_1       1  ''
          356_358  POP_JUMP_IF_FALSE   366  'to 366'

 L. 577       360  LOAD_GLOBAL              init_klipper_clipboard
              362  CALL_FUNCTION_0       0  ''
              364  RETURN_VALUE     
            366_0  COME_FROM           356  '356'
            366_1  COME_FROM           346  '346'

 L. 579       366  SETUP_FINALLY       380  'to 380'

 L. 582       368  LOAD_CONST               0
              370  LOAD_CONST               None
              372  IMPORT_NAME              qtpy
              374  STORE_GLOBAL             qtpy
              376  POP_BLOCK        
              378  JUMP_FORWARD        498  'to 498'
            380_0  COME_FROM_FINALLY   366  '366'

 L. 583       380  DUP_TOP          
              382  LOAD_GLOBAL              ImportError
              384  COMPARE_OP               exception-match
          386_388  POP_JUMP_IF_FALSE   496  'to 496'
              390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L. 585       396  SETUP_FINALLY       410  'to 410'

 L. 586       398  LOAD_CONST               0
              400  LOAD_CONST               None
              402  IMPORT_NAME              PyQt5
              404  STORE_GLOBAL             PyQt5
              406  POP_BLOCK        
              408  JUMP_FORWARD        482  'to 482'
            410_0  COME_FROM_FINALLY   396  '396'

 L. 587       410  DUP_TOP          
              412  LOAD_GLOBAL              ImportError
              414  COMPARE_OP               exception-match
          416_418  POP_JUMP_IF_FALSE   480  'to 480'
              420  POP_TOP          
              422  POP_TOP          
              424  POP_TOP          

 L. 588       426  SETUP_FINALLY       440  'to 440'

 L. 589       428  LOAD_CONST               0
              430  LOAD_CONST               None
              432  IMPORT_NAME              PyQt4
              434  STORE_GLOBAL             PyQt4
              436  POP_BLOCK        
              438  JUMP_FORWARD        462  'to 462'
            440_0  COME_FROM_FINALLY   426  '426'

 L. 590       440  DUP_TOP          
              442  LOAD_GLOBAL              ImportError
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   460  'to 460'
              450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 591       456  POP_EXCEPT       
              458  JUMP_FORWARD        476  'to 476'
            460_0  COME_FROM           446  '446'
              460  END_FINALLY      
            462_0  COME_FROM           438  '438'

 L. 593       462  LOAD_GLOBAL              init_qt_clipboard
              464  CALL_FUNCTION_0       0  ''
              466  ROT_FOUR         
              468  POP_EXCEPT       
              470  ROT_FOUR         
              472  POP_EXCEPT       
              474  RETURN_VALUE     
            476_0  COME_FROM           458  '458'
              476  POP_EXCEPT       
              478  JUMP_FORWARD        492  'to 492'
            480_0  COME_FROM           416  '416'
              480  END_FINALLY      
            482_0  COME_FROM           408  '408'

 L. 595       482  LOAD_GLOBAL              init_qt_clipboard
              484  CALL_FUNCTION_0       0  ''
              486  ROT_FOUR         
              488  POP_EXCEPT       
              490  RETURN_VALUE     
            492_0  COME_FROM           478  '478'
              492  POP_EXCEPT       
              494  JUMP_FORWARD        504  'to 504'
            496_0  COME_FROM           386  '386'
              496  END_FINALLY      
            498_0  COME_FROM           378  '378'

 L. 597       498  LOAD_GLOBAL              init_qt_clipboard
              500  CALL_FUNCTION_0       0  ''
              502  RETURN_VALUE     
            504_0  COME_FROM           494  '494'
            504_1  COME_FROM           232  '232'

 L. 600       504  LOAD_GLOBAL              init_no_clipboard
              506  CALL_FUNCTION_0       0  ''
              508  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 132


    def set_clipboard(clipboard):
        """
    Explicitly sets the clipboard mechanism. The "clipboard mechanism" is how
    the copy() and paste() functions interact with the operating system to
    implement the copy/paste feature. The clipboard parameter must be one of:
        - pbcopy
        - pbobjc (default on Mac OS X)
        - gtk
        - qt
        - xclip
        - xsel
        - klipper
        - windows (default on Windows)
        - no (this is what is set when no clipboard mechanism can be found)
    """
        global copy
        global paste
        clipboard_types = {'pbcopy':init_osx_pbcopy_clipboard, 
         'pyobjc':init_osx_pyobjc_clipboard, 
         'gtk':init_gtk_clipboard, 
         'qt':init_qt_clipboard, 
         'xclip':init_xclip_clipboard, 
         'xsel':init_xsel_clipboard, 
         'wl-clipboard':init_wl_clipboard, 
         'klipper':init_klipper_clipboard, 
         'windows':init_windows_clipboard, 
         'no':init_no_clipboard}
        if clipboard not in clipboard_types:
            raise ValueError('Argument must be one of %s' % ', '.join([repr(_) for _ in clipboard_types.keys()]))
        copy, paste = clipboard_types[clipboard]()


    def lazy_load_stub_copy(text):
        """
    A stub function for copy(), which will load the real copy() function when
    called so that the real copy() function is used for later calls.

    This allows users to import pyperclip without having determine_clipboard()
    automatically run, which will automatically select a clipboard mechanism.
    This could be a problem if it selects, say, the memory-heavy PyQt4 module
    but the user was just going to immediately call set_clipboard() to use a
    different clipboard mechanism.

    The lazy loading this stub function implements gives the user a chance to
    call set_clipboard() to pick another clipboard mechanism. Or, if the user
    simply calls copy() or paste() without calling set_clipboard() first,
    will fall back on whatever clipboard mechanism that determine_clipboard()
    automatically chooses.
    """
        global copy
        global paste
        copy, paste = determine_clipboard()
        return copy(text)


    def lazy_load_stub_paste():
        """
    A stub function for paste(), which will load the real paste() function when
    called so that the real paste() function is used for later calls.

    This allows users to import pyperclip without having determine_clipboard()
    automatically run, which will automatically select a clipboard mechanism.
    This could be a problem if it selects, say, the memory-heavy PyQt4 module
    but the user was just going to immediately call set_clipboard() to use a
    different clipboard mechanism.

    The lazy loading this stub function implements gives the user a chance to
    call set_clipboard() to pick another clipboard mechanism. Or, if the user
    simply calls copy() or paste() without calling set_clipboard() first,
    will fall back on whatever clipboard mechanism that determine_clipboard()
    automatically chooses.
    """
        global copy
        global paste
        copy, paste = determine_clipboard()
        return paste()


    def is_available():
        return copy != lazy_load_stub_copy and paste != lazy_load_stub_paste


    copy, paste = lazy_load_stub_copy, lazy_load_stub_paste

    def waitForPaste(timeout=None):
        """This function call blocks until a non-empty text string exists on the
    clipboard. It returns this text.

    This function raises PyperclipTimeoutException if timeout was set to
    a number of seconds that has elapsed without non-empty text being put on
    the clipboard."""
        startTime = time.time()
        while True:
            clipboardText = paste()
            if clipboardText != '':
                return clipboardText
            time.sleep(0.01)
            if timeout is not None and time.time() > startTime + timeout:
                raise PyperclipTimeoutException('waitForPaste() timed out after ' + str(timeout) + ' seconds.')


    def waitForNewPaste(timeout=None):
        """This function call blocks until a new text string exists on the
    clipboard that is different from the text that was there when the function
    was first called. It returns this text.

    This function raises PyperclipTimeoutException if timeout was set to
    a number of seconds that has elapsed without non-empty text being put on
    the clipboard."""
        startTime = time.time()
        originalText = paste()
        while True:
            currentText = paste()
            if currentText != originalText:
                return currentText
            time.sleep(0.01)
            if timeout is not None and time.time() > startTime + timeout:
                raise PyperclipTimeoutException('waitForNewPaste() timed out after ' + str(timeout) + ' seconds.')


    __all__ = ['copy', 'paste', 'waitForPaste', 'waitForNewPaste', 'set_clipboard', 'determine_clipboard']