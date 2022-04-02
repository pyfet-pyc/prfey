# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: electrum\base_crash_reporter.py
import asyncio, json, locale, traceback, subprocess, sys, os
from .version import ELECTRUM_VERSION
from . import constants
from .i18n import _
from .util import make_aiohttp_session

class BaseCrashReporter:
    report_server = 'https://crashhub.electrum.org'
    config_key = 'show_crash_reporter'
    issue_template = '<h2>Traceback</h2>\n<pre>\n{traceback}\n</pre>\n\n<h2>Additional information</h2>\n<ul>\n  <li>Electrum version: {app_version}</li>\n  <li>Python version: {python_version}</li>\n  <li>Operating system: {os}</li>\n  <li>Wallet type: {wallet_type}</li>\n  <li>Locale: {locale}</li>\n</ul>\n    '
    CRASH_MESSAGE = _('Something went wrong while executing Electrum.')
    CRASH_TITLE = _('Sorry!')
    REQUEST_HELP_MESSAGE = _('To help us diagnose and fix the problem, you can send us a bug report that contains useful debug information:')
    DESCRIBE_ERROR_MESSAGE = _('Please briefly describe what led to the error (optional):')
    ASK_CONFIRM_SEND = _('Do you want to send this report?')

    def __init__(self, exctype, value, tb):
        self.exc_args = (
         exctype, value, tb)

    def send_report(self, asyncio_loop, proxy, endpoint='/crash'):
        response = ''
        return response

    async def do_post--- This code section failed: ---

 L.  68         0  LOAD_GLOBAL              make_aiohttp_session
                2  LOAD_FAST                'proxy'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  BEFORE_ASYNC_WITH
                8  GET_AWAITABLE    
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  SETUP_ASYNC_WITH     72  'to 72'
               16  STORE_FAST               'session'

 L.  69        18  LOAD_FAST                'session'
               20  LOAD_ATTR                post
               22  LOAD_FAST                'url'
               24  LOAD_FAST                'data'
               26  LOAD_CONST               ('data',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  BEFORE_ASYNC_WITH
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  SETUP_ASYNC_WITH     56  'to 56'
               40  STORE_FAST               'resp'

 L.  70        42  LOAD_FAST                'resp'
               44  LOAD_ATTR                text
               46  CALL_FUNCTION_0       0  '0 positional arguments'
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  RETURN_VALUE     
             56_0  COME_FROM_ASYNC_WITH    38  '38'
               56  WITH_CLEANUP_START
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      
               68  POP_BLOCK        
               70  LOAD_CONST               None
             72_0  COME_FROM_ASYNC_WITH    14  '14'
               72  WITH_CLEANUP_START
               74  GET_AWAITABLE    
               76  LOAD_CONST               None
               78  YIELD_FROM       
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 56_0

    def get_traceback_info(self):
        exc_string = str(self.exc_args[1])
        stack = traceback.extract_tb(self.exc_args[2])
        readable_trace = ''.join(traceback.format_list(stack))
        id = {'file':stack[(-1)].filename, 
         'name':stack[(-1)].name, 
         'type':self.exc_args[0].__name__}
        return {'exc_string':exc_string, 
         'stack':readable_trace, 
         'id':id}

    def get_additional_info(self):
        args = {'app_version':ELECTRUM_VERSION, 
         'python_version':sys.version, 
         'os':self.get_os_version, 
         'wallet_type':'unknown', 
         'locale':locale.getdefaultlocale[0] or '?', 
         'description':self.get_user_description}
        try:
            args['wallet_type'] = self.get_wallet_type
        except:
            pass

        try:
            args['app_version'] = self.get_git_version
        except:
            pass

        return args

    @staticmethod
    def get_git_version():
        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        version = subprocess.check_output([
         'git', 'describe', '--always', '--dirty'],
          cwd=dir)
        return str(version, 'utf8').strip

    def get_report_string(self):
        info = self.get_additional_info
        info['traceback'] = ''.join((traceback.format_exception)(*self.exc_args))
        return (self.issue_template.format)(**info)

    def get_user_description(self):
        raise NotImplementedError

    def get_wallet_type(self):
        raise NotImplementedError

    def get_os_version(self):
        raise NotImplementedError