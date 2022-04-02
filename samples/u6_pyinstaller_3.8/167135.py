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
On Linux, install xclip or xsel via package manager. For example, in Debian:
    sudo apt-get install xclip
    sudo apt-get install xsel

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
    - klipper
    - qdbus
A malicious user could rename or add programs with these names, tricking
Pyperclip into running them with whatever permissions the Python process has.

"""
__version__ = '1.8.0'
import contextlib, ctypes, os, platform, subprocess, sys, time, warnings
from ctypes import c_size_t, sizeof, c_wchar_p, get_errno, c_wchar
HAS_DISPLAY = os.getenv('DISPLAY', False)
EXCEPT_MSG = '\n    Pyperclip could not find a copy/paste mechanism for your system.\n    For more information, please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error '
PY2 = sys.version_info[0] == 2
STR_OR_UNICODE = unicode if PY2 else str
ENCODING = 'utf-8'
if platform.system() == 'Windows':
    WHICH_CMD = 'where'
else:
    WHICH_CMD = 'which'

def _executable_exists(name):
    return subprocess.call([WHICH_CMD, name], stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE)) == 0


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

 L. 457         0  LOAD_DEREF               'clipboard'
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           58  'to 58'
                8  POP_TOP          

 L. 458        10  LOAD_DEREF               'safeGetClipboardData'
               12  LOAD_DEREF               'CF_UNICODETEXT'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'handle'

 L. 459        18  LOAD_FAST                'handle'
               20  POP_JUMP_IF_TRUE     36  'to 36'

 L. 464        22  POP_BLOCK        
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  LOAD_STR                 ''
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'

 L. 465        36  LOAD_GLOBAL              c_wchar_p
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

 L. 499         0  LOAD_STR                 'cygwin'
                2  LOAD_GLOBAL              platform
                4  LOAD_METHOD              system
                6  CALL_METHOD_0         0  ''
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  COMPARE_OP               in
               14  POP_JUMP_IF_FALSE    46  'to 46'

 L. 502        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              exists
               22  LOAD_STR                 '/dev/clipboard'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_FALSE    74  'to 74'

 L. 503        28  LOAD_GLOBAL              warnings
               30  LOAD_METHOD              warn
               32  LOAD_STR                 "Pyperclip's support for Cygwin is not perfect, see https://github.com/asweigart/pyperclip/issues/55"
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 504        38  LOAD_GLOBAL              init_dev_clipboard_clipboard
               40  CALL_FUNCTION_0       0  ''
               42  RETURN_VALUE     
               44  JUMP_FORWARD         74  'to 74'
             46_0  COME_FROM            14  '14'

 L. 507        46  LOAD_GLOBAL              os
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

 L. 508        68  LOAD_GLOBAL              init_windows_clipboard
               70  CALL_FUNCTION_0       0  ''
               72  RETURN_VALUE     
             74_0  COME_FROM            66  '66'
             74_1  COME_FROM            44  '44'
             74_2  COME_FROM            26  '26'

 L. 510        74  LOAD_GLOBAL              platform
               76  LOAD_METHOD              system
               78  CALL_METHOD_0         0  ''
               80  LOAD_STR                 'Linux'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   138  'to 138'

 L. 511        86  LOAD_GLOBAL              open
               88  LOAD_STR                 '/proc/version'
               90  LOAD_STR                 'r'
               92  CALL_FUNCTION_2       2  ''
               94  SETUP_WITH          132  'to 132'
               96  STORE_FAST               'f'

 L. 512        98  LOAD_STR                 'Microsoft'
              100  LOAD_FAST                'f'
              102  LOAD_METHOD              read
              104  CALL_METHOD_0         0  ''
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 513       110  LOAD_GLOBAL              init_wsl_clipboard
              112  CALL_FUNCTION_0       0  ''
              114  POP_BLOCK        
              116  ROT_TWO          
              118  BEGIN_FINALLY    
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  POP_FINALLY           0  ''
              126  RETURN_VALUE     
            128_0  COME_FROM           108  '108'
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_WITH       94  '94'
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      
            138_0  COME_FROM            84  '84'

 L. 516       138  LOAD_GLOBAL              os
              140  LOAD_ATTR                name
              142  LOAD_STR                 'mac'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_TRUE    160  'to 160'
              148  LOAD_GLOBAL              platform
              150  LOAD_METHOD              system
              152  CALL_METHOD_0         0  ''
              154  LOAD_STR                 'Darwin'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   214  'to 214'
            160_0  COME_FROM           146  '146'

 L. 517       160  SETUP_FINALLY       182  'to 182'

 L. 518       162  LOAD_CONST               0
              164  LOAD_CONST               None
              166  IMPORT_NAME              Foundation
              168  STORE_GLOBAL             Foundation

 L. 519       170  LOAD_CONST               0
              172  LOAD_CONST               None
              174  IMPORT_NAME              AppKit
              176  STORE_GLOBAL             AppKit
              178  POP_BLOCK        
              180  JUMP_FORWARD        208  'to 208'
            182_0  COME_FROM_FINALLY   160  '160'

 L. 520       182  DUP_TOP          
              184  LOAD_GLOBAL              ImportError
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   206  'to 206'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 521       196  LOAD_GLOBAL              init_osx_pbcopy_clipboard
              198  CALL_FUNCTION_0       0  ''
              200  ROT_FOUR         
              202  POP_EXCEPT       
              204  RETURN_VALUE     
            206_0  COME_FROM           188  '188'
              206  END_FINALLY      
            208_0  COME_FROM           180  '180'

 L. 523       208  LOAD_GLOBAL              init_osx_pyobjc_clipboard
              210  CALL_FUNCTION_0       0  ''
              212  RETURN_VALUE     
            214_0  COME_FROM           158  '158'

 L. 526       214  LOAD_GLOBAL              HAS_DISPLAY
          216_218  POP_JUMP_IF_FALSE   458  'to 458'

 L. 527       220  SETUP_FINALLY       234  'to 234'

 L. 528       222  LOAD_CONST               0
              224  LOAD_CONST               None
              226  IMPORT_NAME              gtk
              228  STORE_GLOBAL             gtk
              230  POP_BLOCK        
              232  JUMP_FORWARD        256  'to 256'
            234_0  COME_FROM_FINALLY   220  '220'

 L. 529       234  DUP_TOP          
              236  LOAD_GLOBAL              ImportError
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   254  'to 254'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 530       250  POP_EXCEPT       
              252  JUMP_FORWARD        262  'to 262'
            254_0  COME_FROM           240  '240'
              254  END_FINALLY      
            256_0  COME_FROM           232  '232'

 L. 532       256  LOAD_GLOBAL              init_gtk_clipboard
              258  CALL_FUNCTION_0       0  ''
              260  RETURN_VALUE     
            262_0  COME_FROM           252  '252'

 L. 534       262  LOAD_GLOBAL              _executable_exists
              264  LOAD_STR                 'xsel'
              266  CALL_FUNCTION_1       1  ''
          268_270  POP_JUMP_IF_FALSE   278  'to 278'

 L. 535       272  LOAD_GLOBAL              init_xsel_clipboard
              274  CALL_FUNCTION_0       0  ''
              276  RETURN_VALUE     
            278_0  COME_FROM           268  '268'

 L. 536       278  LOAD_GLOBAL              _executable_exists
              280  LOAD_STR                 'xclip'
              282  CALL_FUNCTION_1       1  ''
          284_286  POP_JUMP_IF_FALSE   294  'to 294'

 L. 537       288  LOAD_GLOBAL              init_xclip_clipboard
              290  CALL_FUNCTION_0       0  ''
              292  RETURN_VALUE     
            294_0  COME_FROM           284  '284'

 L. 538       294  LOAD_GLOBAL              _executable_exists
              296  LOAD_STR                 'klipper'
              298  CALL_FUNCTION_1       1  ''
          300_302  POP_JUMP_IF_FALSE   320  'to 320'
              304  LOAD_GLOBAL              _executable_exists
              306  LOAD_STR                 'qdbus'
              308  CALL_FUNCTION_1       1  ''
          310_312  POP_JUMP_IF_FALSE   320  'to 320'

 L. 539       314  LOAD_GLOBAL              init_klipper_clipboard
              316  CALL_FUNCTION_0       0  ''
              318  RETURN_VALUE     
            320_0  COME_FROM           310  '310'
            320_1  COME_FROM           300  '300'

 L. 541       320  SETUP_FINALLY       334  'to 334'

 L. 544       322  LOAD_CONST               0
              324  LOAD_CONST               None
              326  IMPORT_NAME              qtpy
              328  STORE_GLOBAL             qtpy
              330  POP_BLOCK        
              332  JUMP_FORWARD        452  'to 452'
            334_0  COME_FROM_FINALLY   320  '320'

 L. 545       334  DUP_TOP          
              336  LOAD_GLOBAL              ImportError
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   450  'to 450'
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 547       350  SETUP_FINALLY       364  'to 364'

 L. 548       352  LOAD_CONST               0
              354  LOAD_CONST               None
              356  IMPORT_NAME              PyQt5
              358  STORE_GLOBAL             PyQt5
              360  POP_BLOCK        
              362  JUMP_FORWARD        436  'to 436'
            364_0  COME_FROM_FINALLY   350  '350'

 L. 549       364  DUP_TOP          
              366  LOAD_GLOBAL              ImportError
              368  COMPARE_OP               exception-match
          370_372  POP_JUMP_IF_FALSE   434  'to 434'
              374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L. 550       380  SETUP_FINALLY       394  'to 394'

 L. 551       382  LOAD_CONST               0
              384  LOAD_CONST               None
              386  IMPORT_NAME              PyQt4
              388  STORE_GLOBAL             PyQt4
              390  POP_BLOCK        
              392  JUMP_FORWARD        416  'to 416'
            394_0  COME_FROM_FINALLY   380  '380'

 L. 552       394  DUP_TOP          
              396  LOAD_GLOBAL              ImportError
              398  COMPARE_OP               exception-match
          400_402  POP_JUMP_IF_FALSE   414  'to 414'
              404  POP_TOP          
              406  POP_TOP          
              408  POP_TOP          

 L. 553       410  POP_EXCEPT       
              412  JUMP_FORWARD        430  'to 430'
            414_0  COME_FROM           400  '400'
              414  END_FINALLY      
            416_0  COME_FROM           392  '392'

 L. 555       416  LOAD_GLOBAL              init_qt_clipboard
              418  CALL_FUNCTION_0       0  ''
              420  ROT_FOUR         
              422  POP_EXCEPT       
              424  ROT_FOUR         
              426  POP_EXCEPT       
              428  RETURN_VALUE     
            430_0  COME_FROM           412  '412'
              430  POP_EXCEPT       
              432  JUMP_FORWARD        446  'to 446'
            434_0  COME_FROM           370  '370'
              434  END_FINALLY      
            436_0  COME_FROM           362  '362'

 L. 557       436  LOAD_GLOBAL              init_qt_clipboard
              438  CALL_FUNCTION_0       0  ''
              440  ROT_FOUR         
              442  POP_EXCEPT       
              444  RETURN_VALUE     
            446_0  COME_FROM           432  '432'
              446  POP_EXCEPT       
              448  JUMP_FORWARD        458  'to 458'
            450_0  COME_FROM           340  '340'
              450  END_FINALLY      
            452_0  COME_FROM           332  '332'

 L. 559       452  LOAD_GLOBAL              init_qt_clipboard
              454  CALL_FUNCTION_0       0  ''
              456  RETURN_VALUE     
            458_0  COME_FROM           448  '448'
            458_1  COME_FROM           216  '216'

 L. 562       458  LOAD_GLOBAL              init_no_clipboard
              460  CALL_FUNCTION_0       0  ''
              462  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 116


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


__all__ = ['copy', 'paste', 'waitForPaste', 'waitForNewPasteset_clipboard', 'determine_clipboard']