# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\result.py
"""Test result object"""
import io, sys, traceback
from . import util
from functools import wraps
__unittest = True

def failfast(method):

    @wraps(method)
    def inner--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'failfast'
                6  LOAD_CONST               False
                8  CALL_FUNCTION_3       3  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  16        12  LOAD_FAST                'self'
               14  LOAD_METHOD              stop
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          
             20_0  COME_FROM            10  '10'

 L.  17        20  LOAD_DEREF               'method'
               22  LOAD_FAST                'self'
               24  BUILD_LIST_1          1 
               26  LOAD_FAST                'args'
               28  CALL_FINALLY         31  'to 31'
               30  WITH_CLEANUP_FINISH
               32  BUILD_MAP_0           0 
               34  LOAD_FAST                'kw'
               36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 28

    return inner


STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'

class TestResult(object):
    __doc__ = 'Holder for test result information.\n\n    Test results are automatically managed by the TestCase and TestSuite\n    classes, and do not need to be explicitly manipulated by writers of tests.\n\n    Each instance holds the total number of tests run, and collections of\n    failures and errors that occurred among those test runs. The collections\n    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the\n    formatted traceback of the error that occurred.\n    '
    _previousTestClass = None
    _testRunEntered = False
    _moduleSetUpFailed = False

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self.tb_locals = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False

    def printErrors(self):
        """Called by TestRunner after test run"""
        pass

    def startTest(self, test):
        """Called when the given test is about to be run"""
        self.testsRun += 1
        self._mirrorOutput = False
        self._setupStdout

    def _setupStdout--- This code section failed: ---

 L.  65         0  LOAD_FAST                'self'
                2  LOAD_ATTR                buffer
                4  POP_JUMP_IF_FALSE    52  'to 52'

 L.  66         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _stderr_buffer
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    36  'to 36'

 L.  67        16  LOAD_GLOBAL              io
               18  LOAD_METHOD              StringIO
               20  CALL_METHOD_0         0  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _stderr_buffer

 L.  68        26  LOAD_GLOBAL              io
               28  LOAD_METHOD              StringIO
               30  CALL_METHOD_0         0  ''
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _stdout_buffer
             36_0  COME_FROM            14  '14'

 L.  69        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _stdout_buffer
               40  LOAD_GLOBAL              sys
               42  STORE_ATTR               stdout

 L.  70        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _stderr_buffer
               48  LOAD_GLOBAL              sys
               50  STORE_ATTR               stderr
             52_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 12

    def startTestRun(self):
        """Called once before any tests are executed.

        See startTest for a method called before each test.
        """
        pass

    def stopTest(self, test):
        """Called when the given test has been run"""
        self._restoreStdout
        self._mirrorOutput = False

    def _restoreStdout(self):
        if self.buffer:
            if self._mirrorOutput:
                output = sys.stdout.getvalue
                error = sys.stderr.getvalue
                if output:
                    if not output.endswith('\n'):
                        output += '\n'
                    self._original_stdout.write(STDOUT_LINE % output)
                if error:
                    if not error.endswith('\n'):
                        error += '\n'
                    self._original_stderr.write(STDERR_LINE % error)
            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._stdout_buffer.seek(0)
            self._stdout_buffer.truncate
            self._stderr_buffer.seek(0)
            self._stderr_buffer.truncate

    def stopTestRun(self):
        """Called once after all tests are executed.

        See stopTest for a method called after each test.
        """
        pass

    @failfast
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    @failfast
    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True

    def addSubTest--- This code section failed: ---

 L. 132         0  LOAD_FAST                'err'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    86  'to 86'

 L. 133         8  LOAD_GLOBAL              getattr
               10  LOAD_FAST                'self'
               12  LOAD_STR                 'failfast'
               14  LOAD_CONST               False
               16  CALL_FUNCTION_3       3  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 134        20  LOAD_FAST                'self'
               22  LOAD_METHOD              stop
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          
             28_0  COME_FROM            18  '18'

 L. 135        28  LOAD_GLOBAL              issubclass
               30  LOAD_FAST                'err'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_FAST                'test'
               38  LOAD_ATTR                failureException
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 136        44  LOAD_FAST                'self'
               46  LOAD_ATTR                failures
               48  STORE_FAST               'errors'
               50  JUMP_FORWARD         58  'to 58'
             52_0  COME_FROM            42  '42'

 L. 138        52  LOAD_FAST                'self'
               54  LOAD_ATTR                errors
               56  STORE_FAST               'errors'
             58_0  COME_FROM            50  '50'

 L. 139        58  LOAD_FAST                'errors'
               60  LOAD_METHOD              append
               62  LOAD_FAST                'subtest'
               64  LOAD_FAST                'self'
               66  LOAD_METHOD              _exc_info_to_string
               68  LOAD_FAST                'err'
               70  LOAD_FAST                'test'
               72  CALL_METHOD_2         2  ''
               74  BUILD_TUPLE_2         2 
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 140        80  LOAD_CONST               True
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _mirrorOutput
             86_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1

    def addSuccess(self, test):
        """Called when a test has completed successfully"""
        pass

    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.skipped.append((test, reason))

    def addExpectedFailure(self, test, err):
        """Called when an expected failure/error occurred."""
        self.expectedFailures.append((
         test, self._exc_info_to_string(err, test)))

    @failfast
    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)

    def wasSuccessful(self):
        """Tells whether or not this result was a success."""
        return len(self.failures) == len(self.errors) == 0 and (not hasattrself'unexpectedSuccesses' or len(self.unexpectedSuccesses) == 0)

    def stop(self):
        """Indicates that the tests should be aborted."""
        self.shouldStop = True

    def _exc_info_to_string--- This code section failed: ---

 L. 175         0  LOAD_FAST                'err'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'exctype'
                6  STORE_FAST               'value'
                8  STORE_FAST               'tb'

 L. 177        10  LOAD_FAST                'tb'
               12  POP_JUMP_IF_FALSE    32  'to 32'
               14  LOAD_FAST                'self'
               16  LOAD_METHOD              _is_relevant_tb_level
               18  LOAD_FAST                'tb'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 178        24  LOAD_FAST                'tb'
               26  LOAD_ATTR                tb_next
               28  STORE_FAST               'tb'
               30  JUMP_BACK            10  'to 10'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            12  '12'

 L. 180        32  LOAD_FAST                'exctype'
               34  LOAD_FAST                'test'
               36  LOAD_ATTR                failureException
               38  <117>                 0  ''
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L. 182        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _count_relevant_tb_levels
               46  LOAD_FAST                'tb'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'length'
               52  JUMP_FORWARD         58  'to 58'
             54_0  COME_FROM            40  '40'

 L. 184        54  LOAD_CONST               None
               56  STORE_FAST               'length'
             58_0  COME_FROM            52  '52'

 L. 185        58  LOAD_GLOBAL              traceback
               60  LOAD_ATTR                TracebackException

 L. 186        62  LOAD_FAST                'exctype'
               64  LOAD_FAST                'value'
               66  LOAD_FAST                'tb'
               68  LOAD_FAST                'length'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                tb_locals

 L. 185        74  LOAD_CONST               ('limit', 'capture_locals')
               76  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               78  STORE_FAST               'tb_e'

 L. 187        80  LOAD_GLOBAL              list
               82  LOAD_FAST                'tb_e'
               84  LOAD_METHOD              format
               86  CALL_METHOD_0         0  ''
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'msgLines'

 L. 189        92  LOAD_FAST                'self'
               94  LOAD_ATTR                buffer
               96  POP_JUMP_IF_FALSE   190  'to 190'

 L. 190        98  LOAD_GLOBAL              sys
              100  LOAD_ATTR                stdout
              102  LOAD_METHOD              getvalue
              104  CALL_METHOD_0         0  ''
              106  STORE_FAST               'output'

 L. 191       108  LOAD_GLOBAL              sys
              110  LOAD_ATTR                stderr
              112  LOAD_METHOD              getvalue
              114  CALL_METHOD_0         0  ''
              116  STORE_FAST               'error'

 L. 192       118  LOAD_FAST                'output'
              120  POP_JUMP_IF_FALSE   154  'to 154'

 L. 193       122  LOAD_FAST                'output'
              124  LOAD_METHOD              endswith
              126  LOAD_STR                 '\n'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_TRUE    140  'to 140'

 L. 194       132  LOAD_FAST                'output'
              134  LOAD_STR                 '\n'
              136  INPLACE_ADD      
              138  STORE_FAST               'output'
            140_0  COME_FROM           130  '130'

 L. 195       140  LOAD_FAST                'msgLines'
              142  LOAD_METHOD              append
              144  LOAD_GLOBAL              STDOUT_LINE
              146  LOAD_FAST                'output'
              148  BINARY_MODULO    
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
            154_0  COME_FROM           120  '120'

 L. 196       154  LOAD_FAST                'error'
              156  POP_JUMP_IF_FALSE   190  'to 190'

 L. 197       158  LOAD_FAST                'error'
              160  LOAD_METHOD              endswith
              162  LOAD_STR                 '\n'
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_TRUE    176  'to 176'

 L. 198       168  LOAD_FAST                'error'
              170  LOAD_STR                 '\n'
              172  INPLACE_ADD      
              174  STORE_FAST               'error'
            176_0  COME_FROM           166  '166'

 L. 199       176  LOAD_FAST                'msgLines'
              178  LOAD_METHOD              append
              180  LOAD_GLOBAL              STDERR_LINE
              182  LOAD_FAST                'error'
              184  BINARY_MODULO    
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
            190_0  COME_FROM           156  '156'
            190_1  COME_FROM            96  '96'

 L. 200       190  LOAD_STR                 ''
              192  LOAD_METHOD              join
              194  LOAD_FAST                'msgLines'
              196  CALL_METHOD_1         1  ''
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 38

    def _is_relevant_tb_level--- This code section failed: ---

 L. 204         0  LOAD_STR                 '__unittest'
                2  LOAD_FAST                'tb'
                4  LOAD_ATTR                tb_frame
                6  LOAD_ATTR                f_globals
                8  <118>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb:
            if not self._is_relevant_tb_level(tb):
                length += 1
                tb = tb.tb_next

        return length

    def __repr__(self):
        return '<%s run=%i errors=%i failures=%i>' % (
         util.strclass(self.__class__), self.testsRun, len(self.errors),
         len(self.failures))