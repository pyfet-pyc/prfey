# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\support\expected_conditions.py
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebElement

class title_is(object):
    __doc__ = 'An expectation for checking the title of a page.\n    title is the expected title, which must be an exact match\n    returns True if the title matches, false otherwise.'

    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        return self.title == driver.title


class title_contains(object):
    __doc__ = ' An expectation for checking that the title contains a case-sensitive\n    substring. title is the fragment of title expected\n    returns True when the title matches, False otherwise\n    '

    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        return self.title in driver.title


class presence_of_element_located(object):
    __doc__ = ' An expectation for checking that an element is present on the DOM\n    of a page. This does not necessarily mean that the element is visible.\n    locator - used to find the element\n    returns the WebElement once it is located\n    '

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return _find_element(driver, self.locator)


class url_contains(object):
    __doc__ = ' An expectation for checking that the current url contains a\n    case-sensitive substring.\n    url is the fragment of url expected,\n    returns True when the url matches, False otherwise\n    '

    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        return self.url in driver.current_url


class url_matches(object):
    __doc__ = 'An expectation for checking the current url.\n    pattern is the expected pattern, which must be an exact match\n    returns True if the url matches, false otherwise.'

    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, driver):
        import re
        match = re.search(self.pattern, driver.current_url)
        return match is not None


class url_to_be(object):
    __doc__ = 'An expectation for checking the current url.\n    url is the expected url, which must be an exact match\n    returns True if the url matches, false otherwise.'

    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        return self.url == driver.current_url


class url_changes(object):
    __doc__ = 'An expectation for checking the current url.\n    url is the expected url, which must not be an exact match\n    returns True if the url is different, false otherwise.'

    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        return self.url != driver.current_url


class visibility_of_element_located(object):
    __doc__ = ' An expectation for checking that an element is present on the DOM of a\n    page and visible. Visibility means that the element is not only displayed\n    but also has a height and width that is greater than 0.\n    locator - used to find the element\n    returns the WebElement once it is located and visible\n    '

    def __init__(self, locator):
        self.locator = locator

    def __call__--- This code section failed: ---

 L. 127         0  SETUP_FINALLY        20  'to 20'

 L. 128         2  LOAD_GLOBAL              _element_if_visible
                4  LOAD_GLOBAL              _find_element
                6  LOAD_FAST                'driver'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                locator
               12  CALL_FUNCTION_2       2  ''
               14  CALL_FUNCTION_1       1  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 129        20  DUP_TOP          
               22  LOAD_GLOBAL              StaleElementReferenceException
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 130        34  POP_EXCEPT       
               36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 36


class visibility_of(object):
    __doc__ = ' An expectation for checking that an element, known to be present on the\n    DOM of a page, is visible. Visibility means that the element is not only\n    displayed but also has a height and width that is greater than 0.\n    element is the WebElement\n    returns the (same) WebElement once it is visible\n    '

    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        return _element_if_visible(self.element)


def _element_if_visible(element, visibility=True):
    if element.is_displayed() == visibility:
        return element
    return False


class presence_of_all_elements_located(object):
    __doc__ = ' An expectation for checking that there is at least one element present\n    on a web page.\n    locator is used to find the element\n    returns the list of WebElements once they are located\n    '

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return _find_elements(driver, self.locator)


class visibility_of_any_elements_located(object):
    __doc__ = ' An expectation for checking that there is at least one element visible\n    on a web page.\n    locator is used to find the element\n    returns the list of WebElements once they are located\n    '

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return [element for element in _find_elements(driver, self.locator) if _element_if_visible(element)]


class visibility_of_all_elements_located(object):
    __doc__ = ' An expectation for checking that all elements are present on the DOM of a\n    page and visible. Visibility means that the elements are not only displayed\n    but also has a height and width that is greater than 0.\n    locator - used to find the elements\n    returns the list of WebElements once they are located and visible\n    '

    def __init__(self, locator):
        self.locator = locator

    def __call__--- This code section failed: ---

 L. 188         0  SETUP_FINALLY        50  'to 50'

 L. 189         2  LOAD_GLOBAL              _find_elements
                4  LOAD_FAST                'driver'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                locator
               10  CALL_FUNCTION_2       2  ''
               12  STORE_FAST               'elements'

 L. 190        14  LOAD_FAST                'elements'
               16  GET_ITER         
             18_0  COME_FROM            42  '42'
             18_1  COME_FROM            32  '32'
               18  FOR_ITER             44  'to 44'
               20  STORE_FAST               'element'

 L. 191        22  LOAD_GLOBAL              _element_if_visible
               24  LOAD_FAST                'element'
               26  LOAD_CONST               False
               28  LOAD_CONST               ('visibility',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 192        34  POP_TOP          
               36  POP_BLOCK        
               38  LOAD_CONST               False
               40  RETURN_VALUE     
               42  JUMP_BACK            18  'to 18'
             44_0  COME_FROM            18  '18'

 L. 193        44  LOAD_FAST                'elements'
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY     0  '0'

 L. 194        50  DUP_TOP          
               52  LOAD_GLOBAL              StaleElementReferenceException
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    70  'to 70'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 195        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
             70_0  COME_FROM            56  '56'
               70  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 36


class text_to_be_present_in_element(object):
    __doc__ = ' An expectation for checking if the given text is present in the\n    specified element.\n    locator, text\n    '

    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__--- This code section failed: ---

 L. 208         0  SETUP_FINALLY        28  'to 28'

 L. 209         2  LOAD_GLOBAL              _find_element
                4  LOAD_FAST                'driver'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                locator
               10  CALL_FUNCTION_2       2  ''
               12  LOAD_ATTR                text
               14  STORE_FAST               'element_text'

 L. 210        16  LOAD_FAST                'self'
               18  LOAD_ATTR                text
               20  LOAD_FAST                'element_text'
               22  COMPARE_OP               in
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     0  '0'

 L. 211        28  DUP_TOP          
               30  LOAD_GLOBAL              StaleElementReferenceException
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 212        42  POP_EXCEPT       
               44  LOAD_CONST               False
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'
               48  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 44


class text_to_be_present_in_element_value(object):
    __doc__ = "\n    An expectation for checking if the given text is present in the element's\n    locator, text\n    "

    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__--- This code section failed: ---

 L. 225         0  SETUP_FINALLY        46  'to 46'

 L. 226         2  LOAD_GLOBAL              _find_element
                4  LOAD_FAST                'driver'

 L. 227         6  LOAD_FAST                'self'
                8  LOAD_ATTR                locator

 L. 226        10  CALL_FUNCTION_2       2  ''
               12  LOAD_METHOD              get_attribute

 L. 227        14  LOAD_STR                 'value'

 L. 226        16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'element_text'

 L. 228        20  LOAD_FAST                'element_text'
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 229        24  LOAD_FAST                'self'
               26  LOAD_ATTR                text
               28  LOAD_FAST                'element_text'
               30  COMPARE_OP               in
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'

 L. 231        36  POP_BLOCK        
               38  LOAD_CONST               False
               40  RETURN_VALUE     
               42  POP_BLOCK        
               44  JUMP_FORWARD         68  'to 68'
             46_0  COME_FROM_FINALLY     0  '0'

 L. 232        46  DUP_TOP          
               48  LOAD_GLOBAL              StaleElementReferenceException
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    66  'to 66'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 233        60  POP_EXCEPT       
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM            52  '52'
               66  END_FINALLY      
             68_0  COME_FROM            44  '44'

Parse error at or near `POP_BLOCK' instruction at offset 42


class frame_to_be_available_and_switch_to_it(object):
    __doc__ = ' An expectation for checking whether the given frame is available to\n    switch to.  If the frame is available it switches the given driver to the\n    specified frame.\n    '

    def __init__(self, locator):
        self.frame_locator = locator

    def __call__--- This code section failed: ---

 L. 245         0  SETUP_FINALLY        56  'to 56'

 L. 246         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                frame_locator
                8  LOAD_GLOBAL              tuple
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    36  'to 36'

 L. 247        14  LOAD_FAST                'driver'
               16  LOAD_ATTR                switch_to
               18  LOAD_METHOD              frame
               20  LOAD_GLOBAL              _find_element
               22  LOAD_FAST                'driver'

 L. 248        24  LOAD_FAST                'self'
               26  LOAD_ATTR                frame_locator

 L. 247        28  CALL_FUNCTION_2       2  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  JUMP_FORWARD         50  'to 50'
             36_0  COME_FROM            12  '12'

 L. 250        36  LOAD_FAST                'driver'
               38  LOAD_ATTR                switch_to
               40  LOAD_METHOD              frame
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                frame_locator
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
             50_0  COME_FROM            34  '34'

 L. 251        50  POP_BLOCK        
               52  LOAD_CONST               True
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY     0  '0'

 L. 252        56  DUP_TOP          
               58  LOAD_GLOBAL              NoSuchFrameException
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 253        70  POP_EXCEPT       
               72  LOAD_CONST               False
               74  RETURN_VALUE     
             76_0  COME_FROM            62  '62'
               76  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 56


class invisibility_of_element_located(object):
    __doc__ = ' An Expectation for checking that an element is either invisible or not\n    present on the DOM.\n\n    locator used to find the element\n    '

    def __init__(self, locator):
        self.target = locator

    def __call__--- This code section failed: ---

 L. 266         0  SETUP_FINALLY        40  'to 40'

 L. 267         2  LOAD_FAST                'self'
                4  LOAD_ATTR                target
                6  STORE_FAST               'target'

 L. 268         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'target'
               12  LOAD_GLOBAL              WebElement
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     28  'to 28'

 L. 269        18  LOAD_GLOBAL              _find_element
               20  LOAD_FAST                'driver'
               22  LOAD_FAST                'target'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'target'
             28_0  COME_FROM            16  '16'

 L. 270        28  LOAD_GLOBAL              _element_if_visible
               30  LOAD_FAST                'target'
               32  LOAD_CONST               False
               34  CALL_FUNCTION_2       2  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L. 271        40  DUP_TOP          
               42  LOAD_GLOBAL              NoSuchElementException
               44  LOAD_GLOBAL              StaleElementReferenceException
               46  BUILD_TUPLE_2         2 
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 277        58  POP_EXCEPT       
               60  LOAD_CONST               True
               62  RETURN_VALUE     
             64_0  COME_FROM            50  '50'
               64  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 60


class invisibility_of_element(invisibility_of_element_located):
    __doc__ = ' An Expectation for checking that an element is either invisible or not\n    present on the DOM.\n\n    element is either a locator (text) or an WebElement\n    '

    def __init(self, element):
        self.target = element


class element_to_be_clickable(object):
    __doc__ = ' An Expectation for checking an element is visible and enabled such that\n    you can click it.'

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = visibility_of_element_located(self.locator)(driver)
        if element:
            if element.is_enabled():
                return element
        return False


class staleness_of(object):
    __doc__ = ' Wait until an element is no longer attached to the DOM.\n    element is the element to wait for.\n    returns False if the element is still attached to the DOM, true otherwise.\n    '

    def __init__(self, element):
        self.element = element

    def __call__--- This code section failed: ---

 L. 313         0  SETUP_FINALLY        18  'to 18'

 L. 315         2  LOAD_FAST                'self'
                4  LOAD_ATTR                element
                6  LOAD_METHOD              is_enabled
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          

 L. 316        12  POP_BLOCK        
               14  LOAD_CONST               False
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 317        18  DUP_TOP          
               20  LOAD_GLOBAL              StaleElementReferenceException
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 318        32  POP_EXCEPT       
               34  LOAD_CONST               True
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 18


class element_to_be_selected(object):
    __doc__ = ' An expectation for checking the selection is selected.\n    element is WebElement object\n    '

    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        return self.element.is_selected()


class element_located_to_be_selected(object):
    __doc__ = 'An expectation for the element to be located is selected.\n    locator is a tuple of (by, path)'

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return _find_element(driver, self.locator).is_selected()


class element_selection_state_to_be(object):
    __doc__ = ' An expectation for checking if the given element is selected.\n    element is WebElement object\n    is_selected is a Boolean."\n    '

    def __init__(self, element, is_selected):
        self.element = element
        self.is_selected = is_selected

    def __call__(self, ignored):
        return self.element.is_selected() == self.is_selected


class element_located_selection_state_to_be(object):
    __doc__ = ' An expectation to locate an element and check if the selection state\n    specified is in that state.\n    locator is a tuple of (by, path)\n    is_selected is a boolean\n    '

    def __init__(self, locator, is_selected):
        self.locator = locator
        self.is_selected = is_selected

    def __call__--- This code section failed: ---

 L. 366         0  SETUP_FINALLY        30  'to 30'

 L. 367         2  LOAD_GLOBAL              _find_element
                4  LOAD_FAST                'driver'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                locator
               10  CALL_FUNCTION_2       2  ''
               12  STORE_FAST               'element'

 L. 368        14  LOAD_FAST                'element'
               16  LOAD_METHOD              is_selected
               18  CALL_METHOD_0         0  ''
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                is_selected
               24  COMPARE_OP               ==
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L. 369        30  DUP_TOP          
               32  LOAD_GLOBAL              StaleElementReferenceException
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 370        44  POP_EXCEPT       
               46  LOAD_CONST               False
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'
               50  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 46


class number_of_windows_to_be(object):
    __doc__ = ' An expectation for the number of windows to be a certain value.'

    def __init__(self, num_windows):
        self.num_windows = num_windows

    def __call__(self, driver):
        return len(driver.window_handles) == self.num_windows


class new_window_is_opened(object):
    __doc__ = ' An expectation that a new window will be opened and have the number of\n    windows handles increase'

    def __init__(self, current_handles):
        self.current_handles = current_handles

    def __call__(self, driver):
        return len(driver.window_handles) > len(self.current_handles)


class alert_is_present(object):
    __doc__ = ' Expect an alert to be present.'

    def __init__(self):
        pass

    def __call__--- This code section failed: ---

 L. 400         0  SETUP_FINALLY        16  'to 16'

 L. 401         2  LOAD_FAST                'driver'
                4  LOAD_ATTR                switch_to
                6  LOAD_ATTR                alert
                8  STORE_FAST               'alert'

 L. 402        10  LOAD_FAST                'alert'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 403        16  DUP_TOP          
               18  LOAD_GLOBAL              NoAlertPresentException
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 404        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 32


def _find_element--- This code section failed: ---

 L. 410         0  SETUP_FINALLY        14  'to 14'

 L. 411         2  LOAD_FAST                'driver'
                4  LOAD_ATTR                find_element
                6  LOAD_FAST                'by'
                8  CALL_FUNCTION_EX      0  'positional arguments only'
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 412        14  DUP_TOP          
               16  LOAD_GLOBAL              NoSuchElementException
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    50  'to 50'
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        38  'to 38'

 L. 413        30  LOAD_FAST                'e'
               32  RAISE_VARARGS_1       1  'exception instance'
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_FINALLY    28  '28'
               38  LOAD_CONST               None
               40  STORE_FAST               'e'
               42  DELETE_FAST              'e'
               44  END_FINALLY      
               46  POP_EXCEPT       
               48  JUMP_FORWARD         88  'to 88'
             50_0  COME_FROM            20  '20'

 L. 414        50  DUP_TOP          
               52  LOAD_GLOBAL              WebDriverException
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    86  'to 86'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        74  'to 74'

 L. 415        66  LOAD_FAST                'e'
               68  RAISE_VARARGS_1       1  'exception instance'
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
             74_0  COME_FROM_FINALLY    64  '64'
               74  LOAD_CONST               None
               76  STORE_FAST               'e'
               78  DELETE_FAST              'e'
               80  END_FINALLY      
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            56  '56'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            48  '48'

Parse error at or near `DUP_TOP' instruction at offset 50


def _find_elements(driver, by):
    try:
        return (driver.find_elements)(*by)
    except WebDriverException as e:
        try:
            raise e
        finally:
            e = None
            del e