# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\common\service.py
import errno, os, platform, subprocess
from subprocess import PIPE
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
try:
    from subprocess import DEVNULL
    _HAS_NATIVE_DEVNULL = True
except ImportError:
    DEVNULL = -3
    _HAS_NATIVE_DEVNULL = False
else:

    class Service(object):

        def __init__(self, executable, port=0, log_file=DEVNULL, env=None, start_error_message=''):
            self.path = executable
            self.port = port
            if self.port == 0:
                self.port = utils.free_port()
            if not _HAS_NATIVE_DEVNULL:
                if log_file == DEVNULL:
                    log_file = open(os.devnull, 'wb')
            self.start_error_message = start_error_message
            self.log_file = log_file
            self.env = env or os.environ

        @property
        def service_url(self):
            """
        Gets the url of the Service
        """
            return 'http://%s' % utils.join_host_port('localhost', self.port)

        def command_line_args(self):
            raise NotImplemented('This method needs to be implemented in a sub class')

        def start(self):
            """
        Starts the Service.

        :Exceptions:
         - WebDriverException : Raised either when it can't start the service
           or when it can't connect to the service
        """
            try:
                cmd = [
                 self.path]
                cmd.extend(self.command_line_args())
                self.process = subprocess.Popen(cmd, env=(self.env), close_fds=(platform.system() != 'Windows'),
                  stdout=(self.log_file),
                  stderr=(self.log_file),
                  stdin=PIPE)
            except TypeError:
                raise
            except OSError as err:
                try:
                    if err.errno == errno.ENOENT:
                        raise WebDriverException("'%s' executable needs to be in PATH. %s" % (
                         os.path.basename(self.path), self.start_error_message))
                    elif err.errno == errno.EACCES:
                        raise WebDriverException("'%s' executable may have wrong permissions. %s" % (
                         os.path.basename(self.path), self.start_error_message))
                    else:
                        raise
                finally:
                    err = None
                    del err

            except Exception as e:
                try:
                    raise WebDriverException('The executable %s needs to be available in the path. %s\n%s' % (
                     os.path.basename(self.path), self.start_error_message, str(e)))
                finally:
                    e = None
                    del e

            else:
                count = 0
                while True:
                    self.assert_process_still_running()
                    if self.is_connectable():
                        pass
                    else:
                        count += 1
                        time.sleep(1)
                        if count == 30:
                            raise WebDriverException('Can not connect to the Service %s' % self.path)

        def assert_process_still_running(self):
            return_code = self.process.poll()
            if return_code is not None:
                raise WebDriverException('Service %s unexpectedly exited. Status code was: %s' % (
                 self.path, return_code))

        def is_connectable(self):
            return utils.is_connectable(self.port)

        def send_remote_shutdown_command--- This code section failed: ---

 L. 118         0  SETUP_FINALLY        24  'to 24'

 L. 119         2  LOAD_CONST               0
                4  LOAD_CONST               ('request',)
                6  IMPORT_NAME              urllib
                8  IMPORT_FROM              request
               10  STORE_FAST               'url_request'
               12  POP_TOP          

 L. 120        14  LOAD_FAST                'url_request'
               16  LOAD_ATTR                URLError
               18  STORE_FAST               'URLError'
               20  POP_BLOCK        
               22  JUMP_FORWARD         66  'to 66'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 121        24  DUP_TOP          
               26  LOAD_GLOBAL              ImportError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    64  'to 64'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 122        38  LOAD_CONST               0
               40  LOAD_CONST               None
               42  IMPORT_NAME              urllib2
               44  STORE_FAST               'url_request'

 L. 123        46  LOAD_CONST               0
               48  LOAD_CONST               None
               50  IMPORT_NAME              urllib2
               52  STORE_FAST               'urllib2'

 L. 124        54  LOAD_FAST                'urllib2'
               56  LOAD_ATTR                URLError
               58  STORE_FAST               'URLError'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            30  '30'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            22  '22'

 L. 126        66  SETUP_FINALLY        88  'to 88'

 L. 127        68  LOAD_FAST                'url_request'
               70  LOAD_METHOD              urlopen
               72  LOAD_STR                 '%s/shutdown'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                service_url
               78  BINARY_MODULO    
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  JUMP_FORWARD        110  'to 110'
             88_0  COME_FROM_FINALLY    66  '66'

 L. 128        88  DUP_TOP          
               90  LOAD_FAST                'URLError'
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   108  'to 108'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 129       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            94  '94'
              108  END_FINALLY      
            110_0  COME_FROM            86  '86'

 L. 131       110  LOAD_GLOBAL              range
              112  LOAD_CONST               30
              114  CALL_FUNCTION_1       1  ''
              116  GET_ITER         
            118_0  COME_FROM           146  '146'
            118_1  COME_FROM           134  '134'
              118  FOR_ITER            148  'to 148'
              120  STORE_FAST               'x'

 L. 132       122  LOAD_FAST                'self'
              124  LOAD_METHOD              is_connectable
              126  CALL_METHOD_0         0  ''
              128  POP_JUMP_IF_TRUE    136  'to 136'

 L. 133       130  POP_TOP          
              132  BREAK_LOOP          148  'to 148'
              134  JUMP_BACK           118  'to 118'
            136_0  COME_FROM           128  '128'

 L. 135       136  LOAD_GLOBAL              time
              138  LOAD_METHOD              sleep
              140  LOAD_CONST               1
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
              146  JUMP_BACK           118  'to 118'
            148_0  COME_FROM           132  '132'
            148_1  COME_FROM           118  '118'

Parse error at or near `COME_FROM' instruction at offset 148_0

        def stop(self):
            """
        Stops the service.
        """
            if not (self.log_file != PIPE and self.log_file == DEVNULL and _HAS_NATIVE_DEVNULL):
                try:
                    self.log_file.close()
                except Exception:
                    pass
                else:
                    if self.process is None:
                        return
            try:
                self.send_remote_shutdown_command()
            except TypeError:
                pass

            try:
                if self.process:
                    for stream in (
                     self.process.stdin,
                     self.process.stdout,
                     self.process.stderr):
                        try:
                            stream.close()
                        except AttributeError:
                            pass

                    else:
                        self.process.terminate()
                        self.process.wait()
                        self.process.kill()
                        self.process = None

            except OSError:
                pass

        def __del__(self):
            try:
                self.stop()
            except Exception:
                pass