# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: unittest\case.py
"""Test case implementation"""
import sys, functools, difflib, logging, pprint, re, warnings, collections, contextlib, traceback, types
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
    def testPartExecutor(self, test_case, isTest=False):
        old_success = self.success
        self.success = True
        try:
            try:
                yield
            except KeyboardInterrupt:
                raise
            except SkipTest as e:
                try:
                    self.success = False
                    self.skipped.append((test_case, str(e)))
                finally:
                    e = None
                    del e

            except _ShouldStop:
                pass
            except:
                exc_info = sys.exc_info()
                if self.expecting_failure:
                    self.expectedFailure = exc_info
                else:
                    self.success = False
                    self.errors.append((test_case, exc_info))
                exc_info = None
            else:
                if self.result_supports_subtests:
                    if self.success:
                        self.errors.append((test_case, None))
        finally:
            self.success = self.success and old_success


def _id(obj):
    return obj


_module_cleanups = []

def addModuleCleanup(function, *args, **kwargs):
    """Same as addCleanup, except the cleanup items are called even if
    setUpModule fails (unlike tearDownModule)."""
    _module_cleanups.append((function, args, kwargs))


def doModuleCleanups():
    """Execute all module cleanup functions. Normally called for you after
    tearDownModule."""
    exceptions = []
    while _module_cleanups:
        function, args, kwargs = _module_cleanups.pop()
        try:
            function(*args, **kwargs)
        except Exception as exc:
            try:
                exceptions.append(exc)
            finally:
                exc = None
                del exc

    if exceptions:
        raise exceptions[0]


def skip(reason):
    """
    Unconditionally skip a test.
    """

    def decorator(test_item):
        if not isinstance(test_item, type):

            @functools.wraps(test_item)
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
        raise self.test_case.failureException(msg)


class _AssertRaisesBaseContext(_BaseTestCaseContext):

    def __init__(self, expected, test_case, expected_regex=None):
        _BaseTestCaseContext.__init__(self, test_case)
        self.expected = expected
        self.test_case = test_case
        if expected_regex is not None:
            expected_regex = re.compile(expected_regex)
        self.expected_regex = expected_regex
        self.obj_name = None
        self.msg = None

    def handle--- This code section failed: ---

 L. 185         0  SETUP_FINALLY       168  'to 168'

 L. 186         2  LOAD_GLOBAL              _is_subtype
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                expected
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _base_type
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     34  'to 34'

 L. 187        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 '%s() arg 1 must be %s'

 L. 188        20  LOAD_FAST                'name'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _base_type_str
               26  BUILD_TUPLE_2         2 

 L. 187        28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            14  '14'

 L. 189        34  LOAD_FAST                'args'
               36  POP_JUMP_IF_TRUE     86  'to 86'

 L. 190        38  LOAD_FAST                'kwargs'
               40  LOAD_METHOD              pop
               42  LOAD_STR                 'msg'
               44  LOAD_CONST               None
               46  CALL_METHOD_2         2  ''
               48  LOAD_FAST                'self'
               50  STORE_ATTR               msg

 L. 191        52  LOAD_FAST                'kwargs'
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L. 192        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 '%r is an invalid keyword argument for this function'

 L. 193        60  LOAD_GLOBAL              next
               62  LOAD_GLOBAL              iter
               64  LOAD_FAST                'kwargs'
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_1         1 

 L. 192        72  BINARY_MODULO    
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            54  '54'

 L. 194        78  LOAD_FAST                'self'
               80  POP_BLOCK        
               82  CALL_FINALLY        168  'to 168'
               84  RETURN_VALUE     
             86_0  COME_FROM            36  '36'

 L. 196        86  LOAD_FAST                'args'
               88  UNPACK_EX_1+0           
               90  STORE_FAST               'callable_obj'
               92  STORE_FAST               'args'

 L. 197        94  SETUP_FINALLY       108  'to 108'

 L. 198        96  LOAD_FAST                'callable_obj'
               98  LOAD_ATTR                __name__
              100  LOAD_FAST                'self'
              102  STORE_ATTR               obj_name
              104  POP_BLOCK        
              106  JUMP_FORWARD        138  'to 138'
            108_0  COME_FROM_FINALLY    94  '94'

 L. 199       108  DUP_TOP          
              110  LOAD_GLOBAL              AttributeError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   136  'to 136'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 200       122  LOAD_GLOBAL              str
              124  LOAD_FAST                'callable_obj'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_FAST                'self'
              130  STORE_ATTR               obj_name
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           114  '114'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM           106  '106'

 L. 201       138  LOAD_FAST                'self'
              140  SETUP_WITH          158  'to 158'
              142  POP_TOP          

 L. 202       144  LOAD_FAST                'callable_obj'
              146  LOAD_FAST                'args'
              148  LOAD_FAST                'kwargs'
              150  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              152  POP_TOP          
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM_WITH      140  '140'
              158  WITH_CLEANUP_START
              160  WITH_CLEANUP_FINISH
              162  END_FINALLY      
              164  POP_BLOCK        
              166  BEGIN_FINALLY    
            168_0  COME_FROM            82  '82'
            168_1  COME_FROM_FINALLY     0  '0'

 L. 205       168  LOAD_CONST               None
              170  STORE_FAST               'self'
              172  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 82


class _AssertRaisesContext(_AssertRaisesBaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertRaises* methods.'
    _base_type = BaseException
    _base_type_str = 'an exception type or tuple of exception types'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            try:
                exc_name = self.expected.__name__
            except AttributeError:
                exc_name = str(self.expected)

            if self.obj_name:
                self._raiseFailure('{} not raised by {}'.format(exc_name, self.obj_name))
            else:
                self._raiseFailure('{} not raised'.format(exc_name))
        else:
            traceback.clear_frames(tb)
        if not issubclass(exc_type, self.expected):
            return False
        self.exception = exc_value.with_traceback(None)
        if self.expected_regex is None:
            return True
        expected_regex = self.expected_regex
        if not expected_regex.search(str(exc_value)):
            self._raiseFailure('"{}" does not match "{}"'.format(expected_regex.pattern, str(exc_value)))
        return True


class _AssertWarnsContext(_AssertRaisesBaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertWarns* methods.'
    _base_type = Warning
    _base_type_str = 'a warning type or tuple of warning types'

    def __enter__(self):
        for v in list(sys.modules.values()):
            if getattr(v, '__warningregistry__', None):
                v.__warningregistry__ = {}
            self.warnings_manager = warnings.catch_warnings(record=True)
            self.warnings = self.warnings_manager.__enter__()
            warnings.simplefilter('always', self.expected)
            return self

    def __exit__(self, exc_type, exc_value, tb):
        self.warnings_manager.__exit__(exc_type, exc_value, tb)
        if exc_type is not None:
            return
        try:
            exc_name = self.expected.__name__
        except AttributeError:
            exc_name = str(self.expected)
        else:
            first_matching = None
        for m in self.warnings:
            w = m.message
            if not isinstance(w, self.expected):
                pass
            else:
                if first_matching is None:
                    first_matching = w
                if self.expected_regex is not None and not self.expected_regex.search(str(w)):
                    pass
                else:
                    self.warning = w
                    self.filename = m.filename
                    self.lineno = m.lineno
                    return None
                    if first_matching is not None:
                        self._raiseFailure('"{}" does not match "{}"'.format(self.expected_regex.pattern, str(first_matching)))
                    elif self.obj_name:
                        self._raiseFailure('{} not triggered by {}'.format(exc_name, self.obj_name))
                    else:
                        self._raiseFailure('{} not triggered'.format(exc_name))


_LoggingWatcher = collections.namedtuple('_LoggingWatcher', [
 'records', 'output'])

class _CapturingHandler(logging.Handler):
    __doc__ = '\n    A logging handler capturing all (raw and formatted) logging output.\n    '

    def __init__(self):
        logging.Handler.__init__(self)
        self.watcher = _LoggingWatcher([], [])

    def flush(self):
        pass

    def emit(self, record):
        self.watcher.records.append(record)
        msg = self.format(record)
        self.watcher.output.append(msg)


class _AssertLogsContext(_BaseTestCaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertLogs().'
    LOGGING_FORMAT = '%(levelname)s:%(name)s:%(message)s'

    def __init__(self, test_case, logger_name, level):
        _BaseTestCaseContext.__init__(self, test_case)
        self.logger_name = logger_name
        if level:
            self.level = logging._nameToLevel.get(level, level)
        else:
            self.level = logging.INFO
        self.msg = None

    def __enter__(self):
        if isinstance(self.logger_name, logging.Logger):
            logger = self.logger = self.logger_name
        else:
            logger = self.logger = logging.getLogger(self.logger_name)
        formatter = logging.Formatter(self.LOGGING_FORMAT)
        handler = _CapturingHandler()
        handler.setFormatter(formatter)
        self.watcher = handler.watcher
        self.old_handlers = logger.handlers[:]
        self.old_level = logger.level
        self.old_propagate = logger.propagate
        logger.handlers = [handler]
        logger.setLevel(self.level)
        logger.propagate = False
        return handler.watcher

    def __exit__(self, exc_type, exc_value, tb):
        self.logger.handlers = self.old_handlers
        self.logger.propagate = self.old_propagate
        self.logger.setLevel(self.old_level)
        if exc_type is not None:
            return False
        if len(self.watcher.records) == 0:
            self._raiseFailure('no logs of level {} or higher triggered on {}'.format(logging.getLevelName(self.level), self.logger.name))


class _OrderedChainMap(collections.ChainMap):

    def __iter__(self):
        seen = set()
        for mapping in self.maps:
            for k in mapping:
                if k not in seen:
                    seen.add(k)
                    (yield k)


class TestCase(object):
    __doc__ = "A class whose instances are single test cases.\n\n    By default, the test code itself should be placed in a method named\n    'runTest'.\n\n    If the fixture may be used for many test cases, create as\n    many test methods as are needed. When instantiating such a TestCase\n    subclass, specify in the constructor arguments the name of the test method\n    that the instance is to execute.\n\n    Test authors should subclass TestCase for their own tests. Construction\n    and deconstruction of the test's environment ('fixture') can be\n    implemented by overriding the 'setUp' and 'tearDown' methods respectively.\n\n    If it is necessary to override the __init__ method, the base class\n    __init__ method must always be called. It is important that subclasses\n    should not change the signature of their __init__ method, since instances\n    of the classes are instantiated automatically by parts of the framework\n    in order to be run.\n\n    When subclassing TestCase, you can set these attributes:\n    * failureException: determines which exception will be raised when\n        the instance's assertion methods fail; test methods raising this\n        exception will be deemed to have 'failed' rather than 'errored'.\n    * longMessage: determines whether long messages (including repr of\n        objects used in assert methods) will be printed on failure in *addition*\n        to any explicit message passed.\n    * maxDiff: sets the maximum length of a diff in failure messages\n        by assert methods using difflib. It is looked up as an instance\n        attribute so can be configured by individual tests if required.\n    "
    failureException = AssertionError
    longMessage = True
    maxDiff = 640
    _diffThreshold = 65536
    _classSetupFailed = False
    _class_cleanups = []

    def __init__(self, methodName='runTest'):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        self._testMethodName = methodName
        self._outcome = None
        self._testMethodDoc = 'No test'
        try:
            testMethod = getattr(self, methodName)
        except AttributeError:
            if methodName != 'runTest':
                raise ValueError('no such test method in %s: %s' % (
                 self.__class__, methodName))
        else:
            self._testMethodDoc = testMethod.__doc__
        self._cleanups = []
        self._subtest = None
        self._type_equality_funcs = {}
        self.addTypeEqualityFunc(dict, 'assertDictEqual')
        self.addTypeEqualityFunc(list, 'assertListEqual')
        self.addTypeEqualityFunc(tuple, 'assertTupleEqual')
        self.addTypeEqualityFunc(set, 'assertSetEqual')
        self.addTypeEqualityFunc(frozenset, 'assertSetEqual')
        self.addTypeEqualityFunc(str, 'assertMultiLineEqual')

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

    def addCleanup(*args, **kwargs):
        """Add a function, with arguments, to be called when the test is
        completed. Functions added are called on a LIFO basis and are
        called after tearDown on test failure or success.

        Cleanup items are called even if setUp fails (unlike tearDown)."""
        if len(args) >= 2:
            self, function, *args = args
        else:
            if not args:
                raise TypeError("descriptor 'addCleanup' of 'TestCase' object needs an argument")
            else:
                if 'function' in kwargs:
                    function = kwargs.pop('function')
                    self, *args = args
                    import warnings
                    warnings.warn("Passing 'function' as keyword argument is deprecated", DeprecationWarning,
                      stacklevel=2)
                else:
                    raise TypeError('addCleanup expected at least 1 positional argument, got %d' % (len(args) - 1))
        args = tuple(args)
        self._cleanups.append((function, args, kwargs))

    addCleanup.__text_signature__ = '($self, function, /, *args, **kwargs)'

    @classmethod
    def addClassCleanup(cls, function, *args, **kwargs):
        """Same as addCleanup, except the cleanup items are called even if
        setUpClass fails (unlike tearDownClass)."""
        cls._class_cleanups.append((function, args, kwargs))

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
        return result.TestResult()

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        doc = self._testMethodDoc
        if doc:
            return doc.strip().split('\n')[0].strip()

    def id(self):
        return '%s.%s' % (strclass(self.__class__), self._testMethodName)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self._testMethodName == other._testMethodName

    def __hash__(self):
        return hash((type(self), self._testMethodName))

    def __str__(self):
        return '%s (%s)' % (self._testMethodName, strclass(self.__class__))

    def __repr__(self):
        return '<%s testMethod=%s>' % (
         strclass(self.__class__), self._testMethodName)

    def _addSkip(self, result, test_case, reason):
        addSkip = getattr(result, 'addSkip', None)
        if addSkip is not None:
            addSkip(test_case, reason)
        else:
            warnings.warn('TestResult has no addSkip method, skips not reported', RuntimeWarning, 2)
            result.addSuccess(test_case)

    @contextlib.contextmanager
    def subTest(self, msg=_subtest_msg_sentinel, **params):
        """Return a context manager that will return the enclosed block
        of code in a subtest identified by the optional message and
        keyword parameters.  A failure in the subtest marks the test
        case as failed but resumes execution at the end of the enclosed
        block, allowing further test code to be executed.
        """
        if not self._outcome is None:
            self._outcome.result_supports_subtests or (yield)
            return
        else:
            parent = self._subtest
            if parent is None:
                params_map = _OrderedChainMap(params)
            else:
                params_map = parent.params.new_child(params)
        self._subtest = _SubTest(self, msg, params_map)
        try:
            with self._outcome.testPartExecutor((self._subtest), isTest=True):
                (yield)
            result = self._outcome.success or self._outcome.result
            if result is not None:
                if result.failfast:
                    raise _ShouldStop
                else:
                    if self._outcome.expectedFailure:
                        raise _ShouldStop
        finally:
            self._subtest = parent

    def _feedErrorsToResult(self, result, errors):
        for test, exc_info in errors:
            if isinstance(test, _SubTest):
                result.addSubTest(test.test_case, test, exc_info)
            elif exc_info is not None:
                if issubclass(exc_info[0], self.failureException):
                    result.addFailure(test, exc_info)
                else:
                    result.addError(test, exc_info)

    def _addExpectedFailure(self, result, exc_info):
        try:
            addExpectedFailure = result.addExpectedFailure
        except AttributeError:
            warnings.warn('TestResult has no addExpectedFailure method, reporting as passes', RuntimeWarning)
            result.addSuccess(self)
        else:
            addExpectedFailure(self, exc_info)

    def _addUnexpectedSuccess(self, result):
        try:
            addUnexpectedSuccess = result.addUnexpectedSuccess
        except AttributeError:
            warnings.warn('TestResult has no addUnexpectedSuccess method, reporting as failure', RuntimeWarning)
            try:
                raise _UnexpectedSuccess from None
            except _UnexpectedSuccess:
                result.addFailure(self, sys.exc_info())

        else:
            addUnexpectedSuccess(self)

    def _callSetUp(self):
        self.setUp()

    def _callTestMethod(self, method):
        method()

    def _callTearDown(self):
        self.tearDown()

    def _callCleanup(self, function, *args, **kwargs):
        function(*args, **kwargs)

    def run--- This code section failed: ---

 L. 642         0  LOAD_FAST                'result'
                2  STORE_FAST               'orig_result'

 L. 643         4  LOAD_FAST                'result'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    46  'to 46'

 L. 644        12  LOAD_FAST                'self'
               14  LOAD_METHOD              defaultTestResult
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'result'

 L. 645        20  LOAD_GLOBAL              getattr
               22  LOAD_FAST                'result'
               24  LOAD_STR                 'startTestRun'
               26  LOAD_CONST               None
               28  CALL_FUNCTION_3       3  ''
               30  STORE_FAST               'startTestRun'

 L. 646        32  LOAD_FAST                'startTestRun'
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 647        40  LOAD_FAST                'startTestRun'
               42  CALL_FUNCTION_0       0  ''
               44  POP_TOP          
             46_0  COME_FROM            38  '38'
             46_1  COME_FROM            10  '10'

 L. 649        46  LOAD_FAST                'result'
               48  LOAD_METHOD              startTest
               50  LOAD_FAST                'self'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 651        56  LOAD_GLOBAL              getattr
               58  LOAD_FAST                'self'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _testMethodName
               64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'testMethod'

 L. 652        68  LOAD_GLOBAL              getattr
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                __class__
               74  LOAD_STR                 '__unittest_skip__'
               76  LOAD_CONST               False
               78  CALL_FUNCTION_3       3  ''
               80  POP_JUMP_IF_TRUE     94  'to 94'

 L. 653        82  LOAD_GLOBAL              getattr
               84  LOAD_FAST                'testMethod'
               86  LOAD_STR                 '__unittest_skip__'
               88  LOAD_CONST               False
               90  CALL_FUNCTION_3       3  ''

 L. 652        92  POP_JUMP_IF_FALSE   156  'to 156'
             94_0  COME_FROM            80  '80'

 L. 655        94  SETUP_FINALLY       140  'to 140'

 L. 656        96  LOAD_GLOBAL              getattr
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                __class__
              102  LOAD_STR                 '__unittest_skip_why__'
              104  LOAD_STR                 ''
              106  CALL_FUNCTION_3       3  ''
              108  JUMP_IF_TRUE_OR_POP   120  'to 120'

 L. 657       110  LOAD_GLOBAL              getattr
              112  LOAD_FAST                'testMethod'
              114  LOAD_STR                 '__unittest_skip_why__'
              116  LOAD_STR                 ''
              118  CALL_FUNCTION_3       3  ''
            120_0  COME_FROM           108  '108'

 L. 656       120  STORE_FAST               'skip_why'

 L. 658       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _addSkip
              126  LOAD_FAST                'result'
              128  LOAD_FAST                'self'
              130  LOAD_FAST                'skip_why'
              132  CALL_METHOD_3         3  ''
              134  POP_TOP          
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM_FINALLY    94  '94'

 L. 660       140  LOAD_FAST                'result'
              142  LOAD_METHOD              stopTest
              144  LOAD_FAST                'self'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  END_FINALLY      

 L. 661       152  LOAD_CONST               None
              154  RETURN_VALUE     
            156_0  COME_FROM            92  '92'

 L. 662       156  LOAD_GLOBAL              getattr
              158  LOAD_FAST                'testMethod'

 L. 663       160  LOAD_STR                 '__unittest_expecting_failure__'

 L. 663       162  LOAD_CONST               False

 L. 662       164  CALL_FUNCTION_3       3  ''
              166  STORE_FAST               'expecting_failure_method'

 L. 664       168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'self'

 L. 665       172  LOAD_STR                 '__unittest_expecting_failure__'

 L. 665       174  LOAD_CONST               False

 L. 664       176  CALL_FUNCTION_3       3  ''
              178  STORE_FAST               'expecting_failure_class'

 L. 666       180  LOAD_FAST                'expecting_failure_class'
              182  JUMP_IF_TRUE_OR_POP   186  'to 186'
              184  LOAD_FAST                'expecting_failure_method'
            186_0  COME_FROM           182  '182'
              186  STORE_FAST               'expecting_failure'

 L. 667       188  LOAD_GLOBAL              _Outcome
              190  LOAD_FAST                'result'
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'outcome'

 L. 668       196  SETUP_FINALLY       442  'to 442'

 L. 669       198  LOAD_FAST                'outcome'
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _outcome

 L. 671       204  LOAD_FAST                'outcome'
              206  LOAD_METHOD              testPartExecutor
              208  LOAD_FAST                'self'
              210  CALL_METHOD_1         1  ''
              212  SETUP_WITH          228  'to 228'
              214  POP_TOP          

 L. 672       216  LOAD_FAST                'self'
              218  LOAD_METHOD              _callSetUp
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_WITH      212  '212'
              228  WITH_CLEANUP_START
              230  WITH_CLEANUP_FINISH
              232  END_FINALLY      

 L. 673       234  LOAD_FAST                'outcome'
              236  LOAD_ATTR                success
          238_240  POP_JUMP_IF_FALSE   320  'to 320'

 L. 674       242  LOAD_FAST                'expecting_failure'
              244  LOAD_FAST                'outcome'
              246  STORE_ATTR               expecting_failure

 L. 675       248  LOAD_FAST                'outcome'
              250  LOAD_ATTR                testPartExecutor
              252  LOAD_FAST                'self'
              254  LOAD_CONST               True
              256  LOAD_CONST               ('isTest',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  SETUP_WITH          278  'to 278'
              262  POP_TOP          

 L. 676       264  LOAD_FAST                'self'
              266  LOAD_METHOD              _callTestMethod
              268  LOAD_FAST                'testMethod'
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          
              274  POP_BLOCK        
              276  BEGIN_FINALLY    
            278_0  COME_FROM_WITH      260  '260'
              278  WITH_CLEANUP_START
              280  WITH_CLEANUP_FINISH
              282  END_FINALLY      

 L. 677       284  LOAD_CONST               False
              286  LOAD_FAST                'outcome'
              288  STORE_ATTR               expecting_failure

 L. 678       290  LOAD_FAST                'outcome'
              292  LOAD_METHOD              testPartExecutor
              294  LOAD_FAST                'self'
              296  CALL_METHOD_1         1  ''
              298  SETUP_WITH          314  'to 314'
              300  POP_TOP          

 L. 679       302  LOAD_FAST                'self'
              304  LOAD_METHOD              _callTearDown
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          
              310  POP_BLOCK        
              312  BEGIN_FINALLY    
            314_0  COME_FROM_WITH      298  '298'
              314  WITH_CLEANUP_START
              316  WITH_CLEANUP_FINISH
              318  END_FINALLY      
            320_0  COME_FROM           238  '238'

 L. 681       320  LOAD_FAST                'self'
              322  LOAD_METHOD              doCleanups
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 682       328  LOAD_FAST                'outcome'
              330  LOAD_ATTR                skipped
              332  GET_ITER         
              334  FOR_ITER            360  'to 360'
              336  UNPACK_SEQUENCE_2     2 
              338  STORE_FAST               'test'
              340  STORE_FAST               'reason'

 L. 683       342  LOAD_FAST                'self'
              344  LOAD_METHOD              _addSkip
              346  LOAD_FAST                'result'
              348  LOAD_FAST                'test'
              350  LOAD_FAST                'reason'
              352  CALL_METHOD_3         3  ''
              354  POP_TOP          
          356_358  JUMP_BACK           334  'to 334'

 L. 684       360  LOAD_FAST                'self'
              362  LOAD_METHOD              _feedErrorsToResult
              364  LOAD_FAST                'result'
              366  LOAD_FAST                'outcome'
              368  LOAD_ATTR                errors
              370  CALL_METHOD_2         2  ''
              372  POP_TOP          

 L. 685       374  LOAD_FAST                'outcome'
              376  LOAD_ATTR                success
          378_380  POP_JUMP_IF_FALSE   434  'to 434'

 L. 686       382  LOAD_FAST                'expecting_failure'
          384_386  POP_JUMP_IF_FALSE   424  'to 424'

 L. 687       388  LOAD_FAST                'outcome'
              390  LOAD_ATTR                expectedFailure
          392_394  POP_JUMP_IF_FALSE   412  'to 412'

 L. 688       396  LOAD_FAST                'self'
              398  LOAD_METHOD              _addExpectedFailure
              400  LOAD_FAST                'result'
              402  LOAD_FAST                'outcome'
              404  LOAD_ATTR                expectedFailure
              406  CALL_METHOD_2         2  ''
              408  POP_TOP          
              410  JUMP_FORWARD        422  'to 422'
            412_0  COME_FROM           392  '392'

 L. 690       412  LOAD_FAST                'self'
              414  LOAD_METHOD              _addUnexpectedSuccess
              416  LOAD_FAST                'result'
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          
            422_0  COME_FROM           410  '410'
              422  JUMP_FORWARD        434  'to 434'
            424_0  COME_FROM           384  '384'

 L. 692       424  LOAD_FAST                'result'
              426  LOAD_METHOD              addSuccess
              428  LOAD_FAST                'self'
              430  CALL_METHOD_1         1  ''
              432  POP_TOP          
            434_0  COME_FROM           422  '422'
            434_1  COME_FROM           378  '378'

 L. 693       434  LOAD_FAST                'result'
              436  POP_BLOCK        
              438  CALL_FINALLY        442  'to 442'
              440  RETURN_VALUE     
            442_0  COME_FROM           438  '438'
            442_1  COME_FROM_FINALLY   196  '196'

 L. 695       442  LOAD_FAST                'result'
              444  LOAD_METHOD              stopTest
              446  LOAD_FAST                'self'
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          

 L. 696       452  LOAD_FAST                'orig_result'
              454  LOAD_CONST               None
              456  COMPARE_OP               is
          458_460  POP_JUMP_IF_FALSE   490  'to 490'

 L. 697       462  LOAD_GLOBAL              getattr
              464  LOAD_FAST                'result'
              466  LOAD_STR                 'stopTestRun'
              468  LOAD_CONST               None
              470  CALL_FUNCTION_3       3  ''
              472  STORE_FAST               'stopTestRun'

 L. 698       474  LOAD_FAST                'stopTestRun'
              476  LOAD_CONST               None
              478  COMPARE_OP               is-not
          480_482  POP_JUMP_IF_FALSE   490  'to 490'

 L. 699       484  LOAD_FAST                'stopTestRun'
              486  CALL_FUNCTION_0       0  ''
              488  POP_TOP          
            490_0  COME_FROM           480  '480'
            490_1  COME_FROM           458  '458'

 L. 704       490  LOAD_FAST                'outcome'
              492  LOAD_ATTR                errors
              494  LOAD_METHOD              clear
              496  CALL_METHOD_0         0  ''
              498  POP_TOP          

 L. 705       500  LOAD_CONST               None
              502  LOAD_FAST                'outcome'
              504  STORE_ATTR               expectedFailure

 L. 708       506  LOAD_CONST               None
              508  LOAD_FAST                'self'
              510  STORE_ATTR               _outcome
              512  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 438

    def doCleanups(self):
        """Execute all cleanup functions. Normally called for you after
        tearDown."""
        outcome = self._outcome or _Outcome()
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop()
            with outcome.testPartExecutor(self):
                (self._callCleanup)(function, *args, **kwargs)

        return outcome.success

    @classmethod
    def doClassCleanups(cls):
        """Execute all class cleanup functions. Normally called for you after
        tearDownClass."""
        cls.tearDown_exceptions = []
        while cls._class_cleanups:
            function, args, kwargs = cls._class_cleanups.pop()
            try:
                function(*args, **kwargs)
            except Exception as exc:
                try:
                    cls.tearDown_exceptions.append(sys.exc_info())
                finally:
                    exc = None
                    del exc

    def __call__(self, *args, **kwds):
        return (self.run)(*args, **kwds)

    def debug(self):
        """Run the test without collecting errors in a TestResult"""
        self.setUp()
        getattr(self, self._testMethodName)()
        self.tearDown()
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop(-1)
            function(*args, **kwargs)

    def skipTest(self, reason):
        """Skip this test."""
        raise SkipTest(reason)

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failureException(msg)

    def assertFalse(self, expr, msg=None):
        """Check that the expression is false."""
        if expr:
            msg = self._formatMessage(msg, '%s is not false' % safe_repr(expr))
            raise self.failureException(msg)

    def assertTrue(self, expr, msg=None):
        """Check that the expression is true."""
        if not expr:
            msg = self._formatMessage(msg, '%s is not true' % safe_repr(expr))
            raise self.failureException(msg)

    def _formatMessage--- This code section failed: ---

 L. 777         0  LOAD_FAST                'self'
                2  LOAD_ATTR                longMessage
                4  POP_JUMP_IF_TRUE     14  'to 14'

 L. 778         6  LOAD_FAST                'msg'
                8  JUMP_IF_TRUE_OR_POP    12  'to 12'
               10  LOAD_FAST                'standardMsg'
             12_0  COME_FROM             8  '8'
               12  RETURN_VALUE     
             14_0  COME_FROM             4  '4'

 L. 779        14  LOAD_FAST                'msg'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 780        22  LOAD_FAST                'standardMsg'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 781        26  SETUP_FINALLY        42  'to 42'

 L. 784        28  LOAD_STR                 '%s : %s'
               30  LOAD_FAST                'standardMsg'
               32  LOAD_FAST                'msg'
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    26  '26'

 L. 785        42  DUP_TOP          
               44  LOAD_GLOBAL              UnicodeDecodeError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    80  'to 80'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 786        56  LOAD_STR                 '%s : %s'
               58  LOAD_GLOBAL              safe_repr
               60  LOAD_FAST                'standardMsg'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_GLOBAL              safe_repr
               66  LOAD_FAST                'msg'
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_2         2 
               72  BINARY_MODULO    
               74  ROT_FOUR         
               76  POP_EXCEPT       
               78  RETURN_VALUE     
             80_0  COME_FROM            48  '48'
               80  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 52

    def assertRaises(self, expected_exception, *args, **kwargs):
        """Fail unless an exception of class expected_exception is raised
           by the callable when invoked with specified positional and
           keyword arguments. If a different type of exception is
           raised, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.

           If called with the callable and arguments omitted, will return a
           context object used like this::

                with self.assertRaises(SomeException):
                    do_something()

           An optional keyword argument 'msg' can be provided when assertRaises
           is used as a context object.

           The context manager keeps a reference to the exception as
           the 'exception' attribute. This allows you to inspect the
           exception after the assertion::

               with self.assertRaises(SomeException) as cm:
                   do_something()
               the_exception = cm.exception
               self.assertEqual(the_exception.error_code, 3)
        """
        context = _AssertRaisesContext(expected_exception, self)
        try:
            return context.handle('assertRaises', args, kwargs)
        finally:
            context = None

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
        return context.handle('assertWarns', args, kwargs)

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
        return _AssertLogsContext(self, logger, level)

    def _getAssertEqualityFunc(self, first, second):
        """Get a detailed comparison function for the types of the two args.

        Returns: A callable accepting (first, second, msg=None) that will
        raise a failure exception if first != second with a useful human
        readable error message for those types.
        """
        if type(first) is type(second):
            asserter = self._type_equality_funcs.get(type(first))
            if asserter is not None:
                if isinstance(asserter, str):
                    asserter = getattr(self, asserter)
                return asserter
        return self._baseAssertEqual

    def _baseAssertEqual(self, first, second, msg=None):
        """The default assertEqual implementation, not type specific."""
        if not first == second:
            standardMsg = '%s != %s' % _common_shorten_repr(first, second)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)

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
            raise self.failureException(msg)

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        """Fail if the two objects are unequal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero, or by comparing that the
           difference between the two objects is more than the given
           delta.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most significant digit).

           If the two objects compare equal then they will automatically
           compare almost equal.
        """
        if first == second:
            return
        else:
            if delta is not None:
                if places is not None:
                    raise TypeError('specify delta or places not both')
            diff = abs(first - second)
            if delta is not None:
                if diff <= delta:
                    return
                standardMsg = '%s != %s within %s delta (%s difference)' % (
                 safe_repr(first),
                 safe_repr(second),
                 safe_repr(delta),
                 safe_repr(diff))
            else:
                if places is None:
                    places = 7
                if round(diff, places) == 0:
                    return
            standardMsg = '%s != %s within %r places (%s difference)' % (
             safe_repr(first),
             safe_repr(second),
             places,
             safe_repr(diff))
        msg = self._formatMessage(msg, standardMsg)
        raise self.failureException(msg)

    def assertNotAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        """Fail if the two objects are equal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero, or by comparing that the
           difference between the two objects is less than the given delta.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most significant digit).

           Objects that are equal automatically fail.
        """
        if delta is not None:
            if places is not None:
                raise TypeError('specify delta or places not both')
        else:
            diff = abs(first - second)
            if delta is not None:
                if not first == second:
                    if diff > delta:
                        return
                standardMsg = '%s == %s within %s delta (%s difference)' % (
                 safe_repr(first),
                 safe_repr(second),
                 safe_repr(delta),
                 safe_repr(diff))
            else:
                if places is None:
                    places = 7
            if not first == second:
                if round(diff, places) != 0:
                    return
            standardMsg = '%s == %s within %r places' % (safe_repr(first),
             safe_repr(second),
             places)
        msg = self._formatMessage(msg, standardMsg)
        raise self.failureException(msg)

    def assertSequenceEqual--- This code section failed: ---

 L.1017         0  LOAD_FAST                'seq_type'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    80  'to 80'

 L.1018         8  LOAD_FAST                'seq_type'
               10  LOAD_ATTR                __name__
               12  STORE_FAST               'seq_type_name'

 L.1019        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'seq1'
               18  LOAD_FAST                'seq_type'
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     46  'to 46'

 L.1020        24  LOAD_FAST                'self'
               26  LOAD_METHOD              failureException
               28  LOAD_STR                 'First sequence is not a %s: %s'

 L.1021        30  LOAD_FAST                'seq_type_name'
               32  LOAD_GLOBAL              safe_repr
               34  LOAD_FAST                'seq1'
               36  CALL_FUNCTION_1       1  ''
               38  BUILD_TUPLE_2         2 

 L.1020        40  BINARY_MODULO    
               42  CALL_METHOD_1         1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            22  '22'

 L.1022        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'seq2'
               50  LOAD_FAST                'seq_type'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_TRUE     84  'to 84'

 L.1023        56  LOAD_FAST                'self'
               58  LOAD_METHOD              failureException
               60  LOAD_STR                 'Second sequence is not a %s: %s'

 L.1024        62  LOAD_FAST                'seq_type_name'
               64  LOAD_GLOBAL              safe_repr
               66  LOAD_FAST                'seq2'
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_2         2 

 L.1023        72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
               78  JUMP_FORWARD         84  'to 84'
             80_0  COME_FROM             6  '6'

 L.1026        80  LOAD_STR                 'sequence'
               82  STORE_FAST               'seq_type_name'
             84_0  COME_FROM            78  '78'
             84_1  COME_FROM            54  '54'

 L.1028        84  LOAD_CONST               None
               86  STORE_FAST               'differing'

 L.1029        88  SETUP_FINALLY       102  'to 102'

 L.1030        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'seq1'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'len1'
               98  POP_BLOCK        
              100  JUMP_FORWARD        134  'to 134'
            102_0  COME_FROM_FINALLY    88  '88'

 L.1031       102  DUP_TOP          
              104  LOAD_GLOBAL              TypeError
              106  LOAD_GLOBAL              NotImplementedError
              108  BUILD_TUPLE_2         2 
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   132  'to 132'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.1032       120  LOAD_STR                 'First %s has no length.    Non-sequence?'

 L.1033       122  LOAD_FAST                'seq_type_name'

 L.1032       124  BINARY_MODULO    
              126  STORE_FAST               'differing'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM           112  '112'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM           100  '100'

 L.1035       134  LOAD_FAST                'differing'
              136  LOAD_CONST               None
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   188  'to 188'

 L.1036       142  SETUP_FINALLY       156  'to 156'

 L.1037       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'seq2'
              148  CALL_FUNCTION_1       1  ''
              150  STORE_FAST               'len2'
              152  POP_BLOCK        
              154  JUMP_FORWARD        188  'to 188'
            156_0  COME_FROM_FINALLY   142  '142'

 L.1038       156  DUP_TOP          
              158  LOAD_GLOBAL              TypeError
              160  LOAD_GLOBAL              NotImplementedError
              162  BUILD_TUPLE_2         2 
              164  COMPARE_OP               exception-match
              166  POP_JUMP_IF_FALSE   186  'to 186'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L.1039       174  LOAD_STR                 'Second %s has no length.    Non-sequence?'

 L.1040       176  LOAD_FAST                'seq_type_name'

 L.1039       178  BINARY_MODULO    
              180  STORE_FAST               'differing'
              182  POP_EXCEPT       
              184  JUMP_FORWARD        188  'to 188'
            186_0  COME_FROM           166  '166'
              186  END_FINALLY      
            188_0  COME_FROM           184  '184'
            188_1  COME_FROM           154  '154'
            188_2  COME_FROM           140  '140'

 L.1042       188  LOAD_FAST                'differing'
              190  LOAD_CONST               None
              192  COMPARE_OP               is
          194_196  POP_JUMP_IF_FALSE   676  'to 676'

 L.1043       198  LOAD_FAST                'seq1'
              200  LOAD_FAST                'seq2'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   210  'to 210'

 L.1044       206  LOAD_CONST               None
              208  RETURN_VALUE     
            210_0  COME_FROM           204  '204'

 L.1046       210  LOAD_STR                 '%ss differ: %s != %s\n'

 L.1047       212  LOAD_FAST                'seq_type_name'
              214  LOAD_METHOD              capitalize
              216  CALL_METHOD_0         0  ''
              218  BUILD_TUPLE_1         1 

 L.1048       220  LOAD_GLOBAL              _common_shorten_repr
              222  LOAD_FAST                'seq1'
              224  LOAD_FAST                'seq2'
              226  CALL_FUNCTION_2       2  ''

 L.1047       228  BINARY_ADD       

 L.1046       230  BINARY_MODULO    
              232  STORE_FAST               'differing'

 L.1050       234  LOAD_GLOBAL              range
              236  LOAD_GLOBAL              min
              238  LOAD_FAST                'len1'
              240  LOAD_FAST                'len2'
              242  CALL_FUNCTION_2       2  ''
              244  CALL_FUNCTION_1       1  ''
              246  GET_ITER         
            248_0  COME_FROM           390  '390'
              248  FOR_ITER            424  'to 424'
              250  STORE_FAST               'i'

 L.1051       252  SETUP_FINALLY       266  'to 266'

 L.1052       254  LOAD_FAST                'seq1'
              256  LOAD_FAST                'i'
              258  BINARY_SUBSCR    
              260  STORE_FAST               'item1'
              262  POP_BLOCK        
              264  JUMP_FORWARD        318  'to 318'
            266_0  COME_FROM_FINALLY   252  '252'

 L.1053       266  DUP_TOP          
              268  LOAD_GLOBAL              TypeError
              270  LOAD_GLOBAL              IndexError
              272  LOAD_GLOBAL              NotImplementedError
              274  BUILD_TUPLE_3         3 
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   316  'to 316'
              282  POP_TOP          
              284  POP_TOP          
              286  POP_TOP          

 L.1054       288  LOAD_FAST                'differing'
              290  LOAD_STR                 '\nUnable to index element %d of first %s\n'

 L.1055       292  LOAD_FAST                'i'
              294  LOAD_FAST                'seq_type_name'
              296  BUILD_TUPLE_2         2 

 L.1054       298  BINARY_MODULO    
              300  INPLACE_ADD      
              302  STORE_FAST               'differing'

 L.1056       304  POP_EXCEPT       
              306  POP_TOP          
          308_310  JUMP_ABSOLUTE       466  'to 466'
              312  POP_EXCEPT       
              314  JUMP_FORWARD        318  'to 318'
            316_0  COME_FROM           278  '278'
              316  END_FINALLY      
            318_0  COME_FROM           314  '314'
            318_1  COME_FROM           264  '264'

 L.1058       318  SETUP_FINALLY       332  'to 332'

 L.1059       320  LOAD_FAST                'seq2'
              322  LOAD_FAST                'i'
              324  BINARY_SUBSCR    
              326  STORE_FAST               'item2'
              328  POP_BLOCK        
              330  JUMP_FORWARD        384  'to 384'
            332_0  COME_FROM_FINALLY   318  '318'

 L.1060       332  DUP_TOP          
              334  LOAD_GLOBAL              TypeError
              336  LOAD_GLOBAL              IndexError
              338  LOAD_GLOBAL              NotImplementedError
              340  BUILD_TUPLE_3         3 
              342  COMPARE_OP               exception-match
          344_346  POP_JUMP_IF_FALSE   382  'to 382'
              348  POP_TOP          
              350  POP_TOP          
              352  POP_TOP          

 L.1061       354  LOAD_FAST                'differing'
              356  LOAD_STR                 '\nUnable to index element %d of second %s\n'

 L.1062       358  LOAD_FAST                'i'
              360  LOAD_FAST                'seq_type_name'
              362  BUILD_TUPLE_2         2 

 L.1061       364  BINARY_MODULO    
              366  INPLACE_ADD      
              368  STORE_FAST               'differing'

 L.1063       370  POP_EXCEPT       
              372  POP_TOP          
          374_376  JUMP_ABSOLUTE       466  'to 466'
              378  POP_EXCEPT       
              380  JUMP_FORWARD        384  'to 384'
            382_0  COME_FROM           344  '344'
              382  END_FINALLY      
            384_0  COME_FROM           380  '380'
            384_1  COME_FROM           330  '330'

 L.1065       384  LOAD_FAST                'item1'
              386  LOAD_FAST                'item2'
              388  COMPARE_OP               !=
              390  POP_JUMP_IF_FALSE   248  'to 248'

 L.1066       392  LOAD_FAST                'differing'
              394  LOAD_STR                 '\nFirst differing element %d:\n%s\n%s\n'

 L.1067       396  LOAD_FAST                'i'
              398  BUILD_TUPLE_1         1 
              400  LOAD_GLOBAL              _common_shorten_repr
              402  LOAD_FAST                'item1'
              404  LOAD_FAST                'item2'
              406  CALL_FUNCTION_2       2  ''
              408  BINARY_ADD       

 L.1066       410  BINARY_MODULO    
              412  INPLACE_ADD      
              414  STORE_FAST               'differing'

 L.1068       416  POP_TOP          
          418_420  BREAK_LOOP          466  'to 466'
              422  JUMP_BACK           248  'to 248'

 L.1070       424  LOAD_FAST                'len1'
              426  LOAD_FAST                'len2'
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   466  'to 466'
              434  LOAD_FAST                'seq_type'
              436  LOAD_CONST               None
              438  COMPARE_OP               is
          440_442  POP_JUMP_IF_FALSE   466  'to 466'

 L.1071       444  LOAD_GLOBAL              type
              446  LOAD_FAST                'seq1'
              448  CALL_FUNCTION_1       1  ''
              450  LOAD_GLOBAL              type
              452  LOAD_FAST                'seq2'
              454  CALL_FUNCTION_1       1  ''
              456  COMPARE_OP               !=

 L.1070   458_460  POP_JUMP_IF_FALSE   466  'to 466'

 L.1073       462  LOAD_CONST               None
              464  RETURN_VALUE     
            466_0  COME_FROM           458  '458'
            466_1  COME_FROM           440  '440'
            466_2  COME_FROM           430  '430'

 L.1075       466  LOAD_FAST                'len1'
              468  LOAD_FAST                'len2'
              470  COMPARE_OP               >
          472_474  POP_JUMP_IF_FALSE   572  'to 572'

 L.1076       476  LOAD_FAST                'differing'
              478  LOAD_STR                 '\nFirst %s contains %d additional elements.\n'

 L.1077       480  LOAD_FAST                'seq_type_name'
              482  LOAD_FAST                'len1'
              484  LOAD_FAST                'len2'
              486  BINARY_SUBTRACT  
              488  BUILD_TUPLE_2         2 

 L.1076       490  BINARY_MODULO    
              492  INPLACE_ADD      
              494  STORE_FAST               'differing'

 L.1078       496  SETUP_FINALLY       526  'to 526'

 L.1079       498  LOAD_FAST                'differing'
              500  LOAD_STR                 'First extra element %d:\n%s\n'

 L.1080       502  LOAD_FAST                'len2'
              504  LOAD_GLOBAL              safe_repr
              506  LOAD_FAST                'seq1'
              508  LOAD_FAST                'len2'
              510  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  ''
              514  BUILD_TUPLE_2         2 

 L.1079       516  BINARY_MODULO    
              518  INPLACE_ADD      
              520  STORE_FAST               'differing'
              522  POP_BLOCK        
              524  JUMP_FORWARD        570  'to 570'
            526_0  COME_FROM_FINALLY   496  '496'

 L.1081       526  DUP_TOP          
              528  LOAD_GLOBAL              TypeError
              530  LOAD_GLOBAL              IndexError
              532  LOAD_GLOBAL              NotImplementedError
              534  BUILD_TUPLE_3         3 
              536  COMPARE_OP               exception-match
          538_540  POP_JUMP_IF_FALSE   568  'to 568'
              542  POP_TOP          
              544  POP_TOP          
              546  POP_TOP          

 L.1082       548  LOAD_FAST                'differing'
              550  LOAD_STR                 'Unable to index element %d of first %s\n'

 L.1083       552  LOAD_FAST                'len2'
              554  LOAD_FAST                'seq_type_name'
              556  BUILD_TUPLE_2         2 

 L.1082       558  BINARY_MODULO    
              560  INPLACE_ADD      
              562  STORE_FAST               'differing'
              564  POP_EXCEPT       
              566  JUMP_FORWARD        570  'to 570'
            568_0  COME_FROM           538  '538'
              568  END_FINALLY      
            570_0  COME_FROM           566  '566'
            570_1  COME_FROM           524  '524'
              570  JUMP_FORWARD        676  'to 676'
            572_0  COME_FROM           472  '472'

 L.1084       572  LOAD_FAST                'len1'
              574  LOAD_FAST                'len2'
              576  COMPARE_OP               <
          578_580  POP_JUMP_IF_FALSE   676  'to 676'

 L.1085       582  LOAD_FAST                'differing'
              584  LOAD_STR                 '\nSecond %s contains %d additional elements.\n'

 L.1086       586  LOAD_FAST                'seq_type_name'
              588  LOAD_FAST                'len2'
              590  LOAD_FAST                'len1'
              592  BINARY_SUBTRACT  
              594  BUILD_TUPLE_2         2 

 L.1085       596  BINARY_MODULO    
              598  INPLACE_ADD      
              600  STORE_FAST               'differing'

 L.1087       602  SETUP_FINALLY       632  'to 632'

 L.1088       604  LOAD_FAST                'differing'
              606  LOAD_STR                 'First extra element %d:\n%s\n'

 L.1089       608  LOAD_FAST                'len1'
              610  LOAD_GLOBAL              safe_repr
              612  LOAD_FAST                'seq2'
              614  LOAD_FAST                'len1'
              616  BINARY_SUBSCR    
              618  CALL_FUNCTION_1       1  ''
              620  BUILD_TUPLE_2         2 

 L.1088       622  BINARY_MODULO    
              624  INPLACE_ADD      
              626  STORE_FAST               'differing'
              628  POP_BLOCK        
              630  JUMP_FORWARD        676  'to 676'
            632_0  COME_FROM_FINALLY   602  '602'

 L.1090       632  DUP_TOP          
              634  LOAD_GLOBAL              TypeError
              636  LOAD_GLOBAL              IndexError
              638  LOAD_GLOBAL              NotImplementedError
              640  BUILD_TUPLE_3         3 
              642  COMPARE_OP               exception-match
          644_646  POP_JUMP_IF_FALSE   674  'to 674'
              648  POP_TOP          
              650  POP_TOP          
              652  POP_TOP          

 L.1091       654  LOAD_FAST                'differing'
              656  LOAD_STR                 'Unable to index element %d of second %s\n'

 L.1092       658  LOAD_FAST                'len1'
              660  LOAD_FAST                'seq_type_name'
              662  BUILD_TUPLE_2         2 

 L.1091       664  BINARY_MODULO    
              666  INPLACE_ADD      
              668  STORE_FAST               'differing'
              670  POP_EXCEPT       
              672  JUMP_FORWARD        676  'to 676'
            674_0  COME_FROM           644  '644'
              674  END_FINALLY      
            676_0  COME_FROM           672  '672'
            676_1  COME_FROM           630  '630'
            676_2  COME_FROM           578  '578'
            676_3  COME_FROM           570  '570'
            676_4  COME_FROM           194  '194'

 L.1093       676  LOAD_FAST                'differing'
              678  STORE_FAST               'standardMsg'

 L.1094       680  LOAD_STR                 '\n'
              682  LOAD_STR                 '\n'
              684  LOAD_METHOD              join

 L.1095       686  LOAD_GLOBAL              difflib
              688  LOAD_METHOD              ndiff
              690  LOAD_GLOBAL              pprint
              692  LOAD_METHOD              pformat
              694  LOAD_FAST                'seq1'
              696  CALL_METHOD_1         1  ''
              698  LOAD_METHOD              splitlines
              700  CALL_METHOD_0         0  ''

 L.1096       702  LOAD_GLOBAL              pprint
              704  LOAD_METHOD              pformat
              706  LOAD_FAST                'seq2'
              708  CALL_METHOD_1         1  ''
              710  LOAD_METHOD              splitlines
              712  CALL_METHOD_0         0  ''

 L.1095       714  CALL_METHOD_2         2  ''

 L.1094       716  CALL_METHOD_1         1  ''
              718  BINARY_ADD       
              720  STORE_FAST               'diffMsg'

 L.1098       722  LOAD_FAST                'self'
              724  LOAD_METHOD              _truncateMessage
              726  LOAD_FAST                'standardMsg'
              728  LOAD_FAST                'diffMsg'
              730  CALL_METHOD_2         2  ''
              732  STORE_FAST               'standardMsg'

 L.1099       734  LOAD_FAST                'self'
              736  LOAD_METHOD              _formatMessage
              738  LOAD_FAST                'msg'
              740  LOAD_FAST                'standardMsg'
              742  CALL_METHOD_2         2  ''
              744  STORE_FAST               'msg'

 L.1100       746  LOAD_FAST                'self'
              748  LOAD_METHOD              fail
              750  LOAD_FAST                'msg'
              752  CALL_METHOD_1         1  ''
              754  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 306

    def _truncateMessage(self, message, diff):
        max_diff = self.maxDiff
        if max_diff is None or len(diff) <= max_diff:
            return message + diff
        return message + DIFF_OMITTED % len(diff)

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

    def assertSetEqual(self, set1, set2, msg=None):
        """A set-specific equality assertion.

        Args:
            set1: The first set to compare.
            set2: The second set to compare.
            msg: Optional message to use on failure instead of a list of
                    differences.

        assertSetEqual uses ducktyping to support different types of sets, and
        is optimized for sets specifically (parameters must support a
        difference method).
        """
        try:
            difference1 = set1.difference(set2)
        except TypeError as e:
            try:
                self.fail('invalid type when attempting set difference: %s' % e)
            finally:
                e = None
                del e

        except AttributeError as e:
            try:
                self.fail('first argument does not support set difference: %s' % e)
            finally:
                e = None
                del e

        else:
            try:
                difference2 = set2.difference(set1)
            except TypeError as e:
                try:
                    self.fail('invalid type when attempting set difference: %s' % e)
                finally:
                    e = None
                    del e

            except AttributeError as e:
                try:
                    self.fail('second argument does not support set difference: %s' % e)
                finally:
                    e = None
                    del e

            else:
                if not difference1:
                    if not difference2:
                        return
                    else:
                        lines = []
                        if difference1:
                            lines.append('Items in the first set but not the second:')
                            for item in difference1:
                                lines.append(repr(item))

                    if difference2:
                        lines.append('Items in the second set but not the first:')
                        for item in difference2:
                            lines.append(repr(item))

                else:
                    standardMsg = '\n'.join(lines)
                    self.fail(self._formatMessage(msg, standardMsg))

    def assertIn(self, member, container, msg=None):
        """Just like self.assertTrue(a in b), but with a nicer default message."""
        if member not in container:
            standardMsg = '%s not found in %s' % (safe_repr(member),
             safe_repr(container))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertNotIn(self, member, container, msg=None):
        """Just like self.assertTrue(a not in b), but with a nicer default message."""
        if member in container:
            standardMsg = '%s unexpectedly found in %s' % (safe_repr(member),
             safe_repr(container))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIs(self, expr1, expr2, msg=None):
        """Just like self.assertTrue(a is b), but with a nicer default message."""
        if expr1 is not expr2:
            standardMsg = '%s is not %s' % (safe_repr(expr1),
             safe_repr(expr2))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsNot(self, expr1, expr2, msg=None):
        """Just like self.assertTrue(a is not b), but with a nicer default message."""
        if expr1 is expr2:
            standardMsg = 'unexpectedly identical: %s' % (safe_repr(expr1),)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertDictEqual(self, d1, d2, msg=None):
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')
        if d1 != d2:
            standardMsg = '%s != %s' % _common_shorten_repr(d1, d2)
            diff = '\n' + '\n'.join(difflib.ndiff(pprint.pformat(d1).splitlines(), pprint.pformat(d2).splitlines()))
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """Checks whether dictionary is a superset of subset."""
        warnings.warn('assertDictContainsSubset is deprecated', DeprecationWarning)
        missing = []
        mismatched = []
        for key, value in subset.items():
            if key not in dictionary:
                missing.append(key)
        else:
            if value != dictionary[key]:
                mismatched.append('%s, expected: %s, actual: %s' % (
                 safe_repr(key), safe_repr(value),
                 safe_repr(dictionary[key])))
            if not missing:
                if not mismatched:
                    return
            standardMsg = ''
            if missing:
                standardMsg = 'Missing: %s' % ','.join((safe_repr(m) for m in missing))
            if mismatched:
                if standardMsg:
                    standardMsg += '; '
                standardMsg += 'Mismatched values: %s' % ','.join(mismatched)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertCountEqual(self, first, second, msg=None):
        """Asserts that two iterables have the same elements, the same number of
        times, without regard to order.

            self.assertEqual(Counter(list(first)),
                             Counter(list(second)))

         Example:
            - [0, 1, 1] and [1, 0, 1] compare equal.
            - [0, 0, 1] and [0, 1] compare unequal.

        """
        first_seq, second_seq = list(first), list(second)
        try:
            first = collections.Counter(first_seq)
            second = collections.Counter(second_seq)
        except TypeError:
            differences = _count_diff_all_purpose(first_seq, second_seq)
        else:
            if first == second:
                return
            differences = _count_diff_hashable(first_seq, second_seq)
        if differences:
            standardMsg = 'Element counts were not equal:\n'
            lines = ['First has %d, Second has %d:  %r' % diff for diff in differences]
            diffMsg = '\n'.join(lines)
            standardMsg = self._truncateMessage(standardMsg, diffMsg)
            msg = self._formatMessage(msg, standardMsg)
            self.fail(msg)

    def assertMultiLineEqual(self, first, second, msg=None):
        """Assert that two multi-line strings are equal."""
        self.assertIsInstance(first, str, 'First argument is not a string')
        self.assertIsInstance(second, str, 'Second argument is not a string')
        if first != second:
            if len(first) > self._diffThreshold or len(second) > self._diffThreshold:
                self._baseAssertEqual(first, second, msg)
            firstlines = first.splitlines(keepends=True)
            secondlines = second.splitlines(keepends=True)
            if len(firstlines) == 1:
                if first.strip('\r\n') == first:
                    firstlines = [
                     first + '\n']
                    secondlines = [second + '\n']
            standardMsg = '%s != %s' % _common_shorten_repr(first, second)
            diff = '\n' + ''.join(difflib.ndiff(firstlines, secondlines))
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertLess(self, a, b, msg=None):
        """Just like self.assertTrue(a < b), but with a nicer default message."""
        if not a < b:
            standardMsg = '%s not less than %s' % (safe_repr(a), safe_repr(b))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertLessEqual(self, a, b, msg=None):
        """Just like self.assertTrue(a <= b), but with a nicer default message."""
        if not a <= b:
            standardMsg = '%s not less than or equal to %s' % (safe_repr(a), safe_repr(b))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertGreater(self, a, b, msg=None):
        """Just like self.assertTrue(a > b), but with a nicer default message."""
        if not a > b:
            standardMsg = '%s not greater than %s' % (safe_repr(a), safe_repr(b))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertGreaterEqual(self, a, b, msg=None):
        """Just like self.assertTrue(a >= b), but with a nicer default message."""
        if not a >= b:
            standardMsg = '%s not greater than or equal to %s' % (safe_repr(a), safe_repr(b))
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsNone(self, obj, msg=None):
        """Same as self.assertTrue(obj is None), with a nicer default message."""
        if obj is not None:
            standardMsg = '%s is not None' % (safe_repr(obj),)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsNotNone(self, obj, msg=None):
        """Included for symmetry with assertIsNone."""
        if obj is None:
            standardMsg = 'unexpectedly None'
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsInstance(self, obj, cls, msg=None):
        """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
        default message."""
        if not isinstance(obj, cls):
            standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertNotIsInstance(self, obj, cls, msg=None):
        """Included for symmetry with assertIsInstance."""
        if isinstance(obj, cls):
            standardMsg = '%s is an instance of %r' % (safe_repr(obj), cls)
            self.fail(self._formatMessage(msg, standardMsg))

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
        return context.handle('assertRaisesRegex', args, kwargs)

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
        return context.handle('assertWarnsRegex', args, kwargs)

    def assertRegex(self, text, expected_regex, msg=None):
        """Fail the test unless the text matches the regular expression."""
        if isinstance(expected_regex, (str, bytes)):
            assert expected_regex, 'expected_regex must not be empty.'
            expected_regex = re.compile(expected_regex)
        if not expected_regex.search(text):
            standardMsg = "Regex didn't match: %r not found in %r" % (
             expected_regex.pattern, text)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)

    def assertNotRegex(self, text, unexpected_regex, msg=None):
        """Fail the test if the text matches the regular expression."""
        if isinstance(unexpected_regex, (str, bytes)):
            unexpected_regex = re.compile(unexpected_regex)
        match = unexpected_regex.search(text)
        if match:
            standardMsg = 'Regex matched: %r matches %r in %r' % (
             text[match.start():match.end()],
             unexpected_regex.pattern,
             text)
            msg = self._formatMessage(msg, standardMsg)
            raise self.failureException(msg)

    def _deprecate(original_func):

        def deprecated_func(*args, **kwargs):
            warnings.warn('Please use {0} instead.'.format(original_func.__name__), DeprecationWarning, 2)
            return original_func(*args, **kwargs)

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
        super(FunctionTestCase, self).__init__()
        self._setUpFunc = setUp
        self._tearDownFunc = tearDown
        self._testFunc = testFunc
        self._description = description

    def setUp(self):
        if self._setUpFunc is not None:
            self._setUpFunc()

    def tearDown(self):
        if self._tearDownFunc is not None:
            self._tearDownFunc()

    def runTest(self):
        self._testFunc()

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

    def shortDescription(self):
        if self._description is not None:
            return self._description
        doc = self._testFunc.__doc__
        return doc and doc.split('\n')[0].strip() or None


class _SubTest(TestCase):

    def __init__(self, test_case, message, params):
        super().__init__()
        self._message = message
        self.test_case = test_case
        self.params = params
        self.failureException = test_case.failureException

    def runTest(self):
        raise NotImplementedError('subtests cannot be run directly')

    def _subDescription(self):
        parts = []
        if self._message is not _subtest_msg_sentinel:
            parts.append('[{}]'.format(self._message))
        if self.params:
            params_desc = ', '.join(('{}={!r}'.format(k, v) for k, v in self.params.items()))
            parts.append('({})'.format(params_desc))
        return ' '.join(parts) or '(<subtest>)'

    def id(self):
        return '{} {}'.format(self.test_case.id(), self._subDescription())

    def shortDescription(self):
        """Returns a one-line description of the subtest, or None if no
        description has been provided.
        """
        return self.test_case.shortDescription()

    def __str__(self):
        return '{} {}'.format(self.test_case, self._subDescription())