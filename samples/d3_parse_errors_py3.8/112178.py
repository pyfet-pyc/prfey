# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: webbrowser.py
"""Interfaces for launching and remotely controlling Web browsers."""
import os, shlex, shutil, sys, subprocess, threading
__all__ = [
 'Error', 'open', 'open_new', 'open_new_tab', 'get', 'register']

class Error(Exception):
    pass


_lock = threading.RLock()
_browsers = {}
_tryorder = None
_os_preferred_browser = None

def register--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              _lock
                2  SETUP_WITH           80  'to 80'
                4  POP_TOP          

 L.  25         6  LOAD_GLOBAL              _tryorder
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L.  26        14  LOAD_GLOBAL              register_standard_browsers
               16  CALL_FUNCTION_0       0  ''
               18  POP_TOP          
             20_0  COME_FROM            12  '12'

 L.  27        20  LOAD_FAST                'klass'
               22  LOAD_FAST                'instance'
               24  BUILD_LIST_2          2 
               26  LOAD_GLOBAL              _browsers
               28  LOAD_FAST                'name'
               30  LOAD_METHOD              lower
               32  CALL_METHOD_0         0  ''
               34  STORE_SUBSCR     

 L.  32        36  LOAD_FAST                'preferred'
               38  POP_JUMP_IF_TRUE     52  'to 52'
               40  LOAD_GLOBAL              _os_preferred_browser
               42  POP_JUMP_IF_FALSE    66  'to 66'
               44  LOAD_FAST                'name'
               46  LOAD_GLOBAL              _os_preferred_browser
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    66  'to 66'
             52_0  COME_FROM            38  '38'

 L.  33        52  LOAD_GLOBAL              _tryorder
               54  LOAD_METHOD              insert
               56  LOAD_CONST               0
               58  LOAD_FAST                'name'
               60  CALL_METHOD_2         2  ''
               62  POP_TOP          
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM            50  '50'
             66_1  COME_FROM            42  '42'

 L.  35        66  LOAD_GLOBAL              _tryorder
               68  LOAD_METHOD              append
               70  LOAD_FAST                'name'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            64  '64'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_WITH        2  '2'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 78


def get(using=None):
    """Return a browser launcher instance appropriate for the environment."""
    global _tryorder
    if _tryorder is None:
        with _lock:
            if _tryorder is None:
                register_standard_browsers()
    if using is not None:
        alternatives = [
         using]
    else:
        alternatives = _tryorder
    for browser in alternatives:
        if '%s' in browser:
            browser = shlex.splitbrowser
            if browser[(-1)] == '&':
                return BackgroundBrowser(browser[:-1])
            return GenericBrowser(browser)
    else:
        try:
            command = _browsers[browser.lower()]
        except KeyError:
            command = _synthesize(browser)
        else:
            if command[1] is not None:
                return command[1]
            if command[0] is not None:
                return command[0]()
            raise Error('could not locate runnable browser')


def open(url, new=0, autoraise=True):
    if _tryorder is None:
        with _lock:
            if _tryorder is None:
                register_standard_browsers()
    for name in _tryorder:
        browser = get(name)
        if browser.open(url, new, autoraise):
            return True
    else:
        return False


def open_new(url):
    return open(url, 1)


def open_new_tab(url):
    return open(url, 2)


def _synthesize(browser, *, preferred=False):
    """Attempt to synthesize a controller base on existing controllers.

    This is useful to create a controller when a user specifies a path to
    an entry in the BROWSER environment variable -- we can copy a general
    controller to operate using a specific installation of the desired
    browser in this way.

    If we can't create a controller in this way, or if there is no
    executable for the requested browser, return [None, None].

    """
    cmd = browser.split()[0]
    if not shutil.whichcmd:
        return [None, None]
    name = os.path.basenamecmd
    try:
        command = _browsers[name.lower()]
    except KeyError:
        return [
         None, None]
    else:
        controller = command[1]
        if controller:
            if name.lower() == controller.basename:
                import copy
                controller = copy.copycontroller
                controller.name = browser
                controller.basename = os.path.basenamebrowser
                register(browser, None, instance=controller, preferred=preferred)
                return [
                 None, controller]
        return [
         None, None]


class BaseBrowser(object):
    __doc__ = 'Parent class for all browsers. Do not use directly.'
    args = [
     '%s']

    def __init__(self, name=''):
        self.name = name
        self.basename = name

    def open(self, url, new=0, autoraise=True):
        raise NotImplementedError

    def open_new(self, url):
        return self.openurl1

    def open_new_tab(self, url):
        return self.openurl2


class GenericBrowser(BaseBrowser):
    __doc__ = 'Class for all browsers started with a command\n       and without remote functionality.'

    def __init__(self, name):
        if isinstance(name, str):
            self.name = name
            self.args = ['%s']
        else:
            self.name = name[0]
            self.args = name[1:]
        self.basename = os.path.basenameself.name

    def open--- This code section failed: ---

 L. 157         0  LOAD_GLOBAL              sys
                2  LOAD_METHOD              audit
                4  LOAD_STR                 'webbrowser.open'
                6  LOAD_DEREF               'url'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 158        12  LOAD_FAST                'self'
               14  LOAD_ATTR                name
               16  BUILD_LIST_1          1 
               18  LOAD_CLOSURE             'url'
               20  BUILD_TUPLE_1         1 
               22  LOAD_LISTCOMP            '<code_object <listcomp>>'
               24  LOAD_STR                 'GenericBrowser.open.<locals>.<listcomp>'
               26  MAKE_FUNCTION_8          'closure'

 L. 159        28  LOAD_FAST                'self'
               30  LOAD_ATTR                args

 L. 158        32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  BINARY_ADD       
               38  STORE_FAST               'cmdline'

 L. 160        40  SETUP_FINALLY        98  'to 98'

 L. 161        42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                platform
               46  LOAD_CONST               None
               48  LOAD_CONST               3
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'win'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L. 162        60  LOAD_GLOBAL              subprocess
               62  LOAD_METHOD              Popen
               64  LOAD_FAST                'cmdline'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'p'
               70  JUMP_FORWARD         86  'to 86'
             72_0  COME_FROM            58  '58'

 L. 164        72  LOAD_GLOBAL              subprocess
               74  LOAD_ATTR                Popen
               76  LOAD_FAST                'cmdline'
               78  LOAD_CONST               True
               80  LOAD_CONST               ('close_fds',)
               82  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               84  STORE_FAST               'p'
             86_0  COME_FROM            70  '70'

 L. 165        86  LOAD_FAST                'p'
               88  LOAD_METHOD              wait
               90  CALL_METHOD_0         0  ''
               92  UNARY_NOT        
               94  POP_BLOCK        
               96  RETURN_VALUE     
             98_0  COME_FROM_FINALLY    40  '40'

 L. 166        98  DUP_TOP          
              100  LOAD_GLOBAL              OSError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   118  'to 118'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L. 167       112  POP_EXCEPT       
              114  LOAD_CONST               False
              116  RETURN_VALUE     
            118_0  COME_FROM           104  '104'
              118  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 114


class BackgroundBrowser(GenericBrowser):
    __doc__ = 'Class for all browsers which are to be started in the\n       background.'

    def open--- This code section failed: ---

 L. 175         0  LOAD_FAST                'self'
                2  LOAD_ATTR                name
                4  BUILD_LIST_1          1 
                6  LOAD_CLOSURE             'url'
                8  BUILD_TUPLE_1         1 
               10  LOAD_LISTCOMP            '<code_object <listcomp>>'
               12  LOAD_STR                 'BackgroundBrowser.open.<locals>.<listcomp>'
               14  MAKE_FUNCTION_8          'closure'

 L. 176        16  LOAD_FAST                'self'
               18  LOAD_ATTR                args

 L. 175        20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  BINARY_ADD       
               26  STORE_FAST               'cmdline'

 L. 177        28  LOAD_GLOBAL              sys
               30  LOAD_METHOD              audit
               32  LOAD_STR                 'webbrowser.open'
               34  LOAD_DEREF               'url'
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L. 178        40  SETUP_FINALLY       102  'to 102'

 L. 179        42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                platform
               46  LOAD_CONST               None
               48  LOAD_CONST               3
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'win'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L. 180        60  LOAD_GLOBAL              subprocess
               62  LOAD_METHOD              Popen
               64  LOAD_FAST                'cmdline'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'p'
               70  JUMP_FORWARD         88  'to 88'
             72_0  COME_FROM            58  '58'

 L. 182        72  LOAD_GLOBAL              subprocess
               74  LOAD_ATTR                Popen
               76  LOAD_FAST                'cmdline'
               78  LOAD_CONST               True

 L. 183        80  LOAD_CONST               True

 L. 182        82  LOAD_CONST               ('close_fds', 'start_new_session')
               84  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               86  STORE_FAST               'p'
             88_0  COME_FROM            70  '70'

 L. 184        88  LOAD_FAST                'p'
               90  LOAD_METHOD              poll
               92  CALL_METHOD_0         0  ''
               94  LOAD_CONST               None
               96  COMPARE_OP               is
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY    40  '40'

 L. 185       102  DUP_TOP          
              104  LOAD_GLOBAL              OSError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   122  'to 122'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 186       116  POP_EXCEPT       
              118  LOAD_CONST               False
              120  RETURN_VALUE     
            122_0  COME_FROM           108  '108'
              122  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 118


class UnixBrowser(BaseBrowser):
    __doc__ = 'Parent class for all Unix browsers with remote functionality.'
    raise_opts = None
    background = False
    redirect_stdout = True
    remote_args = [
     '%action', '%s']
    remote_action = None
    remote_action_newwin = None
    remote_action_newtab = None

    def _invoke--- This code section failed: ---

 L. 207         0  BUILD_LIST_0          0 
                2  STORE_FAST               'raise_opt'

 L. 208         4  LOAD_FAST                'remote'
                6  POP_JUMP_IF_FALSE    42  'to 42'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                raise_opts
               12  POP_JUMP_IF_FALSE    42  'to 42'

 L. 210        14  LOAD_GLOBAL              int
               16  LOAD_FAST                'autoraise'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'autoraise'

 L. 211        22  LOAD_FAST                'self'
               24  LOAD_ATTR                raise_opts
               26  LOAD_FAST                'autoraise'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'opt'

 L. 212        32  LOAD_FAST                'opt'
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 212        36  LOAD_FAST                'opt'
               38  BUILD_LIST_1          1 
               40  STORE_FAST               'raise_opt'
             42_0  COME_FROM            34  '34'
             42_1  COME_FROM            12  '12'
             42_2  COME_FROM             6  '6'

 L. 214        42  LOAD_FAST                'self'
               44  LOAD_ATTR                name
               46  BUILD_LIST_1          1 
               48  LOAD_FAST                'raise_opt'
               50  BINARY_ADD       
               52  LOAD_FAST                'args'
               54  BINARY_ADD       
               56  STORE_FAST               'cmdline'

 L. 216        58  LOAD_FAST                'remote'
               60  POP_JUMP_IF_TRUE     68  'to 68'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                background
               66  POP_JUMP_IF_FALSE    76  'to 76'
             68_0  COME_FROM            60  '60'

 L. 217        68  LOAD_GLOBAL              subprocess
               70  LOAD_ATTR                DEVNULL
               72  STORE_FAST               'inout'
               74  JUMP_FORWARD         80  'to 80'
             76_0  COME_FROM            66  '66'

 L. 220        76  LOAD_CONST               None
               78  STORE_FAST               'inout'
             80_0  COME_FROM            74  '74'

 L. 221        80  LOAD_GLOBAL              subprocess
               82  LOAD_ATTR                Popen
               84  LOAD_FAST                'cmdline'
               86  LOAD_CONST               True
               88  LOAD_FAST                'inout'

 L. 222        90  LOAD_FAST                'self'
               92  LOAD_ATTR                redirect_stdout
               94  POP_JUMP_IF_FALSE   100  'to 100'
               96  LOAD_FAST                'inout'
               98  JUMP_IF_TRUE_OR_POP   102  'to 102'
            100_0  COME_FROM            94  '94'
              100  LOAD_CONST               None
            102_0  COME_FROM            98  '98'

 L. 223       102  LOAD_FAST                'inout'

 L. 223       104  LOAD_CONST               True

 L. 221       106  LOAD_CONST               ('close_fds', 'stdin', 'stdout', 'stderr', 'start_new_session')
              108  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              110  STORE_FAST               'p'

 L. 224       112  LOAD_FAST                'remote'
              114  POP_JUMP_IF_FALSE   162  'to 162'

 L. 227       116  SETUP_FINALLY       136  'to 136'

 L. 228       118  LOAD_FAST                'p'
              120  LOAD_METHOD              wait
              122  LOAD_CONST               5
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'rc'

 L. 230       128  LOAD_FAST                'rc'
              130  UNARY_NOT        
              132  POP_BLOCK        
              134  RETURN_VALUE     
            136_0  COME_FROM_FINALLY   116  '116'

 L. 231       136  DUP_TOP          
              138  LOAD_GLOBAL              subprocess
              140  LOAD_ATTR                TimeoutExpired
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   158  'to 158'
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 232       152  POP_EXCEPT       
              154  LOAD_CONST               True
              156  RETURN_VALUE     
            158_0  COME_FROM           144  '144'
              158  END_FINALLY      
              160  JUMP_FORWARD        200  'to 200'
            162_0  COME_FROM           114  '114'

 L. 233       162  LOAD_FAST                'self'
              164  LOAD_ATTR                background
              166  POP_JUMP_IF_FALSE   190  'to 190'

 L. 234       168  LOAD_FAST                'p'
              170  LOAD_METHOD              poll
              172  CALL_METHOD_0         0  ''
              174  LOAD_CONST               None
              176  COMPARE_OP               is
              178  POP_JUMP_IF_FALSE   184  'to 184'

 L. 235       180  LOAD_CONST               True
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'

 L. 237       184  LOAD_CONST               False
              186  RETURN_VALUE     
              188  JUMP_FORWARD        200  'to 200'
            190_0  COME_FROM           166  '166'

 L. 239       190  LOAD_FAST                'p'
              192  LOAD_METHOD              wait
              194  CALL_METHOD_0         0  ''
              196  UNARY_NOT        
              198  RETURN_VALUE     
            200_0  COME_FROM           188  '188'
            200_1  COME_FROM           160  '160'

Parse error at or near `LOAD_CONST' instruction at offset 154

    def open(self, url, new=0, autoraise=True):
        sys.audit'webbrowser.open'url
        if new == 0:
            action = self.remote_action
        elif new == 1:
            action = self.remote_action_newwin
        elif new == 2:
            if self.remote_action_newtab is None:
                action = self.remote_action_newwin
            else:
                action = self.remote_action_newtab
        else:
            raise Error("Bad 'new' parameter to open(); " + 'expected 0, 1, or 2, got %s' % new)
        args = [arg.replace'%s'url.replace'%action'action for arg in self.remote_args]
        args = [arg for arg in args if arg]
        success = self._invoke(args, True, autoraise, url)
        if not success:
            args = [arg.replace'%s'url for arg in self.args]
            return self._invoke(args, False, False)
        return True


class Mozilla(UnixBrowser):
    __doc__ = 'Launcher class for Mozilla browsers.'
    remote_args = [
     '%action', '%s']
    remote_action = ''
    remote_action_newwin = '-new-window'
    remote_action_newtab = '-new-tab'
    background = True


class Netscape(UnixBrowser):
    __doc__ = 'Launcher class for Netscape browser.'
    raise_opts = [
     '-noraise', '-raise']
    remote_args = ['-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-tab'
    background = True


class Galeon(UnixBrowser):
    __doc__ = 'Launcher class for Galeon/Epiphany browsers.'
    raise_opts = [
     '-noraise', '']
    remote_args = ['%action', '%s']
    remote_action = '-n'
    remote_action_newwin = '-w'
    background = True


class Chrome(UnixBrowser):
    __doc__ = 'Launcher class for Google Chrome browser.'
    remote_args = [
     '%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True


Chromium = Chrome

class Opera(UnixBrowser):
    __doc__ = 'Launcher class for Opera browser.'
    remote_args = [
     '%action', '%s']
    remote_action = ''
    remote_action_newwin = '--new-window'
    remote_action_newtab = ''
    background = True


class Elinks(UnixBrowser):
    __doc__ = 'Launcher class for Elinks browsers.'
    remote_args = [
     '-remote', 'openURL(%s%action)']
    remote_action = ''
    remote_action_newwin = ',new-window'
    remote_action_newtab = ',new-tab'
    background = False
    redirect_stdout = False


class Konqueror(BaseBrowser):
    __doc__ = 'Controller for the KDE File Manager (kfm, or Konqueror).\n\n    See the output of ``kfmclient --commands``\n    for more information on the Konqueror remote-control interface.\n    '

    def open(self, url, new=0, autoraise=True):
        sys.audit'webbrowser.open'url
        if new == 2:
            action = 'newTab'
        else:
            action = 'openURL'
        devnull = subprocess.DEVNULL
        try:
            p = subprocess.Popen(['kfmclient', action, url], close_fds=True,
              stdin=devnull,
              stdout=devnull,
              stderr=devnull)
        except OSError:
            pass
        else:
            p.wait()
            return True
        try:
            p = subprocess.Popen(['konqueror', '--silent', url], close_fds=True,
              stdin=devnull,
              stdout=devnull,
              stderr=devnull,
              start_new_session=True)
        except OSError:
            pass
        else:
            if p.poll() is None:
                return True
        try:
            p = subprocess.Popen(['kfm', '-d', url], close_fds=True,
              stdin=devnull,
              stdout=devnull,
              stderr=devnull,
              start_new_session=True)
        except OSError:
            return False
        else:
            return p.poll() is None


class Grail(BaseBrowser):

    def _find_grail_rc--- This code section failed: ---

 L. 393         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              glob
                6  STORE_FAST               'glob'

 L. 394         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              pwd
               14  STORE_FAST               'pwd'

 L. 395        16  LOAD_CONST               0
               18  LOAD_CONST               None
               20  IMPORT_NAME              socket
               22  STORE_FAST               'socket'

 L. 396        24  LOAD_CONST               0
               26  LOAD_CONST               None
               28  IMPORT_NAME              tempfile
               30  STORE_FAST               'tempfile'

 L. 397        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              join
               38  LOAD_FAST                'tempfile'
               40  LOAD_METHOD              gettempdir
               42  CALL_METHOD_0         0  ''

 L. 398        44  LOAD_STR                 '.grail-unix'

 L. 397        46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'tempdir'

 L. 399        50  LOAD_FAST                'pwd'
               52  LOAD_METHOD              getpwuid
               54  LOAD_GLOBAL              os
               56  LOAD_METHOD              getuid
               58  CALL_METHOD_0         0  ''
               60  CALL_METHOD_1         1  ''
               62  LOAD_CONST               0
               64  BINARY_SUBSCR    
               66  STORE_FAST               'user'

 L. 400        68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              join
               74  LOAD_FAST                'tempdir'
               76  LOAD_FAST                'user'
               78  LOAD_STR                 '-*'
               80  BINARY_ADD       
               82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'filename'

 L. 401        86  LOAD_FAST                'glob'
               88  LOAD_METHOD              glob
               90  LOAD_FAST                'filename'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'maybes'

 L. 402        96  LOAD_FAST                'maybes'
               98  POP_JUMP_IF_TRUE    104  'to 104'

 L. 403       100  LOAD_CONST               None
              102  RETURN_VALUE     
            104_0  COME_FROM            98  '98'

 L. 404       104  LOAD_FAST                'socket'
              106  LOAD_METHOD              socket
              108  LOAD_FAST                'socket'
              110  LOAD_ATTR                AF_UNIX
              112  LOAD_FAST                'socket'
              114  LOAD_ATTR                SOCK_STREAM
              116  CALL_METHOD_2         2  ''
              118  STORE_FAST               's'

 L. 405       120  LOAD_FAST                'maybes'
              122  GET_ITER         
            124_0  COME_FROM           208  '208'
            124_1  COME_FROM           196  '196'
              124  FOR_ITER            210  'to 210'
              126  STORE_FAST               'fn'

 L. 407       128  SETUP_FINALLY       144  'to 144'

 L. 408       130  LOAD_FAST                's'
              132  LOAD_METHOD              connect
              134  LOAD_FAST                'fn'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  POP_BLOCK        
              142  JUMP_FORWARD        200  'to 200'
            144_0  COME_FROM_FINALLY   128  '128'

 L. 409       144  DUP_TOP          
              146  LOAD_GLOBAL              OSError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   198  'to 198'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 411       158  SETUP_FINALLY       174  'to 174'

 L. 412       160  LOAD_GLOBAL              os
              162  LOAD_METHOD              unlink
              164  LOAD_FAST                'fn'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  JUMP_FORWARD        194  'to 194'
            174_0  COME_FROM_FINALLY   158  '158'

 L. 413       174  DUP_TOP          
              176  LOAD_GLOBAL              OSError
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   192  'to 192'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 414       188  POP_EXCEPT       
              190  BREAK_LOOP          194  'to 194'
            192_0  COME_FROM           180  '180'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           172  '172'
              194  POP_EXCEPT       
              196  JUMP_BACK           124  'to 124'
            198_0  COME_FROM           150  '150'
              198  END_FINALLY      
            200_0  COME_FROM           142  '142'

 L. 416       200  LOAD_FAST                's'
              202  ROT_TWO          
              204  POP_TOP          
              206  RETURN_VALUE     
              208  JUMP_BACK           124  'to 124'
            210_0  COME_FROM           124  '124'

Parse error at or near `END_FINALLY' instruction at offset 192

    def _remote(self, action):
        s = self._find_grail_rc()
        if not s:
            return 0
        s.sendaction
        s.close()
        return 1

    def open(self, url, new=0, autoraise=True):
        sys.audit'webbrowser.open'url
        if new:
            ok = self._remote('LOADNEW ' + url)
        else:
            ok = self._remote('LOAD ' + url)
        return ok


def register_X_browsers():
    if shutil.which'xdg-open':
        register('xdg-open', None, BackgroundBrowser('xdg-open'))
    if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
        if shutil.which'gvfs-open':
            register('gvfs-open', None, BackgroundBrowser('gvfs-open'))
    if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
        if shutil.which'gnome-open':
            register('gnome-open', None, BackgroundBrowser('gnome-open'))
    if 'KDE_FULL_SESSION' in os.environ:
        if shutil.which'kfmclient':
            register('kfmclient', Konqueror, Konqueror('kfmclient'))
    if shutil.which'x-www-browser':
        register('x-www-browser', None, BackgroundBrowser('x-www-browser'))
    for browser in ('firefox', 'iceweasel', 'iceape', 'seamonkey'):
        if shutil.whichbrowser:
            register(browser, None, Mozilla(browser))
    else:
        for browser in ('mozilla-firefox', 'mozilla-firebird', 'firebird', 'mozilla',
                        'netscape'):
            if shutil.whichbrowser:
                register(browser, None, Netscape(browser))
        else:
            if shutil.which'kfm':
                register('kfm', Konqueror, Konqueror('kfm'))
            elif shutil.which'konqueror':
                register('konqueror', Konqueror, Konqueror('konqueror'))
            for browser in ('galeon', 'epiphany'):
                if shutil.whichbrowser:
                    register(browser, None, Galeon(browser))
            else:
                if shutil.which'skipstone':
                    register('skipstone', None, BackgroundBrowser('skipstone'))
                for browser in ('google-chrome', 'chrome', 'chromium', 'chromium-browser'):
                    if shutil.whichbrowser:
                        register(browser, None, Chrome(browser))
                else:
                    if shutil.which'opera':
                        register('opera', None, Opera('opera'))
                    if shutil.which'mosaic':
                        register('mosaic', None, BackgroundBrowser('mosaic'))
                    if shutil.which'grail':
                        register('grail', Grail, None)


def register_standard_browsers():
    global _os_preferred_browser
    global _tryorder
    _tryorder = []
    if sys.platform == 'darwin':
        register('MacOSX', None, MacOSXOSAScript('default'))
        register('chrome', None, MacOSXOSAScript('chrome'))
        register('firefox', None, MacOSXOSAScript('firefox'))
        register('safari', None, MacOSXOSAScript('safari'))
    if sys.platform[:3] == 'win':
        register('windows-default', WindowsDefault)
        iexplore = os.path.joinos.environ.get'PROGRAMFILES''C:\\Program Files''Internet Explorer\\IEXPLORE.EXE'
        for browser in (
         'firefox', 'firebird', 'seamonkey', 'mozilla',
         'netscape', 'opera', iexplore):
            if shutil.whichbrowser:
                register(browser, None, BackgroundBrowser(browser))

    else:
        if os.environ.get'DISPLAY':
            try:
                cmd = 'xdg-settings get default-web-browser'.split()
                raw_result = subprocess.check_output(cmd, stderr=(subprocess.DEVNULL))
                result = raw_result.decode().strip()
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass
            else:
                _os_preferred_browser = result
            register_X_browsers()
        if os.environ.get'TERM':
            if shutil.which'www-browser':
                register('www-browser', None, GenericBrowser('www-browser'))
            if shutil.which'links':
                register('links', None, GenericBrowser('links'))
            if shutil.which'elinks':
                register('elinks', None, Elinks('elinks'))
            if shutil.which'lynx':
                register('lynx', None, GenericBrowser('lynx'))
            if shutil.which'w3m':
                register('w3m', None, GenericBrowser('w3m'))
    if 'BROWSER' in os.environ:
        userchoices = os.environ['BROWSER'].splitos.pathsep
        userchoices.reverse()
        for cmdline in userchoices:
            if cmdline != '':
                cmd = _synthesize(cmdline, preferred=True)
                if cmd[1] is None:
                    register(cmdline, None, (GenericBrowser(cmdline)), preferred=True)


if sys.platform[:3] == 'win':

    class WindowsDefault(BaseBrowser):

        def open(self, url, new=0, autoraise=True):
            sys.audit'webbrowser.open'url
            try:
                os.startfileurl
            except OSError:
                return False
            else:
                return True


if sys.platform == 'darwin':

    class MacOSX(BaseBrowser):
        __doc__ = 'Launcher class for Aqua browsers on Mac OS X\n\n        Optionally specify a browser name on instantiation.  Note that this\n        will not work for Aqua browsers if the user has moved the application\n        package after installation.\n\n        If no browser is specified, the default browser, as specified in the\n        Internet System Preferences panel, will be used.\n        '

        def __init__(self, name):
            self.name = name

        def open(self, url, new=0, autoraise=True):
            sys.audit'webbrowser.open'url
            assert "'" not in url
            if ':' not in url:
                url = 'file:' + url
            new = int(bool(new))
            if self.name == 'default':
                script = 'open location "%s"' % url.replace'"''%22'
            else:
                if self.name == 'OmniWeb':
                    toWindow = ''
                else:
                    toWindow = 'toWindow %d' % (new - 1)
                cmd = 'OpenURL "%s"' % url.replace'"''%22'
                script = 'tell application "%s"\n                                activate\n                                %s %s\n                            end tell' % (
                 self.name, cmd, toWindow)
            osapipe = os.popen'osascript''w'
            if osapipe is None:
                return False
            osapipe.writescript
            rc = osapipe.close()
            return not rc


    class MacOSXOSAScript(BaseBrowser):

        def __init__(self, name):
            self._name = name

        def open(self, url, new=0, autoraise=True):
            if self._name == 'default':
                script = 'open location "%s"' % url.replace'"''%22'
            else:
                script = '\n                   tell application "%s"\n                       activate\n                       open location "%s"\n                   end\n                   ' % (
                 self._name, url.replace'"''%22')
            osapipe = os.popen'osascript''w'
            if osapipe is None:
                return False
            osapipe.writescript
            rc = osapipe.close()
            return not rc


def main():
    import getopt
    usage = 'Usage: %s [-n | -t] url\n    -n: open new window\n    -t: open new tab' % sys.argv[0]
    try:
        opts, args = getopt.getoptsys.argv[1:]'ntd'
    except getopt.error as msg:
        try:
            print(msg, file=(sys.stderr))
            print(usage, file=(sys.stderr))
            sys.exit1
        finally:
            msg = None
            del msg

    else:
        new_win = 0
    for o, a in opts:
        if o == '-n':
            new_win = 1
        else:
            if o == '-t':
                new_win = 2
    else:
        if len(args) != 1:
            print(usage, file=(sys.stderr))
            sys.exit1
        url = args[0]
        open(url, new_win)
        print('\x07')


if __name__ == '__main__':
    main()