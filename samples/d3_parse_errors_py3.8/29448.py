# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\support\wait.py
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
POLL_FREQUENCY = 0.5
IGNORED_EXCEPTIONS = (NoSuchElementException,)

class WebDriverWait(object):

    def __init__(self, driver, timeout, poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        r"""Constructor, takes a WebDriver instance and timeout in seconds.

           :Args:
            - driver - Instance of WebDriver (Ie, Firefox, Chrome or Remote)
            - timeout - Number of seconds before timing out
            - poll_frequency - sleep interval between calls
              By default, it is 0.5 second.
            - ignored_exceptions - iterable structure of exception classes ignored during calls.
              By default, it contains NoSuchElementException only.

           Example:
            from selenium.webdriver.support.ui import WebDriverWait 

            element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("someId")) 

            is_disappeared = WebDriverWait(driver, 30, 1, (ElementNotVisibleException)).\ 

                        until_not(lambda x: x.find_element_by_id("someId").is_displayed())
        """
        self._driver = driver
        self._timeout = timeout
        self._poll = poll_frequency
        if self._poll == 0:
            self._poll = POLL_FREQUENCY
        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:
                exceptions.append(ignored_exceptions)

        self._ignored_exceptions = tuple(exceptions)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(type(self), self._driver.session_id)

    def until--- This code section failed: ---

 L.  65         0  LOAD_CONST               None
                2  STORE_FAST               'screen'

 L.  66         4  LOAD_CONST               None
                6  STORE_FAST               'stacktrace'

 L.  68         8  LOAD_GLOBAL              time
               10  LOAD_METHOD              time
               12  CALL_METHOD_0         0  ''
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _timeout
               18  BINARY_ADD       
               20  STORE_FAST               'end_time'
             22_0  COME_FROM           134  '134'
             22_1  COME_FROM           130  '130'

 L.  70        22  SETUP_FINALLY        48  'to 48'

 L.  71        24  LOAD_FAST                'method'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _driver
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'value'

 L.  72        34  LOAD_FAST                'value'
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L.  73        38  LOAD_FAST                'value'
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'
               44  POP_BLOCK        
               46  JUMP_FORWARD        108  'to 108'
             48_0  COME_FROM_FINALLY    22  '22'

 L.  74        48  DUP_TOP          
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _ignored_exceptions
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE   106  'to 106'
               58  POP_TOP          
               60  STORE_FAST               'exc'
               62  POP_TOP          
               64  SETUP_FINALLY        94  'to 94'

 L.  75        66  LOAD_GLOBAL              getattr
               68  LOAD_FAST                'exc'
               70  LOAD_STR                 'screen'
               72  LOAD_CONST               None
               74  CALL_FUNCTION_3       3  ''
               76  STORE_FAST               'screen'

 L.  76        78  LOAD_GLOBAL              getattr
               80  LOAD_FAST                'exc'
               82  LOAD_STR                 'stacktrace'
               84  LOAD_CONST               None
               86  CALL_FUNCTION_3       3  ''
               88  STORE_FAST               'stacktrace'
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_FINALLY    64  '64'
               94  LOAD_CONST               None
               96  STORE_FAST               'exc'
               98  DELETE_FAST              'exc'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            56  '56'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            46  '46'

 L.  77       108  LOAD_GLOBAL              time
              110  LOAD_METHOD              sleep
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _poll
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L.  78       120  LOAD_GLOBAL              time
              122  LOAD_METHOD              time
              124  CALL_METHOD_0         0  ''
              126  LOAD_FAST                'end_time'
              128  COMPARE_OP               >
              130  POP_JUMP_IF_FALSE_BACK    22  'to 22'

 L.  79       132  JUMP_FORWARD        136  'to 136'
              134  JUMP_BACK            22  'to 22'
            136_0  COME_FROM           132  '132'

 L.  80       136  LOAD_GLOBAL              TimeoutException
              138  LOAD_FAST                'message'
              140  LOAD_FAST                'screen'
              142  LOAD_FAST                'stacktrace'
              144  CALL_FUNCTION_3       3  ''
              146  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `JUMP_BACK' instruction at offset 134

    def until_not--- This code section failed: ---

 L.  85         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _timeout
               10  BINARY_ADD       
               12  STORE_FAST               'end_time'
             14_0  COME_FROM            90  '90'
             14_1  COME_FROM            86  '86'

 L.  87        14  SETUP_FINALLY        40  'to 40'

 L.  88        16  LOAD_FAST                'method'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _driver
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'value'

 L.  89        26  LOAD_FAST                'value'
               28  POP_JUMP_IF_TRUE     36  'to 36'

 L.  90        30  LOAD_FAST                'value'
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'
               36  POP_BLOCK        
               38  JUMP_FORWARD         64  'to 64'
             40_0  COME_FROM_FINALLY    14  '14'

 L.  91        40  DUP_TOP          
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _ignored_exceptions
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  92        56  POP_EXCEPT       
               58  LOAD_CONST               True
               60  RETURN_VALUE     
             62_0  COME_FROM            48  '48'
               62  END_FINALLY      
             64_0  COME_FROM            38  '38'

 L.  93        64  LOAD_GLOBAL              time
               66  LOAD_METHOD              sleep
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _poll
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L.  94        76  LOAD_GLOBAL              time
               78  LOAD_METHOD              time
               80  CALL_METHOD_0         0  ''
               82  LOAD_FAST                'end_time'
               84  COMPARE_OP               >
               86  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L.  95        88  JUMP_FORWARD         92  'to 92'
               90  JUMP_BACK            14  'to 14'
             92_0  COME_FROM            88  '88'

 L.  96        92  LOAD_GLOBAL              TimeoutException
               94  LOAD_FAST                'message'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `JUMP_BACK' instruction at offset 90