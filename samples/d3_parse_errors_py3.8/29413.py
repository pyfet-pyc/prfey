# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\firefox\firefox_binary.py
import os, platform
from subprocess import Popen, STDOUT
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
import time

class FirefoxBinary(object):
    NO_FOCUS_LIBRARY_NAME = 'x_ignore_nofocus.so'

    def __init__(self, firefox_path=None, log_file=None):
        """
        Creates a new instance of Firefox binary.

        :Args:
         - firefox_path - Path to the Firefox executable. By default, it will be detected from the standard locations.
         - log_file - A file object to redirect the firefox process output to. It can be sys.stdout.
                      Please note that with parallel run the output won't be synchronous.
                      By default, it will be redirected to /dev/null.
        """
        self._start_cmd = firefox_path
        self._log_file = log_file or open(os.devnull, 'wb')
        self.command_line = None
        if self._start_cmd is None:
            self._start_cmd = self._get_firefox_start_cmd()
        if not self._start_cmd.strip():
            raise WebDriverException("Failed to find firefox binary. You can set it by specifying the path to 'firefox_binary':\n\nfrom selenium.webdriver.firefox.firefox_binary import FirefoxBinary\n\nbinary = FirefoxBinary('/path/to/binary')\ndriver = webdriver.Firefox(firefox_binary=binary)")
        self._firefox_env = os.environ.copy()
        self._firefox_env['MOZ_CRASHREPORTER_DISABLE'] = '1'
        self._firefox_env['MOZ_NO_REMOTE'] = '1'
        self._firefox_env['NO_EM_RESTART'] = '1'

    def add_command_line_options(self, *args):
        self.command_line = args

    def launch_browser(self, profile, timeout=30):
        """Launches the browser for the given profile name.
        It is assumed the profile already exists.
        """
        self.profile = profile
        self._start_from_profile_path(self.profile.path)
        self._wait_until_connectable(timeout=timeout)

    def kill(self):
        """Kill the browser.

        This is useful when the browser is stuck.
        """
        if self.process:
            self.process.kill()
            self.process.wait()

    def _start_from_profile_path(self, path):
        self._firefox_env['XRE_PROFILE_PATH'] = path
        if platform.system().lower() == 'linux':
            self._modify_link_library_path()
        command = [
         self._start_cmd, '-foreground']
        if self.command_line is not None:
            for cli in self.command_line:
                command.append(cli)

        self.process = Popen(command,
          stdout=(self._log_file), stderr=STDOUT, env=(self._firefox_env))

    def _wait_until_connectable(self, timeout=30):
        """Blocks until the extension is connectable in the firefox."""
        count = 0
        while True:
            if not utils.is_connectable(self.profile.port):
                if self.process.poll() is not None:
                    raise WebDriverException('The browser appears to have exited before we could connect. If you specified a log_file in the FirefoxBinary constructor, check it for details.')
                if count >= timeout:
                    self.kill()
                    raise WebDriverException("Can't load the profile. Possible firefox version mismatch. You must use GeckoDriver instead for Firefox 48+. Profile Dir: %s If you specified a log_file in the FirefoxBinary constructor, check it for details." % self.profile.path)
                count += 1
                time.sleep(1)

        return True

    def _find_exe_in_registry--- This code section failed: ---

 L. 120         0  SETUP_FINALLY        30  'to 30'

 L. 121         2  LOAD_CONST               0
                4  LOAD_CONST               ('OpenKey', 'QueryValue', 'HKEY_LOCAL_MACHINE', 'HKEY_CURRENT_USER')
                6  IMPORT_NAME              _winreg
                8  IMPORT_FROM              OpenKey
               10  STORE_FAST               'OpenKey'
               12  IMPORT_FROM              QueryValue
               14  STORE_FAST               'QueryValue'
               16  IMPORT_FROM              HKEY_LOCAL_MACHINE
               18  STORE_FAST               'HKEY_LOCAL_MACHINE'
               20  IMPORT_FROM              HKEY_CURRENT_USER
               22  STORE_FAST               'HKEY_CURRENT_USER'
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD         74  'to 74'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 122        30  DUP_TOP          
               32  LOAD_GLOBAL              ImportError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    72  'to 72'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 123        44  LOAD_CONST               0
               46  LOAD_CONST               ('OpenKey', 'QueryValue', 'HKEY_LOCAL_MACHINE', 'HKEY_CURRENT_USER')
               48  IMPORT_NAME              winreg
               50  IMPORT_FROM              OpenKey
               52  STORE_FAST               'OpenKey'
               54  IMPORT_FROM              QueryValue
               56  STORE_FAST               'QueryValue'
               58  IMPORT_FROM              HKEY_LOCAL_MACHINE
               60  STORE_FAST               'HKEY_LOCAL_MACHINE'
               62  IMPORT_FROM              HKEY_CURRENT_USER
               64  STORE_FAST               'HKEY_CURRENT_USER'
               66  POP_TOP          
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            36  '36'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            28  '28'

 L. 124        74  LOAD_CONST               0
               76  LOAD_CONST               None
               78  IMPORT_NAME              shlex
               80  STORE_FAST               'shlex'

 L. 125        82  LOAD_CONST               ('SOFTWARE\\Classes\\FirefoxHTML\\shell\\open\\command', 'SOFTWARE\\Classes\\Applications\\firefox.exe\\shell\\open\\command')
               84  STORE_FAST               'keys'

 L. 127        86  LOAD_STR                 ''
               88  STORE_FAST               'command'

 L. 128        90  LOAD_FAST                'keys'
               92  GET_ITER         
             94_0  COME_FROM           204  '204'
             94_1  COME_FROM           200  '200'
             94_2  COME_FROM           128  '128'
               94  FOR_ITER            206  'to 206'
               96  STORE_FAST               'path'

 L. 129        98  SETUP_FINALLY       130  'to 130'

 L. 130       100  LOAD_FAST                'OpenKey'
              102  LOAD_FAST                'HKEY_LOCAL_MACHINE'
              104  LOAD_FAST                'path'
              106  CALL_FUNCTION_2       2  ''
              108  STORE_FAST               'key'

 L. 131       110  LOAD_FAST                'QueryValue'
              112  LOAD_FAST                'key'
              114  LOAD_STR                 ''
              116  CALL_FUNCTION_2       2  ''
              118  STORE_FAST               'command'

 L. 132       120  POP_BLOCK        
              122  POP_TOP          
              124  JUMP_FORWARD        210  'to 210'
              126  POP_BLOCK        
              128  JUMP_BACK            94  'to 94'
            130_0  COME_FROM_FINALLY    98  '98'

 L. 133       130  DUP_TOP          
              132  LOAD_GLOBAL              OSError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   202  'to 202'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 134       144  SETUP_FINALLY       178  'to 178'

 L. 135       146  LOAD_FAST                'OpenKey'
              148  LOAD_FAST                'HKEY_CURRENT_USER'
              150  LOAD_FAST                'path'
              152  CALL_FUNCTION_2       2  ''
              154  STORE_FAST               'key'

 L. 136       156  LOAD_FAST                'QueryValue'
              158  LOAD_FAST                'key'
              160  LOAD_STR                 ''
              162  CALL_FUNCTION_2       2  ''
              164  STORE_FAST               'command'

 L. 137       166  POP_BLOCK        
              168  POP_EXCEPT       
              170  POP_TOP          
              172  JUMP_FORWARD        210  'to 210'
              174  POP_BLOCK        
              176  JUMP_FORWARD        198  'to 198'
            178_0  COME_FROM_FINALLY   144  '144'

 L. 138       178  DUP_TOP          
              180  LOAD_GLOBAL              OSError
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   196  'to 196'
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 139       192  POP_EXCEPT       
              194  BREAK_LOOP          198  'to 198'
            196_0  COME_FROM           184  '184'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           176  '176'
              198  POP_EXCEPT       
              200  JUMP_BACK            94  'to 94'
            202_0  COME_FROM           136  '136'
              202  END_FINALLY      
              204  JUMP_BACK            94  'to 94'
            206_0  COME_FROM            94  '94'

 L. 141       206  LOAD_STR                 ''
              208  RETURN_VALUE     
            210_0  COME_FROM           172  '172'
            210_1  COME_FROM           124  '124'

 L. 143       210  LOAD_FAST                'command'
              212  POP_JUMP_IF_TRUE    218  'to 218'

 L. 144       214  LOAD_STR                 ''
              216  RETURN_VALUE     
            218_0  COME_FROM           212  '212'

 L. 146       218  LOAD_FAST                'shlex'
              220  LOAD_METHOD              split
              222  LOAD_FAST                'command'
              224  CALL_METHOD_1         1  ''
              226  LOAD_CONST               0
              228  BINARY_SUBSCR    
              230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 168

    def _get_firefox_start_cmd(self):
        """Return the command to start firefox."""
        start_cmd = ''
        if platform.system() == 'Darwin':
            start_cmd = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
            start_cmd = (os.path.exists(start_cmd) or os.path.expanduser('~')) + start_cmd
        elif platform.system() == 'Windows':
            start_cmd = self._find_exe_in_registry() or self._default_windows_location()
        elif platform.system() == 'Java' and os._name == 'nt':
            start_cmd = self._default_windows_location()
        else:
            for ffname in ('firefox', 'iceweasel'):
                start_cmd = self.which(ffname)
                if start_cmd is not None:
                    break
            else:
                raise RuntimeError('Could not find firefox in your system PATH. Please specify the firefox binary location or install firefox')

        return start_cmd

    def _default_windows_location(self):
        program_files = [
         os.getenv('PROGRAMFILES', 'C:\\Program Files'),
         os.getenv('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')]
        for path in program_files:
            binary_path = os.path.join(path, 'Mozilla Firefox\\firefox.exe')
            if os.access(binary_path, os.X_OK):
                return binary_path
        else:
            return ''

    def _modify_link_library_path(self):
        existing_ld_lib_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_lib_path = self._extract_and_check(self.profile, self.NO_FOCUS_LIBRARY_NAME, 'x86', 'amd64')
        new_ld_lib_path += existing_ld_lib_path
        self._firefox_env['LD_LIBRARY_PATH'] = new_ld_lib_path
        self._firefox_env['LD_PRELOAD'] = self.NO_FOCUS_LIBRARY_NAME

    def _extract_and_check(self, profile, no_focus_so_name, x86, amd64):
        paths = [
         x86, amd64]
        built_path = ''
        for path in paths:
            library_path = os.path.join(profile.path, path)
            if not os.path.exists(library_path):
                os.makedirs(library_path)
            else:
                import shutil
                shutil.copy(os.path.join(os.path.dirname(__file__), path, self.NO_FOCUS_LIBRARY_NAME), library_path)
                built_path += library_path + ':'
        else:
            return built_path

    def which(self, fname):
        """Returns the fully qualified path by searching Path of the given
        name"""
        for pe in os.environ['PATH'].split(os.pathsep):
            checkname = os.path.join(pe, fname)
            if os.access(checkname, os.X_OK):
                if not os.path.isdir(checkname):
                    return checkname