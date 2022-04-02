# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: unittest\loader.py
"""Loading unittests."""
import os, re, sys, traceback, types, functools, warnings
from fnmatch import fnmatch, fnmatchcase
from . import case, suite, util
__unittest = True
VALID_MODULE_NAME = re.compile('[_a-z]\\w*\\.py$', re.IGNORECASE)

class _FailedTest(case.TestCase):
    _testMethodName = None

    def __init__(self, method_name, exception):
        self._exception = exception
        super(_FailedTest, self).__init__(method_name)

    def __getattr__(self, name):
        if name != self._testMethodName:
            return super(_FailedTest, self).__getattr__(name)

        def testFailure():
            raise self._exception

        return testFailure


def _make_failed_import_test(name, suiteClass):
    message = 'Failed to import test module: %s\n%s' % (
     name, traceback.format_exc())
    return _make_failed_test(name, ImportError(message), suiteClass, message)


def _make_failed_load_tests(name, exception, suiteClass):
    message = 'Failed to call load_tests:\n%s' % (traceback.format_exc(),)
    return _make_failed_test(name, exception, suiteClass, message)


def _make_failed_test(methodname, exception, suiteClass, message):
    test = _FailedTest(methodname, exception)
    return (
     suiteClass((test,)), message)


def _make_skipped_test(methodname, exception, suiteClass):

    @case.skip(str(exception))
    def testSkipped(self):
        pass

    attrs = {methodname: testSkipped}
    TestClass = type('ModuleSkipped', (case.TestCase,), attrs)
    return suiteClass((TestClass(methodname),))


def _jython_aware_splitext(path):
    if path.lower().endswith('$py.class'):
        return path[:-9]
    return os.path.splitext(path)[0]


class TestLoader(object):
    __doc__ = '\n    This class is responsible for loading tests according to various criteria\n    and returning them wrapped in a TestSuite\n    '
    testMethodPrefix = 'test'
    sortTestMethodsUsing = staticmethod(util.three_way_cmp)
    testNamePatterns = None
    suiteClass = suite.TestSuite
    _top_level_dir = None

    def __init__(self):
        super(TestLoader, self).__init__()
        self.errors = []
        self._loading_packages = set()

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all test cases contained in testCaseClass"""
        if issubclass(testCaseClass, suite.TestSuite):
            raise TypeError('Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?')
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames:
            if hasattr(testCaseClass, 'runTest'):
                testCaseNames = [
                 'runTest']
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        return loaded_suite

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        """Return a suite of all test cases contained in the given module"""
        if len(args) > 0 or ('use_load_tests' in kws):
            warnings.warn('use_load_tests is deprecated and ignored', DeprecationWarning)
            kws.pop('use_load_tests', None)
        if len(args) > 1:
            complaint = len(args) + 1
            raise TypeError('loadTestsFromModule() takes 1 positional argument but {} were given'.format(complaint))
        if len(kws) != 0:
            complaint = sorted(kws)[0]
            raise TypeError("loadTestsFromModule() got an unexpected keyword argument '{}'".format(complaint))
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type):
                if issubclass(obj, case.TestCase):
                    tests.append(self.loadTestsFromTestCase(obj))

        load_tests = getattr(module, 'load_tests', None)
        tests = self.suiteClass(tests)
        if load_tests is not None:
            try:
                return load_tests(self, tests, pattern)
            except Exception as e:
                try:
                    error_case, error_message = _make_failed_load_tests(module.__name__, e, self.suiteClass)
                    self.errors.append(error_message)
                    return error_case
                finally:
                    e = None
                    del e

            return tests

    def loadTestsFromName--- This code section failed: ---

 L. 147         0  LOAD_FAST                'name'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'parts'

 L. 148        10  LOAD_CONST               (None, None)
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'error_case'
               16  STORE_FAST               'error_message'

 L. 149        18  LOAD_FAST                'module'
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE   150  'to 150'

 L. 150        26  LOAD_FAST                'parts'
               28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  STORE_FAST               'parts_copy'

 L. 151        38  SETUP_LOOP          138  'to 138'
             40_0  COME_FROM           134  '134'
             40_1  COME_FROM           130  '130'
             40_2  COME_FROM            68  '68'
               40  LOAD_FAST                'parts_copy'
               42  POP_JUMP_IF_FALSE   136  'to 136'

 L. 152        44  SETUP_EXCEPT         70  'to 70'

 L. 153        46  LOAD_STR                 '.'
               48  LOAD_METHOD              join
               50  LOAD_FAST                'parts_copy'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  STORE_FAST               'module_name'

 L. 154        56  LOAD_GLOBAL              __import__
               58  LOAD_FAST                'module_name'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  STORE_FAST               'module'

 L. 155        64  BREAK_LOOP       
               66  POP_BLOCK        
               68  JUMP_BACK            40  'to 40'
             70_0  COME_FROM_EXCEPT     44  '44'

 L. 156        70  DUP_TOP          
               72  LOAD_GLOBAL              ImportError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   132  'to 132'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 157        84  LOAD_FAST                'parts_copy'
               86  LOAD_METHOD              pop
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  STORE_FAST               'next_attribute'

 L. 159        92  LOAD_GLOBAL              _make_failed_import_test

 L. 160        94  LOAD_FAST                'next_attribute'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                suiteClass
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'error_case'
              106  STORE_FAST               'error_message'

 L. 161       108  LOAD_FAST                'parts_copy'
              110  POP_JUMP_IF_TRUE    128  'to 128'

 L. 163       112  LOAD_FAST                'self'
              114  LOAD_ATTR                errors
              116  LOAD_METHOD              append
              118  LOAD_FAST                'error_message'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          

 L. 164       124  LOAD_FAST                'error_case'
              126  RETURN_VALUE     
            128_0  COME_FROM           110  '110'
              128  POP_EXCEPT       
              130  JUMP_BACK            40  'to 40'
            132_0  COME_FROM            76  '76'
              132  END_FINALLY      
              134  JUMP_BACK            40  'to 40'
            136_0  COME_FROM            42  '42'
              136  POP_BLOCK        
            138_0  COME_FROM_LOOP       38  '38'

 L. 165       138  LOAD_FAST                'parts'
              140  LOAD_CONST               1
              142  LOAD_CONST               None
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  STORE_FAST               'parts'
            150_0  COME_FROM            24  '24'

 L. 166       150  LOAD_FAST                'module'
              152  STORE_FAST               'obj'

 L. 167       154  SETUP_LOOP          312  'to 312'
              156  LOAD_FAST                'parts'
              158  GET_ITER         
            160_0  COME_FROM           308  '308'
            160_1  COME_FROM           304  '304'
            160_2  COME_FROM           184  '184'
              160  FOR_ITER            310  'to 310'
              162  STORE_FAST               'part'

 L. 168       164  SETUP_EXCEPT        186  'to 186'

 L. 169       166  LOAD_FAST                'obj'
              168  LOAD_GLOBAL              getattr
              170  LOAD_FAST                'obj'
              172  LOAD_FAST                'part'
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  ROT_TWO          
              178  STORE_FAST               'parent'
              180  STORE_FAST               'obj'
              182  POP_BLOCK        
              184  JUMP_BACK           160  'to 160'
            186_0  COME_FROM_EXCEPT    164  '164'

 L. 170       186  DUP_TOP          
              188  LOAD_GLOBAL              AttributeError
              190  COMPARE_OP               exception-match
          192_194  POP_JUMP_IF_FALSE   306  'to 306'
              196  POP_TOP          
              198  STORE_FAST               'e'
              200  POP_TOP          
              202  SETUP_FINALLY       294  'to 294'

 L. 172       204  LOAD_GLOBAL              getattr
              206  LOAD_FAST                'obj'
              208  LOAD_STR                 '__path__'
              210  LOAD_CONST               None
              212  CALL_FUNCTION_3       3  '3 positional arguments'
              214  LOAD_CONST               None
              216  COMPARE_OP               is-not
              218  POP_JUMP_IF_FALSE   244  'to 244'

 L. 173       220  LOAD_FAST                'error_case'
              222  LOAD_CONST               None
              224  COMPARE_OP               is-not
              226  POP_JUMP_IF_FALSE   244  'to 244'

 L. 179       228  LOAD_FAST                'self'
              230  LOAD_ATTR                errors
              232  LOAD_METHOD              append
              234  LOAD_FAST                'error_message'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  POP_TOP          

 L. 180       240  LOAD_FAST                'error_case'
              242  RETURN_VALUE     
            244_0  COME_FROM           226  '226'
            244_1  COME_FROM           218  '218'

 L. 183       244  LOAD_GLOBAL              _make_failed_test

 L. 184       246  LOAD_FAST                'part'
              248  LOAD_FAST                'e'
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                suiteClass

 L. 185       254  LOAD_STR                 'Failed to access attribute:\n%s'

 L. 186       256  LOAD_GLOBAL              traceback
              258  LOAD_METHOD              format_exc
              260  CALL_METHOD_0         0  '0 positional arguments'
              262  BUILD_TUPLE_1         1 
              264  BINARY_MODULO    
              266  CALL_FUNCTION_4       4  '4 positional arguments'
              268  UNPACK_SEQUENCE_2     2 
              270  STORE_FAST               'error_case'
              272  STORE_FAST               'error_message'

 L. 187       274  LOAD_FAST                'self'
              276  LOAD_ATTR                errors
              278  LOAD_METHOD              append
              280  LOAD_FAST                'error_message'
              282  CALL_METHOD_1         1  '1 positional argument'
              284  POP_TOP          

 L. 188       286  LOAD_FAST                'error_case'
              288  RETURN_VALUE     
              290  POP_BLOCK        
              292  LOAD_CONST               None
            294_0  COME_FROM_FINALLY   202  '202'
              294  LOAD_CONST               None
              296  STORE_FAST               'e'
              298  DELETE_FAST              'e'
              300  END_FINALLY      
              302  POP_EXCEPT       
              304  JUMP_BACK           160  'to 160'
            306_0  COME_FROM           192  '192'
              306  END_FINALLY      
              308  JUMP_BACK           160  'to 160'
              310  POP_BLOCK        
            312_0  COME_FROM_LOOP      154  '154'

 L. 190       312  LOAD_GLOBAL              isinstance
              314  LOAD_FAST                'obj'
              316  LOAD_GLOBAL              types
              318  LOAD_ATTR                ModuleType
              320  CALL_FUNCTION_2       2  '2 positional arguments'
          322_324  POP_JUMP_IF_FALSE   336  'to 336'

 L. 191       326  LOAD_FAST                'self'
              328  LOAD_METHOD              loadTestsFromModule
              330  LOAD_FAST                'obj'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  RETURN_VALUE     
            336_0  COME_FROM           322  '322'

 L. 192       336  LOAD_GLOBAL              isinstance
              338  LOAD_FAST                'obj'
              340  LOAD_GLOBAL              type
              342  CALL_FUNCTION_2       2  '2 positional arguments'
          344_346  POP_JUMP_IF_FALSE   372  'to 372'
              348  LOAD_GLOBAL              issubclass
              350  LOAD_FAST                'obj'
              352  LOAD_GLOBAL              case
              354  LOAD_ATTR                TestCase
              356  CALL_FUNCTION_2       2  '2 positional arguments'
          358_360  POP_JUMP_IF_FALSE   372  'to 372'

 L. 193       362  LOAD_FAST                'self'
              364  LOAD_METHOD              loadTestsFromTestCase
              366  LOAD_FAST                'obj'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  RETURN_VALUE     
            372_0  COME_FROM           358  '358'
            372_1  COME_FROM           344  '344'

 L. 194       372  LOAD_GLOBAL              isinstance
              374  LOAD_FAST                'obj'
              376  LOAD_GLOBAL              types
              378  LOAD_ATTR                FunctionType
              380  CALL_FUNCTION_2       2  '2 positional arguments'
          382_384  POP_JUMP_IF_FALSE   462  'to 462'

 L. 195       386  LOAD_GLOBAL              isinstance
              388  LOAD_FAST                'parent'
              390  LOAD_GLOBAL              type
              392  CALL_FUNCTION_2       2  '2 positional arguments'
          394_396  POP_JUMP_IF_FALSE   462  'to 462'

 L. 196       398  LOAD_GLOBAL              issubclass
              400  LOAD_FAST                'parent'
              402  LOAD_GLOBAL              case
              404  LOAD_ATTR                TestCase
              406  CALL_FUNCTION_2       2  '2 positional arguments'
          408_410  POP_JUMP_IF_FALSE   462  'to 462'

 L. 197       412  LOAD_FAST                'parts'
              414  LOAD_CONST               -1
              416  BINARY_SUBSCR    
              418  STORE_FAST               'name'

 L. 198       420  LOAD_FAST                'parent'
              422  LOAD_FAST                'name'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  STORE_FAST               'inst'

 L. 200       428  LOAD_GLOBAL              isinstance
              430  LOAD_GLOBAL              getattr
              432  LOAD_FAST                'inst'
              434  LOAD_FAST                'name'
              436  CALL_FUNCTION_2       2  '2 positional arguments'
              438  LOAD_GLOBAL              types
              440  LOAD_ATTR                FunctionType
              442  CALL_FUNCTION_2       2  '2 positional arguments'
          444_446  POP_JUMP_IF_TRUE    480  'to 480'

 L. 201       448  LOAD_FAST                'self'
              450  LOAD_METHOD              suiteClass
              452  LOAD_FAST                'inst'
              454  BUILD_LIST_1          1 
              456  CALL_METHOD_1         1  '1 positional argument'
              458  RETURN_VALUE     
              460  JUMP_FORWARD        480  'to 480'
            462_0  COME_FROM           408  '408'
            462_1  COME_FROM           394  '394'
            462_2  COME_FROM           382  '382'

 L. 202       462  LOAD_GLOBAL              isinstance
              464  LOAD_FAST                'obj'
              466  LOAD_GLOBAL              suite
              468  LOAD_ATTR                TestSuite
              470  CALL_FUNCTION_2       2  '2 positional arguments'
          472_474  POP_JUMP_IF_FALSE   480  'to 480'

 L. 203       476  LOAD_FAST                'obj'
              478  RETURN_VALUE     
            480_0  COME_FROM           472  '472'
            480_1  COME_FROM           460  '460'
            480_2  COME_FROM           444  '444'

 L. 204       480  LOAD_GLOBAL              callable
              482  LOAD_FAST                'obj'
              484  CALL_FUNCTION_1       1  '1 positional argument'
          486_488  POP_JUMP_IF_FALSE   558  'to 558'

 L. 205       490  LOAD_FAST                'obj'
              492  CALL_FUNCTION_0       0  '0 positional arguments'
              494  STORE_FAST               'test'

 L. 206       496  LOAD_GLOBAL              isinstance
              498  LOAD_FAST                'test'
              500  LOAD_GLOBAL              suite
              502  LOAD_ATTR                TestSuite
              504  CALL_FUNCTION_2       2  '2 positional arguments'
          506_508  POP_JUMP_IF_FALSE   514  'to 514'

 L. 207       510  LOAD_FAST                'test'
              512  RETURN_VALUE     
            514_0  COME_FROM           506  '506'

 L. 208       514  LOAD_GLOBAL              isinstance
              516  LOAD_FAST                'test'
              518  LOAD_GLOBAL              case
              520  LOAD_ATTR                TestCase
              522  CALL_FUNCTION_2       2  '2 positional arguments'
          524_526  POP_JUMP_IF_FALSE   540  'to 540'

 L. 209       528  LOAD_FAST                'self'
              530  LOAD_METHOD              suiteClass
              532  LOAD_FAST                'test'
              534  BUILD_LIST_1          1 
              536  CALL_METHOD_1         1  '1 positional argument'
              538  RETURN_VALUE     
            540_0  COME_FROM           524  '524'

 L. 211       540  LOAD_GLOBAL              TypeError
              542  LOAD_STR                 'calling %s returned %s, not a test'

 L. 212       544  LOAD_FAST                'obj'
              546  LOAD_FAST                'test'
              548  BUILD_TUPLE_2         2 
              550  BINARY_MODULO    
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  RAISE_VARARGS_1       1  'exception instance'
              556  JUMP_FORWARD        570  'to 570'
            558_0  COME_FROM           486  '486'

 L. 214       558  LOAD_GLOBAL              TypeError
              560  LOAD_STR                 "don't know how to make test from: %s"
              562  LOAD_FAST                'obj'
              564  BINARY_MODULO    
              566  CALL_FUNCTION_1       1  '1 positional argument'
              568  RAISE_VARARGS_1       1  'exception instance'
            570_0  COME_FROM           556  '556'

Parse error at or near `LOAD_GLOBAL' instruction at offset 480

    def loadTestsFromNames(self, names, module=None):
        """Return a suite of all test cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = [self.loadTestsFromName(name, module) for name in names]
        return self.suiteClass(suites)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """

        def shouldIncludeMethod(attrname):
            if not attrname.startswith(self.testMethodPrefix):
                return False
            testFunc = getattr(testCaseClass, attrname)
            if not callable(testFunc):
                return False
            fullName = '%s.%s.%s' % (
             testCaseClass.__module__, testCaseClass.__qualname__, attrname)
            return self.testNamePatterns is None or any((fnmatchcase(fullName, pattern) for pattern in self.testNamePatterns))

        testFnNames = list(filter(shouldIncludeMethod, dir(testCaseClass)))
        if self.sortTestMethodsUsing:
            testFnNames.sort(key=(functools.cmp_to_key(self.sortTestMethodsUsing)))
        return testFnNames

    def discover(self, start_dir, pattern='test*.py', top_level_dir=None):
        """Find and return all test modules from the specified start
        directory, recursing into subdirectories to find them and return all
        tests found within them. Only test files that match the pattern will
        be loaded. (Using shell style pattern matching.)

        All test modules must be importable from the top level of the project.
        If the start directory is not the top level directory then the top
        level directory must be specified separately.

        If a test package name (directory with '__init__.py') matches the
        pattern then the package will be checked for a 'load_tests' function. If
        this exists then it will be called with (loader, tests, pattern) unless
        the package has already had load_tests called from the same discovery
        invocation, in which case the package module object is not scanned for
        tests - this ensures that when a package uses discover to further
        discover child tests that infinite recursion does not happen.

        If load_tests exists then discovery does *not* recurse into the package,
        load_tests is responsible for loading all tests in the package.

        The pattern is deliberately not stored as a loader attribute so that
        packages can continue discovery themselves. top_level_dir is stored so
        load_tests does not need to pass this argument in to loader.discover().

        Paths are sorted before being imported to ensure reproducible execution
        order even on filesystems with non-alphabetical ordering like ext3/4.
        """
        set_implicit_top = False
        if top_level_dir is None and self._top_level_dir is not None:
            top_level_dir = self._top_level_dir
        elif top_level_dir is None:
            set_implicit_top = True
            top_level_dir = start_dir
        top_level_dir = os.path.abspath(top_level_dir)
        if top_level_dir not in sys.path:
            sys.path.insert(0, top_level_dir)
        self._top_level_dir = top_level_dir
        is_not_importable = False
        is_namespace = False
        tests = []
        if os.path.isdir(os.path.abspath(start_dir)):
            start_dir = os.path.abspath(start_dir)
            if start_dir != top_level_dir:
                is_not_importable = not os.path.isfile(os.path.join(start_dir, '__init__.py'))
        else:
            try:
                __import__(start_dir)
            except ImportError:
                is_not_importable = True
            else:
                the_module = sys.modules[start_dir]
                top_part = start_dir.split('.')[0]
                try:
                    start_dir = os.path.abspath(os.path.dirname(the_module.__file__))
                except AttributeError:
                    try:
                        spec = the_module.__spec__
                    except AttributeError:
                        spec = None

                    if spec and spec.loader is None:
                        if spec.submodule_search_locations is not None:
                            is_namespace = True
                            for path in the_module.__path__:
                                if not set_implicit_top:
                                    if not path.startswith(top_level_dir):
                                        continue
                                self._top_level_dir = path.split(the_module.__name__.replace('.', os.path.sep))[0]
                                tests.extend(self._find_tests(path, pattern,
                                  namespace=True))

                    elif the_module.__name__ in sys.builtin_module_names:
                        raise TypeError('Can not use builtin modules as dotted module names') from None
                    else:
                        raise TypeError("don't know how to discover from {!r}".format(the_module)) from None

                if set_implicit_top:
                    if not is_namespace:
                        self._top_level_dir = self._get_directory_containing_module(top_part)
                        sys.path.remove(top_level_dir)
                    else:
                        sys.path.remove(top_level_dir)

        if is_not_importable:
            raise ImportError('Start directory is not importable: %r' % start_dir)
        if not is_namespace:
            tests = list(self._find_tests(start_dir, pattern))
        return self.suiteClass(tests)

    def _get_directory_containing_module(self, module_name):
        module = sys.modules[module_name]
        full_path = os.path.abspath(module.__file__)
        if os.path.basename(full_path).lower().startswith('__init__.py'):
            return os.path.dirname(os.path.dirname(full_path))
        return os.path.dirname(full_path)

    def _get_name_from_path(self, path):
        if path == self._top_level_dir:
            return '.'
        path = _jython_aware_splitext(os.path.normpath(path))
        _relpath = os.path.relpath(path, self._top_level_dir)
        if os.path.isabs(_relpath):
            raise AssertionError('Path must be within the project')
        if _relpath.startswith('..'):
            raise AssertionError('Path must be within the project')
        name = _relpath.replace(os.path.sep, '.')
        return name

    def _get_module_from_name(self, name):
        __import__(name)
        return sys.modules[name]

    def _match_path(self, path, full_path, pattern):
        return fnmatch(path, pattern)

    def _find_tests(self, start_dir, pattern, namespace=False):
        """Used by discovery. Yields test suites it loads."""
        name = self._get_name_from_path(start_dir)
        if name != '.':
            if name not in self._loading_packages:
                tests, should_recurse = self._find_test_path(start_dir, pattern, namespace)
                if tests is not None:
                    yield tests
                if not should_recurse:
                    return
                paths = sorted(os.listdir(start_dir))
                for path in paths:
                    full_path = os.path.join(start_dir, path)
                    tests, should_recurse = self._find_test_path(full_path, pattern, namespace)
                    if tests is not None:
                        yield tests
                    if should_recurse:
                        name = self._get_name_from_path(full_path)
                        self._loading_packages.add(name)
                        try:
                            yield from self._find_tests(full_path, pattern, namespace)
                        finally:
                            self._loading_packages.discard(name)

    def _find_test_path(self, full_path, pattern, namespace=False):
        """Used by discovery.

        Loads tests from a single file, or a directories' __init__.py when
        passed the directory.

        Returns a tuple (None_or_tests_from_file, should_recurse).
        """
        basename = os.path.basename(full_path)
        if os.path.isfile(full_path):
            if not VALID_MODULE_NAME.match(basename):
                return (None, False)
            if not self._match_path(basename, full_path, pattern):
                return (None, False)
            name = self._get_name_from_path(full_path)
            try:
                module = self._get_module_from_name(name)
            except case.SkipTest as e:
                try:
                    return (
                     _make_skipped_test(name, e, self.suiteClass), False)
                finally:
                    e = None
                    del e

            except:
                error_case, error_message = _make_failed_import_test(name, self.suiteClass)
                self.errors.append(error_message)
                return (
                 error_case, False)
            else:
                mod_file = os.path.abspath(getattr(module, '__file__', full_path))
                realpath = _jython_aware_splitext(os.path.realpath(mod_file))
                fullpath_noext = _jython_aware_splitext(os.path.realpath(full_path))
                if realpath.lower() != fullpath_noext.lower():
                    module_dir = os.path.dirname(realpath)
                    mod_name = _jython_aware_splitext(os.path.basename(full_path))
                    expected_dir = os.path.dirname(full_path)
                    msg = '%r module incorrectly imported from %r. Expected %r. Is this module globally installed?'
                    raise ImportError(msg % (mod_name, module_dir, expected_dir))
                return (self.loadTestsFromModule(module, pattern=pattern), False)

        elif os.path.isdir(full_path):
            if not namespace:
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    return (None, False)
            load_tests = None
            tests = None
            name = self._get_name_from_path(full_path)
            try:
                package = self._get_module_from_name(name)
            except case.SkipTest as e:
                try:
                    return (
                     _make_skipped_test(name, e, self.suiteClass), False)
                finally:
                    e = None
                    del e

            except:
                error_case, error_message = _make_failed_import_test(name, self.suiteClass)
                self.errors.append(error_message)
                return (
                 error_case, False)
            else:
                load_tests = getattr(package, 'load_tests', None)
                self._loading_packages.add(name)
                try:
                    tests = self.loadTestsFromModule(package, pattern=pattern)
                    if load_tests is not None:
                        return (
                         tests, False)
                    return (tests, True)
                finally:
                    self._loading_packages.discard(name)

        else:
            return (None, False)


defaultTestLoader = TestLoader()

def _makeLoader(prefix, sortUsing, suiteClass=None, testNamePatterns=None):
    loader = TestLoader()
    loader.sortTestMethodsUsing = sortUsing
    loader.testMethodPrefix = prefix
    loader.testNamePatterns = testNamePatterns
    if suiteClass:
        loader.suiteClass = suiteClass
    return loader


def getTestCaseNames(testCaseClass, prefix, sortUsing=util.three_way_cmp, testNamePatterns=None):
    return _makeLoader(prefix, sortUsing, testNamePatterns=testNamePatterns).getTestCaseNames(testCaseClass)


def makeSuite(testCaseClass, prefix='test', sortUsing=util.three_way_cmp, suiteClass=suite.TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromTestCase(testCaseClass)


def findTestCases(module, prefix='test', sortUsing=util.three_way_cmp, suiteClass=suite.TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromModule(module)