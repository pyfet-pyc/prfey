# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
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
               16  CALL_FUNCTION_0       0  '0 positional arguments'
               18  POP_TOP          
             20_0  COME_FROM            12  '12'

 L.  27        20  LOAD_FAST                'klass'
               22  LOAD_FAST                'instance'
               24  BUILD_LIST_2          2 
               26  LOAD_GLOBAL              _browsers
               28  LOAD_FAST                'name'
               30  LOAD_METHOD              lower
               32  CALL_METHOD_0         0  '0 positional arguments'
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
               60  CALL_METHOD_2         2  '2 positional arguments'
               62  POP_TOP          
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM            50  '50'
             66_1  COME_FROM            42  '42'

 L.  35        66  LOAD_GLOBAL              _tryorder
               68  LOAD_METHOD              append
               70  LOAD_FAST                'name'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_TOP          
             76_0  COME_FROM            64  '64'
               76  POP_BLOCK        
               78  LOAD_CONST               None
             80_0  COME_FROM_WITH        2  '2'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 76


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
            else:
                return GenericBrowser(browser)
        else:
            try:
                command = _browsers[browser.lower()]
            except KeyError:
                command = _synthesize(browser)

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

    return False


def open_new(url):
    return open(url, 1)


def open_new_tab(url):
    return open(url, 2)


def _synthesize(browser, *, preferred=False):
    """Attempt to synthesize a controller based on existing controllers.

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

    def open(self, url, new=0, autoraise=True):
        cmdline = [
         self.name] + [arg.replace'%s'url for arg in self.args]
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popencmdline
            else:
                p = subprocess.Popen(cmdline, close_fds=True)
            return not p.wait()
        except OSError:
            return False


class BackgroundBrowser(GenericBrowser):
    __doc__ = 'Class for all browsers which are to be started in the\n       background.'

    def open(self, url, new=0, autoraise=True):
        cmdline = [
         self.name] + [arg.replace'%s'url for arg in self.args]
        try:
            if sys.platform[:3] == 'win':
                p = subprocess.Popencmdline
            else:
                p = subprocess.Popen(cmdline, close_fds=True, start_new_session=True)
            return p.poll() is None
        except OSError:
            return False


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

    def _invoke(self, args, remote, autoraise):
        raise_opt = []
        if remote:
            if self.raise_opts:
                autoraise = int(autoraise)
                opt = self.raise_opts[autoraise]
                if opt:
                    raise_opt = [
                     opt]
        cmdline = [
         self.name] + raise_opt + args
        if remote or self.background:
            inout = subprocess.DEVNULL
        else:
            inout = None
        p = subprocess.Popen(cmdline, close_fds=True, stdin=inout, stdout=(self.redirect_stdout) and inout or None,
          stderr=inout,
          start_new_session=True)
        if remote:
            try:
                rc = p.wait5
                return not rc
            except subprocess.TimeoutExpired:
                return True

        elif self.background:
            if p.poll() is None:
                return True
            return False
        else:
            return not p.wait()

    def open(self, url, new=0, autoraise=True):
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
        success = self._invoke(args, True, autoraise)
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

    def _find_grail_rc(self):
        import glob, pwd, socket, tempfile
        tempdir = os.path.jointempfile.gettempdir()'.grail-unix'
        user = pwd.getpwuidos.getuid()[0]
        filename = os.path.jointempdir(user + '-*')
        maybes = glob.globfilename
        if not maybes:
            return
        s = socket.socketsocket.AF_UNIXsocket.SOCK_STREAM
        for fn in maybes:
            try:
                s.connectfn
            except OSError:
                try:
                    os.unlinkfn
                except OSError:
                    pass

            else:
                return s

    def _remote(self, action):
        s = self._find_grail_rc()
        if not s:
            return 0
        s.sendaction
        s.close()
        return 1

    def open(self, url, new=0, autoraise=True):
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

    for browser in ('mozilla-firefox', 'mozilla-firebird', 'firebird', 'mozilla', 'netscape'):
        if shutil.whichbrowser:
            register(browser, None, Netscape(browser))

    if shutil.which'kfm':
        register('kfm', Konqueror, Konqueror('kfm'))
    elif shutil.which'konqueror':
        register('konqueror', Konqueror, Konqueror('konqueror'))
    for browser in ('galeon', 'epiphany'):
        if shutil.whichbrowser:
            register(browser, None, Galeon(browser))

    if shutil.which'skipstone':
        register('skipstone', None, BackgroundBrowser('skipstone'))
    for browser in ('google-chrome', 'chrome', 'chromium', 'chromium-browser'):
        if shutil.whichbrowser:
            register(browser, None, Chrome(browser))

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
        for browser in ('firefox', 'firebird', 'seamonkey', 'mozilla',
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
                script = 'tell application "%s"\n                                activate\n                                %s %s\n                            end tell' % (self.name, cmd, toWindow)
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
                script = '\n                   tell application "%s"\n                       activate\n                       open location "%s"\n                   end\n                   ' % (self._name, url.replace'"''%22')
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

    new_win = 0
    for o, a in opts:
        if o == '-n':
            new_win = 1
        if o == '-t':
            new_win = 2

    if len(args) != 1:
        print(usage, file=(sys.stderr))
        sys.exit1
    url = args[0]
    open(url, new_win)
    print('\x07')


if __name__ == '__main__':
    main()