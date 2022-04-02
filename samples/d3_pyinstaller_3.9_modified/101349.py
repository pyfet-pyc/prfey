# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\suite.py
"""TestSuite"""
import sys
from . import case
from . import util
__unittest = True

def _call_if_exists(parent, attr):
    func = getattr(parent, attr, lambda: None)
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
        else:
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
            else:
                test(result)
            if self._cleanup:
                self._removeTestAtIndex(index)
        else:
            return result

    def _removeTestAtIndex--- This code section failed: ---

 L.  71         0  SETUP_FINALLY        16  'to 16'

 L.  72         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _tests
                6  LOAD_FAST                'index'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'test'
               12  POP_BLOCK        
               14  JUMP_FORWARD         34  'to 34'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  73        16  DUP_TOP          
               18  LOAD_GLOBAL              TypeError
               20  <121>                32  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  75        28  POP_EXCEPT       
               30  JUMP_FORWARD         72  'to 72'
               32  <48>             
             34_0  COME_FROM            14  '14'

 L.  79        34  LOAD_GLOBAL              hasattr
               36  LOAD_FAST                'test'
               38  LOAD_STR                 'countTestCases'
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    62  'to 62'

 L.  80        44  LOAD_FAST                'self'
               46  DUP_TOP          
               48  LOAD_ATTR                _removed_tests
               50  LOAD_FAST                'test'
               52  LOAD_METHOD              countTestCases
               54  CALL_METHOD_0         0  ''
               56  INPLACE_ADD      
               58  ROT_TWO          
               60  STORE_ATTR               _removed_tests
             62_0  COME_FROM            42  '42'

 L.  81        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _tests
               68  LOAD_FAST                'index'
               70  STORE_SUBSCR     
             72_0  COME_FROM            30  '30'

Parse error at or near `<121>' instruction at offset 20

    def __call__--- This code section failed: ---

 L.  84         0  LOAD_FAST                'self'
                2  LOAD_ATTR                run
                4  LOAD_FAST                'args'
                6  BUILD_MAP_0           0 
                8  LOAD_FAST                'kwds'
               10  <164>                 1  ''
               12  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

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
               16  <117>                 0  ''
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
             38_0  COME_FROM           174  '174'
             38_1  COME_FROM           162  '162'
             38_2  COME_FROM           134  '134'
             38_3  COME_FROM           120  '120'
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
              120  POP_JUMP_IF_TRUE_BACK    38  'to 38'

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
              162  POP_JUMP_IF_FALSE_BACK    38  'to 38'

 L. 127       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _removeTestAtIndex
              168  LOAD_FAST                'index'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_BACK            38  'to 38'
            176_0  COME_FROM            54  '54'
            176_1  COME_FROM            38  '38'

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

Parse error at or near `<117>' instruction at offset 16

    def debug(self):
        """Run the tests without collecting errors in a TestResult"""
        debug = _DebugResult()
        self.rundebugTrue

    def _handleClassSetUp--- This code section failed: ---

 L. 143         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'result'
                4  LOAD_STR                 '_previousTestClass'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'previousClass'

 L. 144        12  LOAD_FAST                'test'
               14  LOAD_ATTR                __class__
               16  STORE_FAST               'currentClass'

 L. 145        18  LOAD_FAST                'currentClass'
               20  LOAD_FAST                'previousClass'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 146        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 147        30  LOAD_FAST                'result'
               32  LOAD_ATTR                _moduleSetUpFailed
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 148        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'

 L. 149        40  LOAD_GLOBAL              getattr
               42  LOAD_FAST                'currentClass'
               44  LOAD_STR                 '__unittest_skip__'
               46  LOAD_CONST               False
               48  CALL_FUNCTION_3       3  ''
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 150        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 152        56  SETUP_FINALLY        68  'to 68'

 L. 153        58  LOAD_CONST               False
               60  LOAD_FAST                'currentClass'
               62  STORE_ATTR               _classSetupFailed
               64  POP_BLOCK        
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM_FINALLY    56  '56'

 L. 154        68  DUP_TOP          
               70  LOAD_GLOBAL              TypeError
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 157        80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            66  '66'

 L. 159        86  LOAD_GLOBAL              getattr
               88  LOAD_FAST                'currentClass'
               90  LOAD_STR                 'setUpClass'
               92  LOAD_CONST               None
               94  CALL_FUNCTION_3       3  ''
               96  STORE_FAST               'setUpClass'

 L. 160        98  LOAD_FAST                'setUpClass'
              100  LOAD_CONST               None
              102  <117>                 1  ''
          104_106  POP_JUMP_IF_FALSE   386  'to 386'

 L. 161       108  LOAD_GLOBAL              _call_if_exists
              110  LOAD_FAST                'result'
              112  LOAD_STR                 '_setupStdout'
              114  CALL_FUNCTION_2       2  ''
              116  POP_TOP          

 L. 162       118  SETUP_FINALLY       300  'to 300'
              120  SETUP_FINALLY       132  'to 132'

 L. 163       122  LOAD_FAST                'setUpClass'
              124  CALL_FUNCTION_0       0  ''
              126  POP_TOP          
              128  POP_BLOCK        
              130  JUMP_FORWARD        212  'to 212'
            132_0  COME_FROM_FINALLY   120  '120'

 L. 164       132  DUP_TOP          
              134  LOAD_GLOBAL              Exception
              136  <121>               210  ''
              138  POP_TOP          
              140  STORE_FAST               'e'
              142  POP_TOP          
              144  SETUP_FINALLY       202  'to 202'

 L. 165       146  LOAD_GLOBAL              isinstance
              148  LOAD_FAST                'result'
              150  LOAD_GLOBAL              _DebugResult
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_FALSE   158  'to 158'

 L. 166       156  RAISE_VARARGS_0       0  'reraise'
            158_0  COME_FROM           154  '154'

 L. 167       158  LOAD_CONST               True
              160  LOAD_FAST                'currentClass'
              162  STORE_ATTR               _classSetupFailed

 L. 168       164  LOAD_GLOBAL              util
              166  LOAD_METHOD              strclass
              168  LOAD_FAST                'currentClass'
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'className'

 L. 169       174  LOAD_FAST                'self'
              176  LOAD_METHOD              _createClassOrModuleLevelException
              178  LOAD_FAST                'result'
              180  LOAD_FAST                'e'

 L. 170       182  LOAD_STR                 'setUpClass'

 L. 171       184  LOAD_FAST                'className'

 L. 169       186  CALL_METHOD_4         4  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  POP_EXCEPT       
              194  LOAD_CONST               None
              196  STORE_FAST               'e'
              198  DELETE_FAST              'e'
              200  JUMP_FORWARD        212  'to 212'
            202_0  COME_FROM_FINALLY   144  '144'
              202  LOAD_CONST               None
              204  STORE_FAST               'e'
              206  DELETE_FAST              'e'
              208  <48>             
              210  <48>             
            212_0  COME_FROM           200  '200'
            212_1  COME_FROM           130  '130'
              212  POP_BLOCK        

 L. 173       214  LOAD_GLOBAL              _call_if_exists
              216  LOAD_FAST                'result'
              218  LOAD_STR                 '_restoreStdout'
              220  CALL_FUNCTION_2       2  ''
              222  POP_TOP          

 L. 174       224  LOAD_FAST                'currentClass'
              226  LOAD_ATTR                _classSetupFailed
              228  LOAD_CONST               True
              230  <117>                 0  ''
          232_234  POP_JUMP_IF_FALSE   386  'to 386'

 L. 175       236  LOAD_FAST                'currentClass'
              238  LOAD_METHOD              doClassCleanups
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          

 L. 176       244  LOAD_GLOBAL              len
              246  LOAD_FAST                'currentClass'
              248  LOAD_ATTR                tearDown_exceptions
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_CONST               0
              254  COMPARE_OP               >
          256_258  POP_JUMP_IF_FALSE   386  'to 386'

 L. 177       260  LOAD_FAST                'currentClass'
              262  LOAD_ATTR                tearDown_exceptions
              264  GET_ITER         
            266_0  COME_FROM           294  '294'
              266  FOR_ITER            298  'to 298'
              268  STORE_FAST               'exc'

 L. 178       270  LOAD_FAST                'self'
              272  LOAD_ATTR                _createClassOrModuleLevelException

 L. 179       274  LOAD_FAST                'result'
              276  LOAD_FAST                'exc'
              278  LOAD_CONST               1
              280  BINARY_SUBSCR    
              282  LOAD_STR                 'setUpClass'
              284  LOAD_FAST                'className'

 L. 180       286  LOAD_FAST                'exc'

 L. 178       288  LOAD_CONST               ('info',)
              290  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              292  POP_TOP          
          294_296  JUMP_BACK           266  'to 266'
            298_0  COME_FROM           266  '266'
              298  JUMP_FORWARD        386  'to 386'
            300_0  COME_FROM_FINALLY   118  '118'

 L. 173       300  LOAD_GLOBAL              _call_if_exists
              302  LOAD_FAST                'result'
              304  LOAD_STR                 '_restoreStdout'
              306  CALL_FUNCTION_2       2  ''
              308  POP_TOP          

 L. 174       310  LOAD_FAST                'currentClass'
              312  LOAD_ATTR                _classSetupFailed
              314  LOAD_CONST               True
              316  <117>                 0  ''
          318_320  POP_JUMP_IF_FALSE   384  'to 384'

 L. 175       322  LOAD_FAST                'currentClass'
              324  LOAD_METHOD              doClassCleanups
              326  CALL_METHOD_0         0  ''
              328  POP_TOP          

 L. 176       330  LOAD_GLOBAL              len
              332  LOAD_FAST                'currentClass'
              334  LOAD_ATTR                tearDown_exceptions
              336  CALL_FUNCTION_1       1  ''
              338  LOAD_CONST               0
              340  COMPARE_OP               >
          342_344  POP_JUMP_IF_FALSE   384  'to 384'

 L. 177       346  LOAD_FAST                'currentClass'
              348  LOAD_ATTR                tearDown_exceptions
              350  GET_ITER         
            352_0  COME_FROM           380  '380'
              352  FOR_ITER            384  'to 384'
              354  STORE_FAST               'exc'

 L. 178       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _createClassOrModuleLevelException

 L. 179       360  LOAD_FAST                'result'
              362  LOAD_FAST                'exc'
              364  LOAD_CONST               1
              366  BINARY_SUBSCR    
              368  LOAD_STR                 'setUpClass'
              370  LOAD_FAST                'className'

 L. 180       372  LOAD_FAST                'exc'

 L. 178       374  LOAD_CONST               ('info',)
              376  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              378  POP_TOP          
          380_382  JUMP_BACK           352  'to 352'
            384_0  COME_FROM           352  '352'
            384_1  COME_FROM           342  '342'
            384_2  COME_FROM           318  '318'
              384  <48>             
            386_0  COME_FROM           298  '298'
            386_1  COME_FROM           256  '256'
            386_2  COME_FROM           232  '232'
            386_3  COME_FROM           104  '104'

Parse error at or near `<121>' instruction at offset 72

    def _get_previous_module--- This code section failed: ---

 L. 183         0  LOAD_CONST               None
                2  STORE_FAST               'previousModule'

 L. 184         4  LOAD_GLOBAL              getattr
                6  LOAD_FAST                'result'
                8  LOAD_STR                 '_previousTestClass'
               10  LOAD_CONST               None
               12  CALL_FUNCTION_3       3  ''
               14  STORE_FAST               'previousClass'

 L. 185        16  LOAD_FAST                'previousClass'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 186        24  LOAD_FAST                'previousClass'
               26  LOAD_ATTR                __module__
               28  STORE_FAST               'previousModule'
             30_0  COME_FROM            22  '22'

 L. 187        30  LOAD_FAST                'previousModule'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20

    def _handleModuleFixture--- This code section failed: ---

 L. 191         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_previous_module
                4  LOAD_FAST                'result'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'previousModule'

 L. 192        10  LOAD_FAST                'test'
               12  LOAD_ATTR                __class__
               14  LOAD_ATTR                __module__
               16  STORE_FAST               'currentModule'

 L. 193        18  LOAD_FAST                'currentModule'
               20  LOAD_FAST                'previousModule'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 194        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 196        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _handleModuleTearDown
               34  LOAD_FAST                'result'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 199        40  LOAD_CONST               False
               42  LOAD_FAST                'result'
               44  STORE_ATTR               _moduleSetUpFailed

 L. 200        46  SETUP_FINALLY        62  'to 62'

 L. 201        48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                modules
               52  LOAD_FAST                'currentModule'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'module'
               58  POP_BLOCK        
               60  JUMP_FORWARD         82  'to 82'
             62_0  COME_FROM_FINALLY    46  '46'

 L. 202        62  DUP_TOP          
               64  LOAD_GLOBAL              KeyError
               66  <121>                80  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 203        74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  RETURN_VALUE     
               80  <48>             
             82_0  COME_FROM            60  '60'

 L. 204        82  LOAD_GLOBAL              getattr
               84  LOAD_FAST                'module'
               86  LOAD_STR                 'setUpModule'
               88  LOAD_CONST               None
               90  CALL_FUNCTION_3       3  ''
               92  STORE_FAST               'setUpModule'

 L. 205        94  LOAD_FAST                'setUpModule'
               96  LOAD_CONST               None
               98  <117>                 1  ''
          100_102  POP_JUMP_IF_FALSE   292  'to 292'

 L. 206       104  LOAD_GLOBAL              _call_if_exists
              106  LOAD_FAST                'result'
              108  LOAD_STR                 '_setupStdout'
              110  CALL_FUNCTION_2       2  ''
              112  POP_TOP          

 L. 207       114  SETUP_FINALLY       280  'to 280'
              116  SETUP_FINALLY       128  'to 128'

 L. 208       118  LOAD_FAST                'setUpModule'
              120  CALL_FUNCTION_0       0  ''
              122  POP_TOP          
              124  POP_BLOCK        
              126  JUMP_FORWARD        266  'to 266'
            128_0  COME_FROM_FINALLY   116  '116'

 L. 209       128  DUP_TOP          
              130  LOAD_GLOBAL              Exception
          132_134  <121>               264  ''
              136  POP_TOP          
              138  STORE_FAST               'e'
              140  POP_TOP          
              142  SETUP_FINALLY       256  'to 256'

 L. 210       144  SETUP_FINALLY       158  'to 158'

 L. 211       146  LOAD_GLOBAL              case
              148  LOAD_METHOD              doModuleCleanups
              150  CALL_METHOD_0         0  ''
              152  POP_TOP          
              154  POP_BLOCK        
              156  JUMP_FORWARD        210  'to 210'
            158_0  COME_FROM_FINALLY   144  '144'

 L. 212       158  DUP_TOP          
              160  LOAD_GLOBAL              Exception
              162  <121>               208  ''
              164  POP_TOP          
              166  STORE_FAST               'exc'
              168  POP_TOP          
              170  SETUP_FINALLY       200  'to 200'

 L. 213       172  LOAD_FAST                'self'
              174  LOAD_METHOD              _createClassOrModuleLevelException
              176  LOAD_FAST                'result'
              178  LOAD_FAST                'exc'

 L. 214       180  LOAD_STR                 'setUpModule'

 L. 215       182  LOAD_FAST                'currentModule'

 L. 213       184  CALL_METHOD_4         4  ''
              186  POP_TOP          
              188  POP_BLOCK        
              190  POP_EXCEPT       
              192  LOAD_CONST               None
              194  STORE_FAST               'exc'
              196  DELETE_FAST              'exc'
              198  JUMP_FORWARD        210  'to 210'
            200_0  COME_FROM_FINALLY   170  '170'
              200  LOAD_CONST               None
              202  STORE_FAST               'exc'
              204  DELETE_FAST              'exc'
              206  <48>             
              208  <48>             
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           156  '156'

 L. 216       210  LOAD_GLOBAL              isinstance
              212  LOAD_FAST                'result'
              214  LOAD_GLOBAL              _DebugResult
              216  CALL_FUNCTION_2       2  ''
              218  POP_JUMP_IF_FALSE   222  'to 222'

 L. 217       220  RAISE_VARARGS_0       0  'reraise'
            222_0  COME_FROM           218  '218'

 L. 218       222  LOAD_CONST               True
              224  LOAD_FAST                'result'
              226  STORE_ATTR               _moduleSetUpFailed

 L. 219       228  LOAD_FAST                'self'
              230  LOAD_METHOD              _createClassOrModuleLevelException
              232  LOAD_FAST                'result'
              234  LOAD_FAST                'e'

 L. 220       236  LOAD_STR                 'setUpModule'

 L. 221       238  LOAD_FAST                'currentModule'

 L. 219       240  CALL_METHOD_4         4  ''
              242  POP_TOP          
              244  POP_BLOCK        
              246  POP_EXCEPT       
              248  LOAD_CONST               None
              250  STORE_FAST               'e'
              252  DELETE_FAST              'e'
              254  JUMP_FORWARD        266  'to 266'
            256_0  COME_FROM_FINALLY   142  '142'
              256  LOAD_CONST               None
              258  STORE_FAST               'e'
              260  DELETE_FAST              'e'
              262  <48>             
              264  <48>             
            266_0  COME_FROM           254  '254'
            266_1  COME_FROM           126  '126'
              266  POP_BLOCK        

 L. 223       268  LOAD_GLOBAL              _call_if_exists
              270  LOAD_FAST                'result'
              272  LOAD_STR                 '_restoreStdout'
              274  CALL_FUNCTION_2       2  ''
              276  POP_TOP          
              278  JUMP_FORWARD        292  'to 292'
            280_0  COME_FROM_FINALLY   114  '114'
              280  LOAD_GLOBAL              _call_if_exists
              282  LOAD_FAST                'result'
              284  LOAD_STR                 '_restoreStdout'
              286  CALL_FUNCTION_2       2  ''
              288  POP_TOP          
              290  <48>             
            292_0  COME_FROM           278  '278'
            292_1  COME_FROM           100  '100'

Parse error at or near `<121>' instruction at offset 66

    def _createClassOrModuleLevelException(self, result, exc, method_name, parent, info=None):
        errorName = f"{method_name} ({parent})"
        self._addClassOrModuleLevelExceptionresultexcerrorNameinfo

    def _addClassOrModuleLevelException--- This code section failed: ---

 L. 232         0  LOAD_GLOBAL              _ErrorHolder
                2  LOAD_FAST                'errorName'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'error'

 L. 233         8  LOAD_GLOBAL              getattr
               10  LOAD_FAST                'result'
               12  LOAD_STR                 'addSkip'
               14  LOAD_CONST               None
               16  CALL_FUNCTION_3       3  ''
               18  STORE_FAST               'addSkip'

 L. 234        20  LOAD_FAST                'addSkip'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    56  'to 56'
               28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'exception'
               32  LOAD_GLOBAL              case
               34  LOAD_ATTR                SkipTest
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    56  'to 56'

 L. 235        40  LOAD_FAST                'addSkip'
               42  LOAD_FAST                'error'
               44  LOAD_GLOBAL              str
               46  LOAD_FAST                'exception'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_FUNCTION_2       2  ''
               52  POP_TOP          
               54  JUMP_FORWARD         90  'to 90'
             56_0  COME_FROM            38  '38'
             56_1  COME_FROM            26  '26'

 L. 237        56  LOAD_FAST                'info'
               58  POP_JUMP_IF_TRUE     78  'to 78'

 L. 238        60  LOAD_FAST                'result'
               62  LOAD_METHOD              addError
               64  LOAD_FAST                'error'
               66  LOAD_GLOBAL              sys
               68  LOAD_METHOD              exc_info
               70  CALL_METHOD_0         0  ''
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM            58  '58'

 L. 240        78  LOAD_FAST                'result'
               80  LOAD_METHOD              addError
               82  LOAD_FAST                'error'
               84  LOAD_FAST                'info'
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          
             90_0  COME_FROM            76  '76'
             90_1  COME_FROM            54  '54'

Parse error at or near `<117>' instruction at offset 24

    def _handleModuleTearDown--- This code section failed: ---

 L. 243         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_previous_module
                4  LOAD_FAST                'result'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'previousModule'

 L. 244        10  LOAD_FAST                'previousModule'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 245        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 246        22  LOAD_FAST                'result'
               24  LOAD_ATTR                _moduleSetUpFailed
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 247        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 249        32  SETUP_FINALLY        48  'to 48'

 L. 250        34  LOAD_GLOBAL              sys
               36  LOAD_ATTR                modules
               38  LOAD_FAST                'previousModule'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'module'
               44  POP_BLOCK        
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM_FINALLY    32  '32'

 L. 251        48  DUP_TOP          
               50  LOAD_GLOBAL              KeyError
               52  <121>                66  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 252        60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  RETURN_VALUE     
               66  <48>             
             68_0  COME_FROM            46  '46'

 L. 254        68  LOAD_GLOBAL              getattr
               70  LOAD_FAST                'module'
               72  LOAD_STR                 'tearDownModule'
               74  LOAD_CONST               None
               76  CALL_FUNCTION_3       3  ''
               78  STORE_FAST               'tearDownModule'

 L. 255        80  LOAD_FAST                'tearDownModule'
               82  LOAD_CONST               None
               84  <117>                 1  ''
            86_88  POP_JUMP_IF_FALSE   340  'to 340'

 L. 256        90  LOAD_GLOBAL              _call_if_exists
               92  LOAD_FAST                'result'
               94  LOAD_STR                 '_setupStdout'
               96  CALL_FUNCTION_2       2  ''
               98  POP_TOP          

 L. 257       100  SETUP_FINALLY       260  'to 260'
              102  SETUP_FINALLY       114  'to 114'

 L. 258       104  LOAD_FAST                'tearDownModule'
              106  CALL_FUNCTION_0       0  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  JUMP_FORWARD        178  'to 178'
            114_0  COME_FROM_FINALLY   102  '102'

 L. 259       114  DUP_TOP          
              116  LOAD_GLOBAL              Exception
              118  <121>               176  ''
              120  POP_TOP          
              122  STORE_FAST               'e'
              124  POP_TOP          
              126  SETUP_FINALLY       168  'to 168'

 L. 260       128  LOAD_GLOBAL              isinstance
              130  LOAD_FAST                'result'
              132  LOAD_GLOBAL              _DebugResult
              134  CALL_FUNCTION_2       2  ''
              136  POP_JUMP_IF_FALSE   140  'to 140'

 L. 261       138  RAISE_VARARGS_0       0  'reraise'
            140_0  COME_FROM           136  '136'

 L. 262       140  LOAD_FAST                'self'
              142  LOAD_METHOD              _createClassOrModuleLevelException
              144  LOAD_FAST                'result'
              146  LOAD_FAST                'e'

 L. 263       148  LOAD_STR                 'tearDownModule'

 L. 264       150  LOAD_FAST                'previousModule'

 L. 262       152  CALL_METHOD_4         4  ''
              154  POP_TOP          
              156  POP_BLOCK        
              158  POP_EXCEPT       
              160  LOAD_CONST               None
              162  STORE_FAST               'e'
              164  DELETE_FAST              'e'
              166  JUMP_FORWARD        178  'to 178'
            168_0  COME_FROM_FINALLY   126  '126'
              168  LOAD_CONST               None
              170  STORE_FAST               'e'
              172  DELETE_FAST              'e'
              174  <48>             
              176  <48>             
            178_0  COME_FROM           166  '166'
            178_1  COME_FROM           112  '112'
              178  POP_BLOCK        

 L. 266       180  LOAD_GLOBAL              _call_if_exists
              182  LOAD_FAST                'result'
              184  LOAD_STR                 '_restoreStdout'
              186  CALL_FUNCTION_2       2  ''
              188  POP_TOP          

 L. 267       190  SETUP_FINALLY       204  'to 204'

 L. 268       192  LOAD_GLOBAL              case
              194  LOAD_METHOD              doModuleCleanups
              196  CALL_METHOD_0         0  ''
              198  POP_TOP          
              200  POP_BLOCK        
              202  JUMP_FORWARD        258  'to 258'
            204_0  COME_FROM_FINALLY   190  '190'

 L. 269       204  DUP_TOP          
              206  LOAD_GLOBAL              Exception
          208_210  <121>               256  ''
              212  POP_TOP          
              214  STORE_FAST               'e'
              216  POP_TOP          
              218  SETUP_FINALLY       248  'to 248'

 L. 270       220  LOAD_FAST                'self'
              222  LOAD_METHOD              _createClassOrModuleLevelException
              224  LOAD_FAST                'result'
              226  LOAD_FAST                'e'

 L. 271       228  LOAD_STR                 'tearDownModule'

 L. 272       230  LOAD_FAST                'previousModule'

 L. 270       232  CALL_METHOD_4         4  ''
              234  POP_TOP          
              236  POP_BLOCK        
              238  POP_EXCEPT       
              240  LOAD_CONST               None
              242  STORE_FAST               'e'
              244  DELETE_FAST              'e'
              246  JUMP_FORWARD        258  'to 258'
            248_0  COME_FROM_FINALLY   218  '218'
              248  LOAD_CONST               None
              250  STORE_FAST               'e'
              252  DELETE_FAST              'e'
              254  <48>             
              256  <48>             
            258_0  COME_FROM           246  '246'
            258_1  COME_FROM           202  '202'
              258  JUMP_FORWARD        340  'to 340'
            260_0  COME_FROM_FINALLY   100  '100'

 L. 266       260  LOAD_GLOBAL              _call_if_exists
              262  LOAD_FAST                'result'
              264  LOAD_STR                 '_restoreStdout'
              266  CALL_FUNCTION_2       2  ''
              268  POP_TOP          

 L. 267       270  SETUP_FINALLY       284  'to 284'

 L. 268       272  LOAD_GLOBAL              case
              274  LOAD_METHOD              doModuleCleanups
              276  CALL_METHOD_0         0  ''
              278  POP_TOP          
              280  POP_BLOCK        
              282  JUMP_FORWARD        338  'to 338'
            284_0  COME_FROM_FINALLY   270  '270'

 L. 269       284  DUP_TOP          
              286  LOAD_GLOBAL              Exception
          288_290  <121>               336  ''
              292  POP_TOP          
              294  STORE_FAST               'e'
              296  POP_TOP          
              298  SETUP_FINALLY       328  'to 328'

 L. 270       300  LOAD_FAST                'self'
              302  LOAD_METHOD              _createClassOrModuleLevelException
              304  LOAD_FAST                'result'
              306  LOAD_FAST                'e'

 L. 271       308  LOAD_STR                 'tearDownModule'

 L. 272       310  LOAD_FAST                'previousModule'

 L. 270       312  CALL_METHOD_4         4  ''
              314  POP_TOP          
              316  POP_BLOCK        
              318  POP_EXCEPT       
              320  LOAD_CONST               None
              322  STORE_FAST               'e'
              324  DELETE_FAST              'e'
              326  JUMP_FORWARD        338  'to 338'
            328_0  COME_FROM_FINALLY   298  '298'
              328  LOAD_CONST               None
              330  STORE_FAST               'e'
              332  DELETE_FAST              'e'
              334  <48>             
              336  <48>             
            338_0  COME_FROM           326  '326'
            338_1  COME_FROM           282  '282'
              338  <48>             
            340_0  COME_FROM           258  '258'
            340_1  COME_FROM            86  '86'

Parse error at or near `<117>' instruction at offset 14

    def _tearDownPreviousClass--- This code section failed: ---

 L. 275         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'result'
                4  LOAD_STR                 '_previousTestClass'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'previousClass'

 L. 276        12  LOAD_FAST                'test'
               14  LOAD_ATTR                __class__
               16  STORE_FAST               'currentClass'

 L. 277        18  LOAD_FAST                'currentClass'
               20  LOAD_FAST                'previousClass'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 278        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 279        30  LOAD_GLOBAL              getattr
               32  LOAD_FAST                'previousClass'
               34  LOAD_STR                 '_classSetupFailed'
               36  LOAD_CONST               False
               38  CALL_FUNCTION_3       3  ''
               40  POP_JUMP_IF_FALSE    46  'to 46'

 L. 280        42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L. 281        46  LOAD_GLOBAL              getattr
               48  LOAD_FAST                'result'
               50  LOAD_STR                 '_moduleSetUpFailed'
               52  LOAD_CONST               False
               54  CALL_FUNCTION_3       3  ''
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 282        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 283        62  LOAD_GLOBAL              getattr
               64  LOAD_FAST                'previousClass'
               66  LOAD_STR                 '__unittest_skip__'
               68  LOAD_CONST               False
               70  CALL_FUNCTION_3       3  ''
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 284        74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L. 286        78  LOAD_GLOBAL              getattr
               80  LOAD_FAST                'previousClass'
               82  LOAD_STR                 'tearDownClass'
               84  LOAD_CONST               None
               86  CALL_FUNCTION_3       3  ''
               88  STORE_FAST               'tearDownClass'

 L. 287        90  LOAD_FAST                'tearDownClass'
               92  LOAD_CONST               None
               94  <117>                 1  ''
            96_98  POP_JUMP_IF_FALSE   366  'to 366'

 L. 288       100  LOAD_GLOBAL              _call_if_exists
              102  LOAD_FAST                'result'
              104  LOAD_STR                 '_setupStdout'
              106  CALL_FUNCTION_2       2  ''
              108  POP_TOP          

 L. 289       110  SETUP_FINALLY       282  'to 282'
              112  SETUP_FINALLY       124  'to 124'

 L. 290       114  LOAD_FAST                'tearDownClass'
              116  CALL_FUNCTION_0       0  ''
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        198  'to 198'
            124_0  COME_FROM_FINALLY   112  '112'

 L. 291       124  DUP_TOP          
              126  LOAD_GLOBAL              Exception
              128  <121>               196  ''
              130  POP_TOP          
              132  STORE_FAST               'e'
              134  POP_TOP          
              136  SETUP_FINALLY       188  'to 188'

 L. 292       138  LOAD_GLOBAL              isinstance
              140  LOAD_FAST                'result'
              142  LOAD_GLOBAL              _DebugResult
              144  CALL_FUNCTION_2       2  ''
              146  POP_JUMP_IF_FALSE   150  'to 150'

 L. 293       148  RAISE_VARARGS_0       0  'reraise'
            150_0  COME_FROM           146  '146'

 L. 294       150  LOAD_GLOBAL              util
              152  LOAD_METHOD              strclass
              154  LOAD_FAST                'previousClass'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'className'

 L. 295       160  LOAD_FAST                'self'
              162  LOAD_METHOD              _createClassOrModuleLevelException
              164  LOAD_FAST                'result'
              166  LOAD_FAST                'e'

 L. 296       168  LOAD_STR                 'tearDownClass'

 L. 297       170  LOAD_FAST                'className'

 L. 295       172  CALL_METHOD_4         4  ''
              174  POP_TOP          
              176  POP_BLOCK        
              178  POP_EXCEPT       
              180  LOAD_CONST               None
              182  STORE_FAST               'e'
              184  DELETE_FAST              'e'
              186  JUMP_FORWARD        198  'to 198'
            188_0  COME_FROM_FINALLY   136  '136'
              188  LOAD_CONST               None
              190  STORE_FAST               'e'
              192  DELETE_FAST              'e'
              194  <48>             
              196  <48>             
            198_0  COME_FROM           186  '186'
            198_1  COME_FROM           122  '122'
              198  POP_BLOCK        

 L. 299       200  LOAD_GLOBAL              _call_if_exists
              202  LOAD_FAST                'result'
              204  LOAD_STR                 '_restoreStdout'
              206  CALL_FUNCTION_2       2  ''
              208  POP_TOP          

 L. 300       210  LOAD_FAST                'previousClass'
              212  LOAD_METHOD              doClassCleanups
              214  CALL_METHOD_0         0  ''
              216  POP_TOP          

 L. 301       218  LOAD_GLOBAL              len
              220  LOAD_FAST                'previousClass'
              222  LOAD_ATTR                tearDown_exceptions
              224  CALL_FUNCTION_1       1  ''
              226  LOAD_CONST               0
              228  COMPARE_OP               >
          230_232  POP_JUMP_IF_FALSE   366  'to 366'

 L. 302       234  LOAD_FAST                'previousClass'
              236  LOAD_ATTR                tearDown_exceptions
              238  GET_ITER         
            240_0  COME_FROM           278  '278'
              240  FOR_ITER            280  'to 280'
              242  STORE_FAST               'exc'

 L. 303       244  LOAD_GLOBAL              util
              246  LOAD_METHOD              strclass
              248  LOAD_FAST                'previousClass'
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'className'

 L. 304       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _createClassOrModuleLevelException
              258  LOAD_FAST                'result'
              260  LOAD_FAST                'exc'
              262  LOAD_CONST               1
              264  BINARY_SUBSCR    

 L. 305       266  LOAD_STR                 'tearDownClass'

 L. 306       268  LOAD_FAST                'className'

 L. 307       270  LOAD_FAST                'exc'

 L. 304       272  LOAD_CONST               ('info',)
              274  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              276  POP_TOP          
              278  JUMP_BACK           240  'to 240'
            280_0  COME_FROM           240  '240'
              280  JUMP_FORWARD        366  'to 366'
            282_0  COME_FROM_FINALLY   110  '110'

 L. 299       282  LOAD_GLOBAL              _call_if_exists
              284  LOAD_FAST                'result'
              286  LOAD_STR                 '_restoreStdout'
              288  CALL_FUNCTION_2       2  ''
              290  POP_TOP          

 L. 300       292  LOAD_FAST                'previousClass'
              294  LOAD_METHOD              doClassCleanups
              296  CALL_METHOD_0         0  ''
              298  POP_TOP          

 L. 301       300  LOAD_GLOBAL              len
              302  LOAD_FAST                'previousClass'
              304  LOAD_ATTR                tearDown_exceptions
              306  CALL_FUNCTION_1       1  ''
              308  LOAD_CONST               0
              310  COMPARE_OP               >
          312_314  POP_JUMP_IF_FALSE   364  'to 364'

 L. 302       316  LOAD_FAST                'previousClass'
              318  LOAD_ATTR                tearDown_exceptions
              320  GET_ITER         
            322_0  COME_FROM           360  '360'
              322  FOR_ITER            364  'to 364'
              324  STORE_FAST               'exc'

 L. 303       326  LOAD_GLOBAL              util
              328  LOAD_METHOD              strclass
              330  LOAD_FAST                'previousClass'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'className'

 L. 304       336  LOAD_FAST                'self'
              338  LOAD_ATTR                _createClassOrModuleLevelException
              340  LOAD_FAST                'result'
              342  LOAD_FAST                'exc'
              344  LOAD_CONST               1
              346  BINARY_SUBSCR    

 L. 305       348  LOAD_STR                 'tearDownClass'

 L. 306       350  LOAD_FAST                'className'

 L. 307       352  LOAD_FAST                'exc'

 L. 304       354  LOAD_CONST               ('info',)
              356  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              358  POP_TOP          
          360_362  JUMP_BACK           322  'to 322'
            364_0  COME_FROM           322  '322'
            364_1  COME_FROM           312  '312'
              364  <48>             
            366_0  COME_FROM           280  '280'
            366_1  COME_FROM           230  '230'
            366_2  COME_FROM            96  '96'

Parse error at or near `<117>' instruction at offset 94


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


def _isnotsuite--- This code section failed: ---

 L. 350         0  SETUP_FINALLY        14  'to 14'

 L. 351         2  LOAD_GLOBAL              iter
                4  LOAD_FAST                'test'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          
               10  POP_BLOCK        
               12  JUMP_FORWARD         34  'to 34'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 352        14  DUP_TOP          
               16  LOAD_GLOBAL              TypeError
               18  <121>                32  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 353        26  POP_EXCEPT       
               28  LOAD_CONST               True
               30  RETURN_VALUE     
               32  <48>             
             34_0  COME_FROM            12  '12'

 L. 354        34  LOAD_CONST               False
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 18


class _DebugResult(object):
    __doc__ = 'Used by the TestSuite to hold previous class when running in debug.'
    _previousTestClass = None
    _moduleSetUpFailed = False
    shouldStop = False