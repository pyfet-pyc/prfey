# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\remote\switch_to.py
from .command import Command
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, NoSuchWindowException
try:
    basestring
except NameError:
    basestring = str
else:

    class SwitchTo:

        def __init__(self, driver):
            self._driver = driver

        @property
        def active_element(self):
            """
        Returns the element with focus, or BODY if nothing has focus.

        :Usage:
            element = driver.switch_to.active_element
        """
            if self._driver.w3c:
                return self._driver.execute(Command.W3C_GET_ACTIVE_ELEMENT)['value']
            return self._driver.execute(Command.GET_ACTIVE_ELEMENT)['value']

        @property
        def alert(self):
            """
        Switches focus to an alert on the page.

        :Usage:
            alert = driver.switch_to.alert
        """
            alert = Alert(self._driver)
            alert.text
            return alert

        def default_content(self):
            """
        Switch focus to the default frame.

        :Usage:
            driver.switch_to.default_content()
        """
            self._driver.execute(Command.SWITCH_TO_FRAME, {'id': None})

        def frame(self, frame_reference):
            """
        Switches focus to the specified frame, by index, name, or webelement.

        :Args:
         - frame_reference: The name of the window to switch to, an integer representing the index,
                            or a webelement that is an (i)frame to switch to.

        :Usage:
            driver.switch_to.frame('frame_name')
            driver.switch_to.frame(1)
            driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        """
            if not isinstance(frame_reference, basestring) or self._driver.w3c:
                try:
                    frame_reference = self._driver.find_element(By.ID, frame_reference)
                except NoSuchElementException:
                    try:
                        frame_reference = self._driver.find_element(By.NAME, frame_reference)
                    except NoSuchElementException:
                        raise NoSuchFrameException(frame_reference)

                else:
                    self._driver.execute(Command.SWITCH_TO_FRAME, {'id': frame_reference})

        def parent_frame(self):
            """
        Switches focus to the parent context. If the current context is the top
        level browsing context, the context remains unchanged.

        :Usage:
            driver.switch_to.parent_frame()
        """
            self._driver.execute(Command.SWITCH_TO_PARENT_FRAME)

        def window(self, window_name):
            """
        Switches focus to the specified window.

        :Args:
         - window_name: The name or window handle of the window to switch to.

        :Usage:
            driver.switch_to.window('main')
        """
            if self._driver.w3c:
                self._w3c_window(window_name)
                return
            data = {'name': window_name}
            self._driver.execute(Command.SWITCH_TO_WINDOW, data)

        def _w3c_window--- This code section failed: ---

 L. 118         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object send_handle>
                6  LOAD_STR                 'SwitchTo._w3c_window.<locals>.send_handle'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'send_handle'

 L. 121        12  SETUP_FINALLY        26  'to 26'

 L. 123        14  LOAD_FAST                'send_handle'
               16  LOAD_FAST                'window_name'
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD        138  'to 138'
             26_0  COME_FROM_FINALLY    12  '12'

 L. 124        26  DUP_TOP          
               28  LOAD_GLOBAL              NoSuchWindowException
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE   136  'to 136'
               34  POP_TOP          
               36  STORE_FAST               'e'
               38  POP_TOP          
               40  SETUP_FINALLY       124  'to 124'

 L. 126        42  LOAD_DEREF               'self'
               44  LOAD_ATTR                _driver
               46  LOAD_ATTR                current_window_handle
               48  STORE_FAST               'original_handle'

 L. 127        50  LOAD_DEREF               'self'
               52  LOAD_ATTR                _driver
               54  LOAD_ATTR                window_handles
               56  STORE_FAST               'handles'

 L. 128        58  LOAD_FAST                'handles'
               60  GET_ITER         
             62_0  COME_FROM           106  '106'
             62_1  COME_FROM            92  '92'
               62  FOR_ITER            108  'to 108'
               64  STORE_FAST               'handle'

 L. 129        66  LOAD_FAST                'send_handle'
               68  LOAD_FAST                'handle'
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          

 L. 130        74  LOAD_DEREF               'self'
               76  LOAD_ATTR                _driver
               78  LOAD_METHOD              execute_script
               80  LOAD_STR                 'return window.name'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'current_name'

 L. 131        86  LOAD_FAST                'window_name'
               88  LOAD_FAST                'current_name'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE_BACK    62  'to 62'

 L. 132        94  POP_TOP          
               96  POP_BLOCK        
               98  POP_EXCEPT       
              100  CALL_FINALLY        124  'to 124'
              102  LOAD_CONST               None
              104  RETURN_VALUE     
              106  JUMP_BACK            62  'to 62'
            108_0  COME_FROM            62  '62'

 L. 133       108  LOAD_FAST                'send_handle'
              110  LOAD_FAST                'original_handle'
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          

 L. 134       116  LOAD_FAST                'e'
              118  RAISE_VARARGS_1       1  'exception instance'
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM           100  '100'
            124_1  COME_FROM_FINALLY    40  '40'
              124  LOAD_CONST               None
              126  STORE_FAST               'e'
              128  DELETE_FAST              'e'
              130  END_FINALLY      
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM            32  '32'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM            24  '24'

Parse error at or near `POP_BLOCK' instruction at offset 96