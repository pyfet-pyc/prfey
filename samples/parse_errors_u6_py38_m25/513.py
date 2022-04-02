# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: unittest\suite.py
"""TestSuite"""
import sys
from . import case
from . import util
__unittest = True

def _call_if_exists(parent, attr):
    func = getattr(parent, attr, lambda : None)
    func()


class BaseTestSuite(object):
    __doc__ = "A simple test suite that doesn't provide class or module shared fixtures.\n    "
    _cleanup = True

    def __init__(self, tests=()):
        self._tests = []
        self._removed_tests = 0
        self.addTests(tests)

    def __repr__(self):
        return '<%s tests=%s>' % (util.strclass(self.__class__), list(self))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return list(self) == list(other)

    def __iter__(self):
        return iter(self._tests)

    def countTestCases(self):
        cases = self._removed_tests
        for test in self:
            if test:
                cases += test.countTestCases()
            return cases

    def addTest(self, test):
        if not callable(test):
            raise TypeError('{} is not callable'.format(repr(test)))
        if isinstance(test, type):
            if issubclass(test, (
             case.TestCase, TestSuite)):
                raise TypeError('TestCases and TestSuites must be instantiated before passing them to addTest()')
        self._tests.append(test)

    def addTests(self, tests):
        if isinstance(tests, str):
            raise TypeError('tests must be an iterable of tests, not a string')
        for test in tests:
            self.addTest(test)

    def run(self, result):
        for index, test in enumerate(self):
            if result.shouldStop:
                break
            test(result)
            if self._cleanup:
                self._removeTestAtIndex(index)
            return result

    def _removeTestAtIndex(self, index):
        """Stop holding a reference to the TestCase at index."""
        try:
            test = self._tests[index]
        except TypeError:
            pass
        else:
            if hasattr(test, 'countTestCases'):
                self._removed_tests += test.countTestCases()
            self._tests[index] = None

    def __call__(self, *args, **kwds):
        return (self.run)(*args, **kwds)

    def debug(self):
        """Run the tests without collecting errors in a TestResult"""
        for test in self:
            test.debug()


class TestSuite(BaseTestSuite):
    __doc__ = 'A test suite is a composite test consisting of a number of TestCases.\n\n    For use, create an instance of TestSuite, then add test case instances.\n    When all tests have been added, the suite can be passed to a test\n    runner, such as TextTestRunner. It will run the individual test cases\n    in the order in which they were added, aggregating the results. When\n    subclassing, do not forget to call the base class constructor.\n    '

    def run--- This code section failed: ---

 L. 103         0  LOAD_CONST               False
                2  STORE_FAST               'topLevel'

 L. 104         4  LOAD_GLOBAL              getattr
                6  LOAD_FAST                'result'
                8  LOAD_STR                 '_testRunEntered'
               10  LOAD_CONST               False
               12  CALL_FUNCTION_3       3  ''
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 105        20  LOAD_CONST               True
               22  DUP_TOP          
               24  LOAD_FAST                'result'
               26  STORE_ATTR               _testRunEntered
               28  STORE_FAST               'topLevel'
             30_0  COME_FROM            18  '18'

 L. 107        30  LOAD_GLOBAL              enumerate
               32  LOAD_FAST                'self'
               34  CALL_FUNCTION_1       1  ''
               36  GET_ITER         
             38_0  COME_FROM           162  '162'
             38_1  COME_FROM           120  '120'
               38  FOR_ITER            176  'to 176'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'index'
               44  STORE_FAST               'test'

 L. 108        46  LOAD_FAST                'result'
               48  LOAD_ATTR                shouldStop
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 109        52  POP_TOP          
               54  BREAK_LOOP          176  'to 176'
             56_0  COME_FROM            50  '50'

 L. 111        56  LOAD_GLOBAL              _isnotsuite
               58  LOAD_FAST                'test'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_FALSE   136  'to 136'

 L. 112        64  LOAD_FAST                'self'
               66  LOAD_METHOD              _tearDownPreviousClass
               68  LOAD_FAST                'test'
               70  LOAD_FAST                'result'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

 L. 113        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _handleModuleFixture
               80  LOAD_FAST                'test'
               82  LOAD_FAST                'result'
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          

 L. 114        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _handleClassSetUp
               92  LOAD_FAST                'test'
               94  LOAD_FAST                'result'
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 115       100  LOAD_FAST                'test'
              102  LOAD_ATTR                __class__
              104  LOAD_FAST                'result'
              106  STORE_ATTR               _previousTestClass

 L. 117       108  LOAD_GLOBAL              getattr
              110  LOAD_FAST                'test'
              112  LOAD_ATTR                __class__
              114  LOAD_STR                 '_classSetupFailed'
              116  LOAD_CONST               False
              118  CALL_FUNCTION_3       3  ''
              120  POP_JUMP_IF_TRUE     38  'to 38'

 L. 118       122  LOAD_GLOBAL              getattr
              124  LOAD_FAST                'result'
              126  LOAD_STR                 '_moduleSetUpFailed'
              128  LOAD_CONST               False
              130  CALL_FUNCTION_3       3  ''

 L. 117       132  POP_JUMP_IF_FALSE   136  'to 136'

 L. 119       134  JUMP_BACK            38  'to 38'
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            62  '62'

 L. 121       136  LOAD_FAST                'debug'
              138  POP_JUMP_IF_TRUE    150  'to 150'

 L. 122       140  LOAD_FAST                'test'
              142  LOAD_FAST                'result'
              144  CALL_FUNCTION_1       1  ''
              146  POP_TOP          
              148  JUMP_FORWARD        158  'to 158'
            150_0  COME_FROM           138  '138'

 L. 124       150  LOAD_FAST                'test'
              152  LOAD_METHOD              debug
              154  CALL_METHOD_0         0  ''
              156  POP_TOP          
            158_0  COME_FROM           148  '148'

 L. 126       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _cleanup
              162  POP_JUMP_IF_FALSE    38  'to 38'

 L. 127       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _removeTestAtIndex
              168  LOAD_FAST                'index'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_BACK            38  'to 38'

 L. 129       176  LOAD_FAST                'topLevel'
              178  POP_JUMP_IF_FALSE   208  'to 208'

 L. 130       180  LOAD_FAST                'self'
              182  LOAD_METHOD              _tearDownPreviousClass
              184  LOAD_CONST               None
              186  LOAD_FAST                'result'
              188  CALL_METHOD_2         2  ''
              190  POP_TOP          

 L. 131       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _handleModuleTearDown
              196  LOAD_FAST                'result'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L. 132       202  LOAD_CONST               False
              204  LOAD_FAST                'result'
              206  STORE_ATTR               _testRunEntered
            208_0  COME_FROM           178  '178'

 L. 133       208  LOAD_FAST                'result'
              210  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 210

    def debug(self):
        """Run the tests without collecting errors in a TestResult"""
        debug = _DebugResult()
        self.rundebugTrue

    def _handleClassSetUp(self, test, result):
        previousClass = getattr(result, '_previousTestClass', None)
        currentClass = test.__class__
        if currentClass == previousClass:
            return
        if result._moduleSetUpFailed:
            return
        if getattr(currentClass, '__unittest_skip__', False):
            return
        try:
            currentClass._classSetupFailed = False
        except TypeError:
            pass
        else:
            setUpClass = getattr(currentClass, 'setUpClass', None)
            if setUpClass is not None:
                _call_if_exists(result, '_setupStdout')
                try:
                    try:
                        setUpClass()
                    except Exception as e:
                        try:
                            if isinstance(result, _DebugResult):
                                raise
                            currentClass._classSetupFailed = True
                            className = util.strclass(currentClass)
                            self._createClassOrModuleLevelException(result, e, 'setUpClass', className)
                        finally:
                            e = None
                            del e

                finally:
                    _call_if_exists(result, '_restoreStdout')
                    if currentClass._classSetupFailed is True:
                        currentClass.doClassCleanups()
                        if len(currentClass.tearDown_exceptions) > 0:
                            for exc in currentClass.tearDown_exceptions:
                                self._createClassOrModuleLevelException(result,
                                  (exc[1]), 'setUpClass', className, info=exc)

    def _get_previous_module(self, result):
        previousModule = None
        previousClass = getattr(result, '_previousTestClass', None)
        if previousClass is not None:
            previousModule = previousClass.__module__
        return previousModule

    def _handleModuleFixture(self, test, result):
        previousModule = self._get_previous_module(result)
        currentModule = test.__class__.__module__
        if currentModule == previousModule:
            return
        self._handleModuleTearDown(result)
        result._moduleSetUpFailed = False
        try:
            module = sys.modules[currentModule]
        except KeyError:
            return
        else:
            setUpModule = getattr(module, 'setUpModule', None)
            if setUpModule is not None:
                _call_if_exists(result, '_setupStdout')
                try:
                    try:
                        setUpModule()
                    except Exception as e:
                        try:
                            try:
                                case.doModuleCleanups()
                            except Exception as exc:
                                try:
                                    self._createClassOrModuleLevelException(result, exc, 'setUpModule', currentModule)
                                finally:
                                    exc = None
                                    del exc

                            else:
                                if isinstance(result, _DebugResult):
                                    raise
                                result._moduleSetUpFailed = True
                                self._createClassOrModuleLevelException(result, e, 'setUpModule', currentModule)
                        finally:
                            e = None
                            del e

                finally:
                    _call_if_exists(result, '_restoreStdout')

    def _createClassOrModuleLevelException(self, result, exc, method_name, parent, info=None):
        errorName = f"{method_name} ({parent})"
        self._addClassOrModuleLevelException(result, exc, errorName, info)

    def _addClassOrModuleLevelException(self, result, exception, errorName, info=None):
        error = _ErrorHolder(errorName)
        addSkip = getattr(result, 'addSkip', None)
        if addSkip is not None and isinstance(exception, case.SkipTest):
            addSkip(error, str(exception))
        else:
            if not info:
                result.addErrorerrorsys.exc_info()
            else:
                result.addErrorerrorinfo

    def _handleModuleTearDown(self, result):
        previousModule = self._get_previous_module(result)
        if previousModule is None:
            return
        if result._moduleSetUpFailed:
            return
        try:
            module = sys.modules[previousModule]
        except KeyError:
            return
        else:
            tearDownModule = getattr(module, 'tearDownModule', None)
            if tearDownModule is not None:
                _call_if_exists(result, '_setupStdout')
                try:
                    try:
                        tearDownModule()
                    except Exception as e:
                        try:
                            if isinstance(result, _DebugResult):
                                raise
                            self._createClassOrModuleLevelException(result, e, 'tearDownModule', previousModule)
                        finally:
                            e = None
                            del e

                finally:
                    _call_if_exists(result, '_restoreStdout')
                    try:
                        case.doModuleCleanups()
                    except Exception as e:
                        try:
                            self._createClassOrModuleLevelException(result, e, 'tearDownModule', previousModule)
                        finally:
                            e = None
                            del e

    def _tearDownPreviousClass(self, test, result):
        previousClass = getattr(result, '_previousTestClass', None)
        currentClass = test.__class__
        if currentClass == previousClass:
            return
        if getattr(previousClass, '_classSetupFailed', False):
            return
        if getattr(result, '_moduleSetUpFailed', False):
            return
        if getattr(previousClass, '__unittest_skip__', False):
            return
        tearDownClass = getattr(previousClass, 'tearDownClass', None)
        if tearDownClass is not None:
            _call_if_exists(result, '_setupStdout')
            try:
                try:
                    tearDownClass()
                except Exception as e:
                    try:
                        if isinstance(result, _DebugResult):
                            raise
                        className = util.strclass(previousClass)
                        self._createClassOrModuleLevelException(result, e, 'tearDownClass', className)
                    finally:
                        e = None
                        del e

            finally:
                _call_if_exists(result, '_restoreStdout')
                previousClass.doClassCleanups()
                if len(previousClass.tearDown_exceptions) > 0:
                    for exc in previousClass.tearDown_exceptions:
                        className = util.strclass(previousClass)
                        self._createClassOrModuleLevelException(result, (exc[1]), 'tearDownClass',
                          className,
                          info=exc)


class _ErrorHolder(object):
    __doc__ = '\n    Placeholder for a TestCase inside a result. As far as a TestResult\n    is concerned, this looks exactly like a unit test. Used to insert\n    arbitrary errors into a test suite run.\n    '
    failureException = None

    def __init__(self, description):
        self.description = description

    def id(self):
        return self.description

    def shortDescription(self):
        pass

    def __repr__(self):
        return '<ErrorHolder description=%r>' % (self.description,)

    def __str__(self):
        return self.id()

    def run(self, result):
        pass

    def __call__(self, result):
        return self.run(result)

    def countTestCases(self):
        return 0


def _isnotsuite(test):
    """A crude way to tell apart testcases and suites with duck-typing"""
    try:
        iter(test)
    except TypeError:
        return True
    else:
        return False


class _DebugResult(object):
    __doc__ = 'Used by the TestSuite to hold previous class when running in debug.'
    _previousTestClass = None
    _moduleSetUpFailed = False
    shouldStop = False