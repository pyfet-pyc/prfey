# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\remote\webelement.py
import base64, hashlib, os, pkgutil, warnings, zipfile
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from .command import Command
try:
    str = basestring
except NameError:
    pass
else:
    try:
        from StringIO import StringIO as IOStream
    except ImportError:
        from io import BytesIO as IOStream
    else:
        _pkg = '.'.join(__name__.split('.')[:-1])
        getAttribute_js = pkgutil.get_data(_pkg, 'getAttribute.js').decode('utf8')
        isDisplayed_js = pkgutil.get_data(_pkg, 'isDisplayed.js').decode('utf8')

        class WebElement(object):
            __doc__ = 'Represents a DOM element.\n\n    Generally, all interesting operations that interact with a document will be\n    performed through this interface.\n\n    All method calls will do a freshness check to ensure that the element\n    reference is still valid.  This essentially determines whether or not the\n    element is still attached to the DOM.  If this test fails, then an\n    ``StaleElementReferenceException`` is thrown, and all future calls to this\n    instance will fail.'

            def __init__(self, parent, id_, w3c=False):
                self._parent = parent
                self._id = id_
                self._w3c = w3c

            def __repr__(self):
                return '<{0.__module__}.{0.__name__} (session="{1}", element="{2}")>'.format(type(self), self._parent.session_id, self._id)

            @property
            def tag_name(self):
                """This element's ``tagName`` property."""
                return self._execute(Command.GET_ELEMENT_TAG_NAME)['value']

            @property
            def text(self):
                """The text of the element."""
                return self._execute(Command.GET_ELEMENT_TEXT)['value']

            def click(self):
                """Clicks the element."""
                self._execute(Command.CLICK_ELEMENT)

            def submit(self):
                """Submits a form."""
                if self._w3c:
                    form = self.find_element(By.XPATH, './ancestor-or-self::form')
                    self._parent.execute_script("var e = arguments[0].ownerDocument.createEvent('Event');e.initEvent('submit', true, true);if (arguments[0].dispatchEvent(e)) { arguments[0].submit() }", form)
                else:
                    self._execute(Command.SUBMIT_ELEMENT)

            def clear(self):
                """Clears the text if it's a text entry element."""
                self._execute(Command.CLEAR_ELEMENT)

            def get_property(self, name):
                """
        Gets the given property of the element.

        :Args:
            - name - Name of the property to retrieve.

        Example::

            text_length = target_element.get_property("text_length")
        """
                try:
                    return self._execute(Command.GET_ELEMENT_PROPERTY, {'name': name})['value']
                except WebDriverException:
                    return self.parent.execute_script('return arguments[0][arguments[1]]', self, name)

            def get_attribute(self, name):
                """Gets the given attribute or property of the element.

        This method will first try to return the value of a property with the
        given name. If a property with that name doesn't exist, it returns the
        value of the attribute with the same name. If there's no attribute with
        that name, ``None`` is returned.

        Values which are considered truthy, that is equals "true" or "false",
        are returned as booleans.  All other non-``None`` values are returned
        as strings.  For attributes or properties which do not exist, ``None``
        is returned.

        :Args:
            - name - Name of the attribute/property to retrieve.

        Example::

            # Check if the "active" CSS class is applied to an element.
            is_active = "active" in target_element.get_attribute("class")

        """
                attributeValue = ''
                if self._w3c:
                    attributeValue = self.parent.execute_script('return (%s).apply(null, arguments);' % getAttribute_js, self, name)
                else:
                    resp = self._execute(Command.GET_ELEMENT_ATTRIBUTE, {'name': name})
                    attributeValue = resp.get('value')
                    if attributeValue is not None:
                        if name != 'value':
                            if attributeValue.lower() in ('true', 'false'):
                                attributeValue = attributeValue.lower()
                return attributeValue

            def is_selected(self):
                """Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
                return self._execute(Command.IS_ELEMENT_SELECTED)['value']

            def is_enabled(self):
                """Returns whether the element is enabled."""
                return self._execute(Command.IS_ELEMENT_ENABLED)['value']

            def find_element_by_id(self, id_):
                r"""Finds element within this element's children by ID.

        :Args:
         - id\_ - ID of child element to locate.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            foo_element = element.find_element_by_id('foo')
        """
                return self.find_element(by=(By.ID), value=id_)

            def find_elements_by_id(self, id_):
                r"""Finds a list of elements within this element's children by ID.
        Will return a list of webelements if found, or an empty list if not.

        :Args:
         - id\_ - Id of child element to find.

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_id('foo')
        """
                return self.find_elements(by=(By.ID), value=id_)

            def find_element_by_name(self, name):
                """Finds element within this element's children by name.

        :Args:
         - name - name property of the element to find.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_name('foo')
        """
                return self.find_element(by=(By.NAME), value=name)

            def find_elements_by_name(self, name):
                """Finds a list of elements within this element's children by name.

        :Args:
         - name - name property to search for.

        :Returns:
         - list of webelement - a list with elements if any was found.  an
           empty list if not

        :Usage:
            elements = element.find_elements_by_name('foo')
        """
                return self.find_elements(by=(By.NAME), value=name)

            def find_element_by_link_text(self, link_text):
                """Finds element within this element's children by visible link text.

        :Args:
         - link_text - Link text string to search for.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_link_text('Sign In')
        """
                return self.find_element(by=(By.LINK_TEXT), value=link_text)

            def find_elements_by_link_text(self, link_text):
                """Finds a list of elements within this element's children by visible link text.

        :Args:
         - link_text - Link text string to search for.

        :Returns:
         - list of webelement - a list with elements if any was found.  an
           empty list if not

        :Usage:
            elements = element.find_elements_by_link_text('Sign In')
        """
                return self.find_elements(by=(By.LINK_TEXT), value=link_text)

            def find_element_by_partial_link_text(self, link_text):
                """Finds element within this element's children by partially visible link text.

        :Args:
         - link_text: The text of the element to partially match on.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_partial_link_text('Sign')
        """
                return self.find_element(by=(By.PARTIAL_LINK_TEXT), value=link_text)

            def find_elements_by_partial_link_text(self, link_text):
                """Finds a list of elements within this element's children by link text.

        :Args:
         - link_text: The text of the element to partial match on.

        :Returns:
         - list of webelement - a list with elements if any was found.  an
           empty list if not

        :Usage:
            elements = element.find_elements_by_partial_link_text('Sign')
        """
                return self.find_elements(by=(By.PARTIAL_LINK_TEXT), value=link_text)

            def find_element_by_tag_name(self, name):
                """Finds element within this element's children by tag name.

        :Args:
         - name - name of html tag (eg: h1, a, span)

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_tag_name('h1')
        """
                return self.find_element(by=(By.TAG_NAME), value=name)

            def find_elements_by_tag_name(self, name):
                """Finds a list of elements within this element's children by tag name.

        :Args:
         - name - name of html tag (eg: h1, a, span)

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_tag_name('h1')
        """
                return self.find_elements(by=(By.TAG_NAME), value=name)

            def find_element_by_xpath(self, xpath):
                """Finds element by xpath.

        :Args:
         - xpath - xpath of element to locate.  "//input[@class='myelement']"

        Note: The base path will be relative to this element's location.

        This will select the first link under this element.

        ::

            myelement.find_element_by_xpath(".//a")

        However, this will select the first link on the page.

        ::

            myelement.find_element_by_xpath("//a")

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_xpath('//div/td[1]')
        """
                return self.find_element(by=(By.XPATH), value=xpath)

            def find_elements_by_xpath(self, xpath):
                """Finds elements within the element by xpath.

        :Args:
         - xpath - xpath locator string.

        Note: The base path will be relative to this element's location.

        This will select all links under this element.

        ::

            myelement.find_elements_by_xpath(".//a")

        However, this will select all links in the page itself.

        ::

            myelement.find_elements_by_xpath("//a")

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_xpath("//div[contains(@class, 'foo')]")

        """
                return self.find_elements(by=(By.XPATH), value=xpath)

            def find_element_by_class_name(self, name):
                """Finds element within this element's children by class name.

        :Args:
         - name: The class name of the element to find.

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_class_name('foo')
        """
                return self.find_element(by=(By.CLASS_NAME), value=name)

            def find_elements_by_class_name(self, name):
                """Finds a list of elements within this element's children by class name.

        :Args:
         - name: The class name of the elements to find.

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_class_name('foo')
        """
                return self.find_elements(by=(By.CLASS_NAME), value=name)

            def find_element_by_css_selector(self, css_selector):
                """Finds element within this element's children by CSS selector.

        :Args:
         - css_selector - CSS selector string, ex: 'a.nav#home'

        :Returns:
         - WebElement - the element if it was found

        :Raises:
         - NoSuchElementException - if the element wasn't found

        :Usage:
            element = element.find_element_by_css_selector('#foo')
        """
                return self.find_element(by=(By.CSS_SELECTOR), value=css_selector)

            def find_elements_by_css_selector(self, css_selector):
                """Finds a list of elements within this element's children by CSS selector.

        :Args:
         - css_selector - CSS selector string, ex: 'a.nav#home'

        :Returns:
         - list of WebElement - a list with elements if any was found.  An
           empty list if not

        :Usage:
            elements = element.find_elements_by_css_selector('.foo')
        """
                return self.find_elements(by=(By.CSS_SELECTOR), value=css_selector)

            def send_keys(self, *value):
                """Simulates typing into the element.

        :Args:
            - value - A string for typing, or setting form fields.  For setting
              file inputs, this could be a local file path.

        Use this to send simple key events or to fill out form fields::

            form_textfield = driver.find_element_by_name('username')
            form_textfield.send_keys("admin")

        This can also be used to set file inputs.

        ::

            file_input = driver.find_element_by_name('profilePic')
            file_input.send_keys("path/to/profilepic.gif")
            # Generally it's better to wrap the file path in one of the methods
            # in os.path to return the actual path to support cross OS testing.
            # file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))

        """
                if self.parent._is_remote:
                    local_file = (self.parent.file_detector.is_local_file)(*value)
                    if local_file is not None:
                        value = self._upload(local_file)
                self._execute(Command.SEND_KEYS_TO_ELEMENT, {'text':''.join(keys_to_typing(value)), 
                 'value':keys_to_typing(value)})

            def is_displayed(self):
                """Whether the element is visible to a user."""
                if self._w3c:
                    return self.parent.execute_script('return (%s).apply(null, arguments);' % isDisplayed_js, self)
                return self._execute(Command.IS_ELEMENT_DISPLAYED)['value']

            @property
            def location_once_scrolled_into_view(self):
                """THIS PROPERTY MAY CHANGE WITHOUT WARNING. Use this to discover
        where on the screen an element is so that we can click it. This method
        should cause the element to be scrolled into view.

        Returns the top lefthand corner location on the screen, or ``None`` if
        the element is not visible.

        """
                if self._w3c:
                    old_loc = self._execute(Command.W3C_EXECUTE_SCRIPT, {'script':'arguments[0].scrollIntoView(true); return arguments[0].getBoundingClientRect()', 
                     'args':[
                      self]})['value']
                    return {'x':round(old_loc['x']), 
                     'y':round(old_loc['y'])}
                return self._execute(Command.GET_ELEMENT_LOCATION_ONCE_SCROLLED_INTO_VIEW)['value']

            @property
            def size(self):
                """The size of the element."""
                size = {}
                if self._w3c:
                    size = self._execute(Command.GET_ELEMENT_RECT)['value']
                else:
                    size = self._execute(Command.GET_ELEMENT_SIZE)['value']
                new_size = {'height':size['height'], 
                 'width':size['width']}
                return new_size

            def value_of_css_property(self, property_name):
                """The value of a CSS property."""
                return self._execute(Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY, {'propertyName': property_name})['value']

            @property
            def location(self):
                """The location of the element in the renderable canvas."""
                if self._w3c:
                    old_loc = self._execute(Command.GET_ELEMENT_RECT)['value']
                else:
                    old_loc = self._execute(Command.GET_ELEMENT_LOCATION)['value']
                new_loc = {'x':round(old_loc['x']), 
                 'y':round(old_loc['y'])}
                return new_loc

            @property
            def rect(self):
                """A dictionary with the size and location of the element."""
                if self._w3c:
                    return self._execute(Command.GET_ELEMENT_RECT)['value']
                rect = self.size.copy()
                rect.update(self.location)
                return rect

            @property
            def screenshot_as_base64(self):
                """
        Gets the screenshot of the current element as a base64 encoded string.

        :Usage:
            img_b64 = element.screenshot_as_base64
        """
                return self._execute(Command.ELEMENT_SCREENSHOT)['value']

            @property
            def screenshot_as_png(self):
                """
        Gets the screenshot of the current element as a binary data.

        :Usage:
            element_png = element.screenshot_as_png
        """
                return base64.b64decode(self.screenshot_as_base64.encode('ascii'))

            def screenshot--- This code section failed: ---

 L. 582         0  LOAD_FAST                'filename'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  LOAD_METHOD              endswith
                8  LOAD_STR                 '.png'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_TRUE     26  'to 26'

 L. 583        14  LOAD_GLOBAL              warnings
               16  LOAD_METHOD              warn
               18  LOAD_STR                 'name used for saved screenshot does not match file type. It should end with a `.png` extension'

 L. 584        20  LOAD_GLOBAL              UserWarning

 L. 583        22  CALL_METHOD_2         2  ''
               24  POP_TOP          
             26_0  COME_FROM            12  '12'

 L. 585        26  LOAD_FAST                'self'
               28  LOAD_ATTR                screenshot_as_png
               30  STORE_FAST               'png'

 L. 586        32  SETUP_FINALLY       102  'to 102'
               34  SETUP_FINALLY        72  'to 72'

 L. 587        36  LOAD_GLOBAL              open
               38  LOAD_FAST                'filename'
               40  LOAD_STR                 'wb'
               42  CALL_FUNCTION_2       2  ''
               44  SETUP_WITH           62  'to 62'
               46  STORE_FAST               'f'

 L. 588        48  LOAD_FAST                'f'
               50  LOAD_METHOD              write
               52  LOAD_FAST                'png'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  POP_BLOCK        
               60  BEGIN_FINALLY    
             62_0  COME_FROM_WITH       44  '44'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      
               68  POP_BLOCK        
               70  JUMP_FORWARD         98  'to 98'
             72_0  COME_FROM_FINALLY    34  '34'

 L. 589        72  DUP_TOP          
               74  LOAD_GLOBAL              IOError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    96  'to 96'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 590        86  POP_EXCEPT       
               88  POP_BLOCK        
               90  CALL_FINALLY        102  'to 102'
               92  LOAD_CONST               False
               94  RETURN_VALUE     
             96_0  COME_FROM            78  '78'
               96  END_FINALLY      
             98_0  COME_FROM            70  '70'
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM            90  '90'
            102_1  COME_FROM_FINALLY    32  '32'

 L. 592       102  DELETE_FAST              'png'
              104  END_FINALLY      

 L. 593       106  LOAD_CONST               True
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 90

            @property
            def parent(self):
                """Internal reference to the WebDriver instance this element was found from."""
                return self._parent

            @property
            def id(self):
                """Internal ID used by selenium.

        This is mainly for internal use. Simple use cases such as checking if 2
        webelements refer to the same element, can be done using ``==``::

            if element1 == element2:
                print("These 2 are equal")

        """
                return self._id

            def __eq__(self, element):
                return hasattrelement'id' and self._id == element.id

            def __ne__(self, element):
                return not self.__eq__(element)

            def _execute(self, command, params=None):
                """Executes a command against the underlying HTML element.

        Args:
          command: The name of the command to _execute as a string.
          params: A dictionary of named parameters to send with the command.

        Returns:
          The command's JSON response loaded into a dictionary object.
        """
                if not params:
                    params = {}
                params['id'] = self._id
                return self._parent.execute(command, params)

            def find_element(self, by=By.ID, value=None):
                """
        Find an element given a By strategy and locator. Prefer the find_element_by_* methods when
        possible.

        :Usage:
            element = element.find_element(By.ID, 'foo')

        :rtype: WebElement
        """
                if self._w3c:
                    if by == By.ID:
                        by = By.CSS_SELECTOR
                        value = '[id="%s"]' % value
                    elif by == By.TAG_NAME:
                        by = By.CSS_SELECTOR
                    elif by == By.CLASS_NAME:
                        by = By.CSS_SELECTOR
                        value = '.%s' % value
                    elif by == By.NAME:
                        by = By.CSS_SELECTOR
                        value = '[name="%s"]' % value
                return self._execute(Command.FIND_CHILD_ELEMENT, {'using':by, 
                 'value':value})['value']

            def find_elements(self, by=By.ID, value=None):
                """
        Find elements given a By strategy and locator. Prefer the find_elements_by_* methods when
        possible.

        :Usage:
            element = element.find_elements(By.CLASS_NAME, 'foo')

        :rtype: list of WebElement
        """
                if self._w3c:
                    if by == By.ID:
                        by = By.CSS_SELECTOR
                        value = '[id="%s"]' % value
                    elif by == By.TAG_NAME:
                        by = By.CSS_SELECTOR
                    elif by == By.CLASS_NAME:
                        by = By.CSS_SELECTOR
                        value = '.%s' % value
                    elif by == By.NAME:
                        by = By.CSS_SELECTOR
                        value = '[name="%s"]' % value
                return self._execute(Command.FIND_CHILD_ELEMENTS, {'using':by, 
                 'value':value})['value']

            def __hash__(self):
                return inthashlib.md5(self._id.encode('utf-8')).hexdigest()16

            def _upload--- This code section failed: ---

 L. 691         0  LOAD_GLOBAL              IOStream
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'fp'

 L. 692         6  LOAD_GLOBAL              zipfile
                8  LOAD_METHOD              ZipFile
               10  LOAD_FAST                'fp'
               12  LOAD_STR                 'w'
               14  LOAD_GLOBAL              zipfile
               16  LOAD_ATTR                ZIP_DEFLATED
               18  CALL_METHOD_3         3  ''
               20  STORE_FAST               'zipped'

 L. 693        22  LOAD_FAST                'zipped'
               24  LOAD_METHOD              write
               26  LOAD_FAST                'filename'
               28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              split
               34  LOAD_FAST                'filename'
               36  CALL_METHOD_1         1  ''
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          

 L. 694        46  LOAD_FAST                'zipped'
               48  LOAD_METHOD              close
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 695        54  LOAD_GLOBAL              base64
               56  LOAD_METHOD              encodestring
               58  LOAD_FAST                'fp'
               60  LOAD_METHOD              getvalue
               62  CALL_METHOD_0         0  ''
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'content'

 L. 696        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'content'
               72  LOAD_GLOBAL              str
               74  CALL_FUNCTION_2       2  ''
               76  POP_JUMP_IF_TRUE     88  'to 88'

 L. 697        78  LOAD_FAST                'content'
               80  LOAD_METHOD              decode
               82  LOAD_STR                 'utf-8'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'content'
             88_0  COME_FROM            76  '76'

 L. 698        88  SETUP_FINALLY       114  'to 114'

 L. 699        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _execute
               94  LOAD_GLOBAL              Command
               96  LOAD_ATTR                UPLOAD_FILE
               98  LOAD_STR                 'file'
              100  LOAD_FAST                'content'
              102  BUILD_MAP_1           1 
              104  CALL_METHOD_2         2  ''
              106  LOAD_STR                 'value'
              108  BINARY_SUBSCR    
              110  POP_BLOCK        
              112  RETURN_VALUE     
            114_0  COME_FROM_FINALLY    88  '88'

 L. 700       114  DUP_TOP          
              116  LOAD_GLOBAL              WebDriverException
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   222  'to 222'
              122  POP_TOP          
              124  STORE_FAST               'e'
              126  POP_TOP          
              128  SETUP_FINALLY       210  'to 210'

 L. 701       130  LOAD_STR                 'Unrecognized command: POST'
              132  LOAD_FAST                'e'
              134  LOAD_METHOD              __str__
              136  CALL_METHOD_0         0  ''
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L. 702       142  LOAD_FAST                'filename'
              144  ROT_FOUR         
              146  POP_BLOCK        
              148  POP_EXCEPT       
              150  CALL_FINALLY        210  'to 210'
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L. 703       154  LOAD_STR                 'Command not found: POST '
              156  LOAD_FAST                'e'
              158  LOAD_METHOD              __str__
              160  CALL_METHOD_0         0  ''
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   178  'to 178'

 L. 704       166  LOAD_FAST                'filename'
              168  ROT_FOUR         
              170  POP_BLOCK        
              172  POP_EXCEPT       
              174  CALL_FINALLY        210  'to 210'
              176  RETURN_VALUE     
            178_0  COME_FROM           164  '164'

 L. 705       178  LOAD_STR                 '{"status":405,"value":["GET","HEAD","DELETE"]}'
              180  LOAD_FAST                'e'
              182  LOAD_METHOD              __str__
              184  CALL_METHOD_0         0  ''
              186  COMPARE_OP               in
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L. 706       190  LOAD_FAST                'filename'
              192  ROT_FOUR         
              194  POP_BLOCK        
              196  POP_EXCEPT       
              198  CALL_FINALLY        210  'to 210'
              200  RETURN_VALUE     
            202_0  COME_FROM           188  '188'

 L. 708       202  LOAD_FAST                'e'
              204  RAISE_VARARGS_1       1  'exception instance'
              206  POP_BLOCK        
              208  BEGIN_FINALLY    
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           174  '174'
            210_2  COME_FROM           150  '150'
            210_3  COME_FROM_FINALLY   128  '128'
              210  LOAD_CONST               None
              212  STORE_FAST               'e'
              214  DELETE_FAST              'e'
              216  END_FINALLY      
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           120  '120'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'

Parse error at or near `POP_BLOCK' instruction at offset 146