# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\case.py
"""Test case implementation"""
import sys, functools, difflib, pprint, re, warnings, collections, contextlib, traceback, types
from . import result
from .util import strclass, safe_repr, _count_diff_all_purpose, _count_diff_hashable, _common_shorten_repr
__unittest = True
_subtest_msg_sentinel = object()
DIFF_OMITTED = '\nDiff is %s characters long. Set self.maxDiff to None to see it.'

class SkipTest(Exception):
    __doc__ = '\n    Raise this exception in a test to skip it.\n\n    Usually you can use TestCase.skipTest() or one of the skipping decorators\n    instead of raising this directly.\n    '


class _ShouldStop(Exception):
    __doc__ = '\n    The test should stop.\n    '


class _UnexpectedSuccess(Exception):
    __doc__ = "\n    The test was supposed to fail, but it didn't!\n    "


class _Outcome(object):

    def __init__(self, result=None):
        self.expecting_failure = False
        self.result = result
        self.result_supports_subtests = hasattr(result, 'addSubTest')
        self.success = True
        self.skipped = []
        self.expectedFailure = None
        self.errors = []

    @contextlib.contextmanager
    def testPartExecutor--- This code section failed: ---

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                success
                4  STORE_FAST               'old_success'

 L.  57         6  LOAD_CONST               True
                8  LOAD_FAST                'self'
               10  STORE_ATTR               success

 L.  58        12  SETUP_FINALLY       224  'to 224'
               14  SETUP_FINALLY        26  'to 26'

 L.  59        16  LOAD_CONST               None
               18  YIELD_VALUE      
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD        180  'to 180'
             26_0  COME_FROM_FINALLY    14  '14'

 L.  60        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyboardInterrupt
               30  <121>                44  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  61        38  RAISE_VARARGS_0       0  'reraise'
               40  POP_EXCEPT       
               42  JUMP_FORWARD        208  'to 208'

 L.  62        44  DUP_TOP          
               46  LOAD_GLOBAL              SkipTest
               48  <121>               104  ''
               50  POP_TOP          
               52  STORE_FAST               'e'
               54  POP_TOP          
               56  SETUP_FINALLY        96  'to 96'

 L.  63        58  LOAD_CONST               False
               60  LOAD_FAST                'self'
               62  STORE_ATTR               success

 L.  64        64  LOAD_FAST                'self'
               66  LOAD_ATTR                skipped
               68  LOAD_METHOD              append
               70  LOAD_FAST                'test_case'
               72  LOAD_GLOBAL              str
               74  LOAD_FAST                'e'
               76  CALL_FUNCTION_1       1  ''
               78  BUILD_TUPLE_2         2 
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  JUMP_FORWARD        208  'to 208'
             96_0  COME_FROM_FINALLY    56  '56'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  <48>             

 L.  65       104  DUP_TOP          
              106  LOAD_GLOBAL              _ShouldStop
              108  <121>               120  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.  66       116  POP_EXCEPT       
              118  JUMP_FORWARD        208  'to 208'

 L.  67       120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L.  68       126  LOAD_GLOBAL              sys
              128  LOAD_METHOD              exc_info
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'exc_info'

 L.  69       134  LOAD_FAST                'self'
              136  LOAD_ATTR                expecting_failure
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.  70       140  LOAD_FAST                'exc_info'
              142  LOAD_FAST                'self'
              144  STORE_ATTR               expectedFailure
              146  JUMP_FORWARD        170  'to 170'
            148_0  COME_FROM           138  '138'

 L.  72       148  LOAD_CONST               False
              150  LOAD_FAST                'self'
              152  STORE_ATTR               success

 L.  73       154  LOAD_FAST                'self'
              156  LOAD_ATTR                errors
              158  LOAD_METHOD              append
              160  LOAD_FAST                'test_case'
              162  LOAD_FAST                'exc_info'
              164  BUILD_TUPLE_2         2 
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
            170_0  COME_FROM           146  '146'

 L.  76       170  LOAD_CONST               None
              172  STORE_FAST               'exc_info'
              174  POP_EXCEPT       
              176  JUMP_FORWARD        208  'to 208'
              178  <48>             
            180_0  COME_FROM            24  '24'

 L.  78       180  LOAD_FAST                'self'
              182  LOAD_ATTR                result_supports_subtests
              184  POP_JUMP_IF_FALSE   208  'to 208'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                success
              190  POP_JUMP_IF_FALSE   208  'to 208'

 L.  79       192  LOAD_FAST                'self'
              194  LOAD_ATTR                errors
              196  LOAD_METHOD              append
              198  LOAD_FAST                'test_case'
              200  LOAD_CONST               None
              202  BUILD_TUPLE_2         2 
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
            208_0  COME_FROM           190  '190'
            208_1  COME_FROM           184  '184'
            208_2  COME_FROM           176  '176'
            208_3  COME_FROM           118  '118'
            208_4  COME_FROM            94  '94'
            208_5  COME_FROM            42  '42'
              208  POP_BLOCK        

 L.  81       210  LOAD_FAST                'self'
              212  LOAD_ATTR                success
              214  JUMP_IF_FALSE_OR_POP   218  'to 218'
              216  LOAD_FAST                'old_success'
            218_0  COME_FROM           214  '214'
              218  LOAD_FAST                'self'
              220  STORE_ATTR               success
              222  JUMP_FORWARD        238  'to 238'
            224_0  COME_FROM_FINALLY    12  '12'
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                success
              228  JUMP_IF_FALSE_OR_POP   232  'to 232'
              230  LOAD_FAST                'old_success'
            232_0  COME_FROM           228  '228'
              232  LOAD_FAST                'self'
              234  STORE_ATTR               success
              236  <48>             
            238_0  COME_FROM           222  '222'

Parse error at or near `<121>' instruction at offset 30


def _id(obj):
    return obj


_module_cleanups = []

def addModuleCleanup(function, *args, **kwargs):
    """Same as addCleanup, except the cleanup items are called even if
    setUpModule fails (unlike tearDownModule)."""
    _module_cleanups.append(function, args, kwargs)


def doModuleCleanups--- This code section failed: ---

 L.  98         0  BUILD_LIST_0          0 
                2  STORE_FAST               'exceptions'
              4_0  COME_FROM            88  '88'
              4_1  COME_FROM            76  '76'
              4_2  COME_FROM            40  '40'

 L.  99         4  LOAD_GLOBAL              _module_cleanups
                6  POP_JUMP_IF_FALSE    90  'to 90'

 L. 100         8  LOAD_GLOBAL              _module_cleanups
               10  LOAD_METHOD              pop
               12  CALL_METHOD_0         0  ''
               14  UNPACK_SEQUENCE_3     3 
               16  STORE_FAST               'function'
               18  STORE_FAST               'args'
               20  STORE_FAST               'kwargs'

 L. 101        22  SETUP_FINALLY        42  'to 42'

 L. 102        24  LOAD_FAST                'function'
               26  LOAD_FAST                'args'
               28  BUILD_MAP_0           0 
               30  LOAD_FAST                'kwargs'
               32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          
               38  POP_BLOCK        
               40  JUMP_BACK             4  'to 4'
             42_0  COME_FROM_FINALLY    22  '22'

 L. 103        42  DUP_TOP          
               44  LOAD_GLOBAL              Exception
               46  <121>                86  ''
               48  POP_TOP          
               50  STORE_FAST               'exc'
               52  POP_TOP          
               54  SETUP_FINALLY        78  'to 78'

 L. 104        56  LOAD_FAST                'exceptions'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'exc'
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  POP_BLOCK        
               68  POP_EXCEPT       
               70  LOAD_CONST               None
               72  STORE_FAST               'exc'
               74  DELETE_FAST              'exc'
               76  JUMP_BACK             4  'to 4'
             78_0  COME_FROM_FINALLY    54  '54'
               78  LOAD_CONST               None
               80  STORE_FAST               'exc'
               82  DELETE_FAST              'exc'
               84  <48>             
               86  <48>             
               88  JUMP_BACK             4  'to 4'
             90_0  COME_FROM             6  '6'

 L. 105        90  LOAD_FAST                'exceptions'
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 108        94  LOAD_FAST                'exceptions'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

Parse error at or near `<164>' instruction at offset 32


def skip(reason):
    """
    Unconditionally skip a test.
    """

    def decorator(test_item):
        if not isinstance(test_item, type):

            @functools.wrapstest_item
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)

            test_item = skip_wrapper
        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item

    if isinstance(reason, types.FunctionType):
        test_item = reason
        reason = ''
        return decorator(test_item)
    return decorator


def skipIf(condition, reason):
    """
    Skip a test if the condition is true.
    """
    if condition:
        return skip(reason)
    return _id


def skipUnless(condition, reason):
    """
    Skip a test unless the condition is true.
    """
    if not condition:
        return skip(reason)
    return _id


def expectedFailure(test_item):
    test_item.__unittest_expecting_failure__ = True
    return test_item


def _is_subtype(expected, basetype):
    if isinstance(expected, tuple):
        return all((_is_subtype(e, basetype) for e in expected))
    return isinstance(expected, type) and issubclass(expected, basetype)


class _BaseTestCaseContext:

    def __init__(self, test_case):
        self.test_case = test_case

    def _raiseFailure(self, standardMsg):
        msg = self.test_case._formatMessage(self.msg, standardMsg)
        raise self.test_case.failureExceptionmsg


class _AssertRaisesBaseContext(_BaseTestCaseContext):

    def __init__--- This code section failed: ---

 L. 168         0  LOAD_GLOBAL              _BaseTestCaseContext
                2  LOAD_METHOD              __init__
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'test_case'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 169        12  LOAD_FAST                'expected'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               expected

 L. 170        18  LOAD_FAST                'test_case'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               test_case

 L. 171        24  LOAD_FAST                'expected_regex'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L. 172        32  LOAD_GLOBAL              re
               34  LOAD_METHOD              compile
               36  LOAD_FAST                'expected_regex'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'expected_regex'
             42_0  COME_FROM            30  '30'

 L. 173        42  LOAD_FAST                'expected_regex'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               expected_regex

 L. 174        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               obj_name

 L. 175        54  LOAD_CONST               None
               56  LOAD_FAST                'self'
               58  STORE_ATTR               msg

Parse error at or near `<117>' instruction at offset 28

    def handle--- This code section failed: ---

 L. 184         0  SETUP_FINALLY       196  'to 196'

 L. 185         2  LOAD_GLOBAL              _is_subtype
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                expected
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _base_type
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     34  'to 34'

 L. 186        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 '%s() arg 1 must be %s'

 L. 187        20  LOAD_FAST                'name'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _base_type_str
               26  BUILD_TUPLE_2         2 

 L. 186        28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'

 L. 188        34  LOAD_FAST                'args'
               36  POP_JUMP_IF_TRUE     88  'to 88'

 L. 189        38  LOAD_FAST                'kwargs'
               40  LOAD_METHOD              pop
               42  LOAD_STR                 'msg'
               44  LOAD_CONST               None
               46  CALL_METHOD_2         2  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               msg

 L. 190        52  LOAD_FAST                'kwargs'
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L. 191        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 '%r is an invalid keyword argument for this function'

 L. 192        60  LOAD_GLOBAL              next
               62  LOAD_GLOBAL              iter
               64  LOAD_FAST                'kwargs'
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_1         1 

 L. 191        72  BINARY_MODULO    
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            54  '54'

 L. 193        78  LOAD_FAST                'self'
               80  POP_BLOCK        

 L. 204        82  LOAD_CONST               None
               84  STORE_FAST               'self'

 L. 193        86  RETURN_VALUE     
             88_0  COME_FROM            36  '36'

 L. 195        88  LOAD_FAST                'args'
               90  UNPACK_EX_1+0           
               92  STORE_FAST               'callable_obj'
               94  STORE_FAST               'args'

 L. 196        96  SETUP_FINALLY       110  'to 110'

 L. 197        98  LOAD_FAST                'callable_obj'
              100  LOAD_ATTR                __name__
              102  LOAD_FAST                'self'
              104  STORE_ATTR               obj_name
              106  POP_BLOCK        
              108  JUMP_FORWARD        138  'to 138'
            110_0  COME_FROM_FINALLY    96  '96'

 L. 198       110  DUP_TOP          
              112  LOAD_GLOBAL              AttributeError
              114  <121>               136  ''
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 199       122  LOAD_GLOBAL              str
              124  LOAD_FAST                'callable_obj'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               obj_name
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
              136  <48>             
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           108  '108'

 L. 200       138  LOAD_FAST                'self'
              140  SETUP_WITH          172  'to 172'
              142  POP_TOP          

 L. 201       144  LOAD_FAST                'callable_obj'
              146  LOAD_FAST                'args'
              148  BUILD_MAP_0           0 
              150  LOAD_FAST                'kwargs'
              152  <164>                 1  ''
              154  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              156  POP_TOP          
              158  POP_BLOCK        
              160  LOAD_CONST               None
              162  DUP_TOP          
              164  DUP_TOP          
              166  CALL_FUNCTION_3       3  ''
              168  POP_TOP          
              170  JUMP_FORWARD        188  'to 188'
            172_0  COME_FROM_WITH      140  '140'
              172  <49>             
              174  POP_JUMP_IF_TRUE    178  'to 178'
              176  <48>             
            178_0  COME_FROM           174  '174'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          
              184  POP_EXCEPT       
              186  POP_TOP          
            188_0  COME_FROM           170  '170'
              188  POP_BLOCK        

 L. 204       190  LOAD_CONST               None
              192  STORE_FAST               'self'
              194  JUMP_FORWARD        202  'to 202'
            196_0  COME_FROM_FINALLY     0  '0'
              196  LOAD_CONST               None
              198  STORE_FAST               'self'
              200  <48>             
            202_0  COME_FROM           194  '194'

Parse error at or near `LOAD_CONST' instruction at offset 82


class _AssertRaisesContext(_AssertRaisesBaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertRaises* methods.'
    _base_type = BaseException
    _base_type_str = 'an exception type or tuple of exception types'

    def __enter__(self):
        return self

    def __exit__--- This code section failed: ---

 L. 217         0  LOAD_FAST                'exc_type'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    96  'to 96'

 L. 218         8  SETUP_FINALLY        22  'to 22'

 L. 219        10  LOAD_FAST                'self'
               12  LOAD_ATTR                expected
               14  LOAD_ATTR                __name__
               16  STORE_FAST               'exc_name'
               18  POP_BLOCK        
               20  JUMP_FORWARD         50  'to 50'
             22_0  COME_FROM_FINALLY     8  '8'

 L. 220        22  DUP_TOP          
               24  LOAD_GLOBAL              AttributeError
               26  <121>                48  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 221        34  LOAD_GLOBAL              str
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                expected
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'exc_name'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            20  '20'

 L. 222        50  LOAD_FAST                'self'
               52  LOAD_ATTR                obj_name
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L. 223        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _raiseFailure
               60  LOAD_STR                 '{} not raised by {}'
               62  LOAD_METHOD              format
               64  LOAD_FAST                'exc_name'

 L. 224        66  LOAD_FAST                'self'
               68  LOAD_ATTR                obj_name

 L. 223        70  CALL_METHOD_2         2  ''
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  JUMP_FORWARD        106  'to 106'
             78_0  COME_FROM            54  '54'

 L. 226        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _raiseFailure
               82  LOAD_STR                 '{} not raised'
               84  LOAD_METHOD              format
               86  LOAD_FAST                'exc_name'
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM             6  '6'

 L. 228        96  LOAD_GLOBAL              traceback
               98  LOAD_METHOD              clear_frames
              100  LOAD_FAST                'tb'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            76  '76'

 L. 229       106  LOAD_GLOBAL              issubclass
              108  LOAD_FAST                'exc_type'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                expected
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_TRUE    122  'to 122'

 L. 231       118  LOAD_CONST               False
              120  RETURN_VALUE     
            122_0  COME_FROM           116  '116'

 L. 233       122  LOAD_FAST                'exc_value'
              124  LOAD_METHOD              with_traceback
              126  LOAD_CONST               None
              128  CALL_METHOD_1         1  ''
              130  LOAD_FAST                'self'
              132  STORE_ATTR               exception

 L. 234       134  LOAD_FAST                'self'
              136  LOAD_ATTR                expected_regex
              138  LOAD_CONST               None
              140  <117>                 0  ''
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L. 235       144  LOAD_CONST               True
              146  RETURN_VALUE     
            148_0  COME_FROM           142  '142'

 L. 237       148  LOAD_FAST                'self'
              150  LOAD_ATTR                expected_regex
              152  STORE_FAST               'expected_regex'

 L. 238       154  LOAD_FAST                'expected_regex'
              156  LOAD_METHOD              search
              158  LOAD_GLOBAL              str
              160  LOAD_FAST                'exc_value'
              162  CALL_FUNCTION_1       1  ''
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_TRUE    192  'to 192'

 L. 239       168  LOAD_FAST                'self'
              170  LOAD_METHOD              _raiseFailure
              172  LOAD_STR                 '"{}" does not match "{}"'
              174  LOAD_METHOD              format

 L. 240       176  LOAD_FAST                'expected_regex'
              178  LOAD_ATTR                pattern
              180  LOAD_GLOBAL              str
              182  LOAD_FAST                'exc_value'
              184  CALL_FUNCTION_1       1  ''

 L. 239       186  CALL_METHOD_2         2  ''
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          
            192_0  COME_FROM           166  '166'

 L. 241       192  LOAD_CONST               True
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    __class_getitem__ = classmethod(types.GenericAlias)


class _AssertWarnsContext(_AssertRaisesBaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertWarns* methods.'
    _base_type = Warning
    _base_type_str = 'a warning type or tuple of warning types'

    def __enter__(self):
        for v in sys.modules.values:
            if getattr(v, '__warningregistry__', None):
                v.__warningregistry__ = {}
        else:
            self.warnings_manager = warnings.catch_warnings(record=True)
            self.warnings = self.warnings_manager.__enter__
            warnings.simplefilter('always', self.expected)
            return self

    def __exit__--- This code section failed: ---

 L. 264         0  LOAD_FAST                'self'
                2  LOAD_ATTR                warnings_manager
                4  LOAD_METHOD              __exit__
                6  LOAD_FAST                'exc_type'
                8  LOAD_FAST                'exc_value'
               10  LOAD_FAST                'tb'
               12  CALL_METHOD_3         3  ''
               14  POP_TOP          

 L. 265        16  LOAD_FAST                'exc_type'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 267        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 268        28  SETUP_FINALLY        42  'to 42'

 L. 269        30  LOAD_FAST                'self'
               32  LOAD_ATTR                expected
               34  LOAD_ATTR                __name__
               36  STORE_FAST               'exc_name'
               38  POP_BLOCK        
               40  JUMP_FORWARD         70  'to 70'
             42_0  COME_FROM_FINALLY    28  '28'

 L. 270        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  <121>                68  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 271        54  LOAD_GLOBAL              str
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                expected
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'exc_name'
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
               68  <48>             
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            40  '40'

 L. 272        70  LOAD_CONST               None
               72  STORE_FAST               'first_matching'

 L. 273        74  LOAD_FAST                'self'
               76  LOAD_ATTR                warnings
               78  GET_ITER         
             80_0  COME_FROM           142  '142'
             80_1  COME_FROM           102  '102'
               80  FOR_ITER            172  'to 172'
               82  STORE_FAST               'm'

 L. 274        84  LOAD_FAST                'm'
               86  LOAD_ATTR                message
               88  STORE_FAST               'w'

 L. 275        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'w'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                expected
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_TRUE    104  'to 104'

 L. 276       102  JUMP_BACK            80  'to 80'
            104_0  COME_FROM           100  '100'

 L. 277       104  LOAD_FAST                'first_matching'
              106  LOAD_CONST               None
              108  <117>                 0  ''
              110  POP_JUMP_IF_FALSE   116  'to 116'

 L. 278       112  LOAD_FAST                'w'
              114  STORE_FAST               'first_matching'
            116_0  COME_FROM           110  '110'

 L. 279       116  LOAD_FAST                'self'
              118  LOAD_ATTR                expected_regex
              120  LOAD_CONST               None
              122  <117>                 1  ''
              124  POP_JUMP_IF_FALSE   144  'to 144'

 L. 280       126  LOAD_FAST                'self'
              128  LOAD_ATTR                expected_regex
              130  LOAD_METHOD              search
              132  LOAD_GLOBAL              str
              134  LOAD_FAST                'w'
              136  CALL_FUNCTION_1       1  ''
              138  CALL_METHOD_1         1  ''

 L. 279       140  POP_JUMP_IF_TRUE    144  'to 144'

 L. 281       142  JUMP_BACK            80  'to 80'
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           124  '124'

 L. 283       144  LOAD_FAST                'w'
              146  LOAD_FAST                'self'
              148  STORE_ATTR               warning

 L. 284       150  LOAD_FAST                'm'
              152  LOAD_ATTR                filename
              154  LOAD_FAST                'self'
              156  STORE_ATTR               filename

 L. 285       158  LOAD_FAST                'm'
              160  LOAD_ATTR                lineno
              162  LOAD_FAST                'self'
              164  STORE_ATTR               lineno

 L. 286       166  POP_TOP          
              168  LOAD_CONST               None
              170  RETURN_VALUE     
            172_0  COME_FROM            80  '80'

 L. 288       172  LOAD_FAST                'first_matching'
              174  LOAD_CONST               None
              176  <117>                 1  ''
              178  POP_JUMP_IF_FALSE   206  'to 206'

 L. 289       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _raiseFailure
              184  LOAD_STR                 '"{}" does not match "{}"'
              186  LOAD_METHOD              format

 L. 290       188  LOAD_FAST                'self'
              190  LOAD_ATTR                expected_regex
              192  LOAD_ATTR                pattern
              194  LOAD_GLOBAL              str
              196  LOAD_FAST                'first_matching'
              198  CALL_FUNCTION_1       1  ''

 L. 289       200  CALL_METHOD_2         2  ''
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
            206_0  COME_FROM           178  '178'

 L. 291       206  LOAD_FAST                'self'
              208  LOAD_ATTR                obj_name
              210  POP_JUMP_IF_FALSE   234  'to 234'

 L. 292       212  LOAD_FAST                'self'
              214  LOAD_METHOD              _raiseFailure
              216  LOAD_STR                 '{} not triggered by {}'
              218  LOAD_METHOD              format
              220  LOAD_FAST                'exc_name'

 L. 293       222  LOAD_FAST                'self'
              224  LOAD_ATTR                obj_name

 L. 292       226  CALL_METHOD_2         2  ''
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  JUMP_FORWARD        250  'to 250'
            234_0  COME_FROM           210  '210'

 L. 295       234  LOAD_FAST                'self'
              236  LOAD_METHOD              _raiseFailure
              238  LOAD_STR                 '{} not triggered'
              240  LOAD_METHOD              format
              242  LOAD_FAST                'exc_name'
              244  CALL_METHOD_1         1  ''
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
            250_0  COME_FROM           232  '232'

Parse error at or near `<117>' instruction at offset 20


class _OrderedChainMap(collections.ChainMap):

    def __iter__--- This code section failed: ---

 L. 301         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'seen'

 L. 302         6  LOAD_FAST                'self'
                8  LOAD_ATTR                maps
               10  GET_ITER         
             12_0  COME_FROM            50  '50'
               12  FOR_ITER             52  'to 52'
               14  STORE_FAST               'mapping'

 L. 303        16  LOAD_FAST                'mapping'
               18  GET_ITER         
             20_0  COME_FROM            48  '48'
             20_1  COME_FROM            30  '30'
               20  FOR_ITER             50  'to 50'
               22  STORE_FAST               'k'

 L. 304        24  LOAD_FAST                'k'
               26  LOAD_FAST                'seen'
               28  <118>                 1  ''
               30  POP_JUMP_IF_FALSE_BACK    20  'to 20'

 L. 305        32  LOAD_FAST                'seen'
               34  LOAD_METHOD              add
               36  LOAD_FAST                'k'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 306        42  LOAD_FAST                'k'
               44  YIELD_VALUE      
               46  POP_TOP          
               48  JUMP_BACK            20  'to 20'
             50_0  COME_FROM            20  '20'
               50  JUMP_BACK            12  'to 12'
             52_0  COME_FROM            12  '12'

Parse error at or near `<118>' instruction at offset 28


class TestCase(object):
    __doc__ = "A class whose instances are single test cases.\n\n    By default, the test code itself should be placed in a method named\n    'runTest'.\n\n    If the fixture may be used for many test cases, create as\n    many test methods as are needed. When instantiating such a TestCase\n    subclass, specify in the constructor arguments the name of the test method\n    that the instance is to execute.\n\n    Test authors should subclass TestCase for their own tests. Construction\n    and deconstruction of the test's environment ('fixture') can be\n    implemented by overriding the 'setUp' and 'tearDown' methods respectively.\n\n    If it is necessary to override the __init__ method, the base class\n    __init__ method must always be called. It is important that subclasses\n    should not change the signature of their __init__ method, since instances\n    of the classes are instantiated automatically by parts of the framework\n    in order to be run.\n\n    When subclassing TestCase, you can set these attributes:\n    * failureException: determines which exception will be raised when\n        the instance's assertion methods fail; test methods raising this\n        exception will be deemed to have 'failed' rather than 'errored'.\n    * longMessage: determines whether long messages (including repr of\n        objects used in assert methods) will be printed on failure in *addition*\n        to any explicit message passed.\n    * maxDiff: sets the maximum length of a diff in failure messages\n        by assert methods using difflib. It is looked up as an instance\n        attribute so can be configured by individual tests if required.\n    "
    failureException = AssertionError
    longMessage = True
    maxDiff = 640
    _diffThreshold = 65536
    _classSetupFailed = False
    _class_cleanups = []

    def __init__--- This code section failed: ---

 L. 363         0  LOAD_FAST                'methodName'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _testMethodName

 L. 364         6  LOAD_CONST               None
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _outcome

 L. 365        12  LOAD_STR                 'No test'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _testMethodDoc

 L. 366        18  SETUP_FINALLY        34  'to 34'

 L. 367        20  LOAD_GLOBAL              getattr
               22  LOAD_FAST                'self'
               24  LOAD_FAST                'methodName'
               26  CALL_FUNCTION_2       2  ''
               28  STORE_FAST               'testMethod'
               30  POP_BLOCK        
               32  JUMP_FORWARD         78  'to 78'
             34_0  COME_FROM_FINALLY    18  '18'

 L. 368        34  DUP_TOP          
               36  LOAD_GLOBAL              AttributeError
               38  <121>                76  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 369        46  LOAD_FAST                'methodName'
               48  LOAD_STR                 'runTest'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE    72  'to 72'

 L. 372        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'no such test method in %s: %s'

 L. 373        58  LOAD_FAST                'self'
               60  LOAD_ATTR                __class__
               62  LOAD_FAST                'methodName'
               64  BUILD_TUPLE_2         2 

 L. 372        66  BINARY_MODULO    
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            52  '52'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         86  'to 86'
               76  <48>             
             78_0  COME_FROM            32  '32'

 L. 375        78  LOAD_FAST                'testMethod'
               80  LOAD_ATTR                __doc__
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _testMethodDoc
             86_0  COME_FROM            74  '74'

 L. 376        86  BUILD_LIST_0          0 
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _cleanups

 L. 377        92  LOAD_CONST               None
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _subtest

 L. 382        98  BUILD_MAP_0           0 
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _type_equality_funcs

 L. 383       104  LOAD_FAST                'self'
              106  LOAD_METHOD              addTypeEqualityFunc
              108  LOAD_GLOBAL              dict
              110  LOAD_STR                 'assertDictEqual'
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L. 384       116  LOAD_FAST                'self'
              118  LOAD_METHOD              addTypeEqualityFunc
              120  LOAD_GLOBAL              list
              122  LOAD_STR                 'assertListEqual'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L. 385       128  LOAD_FAST                'self'
              130  LOAD_METHOD              addTypeEqualityFunc
              132  LOAD_GLOBAL              tuple
              134  LOAD_STR                 'assertTupleEqual'
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          

 L. 386       140  LOAD_FAST                'self'
              142  LOAD_METHOD              addTypeEqualityFunc
              144  LOAD_GLOBAL              set
              146  LOAD_STR                 'assertSetEqual'
              148  CALL_METHOD_2         2  ''
              150  POP_TOP          

 L. 387       152  LOAD_FAST                'self'
              154  LOAD_METHOD              addTypeEqualityFunc
              156  LOAD_GLOBAL              frozenset
              158  LOAD_STR                 'assertSetEqual'
              160  CALL_METHOD_2         2  ''
              162  POP_TOP          

 L. 388       164  LOAD_FAST                'self'
              166  LOAD_METHOD              addTypeEqualityFunc
              168  LOAD_GLOBAL              str
              170  LOAD_STR                 'assertMultiLineEqual'
              172  CALL_METHOD_2         2  ''
              174  POP_TOP          

Parse error at or near `<121>' instruction at offset 38

    def addTypeEqualityFunc(self, typeobj, function):
        """Add a type specific assertEqual style function to compare a type.

        This method is for use by TestCase subclasses that need to register
        their own type equality functions to provide nicer error messages.

        Args:
            typeobj: The data type to call this function on when both values
                    are of the same type in assertEqual().
            function: The callable taking two arguments and an optional
                    msg= argument that raises self.failureException with a
                    useful error message when the two arguments are not equal.
        """
        self._type_equality_funcs[typeobj] = function

    def addCleanup(self, function, *args, **kwargs):
        """Add a function, with arguments, to be called when the test is
        completed. Functions added are called on a LIFO basis and are
        called after tearDown on test failure or success.

        Cleanup items are called even if setUp fails (unlike tearDown)."""
        self._cleanups.append(function, args, kwargs)

    @classmethod
    def addClassCleanup(cls, function, *args, **kwargs):
        """Same as addCleanup, except the cleanup items are called even if
        setUpClass fails (unlike tearDownClass)."""
        cls._class_cleanups.append(function, args, kwargs)

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        pass

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it."""
        pass

    @classmethod
    def setUpClass(cls):
        """Hook method for setting up class fixture before running tests in the class."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Hook method for deconstructing the class fixture after running all tests in the class."""
        pass

    def countTestCases(self):
        return 1

    def defaultTestResult(self):
        return result.TestResult

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        doc = self._testMethodDoc
        if doc:
            return doc.strip.split'\n'[0].strip

    def id(self):
        return '%s.%s' % (strclass(self.__class__), self._testMethodName)

    def __eq__--- This code section failed: ---

 L. 456         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'other'
               10  CALL_FUNCTION_1       1  ''
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 457        16  LOAD_GLOBAL              NotImplemented
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 459        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _testMethodName
               24  LOAD_FAST                'other'
               26  LOAD_ATTR                _testMethodName
               28  COMPARE_OP               ==
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __hash__(self):
        return hash((type(self), self._testMethodName))

    def __str__(self):
        return '%s (%s)' % (self._testMethodName, strclass(self.__class__))

    def __repr__(self):
        return '<%s testMethod=%s>' % (
         strclass(self.__class__), self._testMethodName)

    def _addSkip--- This code section failed: ---

 L. 472         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'result'
                4  LOAD_STR                 'addSkip'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'addSkip'

 L. 473        12  LOAD_FAST                'addSkip'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 474        20  LOAD_FAST                'addSkip'
               22  LOAD_FAST                'test_case'
               24  LOAD_FAST                'reason'
               26  CALL_FUNCTION_2       2  ''
               28  POP_TOP          
               30  JUMP_FORWARD         56  'to 56'
             32_0  COME_FROM            18  '18'

 L. 476        32  LOAD_GLOBAL              warnings
               34  LOAD_METHOD              warn
               36  LOAD_STR                 'TestResult has no addSkip method, skips not reported'

 L. 477        38  LOAD_GLOBAL              RuntimeWarning
               40  LOAD_CONST               2

 L. 476        42  CALL_METHOD_3         3  ''
               44  POP_TOP          

 L. 478        46  LOAD_FAST                'result'
               48  LOAD_METHOD              addSuccess
               50  LOAD_FAST                'test_case'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
             56_0  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 16

    @contextlib.contextmanager
    def subTest--- This code section failed: ---

 L. 488         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _outcome
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _outcome
               14  LOAD_ATTR                result_supports_subtests
               16  POP_JUMP_IF_TRUE     28  'to 28'
             18_0  COME_FROM             8  '8'

 L. 489        18  LOAD_CONST               None
               20  YIELD_VALUE      
               22  POP_TOP          

 L. 490        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            16  '16'

 L. 491        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _subtest
               32  STORE_FAST               'parent'

 L. 492        34  LOAD_FAST                'parent'
               36  LOAD_CONST               None
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 493        42  LOAD_GLOBAL              _OrderedChainMap
               44  LOAD_FAST                'params'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'params_map'
               50  JUMP_FORWARD         64  'to 64'
             52_0  COME_FROM            40  '40'

 L. 495        52  LOAD_FAST                'parent'
               54  LOAD_ATTR                params
               56  LOAD_METHOD              new_child
               58  LOAD_FAST                'params'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'params_map'
             64_0  COME_FROM            50  '50'

 L. 496        64  LOAD_GLOBAL              _SubTest
               66  LOAD_FAST                'self'
               68  LOAD_FAST                'msg'
               70  LOAD_FAST                'params_map'
               72  CALL_FUNCTION_3       3  ''
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _subtest

 L. 497        78  SETUP_FINALLY       194  'to 194'

 L. 498        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _outcome
               84  LOAD_ATTR                testPartExecutor
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _subtest
               90  LOAD_CONST               True
               92  LOAD_CONST               ('isTest',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  SETUP_WITH          120  'to 120'
               98  POP_TOP          

 L. 499       100  LOAD_CONST               None
              102  YIELD_VALUE      
              104  POP_TOP          
              106  POP_BLOCK        
              108  LOAD_CONST               None
              110  DUP_TOP          
              112  DUP_TOP          
              114  CALL_FUNCTION_3       3  ''
              116  POP_TOP          
              118  JUMP_FORWARD        136  'to 136'
            120_0  COME_FROM_WITH       96  '96'
              120  <49>             
              122  POP_JUMP_IF_TRUE    126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          
              132  POP_EXCEPT       
              134  POP_TOP          
            136_0  COME_FROM           118  '118'

 L. 500       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _outcome
              140  LOAD_ATTR                success
              142  POP_JUMP_IF_TRUE    172  'to 172'

 L. 501       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _outcome
              148  LOAD_ATTR                result
              150  STORE_FAST               'result'

 L. 502       152  LOAD_FAST                'result'
              154  LOAD_CONST               None
              156  <117>                 1  ''
              158  POP_JUMP_IF_FALSE   184  'to 184'
              160  LOAD_FAST                'result'
              162  LOAD_ATTR                failfast
              164  POP_JUMP_IF_FALSE   184  'to 184'

 L. 503       166  LOAD_GLOBAL              _ShouldStop
              168  RAISE_VARARGS_1       1  'exception instance'
              170  JUMP_FORWARD        184  'to 184'
            172_0  COME_FROM           142  '142'

 L. 504       172  LOAD_FAST                'self'
              174  LOAD_ATTR                _outcome
              176  LOAD_ATTR                expectedFailure
              178  POP_JUMP_IF_FALSE   184  'to 184'

 L. 507       180  LOAD_GLOBAL              _ShouldStop
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'
            184_1  COME_FROM           170  '170'
            184_2  COME_FROM           164  '164'
            184_3  COME_FROM           158  '158'
              184  POP_BLOCK        

 L. 509       186  LOAD_FAST                'parent'
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _subtest
              192  JUMP_FORWARD        202  'to 202'
            194_0  COME_FROM_FINALLY    78  '78'
              194  LOAD_FAST                'parent'
              196  LOAD_FAST                'self'
              198  STORE_ATTR               _subtest
              200  <48>             
            202_0  COME_FROM           192  '192'

Parse error at or near `None' instruction at offset -1

    def _feedErrorsToResult--- This code section failed: ---

 L. 512         0  LOAD_FAST                'errors'
                2  GET_ITER         
              4_0  COME_FROM            90  '90'
              4_1  COME_FROM            76  '76'
              4_2  COME_FROM            46  '46'
              4_3  COME_FROM            38  '38'
                4  FOR_ITER             92  'to 92'
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'test'
               10  STORE_FAST               'exc_info'

 L. 513        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'test'
               16  LOAD_GLOBAL              _SubTest
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 514        22  LOAD_FAST                'result'
               24  LOAD_METHOD              addSubTest
               26  LOAD_FAST                'test'
               28  LOAD_ATTR                test_case
               30  LOAD_FAST                'test'
               32  LOAD_FAST                'exc_info'
               34  CALL_METHOD_3         3  ''
               36  POP_TOP          
               38  JUMP_BACK             4  'to 4'
             40_0  COME_FROM            20  '20'

 L. 515        40  LOAD_FAST                'exc_info'
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L. 516        48  LOAD_GLOBAL              issubclass
               50  LOAD_FAST                'exc_info'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                failureException
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 517        64  LOAD_FAST                'result'
               66  LOAD_METHOD              addFailure
               68  LOAD_FAST                'test'
               70  LOAD_FAST                'exc_info'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  JUMP_BACK             4  'to 4'
             78_0  COME_FROM            62  '62'

 L. 519        78  LOAD_FAST                'result'
               80  LOAD_METHOD              addError
               82  LOAD_FAST                'test'
               84  LOAD_FAST                'exc_info'
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          
               90  JUMP_BACK             4  'to 4'
             92_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 44

    def _addExpectedFailure--- This code section failed: ---

 L. 522         0  SETUP_FINALLY        12  'to 12'

 L. 523         2  LOAD_FAST                'result'
                4  LOAD_ATTR                addExpectedFailure
                6  STORE_FAST               'addExpectedFailure'
                8  POP_BLOCK        
               10  JUMP_FORWARD         52  'to 52'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 524        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                50  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 525        24  LOAD_GLOBAL              warnings
               26  LOAD_METHOD              warn
               28  LOAD_STR                 'TestResult has no addExpectedFailure method, reporting as passes'

 L. 526        30  LOAD_GLOBAL              RuntimeWarning

 L. 525        32  CALL_METHOD_2         2  ''
               34  POP_TOP          

 L. 527        36  LOAD_FAST                'result'
               38  LOAD_METHOD              addSuccess
               40  LOAD_FAST                'self'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
               46  POP_EXCEPT       
               48  JUMP_FORWARD         62  'to 62'
               50  <48>             
             52_0  COME_FROM            10  '10'

 L. 529        52  LOAD_FAST                'addExpectedFailure'
               54  LOAD_FAST                'self'
               56  LOAD_FAST                'exc_info'
               58  CALL_FUNCTION_2       2  ''
               60  POP_TOP          
             62_0  COME_FROM            48  '48'

Parse error at or near `<121>' instruction at offset 16

    def _addUnexpectedSuccess--- This code section failed: ---

 L. 532         0  SETUP_FINALLY        12  'to 12'

 L. 533         2  LOAD_FAST                'result'
                4  LOAD_ATTR                addUnexpectedSuccess
                6  STORE_FAST               'addUnexpectedSuccess'
                8  POP_BLOCK        
               10  JUMP_FORWARD         88  'to 88'
             12_0  COME_FROM_FINALLY     0  '0'

 L. 534        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  <121>                86  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 535        24  LOAD_GLOBAL              warnings
               26  LOAD_METHOD              warn
               28  LOAD_STR                 'TestResult has no addUnexpectedSuccess method, reporting as failure'

 L. 536        30  LOAD_GLOBAL              RuntimeWarning

 L. 535        32  CALL_METHOD_2         2  ''
               34  POP_TOP          

 L. 539        36  SETUP_FINALLY        48  'to 48'

 L. 540        38  LOAD_GLOBAL              _UnexpectedSuccess
               40  LOAD_CONST               None
               42  RAISE_VARARGS_2       2  'exception instance with __cause__'
               44  POP_BLOCK        
               46  JUMP_FORWARD         82  'to 82'
             48_0  COME_FROM_FINALLY    36  '36'

 L. 541        48  DUP_TOP          
               50  LOAD_GLOBAL              _UnexpectedSuccess
               52  <121>                80  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 542        60  LOAD_FAST                'result'
               62  LOAD_METHOD              addFailure
               64  LOAD_FAST                'self'
               66  LOAD_GLOBAL              sys
               68  LOAD_METHOD              exc_info
               70  CALL_METHOD_0         0  ''
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
               80  <48>             
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            46  '46'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         96  'to 96'
               86  <48>             
             88_0  COME_FROM            10  '10'

 L. 544        88  LOAD_FAST                'addUnexpectedSuccess'
               90  LOAD_FAST                'self'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          
             96_0  COME_FROM            84  '84'

Parse error at or near `<121>' instruction at offset 16

    def _callSetUp(self):
        self.setUp

    def _callTestMethod(self, method):
        method()

    def _callTearDown(self):
        self.tearDown

    def _callCleanup--- This code section failed: ---

 L. 556         0  LOAD_FAST                'function'
                2  LOAD_FAST                'args'
                4  BUILD_MAP_0           0 
                6  LOAD_FAST                'kwargs'
                8  <164>                 1  ''
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def run--- This code section failed: ---

 L. 559         0  LOAD_FAST                'result'
                2  STORE_FAST               'orig_result'

 L. 560         4  LOAD_FAST                'result'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    46  'to 46'

 L. 561        12  LOAD_FAST                'self'
               14  LOAD_METHOD              defaultTestResult
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'result'

 L. 562        20  LOAD_GLOBAL              getattr
               22  LOAD_FAST                'result'
               24  LOAD_STR                 'startTestRun'
               26  LOAD_CONST               None
               28  CALL_FUNCTION_3       3  ''
               30  STORE_FAST               'startTestRun'

 L. 563        32  LOAD_FAST                'startTestRun'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 564        40  LOAD_FAST                'startTestRun'
               42  CALL_FUNCTION_0       0  ''
               44  POP_TOP          
             46_0  COME_FROM            38  '38'
             46_1  COME_FROM            10  '10'

 L. 566        46  LOAD_FAST                'result'
               48  LOAD_METHOD              startTest
               50  LOAD_FAST                'self'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 568        56  LOAD_GLOBAL              getattr
               58  LOAD_FAST                'self'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _testMethodName
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'testMethod'

 L. 569        68  LOAD_GLOBAL              getattr
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                __class__
               74  LOAD_STR                 '__unittest_skip__'
               76  LOAD_CONST               False
               78  CALL_FUNCTION_3       3  ''
               80  POP_JUMP_IF_TRUE     94  'to 94'

 L. 570        82  LOAD_GLOBAL              getattr
               84  LOAD_FAST                'testMethod'
               86  LOAD_STR                 '__unittest_skip__'
               88  LOAD_CONST               False
               90  CALL_FUNCTION_3       3  ''

 L. 569        92  POP_JUMP_IF_FALSE   166  'to 166'
             94_0  COME_FROM            80  '80'

 L. 572        94  SETUP_FINALLY       150  'to 150'

 L. 573        96  LOAD_GLOBAL              getattr
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                __class__
              102  LOAD_STR                 '__unittest_skip_why__'
              104  LOAD_STR                 ''
              106  CALL_FUNCTION_3       3  ''
              108  JUMP_IF_TRUE_OR_POP   120  'to 120'

 L. 574       110  LOAD_GLOBAL              getattr
              112  LOAD_FAST                'testMethod'
              114  LOAD_STR                 '__unittest_skip_why__'
              116  LOAD_STR                 ''
              118  CALL_FUNCTION_3       3  ''
            120_0  COME_FROM           108  '108'

 L. 573       120  STORE_FAST               'skip_why'

 L. 575       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _addSkip
              126  LOAD_FAST                'result'
              128  LOAD_FAST                'self'
              130  LOAD_FAST                'skip_why'
              132  CALL_METHOD_3         3  ''
              134  POP_TOP          
              136  POP_BLOCK        

 L. 577       138  LOAD_FAST                'result'
              140  LOAD_METHOD              stopTest
              142  LOAD_FAST                'self'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  JUMP_FORWARD        162  'to 162'
            150_0  COME_FROM_FINALLY    94  '94'
              150  LOAD_FAST                'result'
              152  LOAD_METHOD              stopTest
              154  LOAD_FAST                'self'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  <48>             
            162_0  COME_FROM           148  '148'

 L. 578       162  LOAD_CONST               None
              164  RETURN_VALUE     
            166_0  COME_FROM            92  '92'

 L. 579       166  LOAD_GLOBAL              getattr
              168  LOAD_FAST                'testMethod'

 L. 580       170  LOAD_STR                 '__unittest_expecting_failure__'
              172  LOAD_CONST               False

 L. 579       174  CALL_FUNCTION_3       3  ''
              176  STORE_FAST               'expecting_failure_method'

 L. 581       178  LOAD_GLOBAL              getattr
              180  LOAD_FAST                'self'

 L. 582       182  LOAD_STR                 '__unittest_expecting_failure__'
              184  LOAD_CONST               False

 L. 581       186  CALL_FUNCTION_3       3  ''
              188  STORE_FAST               'expecting_failure_class'

 L. 583       190  LOAD_FAST                'expecting_failure_class'
              192  JUMP_IF_TRUE_OR_POP   196  'to 196'
              194  LOAD_FAST                'expecting_failure_method'
            196_0  COME_FROM           192  '192'
              196  STORE_FAST               'expecting_failure'

 L. 584       198  LOAD_GLOBAL              _Outcome
              200  LOAD_FAST                'result'
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'outcome'

 L. 585   206_208  SETUP_FINALLY       612  'to 612'

 L. 586       210  LOAD_FAST                'outcome'
              212  LOAD_FAST                'self'
              214  STORE_ATTR               _outcome

 L. 588       216  LOAD_FAST                'outcome'
              218  LOAD_METHOD              testPartExecutor
              220  LOAD_FAST                'self'
              222  CALL_METHOD_1         1  ''
              224  SETUP_WITH          250  'to 250'
              226  POP_TOP          

 L. 589       228  LOAD_FAST                'self'
              230  LOAD_METHOD              _callSetUp
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          
              236  POP_BLOCK        
              238  LOAD_CONST               None
              240  DUP_TOP          
              242  DUP_TOP          
              244  CALL_FUNCTION_3       3  ''
              246  POP_TOP          
              248  JUMP_FORWARD        268  'to 268'
            250_0  COME_FROM_WITH      224  '224'
              250  <49>             
          252_254  POP_JUMP_IF_TRUE    258  'to 258'
              256  <48>             
            258_0  COME_FROM           252  '252'
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          
              264  POP_EXCEPT       
              266  POP_TOP          
            268_0  COME_FROM           248  '248'

 L. 590       268  LOAD_FAST                'outcome'
              270  LOAD_ATTR                success
          272_274  POP_JUMP_IF_FALSE   398  'to 398'

 L. 591       276  LOAD_FAST                'expecting_failure'
              278  LOAD_FAST                'outcome'
              280  STORE_ATTR               expecting_failure

 L. 592       282  LOAD_FAST                'outcome'
              284  LOAD_ATTR                testPartExecutor
              286  LOAD_FAST                'self'
              288  LOAD_CONST               True
              290  LOAD_CONST               ('isTest',)
              292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              294  SETUP_WITH          322  'to 322'
              296  POP_TOP          

 L. 593       298  LOAD_FAST                'self'
              300  LOAD_METHOD              _callTestMethod
              302  LOAD_FAST                'testMethod'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
              308  POP_BLOCK        
              310  LOAD_CONST               None
              312  DUP_TOP          
              314  DUP_TOP          
              316  CALL_FUNCTION_3       3  ''
              318  POP_TOP          
              320  JUMP_FORWARD        340  'to 340'
            322_0  COME_FROM_WITH      294  '294'
              322  <49>             
          324_326  POP_JUMP_IF_TRUE    330  'to 330'
              328  <48>             
            330_0  COME_FROM           324  '324'
              330  POP_TOP          
              332  POP_TOP          
              334  POP_TOP          
              336  POP_EXCEPT       
              338  POP_TOP          
            340_0  COME_FROM           320  '320'

 L. 594       340  LOAD_CONST               False
              342  LOAD_FAST                'outcome'
              344  STORE_ATTR               expecting_failure

 L. 595       346  LOAD_FAST                'outcome'
              348  LOAD_METHOD              testPartExecutor
              350  LOAD_FAST                'self'
              352  CALL_METHOD_1         1  ''
              354  SETUP_WITH          380  'to 380'
              356  POP_TOP          

 L. 596       358  LOAD_FAST                'self'
              360  LOAD_METHOD              _callTearDown
              362  CALL_METHOD_0         0  ''
              364  POP_TOP          
              366  POP_BLOCK        
              368  LOAD_CONST               None
              370  DUP_TOP          
              372  DUP_TOP          
              374  CALL_FUNCTION_3       3  ''
              376  POP_TOP          
              378  JUMP_FORWARD        398  'to 398'
            380_0  COME_FROM_WITH      354  '354'
              380  <49>             
          382_384  POP_JUMP_IF_TRUE    388  'to 388'
              386  <48>             
            388_0  COME_FROM           382  '382'
              388  POP_TOP          
              390  POP_TOP          
              392  POP_TOP          
              394  POP_EXCEPT       
              396  POP_TOP          
            398_0  COME_FROM           378  '378'
            398_1  COME_FROM           272  '272'

 L. 598       398  LOAD_FAST                'self'
              400  LOAD_METHOD              doCleanups
              402  CALL_METHOD_0         0  ''
              404  POP_TOP          

 L. 599       406  LOAD_FAST                'outcome'
              408  LOAD_ATTR                skipped
              410  GET_ITER         
            412_0  COME_FROM           434  '434'
              412  FOR_ITER            438  'to 438'
              414  UNPACK_SEQUENCE_2     2 
              416  STORE_FAST               'test'
              418  STORE_FAST               'reason'

 L. 600       420  LOAD_FAST                'self'
              422  LOAD_METHOD              _addSkip
              424  LOAD_FAST                'result'
              426  LOAD_FAST                'test'
              428  LOAD_FAST                'reason'
              430  CALL_METHOD_3         3  ''
              432  POP_TOP          
          434_436  JUMP_BACK           412  'to 412'
            438_0  COME_FROM           412  '412'

 L. 601       438  LOAD_FAST                'self'
              440  LOAD_METHOD              _feedErrorsToResult
              442  LOAD_FAST                'result'
              444  LOAD_FAST                'outcome'
              446  LOAD_ATTR                errors
              448  CALL_METHOD_2         2  ''
              450  POP_TOP          

 L. 602       452  LOAD_FAST                'outcome'
              454  LOAD_ATTR                success
          456_458  POP_JUMP_IF_FALSE   512  'to 512'

 L. 603       460  LOAD_FAST                'expecting_failure'
          462_464  POP_JUMP_IF_FALSE   502  'to 502'

 L. 604       466  LOAD_FAST                'outcome'
              468  LOAD_ATTR                expectedFailure
          470_472  POP_JUMP_IF_FALSE   490  'to 490'

 L. 605       474  LOAD_FAST                'self'
              476  LOAD_METHOD              _addExpectedFailure
              478  LOAD_FAST                'result'
              480  LOAD_FAST                'outcome'
              482  LOAD_ATTR                expectedFailure
              484  CALL_METHOD_2         2  ''
              486  POP_TOP          
              488  JUMP_FORWARD        500  'to 500'
            490_0  COME_FROM           470  '470'

 L. 607       490  LOAD_FAST                'self'
              492  LOAD_METHOD              _addUnexpectedSuccess
              494  LOAD_FAST                'result'
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          
            500_0  COME_FROM           488  '488'
              500  JUMP_FORWARD        512  'to 512'
            502_0  COME_FROM           462  '462'

 L. 609       502  LOAD_FAST                'result'
              504  LOAD_METHOD              addSuccess
              506  LOAD_FAST                'self'
              508  CALL_METHOD_1         1  ''
              510  POP_TOP          
            512_0  COME_FROM           500  '500'
            512_1  COME_FROM           456  '456'

 L. 610       512  LOAD_FAST                'result'
              514  POP_BLOCK        

 L. 612       516  LOAD_FAST                'result'
              518  LOAD_METHOD              stopTest
              520  LOAD_FAST                'self'
              522  CALL_METHOD_1         1  ''
              524  POP_TOP          

 L. 613       526  LOAD_FAST                'orig_result'
              528  LOAD_CONST               None
              530  <117>                 0  ''
          532_534  POP_JUMP_IF_FALSE   564  'to 564'

 L. 614       536  LOAD_GLOBAL              getattr
              538  LOAD_FAST                'result'
              540  LOAD_STR                 'stopTestRun'
              542  LOAD_CONST               None
              544  CALL_FUNCTION_3       3  ''
              546  STORE_FAST               'stopTestRun'

 L. 615       548  LOAD_FAST                'stopTestRun'
              550  LOAD_CONST               None
              552  <117>                 1  ''
          554_556  POP_JUMP_IF_FALSE   564  'to 564'

 L. 616       558  LOAD_FAST                'stopTestRun'
              560  CALL_FUNCTION_0       0  ''
              562  POP_TOP          
            564_0  COME_FROM           554  '554'
            564_1  COME_FROM           532  '532'

 L. 621       564  LOAD_FAST                'outcome'
              566  LOAD_ATTR                errors
              568  LOAD_METHOD              clear
              570  CALL_METHOD_0         0  ''
              572  POP_TOP          

 L. 622       574  LOAD_CONST               None
              576  LOAD_FAST                'outcome'
              578  STORE_ATTR               expectedFailure

 L. 625       580  LOAD_CONST               None
              582  LOAD_FAST                'self'
              584  STORE_ATTR               _outcome

 L. 610       586  RETURN_VALUE     

 L. 621       588  LOAD_FAST                'outcome'
              590  LOAD_ATTR                errors
              592  LOAD_METHOD              clear
              594  CALL_METHOD_0         0  ''
              596  POP_TOP          

 L. 622       598  LOAD_CONST               None
              600  LOAD_FAST                'outcome'
              602  STORE_ATTR               expectedFailure

 L. 625       604  LOAD_CONST               None
              606  LOAD_FAST                'self'
              608  STORE_ATTR               _outcome
              610  JUMP_FORWARD        684  'to 684'
            612_0  COME_FROM_FINALLY   206  '206'

 L. 612       612  LOAD_FAST                'result'
              614  LOAD_METHOD              stopTest
              616  LOAD_FAST                'self'
              618  CALL_METHOD_1         1  ''
              620  POP_TOP          

 L. 613       622  LOAD_FAST                'orig_result'
              624  LOAD_CONST               None
              626  <117>                 0  ''
          628_630  POP_JUMP_IF_FALSE   660  'to 660'

 L. 614       632  LOAD_GLOBAL              getattr
              634  LOAD_FAST                'result'
              636  LOAD_STR                 'stopTestRun'
              638  LOAD_CONST               None
              640  CALL_FUNCTION_3       3  ''
              642  STORE_FAST               'stopTestRun'

 L. 615       644  LOAD_FAST                'stopTestRun'
              646  LOAD_CONST               None
              648  <117>                 1  ''
          650_652  POP_JUMP_IF_FALSE   660  'to 660'

 L. 616       654  LOAD_FAST                'stopTestRun'
              656  CALL_FUNCTION_0       0  ''
              658  POP_TOP          
            660_0  COME_FROM           650  '650'
            660_1  COME_FROM           628  '628'

 L. 621       660  LOAD_FAST                'outcome'
              662  LOAD_ATTR                errors
              664  LOAD_METHOD              clear
              666  CALL_METHOD_0         0  ''
              668  POP_TOP          

 L. 622       670  LOAD_CONST               None
              672  LOAD_FAST                'outcome'
              674  STORE_ATTR               expectedFailure

 L. 625       676  LOAD_CONST               None
              678  LOAD_FAST                'self'
              680  STORE_ATTR               _outcome
              682  <48>             
            684_0  COME_FROM           610  '610'

Parse error at or near `<117>' instruction at offset 8

    def doCleanups--- This code section failed: ---

 L. 630         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _outcome
                4  JUMP_IF_TRUE_OR_POP    10  'to 10'
                6  LOAD_GLOBAL              _Outcome
                8  CALL_FUNCTION_0       0  ''
             10_0  COME_FROM             4  '4'
               10  STORE_FAST               'outcome'
             12_0  COME_FROM           100  '100'
             12_1  COME_FROM            82  '82'

 L. 631        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _cleanups
               16  POP_JUMP_IF_FALSE   102  'to 102'

 L. 632        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _cleanups
               22  LOAD_METHOD              pop
               24  CALL_METHOD_0         0  ''
               26  UNPACK_SEQUENCE_3     3 
               28  STORE_FAST               'function'
               30  STORE_FAST               'args'
               32  STORE_FAST               'kwargs'

 L. 633        34  LOAD_FAST                'outcome'
               36  LOAD_METHOD              testPartExecutor
               38  LOAD_FAST                'self'
               40  CALL_METHOD_1         1  ''
               42  SETUP_WITH           84  'to 84'
               44  POP_TOP          

 L. 634        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _callCleanup
               50  LOAD_FAST                'function'
               52  BUILD_LIST_1          1 
               54  LOAD_FAST                'args'
               56  CALL_FINALLY         59  'to 59'
               58  WITH_CLEANUP_FINISH
               60  BUILD_MAP_0           0 
               62  LOAD_FAST                'kwargs'
               64  <164>                 1  ''
               66  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               68  POP_TOP          
               70  POP_BLOCK        
               72  LOAD_CONST               None
               74  DUP_TOP          
               76  DUP_TOP          
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_BACK            12  'to 12'
             84_0  COME_FROM_WITH       42  '42'
               84  <49>             
               86  POP_JUMP_IF_TRUE     90  'to 90'
               88  <48>             
             90_0  COME_FROM            86  '86'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          
               96  POP_EXCEPT       
               98  POP_TOP          
              100  JUMP_BACK            12  'to 12'
            102_0  COME_FROM            16  '16'

 L. 638       102  LOAD_FAST                'outcome'
              104  LOAD_ATTR                success
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 56

    @classmethod
    def doClassCleanups--- This code section failed: ---

 L. 644         0  BUILD_LIST_0          0 
                2  LOAD_FAST                'cls'
                4  STORE_ATTR               tearDown_exceptions
              6_0  COME_FROM            82  '82'
              6_1  COME_FROM            78  '78'
              6_2  COME_FROM            46  '46'

 L. 645         6  LOAD_FAST                'cls'
                8  LOAD_ATTR                _class_cleanups
               10  POP_JUMP_IF_FALSE    84  'to 84'

 L. 646        12  LOAD_FAST                'cls'
               14  LOAD_ATTR                _class_cleanups
               16  LOAD_METHOD              pop
               18  CALL_METHOD_0         0  ''
               20  UNPACK_SEQUENCE_3     3 
               22  STORE_FAST               'function'
               24  STORE_FAST               'args'
               26  STORE_FAST               'kwargs'

 L. 647        28  SETUP_FINALLY        48  'to 48'

 L. 648        30  LOAD_FAST                'function'
               32  LOAD_FAST                'args'
               34  BUILD_MAP_0           0 
               36  LOAD_FAST                'kwargs'
               38  <164>                 1  ''
               40  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               42  POP_TOP          
               44  POP_BLOCK        
               46  JUMP_BACK             6  'to 6'
             48_0  COME_FROM_FINALLY    28  '28'

 L. 649        48  DUP_TOP          
               50  LOAD_GLOBAL              Exception
               52  <121>                80  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 650        60  LOAD_FAST                'cls'
               62  LOAD_ATTR                tearDown_exceptions
               64  LOAD_METHOD              append
               66  LOAD_GLOBAL              sys
               68  LOAD_METHOD              exc_info
               70  CALL_METHOD_0         0  ''
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
               76  POP_EXCEPT       
               78  JUMP_BACK             6  'to 6'
               80  <48>             
               82  JUMP_BACK             6  'to 6'
             84_0  COME_FROM            10  '10'

Parse error at or near `<164>' instruction at offset 38

    def __call__--- This code section failed: ---

 L. 653         0  LOAD_FAST                'self'
                2  LOAD_ATTR                run
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwds'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def debug--- This code section failed: ---

 L. 657         0  LOAD_FAST                'self'
                2  LOAD_METHOD              setUp
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 658         8  LOAD_GLOBAL              getattr
               10  LOAD_FAST                'self'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _testMethodName
               16  CALL_FUNCTION_2       2  ''
               18  CALL_FUNCTION_0       0  ''
               20  POP_TOP          

 L. 659        22  LOAD_FAST                'self'
               24  LOAD_METHOD              tearDown
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
             30_0  COME_FROM            68  '68'

 L. 660        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _cleanups
               34  POP_JUMP_IF_FALSE    70  'to 70'

 L. 661        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _cleanups
               40  LOAD_METHOD              pop
               42  LOAD_CONST               -1
               44  CALL_METHOD_1         1  ''
               46  UNPACK_SEQUENCE_3     3 
               48  STORE_FAST               'function'
               50  STORE_FAST               'args'
               52  STORE_FAST               'kwargs'

 L. 662        54  LOAD_FAST                'function'
               56  LOAD_FAST                'args'
               58  BUILD_MAP_0           0 
               60  LOAD_FAST                'kwargs'
               62  <164>                 1  ''
               64  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               66  POP_TOP          
               68  JUMP_BACK            30  'to 30'
             70_0  COME_FROM            34  '34'

Parse error at or near `<164>' instruction at offset 62

    def skipTest(self, reason):
        """Skip this test."""
        raise SkipTest(reason)

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failureExceptionmsg

    def assertFalse(self, expr, msg=None):
        """Check that the expression is false."""
        if expr:
            msg = self._formatMessage(msg, '%s is not false' % safe_repr(expr))
            raise self.failureExceptionmsg

    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        if not expr:
            msg = self._formatMessage(msg, '%s is not true' % safe_repr(expr))
            raise self.failureExceptionmsg

    def _formatMessage--- This code section failed: ---

 L. 694         0  LOAD_FAST                'self'
                2  LOAD_ATTR                longMessage
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 695         6  LOAD_FAST                'msg'
                8  JUMP_IF_TRUE_OR_POP    12  'to 12'
               10  LOAD_FAST                'standardMsg'
             12_0  COME_FROM             8  '8'
               12  RETURN_VALUE     
             14_0  COME_FROM             4  '4'

 L. 696        14  LOAD_FAST                'msg'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 697        22  LOAD_FAST                'standardMsg'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 698        26  SETUP_FINALLY        42  'to 42'

 L. 701        28  LOAD_STR                 '%s : %s'
               30  LOAD_FAST                'standardMsg'
               32  LOAD_FAST                'msg'
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    26  '26'

 L. 702        42  DUP_TOP          
               44  LOAD_GLOBAL              UnicodeDecodeError
               46  <121>                78  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 703        54  LOAD_STR                 '%s : %s'
               56  LOAD_GLOBAL              safe_repr
               58  LOAD_FAST                'standardMsg'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_GLOBAL              safe_repr
               64  LOAD_FAST                'msg'
               66  CALL_FUNCTION_1       1  ''
               68  BUILD_TUPLE_2         2 
               70  BINARY_MODULO    
               72  ROT_FOUR         
               74  POP_EXCEPT       
               76  RETURN_VALUE     
               78  <48>             

Parse error at or near `<117>' instruction at offset 18

    def assertRaises--- This code section failed: ---

 L. 731         0  LOAD_GLOBAL              _AssertRaisesContext
                2  LOAD_FAST                'expected_exception'
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'context'

 L. 732        10  SETUP_FINALLY        32  'to 32'

 L. 733        12  LOAD_FAST                'context'
               14  LOAD_METHOD              handle
               16  LOAD_STR                 'assertRaises'
               18  LOAD_FAST                'args'
               20  LOAD_FAST                'kwargs'
               22  CALL_METHOD_3         3  ''
               24  POP_BLOCK        

 L. 736        26  LOAD_CONST               None
               28  STORE_FAST               'context'

 L. 733        30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY    10  '10'

 L. 736        32  LOAD_CONST               None
               34  STORE_FAST               'context'
               36  <48>             

Parse error at or near `STORE_FAST' instruction at offset 28

    def assertWarns(self, expected_warning, *args, **kwargs):
        """Fail unless a warning of class warnClass is triggered
           by the callable when invoked with specified positional and
           keyword arguments.  If a different type of warning is
           triggered, it will not be handled: depending on the other
           warning filtering rules in effect, it might be silenced, printed
           out, or raised as an exception.

           If called with the callable and arguments omitted, will return a
           context object used like this::

                with self.assertWarns(SomeWarning):
                    do_something()

           An optional keyword argument 'msg' can be provided when assertWarns
           is used as a context object.

           The context manager keeps a reference to the first matching
           warning as the 'warning' attribute; similarly, the 'filename'
           and 'lineno' attributes give you information about the line
           of Python code from which the warning was triggered.
           This allows you to inspect the warning after the assertion::

               with self.assertWarns(SomeWarning) as cm:
                   do_something()
               the_warning = cm.warning
               self.assertEqual(the_warning.some_attribute, 147)
        """
        context = _AssertWarnsContext(expected_warning, self)
        return context.handle'assertWarns'argskwargs

    def assertLogs(self, logger=None, level=None):
        """Fail unless a log message of level *level* or higher is emitted
        on *logger_name* or its children.  If omitted, *level* defaults to
        INFO and *logger* defaults to the root logger.

        This method must be used as a context manager, and will yield
        a recording object with two attributes: `output` and `records`.
        At the end of the context manager, the `output` attribute will
        be a list of the matching formatted log messages and the
        `records` attribute will be a list of the corresponding LogRecord
        objects.

        Example::

            with self.assertLogs('foo', level='INFO') as cm:
                logging.getLogger('foo').info('first message')
                logging.getLogger('foo.bar').error('second message')
            self.assertEqual(cm.output, ['INFO:foo:first message',
                                         'ERROR:foo.bar:second message'])
        """
        from ._log import _AssertLogsContext
        return _AssertLogsContext(self, logger, level)

    def _getAssertEqualityFunc--- This code section failed: ---

 L. 810         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'first'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'second'
               10  CALL_FUNCTION_1       1  ''
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    64  'to 64'

 L. 811        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _type_equality_funcs
               20  LOAD_METHOD              get
               22  LOAD_GLOBAL              type
               24  LOAD_FAST                'first'
               26  CALL_FUNCTION_1       1  ''
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'asserter'

 L. 812        32  LOAD_FAST                'asserter'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    64  'to 64'

 L. 813        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'asserter'
               44  LOAD_GLOBAL              str
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 814        50  LOAD_GLOBAL              getattr
               52  LOAD_FAST                'self'
               54  LOAD_FAST                'asserter'
               56  CALL_FUNCTION_2       2  ''
               58  STORE_FAST               'asserter'
             60_0  COME_FROM            48  '48'

 L. 815        60  LOAD_FAST                'asserter'
               62  RETURN_VALUE     
             64_0  COME_FROM            38  '38'
             64_1  COME_FROM            14  '14'

 L. 817        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _baseAssertEqual
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _baseAssertEqual(self, first, second, msg=None):
        """The default assertEqual implementation, not type specific."""
        if not first == second:
            standardMsg = '%s != %s' % _common_shorten_repr(first, second)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureExceptionmsg

    def assertEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.
        """
        assertion_func = self._getAssertEqualityFunc(first, second)
        assertion_func(first, second, msg=msg)

    def assertNotEqual(self, first, second, msg=None):
        """Fail if the two objects are equal as determined by the '!='
           operator.
        """
        if not first != second:
            msg = self._formatMessage(msg, '%s == %s' % (safe_repr(first),
             safe_repr(second)))
            raise self.failureExceptionmsg

    def assertAlmostEqual--- This code section failed: ---

 L. 856         0  LOAD_FAST                'first'
                2  LOAD_FAST                'second'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 858         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 859        12  LOAD_FAST                'delta'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    36  'to 36'
               20  LOAD_FAST                'places'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 860        28  LOAD_GLOBAL              TypeError
               30  LOAD_STR                 'specify delta or places not both'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'
             36_1  COME_FROM            18  '18'

 L. 862        36  LOAD_GLOBAL              abs
               38  LOAD_FAST                'first'
               40  LOAD_FAST                'second'
               42  BINARY_SUBTRACT  
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'diff'

 L. 863        48  LOAD_FAST                'delta'
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE   102  'to 102'

 L. 864        56  LOAD_FAST                'diff'
               58  LOAD_FAST                'delta'
               60  COMPARE_OP               <=
               62  POP_JUMP_IF_FALSE    68  'to 68'

 L. 865        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            62  '62'

 L. 867        68  LOAD_STR                 '%s != %s within %s delta (%s difference)'

 L. 868        70  LOAD_GLOBAL              safe_repr
               72  LOAD_FAST                'first'
               74  CALL_FUNCTION_1       1  ''

 L. 869        76  LOAD_GLOBAL              safe_repr
               78  LOAD_FAST                'second'
               80  CALL_FUNCTION_1       1  ''

 L. 870        82  LOAD_GLOBAL              safe_repr
               84  LOAD_FAST                'delta'
               86  CALL_FUNCTION_1       1  ''

 L. 871        88  LOAD_GLOBAL              safe_repr
               90  LOAD_FAST                'diff'
               92  CALL_FUNCTION_1       1  ''

 L. 867        94  BUILD_TUPLE_4         4 
               96  BINARY_MODULO    
               98  STORE_FAST               'standardMsg'
              100  JUMP_FORWARD        160  'to 160'
            102_0  COME_FROM            54  '54'

 L. 873       102  LOAD_FAST                'places'
              104  LOAD_CONST               None
              106  <117>                 0  ''
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 874       110  LOAD_CONST               7
              112  STORE_FAST               'places'
            114_0  COME_FROM           108  '108'

 L. 876       114  LOAD_GLOBAL              round
              116  LOAD_FAST                'diff'
              118  LOAD_FAST                'places'
              120  CALL_FUNCTION_2       2  ''
              122  LOAD_CONST               0
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   132  'to 132'

 L. 877       128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

 L. 879       132  LOAD_STR                 '%s != %s within %r places (%s difference)'

 L. 880       134  LOAD_GLOBAL              safe_repr
              136  LOAD_FAST                'first'
              138  CALL_FUNCTION_1       1  ''

 L. 881       140  LOAD_GLOBAL              safe_repr
              142  LOAD_FAST                'second'
              144  CALL_FUNCTION_1       1  ''

 L. 882       146  LOAD_FAST                'places'

 L. 883       148  LOAD_GLOBAL              safe_repr
              150  LOAD_FAST                'diff'
              152  CALL_FUNCTION_1       1  ''

 L. 879       154  BUILD_TUPLE_4         4 
              156  BINARY_MODULO    
              158  STORE_FAST               'standardMsg'
            160_0  COME_FROM           100  '100'

 L. 884       160  LOAD_FAST                'self'
              162  LOAD_METHOD              _formatMessage
              164  LOAD_FAST                'msg'
              166  LOAD_FAST                'standardMsg'
              168  CALL_METHOD_2         2  ''
              170  STORE_FAST               'msg'

 L. 885       172  LOAD_FAST                'self'
              174  LOAD_METHOD              failureException
              176  LOAD_FAST                'msg'
              178  CALL_METHOD_1         1  ''
              180  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 16

    def assertNotAlmostEqual--- This code section failed: ---

 L. 899         0  LOAD_FAST                'delta'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_FAST                'places'
               10  LOAD_CONST               None
               12  <117>                 1  ''
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 900        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'specify delta or places not both'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 901        24  LOAD_GLOBAL              abs
               26  LOAD_FAST                'first'
               28  LOAD_FAST                'second'
               30  BINARY_SUBTRACT  
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'diff'

 L. 902        36  LOAD_FAST                'delta'
               38  LOAD_CONST               None
               40  <117>                 1  ''
               42  POP_JUMP_IF_FALSE    98  'to 98'

 L. 903        44  LOAD_FAST                'first'
               46  LOAD_FAST                'second'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_TRUE     64  'to 64'
               52  LOAD_FAST                'diff'
               54  LOAD_FAST                'delta'
               56  COMPARE_OP               >
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L. 904        60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM            50  '50'

 L. 905        64  LOAD_STR                 '%s == %s within %s delta (%s difference)'

 L. 906        66  LOAD_GLOBAL              safe_repr
               68  LOAD_FAST                'first'
               70  CALL_FUNCTION_1       1  ''

 L. 907        72  LOAD_GLOBAL              safe_repr
               74  LOAD_FAST                'second'
               76  CALL_FUNCTION_1       1  ''

 L. 908        78  LOAD_GLOBAL              safe_repr
               80  LOAD_FAST                'delta'
               82  CALL_FUNCTION_1       1  ''

 L. 909        84  LOAD_GLOBAL              safe_repr
               86  LOAD_FAST                'diff'
               88  CALL_FUNCTION_1       1  ''

 L. 905        90  BUILD_TUPLE_4         4 
               92  BINARY_MODULO    
               94  STORE_FAST               'standardMsg'
               96  JUMP_FORWARD        158  'to 158'
             98_0  COME_FROM            42  '42'

 L. 911        98  LOAD_FAST                'places'
              100  LOAD_CONST               None
              102  <117>                 0  ''
              104  POP_JUMP_IF_FALSE   110  'to 110'

 L. 912       106  LOAD_CONST               7
              108  STORE_FAST               'places'
            110_0  COME_FROM           104  '104'

 L. 913       110  LOAD_FAST                'first'
              112  LOAD_FAST                'second'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    136  'to 136'
              118  LOAD_GLOBAL              round
              120  LOAD_FAST                'diff'
              122  LOAD_FAST                'places'
              124  CALL_FUNCTION_2       2  ''
              126  LOAD_CONST               0
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 914       132  LOAD_CONST               None
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'
            136_1  COME_FROM           116  '116'

 L. 915       136  LOAD_STR                 '%s == %s within %r places'
              138  LOAD_GLOBAL              safe_repr
              140  LOAD_FAST                'first'
              142  CALL_FUNCTION_1       1  ''

 L. 916       144  LOAD_GLOBAL              safe_repr
              146  LOAD_FAST                'second'
              148  CALL_FUNCTION_1       1  ''

 L. 917       150  LOAD_FAST                'places'

 L. 915       152  BUILD_TUPLE_3         3 
              154  BINARY_MODULO    
              156  STORE_FAST               'standardMsg'
            158_0  COME_FROM            96  '96'

 L. 919       158  LOAD_FAST                'self'
              160  LOAD_METHOD              _formatMessage
              162  LOAD_FAST                'msg'
              164  LOAD_FAST                'standardMsg'
              166  CALL_METHOD_2         2  ''
              168  STORE_FAST               'msg'

 L. 920       170  LOAD_FAST                'self'
              172  LOAD_METHOD              failureException
              174  LOAD_FAST                'msg'
              176  CALL_METHOD_1         1  ''
              178  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    def assertSequenceEqual--- This code section failed: ---

 L. 936         0  LOAD_FAST                'seq_type'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    80  'to 80'

 L. 937         8  LOAD_FAST                'seq_type'
               10  LOAD_ATTR                __name__
               12  STORE_FAST               'seq_type_name'

 L. 938        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'seq1'
               18  LOAD_FAST                'seq_type'
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     46  'to 46'

 L. 939        24  LOAD_FAST                'self'
               26  LOAD_METHOD              failureException
               28  LOAD_STR                 'First sequence is not a %s: %s'

 L. 940        30  LOAD_FAST                'seq_type_name'
               32  LOAD_GLOBAL              safe_repr
               34  LOAD_FAST                'seq1'
               36  CALL_FUNCTION_1       1  ''
               38  BUILD_TUPLE_2         2 

 L. 939        40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            22  '22'

 L. 941        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'seq2'
               50  LOAD_FAST                'seq_type'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     84  'to 84'

 L. 942        56  LOAD_FAST                'self'
               58  LOAD_METHOD              failureException
               60  LOAD_STR                 'Second sequence is not a %s: %s'

 L. 943        62  LOAD_FAST                'seq_type_name'
               64  LOAD_GLOBAL              safe_repr
               66  LOAD_FAST                'seq2'
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_2         2 

 L. 942        72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  JUMP_FORWARD         84  'to 84'
             80_0  COME_FROM             6  '6'

 L. 945        80  LOAD_STR                 'sequence'
               82  STORE_FAST               'seq_type_name'
             84_0  COME_FROM            78  '78'
             84_1  COME_FROM            54  '54'

 L. 947        84  LOAD_CONST               None
               86  STORE_FAST               'differing'

 L. 948        88  SETUP_FINALLY       102  'to 102'

 L. 949        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'seq1'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'len1'
               98  POP_BLOCK        
              100  JUMP_FORWARD        132  'to 132'
            102_0  COME_FROM_FINALLY    88  '88'

 L. 950       102  DUP_TOP          
              104  LOAD_GLOBAL              TypeError
              106  LOAD_GLOBAL              NotImplementedError
              108  BUILD_TUPLE_2         2 
              110  <121>               130  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 951       118  LOAD_STR                 'First %s has no length.    Non-sequence?'

 L. 952       120  LOAD_FAST                'seq_type_name'

 L. 951       122  BINARY_MODULO    
              124  STORE_FAST               'differing'
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
              130  <48>             
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM           100  '100'

 L. 954       132  LOAD_FAST                'differing'
              134  LOAD_CONST               None
              136  <117>                 0  ''
              138  POP_JUMP_IF_FALSE   184  'to 184'

 L. 955       140  SETUP_FINALLY       154  'to 154'

 L. 956       142  LOAD_GLOBAL              len
              144  LOAD_FAST                'seq2'
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'len2'
              150  POP_BLOCK        
              152  JUMP_FORWARD        184  'to 184'
            154_0  COME_FROM_FINALLY   140  '140'

 L. 957       154  DUP_TOP          
              156  LOAD_GLOBAL              TypeError
              158  LOAD_GLOBAL              NotImplementedError
              160  BUILD_TUPLE_2         2 
              162  <121>               182  ''
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 958       170  LOAD_STR                 'Second %s has no length.    Non-sequence?'

 L. 959       172  LOAD_FAST                'seq_type_name'

 L. 958       174  BINARY_MODULO    
              176  STORE_FAST               'differing'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           152  '152'
            184_2  COME_FROM           138  '138'

 L. 961       184  LOAD_FAST                'differing'
              186  LOAD_CONST               None
              188  <117>                 0  ''
          190_192  POP_JUMP_IF_FALSE   664  'to 664'

 L. 962       194  LOAD_FAST                'seq1'
              196  LOAD_FAST                'seq2'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   206  'to 206'

 L. 963       202  LOAD_CONST               None
              204  RETURN_VALUE     
            206_0  COME_FROM           200  '200'

 L. 965       206  LOAD_STR                 '%ss differ: %s != %s\n'

 L. 966       208  LOAD_FAST                'seq_type_name'
              210  LOAD_METHOD              capitalize
              212  CALL_METHOD_0         0  ''
              214  BUILD_TUPLE_1         1 

 L. 967       216  LOAD_GLOBAL              _common_shorten_repr
              218  LOAD_FAST                'seq1'
              220  LOAD_FAST                'seq2'
              222  CALL_FUNCTION_2       2  ''

 L. 966       224  BINARY_ADD       

 L. 965       226  BINARY_MODULO    
              228  STORE_FAST               'differing'

 L. 969       230  LOAD_GLOBAL              range
              232  LOAD_GLOBAL              min
              234  LOAD_FAST                'len1'
              236  LOAD_FAST                'len2'
              238  CALL_FUNCTION_2       2  ''
              240  CALL_FUNCTION_1       1  ''
              242  GET_ITER         
            244_0  COME_FROM           414  '414'
            244_1  COME_FROM           382  '382'
              244  FOR_ITER            416  'to 416'
              246  STORE_FAST               'i'

 L. 970       248  SETUP_FINALLY       262  'to 262'

 L. 971       250  LOAD_FAST                'seq1'
              252  LOAD_FAST                'i'
              254  BINARY_SUBSCR    
              256  STORE_FAST               'item1'
              258  POP_BLOCK        
              260  JUMP_FORWARD        312  'to 312'
            262_0  COME_FROM_FINALLY   248  '248'

 L. 972       262  DUP_TOP          
              264  LOAD_GLOBAL              TypeError
              266  LOAD_GLOBAL              IndexError
              268  LOAD_GLOBAL              NotImplementedError
              270  BUILD_TUPLE_3         3 
          272_274  <121>               310  ''
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          

 L. 973       282  LOAD_FAST                'differing'
              284  LOAD_STR                 '\nUnable to index element %d of first %s\n'

 L. 974       286  LOAD_FAST                'i'
              288  LOAD_FAST                'seq_type_name'
              290  BUILD_TUPLE_2         2 

 L. 973       292  BINARY_MODULO    
              294  INPLACE_ADD      
              296  STORE_FAST               'differing'

 L. 975       298  POP_EXCEPT       
              300  POP_TOP          
          302_304  JUMP_FORWARD        458  'to 458'
              306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
              310  <48>             
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           260  '260'

 L. 977       312  SETUP_FINALLY       326  'to 326'

 L. 978       314  LOAD_FAST                'seq2'
              316  LOAD_FAST                'i'
              318  BINARY_SUBSCR    
              320  STORE_FAST               'item2'
              322  POP_BLOCK        
              324  JUMP_FORWARD        376  'to 376'
            326_0  COME_FROM_FINALLY   312  '312'

 L. 979       326  DUP_TOP          
              328  LOAD_GLOBAL              TypeError
              330  LOAD_GLOBAL              IndexError
              332  LOAD_GLOBAL              NotImplementedError
              334  BUILD_TUPLE_3         3 
          336_338  <121>               374  ''
              340  POP_TOP          
              342  POP_TOP          
              344  POP_TOP          

 L. 980       346  LOAD_FAST                'differing'
              348  LOAD_STR                 '\nUnable to index element %d of second %s\n'

 L. 981       350  LOAD_FAST                'i'
              352  LOAD_FAST                'seq_type_name'
              354  BUILD_TUPLE_2         2 

 L. 980       356  BINARY_MODULO    
              358  INPLACE_ADD      
              360  STORE_FAST               'differing'

 L. 982       362  POP_EXCEPT       
              364  POP_TOP          
          366_368  JUMP_FORWARD        458  'to 458'
              370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
              374  <48>             
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           324  '324'

 L. 984       376  LOAD_FAST                'item1'
              378  LOAD_FAST                'item2'
              380  COMPARE_OP               !=
              382  POP_JUMP_IF_FALSE_BACK   244  'to 244'

 L. 985       384  LOAD_FAST                'differing'
              386  LOAD_STR                 '\nFirst differing element %d:\n%s\n%s\n'

 L. 986       388  LOAD_FAST                'i'
              390  BUILD_TUPLE_1         1 
              392  LOAD_GLOBAL              _common_shorten_repr
              394  LOAD_FAST                'item1'
              396  LOAD_FAST                'item2'
              398  CALL_FUNCTION_2       2  ''
              400  BINARY_ADD       

 L. 985       402  BINARY_MODULO    
              404  INPLACE_ADD      
              406  STORE_FAST               'differing'

 L. 987       408  POP_TOP          
          410_412  BREAK_LOOP          458  'to 458'
              414  JUMP_BACK           244  'to 244'
            416_0  COME_FROM           244  '244'

 L. 989       416  LOAD_FAST                'len1'
              418  LOAD_FAST                'len2'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   458  'to 458'
              426  LOAD_FAST                'seq_type'
              428  LOAD_CONST               None
              430  <117>                 0  ''
          432_434  POP_JUMP_IF_FALSE   458  'to 458'

 L. 990       436  LOAD_GLOBAL              type
              438  LOAD_FAST                'seq1'
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_GLOBAL              type
              444  LOAD_FAST                'seq2'
              446  CALL_FUNCTION_1       1  ''
              448  COMPARE_OP               !=

 L. 989   450_452  POP_JUMP_IF_FALSE   458  'to 458'

 L. 992       454  LOAD_CONST               None
              456  RETURN_VALUE     
            458_0  COME_FROM           450  '450'
            458_1  COME_FROM           432  '432'
            458_2  COME_FROM           422  '422'
            458_3  COME_FROM           410  '410'
            458_4  COME_FROM           366  '366'
            458_5  COME_FROM           302  '302'

 L. 994       458  LOAD_FAST                'len1'
              460  LOAD_FAST                'len2'
              462  COMPARE_OP               >
          464_466  POP_JUMP_IF_FALSE   562  'to 562'

 L. 995       468  LOAD_FAST                'differing'
              470  LOAD_STR                 '\nFirst %s contains %d additional elements.\n'

 L. 996       472  LOAD_FAST                'seq_type_name'
              474  LOAD_FAST                'len1'
              476  LOAD_FAST                'len2'
              478  BINARY_SUBTRACT  
              480  BUILD_TUPLE_2         2 

 L. 995       482  BINARY_MODULO    
              484  INPLACE_ADD      
              486  STORE_FAST               'differing'

 L. 997       488  SETUP_FINALLY       518  'to 518'

 L. 998       490  LOAD_FAST                'differing'
              492  LOAD_STR                 'First extra element %d:\n%s\n'

 L. 999       494  LOAD_FAST                'len2'
              496  LOAD_GLOBAL              safe_repr
              498  LOAD_FAST                'seq1'
              500  LOAD_FAST                'len2'
              502  BINARY_SUBSCR    
              504  CALL_FUNCTION_1       1  ''
              506  BUILD_TUPLE_2         2 

 L. 998       508  BINARY_MODULO    
              510  INPLACE_ADD      
              512  STORE_FAST               'differing'
              514  POP_BLOCK        
              516  JUMP_FORWARD        560  'to 560'
            518_0  COME_FROM_FINALLY   488  '488'

 L.1000       518  DUP_TOP          
              520  LOAD_GLOBAL              TypeError
              522  LOAD_GLOBAL              IndexError
              524  LOAD_GLOBAL              NotImplementedError
              526  BUILD_TUPLE_3         3 
          528_530  <121>               558  ''
              532  POP_TOP          
              534  POP_TOP          
              536  POP_TOP          

 L.1001       538  LOAD_FAST                'differing'
              540  LOAD_STR                 'Unable to index element %d of first %s\n'

 L.1002       542  LOAD_FAST                'len2'
              544  LOAD_FAST                'seq_type_name'
              546  BUILD_TUPLE_2         2 

 L.1001       548  BINARY_MODULO    
              550  INPLACE_ADD      
              552  STORE_FAST               'differing'
              554  POP_EXCEPT       
              556  JUMP_FORWARD        560  'to 560'
              558  <48>             
            560_0  COME_FROM           556  '556'
            560_1  COME_FROM           516  '516'
              560  JUMP_FORWARD        664  'to 664'
            562_0  COME_FROM           464  '464'

 L.1003       562  LOAD_FAST                'len1'
              564  LOAD_FAST                'len2'
              566  COMPARE_OP               <
          568_570  POP_JUMP_IF_FALSE   664  'to 664'

 L.1004       572  LOAD_FAST                'differing'
              574  LOAD_STR                 '\nSecond %s contains %d additional elements.\n'

 L.1005       576  LOAD_FAST                'seq_type_name'
              578  LOAD_FAST                'len2'
              580  LOAD_FAST                'len1'
              582  BINARY_SUBTRACT  
              584  BUILD_TUPLE_2         2 

 L.1004       586  BINARY_MODULO    
              588  INPLACE_ADD      
              590  STORE_FAST               'differing'

 L.1006       592  SETUP_FINALLY       622  'to 622'

 L.1007       594  LOAD_FAST                'differing'
              596  LOAD_STR                 'First extra element %d:\n%s\n'

 L.1008       598  LOAD_FAST                'len1'
              600  LOAD_GLOBAL              safe_repr
              602  LOAD_FAST                'seq2'
              604  LOAD_FAST                'len1'
              606  BINARY_SUBSCR    
              608  CALL_FUNCTION_1       1  ''
              610  BUILD_TUPLE_2         2 

 L.1007       612  BINARY_MODULO    
              614  INPLACE_ADD      
              616  STORE_FAST               'differing'
              618  POP_BLOCK        
              620  JUMP_FORWARD        664  'to 664'
            622_0  COME_FROM_FINALLY   592  '592'

 L.1009       622  DUP_TOP          
              624  LOAD_GLOBAL              TypeError
              626  LOAD_GLOBAL              IndexError
              628  LOAD_GLOBAL              NotImplementedError
              630  BUILD_TUPLE_3         3 
          632_634  <121>               662  ''
              636  POP_TOP          
              638  POP_TOP          
              640  POP_TOP          

 L.1010       642  LOAD_FAST                'differing'
              644  LOAD_STR                 'Unable to index element %d of second %s\n'

 L.1011       646  LOAD_FAST                'len1'
              648  LOAD_FAST                'seq_type_name'
              650  BUILD_TUPLE_2         2 

 L.1010       652  BINARY_MODULO    
              654  INPLACE_ADD      
              656  STORE_FAST               'differing'
              658  POP_EXCEPT       
              660  JUMP_FORWARD        664  'to 664'
              662  <48>             
            664_0  COME_FROM           660  '660'
            664_1  COME_FROM           620  '620'
            664_2  COME_FROM           568  '568'
            664_3  COME_FROM           560  '560'
            664_4  COME_FROM           190  '190'

 L.1012       664  LOAD_FAST                'differing'
              666  STORE_FAST               'standardMsg'

 L.1013       668  LOAD_STR                 '\n'
              670  LOAD_STR                 '\n'
              672  LOAD_METHOD              join

 L.1014       674  LOAD_GLOBAL              difflib
              676  LOAD_METHOD              ndiff
              678  LOAD_GLOBAL              pprint
              680  LOAD_METHOD              pformat
              682  LOAD_FAST                'seq1'
              684  CALL_METHOD_1         1  ''
              686  LOAD_METHOD              splitlines
              688  CALL_METHOD_0         0  ''

 L.1015       690  LOAD_GLOBAL              pprint
              692  LOAD_METHOD              pformat
              694  LOAD_FAST                'seq2'
              696  CALL_METHOD_1         1  ''
              698  LOAD_METHOD              splitlines
              700  CALL_METHOD_0         0  ''

 L.1014       702  CALL_METHOD_2         2  ''

 L.1013       704  CALL_METHOD_1         1  ''
              706  BINARY_ADD       
              708  STORE_FAST               'diffMsg'

 L.1017       710  LOAD_FAST                'self'
              712  LOAD_METHOD              _truncateMessage
              714  LOAD_FAST                'standardMsg'
              716  LOAD_FAST                'diffMsg'
              718  CALL_METHOD_2         2  ''
              720  STORE_FAST               'standardMsg'

 L.1018       722  LOAD_FAST                'self'
              724  LOAD_METHOD              _formatMessage
              726  LOAD_FAST                'msg'
              728  LOAD_FAST                'standardMsg'
              730  CALL_METHOD_2         2  ''
              732  STORE_FAST               'msg'

 L.1019       734  LOAD_FAST                'self'
              736  LOAD_METHOD              fail
              738  LOAD_FAST                'msg'
              740  CALL_METHOD_1         1  ''
              742  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _truncateMessage--- This code section failed: ---

 L.1022         0  LOAD_FAST                'self'
                2  LOAD_ATTR                maxDiff
                4  STORE_FAST               'max_diff'

 L.1023         6  LOAD_FAST                'max_diff'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_TRUE     26  'to 26'
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'diff'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_FAST                'max_diff'
               22  COMPARE_OP               <=
               24  POP_JUMP_IF_FALSE    34  'to 34'
             26_0  COME_FROM            12  '12'

 L.1024        26  LOAD_FAST                'message'
               28  LOAD_FAST                'diff'
               30  BINARY_ADD       
               32  RETURN_VALUE     
             34_0  COME_FROM            24  '24'

 L.1025        34  LOAD_FAST                'message'
               36  LOAD_GLOBAL              DIFF_OMITTED
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'diff'
               42  CALL_FUNCTION_1       1  ''
               44  BINARY_MODULO    
               46  BINARY_ADD       
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def assertListEqual(self, list1, list2, msg=None):
        """A list-specific equality assertion.

        Args:
            list1: The first list to compare.
            list2: The second list to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.

        """
        self.assertSequenceEqual(list1, list2, msg, seq_type=list)

    def assertTupleEqual(self, tuple1, tuple2, msg=None):
        """A tuple-specific equality assertion.

        Args:
            tuple1: The first tuple to compare.
            tuple2: The second tuple to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.
        """
        self.assertSequenceEqual(tuple1, tuple2, msg, seq_type=tuple)

    def assertSetEqual--- This code section failed: ---

 L.1063         0  SETUP_FINALLY        16  'to 16'

 L.1064         2  LOAD_FAST                'set1'
                4  LOAD_METHOD              difference
                6  LOAD_FAST                'set2'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'difference1'
               12  POP_BLOCK        
               14  JUMP_FORWARD        114  'to 114'
             16_0  COME_FROM_FINALLY     0  '0'

 L.1065        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  <121>                64  ''
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        56  'to 56'

 L.1066        30  LOAD_FAST                'self'
               32  LOAD_METHOD              fail
               34  LOAD_STR                 'invalid type when attempting set difference: %s'
               36  LOAD_FAST                'e'
               38  BINARY_MODULO    
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'e'
               52  DELETE_FAST              'e'
               54  JUMP_FORWARD        114  'to 114'
             56_0  COME_FROM_FINALLY    28  '28'
               56  LOAD_CONST               None
               58  STORE_FAST               'e'
               60  DELETE_FAST              'e'
               62  <48>             

 L.1067        64  DUP_TOP          
               66  LOAD_GLOBAL              AttributeError
               68  <121>               112  ''
               70  POP_TOP          
               72  STORE_FAST               'e'
               74  POP_TOP          
               76  SETUP_FINALLY       104  'to 104'

 L.1068        78  LOAD_FAST                'self'
               80  LOAD_METHOD              fail
               82  LOAD_STR                 'first argument does not support set difference: %s'
               84  LOAD_FAST                'e'
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  POP_BLOCK        
               94  POP_EXCEPT       
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  JUMP_FORWARD        114  'to 114'
            104_0  COME_FROM_FINALLY    76  '76'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  <48>             
              112  <48>             
            114_0  COME_FROM           102  '102'
            114_1  COME_FROM            54  '54'
            114_2  COME_FROM            14  '14'

 L.1070       114  SETUP_FINALLY       130  'to 130'

 L.1071       116  LOAD_FAST                'set2'
              118  LOAD_METHOD              difference
              120  LOAD_FAST                'set1'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'difference2'
              126  POP_BLOCK        
              128  JUMP_FORWARD        228  'to 228'
            130_0  COME_FROM_FINALLY   114  '114'

 L.1072       130  DUP_TOP          
              132  LOAD_GLOBAL              TypeError
              134  <121>               178  ''
              136  POP_TOP          
              138  STORE_FAST               'e'
              140  POP_TOP          
              142  SETUP_FINALLY       170  'to 170'

 L.1073       144  LOAD_FAST                'self'
              146  LOAD_METHOD              fail
              148  LOAD_STR                 'invalid type when attempting set difference: %s'
              150  LOAD_FAST                'e'
              152  BINARY_MODULO    
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  POP_BLOCK        
              160  POP_EXCEPT       
              162  LOAD_CONST               None
              164  STORE_FAST               'e'
              166  DELETE_FAST              'e'
              168  JUMP_FORWARD        228  'to 228'
            170_0  COME_FROM_FINALLY   142  '142'
              170  LOAD_CONST               None
              172  STORE_FAST               'e'
              174  DELETE_FAST              'e'
              176  <48>             

 L.1074       178  DUP_TOP          
              180  LOAD_GLOBAL              AttributeError
              182  <121>               226  ''
              184  POP_TOP          
              186  STORE_FAST               'e'
              188  POP_TOP          
              190  SETUP_FINALLY       218  'to 218'

 L.1075       192  LOAD_FAST                'self'
              194  LOAD_METHOD              fail
              196  LOAD_STR                 'second argument does not support set difference: %s'
              198  LOAD_FAST                'e'
              200  BINARY_MODULO    
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          
              206  POP_BLOCK        
              208  POP_EXCEPT       
              210  LOAD_CONST               None
              212  STORE_FAST               'e'
              214  DELETE_FAST              'e'
              216  JUMP_FORWARD        228  'to 228'
            218_0  COME_FROM_FINALLY   190  '190'
              218  LOAD_CONST               None
              220  STORE_FAST               'e'
              222  DELETE_FAST              'e'
              224  <48>             
              226  <48>             
            228_0  COME_FROM           216  '216'
            228_1  COME_FROM           168  '168'
            228_2  COME_FROM           128  '128'

 L.1077       228  LOAD_FAST                'difference1'
              230  POP_JUMP_IF_TRUE    240  'to 240'
              232  LOAD_FAST                'difference2'
              234  POP_JUMP_IF_TRUE    240  'to 240'

 L.1078       236  LOAD_CONST               None
              238  RETURN_VALUE     
            240_0  COME_FROM           234  '234'
            240_1  COME_FROM           230  '230'

 L.1080       240  BUILD_LIST_0          0 
              242  STORE_FAST               'lines'

 L.1081       244  LOAD_FAST                'difference1'
          246_248  POP_JUMP_IF_FALSE   286  'to 286'

 L.1082       250  LOAD_FAST                'lines'
              252  LOAD_METHOD              append
              254  LOAD_STR                 'Items in the first set but not the second:'
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L.1083       260  LOAD_FAST                'difference1'
              262  GET_ITER         
            264_0  COME_FROM           282  '282'
              264  FOR_ITER            286  'to 286'
              266  STORE_FAST               'item'

 L.1084       268  LOAD_FAST                'lines'
              270  LOAD_METHOD              append
              272  LOAD_GLOBAL              repr
              274  LOAD_FAST                'item'
              276  CALL_FUNCTION_1       1  ''
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
          282_284  JUMP_BACK           264  'to 264'
            286_0  COME_FROM           264  '264'
            286_1  COME_FROM           246  '246'

 L.1085       286  LOAD_FAST                'difference2'
          288_290  POP_JUMP_IF_FALSE   328  'to 328'

 L.1086       292  LOAD_FAST                'lines'
              294  LOAD_METHOD              append
              296  LOAD_STR                 'Items in the second set but not the first:'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          

 L.1087       302  LOAD_FAST                'difference2'
              304  GET_ITER         
            306_0  COME_FROM           324  '324'
              306  FOR_ITER            328  'to 328'
              308  STORE_FAST               'item'

 L.1088       310  LOAD_FAST                'lines'
              312  LOAD_METHOD              append
              314  LOAD_GLOBAL              repr
              316  LOAD_FAST                'item'
              318  CALL_FUNCTION_1       1  ''
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          
          324_326  JUMP_BACK           306  'to 306'
            328_0  COME_FROM           306  '306'
            328_1  COME_FROM           288  '288'

 L.1090       328  LOAD_STR                 '\n'
              330  LOAD_METHOD              join
              332  LOAD_FAST                'lines'
              334  CALL_METHOD_1         1  ''
              336  STORE_FAST               'standardMsg'

 L.1091       338  LOAD_FAST                'self'
              340  LOAD_METHOD              fail
              342  LOAD_FAST                'self'
              344  LOAD_METHOD              _formatMessage
              346  LOAD_FAST                'msg'
              348  LOAD_FAST                'standardMsg'
              350  CALL_METHOD_2         2  ''
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          

Parse error at or near `<121>' instruction at offset 20

    def assertIn--- This code section failed: ---

 L.1095         0  LOAD_FAST                'member'
                2  LOAD_FAST                'container'
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    46  'to 46'

 L.1096         8  LOAD_STR                 '%s not found in %s'
               10  LOAD_GLOBAL              safe_repr
               12  LOAD_FAST                'member'
               14  CALL_FUNCTION_1       1  ''

 L.1097        16  LOAD_GLOBAL              safe_repr
               18  LOAD_FAST                'container'
               20  CALL_FUNCTION_1       1  ''

 L.1096        22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  STORE_FAST               'standardMsg'

 L.1098        28  LOAD_FAST                'self'
               30  LOAD_METHOD              fail
               32  LOAD_FAST                'self'
               34  LOAD_METHOD              _formatMessage
               36  LOAD_FAST                'msg'
               38  LOAD_FAST                'standardMsg'
               40  CALL_METHOD_2         2  ''
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertNotIn--- This code section failed: ---

 L.1102         0  LOAD_FAST                'member'
                2  LOAD_FAST                'container'
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    46  'to 46'

 L.1103         8  LOAD_STR                 '%s unexpectedly found in %s'
               10  LOAD_GLOBAL              safe_repr
               12  LOAD_FAST                'member'
               14  CALL_FUNCTION_1       1  ''

 L.1104        16  LOAD_GLOBAL              safe_repr
               18  LOAD_FAST                'container'
               20  CALL_FUNCTION_1       1  ''

 L.1103        22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  STORE_FAST               'standardMsg'

 L.1105        28  LOAD_FAST                'self'
               30  LOAD_METHOD              fail
               32  LOAD_FAST                'self'
               34  LOAD_METHOD              _formatMessage
               36  LOAD_FAST                'msg'
               38  LOAD_FAST                'standardMsg'
               40  CALL_METHOD_2         2  ''
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertIs--- This code section failed: ---

 L.1109         0  LOAD_FAST                'expr1'
                2  LOAD_FAST                'expr2'
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    46  'to 46'

 L.1110         8  LOAD_STR                 '%s is not %s'
               10  LOAD_GLOBAL              safe_repr
               12  LOAD_FAST                'expr1'
               14  CALL_FUNCTION_1       1  ''

 L.1111        16  LOAD_GLOBAL              safe_repr
               18  LOAD_FAST                'expr2'
               20  CALL_FUNCTION_1       1  ''

 L.1110        22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  STORE_FAST               'standardMsg'

 L.1112        28  LOAD_FAST                'self'
               30  LOAD_METHOD              fail
               32  LOAD_FAST                'self'
               34  LOAD_METHOD              _formatMessage
               36  LOAD_FAST                'msg'
               38  LOAD_FAST                'standardMsg'
               40  CALL_METHOD_2         2  ''
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertIsNot--- This code section failed: ---

 L.1116         0  LOAD_FAST                'expr1'
                2  LOAD_FAST                'expr2'
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L.1117         8  LOAD_STR                 'unexpectedly identical: %s'
               10  LOAD_GLOBAL              safe_repr
               12  LOAD_FAST                'expr1'
               14  CALL_FUNCTION_1       1  ''
               16  BUILD_TUPLE_1         1 
               18  BINARY_MODULO    
               20  STORE_FAST               'standardMsg'

 L.1118        22  LOAD_FAST                'self'
               24  LOAD_METHOD              fail
               26  LOAD_FAST                'self'
               28  LOAD_METHOD              _formatMessage
               30  LOAD_FAST                'msg'
               32  LOAD_FAST                'standardMsg'
               34  CALL_METHOD_2         2  ''
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
             40_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertDictEqual(self, d1, d2, msg=None):
        self.assertIsInstanced1dict'First argument is not a dictionary'
        self.assertIsInstanced2dict'Second argument is not a dictionary'
        if d1 != d2:
            standardMsg = '%s != %s' % _common_shorten_repr(d1, d2)
            diff = '\n' + '\n'.joindifflib.ndiff(pprint.pformatd1.splitlines, pprint.pformatd2.splitlines)
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.failself._formatMessage(msg, standardMsg)

    def assertDictContainsSubset--- This code section failed: ---

 L.1134         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn
                4  LOAD_STR                 'assertDictContainsSubset is deprecated'

 L.1135         6  LOAD_GLOBAL              DeprecationWarning

 L.1134         8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L.1136        12  BUILD_LIST_0          0 
               14  STORE_FAST               'missing'

 L.1137        16  BUILD_LIST_0          0 
               18  STORE_FAST               'mismatched'

 L.1138        20  LOAD_FAST                'subset'
               22  LOAD_METHOD              items
               24  CALL_METHOD_0         0  ''
               26  GET_ITER         
             28_0  COME_FROM           104  '104'
             28_1  COME_FROM            66  '66'
             28_2  COME_FROM            54  '54'
               28  FOR_ITER            106  'to 106'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'key'
               34  STORE_FAST               'value'

 L.1139        36  LOAD_FAST                'key'
               38  LOAD_FAST                'dictionary'
               40  <118>                 1  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.1140        44  LOAD_FAST                'missing'
               46  LOAD_METHOD              append
               48  LOAD_FAST                'key'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
               54  JUMP_BACK            28  'to 28'
             56_0  COME_FROM            42  '42'

 L.1141        56  LOAD_FAST                'value'
               58  LOAD_FAST                'dictionary'
               60  LOAD_FAST                'key'
               62  BINARY_SUBSCR    
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L.1142        68  LOAD_FAST                'mismatched'
               70  LOAD_METHOD              append
               72  LOAD_STR                 '%s, expected: %s, actual: %s'

 L.1143        74  LOAD_GLOBAL              safe_repr
               76  LOAD_FAST                'key'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_GLOBAL              safe_repr
               82  LOAD_FAST                'value'
               84  CALL_FUNCTION_1       1  ''

 L.1144        86  LOAD_GLOBAL              safe_repr
               88  LOAD_FAST                'dictionary'
               90  LOAD_FAST                'key'
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  ''

 L.1143        96  BUILD_TUPLE_3         3 

 L.1142        98  BINARY_MODULO    
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  JUMP_BACK            28  'to 28'
            106_0  COME_FROM            28  '28'

 L.1146       106  LOAD_FAST                'missing'
              108  POP_JUMP_IF_TRUE    118  'to 118'
              110  LOAD_FAST                'mismatched'
              112  POP_JUMP_IF_TRUE    118  'to 118'

 L.1147       114  LOAD_CONST               None
              116  RETURN_VALUE     
            118_0  COME_FROM           112  '112'
            118_1  COME_FROM           108  '108'

 L.1149       118  LOAD_STR                 ''
              120  STORE_FAST               'standardMsg'

 L.1150       122  LOAD_FAST                'missing'
              124  POP_JUMP_IF_FALSE   150  'to 150'

 L.1151       126  LOAD_STR                 'Missing: %s'
              128  LOAD_STR                 ','
              130  LOAD_METHOD              join
              132  LOAD_GENEXPR             '<code_object <genexpr>>'
              134  LOAD_STR                 'TestCase.assertDictContainsSubset.<locals>.<genexpr>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1152       138  LOAD_FAST                'missing'

 L.1151       140  GET_ITER         
              142  CALL_FUNCTION_1       1  ''
              144  CALL_METHOD_1         1  ''
              146  BINARY_MODULO    
              148  STORE_FAST               'standardMsg'
            150_0  COME_FROM           124  '124'

 L.1153       150  LOAD_FAST                'mismatched'
              152  POP_JUMP_IF_FALSE   184  'to 184'

 L.1154       154  LOAD_FAST                'standardMsg'
              156  POP_JUMP_IF_FALSE   166  'to 166'

 L.1155       158  LOAD_FAST                'standardMsg'
              160  LOAD_STR                 '; '
              162  INPLACE_ADD      
              164  STORE_FAST               'standardMsg'
            166_0  COME_FROM           156  '156'

 L.1156       166  LOAD_FAST                'standardMsg'
              168  LOAD_STR                 'Mismatched values: %s'
              170  LOAD_STR                 ','
              172  LOAD_METHOD              join
              174  LOAD_FAST                'mismatched'
              176  CALL_METHOD_1         1  ''
              178  BINARY_MODULO    
              180  INPLACE_ADD      
              182  STORE_FAST               'standardMsg'
            184_0  COME_FROM           152  '152'

 L.1158       184  LOAD_FAST                'self'
              186  LOAD_METHOD              fail
              188  LOAD_FAST                'self'
              190  LOAD_METHOD              _formatMessage
              192  LOAD_FAST                'msg'
              194  LOAD_FAST                'standardMsg'
              196  CALL_METHOD_2         2  ''
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

Parse error at or near `<118>' instruction at offset 40

    def assertCountEqual--- This code section failed: ---

 L.1173         0  LOAD_GLOBAL              list
                2  LOAD_FAST                'first'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              list
                8  LOAD_FAST                'second'
               10  CALL_FUNCTION_1       1  ''
               12  ROT_TWO          
               14  STORE_FAST               'first_seq'
               16  STORE_FAST               'second_seq'

 L.1174        18  SETUP_FINALLY        44  'to 44'

 L.1175        20  LOAD_GLOBAL              collections
               22  LOAD_METHOD              Counter
               24  LOAD_FAST                'first_seq'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'first'

 L.1176        30  LOAD_GLOBAL              collections
               32  LOAD_METHOD              Counter
               34  LOAD_FAST                'second_seq'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'second'
               40  POP_BLOCK        
               42  JUMP_FORWARD         72  'to 72'
             44_0  COME_FROM_FINALLY    18  '18'

 L.1177        44  DUP_TOP          
               46  LOAD_GLOBAL              TypeError
               48  <121>                70  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.1179        56  LOAD_GLOBAL              _count_diff_all_purpose
               58  LOAD_FAST                'first_seq'
               60  LOAD_FAST                'second_seq'
               62  CALL_FUNCTION_2       2  ''
               64  STORE_FAST               'differences'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         94  'to 94'
               70  <48>             
             72_0  COME_FROM            42  '42'

 L.1181        72  LOAD_FAST                'first'
               74  LOAD_FAST                'second'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    84  'to 84'

 L.1182        80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'

 L.1183        84  LOAD_GLOBAL              _count_diff_hashable
               86  LOAD_FAST                'first_seq'
               88  LOAD_FAST                'second_seq'
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'differences'
             94_0  COME_FROM            68  '68'

 L.1185        94  LOAD_FAST                'differences'
               96  POP_JUMP_IF_FALSE   160  'to 160'

 L.1186        98  LOAD_STR                 'Element counts were not equal:\n'
              100  STORE_FAST               'standardMsg'

 L.1187       102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'TestCase.assertCountEqual.<locals>.<listcomp>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  LOAD_FAST                'differences'
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'lines'

 L.1188       116  LOAD_STR                 '\n'
              118  LOAD_METHOD              join
              120  LOAD_FAST                'lines'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'diffMsg'

 L.1189       126  LOAD_FAST                'self'
              128  LOAD_METHOD              _truncateMessage
              130  LOAD_FAST                'standardMsg'
              132  LOAD_FAST                'diffMsg'
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'standardMsg'

 L.1190       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _formatMessage
              142  LOAD_FAST                'msg'
              144  LOAD_FAST                'standardMsg'
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'msg'

 L.1191       150  LOAD_FAST                'self'
              152  LOAD_METHOD              fail
              154  LOAD_FAST                'msg'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
            160_0  COME_FROM            96  '96'

Parse error at or near `<121>' instruction at offset 48

    def assertMultiLineEqual(self, first, second, msg=None):
        """Assert that two multi-line strings are equal."""
        self.assertIsInstancefirststr'First argument is not a string'
        self.assertIsInstancesecondstr'Second argument is not a string'
        if first != second:
            if len(first) > self._diffThreshold or (len(second) > self._diffThreshold):
                self._baseAssertEqualfirstsecondmsg
            firstlines = first.splitlines(keepends=True)
            secondlines = second.splitlines(keepends=True)
            if len(firstlines) == 1:
                if first.strip'\r\n' == first:
                    firstlines = [
                     first + '\n']
                    secondlines = [second + '\n']
            standardMsg = '%s != %s' % _common_shorten_repr(first, second)
            diff = '\n' + ''.joindifflib.ndiff(firstlines, secondlines)
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.failself._formatMessage(msg, standardMsg)

    def assertLess(self, a, b, msg=None):
        """Just like self.assertTrue(a < b), but with a nicer default message."""
        if not a < b:
            standardMsg = '%s not less than %s' % (safe_repr(a), safe_repr(b))
            self.failself._formatMessage(msg, standardMsg)

    def assertLessEqual(self, a, b, msg=None):
        """Just like self.assertTrue(a <= b), but with a nicer default message."""
        if not a <= b:
            standardMsg = '%s not less than or equal to %s' % (safe_repr(a), safe_repr(b))
            self.failself._formatMessage(msg, standardMsg)

    def assertGreater(self, a, b, msg=None):
        """Just like self.assertTrue(a > b), but with a nicer default message."""
        if not a > b:
            standardMsg = '%s not greater than %s' % (safe_repr(a), safe_repr(b))
            self.failself._formatMessage(msg, standardMsg)

    def assertGreaterEqual(self, a, b, msg=None):
        """Just like self.assertTrue(a >= b), but with a nicer default message."""
        if not a >= b:
            standardMsg = '%s not greater than or equal to %s' % (safe_repr(a), safe_repr(b))
            self.failself._formatMessage(msg, standardMsg)

    def assertIsNone--- This code section failed: ---

 L.1239         0  LOAD_FAST                'obj'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    40  'to 40'

 L.1240         8  LOAD_STR                 '%s is not None'
               10  LOAD_GLOBAL              safe_repr
               12  LOAD_FAST                'obj'
               14  CALL_FUNCTION_1       1  ''
               16  BUILD_TUPLE_1         1 
               18  BINARY_MODULO    
               20  STORE_FAST               'standardMsg'

 L.1241        22  LOAD_FAST                'self'
               24  LOAD_METHOD              fail
               26  LOAD_FAST                'self'
               28  LOAD_METHOD              _formatMessage
               30  LOAD_FAST                'msg'
               32  LOAD_FAST                'standardMsg'
               34  CALL_METHOD_2         2  ''
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
             40_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertIsNotNone--- This code section failed: ---

 L.1245         0  LOAD_FAST                'obj'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L.1246         8  LOAD_STR                 'unexpectedly None'
               10  STORE_FAST               'standardMsg'

 L.1247        12  LOAD_FAST                'self'
               14  LOAD_METHOD              fail
               16  LOAD_FAST                'self'
               18  LOAD_METHOD              _formatMessage
               20  LOAD_FAST                'msg'
               22  LOAD_FAST                'standardMsg'
               24  CALL_METHOD_2         2  ''
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def assertIsInstance(self, obj, cls, msg=None):
        """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
        default message."""
        if not isinstance(obj, cls):
            standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
            self.failself._formatMessage(msg, standardMsg)

    def assertNotIsInstance(self, obj, cls, msg=None):
        """Included for symmetry with assertIsInstance."""
        if isinstance(obj, cls):
            standardMsg = '%s is an instance of %r' % (safe_repr(obj), cls)
            self.failself._formatMessage(msg, standardMsg)

    def assertRaisesRegex(self, expected_exception, expected_regex, *args, **kwargs):
        """Asserts that the message in a raised exception matches a regex.

        Args:
            expected_exception: Exception class expected to be raised.
            expected_regex: Regex (re.Pattern object or string) expected
                    to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                    when assertRaisesRegex is used as a context manager.
        """
        context = _AssertRaisesContext(expected_exception, self, expected_regex)
        return context.handle'assertRaisesRegex'argskwargs

    def assertWarnsRegex(self, expected_warning, expected_regex, *args, **kwargs):
        """Asserts that the message in a triggered warning matches a regexp.
        Basic functioning is similar to assertWarns() with the addition
        that only warnings whose messages also match the regular expression
        are considered successful matches.

        Args:
            expected_warning: Warning class expected to be triggered.
            expected_regex: Regex (re.Pattern object or string) expected
                    to be found in error message.
            args: Function to be called and extra positional args.
            kwargs: Extra kwargs.
            msg: Optional message used in case of failure. Can only be used
                    when assertWarnsRegex is used as a context manager.
        """
        context = _AssertWarnsContext(expected_warning, self, expected_regex)
        return context.handle'assertWarnsRegex'argskwargs

    def assertRegex--- This code section failed: ---

 L.1299         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'expected_regex'
                4  LOAD_GLOBAL              str
                6  LOAD_GLOBAL              bytes
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    36  'to 36'

 L.1300        14  LOAD_FAST                'expected_regex'
               16  POP_JUMP_IF_TRUE     26  'to 26'
               18  <74>             
               20  LOAD_STR                 'expected_regex must not be empty.'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L.1301        26  LOAD_GLOBAL              re
               28  LOAD_METHOD              compile
               30  LOAD_FAST                'expected_regex'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'expected_regex'
             36_0  COME_FROM            12  '12'

 L.1302        36  LOAD_FAST                'expected_regex'
               38  LOAD_METHOD              search
               40  LOAD_FAST                'text'
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_TRUE     82  'to 82'

 L.1303        46  LOAD_STR                 "Regex didn't match: %r not found in %r"

 L.1304        48  LOAD_FAST                'expected_regex'
               50  LOAD_ATTR                pattern
               52  LOAD_FAST                'text'

 L.1303        54  BUILD_TUPLE_2         2 
               56  BINARY_MODULO    
               58  STORE_FAST               'standardMsg'

 L.1306        60  LOAD_FAST                'self'
               62  LOAD_METHOD              _formatMessage
               64  LOAD_FAST                'msg'
               66  LOAD_FAST                'standardMsg'
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'msg'

 L.1307        72  LOAD_FAST                'self'
               74  LOAD_METHOD              failureException
               76  LOAD_FAST                'msg'
               78  CALL_METHOD_1         1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            44  '44'

Parse error at or near `<74>' instruction at offset 18

    def assertNotRegex(self, text, unexpected_regex, msg=None):
        """Fail the test if the text matches the regular expression."""
        if isinstance(unexpected_regex, (str, bytes)):
            unexpected_regex = re.compileunexpected_regex
        match = unexpected_regex.searchtext
        if match:
            standardMsg = 'Regex matched: %r matches %r in %r' % (
             text[match.start:match.end],
             unexpected_regex.pattern,
             text)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureExceptionmsg

    def _deprecate(original_func):

        def deprecated_func--- This code section failed: ---

 L.1326         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn

 L.1327         4  LOAD_STR                 'Please use {0} instead.'
                6  LOAD_METHOD              format
                8  LOAD_DEREF               'original_func'
               10  LOAD_ATTR                __name__
               12  CALL_METHOD_1         1  ''

 L.1328        14  LOAD_GLOBAL              DeprecationWarning
               16  LOAD_CONST               2

 L.1326        18  CALL_METHOD_3         3  ''
               20  POP_TOP          

 L.1329        22  LOAD_DEREF               'original_func'
               24  LOAD_FAST                'args'
               26  BUILD_MAP_0           0 
               28  LOAD_FAST                'kwargs'
               30  <164>                 1  ''
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 30

        return deprecated_func

    failUnlessEqual = assertEquals = _deprecate(assertEqual)
    failIfEqual = assertNotEquals = _deprecate(assertNotEqual)
    failUnlessAlmostEqual = assertAlmostEquals = _deprecate(assertAlmostEqual)
    failIfAlmostEqual = assertNotAlmostEquals = _deprecate(assertNotAlmostEqual)
    failUnless = assert_ = _deprecate(assertTrue)
    failUnlessRaises = _deprecate(assertRaises)
    failIf = _deprecate(assertFalse)
    assertRaisesRegexp = _deprecate(assertRaisesRegex)
    assertRegexpMatches = _deprecate(assertRegex)
    assertNotRegexpMatches = _deprecate(assertNotRegex)


class FunctionTestCase(TestCase):
    __doc__ = "A test case that wraps a test function.\n\n    This is useful for slipping pre-existing test functions into the\n    unittest framework. Optionally, set-up and tidy-up functions can be\n    supplied. As with TestCase, the tidy-up ('tearDown') function will\n    always be called if the set-up ('setUp') function ran successfully.\n    "

    def __init__(self, testFunc, setUp=None, tearDown=None, description=None):
        super(FunctionTestCase, self).__init__
        self._setUpFunc = setUp
        self._tearDownFunc = tearDown
        self._testFunc = testFunc
        self._description = description

    def setUp--- This code section failed: ---

 L.1363         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _setUpFunc
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1364        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _setUpFunc
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def tearDown--- This code section failed: ---

 L.1367         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _tearDownFunc
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.1368        10  LOAD_FAST                'self'
               12  LOAD_METHOD              _tearDownFunc
               14  CALL_METHOD_0         0  ''
               16  POP_TOP          
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def runTest(self):
        self._testFunc

    def id(self):
        return self._testFunc.__name__

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._setUpFunc == other._setUpFunc and self._tearDownFunc == other._tearDownFunc and self._testFunc == other._testFunc and self._description == other._description

    def __hash__(self):
        return hash((type(self), self._setUpFunc, self._tearDownFunc,
         self._testFunc, self._description))

    def __str__(self):
        return '%s (%s)' % (strclass(self.__class__),
         self._testFunc.__name__)

    def __repr__(self):
        return '<%s tec=%s>' % (strclass(self.__class__),
         self._testFunc)

    def shortDescription--- This code section failed: ---

 L.1398         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _description
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L.1399        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _description
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L.1400        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _testFunc
               20  LOAD_ATTR                __doc__
               22  STORE_FAST               'doc'

 L.1401        24  LOAD_FAST                'doc'
               26  POP_JUMP_IF_FALSE    46  'to 46'
               28  LOAD_FAST                'doc'
               30  LOAD_METHOD              split
               32  LOAD_STR                 '\n'
               34  CALL_METHOD_1         1  ''
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              strip
               42  CALL_METHOD_0         0  ''
               44  JUMP_IF_TRUE_OR_POP    48  'to 48'
             46_0  COME_FROM            26  '26'
               46  LOAD_CONST               None
             48_0  COME_FROM            44  '44'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class _SubTest(TestCase):

    def __init__(self, test_case, message, params):
        super().__init__
        self._message = message
        self.test_case = test_case
        self.params = params
        self.failureException = test_case.failureException

    def runTest(self):
        raise NotImplementedError('subtests cannot be run directly')

    def _subDescription--- This code section failed: ---

 L.1417         0  BUILD_LIST_0          0 
                2  STORE_FAST               'parts'

 L.1418         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _message
                8  LOAD_GLOBAL              _subtest_msg_sentinel
               10  <117>                 1  ''
               12  POP_JUMP_IF_FALSE    32  'to 32'

 L.1419        14  LOAD_FAST                'parts'
               16  LOAD_METHOD              append
               18  LOAD_STR                 '[{}]'
               20  LOAD_METHOD              format
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _message
               26  CALL_METHOD_1         1  ''
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
             32_0  COME_FROM            12  '12'

 L.1420        32  LOAD_FAST                'self'
               34  LOAD_ATTR                params
               36  POP_JUMP_IF_FALSE    80  'to 80'

 L.1421        38  LOAD_STR                 ', '
               40  LOAD_METHOD              join
               42  LOAD_GENEXPR             '<code_object <genexpr>>'
               44  LOAD_STR                 '_SubTest._subDescription.<locals>.<genexpr>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.1423        48  LOAD_FAST                'self'
               50  LOAD_ATTR                params
               52  LOAD_METHOD              items
               54  CALL_METHOD_0         0  ''

 L.1421        56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'params_desc'

 L.1424        64  LOAD_FAST                'parts'
               66  LOAD_METHOD              append
               68  LOAD_STR                 '({})'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'params_desc'
               74  CALL_METHOD_1         1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            36  '36'

 L.1425        80  LOAD_STR                 ' '
               82  LOAD_METHOD              join
               84  LOAD_FAST                'parts'
               86  CALL_METHOD_1         1  ''
               88  JUMP_IF_TRUE_OR_POP    92  'to 92'
               90  LOAD_STR                 '(<subtest>)'
             92_0  COME_FROM            88  '88'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def id(self):
        return '{} {}'.format(self.test_case.id, self._subDescription)

    def shortDescription(self):
        """Returns a one-line description of the subtest, or None if no
        description has been provided.
        """
        return self.test_case.shortDescription

    def __str__(self):
        return '{} {}'.format(self.test_case, self._subDescription)